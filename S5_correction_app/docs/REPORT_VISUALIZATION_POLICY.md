# Politique de visualisation des bilans

Ce document répond à une seule question, et il faut pouvoir y répondre avant
d'écrire une ligne de code : **ce graphique dit-il quelque chose de vrai ?**

## Le critère

Une représentation graphique n'est légitime que si les quatre conditions sont
réunies :

1. les données représentées sont **quantitatives** ;
2. le **dénominateur est connu** et affiché ;
3. les catégories comparées sont **réellement comparables** ;
4. la représentation ne suggère **aucune précision** que les données n'ont pas.

Si l'une manque, un tableau ou une phrase dit la même chose sans mentir. Un
graphique n'est jamais ajouté pour rendre un document plus agréable : dans un
bilan pédagogique, l'agrément obtenu au prix d'une fausse impression se paie par
une décision familiale mal fondée.

## Décisions

### Frise de progression S1 → S5 — **REFUSÉE**

*Objectif envisagé* : montrer le chemin parcouru pendant le stage.
*Données* : les thèmes des cinq séances et les compétences ciblées.
*Bénéfice* : une lecture immédiate du parcours.
*Risque* : une courbe montante entre S1 et S5 serait lue comme une mesure de
progression. Or aucune mesure comparable n'existe entre les séances : les
tableaux d'observation ne sont pas renseignés, et le diagnostic initial est
qualitatif. La courbe serait entièrement inventée.
**Décision : ne pas utiliser.** Le parcours est rendu par un tableau
chronologique — séance, axe principal, objectif personnalisé — qui dit ce qui a
été proposé sans prétendre mesurer un progrès.

### Radar de compétences — **REFUSÉ**

*Risque* : un radar suppose des axes comparables et une échelle commune. Nos
compétences n'ont ni le même nombre de critères, ni le même poids, ni la même
importance pour l'année suivante. Une compétence évaluée par un seul critère y
occuperait la même surface qu'une compétence évaluée par quatre.
**Décision : ne pas utiliser.** Jamais, quelle que soit la demande.

### Barres horizontales par domaine — **REFUSÉES pour le bilan parents**

*Objectif envisagé* : points obtenus sur points disponibles, domaine par domaine.
*Données* : quantitatives, dénominateur connu — les deux premières conditions
sont réunies.
*Risque* : la troisième ne l'est pas. Un domaine évalué par un seul critère à
0,5 point produirait une barre à 0 % visuellement identique à un domaine évalué
par six critères. La barre suggère une solidité de mesure que le nombre de
critères ne soutient pas. C'est précisément l'erreur que la notion de force de
preuve existe pour empêcher.
**Décision : ne pas utiliser.** Le tableau par domaines porte la même
information, avec l'état observé écrit en toutes lettres et la mention explicite
des compétences que le sujet ne mesure pas.

### Jauge circulaire du score — **REFUSÉE**

*Risque* : elle donnerait au score brut la place dominante que le §16 lui refuse
explicitement. Le score brut agrège des prérequis et des découvertes ; en faire
l'image centrale du document contredit tout le reste.
**Décision : ne pas utiliser.**

### Profil des types d'erreurs — **ACCEPTÉ, réservé à la synthèse enseignant**

*Objectif* : voir d'un coup d'œil si les erreurs restantes sont surtout de
calcul, de méthode ou de concept.
*Données* : un comptage d'occurrences par code d'erreur. Quantitatif, dénominateur
connu, catégories comparables entre elles.
*Risque* : faible pour un enseignant, qui sait qu'un comptage sur une copie de
quarante-cinq minutes n'est pas un profil psychologique. Réel pour une famille,
qui pourrait y lire un trait de caractère.
**Décision : tableau de comptage dans la synthèse enseignant uniquement.** Il y
figure déjà. Aucune représentation dans le bilan parents, où l'interprétation est
donnée en une phrase — « les erreurs restantes sont principalement des erreurs de
calcul, alors que les méthodes sont généralement identifiées » — qui est plus
utile qu'un histogramme.

### Couverture du stage — **ACCEPTÉE en colonne de tableau, jamais en graphique**

*Risque* : représenter couverture et maîtrise sur une même échelle inviterait à
les additionner ou à les comparer. Ce sont deux grandeurs de nature différente :
l'une décrit le travail proposé, l'autre ce que l'évaluation établit.
**Décision : deux colonnes distinctes dans le tableau par domaines**, avec une
note rappelant qu'elles ne se déduisent pas l'une de l'autre.

## Si une proportion doit être affichée

Ne jamais écrire un pourcentage seul. Toujours donner le compte qui le produit :

> Sur la part du sujet consacrée aux acquis de l'année précédente, 14,5 points
> sur 17,5 sont obtenus, soit 83 %.

Le pourcentage est arrondi à l'unité dans le document destiné aux familles. La
précision décimale y suggérerait une exactitude que quarante-cinq minutes
d'évaluation ne portent pas. La synthèse enseignant peut conserver la précision
technique lorsqu'elle sert au diagnostic.

## Ce qui est interdit sans discussion

* percentile, rang, classement entre élèves ;
* moyenne de groupe dans un document individuel ;
* « score de progression » sous quelque forme que ce soit ;
* toute échelle temporelle suggérant une mesure répétée qui n'a pas eu lieu.

## Pour un futur développeur

Avant d'ajouter une visualisation, écrire les quatre réponses — objectif, données,
bénéfice, risque d'interprétation — puis la décision. Si l'une des quatre
conditions manque, la réponse est un tableau.
