# Micro-passe finale avant pilote réel — Inès KEFI

Application « Nexus S5 — Correction & Bilans », version **1.1.1**.
Passe conduite le 21 août 2026, après la passe corrective de pré-pilote et **avant**
la saisie de la première copie réelle.

Quatre objets, et rien d'autre : le rendu des structures LaTeX, la distinction entre
critères du sujet et lignes analytiques, le doublon de limite d'interprétation de C2,
et la preuve que deux périmètres curriculaires partageant un `skill_id` historique ne
se contaminent pas.

---

## 1. État initial

| élément | valeur relevée avant toute modification |
| --- | --- |
| branche | `main` |
| HEAD | `0abb9ed46b80e8db1766c9bf27a0f09d4f8c1244` |
| `origin/main` | `0abb9ed46b80e8db1766c9bf27a0f09d4f8c1244` |
| working tree | 24 entrées — travail correctif Inès non committé, préservé |
| artefacts distribués | 60 attendus, `changed = 0`, `missing = 0`, verdict PASS |
| corrections réelles en base | **0** |

La base `runtime/corrections.sqlite3` contenait une correction `DRAFT` pour
`asm-ines-kefi`, créée le 21/08 à 20:56 UTC. Inspectée avant toute action : 23 lignes
toutes `PENDING`, aucun score, aucune observation, aucun code d'erreur, aucune durée,
aucun bilan, un seul évènement d'audit `correction.created`. C'était une coquille
ouverte au premier affichage de la page, sans aucune donnée pouvant provenir de
l'enseignant. Rien n'a donc été supprimé au titre du §15 ; la base a été réimportée
plus tard dans la passe, sauvegarde prise (voir §8).

**Branches.** `fix/final-print-ready-audit-20260817` n'existe plus comme référence
locale : elle a été **renommée** en `main` le 21/08 à 13:11, lors d'une mission
antérieure, et subsiste sur `origin`. Aucune branche n'a été supprimée. Les quatre
branches à préserver sont intactes.

---

## 2. Fichiers modifiés

| fichier | nature |
| --- | --- |
| `app/latex_html.py` | **nouveau** — renderer structurel |
| `app/main.py` | enregistrement du filtre Jinja `enonce` |
| `app/templates/correction.html` | filtre appliqué, formulations 22/23, regroupement du détail |
| `app/templates/partials/validation_problems.html` | formulation 22/23 |
| `app/static/app.css` | mise en forme des listes d'énoncé |
| `app/static/app.js` | libellé de progression |
| `app/domain/correction.py` | `progress()` expose `original_criteria` |
| `app/domain/validation.py` | message lisible pour les sous-critères analytiques |
| `app/domain/importer.py` | mode `replace` explicite pour les limites d'interprétation |
| `app/data/criterion_overlays.py` | déclaration du mode `replace` sur C2 uniquement |
| `app/routes/correction.py` | `progress` transmis à la page de refus de validation |
| `app/__init__.py` | version 1.1.0 → 1.1.1 |
| `tests/test_ines_micropass.py` | **nouveau** — 34 tests |
| `tests/test_ines_pilot.py` | deux tests mis à jour et renforcés |
| `docs/INES_UI_MANUAL_CHECKLIST.md` | section 0 (14 contrôles), test clavier détaillé |

Aucun document distribué, aucun fichier de `S5_release/`, `S5_audit/` ou
`S5_post_distribution_v3/` n'a été touché.

---

## 3. Renderer structurel

KaTeX rend les expressions mathématiques ; il ne transforme pas les environnements
documentaires. Les énoncés structurés s'affichaient donc littéralement.

### Périmètre, établi sur le corpus réel

Inventaire des constructions LaTeX présentes dans les 16 manifestes d'évaluation :

| construction | corpus entier | énoncés d'Inès | traitée |
| --- | ---: | ---: | --- |
| `\begin{enumerate}` | 94 | 6 | **oui** → `<ol>` |
| `\item` | 241 | 15 | **oui** → `<li>` |
| `\textbf` | 17 | 1 | **oui** → `<strong>` |
| `\begin{itemize}` | **0** | **0** | non — absent du corpus |
| `\begin{lstlisting}` | 9 | 0 | non — hors périmètre |
| `\begin{tabularx}` | 2 | 0 | non — hors périmètre |
| `\emph` | 6 | 0 | non — hors périmètre |
| `\par` | 2 | 0 | non — hors périmètre |

