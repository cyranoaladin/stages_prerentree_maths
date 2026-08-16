# PROMPT CLAUDE CLI — INTÉGRATION D’INES KEFI ET D’ELYES KEFI, REBUILD COMPLET, QA ET PUSH GITHUB

## Rôle

Vous êtes **Claude CLI**, lead technique, architecte documentaire, ingénieur pédagogique en mathématiques, spécialiste des chaînes de génération Markdown → HTML → PDF, de l’accessibilité, de l’édition imprimée et de la qualité logicielle.

Vous travaillez directement dans le dépôt local correspondant à :

```text
https://github.com/cyranoaladin/stages_prerentree_maths
```

Votre mission n’est pas de produire un audit théorique. Vous devez **inspecter, corriger, intégrer, générer, tester, versionner, pousser et vérifier à distance**.

---

# 1. Décision propriétaire et autorisation de publication

Décision de gouvernance explicite, définitive et non négociable :

- le propriétaire du dépôt **autorise le versionnement et le push de l’intégralité du dossier courant** ;
- cette autorisation inclut les documents nominatifs, les bilans source, les PDF, les packs et les artefacts déjà prévus par l’architecture du dépôt ;
- vous ne devez ni remettre en question cette décision, ni demander une nouvelle confirmation, ni bloquer le travail au motif de la présence de données nominatives ;
- vous devez néanmoins continuer à refuser toute fuite de **secret technique** : token, mot de passe, clé API, clé privée, cookie, fichier `.env`, credential cloud ou chaîne d’authentification.

La séparation logique public/privé du portail, les badges « confidentiel » et les scans anti-contamination doivent être maintenus, même si tous les fichiers du dépôt sont autorisés au push.

---

# 2. Baseline connue à vérifier, jamais à supposer aveuglément

Le dépôt distant comporte actuellement :

```text
REMOTE = https://github.com/cyranoaladin/stages_prerentree_maths
DEFAULT_BRANCH = main
KNOWN_MAIN_SHA = 551bb6c9aa85176ab994f50c33771cb695d491ae
KNOWN_MAIN_MESSAGE = "Refonte complete du paquet de documentation stages maths 2026"
```

La livraison précédente déclarait notamment :

```text
LEVEL_COUNT=4
SESSION_COUNT=5
STUDENT_COUNT=11
ACTIVE_DOCUMENT_COUNT=149
GENERATED_PDF_COUNT=227
COMBINED_PACK_COUNT=78
BROKEN_LINK_COUNT=0
ORPHAN_ACTIVE_FILE_COUNT=0
DUPLICATE_ACTIVE_FILE_COUNT=0
MATH_ERROR_REMAINING_COUNT=0
STUDENT_CORRECTION_LEAK_COUNT=0
CROSS_STUDENT_PII_LEAK_COUNT=0
PDF_STRUCTURAL_FAILURE_COUNT=0
PDF_VISUAL_DEFECT_COUNT=0
BUILD_REPRODUCIBILITY_MISMATCH_COUNT=0
```

La chaîne canonique existante est annoncée comme :

```bash
python3 tools/build.py audit
python3 tools/build.py html
python3 tools/build.py pdf
python3 tools/build.py packs
python3 tools/build.py qa
python3 tools/build.py all

make audit
make build
make pdf
make packs
make qa
make all
make test
```

Le dépôt utilise notamment :

- `tools/build.py` ;
- `content/catalog.json`, généré ;
- `MANIFEST_PUBLIC.csv` ;
- `MANIFEST_PRIVATE.csv` ;
- `dist/site-public/` ;
- `dist/site-private/` ;
- `dist/pdf/` ;
- `dist/packs/` ;
- `reports/FINAL_DELIVERY_REPORT.md` ;
- les répertoires actifs `4e`, `3e`, `2nde`, `1ere_spe` ;
- un module séparé `1re_nsi`, déjà présent dans l’arborescence et à ne pas régresser.

Vous devez d’abord vérifier ces faits avec Git et le système de fichiers. En cas d’écart, documentez l’écart et prenez l’état réellement observé comme baseline.

---

# 3. Nouveaux élèves à intégrer

## 3.1 Ines KEFI — entrée en Quatrième

Répertoire canonique attendu :

```text
4e/04_NOMINATIFS/Ines_Kefi/
```

Fichiers source attendus, avec normalisation des noms si nécessaire :

```text
4e_Dossier_Individuel_Ines_Kefi.md
4e_Remediation_Ciblee_Ines_Kefi_ELEVE.md
4e_Remediation_Ciblee_Ines_Kefi_PROF_Corrige.md
bilan-nexus-eleve_ines_kefi_maths.pdf
bilan-nexus-parents_ines_kefi_maths.pdf
```

Profil à respecter :

