# Terminale Spécialité Mathématiques — Séance 2 — Supports de manipulation
## Fonction exponentielle

## Support 1 — Table de test numérique (confrontation)

À projeter vierge et à compléter collectivement. C'est le cœur de la phase de confrontation.

| x | e^(2x) / e^(x−1) | e^(3x−1) | e^(x+1) | Les trois coïncident-elles ? |
|---:|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 0 | | | | |

*Réponses pour le professeur :*

| x | e^(2x)/e^(x−1) | e^(3x−1) | e^(x+1) |
|---:|---|---|---|
| 1 | e² ≈ 7,39 | e² ≈ 7,39 | e² ≈ 7,39 |
| 2 | e³ ≈ 20,09 | e⁵ ≈ 148,4 | e³ ≈ 20,09 |
| 0 | e ≈ 2,72 | e^(−1) ≈ 0,368 | e ≈ 2,72 |

**Point à faire émerger.** En x = 1, les deux réponses coïncident : ce test ne prouve rien.
C'est en x = 2 ou en x = 0 que la contradiction apparaît. Un contre-exemple mal choisi ne
réfute rien — c'est un geste à conserver pour toute l'année.

## Support 2 — Cartes « vrai ou faux » (reconstruction)

Huit cartes à découper, à trier en deux tas : VRAI / FAUX. Chaque carte fausse doit être
retournée et corrigée au dos par l'élève.

| Carte | Énoncé | Verdict |
|---:|---|---|
| 1 | e^a × e^b = e^(a+b) | VRAI |
| 2 | e^a + e^b = e^(a+b) | FAUX — il n'existe pas de règle pour une somme d'exponentielles |
| 3 | e^a / e^b = e^(a−b) | VRAI |
| 4 | e^a / e^b = e^(a/b) | FAUX — on soustrait les exposants, on ne les divise pas |
| 5 | e^(−a) = 1/e^a | VRAI |
| 6 | e^(−a) = −e^a | FAUX — l'exponentielle est toujours strictement positive |
| 7 | (e^a)^n = e^(na) | VRAI |
| 8 | e^(x²) = (e^x)² | FAUX — (e^x)² = e^(2x), et x² ≠ 2x sauf en 0 et en 2 |

**Usage.** Faire trier en binôme, puis mettre en commun. Les cartes 2, 4, 6 et 8 sont les
quatre erreurs à cibler ; la carte 8 est la plus subtile — la faire tester en x = 3.

## Support 3 — Allure de la courbe (stricte positivité)

Tracer, ou faire tracer, l'allure de la courbe de la fonction exponentielle :

```
        │        /
        │      /
        │    /
      1 ┼──/
        │/
  ──────┼────────────────
        │        l'axe des abscisses est une asymptote :
        │        la courbe s'en approche mais ne le touche jamais
```

Faire formuler la conclusion par les élèves : *la courbe ne coupe jamais l'axe des
abscisses, donc l'équation e^x = 0 n'a pas de solution.*

## Support 4 — Tableau de correspondance exp / ln (ouverture Terminale)

À distribuer vierge dans la colonne de droite, à compléter par les élèves en fin de séance.

| Règle sur exp | Règle correspondante sur ln |
|---|---|
| exp(a + b) = exp(a) × exp(b) | |
| exp(a − b) = exp(a) / exp(b) | |
| exp(na) = (exp(a))^n | |
| exp(x) > 0 pour tout réel x | |

## Support 5 — Affiche de séance

> **Avant de simplifier une exponentielle :**
> 1. J'identifie l'opération : produit, quotient, puissance ?
> 2. J'écris la règle correspondante.
> 3. Je pose la parenthèse autour de l'exposant soustrait.
> 4. Je teste sur une valeur numérique — et pas sur x = 1.
>
> **Et je n'oublie jamais : e^x > 0, toujours.**

## Matériel à prévoir

- Un jeu de huit cartes par binôme.
- Une calculatrice par élève, pour les tests numériques uniquement.
- Le tableau de correspondance exp/ln, un par élève.
