# -*- coding: utf-8 -*-
"""Les quatre questions à correction délicate, et le cas NSI de la liste vide.

Ces tests vérifient que le corrigé affiché au correcteur porte bien la règle d'équité,
et que ce qui est hors barème le reste.
"""

import json

from app.models import CriterionDefinition, ItemDefinition


def _criterion(session, criterion_id):
    crit = session.get(CriterionDefinition, criterion_id)
    assert crit is not None, criterion_id
    return crit


def test_sinda_l_aire_du_triangle_passe_par_le_parallelogramme(session):
    crit = _criterion(session, "4E_SINDA_CHIKHAOUI_C2_c2")
    methodes = " ".join(json.loads(crit.accepted_methods_json))
    assert "parallélogramme" in methodes
    rejected = json.loads(crit.rejected_json or "{}")
    refuse = " ".join(rejected.get("general_justification") or [])
    assert "rectangle" in refuse
    assert crit.evidence_quality == "limited_by_prompt"
    assert crit.teacher_correction and "parallélogramme" in crit.teacher_correction


def test_elyes_l_encadrement_ne_prouve_pas_la_detection(session):
    crit = _criterion(session, "3E_ELYES_KEFI_B4_c2")
    methodes = " ".join(json.loads(crit.accepted_methods_json))
    assert "recomptage" in methodes
    rejected = json.loads(crit.rejected_json or "{}")
    refuse = " ".join(rejected.get("detection") or [])
    assert "encadrement" in refuse and "11,25" in refuse


def test_ahmad_un_argument_general_sans_formalisme_impose(session):
    crit = _criterion(session, "1ERE_SPE_AHMAD_BELDI_B4_c1")
    niveaux = json.loads(crit.proof_levels_json)
    assert "argument valable pour tout" in niveaux["niveau_demande"]
    assert "jamais exigée" in niveaux["preuve_renforcee"]
    regles = " ".join(json.loads(crit.fairness_rules_json))
    assert "formalisme" in regles
    limites = " ".join(json.loads(crit.interpretation_limits_json))
    assert "démonstration universelle" in limites
    # La consigne réellement imprimée demande bien un argument général.
    assert "argument valable pour tout" in (crit.printed_prompt or "")


def test_malek_un_contre_exemple_suffit(session):
    crit = _criterion(session, "1ERE_SPE_MALEK_KHADHRANI_C2_c2")
    methodes = " ".join(json.loads(crit.accepted_methods_json))
    assert "contre-exemple" in methodes
    regles = " ".join(json.loads(crit.fairness_rules_json))
    assert "contre-exemple suffit" in regles
    limites = " ".join(json.loads(crit.interpretation_limits_json))
    assert "monotonie" in limites


def test_nsi_le_cas_de_la_liste_vide_reste_hors_bareme(session):
    from app.models import Assessment
    for student_id in ("ahmad-beldi-nsi", "ahmed-benhadj-salem"):
        assessment = session.query(Assessment).filter_by(student_id=student_id).one()
        item = next(i for i in assessment.items if i.ref == "B2")
        observations = json.loads(item.teacher_observation_non_scored_json)
        assert observations
        assert "division par zéro" in observations[0]["observation"]
        assert "aucun critère du barème ne le rétribue" in observations[0]["raison"]
        assert "hors score" in observations[0]["consequence"] \
            or "aucun code d'erreur scoré" in observations[0]["consequence"]
        # Et aucun critère du barème ne le rétribue.
        descriptions = " ".join(c.description for c in item.criteria)
        assert "liste vide" not in descriptions


def test_nsi_le_test_sur_liste_vide_de_c1_est_bien_au_bareme(session):
    """En C1, l'énoncé imprimé le demande explicitement : il est légitimement scoré."""
    crit = _criterion(session, "1RE_NSI_AHMAD_BELDI_C1_c3")
    assert "liste vide" in crit.description
    assert crit.curriculum_scope == "n_minus_1"


def test_une_methode_alternative_correcte_n_est_pas_une_erreur(client, session):
    from app import database
    from app.models import Assessment
    from app.domain import correction as corr
    student = "fares-laajili"
    client.get("/eleve/%s" % student)
    cible = "3E_FARES_LAAJILI_C2_c1"
    response = client.post("/eleve/%s/critere/%s" % (student, cible),
                           json={"score_centi": 100, "error_codes": [],
                                 "accepted_alternative_method": True,
                                 "observation": "Pythagore puis cosinus : voie N−1 correcte"})
    assert response.status_code == 200
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        row = next(r for r in corr.current_correction(s, assessment.assessment_id).responses
                   if r.scoring_id == cible)
        assert row.accepted_alternative_method is True
        assert json.loads(row.error_codes_json) == []
