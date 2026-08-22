# Terminale Spécialité Mathématiques — Séance 2 — Fiche élève
## Fonction exponentielle : exposants, équations, vers le logarithme

**Ton objectif de séance :** ne plus jamais te tromper de règle sur les exposants, et savoir
le vérifier tout seul.

### Règle de travail

- J'écris la règle utilisée **avant** de simplifier.
- Je teste ma réponse sur une valeur numérique avant de déclarer une certitude de 4.
- Je note la certitude : $\square$1 $\square$2 $\square$3 $\square$4, et l'aide utilisée : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 1)

La suite $(v_n)$ est définie par $v_n = 4 \times 0{,}7^n$. Est-elle croissante ou décroissante ?
Justifier.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Avant tout : ta réponse spontanée

**Question 0.** Simplifier l'expression $e^{2x} / e^{x - 1}$.

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Test en $x = 2$ :
- valeur de $e^{2x} / e^{x - 1}$ : ...........................................................
- valeur de ma réponse : .................................................................

Ce que je constate : .....................................................................

---

## Partie 2 — La trace écrite

> **Les quatre règles.** Pour tous réels a et b :
> $\exp(a) \times \exp(b) = \exp(a + b)$
> $\exp(a) / \exp(b) = \exp(a - b)$
> $\exp( - a) = 1 / \exp(a)$
> $(\exp(a))^n = \exp$(na)
>
> **Dans une division, on soustrait — et on garde la parenthèse :**
> $\exp(2x) / \exp(x - 1) = \exp(2x - (x - 1)) = \exp(2x - x + 1) = \exp(x + 1)$.
>
> **Stricte positivité.** Pour tout réel x, $\exp(x) > 0$.
> Conséquences : $\exp(u(x)) = 0$ n'a jamais de solution ; $\exp(u(x)) > 0$ est toujours vraie ;
> on peut simplifier une équation par $\exp(x)$ sans perdre de solution.
>
> **Attention.** $\exp(a + b)$ n'est pas $\exp(a) + \exp(b)$.

---

## Partie 3 — Entraînement

### Comment tu trouves ton parcours

Ton livret individuel porte, pour cette séance, une **posture** et un **parcours**. Le tableau
ci-dessous dit ce que tu traites. Tu ne fais pas les dix exercices : tu fais les tiens, et tu
les fais entièrement.

| Ta posture du jour | Ce que tu traites | Ce qu'on attend de toi |
|---|---|---|
| **DIAGNOSTIQUER** — tu avais laissé ce domaine sans réponse | Question 0, puis exercices 1 et 2 | Répondre même sans être sûr : déclarer une certitude de 1 est une réponse, pas un aveu |
| **CONFRONTER** — tu t'es trompé en étant sûr de toi | Question 0, puis exercices 1 à 4 | Écrire ce que tu croyais, puis ce qui l'a mis en défaut |
| **INSTALLER** — il te manque quelque chose, et tu le sais | Exercices 1 à 4 | Écrire la propriété utilisée **avant** chaque calcul |
| **CONSOLIDER** — tu réussis, sans en être sûr | Exercices 3 à 6 | Justifier par écrit, et sans carte d'aide |
| **ENTRETENIR** — c'est acquis et assumé | Exercices 6 à 8 | Rédiger la démonstration en entier, pas seulement le calcul |
| **EXCELLENCE** — ton bilan ne comporte aucun domaine à reprendre | Exercices 9 et 10, puis rôle de vérificateur | Produire une rédaction complète, puis relire celle d'un camarade **sans lui donner la réponse** |

> **Le rôle de vérificateur.** Si tu es en parcours excellence, le professeur te confiera la
> copie d'un camarade. Tu ne corriges pas : tu dis si la propriété a été écrite avant le
> calcul, si la conclusion répond bien à la question, et si une étape manque. Savoir dire
> *où* un raisonnement s'interrompt est une compétence de Terminale à part entière.

### Parcours consolidation (exercices 1 à 4)

**Exercice 1.** Simplifier $e^{3x} \times e^{1 - x} / e^{x}$ et donner le résultat sous la forme
$e^{ax+b}$.

Règle utilisée : ...........................................................................

Calcul : ...........................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Résoudre dans $\mathbb{R}$ l'équation $e^{x^2 - 1} = 0$, puis l'inéquation $e^x > 0$.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Simplifier $e^{5x} / e^{2x+3}$.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Écrire $1 / e^{3x}$ sous la forme $e^{ax}$.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

### Parcours maîtrise (exercices 3 à 6)

