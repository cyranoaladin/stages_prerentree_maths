# Terminale Spécialité Mathématiques — Évaluation finale (Corrigé et grille de lecture)

## Principe de lecture

Cette évaluation **n'est pas notée**. Elle est dépouillée avec la matrice réussite $\times$
confiance, exactement comme le positionnement initial. Ce que l'on mesure est le
**déplacement** de chaque élève dans cette matrice entre le début et la fin du stage.

| | Certitude faible (1-2) | Certitude forte (3-4) |
|---|---|---|
| **Réponse fausse** | Notion absente | Conception erronée |
| **Réponse juste** | Acquis fragile | Acquis disponible |

Un élève qui passe d'une case « conception erronée » à une case « acquis fragile » a
progressé, même si sa réponse n'est pas encore assurée : c'est le déplacement le plus
important du stage.

---

## Corrigé

### Exercice 1 — Suites numériques

a) $u_1 = u_0 + 2 \times 0 - 1 = 3 - 1 =$ **2** ; $u_2 = 2 + 2 \times 1 - 1 =$ **3** ; $u_3 = 3 + 2 \times 2 - 1 =$ **6**.

b) $u_{n+1} - u_n =$ **$2n - 1$**. Pour $n \geqslant 1$, on a $2n - 1 \geqslant 1 > 0$ : la suite est **strictement
croissante à partir du rang 1**. (Entre les rangs 0 et 1, la différence vaut $- 1$ : la suite
décroît d'abord, ce qui explique la précision « à partir du rang 1 » de l'énoncé.)

c) **Non.** L'écart $2n - 1$ dépend de n : il n'est pas constant. Une suite arithmétique a un
écart constant.

*Ce qui est visé.* Le calcul systématique de la différence, acquis en séance 1. La question c)
teste la distinction entre suite arithmétique et suite définie par récurrence.

*Piège volontaire.* La différence change de signe entre les rangs 0 et 1. Un élève qui répond
« croissante » sans restriction n'a pas étudié le signe pour toutes les valeurs de n :
réussite partielle.

### Exercice 2 — Fonction exponentielle

a) $e^{4x} \times e^{2 - x} = e^{4x + 2 - x} = e^{3x+2}$. Puis division par $e^{2x}$ :
$e^{3x + 2 - 2x} =$ **$e^{x+2}$**.

b) La fonction exponentielle est strictement positive sur $\mathbb{R}$ : **aucune solution**.

c) $e^{2x} = e^{x+4}$ équivaut à $2x = x + 4$ (l'exponentielle est strictement croissante donc
injective), soit **$x = 4$**.

*Ce qui est visé.* Les deux erreurs de la séance 2 : addition des exposants dans une division,
et solution attribuée à une exponentielle nulle.

*Contrôle attendu.* Test numérique en $x = 1$ : $e^4 \times e^1 / e^2 = e^3$ et $e^{1+2} = e^3 \checkmark$

### Exercice 3 — Second degré

a) $\Delta = 25 - 4 \times ( - 1) \times ( - 6) = 25 - 24 =$ **1**. Racines : $( - 5 \pm 1)/( - 2)$, soit
$( - 5 + 1)/( - 2) =$ **2** et $( - 5 - 1)/( - 2) =$ **3**.
Contrôle : somme $5 = - b/a = - 5/( - 1) \checkmark$ ; produit $6 = c/a = - 6/( - 1) \checkmark$

b) **$a = - 1 < 0$** : le trinôme est négatif à l'extérieur des racines, positif entre elles.

| | $- \infty$ | | 2 | | 3 | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de $P(x)$ | | $-$ | 0 | + | 0 | $-$ | |

c) L'inégalité est **large** : l'ensemble solution est **[2 ; 3]**, crochets fermés.

*Ce qui est visé.* L'erreur centrale de la séance 3 : appliquer la règle du signe sans
regarder le signe de a. Le coefficient dominant est négatif, comme dans l'item du
positionnement initial.

*Points d'attention au dépouillement.* Un élève qui écrit $] - \infty ; 2] \cup [3 ; + \infty [$ a reproduit
l'erreur initiale ; un élève qui écrit ]2 ; 3[ a le bon raisonnement mais pas les bons
crochets — ce sont deux constats très différents à noter séparément.

