# Terminale Spécialité Mathématiques — Séance 1 — Supports de manipulation
## Suites numériques

Ces supports sont à préparer avant la séance. Ils servent la phase de confrontation et la
phase de reconstruction.

## Support 1 — Table de valeurs à compléter (confrontation)

À projeter ou distribuer vierge, à compléter collectivement.

| n | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $u_n = 0{,}5^n$ | | | | | |
| $w_n = 1{,}2^n$ | | | | | |
| $t_n = 3 \times 0{,}8^n$ | | | | | |

*Réponses pour le professeur :*
$0{,}5^n$ : 1 ; 0,5 ; 0,25 ; 0,125 ; 0,0625 — décroissante.
$1{,}2^n$ : 1 ; 1,2 ; 1,44 ; 1,728 ; 2,0736 — croissante.
$3 \times 0{,}8^n$ : 3 ; 2,4 ; 1,92 ; 1,536 ; 1,2288 — décroissante.

**Usage.** Faire remplir la première ligne seulement, après que chaque élève a écrit sa
réponse spontanée. Les deux autres lignes servent à établir que le critère est la position
de la raison par rapport à 1, et non son signe.

## Support 2 — Jeu de cartes « quel critère ? » (reconstruction)

Sept cartes à découper. Chaque carte porte une suite ; l'élève doit poser la carte dans
l'une des deux colonnes d'un tapis : **« comparaison de la raison à 1 »** ou **« signe de
$u_{n+1} - u_n$ »**.

| Carte | Suite | Colonne attendue |
|---:|---|---|
| 1 | $v_n = 2 \times 3^n$ | Raison comparée à 1 |
| 2 | $u_0 = 5$, $u_{n+1} = u_n + 3n$ | Signe de la différence |
| 3 | $u_n = 7 - 2n$ | Signe de la différence (ou raison arithmétique) |
| 4 | $v_n = 4 \times 0{,}25^n$ | Raison comparée à 1 |
| 5 | $u_0 = 1$, $u_{n+1} = 0{,}5 u_n + 3$ | Signe de la différence |
| 6 | $v_n = 0{,}9^n$ | Raison comparée à 1 |
| 7 | $u_n = n^2 - 6n$ | Signe de la différence |

**Point à faire émerger.** La comparaison de la raison à 1 n'est utilisable que pour une
suite géométrique dont on connaît la forme explicite. Le signe de la différence, lui,
fonctionne toujours. C'est la méthode à privilégier en cas de doute.

## Support 3 — Bande numérique de la convergence (ouverture Terminale)

Tracer sur une bande graduée de 0 à 4 les termes de la suite $u_n = 3 - 1/(n+1)$ :

```{=latex}
\begin{center}
\begin{tikzpicture}[x=28mm,y=10mm]
  \draw[->,thick] (0,0) -- (4.35,0);
  \foreach \x in {0,1,2,3,4} \draw (\x,0.14) -- (\x,-0.14) node[below] {$\x$};
  \draw[dashed,Red,thick] (3,-0.55) -- (3,1.3)
        node[above,align=center,font=\small] {plafond $3$\\jamais atteint};
  \foreach \x/\lab in {1/{u_0}, 2/{u_1}, 2.5/{u_2}, 2.667/{u_3}, 2.75/{u_4}}
     \fill[Navy] (\x,0) circle (1.5pt) node[above=1.5mm,font=\small] {$\lab$};
  \draw[->,Green,thick] (1,-0.8) -- (2.85,-0.8)
        node[midway,below,font=\small] {les termes avancent toujours vers la droite};
\end{tikzpicture}
\end{center}
```

Faire placer les points par les élèves, un par un. Faire constater à voix haute : les
points avancent toujours vers la droite (croissance) et ne franchissent jamais le repère 3
(majoration). Écrire au tableau : **croissante + majorée $\implies$ converge**.

## Support 4 — Affiche de séance

À afficher pendant toute la séance :

> **Pour trouver le sens de variation d'une suite :**
> 1. J'écris $u_{n+1}$ et $u_n$.
> 2. Je calcule $u_{n+1} - u_n$.
> 3. J'étudie le signe de cette différence.
> 4. Je conclus — et seulement là.
>
> **Raccourci, pour une suite géométrique de premier terme positif :**
> je compare la raison **à 1**.

## Matériel à prévoir

- Une bande numérique par binôme (ou une bande projetée).
- Un jeu de sept cartes par binôme, découpées à l'avance.
- Les livrets individuels des élèves.
- Une calculatrice par élève, utilisée uniquement en contrôle.
