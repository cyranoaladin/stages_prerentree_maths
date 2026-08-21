# -*- coding: utf-8 -*-
"""Blueprint du niveau « Entrée en Première générale — Spécialité mathématiques »."""

LEVEL = {
    "key": "1ere_spe",
    "label": "Entrée en Première générale — Spécialité mathématiques",
    "subject": "Mathématiques",
    "prefix": "M1RE",
    "year_prev": "Seconde",
    "year_next": "Première spécialité",
    "source_dir": "1ere_spe",
    "baseline_instrument": {
        "name": "Positionnement de pré-rentrée — Mathématiques, entrée en Première spécialité",
        "file": "1ere_spe/03_EVALUATIONS/1ere_spe_Test_Initial.pdf",
        "items": 18, "minutes": 25, "format": "QCM 4 choix + certitude 1-4",
    },
    "sessions": {
        "S1": "Calcul algébrique, inéquations et transition vers le second degré",
        "S2": "Fonctions, fonctions de référence et première approche de la dérivation",
        "S3": "Vecteurs, droites et transition vers le produit scalaire",
        "S4": "Pourcentages, événements et probabilités conditionnelles",
        "S5": "Suites numériques, Python et évaluation de synthèse",
    },
    "skills": {
        "M1RE_ALG_01": {"label": "Développement et identités remarquables",
                        "domain": "Calcul algébrique", "importance_n": "critique",
                        "baseline_items": ["1S_TI_Q01"], "sessions": ["S1"]},
        "M1RE_ALG_02": {"label": "Factorisation, en particulier la différence de deux carrés",
                        "domain": "Calcul algébrique", "importance_n": "critique",
                        "baseline_items": ["1S_TI_Q02"], "sessions": ["S1"]},
        "M1RE_INEQ_01": {"label": "Inéquation du premier degré et écriture en intervalle",
                         "domain": "Inéquations", "importance_n": "critique",
                         "baseline_items": ["1S_TI_Q03"], "sessions": ["S1"]},
        "M1RE_INEQ_02": {"label": "Signe d'un produit et tableau de signes",
                         "domain": "Inéquations", "importance_n": "critique",
                         "baseline_items": ["1S_TI_Q04"], "sessions": ["S1"]},
        "M1RE_FONC_01": {"label": "Image d'un réel, substitution d'une valeur négative",
                         "domain": "Fonctions", "importance_n": "critique",
                         "baseline_items": ["1S_TI_Q05"], "sessions": ["S2"]},
        "M1RE_FONC_02": {"label": "Langage des fonctions : image, antécédent, appartenance à la courbe",
                         "domain": "Fonctions", "importance_n": "critique",
                         "baseline_items": ["1S_TI_Q06"], "sessions": ["S2"]},
        "M1RE_FREF_01": {"label": "Fonctions de référence : carré et inverse, variations",
                         "domain": "Fonctions de référence", "importance_n": "importante",
                         "baseline_items": ["1S_TI_Q07"], "sessions": ["S2"]},
        "M1RE_FREF_02": {"label": "Comparaison de x² et de x selon la position de x",
                         "domain": "Fonctions de référence", "importance_n": "importante",
                         "baseline_items": ["1S_TI_Q08"], "sessions": ["S2"]},
        "M1RE_VECT_01": {"label": "Coordonnées d'un vecteur défini par deux points",
                         "domain": "Vecteurs", "importance_n": "critique",
                         "baseline_items": ["1S_TI_Q09"], "sessions": ["S3"]},
        "M1RE_VECT_02": {"label": "Colinéarité de deux vecteurs",
                         "domain": "Vecteurs", "importance_n": "critique",
                         "baseline_items": ["1S_TI_Q10"], "sessions": ["S3"]},
        "M1RE_DROIT_01": {"label": "Coefficient directeur d'une droite",
                          "domain": "Droites", "importance_n": "critique",
                          "baseline_items": ["1S_TI_Q11"], "sessions": ["S3"]},
        "M1RE_DROIT_02": {"label": "Lecture d'une équation réduite de droite",
                          "domain": "Droites", "importance_n": "importante",
                          "baseline_items": ["1S_TI_Q12"], "sessions": ["S3"]},
        "M1RE_POURC_01": {"label": "Taux d'évolution",
                          "domain": "Pourcentages", "importance_n": "critique",
                          "baseline_items": ["1S_TI_Q13"], "sessions": ["S4"]},
        "M1RE_POURC_02": {"label": "Coefficient multiplicateur et évolutions successives",
                          "domain": "Pourcentages", "importance_n": "critique",
                          "baseline_items": ["1S_TI_Q14"], "sessions": ["S4"]},
        "M1RE_PROBA_01": {"label": "Union, intersection et formule P(A∪B)",
                          "domain": "Probabilités", "importance_n": "importante",
                          "baseline_items": ["1S_TI_Q15"], "sessions": ["S4"]},
        "M1RE_PROBA_02": {"label": "Événement contraire",
                          "domain": "Probabilités", "importance_n": "importante",
                          "baseline_items": ["1S_TI_Q16"], "sessions": ["S4"]},
        "M1RE_NUM_01": {"label": "Calcul avec des puissances",
                        "domain": "Calcul numérique", "importance_n": "importante",
                        "baseline_items": ["1S_TI_Q17"], "sessions": ["S1"]},
        "M1RE_NUM_02": {"label": "Simplification d'un radical",
                        "domain": "Calcul numérique", "importance_n": "importante",
                        "baseline_items": ["1S_TI_Q18"], "sessions": ["S1"]},
    },
    "baseline_items": {
        "1S_TI_Q01": "Développer et réduire (2x − 3)².",
        "1S_TI_Q02": "Factoriser x² − 9.",
        "1S_TI_Q03": "Résoudre −2x + 6 ≥ 0.",
        "1S_TI_Q04": "Pour quelles valeurs de x le produit (2x − 6)(x + 1) est-il strictement négatif ?",
        "1S_TI_Q05": "f(x) = x² − 3x : que vaut f(−2) ?",
        "1S_TI_Q06": "La courbe de f passe par (3 ; 7). On peut affirmer que :",
        "1S_TI_Q07": "La fonction inverse f(x) = 1/x est :",
        "1S_TI_Q08": "Soit x tel que 0 < x < 1. Que peut-on affirmer ?",
        "1S_TI_Q09": "A(1 ; 2) et B(4 ; −3) : coordonnées du vecteur AB ?",
        "1S_TI_Q10": "Les vecteurs u(2 ; −3) et v(−4 ; 6) sont :",
        "1S_TI_Q11": "Coefficient directeur de la droite passant par A(1 ; 3) et B(4 ; 9) ?",
        "1S_TI_Q12": "La droite d'équation y = −3x + 5 :",
        "1S_TI_Q13": "Un article passait de 120 à 90 dinars : pourcentage de réduction ?",
        "1S_TI_Q14": "Coefficient multiplicateur d'une baisse de 15 % ?",
        "1S_TI_Q15": "Dé équilibré, A « nombre pair » et B « nombre supérieur à … » : union/intersection.",
        "1S_TI_Q16": "Événement contraire de « obtenir au moins un six » sur deux lancers ?",
        "1S_TI_Q17": "Simplifier (2³ × 2⁵)/2⁴.",
        "1S_TI_Q18": "Écriture simplifiée de √50.",
    },
    "curriculum_reference": {
        "annee_scolaire_visee": "2026-2027",
        "programme_applique_a_l_eleve": {
            "cycle": "lycée général, spécialité mathématiques de Première",
            "texte": "nouveau programme de la spécialité mathématiques de Première",
            "BO": "BO n° 14 du 2 avril 2026",
            "NOR": "MENE2602917A",
            "entree_en_vigueur": "rentrée 2026-2027",
            "nouvelle_progression_applicable": True,
        },
        "transition": "acquis de Seconde 2025-2026 vers le nouveau programme de spécialité de "
                      "Première applicable en 2026-2027",
        "attendus_de_fin_annee_n_moins_1": "Seconde",
        "source_de_la_reference": "audit indépendant du 21 août 2026, section 9 ; à confirmer "
                                  "auprès du Bulletin officiel avant diffusion externe",
        "verifie_par_un_humain": False,
    },
    "critical_prereqs": ["M1RE_ALG_01", "M1RE_ALG_02", "M1RE_INEQ_01", "M1RE_INEQ_02",
                         "M1RE_FONC_01", "M1RE_FONC_02", "M1RE_VECT_01", "M1RE_VECT_02",
                         "M1RE_DROIT_01", "M1RE_POURC_01", "M1RE_POURC_02"],
    "n_bridges": [
        "suite définie par récurrence à partir d'une évolution en pourcentage",
        "taux de variation moyen d'une fonction, préparation du nombre dérivé",
        "second degré : forme développée, forme factorisée, signe",
    ],
    "phase1": {
        "objectif": "Réactiver les cinq blocs du stage (algèbre, fonctions, vecteurs, droites, pourcentages) avant la phase de consolidation.",
        "consigne": r"Sept minutes seules, sans document, puis trois minutes de mise en commun. Écrire la réponse \emph{et} le contrôle utilisé.",
        "items": [
            {"skill": "M1RE_ALG_02", "tex": r"Factoriser $9x^2 - 25$.", "space": "short",
             "corrige": r"$(3x)^2-5^2=\mathbf{(3x-5)(3x+5)}$. Contrôle : développer redonne $9x^2-25$."},
            {"skill": "M1RE_INEQ_01", "tex": r"Résoudre $-4x + 10 \ge 0$ et donner l'ensemble des solutions sous forme d'intervalle.", "space": "short",
             "corrige": r"$-4x\ge -10$ donc $x\le \frac52$ : $S=\left]-\infty\,;\tfrac52\right]$ (sens de l'inégalité changé)."},
            {"skill": "M1RE_FONC_01", "tex": r"Pour $f(x)=x^2-5x$, calculer $f(-3)$ en écrivant la substitution complète.", "space": "short",
             "corrige": r"$f(-3)=(-3)^2-5\times(-3)=9+15=\mathbf{24}$."},
            {"skill": "M1RE_VECT_01", "tex": r"$A(-2\,;5)$ et $B(3\,;-1)$ : donner les coordonnées de $\vec{AB}$, puis le coefficient directeur de $(AB)$.", "space": "short",
             "corrige": r"$\vec{AB}(3-(-2)\,;-1-5)=\mathbf{(5\,;-6)}$ ; coefficient directeur $=\frac{-6}{5}=\mathbf{-1{,}2}$."},
            {"skill": "M1RE_POURC_01", "tex": r"Un prix passe de $250$ TND à $210$ TND. Calculer le taux d'évolution en pourcentage.", "space": "short",
             "corrige": r"$\frac{210-250}{250}=-0{,}16$, soit une baisse de $\mathbf{16\,\%}$."},
        ],
    },
    "phase4": {
        "titre": "De la Seconde à la Première : la suite et le taux de variation",
        "objectif": "Découverte guidée : construire, à partir des évolutions en pourcentage et du coefficient directeur déjà travaillés, deux notions nouvelles de Première — la suite géométrique définie par récurrence et le taux de variation moyen.",
        "contenu_nouveau_annee_n": True,
        "skills_prev": ["M1RE_POURC_02", "M1RE_DROIT_01", "M1RE_FONC_01"],
        "skills_next": ["suite définie par récurrence", "taux de variation moyen"],
        "tex": r"""
\begin{methodbox}
\textbf{Ce qui change en Première.} Deux objets \textbf{nouveaux} s'appuient sur des acquis de Seconde.
\par\smallskip
Une \textbf{suite} est une liste ordonnée de nombres indexée par les entiers. Toutes les suites ne décrivent
pas une évolution répétée ; en revanche, \emph{certaines} d'entre elles, notamment les \textbf{suites
géométriques}, modélisent exactement cela — c'est le cas étudié ci-dessous.
\par\smallskip
Le \textbf{taux de variation} d'une fonction entre deux points de sa courbe se calcule comme le coefficient
directeur de la droite qui les joint. C'est cette lecture qui conduira, en Première, au nombre dérivé.
\end{methodbox}
\begin{warningbox}\small
\textbf{Cette phase introduit des notions de l'année à venir.} Ce que tu produis ici ne sera donc
\emph{pas} comparé à ton positionnement de début de stage : il ne s'agit pas de mesurer un progrès,
mais de préparer les premières séances de septembre.
\end{warningbox}


\subsectiontitle{A. De l'évolution à la suite — 8 min}
Un capital de $2\,000$ TND est placé à $3\,\%$ par an. On note $u_n$ le capital au bout de $n$ années.
\begin{enumerate}
\item Donner le coefficient multiplicateur annuel. \rule{35mm}{0.32pt} \quad Écrire $u_0$. \rule{28mm}{0.32pt}
\item Écrire la relation qui donne $u_{n+1}$ en fonction de $u_n$. \rule{55mm}{0.32pt}
\item Calculer $u_1$ et $u_2$ (arrondir au centime).
\shortlines{2}
\item Compléter le programme Python ci-dessous, qui affiche $u_0$ puis les cinq termes suivants.
\begin{lstlisting}
u = 2000
print(0, u)
for n in range(5):
    u = _______________________
    print(________, u)
\end{lstlisting}
\par\vspace{0.5mm}
Sans la ligne \code{print(0, u)}, quels termes le programme afficherait-il ? \rule{45mm}{0.32pt}
\item Le capital dépasse-t-il $2\,200$ TND au bout de trois ans ? Répondre par un calcul.
\shortlines{2}
\end{enumerate}

\subsectiontitle{B. Du coefficient directeur au taux de variation — 7 min}
Soit $f$ la fonction définie par $f(x) = x^2$.
\begin{enumerate}
\item Calculer le coefficient directeur de la droite passant par les points de la courbe d'abscisses $1$ et $3$.
\shortlines{1}
\item Recommencer avec les abscisses $1$ et $1{,}5$, puis $1$ et $1{,}1$.
\par\noindent\begin{tabularx}{\linewidth}{|>{\bfseries}p{40mm}|X|X|X|}
\hline
Second point d'abscisse & $3$ & $1{,}5$ & $1{,}1$ \\ \hline
Taux de variation & & & \\ \hline
\end{tabularx}
\item De quel nombre ces taux semblent-ils se rapprocher ? \rule{40mm}{0.32pt}
\item Écrire une phrase expliquant ce que ce nombre décrira en Première.
\worklines{1}
\end{enumerate}

\begin{successbox}
\textbf{Preuve attendue :} la relation de récurrence est écrite avec $u_{n+1}$ et $u_n$, et le taux de variation
est calculé comme un quotient de deux différences, dans le bon ordre.
\end{successbox}
""",
        "corrige": r"""
\textbf{A.} 1. Coefficient $1{,}03$ ; $u_0=2000$. \quad 2. $u_{n+1}=1{,}03\,u_n$.
3. $u_1=2060$ ; $u_2=2121{,}80$. \quad 4. \code{u = 1.03 * u} puis \code{print(n + 1, u)}.
La ligne \code{print(0, u)} placée \emph{avant} la boucle affiche $u_0$ ; sans elle, le programme
afficherait seulement $u_1$ à $u_5$, car l'affectation précède l'affichage à chaque tour.
5. $u_3=2000\times 1{,}03^3\approx 2185{,}45 < 2200$ : non, le seuil n'est pas atteint en trois ans.

\textbf{B.} 1. $\frac{f(3)-f(1)}{3-1}=\frac{9-1}{2}=4$.
2. $\frac{2{,}25-1}{0{,}5}=2{,}5$ ; $\frac{1{,}21-1}{0{,}1}=2{,}1$.
3. Les taux se rapprochent de $2$.
4. Attendu : ce nombre décrira la pente de la tangente à la courbe au point d'abscisse $1$ ; c'est le nombre dérivé.

\textbf{Observation à noter :} écrire $u_{n+1}=u_n+3$ est une erreur de \textsc{CONCEPT} (évolution additive
au lieu d'une évolution multiplicative) ; inverser numérateur et dénominateur du taux de variation est une
erreur de \textsc{METHODE}.
""",
    },
    "eval_common": {
        "A1": {"skill": "M1RE_ALG_02", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Factoriser $16x^2 - 49$.",
               "answer": r"$(4x - 7)(4x + 7)$",
               "steps": [r"reconnaître $a^2-b^2$ avec $a=4x$ et $b=7$"],
               "errors": [{"code": "CONCEPT", "desc": "$(4x-7)^2$ : différence de carrés confondue avec un carré parfait"},
                          {"code": "CALCUL", "desc": "racine de $16x^2$ prise égale à $16x$"}],
               "criteria": [{"points": 1, "desc": "factorisation exacte"}],
               "baseline_item": "1S_TI_Q02", "comparability": "comparable",
               "role_rentree": "outil direct du second degré et des études de signe"},
        "A2": {"skill": "M1RE_INEQ_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Résoudre $-3x + 12 > 0$ et donner l'ensemble des solutions sous forme d'intervalle.",
               "answer": r"$x < 4$, soit $S = \left]-\infty\,;4\right[$",
               "steps": [r"$-3x > -12$", r"division par $-3$ : le sens de l'inégalité change", r"$x<4$"],
               "errors": [{"code": "CONCEPT", "desc": "sens de l'inégalité conservé après division par un négatif"},
                          {"code": "NOTATION", "desc": "crochet fermé sur une inégalité stricte"}],
               "criteria": [{"points": 1, "desc": "solution et intervalle exacts"}],
               "baseline_item": "1S_TI_Q03", "comparability": "comparable",
               "role_rentree": "prérequis des tableaux de signes du second degré"},
        "A3": {"skill": "M1RE_FONC_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Soit $g(x) = 2x^2 + x$. Calculer $g(-3)$ en écrivant la substitution complète.",
               "answer": r"$15$",
               "steps": [r"$g(-3)=2\times(-3)^2+(-3)$", r"$=2\times 9-3=15$"],
               "errors": [{"code": "NOTATION", "desc": "parenthèses omises : $-3^2$ traité comme $-9$"},
                          {"code": "CALCUL", "desc": "$2\\times 9$ mal évalué"}],
               "criteria": [{"points": 1, "desc": "$15$ exact avec la substitution visible"}],
               "baseline_item": "1S_TI_Q05", "comparability": "comparable",
               "role_rentree": "substitution employée en permanence en dérivation et sur les suites"},
        "A4": {"skill": "M1RE_VECT_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"On donne $A(4\,;-1)$ et $B(-2\,;5)$. Déterminer les coordonnées de $\vec{AB}$.",
               "answer": r"$\vec{AB}(-6\,;6)$",
               "steps": [r"$x_B-x_A=-2-4=-6$", r"$y_B-y_A=5-(-1)=6$"],
               "errors": [{"code": "CONCEPT", "desc": "soustraction effectuée dans l'ordre $A-B$"},
                          {"code": "CALCUL", "desc": "$5-(-1)$ traité comme $4$"}],
               "criteria": [{"points": 1, "desc": "les deux coordonnées exactes"}],
               "baseline_item": "1S_TI_Q09", "comparability": "comparable",
               "role_rentree": "prérequis du produit scalaire et de la géométrie repérée"},
        "B1": {"skill": "M1RE_INEQ_02", "points": 2, "minutes": 5, "task": "application",
               "difficulty": "standard", "space": "lines:6",
               "tex": r"""On considère le produit $P(x) = (3x + 6)(2 - x)$.
\begin{enumerate}
\item Déterminer les valeurs de $x$ qui annulent chaque facteur.
\item Construire un tableau de signes, puis donner l'ensemble des $x$ pour lesquels $P(x) > 0$.
\item En déduire, à partir du même tableau, l'ensemble des $x$ pour lesquels $P(x) \leqslant 0$.
\end{enumerate}""",
               "answer": r"Racines $-2$ et $2$ ; $P(x)>0$ sur $\left]-2\,;2\right[$ ; $P(x)\leqslant 0$ sur $\left]-\infty\,;-2\right]\cup\left[2\,;+\infty\right[$.",
               "steps": [r"$3x+6=0 \Leftrightarrow x=-2$ ; $2-x=0 \Leftrightarrow x=2$",
                         r"$3x+6$ négatif avant $-2$, positif après ; $2-x$ positif avant $2$, négatif après",
                         r"produit positif entre les deux racines"],
               "errors": [{"code": "CONCEPT", "desc": "signe de $2-x$ traité comme celui de $x-2$"},
                          {"code": "METHODE", "desc": "tableau de signes non construit alors qu'il est explicitement demandé, le signe étant annoncé sans justification"},
                          {"code": "NOTATION", "desc": "bornes incluses alors que l'inégalité est stricte"}],
               "criteria": [{"points": 0.75, "desc": "racines exactes et tableau complet"},
                            {"points": 0.75, "desc": "ensemble solution exact, bornes correctement ouvertes"},
                            {"points": 0.5, "desc": "ensemble complémentaire exact, bornes fermées incluses"}],
               "baseline_item": "1S_TI_Q04", "comparability": "comparable",
               "role_rentree": "méthode reprise telle quelle pour le signe du trinôme"},
        "B2": {"skill": "M1RE_FONC_02", "skills_extra": ["M1RE_FREF_02"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:6", "confidence": True,
               "tex": r"""\begin{enumerate}
\item La courbe représentative d'une fonction $f$ passe par le point de coordonnées $(-2\,;5)$.
Traduire cette information en employant les mots « image » et « antécédent ».
\item Soit $x$ un réel tel que $0 < x < 1$. Comparer $x^2$ et $x$, puis justifier la réponse
par un exemple numérique et par un argument valable pour tout $x$ de cet intervalle.
\end{enumerate}""",
               "answer": r"$5$ est l'image de $-2$ par $f$ ; $-2$ est un antécédent de $5$. Pour $0<x<1$, $x^2<x$.",
               "steps": [r"$f(-2)=5$",
                         r"exemple : $x=0{,}5$ donne $x^2=0{,}25<0{,}5$",
                         r"argument : $x^2-x=x(x-1)$ avec $x>0$ et $x-1<0$, donc $x^2-x<0$"],
               "errors": [{"code": "CONCEPT", "desc": "image et antécédent échangés"},
                          {"code": "CONCEPT", "desc": "$x^2>x$ affirmé par généralisation du cas $x>1$"},
                          {"code": "JUSTIFICATION", "desc": "un seul exemple donné, sans argument général"}],
               "criteria": [{"points": 1, "desc": "vocabulaire correct dans les deux sens"},
                            {"points": 1, "desc": "comparaison exacte, appuyée sur un exemple et un argument"}],
               "baseline_item": "1S_TI_Q08", "comparability": "comparable",
               "role_rentree": "langage fonctionnel utilisé dans tous les chapitres de Première"},
        "B3": {"skill": "M1RE_POURC_02", "skills_extra": ["M1RE_POURC_01"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""Un abonnement coûte $480$ TND. Son prix baisse de $25\,\%$, puis le nouveau prix
augmente de $20\,\%$.
\begin{enumerate}
\item Calculer le prix après chaque étape.
\item Donner le coefficient multiplicateur global, puis le taux d'évolution global en pourcentage.
\end{enumerate}""",
               "answer": r"$360$ TND puis $432$ TND ; coefficient global $0{,}9$, soit une baisse globale de $10\,\%$.",
               "steps": [r"$480\times 0{,}75=360$", r"$360\times 1{,}2=432$",
                         r"$0{,}75\times 1{,}2=0{,}9$ soit $-10\,\%$"],
               "errors": [{"code": "METHODE", "desc": "$-25\\,\\%$ et $+20\\,\\%$ additionnés en $-5\\,\\%$"},
                          {"code": "CONCEPT", "desc": "coefficient d'une baisse de $25\\,\\%$ pris égal à $0{,}25$"},
                          {"code": "CALCUL", "desc": "produit $0{,}75\\times 1{,}2$ mal évalué alors que la méthode est correcte"}],
               "criteria": [{"points": 0.75, "desc": "les deux prix exacts"},
                            {"points": 0.75, "desc": "coefficient global et taux global exacts"},
                            {"points": 0.5, "desc": "conclusion exacte, justifiée par la comparaison du coefficient global à 1"}],
               "baseline_item": "1S_TI_Q14", "comparability": "comparable",
               "role_rentree": "base des suites géométriques et de l'évolution en pourcentage"},
        "C1": {"skill": "M1RE_DROIT_01",
               "skills_extra": ["M1RE_VECT_02", "M1RE_PROBA_01", "M1RE_POURC_02"],
               "points": 4, "minutes": 10, "task": "transfert", "difficulty": "transfert",
               "space": "lines:12", "confidence": True,
               "tex": r"""\textbf{Le club sportif.} Dans un repère du plan, on donne $A(1\,;2)$ et $B(5\,;10)$.
\begin{enumerate}
\item Déterminer le coefficient directeur de la droite $(AB)$, puis une équation réduite de $(AB)$.
\item Le point $C(-3\,;-6)$ appartient-il à $(AB)$ ? Justifier par un calcul, en indiquant la méthode choisie.
\item Le club compte $60$ membres : $24$ pratiquent la natation, $30$ la course, et $12$ pratiquent les deux.
On choisit un membre au hasard. Calculer la probabilité qu'il pratique la natation ou la course,
puis la probabilité qu'il ne pratique pas la natation.
\item La cotisation, de $180$ TND, augmente de $4\,\%$ par an. On note $u_0 = 180$. Écrire la relation liant
$u_{n+1}$ et $u_n$, puis calculer $u_2$ arrondi au dinar.
\end{enumerate}""",
               "answer": r"$m=2$ et $y=2x$ ; $C$ appartient à $(AB)$ ; $P(N\cup C)=0{,}7$ et $P(\overline{N})=0{,}6$ ; $u_{n+1}=1{,}04\,u_n$ et $u_2\approx 195$ TND.",
               "steps": [r"$m=\frac{10-2}{5-1}=2$ ; $y=2x+p$ avec $2=2\times 1+p$ donc $p=0$",
                         r"$2\times(-3)=-6$ : les coordonnées de $C$ vérifient l'équation (ou $\vec{AB}(4\,;8)$ et $\vec{AC}(-4\,;-8)$ sont colinéaires)",
                         r"$P(N)=0{,}4$, $P(C)=0{,}5$, $P(N\cap C)=0{,}2$ donc $P(N\cup C)=0{,}4+0{,}5-0{,}2=0{,}7$",
                         r"$P(\overline{N})=1-0{,}4=0{,}6$",
                         r"$u_{n+1}=1{,}04\,u_n$ ; $u_2=180\times 1{,}04^2=194{,}688\approx 195$"],
               "errors": [{"code": "CALCUL", "desc": "ordonnée à l'origine non déterminée, équation laissée en $y=2x+p$"},
                          {"code": "CONCEPT", "desc": "$P(N\\cup C)$ obtenue en additionnant sans retirer l'intersection"},
                          {"code": "CONCEPT", "desc": "$u_{n+1}=u_n+4$ : évolution additive au lieu de multiplicative"},
                          {"code": "JUSTIFICATION", "desc": "appartenance de $C$ affirmée sans calcul"}],
               "criteria": [{"points": 1, "desc": "coefficient directeur et équation réduite exacts"},
                            {"points": 1, "desc": "appartenance justifiée par un calcul explicite"},
                            {"points": 1, "desc": "les deux probabilités exactes, intersection correctement retirée"},
                            {"points": 1, "desc": "relation de récurrence correcte et $u_2$ exact"}],
               "baseline_item": None, "comparability": "partiellement_comparable",
               "role_rentree": "quatre entrées de Première mobilisées sur une même situation ; la question 4 s'appuie sur la phase 4 de la séance"},
    },
}
