# -*- coding: utf-8 -*-
"""LongitudinalReportService — orchestration du pipeline de bilan.

L'ordre des étapes n'est pas décoratif : il porte la garantie centrale du système.

    sources → normalisation → faits structurés → calcul déterministe
            → règles pédagogiques → LONGITUDINAL_FACTS.json → rédaction

Aucune rédaction ne commence avant que les faits ne soient figés et empreintés. Un
générateur de texte n'a jamais accès aux sources brutes : il reçoit les faits, et
seulement eux. C'est ce qui rend chaque phrase du bilan traçable.

Deux verrous à l'entrée :

* une correction non validée ne produit pas de bilan final. Un brouillon peut
  changer entre deux régénérations ; un bilan remis à une famille, non ;
* les faits sont liés à une révision de correction précise. Si la correction est
  rouverte et corrigée, le bilan produit auparavant devient **périmé** et le système
  le dit, plutôt que de laisser circuler un document qui ne correspond plus à la copie.
"""

import json

from ... import config
from ...models import (ActionPlanItem, BaselineStatus, LongitudinalFacts, ReportSource,
                       SkillTrajectory)
from .. import analysis as analysis_module
from . import dossier as dossier_module
from . import facts as facts_module
from . import guard as guard_module
from . import plan as plan_module
from . import sources as sources_module
from . import trajectory as trajectory_module


class LongitudinalError(Exception):
    """Refus motivé : la génération n'est pas possible en l'état."""


