# Exploitation — aujourd'hui

Ce document tient sur une page et sert pendant la correction. Le détail des règles
est ailleurs ; ici, on fait.

## La séquence, dans l'ordre

```bash
# 1. portes logicielles — reproductibles, hors réseau, sans coût
make s5-full-gate

# 2. porte live OpenRouter — fixture synthétique uniquement, clé requise, coût réel
make s5-ocr-live-gate

# 3. sauvegarde de l'état propre
make s5-correction-backup
make s5-correction-backup-verify

# 4. lancement
S5_DATA_MODE=REAL NEXUS_S5_PASSWORD='…' \
  NEXUS_S5_CORRECTION_MODE=digital make s5-correction-run   # http://127.0.0.1:8765
```

Puis, dans le navigateur :

| étape | où |
|---|---|
| **téléverser** la copie — PDF multipage ou lot d'images | écran de correction, bloc *Copie de l'élève* |
| **lire** — PRIMARY, puis AVEUGLE | écran *Lecture assistée* |
| **réviser** bloc par bloc, et **attester la complétude** de chaque page | même écran |
| **corriger** — et seulement là | écran de correction |

Le téléversement web est la voie normale. Le CLI (`make s5-correction-copie`) reste
disponible pour l'administration et les lots.

`S5_DATA_MODE=REAL` exige un mot de passe d'au moins 12 caractères : des copies
d'élèves ne s'ouvrent pas sans authentification, même sur la boucle locale. Pour
travailler sur des fixtures, déclarez `S5_DATA_MODE=SYNTHETIC`.

Le tableau de bord affiche deux colonnes distinctes, à ne pas confondre :

* **Correction** — où en est la saisie : non commencée, en cours, validée ;
* **Bilan longitudinal** — ce que les sources permettent d'écrire, indépendamment
  de la saisie. Un élève peut être « non commencé » et son bilan « prêt ».

## Si la correction se fait sur une copie numérisée

Regarder une copie papier et saisir : rien ne change, c'est le mode par défaut.

S'appuyer sur un scan exige de rattacher la pièce avant de corriger — sinon rien ne
dira plus tard ce qui a été observé. La voie normale est le **téléversement web** :
bloc *Copie de l'élève*, miniatures, ordre réglé avant l'envoi, et rien ne part tant
que « Confirmer » n'est pas cliqué.

Voie d'administration, pour les lots :

```bash
make s5-correction-copie ELEVE=<id> COPIE=/chemin/copie.pdf
make s5-correction-copie-etat ELEVE=<id>          # empreintes recontrôlées
```

Dans ce mode, la saisie est refusée tant qu'aucune pièce vérifiée n'est rattachée.
Le détail est dans `docs/SOURCE_COPY_PROVENANCE.md`.

## Lecture assistée d'une copie scannée

Elle propose une transcription ; elle ne corrige rien et ne note rien.

```bash
make s5-ocr-modeles                     # catalogue OpenRouter du jour
export OPENROUTER_API_KEY=...           # jamais dans Git, jamais en base
make s5-ocr-smoke                       # contrôle sur fixture synthétique
```

Puis, sur l'écran **Lecture assistée** de l'élève : « Lecture PRIMARY », « Lecture
VERIFY », et revue bloc par bloc. Seule une transcription vérifiée par un humain fait
foi ; les blocs en désaccord entre les deux lectures sont signalés en rouge et
attendent une décision.

Chaque appel impose ZDR et `data_collection=deny`. Si aucun endpoint conforme
n'existe, l'appel échoue — il n'est jamais rerouté. Le détail est dans
`docs/OCR_TRANSCRIPTION_PIPELINE.md`.

## Corriger un élève

1. cliquer **Corriger** sur la ligne de l'élève ;
2. le sujet distribué s'affiche à gauche et y reste ; la grille est à droite ;
3. saisir chaque critère : un score, éventuellement des codes d'erreur, une
   observation. Les raccourcis clavier sont neutralisés dans les zones de saisie ;
4. renseigner les **observations générales** en bas de page ;
5. cliquer **Valider la correction**. Si des lignes manquent, la page le dit et
   n'enregistre rien.

Le compteur en haut distingue les **critères du sujet** des **lignes analytiques** :
un critère mixte éclaté compte pour une question sur le papier et deux lignes à
renseigner.

## Générer son bilan

1. **Analyse** — vérifier la cohérence des statuts et du profil d'erreurs ;
2. **Bilan longitudinal** — l'écran s'ouvre sur les sources : diagnostic initial,
   cinq séances, réserves documentaires ;
3. parcourir la matrice **Analyse croisée** : départ, séances, travail, évaluation,
   niveau de preuve, trajectoire ;
4. lire le **brouillon parents** ;
5. corriger ce qui doit l'être — une section réécrite et approuvée n'est jamais
   réécrasée par une régénération ;
6. générer les PDF.

Un texte qui contiendrait un identifiant technique, une progression chiffrée ou le
mot « lacune » est refusé **avant** compilation : aucun PDF fautif n'est produit.

## Modifier une correction déjà validée

1. **Rouvrir** — une raison écrite est obligatoire ;
2. modifier les critères concernés ;
3. **revalider** ;
4. le bilan produit auparavant devient **périmé** : l'écran l'affiche en rouge ;
5. régénérer les documents.

L'ancien bilan n'est pas effacé ; il cesse d'être le bilan courant.

## Où sont les documents

| quoi | où |
| --- | --- |
| base de correction | `S5_correction_app/runtime/corrections.sqlite3` |
| sauvegardes | `S5_correction_app/runtime/backups/` |
| bilans produits | `S5_correction_app/runtime/reports/` |
| manifestes de préparation | `S5_correction_app/runtime/readiness/<élève>/` |
| sujets distribués | `S5_cloture/<niveau>/<matière>/<Élève>/` — **jamais modifiés** |

Tout ce qui est sous `runtime/` est hors de Git : aucune correction réelle, aucun
bilan d'élève ne part au dépôt.

## Ce qu'il ne faut pas faire

**Ne pas lancer `init_database.py --force`** une fois la première correction saisie.
La commande refuse d'elle-même et affiche la liste de ce qui serait perdu ; c'est
une protection, pas un obstacle à contourner. Pour faire évoluer le schéma, les
migrations s'appliquent au démarrage sans rien détruire.

## Contrôles rapides

```bash
python3 tools/check_today_readiness.py --no-compile   # toutes les portes, ~1 min
python3 tools/build_readiness.py                      # état des sources des 15
python3 tools/verify_integrity.py                     # immutabilité + référentiel
make s5-correction-test                               # suite de tests
```

## En cas de doute

Si l'application passe en lecture seule, c'est qu'un document distribué ne
correspond plus à son empreinte. Ne pas forcer : le message nomme le fichier. Un
sujet modifié après distribution invaliderait toutes les corrections qui s'y
appuient.
