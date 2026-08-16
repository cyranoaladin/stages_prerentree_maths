# QA accessibilité — 2026-08-16

## Outillage

- Axe : absent (`which axe` → introuvable).
- Lighthouse : absent (`npx --no-install lighthouse --version` → paquet non installé, refusé en mode `--no-install`).
- Playwright (Python) : absent (`import playwright` → `ModuleNotFoundError`).

Aucun de ces outils n'étant disponible localement sans téléchargement réseau (interdit par la règle « travail local uniquement »), le contrôle a été fait par **analyse statique exhaustive** du HTML généré (`html.parser` de la bibliothèque standard Python), sur la totalité des 213 pages de `dist/site-public` (67) et `dist/site-private` (146). Aucun rendu réel de navigateur, donc aucune vérification de contraste calculé, de focus visuel réel ou de comportement de lecteur d'écran — ces points restent non testés et ne doivent pas être considérés comme validés.

## Résultats par contrôle (213 pages)

| Contrôle | Résultat | Pages en défaut |
|---|---|---|
| `<html lang="fr">` | 213/213 conformes | 0 |
| `<meta name="viewport">` présent | 213/213 conformes | 0 |
| Lien d'évitement (skip-link) | 213/213 conformes | 0 |
| Landmarks `header`/`nav`/`main`/`footer` | 213/213 conformes | 0 |
| Ordre des titres (pas de saut de niveau) | 192/213 conformes | **21** |
| `<img>` avec `alt` non vide | 213/213 conformes (0 image trouvée dans le contenu généré, hors logos dans le gabarit) | 0 |
| `<table>` avec `<th>` | 213/213 conformes (aucun tableau sans en-tête) | 0 |
| `tabindex` positif (piège clavier) | 213/213 conformes (aucun) | 0 |

## Détail des 21 sauts de niveau de titre

- 4 pages du site public, 17 pages du site privé (chevauchement attendu : chaque document public existe aussi en miroir privé).
- Deux causes distinctes identifiées :
  1. **Cause structurelle** (majorité des cas, ex. `1ere_spe_S1_PROF_Fiche.html`, `4e_MASTER_Documentation_Stage.html`) : le gabarit ajoute un `<h1>` (titre de page) puis Pandoc restitue le contenu à partir de `##` (shifté en `<h2>`/`<h3>` par `--shift-heading-level-by=1`) ; certains documents sources utilisent des niveaux `####` directement sous un `##` sans passer par `###`, ce qui est un défaut de structuration Markdown source, pas un défaut du moteur de rendu.
  2. **Cause critique** (au moins 1 cas confirmé, `1ere_spe_S3_ELEVE_Activite.html`, probablement davantage — recoupement avec le défaut LaTeX décrit ci-dessous) : une formule mathématique mal délimitée (`[` suivi de `\overrightarrow{AB}` puis d'une ligne `====`) est interprétée par Pandoc comme un titre Markdown *setext*, ce qui crée un `<h2>` fantôme contenant du code LaTeX brut au lieu d'une formule rendue. Ce cas est **critique** : il ne s'agit pas seulement d'un défaut d'accessibilité mais d'une corruption visible du contenu pédagogique. Signalé également dans `reports/NAVIGATION_QA.md` pour routage vers l'audit mathématique et la correction de `tools/build.py::render_fragment` (pipeline Pandoc `--mathml` qui ne reconnaît que `$...$`/`$$...$$`, pas les délimiteurs `(...)`/`[...]` utilisés dans au moins 23 documents sources).

## Comptage retenu

Le saut de niveau de titre est classé par les outils usuels (axe-core, règle `heading-order`) en sévérité **modérée**, pas critique, sauf lorsqu'il s'accompagne d'une perte de contenu (cas 2 ci-dessus, classé critique ici car le contenu affiché est erroné, pas seulement mal structuré).

```text
HTML_CRITICAL_A11Y_COUNT=1
HTML_SERIOUS_A11Y_COUNT=20
```

- `HTML_CRITICAL_A11Y_COUNT=1` : le cas confirmé de formule LaTeX cassée générant un titre fantôme avec contenu corrompu (`1ere_spe_S3_ELEVE_Activite.html`, présent en public et en privé — compté une fois par défaut distinct, pas par page miroir). Il est probable que d'autres des 23 documents sources touchés par le même défaut LaTeX génèrent le même type de titre fantôme — seul celui-ci a été confirmé par lecture directe du rendu ; les autres restent à vérifier un par un par l'agent d'audit mathématique avant de clore ce point.
- `HTML_SERIOUS_A11Y_COUNT=20` : les autres sauts de niveaux de titre, de nature structurelle (Markdown source mal hiérarchisé), sans perte de contenu constatée.

## Contraste de couleur — calcul WCAG (ajouté par l'intégrateur, 2026-08-16)

Un moteur de rendu réel restant indisponible localement, les ratios de contraste ont été calculés directement
(luminance relative WCAG 2.1, formule sRGB) pour chaque paire texte/fond effectivement utilisée dans
`assets/site.css`, plutôt que laissés non vérifiés :

| Paire | Premier plan | Fond | Ratio | Seuil AA texte normal (4,5:1) |
|---|---|---|---:|---|
| Corps de texte | `#172033` | `#fffdf7` | 15,99 | OK |
| En-tête / pied de page | `#ffffff` | `#071A3A` | 17,24 | OK |
| Bouton (`.button`, `button`) | `#08142d` | `#C9A227` | 7,56 | OK |
| Lien | `#073b8e` | `#fffdf7` | 10,19 | OK |
| En-tête de tableau (`th`) | `#ffffff` | `#071A3A` | 17,24 | OK |
| `.notice` | `#172033` | `#fff6c9` | 14,93 | OK |
| `.confidential` | `#6f0f16` | `#fff0f0` | 10,81 | OK |
| Fil d'Ariane | `#172033` | `#e7ebf1` | 13,60 | OK |
| Contour de focus | `#005fcc` | `#fffdf7` | 5,88 | OK |

Les 9 paires utilisées dépassent largement le seuil AA de 4,5:1 pour texte normal (le plus faible est 5,88:1).
Aucune information n'est portée uniquement par la couleur (badges et notices utilisent aussi texte/bordure).
**Ce contrôle reste un calcul statique sur les couleurs déclarées, pas un rendu réel dans un navigateur** :
il ne couvre pas d'éventuels effets d'anti-aliasing, de transparence ou de survol non déclarés en CSS.

## Ce qui n'a pas pu être testé

- Focus visuel effectif (dépend des règles `:focus-visible` de `assets/site.css`, non exécutées dans un moteur de rendu — la règle existe et l'outline calculé ci-dessus est conforme, mais son affichage réel n'a pas été observé).
- Débordement horizontal réel à 320 px/390 px (aucun moteur de rendu disponible ; voir `reports/UX_AUDIT.md`).
- Respect de `prefers-reduced-motion` en usage réel (la règle CSS est présente et statiquement correcte, non observée en conditions réelles).

Ces points doivent être considérés **non validés**, pas conformes par défaut, tant qu'un test avec un moteur de rendu n'aura pas été effectué.
