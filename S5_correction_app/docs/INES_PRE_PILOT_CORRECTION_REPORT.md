# Rapport de la passe corrective — pilote Inès KEFI

21 août 2026. Statut de l'application à l'issue : **`READY_FOR_PILOT`** — inchangé, et
c'est voulu : aucune vraie copie n'a été corrigée.

## 1. Fichiers modifiés

| fichier | nature |
| --- | --- |
| `app/data/criterion_overlays.py` | **créé** — les 22 critères d'Inès : classement sourcé, rubrique de score, suggestions d'erreur, libellé neutre |
| `app/data/__init__.py` | créé |
| `app/models.py` | 5 colonnes sur `criterion_definition`, 3 sur `virtual_criterion_definition` |
| `migrations/__init__.py` | migration de schéma v1 → v2, rejouable |
| `app/__init__.py` | schéma 2, version 1.1.0 |
| `app/domain/importer.py` | application des overlays, éclatement des mixtes, recalcul des totaux de portée |
| `app/domain/correction.py` | observations générales structurées |
| `app/domain/reports.py` | lecture du nouveau format d'observations |
| `app/routes/correction.py` | rubriques, suggestions, libellés neutres, ouverture du détail après tentative |
| `app/schemas.py` | champs `*_choix` / `*_commentaire` |
| `app/templates/correction.html` | bloc critère réécrit, bandeau, observations, corrigé |
| `app/templates/partials/validation_problems.html` | vocabulaire |
| `app/templates/base.html` | chargement de KaTeX local |
| `app/static/app.css` | viewer collant, rubriques, suggestions, repli math |
| `app/static/app.js` | garde-fou clavier |
| `app/static/math.js` | **créé** — rendu mathématique cantonné aux conteneurs `.math` |
| `app/static/vendor/katex/**` | **créé** — 25 fichiers, 608 Ko, copie locale, aucun CDN |
| `tests/test_ines_pilot.py` | **créé** — 28 tests |
| `tests/test_import_and_model.py` | 2 compteurs mis à jour, garantie renforcée |
| `docs/INES_PRE_PILOT_AUDIT.md`, `INES_CURRICULUM_MATRIX.md`, `INES_UI_MANUAL_CHECKLIST.md`, `FUTURE_CURRICULUM_REVIEW.md`, ce rapport | créés |
| `docs/TECHNICAL_DEBT.md` | deux dettes ajoutées |

## 2. Aucun document élève modifié

```
immutable_artifacts_total     60
immutable_artifacts_changed    0
immutable_artifacts_missing    0
verdict                     PASS
```

Les 60 empreintes ont été relevées avant la première modification et comparées une à une
à la fin : **0 différence**. Aucun `S5_TRAVAIL_*`, `S5_EVALUATION_*`, `.pdf` ou `.tex`
n'a été ouvert en écriture.

## 3. Les 22 critères

Matrice complète, avec justification et source pour chacun :
`docs/INES_CURRICULUM_MATRIX.md`.

Le classement ne repose plus sur « ce qui n'est pas déclaré nouveau en phase 4 du livret
est un acquis ». Il repose sur les attendus de fin d'année publiés par éduscol, lus
intégralement, plus l'instrument de diagnostic qui a établi la ligne de base d'Inès.

### La frontière qui a tout décidé

| tâche | attendus **5e** | attendus **4e** |
| --- | --- | --- |
| réduire `ax + bx` | ✅ explicite, exemples `5,2x + 3,4x`, `2,4x − 2,1x` | repris |
| **développer `k(a − b)`** | ❌ absent | ✅ explicite, exemple `3(4x − 2)` |
| substituer pour **contrôler** | ✅ explicite | — |
| produire une expression littérale | ✅ explicite | — |
| fractions, dénominateurs multiples | ✅ explicite | cas général |
| **produit** de relatifs | ❌ absent | ✅ explicite |

## 4. Scopes avant / après

| critère | avant | après | raison |
| --- | --- | --- | --- |
| `B2_c1` développer `5(x−3)` | `n_minus_1` | **`bridge_n`** | absent des attendus de 5e ; explicite en 4e |
| `B2_c2` réduire en `7x−8` | `n_minus_1` | **`bridge_n`** | conditionné par un développement de 4e |
| `A3_c1` réduire `7x+4−3x−9` | `n_minus_1` | **`mixed`** | 5e borne la réduction à `ax+bx` ; 4e l'énonce sans restriction |
| les 19 autres | inchangés | inchangés | vérifiés un par un contre les attendus |

