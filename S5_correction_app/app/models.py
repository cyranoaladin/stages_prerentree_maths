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
    # Ajouts de la passe corrective : ce qu'il faut pour corriger sans ambiguïté.
    neutral_label = Column(String(255), nullable=True)          # ce que mesure le critère
    score_rubric_json = Column(Text, nullable=True)             # score -> règle observable
    error_suggestions_json = Column(Text, nullable=True)        # erreurs propres au critère
    official_source = Column(String(255), nullable=True)        # attendu officiel cité
    scope_certainty = Column(String(16), nullable=True)         # haute | moyenne | faible
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
    neutral_label = Column(String(255), nullable=True)
    score_rubric_json = Column(Text, nullable=True)
    error_suggestions_json = Column(Text, nullable=True)
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
    """Diagnostic initial, qualitatif et par domaine. Jamais converti en nombre.

    Les colonnes ajoutées en version 3 portent ce que le profil d'apprentissage
    documentait déjà mais que l'import laissait tomber : les questions du test
    initial rattachées à la compétence, les séances où elle a été ciblée, et
    l'état de la preuve de séance. Elles décrivent le **travail prévu**, jamais
    une réussite : « ciblée en S1 » ne vaut pas « acquise ».
    """
    __tablename__ = "baseline_status"
    id = Column(Integer, primary_key=True)
    student_id = Column(String(64), ForeignKey("student.student_id"), nullable=False)
    skill_id = Column(String(64), nullable=False)
    status_qualitative = Column(String(48), nullable=True)
    evidence = Column(Text, nullable=True)
    baseline_items_json = Column(Text, nullable=True)
    sessions_json = Column(Text, nullable=True)
    targeted_in_s5 = Column(Boolean, nullable=True)
    stage_evidence_note = Column(Text, nullable=True)
    provisional_priority = Column(String(16), nullable=True)
    domain = Column(String(96), nullable=True)
    importance_n = Column(String(32), nullable=True)
    __table_args__ = (UniqueConstraint("student_id", "skill_id", name="uq_baseline"),)


# ------------------------------------------------------- couche longitudinale
class LongitudinalFacts(Base):
    """Faits longitudinaux figés pour une révision de correction donnée.

    Le contenu JSON est le seul intrant de la rédaction : rien n'est écrit dans un
    bilan qui ne se trouve pas ici. Le hachage permet de constater qu'un bilan a
    été produit à partir d'un état de faits antérieur, et donc de le déclarer
    périmé sans avoir à le recalculer.
    """
    __tablename__ = "longitudinal_facts"
    id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    correction_id = Column(Integer, ForeignKey("correction.correction_id"), nullable=False)
    correction_revision = Column(Integer, nullable=False)
    facts_version = Column(Integer, nullable=False, default=1)
    payload_json = Column(Text, nullable=False)
    facts_sha256 = Column(String(64), nullable=False)
    analysis_sha256 = Column(String(64), nullable=True)
    built_at = Column(DateTime, nullable=False, default=utcnow)
    __table_args__ = (UniqueConstraint("correction_id", "facts_version", name="uq_facts"),)


class SkillTrajectory(Base):
    """Une ligne de la matrice longitudinale, par compétence.

    ``coverage`` décrit le travail fourni pendant le stage ; ``final_status``
    décrit ce que l'évaluation établit. Les deux sont volontairement séparés :
    beaucoup travaillé ne vaut pas acquis.
    """
    __tablename__ = "skill_trajectory"
    id = Column(Integer, primary_key=True)
    facts_id = Column(Integer, ForeignKey("longitudinal_facts.id"), nullable=False)
    analysis_skill_id = Column(String(64), nullable=False)
    curriculum_scope = Column(String(16), nullable=False)
    label = Column(String(255), nullable=True)
    domain = Column(String(96), nullable=True)
    importance_n = Column(String(32), nullable=True)
    initial_status = Column(String(48), nullable=True)
    sessions_json = Column(Text, nullable=True)
    coverage = Column(String(16), nullable=True)
    final_status = Column(String(48), nullable=True)
    evidence_level = Column(String(2), nullable=True)
    evidence_strength = Column(String(16), nullable=True)
    qualitative_trajectory = Column(String(48), nullable=True)
    retention_status = Column(String(32), nullable=True)
    priority_rank = Column(String(16), nullable=True)
    conclusion = Column(Text, nullable=True)
    __table_args__ = (
        UniqueConstraint("facts_id", "analysis_skill_id", "curriculum_scope",
                         name="uq_trajectory"),)


