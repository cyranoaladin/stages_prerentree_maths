# Terminale Spécialité Physique-Chimie — Séance 1 — Supports de manipulation
## Transformations chimiques : avancement, réactif limitant, oxydo-réduction

Tous les supports sont conçus pour être conduits **sans matériel de laboratoire**, sur
documents. Ils se découpent et se distribuent par binôme.

## Support 1 — Le tableau à compléter (confrontation)

À projeter vierge. L'élève complète la ligne « en cours », puis cherche quelle quantité
s'annule la première.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.7}
\begin{tabular}{|>{\bfseries}l|c|c|c|}\hline
\rowcolor{SoftBlue}
État & \ce{2A} & \ce{B} & \ce{C} \\\hline
Initial & \SI{0.4}{\mole} & \SI{0.3}{\mole} & 0 \\\hline
En cours (avancement $x$) & & & \\\hline
S'annule pour $x =$ & & & --- \\\hline
\end{tabular}
\end{center}
```

**Réponses pour le professeur :** ligne « en cours » : $0{,}4 - 2x$ ; $0{,}3 - x$ ; $x$.
S'annule pour $x = 0{,}2$ et $x = 0{,}3$. Le réactif A s'épuise le premier.

**Point à faire émerger.** La plus petite quantité initiale n'est pas le réactif
limitant. Le coefficient 2 fait que A est consommé deux fois plus vite que B.

## Support 2 — Six systèmes à trier (reconstruction)

Six cartes à découper. Pour chacune, l'élève écrit les deux quotients et entoure le
réactif limitant.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.35}
\begin{tabular}{|c|l|c|c|c|}\hline
\rowcolor{SoftBlue}
Carte & Équation & $n$ du premier & $n$ du second & Limitant \\\hline
1 & \ce{A + B -> C} & \SI{0.5}{\mole} & \SI{0.8}{\mole} & A \\\hline
2 & \ce{2A + B -> C} & \SI{0.4}{\mole} & \SI{0.3}{\mole} & A \\\hline
3 & \ce{A + 3B -> C} & \SI{0.5}{\mole} & \SI{1.2}{\mole} & B \\\hline
4 & \ce{3A + 2B -> D} & \SI{0.6}{\mole} & \SI{0.5}{\mole} & A \\\hline
5 & \ce{2A + 5B -> 2C} & \SI{0.8}{\mole} & \SI{1.5}{\mole} & B \\\hline
6 & \ce{4A + B -> C} & \SI{0.8}{\mole} & \SI{0.2}{\mole} & aucun \\\hline
\end{tabular}
\end{center}
```

La carte 6 est un cas d'égalité : $0{,}8/4 = 0{,}2$ et $0{,}2/1 = 0{,}2$. Les deux
réactifs s'épuisent **en même temps** : aucun n'est limitant, aucun n'est en excès. Ce
cas porte un nom, et il vaut la peine d'être écrit au tableau — les réactifs sont
introduits dans les **proportions stœchiométriques**. Il reviendra en Terminale, dans les
titrages, sous le nom d'équivalence.

## Support 3 — L'échelle de pH à garnir

Une échelle par binôme. L'élève place les valeurs, puis écrit le rapport de
concentrations entre deux d'entre elles.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=10mm,y=8mm]
  \draw[->,thick] (-0.4,0) -- (14.6,0) node[right] {pH};
  \foreach \x in {0,...,14} \draw (\x,0.12) -- (\x,-0.12) node[below,font=\small] {\x};
  \draw[Red,line width=2pt] (0,0.5) -- (7,0.5) node[midway,above,font=\small] {acide};
  \draw[Green,line width=2pt] (7,0.5) -- (14,0.5) node[midway,above,font=\small] {basique};
  \fill[Navy] (7,0) circle (2.2pt) node[above=4mm,font=\small\bfseries] {neutre};
  % Les trois valeurs de l'exercice, marquées sans réécrire la graduation.
  \foreach \x in {3,5,11} \draw[Navy,line width=1.4pt] (\x,0.22) -- (\x,-0.22);
\end{tikzpicture}
\end{center}
```

**Question à poser.** Entre pH 3 et pH 5, de combien la concentration en $\ce{H3O+}$
est-elle multipliée ou divisée ?

**Réponse attendue.** Elle est **cent fois plus grande** à pH 3. Une unité de pH vaut un
facteur dix ; deux unités valent un facteur cent.

## Support 4 — Fiche de contrôle oxydant / réducteur

À distribuer, à garder dans le portfolio.

> **Un couple, deux rôles.** Un couple oxydant/réducteur associe **toujours** une espèce
> qui capte des électrons et l'espèce obtenue après ce gain. Il n'existe pas de couple
> formé de deux oxydants.
>
> | Couple | Oxydant | Réducteur | Demi-équation |
> |---|---|---|---|
> | $\ce{Cu^2+/Cu}$ | $\ce{Cu^2+}$ | $\ce{Cu}$ | $\ce{Cu^2+ + 2e^- <=> Cu}$ |
> | $\ce{Fe^2+/Fe}$ | $\ce{Fe^2+}$ | $\ce{Fe}$ | $\ce{Fe^2+ + 2e^- <=> Fe}$ |
> | $\ce{Ag+/Ag}$ | $\ce{Ag+}$ | $\ce{Ag}$ | $\ce{Ag+ + e^- <=> Ag}$ |
>
> **Contrôle en trois secondes :** l'oxydant est toujours l'espèce la **plus chargée**
> positivement, ou la plus oxygénée. C'est elle qui est écrite à gauche du slash.

## Support 5 — Passerelle vers la Terminale

À projeter en fin de séance.

```{=latex}
\begin{center}
\begin{tikzpicture}[node distance=6mm,font=\small,
  every node/.style={rounded corners=2pt,align=center,inner sep=2.5mm}]
  \node[fill=SoftGold,draw=Gold,thick] (t) {Tableau d'avancement\\\textit{Première}};
  \node[fill=SoftBlue,draw=Navy,right=16mm of t] (tau)
       {Taux d'avancement final\\$\tau = x_f / x_{\max}$};
  \draw[->,thick,Navy] (t) -- (tau);
  \node[below=9mm of tau,fill=SoftGray,draw=TextGray,text width=72mm]
       (l) {Quotient de réaction $Q_r$ et constante $K$\\
            Titrage pH-métrique ou conductimétrique\\
            Évolution spontanée et piles\\
            Cinétique : vitesse volumique, temps de demi-réaction};
  \draw[->,thick,TextGray] (tau) -- (l);
\end{tikzpicture}
\end{center}
```

**Ce qui change en Terminale.** En Première, la transformation est supposée totale :
$x_f = x_{\max}$. En Terminale, $\tau$ peut être inférieur à 1, et le système atteint un
**état d'équilibre**. Le tableau, lui, ne change pas.

## Matériel à prévoir

- Le tableau du support 1, projeté ou photocopié vierge, un par élève.
- Les six cartes du support 2, découpées, un jeu par binôme.
- L'échelle de pH, un exemplaire par binôme.
- La fiche de contrôle oxydant/réducteur, un exemplaire par élève.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
