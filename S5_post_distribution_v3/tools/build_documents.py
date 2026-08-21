#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produit les documents lisibles de la couche post-distribution.

    curriculum_scope/SCOPE_RATIONALE.md      pourquoi chaque exception est classée ainsi
    EVALUATION_INTERPRETATION_MATRIX.md      ce que mesure réellement chaque point du sujet
    CANONICAL_POST_DISTRIBUTION.json         les nombres canoniques, recalculés et non recopiés
"""

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import scope_rules
import equity_rules

SCOPE = os.path.join(pd.V3_ROOT, "curriculum_scope", "criteria_scope.json")

COMPARAISON = {
    "indicative_skill_comparison": "confrontation indicative avec le statut de domaine initial",
    "post_only": "état final seul : aucun item initial sur cette compétence",
    "not_comparable": "hors progression : contenu introduit pendant la séance",
    "parallel_measures": "mesures parallèles",
}

INTERPRETATION = {
    "n_minus_1": "acquis N-1 : la réussite documente un prérequis ; la non-réussite peut fonder "
                 "une priorité de consolidation",
    "bridge_n": "passerelle vers N : la réussite documente une première disponibilité ; la "
                "non-réussite ne documente aucun déficit",
    "mixed": "critère mixte : voir les sous-critères analytiques",
}


def rationale():
    L = []
    a = L.append
    a("# Classement curriculaire des critères — justification")
    a("")
    a("Ce document explique, critère par critère, pourquoi un point du sujet déjà distribué "
      "compte dans la consolidation des acquis de l'année N-1 ou dans la disponibilité sur les "
      "passerelles vers l'année N. Aucune question, aucune valeur, aucun identifiant du sujet "
      "n'a été modifié.")
    a("")
    a("## La règle")
    a("")
    a("```")
    a(scope_rules.__doc__.strip())
    a("```")
    a("")
    a("## Ce que les livrets distribués déclarent eux-mêmes nouveau")
    a("")
    a("La source du classement n'est pas une opinion : c'est le livret remis à l'élève, qui "
      "énonce en phase 4, niveau par niveau, ce qui est réinvesti et ce qui est nouveau.")
    a("")
    for key in ("4e", "3e", "2nde", "1ere_spe", "1re_nsi"):
        d = scope_rules.BRIDGE_DECLARED_IN_LIVRET[key]
        a("### %s" % key)
        a("")
        a("> %s" % d["citation"])
        a("")
        for n in d["notions"]:
            a("- %s" % n)
        a("")
    a("## Règles générales de correction, applicables à tous les critères")
    a("")
    for r in equity_rules.GENERAL_RULES:
        a("- %s" % r)
    a("")
    a("## Les exceptions au classement par défaut")
    a("")
    a("Par défaut un critère est `n_minus_1` : c'est la vocation déclarée du sujet de clôture. "
      "%d critères font exception, chacun pour une raison écrite." % len(scope_rules.EXCEPTIONS))
    a("")
    scope = pd.read_json(SCOPE, "carte")
    par_id = {}
    for c in scope["criteria"]:
        par_id.setdefault((c["student_id"], c["item_ref"], c["criterion_rank"]), c)
    for (portee, ref, rank), exc in sorted(scope_rules.EXCEPTIONS.items()):
        touches = [c for c in scope["criteria"]
                   if c["item_ref"] == ref and c["criterion_rank"] == rank
                   and (c["level_key"] == portee or c["student_id"] == portee)]
        a("### `%s` / %s / critère %d — **%s**" % (portee, ref, rank, exc["scope"]))
        a("")
        if exc.get("analysis_skill_id"):
            a("Alias analytique : `%s` — %s"
              % (exc["analysis_skill_id"], exc.get("analysis_skill_label", "")))
            a("")
        a("%s" % exc["rationale"])
        a("")
        if touches:
            a("Critères concernés : %s"
              % ", ".join("`%s` (%.2f pt)" % (c["criterion_id"], c["original_points"])
                          for c in sorted(touches, key=lambda x: x["criterion_id"])))
            a("")
        for v in exc.get("virtual", []):
            a("- sous-critère virtuel `…_%s` : %d %% des points, %s — %s"
              % (v["suffix"], round(100 * v["share"]), v["scope"], v["desc"]))
        if exc.get("virtual"):
            a("")
        for m in exc.get("accepted_methods", []):
            a("- méthode acceptée : %s" % m)
        for r in exc.get("fairness_rules", []):
            a("- règle d'équité : %s" % r)
        for l in exc.get("interpretation_limits", []):
            a("- limite d'interprétation : %s" % l)
        a("")
    a("## Ce que ce classement change, chiffres à l'appui")
    a("")
    a("| élève | niveau | critères | points N-1 | points passerelle | critères mixtes |")
    a("| --- | --- | ---: | ---: | ---: | ---: |")
    for s in scope["per_student"]:
        a("| %s | %s | %d | %.2f | %.2f | %d |"
          % (s["student_id"], s["level_key"], s["criteria"], s["n_minus_1_points"],
             s["bridge_n_points"], s["mixed_criteria"]))
    a("")
    a("Quatre élèves — Ahmed BAKIR, Noa MANIACI, Fares DARGHOUTH et Sinda CHIKHAOUI — n'ont "
      "aucun critère de passerelle : leur sujet de clôture porte intégralement sur des acquis de "
      "l'année N-1. Leur score brut reste néanmoins un score brut, et non un diagnostic complet : "
      "douze items ne mesurent pas une année.")
    return "\n".join(L)


def matrix():
    scope = pd.read_json(SCOPE, "carte")
    by_student = {}
    for c in scope["criteria"]:
        by_student.setdefault(c["student_id"], []).append(c)
    L = []
    a = L.append
    a("# Matrice d'interprétation des quinze évaluations")
    a("")
    a("Ce document répond à une seule question, pour chacun des %d critères réellement "
      "imprimés : **que mesure ce point, et qu'a-t-on le droit d'en conclure ?**"
      % scope["counts"]["criteria_total"])
    a("")
    a("Les sujets ne sont pas modifiés. Les identifiants, les points et l'ordre des questions "
      "sont ceux des documents distribués.")
    a("")
    a("Légende des colonnes :")
    a("")
    a("- **scope** — `n_minus_1` : acquis de l'année précédente ; `bridge_n` : passerelle vers "
      "l'année à venir ; `mixed` : critère indivisible, éclaté en sous-critères analytiques.")
    a("- **preuve** — nature de la tâche : automatisme, procédure, justification, contrôle, "
      "transfert, communication.")
    a("- **comparaison initiale** — ce que le diagnostic de début de stage permet de confronter.")
    a("- **récence** — `immédiat` signale une compétence retravaillée moins d'une heure avant "
      "l'évaluation : la réussite y mesure une performance immédiate, pas une consolidation.")
    a("- **interprétation autorisée** — ce qui peut être écrit, et rien de plus.")
    a("")
    for st in pd.students():
        crits = by_student[st["student_id"]]
        manifest = pd.manifest_of(st)
        items = {i["ref"]: i for i in manifest["items"]}
        profile = pd.profile_of(st)
        baseline = {r["skill_id"]: r for r in profile["baseline"]["skills"]}
        n1 = round(sum(c["original_points"] for c in crits if c["curriculum_scope"] == "n_minus_1")
                   + sum(v["points"] for c in crits if c["curriculum_scope"] == "mixed"
                         for v in c["virtual_subcriteria"]
                         if v["curriculum_scope"] == "n_minus_1"), 2)
        br = round(sum(c["original_points"] for c in crits if c["curriculum_scope"] == "bridge_n")
                   + sum(v["points"] for c in crits if c["curriculum_scope"] == "mixed"
                         for v in c["virtual_subcriteria"]
                         if v["curriculum_scope"] == "bridge_n"), 2)
        a("---")
        a("")
        a("## %s — %s (%s)" % (st["student_name"], st["level_label"], st["subject"]))
        a("")
        a("%d critères ; %.2f points d'acquis N-1 ; %.2f points de passerelle ; "
          "score brut au sujet de clôture sur 20." % (len(crits), n1, br))
        a("")
        a("| item | critère | pts | compétence d'analyse | scope | preuve | comparaison initiale "
          "| récence | interprétation autorisée |")
        a("| --- | --- | ---: | --- | --- | --- | --- | --- | --- |")
        for c in sorted(crits, key=lambda x: (list(items).index(x["item_ref"]),
                                              x["criterion_rank"])):
            it = items[c["item_ref"]]
            ret = (it.get("retention") or {}).get(c["original_skill_id"]) or {}
            recence = "immédiat" if ret.get("recommended_delayed_check") else "—"
            base = baseline.get(c["original_skill_id"], {}).get("statut_avant_s5")
            comp = COMPARAISON.get(it["comparison_status"], it["comparison_status"])
            if base and it["comparison_status"] == "indicative_skill_comparison":
                comp += " (« %s »)" % base.replace("_", " ")
            interp = INTERPRETATION[c["curriculum_scope"]]
            if c["evidence_quality"] == "limited_by_prompt":
                interp += " — énoncé à interprétation limitée"
            a("| %s | `%s` | %.2f | `%s` | %s | %s | %s | %s | %s |"
              % (c["item_ref"], c["criterion_id"], c["original_points"],
                 c["analysis_skill_id"], c["curriculum_scope"], c["evidence_type"],
                 comp, recence, interp))
            for v in c.get("virtual_subcriteria", []):
                a("| %s | ↳ `%s` | %.2f | `%s` | %s | %s | %s | %s | %s |"
                  % (c["item_ref"], v["virtual_criterion_id"], v["points"],
                     v["analysis_skill_id"], v["curriculum_scope"], c["evidence_type"],
                     comp, recence, INTERPRETATION[v["curriculum_scope"]]))
        a("")
        limites = [c for c in crits if c["interpretation_limits"]]
        if limites:
            a("**Limites d'interprétation déclarées**")
            a("")
            for c in limites:
                for l in c["interpretation_limits"]:
                    a("- `%s` — %s" % (c["criterion_id"], l))
            a("")
    return "\n".join(L)


def canonical():
    scope = pd.read_json(SCOPE, "carte")
    freeze = pd.read_json(os.path.join(pd.V3_ROOT, "IMMUTABLE_STUDENT_ARTIFACTS.json"), "gel")
    audit = pd.read_json(os.path.join(pd.V3_ROOT, "reports", "pedagogical_audit.json"), "audit")
    src = pd.read_json(os.path.join(pd.V3_ROOT, "source_evidence",
                                    "SOURCE_VERIFICATION.json"), "sources")
    nonreg = pd.read_json(os.path.join(pd.V3_ROOT, "reports", "NON_REGRESSION.json"), "nonreg")
    per = {s["student_id"]: s for s in scope["per_student"]}
    return {
        "schema": "nexus-s5-canonical-post-distribution-v3",
        "generated_on": pd.GENERATED_ON,
        "principe": ("on ne modifie pas ce que l'élève a reçu ; on améliore ce que nous pouvons "
                     "légitimement conclure de ce qu'il a produit."),
        "artefacts_eleves": {
            "couples_eleve_matiere": freeze["counts"]["couples_eleve_matiere"],
            "pdf_distribues": freeze["counts"]["student_pdf"],
            "sources_latex_gelees": freeze["counts"]["student_tex"],
            "fichiers_geles": freeze["counts"]["total"],
            "student_artifacts_changed": nonreg["student_artifacts_changed"],
        },
        "bareme": {
            "criteres_reels": scope["counts"]["criteria_total"],
            "criteres_n_minus_1": scope["counts"]["n_minus_1"],
            "criteres_bridge_n": scope["counts"]["bridge_n"],
            "criteres_mixtes": scope["counts"]["mixed"],
            "sous_criteres_analytiques_virtuels": scope["counts"]["virtual_subcriteria"],
            "criteres_a_interpretation_limitee":
                scope["counts"]["criteria_with_limited_evidence_quality"],
            "points_bruts_par_eleve": 20,
        },
        "repartition_par_eleve": {
            sid: {"niveau": p["level_key"], "criteres": p["criteria"],
                  "points_n_minus_1": p["n_minus_1_points"],
                  "points_bridge_n": p["bridge_n_points"],
                  "criteres_mixtes": p["mixed_criteria"]}
            for sid, p in sorted(per.items())
        },
        "audit_pedagogique": audit["counts"],
        "tracabilite_des_sources": {
            "mode": src["source_mode"],
            "sources_declarees": src["sources_declared"],
            "sources_verifiees": src["sources_verified"],
            "verdict": src["verdict"],
        },
        "non_regression": {"verdict": nonreg["verdict"],
                           "controles": [{"controle": c["controle"], "verdict": c["verdict"]}
                                         for c in nonreg["checks"]]},
        "interdits": {
            "progression_chiffree": "impossible : aucune mesure initiale nominative appariée",
            "mastery_delta": None,
            "deficit_sur_passerelle": "interdit : un échec bridge_n ne produit ni P1, ni P2, "
                                      "ni « non acquis », ni « lacune »",
        },
    }


def main():
    pd.write_text(os.path.join(pd.V3_ROOT, "curriculum_scope", "SCOPE_RATIONALE.md"), rationale())
    pd.write_text(os.path.join(pd.V3_ROOT, "EVALUATION_INTERPRETATION_MATRIX.md"), matrix())
    pd.write_json(os.path.join(pd.V3_ROOT, "CANONICAL_POST_DISTRIBUTION.json"), canonical())
    print("SCOPE_RATIONALE.md, EVALUATION_INTERPRETATION_MATRIX.md et "
          "CANONICAL_POST_DISTRIBUTION.json écrits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