- 18 questions traitées sur 18 ;
- calibration réussite–confiance : 67 % ;
- domaines solides : proportionnalité, aires et périmètres, statistiques ;
- domaines à rectifier en priorité : nombres relatifs, fractions, géométrie ;
- domaine à installer : calcul littéral ;
- les erreurs sûres doivent être confrontées avant l’entraînement.

Parcours prévu dans les cinq séances :

1. **S1 — nombres relatifs et fractions** : priorité de confrontation et reconstruction ;
2. **S2 — aires et périmètres** : entretien, transfert et approfondissement, sans reprise élémentaire inutile ;
3. **S3 — calcul littéral** : installation structurée, substitution, réduction, distributivité et première équation ;
4. **S4 — géométrie** : confrontation des conceptions, angles, symétrie centrale, parallélogramme et justification ;
5. **S5 — synthèse** : mesure des progrès, transfert, contrôle de vraisemblance et plan de septembre.

## 3.2 Elyes KEFI — entrée en Troisième

Répertoire canonique attendu :

```text
3e/04_NOMINATIFS/Elyes_Kefi/
```

Fichiers source attendus :

```text
3e_Dossier_Individuel_Elyes_Kefi.md
3e_Remediation_Ciblee_Elyes_Kefi_ELEVE.md
3e_Remediation_Ciblee_Elyes_Kefi_PROF_Corrige.md
bilan-nexus-eleve_elyes_kefi_maths.pdf
bilan-nexus-parents_elyes_kefi_maths.pdf
```

Profil à respecter :

- 18 questions traitées sur 18 ;
- calibration réussite–confiance : 82 % ;
- domaines solides : nombres relatifs, puissances, équations, proportionnalité, géométrie, trigonométrie ;
- domaines à rectifier en priorité : fractions, calcul littéral, statistiques ;
- les réponses fausses assurées doivent être confrontées puis reconstruites.

Parcours prévu :

1. **S1 — calcul numérique** : priorité fractions ; relatifs et puissances en maîtrise/approfondissement ;
2. **S2 — calcul littéral, équations, proportionnalité** : priorité calcul littéral ; équations et proportionnalité en transfert ;
3. **S3 — Pythagore et Thalès** : entretien et approfondissement, sans réenseignement massif ;
4. **S4 — trigonométrie** : entretien, problèmes de transfert et anticipation raisonnée ;
5. **S5 — statistiques et probabilités** : priorité statistiques ; probabilités et synthèse en maîtrise.

Les PDF source sont immuables : ne pas les modifier, réencoder, compresser, renommer intérieurement ou régénérer.

---

# 4. Contraintes absolues

1. Ne perdez aucun fichier local, suivi ou non suivi.
2. Ne faites aucun `git reset --hard`, `git clean -fd`, rebase destructif ou force-push.
3. N’écrasez pas les ajouts déjà copiés localement.
4. N’éditez pas manuellement un artefact généré si sa source ou le générateur peut être corrigé.
5. Ne laissez aucun PDF ou HTML dérivé actif dans un répertoire source si l’architecture canonique exige sa génération sous `dist/`.
6. Ne placez aucun dossier nominatif dans le portail public.
7. Ne laissez aucun corrigé dans un document ou pack élève.
8. Ne fabriquez aucun résultat, aucun compteur ni aucune validation visuelle.
9. Ne déclarez aucun gate vert sans preuve reproductible.
10. Ne modifiez pas le contenu du module `1re_nsi` sans nécessité démontrée. Toute modification de ce module doit être explicitement justifiée et testée.
11. Ne vous arrêtez pas après l’ouverture d’une PR : allez jusqu’au push, aux contrôles distants et au merge si les gates sont verts et que les permissions le permettent.
12. La dette résiduelle finale doit être nulle pour le périmètre de ce lot.

---

# 5. Phase 0 — Gel, sauvegarde et état Git

Exécutez et conservez les sorties utiles, sans exposer de données inutiles :

```bash
pwd
git rev-parse --show-toplevel
git remote -v
git status --short --branch
git rev-parse HEAD
git fetch origin --prune
git rev-parse origin/main
git log --oneline --decorate -n 10
find . -maxdepth 3 -type f | sort
```

## 5.1 Préserver le travail local

Avant toute transformation :

- sauvegardez la liste des fichiers suivis, modifiés et non suivis ;
- créez une archive de sécurité **hors dépôt** avec permissions restrictives ;
- calculez les SHA-256 des quatre nouveaux PDF source ;
- exportez un patch des modifications textuelles éventuelles ;
- ne copiez aucun secret technique dans les rapports.

Si la branche courante n’est pas propre, conservez les ajouts et créez une branche de travail sans les perdre.

Branche recommandée :

```text
feat/add-ines-elyes-documentation-20260816
```

