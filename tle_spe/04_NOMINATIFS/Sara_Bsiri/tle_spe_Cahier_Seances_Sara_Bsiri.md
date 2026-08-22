# Terminale Spécialité Mathématiques — Cahier des cinq séances — Sara Bsiri
## Mathématiques — Stage de pré-rentrée 2026-2027

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Sara Bsiri  
**Groupe :** Groupe 1 — Stages de mathématiques et de NSI  
**Matière :** Mathématiques  
**Organisme :** Nexus Réussite  
**Stage :** 10 heures, 2 heures par jour, 5 jours consécutifs  
**Dates :** du 24 au 28 août 2026

---

## Ton parcours de pré-rentrée

Le thème de chaque séance est commun au groupe. L'objectif, la piste et les exercices sont les tiens : ils viennent de ton positionnement.

| Séance | Thème | Ton objectif | Ta piste |
|---:|---|---|:---:|
| 1 | Suites numériques : du sens de variation à la récurrence | Rédiger la démonstration du sens de variation d'une suite géométrique, puis établir qu'une suite peut croître sans jamais dépasser une valeur. | Excellence |
| 2 | Fonction exponentielle : exposants, équations, vers le logarithme | Mener une étude de fonction complète sur un produit faisant intervenir l'exponentielle, et trancher une équation par le tableau de variations. | Excellence |
| 3 | Second degré : discriminant, signe du trinôme, tableau de signes | Factoriser un polynôme de degré 3 à partir d'une racine évidente, puis discuter le nombre de solutions d'une équation selon un paramètre. | Excellence |
| 4 | Dérivation : du nombre dérivé aux variations, ouverture sur la convexité | Dériver un quotient, en déduire un encadrement de la fonction, et distinguer l'annulation de la dérivée du changement de signe. | Excellence |
| 5 | Produit scalaire vers l'espace, probabilités, Python, évaluation | Établir une probabilité en fonction d'un paramètre, la comparer à une valeur seuil par une factorisation, et la vérifier par un programme. | Excellence |

## Comment utiliser ce cahier

- Chaque séance suit le même ordre : réactivation, essentiel, méthode, entraînement, transfert, ouverture, bilan.
- Tu ne traites que les exercices de ta piste. Ils sont déjà sélectionnés ici : ce cahier ne contient pas ceux des autres.
- Écris la propriété ou la relation **avant** de calculer. C'est la seule habitude que ce stage cherche à installer partout.
- Note à chaque fois la lettre de l'aide utilisée. Ce n'est pas un aveu : c'est la mesure de ton autonomie, et on veut la voir baisser d'ici la séance 5.

---

<div class="page-break"></div>

# Séance 1 — Suites numériques : du sens de variation à la récurrence

**Le thème du groupe aujourd'hui :** Suites numériques : du sens de variation à la récurrence.  
**Ta piste :** Excellence. Produis une rédaction complète, puis relis la copie d'un camarade sans lui donner la réponse.

## Aujourd'hui, tu vas…

Rédiger la démonstration du sens de variation d'une suite géométrique, puis établir qu'une suite peut croître sans jamais dépasser une valeur.

> **Rappel.** Un point sur lequel tu peux t'appuyer aujourd'hui : Second degré — réponses justes, données avec assurance : c'est un vrai point d'appui pour la suite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. $(u_n)$ arithmétique, $u_0 = 3$, raison 5. Que vaut $u_4$ ?  ....................
2. $(v_n)$ géométrique, $v_0 = 2$, raison 3. Que vaut $v_3$ ?  ....................
3. Calculer $0{,}5^3$, puis $0{,}5^4$. Laquelle est la plus grande ?  ....................
4. $(w_n)$ géométrique de raison $0{,}9$ et de premier terme positif : croissante ou décroissante ?  ....................
5. Écrire $u_{n+1} - u_n$ pour $u_n = 3n + 1$. Que vaut cette différence ?  ....................
6. Une suite dont la différence $u_{n+1} - u_n$ vaut $- 2$ : que peut-on dire d'elle ?  ....................
7. $u_{n+1}$ et $u_n + 1$ désignent-ils la même chose ?  ....................

## L'essentiel à retenir

