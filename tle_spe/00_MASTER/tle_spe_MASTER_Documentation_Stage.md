# Terminale Spécialité Mathématiques — Documentation d'ensemble du stage
## Stage de pré-rentrée 2026-2027

**Source pédagogique unique :** `05_SOURCES/stage_prerentree_terminale_maths.md`

---

## 1. Identité du stage

| Élément | Valeur |
|---|---|
| Intitulé | Stage de pré-rentrée — Entrée en Terminale générale, spécialité mathématiques |
| Année préparée | 2026-2027 |
| Durée | 5 séances de 2 heures, soit 10 heures |
| Effectif | 8 élèves, répartis en 2 groupes selon la seconde spécialité |
| Référentiel | BO spécial n° 8 du 25 juillet 2019 (Terminale), BO spécial n° 1 du 22 janvier 2019 (Première) |
| Évaluation | Sans note ; matrice réussite × confiance, avant et après |

## 2. Objet du stage

Consolider les notions de Première dont la Terminale a un besoin immédiat, en traitant en
priorité les conceptions erronées repérées par le positionnement de pré-rentrée.

Ce n'est ni un rattrapage du programme de Première, ni une anticipation du programme de
Terminale.

## 3. La cohorte

| Groupe | Spécialités conservées | Effectif | Modules suivis |
|---|---|---:|---|
| Groupe 1 | Mathématiques et NSI | 5 | `tle_spe` et `tle_nsi` |
| Groupe 2 | Mathématiques et Physique-Chimie | 3 | `tle_spe` |

Deux élèves suivent en outre l'enseignement optionnel de mathématiques expertes, traité en
module complémentaire de 20 minutes par séance.

Les deux groupes suivent le module de mathématiques **ensemble** : le diagnostic ne fait pas
apparaître de différence de profil entre eux qui justifierait deux progressions distinctes.
La distinction entre groupes porte sur les modules suivis, pas sur le contenu du module de
mathématiques.

## 4. Le dispositif de diagnostic

Chaque élève a passé un positionnement de 18 items couvrant cinq domaines de Première, avec
un **niveau de certitude déclaré de 1 à 4** à chaque item.

Le croisement réussite × confiance distingue quatre situations, qui n'appellent pas le même
traitement :

| | Certitude faible (1-2) | Certitude forte (3-4) |
|---|---|---|
| **Réponse fausse** | Notion absente → **on installe** | Conception erronée → **on confronte** |
| **Réponse juste** | Acquis fragile → **on consolide** | Acquis disponible → **on entretient** |

Un item non traité relève d'une cinquième situation : **on diagnostique** au démarrage.

C'est ce classement — et non un pourcentage de réussite — qui détermine l'ordre de travail de
chaque élève.

## 5. Progression des cinq séances

| Séance | Thème | Domaine de Première consolidé | Chapitre de Terminale préparé |
|---:|---|---|---|
| 1 | Suites numériques : du sens de variation à la récurrence | Suites arithmétiques et géométriques | Suites et limites ; raisonnement par récurrence |
| 2 | Fonction exponentielle : exposants, équations | Fonction exponentielle | Fonction logarithme ; équations différentielles |
| 3 | Second degré : discriminant, signe du trinôme | Second degré | Continuité, TVI ; lecture du signe d'une dérivée |
| 4 | Dérivation : du nombre dérivé aux variations | Dérivation | Dérivée seconde, convexité, primitives |
| 5 | Produit scalaire, probabilités, Python | Produit scalaire ; probabilités | Géométrie dans l'espace ; loi binomiale |

L'ordre est déduit du diagnostic, pas d'une progression de manuel : les domaines portant le
plus de certitudes erronées passent en premier. Les séances 3 et 4 sont enchaînées dans cet
ordre parce que le tableau de signes d'un trinôme, construit en séance 3, est l'outil de la
séance 4.

## 6. Structure d'une séance

| Durée | Phase | Objet |
|---:|---|---|
| 10 min | Question de contrôle | Réactiver la séance précédente, avec certitude déclarée |
| 20 min | Confrontation | Faire produire la conception erronée, puis la mettre en défaut |
| 25 min | Reconstruction | Propriété, démonstration courte, exemple |
| 30 min | Entraînement différencié | Trois parcours, cinq niveaux d'aide |
| 20 min | Ouverture Terminale | Nommer ce que la notion conditionne l'an prochain |
| 15 min | Trace écrite et auto-évaluation | Portfolio, certitude déclarée |

