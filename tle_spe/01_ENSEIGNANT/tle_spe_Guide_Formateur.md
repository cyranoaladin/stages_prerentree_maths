# Terminale Spécialité Mathématiques — Guide du formateur
## Stage de pré-rentrée 2026-2027 — 10 heures, du 24 au 28 août 2026

**Nexus Réussite**, centre d'accompagnement scolaire · 2 heures par jour, 5 jours consécutifs.

**Source pédagogique unique :** `05_SOURCES/stage_prerentree_terminale_maths.md`

---

## 1. Ce que ce stage est, et ce qu'il n'est pas

**Ce n'est pas** un rattrapage du programme de Première : dix heures n'y suffiraient pas, et
la plupart des élèves n'en ont pas besoin.

**Ce n'est pas** une anticipation du programme de Terminale : introduire la récurrence, les
limites ou le logarithme avant la rentrée désorganiserait le travail du professeur de
l'année.

**C'est** un travail ciblé sur les prérequis de Première dont la Terminale a un besoin
immédiat, avec une priorité absolue donnée aux conceptions erronées repérées par le
positionnement.

Une phrase résume la doctrine :

> Tant qu'un élève croit juste une idée fausse, il ne la corrige pas seul — et aucun
> enseignement empilé par-dessus ne la supprime.

---

## 2. La cohorte

| Groupe | Stages suivis | Élèves |
|---|---|---:|
| Groupe 1 | Mathématiques et NSI | 4 |
| Groupe 2 | Mathématiques | 4 |

Les deux groupes suivent **le même module de mathématiques**, ensemble. Le groupe 1 suit en
outre le module `tle_nsi`.

Dans le groupe 2, deux élèves suivent aussi la physique-chimie — aucun stage n'est organisé
pour cette spécialité ici — et deux ne suivent que les mathématiques. Deux élèves de la
cohorte suivent l'option mathématiques expertes, **sans stage dédié**.

**Une élève n'a pas passé le positionnement en mathématiques** : inscrite après la campagne,
elle reçoit un livret « diagnostic à établir ». **Ne rien inférer à sa place.** Prévoir un jeu
du positionnement papier pour la première séance, et 25 minutes pour la passation.

---

## 3. Diagnostic du groupe en une page

Sur les sept élèves ayant passé le positionnement en mathématiques ; la huitième est
diagnostiquée en séance 1.

| Domaine | Réussite moyenne | Certitudes erronées | À installer | À consolider | Acquis | Sans réponse |
|---|---:|---:|---:|---:|---:|---:|
| Fonction exponentielle | 57,1 % | 3 | 1 | 0 | 3 | 0 |
| Suites numériques | 63,3 % | 4 | 1 | 0 | 2 | 0 |
| Produit scalaire | 71,4 % | 1 | 2 | 0 | 4 | 0 |
| Second degré | 76,2 % | 3 | 0 | 0 | 3 | 1 |
| Dérivation | 81,8 % | 2 | 2 | 1 | 2 | 0 |

Les cinq erreurs structurantes du groupe :

1. le sens de variation d'une suite géométrique déduit du **signe** de la raison au lieu de
   sa position par rapport à 1 ;
2. le sens de variation d'une suite récurrente annoncé sans calcul de u(n+1) − u_n ;
3. les exposants **additionnés** lors d'une division d'exponentielles ;
4. la règle du signe du trinôme appliquée sans regarder le signe du coefficient dominant ;
5. le signe de f' confondu avec le signe de f.

---

## 4. L'ordre des séances, et pourquoi

L'ordre n'est pas celui d'un manuel : il est déduit du nombre de certitudes erronées par
domaine, puis ajusté pour que chaque séance prépare la suivante.

| Séance | Thème | Justification |
|---:|---|---|
| 1 | Suites numériques | Quatre certitudes erronées, le maximum du groupe ; premier chapitre de Terminale |
| 2 | Fonction exponentielle | Domaine le plus faible (57,1 %) ; conditionne le logarithme dès octobre |
| 3 | Second degré et signe | Trois certitudes erronées ; **fournit l'outil de la séance 4** |
| 4 | Dérivation | Profil le plus hétérogène ; s'appuie sur le tableau de signes de la séance 3 |
| 5 | Produit scalaire, probabilités, Python | Domaines peu porteurs d'erreurs ; mise en perspective et évaluation |

Ne pas réordonner les séances 3 et 4 : le tableau de signes d'un trinôme est construit en
séance 3 et réutilisé tel quel en séance 4 sur le signe de f'.

---

## 5. Le rituel de séance

Chaque séance suit la même structure. Sa régularité est ce qui rend le stage lisible pour
les élèves.

| Durée | Phase | Point de vigilance |
|---:|---|---|
| 10 min | Question de contrôle sur la séance précédente | Certitude déclarée obligatoire |
| 20 min | **Confrontation** | Faire produire la réponse fausse **avant** tout commentaire |
| 25 min | Reconstruction | Propriété, démonstration courte, exemple |
| 30 min | Entraînement différencié | Noter l'aide utilisée par chaque élève |
| 20 min | Ouverture Terminale | Nommer explicitement ce que la notion conditionne |
| 15 min | Trace écrite et auto-évaluation | Certitude déclarée, portfolio |

### La phase de confrontation, en détail

C'est la phase qui fait le stage. Elle se conduit en cinq temps, toujours les mêmes :

