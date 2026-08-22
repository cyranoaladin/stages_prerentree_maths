"""Contenus propres aux fiches de séance nominatives.

Les fiches collectives portaient l'essentiel : la confrontation, la trace écrite, les
exercices. Il leur manquait ce qui fait tenir deux heures et ce qu'un élève relit trois
semaines plus tard — les automatismes à réactiver en début de séance, la méthode écrite pas
à pas, et les pièges du domaine. Ces trois blocs sont ici, module par module et séance par
séance ; le générateur les assemble avec les parties communes et avec ce que le bilan de
l'élève dit de lui.

Chaque entrée fournit :
  reactivation — six à huit questions courtes, à faire de tête, en dix minutes ;
  methode      — les gestes numérotés du domaine, dans l'ordre où on les pose ;
  pieges       — les erreurs que le domaine produit, indépendamment de l'élève.
"""

BANK: dict[tuple[str, int], dict[str, object]] = {}

# ------------------------------------------------------------------ mathématiques
BANK[("tle_spe", 1)] = {
    "reactivation": [
        r"$(u_n)$ arithmétique, $u_0 = 3$, raison 5. Que vaut $u_4$ ?",
        r"$(v_n)$ géométrique, $v_0 = 2$, raison 3. Que vaut $v_3$ ?",
        r"Calculer $0{,}5^3$, puis $0{,}5^4$. Laquelle est la plus grande ?",
        r"$(w_n)$ géométrique de raison $0{,}9$ et de premier terme positif : croissante ou décroissante ?",
        r"Écrire $u_{n+1} - u_n$ pour $u_n = 3n + 1$. Que vaut cette différence ?",
        r"Une suite dont la différence $u_{n+1} - u_n$ vaut $- 2$ : que peut-on dire d'elle ?",
        r"$u_{n+1}$ et $u_n + 1$ désignent-ils la même chose ?",
    ],
    "methode": [
        "J'écris la relation qui définit la suite, telle qu'elle est donnée.",
        r"Je calcule la différence $u_{n+1} - u_n$, sans la simplifier tout de suite.",
        "J'étudie le signe de cette différence pour tout entier naturel n.",
        "Je conclus sur le sens de variation, en une phrase complète.",
        "Je contrôle en calculant les trois premiers termes.",
    ],
    "pieges": [
        r"Comparer la raison à 0 au lieu de la comparer à 1. Une raison de $0{,}9$ est positive, et pourtant la suite décroît.",
        r"Conclure sur les variations sans avoir écrit la différence : l'erreur de méthode devient invisible dans un calcul faux.",
        r"Confondre $u_{n+1}$, le terme suivant, et $u_n + 1$, le terme augmenté de 1.",
        r"Écrire $v_n = v_0 \times n \times r$ au lieu de $v_0 \times r^n$ pour une suite géométrique.",
    ],
}

BANK[("tle_spe", 2)] = {
    "reactivation": [
        r"Que vaut $e^0$ ?",
        r"Simplifier $e^3 \times e^{-3}$.",
        r"Écrire $e^{2x} \times e^{x}$ sous la forme $e^{ax}$.",
        r"Écrire $1/e^{x}$ avec un exposant négatif.",
        r"$(e^x)^3$ vaut-il $e^{3x}$ ou $3e^x$ ?",
        r"L'équation $e^x = 0$ a-t-elle une solution ?",
        r"$e^x$ est-il parfois négatif ?",
        r"Résoudre $e^x = e^5$.",
    ],
    "methode": [
        "Je ramène chaque membre à une seule exponentielle, en additionnant les exposants.",
        r"Si l'équation est de la forme $e^A = e^B$, j'utilise la stricte croissance : $A = B$.",
        r"Si un facteur $e^x$ apparaît partout, je le factorise — il ne s'annule jamais.",
        "Je résous l'équation restante, qui ne contient plus d'exponentielle.",
        "Je vérifie la solution en la remplaçant dans l'énoncé de départ.",
    ],
    "pieges": [
        r"Écrire $e^{2x} = 2e^x$. Un exposant n'est pas un facteur : $e^{2x} = (e^x)^2$.",
        r"Chercher les valeurs qui annulent $e^x$ : il n'y en a pas, l'exponentielle est strictement positive.",
        r"Simplifier $e^{a} + e^{b}$ en $e^{a+b}$. La règle vaut pour le produit, pas pour la somme.",
        r"Oublier que $e^{-x} = 1/e^{x}$ et traiter le signe moins comme un facteur.",
    ],
}

