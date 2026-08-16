---
title: "Supports pratiques S4 - Listes, tuples, dictionnaires et tables CSV"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Séance 4 - Supports pratiques</h1>
<div class="subtitle">Listes, tuples, dictionnaires et tables CSV</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Fiches de manipulation, traçage et projet</div>
</div><div class="student-only"></div>
# Support 1 - bande d’indices

Pour `L = [4, 8, 15, 16]` :

| Indice | 0 | 1 | 2 | 3 |
|---|:---:|:---:|:---:|:---:|
| Valeur | 4 | 8 | 15 | 16 |

- longueur : 4 ;
- dernier indice : 3 ;
- dernier élément : `L[-1]`.

# Support 2 - alias ou copie ?

<div class="cut-card"><h3>Alias</h3><pre><code>a = [1, 2]
b = a</code></pre><p>Deux noms, un seul objet.</p></div>
<div class="cut-card"><h3>Copie superficielle</h3><pre><code>a = [1, 2]
b = a.copy()</code></pre><p>Deux listes distinctes au premier niveau.</p></div>

# Support 3 - fiche enregistrement

| Clé | Valeur | Type attendu | Valide ? |
|---|---|---|:---:|
| `id` |  | `str` non vide |  |
| `date` |  | `str` ISO |  |
| `temperature` |  | `float` |  |
| `humidite` |  | `int` |  |
| `statut` |  | `OK` ou `ALERTE` |  |

# Support 4 - mini-table CSV

```text
id,date,temperature,humidite,statut
C01,2026-08-24,28.4,55,OK
C02,2026-08-24,31.2,52,ALERTE
C03,2026-08-24,-1.5,80,ALERTE
```

Questions : quelles valeurs doivent être converties ? Quelles contraintes vérifier ? Comment détecter un identifiant dupliqué ?
