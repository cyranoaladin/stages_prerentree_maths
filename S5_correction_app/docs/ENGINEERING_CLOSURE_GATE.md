# Audit de fermeture — dette connue, limites assumées, portes

Ce document existe pour qu'aucune limite ne soit découverte par surprise. Ce qui n'est
pas démontré y est écrit comme non démontré.

## 1. Dette technique — inventaire

### Résolue pendant cet audit

| id | gravité | défaut | correctif | preuve |
|---|---|---|---|---|
| D-01 | P0 | `--allow-network` exigeait `NEXUS_S5_PASSWORD` mais **rien ne le vérifiait** : exposée au réseau, l'application servait copies, transcriptions et bilans sans authentification. Le test existant ne contrôlait que le refus de démarrage. | authentification HTTP Basic à comparaison en temps constant, sur **toutes** les requêtes dès que `allow_network` est actif | `test_exposee_au_reseau_l_application_exige_une_authentification` |
| D-02 | P0 | aucune protection CSRF : un formulaire tiers pouvait poster du `multipart/form-data` sur la route de téléversement, sans requête préalable | contrôle d'origine (`Origin`/`Referer`) ou en-tête client sur toute méthode mutante | `test_une_requete_mutante_d_origine_etrangere_est_refusee` + test positif |
| D-03 | P0 | `provider.zdr` ne désactive pas le *response caching* d'OpenRouter, qu'un préréglage de compte peut activer | `X-OpenRouter-Cache: false` sur chaque appel, posé après le corps donc non écrasable | `test_l_entete_anti_cache_part_avec_chaque_appel` + test négatif |
| D-04 | P0 | `OPENROUTER_BASE_URL` librement configurable : un mauvais endpoint exfiltrait les copies | HTTPS + hôte en liste blanche ; endpoint personnalisé derrière `NEXUS_S5_ALLOW_CUSTOM_ENDPOINT=1` | 4 tests dont trois négatifs |
| D-05 | P1 | pièces stockées en `0444` — lecture seule **mais lisible par tous** sur un poste partagé | `0400` pour les pièces, `0600` pour cache et archives, `0700` pour les répertoires | `test_les_copies_ne_sont_pas_lisibles_par_tous` |
| D-06 | P1 | copies et transcriptions servies sans `Cache-Control` : un navigateur ou un mandataire pouvait les conserver | `no-store`, `Referrer-Policy: no-referrer`, `nosniff`, `SAMEORIGIN` | `test_les_copies_ne_sont_jamais_mises_en_cache_par_le_navigateur` |
| D-07 | P1 | `redact()` ne masquait que la clé : une exception pouvait charrier l'image base64 ou la copie | masquage des `data:` URL, des blocs base64 longs, et troncature | `test_une_exception_ne_reproduit_ni_la_cle_ni_l_image` |
| D-08 | P1 | seconde lecture **non aveugle** : le modèle voyait la transcription candidate, donc biais de confirmation, et le résultat s'appelait « consensus » | lecture `BLIND` sur la même image sans voir la première, réconciliation locale, statut renommé `AI_TWO_BLIND_READINGS_IDENTICAL` | 5 tests |
| D-09 | P1 | **angle mort de l'omission** : une revue par blocs ne peut pas révéler une zone omise par les deux lectures | attestation humaine de complétude par page, liée au `page_sha256`, exigée par l'invariant ; zones `UNMATCHED` remontées | 3 tests |
| D-10 | P1 | pas d'historique des révisions humaines : une deuxième correction écrasait la première | table `transcription_block_history` append-only (avant/après/quand/qui/action/motif) | `test_deux_corrections_humaines_successives_sont_toutes_conservees` |
| D-11 | P1 | clé de cache fondée sur des **noms** de version : un prompt modifié sans changement de nom réutilisait le cache | empreintes `prompt_sha256` et `schema_sha256` dans la clé et dans la campagne | `test_un_prompt_modifie_invalide_le_cache_sans_changer_de_version` |
| D-12 | P1 | configuration lue à chaque page : une variable changée en cours de route produisait une campagne hétérogène | configuration figée au démarrage dans `ocr_run.frozen_config_json` | `test_la_configuration_de_campagne_est_figee` |
| D-13 | P1 | deux campagnes simultanées possibles (double clic) : double facturation, états concurrents | index **unique partiel** en base sur les campagnes `RUNNING` | `test_deux_campagnes_simultanees_du_meme_role_sont_impossibles` |
| D-14 | P1 | une campagne `RUNNING` après un arrêt du processus restait « en cours » indéfiniment | `resume_interrupted()` au démarrage → `INTERRUPTED`, reprenable, pages en cache non refacturées | `test_une_campagne_restee_en_cours_est_reprise_au_demarrage` |
| D-15 | P1 | copie remplacée pendant une campagne : rien ne signalait que la campagne ne portait plus sur la pièce courante | `is_stale()` + empêchement dans l'invariant | `test_une_campagne_devient_perimee_si_la_copie_est_remplacee` |
| D-16 | P1 | aucune borne de sortie : un modèle défaillant pouvait remplir la base | plafonds réponse HTTP, blocs/page, verbatim, latex, notes, alternatives | 5 tests |
| D-17 | P1 | garde d'exploitation posée sur une route : un autre chemin appelait le moteur directement | invariant unique `transcription_is_usable()`, contrôlé par test structurel | `test_toutes_les_voies_passent_par_l_invariant_unique` |
| D-18 | P1 | envoi d'une copie réelle possible sans décision explicite, alors que la journalisation côté compte n'est pas contrôlable | `ALLOW_REAL_STUDENT_REMOTE_OCR=0` par défaut ; fixtures synthétiques exemptées | 2 tests |
| D-19 | P2 | assertion `assert ... == 0 or True` dans `test_ines_micropass.py` : **ne pouvait jamais échouer** | assertion réelle sur le contenu du champ de saisie | le test passe, et échoue si l'échappement est retiré |
| D-20 | P2 | écrasement silencieux possible d'une pièce stockée en cas de réutilisation d'identifiant | refus explicite, renvoi vers `fsck` | `test_l_ecran_...` / chemin couvert par la suite |
| D-21 | P2 | 48 imports inutilisés, 5 variables mortes | supprimés après examen ; `ruff --select F,E9` passe | `make s5-full-gate` étape 1 |
| D-22 | P2 | aucune réconciliation base ↔ système de fichiers | `tools/fsck.py`, lecture seule, 15 contrôles | `make s5-correction-fsck` |
| D-23 | P1 | **TIFF multipage** : accepté à l'ingestion, mais le rendu n'en prenait que la première image — une page de copie aurait disparu sans trace. Vérifié expérimentalement (2 frames → 1 page rendue). | refus explicite au téléversement, avec la marche à suivre | `test_un_tiff_multipage_est_refuse_explicitement` + test positif sur TIFF d'une page |
| D-24 | P2 | doublon de page rejeté d'office, alors que deux pages blanches identiques sont légitimes | avertissement « DOUBLON DÉTECTÉ » puis confirmation explicite `--autoriser-doublons` ; la provenance reproduit ce qui a été fourni | `test_un_doublon_avertit_et_demande_confirmation` |

