# -*- coding: utf-8 -*-
"""Construction de LONGITUDINAL_FACTS.json.

C'est le pivot du pipeline. Tout ce qui précède est de la collecte et du calcul
déterministe ; tout ce qui suit est de la rédaction. **Aucune phrase d'un bilan ne
peut s'appuyer sur autre chose que ce fichier.** Un générateur de texte — humain ou
non — qui aurait besoin d'une information absente d'ici doit se taire plutôt que
l'inventer.

Chaque fait porte son niveau de preuve et sa provenance. Le document remis aux
familles n'affiche pas cette mécanique, mais le système doit pouvoir répondre, pour
n'importe quelle affirmation du bilan, à la question « d'où sort-elle ? ».
"""

import hashlib
import json

from . import evidence_levels as ev
from . import plan as plan_module
from . import sources as sources_module
from . import trajectory as trajectory_module

FACTS_SCHEMA = "nexus-longitudinal-facts-v1"


def _fact(index, statement, source_type, evidence_level, **extra):
    fait = {"fact_id": "FACT_%04d" % index, "statement": statement,
            "source_type": source_type, "evidence_level": evidence_level}
    fait.update({k: v for k, v in extra.items() if v is not None})
    return fait


def build(student, assessment, correction, analysis, profile, baselines,
          releves, remediation_skills=None, dossier_lu=None) -> dict:
    """Assemble les faits longitudinaux d'un élève.

    ``baselines`` est indexé par ``skill_id``. ``releves`` vient de ``sources.collect``.
    """
    matrice = trajectory_module.build(baselines, analysis, remediation_skills)
    domaines = trajectory_module.by_domain(matrice)
    plan = plan_module.build(matrice)

    base = profile.get("baseline") or {}
    instrument = base.get("instrument") or {}
    diagnostic_disponible = bool(base.get("available"))

    # -------------------------------------------------------------- provenance
    provenance, index = [], 0
    for ligne in matrice:
        index += 1
        if ligne["has_final_evidence"]:
            provenance.append(_fact(
                index,
                "« %s » : %s à l'évaluation de clôture." % (ligne["label"],
                                                            ligne["final_status"]),
                "final_assessment", "A",
                skill_id=ligne["analysis_skill_id"],
                analysis_skill_id=ligne["analysis_skill_id"],
                item_refs=ligne["item_refs"],
                evidence_strength=ligne["evidence_strength"]))
        if ligne["initial_status"]:
            index += 1
            provenance.append(_fact(
                index,
                "« %s » : statut « %s » au diagnostic de pré-rentrée."
                % (ligne["label"], ligne["initial_status"]),
                "initial_diagnostic", "A" if diagnostic_disponible else "D",
                skill_id=ligne["analysis_skill_id"],
                source_path=instrument.get("file"),
                note=ligne.get("initial_evidence")))
        if ligne["sessions"]:
            index += 1
            provenance.append(_fact(
                index,
                "« %s » a été ciblée lors de %s." % (ligne["label"],
                                                     ", ".join(ligne["sessions"])),
                "session_material", "C",
                skill_id=ligne["analysis_skill_id"],
                session=",".join(ligne["sessions"]),
                note="preuve de parcours : établit le travail proposé, pas la réussite"))

    # ------------------------------------------------------------- observations
    observations = _observations(correction)

    n1 = analysis["n_minus_1_consolidation"]
    bridge = analysis["bridge_n_readiness"]

    forces = [l for l in matrice
              if l["curriculum_scope"] == "n_minus_1" and l["has_final_evidence"]
              and l["final_status"] in ("SOLIDE", "SATISFAISANT")]
    priorites = [l for l in matrice
                 if l["curriculum_scope"] == "n_minus_1" and l["has_final_evidence"]
                 and l["priority_rank"] in ("P1", "P2")]
    a_confirmer = [l for l in matrice if l["trajectory_status"] == "REUSSITE_A_CONFIRMER"]
    sans_preuve = [l for l in matrice if not l["has_final_evidence"]]

    payload = {
        "schema": FACTS_SCHEMA,
        "student": {
            "student_id": student.student_id,
            "display_name": student.person.display_name,
            "first_name": student.person.display_name.split()[0],
            "level_label": student.level_label,
            "subject": getattr(student, "subject", None) or "Mathématiques",
            "level_key": assessment.level_key,
        },
        "initial_diagnostic": {
            "available": diagnostic_disponible,
            "instrument": instrument,
            "date": base.get("date"),
            "items_traites": base.get("items_traites"),
            "confidence_calibration": base.get("confidence_calibration"),
            "summary": base.get("summary"),
            "strengths": base.get("strengths") or [],
            "priorities": base.get("priorities") or [],
            "domain_observations": base.get("domain_observations") or [],
            "item_level_results_available": bool(base.get("item_level_results_available")),
            "item_level_results_note": base.get("item_level_results_note"),
            "nominative_measure_available":
                bool(base.get("mesure_initiale_nominative_disponible")),
            "nominative_measure_note": base.get("mesure_initiale_note"),
        },
        "stage_trajectory": _stage_trajectory(profile, matrice, releves, dossier_lu),
        "final_assessment": {
            "correction_status": correction.status,
            "correction_revision": correction.revision,
            "raw_score": analysis["raw_assessment_score"],
            "scored_criteria": analysis.get("scored_criteria"),
            "error_profile": analysis["error_profile"],
            "observations": observations,
        },
        "n_minus_1": n1,
        "bridge_n": bridge,
        "skills": matrice,
        "domains": domaines,
        "strengths": [{"label": l["label"], "domain": l["domain"],
                       "final_status": l["final_status"],
                       "evidence_strength": l["evidence_strength"]}
                      for l in forces],
        "consolidation_priorities": [{"label": l["label"], "domain": l["domain"],
                                      "priority_rank": l["priority_rank"],
                                      "trajectory_status": l["trajectory_status"]}
                                     for l in priorites],
        "to_confirm": [{"label": l["label"], "domain": l["domain"]} for l in a_confirmer],
        "without_final_evidence": [{"label": l["label"], "domain": l["domain"],
                                    "sessions": l["sessions"],
                                    "worked_during_stage": l["worked_during_stage"],
                                    "current_mastery": l["current_mastery"]}
                                   for l in sans_preuve],
        "retention_checks": plan["delayed_checks"],
        "four_week_plan": plan,
        "interpretation_limits": _limits(analysis, base, releves, sans_preuve),
        "provenance": provenance,
        "evidence_model": {
            "levels": {lv: ev.LEVEL_LABELS[lv] for lv in ev.LEVELS},
            "mastery_may_be_asserted_from": [lv for lv in ev.LEVELS
                                             if ev.may_assert_mastery(lv)],
        },
        "mastery_delta": None,
        "mastery_delta_blocked_reason": trajectory_module.MASTERY_DELTA_BLOCKED_REASON,
        "sources": releves,
        "sources_summary": sources_module.summary(releves),
    }
    return payload


