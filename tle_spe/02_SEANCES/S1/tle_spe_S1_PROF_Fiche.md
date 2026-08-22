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

1. Rétablir la méthode du signe de $u_{n+1} - u_n$ pour une suite définie par récurrence.
2. Rétablir la comparaison de la raison **à 1** pour une suite géométrique de premier terme
   positif.
3. Calculer un terme quelconque à partir de la formule explicite d'une suite arithmétique
   ou géométrique.
4. Faire apparaître le besoin de la récurrence, sans la traiter.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Distribue les livrets individuels ; explique la carte maîtrise $\times$ confiance | Lit sa carte, repère son domaine prioritaire |
| 20 min | Confrontation | Pose la question : « La suite $u_n = 0{,}5^n$ est-elle croissante ou décroissante ? » Recueille les réponses **avant** tout commentaire | Répond, puis calcule $u_0$, $u_1$, $u_2$, $u_3$ et confronte |
| 25 min | Reconstruction | Établit les deux méthodes ; démontre le cas géométrique | Prend la trace écrite, reformule à l'oral |
| 30 min | Entraînement différencié | Aiguille chaque élève sur sa piste ; circule ; note les aides utilisées | Traite son parcours, note l'aide utilisée |
| 20 min | Ouverture Terminale | Pose : « Une suite croissante peut-elle rester bornée ? » ; montre l'exemple $u_n = 3 - 1/(n+1)$ | Observe, conjecture, note l'ouverture |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse et l'auto-évaluation | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

Le point décisif est de **faire produire la réponse fausse avant de la corriger**.

1. Poser la question sans support : « $(u_n)$ définie par $u_n = 0{,}5^n$. Croissante ou
   décroissante ? Notez votre réponse et votre certitude. »
2. Recueillir les réponses par écrit, sans commenter. Plusieurs élèves répondront
   « croissante », en invoquant une raison positive.
3. Faire calculer $u_0 = 1 ; u_1 = 0{,}5 ; u_2 = 0{,}25 ; u_3 = 0{,}125$.
4. Faire verbaliser la contradiction : « la raison est positive » n'est pas le bon critère.
5. **Seulement à ce stade**, établir la règle : pour un premier terme positif, on compare
   la raison à 1.

Si aucun élève ne produit l'erreur, ne pas la fabriquer : passer directement à la
reconstruction et consacrer le temps gagné au parcours d'approfondissement.

## Reconstruction — les deux méthodes

**Méthode générale, valable pour toute suite.** On étudie le signe de $u_{n+1} - u_n$.

- Si $u_{n+1} - u_n \geqslant 0$ pour tout n, la suite est croissante.
- Si $u_{n+1} - u_n \leqslant 0$ pour tout n, la suite est décroissante.

C'est la seule méthode utilisable pour une suite définie par récurrence.

**Cas particulier d'une suite géométrique** de premier terme $v_0 > 0$ et de raison $q > 0$ :

| Raison | Sens de variation |
|---|---|
| $q > 1$ | croissante |
| $q = 1$ | constante |
| $0 < q < 1$ | décroissante |

*Démonstration à conduire au tableau, en trois lignes :* $v_{n+1} - v_n = v_0q^n(q - 1)$. Comme
$v_0 > 0$ et $q^n > 0$, le signe de la différence est celui de $q - 1$. La comparaison porte donc
bien sur $q - 1$, c'est-à-dire sur la position de q par rapport à 1.

## Entraînement différencié

L'aiguillage suit les cinq postures de la carte maîtrise $\times$ confiance, et non un niveau
supposé. L'attribution se lit dans le livret individuel de chaque élève, rubrique « Ton
parcours, séance par séance » ; la fiche élève porte le même tableau, pour que l'élève sache
sans le demander ce qu'il a à faire.

| Piste | Posture au diagnostic | Support | Ce qu'on exige |
|---|---|---|---|
| Diagnostiquer | « Suites numériques » laissé sans réponse | Question 0, puis exercices 1 et 2 | Une réponse écrite, quelle que soit la certitude déclarée |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 sur les suites | Question 0, puis exercices 1 à 4, exemple résolu fourni | L'élève écrit ce qu'il croyait avant d'écrire la règle |
| Installer | Réponse fausse avec une certitude basse | Exercices 1 à 4, exemple résolu fourni | La propriété écrite avant chaque calcul |
| Consolider | Réussite hésitante | Exercices 3 à 6, sans exemple résolu | Justification écrite, sans carte d'aide |
| Entretenir | Domaine acquis et assumé | Exercices 6 à 8, dont la démonstration du cas géométrique | La démonstration rédigée en entier |
| Excellence | Aucun domaine à reprendre dans tout le bilan | Exercices 9 et 10, puis rôle de vérificateur | Une rédaction complète, puis la relecture d'une copie sans en donner la réponse |

