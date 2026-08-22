# Terminale NSI — Code du stage

Ce dossier contient les scripts utilisés pendant les cinq séances. Ils sont conçus pour être
exécutés tels quels avec **Python 3, sans aucune bibliothèque externe**, et fonctionnent hors
réseau.

## Inventaire

| Fichier | Séance | Usage |
|---|---:|---|
| `s1_representation.py` | 1 | Conversions et vérification |
| `s2_types_construits.py` | 2 | Confrontation « modifier ou construire » ; pile, file, arbre |
| `s3_fonctions.py` | 3 | Confrontation retour / effet de bord ; script à déboguer |
| `s4_algorithmique.py` | 4 | Dichotomie sur tableau non trié ; comparaison de coûts |
| `s5_tables.py` | 5 | Sélection et projection sur un CSV |
| `eleves.csv` | 5 | Jeu de données de la séance 5 |

## Conduite

Ces scripts servent la démarche du module : **prédire, exécuter, confronter**. L'élève écrit
sa prédiction sur sa fiche **avant** de lancer le script. C'est l'écart entre la prédiction et
la sortie qui est l'objet du travail, pas la sortie elle-même.

Ne pas distribuer les scripts avant que les prédictions soient écrites.

## Vérification

Chaque script est exécutable et se termine sans erreur, à l'exception de `s3_fonctions.py`
dont la dernière section contient **volontairement** une fonction fausse — elle ne lève pas
d'exception, elle renvoie un résultat incorrect, ce qui est précisément le point à faire voir.

```bash
python3 s1_representation.py
python3 s2_types_construits.py
python3 s3_fonctions.py
python3 s4_algorithmique.py
python3 s5_tables.py     # doit etre lance depuis ce dossier, il lit eleves.csv
```
