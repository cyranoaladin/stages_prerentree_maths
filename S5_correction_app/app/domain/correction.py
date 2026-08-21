# -*- coding: utf-8 -*-
"""Correction : création, saisie, machine d'état, révisions.

Deux invariants sont tenus ici, et le serveur refuse d'enregistrer ce qui les enfreint :

* **un critère intégralement réussi ne porte aucun code d'erreur scoré.** Une observation
  libre reste possible — « réponse correcte mais rédaction peu lisible » n'est pas une
  erreur ;
* **un zéro n'oblige à rien.** Le correcteur peut dire « non répondu » ou « cause non
  identifiée » plutôt que d'inventer un code. Une cause fabriquée fausserait le profil
  d'erreurs, donc le plan de rentrée.
"""

import datetime as dt
import json

from sqlalchemy import select

from ..models import (Assessment, AuditEvent, Correction, CriterionDefinition,
                      CriterionResponse, ItemDefinition, ItemObservation)
from . import points

# Codes d'erreur du référentiel S5. La liste est fermée : un code inconnu est refusé.
ERROR_CODES = {
    "CONCEPT": "La notion elle-même n'est pas disponible ou est remplacée par une règle fausse.",
    "METHODE": "La méthode choisie ne convient pas à la tâche demandée.",
    "CALCUL": "La méthode est correcte, l'exécution numérique ne l'est pas.",
    "LECTURE": "Une donnée de l'énoncé est mal lue, oubliée ou ajoutée.",
    "NOTATION": "Écriture, unité ou symbole incorrect alors que le raisonnement tient.",
    "JUSTIFICATION": "Le résultat est exact mais la propriété ou la relation n'est pas nommée.",
    "CONTROLE": "Aucun contrôle de vraisemblance n'est effectué alors qu'il était demandé.",
    "ALGORITHME": "L'enchaînement des instructions ne produit pas l'effet attendu.",
    "SYNTAXE": "Erreur d'écriture du langage, sans erreur de raisonnement.",
    "TRANSFERT": "Les acquis existent mais ne sont pas mobilisés dans un contexte nouveau.",
    "ETOURDERIE": "Écart isolé, non reproduit sur les items voisins de même compétence.",
}

SCORING_STATUSES = ("PENDING", "SCORED", "NOT_ANSWERED", "UNCLASSIFIED", "NEUTRALISED")
ZERO_STATUSES = ("NOT_ANSWERED", "UNCLASSIFIED")

STATUS_FLOW = {
    "DRAFT": ("REVIEW_READY",),
    "REVIEW_READY": ("DRAFT", "VALIDATED"),
    "VALIDATED": ("REPORT_READY",),
    "REPORT_READY": ("REPORT_APPROVED",),
    "REPORT_APPROVED": (),
}

LOCKED_STATUSES = ("VALIDATED", "REPORT_READY", "REPORT_APPROVED")

STATUS_LABELS = {
    "NOT_STARTED": "Non commencée",
    "DRAFT": "En cours",
    "REVIEW_READY": "À vérifier",
    "VALIDATED": "Validée",
    "REPORT_READY": "Bilan à générer",
    "REPORT_GENERATED": "Bilan généré",
    "REPORT_APPROVED": "Bilan approuvé",
}

GENERAL_OBSERVATION_FIELDS = (
    ("autonomie", "Autonomie observée"),
    ("methode", "Méthode de travail"),
    ("rythme", "Rythme"),
    ("redaction", "Qualité de rédaction"),
    ("controle", "Contrôle des résultats"),
    ("erreur", "Attitude face à l'erreur"),
    ("libre", "Remarque libre"),
)


class CorrectionError(Exception):
    pass


class LockedError(CorrectionError):
    pass


def scoring_rows(assessment) -> list:
    """Les lignes réellement notées : critères simples, et sous-critères des mixtes."""
    rows = []
    for item in assessment.items:
        for crit in item.criteria:
            if crit.curriculum_scope == "mixed":
                for virt in crit.virtual_parts:
                    rows.append({
                        "scoring_id": virt.virtual_criterion_id,
                        "criterion_id": crit.criterion_id, "is_virtual": True,
                        "item_id": item.item_id, "item_ref": item.ref,
                        "max_score_centi": virt.max_score_centi,
                        "curriculum_scope": virt.curriculum_scope,
                        "analysis_skill_id": virt.analysis_skill_id,
                        "description": virt.description,
                    })
            else:
                rows.append({
                    "scoring_id": crit.criterion_id, "criterion_id": crit.criterion_id,
                    "is_virtual": False, "item_id": item.item_id, "item_ref": item.ref,
                    "max_score_centi": crit.max_score_centi,
                    "curriculum_scope": crit.curriculum_scope,
                    "analysis_skill_id": crit.analysis_skill_id,
                    "description": crit.description,
                })
    return rows


