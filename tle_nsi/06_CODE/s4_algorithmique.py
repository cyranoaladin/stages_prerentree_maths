"""Seance 4 - Algorithmique. Ecrire ses predictions AVANT d'executer."""

import math
import time


def recherche_dichotomique(tableau, valeur):
    """Precondition : tableau trie par ordre croissant.
    Renvoie l'indice de valeur dans tableau, ou -1 si absente."""
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


def recherche_sequentielle(tableau, valeur):
    """Aucune precondition. Renvoie l'indice de valeur, ou -1 si absente."""
    for indice in range(len(tableau)):
        if tableau[indice] == valeur:
            return indice
    return -1


def fibo_naif(n):
    """Renvoie le n-ieme terme de Fibonacci, en recalculant tout a chaque fois."""
    if n <= 1:
        return n
    return fibo_naif(n - 1) + fibo_naif(n - 2)


def fibo_memo(n, memo=None):
    """Renvoie le n-ieme terme de Fibonacci, en memorisant les resultats deja calcules."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fibo_memo(n - 1, memo) + fibo_memo(n - 2, memo)
    return memo[n]


assert recherche_dichotomique([1, 3, 5, 7, 9, 11, 13], 13) == 6
assert recherche_dichotomique([1, 3, 5, 7, 9], 4) == -1
assert recherche_sequentielle([4, 1, 9, 3], 4) == 0
assert fibo_memo(10) == 55
assert fibo_naif(10) == fibo_memo(10)


if __name__ == "__main__":
    print("--- La precondition non respectee ---")
    t = [4, 1, 9, 3]
    print("Le tableau est :", t, "(il n'est PAS trie)")
    print("La valeur 4 se trouve a l'indice", t.index(4))
    print("La dichotomie repond          :", recherche_dichotomique(t, 4))
    print("La recherche sequentielle repond :", recherche_sequentielle(t, 4))
    print("   Aucune erreur n'est levee. Le programme repond simplement faux.")

    print()
    print("--- Le cout ---")
    print(f"{'taille':>10} {'sequentielle':>14} {'dichotomie':>12}")
    for taille in (16, 100, 1000, 100000, 1000000):
        # Nombre de comparaisons au pire : l'ordre de grandeur est log2(n), arrondi
        # au superieur puisqu'une etape entamee est une comparaison faite.
        etapes = math.ceil(math.log2(taille))
        print(f"{taille:>10} {taille:>14} {etapes:>12}")

    print()
    print("--- Le meme resultat, deux couts ---")
    debut = time.time()
    resultat_naif = fibo_naif(30)
    duree_naif = time.time() - debut

    debut = time.time()
    resultat_memo = fibo_memo(30)
    duree_memo = time.time() - debut

    print("fibo_naif(30) =", resultat_naif, "en", round(duree_naif, 4), "s")
    print("fibo_memo(30) =", resultat_memo, "en", round(duree_memo, 6), "s")
    print("   Meme resultat. La version memoisee stocke ses calculs dans un dictionnaire.")
