"""Garde-fous du cahier de séances nominatif.

Ces tests existent à cause de ce qu'un balayage visuel a trouvé et que rien d'autre n'avait
vu : des exercices de la piste excellence dans le cahier d'un élève en remédiation, un
décalage d'exercices calculé sur le mauvais domaine, un cahier qui parlait d'un
positionnement qui n'avait pas eu lieu. Trois défauts pédagogiques, invisibles à la
compilation, invisibles aux tests de l'époque, et qui auraient donné à un élève un travail
qui n'était pas le sien.

Ce qui est vérifié ici tient en une phrase : **le contenu d'un cahier doit se déduire du
bilan de son élève, et de rien d'autre.**
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from tools.build_terminale import (  # noqa: E402
    MODULES,
    build_documents,
    domains_to_fix,
    session_focus,
)
from build_seances import (  # noqa: E402
    ETAYAGE,
    PISTE_BLOCKS,
    entry_point,
    read_sheet,
    theme_domain,
    trim_exercises,
)
from seance_bank import BANK, COMPLEMENTS  # noqa: E402


@pytest.fixture(scope="module")
def documents() -> dict[str, str]:
    return build_documents()


@pytest.fixture(scope="module")
def cahiers(documents) -> dict[str, str]:
    """Les cahiers produits, indexés par leur chemin."""
    return {path: text for path, text in documents.items() if "_Cahier_Seances_" in path}


@pytest.fixture(scope="module")
def registry() -> dict:
    return json.loads((ROOT / "content/students_terminale.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def diagnostics() -> dict:
    path = ROOT / "content/diagnostics_terminale.json"
    return json.loads(path.read_text(encoding="utf-8"))["diagnostics"]


# --- couverture ---------------------------------------------------------------------

def test_chaque_eleve_inscrit_recoit_un_cahier_par_matiere(cahiers, registry):
    attendus = set()
    for student in registry["students"]:
        if not student.get("active", True):
            continue
        for subject in list(student.get("matieres", [])) + list(
                student.get("matieresSansDiagnostic", [])):
            module = MODULES[subject["module"]]
            attendus.add(f"{module.key}/{module.nominative_dir}/{student['slug']}"
                         f"/{module.key}_Cahier_Seances_{student['slug']}.md")
    assert attendus == set(cahiers), sorted(attendus ^ set(cahiers))


def test_chaque_cahier_couvre_les_cinq_seances(cahiers):
    for path, text in cahiers.items():
        numeros = [int(n) for n in re.findall(r"^# Séance (\d+) —", text, re.M)]
        assert numeros == [1, 2, 3, 4, 5], f"{path} : séances {numeros}"


def test_la_banque_couvre_toutes_les_seances_de_tous_les_modules():
    attendu = {(key, number) for key, module in MODULES.items()
               for number, _theme in module.sessions}
    assert set(BANK) == attendu, sorted(set(BANK) ^ attendu)
    assert set(COMPLEMENTS) == attendu, sorted(set(COMPLEMENTS) ^ attendu)


# --- ce que le balayage visuel avait trouvé -----------------------------------------

def test_les_exercices_de_la_piste_excellence_ne_vont_qu_aux_eleves_de_cette_piste(
        cahiers, registry, diagnostics):
    """Le défaut le plus grave trouvé à l'œil : la séance 5 de mathématiques n'est pas
    découpée en pistes, et sa reprise par thème laissait passer le bloc « Partie 3 bis —
    Exercices 9 et 10, piste Excellence ». Un élève en remédiation recevait un problème de
    type bac au milieu de sa séance."""
    marqueurs = {
        "tle_spe": "urne contient n boules rouges",       # exercice 10, séance 5
        "tle_nsi": "association gère ses adhérents",      # transfert de la séance 5
    }
    for student in registry["students"]:
        if not student.get("active", True):
            continue
        for subject in student.get("matieres", []):
            module = MODULES[subject["module"]]
            marqueur = marqueurs.get(module.key)
            if marqueur is None:
                continue
            chemin = (f"{module.key}/{module.nominative_dir}/{student['slug']}"
                      f"/{module.key}_Cahier_Seances_{student['slug']}.md")
            rows = session_focus(diagnostics[subject["diagnosticId"]], module)
            piste5 = next(r["parcours"] for r in rows if r["seance"] == 5)
            presente = marqueur in cahiers[chemin]
            if module.key == "tle_spe":
                assert presente == (piste5 == "Excellence"), (
                    f"{student['displayName']} est en piste {piste5} en séance 5 et "
                    f"{'reçoit' if presente else 'ne reçoit pas'} l'exercice d'excellence")


def test_le_decalage_du_point_d_entree_suit_le_domaine_des_exercices():
    """Le décalage était calculé sur la réussite du domaine travaillé en temps différencié,
    puis appliqué aux exercices du thème de la séance. Un élève à 0 % sur l'exponentielle
    sautait une application directe d'exponentielle parce qu'il avait 43 % sur les suites."""
    scores = {"Suites numériques": 42.9, "Fonction exponentielle": 0.0}
    theme = "Fonction exponentielle : exposants, équations, vers le logarithme"
    assert theme_domain(theme, scores) == "Fonction exponentielle"
    assert entry_point(scores[theme_domain(theme, scores)]) == 0


def test_le_decalage_ne_s_applique_pas_a_la_piste_confronter(cahiers):
    """Un élève sûr de lui et faux a besoin de la reconstruction complète : son taux de
    réussite ne dit pas qu'il maîtrise l'accès, il dit qu'une partie de ce qu'il croit
    savoir est juste."""
    message = "premier(s) exercice(s) d'application directe"
    for path, text in cahiers.items():
        for bloc in re.split(r"^# Séance ", text, flags=re.M)[1:]:
            if message not in bloc:
                continue
            piste = re.search(r"\*\*Ta piste :\*\* (\w+)", bloc)
            assert piste and piste.group(1) == "Installer", (
                f"{path} : décalage appliqué sur la piste "
                f"{piste.group(1) if piste else '?'}")


def test_un_cahier_sans_positionnement_n_invoque_aucun_positionnement(cahiers, registry):
    """« Non évalué » n'est pas « non maîtrisé », et un positionnement qui n'a pas eu lieu
    ne peut rien avoir montré."""
    for student in registry["students"]:
        for missing in student.get("matieresSansDiagnostic", []):
            module = MODULES[missing["module"]]
            chemin = (f"{module.key}/{module.nominative_dir}/{student['slug']}"
                      f"/{module.key}_Cahier_Seances_{student['slug']}.md")
            texte = cahiers[chemin]
            assert "ton positionnement a montré" not in texte
            assert "ils viennent de ton positionnement" not in texte
            assert "Tu n'as pas passé le positionnement" in texte


def test_un_domaine_sans_reponse_n_affiche_pas_un_taux_de_reussite(cahiers):
    """Le taux de réussite d'un domaine laissé sans réponse vaut zéro, et ce zéro ne mesure
    rien. L'écrire annoncerait un échec là où il n'y a aucune information."""
    for path, text in cahiers.items():
        for bloc in re.split(r"^# Séance ", text, flags=re.M)[1:]:
            if "(DIAGNOSTIQUER)" not in bloc:
                continue
            assert "tu as réussi" not in bloc, (
                f"{path} : un taux de réussite est affiché sur un domaine non évalué")
            assert "restées sans réponse" in bloc


# --- individualisation ---------------------------------------------------------------

def test_l_etayage_depend_de_la_posture_et_non_du_niveau_suppose(cahiers):
    """Un exemple résolu donné à un élève qui réussit déjà lui retire le travail attendu ;
    refusé à un élève qui en a besoin, il le laisse sans prise."""
    for path, text in cahiers.items():
        for bloc in re.split(r"^# Séance ", text, flags=re.M)[1:]:
            piste = re.search(r"\*\*Ta piste :\*\* (\w+)", bloc)
            if not piste:
                continue
            exemple_attendu, indices_attendus, _confrontation, _redaction = ETAYAGE[
                piste.group(1)]
            if not exemple_attendu:
                assert "## Un exemple mené jusqu'au bout" not in bloc, (
                    f"{path} : exemple résolu donné en piste {piste.group(1)}")
            if not indices_attendus:
                assert "### Si tu bloques" not in bloc, (
                    f"{path} : indices gradués donnés en piste {piste.group(1)}")


def test_les_exercices_personnels_couvrent_tout_ce_que_le_bilan_signale(
        cahiers, registry, diagnostics):
    """Aucune priorité du bilan ne doit rester sans exercice d'ici la séance 5."""
    for student in registry["students"]:
        if not student.get("active", True):
            continue
        for subject in student.get("matieres", []):
            module = MODULES[subject["module"]]
            diagnostic = diagnostics[subject["diagnosticId"]]
            if not domains_to_fix(diagnostic):
                continue
            chemin = (f"{module.key}/{module.nominative_dir}/{student['slug']}"
                      f"/{module.key}_Cahier_Seances_{student['slug']}.md")
            texte = cahiers[chemin]
            for domaine in domains_to_fix(diagnostic):
                assert domaine in texte, (
                    f"{student['displayName']} — {subject['matiere']} : le domaine "
                    f"« {domaine} » est signalé au bilan et absent du cahier")


