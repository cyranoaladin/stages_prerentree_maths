# Règles du bilan longitudinal

## 1. La hiérarchie de preuve

| niveau | ce qui l'établit | autorise à écrire « acquis » |
| --- | --- | --- |
| **A** | un critère noté sur la copie de clôture, rattaché à la compétence | oui |
| **B** | une observation écrite de l'enseignant, une production documentée | non |
| **C** | la compétence figure au programme d'une séance ou d'une remédiation | non |
| **D** | inférence, sans preuve directe | non |

Une preuve de niveau C établit **ce qui a été proposé**, jamais ce qui a été acquis.

Interdit : « S2 a consolidé définitivement les fractions. »
Autorisé : « Les fractions ont fait l'objet d'un travail ciblé en S2. »
Puis, si l'évaluation le permet : « L'évaluation de clôture apporte plusieurs
éléments positifs sur cette compétence. »

## 2. Aucune progression chiffrée

Le positionnement initial est qualitatif et par domaine ; l'évaluation finale est
critériée et par compétence. Les deux échelles ne sont pas parallèles, et les
réponses item par item du diagnostic ne sont pas conservées.

`mastery_delta = null`, sans exception. Ni « +35 % », ni « +2 niveaux ».

## 3. La trajectoire qualitative

| statut | lecture |
| --- | --- |
| `CONSOLIDATION_OBSERVEE` | plusieurs indicateurs positifs concordants sur un point signalé au départ |
| `FRAGILITE_INITIALE_EN_VOIE_DE_RESOLUTION` | indicateurs positifs, encore partiels |
| `ACQUIS_ACTUELLEMENT_DISPONIBLE` | l'appui constaté au départ se retrouve |
| `REUSSITE_A_CONFIRMER` | réussite obtenue juste après le travail sur la notion |
| `FRAGILITE_INITIALE_CONFIRMEE` | le point signalé se retrouve, sans travail nourri |
| `FRAGILITE_PERSISTANTE` | la difficulté résiste malgré le travail conduit |
| `PREUVE_FINALE_INSUFFISANTE` | l'évaluation ne dit rien sur ce point |
| `BRIDGE_PROMISING` | première aisance encourageante sur une notion de l'année à venir |
| `BRIDGE_FIRST_EXPOSURE` | première rencontre avec une notion de l'année à venir |

## 4. Couverture et maîtrise ne se confondent jamais

`coverage` ∈ {NONE, LIGHT, MODERATE, STRONG} décrit le **travail fourni**. Il se
calcule sur le nombre de séances, la reprise en séance 5 et l'existence d'une
remédiation nominative. Il est affiché à côté de l'état final, jamais fusionné avec
lui : beaucoup travaillé ne vaut pas acquis.

## 5. Récence

Une compétence retravaillée puis évaluée moins d'une heure plus tard donne
`post_test_context = immediate_after_remediation`, `retention_status =
not_yet_verified`, statut `REUSSITE_A_CONFIRMER`, et un mini-test différé en
semaine 2.

## 6. Passerelles

Une notion du programme de l'année à venir n'est jamais un prérequis manquant. Elle
ne produit aucune priorité N−1, ne porte aucun rang de priorité, et son échec
s'écrit « sera naturellement reprise en classe dans les premières semaines ».
Le mot « lacune » est proscrit du document parents, partout.

## 7. Isolation des périmètres

Un critère de passerelle ne peut jamais diminuer un score N−1, ajouter une erreur au
profil N−1, augmenter le nombre de preuves N−1, ni modifier la consolidation N−1 —
même lorsqu'il partage le `skill_id` historique d'un prérequis. L'agrégation se fait
sur la clé composite `(analysis_skill_id, curriculum_scope)`.

## 8. Données incomplètes

Une source absente est enregistrée avec `present = False` et un motif. Elle n'est
jamais reconstituée. Si le diagnostic initial manque, le bilan reste possible, mais
écrit : « Le dossier disponible ne permet pas de reconstituer un positionnement
initial complet », et ne propose aucune comparaison.
