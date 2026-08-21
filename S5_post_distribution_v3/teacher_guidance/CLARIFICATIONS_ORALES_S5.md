# Clarifications orales — séance 5

**Document strictement enseignant.** Il ne remplace aucun livret et ne corrige aucun
document déjà distribué. Les livrets et les évaluations imprimés restent tels quels.

Deux usages, et deux seulement.

- **Si la séance n'a pas encore eu lieu pour un élève** : les formulations ci-dessous
  peuvent être dites oralement, au moment où le passage concerné est abordé. Il ne
  s'agit pas de corriger le document devant l'élève, mais d'éviter qu'une formulation
  trop absolue s'installe comme une règle fausse.
- **Si la séance a déjà eu lieu** : ne chercher aucune correction rétroactive auprès de
  l'élève. Les approximations relevées ici sont consignées dans l'analyse sous
  `evidence_quality: limited_by_prompt` ou `interpretation_limit`, et le bilan respecte
  cette limite. Rien d'autre.

Chaque point cite d'abord ce qui est écrit dans le support, puis ce qu'il faut dire.

---

## 1. Équation produit nul — module `M2DE_EQ_02`

**Ce qui est écrit dans le rappel du module :**

> « Une équation sous forme factorisée ne doit donc **jamais** être développée. »

**Pourquoi c'est trop absolu.** Développer une équation-produit est mathématiquement
licite. Développer `(2x−6)(x+5)=0` conduit à `2x²+4x−30=0`, équation équivalente, dont
les solutions sont les mêmes. La voie est plus longue, et en Seconde elle ne dispose
d'aucun outil de résolution ; elle n'est pas fausse pour autant.

**À dire :**

> « Dans cette situation, conserver la forme factorisée est la stratégie la plus
> efficace : elle permet d'appliquer directement la propriété du produit nul.
> Développer resterait mathématiquement possible, mais serait moins pertinent — et,
> en Seconde, sans outil pour résoudre l'équation obtenue. »

**Conséquence sur la correction.** Un élève qui développe puis résout correctement
obtient les points. On coche `accepted_alternative_method` et on écrit une observation
de stratégie. Aucun code `CONCEPT` : le raisonnement est valide.

---

## 2. Somme de deux carrés — module `M1RE_ALG_02`

**Ce qui est écrit dans le rappel du module :**

> « Une **somme** de deux carrés ne se factorise pas dans ℝ. »

**Pourquoi c'est inexact.** L'énoncé est faux tel qu'il est écrit. `x⁴+4` est une somme
de deux carrés, et elle se factorise dans ℝ : `x⁴+4 = (x²−2x+2)(x²+2x+2)`. Ce qui est
vrai, c'est qu'il n'existe pas d'identité réelle analogue à `a²−b² = (a−b)(a+b)`
transformant directement `a²+b²` en un produit de deux facteurs linéaires réels non
constants.

**À dire :**

> « Il n'existe pas d'identité réelle analogue à la différence de deux carrés
> permettant de transformer directement `a²+b²` en un produit de deux facteurs
> linéaires réels non constants. »

Et, si un élève pose la question : `x²+9` n'a pas de racine réelle, donc pas de
factorisation en deux facteurs du premier degré à coefficients réels. C'est cet énoncé
précis qui est utile, pas l'énoncé général.

**Le corrigé de l'exercice concerné reste exact** : « c'est une somme de carrés,
strictement positive pour tout réel `x`, elle n'admet aucune racine réelle. » Seule la
règle générale du rappel est à reformuler.

---

## 3. Coefficient directeur et droites parallèles

**Ce qui est écrit** dans le corrigé d'un item de Première : « oui, les deux droites ont
le même coefficient directeur ».

**Ce qu'il faut préciser.**

- Deux droites **non verticales** sont parallèles si et seulement si elles ont le même
  coefficient directeur.
- Le coefficient directeur **n'est pas défini** pour une droite verticale : une droite
  d'équation `x = c` n'a pas d'équation réduite de la forme `y = mx + p`.
- Deux droites verticales sont parallèles entre elles, sans que la notion de
  coefficient directeur intervienne.

**Conséquence sur la correction.** Aucune : les configurations proposées ne contiennent
pas de droite verticale. La précision est à donner à l'oral pour que la règle installée
soit exacte.

---

## 4. `range(a, b, p)` en Python — module `NSI1_BOUCLE_01`

**Ce qui est écrit dans le rappel du module :**

> « `range(a, b, p)` avance de `p` en `p` en s'arrêtant avant `b`. »

**Ce qu'il faut préciser.**

- `p` ne peut pas valoir `0` : `range(a, b, 0)` lève une `ValueError`.
- Si `p > 0`, la progression est croissante et s'arrête avant `b` ; la suite est vide
  si `a >= b`.