> **Sens de variation d'une suite — méthode générale.**
> On étudie le signe de $u_{n+1} - u_n$.
> Si $u_{n+1} - u_n \geqslant 0$ pour tout n, la suite est croissante.
> Si $u_{n+1} - u_n \leqslant 0$ pour tout n, la suite est décroissante.
>
> **Cas d'une suite géométrique** de premier terme $v_0 > 0$ et de raison $q > 0$ :
> $v_{n+1} - v_n = v_0 q^n (q - 1)$. Comme $v_0 > 0$ et $q^n > 0$, le signe est celui de $q - 1$.
> Donc : $q > 1$ croissante ; $q = 1$ constante ; $0 < q < 1$ décroissante.
> **On compare la raison à 1, pas à 0.**
>
> **Formules explicites.**
> Suite arithmétique : $u_n = u_0 + n \times r$.
> Suite géométrique : $v_n = v_0 \times r^n$.

---

## La méthode, dans l'ordre

1. J'écris la relation qui définit la suite, telle qu'elle est donnée.
2. Je calcule la différence $u_{n+1} - u_n$, sans la simplifier tout de suite.
3. J'étudie le signe de cette différence pour tout entier naturel n.
4. Je conclus sur le sens de variation, en une phrase complète.
5. Je contrôle en calculant les trois premiers termes.

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Comparer la raison à 0 au lieu de la comparer à 1. Une raison de $0{,}9$ est positive, et pourtant la suite décroît.
- Conclure sur les variations sans avoir écrit la différence : l'erreur de méthode devient invisible dans un calcul faux.
- Confondre $u_{n+1}$, le terme suivant, et $u_n + 1$, le terme augmenté de 1.
- Écrire $v_n = v_0 \times n \times r$ au lieu de $v_0 \times r^n$ pour une suite géométrique.

## Ton entraînement

**Exercice 9.** La suite $(u_n)$ est définie par $u_0 = 1$ et, pour tout entier naturel n,
$u_{n+1} = u_n/(1 + u_n)$.

a) Calculer $u_1$, $u_2$ et $u_3$ sous forme de fractions irréductibles. Conjecturer une
expression de $u_n$ en fonction de n.

....................................................................................................

....................................................................................................

....................................................................................................

b) On admet que $u_n > 0$ pour tout entier naturel n. Démontrer que la suite est
strictement décroissante.

....................................................................................................

....................................................................................................

....................................................................................................

c) On pose $v_n = 1/u_n$. Calculer $v_0$, $v_1$ et $v_2$, puis démontrer que $(v_n)$ est
arithmétique. En déduire l'expression de $u_n$ en fonction de n, et comparer à ta conjecture.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

d) La suite $(u_n)$ peut-elle s'annuler ? Peut-elle devenir négative ? Justifier.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Un élève écrit : « une suite décroissante finit toujours par devenir
négative ».

a) Produire un contre-exemple, et l'écrire complètement.

....................................................................................................

....................................................................................................

b) Rédiger l'énoncé correct : quelle condition faut-il ajouter pour qu'une suite décroissante
reste positive ?

....................................................................................................

....................................................................................................

c) La réciproque — « une suite qui reste positive est décroissante » — est-elle vraie ?
Justifier.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Ton exercice, celui qui vient de ton positionnement

**Dérivation — Distinguer le signe de la dérivée et le signe de la fonction.** Cet exercice est là parce que, au positionnement, la question correspondante a donné une réussi avec une certitude de 2/4.

On sait que g' est strictement positive sur ]0 ; 5[. Que peut-on affirmer sur les variations de g ? Peut-on en déduire le signe de g sur cet intervalle ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

> **Méthode.** Le signe de f' renseigne sur le sens de variation de f, jamais sur le signe de f. Ce sont deux informations indépendantes.

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

Une entreprise compte $\SI{1200}{}$ abonnés et en perd $\SI{5}{\percent}$
par mois, mais en gagne 30 nouveaux chaque mois. On note $a_n$ le nombre d'abonnés après n
mois. Écris la relation qui lie $a_{n+1}$ à $a_n$. Cette suite est-elle arithmétique ?
géométrique ? Ni l'une ni l'autre ? Calcule $a_1$ et $a_2$, puis dis si le nombre d'abonnés
augmente ou diminue au début.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> Une suite **croissante et majorée** converge : elle se rapproche d'une valeur limite sans
> jamais la dépasser. C'est le premier grand résultat de l'année.
>
> Pour démontrer qu'une suite est majorée, on utilise le **raisonnement par récurrence** :
> on vérifie la propriété au rang 0, puis on démontre que si elle est vraie au rang n, elle
> l'est au rang n+1.
>
> Tout cela part du sens de variation. C'est pourquoi il devait être sûr aujourd'hui.

---

## Ouverture maths expertes — 20 minutes