**Exercice 5.** Résoudre dans $\mathbb{R}$ l'équation $e^{2x} = e^{x+3}$.

....................................................................................................

**Exercice 6.** Factoriser $e^{2x} - e^x$, puis résoudre $e^{2x} - e^x = 0$. Combien de
solutions ? Expliquer pourquoi on n'en perd aucune en simplifiant par $e^x$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Parcours approfondissement (exercices 6 à 8)

**Exercice 7.** Démontrer que pour tout réel x, $\exp(x) > 0$.
*Piste : écrire $\exp(x)$ comme un carré, puis utiliser $\exp(x) \times \exp( - x) = 1$.*

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 8.** Soit f définie sur $\mathbb{R}$ par $f(x) = x e^{ - x}$. Calculer $f'(x)$ et étudier son signe.
En déduire le tableau de variations de f.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Parcours excellence (exercices 9 et 10)

**Exercice 9.** Soit f définie sur $\mathbb{R}$ par $f(x) = (x - 1)e^{x} + 2$.

a) Calculer $f'(x)$ et montrer que $f'(x) = x e^{x}$.

....................................................................................................

....................................................................................................

....................................................................................................

b) Étudier le signe de $f'(x)$, puis dresser le tableau de variations de f sur $\mathbb{R}$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

c) Déterminer une équation de la tangente à la courbe de f au point d'abscisse 0.

....................................................................................................

....................................................................................................

....................................................................................................

d) En déduire que l'équation $f(x) = 0$ n'admet aucune solution réelle.

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Pour chacune des trois affirmations : vraie ou fausse, avec une
démonstration ou un contre-exemple.

a) « Si $e^a = e^b$, alors $a = b$. »

....................................................................................................

....................................................................................................

b) « Pour tout réel x, $e^{2x} = 2e^{x}$. »

....................................................................................................

....................................................................................................

c) « L'équation $e^x = - 3$ n'a pas de solution. »

....................................................................................................

....................................................................................................

d) Parmi ces trois énoncés, l'un est une propriété du cours, un autre une erreur de calcul
courante. Lesquels, et quelle est la différence entre les deux ?

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Partie 4 — Ce que la Terminale en fera

> La **fonction logarithme népérien** est introduite comme la fonction qui défait
> l'exponentielle : $\ln(\exp(x)) = x$, et $\exp(\ln x) = x$ pour $x > 0$.
>
> Chaque règle sur exp devient une règle sur ln :
>
> | exp | ln |
> |---|---|
> | $\exp(a + b) = \exp(a) \times \exp(b)$ | ln(ab) $= \ln a + \ln b$ |
> | $\exp(a - b) = \exp(a) / \exp(b)$ | $\ln(a/b) = \ln a - \ln b$ |
> | exp(na) $= (\exp(a))^n$ | $\ln(a^n) = n \ln$ a |
>
> Une erreur sur exp aujourd'hui deviendra la même erreur sur ln en octobre. C'est la raison
> d'être de cette séance.

---

## Ouverture maths expertes — 20 minutes

> **Pour qui.** Cet encadré ne concerne que les élèves qui ont choisi l'option
> **mathématiques expertes** en Terminale. Les autres passent directement au bilan de séance.
> Le temps y est prélevé sur la phase différenciée : il ne retire rien au programme commun.

**Le lien avec la séance du jour.** Les règles d'exposants que tu viens d'appliquer à l'exponentielle sont
les mêmes que celles de la décomposition d'un entier en facteurs premiers.

**a)** Donner la liste complète des diviseurs positifs de 60. Combien y en a-t-il ?

....................................................................................................

....................................................................................................

**b)** Décomposer 60, puis 360, en produit de facteurs premiers.

....................................................................................................

....................................................................................................

**c)** On admet le résultat suivant : si la décomposition de n en facteurs premiers s'écrit
$n = p_1^{a_1} \times \dots \times p_k^{a_k}$, alors n admet exactement
$(a_1 + 1) \times \dots \times (a_k + 1)$ diviseurs positifs. Vérifier ce résultat sur 60,
puis l'appliquer à 360 sans écrire la liste.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Le fait que cette décomposition soit unique est le
**théorème fondamental de l'arithmétique**. Il sera démontré dans l'option.

---

## Partie 5 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**Mon ancienne erreur, écrite avec mes mots :** ............................................

....................................................................................................

**Le contrôle que je ferai désormais avant de valider :** ..................................

....................................................................................................

**Ma certitude sur la fonction exponentielle, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
