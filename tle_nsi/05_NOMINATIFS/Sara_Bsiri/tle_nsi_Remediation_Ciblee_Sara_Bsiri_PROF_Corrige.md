# Terminale NSI — Plan de remédiation ciblée — Sara Bsiri (Corrigé enseignant)
## NSI — Parcours personnalisé

> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  
> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus Réussite et de la famille concernée.

**Élève :** Sara Bsiri  
**Matière :** NSI  
**Diagnostic du :** 2026-08-14  
**Source :** `Bilans/bilan-nexus-eleve_bsiri_nsi.pdf`

## Profil de l'élève, en une page

| Domaine | Réussite | Situation | Posture de travail |
|---|---:|---|---|
| Représentation binaire | 100 % | Réussite hésitante | **CONSOLIDER** |
| Booléens et logique | 100 % | Réussite hésitante | **CONSOLIDER** |
| Types construits | 83,3 % | Difficulté repérée, sans fausse certitude | **INSTALLER** |
| Programmation | 100 % | Réussite hésitante | **CONSOLIDER** |
| Algorithmique | 100 % | Réussite hésitante | **CONSOLIDER** |
| Données en tables | 100 % | Réussite hésitante | **CONSOLIDER** |
| Architecture et systèmes | 100 % | Réussite hésitante | **CONSOLIDER** |

**Ordre de traitement.** Types construits (INSTALLER) $\to$ Représentation binaire (CONSOLIDER) $\to$ Booléens et logique (CONSOLIDER) $\to$ Programmation (CONSOLIDER) $\to$ Algorithmique (CONSOLIDER) $\to$ Données en tables (CONSOLIDER) $\to$ Architecture et systèmes (CONSOLIDER)

**Calibration de la confiance.** Un levier en plus des notions : ton ressenti et tes résultats ne coïncident pas toujours. Apprendre à repérer quand tu es sûr à raison — et quand tu ne l'es pas — vaut autant que le contenu lui-même.

## Composition de la feuille

| # | Item du positionnement | Domaine | Compétence | Motif de sélection |
|---:|---:|---|---|---|
| 1 | item 7 | Types construits | Accéder à une valeur par sa clé dans un dictionnaire | réponse fausse au positionnement |
| 2 | item 1 | Représentation binaire | Convertir un entier de la base 10 vers la base 2 | réussi, domaine classé en réussite hésitante |
| 3 | item 2 | Représentation binaire | Convertir entre base 16 et base 10 | réussi, domaine classé en réussite hésitante |
| 4 | item 3 | Booléens et logique | Évaluer une expression booléenne | réussi, domaine classé en réussite hésitante |
| 5 | item 4 | Booléens et logique | Maîtriser les tables de vérité de la conjonction et de la disjonction | réussi, domaine classé en réussite hésitante |
| 6 | item 9 | Programmation | Comprendre l'appel de fonction et la valeur renvoyée | réussi, domaine classé en réussite hésitante |
| 7 | item 10 | Programmation | Distinguer effet de bord et valeur renvoyée | réussi, domaine classé en réussite hésitante |
| 8 | item 13 | Algorithmique | Connaître la précondition de la recherche dichotomique | réussi, domaine classé en réussite hésitante |
| 9 | item 14 | Algorithmique | Évaluer le coût d'un algorithme de recherche | réussi, domaine classé en réussite hésitante |
| 10 | item 15 | Données en tables | Distinguer enregistrement et descripteur | réussi, domaine classé en réussite hésitante |
| 11 | item 16 | Données en tables | Nommer les opérations sur une table | réussi, domaine classé en réussite hésitante |
| 12 | item 17 | Architecture et systèmes | Identifier les composants du modèle de von Neumann | réussi, domaine classé en réussite hésitante |
| 13 | item 18 | Architecture et systèmes | Décrire le rôle d'un système d'exploitation | réussi, domaine classé en réussite hésitante |

Chaque exercice est la **variante** de l'item que l'élève a manqué ou réussi sans assurance : même compétence, énoncé différent. La feuille d'un autre élève n'a donc pas la même composition.

