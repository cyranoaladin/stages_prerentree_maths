# Terminale NSI — Séance 1 — Fiche élève
## Représentation des données et booléens

**Ton objectif de séance :** savoir convertir entre les bases 2, 10 et 16 — et savoir
**vérifier** ta conversion toute seule, en une ligne.

### Règle de travail

- Je prédis avant d'exécuter ou de calculer.
- Je vérifie toute conversion en recalculant la valeur décimale.
- Certitude : ☐1 ☐2 ☐3 ☐4 · Aide : A, B, C, D ou E.

---

## Partie 1 — Avant tout : ta réponse spontanée

**Question 0.** Écris l'entier 22 en binaire.

Ma réponse : ..................................................  Ma certitude : ☐1 ☐2 ☐3 ☐4

Vérification — recalcule la valeur décimale de **ta** réponse :

....................................................................................................

Est-ce que tu retombes sur 22 ? ☐oui ☐non

---

## Partie 2 — La trace écrite

> **Base 2 — méthode 1 : puissances de 2.**
>
> | 2⁷ | 2⁶ | 2⁵ | 2⁴ | 2³ | 2² | 2¹ | 2⁰ |
> |---:|---:|---:|---:|---:|---:|---:|---:|
> | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
>
> 22 = 16 + 4 + 2 → **10110**.
>
> **Base 2 — méthode 2 : divisions successives.** On divise par 2 et on lit les restes
> **de bas en haut**.
>
> **Base 16.** A = 10, B = 11, C = 12, D = 13, E = 14, **F = 15**.
> 0x2A = 2 × 16 + 10 = 42. Et 60 = 3 × 16 + 12 = 0x3C.
>
> **Le contrôle, toujours le même :** je recalcule la valeur décimale de ce que j'ai écrit.

---

## Partie 3 — Entraînement

### Parcours consolidation (exercices 1 à 4)

**Exercice 1.** Écris 22 en binaire, puis vérifie en recalculant.

Écriture : ....................  Vérification : ....................

Certitude : ☐1 ☐2 ☐3 ☐4   Aide : ☐A ☐B ☐C ☐D ☐E

**Exercice 2.** Écris 45 en binaire par la méthode des divisions successives.

```
45 = 2 × ....... + .......
....... = 2 × ....... + .......
....... = 2 × ....... + .......
....... = 2 × ....... + .......
....... = 2 × ....... + .......
....... = 2 × ....... + .......
```

Lecture de bas en haut : ....................  Vérification : ....................

**Exercice 3.** Convertis 0x2A en base 10, puis convertis 60 en hexadécimal.

0x2A = ....................    60 = ....................

Certitude : ☐1 ☐2 ☐3 ☐4   Aide : ☐A ☐B ☐C ☐D ☐E

**Exercice 4.** Combien de valeurs différentes peut-on coder sur 8 bits ? Quelle est la plus
grande, écrite en base 10 ?

....................................................................................................

### Parcours maîtrise (exercices 3 à 6)

**Exercice 5.** Convertis 0xFF en base 10 et en binaire. Que remarques-tu sur l'écriture
binaire ?

....................................................................................................

**Exercice 6.** Convertis 1011 0110 (binaire) en hexadécimal **sans passer par la base 10**.
Explique ta méthode.

....................................................................................................

....................................................................................................

### Parcours approfondissement (exercices 6 à 8)

**Exercice 7.** Explique pourquoi un chiffre hexadécimal correspond exactement à quatre bits.
En quoi cela rend-il la conversion binaire ↔ hexadécimal immédiate ?

....................................................................................................

....................................................................................................

**Exercice 8.** Sur 8 bits en complément à deux, comment représente-t-on les entiers
négatifs ? Quelle est la plage de valeurs représentables ?

....................................................................................................

....................................................................................................

---

## Partie 4 — Booléens

> **Priorités :** `not` d'abord, puis `and`, puis `or`.

**Exercice 9.** Que vaut `(not True) or (False and True)` ? Détaille l'ordre d'évaluation.

....................................................................................................

**Exercice 10.** Complète la table de vérité.

| A | B | A and B | not(A and B) | (not A) or (not B) |
|---|---|---|---|---|
| V | V | | | |
| V | F | | | |
| F | V | | | |
| F | F | | | |

Que remarques-tu sur les deux dernières colonnes ? ..........................................

Cette égalité s'appelle une **loi de De Morgan**. Écris-la avec tes mots :

....................................................................................................

---

## Partie 5 — Ce que la Terminale en fera

> **Invariants de boucle.** Pour démontrer qu'un algorithme est correct, on exhibe une
> propriété vraie à chaque tour de boucle. Cette propriété est une expression booléenne, et
> sa négation est la condition d'arrêt.
>
> **Requêtes SQL.** `WHERE age > 18 AND classe = 'TG3'` est une expression booléenne. Sa
> négation n'est **pas** `age <= 18 AND classe != 'TG3'` — c'est De Morgan qui donne
> l'écriture correcte.
>
> **Sécurisation des communications.** Le chiffrement repose sur l'arithmétique des entiers
> en machine : la représentation binaire y est un outil de tous les jours.

---

## Partie 6 — Bilan de séance

**Ce que j'ai compris aujourd'hui :** ......................................................

....................................................................................................

**Le contrôle que je ferai désormais après chaque conversion :** ............................

....................................................................................................

**Ma certitude sur la représentation binaire, aujourd'hui :** ☐1 ☐2 ☐3 ☐4

**Aide maximale utilisée :** ☐A ☐B ☐C ☐D ☐E ☐aucune
