# Règles de correction et d'interprétation

Toutes les règles de ce document sont appliquées par du code, et chacune est couverte par
un test.

## 1. Les invariants de saisie

### Un critère intégralement réussi ne porte aucun code d'erreur

Le serveur refuse l'enregistrement, avec un message explicite. Une **observation** libre
reste possible : « réponse correcte mais rédaction peu lisible » n'est pas une erreur, et
ne doit pas polluer le profil d'erreurs.

### Un zéro n'oblige à aucune cause

Deux statuts existent à côté du score :

| statut | sens |
| --- | --- |
| `NOT_ANSWERED` | l'élève n'a rien écrit |
| `UNCLASSIFIED` | zéro, mais la cause n'est pas identifiable depuis la copie |

Aucun des deux ne porte de code d'erreur. Fabriquer une cause fausserait le profil
d'erreurs, donc le plan de rentrée.

### Une méthode correcte n'est jamais une erreur

Développer une équation-produit avant de la résoudre est plus long ; ce n'est pas faux.
Calculer un troisième côté par Pythagore pour employer ensuite le cosinus est une voie
valable. On coche `accepted_alternative_method` et on écrit l'observation. Jamais un code
`CONCEPT` tant que le raisonnement tient.

### Un score reste dans le barème

L'interface propose une échelle courte, adaptée au maximum du critère : les quarts quand
le maximum est un multiple de 0,25, les moitiés sinon. Le serveur accepte tout multiple de
0,05 compris entre 0 et le maximum — un correcteur qui a une raison d'accorder 0,6 sur 0,7
n'a pas à contourner l'outil.

### Un critère mixte se note par ses sous-critères

Les trois critères mixtes du corpus ne sont pas notés globalement : ce sont leurs
sous-critères analytiques qui reçoivent un score. La somme des maximums est strictement
égale aux points du critère imprimé, et la validation le vérifie. Aucun point n'est
compté deux fois.

## 2. Les deux décomptes, qui ne se mélangent jamais

| portée | ce que c'est | ce que l'échec produit |
| --- | --- | --- |
| `n_minus_1` | acquis attendus à l'entrée dans l'année | peut fonder P1, P2, P3 ou OK |
| `bridge_n` | notion du programme de l'année qui commence, découverte pendant la séance | **jamais** de priorité de remédiation, jamais « fragile », jamais « lacune » |
| `mixed` | critère indivisible rétribuant les deux | éclaté en sous-critères, chacun dans sa portée |

Le score brut sur 20 additionne les deux. Il est donc nommé, partout, **score brut au
sujet de clôture**, jamais « niveau », « progression » ou « maîtrise ».

## 3. Les statuts pédagogiques

### Acquis de l'année précédente

| statut | condition |
| --- | --- |
| `PREUVE_INSUFFISANTE` | force de preuve `INSUFFICIENT` |
| `A_CONFIRMER` | taux ≥ 85 % mais compétence mesurée juste après sa remédiation |
| `SOLIDE` | taux ≥ 85 % et force de preuve au moins `MODERATE` |
| `SATISFAISANT` | taux ≥ 85 % avec preuve faible, ou taux ≥ 60 % avec preuve au moins `MODERATE` |
| `A_CONSOLIDER` | taux ≥ 40 %, ou taux ≥ 60 % avec preuve faible |
| `PRIORITAIRE` | taux < 40 % |

**Un score parfait sur une preuve faible ne donne jamais `SOLIDE`.** C'est la règle qui
empêche de conclure trop vite depuis un critère isolé.

### Priorités qui en découlent

`PRIORITAIRE` → P1 si la compétence est critique, sinon P2. `A_CONSOLIDER` → P2 si
critique, sinon P3. `SATISFAISANT` → P3 si critique, sinon OK. `PREUVE_INSUFFISANTE` →
P3, à revérifier avant de conclure. `SOLIDE` et `A_CONFIRMER` → OK. Le nombre de P1 est
plafonné à quatre : un plan que personne ne tient ne sert à rien.

### Passerelles vers l'année à venir

