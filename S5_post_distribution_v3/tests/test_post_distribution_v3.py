# -*- coding: utf-8 -*-
"""Jeu de tests de la couche post-distribution V3.

Aucun test n'écrit dans S5_cloture, et aucun ne peut supprimer un artefact
distribué : les sorties de test vont dans un répertoire temporaire fourni par
pytest, et le gel est vérifié une dernière fois à la fin du module.
"""

import copy
import importlib.util
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(V3, "tools"))
sys.path.insert(0, HERE)

import pd_core as pd                                     # noqa: E402
import scope_rules                                        # noqa: E402
import equity_rules                                       # noqa: E402
import freeze_student_artifacts as freeze                  # noqa: E402
import verify_no_regression                                # noqa: E402
import verify_sources                                      # noqa: E402
import analyze_s5_post_distribution as A                   # noqa: E402
import migrate_responses_v2_to_v3 as MIG                    # noqa: E402
import check_bilan_language as LANG                         # noqa: E402
import pack_post_distribution as PACK                       # noqa: E402

import importlib.util


def _charger_voisin(nom, prefixe):
    """Charge un module voisin par son chemin, sous un nom de module unique.

    Trois fichiers ``make_fixture.py`` coexistent dans le dépôt (S5_cloture, sa copie
    d'audit, et la couche post-distribution V3). Un import par nom laisserait
    ``sys.modules`` en désigner un seul pour toute la session de tests, et les autres
    suites recevraient silencieusement le mauvais module. Le charger par chemin, sous un
    nom qualifié, supprime l'ambiguïté.
    """
    chemin = os.path.join(HERE, nom + ".py")
    unique = prefixe + nom
    spec = importlib.util.spec_from_file_location(unique, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique] = module
    spec.loader.exec_module(module)
    return module


make_fixture = _charger_voisin("make_fixture", "s5_v3_tests_")

SCOPE = pd.read_json(os.path.join(V3, "curriculum_scope", "criteria_scope.json"), "scope")
STUDENTS = pd.students()
STUDENT_IDS = [s["student_id"] for s in STUDENTS]


def _schema(name):
    return pd.read_json(os.path.join(V3, "schemas", name), "schéma")


# =========================================================== 1. gel des artefacts
def test_freeze_manifeste_couvre_les_60_artefacts():
    man = pd.read_json(os.path.join(V3, "IMMUTABLE_STUDENT_ARTIFACTS.json"), "gel")
    assert man["counts"]["couples_eleve_matiere"] == 15
    assert man["counts"]["student_pdf"] == 30
    assert man["counts"]["student_tex"] == 30
    assert len(man["artifacts"]) == 60
    assert all(a["status"] == "distributed" and a["mutability"] == "immutable"
               for a in man["artifacts"])


def test_aucun_artefact_eleve_n_a_change():
    res = freeze.verify()
    assert res["student_artifacts_changed"] == 0
    assert res["student_artifacts_missing"] == 0
    assert res["student_artifacts_added"] == 0
    assert res["verdict"] == "PASS"


def test_les_outils_v3_refusent_d_ecrire_hors_de_la_couche(tmp_path):
    with pytest.raises(pd.PostDistributionError):
        pd.write_json(os.path.join(pd.S5_ROOT, "interdit.json"), {})
    with pytest.raises(pd.PostDistributionError):
        pd.write_text(str(tmp_path / "interdit.md"), "x")


# ====================================================== 2. classement curriculaire
def test_chaque_critere_possede_un_curriculum_scope():
    assert SCOPE["counts"]["criteria_total"] == 337
    for c in SCOPE["criteria"]:
        assert c["curriculum_scope"] in scope_rules.SCOPES
        assert c["analysis_skill_id"]
        assert c["scope_rationale"]


def test_un_critere_mixte_est_eclate_a_somme_constante():
    mixtes = [c for c in SCOPE["criteria"] if c["curriculum_scope"] == "mixed"]
    assert mixtes, "le mécanisme des sous-critères virtuels doit être exercé sur des données réelles"
    for c in mixtes:
        subs = c["virtual_subcriteria"]
        assert len(subs) >= 2
        assert round(sum(v["points"] for v in subs), 6) == round(c["original_points"], 6)
        assert {v["curriculum_scope"] for v in subs} <= {"n_minus_1", "bridge_n"}


