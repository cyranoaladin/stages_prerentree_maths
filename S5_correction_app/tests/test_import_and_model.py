# -*- coding: utf-8 -*-
"""Import du référentiel V3 et modèle de données."""

from app.models import (Assessment, CriterionDefinition, ItemDefinition, Person, Student,
                        VirtualCriterionDefinition)


def test_quinze_couples_eleve_matiere(session):
    assert session.query(Student).count() == 15
    assert session.query(Assessment).count() == 15


def test_le_nom_n_est_pas_une_cle(session):
    """Ahmad BELDI suit deux matières : une personne, deux couples élève × matière."""
    assert session.query(Person).count() == 14
    beldi = session.query(Person).filter_by(display_name="Ahmad BELDI").one()
    matieres = sorted(s.subject for s in beldi.students)
    assert matieres == ["Mathématiques", "NSI"]
    assert sorted(s.student_id for s in beldi.students) == ["ahmad-beldi-maths",
                                                            "ahmad-beldi-nsi"]


def test_le_referentiel_importe_est_complet(session):
    assert session.query(ItemDefinition).count() == 180
    assert session.query(CriterionDefinition).count() == 337
    # 6 sous-critères issus de la couche V3, plus 2 créés par la revue curriculaire
    # d'Inès sur A3 — voir docs/INES_CURRICULUM_MATRIX.md. Le nombre de critères
    # imprimés, lui, ne bouge pas : c'est ce que garantit la ligne précédente.
    assert session.query(VirtualCriterionDefinition).count() == 8


def test_chaque_critere_porte_un_scope(session):
    scopes = {c.curriculum_scope for c in session.query(CriterionDefinition).all()}
    assert scopes <= {"n_minus_1", "bridge_n", "mixed"}
    assert not session.query(CriterionDefinition).filter(
        CriterionDefinition.curriculum_scope.is_(None)).count()


def test_un_critere_mixte_est_eclate_a_somme_constante(session):
    """L'invariant porte sur chaque critère mixte, quel qu'en soit le nombre.

    Le compte est passé de 3 à 4 lorsque la revue curriculaire d'Inès a déclaré mixte
    la réduction de A3. C'est la garantie — somme constante, aucune duplication — qui
    doit tenir, pas un effectif figé : elle est donc vérifiée sur tous les mixtes, et
    le total des points de chaque évaluation est contrôlé en plus.
    """
    mixtes = session.query(CriterionDefinition).filter_by(curriculum_scope="mixed").all()
    assert len(mixtes) >= 3
    vus = set()
    for crit in mixtes:
        parts = crit.virtual_parts
        assert len(parts) >= 2
        assert sum(p.max_score_centi for p in parts) == crit.max_score_centi
        assert {p.curriculum_scope for p in parts} <= {"n_minus_1", "bridge_n"}
        for part in parts:
            assert part.virtual_criterion_id not in vus, "sous-critère dupliqué"
            vus.add(part.virtual_criterion_id)
        assert crit.criterion_id not in vus, "le critère mixte ne se note pas lui-même"


def test_les_deux_pools_recomposent_vingt_points(session):
    for assessment in session.query(Assessment).all():
        assert assessment.max_points_centi == 2000
        total = (assessment.n_minus_1_available_centi + assessment.bridge_available_centi)
        assert total == 2000, assessment.student_id


def test_les_alias_analytiques_sont_importes(session):
    ids = {c.analysis_skill_id for c in session.query(CriterionDefinition).all()}
    assert "M3_TRIGO_COS_NM1" in ids
    assert "M3_TRIGO_SIN_BRIDGE" in ids
    assert "M4E_REL_PROD_BRIDGE" in ids
    cos = session.query(CriterionDefinition).filter_by(
        analysis_skill_id="M3_TRIGO_COS_NM1").first()
    sin = session.query(CriterionDefinition).filter_by(
        analysis_skill_id="M3_TRIGO_SIN_BRIDGE").first()
    assert cos.curriculum_scope == "n_minus_1"
    assert sin.curriculum_scope == "bridge_n"
    assert cos.original_skill_id == sin.original_skill_id == "M3E_TRIG_01"
