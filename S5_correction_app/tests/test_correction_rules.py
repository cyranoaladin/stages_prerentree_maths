# -*- coding: utf-8 -*-
"""Règles de correction : invariants, statuts, révisions."""

import json


from app import database
from app.models import Assessment
from app.domain import correction as corr
from app.domain import validation
from conftest import fill


def _rows(student_id):
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student_id).one()
        correction = corr.get_or_create_correction(s, assessment)
        s.flush()
        return [(r.scoring_id, r.max_score_centi) for r in correction.responses]


def test_un_critere_pleinement_reussi_ne_porte_pas_de_code_erreur(client):
    student = "amine-mansouri"
    client.get("/eleve/%s" % student)
    scoring_id, max_centi = _rows(student)[0]
    refus = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                        json={"score_centi": max_centi, "error_codes": ["CALCUL"]})
    assert refus.status_code == 400
    assert "intégralement réussi" in refus.json()["detail"]
    ok = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                     json={"score_centi": max_centi, "error_codes": []})
    assert ok.status_code == 200


def test_une_observation_reste_possible_sur_un_critere_reussi(client):
    student = "amine-mansouri"
    scoring_id, max_centi = _rows(student)[0]
    response = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                           json={"score_centi": max_centi, "error_codes": [],
                                 "observation": "réponse correcte, rédaction peu lisible"})
    assert response.status_code == 200


def test_un_zero_n_oblige_a_aucune_cause(client):
    """On ne fabrique pas une cause qu'on n'a pas observée."""
    student = "amine-mansouri"
    scoring_id, _ = _rows(student)[1]
    for status in ("NOT_ANSWERED", "UNCLASSIFIED"):
        response = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                               json={"scoring_status": status})
        assert response.status_code == 200
        body = response.json()
        assert body["scoring_status"] == status
        assert body["score_centi"] == 0
        assert body["error_codes"] == []


def test_un_score_hors_bareme_est_refuse(client):
    student = "amine-mansouri"
    scoring_id, max_centi = _rows(student)[0]
    response = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                           json={"score_centi": max_centi + 100})
    assert response.status_code == 400
    assert "hors barème" in response.json()["detail"]


def test_un_code_d_erreur_inconnu_est_refuse(client):
    student = "amine-mansouri"
    scoring_id, _ = _rows(student)[0]
    response = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                           json={"score_centi": 0, "error_codes": ["INVENTE"]})
    assert response.status_code == 422


def test_une_correction_incomplete_ne_peut_pas_etre_validee(client):
    student = "fares-laajili"
    client.get("/eleve/%s" % student)
    scoring_id, max_centi = _rows(student)[0]
    client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                json={"score_centi": max_centi})
    response = client.post("/eleve/%s/valider" % student)
    assert response.status_code == 400


def test_une_erreur_reste_sur_le_critere_echoue(client):
    """Deux critères dans un item : le code ne touche que celui qui a échoué."""
    student = "selim-mansouri"
    fill(client, student)      # effet de bord : la copie est remplie
    cible = "3E_SELIM_MANSOURI_B4_c2"
    voisin = "3E_SELIM_MANSOURI_B4_c1"
    assert client.post("/eleve/%s/critere/%s" % (student, cible),
                       json={"score_centi": 0, "error_codes": ["CALCUL"]}).status_code == 200
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        by_id = {r.scoring_id: r for r in correction.responses}
        assert json.loads(by_id[cible].error_codes_json) == ["CALCUL"]
        assert json.loads(by_id[voisin].error_codes_json) == []
        porteurs = [r.scoring_id for r in correction.responses
                    if json.loads(r.error_codes_json or "[]")]
        assert porteurs == [cible]


def test_validation_puis_verrouillage_puis_reouverture(client):
    student = "selim-mansouri"
    response = client.post("/eleve/%s/valider" % student, follow_redirects=False)
    assert response.status_code == 303
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        assert correction.status == "VALIDATED"
        premier = correction.revision
        scoring_id = correction.responses[0].scoring_id

    bloque = client.post("/eleve/%s/critere/%s" % (student, scoring_id),
                         json={"score_centi": 0})
    assert bloque.status_code == 423

    sans_raison = client.post("/eleve/%s/rouvrir" % student, json={"reason": "x"})
    assert sans_raison.status_code == 422

    ouvert = client.post("/eleve/%s/rouvrir" % student,
                         json={"reason": "score de B4 mal reporté, vérifié sur la copie"})
    assert ouvert.status_code == 200
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        courante = corr.current_correction(s, assessment.assessment_id)
        assert courante.revision == premier + 1
        assert courante.status == "DRAFT"
        anciennes = [c for c in assessment.corrections if not c.is_current]
        assert anciennes and anciennes[0].status == "VALIDATED"
        assert courante.reopen_reason


def test_la_certitude_n_est_saisissable_que_si_le_sujet_la_demande(client):
    student = "amine-mansouri"
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        avec = next(i for i in assessment.items if i.confidence_probe)
        sans = next(i for i in assessment.items if not i.confidence_probe)
    ok = client.post("/eleve/%s/item/%s/observation" % (student, avec.item_id),
                     json={"confidence": 3})
    assert ok.status_code == 200
    refus = client.post("/eleve/%s/item/%s/observation" % (student, sans.item_id),
                        json={"confidence": 3})
    assert refus.status_code == 400


def test_la_somme_des_sous_criteres_ne_depasse_pas_le_critere_mixte(client):
    from app.models import CriterionDefinition
    student = "malek-khadhrani"
    fill(client, student)
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        mixte = (s.query(CriterionDefinition)
                 .filter_by(curriculum_scope="mixed")
                 .filter(CriterionDefinition.criterion_id.like("1ERE_SPE_MALEK%")).one())
        parts = {p.virtual_criterion_id: p for p in mixte.virtual_parts}
        rows = {r.scoring_id: r for r in correction.responses}
        assert set(parts) <= set(rows)
        total = sum(rows[k].score_centi for k in parts)
        assert total == mixte.max_score_centi
        problems = validation.validate(s, correction, assessment)
        assert not [p for p in problems if p.code.startswith("mixte")]
