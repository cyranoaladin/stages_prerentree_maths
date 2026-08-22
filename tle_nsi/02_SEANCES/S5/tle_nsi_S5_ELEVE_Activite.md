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

### Comment tu trouves ton parcours

Ton livret individuel porte, pour cette séance, une **posture** et un **parcours**. Le tableau
ci-dessous dit ce que tu traites. Tu ne fais pas les huit exercices : tu fais les tiens, et tu
les fais entièrement.

| Ta posture du jour | Ce que tu traites | Ce qu'on attend de toi |
|---|---|---|
| **DIAGNOSTIQUER** — tu avais laissé ce domaine sans réponse | Question 0, puis exercices 1 et 2 | Répondre même sans être sûr : déclarer une certitude de 1 est une réponse, pas un aveu |
| **CONFRONTER** — tu t'es trompé en étant sûr de toi | Question 0, puis exercices 1 à 4 | Écrire ce que tu croyais, puis ce qui l'a mis en défaut |
| **INSTALLER** — il te manque quelque chose, et tu le sais | Exercices 1 à 4 | Exécuter avant de conclure, et écrire la table de trace |
| **CONSOLIDER** — tu réussis, sans en être sûr | Exercices 3 à 6 | Spécifier la fonction et écrire ses tests, sans carte d'aide |
| **ENTRETENIR** — c'est acquis et assumé | Exercices 6 à 8 | Justifier le choix d'algorithme par son coût, pas par le temps mesuré |
| **EXCELLENCE** — ton bilan ne comporte aucun domaine à reprendre, ou tu as terminé ta piste | Exercices 11 et 12, puis l'atelier Terminale | Produire une fonction spécifiée et testée, puis relire la copie d'un camarade **sans lui donner la réponse** |

### Exercices 1 à 4 — pistes Diagnostiquer, Confronter et Installer

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

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

### Exercices 3 à 6 — piste Consolider

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

### Exercices 6 à 8 — piste Entretenir

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

## Piste excellence — exercices 11 et 12

> **Pour qui.** Ces deux exercices sont les tiens si ton bilan ne comporte aucun domaine à
> reprendre, ou si tu as terminé ta piste avant la fin du temps différencié. Le premier est un
> problème complet : on attend une fonction spécifiée, testée, et dont tu sais dire le coût.
> Le second part d'un énoncé faux : on attend un contre-exemple, puis l'énoncé corrigé.
>
> Une fois tes deux exercices rendus, le professeur pourra te confier la copie d'un camarade.
> Tu ne corriges pas : tu dis si la fonction est spécifiée, si le cas limite est traité, et où
> le raisonnement s'interrompt.

**Exercice 11.** Deux tables décrivent des élèves et leurs notes :

```
eleves(id, nom, classe)
notes(id_eleve, matiere, note)
```

a) Quelle est la clé primaire de chaque table ? Quelle est la clé étrangère, et vers quoi
pointe-t-elle ?

....................................................................................................

....................................................................................................

b) Écris la requête SQL qui affiche le nom de chaque élève de la classe `'TG3'` et sa moyenne,
toutes matières confondues.

```sql





```

c) Écris le même traitement en Python, à partir de deux listes de dictionnaires.

```python








```

d) Quelle contrainte d'intégrité empêche d'insérer une note dont l'`id_eleve` ne correspond à
aucun élève ? Que se passerait-il sans elle ?

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 12.** Un élève affirme : « un fichier CSV et une base de données relationnelle,
c'est la même chose avec une syntaxe différente ».

a) Cite deux garanties qu'une base de données offre et qu'un fichier CSV n'offre pas.

....................................................................................................

....................................................................................................

....................................................................................................

b) Dans un CSV, que se passe-t-il si deux lignes portent le même identifiant ? Et dans une
table dotée d'une clé primaire ?

....................................................................................................

....................................................................................................

c) Pourquoi la jointure tient-elle en une ligne de SQL et demande-t-elle une double boucle en
Python ? Qu'est-ce que le système de gestion fait à ta place ?

....................................................................................................

....................................................................................................

....................................................................................................

d) Donne un cas où le fichier CSV reste le bon choix, et dis pourquoi.

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

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

## Atelier Terminale NSI — 20 minutes

> **Pour qui.** Cet atelier est pour toi si tu as terminé ta piste avant la fin du temps
> différencié, ou si tu suis la piste excellence. Il ne porte pas sur le thème du jour : il
> ouvre une notion du programme de Terminale que la Première n'aborde pas, et que la séance
> rend abordable dès maintenant. Le temps y est prélevé sur la phase différenciée.

**Le lien avec la séance du jour.** Tu viens de manipuler des données partagées entre plusieurs tables. Un
système d'exploitation partage autre chose entre plusieurs programmes : le processeur, la
mémoire, les fichiers. Le programme de Terminale appelle cela la **gestion des processus**.

**a)** Un processus peut être **élu**, **prêt** ou **bloqué**. Associe chaque situation à un
état.

| Situation | État |
|---|---|
| Le programme attend la fin d'une lecture sur disque | |
| Le programme s'exécute sur le processeur | |
| Le programme pourrait s'exécuter, mais un autre occupe le processeur | |

**b)** Deux processus, P et Q. P détient le fichier A et demande le fichier B ; Q détient B et
demande A. Décris ce qui se passe. Comment appelle-t-on cette situation ?

....................................................................................................

....................................................................................................

....................................................................................................

**c)** Représente la situation par un schéma où une flèche signifie « attend ». Qu'est-ce qui,
dans ce schéma, caractérise le blocage ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**d)** Propose une règle simple qui empêcherait ce blocage de se produire.

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** L'interblocage se détecte exactement comme un cycle dans un
graphe orienté — le même objet mathématique que les graphes du programme d'algorithmique.
Deux chapitres qui semblent étrangers reposent sur la même structure.

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
