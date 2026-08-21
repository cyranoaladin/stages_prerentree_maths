# Terminale NSI — Séance 5 — Cartes d'aide
## Données en tables, bases de données, systèmes

---

### Carte A — Rappel de vocabulaire et de syntaxe

> Une **ligne** = un enregistrement · une **colonne** = un descripteur.
> La ligne d'en-tête n'est pas un enregistrement.
>
> **Sélection** : on garde des lignes → `WHERE`
> **Projection** : on garde des colonnes → `SELECT`
> **Jointure** : on rapproche deux tables → `JOIN ... ON ...`
>
> Squelette : `SELECT colonnes FROM table WHERE condition ;`

---

### Carte B — Première ligne écrite

> Pour « afficher le nom et la note des élèves de la classe TG3 » :
> ```sql
> SELECT nom, note
> FROM eleves
> WHERE ..........................
> ```
> À toi : quelle condition porte sur la classe ? Attention aux guillemets simples autour d'une
> valeur textuelle.

---

### Carte C — Exemple à transposer

> **Exemple.** « Afficher le nom et la salle des élèves ayant plus de 12. »
>
> ```sql
> SELECT eleves.nom, classes.salle
> FROM eleves
> JOIN classes ON eleves.classe = classes.code
> WHERE eleves.note > 12 ;
> ```
>
> Trois éléments : la **projection** dans le `SELECT`, la **jointure** dans le `JOIN ... ON`,
> la **sélection** dans le `WHERE`. La condition de jointure dit toujours quel attribut
> correspond à quel autre.
>
> **À toi de transposer**, en identifiant d'abord laquelle des trois opérations tu dois écrire.

---

### Carte D — Découpage en quatre questions

> 1. De quelles **colonnes** as-tu besoin ? → elles vont dans le `SELECT`.
> 2. As-tu besoin d'une **deuxième table** ? Si oui, quel attribut est commun aux deux ? →
>    `JOIN ... ON ...`.
> 3. Quelles **lignes** veux-tu garder ? → `WHERE`.
> 4. Relis : chaque nom de colonne que tu écris existe-t-il bien dans une des tables citées ?

---

### Carte E — Requête à compléter

> ```sql
> -- Projection seule
> SELECT .........., .......... FROM eleves ;
>
> -- Selection seule
> SELECT * FROM eleves WHERE .......... > 12 ;
>
> -- Jointure
> SELECT eleves.nom, classes...........
> FROM eleves
> JOIN classes ON eleves........... = classes........... ;
> ```

---

## Carte « contrôle » — à utiliser avant toute certitude de 4

> - J'ai distingué ce qui porte sur les **lignes** de ce qui porte sur les **colonnes**.
> - Ma jointure comporte une condition `ON` : sans elle, la requête est fausse.
> - Chaque colonne citée existe bien dans une table nommée dans le `FROM`.
> - Je n'ai pas compté la ligne d'en-tête parmi les enregistrements.

---

## Carte « erreurs fréquentes » — à distribuer en fin de séance

> 1. Compter la ligne d'en-tête parmi les enregistrements.
> 2. Confondre sélection (lignes) et projection (colonnes).
> 3. Écrire une jointure sans condition `ON` : le résultat croise tout avec tout.
> 4. Confondre clé primaire (elle **identifie**) et clé étrangère (elle **référence**).
> 5. Écrire `SELECT *` par réflexe alors que deux colonnes suffisaient.