| statut | condition | action |
| --- | --- | --- |
| `PROMISING` | taux ≥ 85 % | `DISCOVERY_TO_CONTINUE` |
| `FIRST_EXPOSURE` | taux ≥ 60 % | `DISCOVERY_TO_CONTINUE` |
| `BRIDGE_REVISIT` | taux ≥ 25 % | `BRIDGE_REVISIT` |
| `DISCOVERY_TO_CONTINUE` | taux < 25 % | `BRIDGE_REVISIT` |
| `NO_CONCLUSION` | force de preuve `INSUFFICIENT` | `BRIDGE_REVISIT` |

Aucun de ces libellés ne contient un terme de déficit. On ne peut pas manquer ce qui n'a
pas encore été enseigné.

## 4. La force de preuve

Ce n'est pas une fiabilité statistique, et le terme est proscrit : aucune étude de
fiabilité n'a été conduite, et douze items n'en permettraient pas. C'est un décompte, avec
un barème publié.

| condition | poids |
| --- | ---: |
| au moins deux critères indépendants | +1 |
| au moins deux items distincts | +1 |
| au moins deux points en jeu | +1 |
| au moins deux types de preuve différents | +1 |
| une tâche de transfert réussie | +1 |
| énoncé sans limite d'interprétation connue | +1 |
| comparable au diagnostic initial | +1 |
| compétence mesurée moins d'une heure après sa remédiation | −1 |

Seuils : ≤ 0 `INSUFFICIENT`, 1–2 `LOW`, 3–4 `MODERATE`, ≥ 5 `STRONG`.

## 5. L'effet de récence

Une compétence retravaillée pendant la séance puis évaluée moins d'une heure plus tard
porte `post_test_context = immediate_after_remediation`. L'écran de correction l'affiche,
l'analyse la classe `A_CONFIRMER` quand elle est réussie, et le plan de semaine 2 programme
un mini-test différé de dix minutes.

Une réussite y signifie « réussite immédiate après remédiation ». Pas « consolidation
durable ».

## 6. Aucune progression chiffrée

Les réponses initiales question par question n'ont pas été conservées : le dossier ne
garde qu'un statut qualitatif par domaine. Convertir « fragile » en 1 pour en soustraire un
3 produirait un écart sans mesure derrière lui.

`mastery_delta` vaut donc `null` partout, et la phrase suivante figure dans l'analyse et
dans les documents concernés :

> Les réponses initiales item par item n'étant pas disponibles, aucune progression chiffrée
> pré-test/post-test n'est calculée.

La confrontation avec le diagnostic initial reste **qualitative** : « le diagnostic initial
signalait… », puis « l'évaluation finale montre aujourd'hui… ».

## 7. Les quatre questions à correction délicate

Le corrigé affiché au correcteur porte, pour chacune, la règle d'équité issue de la couche
V3.

| élève | item | règle |
| --- | --- | --- |
| Sinda CHIKHAOUI | 4e C2 | l'aire du triangle se justifie par duplication en **parallélogramme** ; l'argument « moitié d'un rectangle » n'est pas recevable comme justification générale |
| Elyes KEFI | 3e B4 | le recomptage ou le recalcul détectent l'omission ; **l'encadrement ne le fait pas ici** et ne peut pas être exigé comme preuve de détection |
| Ahmad BELDI | 1re spé B4 | la consigne imprimée demande un argument valable pour tout `x` : tout argument général correct convient, **aucun formalisme particulier n'est exigé** |
| Malek KHADHRANI | 1re spé C2 | **un contre-exemple suffit** à réfuter la croissance ; la décroissance sur tout l'intervalle n'est pas demandée |

## 8. Ce qui reste hors barème

Le corrigé de l'item B2 des deux élèves de NSI mentionne que `moyenne([])` provoque une
division par zéro. La question imprimée ne le demande pas, et aucun critère ne le rétribue.
L'application l'affiche comme **hors barème** : la remarque peut être dite oralement, elle
n'entre ni dans le score, ni dans le profil d'erreurs, ni dans les priorités, ni dans le
bilan.

En C1, en revanche, le test sur liste vide **est** explicitement demandé par l'énoncé
imprimé : il est légitimement au barème.
