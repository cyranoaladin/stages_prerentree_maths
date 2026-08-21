# -*- coding: utf-8 -*-
"""Application web : pages, codes de retour, échappement, accessibilité minimale."""

import pytest

from conftest import fill


def test_le_tableau_de_bord_repond(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Tableau de bord S5" in response.text
    assert "15" in response.text


def test_un_eleve_valide_repond_et_un_inconnu_donne_404(client):
    assert client.get("/eleve/elyes-kefi").status_code == 200
    absent = client.get("/eleve/personne-inexistante")
    assert absent.status_code == 404
    assert "personne-inexistante" in absent.text


def test_l_ecran_de_correction_affiche_le_pdf_distribue(client):
    page = client.get("/eleve/elyes-kefi").text
    assert "/document/elyes-kefi/evaluation" in page
    assert "document immuable" in page


def test_les_badges_de_portee_ne_reposent_pas_que_sur_la_couleur(client):
    page = client.get("/eleve/ines-kefi").text
    assert "N-1" in page
    assert "PASSERELLE N" in page
    assert "ne doit pas dégrader le diagnostic" in page


def test_le_pdf_distribue_est_servi(client):
    response = client.get("/document/ines-kefi/evaluation")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content[:4] == b"%PDF"


@pytest.mark.parametrize("chemin", [
    "/document/ines-kefi/../../etc/passwd",
    "/document/ines-kefi/%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "/document/../../../etc/passwd/evaluation",
    "/document/ines-kefi/..%5c..%5cwindows",
])
def test_les_traversees_de_chemin_sont_refusees(client, chemin):
    assert client.get(chemin).status_code in (404, 405)


def test_le_texte_saisi_n_est_jamais_injecte_en_html(client):
    student = "amine-mansouri"
    client.get("/eleve/%s" % student)
    from app import database
    from app.models import Assessment
    from app.domain import correction as corr
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        scoring_id = corr.current_correction(s, assessment.assessment_id).responses[0].scoring_id
    payload = {"score_centi": 0, "error_codes": ["CALCUL"],
               "observation": "<script>alert('xss')</script> & \"guillemets\""}
    assert client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                       json=payload).status_code == 200
    page = client.get("/eleve/%s" % student).text
    assert "<script>alert('xss')</script>" not in page
    assert "&lt;script&gt;" in page


def test_l_analyse_exige_une_correction_validee(client):
    student = "ahmed-bakir"
    client.get("/eleve/%s" % student)
    assert client.get("/eleve/%s/analyse" % student).status_code == 409


def test_le_parcours_complet_repond(client):
    student = "ahmed-bakir"
    fill(client, student)
    assert client.post("/eleve/%s/valider" % student,
                       follow_redirects=False).status_code == 303
    assert client.get("/eleve/%s/analyse" % student).status_code == 200
    assert client.get("/eleve/%s/analyse.json" % student).status_code == 200
    assert client.get("/eleve/%s/bilan" % student).status_code == 200


def test_les_pages_de_service_repondent(client):
    for url in ("/groupe", "/historique", "/admin", "/admin/integrite"):
        assert client.get(url).status_code == 200


def test_l_historique_conserve_les_evenements(client):
    page = client.get("/historique").text
    assert "correction.created" in page
    assert "correction.status" in page


def test_aucune_ressource_distante_n_est_referencee(client):
    from pathlib import Path
    from app import config
    pages = [client.get(u).text for u in ("/", "/eleve/ines-kefi", "/groupe", "/admin")]
    assets = [(config.STATIC_DIR / name).read_text(encoding="utf-8")
              for name in ("app.css", "app.js")]
    for content in pages + assets:
        for interdit in ("http://", "https://", "cdn.", "googleapis", "unpkg", "jsdelivr"):
            assert interdit not in content, interdit
