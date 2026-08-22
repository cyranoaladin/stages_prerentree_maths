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


CONFIRMATION = "--je-confirme-la-perte-des-corrections-reelles"


def real_corrections(db_path) -> list:
    """Corrections non synthétiques portant des données saisies.

    Une base vierge, ou une base ne contenant que des coquilles ouvertes sans
    aucun score, n'est pas « réelle » : il n'y a rien à perdre. Dès qu'un score,
    une observation ou un bilan existe, la base cesse d'être remplaçable.
    """
    import sqlite3
    if not Path(db_path).exists():
        return []
    connexion = sqlite3.connect(str(db_path))
    try:
        colonnes = {r[1] for r in connexion.execute("PRAGMA table_info(correction)")}
        filtre = "AND c.is_synthetic = 0" if "is_synthetic" in colonnes else ""
        lignes = connexion.execute(
            """SELECT c.correction_id, c.assessment_id, c.status,
                      (SELECT COUNT(*) FROM criterion_response r
                        WHERE r.correction_id = c.correction_id
                          AND r.score_centi IS NOT NULL),
                      (SELECT COUNT(*) FROM criterion_response r
                        WHERE r.correction_id = c.correction_id
                          AND TRIM(COALESCE(r.observation, '')) <> '')
                 FROM correction c WHERE 1=1 %s""" % filtre).fetchall()
        reelles = []
        for correction_id, assessment_id, statut, scores, observations in lignes:
            if scores or observations:
                reelles.append({"correction_id": correction_id,
                                "assessment_id": assessment_id, "status": statut,
                                "scores": scores, "observations": observations})
        return reelles
    except sqlite3.DatabaseError:
        # Une base illisible ne doit pas être détruite au prétexte qu'on ne sait
        # pas la lire : on la déclare porteuse de données.
        return [{"correction_id": None, "assessment_id": None, "status": "illisible",
                 "scores": -1, "observations": -1}]
    finally:
        connexion.close()


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    force = "--force" in argv
    confirme = CONFIRMATION in argv
    config.ensure_runtime()
    exists = config.DB_PATH.exists()
    if exists and not force:
        print("la base existe déjà : %s" % config.DB_PATH)
        print("relancer avec --force pour réimporter dans une base vierge "
              "(une sauvegarde est prise avant).")
        return 1
    if exists and force:
        # Garde : à partir de la première correction réelle, la réinitialisation
        # destructrice n'est plus un geste d'exploitation courant. Les migrations
        # font évoluer le schéma sans rien perdre ; c'est la voie normale.
        reelles = real_corrections(config.DB_PATH)
        if reelles and not confirme:
            print("REFUS : la base contient %d correction(s) réelle(s)." % len(reelles),
                  file=sys.stderr)
            for r in reelles:
                print("  correction %s — %s — %s, %s score(s), %s observation(s)"
                      % (r["correction_id"], r["assessment_id"], r["status"],
                         r["scores"], r["observations"]), file=sys.stderr)
            print("", file=sys.stderr)
            print("La base n'a pas été modifiée. Pour faire évoluer le schéma, utiliser",
                  file=sys.stderr)
            print("les migrations : elles s'appliquent sans rien détruire.", file=sys.stderr)
            print("Si la perte est réellement voulue, relancer avec %s ;" % CONFIRMATION,
                  file=sys.stderr)
            print("une sauvegarde sera prise avant suppression.", file=sys.stderr)
            return 3
        if reelles:
            print("AVERTISSEMENT : %d correction(s) réelle(s) vont être perdues."
                  % len(reelles), file=sys.stderr)
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
