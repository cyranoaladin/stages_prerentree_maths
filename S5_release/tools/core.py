# -*- coding: utf-8 -*-
"""Logique déterministe partagée : statuts de compétences, priorités, sources, items.

Aucune de ces fonctions ne produit de résultat final : tout ce qui est calculé ici
décrit l'état *avant* la passation de l'évaluation, à partir des sources documentées.
"""

import os

from data import common
from data import timing
from data import criteria_map
from data.levels import LEVELS, MODULES, LEVEL_ORDER
from data.students import STUDENTS, STATUS_FROM_DOMAIN

HERE = os.path.dirname(os.path.abspath(__file__))
S5_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(S5_ROOT)


def level_of(student):
    return LEVELS[student["level"]]


def slug_level(level):
    return level["key"]


def student_output_dir(student):
    level = level_of(student)
    return os.path.join(S5_ROOT, level["key"], _subject_slug(level["subject"]), student["dir"])


def _subject_slug(subject):
    return {"Mathématiques": "Mathematiques", "NSI": "NSI"}.get(subject, subject)


def doc_basename(kind, student):
    """kind in {TRAVAIL, EVALUATION, ENSEIGNANT}."""
    level = level_of(student)
    return "S5_%s_%s_%s" % (kind, level["key"].upper(), student["dir"].upper())


# ---------------------------------------------------------------- compétences
def skill_status(student, skill_id):
    """Statut d'une compétence AVANT la séance S5 et avant l'évaluation finale.

    Fondé exclusivement sur le diagnostic initial (statut du domaine dans le dossier
    individuel) et sur les précisions explicites du dossier (``skill_overrides``).
    """
    level = level_of(student)
    skill = level["skills"][skill_id]
    if skill_id in student.get("skill_overrides", {}):
        status, evidence = student["skill_overrides"][skill_id]
        return status, evidence
    domain = skill["domain"]
    raw = student["domain_status"].get(domain)
    if raw is None:
        return "non_evalue", "Aucun statut de domaine correspondant dans le dossier individuel."
    if raw not in STATUS_FROM_DOMAIN:
        return "non_evalue", "Statut de domaine non concluant dans le dossier individuel (« %s »)." % raw
    status = STATUS_FROM_DOMAIN[raw]
    evidence = "Statut « %s » porté au dossier individuel pour le domaine « %s »." % (
        raw.replace("_", " "), domain)
    if not skill["baseline_items"] and status == "acquis":
        # Pas d'item de référence : on ne peut pas parler d'acquis.
        return "en_voie_acquisition", evidence + " Aucun item du diagnostic initial n'évalue cette compétence isolément."
    return status, evidence


def priority_pre(student, skill_id, status):
    """Priorité provisoire, avant l'évaluation finale. Définitive après analyze_s5.py."""
    if skill_id in (student["p1"], student["p2"]):
        return "P1"
    level = level_of(student)
    importance = level["skills"][skill_id]["importance_n"]
    if status == "acquis":
        return "OK"
    if status == "fragile":
        return "P1" if importance == "critique" else "P2"
    if status == "en_voie_acquisition":
        return "P2" if importance == "critique" else "P3"
    if status == "non_evalue":
        return "P2" if importance == "critique" else "P3"
    return "P3"


def skill_table(student):
    """Table complète compétence par compétence, avec preuve et priorité provisoire."""
    level = level_of(student)
    rows = []
    for sid, sk in level["skills"].items():
        status, evidence = skill_status(student, sid)
        rows.append({
            "skill_id": sid,
            "label": sk["label"],
            "domain": sk["domain"],
            "importance_n": sk["importance_n"],
            "baseline_items": sk["baseline_items"],
            "sessions_travaillees": sk["sessions"],
            "statut_avant_s5": status,
            "preuve": evidence,
            "preuve_post_s1_s4": "non documentée : les tableaux d'observation séance par séance du dossier individuel sont vierges",
            "priorite_provisoire": priority_pre(student, sid, status),
            "cible_s5": sid in (student["p1"], student["p2"]),
        })
    rows.sort(key=lambda r: (r["priorite_provisoire"], r["skill_id"]))
    return rows


