# Bilan longitudinal — rapport de tests

Toutes les copies employées sont des **fixtures synthétiques** (`TEST_INES`), dans
des bases jetables. Aucun score réel n'a été saisi.

## Comptes

| suite | avant | après |
| --- | --- | --- |
| suite projet | 25 | **25** |
| post-distribution V3 | 98 (4 ignorés) | **98 (4 ignorés)** |
| application correction | 154 (1 ignoré) | **193 (1 ignoré)** |
| dont bilan longitudinal | — | **39** |
| dont micro-passe Inès | 34 | **34** |
| dont pilote Inès | 28 | **28** |
| harness `test_analyze_s5` | 48 | **48** |

Aucun échec. Aucun test supprimé. Le nombre d'ignorés n'augmente pas.

## Ce que couvrent les 39 tests

**Verrous d'entrée.** Une correction en brouillon ne produit pas de bilan ; une
ligne non saisie bloque la génération ; l'absence de correction est un obstacle
explicite et non une exception.

**Sources.** Le diagnostic initial est réellement utilisé (instrument, date, sept
domaines statués). Les cinq séances sont utilisées, chacune avec l'objectif
personnalisé écrit au dossier de l'élève. Chaque source présente porte une empreinte
de 64 caractères. Une source absente est déclarée avec son motif, sans empreinte, et
apparaît dans les limites d'interprétation. Un document couvrant deux séances vaut
pour les deux.

**Modèle de preuve.** La hiérarchie est ordonnée et seul le niveau A autorise une
affirmation de maîtrise. Les faits issus du matériel de séance sont tous de niveau C
et emploient « ciblée », jamais « acquise ». La couverture se calcule séparément de
la maîtrise.

**Test critique — notion ciblée mais non évaluée.** `worked_during_stage = True`,
`current_mastery = unknown`, statut `PREUVE_FINALE_INSUFFISANTE`, et le contrôle
`check_mastery_claims` ne trouve aucune affirmation de maîtrise à son sujet dans le
document parents.

**Test critique — fragilité initiale et réussites finales.**
`qualitative_trajectory = positive_evidence`, `mastery_delta = null`, statut parmi
`CONSOLIDATION_OBSERVEE` ou `FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION`. Le scénario
inverse est également couvert : fragilité initiale et fragilité finale donnent
`persistent_difficulty`.

**Test critique — passerelle échouée.** Aucune priorité N−1, aucun rang de priorité,
aucun diagnostic initial, aucune entrée dans le plan de consolidation, et un
vocabulaire exempt de « lacune », « non acquis », « retard » et « insuffisance ».

**Test critique — récence.** `REUSSITE_A_CONFIRMER`, `retention_status =
not_yet_verified`, et la semaine 2 porte bien un mini-test différé.

**Plan.** Quatre semaines ; chaque objectif porte un seuil constatable ; la charge
reste entre 10 et 25 minutes ; deux P1 au maximum, avec motif de rétrogradation ;
la semaine 3 mêle bien deux compétences.

**Langue.** Le bilan parents passe le contrôle. La contre-épreuve vérifie que le
contrôle **refuse** réellement : huit textes fautifs sont testés un par un
(identifiant de compétence, identifiant de critère, progression chiffrée, « lacune »,
« définitivement acquise », « est indispensable », « élève faible », clé technique).
La synthèse enseignant a le droit aux identifiants mais pas aux progressions
chiffrées. Un texte refusé n'est jamais compilé.

**Provenance.** Chaque fait porte un identifiant, un énoncé, un type de source et un
niveau de preuve. L'empreinte des faits est stable et **auto-vérifiable** : elle
exclut sa propre valeur du calcul, de sorte que `digest(payload) ==
payload["facts_sha256"]` reste vrai après insertion.

**Péremption.** Un bilan produit puis une correction rouverte : le système déclare le
bilan périmé et donne le motif. La recherche porte sur l'évaluation, non sur
l'identifiant de correction — celui-ci change à la réouverture, et chercher par lui
ferait conclure à tort « aucun bilan produit ».

**Anti-copier-coller.** Les cinq objectifs de séance sont distincts et se retrouvent
dans le document rendu. Deux scénarios de correction différents produisent des
sections « essentiel », « score brut » et « consolidation » différentes, tandis que
le cadre institutionnel reste stable.

**Lecture du dossier.** Un tableau de suivi vierge ne produit aucune observation ;
la contre-épreuve vérifie qu'un tableau renseigné est bien détecté ; un dossier
illisible ne fait pas échouer le pipeline.

**Immutabilité et confidentialité.** 60 artefacts distribués, `changed = 0`,
`missing = 0`, avant et après le pipeline. Aucune observation réelle, aucune donnée
générale saisie.

## Deux défauts trouvés par les tests, et corrigés

1. **L'empreinte des faits ne se vérifiait pas elle-même.** Elle était calculée avant
   d'être insérée dans la charge utile ; la recalculer donnait une autre valeur. Le
   calcul exclut désormais sa propre clé.
2. **La péremption ne détectait pas une réouverture.** La recherche portait sur
   l'identifiant de correction, qui change précisément dans ce cas. Elle porte
   désormais sur l'évaluation.
