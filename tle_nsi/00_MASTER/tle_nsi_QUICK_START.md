# Terminale NSI — Démarrage rapide

## Avant la première séance

1. Lire le guide du formateur : `01_ENSEIGNANT/tle_nsi_Guide_Formateur.md`.
2. Lire les cinq livrets individuels sous `05_NOMINATIFS/` et noter, pour la séance 1, le
   parcours de chaque élève (consolidation, maîtrise ou approfondissement).
3. Vérifier que les scripts s'exécutent sur les postes :

```bash
cd tle_nsi/06_CODE
python3 s1_representation.py
python3 s2_types_construits.py
python3 s3_fonctions.py
python3 s4_algorithmique.py
python3 s5_tables.py
```

Tous doivent se terminer sans erreur. `s3_fonctions.py` affiche un résultat volontairement
faux (`moyenne_fausse`) : c'est attendu, il ne lève pas d'exception.

4. Photocopier, pour chaque élève : la fiche élève des cinq séances, le portfolio, le mémento
   Python.

## Pendant une séance

| Ordre | Action |
|---:|---|
| 1 | Question de contrôle sur la séance précédente, certitude déclarée |
| 2 | Confrontation : **faire écrire la prédiction avant de distribuer le script** |
| 3 | Exécution, puis verbalisation de l'écart par un élève |
| 4 | Reconstruction et trace écrite |
| 5 | Entraînement différencié, relever l'aide utilisée par chacun |
| 6 | Ouverture Terminale |
| 7 | Fiche de synthèse dans le portfolio |

## Points de vigilance

- Ne pas distribuer les scripts de `06_CODE/` avant que les prédictions soient écrites.
- `s5_tables.py` se lance **depuis** `06_CODE/` : il lit `eleves.csv` à côté de lui.
- L'attribution des parcours se relit **à chaque séance** dans le livret individuel, pas une
  fois pour toutes.

## Confidentialité

`05_NOMINATIFS/` contient des données personnelles d'élèves mineurs. Ne jamais placer l'un de
ces documents dans un pack collectif, ni le remettre à un autre élève du groupe.

## Après le stage

1. Dépouiller l'évaluation finale avec `03_EVALUATIONS/tle_nsi_Evaluation_Finale_PROF_Corrige_Bareme.md`.
2. Remplir la comparaison initiale / finale dans chaque livret.
3. Faire remplir le plan de septembre.
4. Restituer aux familles ; archiver les portfolios.
