# Terminale NSI — Séance 1 — Supports pratiques
## Représentation des données et booléens

## Support 1 — Réglette des puissances de 2

Une réglette cartonnée par élève, à conserver dans le portfolio.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.6}
\begin{tabular}{|>{\bfseries}l|*{8}{c|}}\hline
\rowcolor{SoftBlue}
poids & $2^{7}$ & $2^{6}$ & $2^{5}$ & $2^{4}$ & $2^{3}$ & $2^{2}$ & $2^{1}$ & $2^{0}$ \\\hline
valeur & 128 & 64 & 32 & 16 & 8 & 4 & 2 & 1 \\\hline
bit & & & & & & & & \\\hline
\end{tabular}
\end{center}
```

**Usage.** L'élève pose des jetons sur les puissances retenues, puis lit la ligne de 0 et de
1. Le passage du geste à l'écriture est immédiat, et le contrôle — additionner les valeurs
sous les jetons — l'est aussi.

## Support 2 — Cartes binaires (confrontation)

Huit cartes recto-verso : au recto une puissance de 2 (1, 2, 4, 8, 16, 32, 64, 128), au verso
rien. L'élève retourne les cartes dont il a besoin pour composer l'entier demandé.

**Entiers à composer, dans l'ordre :** 5, 13, 22, 45, 100, 255.

*Réponses :* 101 ; 1101 ; 10110 ; 101101 ; 1100100 ; 11111111.

**Point à faire émerger.** 255 nécessite les huit cartes : c'est le plus grand entier
représentable sur 8 bits. La question « combien de valeurs sur 8 bits ? » s'y rattache
naturellement : 256, de 0 à 255.

## Support 3 — Table hexadécimale de référence

À imprimer, une par élève, à conserver dans le portfolio.

| Hex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Déc | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| Bin | 0000 | 0001 | 0010 | 0011 | 0100 | 0101 | 0110 | 0111 | 1000 | 1001 | 1010 | 1011 | 1100 | 1101 | 1110 | 1111 |

**Point à faire émerger.** La troisième ligne montre qu'un chiffre hexadécimal vaut
exactement **quatre bits**. La conversion binaire $\leftrightarrow$ hexadécimal se fait donc par paquets de
quatre, sans passer par la base 10 : $1011 0110 \to B6$.

## Support 4 — Vérification en Python

À exécuter en fin de partie 3, pour installer le réflexe de contrôle.

```python
# Conversion et verification
print(bin(22))       # 0b10110
print(int('10110', 2))   # 22
print(hex(42))       # 0x2a
print(int('2A', 16)) # 42

# Verifier soi-meme une ecriture binaire
def valeur_decimale(chaine_binaire):
    total = 0
    for bit in chaine_binaire:
        total = total * 2 + int(bit)
    return total

print(valeur_decimale('10110'))  # 22
```

**Usage.** Faire écrire la fonction `valeur_decimale` par les élèves du parcours maîtrise,
puis l'utiliser comme vérificateur pour tout le groupe. Le fait de construire soi-même son
outil de contrôle est ce qui rend le contrôle durable.

## Support 5 — Cartes booléennes à trier

Six cartes portant une expression. L'élève les trie en deux tas : VRAI / FAUX. Les cartes
fausses sont retournées et corrigées au dos.

| Carte | Expression | Verdict |
|---:|---|---|
| 1 | `True and not False` vaut `True` | VRAI |
| 2 | `(not True) or (False and True)` vaut `True` | FAUX — vaut `False` |
| 3 | `not (A and B)` équivaut à `(not A) or (not B)` | VRAI (De Morgan) |
| 4 | `not (A and B)` équivaut à `(not A) and (not B)` | FAUX |
| 5 | `A or B` est faux uniquement si A et B sont tous deux faux | VRAI |
| 6 | `A and B` est vrai dès que l'un des deux est vrai | FAUX — il faut les deux |

## Support 6 — Affiche de séance

> **Après chaque conversion, je vérifie :**
> je recalcule la valeur décimale de ce que j'ai écrit.
> Si je ne retombe pas sur l'entier de départ, c'est faux.
>
> **$F = 15$**, pas 16.
> **Les restes se lisent de bas en haut.**
> **`not` d'abord, puis `and`, puis `or`.**

## Matériel à prévoir

- Une réglette et un lot de jetons par élève.
- Un jeu de huit cartes binaires par binôme.
- La table hexadécimale de référence, une par élève.
- Un jeu de six cartes booléennes par binôme.
- Un poste avec Python par binôme.
