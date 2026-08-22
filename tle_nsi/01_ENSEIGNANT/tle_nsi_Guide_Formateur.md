# Terminale NSI — Guide du formateur
## Stage de pré-rentrée 2026-2027 — 5 séances de 2 heures

**Source pédagogique unique :** `07_SOURCES/stage_prerentree_terminale_nsi.md`

---

## 1. Ce que ce stage est, et ce qu'il n'est pas

**Ce n'est pas** un rattrapage du programme de Première NSI.

**Ce n'est pas** une anticipation du programme de Terminale : ni récursivité, ni structures de
données implémentées, ni SQL travaillé pour lui-même.

**C'est** un travail ciblé sur les prérequis de Première dont la Terminale a un besoin
immédiat, avec une priorité absolue donnée aux conceptions erronées repérées par le
positionnement.

La doctrine, commune aux deux modules du stage :

> Tant qu'un élève croit juste une idée fausse, il ne la corrige pas seul — et aucun
> enseignement empilé par-dessus ne la supprime.

En NSI, cette doctrine prend une forme particulière : **prédire, exécuter, confronter**.
L'élève écrit sa prédiction, puis lance le programme. L'écart entre les deux est l'objet du
travail. C'est la machine qui contredit, pas l'enseignant.

---

## 2. La cohorte

**5 élèves**, tous issus du groupe 1 de la cohorte de pré-rentrée : ils conservent à la fois
la spécialité mathématiques et la spécialité NSI, et suivent donc également le module
`tle_spe`.

Cette double appartenance est utilisée dans le stage : deux articulations explicites sont
prévues (§ 7).

---

## 3. Diagnostic du groupe en une page

| Domaine | Réussite moyenne | Certitudes erronées | À installer | À consolider | Acquis |
|---|---:|---:|---:|---:|---:|
| Représentation binaire | 40,0 % | 1 | 2 | 1 | 1 |
| Algorithmique | 53,3 % | 2 | 1 | 1 | 1 |
| Données en tables | 53,3 % | 3 | 0 | 1 | 1 |
| Programmation | 56,7 % | 3 | 1 | 1 | 0 |
| Types construits | 63,3 % | 3 | 1 | 0 | 1 |
| Booléens et logique | 80,0 % | 1 | 1 | 1 | 2 |
| Architecture et systèmes | 100,0 % | 0 | 0 | 1 | 4 |

Les cinq erreurs structurantes :

1. la conversion entre bases n'est pas installée — **trois élèves à 0 %** ;
2. l'indexation et la mutabilité des tableaux ne sont pas stabilisées ;
3. la valeur renvoyée est confondue avec l'effet de bord ;
4. sélection, projection et jointure ne sont pas nommées ;
5. la précondition d'un algorithme n'est pas conçue comme une condition de validité.

**Architecture et systèmes est acquis par tout le groupe.** Ce domaine ne fait l'objet
d'aucune séance : il est réinvesti quinze minutes en séance 5 et sert de point d'appui.

---

## 4. L'ordre des séances, et pourquoi

| Séance | Thème | Justification |
|---:|---|---|
| 1 | Représentation des données et booléens | Domaine le plus faible (40 %), trois élèves à 0 % |
| 2 | Types construits | Trois certitudes erronées ; **socle de toutes les structures de Terminale** |
| 3 | Programmation | Trois certitudes erronées ; s'appuie sur la mutabilité vue en séance 2 |
| 4 | Algorithmique | Deux certitudes erronées ; suppose les fonctions de la séance 3 |
| 5 | Données en tables, bases de données, systèmes | Trois certitudes erronées ; réinvestissement de l'architecture |

L'ordre respecte les dépendances techniques : la mutabilité (S2) précède les effets de bord
(S3), qui précèdent l'écriture d'algorithmes (S4).

---

## 5. Le rituel de séance

| Durée | Phase | Point de vigilance |
|---:|---|---|
| 10 min | Question de contrôle sur la séance précédente | Certitude déclarée obligatoire |
| 20 min | **Confrontation** | Prédiction écrite **avant** exécution |
| 25 min | Reconstruction | Propriété, exemple exécuté, trace écrite |
| 30 min | Entraînement différencié | Sur machine ; noter l'aide utilisée |
| 20 min | Ouverture Terminale | Nommer explicitement ce que la notion conditionne |
| 15 min | Trace écrite et auto-évaluation | Certitude déclarée, portfolio |

