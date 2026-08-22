# Provenance de la copie source

Ce document répond à une seule question, et il doit permettre d'y répondre des mois
plus tard, sans le corrigé sous les yeux :

> **quelle copie réelle a servi à cette correction ?**

Il traite de l'identité et de la provenance du document source, et de rien d'autre.
La lecture assistée — rendu des pages, transcription par modèle vision, revue humaine —
est décrite dans `docs/OCR_TRANSCRIPTION_PIPELINE.md`. Les deux couches sont distinctes
à dessein : la pièce probante existe et se vérifie indépendamment de toute lecture,
automatique ou humaine.

## Deux modes d'usage, et pourquoi la distinction compte

| | **mode humain** | **mode copie numérisée** |
|---|---|---|
| ce que l'enseignant regarde | la copie papier, posée à côté de lui | un PDF ou des photographies |
| pièce probante | physique, hors du système | numérique, dans le système |
| pièce jointe exigée | non | oui |
| absence de pièce jointe | normal, ce n'est pas un défaut | trou de provenance |
| clé de configuration | `NEXUS_S5_CORRECTION_MODE=human` (défaut) | `NEXUS_S5_CORRECTION_MODE=digital` |

Le mode humain est le mode historique, et il reste le mode par défaut. Une correction
faite en regardant une copie papier n'a pas besoin qu'on lui invente une pièce jointe :
la pièce existe, elle est simplement ailleurs. Les dossiers déjà corrigés continuent
donc de fonctionner à l'identique, et **aucune copie numérique n'est fabriquée
rétroactivement** pour eux.

Le mode copie numérisée est différent par nature. Si la correction s'appuie sur des
fichiers, alors ces fichiers *sont* l'observation. Ne pas les enregistrer reviendrait
à ne pas pouvoir démontrer ce qui a été lu — et une correction dont on ne peut plus
dire sur quoi elle portait n'est pas auditable. Dans ce mode, la saisie est donc
refusée tant qu'aucune pièce vérifiée n'est rattachée.

Le système ne connaît que deux états, et ne les devine jamais :

* `SOURCE COPY = ABSENT` — aucune ligne `source_copy` pour cette évaluation ;
* `SOURCE COPY = ATTACHED + VERIFIED` — une pièce rattachée dont chaque empreinte se
  recalcule à l'identique.

## Chaîne de provenance

```
COPIE RÉELLE ORIGINALE  (fichier fourni par l'utilisateur, jamais modifié)
   ↓ sha256 par fichier, recalculé après recopie
source_copy_file        (page_index, nom d'origine, type MIME, taille, empreinte)
   ↓
source_copy             (REAL_STUDENT_COPY, ORIGINAL|DERIVED, ATTACHED|SUPERSEDED)
   ↓ assessment_id
assessment  asm-<student_id>
   ↓ révision courante
correction  correction_id / revision
   ↓
réponses analytiques → diagnostic → bilans
```

La pièce est rattachée à l'**évaluation**, pas à une révision de correction. Rouvrir
une correction crée une révision ; cela ne crée pas une nouvelle copie papier. La
correction se retrouve depuis l'évaluation, par la même relation qui porte déjà les
items et les révisions.

## Ce qui est enregistré

`source_copy` : `assessment_id`, `source_kind` (`REAL_STUDENT_COPY`), `origin`
(`ORIGINAL` ou `DERIVED`), `derived_from_id`, `label`, `page_count`, `file_count`,
`status`, `is_immutable`, `note`, `ingested_at`.

`source_copy_file` : `page_index`, `original_name`, `media_type`, `byte_size`,
`sha256`, `stored_path` — un fichier par page photographiée, ou un seul fichier pour
un PDF multipage.

Formats acceptés : PDF, PNG, JPEG, TIFF, WEBP. Le type est lu **dans les octets de
tête**, pas dans l'extension : une photographie renommée `.pdf` est refusée.

## Immutabilité

