# QA finale — Nexus S5 Correction & Bilans

Portes de qualité au 21 août 2026. Un avertissement n'est jamais requalifié en `PASS`.

| porte | verdict | ce qui l'établit |
| --- | --- | --- |
| DATA | **PASS** | 14 personnes, 15 couples, 180 items, 337 critères, 6 sous-critères, 40 contrôles différés importés depuis la couche V3 ; chaque source empreintée ; les deux décomptes recomposent 20 points pour les 15 élèves |
| IMMUTABILITY | **PASS** | 60/60 artefacts vérifiés, 0 modifié, 0 manquant, avant et après l'exécution complète de la suite |
| CORRECTION | **PASS** | invariant erreur/réussite, zéro sans cause, barème respecté, critères mixtes cohérents, machine d'état, révisions ; 10 tests |
| ANALYSIS | **PASS** | deux décomptes étanches, erreurs non propagées, `mastery_delta` nul, force de preuve à barème publié, statuts documentés ; accord chiffré avec l'analyseur V3 de référence |
| REPORTS | **PASS** | quatre documents, blocs à provenance, modification humaine préservée, versions non écrasées, manifeste par PDF |
| LATEX | **PASS** | les quatre PDF compilent ; aucun identifiant technique, aucune accolade, aucune progression chiffrée, aucune « lacune » dans le bilan parents |
| SECURITY | **PASS** | écoute locale, mot de passe exigé en mode réseau, traversées de chemin refusées, XSS échappé, LaTeX échappé, `shell=False` vérifié sur l'AST, aucun secret littéral |
| PRIVACY | **PASS** | `runtime/` exclu de Git, contrôle automatique du suivi Git, export d'un élève sans aucun autre élève, sauvegarde sans recopie des documents distribués |
| UX | **PASS WITH WARNING** | deux colonnes, mode rapide, raccourcis, autosave, badges non fondés sur la seule couleur, impression propre, repli en onglets sous 1100 px. **Rien de tout cela n'a été essayé dans un vrai navigateur par un vrai correcteur** : Playwright est absent, et l'ergonomie se juge en usage. |
| TESTS | **PASS WITH WARNING** | 92 passés, 0 échec. **1 ignoré** : le parcours navigateur, faute de Playwright. Les mêmes parcours sont couverts par TestClient, mais sans le rendu réel. |

## Statut opérationnel

```
READY_FOR_PILOT
```

Le système **n'est pas** déclaré validé en production. Le pipeline a été éprouvé sur des
jeux synthétiques ; aucune copie réelle n'a été corrigée. Le passage à
`OPERATIONALLY_VALIDATED` suppose la procédure de `PILOT_REAL_COPY_VALIDATION.md`, et une
revue humaine du premier bilan.

À compléter après le pilote :

```
Statut : ...................................
Élève pilote : ..............................
Date : ......................................
Revue par : .................................
```

## Ce qui pourrait faire échouer une porte plus tard

| porte | ce qui la ferait basculer |
| --- | --- |
| IMMUTABILITY | une régénération d'un PDF distribué, même à l'identique du texte |
| DATA | une modification d'un fichier de `S5_post_distribution_v3/` après import, non répercutée |
| ANALYSIS | une modification des seuils de statut sans mise à jour de `CORRECTION_RULES.md` |
| LATEX | une distribution LaTeX différente, ou un paquet manquant |
| PRIVACY | un `git add -f` sur `runtime/` |

## Chiffres de référence

```
immutable_artifacts_total     60
immutable_artifacts_changed    0
immutable_artifacts_missing    0

élèves × matières             15
personnes                     14
items                        180
critères                     337   (311 n_minus_1 · 23 bridge_n · 3 mixed)
sous-critères analytiques      6
lignes réellement notées     340
points bruts par élève        20

tests                         92 passés · 1 ignoré · 0 échec
```
