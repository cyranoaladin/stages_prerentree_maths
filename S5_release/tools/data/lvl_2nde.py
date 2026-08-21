# -*- coding: utf-8 -*-
"""Blueprint du niveau « Entrée en Seconde générale et technologique — Mathématiques »."""

LEVEL = {
    "key": "2nde",
    "label": "Entrée en Seconde générale et technologique",
    "subject": "Mathématiques",
    "prefix": "M2DE",
    "year_prev": "Troisième",
    "year_next": "Seconde",
    "source_dir": "2nde",
    "baseline_instrument": {
        "name": "Positionnement de pré-rentrée — Mathématiques, entrée en Seconde",
        "file": "2nde/03_EVALUATIONS/2nde_Test_Initial.pdf",
        "items": 18, "minutes": 25, "format": "QCM 4 choix + certitude 1-4",
    },
    "sessions": {
        "S1": "Réparer le moteur de calcul (priorités, fractions, puissances)",
        "S2": "Construire l'algèbre du lycée (développement, factorisation, équations)",
        "S3": "Modéliser une situation (pourcentages, fonctions)",
        "S4": "Choisir le bon théorème (Pythagore, Thalès, trigonométrie)",
        "S5": "Relier, contrôler et expliquer (statistiques, probabilités, algorithmique)",
    },
    "skills": {
        "M2DE_CALC_01": {"label": "Priorités opératoires, signes et puissance d'un relatif",
                         "domain": "Calcul numérique", "importance_n": "critique",
                         "baseline_items": ["2N_TI_Q01", "2N_TI_Q02"], "sessions": ["S1"]},
        "M2DE_FRAC_01": {"label": "Somme et quotient de fractions",
                         "domain": "Fractions", "importance_n": "critique",
                         "baseline_items": ["2N_TI_Q03", "2N_TI_Q04"], "sessions": ["S1"]},
        "M2DE_PUIS_01": {"label": "Puissances de 10, exposants négatifs, écriture scientifique",
                         "domain": "Puissances", "importance_n": "critique",
                         "baseline_items": ["2N_TI_Q05", "2N_TI_Q06"], "sessions": ["S1"]},
        "M2DE_ALG_01": {"label": "Double distributivité et identités remarquables",
                        "domain": "Calcul littéral", "importance_n": "critique",
                        "baseline_items": ["2N_TI_Q07", "2N_TI_Q08"], "sessions": ["S2"]},
        "M2DE_EQ_01": {"label": "Équation du premier degré, inconnue dans les deux membres",
                       "domain": "Équations", "importance_n": "critique",
                       "baseline_items": ["2N_TI_Q09"], "sessions": ["S2"]},
        "M2DE_EQ_02": {"label": "Équation produit nul",
                       "domain": "Équations", "importance_n": "critique",
                       "baseline_items": ["2N_TI_Q10"], "sessions": ["S2"]},
        "M2DE_POURC_01": {"label": "Pourcentages, coefficient multiplicateur, évolutions successives",
                          "domain": "Proportionnalité", "importance_n": "critique",
                          "baseline_items": ["2N_TI_Q11", "2N_TI_Q12"], "sessions": ["S3"]},
        "M2DE_GEO_01": {"label": "Théorème de Pythagore, direct et réciproque",
                        "domain": "Géométrie", "importance_n": "critique",
                        "baseline_items": ["2N_TI_Q13", "2N_TI_Q14"], "sessions": ["S4"]},
        "M2DE_GEO_02": {"label": "Théorème de Thalès et agrandissement-réduction",
                        "domain": "Géométrie", "importance_n": "importante",
                        "baseline_items": ["2N_TI_Q15", "2N_TI_Q16"], "sessions": ["S4"]},
        "M2DE_TRIG_01": {"label": "Rapports trigonométriques dans le triangle rectangle",
                         "domain": "Trigonométrie", "importance_n": "importante",
                         "baseline_items": ["2N_TI_Q17", "2N_TI_Q18"], "sessions": ["S4"]},
    },
    "baseline_items": {
        "2N_TI_Q01": "Calculer −3 + 4 × (−2).",
        "2N_TI_Q02": "Calculer (−2)³.",
        "2N_TI_Q03": "Calculer 2/3 + 1/4.",
        "2N_TI_Q04": "Calculer (3/4) ÷ (2/5).",
        "2N_TI_Q05": "Simplifier 10³ × 10⁻⁵.",
        "2N_TI_Q06": "Écriture scientifique de 0,00034.",
        "2N_TI_Q07": "Développer et réduire (x + 3)(x − 5).",
        "2N_TI_Q08": "Développer (x − 4)².",
        "2N_TI_Q09": "Résoudre 3x − 7 = 2x + 5.",
        "2N_TI_Q10": "Résoudre (x − 2)(x + 5) = 0.",
        "2N_TI_Q11": "Un article coûte 80 dinars et augmente de 15 % : nouveau prix ?",
        "2N_TI_Q12": "Un prix baisse de 20 %, puis augmente de 20 % : que vaut le prix final ?",
        "2N_TI_Q13": "ABC rectangle en A, AB = 3 cm, AC = 4 cm : longueur BC ?",
        "2N_TI_Q14": "Un triangle a pour côtés 6, 8 et 10 cm : que peut-on affirmer ?",
        "2N_TI_Q15": "Configuration de Thalès : AM = 2, AB = 6, AN = 3, calculer AC.",
        "2N_TI_Q16": "Agrandissement de rapport 3 : par combien l'aire est-elle multipliée ?",
        "2N_TI_Q17": "Dans ABC rectangle en A, le cosinus de l'angle B est égal à :",
        "2N_TI_Q18": "Hypoténuse 10 cm, angle aigu 30° : longueur du côté opposé ?",
    },
    "curriculum_reference": {
        "annee_scolaire_visee": "2026-2027",
        "programme_applique_a_l_eleve": {
            "cycle": "lycée général et technologique, classe de Seconde",
            "texte": "nouveau programme de mathématiques de Seconde",
            "BO": "BO n° 14 du 2 avril 2026",
            "NOR": "MENE2602914A",
            "entree_en_vigueur": "rentrée 2026-2027",
            "nouvelle_progression_applicable": True,
        },
        "transition": "acquis de Troisième 2025-2026, relevant du programme de cycle 4 alors en "
                      "vigueur, vers le nouveau programme de Seconde applicable dès 2026-2027",
        "attendus_de_fin_annee_n_moins_1": "Troisième",
        "source_de_la_reference": "audit indépendant du 21 août 2026, section 9 ; à confirmer "
                                  "auprès du Bulletin officiel avant diffusion externe",
        "verifie_par_un_humain": False,
    },
    "critical_prereqs": ["M2DE_CALC_01", "M2DE_FRAC_01", "M2DE_PUIS_01", "M2DE_ALG_01",
                         "M2DE_EQ_01", "M2DE_EQ_02", "M2DE_POURC_01", "M2DE_GEO_01"],
    "n_bridges": [
        "intervalles de réels et ensembles de nombres",
        "notion de fonction : image, antécédent, tableau de valeurs, courbe",
        "repérage dans le plan et algorithmique en Python",
    ],
    "phase1": {
        "objectif": "Réactiver les automatismes de calcul et d'algèbre qui conditionnent les premières semaines de Seconde.",
        "consigne": r"Sept minutes seules, sans carte de rappel, puis trois minutes de mise en commun. Écrire la réponse \emph{et} le contrôle utilisé.",
        "items": [
            {"skill": "M2DE_CALC_01", "tex": r"Calculer $-5 + 3\times(-4) - (-2)$.", "space": "short",
             "corrige": r"$-5 + (-12) + 2 = \mathbf{-15}$. Le produit se calcule avant les additions."},
            {"skill": "M2DE_FRAC_01", "tex": r"Calculer $\dfrac{5}{6}\div\dfrac{10}{9}$ et simplifier.", "space": "short",
             "corrige": r"$\frac{5}{6}\times\frac{9}{10}=\frac{45}{60}=\mathbf{\frac{3}{4}}$."},
            {"skill": "M2DE_ALG_01", "tex": r"Développer et réduire $(x-3)(x+7)$.", "space": "short",
             "corrige": r"$x^2+7x-3x-21=\mathbf{x^2+4x-21}$. Contrôle pour $x=1$ : $(-2)\times 8=-16$ et $1+4-21=-16$."},
            {"skill": "M2DE_EQ_02", "tex": r"Résoudre $(3x-6)(x+4)=0$.", "space": "short",
             "corrige": r"Un produit est nul si l'un des facteurs est nul : $x=\mathbf{2}$ ou $x=\mathbf{-4}$."},
            {"skill": "M2DE_PUIS_01", "tex": r"Écrire $0{,}00058$ en notation scientifique.", "space": "short",
             "corrige": r"$\mathbf{5{,}8\times 10^{-4}}$ : un seul chiffre non nul avant la virgule."},
        ],
    },
    "phase4": {
        "titre": "De la Troisième à la Seconde : intervalles et langage des fonctions",
        "objectif": "Découverte guidée : construire, à partir du calcul et des équations déjà travaillés, deux notations nouvelles de Seconde — l'intervalle et le langage des fonctions.",
        "contenu_nouveau_annee_n": True,
        "skills_prev": ["M2DE_EQ_01", "M2DE_ALG_01", "M2DE_CALC_01"],
        "skills_next": ["intervalles de réels", "image, antécédent, tableau de valeurs"],
        "tex": r"""
\begin{methodbox}
\textbf{Ce qui change en Seconde.} Deux outils \textbf{nouveaux} apparaissent dès les premières semaines :
l'\textbf{intervalle}, qui remplace les phrases du type « $x$ est compris entre... », et le \textbf{langage
des fonctions}, qui donne un statut nouveau aux expressions littérales déjà manipulées.
\par\smallskip
\textbf{Ce qui est réinvesti} : le calcul numérique, la substitution et l'équation produit nul, travaillés
en séances 1 et 2. \textbf{Ce qui est nouveau} : la notation en intervalle et le vocabulaire fonctionnel.
Les deux blocs ci-dessous sont donc une \textbf{découverte guidée}, non un réemploi.
\end{methodbox}
\begin{warningbox}\small
\textbf{Cette phase introduit des notions de l'année à venir.} Ce que tu produis ici ne sera donc
\emph{pas} comparé à ton positionnement de début de stage : il ne s'agit pas de mesurer un progrès,
mais de préparer les premières séances de septembre.
\end{warningbox}


\subsectiontitle{A. De l'inégalité à l'intervalle — 6 min}
\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{40mm} X X}
\toprule
Phrase & Inégalité & Intervalle \\
\midrule
$x$ est strictement supérieur à $2$ & & \\
$x$ est inférieur ou égal à $5$ & & \\
$x$ est compris entre $-2$ (inclus) et $3$ (exclu) & & \\
$x$ est un nombre quelconque & & \\
\bottomrule
\end{tabularx}
\par\vspace{1.5mm}
Placer ensuite sur l'axe l'ensemble $[-2\,;3[$ en marquant clairement les bornes ouvertes et fermées.
\begin{center}
\begin{tikzpicture}[x=1cm]
\draw[->,thick] (-5,0) -- (5,0);
\foreach \x in {-4,-3,-2,-1,0,1,2,3,4}{\draw (\x,0.12) -- (\x,-0.12) node[below]{\small $\x$};}
\end{tikzpicture}
\end{center}

\subsectiontitle{B. D'un programme de calcul à une fonction — 9 min}
Programme : « choisir un nombre, l'élever au carré, puis retrancher le triple du nombre ».
\begin{enumerate}
\item Écrire l'expression obtenue en partant de $x$ ; on la note $f(x)$. \rule{50mm}{0.32pt}
\item Calculer $f(4)$ et $f(-2)$ en écrivant la substitution complète, parenthèses comprises.
\shortlines{2}
\item Compléter le tableau de valeurs.
\end{enumerate}
\par\noindent\begin{tabularx}{\linewidth}{|>{\bfseries}p{18mm}|X|X|X|X|X|X|}
\hline
$x$ & $-2$ & $-1$ & $0$ & $1$ & $3$ & $4$ \\ \hline
$f(x)$ & & & & & & \\ \hline
\end{tabularx}
\begin{enumerate}\setcounter{enumi}{3}
\item Déterminer un antécédent de $0$ par $f$ en écrivant une équation produit nul.
\worklines{2}
\item Vrai ou faux : « le point de coordonnées $(3\,;0)$ appartient à la courbe de $f$ ». Justifier par un calcul.
\shortlines{1}
\end{enumerate}

\begin{successbox}
\textbf{Preuve attendue :} la substitution d'un nombre négatif est écrite avec des parenthèses, et l'antécédent
est obtenu par une équation, non par lecture approximative.
\end{successbox}
""",
        "corrige": r"""
\textbf{A.} $x>2 \to \left]2\,;+\infty\right[$ ; $x\le 5 \to \left]-\infty\,;5\right]$ ;
$-2\le x<3 \to [-2\,;3[$ ; $x$ quelconque $\to \mathbb{R}=\left]-\infty\,;+\infty\right[$.
Sur l'axe : crochet fermé en $-2$, crochet ouvert en $3$.

\textbf{B.} 1. $f(x)=x^2-3x$. \quad 2. $f(4)=16-12=4$ ; $f(-2)=(-2)^2-3\times(-2)=4+6=10$.
3. Tableau : $10$ ; $4$ ; $0$ ; $-2$ ; $0$ ; $4$.
4. $x^2-3x=0$ s'écrit $x(x-3)=0$, donc $x=0$ ou $x=3$ : deux antécédents de $0$.
5. Vrai : $f(3)=9-9=0$.

\textbf{Observation à noter :} oublier les parenthèses dans $(-2)^2$ est une erreur de \textsc{NOTATION}
qui produit une erreur de \textsc{CALCUL} ; ne trouver qu'un seul antécédent de $0$ est une erreur de \textsc{METHODE}.
""",
    },
    "eval_common": {
        "A1": {"skill": "M2DE_CALC_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Calculer $-4 + 5\times(-3) - (-6)$.",
               "answer": r"$-13$",
               "steps": [r"$5\times(-3)=-15$", r"$-4-15+6=-13$"],
               "errors": [{"code": "METHODE", "desc": "calcul de gauche à droite : $(-4+5)\\times(-3)$"},
                          {"code": "CONCEPT", "desc": "$-(-6)$ traité comme $-6$"}],
               "criteria": [{"points": 1, "desc": "$-13$ exact"}],
               "baseline_item": "2N_TI_Q01", "comparability": "comparable",
               "role_rentree": "socle du calcul algébrique et de l'étude de signes en Seconde"},
        "A2": {"skill": "M2DE_FRAC_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Calculer $\dfrac{3}{8} + \dfrac{5}{12}$.",
               "answer": r"$\dfrac{19}{24}$",
               "steps": [r"dénominateur commun $24$", r"$\frac{9}{24}+\frac{10}{24}=\frac{19}{24}$"],
               "errors": [{"code": "CONCEPT", "desc": "numérateurs et dénominateurs additionnés séparément"},
                          {"code": "CALCUL", "desc": "facteur de conversion appliqué au seul dénominateur"}],
               "criteria": [{"points": 1, "desc": "$\\frac{19}{24}$ exact"}],
               "baseline_item": "2N_TI_Q03", "comparability": "comparable",
               "role_rentree": "calcul exact exigé en Seconde, y compris avec des lettres"},
        "A3": {"skill": "M2DE_PUIS_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Simplifier $\dfrac{10^{5}\times 10^{-2}}{10^{4}}$ et donner le résultat sous la forme d'une puissance de $10$.",
               "answer": r"$10^{-1}$",
               "steps": [r"$10^{5}\times 10^{-2}=10^{3}$", r"$10^{3}\div 10^{4}=10^{-1}$"],
               "errors": [{"code": "CONCEPT", "desc": "exposants multipliés au lieu d'être additionnés"},
                          {"code": "CALCUL", "desc": "signe de l'exposant négatif perdu"}],
               "criteria": [{"points": 1, "desc": "$10^{-1}$ (ou $0{,}1$) exact"}],
               "baseline_item": "2N_TI_Q05", "comparability": "comparable",
               "role_rentree": "notation scientifique utilisée en physique et en statistiques dès septembre"},
        "A4": {"skill": "M2DE_ALG_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Développer $(x - 5)^2$.",
               "answer": r"$x^2 - 10x + 25$",
               "steps": [r"$(a-b)^2=a^2-2ab+b^2$", r"$x^2-2\times 5x+25$"],
               "errors": [{"code": "CONCEPT", "desc": "double produit oublié : $x^2+25$"},
                          {"code": "CALCUL", "desc": "signe du double produit erroné"}],
               "criteria": [{"points": 1, "desc": "$x^2-10x+25$ exact"}],
               "baseline_item": "2N_TI_Q08", "comparability": "comparable",
               "role_rentree": "identité indispensable à la forme canonique et à la factorisation"},
        "B1": {"skill": "M2DE_EQ_01", "skills_extra": ["M2DE_EQ_02"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""\begin{enumerate}
\item Résoudre $5x - 8 = 2x + 7$, puis vérifier la solution.
\item Résoudre $(2x + 7)(x - 3) = 0$ en indiquant la propriété utilisée.
\item Vérifier la solution entière de cette seconde équation.
\end{enumerate}""",
               "answer": r"$x=5$ (vérification : $17=17$) ; $x=-3{,}5$ ou $x=3$ ; vérification de $x=3$ : $(2\times 3+7)(3-3)=13\times 0=0$.",
               "steps": [r"$5x-2x=7+8$ donc $3x=15$ et $x=5$",
                         r"vérification : $5\times 5-8=17$ et $2\times 5+7=17$",
                         r"produit nul : $2x+7=0$ ou $x-3=0$"],
               "errors": [{"code": "CONCEPT", "desc": "une seule solution donnée pour l'équation produit"},
                          {"code": "JUSTIFICATION", "desc": "propriété du produit nul non nommée alors qu'elle est demandée"},
                          {"code": "CONTROLE", "desc": "vérification demandée à la question 1 mais non effectuée"}],
               "methodes_alternatives_acceptees": [
                   "développer $(2x+7)(x-3)$ puis résoudre l'équation obtenue : la méthode est mathématiquement "
                   "valide, seulement moins directe. Elle reçoit la totalité des points si les deux solutions "
                   "sont exactes et si la propriété est nommée"],
               "criteria": [{"points": 0.75, "desc": "$x=5$ et vérification écrite"},
                            {"points": 0.75, "desc": "les deux solutions exactes et propriété nommée, quelle que soit la méthode"},
                            {"points": 0.5, "desc": "vérification de la solution entière conduite jusqu'au produit nul"}],
               "baseline_item": "2N_TI_Q10", "comparability": "comparable",
               "role_rentree": "outil de base pour les équations du second degré et les études de signe"},
        "B2": {"skill": "M2DE_POURC_01", "points": 2, "minutes": 5, "task": "application",
               "difficulty": "standard", "space": "lines:5", "confidence": True,
               "tex": r"""Un article coûte $250$ TND. Son prix augmente de $12\,\%$, puis le nouveau prix baisse de $12\,\%$.
\begin{enumerate}
\item Calculer le prix après chaque étape.
\item Le prix final est-il égal au prix initial ? Justifier à l'aide du coefficient multiplicateur global.
\end{enumerate}""",
               "answer": r"$280$ TND puis $246{,}40$ TND ; $1{,}12\times 0{,}88=0{,}9856 \neq 1$ : le prix final est inférieur de $1{,}44\,\%$.",
               "steps": [r"$250\times 1{,}12=280$", r"$280\times 0{,}88=246{,}40$",
                         r"coefficient global $1{,}12\times 0{,}88=0{,}9856$, soit une baisse de $1{,}44\,\%$"],
               "errors": [{"code": "CONCEPT", "desc": "les deux pourcentages compensés : réponse « prix identique »"},
                          {"code": "METHODE", "desc": "coefficients additionnés au lieu d'être multipliés"},
                          {"code": "JUSTIFICATION", "desc": "conclusion donnée sans le coefficient global"}],
               "criteria": [{"points": 1, "desc": "les deux prix intermédiaires exacts"},
                            {"points": 1, "desc": "coefficient global calculé et conclusion argumentée"}],
               "baseline_item": "2N_TI_Q12", "comparability": "comparable",
               "role_rentree": "évolutions successives réutilisées en Seconde puis en Première"},
        "B3": {"skill": "M2DE_GEO_01", "skills_extra": ["M2DE_GEO_02"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""Le triangle $ABC$ est rectangle en $A$, avec $AB = 9$ cm et $AC = 12$ cm.
Le point $M$ appartient à $[AB]$ et le point $N$ à $[AC]$, avec $(MN)$ parallèle à $(BC)$ et $AM = 3$ cm.
\begin{enumerate}
\item Calculer $BC$.
\item Calculer $AN$ et $MN$ en citant le théorème utilisé.
\item En déduire le périmètre du triangle $AMN$.
\end{enumerate}""",
               "answer": r"$BC = 15$ cm ; $AN = 4$ cm ; $MN = 5$ cm ; périmètre de $AMN$ $= 3+4+5 = 12$ cm.",
               "steps": [r"$BC^2=81+144=225$ donc $BC=15$",
                         r"Thalès : $\frac{AM}{AB}=\frac{AN}{AC}=\frac{MN}{BC}=\frac{3}{9}=\frac{1}{3}$",
                         r"$AN=12\times\frac13=4$ ; $MN=15\times\frac13=5$"],
               "errors": [{"code": "METHODE", "desc": "rapport de réduction inversé ($3$ au lieu de $\\frac13$)"},
                          {"code": "JUSTIFICATION", "desc": "théorème de Thalès non cité"},
                          {"code": "LECTURE", "desc": "$AM$ confondu avec $MB$"}],
               "criteria": [{"points": 0.75, "desc": "$BC=15$ cm avec la relation écrite"},
                            {"points": 0.75, "desc": "$AN$ et $MN$ exacts, théorème cité"},
                            {"points": 0.5, "desc": "périmètre exact, avec l'unité"}],
               "baseline_item": "2N_TI_Q15", "comparability": "comparable",
               "role_rentree": "configurations réinvesties en géométrie repérée et en vecteurs"},
        "C1": {"skill": "M2DE_ALG_01",
               "skills_extra": ["M2DE_GEO_01", "M2DE_POURC_01"],
               "points": 4, "minutes": 10, "task": "transfert", "difficulty": "transfert",
               "space": "lines:12", "confidence": True,
               "tex": r"""\textbf{L'écran d'affichage.} Un écran rectangulaire a pour largeur $x$ mètres et pour
hauteur $x - 1$ mètres, avec $x > 1$.
\begin{enumerate}
\item Écrire l'aire $A(x)$ de l'écran, puis la développer et la réduire.
\item Calculer $A(4)$, puis vérifier ce résultat par le calcul direct de l'aire d'un écran de $4$ m sur $3$ m.
\item Calculer la longueur de la diagonale de cet écran de $4$ m sur $3$ m, en citant le théorème utilisé.
\item L'écran est affiché $1\,250$ TND. Une remise de $15\,\%$ est accordée, puis une taxe de $19\,\%$ s'applique
sur le prix remisé. Calculer le prix final, puis dire s'il est supérieur ou inférieur au prix affiché.
Justifier à l'aide du coefficient multiplicateur global.
\end{enumerate}""",
               "answer": r"$A(x)=x(x-1)=x^2-x$ ; $A(4)=12$ ; diagonale $=5$ m ; prix final $=1\,264{,}38$ TND environ, supérieur car $0{,}85\times 1{,}19=1{,}0115>1$.",
               "steps": [r"$A(x)=x(x-1)=x^2-x$",
                         r"$A(4)=16-4=12$ et $4\times 3=12$ : les deux voies concordent",
                         r"$d^2=4^2+3^2=25$ donc $d=5$ m",
                         r"$1250\times 0{,}85=1062{,}50$ puis $\times 1{,}19 = 1264{,}375$",
                         r"$0{,}85\times 1{,}19=1{,}0115>1$ : hausse de $1{,}15\,\%$"],
               "errors": [{"code": "CONCEPT", "desc": "$A(x)$ écrit $x^2-1$ : distributivité appliquée au carré"},
                          {"code": "CONTROLE", "desc": "aucune des deux voies n'est utilisée pour vérifier $A(4)$"},
                          {"code": "METHODE", "desc": "$-15\\,\\%$ et $+19\\,\\%$ additionnés en $+4\\,\\%$"},
                          {"code": "NOTATION", "desc": "unité monétaire absente de la conclusion"}],
               "criteria": [{"points": 1, "desc": "expression développée et réduite exacte"},
                            {"points": 0.5, "desc": "$A(4)$ exact et vérifié par les deux voies"},
                            {"points": 1, "desc": "diagonale exacte, théorème cité"},
                            {"points": 1.5, "desc": "prix final exact, coefficient global et conclusion argumentée"}],
               "baseline_item": None, "comparability": "partiellement_comparable",
               "role_rentree": "modéliser, contrôler par deux voies, décider : conduite attendue en Seconde"},
    },
}
