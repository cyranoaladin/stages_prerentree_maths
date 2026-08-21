# Audit d'intégration initial — Nexus S5 Correction & Bilans

Réalisé le 21 août 2026, **avant** l'écriture de la moindre ligne applicative. Aucun
artefact existant n'a été modifié pendant cet audit : il n'a produit que ce document.

## 1. État Git au moment de l'audit

```
 M S5_cloture/_teacher_private/tests_s5_nsi.py
 M S5_cloture/tools/make_release.py
?? S5_post_distribution_v3/
```

Branche : `main`.

Deux fichiers modifiés et un répertoire non suivi préexistent — ils proviennent de la
mission post-distribution V3. **Ils sont laissés intacts.** Aucun `reset`, `clean`,
`checkout --`, `stash` ni commit n'a été exécuté, et aucun ne le sera sans demande
explicite.

## 2. Vérification d'immutabilité, avant tout travail

```
artefacts élèves attendus : 60
student_artifacts_changed = 0
student_artifacts_missing = 0
student_artifacts_added   = 0
verdict : PASS
```

Les huit contrôles de non-régression de la couche V3 passent également, dont « aucun
corrigé dans les documents élèves ». Le corpus distribué est donc dans l'état
contractuel attendu, et l'application se construira autour de lui.

## 3. Où se trouve réellement la couche V3

Racine : `S5_post_distribution_v3/`. L'organisation constatée, et non supposée :

| chemin | rôle pour l'application |
| --- | --- |
| `IMMUTABLE_STUDENT_ARTIFACTS.json` | 60 empreintes SHA-256 — source du contrôle au démarrage |
| `curriculum_scope/criteria_scope.json` | les 337 critères, classés et justifiés — **source primaire du référentiel** |
| `curriculum_scope/analysis_skills.json` | 6 alias analytiques (cosinus/sinus, produit de relatifs, suites, double distributivité, algorithmes de recherche) |
| `curriculum_scope/curriculum_references.json` | textes réglementaires par niveau, NOR non documentés déclarés `null` |
| `correction_overlays/<élève>/ANSWER_KEY_OVERLAY.json` | 15 fichiers — barème équitable, méthodes acceptées, limites, rétention, réponse attendue d'origine |
| `correction_overlays/<élève>/CORRECTION_POLICY.json` | 15 fichiers — répartition N−1/passerelle, observations non scorées, durée estimée |
| `correction_overlays/<élève>/TEACHER_NOTES.md` | notes de correction lisibles |
| `responses/responses_v3_TEMPLATE_<élève>.json` | 15 gabarits de saisie, tous vierges |
| `schemas/responses_v3.schema.json` | schéma de saisie |
| `schemas/post_stage_analysis_v3.schema.json` | schéma de sortie d'analyse |
| `tools/analyze_s5_post_distribution.py` | analyseur déterministe V3 — **référence de comportement** |
| `tools/pd_core.py`, `scope_rules.py`, `equity_rules.py` | socle, classement, règles d'équité |
| `teacher_guidance/mini_test_differe_s2.json` | mini-tests différés, 40 compétences sur 15 élèves |
| `tests/test_post_distribution_v3.py` | 98 tests, 4 ignorés |
| `CANONICAL_POST_DISTRIBUTION.json` | nombres canoniques |

Sources secondaires, lues en lecture seule dans `S5_cloture/` :

| chemin | rôle |
| --- | --- |
| `<niveau>/<matière>/<Élève>/S5_EVALUATION_*.pdf` | PDF affiché dans l'écran de correction |
| `<niveau>/<matière>/<Élève>/S5_TRAVAIL_*.pdf` | livret, consultable |
| `<niveau>/<matière>/<Élève>/_ENSEIGNANT/evaluation_manifest.json` | énoncés, étapes, erreurs probables, sondes de certitude, comparabilité |
| `<niveau>/<matière>/<Élève>/student_learning_profile.json` | diagnostic initial qualitatif par domaine |
| `tools/data/levels.py` | libellés de compétences, importance, domaines |

## 4. Les 15 couples élève × matière

| élève | niveau | critères | points N−1 | points passerelle | critères mixtes |
| --- | --- | ---: | ---: | ---: | ---: |
| ahmad-beldi-maths | 1ere_spe | 23 | 17,50 | 2,50 | 1 |
| ahmad-beldi-nsi | 1re_nsi | 21 | 14,75 | 5,25 | 0 |
| ahmed-bakir | 2nde | 22 | 20,00 | 0,00 | 0 |
| ahmed-benhadj-salem | 1re_nsi | 22 | 14,75 | 5,25 | 0 |
| amine-mansouri | 3e | 22 | 19,50 | 0,50 | 0 |
| donia-khadhrani | 1ere_spe | 23 | 19,50 | 0,50 | 1 |
| elyes-kefi | 3e | 23 | 18,50 | 1,50 | 0 |
| fares-darghouth | 4e | 23 | 20,00 | 0,00 | 0 |
| fares-laajili | 3e | 22 | 16,50 | 3,50 | 0 |
| ines-kefi | 4e | 22 | 19,00 | 1,00 | 0 |
| malek-khadhrani | 1ere_spe | 23 | 19,50 | 0,50 | 1 |
| noa-maniaci | 2nde | 23 | 20,00 | 0,00 | 0 |
| sarah-bargaoui | 3e | 23 | 19,50 | 0,50 | 0 |
| selim-mansouri | 3e | 22 | 18,50 | 1,50 | 0 |
| sinda-chikhaoui | 4e | 23 | 20,00 | 0,00 | 0 |

