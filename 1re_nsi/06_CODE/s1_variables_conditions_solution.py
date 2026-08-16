"""Séance 1 - solution de référence."""

temperature = 28.4

if temperature < 0:
    etat = "gel"
elif temperature <= 30:
    etat = "normal"
else:
    etat = "alerte"

print(temperature, etat)