La branche doit partir du dernier `origin/main`, sauf si le travail local contient déjà les ajouts non commités : dans ce cas, préservez-les puis rattachez-les proprement à la branche sans perte.

Produisez un état baseline :

```text
BASE_HEAD_SHA=
ORIGIN_MAIN_SHA=
WORKTREE_DIRTY_COUNT=
UNTRACKED_FILE_COUNT=
NEW_INES_FILE_COUNT=
NEW_ELYES_FILE_COUNT=
```

---

# 6. Phase 1 — Audit de l’import et rectification de l’arborescence

## 6.1 Inventaire exhaustif

Recherchez toutes les variantes :

```bash
find . -iname '*ines*' -o -iname '*elyes*' -o -iname '*kefi*'
grep -RIl --exclude-dir=.git -E 'Ines[[:space:]]+K[Ee][Ff][Ii]|Elyes[[:space:]]+K[Ee][Ff][Ii]' .
```

Pour chaque fichier trouvé, classez-le :

- source canonique ;
- PDF source original ;
- source Markdown opérationnelle ;
- artefact généré ;
- doublon exact ;
- doublon divergent ;
- fichier orphelin ;
- fichier mal nommé ;
- fichier situé dans le mauvais répertoire.

## 6.2 Arborescence canonique

Dans chacun des deux répertoires nominatifs actifs, conservez seulement :

- les trois Markdown opérationnels ;
- les deux PDF source originaux.

Les HTML et PDF dérivés doivent être générés sous `dist/`.

Si l’archive d’ajout a placé des PDF dérivés dans `04_NOMINATIFS`, ne les laissez pas actifs en doublon :

- comparez leur contenu avec le futur build ;
- archivez les versions importées dans un sous-dossier horodaté de `_archive/` si une conservation est nécessaire ;
- sinon retirez uniquement les artefacts reproductibles devenus redondants ;
- documentez précisément chaque déplacement ou suppression.

N’utilisez qu’un slug de répertoire :

```text
Ines_Kefi
Elyes_Kefi
```

Utilisez comme nom d’affichage canonique :

```text
Ines KEFI
Elyes KEFI
```

Les variantes historiques `Ines Kefi`, `Elyes Kefi`, différences de casse et variantes Unicode doivent être reconnues comme alias de la même personne pour les scans PII.

## 6.3 Contrôle des nouveaux documents

Comparez Ines aux dossiers existants de Quatrième, notamment Sinda Chikhaoui et Fares Darghouth.

Comparez Elyes aux dossiers existants de Troisième, notamment Fares Laajili, Sarah Bargaoui, Selim Mansouri et Amine Mansouri.

Vérifiez :

- structure des titres ;
- audience ;
- absence de corrigé côté élève ;
- présence d’espaces de réponse ;
- cohérence du plan d’action ;
- cohérence des exercices ciblés avec le diagnostic ;
- exactitude mathématique de tous les énoncés et corrigés ;
- aucune mention d’un autre élève ;
- aucune incohérence entre le bilan source et le dossier généré ;
- aucune surestimation de maîtrise.

---

# 7. Phase 2 — Supprimer le hardcoding et établir une source de vérité

Le fichier `tools/build.py` contient actuellement une liste codée en dur des 11 noms d’élèves. Cette dette doit disparaître.

## 7.1 Registre nominatif canonique

Créez un registre unique, par exemple :

```text
content/students.json
```

Schéma minimal recommandé :

```json
{
  "schemaVersion": "nexus-students-v1",
  "students": [
    {
      "id": "ines-kefi",
      "displayName": "Ines KEFI",
      "aliases": ["Ines Kefi", "INES KEFI", "Ines KEFI"],
      "level": "4e",
      "directory": "4e/04_NOMINATIFS/Ines_Kefi",
      "active": true,
      "sourceStudentReport": "bilan-nexus-eleve_ines_kefi_maths.pdf",
      "sourceParentReport": "bilan-nexus-parents_ines_kefi_maths.pdf"
    }
  ]
}
```

Incluez les 13 élèves, pas uniquement les deux nouveaux.

Ajoutez une validation stricte :

- identifiant unique ;
- nom d’affichage unique ;
- alias non ambigu ;
- niveau valide ;
- répertoire existant ;
- fichiers attendus présents ;
- pas de symlink ;
- pas de sortie hors racine ;
- trois Markdown opérationnels exactement, sauf exception documentée ;
- deux PDF source exactement ;
- aucune collision de slug.

Un schéma JSON ou un validateur Python explicite est requis.

## 7.2 Mise à jour du build

Modifiez `tools/build.py` afin que :

