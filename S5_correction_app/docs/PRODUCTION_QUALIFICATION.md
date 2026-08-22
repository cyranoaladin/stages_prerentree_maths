# Qualification de production — S5 Correction & Bilans

Rapport de clôture de la mission autonome finale.
Portée : ce que le logiciel a démontré, et ce qu'il n'a pas pu démontrer.

État Git au moment du rapport : `f77f534` (fusion de la PR #11), branche `main`.

---

## A. Verdict

| Verdict | Valeur |
|---|---|
| `S5_SOFTWARE_READY` | **YES** |
| `S5_PRODUCTION_READY` | **NO** |
| `BLOCKER` | `REAL_COPY_SOURCE_MISSING` |
| `HANDWRITING_REAL_ACCURACY_GATE` | `NOT_RUN` |
| `PILOT_SOFTWARE_READY` | `YES` |
| `GENERAL_HTR_PRODUCTION_QUALIFICATION` | `INSUFFICIENT_REAL_SAMPLE` |

Le logiciel est prêt à recevoir une vraie copie. Il n'en a jamais reçu une seule.
Ces deux phrases doivent rester ensemble : la première sans la seconde serait un faux
`PRODUCTION_READY`.

## B. Ce qui est démontré

| Porte | Résultat | Preuve |
|---|---|---|
| `S5_FULL_GATE` | PASS | 8 étapes, **491 tests, 0 ignoré**, 129 s |
| `NO_KNOWN_TECH_DEBT` | PASS **calculé** | 51 défauts, 0 ouvert, 0 limitation bloquante |
| `TODAY_READINESS` | PASS | immutabilité 60/60, 15 élèves, 15 évaluations |
| Réconciliation base ↔ fichiers | PASS | `tools/fsck.py` |
| Sauvegarde / restauration | `RESTORE VERIFIED` | archive du 2026-08-22 16:11:59 |
| Connectivité live | PASS | `runtime/live_gate_status.json` |
| Routage confidentiel live | PASS | `data_collection=deny`, ZDR, sans repli |
| Confidentialité Git | PASS | 0 fichier de runtime suivi, 4631 fichiers contrôlés |

## C. Ce qui n'est pas démontré, et ne peut pas l'être ici

| Élément | État | Pourquoi |
|---|---|---|
| Exactitude de lecture manuscrite | `NOT_RUN` | aucune copie manuscrite réelle n'existe dans le système |
| Transcription humaine de référence (GOLD) | absente | elle ne peut être produite que par un humain lisant la copie |
| Qualification générale multi-écritures | `INSUFFICIENT_REAL_SAMPLE` | 0 copie réelle sur 15 élèves |
| Politique de confidentialité du compte | jamais `VERIFIED` | non exposée par l'API ; relève du tableau de bord |
| Résidence des données | non garantie | ZDR ≠ localisation ; voir `PRIVACY_SECURITY.md` |
| Coûts et latences sur page manuscrite | inconnus | une fixture typographique ne les préjuge pas |

## D. Répétition de bout en bout

Chaîne canonique jouée intégralement, sur une copie **synthétique**, dans un runtime
isolé : téléversement → empreintes → rasterisation → lecture PRIMARY → lecture BLIND
→ réconciliation locale → revue humaine → attestation de complétude. 7 étapes sur 7.

Également vérifiés : redémarrage à froid, cohérence sauvegarde/restauration sur un
système peuplé (3 copies, 3/3 empreintes conformes), mode dégradé sans clé, 12 types
d'événements d'audit.

Ce que cette répétition ne prouve pas : qu'un modèle sait lire une écriture d'élève.

## E. État de la copie d'Inès KEFI

Contrôle automatique du 2026-08-22 :

```
copies sources 0 · campagnes OCR 0 · blocs transcrits 0 · bilans 0
correction     1 — DRAFT, révision 1, 23 réponses PENDING
                   0 score, 0 observation, 0 code d'erreur
                   12 lignes d'observation d'item, toutes vides
```

Cette correction est une **coquille vide** créée le 2026-08-22 à 02:34:26 par la
simple ouverture de l'écran de correction pendant le diagnostic d'un défaut. Elle ne
contient aucune donnée d'élève. Aucune réponse d'Inès n'a été saisie, inférée ou
fabriquée.

Tous les fichiers portant son nom sur le poste sont soit des livrables générés, soit
le sujet distribué — empreintes vérifiées. Aucune copie rendue.

## F. Le blocage, et l'action humaine unique

`REAL_COPY_SOURCE = MISSING`.

**Une seule action humaine débloque la suite** : téléverser, depuis l'interface S5,
le PDF multipage ou les images de la vraie copie rendue par Inès.

Ensuite seulement viennent les deux autres décisions qui ne m'appartiennent pas :
valider humainement la transcription de référence, puis décider de la publication.

## G. Ce qu'il ne faut pas conclure

Ne pas conclure d'un `S5_FULL_GATE = PASS` que le système lit bien les copies : la
porte mesure le logiciel, pas la lecture. Ne pas conclure d'une répétition synthétique
réussie qu'une vraie copie passera. Ne pas conclure d'un succès sur la copie d'Inès
que les quatorze autres écritures seront lues correctement — d'où le déploiement par
lots décrit dans `OPERATIONS_RUNBOOK.md`.