BANK[("tle_spe", 3)] = {
    "reactivation": [
        r"Que vaut le discriminant de $x^2 - 5x + 6$ ?",
        r"Combien de racines si $\Delta < 0$ ?",
        r"Racines de $x^2 - 4 = 0$.",
        r"Le trinôme $x^2 + 1$ s'annule-t-il sur $\mathbb{R}$ ?",
        r"Somme et produit des racines de $x^2 - 7x + 12$.",
        r"Signe de $- 2x^2 + 3$ quand x est très grand.",
        r"Un trinôme de coefficient dominant positif et de discriminant négatif : quel est son signe ?",
    ],
    "methode": [
        r"J'identifie a, b et c, en respectant les signes.",
        r"Je calcule $\Delta = b^2 - 4ac$.",
        r"Je discute : deux racines si $\Delta > 0$, une racine double si $\Delta = 0$, aucune si $\Delta < 0$.",
        r"Je place les racines dans un tableau de signes, et j'écris d'abord le signe de a.",
        r"Le trinôme est du signe de a partout, sauf entre les racines.",
    ],
    "pieges": [
        r"Dresser un tableau de signes sans y faire figurer le signe de a : le tableau est alors faux une fois sur deux.",
        r"Oublier le signe de b dans $b^2$ : le carré rend positif, mais $- 4ac$ garde le sien.",
        r"Conclure « pas de solution » quand $\Delta < 0$ sans préciser « dans $\mathbb{R}$ ».",
        r"Résoudre une inéquation en gardant le sens de l'inégalité après multiplication par un nombre négatif.",
    ],
}

BANK[("tle_spe", 4)] = {
    "reactivation": [
        r"Dérivée de $x^3$.",
        r"Dérivée de $5x$.",
        r"Dérivée d'une constante.",
        r"Formule de $(uv)'$.",
        r"Formule de $(u/v)'$.",
        r"Si $f'$ est négative sur un intervalle, que fait f ?",
        r"$f'(2) = 0$ : que peut-on affirmer, et que ne peut-on pas affirmer ?",
        r"Que représente $f'(a)$ pour la courbe de f au point d'abscisse a ?",
    ],
    "methode": [
        "Je repère la forme de l'expression : produit, quotient, ou somme de termes simples.",
        r"Je pose u et v à part, puis j'écris $u'$ et $v'$ avant toute chose.",
        "J'applique la formule correspondante, sans développer tout de suite.",
        "Je factorise la dérivée : le signe se lit sur une forme factorisée, jamais sur une forme développée.",
        "Je dresse le tableau de signes de la dérivée, puis celui des variations.",
    ],
    "pieges": [
        r"Écrire $(uv)' = u'v'$. La dérivée d'un produit n'est pas le produit des dérivées.",
        r"Conclure sur les variations à partir d'une dérivée développée, dont le signe ne se lit pas.",
        r"Déduire de $f'(a) = 0$ qu'il y a un extremum : il faut que $f'$ change de signe.",
        r"Confondre $f(a)$, l'ordonnée, et $f'(a)$, la pente de la tangente.",
    ],
}

BANK[("tle_spe", 5)] = {
    "reactivation": [
        r"$u(3 ; - 1)$ et $v(2 ; 6)$ : calculer $u \cdot v$.",
        r"Le produit scalaire est-il un nombre ou un vecteur ?",
        r"Deux vecteurs non nuls orthogonaux : que vaut leur produit scalaire ?",
        r"$P(A) = 0{,}3$ : que vaut $P(\bar{A})$ ?",
        r"A et B incompatibles : que vaut $P(A \cap B)$ ?",
        r"Formule de $P(A \cup B)$.",
        r"Que renvoie `range(2, 10, 3)` ?",
        r"Une variable aléatoire prend les valeurs 0 et 2 avec les probabilités $0{,}4$ et $0{,}6$ : que vaut son espérance ?",
    ],
    "methode": [
        "Pour le produit scalaire : j'écris les coordonnées des deux vecteurs, puis j'applique la formule.",
        "Pour l'orthogonalité : je pose le produit scalaire égal à zéro et je résous.",
        "Pour une probabilité : je décris l'expérience, puis je choisis entre arbre et tableau.",
        "Pour une espérance : je dresse la loi de probabilité complète avant de sommer.",
        "Pour un programme : je déroule une table de trace sur trois tours avant d'exécuter.",
    ],
    "pieges": [
        r"Annoncer un vecteur comme résultat d'un produit scalaire : c'est un nombre.",
        r"Confondre événements incompatibles et événements indépendants.",
        r"Oublier que la somme des probabilités d'une loi vaut 1, et ne pas s'en servir pour contrôler.",
        r"Dans une boucle `for`, confondre le nombre d'itérations et la dernière valeur prise.",
    ],
}

