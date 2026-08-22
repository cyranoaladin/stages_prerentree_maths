# Terminale NSI — Séance 3 — Supports pratiques
## Programmation

## Support 1 — Script de confrontation

À fournir sur les postes. Les élèves écrivent **quatre** prédictions avant de lancer.

```python
def h(L):
    L.append(0)

def h2(L):
    L.append(0)
    return L

M = [1, 2]
r = h(M)
print("1. r vaut :", r)
print("2. M vaut :", M)

N = [1, 2]
s = h2(N)
print("3. s vaut :", s)
print("4. N vaut :", N)
```

*Sorties :* `None` ; `[1, 2, 0]` ; `[1, 2, 0]` ; `[1, 2, 0]`.

**Point à faire émerger.** Entre `h` et `h2`, seule la **valeur renvoyée** change. La liste
est modifiée dans les deux cas. Renvoyer et modifier sont deux questions indépendantes.

## Support 2 — Tableau des quatre cas de figure

À projeter, puis à distribuer complété, à conserver dans le portfolio.

| Fonction | Renvoie | Modifie l'argument | Usage typique |
|---|---|---|---|
| `def f(x): return x * 2` | une valeur | non | calcul pur |
| `def g(L): L.append(0)` | `None` | oui | procédure de modification |
| `def h(L): L.append(0); return L` | une valeur | oui | à éviter : deux effets, source de confusion |
| `def k(x): print(x)` | `None` | non | affichage |

**Règle de style à faire énoncer.** Une fonction fait de préférence **une seule** de ces deux
choses : soit elle calcule et renvoie, soit elle modifie et ne renvoie rien. La troisième
ligne est celle qui produit le plus de bugs.

## Support 3 — Gabarit de table de trace

À photocopier, plusieurs exemplaires par élève.

> **Programme tracé :** .........................................................
>
> | tour | variable 1 | variable 2 | variable 3 | commentaire |
> |---:|---|---|---|---|
> | avant | | | | initialisation |
> | 1 | | | | |
> | 2 | | | | |
> | 3 | | | | |
> | 4 | | | | |
> | 5 | | | | |
> | après | | | | valeur finale |
>
> **Prédiction du résultat :** ...............
> **Résultat réel après exécution :** ...............
> **Écart :** $\square$aucun $\square$ oui, d'où vient-il ? ...............................

## Support 4 — Cartes `range`

Huit cartes portant une écriture de `range`. L'élève associe chaque carte au nombre de tours
et aux valeurs produites.

| Carte | Écriture | Valeurs | Tours |
|---:|---|---|---:|
| 1 | `range(3)` | 0, 1, 2 | 3 |
| 2 | `range(1, 4)` | 1, 2, 3 | 3 |
| 3 | `range(0, 10, 2)` | 0, 2, 4, 6, 8 | 5 |
| 4 | `range(2, 10, 3)` | 2, 5, 8 | 3 |
| 5 | `range(1, 10, 4)` | 1, 5, 9 | 3 |
| 6 | `range(5, 5)` | aucune | 0 |
| 7 | `range(10, 0, -2)` | 10, 8, 6, 4, 2 | 5 |
| 8 | `range(4, 1)` | aucune | 0 |

**Cartes à discuter en priorité.** Les cartes 6 et 8 produisent zéro tour : la boucle ne
s'exécute pas du tout. C'est une source classique de bug silencieux.

## Support 5 — Script à déboguer (parcours maîtrise)

```python
def moyenne(notes):
    for note in notes:
        total = 0
        total = total + note
    return total / len(notes)

print(moyenne([10, 20, 30]))   # attendu 20, obtenu ?
```

**Conduite.** Faire remplir la table de trace **avant** d'exécuter. L'accumulateur `total`
est remis à zéro à chaque tour : la table le rend visible immédiatement, alors que la sortie
seule (30.0 divisé par 3, soit 10.0) ne dit pas où est le problème.

Correction : sortir `total = 0` de la boucle.

## Support 6 — Fiche « spécification et tests »

À conserver dans le portfolio.

> **Toute fonction que j'écris comporte :**
>
> 1. une phrase disant ce qu'elle **prend** et ce qu'elle **renvoie** ;
> 2. au moins **deux** tests, dont un cas limite (liste vide, valeur nulle, borne).
>
> ```python
> def moyenne(notes):
>     """Prend une liste non vide de nombres, renvoie leur moyenne."""
>     return sum(notes) / len(notes)
>
> assert moyenne([10, 20]) == 15
> assert moyenne([5]) == 5
> ```
>
> Un `assert` qui passe n'affiche rien. Un `assert` qui échoue arrête le programme : c'est
> exactement ce qu'on veut.

## Matériel à prévoir

- Un poste par élève si possible, sinon par binôme.
- Le script de confrontation et le script à déboguer, prêts à lancer.
- Gabarits de table de trace, au moins quatre par élève.
- Un jeu de huit cartes `range` par binôme.
- La fiche « spécification et tests », une par élève.
