# Terminale Spécialité Mathématiques — Séance 3 — Fiche professeur
## Second degré : discriminant, signe du trinôme, tableau de signes

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_maths.md`

## Pourquoi cette séance

Le second degré est réussi à 76,2 % en moyenne, mais il porte **trois certitudes erronées**
et un item resté sans réponse. L'erreur n'est pas sur le discriminant : elle est sur le
**signe du trinôme**, où la règle « du signe de a à l'extérieur des racines » est appliquée
sans regarder le signe de a.

Cette séance précède volontairement la séance sur la dérivation : le tableau de signes d'un
trinôme est exactement l'outil dont on aura besoin le lendemain pour lire le signe de f'.

## Objectifs de la séance

1. Résoudre une équation du second degré et contrôler par la somme et le produit des
   racines.
2. Dresser un tableau de signes complet, en tenant compte du signe du coefficient dominant.
3. Résoudre une inéquation du second degré à partir de ce tableau et en écrire correctement
   l'ensemble solution.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Contrôle sur la séance 2 : simplifier $e^{4x}/e^{x+2}$ | Répond, déclare sa certitude |
| 20 min | Confrontation | « Sur quel intervalle $- x^2 + 3x - 2$ est-il strictement positif ? » | Répond, puis teste en $x = 0$ et $x = 1{,}5$ |
| 25 min | Reconstruction | Discriminant, racines, factorisation ; règle du signe de a ; tableau de signes | Prend la trace écrite |
| 30 min | Entraînement différencié | Aiguille chaque élève sur sa piste | Traite son parcours |
| 20 min | Ouverture Terminale | Le tableau de signes d'une dérivée ; mention du théorème des valeurs intermédiaires | Observe, note |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

1. Écrire : « Sur quel intervalle le trinôme $- x^2 + 3x - 2$ est-il strictement positif ? »
   Recueillir les réponses écrites et les certitudes, sans commenter.
2. La réponse fausse attendue est « à l'extérieur des racines », soit
   $] - \infty ; 1[ \cup ]2 ; + \infty [$ — le réflexe pris avec des trinômes à coefficient dominant positif.
3. Faire **tester deux valeurs** :
   - en $x = 0$ : $- 0 + 0 - 2 = - 2$, négatif ;
   - en $x = 1{,}5$ : $- 2{,}25 + 4{,}5 - 2 = 0{,}25$, positif.
4. Faire verbaliser : la valeur 0 est à l'extérieur des racines et pourtant le trinôme y est
   négatif. La règle a été appliquée sans regarder le signe de a.
5. **Puis** reconstruire : le trinôme est du signe de a à l'extérieur des racines. Ici
   $a = - 1$ : à l'extérieur il est négatif, entre les racines il est positif.

## Reconstruction

**Résolution.** $\Delta = b^2 - 4$ac.

| Signe de $\Delta$ | Racines |
|---|---|
| $\Delta > 0$ | deux racines distinctes $( - b \pm \surd \Delta )/(2a)$ |
| $\Delta = 0$ | une racine double $- b/(2a)$ |
| $\Delta < 0$ | aucune racine réelle |

**Contrôle systématique** : somme des racines = $- b/a$, produit = c/a. Ce contrôle prend cinq
secondes et détecte la quasi-totalité des erreurs de calcul.

**Signe du trinôme.** Faire construire le tableau au tableau, avec les élèves :

| | $- \infty$ | | $x_1$ | | $x_2$ | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de ax^2+bx+c | | signe de a | 0 | signe de $- a$ | 0 | signe de a | |

Quand $\Delta < 0$, le trinôme garde le signe de a sur $\mathbb{R}$ tout entier — cas à traiter
explicitement, car il est souvent oublié.

**Écriture de l'ensemble solution.** Insister sur la réunion : pour $x^2 - 9 \geqslant 0$, l'ensemble
solution est $] - \infty ; - 3] \cup [3 ; + \infty [$, avec les crochets fermés puisque l'inégalité est large.

## Entraînement différencié

L'aiguillage suit les cinq postures de la carte maîtrise $\times$ confiance, et non un niveau
supposé. L'attribution se lit dans le livret individuel de chaque élève, rubrique « Ton
parcours, séance par séance » ; la fiche élève porte le même tableau, pour que l'élève sache
sans le demander ce qu'il a à faire.

| Piste | Posture au diagnostic | Support | Ce qu'on exige |
|---|---|---|---|
| Diagnostiquer | « Second degré » laissé sans réponse | Question 0, puis exercices 1 et 2 | Une réponse écrite, quelle que soit la certitude déclarée |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 sur le second degré | Question 0, puis exercices 1 à 4, exemple résolu fourni | L'élève écrit ce qu'il croyait avant d'écrire la règle |
| Installer | Réponse fausse avec une certitude basse | Exercices 1 à 4, exemple résolu fourni | La propriété écrite avant chaque calcul |
| Consolider | Réussite hésitante | Exercices 3 à 6, sans exemple résolu | Justification écrite, sans carte d'aide |
| Entretenir | Domaine acquis et assumé | Exercices 6 à 8, dont une discussion selon un paramètre | La démonstration rédigée en entier |
| Excellence | Aucun domaine à reprendre dans tout le bilan | Exercices 9 et 10, puis rôle de vérificateur | Une rédaction complète, puis la relecture d'une copie sans en donner la réponse |

**Le rôle de vérificateur.** Confier à l'élève de la piste excellence, une fois ses exercices
rendus, la copie d'un camarade. Sa tâche n'est pas de corriger : il indique si la propriété a
été écrite avant le calcul, si la conclusion répond à la question posée, et où le raisonnement
s'interrompt. Ne jamais lui confier l'explication d'une notion à un camarade porteur d'une
certitude erronée : la confrontation demande un pilotage que seul l'enseignant peut assurer.

## Ouverture sur la Terminale — 20 minutes

Écrire : soit $f(x) = x^3 - 3x^2 + 1$. Faire calculer $f'(x) = 3x^2 - 6x = 3x(x - 2)$.

Faire remarquer : **f' est un trinôme**. Dresser son tableau de signes exactement comme
depuis le début de la séance. En déduire les variations de f — sans les démontrer, elles
seront reprises en séance 4.

Puis annoncer le prolongement de Terminale :

> En Terminale, on dérivera une deuxième fois : f''$(x) = 6x - 6$. Le signe de f'' donne les
> variations de f', donc la **convexité** de f. Le tableau de signes que vous savez faire
> aujourd'hui servira deux fois par exercice.

Mentionner enfin le **théorème des valeurs intermédiaires** : si f est continue et
strictement monotone sur un intervalle, et change de signe, l'équation $f(x) = 0$ y admet une
solution unique. Les variations en sont l'ingrédient. Ne pas aller plus loin.

## Corrigé du parcours excellence

**Exercice 9.**
a) $P(2) = 16 - 12 - 6 + 2 = 0$.
b) Par identification ou division : $a = 2$, $b = 1$, $c = - 1$, soit
$P(x) = (x - 2)(2x^2 + x - 1)$.
c) $\Delta = 1 + 8 = 9$, donc $x = ( - 1 - 3)/4 = - 1$ ou $x = ( - 1 + 3)/4 = 1/2$.
d) Solutions de $P(x) = 0$ : $\{ - 1 ; 1/2 ; 2 \}$. Tableau de signes sur les quatre
intervalles délimités par ces trois racines : P est négatif sur $] - \infty ; - 1]$, positif
sur $[ - 1 ; 1/2]$, négatif sur $[1/2 ; 2]$, positif sur $[2 ; + \infty[$. Le coefficient
dominant est 2, positif : le signe à l'extrême droite est positif, et alterne à chaque racine
simple.

**Exercice 10.**
a) La faille est le cas $m = 0$ : l'équation devient $- 4x + 1 = 0$, du premier degré. Elle
n'a pas de discriminant, et admet une unique solution. Parler de discriminant suppose
$m \neq 0$.
b) Si $m = 0$ : une solution, $x = 1/4$. Si $m \neq 0$ : $\Delta = 16 - 4m$, donc deux
solutions pour $m < 4$ (et $m \neq 0$), une solution double pour $m = 4$, aucune pour
$m > 4$.
c) Deux cas, de nature différente : $m = 0$ (équation du premier degré) et $m = 4$ (racine
double). C'est le point de l'exercice : reconnaître que l'unicité de la solution ne recouvre
pas le même phénomène dans les deux cas.

## Corrigé de l'ouverture maths expertes

a) $252 = 1 \times 198 + 54$ ; $198 = 3 \times 54 + 36$ ; $54 = 1 \times 36 + 18$ ;
$36 = 2 \times 18 + 0$. Le dernier reste non nul vaut 18, donc le PGCD vaut **18**.
b) $252/198 = 14/11$.
c) Non, 252 et 198 ont 18 pour PGCD. Oui pour 14 et 11 : leur PGCD vaut 1, c'est précisément
ce que signifie « fraction irréductible ».

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Règle du signe appliquée sans regarder a | Faire tester une valeur à l'extérieur des racines |
| Cas $\Delta < 0$ oublié | Faire chercher le signe de $2x^2 + x + 3$ sur $\mathbb{R}$ |
| Solutions d'équation confondues avec ensemble solution d'inéquation | Faire écrire les deux pour le même trinôme |
| Réunion oubliée dans l'ensemble solution | Faire placer les intervalles sur une droite graduée |
| $\Delta = b^2 + 4$ac | Faire réécrire la formule avant chaque calcul |

## Indicateurs de fin de séance

- L'élève écrit le signe de a avant de remplir son tableau de signes.
- L'élève contrôle ses racines par la somme et le produit.
- L'élève écrit un ensemble solution avec le bon type de crochets.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
