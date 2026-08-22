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

## Partie 5 — Bilan de séance

**Ce que je sais faire maintenant et que je ne savais pas faire ce matin :**

....................................................................................................

**Ma certitude sur le bilan des forces, en fin de séance :** $\square$1 $\square$2 $\square$3 $\square$4

**Le geste que je dois automatiser :** ..............................................................

**Avant la prochaine séance :** relire la définition de la chute libre, et refaire
l'exercice 5 en nommant l'objet qui exerce chaque force.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
