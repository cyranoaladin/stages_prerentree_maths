# QA post-distribution — séance 5

Généré le 2026-08-21. Tous les nombres de ce document sont produits par les contrôles eux-mêmes ; aucun n'est recopié à la main.

## 1. Empreintes des documents figés

| | |
| --- | ---: |
| couples élève × matière | 15 |
| PDF distribués, gelés | 30 |
| sources LaTeX gelées | 30 |
| fichiers empreintés au total | 60 |

Les empreintes complètes sont dans `IMMUTABLE_STUDENT_ARTIFACTS.json`. Extrait, à titre de témoin :

| fichier | sha256 (16 premiers caractères) | octets |
| --- | --- | ---: |
| `S5_EVALUATION_1ERE_SPE_AHMAD_BELDI.pdf` | `f916946d34cf667e…` | 263391 |
| `S5_EVALUATION_1ERE_SPE_AHMAD_BELDI.tex` | `aac6809cbb113d0d…` | 6745 |
| `S5_TRAVAIL_1ERE_SPE_AHMAD_BELDI.pdf` | `bcdda1c5b13ea1fd…` | 349299 |
| `S5_TRAVAIL_1ERE_SPE_AHMAD_BELDI.tex` | `6bb5132cbbbe3852…` | 11602 |
| `S5_EVALUATION_1ERE_SPE_DONIA_KHADHRANI.pdf` | `136c4fa59edf07a8…` | 254079 |
| `S5_EVALUATION_1ERE_SPE_DONIA_KHADHRANI.tex` | `33e4b37340a4481d…` | 6589 |

## 2. Confirmation de non-modification

```
student_artifacts_changed = 0
```

| contrôle | verdict | détail |
| --- | --- | --- |
| empreintes des artefacts élèves | **PASS** | student_artifacts_changed = 0, manquants = 0, ajoutés = 0 |
| 15 couples élève x matière | **PASS** | 15 couples trouvés |
| 30 PDF élèves présents | **PASS** | 30 / 30 présents |
| 30 sources LaTeX présentes | **PASS** | 30 / 30 présentes |
| identifiants d'items inchangés | **PASS** | 180 items ; écarts : aucun |
| identifiants et points des critères d'origine inchangés | **PASS** | 337 critères ; écarts : aucun |
| 20 points bruts conservés par élève | **PASS** | écarts : aucun |
| aucun corrigé dans les documents élèves | **PASS** | fuites : aucune |

Verdict global de non-régression : **PASS**.

## 3. Nombre réel de critères

Le nombre canonique est recalculé, non postulé : **337 critères réels**, hors élève fictif du jeu de tests.

| | |
| --- | ---: |
| critères d'origine | 337 |
| dont mixtes, éclatés en sous-critères virtuels | 3 |
| sous-critères analytiques virtuels créés | 6 |
| lignes réellement notées | 340 |

## 4. Classement N−1 / passerelle vers N

| classement | critères |
| --- | ---: |
| `n_minus_1` | 311 |
| `bridge_n` | 23 |
| `mixed` | 3 |

24 exceptions au classement par défaut, chacune justifiée par écrit dans `curriculum_scope/SCOPE_RATIONALE.md`, en citant le livret distribué.

Six alias analytiques ont été créés pour ne plus fusionner sous un même identifiant une compétence N−1 et une notion N. Les `skill_id` d'origine sont conservés tels quels : `M3E_TRIG_01` reste `M3E_TRIG_01`, et se lit désormais soit `M3_TRIGO_COS_NM1`, soit `M3_TRIGO_SIN_BRIDGE`, selon le critère.

## 5. Points N−1 et points de passerelle, par élève