def test_la_reprise_espacee_rappelle_un_domaine_deux_seances_plus_tard(cahiers):
    """Une réussite le jour même ne prouve pas qu'une notion est installée."""
    rappels = sum(len(re.findall(r"Tu as travaillé \*\*", text)) for text in cahiers.values())
    assert rappels >= 10, f"{rappels} rappel(s) différé(s) seulement"


# --- mécanique du découpage ----------------------------------------------------------

def test_chaque_fiche_collective_offre_les_blocs_de_toutes_les_pistes():
    """Si une fiche perd un bloc de piste, les élèves de cette piste se retrouvent avec la
    reprise par thème — c'est-à-dire le contenu des autres."""
    for key, module in MODULES.items():
        for number, _theme in module.sessions:
            parts = read_sheet(key, number, ROOT)
            disponibles = {piste for piste in PISTE_BLOCKS if f"piste:{piste}" in parts}
            assert disponibles or parts.get("thematiques"), (
                f"{key}/S{number} : ni bloc de piste, ni reprise par thème")


def test_le_decoupage_ne_reprend_jamais_un_bloc_reserve_a_une_piste():
    for key, module in MODULES.items():
        for number, _theme in module.sessions:
            thematiques = read_sheet(key, number, ROOT).get("thematiques", "")
            for interdit in ("xcellence", "Évaluation finale", "Carte de sortie"):
                assert interdit not in thematiques, (
                    f"{key}/S{number} : « {interdit} » repris dans le contenu commun")


