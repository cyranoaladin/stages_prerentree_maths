# Audit indépendant — S5 de clôture des stages Nexus Réussite

**Date :** 21 août 2026  
**Archive auditée :** `S5_cloture_AUDIT.tar.gz`  
**Objet :** contre-audit technique, scientifique, pédagogique, docimologique, données/LLM et sécurité de la livraison S5.

## Verdict exécutif

**HOLD — la livraison ne doit pas encore être distribuée aux élèves ni utilisée pour générer des bilans parents.**

La production est très solide sur la chaîne LaTeX/PDF, l'organisation des livrables, la séparation élève/enseignant et la structuration JSON. En revanche, plusieurs défauts substantiels ont été identifiés :

1. l'audit de durée à 41 minutes est rendu circulaire par un écrasement programmatique des durées ;
2. les deux évaluations NSI sont objectivement surchargées pour 45 minutes selon leurs propres estimations d'origine (54,5 et 55 min) ;
3. le calcul de `mastery_delta` convertit un statut qualitatif initial en score numérique 0–4 alors que les profils déclarent ne pas disposer de résultats initiaux item par item ;
4. l'agrégation des compétences répartit arbitrairement le score d'un item à parts égales entre toutes ses compétences ;
5. le schéma JSON de diagnostic final et la sortie réelle de `analyze_s5.py` ne sont pas compatibles ;
6. plusieurs formulations/corrigés comportent des défauts scientifiques ou de validité de justification ;
7. les acquis travaillés pour la première fois juste avant le post-test ne sont pas distingués d'une consolidation durable ;
8. le runner NSI exécute le code élève dans un sous-processus, mais pas dans une sandbox de sécurité ;
9. les blueprints ne fixent pas explicitement les références réglementaires 2026 applicables ;
10. le paquet contient des caches Python et ne reproduit pas seul la validation de traçabilité vers les sources S1–S4.

## 1. Contrôles indépendants effectués

### 1.1 Intégrité de l'archive

- Pas de chemin absolu dans le tar.
- Pas de traversée `..` détectée.
- Pas de lien symbolique, hard-link ou périphérique dangereux détecté.
- **333 fichiers réguliers dans l'archive d'origine.**

Répartition :

| Type | Nombre |
|---|---:|
| `.json` | 127 |
| `.tex` | 45 |
| `.pdf` | 45 |
| `.log` | 45 |
| `.py` | 28 |
| `.md` | 24 |
| `.pyc` | 17 |
| `.sty` | 1 |
| `.sh` | 1 |
| **Total** | **333** |

Le résumé Claude annonçait 316 fichiers ; **333 − 17 `.pyc` = 316**, ce qui indique vraisemblablement qu'il a exclu les caches Python de son décompte. Cependant, sa ventilation publiée ne totalisait que 271 car elle omettait aussi les 45 `.log`. Le rapport de livraison doit être rendu arithmétiquement exact.

### 1.2 Compilation LaTeX indépendante

- **45/45 fichiers `.tex` recompilés avec succès.**
- Aucun échec bloquant observé lors de la recompilation indépendante.
- Aucun PDF identique octet pour octet entre deux livrables ; idem pour les 45 `.tex`.

### 1.3 Contrôle visuel indépendant complet

Contrairement à l'échantillon de 18 documents annoncé par Claude, l'audit indépendant a rasterisé **les 45 PDF, soit 351 pages**.

Résultat :

- pas de page blanche accidentelle détectée ;
- pas de clipping gauche/droite significatif ;
- pas de collision majeure de blocs ;
- pas de glyphes manifestement absents ;
- entêtes/pieds de page globalement cohérents ;
- tableaux, TikZ, code et espaces de réponse visuellement exploitables.

**Verdict visuel : PASS.** Les pages parfois très aérées sont principalement justifiées par les espaces de réponse/brouillon.

### 1.4 Validateur livré

Sur l'archive seule :

```text
contrôles exécutés : 4350
échecs critiques  : 15
avertissements    : 0
RESULTAT : FAIL
```