class ActionPlanItem(Base):
    """Un objectif du plan de rentrée, avec son seuil de réussite mesurable."""
    __tablename__ = "action_plan_item"
    id = Column(Integer, primary_key=True)
    facts_id = Column(Integer, ForeignKey("longitudinal_facts.id"), nullable=False)
    week = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    analysis_skill_id = Column(String(64), nullable=True)
    label = Column(String(255), nullable=True)
    objective = Column(Text, nullable=True)
    work = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    frequency = Column(String(96), nullable=True)
    success_threshold = Column(Text, nullable=True)
    is_delayed_check = Column(Boolean, nullable=False, default=False)
    kind = Column(String(24), nullable=False, default="n_minus_1")


class ReportSource(Base):
    """Provenance : ce qui a été réellement lu, et ce qui manquait.

    Une source absente est enregistrée avec ``present = False`` plutôt que
    silencieusement omise : le bilan doit pouvoir dire ce qu'il n'a pas pu lire.
    """
    __tablename__ = "report_source"
    id = Column(Integer, primary_key=True)
    facts_id = Column(Integer, ForeignKey("longitudinal_facts.id"), nullable=False)
    role = Column(String(64), nullable=False)
    source_type = Column(String(64), nullable=False)
    source_path = Column(String(512), nullable=True)
    source_sha256 = Column(String(64), nullable=True)
    session = Column(String(8), nullable=True)
    present = Column(Boolean, nullable=False, default=True)
    note = Column(Text, nullable=True)


class DelayedCheck(Base):
    __tablename__ = "delayed_check"
    id = Column(Integer, primary_key=True)
    student_id = Column(String(64), ForeignKey("student.student_id"), nullable=False)
    skill_id = Column(String(64), nullable=False)
    label = Column(String(255), nullable=True)
    importance_n = Column(String(32), nullable=True)
    reason = Column(Text, nullable=True)
    parallel_items_json = Column(Text, nullable=True)


# -------------------------------------------------------------- copie réelle
class SourceCopy(Base):
    """La copie réellement produite par l'élève, rattachée à son évaluation.

    Elle est rattachée à l'``assessment`` et non à une ``correction`` : rouvrir une
    correction crée une révision, mais ne crée pas une nouvelle copie papier. La
    correction se retrouve par ``assessment_id`` — c'est la même relation qui relie
    déjà les items et les révisions.

    ``origin`` sépare la pièce fournie par l'utilisateur, qui ne bouge plus jamais,
    d'une éventuelle pièce dérivée — recompressée, redressée, convertie — qui porte
    sa propre empreinte et pointe vers son original. Rien n'est jamais remplacé :
    une copie rattachée que l'on remplace devient ``SUPERSEDED`` et reste en base.
    """
    __tablename__ = "source_copy"
    source_copy_id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    source_kind = Column(String(32), nullable=False, default="REAL_STUDENT_COPY")
    origin = Column(String(16), nullable=False, default="ORIGINAL")   # ORIGINAL | DERIVED
    derived_from_id = Column(Integer, ForeignKey("source_copy.source_copy_id"), nullable=True)
    label = Column(String(255), nullable=True)
    page_count = Column(Integer, nullable=True)
    file_count = Column(Integer, nullable=False, default=0)
    status = Column(String(16), nullable=False, default="ATTACHED")   # ATTACHED | SUPERSEDED
    is_immutable = Column(Boolean, nullable=False, default=True)
    # Marque une pièce fabriquée pour un test ou un contrôle de chaîne. Une copie
    # d'élève réelle vaut False, et c'est ce qui déclenche le garde-fou d'envoi
    # distant : une fixture synthétique ne contient aucune donnée personnelle.
    is_synthetic = Column(Boolean, nullable=False, default=False)
    note = Column(Text, nullable=True)
    ingested_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    files = relationship("SourceCopyFile", back_populates="copy",
                         order_by="SourceCopyFile.page_index")
    __table_args__ = (Index("ix_source_copy_assessment", "assessment_id"),)


