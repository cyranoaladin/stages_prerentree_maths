# Terminale Spécialité Physique-Chimie — Séance 5 — Supports de manipulation
## Électricité, chimie organique, mesure et incertitudes, évaluation

## Support 1 — Le circuit à commenter

Un circuit série, deux résistances. À projeter. Selon le parcours, l'élève installe
$P = U \times I$ ou conduit le bilan de puissance complet.

```{=latex}
\begin{center}
\begin{tikzpicture}[x=11mm,y=11mm,thick]
  \draw[Navy] (0,0) -- (0,2) -- (2,2);
  \draw[Navy] (2,2) -- (2.2,2);
  \draw[Navy,fill=SoftBlue] (2.2,1.72) rectangle (3.8,2.28);
  \node[font=\small] at (3,2) {$R_1$};
  \draw[Navy] (3.8,2) -- (5,2);
  \draw[Navy,fill=SoftBlue] (5,1.72) rectangle (6.6,2.28);
  \node[font=\small] at (5.8,2) {$R_2$};
  \draw[Navy] (6.6,2) -- (8,2) -- (8,0) -- (0,0);
  % générateur
  \draw[Navy,line width=1.6pt] (-0.28,1.15) -- (0.28,1.15);
  \draw[Navy,line width=0.9pt] (-0.16,0.85) -- (0.16,0.85);
  \node[font=\small,left=1mm] at (-0.28,1) {$U$};
  \draw[->,Red,thick] (1,2.45) -- (2,2.45) node[midway,above,font=\small] {$I$};
  \node[font=\small,TextGray,align=center] at (4,-0.55)
       {circuit série : la même intensité $I$ traverse les deux conducteurs};
\end{tikzpicture}
\end{center}
```

**Questions graduées, du parcours d'installation au parcours d'approfondissement.**

1. Quelle est l'intensité qui traverse $R_2$, comparée à celle qui traverse $R_1$ ?
2. Écrire la puissance dissipée dans $R_1$, puis dans $R_2$.
3. Écrire la puissance totale fournie par le générateur.
4. Où part l'énergie dissipée ? Sous quelle forme ?

**Réponses pour le professeur.** (1) La même : le circuit est en série. (2)
$P_1 = R_1 I^2$ et $P_2 = R_2 I^2$. (3) $P = U \times I = (R_1 + R_2) I^2$. (4) Sous forme
thermique, par effet Joule : les conducteurs chauffent.

**Point à faire émerger.** L'intensité est la **même** en amont et en aval de chaque
résistance. L'effet Joule ne consomme pas de courant : il transforme de l'énergie. C'est
la confusion la plus tenace du domaine, et le circuit série la rend visible.

## Support 2 — Cinq formules, trente secondes chacune

À projeter une par une, chronomètre en main. L'élève écrit la famille sans réfléchir : le
but est de vérifier que l'identification est **immédiate**, pas de la réenseigner.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.55}
\begin{tabular}{|c|c|>{\bfseries}l|p{52mm}|}\hline
\rowcolor{SoftBlue}
 & Formule & Famille & Ce que la Terminale en fera \\\hline
1 & \ce{CH3-CH2-OH} & alcool & site donneur de doublet ; oxydation \\\hline
2 & \ce{CH3-CHO} & aldéhyde & site accepteur ; addition nucléophile \\\hline
3 & \ce{CH3-CO-CH3} & cétone & site accepteur ; protection de fonction \\\hline
4 & \ce{CH3-COOH} & acide carboxylique & acide-base ; estérification \\\hline
5 & \ce{CH3-COO-CH3} & ester & hydrolyse ; stratégie de synthèse \\\hline
\end{tabular}
\end{center}
```

**Ce qui compte à la correction.** Pas la note, mais le **délai**. Un groupe identifié en
dix secondes est disponible pour un mécanisme de Terminale ; un groupe identifié en une
minute ne l'est pas.

## Support 3 — Trois résultats à rendre

À distribuer. L'élève corrige la **forme** seulement.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.5}
\begin{tabular}{|c|p{50mm}|p{34mm}|p{40mm}|}\hline
\rowcolor{SoftBlue}
 & Résultat proposé & Ce qui ne va pas & Résultat corrigé \\\hline
1 & La vitesse vaut $3{,}428571429$ & & \\\hline
2 & La longueur d'onde vaut \SI{0.7727272}{\metre} & & \\\hline
3 & L'énergie vaut \SI{240}{\newton} & & \\\hline
\end{tabular}
\end{center}
```

