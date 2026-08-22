# -*- coding: utf-8 -*-
"""Passe corrective Inès KEFI — référentiel, rubriques, erreurs, interface.

Aucun test n'invente de score au nom d'Inès : les valeurs employées sont des fixtures
synthétiques, préfixées ``TEST_INES``, dans une base jetable.
"""

import json
import re


from app import config, database
from app.data import criterion_overlays
from app.domain import analysis as ana
from app.domain import correction as corr
from app.domain import points
from app.models import Assessment, CriterionDefinition
from conftest import fill

STUDENT = "ines-kefi"
TEST_LABEL = "TEST_INES"          # marqueur des données synthétiques de ce module


# ============================================================ 1. les 22 critères
def test_1_les_22_criteres_originaux_sont_presents(session):
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    criteres = [c for item in assessment.items for c in item.criteria]
    assert len(criteres) == 22
    attendus = set(criterion_overlays.covered_criteria())
    assert {c.criterion_id for c in criteres} == attendus
    # Les identifiants imprimés n'ont pas bougé.
    for c in criteres:
        assert c.criterion_id.startswith("4E_INES_KEFI_")


def test_2_le_score_brut_maximum_reste_vingt(session):
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    assert assessment.max_points_centi == 2000
    somme = sum(c.max_score_centi for item in assessment.items for c in item.criteria)
    assert somme == 2000


def test_3_les_portees_recomposent_exactement_vingt_points(session):
    """N−1 + passerelle + sous-critères virtuels = 20, sans perte ni double comptage."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    n1 = bridge = mixed_total = 0
    lignes = set()
    for item in assessment.items:
        for crit in item.criteria:
            if crit.curriculum_scope == "mixed":
                mixed_total += crit.max_score_centi
                assert sum(p.max_score_centi for p in crit.virtual_parts) == \
                    crit.max_score_centi
                for part in crit.virtual_parts:
                    assert part.virtual_criterion_id not in lignes
                    lignes.add(part.virtual_criterion_id)
                    if part.curriculum_scope == "bridge_n":
                        bridge += part.max_score_centi
                    else:
                        n1 += part.max_score_centi
            else:
                assert crit.criterion_id not in lignes
                lignes.add(crit.criterion_id)
                if crit.curriculum_scope == "bridge_n":
                    bridge += crit.max_score_centi
                else:
                    n1 += crit.max_score_centi
    assert n1 + bridge == 2000
    assert (n1, bridge) == (1750, 250), (points.format_fr(n1), points.format_fr(bridge))
    assert assessment.n_minus_1_available_centi == n1
    assert assessment.bridge_available_centi == bridge
    assert mixed_total == 100


def test_3b_le_nouveau_classement_est_source(session):
    """Chaque critère cite un attendu officiel, et non « il n'est pas en phase 4 »."""
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    for item in assessment.items:
        for crit in item.criteria:
            assert crit.official_source, crit.criterion_id
            assert crit.scope_certainty in criterion_overlays.CERTAINTY
            assert crit.scope_rationale
            assert "aucune notion du programme de l'année N n'est requise" \
                not in crit.scope_rationale, crit.criterion_id


def test_3c_les_reclassements_attendus_sont_effectifs(session):
    """Ce que la revue réglementaire a changé, et ce qu'elle a confirmé."""
    par_id = {c.criterion_id: c for item in
              session.query(Assessment).filter_by(student_id=STUDENT).one().items
              for c in item.criteria}
    # développer k(a − b) : absent des attendus de 5e, explicite en 4e
    assert par_id["4E_INES_KEFI_B2_c1"].curriculum_scope == "bridge_n"
    assert par_id["4E_INES_KEFI_B2_c2"].curriculum_scope == "bridge_n"
    # substituer pour contrôler : explicitement attendu en 5e
    assert par_id["4E_INES_KEFI_B2_c3"].curriculum_scope == "n_minus_1"
    # produit de relatifs : attendu de 4e, déjà classé passerelle
    assert par_id["4E_INES_KEFI_C2_c2"].curriculum_scope == "bridge_n"
    # déplacements sur droite graduée : resté séparé et en N−1
    assert par_id["4E_INES_KEFI_C2_c1"].curriculum_scope == "n_minus_1"
    # dénominateurs multiples l'un de l'autre : attendu de 5e
    assert par_id["4E_INES_KEFI_A2_c1"].curriculum_scope == "n_minus_1"
    # expression littérale et substitution : attendus de 5e, non reclassés
    assert par_id["4E_INES_KEFI_C1_c3"].curriculum_scope == "n_minus_1"
    assert par_id["4E_INES_KEFI_C1_c4"].curriculum_scope == "n_minus_1"
    # réduction mêlant termes en x et constantes : ambiguïté assumée
    assert par_id["4E_INES_KEFI_A3_c1"].curriculum_scope == "mixed"
    assert par_id["4E_INES_KEFI_A3_c1"].scope_certainty == "moyenne"


