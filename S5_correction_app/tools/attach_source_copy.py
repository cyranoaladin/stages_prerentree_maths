#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rattache une copie réelle d'élève à son évaluation.

Une pièce probante entre dans le système par une décision explicite, pas par un
formulaire de téléversement : on nomme l'élève, on nomme les fichiers, et on lit ce
que l'outil répond avant de corriger quoi que ce soit.

    python3 tools/attach_source_copy.py ines-kefi copie_ines.pdf
    python3 tools/attach_source_copy.py ines-kefi p1.jpg p2.jpg p3.jpg --libelle "4 photos"

Les fichiers d'origine ne sont ni déplacés, ni modifiés, ni recompressés : ils sont
recopiés dans ``runtime/source_copies/`` et passés en lecture seule. L'empreinte est
recalculée après recopie et comparée à celle de l'original.

    --lister            affiche la copie rattachée et vérifie ses empreintes
    --autoriser-partage accepte un fichier déjà rattaché à une autre évaluation
    --remplacer         l'ancienne pièce devient SUPERSEDED ; elle n'est pas effacée
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                            # noqa: E402
from app.domain import source_copy as sc                    # noqa: E402
from app.models import Assessment                           # noqa: E402


def _assessment(session, student_id):
    assessment = (session.query(Assessment)
                  .filter(Assessment.student_id == student_id).one_or_none())
    if assessment is None:
        raise SystemExit("aucun élève ne porte l'identifiant « %s »." % student_id)
    return assessment


def _show(session, assessment) -> int:
    described = sc.describe(session, assessment)
    print(json.dumps(described, ensure_ascii=False, indent=2, default=str))
    if not described["attached"]:
        return 1
    return 0 if described["verification"]["ok"] else 2


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("student_id")
    parser.add_argument("fichiers", nargs="*",
                        help="un PDF multipage, ou les images dans l'ordre des pages")
    parser.add_argument("--libelle", default=None)
    parser.add_argument("--note", default=None)
    parser.add_argument("--lister", action="store_true")
    parser.add_argument("--autoriser-partage", dest="allow_shared", action="store_true")
    parser.add_argument("--remplacer", dest="replace", action="store_true")
    parser.add_argument("--autoriser-doublons", dest="allow_duplicates",
                        action="store_true",
                        help="accepte deux pages d'empreinte identique")
    args = parser.parse_args(argv)

    config.ensure_runtime()
    import migrations
    migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)

    with database.session_scope() as session:
        assessment = _assessment(session, args.student_id)
        if args.lister or not args.fichiers:
            return _show(session, assessment)
        try:
            copy = sc.attach(session, assessment, args.fichiers, label=args.libelle,
                             note=args.note, allow_shared=args.allow_shared,
                             replace=args.replace,
                             allow_duplicates=args.allow_duplicates)
        except sc.SourceCopyError as exc:
            print("rattachement refusé : %s" % exc, file=sys.stderr)
            return 1
        session.commit()
        print("copie rattachée à %s — pièce n° %d, %d fichier(s), %s page(s)"
              % (assessment.assessment_id, copy.source_copy_id, copy.file_count,
                 copy.page_count if copy.page_count is not None else "?"))
        for row in sc.files_of(session, copy):
            print("  page %d  %s  %s  %d octets  sha256 %s"
                  % (row.page_index, row.original_name, row.media_type,
                     row.byte_size, row.sha256))
        return 0


if __name__ == "__main__":
    sys.exit(main())
