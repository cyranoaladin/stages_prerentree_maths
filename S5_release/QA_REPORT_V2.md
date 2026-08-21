# QA_REPORT_V2 — livraison S5 après passe corrective

**Date :** 2026-08-21. **Objet :** réponse point par point à l'audit indépendant du 21 août 2026.

## Verdict global

**PASS WITH WARNINGS — la livraison sort de HOLD.**

Les six gates de sortie sont franchies. Les avertissements résiduels sont documentaires et ne peuvent pas être levés par la production : ils tiennent à des sources qui n'existent pas, non à des défauts de fabrication.

| Gate | Verdict | Ce qui a été fait |
|---|:--:|---|
| A — scientifique | **PASS** | 100 items contre-résolus, 4 FAIL et 8 WARN traités, phases 4 reformulées |
| B — temps | **PASS** | écrasement supprimé, deux estimateurs indépendants, NSI ramenée de 54,5 et 55 min à 38,7 et 40,5 min |
| C — mesure de progression | **PASS** | aucun écart chiffré produit, statuts explicites, scoring par critère, contexte de rétention |
| D — données | **PASS** | schéma v2 conforme à la sortie réelle, validé par jsonschema, force de preuve rigoureuse |
| E — programmes | **PASS** | référence BO/NOR et année d'effet dans les 5 blueprints ; cycle 4 non anticipé |
| F — sécurité et paquetage | **PASS** | exécution refusée par défaut, conteneur en option, caches retirés, paquets séparés, manifestes de traçabilité et de distribution |

## Verdict par axe

| Axe | Verdict |
|---|:--:|
| technique | **PASS** |
| scientifique | **PASS** |
| pedagogique et docimologique | **PASS** |
| donnees | **PASS** |
| securite et paquetage | **PASS** |

### Technique — PASS

- 45 documents LaTeX compilés, 0 échec
- 0 `Undefined control sequence`, 0 référence cassée, 0 `Overfull \hbox`, 0 avertissement `headheight`
- 364 pages rasterisées et analysées une par une, 0 défaut bloquant
- marges d'encre : en-tête ramené de 0,5 mm à environ 10 mm du bord, pied à 8 mm, côtés à 15 mm — la géométrie précédente était inimprimable en tête de page
- 7611 contrôles de validation, 0 échec critique
- 0 cache Python dans la livraison

### Scientifique — PASS

- 100 items uniques contre-résolus : 100 PASS, 0 WARN, 0 FAIL
- 93 items re-résolus par un calcul exécutable, 7 par une revue documentée
- les 4 FAIL et les 8 WARN de la revue du 21 août sont traités un par un (voir SCIENTIFIC_AUDIT.md)
- les 5 phases 4 sont reformulées : ce qui est nouveau y est annoncé comme nouveau
- convention du milieu fixée pour la dichotomie

### Pedagogique et docimologique — PASS

- durée : deux estimateurs indépendants, l'un fondé sur le contenu, l'autre sur le barème ; durée prudente 38.66 à 41.81 min, marge 3.19 à 6.34 min sur 45
- aucune durée n'est imposée : la table `ITEM_MINUTES` a été supprimée
- barème : 20 points pour les 15 sujets, noyau commun 70 %, individualisé 30 %
- aucune reprise à l'identique d'un exercice antérieur sur 405 énoncés
- proximité maximale entre deux livrets d'un même niveau : 0.484
- un code d'erreur ne peut plus sanctionner une exigence non formulée ; les méthodes valides mais moins directes reçoivent la totalité des points

### Donnees — PASS

- schéma canonique v2, et la sortie réelle de `analyze_s5.py` est validée par `jsonschema` dans les tests
- scoring par critère : 337 critères, chacun portant une compétence unique et un type de preuve
- `mastery_delta` vaut null pour toutes les compétences, et le schéma refuse toute autre valeur
- `measurement_reliability` remplacé par `evidence_strength`, calculé sur cinq critères explicites
- contexte de remédiation immédiate et statut de rétention portés par chaque compétence
- 48 tests, 48 réussis, 0 échoués

### Securite et paquetage — PASS

- l'exécution du code élève est refusée par défaut : le script sort en erreur tant qu'aucun mode n'est choisi (code de sortie 3)
- deux modes seulement : `--mode relu`, explicitement annoncé comme NON SANDBOXÉ, et `--mode conteneur`, jetable, sans réseau, en lecture seule, utilisateur non privilégié, limites CPU/mémoire/processus
- paquet d'exploitation et paquet d'audit séparés (211 et 332 fichiers)
- 210 sources S1-S4 empreintées en SHA-256 dans `source_evidence_manifest.json`
- `CANONICAL_DELIVERY.json` désigne le document exact à distribuer et les 4 documents qu'il remplace

## Ce qui a changé, point par point