## 7. Individualisation

Chaque élève dispose, sous `04_NOMINATIFS/`, de trois documents construits à partir de **son
propre** bilan de positionnement :

| Document | Contenu |
|---|---|
| Livret individuel | Carte maîtrise × confiance, priorités, parcours séance par séance, reprise item par item de chaque erreur, plan de septembre, fiches de suivi |
| Plan de remédiation ciblée (élève) | Exercices choisis d'après ses propres erreurs, sans corrigé |
| Plan de remédiation ciblée (corrigé enseignant) | Les mêmes exercices, avec corrigé, relevé de maîtrise et notes de conduite |

Aucune de ces pièces n'est un modèle rempli : les erreurs reprises sont les erreurs
effectivement commises par l'élève, avec l'énoncé exact, sa réponse, la réponse attendue et
l'origine de l'erreur telle qu'établie par le bilan.

Ces documents sont générés par `tools/build_terminale.py` à partir de trois sources :

- `content/students_terminale.json` — le registre de la cohorte ;
- `content/diagnostics_terminale.json` — les diagnostics extraits des bilans PDF ;
- `content/items_terminale.json` — la banque d'items, avec pour chacun le lien avec le
  programme de Terminale et un exercice-variante corrigé.

## 8. Confidentialité

Le dossier `04_NOMINATIFS/` contient des données personnelles d'élèves mineurs. Sa
circulation est strictement limitée à Nexus Réussite et à la famille concernée. Aucun
document de ce dossier ne doit être placé dans un pack collectif, ni diffusé à un autre
élève du groupe.

Les documents de `00_MASTER/`, `01_ENSEIGNANT/`, `02_SEANCES/`, `03_EVALUATIONS/` et
`05_SOURCES/` ne contiennent aucun nom d'élève, à l'exception du tableau de bord enseignant,
qui est nominatif et signalé comme tel.

## 9. Critères de réussite du stage

Pour chaque élève :

1. plus aucune conception erronée sur les domaines traités ;
2. la propriété est écrite avant le calcul, sans qu'on le demande ;
3. un contrôle est effectué avant toute certitude de 4 ;
4. l'aide maximale utilisée a diminué entre la séance 1 et la séance 5 ;
5. un plan de travail écrit pour septembre est rempli et argumenté.

## 10. Inventaire des documents

| Chemin | Document | Public |
|---|---|---|
| `00_MASTER/index.md` | Index du module | Tous |
| `00_MASTER/tle_spe_MASTER_Documentation_Stage.md` | Ce document | Tous |
| `01_ENSEIGNANT/tle_spe_Guide_Formateur.md` | Guide du formateur | Enseignant |
| `01_ENSEIGNANT/tle_spe_Tableau_Bord_Enseignant.md` | Tableau de bord nominatif | **Enseignant, confidentiel** |
| `01_ENSEIGNANT/tle_spe_Option_Maths_Expertes.md` | Module mathématiques expertes | Enseignant |
| `02_SEANCES/S1` à `S5` | 4 documents par séance | Enseignant et élèves |
| `03_EVALUATIONS/tle_spe_Mini_Diagnostic_ELEVE.md` | Mini-diagnostic | Élèves |
| `03_EVALUATIONS/tle_spe_Mini_Diagnostic_PROF_Corrige.md` | Corrigé et grille de décision | Enseignant |
| `03_EVALUATIONS/tle_spe_Evaluation_Finale_ELEVE.md` | Évaluation finale | Élèves |
| `03_EVALUATIONS/tle_spe_Evaluation_Finale_PROF_Corrige_Bareme.md` | Corrigé et grille de lecture | Enseignant |
| `03_EVALUATIONS/tle_spe_Portfolio_Individuel.md` | Portfolio du stage | Élèves |
| `04_NOMINATIFS/<Élève>/` | 3 documents par élève | **Confidentiel** |
| `05_SOURCES/stage_prerentree_terminale_maths.md` | Programme complet | Enseignant |

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
