"""Seance 1 - Representation des donnees. A executer apres avoir ecrit ses predictions."""


def valeur_decimale(chaine_binaire):
    """Prend une chaine de '0' et de '1', renvoie l'entier correspondant."""
    total = 0
    for bit in chaine_binaire:
        total = total * 2 + int(bit)
    return total


def en_binaire(entier):
    """Prend un entier positif, renvoie son ecriture binaire sous forme de chaine."""
    if entier == 0:
        return "0"
    restes = []
    while entier > 0:
        restes.append(str(entier % 2))
        entier = entier // 2
    # les restes se lisent de bas en haut : on inverse
    return "".join(reversed(restes))


assert valeur_decimale("10110") == 22
assert valeur_decimale("1111") == 15
assert en_binaire(22) == "10110"
assert en_binaire(45) == "101101"
assert en_binaire(0) == "0"


if __name__ == "__main__":
    print("--- Outils Python ---")
    print("bin(22)         =", bin(22))
    print("int('10110', 2) =", int("10110", 2))
    print("hex(42)         =", hex(42))
    print("int('2A', 16)   =", int("2A", 16))

    print()
    print("--- Nos propres fonctions ---")
    for n in (5, 13, 22, 45, 100, 255):
        binaire = en_binaire(n)
        print(f"{n:>4} -> {binaire:>8}  (verification : {valeur_decimale(binaire)})")

    print()
    print("--- Le piege de l'hexadecimal ---")
    print("F vaut", int("F", 16), "et non 16.")
    print("0xFF vaut", int("FF", 16), ", soit le plus grand entier sur 8 bits.")