# --------------------------------------------------------------------------- NSI
BANK[("tle_nsi", 1)] = {
    "reactivation": [
        "Écrire 13 en binaire.",
        "Que vaut `1011` en base 10 ?",
        "Combien de valeurs sur 4 bits ? Sur 8 bits ?",
        "Que vaut `0xF` en base 10 ?",
        "Combien de bits code un chiffre hexadécimal ?",
        "Que vaut `not (True and False)` ?",
        "Écrire la négation de `a > 3 and b == 2`.",
        "Sur 8 bits non signés, quelle est la plus grande valeur ?",
    ],
    "methode": [
        "Pour convertir vers le binaire : divisions successives par 2, puis je lis les restes de bas en haut.",
        "Pour convertir vers le décimal : je place les puissances de 2 au-dessus des bits, puis j'additionne celles qui portent un 1.",
        "Pour l'hexadécimal : je découpe le binaire en paquets de quatre bits en partant de la droite.",
        "Pour une expression booléenne : j'évalue les parenthèses, puis `not`, puis `and`, puis `or`.",
        "Je vérifie toute conversion en la refaisant dans l'autre sens.",
    ],
    "pieges": [
        "Lire les restes des divisions successives de haut en bas au lieu de bas en haut.",
        "Nier `a and b` en `not a and not b` : De Morgan donne `not a or not b`.",
        "Confondre le nombre de valeurs représentables et la plus grande valeur : sur n bits, $2^n$ valeurs mais un maximum de $2^n - 1$.",
        "Découper le binaire en paquets de quatre en partant de la gauche.",
    ],
}

BANK[("tle_nsi", 2)] = {
    "reactivation": [
        "`L = [4, 7, 2]` : que vaut `L[0]` ? `L[-1]` ?",
        "Que provoque `L[3]` sur cette liste ?",
        "Après `L.append(9)`, que contient `L` ?",
        "Différence entre `L.append(x)` et `L + [x]` ?",
        "`d = {'a': 1}` : que vaut `d['a']` ? Et `d['b']` ?",
        "Comment ajouter la clé `'b'` de valeur 2 à `d` ?",
        "Une chaîne de caractères est-elle muable ?",
        "Après `M = L` puis `M.append(0)`, que contient `L` ?",
    ],
    "methode": [
        "J'écris le contenu de la structure avant l'instruction, puis après : deux lignes, pas une.",
        "Je distingue ce que l'instruction renvoie de ce qu'elle modifie.",
        "Pour un dictionnaire, je vérifie qu'une clé existe avant de la lire.",
        "Pour un accès par indice, je vérifie que l'indice est dans les bornes.",
        "Je teste sur un cas de taille 1 et sur un cas vide.",
    ],
    "pieges": [
        "Croire que `M = L` recopie la liste : les deux noms désignent le même objet.",
        "Attendre une valeur de retour de `L.append(x)`, qui ne renvoie rien.",
        "Utiliser une liste muable comme valeur par défaut d'un paramètre.",
        "Lire une clé absente d'un dictionnaire sans avoir prévu le cas.",
    ],
}

BANK[("tle_nsi", 3)] = {
    "reactivation": [
        "Quelle est la différence entre `return` et `print` ?",
        "Que renvoie une fonction sans `return` ?",
        "`def f(x): return x + 1` : que vaut `f(f(1))` ?",
        "Combien de tours fait `for i in range(3)` ? Quelles valeurs prend `i` ?",
        "Que vaut `i` après `for i in range(5)` ?",
        "Une variable définie dans une fonction est-elle visible en dehors ?",
        "Que fait `while` si la condition est fausse dès le départ ?",
        "Écrire l'en-tête d'une fonction `moyenne` prenant une liste.",
    ],
    "methode": [
        "J'écris la spécification avant le corps : ce que la fonction prend, ce qu'elle renvoie.",
        "Je traite le cas général, puis je reviens sur le cas limite — liste vide, valeur unique.",
        "Je déroule une table de trace sur trois tours avant d'exécuter.",
        "J'écris au moins deux tests, dont un cas limite.",
        "Je vérifie que chaque branche du code se termine par un `return`.",
    ],
    "pieges": [
        "Écrire `print` là où l'on attend `return` : la fonction affiche mais ne renvoie rien.",
        "Réinitialiser un accumulateur à l'intérieur de la boucle au lieu de l'initialiser avant.",
        "Affecter une variable globale dans une fonction sans la déclarer : Python la rend locale.",
        "Oublier le cas de la liste vide, qui fait échouer la fonction à l'exécution.",
    ],
}

BANK[("tle_nsi", 4)] = {
    "reactivation": [
        "La recherche dichotomique exige quoi du tableau ?",
        "Sur 1 000 éléments triés, combien de comparaisons au pire en dichotomie ?",
        "Et en recherche séquentielle ?",
        "Qu'est-ce qu'une précondition ?",
        "Que fait `assert` quand la condition est fausse ?",
        "Le tri par insertion sur une liste déjà triée : combien de comparaisons ?",
        "Que compare-t-on pour juger deux algorithmes : le temps mesuré ou le nombre d'opérations ?",
        "Qu'est-ce qu'un invariant de boucle ?",
    ],
    "methode": [
        "J'écris la précondition, puis l'`assert` qui la vérifie.",
        "Je déroule l'algorithme à la main sur un exemple de quatre éléments.",
        "Je compte les comparaisons, pas les secondes.",
        "Je cherche le cas le plus favorable et le cas le pire, séparément.",
        "Je vérifie que la boucle se termine : quelle quantité décroît à chaque tour ?",
    ],
    "pieges": [
        "Appliquer la dichotomie à un tableau non trié : le résultat est faux sans être détecté.",
        "Confondre le coût dans le pire des cas et le coût moyen.",
        "Juger un algorithme au chronomètre sur un seul jeu de données.",
        "Écrire une boucle dont rien ne garantit qu'elle s'arrête.",
    ],
}

