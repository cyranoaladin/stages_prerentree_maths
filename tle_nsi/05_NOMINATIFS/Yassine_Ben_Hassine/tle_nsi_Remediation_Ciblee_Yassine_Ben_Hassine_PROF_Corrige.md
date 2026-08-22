# Terminale NSI — Plan de remédiation ciblée — Yassine Ben Hassine (Corrigé enseignant)
## NSI — Parcours personnalisé

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Yassine Ben Hassine  
**Matière :** NSI  
**Diagnostic du :** 2026-08-14  
**Source :** `Bilans/bilan-nexus-eleve_yassine_nsi.pdf`

## Profil de l'élève, en une page

| Domaine | Réussite | Situation | Posture de travail |
|---|---:|---|---|
| Représentation binaire | 0 % | Certitude à revoir | **CONFRONTER** |
| Booléens et logique | 66,7 % | Certitude à revoir | **CONFRONTER** |
| Types construits | 33,3 % | Certitude à revoir | **CONFRONTER** |
| Programmation | 33,3 % | Certitude à revoir | **CONFRONTER** |
| Algorithmique | 33,3 % | Certitude à revoir | **CONFRONTER** |
| Données en tables | 66,7 % | Certitude à revoir | **CONFRONTER** |
| Architecture et systèmes | 100 % | Acquis disponible | **ENTRETENIR** |

**Ordre de traitement.** Représentation binaire (CONFRONTER) $\to$ Booléens et logique (CONFRONTER) $\to$ Types construits (CONFRONTER) $\to$ Programmation (CONFRONTER) $\to$ Algorithmique (CONFRONTER) $\to$ Données en tables (CONFRONTER)

**Calibration de la confiance.** Un levier en plus des notions : ton ressenti et tes résultats ne coïncident pas toujours. Apprendre à repérer quand tu es sûr à raison — et quand tu ne l'es pas — vaut autant que le contenu lui-même.

## Composition de la feuille

| # | Item du positionnement | Domaine | Compétence | Motif de sélection |
|---:|---:|---|---|---|
| 1 | item 1 | Représentation binaire | Convertir un entier de la base 10 vers la base 2 | réponse fausse |
| 2 | item 2 | Représentation binaire | Convertir entre base 16 et base 10 | réponse fausse |
| 3 | item 3 | Booléens et logique | Évaluer une expression booléenne | réponse fausse |
| 4 | item 6 | Types construits | Modifier un tableau en place | réponse fausse |
| 5 | item 8 | Types construits | Créer, modifier et supprimer une entrée de dictionnaire | réponse fausse |
| 6 | item 10 | Programmation | Distinguer effet de bord et valeur renvoyée | réponse fausse |
| 7 | item 12 | Programmation | Construire un accumulateur dans une boucle | réponse fausse |
| 8 | item 14 | Algorithmique | Évaluer le coût d'un algorithme de recherche | réponse fausse |
| 9 | item 15 | Données en tables | Distinguer enregistrement et descripteur | réponse fausse |

Chaque exercice est la **variante** de l'item que l'élève a manqué ou réussi sans assurance : même compétence, énoncé différent. La feuille d'un autre élève n'a donc pas la même composition.

<div class="page-break"></div>

## Corrigé

### Exercice 1 — Représentation binaire

**Énoncé.** Écrire 22 en binaire, puis vérifier en recalculant la valeur décimale.

**Corrigé.** $22 = 16 + 4 + 2 = 2^4 + 2^2 + 2^1$, ce qui s'écrit 10110. Vérification : $16 + 0 + 4 + 2 + 0 = 22$.

**Geste à installer.** Décomposer en somme de puissances de 2 décroissantes, ou diviser successivement par 2 et lire les restes de bas en haut.

