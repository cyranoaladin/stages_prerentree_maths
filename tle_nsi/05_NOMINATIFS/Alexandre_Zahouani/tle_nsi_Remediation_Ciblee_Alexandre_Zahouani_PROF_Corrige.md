# Terminale NSI — Plan de remédiation ciblée — Alexandre Zahouani (Corrigé enseignant)
## NSI — Parcours personnalisé

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Alexandre Zahouani  
**Matière :** NSI  
**Diagnostic du :** 2026-08-13  
**Source :** `Bilans/bilan-nexus-eleve_alexandre_zahouani_nsi.pdf`

## Profil de l'élève, en une page

| Domaine | Réussite | Situation | Posture de travail |
|---|---:|---|---|
| Représentation binaire | 0 % | Difficulté repérée, sans fausse certitude | **INSTALLER** |
| Booléens et logique | 100 % | Acquis disponible | **ENTRETENIR** |
| Types construits | 50 % | Certitude à revoir | **CONFRONTER** |
| Programmation | 66,7 % | Difficulté repérée, sans fausse certitude | **INSTALLER** |
| Algorithmique | 33,3 % | Certitude à revoir | **CONFRONTER** |
| Données en tables | 0 % | Certitude à revoir | **CONFRONTER** |
| Architecture et systèmes | 100 % | Acquis disponible | **ENTRETENIR** |

**Ordre de traitement.** Types construits (CONFRONTER) $\to$ Algorithmique (CONFRONTER) $\to$ Données en tables (CONFRONTER) $\to$ Représentation binaire (INSTALLER) $\to$ Programmation (INSTALLER)

**Calibration de la confiance.** Point fort : ton auto-évaluation est fiable — tu sais globalement ce que tu sais. C'est un vrai atout pour réviser juste, sans perdre de temps.

## Composition de la feuille

| # | Item du positionnement | Domaine | Compétence | Motif de sélection |
|---:|---:|---|---|---|
| 1 | item 7 | Types construits | Accéder à une valeur par sa clé dans un dictionnaire | réponse fausse |
| 2 | item 8 | Types construits | Créer, modifier et supprimer une entrée de dictionnaire | réponse fausse |
| 3 | item 14 | Algorithmique | Évaluer le coût d'un algorithme de recherche | réponse fausse |
| 4 | item 15 | Données en tables | Distinguer enregistrement et descripteur | réponse fausse |
| 5 | item 16 | Données en tables | Nommer les opérations sur une table | réponse fausse |
| 6 | item 1 | Représentation binaire | Convertir un entier de la base 10 vers la base 2 | réponse fausse |
| 7 | item 2 | Représentation binaire | Convertir entre base 16 et base 10 | réponse fausse |
| 8 | item 10 | Programmation | Distinguer effet de bord et valeur renvoyée | réponse fausse |
| 9 | item 12 | Programmation | Construire un accumulateur dans une boucle | réussi avec une certitude de 2/4 |

Chaque exercice est la **variante** de l'item que l'élève a manqué ou réussi sans assurance : même compétence, énoncé différent. La feuille d'un autre élève n'a donc pas la même composition.

<div class="page-break"></div>

## Corrigé

### Exercice 1 — Types construits

**Énoncé.** Soit $d =$ {'x': 10, 'y': 20}. Que vaut d['y'] ? Que se passe-t-il si on écrit d['z'] ? Comment obtenir 0 dans ce cas sans erreur ?

**Corrigé.** d['y'] vaut 20. L'expression d['z'] lève une erreur KeyError car la clé n'existe pas. Pour obtenir une valeur par défaut sans erreur, on écrit d.get('z', 0).

**Geste à installer.** Un dictionnaire s'indexe par clé, pas par position. L'accès à une clé absente lève une erreur.

**Erreur à surveiller chez cet élève.** Suppose à tort que la clé 'b' n'existe pas. (constatée à l'item 7 du positionnement, donné avec une certitude de 4/4.)

### Exercice 2 — Types construits