class SourceCopyFile(Base):
    """Un fichier d'une copie : le PDF unique, ou une page photographiée.

    ``page_index`` est l'ordre fourni au rattachement, jamais un ordre déduit d'un
    nom de fichier. ``stored_path`` est relatif à ``runtime/`` : la sauvegarde et la
    restauration n'ont pas à connaître l'arborescence du poste.
    """
    __tablename__ = "source_copy_file"
    id = Column(Integer, primary_key=True)
    source_copy_id = Column(Integer, ForeignKey("source_copy.source_copy_id"), nullable=False)
    page_index = Column(Integer, nullable=False)
    original_name = Column(String(255), nullable=False)
    media_type = Column(String(64), nullable=False)
    byte_size = Column(Integer, nullable=False)
    sha256 = Column(String(64), nullable=False)
    stored_path = Column(String(512), nullable=False)
    # Renseignés pour une page rastérisée : ils disent à quelle résolution la page a
    # été rendue, donc ce que le modèle a réellement pu voir.
    width_px = Column(Integer, nullable=True)
    height_px = Column(Integer, nullable=True)
    dpi = Column(Integer, nullable=True)
    # Rotation réellement appliquée aux pixels de cette page dérivée, en degrés.
    # Une rotation d'affichage dans le navigateur ne changerait pas ce que voit le
    # modèle : celle-ci, si.
    rotation = Column(Integer, nullable=False, default=0)
    copy = relationship("SourceCopy", back_populates="files")
    __table_args__ = (UniqueConstraint("source_copy_id", "page_index", name="uq_copy_page"),
                      Index("ix_source_copy_file_sha", "sha256"))


# ------------------------------------------------- lecture assistée des copies
class OcrRun(Base):
    """Une campagne de lecture assistée sur une copie : qui a lu, avec quoi, quand.

    La transcription est une couche probante distincte de la correction. Elle ne
    touche jamais ``criterion_response`` : un score reste une décision humaine, la
    transcription n'est que la restitution de ce qui est écrit sur la page.
    """
    __tablename__ = "ocr_run"
    run_id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    source_copy_id = Column(Integer, ForeignKey("source_copy.source_copy_id"), nullable=False)
    derived_copy_id = Column(Integer, ForeignKey("source_copy.source_copy_id"), nullable=True)
    role = Column(String(16), nullable=False)              # PRIMARY | VERIFY | BASELINE
    model_id = Column(String(128), nullable=False)
    provider_name = Column(String(96), nullable=True)
    prompt_version = Column(String(64), nullable=False)
    schema_version = Column(String(64), nullable=False)
    params_json = Column(Text, nullable=True)
    # Empreintes techniques : un prompt ou un schéma modifié sans changement de nom
    # de version se voit ici, et invalide le cache.
    prompt_sha256 = Column(String(64), nullable=True)
    schema_sha256 = Column(String(64), nullable=True)
    # Configuration figée au démarrage. Une variable d'environnement modifiée à la
    # page 7 ne doit pas produire une campagne hétérogène.
    frozen_config_json = Column(Text, nullable=True)
    # BLIND : seconde lecture indépendante, qui n'a pas vu la première.
    # SECOND_LOOK : relecture assistée, à qui l'on montre la transcription candidate.
    verify_mode = Column(String(16), nullable=True)
    # RUNNING|DONE|FAILED|INTERRUPTED
    status = Column(String(16), nullable=False, default="RUNNING")
    pages_total = Column(Integer, nullable=False, default=0)
    calls = Column(Integer, nullable=False, default=0)
    cached_calls = Column(Integer, nullable=False, default=0)
    tokens_in = Column(Integer, nullable=False, default=0)
    tokens_out = Column(Integer, nullable=False, default=0)
    cost_usd = Column(String(32), nullable=True)           # texte : jamais un flottant en base
    error = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    finished_at = Column(DateTime(timezone=True), nullable=True)


