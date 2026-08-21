# Terminale NSI — Séance 1 — Fiche professeur
## Représentation des données et booléens

**Durée :** 2 heures · **Effectif :** 5 élèves · **Source pédagogique :** `stage_prerentree_terminale_nsi.md`

## Pourquoi cette séance en premier

La représentation binaire est le **domaine le plus faible du groupe** : 40 % de réussite
moyenne, avec **trois élèves à 0 %**. Ce n'est pas une fragilité, c'est une absence.

L'enjeu pour la Terminale est indirect mais réel : le typage des attributs dans une base de
données, le coût mémoire des structures de données et surtout l'arithmétique modulaire du
chapitre « sécurisation des communications » supposent une aisance sur les entiers en machine.

Les booléens sont traités dans la même séance : ils sont mieux réussis (80 %) et le lien est
naturel — ce sont les deux faces de la représentation des données de base.

## Objectifs de la séance

1. Convertir un entier entre les bases 2, 10 et 16, dans les deux sens.
2. Évaluer une expression booléenne en respectant les priorités `not`, `and`, `or`.
3. Écrire la négation d'une expression composée (lois de De Morgan).

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Distribue les livrets ; explique la carte maîtrise × confiance | Lit sa carte, repère son domaine prioritaire |
| 20 min | Confrontation | « Écrivez 22 en binaire » — recueil **avant** tout rappel | Écrit sa réponse, puis recalcule la valeur décimale |
| 25 min | Reconstruction | Décomposition en puissances de 2 ; divisions successives ; base 16 | Prend la trace écrite, s'entraîne sur deux exemples |
| 30 min | Entraînement différencié | Distribue les trois parcours ; circule | Traite son parcours, note l'aide utilisée |
| 20 min | Booléens et ouverture | Tables de vérité ; De Morgan ; usage en boucle et en SQL | Complète les tables, formule De Morgan |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

Le principe du module : **prédire, exécuter, confronter**. Ici, l'exécution est un recalcul.

1. Poser : « Écrivez l'entier 22 en binaire. Notez votre réponse et votre certitude. »
   Aucun rappel préalable.
2. Recueillir sans commenter. Les erreurs attendues sont un nombre de bits erroné, ou des
   restes lus dans le mauvais sens.
3. Faire **vérifier chaque réponse** en recalculant : chaque élève reprend son écriture et
   calcule la somme des puissances de 2 correspondantes. C'est le contrôle à installer.
4. Faire constater qui retombe sur 22 et qui non.
5. **Puis** reconstruire les deux méthodes.

Le point à faire passer n'est pas la conversion elle-même : c'est que **toute conversion se
vérifie en une ligne**, et qu'il n'y a donc aucune raison de rendre une conversion fausse.

## Reconstruction

**Méthode 1 — décomposition en puissances de 2.** Écrire les puissances au tableau :

| 2⁷ | 2⁶ | 2⁵ | 2⁴ | 2³ | 2² | 2¹ | 2⁰ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

22 = 16 + 4 + 2, donc on place un 1 sous 16, 4 et 2 : **10110**.

**Méthode 2 — divisions successives.** Diviser par 2 en notant les restes, puis lire les
restes **de bas en haut** :

```
22 = 2 × 11 + 0
11 = 2 ×  5 + 1
 5 = 2 ×  2 + 1
 2 = 2 ×  1 + 0
 1 = 2 ×  0 + 1        →  lecture de bas en haut : 10110
```

Le sens de lecture est l'erreur classique de cette méthode : le faire dire à voix haute.

**Base 16.** A = 10, B = 11, C = 12, D = 13, E = 14, F = 15. Insister : F vaut **15**, pas 16.

0x2A = 2 × 16 + 10 = 42. Réciproquement, 60 = 3 × 16 + 12 = 0x3C.

## Entraînement différencié

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Représentation binaire en priorité 1 ou 2 dans le livret | Exercices 1 à 4, tableau de puissances fourni |
| Maîtrise | Domaine réussi mais hésitant | Exercices 3 à 6, sans tableau |
| Approfondissement | Domaine acquis avec certitude | Exercices 6 à 8, dont un passage par la base 16 |

## Booléens et ouverture — 20 minutes

**Priorités.** `not` d'abord, puis `and`, puis `or`. Faire évaluer pas à pas :
`(not True) or (False and True)` → `False or False` → `False`.

**Tables de vérité.** Faire compléter les quatre lignes de `A and B`, puis celles de
`not (A and B)`. Faire constater que la seconde coïncide avec `(not A) or (not B)` :
c'est la loi de De Morgan, à faire énoncer par un élève.

| A | B | A and B | not(A and B) | (not A) or (not B) |
|---|---|---|---|---|
| V | V | V | F | F |
| V | F | F | V | V |
| F | V | F | V | V |
| F | F | F | V | V |

**Ouverture Terminale.** Deux usages à nommer :

> **Invariants de boucle.** En Terminale, on démontre qu'un algorithme est correct en
> exhibant une propriété vraie à chaque tour de boucle. Cette propriété est une expression
> booléenne, et sa négation est la condition d'arrêt.
>
> **Clauses SQL.** Une requête `WHERE age > 18 AND classe = 'TG3'` est une expression
> booléenne. Sa négation correcte n'est pas `age <= 18 AND classe != 'TG3'` : c'est De Morgan
> qui donne la bonne écriture.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Restes lus de haut en bas | Faire vérifier par recalcul : le résultat ne retombe pas sur l'entier de départ |
| F pris pour 16 | Faire écrire la table complète A à F une fois pour toutes |
| Bits oubliés en tête | Faire aligner l'écriture sous le tableau des puissances |
| `not(A and B)` écrit `(not A) and (not B)` | Faire compléter la table de vérité ligne par ligne |
| Priorité de `not` ignorée | Faire parenthéser explicitement avant d'évaluer |

## Indicateurs de fin de séance

- L'élève recalcule systématiquement sa conversion pour la vérifier.
- L'élève écrit la table des correspondances hexadécimales sans hésiter.
- L'élève sait énoncer une loi de De Morgan avec ses mots.

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
