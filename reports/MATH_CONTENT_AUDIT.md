# Audit du contenu mathématique — 4e / 3e / 2nde / 1re spécialité

Périmètre : les quatre sources canoniques (`05_SOURCES/`) et les documents opérationnels dérivés qui portent
un corrigé — 20 fiches professeur (`02_SEANCES/S1..S5/*_PROF_Fiche.md`) et 8 corrigés d'évaluation
(`03_EVALUATIONS/*_PROF_Corrige*.md` et `*_Mini_Diagnostic_PROF_Corrige.md`), pour les niveaux 4e, 3e, 2nde et
1re spécialité. Le sous-paquet `1re_nsi/` est hors périmètre (mission mathématiques uniquement) et n'a pas été
audité ici.

## Méthode

1. **Minutage des séances** — extraction automatisée (script Python, expressions régulières) de tous les
   intervalles `"a-b min"` des tableaux « Déroulé horaire »/« Déroulé précis » des 20 fiches professeur, puis
   vérification que les intervalles pavent exactement `[0;120]` sans trou ni chevauchement (et pas seulement
   que la dernière borne vaut 120, ce que faisait le contrôle automatisé existant de `tools/build.py`).
   **Résultat : les 20 fiches sont conformes.**
2. **Recalcul des résultats** — chaque exercice numéroté des 20 banques d'exercices et des 8 corrigés
   d'évaluation a été relu et recalculé indépendamment (calcul mental/algébrique direct pour l'arithmétique,
   les fractions, le calcul littéral, les pourcentages, les probabilités élémentaires ; script Python avec les
   fonctions trigonométriques standard, en degrés, pour les calculs d'angles et de longueurs ; vérification
   symbolique manuelle pour les identités et développements). **173 exercices numérotés recalculés** (20
   fiches professeur + 8 corrigés d'évaluation/diagnostic), en excluant les questions de construction pure
   (tracé, découpage) sans résultat chiffré vérifiable.
3. **Correspondance élève ↔ professeur** — pour chaque énoncé numéroté d'une banque d'exercices, vérification
   qu'une entrée correspondante existe dans la liste des corrections (script de comptage comparant les
   numéros d'énoncés à ceux des corrections).
4. **Notation française** — vérification par échantillonnage des virgules décimales (`0{,}6`), espaces avant
   unités et pourcentages, notation d'intervalle française (crochets tournés pour les bornes exclues), degrés.
5. **Proportion tronc commun / différenciation** — vérification que les quatre sources canoniques annoncent
   bien une cible de 65–70 % de tronc commun et 30–35 % de différenciation (elles le font explicitement,
   citations identiques dans les quatre fichiers), et contrôle par sondage que les blocs « Ateliers
   différenciés » + « Diagnostic complémentaire » des déroulés occupent une part cohérente avec cette cible
   (entre 20 et 35 minutes différenciées sur 120 minutes selon les séances observées). **Ce contrôle n'a pas
   été fait exhaustivement minute par minute sur les 20 séances** : il s'agit d'un objectif de conception
   énoncé et globalement cohérent avec les déroulés, pas d'une mesure automatisée exhaustive — voir
   `CONTENT_GAPS.md`.

## Résultats

- **Erreurs mathématiques trouvées et corrigées : 0** parmi les résultats chiffrés eux-mêmes — tous les
  résultats recalculés indépendamment étaient corrects. Les défauts trouvés portaient sur la **structure des
  corrigés** (contenu dupliqué, corrigé manquant ou mal numéroté, énoncé sans donnée chiffrée, formules
  amputées par une corruption de mise en forme), consignés et corrigés dans `reports/SOURCE_ERRATA.md`
  (entrées ERR-001 à ERR-005) :
  - ERR-001 : banque d'exercices de 3e Séance 4 dupliquée depuis la Séance 3 (Pythagore/Thalès au lieu de
    trigonométrie) — réécrite avec 9 nouveaux exercices de trigonométrie vérifiés.
  - ERR-002 : corrigé mal numéroté en 4e Séance 4 (décalage exercice 7/8).
  - ERR-003 : deux exercices de l'évaluation finale de 4e sans énoncé chiffré ni corrigé (items 15 et 16) —
    complétés.
  - ERR-004 : quatre exercices d'approfondissement de 3e sans corrigé (S1-11, S1-12, S3-9, S5-9) — complétés.
  - ERR-005 : six formules de 1re spécialité amputées de leur signe « = » (et, dans un cas, de leur résultat)
    par une corruption Markdown affectant 28 emplacements dans 8 fichiers, source canonique comprise —
    corrigées.
- **Violations de la durée de 120 minutes : 0** sur les 20 fiches professeur, après contrôle par pavage
  d'intervalles (plus strict que le contrôle existant).
- **Corrigés manquants après correction : 0** (contrôle automatisé de recoupement énoncés/corrections
  exécuté après application des correctifs — voir script dans l'historique de cet audit).
- **Notation française** : conforme par échantillonnage (virgules décimales systématiques, notation
  d'intervalle correcte, degrés et unités attachés).

## Défaut hors périmètre signalé (non corrigé ici)

Un défaut de rendu, distinct du contenu mathématique proprement dit, a été identifié pendant cet audit :
Pandoc (`pandoc --from=gfm --to=html5 --mathml`, utilisé par `tools/build.py`) ne reconnaît pas la convention
`(...)` / `[...]` employée dans **tout** le corpus pour délimiter les expressions mathématiques ; il affiche le
code LaTeX brut tel quel (`\cos\theta`, `\frac{6}{10}`, etc.) dans le HTML et donc dans le PDF généré, y
compris dans les documents élèves. Ceci contredit la contrainte de rendu mathématique de la mission (aucun
LaTeX brut visible côté élève). Ce n'est pas une erreur de contenu mathématique (les formules elles-mêmes,
une fois lues comme du LaTeX, sont exactes) mais un défaut du pipeline de build, hors périmètre de cet audit
de contenu ; il est documenté ici et dans `reports/SOURCE_ERRATA.md` (ERR-005) pour transmission à l'agent
responsable de la chaîne HTML/PDF.

## Validation humaine encore nécessaire

Voir `reports/CONTENT_GAPS.md`.
