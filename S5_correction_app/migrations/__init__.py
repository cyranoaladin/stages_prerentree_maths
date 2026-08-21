# -*- coding: utf-8 -*-
"""Migrations explicites.

Pas de migration automatique déclenchée par un import de module : une migration se
demande, se journalise, et est précédée d'une sauvegarde de la base. La version courante
est inscrite dans ``app_meta.domain_schema_version``.
"""

import datetime as dt
import shutil
from pathlib import Path

from sqlalchemy import text

from app import APP_VERSION, DOMAIN_SCHEMA_VERSION, IMPORT_SOURCE_VERSION
from app.models import Base

CURRENT_VERSION = int(DOMAIN_SCHEMA_VERSION)

# Chaque entrée : (version cible, description, liste d'instructions SQL).
# La version 1 est créée par ``Base.metadata.create_all`` ; les suivantes s'ajoutent ici.
UPGRADES = []


def _meta_get(conn, key):
    row = conn.execute(text("SELECT value FROM app_meta WHERE key=:k"), {"k": key}).fetchone()
    return row[0] if row else None


def _meta_set(conn, key, value):
    conn.execute(text("INSERT INTO app_meta(key, value) VALUES(:k, :v) "
                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value"),
                 {"k": key, "v": str(value)})


def backup_database(db_path: Path, backups_dir: Path) -> Path:
    db_path, backups_dir = Path(db_path), Path(backups_dir)
    if not db_path.exists():
        return None
    backups_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = backups_dir / ("corrections_%s.sqlite3" % stamp)
    shutil.copy2(db_path, target)
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
                conn.execute(text(sql))
        _meta_set(conn, "domain_schema_version", CURRENT_VERSION)
        _meta_set(conn, "app_version", APP_VERSION)
        _meta_set(conn, "import_source_version", IMPORT_SOURCE_VERSION)
    return {"version_avant": before, "version_apres": CURRENT_VERSION,
            "sauvegarde": str(backup) if backup else None}
