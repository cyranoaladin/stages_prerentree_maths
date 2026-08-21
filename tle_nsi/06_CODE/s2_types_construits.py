"""Seance 2 - Types construits. Ecrire ses predictions AVANT d'executer."""

if __name__ == "__main__":
    print("--- Bloc 1 : le piege ---")
    L = [1, 2, 3]
    L = L.append(4)
    print("L vaut :", L)

    print()
    print("--- Bloc 2 : la version correcte ---")
    L = [1, 2, 3]
    L.append(4)
    print("L vaut :", L)

    print()
    print("--- Bloc 3 : construire au lieu de modifier ---")
    L = [1, 2, 3]
    M = L + [4]
    print("L vaut :", L, "et M vaut :", M)

    print()
    print("--- Bloc 4 : trier ---")
    L = [3, 1, 2]
    M = sorted(L)
    print("apres sorted   : L vaut", L, "et M vaut", M)
    L.sort()
    print("apres L.sort() : L vaut", L)

    print()
    print("--- Bloc 5 : les structures de Terminale ---")
    pile = []
    pile.append(1)
    pile.append(2)
    print("pile, on depile le dernier entre :", pile.pop())

    file = []
    file.append(1)
    file.append(2)
    print("file, on defile le premier entre :", file.pop(0))

    arbre = {
        "valeur": 5,
        "gauche": {"valeur": 3, "gauche": None, "droite": None},
        "droite": {"valeur": 8, "gauche": None, "droite": None},
    }
    print("arbre, fils gauche :", arbre["gauche"]["valeur"])
    print()
    print("Une pile et une file ne different ici que par l'argument de pop().")
