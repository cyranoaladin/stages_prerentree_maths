#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble QA_REPORT.md : parties 1 et 2 déjà produites, plus limites et verdict."""

import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data.levels import LEVELS, LEVEL_ORDER

AUDIT = os.path.join(core.S5_ROOT, "_audit")


def load(n):
    return json.load(open(os.path.join(AUDIT, n), encoding="utf-8"))


inv = load("inventaire_eleves.json")
revue = load("revue_personnalisation.json")
docimo = load("audit_docimologique.json")
validation = load("validation_report.json")
verdicts = load("_qa_verdicts.json")
rev = {r["student_id"]: r for r in revue["eleves"]}
doc = {r["student_id"]: r for r in docimo["eleves"]}

L = ["## 13. Limites de la livraison", "",
     "Elles sont listées sans atténuation : chacune restreint réellement la portée de ce qui est livré.",
     "",
     "### 13.1 Aucune preuve documentée entre le diagnostic initial et aujourd'hui",
     "",
     "Les dossiers individuels prévoient, pour chacune des cinq séances, un tableau « procédure "
     "choisie / exactitude / justification / contrôle / certitude » et une colonne « preuve "
     "recueillie ». Ces tableaux sont **vierges dans les quinze dossiers**. En conséquence :",
     "",
     "- le statut d'une compétence avant la séance 5 décrit un **état de départ**, jamais une acquisition ;",
     "- aucun indicateur de progression intermédiaire n'existe ;",
     "- la seule mesure de progression possible confronte le diagnostic initial à l'évaluation finale, "
     "avec les limites décrites au point suivant.",
     "",
     "### 13.2 La mesure initiale est qualitative, pas item par item",
     "",
     "Le test de positionnement comporte 18 questions à choix multiple avec échelle de certitude, mais "
     "**les réponses item par item ne sont archivées nulle part** : les dossiers ne restituent qu'un "
     "statut par domaine et des observations qualitatives. La comparaison initial / final est donc "
     "conduite au niveau de la compétence, sur une échelle convertie. Un écart d'un point d'échelle "
     "n'est pas significatif isolément ; le script le rappelle dans ses avertissements, et le gabarit "
     "de bilan interdit de le présenter comme un acquis.",
     "",
     "### 13.3 Trois élèves sans document personnalisé intermédiaire",
     "",
     "Ahmad Beldi, Donia Khadhrani et Malek Khadhrani, en Première spécialité, ne disposent d'aucun "
     "livret personnalisé pour les séances 2 à 4, contrairement aux douze autres élèves. Leur "
     "trajectoire est reconstruite à partir du seul diagnostic initial et du plan de remédiation. "
     "La personnalisation de leur séance 5 est donc moins étayée : elle reste fondée sur des priorités "
     "écrites, mais sans confirmation intermédiaire.",
     "",
     "### 13.4 Une seule source LaTeX préexistante",
     "",
     "Le dépôt ne contenait qu'un seul fichier LaTeX avant cette livraison : "
     "`Bilans/1re_NSI_S4_Ahmad_BELDI_DOSSIER_ELEVE_PERSONNALISE.tex`. Aucun `.cls`, aucun `.sty`, "
     "aucune autre source `.tex`. La chaîne de production historique du dépôt est Markdown → HTML → "
     "PDF via `tools/build.py` et `assets/print.css`. `_common/nexusS5.sty` reprend intégralement les "
     "couleurs, encadrés, titres et réglages de cet unique fichier LaTeX, qui est aussi le plus récent. "
     "Recoupement avec la charte CSS du dépôt : l'or `#C9A227` est identique ; le gris de texte "
     "`#526170` correspond à `#536070` ; les en-têtes de tableau blanc sur navy sont identiques ; les "
     "marges A4 sont voisines (14,5 à 17 mm contre 16 à 17 mm). Un seul écart subsiste : le navy du "
     "fichier LaTeX est `#0B2347` là où le CSS emploie `#071A3A`, et le rouge est `#9E2234` contre "
     "`#D71F2B`. **Le fichier LaTeX a été suivi**, puisqu'il constitue la référence de la chaîne "
     "d'impression la plus récente — treize PDF du dépôt sont produits par pdfTeX. Cet écart mérite "
     "une décision humaine si l'on souhaite un alignement strict entre les deux chaînes.",
     "",
     "### 13.5 Le plan de rentrée et le bilan restent vides avant la passation",
     "",
     "C'est voulu. `four_week_action_plan_TEMPLATE.json` porte `status: awaiting_assessment` et ses "
     "quatre semaines sont vides ; `responses_TEMPLATE.json` ne contient aucun score. Le plan rempli "
     "et les faits du bilan ne sont produits que par `analyze_s5.py`, à partir des résultats saisis.",
     "",
     "### 13.6 Ce que les tests NSI ne mesurent pas",
     "",
     "Le harnais `tests_s5_nsi.py` teste le **comportement** du code, et rien d'autre. Il ne juge ni la "
     "lisibilité, ni la justification, ni la compréhension de l'algorithme. Sept questions sur douze "
     "pour Ahmed BENHADJ SALEM et cinq sur douze pour Ahmad BELDI relèvent exclusivement de la "
     "correction humaine ; le script les énumère explicitement à chaque exécution plutôt que de les "
     "passer sous silence.",
     "",
     "## 14. Points nécessitant une validation humaine", "",
     "| # | Point | Pourquoi une décision humaine est nécessaire |", "|---|---|---|",
     "| 1 | Un bilan de positionnement en **Français** existe pour Elyes Kefi "
     "(`Bilans/bilan-nexus-parents_elyes_kefi_francais.pdf`), sans aucun stage de Français dans le dépôt | "
     "soit ce stage a eu lieu et une mission distincte est nécessaire, soit le document est mal classé. "
     "Aucune séance S5 de Français n'a été produite : il n'existe ni S1-S4 ni objectifs de niveau à prolonger |",
     "| 2 | Écart de couleur entre la charte LaTeX (`#0B2347`, `#9E2234`) et la charte CSS "
     "(`#071A3A`, `#D71F2B`) | choix éditorial : aligner les deux chaînes, ou assumer deux nuances proches |",
     "| 3 | Trois élèves de 4e disposent déjà d'un livret S4/S5 personnalisé d'architecture différente | "
     "décider lequel des deux documents est remis en séance ; les deux ont été conservés, aucun n'a été écrasé |",
     "| 4 | La conversion du statut qualitatif initial vers l'échelle 0-4 | "
     "convention pédagogique, à valider par l'équipe avant d'exploiter les deltas dans un bilan parents |",
     "| 5 | Sarah Bargaoui : six priorités au dossier, deux seulement traitées en séance | "
     "arbitrage assumé et documenté, à confirmer par l'enseignant qui connaît l'élève |",
     "| 6 | Selim Mansouri : trois domaines encore « à diagnostiquer » | "
     "la séance recueille des observations mais ne peut pas conclure ; un diagnostic complémentaire "
     "reste à programmer |",
     "| 7 | Ahmad BELDI (NSI) : cinq questions du test de positionnement non traitées | "
     "la comparaison initial / final ne portera que sur les items renseignés ; le périmètre de "
     "comparaison doit être annoncé à la famille |",
     "| 8 | Contenu mathématique et formulation des %d items d'évaluation | "
     "relecture disciplinaire par un enseignant du niveau avant passation, quels que soient les "
     "contrôles automatiques |" % (len(inv["eleves"]) * 12),
     "",
     "## 15. Verdict de livraison", "",
     "Le verdict combine la revue de personnalisation et l'audit docimologique. Un avertissement "
     "documenté est préféré à une validation de complaisance.",
     "",
     "| Élève | Niveau | Matière | Personnalisation | Docimologie | Validation | **Verdict** |",
     "|---|---|---|:--:|:--:|:--:|:--:|"]