<div class="page-break"></div>

## Corrigé

### Exercice 1 — Types construits

**Énoncé.** Soit $d =$ {'x': 10, 'y': 20}. Que vaut d['y'] ? Que se passe-t-il si on écrit d['z'] ? Comment obtenir 0 dans ce cas sans erreur ?

**Corrigé.** d['y'] vaut 20. L'expression d['z'] lève une erreur KeyError car la clé n'existe pas. Pour obtenir une valeur par défaut sans erreur, on écrit d.get('z', 0).

**Geste à installer.** Un dictionnaire s'indexe par clé, pas par position. L'accès à une clé absente lève une erreur.

**Erreur à surveiller chez cet élève.** Suppose à tort que la clé 'b' n'existe pas. (constatée à l'item 7 du positionnement.)

### Exercice 2 — Représentation binaire

**Énoncé.** Écrire 22 en binaire, puis vérifier en recalculant la valeur décimale.

**Corrigé.** $22 = 16 + 4 + 2 = 2^4 + 2^2 + 2^1$, ce qui s'écrit 10110. Vérification : $16 + 0 + 4 + 2 + 0 = 22$.

**Geste à installer.** Décomposer en somme de puissances de 2 décroissantes, ou diviser successivement par 2 et lire les restes de bas en haut.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 3 — Représentation binaire

**Énoncé.** Convertir 0x2A en base 10, puis convertir 60 en hexadécimal.

**Corrigé.** $0x2A = 2 \times 16 + 10 = 42$. Pour 60 : $60 = 3 \times 16 + 12$, et 12 s'écrit C, donc 60 s'écrit 0x3C.

**Geste à installer.** En hexadécimal, $A = 10$, $B = 11$, $C = 12$, $D = 13$, $E = 14$, $F = 15$. Chaque position vaut une puissance de 16.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 4 — Booléens et logique

**Énoncé.** Que vaut l'expression (not True) or (False and True) ? Détailler l'ordre d'évaluation.

**Corrigé.** not True vaut False ; False and True vaut False ; False or False vaut False. L'expression vaut donc False.

**Geste à installer.** Évaluer de l'intérieur vers l'extérieur, en respectant la priorité : not, puis and, puis or.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 5 — Booléens et logique

**Énoncé.** L'expression « A ET B » est vraie uniquement lorsque… ? Écrire la table de vérité complète de A ET B, puis celle de non(A ET B).

**Corrigé.** « A ET B » n'est vraie que si A et B sont tous les deux vrais. Table : (V,$V) \to V ; (V$,$F) \to F ; (F$,$V) \to F ; (F$,$F) \to F$. Sa négation non(A ET B) vaut respectivement F, V, V, V : c'est « non A OU non B » (loi de De Morgan).

**Geste à installer.** Une disjonction n'est fausse que si les deux opérandes sont faux ; une conjonction n'est vraie que si les deux sont vrais. Écrire la table de vérité plutôt que se fier à l'intuition.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 6 — Programmation

**Énoncé.** Soit def $g(n)$: return n*n + 1. Que renvoie $g(4)$ ? Que vaut $g(g(1))$ ?

**Corrigé.** $g(4)$ renvoie $4 \times 4 + 1 = 17$. Pour $g(g(1))$ : $g(1) = 1 \times 1 + 1 = 2$, puis $g(2) = 2 \times 2 + 1 = 5$.

**Geste à installer.** Le paramètre prend la valeur de l'argument à l'appel ; return renvoie une valeur à l'appelant et termine la fonction.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 7 — Programmation

**Énoncé.** Soit def $h(L)$: L.append(0). Que vaut r après $r = h([1$, 2]) ? Si on écrit $M = [1$, 2] puis $h(M)$, que contient M ?

**Corrigé.** h ne comporte pas de return : r vaut None. En revanche la liste est mutable et modifiée en place, donc après $h(M)$ la liste M contient [1, 2, 0].

