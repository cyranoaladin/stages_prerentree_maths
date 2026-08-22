#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle d'intégrité complet, à lancer avant et après toute campagne de correction."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                          # noqa: E402
from app.domain import immutability, importer             # noqa: E402


def main() -> int:
    report = immutability.verify()
    summary = report.summary()
    print("== Documents distribués")
    for key, value in summary.items():
        print("  %-32s %s" % (key, value))
    for changed in report.changed:
        print("  MODIFIÉ  %s" % changed["path"])
    for missing in report.missing:
        print("  MANQUANT %s" % missing)

    drift = []
    if config.DB_PATH.exists():
        with database.session_scope() as session:
            drift = importer.check_sources_unchanged(session)
    print("== Référentiel V3 importé")
    if not config.DB_PATH.exists():
        print("  base absente : rien à comparer")
    elif drift:
        for row in drift:
            print("  DÉRIVE   %s (%s)" % (row["source_path"], row["etat"]))
    else:
        print("  toutes les sources importées sont inchangées")

    ok = report.ok and not drift
    print("verdict : %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
