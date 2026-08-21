---
title: "Guide d’installation Python - Première NSI"
author: "Nexus Réussite"
lang: fr-FR
subject: "Stage de pré-rentrée - Première NSI"
---
<div class="cover">
<img src="logo_slogan_nexus.png" alt="Nexus Réussite">
<div class="kicker">Pré-rentrée 2026-2027</div>
<h1>Installer l’environnement</h1>
<div class="subtitle">Python 3 et Thonny</div>
<div class="meta">5 séances de 2 heures - 10 heures<br>Python 3 - théorie, pratique, tests et projet<br>Guide famille et élève</div>
</div>

## Configuration recommandée

- un ordinateur portable par élève ;
- Python 3.11 ou supérieur ;
- Thonny récent ;
- 2 Go d’espace libre ;
- un dossier local de travail sauvegardé ;
- le pack de code élève correspondant, sans solution.

## Installation

## Windows et macOS

1. Télécharger Thonny depuis son site officiel.
2. Installer avec les options par défaut.
3. Ouvrir Thonny.
4. Vérifier dans **Outils > Options > Interpréteur** que Python 3 est sélectionné.
5. Exécuter :

```python
print("Nexus NSI prêt")
```

## Linux

Installer Python 3 et Thonny avec le gestionnaire de paquets de la distribution ou l’installateur officiel. Vérifier dans un terminal :

```bash
python3 --version
```

## Packs de code à utiliser

Dans `09_PACKS_CODE/` :

- `1re_nsi_CODE_ELEVE_COMMUN.zip` : fichiers communs sans solution ;
- `1re_nsi_CODE_Ahmad_BELDI.zip` : fichiers et consignes du parcours Fondations ;
- `1re_nsi_CODE_Ahmed_BENHADJ_SALEM.zip` : fichiers et consignes du parcours Reprise/Examen ;
- `1re_nsi_CODE_ENSEIGNANT.zip` : solutions et tests - à ne jamais copier sur un poste élève.

## Arborescence conseillée

```text
Premiere_NSI/
├── S1_variables_conditions/
├── S2_boucles/
├── S3_fonctions_tests/
├── S4_structures_csv/
├── S5_projet_capteurs/
└── sauvegardes/
```

## Vérification de l’environnement

Créer `test_installation.py` :

```python
from pathlib import Path

print("Python fonctionne")
print("Dossier courant :", Path.cwd())
assert 2 + 2 == 4
```

Le programme doit s’exécuter sans erreur.

## Règles de sauvegarde

- ne jamais écraser la dernière version qui fonctionne ;
- utiliser des noms comme `projet_v01.py`, `projet_v02.py` ;
- conserver `mesures_capteurs.csv` avec le projet ;
- enregistrer après chaque jalon ;
- ne jamais stocker de mot de passe, clé ou donnée personnelle dans un script ;
- ne pas utiliser de vraies données d’élèves.

## En cas de problème

Noter le message exact, le système, la version de Python, le fichier et l’étape qui échoue. Joindre une capture du message complet ; ne pas se contenter de « ça ne marche pas ».
