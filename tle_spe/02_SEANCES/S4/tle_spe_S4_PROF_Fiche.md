# Terminale Spécialité Mathématiques — Séance 4 — Fiche professeur
## Dérivation : du nombre dérivé aux variations, ouverture sur la convexité

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_maths.md`

## Pourquoi cette séance

La dérivation est le domaine le mieux réussi du groupe (81,8 %) mais c'est aussi celui qui
présente le profil le plus hétérogène : deux certitudes erronées, deux notions à installer,
une consolidation, deux acquis. Les formules sont connues ; c'est **l'interprétation** qui
manque.

L'erreur centrale est la confusion entre le signe de f' et le signe de f. En Terminale, la
convexité ajoute un troisième niveau : le signe de f'' donne les variations de f', qui
donnent la forme de la courbe de f. Un premier niveau instable rend le troisième
inaccessible.

Cette séance s'appuie directement sur le tableau de signes construit en séance 3.

## Objectifs de la séance

1. Distinguer explicitement le signe de f' et le signe de f.
2. Dériver un produit et un quotient sans erreur d'ordre.
3. Écrire l'équation d'une tangente.
4. Passer du tableau de signes de f' au tableau de variations de f.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Contrôle sur la séance 3 : signe de $- 3x^2 + 12$ | Répond, déclare sa certitude |
| 20 min | Confrontation | « $f' < 0$ sur ]1 ; 4[. Que peut-on affirmer ? » | Répond, puis examine le contre-exemple |
| 25 min | Reconstruction | Nombre dérivé et tangente ; formules ; du signe de f' aux variations de f | Prend la trace écrite |
| 30 min | Entraînement différencié | Aiguille chaque élève sur sa piste | Traite son parcours |
| 20 min | Ouverture Terminale | Dérivée seconde et convexité, sur un exemple | Observe, note |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

1. Écrire : « On sait que f' est strictement négative sur ]1 ; 4[. Que peut-on affirmer ? »
   Recueillir les réponses écrites et les certitudes.
2. La réponse fausse attendue est « f est strictement négative sur ]1 ; 4[ ».
3. Proposer le contre-exemple **$f(x) = x - 10$**… puis se raviser avec les élèves : sa
   dérivée vaut 1, elle est positive. Prendre **$f(x) = - x + 10$** : $f'(x) = - 1 < 0$, et
   pourtant $f(2) = 8 > 0$. La fonction décroît **et** reste positive.
4. Proposer ensuite **$g(x) = - x - 10$** : même dérivée, mais $g(2) = - 12 < 0$.
5. Faire verbaliser : deux fonctions ayant exactement la même dérivée ont des signes
   différents. Le signe de f' ne détermine donc pas le signe de f.
6. **Puis** reconstruire : le signe de f' donne le sens de variation, rien d'autre. Le signe
   de f se lit sur les valeurs de f, pas sur celles de f'.

*Variante graphique.* Tracer deux droites parallèles de pente $- 1$, l'une au-dessus, l'autre
au-dessous de l'axe des abscisses. Même pente, signes opposés : l'image est immédiate.

## Reconstruction

**Nombre dérivé.** $f'(a)$ est le coefficient directeur de la tangente à la courbe au point
d'abscisse a. Équation de cette tangente : **$y = f'(a)(x - a) + f(a)$**. Faire remarquer que
la formule contient à la fois $f'(a)$ et $f(a)$ : oublier $f(a)$ donne une droite parallèle à la
tangente, pas la tangente.

**Formules.**

| Opération | Dérivée |
|---|---|
| u + v | u' + v' |
| ku | ku' |
| uv | u'v + uv' |
| u/v | (u'$v -$ uv')$/v^2$ |

Insister sur l'ordre du numérateur de la dérivée d'un quotient : **u'v vient en premier**.
Faire écrire u, v, u', v' séparément avant d'appliquer la formule — c'est ce geste qui
supprime l'erreur d'ordre.

**Du signe de f' aux variations de f.** Reprendre le tableau de la séance 3 :

| | $- \infty$ | | 0 | | 2 | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de $f'(x)$ | | + | 0 | $-$ | 0 | + | |
| variations de f | | $\nearrow$ | | $\searrow$ | | $\nearrow$ | |

Faire énoncer par un élève : « f' positive, f croît ; f' négative, f décroît. Cela ne dit
rien du signe de f. »

## Entraînement différencié

L'aiguillage suit les cinq postures de la carte maîtrise $\times$ confiance, et non un niveau
supposé. L'attribution se lit dans le livret individuel de chaque élève, rubrique « Ton
parcours, séance par séance » ; la fiche élève porte le même tableau, pour que l'élève sache
sans le demander ce qu'il a à faire.

| Piste | Posture au diagnostic | Support | Ce qu'on exige |
|---|---|---|---|
| Diagnostiquer | « Dérivation » laissé sans réponse | Question 0, puis exercices 1 et 2 | Une réponse écrite, quelle que soit la certitude déclarée |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 sur la dérivation | Question 0, puis exercices 1 à 4, exemple résolu fourni | L'élève écrit ce qu'il croyait avant d'écrire la règle |
| Installer | Réponse fausse avec une certitude basse | Exercices 1 à 4, exemple résolu fourni | La propriété écrite avant chaque calcul |
| Consolider | Réussite hésitante | Exercices 3 à 6, sans exemple résolu | Justification écrite, sans carte d'aide |
| Entretenir | Domaine acquis et assumé | Exercices 6 à 8, dont une étude complète de fonction | La démonstration rédigée en entier |
| Excellence | Aucun domaine à reprendre dans tout le bilan | Exercices 9 et 10, puis rôle de vérificateur | Une rédaction complète, puis la relecture d'une copie sans en donner la réponse |

**Le rôle de vérificateur.** Confier à l'élève de la piste excellence, une fois ses exercices
rendus, la copie d'un camarade. Sa tâche n'est pas de corriger : il indique si la propriété a
été écrite avant le calcul, si la conclusion répond à la question posée, et où le raisonnement
s'interrompt. Ne jamais lui confier l'explication d'une notion à un camarade porteur d'une
certitude erronée : la confrontation demande un pilotage que seul l'enseignant peut assurer.

## Ouverture sur la Terminale — 20 minutes

Prendre $f(x) = x^3 - 3x^2$. Calculer $f'(x) = 3x^2 - 6x$, puis **f''$(x) = 6x - 6$**.

Faire dresser le tableau de signes de f'' : négatif avant 1, positif après.

Énoncer :

> Le signe de f'' donne les variations de f'. Là où f'' $\geqslant 0$, f' croît : la courbe de f
> tourne vers le haut, on dit que f est **convexe**. Là où f'' $\leqslant 0$, f est **concave**. Le
> point où f'' change de signe est un **point d'inflexion**.

Faire tracer, à main levée, l'allure de la courbe de f et repérer le point d'inflexion en
$x = 1$. Insister : c'est le même geste qu'aujourd'hui, appliqué une fois de plus.

Ne pas demander d'exercice de convexité pendant le stage.

## Corrigé du parcours excellence

**Exercice 9.**
a) $u = 2x$, $u' = 2$, $v = x^2 + 1$, $v' = 2x$, donc
$f'(x) = (2(x^2 + 1) - 2x \times 2x)/(x^2 + 1)^2 = (2 - 2x^2)/(x^2 + 1)^2 = 2(1 - x^2)/(x^2 + 1)^2$.
b) Le dénominateur est strictement positif : $f'(x)$ a le signe de $1 - x^2$, donc de
$(1 - x)(1 + x)$. f décroît sur $] - \infty ; - 1]$, croît sur $[ - 1 ; 1]$, décroît sur
$[1 ; + \infty[$. Minimum $f( - 1) = - 1$, maximum $f(1) = 1$.
c) Le tableau de variations donne directement l'encadrement : f atteint son minimum en $- 1$
et son maximum en 1 sur $\mathbb{R}$.
d) $f(0) = 0$ et $f'(0) = 2$ : la tangente a pour équation $y = 2x$.

**Exercice 10.**
a) $f(x) = x^3$ : $f'(0) = 0$ et pourtant f est strictement croissante sur $\mathbb{R}$, sans
extremum en 0. Exiger le calcul de $f'(x) = 3x^2$ et la remarque que $f'$ ne change pas de
signe.
b) Il faut que $f'$ **change de signe** en a. L'annulation seule ne suffit pas.
c) Sur $\mathbb{R}$, oui pour une fonction dérivable : en un extremum, la dérivée s'annule.
Sur $[0 ; 1]$, non : $f(x) = x$ atteint son minimum en 0 et son maximum en 1, alors que
$f'(x) = 1$ ne s'annule jamais. Le résultat ne vaut qu'aux points **intérieurs** à
l'intervalle — distinction que l'option exige et que la spécialité passe souvent sous silence.

## Corrigé de l'ouverture maths expertes

a) Contraposée : « si n est impair, alors $n^2$ est impair ».
b) Si n est impair, $n = 2k + 1$ avec k entier, donc
$n^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$, qui est impair. La contraposée étant vraie,
l'implication initiale l'est aussi.
c) Réciproque : « si n est pair, alors $n^2$ est pair ». Elle est vraie : $n = 2k$ donne
$n^2 = 2(2k^2)$. Faire remarquer qu'ici les deux sens sont vrais, ce qui n'est pas le cas
général — c'est ce qui autorise l'équivalence.
d) Faux : 9 est impair et n'est pas premier. Un seul contre-exemple suffit à réfuter une
proposition universelle ; en revanche, aucun nombre d'exemples ne suffirait à la démontrer.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Signe de f' confondu avec signe de f | Reprendre les deux droites parallèles de pente $- 1$ |
| Ordre inversé dans la dérivée d'un quotient | Imposer l'écriture séparée de u, v, u', v' |
| $f(a)$ oublié dans l'équation de la tangente | Faire vérifier que le point $(a ; f(a))$ appartient à la droite obtenue |
| Conclusion sur les variations sans factoriser f' | Refuser la conclusion tant que f' n'est pas factorisée |
| (uv)' écrit u'v' | Test numérique sur $u = v = x$ en $x = 2$ : $(x^2)$' = $2x = 4$, contre $1 \times 1 = 1$ |

## Indicateurs de fin de séance

- L'élève écrit u, v, u', v' avant d'appliquer une formule.
- L'élève dit, sans qu'on le lui demande, que le signe de f' ne donne pas le signe de f.
- L'élève vérifie que le point de contact appartient à la tangente qu'il a trouvée.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
