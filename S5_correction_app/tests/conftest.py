# -*- coding: utf-8 -*-
"""Environnement de test : base jetable, jamais celle de l'enseignant.

Chaque session de test travaille dans un répertoire temporaire. Aucun test n'écrit dans
``runtime/`` du poste, et aucun n'ouvre en écriture un document distribué.
"""

import sys
from pathlib import Path

import pytest

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
# Les fichiers de test se partagent des fixtures (client simulé, fabriques de pages).
# Le répertoire est donc importable explicitement, plutôt que de dépendre de la façon
# dont pytest devine sa racine.
sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture(scope="module")
def runtime(tmp_path_factory):
    from app import config, database
    root = tmp_path_factory.mktemp("nexus_runtime")
    # Chaque module de test travaille sur sa propre base : aucun test n'hérite de l'état
    # laissé par un autre, et l'ordre d'exécution n'a pas d'influence.
    config.RUNTIME_DIR = root
    config.DB_PATH = root / "corrections.sqlite3"
    config.EXPORTS_DIR = root / "exports"
    config.REPORTS_DIR = root / "reports"
    config.BACKUPS_DIR = root / "backups"
    config.BUILD_DIR = root / "build"
    config.SOURCE_COPIES_DIR = root / "source_copies"
    config.OCR_CACHE_DIR = root / "ocr_cache"
    # Aucun test ne doit pouvoir lire un secret réel du poste, ni en écrire un.
    config.SECRETS_DIR = root / "secrets"
    config.OPENROUTER_KEY_FILE = config.SECRETS_DIR / "openrouter.key"
    # Les tests ne manipulent que des fixtures : ils déclarent le mode SYNTHETIC,
    # qui n'exige pas d'authentification. Le mode REAL, lui, l'exige toujours — et
    # un test dédié le vérifie.
    config.settings.data_mode = "SYNTHETIC"
    config.ensure_runtime()
    database.reset_engine()
    return root


@pytest.fixture(scope="module")
def client(runtime):
    import warnings
    warnings.filterwarnings("ignore")
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app, headers={"X-Requested-With": "nexus-tests"}) as test_client:
        # Comme un navigateur : une première page pose le cookie anti-CSRF, que le
        # client renvoie ensuite. Sans cette étape, toute requête mutante est refusée
        # — c'est précisément ce que le contrôle doit garantir.
        test_client.get("/")
        yield test_client


@pytest.fixture()
def session(client):
    from app import database
    with database.session_scope() as s:
        yield s


@pytest.fixture(scope="session")
def immutability_before():
    """Empreintes relevées avant toute utilisation de l'application."""
    from app.domain import immutability
    return immutability.verify()


def scoring_rows(session, student_id):
    from app.models import Assessment
    from app.domain import correction as corr
    assessment = session.query(Assessment).filter_by(student_id=student_id).one()
    correction = corr.get_or_create_correction(session, assessment)
    session.flush()
    return assessment, correction


def fill(client, student_id, overrides=None):
    """Remplit une copie de façon synthétique. Aucune donnée d'élève réel n'est inventée
    ici : ce sont des scores de test, dans une base jetable."""
    from app import database
    from app.models import Assessment
    from app.domain import correction as corr
    overrides = overrides or {}
    client.get("/eleve/%s" % student_id)
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student_id).one()
        rows = [(r.scoring_id, r.max_score_centi)
                for r in corr.current_correction(s, assessment.assessment_id).responses]
    for scoring_id, max_centi in rows:
        payload = overrides.get(scoring_id, {"score_centi": max_centi, "error_codes": []})
        response = client.post("/eleve/%s/critere/%s" % (student_id, scoring_id),
                               json=payload)
        assert response.status_code == 200, (scoring_id, response.text)
    return rows