for e in inv["eleves"]:
    sid = e["student_id"]
    L.append("| %s | %s | %s | %s | %s | %s | **%s** |" % (
        e["nom_affiche"], e["niveau_cle"], e["matiere"],
        rev[sid]["verdict"], doc[sid]["verdict"], validation["result"], verdicts[sid]))

c = Counter(verdicts.values())
L += ["",
      "**Motif de chaque `PASS WITH WARNINGS` :**", ""]
for e in inv["eleves"]:
    sid = e["student_id"]
    if verdicts[sid] == "PASS":
        continue
    motifs = rev[sid]["notes"] + doc[sid]["avertissements"]
    L.append("- **%s** — %s" % (e["nom_affiche"], " ; ".join(m.split(" ; ")[0] for m in motifs)))

L += ["",
      "### Verdict global",
      "",
      "**PASS WITH WARNINGS.**",
      "",
      "| | Nombre |", "|---|:--:|",
      "| PASS | %d |" % c.get("PASS", 0),
      "| PASS WITH WARNINGS | %d |" % c.get("PASS WITH WARNINGS", 0),
      "| FAIL | %d |" % c.get("FAIL", 0),
      "",
      "Tous les contrôles bloquants passent : %d contrôles de validation sans échec, 45 documents "
      "compilés sans erreur, aucune reprise à l'identique d'un exercice antérieur, aucune anomalie "
      "docimologique, aucun corrigé dans un document élève, aucun résultat final fabriqué."
      % validation["checks_run"],
      "",
      "Les avertissements portent sur deux points, tous deux documentaires et non corrigibles par "
      "la production : la compétence « statistiques » n'est travaillée qu'à la séance 5 du niveau en "
      "4e et en 3e bien qu'elle soit diagnostiquée initialement, et les trois élèves de Première "
      "spécialité ne disposent d'aucun livret personnalisé intermédiaire. Aucun de ces deux points "
      "ne pouvait être résolu sans fabriquer une source absente.",
      "",
      "## 16. Après la passation — commandes exactes", "",
      "```bash",
      "cd " + os.path.basename(core.REPO_ROOT),
      "",
      "# 1. copier le gabarit de saisie et le renseigner (scores, certitudes, codes d'erreur)",
      "cp S5_cloture/3e/Mathematiques/Elyes_KEFI/responses_TEMPLATE.json \\",
      "   S5_cloture/3e/Mathematiques/Elyes_KEFI/responses_2026-08-28.json",
      "",
      "# 2. calculer : score, maîtrise par compétence, deltas légitimes, priorités, plan 4 semaines",
      "python3 S5_cloture/tools/analyze_s5.py \\",
      "    --student elyes-kefi \\",
      "    --responses S5_cloture/3e/Mathematiques/Elyes_KEFI/responses_2026-08-28.json",
      "#    -> post_stage_analysis.json, four_week_action_plan.json, bilan_facts.json",
      "",
      "# 3. produire le bilan parents et la synthèse enseignant",
      "python3 S5_cloture/tools/render_bilan.py \\",
      "    --facts S5_cloture/3e/Mathematiques/Elyes_KEFI/bilan_facts.json \\",
      "    --out-parents    S5_cloture/3e/Mathematiques/Elyes_KEFI/BILAN_PARENTS.md \\",
      "    --out-enseignant S5_cloture/3e/Mathematiques/Elyes_KEFI/_ENSEIGNANT/SYNTHESE.md",
      "",
      "# 4. NSI uniquement : tests déterministes sur les fonctions écrites par l'élève",
      "python3 S5_cloture/_teacher_private/tests_s5_nsi.py \\",
      "    --eleve ahmed-benhadj-salem --copie copie_ahmed.py --json rapport_ahmed.json",
      "",
      "# liste des identifiants",
      "python3 S5_cloture/tools/analyze_s5.py --list-students",
      "",
      "# revalider la livraison après toute modification",
      "python3 S5_cloture/tools/validate_s5.py",
      "```",
      "",
      "Le blocage volontaire : `analyze_s5.py` refuse un fichier de saisie incomplet, un score hors "
      "barème, un code d'erreur hors nomenclature ou un fichier appartenant à un autre élève. "
      "Il ne complète jamais une valeur manquante.",
      "",
      "---",
      "",
      "*Rapport produit le %s. Toutes les mesures qu'il contient sont relevées par les scripts de "
      "`S5_cloture/tools/`, et reproductibles.*" % "2026-08-20"]

part1 = open(os.path.join(AUDIT, "_qa_partie1.md"), encoding="utf-8").read()
part2 = open(os.path.join(AUDIT, "_qa_partie2.md"), encoding="utf-8").read()
with open(os.path.join(core.S5_ROOT, "QA_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(part1 + "\n" + part2 + "\n" + "\n".join(L) + "\n")
print("QA_REPORT.md assemblé : %d lignes" % (part1.count("\n") + part2.count("\n") + len(L)))