**Énoncé.** Écrire les instructions qui ajoutent à d la clé 'z' de valeur 30, puis suppriment la clé 'x', puis parcourent d en affichant chaque couple clé-valeur.

**Corrigé.** d['$z'] = 30$ crée l'entrée. del d['x'] (ou d.pop('x')) la supprime. Le parcours s'écrit : for cle, valeur in d.items(): print(cle, valeur).

**Geste à installer.** Une affectation d[clé] $=$ valeur crée l'entrée si elle n'existe pas et la remplace sinon ; del d[clé] la supprime.

**Erreur à surveiller chez cet élève.** == est un test d'égalité, il n'affecte aucune valeur. (constatée à l'item 8 du positionnement, donné avec une certitude de 3/4.)

### Exercice 3 — Algorithmique

**Énoncé.** Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour une recherche dichotomique ? Et pour une recherche séquentielle ?

**Corrigé.** La dichotomie effectue de l'ordre de $\log_2(1 000) \approx 10$ comparaisons au pire, car $2^{10} = 1 024$. La recherche séquentielle en effectue jusqu'à 1 000 : c'est le gain qui justifie de trier.

**Geste à installer.** À chaque étape la taille est divisée par deux : le nombre d'étapes est de l'ordre de $\log_2(n)$. Retenir les repères : $2^{10} \approx 1 000$, $2^{20} \approx 1 000 000$.

**Erreur à surveiller chez cet élève.** Suppose que l'on divise une seule fois la taille par deux. (constatée à l'item 14 du positionnement, donné avec une certitude de 3/4.)

### Exercice 4 — Données en tables

**Énoncé.** Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête. Combien de lignes contient le fichier ? Combien d'enregistrements ? Combien de descripteurs ?

**Corrigé.** Le fichier contient 501 lignes : 1 ligne d'en-tête et 500 lignes de données. Il y a donc 500 enregistrements et 6 descripteurs.

**Geste à installer.** Une ligne est un enregistrement (un individu, un objet) ; une colonne est un descripteur (un attribut). La première ligne du fichier contient en général les noms des descripteurs.

**Erreur à surveiller chez cet élève.** La colonne est verticale ; la ligne décrit un enregistrement. (constatée à l'item 15 du positionnement, donné avec une certitude de 2/4.)

### Exercice 5 — Données en tables

**Énoncé.** Ne garder que les colonnes « nom » et « note » d'une table : de quelle opération s'agit-il ? Et rapprocher une table « élèves » d'une table « classes » par l'identifiant de classe ? Écrire la première en SQL.

**Corrigé.** Ne garder que certaines colonnes est une projection ; rapprocher deux tables par un attribut commun est une jointure. En SQL : SELECT nom, note FROM eleves ;

**Geste à installer.** Sélection : on choisit des lignes selon une condition. Projection : on choisit des colonnes. Jointure : on rapproche deux tables par un attribut commun.

**Erreur à surveiller chez cet élève.** Le tri réordonne les lignes sans en supprimer. (constatée à l'item 16 du positionnement, donné avec une certitude de 4/4.)

### Exercice 6 — Représentation binaire

**Énoncé.** Écrire 22 en binaire, puis vérifier en recalculant la valeur décimale.

**Corrigé.** $22 = 16 + 4 + 2 = 2^4 + 2^2 + 2^1$, ce qui s'écrit 10110. Vérification : $16 + 0 + 4 + 2 + 0 = 22$.

**Geste à installer.** Décomposer en somme de puissances de 2 décroissantes, ou diviser successivement par 2 et lire les restes de bas en haut.

**Erreur à surveiller chez cet élève.** Vaut 14 : décale d'une unité. (constatée à l'item 1 du positionnement, donné avec une certitude de 3/4.)

### Exercice 7 — Représentation binaire

**Énoncé.** Convertir 0x2A en base 10, puis convertir 60 en hexadécimal.

**Corrigé.** $0x2A = 2 \times 16 + 10 = 42$. Pour 60 : $60 = 3 \times 16 + 12$, et 12 s'écrit C, donc 60 s'écrit 0x3C.

**Geste à installer.** En hexadécimal, $A = 10$, $B = 11$, $C = 12$, $D = 13$, $E = 14$, $F = 15$. Chaque position vaut une puissance de 16.

**Erreur à surveiller chez cet élève.** Traite F comme s'il valait 9. (constatée à l'item 2 du positionnement, donné avec une certitude de 1/4.)

