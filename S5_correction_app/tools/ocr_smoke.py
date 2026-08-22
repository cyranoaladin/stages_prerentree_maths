#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle de bout en bout de la chaîne OpenRouter, sur une fixture synthétique.

Ce que ce test vérifie réellement :

* l'authentification fonctionne ;
* le modèle demandé est joignable ;
* un endpoint **ZDR sans conservation de données** existe pour lui — sinon l'appel
  échoue, et c'est le résultat attendu, pas une panne ;
* le modèle voit bien l'image ;
* il honore les sorties structurées ;
* la réponse se valide contre notre schéma ;
* le coût est récupérable.

Ce que ce test ne vérifie **pas** : la qualité de lecture d'une écriture manuscrite.
La fixture est typographique. Un modèle qui réussit ici peut échouer sur une copie
d'élève ; la qualification se fait sur des pages réelles, avec une transcription
humaine de référence.

    OPENROUTER_API_KEY=... python3 tools/ocr_smoke.py
    OPENROUTER_API_KEY=... python3 tools/ocr_smoke.py --modele qwen/qwen3-vl-8b-instruct

**Aucune copie réelle n'est utilisée**, et la clé n'est jamais affichée.
"""

import argparse
import datetime as _dt
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config                                       # noqa: E402
from app.domain import ocr_prompts, ocr_schema, openrouter    # noqa: E402

# Ce que la fixture porte, y compris une égalité fausse : un modèle qui « corrige »
# spontanément l'erreur est un modèle inadapté à la transcription de copies.
FIXTURE_LIGNES = [
    "A1.  (-8) + 3 - (-5) = -10",
    "A2.  5/8 - 1/4 = 3/8",
    "A3.  7x + 4 - 3x - 9 = 4x - 5",
]
ERREUR_DELIBEREE = "-10"

# Ce que la porte sait distinguer. Ne pas confondre « le modèle n'existe pas » avec
# « la politique le refuse » : la conduite à tenir n'est pas la même. Dans le premier
# cas on change de candidat ; dans le second, on change de candidat aussi — mais
# jamais la politique.
ETAT_DISPONIBLE = "MODEL_AVAILABLE"
ETAT_REFUSE_POLITIQUE = "MODEL_REJECTED_BY_POLICY"
ETAT_INDISPONIBLE = "MODEL_UNAVAILABLE"
ETAT_PARAMETRE = "PARAMETER_UNSUPPORTED"
ETAT_RESEAU = "NETWORK_ERROR"


def classer_echec(exc) -> str:
    """Traduit une erreur d'appel en cause opérationnelle, autant que le backend le permet."""
    from app.domain import openrouter as o
    if isinstance(exc, o.NoCompliantEndpointError):
        return ETAT_REFUSE_POLITIQUE
    if isinstance(exc, o.StructuredOutputError):
        return ETAT_PARAMETRE
    message = str(exc).lower()
    if isinstance(exc, o.OpenRouterError):
        if exc.status in (404,) or "not found" in message or "no such model" in message:
            return ETAT_INDISPONIBLE
        if ("require_parameters" in message or "unsupported" in message
                or "response_format" in message or exc.status == 422):
            return ETAT_PARAMETRE
        if exc.status in (401, 402, 403):
            return ETAT_INDISPONIBLE
        if exc.status is None or exc.retryable:
            return ETAT_RESEAU
    return ETAT_RESEAU


def fabrique_page(chemin: Path) -> Path:
    """Une page synthétique, lisible, avec une erreur volontaire. Aucun élève réel."""
    from PIL import Image, ImageDraw
    image = Image.new("RGB", (1240, 1754), "white")
    dessin = ImageDraw.Draw(image)
    police = None
    for candidat in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                     "/usr/share/fonts/TTF/DejaVuSans.ttf"):
        if Path(candidat).exists():
            from PIL import ImageFont
            police = ImageFont.truetype(candidat, 48)
            break
    y = 160
    dessin.text((90, 70), "FIXTURE SYNTHETIQUE - AUCUN ELEVE REEL",
                fill="black", font=police)
    for ligne in FIXTURE_LIGNES:
        dessin.text((90, y), ligne, fill="black", font=police)
        y += 130
    image.save(chemin, format="PNG")
    return chemin