**Erreur à surveiller chez cet élève.** Vaut 12 : oublie le bit des unités. (constatée à l'item 1 du positionnement, donné avec une certitude de 4/4.)

### Exercice 2 — Représentation binaire

**Énoncé.** Convertir 0x2A en base 10, puis convertir 60 en hexadécimal.

**Corrigé.** $0x2A = 2 \times 16 + 10 = 42$. Pour 60 : $60 = 3 \times 16 + 12$, et 12 s'écrit C, donc 60 s'écrit 0x3C.

**Geste à installer.** En hexadécimal, $A = 10$, $B = 11$, $C = 12$, $D = 13$, $E = 14$, $F = 15$. Chaque position vaut une puissance de 16.

**Erreur à surveiller chez cet élève.** Ne compte que le chiffre F et oublie le 1 des « seizaines ». (constatée à l'item 2 du positionnement, donné avec une certitude de 3/4.)

### Exercice 3 — Booléens et logique

**Énoncé.** Que vaut l'expression (not True) or (False and True) ? Détailler l'ordre d'évaluation.

**Corrigé.** not True vaut False ; False and True vaut False ; False or False vaut False. L'expression vaut donc False.

**Geste à installer.** Évaluer de l'intérieur vers l'extérieur, en respectant la priorité : not, puis and, puis or.

**Erreur à surveiller chez cet élève.** Confond une expression booléenne avec une absence de valeur. (constatée à l'item 3 du positionnement, donné avec une certitude de 3/4.)

### Exercice 4 — Types construits

**Énoncé.** Soit $L = [1$, 2, 3]. Après L.insert(0, 9) puis L.append(4), que contient L ? Que vaudrait L après $L = L$.append(5) ?

**Corrigé.** insert(0, 9) place 9 en tête : L vaut [9, 1, 2, 3], puis append(4) donne [9, 1, 2, 3, 4]. En revanche $L = L$.append(5) affecte à L la valeur renvoyée par append, c'est-à-dire None : la liste est perdue.

**Geste à installer.** append ajoute en fin de liste et ne renvoie rien : écrire $L = L$.append(4) détruit la liste en la remplaçant par None.

**Erreur à surveiller chez cet élève.** append ajoute en fin de liste, pas au début. (constatée à l'item 6 du positionnement, donné avec une certitude de 3/4.)

### Exercice 5 — Types construits

**Énoncé.** Écrire les instructions qui ajoutent à d la clé 'z' de valeur 30, puis suppriment la clé 'x', puis parcourent d en affichant chaque couple clé-valeur.

**Corrigé.** d['$z'] = 30$ crée l'entrée. del d['x'] (ou d.pop('x')) la supprime. Le parcours s'écrit : for cle, valeur in d.items(): print(cle, valeur).

**Geste à installer.** Une affectation d[clé] $=$ valeur crée l'entrée si elle n'existe pas et la remplace sinon ; del d[clé] la supprime.

**Erreur à surveiller chez cet élève.** append est une méthode des listes, pas des dictionnaires. (constatée à l'item 8 du positionnement, donné avec une certitude de 4/4.)

### Exercice 6 — Programmation

**Énoncé.** Soit def $h(L)$: L.append(0). Que vaut r après $r = h([1$, 2]) ? Si on écrit $M = [1$, 2] puis $h(M)$, que contient M ?

**Corrigé.** h ne comporte pas de return : r vaut None. En revanche la liste est mutable et modifiée en place, donc après $h(M)$ la liste M contient [1, 2, 0].

**Geste à installer.** Sans return, une fonction renvoie None. Une fonction peut modifier un objet mutable reçu en paramètre tout en renvoyant None : ce sont deux choses distinctes.

**Erreur à surveiller chez cet élève.** Une fonction sans return est valide ; elle ne provoque pas d'erreur. (constatée à l'item 10 du positionnement, donné avec une certitude de 4/4.)

### Exercice 7 — Programmation

**Énoncé.** Soit $s = 0$ puis « for i in range(1, 6): $s = s + i$*i ». Que vaut s ? Dresser la table de trace.

**Corrigé.** range(1, 6) produit 1, 2, 3, 4, 5. Table de trace : s vaut successivement 1, 5, 14, 30 puis 55. Au final $s = 1 + 4 + 9 + 16 + 25 = 55$.

**Geste à installer.** Initialiser l'accumulateur avant la boucle, écrire la valeur des variables à chaque tour dans une table de trace pour vérifier.

**Erreur à surveiller chez cet élève.** Compte le nombre d'itérations au lieu de la somme. (constatée à l'item 12 du positionnement, donné avec une certitude de 4/4.)

### Exercice 8 — Algorithmique

**Énoncé.** Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour une recherche dichotomique ? Et pour une recherche séquentielle ?

**Corrigé.** La dichotomie effectue de l'ordre de $\log_2(1 000) \approx 10$ comparaisons au pire, car $2^{10} = 1 024$. La recherche séquentielle en effectue jusqu'à 1 000 : c'est le gain qui justifie de trier.

**Geste à installer.** À chaque étape la taille est divisée par deux : le nombre d'étapes est de l'ordre de $\log_2(n)$. Retenir les repères : $2^{10} \approx 1 000$, $2^{20} \approx 1 000 000$.

**Erreur à surveiller chez cet élève.** Correspond à une recherche séquentielle, pas dichotomique. (constatée à l'item 14 du positionnement, donné avec une certitude de 3/4.)

### Exercice 9 — Données en tables

**Énoncé.** Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête. Combien de lignes contient le fichier ? Combien d'enregistrements ? Combien de descripteurs ?

**Corrigé.** Le fichier contient 501 lignes : 1 ligne d'en-tête et 500 lignes de données. Il y a donc 500 enregistrements et 6 descripteurs.

**Geste à installer.** Une ligne est un enregistrement (un individu, un objet) ; une colonne est un descripteur (un attribut). La première ligne du fichier contient en général les noms des descripteurs.

**Erreur à surveiller chez cet élève.** Une ligne n'est qu'un enregistrement du fichier, pas le fichier. (constatée à l'item 15 du positionnement, donné avec une certitude de 4/4.)

## Relevé de maîtrise

| Exercice | Juste sans aide | Juste avec aide | Erreur de procédure | Erreur de calcul | À reprendre |
|---:|:---:|:---:|:---:|:---:|:---:|
| 1 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 2 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 3 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 4 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 5 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 6 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 7 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 8 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 9 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |

## Conduite recommandée

### Représentation binaire — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** La représentation en machine reste sous-jacente partout en Terminale : typage des attributs d'une base de données, coût mémoire des structures de données, arithmétique modulaire du chiffrement dans la sécurisation des communications, adressage réseau.

### Booléens et logique — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Les conditions composées structurent les invariants de boucle, la preuve de terminaison et de correction d'un algorithme, ainsi que les clauses WHERE d'une requête SQL. Une négation mal formée fausse aussi bien un algorithme qu'une requête.

### Types construits — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Toutes les structures de données de Terminale sont bâties dessus : listes chaînées, piles, files, arbres et graphes s'implémentent avec des listes et des dictionnaires. Une confusion sur l'indexation ou sur la mutabilité se paie immédiatement dans ces implémentations.

### Programmation — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** La récursivité, la modularité, la programmation objet et la mise au point systématique s'appuient entièrement sur une compréhension juste de l'appel de fonction, du retour et de la portée des variables.

### Algorithmique — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Diviser pour régner, programmation dynamique, parcours d'arbres et de graphes, recherche textuelle : tous ces algorithmes se justifient par un raisonnement sur le coût, dans la continuité directe de la dichotomie de Première.

### Données en tables — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Le chapitre « Bases de données » reprend ces opérations dans le modèle relationnel : sélection, projection et jointure deviennent SELECT, WHERE et JOIN en SQL, avec en plus les contraintes d'intégrité et la notion de clé.

## Décision de fin de parcours

| Domaine | Situation initiale | Situation finale | Décision pour septembre |
|---|---|---|---|
| Représentation binaire | Certitude à revoir | | |
| Booléens et logique | Certitude à revoir | | |
| Types construits | Certitude à revoir | | |
| Programmation | Certitude à revoir | | |
| Algorithmique | Certitude à revoir | | |
| Données en tables | Certitude à revoir | | |
| Architecture et systèmes | Acquis disponible | | |

---
_Document enseignant. Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
