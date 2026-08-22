# -*- coding: utf-8 -*-
"""Pipeline de bilan longitudinal : preuves, trajectoire, plan, langue.

Aucun score réel n'est saisi. Les copies sont des fixtures synthétiques, dans des
bases jetables créées par conftest, et les noms de scénarios le disent.

Le test qui compte le plus est ``test_notion_ciblee_mais_non_evaluee`` : il vérifie
que le système refuse le glissement « figure au livret de la séance 1 » → « acquise ».
C'est la faute que ce pipeline existe pour empêcher.
"""

import json

import pytest

from app import database
from app.domain import correction as corr
from app.domain.longitudinal import (LongitudinalReportService,
                                     dossier, evidence_levels, guard, narrative,
                                     plan as plan_module, render, sources)
from app.models import Assessment

STUDENT = "ines-kefi"
TEST_LABEL = "TEST_INES"        # marqueur des données synthétiques

# Les quatre lignes de passerelle du sujet d'Inès.
BRIDGE = ("4E_INES_KEFI_B2_c1", "4E_INES_KEFI_B2_c2",
          "4E_INES_KEFI_C2_c2", "4E_INES_KEFI_A3_c1_v2")


# ------------------------------------------------------------------ fixtures
def _rouvrir_si_verrouillee(client, session_scope):
    """Une correction validée est verrouillée : la rouvrir est la voie prévue.

    Les tests de ce module enchaînent plusieurs copies synthétiques sur le même
    élève ; chacune doit repartir d'une correction modifiable, exactement comme
    le ferait un enseignant qui corrige une erreur de saisie.
    """
    with session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(s, assessment.assessment_id)
        verrouillee = courante is not None and courante.status != "DRAFT"
    if verrouillee:
        client.post("/eleve/%s/rouvrir" % STUDENT,
                    json={"reason": "%s — nouveau scénario synthétique" % TEST_LABEL},
                    follow_redirects=False)


def _remplir(client, session_scope, overrides_fn, valider=True):
    """Remplit une copie de façon synthétique, puis la valide."""
    client.get("/eleve/%s" % STUDENT)
    _rouvrir_si_verrouillee(client, session_scope)
    with session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        lignes = [(r.scoring_id, r.max_score_centi)
                  for r in corr.current_correction(s, assessment.assessment_id).responses]
    for scoring_id, maximum in lignes:
        reponse = client.post("/eleve/%s/critere/%s" % (STUDENT, scoring_id),
                              json=overrides_fn(scoring_id, maximum))
        assert reponse.status_code == 200, (scoring_id, reponse.text)
    if valider:
        client.post("/eleve/%s/valider" % STUDENT, follow_redirects=False)


def _faits(session_scope, persist=False):
    with session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(s, assessment.assessment_id)
        return LongitudinalReportService(s).build_longitudinal_facts(
            assessment, courante, persist=persist)


def _tout_reussi_sauf_passerelles(scoring_id, maximum):
    if scoring_id in BRIDGE:
        return {"score_centi": 0, "error_codes": ["CONCEPT"]}
    return {"score_centi": maximum, "error_codes": []}


@pytest.fixture(scope="module")
def facts(client):
    """Copie synthétique : prérequis réussis, passerelles échouées."""
    _remplir(client, database.session_scope, _tout_reussi_sauf_passerelles)
    return _faits(database.session_scope)


# =============================================== 1. verrous d'entrée (§17, §54)
def test_une_correction_non_validee_ne_produit_pas_de_bilan(client):
    """§17 — un brouillon peut encore changer ; il ne fonde pas un bilan remis."""
    class _Brouillon:
        status = "DRAFT"
        responses = []
    obstacles = LongitudinalReportService.check_ready(_Brouillon())
    assert obstacles
    assert "validée" in obstacles[0]


def test_une_ligne_non_saisie_bloque_la_generation():
    class _Partielle:
        status = "VALIDATED"

        class _Ligne:
            scoring_status = "PENDING"
            scoring_id = "X"
        responses = [_Ligne()]
    obstacles = LongitudinalReportService.check_ready(_Partielle())
    assert any("ne sont pas renseignées" in o for o in obstacles)


def test_absence_de_correction_est_un_obstacle_explicite():
    assert LongitudinalReportService.check_ready(None) == [
        "aucune correction n'existe pour cet élève"]