### Dette connue **non résolue**, assumée et documentée

| id | gravité | limite | pourquoi elle reste | ce qu'il faudrait |
|---|---|---|---|---|
| R-01 | — | **aucune mesure de qualité HTR** | il n'existe aucune copie manuscrite réelle ni transcription humaine de référence | la copie d'Inès, puis le protocole du §16 |
| R-02 | — | **connectivité OpenRouter non éprouvée** | `OPENROUTER_API_KEY` absente de cet environnement | `make s5-ocr-live-gate` |
| R-03 | P2 | pas de test navigateur réel (glisser-déposer, réordonnancement, miniatures, zoom, KaTeX) | Playwright n'est pas installé ; l'installer pour ce seul gate serait disproportionné | QA manuelle documentée, ou installation de Playwright |
| R-06 | P2 | **rotation** : l'interface tourne l'affichage, pas l'image envoyée au modèle | une page scannée à 90° part telle quelle | dérivation `DERIVED_ROTATED_PAGE`, avec provenance |
| R-07 | P2 | **contenu non textuel** : `origin=DIAGRAM_ANNOTATION` existe, mais il n'y a ni `NON_TEXT_EVIDENCE`, ni `CODE` | inutile pour le pilote mathématiques ; nécessaire pour NSI | extension du schéma, sans migration cassante |
| R-08 | P2 | **continuation entre pages** : colonnes `continues_from` / `continues_to` créées, aucune interface | non nécessaire pour trancher le pilote | exposition dans l'écran de revue |
| R-09 | P3 | pas de mesure de performance sur 60 pages | aucune copie de cette taille disponible | simulation hors ligne avant une copie longue |
| R-10 | P3 | limites de CPU et de mémoire non posées sur `pdftoppm` | `timeout`, `shell=False`, environnement minimal et répertoire privé sont en place ; `setrlimit` ne l'est pas | `resource.setrlimit` dans un préexécuteur |
| R-11 | — | **application mono-utilisateur sans authentification en local** | c'est le mode d'usage prévu | `actor()` retourne `authenticated: False` et l'audit le dit |

