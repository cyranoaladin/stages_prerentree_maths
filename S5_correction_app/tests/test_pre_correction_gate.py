# -*- coding: utf-8 -*-
"""Neutralité de l'état initial, avant la première correction réelle.

La propriété que ce module protège tient en une phrase : **avant qu'un enseignant
saisisse la première réponse, le système ne doit rien prétendre sur l'élève qu'il
ne puisse prouver.**

La distinction qui structure tous ces tests est celle entre quatre natures
d'information, que l'interface ne doit jamais confondre :

* le **barème** mis à disposition du correcteur ;
* les **erreurs fréquentes** proposées comme aide à la saisie ;
* les **données historiques sourcées**, antérieures à l'évaluation ;
* les **données de la correction en cours**, qui n'existent pas encore.

Aucune donnée réelle n'est saisie ici : les tests travaillent sur une base jetable
et n'écrivent jamais dans le runtime de l'enseignant.
"""

import json
import re

import pytest

from app import database
from app.domain import correction as corr
from app.models import Assessment, CriterionDefinition

STUDENT = "ines-kefi"
TEST_LABEL = "TEST_INES"

# Sept critères d'Inès portent un contrôle différé, dans deux contextes distincts
# qu'il ne faut pas confondre.
CONTEXTES_ATTENDUS = {
    "4E_INES_KEFI_A2_c1": "immediate_after_remediation",
    "4E_INES_KEFI_A5_c1": "immediate_after_remediation",
    "4E_INES_KEFI_A6_c1": "immediate_after_remediation",
    "4E_INES_KEFI_B3_c2": "first_worked_in_session_5",
    "4E_INES_KEFI_B3_c3": "first_worked_in_session_5",
    "4E_INES_KEFI_C1_c2": "immediate_after_remediation",
    "4E_INES_KEFI_C2_c1": "immediate_after_remediation",
}


@pytest.fixture(scope="module")
def page_initiale(client):
    """La page de correction, telle qu'elle s'affiche avant toute saisie."""
    return client.get("/eleve/%s" % STUDENT).text


# ============================== 1. aucune affirmation de résultat avant saisie
def test_la_copie_est_bien_vierge(client, page_initiale):
    """Préalable : sans cela, les tests suivants ne prouveraient rien."""
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(session, assessment.assessment_id)
        assert courante is not None
        assert courante.status == "DRAFT"
        assert all(r.score_centi is None for r in courante.responses)
        assert all(r.scoring_status == "PENDING" for r in courante.responses)
        assert all(not (r.observation or "").strip() for r in courante.responses)


def test_aucune_reussite_n_est_affirmee_avant_la_moindre_saisie(page_initiale):
    """Le défaut que ce module existe pour empêcher.

    « Réussite immédiate après remédiation » est une affirmation de performance.
    Elle ne peut pas figurer sur une page où rien n'est encore corrigé — et
    surtout pas déduite de la seule existence d'une remédiation au programme.
    """
    # Recherche à frontières de mots : « la réussite s'appuie sur… » est une
    # limite d'interprétation légitime, qui dit comment lire un résultat futur ;
    # elle contient « a réussi » sans rien affirmer.
    interdits = (r"[Rr]éussite immédiate", r"\ba réussi\b", r"\bréussite obtenue\b",
                 r"\bl'élève a (?:réussi|obtenu|montré)\b")
    for motif in interdits:
        trouve = re.search(motif, page_initiale)
        assert trouve is None, (motif, page_initiale[max(0, trouve.start() - 90):
                                                     trouve.end() + 40] if trouve else "")


def test_aucune_remediation_n_est_affirmee_pour_une_notion_decouverte(page_initiale):
    """Deux critères d'Inès portent sur une notion *découverte* en séance 5.

    Aucune remédiation n'a eu lieu pour eux : l'écrire serait faux, pas seulement
    prématuré.
    """
    decouvertes = [cid for cid, ctx in CONTEXTES_ATTENDUS.items()
                   if ctx == "first_worked_in_session_5"]
    assert decouvertes, "le corpus d'Inès comporte des notions découvertes en S5"
    for criterion_id in decouvertes:
        bloc = _bloc_du_critere(page_initiale, criterion_id)
        assert "remédiation" not in bloc.lower(), criterion_id


