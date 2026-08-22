#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comparaison de modèles de lecture sur des pages données.

L'outil mesure ; il ne décrète pas. Aucun modèle n'est « le meilleur » parce qu'il
est connu, récent ou cher : il l'est parce qu'il lit mieux **nos** copies.

    # comparer plusieurs modèles sur les pages rendues d'une copie ; sans --modeles,
    # ce sont les défauts de config.py — l'unique autorité — qui sont employés
    python3 tools/ocr_benchmark.py --eleve sinda-chikhaoui
    python3 tools/ocr_benchmark.py --eleve sinda-chikhaoui --modeles <a> <b> <c>

    Les candidats se choisissent au catalogue **du jour** (make s5-ocr-modeles). Un
    modèle refusé par la politique de routage à une date donnée reste un candidat
    légitime : la compatibilité fournisseur change. La politique, elle, ne change pas.

    # avec une transcription humaine de référence
    python3 tools/ocr_benchmark.py --eleve ines-kefi --reference reference.json

Deux régimes de mesure, et l'outil ne les confond jamais :

**Sans référence humaine** — il mesure ce qui est mesurable sans vérité : latence,
coût, nombre de blocs, blocs mathématiques, ratures relevées, incertitudes déclarées,
rattachement aux items, et **accord entre modèles**. L'accord n'est pas la justesse :
deux modèles peuvent se tromper de la même façon.

**Avec référence humaine** — il ajoute les mesures qui exigent une vérité : taux
d'erreur caractère (CER), correspondance exacte des expressions mathématiques, signes
mathématiques erronés, omissions et hallucinations.

Le fichier de référence est une transcription humaine, au format ::

    {"pages": {"1": [{"block_id": "...", "item_ref": "A1", "verbatim": "...",
                      "kind": "MATH", "status": "ACTIVE"}]}}

Sans ce fichier, les colonnes de qualité restent vides. **Aucune métrique de qualité
n'est fabriquée** : ce qui n'a pas été mesuré ne s'affiche pas.
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                            # noqa: E402
from app.domain import ocr_prompts, ocr_schema, openrouter  # noqa: E402
from app.domain import source_copy as sc                    # noqa: E402
from app.domain import transcription                        # noqa: E402
from app.models import Assessment                           # noqa: E402

# Signes dont la confusion change le sens d'une réponse, et qu'on compte séparément.
SIGNES_SENSIBLES = "-−+×÷/^_()[]{}=<>≤≥≠,.%°√"


def normaliser(texte: str) -> str:
    return " ".join((texte or "").split()).replace("−", "-")


def distance_levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    precedente = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        courante = [i]
        for j, cb in enumerate(b, start=1):
            courante.append(min(precedente[j] + 1, courante[j - 1] + 1,
                                precedente[j - 1] + (ca != cb)))
        precedente = courante
    return precedente[-1]


def cer(reference: str, hypothese: str):
    """Taux d'erreur caractère. ``None`` si la référence est vide."""
    ref, hyp = normaliser(reference), normaliser(hypothese)
    if not ref:
        return None
    return distance_levenshtein(ref, hyp) / len(ref)


def signes(texte: str) -> str:
    return "".join(c for c in normaliser(texte) if c in SIGNES_SENSIBLES)


def lire_page(modele, chemin, page_index, page_total, hints):
    """Un appel de lecture, chronométré. Les contraintes de confidentialité s'appliquent."""
    messages = [
        {"role": "system", "content": ocr_prompts.transcription_system_prompt()},
        {"role": "user", "content": [
            {"type": "text",
             "text": ocr_prompts.transcription_user_prompt(page_index, page_total,
                                                           hints)},
            {"type": "image_url",
             "image_url": {"url": openrouter.image_data_url(chemin, "image/png")}},
        ]},
    ]
    debut = time.monotonic()
    completion = openrouter.chat(messages, model=modele,
                                 response_format=ocr_schema.PAGE_RESPONSE_FORMAT,
                                 temperature=0)
    valide = ocr_schema.validate_page(completion.parsed)
    valide["page_index"] = page_index
    return {
        "page_index": page_index,
        "blocs": valide["blocks"],
        "latence_ms": int((time.monotonic() - debut) * 1000),
        "jetons_entree": completion.usage.tokens_in,
        "jetons_sortie": completion.usage.tokens_out,
        "cout_usd": completion.usage.cost_usd,
        "fournisseur": completion.provider_name,
        "modele_servi": completion.model_id,
    }


