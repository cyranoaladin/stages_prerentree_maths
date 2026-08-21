"""Séance 4 - structures et CSV - version élève."""
import csv

def charger_mesures(chemin):
    # TODO: utiliser csv.DictReader et convertir temperature/humidite.
    pass

def filtrer_alertes(mesures):
    # TODO: renvoyer une nouvelle liste.
    pass

if __name__ == "__main__":
    mesures = charger_mesures("mesures_capteurs.csv")
    print(filtrer_alertes(mesures))
