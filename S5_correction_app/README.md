# Nexus S5 — Correction & Bilans

Application web **locale** pour corriger les quinze évaluations S5 déjà distribuées, puis
produire les bilans de fin de stage.

> Les livrets et les évaluations ont été imprimés et remis aux élèves. Ils sont figés.
> L'application travaille **autour** d'eux : elle les affiche, elle ne les touche jamais.

---

## Lancer

```bash
make s5-correction-run
```

Puis ouvrir dans le navigateur :

```
http://127.0.0.1:8765
```

Pour arrêter : `Ctrl` + `C` dans le terminal. Tout est enregistré au fil de la saisie ;
rien n'est perdu en fermant l'onglet.

## Première installation

```bash
make s5-correction-install     # dépendances Python
make s5-correction-init        # base, référentiel V3, contrôle des empreintes
make s5-correction-run
```

Au premier démarrage, l'application crée sa base, importe les 15 élèves, les 180 items et
les 337 critères depuis la couche V3, puis recalcule les 60 empreintes des documents
distribués. Si une empreinte a changé, elle démarre en lecture seule et le dit.

## Corriger, en cinq gestes

1. **Choisir l'élève** dans le tableau de bord.
2. **Corriger** : le sujet distribué s'affiche à gauche, la grille à droite. Un clic par
   critère. Tout s'enregistre seul.
3. **Valider** : l'application vérifie la cohérence avant de verrouiller.
4. **Analyser** : score brut, acquis N−1, passerelles, compétences, erreurs, plan de
   quatre semaines.
5. **Générer le bilan** : relire les textes, les modifier si besoin, cliquer sur
   « Générer le PDF ».

En usage courant, il n'y a rien d'autre à faire au terminal que `make s5-correction-run`.

## Trois règles de correction

1. **Un critère intégralement réussi ne porte aucun code d'erreur.** Une observation
   libre reste possible.
2. **Un zéro n'oblige à aucune cause.** « Non répondu » et « zéro, cause non identifiée »
   existent : on ne fabrique pas une explication qu'on n'a pas observée.
3. **Une méthode correcte n'est jamais une erreur**, même si elle n'est pas la plus
   rapide. Cochez la case prévue et écrivez l'observation.

## Raccourcis clavier

| touche | effet |
| --- | --- |
| `0`…`9` | applique le score proposé à ce rang |
| `F` | plein score, puis critère suivant |
| `N` | non répondu, puis critère suivant |
| `E` | ouvre les codes d'erreur |
| `O` | place le curseur dans l'observation |
| `→` `←` | critère suivant / précédent |

Aucun raccourci ne supprime une saisie.

## Ce que l'application refuse de faire

- calculer une progression chiffrée entre le début et la fin du stage — les réponses
  initiales question par question n'existent pas ;
- laisser une non-réussite sur une notion de découverte devenir une « lacune » ;
- générer un bilan à partir d'une correction non validée ;
- écraser un texte que vous avez modifié et approuvé ;
- écrire quoi que ce soit dans les documents distribués.

## Confidentialité

Les corrections, la base et les bilans restent dans `runtime/`, qui est exclu de Git. Le
serveur n'écoute que `127.0.0.1`. Aucune ressource distante n'est chargée : ni police, ni
CDN, ni API. Aucun modèle de langage n'est appelé — la génération déterministe suffit et
c'est elle qui est utilisée.

## Documentation

| document | contenu |
| --- | --- |
| `docs/ARCHITECTURE.md` | structure du code et flux de données |
| `docs/DATA_MODEL.md` | tables, identifiants, exactitude des points |
| `docs/CORRECTION_RULES.md` | invariants, statuts, règles pédagogiques |
| `docs/REPORT_GENERATION.md` | blocs, provenance, LaTeX, PDF |
| `docs/PRIVACY_SECURITY.md` | données, réseau, chemins, sous-processus |
| `docs/OPERATIONS_RUNBOOK.md` | démarrer, sauvegarder, restaurer, dépanner |
| `docs/PILOT_REAL_COPY_VALIDATION.md` | validation sur la première copie réelle |
| `docs/TEST_REPORT.md` | ce qui est testé, et ce qui ne l'est pas |
| `docs/QA_FINAL.md` | portes de qualité et verdicts |
| `docs/TECHNICAL_DEBT.md` | dettes restantes, sans en cacher |
