#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mini-test différé de semaine 2 : ce qu'il faut revérifier, et pourquoi.

Une compétence retravaillée pendant la séance puis évaluée moins d'une heure plus tard
a été mesurée dans les conditions les plus favorables qui soient. La réussite y est
réelle, mais elle ne dit rien de la rétention. Ce document liste, élève par élève, les
compétences concernées — indépendamment des scores, qui ne sont pas encore saisis — et
les items de l'évaluation dont il faut construire des équivalents parallèles.
"""

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd

OUT_MD = os.path.join(pd.V3_ROOT, "teacher_guidance", "MINI_TEST_DIFFERE_S2.md")
OUT_JSON = os.path.join(pd.V3_ROOT, "teacher_guidance", "mini_test_differe_s2.json")


def build():
    sys.path.insert(0, pd.S5_TOOLS)
    from data.levels import LEVELS
    rows = []
    for st in pd.students():
        manifest = pd.manifest_of(st)
        skills = {}
        for it in manifest["items"]:
            for sid, ret in (it.get("retention") or {}).items():
                if not ret.get("recommended_delayed_check"):
                    continue
                s = skills.setdefault(sid, {
                    "skill_id": sid,
                    "label": LEVELS[st["level_key"]]["skills"][sid]["label"],
                    "importance_n": LEVELS[st["level_key"]]["skills"][sid]["importance_n"],
                    "post_test_context": ret.get("post_test_context"),
                    "retention_status": ret.get("retention_status"),
                    "raison": ret.get("reason"),
                    "items_paralleles": [],
                })
                s["items_paralleles"].append(it["ref"])
        rows.append({
            "student_id": st["student_id"], "student_name": st["student_name"],
            "level_key": st["level_key"], "level_label": st["level_label"],
            "subject": st["subject"],
            "semaine": 2,
            "duree_minutes": 10,
            "format": "deux items par compétence, parallèles à ceux de l'évaluation de clôture, "
                      "sans aide et sans carte de rappel",
            "critere_de_reussite": "réussite maintenue sur au moins un item par compétence",
            "obligatoire": bool(skills),
            "skills": [skills[k] for k in sorted(skills)],
        })
    return rows


def markdown(rows):
    L = []
    a = L.append
    a("# Mini-test différé — semaine 2")
    a("")
    a("**Document enseignant.** Il ne concerne aucun document déjà distribué.")
    a("")
    a("## Pourquoi")
    a("")
    a("Certaines compétences ont été retravaillées pendant les soixante-quinze minutes de "
      "travail, puis évaluées moins d'une heure plus tard. Elles ont donc été mesurées dans les "
      "conditions les plus favorables possibles. Une réussite y signifie « réussite immédiate "
      "après remédiation ». Elle ne signifie pas encore « consolidation durable », et le bilan "
      "n'a pas le droit de l'écrire.")
    a("")
    a("Le mini-test différé tranche cette question, et lui seule. Dix minutes, en semaine 2, "
      "sans aide. Il ne porte que sur les compétences listées ci-dessous.")
    a("")
    a("## Ce que le résultat autorise à écrire")
    a("")
    a("| résultat du mini-test | formulation autorisée |")
    a("| --- | --- |")
    a("| réussite maintenue | « la réussite observée en fin de stage s'est maintenue à "
      "distance » |")
    a("| réussite non maintenue | « la réussite de fin de stage n'a pas été retrouvée à "
      "distance : la compétence demande une réactivation espacée » |")
    a("| non passé | « la rétention n'a pas été vérifiée » — et rien d'autre |")
    a("")
    total = sum(len(r["skills"]) for r in rows)
    a("## Par élève")
    a("")
    a("%d compétences à revérifier au total, réparties sur %d élèves."
      % (total, sum(1 for r in rows if r["skills"])))
    a("")
    for r in rows:
        a("### %s — %s (%s)" % (r["student_name"], r["level_label"], r["subject"]))
        a("")
        if not r["skills"]:
            a("Aucune compétence évaluée immédiatement après remédiation : pas de mini-test "
              "différé pour cet élève.")
            a("")
            continue
        a("| compétence | libellé | importance | items parallèles à construire |")
        a("| --- | --- | --- | --- |")
        for s in r["skills"]:
            a("| `%s` | %s | %s | %s |"
              % (s["skill_id"], s["label"], s["importance_n"],
                 ", ".join(sorted(set(s["items_paralleles"])))))
        a("")
        a("Durée : %d minutes. Critère : %s." % (r["duree_minutes"], r["critere_de_reussite"]))
        a("")
    return "\n".join(L)


def main():
    rows = build()
    pd.write_json(OUT_JSON, {
        "schema": "nexus-s5-delayed-check-v3",
        "generated_on": pd.GENERATED_ON,
        "semaine": 2,
        "principe": ("une réussite immédiate après remédiation n'est pas une consolidation "
                     "durable ; seul un contrôle différé permet de trancher."),
        "eleves": rows,
    })
    pd.write_text(OUT_MD, markdown(rows))
    print("mini-test différé : %d compétences sur %d élèves"
          % (sum(len(r["skills"]) for r in rows), sum(1 for r in rows if r["skills"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