# -------------------------------------------------------------------- sources
def student_sources(student):
    level = level_of(student)
    d = level["source_dir"]
    if level["key"] == "1re_nsi":
        nom = os.path.join(d, "05_NOMINATIFS", student["dir"])
        srcs = [
            os.path.join(nom, "1re_nsi_Dossier_Individuel_%s.md" % student["dir"]),
            os.path.join(nom, "1re_nsi_Remediation_Ciblee_%s_ELEVE.md" % student["dir"]),
            os.path.join(nom, "1re_nsi_Remediation_Ciblee_%s_PROF_Corrige.md" % student["dir"]),
        ]
    else:
        folder = student["dir"].title().replace("_", "_")
        nom = os.path.join(d, "04_NOMINATIFS", _maths_folder(student))
        srcs = [
            os.path.join(nom, "%s_Dossier_Individuel_%s.md" % (d, _maths_folder(student))),
            os.path.join(nom, "%s_Remediation_Ciblee_%s_ELEVE.md" % (d, _maths_folder(student))),
            os.path.join(nom, "%s_Remediation_Ciblee_%s_PROF_Corrige.md" % (d, _maths_folder(student))),
        ]
    srcs.append(level["baseline_instrument"]["file"])
    for s in ("S1", "S2", "S3", "S4", "S5"):
        srcs.append(os.path.join(d, "02_SEANCES", s))
    srcs.extend(student.get("extra_sources", []))
    return srcs


_MATHS_FOLDERS = {
    "ines-kefi": "Ines_Kefi", "sinda-chikhaoui": "Sinda_Chikhaoui",
    "fares-darghouth": "Fares_Darghouth", "elyes-kefi": "Elyes_Kefi",
    "amine-mansouri": "Amine_Mansouri", "fares-laajili": "Fares_Laajili",
    "sarah-bargaoui": "Sarah_Bargaoui", "selim-mansouri": "Selim_Mansouri",
    "ahmed-bakir": "Ahmed_Bakir", "noa-maniaci": "Noa_Maniaci",
    "ahmad-beldi-maths": "Ahmad_Beldi", "donia-khadhrani": "Donia_Khadhrani",
    "malek-khadhrani": "Malek_Khadhrani",
}


def _maths_folder(student):
    # Le jeu de tests synthétique n'a pas de dossier nominatif dans le dépôt.
    return _MATHS_FOLDERS.get(student["id"], student["dir"])


def source_exists(path):
    return os.path.exists(os.path.join(REPO_ROOT, path))


# ------------------------------------------------------------------ évaluation
def exam_items(student):
    """Liste ordonnée des 12 items, noyau commun et items individualisés fusionnés."""
    level = level_of(student)
    items = []
    for iid in common.EXAM_ITEM_ORDER:
        if iid in level["eval_common"]:
            src = dict(level["eval_common"][iid])
            src["kind"] = "commun"
        else:
            src = dict(student["eval_individual"][iid])
            src["kind"] = "individuel"
        # Durée estimée à partir du contenu de l'item, jamais imposée.
        est = timing.estimate(src, level["key"])
        src["minutes"] = est["minutes"]
        src["time_estimate"] = est
        src["item_id"] = "%s_%s_%s" % (level["key"].upper(), student["dir"].upper(), iid)
        src["ref"] = iid
        src["part"] = iid[0]
        src["comparison_status"] = COMPARISON_STATUS[src["comparability"]]
        src["criteria"] = enrich_criteria(student, src, iid, src["item_id"])
        # Les compétences de l'item sont désormais celles de ses critères.
        skills = item_skills(src)
        src["skill"] = skills[0] if src["skill"] not in skills else src["skill"]
        src["skills_extra"] = [s for s in skills if s != src["skill"]]
        src["baseline_skill_refs"] = baseline_skill_refs(student, src)
        items.append(src)
    return items


