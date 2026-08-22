# Terminale Spécialité Physique-Chimie — Séance 4 — Supports de manipulation
## Ondes et optique : période, célérité, longueur d'onde, lentilles minces

## Support 1 — Qui impose quoi ? (confrontation)

À projeter vierge. L'élève remplit la troisième colonne **avant** toute explication.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.55}
\begin{tabular}{|>{\bfseries}p{34mm}|p{44mm}|p{56mm}|}\hline
\rowcolor{SoftBlue}
Grandeur & Imposée par & Change quand l'onde change de milieu ? \\\hline
Fréquence $f$ & & \\\hline
Période $T$ & & \\\hline
Célérité $v$ & & \\\hline
Longueur d'onde $\lambda$ & & \\\hline
\end{tabular}
\end{center}
```

**Réponses pour le professeur.** Fréquence et période : imposées par la **source**, elles
ne changent pas. Célérité : imposée par le **milieu**, elle change. Longueur d'onde :
conséquence des deux, elle change.

**Point à faire émerger.** Deux lignes sur quatre ne changent pas. C'est la source qui
décide de la fréquence, et l'eau ne peut pas modifier la vitesse à laquelle un
haut-parleur vibre.

## Support 2 — La même note dans deux milieux

À distribuer après la confrontation.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.5}
\begin{tabular}{|>{\bfseries}l|c|c|c|}\hline
\rowcolor{SoftBlue}
Milieu & Fréquence $f$ & Célérité $v$ & Longueur d'onde $\lambda = v/f$ \\\hline
Air & \SI{440}{\hertz} & \SI{340}{\metre\per\second} & \SI{0.77}{\metre} \\\hline
Eau & \SI{440}{\hertz} & \SI{1500}{\metre\per\second} & \SI{3.4}{\metre} \\\hline
Acier & \SI{440}{\hertz} & \SI{5000}{\metre\per\second} & \SI{11}{\metre} \\\hline
\end{tabular}
\end{center}
```

**Ce qui doit être lu à voix haute.** La colonne de gauche ne bouge pas. Les deux autres
sont multipliées par le même facteur. La note reste un la ; c'est sa longueur d'onde qui
change.

**Contrôle par les unités, à faire poser au tableau.**

$$[\lambda] = \frac{\si{\metre\per\second}}{\si{\per\second}} = \si{\metre} \qquad
\text{alors que} \qquad
(\si{\metre\per\second}) \times (\si{\per\second}) = \si{\metre\per\second\squared}$$

L'élève qui écrit $\lambda = v \times f$ obtient une accélération, pas une longueur. Poser
les unités suffit à trancher, sans rien retenir par cœur.

## Support 3 — Les trois rayons, un tracé par rayon