1. **Poser la question sans support.** Aucun rappel préalable, aucun indice.
2. **Recueillir par écrit**, avec la certitude, et **ne pas commenter**. Un « attention »
   prononcé ici suffit à faire changer d'avis sans qu'aucune conception ait été traitée.
3. **Mettre à l'épreuve** : calcul des premiers termes, test numérique, contre-exemple.
   Le cas doit être choisi pour que l'erreur soit visible — c'est le point technique de la
   phase (voir la séance 2 : le test en x = 1 ne discrimine rien).
4. **Faire verbaliser la contradiction** par un élève, à voix haute, avec ses mots.
5. **Seulement alors, reconstruire.**

Si personne ne produit l'erreur attendue, **ne pas la fabriquer**. Passer à la
reconstruction et reverser le temps gagné au parcours d'approfondissement.

---

## 6. Différenciation

### Les trois parcours

| Parcours | Attribution | Ce qui change |
|---|---|---|
| Consolidation | Le domaine de la séance est en priorité 1 ou 2 dans le livret | Exemple résolu fourni, valeurs simples, étayage écrit |
| Maîtrise | Le domaine est réussi mais hésitant | Pas d'exemple résolu, justification écrite exigée |
| Approfondissement | Le domaine est acquis avec certitude | Question ouverte, démonstration à rédiger |

L'attribution est **relue à chaque séance** dans le livret individuel. Un élève peut être en
consolidation en séance 1 et en approfondissement en séance 3 : c'est le cas le plus
fréquent, pas l'exception.

### Les cinq aides

| Aide | Contenu |
|---|---|
| A | Rappel de la propriété, sans application |
| B | Première étape faite |
| C | Exemple résolu analogue, à transposer |
| D | Découpage de la tâche en sous-questions |
| E | Corrigé partiel à compléter |

L'élève **note la lettre** de l'aide utilisée. Ce relevé n'est pas administratif : la
décroissance de l'aide maximale entre la séance 1 et la séance 5 est l'un des cinq critères
de réussite du stage.

---

## 7. Gérer les deux élèves sans erreur au positionnement

Deux élèves ont un positionnement en mathématiques sans aucune erreur. Ils ne doivent ni
s'ennuyer, ni servir de répétiteurs par défaut.

**Ce qui est prévu.**

- Parcours approfondissement dès la séance 1, avec démonstration à rédiger.
- Pour l'une des deux, le module mathématiques expertes prend une partie du temps
  différencié (§ 8).
- Rôle de **vérificateur** : relire la rédaction d'un camarade et dire si la propriété a
  été écrite avant le calcul — sans donner la réponse. Cette tâche travaille l'exigence de
  rédaction, qui est justement ce que le positionnement ne mesure pas.

**Ce qu'il faut éviter.** Leur confier l'explication d'une notion à un camarade porteur d'une
certitude erronée : la confrontation demande un pilotage que seul l'enseignant peut assurer.

---

## 8. L'option mathématiques expertes

Deux élèves. **Il n'existe aucun stage de mathématiques expertes** : l'option est traitée à
raison de 20 minutes par séance, prélevées sur le temps différencié, et son diagnostic propre
est repris dans le livret de mathématiques de chacune, section « Option annuelle ». Le détail
de la conduite figure dans `tle_spe_Option_Maths_Expertes.md`.

Le profil des deux élèves est très contrasté : l'une n'a qu'un point à consolider, l'autre a
laissé deux domaines entiers sans réponse. Le module doit donc être conduit
individuellement, pas en petit groupe.

---

## 9. Ce qu'il faut refuser

| Situation | Pourquoi refuser |
|---|---|
| Une conclusion sans propriété écrite | L'erreur de méthode devient invisible dans un calcul faux |
| Une certitude de 4 sans contrôle | La calibration de la confiance est un objectif du stage |
| Un tableau de signes sans le signe de a | C'est l'erreur exacte du positionnement |
| Une conclusion sur les variations sans f' factorisée | Le signe ne se lit pas sur une forme développée |
| Une réponse lue à la calculatrice sans justification | La calculatrice contrôle, elle n'établit pas |

---

## 10. Calendrier de préparation

| Quand | Quoi |
|---|---|
| J−7 | Lire les huit livrets individuels ; repérer les parcours de la séance 1 |
| J−3 | Préparer les supports : cartes, bandes numériques, gabarits, arbres pondérés |
| J−1 | Photocopier les fiches élèves des cinq séances et les portfolios |
| Séance 1, début | Faire passer le mini-diagnostic complémentaire (20 min) |
| Séance 1, fin | Dépouiller le mini-diagnostic ; ajuster la séance 5 en conséquence |
| Séance 5, fin | Dépouiller l'évaluation finale ; remplir la comparaison initiale/finale |
| J+1 | Restituer aux familles ; archiver les portfolios |

---

## 11. Documents du module

| Dossier | Contenu |
|---|---|
| `00_MASTER/` | Index et documentation d'ensemble |
| `01_ENSEIGNANT/` | Ce guide, le tableau de bord, le module mathématiques expertes |
| `02_SEANCES/S1` à `S5` | Fiche professeur, fiche élève, supports, cartes d'aide |
| `03_EVALUATIONS/` | Mini-diagnostic, évaluation finale, portfolio |
| `04_NOMINATIFS/` | **Confidentiel** — un dossier par élève |
| `05_SOURCES/` | Programme complet du stage, source unique |

---
_Source pédagogique unique : `stage_prerentree_terminale_maths.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ; ils sont déclinés ici en supports opérationnels._