def test_les_alias_ne_fusionnent_plus_cosinus_et_sinus():
    alias = pd.read_json(os.path.join(V3, "curriculum_scope", "analysis_skills.json"), "alias")
    ids = {a["analysis_skill_id"]: a for a in alias["aliases"]}
    assert ids["M3_TRIGO_COS_NM1"]["curriculum_scope"] == "n_minus_1"
    assert ids["M3_TRIGO_SIN_BRIDGE"]["curriculum_scope"] == "bridge_n"
    assert ids["M3_TRIGO_COS_NM1"]["original_skill_ids"] == ["M3E_TRIG_01"]
    assert ids["M3_TRIGO_SIN_BRIDGE"]["original_skill_ids"] == ["M3E_TRIG_01"]


def test_le_produit_de_relatifs_est_une_passerelle_de_quatrieme():
    c = next(c for c in SCOPE["criteria"] if c["criterion_id"] == "4E_INES_KEFI_C2_c2")
    assert c["curriculum_scope"] == "bridge_n"
    assert c["analysis_skill_id"] == "M4E_REL_PROD_BRIDGE"
    somme = next(c for c in SCOPE["criteria"] if c["criterion_id"] == "4E_INES_KEFI_A1_c1")
    assert somme["curriculum_scope"] == "n_minus_1"


def test_les_references_curriculaires_ne_sont_jamais_inventees():
    refs = pd.read_json(os.path.join(V3, "curriculum_scope", "curriculum_references.json"), "refs")
    for key, lv in refs["levels"].items():
        for bloc in lv.values():
            if isinstance(bloc, dict) and "nor_documente" in bloc:
                if bloc["nor_documente"]:
                    assert bloc["nor"], key
                else:
                    assert bloc["nor"] is None and bloc.get("note"), key
    assert refs["levels"]["4e"]["curriculum_successor"]["applicable_to_grade_2026_2027"] is False
    assert refs["levels"]["3e"]["curriculum_successor"]["applicable_to_grade_2026_2027"] is False
    assert refs["levels"]["2nde"]["curriculum_current"]["nor"] == "MENE2602914A"
    assert refs["levels"]["1ere_spe"]["curriculum_current"]["nor"] == "MENE2602917A"
    assert refs["levels"]["1re_nsi"]["curriculum_current"]["nor"] == "MENE1901633A"


# ============================================================ 3. double décompte
@pytest.mark.parametrize("student_id", STUDENT_IDS)
def test_les_deux_pools_recomposent_exactement_vingt_points(student_id):
    doc = make_fixture.fill(student_id)
    a = A.analyse(student_id, doc)
    n1 = a["n_minus_1_consolidation"]["available"]
    br = a["bridge_n_readiness"]["available"]
    assert round(n1 + br, 6) == 20.0
    assert a["raw_assessment_score"]["max"] == 20


@pytest.mark.parametrize("student_id", STUDENT_IDS)
def test_aucun_critere_bridge_ne_contribue_a_la_consolidation(student_id):
    doc = make_fixture.fill(student_id)
    a = A.analyse(student_id, doc)
    n1_ids = {c["scoring_id"] for c in a["criteria"] if c["curriculum_scope"] == "n_minus_1"}
    br_ids = {c["scoring_id"] for c in a["criteria"] if c["curriculum_scope"] == "bridge_n"}
    assert not (n1_ids & br_ids)
    recompute = round(sum(c["score"] for c in a["criteria"]
                          if c["curriculum_scope"] == "n_minus_1" and c["score"] is not None), 4)
    assert recompute == a["n_minus_1_consolidation"]["earned"]
    for s in a["skills"]:
        assert s["curriculum_scope"] in ("n_minus_1", "bridge_n")


def test_le_score_brut_n_est_jamais_presente_comme_un_diagnostic():
    doc = make_fixture.fill("ahmad-beldi-nsi")
    a = A.analyse("ahmad-beldi-nsi", doc)
    assert a["raw_assessment_score"]["label"] == "score brut au sujet de clôture"
    assert "passerelle" in a["raw_assessment_score"]["avertissement"]


# ================================================== 4. attribution des erreurs
def test_un_code_d_erreur_ne_contamine_pas_un_critere_reussi():
    sid = "elyes-kefi"
    cible = "3E_ELYES_KEFI_B4_c2"
    doc = make_fixture.fill(sid, {cible: (0.0, ["METHODE"])})
    a = A.analyse(sid, doc)
    porteurs = [c["scoring_id"] for c in a["criteria"] if c["error_codes"]]
    assert porteurs == [cible]
    for c in a["criteria"]:
        if c["scoring_id"] != cible:
            assert c["error_codes"] == []
    voisins = [c for c in a["criteria"]
               if c["item_ref"] == "B4" and c["scoring_id"] != cible]
    assert voisins and all(c["error_codes"] == [] for c in voisins)


