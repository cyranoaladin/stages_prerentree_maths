# -*- coding: utf-8 -*-
"""Matrice longitudinale : une ligne par compétence, du diagnostic à la rentrée.

La règle qui gouverne tout ce module tient en une phrase : **la couverture et la
maîtrise ne se confondent jamais**. Une compétence peut avoir été travaillée aux
cinq séances et rester sans preuve finale ; elle peut n'avoir été ciblée nulle part
et être réussie. Les deux colonnes sont donc calculées séparément, à partir de
sources différentes, et le statut de trajectoire n'est produit que lorsqu'une preuve
finale existe réellement.

Aucun écart chiffré n'est produit. Le diagnostic initial est qualitatif et par
domaine ; l'évaluation finale est critériée et par compétence. Les deux échelles ne
sont pas parallèles : ``mastery_delta`` vaut ``None``, sans exception.
"""

from . import evidence_levels as ev

MASTERY_DELTA_BLOCKED_REASON = (
    "les réponses item par item du diagnostic initial ne sont pas conservées : "
    "aucune mesure initiale nominative n'existe, donc aucun écart de maîtrise ne "
    "peut être calculé sans fabriquer une comparaison entre deux échelles "
    "différentes"
)

_POSITIF = ("SOLIDE", "SATISFAISANT")
_NEGATIF = ("A_CONSOLIDER", "PRIORITAIRE")

_BRIDGE_TRAJECTORY = {
    "PROMISING": "BRIDGE_PROMISING",
    "FIRST_EXPOSURE": "BRIDGE_FIRST_EXPOSURE",
    "BRIDGE_REVISIT": "BRIDGE_FIRST_EXPOSURE",
    "DISCOVERY_TO_CONTINUE": "BRIDGE_FIRST_EXPOSURE",
    "NO_CONCLUSION": "PREUVE_FINALE_INSUFFISANTE",
}

# Libellés destinés aux familles. Ils tiennent dans une colonne de tableau : la
# version longue de « en cours d'installation » s'y coupait en deux lignes à
# chaque occurrence, ce qui rendait la colonne illisible.
INITIAL_LABELS = {
    "acquis": "point d'appui",
    "en_voie_acquisition": "à installer",
    "fragile": "point de vigilance",
    "non_evalue": "non positionné",
    None: "non positionné",
}


def _trajectory_n1(initial, final_status, strength, coverage, immediate):
    """Statut de trajectoire d'un prérequis, dans un ordre de décision explicite."""
    if final_status == "PREUVE_INSUFFISANTE" or strength == "INSUFFICIENT":
        return "PREUVE_FINALE_INSUFFISANTE"
    if final_status == "A_CONFIRMER" or immediate:
        # Réussite obtenue juste après un travail sur la notion : elle vaut, mais
        # elle n'établit pas encore la disponibilité à distance.
        return "REUSSITE_A_CONFIRMER"
    if final_status in _POSITIF:
        if initial == "fragile":
            return ("CONSOLIDATION_OBSERVEE"
                    if strength in ("MODERATE", "STRONG")
                    else "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION")
        if initial == "en_voie_acquisition":
            return ("CONSOLIDATION_OBSERVEE"
                    if strength in ("MODERATE", "STRONG")
                    else "FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION")
        return "ACQUIS_ACTUELLEMENT_DISPONIBLE"
    if final_status in _NEGATIF:
        if initial in ("fragile", "en_voie_acquisition"):
            # Distinguer ce qui a été travaillé sans céder de ce qui n'a été que
            # confirmé faute de travail : la conséquence pédagogique diffère.
            return ("FRAGILITE_PERSISTANTE" if coverage in ("MODERATE", "STRONG")
                    else "FRAGILITE_INITIALE_CONFIRMEE")
        return "FRAGILITE_PERSISTANTE"
    return "PREUVE_FINALE_INSUFFISANTE"


