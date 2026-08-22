# Terminale Spécialité Physique-Chimie — Séance 3 — Supports de manipulation
## Énergie : travail, énergies cinétique et potentielle, énergie mécanique

## Support 1 — Cinq situations, cinq angles (confrontation)

À projeter une par une. Pour chacune, l'élève trace l'angle entre la force et le
déplacement, **puis** dit si le travail est moteur, nul ou résistant. Il ne calcule rien.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.45}
\begin{tabular}{|c|p{62mm}|c|c|c|}\hline
\rowcolor{SoftBlue}
 & Situation & Force étudiée & $\alpha$ & Travail \\\hline
1 & Valise tirée sur un sol horizontal & poids & $90°$ & nul \\\hline
2 & Valise tirée sur un sol horizontal & traction horizontale & $0°$ & moteur \\\hline
3 & Bille en chute libre & poids & $0°$ & moteur \\\hline
4 & Bille lancée vers le haut & poids & $180°$ & résistant \\\hline
5 & Satellite en orbite circulaire & gravitation & $90°$ & nul \\\hline
\end{tabular}
\end{center}
```

**Point à faire émerger.** Les lignes 1 et 5 portent la même conclusion pour des raisons
identiques, sur des échelles sans rapport : le poids d'une valise et la gravitation d'un
satellite ne travaillent pas, parce qu'ils sont perpendiculaires au déplacement. Ce n'est
pas la force qui décide, c'est l'**angle**.

## Support 2 — Le cercle des angles

À distribuer, un par binôme. L'élève place les cinq situations du support 1 sur le
cercle, selon l'angle entre force et déplacement.

```{=latex}
\begin{center}
\begin{tikzpicture}[scale=1.6]
  \draw[TextGray,thin] (0,0) circle (1.5);
  \draw[->,very thick,Navy] (0,0) -- (1.5,0)
       node[right,font=\small\bfseries] {déplacement $\vv{AB}$};
  \foreach \a/\lab/\col in {0/{$0°$ moteur maximal}/Green,
                            45/{$45°$ moteur}/Green,
                            90/{$90°$ \textbf{nul}}/Navy,
                            135/{$135°$ résistant}/Red,
                            180/{$180°$ résistant maximal}/Red}
     {\draw[->,thick,\col] (0,0) -- (\a:1.5);
      \node[\col,font=\scriptsize,anchor=west] at (\a:1.62) {\lab};}
  \draw[Gold,line width=1.2pt] (0.42,0) arc (0:90:0.42);
  \node[Gold,font=\scriptsize] at (45:0.62) {$\alpha$};
\end{tikzpicture}
\end{center}
```

**Ce qui doit être dit à voix haute.** À gauche de la verticale, le travail est négatif :
la force freine. Sur la verticale exactement, il est nul. Le signe du travail est le
signe du cosinus, rien d'autre.

## Support 3 — Deux expressions à ne pas confondre

À distribuer, à garder dans le portfolio.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.6}
\begin{tabular}{|>{\bfseries}p{34mm}|c|p{34mm}|p{34mm}|}\hline
\rowcolor{SoftBlue}
Grandeur & Expression & Dépend de & Ne dépend pas de \\\hline
Énergie cinétique & $E_c = \dfrac{1}{2}mv^{2}$ & la masse, la vitesse & l'altitude \\\hline
Énergie potentielle de pesanteur & $E_{pp} = mgz$ & la masse, l'altitude & la vitesse \\\hline
\end{tabular}
\end{center}
```

> **Deux contrôles de trois secondes.**
>
> - Un objet **immobile** en haut d'une étagère : $E_c = 0$, mais $E_{pp} \neq 0$. Si ton
>   expression donne une énergie cinétique non nulle pour un objet immobile, elle est
>   fausse.
> - Un objet qui roule **au sol** : $E_{pp} = 0$ si l'on prend le sol comme référence,
>   mais $E_c \neq 0$.
>
> Ces deux cas séparent les deux expressions mieux qu'une règle mnémotechnique.

**Le rôle du carré.** Faire calculer $E_c$ pour $v$, puis pour $2v$ : l'énergie est
multipliée par **quatre**, pas par deux. C'est ce qui explique qu'une distance de freinage
soit multipliée par quatre quand la vitesse double.

## Support 4 — La pente sans frottement

Le support de l'exercice 5. À distribuer avec la question, pas avant.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=9mm,y=9mm]
  \fill[SoftGray] (0,0) -- (11,0) -- (11,0.25) -- (0,0.25) -- cycle;
  \draw[Navy,very thick] (0.6,5.4) .. controls (4,5.2) and (5,0.6) .. (10.4,0.28);
  \draw[TextGray,dashed] (0.6,5.4) -- (0.6,0.25);
  \draw[<->,TextGray] (0.25,0.25) -- (0.25,5.4)
       node[midway,left,font=\small] {\SI{12}{\metre}};
  \fill[Red] (0.6,5.4) circle (2.4pt) node[above right,font=\small] {départ, $v = 0$};
  \fill[Red] (10.4,0.28) circle (2.4pt) node[above left=1mm,font=\small] {arrivée, $v = ?$};
  \node[font=\small,Green,align=center] at (5.8,3.2)
       {sans frottement :\\$E_m$ se conserve};
\end{tikzpicture}
\end{center}
```

**Conduite.** Faire écrire la conservation **avant** tout calcul :

$$E_c(\text{départ}) + E_{pp}(\text{départ}) = E_c(\text{arrivée}) + E_{pp}(\text{arrivée})$$

Puis faire remarquer que la masse se simplifie : la vitesse en bas ne dépend pas de la
masse de la luge. C'est un résultat qui surprend, et qui mérite d'être commenté.

## Support 5 — Passerelle vers la Terminale

À projeter en fin de séance.

```{=latex}
\begin{center}
\begin{tikzpicture}[node distance=5mm,font=\small,
  every node/.style={rounded corners=2pt,align=center,inner sep=2.5mm,text width=46mm}]
  \node[fill=SoftGold,draw=Gold,thick] (a) {$E_m = E_c + E_{pp}$\\\textit{bilan de Première}};
  % 32 mm entre les deux encadrés : le libellé de la flèche tient sur deux lignes et
  % ne mord plus sur les boîtes, comme c'était le cas avec un écart de 14 mm.
  \node[fill=SoftBlue,draw=Navy,thick,right=32mm of a] (b)
       {$\Delta U = W + Q$\\\textit{premier principe, Terminale}};
  \draw[->,very thick,Navy] (a) -- (b);
  \node[font=\scriptsize,above=2mm,text width=30mm,align=center]
       at ($(a)!0.5!(b)$) {on ajoute\\l'énergie interne};
  \node[below=8mm of b,fill=SoftGray,draw=TextGray,text width=58mm]
       (c) {Flux thermique\\Résistance thermique\\Loi de refroidissement de Newton};
  \draw[->,thick,TextGray] (b) -- (c);
\end{tikzpicture}
\end{center}
```

**La question qui ouvre.** « Une voiture freine et s'arrête. Son énergie cinétique valait
$\SI{200}{\kilo\joule}$. Où est-elle passée ? » Les freins ont chauffé : cette énergie est
devenue de l'énergie interne. Le premier principe est exactement la comptabilité qui en
rend compte.

## Matériel à prévoir

- Le tableau du support 1, projeté, une ligne à la fois.
- Le cercle des angles, un exemplaire par binôme.
- La fiche des deux expressions, un exemplaire par élève.
- Le schéma de la pente, distribué avec l'exercice 5 seulement.
- Une calculatrice par élève.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
