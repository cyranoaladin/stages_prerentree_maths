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