`itemize` n'a **pas** été implémenté : le §4.1 le conditionnait à sa présence réelle
dans les énoncés utilisés, et il n'apparaît nulle part. La décision est figée par un
test, qui échouerait si un énoncé venait à en introduire un.

Les quatre dernières constructions concernent des élèves de NSI et de seconde, jamais
Inès. Elles restent affichées littéralement, **exactement comme avant cette passe** :
aucune régression n'est introduite, aucune amélioration non plus. C'est une limite
connue, consignée au §10.

### Sécurité

Deux règles, dans cet ordre :

1. le texte est **intégralement échappé avant** toute insertion de balise. Un `<`
   présent dans la source devient `&lt;` et ne peut jamais ouvrir un élément. Les
   seules balises du résultat sont celles que le module écrit lui-même, depuis une
   liste fermée de trois constructions ;
2. le filtre ne s'applique qu'à `item.statement` et `item.expected_answer` — les deux
   seuls champs du référentiel porteurs de LaTeX structurel. **Aucune saisie
   enseignant ne passe par lui** : observations de critère, observations d'item et
   remarque libre restent échappées par le gabarit, comme du texte.

`\textbf` n'est converti qu'en dehors des délimiteurs mathématiques : à l'intérieur,
la commande appartient à KaTeX et lui parvient intacte.

### Résultat

B2 s'affiche désormais :

> 1. Développer 5(x − 3).
> 2. Réduire ensuite 5(x − 3) + 2x + 7.
> 3. Contrôler le résultat obtenu pour x = 2, en calculant séparément les deux écritures.

Même transformation pour B1, B3, B4, C1 et C2. C1 conserve son titre en gras.

---

## 4. Sémantique 22 / 23

Le sujet distribué comporte **22 critères imprimés**. L'éclatement analytique du
critère mixte A3 porte à **23** le nombre de lignes à renseigner. L'affichage
`0 / 23 critères renseignés` était donc faux au sens propre.

| grandeur | valeur | inchangée |
| --- | ---: | --- |
| critères originaux du sujet | 22 | oui |
| lignes analytiques à renseigner | 23 | oui |
| score brut maximal | 20,00 | oui |
| consolidation N−1 maximale | 17,50 | oui |
| passerelles N maximales | 2,50 | oui |
| A3 : somme des sous-critères | 0,50 + 0,50 = 1,00 | oui |

`progress()` expose désormais les deux comptes séparément, `original_criteria` étant
dérivé du nombre de `criterion_id` distincts — jamais codé en dur.

**En-tête.** « 22 critères du sujet · 0 / 23 lignes analytiques renseignées — 0 % »

**Bandeau.** « 23 lignes analytiques restent à renseigner pour les 22 critères du
sujet, avant validation. »

**Détail des manques.** Les manques sont regroupés par item du sujet. A3 n'apparaît
donc qu'une fois, avec ses deux sous-critères imbriqués, désignés par leur périmètre
et leur libellé au lieu de leurs identifiants bruts `_v1` / `_v2` :

> **A3**
> - sous-critère analytique N−1 — Regroupement des termes en x : non renseigné
> - sous-critère analytique passerelle N — Écriture réduite complète, constantes signées comprises : non renseigné

Aucun document n'affirme rétrospectivement qu'Inès « avait 23 critères au sujet ».

---

## 5. Doublon C2

Le critère `4E_INES_KEFI_C2_c2` portait deux mises en garde quasi identiques, parce
que deux couches indépendantes en produisaient chacune une :

| couche | formulation |
| --- | --- |
| `S5_post_distribution_v3/tools/scope_rules.py` | « … mesurées séparément en **A1 et A5** » |
| `app/data/criterion_overlays.py` | « … mesurées séparément en **A1, A5 et C2 question 1** » |

L'importeur concaténait les deux listes en dédupliquant par égalité exacte de chaîne ;
les deux phrases différant d'un membre, elles survivaient toutes les deux.

