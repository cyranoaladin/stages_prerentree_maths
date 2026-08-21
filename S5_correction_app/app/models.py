# -*- coding: utf-8 -*-
"""Modèle de données.

Trois décisions structurantes, toutes prises à l'audit et justifiées là :

* le nom n'est jamais une clé. Ahmad BELDI est une *personne* inscrite à deux couples
  élève × matière distincts ; ``person_id``, ``student_id`` et ``assessment_id`` sont
  des identifiants stables et indépendants du nom affiché ;
* les points sont des entiers en **centièmes de point**. Le barème distribué contient
  0,3 / 0,4 / 0,6 / 0,7, qui ne sont pas des quarts ; le centième est la plus grande
  unité qui représente tout le barème sans arrondi. Aucun flottant n'intervient ;
* rien n'est jamais écrasé. Une correction validée puis rouverte crée une révision ; un
  rapport régénéré crée une version. L'historique n'est pas effaçable depuis l'interface.
"""

import datetime as dt

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String, Text,
                        UniqueConstraint, Index)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def utcnow():
    return dt.datetime.now(dt.timezone.utc)


# --------------------------------------------------------------------- méta
class AppMeta(Base):
    __tablename__ = "app_meta"
    key = Column(String(64), primary_key=True)
    value = Column(String(255), nullable=False)


class ImportSource(Base):
    """Ce qui a été importé, d'où, et dans quel état la source se trouvait alors."""
    __tablename__ = "import_source"
    id = Column(Integer, primary_key=True)
    source_path = Column(String(512), nullable=False)
    source_sha256 = Column(String(64), nullable=False)
    schema_version = Column(String(64), nullable=False)
    kind = Column(String(64), nullable=False)
    imported_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    __table_args__ = (Index("ix_import_source_path", "source_path"),)


# ------------------------------------------------------------------ personnes
class Person(Base):
    """Un être humain. Peut suivre plusieurs matières."""
    __tablename__ = "person"
    person_id = Column(String(64), primary_key=True)
    display_name = Column(String(128), nullable=False)
    students = relationship("Student", back_populates="person")


class Student(Base):
    """Un couple personne × niveau × matière. C'est l'unité de travail réelle."""
    __tablename__ = "student"
    student_id = Column(String(64), primary_key=True)
    person_id = Column(String(64), ForeignKey("person.person_id"), nullable=False)
    level_key = Column(String(32), nullable=False)
    level_label = Column(String(160), nullable=False)
    subject = Column(String(64), nullable=False)
    person = relationship("Person", back_populates="students")
    assessments = relationship("Assessment", back_populates="student")


class Assessment(Base):
    """L'évaluation de clôture réellement distribuée à ce couple."""
    __tablename__ = "assessment"
    assessment_id = Column(String(64), primary_key=True)
    student_id = Column(String(64), ForeignKey("student.student_id"), nullable=False)
    subject = Column(String(64), nullable=False)
    level_key = Column(String(32), nullable=False)
    evaluation_pdf_path = Column(String(512), nullable=False)
    evaluation_pdf_sha256 = Column(String(64), nullable=False)
    travail_pdf_path = Column(String(512), nullable=False)
    travail_pdf_sha256 = Column(String(64), nullable=False)
    distributed_on = Column(String(32), nullable=True)
    max_points_centi = Column(Integer, nullable=False)
    n_minus_1_available_centi = Column(Integer, nullable=False)
    bridge_available_centi = Column(Integer, nullable=False)
    estimated_duration_minutes = Column(Integer, nullable=True)
    status = Column(String(32), nullable=False, default="NOT_STARTED")
    student = relationship("Student", back_populates="assessments")
    items = relationship("ItemDefinition", back_populates="assessment",
                         order_by="ItemDefinition.position")
    corrections = relationship("Correction", back_populates="assessment",
                               order_by="Correction.revision")


