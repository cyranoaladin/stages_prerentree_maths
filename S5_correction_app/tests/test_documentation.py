# -*- coding: utf-8 -*-
"""Les dettes scientifiques restent dans la documentation enseignant.

Elles ne doivent pas se retrouver dans une conclusion adressée à un élève ou à une
famille : ce sont des points de vigilance de support, pas des jugements sur la copie.
"""

from pathlib import Path

import pytest

from app import config

CLARIFICATIONS = Path(config.V3_ROOT) / "teacher_guidance" / "CLARIFICATIONS_ORALES_S5.md"

SUJETS = [
    ("somme de deux carrés", "somme"),
    ("équation-produit", "produit nul"),
    ("droites verticales", "verticale"),
    ("range", "range(a, b, p)"),
    ("variant de boucle", "variant"),
]


@pytest.mark.skipif(not CLARIFICATIONS.exists(), reason="couche V3 absente")
@pytest.mark.parametrize("sujet,motif", SUJETS)
def test_les_clarifications_sont_documentees_pour_l_enseignant(sujet, motif):
    texte = CLARIFICATIONS.read_text(encoding="utf-8")
    assert motif in texte, sujet
    assert "strictement enseignant" in texte.lower()


@pytest.mark.skipif(not CLARIFICATIONS.exists(), reason="couche V3 absente")
def test_les_clarifications_ne_sont_pas_reprises_dans_les_textes_eleves():
    from app.domain import narrative
    generator = narrative.DeterministicNarrativeGenerator()
    source = Path(config.APP_DIR, "domain", "narrative.py").read_text(encoding="utf-8")
    for interdit in ("somme de deux carrés", "produit nul", "variant de boucle",
                     "range(a, b, p)"):
        assert interdit not in source, interdit
    assert generator.name == "deterministic"


def test_la_limite_scientifique_est_affichee_dans_l_application():
    from app.domain import analysis as ana
    assert "aucune progression chiffrée" in ana.DELTA_BLOCKED_REASON.lower()
    modele = Path(config.TEMPLATES_DIR, "analysis.html").read_text(encoding="utf-8")
    assert "delta_blocked_reason" in modele


def test_la_documentation_de_l_application_existe():
    docs = Path(config.PROJECT_DIR) / "docs"
    for nom in ("INITIAL_INTEGRATION_AUDIT.md",):
        assert (docs / nom).exists(), nom