**Vérifiés et confirmés sans changement**, contrairement à ce que les alertes laissaient
craindre : `A2_c1` (8 est multiple de 4 — l'attendu de 5e couvre exactement ce cas),
`B2_c3` (« substituer […] pour contrôler son résultat » est mot pour mot un attendu de
5e), `C1_c3` et `C1_c4` (« produire une expression littérale », « substituer »),
`C2_c2` (produit de relatifs, déjà en passerelle), `C2_c1` (resté séparé).

## 5. Nouveau décompte

```
Ines KEFI
raw max            = 20
N−1 max            = 17,5   (avant : 19)
Bridge max         = 2,5    (avant : 1)
Mixed              = 1 critère (A3_c1, 1 pt) éclaté en 2 sous-critères de 0,5
criteria original  = 22
lignes notées      = 23     (21 critères simples + 2 sous-critères)
```

Les points de passerelle passent de 1 à 2,5. C'est le changement le plus lourd de
conséquence : 1,5 point qui pesait sur le diagnostic des acquis de Cinquième n'y pèse
plus. Le score brut, lui, reste à 20 — le sujet n'a pas bougé.

## 6. Critères mixtes

Un seul : `A3_c1`, éclaté en `A3_c1_v1` (0,5 pt, `n_minus_1`, regroupement des termes en
x) et `A3_c1_v2` (0,5 pt, `bridge_n`, écriture réduite avec constantes signées). La somme
est strictement égale au point du critère imprimé, et un test le vérifie. Le critère
parent n'est plus noté directement : ce sont ses sous-critères qui le sont, donc aucune
duplication n'est possible.

Sa certitude est notée **moyenne**, et l'interface l'affiche. Les attendus de 5e bornent
la réduction à `ax + bx`, ceux de 4e ne la bornent pas, et le diagnostic d'entrée d'Inès
comportait pourtant un item de ce type. Plutôt que de trancher, on déclare l'ambiguïté.

## 7. Règles de score

Chaque valeur proposée par l'interface est désormais adossée à une règle observable.
L'échelle n'est plus arithmétique : elle est celle que la rubrique décrit.

| critère | avant | après |
| --- | --- | --- |
| `A1_c1` | 0 / 0,25 / 0,5 / 0,75 / 1 | 0 / 0,5 / 1 |
| `B1_c1` | 0 / 0,25 / 0,5 / 0,75 / 1 | 0 / 0,25 / 0,5 / 0,75 / 1, chacune décrite |
| `B3_c3` | 0 / 0,15 / 0,3 | 0 / 0,3 — l'encadrement est écrit, ou il ne l'est pas |
| `B2_c1` | 0 / 0,25 / 0,5 | 0 / 0,25 / 0,5, le 0,25 décrivant l'erreur de signe |

Exemple, `B1_c1` :

| score | attribution |
| ---: | --- |
| 1 | aire et périmètre exacts, avec les unités correctes |
| 0,75 | les deux calculs exacts, une unité manquante ou erronée |
| 0,5 | un des deux calculs exact, avec son unité |
| 0,25 | formule pertinente engagée, aucun résultat abouti |
| 0 | aucun élément mathématiquement exploitable |

La rubrique est affichée sous les boutons, dépliée par défaut, et la ligne correspondant
au score choisi se surligne.

## 8. Erreurs spécifiques au critère

Avant, l'interface répétait les erreurs de l'item sous chacun de ses critères. `B1_c1` et
`B1_c2` affichaient les mêmes trois codes ; les trois critères de `B2` affichaient
`CONCEPT`, `CONCEPT`, `CONTROLE` — avec `CONCEPT` en doublon.

Après :

| critère | suggestions |
| --- | --- |
| `B1_c1` aire | `CONCEPT` aire et périmètre confondus · `NOTATION` unité m pour une aire · `CALCUL` |
| `B1_c2` prix | `METHODE` prix calculé à partir du périmètre · `CALCUL` |
| `B2_c1` développement | `CONCEPT` distributivité sur le seul premier terme · `CALCUL` erreur de signe |
| `B2_c2` réduction | `CONCEPT` termes en x et constantes additionnés · `CALCUL` |
| `B2_c3` contrôle | `CONTROLE` aucun contrôle mené · `CALCUL` substitution |

Chaque suggestion porte son `criterion_id`. Aucune n'est cochée d'office : le score ne
déclenche jamais l'ajout d'un code. Les autres codes restent accessibles sous
« Autre code d'erreur que ceux suggérés », et `NON_CLASSIFIE` reste disponible.

## 9. Rendu mathématique

KaTeX 0.16.47, licence MIT, **copié depuis le poste** — aucun téléchargement, aucun CDN.
25 fichiers, 608 Ko : `katex.min.js`, `katex.min.css`, `auto-render.min.js` et 20 polices
`woff2`. Les variantes `woff` et `ttf` ont été écartées pour ne pas tripler le poids.
La feuille de style ne contient aucune URL distante.

Le rendu reconnaît `$…$`, `\(…\)`, `\[…\]` et `$$…$$`, et il est **cantonné aux éléments
portant la classe `math`** — énoncés, libellés, rubriques, corrigés. Une observation
saisie par l'enseignant est échappée par le gabarit et n'est jamais confiée au moteur.
Si KaTeX ne peut pas s'exécuter, la source LaTeX reste lisible en monospace plutôt que
de se confondre avec du texte courant.

## 10. Viewer PDF collant

Au-dessus de 1100 px, `.pane-pdf` est `position: sticky`, `top: 12px`,
`max-height: calc(100vh - 24px)`. Le sujet reste visible jusqu'au dernier critère et ne
recouvre jamais l'entête. En dessous de 1100 px, le sticky est désactivé et les deux
onglets « Sujet » / « Correction » reprennent la main.

## 11. Raccourcis clavier

Le garde-fou couvre désormais `input`, `textarea`, `select`, `button`, `option`, tout
élément `contenteditable`, et les rôles ARIA `textbox`, `checkbox`, `combobox` — y
compris via `closest()`, pour les éléments imbriqués. Il s'exécute **avant** toute
interprétation de touche, ce qu'un test vérifie en comparant les positions dans le source.

Un clic sur un bouton de score rend maintenant le focus au critère : les raccourcis sont
neutralisés sur les boutons, la navigation au clavier devait pouvoir reprendre.

## 12. Observations générales

Sept zones de texte libre sont devenues six listes déroulantes assorties d'un commentaire
facultatif, plus une seule grande zone « Remarque libre ». Un choix hors liste est
refusé : la valeur doit rester comparable d'un élève à l'autre. Rien n'est obligatoire,
et un test vérifie que le score ne bouge pas quand une observation est enregistrée.

La durée réellement observée reste saisissable, facultative, et affichée comme n'entrant
dans aucun calcul.

## 13. Base de données

Schéma passé de 1 à 2 : cinq colonnes sur `criterion_definition`, trois sur
`virtual_criterion_definition`. La migration est explicite, précédée d'une sauvegarde
automatique, et rejouable — un `duplicate column name` est absorbé, toute autre erreur
reste fatale.

**Anomalie signalée** — `§36` demandait de vérifier `corrections_real_count == 0`. Le
compte valait 1. Inspection : coquille vide créée le 21/08 à 19:08 par le test de fumée
du serveur de la mission précédente, 22 lignes `PENDING`, 0 score, 0 code, 0 observation,
un seul évènement d'audit. Ce n'était pas une saisie enseignant. Elle a été supprimée par
le réimport, après sauvegarde. La base livrée contient **0 correction, 0 score,
0 rapport**.

## 14. Tests

| suite | résultat |
| --- | --- |
| suite projet (documentation) | 25 / 25 PASS |
| couche post-distribution V3 | 98 PASS, 4 ignorés |
| harness `test_analyze_s5.py` | 48 / 48 PASS |
| application de correction | 120 PASS, 1 ignoré |
| dont tests ciblés Inès | 28 / 28 PASS |
| immutabilité | 60 / 60, changed = 0 |
| confidentialité | PASS, 4 333 fichiers contrôlés |

Les 28 tests Inès couvrent les quinze points exigés, plus la non-régression des quatre
overlays post-distribution (Sinda, Elyes, Ahmad, Malek), la préservation des 14 autres
élèves, et l'immutabilité finale.

### Deux tests existants modifiés, et pourquoi

`test_le_referentiel_importe_est_complet` et `test_un_critere_mixte_est_eclate_a_somme_constante`
comptaient 6 sous-critères et 3 critères mixtes. La revue curriculaire d'Inès en ajoute
respectivement 2 et 1. Ces tests n'encodaient pas une hypothèse fausse : ils figeaient un
effectif. La garantie qu'ils protégeaient — somme constante, aucune duplication — a été
**renforcée** plutôt que simplement ajustée : elle est désormais vérifiée sur tous les
critères mixtes quel qu'en soit le nombre, avec en plus le contrôle qu'aucun sous-critère
n'est dupliqué et que le critère parent ne se note pas lui-même.

Aucun test n'a été supprimé ni ignoré.

## 15. Dettes restantes

Consignées dans `docs/TECHNICAL_DEBT.md` et `docs/FUTURE_CURRICULUM_REVIEW.md`.

Les deux principales :

1. **La règle établie pour Inès concerne probablement Fares et Sinda.** `A3` et `B2` sont
   des items du noyau commun de Quatrième : ils sont identiques pour les trois. Leur
   classement n'a pas été touché — la mission l'interdisait — mais la question est
   ouverte et documentée.
2. **Seuls les 22 critères d'Inès ont une rubrique de score et des suggestions par
   critère.** Les 315 autres conservent l'échelle arithmétique et les erreurs de l'item.

Et une troisième, de nature différente : **le rendu réel dans un navigateur n'est pas
testé automatiquement.** Playwright reste absent, et la livraison ne doit pas en dépendre.
`docs/INES_UI_MANUAL_CHECKLIST.md` couvre ce que les tests DOM ne peuvent pas voir.
