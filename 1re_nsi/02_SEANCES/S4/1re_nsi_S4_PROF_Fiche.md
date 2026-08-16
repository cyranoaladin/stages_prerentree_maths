---
title: "Fiche enseignant S4 - Listes, tuples, dictionnaires et tables CSV"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 4 - Fiche enseignant</h1>
<div class="subtitle">Listes, tuples, dictionnaires et tables CSV</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Corrigé, différenciation et pilotage</div>
</div><div class="prof-only"></div>
# Objectifs

- maîtriser indexation et longueur ;
- comprendre mutation et aliasing ;
- utiliser listes et dictionnaires ;
- importer une table CSV ;
- filtrer, trier et contrôler des données ;

# Déroulé minute par minute

- 0-10 rituel ;
- 10-28 listes/index ;
- 28-45 aliasing ;
- 45-65 dictionnaires ;
- 65-70 pause ;
- 70-100 CSV ;
- 100-112 tri/cohérence ;
- 112-120 synthèse/exit ;

# Rituel prêt à l’emploi

## Question 1

Pour `L = [4, 8, 15, 16]`, donner `L[1]`, `len(L)` et le dernier indice.

**Réponse attendue :** `L[1] = 8`, `len(L) = 4`, dernier indice : 3.

## Question 2

Prédire la valeur de `a` :

```python
a = [1, 2]
b = a
b.append(3)
```

**Réponse attendue :** `a` vaut `[1, 2, 3]`, car `a` et `b` sont deux noms du même objet liste.


## Notions de cours

### Listes

- premier élément : `L[0]` ;
- dernier élément : `L[-1]` ;
- longueur : `len(L)` ;
- ajout : `L.append(x)` ;
- parcours : `for valeur in L:` ;
- compréhension : `[x*x for x in L if x >= 0]`.

### Alias

```python
a = [1, 2]
b = a
b.append(3)
```

`a` et `b` désignent la même liste. Pour une copie superficielle : `b = a.copy()`.

### Dictionnaires

```python
mesure = {"id": "C01", "temperature": 28.4}
```

Parcours : `for cle, valeur in mesure.items():`.

### CSV

La bibliothèque standard `csv` permet d’importer une table. Chaque ligne peut devenir un dictionnaire avec `csv.DictReader`.



## Activité commune - index, longueur et mutation

```python
L = [4, 8, 15, 16]
```

| Expression | Valeur |
|---|---|
| `L[0]` |  |
| `L[1]` |  |
| `len(L)` |  |
| `L[len(L)-1]` |  |

### Alias

Prédire puis exécuter :

```python
a = [1, 2]
b = a
b.append(3)
print(a)
```

Expliquer le résultat.



## Parcours Fondations - Ahmad

1. Corriger cinq expressions d’indexation.
2. Écrire une boucle qui double chaque valeur sans modifier la liste d’origine.
3. Construire un dictionnaire décrivant une mesure.
4. Parcourir `keys`, `values` et `items`.
5. Importer `mesures_capteurs.csv` et afficher les identifiants.

## Parcours Fiabilisation - Ahmed

1. Démontrer un effet d’aliasing et le corriger.
2. Construire une compréhension filtrant les alertes.
3. Valider chaque ligne du CSV.
4. Détecter un identifiant dupliqué.
5. Trier les mesures par température puis par identifiant.



## Corrigé essentiel

- `L[0]=4`, `L[1]=8`, `len(L)=4`, dernier élément `16` ;
- l’aliasing modifie les deux noms car ils désignent le même objet ;
- une copie indépendante se crée avec `copy()` ;
- `csv.DictReader` produit des dictionnaires dont les valeurs sont d’abord des chaînes : il faut convertir les nombres.


# Consignes prêtes à dire

- « Avant d’exécuter, écris ce que tu prévois. »
- « Une réponse sans contrôle reste une hypothèse. »
- « Le bug utile est celui que l’on peut reproduire. »
- « Ne change qu’une chose à la fois, puis relance les tests. »
- « Explique le rôle de cette variable sans lire le code mot à mot. »

# Points de vigilance

- ne pas transformer l’activité en copie de code projeté ;
- vérifier que les deux élèves alternent pilote et navigateur ;
- ne pas confondre réussite après aide D/E et autonomie ;
- demander un test sur les bornes ;
- conserver le fichier final et le journal des erreurs.

# Indicateurs de réussite

| Élève | Prévision exacte | Code exécutable | Tests pertinents | Explication | Aide maximale |
|---|:---:|:---:|:---:|:---:|:---:|
| Ahmad BELDI |  |  |  |  |  |
| Ahmed BENHADJ SALEM |  |  |  |  |  |