Les 15 erreurs correspondent exactement aux 15 couples élève × matière et concernent l'absence, dans l'archive, des sources originales S1–S4/diagnostics auxquelles les profils font référence.

Cela ne prouve pas que les 4350/0 annoncés dans le dépôt parent soient faux ; cela montre que **l'archive livrée n'est pas autoportante pour reproduire cette validation**. Le rapport doit donc distinguer :

- validation **dans le dépôt source complet** ;
- validation **du paquet S5 autonome**.

## 2. Blocage critique — durée de l'évaluation

### 2.1 Audit circulaire à 41 minutes

Dans `tools/data/common.py`, une table globale impose :

```python
ITEM_MINUTES = {
    "A1": 1.5, "A2": 1.5, "A3": 1.5, "A4": 1.5, "A5": 1.5, "A6": 1.5,
    "B1": 5, "B2": 5, "B3": 5, "B4": 4,
    "C1": 9, "C2": 4,
}
EXAM_TARGET_MINUTES = 41
```

Dans `tools/core.py`, `exam_items()` écrase ensuite les durées définies dans les banques d'items :

```python
src["minutes"] = common.ITEM_MINUTES[iid]
```

avec le commentaire explicite indiquant que cela « garantit une somme de 41 min pour tous les élèves ».

Par conséquent, `audit_docimologie.py` ne mesure pas indépendamment la faisabilité : il relit une valeur imposée par conception.

### 2.2 Durées originales avant écrasement

| Élève / matière | Durée brute déclarée dans les items |
|---|---:|
| Fares DARGHOUTH — 4e maths | 45,0 min |
| Ines KEFI — 4e maths | 45,0 min |
| Sinda CHIKHAOUI — 4e maths | 45,0 min |
| Amine MANSOURI — 3e maths | 45,5 min |
| Elyes KEFI — 3e maths | 45,5 min |
| Fares LAAJILI — 3e maths | 46,0 min |
| Sarah BARGAOUI — 3e maths | 45,5 min |
| Selim MANSOURI — 3e maths | 45,0 min |
| Ahmed BAKIR — 2nde maths | 46,5 min |
| Noa MANIACI — 2nde maths | 46,0 min |
| Ahmad BELDI — 1re spé maths | 45,5 min |
| Donia KHADHRANI — 1re spé maths | 47,0 min |
| Malek KHADHRANI — 1re spé maths | 47,0 min |
| Ahmad BELDI — 1re NSI | **54,5 min** |
| Ahmed BENHADJ SALEM — 1re NSI | **55,0 min** |

Les mathématiques sont généralement proches de la cible, mais plusieurs sujets sont déjà au-dessus de 45 min sans marge. La NSI est nettement trop longue.

### 2.3 Correctif requis

- Ne plus écraser les durées d'items.
- Conserver une estimation propre à chaque item.
- Effectuer un second audit de temps indépendant du générateur.
- Viser plutôt **40–42 minutes médianes** pour laisser 3–5 minutes de lecture/relecture.
- Réduire substantiellement l'évaluation NSI.

## 3. Blocage critique — mesure de progression non défendable

Tous les profils indiquent en substance que les dossiers initiaux fournissent des **statuts par domaine**, mais pas les réponses réelles aux items du diagnostic initial.

Pourtant `analyze_s5.py` transforme :

```python
"acquis" -> 3
"en_voie_acquisition" -> 2
"fragile" -> 1
```

puis compare cette valeur au `post_mastery` issu du score S5 et peut calculer :

```python
mastery_delta = post - base
```

lorsqu'un item final possède un `baseline_item` parallèle.

Le problème est conceptuel : **l'existence de l'énoncé initial ne constitue pas une mesure initiale de l'élève**. Sans réponse/score initial nominatif, le delta numérique n'est pas une mesure de progrès psychométriquement défendable.

### Correctif requis

Tant que les réponses initiales item par item ne sont pas récupérées :

- `mastery_delta = null` pour tous les élèves ;
- ne jamais employer `progression_documented` au sens numérique ;
- conserver une comparaison qualitative du type :
  - `post_only` ;
  - `indicative_skill_comparison` ;
  - `not_comparable` ;
