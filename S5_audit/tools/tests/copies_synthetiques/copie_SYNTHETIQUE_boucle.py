# JEU DE DONNEES SYNTHETIQUE — boucle infinie volontaire.
def maximum(L):
    m = L[0]
    i = 0
    while i < len(L):
        if L[i] > m:
            m = L[i]
    return m
