# 1ere_spe_S5_PROF_Fiche
## Séance 5 — Suites numériques, Python et évaluation de synthèse

> **Nexus Réussite - Stage de pré-rentrée 2026-2027**


## Préparation avant l’arrivée des élèves

- Imprimer la fiche élève, les cartes d’aide et les supports de manipulation.
- Préparer les mini-tableaux et les feutres.
- Ouvrir la grille d’observation de la séance.
- Repérer les exercices de consolidation, maîtrise et approfondissement.
- Prévoir une horloge visible et une pause de cinq minutes.

## Consignes orales essentielles

1. « Écris d’abord ta réponse et ta certitude ; ne corrige pas encore. »
2. « Nomme la relation ou la propriété que tu utilises. »
3. « Une erreur n’est pas effacée : elle devient une donnée pour comprendre. »
4. « Demande une carte d’aide seulement après une première tentative. »
5. « Avant de valider, effectue un contrôle de vraisemblance. »

## Parcours nominatifs

- **Donia Khadhrani** : Suites et bilan
- **Malek Khadhrani** : Suites/Python
- **Ahmad Beldi** : Suites/Python approfondi

## Déroulé validé du programme

## Séance 5 — Suites numériques, Python et évaluation de synthèse

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

### Déroulé

|       Temps | Phase                  | Tronc commun                                  | Différenciation et supports       | Indicateurs                        |
| ----------: | ---------------------- | --------------------------------------------- | --------------------------------- | ---------------------------------- |
|    0-10 min | Rituel cumulatif       | Une question par séance                       | Individuel                        | 4/5                                |
|   10-30 min | Construction           | Suite, indice, terme, explicite et récurrence | Tableau de termes                 | Les notations sont comprises       |
|   30-50 min | Modèles                | Suites arithmétiques et géométriques          | Contextes de capital et de points | Modèle correctement choisi         |
|   50-65 min | Python                 | Boucle, fonction, liste de termes             | Ordinateurs ou code projeté       | Code exécuté ou tracé correctement |
|   65-70 min | Pause                  | —                                             | —                                 | —                                  |
|   70-90 min | Parcours personnalisés | Suites et Python gradués                      | Voir ci-dessous                   | 80 % du parcours                   |
|  90-115 min | Évaluation finale      | 16 items, certitude 1 à 4                     | Individuel                        | Comparaison initial/final          |
| 115-120 min | Bilan                  | Une priorité et un engagement                 | Carte personnelle                 | Plan explicite                     |

### Contenus personnalisés

| Élève     | Travail prioritaire                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------- |
| **Donia** | Tableau de termes, distinction $u_n$ et $u_{n+1}$, lien avec coefficients multiplicateurs            |
| **Malek** | Reconnaître une suite géométrique, contrôler les puissances dans le terme général, écrire une boucle |
| **Ahmad** | Passer d’un contexte à une récurrence, programmer un seuil, approfondissement logique                |

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

### Erreurs à surveiller

* confondre indice et valeur ;
* commencer au mauvais indice ;
* calculer $u_{n+1}$ avec la valeur initiale à chaque étape ;
* confondre accroissement constant et taux constant ;
* écrire $u_n=u_0+nq$ pour une suite géométrique ;
* placer `return` dans la boucle ;
* modifier une variable sans conserver les valeurs dans une liste ;
* oublier que `range(5)` produit cinq indices de 0 à 4.

---


## Activités de construction

### Activité 5 — « De l’évolution à la suite »

Un capital de 200 TND augmente de 5 % par mois :

$$u_{n+1}=1{,}05u_n.$$

Faire produire successivement :

* un tableau ;
* une relation de récurrence ;
* une formule explicite ;
* un programme Python.


## Banque d’exercices et corrigé

### Série 5 — Suites et Python

1. Soit $u_0=5$ et $u_{n+1}=u_n+3$. Calculer $u_1,u_2,u_3$.
2. Donner $u_n$.
3. Soit $v_0=200$ et $v_{n+1}=1{,}05v_n$. Calculer $v_1$ et $v_2$.
4. Donner $v_n$.
5. Déterminer la liste construite :

```python
u = 3
termes = []

for _ in range(5):
    termes.append(u)
    u = 2 * u - 1
```

#### Correction

1.

$$u_1=8,\quad u_2=11,\quad u_3=14.$$

2.

$$u_n=5+3n.$$

3.

$$v_1=210,\qquad v_2=220{,}5.$$

4.

$$v_n=200\times1{,}05^n.$$

5.

```python
[3, 5, 9, 17, 33]
```

---


## Corrigé rapide à garder sous la main

#### Correction

1.

$$u_1=8,\quad u_2=11,\quad u_3=14.$$

2.

$$u_n=5+3n.$$

3.

$$v_1=210,\qquad v_2=220{,}5.$$

4.

$$v_n=200\times1{,}05^n.$$

5.

```python
[3, 5, 9, 17, 33]
```

---


## Observation minute par minute

| Moment | Élément à observer | Preuve attendue |
|---|---|---|
| Rituel | Procédure spontanée et certitude | Réponse individuelle non corrigée |
| Construction | Capacité à verbaliser l’idée initiale | Phrase ou schéma explicatif |
| Entraînement | Stabilisation après correction | Deux réussites consécutives |
| Différenciation | Niveau d’aide réellement nécessaire | Carte maximale utilisée |
| Synthèse | Capacité à reformuler la trace | Exemple personnel exact |
| Exit ticket | Disponibilité immédiate | Réponse autonome et certitude cohérente |

## Décision de fin de séance

- **Poursuivre en consolidation** si la réussite exige encore les cartes C ou D.
- **Passer en maîtrise** après deux réussites autonomes sur des données différentes.
- **Passer en approfondissement** si l’élève justifie, contrôle et transfère.
- **Reprogrammer une reprise** si une erreur initiale réapparaît avec certitude 3 ou 4.


<hr>
_Source pédagogique unique : `stage_prerentree_premiere_maths.md`. Les objectifs, l’ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
