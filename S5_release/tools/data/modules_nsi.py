# -*- coding: utf-8 -*-
"""Modules de consolidation ciblée (phases 2 et 3 de la séance S5) — NSI.

Même structure que ``modules_maths`` : rappel, exemple guidé, six exercices gradués,
erreurs probables et critère de réussite observable.
Les exercices se traitent sur papier, l'ordinateur n'intervenant qu'en contrôle.
"""

MODULES = {
    "NSI1_FONC_01": {
        "titre": "Paramètre, argument, valeur renvoyée et None",
        "pourquoi": "Le dossier individuel place la compétence « Fonctions » au niveau 1 en début de stage et documente la conception « un paramètre n'est pas la valeur renvoyée » ; sans return, aucune composition de fonctions n'est possible.",
        "rappel": r"""\begin{methodbox}
\textbf{Quatre mots à ne jamais confondre.}
Le \textbf{paramètre} est le nom écrit dans la définition. L'\textbf{argument} est la valeur fournie à l'appel.
\code{return} \textbf{renvoie} une valeur à celui qui a appelé ; \code{print} se contente d'\textbf{afficher}
à l'écran. Une fonction sans \code{return} renvoie \code{None}.
\textbf{Contrôle :} si le résultat d'un appel est rangé dans une variable, cette variable doit contenir autre chose que \code{None}.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.}
\begin{lstlisting}
def double(n):
    return 2 * n

r = double(5)
\end{lstlisting}
\begin{enumerate}
\item Le paramètre est \code{n}, l'argument est \code{5}, la valeur renvoyée est \code{10}.
\item \code{r} vaut donc \code{10} et peut servir à un autre calcul.
\item Si l'on remplace \code{return 2 * n} par \code{print(2 * n)}, l'écran affiche bien \code{10}, mais \code{r} vaut \code{None}.
\end{enumerate}""",
        "exos": [
            {"tex": r"Écrire une fonction \code{triple(n)} qui \emph{renvoie} le triple de \code{n}, puis un appel qui range le résultat dans une variable \code{t}.", "space": "lines:4",
             "corrige": r"\code{def triple(n): return 3 * n} puis \code{t = triple(7)}."},
            {"tex": r"Dans \code{def aire(b, h): return b * h / 2}, nommer le paramètre, l'argument et la valeur renvoyée pour l'appel \code{aire(6, 4)}.", "space": "lines:3",
             "corrige": r"Paramètres : \code{b} et \code{h} ; arguments : \code{6} et \code{4} ; valeur renvoyée : \code{12.0}."},
            {"tex": r"Corriger \code{def somme(a, b): print(a + b)} pour que \code{s = somme(2, 3)} donne bien \code{5}.", "space": "lines:3",
             "corrige": r"Remplacer \code{print(a + b)} par \code{return a + b}."},
            {"tex": r"Que vaut \code{x} après \code{x = print(\"bonjour\")} ? Expliquer en une phrase.", "space": "lines:2",
             "corrige": r"\code{x} vaut \code{None} : \code{print} affiche mais ne renvoie rien."},
            {"tex": r"Écrire une fonction \code{est_negatif(n)} qui renvoie \code{True} ou \code{False}, puis deux assertions qui la testent.", "space": "lines:5",
             "corrige": r"\code{def est_negatif(n): return n < 0} ; \code{assert est_negatif(-3)} et \code{assert not est_negatif(5)}."},
            {"tex": r"Un élève écrit \code{def carre(n): n * n}. Expliquer précisément ce que renvoie \code{carre(4)}, puis corriger.", "space": "lines:3",
             "corrige": r"Le calcul est effectué puis jeté : la fonction renvoie \code{None}. Il faut écrire \code{return n * n}."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "print confondu avec return"},
                    {"code": "ALGORITHME", "desc": "valeur calculée mais non renvoyée"},
                    {"code": "SYNTAXE", "desc": "indentation du return hors du corps de la fonction"}],
        "reussite": "trois fonctions écrites en autonomie qui renvoient effectivement une valeur exploitable par un appel.",
    },
    "NSI1_BOUCLE_01": {
        "titre": "range, bornes et nombre d'itérations",
        "pourquoi": "Compétence « Boucles » au niveau 1 au diagnostic, avec la conception « range(3) produit trois valeurs » à stabiliser ; toute erreur de borne fausse silencieusement un traitement de données.",
        "rappel": r"""\begin{methodbox}
\textbf{La borne de fin est toujours exclue.}
\code{range(n)} produit $0, 1, \ldots, n-1$ : $n$ valeurs.
\code{range(a, b)} produit $a, a+1, \ldots, b-1$.
\code{range(a, b, p)} avance de $p$ en $p$ en s'arrêtant avant $b$.
\textbf{Contrôle :} écrire les valeurs produites \emph{avant} d'écrire la boucle.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Que produit \code{range(1, 10, 3)} ?
\begin{enumerate}
\item Départ à $1$, pas de $3$ : $1$, puis $4$, puis $7$.
\item Valeur suivante : $10$, mais la borne $10$ est exclue : on s'arrête.
\item Valeurs produites : $1, 4, 7$ — soit \textbf{trois} tours de boucle.
\end{enumerate}""",
        "exos": [
            {"tex": r"Donner les valeurs produites par \code{range(5)}, \code{range(2, 6)} et \code{range(0, 10, 5)}.", "space": "lines:3",
             "corrige": r"\code{0,1,2,3,4} ; \code{2,3,4,5} ; \code{0,5}."},
            {"tex": r"Combien de tours pour \code{for i in range(4, 20, 5)} ? Donner les valeurs prises par \code{i}.", "space": "lines:2",
             "corrige": r"\code{4, 9, 14, 19} : quatre tours."},
            {"tex": r"Compléter \code{for i in range(____):} pour parcourir les entiers de $1$ à $6$ inclus.", "space": "lines:2",
             "corrige": r"\code{range(1, 7)} : la borne $7$ est exclue, donc $6$ est bien la dernière valeur."},
            {"tex": r"Écrire la boucle qui calcule la somme des entiers de $1$ à $6$, puis compléter le tableau d'état après chaque tour.", "space": "lines:5",
             "corrige": r"\code{total = 0} puis \code{for i in range(1, 7): total = total + i}. États : $1, 3, 6, 10, 15, 21$. Résultat \textbf{21}."},
            {"tex": r"Un élève écrit \code{for i in range(1, 5)} pour parcourir les entiers de $1$ à $5$. Corriger et expliquer l'erreur.", "space": "lines:3",
             "corrige": r"Il manque la valeur $5$ : il faut \code{range(1, 6)}. La borne de fin est exclue."},
            {"tex": r"Pour \code{L = [3, 8, 5]}, écrire une boucle qui affiche l'indice \emph{et} la valeur sans provoquer d'erreur d'indice.", "space": "lines:4",
             "corrige": r"\code{for i in range(len(L)): print(i, L[i])} : \code{len(L)} vaut $3$ et la borne étant exclue, le dernier indice utilisé est $2$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "borne de fin comptée comme atteinte"},
                    {"code": "CONCEPT", "desc": "pas de la boucle confondu avec le nombre de tours"},
                    {"code": "ALGORITHME", "desc": "accès à l'indice len(L) provoquant une erreur"}],
        "reussite": "quatre boucles dont les bornes sont exactes du premier coup, les valeurs produites étant écrites avant exécution.",
    },
    "NSI1_ACC_01": {
        "titre": "Accumulateurs : somme, compteur, invariant et variant",
        "pourquoi": "Erreur documentée et persistante dans les deux bilans de positionnement : la somme d'une suite de valeurs est confondue avec le nombre d'itérations. La compétence conditionne tout traitement de données.",
        "rappel": r"""\begin{methodbox}
\textbf{Deux variables, deux rôles distincts.} Un \textbf{accumulateur} de somme cumule des valeurs ;
un \textbf{compteur} compte des tours, indépendamment du contenu. Tous deux s'initialisent
\textbf{avant} la boucle, jamais à l'intérieur.
\par\smallskip
\textbf{Invariant :} propriété vraie avant et après chaque tour, par exemple « \code{total} contient la somme
des valeurs déjà parcourues ». \textbf{Variant :} quantité entière positive qui décroît et garantit l'arrêt.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Somme des valeurs de \code{range(1, 4)}.
\begin{lstlisting}
total = 0
for i in range(1, 4):
    total = total + i
\end{lstlisting}
\begin{enumerate}
\item Les valeurs parcourues sont $1$, $2$, $3$ : trois tours.
\item États successifs de \code{total} : $1$, puis $3$, puis $6$.
\item Le résultat est $6$, et non $3$ : $3$ est le \emph{nombre} de tours, pas la somme.
\item Invariant : après $k$ tours, \code{total} contient la somme des $k$ premières valeurs.
\end{enumerate}""",
        "exos": [
            {"tex": r"Tracer l'exécution de \code{total = 0} puis \code{for i in range(1, 6): total = total + i}, en écrivant l'état après chaque tour, puis donner le résultat.", "space": "lines:4",
             "corrige": r"États : $1, 3, 6, 10, 15$. Résultat : \textbf{15}."},
            {"tex": r"Écrire une fonction \code{bilan(L)} qui renvoie la somme des éléments de \code{L} \emph{et} le nombre de valeurs strictement négatives.", "space": "lines:6",
             "corrige": r"Deux accumulateurs initialisés avant la boucle : \code{total = 0} et \code{n = 0} ; dans la boucle, \code{total = total + v} et \code{if v < 0: n = n + 1} ; puis \code{return total, n}."},
            {"tex": r"Énoncer l'invariant de la boucle de l'exercice 1, puis indiquer ce qui joue le rôle de variant.", "space": "lines:3",
             "corrige": r"Invariant : après $k$ tours, \code{total} contient la somme des $k$ premiers entiers parcourus. Variant : le nombre de valeurs restant à parcourir, qui décroît d'une unité par tour."},
            {"tex": r"Trouver l'erreur et corriger : \code{for v in L:} suivi de \code{total = 0} puis \code{total = total + v}.", "space": "lines:3",
             "corrige": r"L'accumulateur est réinitialisé à chaque tour : à la fin, \code{total} ne contient que la dernière valeur. Il faut placer \code{total = 0} \emph{avant} la boucle."},
            {"tex": r"Écrire une boucle qui calcule le maximum d'une liste non vide, et justifier l'initialisation choisie.", "space": "lines:5",
             "corrige": r"\code{m = L[0]} puis \code{for v in L: if v > m: m = v}. Initialiser à \code{0} serait faux pour une liste de valeurs toutes négatives."},
            {"tex": r"Un élève annonce que la somme des valeurs de \code{range(1, 4)} vaut $3$. Expliquer précisément la confusion, puis donner la valeur exacte.", "space": "lines:3",
             "corrige": r"Il a donné le \emph{nombre d'itérations} et non la somme accumulée. La somme vaut $1+2+3=\textbf{6}$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "somme confondue avec le nombre d'itérations"},
                    {"code": "ALGORITHME", "desc": "accumulateur initialisé à l'intérieur de la boucle"},
                    {"code": "ALGORITHME", "desc": "initialisation à 0 d'un maximum sur des valeurs négatives"}],
        "reussite": "deux accumulateurs corrects écrits en autonomie, avec un invariant énoncé et un tableau d'état exact.",
    },
    "NSI1_TEST_01": {
        "titre": "Tests, assertions et cas limites",
        "pourquoi": "Compétence « Tests » au niveau 1 au diagnostic, la plus basse du profil malgré des connaissances théoriques étendues ; c'est le levier principal de fiabilité pour un parcours en autonomie.",
        "rappel": r"""\begin{methodbox}
\textbf{Un test, c'est une entrée et un résultat attendu, écrits avant l'exécution.}
Une \textbf{assertion} vérifie ce couple : \code{assert f(4) == 16}.
\par\smallskip
\textbf{Cas limites à examiner systématiquement :} structure vide, un seul élément, valeur absente,
première et dernière position, valeur nulle ou négative.
\textbf{Règle :} un test qui échoue n'est pas effacé ; il localise le premier écart.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Tester \code{moyenne(L)} qui renvoie la moyenne d'une liste de nombres.
\begin{enumerate}
\item Cas ordinaire : \code{moyenne([4, 6])} doit valoir \code{5.0}.
\item Cas d'un seul élément : \code{moyenne([7])} doit valoir \code{7.0}.
\item Cas limite : \code{moyenne([])} — la division par zéro doit être traitée explicitement.
\item Écrire les assertions correspondantes avant de lancer le programme.
\end{enumerate}""",
        "exos": [
            {"tex": r"Pour une fonction \code{maximum(L)}, écrire quatre tests avec leur résultat attendu, dont deux cas limites.", "space": "lines:6",
             "corrige": r"Par exemple \code{maximum([3, 9, 2]) == 9} ; \code{maximum([5]) == 5} ; \code{maximum([-4, -1]) == -1} ; \code{maximum([])} doit lever une erreur ou renvoyer \code{None} selon le contrat annoncé."},
            {"tex": r"Écrire en Python les assertions correspondant aux trois premiers tests de l'exercice précédent.", "space": "lines:4",
             "corrige": r"\code{assert maximum([3, 9, 2]) == 9} ; \code{assert maximum([5]) == 5} ; \code{assert maximum([-4, -1]) == -1}."},
            {"tex": r"L'assertion \code{assert 0.1 + 0.2 == 0.3} échoue. Expliquer pourquoi, puis proposer une écriture correcte.", "space": "lines:4",
             "corrige": r"Les nombres flottants sont représentés de façon approchée en binaire : $0{,}1+0{,}2$ vaut $0{,}30000000000000004$. Écriture correcte : \code{math.isclose(0.1 + 0.2, 0.3)}."},
            {"tex": r"Spécifier la fonction \code{indice_de(L, cible)} : entrées, sortie attendue, comportement lorsque la cible est absente.", "space": "lines:5",
             "corrige": r"Entrées : une liste \code{L} et une valeur \code{cible}. Sortie : l'indice de la première occurrence. Absence : renvoie $-1$, valeur qui ne peut être confondue avec un indice valide."},
            {"tex": r"Un test échoue. Décrire une démarche en trois étapes pour localiser précisément l'écart.", "space": "lines:4",
             "corrige": r"1. Relire le résultat attendu et vérifier qu'il est juste. 2. Afficher l'état des variables juste avant l'instruction suspecte. 3. Réduire l'entrée au plus petit cas qui échoue encore."},
            {"tex": r"Écrire un test qui distingue une fonction qui \emph{renvoie} un résultat d'une fonction qui se contente de l'\emph{afficher}.", "space": "lines:3",
             "corrige": r"\code{assert f(2) is not None} : une fonction qui se contente d'afficher renvoie \code{None} et fait échouer l'assertion."},
        ],
        "erreurs": [{"code": "TRANSFERT", "desc": "aucun cas limite envisagé"},
                    {"code": "METHODE", "desc": "résultat attendu écrit après avoir lu la sortie du programme"},
                    {"code": "CONCEPT", "desc": "égalité stricte utilisée sur des flottants"}],
        "reussite": "un jeu de tests couvrant au moins un cas ordinaire et deux cas limites, écrit avant toute exécution.",
    },
}