| élève | niveau | critères | points N−1 | points passerelle |
| --- | --- | ---: | ---: | ---: |
| ahmad-beldi-maths | 1ere_spe | 23 | 17.50 | 2.50 |
| ahmad-beldi-nsi | 1re_nsi | 21 | 14.75 | 5.25 |
| ahmed-bakir | 2nde | 22 | 20.00 | 0.00 |
| ahmed-benhadj-salem | 1re_nsi | 22 | 14.75 | 5.25 |
| amine-mansouri | 3e | 22 | 19.50 | 0.50 |
| donia-khadhrani | 1ere_spe | 23 | 19.50 | 0.50 |
| elyes-kefi | 3e | 23 | 18.50 | 1.50 |
| fares-darghouth | 4e | 23 | 20.00 | 0.00 |
| fares-laajili | 3e | 22 | 16.50 | 3.50 |
| ines-kefi | 4e | 22 | 19.00 | 1.00 |
| malek-khadhrani | 1ere_spe | 23 | 19.50 | 0.50 |
| noa-maniaci | 2nde | 23 | 20.00 | 0.00 |
| sarah-bargaoui | 3e | 23 | 19.50 | 0.50 |
| selim-mansouri | 3e | 22 | 18.50 | 1.50 |
| sinda-chikhaoui | 4e | 23 | 20.00 | 0.00 |

Les deux colonnes recomposent exactement 20 points pour chacun des quinze élèves ; c'est vérifié par un test paramétré.

## 6. Questions à interprétation limitée

9 critères portent `evidence_quality: limited_by_prompt`. La formulation imprimée n'y soutient pas une inférence forte, et le bilan doit respecter cette limite.

| critère | élève | item | ce que la formulation ne permet pas |
| --- | --- | --- | --- |
| `1ERE_SPE_AHMAD_BELDI_B2_c2` | ahmad-beldi-maths | B2 | cet item, seul, ne prouve pas une compétence de démonstration universelle |
| `1ERE_SPE_AHMAD_BELDI_B4_c1` | ahmad-beldi-maths | B4 | cet item, seul, ne prouve pas une compétence de démonstration universelle : il porte sur un intervalle donné et sur deux puissances voisines |
| `1ERE_SPE_AHMAD_BELDI_B4_c2` | ahmad-beldi-maths | B4 | correction prudente documentée dans l'overlay |
| `1ERE_SPE_DONIA_KHADHRANI_B2_c2` | donia-khadhrani | B2 | cet item, seul, ne prouve pas une compétence de démonstration universelle |
| `1ERE_SPE_MALEK_KHADHRANI_B2_c2` | malek-khadhrani | B2 | cet item, seul, ne prouve pas une compétence de démonstration universelle |
| `1ERE_SPE_MALEK_KHADHRANI_C2_c2` | malek-khadhrani | C2 | cette question ne permet pas de conclure que l'élève sait établir la monotonie d'une fonction sur un intervalle : elle mesure l'usage d'un contre-exemple |
| `3E_ELYES_KEFI_B4_c2` | elyes-kefi | B4 | la distinction entre contrôle de vraisemblance et contrôle détecteur est fine ; la non-réussite ne documente pas une absence de pratique du contrôle |
| `3E_ELYES_KEFI_B4_c3` | elyes-kefi | B4 | correction prudente documentée dans l'overlay |
| `4E_SINDA_CHIKHAOUI_C2_c2` | sinda-chikhaoui | C2 | cet item ne suffit pas à conclure sur la compétence générale de démonstration géométrique |

## 7. Corrections enseignantes appliquées

Quatre questions ont reçu un barème interne précisé, sans qu'une seule ligne du sujet change : Sinda CHIKHAOUI 4e C2, Elyes KEFI 3e B4, Ahmad BELDI 1re spé B4, Malek KHADHRANI 1re spé C2. Le détail figure dans `SCIENTIFIC_AUDIT_POST_DISTRIBUTION.md` et, élève par élève, dans `correction_overlays/<élève>/TEACHER_NOTES.md`.

Une observation de corrigé a été explicitement sortie du barème : le cas de la liste vide en B2 pour les deux élèves de NSI, que la question imprimée ne demande pas.

Sept imprécisions de support ont été relevées et traitées en clarifications orales. L'une d'elles — « une somme de deux carrés ne se factorise pas dans ℝ » — est un énoncé faux, pas une approximation.

## 8. Moteur d'analyse

`tools/analyze_s5_post_distribution.py` produit `raw_assessment_score`, `n_minus_1_consolidation`, `bridge_n_readiness`, `skills`, `error_profile`, `retention`, `delayed_checks` et `action_plan_inputs`, validés par `schemas/post_stage_analysis_v3.schema.json`.