- la liste PII soit chargée depuis le registre ;
- la détection soit insensible à la casse et normalisée Unicode ;
- le nombre d’élèves soit calculé depuis le registre ;
- les packs nominatifs soient dérivés du registre ;
- les liens privés soient générés depuis le registre ;
- aucun nom ne soit codé en dur dans le code ;
- les deux nouveaux élèves soient automatiquement pris en compte ;
- une entrée orpheline ou un dossier non déclaré fasse échouer le build ;
- un élève déclaré sans fichiers complets fasse échouer le build ;
- un dossier nominatif non déclaré fasse échouer le build.

Ajoutez des tests dédiés, au minimum :

```text
tests/test_student_registry.py
tests/test_new_students_integration.py
tests/test_public_private_separation.py
tests/test_nominative_pack_generation.py
```

## 7.3 Catalog et statut QA

`content/catalog.json` est un fichier généré : ne l’éditez pas à la main.

Après un build final réussi :

- les six nouveaux Markdown doivent produire six nouvelles entrées privées ;
- `html_public` doit être nul pour les six ;
- `html_private` doit être présent ;
- `contains_pii` doit être vrai ;
- le bucket PDF doit être `nominatifs-prives`.

Ne laissez pas un champ final trompeur tel que `validation_status: pending_qa` après une livraison déclarée validée. Choisissez une solution propre :

- soit le statut est mis à `validated` après succès du QA ;
- soit ce champ est retiré du catalog et remplacé par un artefact QA séparé, déterministe et lié aux hashes.

Documentez la décision.

## 7.4 Reproductibilité temporelle

Le build ne doit pas dépendre silencieusement de `date.today()`.

Utilisez une valeur déterministe :

- `SOURCE_DATE_EPOCH` ;
- ou la date du commit ;
- ou une version de livraison déclarée dans un fichier de configuration.

Deux builds réalisés dans des environnements propres doivent produire les mêmes hashes, indépendamment de l’heure d’exécution.

---

# 8. Phase 3 — Intégration pédagogique d’Ines dans le niveau 4e

Le groupe Quatrième passe de 2 à 3 élèves.

Mettez à jour toutes les sources actives concernées, sans modifier le test initial ni les bilans source :

```text
4e/05_SOURCES/stage_prerentree_quatrieme_maths.md
4e/01_ENSEIGNANT/4e_Guide_Formateur.md
4e/01_ENSEIGNANT/4e_Tableau_Bord_Enseignant.md
4e/00_MASTER/index.md
4e/00_MASTER/4e_MASTER_Documentation_Stage.md
4e/02_SEANCES/S1/4e_S1_PROF_Fiche.md
4e/02_SEANCES/S2/4e_S2_PROF_Fiche.md
4e/02_SEANCES/S3/4e_S3_PROF_Fiche.md
4e/02_SEANCES/S4/4e_S4_PROF_Fiche.md
4e/02_SEANCES/S5/4e_S5_PROF_Fiche.md
```

Recherchez d’autres fichiers actifs contenant des listes d’élèves, effectifs ou tableaux nominatifs et mettez-les à jour.

## 8.1 Diagnostic collectif recalculé

Ne juxtaposez pas un paragraphe ajouté artificiellement. Recalculez le diagnostic du groupe :

- points communs ;
- différences ;
- groupes de besoin ;
- ordre des remédiations ;
- répartition du temps de l’enseignant ;
- impact sur les parcours de Sinda et Fares ;
- parcours propre d’Ines.

Conservez les cinq thèmes validés. N’ajoutez pas une sixième séance et ne réduisez aucune séance.

## 8.2 Différenciation d’Ines

Dans chaque fiche professeur, ajoutez une ligne ou section réellement exploitable :

- objectif individuel ;
- tâche de départ ;
- niveau de parcours ;
- aide maximale prévue ;
- critère de réussite ;
- tâche de transfert ;
- décision en cas de réussite rapide ou de blocage.

Les exercices communs élèves ne doivent être modifiés que si une amélioration pédagogique générale est justifiée. Dans ce cas, recalculer et recorriger toutes les réponses concernées.

---

# 9. Phase 4 — Intégration pédagogique d’Elyes dans le niveau 3e

Le groupe Troisième passe de 4 à 5 élèves.

Mettez à jour au minimum :

```text
3e/05_SOURCES/stage_prerentree_troisieme_maths.md
3e/01_ENSEIGNANT/3e_Guide_Formateur.md
3e/01_ENSEIGNANT/3e_Tableau_Bord_Enseignant.md
3e/00_MASTER/index.md
3e/00_MASTER/3e_MASTER_Documentation_Stage.md
3e/02_SEANCES/S1/3e_S1_PROF_Fiche.md
3e/02_SEANCES/S2/3e_S2_PROF_Fiche.md
3e/02_SEANCES/S3/3e_S3_PROF_Fiche.md
3e/02_SEANCES/S4/3e_S4_PROF_Fiche.md
3e/02_SEANCES/S5/3e_S5_PROF_Fiche.md
```

