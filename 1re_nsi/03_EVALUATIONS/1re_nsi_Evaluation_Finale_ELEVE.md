---
title: "Évaluation finale Première NSI"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Évaluation finale</h1>
<div class="subtitle">Python - théorie et pratique</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Document élève - sans correction</div>
</div>
<div class="student-only"></div>

# Partie A - connaissances et traçage - 8 points

1. Expliquer la différence entre `=` et `==`.
2. Donner la négation de `(x >= 0) and (x < 10)`.
3. Donner les valeurs produites par `range(5, 0, -2)`.
4. Expliquer la différence entre `len(L)` et le dernier indice.
5. Que renvoie une fonction sans `return` ?
6. Pourquoi tester deux flottants avec `==` peut-il être fragile ?
7. Quel prérequis rend possible une recherche dichotomique ?
8. Donner un cas limite pour une fonction calculant une moyenne.

## Feuille de réponses - partie A

<table>
<tr><th style="width:9%">Q</th><th>Réponse</th></tr>
<tr><td>1</td><td style="height:13mm"></td></tr>
<tr><td>2</td><td style="height:13mm"></td></tr>
<tr><td>3</td><td style="height:13mm"></td></tr>
<tr><td>4</td><td style="height:13mm"></td></tr>
<tr><td>5</td><td style="height:13mm"></td></tr>
<tr><td>6</td><td style="height:13mm"></td></tr>
<tr><td>7</td><td style="height:13mm"></td></tr>
<tr><td>8</td><td style="height:13mm"></td></tr>
</table>

# Partie B - pratique - 12 points

Écrire un programme comprenant les fonctions suivantes :

```python
def valeurs_valides(valeurs, minimum, maximum):
    """Renvoie une nouvelle liste contenant les valeurs dans l'intervalle fermé."""


def statistiques(valeurs):
    """Renvoie un tuple (minimum, maximum, moyenne) pour une liste non vide."""


def indice_capteur(mesures, identifiant):
    """Renvoie l'indice du premier capteur trouvé, sinon None."""
```

Contraintes :

- ne pas modifier la liste d’origine ;
- ne pas utiliser `min`, `max` ou `sum` dans `statistiques` ;
- écrire au moins six assertions ;
- documenter les préconditions ;
- traiter l’identifiant absent.

# Extension

Expliquer comment adapter `indice_capteur` à une recherche dichotomique lorsque les identifiants sont triés.

<div class="answer-lg"></div>

## Fichiers remis

- nom du fichier Python : .............................................................................
- nombre d’assertions exécutées : .....................................................................
- résultat du dernier test : ..........................................................................