- réserver un delta chiffré à un futur cas où des preuves initiales appariées sont disponibles.

**`render_bilan.py` ne doit pas être utilisé en production avant cette correction.**

## 4. Défaut de validité — agrégation par compétence

Le code répartit actuellement le score total de chaque item à parts égales entre toutes les compétences taguées :

```python
share_max = i["max_points"] / len(i["skills"])
share_got = i["points"] / len(i["skills"])
```

Cela peut créditer une compétence non réellement réussie.

Exemple type : un item de 2 points comporte une sous-question d'aire et une sous-question de proportionnalité. Si seule l'aire est correcte, un partage 50/50 du score total ne permet pas d'identifier quelle compétence est effectivement réussie.

### Correctif requis

Passer à un barème au niveau des critères :

```json
{
  "criterion_id": "B1_c1",
  "points": 1,
  "skill_id": "...",
  "evidence_type": "application"
}
```

Les réponses doivent permettre la saisie de scores par critère ou sous-question. Les scores de compétence doivent être calculés à partir de ces critères, non d'une division uniforme.

## 5. Défaut de schéma JSON

Le fichier `post_stage_analysis_schema.json` exige, pour chaque compétence :

```json
"required": ["skill_id", "post_mastery", "comparability"]
```

et définit un champ `comparability`.

Or `analyze_s5.py` produit un champ :

```json
"comparison_status": status
```

et ne renseigne pas `comparability` dans l'objet compétence produit.

La sortie réelle de l'analyse n'est donc pas conforme à son propre schéma déclaré.

### Correctif requis

- Définir un modèle canonique unique.
- Versionner le schéma (`v2`) si nécessaire.
- Faire valider **la sortie réelle de `analyze_s5.py`** par `jsonschema` dans les tests CI.
- Interdire un PASS global si la sortie générée ne passe pas son schéma.

## 6. Terme `measurement_reliability` impropre

Le code déclare :

```python
"measurement_reliability": "fragile" if a["max"] < 2 else "acceptable"
```

Ce n'est pas une mesure de fiabilité au sens docimologique/psychométrique. Deux points affectés à une compétence ne rendent pas une mesure « fiable ».

Le schéma affirme en plus que `fragile` correspond à une compétence reposant sur un seul item, ce qui n'est pas la règle réellement implémentée.

### Correctif requis

Renommer en `evidence_strength` et l'estimer à partir de :

- nombre de critères indépendants ;
- nombre d'items ;
- nombre de points ;
- présence d'une tâche de transfert ;
- comparabilité avec une mesure initiale réelle ;
- proximité temporelle d'une remédiation.

## 7. Effet de récence et consolidation durable

Pour plusieurs élèves de 4e/3e, les statistiques sont diagnostiquées initialement mais ne sont retravaillées qu'en S5 juste avant l'évaluation.

Une réussite 30 à 60 minutes après remédiation mesure une **performance immédiate**, pas nécessairement une consolidation durable.

### Correctif requis

Ajouter :

```json
{
  "post_test_context": "immediate_after_remediation",
  "retention_status": "not_yet_verified",
  "recommended_delayed_check": true
}
```

et prévoir un mini-test différé en semaine 1 ou 2 de rentrée.

Même principe pour les contenus réellement nouveaux introduits en phase 4 : ils doivent être exclus de tout calcul de progression N−1 → N.

## 8. Défauts scientifiques/pédagogiques concrets à corriger

### 8.1 Elyes KEFI — 3e — statistique

Un exercice porte sur une moyenne erronée après omission de la valeur 5 et propose comme contrôle détecteur à la fois le recomptage et l'encadrement de la moyenne entre 5 et 15.

Or **11,25 est bien compris entre 5 et 15** : l'encadrement ne détecte donc pas l'omission.

**Correction :** le contrôle détecteur doit reposer sur le recomptage de l'effectif, la somme ou la confrontation à la liste source ; l'encadrement peut rester un contrôle de vraisemblance général, mais pas être présenté comme détectant cette omission.

### 8.2 Sinda CHIKHAOUI — 4e — aire du triangle

