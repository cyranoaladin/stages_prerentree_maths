# -*- coding: utf-8 -*-
"""Blueprint du niveau « Entrée en Première — Numérique et sciences informatiques »."""

LEVEL = {
    "key": "1re_nsi",
    "label": "Entrée en Première — Numérique et sciences informatiques",
    "subject": "NSI",
    "prefix": "NSI1",
    "year_prev": "Seconde (SNT et algorithmique)",
    "year_next": "Première NSI",
    "source_dir": "1re_nsi",
    "baseline_instrument": {
        "name": "Positionnement de pré-rentrée — NSI, entrée en Première",
        "file": "1re_nsi/03_EVALUATIONS/1re_nsi_Test_Initial_ORIGINAL.pdf",
        "items": 18, "minutes": 25, "format": "QCM 4 choix + certitude 1-4",
    },
    "sessions": {
        "S1": "Variables, affectation et conditions",
        "S2": "Boucles, compteurs et accumulateurs",
        "S3": "Fonctions, contrats et tests",
        "S4": "Listes, enregistrements et données CSV",
        "S5": "Algorithmes et mini-projet de synthèse",
    },
    "skills": {
        "NSI1_REP_01": {"label": "Représentation binaire d'un entier et capacité sur n bits",
                        "domain": "Représentation des données", "importance_n": "importante",
                        "baseline_items": ["NSI_TI_Q01", "NSI_TI_Q02"], "sessions": ["S1"]},
        "NSI1_AFF_01": {"label": "Modèle d'affectation : la valeur est copiée, pas liée",
                        "domain": "Programmation", "importance_n": "critique",
                        "baseline_items": ["NSI_TI_Q03", "NSI_TI_Q04"], "sessions": ["S1"]},
        "NSI1_LOG_01": {"label": "Conditions composées et négation d'une condition",
                        "domain": "Programmation", "importance_n": "critique",
                        "baseline_items": ["NSI_TI_Q05", "NSI_TI_Q06"], "sessions": ["S1"]},
        "NSI1_BOUCLE_01": {"label": "range : valeurs produites, bornes et nombre d'itérations",
                           "domain": "Programmation", "importance_n": "critique",
                           "baseline_items": ["NSI_TI_Q07"], "sessions": ["S2"]},
        "NSI1_BOUCLE_02": {"label": "Choisir entre une boucle for et une boucle while",
                           "domain": "Programmation", "importance_n": "critique",
                           "baseline_items": ["NSI_TI_Q08"], "sessions": ["S2"]},
        "NSI1_ACC_01": {"label": "Accumulateur : somme, compteur, invariant de boucle",
                        "domain": "Programmation", "importance_n": "critique",
                        "baseline_items": [], "sessions": ["S2", "S4"]},
        "NSI1_LIST_01": {"label": "Indexation d'une liste, len et dernier indice valide",
                         "domain": "Types construits", "importance_n": "critique",
                         "baseline_items": ["NSI_TI_Q09", "NSI_TI_Q10"], "sessions": ["S4"]},
        "NSI1_MUT_01": {"label": "Alias, copie et mutabilité d'une liste",
                        "domain": "Types construits", "importance_n": "importante",
                        "baseline_items": [], "sessions": ["S4"]},
        "NSI1_FONC_01": {"label": "Paramètre, argument, valeur renvoyée et None",
                         "domain": "Programmation", "importance_n": "critique",
                         "baseline_items": ["NSI_TI_Q11", "NSI_TI_Q12"], "sessions": ["S3"]},
        "NSI1_TEST_01": {"label": "Tests, assertions et cas limites",
                         "domain": "Qualité du code", "importance_n": "critique",
                         "baseline_items": [], "sessions": ["S3", "S4"]},
        "NSI1_CSV_01": {"label": "Chargement d'un fichier CSV et conversion des types",
                        "domain": "Données en tables", "importance_n": "critique",
                        "baseline_items": [], "sessions": ["S4"]},
        "NSI1_TAB_01": {"label": "Enregistrement, attribut et métadonnée",
                        "domain": "Données en tables", "importance_n": "importante",
                        "baseline_items": ["NSI_TI_Q17", "NSI_TI_Q18"], "sessions": ["S4"]},
        "NSI1_WEB_01": {"label": "Rôle du CSS et modèle client-serveur",
                        "domain": "Web", "importance_n": "utile",
                        "baseline_items": ["NSI_TI_Q13", "NSI_TI_Q14"], "sessions": []},
        "NSI1_RES_01": {"label": "Adresse IP et rôle d'un routeur",
                        "domain": "Réseaux", "importance_n": "utile",
                        "baseline_items": ["NSI_TI_Q15", "NSI_TI_Q16"], "sessions": []},
        "NSI1_ALGO_01": {"label": "Recherche séquentielle et principe de la dichotomie",
                         "domain": "Algorithmique", "importance_n": "critique",
                         "baseline_items": [], "sessions": ["S5"]},
    },
    "baseline_items": {
        "NSI_TI_Q01": "Valeur décimale de l'entier écrit 1011 en binaire ?",
        "NSI_TI_Q02": "Sur huit bits, combien de valeurs entières différentes ?",
        "NSI_TI_Q03": "a = 3, puis b = a, puis a = 5 : que vaut b à la fin ?",
        "NSI_TI_Q04": "Que fait l'instruction x = x + 1 ?",
        "NSI_TI_Q05": "L'expression (x > 0) and (x < 10) est vraie :",
        "NSI_TI_Q06": "Quelle est la négation de la condition « x > 5 » ?",
        "NSI_TI_Q07": "Combien de fois le corps de « for i in range(3) » s'exécute-t-il ?",
        "NSI_TI_Q08": "Dans quel cas emploie-t-on une boucle while plutôt qu'une boucle for ?",
        "NSI_TI_Q09": "Soit L = [4, 8, 15, 16]. Que vaut L[1] ?",
        "NSI_TI_Q10": "Que vaut len([3, 7, 9]) ?",
        "NSI_TI_Q11": "Dans « def carre(n): return n * n », que désigne n ?",
        "NSI_TI_Q12": "Que renvoie une fonction Python sans instruction return ?",
        "NSI_TI_Q13": "Dans une page web, quel est le rôle du CSS ?",
        "NSI_TI_Q14": "Modèle client-serveur : que se passe-t-il lors de la consultation d'une page ?",
        "NSI_TI_Q15": "À quoi sert une adresse IP ?",
        "NSI_TI_Q16": "Quel est le rôle d'un routeur ?",
        "NSI_TI_Q17": "Dans un fichier CSV décrivant des élèves, à quoi correspond une ligne ?",
        "NSI_TI_Q18": "Que désigne-t-on par « métadonnée » ?",
    },
    "curriculum_reference": {
        "annee_scolaire_visee": "2026-2027",
        "programme_applique_a_l_eleve": {
            "cycle": "lycée général, spécialité numérique et sciences informatiques de Première",
            "texte": "programme de Première NSI, toujours en vigueur en 2026",
            "BO": "BO spécial n° 1 du 22 janvier 2019",
            "NOR": "MENE1901633A",
            "entree_en_vigueur": "rentrée 2019, non remplacé à la rentrée 2026",
            "nouvelle_progression_applicable": False,
        },
        "transition": "acquis de Seconde 2025-2026, notamment SNT et algorithmique, vers le "
                      "programme de Première NSI de 2019",
        "attendus_de_fin_annee_n_moins_1": "Seconde (SNT et algorithmique)",
        "source_de_la_reference": "audit indépendant du 21 août 2026, section 9 ; à confirmer "
                                  "auprès du Bulletin officiel avant diffusion externe",
        "verifie_par_un_humain": False,
    },
    "critical_prereqs": ["NSI1_AFF_01", "NSI1_LOG_01", "NSI1_BOUCLE_01", "NSI1_BOUCLE_02",
                         "NSI1_ACC_01", "NSI1_LIST_01", "NSI1_FONC_01", "NSI1_TEST_01",
                         "NSI1_CSV_01"],
    "n_bridges": [
        "recherche séquentielle : parcours complet, valeur sentinelle de retour",
        "recherche dichotomique : précondition de tri, division de l'espace de recherche",
        "spécifier une fonction avant de l'écrire, puis la tester",
    ],
    "phase1": {
        "objectif": "Réactiver sans ordinateur les cinq constructions travaillées de la séance 1 à la séance 4.",
        "consigne": r"Sept minutes sans machine. L'ordinateur ne sert ensuite qu'à \emph{contrôler}, jamais à trouver la réponse.",
        "items": [
            {"skill": "NSI1_LIST_01", "tex": r"Pour \code{L = [5, 2, 9, 4]}, donner \code{L[0]}, \code{L[-1]}, \code{len(L)} et le dernier indice valide.", "space": "short",
             "corrige": r"\code{5} ; \code{4} ; \code{4} ; dernier indice \code{3}. Une liste de longueur $n$ a les indices $0$ à $n-1$."},
            {"skill": "NSI1_LOG_01", "tex": r"Écrire la négation de \code{(x >= 3) and (x <= 12)}.", "space": "short",
             "corrige": r"\code{(x < 3) or (x > 12)} : la négation d'un \emph{et} est un \emph{ou}, et chaque comparaison est inversée."},
            {"skill": "NSI1_BOUCLE_01", "tex": r"Donner les valeurs produites par \code{range(2, 11, 3)} et le nombre de tours de boucle.", "space": "short",
             "corrige": r"\code{2, 5, 8} : trois tours. La borne \code{11} est exclue."},
            {"skill": "NSI1_AFF_01", "tex": r"Après \code{a = 4} puis \code{b = a} puis \code{a = 9}, que valent \code{a} et \code{b} ?", "space": "short",
             "corrige": r"\code{a} vaut \code{9} et \code{b} vaut \code{4} : \code{b = a} copie la valeur au moment de l'affectation."},
            {"skill": "NSI1_FONC_01", "tex": r"Que renvoie une fonction qui ne contient aucune instruction \code{return} ? Que vaut alors la variable qui reçoit le résultat ?", "space": "short",
             "corrige": r"Elle renvoie \code{None} ; la variable vaut donc \code{None}, ce qui provoque une erreur au premier calcul."},
        ],
    },
    "phase4": {
        "titre": "Chercher dans une liste : du parcours complet à la dichotomie",
        "objectif": "Découverte guidée : construire, à partir du parcours de liste déjà travaillé, deux algorithmes nouveaux du programme de Première — la recherche séquentielle et la recherche dichotomique, avec leur précondition et leur coût.",
        "contenu_nouveau_annee_n": True,
        "skills_prev": ["NSI1_LIST_01", "NSI1_BOUCLE_01", "NSI1_FONC_01"],
        "skills_next": ["recherche séquentielle", "recherche dichotomique"],
        "tex": r"""
\begin{methodbox}
\textbf{Ce qui change en Première NSI.} Un parcours de liste n'est plus une fin en soi : il devient un
\textbf{algorithme}, c'est-à-dire une procédure dont on sait dire ce qu'elle renvoie, dans quels cas, et à
quel coût.
\par\smallskip
\textbf{Ce qui est réinvesti} : la boucle, l'indexation, le test et le contrat d'une fonction, travaillés de
la séance 1 à la séance 4. \textbf{Ce qui est nouveau} : les \textbf{algorithmes de recherche} eux-mêmes,
leur précondition et leur coût, qui appartiennent au programme de Première.
\end{methodbox}
\begin{warningbox}\small
\textbf{Cette phase introduit des notions de l'année à venir.} Ce que tu produis ici ne sera donc
\emph{pas} comparé à ton positionnement de début de stage : il ne s'agit pas de mesurer un progrès,
mais de préparer les premières séances de septembre.
\end{warningbox}


\subsectiontitle{A. La recherche séquentielle — 8 min}
\begin{lstlisting}
def indice_de(L, cible):
    for i in range(len(L)):
        if ____________________:
            return ____
    return -1
\end{lstlisting}
\begin{enumerate}
\item Compléter les deux trous. \quad Pourquoi renvoie-t-on $-1$ et non $0$ lorsque la cible est absente ?
\shortlines{1}
\item Tracer l'exécution pour \code{L = [7, 3, 9, 3]} et \code{cible = 3}.
\par\noindent\begin{tabularx}{\linewidth}{|>{\bfseries}p{16mm}|X|X|X|}
\hline
Tour & \code{i} & \code{L[i]} & Condition vraie ? \\ \hline
1 & & & \\ \hline
2 & & & \\ \hline
\end{tabularx}
\item Que renvoie l'appel ? \rule{25mm}{0.32pt} \quad Et \code{indice_de([7, 3, 9, 3], 5)} ? \rule{25mm}{0.32pt}
\item Combien de comparaisons au maximum pour une liste de $100$ éléments ? \rule{25mm}{0.32pt}
\end{enumerate}

\subsectiontitle{B. Et si la liste était triée ? — 7 min}
On cherche $41$ dans la liste triée \code{[3, 8, 12, 19, 25, 33, 41, 50]}, dont les indices vont de $0$ à $7$.
\begin{graybox}\small
\textbf{Convention retenue pour tout l'exercice :} la zone de recherche est délimitée par deux indices
\code{g} et \code{d} ; l'indice du milieu est \code{m = (g + d) // 2}, c'est-à-dire le quotient entier.
Une autre convention donnerait un autre décompte : c'est pourquoi on la fixe avant de commencer.
\end{graybox}
\begin{enumerate}
\item Premier tour : \code{g = 0} et \code{d = 7}. Calculer \code{m}, comparer \code{L[m]} à $41$, puis dire
quelle moitié est éliminée.
\shortlines{1}
\item Poursuivre en notant \code{g}, \code{d} et \code{m} à chaque tour. Combien de comparaisons ont été
nécessaires ? \rule{22mm}{0.32pt}
\item Compléter : à chaque étape, la zone de recherche est divisée par \rule{15mm}{0.32pt}.
\item Écrire la \textbf{précondition} indispensable à cet algorithme. \rule{75mm}{0.32pt}
\item Un élève applique cette méthode à une liste non triée et trouve « absent » alors que la valeur y figure.
Expliquer précisément l'origine de l'erreur.
\worklines{2}
\end{enumerate}

\begin{successbox}
\textbf{Preuve attendue :} la valeur de retour en cas d'absence est justifiée ; la précondition de tri est
énoncée avant tout jugement sur l'efficacité.
\end{successbox}
""",
        "corrige": r"""
\textbf{A.} 1. \code{if L[i] == cible:} puis \code{return i}. On renvoie $-1$ parce que $0$ est un indice
valide : $0$ signifierait « trouvé en première position ». $-1$ ne peut être confondu avec aucun indice
renvoyé par la boucle.
2. Tour 1 : \code{i = 0}, \code{L[0] = 7}, condition fausse ; tour 2 : \code{i = 1}, \code{L[1] = 3}, condition vraie.
3. L'appel renvoie \code{1} (première occurrence) ; avec la cible \code{5}, il renvoie \code{-1}.
4. Au maximum $100$ comparaisons.

\textbf{B.} Avec la convention \code{m = (g + d) // 2} :
tour 1, \code{g=0}, \code{d=7}, \code{m=3}, \code{L[3]} vaut $19$, inférieur à $41$, donc \code{g=4} ;
tour 2, \code{g=4}, \code{d=7}, \code{m=5}, \code{L[5]} vaut $33$, inférieur à $41$, donc \code{g=6} ;
tour 3, \code{g=6}, \code{d=7}, \code{m=6}, \code{L[6]} vaut $41$ : trouvé.
1. La moitié gauche est éliminée dès le premier tour. 2. \textbf{Trois} comparaisons.
Avec la convention \code{m = (g + d + 1) // 2}, le premier milieu serait $25$ et deux comparaisons
suffiraient : le décompte dépend de la convention, ce qui justifie de la fixer d'emblée. 3. Divisée par $2$.
4. Précondition : la liste doit être \textbf{triée}. 5. Sans tri, éliminer une moitié n'est pas justifié :
la valeur cherchée peut se trouver dans la partie écartée. L'algorithme reste rapide mais devient faux.

\textbf{Observation à noter :} renvoyer \code{0} au lieu de \code{-1} est une erreur de \textsc{ALGORITHME}
et non de \textsc{SYNTAXE} : le programme s'exécute sans message d'erreur mais ment sur son résultat.
""",
    },
    "eval_common": {
        "A1": {"skill": "NSI1_LIST_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "lines:2",
               "tex": r"Pour \code{L = [7, 1, 8, 4, 2]}, donner \code{L[2]}, \code{L[-1]}, \code{len(L)} et le dernier indice valide.",
               "answer": r"\code{8} ; \code{2} ; \code{5} ; dernier indice \code{4}.",
               "steps": [r"les indices vont de $0$ à $\text{len}(L)-1$"],
               "errors": [{"code": "CONCEPT", "desc": "dernier indice donné égal à \\code{len(L)}"},
                          {"code": "CONCEPT", "desc": "indexation supposée commencer à 1"}],
               "criteria": [{"points": 1, "desc": "les quatre réponses exactes"}],
               "baseline_item": "NSI_TI_Q09", "comparability": "comparable",
               "role_rentree": "prérequis de tout parcours de tableau en Première"},
        "A2": {"skill": "NSI1_LOG_01", "points": 1, "minutes": 2, "task": "automatisme",
               "difficulty": "socle", "space": "lines:2",
               "tex": r"Écrire la négation de \code{x <= 8}, puis celle de \code{(x > 2) or (x == 0)}.",
               "answer": r"\code{x > 8} ; \code{(x <= 2) and (x != 0)}.",
               "steps": [r"négation d'une comparaison", r"négation d'un \code{or} : un \code{and} de négations"],
               "errors": [{"code": "CONCEPT", "desc": "\\code{x < 8} donné comme négation de \\code{x <= 8}"},
                          {"code": "CONCEPT", "desc": "\\code{or} conservé dans la négation"}],
               "criteria": [{"points": 1, "desc": "les deux négations exactes"}],
               "baseline_item": "NSI_TI_Q06", "comparability": "comparable",
               "role_rentree": "conditions de sortie de boucle et tests de bornes"},
        "A3": {"skill": "NSI1_BOUCLE_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "short",
               "tex": r"Pour \code{for i in range(3, 12, 4):}, donner les valeurs prises par \code{i} et le nombre de tours.",
               "answer": r"\code{3, 7, 11} ; trois tours.",
               "steps": [r"départ à 3, pas de 4, borne 12 exclue"],
               "errors": [{"code": "CONCEPT", "desc": "borne supérieure comptée comme atteinte"},
                          {"code": "CALCUL", "desc": "pas confondu avec le nombre de tours"}],
               "criteria": [{"points": 1, "desc": "valeurs et nombre de tours exacts"}],
               "baseline_item": "NSI_TI_Q07", "comparability": "comparable",
               "role_rentree": "contrôle des bornes dans tout algorithme de parcours"},
        "A4": {"skill": "NSI1_AFF_01", "points": 1, "minutes": 1.5, "task": "automatisme",
               "difficulty": "socle", "space": "lines:2",
               "tex": r"On exécute \code{a = 6}, puis \code{b = a}, puis \code{a = a + 4}. Donner \code{a} et \code{b}, puis expliquer en une phrase.",
               "answer": r"\code{a} vaut \code{10}, \code{b} vaut \code{6} : \code{b} a reçu une copie de la valeur, il n'est pas lié à \code{a}.",
               "steps": [r"\code{b = a} copie la valeur 6", r"\code{a = a + 4} réaffecte seulement \code{a}"],
               "errors": [{"code": "CONCEPT", "desc": "\\code{b} supposé suivre les changements de \\code{a}"},
                          {"code": "JUSTIFICATION", "desc": "valeurs exactes mais explication absente"}],
               "criteria": [{"points": 1, "desc": "les deux valeurs exactes et une explication correcte"}],
               "baseline_item": "NSI_TI_Q03", "comparability": "comparable",
               "role_rentree": "modèle mental indispensable avant d'aborder les objets mutables"},
        "B1": {"skill": "NSI1_ACC_01", "points": 2, "minutes": 6, "task": "application",
               "difficulty": "standard", "space": "lines:4", "confidence": True,
               "tex": r"""On exécute le programme suivant.
\begin{lstlisting}
total = 0
n = 0
for v in [4, 9, 2, 7]:
    total = total + v
    n = n + 1
\end{lstlisting}
\begin{enumerate}
\item Compléter le tableau d'état après chaque tour de boucle.
\par\noindent\begin{tabularx}{\linewidth}{|>{\bfseries}p{16mm}|X|X|X|X|}
\hline
Après le tour & 1 & 2 & 3 & 4 \\ \hline
\code{total} & & & & \\ \hline
\code{n} & & & & \\ \hline
\end{tabularx}
\item Donner les valeurs finales, puis dire en une phrase ce que représente chacune des deux variables.
\end{enumerate}""",
               "answer": r"\code{total} : 4, 13, 15, 22 ; \code{n} : 1, 2, 3, 4. Finalement \code{total = 22} (somme des valeurs) et \code{n = 4} (nombre de valeurs parcourues).",
               "steps": [r"accumulation successive des valeurs", r"comptage indépendant du contenu"],
               "errors": [{"code": "CONCEPT", "desc": "somme confondue avec le nombre d'itérations"},
                          {"code": "ALGORITHME", "desc": "accumulateur réinitialisé à chaque tour"},
                          {"code": "JUSTIFICATION", "desc": "tableau exact mais rôle des variables non explicité"}],
               "criteria": [{"points": 1, "desc": "tableau d'état complet et exact"},
                            {"points": 1, "desc": "valeurs finales exactes et rôle de chaque variable correctement énoncé"}],
               "baseline_item": None, "comparability": "non_comparable_absence_baseline",
               "role_rentree": "tout traitement de données de Première repose sur un accumulateur correct"},
        "B2": {"skill": "NSI1_FONC_01", "points": 2, "minutes": 6, "task": "application",
               "difficulty": "standard", "space": "lines:5",
               "tex": r"""On dispose de la fonction suivante.
\begin{lstlisting}
def moyenne(valeurs):
    total = 0
    for v in valeurs:
        total = total + v
    print(total / len(valeurs))
\end{lstlisting}
\begin{enumerate}
\item On écrit \code{m = moyenne([4, 6])}. Que vaut \code{m} ? Justifier.
\item Corriger la fonction pour qu'elle \emph{renvoie} la moyenne.
\end{enumerate}""",
               "answer": r"\code{m} vaut \code{None} car la fonction affiche sans renvoyer ; il faut remplacer \code{print(...)} par \code{return total / len(valeurs)} ; l'appel \code{moyenne([])} provoque une division par zéro.",
               "steps": [r"absence de \code{return} : la fonction renvoie \code{None}",
                         r"correction par \code{return}",
                         r"cas limite de la liste vide : \code{len(valeurs)} vaut 0"],
               "errors": [{"code": "CONCEPT", "desc": "\\code{m} supposé recevoir la valeur affichée"},
                          {"code": "ALGORITHME", "desc": "\\code{print} conservé en plus du \\code{return} sans que la question soit traitée"},
                          {"code": "TRANSFERT", "desc": "aucun cas limite identifié"}],
               "criteria": [{"points": 1.25, "desc": "\\code{None} identifié et justifié par l'absence de \\code{return}"},
                            {"points": 0.75, "desc": "correction par \\code{return} exacte et complète"}],
               "baseline_item": "NSI_TI_Q12", "comparability": "comparable",
               "role_rentree": "contrat d'une fonction : entrée, sortie, cas limites"},
        "B3": {"skill": "NSI1_CSV_01", "skills_extra": ["NSI1_TAB_01"], "points": 2, "minutes": 6,
               "task": "application", "difficulty": "standard", "space": "lines:5",
               "tex": r"""On dispose de l'extrait de fichier suivant.
\begin{lstlisting}[language={}]
id,date,temperature,humidite,statut
C07,2026-08-24,26.5,58,OK
C08,2026-08-24,32.1,49,ALERTE
\end{lstlisting}
\begin{enumerate}
\item Quelles colonnes doivent être converties avant tout calcul, et en quel type ?
\item Expliquer pourquoi \code{"26.5" + "1"} ne donne pas $27{,}5$.
\item Donner un exemple de \emph{métadonnée} associable à ce fichier, et dire en quoi elle
diffère d'une donnée du tableau.
\end{enumerate}""",
               "answer": r'''\code{temperature} se convertit en \code{float} et \code{humidite} en \code{int} ; l'opérateur \code{+} appliqué à deux chaînes les concatène et produit \code{"26.51"} ; une métadonnée décrit le fichier lui-même — date de production, capteur d'origine, unité de mesure, encodage — alors qu'une donnée du tableau décrit un enregistrement.''',
               "steps": [r"conversion obligatoire avant tout calcul",
                         r"\code{+} entre deux chaînes est une concaténation",
                         r"une métadonnée porte sur le fichier, une donnée sur un enregistrement"],
               "errors": [{"code": "CONCEPT", "desc": "conversion jugée inutile parce que la valeur « ressemble » à un nombre"},
                          {"code": "CONCEPT", "desc": "métadonnée confondue avec une donnée du tableau"},
                          {"code": "ALGORITHME", "desc": "concaténation attribuée à une erreur du langage plutôt qu'au type des opérandes"}],
               "criteria": [{"points": 0.75, "desc": "colonnes et types de conversion exacts"},
                            {"points": 0.5, "desc": "concaténation correctement expliquée par le type des opérandes"},
                            {"points": 0.75, "desc": "métadonnée pertinente et distinction avec une donnée du tableau"}],
               "baseline_item": "NSI_TI_Q17", "comparability": "comparable",
               "role_rentree": "traitement de données en tables, chapitre entier de Première"},
        "C1": {"skill": "NSI1_ALGO_01", "skills_extra": ["NSI1_TEST_01", "NSI1_LIST_01"],
               "points": 4, "minutes": 15, "task": "transfert", "difficulty": "transfert",
               "space": "lines:8", "confidence": True,
               "tex": r"""\textbf{Rechercher un capteur.} On dispose d'une liste de dictionnaires
\code{mesures}, chacun possédant au moins la clé \code{"id"}.
\begin{lstlisting}
def chercher(mesures, identifiant):
    for i in range(len(mesures)):
        if ____________________________:
            return ____
    return -1
\end{lstlisting}
\begin{enumerate}
\item Compléter les deux trous.
\item On pose \code{mesures = [{"id": "C01"}, {"id": "C02"}, {"id": "C03"}]}. Donner le résultat de
\code{chercher(mesures, "C03")} et de \code{chercher(mesures, "C09")}, puis écrire un test portant sur
une liste vide, avec son résultat attendu.
\item La liste est désormais triée par identifiant. En une phrase, dire ce que permet alors la recherche
dichotomique et à quelle condition.
\end{enumerate}""",
               "answer": r'''\code{if mesures[i]["id"] == identifiant:} puis \code{return i} ; les résultats sont \code{2} et \code{-1} ; test sur liste vide : \code{chercher([], "C01")} doit renvoyer \code{-1} ; la recherche dichotomique divise par deux la zone de recherche à chaque étape, à la condition que la liste soit triée.''',
               "steps": [r"accès à la clé d'un dictionnaire à l'intérieur d'une liste",
                         r"parcours complet puis valeur sentinelle $-1$",
                         r"cas limite : liste vide",
                         r"précondition de tri, coût logarithmique"],
               "errors": [{"code": "SYNTAXE", "desc": "\\code{mesures[i].id} au lieu de \\code{mesures[i][\"id\"]}"},
                          {"code": "ALGORITHME", "desc": "\\code{return i} placé hors de la condition, la boucle s'arrête au premier tour"},
                          {"code": "TRANSFERT", "desc": "aucun cas limite proposé parmi les deux tests"},
                          {"code": "CONCEPT", "desc": "dichotomie appliquée sans mentionner la précondition de tri"}],
               "criteria": [{"points": 1.5, "desc": "les deux trous complétés correctement"},
                            {"points": 1.5, "desc": "les deux résultats exacts, dont la valeur d'absence, et le test sur liste vide avec son résultat attendu"},
                            {"points": 1, "desc": "gain et précondition de la dichotomie correctement énoncés"}],
               "baseline_item": None, "comparability": "non_comparable_contenu_nouveau",
               "role_rentree": "premier algorithme du programme de Première ; travaillé en phase 4 de cette même séance"},
    },
}
