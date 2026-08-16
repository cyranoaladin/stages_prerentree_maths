"""Séance 2 - solution de référence."""

valeurs = [12.5, -3.0, 8.5, 17.0, 0.0]
assert len(valeurs) > 0

somme = 0.0
positives = 0
maximum = valeurs[0]

for valeur in valeurs:
    somme += valeur
    if valeur > 0:
        positives += 1
    if valeur > maximum:
        maximum = valeur

print("somme =", somme)
print("positives =", positives)
print("maximum =", maximum)
