# Terminale Spécialité Mathématiques — Séance 5 — Cartes d'aide
## Produit scalaire, probabilités, Python

---

### Carte A — Rappel de propriété

> **Produit scalaire.** En repère orthonormé : u·v = x_u x_v + y_u y_v. Le résultat est un
> nombre. u et v non nuls sont orthogonaux ⟺ u·v = 0.
>
> **Probabilités.** P(A ∩ B) = P(A) × P_A(B). A et B indépendants ⟺ P_A(B) = P(B).
> E(X) = Σ x_i × P(X = x_i).
>
> **Python.** `range(n)` produit n valeurs : 0, 1, …, n−1.

---

### Carte B — Première étape faite

> **Produit scalaire.** Pour montrer que ABC est rectangle en A, avec A(1 ; 2), B(4 ; 3),
> C(2 ; 8) : les vecteurs à utiliser sont **AB(3 ; 1)** et **AC(1 ; 6)**.
>
> À toi : calcule AB·AC et conclus.
>
> **Probabilités.** Pour l'urne à 3 rouges et 2 noires, la probabilité de la première branche
> « rouge » est **3/5**.
>
> À toi : que devient la composition de l'urne après ce tirage sans remise ?

---

### Carte C — Exemple résolu à transposer

> **Exemple — détermination d'un paramètre.**
> Pour quel réel k les vecteurs u(4 ; k) et v(3 ; −6) sont-ils orthogonaux ?
> Le critère u·v = 0 s'écrit : 4 × 3 + k × (−6) = 0, soit 12 − 6k = 0, donc **k = 2**.
> Contrôle : u(4 ; 2) et v(3 ; −6) donnent 12 − 12 = 0 ✓
>
> **À toi de transposer** en gardant les trois étapes : écrire le critère comme une équation,
> résoudre, contrôler.

---

### Carte D — Découpage en trois questions

> **Pour un triangle rectangle :**
> 1. Quels sont les deux vecteurs qui partent du sommet supposé rectangle ?
> 2. Quelles sont leurs coordonnées (extrémité moins origine) ?
> 3. Leur produit scalaire est-il nul ?
>
> **Pour un arbre pondéré :**
> 1. Quelles sont les probabilités du premier niveau ?
> 2. Que devient la situation après le premier tirage ?
> 3. Pour un chemin complet, on **multiplie** les probabilités rencontrées.

---

### Carte E — Corrigé partiel à compléter

> **Orthogonalité avec paramètre.** u(3 ; m) et v(−2 ; 6).
> Le critère s'écrit : 3 × ( ......... ) + m × ( ......... ) = 0.
> Soit ......... + 6m = 0, donc m = ......... .
> Contrôle : u( ......... ; ......... )·v(−2 ; 6) = ......... ✓
>
> **Python.**
> ```python
> def terme_geometrique(v0, q, n):
>     v = .........
>     for _ in range(.........):
>         v = ......... * v
>     return v
> ```

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> - Mon produit scalaire est bien un **nombre**.
> - J'ai vérifié le signe avec l'angle : positif ⟹ aigu, nul ⟹ droit, négatif ⟹ obtus.
> - Sur un arbre, la somme des probabilités partant d'un même nœud vaut 1.
> - Mon programme donne le même résultat que mon calcul à la main sur un cas simple.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> 1. Annoncer un **vecteur** comme résultat d'un produit scalaire.
> 2. Prendre les coordonnées des points au lieu de celles des vecteurs.
> 3. Confondre P(A ∩ B) et P_A(B) : la conditionnelle est **sur** la branche, l'intersection
>    est **au bout** du chemin.
> 4. Confondre indépendance et incompatibilité.
> 5. Décaler les bornes d'une boucle : `range(n)` fait n tours, pas n + 1.