def test_le_contexte_de_passation_reste_affiche_et_sourcé(page_initiale):
    """La donnée est légitime : on ne la supprime pas, on l'énonce correctement.

    Le correcteur doit savoir que la notion a été travaillée juste avant, pour
    lire son propre score avec la prudence voulue.
    """
    for criterion_id in CONTEXTES_ATTENDUS:
        bloc = _bloc_du_critere(page_initiale, criterion_id)
        assert "séance 5" in bloc or "mini-test" in bloc, criterion_id
        # la conséquence est énoncée au conditionnel, jamais au passé composé
        assert "devra être" in bloc or "à revérifier" in bloc, criterion_id


def _bloc_du_critere(page, criterion_id):
    """Extrait le fragment de page correspondant à un critère."""
    ancre = 'data-scoring-id="%s"' % criterion_id
    debut = page.find(ancre)
    assert debut != -1, criterion_id
    suite = page.find('data-scoring-id="', debut + len(ancre))
    return page[debut:suite if suite != -1 else len(page)]


# =========================== 2. aucune fuite de résultat dans l'état initial
def test_aucun_score_n_est_prerempli(page_initiale):
    """Un bouton de score sélectionné avant toute saisie induirait le correcteur.

    Le marquage ARIA « aria-checked="false" » est au contraire attendu, et
    présent sur chaque bouton : c'est ce qui rend l'état lisible par un lecteur
    d'écran. Seul « true » signalerait une sélection.
    """
    assert 'class="score-btn' in page_initiale, "les boutons de score sont présents"
    assert "score-btn btn-sm  selected" not in page_initiale
    assert 'aria-checked="true"' not in page_initiale
    assert "is-current" not in page_initiale
    # tous les critères sont dans l'état « à renseigner »
    assert 'class="criterion done' not in page_initiale
    assert page_initiale.count('class="criterion pending') == 23


def test_aucun_code_d_erreur_n_est_preselectionne(page_initiale):
    """Les suggestions sont une aide à la saisie, pas un constat."""
    assert "is-selected" not in page_initiale
    assert 'aria-checked="true"' not in page_initiale


def test_aucune_observation_generale_n_est_prerenseignee(client):
    """§13 — les rubriques d'observation restent vides tant que rien n'est saisi."""
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(session, assessment.assessment_id)
        brut = courante.general_observations_json
        assert brut in (None, "", "{}"), brut
        assert courante.observed_duration_minutes is None


def test_aucun_diagnostic_courant_n_est_produit_avant_validation(client):
    """L'analyse ne doit rien conclure sur une copie vierge."""
    reponse = client.get("/eleve/%s/bilan-longitudinal/faits" % STUDENT)
    assert reponse.status_code == 409, reponse.status_code
    assert "validée" in reponse.json()["detail"]


def test_le_pourcentage_de_progression_est_nul(page_initiale):
    assert "0 / 23 lignes analytiques" in page_initiale
    assert "— 0 %" in page_initiale


def test_la_validation_est_bloquee_sur_une_copie_vierge(client):
    refus = client.post("/eleve/%s/valider" % STUDENT)
    assert refus.status_code == 400
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
        assert corr.current_correction(
            session, assessment.assessment_id).status == "DRAFT"


# ============================ 3. les quatre natures d'information sont séparées
def test_le_barème_est_present_sans_valoir_constat(page_initiale):
    """Le barème s'affiche — c'est son rôle — mais sous un intitulé de règle."""
    assert "Règle d'attribution" in page_initiale or "rubric" in page_initiale.lower()