> **Pour qui.** Cet encadré ne concerne que les élèves qui ont choisi l'option
> **mathématiques expertes** en Terminale. Les autres passent directement au bilan de séance.
> Le temps y est prélevé sur la phase différenciée : il ne retire rien au programme commun.

**Le lien avec la séance du jour.** Une suite d'entiers, c'est une famille infinie de nombres dont on
peut étudier la divisibilité. L'option commence là : par la division euclidienne.

**a)** Effectuer la division euclidienne de 47 par 6 : écrire $47 = 6q + r$ en contrôlant
que $0 \leqslant r < 6$.

....................................................................................................

....................................................................................................

**b)** Pour tout entier naturel n, on pose $u_n = 4n + 3$. Calculer $u_0$, $u_1$, $u_2$ et
$u_3$, puis effectuer la division euclidienne de chacun par 4. Que remarques-tu sur le reste ?

....................................................................................................

....................................................................................................

....................................................................................................

**c)** Démontrer qu'aucun terme de la suite $(u_n)$ n'est divisible par 4.

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Ce reste constant, c'est la notion de **congruence** : on
écrira que $u_n$ est congru à 3 modulo 4. Toute l'arithmétique de l'option repose dessus.

---

## Prendre du recul

- Comment vérifier, sans refaire le calcul, qu'une suite annoncée décroissante l'est bien ?

....................................................................................................

- Quelle donnée de l'énoncé aurais-tu pu ignorer sans changer ta réponse ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Écris la différence $u_{n+1} - u_n$ pour $u_n = 2 \times 3^n$, sans la calculer.

....................................................................................................

**2.** Une suite géométrique de raison $0{,}95$ et de premier terme 100 : croissante ou décroissante ? Pourquoi ?

....................................................................................................

**3.** En une phrase : à quoi le sens de variation va-t-il servir en Terminale ?

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Ton bilan ne signale aucune priorité : le stage servira à prolonger tes acquis. Choisis un domaine que tu veux pousser plus loin — on partira de là.

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 2 — Fonction exponentielle : exposants, équations, vers le logarithme

**Le thème du groupe aujourd'hui :** Fonction exponentielle : exposants, équations, vers le logarithme.  
**Ta piste :** Excellence. Produis une rédaction complète, puis relis la copie d'un camarade sans lui donner la réponse.

## Aujourd'hui, tu vas…

Mener une étude de fonction complète sur un produit faisant intervenir l'exponentielle, et trancher une équation par le tableau de variations.

> **Rappel.** Un point sur lequel tu peux t'appuyer aujourd'hui : Tu peux t'appuyer sur la dérivation : les réponses sont justes et assumées, rien à reprendre pour l'instant.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Que vaut $e^0$ ?  ....................
2. Simplifier $e^3 \times e^{-3}$.  ....................
3. Écrire $e^{2x} \times e^{x}$ sous la forme $e^{ax}$.  ....................
4. Écrire $1/e^{x}$ avec un exposant négatif.  ....................
5. $(e^x)^3$ vaut-il $e^{3x}$ ou $3e^x$ ?  ....................
6. L'équation $e^x = 0$ a-t-elle une solution ?  ....................
7. $e^x$ est-il parfois négatif ?  ....................
8. Résoudre $e^x = e^5$.  ....................

## L'essentiel à retenir

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

## La méthode, dans l'ordre

1. Je ramène chaque membre à une seule exponentielle, en additionnant les exposants.
2. Si l'équation est de la forme $e^A = e^B$, j'utilise la stricte croissance : $A = B$.
3. Si un facteur $e^x$ apparaît partout, je le factorise — il ne s'annule jamais.
4. Je résous l'équation restante, qui ne contient plus d'exponentielle.
5. Je vérifie la solution en la remplaçant dans l'énoncé de départ.

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Écrire $e^{2x} = 2e^x$. Un exposant n'est pas un facteur : $e^{2x} = (e^x)^2$.
- Chercher les valeurs qui annulent $e^x$ : il n'y en a pas, l'exponentielle est strictement positive.
- Simplifier $e^{a} + e^{b}$ en $e^{a+b}$. La règle vaut pour le produit, pas pour la somme.
- Oublier que $e^{-x} = 1/e^{x}$ et traiter le signe moins comme un facteur.

## Ton entraînement

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

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

Une population de bactéries suit $N(t) = 500 e^{0{,}3t}$, où t est en
heures. Au bout de combien d'heures la population dépasse-t-elle 2000 ? Tu ne disposes pas
encore du logarithme : procède par encadrement, en calculant $N(4)$ et $N(5)$. Que faudrait-il
pour répondre exactement ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

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

