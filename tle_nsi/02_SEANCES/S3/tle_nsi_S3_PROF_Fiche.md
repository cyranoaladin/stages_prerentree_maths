# Terminale NSI — Séance 3 — Fiche professeur
## Programmation : fonctions, retour, portée, boucles

**Durée :** 2 heures · **Source pédagogique :** `stage_prerentree_terminale_nsi.md`

## Pourquoi cette séance

La programmation porte **trois certitudes erronées** et affiche 56,7 % de réussite. L'erreur
dominante concerne `return` : une fonction sans `return` renvoie `None`, ce qui n'empêche pas
qu'elle ait modifié un objet mutable reçu en paramètre. Les deux notions sont confondues.

C'est un prérequis bloquant pour la Terminale : une fonction **récursive** renvoie une valeur
construite à partir de la valeur renvoyée par l'appel suivant. Tant que la valeur de retour
n'est pas nette, la récursivité est inaccessible.

La séance s'appuie sur la séance 2 : la mutabilité y a été installée, on en tire ici les
conséquences sur les fonctions.

## Objectifs de la séance

1. Distinguer valeur renvoyée et effet de bord.
2. Maîtriser les bornes de `range`, y compris avec un pas.
3. Construire une table de trace pour un accumulateur.
4. Écrire une spécification et deux tests pour chaque fonction.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| 10 min | Ouverture | Contrôle sur la séance 2 : contenu de L après `L.insert(0, 9)` | Répond, déclare sa certitude |
| 20 min | Confrontation | `r = h([1, 2])` où h ne fait qu'un `append` : que vaut r ? Et la liste ? | Prédit, puis exécute |
| 25 min | Reconstruction | Appel, paramètre, retour, `None` ; portée ; bornes de `range` ; table de trace | Prend la trace écrite |
| 30 min | Entraînement différencié | Aiguille chaque élève sur sa piste, sur machine | Traite son parcours |
| 20 min | Évaluation pratique | Fait passer le mini-diagnostic pratique | Traite l'épreuve sur machine |
| 15 min | Trace écrite et bilan | Fait remplir la fiche de synthèse | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

1. Écrire au tableau :
   ```python
   def h(L):
       L.append(0)

   M = [1, 2]
   r = h(M)
   print("r vaut :", r)
   print("M vaut :", M)
   ```
   Demander **deux** prédictions écrites : la valeur de `r` et le contenu de `M`.
2. Les erreurs attendues : `r` prédit à `[1, 2, 0]`, ou `M` prédit inchangé à `[1, 2]`.
3. **Faire exécuter.** Sortie : `r vaut : None` et `M vaut : [1, 2, 0]`.
4. Laisser le temps du silence. C'est le résultat le plus contre-intuitif du module : la
   fonction « ne renvoie rien » et pourtant « elle a fait quelque chose ».
5. Faire verbaliser la distinction par un élève :
   - **la valeur renvoyée** est ce que l'appel « vaut » — ici `None`, faute de `return` ;
   - **l'effet de bord** est ce que la fonction a changé dans le monde extérieur — ici, elle
     a modifié la liste qu'on lui a passée.
   Les deux sont indépendants : une fonction peut faire les deux, l'une, l'autre, ou aucune.
6. **Puis** faire écrire la version qui renvoie :
   ```python
   def h2(L):
       L.append(0)
       return L
   ```
   Faire constater que `r` vaut maintenant la liste — mais que `M` a été modifiée dans les
   deux cas.

## Reconstruction

**Les quatre cas de figure.** À construire au tableau avec les élèves :

| Fonction | Renvoie | Modifie l'argument |
|---|---|---|
| `def f(x): return x * 2` | une valeur | non |
| `def g(L): L.append(0)` | `None` | oui |
| `def h(L): L.append(0); return L` | une valeur | oui |
| `def k(x): print(x)` | `None` | non |

**Portée.** Une variable créée dans une fonction est **locale** : elle disparaît à la fin de
l'appel. Réaffecter un paramètre entier ne change rien à l'extérieur ; modifier une liste
reçue en paramètre, si.

**Bornes de `range`.**

| Écriture | Valeurs produites | Nombre de tours |
|---|---|---:|
| `range(3)` | 0, 1, 2 | 3 |
| `range(1, 4)` | 1, 2, 3 | 3 |
| `range(2, 10, 3)` | 2, 5, 8 | 3 |
| `range(1, 10, 4)` | 1, 5, 9 | 3 |

La règle : la borne supérieure est **exclue**, toujours.

**Table de trace.** Pour `s = 0` puis `for i in range(1, 6): s = s + i*i` :

| tour | i | i*i | s après |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 4 | 5 |
| 3 | 3 | 9 | 14 |
| 4 | 4 | 16 | 30 |
| 5 | 5 | 25 | 55 |

Imposer ce tableau **avant** toute exécution : c'est le geste central de la séance.

**Spécification et tests.** Chaque fonction écrite est accompagnée :

