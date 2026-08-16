---
title: "Rapport final de production - Première NSI"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
# Rapport final de production - Première NSI

**Statut : `DOCUMENTATION_NSI_GO_LIVE_READY`**

# 1. Périmètre livré

Le module ajoute un stage Python complet, cinq séances de deux heures, deux parcours individualisés, les documents professeur et élève, les supports pratiques, les évaluations, le QCM candidat individuel, les fichiers Python, les packs de code et les packs PDF.

# 2. Progression

| Séance | Axe | Production |
|---:|---|---|
| 1 | exécution, types, affectations, booléens et conditions | premier programme interactif |
| 2 | `for`, `range`, `while`, compteur et accumulateur | analyse d’une liste |
| 3 | fonctions, `return`, `None`, contrats, tests et débogage | module testé |
| 4 | listes, dictionnaires, aliasing et CSV | traitement des capteurs |
| 5 | recherche, tri, dichotomie, coût et mini-projet | projet documenté et présenté |

# 3. Contrôles

| Gate | Résultat |
|---|---|
| all_sessions_120 | PASS |
| qcm_contract | PASS |
| python_compile | PASS |
| python_solutions_run | PASS |
| pdf_openable | PASS |
| pdf_a4 | PASS |
| pdf_no_blank_pages | PASS |
| links_clean | PASS |
| offline_resources | PASS |
| student_no_solution_leak | PASS |
| generic_student_no_names | PASS |
| student_code_zips_clean | PASS |
| cross_student_clean | PASS |
| all_expected_present | PASS |

# 4. Inventaire

- PDF : **56** ;
- pages PDF, sources et packs compris : **652** ;
- fichiers Markdown : **47** ;
- fichiers HTML : **45** ;
- fichiers Python : **11** ;
- packs PDF : **4** ;
- packs de code : **4** ;
- dossiers nominatifs : **2**.

# 5. Confidentialité

Le pack élève commun ne contient aucun nom complet ni corrigé. Les packs de code élève ne contiennent aucune solution. Les dossiers nominatifs sont séparés et le candidat individuel reçoit le QCM sans son corrigé. Les données du projet sont synthétiques.

# 6. Limite pédagogique

Le stage rend les élèves opérationnels en Python ; il ne prétend pas achever tout le programme annuel. La matrice annuelle organise ensuite représentation des données, Web, architecture, systèmes, réseaux, histoire de l’informatique et approfondissement algorithmique.