def mesures_sans_reference(pages) -> dict:
    blocs = [b for p in pages for b in p["blocs"]]
    couts = [p["cout_usd"] for p in pages if p["cout_usd"] is not None]
    return {
        "pages": len(pages),
        "blocs": len(blocs),
        "manuscrits": sum(1 for b in blocs if b["origin"] == "HANDWRITTEN"),
        "mathematiques": sum(1 for b in blocs if b["kind"] in ("MATH", "MIXED")),
        "ratures": sum(1 for b in blocs if b["status"] == "CROSSED_OUT"),
        "incertains": sum(1 for b in blocs if b["uncertainty"] != "LOW"),
        "illisibles": sum(1 for b in blocs if "[illisible]" in (b["verbatim"] or "")),
        "avec_item_ref": sum(1 for b in blocs if b["item_ref"]),
        "avec_latex": sum(1 for b in blocs if b["latex"]),
        "latence_ms_totale": sum(p["latence_ms"] for p in pages),
        "latence_ms_par_page": round(sum(p["latence_ms"] for p in pages) / max(1, len(pages))),
        "jetons_entree": sum(p["jetons_entree"] or 0 for p in pages),
        "jetons_sortie": sum(p["jetons_sortie"] or 0 for p in pages),
        "cout_usd": round(sum(couts), 6) if couts else None,
        "cout_par_page_usd": round(sum(couts) / max(1, len(pages)), 6) if couts else None,
    }


def mesures_avec_reference(pages, reference) -> dict:
    """Mesures de qualité. Exigent une transcription humaine, et le disent sinon."""
    total_cer, apparies, exacts_math, signes_faux = [], 0, 0, 0
    attendus, omissions, hallucinations = 0, 0, 0
    items_corrects = 0
    for page in pages:
        refs = reference.get("pages", {}).get(str(page["page_index"]), [])
        attendus += len(refs)
        par_id = {b["block_id"]: b for b in page["blocs"]}
        vus = set()
        for attendu in refs:
            candidat = par_id.get(attendu.get("block_id"))
            if candidat is None:
                # Appariement de repli, par item et par nature.
                candidats = [b for b in page["blocs"]
                             if b["item_ref"] == attendu.get("item_ref")
                             and b["block_id"] not in vus]
                candidat = candidats[0] if candidats else None
            if candidat is None:
                omissions += 1
                continue
            vus.add(candidat["block_id"])
            apparies += 1
            valeur = cer(attendu["verbatim"], candidat["verbatim"])
            if valeur is not None:
                total_cer.append(valeur)
            if normaliser(attendu["verbatim"]) == normaliser(candidat["verbatim"]):
                if attendu.get("kind") in ("MATH", "MIXED"):
                    exacts_math += 1
            elif signes(attendu["verbatim"]) != signes(candidat["verbatim"]):
                signes_faux += 1
            if attendu.get("item_ref") and attendu["item_ref"] == candidat["item_ref"]:
                items_corrects += 1
        hallucinations += len([b for b in page["blocs"] if b["block_id"] not in vus])

    math_attendus = sum(1 for p in reference.get("pages", {}).values()
                        for b in p if b.get("kind") in ("MATH", "MIXED"))
    return {
        "blocs_de_reference": attendus,
        "apparies": apparies,
        "omissions": omissions,
        "blocs_non_apparies": hallucinations,
        "cer_moyen": round(sum(total_cer) / len(total_cer), 4) if total_cer else None,
        "math_exacts": exacts_math,
        "math_attendus": math_attendus,
        "signes_mathematiques_errones": signes_faux,
        "items_correctement_rattaches": items_corrects,
    }


