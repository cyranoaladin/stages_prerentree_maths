# QA navigation et expérience utilisateur — 2026-08-16

Portée : `dist/site-public` (67 pages HTML) et `dist/site-private` (146 pages HTML), générés par `python3 tools/build.py all` après la correction du bug de classification des buckets dans `tools/build.py`. Contrôle automatisé par script Python (`html.parser`), pas d'échantillonnage — toutes les pages des deux sites ont été analysées.

## Constat transverse prioritaire (hors périmètre de ce rapport, à router vers l'audit mathématique)

23 documents sources (2nde, 3e, 1re spé — 4e non affecté) contiennent des expressions LaTeX écrites entre parenthèses `(...)` ou crochets `[...]` au lieu des délimiteurs `$...$` / `$$...$$` que Pandoc reconnaît. Conséquence concrète observée : dans `1ere_spe/02_SEANCES/S3/1ere_spe_S3_ELEVE_Activite.md` (lignes 89-91), un bloc `[` suivi de `\overrightarrow{AB}` puis d'une ligne `====` est interprété par Pandoc comme un titre Markdown *setext* — la formule disparaît du rendu et le code `\begin{pmatrix}...\end{pmatrix}` apparaît ensuite en texte brut visible dans le document élève. Ce même défaut existe dans au moins 23 fichiers (62 pages HTML générées, sites public+privé confondus, avant dédoublonnage). C'est un défaut bloquant au sens de la section 6.4 et 12.1 du mandat (« aucun code LaTeX brut visible dans la version élève », « pas de formule cassée »). Ne relève pas de mon périmètre (build.py / contenu mathématique) : signalé ici pour routage vers l'agent d'audit mathématique et vers la correction de `tools/build.py::render_fragment`.

## 1. Liens internes

- Liens relatifs contrôlés : tous les `href`/`src` de `a`, `link`, `script`, `img` sur 213 pages HTML (67 + 146).
- **BROKEN_LINK_COUNT = 42** (6 cibles distinctes, répétées) :
  - **40 occurrences** — cause unique : `tools/build.py:256`, dans `level_page()`. Quand une action de séance (Professeur/Élève/Supports/Aides) n'est pas publique, le code génère `<a href="../site-private/{level}/index.html">` depuis `dist/site-public/{level}/index.html`. Un seul niveau de `../` ne suffit pas : le fichier est à `dist/site-public/{level}/index.html`, il faut remonter deux niveaux pour atteindre `dist/`. Le lien pointe donc vers l'inexistant `dist/site-public/site-private/{level}/index.html` au lieu de `dist/site-private/{level}/index.html`.
    **Correctif suggéré** : remplacer `f'<a href="../site-private/{level}/index.html">'` par `f'<a href="../../site-private/{level}/index.html">'` à la ligne 256.
    Touche les 4 pages de niveau publiques (`dist/site-public/{4e,3e,2nde,1ere_spe}/index.html`), 10 occurrences chacune (5 séances × 2 libellés privés : Professeur et Aides, puisque PROF_Fiche et AIDES_Cartes restent confidentiels par mention nominative alors qu'Élève et Supports sont publics).
  - **2 occurrences** — le portail (public et privé) pointe vers `../reports/FINAL_DELIVERY_REPORT.md`, qui n'existe pas encore au moment de cet audit. Non-bug de code : se résoudra automatiquement dès que ce rapport sera écrit dans `reports/` et que `python3 tools/build.py html` (qui copie `reports/` vers `dist/reports/`) sera relancé.
- **EXTERNAL_RESOURCE_COUNT = 0** — aucune ressource `http://`/`https://` chargée dans les 213 pages. Conforme à la règle « travail local uniquement ».
- **ORPHAN_ACTIVE_FILE_COUNT = 0** — reachability calculée par parcours en profondeur depuis `index.html` de chaque site en suivant tous les liens internes `.html` : les 67 pages publiques et les 146 pages privées sont toutes atteignables depuis leur portail respectif.

## 2. Fil d'Ariane et boutons

- Fil d'Ariane (`nav.breadcrumbs`) présent sur les 213 pages générées (vérifié via le landmark `nav`).
- Bouton retour au niveau et bouton Imprimer présents sur toutes les pages (template unique `page_shell`), donc homogènes par construction — pas de vérification page par page nécessaire au-delà du gabarit.
- Lien PDF (« Télécharger le PDF ») : présent sur chaque page document (`pdf_href` toujours renseigné dans `write_document_html`), pointant vers `dist/pdf/...`. Les fichiers PDF cibles existent bien (contrôle croisé avec `dist/pdf`, 216 PDF générés — 0 cible manquante détectée dans les liens PDF).

## 3. Clics pour atteindre un document (audit UX statique)

Racine (`dist/site-public/index.html`) → carte de niveau (1 clic) → page de niveau (`{niveau}/index.html`) → séance repérée par sa carte, action « Élève »/« Supports » (1 clic) → document HTML. **3 clics maximum** pour un document public, conforme à l'exigence de la section 12.2. Pour un document confidentiel (Professeur/Aides), l'utilisateur doit en plus ouvrir la zone privée (bouton « Ouvrir le dossier confidentiel » sur la racine) — 1 clic supplémentaire, ce qui reste raisonnable et volontaire (avertissement de confidentialité affiché avant l'accès).

Voir aussi `reports/UX_AUDIT.md` pour le détail des dimensions responsive/clavier/zoom (limites de l'audit statique).

## Résumé des compteurs (ce rapport)

```text
BROKEN_LINK_COUNT=42
ORPHAN_ACTIVE_FILE_COUNT=0
EXTERNAL_RESOURCE_COUNT=0
```