### La phase de confrontation, en détail

1. **Poser la question sans support.** Aucun rappel préalable.
2. **Faire écrire la prédiction**, avec la certitude. Ne pas commenter — un « attention »
   prononcé ici suffit à faire changer d'avis sans qu'aucune conception ait été traitée.
3. **Faire exécuter.** C'est la machine qui contredit.
4. **Faire verbaliser** la contradiction par un élève, avec ses mots.
5. **Seulement alors, reconstruire.**

Ne pas distribuer les scripts de `06_CODE/` avant que les prédictions soient écrites.

Si personne ne produit l'erreur attendue, ne pas la fabriquer : passer à la reconstruction et
reverser le temps gagné au parcours d'approfondissement.

---

## 6. Différenciation

### Les cinq pistes

| Parcours | Attribution | Ce qui change |
|---|---|---|
| Diagnostiquer | Le domaine de la séance a été laissé sans réponse | Question 0 puis exercices 1 et 2 ; établir ce que l'élève sait avant toute remédiation |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 | La réponse fausse est produite avant d'être corrigée, puis exemple exécuté fourni |
| Installer | Réponse fausse avec une certitude basse | Exemple exécuté fourni, table de trace pré-remplie |
| Consolider | Le domaine est réussi mais hésitant | Pas d'exemple ; spécification et tests exigés |
| Entretenir | Le domaine est acquis avec certitude | Problème ouvert, comparaison d'algorithmes |

Les cinq pistes reprennent une à une les postures de la carte maîtrise $\times$ confiance : un élève qui n'a pas répondu et un élève qui s'est trompé en étant sûr de lui n'ont pas le même besoin. Ce sont les libellés que porte le livret individuel de chaque élève et le tableau d'aiguillage de chaque fiche de séance.

L'attribution est **relue à chaque séance** dans le livret individuel.

### La piste excellence et l'atelier Terminale

La NSI ne comporte pas d'option annuelle : l'équivalent de l'ouverture mathématiques expertes
vient donc du programme de Terminale de la discipline lui-même.

| Séance | Piste excellence — les deux derniers exercices | Atelier Terminale — 20 minutes |
|---:|---|---|
| 1 | Complément à deux ; réfuter « ajouter un bit double le maximum » | Adressage IP et masque de sous-réseau, par le ET bit à bit |
| 2 | File par deux piles ; mutabilité de l'argument par défaut | Arbre binaire de recherche : insertion, parcours infixe, hauteur |
| 3 | Second maximum en un parcours ; portée et `UnboundLocalError` | Programmation orientée objet : écrire une classe `Pile` |
| 4 | Dichotomie : variant, invariant, coût ; réfuter « $O$ décide toujours » | Diviser pour régner : le tri fusion et son coût |
| 5 | Schéma relationnel, jointure, intégrité ; CSV contre base de données | Processus, états, interblocage : le cycle dans un graphe |

L'atelier n'est pas réservé aux élèves sans erreur : il s'adresse à quiconque a terminé sa
piste avant la fin du temps différencié. Il se distingue de la rubrique « Ce que la Terminale
en fera », qui se lit : ici, l'élève traite des questions.

### Les cinq aides

| Aide | Contenu |
|---|---|
| A | Rappel de la syntaxe ou de la propriété, sans application |
| B | Première ligne écrite |
| C | Exemple exécuté analogue, avec sa sortie |
| D | Découpage en sous-questions ou sous-fonctions |
| E | Squelette de code à compléter |

L'élève note la lettre utilisée. La décroissance de l'aide maximale entre les séances 1 et 5
est l'un des cinq critères de réussite.

---

## 7. Articulation avec le module de mathématiques

Les cinq élèves suivent les deux modules. Deux articulations sont explicites et doivent être
nommées devant eux :