### Exercice 8 — Programmation

**Énoncé.** Soit def $h(L)$: L.append(0). Que vaut r après $r = h([1$, 2]) ? Si on écrit $M = [1$, 2] puis $h(M)$, que contient M ?

**Corrigé.** h ne comporte pas de return : r vaut None. En revanche la liste est mutable et modifiée en place, donc après $h(M)$ la liste M contient [1, 2, 0].

**Geste à installer.** Sans return, une fonction renvoie None. Une fonction peut modifier un objet mutable reçu en paramètre tout en renvoyant None : ce sont deux choses distinctes.

**Erreur à surveiller chez cet élève.** Confond l'absence de valeur avec une chaîne vide. (constatée à l'item 10 du positionnement, donné avec une certitude de 2/4.)

### Exercice 9 — Programmation

**Énoncé.** Soit $s = 0$ puis « for i in range(1, 6): $s = s + i$*i ». Que vaut s ? Dresser la table de trace.

**Corrigé.** range(1, 6) produit 1, 2, 3, 4, 5. Table de trace : s vaut successivement 1, 5, 14, 30 puis 55. Au final $s = 1 + 4 + 9 + 16 + 25 = 55$.

**Geste à installer.** Initialiser l'accumulateur avant la boucle, écrire la valeur des variables à chaque tour dans une table de trace pour vérifier.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

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

### Types construits — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Toutes les structures de données de Terminale sont bâties dessus : listes chaînées, piles, files, arbres et graphes s'implémentent avec des listes et des dictionnaires. Une confusion sur l'indexation ou sur la mutabilité se paie immédiatement dans ces implémentations.

### Algorithmique — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Diviser pour régner, programmation dynamique, parcours d'arbres et de graphes, recherche textuelle : tous ces algorithmes se justifient par un raisonnement sur le coût, dans la continuité directe de la dichotomie de Première.

### Données en tables — CONFRONTER

Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la notion avant tout entraînement.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** Le chapitre « Bases de données » reprend ces opérations dans le modèle relationnel : sélection, projection et jointure deviennent SELECT, WHERE et JOIN en SQL, avec en plus les contraintes d'intégrité et la notion de clé.

### Représentation binaire — INSTALLER

La difficulté est repérée et assumée : il n'y a aucune fausse certitude à défaire. On pose les définitions utiles, on montre des exemples résolus, puis on entraîne court et souvent.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** La représentation en machine reste sous-jacente partout en Terminale : typage des attributs d'une base de données, coût mémoire des structures de données, arithmétique modulaire du chiffrement dans la sécurisation des communications, adressage réseau.

### Programmation — INSTALLER

La difficulté est repérée et assumée : il n'y a aucune fausse certitude à défaire. On pose les définitions utiles, on montre des exemples résolus, puis on entraîne court et souvent.

**Ce que ce domaine conditionne en Terminale — repère pour vous, non à lire tel quel.** La récursivité, la modularité, la programmation objet et la mise au point systématique s'appuient entièrement sur une compréhension juste de l'appel de fonction, du retour et de la portée des variables.

## Décision de fin de parcours

| Domaine | Situation initiale | Situation finale | Décision pour septembre |
|---|---|---|---|
| Représentation binaire | Difficulté repérée, sans fausse certitude | | |
| Booléens et logique | Acquis disponible | | |
| Types construits | Certitude à revoir | | |
| Programmation | Difficulté repérée, sans fausse certitude | | |
| Algorithmique | Certitude à revoir | | |
| Données en tables | Certitude à revoir | | |
| Architecture et systèmes | Acquis disponible | | |

---
_Document enseignant. Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