# ================================================== 2. sources (§4, §5, §53, §61)
def test_le_diagnostic_initial_est_utilise(facts):
    diag = facts["initial_diagnostic"]
    assert diag["available"] is True
    assert diag["instrument"]["file"].endswith("4e_Test_Initial.pdf")
    assert diag["date"]
    assert diag["strengths"] and diag["priorities"]
    # sept domaines statués au diagnostic
    assert len(diag["domain_observations"]) == 7


def test_les_cinq_seances_sont_utilisees(facts):
    seances = facts["stage_trajectory"]["sessions"]
    assert [s["session"] for s in seances] == ["S1", "S2", "S3", "S4", "S5"]
    # chaque séance porte l'objectif personnalisé écrit au dossier de l'élève
    assert all(s["personal_focus"] for s in seances)
    # et au moins une compétence ciblée
    assert sum(1 for s in seances if s["skills_targeted"]) >= 4


def test_chaque_source_presente_porte_une_empreinte(facts):
    for releve in facts["sources"]:
        if releve["present"]:
            assert releve["source_sha256"], releve["source_path"]
            assert len(releve["source_sha256"]) == 64


def test_une_source_absente_est_declaree_et_jamais_inventee(facts):
    """§53 — aucun dossier personnalisé n'existe pour S1 : on le dit."""
    absentes = [r for r in facts["sources"] if not r["present"]]
    assert absentes, "le corpus d'Inès comporte au moins une source absente"
    for releve in absentes:
        assert releve["note"], "une absence sans motif est une omission silencieuse"
        assert releve["source_sha256"] is None
    limites = " ".join(facts["interpretation_limits"])
    assert "n'ont pas été trouvées" in limites or "aucun dossier" in limites


def test_un_document_couvrant_deux_seances_vaut_pour_les_deux():
    """« LIVRETS_S4_S5 » ne doit pas faire déclarer S5 manquante."""
    assert sources._sessions_of("Bilans/4e_X_LIVRETS_S4_S5_PERSONNALISES.pdf") == ["S4", "S5"]
    assert sources._sessions_of("4e/02_SEANCES/S3") == ["S3"]


# ========================================= 3. modèle de preuve (§2, §3, §22, §74)
def test_la_hierarchie_de_preuve_est_ordonnee():
    assert evidence_levels.strongest(["C", "A", "D"]) == "A"
    assert evidence_levels.strongest([]) == "D"
    assert evidence_levels.may_assert_mastery("A") is True
    for niveau in ("B", "C", "D"):
        assert evidence_levels.may_assert_mastery(niveau) is False


def test_une_notion_du_livret_ne_vaut_pas_une_preuve_de_reussite(facts):
    """§3 — la présence au livret est une preuve de parcours, de niveau C."""
    parcours = [f for f in facts["provenance"] if f["source_type"] == "session_material"]
    assert parcours
    for fait in parcours:
        assert fait["evidence_level"] == "C"
        assert "ciblée" in fait["statement"]
        assert "acquise" not in fait["statement"]


def test_notion_ciblee_mais_non_evaluee(facts):
    """§74 — travaillée pendant le stage, mesurée par aucun critère.

    Attendu : worked_during_stage = True, current_mastery = unknown, et le mot
    « acquise » n'apparaît nulle part à son sujet dans le document parents.
    """
    sans_preuve = facts["without_final_evidence"]
    assert sans_preuve, "le corpus d'Inès comporte une compétence non évaluée"
    for entree in sans_preuve:
        assert entree["current_mastery"] == "unknown"
    travaillees = [e for e in sans_preuve if e["worked_during_stage"]]
    assert travaillees, "au moins une notion ciblée n'est pas évaluée"

    ligne = next(l for l in facts["skills"]
                 if l["label"] == travaillees[0]["label"] and not l["has_final_evidence"])
    assert ligne["evidence_level"] in ("C", "D")
    assert ligne["trajectory_status"] == "PREUVE_FINALE_INSUFFISANTE"
    assert ligne["mastery_delta"] is None

    blocs = narrative.parent_blocks(facts)
    texte = "\n".join(c for _, _, c in blocs)
    manquements = guard.check_mastery_claims(facts["skills"], texte)
    assert manquements == [], manquements


