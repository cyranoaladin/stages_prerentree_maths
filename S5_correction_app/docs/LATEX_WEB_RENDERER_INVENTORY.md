# Inventaire du rendu web des structures LaTeX

Relevé sur les **quinze manifestes d'évaluation**, dans les champs réellement
affichés par l'application : énoncé, réponse attendue, étapes significatives et
description de critère.

La règle du périmètre est stricte : **on n'implémente rien qui ne figure pas ici**.
Un support développé pour une construction absente du corpus est du code non testé
par les données réelles, donc du code qui se dégradera sans qu'on le sache.

## Environnements

| environnement | occurrences | niveaux concernés | élèves | champs | support actuel | action |
| --- | ---: | --- | ---: | --- | --- | --- |
| `enumerate` | 90 | 1re NSI, 1re spé maths, Quatrième, Seconde, Troisième | 14 | statement | converti en `<ol>` / `<li>` | aucune — en service |
| `lstlisting` | 9 | 1re NSI | 2 | statement | converti en `<pre><code>` | aucune — livré dans cette passe |
| `tabularx` | 2 | 1re NSI | 2 | statement | converti en `<table>`, repli si la forme s'écarte | aucune — livré dans cette passe |

Environnements recherchés et **absents du corpus**, donc non implémentés :
`itemize`, `verbatim`, `tabular`, `array`, `center`, `minipage`, `figure`, `align`.

## Macros en ligne

| macro | occurrences | niveaux | rendu |
| --- | ---: | --- | --- |
| `\item` | 230 | 1re NSI, 1re spé maths, Quatrième, Seconde, Troisième | élément de liste |
| `\code` | 183 | 1re NSI | `<code>` |
| `\textbf` | 16 | 1re NSI, 1re spé maths, Quatrième, Seconde, Troisième | `<strong>` |
| `\hline` | 8 | 1re NSI | filet de tableau |
| `\emph` | 6 | 1re NSI, 1re spé maths, Troisième | `<em>` |
| `\par` | 2 | 1re NSI | séparation de paragraphe |
| `\noindent` | 2 | 1re NSI | retiré |

## Décisions

**`lstlisting` → bloc de code.** L'indentation et les retours à la ligne sont
conservés : en Python, ils portent le sens. Le contenu est verbatim — une commande
LaTeX ou un `$` à l'intérieur restent du texte — puis échappé. Aucune coloration
syntaxique : elle exigerait une dépendance externe, et l'application doit
fonctionner sans réseau. KaTeX ignore `<pre>` et `<code>` par défaut, donc un `$`
dans du code n'est jamais interprété comme une formule.

**`[language={}]` → aucune classe de langage.** Cette forme désigne, dans le
corpus, un extrait de fichier CSV et non du code.

**`tabularx` → tableau, ou renvoi au PDF.** Le corpus n'en contient qu'une forme :
une ligne d'en-tête, puis des lignes dont la première cellule est en gras. Elle est
convertie. Toute forme qui s'en écarte — nombre de cellules irrégulier, commande
inconnue dans une cellule — bascule sur un renvoi au PDF distribué plutôt que de
produire une grille approximative. La priorité est de corriger juste, pas de
reproduire une mise en page ; et le sujet reste affiché en vis-à-vis.

**Aucune structure inconnue n'atteint l'écran.** Un `\begin{...}` non traité est
remplacé par le renvoi au PDF ; un délimiteur orphelin est retiré. C'est vérifié
sur les quinze pages par un test de balayage.

## Contrôle

Le balayage des quinze pages de correction ne trouve **aucune** des séquences
`\begin{`, `\end{`, `\item`, `\code{`, `\textbf{`, `\emph{`, `\hline`.