# Statuts de comparaison initial / final.
#
#   parallel_measures            deux mesures nominatives réelles existent pour la
#                                compétence : un delta chiffré serait légitime.
#                                Aucun élève n'est dans ce cas aujourd'hui, les
#                                réponses item par item du diagnostic initial
#                                n'ayant pas été conservées.
#   indicative_skill_comparison  un item parallèle existe dans le test de
#                                positionnement et le dossier documente un statut
#                                qualitatif de domaine : la confrontation est
#                                indicative, jamais chiffrée.
#   post_only                    la compétence n'est mesurée qu'en fin de stage.
#   not_comparable               contenu introduit pendant la séance 5 elle-même.
COMPARISON_STATUS = {
    "comparable": "indicative_skill_comparison",
    "partiellement_comparable": "indicative_skill_comparison",
    "non_comparable_contenu_nouveau": "not_comparable",
    "non_comparable_absence_baseline": "post_only",
}
COMPARISON_VALUES = ("parallel_measures", "indicative_skill_comparison",
                     "post_only", "not_comparable")


def item_skills(item):
    """Compétences réellement évaluées : exactement celles des critères du barème."""
    seen = []
    for c in item["criteria"]:
        if c["skill_id"] not in seen:
            seen.append(c["skill_id"])
    return seen


def enrich_criteria(student, item, ref, item_id):
    """Attribue à chaque critère un identifiant, une compétence et un type de preuve.

    Pour un item mono-compétence, la compétence du critère est celle de l'item :
    c'est une identité, pas une supposition. Pour un item multi-compétences, la
    table `criteria_map.CRITERIA` fournit l'attribution explicite, critère par
    critère ; l'absence d'entrée est une erreur bloquante.
    """
    level = level_of(student)
    key = (level["key"], ref) if item["kind"] == "commun" else (student["id"], ref)
    mapped = criteria_map.CRITERIA.get(key)
    out = []
    if mapped is not None:
        for k, (pts, sid, ev, sub, desc) in enumerate(mapped, 1):
            out.append({"criterion_id": "%s_c%d" % (item_id, k), "points": pts,
                        "skill_id": sid, "evidence_type": ev, "subpart": sub,
                        "desc": desc})
    else:
        if item.get("skills_extra"):
            raise ValueError("item multi-compétences sans attribution explicite des "
                             "critères : %s" % (key,))
        for k, c in enumerate(item["criteria"], 1):
            out.append({"criterion_id": "%s_c%d" % (item_id, k), "points": c["points"],
                        "skill_id": item["skill"],
                        "evidence_type": criteria_map.evidence_for(c["desc"]),
                        "subpart": str(k), "desc": c["desc"]})
    total = round(sum(c["points"] for c in out), 6)
    if total != float(item["points"]):
        raise ValueError("somme des critères %s = %s, attendu %s"
                         % (key, total, item["points"]))
    return out


def baseline_skill_refs(student, item):
    """Compétences de l'item disposant d'au moins un item du diagnostic initial.

    Permet une comparaison au niveau de la compétence lorsqu'aucun item parallèle
    n'existe (tâche de synthèse), sans jamais prétendre à un delta item par item.
    """
    lv = level_of(student)
    refs = []
    for sid in item_skills(item):
        b = lv["skills"][sid]["baseline_items"]
        if b:
            refs.append({"skill_id": sid, "baseline_items": list(b)})
    return refs


def points_per_skill(student, items):
    """Points attribués compétence par compétence, à partir des critères du barème.

    Aucune répartition uniforme : chaque critère porte sa compétence, et ses points
    vont à celle-ci et à aucune autre.
    """
    out = {}
    for it in items:
        for c in it["criteria"]:
            out[c["skill_id"]] = round(out.get(c["skill_id"], 0.0) + c["points"], 4)
    return out


