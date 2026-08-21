# Terminale NSI — Séance 1 — Cartes d'aide
## Représentation des données et booléens

---

### Carte A — Rappel de syntaxe et de propriété

> Puissances de 2 : 128, 64, 32, 16, 8, 4, 2, 1.
> Hexadécimal : A = 10, B = 11, C = 12, D = 13, E = 14, F = 15.
> Un chiffre hexadécimal = quatre bits.
> Priorités booléennes : `not`, puis `and`, puis `or`.
> De Morgan : `not (A and B)` = `(not A) or (not B)`.

---

### Carte B — Première ligne écrite

> Pour convertir **45** en binaire par divisions successives :
> ```
> 45 = 2 × 22 + 1
> ```
> À toi de continuer : divise 22 par 2, puis le quotient obtenu, jusqu'à 0.
> Les restes se lisent **de bas en haut**.

---

### Carte C — Exemple exécuté à transposer

> **Exemple.** Convertir 37 en binaire.
> Puissances utiles : 32 + 4 + 1 = 37.
> On place un 1 sous 32, 4 et 1, un 0 ailleurs :
>
> | 32 | 16 | 8 | 4 | 2 | 1 |
> |---:|---:|---:|---:|---:|---:|
> | 1 | 0 | 0 | 1 | 0 | 1 |
>
> Résultat : **100101**.
> **Vérification :** 32 + 0 + 0 + 4 + 0 + 1 = 37 ✓
>
> **À toi de transposer**, en gardant les trois étapes : décomposition, écriture,
> vérification.

---

### Carte D — Découpage en trois questions

> 1. Quelle est la plus grande puissance de 2 inférieure ou égale à ton nombre ?
> 2. Soustrais-la, puis recommence avec ce qui reste, jusqu'à 0.
> 3. Écris un 1 sous chaque puissance utilisée, un 0 sous les autres — sans en oublier.
>
> Puis vérifie : additionne les puissances marquées d'un 1.

---

### Carte E — Squelette de code à compléter

> ```python
> def valeur_decimale(chaine_binaire):
>     total = 0
>     for bit in chaine_binaire:
>         total = total * ....... + int(bit)
>     return total
>
> # Tests attendus
> # valeur_decimale('10110') doit valoir .......
> # valeur_decimale('1111')  doit valoir .......
> ```

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> - J'ai recalculé la valeur décimale de mon écriture binaire.
> - Je retombe bien sur l'entier de départ.
> - Pour l'hexadécimal, j'ai vérifié que F vaut 15 et non 16.
> - Pour une expression booléenne, j'ai parenthésé avant d'évaluer.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> 1. Lire les restes **de haut en bas** au lieu de bas en haut.
> 2. Oublier un 0 intermédiaire dans l'écriture binaire.
> 3. Prendre F pour 16 : F vaut **15**.
> 4. Écrire `not (A and B)` comme `(not A) and (not B)` — c'est `or` qu'il faut.
> 5. Évaluer une expression booléenne de gauche à droite sans respecter la priorité de `not`.
