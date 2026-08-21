#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstruit toute la couche post-distribution, dans l'ordre, puis contrôle le gel.

Ordre imposé : geler d'abord, produire ensuite, revérifier à la fin. Le code de sortie
vaut 0 seulement si student_artifacts_changed vaut 0 et si aucune étape n'a échoué.

`tools/make_release.py` n'est jamais appelé par ce script.
"""

import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pd_core as pd
import freeze_student_artifacts as freeze

ETAPES = [
    ("gel des artefacts élèves", ["freeze_student_artifacts.py"]),
    ("carte curriculaire critère par critère", ["build_curriculum_scope.py"]),
    ("overlays de correction", ["build_overlays.py"]),
    ("gabarits de saisie V3", ["build_response_templates.py"]),
    ("mini-test différé de semaine 2", ["build_delayed_check.py"]),
    ("audit des modules pédagogiques", ["audit_pedagogical_modules.py"]),
    ("traçabilité des sources, mode live", ["verify_sources.py", "--source-mode", "live"]),
    ("non-régression", ["verify_no_regression.py"]),
    ("documents lisibles", ["build_documents.py"]),
    ("rapport de qualité", ["build_qa.py"]),
]


def main():
    avant = freeze.verify() if os.path.exists(
        os.path.join(pd.V3_ROOT, "IMMUTABLE_STUDENT_ARTIFACTS.json")) else None
    if avant and avant["student_artifacts_changed"]:
        print("ARRÊT : les artefacts élèves ont changé avant même de commencer.",
              file=sys.stderr)
        return 1
    echecs = []
    for label, cmd in ETAPES:
        print("\n=== %s" % label)
        r = subprocess.run([sys.executable, os.path.join(HERE, cmd[0])] + cmd[1:],
                           cwd=pd.V3_ROOT)
        if r.returncode != 0:
            echecs.append(label)
    apres = freeze.verify()
    print("\n=== contrôle final")
    print("student_artifacts_changed = %d" % apres["student_artifacts_changed"])
    if echecs:
        print("étapes en échec : %s" % ", ".join(echecs), file=sys.stderr)
    ok = apres["student_artifacts_changed"] == 0 and not echecs
    print("verdict : %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