Recherchez tous les autres fichiers actifs à mettre à jour.

## 9.1 Diagnostic collectif

Recalculez :

- les besoins communs ;
- les élèves nécessitant une confrontation ;
- les élèves en consolidation ;
- les élèves pouvant approfondir ;
- les groupes tournants ;
- la place d’Elyes sans dégrader les parcours de Sarah, Selim, Amine et Fares.

## 9.2 Différenciation d’Elyes

Elyes ne doit pas refaire inutilement les domaines solides.

Ses tâches prioritaires sont :

- fractions en S1 ;
- calcul littéral en S2 ;
- statistiques en S5.

En S3 et S4, prévoyez des activités de transfert, justification, Thalès, choix de méthode et trigonométrie plus exigeante.

---

# 10. Phase 5 — Cohérence générale de l’arborescence

## 10.1 Sources et artefacts

La convention finale doit être explicite :

- sources actives Markdown dans les dossiers de niveau ;
- bilans PDF source conservés dans les dossiers nominatifs ;
- HTML générés sous `dist/site-public` ou `dist/site-private` ;
- PDF générés sous `dist/pdf` ;
- packs sous `dist/packs` ;
- rapports sous `reports` et copiés dans `dist/reports` ;
- archives historiques sous `_archive`, exclues du catalog actif.

Aucun artefact actif ne doit exister à deux endroits.

## 10.2 Module `1re_nsi`

Le dépôt contient aussi `1re_nsi`, alors que le build mathématique précédent le déclarait hors périmètre.

Résolvez cette incohérence documentaire sans élargir imprudemment le lot :

- préservez le contenu NSI et ses artefacts ;
- vérifiez que ses liens restent valides ;
- mettez à jour le README racine pour décrire honnêtement la présence d’un module NSI séparé ;
- ajoutez-le au registre global de navigation si un portail racine existe ;
- ne l’intégrez au pipeline mathématique que si cette intégration peut être entièrement testée sans régression ;
- sinon documentez clairement : pipeline mathématique canonique + module NSI indépendant ;
- aucun fichier `1re_nsi` ne doit rester orphelin ou invisible depuis la racine.

## 10.3 Accessibilité résiduelle

La livraison précédente conservait 20 sauts de niveaux de titres classés « sérieux mais non critiques ».

Ce lot doit viser :

```text
HTML_CRITICAL_A11Y_COUNT=0
HTML_SERIOUS_A11Y_COUNT=0
```

Corrigez la hiérarchie des titres à la source ou lors du rendu, sans casser la structure pédagogique.

---

# 11. Phase 6 — Génération complète

## 11.1 Dépendances reproductibles

Si le dépôt ne possède pas de fichier de dépendances, ajoutez une définition versionnée et épinglée, par exemple `requirements.lock` ou `pyproject.toml`, couvrant au minimum les versions réellement utilisées :

- WeasyPrint ;
- pypdf ;
- pytest ;
- les autres bibliothèques Python nécessaires.

Documentez les dépendances système :

- Python ;
- Pandoc ;
- qpdf ;
- Poppler ;
- ImageMagick ou outil équivalent pour l’inspection visuelle.

Ne téléchargez aucune police distante.

## 11.2 Build propre

Exécutez depuis un état propre :

```bash
make clean-generated
make test
make all
```

Puis exécutez une seconde génération propre afin de prouver la reproductibilité.

Le build doit produire au minimum :

### Ines KEFI

```text
dist/site-private/4e/04_NOMINATIFS/Ines_Kefi/*.html
dist/pdf/4e/nominatifs-prives/4e_Dossier_Individuel_Ines_Kefi.pdf
dist/pdf/4e/nominatifs-prives/4e_Remediation_Ciblee_Ines_Kefi_ELEVE.pdf
dist/pdf/4e/nominatifs-prives/4e_Remediation_Ciblee_Ines_Kefi_PROF_Corrige.pdf
dist/packs/nominatifs-prives/4e_Ines_Kefi_PACK_TRAVAIL_PERSONNALISE.pdf
dist/packs/nominatifs-prives/4e_Ines_Kefi_DOSSIER_ENSEIGNANT_CONFIDENTIEL.pdf
```

### Elyes KEFI

```text
dist/site-private/3e/04_NOMINATIFS/Elyes_Kefi/*.html
dist/pdf/3e/nominatifs-prives/3e_Dossier_Individuel_Elyes_Kefi.pdf
dist/pdf/3e/nominatifs-prives/3e_Remediation_Ciblee_Elyes_Kefi_ELEVE.pdf
dist/pdf/3e/nominatifs-prives/3e_Remediation_Ciblee_Elyes_Kefi_PROF_Corrige.pdf
dist/packs/nominatifs-prives/3e_Elyes_Kefi_PACK_TRAVAIL_PERSONNALISE.pdf
dist/packs/nominatifs-prives/3e_Elyes_Kefi_DOSSIER_ENSEIGNANT_CONFIDENTIEL.pdf
```