## Prendre du recul

- Comment vérifier qu'une solution d'équation avec exponentielle est correcte ?

....................................................................................................

- Pourquoi l'équation $e^x = k$ n'a-t-elle pas toujours de solution ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Simplifie $e^{4x} / e^{x-2}$.

....................................................................................................

**2.** Résous $e^{3x} = e^{x+4}$.

....................................................................................................

**3.** Vrai ou faux : $e^{x}$ peut valoir 0. Justifie en une ligne.

....................................................................................................

### D'ici la prochaine séance — quinze minutes, pas davantage

Et pendant tout le stage, garde le réflexe du bilan : avant de valider une réponse, demande-toi « j'en suis sûr, ou je crois l'être ? ».

Fait : $\square$oui $\square$non    Ce que j'ai noté : ..................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 3 — Second degré : discriminant, signe du trinôme, tableau de signes

**Le thème du groupe aujourd'hui :** Second degré : discriminant, signe du trinôme, tableau de signes.  
**Ta piste :** Excellence. Produis une rédaction complète, puis relis la copie d'un camarade sans lui donner la réponse.

## Aujourd'hui, tu vas…

Factoriser un polynôme de degré 3 à partir d'une racine évidente, puis discuter le nombre de solutions d'une équation selon un paramètre.

> **Rappel.** Un point sur lequel tu peux t'appuyer aujourd'hui : Fonction exponentielle — acquis et disponible. On s'en servira comme socle pour aller plus loin.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Que vaut le discriminant de $x^2 - 5x + 6$ ?  ....................
2. Combien de racines si $\Delta < 0$ ?  ....................
3. Racines de $x^2 - 4 = 0$.  ....................
4. Le trinôme $x^2 + 1$ s'annule-t-il sur $\mathbb{R}$ ?  ....................
5. Somme et produit des racines de $x^2 - 7x + 12$.  ....................
6. Signe de $- 2x^2 + 3$ quand x est très grand.  ....................
7. Un trinôme de coefficient dominant positif et de discriminant négatif : quel est son signe ?  ....................

## L'essentiel à retenir

> **Résolution.** $\Delta = b^2 - 4$ac.
> $\Delta > 0$ : deux racines $( - b \pm \surd \Delta )/(2a)$. $\Delta = 0$ : une racine double $- b/(2a)$. $\Delta < 0$ : aucune
> racine réelle.
> **Contrôle :** somme des racines = $- b/a$, produit = c/a.
>
> **Signe du trinôme ax^2 + bx + c :**
> il est **du signe de a à l'extérieur des racines**, et **du signe contraire entre les
> racines**.
> Si $\Delta < 0$, il garde le signe de a sur $\mathbb{R}$ tout entier.
>
> **Ensemble solution.** Crochets ouverts pour une inégalité stricte, fermés pour une
> inégalité large. Deux intervalles disjoints se relient par le symbole $\cup$.

---

## La méthode, dans l'ordre

1. J'identifie a, b et c, en respectant les signes.
2. Je calcule $\Delta = b^2 - 4ac$.
3. Je discute : deux racines si $\Delta > 0$, une racine double si $\Delta = 0$, aucune si $\Delta < 0$.
4. Je place les racines dans un tableau de signes, et j'écris d'abord le signe de a.
5. Le trinôme est du signe de a partout, sauf entre les racines.

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Dresser un tableau de signes sans y faire figurer le signe de a : le tableau est alors faux une fois sur deux.
- Oublier le signe de b dans $b^2$ : le carré rend positif, mais $- 4ac$ garde le sien.
- Conclure « pas de solution » quand $\Delta < 0$ sans préciser « dans $\mathbb{R}$ ».
- Résoudre une inéquation en gardant le sens de l'inégalité après multiplication par un nombre négatif.

## Ton entraînement

**Exercice 9.** Soit $P(x) = 2x^3 - 3x^2 - 3x + 2$.

a) Vérifier que $P(2) = 0$.

....................................................................................................

....................................................................................................

b) Déterminer les réels a, b et c tels que, pour tout réel x,
$P(x) = (x - 2)(ax^2 + bx + c)$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

c) Résoudre dans $\mathbb{R}$ l'équation $2x^2 + x - 1 = 0$.

....................................................................................................

....................................................................................................

....................................................................................................

d) En déduire l'ensemble des solutions de $P(x) = 0$, puis dresser le tableau de signes
de P sur $\mathbb{R}$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** On considère l'équation $m x^2 - 4x + 1 = 0$, où m est un réel.

