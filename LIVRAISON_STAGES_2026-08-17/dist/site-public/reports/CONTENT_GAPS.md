# Lacunes nécessitant un arbitrage humain

Issu de l'audit mathématique (`reports/MATH_CONTENT_AUDIT.md`) et de l'audit d'inventaire. Chaque point
ci-dessous n'a pas été corrigé automatiquement soit parce qu'il exige un jugement pédagogique, soit parce
qu'il dépasse le périmètre de contenu mathématique.

## 1. Rendu mathématique brut dans le HTML/PDF — RÉSOLU le 2026-08-16

~~Pandoc ne convertit pas la syntaxe `(...)`/`[...]` du corpus en formules mathématiques réelles.~~ Corrigé
par l'intégrateur : script `tools/normalize_math_delimiters.py` exécuté une fois sur les 72 fichiers
concernés (72 documents opérationnels + les 4 sources canoniques), convertissant uniquement les passages
portant un signal LaTeX univoque (`\commande`, `^`, `_`, macro décimale `{,}`) vers `$...$`/`$$...$$`. Voir
`reports/SOURCE_ERRATA.md` ERR-006 pour la méthode complète et la preuve de validation (rendu Pandoc des 72
fichiers, 0 fuite de LaTeX brut hors de la balise `<annotation>` MathML, 0 avertissement Pandoc). Le script
est conservé sous `tools/` et est idempotent (un second passage sur un fichier déjà normalisé ne produit
aucune modification), au cas où un nouveau contenu reproduirait la même convention d'écriture.

## 2. Proportion tronc commun / différenciation — contrôle non exhaustif

Les quatre sources canoniques annoncent explicitement une cible de 65–70 % de tronc commun et 30–35 % de
différenciation, cohérente avec la contrainte de la mission. Un sondage sur les tableaux « Déroulé
horaire »/« Déroulé précis » des 20 séances confirme un ordre de grandeur plausible (blocs différenciés et
diagnostics complémentaires occupant généralement 20 à 35 minutes sur 120), mais **aucun décompte minute par
minute exhaustif des 20 séances n'a été réalisé** pour vérifier que chaque séance individuelle respecte
précisément la fourchette. Une validation fine nécessiterait de catégoriser manuellement chaque ligne de
chaque tableau horaire (tronc commun strict / différencié / mixte), ce qui est un jugement d'interprétation
plutôt qu'un calcul automatisable à 100 %.

## 3. 4e Séance 5 : pas de banque d'exercices propre

Contrairement aux Séances 5 de 3e, 2nde et 1re spécialité (qui ont chacune leur propre « Série » d'exercices
de synthèse), la Séance 5 de 4e ne contient aucune banque d'exercices : la fiche renvoie explicitement au
corrigé de l'évaluation finale et aux réponses de la fiche élève. Ce n'est pas nécessairement une erreur
(structure différente assumée), mais l'incohérence avec les trois autres niveaux n'a pas été expliquée dans
la source canonique. **Décision à prendre par l'équipe pédagogique** : ajouter une série de synthèse dédiée
à la Séance 5 de 4e (comme pour les autres niveaux), ou documenter explicitement ce choix de conception dans
la source canonique `4e/05_SOURCES/stage_prerentree_quatrieme_maths.md`.

## 4. Exercices de construction/justification sans réponse chiffrée unique

Plusieurs exercices d'approfondissement demandent une construction ou une justification ouverte (par exemple
« construire un exemple de... », « rédiger la justification : données, propriété, conclusion »). Un exemple
ou une trame de correction a été ajouté pour chacun (voir ERR-004 dans `SOURCE_ERRATA.md`), mais **l'évaluation
de ce type de production reste, par nature, qualitative** et laissée au jugement de l'enseignant plutôt qu'à
un corrigé chiffré unique — ce n'est pas un défaut à corriger, mais un point à garder en tête lors de la
correction en classe.

## 5bis. Rendu MathML dans le PDF — RÉSOLU le 2026-08-16 (voir ERR-009)

Découvert par inspection visuelle réelle des PDF (section 10.4) : WeasyPrint 68.1 n'implémente pas la mise
en page des éléments structurels MathML (`<mfrac>`, `<msup>`, `<msub>`, `<msqrt>`), rendant par exemple
`3/4 ÷ 2/5` comme « 34÷25 » — une fraction affichée comme un nombre entier, trompeuse mathématiquement.
Corrigé par un post-traitement HTML/CSS dans `tools/build.py` (voir `reports/SOURCE_ERRATA.md` ERR-009 pour
le détail complet et les tests de validation).

## 6. Notation caret/underscore résiduelle hors délimiteurs mathématiques (mineur, non corrigé)

Quelques énoncés utilisent un exposant ou un indice en notation informelle collée à un groupe entre
parenthèses sans signal LaTeX à l'intérieur des parenthèses elles-mêmes — par exemple « Développer
`(x-5)^2`. » ou « Si `(2,5)∈C_f` » — où le `(x-5)` ou le `C` ne contient, à lui seul, ni `\`, ni `^`, ni `_`,
donc `tools/normalize_math_delimiters.py` (qui ne convertit que les parenthèses contenant elles-mêmes un
signal LaTeX, pour ne jamais toucher une parenthèse de prose ordinaire) ne les a pas englobées. Résultat :
le `^2`/`_f` s'affiche en caractères ordinaires plutôt qu'en exposant/indice réel. **Ce n'est pas une fuite
de code LaTeX brut** (aucun `\`, rien d'illisible) et le sens reste sans ambiguïté pour un lecteur humain —
seulement une inconsistance cosmétique mineure par rapport aux exercices voisins qui utilisent, eux, un
exposant réel. Non corrigé ici : une correction fiable exigerait de distinguer, exercice par exercice, un
caret informel de convention d'écriture d'un caret qui appartient à un ensemble plus large déjà couvert —
un jugement de contenu au cas par cas plutôt qu'une règle automatisable sans risque de faux positif sur du
texte de prose contenant parenthèses et chiffres (ex. « (2 points) »). Occurrences observées lors de
l'inspection visuelle : `2nde_S1_ELEVE_Activite` / `2nde_S1_PROF_Fiche` (« Calculer (-2)^3 », « Simplifier
10^3×10^-5 ») et `1ere_spe_Remediation_Ciblee_*` (« Si (2,5)∈C_f »). **Décision à prendre** : accepter tel
quel (lisible, non trompeur) ou demander une passe de relecture manuelle ciblée sur ces énoncés précis.

## 7. Sous-paquet `1re_nsi/` — hors périmètre de cet audit

Le dossier `1re_nsi/` (Première spécialité NSI) existe dans le paquet mais n'appartient pas aux quatre
niveaux mathématiques listés dans le mandat (`4e`, `3e`, `2nde`, `1ere_spe`). Il n'a pas été audité
mathématiquement dans le cadre de cette mission et n'apparaît pas dans les compteurs de cet audit. **Décision
à prendre** : clarifier si `1re_nsi/` doit être intégré au périmètre officiel du paquet de documentation ou
traité comme un projet séparé.