def accord_entre_modeles(resultats) -> dict:
    """Combien de blocs se lisent pareil chez tous les modèles. Ce n'est pas la justesse."""
    if len(resultats) < 2 :
        return {}
    par_modele = {}
    for nom, donnees in resultats.items():
        textes = {}
        for page in donnees["pages"]:
            for bloc in page["blocs"]:
                cle = (page["page_index"], bloc["item_ref"], bloc["block_id"])
                textes[cle] = normaliser(bloc["verbatim"])
        par_modele[nom] = textes
    communes = set.intersection(*(set(t) for t in par_modele.values()))
    identiques = sum(1 for cle in communes
                     if len({t[cle] for t in par_modele.values()}) == 1)
    return {"blocs_communs": len(communes), "lectures_identiques": identiques,
            "note": "l'accord n'est pas la justesse : deux modèles peuvent se tromper "
                    "de la même manière."}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--eleve", required=True)
    parser.add_argument("--modeles", nargs="+", default=None)
    parser.add_argument("--reference", default=None,
                        help="transcription humaine de référence (JSON)")
    parser.add_argument("--pages", type=int, default=None,
                        help="limiter aux N premières pages")
    parser.add_argument("--sortie", default=None)
    args = parser.parse_args(argv)

    if not openrouter.is_configured():
        print("OpenRouter : clé absente.", file=sys.stderr)
        return 2

    modeles = args.modeles or [config.OCR_MODEL_PRIMARY, config.OCR_MODEL_VERIFY]
    reference = None
    if args.reference:
        reference = json.loads(Path(args.reference).read_text(encoding="utf-8"))

    import migrations
    migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)

    with database.session_scope() as session:
        assessment = (session.query(Assessment)
                      .filter_by(student_id=args.eleve).one_or_none())
        if assessment is None:
            print("élève inconnu : %s" % args.eleve, file=sys.stderr)
            return 1
        original = sc.current_copy(session, assessment.assessment_id)
        if original is None:
            print("aucune copie rattachée à %s." % args.eleve, file=sys.stderr)
            return 1
        derived = sc.derived_pages(session, original)
        if derived is None:
            print("les pages ne sont pas rendues. Lancez d'abord la rastérisation.",
                  file=sys.stderr)
            return 1
        chemins = [(r.page_index, sc.stored_path(r))
                   for r in sc.files_of(session, derived)]
        if args.pages:
            chemins = chemins[:args.pages]
        hints = transcription.item_hints(session, assessment)

    resultats = {}
    for modele in modeles:
        print("lecture par %s (%d page(s))…" % (modele, len(chemins)))
        pages, erreur = [], None
        for page_index, chemin in chemins:
            try:
                pages.append(lire_page(modele, chemin, page_index, len(chemins), hints))
            except openrouter.OpenRouterError as exc:
                erreur = openrouter.redact(str(exc))[:300]
                print("  page %d : échec — %s" % (page_index, erreur))
                break
        donnees = {"pages": pages, "erreur": erreur,
                   "mesures": mesures_sans_reference(pages) if pages else {}}
        if reference and pages:
            donnees["qualite"] = mesures_avec_reference(pages, reference)
        resultats[modele] = donnees

    rapport = {
        "eleve": args.eleve,
        "modeles": modeles,
        "prompt_version": ocr_prompts.TRANSCRIPTION_PROMPT_VERSION,
        "schema_version": ocr_schema.SCHEMA_VERSION,
        "reference_humaine": bool(reference),
        "resultats": resultats,
        "accord": accord_entre_modeles({k: v for k, v in resultats.items()
                                        if v["pages"]}),
    }
    if not reference:
        rapport["avertissement"] = (
            "Aucune transcription humaine de référence : les mesures de qualité "
            "(CER, exactitude mathématique, omissions, hallucinations) ne sont pas "
            "calculées. Elles ne peuvent pas l'être sans vérité.")

    sortie = json.dumps(rapport, ensure_ascii=False, indent=2)
    if args.sortie:
        Path(args.sortie).write_text(sortie, encoding="utf-8")
        print("rapport écrit : %s" % args.sortie)
    else:
        print(sortie)
    return 0


if __name__ == "__main__":
    sys.exit(main())