BANK[("tle_nsi", 5)] = {
    "reactivation": [
        "Dans un fichier CSV avec en-tête, combien d'enregistrements pour 501 lignes ?",
        "Qu'est-ce qu'un descripteur ?",
        "Écrire en SQL : afficher tous les champs de la table `eleves`.",
        "Ajouter à cette requête la condition « classe vaut TG3 ».",
        "Comment s'appelle l'opération qui garde certaines lignes ? Certaines colonnes ?",
        "Qu'est-ce qu'une clé primaire ?",
        "Citer les quatre éléments du modèle de von Neumann.",
        "Citer deux ressources gérées par un système d'exploitation.",
    ],
    "methode": [
        "J'identifie d'abord les tables concernées, puis les colonnes voulues.",
        "J'écris `SELECT`, puis `FROM`, puis `WHERE` : dans cet ordre, même si l'exécution diffère.",
        "Pour un rapprochement entre deux tables, je repère la clé étrangère avant d'écrire la jointure.",
        "Je contrôle le résultat sur trois lignes à la main.",
        "En Python, je nomme chaque étape par l'opération relationnelle qu'elle réalise.",
    ],
    "pieges": [
        "Compter la ligne d'en-tête d'un CSV comme un enregistrement.",
        "Confondre sélection, qui porte sur les lignes, et projection, qui porte sur les colonnes.",
        "Écrire une jointure sans condition de rapprochement : le résultat croise tout avec tout.",
        "Supposer qu'un CSV garantit l'unicité des identifiants.",
    ],
}

# ---------------------------------------------------------------- physique-chimie
BANK[("tle_pc", 1)] = {
    "reactivation": [
        r"Formule reliant quantité de matière, masse et masse molaire.",
        r"Formule reliant quantité de matière, concentration et volume.",
        r"$\SI{0.20}{\mole\per\litre}$ dans $\SI{250}{\milli\litre}$ : quelle quantité de matière ?",
        r"Dans un couple $\ce{Ox/Red}$, lequel gagne des électrons ?",
        r"Une solution de pH 3 est-elle plus ou moins acide qu'une solution de pH 6 ?",
        r"Que vaut l'avancement à l'état initial ?",
        r"Qu'est-ce qui est conservé au cours d'une transformation chimique ?",
    ],
    "methode": [
        "Je convertis toutes les données dans les unités du système international.",
        "Je calcule les quantités de matière initiales de chaque réactif.",
        "Je dresse le tableau d'avancement, ligne par ligne, sans sauter l'état intermédiaire.",
        "Je divise chaque quantité initiale par son coefficient stœchiométrique : le plus petit quotient désigne le limitant.",
        "Je contrôle que l'état final ne comporte aucune quantité négative.",
    ],
    "pieges": [
        r"Désigner comme limitant le réactif le moins abondant, sans diviser par le coefficient stœchiométrique.",
        r"Oublier de convertir les millilitres en litres avant d'appliquer $n = C \times V$.",
        r"Écrire une demi-équation sans équilibrer les charges.",
        r"Croire qu'un pH élevé signifie une solution plus acide.",
    ],
}

BANK[("tle_pc", 2)] = {
    "reactivation": [
        r"Formule du poids d'un objet de masse m.",
        r"Unité d'une force.",
        r"Poids d'un objet de $\SI{2.0}{\kilogram}$, avec $g = \SI{9.8}{\newton\per\kilogram}$.",
        r"Le vecteur vitesse est-il tangent ou perpendiculaire à la trajectoire ?",
        r"Un objet immobile : les forces se compensent-elles ?",
        r"Qui exerce le poids d'un objet ?",
        r"Un mouvement à vitesse de norme constante sur un cercle : le vecteur vitesse est-il constant ?",
    ],
    "methode": [
        "Je définis le système étudié, en une phrase, avant tout schéma.",
        "Je fais l'inventaire des forces, en nommant pour chacune ce qui l'exerce.",
        "Je représente chaque force par une flèche partant du centre du système.",
        "Je regarde si les forces se compensent, et je conclus sur le vecteur vitesse.",
        "Je contrôle l'unité de chaque résultat.",
    ],
    "pieges": [
        r"Confondre masse, en kilogrammes, et poids, en newtons.",
        r"Oublier une force de contact — la réaction du support, la tension d'un fil.",
        r"Croire qu'un objet immobile ne subit aucune force.",
        r"Raisonner sur la norme de la vitesse en oubliant sa direction.",
    ],
}

