# -*- coding: utf-8 -*-
"""Blueprint du niveau « Entrée en Quatrième — Mathématiques ».

Sources de vérité :
  - 4e/03_EVALUATIONS/4e_Test_Initial.pdf            (diagnostic initial, 18 items QCM, certitude 1-4)
  - 4e/02_SEANCES/S1..S5/*.md                        (contenus réellement travaillés)
  - 4e/04_NOMINATIFS/<eleve>/4e_Dossier_Individuel_*.md
  - 4e/05_SOURCES/stage_prerentree_quatrieme_maths.md
"""

LEVEL = {
    "key": "4e",
    "label": "Entrée en Quatrième",
    "subject": "Mathématiques",
    "prefix": "M4E",
    "year_prev": "Cinquième",
    "year_next": "Quatrième",
    "source_dir": "4e",
    "baseline_instrument": {
        "name": "Positionnement de pré-rentrée — Mathématiques, entrée en Quatrième",
        "file": "4e/03_EVALUATIONS/4e_Test_Initial.pdf",
        "items": 18, "minutes": 25, "format": "QCM 4 choix + certitude 1-4",
    },
    "sessions": {
        "S1": "Calculer avec du sens (relatifs, fractions)",
        "S2": "Mesurer une surface ou un contour (aires et périmètres)",
        "S3": "Donner du sens aux lettres (calcul littéral)",
        "S4": "Voir, raisonner, démontrer (géométrie)",
        "S5": "Réinvestir, mesurer les progrès et préparer septembre",
    },
    "skills": {
        "M4E_REL_01": {"label": "Somme et différence de relatifs, dont la soustraction d'un négatif",
                       "domain": "Nombres relatifs", "importance_n": "critique",
                       "baseline_items": ["4E_TI_Q01", "4E_TI_Q02"], "sessions": ["S1"]},
        "M4E_REL_02": {"label": "Ordre des relatifs et déplacements sur une droite graduée",
                       "domain": "Nombres relatifs", "importance_n": "critique",
                       "baseline_items": ["4E_TI_Q17", "4E_TI_Q18"], "sessions": ["S1"]},
        "M4E_FRAC_01": {"label": "Somme et différence de fractions de même dénominateur",
                        "domain": "Fractions", "importance_n": "critique",
                        "baseline_items": ["4E_TI_Q03"], "sessions": ["S1"]},
        "M4E_FRAC_02": {"label": "Fractions équivalentes et réduction au même dénominateur",
                        "domain": "Fractions", "importance_n": "critique",
                        "baseline_items": ["4E_TI_Q04"], "sessions": ["S1"]},
        "M4E_LIT_01": {"label": "Distributivité simple : développer k(a+b)",
                       "domain": "Calcul littéral", "importance_n": "critique",
                       "baseline_items": ["4E_TI_Q07"], "sessions": ["S3"]},
        "M4E_LIT_02": {"label": "Réduction d'une expression avec constantes signées",
                       "domain": "Calcul littéral", "importance_n": "critique",
                       "baseline_items": ["4E_TI_Q08"], "sessions": ["S3"]},
        "M4E_GEO_01": {"label": "Somme des angles d'un triangle, triangle rectangle",
                       "domain": "Géométrie", "importance_n": "critique",
                       "baseline_items": ["4E_TI_Q09", "4E_TI_Q10"], "sessions": ["S4"]},
        "M4E_GEO_02": {"label": "Symétrie centrale et caractérisation du parallélogramme",
                       "domain": "Géométrie", "importance_n": "importante",
                       "baseline_items": ["4E_TI_Q13", "4E_TI_Q14"], "sessions": ["S4"]},
        "M4E_AIRE_01": {"label": "Aire et périmètre du rectangle et du triangle, unités",
                        "domain": "Grandeurs et mesures", "importance_n": "critique",
                        "baseline_items": ["4E_TI_Q11", "4E_TI_Q12"], "sessions": ["S2"]},
        "M4E_PROP_01": {"label": "Quatrième proportionnelle et retour à l'unité",
                        "domain": "Proportionnalité", "importance_n": "critique",
                        "baseline_items": ["4E_TI_Q05"], "sessions": ["S2", "S5"]},
        "M4E_PROP_02": {"label": "Pourcentage d'une quantité, fréquence",
                        "domain": "Proportionnalité", "importance_n": "importante",
                        "baseline_items": ["4E_TI_Q06", "4E_TI_Q16"], "sessions": ["S2", "S5"]},
        "M4E_STAT_01": {"label": "Moyenne d'une série et contrôle de vraisemblance",
                        "domain": "Statistiques", "importance_n": "importante",
                        "baseline_items": ["4E_TI_Q15"], "sessions": ["S5"]},
    },
    "baseline_items": {
        "4E_TI_Q01": "Calculer (−7) + (−5).",
        "4E_TI_Q02": "Calculer 3 − (−4) + (−6).",
        "4E_TI_Q03": "Calculer 3/7 + 2/7.",
        "4E_TI_Q04": "Calculer 5/6 − 1/3.",
        "4E_TI_Q05": "5 cahiers identiques coûtent 12 dinars. Combien coûtent 15 cahiers ?",
        "4E_TI_Q06": "Dans une classe de 25 élèves, 20 % sont absents. Combien d'élèves sont absents ?",
        "4E_TI_Q07": "Développer 4(x + 3).",
        "4E_TI_Q08": "Réduire l'expression 5x + 2 + 3x − 6.",
        "4E_TI_Q09": "Dans un triangle, deux angles mesurent 50° et 70°. Mesure du troisième ?",
        "4E_TI_Q10": "Triangle rectangle dont un angle aigu mesure 35° : que vaut l'autre angle aigu ?",
        "4E_TI_Q11": "Aire d'un rectangle de longueur 8 cm et de largeur 5 cm.",
        "4E_TI_Q12": "Aire d'un triangle de base 6 cm et de hauteur 4 cm.",
        "4E_TI_Q13": "Par la symétrie centrale de centre O, l'image d'un segment [AB] est :",
        "4E_TI_Q14": "Un quadrilatère qui admet un centre de symétrie est nécessairement :",
        "4E_TI_Q15": "Moyenne de la série 6 ; 9 ; 12 ; 9.",
        "4E_TI_Q16": "Sur 20 élèves, 8 pratiquent le football : fréquence en pourcentage ?",
        "4E_TI_Q17": "Ranger dans l'ordre croissant : −3 ; 2 ; −7 ; 0.",
        "4E_TI_Q18": "Sur une droite graduée, un point a pour abscisse −4 ; un second est 6 unités à sa droite.",
    },
    "curriculum_reference": {
        "annee_scolaire_visee": "2026-2027",
        "programme_applique_a_l_eleve": {
            "cycle": "cycle 4",
            "texte": "programme de cycle 4 en vigueur pour la classe de Quatrième en 2026-2027",
            "remarque": "un nouveau programme de cycle 4 a été publié en 2026, mais son application "
                        "est progressive : Cinquième en 2026-2027, Quatrième en 2027-2028, "
                        "Troisième en 2028-2029. Les élèves entrant en Quatrième à la rentrée 2026 "
                        "ne relèvent donc PAS de la nouvelle progression.",
            "nouvelle_progression_applicable": False,
            "annee_d_application_pour_ce_niveau": "2027-2028",
        },
        "transition": "acquis de Cinquième 2025-2026 vers la Quatrième 2026-2027",
        "attendus_de_fin_annee_n_moins_1": "Cinquième",
        "source_de_la_reference": "audit indépendant du 21 août 2026, section 9 ; à confirmer "
                                  "auprès du Bulletin officiel avant diffusion externe",
        "verifie_par_un_humain": False,
    },
    "critical_prereqs": [
        "M4E_REL_01", "M4E_REL_02", "M4E_FRAC_02", "M4E_LIT_01",
        "M4E_LIT_02", "M4E_GEO_01", "M4E_AIRE_01", "M4E_PROP_01",
    ],
    "n_bridges": [
        "produit et quotient de nombres relatifs",
        "résolution d'une équation du premier degré ax + b = c",
        "médiane d'une série et événement contraire",
    ],
    # ------------------------------------------------------------------ phases
    "phase1": {
        "objectif": "Remettre en activité sur les cinq domaines du stage et faire apparaître immédiatement les oublis.",
        "consigne": r"Sept minutes seules, sans carte de rappel, puis trois minutes de mise en commun. Écrire la réponse \emph{et} le contrôle utilisé.",
        "items": [
            {"skill": "M4E_REL_01", "tex": r"Calculer $(-9) + 4 - (-6)$.", "space": "short",
             "corrige": r"$-9+4=-5$ puis $-5-(-6)=-5+6=\mathbf{1}$."},
            {"skill": "M4E_FRAC_02", "tex": r"Calculer $\dfrac{7}{10} - \dfrac{2}{5}$ en transformant entièrement la seconde fraction.", "space": "short",
             "corrige": r"$\frac{2}{5}=\frac{4}{10}$ (numérateur \emph{et} dénominateur multipliés par 2), donc $\frac{7}{10}-\frac{4}{10}=\mathbf{\frac{3}{10}}$."},
            {"skill": "M4E_LIT_02", "tex": r"Réduire $6x - 5 + 2x + 9$, puis contrôler pour $x = 1$.", "space": "short",
             "corrige": r"$8x+4$. Contrôle : $6-5+2+9=12$ et $8\times 1+4=12$."},
            {"skill": "M4E_GEO_01", "tex": r"Deux angles d'un triangle mesurent $43^\circ$ et $68^\circ$. Calculer le troisième en citant la propriété.", "space": "short",
             "corrige": r"Somme des angles d'un triangle $=180^\circ$ : $180-(43+68)=\mathbf{69^\circ}$."},
            {"skill": "M4E_AIRE_01", "tex": r"Un rectangle mesure 11 cm sur 6 cm. Donner son aire et son périmètre, unités comprises.", "space": "short",
             "corrige": r"Aire $=11\times 6=\mathbf{66\ \text{cm}^2}$ ; périmètre $=2\times(11+6)=\mathbf{34\ \text{cm}}$."},
        ],
    },
    "phase4": {
        "titre": "De la Cinquième à la Quatrième : le signe d'un produit et la première équation",
        "objectif": "Découverte guidée : construire, à partir d'acquis de Cinquième, deux notions nouvelles de Quatrième — le signe d'un produit de relatifs et l'équation du premier degré.",
        "contenu_nouveau_annee_n": True,
        "skills_prev": ["M4E_REL_01", "M4E_LIT_01", "M4E_LIT_02"],
        "skills_next": ["produit de relatifs", "équation du premier degré"],
        "tex": r"""
\begin{methodbox}
\textbf{Ce qui change en Quatrième.} L'addition et la soustraction des relatifs sont supposées acquises :
elles ont été travaillées en séance 1. La Quatrième y ajoute le \textbf{produit} et le \textbf{quotient} de
relatifs, puis utilise les expressions littérales pour écrire et résoudre des \textbf{équations}.
\par\smallskip
Ces deux notions sont \textbf{nouvelles}. Les blocs ci-dessous ne sont donc pas un réemploi : ce sont deux
\textbf{découvertes guidées}. Chacune part d'un acquis de Cinquième — le sens des signes, l'écriture d'une
expression littérale — pour construire la règle nouvelle pas à pas.
\end{methodbox}
\begin{warningbox}\small
\textbf{Cette phase introduit des notions de l'année à venir.} Ce que tu produis ici ne sera donc
\emph{pas} comparé à ton positionnement de début de stage : il ne s'agit pas de mesurer un progrès,
mais de préparer les premières séances de septembre.
\end{warningbox}


\subsectiontitle{A. Le signe d'un produit — 6 min}
Compléter le tableau, puis écrire la règle en une phrase.
\par\noindent\begin{tabularx}{\linewidth}{>{\bfseries}p{30mm} X >{\bfseries}p{30mm} X}
\toprule
Produit & Résultat & Produit & Résultat \\
\midrule
$3 \times (-4)$ & & $(-3)\times(-4)$ & \\
$(-5)\times 2$ & & $(-5)\times(-2)$ & \\
\bottomrule
\end{tabularx}
\par\vspace{1mm}
Ma règle : \rule{125mm}{0.32pt}
\par\vspace{1mm}
Contrôle demandé : donner un produit de deux nombres dont le résultat est $-12$, puis un autre, différent.
\shortlines{1}

\subsectiontitle{B. Écrire puis résoudre une équation — 9 min}
Une salle est louée $35$ TND, auxquels s'ajoutent $4$ TND par participant.
\begin{enumerate}
\item Écrire l'expression $C(n)$ du coût pour $n$ participants. \rule{60mm}{0.32pt}
\item Calculer $C(12)$ en montrant la substitution.
\shortlines{1}
\item La facture s'élève à $99$ TND. Écrire l'équation correspondante, puis la résoudre en écrivant chaque étape.
\worklines{3}
\item Contrôler la solution trouvée en la remplaçant dans $C(n)$.
\shortlines{1}
\end{enumerate}

\begin{successbox}
\textbf{Preuve attendue :} l'expression est écrite avant tout calcul ; la solution de l'équation est
contrôlée par substitution et non par une simple relecture.
\end{successbox}
""",
        "corrige": r"""
\textbf{A.} $3\times(-4)=-12$ ; $(-3)\times(-4)=12$ ; $(-5)\times 2=-10$ ; $(-5)\times(-2)=10$.
Règle attendue : deux facteurs de \emph{même} signe donnent un produit positif, de signes \emph{contraires}
un produit négatif. Contrôles possibles : $3\times(-4)$ et $(-6)\times 2$, ou $12\times(-1)$.

\textbf{B.} 1. $C(n)=35+4n$ (ou $4n+35$). \quad 2. $C(12)=35+4\times 12=35+48=83$ TND.
3. $35+4n=99$ donc $4n=64$ puis $n=16$. \quad 4. $35+4\times 16=35+64=99$ : la solution convient.

\textbf{Observation à noter :} un élève qui écrit $C(n)=39n$ confond un terme constant et un coefficient ;
c'est une erreur de type \textsc{CONCEPT}, à distinguer d'une erreur de calcul sur $4\times 12$.
""",
    },
    # -------------------------------------------------- évaluation : noyau commun
    "eval_common": {
        "A1": {"skill": "M4E_REL_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Calculer $(-8) + 3 - (-5)$.",
               "answer": r"$0$",
               "steps": [r"$-8+3=-5$", r"$-5-(-5)=-5+5=0$"],
               "errors": [{"code": "CONCEPT", "desc": "soustraire un négatif traité comme une soustraction (résultat $-10$)"},
                          {"code": "CALCUL", "desc": "erreur isolée sur $-8+3$"}],
               "criteria": [{"points": 1, "desc": "résultat $0$ exact"}],
               "baseline_item": "4E_TI_Q02", "comparability": "comparable",
               "role_rentree": "prérequis direct du produit de relatifs en Quatrième"},
        "A2": {"skill": "M4E_FRAC_02", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Calculer $\dfrac{5}{8} - \dfrac{1}{4}$.",
               "answer": r"$\dfrac{3}{8}$",
               "steps": [r"$\frac{1}{4}=\frac{2}{8}$", r"$\frac{5}{8}-\frac{2}{8}=\frac{3}{8}$"],
               "errors": [{"code": "CONCEPT", "desc": "dénominateur converti sans convertir le numérateur (réponse $\\frac{4}{8}$)"},
                          {"code": "METHODE", "desc": "soustraction terme à terme des numérateurs et des dénominateurs"}],
               "criteria": [{"points": 1, "desc": "$\\frac{3}{8}$ ou une écriture équivalente correcte"}],
               "baseline_item": "4E_TI_Q04", "comparability": "comparable",
               "role_rentree": "prérequis du produit et du quotient de fractions en Quatrième"},
        "A3": {"skill": "M4E_LIT_02", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Réduire $7x + 4 - 3x - 9$.",
               "answer": r"$4x - 5$",
               "steps": [r"termes en $x$ : $7x-3x=4x$", r"constantes : $4-9=-5$"],
               "errors": [{"code": "CONCEPT", "desc": "constantes additionnées sans tenir compte des signes ($+13$ ou $-13$)"},
                          {"code": "CONCEPT", "desc": "$4x$ et $-5$ additionnés en $-x$"}],
               "criteria": [{"points": 1, "desc": "$4x-5$ exact"}],
               "baseline_item": "4E_TI_Q08", "comparability": "comparable",
               "role_rentree": "prérequis de l'équation du premier degré"},
        "A4": {"skill": "M4E_GEO_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Dans un triangle rectangle, un angle aigu mesure $37^\circ$. Calculer l'autre angle aigu.",
               "answer": r"$53^\circ$",
               "steps": [r"les deux angles aigus sont complémentaires", r"$90-37=53$"],
               "errors": [{"code": "METHODE", "desc": "$180-37=143$ : l'angle droit n'est pas retiré"},
                          {"code": "LECTURE", "desc": "angle droit compté comme un angle aigu"}],
               "criteria": [{"points": 1, "desc": "$53^\\circ$ exact"}],
               "baseline_item": "4E_TI_Q10", "comparability": "comparable",
               "role_rentree": "prérequis de la trigonométrie et de Pythagore en Quatrième"},
        "B1": {"skill": "M4E_AIRE_01", "skills_extra": ["M4E_PROP_01"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""Une terrasse rectangulaire mesure $12$ m de long et $7$ m de large.
\begin{enumerate}
\item Calculer son aire et son périmètre, en écrivant les unités.
\item Le carrelage coûte $26$ TND le mètre carré. Calculer le prix du carrelage de la terrasse.
\end{enumerate}""",
               "answer": r"Aire $=84\ \text{m}^2$ ; périmètre $=38$ m ; prix $=84\times 26=2\,184$ TND.",
               "steps": [r"$12\times 7=84\ \text{m}^2$", r"$2\times(12+7)=38$ m",
                         r"le prix se calcule sur l'aire, pas sur le périmètre : $84\times 26=2184$"],
               "errors": [{"code": "CONCEPT", "desc": "aire et périmètre échangés"},
                          {"code": "NOTATION", "desc": "unité absente ou $\\text{m}$ au lieu de $\\text{m}^2$"},
                          {"code": "METHODE", "desc": "prix calculé à partir du périmètre"}],
               "criteria": [{"points": 1, "desc": "aire et périmètre exacts avec les unités correctes"},
                            {"points": 1, "desc": "prix exact, calculé à partir de l'aire"}],
               "baseline_item": "4E_TI_Q11", "comparability": "comparable",
               "role_rentree": "grandeurs composées et coût proportionnel, réutilisés toute l'année"},
        "B2": {"skill": "M4E_LIT_01", "skills_extra": ["M4E_LIT_02"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5", "confidence": True,
               "tex": r"""\begin{enumerate}
\item Développer $5(x - 3)$.
\item Réduire ensuite $5(x - 3) + 2x + 7$.
\item Contrôler le résultat obtenu pour $x = 2$, en calculant séparément les deux écritures.
\end{enumerate}""",
               "answer": r"$5x-15$ ; puis $7x-8$ ; contrôle : les deux écritures donnent $6$ pour $x=2$.",
               "steps": [r"$5(x-3)=5x-15$", r"$5x-15+2x+7=7x-8$",
                         r"$x=2$ : $5\times(2-3)+2\times 2+7=-5+4+7=6$ et $7\times 2-8=6$"],
               "errors": [{"code": "CONCEPT", "desc": "distributivité incomplète : $5x-3$"},
                          {"code": "CONCEPT", "desc": "constantes signées : $-15+7$ traité comme $-22$"},
                          {"code": "CONTROLE", "desc": "contrôle annoncé mais une seule écriture évaluée"}],
               "criteria": [{"points": 1, "desc": "développement et réduction exacts"},
                            {"points": 1, "desc": "contrôle mené sur les deux écritures avec la même valeur"}],
               "baseline_item": "4E_TI_Q07", "comparability": "comparable",
               "role_rentree": "double distributivité et mise en équation en Quatrième"},
        "B3": {"skill": "M4E_STAT_01", "skills_extra": ["M4E_PROP_02"], "points": 2, "minutes": 5,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""Un club compte $40$ membres ; $14$ d'entre eux pratiquent la natation.
\begin{enumerate}
\item Calculer la fréquence des nageurs, en pourcentage.
\item Les âges d'un groupe sont $11$ ; $12$ ; $12$ ; $13$ ; $15$ ; $15$ ; $15$ ; $17$.
Calculer la moyenne, puis vérifier qu'elle est comprise entre la plus petite et la plus grande valeur.
\end{enumerate}""",
               "answer": r"$35\,\%$ ; somme $=110$, effectif $=8$, moyenne $=13{,}75$, comprise entre $11$ et $17$.",
               "steps": [r"$14\div 40=0{,}35=35\,\%$", r"somme $=110$ ; $110\div 8=13{,}75$",
                         r"$11 < 13{,}75 < 17$ : le contrôle est concluant"],
               "errors": [{"code": "LECTURE", "desc": "une valeur oubliée dans la somme"},
                          {"code": "METHODE", "desc": "division par le nombre de valeurs distinctes et non par l'effectif"},
                          {"code": "CONTROLE", "desc": "encadrement non effectué"}],
               "criteria": [{"points": 1, "desc": "fréquence exacte en pourcentage"},
                            {"points": 1, "desc": "moyenne exacte et encadrement écrit"}],
               "baseline_item": "4E_TI_Q15", "comparability": "comparable",
               "role_rentree": "moyenne pondérée et médiane en Quatrième"},
        "C1": {"skill": "M4E_AIRE_01",
               "skills_extra": ["M4E_FRAC_02", "M4E_LIT_01", "M4E_PROP_01"],
               "points": 4, "minutes": 10, "task": "transfert", "difficulty": "transfert",
               "space": "lines:10", "confidence": True,
               "tex": r"""\textbf{L'atelier de peinture.} Un mur rectangulaire mesure $6$ m de long et $3$ m de haut.
Une fenêtre rectangulaire de $2$ m sur $1{,}5$ m ne doit pas être peinte.
\begin{enumerate}
\item Calculer l'aire de la surface réellement à peindre.
\item Le tiers de cette surface reçoit d'abord une sous-couche. Calculer l'aire concernée.
\item La peinture coûte $19$ TND le pot et le magasin ajoute un forfait de livraison de $25$ TND.
Écrire l'expression $C(n)$ du coût total pour $n$ pots, puis calculer $C(6)$ en montrant la substitution.
\item Le budget est de $200$ TND. Peut-on acheter $10$ pots ? Répondre par un calcul, puis conclure par une phrase.
\end{enumerate}""",
               "answer": r"$15\ \text{m}^2$ ; $5\ \text{m}^2$ ; $C(n)=19n+25$ ; $C(6)=139$ TND ; $C(10)=215>200$ : non.",
               "steps": [r"$6\times 3=18$ et $2\times 1{,}5=3$, donc $18-3=15\ \text{m}^2$",
                         r"$15\div 3=5\ \text{m}^2$",
                         r"$C(n)=19n+25$",
                         r"$C(6)=19\times 6+25=114+25=139$ TND",
                         r"$C(10)=190+25=215$ ; $215>200$ donc dix pots dépassent le budget"],
               "errors": [{"code": "TRANSFERT", "desc": "aire de la fenêtre non retirée"},
                          {"code": "CONCEPT", "desc": "$C(n)$ écrit $44n$ : forfait et coût unitaire confondus"},
                          {"code": "LECTURE", "desc": "réponse donnée sans comparer $215$ et $200$"},
                          {"code": "NOTATION", "desc": "unités absentes dans la conclusion"}],
               "criteria": [{"points": 1, "desc": "aire à peindre exacte, soustraction de la fenêtre visible"},
                            {"points": 0.5, "desc": "aire de la sous-couche exacte"},
                            {"points": 1.5, "desc": "expression littérale correcte, substitution écrite et $C(6)$ exact"},
                            {"points": 1, "desc": "décision justifiée par la comparaison des deux nombres"}],
               "baseline_item": None, "comparability": "partiellement_comparable",
               "role_rentree": "tâche complexe de rentrée : lire, choisir, calculer, décider"},
    },
}