def controle(modele, chemin: Path, verbeux=False) -> dict:
    messages = [
        {"role": "system", "content": ocr_prompts.transcription_system_prompt()},
        {"role": "user", "content": [
            {"type": "text",
             "text": ocr_prompts.transcription_user_prompt(1, 1, None)},
            {"type": "image_url",
             "image_url": {"url": openrouter.image_data_url(chemin, "image/png")}},
        ]},
    ]
    completion = openrouter.chat(messages, model=modele,
                                 response_format=ocr_schema.PAGE_RESPONSE_FORMAT,
                                 temperature=0, max_tokens=4000)
    valide = ocr_schema.validate_page(completion.parsed)
    texte = " ".join(b["verbatim"] for b in valide["blocks"])

    return {
        "modele_demande": modele,
        "modele_servi": completion.model_id,
        "fournisseur": completion.provider_name,
        "generation_id": completion.generation_id,
        "latence_ms": completion.latency_ms,
        "blocs": len(valide["blocks"]),
        "vision_confirmee": any(marque in texte for marque in ("A1", "A2", "A3", "5/8")),
        "erreur_conservee": ERREUR_DELIBEREE in texte,
        "schema_valide": True,
        "jetons_entree": completion.usage.tokens_in,
        "jetons_sortie": completion.usage.tokens_out,
        "cout_usd": completion.usage.cost_usd,
        # §13 — ce que la passerelle DIT avoir fait, pas seulement ce qu'on a demandé.
        # §10 — absence d'information n'est pas « MISS » ni « désactivé confirmé ».
        "cache_status": completion.cache_status or "NOT_REPORTED",
        "etat": ETAT_DISPONIBLE,
        "extrait": texte[:400],
    }


