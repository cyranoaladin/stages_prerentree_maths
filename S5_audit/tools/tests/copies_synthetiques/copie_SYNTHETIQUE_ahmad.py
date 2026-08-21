# JEU DE DONNEES SYNTHETIQUE — copie fictive, ne correspond a aucun eleve reel.
# Erreurs volontaires : moyenne affiche au lieu de renvoyer ; chercher renvoie 0
# en cas d'absence ; premier_negatif accepte zero.

def triple(n):
    return 3 * n

def somme(a, b):
    print(a + b)

def est_negatif(n):
    return n < 0

def moyenne(valeurs):
    total = 0
    for v in valeurs:
        total = total + v
    print(total / len(valeurs))

def indice_de(L, cible):
    for i in range(len(L)):
        if L[i] == cible:
            return i
    return -1

def chercher(mesures, identifiant):
    for i in range(len(mesures)):
        if mesures[i]["id"] == identifiant:
            return i
    return 0

def premier_negatif(L):
    for i in range(len(L)):
        if L[i] <= 0:
            return i
    return -1
