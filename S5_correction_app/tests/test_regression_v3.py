# -*- coding: utf-8 -*-
"""Non-régression : l'application et l'analyseur V3 doivent dire la même chose.

L'analyseur ``S5_post_distribution_v3/tools/analyze_s5_post_distribution.py`` est la
référence de comportement. Sur une même saisie, le score brut, la consolidation N−1, la
disponibilité sur les passerelles et le profil d'erreurs doivent coïncider.
"""

import sys
from pathlib import Path

import pytest

from app import config, database
from app.models import Assessment
from app.domain import analysis as ana
from app.domain import correction as corr
from conftest import fill

V3_TOOLS = Path(config.V3_ROOT) / "tools"
V3_AVAILABLE = (V3_TOOLS / "analyze_s5_post_distribution.py").exists()
STUDENT = "elyes-kefi"


def _v3_analyse(student_id, overrides):
    sys.path.insert(0, str(V3_TOOLS))
    sys.path.insert(0, str(Path(config.V3_ROOT) / "tests"))
    import importlib
    make_fixture = importlib.import_module("make_fixture")
    analyzer = importlib.import_module("analyze_s5_post_distribution")
    doc = make_fixture.fill(student_id, overrides)
    return analyzer.analyse(student_id, doc)


@pytest.mark.skipif(not V3_AVAILABLE, reason="couche V3 absente")
def test_les_deux_moteurs_saccordent_sur_les_chiffres(client):
    """Un critère raté, avec un code d'erreur : les deux moteurs doivent concorder."""
    cible = "3E_ELYES_KEFI_B4_c2"
    fill(client, STUDENT, {cible: {"score_centi": 0, "error_codes": ["METHODE"]}})
    client.post("/eleve/%s/valider" % STUDENT, follow_redirects=False)
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        app_payload = ana.analyse(s, correction, assessment)

    v3 = _v3_analyse(STUDENT, {cible: (0.0, ["METHODE"])})

    assert app_payload["raw_assessment_score"]["earned_centi"] / 100.0 == \
        v3["raw_assessment_score"]["score"]
    assert app_payload["n_minus_1_consolidation"]["earned_centi"] / 100.0 == \
        v3["n_minus_1_consolidation"]["earned"]
    assert app_payload["n_minus_1_consolidation"]["available_centi"] / 100.0 == \
        v3["n_minus_1_consolidation"]["available"]
    assert app_payload["bridge_n_readiness"]["earned_centi"] / 100.0 == \
        v3["bridge_n_readiness"]["earned"]
    assert app_payload["bridge_n_readiness"]["available_centi"] / 100.0 == \
        v3["bridge_n_readiness"]["available"]
    assert app_payload["error_profile"]["n_minus_1"] == v3["error_profile"]["n_minus_1"]
    assert app_payload["error_profile"]["bridge_n"] == v3["error_profile"]["bridge_n"]


@pytest.mark.skipif(not V3_AVAILABLE, reason="couche V3 absente")
def test_les_deux_moteurs_couvrent_les_memes_criteres(client):
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        app_payload = ana.analyse(s, correction, assessment)
    v3 = _v3_analyse(STUDENT, {})
    assert {c["scoring_id"] for c in app_payload["criteria"]} == \
        {c["scoring_id"] for c in v3["criteria"]}


@pytest.mark.skipif(not V3_AVAILABLE, reason="couche V3 absente")
def test_les_deux_moteurs_refusent_toute_progression_chiffree(client):
    v3 = _v3_analyse(STUDENT, {})
    assert v3["baseline_measure_available"] is False
    assert all(s["mastery_delta"] is None for s in v3["skills"])
    assert ana.BASELINE_MEASURE_AVAILABLE is False