Le corrigé affirme que le triangle est la moitié « d'un rectangle obtenu par duplication autour du milieu d'un côté ».

Une symétrie centrale/rotation de 180° autour du milieu d'un côté produit en général un **parallélogramme**, pas nécessairement un rectangle.

**Correction :** deux triangles congruents permettent de former un parallélogramme de même base et hauteur ; son aire vaut `base × hauteur`, donc celle du triangle vaut la moitié.

### 8.3 Ahmad BELDI — 1re spé — comparaison `x³` / `x²`

La question demande une conclusion valable pour tout `0 < x < 1` « en appuyant la réponse sur un exemple numérique ». Un exemple ne démontre pas une propriété universelle, alors que le barème exige aussi un argument général.

**Correction :** demander explicitement « justifier puis illustrer par un exemple » et écrire dans la réponse : `x² > 0` et `x-1 < 0`, donc `x³-x²=x²(x-1)<0`.

### 8.4 Malek KHADHRANI — 1re spé — fonction inverse

La consigne demande si `1/x` est croissante sur `]0,+∞[` et propose deux valeurs. Deux valeurs suffisent à **réfuter la croissance**, mais pas à démontrer globalement que la fonction est décroissante.

**Correction possible :** conclure seulement « non : 1 < 2 mais f(1) > f(2) » ; ou demander une véritable preuve de décroissance si cette propriété doit être établie.

### 8.5 Phase 4 — entrée en 4e

Le texte annonce comme nouveautés le produit/quotient de relatifs et les équations, puis affirme que les activités « ne demandent aucune connaissance nouvelle ».

**Correction :** présenter la phase comme une **découverte guidée / pont vers la 4e**, et non comme un simple réemploi de connaissances déjà acquises.

### 8.6 Phase 4 — entrée en 3e

Même contradiction pour la double distributivité et le vocabulaire des fonctions, qualifiés de nouveautés puis de « rien de neuf ».

**Correction :** distinguer explicitement prérequis réinvestis et premiers éléments nouveaux.

### 8.7 Phase 4 — entrée en 1re spé

« La suite n'est qu'une évolution répétée » est une généralisation fausse : toutes les suites ne modélisent pas une évolution répétée.

**Correction :** « certaines suites, notamment les suites géométriques, modélisent une évolution répétée ».

Le programme Python annoncé comme affichant les « cinq premiers termes » initialise `u=2000`, puis multiplie avant affichage dans `range(5)` : il affiche en réalité `u1` à `u5`, pas `u0` à `u4`.

**Correction :** écrire « les cinq termes suivants » ou modifier le programme pour afficher `u0` avant la boucle.

### 8.8 Phase 4 NSI — recherche dichotomique

Le corrigé accepte un élément central 19 ou 25 « selon convention », puis affirme que trois étapes suffisent pour trouver 41.

Avec certaines conventions de milieu, 41 est atteint en deux comparaisons ; avec d'autres, trois.

**Correction :** fixer la convention de calcul de l'indice milieu ou accepter explicitement 2/3 étapes selon convention.

### 8.9 Taxonomie des erreurs / équité de correction

Plusieurs erreurs probables codent comme faute une action non explicitement demandée ou une méthode mathématiquement valide mais moins efficace.

Exemples :

- ne pas pénaliser l'absence de vérification si la consigne ne la demande pas ;
- développer une équation-produit avant de la résoudre est inefficace mais pas conceptuellement faux ; ne pas coder cela automatiquement `CONCEPT` si la résolution reste correcte.

**Règle à imposer :** un code d'erreur doit correspondre à un comportement observable et à une exigence explicite du sujet ; toute méthode mathématiquement valide doit pouvoir obtenir le crédit correspondant.

## 9. Alignement programmes 2026 — traçabilité insuffisante

Les blueprints devraient embarquer une référence réglementaire explicite avec version et année d'effet.

Règles à respecter :

