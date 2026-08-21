# -*- coding: utf-8 -*-
"""Blueprint du niveau « Entrée en Troisième — Mathématiques »."""

LEVEL = {
    "key": "3e",
    "label": "Entrée en Troisième",
    "subject": "Mathématiques",
    "prefix": "M3E",
    "year_prev": "Quatrième",
    "year_next": "Troisième",
    "source_dir": "3e",
    "baseline_instrument": {
        "name": "Positionnement de pré-rentrée — Mathématiques, entrée en Troisième",
        "file": "3e/03_EVALUATIONS/3e_Test_Initial.pdf",
        "items": 18, "minutes": 25, "format": "QCM 4 choix + certitude 1-4",
    },
    "sessions": {
        "S1": "Sécuriser le moteur numérique (nombres, fractions, puissances)",
        "S2": "Passer du calcul à l'algèbre (calcul littéral, équations)",
        "S3": "Construire et justifier (Pythagore, Thalès)",
        "S4": "Choisir un rapport trigonométrique",
        "S5": "Lire les données et mobiliser l'ensemble des acquis",
    },
    "skills": {
        "M3E_REL_01": {"label": "Produit, quotient et priorités avec des nombres relatifs",
                       "domain": "Nombres relatifs", "importance_n": "critique",
                       "baseline_items": ["3E_TI_Q01", "3E_TI_Q02"], "sessions": ["S1"]},
        "M3E_FRAC_01": {"label": "Somme et différence de fractions",
                        "domain": "Fractions", "importance_n": "critique",
                        "baseline_items": ["3E_TI_Q03"], "sessions": ["S1"]},
        "M3E_FRAC_02": {"label": "Produit et quotient de fractions, simplification",
                        "domain": "Fractions", "importance_n": "critique",
                        "baseline_items": ["3E_TI_Q04"], "sessions": ["S1"]},
        "M3E_PUIS_01": {"label": "Puissances : calcul et produit de puissances de même base",
                        "domain": "Puissances", "importance_n": "importante",
                        "baseline_items": ["3E_TI_Q05", "3E_TI_Q06"], "sessions": ["S1"]},
        "M3E_LIT_01": {"label": "Distributivité : développer k(ax+b)",
                       "domain": "Calcul littéral", "importance_n": "critique",
                       "baseline_items": ["3E_TI_Q07"], "sessions": ["S2"]},
        "M3E_LIT_02": {"label": "Réduction d'une expression avec constantes signées",
                       "domain": "Calcul littéral", "importance_n": "critique",
                       "baseline_items": ["3E_TI_Q08"], "sessions": ["S2"]},
        "M3E_EQ_01": {"label": "Équation du premier degré, inconnue dans les deux membres",
                      "domain": "Équations", "importance_n": "critique",
                      "baseline_items": ["3E_TI_Q09", "3E_TI_Q10"], "sessions": ["S2"]},
        "M3E_PROP_01": {"label": "Proportionnalité : quatrième proportionnelle et vitesse",
                        "domain": "Proportionnalité", "importance_n": "critique",
                        "baseline_items": ["3E_TI_Q11", "3E_TI_Q12"], "sessions": ["S2", "S5"]},
        "M3E_GEO_01": {"label": "Théorème de Pythagore : calcul d'une longueur",
                       "domain": "Géométrie", "importance_n": "critique",
                       "baseline_items": ["3E_TI_Q13", "3E_TI_Q14"], "sessions": ["S3"]},
        "M3E_TRIG_01": {"label": "Choix et emploi d'un rapport trigonométrique (cosinus, sinus)",
                        "domain": "Trigonométrie", "importance_n": "critique",
                        "baseline_items": ["3E_TI_Q15", "3E_TI_Q16"], "sessions": ["S4"]},
        "M3E_STAT_01": {"label": "Moyenne simple et moyenne pondérée",
                        "domain": "Statistiques", "importance_n": "importante",
                        "baseline_items": ["3E_TI_Q17", "3E_TI_Q18"], "sessions": ["S5"]},
    },
    "baseline_items": {
        "3E_TI_Q01": "Calculer (−5) × (−3).",
        "3E_TI_Q02": "Calculer (−12) ÷ 4 + (−2) × (−3).",
        "3E_TI_Q03": "Calculer 3/5 − 1/2.",
        "3E_TI_Q04": "Calculer 2/3 × 9/4.",
        "3E_TI_Q05": "Calculer 2⁵.",
        "3E_TI_Q06": "Écrire 3⁴ × 3² sous la forme d'une seule puissance.",
        "3E_TI_Q07": "Développer 3(2x − 5).",
        "3E_TI_Q08": "Réduire l'expression 4x − 7 + 2x + 3.",
        "3E_TI_Q09": "Résoudre l'équation 2x + 3 = 11.",
        "3E_TI_Q10": "Résoudre l'équation 5x − 2 = 3x + 8.",
        "3E_TI_Q11": "4 stylos identiques coûtent 6 dinars. Combien coûtent 10 stylos ?",
        "3E_TI_Q12": "Une voiture parcourt 150 km en 2 h : quelle distance en 5 h ?",
        "3E_TI_Q13": "ABC rectangle en A, AB = 6 cm, AC = 8 cm : longueur BC ?",
        "3E_TI_Q14": "ABC rectangle en A, BC = 13 cm, AB = 5 cm : longueur AC ?",
        "3E_TI_Q15": "Dans ABC rectangle en A, le cosinus de l'angle B est égal à :",
        "3E_TI_Q16": "Côté adjacent 4 cm, hypoténuse 8 cm : mesure de l'angle B ?",
        "3E_TI_Q17": "Moyenne de la série 8 ; 12 ; 10 ; 14.",
        "3E_TI_Q18": "12 (coefficient 1) et 8 (coefficient 3) : moyenne pondérée ?",
    },
    "curriculum_reference": {
        "annee_scolaire_visee": "2026-2027",
        "programme_applique_a_l_eleve": {
            "cycle": "cycle 4",
            "texte": "programme de cycle 4 en vigueur pour la classe de Troisième en 2026-2027",
            "remarque": "le nouveau programme de cycle 4 publié en 2026 s'applique progressivement : "
                        "Cinquième en 2026-2027, Quatrième en 2027-2028, Troisième en 2028-2029. "
                        "Les élèves entrant en Troisième à la rentrée 2026 ne relèvent donc PAS de "
                        "la nouvelle progression.",
            "nouvelle_progression_applicable": False,
            "annee_d_application_pour_ce_niveau": "2028-2029",
        },
        "transition": "acquis de Quatrième 2025-2026 vers la Troisième 2026-2027",
        "attendus_de_fin_annee_n_moins_1": "Quatrième",
        "source_de_la_reference": "audit indépendant du 21 août 2026, section 9 ; à confirmer "
                                  "auprès du Bulletin officiel avant diffusion externe",
        "verifie_par_un_humain": False,
    },
    "critical_prereqs": ["M3E_REL_01", "M3E_FRAC_02", "M3E_LIT_01", "M3E_LIT_02",
                         "M3E_EQ_01", "M3E_PROP_01", "M3E_GEO_01", "M3E_TRIG_01"],
    "n_bridges": [
        "double distributivité (a+b)(c+d) et amorce des identités remarquables",
        "notion de fonction : image, antécédent, tableau de valeurs",
        "théorème de Thalès et agrandissement-réduction",
    ],
    "phase1": {
        "objectif": "Réactiver les cinq domaines du stage et repérer immédiatement les automatismes qui se sont dégradés.",
        "consigne": r"Sept minutes seules, sans carte de rappel, puis trois minutes de mise en commun. Écrire la réponse \emph{et} le contrôle utilisé.",
        "items": [
            {"skill": "M3E_REL_01", "tex": r"Calculer $(-6)\times(-4) + (-3)\times 5$.", "space": "short",
             "corrige": r"$24 + (-15) = \mathbf{9}$. Contrôle : deux facteurs de même signe donnent un produit positif."},
            {"skill": "M3E_FRAC_02", "tex": r"Calculer $\dfrac{3}{4}\times\dfrac{8}{9}$ et donner le résultat simplifié.", "space": "short",
             "corrige": r"$\frac{3\times 8}{4\times 9}=\frac{24}{36}=\mathbf{\frac{2}{3}}$ (ou simplification avant le produit)."},
            {"skill": "M3E_LIT_02", "tex": r"Réduire $5x - 8 + 3x + 2$, puis contrôler pour $x = 1$.", "space": "short",
             "corrige": r"$8x-6$. Contrôle : $5-8+3+2=2$ et $8\times 1-6=2$."},
            {"skill": "M3E_GEO_01", "tex": r"$ABC$ est rectangle en $A$ avec $AB = 9$ cm et $AC = 12$ cm. Calculer $BC$ en citant le théorème.", "space": "short",
             "corrige": r"Pythagore : $BC^2=9^2+12^2=81+144=225$, donc $BC=\mathbf{15}$ cm."},
            {"skill": "M3E_STAT_01", "tex": r"Calculer la moyenne de la série $7$ ; $11$ ; $9$ ; $13$, puis vérifier qu'elle est comprise entre le minimum et le maximum.", "space": "short",
             "corrige": r"$\frac{40}{4}=\mathbf{10}$ ; $7 < 10 < 13$ : contrôle concluant."},
        ],
    },
    "phase4": {
        "titre": "De la Quatrième à la Troisième : le double produit et l'entrée dans les fonctions",
        "objectif": "Découverte guidée : construire, à partir de la distributivité et des équations déjà travaillées, deux notions nouvelles de Troisième — le double produit et le vocabulaire des fonctions.",
        "contenu_nouveau_annee_n": True,
        "skills_prev": ["M3E_LIT_01", "M3E_LIT_02", "M3E_EQ_01"],
        "skills_next": ["double distributivité", "image et antécédent d'une fonction"],
        "tex": r"""
\begin{methodbox}
\textbf{Ce qui change en Troisième.} Deux éléments sont à distinguer nettement.
\par\smallskip
\textbf{Ce qui est réinvesti} — et qui a été travaillé de la séance 1 à la séance 4 : la distributivité
$k(a+b)$, la réduction d'une expression, la résolution d'une équation du premier degré, le calcul d'une aire.
\par\smallskip
\textbf{Ce qui est nouveau} — et qui appartient au programme de Troisième : le \textbf{double produit}
$(a+b)(c+d)$, et le \textbf{statut de fonction} donné à une expression littérale, avec le vocabulaire
« image » et « antécédent ». Les deux blocs ci-dessous construisent ces deux nouveautés à partir des acquis
énumérés ci-dessus.
\end{methodbox}
\begin{warningbox}\small
\textbf{Cette phase introduit des notions de l'année à venir.} Ce que tu produis ici ne sera donc
\emph{pas} comparé à ton positionnement de début de stage : il ne s'agit pas de mesurer un progrès,
mais de préparer les premières séances de septembre.
\end{warningbox}


\subsectiontitle{A. Du rectangle au double produit — 7 min}
Un rectangle a pour longueur $x+3$ et pour largeur $x+2$. On le découpe en quatre parties.
\begin{center}
\begin{tikzpicture}[x=1cm,y=1cm]
\draw[fill=SoftBlue] (0,0) rectangle (3,2);
\draw[fill=SoftGold] (3,0) rectangle (4.5,2);
\draw[fill=SoftGray] (0,2) rectangle (3,3);
\draw[fill=green!8] (3,2) rectangle (4.5,3);
\draw[thick] (0,0) rectangle (4.5,3);
\node at (1.5,1) {$x \times x$};
\node at (3.75,1) {$3 \times x$};
\node at (1.5,2.5) {$2 \times x$};
\node at (3.75,2.5) {$3\times 2$};
\node[below] at (1.5,0) {$x$};
\node[below] at (3.75,0) {$3$};
\node[left] at (0,1) {$x$};
\node[left] at (0,2.5) {$2$};
\end{tikzpicture}
\end{center}
\begin{enumerate}
\item Écrire l'aire totale sous la forme d'un produit : \rule{55mm}{0.32pt}
\item Écrire l'aire totale comme la somme des quatre parties, puis réduire.
\shortlines{2}
\item Contrôler l'égalité obtenue pour $x = 4$ : les deux écritures doivent donner le même nombre.
\shortlines{1}
\item Développer de la même manière $(x+5)(x+1)$.
\shortlines{1}
\end{enumerate}

\subsectiontitle{B. D'un programme de calcul à une fonction — 8 min}
Programme : « choisir un nombre, le multiplier par $2$, puis retrancher $3$ ».
\begin{enumerate}
\item Écrire l'expression obtenue en partant de $x$. On la note $f(x)$. \rule{45mm}{0.32pt}
\item Calculer $f(5)$. On dit que $7$ est \rule{28mm}{0.32pt} de $5$ par $f$. \quad Calculer $f(-2)$.
\shortlines{1}
\item Quel nombre faut-il choisir pour obtenir $9$ ? Écrire l'équation, la résoudre, puis conclure :
$6$ est \rule{28mm}{0.32pt} de $9$ par $f$.
\worklines{2}
\item Compléter le tableau de valeurs.
\end{enumerate}
\par\noindent\begin{tabularx}{\linewidth}{|>{\bfseries}p{18mm}|X|X|X|X|X|}
\hline
$x$ & $-2$ & $0$ & $1$ & $3$ & $5$ \\ \hline
$f(x)$ & & & & & \\ \hline
\end{tabularx}

\begin{successbox}
\textbf{Preuve attendue :} les mots « image » et « antécédent » sont employés au bon endroit, et le calcul
d'un antécédent passe par une équation, non par un essai au hasard.
\end{successbox}
""",
        "corrige": r"""
\textbf{A.} 1. $(x+3)(x+2)$. \quad 2. $x^2 + 2x + 3x + 6 = x^2 + 5x + 6$.
3. $x=4$ : $(4+3)(4+2)=7\times 6=42$ et $16+20+6=42$. \quad 4. $(x+5)(x+1)=x^2+x+5x+5=x^2+6x+5$.

\textbf{B.} 1. $f(x)=2x-3$. \quad 2. $f(5)=7$ : $7$ est l'\textbf{image} de $5$ ; $f(-2)=-7$.
3. $2x-3=9$ donc $2x=12$ et $x=6$ : $6$ est un \textbf{antécédent} de $9$.
4. Tableau : $-7$ ; $-3$ ; $-1$ ; $3$ ; $7$.

\textbf{Observation à noter :} confondre image et antécédent est une erreur de \textsc{CONCEPT} ;
chercher l'antécédent par essais successifs sans écrire l'équation est une erreur de \textsc{METHODE}.
""",
    },
    "eval_common": {
        "A1": {"skill": "M3E_REL_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Calculer $(-15) \div 3 + (-2)\times(-6)$.",
               "answer": r"$7$",
               "steps": [r"$(-15)\div 3=-5$", r"$(-2)\times(-6)=12$", r"$-5+12=7$"],
               "errors": [{"code": "CONCEPT", "desc": "règle des signes non appliquée sur le produit ($-12$)"},
                          {"code": "METHODE", "desc": "opérations effectuées de gauche à droite sans priorité"}],
               "criteria": [{"points": 1, "desc": "résultat $7$ exact"}],
               "baseline_item": "3E_TI_Q02", "comparability": "comparable",
               "role_rentree": "socle de tout calcul algébrique de Troisième"},
        "A2": {"skill": "M3E_FRAC_02", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Calculer $\dfrac{4}{5}\times\dfrac{15}{8}$ et donner le résultat simplifié.",
               "answer": r"$\dfrac{3}{2}$",
               "steps": [r"$\frac{4\times 15}{5\times 8}=\frac{60}{40}$", r"simplification par $20$ : $\frac{3}{2}$"],
               "errors": [{"code": "CONCEPT", "desc": "produit en croix : $\\frac{4\\times 8}{5\\times 15}$"},
                          {"code": "METHODE", "desc": "réduction au même dénominateur avant un produit"}],
               "criteria": [{"points": 1, "desc": "$\\frac{3}{2}$ ou $1{,}5$ exact"}],
               "baseline_item": "3E_TI_Q04", "comparability": "comparable",
               "role_rentree": "calcul fractionnaire exigé en permanence en Troisième"},
        "A3": {"skill": "M3E_LIT_02", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Réduire $9x - 4 - 5x - 7$.",
               "answer": r"$4x - 11$",
               "steps": [r"$9x-5x=4x$", r"$-4-7=-11$"],
               "errors": [{"code": "CONCEPT", "desc": "$-4-7$ traité comme $-3$ ou $+11$"},
                          {"code": "CONCEPT", "desc": "$4x$ et $-11$ regroupés"}],
               "criteria": [{"points": 1, "desc": "$4x-11$ exact"}],
               "baseline_item": "3E_TI_Q08", "comparability": "comparable",
               "role_rentree": "prérequis de la factorisation et des identités remarquables"},
        "A4": {"skill": "M3E_EQ_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "lines:2",
               "tex": r"Résoudre l'équation $4x - 3 = 2x + 9$.",
               "answer": r"$x = 6$",
               "steps": [r"$4x-2x=9+3$", r"$2x=12$", r"$x=6$"],
               "errors": [{"code": "CONCEPT", "desc": "signe non changé lors du passage d'un membre à l'autre"},
                          {"code": "CALCUL", "desc": "$2x=12$ mal résolu alors que le regroupement est correct"}],
               "criteria": [{"points": 1, "desc": "$x=6$ avec au moins une étape écrite"}],
               "baseline_item": "3E_TI_Q10", "comparability": "comparable",
               "role_rentree": "prérequis des équations produit et des systèmes"},
        "B1": {"skill": "M3E_GEO_01", "points": 2, "minutes": 5, "task": "application",
               "difficulty": "standard", "space": "lines:5",
               "tex": r"""Le triangle $ABC$ est rectangle en $A$. On donne $BC = 20$ cm et $AB = 12$ cm.
\begin{enumerate}
\item Calculer $AC$ en citant le théorème utilisé et en écrivant la relation avant les nombres.
\item Vérifier la vraisemblance du résultat : $AC$ doit-elle être plus petite ou plus grande que $BC$ ? Pourquoi ?
\end{enumerate}""",
               "answer": r"$AC = 16$ cm ; $AC < BC$ car l'hypoténuse est le plus grand côté.",
               "steps": [r"$BC^2 = AB^2 + AC^2$", r"$400 = 144 + AC^2$", r"$AC^2 = 256$ donc $AC = 16$"],
               "errors": [{"code": "CONCEPT", "desc": "$20^2 + 12^2$ additionnés : l'hypoténuse n'est pas identifiée"},
                          {"code": "JUSTIFICATION", "desc": "théorème non cité"},
                          {"code": "CALCUL", "desc": "racine carrée de 256 erronée"}],
               "criteria": [{"points": 1.5, "desc": "relation correcte, théorème cité, $AC=16$ cm"},
                            {"points": 0.5, "desc": "contrôle de vraisemblance argumenté"}],
               "baseline_item": "3E_TI_Q14", "comparability": "comparable",
               "role_rentree": "base de Thalès, de la trigonométrie et du repérage en Troisième"},
        "B2": {"skill": "M3E_TRIG_01", "points": 2, "minutes": 5, "task": "application",
               "difficulty": "standard", "space": "lines:5", "confidence": True,
               "tex": r"""Le triangle $ABC$ est rectangle en $A$. On donne $AB = 5$ cm et $BC = 13$ cm.
\begin{enumerate}
\item Par rapport à l'angle $\widehat{B}$, nommer chacun des côtés $AB$ et $BC$.
\item En déduire $\cos\widehat{B}$, puis la mesure de $\widehat{B}$ arrondie au degré.
\item Si l'on connaissait le côté opposé à $\widehat{B}$ et l'hypoténuse, quel rapport faudrait-il utiliser ?
\end{enumerate}""",
               "answer": r"$AB$ : côté adjacent ; $BC$ : hypoténuse ; $\cos\widehat{B}=\frac{5}{13}\approx 0{,}3846$ donc $\widehat{B}\approx 67^\circ$ ; il faudrait le sinus.",
               "steps": [r"identification des côtés relativement à l'angle $\widehat{B}$",
                         r"$\cos\widehat{B}=\frac{\text{adjacent}}{\text{hypoténuse}}=\frac{5}{13}$",
                         r"$\widehat{B}=\arccos(5/13)\approx 67^\circ$"],
               "errors": [{"code": "CONCEPT", "desc": "cosinus et sinus échangés"},
                          {"code": "LECTURE", "desc": "côté adjacent identifié par rapport au mauvais angle"},
                          {"code": "CALCUL", "desc": "arrondi ou emploi de la calculatrice en radians"}],
               "criteria": [{"points": 1, "desc": "côtés correctement nommés et rapport correct"},
                            {"points": 0.5, "desc": "mesure de l'angle exacte au degré près"},
                            {"points": 0.5, "desc": "sinus identifié à la question 3"}],
               "baseline_item": "3E_TI_Q16", "comparability": "comparable",
               "role_rentree": "trigonométrie réinvestie dès les premiers chapitres de Troisième"},
        "B3": {"skill": "M3E_PROP_01", "skills_extra": ["M3E_STAT_01"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""\begin{enumerate}
\item Un train parcourt $210$ km en $1$ h $30$ min à vitesse constante. Calculer sa vitesse moyenne en km/h.
\item Un élève obtient $14$ (coefficient $2$) et $9$ (coefficient $3$). Calculer sa moyenne pondérée, puis vérifier
qu'elle est comprise entre $9$ et $14$.
\end{enumerate}""",
               "answer": r"$140$ km/h ; moyenne pondérée $=\frac{28+27}{5}=11$, comprise entre $9$ et $14$.",
               "steps": [r"$1$ h $30$ min $=1{,}5$ h ; $210 \div 1{,}5 = 140$",
                         r"$14\times 2 + 9\times 3 = 55$ ; $55 \div 5 = 11$"],
               "errors": [{"code": "CONCEPT", "desc": "$1$ h $30$ converti en $1{,}30$ h"},
                          {"code": "METHODE", "desc": "moyenne pondérée calculée comme une moyenne simple ($11{,}5$)"},
                          {"code": "LECTURE", "desc": "division par 2 au lieu de la somme des coefficients"}],
               "criteria": [{"points": 1, "desc": "vitesse exacte, conversion visible"},
                            {"points": 1, "desc": "moyenne pondérée exacte et encadrement écrit"}],
               "baseline_item": "3E_TI_Q18", "comparability": "comparable",
               "role_rentree": "grandeurs quotients et statistiques, réinvesties toute l'année"},
        "C1": {"skill": "M3E_GEO_01",
               "skills_extra": ["M3E_TRIG_01", "M3E_PROP_01", "M3E_LIT_01"],
               "points": 4, "minutes": 10, "task": "transfert", "difficulty": "transfert",
               "space": "lines:12", "confidence": True,
               "tex": r"""\textbf{La rampe d'accès.} Une rampe d'accès s'appuie sur une longueur au sol de $4{,}8$ m
et atteint une hauteur de $1{,}4$ m. Le triangle formé est rectangle.
\begin{enumerate}
\item Calculer la longueur de la rampe en citant le théorème utilisé.
\item Calculer la mesure de l'angle formé par la rampe et le sol, arrondie au degré.
\item La réglementation impose une pente d'au plus $5\,\%$, la pente étant le quotient de la hauteur par la
longueur au sol. Calculer la pente en pourcentage, puis conclure.
\item Le coût de fabrication est donné par $C(x) = 85x + 120$ TND, où $x$ est la longueur de la rampe en mètres.
Calculer $C$ pour la rampe étudiée et expliquer ce que représente le nombre $120$.
\end{enumerate}""",
               "answer": r"$5$ m ; environ $16^\circ$ ; pente $\approx 29{,}2\,\% > 5\,\%$ : non conforme ; $C(5)=545$ TND, $120$ est la part fixe.",
               "steps": [r"$4{,}8^2+1{,}4^2=23{,}04+1{,}96=25$ donc longueur $=5$ m",
                         r"$\cos\alpha = \frac{4{,}8}{5}=0{,}96$ donc $\alpha\approx 16^\circ$",
                         r"$1{,}4 \div 4{,}8 \approx 0{,}2917 = 29{,}2\,\%$, très supérieur à $5\,\%$",
                         r"$C(5)=85\times 5+120=425+120=545$ TND ; $120$ ne dépend pas de la longueur"],
               "errors": [{"code": "TRANSFERT", "desc": "la pente est confondue avec l'angle en degrés"},
                          {"code": "CONCEPT", "desc": "cosinus appliqué avec l'hypoténuse au numérateur"},
                          {"code": "JUSTIFICATION", "desc": "conclusion sur la conformité absente ou non chiffrée"},
                          {"code": "CONCEPT", "desc": "$120$ interprété comme un coût par mètre"}],
               "criteria": [{"points": 1, "desc": "longueur exacte, théorème cité"},
                            {"points": 1, "desc": "angle exact au degré près, rapport correctement choisi"},
                            {"points": 1, "desc": "pente exprimée en pourcentage et conclusion explicite"},
                            {"points": 1, "desc": "$C(5)$ exact et rôle du terme constant correctement expliqué"}],
               "baseline_item": None, "comparability": "partiellement_comparable",
               "role_rentree": "tâche complexe type brevet : plusieurs domaines, une décision à justifier"},
    },
}
