# Audit avant pilote — Inès KEFI

Réalisé le 21 août 2026, **avant** toute modification, conformément au périmètre de la
passe corrective. Ce document décrit le comportement **constaté**, pas le comportement
souhaité.

## 0. Baseline Git au démarrage

```
branche       main
HEAD          b3a1a14f6cefebd1cccfa94327738d63176fc388
origin/main   b3a1a14f6cefebd1cccfa94327738d63176fc388
working tree  propre
```

PR #3 (`2463e16`) et PR #4 (`177fe31`) sont bien ancêtres de `main`. `S5_correction_app/`
et `S5_post_distribution_v3/` sont présents.

Immutabilité relevée avant correction : **60 artefacts, changed = 0, missing = 0, PASS.**
Les 60 empreintes ont été archivées pour comparaison finale.

## 1. Anomalie relevée dans la base pilote

`§36` demande de vérifier `corrections_real_count == 0` avant toute synchronisation. Le
compte n'est pas nul :

```
corrections     : 1
scores saisis   : 0
rapports        : 0
analyses        : 0
```

Inspection de la ligne : `correction_id = 1`, `asm-ines-kefi`, révision 1, statut `DRAFT`,
créée le **21/08 à 19:08**, 22 lignes toutes `PENDING`, 0 score, 0 code d'erreur,
0 observation, 0 certitude, aucune observation générale, aucune durée. Journal d'audit :
un seul évènement, `correction.created`.

Origine : le test de fumée du serveur mené à la fin de la mission précédente
(`GET /eleve/ines-kefi`). L'application crée une coquille de correction vide à l'ouverture
d'un élève. **Ce n'est pas une saisie enseignant.** La coquille sera supprimée après
sauvegarde, pour que le pilote démarre d'un état réellement vierge.

## 2. Où vivent les 22 critères d'Inès

| ce qu'on cherche | où c'est réellement |
| --- | --- |
| définition des critères | `S5_post_distribution_v3/curriculum_scope/criteria_scope.json`, produit par `tools/scope_rules.py` |
| overlay par élève | `S5_post_distribution_v3/correction_overlays/ines-kefi/ANSWER_KEY_OVERLAY.json` |
| énoncés, étapes, erreurs probables | `S5_cloture/4e/Mathematiques/Ines_KEFI/_ENSEIGNANT/evaluation_manifest.json` |
| diagnostic initial | `S5_cloture/4e/Mathematiques/Ines_KEFI/student_learning_profile.json` |
| import en base | `S5_correction_app/app/domain/importer.py` |
| tables | `criterion_definition`, `virtual_criterion_definition`, `item_definition` |
| valeurs de score proposées | `app/domain/points.py::allowed_scores` |
| affichage de la grille | `app/routes/correction.py::_grid` + `app/templates/correction.html` |
| corrigé | bloc `<details class="key">` de `correction.html` |
| raccourcis clavier | `app/static/app.js::bindKeyboard` |
| viewer PDF | `.pane-pdf` / `.pdf-frame` dans `app/static/app.css` |
| bandeau de validation | `correction.html` ligne 41 et `partials/validation_problems.html` |
| observations générales | `app/domain/correction.py::GENERAL_OBSERVATION_FIELDS` |

## 3. État constaté du référentiel d'Inès

22 critères, 20 points. Répartition actuelle : **19 points `n_minus_1`, 1 point
`bridge_n`, 0 critère mixte.**

Seul `C2_c2` — `(-4) × (-7)` et justification du signe — est classé `bridge_n`.

### 3.1 Le classement repose sur une justification faible

Chaque critère `n_minus_1` porte le même texte, généré automatiquement :

> « aucune notion du programme de l'année N n'est requise pour traiter la question
> imprimée : le critère mesure un acquis de l'année N-1. »

C'est une affirmation, pas une justification. Aucun critère ne cite d'attendu officiel, et
le classement dérive en pratique du raisonnement « ce qui n'est pas déclaré nouveau en
phase 4 du livret est un acquis N−1 ». Le livret documente une intention pédagogique ; il
n'a pas autorité curriculaire.

## 4. Défauts d'interface constatés

### 4.1 Les erreurs probables sont celles de l'ITEM, pas du critère

`app/routes/correction.py::_grid` lit `item.likely_errors_json` et l'affiche sous chaque
critère de l'item. Conséquences observées :

| item | critères | erreurs affichées sous **chacun** |
| --- | --- | --- |
| B1 | `B1_c1` aire/périmètre, `B1_c2` prix | `CONCEPT`, `NOTATION`, `METHODE` — identiques |
| B2 | `B2_c1` développement, `B2_c2` réduction, `B2_c3` contrôle | `CONCEPT`, `CONCEPT`, `CONTROLE` — identiques, et `CONCEPT` en doublon |
| C1 | quatre critères | `TRANSFERT`, `CONCEPT`, `LECTURE`, `NOTATION` — identiques |

