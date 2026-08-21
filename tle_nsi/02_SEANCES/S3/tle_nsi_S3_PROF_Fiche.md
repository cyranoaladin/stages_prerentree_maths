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
| 30 min | Entraînement différencié | Distribue les trois parcours, sur machine | Traite son parcours |
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

| Parcours | Élèves concernés | Support |
|---|---|---|
| Consolidation | Programmation en priorité 1 ou 2 dans le livret | Exercices 1 à 4, tables de trace pré-imprimées |
| Maîtrise | Domaine réussi mais hésitant | Exercices 3 à 6, spécification et deux tests exigés |
| Approfondissement | Domaine acquis avec certitude | Exercices 6 à 8, dont une fonction à effets multiples |

## Évaluation pratique — 20 minutes

Faire passer `03_EVALUATIONS/tle_nsi_Mini_Diagnostic_Pratique_ELEVE.md`. C'est la seule
épreuve **sur machine** du stage : le positionnement initial ne mesurait que des
connaissances déclaratives, pas la capacité à écrire un programme qui tourne.

## Articulation avec le module de mathématiques

Les cinq élèves suivent aussi le module `tle_spe`. Les boucles de calcul des termes d'une
suite y sont écrites en séance 5. Signaler explicitement le lien : c'est le même `range`, le
même risque de décalage d'une unité, et le même contrôle — confronter la sortie du programme
au calcul fait à la main.

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
