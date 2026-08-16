"""Projet final - solution de référence, bibliothèque standard uniquement."""
from __future__ import annotations
import csv

def charger_mesures(chemin: str) -> list[dict]:
    """Charge et valide un fichier de mesures synthétiques."""
    mesures: list[dict] = []
    ids: set[str] = set()
    with open(chemin, encoding="utf-8", newline="") as fichier:
        for numero, ligne in enumerate(csv.DictReader(fichier), start=2):
            identifiant = ligne["id"].strip()
            if not identifiant:
                raise ValueError(f"identifiant absent ligne {numero}")
            if identifiant in ids:
                raise ValueError(f"identifiant dupliqué: {identifiant}")
            ids.add(identifiant)
            mesure = {
                "id": identifiant,
                "date": ligne["date"].strip(),
                "temperature": float(ligne["temperature"]),
                "humidite": int(ligne["humidite"]),
                "statut": ligne["statut"].strip(),
            }
            mesures.append(mesure)
    return mesures

def temperatures(mesures: list[dict]) -> list[float]:
    return [mesure["temperature"] for mesure in mesures]

def statistiques(valeurs: list[float]) -> tuple[float, float, float]:
    assert len(valeurs) > 0
    minimum = valeurs[0]
    maximum = valeurs[0]
    total = 0.0
    for valeur in valeurs:
        if valeur < minimum:
            minimum = valeur
        if valeur > maximum:
            maximum = valeur
        total += valeur
    return minimum, maximum, total / len(valeurs)

def alertes(mesures: list[dict]) -> list[dict]:
    return [m for m in mesures if m["statut"] == "ALERTE"]

def indice_capteur(mesures: list[dict], identifiant: str) -> int | None:
    for i in range(len(mesures)):
        if mesures[i]["id"] == identifiant:
            return i
    return None

def tri_insertion_temperature(mesures: list[dict]) -> list[dict]:
    resultat = mesures.copy()
    for i in range(1, len(resultat)):
        element = resultat[i]
        j = i - 1
        while j >= 0 and resultat[j]["temperature"] > element["temperature"]:
            resultat[j + 1] = resultat[j]
            j -= 1
        resultat[j + 1] = element
    return resultat

def afficher_rapport(mesures: list[dict]) -> None:
    valeurs = temperatures(mesures)
    minimum, maximum, moyenne = statistiques(valeurs)
    print(f"Nombre de mesures : {len(mesures)}")
    print(f"Température minimale : {minimum:.1f}")
    print(f"Température maximale : {maximum:.1f}")
    print(f"Température moyenne : {moyenne:.2f}")
    print(f"Alertes : {len(alertes(mesures))}")

if __name__ == "__main__":
    mesures = charger_mesures("mesures_capteurs.csv")
    afficher_rapport(mesures)