def audit(session, action, object_type, object_id, assessment_id=None,
          old_value=None, new_value=None, reason=None):
    session.add(AuditEvent(action=action, object_type=object_type,
                           object_id=str(object_id), assessment_id=assessment_id,
                           old_value=old_value, new_value=new_value, reason=reason))


def current_correction(session, assessment_id: str):
    return session.execute(
        select(Correction).where(Correction.assessment_id == assessment_id,
                                 Correction.is_current.is_(True))).scalar_one_or_none()


def get_or_create_correction(session, assessment: Assessment) -> Correction:
    existing = current_correction(session, assessment.assessment_id)
    if existing:
        return existing
    correction = Correction(assessment_id=assessment.assessment_id, revision=1,
                            status="DRAFT", is_current=True)
    session.add(correction)
    session.flush()
    for row in scoring_rows(assessment):
        session.add(CriterionResponse(
            correction_id=correction.correction_id, scoring_id=row["scoring_id"],
            criterion_id=row["criterion_id"], is_virtual=row["is_virtual"],
            score_centi=None, max_score_centi=row["max_score_centi"],
            error_codes_json="[]", scoring_status="PENDING"))
    for item in assessment.items:
        session.add(ItemObservation(correction_id=correction.correction_id,
                                    item_id=item.item_id))
    if assessment.status == "NOT_STARTED":
        assessment.status = "DRAFT"
    audit(session, "correction.created", "correction", correction.correction_id,
          assessment.assessment_id, new_value="revision 1")
    session.flush()
    return correction


def reopen(session, correction: Correction, reason: str) -> Correction:
    """Rouvre une correction verrouillée en créant une révision. L'ancienne est conservée."""
    if not (reason or "").strip():
        raise CorrectionError("une réouverture demande une raison écrite")
    if correction.status not in LOCKED_STATUSES:
        raise CorrectionError("cette correction n'est pas verrouillée")
    correction.is_current = False
    new = Correction(assessment_id=correction.assessment_id,
                     revision=correction.revision + 1, status="DRAFT", is_current=True,
                     reopen_reason=reason.strip(),
                     corrected_on=correction.corrected_on,
                     observed_duration_minutes=correction.observed_duration_minutes,
                     general_observations_json=correction.general_observations_json)
    session.add(new)
    session.flush()
    for old in correction.responses:
        session.add(CriterionResponse(
            correction_id=new.correction_id, scoring_id=old.scoring_id,
            criterion_id=old.criterion_id, is_virtual=old.is_virtual,
            score_centi=old.score_centi, max_score_centi=old.max_score_centi,
            error_codes_json=old.error_codes_json, observation=old.observation,
            accepted_alternative_method=old.accepted_alternative_method,
            scoring_status=old.scoring_status))
    for old in correction.item_observations:
        session.add(ItemObservation(correction_id=new.correction_id, item_id=old.item_id,
                                    confidence=old.confidence, observation=old.observation))
    correction.assessment.status = "DRAFT"
    audit(session, "correction.reopened", "correction", new.correction_id,
          correction.assessment_id, old_value="revision %d (%s)"
          % (correction.revision, correction.status),
          new_value="revision %d" % new.revision, reason=reason.strip())
    session.flush()
    return new


def ensure_editable(correction: Correction):
    if correction.status in LOCKED_STATUSES:
        raise LockedError(
            "la correction est %s : elle doit être rouverte, avec une raison, avant "
            "toute modification." % STATUS_LABELS.get(correction.status, correction.status))


def set_status(session, correction: Correction, new_status: str, reason: str = None):
    allowed = STATUS_FLOW.get(correction.status, ())
    if new_status not in allowed:
        raise CorrectionError("transition interdite : %s → %s"
                              % (correction.status, new_status))
    old = correction.status
    correction.status = new_status
    if new_status == "VALIDATED":
        correction.validated_at = dt.datetime.now(dt.timezone.utc)
    correction.assessment.status = new_status
    audit(session, "correction.status", "correction", correction.correction_id,
          correction.assessment_id, old_value=old, new_value=new_status, reason=reason)