def test_3d_les_quatorze_autres_eleves_ne_sont_pas_touches(session):
    """La passe ne porte que sur Inès : aucun autre élève ne change de portée."""
    attendus = {"ahmad-beldi-maths": (1750, 250), "ahmad-beldi-nsi": (1475, 525),
                "ahmed-bakir": (2000, 0), "ahmed-benhadj-salem": (1475, 525),
                "amine-mansouri": (1950, 50), "donia-khadhrani": (1950, 50),
                "elyes-kefi": (1850, 150), "fares-darghouth": (2000, 0),
                "fares-laajili": (1650, 350), "malek-khadhrani": (1950, 50),
                "noa-maniaci": (2000, 0), "sarah-bargaoui": (1950, 50),
                "selim-mansouri": (1850, 150), "sinda-chikhaoui": (2000, 0)}
    for student_id, (n1, bridge) in attendus.items():
        a = session.query(Assessment).filter_by(student_id=student_id).one()
        assert (a.n_minus_1_available_centi, a.bridge_available_centi) == (n1, bridge), \
            student_id
    couverts = {cid.rsplit("_c", 1)[0] for cid in criterion_overlays.covered_criteria()}
    assert all(c.startswith("4E_INES_KEFI") for c in couverts)


# ================================================== 5 & 6. rubriques de score
def _scoring_rows(session):
    assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
    rows = []
    for item in assessment.items:
        for crit in item.criteria:
            if crit.curriculum_scope == "mixed":
                rows.extend(crit.virtual_parts)
            else:
                rows.append(crit)
    return rows


def test_5_chaque_score_possible_possede_une_regle(session):
    for row in _scoring_rows(session):
        rubric = json.loads(row.score_rubric_json or "[]")
        assert rubric, getattr(row, "virtual_criterion_id", None) or row.criterion_id
        for niveau in rubric:
            assert niveau["regle"].strip()
            assert 0 <= niveau["score_centi"] <= row.max_score_centi
        scores = [n["score_centi"] for n in rubric]
        assert 0 in scores, "le zéro doit toujours être décrit"
        assert row.max_score_centi in scores, "le plein score doit toujours être décrit"
        assert len(scores) == len(set(scores))


def test_6_aucune_valeur_proposee_par_l_interface_n_est_sans_rubrique(client, session):
    """Les boutons affichés sont exactement ceux que la rubrique décrit."""
    page = client.get("/eleve/%s" % STUDENT).text
    for row in _scoring_rows(session):
        scoring_id = getattr(row, "virtual_criterion_id", None) or row.criterion_id
        bloc = _bloc(page, scoring_id)
        proposes = sorted(int(v) for v in
                          re.findall(r'class="score-btn[^"]*"[^>]*data-centi="(\d+)"', bloc))
        decrits = sorted(n["score_centi"] for n in json.loads(row.score_rubric_json))
        assert proposes == decrits, scoring_id
    # Les valeurs que rien ne justifiait ont disparu : 0,15 sur un critère à 0,3 était
    # une simple moitié arithmétique, sans règle d'attribution derrière elle.
    assert 'data-centi="15"' not in page


def _bloc(page: str, scoring_id: str) -> str:
    start = page.find('data-scoring-id="%s"' % scoring_id)
    assert start != -1, scoring_id
    end = page.find('data-scoring-id="', start + 10)
    return page[start:end if end != -1 else start + 12000]


# ============================================ 7-9. erreurs propres au critère
def test_7_chaque_suggestion_est_rattachee_a_un_criterion_id(session):
    for row in _scoring_rows(session):
        parent = row.criterion_id
        suggestions = json.loads(row.error_suggestions_json or "[]")
        assert suggestions, parent
        for suggestion in suggestions:
            assert suggestion["criterion_id"] == parent
            assert suggestion["error_code"] in corr.ERROR_CODES
            assert suggestion["description"].strip()


