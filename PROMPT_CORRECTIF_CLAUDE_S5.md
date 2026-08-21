# Prompt correctif à exécuter dans Claude CLI — S5 Nexus Réussite

Tu dois effectuer une passe corrective sur `S5_cloture/` à partir de l'audit indépendant ci-dessous. Ne reconstruis pas le projet à zéro : conserve ce qui est sain, corrige les défauts, régénère tous les artefacts dépendants, puis exécute une validation finale réellement indépendante.

## Règle de release

La livraison reste en HOLD tant que chacun des points bloquants n'est pas corrigé et testé. Ne transforme aucun FAIL en warning par simple changement de seuil. Ne masque aucune anomalie. Ne modifie aucun document source S1–S4 hors de `S5_cloture/`.

## 1. Supprimer l'audit temporel circulaire

- Retirer de `core.exam_items()` l'écrasement `src["minutes"] = common.ITEM_MINUTES[iid]`.
- Ne plus utiliser une table globale de temps dans le but de forcer 41 minutes.
- Conserver les temps propres aux items et construire un audit secondaire indépendant.
- Réestimer chaque item selon charge de lecture, nombre d'opérations, rédaction et niveau.
- Viser une épreuve réalisable en 45 min avec 3–5 min de marge.
- Les temps bruts actuels sont : 45 / 45 / 45 ; 45,5 / 45,5 / 46 / 45,5 / 45 ; 46,5 / 46 ; 45,5 / 47 / 47 ; NSI 54,5 et 55 min.
- Réduire fortement les deux évaluations NSI, sans sacrifier le noyau de compétences essentiel.

## 2. Interdire le faux delta de progression

Les profils indiquent qu'il n'existe pas de réponse initiale item par item. Il est donc interdit de convertir `acquis/en_voie_acquisition/fragile` en score initial pour calculer un `mastery_delta` numérique.

- Tant qu'une vraie réponse/mesure initiale appariée n'existe pas : `mastery_delta: null`.
- Remplacer `item_level/skill_level` par des statuts sémantiquement explicites : `parallel_measures`, `indicative_skill_comparison`, `post_only`, `not_comparable`.
- `parallel_measures` n'est autorisé que si deux mesures nominatives réelles sont disponibles.
- Interdire `progression_documented` et toute phrase « maîtrise X -> Y » sans mesure initiale réelle.
- Adapter `render_bilan.py` en conséquence et ajouter des tests de non-régression.

## 3. Scoring par critères, pas partage uniforme

Supprimer l'algorithme qui divise le score de l'item équitablement entre ses `skills`.

Chaque critère de barème doit disposer de :
- `criterion_id` unique ;
- `points` ;
- `skill_id` principal ;
- éventuellement `evidence_type` ;
- `subpart`.

Le fichier de réponses doit permettre la saisie par critère. Les scores de compétence doivent être agrégés depuis les critères réellement réussis.

## 4. Corriger le schéma JSON

Le schéma actuel exige `comparability` dans chaque skill alors que l'analyseur produit `comparison_status`.

- Définir un schéma canonique v2.
- Mettre toutes les sorties en conformité.
- Ajouter un test `jsonschema.validate()` sur la sortie réelle de `analyze_s5.py`.
- Aucun PASS si la sortie échoue au schéma.

Renommer `measurement_reliability` en `evidence_strength` ; ne pas appeler « fiabilité » un simple seuil de points.

## 5. Retention / remédiation immédiate

Pour toute compétence retravaillée pour la première fois en S5 puis testée immédiatement :
- `post_test_context = immediate_after_remediation` ;
- `retention_status = not_yet_verified` ;
- `recommended_delayed_check = true`.

Prévoir un mini-test différé semaine 1 ou 2. Le bilan parent doit dire « réussite immédiate à confirmer », jamais « acquis durablement consolidé » sur cette seule preuve.

Tout contenu nouveau de l'année N doit rester exclu de la mesure de progression N-1 -> N.

## 6. Corrections scientifiques obligatoires