def save_response(session, correction: Correction, scoring_id: str, score_centi,
                  error_codes, observation, accepted_alternative_method,
                  scoring_status: str = None) -> CriterionResponse:
    """Enregistre une ligne notée. Refuse plutôt que d'accepter une saisie incohérente."""
    ensure_editable(correction)
    response = session.execute(
        select(CriterionResponse).where(
            CriterionResponse.correction_id == correction.correction_id,
            CriterionResponse.scoring_id == scoring_id)).scalar_one_or_none()
    if response is None:
        raise CorrectionError("critère inconnu pour cette correction : %s" % scoring_id)

    codes = [c.strip().upper() for c in (error_codes or []) if str(c).strip()]
    for code in codes:
        if code not in ERROR_CODES:
            raise CorrectionError("code d'erreur inconnu : %s" % code)
    codes = sorted(set(codes))

    status = (scoring_status or "").upper() or None
    if status and status not in SCORING_STATUSES:
        raise CorrectionError("statut de saisie inconnu : %s" % status)

    if status == "NEUTRALISED":
        score_centi, codes = None, []
        if not (observation or "").strip():
            raise CorrectionError("neutraliser un critère demande une justification écrite")
    elif status in ZERO_STATUSES:
        score_centi, codes = 0, []
    else:
        if score_centi is None:
            status = "PENDING"
        else:
            score_centi = int(score_centi)
            if not points.is_acceptable(score_centi, response.max_score_centi):
                raise CorrectionError(
                    "score hors barème : %s pour un maximum de %s"
                    % (points.format_fr(score_centi), points.format_fr(response.max_score_centi)))
            status = "SCORED"

    # L'invariant : réussite pleine et code d'erreur ne coexistent pas.
    if status == "SCORED" and score_centi == response.max_score_centi and codes:
        raise CorrectionError(
            "un critère intégralement réussi ne peut pas porter de code d'erreur. "
            "Une observation libre reste possible.")

    old = {"score": response.score_centi, "codes": json.loads(response.error_codes_json or "[]"),
           "status": response.scoring_status}
    response.score_centi = score_centi
    response.error_codes_json = json.dumps(codes, ensure_ascii=False)
    response.observation = (observation or "").strip() or None
    response.accepted_alternative_method = bool(accepted_alternative_method)
    response.scoring_status = status or "PENDING"
    new = {"score": score_centi, "codes": codes, "status": response.scoring_status}
    if old != new:
        audit(session, "response.saved", "criterion_response", scoring_id,
              correction.assessment_id, old_value=json.dumps(old, ensure_ascii=False),
              new_value=json.dumps(new, ensure_ascii=False))
    if correction.status == "DRAFT":
        correction.assessment.status = "DRAFT"
    return response


def save_item_observation(session, correction: Correction, item_id: str,
                          confidence=None, observation=None) -> ItemObservation:
    ensure_editable(correction)
    row = session.execute(
        select(ItemObservation).where(ItemObservation.correction_id == correction.correction_id,
                                      ItemObservation.item_id == item_id)).scalar_one_or_none()
    if row is None:
        raise CorrectionError("item inconnu pour cette correction : %s" % item_id)
    item = session.get(ItemDefinition, item_id)
    if confidence in ("", None):
        confidence = None
    else:
        confidence = int(confidence)
        if confidence not in (1, 2, 3, 4):
            raise CorrectionError("la certitude se note de 1 à 4")
        if not item.confidence_probe:
            raise CorrectionError("cet item ne comporte pas de ligne « certitude » sur le sujet "
                                  "distribué : elle ne peut pas être saisie")
    row.confidence = confidence
    row.observation = (observation or "").strip() or None
    return row


def save_general_observations(session, correction: Correction, data: dict):
    ensure_editable(correction)
    cleaned = {key: (data.get(key) or "").strip()
               for key, _ in GENERAL_OBSERVATION_FIELDS if (data.get(key) or "").strip()}
    correction.general_observations_json = json.dumps(cleaned, ensure_ascii=False)
    return cleaned


def progress(correction: Correction) -> dict:
    total = len(correction.responses)
    done = sum(1 for r in correction.responses if r.scoring_status != "PENDING")
    return {"total": total, "done": done,
            "percent": int(round(100.0 * done / total)) if total else 0,
            "remaining": total - done}


def raw_total_centi(correction: Correction) -> int:
    return sum(r.score_centi or 0 for r in correction.responses
               if r.scoring_status not in ("PENDING", "NEUTRALISED"))
