# Manuel d'exploitation

## Démarrer

```bash
make s5-correction-run
```

→ `http://127.0.0.1:8765`. Pour arrêter : `Ctrl` + `C`.

## Première installation

```bash
make s5-correction-install
make s5-correction-init
```

`init` crée la base, applique le schéma, contrôle les 60 empreintes, puis importe le
référentiel V3. Il refuse d'écraser une base existante sans `--force`, et prend une
sauvegarde avant de le faire.

## Contrôler l'intégrité

```bash
make s5-correction-qa          # intégrité + suite de tests
python3 tools/verify_integrity.py
python3 -m app.cli check
```

Le verdict attendu est `PASS`, avec `immutable_artifacts_changed = 0`.

## Sauvegarder

```bash
make s5-correction-backup
```

ou, dans l'interface, **Maintenance → Sauvegarder maintenant**. L'archive contient la
base, les rapports générés, les exports et un manifeste. Les documents distribués n'y sont
pas recopiés : ils sont identifiés par leurs empreintes.

Une sauvegarde est également prise automatiquement avant toute migration de schéma.

## Restaurer

1. Arrêter l'application.
2. Déplacer `runtime/corrections.sqlite3` (ne pas le supprimer).
3. Extraire `corrections.sqlite3` de l'archive choisie à sa place.
4. Redémarrer, puis vérifier l'écran **Maintenance**.

## Que faire si…

### « IMMUTABILITY FAILURE » au démarrage

Un document distribué ne correspond plus à son empreinte. L'application passe en lecture
seule ; c'est voulu.

1. Ne rien corriger tant que la cause n'est pas comprise.
2. `python3 tools/verify_integrity.py` liste les fichiers concernés.
3. Restaurer le document d'origine depuis la sauvegarde du dépôt ou depuis l'archive de
   livraison. Ne **pas** régénérer le PDF : il ne serait plus celui que l'élève a reçu.
4. Relancer. Le verdict doit revenir à `PASS`.

### « Le référentiel V3 a changé depuis l'import »

Un fichier source de `S5_post_distribution_v3/` a été modifié. Rien n'est resynchronisé
automatiquement : c'est une décision.

1. Regarder, dans **Maintenance**, quels fichiers ont changé et ce qui a changé.
2. Si le changement doit être pris en compte : sauvegarder, exporter les corrections en
   cours, puis `python3 tools/init_database.py --force`, et **ressaisir** les corrections
   à partir de l'export. Le référentiel ayant changé, une reprise automatique serait
   hasardeuse.
3. Si le changement est involontaire : restaurer le fichier V3.

### La compilation LaTeX échoue

Le message d'erreur et la fin du journal sont affichés ; le `.tex` est conservé dans
`runtime/build/`. Le rapport n'est pas marqué généré. Ouvrir le `.tex`, corriger ce qui
bloque — le plus souvent un caractère inhabituel dans un texte saisi — puis régénérer.

### Une correction a été validée trop tôt

**Réouvrir**, en indiquant la raison. Une révision est créée, l'ancienne est conservée avec
son statut, et l'historique garde la trace de la réouverture et de son motif.

### Un bilan approuvé doit être modifié

Régénérer : une nouvelle version est créée, la version approuvée reste intacte et son PDF
reste disponible. Les blocs que vous aviez modifiés sont reportés dans la nouvelle version.

### Une mauvaise copie a été téléversée

Ne supprimez rien. Téléversez la bonne en cochant **remplacer la pièce actuelle** :
l'ancienne passe `SUPERSEDED` et reste consultable. Toute campagne de lecture menée
sur elle devient automatiquement périmée, et l'invariant refuse d'exploiter une
transcription rattachée à une pièce qui n'est plus la pièce courante.

```bash
make s5-correction-fsck        # confirme qu'aucune pièce orpheline ne traîne
```

### Une page manque, ou le scan est de travers

Page manquante : la copie est incomplète, il faut la reprendre entièrement — un
téléversement partiel ne se complète pas, il se remplace.

Page de travers : bouton **⟳ 90°/180°/270°** sur l'écran de lecture assistée. La
rotation change réellement les pixels envoyés au modèle, produit une pièce dérivée
tracée, et la page est relue automatiquement (son empreinte a changé). L'original ne
bouge pas.

### La copie a été rattachée au mauvais élève

