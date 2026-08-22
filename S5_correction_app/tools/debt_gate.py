#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verdict de dette technique, **calculé** et non déclaré.

``NO_KNOWN_TECH_DEBT = PASS`` ne doit jamais être écrit à la main : un rapport
antérieur l'a fait alors que sept réserves techniques restaient ouvertes. Le verdict
se calcule ici, à partir de sources vérifiables :

* les défauts ouverts et les limitations bloquantes, lus dans le registre
  ``docs/DEBT_REGISTER.json`` ;
* les tests ignorés sans condition intrinsèque ;
* l'analyse statique ;
* la réconciliation base ↔ fichiers.

Une limitation non bloquante explicitement acceptée est rapportée séparément, sous
``PRODUCT_LIMITATION_ACCEPTED``. Elle ne masque aucune dette : elle est comptée,
nommée, et son caractère non bloquant est motivé dans le registre.

    make s5-debt-gate
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))

REGISTRE = RACINE / "docs" / "DEBT_REGISTER.json"


def charger_registre() -> dict:
    if not REGISTRE.exists():
        raise SystemExit("registre de dette absent : %s" % REGISTRE)
    return json.loads(REGISTRE.read_text(encoding="utf-8"))


def analyse_statique() -> dict:
    done = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "app", "tools", "tests", "migrations",
         "--select", "F,E9", "--output-format", "concise"],
        cwd=RACINE, capture_output=True, text=True)
    lignes = [l for l in done.stdout.splitlines() if ":" in l]
    return {"ok": done.returncode == 0, "erreurs": len(lignes),
            "detail": lignes[:5]}


def skips_non_expliques() -> dict:
    """Un test ignoré doit l'être pour une condition intrinsèque, testée et nommée."""
    done = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-rs", "--collect-only"],
        cwd=RACINE, capture_output=True, text=True)
    # La collecte ne dit rien des skips conditionnels ; on exécute la suite courte.
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rs"],
                          cwd=RACINE, capture_output=True, text=True)
    skips = [l for l in done.stdout.splitlines() if l.startswith("SKIPPED")]
    return {"tests_ok": done.returncode == 0, "skips": len(skips),
            "detail": skips}


def fsck() -> dict:
    done = subprocess.run([sys.executable, "tools/fsck.py", "--json"],
                          cwd=RACINE, capture_output=True, text=True)
    try:
        rapport = json.loads(done.stdout)
    except ValueError:
        return {"ok": False, "verdict": "FSCK ILLISIBLE"}
    return {"ok": done.returncode == 0, "verdict": rapport.get("verdict"),
            "par_gravite": rapport.get("par_gravite")}


def evaluer(inclure_tests=True) -> dict:
    registre = charger_registre()
    ouverts = [d for d in registre["defects"] if d["status"] != "CLOSED"]
    bloquantes = [l for l in registre["limitations"] if l.get("blocking")]
    acceptees = [l for l in registre["limitations"] if not l.get("blocking")]

    resultat = {
        "defects_total": len(registre["defects"]),
        "defects_open": len(ouverts),
        "defects_open_ids": [d["id"] for d in ouverts],
        "blocking_limitations": len(bloquantes),
        "blocking_limitation_ids": [l["id"] for l in bloquantes],
        "product_limitations_accepted": len(acceptees),
        "product_limitation_ids": [l["id"] for l in acceptees],
        "static": analyse_statique(),
        "fsck": fsck(),
    }
    if inclure_tests:
        resultat["tests"] = skips_non_expliques()
        resultat["unexplained_skips"] = resultat["tests"]["skips"]
    else:
        resultat["tests"] = {"tests_ok": None, "skips": None, "detail": []}
        resultat["unexplained_skips"] = None

    conditions = {
        "defects_open == 0": resultat["defects_open"] == 0,
        "blocking_limitations == 0": resultat["blocking_limitations"] == 0,
        "analyse statique sans erreur": resultat["static"]["ok"],
        "fsck PASS": resultat["fsck"]["ok"],
    }
    if inclure_tests:
        conditions["suite de tests verte"] = resultat["tests"]["tests_ok"]
        conditions["aucun skip inexpliqué"] = resultat["unexplained_skips"] == 0
    resultat["conditions"] = conditions
    resultat["verdict"] = "PASS" if all(conditions.values()) else "FAIL"
    return resultat