**Correction, au point le plus étroit possible.** L'importeur accepte désormais un
mode explicite `interpretation_limits_mode: "replace"`, déclaré **critère par
critère**. Il est posé sur `4E_INES_KEFI_C2_c2` et sur lui seul ; partout ailleurs le
comportement de concaténation est inchangé. La couche V3 n'a pas été modifiée : ni
`scope_rules.py`, ni `criteria_scope.json`, ni les overlays V3 déjà validés.

La formulation conservée est la plus complète — celle qui cite C2 question 1, où la
somme et la différence de relatifs sont justement mesurées.

---

## 6. Audit skill_id historique / curriculum_scope

C'était le point le plus important de cette passe, et un blocker potentiel.

### 6.1 Le chevauchement est réel

| `analysis_skill_id` | périmètres | lignes concernées |
| --- | --- | --- |
| `M4E_LIT_01` | `n_minus_1` **et** `bridge_n` | C1_c3 (1,5) et C1_c4 (1,0) en N−1 ; B2_c1 (0,5) en passerelle |
| `M4E_LIT_02` | `n_minus_1` **et** `bridge_n` | B2_c3 (1,0) et A3_c1_v1 (0,5) en N−1 ; B2_c2 (0,5) en passerelle |

`C2_c2` ne figure pas dans ce tableau : la passe précédente lui avait déjà donné un
identifiant d'analyse distinct, `M4E_REL_PROD_BRIDGE`, alors que son `skill_id`
d'origine reste `M4E_REL_01`. La séparation y est donc acquise au niveau de
l'identifiant lui-même.

### 6.2 Mécanisme d'agrégation réel

**L'agrégation ne se fait pas par `skill_id` seul.** `app/domain/analysis.py`
construit ses seaux sur une clé composite :

```python
key = (e["analysis_skill_id"], e["curriculum_scope"])
```

La séparation est ensuite maintenue à chaque étape en aval :

| étape | mécanisme |
| --- | --- |
| pools de points | `pool(scope)` filtre sur `curriculum_scope` |
| statut de compétence | branchement explicite : `bridge_status()` si `bridge_n`, `n1_status()` sinon |
| rang de priorité | calculé pour le seul N−1 ; une passerelle a `priority_rank = None` |
| profil d'erreurs | `error_profile(scope)` ignore toute compétence d'un autre périmètre |
| consolidation N−1 | `n_minus_1_consolidation = pool("n_minus_1")` |
| force de la preuve | calculée par seau, donc par couple (compétence, périmètre) |

Le seul point où un `skill_id` seul sert de clé est
`baselines = {b.skill_id: b for …}`, utilisé pour renseigner un libellé qualitatif
d'affichage `baseline_status_qualitative`. Ce champ n'entre dans aucun score, aucun
statut, aucun rang, aucun profil d'erreurs, et `mastery_delta` reste `None` en toute
circonstance. Il ne peut donc pas contaminer une grandeur N−1.

**Conclusion : le code était déjà sûr.** Conformément au §9.7, aucun refactor n'a été
entrepris. Seuls des tests de non-régression ont été ajoutés.

### 6.3 Formulation à retenir

> `historical_skill_id` may overlap across scopes.
> Analysis isolation is guaranteed by the composite bucket key
> `(analysis_skill_id, curriculum_scope)` in `app/domain/analysis.py`, and preserved
> downstream by per-scope filtering of pools, error profiles, statuses and priorities.

### 6.4 Contamination N−1 possible ?

**NON.** Vérifié par trois scénarios synthétiques, et non par lecture seule du code.

---

## 7. Tests

| suite | avant | après |
| --- | --- | --- |
| suite projet | 25 | **25** |
| post-distribution V3 | 98 (4 ignorés) | **98 (4 ignorés)** |
| application correction | 120 (1 ignoré) | **154 (1 ignoré)** |
| dont tests Inès (pilote) | 28 | **28** |
| dont nouveaux tests (micro-passe) | — | **34** |
| harness `test_analyze_s5` | 48 | **48** |

Aucun échec. **Aucun test supprimé.** Le nombre d'ignorés n'augmente pas : il reste
de 4 en V3 et de 1 dans l'application, exactement comme avant la passe.

