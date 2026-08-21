# S5 — couche post-distribution V3

Les livrets et les évaluations de la séance 5 ont été **imprimés et distribués**. Ils
sont la version contractuelle. Ce répertoire ne les modifie pas : il construit, à côté
d'eux, de quoi les corriger équitablement et en tirer des conclusions défendables.

> On ne modifie pas ce que l'élève a reçu ; on améliore ce que nous pouvons légitimement
> conclure de ce qu'il a produit.

## Par où commencer

| vous voulez… | lisez |
| --- | --- |
| comprendre la règle du jeu | `POST_DISTRIBUTION_POLICY.md` |
| savoir ce que mesure chaque point du sujet | `EVALUATION_INTERPRETATION_MATRIX.md` |
| corriger la copie d'un élève | `correction_overlays/<élève>/TEACHER_NOTES.md` |
| savoir pourquoi un critère est classé « passerelle » | `curriculum_scope/SCOPE_RATIONALE.md` |
| sécuriser une formulation à l'oral | `teacher_guidance/CLARIFICATIONS_ORALES_S5.md` |
| savoir ce qui a été vérifié, et comment | `SCIENTIFIC_AUDIT_POST_DISTRIBUTION.md` |
| rédiger le bilan parents | `teacher_guidance/GABARIT_BILAN_PARENTS.md` |
| revérifier la rétention en semaine 2 | `teacher_guidance/MINI_TEST_DIFFERE_S2.md` |
| l'état des lieux complet, chiffres compris | `QA_POST_DISTRIBUTION.md` |

## Corriger, puis analyser

```bash
cd S5_post_distribution_v3

# 1. copier le gabarit et le renseigner, critère par critère
cp responses/responses_v3_TEMPLATE_elyes-kefi.json \
   responses/responses_elyes-kefi_2026-08-28.json

# 2. analyser
python3 tools/analyze_s5_post_distribution.py \
    --student elyes-kefi \
    --responses responses/responses_elyes-kefi_2026-08-28.json

# 3. après rédaction du bilan, contrôler le langage employé
python3 tools/check_bilan_language.py \
    --bilan reports/bilan_elyes-kefi.md \
    --facts analysis/elyes-kefi/bilan_facts_v3.json \
    --analysis analysis/elyes-kefi/post_stage_analysis_v3.json
```

Trois règles de saisie, sans exception :

1. **critère par critère** — le script refuse un fichier incomplet plutôt que de deviner ;
2. **un code d'erreur appartient au critère qui a échoué**, et à aucun autre ;
3. **une méthode mathématiquement correcte n'est jamais une erreur** — cocher
   `accepted_alternative_method` et écrire l'observation.

## Reconstruire toute la couche

```bash
python3 tools/run_all.py
```

Le script gèle, produit, puis recontrôle. Il ne rend 0 que si
`student_artifacts_changed` vaut 0.

## Vérifier que rien n'a bougé

```bash
python3 tools/freeze_student_artifacts.py --verify
python3 tools/verify_no_regression.py
python3 -m pytest tests/
```

## Ce que ce répertoire contient

```
IMMUTABLE_STUDENT_ARTIFACTS.json   empreintes des 60 fichiers figés
POST_DISTRIBUTION_POLICY.md        la règle du jeu
EVALUATION_INTERPRETATION_MATRIX.md ce que mesure chaque critère
SCIENTIFIC_AUDIT_POST_DISTRIBUTION.md  ce qui a été vérifié, et par quel moyen
QA_POST_DISTRIBUTION.md            l'état des lieux, dettes comprises
CANONICAL_POST_DISTRIBUTION.json   les nombres canoniques
curriculum_scope/                  classement N-1 / passerelle, références, justifications
correction_overlays/<élève>/       politique, overlay de corrigé, notes de correction
responses/                         gabarits de saisie V3, un par élève
analysis/                          sorties de l'analyseur, une fois la correction saisie
reports/                           non-régression, audit pédagogique, bilans
teacher_guidance/                  clarifications orales, mini-test différé
schemas/                           schémas JSON V3
tools/                             les scripts
tests/                             le jeu de tests
source_evidence/                   vérification de la traçabilité S1-S4
```

## Ce qui n'est pas ici, et pourquoi

Aucun sujet, aucun corrigé réécrit, aucune régénération de PDF. Les documents élèves
restent dans `S5_cloture/`, intacts. Le corrigé d'origine y reste également : il est la
preuve de ce qui existait au moment de la distribution. L'overlay ne le remplace pas, il
s'y superpose.

`tools/make_release.py`, dans `S5_cloture`, ne doit pas être lancé sans lire d'abord la
section « Sécurité » de `QA_POST_DISTRIBUTION.md`.
