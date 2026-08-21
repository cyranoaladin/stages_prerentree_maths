#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crée la base, applique les migrations, importe le référentiel V3, contrôle les hashes.

Aucune donnée n'est inventée : si une source manque, le script s'arrête et le dit.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                          # noqa: E402
from app.domain import immutability, importer             # noqa: E402
import migrations                                          # noqa: E402


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    force = "--force" in argv
    config.ensure_runtime()
    exists = config.DB_PATH.exists()
    if exists and not force:
        print("la base existe déjà : %s" % config.DB_PATH)
        print("relancer avec --force pour réimporter dans une base vierge "
              "(une sauvegarde est prise avant).")
        return 1
    if exists and force:
        backup = migrations.backup_database(config.DB_PATH, config.BACKUPS_DIR)
        print("sauvegarde : %s" % backup)
        config.DB_PATH.unlink()
        for suffix in ("-wal", "-shm"):
            side = Path(str(config.DB_PATH) + suffix)
            if side.exists():
                side.unlink()
        database.reset_engine()

    report = immutability.verify()
    print("immutabilité : %s (%d/%d vérifiés)"
          % (report.verdict, report.verified, report.total))
    if not report.ok:
        print("IMMUTABILITY FAILURE : import interrompu.", file=sys.stderr)
        for c in report.changed:
            print("  modifié : %s" % c["path"], file=sys.stderr)
        for m in report.missing:
            print("  manquant : %s" % m, file=sys.stderr)
        return 2

    info = migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)
    print("schéma : version %s" % info["version_apres"])
    with database.session_scope() as session:
        stats = importer.run_import(session)
    for key in ("persons", "students", "assessments", "items", "criteria",
                "virtual_criteria", "skills", "baselines", "delayed_checks", "sources"):
        print("  %-18s %d" % (key, stats[key]))
    print("base prête : %s" % config.DB_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