Les noms réels produits par le générateur peuvent varier uniquement si la convention canonique du dépôt impose une autre forme cohérente. Dans ce cas, mettez à jour les liens et documentez la convention.

## 11.3 Deltas attendus

Sous l’hypothèse de trois Markdown actifs par nouvel élève :

```text
STUDENT_COUNT: 11 -> 13
ACTIVE_DOCUMENT_COUNT: 149 -> 155
UNIT_PDF_COUNT: +6
NOMINATIVE_PACK_COUNT: +4
TOTAL_GENERATED_PDF_COUNT: 227 -> 237
```

Ne forcez pas artificiellement ces nombres. Calculez-les à partir du catalog final. Si le delta diffère, expliquez précisément pourquoi et vérifiez qu’aucun document ne manque ou n’est dupliqué.

---

# 12. Phase 7 — QA exhaustif

## 12.1 Audit mathématique

Recalculez indépendamment :

- chaque exercice ciblé d’Ines ;
- chaque exercice ciblé d’Elyes ;
- tous les corrigés ajoutés ou modifiés ;
- tout exercice générique modifié dans les niveaux 4e ou 3e.

Vérifiez :

- unicité des réponses ;
- consignes complètes ;
- données suffisantes ;
- unités ;
- fractions ;
- signes ;
- arrondis ;
- figures ;
- cohérence des trois parcours ;
- absence d’ambiguïté.

Mettez à jour :

```text
reports/MATH_CONTENT_AUDIT.md
reports/SOURCE_ERRATA.md
```

## 12.2 Confidentialité logique

Gates obligatoires :

```text
PUBLIC_OCCURRENCE_INES_COUNT=0
PUBLIC_OCCURRENCE_ELYES_COUNT=0
PUBLIC_STUDENT_ALIAS_OCCURRENCE_COUNT=0
STUDENT_CORRECTION_LEAK_COUNT=0
CROSS_STUDENT_PII_LEAK_COUNT=0
```

Scannez tous les alias des 13 élèves dans :

```text
dist/site-public/
dist/packs/eleves/
dist/pdf/*/eleves/
MANIFEST_PUBLIC.csv
```

Pour chaque pack nominatif, vérifiez qu’il ne contient aucun nom d’un autre élève.

Les versions élève des remédiations ne doivent contenir :

- ni corrigé ;
- ni réponse attendue ;
- ni solution masquée ;
- ni commentaire HTML enseignant ;
- ni métadonnée révélant le corrigé.

## 12.3 Navigation et portail

Vérifiez :

- Ines visible dans la zone privée du niveau 4e ;
- Elyes visible dans la zone privée du niveau 3e ;
- aucun des deux dans la zone publique ;
- recherche privée fonctionnelle sur leur nom et leurs documents ;
- recherche publique sans résultat nominatif ;
- liens HTML, PDF et packs valides ;
- fil d’Ariane ;
- navigation précédente/suivante ;
- page « Suivi nominatif » ;
- page « Packs prêts à imprimer » ;
- trois clics maximum depuis la zone privée vers un dossier nominatif ;
- zéro lien cassé ;
- zéro ressource externe.

## 12.4 Responsive et accessibilité

Testez réellement avec Chromium ou équivalent :

- largeur 320 px ;
- largeur 390 px ;
- tablette ;
- desktop ;
- zoom 200 % ;
- clavier ;
- focus visible ;
- tableaux larges ;
- portail privé avec les 13 élèves.

Vérifiez :

```text
MOBILE_HORIZONTAL_OVERFLOW_COUNT=0
KEYBOARD_BLOCKER_COUNT=0
FOCUS_VISIBILITY_FAILURE_COUNT=0
HTML_CRITICAL_A11Y_COUNT=0
HTML_SERIOUS_A11Y_COUNT=0
```

## 12.5 PDF structurel

Pour tous les PDF :

- `qpdf --check` ;
- A4 portrait ;
- polices incorporées ;
- texte extractible ;
- zéro chiffrement ;
- zéro page vide ;
- métadonnées en français ;
- aucune formule LaTeX brute ;
- aucun `$` orphelin ;
- aucun lien cassé ;
- aucune image manquante.

## 12.6 Inspection visuelle réelle

Ne validez pas les PDF uniquement par `pdftotext`.

1. Comparez les hashes avant/après pour identifier chaque PDF modifié.
2. Rasterisez **chaque page de chaque PDF nouveau ou modifié**.
3. Inspectez visuellement :
   - fractions ;
   - exposants ;
   - indices ;
   - racines ;
   - tableaux ;
   - lignes coupées ;
   - titres orphelins ;
   - espaces de réponse ;
   - cartes à découper ;
   - pieds de page ;
   - mention confidentielle ;
   - ordre des pages dans les packs.