Le fichier fourni est **recopié**, jamais déplacé ni réécrit. La copie stockée sous
`runtime/source_copies/` est passée en `0444`, et son empreinte est recalculée à
chaque affichage de l'écran de correction. Corriger, valider, analyser ou régénérer
un PDF ne touche aucun de ces octets.

Si une normalisation devient un jour nécessaire — redressement, conversion,
recompression — elle ne remplace pas l'original :

```
ORIGINAL   origin=ORIGINAL   sha256 A   ← ne bouge plus jamais
DERIVED    origin=DERIVED    sha256 B   → derived_from_id pointe vers l'original
```

Rien n'est effacé. Remplacer une pièce rattachée fait passer l'ancienne en
`SUPERSEDED` ; ses fichiers restent sur le disque et dans les sauvegardes.

## Contrôles au rattachement

* **fichier introuvable** → refusé ;
* **format non reconnu** → refusé, avec le message qui dit quoi faire ;
* **même fichier deux fois dans une même copie** → refusé : l'ordre des pages serait
  indéfendable ;
* **PDF et images mélangés**, ou plusieurs PDF → refusé, même raison ;
* **fichier déjà rattaché à une autre évaluation** → refusé, sauf
  `--autoriser-partage`, qui est une décision explicite et journalisée ;
* **copie déjà rattachée à cette évaluation** → refusé, sauf `--remplacer`.

L'**ordre des pages est celui qui a été fourni**. Il n'est jamais déduit d'un nom de
fichier, ni retrié.

Chaque rattachement produit un événement d'audit `source_copy.attached`, daté, portant
l'`assessment_id` et les empreintes.

## Sauvegarde et restauration

Les documents distribués ne sont pas recopiés dans les sauvegardes : ils sont
reproductibles et déjà identifiés dans `IMMUTABLE_STUDENT_ARTIFACTS.json`. Les copies
réelles, elles, **n'ont pas de seconde source** : leurs octets figurent dans l'archive,
et `BACKUP_MANIFEST.json` porte l'empreinte de chacune.

```bash
make s5-correction-backup          # sauvegarde, copies réelles incluses
make s5-correction-backup-verify   # restaure dans un temporaire, recontrôle les sha256
```

La vérification ne touche pas à `runtime/` : elle répond à « la sauvegarde rendrait-elle
exactement les mêmes octets ? ».

## Confidentialité

`runtime/` est exclu de Git — donc `runtime/source_copies/` aussi. Une copie d'élève
n'entre jamais dans le dépôt.

## Utilisation

Depuis l'interface : écran de correction → bloc **Copie de l'élève** →
**Téléverser la copie**. Les miniatures s'affichent, l'ordre se règle avant l'envoi,
et rien ne part tant que « Confirmer » n'est pas cliqué. Le détail du téléversement
et de la lecture assistée est dans `docs/OCR_TRANSCRIPTION_PIPELINE.md`.

En ligne de commande :

```bash
# rattacher un PDF multipage
make s5-correction-copie ELEVE=ines-kefi COPIE=/chemin/copie_ines.pdf

# rattacher des photographies, dans l'ordre des pages
make s5-correction-copie ELEVE=ines-kefi COPIE="/chemin/p1.jpg /chemin/p2.jpg /chemin/p3.jpg"

# état de la pièce rattachée, empreintes recontrôlées
make s5-correction-copie-etat ELEVE=ines-kefi

# corriger en mode copie numérisée
NEXUS_S5_CORRECTION_MODE=digital make s5-correction-run
```

Dans l'écran de correction, un bloc **Copie de l'élève**, distinct du sujet distribué,
du livret et du corrigé, affiche la pièce, sa pagination, l'état de son empreinte et un
lien de lecture seule par page. S'il n'y a rien : « Aucune copie élève rattachée ».

Le manifeste complet est lisible à `/eleve/<student_id>/copie/manifeste`.

## Ce que ce mécanisme ne fait pas

* il ne lit pas la copie ;
* il n'extrait aucune réponse ;
* il ne propose aucun score ;
* il ne remplace pas l'observation de l'enseignant.

Il garantit seulement que l'on saura toujours **sur quoi** la correction a porté.