a) Un élève affirme : « le discriminant vaut $16 - 4m$, donc l'équation admet deux solutions
dès que $m < 4$ ». Où est la faille ?

....................................................................................................

....................................................................................................

....................................................................................................

b) Discuter, selon les valeurs de m, le nombre de solutions réelles de l'équation.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

c) Pour quelles valeurs de m l'équation admet-elle exactement une solution réelle ?
*Attention : il y a deux cas, et ils ne relèvent pas du même raisonnement.*

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

Un objet lancé vers le haut a pour altitude $h(t) = - 5t^2 + 20t + 1$,
en mètres, t étant en secondes. Pendant combien de temps l'objet est-il au-dessus de
$\SI{16}{\metre}$ ? Rien dans l'énoncé ne dit d'utiliser le second degré : c'est à toi de le
reconnaître.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> La dérivée d'une fonction polynôme du troisième degré est **un trinôme**. Le tableau de
> signes que tu viens de faire est donc exactement celui dont tu auras besoin pour trouver
> les variations d'une fonction.
>
> En Terminale, on dérive une deuxième fois : le signe de f'' donne les variations de f',
> donc la **convexité** de f. Le même tableau, deux fois par exercice.
>
> Le **théorème des valeurs intermédiaires** s'appuie aussi dessus : si une fonction
> continue est strictement monotone sur un intervalle et y change de signe, l'équation
> $f(x) = 0 y$ a une solution, et une seule.

---

## Ouverture maths expertes — 20 minutes

> **Pour qui.** Cet encadré ne concerne que les élèves qui ont choisi l'option
> **mathématiques expertes** en Terminale. Les autres passent directement au bilan de séance.
> Le temps y est prélevé sur la phase différenciée : il ne retire rien au programme commun.

**Le lien avec la séance du jour.** Le discriminant décide de l'existence des racines ; l'algorithme
d'Euclide décide de l'irréductibilité d'une fraction. Dans les deux cas, un calcul tranche
une question d'existence.

**a)** Calculer le PGCD de 252 et 198 par l'algorithme d'Euclide, en écrivant chaque division
euclidienne sur une ligne.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**b)** En déduire la forme irréductible de la fraction $252/198$.

....................................................................................................

....................................................................................................

**c)** Deux entiers sont dits **premiers entre eux** lorsque leur PGCD vaut 1. Les entiers 252
et 198 le sont-ils ? Et le numérateur et le dénominateur de la fraction obtenue en b) ?

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** L'algorithme d'Euclide fournit aussi deux entiers u et v tels
que $au + bv$ soit égal au PGCD de a et b : c'est le **théorème de Bézout**, cœur de l'option.

---

## Prendre du recul

- Comment vérifier deux racines trouvées sans refaire le discriminant ?

....................................................................................................

- Un tableau de signes sans le signe de a : pourquoi est-ce faux une fois sur deux ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Que vaut le discriminant de $2x^2 - 4x + 5$ ? Combien de racines ?

....................................................................................................

**2.** Signe de $- x^2 + 4$ sur $\mathbb{R}$, en une ligne.

....................................................................................................

**3.** Somme et produit des racines de $x^2 - 9x + 20$, sans les calculer.

....................................................................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 4 — Dérivation : du nombre dérivé aux variations, ouverture sur la convexité

**Le thème du groupe aujourd'hui :** Dérivation : du nombre dérivé aux variations, ouverture sur la convexité.  
**Ta piste :** Excellence. Produis une rédaction complète, puis relis la copie d'un camarade sans lui donner la réponse.

## Aujourd'hui, tu vas…

Dériver un quotient, en déduire un encadrement de la fonction, et distinguer l'annulation de la dérivée du changement de signe.

> **Rappel.** Un point sur lequel tu peux t'appuyer aujourd'hui : Suites numériques — réponses justes, données avec assurance : c'est un vrai point d'appui pour la suite.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. Dérivée de $x^3$.  ....................
2. Dérivée de $5x$.  ....................
3. Dérivée d'une constante.  ....................
4. Formule de $(uv)'$.  ....................
5. Formule de $(u/v)'$.  ....................
6. Si $f'$ est négative sur un intervalle, que fait f ?  ....................
7. $f'(2) = 0$ : que peut-on affirmer, et que ne peut-on pas affirmer ?  ....................
8. Que représente $f'(a)$ pour la courbe de f au point d'abscisse a ?  ....................

## L'essentiel à retenir