### Exercice 4 — Dérivation

a) $u = x - 1$, $u' = 1 ; v = x^2 + 2$, $v' = 2x$.
$f'(x) = 1 \times (x^2 + 2) + (x - 1) \times 2x = x^2 + 2 + 2x^2 - 2x =$ **$3x^2 - 2x + 2$**.

b) Discriminant de f' : $\Delta = 4 - 24 = - 20 < 0$, et le coefficient dominant 3 est positif :
**$f'(x) > 0$ pour tout réel x**. Donc f est **strictement croissante sur $\mathbb{R}$**.

c) **Non.** Le signe de g' donne le sens de variation de g, pas son signe. Contre-exemple :
$g(x) = - x + 10$ a une dérivée strictement négative et reste positive sur ]0 ; 3[.

*Ce qui est visé.* La question b) réinvestit le cas $\Delta < 0$ de la séance 3 dans le contexte de
la séance 4 : c'est le point de jonction des deux séances. La question c) est la reprise
directe de l'item du positionnement initial le plus souvent manqué.

### Exercice 5 — Produit scalaire

a) AB$(3 - 0 ; 2 - 1) =$ **AB(3 ; 1)** et AC$(1 - 0 ; 7 - 1) =$ **AC(1 ; 6)**.

b) AB·AC = $3 \times 1 + 1 \times 6 =$ **9**. Ce produit n'est pas nul : le triangle **n'est pas
rectangle en A**.

c) $w(t ; - 2)$ orthogonal à AB(3 ; 1) : $3t + 1 \times ( - 2) = 0$, soit $3t = 2$ et **$t = 2/3$**.
Contrôle : $w(2/3 ; - 2) \cdot$AB$(3 ; 1) = 2 - 2 = 0 \checkmark$

*Ce qui est visé.* La question a) vérifie que l'élève prend bien les coordonnées des
**vecteurs** et non des points. La question c) est le nouvel usage travaillé en séance 5 : le
critère lu comme une équation.

---

## Grille de dépouillement individuelle

À reporter dans le livret de l'élève, rubrique « Bilan final ».

| Exercice | Domaine | Juste | Faux | Vide | Certitude déclarée | Contrôle effectué | Case de la matrice |
|---:|---|:---:|:---:|:---:|:---:|:---:|---|
| 1 | Suites numériques | $\square$ | $\square$ | $\square$ | ...../4 | $\square$ | |
| 2 | Fonction exponentielle | $\square$ | $\square$ | $\square$ | ...../4 | $\square$ | |
| 3 | Second degré | $\square$ | $\square$ | $\square$ | ...../4 | $\square$ | |
| 4 | Dérivation | $\square$ | $\square$ | $\square$ | ...../4 | $\square$ | |
| 5 | Produit scalaire | $\square$ | $\square$ | $\square$ | ...../4 | $\square$ | |

## Comparaison initiale / finale

| Domaine | Case au positionnement initial | Case à l'évaluation finale | Déplacement |
|---|---|---|---|
| Suites numériques | | | |
| Fonction exponentielle | | | |
| Second degré | | | |
| Dérivation | | | |
| Produit scalaire | | | |

## Indicateurs transversaux

| Indicateur | Constat |
|---|---|
| Nombre de propriétés écrites avant calcul (sur 5) | ....... |
| Nombre de contrôles effectués (sur 5) | ....... |
| Écart moyen entre certitude déclarée et réussite | ....... |
| Aide maximale utilisée en séance 5 | ....... |

## Critères de réussite du stage

Le stage est réussi pour un élève lorsque les cinq conditions suivantes sont réunies :

1. plus aucune case « conception erronée » sur les domaines traités ;
2. au moins trois propriétés écrites avant calcul sur cinq exercices ;
3. au moins trois contrôles effectués sur cinq ;
4. aide maximale utilisée en séance 5 strictement inférieure à celle de la séance 1 ;
5. plan de septembre rempli et argumenté.

---
_Document enseignant. Ne pas diffuser aux élèves avant la fin de l'évaluation._
