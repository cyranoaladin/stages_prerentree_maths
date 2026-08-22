# -*- coding: utf-8 -*-
"""Micro-passe finale avant la saisie de la première copie réelle d'Inès KEFI.

Quatre objets, et rien d'autre :

1. le rendu des structures LaTeX documentaires (enumerate, item, textbf) ;
2. la distinction entre les 22 critères du sujet et les 23 lignes analytiques ;
3. l'unicité de la limite d'interprétation de C2 ;
4. l'isolation analytique entre deux critères qui partagent un skill_id
   historique mais relèvent de périmètres curriculaires différents.

Aucun score réel n'est saisi ici. Toutes les valeurs employées sont des fixtures
synthétiques, dans une base jetable créée par conftest.
"""

import html as html_mod
import json
import re

import pytest

from app import database
from app.data import criterion_overlays
from app.domain import analysis as ana
from app.domain import correction as corr
from app.latex_html import (STRUCTURES_AVEC_REPLI, STRUCTURES_PRISES_EN_CHARGE,
                            render_statement, unsupported_structures)
from app.models import Assessment, CriterionDefinition
from conftest import fill

STUDENT = "ines-kefi"
TEST_LABEL = "TEST_INES"

# Les quatre items dont l'énoncé est structuré par un environnement enumerate.
ITEMS_STRUCTURES = ("4E_INES_KEFI_B2", "4E_INES_KEFI_B3",
                    "4E_INES_KEFI_C1", "4E_INES_KEFI_C2")

SEQUENCES_INTERDITES = ("\\begin{enumerate}", "\\end{enumerate}", "\\item")


# ==================================================================== 1. renderer
# ---------------------------------------------------------------------- TEST A
def test_a_enumerate_produit_une_liste_ordonnee():
    rendu = render_statement(
        "\\begin{enumerate}\n\\item Premier.\n\\item Deuxième.\n\\item Troisième.\n"
        "\\end{enumerate}")
    assert rendu.count("<ol") == 1
    assert rendu.count("</ol>") == 1
    assert rendu.count("<li>") == 3
    assert rendu.count("</li>") == 3
    for attendu in ("Premier.", "Deuxième.", "Troisième."):
        assert "<li>%s</li>" % attendu in rendu


def test_a2_la_prose_precedant_la_liste_est_conservee():
    rendu = render_statement(
        "Une terrasse mesure $12$ m.\n\\begin{enumerate}\n\\item Calculer l'aire.\n"
        "\\end{enumerate}")
    assert "<p>Une terrasse mesure $12$ m.</p>" in rendu
    assert rendu.index("<p>") < rendu.index("<ol")


def test_a3_un_item_sur_plusieurs_lignes_reste_un_seul_item():
    """En LaTeX un simple passage à la ligne vaut une espace, pas un nouvel item."""
    rendu = render_statement(
        "\\begin{enumerate}\n\\item Première phrase.\nSeconde phrase du même item.\n"
        "\\end{enumerate}")
    assert rendu.count("<li>") == 1
    assert "Première phrase. Seconde phrase du même item." in rendu


def test_a4_itemize_n_est_pas_pris_en_charge_car_absent_du_corpus():
    """Décision explicite : le corpus ne contient aucun itemize (§4.1).

    Si un énoncé venait à en introduire un, ce test échouerait en même temps que
    l'affichage se dégraderait — ce qui est le comportement recherché.
    """
    assert "itemize" not in STRUCTURES_PRISES_EN_CHARGE
    rendu = render_statement("\\begin{itemize}\n\\item Un.\n\\end{itemize}")
    assert "<ul>" not in rendu          # non converti, donc non silencieusement cassé


# ------------------------------------------------------------------- \textbf
def test_a5_textbf_hors_math_devient_strong():
    rendu = render_statement("\\textbf{L'atelier de peinture.} Un mur mesure $6$ m.")
    assert "<strong>L'atelier de peinture.</strong>" in rendu
    assert "\\textbf" not in rendu


def test_a6_textbf_a_l_interieur_des_maths_reste_intact():
    """Dans un segment mathématique, la commande appartient à KaTeX."""
    rendu = render_statement("Comparer $\\textbf{x}$ et $y$.")
    assert "$\\textbf{x}$" in rendu
    assert "<strong>" not in rendu


