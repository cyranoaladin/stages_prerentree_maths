# Terminale NSI — Séance 1 — Fiche élève
## Représentation des données et booléens

**Ton objectif de séance :** savoir convertir entre les bases 2, 10 et 16 — et savoir
**vérifier** ta conversion toute seule, en une ligne.

### Règle de travail

- Je prédis avant d'exécuter ou de calculer.
- Je vérifie toute conversion en recalculant la valeur décimale.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Partie 1 — Avant tout : ta réponse spontanée

**Question 0.** Écris l'entier 22 en binaire.

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Vérification — recalcule la valeur décimale de **ta** réponse :

....................................................................................................

Est-ce que tu retombes sur 22 ? $\square$oui $\square$non

---

## Partie 2 — La trace écrite

> **Base 2 — méthode 1 : puissances de 2.**
>
> | $2^7$ | $2^6$ | $2^5$ | $2^4$ | $2^3$ | $2^2$ | $2^1$ | $2^0$ |
> |---:|---:|---:|---:|---:|---:|---:|---:|
> | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
>
> $22 = 16 + 4 + 2 \to$ **10110**.
>
> **Base 2 — méthode 2 : divisions successives.** On divise par 2 et on lit les restes
> **de bas en haut**.
>
> **Base 16.** $A = 10$, $B = 11$, $C = 12$, $D = 13$, $E = 14$, **$F = 15$**.
> $0x2A = 2 \times 16 + 10 = 42$. Et $60 = 3 \times 16 + 12 = 0x3C$.
>
> **Le contrôle, toujours le même :** je recalcule la valeur décimale de ce que j'ai écrit.

---

## Partie 3 — Entraînement

### Comment tu trouves ton parcours

Ton livret individuel porte, pour cette séance, une **posture** et un **parcours**. Le tableau
ci-dessous dit ce que tu traites. Tu ne fais pas les huit exercices : tu fais les tiens, et tu
les fais entièrement.

| Ta posture du jour | Ce que tu traites | Ce qu'on attend de toi |
|---|---|---|
| **DIAGNOSTIQUER** — tu avais laissé ce domaine sans réponse | Question 0, puis exercices 1 et 2 | Répondre même sans être sûr : déclarer une certitude de 1 est une réponse, pas un aveu |
| **CONFRONTER** — tu t'es trompé en étant sûr de toi | Question 0, puis exercices 1 à 4 | Écrire ce que tu croyais, puis ce qui l'a mis en défaut |
| **INSTALLER** — il te manque quelque chose, et tu le sais | Exercices 1 à 4 | Exécuter avant de conclure, et écrire la table de trace |
| **CONSOLIDER** — tu réussis, sans en être sûr | Exercices 3 à 6 | Spécifier la fonction et écrire ses tests, sans carte d'aide |
| **ENTRETENIR** — c'est acquis et assumé | Exercices 6 à 8 | Justifier le choix d'algorithme par son coût, pas par le temps mesuré |

### Exercices 1 à 4 — pistes Diagnostiquer, Confronter et Installer

**Exercice 1.** Écris 22 en binaire, puis vérifie en recalculant.

Écriture : ....................  Vérification : ....................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Écris 45 en binaire par la méthode des divisions successives.

```{=latex}
\begin{center}
$\begin{aligned}
45 &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt} \\[2.2mm]
\rule{16mm}{0.3pt} &= 2 \times \rule{16mm}{0.3pt} + \rule{8mm}{0.3pt}
\end{aligned}$
\end{center}
```

Lecture de bas en haut : ....................  Vérification : ....................

**Exercice 3.** Convertis 0x2A en base 10, puis convertis 60 en hexadécimal.

$0x2A =$ ....................    $60 =$ ....................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Combien de valeurs différentes peut-on coder sur 8 bits ? Quelle est la plus
grande, écrite en base 10 ?

....................................................................................................

### Exercices 3 à 6 — piste Consolider

**Exercice 5.** Convertis 0xFF en base 10 et en binaire. Que remarques-tu sur l'écriture
binaire ?

....................................................................................................

**Exercice 6.** Convertis 1011 0110 (binaire) en hexadécimal **sans passer par la base 10**.
Explique ta méthode.

....................................................................................................

....................................................................................................

### Exercices 6 à 8 — piste Entretenir

**Exercice 7.** Explique pourquoi un chiffre hexadécimal correspond exactement à quatre bits.
En quoi cela rend-il la conversion binaire $\leftrightarrow$ hexadécimal immédiate ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 8.** Sur 8 bits en complément à deux, comment représente-t-on les entiers
négatifs ? Quelle est la plage de valeurs représentables ?

....................................................................................................

....................................................................................................

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

**Ma certitude sur la représentation binaire, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Aide maximale utilisée :** $\square$A $\square$B $\square$C $\square$D $\square$E $\square$aucune