LIVE_ETAT = Path(__file__).resolve().parents[1] / "runtime" / "live_gate_status.json"


def statut_live() -> dict:
    """Dernier résultat connu de la porte live, ou son absence.

    La porte live n'est PAS rejouée ici : elle consomme des ressources et dépend d'un
    service externe. Le verdict de préparation lit son dernier résultat écrit, et
    considère qu'un résultat absent vaut « non exécutée » — jamais « réussie ».
    """
    if not LIVE_ETAT.exists():
        return {"connectivity": "NOT_RUN", "privacy_routing": "NOT_RUN",
                "raison": "aucun résultat de porte live enregistré"}
    try:
        return json.loads(LIVE_ETAT.read_text(encoding="utf-8"))
    except ValueError:
        return {"connectivity": "NOT_RUN", "privacy_routing": "NOT_RUN",
                "raison": "résultat de porte live illisible"}


def preparation_pilote(full_gate_ok: bool) -> dict:
    """PILOT_SOFTWARE_READY = full gate ET connectivité live ET routage live.

    Trois portes, trois preuves distinctes. La qualité de lecture manuscrite n'entre
    pas dans ce calcul : elle reste NOT_RUN jusqu'au premier vrai benchmark, et c'est
    précisément pour la mesurer que le pilote peut démarrer.
    """
    live = statut_live()
    conditions = {
        "S5_FULL_GATE": full_gate_ok,
        "OPENROUTER_LIVE_CONNECTIVITY_GATE": live.get("connectivity") == "PASS",
        "OPENROUTER_PRIVACY_ROUTING_GATE": live.get("privacy_routing") == "PASS",
    }
    return {"conditions": conditions, "live": live,
            "PILOT_SOFTWARE_READY": "YES" if all(conditions.values()) else "NO",
            "HANDWRITING_REAL_ACCURACY_GATE": "NOT_RUN"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sans-tests", action="store_true",
                        help="ne relance pas la suite (elle tourne déjà dans la porte)")
    args = parser.parse_args(argv)

    resultat = evaluer(inclure_tests=not args.sans_tests)
    if args.json:
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
        return 0 if resultat["verdict"] == "PASS" else 1

    print("REGISTRE DE DETTE")
    print("  défauts enregistrés            %d" % resultat["defects_total"])
    print("  REMAINING_TECH_DEBT            %d %s"
          % (resultat["defects_open"], resultat["defects_open_ids"] or ""))
    print("  REMAINING_BLOCKING_LIMITATIONS %d %s"
          % (resultat["blocking_limitations"], resultat["blocking_limitation_ids"] or ""))
    print("  PRODUCT_LIMITATION_ACCEPTED    %d %s"
          % (resultat["product_limitations_accepted"],
             ", ".join(resultat["product_limitation_ids"]) or "—"))
    print()
    print("CONTRÔLES")
    for nom, ok in resultat["conditions"].items():
        print("  %-32s %s" % (nom, "OK" if ok else "ÉCHEC"))
    if resultat["tests"]["detail"]:
        print()
        print("  skips relevés :")
        for ligne in resultat["tests"]["detail"]:
            print("    %s" % ligne)
    print()
    print("NO_KNOWN_TECH_DEBT = %s" % resultat["verdict"])
    print("(verdict calculé — il n'est écrit nulle part en dur)")
    print()

    preparation = preparation_pilote(resultat["verdict"] == "PASS")
    print("PRÉPARATION DU PILOTE")
    for nom, ok in preparation["conditions"].items():
        print("  %-38s %s" % (nom, "PASS" if ok else "NON DÉMONTRÉ"))
    if preparation["live"].get("raison"):
        print("  (%s)" % preparation["live"]["raison"])
    print()
    print("PILOT_SOFTWARE_READY = %s" % preparation["PILOT_SOFTWARE_READY"])
    print("HANDWRITING_REAL_ACCURACY_GATE = %s   ← mesurable seulement sur une vraie "
          "copie" % preparation["HANDWRITING_REAL_ACCURACY_GATE"])
    return 0 if resultat["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
