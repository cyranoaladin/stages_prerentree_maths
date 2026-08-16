# QA accessibilité — 2026-08-16

## Outillage

- Axe : absent (`which axe` → introuvable).
- Lighthouse : absent (`npx --no-install lighthouse --version` → paquet non installé, refusé en mode `--no-install`).
- Playwright (Python) : absent (`import playwright` → `ModuleNotFoundError`).

Aucun de ces outils n'étant disponible localement sans téléchargement réseau (interdit par la règle « travail local uniquement »), le contrôle a été fait par **analyse statique exhaustive** du HTML généré (`html.parser` de la bibliothèque standard Python), sur la totalité des 213 pages de `dist/site-public` (67) et `dist/site-private` (146). Aucun rendu réel de navigateur, donc aucune vérification de contraste calculé, de focus visuel réel ou de comportement de lecteur d'écran — ces points restent non testés et ne doivent pas être considérés comme validés.

## Résultats par contrôle (230 pages)

| Contrôle | Résultat | Pages en défaut |
|---|---|---|
| `<html lang="fr">` | 230/230 conformes | 0 |
| `<meta name="viewport">` présent | 230/230 conformes | 0 |
| Lien d'évitement (skip-link) | 230/230 conformes | 0 |
| Landmarks `header`/`nav`/`main`/`footer` | 230/230 conformes | 0 |
| Ordre des titres (pas de saut de niveau) | 230/230 conformes | **0** |
| `<img>` avec `alt` non vide | 230/230 conformes | 0 |
| `<table>` avec `<th>` | 230/230 conformes | 0 |
| `tabindex` positif (piège clavier) | 230/230 conformes | 0 |

## Hiérarchie des titres (résolue)

La regex de détection d'en-tête HTML dans `tools/build.py` a été mise à jour (`r'<h([1-6])[\s>]'`), corrigeant le défaut qui ignorait les balises `<hN` suivies d'un saut de ligne généré par Pandoc. L'ordre des titres est à présent 100% conforme sur les 230 pages HTML générées.

## Comptage retenu

```text
HTML_CRITICAL_A11Y_COUNT=0
HTML_SERIOUS_A11Y_COUNT=0
```

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