class ItemDefinition(Base):
    __tablename__ = "item_definition"
    item_id = Column(String(96), primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    ref = Column(String(16), nullable=False)
    position = Column(Integer, nullable=False)
    part = Column(String(4), nullable=False)
    kind = Column(String(16), nullable=False)
    statement = Column(Text, nullable=False)
    max_points_centi = Column(Integer, nullable=False)
    expected_answer = Column(Text, nullable=True)
    significant_steps_json = Column(Text, nullable=True)
    likely_errors_json = Column(Text, nullable=True)
    accepted_methods_json = Column(Text, nullable=True)
    teacher_observation_non_scored_json = Column(Text, nullable=True)
    confidence_probe = Column(Boolean, nullable=False, default=False)
    comparison_status = Column(String(48), nullable=True)
    estimated_duration_minutes_centi = Column(Integer, nullable=True)
    assessment = relationship("Assessment", back_populates="items")
    criteria = relationship("CriterionDefinition", back_populates="item",
                            order_by="CriterionDefinition.rank")


class CriterionDefinition(Base):
    __tablename__ = "criterion_definition"
    criterion_id = Column(String(128), primary_key=True)
    item_id = Column(String(96), ForeignKey("item_definition.item_id"), nullable=False)
    rank = Column(Integer, nullable=False)
    subpart = Column(String(16), nullable=True)
    description = Column(Text, nullable=False)
    max_score_centi = Column(Integer, nullable=False)
    original_skill_id = Column(String(64), nullable=False)
    analysis_skill_id = Column(String(64), nullable=False)
    analysis_skill_label = Column(String(255), nullable=True)
    curriculum_scope = Column(String(16), nullable=False)   # n_minus_1 | bridge_n | mixed
    evidence_type = Column(String(32), nullable=False)
    evidence_quality = Column(String(32), nullable=False, default="standard")
    scope_rationale = Column(Text, nullable=True)
    accepted_methods_json = Column(Text, nullable=True)
    interpretation_limits_json = Column(Text, nullable=True)
    fairness_rules_json = Column(Text, nullable=True)
    error_codes_allowed_json = Column(Text, nullable=True)
    printed_prompt = Column(Text, nullable=True)
    proof_levels_json = Column(Text, nullable=True)
    teacher_correction = Column(Text, nullable=True)
    rejected_json = Column(Text, nullable=True)
    retention_json = Column(Text, nullable=True)
    item = relationship("ItemDefinition", back_populates="criteria")
    virtual_parts = relationship("VirtualCriterionDefinition", back_populates="criterion",
                                 order_by="VirtualCriterionDefinition.rank")


class VirtualCriterionDefinition(Base):
    """Sous-critère analytique d'un critère mixte. N'existe pas sur le sujet papier."""
    __tablename__ = "virtual_criterion_definition"
    virtual_criterion_id = Column(String(160), primary_key=True)
    criterion_id = Column(String(128), ForeignKey("criterion_definition.criterion_id"),
                          nullable=False)
    rank = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    max_score_centi = Column(Integer, nullable=False)
    analysis_skill_id = Column(String(64), nullable=False)
    analysis_skill_label = Column(String(255), nullable=True)
    curriculum_scope = Column(String(16), nullable=False)   # n_minus_1 | bridge_n
    criterion = relationship("CriterionDefinition", back_populates="virtual_parts")


class SkillReference(Base):
    """Libellé, domaine et importance d'une compétence d'analyse."""
    __tablename__ = "skill_reference"
    id = Column(Integer, primary_key=True)
    level_key = Column(String(32), nullable=False)
    analysis_skill_id = Column(String(64), nullable=False)
    label = Column(String(255), nullable=False)
    domain = Column(String(96), nullable=True)
    importance_n = Column(String(32), nullable=True)
    curriculum_scope = Column(String(16), nullable=False)
    is_alias = Column(Boolean, nullable=False, default=False)
    original_skill_ids_json = Column(Text, nullable=True)
    __table_args__ = (UniqueConstraint("level_key", "analysis_skill_id",
                                       name="uq_skill_level"),)


class BaselineStatus(Base):
    """Diagnostic initial, qualitatif et par domaine. Jamais converti en nombre."""
    __tablename__ = "baseline_status"
    id = Column(Integer, primary_key=True)
    student_id = Column(String(64), ForeignKey("student.student_id"), nullable=False)
    skill_id = Column(String(64), nullable=False)
    status_qualitative = Column(String(48), nullable=True)
    evidence = Column(Text, nullable=True)
    __table_args__ = (UniqueConstraint("student_id", "skill_id", name="uq_baseline"),)


class DelayedCheck(Base):
    __tablename__ = "delayed_check"
    id = Column(Integer, primary_key=True)
    student_id = Column(String(64), ForeignKey("student.student_id"), nullable=False)
    skill_id = Column(String(64), nullable=False)
    label = Column(String(255), nullable=True)
    importance_n = Column(String(32), nullable=True)
    reason = Column(Text, nullable=True)
    parallel_items_json = Column(Text, nullable=True)


# ----------------------------------------------------------------- correction
class Correction(Base):
    __tablename__ = "correction"
    correction_id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    revision = Column(Integer, nullable=False, default=1)
    status = Column(String(32), nullable=False, default="DRAFT")
    is_current = Column(Boolean, nullable=False, default=True)
    corrected_on = Column(String(32), nullable=True)
    observed_duration_minutes = Column(Integer, nullable=True)
    general_observations_json = Column(Text, nullable=True)
    reopen_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow,
                        onupdate=utcnow)
    validated_at = Column(DateTime(timezone=True), nullable=True)
    assessment = relationship("Assessment", back_populates="corrections")
    responses = relationship("CriterionResponse", back_populates="correction",
                            cascade="all, delete-orphan")
    item_observations = relationship("ItemObservation", back_populates="correction",
                                     cascade="all, delete-orphan")
    __table_args__ = (UniqueConstraint("assessment_id", "revision", name="uq_correction_rev"),)