- Si `p < 0`, la progression est décroissante et s'arrête également avant `b` ; la suite
  est vide si `a <= b`.
- Dans tous les cas, la borne finale `b` n'est **jamais** incluse.

**À dire :**

> « Le pas peut être négatif : la progression est alors décroissante. Le pas ne peut pas
> être nul. Et dans les deux sens, la borne d'arrivée n'est jamais atteinte. »

---

## 5. Variant de boucle — module `NSI1_ACC_01`

**Ce qui est écrit dans le rappel du module :**

> « **Variant :** quantité entière positive qui décroît et garantit l'arrêt. »

**Ce qu'il faut préciser.** « Positive » et « décroît » sont trop vagues : une quantité
positive qui décroît peut décroître indéfiniment sans jamais s'arrêter si elle n'est pas
entière, et une décroissance non stricte ne garantit rien.

**À dire :**

> « Un variant est une quantité à valeurs entières naturelles — ou du moins entières et
> minorées — qui décroît **strictement** à chaque tour tant que la boucle continue.
> Comme elle est minorée et strictement décroissante dans les entiers, elle ne peut pas
> décroître indéfiniment : la boucle s'arrête. »

Le variant donné dans le corrigé — « le nombre de valeurs restant à parcourir, qui
décroît d'une unité par tour » — satisfait exactement cette définition. C'est la
définition générale du rappel qui est à resserrer, pas l'exemple.

---

## 6. `assert f(2) is not None` — module `NSI1_TEST_01`

**Ce qui est écrit dans un corrigé du module :**

> « `assert f(2) is not None` : une fonction qui se contente d'afficher renvoie `None`
> et fait échouer l'assertion. »

**Ce qu'il faut préciser.** L'assertion ne teste pas le contrat de la fonction. Elle
distingue seulement, et seulement dans certains cas, une fonction qui renvoie quelque
chose d'une fonction qui se contente d'afficher :

- une fonction qui renvoie une valeur **fausse** passe le test ;
- une fonction dont le contrat est précisément de renvoyer `None` échoue le test alors
  qu'elle est correcte ;
- une fonction correcte qui renvoie `0`, `False` ou la liste vide passe ce test — mais
  échouerait un test écrit `assert f(2)`, ce qui montre bien qu'on ne teste pas la même
  chose.

**À dire :**

> « Cette assertion sert à repérer un `print` conservé à la place d'un `return`. Ce
> n'est pas un test de correction : pour tester le contrat, il faut comparer à la valeur
> attendue, par exemple `assert moyenne([4, 6]) == 5.0`. »

---

## 7. Mise au point curriculaire — entrée en Seconde

**Ce qui est écrit** dans le livret de phase 4 des élèves entrant en Seconde :

> « Ce qui est nouveau : la notation en intervalle et le vocabulaire fonctionnel. »

**Ce qui est inexact.** La notion de fonction, l'image, l'antécédent et la notation
`f(x)` appartiennent déjà à la progression de **Troisième**. Le livret de phase 4 des
élèves entrant en Troisième le dit d'ailleurs lui-même, en présentant le statut de
fonction comme une nouveauté de Troisième. Les deux livrets ne peuvent pas avoir raison
en même temps.

**Ce qui est réellement nouveau en Seconde** : la notation en intervalle, ainsi que
certains approfondissements et certaines notations propres à la classe de Seconde
(ensemble de définition, tableau de variations, courbe représentative comme objet
d'étude).

**À dire, si la séance n'a pas eu lieu :**

> « Le vocabulaire des fonctions — image, antécédent, `f(x)` — n'est pas nouveau : tu
> l'as rencontré en Troisième. Ce qui est nouveau ici, c'est la notation en intervalle,
> et la place beaucoup plus centrale que les fonctions vont prendre. »

**Ce qui a été corrigé.** La métadonnée seulement : `curriculum_scope` ne classe aucun
critère de fonction en `bridge_n` pour les élèves entrant en Seconde, et la mise au
point figure dans `curriculum_scope/curriculum_references.json`. Le livret distribué
n'est pas modifié. Cette question n'a d'ailleurs aucun effet sur les scores : aucun
critère de l'évaluation de Seconde ne porte sur le langage fonctionnel.

---

## 8. Ce que ce document ne fait pas

Il ne rouvre aucune correction déjà rendue. Il ne demande à aucun élève de refaire quoi
que ce soit. Il ne modifie aucun point, aucun barème, aucun identifiant.

Les six premiers points portent sur des supports de séance ; le septième sur une
métadonnée. Aucun n'affecte le score d'un élève, à une exception près, déjà traitée dans
les overlays de correction : une équation-produit développée puis résolue correctement
doit être créditée intégralement.