def _conclusion(row) -> str:
    """Phrase interne résumant la ligne. Elle n'est pas destinée aux familles telle
    quelle : le rédacteur s'en sert comme d'un fait, pas comme d'une formulation."""
    initial = INITIAL_LABELS.get(row["initial_status"], "non positionné au diagnostic")
    seances = row["sessions"]
    part_stage = ("ciblée lors de %s" % ", ".join(seances)) if seances \
        else "non ciblée pendant le stage"
    if not row["has_final_evidence"]:
        return ("%s au diagnostic, %s ; l'évaluation de clôture n'apporte aucun "
                "élément sur ce point, l'état actuel reste inconnu."
                % (initial.capitalize(), part_stage))
    if row["initial_status"] in (None, "non_evalue"):
        socle = ("Aucun positionnement initial n'était disponible sur ce point ; %s."
                 % part_stage)
    else:
        socle = "%s au diagnostic, %s." % (initial.capitalize(), part_stage)
    return "%s %s" % (socle, ev.TRAJECTORY_LABELS.get(row["trajectory_status"], ""))


def build(baselines: dict, analysis: dict, remediation_skills=None) -> list:
    """Construit la matrice.

    ``baselines`` : ``skill_id -> dict`` issu de la table ``baseline_status``.
    ``analysis``  : la charge utile de ``analysis.analyse``.
    ``remediation_skills`` : compétences couvertes par la remédiation nominative.
    """
    remediation_skills = set(remediation_skills or ())
    lignes = []
    vus = set()

    for skill in analysis["skills"]:
        skill_id = skill["analysis_skill_id"]
        scope = skill["curriculum_scope"]
        vus.add((skill_id, scope))
        # Le socle initial se lit sur le skill_id d'origine : un alias d'analyse
        # (créé pour séparer une découverte d'un acquis) n'a pas de diagnostic.
        base = baselines.get(skill_id) or {}
        for origine in skill.get("original_skill_ids") or []:
            if not base:
                base = baselines.get(origine) or {}
        seances = list(base.get("sessions") or [])
        couverture = ev.coverage_of(seances, base.get("targeted_in_s5"),
                                    skill_id in remediation_skills)
        immediat = bool(skill.get("recommended_delayed_check"))

        if scope == "bridge_n":
            statut = _BRIDGE_TRAJECTORY.get(skill["status"], "BRIDGE_FIRST_EXPOSURE")
            initial = None          # une passerelle n'a pas de diagnostic initial
        else:
            initial = base.get("status_qualitative")
            statut = _trajectory_n1(initial, skill["status"],
                                    skill["evidence_strength"], couverture, immediat)

        ligne = {
            "analysis_skill_id": skill_id,
            "curriculum_scope": scope,
            "label": skill["label"],
            "domain": skill.get("domain") or base.get("domain"),
            "importance_n": skill.get("importance_n") or base.get("importance_n"),
            "initial_status": initial,
            "initial_evidence": base.get("evidence"),
            "sessions": seances,
            "coverage": couverture,
            "coverage_label": ev.COVERAGE_LABELS[couverture],
            "stage_evidence_note": base.get("stage_evidence_note"),
            "has_final_evidence": True,
            "final_status": skill["status"],
            "final_status_label": skill["status_label"],
            "evidence_level": "A",
            "evidence_strength": skill["evidence_strength"],
            "success_rate": skill["success_rate"],
            "criteria_count": len(skill["criteria"]),
            "item_refs": skill["item_refs"],
            "error_codes": skill["error_codes"],
            "retention_status": ("not_yet_verified" if immediat else "not_measured"),
            "recommended_delayed_check": immediat,
            "priority_rank": skill["priority_rank"],
            "bridge_action": skill.get("bridge_action"),
            "trajectory_status": statut,
            "mastery_delta": None,
            "mastery_delta_blocked_reason": MASTERY_DELTA_BLOCKED_REASON,
            "worked_during_stage": bool(seances) or bool(base.get("targeted_in_s5")),
            "current_mastery": "documented",
        }
        ligne["qualitative_trajectory"] = ev.qualitative_of(statut)
        ligne["conclusion"] = _conclusion(ligne)
        lignes.append(ligne)

    # Compétences du diagnostic que l'évaluation de clôture ne couvre pas. Elles
    # doivent figurer : leur absence du sujet est une information, et le bilan ne
    # doit surtout pas laisser croire qu'elles ont été vérifiées.
    for skill_id, base in sorted(baselines.items()):
        if any(skill_id == s for s, _ in vus):
            continue
        seances = list(base.get("sessions") or [])
        couverture = ev.coverage_of(seances, base.get("targeted_in_s5"),
                                    skill_id in remediation_skills)
        ligne = {
            "analysis_skill_id": skill_id,
            "curriculum_scope": "n_minus_1",
            "label": base.get("label") or skill_id,
            "domain": base.get("domain"),
            "importance_n": base.get("importance_n"),
            "initial_status": base.get("status_qualitative"),
            "initial_evidence": base.get("evidence"),
            "sessions": seances,
            "coverage": couverture,
            "coverage_label": ev.COVERAGE_LABELS[couverture],
            "stage_evidence_note": base.get("stage_evidence_note"),
            "has_final_evidence": False,
            "final_status": None,
            "final_status_label": None,
            # Sans critère évalué, la meilleure preuve disponible est celle du
            # parcours — ou aucune.
            "evidence_level": "C" if seances else "D",
            "evidence_strength": None,
            "success_rate": None,
            "criteria_count": 0,
            "item_refs": [],
            "error_codes": [],
            "retention_status": "not_measured",
            "recommended_delayed_check": False,
            "priority_rank": None,
            "bridge_action": None,
            "trajectory_status": "PREUVE_FINALE_INSUFFISANTE",
            "mastery_delta": None,
            "mastery_delta_blocked_reason": MASTERY_DELTA_BLOCKED_REASON,
            "worked_during_stage": bool(seances) or bool(base.get("targeted_in_s5")),
            "current_mastery": "unknown",
        }
        ligne["qualitative_trajectory"] = ev.qualitative_of(ligne["trajectory_status"])
        ligne["conclusion"] = _conclusion(ligne)
        lignes.append(ligne)

    lignes.sort(key=lambda r: (r["curriculum_scope"] != "n_minus_1",
                               r["domain"] or "", r["analysis_skill_id"]))
    return lignes