class OcrPage(Base):
    """Le résultat brut d'un appel, page par page, tel que le modèle l'a rendu."""
    __tablename__ = "ocr_page"
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("ocr_run.run_id"), nullable=False)
    page_index = Column(Integer, nullable=False)
    page_sha256 = Column(String(64), nullable=False)
    status = Column(String(16), nullable=False, default="OK")    # OK | FAILED | CACHED
    request_id = Column(String(128), nullable=True)
    generation_id = Column(String(128), nullable=True)
    raw_json = Column(Text, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    tokens_in = Column(Integer, nullable=True)
    tokens_out = Column(Integer, nullable=True)
    cost_usd = Column(String(32), nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    __table_args__ = (UniqueConstraint("run_id", "page_index", name="uq_ocr_page"),)


class TranscriptionBlock(Base):
    """Un bloc transcrit : ce que le modèle a lu, ce que la vérification en dit,
    et ce qu'un humain a éventuellement corrigé.

    La proposition de l'IA n'est jamais écrasée. Une correction humaine s'écrit dans
    ``human_*`` et laisse ``verbatim``/``latex`` intacts : on doit pouvoir montrer,
    plus tard, ce que la machine avait proposé et ce que l'humain a retenu.
    """
    __tablename__ = "transcription_block"
    id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    source_copy_id = Column(Integer, ForeignKey("source_copy.source_copy_id"), nullable=False)
    page_index = Column(Integer, nullable=False)
    block_id = Column(String(64), nullable=False)
    item_ref = Column(String(16), nullable=True)
    origin = Column(String(24), nullable=False)      # PRINTED|HANDWRITTEN|DIAGRAM_ANNOTATION
    # Taxonomie volontairement large et extensible : toute preuve d'élève n'est pas
    # du texte. Une figure, un tracé, un tableau ou un programme peuvent constituer
    # la réponse entière. L'absence de texte transcrit ne vaut JAMAIS « non répondu ».
    kind = Column(String(32), nullable=False)
    status = Column(String(16), nullable=False)      # ACTIVE|CROSSED_OUT|OVERWRITTEN|AMBIGUOUS
    verbatim = Column(Text, nullable=False)
    latex = Column(Text, nullable=True)
    uncertainty = Column(String(8), nullable=False, default="LOW")   # LOW | MEDIUM | HIGH
    alternatives_json = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    bbox_json = Column(Text, nullable=True)
    # Programme d'élève : la transcription doit préserver l'indentation, les espaces
    # significatifs, la casse et la ponctuation. Aucun formatage automatique, aucune
    # réparation : l'erreur de l'élève reste l'erreur de l'élève.
    verbatim_code = Column(Text, nullable=True)
    language_hint = Column(String(32), nullable=True)
    # Preuve non textuelle : la description ne remplace jamais l'image, elle la situe.
    ai_description = Column(Text, nullable=True)
    human_description = Column(Text, nullable=True)
    # PRIMARY : première lecture. BLIND : seconde lecture indépendante, stockée
    # comme lecture à part entière et non comme simple verdict.
    reading = Column(String(16), nullable=False, default="PRIMARY")
    primary_run_id = Column(Integer, ForeignKey("ocr_run.run_id"), nullable=True)
    verify_run_id = Column(Integer, ForeignKey("ocr_run.run_id"), nullable=True)
    verify_mode = Column(String(16), nullable=True)        # BLIND | SECOND_LOOK
    # BLIND     : IDENTICAL | DIFFERENT | UNMATCHED, calculé localement.
    # SECOND_LOOK : AGREE | DISAGREE | UNCERTAIN, rendu par le modèle.
    verify_verdict = Column(String(16), nullable=True)
    verify_block_id = Column(String(64), nullable=True)
    verify_verbatim = Column(Text, nullable=True)
    verify_latex = Column(Text, nullable=True)
    verify_note = Column(Text, nullable=True)
    # AI_CONSENSUS lorsque les deux lectures concordent ; sinon la main est rendue
    # à l'humain. Aucun troisième modèle ne vote pour départager.
    reconciliation = Column(String(24), nullable=True)
    review_state = Column(String(24), nullable=False, default="AI_PROPOSED")
    human_verbatim = Column(Text, nullable=True)
    human_latex = Column(Text, nullable=True)
    human_note = Column(Text, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by_role = Column(String(32), nullable=True)
    reviewed_by_identity = Column(String(96), nullable=True)
    # Rattachement d'item corrigé à la main : l'OCR peut lire parfaitement et
    # rattacher à la mauvaise question, ce qui est aussi grave qu'un caractère faux.
    human_item_ref = Column(String(16), nullable=True)
    # Une réponse peut commencer page N et se poursuivre page N+1.
    # Une réponse peut commencer page N et finir page N+1. La liaison proposée par
    # le modèle est révisable : elle ne doit jamais rattacher une suite à la question
    # dont elle est physiquement la plus proche.
    continues_from = Column(String(96), nullable=True)
    continues_to = Column(String(96), nullable=True)
    human_continues_from = Column(String(96), nullable=True)
    human_continues_to = Column(String(96), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    __table_args__ = (
        UniqueConstraint("source_copy_id", "page_index", "block_id", "reading",
                         name="uq_block"),
        Index("ix_block_assessment", "assessment_id"),)


class TranscriptionBlockHistory(Base):
    """Historique append-only des décisions humaines sur un bloc.

    ``human_verbatim`` seul ne suffit pas : un relecteur peut se reprendre. Chaque
    révision est conservée — avant, après, quand, qui, quelle action, pourquoi.
    Rien n'est écrasé, jamais.
    """
    __tablename__ = "transcription_block_history"
    id = Column(Integer, primary_key=True)
    block_pk = Column(Integer, ForeignKey("transcription_block.id"), nullable=False)
    action = Column(String(24), nullable=False)
    before_verbatim = Column(Text, nullable=True)
    after_verbatim = Column(Text, nullable=True)
    before_latex = Column(Text, nullable=True)
    after_latex = Column(Text, nullable=True)
    before_item_ref = Column(String(16), nullable=True)
    after_item_ref = Column(String(16), nullable=True)
    before_state = Column(String(24), nullable=True)
    after_state = Column(String(24), nullable=True)
    reason = Column(Text, nullable=True)
    actor_identity = Column(String(96), nullable=True)
    actor_role = Column(String(32), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=utcnow)
    __table_args__ = (Index("ix_block_history", "block_pk"),)


class PageAttestation(Base):
    """Attestation humaine de complétude, page par page.

    Une collection de blocs tous « acceptés » ne démontre pas qu'aucune zone
    manuscrite n'a été **omise** par le modèle : l'interface ne montre que ce que le
    modèle a vu. Seul un humain, en comparant la page et la transcription, peut
    attester que rien de pertinent ne manque. Sans cette attestation, une page n'est
    jamais considérée comme vérifiée.
    """
    __tablename__ = "page_attestation"
    id = Column(Integer, primary_key=True)
    source_copy_id = Column(Integer, ForeignKey("source_copy.source_copy_id"),
                            nullable=False)
    page_index = Column(Integer, nullable=False)
    page_sha256 = Column(String(64), nullable=False)
    attested = Column(Boolean, nullable=False, default=False)
    note = Column(Text, nullable=True)
    actor_identity = Column(String(96), nullable=True)
    actor_role = Column(String(32), nullable=True)
    attested_at = Column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("source_copy_id", "page_index",
                                       name="uq_page_attestation"),)


class TranscriptionState(Base):
    """État de la lecture assistée pour une copie. Une seule ligne courante."""
    __tablename__ = "transcription_state"
    id = Column(Integer, primary_key=True)
    assessment_id = Column(String(64), ForeignKey("assessment.assessment_id"), nullable=False)
    source_copy_id = Column(Integer, ForeignKey("source_copy.source_copy_id"), nullable=False)
    # NOT_STARTED | RUNNING | AI_PROPOSED | REVIEW_REQUIRED | HUMAN_VERIFIED | FAILED
    state = Column(String(24), nullable=False, default="NOT_STARTED")
    detail = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=utcnow,
                        onupdate=utcnow)
    __table_args__ = (UniqueConstraint("source_copy_id", name="uq_transcription_state"),)


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
    # Marque une correction produite par une fixture de test. Une correction
    # saisie par l'enseignant vaut False, et c'est ce qui protège la base : la
    # réinitialisation destructrice refuse de s'exécuter tant qu'une correction
    # non synthétique porte des scores.
    is_synthetic = Column(Boolean, nullable=False, default=False)
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
