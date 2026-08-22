# Terminale NSI — Séance 5 — Fiche élève
## Données en tables, bases de données, systèmes

**Ton objectif de séance :** savoir nommer les trois opérations sur une table — sélection,
projection, jointure — et les écrire en SQL.

### Règle de travail

- Je distingue **lignes** et **colonnes** avant de nommer une opération.
- Certitude : $\square$1 $\square$2 $\square$3 $\square$4 · Aide : A, B, C, D ou E.

---

## Contrôle d'entrée (séance 4)

Quelle est la précondition de la recherche dichotomique ? Que se passe-t-il si elle n'est pas
respectée ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 1 — Enregistrements et descripteurs

Voici un extrait de fichier CSV :

```
nom,prenom,classe,note
Durand,Camille,TG3,14
Nguyen,Léo,TG1,11
Ferrand,Sacha,TG3,17
```

**Question 1.** Combien de **lignes** contient ce fichier ? ....................

**Question 2.** Combien d'**enregistrements** ? ....................

**Question 3.** Combien de **descripteurs** ? ....................

**Pourquoi les réponses 1 et 2 diffèrent-elles ?** ..........................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4

---

## Partie 2 — La trace écrite

> **Une table.** Une **ligne** est un enregistrement (un individu, un objet). Une **colonne**
> est un descripteur (un attribut). La première ligne d'un CSV contient les noms des
> descripteurs : ce **n'est pas** une donnée.
>
> **Trois opérations.**
>
> | Opération | Ce qu'on garde |
> |---|---|
> | **Sélection** | des **lignes**, selon une condition |
> | **Projection** | des **colonnes** |
> | **Jointure** | on rapproche deux tables par un attribut commun |
>
> **En SQL.**
> ```sql
> SELECT nom, note FROM eleves ;                    -- projection
> SELECT * FROM eleves WHERE note > 12 ;            -- selection
> SELECT nom, note FROM eleves WHERE note > 12 ;    -- les deux
> SELECT eleves.nom, classes.professeur
> FROM eleves JOIN classes ON eleves.classe = classes.code ;   -- jointure
> ```

---

## Partie 3 — Entraînement

### Parcours consolidation (exercices 1 à 4)

**Exercice 1.** Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête.
Combien de lignes ? Combien d'enregistrements ? Combien de descripteurs ?

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Pour chaque opération, écris son nom.

| Ce qu'on fait | Nom de l'opération |
|---|---|
| Ne garder que les élèves dont la note dépasse 12 | |
| Ne garder que les colonnes « nom » et « note » | |
| Rapprocher la table des élèves et celle des classes | |

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Écris en SQL : « afficher le nom et la note des élèves de la classe TG3 ».

```sql

```

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Sur l'extrait de la partie 1, applique une sélection `note > 12` **puis** une
projection sur `nom` et `note`. Écris la table obtenue.

| | |
|---|---|
| | |
| | |

### Parcours maîtrise (exercices 3 à 6)

**Exercice 5.** Écris en SQL : « afficher le nom des élèves dont la note est supérieure à 12
**et** qui sont en TG3 ». Puis écris la requête qui donne exactement les élèves **exclus** par
cette condition.

```sql


```

*Indication : pour la seconde, souviens-toi de De Morgan (séance 1).*

**Exercice 6.** Deux tables :

```
eleves(id, nom, classe)
classes(code, professeur, salle)
```

Écris la requête qui affiche, pour chaque élève, son nom et le nom de son professeur.

```sql


```

Quel attribut sert au rapprochement ? ....................

### Parcours approfondissement (exercices 6 à 8)

**Exercice 7.** Dans les deux tables ci-dessus, quelle est la clé primaire de `eleves` ? Celle
de `classes` ? Quel attribut de `eleves` est une clé étrangère ? Que se passerait-il si un
élève portait une valeur de `classe` qui n'existe pas dans `classes` ?

....................................................................................................

....................................................................................................

**Exercice 8.** Écris un programme Python qui lit le fichier CSV, ne garde que les
enregistrements dont la note dépasse 12, et affiche le nom et la note. Quelle opération
réalises-tu à chaque étape ?

```python
import csv

with open('eleves.csv', encoding='utf-8') as fichier:
    lecteur = csv.DictReader(fichier)
    for ligne in lecteur:
        ...
```

---

## Partie 4 — Architecture et systèmes

Ce domaine est **acquis par tout le groupe**. On le réinvestit, on ne le réapprend pas.

**Exercice 9.** Complète.

| Élément du modèle de von Neumann | Son rôle |
|---|---|
| Unité arithmétique et logique | |
| Unité de commande | |
| Mémoire | |
| Bus | |

**Exercice 10.** Cite trois ressources gérées par un système d'exploitation, puis deux
commandes du shell agissant sur le système de fichiers.

....................................................................................................

---

## Partie 5 — Ce que la Terminale en fera

> **Bases de données.** Le chapitre reprend les trois opérations sous leurs noms SQL, et ajoute
> le modèle relationnel, les clés primaires et étrangères, les contraintes d'intégrité et le
> système de gestion de bases de données.
>
> **Processus et ordonnancement.** Un système exécute plusieurs programmes « en même temps »
> alors qu'un cœur n'en exécute qu'un : il partage le temps du processeur. Quand deux
> processus s'attendent mutuellement, il y a **interblocage**.
>
> **Réseaux.** Les protocoles de routage (RIP, OSPF) déterminent le chemin d'un message : ce
> sont des **algorithmes de plus court chemin sur un graphe** — le bloc algorithmique de
> l'année.
>
> **Sécurisation des communications.** Le chiffrement repose sur l'arithmétique des entiers,
> donc sur la représentation binaire de la séance 1.
>
> Remarque : les trois dernières ouvertures renvoient à des séances que tu as déjà faites.

---

## Partie 6 — Bilan du stage

**Ce que j'ai corrigé pendant ce stage :** ..................................................

....................................................................................................

**Ce qui reste fragile :** ..................................................................

....................................................................................................

**Ma certitude générale en NSI, aujourd'hui :** $\square$1 $\square$2 $\square$3 $\square$4

**Mon plan pour les quatre premières semaines de septembre** (à reporter dans mon livret) :

| Semaine | Ce que je travaille |
|---:|---|
| 1 | |
| 2 | |
| 3 | |
| 4 | |