def enregistrer_resultat(resultats, code) -> Path:
    """Écrit le résultat de la porte live, que le verdict de préparation relira.

    La porte live n'est pas rejouable à volonté : elle demande une clé, dépend d'un
    service externe et coûte de l'argent. Son résultat est donc **écrit**, daté, et
    lu par ``tools/debt_gate.py``. Un résultat absent vaut « non exécutée » — jamais
    « réussie ».
    """
    from app import config
    reussis = [r for r in resultats if r.get("etat") == ETAT_DISPONIBLE]
    refuses = [r for r in resultats if r.get("etat") == ETAT_REFUSE_POLITIQUE]
    # Le routage est démontré si aucun appel n'a été refusé par la politique ET si les
    # contraintes ont bien été imposées à chaque appel : un « HIT » de cache, lui,
    # invaliderait la porte de confidentialité.
    cache_hit = any((r.get("cache_status") or "").upper().startswith("HIT")
                    for r in resultats)
    etat = {
        "date_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "connectivity": "PASS" if (code == 0 and len(reussis) == len(resultats)
                                   and resultats) else "FAIL",
        "privacy_routing": "PASS" if (resultats and not refuses and not cache_hit
                                      and code == 0) else "FAIL",
        "modeles": {r["modele_demande"]: r.get("etat") for r in resultats},
        "cache_status": {r["modele_demande"]: r.get("cache_status", "NOT_REPORTED")
                         for r in resultats},
        "politique": dict(openrouter.PRIVACY_PROVIDER_BLOCK),
        "fixture": "synthetique",
    }
    chemin = Path(config.RUNTIME_DIR) / "live_gate_status.json"
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(etat, ensure_ascii=False, indent=2), encoding="utf-8")
    return chemin


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--modele", default=None)
    parser.add_argument("--verifier-aussi", action="store_true",
                        help="contrôle également le modèle VERIFY")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    statut = openrouter.configuration_status()
    if not statut["configured"]:
        print("OpenRouter : clé absente. Renseignez OPENROUTER_API_KEY, ou déposez la "
              "clé dans %s avec le mode 600." % config.OPENROUTER_KEY_FILE,
              file=sys.stderr)
        if statut.get("problem"):
            print(statut["problem"], file=sys.stderr)
        return 2

    modeles = [args.modele or config.OCR_MODEL_PRIMARY]
    if args.verifier_aussi and not args.modele:
        modeles.append(config.OCR_MODEL_VERIFY)

    print("OpenRouter : configuré")
    print("contraintes imposées à chaque appel : %s"
          % json.dumps(openrouter.PRIVACY_PROVIDER_BLOCK, ensure_ascii=False))
    print()

    resultats, code = [], 0
    with tempfile.TemporaryDirectory(prefix="nexus_smoke_") as tmp:
        page = fabrique_page(Path(tmp) / "fixture_synthetique.png")
        print("fixture : %s (%d octets)" % (page.name, page.stat().st_size))
        print()
        for modele in modeles:
            try:
                resultat = controle(modele, page)
                resultats.append(resultat)
                if not args.json:
                    print("MODÈLE  %s" % modele)
                    print("  servi par        %s / %s"
                          % (resultat["modele_servi"], resultat["fournisseur"] or "?"))
                    print("  latence          %d ms" % resultat["latence_ms"])
                    print("  sortie structurée conforme au schéma : oui")
                    print("  vision           %s"
                          % ("oui" if resultat["vision_confirmee"] else
                             "DOUTEUSE — le contenu de l'image n'est pas restitué"))
                    print("  erreur conservée %s"
                          % ("oui" if resultat["erreur_conservee"] else
                             "NON — le modèle a corrigé l'erreur, ce qui le disqualifie "
                             "pour transcrire des copies"))
                    print("  jetons           %s entrée / %s sortie"
                          % (resultat["jetons_entree"], resultat["jetons_sortie"]))
                    print("  coût             %s"
                          % ("%.6f $" % resultat["cout_usd"]
                             if resultat["cout_usd"] is not None
                             else "non communiqué par le fournisseur"))
                    print("  cache passerelle %s"
                          % (resultat["cache_status"] or "non communiqué"))
                    print("  extrait          %s" % resultat["extrait"][:160])
                    print()
                if not resultat["vision_confirmee"] or not resultat["erreur_conservee"]:
                    code = 1
                # Un « HIT » signifierait que « X-OpenRouter-Cache: false » n'a pas
                # été honoré. Sur fixture synthétique, c'est un avertissement ; sur
                # une copie réelle, ce serait un échec de la porte de confidentialité.
                if (resultat["cache_status"] or "").upper().startswith("HIT"):
                    print("  ATTENTION : la passerelle annonce un cache HIT malgré "
                          "X-OpenRouter-Cache: false.\n"
                          "  Sur une copie réelle, cela vaudrait "
                          "OPENROUTER_PRIVACY_ROUTING_GATE = FAIL.")
                    code = 1
            except openrouter.OpenRouterError as exc:
                etat = classer_echec(exc)
                print("MODÈLE  %s" % modele)
                print("  ÉTAT   %s" % etat)
                if etat == ETAT_REFUSE_POLITIQUE:
                    print("  Aucun endpoint ne satisfait ZDR + data_collection=deny "
                          "pour ce modèle.\n"
                          "  L'appel est refusé, jamais rerouté. Changez de candidat "
                          "— jamais la politique.")
                print("  %s" % openrouter.redact(str(exc))[:300])
                print()
                resultats.append({"modele_demande": modele, "etat": etat,
                                  "erreur": openrouter.redact(str(exc))[:300]})
                code = 3 if etat == ETAT_REFUSE_POLITIQUE else 1

    if args.json:
        print(json.dumps(resultats, ensure_ascii=False, indent=2))
    else:
        print("ÉTATS PAR MODÈLE")
        for resultat in resultats:
            print("  %-40s %s" % (resultat["modele_demande"],
                                  resultat.get("etat", "?")))
        print()
        chemin = enregistrer_resultat(resultats, code)
        print("OCR_SMOKE = %s" % ("PASS" if code == 0 else "FAIL"))
        print("résultat enregistré : %s" % chemin)
        print("Rappel : cette fixture est typographique. La qualité de lecture "
              "manuscrite\nne s'en déduit pas et reste à mesurer sur des pages réelles.")
    return code


if __name__ == "__main__":
    sys.exit(main())