| Point de l'audit | État avant | État après |
|---|---|---|
| Audit de durée circulaire | `core.exam_items()` écrasait la durée de chaque item par `common.ITEM_MINUTES` pour garantir 41 min | la table est supprimée ; `data/timing.py` estime chaque item depuis son contenu, et `audit_docimologie.py` recalcule une seconde durée depuis le seul barème, sans entrée commune |
| Évaluations NSI surchargées | 54,5 et 55 min | 38,7 et 40,5 min de durée prudente, après retrait réel de sous-questions (B2, B3, C1) |
| Delta de progression non défendable | statut qualitatif converti en score 0-4 puis soustrait | `mastery_delta` vaut null partout, le schéma l'impose, un test le vérifie, et le bilan parents explique pourquoi aucune progression chiffrée n'est écrite |
| Agrégation par compétence | points de l'item divisés à parts égales entre ses compétences | barème au niveau du critère : 337 critères, chacun portant une compétence unique, un type de preuve et une sous-partie ; la saisie se fait critère par critère |
| Schéma JSON incompatible | le schéma exigeait `comparability`, l'analyseur produisait `comparison_status` | schéma canonique v2 aligné sur la sortie réelle, validé par `jsonschema` dans les tests, et refusant tout `mastery_delta` chiffré |
| `measurement_reliability` impropre | seuil binaire à 2 points | `evidence_strength`, calculée sur cinq critères déclarés : nombre de critères, d'items, de points, présence d'une tâche de transfert, proximité d'une remédiation |
| Effet de récence ignoré | rien | chaque compétence porte `post_test_context`, `retention_status` et `recommended_delayed_check` ; un mini-test différé en semaine 2 est inscrit dans le plan de rentrée ; le bilan dit « réussite immédiate à confirmer » |
| Défauts scientifiques | 4 FAIL, 8 WARN | tous traités et re-vérifiés ; 100 items contre-résolus, 100 PASS |
| Références réglementaires | absentes | `curriculum_reference` dans les 5 blueprints, avec BO, NOR et année d'effet, et interdiction explicite d'anticiper la nouvelle progression de cycle 4 en 4e et 3e |
| Runner NSI non sandboxé | exécution automatique | exécution refusée par défaut ; `--mode relu` avertit qu'il n'y a aucune isolation ; `--mode conteneur` isole réellement |
| Caches Python livrés | 17 `.pyc` | 0 ; les scripts désactivent l'écriture de bytecode et le validateur refuse la livraison si un cache réapparaît |
| Paquet non autoportant | une seule archive | `S5_release/` et `S5_audit/` séparés, plus `source_evidence_manifest.json` (210 sources empreintées) et `CANONICAL_DELIVERY.json` |
| Décompte de fichiers inexact | 316 annoncés, 333 réels | décompte ci-dessous, complet et arithmétiquement vérifiable |

## Décompte des fichiers

| Extension | S5_release | S5_audit |
|---|:--:|:--:|
| `.pdf` | 45 | 45 |
| `.json` | 113 | 134 |
| `.tex` | 0 | 45 |
| `.md` | 21 | 26 |
| `.py` | 31 | 36 |
| `.log` | 0 | 45 |
| `.sty` | 1 | 1 |
| `.sh` | 1 | 1 |
| `.pyc` | 0 | 0 |
| **total** | **212** | **333** |

Somme des extensions listées : release 212, audit 333. Le complément correspond aux fichiers sans extension listée.

## Durées recalculées, sans table imposée

| Élève | Estimateur contenu | Estimateur barème | Écart | Durée prudente | Marge sur 45 |
|---|:--:|:--:|:--:|:--:|:--:|
| Fares DARGHOUTH | 40.75 min | 40.62 min | -0.3 % | **40.75 min** | 4.25 min |
| Ines KEFI | 38.75 min | 40.14 min | +3.6 % | **40.14 min** | 4.86 min |
| Sinda CHIKHAOUI | 40.0 min | 40.64 min | +1.6 % | **40.64 min** | 4.36 min |
| Amine MANSOURI | 37.75 min | 39.68 min | +5.1 % | **39.68 min** | 5.32 min |
| Elyes KEFI | 37.75 min | 40.58 min | +7.5 % | **40.58 min** | 4.42 min |
| Fares LAAJILI | 38.75 min | 40.13 min | +3.6 % | **40.13 min** | 4.87 min |
| Sarah BARGAOUI | 37.75 min | 39.82 min | +5.5 % | **39.82 min** | 5.18 min |
| Selim MANSOURI | 37.5 min | 39.88 min | +6.3 % | **39.88 min** | 5.12 min |
| Ahmed BAKIR | 37.0 min | 39.65 min | +7.2 % | **39.65 min** | 5.35 min |
| Noa MANIACI | 39.5 min | 40.95 min | +3.7 % | **40.95 min** | 4.05 min |
| Ahmad BELDI | 35.75 min | 40.77 min | +14.0 % | **40.77 min** | 4.23 min |
| Donia KHADHRANI | 36.75 min | 41.81 min | +13.8 % | **41.81 min** | 3.19 min |
| Malek KHADHRANI | 37.25 min | 41.49 min | +11.4 % | **41.49 min** | 3.51 min |
| Ahmad BELDI | 38.0 min | 38.66 min | +1.7 % | **38.66 min** | 6.34 min |
| Ahmed BENHADJ SALEM | 40.5 min | 40.17 min | -0.8 % | **40.5 min** | 4.5 min |