- **Entrée en Seconde 2026 :** transition depuis les acquis de 3e 2025-2026 vers le nouveau programme de Seconde applicable dès 2026-2027.
- **Entrée en 1re spécialité maths 2026 :** transition depuis la Seconde 2025-2026 vers le nouveau programme de spécialité de Première applicable en 2026-2027.
- **Entrée en 4e/3e 2026 :** ne pas appliquer prématurément la nouvelle progression de cycle 4 à ces classes ; son déploiement est progressif (5e en 2026, 4e en 2027, 3e en 2028).
- **Entrée en 1re NSI :** programme de Première NSI 2019 toujours présenté comme programme en vigueur en 2026.

Ajouter aux blueprints :

```json
"curriculum_reference": {
  "NOR": "...",
  "BO_date": "...",
  "effective_school_year": "...",
  "transition": "N-1 -> N"
}
```

## 10. Sécurité NSI — exécution de code élève non sandboxée

`_teacher_private/tests_s5_nsi.py` charge le fichier de l'élève dans un nouveau processus Python avec un timeout.

Le timeout protège contre une boucle infinie, mais **un sous-processus n'est pas une sandbox de sécurité**. Le code exécuté conserve les permissions du compte : fichiers, réseau, lancement de processus, variables d'environnement, etc.

### Correctif requis

Soit :

- ne jamais exécuter automatiquement un fichier non relu ;

soit utiliser un conteneur jetable avec :

- réseau désactivé ;
- système de fichiers en lecture seule sauf `/tmp` ;
- aucun `$HOME` ni secret monté ;
- limites CPU/RAM/PID ;
- utilisateur non privilégié ;
- timeout externe.

La documentation actuelle doit au minimum dire « sous-processus séparé, non sandboxé ».

## 11. Paquetage et reproductibilité

### 11.1 Caches Python

L'archive contient 17 `.pyc`/`__pycache__`. Ils ne doivent pas être livrés.

### 11.2 Logs de build

Les 45 `.log` peuvent être utiles dans un paquet d'audit, mais pas dans le paquet distribué aux élèves.

Recommandation : distinguer :

- `S5_release/` — uniquement fichiers nécessaires à l'exploitation ;
- `S5_audit/` — logs, tests, rapports, preuves.

### 11.3 Traçabilité des sources

Le paquet n'embarque pas les sources S1–S4/diagnostics d'origine. Pour rendre l'audit reproductible sans divulguer tout le corpus, ajouter un `source_evidence_manifest.json` contenant au minimum :

- chemin canonique ;
- SHA-256 ;
- type de source ;
- élève/matière ;
- compétences/observations réellement extraites ;
- éventuellement courts extraits de preuve non sensibles.

## 12. Personnalisation — constat et limite

Points positifs :

- aucun des 45 PDF n'est identique octet pour octet ;
- aucun des 45 `.tex` n'est identique ;
- l'architecture prévoit des éléments individuels ;
- les profils et manifestes relient les priorités à des compétences.

Limite : un score de similarité lexicale/Jaccard ne démontre pas à lui seul la personnalisation pédagogique.

La preuve forte à produire pour chaque priorité est :

`preuve diagnostic -> priorité -> activité S5 -> critère d'évaluation -> décision rentrée`.

## 13. Cas des 1res spé sans supports personnalisés S2–S4

Pour Ahmad BELDI, Donia KHADHRANI et Malek KHADHRANI, l'absence de livrets individualisés S2–S4 interdit toute affirmation du type « cette difficulté a été travaillée individuellement en S2 puis consolidée en S3 » sans preuve.

Le futur bilan doit distinguer :

- contenu commun proposé au groupe ;
- observation individuelle effectivement documentée ;
- performance finale S5.

## 14. Canonicalisation de la livraison 4e

Le QA signale que certains élèves de 4e possèdent déjà d'anciens S4/S5 personnalisés d'une autre architecture.

Avant distribution, créer un manifeste canonique :

```json
{
  "student_id": "...",
  "subject": "...",
  "canonical_work_pdf": "...",
  "canonical_assessment_pdf": "...",
  "supersedes": ["..."]
}
```

afin d'éviter l'envoi du mauvais S5.

## 15. Ce qui est réellement réussi

La livraison présente plusieurs qualités importantes qu'il faut conserver :