> **Nombre dérivé.** $f'(a)$ est le coefficient directeur de la tangente à la courbe au point
> d'abscisse a.
> Équation de la tangente : **$y = f'(a)(x - a) + f(a)$**.
>
> **Formules.**
> (u + v)' = u' + v' · (ku)' = ku' · (uv)' = u'v + uv' · (u/v)' = (u'$v -$ uv')$/v^2$
>
> **Signe et variations.**
> Là où $f' > 0$, f est strictement **croissante**.
> Là où $f' < 0$, f est strictement **décroissante**.
> Le signe de f' ne dit **rien** du signe de f.

---

## La méthode, dans l'ordre

1. Je repère la forme de l'expression : produit, quotient, ou somme de termes simples.
2. Je pose u et v à part, puis j'écris $u'$ et $v'$ avant toute chose.
3. J'applique la formule correspondante, sans développer tout de suite.
4. Je factorise la dérivée : le signe se lit sur une forme factorisée, jamais sur une forme développée.
5. Je dresse le tableau de signes de la dérivée, puis celui des variations.

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Écrire $(uv)' = u'v'$. La dérivée d'un produit n'est pas le produit des dérivées.
- Conclure sur les variations à partir d'une dérivée développée, dont le signe ne se lit pas.
- Déduire de $f'(a) = 0$ qu'il y a un extremum : il faut que $f'$ change de signe.
- Confondre $f(a)$, l'ordonnée, et $f'(a)$, la pente de la tangente.

## Ton entraînement

**Exercice 9.** Soit f définie sur $\mathbb{R}$ par $f(x) = 2x/(x^2 + 1)$.

a) Calculer $f'(x)$ et montrer que $f'(x) = 2(1 - x^2)/(x^2 + 1)^2$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

b) Étudier le signe de $f'(x)$, puis dresser le tableau de variations de f sur $\mathbb{R}$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

c) En déduire que pour tout réel x, $- 1 \leqslant f(x) \leqslant 1$.

....................................................................................................

....................................................................................................

....................................................................................................

d) Déterminer une équation de la tangente à la courbe de f au point d'abscisse 0.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Un élève écrit : « si $f'(a) = 0$, alors f admet un extremum en a ».

a) Produire un contre-exemple, avec le calcul qui l'établit.

....................................................................................................

....................................................................................................

....................................................................................................

b) Rédiger l'énoncé correct : quelle condition faut-il ajouter sur $f'$ au voisinage de a ?

....................................................................................................

....................................................................................................

....................................................................................................

c) La réciproque — « si f admet un extremum en a, alors $f'(a) = 0$ » — est-elle vraie pour
une fonction dérivable sur $\mathbb{R}$ ? Et pour une fonction dérivable sur $[0 ; 1]$ ?

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

Une boîte sans couvercle est fabriquée dans un carré de carton de
$\SI{20}{\centi\metre}$ de côté, en découpant un carré de côté x à chaque coin. Son volume
vaut $V(x) = x(20 - 2x)^2$. Pour quelle valeur de x le volume est-il maximal ? L'énoncé ne
dit pas de dériver : à toi de décider.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> En Terminale, on dérive **une deuxième fois**.
>
> Le signe de f'' donne les variations de f'. Là où f'' $\geqslant 0$, f' croît : la courbe de f
> tourne vers le haut, on dit que f est **convexe**. Là où f'' $\leqslant 0$, f est **concave**. Le
> point où f'' change de signe est un **point d'inflexion**.
>
> C'est exactement le geste d'aujourd'hui, fait une fois de plus. Pour qu'il fonctionne au
> deuxième étage, il doit être sûr au premier.

---

## Ouverture maths expertes — 20 minutes

> **Pour qui.** Cet encadré ne concerne que les élèves qui ont choisi l'option
> **mathématiques expertes** en Terminale. Les autres passent directement au bilan de séance.
> Le temps y est prélevé sur la phase différenciée : il ne retire rien au programme commun.

**Le lien avec la séance du jour.** Tu viens d'écrire « si $f'$ est positive, alors f est croissante », et de
constater que la réciproque ne se déduit pas de l'énoncé. C'est exactement l'objet de la
logique de l'option.

**a)** Écrire la contraposée de l'implication : « si $n^2$ est pair, alors n est pair ».

....................................................................................................

....................................................................................................

**b)** Démontrer cette implication en utilisant sa contraposée. *Piste : un entier impair
s'écrit $2k + 1$.*

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**c)** Écrire la réciproque de cette implication. Est-elle vraie ? Justifier.

....................................................................................................

....................................................................................................

