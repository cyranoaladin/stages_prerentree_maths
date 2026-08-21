# S5_cloture — séance 5 de clôture, stages de pré-rentrée 2026-2027

Séance finale individualisée pour les **15 couples élève × matière** attestés par les
dossiers nominatifs du dépôt : 13 élèves de mathématiques répartis sur quatre niveaux,
et 2 élèves de Première NSI.

Chaque séance dure **2 heures** : 1 h 15 de travail pédagogique, puis 45 minutes
d'évaluation finale, dans deux documents séparés.

**Rien n'a été écrit hors de ce répertoire.** Aucun document S1 à S4 n'a été modifié.

## Par où commencer

| Vous voulez… | Lisez |
|---|---|
| savoir ce qui a été produit, pour qui | `INDEX_S5.md` |
| **quel document distribuer à quel élève** | `CANONICAL_DELIVERY.json` |
| savoir ce qui a été vérifié après la passe corrective | `QA_REPORT_V2.md` |
| la contre-résolution des 100 items | `SCIENTIFIC_AUDIT.md` |
| le rapport qualité de la première livraison | `QA_REPORT.md` |
| comprendre sur quoi la personnalisation repose | `_audit/AUDIT_S1_S4.md` |
| connaître les contradictions de sources et les arbitrages | `_audit/conflits_sources.json` |
| animer la séance d'un élève | `<niveau>/<matière>/<Élève>/_ENSEIGNANT/S5_ENSEIGNANT_*.pdf` |
| imprimer pour l'élève | `S5_TRAVAIL_*.pdf` puis, séparément, `S5_EVALUATION_*.pdf` |

## Arborescence

```
S5_cloture/
├── INDEX_S5.md                     tableau de livraison des 15 couples
├── QA_REPORT.md                    rapport qualité et verdict de livraison
├── _audit/                         inventaire, audit S1-S4, conflits, revues, validation
├── _common/
│   ├── nexusS5.sty                 charte graphique partagée par les 45 documents
│   └── blueprints/                 référentiel de compétences des 5 niveaux
├── _teacher_private/               gabarit de bilan, tests déterministes NSI
├── tools/                          génération, validation, analyse, rapports, tests
├── _build_logs/                    journaux de compilation
└── <niveau>/<matière>/<Élève>/
    ├── S5_TRAVAIL_*.tex / .pdf         75 min, aucun corrigé
    ├── S5_EVALUATION_*.tex / .pdf      45 min, aucun corrigé, aucun barème
    ├── student_learning_profile.json
    ├── evaluation_blueprint.json
    ├── responses_TEMPLATE.json
    ├── post_stage_analysis_schema.json
    ├── four_week_action_plan_TEMPLATE.json
    └── _ENSEIGNANT/                    tout ce qui révèle une réponse attendue
        ├── S5_ENSEIGNANT_*.tex / .pdf
        ├── evaluation_manifest.json
        ├── answer_key.json
        └── README.md
```

## Reproduire la livraison

```bash
python3 S5_cloture/tools/build_audit.py            # inventaire et audit
python3 S5_cloture/tools/generate_s5.py            # 45 .tex + 105 JSON
./S5_cloture/tools/build_pdf.sh                    # 45 PDF
python3 S5_cloture/tools/validate_s5.py            # contrôles bloquants
python3 S5_cloture/tools/review_personnalisation.py
python3 S5_cloture/tools/audit_docimologie.py
python3 S5_cloture/tools/tests/test_analyze_s5.py
```

La génération est déterministe : relancer `generate_s5.py` reproduit exactement les
mêmes fichiers.

## Après la passation

Les quatre couches sont séparées : données brutes saisies, calcul déterministe,
interprétation pédagogique, rédaction. **Aucune affirmation chiffrée ne doit provenir
d'ailleurs que de la couche de calcul.**

```bash
cp .../responses_TEMPLATE.json .../responses_2026-08-28.json   # 1. saisir
python3 S5_cloture/tools/analyze_s5.py --student <id> --responses .../responses_2026-08-28.json
python3 S5_cloture/tools/render_bilan.py --facts .../bilan_facts.json \
    --out-parents .../BILAN_PARENTS.md --out-enseignant .../_ENSEIGNANT/SYNTHESE.md
```

`python3 S5_cloture/tools/analyze_s5.py --list-students` donne les identifiants.

## Quatre règles qui traversent toute la livraison

1. **Travaillé n'est pas acquis.** Les tableaux d'observation S1 à S4 des dossiers
   individuels sont vierges : aucune preuve n'existe entre le diagnostic initial et
   aujourd'hui. Tout statut porté avant l'évaluation décrit un état de départ.
2. **Aucune progression chiffrée.** Les réponses de l'élève aux 18 questions du
   positionnement initial n'ont pas été conservées ; le dossier n'en garde qu'un statut
   par domaine. Un statut n'est pas une mesure : `mastery_delta` vaut `null` pour toutes
   les compétences, le schéma JSON l'impose, et un test le vérifie. Les statuts employés
   sont `indicative_skill_comparison`, `post_only` et `not_comparable` ; `parallel_measures`
   existe mais reste inutilisé, faute de mesures appariées.
3. **Réussir juste après la reprise n'est pas consolider.** Toute compétence retravaillée
   pendant la séance puis évaluée moins d'une heure plus tard porte
   `post_test_context: immediate_after_remediation` et `retention_status: not_yet_verified`.
   Un mini-test différé est inscrit en semaine 2 du plan de rentrée.
4. **Les scores viennent des critères.** Chaque critère de barème porte une compétence
   unique et un type de preuve ; la saisie se fait critère par critère, et les scores par
   compétence en sont la somme. Aucune répartition uniforme.

## Durées

Aucune durée n'est imposée. `data/timing.py` estime chaque item depuis son contenu
(lecture, traitement, rédaction) ; `audit_docimologie.py` recalcule une seconde durée
depuis le seul barème, sans entrée commune. La plus prudente des deux fait foi :
elle va de 38,7 à 41,8 minutes selon les élèves, pour une épreuve de 45 minutes.

## Exécution du code des élèves (NSI)

`_teacher_private/tests_s5_nsi.py` **refuse d'exécuter quoi que ce soit par défaut**.
Deux modes : `--mode relu` (sous-processus, explicitement **non sandboxé**, réservé à une
copie relue ligne par ligne) et `--mode conteneur` (conteneur jetable, sans réseau, en
lecture seule, utilisateur non privilégié ; l'image doit être présente localement).
