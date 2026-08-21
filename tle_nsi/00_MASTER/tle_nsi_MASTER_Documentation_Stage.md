# Terminale NSI — Documentation d'ensemble du stage
## Stage de pré-rentrée 2026-2027

**Source pédagogique unique :** `07_SOURCES/stage_prerentree_terminale_nsi.md`

---

## 1. Identité du stage

| Élément | Valeur |
|---|---|
| Intitulé | Stage de pré-rentrée — Entrée en Terminale, spécialité NSI |
| Année préparée | 2026-2027 |
| Durée | 5 séances de 2 heures, soit 10 heures |
| Effectif | 5 élèves, tous du groupe 1 (mathématiques et NSI) |
| Référentiel | BO spécial n° 8 du 25 juillet 2019 (Terminale), BO spécial n° 1 du 22 janvier 2019 (Première) |
| Environnement | Python 3, sans bibliothèque externe, hors réseau |
| Évaluation | Sans note ; matrice réussite × confiance, avant et après |

## 2. Objet du stage

Consolider les notions de Première NSI dont la Terminale a un besoin immédiat, en traitant en
priorité les conceptions erronées repérées par le positionnement.

Ni rattrapage du programme de Première, ni anticipation du programme de Terminale.

## 3. La méthode : prédire, exécuter, confronter

En NSI, la confrontation ne se conduit pas au tableau : elle se conduit à l'écran.

1. L'élève **écrit sa prédiction** et sa certitude, sans indice préalable.
2. Il **exécute**.
3. Il **constate l'écart** — c'est la machine qui contredit, pas l'enseignant.
4. Il **verbalise** la contradiction.
5. **Alors seulement** la notion est reconstruite.

C'est ce qui rend la correction durable : une conception erronée cède à une réfutation
observée, rarement à une explication.

## 4. Le dispositif de diagnostic

Positionnement de 18 items couvrant sept domaines, avec un **niveau de certitude déclaré de 1
à 4** à chaque item.

| | Certitude faible (1-2) | Certitude forte (3-4) |
|---|---|---|
| **Réponse fausse** | Notion absente → **on installe** | Conception erronée → **on confronte** |
| **Réponse juste** | Acquis fragile → **on consolide** | Acquis disponible → **on entretient** |

C'est ce classement, et non un pourcentage de réussite, qui détermine l'ordre de travail de
chaque élève.

## 5. Progression des cinq séances

| Séance | Thème | Domaine de Première consolidé | Bloc de Terminale préparé |
|---:|---|---|---|
| 1 | Représentation des données et booléens | Types et valeurs de base | Bases de données ; sécurisation des communications ; invariants |
| 2 | Types construits | p-uplets, tableaux, dictionnaires | Structures de données : piles, files, arbres, graphes |
| 3 | Programmation | Langages et programmation | Récursivité, modularité, mise au point |
| 4 | Algorithmique | Dichotomie, tris, coût | Diviser pour régner, programmation dynamique, graphes |
| 5 | Données en tables, systèmes | Traitement de données en tables ; architectures | Bases de données et SQL ; processus, ordonnancement, réseaux |

L'ordre est déduit du diagnostic et respecte les dépendances techniques : la mutabilité
(séance 2) précède les effets de bord (séance 3), qui précèdent l'écriture d'algorithmes
(séance 4).

## 6. Structure d'une séance

| Durée | Phase | Objet |
|---:|---|---|
| 10 min | Question de contrôle | Réactiver la séance précédente, avec certitude déclarée |
| 20 min | Confrontation | Prédire, exécuter, constater l'écart |
| 25 min | Reconstruction | Propriété, exemple exécuté, trace écrite |
| 30 min | Entraînement différencié | Trois parcours, cinq niveaux d'aide, sur machine |
| 20 min | Ouverture Terminale | Nommer ce que la notion conditionne l'an prochain |
| 15 min | Trace écrite et auto-évaluation | Portfolio, certitude déclarée |

## 7. Individualisation

Chaque élève dispose, sous `05_NOMINATIFS/`, de trois documents construits à partir de **son
propre** bilan :

