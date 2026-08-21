
## 6. Compilation

Moteur : `pdflatex` piloté par `latexmk`, en `-interaction=nonstopmode -halt-on-error`. Le style partagé est trouvé par `TEXINPUTS`, sans duplication de fichier.

| Contrôle | Résultat |
|---|---|
| Documents LaTeX compilés | 45 / 45 |
| Échecs de compilation | 0 |
| `Undefined control sequence` | 0 |
| `LaTeX Warning: Reference` | 0 |
| `Overfull \hbox` | 0 |
| Fichiers auxiliaires laissés dans les dossiers élèves | 0 (nettoyés par `latexmk -c`) |

Commande de reproduction : `./S5_cloture/tools/build_pdf.sh`. Les journaux complets sont conservés dans `S5_cloture/_build_logs/`.

## 7. Validation automatique

| Indicateur | Valeur |
|---|---|
| Contrôles exécutés | 7611 |
| Échecs critiques | 0 |
| Avertissements | 0 |
| Résultat | **PASS** |

Le validateur vérifie notamment : présence des 15 couples, des 45 `.tex` et des 45 PDF, présence et validité des sept JSON par élève, unicité des `item_id`, appartenance des `skill_id` au référentiel du niveau, somme des points égale à 20, durée de l'évaluation inférieure à 45 minutes, durée du travail égale à 75 minutes, cohérence manifeste ↔ corrigé, présence d'un barème pour chaque item et somme des critères égale aux points, présence de chaque item dans le PDF d'évaluation, cohérence nom / niveau / matière dans les PDF, validité des liens vers le diagnostic initial, existence des fichiers sources référencés, absence de chemin absolu, absence de donnée post-évaluation pré-remplie, absence de données de test dans la livraison, et absence de tout corrigé dans les documents élèves.

**Contrôle anti-corrigé.** Pour chacun des 180 items, la réponse attendue est normalisée (commandes LaTeX retirées, minuscules, espaces et ponctuation supprimés) puis recherchée dans la source et dans le texte extrait du PDF de chaque document élève. Douze marqueurs de document enseignant y sont également recherchés.

## 8. Contrôle visuel

18 documents rasterisés et inspectés page par page, couvrant les cinq niveaux, les deux matières et les trois types de document, y compris premières et dernières pages, pages de tableaux, de figures, de code et de zones de réponse.

| Défaut détecté | Correction apportée |
|---|---|
| collision entre l'en-tête gauche et l'en-tête droit sur les dossiers enseignants | en-tête droit raccourci en « Dossier enseignant — confidentiel » et composé en \small |
| la ligne « Certitude » et la ligne « Contrôle » se chevauchaient à l'intérieur des encadrés (un \hfill ne s'étire pas de façon fiable dans un tcolorbox) | macros \certline et \certbox réécrites sur deux lignes distinctes |
| la ligne d'aide graduée débordait sur une seconde ligne | libellés raccourcis dans la macro \aideline |
| tableau « le fil des cinq séances » mal aligné verticalement | remplacé par une liste à puces à étiquettes |
| pages remplies au tiers à cause d'un saut de page systématique entre les phases et entre les parties de l'évaluation | sauts de page remplacés par \needspace, sauf avant la partie A ; espaces de réponse portés à deux lignes minimum en partie A et élargis dans les phases de consolidation |
| une seule ligne de réponse pour des exercices de consolidation traités au stylo | table SPACE_UP dans le générateur : chaque exercice de phase 2 et 3 gagne une ligne |
| espace de brouillon isolé sur une page presque vide en partie A | déplacé en fin de partie C, dimensionné au tiers de la hauteur de texte |
| libellé « Espace de brouillon — non corrigé » déclenchant à tort le contrôle anti-corrigé | libellé remplacé par « non relevé » |
| caractères Unicode mathématiques (∪, ×, −, ²) issus des dossiers sources, non compilables en pdfLaTeX | table de substitution TEX_SUBST dans le générateur |
| colonne trop étroite dans le tableau d'engagement de la phase 5 : coupures « systémati-quement » et « der-nier » | tableau supprimé, remplacé par deux lignes pleine largeur avec filet de réponse calculé sur \linewidth |

