# Rapport d'implémentation — Nexus S5 Correction & Bilans

Version 1.0.0, 21 août 2026.

## 1. Ce qui a été livré

Une application web locale qui permet de corriger les quinze évaluations S5 distribuées,
critère par critère, puis de produire quatre documents de fin de stage. Elle démarre par
`make s5-correction-run` et s'utilise ensuite entièrement dans le navigateur.

En usage courant, l'enseignant ne touche plus au terminal, n'édite aucun JSON, ne lance
aucun script.

## 2. Architecture

Détaillée dans `ARCHITECTURE.md`. En bref : FastAPI + Jinja2 rendu côté serveur, SQLAlchemy
2 sur SQLite, JavaScript minimal sans dépendance, LaTeX pour les PDF. Aucun framework SPA,
aucun CDN, aucun appel réseau.

Le domaine métier est isolé dans `app/domain/` : il calcule et ne rend rien. Les routes
rendent et ne calculent rien.

## 3. Fichiers créés

| ensemble | fichiers | lignes |
| --- | ---: | ---: |
| code applicatif (`app/`, `tools/`, `migrations/`) | 33 fichiers Python | 4 461 |
| gabarits HTML | 10 | 783 |
| style et gabarits LaTeX | 5 | 383 |
| tests | 12 fichiers | 1 249 |
| documentation | 12 documents | — |

Structure complète dans `ARCHITECTURE.md`.

## 4. Modifications hors du répertoire de l'application

Trois, et trois seulement. Chacune était annoncée dans l'audit initial.

| fichier | modification | raison |
| --- | --- | --- |
| `.gitignore` | ajout d'un bloc de neuf règles | empêcher le versionnement de la base, des corrections, des bilans et des exports. Le dépôt peut être public ; ces fichiers sont des données personnelles d'élèves. |
| `Makefile` | ajout de six cibles `s5-correction-*` | permettre le lancement sans commande complexe. **Aucune cible existante n'a été touchée** : les 17 cibles préexistantes sont inchangées. |
| `S5_correction_app/requirements-correction.lock` | création | tracer les versions réellement utilisées |

Les modifications de `S5_cloture/tools/make_release.py` et
`S5_cloture/_teacher_private/tests_s5_nsi.py` visibles dans `git status` **préexistaient à
cette mission** : elles proviennent de la couche post-distribution V3. Elles n'ont pas été
touchées.

Aucun PDF élève, aucun `.tex` élève, aucun fichier de `S5_post_distribution_v3/` n'a été
modifié.

## 5. Base de données et migrations

SQLite, en WAL, avec `foreign_keys=ON` et `synchronous=FULL`. Le schéma est créé par
`migrations.apply`, qui inscrit `domain_schema_version`, `app_version` et
`import_source_version` dans `app_meta`. Une migration future s'ajoute à la liste
`UPGRADES` ; elle est précédée d'une sauvegarde automatique de la base.

Aucune migration ne se déclenche à l'import d'un module.

## 6. Import du référentiel

`app/domain/importer.py` lit la couche V3 et les manifestes enseignants, sans rien
ressaisir. Résultat constaté :

```
persons            14
students           15
assessments        15
items             180
criteria          337
virtual_criteria    6
skills             72
baselines         195
delayed_checks     40
sources            64
```

Chaque fichier lu est empreinté dans `import_source`. Si une source change après l'import,
l'écran de maintenance l'affiche. **Rien n'est resynchronisé automatiquement** : c'est une
décision, pas un automatisme.

## 7. Décisions techniques qui méritent d'être justifiées

### Les points sont des entiers en centièmes, pas des quarts

Le cahier des charges proposait « `Decimal` ou entier représentant les quarts de point ».
Le barème réel contient 0,3 / 0,4 / 0,6 / 0,7, qui **ne sont pas des quarts** : 29 critères
sur 337 seraient irreprésentables. Tous les montants sont en revanche des multiples de
0,05. Les scores sont donc stockés en centièmes entiers et manipulés en `Decimal` dans le
domaine. Aucun flottant binaire n'entre dans un calcul.

### Trois niveaux de personne

