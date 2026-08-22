# -*- coding: utf-8 -*-
"""Rendu web des énoncés NSI : code, tableaux d'état, repli.

Le blocker levé ici est simple à énoncer : un énoncé de NSI contient du code Python
et un tableau d'état. Sans conversion, l'enseignant voyait ``\\begin{lstlisting}``
au milieu de la page, ce qui rendait la correction pénible et l'application
inutilisable pour deux des quinze couples.

Le principe retenu n'est pas la reproduction parfaite : c'est **ne jamais afficher
de LaTeX brut**. Ce que la conversion ne sait pas traiter sûrement renvoie au PDF
distribué, qui reste affiché en vis-à-vis.

Aucun score réel n'est saisi. Les élèves NSI servent de cas d'intégration
synthétiques.
"""

import json
import re
from pathlib import Path

import pytest

from app import config
from app.latex_html import (FALLBACK_TEXTE, render_statement,
                            unsupported_structures)

NSI_ELEVES = ("ahmad-beldi-nsi", "ahmed-benhadj-salem")
SEQUENCES_INTERDITES = ("\\begin{", "\\end{", "\\item", "\\hline", "\\code{",
                        "\\textbf{", "\\emph{")


# ============================================================ 1. lstlisting
def test_un_listing_devient_un_bloc_de_code():
    rendu = str(render_statement(
        "Voici le programme.\n\\begin{lstlisting}\ntotal = 0\nfor v in [1, 2]:\n"
        "    total = total + v\n\\end{lstlisting}\nCommenter."))
    assert '<pre class="code-bloc code-python">' in rendu
    assert "<code>" in rendu and "</code></pre>" in rendu
    assert "\\begin{lstlisting}" not in rendu


def test_l_indentation_du_code_est_conservee():
    """En Python, l'indentation porte le sens : la perdre rend le code faux."""
    rendu = str(render_statement(
        "\\begin{lstlisting}\ndef f(x):\n    if x > 0:\n        return 1\n    return 0\n"
        "\\end{lstlisting}"))
    bloc = rendu[rendu.index("<code>") + 6:rendu.index("</code>")]
    lignes = bloc.split("\n")
    assert lignes[0] == "def f(x):"
    assert lignes[1] == "    if x &gt; 0:"       # quatre espaces conservés
    assert lignes[2] == "        return 1"       # huit espaces conservés
    assert lignes[3] == "    return 0"


def test_les_caracteres_speciaux_du_code_sont_echappes():
    """§8 — « < », « > » et « & » ne doivent jamais ouvrir un élément."""
    rendu = str(render_statement(
        "\\begin{lstlisting}\nif a < b and c > d & e:\n    print('<b>')\n"
        "\\end{lstlisting}"))
    assert "&lt;" in rendu and "&gt;" in rendu and "&amp;" in rendu
    assert "<b>" not in rendu
    assert "a < b" not in rendu


def test_aucune_injection_html_depuis_un_listing():
    rendu = str(render_statement(
        "\\begin{lstlisting}\n</code></pre><script>alert(1)</script>\n\\end{lstlisting}"))
    assert "<script>" not in rendu
    assert "&lt;script&gt;" in rendu
    # une seule ouverture et une seule fermeture de bloc
    assert rendu.count("<pre") == 1 and rendu.count("</pre>") == 1


def test_l_option_de_langage_est_reconnue_sans_etre_affichee():
    rendu = str(render_statement(
        "\\begin{lstlisting}[language=Python]\nx = 1\n\\end{lstlisting}"))
    assert "code-python" in rendu
    assert "language=Python" not in rendu
    assert "[language" not in rendu


def test_un_contenu_declare_sans_langage_ne_recoit_aucune_classe_de_langage():
    """« [language={}] » signale un extrait de fichier, pas du code."""
    rendu = str(render_statement(
        "\\begin{lstlisting}[language={}]\nid,date,valeur\nC07,2026-08-24,26.5\n"
        "\\end{lstlisting}"))
    assert 'class="code-bloc"' in rendu
    assert "code-python" not in rendu
    assert "id,date,valeur" in rendu


def test_le_contenu_d_un_listing_n_est_pas_transforme():
    """Verbatim : une commande LaTeX dans du code reste du texte."""
    rendu = str(render_statement(
        "\\begin{lstlisting}\ns = \"\\\\textbf{gras}\"\nt = \"$x$\"\n\\end{lstlisting}"))
    bloc = rendu[rendu.index("<code>"):rendu.index("</code>")]
    assert "<strong>" not in bloc
    assert "textbf{gras}" in bloc
    assert "$x$" in bloc