1. Elyes KEFI 3e statistiques : l'encadrement de 11,25 entre 5 et 15 ne détecte pas l'omission de 5. Utiliser recomptage/somme/source-list comme contrôle détecteur.
2. Sinda CHIKHAOUI 4e : la duplication autour du milieu d'un côté produit en général un parallélogramme, pas un rectangle. Corriger l'explication de l'aire du triangle.
3. Ahmad BELDI 1re spé x³/x² : exiger une preuve générale plus un exemple ; ne pas laisser croire que l'exemple démontre le résultat universel.
4. Malek KHADHRANI 1re spé 1/x : deux valeurs réfutent la croissance mais ne démontrent pas la décroissance globale. Corriger consigne/réponse/barème.
5. Phase 4 4e : remplacer « aucune connaissance nouvelle » par une formulation de découverte guidée/pont vers la 4e.
6. Phase 4 3e : même correction pour double distributivité/fonctions.
7. Phase 4 1re spé : remplacer « la suite n'est qu'une évolution répétée » par une formulation exacte ; corriger l'ambiguïté « cinq premiers termes » du code `range(5)` qui affiche u1..u5.
8. NSI dichotomie : fixer la convention du milieu ou accepter explicitement 2/3 comparaisons selon la convention.
9. Revoir les codes d'erreur : ne pas pénaliser un contrôle non demandé ; ne pas étiqueter `CONCEPT` une méthode valide mais moins efficace.

Puis effectuer une contre-résolution explicite des 100 couples énoncé/réponse uniques et consigner le résultat dans `SCIENTIFIC_AUDIT.md` avec PASS/FAIL par item unique.

## 7. Références réglementaires 2026

Ajouter aux 5 blueprints un objet `curriculum_reference` complet.

- Seconde maths : nouveau programme BO n°14 du 2 avril 2026, NOR MENE2602914A, application rentrée 2026-2027.
- Première spécialité maths : BO n°14 du 2 avril 2026, NOR MENE2602917A, application rentrée 2026-2027.
- Cycle 4 : nouveau programme publié en 2026 mais application progressive : 5e en 2026-2027, 4e en 2027-2028, 3e en 2028-2029. Ne pas appliquer prématurément la nouvelle progression aux élèves entrant en 4e/3e en 2026.
- Première NSI : programme en vigueur BO spécial n°1 du 22 janvier 2019, NOR MENE1901633A.

Documenter pour chaque niveau la transition N-1 -> N réellement visée.

## 8. Sécurité du runner NSI

`tests_s5_nsi.py` utilise un sous-processus avec timeout mais ce n'est pas une sandbox.

Deux options acceptables :
- désactiver par défaut l'exécution automatique d'une copie non relue ; ou
- exécuter dans un conteneur jetable sans réseau, non privilégié, filesystem read-only sauf tmp, sans HOME/secrets, limites CPU/RAM/PID et timeout externe.

La documentation doit dire explicitement si l'exécution n'est pas sandboxée.

## 9. Release propre

- Supprimer tous les `.pyc` et `__pycache__` du paquet de release.
- Séparer `release` (fichiers réellement nécessaires) et `audit` (logs/tests/preuves).
- Conserver éventuellement les 45 logs seulement dans le paquet d'audit.
- Ajouter `source_evidence_manifest.json` avec chemins, SHA-256 et preuves utilisées afin que la traçabilité soit vérifiable sans le corpus complet.
- Ajouter `CANONICAL_DELIVERY.json` : pour chaque élève/matière, chemin exact du livret S5 et de l'évaluation finale à distribuer, et anciens documents superseded.

## 10. Revalidation finale obligatoire

Après corrections :

1. régénérer les 45 `.tex` et 45 PDF ;
2. compiler 45/45 ;
3. rasteriser et contrôler les 351+ pages ;
4. valider tous les JSON avec leur schéma ;
5. exécuter l'analyseur sur fixture synthétique puis valider sa sortie JSON ;
6. exécuter tous les tests ;
7. auditer les temps SANS table imposée ;
8. vérifier `mastery_delta == null` lorsque la baseline nominative manque ;
9. vérifier le scoring par critères ;
10. vérifier qu'aucune réponse/corrigé n'est présente dans les PDF élèves ;
11. vérifier l'absence de caches dans le paquet release ;
12. produire un `QA_REPORT_V2.md` qui distingue clairement PASS technique, scientifique, pédagogique/docimologique, données et sécurité.

Ne déclare pas la mission terminée tant qu'un FAIL critique subsiste. Retour final attendu : liste des corrections, fichiers modifiés, tests exécutés, résultats exacts, warnings résiduels justifiés, et chemin d'une nouvelle archive `S5_cloture_AUDIT_V2.tar.gz`.