def _stage_trajectory(profile, matrice, releves, dossier_lu=None):
    """Ce que le stage a proposé, séance par séance — sans jamais parler de réussite.

    L'objectif personnalisé vient du dossier individuel de l'élève, où il est écrit
    séance par séance. C'est lui qui rend le bilan réellement propre à cet élève :
    sans lui, deux élèves du même niveau recevraient la même page.
    """
    brut = profile.get("trajectory") or {}
    seances_dossier = (dossier_lu or {}).get("sessions") or {}
    manquantes = {r["session"] for r in releves
                  if not r["present"] and r["role"] == "personalised_session_dossier"}
    seances = []
    for cle in sources_module.SESSIONS:
        donnees = brut.get(cle) or {}
        cibles = [l["label"] for l in matrice if cle in (l["sessions"] or [])]
        du_dossier = seances_dossier.get(cle) or {}
        seances.append({
            "session": cle,
            "theme": (donnees.get("theme") or du_dossier.get("theme")
                      or (profile.get("session5", {}).get("objective")
                          if cle == "S5" else None)),
            "personal_focus": du_dossier.get("personal_focus"),
            "skills_targeted": cibles,
            "documented_evidence": donnees.get("documented_evidence"),
            "observations_available": bool(donnees.get("documented_evidence")
                                           or du_dossier.get("observations_available")),
            "personalised_dossier_missing": cle in manquantes,
        })
    s5 = profile.get("session5") or {}
    return {
        "sessions": seances,
        "note": brut.get("note"),
        "session5": {"objective": s5.get("objective"),
                     "priority_skills": s5.get("priority_skills") or [],
                     "activities": s5.get("activities") or [],
                     "work_minutes": s5.get("work_minutes"),
                     "exam_minutes": s5.get("exam_minutes")},
        "observations_available_anywhere":
            any(s["observations_available"] for s in seances),
    }


def _observations(correction):
    """Observations écrites de l'enseignant, seule source de preuve de niveau B."""
    generales = {}
    if getattr(correction, "general_observations_json", None):
        try:
            generales = json.loads(correction.general_observations_json)
        except ValueError:
            generales = {}
    par_critere = [{"scoring_id": r.scoring_id, "text": r.observation}
                   for r in correction.responses
                   if (r.observation or "").strip()]
    return {"general": generales, "per_criterion": par_critere,
            "available": bool(generales or par_critere),
            "evidence_level": "B" if (generales or par_critere) else None}


def _limits(analysis, base, releves, sans_preuve):
    limites = list(analysis.get("interpretation_limits") or [])
    limites.append(
        "le diagnostic de pré-rentrée était qualitatif et par domaine : il ne "
        "conservait pas les réponses question par question, de sorte qu'aucun écart "
        "de maîtrise chiffré ne peut être établi entre le début et la fin du stage")
    if not base.get("available"):
        limites.append(
            "le dossier disponible ne permet pas de reconstituer un positionnement "
            "initial complet ; aucune comparaison n'est proposée")
    absentes = sources_module.missing(releves)
    if absentes:
        limites.append(
            "%d source(s) attendue(s) n'ont pas été trouvées : le bilan s'appuie sur "
            "les documents effectivement disponibles, sans reconstituer les autres"
            % len(absentes))
    if sans_preuve:
        limites.append(
            "%d compétence(s) travaillées pendant le stage ne sont évaluées par aucun "
            "critère de la copie de clôture : leur état actuel n'est pas documenté"
            % len(sans_preuve))
    if not any(r["present"] for r in releves
               if r["role"] == "personalised_session_dossier"):
        limites.append(
            "aucune observation de séance n'a été saisie : les tableaux de suivi des "
            "dossiers individuels sont vierges, « travaillé » ne vaut donc pas « acquis »")
    return limites


def digest(payload: dict) -> str:
    """Empreinte stable des faits, indépendante de l'ordre des clés.

    L'empreinte elle-même est exclue du calcul : sans cela, l'insérer dans la
    charge utile la rendrait invérifiable, puisque re-calculer donnerait une autre
    valeur. Ainsi ``digest(payload) == payload["facts_sha256"]`` reste vrai après
    l'insertion, et un bilan peut être contrôlé longtemps après sa production.
    """
    sans_empreinte = {k: v for k, v in payload.items() if k != "facts_sha256"}
    canonique = json.dumps(sans_empreinte, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"))
    return hashlib.sha256(canonique.encode("utf-8")).hexdigest()
