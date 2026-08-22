# Terminale Spécialité Mathématiques — Séance 3 — Fiche professeur
## Second degré : discriminant, signe du trinôme, tableau de signes

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_maths.md`

## Pourquoi cette séance

Le second degré est réussi à 76,2 % en moyenne, mais il porte **trois certitudes erronées**
et un item resté sans réponse. L'erreur n'est pas sur le discriminant : elle est sur le
**signe du trinôme**, où la règle « du signe de a à l'extérieur des racines » est appliquée
sans regarder le signe de a.

Cette séance précède volontairement la séance sur la dérivation : le tableau de signes d'un
trinôme est exactement l'outil dont on aura besoin le lendemain pour lire le signe de f'.

## Objectifs de la séance

1. Résoudre une équation du second degré et contrôler par la somme et le produit des
   racines.
2. Dresser un tableau de signes complet, en tenant compte du signe du coefficient dominant.
3. Résoudre une inéquation du second degré à partir de ce tableau et en écrire correctement
   l'ensemble solution.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Contrôle sur la séance 2 : simplifier $e^{4x}/e^{x+2}$ | Répond, déclare sa certitude |
| 20 min | Confrontation | « Sur quel intervalle $- x^2 + 3x - 2$ est-il strictement positif ? » | Répond, puis teste en $x = 0$ et $x = 1{,}5$ |
| 25 min | Reconstruction | Discriminant, racines, factorisation ; règle du signe de a ; tableau de signes | Prend la trace écrite |
| 30 min | Entraînement différencié | Distribue les trois parcours | Traite son parcours |
| 20 min | Ouverture Terminale | Le tableau de signes d'une dérivée ; mention du théorème des valeurs intermédiaires | Observe, note |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

1. Écrire : « Sur quel intervalle le trinôme $- x^2 + 3x - 2$ est-il strictement positif ? »
   Recueillir les réponses écrites et les certitudes, sans commenter.
2. La réponse fausse attendue est « à l'extérieur des racines », soit
   $] - \infty ; 1[ \cup ]2 ; + \infty [$ — le réflexe pris avec des trinômes à coefficient dominant positif.
3. Faire **tester deux valeurs** :
   - en $x = 0$ : $- 0 + 0 - 2 = - 2$, négatif ;
   - en $x = 1{,}5$ : $- 2{,}25 + 4{,}5 - 2 = 0{,}25$, positif.
4. Faire verbaliser : la valeur 0 est à l'extérieur des racines et pourtant le trinôme y est
   négatif. La règle a été appliquée sans regarder le signe de a.
5. **Puis** reconstruire : le trinôme est du signe de a à l'extérieur des racines. Ici
   $a = - 1$ : à l'extérieur il est négatif, entre les racines il est positif.

## Reconstruction

**Résolution.** $\Delta = b^2 - 4$ac.

| Signe de $\Delta$ | Racines |
|---|---|
| $\Delta > 0$ | deux racines distinctes $( - b \pm \surd \Delta )/(2a)$ |
| $\Delta = 0$ | une racine double $- b/(2a)$ |
| $\Delta < 0$ | aucune racine réelle |

**Contrôle systématique** : somme des racines = $- b/a$, produit = c/a. Ce contrôle prend cinq
secondes et détecte la quasi-totalité des erreurs de calcul.

**Signe du trinôme.** Faire construire le tableau au tableau, avec les élèves :

| | $- \infty$ | | $x_1$ | | $x_2$ | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de ax^2+bx+c | | signe de a | 0 | signe de $- a$ | 0 | signe de a | |

Quand $\Delta < 0$, le trinôme garde le signe de a sur $\mathbb{R}$ tout entier — cas à traiter
explicitement, car il est souvent oublié.

**Écriture de l'ensemble solution.** Insister sur la réunion : pour $x^2 - 9 \geqslant 0$, l'ensemble
solution est $] - \infty ; - 3] \cup [3 ; + \infty [$, avec les crochets fermés puisque l'inégalité est large.

## Entraînement différencié

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Certitude erronée ou item sans réponse sur le second degré | Exercices 1 à 4, tableau de signes pré-imprimé |
| Maîtrise | Réussite hésitante | Exercices 3 à 6, tableau à construire seul |
| Approfondissement | Domaine acquis | Exercices 6 à 8, dont une discussion selon un paramètre |

## Ouverture sur la Terminale — 20 minutes

Écrire : soit $f(x) = x^3 - 3x^2 + 1$. Faire calculer $f'(x) = 3x^2 - 6x = 3x(x - 2)$.

Faire remarquer : **f' est un trinôme**. Dresser son tableau de signes exactement comme
depuis le début de la séance. En déduire les variations de f — sans les démontrer, elles
seront reprises en séance 4.

Puis annoncer le prolongement de Terminale :

> En Terminale, on dérivera une deuxième fois : f''$(x) = 6x - 6$. Le signe de f'' donne les
> variations de f', donc la **convexité** de f. Le tableau de signes que vous savez faire
> aujourd'hui servira deux fois par exercice.

Mentionner enfin le **théorème des valeurs intermédiaires** : si f est continue et
strictement monotone sur un intervalle, et change de signe, l'équation $f(x) = 0$ y admet une
solution unique. Les variations en sont l'ingrédient. Ne pas aller plus loin.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Règle du signe appliquée sans regarder a | Faire tester une valeur à l'extérieur des racines |
| Cas $\Delta < 0$ oublié | Faire chercher le signe de $2x^2 + x + 3$ sur $\mathbb{R}$ |
| Solutions d'équation confondues avec ensemble solution d'inéquation | Faire écrire les deux pour le même trinôme |
| Réunion oubliée dans l'ensemble solution | Faire placer les intervalles sur une droite graduée |
| $\Delta = b^2 + 4$ac | Faire réécrire la formule avant chaque calcul |

## Indicateurs de fin de séance

- L'élève écrit le signe de a avant de remplir son tableau de signes.
- L'élève contrôle ses racines par la somme et le produit.
- L'élève écrit un ensemble solution avec le bon type de crochets.

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`._