def test_les_erreurs_frequentes_sont_annoncees_comme_des_suggestions(page_initiale):
    for marqueur in ("suggestion", "Erreurs fréquentes", "propres à ce critère"):
        if marqueur.lower() in page_initiale.lower():
            break
    else:
        pytest.fail("les erreurs proposées ne sont pas annoncées comme telles")


def test_les_donnees_historiques_sont_datees_ou_situees(page_initiale):
    """Une donnée antérieure doit être reconnaissable comme antérieure."""
    for criterion_id, contexte in CONTEXTES_ATTENDUS.items():
        bloc = _bloc_du_critere(page_initiale, criterion_id)
        assert "séance 5" in bloc, (criterion_id, contexte)


# ======================================= 4. contexte de passation, par nature
def test_les_deux_contextes_de_passation_sont_distingues():
    """Le drapeau booléen recouvre deux situations pédagogiques différentes."""
    notice_remediation = corr.retention_notice(
        {"recommended_delayed_check": True,
         "post_test_context": "immediate_after_remediation",
         "reason": "motif documenté"})
    notice_decouverte = corr.retention_notice(
        {"recommended_delayed_check": True,
         "post_test_context": "first_worked_in_session_5",
         "reason": "motif documenté"})
    assert notice_remediation and notice_decouverte
    assert notice_remediation["title"] != notice_decouverte["title"]
    assert "retravaillée" in notice_remediation["title"]
    assert "découverte" in notice_decouverte["title"]
    assert "remédiation" not in notice_decouverte["text"].lower()
    assert "remédiation" not in notice_decouverte["title"].lower()


def test_aucune_notice_sans_controle_differe():
    assert corr.retention_notice(None) is None
    assert corr.retention_notice({}) is None
    assert corr.retention_notice({"recommended_delayed_check": False}) is None


def test_un_contexte_inconnu_ne_produit_aucune_affirmation():
    """Face à un contexte non prévu, on décrit sans inventer de cause."""
    notice = corr.retention_notice(
        {"recommended_delayed_check": True, "post_test_context": "inconnu_xyz"})
    assert notice is not None
    assert "remédiation" not in notice["title"].lower()
    assert "réussite" not in notice["text"].lower()


def test_la_notice_conserve_le_motif_de_la_source():
    """La provenance reste inspectable : on ne perd pas le motif documenté."""
    notice = corr.retention_notice(
        {"recommended_delayed_check": True,
         "post_test_context": "immediate_after_remediation",
         "reason": "compétence retravaillée en phase 2 ou 3 de la séance"})
    assert notice["source"] == "compétence retravaillée en phase 2 ou 3 de la séance"
    assert notice["context"] == "immediate_after_remediation"


# ======================== 5. le moteur d'analyse ne parle plus de remédiation
def test_les_libelles_d_analyse_ne_supposent_plus_une_remediation():
    """Dix élèves sur quinze ont des notions découvertes en S5, jamais remédiées."""
    from app.domain import analysis
    # La lecture du statut, et non son étiquette courte, portait l'affirmation.
    lecture = analysis.N1_READING["A_CONFIRMER"].lower()
    assert "remédiation" not in lecture, lecture
    assert "travail sur la notion" in lecture, lecture
    assert "remédiation" not in analysis.N1_LABELS["A_CONFIRMER"].lower()


def test_aucune_contamination_sur_les_quinze_dossiers(session):
    """Le contexte de passation est renseigné partout où un contrôle est demandé."""
    contextes = set()
    manquants = []
    lignes = session.query(CriterionDefinition).all()
    for ligne in lignes:
        if not ligne.retention_json:
            continue
        retention = json.loads(ligne.retention_json)
        if not retention.get("recommended_delayed_check"):
            continue
        contexte = retention.get("post_test_context")
        if not contexte:
            manquants.append(ligne.criterion_id)
        else:
            contextes.add(contexte)
    assert manquants == [], manquants
    assert contextes <= {"immediate_after_remediation", "first_worked_in_session_5"}, \
        contextes