**d)** « Tout entier impair est premier. » Vrai ou faux ? Si c'est faux, un contre-exemple
suffit-il à le prouver ? Et s'il s'agissait de prouver que c'est vrai ?

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Contraposée, réciproque, contre-exemple, raisonnement par
l'absurde : l'option exige que chaque démonstration annonce lequel de ces raisonnements elle
emploie.

---

## Prendre du recul

- Comment savoir si un extremum trouvé est un maximum et non un minimum ?

....................................................................................................

- Pourquoi factoriser la dérivée avant d'étudier son signe ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** Dérive $f(x) = (2x + 1)(x - 3)$.

....................................................................................................

**2.** $f'$ est négative sur $]0 ; 3[$ : que fait f sur cet intervalle ?

....................................................................................................

**3.** $f'(2) = 0$ : peut-on affirmer qu'il y a un extremum en 2 ? Justifie.

....................................................................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

# Séance 5 — Produit scalaire vers l'espace, probabilités, Python, évaluation

**Le thème du groupe aujourd'hui :** Produit scalaire vers l'espace, probabilités, Python, évaluation.  
**Ta piste :** Excellence. Produis une rédaction complète, puis relis la copie d'un camarade sans lui donner la réponse.

## Aujourd'hui, tu vas…

Établir une probabilité en fonction d'un paramètre, la comparer à une valeur seuil par une factorisation, et la vérifier par un programme.

> **Rappel.** Un point sur lequel tu peux t'appuyer aujourd'hui : Tu peux t'appuyer sur le produit scalaire : les réponses sont justes et assumées, rien à reprendre pour l'instant.

## Pour commencer — dix minutes, de tête

Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a besoin. Si l'une te bloque, signale-la : c'est une information utile.

1. $u(3 ; - 1)$ et $v(2 ; 6)$ : calculer $u \cdot v$.  ....................
2. Le produit scalaire est-il un nombre ou un vecteur ?  ....................
3. Deux vecteurs non nuls orthogonaux : que vaut leur produit scalaire ?  ....................
4. $P(A) = 0{,}3$ : que vaut $P(\bar{A})$ ?  ....................
5. A et B incompatibles : que vaut $P(A \cap B)$ ?  ....................
6. Formule de $P(A \cup B)$.  ....................
7. Que renvoie `range(2, 10, 3)` ?  ....................
8. Une variable aléatoire prend les valeurs 0 et 2 avec les probabilités $0{,}4$ et $0{,}6$ : que vaut son espérance ?  ....................

## La méthode, dans l'ordre

1. Pour le produit scalaire : j'écris les coordonnées des deux vecteurs, puis j'applique la formule.
2. Pour l'orthogonalité : je pose le produit scalaire égal à zéro et je résous.
3. Pour une probabilité : je décris l'expérience, puis je choisis entre arbre et tableau.
4. Pour une espérance : je dresse la loi de probabilité complète avant de sommer.
5. Pour un programme : je déroule une table de trace sur trois tours avant d'exécuter.

> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la propriété écrite avant le calcul, la conclusion qui répond à la question posée.

## Les pièges de ce domaine

- Annoncer un vecteur comme résultat d'un produit scalaire : c'est un nombre.
- Confondre événements incompatibles et événements indépendants.
- Oublier que la somme des probabilités d'une loi vaut 1, et ne pas s'en servir pour contrôler.
- Dans une boucle `for`, confondre le nombre d'itérations et la dernière valeur prise.

## Ton entraînement

**Exercice 9.** Dans un repère orthonormé, on donne $A(1 ; 2)$, $B(5 ; 0)$ et $C(4 ; 5)$.

a) Calculer $\vv{AB} \cdot \vv{AC}$.

....................................................................................................

....................................................................................................

....................................................................................................

b) Calculer les longueurs AB et AC, puis en déduire la valeur exacte du cosinus de l'angle
$\widehat{BAC}$.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

c) Déterminer une équation cartésienne de la droite passant par A et perpendiculaire à (BC).

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

d) Le point $H(3 ; 2{,}4)$ appartient-il à cette droite ? Justifier par le calcul.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Une urne contient n boules rouges et 3 boules noires, n étant un entier
naturel non nul. On tire une boule, on note sa couleur, on la remet, puis on tire une seconde
boule.

a) Exprimer, en fonction de n, la probabilité d'obtenir deux boules de la même couleur.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

b) Pour quelle valeur de n cette probabilité vaut-elle exactement 0,5 ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

c) Écrire une fonction Python `proba(n)` qui renvoie cette probabilité, puis vérifier ta
réponse à la question b).

```python
def proba(n):




```

