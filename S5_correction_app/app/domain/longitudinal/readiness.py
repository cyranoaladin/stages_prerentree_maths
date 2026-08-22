# -*- coding: utf-8 -*-
"""État de préparation d'un couple élève × matière, avant la première correction.

Aucun élève ne doit rester dans un état implicite. Chacun reçoit l'un de trois
états, et la différence entre les deux premiers est le point qui compte :

``READY_FOR_CORRECTION``
    tout est là.

``READY_WITH_DOCUMENTARY_WARNING``
    il manque un document, le bilan reste produisible, et le manque sera écrit
    dans le bilan. Un dossier de séance personnalisé absent relève de ce cas :
    la séance de niveau est connue, la personnalisation ne l'est pas, et rien ne
    sera inventé pour combler le trou.

``BLOCKED``
    une donnée indispensable manque réellement : sans elle, le bilan mentirait ou
    n'existerait pas. Le barème introuvable, les points qui ne se recomposent pas,
    un artefact distribué modifié.

La règle qui gouverne le classement : **un manque documentaire n'est pas un
blocage**. Il devient une limite d'interprétation écrite, ce qui est le
comportement honnête. On ne bloque que ce qui empêche de produire un document vrai.
"""

import json

from ...models import Assessment, BaselineStatus, Student
from ... import latex_html
from .. import correction as corr
from .. import immutability
from . import sources as sources_module

READY = "READY_FOR_CORRECTION"
WARNING = "READY_WITH_DOCUMENTARY_WARNING"
BLOCKED = "BLOCKED"


