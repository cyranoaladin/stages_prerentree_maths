# -*- coding: utf-8 -*-
"""Migrations explicites.

Pas de migration automatique déclenchée par un import de module : une migration se
demande, se journalise, et est précédée d'une sauvegarde de la base. La version courante
est inscrite dans ``app_meta.domain_schema_version``.
"""

import datetime as dt
import sqlite3
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app import APP_VERSION, DOMAIN_SCHEMA_VERSION, IMPORT_SOURCE_VERSION
from app.models import Base

CURRENT_VERSION = int(DOMAIN_SCHEMA_VERSION)

# Chaque entrée : (version cible, description, liste d'instructions SQL).
# La version 1 est créée par ``Base.metadata.create_all`` ; les suivantes s'ajoutent ici.
#
# ``create_all`` ne modifie jamais une table existante : sur une base déjà créée en
# version 1, les colonnes ajoutées en version 2 doivent l'être explicitement. Les
# instructions sont écrites pour être rejouables sans dommage.
UPGRADES = [
    (2,
     "rubriques de score, suggestions d'erreur par critère et traçabilité curriculaire",
     [
         "ALTER TABLE criterion_definition ADD COLUMN neutral_label VARCHAR(255)",
         "ALTER TABLE criterion_definition ADD COLUMN score_rubric_json TEXT",
         "ALTER TABLE criterion_definition ADD COLUMN error_suggestions_json TEXT",
         "ALTER TABLE criterion_definition ADD COLUMN official_source VARCHAR(255)",
         "ALTER TABLE criterion_definition ADD COLUMN scope_certainty VARCHAR(16)",
         "ALTER TABLE virtual_criterion_definition ADD COLUMN neutral_label VARCHAR(255)",
         "ALTER TABLE virtual_criterion_definition ADD COLUMN score_rubric_json TEXT",
         "ALTER TABLE virtual_criterion_definition ADD COLUMN error_suggestions_json TEXT",
     ]),
    (3,
     "couche longitudinale : faits, matrice de trajectoire, plan de rentrée, provenance",
     [
         # Le profil d'apprentissage documentait déjà ces champs ; l'import les
         # laissait tomber. Ils décrivent le travail ciblé, jamais une réussite.
         "ALTER TABLE baseline_status ADD COLUMN baseline_items_json TEXT",
         "ALTER TABLE baseline_status ADD COLUMN sessions_json TEXT",
         "ALTER TABLE baseline_status ADD COLUMN targeted_in_s5 BOOLEAN",
         "ALTER TABLE baseline_status ADD COLUMN stage_evidence_note TEXT",
         "ALTER TABLE baseline_status ADD COLUMN provisional_priority VARCHAR(16)",
         "ALTER TABLE baseline_status ADD COLUMN domain VARCHAR(96)",
         "ALTER TABLE baseline_status ADD COLUMN importance_n VARCHAR(32)",
         """CREATE TABLE IF NOT EXISTS longitudinal_facts (
                id INTEGER NOT NULL PRIMARY KEY,
                assessment_id VARCHAR(64) NOT NULL REFERENCES assessment(assessment_id),
                correction_id INTEGER NOT NULL REFERENCES correction(correction_id),
                correction_revision INTEGER NOT NULL,
                facts_version INTEGER NOT NULL,
                payload_json TEXT NOT NULL,
                facts_sha256 VARCHAR(64) NOT NULL,
                analysis_sha256 VARCHAR(64),
                built_at DATETIME NOT NULL,
                CONSTRAINT uq_facts UNIQUE (correction_id, facts_version))""",
         """CREATE TABLE IF NOT EXISTS skill_trajectory (
                id INTEGER NOT NULL PRIMARY KEY,
                facts_id INTEGER NOT NULL REFERENCES longitudinal_facts(id),
                analysis_skill_id VARCHAR(64) NOT NULL,
                curriculum_scope VARCHAR(16) NOT NULL,
                label VARCHAR(255), domain VARCHAR(96), importance_n VARCHAR(32),
                initial_status VARCHAR(48), sessions_json TEXT, coverage VARCHAR(16),
                final_status VARCHAR(48), evidence_level VARCHAR(2),
                evidence_strength VARCHAR(16), qualitative_trajectory VARCHAR(48),
                retention_status VARCHAR(32), priority_rank VARCHAR(16), conclusion TEXT,
                CONSTRAINT uq_trajectory UNIQUE (facts_id, analysis_skill_id, curriculum_scope))""",
         """CREATE TABLE IF NOT EXISTS action_plan_item (
                id INTEGER NOT NULL PRIMARY KEY,
                facts_id INTEGER NOT NULL REFERENCES longitudinal_facts(id),
                week INTEGER NOT NULL, rank INTEGER NOT NULL,
                analysis_skill_id VARCHAR(64), label VARCHAR(255), objective TEXT,
                work TEXT, duration_minutes INTEGER, frequency VARCHAR(96),
                success_threshold TEXT, is_delayed_check BOOLEAN NOT NULL DEFAULT 0,
                kind VARCHAR(24) NOT NULL DEFAULT 'n_minus_1')""",
         """CREATE TABLE IF NOT EXISTS report_source (
                id INTEGER NOT NULL PRIMARY KEY,
                facts_id INTEGER NOT NULL REFERENCES longitudinal_facts(id),
                role VARCHAR(64) NOT NULL, source_type VARCHAR(64) NOT NULL,
                source_path VARCHAR(512), source_sha256 VARCHAR(64), session VARCHAR(8),
                present BOOLEAN NOT NULL DEFAULT 1, note TEXT)""",
     ]),
    (4,
     "marquage des corrections synthétiques, pour protéger la base réelle",
     [
         "ALTER TABLE correction ADD COLUMN is_synthetic BOOLEAN NOT NULL DEFAULT 0",
     ]),
    (5,
     "provenance de la copie réelle : pièce source rattachée à une évaluation",
     [
         # Aucune copie historique n'est inventée : les évaluations déjà corrigées
         # n'ont simplement aucune ligne ici, ce qui se lit « SOURCE COPY = ABSENT ».
         """CREATE TABLE IF NOT EXISTS source_copy (
                source_copy_id INTEGER NOT NULL PRIMARY KEY,
                assessment_id VARCHAR(64) NOT NULL REFERENCES assessment(assessment_id),
                source_kind VARCHAR(32) NOT NULL DEFAULT 'REAL_STUDENT_COPY',
                origin VARCHAR(16) NOT NULL DEFAULT 'ORIGINAL',
                derived_from_id INTEGER REFERENCES source_copy(source_copy_id),
                label VARCHAR(255), page_count INTEGER,
                file_count INTEGER NOT NULL DEFAULT 0,
                status VARCHAR(16) NOT NULL DEFAULT 'ATTACHED',
                is_immutable BOOLEAN NOT NULL DEFAULT 1,
                note TEXT,
                ingested_at DATETIME NOT NULL)""",
         "CREATE INDEX IF NOT EXISTS ix_source_copy_assessment "
         "ON source_copy (assessment_id)",
         """CREATE TABLE IF NOT EXISTS source_copy_file (
                id INTEGER NOT NULL PRIMARY KEY,
                source_copy_id INTEGER NOT NULL REFERENCES source_copy(source_copy_id),
                page_index INTEGER NOT NULL,
                original_name VARCHAR(255) NOT NULL,
                media_type VARCHAR(64) NOT NULL,
                byte_size INTEGER NOT NULL,
                sha256 VARCHAR(64) NOT NULL,
                stored_path VARCHAR(512) NOT NULL,
                CONSTRAINT uq_copy_page UNIQUE (source_copy_id, page_index))""",
         "CREATE INDEX IF NOT EXISTS ix_source_copy_file_sha "
         "ON source_copy_file (sha256)",
     ]),
    (6,
     "lecture assistée : pages dérivées, campagnes OCR, blocs transcrits",
     [
         # Dimensions des pages rastérisées : ce que le modèle a réellement vu.
         "ALTER TABLE source_copy_file ADD COLUMN width_px INTEGER",
         "ALTER TABLE source_copy_file ADD COLUMN height_px INTEGER",
         "ALTER TABLE source_copy_file ADD COLUMN dpi INTEGER",
         """CREATE TABLE IF NOT EXISTS ocr_run (
                run_id INTEGER NOT NULL PRIMARY KEY,
                assessment_id VARCHAR(64) NOT NULL REFERENCES assessment(assessment_id),
                source_copy_id INTEGER NOT NULL REFERENCES source_copy(source_copy_id),
                derived_copy_id INTEGER REFERENCES source_copy(source_copy_id),
                role VARCHAR(16) NOT NULL,
                model_id VARCHAR(128) NOT NULL,
                provider_name VARCHAR(96),
                prompt_version VARCHAR(64) NOT NULL,
                schema_version VARCHAR(64) NOT NULL,
                params_json TEXT,
                status VARCHAR(16) NOT NULL DEFAULT 'RUNNING',
                pages_total INTEGER NOT NULL DEFAULT 0,
                calls INTEGER NOT NULL DEFAULT 0,
                cached_calls INTEGER NOT NULL DEFAULT 0,
                tokens_in INTEGER NOT NULL DEFAULT 0,
                tokens_out INTEGER NOT NULL DEFAULT 0,
                cost_usd VARCHAR(32),
                error TEXT,
                started_at DATETIME NOT NULL,
                finished_at DATETIME)""",
         """CREATE TABLE IF NOT EXISTS ocr_page (
                id INTEGER NOT NULL PRIMARY KEY,
                run_id INTEGER NOT NULL REFERENCES ocr_run(run_id),
                page_index INTEGER NOT NULL,
                page_sha256 VARCHAR(64) NOT NULL,
                status VARCHAR(16) NOT NULL DEFAULT 'OK',
                request_id VARCHAR(128), generation_id VARCHAR(128),
                raw_json TEXT, latency_ms INTEGER,
                tokens_in INTEGER, tokens_out INTEGER, cost_usd VARCHAR(32),
                error TEXT, created_at DATETIME NOT NULL,
                CONSTRAINT uq_ocr_page UNIQUE (run_id, page_index))""",
         """CREATE TABLE IF NOT EXISTS transcription_block (
                id INTEGER NOT NULL PRIMARY KEY,
                assessment_id VARCHAR(64) NOT NULL REFERENCES assessment(assessment_id),
                source_copy_id INTEGER NOT NULL REFERENCES source_copy(source_copy_id),
                page_index INTEGER NOT NULL,
                block_id VARCHAR(64) NOT NULL,
                item_ref VARCHAR(16),
                origin VARCHAR(24) NOT NULL,
                kind VARCHAR(8) NOT NULL,
                status VARCHAR(16) NOT NULL,
                verbatim TEXT NOT NULL,
                latex TEXT,
                uncertainty VARCHAR(8) NOT NULL DEFAULT 'LOW',
                alternatives_json TEXT, notes TEXT, bbox_json TEXT,
                primary_run_id INTEGER REFERENCES ocr_run(run_id),
                verify_run_id INTEGER REFERENCES ocr_run(run_id),
                verify_verdict VARCHAR(16), verify_verbatim TEXT, verify_latex TEXT,
                verify_note TEXT,
                reconciliation VARCHAR(24),
                review_state VARCHAR(24) NOT NULL DEFAULT 'AI_PROPOSED',
                human_verbatim TEXT, human_latex TEXT, human_note TEXT,
                reviewed_at DATETIME, reviewed_by_role VARCHAR(32),
                created_at DATETIME NOT NULL,
                CONSTRAINT uq_block UNIQUE (source_copy_id, page_index, block_id))""",
         "CREATE INDEX IF NOT EXISTS ix_block_assessment "
         "ON transcription_block (assessment_id)",
         """CREATE TABLE IF NOT EXISTS transcription_state (
                id INTEGER NOT NULL PRIMARY KEY,
                assessment_id VARCHAR(64) NOT NULL REFERENCES assessment(assessment_id),
                source_copy_id INTEGER NOT NULL REFERENCES source_copy(source_copy_id),
                state VARCHAR(24) NOT NULL DEFAULT 'NOT_STARTED',
                detail TEXT,
                updated_at DATETIME NOT NULL,
                CONSTRAINT uq_transcription_state UNIQUE (source_copy_id))""",
     ]),
    (7,
     "durcissement : double lecture aveugle, attestation de complétude, "
     "historique append-only, campagnes figées",
     [
         # Empreintes techniques et configuration figée d'une campagne.
         # Une pièce synthétique n'est pas une copie d'élève : elle ne déclenche
         # pas le garde-fou d'envoi distant.
         "ALTER TABLE source_copy ADD COLUMN is_synthetic BOOLEAN NOT NULL DEFAULT 0",
         "ALTER TABLE ocr_run ADD COLUMN prompt_sha256 VARCHAR(64)",
         "ALTER TABLE ocr_run ADD COLUMN schema_sha256 VARCHAR(64)",
         "ALTER TABLE ocr_run ADD COLUMN frozen_config_json TEXT",
         "ALTER TABLE ocr_run ADD COLUMN verify_mode VARCHAR(16)",
         # Une seconde lecture aveugle est une lecture à part entière.
         "ALTER TABLE transcription_block ADD COLUMN reading VARCHAR(16) "
         "NOT NULL DEFAULT 'PRIMARY'",
         "ALTER TABLE transcription_block ADD COLUMN verify_mode VARCHAR(16)",
         "ALTER TABLE transcription_block ADD COLUMN verify_block_id VARCHAR(64)",
         "ALTER TABLE transcription_block ADD COLUMN reviewed_by_identity VARCHAR(96)",
         "ALTER TABLE transcription_block ADD COLUMN human_item_ref VARCHAR(16)",
         "ALTER TABLE transcription_block ADD COLUMN continues_from VARCHAR(96)",
         "ALTER TABLE transcription_block ADD COLUMN continues_to VARCHAR(96)",
         """CREATE TABLE IF NOT EXISTS transcription_block_history (
                id INTEGER NOT NULL PRIMARY KEY,
                block_pk INTEGER NOT NULL REFERENCES transcription_block(id),
                action VARCHAR(24) NOT NULL,
                before_verbatim TEXT, after_verbatim TEXT,
                before_latex TEXT, after_latex TEXT,
                before_item_ref VARCHAR(16), after_item_ref VARCHAR(16),
                before_state VARCHAR(24), after_state VARCHAR(24),
                reason TEXT,
                actor_identity VARCHAR(96), actor_role VARCHAR(32),
                created_at DATETIME NOT NULL)""",
         "CREATE INDEX IF NOT EXISTS ix_block_history "
         "ON transcription_block_history (block_pk)",
         """CREATE TABLE IF NOT EXISTS page_attestation (
                id INTEGER NOT NULL PRIMARY KEY,
                source_copy_id INTEGER NOT NULL REFERENCES source_copy(source_copy_id),
                page_index INTEGER NOT NULL,
                page_sha256 VARCHAR(64) NOT NULL,
                attested BOOLEAN NOT NULL DEFAULT 0,
                note TEXT,
                actor_identity VARCHAR(96), actor_role VARCHAR(32),
                attested_at DATETIME,
                CONSTRAINT uq_page_attestation UNIQUE (source_copy_id, page_index))""",
         # Deux campagnes simultanées du même rôle sur la même copie : impossible.
         # L'index partiel rend la contrainte inviolable, y compris sur double clic.
         "CREATE UNIQUE INDEX IF NOT EXISTS uq_ocr_run_en_cours "
         "ON ocr_run (source_copy_id, role) WHERE status = 'RUNNING'",
         # L'unicité d'un bloc inclut désormais la lecture dont il provient.
         "DROP INDEX IF EXISTS uq_block",
         "CREATE UNIQUE INDEX IF NOT EXISTS uq_block "
         "ON transcription_block (source_copy_id, page_index, block_id, reading)",
     ]),
    (8,
     "rotation réelle des pages, preuves non textuelles, code, continuation révisable",
     [
         # Rotation appliquée aux pixels, pas seulement à l'affichage.
         "ALTER TABLE source_copy_file ADD COLUMN rotation INTEGER NOT NULL DEFAULT 0",
         # Programme d'élève : la mise en forme EST la donnée.
         "ALTER TABLE transcription_block ADD COLUMN verbatim_code TEXT",
         "ALTER TABLE transcription_block ADD COLUMN language_hint VARCHAR(32)",
         # Preuve non textuelle : une figure peut être toute la réponse.
         "ALTER TABLE transcription_block ADD COLUMN ai_description TEXT",
         "ALTER TABLE transcription_block ADD COLUMN human_description TEXT",
         # Continuation entre pages, révisable par un humain.
         "ALTER TABLE transcription_block ADD COLUMN human_continues_from VARCHAR(96)",
         "ALTER TABLE transcription_block ADD COLUMN human_continues_to VARCHAR(96)",
         # « kind » passe de 8 à 32 caractères : OTHER_NON_TEXT n'y tenait pas.
         # SQLite ne contraint pas la longueur d'un VARCHAR ; la colonne existante
         # accepte donc déjà les nouvelles valeurs, et aucune réécriture de table
         # n'est nécessaire. La déclaration ORM est mise à jour pour rester exacte.
     ]),
]