def test_la_couverture_ne_se_confond_jamais_avec_la_maitrise():
    """§16, §47 — deux axes distincts, calculés séparément."""
    assert evidence_levels.coverage_of([]) == "NONE"
    assert evidence_levels.coverage_of(["S1"]) == "LIGHT"
    assert evidence_levels.coverage_of(["S1"], targeted_in_s5=True) == "MODERATE"
    assert evidence_levels.coverage_of(["S1", "S3"], True, True) == "STRONG"


# ==================================== 4. trajectoire qualitative (§7, §8, §75, §76)
def test_aucune_progression_chiffree_n_est_produite(facts):
    """§7 — les mesures pré et post ne sont pas parallèles."""
    assert facts["mastery_delta"] is None
    assert facts["mastery_delta_blocked_reason"]
    for ligne in facts["skills"]:
        assert ligne["mastery_delta"] is None
    assert facts["initial_diagnostic"]["nominative_measure_available"] is False


def test_fragilite_initiale_plus_reussites_finales_donne_une_trajectoire_positive(facts):
    """§75 — qualitative_trajectory = positive_evidence, mastery_delta = null."""
    concernees = [l for l in facts["skills"]
                  if l["initial_status"] in ("fragile", "en_voie_acquisition")
                  and l["has_final_evidence"]
                  and l["final_status"] in ("SOLIDE", "SATISFAISANT")]
    assert concernees, "la copie synthétique réussit les prérequis"
    for ligne in concernees:
        assert ligne["qualitative_trajectory"] == "positive_evidence"
        assert ligne["mastery_delta"] is None
        assert ligne["trajectory_status"] in (
            "CONSOLIDATION_OBSERVEE", "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION")


def test_fragilite_initiale_plus_fragilite_finale(client):
    """L'inverse : le point signalé au départ se retrouve à l'évaluation."""
    echec = ("A1", "A5")

    def override(scoring_id, maximum):
        ref = scoring_id.replace("4E_INES_KEFI_", "").split("_")[0]
        if ref in echec:
            return {"score_centi": 0, "error_codes": ["CONCEPT"]}
        return {"score_centi": maximum, "error_codes": []}

    _remplir(client, database.session_scope, override)
    faits = _faits(database.session_scope)
    negatives = [l for l in faits["skills"]
                 if l["qualitative_trajectory"] == "persistent_difficulty"]
    assert negatives
    for ligne in negatives:
        assert ligne["initial_status"] in ("fragile", "en_voie_acquisition", None)
        assert ligne["trajectory_status"] in ("FRAGILITE_PERSISTANTE",
                                              "FRAGILITE_INITIALE_CONFIRMEE")
        assert ligne["mastery_delta"] is None


def test_un_echec_de_passerelle_ne_cree_aucune_priorite_n_moins_1(facts):
    """§76 — une notion de l'année à venir n'est pas un prérequis manquant."""
    passerelles = [l for l in facts["skills"] if l["curriculum_scope"] == "bridge_n"]
    assert len(passerelles) == 4
    for ligne in passerelles:
        assert ligne["priority_rank"] is None
        assert ligne["trajectory_status"].startswith("BRIDGE_")
        assert ligne["initial_status"] is None   # aucun diagnostic sur une découverte
    # aucune passerelle dans les priorités de consolidation ni dans le plan N−1
    labels_passerelles = {l["label"] for l in passerelles}
    for priorite in facts["consolidation_priorities"]:
        assert priorite["label"] not in labels_passerelles
    for semaine in facts["four_week_plan"]["weeks"]:
        for objectif in semaine["objectives"]:
            assert objectif["kind"] != "bridge_n"


def test_le_vocabulaire_des_passerelles_ne_disqualifie_jamais(facts):
    blocs = dict((cle, contenu) for cle, _, contenu in narrative.parent_blocks(facts))
    texte = blocs["passerelles"].lower()
    for interdit in ("lacune", "non acquis", "retard", "insuffisance"):
        assert interdit not in texte
    assert "passerelle" in texte or "année à venir" in texte


