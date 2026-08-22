# Terminale Spécialité Physique-Chimie — Séance 4 — Fiche élève
## Ondes et optique : période, célérité, longueur d'onde, lentilles minces

**Ton objectif de séance :** savoir dire *quelle grandeur est imposée par la source* et
*quelle grandeur est imposée par le milieu*.

### Règle de travail

- Avant d'accepter une relation, je **pose les unités** et je vérifie qu'elles collent.
- En optique, je nomme $F$ et $F'$ sur le schéma **avant** de tracer un rayon.
- Je note la certitude de ma réponse : $\square$1 $\square$2 $\square$3 $\square$4.
- Je note l'aide que j'ai utilisée : A, B, C, D ou E.

---

## Partie 1 — Avant tout : ta réponse spontanée

**Question 0.** Une onde sonore passe de l'air à l'eau. Que devient sa fréquence ?

Ma réponse : ..................................................  Ma certitude : $\square$1 $\square$2 $\square$3 $\square$4

Maintenant : qu'est-ce qui, physiquement, décide de la fréquence d'un son ?

....................................................................................................

L'eau peut-elle changer la vitesse à laquelle la source vibre ?

....................................................................................................

**Le contre-exemple.** Si la fréquence changeait dans l'eau, une note jouée à la surface
serait entendue plus grave par un plongeur. L'est-elle ?

....................................................................................................

---

## Partie 2 — La trace écrite

> **La relation des ondes.**
> $$\lambda = v \times T = \frac{v}{f}$$
>
> | Grandeur | Imposée par | Change en changeant de milieu ? |
> |---|---|---|
> | Fréquence $f$ | la **source** | **non** |
> | Période $T = 1/f$ | la **source** | **non** |
> | Célérité $v$ | le **milieu** | **oui** |
> | Longueur d'onde $\lambda$ | les deux | **oui** |
>
> **Contrôle par les unités.** $\si{\metre} = \dfrac{ \si{\metre\per\second} }{ \si{\per\second} }$
> est cohérent. Le produit $v \times f$ ne l'est pas : il ne donne pas une longueur.
>
> **Contrôle qualitatif.** Plus la fréquence est grande, plus la longueur d'onde est
> **petite**. Un son aigu a une longueur d'onde plus courte qu'un son grave.
>
> **Les trois rayons particuliers d'une lentille mince convergente.**
>
> 1. Un rayon **parallèle à l'axe optique** émerge en passant par le foyer image $F'$.
> 2. Un rayon **passant par le foyer objet** $F$ émerge parallèle à l'axe optique.
> 3. Un rayon **passant par le centre optique** $O$ **n'est pas dévié**.
>
> **Objet à l'infini.** Les rayons arrivent parallèles entre eux. Ils convergent tous dans
> le **plan focal image**. Pas au centre optique : le centre optique est un point de la
> lentille, pas un lieu de convergence.

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

**Exercice 1.** Un son de fréquence $\SI{440}{\hertz}$ se propage dans l'air, où la célérité
vaut $\SI{340}{\metre\per\second}$. Calculer sa longueur d'onde.

Relation utilisée : ......................................................................

Calcul : ...........................................................................................

Résultat : ..............................  Unité : ..........

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 2.** Le même son passe dans l'eau, où la célérité vaut
$\SI{1500}{\metre\per\second}$. Que valent sa fréquence et sa longueur d'onde dans l'eau ?

Fréquence : ..............................  Longueur d'onde : ..............................

Justification de la fréquence : ...........................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 3.** Sur le schéma ci-dessous, trace les trois rayons particuliers issus du
point $B$, puis place l'image $B'$.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=10mm,y=10mm]
  \draw[TextGray,thin,->] (-5.6,0) -- (5.8,0) node[right,font=\small] {axe optique};
  \draw[Navy,very thick] (0,-2.1) -- (0,2.1);
  \draw[Navy,thick] (-0.22,1.88) -- (0,2.1) -- (0.22,1.88);
  \draw[Navy,thick] (-0.22,-1.88) -- (0,-2.1) -- (0.22,-1.88);
  \foreach \x/\lab/\pos in {-2.5/F/below,2.5/{F'}/below,0/O/{below left}}
     {\fill (\x,0) circle (1.7pt); \node[\pos=1mm,font=\small] at (\x,0) {$\lab$};}
  \draw[->,Red,very thick] (-4.2,0) -- (-4.2,1.5) node[above,font=\small] {$B$};
  \node[Red,font=\small,below] at (-4.2,0) {$A$};
\end{tikzpicture}
\end{center}
```

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 4.** Un objet est situé à l'infini. Où se forme son image ? Cocher la bonne
réponse et justifier.

$\square$ au centre optique  $\square$ dans le plan focal image  $\square$ à l'infini

Justification : ...........................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

### Exercices 3 à 6 — piste Consolider

**Exercice 5.** Une onde a une longueur d'onde de $\SI{2.5}{\metre}$ et se propage à
$\SI{20}{\metre\per\second}$. Calculer sa fréquence et sa période.

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

**Exercice 6.** Un objet réel est placé **entre** le foyer objet $F$ et le centre optique
$O$. Construire l'image et préciser si elle est réelle ou virtuelle, droite ou renversée.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

### Exercices 6 à 8 — piste Entretenir

**Exercice 7.** Deux lentilles convergentes sont placées sur le même axe, la seconde après
la première. Un objet est à l'infini. Où se forme l'image donnée par la première lentille,
et quel rôle joue-t-elle pour la seconde ?

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

**Exercice 8.** Une source sonore s'approche d'un observateur immobile. La fréquence
perçue augmente. Est-ce en contradiction avec ce que tu as établi aujourd'hui — que la
fréquence ne change pas d'un milieu à l'autre ? Justifier.

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

....................................................................................................

Certitude : $\square$1 $\square$2 $\square$3 $\square$4   Aide utilisée : $\square$A $\square$B $\square$C $\square$D $\square$E

---

## Partie 4 — Ce que la Terminale en fera

**Diffraction et interférences.** Les deux se quantifient à partir de $\lambda$. L'écart
angulaire de diffraction vaut $\theta = \lambda / a$, où $a$ est la largeur de la fente :
la longueur d'onde d'aujourd'hui, dans une relation de demain.

**Effet Doppler.** Quand une source s'**approche**, la fréquence perçue augmente. Ce n'est
pas une contradiction : ici ce n'est pas le milieu qui change, c'est le mouvement relatif
de la source et de l'observateur.

**Lunette astronomique.** Deux lentilles convergentes en série. Un objet à l'infini donne
une image dans le plan focal de la première, qui sert d'objet à la seconde. Les trois
rayons d'aujourd'hui suffisent à construire toute la lunette.

**Et une nouveauté :** la lumière décrite comme un flux de **photons**, avec des
transitions d'énergie. Là, le tracé géométrique cède la place à un bilan énergétique.

---

## Partie 5 — Bilan de séance

**Ma certitude en fin de séance :**

- sur la relation $\lambda = v/f$ : $\square$1 $\square$2 $\square$3 $\square$4
- sur les trois rayons particuliers : $\square$1 $\square$2 $\square$3 $\square$4

**Ce que je sais faire maintenant et que je ne savais pas faire ce matin :**

....................................................................................................

**Avant la prochaine séance :** retracer les trois rayons particuliers de mémoire, sur une
feuille blanche.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