# ------------------------------------------------------------------ sécurité
def test_a7_aucune_balise_arbitraire_ne_survit_au_renderer():
    """Le texte est échappé AVANT insertion : seules les balises du module passent."""
    rendu = str(render_statement(
        "<script>alert(1)</script> et <b>gras</b> et <img src=x onerror=y>"))
    assert "<script>" not in rendu
    assert "<b>" not in rendu
    assert "<img" not in rendu
    assert "&lt;script&gt;" in rendu
    assert "&lt;b&gt;" in rendu


def test_a8_une_balise_dans_un_item_est_echappee_mais_l_item_reste_une_liste():
    rendu = str(render_statement(
        "\\begin{enumerate}\n\\item <script>alert(1)</script>\n\\end{enumerate}"))
    assert "<li>" in rendu
    assert "<script>" not in rendu
    assert "&lt;script&gt;" in rendu


def test_a9_les_structures_du_corpus_sont_toutes_couvertes():
    """Suite à la mise en service, lstlisting et tabularx sont pris en charge.

    Ce test remplace celui qui figeait leur mise hors périmètre : la décision a
    été renversée pour rendre l'application utilisable en NSI. Les énoncés d'Inès
    n'en contiennent toujours aucun ; ce qui compte ici est qu'aucune structure du
    corpus ne reste sans traitement ni repli.
    """
    for structure in ("enumerate", "lstlisting", "tabularx"):
        assert structure in STRUCTURES_PRISES_EN_CHARGE
    assert "tabularx" in STRUCTURES_AVEC_REPLI
    # aucun énoncé d'Inès ne déclenche de repli
    assert unsupported_structures(
        "\\begin{enumerate}\\item Développer $5(x-3)$.\\end{enumerate}") == []


# ---------------------------------------------------------------------- TEST E
def test_e_aucune_regression_sur_les_expressions_inline():
    """Les fragments mathématiques traversent le renderer sans altération."""
    for expression in ("$(-8)+3-(-5)$", "$5(x-3)$", "$\\dfrac{3}{4}$",
                       "$(-4)\\times(-7)$", "$1{,}5$", "$53^\\circ$"):
        assert expression in str(render_statement("Calculer %s." % expression))


# ============================================== 2. page réelle d'Inès (TEST B/C)
@pytest.fixture(scope="module")
def page(client):
    return client.get("/eleve/%s" % STUDENT).text


def test_b_aucune_sequence_latex_structurelle_dans_le_html_final(page):
    """TEST B — plus aucune séquence brute sur la page d'Inès."""
    for sequence in SEQUENCES_INTERDITES:
        assert sequence not in page, "séquence %r encore présente" % sequence


def test_b2_les_quatre_items_structures_rendent_une_liste_ordonnee(page):
    for item_id in ITEMS_STRUCTURES:
        ancre = 'id="item-%s"' % item_id.replace("4E_INES_KEFI_", "")
        # On délimite la carte de l'item pour ne pas confondre avec une autre.
        debut = page.find(ancre)
        assert debut != -1, "item %s introuvable dans la page" % item_id
        fin = page.find('class="item-card"', debut + 1)
        carte = page[debut:fin if fin != -1 else len(page)]
        assert '<ol class="enonce-liste">' in carte, "%s sans liste" % item_id
        assert carte.count("<li>") >= 2


def test_b3_b2_affiche_exactement_ses_trois_questions(page):
    debut = page.find('id="item-B2"')
    fin = page.find('class="item-card"', debut + 1)
    carte = page[debut:fin]
    liste = carte[carte.index('<ol class="enonce-liste">'):carte.index("</ol>")]
    assert liste.count("<li>") == 3
    assert "Développer" in liste
    assert "Réduire ensuite" in liste
    assert "Contrôler" in liste


def test_c_les_maths_restent_disponibles_pour_katex_dans_les_li(page):
    """TEST C — les délimiteurs mathématiques survivent à la mise en liste."""
    debut = page.find('id="item-B2"')
    carte = page[debut:page.find('class="item-card"', debut + 1)]
    liste = carte[carte.index('<ol class="enonce-liste">'):carte.index("</ol>")]
    assert "$5(x - 3)$" in liste
    assert "$x = 2$" in liste
    # le conteneur porte toujours la classe que le moteur cible
    assert 'class="item-statement math"' in carte


def test_c2_katex_reste_local_et_sans_appel_reseau(page):
    """Aucune ressource n'est chargée depuis un hôte distant."""
    assert "/static/vendor/katex/" in page
    # On inspecte les URL réellement chargées, pas le texte de la page : celle-ci
    # contient un commentaire qui mentionne légitimement le mot « cdn ».
    for attribut, valeur in re.findall(r'\b(src|href)\s*=\s*"([^"]*)"', page):
        assert not valeur.startswith(("http://", "https://", "//")), (attribut, valeur)