def exam_totals(items):
    total = sum(i["points"] for i in items)
    minutes = sum(i["minutes"] for i in items)
    commun = sum(i["points"] for i in items if i["kind"] == "commun")
    indiv = total - commun
    return {"points": total, "minutes": minutes, "points_commun": commun,
            "points_individuel": indiv,
            "part_commun_pct": round(100.0 * commun / total, 1),
            "part_individuel_pct": round(100.0 * indiv / total, 1)}


# ---------------------------------------------------------------------- phases
def phases(student):
    """Les cinq phases des 75 minutes, phases 2 et 3 instanciées par les modules."""
    level = level_of(student)
    out = []
    start = 0
    for n, titre, minutes, commun, indiv in common.PHASE_PLAN:
        p = {"n": n, "titre": titre, "minutes": minutes,
             "debut": start, "fin": start + minutes,
             "minutes_objectifs_communs": commun, "minutes_individualisees": indiv}
        if n == 1:
            p["objectif"] = level["phase1"]["objectif"]
            p["type"] = "reactivation"
        elif n == 2:
            m = MODULES[student["p1"]]
            p["objectif"] = m["titre"]
            p["skill"] = student["p1"]
            p["module"] = m
            p["type"] = "consolidation"
            p["exos"] = m["exos"]
            p["avec_exemple"] = True
        elif n == 3:
            m = MODULES[student["p2"]]
            p["objectif"] = m["titre"]
            p["skill"] = student["p2"]
            p["module"] = m
            p["type"] = "consolidation"
            p["exos"] = m["exos"][:4]
            p["avec_exemple"] = False
        elif n == 4:
            p["objectif"] = level["phase4"]["titre"]
            p["type"] = "transfert"
        else:
            p["objectif"] = "Cadrage méthodologique, sans aucune information sur le contenu de l'évaluation."
            p["type"] = "methodologie"
        out.append(p)
        start += minutes
    return out


# ------------------------------------------------- contexte de remédiation (§5)
def retention_context(student, skill_id):
    """Une réussite mesurée juste après la remédiation n'est pas une consolidation.

    Trois cas : la compétence a été retravaillée pendant la séance même (phases 2,
    3 ou 4), auquel cas la performance finale est immédiate et la rétention reste à
    vérifier ; la compétence n'a été travaillée qu'à la séance 5 du niveau ; ou la
    compétence n'a pas été retravaillée pendant la séance.
    """
    level = level_of(student)
    sk = level["skills"][skill_id]
    remediated_here = skill_id in (student["p1"], student["p2"])
    only_s5 = sk["sessions"] == ["S5"]
    introduced_here = not sk["sessions"] or sk["sessions"] == ["S5"]
    if remediated_here:
        return {"post_test_context": "immediate_after_remediation",
                "retention_status": "not_yet_verified",
                "recommended_delayed_check": True,
                "reason": "compétence retravaillée en phase 2 ou 3 de la séance, puis évaluée "
                          "moins d'une heure plus tard"}
    if only_s5:
        return {"post_test_context": "first_worked_in_session_5",
                "retention_status": "not_yet_verified",
                "recommended_delayed_check": True,
                "reason": "compétence travaillée uniquement lors de la séance 5 du niveau, "
                          "puis évaluée immédiatement"}
    if introduced_here:
        return {"post_test_context": "introduced_in_session_5",
                "retention_status": "not_yet_verified",
                "recommended_delayed_check": True,
                "reason": "contenu de l'année suivante introduit en phase 4 de la séance"}
    return {"post_test_context": "no_remediation_in_session",
            "retention_status": "not_measured",
            "recommended_delayed_check": False,
            "reason": "compétence non retravaillée pendant la séance 5 ; la performance finale "
                      "ne relève pas d'un effet de récence"}


def all_students():
    return sorted(STUDENTS, key=lambda s: (LEVEL_ORDER.index(s["level"]), s["name"]))
