"""Seance 3 - Fonctions, retour, portee. Ecrire ses predictions AVANT d'executer."""


def h(L):
    """Ajoute 0 a la liste. Ne renvoie rien."""
    L.append(0)


def h2(L):
    """Ajoute 0 a la liste et renvoie la liste modifiee."""
    L.append(0)
    return L


def moyenne_fausse(notes):
    """VOLONTAIREMENT FAUSSE : l'accumulateur est reinitialise a chaque tour."""
    for note in notes:
        total = 0
        total = total + note
    return total / len(notes)


def moyenne(notes):
    """Prend une liste non vide de nombres, renvoie leur moyenne."""
    total = 0
    for note in notes:
        total = total + note
    return total / len(notes)


assert moyenne([10, 20]) == 15
assert moyenne([5]) == 5


if __name__ == "__main__":
    print("--- Renvoyer ou modifier ---")
    M = [1, 2]
    r = h(M)
    print("1. r vaut :", r)
    print("2. M vaut :", M)

    N = [1, 2]
    s = h2(N)
    print("3. s vaut :", s)
    print("4. N vaut :", N)
    print("   Seule la valeur renvoyee change. La liste est modifiee dans les deux cas.")

    print()
    print("--- Bornes de range ---")
    for ecriture, valeurs in (
        ("range(3)", list(range(3))),
        ("range(1, 4)", list(range(1, 4))),
        ("range(2, 10, 3)", list(range(2, 10, 3))),
        ("range(10, 0, -2)", list(range(10, 0, -2))),
        ("range(5, 5)", list(range(5, 5))),
        ("range(4, 1)", list(range(4, 1))),
    ):
        print(f"{ecriture:<18} -> {valeurs}  ({len(valeurs)} tours)")

    print()
    print("--- Le bug de l'accumulateur ---")
    print("moyenne_fausse([10, 20, 30]) renvoie", moyenne_fausse([10, 20, 30]))
    print("moyenne([10, 20, 30])        renvoie", moyenne([10, 20, 30]))
    print("   Aucune erreur n'est levee : le resultat est simplement faux.")