d) Cette probabilité peut-elle être strictement inférieure à 0,5 ? Justifier — la réponse
tient en une factorisation.

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Transfert — à toi de choisir la méthode

Rien dans cet énoncé ne dit quelle notion employer. C'est la question.

Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la conclusion écrite en français.

Un jeu propose de tirer une carte dans un jeu de 32. Tu gagnes 5 euros si
c'est un cœur, 10 euros si c'est l'as de pique, et tu perds 2 euros sinon. Le jeu
est-il favorable au joueur ? Décide quelle notion utiliser, puis conclus.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

## Pour aller vers la Terminale

Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies à quoi sert ce que tu viens de travailler.

> Dans l'espace, le produit scalaire s'écrit avec trois coordonnées :
> $u \cdot v = x_u x_v + y_u y_v + z_u z_v$.
>
> Un vecteur **normal** à un plan est orthogonal à deux vecteurs directeurs de ce plan. Si
> $n(a ; b ; c)$ est normal au plan P et si $A(x_0 ; y_0 ; z_0)$ appartient à P, alors P a pour
> équation cartésienne :
> $a(x - x_0) + b(y - y_0) + c(z - z_0) = 0$.
>
> Autrement dit : **l'équation d'un plan est un produit scalaire nul.** Le critère que tu
> viens d'utiliser est l'outil principal de toute la géométrie de Terminale.

---

## Ouverture maths expertes — 20 minutes

> **Pour qui.** Cet encadré ne concerne que les élèves qui ont choisi l'option
> **mathématiques expertes** en Terminale. Les autres passent directement au bilan de séance.
> Le temps y est prélevé sur la phase différenciée : il ne retire rien au programme commun.

**Le lien avec la séance du jour.** Un système linéaire et un produit scalaire manipulent les mêmes
coefficients. L'option leur donne un objet commun : la matrice.

**a)** Résoudre par substitution le système formé de $2x + 3y = 8$ et $5x - y = 3$, puis
vérifier le résultat par combinaison linéaire des deux lignes.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**b)** Ce système s'écrit $AX = B$, où A est le tableau des coefficients
$\begin{pmatrix} 2 & 3 \\ 5 & -1 \end{pmatrix}$. Le nombre $2 \times ( - 1) - 3 \times 5$
s'appelle le **déterminant** de A. Le calculer. Que se passerait-il, pour le système, si ce
nombre était nul ?

....................................................................................................

....................................................................................................

....................................................................................................

**c)** Développer $(a + b)^2$, puis $(a - b)(a + b)$. En Terminale, l'option étend ces
identités aux **nombres complexes**, où un nombre i vérifie $i^2 = - 1$. Calculer
$(2 + i)(2 - i)$.

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Matrices et nombres complexes sont les deux autres piliers de
l'option, à côté de l'arithmétique travaillée aux séances 1 à 4.

---

## Prendre du recul

- Comment contrôler qu'une loi de probabilité est complète ?

....................................................................................................

- Un produit scalaire nul : que peux-tu affirmer, et que ne peux-tu pas affirmer ?

....................................................................................................

## Avant de partir

Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est à confirmer, et ce qui doit être repris à la séance suivante.

**1.** $u(2 ; - 3)$ et $v(6 ; 4)$ : ces vecteurs sont-ils orthogonaux ?

....................................................................................................

**2.** $P(A) = 0{,}4$, $P(B) = 0{,}5$, A et B incompatibles : que vaut $P(A \cup B)$ ?

....................................................................................................

**3.** Une espérance négative : qu'est-ce que cela signifie pour un jeu ?

....................................................................................................

**Ma certitude sur cette séance :** $\square$1 $\square$2 $\square$3 $\square$4  
**L'aide maximale que j'ai utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune

---

<div class="page-break"></div>

## Bilan personnel — à remplir à la fin du stage

Rien n'est prérempli ici : ce sont des constats, et ils n'existent qu'après les cinq séances.

| Séance | 1 | 2 | 3 | 4 | 5 |
|---|:---:|:---:|:---:|:---:|:---:|
| Aide maximale utilisée | | | | | |
| Certitude déclarée | | | | | |

**Ce que je consolide vraiment, et que je saurais refaire seul**

....................................................................................................

....................................................................................................

**Le point que je dois encore surveiller à la rentrée**

....................................................................................................

....................................................................................................

**Une méthode que je retiens, écrite avec mes mots**

....................................................................................................

....................................................................................................

**La première notion de Terminale que je me sens prêt à aborder**

....................................................................................................

....................................................................................................
