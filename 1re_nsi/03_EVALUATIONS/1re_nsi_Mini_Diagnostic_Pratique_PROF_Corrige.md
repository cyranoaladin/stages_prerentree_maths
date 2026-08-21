---
title: "Corrigé mini-diagnostic pratique Première NSI"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Corrigé du mini-diagnostic</h1>
<div class="subtitle">Python - pilotage enseignant</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Document enseignant</div>
</div>
<div class="prof-only"></div>

## Réponses

1. `a = 10`, `b = 5`.
2. `range(2,6)` produit 2,3,4,5 ; `s = 14`.
3. `L[1] = 8`, `len(L)=3`, dernier indice `2`.
4. le programme affiche 6 ; `r` vaut `None`.

```python
def compte_superieurs(valeurs, seuil):
    compteur = 0
    for valeur in valeurs:
        if valeur > seuil:
            compteur += 1
    return compteur

assert compte_superieurs([1, 5, 8], 4) == 2
assert compte_superieurs([], 4) == 0
```

## Lecture pédagogique

| Élément | Indice d’une difficulté |
|---|---|
| `b` suit encore `a` | modèle d’affectation erroné |
| somme 4 ou nombre de tours | accumulateur non compris |
| `L[1]=5` | indexation à partir de 1 |
| `r=6` | confusion `print` / `return` |
| compteur réinitialisé dans la boucle | état de boucle non compris |