Défaut assumé, non corrigé :

- certaines pages de livret de travail se terminent au quart inférieur vide lorsque la phase suivante réclame 62 mm de hauteur — accepté : la coupure d'une phase entre deux pages serait plus gênante en séance que l'espace résiduel, qui reste utilisable comme brouillon

## 9. Données structurées

| Contrôle | Résultat |
|---|---|
| Fichiers JSON | 133 |
| JSON syntaxiquement valides | 133 |
| JSON invalides | 0 |
| Encodage | UTF-8, sans commentaire non standard |
| `item_id` uniques | 180 / 180 |
| Profils dont `post_stage.status` vaut `awaiting_assessment` | 15 / 15 |

Sept fichiers par élève : profil d'apprentissage, blueprint d'évaluation, gabarit de saisie, schéma d'analyse et gabarit de plan de rentrée du côté élève ; manifeste détaillé des items et corrigé structuré du côté enseignant.

## 10. Scripts et tests

| Script | Rôle | Vérification |
|---|---|---|
| `tools/build_audit.py` | inventaire, audit S1-S4, registre des conflits | exécuté, 15 élèves, toutes les sources déclarées présentes |
| `tools/generate_s5.py` | génération des 45 `.tex` et des 105 JSON | exécuté, sortie déterministe |
| `tools/build_pdf.sh` | compilation de tous les documents | 45 réussites, 0 échec |
| `tools/validate_s5.py` | validation bloquante de la livraison | 7611 contrôles, 0 échec |
| `tools/analyze_s5.py` | calculs déterministes après passation | 48 tests, 48 réussis, 0 échoués |
| `tools/review_personnalisation.py` | contrôle de continuité S1-S4 → S5 | exécuté, 0 reprise à l'identique |
| `tools/audit_docimologie.py` | audit des 15 évaluations | exécuté, 0 anomalie bloquante |
| `tools/render_bilan.py` | remplissage du bilan à partir des données calculées | exécuté sur le jeu synthétique |
| `tools/build_reports.py` | assemblage de l'index et du rapport qualité | exécuté |
| `_teacher_private/tests_s5_nsi.py` | tests déterministes des productions de code NSI | exécuté |

### Jeu de données de test

`tools/tests/fixture_synthetique/` contient un élève fictif — « ELEVE SYNTHETIQUE », identifiant `eleve-synthetique-test` — construit sur le noyau commun réel du niveau 4e et sur quatre items individualisés fictifs. Toutes ses données portent le marqueur `SYNTHETIQUE`, et le validateur vérifie que ce marqueur n'apparaît nulle part ailleurs. L'élève fictif n'est volontairement pas enregistré dans le registre des élèves : la ligne de commande de `analyze_s5.py` le refuse, ce qui rend impossible toute confusion avec un élève réel. Deux copies de code délibérément fautives (`copie_SYNTHETIQUE_ahmad.py`, erreur de syntaxe, boucle infinie) servent à éprouver le harnais NSI.

### Ce que les tests couvrent

- score brut, note sur 20, taux de réussite, décomposition par partie et par nature d'item ;
- répartition des points entre compétences pour un item qui en mobilise plusieurs ;
- absence de delta lorsque la mesure initiale manque ou que la tâche n'est pas parallèle ;
- plafonnement de la maîtrise 4 en l'absence de réussite sur une tâche de transfert ;
- profil d'erreurs et code dominant ;
- cellules de calibration réussite / confiance, y compris la réussite partielle non classée ;
- plafonnement du nombre de compétences classées P1 ;
- structure du plan de quatre semaines ;
- refus d'un score manquant, hors barème, d'un code d'erreur inconnu, d'une saisie incomplète, d'un fichier appartenant à un autre élève et d'un gabarit non renseigné.

## 11. Contradictions de sources

