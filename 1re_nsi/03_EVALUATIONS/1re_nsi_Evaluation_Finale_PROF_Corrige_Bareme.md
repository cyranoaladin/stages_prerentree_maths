---
title: "Corrigé et barème Première NSI"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Corrigé et barème</h1>
<div class="subtitle">Évaluation finale Python</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Document enseignant</div>
</div>
<div class="prof-only"></div>

## Partie A

1. `=` affecte ; `==` compare.
2. `(x < 0) or (x >= 10)`.
3. `5, 3, 1`.
4. `len(L)` est le nombre d’éléments ; le dernier indice est `len(L)-1`.
5. `None`.
6. Les flottants sont représentés de façon approximative ; utiliser une tolérance.
7. La collection doit être triée selon la clé recherchée.
8. La liste vide.

## Partie B - solution de référence

```python
def valeurs_valides(valeurs, minimum, maximum):
    assert minimum <= maximum
    resultat = []
    for valeur in valeurs:
        if minimum <= valeur <= maximum:
            resultat.append(valeur)
    return resultat


def statistiques(valeurs):
    assert len(valeurs) > 0
    plus_petite = valeurs[0]
    plus_grande = valeurs[0]
    total = 0
    for valeur in valeurs:
        if valeur < plus_petite:
            plus_petite = valeur
        if valeur > plus_grande:
            plus_grande = valeur
        total += valeur
    return plus_petite, plus_grande, total / len(valeurs)


def indice_capteur(mesures, identifiant):
    for i in range(len(mesures)):
        if mesures[i]["id"] == identifiant:
            return i
    return None
```

## Barème - 20 points

| Critère | Points |
|---|---:|
| connaissances et traçage | 8 |
| exactitude des fonctions | 5 |
| décomposition et lisibilité | 2 |
| tests | 2 |
| cas limites et contrats | 1 |
| explication orale | 2 |

Le résultat n’est pas utilisé comme note de classement. Une erreur avec forte certitude déclenche une remédiation prioritaire.