# ---------------------------------------------------------------------- TEST D
def test_d_une_observation_utilisateur_n_est_jamais_rendue_en_html(client):
    """TEST D — la saisie enseignant reste du texte échappé, jamais du HTML actif."""
    poison = "\\begin{enumerate}\\item x\\end{enumerate} <script>alert(1)</script> <b>gras</b>"
    scoring_id = "4E_INES_KEFI_A1_c1"
    reponse = client.post("/eleve/%s/critere/%s" % (STUDENT, scoring_id),
                          json={"score_centi": 100, "error_codes": [],
                                "observation": poison})
    assert reponse.status_code == 200

    page = client.get("/eleve/%s" % STUDENT).text
    # Aucune balise active n'a été introduite par la saisie.
    assert "<script>alert(1)</script>" not in page
    assert "<b>gras</b>" not in page
    # Le texte est bien présent, mais échappé.
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
    assert "&lt;b&gt;gras&lt;/b&gt;" in page
    # Le LaTeX saisi par l'enseignant n'est pas transformé en liste : il n'est pas
    # du contenu de référentiel et ne passe donc pas par le renderer structurel.
    #
    # L'assertion précédente se terminait par « or True » : elle ne pouvait pas
    # échouer, et ne vérifiait donc rien. On délimite réellement le champ de saisie
    # qui porte l'observation, et on regarde ce qu'il contient.
    assert "\\begin{enumerate}" in page          # conservé comme texte
    ancre = page.find(html_mod.escape("\\begin{enumerate}"))
    assert ancre != -1, "l'observation saisie doit figurer dans la page"
    ouverture = page.rfind("<textarea", 0, ancre)
    fermeture = page.find("</textarea>", ancre)
    assert ouverture != -1 and fermeture != -1, \
        "l'observation doit être rendue dans un champ de saisie, pas en HTML libre"
    champ = page[ouverture:fermeture]
    assert '<ol class="enonce-liste">' not in champ, \
        "la saisie enseignant ne doit jamais passer par le renderer structurel"
    assert "<script" not in champ and "<b>" not in champ

    # On remet la ligne à son état non renseigné pour ne pas influencer la suite.
    client.post("/eleve/%s/critere/%s" % (STUDENT, scoring_id),
                json={"score_centi": None, "error_codes": [], "observation": "",
                      "scoring_status": "PENDING"})


# ================================================= 3. sémantique 22 / 23 (§6-§7)
def test_22_criteres_originaux_et_23_lignes_analytiques(session):
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    criteres = [c for item in assessment.items for c in item.criteria]
    lignes = corr.scoring_rows(assessment)

    original_criteria_count = len(criteres)
    analytic_scoring_line_count = len(lignes)

    assert original_criteria_count == 22
    assert analytic_scoring_line_count == 23
    # Une seule ligne de plus que de critères : celle du seul critère mixte.
    mixtes = [c for c in criteres if c.curriculum_scope == "mixed"]
    assert len(mixtes) == 1
    assert analytic_scoring_line_count - original_criteria_count == \
        sum(len(c.virtual_parts) - 1 for c in mixtes)


def test_la_somme_des_points_analytiques_reste_vingt(session):
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    lignes = corr.scoring_rows(assessment)
    assert sum(r["max_score_centi"] for r in lignes) == 2000
    assert assessment.max_points_centi == 2000


def test_les_sous_criteres_de_a3_totalisent_exactement_le_critere_imprime(session):
    a3 = session.query(CriterionDefinition).filter_by(
        criterion_id="4E_INES_KEFI_A3_c1").one()
    assert a3.curriculum_scope == "mixed"
    assert a3.max_score_centi == 100
    parts = list(a3.virtual_parts)
    assert len(parts) == 2
    assert sum(p.max_score_centi for p in parts) == a3.max_score_centi == 100
    # un sous-critère de chaque périmètre, sans duplication de points
    assert sorted(p.curriculum_scope for p in parts) == ["bridge_n", "n_minus_1"]
    assert len({p.virtual_criterion_id for p in parts}) == 2


