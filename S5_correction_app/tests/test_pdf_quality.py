# -*- coding: utf-8 -*-
"""Qualité des documents produits : typographie, langue, provenance, format.

Ce module teste ce qu'une machine peut établir. Il ne teste pas l'esthétique :
aucune assertion ici ne dit qu'une page est belle ou qu'une hiérarchie se lit
bien. Ces jugements sont portés par la relecture visuelle, consignée dans
``docs/PDF_VISUAL_QA_FINAL.md``, et le rapport de QA le dit explicitement.

Les tests qui compilent réellement un PDF sont marqués : ils prennent quelques
secondes chacun et ne portent que sur un échantillon. Le contrôle exhaustif des
quarante-cinq documents est l'affaire de ``tools/check_report_pdf_quality.py``.
"""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

from app import database
from app.domain import correction as corr
from app.domain.longitudinal import LongitudinalReportService, narrative, render
from app.domain.reports import latex_escape, latex_id, latex_pedagogique
from app.models import Assessment

STUDENT = "ines-kefi"
TEST_LABEL = "TEST_INES"

LATEX_MOTEUR_PRESENT = shutil.which("pdflatex") is not None
POPPLER_PRESENT = shutil.which("pdfinfo") is not None


# ================================================ 1. échappement typographique
def test_les_macros_pedagogiques_deviennent_des_commandes_latex():
    """« \\code{return} » s'affichait tel quel dans la synthèse enseignant."""
    assert latex_pedagogique(r"absence de \code{return}") == \
        r"absence de \texttt{return}"
    assert latex_pedagogique(r"\textbf{Titre.} suite") == r"\textbf{Titre.} suite"
    assert latex_pedagogique(r"un \emph{exemple}") == r"un \emph{exemple}"


def test_le_contenu_d_une_macro_reste_echappe():
    """L'enveloppe devient une commande ; son contenu reste du texte."""
    rendu = latex_pedagogique(r"\code{a & b # c}")
    assert rendu.startswith(r"\texttt{")
    assert r"\&" in rendu and r"\#" in rendu


def test_une_macro_inconnue_n_est_pas_interpretee():
    rendu = latex_pedagogique(r"\dangereux{rm -rf}")
    assert r"\dangereux" not in rendu
    assert "textbackslash" in rendu


def test_une_accolade_non_refermee_ne_casse_pas_le_document():
    rendu = latex_pedagogique(r"\code{sans fin")
    assert r"\texttt{" not in rendu          # on n'invente pas la fermeture


def test_un_identifiant_technique_devient_secable():
    """Sans point de césure, un identifiant déborde de sa colonne de tableau."""
    rendu = latex_id("M1RE_SUITES_RECURRENCE_BRIDGE")
    assert r"\allowbreak" in rendu
    assert rendu.count(r"\allowbreak") == 3
    assert "M1RE" in rendu and "BRIDGE" in rendu


def test_les_caracteres_refuses_par_le_moteur_sont_traduits():
    """Relevés sur le corpus, chacun vérifié par une compilation d'essai."""
    for caractere, attendu in (("−", "-"), ("∪", r"$\cup$"),
                               ("≥", r"$\geq$"), ("⁴", r"$^{4}$"),
                               ("⁻", r"$^{-}$")):
        assert latex_escape(caractere) == attendu


def test_un_caractere_imprevu_ne_fait_jamais_echouer_un_document():
    for caractere in "∀∮♠⨁":
        assert caractere not in latex_escape("a %s b" % caractere)


def test_les_caracteres_acceptes_traversent_intacts():
    texte = "« citation » 3° 2² 3³ 5×2 6÷3 — …"
    assert latex_escape(texte) == texte


# ==================================================== 2. gabarit parents
@pytest.fixture(scope="module")
def facts(client):
    """Copie synthétique validée : prérequis réussis, passerelles échouées."""
    bridge = ("4E_INES_KEFI_B2_c1", "4E_INES_KEFI_B2_c2",
              "4E_INES_KEFI_C2_c2", "4E_INES_KEFI_A3_c1_v2")
    client.get("/eleve/%s" % STUDENT)
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
        lignes = [(r.scoring_id, r.max_score_centi)
                  for r in corr.current_correction(
                      session, assessment.assessment_id).responses]
    for scoring_id, maximum in lignes:
        client.post("/eleve/%s/critere/%s" % (STUDENT, scoring_id),
                    json={"score_centi": 0, "error_codes": ["CONCEPT"]}
                    if scoring_id in bridge
                    else {"score_centi": maximum, "error_codes": []})
    client.post("/eleve/%s/valider" % STUDENT, follow_redirects=False)
    with database.session_scope() as session:
        assessment = session.query(Assessment).filter_by(student_id=STUDENT).one()
        return LongitudinalReportService(session).build_longitudinal_facts(
            assessment, corr.current_correction(session, assessment.assessment_id),
            persist=False)