- bonne séparation entre livret de travail, évaluation et dossier enseignant ;
- absence de résultat final fictif avant passation ;
- compilation LaTeX robuste ;
- rendu visuel propre sur l'ensemble des 351 pages auditées ;
- JSON structurés et nombreux garde-fous de cohérence ;
- barème commun 14/20 + individualisation 6/20 cohérent comme principe ;
- distinction explicite entre contenu travaillé et acquisition, dans de nombreux endroits ;
- tests de saisie et refus des valeurs hors barème dans l'analyseur ;
- absence de duplicata exact des documents élève ;
- conception générale du plan quatre semaines pertinente.

Le projet mérite donc une **passe corrective ciblée**, pas une reconstruction complète.

## 16. Gates obligatoires avant distribution

### Gate A — scientifique

La contre-revue indépendante a ramené les 180 occurrences d’items à **100 couples énoncé/réponse uniques** : **88 PASS, 8 WARN, 4 FAIL**. Le détail figure dans `SCIENTIFIC_ITEM_AUDIT_S5.md`.

- [ ] Corriger les quatre FAIL et les huit WARN de la revue d’items, ainsi que les défauts de phase 4 listés au §8.
- [ ] Régénérer les documents dépendants.
- [ ] Refaire la revue des 100 items après correction.
- [ ] Vérifier qu'aucune méthode valide n'est pénalisée à tort.

### Gate B — temps

- [ ] Supprimer l'écrasement artificiel des durées.
- [ ] Recalibrer les 15 évaluations.
- [ ] Ramener la NSI à une charge réelle compatible 45 min.
- [ ] Prévoir 3–5 min de marge raisonnable.

### Gate C — mesure de progression

- [ ] `mastery_delta = null` sans mesure initiale nominative appariée.
- [ ] Supprimer les formulations de progression chiffrée non défendables.
- [ ] Ajouter le contexte de remédiation immédiate/retention.
- [ ] Passer au scoring par critères.

### Gate D — données

- [ ] Mettre schéma et sortie analyseur en conformité.
- [ ] Tester les sorties avec `jsonschema`.
- [ ] Remplacer `measurement_reliability` par une force de preuve plus rigoureuse.

### Gate E — programmes

- [ ] Ajouter les références BO/NOR/année d'effet aux blueprints.
- [ ] Vérifier les transitions réglementaires 2026 pour chaque niveau.

### Gate F — sécurité / release

- [ ] Sandbox réelle pour le code NSI ou désactivation de l'exécution automatique.
- [ ] Retirer `.pyc`/`__pycache__`.
- [ ] Créer un paquet `release` propre et un paquet `audit` séparé.
- [ ] Créer le manifeste canonique de distribution.
- [ ] Refaire tous les tests après corrections.

## 17. Verdict par axe

| Axe | Verdict indépendant |
|---|---|
| Sécurité de l'archive | PASS |
| Compilation LaTeX | PASS |
| Qualité visuelle PDF | PASS |
| Organisation des livrables | PASS WITH MINOR CLEANUP |
| Reproductibilité standalone | WARNING |
| Exactitude scientifique | FAIL UNTIL CORRECTED |
| Faisabilité 45 min | FAIL, surtout NSI |
| Mesure de progression | FAIL |
| Scoring par compétences | FAIL / modèle à corriger |
| Schémas de données | FAIL (incompatibilité) |
| Alignement réglementaire explicite | WARNING / à documenter |
| Sécurité exécution NSI | FAIL si code non fiable exécuté |
| **Release élèves** | **HOLD** |

## 18. Critère de sortie de HOLD

La livraison pourra être considérée comme distribuable lorsque :

1. tous les blockers ci-dessus sont corrigés ;
2. les 45 PDF recompilent ;
3. les 15 sujets sont recalibrés sans durée imposée artificiellement ;
4. toutes les sorties JSON passent leur schéma ;
5. aucune progression numérique n'est produite sans mesure initiale réelle ;
6. le runner NSI est sandboxé ou désactivé ;
7. les corrections scientifiques sont intégrées ;
8. un nouveau QA indépendant ne présente aucun FAIL critique.