Le correcteur voit donc, sous le critère « aire et périmètre », une erreur qui appartient
au critère « prix ». Et `CONCEPT` apparaît deux fois de suite sous les trois critères de B2.

### 4.2 Les scores partiels n'ont aucune règle d'attribution

`points.allowed_scores` produit une échelle purement arithmétique :

```
critère à 1 pt    → 0 / 0,25 / 0,5 / 0,75 / 1
critère à 0,5 pt  → 0 / 0,25 / 0,5
critère à 0,7 pt  → 0 / 0,35 / 0,7
critère à 0,3 pt  → 0 / 0,15 / 0,3
critère à 1,5 pt  → 0 / 0,25 / 0,5 / 0,75 / 1 / 1,25 / 1,5
```

Rien n'indique ce que vaut 0,75 plutôt que 0,5. Deux correcteurs — ou le même à deux
moments — n'attribueraient pas la même chose. `0,35` et `0,15` sont en outre des valeurs
que rien ne justifie pédagogiquement.

### 4.3 Le LaTeX s'affiche brut

L'interface rend littéralement le contenu du référentiel :

```
Calculer $\dfrac{5}{8} - \dfrac{1}{4}$.
$4x-5$ exact
$53^\circ$ exact
$\frac{3}{8}$ ou une écriture équivalente correcte
```

Aucun moteur de rendu mathématique n'est chargé.

### 4.4 Le corrigé est visible avant d'être demandé

`correction.html` ligne 101 affiche `row.description` comme titre du critère. Or ces
descriptions **sont** le corrigé :

```
A1_c1  « résultat $0$ exact »
A2_c1  « $\frac{3}{8}$ ou une écriture équivalente correcte »
A4_c1  « $53^\circ$ exact »
A3_c1  « $4x-5$ exact »
```

Le bouton « Afficher le corrigé et le barème » n'a plus grand-chose à révéler.

### 4.5 Le PDF défile hors de l'écran

`.pane-pdf` n'a aucune règle `position: sticky`. `.pdf-frame` fait
`height: calc(100vh - 210px)`. Sur une page de 22 critères, dès qu'on descend dans la
grille, le sujet disparaît. Seule `.sticky-bar` est collante.

### 4.6 Le bandeau parle de « points »

`correction.html` ligne 41 :

```
{{ problems|length }} point(s) à traiter avant de pouvoir valider.
```

Sur une page où « point » désigne aussi une unité de barème, c'est une ambiguïté fâcheuse :
au départ, l'interface annonce « 22 point(s) à traiter » sur une évaluation qui vaut
20 points. Les 22 entrées sont en outre listées d'emblée, sans repli.

### 4.7 Les raccourcis clavier ne sont pas suffisamment neutralisés

`app.js::bindKeyboard` teste :

```js
if (tag === "textarea" || tag === "input" || event.ctrlKey || ...) { return; }
```

`select`, `button` et les éléments `contenteditable` ne sont pas couverts. Taper dans un
`select` ou avec le focus sur un bouton de score peut déclencher un raccourci.

### 4.8 Les observations générales sont sept zones de texte libre

`GENERAL_OBSERVATION_FIELDS` définit sept `textarea` : autonomie, méthode, rythme,
rédaction, contrôle, attitude face à l'erreur, remarque libre. Aucune saisie structurée,
donc une saisie lente et des formulations non comparables d'un élève à l'autre.

## 5. Ce que l'audit ne remet pas en cause

- le moteur d'analyse V3 : erreurs par critère, séparation N−1 / passerelle, absence de
  faux delta, force de preuve ;
- les overlays des quatre cas post-distribution (Sinda, Elyes, Ahmad, Malek) ;
- l'immutabilité des 60 artefacts ;
- le total de 20 points et les identifiants des 22 critères.

## 6. Ce que la passe corrective doit produire

1. un classement curriculaire **sourcé** des 22 critères, adossé aux attendus officiels et
   au diagnostic d'entrée, et non au livret ;
2. une rubrique de score explicite par critère, et des valeurs proposées limitées à celles
   que la rubrique décrit ;
3. des suggestions d'erreur **propres au critère** ;
4. un rendu mathématique local ;
5. un corrigé réellement masqué avant ouverture ;
6. un viewer PDF collant sur desktop ;
7. un bandeau parlant de « critères », replié tant qu'aucune validation n'a été tentée ;
8. des raccourcis inertes dans tout champ de saisie ;
9. des observations générales structurées ;
10. les tests de non-régression correspondants.