**Geste à installer.** Sans return, une fonction renvoie None. Une fonction peut modifier un objet mutable reçu en paramètre tout en renvoyant None : ce sont deux choses distinctes.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 8 — Algorithmique

**Énoncé.** Peut-on appliquer directement la recherche dichotomique au tableau [4, 1, 9, 3] ? Que faut-il faire avant ? Quel est alors le coût total ?

**Corrigé.** Non : le tableau n'est pas trié, la précondition n'est pas vérifiée. Il faut le trier d'abord. Le coût total devient celui du tri (de l'ordre de n log n pour un tri efficace, $n^2$ pour un tri par insertion) suivi de la recherche en log n : le tri domine, sauf si l'on effectue de nombreuses recherches sur le même tableau.

**Geste à installer.** La dichotomie compare à l'élément central pour éliminer une moitié : cette élimination n'est valide que sur un tableau trié. La précondition fait partie de la spécification.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 9 — Algorithmique

**Énoncé.** Dans un tableau trié de 1 000 éléments, combien de comparaisons au pire pour une recherche dichotomique ? Et pour une recherche séquentielle ?

**Corrigé.** La dichotomie effectue de l'ordre de $\log_2(1 000) \approx 10$ comparaisons au pire, car $2^{10} = 1 024$. La recherche séquentielle en effectue jusqu'à 1 000 : c'est le gain qui justifie de trier.

**Geste à installer.** À chaque étape la taille est divisée par deux : le nombre d'étapes est de l'ordre de $\log_2(n)$. Retenir les repères : $2^{10} \approx 1 000$, $2^{20} \approx 1 000 000$.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 10 — Données en tables

**Énoncé.** Un fichier CSV décrit 500 élèves par 6 attributs, avec une ligne d'en-tête. Combien de lignes contient le fichier ? Combien d'enregistrements ? Combien de descripteurs ?

**Corrigé.** Le fichier contient 501 lignes : 1 ligne d'en-tête et 500 lignes de données. Il y a donc 500 enregistrements et 6 descripteurs.

**Geste à installer.** Une ligne est un enregistrement (un individu, un objet) ; une colonne est un descripteur (un attribut). La première ligne du fichier contient en général les noms des descripteurs.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 11 — Données en tables

**Énoncé.** Ne garder que les colonnes « nom » et « note » d'une table : de quelle opération s'agit-il ? Et rapprocher une table « élèves » d'une table « classes » par l'identifiant de classe ? Écrire la première en SQL.

**Corrigé.** Ne garder que certaines colonnes est une projection ; rapprocher deux tables par un attribut commun est une jointure. En SQL : SELECT nom, note FROM eleves ;

**Geste à installer.** Sélection : on choisit des lignes selon une condition. Projection : on choisit des colonnes. Jointure : on rapproche deux tables par un attribut commun.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 12 — Architecture et systèmes

**Énoncé.** Dans le modèle de von Neumann, quel élément stocke les instructions du programme en cours d'exécution ? Quel élément séquence leur exécution ? Quel est le rôle des bus ?

**Corrigé.** La mémoire stocke à la fois les données et les instructions — c'est le principe même du modèle de von Neumann. L'unité de commande (ou de contrôle) séquence l'exécution des instructions. Les bus assurent le transport des adresses, des données et des signaux de commande entre les composants.

**Geste à installer.** Le processeur contient l'unité arithmétique et logique (les calculs) et l'unité de commande (le séquencement) ; la mémoire contient données et instructions ; les bus les relient.

**Point de vigilance.** L'item était réussi mais avec une certitude faible : l'objectif est la **vitesse et l'assurance**, pas la compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.

### Exercice 13 — Architecture et systèmes

**Énoncé.** Citer trois ressources gérées par un système d'exploitation, puis deux commandes du shell agissant sur le système de fichiers en précisant leur effet.

**Corrigé.** Le système d'exploitation gère notamment la mémoire, le processeur (ordonnancement des processus), les périphériques et le système de fichiers. Côté shell : ls affiche le contenu du répertoire courant, cd change de répertoire courant, mkdir crée un répertoire, pwd affiche le chemin du répertoire courant.

