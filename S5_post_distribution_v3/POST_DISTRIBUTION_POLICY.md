# Politique post-distribution — séance 5, promotion 2026-2027

## Le principe, en une phrase

On ne modifie pas ce que l'élève a reçu ; on améliore ce que nous pouvons légitimement
conclure de ce qu'il a produit.

## Ce qui est figé, et ce que « figé » veut dire

Les trente PDF remis aux quinze élèves — un livret de travail et une évaluation par
couple élève × matière — ont été imprimés et distribués. Ils constituent la version
contractuelle. Les trente sources LaTeX correspondantes sont figées avec eux : sans
cela, la source et le document remis pourraient diverger sans que rien ne le signale.

Ces soixante fichiers sont empreintés dans `IMMUTABLE_STUDENT_ARTIFACTS.json`. Ils ne
doivent être ni modifiés, ni régénérés, ni recompilés, ni remplacés, ni renumérotés, ni
réordonnés. Aucun outil de cette couche n'ouvre l'un d'eux en écriture : la fonction
d'écriture partagée refuse, par construction, tout chemin situé hors de
`S5_post_distribution_v3/`.

Le contrôle est mécanique et rejouable :

```
python3 tools/freeze_student_artifacts.py --verify
python3 tools/verify_no_regression.py
```

`student_artifacts_changed` doit valoir zéro. S'il vaut autre chose, la mission est en
échec, quelle que soit la qualité du reste.

## Ce que la couche post-distribution ajoute

Rien qui ressemble à un sujet. Elle ajoute une lecture :

- un classement curriculaire critère par critère — acquis de l'année N−1, ou passerelle
  vers l'année N ;
- un barème équitable pour les questions dont la formulation imprimée appelle une
  correction prudente ;
- un modèle d'erreurs attaché au critère, et non plus à l'item ;
- une mesure de la force de la preuve disponible pour chaque compétence ;
- un signalement de ce qui a été évalué juste après remédiation ;
- un plan de quatre semaines qui distingue la consolidation d'un prérequis de la reprise
  d'une découverte ;
- des faits structurés à partir desquels un bilan peut être écrit sans surinterprétation.

## Les deux objectifs de la séance, et pourquoi il faut les séparer

La séance finale poursuivait deux buts distincts : vérifier les acquis de l'année N−1
indispensables à l'entrée en N, et créer des passerelles vers certaines notions de
l'année N. Les deux sont pédagogiquement légitimes. Les fondre dans un même indicateur
ne l'est pas : un élève qui découvre le produit de deux relatifs le jour même n'a pas
une « lacune » quand il se trompe. Il n'a pas encore appris.

D'où deux décomptes séparés, et jamais additionnés en un seul jugement :

```json
"n_minus_1_consolidation": { "earned": …, "available": …, "percentage": … }
"bridge_n_readiness":      { "earned": …, "available": …, "percentage": … }
```

Le second n'est pas une mesure d'acquisition attendue. Il mesure une première
disponibilité.

## Le score sur 20 n'est pas le diagnostic

Le total du sujet est conservé et communiqué sous un nom qui dit ce qu'il est : **score
brut au sujet de clôture**. Il ne doit jamais être présenté comme un score de
consolidation, une progression, un niveau N−1 ou une maîtrise des prérequis. Selon
l'élève, il contient de 0 à 5,25 points de passerelle sur 20.

## La règle de classement

Un critère est classé :

- `n_minus_1` lorsque la question imprimée peut être traitée entièrement avec des
  notions de l'année N−1 ;
- `bridge_n` lorsque la voie directe prévue par la question mobilise une notion du
  programme de l'année N ;
- `mixed` lorsqu'un même critère, indivisible tel qu'il a été imprimé, rétribue les deux.
  Il est alors éclaté en sous-critères analytiques **virtuels**, dont la somme des points
  est strictement égale aux points du critère d'origine. Le sujet papier, lui, ne bouge
  pas.