# ================================================== 5. récence et rétention (§10, §77)
def test_reussite_immediate_apres_remediation_donne_a_confirmer(facts):
    """§77 — A_CONFIRMER, et un mini-test différé en semaine 2."""
    a_confirmer = [l for l in facts["skills"]
                   if l["trajectory_status"] == "REUSSITE_A_CONFIRMER"]
    assert a_confirmer, "au moins une compétence a été retravaillée puis évaluée aussitôt"
    for ligne in a_confirmer:
        assert ligne["retention_status"] == "not_yet_verified"
        assert ligne["recommended_delayed_check"] is True

    semaine2 = next(w for w in facts["four_week_plan"]["weeks"] if w["week"] == 2)
    differes = [o for o in semaine2["objectives"] if o["is_delayed_check"]]
    assert differes, "la semaine 2 doit porter le contrôle différé"
    for objectif in differes:
        assert "sans révision" in objectif["objective"] or "distance" in objectif["objective"]


# ===================================================== 6. plan de rentrée (§30-§36, §49)
def test_le_plan_couvre_quatre_semaines(facts):
    semaines = facts["four_week_plan"]["weeks"]
    assert [w["week"] for w in semaines] == [1, 2, 3, 4]


def test_chaque_objectif_porte_un_seuil_mesurable(facts):
    """§36 — un objectif sans seuil constatable n'est pas un objectif."""
    for semaine in facts["four_week_plan"]["weeks"]:
        for objectif in semaine["objectives"]:
            seuil = objectif["success_threshold"]
            assert seuil, objectif
            assert any(marqueur in seuil
                       for marqueur in (" sur ", "même résultat", "sans aide")), seuil


def test_la_charge_de_travail_reste_realiste(facts):
    """§35 — jamais une heure par jour."""
    for semaine in facts["four_week_plan"]["weeks"]:
        for objectif in semaine["objectives"]:
            assert 10 <= objectif["duration_minutes"] <= 25, objectif
        assert len(semaine["objectives"]) <= 4


def test_deux_priorites_de_rang_un_au_maximum(client):
    """§49 — au-delà de deux, un plan de rentrée n'est pas tenu."""
    echec = ("A1", "A2", "A5", "A6", "C2")

    def override(scoring_id, maximum):
        ref = scoring_id.replace("4E_INES_KEFI_", "").split("_")[0]
        if ref in echec:
            return {"score_centi": 0, "error_codes": ["CONCEPT", "CALCUL"]}
        return {"score_centi": maximum, "error_codes": []}

    _remplir(client, database.session_scope, override)
    faits = _faits(database.session_scope)
    plan = faits["four_week_plan"]
    assert plan["p1_count"] <= plan_module.MAX_P1
    assert plan["p1_within_cap"] is True
    if plan["p1_downgraded_by_plan"]:
        for entree in plan["p1_downgraded_by_plan"]:
            assert entree["reason"]


def test_la_semaine_trois_mele_deux_competences(facts):
    """§33 — la semaine de transfert doit transférer."""
    semaine3 = next(w for w in facts["four_week_plan"]["weeks"] if w["week"] == 3)
    transferts = [o for o in semaine3["objectives"]
                  if "ensemble" in o["objective"] or o["kind"] == "transfer"]
    assert transferts, semaine3["objectives"]


# ================================================ 7. documents produits (§20, §38, §63)
def test_le_bilan_parents_ne_contient_aucun_jargon(facts):
    """§20, §63 — ni identifiant de compétence, ni de critère, ni clé technique."""
    blocs = narrative.parent_blocks(facts)
    texte = "\n".join(contenu for _, _, contenu in blocs)
    controle = guard.validate(texte, facts["skills"], "parents")
    assert controle["ok"], controle["violations"]


def test_le_controle_de_langue_attrape_ce_qu_il_doit_attraper():
    """Contre-épreuve : un contrôle qui ne refuse rien ne prouve rien."""
    cas = [
        ("La compétence M4E_REL_02 est en place.", "skill_id"),
        ("Le critère 4E_INES_KEFI_B2_c1 est réussi.", "criterion_id"),
        ("Progression de 35 % sur le stage.", "progression_chiffree"),
        ("Une lacune subsiste en géométrie.", "lacune"),
        ("Cette compétence est définitivement acquise.", "phrase_interdite"),
        ("Un suivi Nexus Réussite est indispensable.", "phrase_interdite"),
        ("Élève faible en calcul.", "phrase_interdite"),
        ("Le curriculum_scope est n_minus_1.", "cle_technique"),
    ]
    for texte, regle in cas:
        resultat = guard.validate(texte, None, "parents")
        assert not resultat["ok"], texte
        assert regle in [v["rule"] for v in resultat["violations"]], (texte, resultat)


