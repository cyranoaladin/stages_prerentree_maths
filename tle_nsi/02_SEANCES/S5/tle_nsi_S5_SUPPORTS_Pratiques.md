# Terminale NSI — Séance 5 — Supports pratiques
## Données en tables, bases de données, systèmes

## Support 1 — Extrait CSV projeté

À projeter en grand et à distribuer imprimé, une copie par binôme.

```
nom,prenom,classe,note
Durand,Camille,TG3,14
Nguyen,Léo,TG1,11
Ferrand,Sacha,TG3,17
```

**Trois questions à poser dans cet ordre, avec réponse écrite avant discussion :**

| Question | Réponse | Ce qu'elle révèle |
|---|---:|---|
| Combien de lignes ? | 4 | comptage brut |
| Combien d'enregistrements ? | 3 | l'en-tête n'est pas une donnée |
| Combien de descripteurs ? | 4 | une colonne = un attribut |

L'écart entre les deux premières réponses est le point à installer.

## Support 2 — Le geste des trois opérations

Deux accessoires simples, un jeu par binôme :

- une **bande de papier opaque** : on la pose sur les lignes qu'on écarte $\to$ **sélection** ;
- la feuille se **plie** verticalement pour cacher des colonnes $\to$ **projection** ;
- deux feuilles se **posent côte à côte**, alignées sur une colonne commune $\to$ **jointure**.

**Consigne.** Réaliser physiquement chacune des trois opérations sur l'extrait imprimé, puis
nommer ce qu'on vient de faire. Le geste précède le mot.

| Geste | Opération | Ce qui change |
|---|---|---|
| Masquer des lignes | Sélection | moins de lignes, mêmes colonnes |
| Plier des colonnes | Projection | mêmes lignes, moins de colonnes |
| Aligner deux feuilles | Jointure | plus de colonnes, lignes appariées |

## Support 3 — Table de correspondance opérations / SQL

À distribuer vierge dans la colonne de droite, à compléter en fin de partie 2, à conserver
dans le portfolio.

| Opération de Première | Mot-clé SQL | Exemple |
|---|---|---|
| Projection | | |
| Sélection | | |
| Jointure | | |

*Corrigé pour le professeur :*

| Opération | Mot-clé SQL | Exemple |
|---|---|---|
| Projection | `SELECT` (liste des colonnes) | `SELECT nom, note FROM eleves ;` |
| Sélection | `WHERE` | `SELECT * FROM eleves WHERE note > 12 ;` |
| Jointure | `JOIN ... ON ...` | `SELECT ... FROM eleves JOIN classes ON eleves.classe = classes.code ;` |

## Support 4 — Deux tables à joindre

Imprimées sur deux feuilles distinctes, à poser côte à côte.

**Table `eleves`**

| id | nom | classe |
|---:|---|---|
| 1 | Durand | TG3 |
| 2 | Nguyen | TG1 |
| 3 | Ferrand | TG3 |

**Table `classes`**

| code | professeur | salle |
|---|---|---|
| TG1 | Morel | B12 |
| TG3 | Andrieu | A04 |

**Questions à poser.**

1. Quel attribut permet de rapprocher les deux tables ? *(`classe` d'un côté, `code` de
   l'autre)*
2. Quelle est la clé primaire de chaque table ? *(`id` et `code`)*
3. Quel attribut de `eleves` est une clé étrangère ? *(`classe`)*
4. Que se passerait-il si un élève avait `classe = 'TG5'` ? *(la jointure ne le retiendrait
   pas ; c'est une violation d'intégrité référentielle)*

**Résultat attendu de la jointure :**

| nom | professeur |
|---|---|
| Durand | Andrieu |
| Nguyen | Morel |
| Ferrand | Andrieu |

## Support 5 — Traitement en Python

À exécuter en parcours approfondissement. Le fichier `eleves.csv` est fourni avec l'extrait de
la partie 1.

```python
import csv

with open('eleves.csv', encoding='utf-8') as fichier:
    lecteur = csv.DictReader(fichier)
    table = list(lecteur)

# Selection : on garde des lignes
retenus = [ligne for ligne in table if int(ligne['note']) > 12]

# Projection : on garde des colonnes
projete = [{'nom': ligne['nom'], 'note': ligne['note']} for ligne in retenus]

for ligne in projete:
    print(ligne['nom'], ligne['note'])
```

**Point à faire émerger.** `DictReader` traite automatiquement la première ligne comme
l'en-tête : `table` contient 3 enregistrements, pas 4. C'est la question 2 du support 1,
vérifiée par le programme.

Faire nommer chaque étape : la première compréhension de liste est une **sélection**, la
seconde une **projection**. Ce sont les mêmes mots qu'en SQL.

## Support 6 — Affiche de séance

> **Sélection** $\to$ des **lignes** $\to$ `WHERE`
> **Projection** $\to$ des **colonnes** $\to$ `SELECT`
> **Jointure** $\to$ deux tables, un attribut commun $\to$ `JOIN ... ON ...`
>
> **La ligne d'en-tête n'est pas un enregistrement.**

## Matériel à prévoir

- L'extrait CSV imprimé, un par binôme, plus une projection.
- Une bande de papier opaque par binôme.
- Les deux tables à joindre, imprimées séparément.
- Un poste par binôme avec `eleves.csv` et le script de traitement.
- La table de correspondance opérations / SQL, une par élève.