# ============================================================ 2. tabularx
TABLEAU_REEL = (
    "\\par\\noindent\\begin{tabularx}{\\linewidth}{|>{\\bfseries}p{16mm}|X|X|X|X|}\n"
    "\\hline\n"
    "Après le tour & 1 & 2 & 3 & 4 \\\\ \\hline\n"
    "\\code{total} & & & & \\\\ \\hline\n"
    "\\code{n} & & & & \\\\ \\hline\n"
    "\\end{tabularx}")


def test_le_tableau_du_corpus_devient_un_vrai_tableau():
    rendu = str(render_statement(TABLEAU_REEL))
    assert '<table class="enonce-tableau">' in rendu
    assert rendu.count("<tr>") == 3          # un en-tête, deux lignes
    assert rendu.count("<th>") == 5          # cinq colonnes d'en-tête
    assert rendu.count('<th scope="row">') == 2
    assert rendu.count("<td>") == 8          # deux lignes de quatre cellules vides
    assert "Après le tour" in rendu
    assert "<code>total</code>" in rendu


def test_les_cellules_vides_restent_visibles():
    """L'élève les remplit sur le papier ; elles doivent rester lisibles à l'écran."""
    rendu = str(render_statement(TABLEAU_REEL))
    assert rendu.count("&nbsp;") == 8


def test_les_maths_d_une_cellule_restent_disponibles_pour_katex():
    tableau = ("\\begin{tabularx}{\\linewidth}{|X|X|}\n\\hline\n"
               "Valeur & Résultat \\\\ \\hline\n"
               "$x^2$ & $4$ \\\\ \\hline\n\\end{tabularx}")
    rendu = str(render_statement(tableau))
    assert "<table" in rendu
    assert "$x^2$" in rendu and "$4$" in rendu


def test_un_tableau_irregulier_bascule_sur_le_repli():
    """Nombre de cellules variable : on renvoie au PDF plutôt que de deviner."""
    tableau = ("\\begin{tabularx}{\\linewidth}{|X|X|X|}\n\\hline\n"
               "A & B & C \\\\ \\hline\n"
               "1 & 2 \\\\ \\hline\n\\end{tabularx}")
    rendu = str(render_statement(tableau))
    assert "<table" not in rendu
    assert FALLBACK_TEXTE in rendu


def test_une_commande_inconnue_dans_une_cellule_bascule_sur_le_repli():
    tableau = ("\\begin{tabularx}{\\linewidth}{|X|X|}\n\\hline\n"
               "A & B \\\\ \\hline\n"
               "\\multicolumn{2}{c}{fusion} & \\\\ \\hline\n\\end{tabularx}")
    rendu = str(render_statement(tableau))
    assert FALLBACK_TEXTE in rendu
    assert "multicolumn" not in rendu


# ============================================================ 3. repli général
def test_une_structure_inconnue_n_apparait_jamais_en_latex_brut():
    """§7 — jamais de \\begin{...} silencieux dans l'interface."""
    rendu = str(render_statement(
        "Avant.\n\\begin{minipage}{0.5\\linewidth}\nContenu\n\\end{minipage}\nAprès."))
    assert "\\begin{minipage}" not in rendu
    assert "minipage" not in rendu
    assert FALLBACK_TEXTE in rendu
    assert "Avant." in rendu and "Après." in rendu


def test_un_delimiteur_orphelin_est_retire():
    rendu = str(render_statement("Texte \\begin{center} sans fermeture."))
    assert "\\begin{" not in rendu
    assert "Texte" in rendu


def test_le_repli_est_annonce_par_l_inventaire():
    assert unsupported_structures("\\begin{minipage}{x}a\\end{minipage}") == ["minipage"]
    assert unsupported_structures(TABLEAU_REEL) == []
    assert unsupported_structures("\\begin{lstlisting}\nx=1\n\\end{lstlisting}") == []


# ================================================ 4. corpus NSI réel (§8)
def _manifestes_nsi():
    racine = Path(config.CLOTURE_ROOT) / "1re_nsi"
    return sorted(racine.glob("*/*/_ENSEIGNANT/evaluation_manifest.json"))


def test_le_corpus_nsi_est_bien_present():
    manifestes = _manifestes_nsi()
    assert len(manifestes) == 2, "Ahmad BELDI et Ahmed BENHADJ SALEM"


