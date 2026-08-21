# -*- coding: utf-8 -*-
"""Modules de consolidation ciblée (phases 2 et 3 de la séance S5) — mathématiques.

Un module est indexé par un skill_id. Il fournit :
  - rappel      : le minimum théorique, jamais un cours magistral ;
  - exemple     : un exemple guidé, utilisé en phase 2 uniquement (25 min) ;
  - exos        : six exercices gradués ; la phase 2 les utilise tous,
                  la phase 3 (20 min, second axe) n'utilise que les quatre premiers ;
  - erreurs     : erreurs probables, avec le code de la nomenclature ;
  - reussite    : critère observable de fin de phase.

Aucun exercice ne reprend à l'identique un exercice déjà donné en S1-S4 ou dans le
plan de remédiation individuel : les items 6 sont volontairement construits comme des
*analyses d'erreur* portant sur la conception documentée de l'élève, ce qui est un
format nouveau et non une répétition.
"""

MODULES = {
    # ================================================================= 4e
    "M4E_REL_01": {
        "titre": "Somme, différence et soustraction d'un nombre négatif",
        "pourquoi": "Erreur documentée au diagnostic initial sur la soustraction d'un négatif ; compétence critique pour aborder le produit de relatifs en Quatrième.",
        "rappel": r"""\begin{methodbox}
\textbf{Une seule règle.} Soustraire un nombre, c'est ajouter son opposé : $a - (-b) = a + b$.
Sur la droite graduée, soustraire un nombre négatif revient à se déplacer vers la \textbf{droite}.
\textbf{Contrôle :} un résultat doit toujours pouvoir être situé approximativement sur la droite graduée.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Calculer $6 - (-9) + (-4)$.
\begin{enumerate}
\item Réécrire chaque soustraction en addition : $6 + 9 + (-4)$.
\item Calculer de gauche à droite : $15 + (-4) = 11$.
\item Contrôler : on part de $6$, on avance de $9$ (donc au-delà de $10$), puis on recule de $4$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Calculer $8 - (-3)$.", "space": "short", "corrige": r"$8+3=\mathbf{11}$."},
            {"tex": r"Calculer $-6 + (-5) - (-9)$.", "space": "short", "corrige": r"$-6-5+9=\mathbf{-2}$."},
            {"tex": r"Calculer $12 - (-4) - 7$.", "space": "short", "corrige": r"$12+4-7=\mathbf{9}$."},
            {"tex": r"Un point d'abscisse $-11$ se déplace de $15$ unités vers la droite. Donner son abscisse finale.", "space": "short",
             "corrige": r"$-11+15=\mathbf{4}$."},
            {"tex": r"Compléter : $-7 - (\ldots) = -2$, puis expliquer la démarche.", "space": "lines:2",
             "corrige": r"$-7-(-5)=-7+5=-2$ : le nombre manquant est $\mathbf{-5}$."},
            {"tex": r"Un élève écrit $9 - (-6) = 3$. Nommer précisément son erreur, donner le résultat exact et proposer un contrôle.", "space": "lines:3",
             "corrige": r"Il a traité $-(-6)$ comme $-6$. Résultat exact : $\mathbf{15}$. Contrôle : $15$ est à droite de $9$, ce qui est cohérent avec une soustraction de nombre négatif."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "soustraire un négatif traité comme une soustraction ordinaire"},
                    {"code": "CALCUL", "desc": "erreur isolée sur une somme de deux négatifs"}],
        "reussite": "quatre calculs exacts consécutifs, dont deux comportant une soustraction d'un nombre négatif, avec un contrôle écrit.",
    },
    "M4E_REL_02": {
        "titre": "Ordre des nombres relatifs et déplacements sur une droite graduée",
        "pourquoi": "Deux réponses fausses données avec une certitude maximale au diagnostic initial : la conviction doit être confrontée avant toute reprise technique.",
        "rappel": r"""\begin{methodbox}
\textbf{Trois repères.} Ranger dans l'ordre \textbf{croissant}, c'est lire la droite graduée de la \textbf{gauche vers la droite}.
Se déplacer vers la droite, c'est \textbf{ajouter} ; vers la gauche, c'est \textbf{soustraire}.
Entre deux nombres négatifs, le plus grand est celui qui est le plus \textbf{proche de zéro}.
\end{methodbox}
\begin{center}
\begin{tikzpicture}[x=0.85cm]
\draw[->,thick] (-6.5,0) -- (4.5,0);
\foreach \x in {-6,-5,-4,-3,-2,-1,0,1,2,3,4}{\draw (\x,0.12) -- (\x,-0.12) node[below]{\small $\x$};}
\draw[->,Blue,thick] (-5,0.5) -- (-1,0.5) node[midway,above]{\small $+4$};
\draw[->,Red,thick] (3,-0.75) -- (0,-0.75) node[midway,below]{\small $-3$};
\end{tikzpicture}
\end{center}""",
        "exemple": r"""\textbf{Exemple guidé.} Ranger dans l'ordre croissant : $-8$ ; $3$ ; $-2$ ; $0$ ; $-11$.
\begin{enumerate}
\item Placer mentalement chaque nombre sur la droite.
\item Lire de gauche à droite : $-11$ ; $-8$ ; $-2$ ; $0$ ; $3$.
\item Contrôler : les négatifs se rangent « à l'envers » des nombres positifs correspondants ($11 > 8 > 2$ devient $-11 < -8 < -2$).
\end{enumerate}""",
        "exos": [
            {"tex": r"Ranger dans l'ordre croissant : $-6$ ; $1$ ; $-13$ ; $0$ ; $-4$.", "space": "short",
             "corrige": r"$-13 < -6 < -4 < 0 < 1$."},
            {"tex": r"Ranger dans l'ordre décroissant : $-9$ ; $5$ ; $-2$ ; $7$.", "space": "short",
             "corrige": r"$7 > 5 > -2 > -9$."},
            {"tex": r"Un point d'abscisse $-13$ se déplace de $17$ unités vers la droite. Donner son abscisse finale.", "space": "short",
             "corrige": r"$-13+17=\mathbf{4}$."},
            {"tex": r"Un point d'abscisse $6$ se déplace de $11$ unités vers la gauche. Donner son abscisse finale.", "space": "short",
             "corrige": r"$6-11=\mathbf{-5}$."},
            {"tex": r"Comparer $-17$ et $-8$, puis justifier la réponse par une phrase et non par une règle apprise.", "space": "lines:2",
             "corrige": r"$-17 < -8$ : $-17$ est plus éloigné de zéro du côté négatif, donc plus à gauche sur la droite graduée."},
            {"tex": r"Un élève range $-3$ ; $-7$ ; $-10$ en écrivant « $-3 < -7 < -10$ ». Expliquer l'erreur, corriger, puis indiquer le contrôle qui l'aurait évitée.", "space": "lines:3",
             "corrige": r"Il a rangé les nombres comme s'ils étaient positifs. Ordre correct : $-10 < -7 < -3$. Contrôle : placer les trois points sur une droite graduée avant de conclure."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "ordre des négatifs calqué sur celui des positifs"},
                    {"code": "CONCEPT", "desc": "déplacement vers la droite traité comme une soustraction"},
                    {"code": "CONTROLE", "desc": "réponse donnée avec certitude sans support graphique"}],
        "reussite": "quatre classements ou déplacements corrects consécutifs, chacun justifié oralement par la position sur la droite.",
    },
    "M4E_FRAC_02": {
        "titre": "Fractions équivalentes et réduction au même dénominateur",
        "pourquoi": "Erreur documentée : le dénominateur est converti mais le numérateur ne l'est pas. C'est une erreur de concept sur l'égalité de deux fractions, non une erreur de calcul.",
        "rappel": r"""\begin{methodbox}
\textbf{Transformer une fraction, c'est transformer ses deux termes.} Multiplier le numérateur \emph{et}
le dénominateur par un même nombre non nul ne change pas la valeur de la fraction :
$\dfrac{a}{b}=\dfrac{a\times k}{b\times k}$. Si un seul terme est modifié, la fraction change de valeur.
\textbf{Contrôle :} une différence de deux fractions positives doit être plus petite que la première.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Calculer $\dfrac{5}{6}-\dfrac{1}{4}$.
\begin{enumerate}
\item Choisir un dénominateur commun : $12$.
\item Transformer \emph{entièrement} chaque fraction : $\frac{5}{6}=\frac{10}{12}$ (facteur $2$) et $\frac{1}{4}=\frac{3}{12}$ (facteur $3$).
\item Soustraire les numérateurs : $\frac{10}{12}-\frac{3}{12}=\frac{7}{12}$.
\item Contrôler : $\frac{7}{12}$ est bien inférieur à $\frac{5}{6}=\frac{10}{12}$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Compléter $\dfrac{3}{4}=\dfrac{\ldots}{20}$ et écrire le facteur utilisé.", "space": "short",
             "corrige": r"$\frac{15}{20}$, facteur $5$ appliqué aux deux termes."},
            {"tex": r"Calculer $\dfrac{5}{9}-\dfrac{1}{3}$.", "space": "short",
             "corrige": r"$\frac{5}{9}-\frac{3}{9}=\mathbf{\frac{2}{9}}$."},
            {"tex": r"Calculer $\dfrac{3}{4}+\dfrac{5}{12}$.", "space": "short",
             "corrige": r"$\frac{9}{12}+\frac{5}{12}=\frac{14}{12}=\mathbf{\frac{7}{6}}$."},
            {"tex": r"Calculer $\dfrac{7}{8}-\dfrac{3}{16}$.", "space": "short",
             "corrige": r"$\frac{14}{16}-\frac{3}{16}=\mathbf{\frac{11}{16}}$."},
            {"tex": r"Comparer $\dfrac{5}{8}$ et $\dfrac{7}{12}$ en les réduisant au même dénominateur.", "space": "lines:2",
             "corrige": r"$\frac{15}{24}$ et $\frac{14}{24}$ : donc $\frac{5}{8}>\frac{7}{12}$."},
            {"tex": r"Un élève écrit $\dfrac{5}{6}-\dfrac{1}{3}=\dfrac{4}{6}$. Nommer précisément l'erreur, corriger et écrire le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Le dénominateur de $\frac13$ a été converti en $6$ sans convertir le numérateur. $\frac13=\frac26$, donc le résultat exact est $\frac{3}{6}=\mathbf{\frac12}$. Contrôle : $\frac13$ vaut environ $0{,}33$ et $\frac56$ environ $0{,}83$ ; la différence vaut environ $0{,}5$, pas $0{,}67$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "conversion incomplète : un seul des deux termes est multiplié"},
                    {"code": "METHODE", "desc": "numérateurs et dénominateurs soustraits terme à terme"},
                    {"code": "CALCUL", "desc": "erreur sur le facteur de conversion"}],
        "reussite": "quatre soustractions ou additions consécutives exactes, la transformation complète de chaque fraction étant écrite.",
    },
    "M4E_LIT_02": {
        "titre": "Réduire une expression en respectant le signe des constantes",
        "pourquoi": "Erreur documentée sur la réduction des constantes signées ; compétence critique pour l'équation du premier degré travaillée dès septembre.",
        "rappel": r"""\begin{methodbox}
\textbf{Deux familles, jamais mélangées.} Les termes en $x$ se regroupent entre eux, les constantes entre elles.
Le signe qui précède un nombre lui \textbf{appartient} : dans $3 - 8$, la constante est $-8$.
\textbf{Contrôle :} remplacer $x$ par $0$ ne laisse que les constantes ; remplacer $x$ par $1$ vérifie l'ensemble.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Réduire $-2x + 7 + 5x - 12$.
\begin{enumerate}
\item Entourer les termes en $x$ : $-2x$ et $+5x$, donc $3x$.
\item Souligner les constantes avec leur signe : $+7$ et $-12$, donc $-5$.
\item Écrire $3x - 5$.
\item Contrôler avec $x = 0$ : l'expression de départ vaut $7 - 12 = -5$, l'expression réduite aussi.
\end{enumerate}""",
        "exos": [
            {"tex": r"Réduire $8x + 3 - 5x - 11$.", "space": "short", "corrige": r"$\mathbf{3x-8}$."},
            {"tex": r"Réduire $-4x + 9 + 7x - 2$.", "space": "short", "corrige": r"$\mathbf{3x+7}$."},
            {"tex": r"Développer puis réduire $3(x + 4) + 2x - 5$.", "space": "lines:2",
             "corrige": r"$3x+12+2x-5=\mathbf{5x+7}$."},
            {"tex": r"Développer puis réduire $6(x - 2) - x + 9$.", "space": "lines:2",
             "corrige": r"$6x-12-x+9=\mathbf{5x-3}$."},
            {"tex": r"Contrôler pour $x = 2$ que $8x + 3 - 5x - 11$ et $3x - 8$ donnent la même valeur.", "space": "lines:2",
             "corrige": r"$16+3-10-11=-2$ et $3\times 2-8=-2$ : les deux écritures coïncident."},
            {"tex": r"Un élève réduit $5x + 2 - 3x - 7$ en $2x + 9$. Nommer l'erreur, corriger et indiquer le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Il a additionné $2$ et $7$ en ignorant le signe $-$. Résultat exact : $\mathbf{2x-5}$. Contrôle : pour $x=0$, l'expression vaut $2-7=-5$ et non $+9$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "signe de la constante ignoré lors du regroupement"},
                    {"code": "CONCEPT", "desc": "terme en $x$ additionné à une constante"},
                    {"code": "CONTROLE", "desc": "aucune substitution de contrôle"}],
        "reussite": "trois réductions consécutives exactes avec constantes signées, dont une après développement, chacune contrôlée par substitution.",
    },
    "M4E_AIRE_01": {
        "titre": "Distinguer et calculer une aire et un périmètre",
        "pourquoi": "Confusion aire / périmètre documentée au diagnostic initial ; indicateur de réussite fixé au dossier : quatre exercices aire/périmètre consécutifs corrects.",
        "rappel": r"""\begin{methodbox}
\textbf{Deux questions différentes.} Le \textbf{périmètre} répond à « quelle est la longueur du contour ? »
et s'exprime en cm ou en m. L'\textbf{aire} répond à « quelle surface est occupée ? » et s'exprime en
$\text{cm}^2$ ou en $\text{m}^2$. Aire du triangle : $\text{base}\times\text{hauteur}\div 2$.
\textbf{Contrôle :} l'unité choisie est la première preuve que la bonne grandeur a été calculée.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Un rectangle mesure $9$ m sur $5$ m.
\begin{enumerate}
\item Périmètre : on fait le tour, $2\times(9+5)=28$ m.
\item Aire : on recouvre la surface, $9\times 5=45\ \text{m}^2$.
\item Contrôler : deux nombres différents, deux unités différentes. Écrire l'unité \emph{avant} de conclure.
\end{enumerate}""",
        "exos": [
            {"tex": r"Un rectangle mesure $13$ cm sur $6$ cm. Calculer son aire et son périmètre, unités comprises.", "space": "lines:2",
             "corrige": r"Aire $=78\ \text{cm}^2$ ; périmètre $=38$ cm."},
            {"tex": r"Un triangle a une base de $14$ cm et une hauteur de $5$ cm. Calculer son aire.", "space": "short",
             "corrige": r"$14\times 5\div 2=\mathbf{35\ \text{cm}^2}$."},
            {"tex": r"Un triangle a une aire de $42\ \text{cm}^2$ et une base de $12$ cm. Déterminer sa hauteur.", "space": "lines:2",
             "corrige": r"$h = 42\times 2 \div 12 = \mathbf{7}$ cm."},
            {"tex": r"Deux rectangles ont le même périmètre, $24$ cm : l'un mesure $8\times 4$, l'autre $10\times 2$. Comparer leurs aires et conclure en une phrase.", "space": "lines:3",
             "corrige": r"$32\ \text{cm}^2$ contre $20\ \text{cm}^2$ : deux figures de même périmètre n'ont pas nécessairement la même aire."},
            {"tex": r"Une pièce rectangulaire de $10$ m sur $4$ m comporte un placard carré de $3$ m de côté. Calculer l'aire restante.", "space": "lines:2",
             "corrige": r"$40 - 9 = \mathbf{31\ \text{m}^2}$."},
            {"tex": r"Un élève annonce : « l'aire de ce rectangle de $11$ cm sur $8$ cm est $38$ cm ». Repérer les deux erreurs et rectifier.", "space": "lines:3",
             "corrige": r"Il a calculé le périmètre et non l'aire, et il a employé une unité de longueur. Aire $=88\ \text{cm}^2$ ; périmètre $=38$ cm."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "aire et périmètre échangés"},
                    {"code": "NOTATION", "desc": "unité absente ou unité de longueur pour une aire"},
                    {"code": "METHODE", "desc": "division par 2 oubliée pour le triangle"}],
        "reussite": "quatre exercices consécutifs aire/périmètre corrects, chacun conclu par une unité écrite.",
    },
    "M4E_GEO_02": {
        "titre": "Symétrie centrale, parallélogramme et raisonnement donnée-propriété-conclusion",
        "pourquoi": "Le diagnostic montre une hypothèse ajoutée sans justification et une confusion entre parallélogramme et carré ; le travail porte sur la structure du raisonnement autant que sur la propriété.",
        "rappel": r"""\begin{methodbox}
\textbf{Trois lignes, toujours dans cet ordre.}
\textbf{Donnée} : ce que l'énoncé écrit ou code sur la figure — jamais ce que le dessin suggère.
\textbf{Propriété} : la règle mobilisée, énoncée en entier.
\textbf{Conclusion} : ce que l'on peut affirmer, et rien de plus.
\par\smallskip
Un quadrilatère dont les diagonales se coupent en leur milieu est un \textbf{parallélogramme}.
Le carré est un parallélogramme particulier : la réciproque est fausse.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} $ABCD$ a des diagonales qui se coupent en $O$ avec $AO = OC$ et $BO = OD$.
\begin{enumerate}
\item \textbf{Donnée} : les diagonales de $ABCD$ ont le même milieu $O$.
\item \textbf{Propriété} : si les diagonales d'un quadrilatère se coupent en leur milieu, alors ce quadrilatère est un parallélogramme.
\item \textbf{Conclusion} : $ABCD$ est un parallélogramme. On ne peut rien affirmer de plus sur ses angles ou ses côtés.
\end{enumerate}""",
        "exos": [
            {"tex": r"Deux angles d'un triangle mesurent $52^\circ$ et $61^\circ$. Calculer le troisième en rédigeant en donnée-propriété-conclusion.", "space": "lines:3",
             "corrige": r"Donnée : deux angles de $52^\circ$ et $61^\circ$. Propriété : la somme des angles d'un triangle vaut $180^\circ$. Conclusion : le troisième mesure $\mathbf{67^\circ}$."},
            {"tex": r"$EFGH$ a des diagonales de même milieu. Rédiger la conclusion la plus précise possible, en donnée-propriété-conclusion.", "space": "lines:3",
             "corrige": r"$EFGH$ est un parallélogramme. Toute affirmation supplémentaire (losange, rectangle) serait une hypothèse ajoutée."},
            {"tex": r"Un quadrilatère possède un centre de symétrie. Peut-on affirmer que c'est un carré ? Donner un contre-exemple précis.", "space": "lines:3",
             "corrige": r"Non : c'est un parallélogramme. Contre-exemple : un rectangle de $6$ cm sur $3$ cm possède un centre de symétrie sans être un carré."},
            {"tex": r"Un parallélogramme a ses diagonales perpendiculaires. Préciser sa nature et citer la propriété utilisée.", "space": "lines:2",
             "corrige": r"C'est un \textbf{losange} : un parallélogramme dont les diagonales sont perpendiculaires est un losange."},
            {"tex": r"Vrai ou faux, avec justification : « les diagonales d'un quadrilatère sont perpendiculaires, donc c'est un losange ».", "space": "lines:3",
             "corrige": r"Faux : il manque l'hypothèse « parallélogramme ». Un cerf-volant a des diagonales perpendiculaires sans être un losange."},
            {"tex": r"Sur une figure, deux côtés \emph{semblent} égaux mais rien n'est codé. Un élève écrit « $AB = AC$ donc le triangle est isocèle ». Nommer l'erreur de raisonnement et indiquer ce qui aurait été nécessaire.", "space": "lines:3",
             "corrige": r"Une apparence a été prise pour une donnée. Il aurait fallu un codage sur la figure ou une mention dans l'énoncé."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "réciproque supposée vraie (centre de symétrie donc carré)"},
                    {"code": "JUSTIFICATION", "desc": "conclusion exacte mais propriété non citée"},
                    {"code": "LECTURE", "desc": "apparence du dessin utilisée comme donnée"}],
        "reussite": "trois raisonnements complets rédigés en donnée-propriété-conclusion, sans aucune hypothèse ajoutée.",
    },

    # ================================================================= 3e
    "M3E_REL_01": {
        "titre": "Produit, quotient et priorités avec des nombres relatifs",
        "pourquoi": "Le signe d'un produit figure parmi les priorités du dossier individuel ; c'est le socle de tout le calcul littéral de Troisième.",
        "rappel": r"""\begin{methodbox}
\textbf{Deux règles, un ordre.} Deux facteurs de \textbf{même} signe donnent un produit \textbf{positif} ;
de signes \textbf{contraires}, un produit \textbf{négatif}. La même règle vaut pour le quotient.
\textbf{Ordre des opérations :} puissances, puis produits et quotients, puis sommes et différences.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Calculer $(-4)\times(-7) + (-18)\div 3$.
\begin{enumerate}
\item Repérer les deux opérations prioritaires : un produit et un quotient.
\item $(-4)\times(-7)=28$ (même signe) et $(-18)\div 3=-6$ (signes contraires).
\item Additionner : $28 + (-6) = 22$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Calculer $(-8)\times(-6)$.", "space": "short", "corrige": r"$\mathbf{48}$."},
            {"tex": r"Calculer $(-36)\div(-9) + (-5)\times 2$.", "space": "short", "corrige": r"$4 + (-10) = \mathbf{-6}$."},
            {"tex": r"Calculer $-3 \times (-2) \times (-5)$.", "space": "short",
             "corrige": r"$6\times(-5)=\mathbf{-30}$ : trois facteurs négatifs donnent un produit négatif."},
            {"tex": r"Calculer $(-7)\times 4 - (-12)\div(-3)$.", "space": "short", "corrige": r"$-28 - 4 = \mathbf{-32}$."},
            {"tex": r"Compléter : $(-6)\times(\ldots) = 42$, puis justifier le signe choisi.", "space": "lines:2",
             "corrige": r"Le facteur manquant est $\mathbf{-7}$ : le produit étant positif, les deux facteurs sont de même signe."},
            {"tex": r"Un élève écrit $(-5)\times(-3) = -15$. Nommer l'erreur, corriger et proposer un contrôle.", "space": "lines:3",
             "corrige": r"Il a appliqué la règle de l'addition de deux négatifs. Résultat exact : $\mathbf{15}$. Contrôle : $(-5)\times(-3)$ est l'opposé de $(-5)\times 3=-15$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "règle des signes de l'addition appliquée au produit"},
                    {"code": "METHODE", "desc": "calcul de gauche à droite sans respecter les priorités"}],
        "reussite": "cinq produits ou quotients relatifs exacts consécutifs, le signe étant annoncé avant le calcul de la valeur.",
    },
    "M3E_LIT_01": {
        "titre": "Développer avec la distributivité, y compris avec un facteur négatif",
        "pourquoi": "La distributivité figure parmi les priorités du dossier ; l'erreur porte sur la propagation du signe au second terme.",
        "rappel": r"""\begin{methodbox}
\textbf{Chaque terme, sans exception.} $k(a + b) = ka + kb$. Le facteur $k$ multiplie \textbf{tous} les
termes de la parenthèse, avec son signe. \textbf{Contrôle :} substituer une valeur simple dans les deux écritures.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Développer $-2(3x - 5)$.
\begin{enumerate}
\item Multiplier le premier terme : $-2 \times 3x = -6x$.
\item Multiplier le second terme \emph{avec son signe} : $-2 \times (-5) = +10$.
\item Écrire $-6x + 10$, puis contrôler pour $x = 1$ : $-2\times(-2)=4$ et $-6+10=4$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Développer $5(3x - 4)$.", "space": "short", "corrige": r"$\mathbf{15x-20}$."},
            {"tex": r"Développer $-3(2x + 7)$.", "space": "short", "corrige": r"$\mathbf{-6x-21}$."},
            {"tex": r"Développer $-4(5 - 2x)$.", "space": "short", "corrige": r"$\mathbf{-20+8x}$."},
            {"tex": r"Développer puis réduire $2(3x - 1) + 4x + 5$.", "space": "lines:2",
             "corrige": r"$6x-2+4x+5=\mathbf{10x+3}$."},
            {"tex": r"Contrôler pour $x = 3$ que $5(3x - 4)$ et $15x - 20$ donnent la même valeur.", "space": "lines:2",
             "corrige": r"$5\times 5 = 25$ et $45-20=25$."},
            {"tex": r"Un élève développe $3(2x - 5)$ en $6x - 5$. Nommer l'erreur, corriger et indiquer le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Le second terme n'a pas été multiplié. Résultat exact : $\mathbf{6x-15}$. Contrôle : pour $x=0$, l'expression vaut $3\times(-5)=-15$, et non $-5$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "distributivité appliquée au seul premier terme"},
                    {"code": "CALCUL", "desc": "signe du second produit erroné"}],
        "reussite": "quatre développements complets consécutifs, dont deux avec un facteur négatif, chacun contrôlé par substitution.",
    },
    "M3E_LIT_02": {
        "titre": "Réduire une expression avec des constantes signées",
        "pourquoi": "Erreur documentée sur l'addition des constantes signées lors d'une réduction ; prérequis direct de la factorisation et des identités remarquables de Troisième.",
        "rappel": r"""\begin{methodbox}
\textbf{Le signe appartient au nombre qui le suit.} Dans $4x - 7 + 2x + 3$, les constantes sont $-7$ et $+3$,
et non $7$ et $3$. Regrouper les termes en $x$ d'un côté, les constantes de l'autre.
\textbf{Contrôle :} pour $x = 0$, l'expression réduite doit rendre exactement la somme des constantes.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Réduire $-3x + 8 + 7x - 14$.
\begin{enumerate}
\item Termes en $x$ : $-3x + 7x = 4x$.
\item Constantes avec leur signe : $+8$ et $-14$, donc $-6$.
\item Écrire $4x - 6$, puis contrôler pour $x = 0$ : $8 - 14 = -6$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Réduire $9x - 6 + 2x - 5$.", "space": "short", "corrige": r"$\mathbf{11x-11}$."},
            {"tex": r"Réduire $-5x + 12 + 8x - 3$.", "space": "short", "corrige": r"$\mathbf{3x+9}$."},
            {"tex": r"Développer puis réduire $4(2x - 3) - 3x + 8$.", "space": "lines:2",
             "corrige": r"$8x-12-3x+8=\mathbf{5x-4}$."},
            {"tex": r"Développer puis réduire $-2(x - 6) + 5x - 9$.", "space": "lines:2",
             "corrige": r"$-2x+12+5x-9=\mathbf{3x+3}$."},
            {"tex": r"Contrôler pour $x = -1$ que $9x - 6 + 2x - 5$ et $11x - 11$ coïncident.", "space": "lines:2",
             "corrige": r"$-9-6-2-5=-22$ et $-11-11=-22$."},
            {"tex": r"Un élève réduit $4x - 7 + 2x + 3$ en $6x + 10$. Nommer l'erreur, corriger et écrire le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Les constantes ont été additionnées sans leur signe. Résultat exact : $\mathbf{6x-4}$. Contrôle : pour $x=0$, l'expression vaut $-7+3=-4$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "signe de la constante négligé"},
                    {"code": "CONCEPT", "desc": "termes en $x$ et constantes regroupés ensemble"},
                    {"code": "CONTROLE", "desc": "aucune substitution de vérification"}],
        "reussite": "quatre réductions consécutives exactes avec constantes signées, chacune contrôlée par $x = 0$ ou $x = -1$.",
    },
    "M3E_FRAC_02": {
        "titre": "Produit et quotient de fractions",
        "pourquoi": "Erreur documentée : croisement des termes lors d'un produit. La procédure du produit est confondue avec celle de la somme.",
        "rappel": r"""\begin{methodbox}
\textbf{Deux procédures à ne pas mélanger.} Pour un \textbf{produit} : numérateurs entre eux, dénominateurs
entre eux, sans dénominateur commun. Pour un \textbf{quotient} : multiplier par l'inverse.
Pour une \textbf{somme} : réduire d'abord au même dénominateur.
\textbf{Contrôle :} estimer l'ordre de grandeur avant de calculer.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Calculer $\dfrac{3}{8}\times\dfrac{4}{9}$.
\begin{enumerate}
\item Simplifier avant de multiplier : $3$ et $9$ par $3$ ; $4$ et $8$ par $4$.
\item Il reste $\frac{1}{2}\times\frac{1}{3}=\frac{1}{6}$.
\item Contrôler : $\frac38$ vaut environ $0{,}38$ et $\frac49$ environ $0{,}44$ ; leur produit vaut environ $0{,}17$, soit $\frac16$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Calculer $\dfrac{5}{7}\times\dfrac{14}{15}$ et simplifier.", "space": "short",
             "corrige": r"$\frac{70}{105}=\mathbf{\frac{2}{3}}$."},
            {"tex": r"Calculer $\dfrac{3}{10}\times\dfrac{25}{9}$ et simplifier.", "space": "short",
             "corrige": r"$\frac{75}{90}=\mathbf{\frac{5}{6}}$."},
            {"tex": r"Calculer $\dfrac{8}{15}\div\dfrac{4}{5}$.", "space": "lines:2",
             "corrige": r"$\frac{8}{15}\times\frac{5}{4}=\frac{40}{60}=\mathbf{\frac{2}{3}}$."},
            {"tex": r"Calculer $\dfrac{9}{16}\div\dfrac{3}{8}$.", "space": "lines:2",
             "corrige": r"$\frac{9}{16}\times\frac{8}{3}=\frac{72}{48}=\mathbf{\frac{3}{2}}$."},
            {"tex": r"Calculer $\dfrac{2}{3}\times\dfrac{6}{5}$ puis $\dfrac{2}{3}+\dfrac{6}{5}$, et expliquer pourquoi les deux méthodes diffèrent.", "space": "lines:3",
             "corrige": r"$\frac{12}{15}=\frac45$ ; $\frac{10}{15}+\frac{18}{15}=\frac{28}{15}$. Le produit n'exige aucun dénominateur commun, la somme si."},
            {"tex": r"Un élève écrit $\dfrac{2}{3}\times\dfrac{9}{4}=\dfrac{8}{27}$. Nommer l'erreur, corriger et donner un contrôle par estimation.", "space": "lines:3",
             "corrige": r"Il a croisé les termes. Résultat exact : $\frac{18}{12}=\mathbf{\frac{3}{2}}$. Contrôle : $\frac23$ est inférieur à $1$ et $\frac94$ supérieur à $2$, donc le produit vaut environ $1{,}5$ — certainement pas $0{,}3$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "termes croisés lors du produit"},
                    {"code": "METHODE", "desc": "réduction au même dénominateur appliquée à un produit"},
                    {"code": "CALCUL", "desc": "simplification incomplète"}],
        "reussite": "cinq produits ou quotients exacts consécutifs, dont deux comportant une simplification, avec une estimation écrite.",
    },
    "M3E_EQ_01": {
        "titre": "Résoudre une équation du premier degré et vérifier la solution",
        "pourquoi": "Les équations figurent parmi les domaines à installer d'après le dossier individuel ; elles conditionnent la mise en équation des problèmes de Troisième.",
        "rappel": r"""\begin{methodbox}
\textbf{Une balance.} Ce que l'on fait à un membre, on le fait à l'autre. On regroupe les termes en $x$ d'un
côté, les nombres de l'autre, puis on divise par le coefficient de $x$.
\textbf{Contrôle obligatoire :} remplacer la valeur trouvée dans l'équation de départ et calculer les deux membres séparément.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Résoudre $5x - 4 = 2x + 11$.
\begin{enumerate}
\item Retrancher $2x$ aux deux membres : $3x - 4 = 11$.
\item Ajouter $4$ aux deux membres : $3x = 15$.
\item Diviser par $3$ : $x = 5$.
\item Contrôler : $5\times 5-4=21$ et $2\times 5+11=21$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Résoudre $3x + 7 = 25$.", "space": "lines:2", "corrige": r"$3x=18$ donc $\mathbf{x=6}$."},
            {"tex": r"Résoudre $6x - 5 = 4x + 9$.", "space": "lines:2", "corrige": r"$2x=14$ donc $\mathbf{x=7}$."},
            {"tex": r"Résoudre $2(x + 3) = 14$.", "space": "lines:2",
             "corrige": r"$2x+6=14$ donc $2x=8$ et $\mathbf{x=4}$."},
            {"tex": r"Résoudre $5x + 2 = 3x - 8$.", "space": "lines:2", "corrige": r"$2x=-10$ donc $\mathbf{x=-5}$."},
            {"tex": r"Vérifier que $x = 4$ est solution de $7x - 9 = 3x + 7$, en calculant les deux membres séparément.", "space": "lines:2",
             "corrige": r"$28-9=19$ et $12+7=19$ : $x=4$ est bien solution."},
            {"tex": r"Un élève résout $5x - 2 = 3x + 8$ en écrivant $5x + 3x = 8 + 2$. Nommer l'erreur, corriger et donner la solution exacte.", "space": "lines:3",
             "corrige": r"Le terme $3x$ a changé de membre sans changer de signe. Il fallait écrire $5x-3x=8+2$, donc $2x=10$ et $\mathbf{x=5}$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "signe non changé lors du passage d'un membre à l'autre"},
                    {"code": "METHODE", "desc": "division effectuée avant le regroupement"},
                    {"code": "CONTROLE", "desc": "solution non vérifiée"}],
        "reussite": "trois équations résolues et vérifiées consécutivement, dont une avec l'inconnue dans les deux membres.",
    },
    "M3E_TRIG_01": {
        "titre": "Identifier les côtés puis choisir le rapport trigonométrique",
        "pourquoi": "Le dossier signale une trigonométrie à installer ou une confusion cosinus/sinus ; l'erreur est un défaut d'identification des côtés, non un défaut de calcul.",
        "rappel": r"""\begin{methodbox}
\textbf{Le nom d'un côté dépend de l'angle choisi.} L'\textbf{hypoténuse} est toujours le côté opposé à
l'angle droit. Les deux autres côtés changent de nom selon l'angle aigu considéré : \textbf{adjacent}
s'il touche l'angle, \textbf{opposé} sinon.
\par\smallskip
$\cos = \dfrac{\text{adjacent}}{\text{hypoténuse}}$ \qquad $\sin = \dfrac{\text{opposé}}{\text{hypoténuse}}$
\par\smallskip
\textbf{Contrôle :} un cosinus ou un sinus est toujours compris entre $0$ et $1$ dans un triangle rectangle.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} $ABC$ est rectangle en $A$, $AB = 8$ cm, $BC = 17$ cm. Calculer $\widehat{B}$.
\begin{enumerate}
\item Par rapport à $\widehat{B}$ : $AB$ touche l'angle, c'est l'\textbf{adjacent} ; $BC$ est l'\textbf{hypoténuse}.
\item Le rapport disponible est donc le cosinus : $\cos\widehat{B}=\frac{8}{17}\approx 0{,}4706$.
\item $\widehat{B}\approx 62^\circ$. Contrôle : $0{,}4706$ est bien compris entre $0$ et $1$.
\end{enumerate}""",
        "exos": [
            {"tex": r"$ABC$ est rectangle en $A$. Par rapport à l'angle $\widehat{C}$, nommer $AB$, $AC$ et $BC$.", "space": "lines:2",
             "corrige": r"$AC$ : côté adjacent à $\widehat{C}$ ; $AB$ : côté opposé à $\widehat{C}$ ; $BC$ : hypoténuse."},
            {"tex": r"$ABC$ est rectangle en $A$ avec $AC = 7$ cm et $BC = 25$ cm. Calculer $\cos\widehat{C}$ puis $\widehat{C}$ au degré près.", "space": "lines:2",
             "corrige": r"$\cos\widehat{C}=\frac{7}{25}=0{,}28$ donc $\widehat{C}\approx \mathbf{74^\circ}$."},
            {"tex": r"$ABC$ est rectangle en $A$ avec $AB = 9$ cm et $BC = 15$ cm. Quel rapport permet de calculer $\widehat{C}$ ? Le calculer, puis donner $\widehat{C}$ au degré près.", "space": "lines:3",
             "corrige": r"$AB$ est opposé à $\widehat{C}$ : c'est le sinus. $\sin\widehat{C}=\frac{9}{15}=0{,}6$ donc $\widehat{C}\approx \mathbf{37^\circ}$."},
            {"tex": r"$ABC$ est rectangle en $A$, $BC = 20$ cm et $\widehat{B} = 35^\circ$. Calculer $AB$ au dixième près.", "space": "lines:3",
             "corrige": r"$\cos 35^\circ = \frac{AB}{20}$ donc $AB = 20\cos 35^\circ \approx \mathbf{16{,}4}$ cm."},
            {"tex": r"Un élève écrit $\cos\widehat{B} = \dfrac{BC}{AB}$ avec $BC$ l'hypoténuse. Expliquer pourquoi c'est impossible \emph{sans effectuer aucun calcul}.", "space": "lines:3",
             "corrige": r"L'hypoténuse est le plus grand côté : ce quotient est donc supérieur à $1$, ce qu'un cosinus ne peut pas être."},
            {"tex": r"Compléter : si l'on connaît l'adjacent et l'hypoténuse, on utilise \rule{25mm}{0.32pt} ; si l'on connaît l'opposé et l'hypoténuse, on utilise \rule{25mm}{0.32pt}. Justifier chaque choix en une phrase.", "space": "lines:3",
             "corrige": r"Le cosinus, puis le sinus : chaque rapport est défini par les deux côtés qu'il met en jeu."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "cosinus et sinus échangés"},
                    {"code": "LECTURE", "desc": "côtés nommés par rapport au mauvais angle"},
                    {"code": "CONTROLE", "desc": "valeur supérieure à 1 acceptée pour un cosinus"}],
        "reussite": "quatre rapports correctement identifiés puis employés, chaque réponse étant précédée du nom des côtés utilisés.",
    },

    # ================================================================= 2nde
    "M2DE_CALC_01": {
        "titre": "Priorités opératoires, signes et puissance d'un nombre négatif",
        "pourquoi": "Le diagnostic signale des certitudes erronées sur les priorités et les signes ; ces automatismes conditionnent tout le calcul algébrique de Seconde.",
        "rappel": r"""\begin{methodbox}
\textbf{Un ordre, jamais la lecture de gauche à droite.} Puissances, puis produits et quotients,
puis sommes et différences. Les parenthèses passent avant tout.
\par\smallskip
$(-2)^3 = -8$ mais $(-2)^4 = 16$ ; en revanche $-2^4 = -16$ : la parenthèse change le sens de l'écriture.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Calculer $-4 + 2 \times (-3)^2$.
\begin{enumerate}
\item Puissance d'abord : $(-3)^2 = 9$.
\item Produit ensuite : $2 \times 9 = 18$.
\item Somme enfin : $-4 + 18 = 14$.
\item Contrôle : lire l'expression à voix haute en nommant l'opération traitée à chaque étape.
\end{enumerate}""",
        "exos": [
            {"tex": r"Calculer $-7 + 2 \times (-5)$.", "space": "short", "corrige": r"$-7-10=\mathbf{-17}$."},
            {"tex": r"Calculer $(-3)^2 - (-3)^3$.", "space": "short", "corrige": r"$9 - (-27) = \mathbf{36}$."},
            {"tex": r"Calculer séparément $(-2)^4$ et $-2^4$, puis expliquer la différence.", "space": "lines:2",
             "corrige": r"$16$ et $-16$ : dans le second cas, seule la puissance de $2$ est calculée, le signe reste devant."},
            {"tex": r"Calculer $12 \div (-4) + (-2)\times(-6)$.", "space": "short", "corrige": r"$-3 + 12 = \mathbf{9}$."},
            {"tex": r"Calculer $-5 - 3 \times (2 - 7)$.", "space": "lines:2", "corrige": r"$-5 - 3\times(-5) = -5 + 15 = \mathbf{10}$."},
            {"tex": r"Un élève écrit $-3 + 4 \times (-2) = -2$. Nommer l'erreur, corriger et indiquer le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Il a calculé $(-3+4)\times(-2)$. Résultat exact : $-3-8=\mathbf{-11}$. Contrôle : nommer l'opération prioritaire avant d'écrire le premier chiffre."},
        ],
        "erreurs": [{"code": "METHODE", "desc": "lecture de gauche à droite sans priorité"},
                    {"code": "NOTATION", "desc": "parenthèses de $(-a)^n$ ignorées"},
                    {"code": "CONCEPT", "desc": "règle des signes du produit appliquée à une somme"}],
        "reussite": "cinq calculs exacts consécutifs, l'opération prioritaire étant annoncée avant chaque résolution.",
    },
    "M2DE_ALG_01": {
        "titre": "Double distributivité et identités remarquables",
        "pourquoi": "Les identités remarquables figurent parmi les priorités du dossier ; elles sont l'outil de base des chapitres d'algèbre de Seconde.",
        "rappel": r"""\begin{methodbox}
\textbf{Quatre produits, jamais deux.} $(a+b)(c+d) = ac + ad + bc + bd$.
\par\smallskip
$(a+b)^2 = a^2 + 2ab + b^2$ \qquad $(a-b)^2 = a^2 - 2ab + b^2$ \qquad $(a-b)(a+b) = a^2 - b^2$
\par\smallskip
\textbf{Contrôle :} substituer $x = 1$ ou $x = 2$ dans la forme initiale et dans la forme développée.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Développer et réduire $(x - 4)(x + 6)$.
\begin{enumerate}
\item Les quatre produits : $x\times x$, $x\times 6$, $-4\times x$, $-4\times 6$.
\item On obtient $x^2 + 6x - 4x - 24$.
\item Réduire : $x^2 + 2x - 24$.
\item Contrôler pour $x = 1$ : $(-3)\times 7 = -21$ et $1 + 2 - 24 = -21$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Développer et réduire $(x + 2)(x - 9)$.", "space": "lines:2", "corrige": r"$x^2-9x+2x-18=\mathbf{x^2-7x-18}$."},
            {"tex": r"Développer $(x + 6)^2$.", "space": "short", "corrige": r"$\mathbf{x^2+12x+36}$."},
            {"tex": r"Développer $(3x - 4)^2$.", "space": "lines:2", "corrige": r"$\mathbf{9x^2-24x+16}$."},
            {"tex": r"Développer $(3x - 7)(3x + 7)$.", "space": "lines:2", "corrige": r"$\mathbf{9x^2-49}$ : le double produit se simplifie."},
            {"tex": r"Contrôler pour $x = 2$ que $(x + 2)(x - 9)$ et $x^2 - 7x - 18$ donnent la même valeur.", "space": "lines:2",
             "corrige": r"$4\times(-7)=-28$ et $4-14-18=-28$."},
            {"tex": r"Un élève écrit $(x - 4)^2 = x^2 - 16$. Nommer l'erreur, corriger et donner le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Le double produit a été oublié ; il a confondu $(a-b)^2$ et $a^2-b^2$. Résultat exact : $\mathbf{x^2-8x+16}$. Contrôle : pour $x=0$, $(0-4)^2=16$ et non $-16$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "double produit oublié dans le carré d'une somme ou d'une différence"},
                    {"code": "CONCEPT", "desc": "$(a-b)^2$ confondu avec $a^2-b^2$"},
                    {"code": "CALCUL", "desc": "signe du double produit erroné"}],
        "reussite": "quatre développements exacts consécutifs, dont deux identités remarquables, chacun contrôlé par substitution.",
    },
    "M2DE_EQ_02": {
        "titre": "Équation produit nul",
        "pourquoi": "Le dossier place les équations parmi les domaines à installer ; l'équation produit nul est l'outil qui prépare le second degré.",
        "rappel": r"""\begin{methodbox}
\textbf{Une propriété, pas une manipulation.} Un produit de facteurs est nul \textbf{si et seulement si}
l'un au moins des facteurs est nul. Une équation sous forme factorisée ne doit donc \textbf{jamais} être développée.
\textbf{Contrôle :} une équation produit à deux facteurs distincts possède en général deux solutions.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Résoudre $(2x - 6)(x + 5) = 0$.
\begin{enumerate}
\item Propriété : le produit est nul, donc $2x - 6 = 0$ ou $x + 5 = 0$.
\item Première équation : $2x = 6$, donc $x = 3$.
\item Seconde équation : $x = -5$.
\item Contrôler $x = 3$ : $(0)\times 8 = 0$. Contrôler $x = -5$ : $(-16)\times 0 = 0$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Résoudre $(x - 7)(x + 2) = 0$.", "space": "lines:2", "corrige": r"$x=\mathbf{7}$ ou $x=\mathbf{-2}$."},
            {"tex": r"Résoudre $(3x + 9)(2x - 5) = 0$.", "space": "lines:2", "corrige": r"$x=\mathbf{-3}$ ou $x=\mathbf{\frac52}$."},
            {"tex": r"Résoudre $x(x - 4) = 0$.", "space": "lines:2", "corrige": r"$x=\mathbf{0}$ ou $x=\mathbf{4}$ : $x$ est lui-même un facteur."},
            {"tex": r"Factoriser $x^2 - 5x$, puis résoudre $x^2 - 5x = 0$.", "space": "lines:3",
             "corrige": r"$x(x-5)=0$ donc $x=\mathbf{0}$ ou $x=\mathbf{5}$."},
            {"tex": r"Vérifier que $-4$ est solution de $(x + 4)(3x - 1) = 0$, puis donner l'autre solution.", "space": "lines:2",
             "corrige": r"$(0)\times(-13)=0$ : $-4$ convient. L'autre solution est $x=\mathbf{\frac13}$."},
            {"tex": r"Un élève résout $(3x + 5)(x - 2) = 0$ en développant d'abord. Expliquer pourquoi la forme factorisée est préférable et ce qu'il risque de perdre.", "space": "lines:3",
             "corrige": r"Développer donne $3x^2-x-10=0$, équation qu'il ne sait pas encore résoudre : il perd l'accès direct aux deux solutions $-\frac53$ et $2$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "une seule solution retenue"},
                    {"code": "METHODE", "desc": "forme factorisée développée avant résolution"},
                    {"code": "JUSTIFICATION", "desc": "propriété du produit nul non énoncée"}],
        "reussite": "trois équations produit résolues consécutivement avec les deux solutions et la propriété citée.",
    },
    "M2DE_POURC_01": {
        "titre": "Coefficient multiplicateur et évolutions successives",
        "pourquoi": "Le diagnostic montre que deux évolutions successives sont traitées comme une somme de pourcentages ; c'est une erreur de concept persistante jusqu'en Première.",
        "rappel": r"""\begin{methodbox}
\textbf{Un pourcentage se traduit par un coefficient.} Une hausse de $t\,\%$ correspond au coefficient
$1 + \frac{t}{100}$, une baisse de $t\,\%$ au coefficient $1 - \frac{t}{100}$.
\par\smallskip
\textbf{Deux évolutions successives se multiplient, elles ne s'additionnent jamais.}
\textbf{Contrôle :} un coefficient global supérieur à $1$ signifie une hausse globale, inférieur à $1$ une baisse.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Un prix de $200$ TND augmente de $25\,\%$, puis baisse de $25\,\%$.
\begin{enumerate}
\item Coefficients : $1{,}25$ puis $0{,}75$.
\item Prix intermédiaire : $200\times 1{,}25 = 250$ TND. Prix final : $250\times 0{,}75 = 187{,}50$ TND.
\item Coefficient global : $1{,}25\times 0{,}75 = 0{,}9375$, soit une baisse globale de $6{,}25\,\%$.
\item Contrôle : le prix final est bien inférieur au prix initial, ce que le coefficient global annonçait.
\end{enumerate}""",
        "exos": [
            {"tex": r"Un prix de $340$ TND augmente de $15\,\%$. Calculer le nouveau prix.", "space": "short",
             "corrige": r"$340\times 1{,}15 = \mathbf{391}$ TND."},
            {"tex": r"Un prix de $340$ TND baisse de $15\,\%$. Calculer le nouveau prix.", "space": "short",
             "corrige": r"$340\times 0{,}85 = \mathbf{289}$ TND."},
            {"tex": r"Donner le coefficient multiplicateur d'une hausse de $8\,\%$, puis celui d'une baisse de $8\,\%$.", "space": "short",
             "corrige": r"$1{,}08$ et $0{,}92$."},
            {"tex": r"Un prix augmente de $10\,\%$ puis de $30\,\%$. Le coefficient global vaut-il $1{,}40$ ? Justifier par le calcul.", "space": "lines:3",
             "corrige": r"Non : $1{,}1\times 1{,}3 = 1{,}43$, soit une hausse globale de $43\,\%$ et non de $40\,\%$."},
            {"tex": r"Un prix passe de $480$ TND à $552$ TND. Calculer le taux d'évolution en pourcentage.", "space": "lines:2",
             "corrige": r"$\frac{552-480}{480}=0{,}15$, soit une hausse de $\mathbf{15\,\%}$."},
            {"tex": r"Un élève affirme : « une hausse de $20\,\%$ suivie d'une baisse de $20\,\%$ ramène au prix initial ». Réfuter par un calcul sur $100$ TND, puis nommer la conception erronée.", "space": "lines:3",
             "corrige": r"$100\to 120\to 96$ : le prix final est inférieur. Conception erronée : les pourcentages sont additionnés alors que les coefficients se multiplient ($1{,}2\times 0{,}8=0{,}96$)."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "pourcentages additionnés au lieu de coefficients multipliés"},
                    {"code": "CONCEPT", "desc": "coefficient d'une baisse de $t\\,\\%$ pris égal à $t/100$"},
                    {"code": "CONTROLE", "desc": "sens de l'évolution globale non vérifié"}],
        "reussite": "trois situations d'évolution traitées consécutivement par coefficient multiplicateur, dont une composée, avec conclusion argumentée.",
    },

    # ================================================================= 1ere_spe
    "M1RE_ALG_02": {
        "titre": "Factoriser, en particulier une différence de deux carrés",
        "pourquoi": "La factorisation figure parmi les priorités du dossier ; c'est l'outil direct de l'étude du signe d'un trinôme en Première.",
        "rappel": r"""\begin{methodbox}
\textbf{Reconnaître avant de calculer.} $a^2 - b^2 = (a - b)(a + b)$. Il faut identifier ce qui joue le rôle
de $a$ et de $b$, y compris lorsque $a$ contient la variable.
\par\smallskip
Une \textbf{somme} de deux carrés ne se factorise pas dans $\mathbb{R}$.
\textbf{Contrôle :} développer la forme factorisée doit redonner exactement l'expression de départ.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Factoriser $4x^2 - 81$.
\begin{enumerate}
\item Écrire chaque terme comme un carré : $4x^2 = (2x)^2$ et $81 = 9^2$.
\item Appliquer l'identité : $(2x - 9)(2x + 9)$.
\item Contrôler : $(2x)^2 - 9^2 = 4x^2 - 81$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Factoriser $x^2 - 36$.", "space": "short", "corrige": r"$\mathbf{(x-6)(x+6)}$."},
            {"tex": r"Factoriser $25x^2 - 4$.", "space": "short", "corrige": r"$\mathbf{(5x-2)(5x+2)}$."},
            {"tex": r"Factoriser $(x + 1)^2 - 9$.", "space": "lines:2",
             "corrige": r"$(x+1-3)(x+1+3)=\mathbf{(x-2)(x+4)}$."},
            {"tex": r"Factoriser $3x^2 - 12$.", "space": "lines:2",
             "corrige": r"$3(x^2-4)=\mathbf{3(x-2)(x+2)}$ : facteur commun d'abord."},
            {"tex": r"Peut-on factoriser $x^2 + 16$ dans $\mathbb{R}$ ? Justifier en une phrase.", "space": "lines:2",
             "corrige": r"Non : c'est une somme de carrés, strictement positive pour tout réel $x$, elle n'admet aucune racine réelle."},
            {"tex": r"Un élève factorise $x^2 - 9$ en $(x - 3)^2$. Nommer l'erreur, corriger et donner le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Il a confondu différence de carrés et carré d'une différence. Factorisation exacte : $\mathbf{(x-3)(x+3)}$. Contrôle : développer $(x-3)^2$ donne $x^2-6x+9$, ce qui n'est pas $x^2-9$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "$a^2-b^2$ confondu avec $(a-b)^2$"},
                    {"code": "METHODE", "desc": "facteur commun non extrait avant l'identité"},
                    {"code": "CONTROLE", "desc": "factorisation non vérifiée par développement"}],
        "reussite": "cinq factorisations immédiates consécutives exactes, chacune vérifiée par développement.",
    },
    "M1RE_FONC_02": {
        "titre": "Le langage des fonctions : image, antécédent, appartenance à la courbe",
        "pourquoi": "Le dossier signale un langage fonctionnel à rectifier ; ce vocabulaire est employé dans tous les chapitres de Première, en particulier en dérivation.",
        "rappel": r"""\begin{methodbox}
\textbf{Une égalité, trois formulations équivalentes.} $f(a) = b$ signifie exactement :
\begin{itemize}
\item $b$ est l'\textbf{image} de $a$ par $f$ ;
\item $a$ est \textbf{un} antécédent de $b$ par $f$ ;
\item le point de coordonnées $(a\,;b)$ appartient à la courbe de $f$.
\end{itemize}
\textbf{Attention :} une image est unique, un antécédent ne l'est pas nécessairement.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} La courbe de $f$ passe par le point de coordonnées $(2\,;-3)$.
\begin{enumerate}
\item Traduire par une égalité : $f(2) = -3$.
\item Première lecture : $-3$ est l'image de $2$.
\item Seconde lecture : $2$ est un antécédent de $-3$.
\item Contrôle : l'abscisse est toujours l'entrée de la fonction, l'ordonnée toujours la sortie.
\end{enumerate}""",
        "exos": [
            {"tex": r"La courbe de $f$ passe par $(-1\,;4)$. Écrire l'égalité correspondante, puis les deux phrases avec « image » et « antécédent ».", "space": "lines:3",
             "corrige": r"$f(-1)=4$ ; $4$ est l'image de $-1$ ; $-1$ est un antécédent de $4$."},
            {"tex": r"Soit $f(x) = 3x - 5$. Calculer l'image de $-2$.", "space": "short", "corrige": r"$f(-2)=-6-5=\mathbf{-11}$."},
            {"tex": r"Soit $f(x) = 3x - 5$. Déterminer l'antécédent de $7$ en écrivant l'équation résolue.", "space": "lines:2",
             "corrige": r"$3x-5=7$ donne $3x=12$ donc $x=\mathbf{4}$."},
            {"tex": r"Soit $g(x) = x^2 - 4$. Déterminer \emph{tous} les antécédents de $0$.", "space": "lines:2",
             "corrige": r"$x^2-4=0$ donne $(x-2)(x+2)=0$ : les antécédents sont $\mathbf{-2}$ et $\mathbf{2}$."},
            {"tex": r"Le point de coordonnées $(5\,;0)$ appartient-il à la courbe de $h$ définie par $h(x) = x^2 - 5x$ ? Justifier par un calcul.", "space": "lines:2",
             "corrige": r"$h(5)=25-25=0$ : oui, le point appartient à la courbe."},
            {"tex": r"Un élève écrit « l'image de $7$ par $f$ est $4$ » alors que l'énoncé donne $f(4) = 7$. Nommer l'erreur et rectifier les deux formulations.", "space": "lines:3",
             "corrige": r"Image et antécédent sont inversés. Formulations exactes : $7$ est l'image de $4$ ; $4$ est un antécédent de $7$."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "image et antécédent échangés"},
                    {"code": "METHODE", "desc": "antécédent cherché par essais au lieu d'une équation"},
                    {"code": "CONCEPT", "desc": "un seul antécédent donné lorsqu'il en existe deux"}],
        "reussite": "quatre formulations fonctionnelles correctes consécutives, dont un antécédent obtenu par résolution d'équation.",
    },
    "M1RE_INEQ_01": {
        "titre": "Inéquation du premier degré et écriture en intervalle",
        "pourquoi": "Les inéquations figurent parmi les domaines à installer d'après le dossier ; elles conditionnent les tableaux de signes du second degré.",
        "rappel": r"""\begin{methodbox}
\textbf{Une seule différence avec les équations.} Ajouter ou retrancher un nombre ne change rien.
Multiplier ou diviser par un nombre \textbf{positif} conserve le sens de l'inégalité ; par un nombre
\textbf{négatif}, le sens s'\textbf{inverse}.
\par\smallskip
Écriture en intervalle : $x < a$ donne $\left]-\infty\,;a\right[$ ; $x \ge a$ donne $\left[a\,;+\infty\right[$.
Une inégalité stricte donne toujours un crochet ouvert.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Résoudre $-5x + 3 < 18$.
\begin{enumerate}
\item Retrancher $3$ : $-5x < 15$.
\item Diviser par $-5$ : le sens change, donc $x > -3$.
\item Écrire l'ensemble des solutions : $S = \left]-3\,;+\infty\right[$.
\item Contrôle : tester $x = 0$ dans l'inéquation initiale : $3 < 18$, vrai, et $0$ appartient bien à $S$.
\end{enumerate}""",
        "exos": [
            {"tex": r"Résoudre $4x - 7 \le 9$ et donner l'ensemble des solutions sous forme d'intervalle.", "space": "lines:2",
             "corrige": r"$4x\le 16$ donc $x\le 4$ : $S=\left]-\infty\,;4\right]$."},
            {"tex": r"Résoudre $-2x + 5 > 11$ et donner l'intervalle.", "space": "lines:2",
             "corrige": r"$-2x>6$ donc $x<-3$ : $S=\left]-\infty\,;-3\right[$."},
            {"tex": r"Résoudre $3x + 2 \ge 5x - 6$.", "space": "lines:2",
             "corrige": r"$-2x \ge -8$ donc $x\le 4$ : $S=\left]-\infty\,;4\right]$."},
            {"tex": r"Traduire par une inéquation puis résoudre : « le triple d'un nombre diminué de $4$ ne dépasse pas $20$ ».", "space": "lines:3",
             "corrige": r"$3x-4\le 20$ donne $x\le 8$ : $S=\left]-\infty\,;8\right]$."},
            {"tex": r"Représenter sur un axe l'ensemble $\left]-\infty\,;4\right]$, puis donner deux valeurs qui conviennent et une qui ne convient pas.", "space": "lines:3",
             "corrige": r"Crochet fermé en $4$, hachures vers la gauche. Par exemple $0$ et $4$ conviennent ; $5$ ne convient pas."},
            {"tex": r"Un élève résout $-3x > 9$ en écrivant $x > -3$. Nommer l'erreur, corriger et donner le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Le sens de l'inégalité n'a pas été inversé lors de la division par $-3$. Solution exacte : $x < -3$. Contrôle : $x=0$ donne $0 > 9$, faux, donc $0$ n'appartient pas à l'ensemble des solutions."},
        ],
        "erreurs": [{"code": "CONCEPT", "desc": "sens de l'inégalité conservé après division par un négatif"},
                    {"code": "NOTATION", "desc": "crochet fermé sur une inégalité stricte ou sur l'infini"},
                    {"code": "CONTROLE", "desc": "aucune valeur testée dans l'inéquation initiale"}],
        "reussite": "trois inéquations résolues consécutivement en autonomie, chacune assortie de l'intervalle et d'une valeur de contrôle.",
    },
    "M1RE_FONC_01": {
        "titre": "Calculer une image, en particulier pour une valeur négative",
        "pourquoi": "Erreur documentée sur la substitution d'un nombre négatif ; l'omission des parenthèses est une erreur d'écriture qui produit systématiquement un résultat faux.",
        "rappel": r"""\begin{methodbox}
\textbf{Substituer, c'est remplacer la lettre par le nombre \emph{entre parenthèses}.}
$(-3)^2 = 9$ alors que $-3^2 = -9$ : dans la seconde écriture, le carré ne porte que sur $3$.
\textbf{Contrôle :} réécrire l'expression complète avec les parenthèses avant d'effectuer le moindre calcul.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Pour $f(x) = x^2 - 4x$, calculer $f(-3)$.
\begin{enumerate}
\item Écrire la substitution complète : $f(-3) = (-3)^2 - 4\times(-3)$.
\item Calculer chaque terme : $9$ et $+12$.
\item Conclure : $f(-3) = 21$.
\item Contrôle : les deux termes sont positifs, le résultat ne peut pas être négatif.
\end{enumerate}""",
        "exos": [
            {"tex": r"Soit $f(x) = x^2 + 2x$. Calculer $f(-4)$, $f(0)$ et $f(3)$.", "space": "lines:3",
             "corrige": r"$f(-4)=16-8=\mathbf{8}$ ; $f(0)=\mathbf{0}$ ; $f(3)=9+6=\mathbf{15}$."},
            {"tex": r"Soit $g(x) = -2x^2 + x$. Calculer $g(-3)$.", "space": "lines:2",
             "corrige": r"$g(-3)=-2\times 9 + (-3) = \mathbf{-21}$."},
            {"tex": r"Soit $h(x) = (x - 1)^2$. Calculer $h(-4)$.", "space": "lines:2",
             "corrige": r"$h(-4)=(-5)^2=\mathbf{25}$."},
            {"tex": r"Calculer séparément $(-5)^2$ et $-5^2$, puis expliquer la différence en une phrase.", "space": "lines:2",
             "corrige": r"$25$ et $-25$ : dans le second cas, le signe $-$ est appliqué après le carré."},
            {"tex": r"Soit $k(x) = x^3$. Calculer $k(-2)$ et justifier le signe obtenu.", "space": "lines:2",
             "corrige": r"$k(-2)=-8$ : un exposant impair conserve le signe du nombre."},
            {"tex": r"Pour $f(x) = x^2 - 3x$, un élève écrit $f(-2) = -2^2 - 3\times(-2) = -4 + 6 = 2$. Nommer l'erreur, corriger et donner le contrôle qui l'aurait détectée.", "space": "lines:3",
             "corrige": r"Les parenthèses manquent autour de $-2$ : il fallait $(-2)^2 = 4$. Résultat exact : $f(-2)=4+6=\mathbf{10}$. Contrôle : les deux termes sont positifs, le résultat ne peut valoir $2$."},
        ],
        "erreurs": [{"code": "NOTATION", "desc": "parenthèses omises autour d'une valeur négative substituée"},
                    {"code": "CALCUL", "desc": "signe du produit $-4\\times(-3)$ erroné"},
                    {"code": "CONTROLE", "desc": "signe du résultat non confronté aux signes des termes"}],
        "reussite": "trois substitutions négatives consécutives sans erreur de signe, la substitution complète étant écrite avant tout calcul.",
    },
    "M1RE_VECT_02": {
        "titre": "Colinéarité de deux vecteurs et alignement de trois points",
        "pourquoi": "La colinéarité figure parmi les priorités du dossier ; c'est le critère utilisé toute l'année pour l'alignement, le parallélisme et l'équation de droite.",
        "rappel": r"""\begin{methodbox}
\textbf{Un seul calcul.} Les vecteurs $\vec{u}(x\,;y)$ et $\vec{v}(x'\,;y')$ sont colinéaires si et seulement si
le \textbf{déterminant} $xy' - yx'$ est nul.
\par\smallskip
Trois points $A$, $B$, $C$ sont alignés si et seulement si $\vec{AB}$ et $\vec{AC}$ sont colinéaires.
\textbf{Contrôle :} deux vecteurs colinéaires ont le même coefficient directeur, lorsqu'il existe.
\end{methodbox}""",
        "exemple": r"""\textbf{Exemple guidé.} Les vecteurs $\vec{u}(2\,;-3)$ et $\vec{v}(-4\,;6)$ sont-ils colinéaires ?
\begin{enumerate}
\item Calculer le déterminant : $2\times 6 - (-3)\times(-4)$.
\item Soit $12 - 12 = 0$.
\item Conclusion : les vecteurs sont colinéaires.
\item Contrôle : $\vec{v} = -2\,\vec{u}$, ce qui confirme le résultat.
\end{enumerate}""",
        "exos": [
            {"tex": r"Les vecteurs $\vec{u}(5\,;-2)$ et $\vec{v}(-15\,;6)$ sont-ils colinéaires ? Justifier par le calcul du déterminant.", "space": "lines:2",
             "corrige": r"$5\times 6 - (-2)\times(-15) = 30 - 30 = 0$ : ils sont \textbf{colinéaires}."},
            {"tex": r"Les vecteurs $\vec{u}(4\,;7)$ et $\vec{v}(2\,;3)$ sont-ils colinéaires ?", "space": "lines:2",
             "corrige": r"$4\times 3 - 7\times 2 = 12 - 14 = -2 \neq 0$ : ils ne sont \textbf{pas} colinéaires."},
            {"tex": r"On donne $A(1\,;2)$, $B(4\,;8)$ et $C(-1\,;-2)$. Montrer que ces trois points sont alignés.", "space": "lines:3",
             "corrige": r"$\vec{AB}(3\,;6)$ et $\vec{AC}(-2\,;-4)$ ; déterminant $3\times(-4)-6\times(-2)=-12+12=0$ : les points sont alignés."},
            {"tex": r"Déterminer $k$ pour que $\vec{u}(3\,;k)$ et $\vec{v}(9\,;15)$ soient colinéaires.", "space": "lines:3",
             "corrige": r"$3\times 15 - k\times 9 = 0$ donne $45 = 9k$ donc $k = \mathbf{5}$."},
            {"tex": r"Expliquer en une phrase le lien entre la colinéarité de deux vecteurs directeurs et le coefficient directeur de deux droites.", "space": "lines:2",
             "corrige": r"Deux droites de vecteurs directeurs colinéaires sont parallèles et ont donc le même coefficient directeur."},
            {"tex": r"Un élève conclut que $\vec{u}(2\,;3)$ et $\vec{v}(4\,;5)$ sont colinéaires « car on multiplie par $2$ ». Réfuter par le calcul et expliquer ce qu'il aurait dû vérifier.", "space": "lines:3",
             "corrige": r"$2\times 5 - 3\times 4 = -2 \neq 0$ : ils ne sont pas colinéaires. Le facteur $2$ ne s'applique qu'à la première coordonnée ; il faut vérifier les deux, ou calculer le déterminant."},
        ],
        "erreurs": [{"code": "METHODE", "desc": "conclusion tirée d'une seule coordonnée"},
                    {"code": "CALCUL", "desc": "signe perdu dans le produit $-y\\times x'$"},
                    {"code": "JUSTIFICATION", "desc": "colinéarité affirmée sans calcul du déterminant"}],
        "reussite": "quatre tests de colinéarité corrects consécutifs, dont un alignement de trois points, le déterminant étant écrit à chaque fois.",
    },
}
