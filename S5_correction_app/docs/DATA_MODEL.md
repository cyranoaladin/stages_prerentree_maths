# Modèle de données

## Trois décisions structurantes

### 1. Le nom n'est jamais une clé

Ahmad BELDI suit **deux** matières. Une table `person` porte l'être humain ; une table
`student` porte le couple personne × niveau × matière ; une table `assessment` porte
l'évaluation distribuée à ce couple.

```
person(person_id)  1 ── n  student(student_id)  1 ── n  assessment(assessment_id)
```

Constaté à l'import : **14 personnes, 15 couples**. Aucun écran, aucun export, aucun nom
de fichier ne se fie au nom seul : `output_basename` ajoute la matière lorsqu'une personne
en suit plusieurs.

### 2. Les points sont des entiers, en centièmes

Le barème réel emploie 0,3 / 0,4 / 0,6 / 0,7 : **ce ne sont pas des quarts de point**. Un
entier de quarts ne représenterait pas ce barème. Tous les montants sont en revanche des
multiples de 0,05.

Les points circulent donc en `Integer`, en centièmes, et ne redeviennent `Decimal` que
pour l'affichage ou l'export. Aucun flottant binaire n'entre dans un calcul de score.

```python
points.to_centi("0.7") == 70
points.format_fr(1450) == "14,5"
```

### 3. Rien n'est écrasé

Une correction validée puis rouverte crée une **révision** ; l'ancienne est conservée avec
son statut et sa raison de réouverture. Un rapport approuvé puis régénéré crée une
**version** ; l'ancienne reste approuvée. Un bloc de texte remplacé laisse son ancienne
version dans `report_block_history`.

## Les tables

| table | rôle |
| --- | --- |
| `app_meta` | `domain_schema_version`, `app_version`, `import_source_version` |
| `import_source` | chaque fichier V3 lu : chemin, empreinte, schéma, date |
| `person` | un être humain |
| `student` | un couple personne × niveau × matière |
| `assessment` | l'évaluation distribuée : chemins et empreintes des deux PDF, points disponibles par portée |
| `item_definition` | les 180 items : énoncé, points, réponse attendue, étapes, erreurs probables, sonde de certitude |
| `criterion_definition` | les 337 critères : points, compétence, alias analytique, portée, type de preuve, méthodes acceptées, limites, règles d'équité, rétention |
| `virtual_criterion_definition` | les 6 sous-critères analytiques des 3 critères mixtes |
| `skill_reference` | libellé, domaine, importance et portée d'une compétence d'analyse |
| `baseline_status` | diagnostic initial, qualitatif, par domaine — jamais converti en nombre |
| `delayed_check` | compétences à revérifier en semaine 2 |
| `correction` | révision, statut, durée observée, observations générales |
| `criterion_response` | **la ligne notée** : score, codes d'erreur, observation, méthode alternative, statut |
| `item_observation` | certitude et observation libre au niveau de l'item, jamais scorées |
| `analysis_snapshot` | l'analyse calculée, avec son empreinte |
| `report` | type, version, statut, chemins, empreinte du PDF, manifeste |
| `report_block` | un paragraphe, sa provenance et son approbation |
| `report_block_history` | ce qu'un bloc contenait avant d'être remplacé |
| `audit_event` | qui a fait quoi, quand, avant/après, et pourquoi |

## Ce qu'est une « ligne notée »

`criterion_response.scoring_id` vaut :

- le `criterion_id` pour un critère simple ;
- le `virtual_criterion_id` pour un sous-critère d'un critère mixte.

C'est ce grain qui est saisi, scoré et porteur des codes d'erreur. Pour les 15 évaluations,
cela fait **340 lignes notées** pour 337 critères imprimés — les trois critères mixtes se
notant chacun en deux sous-critères.

## Statuts

**Correction** : `DRAFT` → `REVIEW_READY` → `VALIDATED` → `REPORT_READY` →
`REPORT_APPROVED`. À partir de `VALIDATED`, toute modification exige une réouverture
motivée, qui crée une révision.

**Ligne notée** : `PENDING`, `SCORED`, `NOT_ANSWERED`, `UNCLASSIFIED`, `NEUTRALISED`.
Les deux derniers zéros ne portent aucun code d'erreur — on n'invente pas une cause.

**Rapport** : `DRAFT` → `GENERATED` → `APPROVED`.

## Versionnement

`app_meta.domain_schema_version` vaut la version du schéma métier. Une migration est
explicite : elle se demande, elle est précédée d'une sauvegarde automatique de la base, et
elle est journalisée. Aucune migration ne se déclenche à l'import d'un module.
