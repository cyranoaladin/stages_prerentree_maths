# Terminale Spécialité Mathématiques — Séance 5 — Fiche élève
## Produit scalaire vers l'espace, probabilités, Python

**Ton objectif de séance :** utiliser le produit scalaire comme un outil de preuve,
réactiver les probabilités, et faire calculer une suite par un programme.

### Règle de travail

- Un produit scalaire donne un **nombre**, jamais un vecteur.
- J'écris la propriété utilisée avant de calculer.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 4)

On sait que f' est strictement positive sur ]2 ; 7[. Que peut-on affirmer sur f ? Que ne
peut-on pas affirmer ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

### Comment tu trouves ton parcours

Cette dernière séance couvre trois domaines et se termine par l'évaluation. Ton livret
individuel porte la posture qui est la tienne : elle dit avec quelle exigence tu traites
chaque partie, pas quels exercices tu sautes.

| Ta posture du jour | Ce que tu traites | Ce qu'on attend de toi |
|---|---|---|
| **DIAGNOSTIQUER** — tu avais laissé ce domaine sans réponse | Exercices 1, 2 et 4 | Répondre même sans être sûr : déclarer une certitude de 1 est une réponse, pas un aveu |
| **CONFRONTER** — tu t'es trompé en étant sûr de toi | Exercices 1 à 4 | Écrire ce que tu croyais, puis ce qui l'a mis en défaut |
| **INSTALLER** — il te manque quelque chose, et tu le sais | Exercices 1 à 4 | Écrire la propriété utilisée **avant** chaque calcul |
| **CONSOLIDER** — tu réussis, sans en être sûr | Exercices 3 à 6 | Justifier par écrit, et sans carte d'aide |
| **ENTRETENIR** — c'est acquis et assumé | Exercices 6 à 8 | Rédiger la démonstration en entier, pas seulement le calcul |
| **EXCELLENCE** — ton bilan ne comporte aucun domaine à reprendre | Exercices 9 et 10, puis rôle de vérificateur | Produire une rédaction complète, puis relire celle d'un camarade **sans lui donner la réponse** |

> **Le rôle de vérificateur.** Si tu es en parcours excellence, le professeur te confiera la
> copie d'un camarade. Tu ne corriges pas : tu dis si la propriété a été écrite avant le
> calcul, si la conclusion répond bien à la question, et si une étape manque. Savoir dire
> *où* un raisonnement s'interrompt est une compétence de Terminale à part entière.

---

## Partie 1 — Produit scalaire

> **Rappel.** En repère orthonormé : $u \cdot v = x_u x_v + y_u y_v$. **Le résultat est un nombre.**
> Deux vecteurs non nuls sont orthogonaux **si et seulement si** $u \cdot v = 0$.

**Exercice 1.** $u( - 2 ; 5)$ et $v(4 ; 1)$. Calculer u·v, puis dire si les vecteurs sont
orthogonaux.

$u \cdot v =$ ...........................................  Conclusion : ...........................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Déterminer le réel m pour que $u(3 ; m)$ et $v( - 2 ; 6)$ soient orthogonaux.

Équation posée : ..........................................................................

$m =$ ...........................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** ABC est un triangle avec $A(1 ; 2)$, $B(4 ; 3)$ et $C(2 ; 8)$. Le triangle est-il
rectangle en A ?

Vecteurs à utiliser : ....................................................................

Calcul : ...........................................................................................

Conclusion : ......................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

### Ce que la Terminale en fera

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

## Partie 2 — Probabilités

> **Rappels.**
> $P(A \cap B) = P(A) \times P_A(B)$.
> Probabilités totales : $P(B) = P(A) \times P_A(B) + P(\overline{A}) \times P_{\overline{A}}(B)$.
> A et B sont **indépendants** lorsque $P_A(B) = P(B)$.
> Espérance d'une variable aléatoire : $E(X) = \sum x_i \times P(X = x_i)$.

**Exercice 4.** Une urne contient 3 boules rouges et 2 boules noires. On tire deux boules
successivement, **sans remise**. Construire l'arbre pondéré, puis calculer la probabilité de
tirer deux boules rouges.

Arbre :

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

P(deux rouges) $=$ ...........................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 5.** Deux événements A et B de probabilités non nulles sont **incompatibles**.
Peuvent-ils être indépendants ? Justifier en calculant $P_A(B)$.

....................................................................................................

....................................................................................................

**Exercice 6.** Une variable aléatoire X prend les valeurs 0, 1 et 3 avec les probabilités
0,5 ; 0,3 et 0,2. Calculer $E(X)$ et interpréter le résultat.

$E(X) =$ ...........................  Interprétation : ...........................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Ce que la Terminale en fera

> Répéter n fois, de façon indépendante, une même épreuve à deux issues donne un **schéma de
> Bernoulli**. Le nombre de succès suit alors la **loi binomiale** de paramètres n et p, dont
> l'espérance vaut np.
>
> La **loi des grands nombres** justifiera ensuite pourquoi la moyenne observée sur beaucoup
> de répétitions se rapproche de l'espérance.

---

## Partie 3 — Python

**Exercice 7.** Compléter le programme suivant pour qu'il renvoie le terme de rang n d'une
suite géométrique de premier terme v0 et de raison q.

```python
def terme_geometrique(v0, q, n):
    v = ..........
    for _ in range(..........):
        v = ..........
    return v
```

Tester avec `terme_geometrique(2, 3, 4)`. Le résultat doit valoir : ...........................

**Exercice 8.** Ce programme cherche le premier rang à partir duquel la suite dépasse un
seuil.

```python
def premier_rang_depassement(v0, q, seuil):
    v = v0
    n = 0
    while v <= seuil:
        v = q * v
        n = n + 1
    return n
```

a) Que renvoie `premier_rang_depassement(2, 3, 100)` ? ...........................

b) Que se passe-t-il si $q = 0{,}5$ et seuil = 100, avec $v0 = 2$ ? Pourquoi ?

....................................................................................................

....................................................................................................

c) Quel lien avec le sens de variation vu en séance 1 ?

....................................................................................................

....................................................................................................

## Partie 3 bis — Exercices 9 et 10, piste Excellence

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

## Partie 4 — Bilan du stage

**Ce que j'ai corrigé pendant ce stage :** ..................................................

....................................................................................................

**Ce qui reste fragile :** ..................................................................

....................................................................................................

**Ma certitude générale en mathématiques, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Mon plan pour les quatre premières semaines de septembre** (à reporter dans mon livret) :

| Semaine | Ce que je travaille |
|---:|---|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