# ============================================ 6. sémantique des passerelles (§6)
CLASSEMENT_ATTENDU = {
    "4E_INES_KEFI_A3_c1_v1": "n_minus_1",     # regroupement des termes en x
    "4E_INES_KEFI_A3_c1_v2": "bridge_n",      # écriture réduite complète
    "4E_INES_KEFI_B2_c1": "bridge_n",         # développement 5(x−3)
    "4E_INES_KEFI_B2_c2": "bridge_n",         # réduction de l'expression obtenue
    "4E_INES_KEFI_B2_c3": "n_minus_1",        # contrôle par substitution
    "4E_INES_KEFI_C2_c1": "n_minus_1",        # déplacements et somme de relatifs
    "4E_INES_KEFI_C2_c2": "bridge_n",         # produit de deux relatifs
}


def test_le_classement_curriculaire_est_celui_de_la_doctrine(session):
    """§6 — A3, B2 et C2, critère par critère."""
    from app.models import VirtualCriterionDefinition
    for identifiant, attendu in CLASSEMENT_ATTENDU.items():
        ligne = (session.query(CriterionDefinition)
                 .filter_by(criterion_id=identifiant).one_or_none()
                 or session.query(VirtualCriterionDefinition)
                 .filter_by(virtual_criterion_id=identifiant).one())
        assert ligne.curriculum_scope == attendu, identifiant


def test_une_classification_incertaine_le_reste(session):
    """§9 — B2_c2 est classé avec une certitude moyenne ; elle ne doit pas être
    silencieusement promue en certitude haute pour simplifier le système."""
    ligne = session.query(CriterionDefinition).filter_by(
        criterion_id="4E_INES_KEFI_B2_c2").one()
    assert ligne.scope_certainty == "moyenne"
    assert ligne.scope_rationale and len(ligne.scope_rationale) > 60
    assert ligne.official_source


def test_aucune_passerelle_ne_parle_de_lacune_de_cinquieme(session):
    """§6 — une non-réussite en passerelle n'est jamais un déficit N−1."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    for item in assessment.items:
        for critere in item.criteria:
            if critere.curriculum_scope != "bridge_n":
                continue
            textes = [critere.description or "", critere.neutral_label or "",
                      critere.scope_rationale or ""]
            textes += json.loads(critere.interpretation_limits_json or "[]")
            for texte in textes:
                minuscule = texte.lower()
                for interdit in ("lacune", "déficit", "non acquis de cinquième"):
                    assert interdit not in minuscule, (critere.criterion_id, interdit)


def test_les_passerelles_portent_une_limite_protegeant_le_diagnostic(session):
    """Les passerelles dont l'échec pourrait être lu comme une fragilité N−1
    portent explicitement la mise en garde."""
    for identifiant in ("4E_INES_KEFI_B2_c1", "4E_INES_KEFI_C2_c2"):
        ligne = session.query(CriterionDefinition).filter_by(
            criterion_id=identifiant).one()
        limites = json.loads(ligne.interpretation_limits_json or "[]")
        assert limites, identifiant
        assert any("ne documente aucune fragilité" in m for m in limites), identifiant


# ==================================== 7. absence de double sanction (§7)
def test_la_regle_anti_double_sanction_existe_sur_la_chaine_b2(session):
    """La réduction s'apprécie sur l'expression que l'élève a obtenue."""
    ligne = session.query(CriterionDefinition).filter_by(
        criterion_id="4E_INES_KEFI_B2_c2").one()
    regles = json.loads(ligne.fairness_rules_json or "[]")
    assert regles, "B2_c2 doit porter une règle d'équité"
    assert any("effectivement obtenue" in r and "deux fois" in r for r in regles), regles


def test_la_regle_anti_double_sanction_est_visible_au_moment_de_noter(page_initiale):
    """Le défaut corrigé : la règle vivait dans le corrigé replié.

    La rubrique de notation est ouverte par défaut ; une règle qui modifie son
    application doit se lire au même endroit, sinon elle n'est pas lue.
    """
    bloc = _bloc_du_critere(page_initiale, "4E_INES_KEFI_B2_c2")
    position_regle = bloc.find("fairness-rules")
    position_corrige = bloc.find("Afficher le corrigé")
    assert position_regle != -1, "la règle d'équité n'apparaît pas"
    assert position_corrige == -1 or position_regle < position_corrige, \
        "la règle d'équité est enfouie dans le corrigé replié"
    assert "sanctionnée deux fois" in bloc