Deux tests existants ont été **mis à jour** — `test_13` et `test_13b` de
`test_ines_pilot.py` — parce que le §6.2 imposait précisément de changer la
formulation sur laquelle ils s'appuyaient. Ils n'ont pas été affaiblis : ils
vérifient désormais en plus que les deux comptes, 22 et 23, sont tous deux lisibles.

### Les 34 nouveaux tests

**Renderer (§5).** TEST A : `enumerate` produit un `<ol>` avec le bon nombre de
`<li>` ; prose conservée ; un item sur plusieurs lignes reste un seul item. TEST B :
aucune des trois séquences `\begin{enumerate}`, `\end{enumerate}`, `\item` ne subsiste
dans le HTML servi de la page d'Inès. TEST C : les délimiteurs mathématiques survivent
à la mise en liste et le conteneur porte toujours la classe `math`. TEST D : une
observation enseignant contenant `\begin{enumerate}`, `<script>` et `<b>` reste du
texte échappé — aucune balise active, aucune liste fabriquée. TEST E : six expressions
inline traversent le renderer sans altération. Trois tests de sécurité supplémentaires
vérifient qu'aucune balise arbitraire ne survit, y compris à l'intérieur d'un item.

**Sémantique 22/23 (§7).** `original_criteria_count == 22`,
`analytic_scoring_line_count == 23`, somme des points analytiques `== 20,00`,
`sum(A3_virtual_max) == A3_original_max == 1,00`, absence de double comptage (le
critère parent mixte n'est jamais noté), et l'écart 23 − 22 est exactement la somme
des parties supplémentaires des critères mixtes.

**Doublon C2 (§8).** Une seule limite de cette nature sur C2 ; c'est la formulation
complète qui est conservée ; aucun autre critère d'Inès ne porte de limite dupliquée ;
le mode `replace` ne concerne qu'un seul critère dans tout le référentiel.

**Isolation (§9).** L'audit du chevauchement est lui-même un test : il vérifie d'abord
que la situation décrite existe réellement dans les données, puis que l'analyse produit
bien deux entrées disjointes par identifiant partagé, sans qu'aucune ligne ne soit
comptée deux fois. Puis les trois scénarios.

**Autres élèves (§13).** Les 14 autres couples recomposent exactement leur total
imprimé et n'ont aucun périmètre inconnu. L'inventaire des critères mixtes de toute
l'application est figé : quatre au total, dont trois préexistants à la passe Inès.

### Scénarios d'isolation

**Scénario 1 (§9.3)** — B2_c1 (passerelle, `M4E_LIT_01`) à 0 avec une erreur
`CONCEPT`, C1_c3 et C1_c4 (N−1, même `M4E_LIT_01`) au maximum :

- le N−1 reste entièrement réussi, `success_rate = 1.0`, 2,50 sur 2,50 ;
- son statut n'est ni `A_CONSOLIDER` ni `PRIORITAIRE` ;
- `error_codes` du N−1 est vide, et `CONCEPT` n'apparaît pas au profil N−1 ;
- les preuves ne sont pas mélangées : le seau N−1 ne contient que C1_c3 et C1_c4, le
  seau passerelle ne contient que B2_c1 ;
- la passerelle est marquée `BRIDGE_REVISIT` ou `DISCOVERY_TO_CONTINUE`, avec
  `priority_rank = None` ;
- `n_minus_1_consolidation = 100 %`.

**Scénario 2 (§9.4)** — B2_c2 (passerelle, `M4E_LIT_02`) à 0 avec une erreur `CALCUL`,
B2_c3 (N−1, même `M4E_LIT_02`) au maximum :

- la compétence de contrôle par substitution reste réussie ;
- `CALCUL` n'apparaît pas au profil N−1 ;
- la passerelle réduction peut être à revoir, sans qu'aucun des mots « non acquis »,
  « lacune », « fragile » ou « prioritaire » n'apparaisse dans sa lecture.

**Scénario 3 (§9.5)** — toutes les passerelles à 0, tous les N−1 au maximum :
`n_minus_1_consolidation = 100 %`, 17,50 disponibles en N−1 et 2,50 en passerelle,
profil d'erreurs N−1 vide, et aucune ligne d'un autre périmètre n'a servi de preuve à
une compétence N−1. Ce scénario était déjà couvert par la passe précédente ; il est ici
renforcé par la vérification ligne à ligne des preuves.

---

## 8. Immutabilité et confidentialité

| contrôle | résultat |
| --- | --- |
| `immutable_artifacts_total` | **60** |
| `immutable_artifacts_changed` | **0** |
| `immutable_artifacts_missing` | **0** |
| verdict | **PASS** |
| sources V3 importées | toutes inchangées |
| données réelles suivies par Git | **aucune** (4 359 fichiers contrôlés) |
| corrections réelles en base | **0** |
| scores saisis en base | **0** |

Vérifié par les deux couches indépendamment : `freeze_student_artifacts.py --verify`
et `app/domain/immutability.verify()`.

**Réinitialisation de la base.** L'application ne réimporte le référentiel que si la
base n'existe pas. Sans réinitialisation, le correctif C2 n'aurait pas été visible au
contrôle visuel. `tools/init_database.py --force` a donc été exécuté : il prend une
sauvegarde avant de supprimer (`runtime/backups/corrections_20260821_223123.sqlite3`),
puis réimporte. La seule donnée perdue est la coquille `DRAFT` vide décrite au §1.
La base résultante contient 0 correction et 0 score.

Aucune donnée réelle n'a été saisie. Toutes les valeurs employées par les tests sont
synthétiques, dans des bases jetables créées par `conftest`, jamais dans `runtime/`.

---

## 9. Version

**1.1.0 → 1.1.1.** Le dépôt versionne les changements visibles par l'utilisateur : la
passe précédente était passée de 1.0.0 à 1.1.0 pour cette raison. Cette micro-passe
modifie l'affichage des énoncés et deux formulations de l'interface, ce qui relève de
la même catégorie. Le §19 autorisait explicitement 1.1.1 et interdisait 1.2.0.

---

## 10. Limites restantes

1. **`lstlisting`, `tabularx`, `emph` et `par` ne sont pas rendus.** Ces constructions
   existent dans le corpus (9, 2, 6 et 2 occurrences) mais dans aucun énoncé d'Inès.
   Elles restent affichées littéralement, comme avant cette passe. À traiter avant
   d'ouvrir le pilote aux élèves de NSI et de seconde.
2. **Le rendu navigateur n'est pas testé automatiquement.** Playwright n'est pas
   installé. `TestClient` vérifie le HTML servi ; il ne vérifie pas ce que Chrome
   affiche. D'où la checklist manuelle.
3. **L'extraction textuelle de KaTeX produit des duplications MathML/HTML.** Ce n'est
   pas un défaut visible dans le navigateur et aucun correctif n'a été écrit pour le
   masquer, conformément au §17.
4. **Le mode `replace` des limites d'interprétation est déclaratif.** Si la couche V3
   modifiait un jour la formulation qu'il remplace, le remplacement resterait valable
   mais la justification écrite ici deviendrait obsolète. Le test d'unicité sur C2
   continuerait toutefois de garantir l'absence de doublon.
5. **La justesse pédagogique des rubriques n'est pas jugée.** Elle ne peut l'être
   qu'en corrigeant une vraie copie — objet de `PILOT_REAL_COPY_VALIDATION.md`.

---

## 11. Statut

**READY_FOR_PILOT.**

Les six conditions du §23 sont remplies : artefacts distribués inchangés (0), 22
critères clairement distingués de 23 lignes analytiques, aucune structure `enumerate`
brute sur les énoncés d'Inès, maths inline intactes, limite C2 unique, périmètres N−1
et passerelle analytiquement isolés malgré le partage de `skill_id`, aucune donnée
réelle saisie, toutes les suites au vert.

Aucun commit, aucun push, aucune pull request. Les modifications sont locales et
visibles dans `git status`.

### Prochaine action humaine

1. `make s5-correction-run`
2. ouvrir `http://127.0.0.1:8765/eleve/ines-kefi`
3. dérouler `docs/INES_UI_MANUAL_CHECKLIST.md`, section 0 d'abord
4. tester les raccourcis dans les deux zones de saisie (section 8)
5. **seulement ensuite**, saisir la vraie copie d'Inès
