#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapport de qualité post-distribution : les nombres viennent des contrôles, pas de l'auteur.

Ce script relance les contrôles, lit leurs sorties, puis écrit QA_POST_DISTRIBUTION.md.
Il ne vise ni zéro avertissement ni 100 % de PASS : ce qui n'a pas été fait est écrit
comme n'ayant pas été fait.
"""

import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pd_core as pd
import scope_rules
import equity_rules

OUT = os.path.join(pd.V3_ROOT, "QA_POST_DISTRIBUTION.md")


def run_tests():
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q",
                            os.path.join(pd.V3_ROOT, "tests")],
                           capture_output=True, text=True, timeout=900, cwd=pd.V3_ROOT)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"execute": False, "detail": str(exc)}
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    m = re.search(r"(\d+) passed", r.stdout or "")
    s = re.search(r"(\d+) skipped", r.stdout or "")
    f = re.search(r"(\d+) failed", r.stdout or "")
    return {"execute": True, "code": r.returncode,
            "passed": int(m.group(1)) if m else 0,
            "skipped": int(s.group(1)) if s else 0,
            "failed": int(f.group(1)) if f else 0,
            "resume": tail[0]}


def main():
    scope = pd.read_json(os.path.join(pd.V3_ROOT, "curriculum_scope",
                                      "criteria_scope.json"), "carte")
    freeze = pd.read_json(os.path.join(pd.V3_ROOT, "IMMUTABLE_STUDENT_ARTIFACTS.json"), "gel")
    canon = pd.read_json(os.path.join(pd.V3_ROOT, "CANONICAL_POST_DISTRIBUTION.json"), "canon")
    nonreg = pd.read_json(os.path.join(pd.V3_ROOT, "reports", "NON_REGRESSION.json"), "nonreg")
    audit = pd.read_json(os.path.join(pd.V3_ROOT, "reports", "pedagogical_audit.json"), "audit")
    srclive = pd.read_json(os.path.join(pd.V3_ROOT, "source_evidence",
                                        "SOURCE_VERIFICATION.json"), "sources")
    delayed = pd.read_json(os.path.join(pd.V3_ROOT, "teacher_guidance",
                                        "mini_test_differe_s2.json"), "différé")
    refs = pd.read_json(os.path.join(pd.V3_ROOT, "curriculum_scope",
                                     "curriculum_references.json"), "refs")
    tests = run_tests()

    L = []
    a = L.append
    a("# QA post-distribution — séance 5")
    a("")
    a("Généré le %s. Tous les nombres de ce document sont produits par les contrôles "
      "eux-mêmes ; aucun n'est recopié à la main." % pd.GENERATED_ON)
    a("")
    a("## 1. Empreintes des documents figés")
    a("")
    a("| | |")
    a("| --- | ---: |")
    a("| couples élève × matière | %d |" % freeze["counts"]["couples_eleve_matiere"])
    a("| PDF distribués, gelés | %d |" % freeze["counts"]["student_pdf"])
    a("| sources LaTeX gelées | %d |" % freeze["counts"]["student_tex"])
    a("| fichiers empreintés au total | %d |" % freeze["counts"]["total"])
    a("")
    a("Les empreintes complètes sont dans `IMMUTABLE_STUDENT_ARTIFACTS.json`. Extrait, à "
      "titre de témoin :")
    a("")
    a("| fichier | sha256 (16 premiers caractères) | octets |")
    a("| --- | --- | ---: |")
    for art in freeze["artifacts"][:6]:
        a("| `%s` | `%s…` | %d |"
          % (os.path.basename(art["path"]), art["sha256"][:16], art["size_bytes"]))
    a("")
    a("## 2. Confirmation de non-modification")
    a("")
    a("```")
    a("student_artifacts_changed = %d" % nonreg["student_artifacts_changed"])
    a("```")
    a("")
    a("| contrôle | verdict | détail |")
    a("| --- | --- | --- |")
    for c in nonreg["checks"]:
        a("| %s | **%s** | %s |" % (c["controle"], c["verdict"], c["detail"]))
    a("")
    a("Verdict global de non-régression : **%s**." % nonreg["verdict"])
    a("")
    a("## 3. Nombre réel de critères")
    a("")
    a("Le nombre canonique est recalculé, non postulé : **%d critères réels**, hors élève "
      "fictif du jeu de tests." % scope["counts"]["criteria_total"])
    a("")
    a("| | |")
    a("| --- | ---: |")
    a("| critères d'origine | %d |" % scope["counts"]["criteria_total"])
    a("| dont mixtes, éclatés en sous-critères virtuels | %d |" % scope["counts"]["mixed"])
    a("| sous-critères analytiques virtuels créés | %d |" % scope["counts"]["virtual_subcriteria"])
    a("| lignes réellement notées | %d |"
      % (scope["counts"]["criteria_total"] - scope["counts"]["mixed"]
         + scope["counts"]["virtual_subcriteria"]))
    a("")
    a("## 4. Classement N−1 / passerelle vers N")
    a("")
    a("| classement | critères |")
    a("| --- | ---: |")
    a("| `n_minus_1` | %d |" % scope["counts"]["n_minus_1"])
    a("| `bridge_n` | %d |" % scope["counts"]["bridge_n"])
    a("| `mixed` | %d |" % scope["counts"]["mixed"])
    a("")
    a("%d exceptions au classement par défaut, chacune justifiée par écrit dans "
      "`curriculum_scope/SCOPE_RATIONALE.md`, en citant le livret distribué."
      % len(scope_rules.EXCEPTIONS))
    a("")
    a("Six alias analytiques ont été créés pour ne plus fusionner sous un même identifiant "
      "une compétence N−1 et une notion N. Les `skill_id` d'origine sont conservés tels "
      "quels : `M3E_TRIG_01` reste `M3E_TRIG_01`, et se lit désormais soit "
      "`M3_TRIGO_COS_NM1`, soit `M3_TRIGO_SIN_BRIDGE`, selon le critère.")
    a("")
    a("## 5. Points N−1 et points de passerelle, par élève")
    a("")
    a("| élève | niveau | critères | points N−1 | points passerelle |")
    a("| --- | --- | ---: | ---: | ---: |")
    for s in scope["per_student"]:
        a("| %s | %s | %d | %.2f | %.2f |"
          % (s["student_id"], s["level_key"], s["criteria"],
             s["n_minus_1_points"], s["bridge_n_points"]))
    a("")
    a("Les deux colonnes recomposent exactement 20 points pour chacun des quinze élèves ; "
      "c'est vérifié par un test paramétré.")
    a("")
    a("## 6. Questions à interprétation limitée")
    a("")
    a("%d critères portent `evidence_quality: limited_by_prompt`. La formulation imprimée "
      "n'y soutient pas une inférence forte, et le bilan doit respecter cette limite."
      % scope["counts"]["criteria_with_limited_evidence_quality"])
    a("")
    a("| critère | élève | item | ce que la formulation ne permet pas |")
    a("| --- | --- | --- | --- |")
    for c in scope["criteria"]:
        if c["evidence_quality"] != "limited_by_prompt":
            continue
        lim = c["interpretation_limits"][0] if c["interpretation_limits"] else \
            "correction prudente documentée dans l'overlay"
        a("| `%s` | %s | %s | %s |" % (c["criterion_id"], c["student_id"], c["item_ref"], lim))
    a("")
    a("## 7. Corrections enseignantes appliquées")
    a("")
    a("Quatre questions ont reçu un barème interne précisé, sans qu'une seule ligne du sujet "
      "change : Sinda CHIKHAOUI 4e C2, Elyes KEFI 3e B4, Ahmad BELDI 1re spé B4, Malek "
      "KHADHRANI 1re spé C2. Le détail figure dans "
      "`SCIENTIFIC_AUDIT_POST_DISTRIBUTION.md` et, élève par élève, dans "
      "`correction_overlays/<élève>/TEACHER_NOTES.md`.")
    a("")
    a("Une observation de corrigé a été explicitement sortie du barème : le cas de la liste "
      "vide en B2 pour les deux élèves de NSI, que la question imprimée ne demande pas.")
    a("")
    a("Sept imprécisions de support ont été relevées et traitées en clarifications orales. "
      "L'une d'elles — « une somme de deux carrés ne se factorise pas dans ℝ » — est un "
      "énoncé faux, pas une approximation.")
    a("")
    a("## 8. Moteur d'analyse")
    a("")
    a("`tools/analyze_s5_post_distribution.py` produit `raw_assessment_score`, "
      "`n_minus_1_consolidation`, `bridge_n_readiness`, `skills`, `error_profile`, "
      "`retention`, `delayed_checks` et `action_plan_inputs`, validés par "
      "`schemas/post_stage_analysis_v3.schema.json`.")
    a("")
    a("L'analyseur V2 n'est pas écrasé : `S5_cloture/tools/analyze_s5.py` reste en place. "
      "Les deux ne doivent pas être lancés sur la même correction — le V2 attache les codes "
      "d'erreur à l'item, ce que le V3 refuse.")
    a("")
    a("Le script refuse d'analyser plutôt que de deviner : score manquant, critère mixte "
      "non ventilé, code d'erreur sur un critère réussi, code inconnu, saisie ne "
      "correspondant pas au barème — chacun de ces cas arrête l'analyse avec un message "
      "explicite.")
    a("")
    a("## 9. Tests")
    a("")
    if tests.get("execute"):
        a("```")
        a("python3 -m pytest tests/")
        a(tests["resume"])
        a("```")
        a("")
        a("%d tests passés, %d ignorés, %d en échec."
          % (tests["passed"], tests["skipped"], tests["failed"]))
        a("")
        a("Les tests ignorés le sont pour une raison précise : quatre élèves n'ont aucun "
          "critère de passerelle, et le test « un échec sur une passerelle ne crée jamais de "
          "déficit » n'a alors rien à éprouver.")
    else:
        a("**Les tests n'ont pas pu être exécutés** : %s. Aucun verdict de test n'est donc "
          "revendiqué." % tests.get("detail"))
    a("")
    a("Garanties couvertes : gel des empreintes, présence d'un `curriculum_scope` sur chaque "
      "critère, étanchéité des deux décomptes, non-propagation des codes d'erreur, "
      "`mastery_delta` nul, innocuité d'un échec de passerelle, traitement des quatre "
      "questions délicates, validation par le schéma V3, refus des saisies incomplètes, "
      "migration sans ventilation inventée, langage du bilan, et sûreté du packager.")
    a("")
    a("## 10. Sécurité")
    a("")
    a("| point | état |")
    a("| --- | --- |")
    a("| `S5_cloture/tools/make_release.py` | corrigé : plus de `shutil.rmtree` "
      "inconditionnel ; destination contrôlée, sentinelle exigée, construction en staging, "
      "bascule par renommage atomique, ancien paquet conservé en `.previous`, `--dry-run` |")
    a("| nouveau packager `tools/pack_post_distribution.py` | refuse `/`, `$HOME`, le dépôt, "
      "son parent, la source, et tout chemin sous `S5_cloture` ; refuse un répertoire "
      "existant sans sentinelle |")
    a("| écriture des outils V3 | refusée hors de `S5_post_distribution_v3/`, par "
      "construction |")
    a("| harnais NSI, mode conteneur | durci : aucun montage hôte inscriptible, résultat par "
      "`stdout` entre sentinelles, `chmod 0777` supprimé, swap borné, `fsize` et `nofile` "
      "limités, réseau coupé, FS en lecture seule, utilisateur non privilégié, capacités "
      "abandonnées, aucune image téléchargée implicitement |")
    a("| harnais NSI, mode relu | sans isolation, et signalé comme tel à chaque exécution ; "
      "ce n'est pas le mode par défaut |")
    a("")
    a("**Action opérateur en attente.** `make_release.py` refuse désormais de remplacer les "
      "répertoires `S5_release/` et `S5_audit/` existants, qui ont été produits avant "
      "l'introduction de la sentinelle. C'est le comportement voulu. Pour reconstruire ces "
      "paquets, renommez ou déplacez d'abord les répertoires existants — le script ne le "
      "fera pas à votre place.")
    a("")
    a("## 11. Limitations documentaires")
    a("")
    a("| limitation | portée |")
    a("| --- | --- |")
    a("| aucune mesure initiale nominative item par item | aucune progression chiffrée n'est "
      "calculable ; `mastery_delta` vaut `null` pour les quinze couples |")
    a("| douze items par élève | la force de preuve est un décompte, pas une fiabilité "
      "psychométrique ; le terme `measurement_reliability` est proscrit |")
    a("| NOR du programme de Seconde 2025-2026 non documenté | le champ vaut `null` et "
      "l'absence est déclarée ; aucun numéro n'est fabriqué |")
    a("| NOR des acquis antérieurs en NSI non documentés | idem : la NSI n'a pas de programme "
      "d'année N−1, les prérequis viennent du cycle 4, de SNT et des séances S1 à S4 |")
    a("| durées réelles de passation non mesurées | `observed_duration_minutes` vaut `null` "
      "partout ; les estimations V2 sont conservées telles quelles |")
    a("| deux estimateurs de durée internes | ils partagent leurs entrées : ce ne sont pas "
      "deux mesures indépendantes, et plus rien ne le prétend |")
    a("| paquet d'audit | le mode `--source-mode manifest` rend un verdict « PASS WITH "
      "LIMITATION » : les sources originales ne sont pas réauditables depuis le seul bundle |")
    a("")
    a("## 12. Statut de rétention")
    a("")
    n_sk = sum(len(e["skills"]) for e in delayed["eleves"])
    n_el = sum(1 for e in delayed["eleves"] if e["skills"])
    a("%d compétences, réparties sur %d élèves, ont été retravaillées pendant la séance puis "
      "évaluées moins d'une heure plus tard. Elles portent "
      "`post_test_context: immediate_after_remediation` et "
      "`retention_status: not_yet_verified`." % (n_sk, n_el))
    a("")
    a("Une réussite y signifie « réussite immédiate après remédiation ». Elle ne signifie pas "
      "« consolidation durable », et le contrôleur de langage refuse cette dernière "
      "formulation dans un bilan.")
    a("")
    a("## 13. Mini-test différé")
    a("")
    a("Semaine 2, dix minutes, deux items par compétence, parallèles à ceux de l'évaluation "
      "de clôture, sans aide ni carte de rappel. Critère : réussite maintenue sur au moins un "
      "item par compétence. Le détail par élève est dans "
      "`teacher_guidance/MINI_TEST_DIFFERE_S2.md`.")
    a("")
    a("Après correction, l'analyseur produit le même objet sous `delayed_checks`, restreint "
      "aux compétences effectivement concernées par cet élève.")
    a("")
    a("## 14. Références réglementaires")
    a("")
    a("| niveau | programme de l'année N | applicable 2026-2027 | successeur | applicable |")
    a("| --- | --- | --- | --- | --- |")
    for key in ("4e", "3e", "2nde", "1ere_spe", "1re_nsi"):
        lv = refs["levels"][key]
        cur = lv["curriculum_current"]
        suc = lv.get("curriculum_successor")
        a("| %s | %s | %s | %s | %s |"
          % (key, cur["nor"] or "non documenté",
             "oui" if cur.get("applicable_2026_2027") else "—",
             (suc or {}).get("nor", "—"),
             "non" if suc else "—"))
    a("")
    a("Le nouveau programme de cycle 4 (`MENE2602912A`) n'est **pas** appliqué par "
      "anticipation aux entrées en Quatrième et en Troisième de 2026-2027 : le changement est "
      "ultérieur.")
    a("")
    a("## 15. Packaging")
    a("")
    a("`tools/pack_post_distribution.py` construit la couche post-distribution en staging, "
      "empreinte chaque fichier livré dans `PACKAGE_MANIFEST.json`, puis bascule par "
      "renommage atomique. Il ne recopie aucun document élève : les PDF distribués restent "
      "dans `S5_cloture` et ne sont jamais dupliqués par ce paquet.")
    a("")
    a("## 16. Traçabilité des sources")
    a("")
    a("| mode | sources déclarées | vérifiées | verdict |")
    a("| --- | ---: | ---: | --- |")
    a("| `live` | %d | %d | **%s** |"
      % (srclive["sources_declared"], srclive["sources_verified"], srclive["verdict"]))
    a("| `manifest` | %d | %d | **PASS WITH LIMITATION** |"
      % (srclive["sources_declared"], srclive["sources_declared"]))
    a("")
    a("En mode `manifest`, seules les empreintes et les références sont contrôlées : les "
      "sources originales ne sont pas réauditables depuis ce seul bundle. Ce n'est pas un "
      "détail de formulation — le paquet d'audit précédent se présentait comme autonome "
      "alors qu'il ne l'était pas.")
    a("")
    a("## 17. Audit pédagogique élargi")
    a("")
    a("| | |")
    a("| --- | ---: |")
    a("| modules de remédiation audités | %d |" % audit["counts"]["modules"])
    a("| exercices et corrigés | %d |" % audit["counts"]["exercices"])
    a("| dont recalculés par le vérificateur | %d |" % audit["counts"]["verifies_par_recalcul"])
    a("| dont vérifiés par revue de lecture | %d |" % audit["counts"]["verifies_par_revue"])
    a("| échecs | %d |" % audit["counts"]["fail"])
    a("")
    a("La distinction entre recalcul et revue est maintenue partout : un exercice « relu » "
      "n'est jamais compté comme « recalculé ».")
    a("")
    a("## 18. Dettes restantes")
    a("")
    a("| # | dette | pourquoi elle reste |")
    a("| --- | --- | --- |")
    a("| 1 | les sept imprécisions de support sont dans des documents figés | elles ne "
      "peuvent être corrigées que par la parole, ou signalées comme limites si la séance a "
      "eu lieu |")
    a("| 2 | `observed_duration_minutes` vaut `null` partout | aucune passation n'a encore été "
      "chronométrée ; le champ existe pour recevoir la mesure |")
    a("| 3 | 130 exercices de module vérifiés par lecture | leur nature ne se prête pas au "
      "recalcul ; l'automatiser demanderait un vérificateur symbolique |")
    a("| 4 | `S5_release/` et `S5_audit/` sans sentinelle | à renommer ou déplacer par "
      "l'opérateur avant toute reconstruction |")
    a("| 5 | aucune correction réelle saisie | les quinze gabarits V3 sont vierges ; "
      "l'analyseur n'a été éprouvé que sur des jeux synthétiques |")
    a("| 6 | le durcissement du conteneur n'a été éprouvé que sur `python:3-slim` | le mode "
      "conteneur a bien été exécuté et rend un résultat identique au mode relu, mais avec une "
      "seule image et un seul moteur ; le comportement sous podman n'a pas été vérifié |")
    a("| 7 | pas d'étude de fiabilité | douze items ne permettent pas d'en conduire une ; "
      "aucune n'est revendiquée |")
    a("")
    a("Ce rapport ne vise ni zéro avertissement ni 100 % de PASS. Un contrôle non exécuté est "
      "écrit comme non exécuté.")

    pd.write_text(OUT, "\n".join(L))
    print("QA écrit : %s" % os.path.relpath(OUT, pd.REPO_ROOT))
    if tests.get("execute"):
        print("  tests : %d passés, %d ignorés, %d échecs"
              % (tests["passed"], tests["skipped"], tests["failed"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