def test_un_code_d_erreur_sur_un_critere_integralement_reussi_est_refuse():
    doc = make_fixture.fill("elyes-kefi")
    for item in doc["responses"]:
        for c in item["criteria"]:
            c["error_codes"] = ["CALCUL"]
            break
        break
    with pytest.raises(A.InputError):
        A.analyse("elyes-kefi", doc)


def test_le_profil_d_erreurs_separe_les_deux_familles():
    sid = "fares-laajili"
    doc = make_fixture.fill(sid, {"3E_FARES_LAAJILI_C2_c1": (0.0, ["CONCEPT"]),
                                  "3E_FARES_LAAJILI_B1_c1": (0.0, ["CALCUL"])})
    a = A.analyse(sid, doc)
    assert a["error_profile"]["bridge_n"] == {"CONCEPT": 1}
    assert a["error_profile"]["n_minus_1"] == {"CALCUL": 1}


# ======================================================== 5. aucune progression
@pytest.mark.parametrize("student_id", STUDENT_IDS)
def test_mastery_delta_reste_nul(student_id):
    a = A.analyse(student_id, make_fixture.fill(student_id))
    assert a["baseline_measure_available"] is False
    for s in a["skills"]:
        assert s["mastery_delta"] is None
        assert s["delta_blocked_reason"]


# =================================================== 6. échec sur une passerelle
@pytest.mark.parametrize("student_id", [s["student_id"] for s in STUDENTS])
def test_un_echec_sur_une_passerelle_ne_cree_jamais_de_deficit(student_id):
    bridge = [c["criterion_id"] for c in SCOPE["criteria"]
              if c["student_id"] == student_id and c["curriculum_scope"] == "bridge_n"]
    bridge += [v["virtual_criterion_id"] for c in SCOPE["criteria"]
               if c["student_id"] == student_id and c["curriculum_scope"] == "mixed"
               for v in c["virtual_subcriteria"] if v["curriculum_scope"] == "bridge_n"]
    if not bridge:
        pytest.skip("aucun critère de passerelle pour cet élève")
    doc = make_fixture.fill(student_id, {cid: (0.0, ["CONCEPT"]) for cid in bridge})
    a = A.analyse(student_id, doc)
    assert a["n_minus_1_consolidation"]["percentage"] == 100.0
    for p in a["action_plan_inputs"]["n_minus_1_priorities"]:
        assert p["priority_rank"] == "OK"
    for b in a["action_plan_inputs"]["bridge_actions"]:
        assert b["action"] in ("BRIDGE_REVISIT", "DISCOVERY_TO_CONTINUE")
        assert "priority_rank" not in b
    for s in a["skills"]:
        if s["curriculum_scope"] == "bridge_n":
            assert s["interpretation"]["status"] in scope_rules.BRIDGE_STATUSES
            texte = " ".join(s["interpretation"]["authorised_wording"]).lower()
            assert "non acquis" not in texte and "lacune" not in texte
            assert "fragile" not in texte
    plan = A.build_plan(a)
    for w in plan["consolidation_n_minus_1"]:
        assert not w["skills"]


# ================================================ 7. quatre questions délicates
def test_les_quatre_cas_documentes_sont_traites():
    par_id = {c["criterion_id"]: c for c in SCOPE["criteria"]}

    sinda = par_id["4E_SINDA_CHIKHAOUI_C2_c2"]
    assert sinda["evidence_quality"] == "limited_by_prompt"
    assert any("parallélogramme" in m for m in sinda["accepted_methods"])
    assert any("rectangle" in m for m in sinda["rejected_as_general_justification"])

    elyes = par_id["3E_ELYES_KEFI_B4_c2"]
    assert any("recomptage" in m for m in elyes["accepted_methods"])
    assert any("encadrement" in m for m in elyes["rejected_as_detection"])

    ahmad = par_id["1ERE_SPE_AHMAD_BELDI_B4_c1"]
    assert "proof_levels" in ahmad
    assert "niveau_demande" in ahmad["proof_levels"]
    assert "preuve_renforcee" in ahmad["proof_levels"]
    assert any("démonstration universelle" in l for l in ahmad["interpretation_limits"])

    malek = par_id["1ERE_SPE_MALEK_KHADHRANI_C2_c2"]
    assert any("contre-exemple" in m for m in malek["accepted_methods"])
    assert any("monotonie" in l for l in malek["interpretation_limits"])


