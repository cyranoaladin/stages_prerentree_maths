# Terminale NSI — Séance 5 — Fiche professeur
## Données en tables, bases de données, systèmes, évaluation

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_nsi.md`

## Pourquoi cette séance

Les données en tables portent **trois certitudes erronées** pour 53,3 % de réussite. Ce n'est
pas l'opération qui manque, c'est son **nom** : sélection, projection et jointure ne sont pas
distinguées.

Or le chapitre « bases de données » de Terminale reprend exactement ces trois opérations, sous
les noms SQL `WHERE`, `SELECT` et `JOIN`. Une confusion de vocabulaire y devient une confusion
de requête.

L'architecture et les systèmes sont **acquis par tout le groupe** (100 % de réussite, aucune
erreur). Ce domaine ne fait donc l'objet d'aucune reconstruction : il est réinvesti en
quinze minutes et sert de point d'appui.

## Objectifs de la séance

1. Nommer sélection, projection et jointure, et les écrire en SQL.
2. Distinguer enregistrement et descripteur, y compris pour le comptage des lignes.
3. Réinvestir architecture et systèmes ; ouvrir sur processus et réseaux.
4. Mesurer les progrès et fixer le plan de septembre.

## Déroulé minuté

| Durée | Phase | Contenu |
|---:|---|---|
| 10 min | Ouverture | Contrôle sur la séance 4 : précondition de la dichotomie |
| 25 min | Données en tables | Enregistrement et descripteur ; sélection, projection, jointure |
| 20 min | Ouverture bases de données | Les trois opérations en SQL ; clé primaire, clé étrangère |
| 15 min | Architecture et systèmes | Réinvestissement ; ouverture processus, ordonnancement, réseaux |
| 35 min | Évaluation finale | Épreuve de synthèse |
| 15 min | Bilan | Restitution, plan de septembre, portfolio |

## Données en tables — 25 minutes

### Enregistrement et descripteur

Projeter un extrait de fichier CSV :

```
nom,prenom,classe,note
Durand,Camille,TG3,14
Nguyen,Léo,TG1,11
Ferrand,Sacha,TG3,17
```

Poser trois questions et recueillir les réponses par écrit :

1. Combien de lignes contient ce fichier ? *(4)*
2. Combien d'enregistrements ? *(3 — la ligne d'en-tête n'en est pas un)*
3. Combien de descripteurs ? *(4)*

L'écart entre les questions 1 et 2 est le point à installer : **la ligne d'en-tête n'est pas
une donnée**.

### Les trois opérations

Construire le tableau avec les élèves, en manipulant l'extrait projeté :

| Opération | Ce qu'on garde | Sur l'exemple | Résultat |
|---|---|---|---|
| **Sélection** | des **lignes**, selon une condition | note > 12 | Durand et Ferrand |
| **Projection** | des **colonnes** | nom et note | 3 lignes, 2 colonnes |
| **Jointure** | on rapproche deux tables par un attribut commun | élèves $\times$ classes, par `classe` | table élargie |

Faire manipuler physiquement : masquer des lignes avec une bande de papier (sélection), plier
la feuille pour cacher des colonnes (projection). Le geste distingue les deux opérations mieux
qu'une définition.

## Ouverture bases de données — 20 minutes

Faire écrire les trois opérations en SQL, en partant de celles qui viennent d'être nommées.

```sql
-- Projection : on choisit des colonnes
SELECT nom, note FROM eleves ;

-- Selection : on choisit des lignes
SELECT * FROM eleves WHERE note > 12 ;

-- Les deux ensemble
SELECT nom, note FROM eleves WHERE note > 12 ;

-- Jointure : on rapproche deux tables
SELECT eleves.nom, classes.professeur
FROM eleves
JOIN classes ON eleves.classe = classes.code ;
```

Faire remarquer la correspondance, mot à mot :

| Opération de Première | Mot-clé SQL de Terminale |
|---|---|
| Projection | `SELECT` (la liste des colonnes) |
| Sélection | `WHERE` |
| Jointure | `JOIN ... ON ...` |

**Clés.** Introduire brièvement, sans exercice :

> Une **clé primaire** identifie de façon unique chaque enregistrement d'une table. Une **clé
> étrangère** est un attribut qui référence la clé primaire d'une autre table : c'est elle qui
> rend la jointure possible.
>
> En Terminale, le chapitre ajoutera le modèle relationnel, les contraintes d'intégrité et le
> système de gestion de bases de données. Les trois opérations, elles, resteront les mêmes.

**Rappel de la séance 1.** Une clause `WHERE note > 12 AND classe = 'TG3'` est une expression
booléenne. Sa négation s'écrit avec De Morgan. Le lien est explicite.

## Architecture et systèmes — 15 minutes

Le domaine est acquis par tout le groupe : il s'agit d'un **réinvestissement**, pas d'un
enseignement.

Faire restituer oralement, en cinq minutes : les composants du modèle de von Neumann, le rôle
de l'unité arithmétique et logique, celui de l'unité de commande, le fait que la mémoire
contient à la fois données et instructions.

Puis ouvrir, en dix minutes :

> **Processus et ordonnancement.** Un système d'exploitation exécute plusieurs programmes
> « en même temps » alors qu'un cœur n'en exécute qu'un. Il partage le temps du processeur
> entre les processus : c'est l'ordonnancement. Quand deux processus s'attendent mutuellement,
> il y a **interblocage**.
>
> **Réseaux.** Un message traverse plusieurs routeurs. Les protocoles de routage — RIP, OSPF —
> déterminent le chemin. Ce sont des **algorithmes de plus court chemin sur un graphe** :
> exactement l'objet du bloc « algorithmique » de Terminale.
>
> **Sécurisation des communications.** Le chiffrement repose sur l'arithmétique des entiers,
> donc sur la représentation binaire de la séance 1.

Faire remarquer que les trois ouvertures renvoient à des séances déjà faites. Le stage se
referme sur lui-même : c'est la conclusion à faire formuler.

## Évaluation finale — 35 minutes

Distribuer `03_EVALUATIONS/tle_nsi_Evaluation_Finale_ELEVE.md`. Sept exercices, un par
domaine, avec certitude déclarée. Aucune note : la copie est relue avec la matrice réussite $\times$
confiance et comparée au positionnement initial.

## Bilan — 15 minutes

1. Restituer à chaque élève la comparaison entre sa carte initiale et son résultat final.
2. Faire remplir le plan de septembre dans le livret individuel (quatre semaines).
3. Faire compléter le portfolio et l'auto-évaluation finale.
4. Faire formuler à chacun une phrase : « ce que j'ai corrigé pendant ce stage, c'est… ».

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Ligne d'en-tête comptée comme enregistrement | Faire compter les élèves réels de l'extrait |
| Sélection et projection confondues | Reprendre le geste : masquer des lignes, plier des colonnes |
| Jointure écrite sans condition de rapprochement | Demander : « sur quel attribut commun ? » |
| Clé primaire et clé étrangère confondues | Faire désigner, sur l'exemple, laquelle identifie et laquelle référence |
| `SELECT *` employé systématiquement | Demander quelles colonnes sont réellement utiles |

## Indicateurs de fin de séance

- L'élève nomme correctement les trois opérations sans hésiter.
- L'élève écrit une requête `SELECT ... FROM ... WHERE ...` correcte.
- L'élève sait dire ce que le chapitre « bases de données » ajoutera à ce qu'il sait déjà.

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