L'analyseur V2 n'est pas écrasé : `S5_cloture/tools/analyze_s5.py` reste en place. Les deux ne doivent pas être lancés sur la même correction — le V2 attache les codes d'erreur à l'item, ce que le V3 refuse.

Le script refuse d'analyser plutôt que de deviner : score manquant, critère mixte non ventilé, code d'erreur sur un critère réussi, code inconnu, saisie ne correspondant pas au barème — chacun de ces cas arrête l'analyse avec un message explicite.

## 9. Tests

```
python3 -m pytest tests/
98 passed, 4 skipped in 1.76s
```

98 tests passés, 4 ignorés, 0 en échec.

Les tests ignorés le sont pour une raison précise : quatre élèves n'ont aucun critère de passerelle, et le test « un échec sur une passerelle ne crée jamais de déficit » n'a alors rien à éprouver.

Garanties couvertes : gel des empreintes, présence d'un `curriculum_scope` sur chaque critère, étanchéité des deux décomptes, non-propagation des codes d'erreur, `mastery_delta` nul, innocuité d'un échec de passerelle, traitement des quatre questions délicates, validation par le schéma V3, refus des saisies incomplètes, migration sans ventilation inventée, langage du bilan, et sûreté du packager.

## 10. Sécurité

| point | état |
| --- | --- |
| `S5_cloture/tools/make_release.py` | corrigé : plus de `shutil.rmtree` inconditionnel ; destination contrôlée, sentinelle exigée, construction en staging, bascule par renommage atomique, ancien paquet conservé en `.previous`, `--dry-run` |
| nouveau packager `tools/pack_post_distribution.py` | refuse `/`, `$HOME`, le dépôt, son parent, la source, et tout chemin sous `S5_cloture` ; refuse un répertoire existant sans sentinelle |
| écriture des outils V3 | refusée hors de `S5_post_distribution_v3/`, par construction |
| harnais NSI, mode conteneur | durci : aucun montage hôte inscriptible, résultat par `stdout` entre sentinelles, `chmod 0777` supprimé, swap borné, `fsize` et `nofile` limités, réseau coupé, FS en lecture seule, utilisateur non privilégié, capacités abandonnées, aucune image téléchargée implicitement |
| harnais NSI, mode relu | sans isolation, et signalé comme tel à chaque exécution ; ce n'est pas le mode par défaut |

**Action opérateur en attente.** `make_release.py` refuse désormais de remplacer les répertoires `S5_release/` et `S5_audit/` existants, qui ont été produits avant l'introduction de la sentinelle. C'est le comportement voulu. Pour reconstruire ces paquets, renommez ou déplacez d'abord les répertoires existants — le script ne le fera pas à votre place.

## 11. Limitations documentaires

| limitation | portée |
| --- | --- |
| aucune mesure initiale nominative item par item | aucune progression chiffrée n'est calculable ; `mastery_delta` vaut `null` pour les quinze couples |
| douze items par élève | la force de preuve est un décompte, pas une fiabilité psychométrique ; le terme `measurement_reliability` est proscrit |
| NOR du programme de Seconde 2025-2026 non documenté | le champ vaut `null` et l'absence est déclarée ; aucun numéro n'est fabriqué |
| NOR des acquis antérieurs en NSI non documentés | idem : la NSI n'a pas de programme d'année N−1, les prérequis viennent du cycle 4, de SNT et des séances S1 à S4 |
| durées réelles de passation non mesurées | `observed_duration_minutes` vaut `null` partout ; les estimations V2 sont conservées telles quelles |
| deux estimateurs de durée internes | ils partagent leurs entrées : ce ne sont pas deux mesures indépendantes, et plus rien ne le prétend |
| paquet d'audit | le mode `--source-mode manifest` rend un verdict « PASS WITH LIMITATION » : les sources originales ne sont pas réauditables depuis le seul bundle |

## 12. Statut de rétention