def test_le_cas_liste_vide_de_b2_reste_hors_barreme():
    for sid in ("ahmad-beldi-nsi", "ahmed-benhadj-salem"):
        obs = equity_rules.non_scored_for(sid, "B2")
        assert obs and "division par zéro" in obs[0]["observation"]
        pol = pd.read_json(os.path.join(V3, "correction_overlays", sid,
                                        "CORRECTION_POLICY.json"), "policy")
        assert any(r["item_ref"] == "B2" for r in pol["teacher_observation_non_scored"])
        a = A.analyse(sid, make_fixture.fill(sid))
        b2 = [c for c in a["criteria"] if c["item_ref"] == "B2"]
        assert len(b2) == 2 and all(not c["error_codes"] for c in b2)


def test_une_methode_alternative_correcte_n_est_pas_une_erreur():
    sid = "fares-laajili"
    doc = make_fixture.fill(sid)
    for item in doc["responses"]:
        for c in item["criteria"]:
            if c["criterion_id"] == "3E_FARES_LAAJILI_C2_c1":
                c["accepted_alternative_method"] = True
                c["observation"] = "Pythagore puis cosinus : voie N-1 correcte"
    a = A.analyse(sid, doc)
    crit = next(c for c in a["criteria"] if c["scoring_id"] == "3E_FARES_LAAJILI_C2_c1")
    assert crit["accepted_alternative_method"] is True
    assert crit["error_codes"] == []


# ============================================================== 8. JSON Schema
@pytest.mark.parametrize("student_id", STUDENT_IDS)
def test_les_sorties_reelles_valident_le_schema_v3(student_id):
    jsonschema = pytest.importorskip("jsonschema")
    tpl = pd.read_json(os.path.join(V3, "responses",
                                    "responses_v3_TEMPLATE_%s.json" % student_id), "gabarit")
    jsonschema.validate(tpl, _schema("responses_v3.schema.json"))
    doc = make_fixture.fill(student_id)
    jsonschema.validate(doc, _schema("responses_v3.schema.json"))
    a = A.analyse(student_id, doc)
    jsonschema.validate(a, _schema("post_stage_analysis_v3.schema.json"))


# ============================================================ 9. saisie refusée
def test_un_score_manquant_arrete_l_analyse():
    doc = make_fixture.fill("noa-maniaci")
    doc["responses"][0]["criteria"][0]["score"] = None
    with pytest.raises(A.InputError):
        A.analyse("noa-maniaci", doc)


def test_un_statut_requires_human_allocation_arrete_l_analyse():
    doc = make_fixture.fill("noa-maniaci",
                            {"2NDE_NOA_MANIACI_A1_c1": ("REQUIRES_HUMAN", [])})
    with pytest.raises(A.InputError):
        A.analyse("noa-maniaci", doc)


def test_un_critere_neutralise_sort_des_deux_decomptes():
    doc = make_fixture.fill("sinda-chikhaoui",
                            {"4E_SINDA_CHIKHAOUI_C2_c2": ("NEUTRALISE", [])})
    a = A.analyse("sinda-chikhaoui", doc)
    assert a["raw_assessment_score"]["neutralised_points"] == 1.0
    assert a["n_minus_1_consolidation"]["available"] == 19.0
    assert len(a["neutralised_criteria"]) == 1


# ================================================================ 10. migration
def test_le_migrateur_n_invente_aucune_ventilation():
    sid = "ines-kefi"
    v2 = pd.read_json(os.path.join(next(s["dir"] for s in STUDENTS if s["student_id"] == sid),
                                   "responses_TEMPLATE.json"), "gabarit V2")
    v2 = copy.deepcopy(v2)
    for item in v2["responses"]:
        for c in item["criteria"]:
            c["score"] = c["max_points"]
        if item["ref"] == "C2":
            item["criteria"][0]["score"] = 0.0
            item["criteria"][1]["score"] = 0.0
            item["error_codes"] = ["CONCEPT", "CALCUL"]
    doc, report = MIG.migrate(v2, sid)
    assert report["error_codes_non_attribuables"] == 2
    assert report["criteria_requires_human_allocation"] >= 2
    with pytest.raises(A.InputError):
        A.analyse(sid, doc)