def test_8_b1_n_affiche_pas_l_erreur_de_son_autre_critere(client):
    page = client.get("/eleve/%s" % STUDENT).text
    aire = _bloc(page, "4E_INES_KEFI_B1_c1")
    prix = _bloc(page, "4E_INES_KEFI_B1_c2")

    def suggeres(bloc):
        return set(re.findall(r'code-chip suggested[^>]*data-code="([A-Z]+)"', bloc))

    assert suggeres(aire) != suggeres(prix)
    # L'erreur « prix calculé à partir du périmètre » appartient au critère prix.
    assert "à partir du périmètre" in prix
    assert "à partir du périmètre" not in aire
    # L'erreur d'unité appartient au critère aire.
    assert "unité m employée pour une aire" in aire
    assert "unité m employée pour une aire" not in prix


def test_9_b2_distingue_developpement_reduction_et_controle(client):
    page = client.get("/eleve/%s" % STUDENT).text
    dev = _bloc(page, "4E_INES_KEFI_B2_c1")
    red = _bloc(page, "4E_INES_KEFI_B2_c2")
    ctrl = _bloc(page, "4E_INES_KEFI_B2_c3")
    assert "distributivité appliquée au seul premier terme" in dev
    assert "distributivité appliquée au seul premier terme" not in red
    assert "distributivité appliquée au seul premier terme" not in ctrl
    assert "aucun contrôle mené" in ctrl
    assert "aucun contrôle mené" not in dev
    assert "aucun contrôle mené" not in red

    def suggeres(bloc):
        return set(re.findall(r'code-chip suggested[^>]*data-code="([A-Z]+)"', bloc))

    assert suggeres(ctrl) != suggeres(dev)
    assert "CONTROLE" in suggeres(ctrl)
    assert "CONTROLE" not in suggeres(dev)


def test_9b_une_suggestion_n_est_jamais_cochee_d_office(client):
    page = client.get("/eleve/%s" % STUDENT).text
    assert 'code-chip suggested on"' not in page
    assert not re.search(r'code-chip suggested[^>]*aria-checked="true"', page)


# ============================================================ 10. mathématiques
def test_10_les_mathematiques_sont_rendues_et_katex_est_local(client):
    page = client.get("/eleve/%s" % STUDENT).text
    assert "/static/vendor/katex/katex.min.js" in page
    assert "/static/vendor/katex/katex.min.css" in page
    assert "/static/math.js" in page
    # aucune ressource distante
    assert not re.search(r'(src|href)="https?://', page)
    # tout le LaTeX visible est confié au moteur : il vit dans un conteneur « math »
    for motif in (r"\dfrac", r"\frac", r"^\circ"):
        for position in [m.start() for m in re.finditer(re.escape(motif), page)]:
            contexte = page[max(0, position - 900):position]
            assert 'class="math"' in contexte or "math\"" in contexte, \
                "%s hors d'un conteneur math" % motif


def test_10b_les_ressources_katex_sont_servies_localement(client):
    for chemin in ("/static/vendor/katex/katex.min.js",
                   "/static/vendor/katex/katex.min.css",
                   "/static/vendor/katex/auto-render.min.js",
                   "/static/math.js"):
        reponse = client.get(chemin)
        assert reponse.status_code == 200, chemin
        assert len(reponse.content) > 500, chemin
    css = (config.STATIC_DIR / "vendor" / "katex" / "katex.min.css").read_text(
        encoding="utf-8")
    assert not re.search(r"url\((https?:)?//", css), "police distante dans la CSS KaTeX"
    fonts = list((config.STATIC_DIR / "vendor" / "katex" / "fonts").glob("*.woff2"))
    assert len(fonts) >= 15


# ==================================================== 11. raccourcis clavier
def test_11_les_raccourcis_sont_neutralises_dans_les_champs_de_saisie():
    """Le garde-fou couvre input, textarea, select, button et contenteditable."""
    source = (config.STATIC_DIR / "app.js").read_text(encoding="utf-8")
    assert "isTypingContext" in source
    for balise in ("input", "textarea", "select", "button"):
        assert '"%s"' % balise in source
    assert "isContentEditable" in source
    assert "contenteditable" in source
    # le garde-fou est appelé avant toute interprétation de touche
    garde = source.index("isTypingContext(event.target)")
    for touche in ('key === "f"', 'key === "n"', "/^[0-9]$/.test(key)"):
        assert source.index(touche) > garde, touche


def test_11b_les_champs_de_saisie_sont_bien_identifiables(client):
    page = client.get("/eleve/%s" % STUDENT).text
    assert "<textarea" in page and "<select" in page
    assert "nexusIsTypingContext" in (config.STATIC_DIR / "app.js").read_text(
        encoding="utf-8")