```python
def moyenne(notes):
    """Prend une liste non vide de nombres, renvoie leur moyenne."""
    return sum(notes) / len(notes)

# Tests
assert moyenne([10, 20]) == 15
assert moyenne([5]) == 5
```

## Entraînement différencié

L'aiguillage suit les cinq postures de la carte maîtrise $\times$ confiance, et non un niveau
supposé. L'attribution se lit dans le livret individuel de chaque élève, rubrique « Ton
parcours, séance par séance » ; la fiche élève porte le même tableau.

| Piste | Posture au diagnostic | Support |
|---|---|---|
| Diagnostiquer | Le domaine de la séance a été laissé sans réponse | Question 0, puis exercices 1 et 2 ; établir ce que l'élève sait avant toute remédiation |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 | Question 0, puis exercices 1 à 4 ; la réponse fausse est produite avant d'être corrigée |
| Installer | Réponse fausse avec une certitude basse | Exercices 1 à 4, tables de trace pré-imprimées |
| Consolider | Domaine réussi mais hésitant | Exercices 3 à 6, spécification et deux tests exigés |
| Entretenir | Domaine acquis et assumé | Exercices 6 à 8, dont une fonction à effets multiples |

## Évaluation pratique — 20 minutes

Faire passer `03_EVALUATIONS/tle_nsi_Mini_Diagnostic_Pratique_ELEVE.md`. C'est la seule
épreuve **sur machine** du stage : le positionnement initial ne mesurait que des
connaissances déclaratives, pas la capacité à écrire un programme qui tourne.

## Articulation avec le module de mathématiques

Les cinq élèves suivent aussi le module `tle_spe`. Les boucles de calcul des termes d'une
suite y sont écrites en séance 5. Signaler explicitement le lien : c'est le même `range`, le
même risque de décalage d'une unité, et le même contrôle — confronter la sortie du programme
au calcul fait à la main.

## Corrigé de la piste excellence

**Exercice 9.** a) Maintenir deux variables, le maximum et le second, et les mettre à jour à
chaque élément : si l'élément dépasse le maximum, l'ancien maximum devient le second ; sinon,
s'il dépasse le second **et diffère du maximum**, il devient le second. L'égalité stricte est
le piège de l'exercice.
b) `L` doit contenir au moins deux valeurs distinctes : `assert len(set(L)) >= 2`.
c) Cas limite acceptable : une liste où le maximum est répété, par exemple `[5, 5, 3]`, qui
doit renvoyer 3.
d) Deux comparaisons par élément au pire, soit environ $2n$ : coût linéaire. Trier puis
prendre l'avant-dernier coûte $n \log n$ — et échoue si le maximum est répété.

**Exercice 10.** a) `UnboundLocalError`. L'affectation `compteur = ...` fait de `compteur` une
variable **locale** pour tout le corps de la fonction ; elle est donc lue avant d'exister.
Le nom global est masqué, pas utilisé.
b) Soit déclarer `global compteur`, soit — nettement préférable — passer la valeur en paramètre
et renvoyer le résultat. La seconde rend la fonction testable et sans effet de bord.
c) Une fonction qui trie une liste en place, ou qui écrit dans un fichier, ne renvoie rien et
sert. L'exercice 8 de la séance en donne deux.
d) Oui, techniquement : `def f(L): L.append(0); return len(L)`. C'est une mauvaise idée parce
que l'appelant ne peut plus prévoir l'état de son argument à la lecture de l'appel — la
spécification doit alors énoncer les deux comportements.

## Corrigé de l'atelier Terminale NSI

a) `empiler` : `self.contenu.append(x)`. `depiler` : `return self.contenu.pop()`.
`est_vide` : `return self.contenu == []`.
b) `p = Pile()` puis `p.empiler(5)` puis `p.depiler()`.
c) `self` désigne l'objet sur lequel la méthode est appelée : c'est par lui que la méthode
atteint `contenu`. Sans lui, Python signale que la méthode reçoit un argument de trop —
l'objet est toujours passé en premier.
d) L'écriture par fonctions laissait n'importe qui manipuler la liste directement, y compris
par `p.insert(0, x)`, ce qui n'est plus une pile. La classe fixe **l'interface** : on ne peut
agir sur le contenu que par les trois méthodes prévues.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| Croire qu'une fonction sans `return` ne fait rien | Reprendre les quatre cas de figure |
| Croire qu'une fonction qui modifie une liste la renvoie | Faire afficher la valeur de retour |
| Décalage d'une unité sur les bornes | Faire écrire les valeurs de `range` avant la boucle |
| Accumulateur initialisé dans la boucle | Faire la table de trace : la remise à zéro apparaît |
| Variable locale prise pour globale | Faire afficher la variable après l'appel |

## Indicateurs de fin de séance

- L'élève écrit une table de trace avant d'exécuter, sans qu'on le lui demande.
- L'élève accompagne chaque fonction d'une spécification et de deux tests.
- L'élève sait dire, pour une fonction donnée, ce qu'elle renvoie **et** ce qu'elle modifie.

---
_Source pédagogique unique : `stage_prerentree_terminale_nsi.md`._
