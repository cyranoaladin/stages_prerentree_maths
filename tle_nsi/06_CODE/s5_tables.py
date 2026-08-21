"""Seance 5 - Donnees en tables. A lancer depuis le dossier 06_CODE."""

import csv
import os

CHEMIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eleves.csv")


def charger(chemin=CHEMIN):
    """Renvoie la liste des enregistrements du fichier CSV.
    DictReader traite la premiere ligne comme l'en-tete : elle n'est pas un enregistrement."""
    with open(chemin, encoding="utf-8") as fichier:
        return list(csv.DictReader(fichier))


def selection(table, seuil):
    """Selection : on garde les LIGNES dont la note depasse le seuil."""
    return [ligne for ligne in table if int(ligne["note"]) > seuil]


def projection(table, colonnes):
    """Projection : on garde les COLONNES demandees."""
    return [{colonne: ligne[colonne] for colonne in colonnes} for ligne in table]


if __name__ == "__main__":
    table = charger()

    print("--- Enregistrements et descripteurs ---")
    with open(CHEMIN, encoding="utf-8") as fichier:
        nb_lignes = sum(1 for _ in fichier)
    print("lignes du fichier   :", nb_lignes)
    print("enregistrements     :", len(table), "  (l'en-tete n'en est pas un)")
    print("descripteurs        :", len(table[0]))

    print()
    print("--- Selection : note > 12 ---")
    retenus = selection(table, 12)
    for ligne in retenus:
        print(" ", ligne)

    print()
    print("--- Projection : nom et note ---")
    for ligne in projection(retenus, ["nom", "note"]):
        print(" ", ligne)

    print()
    print("En SQL, ces deux operations s'ecrivent en une requete :")
    print("  SELECT nom, note FROM eleves WHERE note > 12 ;")