# ======================================================== 12. viewer collant
def test_12_le_viewer_pdf_est_collant_sur_desktop():
    css = (config.STATIC_DIR / "app.css").read_text(encoding="utf-8")
    desktop = css[css.index("@media (min-width: 1101px)"):]
    bloc = desktop[:desktop.index("/* ---")]
    assert ".pane-pdf" in bloc
    assert "position: sticky" in bloc
    assert "top:" in bloc
    assert "max-height: calc(100vh" in bloc
    # sur écran étroit, le sticky ne s'applique pas : on repasse en onglets
    assert "@media (max-width: 1100px)" in css
    assert ".split.tab-correction > .pane-pdf { display: none; }" in css


def test_12b_le_viewer_ne_recouvre_pas_l_entete(client):
    page = client.get("/eleve/%s" % STUDENT).text
    assert page.index("header class=\"topbar\"") < page.index("pane-pdf")


# ============================================================ 13. vocabulaire
ANCRE_BANDEAU = "lignes analytiques restent à renseigner"


def test_13_le_bandeau_parle_de_criteres_et_non_de_points(client):
    page = client.get("/eleve/%s" % STUDENT).text
    assert ANCRE_BANDEAU in page
    assert "point(s) à traiter" not in page
    assert "22 point" not in page
    # Le bandeau doit nommer les deux comptes : les lignes analytiques restant à
    # saisir, et les critères réellement imprimés sur le sujet distribué.
    assert "pour les 22 critères du sujet" in page
    # le détail est replié tant qu'aucune validation n'a été tentée
    bandeau = page[page.index(ANCRE_BANDEAU) - 400:
                   page.index(ANCRE_BANDEAU) + 200]
    assert "<details" in bandeau
    assert "<details open" not in bandeau


def test_13b_le_detail_s_ouvre_apres_une_tentative_de_validation(client):
    refus = client.post("/eleve/%s/valider" % STUDENT)
    assert refus.status_code == 400
    page = client.get("/eleve/%s?verif=1" % STUDENT).text
    index = page.index(ANCRE_BANDEAU)
    assert "<details open" in page[index - 400:index]


# ============================================================ 14. corrigé masqué
def test_14_le_corrige_est_masque_avant_ouverture(client):
    page = client.get("/eleve/%s" % STUDENT).text
    for bloc_id, reponse in (("4E_INES_KEFI_A1_c1", "résultat $0$ exact"),
                             ("4E_INES_KEFI_A4_c1", "53^\\circ$ exact"),
                             ("4E_INES_KEFI_A3_c1_v1", "4x-5")):
        bloc = _bloc(page, bloc_id)
        avant = bloc[:bloc.find("<details class=\"key\"")] if "<details class=\"key\"" \
            in bloc else bloc
        assert reponse not in avant, bloc_id
    # ce qui reste visible : la nature du critère, sa portée, sa preuve, son maximum
    bloc = _bloc(page, "4E_INES_KEFI_A1_c1")
    assert "Somme algébrique de relatifs" in bloc
    assert "maximum" in bloc
    assert "compétence" in bloc
    assert "preuve :" in bloc
    assert "N-1" in bloc


def test_14b_le_corrige_reste_accessible_dans_le_panneau(client):
    import html as html_module
    bloc = _bloc(client.get("/eleve/%s" % STUDENT).text, "4E_INES_KEFI_A1_c1")
    # Le gabarit échappe le texte : on désenchappe pour comparer au texte source.
    panneau = html_module.unescape(bloc[bloc.index('<details class="key"'):])
    assert "Réponse attendue" in panneau
    assert "Ce que ce critère attend" in panneau
    assert "Règle d'attribution" in panneau
    assert "Classement curriculaire" in panneau
    assert "Attendus de fin d'année de cinquième" in panneau
    assert "certitude haute" in panneau


# =============================================== 15. observations non scorées
def test_15_les_observations_generales_ne_touchent_jamais_les_points(client):
    payload = {"autonomie_choix": "Aide ponctuelle",
               "autonomie_commentaire": "%s : relance sur la lecture de l'énoncé" % TEST_LABEL,
               "rythme_choix": "Adapté",
               "libre_commentaire": "%s remarque synthétique" % TEST_LABEL,
               "observed_duration_minutes": 41}
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        avant = corr.raw_total_centi(corr.current_correction(s, assessment.assessment_id))
    assert client.post("/eleve/%s/observations" % STUDENT, json=payload).status_code == 200
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        correction = corr.current_correction(s, assessment.assessment_id)
        assert corr.raw_total_centi(correction) == avant
        stored = json.loads(correction.general_observations_json)
        assert stored["autonomie"]["choix"] == "Aide ponctuelle"
        assert TEST_LABEL in stored["autonomie"]["commentaire"]
        assert correction.observed_duration_minutes == 41