La source du classement n'est pas une opinion : c'est le livret remis à l'élève, qui
énonce lui-même, en phase 4, ce qui est réinvesti et ce qui est nouveau. Les
justifications figurent une par une dans `curriculum_scope/SCOPE_RATIONALE.md`.

## Ce qu'un échec sur une passerelle ne peut jamais produire

Ni `fragile`, ni `non acquis`, ni `lacune`, ni priorité P1 ou P2 de remédiation N−1, ni
jugement négatif. Les seuls statuts disponibles sont `first_exposure`,
`not_yet_installed`, `bridge_to_revisit` et `no_conclusion` ; les seules actions de plan
sont `BRIDGE_REVISIT` et `DISCOVERY_TO_CONTINUE`.

## Les erreurs appartiennent au critère

Un code d'erreur se saisit sur le critère qui a effectivement échoué, et sur lui seul. Il
ne se propage ni aux autres critères de l'item, ni aux autres compétences de l'item.
L'analyseur refuse un code d'erreur porté sur un critère intégralement réussi.

## Une méthode correcte n'est jamais une erreur

Développer une équation-produit avant de la résoudre est moins efficace ; ce n'est pas
faux. Calculer un troisième côté par Pythagore pour employer ensuite le cosinus est plus
long ; c'est correct. Ces cas se cochent `accepted_alternative_method` et se commentent
en observation de stratégie. Jamais un code `CONCEPT` tant que le raisonnement tient.

## Ce qui se fait devant une question ambiguë

Dans cet ordre, sans en sauter :

1. retenir l'interprétation la plus favorable compatible avec la consigne imprimée ;
2. accepter toute méthode mathématiquement correcte ;
3. n'exiger aucune justification que la consigne ne demande pas explicitement ;
4. neutraliser le sous-critère si aucune correction équitable n'est possible ;
5. marquer `evidence_quality: limited_by_prompt`.

Une ambiguïté de sujet est un défaut du sujet. Elle ne devient pas une faiblesse
attribuée à l'élève.

## Aucune progression chiffrée

Les réponses initiales item par item n'ont pas été conservées : le dossier ne garde qu'un
statut qualitatif par domaine. Convertir « fragile » en 1 et « maîtrisé » en 3 pour en
soustraire l'un de l'autre produirait un écart sans valeur de mesure. `mastery_delta`
vaut donc `null` pour les quinze couples, et le contrôleur de langage refuse toute
phrase de progression chiffrée dans un bilan.

Les formulations autorisées sont qualitatives : fragilité initialement documentée,
réussite actuelle observée, fragilité persistante, résultat final non comparable,
première confrontation réussie, compétence à vérifier dans la durée.

## L'effet de récence

Une compétence retravaillée pendant les soixante-quinze premières minutes puis évaluée
moins d'une heure plus tard porte `post_test_context: immediate_after_remediation` et
`retention_status: not_yet_verified`. Une réussite y signifie « réussite immédiate après
remédiation », pas « consolidation durable ». Un mini-test différé de semaine 2 est
prévu pour ces compétences, et pour elles seules.

## Si la séance a déjà eu lieu

Aucune correction rétroactive n'est demandée à l'élève. Les approximations relevées dans
les supports sont consignées comme limites d'interprétation, et le bilan les respecte.

## Ordre d'exploitation après correction

1. saisir les scores critère par critère ;
2. saisir les erreurs sur le seul critère concerné ;
3. lancer `tools/analyze_s5_post_distribution.py` ;
4. lire la consolidation N−1, les observations de passerelle, le profil d'erreurs, la
   force de preuve et les besoins de rétention différée ;
5. produire le plan de quatre semaines ;
6. produire les faits structurés ;
7. seulement ensuite, faire rédiger le bilan parents, puis le passer à
   `tools/check_bilan_language.py`.

Le script calcule. Le modèle de langage interprète. Il ne recalcule ni ne corrige aucun
score.
