"""Séance 3 - fonctions et tests - solution de référence."""

def est_pair(n: int) -> bool:
    """Renvoie True si n est pair."""
    return n % 2 == 0

def maximum_deux(a, b):
    """Renvoie la plus grande des deux valeurs."""
    if a >= b:
        return a
    return b

def moyenne(valeurs):
    """Renvoie la moyenne d'une liste non vide."""
    assert len(valeurs) > 0
    total = 0.0
    for valeur in valeurs:
        total += valeur
    return total / len(valeurs)

assert est_pair(4) is True
assert est_pair(5) is False
assert est_pair(0) is True
assert maximum_deux(2, 7) == 7
assert maximum_deux(-2, -7) == -2
assert maximum_deux(3, 3) == 3
assert moyenne([2, 4, 6]) == 4
assert moyenne([5]) == 5
