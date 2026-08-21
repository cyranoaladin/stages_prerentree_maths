#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gel des artefacts élèves distribués : empreinte, puis contrôle de non-régression.

Les 30 PDF réellement imprimés et distribués constituent la référence
contractuelle. Les 30 sources LaTeX correspondantes sont gelées avec eux : sans
cela, la source et le document remis à l'élève pourraient diverger sans que rien
ne le signale.

    python3 tools/freeze_student_artifacts.py            écrit IMMUTABLE_STUDENT_ARTIFACTS.json
    python3 tools/freeze_student_artifacts.py --verify    recalcule et compare, n'écrit rien

En mode --verify, le code de sortie vaut 0 si et seulement si
``student_artifacts_changed`` vaut 0.
"""

import argparse
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

OUT = os.path.join(pd.V3_ROOT, "IMMUTABLE_STUDENT_ARTIFACTS.json")

KINDS = (
    ("travail_pdf", "travail", "pdf"),
    ("travail_tex", "travail", "tex"),
    ("evaluation_pdf", "evaluation", "pdf"),
    ("evaluation_tex", "evaluation", "tex"),
)


def collect():
    rows = []
    for st in pd.students():
        for key, nature, fmt in KINDS:
            path = st[key]
            if not os.path.exists(path):
                raise pd.PostDistributionError(
                    "artefact élève distribué introuvable : %s" % path)
            rows.append({
                "path": os.path.relpath(path, pd.REPO_ROOT),
                "student_id": st["student_id"],
                "student_name": st["student_name"],
                "level_key": st["level_key"],
                "level_label": st["level_label"],
                "subject": st["subject"],
                "nature": nature,
                "format": fmt,
                "sha256": pd.sha256(path),
                "size_bytes": os.path.getsize(path),
                "status": "distributed",
                "mutability": "immutable",
            })
    rows.sort(key=lambda r: r["path"])
    return rows


def build():
    rows = collect()
    pdfs = [r for r in rows if r["format"] == "pdf"]
    texs = [r for r in rows if r["format"] == "tex"]
    return {
        "schema": "nexus-s5-immutable-student-artifacts-v3",
        "generated_on": pd.GENERATED_ON,
        "objet": ("empreinte des documents réellement imprimés et distribués aux élèves. "
                  "Toute divergence ultérieure d'un seul octet rend la mission FAIL."),
        "regle": ("les fichiers listés ici ne doivent être ni modifiés, ni régénérés, ni "
                  "recompilés, ni remplacés. La couche post-distribution ne fait que les lire."),
        "reference_root": "Nexus_Reussite_Documentation_Stages_Maths_2026",
        "counts": {
            "couples_eleve_matiere": len(pd.students()),
            "student_pdf": len(pdfs),
            "student_tex": len(texs),
            "total": len(rows),
        },
        "artifacts": rows,
    }


def verify():
    if not os.path.exists(OUT):
        raise pd.PostDistributionError(
            "IMMUTABLE_STUDENT_ARTIFACTS.json absent : lancer d'abord le gel sans --verify")
    ref = pd.read_json(OUT, "manifeste de gel")
    known = {r["path"]: r for r in ref["artifacts"]}
    changed, missing, added = [], [], []
    for path, row in sorted(known.items()):
        full = os.path.join(pd.REPO_ROOT, path)
        if not os.path.exists(full):
            missing.append(path)
            continue
        got = pd.sha256(full)
        if got != row["sha256"]:
            changed.append({"path": path, "expected": row["sha256"], "observed": got,
                            "expected_size": row["size_bytes"],
                            "observed_size": os.path.getsize(full)})
    for row in collect():
        if row["path"] not in known:
            added.append(row["path"])
    return {
        "checked_on": pd.GENERATED_ON,
        "student_artifacts_expected": len(known),
        "student_artifacts_changed": len(changed),
        "student_artifacts_missing": len(missing),
        "student_artifacts_added": len(added),
        "changed": changed,
        "missing": missing,
        "added": added,
        "verdict": "PASS" if not (changed or missing or added) else "FAIL",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--verify", action="store_true",
                    help="recalcule les empreintes et les compare au manifeste de gel")
    args = ap.parse_args(argv)
    if args.verify:
        res = verify()
        print("artefacts élèves attendus : %d" % res["student_artifacts_expected"])
        print("student_artifacts_changed = %d" % res["student_artifacts_changed"])
        print("student_artifacts_missing = %d" % res["student_artifacts_missing"])
        print("student_artifacts_added   = %d" % res["student_artifacts_added"])
        for c in res["changed"]:
            print("  MODIFIÉ %s" % c["path"])
        for m in res["missing"]:
            print("  MANQUANT %s" % m)
        print("verdict : %s" % res["verdict"])
        return 0 if res["verdict"] == "PASS" else 1
    obj = build()
    pd.write_json(OUT, obj)
    print("gel écrit : %s" % os.path.relpath(OUT, pd.REPO_ROOT))
    print("  %d couples élève x matière" % obj["counts"]["couples_eleve_matiere"])
    print("  %d PDF élèves, %d sources LaTeX, %d fichiers gelés"
          % (obj["counts"]["student_pdf"], obj["counts"]["student_tex"], obj["counts"]["total"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