def test_le_migrateur_reporte_un_code_sans_ambiguite():
    sid = "ines-kefi"
    v2 = copy.deepcopy(pd.read_json(
        os.path.join(next(s["dir"] for s in STUDENTS if s["student_id"] == sid),
                     "responses_TEMPLATE.json"), "gabarit V2"))
    for item in v2["responses"]:
        for c in item["criteria"]:
            c["score"] = c["max_points"]
        if item["ref"] == "C2":
            item["criteria"][1]["score"] = 0.0
            item["error_codes"] = ["CONCEPT"]
    doc, report = MIG.migrate(v2, sid)
    assert report["error_codes_reportes"] == 1
    cible = [c for it in doc["responses"] for c in it["criteria"]
             if c["criterion_id"] == "4E_INES_KEFI_C2_c2"]
    assert cible and cible[0]["error_codes"] == ["CONCEPT"]


# ====================================================== 11. langage du bilan
def test_les_formulations_interdites_sont_detectees():
    facts = {"progression_chiffree_possible": False,
             "premieres_passerelles": [{"analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
                                        "label": "Algorithmes de recherche : séquentielle et "
                                                 "dichotomique"}],
             "reussites_immediates_a_confirmer": ["NSI1_ACC_01"],
             "_skills": [{"analysis_skill_id": "NSI1_TEST_01", "evidence_strength": "low"}]}
    interdits = [
        "L'élève affiche une progression de 40 %.",
        "Il a progressé de 2 niveaux.",
        "Il maîtrise désormais les tests.",
        "La recherche séquentielle n'est pas acquise.",
        "On note une lacune sur les algorithmes de recherche.",
        "Cet acquis est durablement consolidé.",
        "Avec 7/20, le niveau insuffisant est confirmé.",
    ]
    for phrase in interdits:
        assert LANG.check(phrase, facts), phrase


def test_les_formulations_autorisees_passent():
    facts = {"progression_chiffree_possible": False,
             "premieres_passerelles": [{"analysis_skill_id": "NSI1_ALGO_RECHERCHE_BRIDGE",
                                        "label": "Algorithmes de recherche"}],
             "reussites_immediates_a_confirmer": [], "_skills": []}
    autorisees = [
        "Le calcul sur les fractions est actuellement réussi sur deux critères distincts ; "
        "cette réussite reste à confirmer dans la durée.",
        "La recherche séquentielle a été abordée comme première passerelle vers la Première NSI.",
        "Le diagnostic initial signalait une fragilité en calcul littéral ; l'évaluation apporte "
        "plusieurs éléments positifs, sans progression chiffrée.",
    ]
    for phrase in autorisees:
        assert LANG.check(phrase, facts) == [], phrase


# ============================================================== 12. packaging
def test_le_packager_refuse_les_destinations_dangereuses(tmp_path):
    for dangereux in (os.sep, os.path.expanduser("~"), pd.REPO_ROOT, pd.S5_ROOT,
                      os.path.join(pd.S5_ROOT, "quelque_part"), pd.V3_ROOT):
        with pytest.raises(pd.PostDistributionError):
            PACK.check_destination(dangereux, pd.V3_ROOT)
    existant = tmp_path / "deja_la"
    existant.mkdir()
    (existant / "important.txt").write_text("ne pas supprimer", encoding="utf-8")
    with pytest.raises(pd.PostDistributionError):
        PACK.check_destination(str(existant), pd.V3_ROOT)
    assert (existant / "important.txt").exists()


def test_le_packager_ne_touche_a_aucun_artefact_eleve(tmp_path):
    avant = freeze.verify()
    PACK.build(pd.V3_ROOT, str(tmp_path / "paquet"))
    apres = freeze.verify()
    assert avant["student_artifacts_changed"] == apres["student_artifacts_changed"] == 0
    contenu = [f for _, f in PACK.iter_files(str(tmp_path / "paquet"))]
    assert not any(f.endswith(".pdf") for f in contenu)


# ========================================================= 13. non-régression
def test_le_controle_de_non_regression_passe():
    res = verify_no_regression.run(check_pdf_text=False)
    assert res["student_artifacts_changed"] == 0
    for c in res["checks"]:
        assert c["verdict"] in ("PASS", "NON EXÉCUTÉ"), c


def test_la_tracabilite_des_sources_distingue_les_deux_modes():
    live = verify_sources.verify("live")
    assert live["verdict"] == "PASS"
    assert live["standalone_bundle"] is False
    man = verify_sources.verify("manifest")
    assert man["verdict"] == "PASS WITH LIMITATION"
    assert man["standalone_bundle"] is True
    assert man["limitation"]


# ========================== dernier mot : rien n'a bougé pendant les tests
def test_zzz_les_artefacts_eleves_sont_intacts_apres_tous_les_tests():
    assert freeze.verify()["student_artifacts_changed"] == 0
