# Plan des quatre premières semaines — règles

## Quatre partis pris

1. **Peu d'objectifs.** Deux par semaine, trois la dernière. Un plan qui liste huit
   priorités n'est pas suivi.
2. **Une charge réaliste.** Quinze à vingt-cinq minutes, deux à quatre fois par
   semaine. Jamais « une heure de mathématiques par jour » : l'élève reprend une
   scolarité complète.
3. **Un seuil vérifiable.** « Travailler les fractions » n'est pas un objectif.
   « Réussir 5 soustractions de fractions sur 6 sans aide » en est un : la famille
   peut le constater elle-même.
4. **Les passerelles ne sont pas des priorités.** Une notion découverte le jour de
   l'évaluation ne devient pas un travail de rattrapage.

## Ce que fait chaque semaine

| semaine | intention | contenu |
| --- | --- | --- |
| 1 | stabiliser | les prérequis les plus critiques, 3 × 15 min |
| 2 | vérifier à distance | **mini-tests différés** sur les réussites obtenues juste après remédiation, 3 × 15 min |
| 3 | transférer | deux compétences mêlées dans un même problème, 2 × 20 min |
| 4 | faire le point | bilan cumulatif court, et **réévaluation des P1 et P2**, 2 × 20 min |

La semaine 2 est structurellement réservée à la rétention. Toute compétence dont
`retention_status = not_yet_verified` y est revérifiée, sans révision le jour même :
c'est la seule façon de distinguer une réussite installée d'un effet de récence.

## Priorisation

`priority_rank` ∈ {P1, P2, P3, OK} est calculé par le moteur d'analyse à partir du
statut final et de l'importance pour l'année à venir. Le plan applique ensuite son
propre plafond : **deux P1 au maximum**. Les suivantes deviennent P2, restent au
plan, et le motif de la rétrogradation est enregistré.

Le moteur d'analyse partagé tolère davantage de P1 — il décrit l'état des
compétences, sans se soucier de ce qu'une famille peut tenir. Le plafond appartient
au plan, pas au moteur.

## Seuils par domaine

| domaine | travail | seuil |
| --- | --- | --- |
| Nombres relatifs | 4 sommes ou différences, 2 placements sur droite graduée | 5 sur 6 sans aide |
| Fractions | 4 soustractions à dénominateurs différents, 2 problèmes | 5 sur 6 sans aide |
| Calcul littéral | 4 développements k(a − b), 2 réductions signées | 5 sur 6, signes compris |
| Géométrie | 3 raisonnements donnée–propriété–conclusion | 3 sur 4 sans hypothèse ajoutée |
| Grandeurs et mesures | 3 aires ou périmètres, figures composées | 3 sur 4, unités écrites |
| Proportionnalité | 3 quatrièmes proportionnelles dont un pourcentage | 3 sur 4 sans aide |
| Statistiques | 2 moyennes suivies d'un contrôle de vraisemblance | 3 sur 4 |

## Mode entretien

Si l'évaluation ne dégage aucune priorité de consolidation, le plan bascule en
entretien et le dit : les objectifs portent alors sur les compétences les plus
sollicitées en début d'année, et sur les notions de l'année à venir. Un élève qui
réussit tout n'a pas besoin d'un plan de rattrapage, mais il a besoin d'un plan.

## Aucune recommandation commerciale

Une proposition de suivi doit être pédagogiquement justifiée et écrite par
l'enseignant. Le générateur n'en produit jamais ; la phrase « est indispensable »
est refusée par le contrôle de langue.