| Articulation | Où | Contenu |
|---|---|---|
| Boucles et bornes | `tle_spe` $S5 \leftrightarrow$ `tle_nsi` S3 | Le calcul des termes d'une suite en Python est écrit en mathématiques, spécifié et testé en NSI |
| Contre-exemple | `tle_spe` $S4 \leftrightarrow$ `tle_nsi` S3 et S4 | Réfuter une affirmation par un cas qui échoue est le même geste dans les deux disciplines |

Un troisième lien est utile à signaler : le raisonnement sur les ordres de grandeur
(séance 4 NSI) rejoint celui des puissances et des croissances comparées en mathématiques.

---

## 8. Gérer les deux élèves quasi complets

Deux élèves présentent un positionnement quasi complet. Ils ne doivent ni s'ennuyer, ni servir
de dépanneurs techniques.

**Ce qui est prévu.**

- Parcours approfondissement dès la séance 1.
- Rôle de **relecteur de spécification** : lire la fonction d'un camarade et dire si la
  spécification décrit bien ce que fait le code — sans corriger le code. Cette tâche travaille
  exactement ce que le positionnement ne mesurait pas.
- En séance 4, la comparaison expérimentale des deux versions de Fibonacci, avec
  chronométrage.

**Ce qu'il faut éviter.** Leur faire déboguer le code d'un camarade : l'élève en difficulté
perd alors la confrontation, qui est le moment le plus utile de la séance.

---

## 9. Ce qu'il faut refuser

| Situation | Pourquoi refuser |
|---|---|
| Une exécution avant la prédiction écrite | La confrontation perd tout son effet |
| Une boucle écrite sans table de trace | L'erreur de raisonnement devient invisible |
| Une fonction sans spécification | C'est le geste attendu en mise au point en Terminale |
| Une fonction avec un seul test | Le cas limite est celui qui révèle les bugs |
| Un algorithme utilisé sans énoncé de sa précondition | C'est l'erreur silencieuse de la séance 4 |

---

## 10. Environnement technique

- **Python 3**, sans aucune bibliothèque externe. Les scripts de `06_CODE/` fonctionnent hors
  réseau.
- Un poste par élève si possible, sinon par binôme.
- `s5_tables.py` doit être lancé **depuis le dossier `06_CODE/`** : il lit `eleves.csv` à côté
  de lui.
- `s3_fonctions.py` contient volontairement une fonction fausse (`moyenne_fausse`) qui ne lève
  aucune exception. C'est intentionnel : le point à faire voir est précisément l'absence
  d'erreur.
- Pas de SGBD requis : le SQL de la séance 5 est écrit et lu, pas exécuté. Si un environnement
  SQL est disponible, l'exécution est un plus, non un prérequis.

---

## 11. Calendrier de préparation

| Quand | Quoi |
|---|---|
| $J - 7$ | Lire les cinq livrets individuels ; repérer les parcours de la séance 1 |
| $J - 3$ | Vérifier que les cinq scripts de `06_CODE/` s'exécutent sur les postes |
| $J - 3$ | Préparer les supports : réglettes, cartes, bandes d'indices, tables imprimées |
| $J - 1$ | Photocopier les fiches élèves, les mémentos et les portfolios |
| Séance 3 | Faire passer le mini-diagnostic pratique (20 min) |
| Séance 3, fin | Dépouiller ; ajuster les séances 4 et 5 en conséquence |
| Séance 5, fin | Dépouiller l'évaluation finale ; remplir la comparaison initiale/finale |
| J+1 | Restituer aux familles ; archiver les portfolios |

---

## 12. Documents du module

| Dossier | Contenu |
|---|---|
| `00_MASTER/` | Index et documentation d'ensemble |
| `01_ENSEIGNANT/` | Ce guide, le tableau de bord |
| `02_SEANCES/S1` à `S5` | Fiche professeur, fiche élève, supports pratiques, cartes d'aide |
| `03_EVALUATIONS/` | Mini-diagnostic pratique, évaluation finale |
| `04_PORTFOLIO/` | Mémento Python, portfolio du stage |
| `05_NOMINATIFS/` | **Confidentiel** — un dossier par élève |
| `06_CODE/` | Scripts exécutables des cinq séances |
| `07_SOURCES/` | Programme complet du stage, source unique |

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
