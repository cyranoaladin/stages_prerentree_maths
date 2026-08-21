# Terminale Spécialité Mathématiques — Séance 1 — Fiche professeur
## Suites numériques : du sens de variation à la récurrence

**Durée :** 2 heures · **Effectif :** 8 élèves (2 groupes réunis) · **Source pédagogique :** `stage_prerentree_terminale_maths.md`

## Pourquoi cette séance en premier

Les suites numériques concentrent le plus grand nombre de certitudes erronées du groupe :
**quatre élèves sur sept** ont donné une réponse fausse avec une certitude de 3 ou 4 sur 4.
La réussite moyenne du domaine est de 63,3 %.

C'est aussi le domaine dont la Terminale a le besoin le plus immédiat : le raisonnement par
récurrence et l'étude des limites de suites ouvrent l'année. Une suite dont on ne sait pas
établir le sens de variation ne peut être ni majorée par récurrence, ni déclarée convergente.

## Objectifs de la séance

1. Rétablir la méthode du signe de u(n+1) − u(n) pour une suite définie par récurrence.
2. Rétablir la comparaison de la raison **à 1** pour une suite géométrique de premier terme
   positif.
3. Calculer un terme quelconque à partir de la formule explicite d'une suite arithmétique
   ou géométrique.
4. Faire apparaître le besoin de la récurrence, sans la traiter.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Distribue les livrets individuels ; explique la carte maîtrise × confiance | Lit sa carte, repère son domaine prioritaire |
| 20 min | Confrontation | Pose la question : « La suite u(n) = 0,5^n est-elle croissante ou décroissante ? » Recueille les réponses **avant** tout commentaire | Répond, puis calcule u₀, u₁, u₂, u₃ et confronte |
| 25 min | Reconstruction | Établit les deux méthodes ; démontre le cas géométrique | Prend la trace écrite, reformule à l'oral |
| 30 min | Entraînement différencié | Distribue les trois parcours ; circule ; note les aides utilisées | Traite son parcours, note l'aide utilisée |
| 20 min | Ouverture Terminale | Pose : « Une suite croissante peut-elle rester bornée ? » ; montre l'exemple u(n) = 3 − 1/(n+1) | Observe, conjecture, note l'ouverture |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse et l'auto-évaluation | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

Le point décisif est de **faire produire la réponse fausse avant de la corriger**.

1. Poser la question sans support : « (u_n) définie par u(n) = 0,5^n. Croissante ou
   décroissante ? Notez votre réponse et votre certitude. »
2. Recueillir les réponses par écrit, sans commenter. Plusieurs élèves répondront
   « croissante », en invoquant une raison positive.
3. Faire calculer u₀ = 1 ; u₁ = 0,5 ; u₂ = 0,25 ; u₃ = 0,125.
4. Faire verbaliser la contradiction : « la raison est positive » n'est pas le bon critère.
5. **Seulement à ce stade**, établir la règle : pour un premier terme positif, on compare
   la raison à 1.

Si aucun élève ne produit l'erreur, ne pas la fabriquer : passer directement à la
reconstruction et consacrer le temps gagné au parcours d'approfondissement.

## Reconstruction — les deux méthodes

**Méthode générale, valable pour toute suite.** On étudie le signe de u(n+1) − u(n).

- Si u(n+1) − u(n) ≥ 0 pour tout n, la suite est croissante.
- Si u(n+1) − u(n) ≤ 0 pour tout n, la suite est décroissante.

C'est la seule méthode utilisable pour une suite définie par récurrence.

**Cas particulier d'une suite géométrique** de premier terme v₀ > 0 et de raison q > 0 :

| Raison | Sens de variation |
|---|---|
| q > 1 | croissante |
| q = 1 | constante |
| 0 < q < 1 | décroissante |

*Démonstration à conduire au tableau, en trois lignes :* v(n+1) − v(n) = v₀q^n(q − 1). Comme
v₀ > 0 et q^n > 0, le signe de la différence est celui de q − 1. La comparaison porte donc
bien sur q − 1, c'est-à-dire sur la position de q par rapport à 1.

## Entraînement différencié

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Ceux dont le livret porte « Suites numériques » en priorité 1 ou 2 | Exercices 1 à 4 de la fiche élève, avec exemple résolu |
| Maîtrise | Ceux dont les suites sont réussies mais hésitantes | Exercices 3 à 6, justification écrite exigée |
| Approfondissement | Ceux dont les suites sont acquises avec certitude | Exercices 6 à 8, dont la démonstration du cas géométrique |

L'attribution se lit dans le livret individuel de chaque élève, rubrique « Parcours
personnalisé séance par séance ».

## Ouverture sur la Terminale — 20 minutes

Poser la question : « Une suite croissante peut-elle rester bornée ? »

Proposer u(n) = 3 − 1/(n+1). Faire calculer les premiers termes : 2 ; 2,5 ; 2,666… ; 2,75.
Faire constater que la suite croît et ne dépasse jamais 3.

Énoncer, sans démonstration : **une suite croissante et majorée converge**. Préciser que
la Terminale démontrera qu'une suite est majorée par un raisonnement par récurrence, et
que ce raisonnement est le premier chapitre de l'année.

Écrire au tableau le principe, sans l'utiliser :

> Pour démontrer qu'une propriété P(n) est vraie pour tout entier n : on vérifie P(0), puis
> on démontre que si P(n) est vraie alors P(n+1) l'est. On conclut que P(n) est vraie pour
> tout n.

Ne pas faire de démonstration par récurrence pendant le stage : l'objectif est de rendre
lisible ce à quoi le sens de variation va servir, pas d'anticiper le programme.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| « La raison est positive donc la suite croît » | Faire calculer les premiers termes ; faire écrire v(n+1) − v(n) = v₀q^n(q − 1) |
| Sens de variation annoncé sans calcul de la différence | Refuser la conclusion tant que la différence n'est pas écrite |
| u(n+1) confondu avec u(n) + 1 | Faire écrire les deux expressions côte à côte sur un exemple |
| Formule explicite et relation de récurrence confondues | Faire produire les deux écritures pour la même suite |
| v(n) = v₀ × n × r au lieu de v₀ × r^n | Faire calculer v₂ par les deux formules et comparer |

## Indicateurs de fin de séance

- L'élève écrit la différence u(n+1) − u(n) sans qu'on le lui demande.
- L'élève compare la raison à 1 et le dit à voix haute.
- L'élève déclare une certitude cohérente avec sa réussite effective.
- L'aide maximale utilisée est notée dans le livret.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
