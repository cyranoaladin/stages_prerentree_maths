# Terminale NSI — Séance 2 — Supports pratiques
## Types construits

## Support 1 — Bande d'indices (reconstruction)

Une bande cartonnée par élève, avec deux lignes de cases.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{|>{\bfseries}l|c|c|c|c|}\hline
\rowcolor{SoftBlue}
valeurs & 5 & 7 & 9 & 11 \\\hline
indices positifs & 0 & 1 & 2 & 3 \\\hline
indices négatifs & $-4$ & $-3$ & $-2$ & $-1$ \\\hline
\end{tabular}
\end{center}
```

**Usage.** L'élève pointe une case et lit les deux indices possibles. Le fait de voir
simultanément l'indexation positive et négative supprime l'hésitation sur `L[-1]`.

**Question à poser :** où est la case d'indice 4 ? Réponse : elle n'existe pas — d'où
l'`IndexError`.

## Support 2 — Fiche « modifier ou construire » (confrontation)

À projeter, puis à distribuer complétée.

| Écriture | Modifie L ? | Renvoie quoi ? | Après exécution, L vaut |
|---|:---:|---|---|
| `L.append(4)` | oui | `None` | `[1, 2, 3, 4]` |
| `L = L.append(4)` | oui | `None` | **`None`** — la liste est perdue |
| `M = L + [4]` | non | nouvelle liste | `[1, 2, 3]` inchangée |
| `L.insert(0, 9)` | oui | `None` | `[9, 1, 2, 3]` |
| `L.sort()` | oui | `None` | trié sur place |
| `M = sorted(L)` | non | nouvelle liste | inchangée |

**Point à faire émerger.** La ligne 2 est la seule qui détruit une information. Toutes les
autres sont sûres. La règle pratique : **ne jamais affecter le résultat d'une méthode qui
modifie en place.**

## Support 3 — Script de confrontation à exécuter

À fournir sur les postes, prêt à lancer.

```python
# --- Bloc 1 : le piege ---
L = [1, 2, 3]
L = L.append(4)
print("Bloc 1, L vaut :", L)

# --- Bloc 2 : la version correcte ---
L = [1, 2, 3]
L.append(4)
print("Bloc 2, L vaut :", L)

# --- Bloc 3 : construire au lieu de modifier ---
L = [1, 2, 3]
M = L + [4]
print("Bloc 3, L vaut :", L, "et M vaut :", M)

# --- Bloc 4 : trier ---
L = [3, 1, 2]
M = sorted(L)
print("Bloc 4a, L vaut :", L, "et M vaut :", M)
L.sort()
print("Bloc 4b, L vaut :", L)
```

**Consigne.** Chaque élève écrit les six sorties attendues **avant** de lancer le script.
Le bilan porte sur le nombre de prédictions justes, pas sur les sorties elles-mêmes.

## Support 4 — Cartes dictionnaire

Six cartes décrivant une opération sur `d = {'x': 10, 'y': 20}`. L'élève associe chaque carte
à son résultat.

| Carte | Opération | Résultat |
|---:|---|---|
| 1 | `d['y']` | 20 |
| 2 | `d['z']` | `KeyError` |
| 3 | `d.get('z', 0)` | 0 |
| 4 | `d['z'] = 30` | crée l'entrée, d a trois clés |
| 5 | `del d['x']` | supprime, d a une clé de moins |
| 6 | `len(d)` | nombre de clés |

## Support 5 — Les structures de Terminale, à exécuter

```python
# Une pile : dernier entre, premier sorti (LIFO)
pile = []
pile.append(1)
pile.append(2)
print("sommet depile :", pile.pop())     # 2

# Une file : premier entre, premier sorti (FIFO)
file = []
file.append(1)
file.append(2)
print("premier defile :", file.pop(0))   # 1

# Un arbre binaire decrit par un dictionnaire
arbre = {
    'valeur': 5,
    'gauche': {'valeur': 3, 'gauche': None, 'droite': None},
    'droite': {'valeur': 8, 'gauche': None, 'droite': None},
}
print("fils gauche :", arbre['gauche']['valeur'])   # 3
```

**Question à poser après exécution.** Quelle est la seule différence entre la pile et la
file, dans ce code ? Réponse : l'argument de `pop`. Une pile dépile à la fin (`pop()`), une
file défile au début (`pop(0)`). Une ligne sépare les deux structures.

## Support 6 — Affiche de séance

> **Avant d'écrire une instruction sur une liste, je me demande :**
> est-ce qu'elle **modifie** l'objet, ou est-ce qu'elle en **construit** un nouveau ?
>
> Si elle modifie : **je n'affecte pas son résultat.**
>
> **Les indices commencent à 0.** Pour n éléments, le dernier est $n - 1$.
> **Une clé peut être absente :** `get` plutôt que les crochets, en cas de doute.

## Matériel à prévoir

- Une bande d'indices par élève.
- Un poste par binôme, avec le script de confrontation prêt à lancer.
- Un jeu de six cartes dictionnaire par binôme.
- La fiche « modifier ou construire », une par élève, à conserver dans le portfolio.