def test_retirer_des_exercices_laisse_toujours_de_quoi_travailler():
    bloc = "\n".join(f"**Exercice {n}.** Énoncé {n}.\n" for n in range(1, 5))
    assert trim_exercises(bloc, 0) == (bloc, 0)
    _reste, retires = trim_exercises(bloc, 2)
    assert retires == 2
    # On ne vide jamais la série : trois exercices retirés sur quatre laisserait un seul
    # énoncé, et le décalage perdrait son sens.
    assert trim_exercises(bloc, 3) == (bloc, 0)


@pytest.mark.parametrize("reussite,attendu", [
    (None, 0), (0.0, 0), (39.9, 0), (40.0, 1), (69.9, 1), (70.0, 2), (100.0, 2),
])
def test_le_point_d_entree_suit_des_seuils_explicites(reussite, attendu):
    assert entry_point(reussite) == attendu


# --- rendu LaTeX : ce qui doit rester du code -------------------------------------
# Une fiche Python à trous — « u = .......... » — est passée en production avec la
# commande LaTeX écrite en toutes lettres dans le code : \rule n'est pas interprété en
# verbatim. Trente blocs, dans les fiches collectives comme dans les cahiers d'élèves.
# Rien ne le voyait : ni la compilation, qui réussit, ni le contrôle de densité, qui
# compte des caractères.

