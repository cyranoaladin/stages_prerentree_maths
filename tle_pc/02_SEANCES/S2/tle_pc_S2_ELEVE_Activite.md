# Terminale Spécialité Physique-Chimie — Séance 2 — Fiche élève
## Mécanique : vecteur vitesse, forces, vers la deuxième loi de Newton

**Ton objectif de séance :** savoir dire ce qu'un **modèle** retient et ce qu'il écarte,
et savoir tracer un vecteur vitesse.

### Règle de travail

- J'écris le système et le référentiel **avant** de lister les forces.
- Pour chaque force, je sais dire **quel objet l'exerce**.
- Je note la certitude de ma réponse : $\square$1 $\square$2 $\square$3 $\square$4.
- Je note l'aide que j'ai utilisée : A, B, C, D ou E.

---

## Partie 1 — Avant tout : ta réponse spontanée

**Question 0.** Un objet en chute libre est soumis à quoi ?

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Maintenant, réponds à cette question : dans « chute **libre** », libre de quoi ?

....................................................................................................

Relis ta première réponse. Y a-t-il une force que la définition écarte ?

....................................................................................................

---

## Partie 2 — La trace écrite

> **Chute libre.** Un corps est en chute libre lorsqu'il est soumis à **son seul poids**.
> Le frottement de l'air n'y figure pas : ce n'est pas un oubli, c'est la définition.
>
> Le frottement existe dans la réalité. Mais un énoncé qui parle de chute libre a décidé
> de le négliger. Si l'énoncé demande d'en tenir compte, le mouvement **n'est plus** une
> chute libre.
>
> **Vecteur vitesse.** En chaque point, le vecteur vitesse est **tangent à la
> trajectoire** et orienté dans le sens du mouvement.
>
> - La trajectoire impose la **direction**. Rien d'autre.
> - La **norme** peut varier d'un point à l'autre, même sur une courbe.
> - Une norme constante sur une trajectoire courbe, c'est le cas particulier du mouvement
>   circulaire **uniforme** — pas une règle générale.
>
> **Bilan des forces — toujours dans cet ordre.**
>
> 1. Le **système** : quel objet ?
> 2. Le **référentiel** : par rapport à quoi ?
> 3. La **liste** des forces extérieures, chacune avec son point d'application, sa
>    direction, son sens.
> 4. Seulement ensuite : une relation.
>
> **Contrôle.** Pour chaque force de ta liste, demande-toi : exercée par **quel objet** ?
> Une force sans objet qui l'exerce n'existe pas.

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
| **INSTALLER** — il te manque quelque chose, et tu le sais | Exercices 1 à 4 | Écrire la relation utilisée **avant** de remplacer par les valeurs |
| **CONSOLIDER** — tu réussis, sans en être sûr | Exercices 3 à 6 | Justifier par écrit, et contrôler l'unité du résultat |
| **ENTRETENIR** — c'est acquis et assumé | Exercices 6 à 8 | Contrôler l'ordre de grandeur et les chiffres significatifs |
| **EXCELLENCE** — ton bilan ne comporte aucun domaine à reprendre, ou tu as terminé ta piste | Exercices 9 et 10, puis l'atelier Terminale | Produire un résultat avec son unité et ses chiffres significatifs, puis relire la copie d'un camarade **sans lui donner la réponse** |

### Exercices 1 à 4 — pistes Diagnostiquer, Confronter et Installer

**Exercice 1.** Une balle est lâchée sans vitesse initiale. On néglige l'action de l'air.
Système, référentiel, bilan des forces.

Système : ..................................  Référentiel : ..................................

Forces : ...........................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** La même balle, mais l'énoncé précise cette fois « en tenant compte de la
résistance de l'air ». Le mouvement est-il encore une chute libre ? Quel est le nouveau
bilan des forces ?

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Sur la trajectoire ci-dessous, trace le vecteur vitesse aux points
$A$, $B$ et $C$. La vitesse est plus grande en $B$ qu'en $A$ et en $C$.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=13mm,y=13mm]
  \draw[Navy,very thick] plot[smooth,domain=0:5.2,samples=80] (\x,{1.4*sin(\x r)+0.2*\x});
  \foreach \x/\lab in {0.9/A, 2.6/B, 4.4/C}
     \fill[Red] (\x,{1.4*sin(\x r)+0.2*\x}) circle (2pt)
        node[below right=0.5mm,font=\small\bfseries] {$\lab$};
