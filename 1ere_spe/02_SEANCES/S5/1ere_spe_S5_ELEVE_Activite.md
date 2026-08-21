# 1re Spécialité Mathématiques — Séance 5 : Suites numériques, Python et évaluation de synthèse
## ELEVE A

**Nom et prénom :** ..............................................................................  
**Date :** ....................................................

## Mes objectifs

### Objectifs

* découvrir les modes de définition d’une suite ;
* calculer des termes ;
* reconnaître un accroissement constant ou un taux constant ;
* relier suites et évolutions ;
* générer des termes en Python ;
* utiliser une liste ;
* réinvestir les acquis des quatre séances ;
* élaborer un plan de travail pour septembre.

Le programme de Première présente les suites par formule explicite, relation de récurrence, algorithme ou motif. Il formalise ensuite les suites arithmétiques et géométriques.


## Rituel d’entrée

1. Calculer u1,u2,u3.

Réponse : ............................................................  Certitude : ☐1 ☐2 ☐3 ☐4

2. Distinguer explicite/récurrence.

Réponse : ............................................................  Certitude : ☐1 ☐2 ☐3 ☐4

3. Reconnaître arithmétique/géométrique.

Réponse : ............................................................  Certitude : ☐1 ☐2 ☐3 ☐4

4. Tracer une boucle Python.

Réponse : ............................................................  Certitude : ☐1 ☐2 ☐3 ☐4


## Activité de départ

### Activité 5 — « De l’évolution à la suite »

Un capital de 200 TND augmente de 5 % par mois :

$$u_{n+1}=1{,}05u_n.$$

Faire produire successivement :

* un tableau ;
* une relation de récurrence ;
* une formule explicite ;
* un programme Python.


## Tronc commun et parcours différenciés

> Commence par les exercices indiqués par l’enseignant. Passe au parcours suivant seulement après validation. Pour chaque réponse, ajoute un contrôle ou une justification.

### Série 5 — Suites et Python

1. Soit $u_0=5$ et $u_{n+1}=u_n+3$. Calculer $u_1,u_2,u_3$.

....................................................................................................
2. Donner $u_n$.

....................................................................................................
3. Soit $v_0=200$ et $v_{n+1}=1{,}05v_n$. Calculer $v_1$ et $v_2$.

....................................................................................................
4. Donner $v_n$.

....................................................................................................
5. Déterminer la liste construite :

....................................................................................................

```python
u = 3
termes = []

for _ in range(5):
    termes.append(u)
    u = 2 * u - 1
```

## Ma trace écrite

### Trace écrite attendue

Une suite peut être définie :

* explicitement : $u_n=f(n)$ ;
* par récurrence : $u_{n+1}=f(u_n)$ avec un terme initial.

Suite arithmétique :

$$u_{n+1}=u_n+r \quad\Longrightarrow\quad u_n=u_0+nr.$$

Suite géométrique :

$$u_{n+1}=q,u_n \quad\Longrightarrow\quad u_n=u_0q^n.$$

Exemple Python :

```python
def termes_suite(u0: float, q: float, nombre: int) -> list[float]:
    """Renvoie les premiers termes d'une suite géométrique."""
    if nombre < 0:
        raise ValueError("Le nombre de termes doit être positif.")

    termes: list[float] = []
    u = u0

    for _ in range(nombre):
        termes.append(u)
        u *= q

    return termes
```


### Exemple personnel

....................................................................................................

....................................................................................................

## Mon auto-évaluation

| Je peux… | Pas encore | Avec aide | Seul | Expliquer |
|---|:---:|:---:|:---:|:---:|
| reformuler la question | ☐ | ☐ | ☐ | ☐ |
| choisir une relation ou une propriété | ☐ | ☐ | ☐ | ☐ |
| effectuer le calcul sans erreur | ☐ | ☐ | ☐ | ☐ |
| contrôler mon résultat | ☐ | ☐ | ☐ | ☐ |
| estimer correctement ma certitude | ☐ | ☐ | ☐ | ☐ |

## Exit ticket

1. Donner le terme général.

....................................................................................................

2. Compléter une fonction Python.

....................................................................................................

3. Rechercher un seuil.

....................................................................................................


**Ce que je retiens aujourd’hui :**

....................................................................................................

**La notion que je dois encore reprendre :**

....................................................................................................


<hr>
_Source pédagogique unique : `stage_prerentree_premiere_maths.md`. Les objectifs, l’ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