def by_domain(lignes) -> list:
    """Regroupement par domaine intelligible, pour le document destiné aux familles.

    Aucun identifiant technique ne franchit cette frontière : le domaine est la
    granularité que lisent les parents.
    """
    groupes = {}
    for ligne in lignes:
        if ligne["curriculum_scope"] != "n_minus_1":
            continue
        domaine = ligne["domain"] or "Autres compétences"
        g = groupes.setdefault(domaine, {
            "domain": domaine, "skills": [], "initial": set(), "sessions": set(),
            "coverage": "NONE", "final": [], "unknown": 0,
        })
        g["skills"].append(ligne)
        g["initial"].add(ligne["initial_status"])
        g["sessions"].update(ligne["sessions"])
        if ev.COVERAGE_LEVELS.index(ligne["coverage"]) > ev.COVERAGE_LEVELS.index(g["coverage"]):
            g["coverage"] = ligne["coverage"]
        if ligne["has_final_evidence"]:
            g["final"].append(ligne["final_status"])
        else:
            g["unknown"] += 1

    sortie = []
    for domaine in sorted(groupes):
        g = groupes[domaine]
        initiaux = [s for s in g["initial"] if s]
        sortie.append({
            "domain": domaine,
            "initial_status": _pire_initial(initiaux),
            "initial_label": INITIAL_LABELS.get(_pire_initial(initiaux),
                                                "non positionné au diagnostic"),
            "sessions": sorted(g["sessions"]),
            "coverage": g["coverage"],
            "coverage_label": ev.COVERAGE_LABELS[g["coverage"]],
            "final_status": _pire_final(g["final"]),
            "skills_without_final_evidence": g["unknown"],
            "skills": g["skills"],
        })
    return sortie


_ORDRE_INITIAL = ["fragile", "en_voie_acquisition", "non_evalue", "acquis"]
_ORDRE_FINAL = ["PRIORITAIRE", "A_CONSOLIDER", "PREUVE_INSUFFISANTE", "A_CONFIRMER",
                "SATISFAISANT", "SOLIDE"]


def _pire_initial(valeurs):
    for v in _ORDRE_INITIAL:
        if v in valeurs:
            return v
    return None


def _pire_final(valeurs):
    for v in _ORDRE_FINAL:
        if v in valeurs:
            return v
    return None