Rattachez la bonne pièce à l'élève concerné, et remplacez celle de l'élève erroné.
Le système refuse déjà un même fichier chez deux élèves sans `--autoriser-partage`.
Vérifiez ensuite le manifeste de chacun : `/eleve/<id>/copie/manifeste`.

### L'OCR a mal lu

C'est le cas prévu, pas un incident. Corrigez le bloc dans l'écran de revue : la
proposition du modèle est conservée, votre lecture s'ajoute, et l'historique garde
les deux. Si une zone entière a été omise par les deux lectures, c'est l'attestation
de complétude qui doit la faire remonter — ne l'attestez pas tant qu'il manque
quelque chose.

### Le fournisseur est indisponible

L'appel échoue explicitement ; il n'est jamais rerouté vers un fournisseur moins
protecteur. Diagnostic :

```bash
make s5-ocr-live-gate          # état par modèle, sur fixture synthétique
```

`MODEL_REJECTED_BY_POLICY` signifie qu'aucun endpoint conforme n'existe pour ce
modèle : changez de candidat, **jamais** la politique. En attendant, la correction
humaine reste entièrement disponible : le mode papier n'a jamais eu besoin d'IA.

### Une correction validée est fautive

Passez par **Rouvrir** — une raison écrite est obligatoire, une révision est créée,
et le bilan précédent devient périmé. Jamais d'édition directe de la base.

### Il faut restaurer

Voir « Restaurer » ci-dessus. Après restauration, contrôlez systématiquement :

```bash
make s5-correction-fsck
```

et vérifiez pour l'élève concerné : empreinte de la source, état de transcription,
statut de correction, rapports présents.

## Exports

| action | résultat |
| --- | --- |
| **Exporter cet élève** | `runtime/exports/export_<élève>.json` — cet élève uniquement |
| **Exporter toutes les corrections** | `runtime/exports/export_corrections_<date>.json` |
| **Exporter la clôture du stage** | `runtime/exports/stage_cloture_<date>/` avec les quatre dossiers de documents, les analyses JSON et `MANIFEST_SHA256.json` |

## Vérifier avant un push Git

```bash
python3 tools/check_runtime_not_tracked.py
```

Il échoue si une base, un bilan ou un export réel est suivi par Git.

## Déploiement aux autres élèves (rollout)

Réussir sur une copie ne démontre pas que le système sait lire toutes les écritures.
Le déploiement se fait donc par lots, avec un point d'arrêt après chacun.

**Prérequis** — la copie pilote a franchi toute la chaîne : transcription vérifiée
page par page, complétude attestée, correction validée, bilans relus.

**Taille de lot** — 3 élèves. Assez pour voir un défaut se répéter, assez peu pour
que la relecture humaine reste possible dans la journée.

**Après chaque lot, sans exception :**

```bash
make s5-correction-fsck        # cohérence base / fichiers
make s5-full-gate              # le système doit rester vert avec des données réelles
make s5-correction-backup && make s5-correction-backup-verify
```

et, pour chaque élève du lot : divergences entre les deux lectures, nombre de
corrections humaines nécessaires, zones illisibles, QA visuelle des PDF.

**Surveillance** — ce qui doit faire lever la tête d'un lot à l'autre : le nombre de
corrections humaines par page qui augmente, des omissions qui se répètent au même
endroit d'une copie à l'autre, un désaccord systématique sur un type de signe, un
coût par page qui dérive.

**Arrêt immédiat** en cas de défaut systémique : ne pas terminer le lot, conserver
les preuves, corriger le moteur sur une branche dédiée, écrire le test de régression
à partir d'une **fixture synthétique** reproduisant la structure du défaut — jamais
avec l'écriture ni les réponses nominatives d'un élève —, repasser les portes, puis
reprendre.

**Retour en arrière** — aucune donnée n'est jamais écrasée : les pièces remplacées
restent `SUPERSEDED`, les corrections rouvertes créent une révision, les bilans
antérieurs sont conservés. Un retour en arrière consiste donc à rouvrir et
revalider, jamais à effacer. En dernier recours, la sauvegarde antérieure au lot est
restaurable et vérifiable.

**Ce qui reste obligatoire quel que soit le lot** : la revue humaine et l'attestation
de complétude. Elles ne s'automatisent pas parce que le lot précédent s'est bien
passé.