\end{tikzpicture}
\end{center}
```

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Un point décrit un cercle à vitesse de norme constante. Le vecteur
vitesse est-il constant ? Justifier.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

### Exercices 3 à 6 — piste Consolider

**Exercice 5.** Un livre est posé, immobile, sur une table horizontale. Bilan des forces.
Pour chacune, nommer l'objet qui l'exerce. Que dit le principe d'inertie de la somme de
ces forces ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 6.** Une pierre est lancée obliquement vers le haut. On néglige l'action de
l'air. Au sommet de la trajectoire, quelle est la direction du vecteur vitesse ? Et celle
du poids ? Le mouvement est-il accéléré à cet instant ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

### Exercices 6 à 8 — piste Entretenir

**Exercice 7.** Un solide glisse sans frottement sur un plan incliné d'un angle $\alpha$
avec l'horizontale. Faire le bilan des forces et préciser la direction de chacune par
rapport au plan.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 8.** Deux affirmations circulent :

- « Un mouvement à vitesse de norme constante n'est pas accéléré. »
- « Un mouvement rectiligne uniforme n'est pas accéléré. »

L'une est fausse, l'autre est vraie. Laquelle, et pourquoi ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Piste excellence — exercices 9 et 10

> **Pour qui.** Ces deux exercices sont les tiens si ton bilan ne comporte aucun domaine à
> reprendre, ou si tu as terminé ta piste avant la fin du temps différencié. Le premier est un
> problème complet : on attend un résultat écrit avec son unité et un nombre de chiffres
> significatifs justifié. Le second part d'une affirmation fausse : on attend un
> contre-exemple précis, puis l'énoncé corrigé.
>
> Une fois tes deux exercices rendus, le professeur pourra te confier la copie d'un camarade.
> Tu ne corriges pas : tu dis si la relation a été écrite avant les valeurs, si l'unité suit
> le résultat, et où le raisonnement s'interrompt.

**Exercice 9.** Un solide de masse $m = \SI{0.50}{\kilogram}$ glisse sur un plan
incliné faisant un angle $\alpha = 30\degree$ avec l'horizontale. On prend
$g = \SI{9.8}{\newton\per\kilogram}$.

a) Faire le bilan des forces et les représenter sur un schéma. Préciser, pour chacune, ce qui
l'exerce.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

b) La composante du poids parallèle au plan vaut $P_x = m g \sin\alpha$. La calculer.

....................................................................................................

....................................................................................................

c) En l'absence de frottement, la réaction du support est perpendiculaire au plan et vaut
$R = m g \cos\alpha$. La calculer.

....................................................................................................

....................................................................................................

d) La somme vectorielle des forces est-elle nulle ? Qu'en déduire sur le vecteur vitesse du
solide au cours du mouvement ?

....................................................................................................

....................................................................................................

....................................................................................................

e) On tient maintenant compte d'une force de frottement de $\SI{1.0}{\newton}$, opposée au
mouvement. Que devient la résultante ? Le mouvement est-il encore accéléré ?

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 10.** Un élève affirme : « un objet immobile n'est soumis à aucune force ».

a) Réfuter à l'aide du livre posé sur la table, étudié en début de séance.

....................................................................................................

....................................................................................................

b) Écrire l'énoncé correct.

....................................................................................................

....................................................................................................

c) « Si les forces se compensent, l'objet est immobile. » Vrai ou faux ? Donner un
contre-exemple.

....................................................................................................

....................................................................................................

....................................................................................................

d) Un satellite décrit une orbite circulaire à vitesse de norme constante. La somme des forces
qu'il subit est-elle nulle ? Raisonner sur le **vecteur** vitesse, pas sur sa norme.

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Partie 4 — Ce que la Terminale en fera

Le **vecteur accélération** mesure la variation du vecteur vitesse. Il n'est pas nul dès
que la vitesse change — **en norme ou en direction**.

Toute la mécanique de Terminale tient dans une seule relation :

$$\sum \vv{F}_{\text{ext}} = m \, \vv{a}$$

C'est une égalité entre **vecteurs**. On la résout en la **projetant** sur des axes :
chaque projection donne une équation. C'est pour cela que le caractère vectoriel de la
vitesse, travaillé aujourd'hui, n'est pas un détail de notation.

Trois mouvements seront traités avec elle : dans un champ de pesanteur uniforme, dans un
champ électrique uniforme, dans un champ de gravitation — avec les lois de Kepler.

---

## Atelier Terminale physique-chimie — 20 minutes

> **Pour qui.** Cet atelier est pour toi si tu as terminé ta piste avant la fin du temps
> différencié, ou si tu suis la piste excellence. Il ne porte pas sur le thème du jour : il
> ouvre une notion du programme de Terminale que la Première n'aborde pas, et que la séance
> rend abordable dès maintenant. Le temps y est prélevé sur la phase différenciée.

**Le lien avec la séance du jour.** Tu viens d'établir que la somme des forces n'est pas nulle et d'en
déduire que le vecteur vitesse varie. La **deuxième loi de Newton**, au programme de
Terminale, chiffre exactement de combien.

Elle s'écrit $\sum \vv{F} = m \vec{a}$, où $\vec{a}$ est le **vecteur accélération** : il
mesure la variation du vecteur vitesse par unité de temps, et il a la même direction et le
même sens que la résultante des forces.

**a)** Reprends le solide de $\SI{0.50}{\kilogram}$ sur le plan incliné à $30\degree$, sans
frottement. La résultante vaut $\SI{2.45}{\newton}$ le long du plan. Calcule la valeur de
l'accélération.

....................................................................................................

....................................................................................................

....................................................................................................

**b)** Cette accélération dépend-elle de la masse du solide ? Reprends le calcul avec
$m = \SI{2.0}{\kilogram}$ et conclus.

....................................................................................................

....................................................................................................

....................................................................................................

**c)** En chute libre verticale, la seule force est le poids. Montre que l'accélération vaut
alors g, quelle que soit la masse.

....................................................................................................

....................................................................................................

....................................................................................................

**d)** Un objet est lancé horizontalement. Le poids est vertical. Que peut-on dire de
l'accélération horizontale ? Et de la composante horizontale du vecteur vitesse ?

....................................................................................................

....................................................................................................

....................................................................................................

**Ce que la Terminale en fera.** Toute la mécanique de l'année tient dans cette relation :
on fait le bilan des forces, on projette sur deux axes, on obtient l'accélération, puis les
équations horaires du mouvement.

---

## Partie 5 — Bilan de séance

**Ce que je sais faire maintenant et que je ne savais pas faire ce matin :**

....................................................................................................

**Ma certitude sur le bilan des forces, en fin de séance :** $\square$1 $\square$2 $\square$3 $\square$4

**Le geste que je dois automatiser :** ..............................................................

**Avant la prochaine séance :** relire la définition de la chute libre, et refaire
l'exercice 5 en nommant l'objet qui exerce chaque force.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
