#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remplit le gabarit de bilan à partir des données calculées, et d'elles seules.

Le script n'écrit aucune appréciation : il remplit les champs chiffrés et factuels
depuis `bilan_facts.json` et `four_week_action_plan.json`, puis laisse en place les
blocs `[[À RÉDIGER]]` destinés à l'enseignant. Il produit également une synthèse
enseignant plus détaillée.

USAGE
    python3 S5_cloture/tools/render_bilan.py \
        --facts   .../bilan_facts.json \
        --plan    .../four_week_action_plan.json \
        --analysis .../post_stage_analysis.json \
        --out-parents  .../BILAN_PARENTS.md \
        --out-enseignant .../SYNTHESE_ENSEIGNANT.md

Si --plan et --analysis ne sont pas fournis, ils sont cherchés à côté de --facts.
"""

import argparse
import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TEMPLATE = os.path.join(os.path.dirname(HERE), "_teacher_private", "BILAN_TEMPLATE_PARENTS.md")

MASTERY_WORDS = {0: "non maîtrisé", 1: "très fragile", 2: "partiellement maîtrisé",
                 3: "maîtrisé", 4: "maîtrise solide, transfert réussi"}

STATUT_FR = {"acquis": "acquis au positionnement initial",
             "en_voie_acquisition": "en voie d'acquisition",
             "fragile": "fragile", "non_evalue": "non évalué au positionnement initial",
             "non_travaille": "non travaillé"}


def bullets(rows, fmt):
    return "\n".join("- " + fmt(r) for r in rows) if rows else "_Aucun élément dans cette catégorie._"


def render(facts, plan, analysis, profile):
    lv_sessions = profile["trajectory"]
    sessions = "\n".join("- **%s** — %s" % (k, lv_sessions[k]["theme"])
                         for k in ("S1", "S2", "S3", "S4"))
    sessions += "\n- **S5** — réactivation, deux axes de consolidation personnels, " \
                "pont vers l'année suivante, puis évaluation finale."

    progression = (
        "_Aucune progression chiffrée ne peut être établie, et aucune ne sera écrite._\n\n"
        "Le positionnement de début de stage a fourni un **statut par domaine**, pas les réponses "
        "de votre enfant question par question. Un statut n'est pas une mesure : le convertir en "
        "note pour en soustraire une autre produirait un chiffre sans valeur. Ce compte rendu se "
        "limite donc à ce qui est réellement établi — ce qui est démontré aujourd'hui — et à une "
        "confrontation **indicative** avec le point de départ.\n\n")
    if facts["comparaison_qualitative"]:
        progression += "| Compétence | Point de départ documenté | État constaté à l'évaluation | Force de la preuve |\n"
        progression += "|---|---|---|---|\n"
        for r in facts["comparaison_qualitative"]:
            progression += "| %s | %s | %s | %s |\n" % (
                r["label"], r["statut_initial_qualitatif"].replace("_", " "),
                MASTERY_WORDS[r["maitrise_finale"]], r["evidence_strength"])
        progression += ("\n_Cette table se lit ligne par ligne. Elle ne se soustrait pas : "
                        "les deux colonnes ne sont pas mesurées sur la même échelle._\n")
    else:
        progression += "_Aucune compétence évaluée ne dispose d'un point de départ documenté._\n"

    nc = facts["contenus_nouveaux_hors_progression"]
    not_comp = ("_%d compétence(s) relèvent de notions introduites pendant la séance elle-même "
                "(%s) : elles sont notées, mais exclues de toute lecture de progression._"
                % (len(nc), ", ".join(nc))) if nc else ""
    po = facts["etat_final_seul"]
    if po:
        not_comp += ("\n\n_%d compétence(s) n'apparaissaient pas au positionnement initial (%s) : "
                     "seul l'état final est connu._" % (len(po), ", ".join(po)))

    strengths = bullets(facts["skills_demonstrated"],
                        lambda r: "**%s** — %s%s." % (
                            r["label"], MASTERY_WORDS[r["post_mastery"]],
                            " (réussite obtenue juste après la reprise en séance : à confirmer "
                            "à distance)" if r["a_confirmer_a_distance"] else ""))
    ret = facts["retention_a_verifier"]
    consolidated = (
        "_Cette section reste volontairement vide._\n\n"
        "Une consolidation durable ne se constate pas le jour même. Les compétences reprises "
        "pendant la séance ont été évaluées moins d'une heure plus tard : ce qui est mesuré est "
        "une **réussite immédiate**, ce qui est déjà un résultat, mais pas encore un acquis "
        "stabilisé.\n" if not ret else
        "_Aucune consolidation durable ne peut être affirmée à ce stade._\n\n"
        "Les compétences suivantes ont été reprises pendant la séance puis évaluées moins d'une "
        "heure après. Leur réussite est réelle, mais elle mesure une performance immédiate :\n\n"
        + bullets(ret, lambda r: "**%s**" % r["label"])
        + "\n\nUn mini-test différé est prévu en semaine 2 du plan ci-dessous : c'est lui qui "
          "permettra de parler de consolidation.\n")
    fragile = bullets(facts["skills_fragile"],
                      lambda r: "**%s** — %s (force de la preuve : %s)."
                                % (r["label"], MASTERY_WORDS[r["post_mastery"]], r["evidence_strength"]))

    prio = [p for p in facts["priorities"] if p["priority_rank"] in ("P1", "P2")]
    priorities = bullets(prio, lambda p: "`%s` **%s** — %s" % (p["priority_rank"], p["label"], p["reason"]))

    weeks = []
    for w in plan["weeks"]:
        if not w["skills"]:
            weeks.append("**Semaine %d** — aucune priorité restante ; problème mixte de réinvestissement." % w["week"])
            continue
        weeks.append("**Semaine %d** — %s\n  - objectif : %s\n  - travail : %s, %s de %d minutes"
                     "\n  - critère de réussite : %s"
                     % (w["week"], " ; ".join(w["labels"]), w["objective"], w["work_type"],
                        w["frequency"], w["duration_minutes"], w["success_criterion"]))
    dr = plan.get("delayed_retention_check") or {}
    if dr.get("obligatoire"):
        weeks.append("**Contrôle différé — semaine %d** : %s\n  - compétences : %s\n  - format : %s"
                     "\n  - critère : %s"
                     % (dr["semaine"], dr["objet"], ", ".join(dr["skills"]), dr["format"], dr["critere"]))
    fu = plan["follow_up_recommendation"]
    follow = "**%s.** %s" % (fu["proposed"].capitalize(), fu["justification"])

    by_part = " ; ".join("partie %s : %.1f / %s" % (p, v["points"], v["max_points"])
                         for p, v in sorted(facts["by_part"].items()))
    cells = facts["calibration_cells"]
    calib = ("juste et sûr : %d ; juste mais hésitant : %d ; faux et hésitant : %d ; "
             "faux mais sûr : %d ; réussite partielle non classée : %d"
             % (cells["juste_confiance_haute"], cells["juste_confiance_basse"],
                cells["faux_confiance_basse"], cells["faux_confiance_haute"],
                cells.get("partiel_non_classe", 0)))

    values = {
        "student_name": facts["student_name"], "level": facts["level"], "subject": facts["subject"],
        "analysed_on": analysis.get("analysed_on") or "date non renseignée dans le fichier de saisie",
        "baseline_summary": profile["baseline"]["summary"],
        "baseline_strengths": bullets(profile["baseline"]["strengths"], lambda x: x),
        "baseline_priorities": bullets(profile["baseline"]["priorities"], lambda x: x),
        "sessions_worked": sessions,
        "progression_block": progression, "not_comparable_block": not_comp,
        "strengths_block": strengths, "consolidated_block": consolidated,
        "fragile_block": fragile,
        "dominant_errors": ", ".join(facts["dominant_error_codes"]) or "aucun code d'erreur saisi",
        "note_sur_20": facts["note_sur_20"], "success_rate_pct": facts["success_rate_pct"],
        "by_part": by_part, "priorities_block": priorities,
        "plan_block": "\n\n".join(weeks), "follow_up_block": follow,
        "calibration": calib,
        "warnings_block": bullets(facts["warnings"], lambda x: x),
    }
    with open(TEMPLATE, encoding="utf-8") as f:
        body = f.read()
    for k, v in values.items():
        body = body.replace("{{%s}}" % k, str(v))
    return body


def render_teacher(facts, plan, analysis):
    out = ["# Synthèse enseignant — %s" % facts["student_name"],
           "",
           "> Usage interne. Ne pas transmettre aux responsables légaux.",
           "",
           "**Note : %.2f / 20** — réussite %.1f %%." % (facts["note_sur_20"], facts["success_rate_pct"]),
           "",
           "## Compétence par compétence", "",
           "| skill_id | statut initial (qualitatif) | maîtrise finale | écart | comparaison | force de preuve | contexte | priorité |",
           "|---|---|:--:|:--:|---|---|---|:--:|"]
    prio = {p["skill_id"]: p["priority_rank"] for p in analysis["priorities"]}
    for s in analysis["skills"]:
        out.append("| `%s` | %s | %d | %s | %s | %s | %s | %s |" % (
            s["skill_id"],
            s["baseline_status_qualitative"].replace("_", " "),
            s["post_mastery"],
            "non calculable",
            s["comparison_status"], s["evidence_strength"],
            s["post_test_context"].replace("_", " "), prio.get(s["skill_id"], "")))
    out += ["", "## Item par item", "",
            "| item | compétence | points | réussite | codes d'erreur | certitude |",
            "|---|---|:--:|:--:|---|:--:|"]
    for i in analysis["items"]:
        out.append("| %s | `%s` | %s / %s | %.0f %% | %s | %s |" % (
            i["ref"], i["skill_id"], i["points"], i["max_points"],
            100 * (i["success_rate"] or 0), ", ".join(i["error_codes"]) or "—",
            i["confidence"] if i["confidence"] is not None else "—"))
    out += ["", "## Profil d'erreurs", "",
            "\n".join("- `%s` : %d occurrence(s)" % (k, v)
                      for k, v in sorted(analysis["errors"]["error_profile_after"].items(),
                                         key=lambda kv: -kv[1])) or "- aucun code saisi",
            "", "## Calibration réussite / confiance", "",
            "\n".join("- %s : %d" % (k.replace("_", " "), v)
                      for k, v in analysis["confidence"]["calibration_cells"].items()),
            "", "## Avertissements produits par le calcul", "",
            "\n".join("- %s" % w for w in analysis["warnings"]),
            "", "## À reprendre à l'oral avec l'élève", "",
            "\n".join("- item %s (`%s`) : réussite %.0f %%"
                      % (i["ref"], i["skill_id"], 100 * (i["success_rate"] or 0))
                      for i in analysis["items"] if (i["success_rate"] or 0) < 0.5) or "- aucun item en dessous de 50 %"]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--facts", required=True)
    ap.add_argument("--plan")
    ap.add_argument("--analysis")
    ap.add_argument("--profile", help="student_learning_profile.json (déduit du dossier si absent)")
    ap.add_argument("--out-parents")
    ap.add_argument("--out-enseignant")
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(args.facts))
    facts = json.load(open(args.facts, encoding="utf-8"))
    plan = json.load(open(args.plan or os.path.join(base, "four_week_action_plan.json"), encoding="utf-8"))
    analysis = json.load(open(args.analysis or os.path.join(base, "post_stage_analysis.json"), encoding="utf-8"))
    profile_path = args.profile or os.path.join(base, "student_learning_profile.json")
    profile = json.load(open(profile_path, encoding="utf-8"))

    parents = render(facts, plan, analysis, profile)
    teacher = render_teacher(facts, plan, analysis)
    if args.out_parents:
        open(args.out_parents, "w", encoding="utf-8").write(parents)
        print("écrit : %s" % args.out_parents)
    else:
        print(parents)
    if args.out_enseignant:
        open(args.out_enseignant, "w", encoding="utf-8").write(teacher)
        print("écrit : %s" % args.out_enseignant)
    return 0


if __name__ == "__main__":
    sys.exit(main())
