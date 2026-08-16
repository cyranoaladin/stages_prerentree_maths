"""Séance 4 - structures et CSV - solution de référence."""
import csv

def charger_mesures(chemin):
    """Charge le CSV et convertit les valeurs numériques."""
    mesures = []
    with open(chemin, encoding="utf-8", newline="") as fichier:
        for ligne in csv.DictReader(fichier):
            mesure = {
                "id": ligne["id"],
                "date": ligne["date"],
                "temperature": float(ligne["temperature"]),
                "humidite": int(ligne["humidite"]),
                "statut": ligne["statut"],
            }
            mesures.append(mesure)
    return mesures

def filtrer_alertes(mesures):
    """Renvoie les mesures dont le statut vaut ALERTE."""
    return [mesure for mesure in mesures if mesure["statut"] == "ALERTE"]

if __name__ == "__main__":
    mesures = charger_mesures("mesures_capteurs.csv")
    print(filtrer_alertes(mesures))