def test_la_synthese_enseignant_a_le_droit_aux_identifiants():
    """Le document enseignant porte les clés techniques : il en a besoin."""
    resultat = guard.validate("Compétence M4E_REL_02, critère 4E_INES_KEFI_A5_c1.",
                              None, "enseignant")
    assert resultat["ok"]
    # mais pas aux progressions chiffrées
    assert not guard.validate("Progression de 35 %.", None, "enseignant")["ok"]


def test_la_fiche_eleve_est_simple_et_sans_jargon(facts):
    """§37 — langage simple, aucune clé technique."""
    blocs = narrative.student_blocks(facts)
    cles = [c for c, _, _ in blocs]
    assert cles == ["sais_faire", "a_consolider", "objectifs", "preuve"]
    texte = "\n".join(contenu for _, _, contenu in blocs)
    assert guard.validate(texte, None, "eleve")["ok"]


def test_le_document_parents_se_rend_et_passe_le_controle(facts):
    rendu = render.render_and_check(facts)
    assert rendu["validation"]["ok"], rendu["validation"]["violations"]
    assert "\\documentclass" in rendu["tex"]
    assert "BILAN INDIVIDUEL DE FIN DE STAGE" in rendu["tex"]
    # Cinq pages, dont la logique éditoriale est fixée par le gabarit : identité et
    # situation, trajectoire, domaines et évaluation, ce que l'évaluation établit,
    # plan de rentrée. Quatre sauts de page les séparent.
    assert rendu["tex"].count("\\newpage") == 4
    # les métadonnées du PDF sont renseignées, sans chemin local
    assert "pdftitle=" in rendu["tex"] and "pdfauthor={Nexus Réussite}" in rendu["tex"]
    assert "/home/" not in rendu["tex"]


def test_un_texte_refuse_n_est_jamais_compile(facts):
    """Le contrôle précède la compilation : un PDF fautif ne doit pas exister."""
    blocs = [("essentiel", "L'essentiel", "Progression de 35 % cette année."),
             ("conseil", "Conseil", "Une lacune persiste.")]
    resultat = render.compile_pdf(facts, "TEST_INES_REFUS", blocs)
    assert resultat["ok"] is False
    assert resultat["pdf_path"] is None
    assert resultat["validation"]["violations"]


# ============================================================ 8. provenance (§5, §42)
def test_chaque_fait_porte_sa_provenance_et_son_niveau(facts):
    assert facts["provenance"]
    niveaux = set()
    for fait in facts["provenance"]:
        assert fait["fact_id"].startswith("FACT_")
        assert fait["statement"]
        assert fait["source_type"]
        assert fait["evidence_level"] in evidence_levels.LEVELS
        niveaux.add(fait["evidence_level"])
    # les trois niveaux réellement disponibles dans ce corpus
    assert {"A", "C"} <= niveaux


def test_les_faits_sont_empreintes_et_stables(facts):
    from app.domain.longitudinal import facts as facts_module
    premier = facts_module.digest(facts)
    second = facts_module.digest(json.loads(json.dumps(facts, ensure_ascii=False)))
    assert premier == second == facts["facts_sha256"]


# ============================================================ 9. péremption (§60)
def test_une_correction_rouverte_rend_le_bilan_perime(client):
    """§60 — un bilan produit sur une révision antérieure n'est plus actuel."""
    _remplir(client, database.session_scope, _tout_reussi_sauf_passerelles)
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(s, assessment.assessment_id)
        service = LongitudinalReportService(s)
        service.build_longitudinal_facts(assessment, courante, persist=True)
        etat = service.is_stale(courante)
        assert etat["stale"] is False

    reponse = client.post("/eleve/%s/rouvrir" % STUDENT,
                          json={"reason": "TEST_INES — vérification de la péremption"},
                          follow_redirects=False)
    assert reponse.status_code in (200, 303)

    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(s, assessment.assessment_id)
        etat = LongitudinalReportService(s).is_stale(courante)
        assert etat["stale"] is True
        assert "rouverte" in etat["reason"]


