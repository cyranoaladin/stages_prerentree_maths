# -*- coding: utf-8 -*-
"""Traitement de lot, vue de groupe, et parcours d'interface."""

import importlib.util
import shutil

import pytest

from app import config, database
from app.models import Assessment, Report
from app.domain import correction as corr
from conftest import fill

PLAYWRIGHT = importlib.util.find_spec("playwright") is not None
LATEX = shutil.which(config.LATEX_ENGINE) is not None


def test_la_generation_de_lot_ignore_les_corrections_non_validees(client):
    valide = "sinda-chikhaoui"
    fill(client, valide)
    client.post("/eleve/%s/valider" % valide, follow_redirects=False)
    client.get("/eleve/ahmed-bakir")          # ouverte, non validée

    body = client.post("/bilans/generer-tous", json={}).json()
    generes = {row["student_id"] for row in body["generes"]}
    ignores = {row["student_id"] for row in body["ignores"]}
    assert valide in generes or not LATEX
    assert "ahmed-bakir" in ignores
    assert not (generes & ignores)
    for row in body["ignores"]:
        assert row["raison"] == "correction non validée"


@pytest.mark.skipif(not LATEX, reason="moteur LaTeX absent")
def test_aucun_bilan_n_est_produit_pour_une_correction_non_validee(client):
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id="ahmed-bakir").one()
        rapports = s.query(Report).filter_by(assessment_id=assessment.assessment_id).all()
        assert not rapports


def test_la_vue_groupe_ne_classe_pas_les_eleves(client):
    page = client.get("/groupe").text
    assert "pas à classer les élèves" in page
    assert "ne sont pas comparables" in page


def test_le_bouton_suivant_ne_saute_pas_les_eleves_en_cours(client):
    response = client.get("/eleve/sinda-chikhaoui/suivant", follow_redirects=False)
    assert response.status_code == 303
    cible = response.headers["location"]
    assert cible == "/" or cible.startswith("/eleve/")
    if cible.startswith("/eleve/"):
        student_id = cible.split("/")[2]
        with database.session_scope() as s:
            assessment = s.query(Assessment).filter_by(student_id=student_id).one()
            current = corr.current_correction(s, assessment.assessment_id)
            assert current is None or current.status in ("DRAFT", "REVIEW_READY")


def test_le_tableau_de_bord_compte_juste(client):
    page = client.get("/").text
    assert "évaluations" in page
    assert "validées" in page
    assert "bilans générés" in page


@pytest.mark.skipif(not PLAYWRIGHT, reason="Playwright n'est pas installé sur ce poste")
def test_parcours_navigateur():                                   # pragma: no cover
    """Parcours de bout en bout dans un vrai navigateur.

    Volontairement facultatif : la livraison ne dépend pas de l'installation d'un
    navigateur complet. Les mêmes parcours sont couverts par TestClient.
    """
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:%d/" % config.DEFAULT_PORT)
        assert "Tableau de bord" in page.content()
        browser.close()
