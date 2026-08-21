# Gabarit du bilan parents — V3

Le bilan répond aux données. Jamais l'inverse. Chaque phrase chiffrée doit renvoyer à une
clé de `analysis/<élève>/bilan_facts_v3.json` ; toute affirmation quantitative produite
autrement est à retirer.

Le score sur 20 n'est **pas** le titre du bilan. S'il est communiqué, il l'est sous son
nom : *score brut au sujet de clôture*, assorti de la précision que le sujet contenait
aussi des éléments de passerelle vers l'année suivante. Le diagnostic principal est
compétence par compétence.

## Les neuf sections, et la clé qui les alimente

| # | section | source dans `bilan_facts_v3.json` |
| --- | --- | --- |
| 1 | Situation de départ documentée | `comparaison_initiale_qualitative[]` — statuts qualitatifs de domaine, jamais des notes |
| 2 | Travail réalisé pendant le stage | livret de la séance et modules travaillés en phases 2 et 3 |
| 3 | Acquis N−1 actuellement observés | `acquis_n_minus_1_observes[]` |
| 4 | Points N−1 à consolider | `points_n_minus_1_a_consolider[]` |
| 5 | Premières passerelles vers l'année N | `premieres_passerelles[]`, avec `phrase_autorisee` |
| 6 | Réussites immédiates à confirmer dans la durée | `reussites_immediates_a_confirmer[]` |
| 7 | Plan des quatre premières semaines | `four_week_action_plan_v3.json`, section `consolidation_n_minus_1` |
| 8 | Mini-test différé, si nécessaire | `controle_differe` |
| 9 | Recommandation de suivi | à écrire à partir des sections 3 à 8, jamais à partir de la seule note |

Le score brut, s'il figure, se place en annexe ou en fin de section 3, sous
`raw_assessment_score`, avec son avertissement.

## Ce qui peut s'écrire

> « Le calcul sur les fractions est actuellement réussi sur deux critères distincts ;
> cette réussite reste à confirmer dans la durée car la notion a été retravaillée
> immédiatement avant l'évaluation. »

> « La recherche séquentielle a été abordée comme première passerelle vers la Première
> NSI. Le résultat de cette question ne constitue donc pas un jugement sur les acquis
> antérieurs de l'élève. »

> « Le diagnostic initial signalait une fragilité en calcul littéral. L'évaluation finale
> apporte aujourd'hui plusieurs éléments positifs sur ce domaine, sans permettre de
> calculer une progression chiffrée faute de réponses initiales item par item. »

> « Cette notion, nouvellement introduite, sera reprise pendant la rentrée. »

## Ce qui ne peut pas s'écrire

| interdit | pourquoi |
| --- | --- |
| « progression de 40 % » | aucune mesure initiale appariée : l'écart n'existe pas |
| « a progressé de deux niveaux » | les niveaux de maîtrise initiaux n'ont jamais été mesurés |
| « maîtrise désormais » sur une preuve faible | un critère isolé ne fonde pas une maîtrise |
| « non acquis » sur une notion de passerelle | elle n'a pas encore été enseignée |
| « lacune » sur une notion jamais enseignée | même raison |
| « consolidation durable » après remédiation immédiate | la rétention n'a pas encore été vérifiée |
| « niveau insuffisant » sur la seule note brute | douze items ne mesurent pas une année |

## Contrôle avant envoi

```bash
python3 tools/check_bilan_language.py \
    --bilan reports/bilan_<élève>.md \
    --facts analysis/<élève>/bilan_facts_v3.json \
    --analysis analysis/<élève>/post_stage_analysis_v3.json
```

Le contrôleur signale la phrase et la règle enfreinte. Il ne réécrit rien : c'est à
l'auteur de reformuler, ou d'assumer et de documenter l'écart.

## Une note sur le ton

Un bilan prudent n'est pas un bilan tiède. Dire « réussi sur deux critères distincts,
à confirmer dans la durée » est plus informatif, et plus utile à une famille, que
« maîtrise acquise ». La prudence porte sur ce qu'on affirme, pas sur ce qu'on constate.