# ================================================== 10. anti-copier-coller (§51, §52)
def test_le_bilan_est_reellement_personnalise(facts):
    """§51 — le document cite le parcours propre de cet élève.

    On vérifie la présence des objectifs de séance écrits dans SON dossier : ce
    sont eux qui distinguent deux élèves d'un même niveau, pas le prénom.
    """
    contexte = render.build_context(facts)
    focus = [s["personal_focus"] for s in contexte["sessions"] if s["personal_focus"]]
    assert len(focus) == 5
    assert len(set(focus)) == 5, "cinq objectifs distincts, un par séance"
    tex = render.render_tex(facts)
    for objectif in focus:
        fragment = objectif.split(",")[0].split(";")[0].strip().rstrip(".")
        assert fragment[:24] in tex, fragment


def test_deux_scenarios_differents_donnent_des_bilans_differents(client, facts):
    """§52 — les sections personnalisées doivent diverger d'un dossier à l'autre.

    Les paragraphes institutionnels peuvent légitimement se ressembler ; la
    situation, les points forts, les priorités et le plan, non.
    """
    reference = {cle: contenu for cle, _, contenu in narrative.parent_blocks(facts)}

    echec = ("A1", "A2", "A5", "A6", "B4", "C2")

    def override(scoring_id, maximum):
        ref = scoring_id.replace("4E_INES_KEFI_", "").split("_")[0]
        if ref in echec:
            return {"score_centi": 0, "error_codes": ["CONCEPT", "METHODE"]}
        return {"score_centi": maximum, "error_codes": []}

    _remplir(client, database.session_scope, override)
    autre = {cle: contenu for cle, _, contenu in
             narrative.parent_blocks(_faits(database.session_scope))}

    personnalisees = ("essentiel", "score_brut", "consolidation")
    for cle in personnalisees:
        assert reference.get(cle) != autre.get(cle), \
            "la section « %s » ne varie pas d'un dossier à l'autre" % cle

    # à l'inverse, le cadre institutionnel a le droit d'être stable
    assert reference["objectifs_stage"] == autre["objectifs_stage"]


# ============================================== 11. lecture du dossier individuel
def test_les_tableaux_de_suivi_vierges_ne_produisent_aucune_observation():
    """§15 — ne pas inventer une observation là où le formulaire est vide."""
    texte = (
        "## Parcours personnalisé séance par séance\n"
        "| 1 | Calculer avec du sens | Fractions équivalentes. |  |  |\n"
        "## Suivi des cinq séances\n"
        "### Séance 1 - Calculer avec du sens\n"
        "**Objectif personnel :** Fractions équivalentes.\n"
        "| Observation | Initial | Fin de séance | Commentaire |\n"
        "| Procédure choisie |  |  |  |\n"
        "| Exactitude |  |  |  |\n")
    lecture = dossier.parse(texte)
    assert lecture["sessions"]["S1"]["personal_focus"] == "Fractions équivalentes."
    assert lecture["sessions"]["S1"]["observations_available"] is False
    assert lecture["observations_available_anywhere"] is False


def test_un_tableau_renseigne_est_bien_detecte():
    """Contre-épreuve : la détection ne renvoie pas systématiquement False."""
    texte = (
        "## Suivi des cinq séances\n"
        "### Séance 2 - Mesurer\n"
        "| Observation | Initial | Fin de séance | Commentaire |\n"
        "| Exactitude | partielle | complète | net progrès |\n")
    lecture = dossier.parse(texte)
    assert lecture["sessions"]["S2"]["observations_available"] is True
    assert lecture["observations_available_anywhere"] is True


def test_un_dossier_illisible_ne_fait_pas_echouer_le_pipeline():
    lecture = dossier.read("/chemin/qui/n/existe/pas.md")
    assert lecture["unreadable"] is True
    assert lecture["sessions"] == {}


# ============================================== 12. immutabilité et périmètre (§57)
def test_le_pipeline_ne_touche_aucun_document_distribue(immutability_before):
    from app.domain import immutability
    apres = immutability.verify()
    assert apres.ok
    assert len(apres.changed) == 0
    assert len(apres.missing) == 0
    assert apres.total == immutability_before.total == 60


def test_aucune_donnee_reelle_n_est_saisie(facts):
    """§14 — toutes les valeurs employées sont synthétiques."""
    assert facts["final_assessment"]["correction_status"] in (
        "VALIDATED", "REPORT_READY", "REPORT_APPROVED")
    observations = facts["final_assessment"]["observations"]
    assert observations["per_criterion"] == []
    assert observations["general"] in ({}, None)