4. Contrôlez au minimum un échantillon représentatif de tous les PDF non modifiés afin de détecter une régression globale du moteur.
5. Conservez les preuves sous un répertoire de rapport non ambigu.

Mettez à jour :

```text
reports/PDF_STRUCTURAL_QA.md
reports/PDF_VISUAL_QA.md
reports/NAVIGATION_QA.md
reports/ACCESSIBILITY_QA.md
reports/UX_AUDIT.md
reports/CONTENT_GAPS.md
```

Aucun défaut bloquant ou sérieux ne doit rester ouvert.

## 12.7 Reproductibilité

Faites deux builds propres dans deux répertoires indépendants avec la même source :

- même liste de fichiers ;
- mêmes SHA-256 ;
- mêmes nombres de pages ;
- mêmes manifests ;
- aucun timestamp variable non maîtrisé.

Gate :

```text
BUILD_REPRODUCIBILITY_MISMATCH_COUNT=0
```

---

# 13. Phase 8 — CI GitHub

Le dépôt ne doit pas dépendre uniquement d’un contrôle manuel local.

S’il n’existe pas de CI, créez :

```text
.github/workflows/documentation-ci.yml
```

Le workflow doit :

1. checkout ;
2. installer Python et les dépendances verrouillées ;
3. installer les dépendances système nécessaires ;
4. exécuter `make test` ;
5. exécuter `make all` ;
6. exécuter les scans de secrets ;
7. exécuter les gates de confidentialité logique ;
8. vérifier `git diff --exit-code` après génération ;
9. publier les rapports QA comme artefact de workflow ;
10. échouer au moindre fichier généré non versionné, lien cassé, fuite de corrigé, contamination nominative ou erreur PDF.

Évitez les actions non épinglées sur une version majeure non maîtrisée.

---

# 14. Phase 9 — Commits, push, PR et merge

## 14.1 Commits atomiques recommandés

```text
1. chore(build): centralize student registry and harden deterministic QA
2. feat(students): add Ines KEFI and Elyes KEFI to 4e and 3e stages
3. docs(dist): regenerate portals PDFs packs manifests and QA reports
```

Adaptez si nécessaire, mais gardez des commits lisibles.

## 14.2 Push

Poussez la branche :

```bash
git push -u origin feat/add-ines-elyes-documentation-20260816
```

Ouvrez une PR avec :

- baseline ;
- fichiers source ajoutés ;
- mises à jour pédagogiques ;
- évolution du registre ;
- deltas de catalog/PDF/packs ;
- résultats QA ;
- preuve de reproductibilité ;
- absence de fuite publique logique ;
- liste des rapports.

## 14.3 Revue

Effectuez une auto-revue complète du diff.

Si Codex/Cubic ou un autre reviewer est disponible, demandez une revue. Corrigez tout commentaire pertinent. Ne bloquez pas le lot uniquement si un reviewer payant est indisponible : la décision owner autorise la poursuite avec une revue locale renforcée et des gates verts.

## 14.4 Merge

Lorsque tous les checks sont verts et qu’aucun thread bloquant n’est ouvert :

- fusionnez la PR dans `main` ;
- ne faites pas de force-push ;
- supprimez la branche distante après merge ;
- mettez à jour la branche locale `main` ;
- vérifiez l’égalité :

```text
LOCAL_MAIN_SHA = ORIGIN_MAIN_SHA = MERGE_SHA
```

Option recommandée : tag annoté

```text
stages-maths-2026.2-ines-elyes
```

Le tag doit pointer exactement sur le SHA fusionné.

---

# 15. Vérification distante après push

Vérifiez sur GitHub :

- présence des deux nouveaux répertoires ;
- présence des 10 fichiers source attendus ;
- présence du registre des 13 élèves ;
- présence des PDF générés et packs ;
- manifests à jour ;
- rapport final à jour ;
- aucun fichier local oublié ;
- aucun fichier inattendu ;
- aucun secret détecté ;
- workflow CI vert ;
- SHA local et distant identiques.

---

# 16. Rapport final obligatoire

Mettez à jour :

```text
reports/FINAL_DELIVERY_REPORT.md
CHANGELOG.md
README.md
QUICK_START.md
PRINT_GUIDE.md
PRINT_CHECKLIST.csv
MANIFEST_PUBLIC.csv
MANIFEST_PRIVATE.csv
```

Le rapport final doit contenir exactement les sections suivantes :