@pytest.mark.parametrize("manifeste", _manifestes_nsi(), ids=lambda p: p.parts[-3])
def test_aucun_enonce_nsi_ne_laisse_de_latex_brut(manifeste):
    """Le contrôle qui compte : après rendu, plus rien d'illisible à l'écran."""
    donnees = json.loads(manifeste.read_text(encoding="utf-8"))
    for item in donnees["items"]:
        rendu = str(render_statement(item.get("statement")))
        for sequence in SEQUENCES_INTERDITES:
            assert sequence not in rendu, (item["item_id"], sequence)
        rendu_reponse = str(render_statement(item.get("expected_answer")))
        for sequence in SEQUENCES_INTERDITES:
            assert sequence not in rendu_reponse, (item["item_id"], sequence)


@pytest.mark.parametrize("manifeste", _manifestes_nsi(), ids=lambda p: p.parts[-3])
def test_les_enonces_nsi_produisent_du_code_et_un_tableau(manifeste):
    donnees = json.loads(manifeste.read_text(encoding="utf-8"))
    rendus = [str(render_statement(i.get("statement"))) for i in donnees["items"]]
    complet = "\n".join(rendus)
    assert complet.count("<pre class=\"code-bloc") >= 4
    assert '<table class="enonce-tableau">' in complet
    # aucun repli n'est nécessaire sur ce corpus : tout est converti
    assert FALLBACK_TEXTE not in complet


@pytest.mark.parametrize("manifeste", _manifestes_nsi(), ids=lambda p: p.parts[-3])
def test_aucune_balise_active_n_est_introduite(manifeste):
    donnees = json.loads(manifeste.read_text(encoding="utf-8"))
    autorisees = {"p", "ol", "li", "strong", "em", "code", "pre", "table", "thead",
                  "tbody", "tr", "th", "td", "span"}
    for item in donnees["items"]:
        rendu = str(render_statement(item.get("statement")))
        for balise in re.findall(r"</?([a-zA-Z][a-zA-Z0-9]*)", rendu):
            assert balise.lower() in autorisees, (item["item_id"], balise)


# ============================================ 5. intégration web des deux NSI
@pytest.mark.parametrize("student_id", NSI_ELEVES)
def test_la_page_nsi_ne_montre_aucun_latex_brut(client, student_id):
    page = client.get("/eleve/%s" % student_id).text
    assert page.count('id="item-') > 0
    for sequence in ("\\begin{lstlisting}", "\\end{lstlisting}", "\\begin{tabularx}",
                     "\\begin{enumerate}", "\\item", "\\code{"):
        assert sequence not in page, sequence


@pytest.mark.parametrize("student_id", NSI_ELEVES)
def test_la_page_nsi_affiche_le_code_et_le_pdf(client, student_id):
    page = client.get("/eleve/%s" % student_id).text
    assert 'class="code-bloc' in page
    # le PDF distribué reste accessible : c'est ce qui rend le repli acceptable
    assert "/document/%s/evaluation" % student_id in page
    assert 'class="pdf-frame"' in page


def test_le_tableau_d_etat_est_rendu_pour_ahmad_beldi(client):
    page = client.get("/eleve/ahmad-beldi-nsi").text
    assert '<table class="enonce-tableau">' in page
    assert "Après le tour" in page


@pytest.mark.parametrize("student_id", NSI_ELEVES)
def test_le_css_du_code_est_local(client, student_id):
    css = client.get("/static/app.css").text
    assert ".code-bloc" in css
    assert ".enonce-tableau" in css
    assert ".latex-repli" in css
    page = client.get("/eleve/%s" % student_id).text
    for attribut, valeur in re.findall(r'\b(src|href)\s*=\s*"([^"]*)"', page):
        assert not valeur.startswith(("http://", "https://", "//")), (attribut, valeur)


# =================================================== 6. non-régression maths
def test_les_niveaux_non_nsi_ne_sont_pas_affectes():
    """Un énoncé de mathématiques rend exactement comme avant cette passe."""
    rendu = str(render_statement(
        "\\begin{enumerate}\n\\item Développer $5(x - 3)$.\n"
        "\\item Réduire ensuite $5(x - 3) + 2x + 7$.\n\\end{enumerate}"))
    assert rendu == ('<ol class="enonce-liste">'
                     "<li>Développer $5(x - 3)$.</li>"
                     "<li>Réduire ensuite $5(x - 3) + 2x + 7$.</li></ol>")


def test_textbf_hors_math_reste_converti():
    rendu = str(render_statement("\\textbf{L'atelier de peinture.} Un mur."))
    assert "<strong>L'atelier de peinture.</strong>" in rendu