## Verdict par couple élève × matière

| Élève | Niveau | Matière | Personnalisation | Docimologie | Scientifique | Verdict |
|---|---|---|:--:|:--:|:--:|:--:|
| Fares DARGHOUTH | 4e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Ines KEFI | 4e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Sinda CHIKHAOUI | 4e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Amine MANSOURI | 3e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Elyes KEFI | 3e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Fares LAAJILI | 3e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Sarah BARGAOUI | 3e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Selim MANSOURI | 3e | Mathématiques | PASS | PASS WITH WARNINGS | PASS | **PASS WITH WARNINGS** |
| Ahmed BAKIR | 2nde | Mathématiques | PASS | PASS | PASS | **PASS** |
| Noa MANIACI | 2nde | Mathématiques | PASS | PASS | PASS | **PASS** |
| Ahmad BELDI | 1ere_spe | Mathématiques | WARNING | PASS | PASS | **PASS WITH WARNINGS** |
| Donia KHADHRANI | 1ere_spe | Mathématiques | WARNING | PASS | PASS | **PASS WITH WARNINGS** |
| Malek KHADHRANI | 1ere_spe | Mathématiques | WARNING | PASS | PASS | **PASS WITH WARNINGS** |
| Ahmad BELDI | 1re_nsi | NSI | PASS | PASS | PASS | **PASS** |
| Ahmed BENHADJ SALEM | 1re_nsi | NSI | PASS | PASS | PASS | **PASS** |

| | Nombre |
|---|:--:|
| PASS | 4 |
| PASS WITH WARNINGS | 11 |
| FAIL | 0 |

## Avertissements résiduels, et pourquoi ils demeurent

| Avertissement | Élèves | Pourquoi il ne peut pas être levé |
|---|---|---|
| La compétence « statistiques » n'est travaillée qu'à la séance 5 du niveau, bien qu'elle soit diagnostiquée initialement | 8 élèves de 4e et 3e | c'est la progression réelle du stage, décidée avant cette mission. L'item correspondant relève de l'application d'une notion diagnostiquée, et la compétence est marquée pour un contrôle différé |
| Aucun livret personnalisé S2 à S4 en Première spécialité | Ahmad Beldi, Donia Khadhrani, Malek Khadhrani | ces documents n'existent pas. Les fabriquer serait inventer une trajectoire. La personnalisation repose sur le diagnostic et la remédiation seuls, et le dossier enseignant le dit |
| Aucune progression chiffrée pour aucun élève | les 15 | les réponses item par item du positionnement initial n'ont pas été conservées. C'est une limite de données, pas de méthode : le jour où ces réponses seront disponibles, le statut `parallel_measures` existe déjà et le calcul suivra |

## Ce qui reste à décider par un humain

| # | Point | Décision attendue |
|---|---|---|
| 1 | Les références BO/NOR ajoutées aux blueprints proviennent de l'audit du 21 août, elles n'ont pas été vérifiées au Bulletin officiel | `verifie_par_un_humain: false` est porté dans chaque blueprint : confirmer avant toute diffusion externe |
| 2 | Bilan de positionnement en Français d'Elyes Kefi, sans stage de Français dans le dépôt | déterminer s'il s'agit d'un stage réellement suivi |
| 3 | Contenu mathématique des 100 items | relecture disciplinaire humaine, quels que soient les contrôles automatiques |
| 4 | Écart de couleur entre la charte LaTeX (`#0B2347`) et la charte CSS (`#071A3A`) | aligner les deux chaînes, ou assumer deux nuances proches |
| 5 | Sarah Bargaoui : six priorités au dossier, deux traitées | confirmer l'arbitrage |
| 6 | Selim Mansouri : trois domaines encore à diagnostiquer | programmer un diagnostic complémentaire |
| 7 | Ahmad BELDI (NSI) : cinq questions du positionnement non traitées | annoncer à la famille le périmètre réel de comparaison |

## Commandes de vérification

```bash
python3 S5_cloture/tools/generate_s5.py        # 45 .tex + JSON, sortie déterministe
./S5_cloture/tools/build_pdf.sh                # 45 PDF
python3 S5_cloture/tools/validate_s5.py        # 7611 contrôles bloquants
python3 S5_cloture/tools/verify_items.py       # contre-résolution des 100 items
python3 S5_cloture/tools/raster_check.py       # 364 pages analysées une par une
python3 S5_cloture/tools/audit_docimologie.py  # deux estimateurs de durée indépendants
python3 S5_cloture/tools/review_personnalisation.py
python3 S5_cloture/tools/tests/test_analyze_s5.py
python3 S5_cloture/tools/make_release.py       # paquets release et audit
```

---

*Toutes les mesures de ce rapport sont relevées par les scripts de `S5_cloture/tools/` et reproductibles. Aucune n'est saisie à la main.*