BANK[("tle_pc", 3)] = {
    "reactivation": [
        r"Formule de l'énergie cinétique.",
        r"Formule de l'énergie potentielle de pesanteur.",
        r"Unité de l'énergie.",
        r"Un objet de $\SI{2.0}{\kilogram}$ à $\SI{3.0}{\metre\per\second}$ : quelle énergie cinétique ?",
        r"L'énergie potentielle dépend-elle de l'origine choisie ?",
        r"Que vaut le travail d'une force perpendiculaire au déplacement ?",
        r"Un objet immobile posé sur une étagère a-t-il une énergie cinétique ?",
    ],
    "methode": [
        "Je choisis l'origine des altitudes et je l'annonce.",
        "Je calcule l'énergie mécanique à l'état initial, puis à l'état final.",
        "Je compare les deux : l'écart est l'énergie échangée avec l'extérieur.",
        "S'il y a frottement, je nomme l'énergie dissipée au lieu de dire qu'elle a disparu.",
        "Je contrôle l'ordre de grandeur du résultat.",
    ],
    "pieges": [
        r"Oublier le facteur $\frac{1}{2}$ dans l'énergie cinétique.",
        r"Élever la masse au carré au lieu de la vitesse.",
        r"Appliquer la conservation de l'énergie mécanique en présence de frottement.",
        r"Dire que l'énergie dissipée est perdue : elle a changé de forme, la "
        r"matière s'est échauffée.",
    ],
}

BANK[("tle_pc", 4)] = {
    "reactivation": [
        r"Relation entre longueur d'onde, célérité et fréquence.",
        r"Relation entre période et fréquence.",
        r"Unité de la fréquence.",
        r"$\SI{340}{\metre\per\second}$ et $\SI{170}{\hertz}$ : quelle longueur d'onde ?",
        r"Quand une onde change de milieu, qu'est-ce qui ne change pas ?",
        r"Où se forme l'image d'un objet situé à l'infini ?",
        r"Un rayon passant par le centre optique : que devient-il ?",
    ],
    "methode": [
        "J'écris la relation avant de remplacer par les valeurs.",
        "Je convertis toutes les grandeurs dans les unités du système international.",
        "Pour une lentille, je trace les deux rayons particuliers avant d'en tracer un troisième.",
        "Je repère l'image à l'intersection des rayons émergents, ou de leurs prolongements.",
        "Je contrôle l'ordre de grandeur et l'unité.",
    ],
    "pieges": [
        r"Croire que la fréquence change quand l'onde change de milieu : c'est la longueur d'onde qui change.",
        r"Confondre période et fréquence, qui sont inverses l'une de l'autre.",
        r"Tracer un rayon particulier faux, et construire l'image dessus sans le voir.",
        r"Croire qu'en masquant la moitié d'une lentille on perd la moitié de l'image.",
    ],
}

BANK[("tle_pc", 5)] = {
    "reactivation": [
        r"Loi d'Ohm.",
        r"Formule de la puissance dissipée par un conducteur ohmique, à partir de R et I.",
        r"Relation entre énergie, puissance et durée.",
        r"Unité de la puissance. Unité de l'énergie.",
        r"$\SI{20}{\ohm}$ traversé par $\SI{0.50}{\ampere}$ : quelle tension ?",
        r"Combien de chiffres significatifs dans $\SI{0.0250}{\metre}$ ?",
        r"Le courant est-il le même avant et après une résistance ?",
    ],
    "methode": [
        "J'écris la relation littérale avant de remplacer par les valeurs.",
        "Je convertis les durées en secondes avant tout calcul d'énergie.",
        "Je calcule, puis j'arrondis en dernier — jamais en cours de calcul.",
        "Je fixe le nombre de chiffres significatifs d'après la donnée la moins précise.",
        "J'écris le résultat avec son unité, et je contrôle son ordre de grandeur.",
    ],
    "pieges": [
        r"Croire que l'intensité diminue après la traversée d'une résistance.",
        r"Laisser une durée en minutes dans un calcul d'énergie en joules.",
        r"Recopier tous les chiffres de la calculatrice comme s'ils étaient significatifs.",
        r"Arrondir à chaque étape intermédiaire, ce qui déplace le résultat final.",
    ],
}


# ---------------------------------------------------------------------------------
# Transfert, prise de recul et question de sortie.
#
# Le transfert place l'élève devant une situation où la méthode n'est pas annoncée : c'est
# le seul moment où l'on voit s'il a compris ou seulement suivi. Le contrôle lui demande
# comment il sait que son résultat tient. La question de sortie sert au professeur à
# trancher, en fin de séance, entre acquis, à confirmer et à reprendre.

