# Terminale Spécialité Mathématiques — Séance 2 — Cartes d'aide
## Fonction exponentielle

---

### Carte A — Rappel de propriété

> exp(a) × exp(b) = exp(a + b)
> exp(a) / exp(b) = exp(a − b)
> exp(−a) = 1 / exp(a)
> (exp(a))^n = exp(na)
> Pour tout réel x : exp(x) > 0.

---

### Carte B — Première étape faite

> Pour simplifier e^(3x) × e^(1−x) / e^x :
> le produit du numérateur donne e^(3x + (1 − x)) = **e^(2x+1)**.
>
> À toi : il reste à diviser par e^x. Quelle opération sur les exposants ?

---

### Carte C — Exemple résolu à transposer

> **Exemple.** Simplifier e^(4x) / e^(x−2).
> Division : on soustrait les exposants, avec la parenthèse.
> 4x − (x − 2) = 4x − x + 2 = 3x + 2.
> Donc e^(4x) / e^(x−2) = e^(3x+2).
> **Contrôle en x = 1 :** e⁴/e^(−1) = e⁵ ≈ 148,4 ; e^(3+2) = e⁵ ≈ 148,4. ✓
>
> **À toi de transposer**, en gardant les trois étapes : règle, parenthèse, contrôle.

---

### Carte D — Découpage en trois questions

> 1. L'expression est-elle un produit, un quotient, ou les deux ?
> 2. Écris l'exposant final sous forme d'une somme ou d'une différence, avec toutes les
>    parenthèses.
> 3. Développe cet exposant, puis contrôle sur une valeur numérique différente de 1.

---

### Carte E — Corrigé partiel à compléter

> **e^(5x) / e^(2x+3)**
> Division : on ......................... les exposants.
> Exposant : 5x − ( ......................... ) = 5x − 2x − 3 = ......................... .
> Résultat : e^( ......................... ).
> Contrôle en x = 2 : e^10 / e^7 = e^....... et e^(3×2−3) = e^....... . ✓

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> Avant de déclarer une certitude de 4 :
> - je choisis une valeur numérique **autre que 0 et 1** ;
> - je calcule l'expression de départ et ma réponse ;
> - je vérifie qu'elles coïncident.
>
> Si elles coïncident pour une seule valeur, ce n'est pas une preuve — mais si elles
> diffèrent, c'est une réfutation certaine.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> **Les quatre pièges de ce chapitre :**
> 1. additionner les exposants dans une division ;
> 2. oublier la parenthèse : 2x − (x − 1) vaut x + 1, pas x − 1 ;
> 3. donner une solution à e^x = 0 — il n'y en a aucune ;
> 4. écrire e^(x²) = (e^x)² — c'est faux dès que x ∉ {0 ; 2}.