def _profile_for(assessment, config_module):
    """Profil d'apprentissage de l'élève, retrouvé à sa source."""
    for candidat in config_module.CLOTURE_ROOT.rglob("student_learning_profile.json"):
        try:
            donnees = json.loads(candidat.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if (donnees.get("student") or {}).get("id") == assessment.student_id:
            return donnees, candidat
    return None, None


def _check_assessment(assessment) -> list:
    """Blocages réels sur la définition de l'évaluation."""
    blocages = []
    items = list(assessment.items)
    if not items:
        blocages.append("aucun item n'est défini pour cette évaluation")
        return blocages

    lignes = corr.scoring_rows(assessment)
    if not lignes:
        blocages.append("aucun critère de notation n'est défini")
        return blocages

    somme = sum(r["max_score_centi"] for r in lignes)
    if somme != assessment.max_points_centi:
        blocages.append(
            "les points ne se recomposent pas : %s centièmes répartis pour un total "
            "imprimé de %s" % (somme, assessment.max_points_centi))

    identifiants = [r["scoring_id"] for r in lignes]
    if len(identifiants) != len(set(identifiants)):
        blocages.append("deux lignes de notation portent le même identifiant")

    for ligne in lignes:
        if ligne["curriculum_scope"] not in ("n_minus_1", "bridge_n"):
            blocages.append("périmètre curriculaire inconnu sur %s : %s"
                            % (ligne["scoring_id"], ligne["curriculum_scope"]))
            break
        if not ligne["analysis_skill_id"]:
            blocages.append("aucune compétence d'analyse sur %s" % ligne["scoring_id"])
            break

    # Un critère mixte doit se recomposer exactement, sans perte ni duplication.
    for item in items:
        for critere in item.criteria:
            if critere.curriculum_scope == "mixed":
                parties = list(critere.virtual_parts)
                if not parties:
                    blocages.append("le critère mixte %s n'a pas de sous-critère"
                                    % critere.criterion_id)
                elif sum(p.max_score_centi for p in parties) != critere.max_score_centi:
                    blocages.append("les sous-critères de %s ne totalisent pas ses points"
                                    % critere.criterion_id)
    return blocages


def _check_rendering(assessment) -> dict:
    """Le rendu web couvre-t-il les énoncés de cette évaluation ?

    Une structure sans conversion n'est pas un blocage : elle produit un renvoi au
    PDF distribué, qui reste affiché. Elle est seulement signalée.
    """
    non_couvertes, avec_repli = set(), 0
    for item in assessment.items:
        for champ in (item.statement, item.expected_answer):
            restantes = latex_html.unsupported_structures(champ)
            if restantes:
                non_couvertes.update(restantes)
                avec_repli += 1
        rendu = str(latex_html.render_statement(item.statement))
        if "\\begin{" in rendu or "\\item" in rendu:
            non_couvertes.add("rendu brut résiduel sur %s" % item.item_id)
    return {"compatible": True, "fallbacks": avec_repli,
            "structures_without_conversion": sorted(non_couvertes)}


def _check_documents(assessment, config_module) -> dict:
    """Sources documentaires : le diagnostic, les cinq séances, la personnalisation."""
    profil, chemin = _profile_for(assessment, config_module)
    if profil is None:
        return {"profile_found": False, "sources": [], "missing": [],
                "diagnostic": {"available": False}, "sessions": {}}

    releves = sources_module.collect(profil, chemin)
    base = profil.get("baseline") or {}
    trajectoire = profil.get("trajectory") or {}

    par_seance = {}
    for cle in sources_module.SESSIONS:
        materiel = [r for r in releves
                    if r["role"] == "session_material"
                    and cle in (r.get("sessions_covered") or [r.get("session")])]
        personnalise = [r for r in releves
                        if r["role"] == "personalised_session_dossier"
                        and r["present"]
                        and cle in (r.get("sessions_covered") or [r.get("session")])]
        theme = (trajectoire.get(cle) or {}).get("theme")
        if cle == "S5" and not theme:
            theme = (profil.get("session5") or {}).get("objective")
        par_seance[cle] = {
            "theme": theme,
            "general_material": bool(materiel and materiel[0]["present"]),
            "personalised_dossier": bool(personnalise),
            "observations_recorded": bool((trajectoire.get(cle) or {})
                                          .get("documented_evidence")),
        }

    return {
        "profile_found": True,
        "profile_path": str(chemin),
        "sources": releves,
        "missing": sources_module.missing(releves),
        "diagnostic": {
            "available": bool(base.get("available")),
            "instrument": (base.get("instrument") or {}).get("name"),
            "date": base.get("date"),
            "domains": len(base.get("domain_observations") or []),
            "skills": len(base.get("skills") or []),
            "item_level_results_available": bool(base.get("item_level_results_available")),
        },
        "sessions": par_seance,
    }


def evaluate(session, assessment, config_module, immutability_report=None) -> dict:
    """État de préparation complet d'un couple élève × matière."""
    blocages, avertissements = [], []

    rapport = immutability_report or immutability.verify()
    if not rapport.ok:
        blocages.append("des artefacts distribués ne correspondent plus à leur empreinte")

    blocages += _check_assessment(assessment)
    documents = _check_documents(assessment, config_module)
    rendu = _check_rendering(assessment)

    if not documents["profile_found"]:
        # Sans profil, le diagnostic et la trajectoire sont introuvables : le bilan
        # longitudinal ne peut pas être reconstitué honnêtement.
        blocages.append("aucun profil d'apprentissage n'a été trouvé pour cet élève")
    else:
        if not documents["diagnostic"]["available"]:
            avertissements.append(
                "le dossier disponible ne permet pas de reconstituer un positionnement "
                "initial complet ; le bilan le dira et ne proposera aucune comparaison")
        else:
            # Le diagnostic existe, mais son niveau de détail varie selon les
            # dossiers : onze profils sur quinze n'ont pas d'observation rédigée
            # par domaine. Les statuts par compétence, eux, sont présents partout
            # — la trajectoire reste donc calculable, seule la prose de la page
            # « situation de départ » sera plus brève.
            if not documents["diagnostic"]["domains"]:
                avertissements.append(
                    "le diagnostic ne comporte aucune observation rédigée par domaine : "
                    "la situation de départ du bilan restera brève, appuyée sur les "
                    "points d'appui et les priorités")
            if not documents["diagnostic"]["skills"]:
                blocages.append(
                    "le diagnostic ne porte aucun statut par compétence : la "
                    "trajectoire longitudinale ne peut pas être établie")
        for cle, etat in documents["sessions"].items():
            if not etat["general_material"]:
                avertissements.append("aucun matériel de séance trouvé pour %s" % cle)
            elif not etat["personalised_dossier"]:
                avertissements.append(
                    "%s : aucun dossier personnalisé ; la séance de niveau est connue, "
                    "la personnalisation ne l'est pas" % cle)
        if not any(e["observations_recorded"] for e in documents["sessions"].values()):
            avertissements.append(
                "aucune observation de séance n'a été saisie : « travaillé » ne vaudra "
                "jamais « acquis » dans le bilan")

    if rendu["structures_without_conversion"]:
        avertissements.append(
            "structures d'énoncé sans conversion, renvoyées au PDF : %s"
            % ", ".join(rendu["structures_without_conversion"]))

    baselines = session.query(BaselineStatus).filter_by(
        student_id=assessment.student_id).count()
    if documents["profile_found"] and not baselines:
        avertissements.append("aucun statut initial n'a été importé pour cet élève")

    lignes = corr.scoring_rows(assessment) if assessment.items else []
    etat = BLOCKED if blocages else (WARNING if avertissements else READY)

    return {
        "assessment_id": assessment.assessment_id,
        "student_id": assessment.student_id,
        "display_name": assessment.student.person.display_name,
        "level_key": assessment.level_key,
        "level_label": assessment.student.level_label,
        "diagnostic": documents["diagnostic"],
        "sessions": documents["sessions"],
        "personalized_sources": [r["source_path"] for r in documents["sources"]
                                 if r["role"] == "personalised_session_dossier"
                                 and r["present"]],
        "missing_sources": [{"role": r["role"], "session": r["session"],
                             "note": r["note"]} for r in documents["missing"]],
        "final_assessment": {
            "items": len(assessment.items),
            "scoring_lines": len(lignes),
            "original_criteria": len({r["criterion_id"] for r in lignes}),
            "max_points_centi": assessment.max_points_centi,
            "n_minus_1_centi": sum(r["max_score_centi"] for r in lignes
                                   if r["curriculum_scope"] == "n_minus_1"),
            "bridge_n_centi": sum(r["max_score_centi"] for r in lignes
                                  if r["curriculum_scope"] == "bridge_n"),
            "defined": bool(lignes),
        },
        "web_rendering": rendu,
        "correction_possible": not blocages,
        "analysis_possible": not blocages,
        "longitudinal_report": {
            "ready": not blocages,
            "warnings": avertissements,
        },
        "four_week_plan": {"ready": not blocages},
        "blockers": blocages,
        "status": etat,
    }


def evaluate_all(session, config_module) -> list:
    """État de préparation des quinze couples, dans l'ordre alphabétique."""
    rapport = immutability.verify()
    sortie = []
    for student in session.query(Student).order_by(Student.student_id).all():
        assessment = session.query(Assessment).filter_by(
            student_id=student.student_id).one_or_none()
        if assessment is None:
            sortie.append({
                "student_id": student.student_id,
                "display_name": student.person.display_name,
                "status": BLOCKED,
                "blockers": ["aucune évaluation finale n'est définie pour cet élève"],
                "longitudinal_report": {"ready": False, "warnings": []},
            })
            continue
        sortie.append(evaluate(session, assessment, config_module, rapport))
    return sortie


def summary(etats) -> dict:
    compte = {READY: 0, WARNING: 0, BLOCKED: 0}
    for etat in etats:
        compte[etat["status"]] = compte.get(etat["status"], 0) + 1
    return {"total": len(etats), "ready": compte[READY],
            "ready_with_warning": compte[WARNING], "blocked": compte[BLOCKED],
            "all_correctable": compte[BLOCKED] == 0}
