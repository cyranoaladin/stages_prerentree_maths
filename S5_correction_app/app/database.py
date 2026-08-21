# -*- coding: utf-8 -*-
"""Accès SQLite : moteur, session, création et migration explicite.

Aucune requête n'est construite par concaténation de chaînes : tout passe par l'ORM ou
par des paramètres liés.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker

from . import config

_engine = None
_SessionLocal = None


def engine():
    global _engine, _SessionLocal
    if _engine is None:
        config.ensure_runtime()
        url = "sqlite:///%s" % config.DB_PATH
        _engine = create_engine(url, future=True, echo=False,
                                connect_args={"check_same_thread": False})

        @event.listens_for(_engine, "connect")
        def _pragmas(dbapi_connection, connection_record):
            cur = dbapi_connection.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            cur.execute("PRAGMA journal_mode=WAL")
            cur.execute("PRAGMA synchronous=FULL")
            cur.close()

        _SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False, future=True)
    return _engine


def reset_engine():
    """Utilisé par les tests, qui pointent la base ailleurs entre deux cas."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None


def session_factory():
    engine()
    return _SessionLocal


@contextmanager
def session_scope():
    """Session transactionnelle : un commit, ou un rollback complet."""
    s = session_factory()()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def get_session():
    """Dépendance FastAPI."""
    s = session_factory()()
    try:
        yield s
    finally:
        s.close()


def schema_version(conn) -> int:
    row = conn.execute(text("SELECT value FROM app_meta WHERE key='domain_schema_version'")
                       ).fetchone()
    return int(row[0]) if row else 0