def test_un_code_d_erreur_ne_se_propage_pas_aux_criteres_suivants(session):
    """La politique de correction l'énonce ; le modèle le rend possible.

    Chaque ligne porte ses propres codes : rien dans le schéma ne propage un code
    d'un critère à un autre.
    """
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    courante = corr.current_correction(session, assessment.assessment_id)
    for reponse in courante.responses:
        assert json.loads(reponse.error_codes_json or "[]") == []


# ============================================== 8. modèle de notation (§8)
def test_chaque_item_se_recompose_exactement(session):
    from app.models import VirtualCriterionDefinition          # noqa: F401
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    total = 0
    for item in assessment.items:
        somme = 0
        for critere in item.criteria:
            if critere.curriculum_scope == "mixed":
                parts = list(critere.virtual_parts)
                assert sum(p.max_score_centi for p in parts) == critere.max_score_centi
                somme += critere.max_score_centi
            else:
                somme += critere.max_score_centi
        assert somme == item.max_points_centi, item.ref
        total += somme
    assert total == assessment.max_points_centi == 2000


def test_les_scores_autorises_sont_exacts_sans_flottant(session):
    """Les barèmes contiennent 0,3 et 0,7 : les quarts n'y sont pas représentables."""
    from app.domain import points
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    for ligne in corr.scoring_rows(assessment):
        autorises = points.allowed_scores(ligne["max_score_centi"])
        assert all(isinstance(v, int) for v in autorises), ligne["scoring_id"]
        assert autorises[0] == 0
        assert autorises[-1] == ligne["max_score_centi"]
        for valeur in autorises:
            assert points.is_acceptable(valeur, ligne["max_score_centi"])


def test_les_maxima_particuliers_du_sujet_sont_bien_presents(session):
    """0,3 · 0,5 · 0,7 · 1 · 1,5 — si l'un disparaît, un barème a été altéré."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    maxima = {r["max_score_centi"] for r in corr.scoring_rows(assessment)}
    assert {30, 50, 70, 100, 150} <= maxima, sorted(maxima)


# ============================================ 12. validation et facultatifs
def test_la_validation_n_exige_aucun_champ_facultatif(client):
    """§12 — observations, durée et certitude ne conditionnent pas la validation."""
    from app.domain import validation
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
        courante = corr.current_correction(session, assessment.assessment_id)
        problemes = validation.validate(session, courante, assessment)
    codes = {p.code for p in problemes}
    assert codes == {"non_saisi"}, codes
    assert len(problemes) == 23
    for interdit in ("observation", "duree", "certitude", "general"):
        assert not any(interdit in p.code for p in problemes), interdit


# ================================== 13. observations générales (§13)
def test_aucune_rubrique_d_observation_n_est_preselectionnee(page_initiale):
    """Aucune valeur par défaut autre que « non renseigné »."""
    zone = page_initiale[page_initiale.find('id="observations-generales"'):]
    assert zone, "le panneau d'observations générales est présent"
    assert "selected" not in zone.split("</div>")[0].lower() or \
        'value="" selected' in zone or "selected>" not in zone


def test_les_observations_generales_n_influencent_aucun_point(session):
    """Elles nourrissent le bilan, jamais le score."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    courante = corr.current_correction(session, assessment.assessment_id)
    avant = corr.raw_total_centi(courante)
    courante.general_observations_json = json.dumps(
        {"autonomie": "TEST_INES", "methode": "TEST_INES"}, ensure_ascii=False)
    session.flush()
    assert corr.raw_total_centi(courante) == avant == 0
    courante.general_observations_json = None      # on ne laisse aucune trace
    session.flush()