COMPLEMENTS: dict[tuple[str, int], dict[str, object]] = {

("tle_spe", 1): {
    "transfert": r"""Une entreprise compte $\SI{1200}{}$ abonnés et en perd $\SI{5}{\percent}$
par mois, mais en gagne 30 nouveaux chaque mois. On note $a_n$ le nombre d'abonnés après n
mois. Écris la relation qui lie $a_{n+1}$ à $a_n$. Cette suite est-elle arithmétique ?
géométrique ? Ni l'une ni l'autre ? Calcule $a_1$ et $a_2$, puis dis si le nombre d'abonnés
augmente ou diminue au début.""",
    "controle": [
        r"Comment vérifier, sans refaire le calcul, qu'une suite annoncée décroissante l'est bien ?",
        r"Quelle donnée de l'énoncé aurais-tu pu ignorer sans changer ta réponse ?",
    ],
    "exit": [
        r"Écris la différence $u_{n+1} - u_n$ pour $u_n = 2 \times 3^n$, sans la calculer.",
        r"Une suite géométrique de raison $0{,}95$ et de premier terme 100 : croissante ou décroissante ? Pourquoi ?",
        r"En une phrase : à quoi le sens de variation va-t-il servir en Terminale ?",
    ],
},

("tle_spe", 2): {
    "transfert": r"""Une population de bactéries suit $N(t) = 500 e^{0{,}3t}$, où t est en
heures. Au bout de combien d'heures la population dépasse-t-elle 2000 ? Tu ne disposes pas
encore du logarithme : procède par encadrement, en calculant $N(4)$ et $N(5)$. Que faudrait-il
pour répondre exactement ?""",
    "controle": [
        r"Comment vérifier qu'une solution d'équation avec exponentielle est correcte ?",
        r"Pourquoi l'équation $e^x = k$ n'a-t-elle pas toujours de solution ?",
    ],
    "exit": [
        r"Simplifie $e^{4x} / e^{x-2}$.",
        r"Résous $e^{3x} = e^{x+4}$.",
        r"Vrai ou faux : $e^{x}$ peut valoir 0. Justifie en une ligne.",
    ],
},

("tle_spe", 3): {
    "transfert": r"""Un objet lancé vers le haut a pour altitude $h(t) = - 5t^2 + 20t + 1$,
en mètres, t étant en secondes. Pendant combien de temps l'objet est-il au-dessus de
$\SI{16}{\metre}$ ? Rien dans l'énoncé ne dit d'utiliser le second degré : c'est à toi de le
reconnaître.""",
    "controle": [
        r"Comment vérifier deux racines trouvées sans refaire le discriminant ?",
        r"Un tableau de signes sans le signe de a : pourquoi est-ce faux une fois sur deux ?",
    ],
    "exit": [
        r"Que vaut le discriminant de $2x^2 - 4x + 5$ ? Combien de racines ?",
        r"Signe de $- x^2 + 4$ sur $\mathbb{R}$, en une ligne.",
        r"Somme et produit des racines de $x^2 - 9x + 20$, sans les calculer.",
    ],
},

("tle_spe", 4): {
    "transfert": r"""Une boîte sans couvercle est fabriquée dans un carré de carton de
$\SI{20}{\centi\metre}$ de côté, en découpant un carré de côté x à chaque coin. Son volume
vaut $V(x) = x(20 - 2x)^2$. Pour quelle valeur de x le volume est-il maximal ? L'énoncé ne
dit pas de dériver : à toi de décider.""",
    "controle": [
        r"Comment savoir si un extremum trouvé est un maximum et non un minimum ?",
        r"Pourquoi factoriser la dérivée avant d'étudier son signe ?",
    ],
    "exit": [
        r"Dérive $f(x) = (2x + 1)(x - 3)$.",
        r"$f'$ est négative sur $]0 ; 3[$ : que fait f sur cet intervalle ?",
        r"$f'(2) = 0$ : peut-on affirmer qu'il y a un extremum en 2 ? Justifie.",
    ],
},

("tle_spe", 5): {
    "transfert": r"""Un jeu propose de tirer une carte dans un jeu de 32. Tu gagnes 5 euros si
c'est un cœur, 10 euros si c'est l'as de pique, et tu perds 2 euros sinon. Le jeu
est-il favorable au joueur ? Décide quelle notion utiliser, puis conclus.""",
    "controle": [
        r"Comment contrôler qu'une loi de probabilité est complète ?",
        r"Un produit scalaire nul : que peux-tu affirmer, et que ne peux-tu pas affirmer ?",
    ],
    "exit": [
        r"$u(2 ; - 3)$ et $v(6 ; 4)$ : ces vecteurs sont-ils orthogonaux ?",
        r"$P(A) = 0{,}4$, $P(B) = 0{,}5$, A et B incompatibles : que vaut $P(A \cup B)$ ?",
        r"Une espérance négative : qu'est-ce que cela signifie pour un jeu ?",
    ],
},

("tle_nsi", 1): {
    "transfert": r"""Un capteur transmet ses mesures sur un octet non signé. On relève la
trame `11001010`. a) Quelle valeur décimale ? b) Le constructeur annonce une plage de 0 à
200 : la valeur relevée est-elle plausible ? c) On passe à un codage signé en complément à
deux, sans changer les bits. Que devient la valeur ?""",
    "controle": [
        r"Comment vérifier une conversion binaire sans refaire les divisions ?",
        r"Pourquoi le nombre de valeurs et la valeur maximale ne sont-ils pas le même nombre ?",
    ],
    "exit": [
        r"Écris 26 en binaire.",
        r"Que vaut `0x1F` en base 10 ?",
        r"Écris la négation de `x >= 0 and y < 10`.",
    ],
},

("tle_nsi", 2): {
    "transfert": r"""On veut compter les mots d'un texte. Deux structures sont possibles :
une liste de couples `(mot, effectif)` ou un dictionnaire `mot -> effectif`. a) Écris
l'ajout d'un mot dans chacune. b) Laquelle est la plus rapide pour savoir si un mot est déjà
présent ? Pourquoi ? c) Laquelle choisirais-tu, et dans quel cas l'autre serait-elle
préférable ?""",
    "controle": [
        r"Comment savoir si une opération a modifié la structure ou en a créé une nouvelle ?",
        r"Quel test simple révèle qu'une liste a été copiée par référence ?",
    ],
    "exit": [
        r"`L = [1, 2, 3]` puis `M = L` puis `M.append(4)`. Que contient `L` ?",
        r"Comment tester qu'une clé existe dans un dictionnaire `d` ?",
        r"Cite une structure muable et une structure immuable.",
    ],
},

("tle_nsi", 3): {
    "transfert": r"""Écris une fonction `est_croissante(L)` qui renvoie `True` si la liste est
triée par ordre croissant. a) La fonction. b) Sa spécification. c) Que doit-elle renvoyer sur
une liste vide ? sur une liste d'un seul élément ? Justifie ton choix — il n'y a pas une seule
réponse acceptable, mais il faut le dire dans la spécification.""",
    "controle": [
        r"Comment savoir si une fonction renvoie bien quelque chose dans tous les cas ?",
        r"Quelle question poser à un programme qui « marche » sur un exemple ?",
    ],
    "exit": [
        r"Quelle est la différence entre `return` et `print` ?",
        r"Combien de tours fait `for i in range(1, 7, 2)` ?",
        r"Une variable affectée dans une fonction est-elle visible en dehors ?",
    ],
},

("tle_nsi", 4): {
    "transfert": r"""Un site conserve les identifiants de ses membres. On doit décider entre
garder la liste triée et faire une dichotomie, ou la laisser en désordre et faire une
recherche séquentielle. Le site compte $\SI{100000}{}$ membres, avec 10 inscriptions et
$\SI{50000}{}$ recherches par jour. Quelle solution choisis-tu ? Justifie par un ordre de
grandeur du nombre d'opérations, pas par une impression.""",
    "controle": [
        r"Comment être sûr qu'une boucle s'arrête ?",
        r"Pourquoi chronométrer un algorithme ne suffit-il pas à le juger ?",
    ],
    "exit": [
        r"Que faut-il vérifier avant d'appliquer une recherche dichotomique ?",
        r"Sur 1000 éléments triés, combien de comparaisons au pire ?",
        r"Le tri par insertion sur une liste déjà triée : combien de comparaisons ?",
    ],
},

("tle_nsi", 5): {
    "transfert": r"""Une association gère ses adhérents dans un fichier CSV de 4000 lignes.
Elle veut savoir quels adhérents n'ont pas payé leur cotisation cette année, en croisant avec
un second fichier des paiements. a) Écris la requête SQL si les deux fichiers étaient des
tables. b) Décris l'algorithme Python à partir des deux fichiers. c) Que gagne-t-elle à passer
à une base de données ?""",
    "controle": [
        r"Comment vérifier qu'une requête SQL renvoie bien ce qu'on voulait ? "
        r"(SQL est au programme de Terminale : on l'ouvre ici, on ne l'exige pas.)",
        r"Qu'est-ce qui, dans un CSV, peut casser silencieusement un traitement ?",
    ],
    "exit": [
        r"Sélection ou projection : laquelle porte sur les colonnes ?",
        r"À quoi sert une clé étrangère ?",
        r"Cite deux ressources gérées par le système d'exploitation.",
    ],
},

("tle_pc", 1): {
    "transfert": r"""Un comprimé effervescent contient $\SI{0.50}{\gram}$ d'hydrogénocarbonate
de sodium $\ce{NaHCO3}$ ($M = \SI{84}{\gram\per\mole}$). Plongé dans un excès d'acide, il
libère du dioxyde de carbone selon $\ce{HCO3- + H+ -> H2O + CO2}$. a) Quel est le réactif
limitant, et pourquoi n'y a-t-il pas à le chercher ici ? b) Quel volume de $\ce{CO2}$ obtient-on,
avec $V_m = \SI{24}{\litre\per\mole}$ ? c) L'ordre de grandeur est-il plausible pour un
comprimé ?""",
    "controle": [
        r"Comment savoir, sans tableau, qu'un réactif est en excès ?",
        r"Quel contrôle rapide révèle une erreur de conversion millilitres-litres ?",
    ],
    "exit": [
        r"Écris la relation entre quantité de matière, masse et masse molaire.",
        r"$\SI{0.10}{\mole\per\litre}$ dans $\SI{50}{\milli\litre}$ : quelle quantité de matière ?",
        r"Comment désigne-t-on le réactif qui disparaît le premier ?",
    ],
},

("tle_pc", 2): {
    "transfert": r"""Un skieur descend une piste rectiligne à vitesse constante. a) Que peut-on
affirmer sur la somme des forces qu'il subit ? b) Fais le bilan des forces et explique comment
elles se compensent, alors que la pente n'est pas horizontale. c) Le skieur accélère
maintenant : qu'est-ce qui a changé dans le bilan ?""",
    "controle": [
        r"Comment vérifier qu'un bilan des forces est complet ?",
        r"Vitesse constante en norme : la somme des forces est-elle nécessairement nulle ?",
    ],
    "exit": [
        r"Poids d'un objet de $\SI{5.0}{\kilogram}$, avec $g = \SI{9.8}{\newton\per\kilogram}$.",
        r"Le vecteur vitesse est-il tangent à la trajectoire ?",
        r"Un objet immobile subit-il des forces ?",
    ],
},

("tle_pc", 3): {
    "transfert": r"""Un ascenseur de $\SI{800}{\kilogram}$ monte de $\SI{15}{\metre}$ à vitesse
constante en $\SI{20}{\second}$. a) Quelle énergie le moteur a-t-il fournie, au minimum ?
b) Quelle puissance cela représente-t-il ? c) La puissance réelle du moteur est de
$\SI{8}{\kilo\watt}$. Que devient la différence ?""",
    "controle": [
        r"Comment contrôler qu'une énergie calculée a le bon ordre de grandeur ?",
        r"Pourquoi faut-il annoncer l'origine des altitudes avant de calculer une énergie potentielle ?",
    ],
    "exit": [
        r"Énergie cinétique d'un objet de $\SI{4.0}{\kilogram}$ à $\SI{5.0}{\metre\per\second}$.",
        r"Quelle est l'unité de l'énergie ?",
        r"En présence de frottement, l'énergie mécanique se conserve-t-elle ?",
    ],
},

("tle_pc", 4): {
    "transfert": r"""Une chauve-souris émet un cri de $\SI{40}{\kilo\hertz}$ dans l'air
($v = \SI{340}{\metre\per\second}$) et perçoit l'écho $\SI{12}{\milli\second}$ plus tard.
a) Quelle est la longueur d'onde de son cri ? b) À quelle distance se trouve l'obstacle ?
Attention au trajet parcouru. c) Pourquoi une fréquence élevée est-elle un avantage ici ?""",
    "controle": [
        r"Comment vérifier qu'une longueur d'onde calculée est plausible ?",
        r"Quelle grandeur ne change pas quand une onde change de milieu ?",
    ],
    "exit": [
        r"Relation entre longueur d'onde, célérité et fréquence.",
        r"$\SI{340}{\metre\per\second}$ et $\SI{680}{\hertz}$ : quelle longueur d'onde ?",
        r"Où se forme l'image d'un objet situé à l'infini ?",
    ],
},

("tle_pc", 5): {
    "transfert": r"""Une plaque chauffante porte l'indication « $\SI{230}{\volt}$ —
$\SI{2000}{\watt}$ ». a) Quelle intensité la traverse en fonctionnement normal ? b) Quelle est
sa résistance ? c) Elle chauffe $\SI{1.5}{\litre}$ d'eau pendant $\SI{6.0}{\minute}$. Quelle
énergie a-t-elle consommée ? d) Écris chaque résultat avec un nombre de chiffres significatifs
justifié.""",
    "controle": [
        r"Comment contrôler qu'une puissance calculée est plausible pour un appareil domestique ?",
        r"Combien de chiffres significatifs peut-on garder quand la donnée la moins précise en a deux ?",
    ],
    "exit": [
        r"Loi d'Ohm.",
        r"$\SI{100}{\ohm}$ traversé par $\SI{0.20}{\ampere}$ : quelle puissance dissipée ?",
        r"Le courant est-il le même avant et après une résistance ?",
    ],
},

}


def bloc(module: str, session: int, nom: str):
    """Le bloc demandé, ou None s'il n'existe pas pour cette séance."""
    return COMPLEMENTS.get((module, session), {}).get(nom)