**Le rôle de vérificateur.** Confier à l'élève de la piste excellence, une fois ses exercices
rendus, la copie d'un camarade. Sa tâche n'est pas de corriger : il indique si la propriété a
été écrite avant le calcul, si la conclusion répond à la question posée, et où le raisonnement
s'interrompt. Ne jamais lui confier l'explication d'une notion à un camarade porteur d'une
certitude erronée : la confrontation demande un pilotage que seul l'enseignant peut assurer.

## Ouverture sur la Terminale — 20 minutes

Poser la question : « Une suite croissante peut-elle rester bornée ? »

Proposer $u_n = 3 - 1/(n+1)$. Faire calculer les premiers termes : 2 ; 2,5 ; 2,666… ; 2,75.
Faire constater que la suite croît et ne dépasse jamais 3.

Énoncer, sans démonstration : **une suite croissante et majorée converge**. Préciser que
la Terminale démontrera qu'une suite est majorée par un raisonnement par récurrence, et
que ce raisonnement est le premier chapitre de l'année.

Écrire au tableau le principe, sans l'utiliser :

> Pour démontrer qu'une propriété $P(n)$ est vraie pour tout entier n : on vérifie $P(0)$, puis
> on démontre que si $P(n)$ est vraie alors $P(n+1)$ l'est. On conclut que $P(n)$ est vraie pour
> tout n.

Ne pas faire de démonstration par récurrence pendant le stage : l'objectif est de rendre
lisible ce à quoi le sens de variation va servir, pas d'anticiper le programme.

## Corrigé du parcours excellence

**Exercice 9.**
a) $u_1 = 1/2$, $u_2 = 1/3$, $u_3 = 1/4$. Conjecture : $u_n = 1/(n + 1)$.
b) $u_{n+1} - u_n = u_n/(1 + u_n) - u_n = - u_n^2/(1 + u_n)$. Le numérateur est négatif ou
nul, le dénominateur strictement positif puisque $u_n > 0$ : la différence est strictement
négative, la suite est strictement décroissante.
c) $v_n = 1/u_n$ donne $v_{n+1} = (1 + u_n)/u_n = 1 + v_n$. La suite $(v_n)$ est donc
arithmétique de raison 1 et de premier terme $v_0 = 1$, d'où $v_n = n + 1$ et
$u_n = 1/(n + 1)$ : la conjecture est démontrée.
d) Non : $1/(n+1)$ est strictement positif pour tout entier naturel n. La suite décroît sans
jamais s'annuler — c'est exactement la situation « décroissante et minorée » que la Terminale
reliera à la convergence.

**Exercice 10.**
a) $u_n = 1/(n+1)$, ou $u_n = 2 + 0{,}5^n$ : décroissantes, toujours strictement positives.
b) « Une suite décroissante et **minorée par un réel positif** reste positive. » Accepter
toute formulation correcte d'une minoration.
c) Fausse. Contre-exemple : $u_n = n$ reste positive et croît. Attendre que l'élève dise
qu'un seul contre-exemple suffit à réfuter une proposition universelle.

## Corrigé de l'ouverture maths expertes

a) $47 = 6 \times 7 + 5$, avec $0 \leqslant 5 < 6$.
b) $u_0 = 3$, $u_1 = 7$, $u_2 = 11$, $u_3 = 15$ ; les divisions par 4 donnent
$3 = 4 \times 0 + 3$, $7 = 4 \times 1 + 3$, $11 = 4 \times 2 + 3$, $15 = 4 \times 3 + 3$.
Le reste vaut toujours 3.
c) $u_n = 4n + 3$ est déjà l'écriture de la division euclidienne de $u_n$ par 4, puisque
$0 \leqslant 3 < 4$. Par unicité du couple quotient-reste, le reste vaut 3, jamais 0 : aucun
terme n'est divisible par 4. **Exiger l'argument d'unicité** — c'est lui qui fait la
démonstration, pas le tableau de valeurs.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| « La raison est positive donc la suite croît » | Faire calculer les premiers termes ; faire écrire $v_{n+1} - v_n = v_0q^n(q - 1)$ |
| Sens de variation annoncé sans calcul de la différence | Refuser la conclusion tant que la différence n'est pas écrite |
| $u_{n+1}$ confondu avec $u_n + 1$ | Faire écrire les deux expressions côte à côte sur un exemple |
| Formule explicite et relation de récurrence confondues | Faire produire les deux écritures pour la même suite |
| $v_n = v_0 \times n \times r$ au lieu de $v_0 \times r^n$ | Faire calculer $v_2$ par les deux formules et comparer |

## Indicateurs de fin de séance

- L'élève écrit la différence $u_{n+1} - u_n$ sans qu'on le lui demande.
- L'élève compare la raison à 1 et le dit à voix haute.
- L'élève déclare une certitude cohérente avec sa réussite effective.
- L'aide maximale utilisée est notée dans le livret.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