1. **Baseline Git et fichiers locaux**
2. **Arborescence avant/après**
3. **Fichiers Ines ajoutés**
4. **Fichiers Elyes ajoutés**
5. **Registre nominatif et suppression du hardcoding**
6. **Mise à jour pédagogique du groupe 4e**
7. **Mise à jour pédagogique du groupe 3e**
8. **Catalog et manifests**
9. **PDF unitaires et packs**
10. **Portails et navigation**
11. **Confidentialité logique**
12. **Audit mathématique**
13. **Accessibilité**
14. **QA PDF structurel**
15. **QA visuel**
16. **Reproductibilité**
17. **Tests locaux**
18. **CI GitHub**
19. **Commits, PR, merge et tag**
20. **État distant final**
21. **Dette résiduelle**
22. **Statut final**

Compteurs obligatoires :

```text
BASE_HEAD_SHA=
FINAL_MAIN_SHA=
TAG_SHA=
STUDENT_COUNT_BEFORE=
STUDENT_COUNT_AFTER=
ACTIVE_DOCUMENT_COUNT_BEFORE=
ACTIVE_DOCUMENT_COUNT_AFTER=
NEW_ACTIVE_DOCUMENT_COUNT=
GENERATED_HTML_COUNT=
UNIT_PDF_COUNT=
COMBINED_PACK_COUNT=
TOTAL_GENERATED_PDF_COUNT=
TOTAL_GENERATED_PDF_PAGE_COUNT=
BROKEN_LINK_COUNT=
ORPHAN_ACTIVE_FILE_COUNT=
DUPLICATE_ACTIVE_FILE_COUNT=
MATH_ERROR_REMAINING_COUNT=
STUDENT_CORRECTION_LEAK_COUNT=
CROSS_STUDENT_PII_LEAK_COUNT=
PUBLIC_STUDENT_ALIAS_OCCURRENCE_COUNT=
HTML_CRITICAL_A11Y_COUNT=
HTML_SERIOUS_A11Y_COUNT=
PDF_STRUCTURAL_FAILURE_COUNT=
PDF_VISUAL_DEFECT_COUNT=
MISSING_EXPECTED_DOCUMENT_COUNT=
BUILD_REPRODUCIBILITY_MISMATCH_COUNT=
SECRET_FINDING_COUNT=
CI_FAILURE_COUNT=
OPEN_REVIEW_BLOCKER_COUNT=
RESIDUAL_TECHNICAL_DEBT_COUNT=
```

Valeurs finales exigées :

```text
BROKEN_LINK_COUNT=0
ORPHAN_ACTIVE_FILE_COUNT=0
DUPLICATE_ACTIVE_FILE_COUNT=0
MATH_ERROR_REMAINING_COUNT=0
STUDENT_CORRECTION_LEAK_COUNT=0
CROSS_STUDENT_PII_LEAK_COUNT=0
PUBLIC_STUDENT_ALIAS_OCCURRENCE_COUNT=0
HTML_CRITICAL_A11Y_COUNT=0
HTML_SERIOUS_A11Y_COUNT=0
PDF_STRUCTURAL_FAILURE_COUNT=0
PDF_VISUAL_DEFECT_COUNT=0
MISSING_EXPECTED_DOCUMENT_COUNT=0
BUILD_REPRODUCIBILITY_MISMATCH_COUNT=0
SECRET_FINDING_COUNT=0
CI_FAILURE_COUNT=0
OPEN_REVIEW_BLOCKER_COUNT=0
RESIDUAL_TECHNICAL_DEBT_COUNT=0
```

Statut de succès exact :

```text
INES_ELYES_DOCUMENTATION_INTEGRATED_REBUILT_PUSHED_AND_VERIFIED
```

N’utilisez un statut bloqué que pour une impossibilité réelle et prouvée :

```text
BLOCKED_BY_SOURCE_CONFLICT
BLOCKED_BY_BUILD_OR_QA_FAILURE
BLOCKED_BY_GITHUB_PERMISSION
BLOCKED_BY_SECRET_EXPOSURE
```

Dans ce cas, conservez tous les changements sûrs, ne dégradez pas `main`, et fournissez la preuve technique exacte.

---

# 17. Règle de clôture

Vous n’avez pas terminé lorsque les fichiers sont simplement copiés.

Vous avez terminé uniquement lorsque :

- Ines et Elyes sont intégrés dans les diagnostics collectifs ;
- leurs parcours apparaissent dans les cinq fiches professeur de leur niveau ;
- leurs dossiers et remédiations sont cohérents avec les bilans ;
- le registre des élèves remplace le hardcoding ;
- les catalogues et manifests sont régénérés ;
- tous les PDF et packs sont produits ;
- chaque PDF modifié est inspecté ;
- les portails sont fonctionnels ;
- les scans public/privé sont verts ;
- le build est reproductible ;
- la CI est verte ;
- la PR est fusionnée ;
- `main` distant contient l’intégralité du dossier autorisé ;
- la dette résiduelle du lot est nulle ;
- le rapport final porte le statut demandé.