def test_aucune_duplication_de_score_entre_critere_mixte_et_sous_criteres(session):
    """Le critère mixte lui-même ne doit jamais être noté en plus de ses parties."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    ids = [r["scoring_id"] for r in corr.scoring_rows(assessment)]
    assert len(ids) == len(set(ids))
    assert "4E_INES_KEFI_A3_c1" not in ids          # le parent n'est pas noté
    assert "4E_INES_KEFI_A3_c1_v1" in ids
    assert "4E_INES_KEFI_A3_c1_v2" in ids


def test_les_deux_comptes_sont_distingues_dans_l_interface(page):
    """L'en-tête ne doit plus laisser croire que le sujet comportait 23 critères."""
    assert "22 critères du sujet" in page
    assert "lignes analytiques renseignées" in page
    assert "23 critères" not in page


def test_le_progres_expose_les_deux_comptes(session):
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    correction = corr.get_or_create_correction(session, assessment)
    session.flush()
    avancement = corr.progress(correction)
    assert avancement["original_criteria"] == 22
    assert avancement["total"] == 23


def test_a3_apparait_une_seule_fois_dans_le_detail_des_manques(client):
    """§6.3 — A3 est un item du sujet, avec deux sous-critères, pas deux questions."""
    refus = client.post("/eleve/%s/valider" % STUDENT)
    assert refus.status_code == 400
    detail = refus.text
    # Les identifiants bruts des sous-critères ne sont plus donnés à lire.
    assert "sous-critère analytique N−1" in detail
    assert "sous-critère analytique passerelle N" in detail
    assert "Regroupement des termes en x" in detail
    assert "Écriture réduite complète" in detail


# ========================================================== 4. doublon C2 (§8)
LIMITE_C2 = ("une non-réussite ici ne documente aucune fragilité sur la somme et la "
             "différence de relatifs")


def test_c2_ne_porte_qu_une_seule_limite_d_interpretation(session):
    crit = session.query(CriterionDefinition).filter_by(
        criterion_id="4E_INES_KEFI_C2_c2").one()
    limites = json.loads(crit.interpretation_limits_json or "[]")
    concernees = [m for m in limites if LIMITE_C2 in m]
    assert len(concernees) == 1, concernees
    # C'est bien la formulation complète qui a été conservée.
    assert "A1, A5 et C2 question 1" in concernees[0]
    assert not [m for m in limites if m.endswith("en A1 et A5")]


def test_c2_aucune_duplication_semantique_dans_la_page(page):
    debut = page.find('id="item-C2"')
    carte = page[debut:page.find('class="item-card"', debut + 1)]
    assert carte.count("ne documente aucune fragilité sur la somme") == 1


