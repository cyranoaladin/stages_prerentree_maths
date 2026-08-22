# -*- coding: utf-8 -*-
"""Analyse : séparation des deux décomptes, force de preuve, absence de faux delta."""


from app import database
from app.models import Assessment
from app.domain import action_plan
from app.domain import analysis as ana
from app.domain import correction as corr
from app.domain import evidence
from conftest import fill

BRIDGE_STUDENTS = ["ahmad-beldi-nsi", "ahmed-benhadj-salem", "fares-laajili", "elyes-kefi",
                   "ines-kefi", "ahmad-beldi-maths"]


def _analyse(client, student_id, overrides=None):
    fill(client, student_id, overrides)
    client.post("/eleve/%s/valider" % student_id, follow_redirects=False)
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student_id).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        payload = ana.analyse(s, correction, assessment)
        plan = action_plan.build(payload, [])
    return payload, plan


def test_le_score_brut_vaut_vingt_quand_tout_est_reussi(client):
    payload, _ = _analyse(client, "noa-maniaci")
    assert payload["raw_assessment_score"]["earned_centi"] == 2000
    assert payload["raw_assessment_score"]["sur_20"] == "20"
    n1 = payload["n_minus_1_consolidation"]["available_centi"]
    bridge = payload["bridge_n_readiness"]["available_centi"]
    assert n1 + bridge == 2000


def test_aucun_double_comptage_entre_les_deux_pools(client):
    payload, _ = _analyse(client, "ahmad-beldi-maths")
    n1_ids = {c["scoring_id"] for c in payload["criteria"]
              if c["curriculum_scope"] == "n_minus_1"}
    bridge_ids = {c["scoring_id"] for c in payload["criteria"]
                  if c["curriculum_scope"] == "bridge_n"}
    assert not (n1_ids & bridge_ids)
    recompute = sum(c["score_centi"] for c in payload["criteria"]
                    if c["curriculum_scope"] == "n_minus_1" and c["score_centi"] is not None)
    assert recompute == payload["n_minus_1_consolidation"]["earned_centi"]


def test_un_echec_total_sur_les_passerelles_ne_degrade_pas_les_acquis(client):
    """Le scénario du cahier des charges : tout N−1 réussi, tout bridge échoué."""
    student = "ahmad-beldi-nsi"
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=student).one()
        bridge_ids = []
        for item in assessment.items:
            for crit in item.criteria:
                if crit.curriculum_scope == "bridge_n":
                    bridge_ids.append(crit.criterion_id)
                for part in crit.virtual_parts:
                    if part.curriculum_scope == "bridge_n":
                        bridge_ids.append(part.virtual_criterion_id)
    assert bridge_ids
    overrides = {sid: {"score_centi": 0, "error_codes": ["CONCEPT"]} for sid in bridge_ids}
    payload, plan = _analyse(client, student, overrides)

    assert payload["n_minus_1_consolidation"]["percentage"] == 100.0
    assert payload["bridge_n_readiness"]["percentage"] == 0.0
    for skill in payload["skills"]:
        if skill["curriculum_scope"] == "n_minus_1":
            assert skill["status"] in ("SOLIDE", "SATISFAISANT", "A_CONFIRMER",
                                        "PREUVE_INSUFFISANTE")
            assert skill["priority_rank"] in ("OK", "P3")
        else:
            assert skill["status"] in ana.BRIDGE_STATUSES
            assert skill["bridge_action"] in ("BRIDGE_REVISIT", "DISCOVERY_TO_CONTINUE")
            texte = (skill["reading"] + skill["status_label"]).lower()
            for interdit in ("non acquis", "lacune", "fragile"):
                assert interdit not in texte
    assert not [p for p in payload["priorities"] if p["priority_rank"] in ("P1", "P2")]
    assert all(b["action"] == "BRIDGE_REVISIT" for b in plan["bridge_actions"])
    assert payload["error_profile"]["n_minus_1"] == {}
    assert payload["error_profile"]["bridge_n"] == {"CONCEPT": len(bridge_ids)}


def test_le_code_erreur_ne_touche_qu_une_competence(client):
    student = "sarah-bargaoui"
    cible = "3E_SARAH_BARGAOUI_C2_c2"
    payload, _ = _analyse(client, student,
                          {cible: {"score_centi": 0, "error_codes": ["CALCUL"]}})
    porteuses = [s for s in payload["skills"] if s["error_codes"]]
    assert len(porteuses) == 1
    assert porteuses[0]["errors"][0]["scoring_id"] == cible
    assert sum(payload["error_profile"]["n_minus_1"].values()) == 1


def test_aucune_progression_chiffree(client):
    payload, plan = _analyse(client, "amine-mansouri")
    assert payload["baseline_measure_available"] is False
    assert payload["mastery_delta"] is None
    for skill in payload["skills"]:
        assert skill["mastery_delta"] is None
        assert skill["delta_blocked_reason"]
    assert plan["progression_chiffree_possible"] is False


def test_un_score_parfait_sur_une_preuve_faible_ne_donne_pas_solide(client):
    payload, _ = _analyse(client, "donia-khadhrani")
    for skill in payload["skills"]:
        if skill["status"] == "SOLIDE":
            assert evidence.at_least(skill["evidence_strength"], "MODERATE")


def test_la_recence_produit_a_confirmer_et_un_controle_differe(client):
    payload, _ = _analyse(client, "ines-kefi")
    immediates = [s for s in payload["skills"] if s["recommended_delayed_check"]]
    assert immediates
    for skill in immediates:
        if skill["curriculum_scope"] == "n_minus_1" and skill["success_rate"] >= 0.85:
            assert skill["status"] == "A_CONFIRMER"
    assert payload["retention"]["skills"]


def test_les_trois_blocs_de_conclusion_existent(client):
    payload, _ = _analyse(client, "fares-darghouth")
    assert set(payload["conclusions"]) == {"etayees", "prudentes", "limites"}
    joined = " ".join(payload["conclusions"]["limites"])
    assert "aucune progression chiffrée" in joined.lower()


def test_le_plan_tient_en_deux_ou_trois_objectifs_par_semaine(client):
    payload, plan = _analyse(client, "fares-laajili",
                             {"3E_FARES_LAAJILI_A1_c1": {"score_centi": 0,
                                                          "error_codes": ["CALCUL"]},
                              "3E_FARES_LAAJILI_A3_c1": {"score_centi": 0,
                                                          "error_codes": ["CALCUL"]}})
    assert len(plan["weeks"]) == 4
    for week in plan["weeks"]:
        assert len(week["objectives"]) <= 3
    assert plan["weeks"][1]["week"] == 2
