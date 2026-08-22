# Stages de pré-rentrée Mathématiques 2026-2027

Ce paquet local rassemble les stages d’entrée en `4e`, `3e`, `2nde` et `1ere_spe`. Il génère un portail hors ligne, des PDF A4 et des packs d’impression à partir des Markdown opérationnels.

## Démarrer

```bash
python3 -m pip install --require-hashes -r requirements.lock
make all
make serve
```

Ouvrez ensuite `http://localhost:8000`. Le portail public est dans `dist/site-public/`; le portail confidentiel est dans `dist/site-private/` et ne doit pas être diffusé.

## Dépendances

- **Python** :
  - `requirements.in` contient les dépendances directes du projet ;
  - `requirements.constraints` fixe les versions transitives de l’environnement validé ;
  - `requirements.lock` est généré avec `pip-compile`, contient l’ensemble des dépendances transitives verrouillées et leurs hashes SHA-256 ;
  - l’installation de production/CI doit utiliser `python3 -m pip install --require-hashes -r requirements.lock`.
- **Système** : Pandoc, qpdf, Poppler (`pdftotext`), Ghostscript ou ImageMagick (`convert`/`identify`) pour l’inspection visuelle des PDF.
- Aucune police n’est téléchargée à distance : le build fonctionne hors ligne.

## Source et confidentialité

- `05_SOURCES/` contient les programmes canoniques : le build ne les modifie pas.
- `04_NOMINATIFS/` et `dist/site-private/` contiennent des données de mineurs : circulation locale strictement limitée.
- Les PDF sources initiaux sont préservés et exclus des packs générés.
- Le registre nominatif canonique du pipeline Mathématiques (13 élèves) est `content/students.json` ; `tools/build.py` ne contient plus aucun nom en dur.
- Les stages Terminale ont leur propre registre, `content/students_terminale.json` : les deux ne se mélangent pas.

## Stages de pré-rentrée Terminale

Le dépôt contient deux modules de pré-rentrée pour l'entrée en Terminale, `tle_spe`
(spécialité mathématiques) et `tle_nsi` (numérique et sciences informatiques). Comme
`1re_nsi/`, ils forment un **pipeline de documentation distinct** : ils ne sont pas
ramassés par `tools/build.py`, dont la constante `LEVELS` reste inchangée, et ils
n'utilisent pas `content/students.json`.

La cohorte compte neuf élèves répartis en deux groupes selon la seconde spécialité
conservée. Le groupe organise les séances : un élève peut y être rattaché sans suivre
exactement la combinaison qui lui donne son nom, et son livret le précise alors.


| Groupe | Spécialités | Effectif | Modules suivis |
|---|---|---:|---|
| Groupe 1 | Mathématiques et NSI | 5 | `tle_spe` et `tle_nsi` |
| Groupe 2 | Mathématiques et Physique-Chimie | 4 | `tle_spe` |

Deux élèves suivent en outre l'option mathématiques expertes, traitée en module
complémentaire.

### Trois sources, et rien d'autre

L'individualisation des livrets ne repose sur aucune saisie manuelle :

| Fichier | Rôle |
|---|---|
| `content/students_terminale.json` | Registre nominatif de la cohorte : groupes, matières, bilans sources |
| `content/diagnostics_terminale.json` | Diagnostics extraits des 14 bilans PDF, item par item |
| `content/items_terminale.json` | Banque des 54 items : compétence évaluée, geste correct, lien avec le programme de Terminale, exercice-variante corrigé |

Chaque livret reprend, pour son élève, l'énoncé exact de chaque item manqué, la réponse
donnée, la réponse attendue et l'origine de l'erreur telle qu'établie par le bilan. Aucun
contenu n'est extrapolé au-delà.

### Commandes

```bash
make terminale         # régénère les documents nominatifs des deux modules
make terminale-check   # échoue si un document committé est périmé
make terminale-test    # suite de tests dédiée
make terminale-extract # ré-extrait les diagnostics depuis les bilans PDF (voir ci-dessous)
```

`make terminale-extract` **n'est pas exécutée en intégration continue** : le rendu du texte
d'un PDF dépend de la version de `pypdf`, et les versions antérieures à la 6.16 coupent les
mots au milieu (« T erm inale ») sans rien signaler. `content/diagnostics_terminale.json`
est donc un artefact committé et relu ; le script refuse de s'exécuter sous une version qui
dégraderait l'extraction, et `tests/test_terminale.py` compare les 18 énoncés de chaque
instrument à la banque, caractère pour caractère.

### Rendu imprimable

```bash
make terminale-pdf        # assemble les PDF A4 sous dist/terminale/
make terminale-pdf-list   # liste ce qui serait produit, sans rendre
```

`tools/build_terminale_pdf.py` assemble les Markdown en dossiers prêts à distribuer : un
dossier par élève et par matière, les corrigés tenus à part, et les fiches de séances à
photocopier. Un pack élève ne peut pas contenir de corrigé — l'assemblage échoue plutôt que
de produire un fichier douteux.

Les PDF **ne sont pas versionnés** (`dist/terminale/` est ignoré) : leur binaire dépend de la
version de WeasyPrint et des polices installées. Le Markdown fait foi. Détail des réglages
d'impression et de la distribution : `tle_spe/00_MASTER/PRINT_GUIDE_TERMINALE.md`.

### Confidentialité

`tle_spe/04_NOMINATIFS/` et `tle_nsi/05_NOMINATIFS/` contiennent des données de mineurs.
Dans ces deux modules, le **seul** document commun nominatif est le tableau de bord
enseignant, qui porte aussi les liens vers les dossiers individuels : les index de module ne
nomment personne. Les tests vérifient qu'aucun nom ne figure ailleurs, qu'aucun élève
n'apparaît dans le dossier d'un autre, et qu'aucune feuille élève ne contient de corrigé.

## Module Première NSI

Le dépôt contient également un module indépendant `1re_nsi/` (stage Python, Première NSI). Il n’est **pas** intégré au pipeline mathématique `tools/build.py` (niveaux `4e`, `3e`, `2nde`, `1ere_spe`) : c’est un pipeline de documentation séparé, avec ses propres Markdown, HTML et PDF déjà générés et versionnés directement dans l’arborescence `1re_nsi/`. Point d’entrée : [`1re_nsi/00_MASTER/index.md`](1re_nsi/00_MASTER/index.md).

Voir `QUICK_START.md` et `PRINT_GUIDE.md` pour les usages courants.