def test_15b_un_choix_hors_liste_est_refuse(client):
    refus = client.post("/eleve/%s/observations" % STUDENT,
                        json={"autonomie_choix": "Formidable"})
    assert refus.status_code == 400
    assert "valeur inconnue" in refus.json()["detail"]


def test_15c_les_observations_sont_structurees_et_facultatives(client):
    page = client.get("/eleve/%s" % STUDENT).text
    assert page.count("<select name=\"") >= 6
    assert "Remarque libre" in page
    assert "n'entre dans aucun calcul de points" in page
    assert client.post("/eleve/%s/observations" % STUDENT, json={}).status_code == 200


# ================================= 47. non-régression des quatre cas V3
def test_47_les_quatre_overlays_post_distribution_sont_intacts(session):
    """Sinda, Elyes, Ahmad et Malek ne doivent pas bouger pendant cette passe."""
    attendus = {
        "4E_SINDA_CHIKHAOUI_C2_c2": ("parallélogramme", "accepted_methods_json"),
        "3E_ELYES_KEFI_B4_c2": ("recomptage", "accepted_methods_json"),
        "1ERE_SPE_AHMAD_BELDI_B4_c1": ("argument valable pour tout", "proof_levels_json"),
        "1ERE_SPE_MALEK_KHADHRANI_C2_c2": ("contre-exemple", "accepted_methods_json"),
    }
    for criterion_id, (motif, colonne) in attendus.items():
        crit = session.get(CriterionDefinition, criterion_id)
        assert crit is not None, criterion_id
        assert motif in (getattr(crit, colonne) or ""), criterion_id
        assert crit.evidence_quality == "limited_by_prompt", criterion_id
        # aucun overlay applicatif ne les a touchés
        assert criterion_overlays.for_criterion(criterion_id) is None


# ================================================ 4. la passerelle ne dégrade rien
def test_4_un_echec_sur_les_passerelles_ne_degrade_pas_les_acquis(client):
    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        bridge_ids = []
        for item in assessment.items:
            for crit in item.criteria:
                if crit.curriculum_scope == "bridge_n":
                    bridge_ids.append(crit.criterion_id)
                for part in crit.virtual_parts:
                    if part.curriculum_scope == "bridge_n":
                        bridge_ids.append(part.virtual_criterion_id)
    assert len(bridge_ids) == 4          # B2_c1, B2_c2, C2_c2, A3_c1_v2

    overrides = {sid: {"score_centi": 0, "error_codes": ["CONCEPT"]} for sid in bridge_ids}
    fill(client, STUDENT, overrides)
    client.post("/eleve/%s/valider" % STUDENT, follow_redirects=False)

    with database.session_scope() as s:
        assessment = s.query(Assessment).filter_by(student_id=STUDENT).one()
        payload = ana.analyse(s, corr.current_correction(s, assessment.assessment_id),
                              assessment)

    assert payload["n_minus_1_consolidation"]["percentage"] == 100.0
    assert payload["bridge_n_readiness"]["percentage"] == 0.0
    for skill in payload["skills"]:
        if skill["curriculum_scope"] == "n_minus_1":
            assert skill["status"] not in ("A_CONSOLIDER", "PRIORITAIRE")
            assert skill["priority_rank"] in ("OK", "P3")
        else:
            assert skill["bridge_action"] in ("BRIDGE_REVISIT", "DISCOVERY_TO_CONTINUE")
            texte = (skill["reading"] + skill["status_label"]).lower()
            for interdit in ("non acquis", "lacune", "fragile", "prioritaire"):
                assert interdit not in texte
    assert not [p for p in payload["priorities"] if p["priority_rank"] in ("P1", "P2")]
    assert payload["error_profile"]["n_minus_1"] == {}
    assert payload["error_profile"]["bridge_n"] == {"CONCEPT": 4}


# ==================================================== 38. immutabilité finale
def test_zzz_38_aucun_artefact_distribue_n_a_change(immutability_before):
    from app.domain import immutability
    apres = immutability.verify()
    assert apres.total == 60
    assert apres.summary()["immutable_artifacts_changed"] == 0
    assert apres.summary()["immutable_artifacts_missing"] == 0
    for chemin, empreinte in immutability_before.by_path.items():
        assert apres.by_path[chemin] == empreinte, chemin
