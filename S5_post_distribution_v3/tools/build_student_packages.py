#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Paquet par élève — pour l'avenir seulement.

Les documents ayant déjà été distribués, aucune nouvelle distribution n'est nécessaire
aujourd'hui. Ce script existe pour les prochaines séances : il produit, par élève, un
paquet ne contenant strictement que ce qui lui revient.

    <student_id>/
        S5_TRAVAIL_<...>.pdf
        S5_EVALUATION_<...>.pdf
        MANIFEST.json

Aucun corrigé. Aucun autre élève. Aucun profil interne. Aucun document enseignant.

Les PDF sont copiés en lecture depuis S5_cloture ; les originaux ne sont jamais touchés,
et leur empreinte est recontrôlée après copie.
"""

import argparse
import os
import shutil
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import freeze_student_artifacts as freeze

INTERDIT = ("answer_key", "_ENSEIGNANT", "manifest", "profile", "corrige", "bareme",
            "responses", "blueprint")


def build(dest, only=None, dry_run=False):
    dest = os.path.abspath(dest)
    home = os.path.abspath(os.path.expanduser("~"))
    if dest in {os.path.abspath(os.sep), home, pd.REPO_ROOT, pd.S5_ROOT, pd.V3_ROOT}:
        raise pd.PostDistributionError("destination refusée : %s" % dest)
    if dest.startswith(pd.S5_ROOT + os.sep):
        raise pd.PostDistributionError("aucune écriture dans S5_cloture")
    before = freeze.verify()
    if before["student_artifacts_changed"]:
        raise pd.PostDistributionError(
            "les artefacts élèves ont changé : aucune distribution n'est produite tant que le "
            "gel n'est pas rétabli")
    made = []
    for st in pd.students():
        if only and st["student_id"] not in only:
            continue
        files = [st["travail_pdf"], st["evaluation_pdf"]]
        entries = [{"fichier": os.path.basename(p), "sha256": pd.sha256(p),
                    "octets": os.path.getsize(p)} for p in files]
        manifest = {
            "schema": "nexus-s5-student-package-v3",
            "generated_on": pd.GENERATED_ON,
            "student_id": st["student_id"],
            "student_name": st["student_name"],
            "level_label": st["level_label"],
            "subject": st["subject"],
            "contenu": entries,
            "ne_contient_pas": ["corrigé", "barème", "profil d'apprentissage",
                                "document enseignant", "tout autre élève"],
        }
        for e in entries:
            low = e["fichier"].lower()
            if any(bad in low for bad in INTERDIT):
                raise pd.PostDistributionError(
                    "fichier au nom suspect dans un paquet élève : %s" % e["fichier"])
        made.append((st, files, manifest))
        if dry_run:
            continue
        d = os.path.join(dest, st["student_id"])
        os.makedirs(d, exist_ok=True)
        for p in files:
            shutil.copy2(p, os.path.join(d, os.path.basename(p)))
        import json
        with open(os.path.join(d, "MANIFEST.json"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
            f.write("\n")
    after = freeze.verify()
    if after["student_artifacts_changed"]:
        raise pd.PostDistributionError("les originaux ont été modifiés pendant la copie")
    return made


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dest", required=True)
    ap.add_argument("--student", action="append", dest="only")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    try:
        made = build(args.dest, args.only, args.dry_run)
    except pd.PostDistributionError as exc:
        print("REFUS : %s" % exc, file=sys.stderr)
        return 2
    print("%s%d paquet(s) élève : 2 PDF et un manifeste chacun, aucun corrigé."
          % ("--dry-run : " if args.dry_run else "", len(made)))
    for st, files, _ in made:
        print("  %-22s %s" % (st["student_id"], ", ".join(os.path.basename(f) for f in files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