40 compétences, réparties sur 15 élèves, ont été retravaillées pendant la séance puis évaluées moins d'une heure plus tard. Elles portent `post_test_context: immediate_after_remediation` et `retention_status: not_yet_verified`.

Une réussite y signifie « réussite immédiate après remédiation ». Elle ne signifie pas « consolidation durable », et le contrôleur de langage refuse cette dernière formulation dans un bilan.

## 13. Mini-test différé

Semaine 2, dix minutes, deux items par compétence, parallèles à ceux de l'évaluation de clôture, sans aide ni carte de rappel. Critère : réussite maintenue sur au moins un item par compétence. Le détail par élève est dans `teacher_guidance/MINI_TEST_DIFFERE_S2.md`.

Après correction, l'analyseur produit le même objet sous `delayed_checks`, restreint aux compétences effectivement concernées par cet élève.

## 14. Références réglementaires

| niveau | programme de l'année N | applicable 2026-2027 | successeur | applicable |
| --- | --- | --- | --- | --- |
| 4e | MENE2018714A | oui | MENE2602912A | non |
| 3e | MENE2018714A | oui | MENE2602912A | non |
| 2nde | MENE2602914A | oui | — | — |
| 1ere_spe | MENE2602917A | oui | — | — |
| 1re_nsi | MENE1901633A | oui | — | — |

Le nouveau programme de cycle 4 (`MENE2602912A`) n'est **pas** appliqué par anticipation aux entrées en Quatrième et en Troisième de 2026-2027 : le changement est ultérieur.

## 15. Packaging

`tools/pack_post_distribution.py` construit la couche post-distribution en staging, empreinte chaque fichier livré dans `PACKAGE_MANIFEST.json`, puis bascule par renommage atomique. Il ne recopie aucun document élève : les PDF distribués restent dans `S5_cloture` et ne sont jamais dupliqués par ce paquet.

## 16. Traçabilité des sources

| mode | sources déclarées | vérifiées | verdict |
| --- | ---: | ---: | --- |
| `live` | 210 | 210 | **PASS** |
| `manifest` | 210 | 210 | **PASS WITH LIMITATION** |

En mode `manifest`, seules les empreintes et les références sont contrôlées : les sources originales ne sont pas réauditables depuis ce seul bundle. Ce n'est pas un détail de formulation — le paquet d'audit précédent se présentait comme autonome alors qu'il ne l'était pas.

## 17. Audit pédagogique élargi

| | |
| --- | ---: |
| modules de remédiation audités | 25 |
| exercices et corrigés | 150 |
| dont recalculés par le vérificateur | 20 |
| dont vérifiés par revue de lecture | 130 |
| échecs | 0 |

La distinction entre recalcul et revue est maintenue partout : un exercice « relu » n'est jamais compté comme « recalculé ».

## 18. Dettes restantes

| # | dette | pourquoi elle reste |
| --- | --- | --- |
| 1 | les sept imprécisions de support sont dans des documents figés | elles ne peuvent être corrigées que par la parole, ou signalées comme limites si la séance a eu lieu |
| 2 | `observed_duration_minutes` vaut `null` partout | aucune passation n'a encore été chronométrée ; le champ existe pour recevoir la mesure |
| 3 | 130 exercices de module vérifiés par lecture | leur nature ne se prête pas au recalcul ; l'automatiser demanderait un vérificateur symbolique |
| 4 | `S5_release/` et `S5_audit/` sans sentinelle | à renommer ou déplacer par l'opérateur avant toute reconstruction |
| 5 | aucune correction réelle saisie | les quinze gabarits V3 sont vierges ; l'analyseur n'a été éprouvé que sur des jeux synthétiques |
| 6 | le durcissement du conteneur n'a été éprouvé que sur `python:3-slim` | le mode conteneur a bien été exécuté et rend un résultat identique au mode relu, mais avec une seule image et un seul moteur ; le comportement sous podman n'a pas été vérifié |
| 7 | pas d'étude de fiabilité | douze items ne permettent pas d'en conduire une ; aucune n'est revendiquée |

Ce rapport ne vise ni zéro avertissement ni 100 % de PASS. Un contrôle non exécuté est écrit comme non exécuté.
