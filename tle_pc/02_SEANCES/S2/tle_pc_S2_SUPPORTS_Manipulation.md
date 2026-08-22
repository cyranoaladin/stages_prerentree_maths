# Terminale Spécialité Physique-Chimie — Séance 2 — Supports de manipulation
## Mécanique : vecteur vitesse, forces, vers la deuxième loi de Newton

Tous les supports se conduisent **sans matériel**, sur documents.

## Support 1 — Le mot « libre » (confrontation)

À projeter vierge, une colonne à la fois.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.5}
\begin{tabular}{|>{\bfseries}p{42mm}|p{52mm}|p{52mm}|}\hline
\rowcolor{SoftBlue}
Situation & Forces retenues par le modèle & Forces écartées par le modèle \\\hline
Chute libre & & \\\hline
Chute avec résistance de l'air & & \\\hline
Bille dans un fluide visqueux & & \\\hline
\end{tabular}
\end{center}
```

**Réponses pour le professeur.** Chute libre : le poids seul ; la résistance de l'air est
écartée. Chute avec résistance de l'air : poids et force de frottement fluide ; aucune
n'est écartée, ce n'est plus une chute libre. Bille dans un fluide : poids, poussée
d'Archimède, frottement fluide.

**Point à faire émerger.** Ce n'est pas la réalité qui change d'une ligne à l'autre :
c'est le **modèle** que l'énoncé a choisi. Le frottement de l'air existe dans les trois
cas ; seul le premier décide de le négliger.

## Support 2 — Trajectoires à équiper de vecteurs

Trois trajectoires par binôme. L'élève trace la tangente au crayon, puis le vecteur
vitesse par-dessus. Les longueurs demandées sont indiquées sous chaque schéma.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=11mm,y=11mm]
  % --- trajectoire 1 : parabole, vitesse décroissante puis croissante
  \begin{scope}
    \draw[Navy,very thick] plot[smooth,domain=-1.6:1.6,samples=60] (\x,{2.4-0.9*\x*\x});
    \foreach \x in {-1.2,0,1.2} \fill[Red] (\x,{2.4-0.9*\x*\x}) circle (1.8pt);
    \node[font=\small,below] at (0,-0.3) {trajectoire 1 --- vitesse minimale au sommet};
  \end{scope}
  % --- trajectoire 2 : cercle, mouvement circulaire uniforme
  \begin{scope}[xshift=58mm,yshift=12mm]
    \draw[Navy,very thick] (0,0) circle (1.25);
    \foreach \a in {40,160,280} \fill[Red] (\a:1.25) circle (1.8pt);
    \node[font=\small,below] at (0,-1.85) {trajectoire 2 --- norme constante};
  \end{scope}
  % --- trajectoire 3 : ligne droite, mouvement accéléré
  \begin{scope}[xshift=100mm,yshift=12mm]
    \draw[Navy,very thick] (-1.4,-0.8) -- (1.4,0.8);
    \foreach \t in {-1,0,1} \fill[Red] (\t,{0.571*\t}) circle (1.8pt);
    \node[font=\small,below] at (0,-1.85) {trajectoire 3 --- norme croissante};
  \end{scope}
\end{tikzpicture}
\end{center}
```

**Ce qui est vérifié à la correction.** Sur la trajectoire 2, les trois vecteurs ont la
même longueur mais des directions différentes : c'est le point à faire dire à voix haute.
La norme est constante, le **vecteur** ne l'est pas.

## Support 3 — Fiche de contrôle « exercée par quoi ? »

À distribuer, à garder dans le portfolio.

> **Une force sans objet qui l'exerce n'existe pas.**
>
> | Force | Exercée par | Direction |
> |---|---|---|
> | Poids $\vv{P}$ | la Terre | verticale, vers le bas |
> | Réaction du support $\vv{R}$ | le support | perpendiculaire au support si le contact est sans frottement |
> | Tension d'un fil $\vv{T}$ | le fil | le long du fil |
> | Frottement fluide $\vv{f}$ | l'air ou le liquide | opposée au mouvement |
> | Poussée d'Archimède $\vv{\Pi}$ | le fluide | verticale, vers le haut |
>
> **Le contrôle en trois secondes.** Pour chaque force que tu écris, complète la phrase :
> « cette force est exercée par ... ». Si tu ne peux pas la compléter, la force n'existe
> pas. C'est ce contrôle qui élimine la « force qui ralentit la chute ».

## Support 4 — Le bilan des forces en quatre lignes

À afficher pendant toute la séance.

```{=latex}
\begin{center}
\begin{tikzpicture}[node distance=4mm,font=\small,
  every node/.style={rounded corners=2pt,align=left,inner sep=2.5mm,text width=88mm}]
  \node[fill=SoftBlue,draw=Navy,thick] (a) {\textbf{1. Système} --- quel objet j'étudie};
  \node[fill=SoftBlue,draw=Navy,thick,below=of a] (b)
       {\textbf{2. Référentiel} --- par rapport à quoi je décris le mouvement};
  \node[fill=SoftGold,draw=Gold,thick,below=of b] (c)
       {\textbf{3. Liste des forces extérieures} --- chacune avec son point
        d'application, sa direction, son sens};
  \node[fill=SoftGray,draw=TextGray,below=of c] (d)
       {\textbf{4. Seulement ensuite} --- une relation};
  \draw[->,thick,Navy] (a) -- (b); \draw[->,thick,Navy] (b) -- (c);
  \draw[->,thick,TextGray] (c) -- (d);
\end{tikzpicture}
\end{center}
```

L'étape 3 est une **liste**, pas un calcul. Aucune équation ne s'écrit avant qu'elle soit
complète.

## Support 5 — Passerelle vers la Terminale

À projeter en fin de séance.

$$\sum \vv{F}_{\text{ext}} = m \, \vv{a}$$

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.4}
\begin{tabular}{|>{\bfseries}p{40mm}|p{58mm}|p{40mm}|}\hline
\rowcolor{SoftBlue}
Ce que tu sais déjà & Ce que la Terminale ajoute & Ce que cela permet \\\hline
Le vecteur vitesse & Le vecteur accélération, variation du vecteur vitesse & Décrire un mouvement quelconque \\\hline
Le bilan des forces & La deuxième loi de Newton & Prévoir le mouvement à partir des forces \\\hline
La chute libre & Le mouvement dans un champ uniforme & Trajectoire parabolique, portée, flèche \\\hline
\end{tabular}
\end{center}
```

**Le point qui surprend, et qu'il faut faire dire.** Un mouvement circulaire uniforme est
**accéléré**, alors que la norme de la vitesse est constante : c'est la **direction** du
vecteur vitesse qui change. Sans le caractère vectoriel de la vitesse, cette phrase est
incompréhensible.

## Matériel à prévoir

- Le tableau du support 1, projeté ou photocopié vierge.
- Les trois trajectoires du support 2, un jeu par binôme, avec un crayon à papier.
- La fiche « exercée par quoi ? », un exemplaire par élève.
- L'affiche du support 4, agrandie, visible pendant toute la séance.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