**Geste à installer.** Le système d'exploitation est l'intermédiaire entre les programmes et le matériel : il gère mémoire, processeur, périphériques, fichiers et processus.

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
| 10 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 11 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 12 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |
| 13 | $\square$ | $\square$ | $\square$ | $\square$ | $\square$ |

## Conduite recommandée

### Types construits — INSTALLER

La difficulté est repérée et assumée : il n'y a aucune fausse certitude à défaire. On pose les définitions utiles, on montre des exemples résolus, puis on entraîne court et souvent.

**Argument à donner à l'élève.** Toutes les structures de données de Terminale sont bâties dessus : listes chaînées, piles, files, arbres et graphes s'implémentent avec des listes et des dictionnaires. Une confusion sur l'indexation ou sur la mutabilité se paie immédiatement dans ces implémentations.

### Représentation binaire — CONSOLIDER

Les réponses sont justes mais l'hésitation se sent encore. On organise un entraînement espacé, sans réenseigner ce qui est déjà compris.

**Argument à donner à l'élève.** La représentation en machine reste sous-jacente partout en Terminale : typage des attributs d'une base de données, coût mémoire des structures de données, arithmétique modulaire du chiffrement dans la sécurisation des communications, adressage réseau.

### Booléens et logique — CONSOLIDER

Les réponses sont justes mais l'hésitation se sent encore. On organise un entraînement espacé, sans réenseigner ce qui est déjà compris.

**Argument à donner à l'élève.** Les conditions composées structurent les invariants de boucle, la preuve de terminaison et de correction d'un algorithme, ainsi que les clauses WHERE d'une requête SQL. Une négation mal formée fausse aussi bien un algorithme qu'une requête.

### Programmation — CONSOLIDER

Les réponses sont justes mais l'hésitation se sent encore. On organise un entraînement espacé, sans réenseigner ce qui est déjà compris.

**Argument à donner à l'élève.** La récursivité, la modularité, la programmation objet et la mise au point systématique s'appuient entièrement sur une compréhension juste de l'appel de fonction, du retour et de la portée des variables.

### Algorithmique — CONSOLIDER

Les réponses sont justes mais l'hésitation se sent encore. On organise un entraînement espacé, sans réenseigner ce qui est déjà compris.

**Argument à donner à l'élève.** Diviser pour régner, programmation dynamique, parcours d'arbres et de graphes, recherche textuelle : tous ces algorithmes se justifient par un raisonnement sur le coût, dans la continuité directe de la dichotomie de Première.

### Données en tables — CONSOLIDER

Les réponses sont justes mais l'hésitation se sent encore. On organise un entraînement espacé, sans réenseigner ce qui est déjà compris.

**Argument à donner à l'élève.** Le chapitre « Bases de données » reprend ces opérations dans le modèle relationnel : sélection, projection et jointure deviennent SELECT, WHERE et JOIN en SQL, avec en plus les contraintes d'intégrité et la notion de clé.

### Architecture et systèmes — CONSOLIDER

Les réponses sont justes mais l'hésitation se sent encore. On organise un entraînement espacé, sans réenseigner ce qui est déjà compris.

**Argument à donner à l'élève.** En Terminale : gestion des processus et des ressources, ordonnancement, interblocage, protocoles de routage (RIP, OSPF), sécurisation des communications. La connaissance du modèle de von Neumann est le socle de tout le chapitre.

## Décision de fin de parcours

| Domaine | Situation initiale | Situation finale | Décision pour septembre |
|---|---|---|---|
| Représentation binaire | Réussite hésitante | | |
| Booléens et logique | Réussite hésitante | | |
| Types construits | Difficulté repérée, sans fausse certitude | | |
| Programmation | Réussite hésitante | | |
| Algorithmique | Réussite hésitante | | |
| Données en tables | Réussite hésitante | | |
| Architecture et systèmes | Réussite hésitante | | |

---
_Document enseignant. Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