def test_les_files_de_points_deviennent_des_filets_hors_du_code():
    from tools.build_terminale_pdf import rule_dotted_runs
    rendu = rule_dotted_runs(r"Réponse : .......... fin")
    assert r"\rule" in rendu
    assert "........" not in rendu


@pytest.mark.parametrize("environnement", ["lstlisting", "verbatim", "Shaded"])
def test_les_files_de_points_restent_des_points_dans_le_code(environnement):
    from tools.build_terminale_pdf import rule_dotted_runs
    source = ("\\begin{%s}\nu = ..........\n\\end{%s}" % (environnement, environnement))
    assert rule_dotted_runs(source) == source


def test_un_document_melangeant_code_et_prose_traite_chaque_partie_selon_sa_nature():
    from tools.build_terminale_pdf import rule_dotted_runs
    rendu = rule_dotted_runs(
        "Avant ..........\n"
        r"\begin{lstlisting}[language=Python]" "\nu = ..........\n" r"\end{lstlisting}"
        "\nAprès ..........")
    assert rendu.count(r"\rule") == 2, "la prose doit porter deux filets"
    assert rendu.count("..........") == 1, "le code doit garder ses points"


def test_aucun_bloc_de_code_du_corpus_ne_sort_avec_une_commande_latex_dans_le_code():
    """Le contrôle de bout en bout, sur les sources réelles."""
    from tools.build_terminale_pdf import rule_dotted_runs
    fence = re.compile(r"^```.*?^```", re.M | re.S)
    vus = 0
    for chemin in sorted(ROOT.glob("tle_*/**/*.md")):
        for bloc in fence.finditer(chemin.read_text(encoding="utf-8")):
            if "........" not in bloc.group(0):
                continue
            vus += 1
            latex = "\\begin{lstlisting}\n" + bloc.group(0) + "\n\\end{lstlisting}"
            assert r"\rule" not in rule_dotted_runs(latex), (
                f"{chemin.relative_to(ROOT)} : un trou de code deviendrait une commande "
                f"LaTeX imprimée en toutes lettres")
    assert vus >= 20, f"seulement {vus} blocs de code à trous trouvés : le corpus a changé"


# --- index des modules : aucun lien ne doit pointer dans le vide -------------------
# Le générateur branchait sur la clé du module au lieu d'employer les champs prévus
# (`diagnostic_prefix`, `portfolio_dir`, `extra_portfolio`). La physique-chimie héritait
# donc de la forme de NSI, et son index proposait quatre documents qui n'existent pas —
# dont un mini-diagnostic « pratique » et un mémento Python. Le mémento de formules, lui,
# n'était lié nulle part.

LIEN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@pytest.mark.parametrize("module", ["tle_spe", "tle_nsi", "tle_pc"])
def test_aucun_lien_mort_dans_l_index_d_un_module(module):
    index = ROOT / module / "00_MASTER" / "index.md"
    morts = []
    for cible in LIEN.findall(index.read_text(encoding="utf-8")):
        if cible.startswith(("http://", "https://", "#")):
            continue
        chemin = (index.parent / cible.split("#")[0]).resolve()
        if not chemin.exists():
            morts.append(cible)
    assert not morts, f"{index.relative_to(ROOT)} : liens morts {morts}"


@pytest.mark.parametrize("module,memento", [
    ("tle_nsi", "Memento_Python"),
    ("tle_pc", "Memento_Formules"),
])
def test_le_memento_que_l_eleve_emporte_est_lie_depuis_l_index(module, memento):
    """C'est le seul document destiné à servir après le stage : il doit se trouver."""
    index = (ROOT / module / "00_MASTER" / "index.md").read_text(encoding="utf-8")
    assert memento in index, f"{module} : le mémento n'est lié depuis aucun index"


def test_l_index_mene_a_la_note_de_remise_et_au_guide_d_impression():
    for module in ("tle_spe", "tle_nsi", "tle_pc"):
        index = (ROOT / module / "00_MASTER" / "index.md").read_text(encoding="utf-8")
        assert "PRINT_GUIDE_TERMINALE.md" in index, f"{module} : guide d'impression absent"
        assert "terminale-livraison" in index, f"{module} : note de remise absente"
