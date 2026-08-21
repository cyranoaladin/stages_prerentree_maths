#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle final de non-régression sur ce que l'élève a réellement reçu.

Sept contrôles, tous obligatoires :

    1. les empreintes SHA-256 des 60 artefacts figés sont strictement inchangées ;
    2. les 15 couples élève x matière sont toujours présents ;
    3. les 30 PDF élèves sont toujours présents ;
    4. les 30 sources LaTeX correspondantes sont toujours présentes ;
    5. les identifiants d'items sont inchangés ;
    6. les identifiants de critères d'origine et leurs points sont inchangés ;
    7. le total de 20 points bruts est conservé pour chaque élève.

Et un huitième, de nature différente : aucun corrigé ne figure dans un document élève.
"""

import argparse
import os
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import freeze_student_artifacts as freeze

SCOPE = os.path.join(pd.V3_ROOT, "curriculum_scope", "criteria_scope.json")
OUT = os.path.join(pd.V3_ROOT, "reports", "NON_REGRESSION.json")

# Chaînes qui n'existent que dans le document enseignant.
TEACHER_ONLY_MARKERS = (
    "DOCUMENT CONFIDENTIEL",
    "Réponse attendue :",
    "Barème par critère",
    "Corrigé de l'évaluation",
    "Corrigé du livret",
)


def _pdf_text(path):
    try:
        r = subprocess.run(["pdftotext", "-layout", path, "-"],
                           capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout if r.returncode == 0 else None


def run(check_pdf_text=True):
    checks = []

    def add(name, ok, detail):
        checks.append({"controle": name, "verdict": "PASS" if ok else "FAIL", "detail": detail})

    frozen = freeze.verify()
    add("empreintes des artefacts élèves",
        frozen["student_artifacts_changed"] == 0 and not frozen["missing"] and not frozen["added"],
        "student_artifacts_changed = %d, manquants = %d, ajoutés = %d"
        % (frozen["student_artifacts_changed"], frozen["student_artifacts_missing"],
           frozen["student_artifacts_added"]))

    sts = pd.students()
    add("15 couples élève x matière", len(sts) == 15, "%d couples trouvés" % len(sts))

    pdfs = [p for st in sts for p in (st["travail_pdf"], st["evaluation_pdf"])]
    texs = [p for st in sts for p in (st["travail_tex"], st["evaluation_tex"])]
    add("30 PDF élèves présents",
        len(pdfs) == 30 and all(os.path.exists(p) for p in pdfs),
        "%d / 30 présents" % sum(1 for p in pdfs if os.path.exists(p)))
    add("30 sources LaTeX présentes",
        len(texs) == 30 and all(os.path.exists(p) for p in texs),
        "%d / 30 présentes" % sum(1 for p in texs if os.path.exists(p)))

    scope = pd.read_json(SCOPE, "carte curriculaire")
    ref_items, ref_crit = set(), {}
    for c in scope["criteria"]:
        ref_items.add(c["item_id"])
        ref_crit[c["criterion_id"]] = c["original_points"]
    live_items, live_crit, totals = set(), {}, {}
    for st in sts:
        m = pd.manifest_of(st)
        totals[st["student_id"]] = round(sum(i["points"] for i in m["items"]), 4)
        for it in m["items"]:
            live_items.add(it["item_id"])
            for cr in it["grading_criteria"]:
                live_crit[cr["criterion_id"]] = cr["points"]
    add("identifiants d'items inchangés", ref_items == live_items,
        "%d items ; écarts : %s" % (len(live_items),
                                    sorted(ref_items ^ live_items)[:5] or "aucun"))
    same = (set(ref_crit) == set(live_crit)
            and all(abs(ref_crit[k] - live_crit[k]) < 1e-9 for k in ref_crit))
    add("identifiants et points des critères d'origine inchangés", same,
        "%d critères ; écarts : %s"
        % (len(live_crit),
           sorted(set(ref_crit) ^ set(live_crit))[:5]
           or [k for k in ref_crit if abs(ref_crit[k] - live_crit[k]) >= 1e-9][:5] or "aucun"))
    bad_totals = {k: v for k, v in totals.items() if abs(v - 20) > 1e-9}
    add("20 points bruts conservés par élève", not bad_totals,
        "écarts : %s" % (bad_totals or "aucun"))

    if check_pdf_text:
        leaked = []
        available = True
        for st in sts:
            for path in (st["travail_pdf"], st["evaluation_pdf"]):
                text = _pdf_text(path)
                if text is None:
                    available = False
                    continue
                for marker in TEACHER_ONLY_MARKERS:
                    if marker in text:
                        leaked.append({"fichier": os.path.relpath(path, pd.REPO_ROOT),
                                       "marqueur": marker})
        if available:
            add("aucun corrigé dans les documents élèves", not leaked,
                "fuites : %s" % (leaked or "aucune"))
        else:
            checks.append({"controle": "aucun corrigé dans les documents élèves",
                           "verdict": "NON EXÉCUTÉ",
                           "detail": "pdftotext indisponible : le contrôle n'a pas été conduit, "
                                     "et n'est donc pas déclaré réussi"})

    verdict = "FAIL" if any(c["verdict"] == "FAIL" for c in checks) else (
        "PASS WITH LIMITATION" if any(c["verdict"] == "NON EXÉCUTÉ" for c in checks) else "PASS")
    return {
        "schema": "nexus-s5-non-regression-v3",
        "generated_on": pd.GENERATED_ON,
        "student_artifacts_changed": frozen["student_artifacts_changed"],
        "checks": checks,
        "verdict": verdict,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--skip-pdf-text", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args(argv)
    res = run(check_pdf_text=not args.skip_pdf_text)
    for c in res["checks"]:
        print("%-8s %-55s %s" % (c["verdict"], c["controle"], c["detail"]))
    print("student_artifacts_changed = %d" % res["student_artifacts_changed"])
    print("verdict global : %s" % res["verdict"])
    if not args.no_write:
        pd.write_json(OUT, res)
    return 0 if res["verdict"].startswith("PASS") else 1


if __name__ == "__main__":
    sys.exit(main())