**14 personnes, 15 couples.** Ahmad BELDI est inscrit en mathématiques *et* en NSI. Le
modèle de données sépare donc `Person`, `Student` (couple personne × niveau × matière)
et `Assessment` ; le nom n'est jamais une clé.

## 5. Nombre réel de critères

Recompté depuis `criteria_scope.json`, non recopié :

| | |
| --- | ---: |
| items | 180 |
| critères d'origine | 337 |
| dont `n_minus_1` | 311 |
| dont `bridge_n` | 23 |
| dont `mixed` | 3 |
| sous-critères analytiques virtuels | 6 |
| **lignes réellement notées** | **340** |
| critères à interprétation limitée | 9 |
| items portant une sonde de certitude | 30 |

## 6. Constat déterminant sur les points : les quarts ne suffisent pas

Le barème distribué emploie les valeurs suivantes :

```
0,25 (×1)   0,3 (×8)   0,4 (×5)   0,5 (×45)   0,6 (×6)
0,7 (×10)   0,75 (×25) 1 (×223)   1,25 (×2)   1,5 (×12)
```

`0,3`, `0,4`, `0,6` et `0,7` **ne sont pas des multiples de 0,25**. La consigne
« entier représentant les quarts de point » est donc inapplicable telle quelle sur ce
corpus. Tous les montants sont en revanche des multiples de **0,05**.

Décision : les scores sont stockés en **centièmes de point, sous forme d'entiers**
(`Integer`), et manipulés en `Decimal` dans le domaine. Aucun flottant binaire
n'intervient dans un calcul de score. C'est exact, ordonnable en SQL, et cela couvre la
totalité du barème réel.

## 7. Ce que l'application devra recalculer, et ce qu'elle importera

Importé tel quel, jamais ressaisi : élèves, niveaux, matières, items, critères, points,
`curriculum_scope`, alias analytiques, méthodes acceptées, limites d'interprétation,
règles d'équité, réponses attendues, sondes de certitude, contexte de rétention,
observations non scorées, profils initiaux qualitatifs, mini-tests différés.

Recalculé par l'application, de façon déterministe : score brut, consolidation N−1,
disponibilité sur les passerelles, agrégation par compétence d'analyse, force de preuve,
profil d'erreurs, statuts pédagogiques, priorités, plan de quatre semaines.

Le comportement de référence est celui de `tools/analyze_s5_post_distribution.py`. Un
test de non-régression compare les deux moteurs sur des saisies synthétiques : score
brut, N−1, passerelle et profil d'erreurs doivent coïncider.

## 8. Contraintes retenues de l'environnement

| composant | état constaté |
| --- | --- |
| FastAPI 0.135.2, Starlette, Uvicorn 0.42.0 | disponibles |
| Jinja2 3.1.6, SQLAlchemy 2.0.42, Pydantic 2.11.7 | disponibles |
| httpx 0.28.1, python-multipart, itsdangerous | disponibles — TestClient et formulaires utilisables |
| pdflatex, lualatex, xelatex, latexmk | disponibles |
| Playwright | **absent** — les tests de bout en bout navigateur ne seront pas une dépendance de livraison |

Aucun CDN ne sera utilisé : CSS et JavaScript seront servis depuis `app/static/`.

## 9. Ce qui sera modifié hors du répertoire de l'application

Trois fichiers, et rien d'autre — chacun justifié dans le rapport d'implémentation :

| fichier | modification | raison |
| --- | --- | --- |
| `.gitignore` | ajout de règles | empêcher le versionnement des corrections réelles, de la base SQLite et des bilans générés |
| `Makefile` | ajout de cibles `s5-correction-*` | lancement sans terminal complexe ; aucune cible existante n'est touchée |
| `S5_correction_app/requirements-correction.lock` | création | traçabilité des versions réellement utilisées |

Les PDF élèves, leurs sources LaTeX, la photographie V2/V3 distribuée et
`S5_cloture/**` ne seront pas modifiés.

## 10. Risques identifiés avant de commencer

| # | risque | traitement prévu |
| --- | --- | --- |
| 1 | homonymie Ahmad BELDI | identifiants stables `student_id` / `assessment_id`, jamais le nom |
| 2 | points non multiples de 0,25 | stockage en centièmes entiers |
| 3 | dérive silencieuse entre la source V3 et la base | empreinte de chaque source à l'import ; alerte explicite, jamais de resynchronisation automatique |
| 4 | fuite de données réelles vers Git | `runtime/` ignoré, plus un test qui échoue si un fichier sensible est suivi |
| 5 | rapport généré depuis une correction non validée | interdit par la machine d'état |
| 6 | écrasement d'un texte modifié par un humain | provenance et approbation par bloc ; une régénération ne remplace jamais un bloc approuvé |
| 7 | traversée de chemin sur les routes PDF | résolution `realpath` et confinement aux racines autorisées |
| 8 | compilation LaTeX injectée | `subprocess` sans `shell=True`, arguments listés, identifiants assainis |

## 11. Conclusion de l'audit

La couche V3 est complète, cohérente et directement exploitable comme référentiel. Les
60 artefacts distribués sont intacts. Deux points appelaient une décision technique avant
de coder — l'homonymie et la granularité des points — et les deux sont tranchés ci-dessus.

Le développement peut commencer.