def _meta_get(conn, key):
    row = conn.execute(text("SELECT value FROM app_meta WHERE key=:k"), {"k": key}).fetchone()
    return row[0] if row else None


def _meta_set(conn, key, value):
    conn.execute(text("INSERT INTO app_meta(key, value) VALUES(:k, :v) "
                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value"),
                 {"k": key, "v": str(value)})


def backup_database(db_path: Path, backups_dir: Path) -> Path:
    """Instantané cohérent de la base, avant migration.

    Une copie de fichier ne convient pas : la base est en mode WAL, et les
    transactions récentes vivent dans le journal ``-wal``. Copier le seul fichier
    principal produit une sauvegarde **incomplète**, parfois vide de ses dernières
    tables — vérifié expérimentalement. On emploie l'API de sauvegarde en ligne de
    SQLite, qui rend une base complète et cohérente.
    """
    db_path, backups_dir = Path(db_path), Path(backups_dir)
    if not db_path.exists():
        return None
    backups_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = backups_dir / ("corrections_%s.sqlite3" % stamp)
    source = sqlite3.connect(str(db_path))
    destination = sqlite3.connect(str(target))
    try:
        source.backup(destination)
    finally:
        destination.close()
        source.close()
    try:
        target.chmod(0o600)
    except OSError:
        pass
    return target


def current_version(engine) -> int:
    with engine.connect() as conn:
        try:
            value = _meta_get(conn, "domain_schema_version")
        except Exception:
            return 0
    return int(value) if value else 0


def apply(engine, db_path: Path = None, backups_dir: Path = None) -> dict:
    """Crée ou met à niveau le schéma. Sauvegarde d'abord si une base existe déjà."""
    before = current_version(engine)
    backup = None
    if before and before < CURRENT_VERSION and db_path:
        backup = backup_database(db_path, backups_dir)
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        for version, description, statements in UPGRADES:
            if version <= before:
                continue
            for sql in statements:
                try:
                    conn.execute(text(sql))
                except OperationalError as exc:
                    # « duplicate column name » : la colonne existe déjà parce que
                    # create_all vient de créer la table dans sa forme courante. Toute
                    # autre erreur reste fatale.
                    if "duplicate column name" not in str(exc).lower():
                        raise
        _meta_set(conn, "domain_schema_version", CURRENT_VERSION)
        _meta_set(conn, "app_version", APP_VERSION)
        _meta_set(conn, "import_source_version", IMPORT_SOURCE_VERSION)
    return {"version_avant": before, "version_apres": CURRENT_VERSION,
            "sauvegarde": str(backup) if backup else None}
