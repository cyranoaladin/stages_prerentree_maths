# Terminale Spécialité Physique-Chimie — Séance 3 — Fiche professeur
## Énergie : travail, énergies cinétique et potentielle, énergie mécanique

**Durée :** 2 heures · **Effectif :** 3 élèves · **Source pédagogique :** `stage_prerentree_terminale_pc.md`

## Pourquoi cette séance à ce rang

Réussite moyenne du domaine : **41,7 %**, et l'écart entre les élèves y est le plus grand
du stage — de 0 % à 100 %. La séance est donc conduite en différencié dès la phase
d'entraînement.

L'erreur structurante est partagée par deux élèves sur trois : à la question du travail
du poids lors d'un déplacement **horizontal**, tous deux ont répondu qu'il est « maximal,
car le poids agit en permanence ». La confusion porte sur ce qu'est un travail : ils
raisonnent sur l'**existence** d'une force, là où le travail dépend de son **orientation**
par rapport au déplacement.

Une élève a par ailleurs donné $mgz$ pour l'énergie cinétique — l'expression de l'énergie
potentielle de pesanteur.

La séance vient après la mécanique, et ce n'est pas indifférent : le travail d'une force
est un **produit scalaire**, et les deux élèves qui suivent aussi le stage de
mathématiques l'ont rencontré à ce titre. Le dire explicitement fait gagner du temps aux
deux disciplines.

## Objectifs de la séance

1. Écrire $W_{AB}(\vv{F}) = \vv{F} \cdot \vv{AB}$ et conclure à un travail **nul** quand
   la force est perpendiculaire au déplacement.
2. Distinguer $E_c = \frac{1}{2}mv^2$ de $E_{pp} = mgz$.
3. Écrire un bilan d'énergie mécanique et repérer les cas de conservation.
4. Contrôler systématiquement l'unité et l'ordre de grandeur d'un résultat énergétique.

## Déroulé minuté

| Durée | Phase | Ce que fait le professeur | Ce que fait l'élève |
|---:|---|---|---|
| $\SI{10}{\minute}$ | Ouverture | Retour sur la séance 2 : un bilan des forces au tableau | Répond, note sa certitude |
| $\SI{20}{\minute}$ | Confrontation | Pose : « une valise tirée horizontalement — que vaut le travail du poids ? » | Répond, déclare sa certitude |
| $\SI{25}{\minute}$ | Reconstruction | Établit $W = F \times AB \times \cos\alpha$ ; balaie les trois cas d'angle | Prend la trace écrite |
| $\SI{30}{\minute}$ | Entraînement différencié | Aiguille chaque élève sur sa piste ; circule ; note les aides utilisées | Traite son parcours |
| $\SI{20}{\minute}$ | Ouverture Terminale | Nomme le premier principe et ce qu'il ajoute au bilan | Observe, note l'ouverture |
| $\SI{15}{\minute}$ | Trace écrite et bilan | Fait remplir la synthèse et l'auto-évaluation | Remplit, déclare sa certitude |

## Conduite de la phase de confrontation

1. Poser la situation sans support : « Tu tires une valise à roulettes sur un sol
   horizontal, sur $\SI{20}{\metre}$. Que vaut le travail du **poids** de la valise ? Notez
   votre réponse **et** votre certitude. »
2. Recueillir par écrit, sans commenter. La réponse attendue est « maximal » ou « grand,
   car le poids agit tout le temps ».
3. Poser alors une question qui déplace le problème : « De combien la valise
   est-elle montée ou descendue ? »
4. Laisser répondre : de rien du tout, le sol est horizontal.
5. Demander : « Et si le poids avait travaillé, où serait passée cette énergie ? »
6. **Seulement alors**, écrire la relation et faire calculer $\cos 90° = 0$.

Le détour par l'altitude est ce qui rend le résultat acceptable : un élève à qui l'on dit
« $\cos 90° = 0$ » retient une règle de calcul ; un élève qui constate que la valise n'a
pas changé d'altitude comprend pourquoi le poids n'a rien transféré.

Faire ensuite énoncer par les élèves : **une force peut s'exercer en permanence sans
jamais travailler.**

## Reconstruction — le travail d'une force constante

$$W_{AB}(\vv{F}) = \vv{F} \cdot \vv{AB} = F \times AB \times \cos\alpha$$

où $\alpha$ est l'angle entre la force et le déplacement.

| Angle $\alpha$ | $\cos\alpha$ | Travail | Interprétation |
|---|---:|---|---|
| $0°$ | $1$ | $W = F \times AB$, maximal, **moteur** | la force pousse dans le sens du déplacement |
| entre $0°$ et $90°$ | entre 0 et 1 | positif, moteur | la force aide |
| $90°$ | $0$ | **nul** | la force n'aide ni ne freine |
| entre $90°$ et $180°$ | négatif | négatif, **résistant** | la force freine |
| $180°$ | $-1$ | $W = -F \times AB$, résistant | la force s'oppose |