def test_le_gabarit_parents_declare_ses_metadonnees(facts):
    """§40 — un PDF sans titre s'affiche « sans nom » dans un lecteur."""
    tex = render.render_tex(facts)
    assert "pdftitle={Bilan individuel de fin de stage" in tex
    assert "pdfauthor={Nexus Réussite}" in tex
    assert "pdfsubject={Stage de pré-rentrée" in tex


def test_aucun_chemin_local_ne_figure_dans_le_document(facts):
    """§40 — ni chemin, ni nom d'utilisateur, ni URI file://."""
    tex = render.render_tex(facts)
    assert "/home/" not in tex
    assert "file://" not in tex
    assert "/Users/" not in tex


def test_la_structure_editoriale_est_stable(facts):
    """Quatre sauts de page fixent les cinq premières sections.

    La clôture — priorités, conseil, limites — suit le plan sans saut forcé : le
    tableau du plan occupe déjà une page entière, et forcer un cinquième saut
    produirait une page presque vide plutôt qu'une page de clôture.
    """
    tex = render.render_tex(facts)
    assert tex.count("\\newpage") == 4
    for titre in ("L'essentiel", "La trajectoire du stage", "Bilan par domaines",
                  "L'évaluation de clôture", "Plan de travail",
                  "Conseil Nexus Réussite"):
        assert titre in tex, titre


def test_les_largeurs_de_colonnes_tiennent_dans_le_bloc_de_texte(facts):
    """§14 — une somme de colonnes supérieure au bloc produit un débordement.

    Le bloc de texte fait 178 mm (A4 moins deux marges de 16 mm).
    """
    tex = render.render_tex(facts)
    for specification in re.findall(r"\{@\{\}([^}]*(?:\{[^}]*\}[^}]*)*)@\{\}\}", tex):
        largeurs = [float(v) for v in re.findall(r"p\{([\d.]+)mm\}", specification)]
        if largeurs:
            assert sum(largeurs) <= 178, (specification, sum(largeurs))


def test_le_plan_est_un_tableau_unique_a_en_tete_repete(facts):
    """§15 — un tableau long doit répéter son en-tête, pas la perdre."""
    tex = render.render_tex(facts)
    plan = tex[tex.index("Plan de travail"):]
    assert plan.count("\\begin{longtable}") == 1
    assert "\\endhead" in plan


def test_le_document_parents_ne_contient_aucun_jargon(facts):
    from app.domain.longitudinal import guard
    blocs = narrative.parent_blocks(facts)
    texte = "\n".join(contenu for _, _, contenu in blocs)
    controle = guard.validate(texte, facts["skills"], "parents")
    assert controle["ok"], controle["violations"]


# ============================================== 3. provenance du texte (§52)
def test_chaque_affirmation_du_bilan_remonte_aux_faits(facts):
    """§52 — un échantillon de phrases, rattaché à LONGITUDINAL_FACTS.

    On ne vérifie pas la grammaire mais l'ancrage : tout libellé de compétence
    cité dans le document doit exister dans la matrice, et tout chiffre annoncé
    doit provenir des pools calculés.
    """
    blocs = dict((cle, contenu) for cle, _, contenu in narrative.parent_blocks(facts))
    labels = {(l["label"] or "").lower().rstrip(".") for l in facts["skills"]}
    domaines = {(d["domain"] or "").lower() for d in facts["domains"]}
    connus = labels | domaines

    # Les points forts et les points à consolider ne citent que des compétences
    # présentes dans la matrice.
    for cle in ("points_forts", "points_consolider", "a_confirmer"):
        for ligne in (blocs.get(cle) or "").splitlines():
            if not ligne.startswith("— "):
                continue
            # Le libellé d'une compétence peut lui-même contenir « : »
            # (« distributivité simple : développer k(a+b) ») : on cherche donc
            # un libellé connu en tête de ligne, sans découper sur le séparateur.
            debut = ligne[2:].lower()
            assert any(debut.startswith(connu) for connu in connus if connu), ligne[:90]

    # Les chiffres de la consolidation viennent du pool, pas d'un calcul ad hoc.
    consolidation = blocs["consolidation"]
    n1 = facts["n_minus_1"]
    assert n1["earned"] in consolidation
    assert n1["available"] in consolidation


def test_le_score_brut_annonce_est_celui_de_l_analyse(facts):
    blocs = dict((cle, contenu) for cle, _, contenu in narrative.parent_blocks(facts))
    brut = facts["final_assessment"]["raw_score"]
    attendu = brut["sur_20"] if isinstance(brut, dict) else str(brut)
    assert attendu in blocs["score_brut"]


# Blocs qui rapportent un résultat chiffré. Ailleurs, un pourcentage peut être une
# statistique reprise du diagnostic — l'accord entre réussite et certitude
# annoncée, par exemple — qui n'a pas de dénominateur à exhiber : la phrase qui la
# porte en donne déjà le sens.
BLOCS_CHIFFRES = ("essentiel", "consolidation", "score_brut", "passerelles")