def test_aucun_autre_critere_n_a_de_limite_dupliquee(session):
    """Contrôle global : le correctif ne masque pas un doublon ailleurs."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    for item in assessment.items:
        for crit in item.criteria:
            limites = json.loads(crit.interpretation_limits_json or "[]")
            assert len(limites) == len(set(limites)), crit.criterion_id


# ================================ 5. isolation skill_id historique / scope (§9)
def _analyse(client, overrides):
    """Remplit la copie de façon synthétique puis renvoie l'analyse.

    Aucune validation n'est déclenchée : la correction reste modifiable, de sorte
    que l'ordre des tests de ce module n'a pas d'influence.
    """
    fill(client, STUDENT, overrides)
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        return ana.analyse(s, corr.current_correction(s, assessment.assessment_id),
                           assessment)


def _skill(payload, skill_id, scope):
    trouve = [s for s in payload["skills"]
              if s["analysis_skill_id"] == skill_id and s["curriculum_scope"] == scope]
    assert len(trouve) == 1, (skill_id, scope, len(trouve))
    return trouve[0]


# --------------------------------------------------------------- 9.1 — audit
def test_9_1_l_agregation_se_fait_sur_une_cle_composite(session, client):
    """Le mécanisme réel d'agrégation, constaté par son comportement.

    Deux critères portent le même analysis_skill_id M4E_LIT_01 avec des périmètres
    différents. S'ils étaient agrégés par skill_id seul, l'analyse ne produirait
    qu'une entrée ; la clé composite en produit deux, strictement disjointes.
    """
    partages = {}
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    for row in corr.scoring_rows(assessment):
        partages.setdefault(row["analysis_skill_id"], set()).add(row["curriculum_scope"])
    chevauchants = {k: v for k, v in partages.items() if len(v) > 1}
    # La situation décrite existe réellement dans les données d'Inès.
    assert "M4E_LIT_01" in chevauchants
    assert chevauchants["M4E_LIT_01"] == {"n_minus_1", "bridge_n"}
    assert "M4E_LIT_02" in chevauchants
    assert chevauchants["M4E_LIT_02"] == {"n_minus_1", "bridge_n"}

    payload = _analyse(client, {})
    for skill_id, scopes in chevauchants.items():
        entrees = [s for s in payload["skills"] if s["analysis_skill_id"] == skill_id]
        assert len(entrees) == len(scopes), skill_id
        assert {e["curriculum_scope"] for e in entrees} == scopes
        # aucune ligne analytique n'est comptée dans deux entrées à la fois
        vues = [c for e in entrees for c in e["criteria"]]
        assert len(vues) == len(set(vues))


# ----------------------------------------------------------- 9.3 — scénario 1
def test_9_3_scenario_1_bridge_echoue_le_n_moins_1_du_meme_skill_reste_intact(client):
    """B2_c1 (bridge, M4E_LIT_01) à 0 ; C1_c3 et C1_c4 (N−1, M4E_LIT_01) au maximum."""
    payload = _analyse(client, {
        "4E_INES_KEFI_B2_c1": {"score_centi": 0, "error_codes": ["CONCEPT"]},
    })

    n1 = _skill(payload, "M4E_LIT_01", "n_minus_1")
    bridge = _skill(payload, "M4E_LIT_01", "bridge_n")

    # le N−1 reste entièrement réussi
    assert n1["success_rate"] == 1.0
    assert n1["earned_centi"] == n1["available_centi"] == 250   # C1_c3 1,5 + C1_c4 1,0
    assert n1["status"] not in ("A_CONSOLIDER", "PRIORITAIRE")
    assert n1["priority_rank"] in ("OK", "P3")

    # aucune erreur du bridge n'a rejoint le profil N−1
    assert n1["error_codes"] == []
    assert "CONCEPT" not in payload["error_profile"]["n_minus_1"]
    assert payload["error_profile"]["bridge_n"].get("CONCEPT") == 1

    # les preuves ne sont pas mélangées : la ligne bridge n'est pas comptée en N−1
    assert "4E_INES_KEFI_B2_c1" not in n1["criteria"]
    assert n1["criteria"] == ["4E_INES_KEFI_C1_c3", "4E_INES_KEFI_C1_c4"]
    assert bridge["criteria"] == ["4E_INES_KEFI_B2_c1"]
    assert bridge["success_rate"] == 0.0
    assert bridge["bridge_action"] in ("BRIDGE_REVISIT", "DISCOVERY_TO_CONTINUE")
    assert bridge["priority_rank"] is None      # une passerelle ne devient jamais P1

    # la consolidation N−1 n'est pas entamée par l'échec de la passerelle
    assert payload["n_minus_1_consolidation"]["percentage"] == 100.0


# ----------------------------------------------------------- 9.4 — scénario 2
def test_9_4_scenario_2_reduction_bridge_a_zero_et_controle_n_moins_1_reussi(client):
    """B2_c2 (bridge, M4E_LIT_02) à 0 ; B2_c3 (N−1, M4E_LIT_02) au maximum."""
    payload = _analyse(client, {
        "4E_INES_KEFI_B2_c2": {"score_centi": 0, "error_codes": ["CALCUL"]},
    })

    n1 = _skill(payload, "M4E_LIT_02", "n_minus_1")
    bridge = _skill(payload, "M4E_LIT_02", "bridge_n")

    # la compétence de contrôle par substitution reste réussie
    assert n1["success_rate"] == 1.0
    assert "4E_INES_KEFI_B2_c3" in n1["criteria"]
    assert "4E_INES_KEFI_B2_c2" not in n1["criteria"]
    assert n1["status"] not in ("A_CONSOLIDER", "PRIORITAIRE")

    # aucun code d'erreur de la passerelle dans les erreurs N−1
    assert n1["error_codes"] == []
    assert "CALCUL" not in payload["error_profile"]["n_minus_1"]
    assert payload["error_profile"]["bridge_n"].get("CALCUL") == 1

    # la passerelle peut être à revoir, sans conclusion négative sur le N−1
    assert bridge["criteria"] == ["4E_INES_KEFI_B2_c2"]
    assert bridge["bridge_action"] in ("BRIDGE_REVISIT", "DISCOVERY_TO_CONTINUE")
    for interdit in ("non acquis", "lacune", "fragile", "prioritaire"):
        assert interdit not in (bridge["reading"] + bridge["status_label"]).lower()


# ------------------------------------------- 9.2 — invariant, tous scopes mêlés
def test_9_2_aucune_ligne_bridge_n_influence_une_grandeur_n_moins_1(client, session):
    """Invariant absolu : toutes les passerelles à 0, tous les N−1 au maximum."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    bridge_ids = [r["scoring_id"] for r in corr.scoring_rows(assessment)
                  if r["curriculum_scope"] == "bridge_n"]
    assert len(bridge_ids) == 4

    payload = _analyse(client, {
        sid: {"score_centi": 0, "error_codes": ["CONCEPT"]} for sid in bridge_ids})

    assert payload["n_minus_1_consolidation"]["percentage"] == 100.0
    assert payload["n_minus_1_consolidation"]["available_centi"] == 1750
    assert payload["bridge_n_readiness"]["available_centi"] == 250
    assert payload["error_profile"]["n_minus_1"] == {}

    for skill in payload["skills"]:
        if skill["curriculum_scope"] != "n_minus_1":
            continue
        assert skill["success_rate"] == 1.0
        assert skill["error_codes"] == []
        assert skill["status"] not in ("A_CONSOLIDER", "PRIORITAIRE")
        assert skill["priority_rank"] in ("OK", "P3")
        # aucune ligne d'un autre périmètre n'a servi de preuve
        for scoring_id in skill["criteria"]:
            assert scoring_id not in bridge_ids