class LongitudinalReportService:
    def __init__(self, session):
        self.session = session

    # ------------------------------------------------------------------ garde
    @staticmethod
    def check_ready(correction) -> list:
        """Conditions d'entrée. Retourne la liste des obstacles ; vide vaut feu vert."""
        obstacles = []
        if correction is None:
            obstacles.append("aucune correction n'existe pour cet élève")
            return obstacles
        if correction.status not in ("VALIDATED", "REPORT_READY", "REPORT_APPROVED"):
            obstacles.append(
                "la correction est au statut « %s » : un bilan longitudinal ne peut "
                "être produit qu'à partir d'une correction validée" % correction.status)
        non_saisis = [r.scoring_id for r in correction.responses
                      if r.scoring_status == "PENDING"]
        if non_saisis:
            obstacles.append("%d ligne(s) analytique(s) ne sont pas renseignées"
                             % len(non_saisis))
        return obstacles

    # -------------------------------------------------------------- collecte
    def collect_sources(self, assessment):
        """Étape 1 — retrouver les documents, les empreinter, nommer les absents."""
        profil, chemin = self._profile(assessment)
        return sources_module.collect(profil, chemin), profil

    def normalize_sources(self, assessment, profile):
        """Étape 2 — ramener le diagnostic initial à un état par compétence.

        L'import a déjà fait ce travail : la normalisation consiste ici à relire
        la table plutôt qu'à réinterpréter les documents, de sorte qu'un bilan et
        l'écran de correction parlent toujours du même diagnostic.
        """
        lignes = self.session.query(BaselineStatus).filter_by(
            student_id=assessment.student_id).all()
        etiquettes = {s["skill_id"]: s for s in
                      ((profile.get("baseline") or {}).get("skills") or [])}
        sortie = {}
        for ligne in lignes:
            brut = etiquettes.get(ligne.skill_id, {})
            sortie[ligne.skill_id] = {
                "skill_id": ligne.skill_id,
                "label": brut.get("label"),
                "domain": ligne.domain or brut.get("domain"),
                "importance_n": ligne.importance_n or brut.get("importance_n"),
                "status_qualitative": ligne.status_qualitative,
                "evidence": ligne.evidence,
                "sessions": json.loads(ligne.sessions_json or "[]"),
                "baseline_items": json.loads(ligne.baseline_items_json or "[]"),
                "targeted_in_s5": bool(ligne.targeted_in_s5),
                "stage_evidence_note": ligne.stage_evidence_note,
                "provisional_priority": ligne.provisional_priority,
            }
        return sortie

    # ------------------------------------------------------------- calculs
    def build_skill_trajectory(self, baselines, analysis, remediation_skills=None):
        """Étape 3 — la matrice, compétence par compétence."""
        return trajectory_module.build(baselines, analysis, remediation_skills)

    def build_action_plan(self, matrice):
        """Étape 5 — les quatre semaines, à partir de la matrice seule."""
        return plan_module.build(matrice)

    def build_longitudinal_facts(self, assessment, correction, persist: bool = True):
        """Étape 4 — assembler, empreinter et, si demandé, figer en base."""
        obstacles = self.check_ready(correction)
        if obstacles:
            raise LongitudinalError(" ; ".join(obstacles))

        releves, profil = self.collect_sources(assessment)
        baselines = self.normalize_sources(assessment, profil)
        analyse = analysis_module.analyse(self.session, correction, assessment)
        remediation = self._remediation_skills(baselines, releves)

        lecture_dossier = self._read_dossier(releves)
        payload = facts_module.build(
            assessment.student, assessment, correction, analyse, profil,
            baselines, releves, remediation, lecture_dossier)
        payload["facts_sha256"] = facts_module.digest(payload)

        if not persist:
            return payload

        version = 1 + self.session.query(LongitudinalFacts).filter_by(
            correction_id=correction.correction_id).count()
        enregistrement = LongitudinalFacts(
            assessment_id=assessment.assessment_id,
            correction_id=correction.correction_id,
            correction_revision=correction.revision,
            facts_version=version,
            payload_json=json.dumps(payload, ensure_ascii=False),
            facts_sha256=payload["facts_sha256"],
            analysis_sha256=analyse.get("analysis_sha256"))
        self.session.add(enregistrement)
        self.session.flush()
        self._persist_rows(enregistrement, payload)
        return payload

    # ------------------------------------------------------------ péremption
    def is_stale(self, correction) -> dict:
        """Un bilan est périmé dès que la correction a changé après sa production.

        La recherche porte sur l'évaluation, non sur l'identifiant de correction :
        rouvrir une copie crée une **nouvelle** correction, et c'est précisément le
        cas que ce contrôle existe pour couvrir. Chercher par correction ferait
        conclure « aucun bilan produit » là où un bilan périmé circule.
        """
        dernier = self.session.query(LongitudinalFacts).filter_by(
            assessment_id=correction.assessment_id).order_by(
            LongitudinalFacts.id.desc()).first()
        if dernier is None:
            return {"stale": True, "reason": "aucun bilan n'a encore été produit",
                    "facts_revision": None, "correction_revision": correction.revision}
        perime = dernier.correction_revision != correction.revision
        return {
            "stale": perime,
            "reason": ("la correction a été rouverte et corrigée depuis : le bilan "
                       "porte la révision %s, la correction en est à la révision %s"
                       % (dernier.correction_revision, correction.revision))
            if perime else None,
            "facts_revision": dernier.correction_revision,
            "correction_revision": correction.revision,
            "facts_sha256": dernier.facts_sha256,
        }

    # ------------------------------------------------------------- validation
    @staticmethod
    def validate_report(texte: str, payload: dict, audience: str = "parents") -> dict:
        """Étape 9 — refuser un texte qui affirme plus que les faits ne portent."""
        return guard_module.validate(texte, payload.get("skills"), audience)

    # ----------------------------------------------------------------- outils
    def _profile(self, assessment):
        """Profil d'apprentissage de l'élève, relu à sa source."""
        chemin = None
        for candidat in config.CLOTURE_ROOT.rglob("student_learning_profile.json"):
            try:
                donnees = json.loads(candidat.read_text(encoding="utf-8"))
            except ValueError:
                continue
            if (donnees.get("student") or {}).get("id") == assessment.student_id:
                chemin = candidat
                return donnees, chemin
        raise LongitudinalError(
            "aucun profil d'apprentissage n'a été trouvé pour %s : le bilan "
            "longitudinal ne peut pas être reconstitué sans lui" % assessment.student_id)

    @staticmethod
    def _read_dossier(releves):
        """Lit le dossier individuel, s'il figure parmi les sources présentes."""
        for releve in releves:
            if releve["role"] == "individual_dossier" and releve["present"]:
                return dossier_module.read(
                    config.REPO_ROOT / releve["source_path"])
        return None

    @staticmethod
    def _remediation_skills(baselines, releves):
        """Compétences couvertes par la remédiation nominative.

        Le document de remédiation est organisé par domaine ; on rattache donc les
        compétences par leur domaine, sans prétendre à une correspondance exercice
        par exercice qui n'existe pas dans la source.
        """
        if not any(r["present"] for r in releves if r["role"] == "remediation"):
            return set()
        prioritaires = {b["skill_id"] for b in baselines.values()
                        if b.get("status_qualitative") in ("fragile", "en_voie_acquisition")}
        return prioritaires

    def _persist_rows(self, enregistrement, payload):
        for ligne in payload["skills"]:
            self.session.add(SkillTrajectory(
                facts_id=enregistrement.id,
                analysis_skill_id=ligne["analysis_skill_id"],
                curriculum_scope=ligne["curriculum_scope"],
                label=ligne["label"], domain=ligne["domain"],
                importance_n=ligne["importance_n"],
                initial_status=ligne["initial_status"],
                sessions_json=json.dumps(ligne["sessions"], ensure_ascii=False),
                coverage=ligne["coverage"], final_status=ligne["final_status"],
                evidence_level=ligne["evidence_level"],
                evidence_strength=ligne["evidence_strength"],
                qualitative_trajectory=ligne["qualitative_trajectory"],
                retention_status=ligne["retention_status"],
                priority_rank=ligne["priority_rank"],
                conclusion=ligne["conclusion"]))
        for semaine in payload["four_week_plan"]["weeks"]:
            for objectif in semaine["objectives"]:
                self.session.add(ActionPlanItem(
                    facts_id=enregistrement.id, week=semaine["week"],
                    rank=objectif["rank"],
                    analysis_skill_id=objectif["analysis_skill_id"],
                    label=objectif["label"], objective=objectif["objective"],
                    work=objectif["work"],
                    duration_minutes=objectif["duration_minutes"],
                    frequency=objectif["frequency"],
                    success_threshold=objectif["success_threshold"],
                    is_delayed_check=objectif["is_delayed_check"],
                    kind=objectif["kind"]))
        for releve in payload["sources"]:
            self.session.add(ReportSource(
                facts_id=enregistrement.id, role=releve["role"],
                source_type=releve["source_type"], source_path=releve["source_path"],
                source_sha256=releve["source_sha256"], session=releve["session"],
                present=releve["present"], note=releve["note"]))
