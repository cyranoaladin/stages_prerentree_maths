#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Réimport explicite du référentiel V3 dans une base vierge.

Cet outil ne synchronise jamais en silence : il refuse une base déjà peuplée, et
demande de repartir d'une base neuve après sauvegarde. Une dérive de source est une
décision, pas un automatisme.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                          # noqa: E402
from app.domain import immutability, importer             # noqa: E402


def main() -> int:
    report = immutability.verify()
    if not report.ok:
        print("IMMUTABILITY FAILURE : import refusé.", file=sys.stderr)
        return 2
    with database.session_scope() as session:
        drift = importer.check_sources_unchanged(session)
        if drift:
            print("Sources ayant changé depuis le dernier import :")
            for row in drift:
                print("  %s (%s)" % (row["source_path"], row["etat"]))
        try:
            stats = importer.run_import(session)
        except importer.ImportError_ as exc:
            print("REFUS : %s" % exc, file=sys.stderr)
            print("Pour réimporter : sauvegardez, puis lancez "
                  "tools/init_database.py --force", file=sys.stderr)
            return 1
    for key, value in sorted(stats.items()):
        print("  %-18s %s" % (key, value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
