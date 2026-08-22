#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Réconciliation entre la base et le système de fichiers.

SQLite et les fichiers stockés ne forment pas une transaction unique : une base peut
référencer un fichier absent, un fichier peut traîner sans ligne, une empreinte peut
avoir changé. Rien de tout cela ne se voit à l'usage — jusqu'au jour où l'on a besoin
de la pièce.

    make s5-correction-fsck            # diagnostic, lecture seule
    make s5-correction-fsck-json       # même chose, format machine

**Mode par défaut : lecture seule.** Aucune réparation n'est automatique. Une pièce
probante correctement rattachée n'est jamais supprimée par cet outil, quelle que soit
l'option employée.
"""

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config, database                              # noqa: E402
from app.domain import source_copy as sc                      # noqa: E402
from app.models import (OcrRun, PageAttestation, SourceCopy,  # noqa: E402
                        SourceCopyFile, TranscriptionBlock)
from app.security import sha256_file                          # noqa: E402

# Un staging n'existe pas dans cette architecture — l'ingestion est atomique et le
# temporaire est détruit à la sortie du bloc. On vérifie tout de même qu'il n'en
# subsiste aucun : une hypothèse non vérifiée n'est pas une garantie.
AGE_MINIMUM_ORPHELIN_SECONDES = 3600


class Constat:
    def __init__(self):
        self.problemes = []

    def signaler(self, code, gravite, message, detail=None):
        self.problemes.append({"code": code, "gravite": gravite, "message": message,
                               "detail": detail})

    def par_gravite(self, niveau):
        return [p for p in self.problemes if p["gravite"] == niveau]


def controler(session, verifier_empreintes=True) -> Constat:
    constat = Constat()
    racine = Path(config.SOURCE_COPIES_DIR)

    # ---- base → fichier
    connus = set()
    for row in session.query(SourceCopyFile).all():
        chemin = sc.stored_path(row)
        connus.add(chemin.resolve()) if chemin.exists() else None
        if not chemin.exists():
            constat.signaler("fichier_absent", "P0",
                             "la base référence un fichier absent : %s"
                             % row.stored_path,
                             {"source_copy_id": row.source_copy_id,
                              "page_index": row.page_index})
            continue
        mode = chemin.stat().st_mode & 0o777
        if mode & 0o077:
            constat.signaler("droits_trop_ouverts", "P1",
                             "%s est lisible au-delà de son propriétaire (mode %o)"
                             % (row.stored_path, mode))
        if mode & 0o200:
            constat.signaler("piece_inscriptible", "P1",
                             "%s reste inscriptible : une pièce stockée doit être "
                             "en lecture seule" % row.stored_path)
        if verifier_empreintes and sha256_file(chemin) != row.sha256:
            constat.signaler("empreinte_divergente", "P0",
                             "l'empreinte de %s ne correspond plus à la base"
                             % row.stored_path)

    # ---- fichier → base
    if racine.exists():
        maintenant = time.time()
        for chemin in racine.rglob("*"):
            if not chemin.is_file():
                continue
            if chemin.resolve() in connus:
                continue
            age = maintenant - chemin.stat().st_mtime
            gravite = "P2" if age > AGE_MINIMUM_ORPHELIN_SECONDES else "P3"
            constat.signaler("fichier_orphelin", gravite,
                             "fichier sans ligne en base : %s"
                             % chemin.relative_to(racine),
                             {"age_secondes": int(age)})

    # ---- cohérence des pièces
    for copy in session.query(SourceCopy).all():
        fichiers = sc.files_of(session, copy)
        if copy.file_count != len(fichiers):
            constat.signaler("compte_fichiers", "P1",
                             "pièce n° %d : %d fichier(s) annoncés, %d en base"
                             % (copy.source_copy_id, copy.file_count, len(fichiers)))
        rangs = [f.page_index for f in fichiers]
        if len(set(rangs)) != len(rangs):
            constat.signaler("page_index_duplique", "P0",
                             "pièce n° %d : rangs de page dupliqués"
                             % copy.source_copy_id, {"rangs": rangs})
        if copy.origin == "DERIVED" and copy.derived_from_id is None:
            constat.signaler("derive_sans_original", "P0",
                             "pièce n° %d dérivée sans original"
                             % copy.source_copy_id)
        if copy.derived_from_id is not None:
            parent = session.get(SourceCopy, copy.derived_from_id)
            if parent is None:
                constat.signaler("original_introuvable", "P0",
                                 "pièce n° %d référence un original absent"
                                 % copy.source_copy_id)

    # ---- une seule pièce courante par évaluation
    for assessment_id in {c.assessment_id for c in session.query(SourceCopy).all()}:
        courantes = (session.query(SourceCopy)
                     .filter_by(assessment_id=assessment_id,
                                source_kind=sc.REAL_STUDENT_COPY,
                                status=sc.STATUS_ATTACHED).all())
        if len(courantes) > 1:
            constat.signaler("plusieurs_pieces_courantes", "P0",
                             "%s a %d pièces marquées courantes"
                             % (assessment_id, len(courantes)),
                             {"ids": [c.source_copy_id for c in courantes]})

    # ---- campagnes
    for run in session.query(OcrRun).all():
        copy = session.get(SourceCopy, run.source_copy_id)
        if copy is None:
            constat.signaler("campagne_orpheline", "P0",
                             "campagne n° %d sur une pièce absente" % run.run_id)
            continue
        if copy.status == sc.STATUS_SUPERSEDED:
            constat.signaler("campagne_sur_piece_remplacee", "P2",
                             "campagne n° %d porte sur une pièce remplacée : elle "
                             "reste vraie de cette pièce, mais ne peut plus servir "
                             "la correction courante" % run.run_id)
        if run.status == "RUNNING":
            constat.signaler("campagne_bloquee", "P1",
                             "campagne n° %d encore marquée en cours : si aucun "
                             "processus ne tourne, elle doit passer INTERRUPTED"
                             % run.run_id)

    # ---- blocs et attestations
    for bloc in session.query(TranscriptionBlock).all():
        if session.get(SourceCopy, bloc.source_copy_id) is None:
            constat.signaler("bloc_orphelin", "P0",
                             "bloc n° %d rattaché à une pièce absente" % bloc.id)
    for attestation in session.query(PageAttestation).all():
        copy = session.get(SourceCopy, attestation.source_copy_id)
        if copy is None:
            constat.signaler("attestation_orpheline", "P0",
                             "attestation n° %d sur une pièce absente"
                             % attestation.id)
            continue
        derived = sc.derived_pages(session, copy)
        page = next((r for r in sc.files_of(session, derived)
                     if r.page_index == attestation.page_index), None) \
            if derived else None
        if page is not None and attestation.attested \
                and page.sha256 != attestation.page_sha256:
            constat.signaler("attestation_perimee", "P1",
                             "l'attestation de la page %d ne porte plus sur les "
                             "octets rendus" % attestation.page_index)

    # ---- cache orphelin
    cache = Path(config.OCR_CACHE_DIR)
    if cache.exists():
        for fichier in cache.glob("*.json"):
            mode = fichier.stat().st_mode & 0o777
            if mode & 0o077:
                constat.signaler("cache_trop_ouvert", "P1",
                                 "le cache %s est lisible au-delà de son "
                                 "propriétaire (mode %o)" % (fichier.name, mode))

    # ---- répertoires sensibles
    for repertoire in (config.SOURCE_COPIES_DIR, config.OCR_CACHE_DIR,
                       config.SECRETS_DIR, config.BACKUPS_DIR):
        chemin = Path(repertoire)
        if not chemin.exists():
            continue
        mode = chemin.stat().st_mode & 0o777
        if mode & 0o077:
            constat.signaler("repertoire_trop_ouvert", "P1",
                             "%s est accessible au-delà de son propriétaire "
                             "(mode %o)" % (chemin.name, mode))

    # ---- staging résiduel : l'ingestion est atomique, rien ne doit subsister
    import tempfile
    for motif in ("nexus_upload_*", "nexus_raster_*", "nexus_measure_*"):
        for reste in Path(tempfile.gettempdir()).glob(motif):
            constat.signaler("temporaire_residuel", "P1",
                             "temporaire d'ingestion resté en clair : %s" % reste)
    return constat


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rapide", action="store_true",
                        help="ne recalcule pas les empreintes")
    args = parser.parse_args(argv)

    config.ensure_runtime()
    import migrations
    migrations.apply(database.engine(), config.DB_PATH, config.BACKUPS_DIR)

    with database.session_scope() as session:
        constat = controler(session, verifier_empreintes=not args.rapide)

    par_gravite = {niveau: constat.par_gravite(niveau)
                   for niveau in ("P0", "P1", "P2", "P3")}
    bloquant = bool(par_gravite["P0"] or par_gravite["P1"])

    if args.json:
        print(json.dumps({"problemes": constat.problemes,
                          "par_gravite": {k: len(v) for k, v in par_gravite.items()},
                          "verdict": "FSCK FAILURE" if bloquant else "FSCK PASS"},
                         ensure_ascii=False, indent=2))
        return 1 if bloquant else 0

    if not constat.problemes:
        print("aucune incohérence entre la base et les fichiers.")
    for niveau in ("P0", "P1", "P2", "P3"):
        for probleme in par_gravite[niveau]:
            print("%s  %-28s %s" % (niveau, probleme["code"], probleme["message"]))
    print()
    print("FSCK = %s" % ("FAILURE" if bloquant else "PASS"))
    print("Mode lecture seule : aucune réparation n'a été tentée, et une pièce "
          "correctement\nrattachée n'est jamais supprimée par cet outil.")
    return 1 if bloquant else 0


if __name__ == "__main__":
    sys.exit(main())