10 contradictions ont été relevées, tranchées et consignées dans `_audit/conflits_sources.json`. Aucune n'a été résolue silencieusement.

| Réf. | Objet | Décision |
|---|---|---|
| CONF-01 | Architecture temporelle de la séance 5 | Appliquer 75 min + 45 min dans S5_cloture. Les fiches S5 existantes ne sont pas modifiées. |
| CONF-02 | Évaluation finale de niveau contre évaluation finale individualisée | Produire dans S5_cloture une évaluation distincte de 12 items (14 points communs, 6 points individualisés, total 20), sans toucher à l'évaluation finale de niveau. |
| CONF-03 | Livrets S4/S5 personnalisés déjà produits pour trois élèves de Quatrième | Ne rien écraser. Produire la version conforme dans S5_cloture, et relever les énoncés déjà utilisés dans ces livrets afin de ne pas les reprendre. |
| CONF-04 | Périmètre : le registre content/students.json ne couvre pas la NSI | Le périmètre S5 retenu est de 15 couples élève × matière : les 13 élèves de mathématiques et les 2 élèves de NSI. |
| CONF-05 | Deux positionnements pour Ahmed BENHADJ SALEM | Retenir le positionnement Première comme référence de comparaison initiale ; utiliser le positionnement Terminale uniquement comme confirmation de l'erreur d'accumulateur. |
| CONF-06 | Un bilan de Français existe pour Elyes Kefi, sans stage de Français dans le dépôt | Hors périmètre S5. Aucun dossier S5 de Français n'est produit ; l'élément est signalé pour validation humaine. |
| CONF-07 | Dossier Sarra ESSANAA présent dans le répertoire | Hors périmètre. Aucune séance S5 n'est produite pour cette personne. |
| CONF-08 | Absence de dossiers personnalisés S2 à S5 en Première spécialité | Reconstruire la trajectoire de ces trois élèves à partir des séances de niveau et du plan de remédiation individuel uniquement, et le signaler explicitement dans chaque dossier enseignant. |
| CONF-09 | Absence de preuve documentée entre le diagnostic initial et la séance 5 | Le statut de chaque compétence avant la S5 est fondé sur le seul diagnostic initial, avec la mention explicite « preuve postérieure non documentée ». |
| CONF-10 | Casse des noms d'élèves | Uniformiser dans S5_cloture : prénom en casse ordinaire, nom de famille en capitales, pour les quinze dossiers. |

## 12. Hypothèses retenues

| Hypothèse | Portée | Justification |
|---|---|---|
| Le statut d'une compétence avant la S5 est déduit du statut de domaine écrit au dossier individuel | les 15 élèves | aucune autre source ne documente l'état des compétences ; les précisions explicites du dossier surchargent cette déduction, compétence par compétence |
| La conversion du statut qualitatif vers l'échelle de maîtrise 0-4 est : acquis → 3, en voie d'acquisition → 2, fragile → 1, non évalué → absence de valeur | calcul des deltas | conversion déclarée dans chaque sortie d'analyse et signalée comme grossière ; un écart d'un point d'échelle est présenté comme une tendance, non comme un acquis |
| Une compétence sans item au diagnostic initial ne peut pas produire de delta | tous niveaux | règle appliquée par le script, testée, et matérialisée par `comparison_status` |
| Le noyau commun de l'évaluation est strictement identique pour tous les élèves d'un même niveau | équité | vérifié par comparaison des énoncés dans `audit_docimologie.py` |
| La durée cible par item est normalisée (1,5 min en partie A, 4 à 5 min en partie B, 9 et 4 min en partie C) | les 15 évaluations | garantit une somme de 41 minutes et 4 minutes de marge pour tous, et rend les copies comparables |
| Les compétences travaillées uniquement lors de la séance 5 du niveau mais diagnostiquées initialement restent comparables | statistiques en 4e et 3e | l'item correspondant relève de l'application d'une notion diagnostiquée, non du transfert d'un contenu nouveau |