class CriterionResponse(Base):
    """Une ligne notée : un critère simple, ou un sous-critère virtuel d'un critère mixte."""
    __tablename__ = "criterion_response"
    id = Column(Integer, primary_key=True)
    correction_id = Column(Integer, ForeignKey("correction.correction_id"), nullable=False)
    scoring_id = Column(String(160), nullable=False)
    criterion_id = Column(String(128), ForeignKey("criterion_definition.criterion_id"),
                          nullable=False)
    is_virtual = Column(Boolean, nullable=False, default=False)
    score_centi = Column(Integer, nullable=True)
    max_score_centi = Column(Integer, nullable=False)
    error_codes_json = Column(Text, nullable=False, default="[]")
    observation = Column(Text, nullable=True)
    accepted_alternative_method = Column(Boolean, nullable=False, default=False)
    scoring_status = Column(String(32), nullable=False, default="PENDING")
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow,
                        onupdate=utcnow)
    correction = relationship("Correction", back_populates="responses")
    __table_args__ = (UniqueConstraint("correction_id", "scoring_id", name="uq_resp"),)


class ItemObservation(Base):
    """Observation libre au niveau de l'item. Jamais scorée, jamais utilisée en calcul."""
    __tablename__ = "item_observation"
    id = Column(Integer, primary_key=True)
    correction_id = Column(Integer, ForeignKey("correction.correction_id"), nullable=False)
    item_id = Column(String(96), ForeignKey("item_definition.item_id"), nullable=False)
    confidence = Column(Integer, nullable=True)
    observation = Column(Text, nullable=True)
    correction = relationship("Correction", back_populates="item_observations")
    __table_args__ = (UniqueConstraint("correction_id", "item_id", name="uq_item_obs"),)


# ------------------------------------------------------------------- analyse
class AnalysisSnapshot(Base):
    __tablename__ = "analysis_snapshot"
    id = Column(Integer, primary_key=True)
    correction_id = Column(Integer, ForeignKey("correction.correction_id"), nullable=False)
    analysis_sha256 = Column(String(64), nullable=False)
    payload_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)


# ------------------------------------------------------------------ rapports
class Report(Base):
    __tablename__ = "report"
    report_id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    correction_id = Column(Integer, ForeignKey("correction.correction_id"), nullable=False)
    report_type = Column(String(48), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(32), nullable=False, default="DRAFT")
    analysis_sha256 = Column(String(64), nullable=True)
    template_version = Column(String(32), nullable=True)
    tex_path = Column(String(512), nullable=True)
    pdf_path = Column(String(512), nullable=True)
    pdf_sha256 = Column(String(64), nullable=True)
    manifest_path = Column(String(512), nullable=True)
    generated_at = Column(DateTime(timezone=True), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    blocks = relationship("ReportBlock", back_populates="report",
                          cascade="all, delete-orphan", order_by="ReportBlock.position")
    __table_args__ = (UniqueConstraint("assessment_id", "report_type", "version",
                                       name="uq_report_version"),)


class ReportBlock(Base):
    """Un paragraphe du rapport, avec sa provenance et son état d'approbation."""
    __tablename__ = "report_block"
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey("report.report_id"), nullable=False)
    block_key = Column(String(96), nullable=False)
    position = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False, default="")
    source = Column(String(32), nullable=False, default="deterministic")
    approved = Column(Boolean, nullable=False, default=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow,
                        onupdate=utcnow)
    report = relationship("Report", back_populates="blocks")
    __table_args__ = (UniqueConstraint("report_id", "block_key", name="uq_block"),)


class ReportBlockHistory(Base):
    __tablename__ = "report_block_history"
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey("report.report_id"), nullable=False)
    block_key = Column(String(96), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(32), nullable=False)
    replaced_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)


# --------------------------------------------------------------------- audit
class AuditEvent(Base):
    __tablename__ = "audit_event"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    action = Column(String(64), nullable=False)
    object_type = Column(String(64), nullable=False)
    object_id = Column(String(160), nullable=False)
    assessment_id = Column(String(64), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    __table_args__ = (Index("ix_audit_assessment", "assessment_id"),
                      Index("ix_audit_created", "created_at"))