def test_9_2b_le_mastery_delta_reste_indisponible(client):
    """Aucune progression n'est fabriquée, quel que soit le périmètre."""
    payload = _analyse(client, {})
    for skill in payload["skills"]:
        assert skill["mastery_delta"] is None


# ============================================ 6. les autres élèves sont intacts
def test_les_quatorze_autres_couples_ne_sont_pas_reclasses(session):
    """§13 — expected_semantic_changes = 0 pour les autres élèves.

    Le renderer et la déduplication des limites sont techniquement généraux ; ce
    test vérifie qu'ils n'ont reclassé aucun critère ni déplacé aucun barème.
    """
    from app.models import Student
    autres = [s for s in session.query(Student).all() if s.student_id != STUDENT]
    assert len(autres) == 14

    for student in autres:
        assessment = session.query(Assessment).filter_by(
            student_id=student.student_id).one()
        lignes = corr.scoring_rows(assessment)
        # le total imprimé est intact et se recompose exactement
        assert sum(r["max_score_centi"] for r in lignes) == assessment.max_points_centi
        # aucun périmètre inconnu n'a été introduit
        for row in lignes:
            assert row["curriculum_scope"] in ("n_minus_1", "bridge_n")


def test_le_perimetre_des_criteres_mixtes_n_a_pas_bouge(session):
    """Quatre critères mixtes dans toute l'application, et pas un de plus.

    Trois préexistent à la passe Inès : ils viennent de la couche V3 et concernent
    le même critère C1_c4 chez trois élèves de première spécialité. Le quatrième
    est A3_c1 d'Inès, introduit par la passe corrective précédente. Ce test fige
    l'inventaire pour qu'un éclatement supplémentaire ne passe pas inaperçu.
    """
    from app.models import Student
    mixtes = {}
    for student in session.query(Student).all():
        assessment = session.query(Assessment).filter_by(
            student_id=student.student_id).one()
        for item in assessment.items:
            for crit in item.criteria:
                if crit.curriculum_scope == "mixed":
                    mixtes[student.student_id] = crit.criterion_id
                    # tout critère mixte se recompose exactement, chez tout le monde
                    assert sum(p.max_score_centi for p in crit.virtual_parts) == \
                        crit.max_score_centi

    assert mixtes == {
        "ahmad-beldi-maths": "1ERE_SPE_AHMAD_BELDI_C1_c4",
        "donia-khadhrani": "1ERE_SPE_DONIA_KHADHRANI_C1_c4",
        "malek-khadhrani": "1ERE_SPE_MALEK_KHADHRANI_C1_c4",
        STUDENT: "4E_INES_KEFI_A3_c1",
    }


def test_le_mode_replace_ne_concerne_qu_un_seul_critere():
    """Le correctif du doublon C2 est déclaré critère par critère, pas globalement."""
    concernes = [cid for cid, overlay in criterion_overlays.OVERLAYS.items()
                 if overlay.get("interpretation_limits_mode") == "replace"]
    assert concernes == ["4E_INES_KEFI_C2_c2"]