Le cahier des charges demandait de ne pas utiliser le nom comme identifiant, en citant
Ahmad BELDI. Le modèle sépare `person`, `student` et `assessment` : 14 personnes pour 15
couples. Les noms de fichiers produits ajoutent la matière quand une personne en suit
plusieurs.

### L'échelle de scores proposée dépend du barème du critère

Quarts quand le maximum est un multiple de 0,25 — c'est le cas de 292 critères sur 337 —
moitiés sinon, pour éviter une échelle inutilisable sur un critère à 0,3 point. Le serveur
reste un peu plus tolérant que les boutons : il accepte tout multiple de 0,05 dans
l'intervalle, pour ne pas forcer un correcteur à contourner l'outil.

### Le statut `UNCLASSIFIED` existe

Un zéro n'oblige à aucune cause. Fabriquer un code d'erreur fausserait le profil d'erreurs,
donc le plan de rentrée. `NOT_ANSWERED` et `UNCLASSIFIED` permettent de dire ce qu'on a vu,
et rien de plus.

## 8. Sécurité

| point | traitement |
| --- | --- |
| écoute réseau | `127.0.0.1` par défaut ; `--allow-network` exige `NEXUS_S5_PASSWORD` d'au moins 12 caractères, sans valeur par défaut |
| chemins de documents | reconstruits côté serveur, résolus par `realpath`, confinés aux racines autorisées |
| SQL | ORM et paramètres liés uniquement |
| XSS | échappement Jinja2 par défaut ; testé sur une observation contenant `<script>` |
| injection LaTeX | `latex_escape` sur tout texte humain ; testé sur `100 % & <b>sûr</b>` |
| sous-processus | `shell=False` imposé ; vérifié sur l'arbre syntaxique de tout `app/**.py` |
| noms de fichiers | `safe_slug` : ASCII, majuscules, tirets bas |
| secrets | aucun littéral ; vérifié par analyse syntaxique |
| CSRF | jetons HMAC disponibles ; non exigés en localhost strict sans compte — choix documenté |

## 9. Immutabilité

```
immutable_artifacts_total     60
immutable_artifacts_verified  60
immutable_artifacts_changed    0
immutable_artifacts_missing    0
verdict                     PASS
```

Contrôlée au démarrage, avant chaque validation, avant toute production de paquet élève, et
par `tools/verify_integrity.py`. En cas d'échec, l'application bascule en lecture seule et
l'affiche sur toutes les pages : elle ne continue jamais en silence.

Un test relève les 60 empreintes avant la suite, en fait autant après, et compare une à
une.

## 10. Portées curriculaires

| portée | critères |
| --- | ---: |
| `n_minus_1` | 311 |
| `bridge_n` | 23 |
| `mixed` | 3, éclatés en 6 sous-critères |

Les deux décomptes recomposent exactement 20 points pour chacun des 15 élèves, sans double
comptage — c'est vérifié pour les quinze.

## 11. Tests

92 passés, 1 ignoré, 0 échec. Le détail et ce qui n'est pas couvert figurent dans
`TEST_REPORT.md`.

Un module compare l'application à l'analyseur V3 de référence sur la même saisie : score
brut, consolidation N−1, disponibilité sur les passerelles et profil d'erreurs coïncident.

## 12. Dépendances

`requirements-correction.lock`. Tout est déjà présent sur le poste. Playwright ne l'est
pas, et la livraison n'en dépend pas.

## 13. Commandes

```bash
make s5-correction-install     # dépendances
make s5-correction-init        # base + import + contrôle des empreintes
make s5-correction-run         # http://127.0.0.1:8765
make s5-correction-test        # suite de tests
make s5-correction-qa          # intégrité + tests
make s5-correction-backup      # sauvegarde
```

## 14. Statut

```
READY_FOR_PILOT
```

Le système n'est pas déclaré validé en production. Il le sera après la correction complète
d'une première copie réelle et la revue humaine du bilan produit : la procédure est dans
`PILOT_REAL_COPY_VALIDATION.md`.

**Aucune correction réelle n'a été saisie.** Les quinze grilles sont vierges.
