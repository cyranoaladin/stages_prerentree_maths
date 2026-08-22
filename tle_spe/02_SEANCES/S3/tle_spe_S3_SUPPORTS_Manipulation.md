# Terminale Spécialité Mathématiques — Séance 3 — Supports de manipulation
## Second degré et signe du trinôme

## Support 1 — Test de valeurs (confrontation)

À projeter vierge. Le trinôme est $- x^2 + 3x - 2$, dont les racines sont 1 et 2.

| x | $- 2$ | 0 | 1 | 1,5 | 2 | 4 |
|---|---|---|---|---|---|---|
| $- x^2 + 3x - 2$ | | | | | | |
| signe | | | | | | |

*Réponses pour le professeur :* $- 12 ; - 2 ; 0 ; 0{,}25 ; 0 ; - 6$.
Signes : $- ; - ; 0 ; + ; 0 ; -$.

**Point à faire émerger.** Le trinôme est positif **entre** les racines et négatif à
l'extérieur : c'est l'inverse du réflexe habituel, parce que $a = - 1$ est négatif.

## Support 2 — Tableaux de signes à trier (reconstruction)

Six trinômes à découper et à associer à l'un des trois tableaux de signes types.

| Trinôme | a | $\Delta$ | Tableau attendu |
|---|---:|---|---|
| $x^2 - 4$ | +1 | > 0 | + $0 - 0 +$ |
| $- x^2 + 3x - 2$ | $- 1$ | > 0 | $- 0 + 0 -$ |
| $2x^2 + x + 3$ | +2 | < 0 | + partout |
| $- 3x^2 + x - 5$ | $- 3$ | < 0 | $-$ partout |
| $x^2 - 6x + 9$ | +1 | = 0 | + 0 + |
| $- 2x^2 + 8x - 6$ | $- 2$ | > 0 | $- 0 + 0 -$ |

**Trois tableaux types à afficher :**

```{=latex}
\begin{center}\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{@{}c@{\hspace{6mm}}c@{\hspace{6mm}}c@{}}
\textbf{Type 1} --- $\Delta>0$, $a>0$ &
\textbf{Type 2} --- $\Delta>0$, $a<0$ &
\textbf{Type 3} --- $\Delta<0$ \\[1.5mm]
\begin{tabular}{|c|c|c|c|c|}\hline
$x$ & $-\infty$ & $x_1$ & $x_2$ & $+\infty$ \\\hline
signe & $+$ & $0\ \ -$ & $0$ & $+$ \\\hline
\end{tabular} &
\begin{tabular}{|c|c|c|c|c|}\hline
$x$ & $-\infty$ & $x_1$ & $x_2$ & $+\infty$ \\\hline
signe & $-$ & $0\ \ +$ & $0$ & $-$ \\\hline
\end{tabular} &
\begin{tabular}{|c|c|c|}\hline
$x$ & $-\infty$ & $+\infty$ \\\hline
signe & \multicolumn{2}{c|}{signe de $a$} \\\hline
\end{tabular}
\end{tabular}
\end{center}
```

Le tableau du cas $\Delta = 0$ (signe de a partout, avec un zéro isolé) est traité à part.

## Support 3 — Droite graduée pour l'ensemble solution

Une droite graduée par binôme, avec des jetons de deux couleurs. L'élève place les racines,
colorie les zones où le trinôme est positif, puis **écrit** l'ensemble solution.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=15mm,y=8mm]
  \draw[->,thick] (-5.2,0) -- (5.2,0) node[right] {$x$};
  \foreach \x in {-5,...,5} \draw (\x,0.12) -- (\x,-0.12);
  \foreach \x/\l in {-4/{-4},-3/{-3},3/{3},4/{4}}
      \fill[Navy] (\x,0) circle (2pt) node[below=2mm,font=\small] {$\l$};
  \draw[Green,line width=1.6pt] (-5.2,0.36) -- (-3,0.36);
  \draw[Green,line width=1.6pt] (3,0.36) -- (5.2,0.36);
  \node[Green,font=\small,above] at (-4.1,0.42) {trinôme $\geqslant 0$};
  \node[Green,font=\small,above] at (4.1,0.42) {trinôme $\geqslant 0$};
\end{tikzpicture}
\end{center}
```

**Point à faire travailler.** Le passage du dessin à l'écriture : $] - \infty ; - 3] \cup [3 ; + \infty [$.
Faire vérifier crochet par crochet : inégalité large $\implies$ crochet fermé ; borne infinie $\implies$
crochet toujours ouvert.

## Support 4 — Fiche de contrôle somme et produit

À distribuer, à garder dans le portfolio.

> Après avoir trouvé les racines $x_1$ et $x_2$ de $ax^2 + bx + c$ :
>
> | Contrôle | Valeur attendue |
> |---|---|
> | $x_1 + x_2$ | $- b/a$ |
> | $x_1 \times x_2$ | c/a |
>
> Exemple : $x^2 - 7x + 12$, racines 3 et 4. Somme $7 = - ( - 7)/1 \checkmark$. Produit $12 = 12/1 \checkmark$.

## Support 5 — Passerelle vers la séance 4

À projeter en fin de séance.

```{=latex}
\begin{center}
$\displaystyle f(x) = x^{3} - 3x^{2} + 1
 \qquad\text{d'où}\qquad
 f'(x) = 3x^{2} - 6x = 3x\,(x-2)$
\end{center}
\begin{center}\small\color{Blue}
la dérivée d'une fonction du troisième degré est un trinôme : le tableau de signes
de la séance 3 sert directement à lire les variations
\end{center}
```

| | $- \infty$ | | 0 | | 2 | | +$\infty$ |
|---|---|---|---|---|---|---|---|
| signe de $f'(x)$ | | + | 0 | $-$ | 0 | + | |
| variations de f | | $\nearrow$ | | $\searrow$ | | $\nearrow$ | |

Faire remplir la ligne « signe de f' » par les élèves, avec la méthode de la séance. La
ligne « variations de f » est donnée : elle sera justifiée en séance 4.

## Matériel à prévoir

- Un jeu de six trinômes et trois tableaux types par binôme.
- Une droite graduée et des jetons par binôme.
- La fiche de contrôle somme/produit, un exemplaire par élève.