## 2. Limites assumées, à ne pas confondre avec des garanties

* **`AI_TWO_BLIND_READINGS_IDENTICAL` ≠ correct.** Deux modèles peuvent se tromper de
  la même manière.
* **Tous les blocs acceptés ≠ rien d'omis.** D'où l'attestation de complétude.
* **Empreinte correcte ≠ confidentialité.** Le hachage prouve l'intégrité, rien d'autre.
* **ZDR ≠ résidence des données, ≠ conformité juridique, ≠ absence de cache, ≠ absence
  de journalisation côté compte.**
* **Aucune donnée personnelle dans le JSON ≠ aucune donnée personnelle envoyée.**
  L'image *est* la copie, et porte le nom de l'élève.
* **300 dpi = valeur d'ingénierie par défaut**, pas optimum démontré.
* **Les archives ne sont pas chiffrées** ; elles sont seulement privées (`0600`).
* **Le plafond de coût applicatif ne remplace pas un plafond fournisseur**, et une
  reprise après expiration du délai côté client peut être facturée deux fois.
* **Identité du relecteur déclarée, non authentifiée** en usage local.

## 3. Portes, et leur état réel

| porte | état | fondé sur |
|---|---|---|
| `ENGINEERING_CLOSURE_GATE` | PASS | `make s5-full-gate` |
| `SOURCE_COPY_SECURITY_GATE` | PASS | droits, ingestion atomique, octets, CSRF, en-têtes |
| `OCR_OFFLINE_GATE` | PASS | 110 tests hors ligne, client simulé |
| `HUMAN_REVIEW_INVARIANTS_GATE` | PASS | invariant unique, attestation, historique append-only |
| `BACKUP_CONSISTENCY_GATE` | PASS | archive + restauration vérifiée + sentinelle de secret |
| `MIGRATION_GATE` | PASS | v4→v7 sur copie puis sur base réelle, `fsck` PASS |
| `NO_KNOWN_TECH_DEBT` | PASS | 22 défauts corrigés, 11 limites documentées ci-dessus |
| `OPENROUTER_IMPLEMENTATION_GATE` | PASS | contraintes, en-tête, endpoint, bornes, reprises — tous testés |
| `OPENROUTER_LIVE_CONNECTIVITY_GATE` | **NOT_RUN** | aucune clé dans cet environnement |
| `OPENROUTER_PRIVACY_ROUTING_GATE` | **NOT_RUN** | exige un appel réel : rien ne prouve encore qu'un endpoint ZDR existe pour les modèles retenus |
| `HANDWRITING_REAL_ACCURACY_GATE` | **NOT_RUN** | aucune copie manuscrite réelle |

`OPENROUTER_VISION_PIPELINE` **n'est pas déclaré PASS** : il exige les deux portes
live. La formulation employée dans un rapport antérieur était trop forte.

## 4. Ce qu'il reste à faire, dans l'ordre

1. `OPENROUTER_API_KEY=… make s5-ocr-live-gate` — fixture synthétique uniquement.
   Si un modèle n'a aucun endpoint conforme : **changer de candidat**, jamais
   assouplir la politique.
2. Décider R-04 (TIFF multipage) et R-05 (doublons) avant d'ingérer une copie réelle
   dont on ne connaît pas le format.
3. Ingérer la copie d'Inès, la rendre, lire PRIMARY, lire BLIND, réviser, attester,
   constituer la transcription humaine de référence, mesurer.
4. Seulement ensuite : `HANDWRITING_TRANSCRIPTION_GATE`.
5. La correction elle-même vient après, dans une mission distincte.
