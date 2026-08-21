# Terminale NSI — Séance 4 — Supports pratiques
## Algorithmique

## Support 1 — Script de confrontation

À fournir sur les postes, prêt à lancer. Les élèves prédisent **avant**.

```python
def recherche_dichotomique(tableau, valeur):
    gauche, droite = 0, len(tableau) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if tableau[milieu] == valeur:
            return milieu
        if tableau[milieu] < valeur:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return -1

t = [4, 1, 9, 3]
print("La valeur 4 est a l'indice", t.index(4))
print("La dichotomie repond :", recherche_dichotomique(t, 4))
```

*Sortie :* `La valeur 4 est a l'indice 0` puis `La dichotomie repond : -1`.

**Point à faire émerger.** Aucune erreur n'est affichée. Le programme ne plante pas, ne
prévient pas, ne ralentit pas : il **répond faux**. Un programme qui plante se répare ; un
programme qui ment se propage.

## Support 2 — Déroulé à la main

Tableau à compléter, pour la recherche de 4 dans `[4, 1, 9, 3]`.

| tour | gauche | droite | milieu | tableau[milieu] | décision |
|---:|---:|---:|---:|---:|---|
| 1 | 0 | 3 | 1 | 1 | 1 < 4 → gauche = 2 |
| 2 | 2 | 3 | 2 | 9 | 9 > 4 → droite = 1 |
| — | 2 | 1 | — | — | gauche > droite → renvoie −1 |

**Question à poser.** À quel tour l'indice 0 a-t-il été examiné ? Réponse : jamais. Dès le
premier tour, la moitié gauche a été écartée — à tort, puisque le tableau n'était pas trié.

## Support 3 — Table des coûts

À projeter vierge, à compléter collectivement, puis à conserver dans le portfolio.

| Taille n | Recherche séquentielle (pire cas) | Dichotomie (pire cas) | Puissance de 2 correspondante |
|---:|---:|---:|---|
| 16 | 16 | 4 | 2⁴ = 16 |
| 100 | 100 | 7 | 2⁷ = 128 |
| 1 000 | 1 000 | 10 | 2¹⁰ = 1 024 |
| 100 000 | 100 000 | 17 | 2¹⁷ ≈ 131 000 |
| 1 000 000 | 1 000 000 | 20 | 2²⁰ ≈ 1 048 000 |

**Point à faire émerger.** Passer de 1 000 à 1 000 000 d'éléments multiplie le coût
séquentiel par 1 000, et double seulement le coût de la dichotomie. C'est ce que signifie
« logarithmique ».

**Repères à mémoriser :** 2¹⁰ = 1 024 et 2²⁰ ≈ 10⁶.

## Support 4 — Cartes de tri par insertion

Quatre cartes portant 5, 2, 8 et 1, à manipuler physiquement.

**Consigne.** Trier les cartes par insertion : prendre les cartes une à une et insérer chacune
à sa place dans la partie déjà triée. **Compter chaque comparaison à voix haute.**

| étape | état | comparaisons |
|---:|---|---:|
| départ | 5 · 2 · 8 · 1 | 0 |
| insérer 2 | 2 · 5 · 8 · 1 | 1 |
| insérer 8 | 2 · 5 · 8 · 1 | 1 |
| insérer 1 | 1 · 2 · 5 · 8 | 3 |
| total | | 5 |

**Prolongement.** Faire refaire avec le tableau `[8, 5, 2, 1]`, déjà trié à l'envers : le
nombre de comparaisons passe à 6, le maximum pour quatre cartes. Faire le lien avec « pire
cas en n² ».

## Support 5 — Le grand écart, à chronométrer

```python
import time

def fibo_naif(n):
    if n <= 1:
        return n
    return fibo_naif(n - 1) + fibo_naif(n - 2)

def fibo_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fibo_memo(n - 1, memo) + fibo_memo(n - 2, memo)
    return memo[n]

debut = time.time()
resultat = fibo_naif(32)
print("naif  :", resultat, "en", round(time.time() - debut, 3), "s")

debut = time.time()
resultat = fibo_memo(32)
print("memo  :", resultat, "en", round(time.time() - debut, 6), "s")
```

**Conduite.** Faire lancer sur chaque poste. Les deux fonctions renvoient le **même**
résultat ; seul le temps diffère, de plusieurs ordres de grandeur.

Faire formuler la raison : la version naïve recalcule `fibo(30)` des milliers de fois. La
seconde le mémorise dans un **dictionnaire** — celui de la séance 2.

Ne pas demander d'écrire une fonction récursive : ces deux fonctions sont fournies, exécutées
et commentées, pas reproduites.

## Support 6 — Affiche de séance

> **Avant d'utiliser un algorithme, j'écris sa précondition.**
>
> Un algorithme dont la précondition n'est pas respectée **ne plante pas** :
> il répond faux, sans prévenir.
>
> **Repères de coût :** 2¹⁰ = 1 024 · 2²⁰ ≈ 1 000 000.
> Séquentielle : n comparaisons. Dichotomie : log₂ n.

## Matériel à prévoir

- Un poste par binôme, avec les trois scripts prêts à lancer.
- Un jeu de quatre cartes numérotées par binôme.
- La table des coûts, vierge puis complétée, une par élève.