**À dire explicitement aux deux élèves qui suivent aussi le stage de mathématiques :**
$\vv{F} \cdot \vv{AB}$ est le **produit scalaire** rencontré en séance 5 de mathématiques.
Le critère « produit scalaire nul $\iff$ vecteurs orthogonaux » et le fait qu'une force
perpendiculaire ne travaille pas sont le **même énoncé**, écrit dans deux langues.

## Reconstruction — les trois énergies

| Grandeur | Expression | Dépend de | Unité |
|---|---|---|---|
| Énergie cinétique | $E_c = \frac{1}{2}mv^2$ | la **vitesse** | joule ($\si{\joule}$) |
| Énergie potentielle de pesanteur | $E_{pp} = mgz$ | l'**altitude** | joule ($\si{\joule}$) |
| Énergie mécanique | $E_m = E_c + E_{pp}$ | les deux | joule ($\si{\joule}$) |

**Trois contrôles à installer :**

1. $E_c$ contient la vitesse **au carré** et le facteur $\frac{1}{2}$. Doubler la vitesse
   quadruple l'énergie cinétique.
2. $E_{pp}$ ne contient aucune vitesse. Un objet immobile en hauteur a une énergie
   potentielle non nulle et une énergie cinétique nulle.
3. Les trois s'expriment en **joules**. Une réponse en newtons ou en watts est fausse
   avant même d'être lue.

**Conservation.** En l'absence de frottement, $E_m$ reste constante : ce que l'objet perd
en altitude, il le gagne en vitesse. C'est la formulation que la Terminale généralisera.

## Entraînement différencié

L'aiguillage suit les cinq postures de la carte maîtrise $\times$ confiance, et non un niveau
supposé. L'attribution se lit dans le livret individuel de chaque élève, rubrique « Ton
parcours, séance par séance » ; la fiche élève porte le même tableau.

| Piste | Posture au diagnostic | Support |
|---|---|---|
| Diagnostiquer | Le domaine de la séance a été laissé sans réponse | Question 0, puis exercices 1 et 2 ; établir ce que l'élève sait avant toute remédiation |
| Confronter | Réponse fausse donnée avec une certitude de 3 ou 4 | Question 0, puis exercices 1 à 4 ; la réponse fausse est produite avant d'être corrigée |
| Installer | Réponse fausse avec une certitude basse | Exercices 1 à 4, angles fournis sur schéma |
| Consolider | Domaine réussi mais hésitant | Exercices 3 à 6, justification écrite exigée |
| Entretenir | Domaine acquis et assumé | Exercices 6 à 8, dont un plan incliné avec frottement |

## Ouverture sur la Terminale — 20 minutes

Poser la question : « Une voiture freine et s'arrête. Son énergie cinétique était de
$\SI{200}{\kilo\joule}$. Où est passée cette énergie ? »

Laisser chercher. La réponse — les freins ont chauffé — est accessible, et c'est
exactement le point d'entrée du premier principe.

Écrire au tableau, **sans le traiter** :

> Le bilan mécanique de Première ne suit que $E_c$ et $E_{pp}$. Quand il y a frottement,
> l'énergie mécanique diminue : elle n'a pas disparu, elle est passée sous une autre
> forme, l'**énergie interne**.
>
> Le **premier principe** de la thermodynamique complète le bilan :
> $$\Delta U = W + Q$$
> où $Q$ est le transfert thermique. Rien n'est perdu ; tout est compté.

Nommer ensuite les trois objets que la Terminale construit là-dessus : flux thermique,
résistance thermique, loi de refroidissement de Newton. Et s'arrêter.

## Erreurs à surveiller et réponses à apporter

| Erreur observée | Réponse |
|---|---|
| « Le travail est maximal car la force agit en permanence » | Demander de combien l'altitude a changé |
| $mgz$ donné pour l'énergie cinétique | Faire écrire les deux expressions côte à côte, souligner ce dont chacune dépend |
| Facteur $\frac{1}{2}$ ou carré oublié dans $E_c$ | Faire calculer $E_c$ pour $v$ puis pour $2v$ et comparer |
| Travail résistant compté positivement | Faire tracer l'angle sur le schéma avant tout calcul |
| Résultat donné sans unité | Refuser la réponse : un nombre sans unité n'est pas un résultat |
| Puissance et énergie confondues | Rappeler que la puissance est une énergie **par seconde** |

## Indicateurs de fin de séance

- L'élève trace l'angle entre la force et le déplacement **avant** de calculer.
- L'élève conclut à un travail nul pour une force perpendiculaire, sans hésiter.
- L'élève écrit $\frac{1}{2}mv^2$ et $mgz$ sans les confondre.
- Toute réponse énergétique porte l'unité $\si{\joule}$.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`. Les objectifs, l'ordre des séances et les diagnostics ne sont pas modifiés ici ; ils y sont déclinés en supports opérationnels._