| Document | Contenu |
|---|---|
| Livret individuel | Carte maîtrise × confiance, priorités, parcours séance par séance, reprise item par item de chaque erreur, plan de septembre, fiches de suivi |
| Plan de remédiation ciblée (élève) | Exercices choisis d'après ses propres erreurs, sans corrigé |
| Plan de remédiation ciblée (corrigé enseignant) | Les mêmes exercices, avec corrigé, relevé de maîtrise et notes de conduite |

Les erreurs reprises sont les erreurs effectivement commises, avec l'énoncé exact, la réponse
donnée, la réponse attendue et l'origine de l'erreur telle qu'établie par le bilan.

Ces documents sont générés par `tools/build_terminale.py` à partir de :

- `content/students_terminale.json` — le registre de la cohorte ;
- `content/diagnostics_terminale.json` — les diagnostics extraits des bilans PDF ;
- `content/items_terminale.json` — la banque d'items, avec le lien vers le programme de
  Terminale et un exercice-variante corrigé.

## 8. Articulation avec le module de mathématiques

Les cinq élèves suivent aussi `tle_spe`. Deux articulations sont explicites :

| Articulation | Où | Contenu |
|---|---|---|
| Boucles et bornes | `tle_spe` S5 ↔ `tle_nsi` S3 | Les termes d'une suite calculés en mathématiques sont spécifiés et testés en NSI |
| Contre-exemple | `tle_spe` S4 ↔ `tle_nsi` S3 et S4 | Réfuter par un cas qui échoue est le même geste dans les deux disciplines |

## 9. Confidentialité

Le dossier `05_NOMINATIFS/` contient des données personnelles d'élèves mineurs. Sa circulation
est strictement limitée à Nexus Réussite et à la famille concernée.

Les autres dossiers ne contiennent aucun nom d'élève, à l'exception du tableau de bord
enseignant, qui est nominatif et signalé comme tel.

## 10. Critères de réussite du stage

1. Plus aucune conception erronée sur les domaines traités.
2. Une table de trace est écrite avant toute exécution, sans qu'on le demande.
3. Chaque fonction écrite porte une spécification et deux tests, dont un cas limite.
4. L'aide maximale utilisée a diminué entre la séance 1 et la séance 5.
5. Un plan de travail écrit pour septembre est rempli et argumenté.

## 11. Inventaire des documents

| Chemin | Document | Public |
|---|---|---|
| `00_MASTER/index.md` | Index du module | Tous |
| `00_MASTER/tle_nsi_MASTER_Documentation_Stage.md` | Ce document | Tous |
| `00_MASTER/tle_nsi_Programme_Stage_PUBLIC.md` | Présentation aux familles | Familles |
| `00_MASTER/tle_nsi_QUICK_START.md` | Démarrage rapide | Enseignant |
| `01_ENSEIGNANT/tle_nsi_Guide_Formateur.md` | Guide du formateur | Enseignant |
| `01_ENSEIGNANT/tle_nsi_Tableau_Bord_Enseignant.md` | Tableau de bord nominatif | **Enseignant, confidentiel** |
| `02_SEANCES/S1` à `S5` | 4 documents par séance | Enseignant et élèves |
| `03_EVALUATIONS/tle_nsi_Mini_Diagnostic_Pratique_ELEVE.md` | Épreuve sur machine | Élèves |
| `03_EVALUATIONS/tle_nsi_Mini_Diagnostic_Pratique_PROF_Corrige.md` | Corrigé et grille de décision | Enseignant |
| `03_EVALUATIONS/tle_nsi_Evaluation_Finale_ELEVE.md` | Évaluation finale | Élèves |
| `03_EVALUATIONS/tle_nsi_Evaluation_Finale_PROF_Corrige_Bareme.md` | Corrigé et grille de lecture | Enseignant |
| `04_PORTFOLIO/tle_nsi_Memento_Python_Terminale_ELEVE.md` | Mémento Python | Élèves |
| `04_PORTFOLIO/tle_nsi_Portfolio_Individuel.md` | Portfolio du stage | Élèves |
| `05_NOMINATIFS/<Élève>/` | 3 documents par élève | **Confidentiel** |
| `06_CODE/` | 5 scripts et un jeu de données | Enseignant et élèves |
| `07_SOURCES/stage_prerentree_terminale_nsi.md` | Programme complet | Enseignant |

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