Trois schémas identiques par binôme, à remplir un par un. Chaque schéma ne reçoit **qu'un
seul** rayon : c'est ce qui empêche de les confondre.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=5.4mm,y=5.4mm]
\foreach \k/\titre in {0/{rayon 1 --- parallèle à l'axe},
                       1/{rayon 2 --- par le foyer objet $F$},
                       2/{rayon 3 --- par le centre optique $O$}}
{
  \begin{scope}[xshift=\k*56mm]
    % Un cadre léger par schéma : sans lui, les trois axes se touchaient et se
    % lisaient comme une seule droite portant trois lentilles.
    \draw[SoftGray,fill=SoftGray,rounded corners=1.5mm]
         (-4.5,-2.9) rectangle (4.5,3.1);
    \draw[TextGray,thin,->] (-4.1,0) -- (4.2,0);
    \draw[Navy,very thick] (0,-2.1) -- (0,2.1);
    \draw[Navy,thick] (-0.22,1.88) -- (0,2.1) -- (0.22,1.88);
    \draw[Navy,thick] (-0.22,-1.88) -- (0,-2.1) -- (0.22,-1.88);
    \foreach \x/\lab in {-2.3/F,2.3/{F'},0/O}
       {\fill (\x,0) circle (1.5pt);
        \node[below=0.7mm,font=\scriptsize] at (\x,0) {$\lab$};}
    \draw[->,Red,very thick] (-3.5,0) -- (-3.5,1.7);
    \node[Red,font=\scriptsize,above] at (-3.5,1.7) {$B$};
    \node[Red,font=\scriptsize,below left=0.2mm] at (-3.5,0) {$A$};
    \node[font=\scriptsize,align=center] at (0,-2.55) {\titre};
  \end{scope}
}
\end{tikzpicture}
\end{center}
```

**Corrigé, à ne montrer qu'après le tracé des élèves.** Rayon 1 : de $B$, horizontal
jusqu'à la lentille, puis vers $F'$. Rayon 2 : de $B$ en passant par $F$, puis horizontal
après la lentille. Rayon 3 : de $B$ vers $O$, **et il continue tout droit**.

**Point à faire travailler.** Le rayon 3 est celui qui manque au groupe. Le faire tracer
trois fois, avec des positions d'objet différentes. Ce n'est pas une exception à retenir :
c'est le rayon qui passe par le centre de la lentille et qui, pour cette raison, la
traverse sans être dévié.

## Support 4 — Fiche de contrôle optique

À distribuer, à garder dans le portfolio.

> **Trois confusions à éliminer.**
>
> | Ce qu'on croit | Ce qui est vrai |
> |---|---|
> | Le rayon par $O$ est dévié | Il **n'est pas** dévié : il traverse tout droit |
> | Le rayon par $O$ est réfléchi | Une lentille n'est pas un miroir : la lumière la traverse |
> | L'image d'un objet à l'infini est en $O$ | Elle est dans le **plan focal image** |
>
> **Pourquoi l'objet à l'infini donne une image dans le plan focal.** Les rayons issus
> d'un point à l'infini arrivent **parallèles** entre eux. Or tout faisceau parallèle
> converge dans le plan focal image — c'est la règle 1, appliquée à chacun des rayons du
> faisceau.
>
> **Le centre optique n'est pas un lieu de convergence.** C'est un point **de la
> lentille**, sur l'axe. Rien ne s'y forme.

## Support 5 — Passerelle vers la Terminale

À projeter en fin de séance.

```{=latex}
\begin{center}
\begin{tikzpicture}[node distance=5mm,font=\small,
  every node/.style={rounded corners=2pt,align=center,inner sep=2.5mm,text width=44mm}]
  \node[fill=SoftGold,draw=Gold,thick] (l) {$\lambda = v/f$\\\textit{Première}};
  \node[fill=SoftBlue,draw=Navy,above right=2mm and 16mm of l] (d)
       {Diffraction\\$\theta = \lambda / a$};
  \node[fill=SoftBlue,draw=Navy,below right=2mm and 16mm of l] (i)
       {Interférences\\différence de marche en $\lambda$};
  \draw[->,thick,Navy] (l) -- (d); \draw[->,thick,Navy] (l) -- (i);
  \node[fill=SoftGray,draw=TextGray,below=12mm of l,text width=76mm] (dop)
       {\textbf{Effet Doppler} --- la fréquence \emph{perçue} change quand la source se
        déplace. Ce n'est pas le milieu qui change : c'est le mouvement relatif.};
  \draw[->,thick,TextGray] (l) -- (dop);
\end{tikzpicture}
\end{center}
```

**La distinction à faire dire aux élèves.** Aujourd'hui : la fréquence ne change pas quand
le **milieu** change. En Terminale : la fréquence perçue change quand la **source bouge**.
Les deux énoncés sont compatibles, parce qu'ils ne parlent pas de la même chose.

**Et l'optique.** La lunette astronomique est une association de deux lentilles
convergentes ; le modèle de l'œil est une lentille et un écran. Aucun rayon nouveau n'est
introduit : ceux d'aujourd'hui suffisent.

## Matériel à prévoir

- Le tableau du support 1, projeté ou photocopié vierge.
- Le tableau des trois milieux, distribué **après** la confrontation.
- Les trois schémas de lentille, un jeu par binôme, avec une règle.
- La fiche de contrôle optique, un exemplaire par élève.
- Une calculatrice par élève.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