**Réponses pour le professeur.** (1) Pas d'unité, et trop de chiffres :
$\SI{3.4}{\metre\per\second}$. (2) Trop de chiffres significatifs par rapport aux données :
$\SI{0.77}{\metre}$. (3) Unité incohérente — une énergie est en joules, pas en newtons :
$\SI{240}{\joule}$.

**La règle des chiffres significatifs, en une phrase.** Le résultat ne peut pas être plus
précis que la donnée la moins précise qui a servi à le calculer.

## Support 4 — Fiche de contrôle finale

À distribuer, à garder dans le portfolio. C'est la fiche que l'élève emporte en septembre.

> **Les trois gestes du stage, valables dans les cinq domaines.**
>
> 1. **La relation d'abord.** Aucune valeur numérique tant que la relation littérale n'est
>    pas écrite. C'est ce qui permet de relire un calcul, et de trouver l'erreur.
> 2. **L'unité toujours.** Un résultat sans unité n'est pas un résultat. Et une unité
>    incohérente signale une erreur avant même la vérification du calcul.
> 3. **L'ordre de grandeur en dernier.** Avant de conclure, se demander si le résultat est
>    plausible. Quelques repères :
>
> | Grandeur | Ordre de grandeur |
> |---|---|
> | Vitesse d'un piéton | $\SI{1.5}{\metre\per\second}$ |
> | Célérité du son dans l'air | $\SI{340}{\metre\per\second}$ |
> | Longueur d'onde d'un son audible | de quelques $\si{\centi\metre}$ à quelques $\si{\metre}$ |
> | Énergie potentielle gagnée en montant un étage | quelques $\si{\kilo\joule}$ |
> | Énergie cinétique d'une voiture sur autoroute | quelques centaines de $\si{\kilo\joule}$ |
> | pH d'une solution courante | entre 0 et 14 |

## Support 5 — La carte d'entrée et la carte de sortie

À projeter pendant la phase de bilan, après la correction de l'évaluation.

```{=latex}
\begin{center}\small
\renewcommand{\arraystretch}{1.5}
\begin{tabular}{|p{30mm}|p{45mm}|p{45mm}|}\hline
\rowcolor{SoftBlue}
 & \textbf{Réponse juste} & \textbf{Réponse fausse} \\\hline
\textbf{Certitude haute} & \cellcolor{green!8}Acquis --- à entretenir &
   \cellcolor{Red!8}Certitude à revoir --- \textbf{priorité} \\\hline
\textbf{Certitude basse} & \cellcolor{SoftGold}À consolider &
   \cellcolor{SoftGray}À installer \\\hline
\end{tabular}
\end{center}
```

**Ce qu'il faut dire explicitement, et qui n'est pas intuitif.** Passer de la case rouge à
la case grise est un **progrès**, même si la réponse reste fausse. L'élève sait désormais
qu'il ne sait pas : c'est la condition pour apprendre en septembre. Une certitude haute et
fausse, elle, ne se corrige jamais toute seule.

## Matériel à prévoir

- Le circuit du support 1, projeté.
- Les cinq formules du support 2, projetées une par une, avec un chronomètre.
- Les trois résultats du support 3, un exemplaire par élève.
- La fiche de contrôle finale, un exemplaire par élève, à garder.
- L'évaluation finale, un exemplaire par élève.

---
_Source pédagogique unique : `stage_prerentree_terminale_pc.md`._
