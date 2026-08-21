# Terminale Spécialité Mathématiques — Séance 5 — Supports de manipulation
## Produit scalaire, probabilités, Python

## Support 1 — Repère quadrillé et vecteurs à tracer

Une feuille quadrillée avec un repère orthonormé par élève. Faire tracer les vecteurs
u(−2 ; 5) et v(4 ; 1), puis u(3 ; 1) et v(−2 ; 6).

**Objectif.** Vérifier visuellement l'angle avant de calculer, puis confronter le calcul à
l'impression visuelle. Le produit scalaire négatif correspond à un angle obtus : l'observer
donne un contrôle de vraisemblance immédiat.

| Situation | u·v | Angle observé |
|---|---|---|
| u(−2 ; 5), v(4 ; 1) | −3 | obtus |
| u(3 ; 1), v(−2 ; 6) | 0 | droit |
| u(2 ; 1), v(4 ; 3) | 11 | aigu |

**Règle de contrôle à faire formuler :** produit scalaire positif ⟹ angle aigu ; nul ⟹
angle droit ; négatif ⟹ angle obtus.

## Support 2 — Du plan à l'espace (ouverture)

Un cube en fil de fer, ou à défaut une représentation en perspective cavalière, avec le
repère (A ; AB, AD, AE).

Faire lire les coordonnées de quelques vecteurs, puis calculer un produit scalaire à trois
coordonnées. Faire constater que la formule est la même, avec un terme de plus.

```
        H────────G
       /│       /│
      E────────F │
      │ │      │ │
      │ D──────│─C
      │/       │/
      A────────B
```

Question à poser : les vecteurs AG et BD sont-ils orthogonaux ? Avec A origine,
AG(1 ; 1 ; 1) et BD(−1 ; 1 ; 0), le produit scalaire vaut −1 + 1 + 0 = 0 : ils le sont.

**Point à faire émerger.** Cette démonstration serait longue par la géométrie classique ;
elle tient en une ligne avec le produit scalaire. C'est l'argument qui justifie tout le
chapitre de Terminale.

## Support 3 — Arbre pondéré vierge

Un arbre à deux niveaux, à photocopier, pour le tirage sans remise dans une urne de 3 boules
rouges et 2 noires.

```
                ┌── R  (....)
        ┌── R ──┤
        │(....) └── N  (....)
   ─────┤
        │       ┌── R  (....)
        └── N ──┤
         (....) └── N  (....)
```

*Réponses :* premier niveau 3/5 et 2/5 ; depuis R : 2/4 et 2/4 ; depuis N : 3/4 et 1/4.
P(deux rouges) = 3/5 × 2/4 = 6/20 = 3/10.

**Point de vigilance.** Les probabilités **sur** les branches sont conditionnelles ; celles
obtenues **au bout** d'un chemin sont des intersections. Faire écrire les deux notations à
côté de l'arbre.

## Support 4 — Cartes « indépendants ou incompatibles ? »

Quatre situations à trier.

| Carte | Situation | Verdict |
|---:|---|---|
| 1 | On lance un dé : A = « obtenir un nombre pair », B = « obtenir 3 » | Incompatibles, non indépendants |
| 2 | On lance deux fois une pièce : A = « pile au premier », B = « pile au second » | Indépendants |
| 3 | On tire une carte : A = « c'est un cœur », B = « c'est un roi » | Indépendants |
| 4 | On tire une carte : A = « c'est un cœur », B = « c'est un pique » | Incompatibles, non indépendants |

**Point à faire émerger.** Incompatible signifie « ne peuvent pas se produire ensemble » ;
indépendant signifie « l'un n'informe pas sur l'autre ». Deux événements incompatibles de
probabilités non nulles sont fortement dépendants : si A se produit, B est impossible.

## Support 5 — Fiche Python à compléter

À distribuer imprimée, avec les trous.

```python
def terme_arithmetique(u0, r, n):
    u = ..........
    for _ in range(..........):
        u = ..........
    return u

def terme_geometrique(v0, q, n):
    v = ..........
    for _ in range(..........):
        v = ..........
    return v

def premier_rang_depassement(v0, q, seuil):
    v = v0
    n = 0
    while v <= seuil:
        v = ..........
        n = ..........
    return n
```

**Jeu de tests à faire exécuter :**

| Appel | Résultat attendu | Contrôle à la main |
|---|---:|---|
| `terme_arithmetique(5, -2, 10)` | −15 | 5 + 10 × (−2) |
| `terme_geometrique(2, 3, 4)` | 162 | 2 × 3⁴ |
| `premier_rang_depassement(2, 3, 100)` | 4 | 2, 6, 18, 54, 162 |

## Matériel à prévoir

- Feuilles quadrillées avec repère, une par élève.
- Un cube en fil de fer ou une figure en perspective projetée.
- Arbres pondérés vierges photocopiés.
- Un jeu de quatre cartes par binôme.
- Un poste avec Python par binôme (ou une exécution projetée).