def test_aucun_pourcentage_de_resultat_n_est_affiche_sans_son_compte(facts):
    """§21 — « 83 % » seul ne veut rien dire ; il lui faut son dénominateur."""
    blocs = dict((cle, contenu) for cle, _, contenu in narrative.parent_blocks(facts))
    for cle in BLOCS_CHIFFRES:
        contenu = blocs.get(cle) or ""
        for trouve in re.finditer(r"(\d+(?:,\d+)?)\s*%", contenu):
            debut = max(0, trouve.start() - 260)
            contexte = contenu[debut:trouve.start()]
            assert " sur " in contexte or "points" in contexte, (cle, trouve.group(0))


def test_les_pourcentages_destines_aux_familles_sont_arrondis(facts):
    """§22 — pas de décimale superflue dans le document parents."""
    blocs = dict((cle, contenu) for cle, _, contenu in narrative.parent_blocks(facts))
    for contenu in blocs.values():
        for trouve in re.finditer(r"(\d+),(\d+)\s*%", contenu):
            assert len(trouve.group(2)) <= 1, trouve.group(0)


# ============================================ 4. compilation d'un échantillon
@pytest.mark.skipif(not (LATEX_MOTEUR_PRESENT and POPPLER_PRESENT),
                    reason="moteur LaTeX ou poppler absent de cette machine")
def test_le_bilan_parents_compile_en_a4_avec_ses_metadonnees(facts):
    travail = Path(tempfile.mkdtemp(prefix="nexus_pdfqa_test_"))
    resultat = render.compile_pdf(facts, "%s_QA" % TEST_LABEL, work_dir=travail)
    assert resultat["ok"], resultat.get("reason")

    infos = subprocess.run(["pdfinfo", resultat["pdf_path"]], capture_output=True,
                           text=True, shell=False).stdout
    assert "595.276 x 841.89 pts" in infos, infos
    assert "Bilan individuel de fin de stage" in infos
    assert "Nexus Réussite" in infos

    pages = int(infos.split("Pages:")[1].split("\n")[0].strip())
    assert 4 <= pages <= 6, pages

    texte = subprocess.run(["pdftotext", resultat["pdf_path"], "-"],
                           capture_output=True, text=True, shell=False).stdout
    for sequence in ("\\begin{", "\\end{", "\\VAR{", "\\code{", "\\textbf{"):
        assert sequence not in texte, sequence
    assert "/home/" not in texte
    shutil.rmtree(travail, ignore_errors=True)


@pytest.mark.skipif(not (LATEX_MOTEUR_PRESENT and POPPLER_PRESENT),
                    reason="moteur LaTeX ou poppler absent de cette machine")
def test_aucune_page_du_bilan_n_est_vide(facts):
    """Une page blanche au milieu d'un document remis est un défaut bloquant."""
    from tools import pdf_visual_qa as visual
    travail = Path(tempfile.mkdtemp(prefix="nexus_pdfqa_blank_"))
    resultat = render.compile_pdf(facts, "%s_BLANK" % TEST_LABEL, work_dir=travail)
    assert resultat["ok"]
    audit = visual.auditer(resultat["pdf_path"], travail, dpi=90, contact=False)
    vides = [m["page"] for m in audit["pages_measured"] if m["blank"]]
    assert vides == [], vides
    assert audit["is_a4"]
    shutil.rmtree(travail, ignore_errors=True)


@pytest.mark.skipif(not (LATEX_MOTEUR_PRESENT and POPPLER_PRESENT),
                    reason="moteur LaTeX ou poppler absent de cette machine")
def test_rien_n_approche_le_bord_de_la_feuille(facts):
    """§5 — huit millimètres au moins entre l'encre et le bord."""
    from tools import pdf_visual_qa as visual
    travail = Path(tempfile.mkdtemp(prefix="nexus_pdfqa_marge_"))
    resultat = render.compile_pdf(facts, "%s_MARGE" % TEST_LABEL, work_dir=travail)
    assert resultat["ok"]
    audit = visual.auditer(resultat["pdf_path"], travail, dpi=110, contact=False)
    serrees = [a for a in audit["alerts"] if a["code"] == "marge_critique"]
    assert serrees == [], serrees
    shutil.rmtree(travail, ignore_errors=True)


# ================================================= 5. politique graphique (§18)
def test_aucun_graphique_interdit_n_est_produit(facts):
    """Radar, jauge, courbe de progression : la politique les refuse.

    Le contrôle porte sur le LaTeX produit : aucun environnement de dessin ne doit
    y apparaître. C'est la traduction technique de REPORT_VISUALIZATION_POLICY.md.
    """
    tex = render.render_tex(facts)
    for environnement in ("tikzpicture", "pgfplots", "axis", "pspicture",
                          "spider", "radar"):
        assert "\\begin{%s}" % environnement not in tex, environnement


def test_la_politique_de_visualisation_est_documentee():
    from app import config
    chemin = Path(config.PROJECT_DIR) / "docs" / "REPORT_VISUALIZATION_POLICY.md"
    assert chemin.exists()
    texte = chemin.read_text(encoding="utf-8")
    for decision in ("REFUSÉE", "REFUSÉ", "ACCEPTÉ"):
        assert decision in texte
    for sujet in ("radar", "Frise de progression", "Barres horizontales"):
        assert sujet.lower() in texte.lower(), sujet
