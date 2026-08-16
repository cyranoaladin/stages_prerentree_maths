# Audit UI/UX — 2026-08-16

Méthode : audit statique (structure HTML/CSS générée, `assets/site.css`, `assets/print.css`) — aucun navigateur piloté n'était disponible (ni Playwright ni Puppeteer installés localement, vérifié par `python3 -c "import playwright"` → `ModuleNotFoundError`). Les points nécessitant un rendu réel (comportement effectif à 320 px, zoom 200 %, focus visuel) sont donc évalués sur le CSS source et marqués comme tels, pas comme « testés en conditions réelles ». Sévérité : P0 bloquant, P1 majeur, P2 mineur, P3 cosmétique.

## Navigation

- Racine → niveau → séance → document : **3 clics**, conforme (section 12.2). Voir `reports/NAVIGATION_QA.md`.
- Retour à la racine et au niveau : liens statiques présents sur chaque page (`page_shell`, breadcrumb + brand). **Conforme.**
- 40 liens de navigation vers la zone privée sont cassés (défaut de comptage de niveaux de répertoire) — voir `reports/NAVIGATION_QA.md`. **P0** : rend inaccessible depuis le portail public la bascule annoncée vers les fiches professeur/aides d'une séance donnée (l'utilisateur atterrit sur une erreur 404 `file://`).
- Recherche locale : un champ `#search` et un index JS embarqué (`assets/search-index.js`, données inline, aucun `fetch`) sont présents sur les deux portails. Fonctionne en `file://` par construction (pas de requête réseau). **Conforme** aux exigences de la section 7.5. Non testé en interaction réelle (pas de navigateur piloté) — le code JS (`assets/site.js`) n'a pas été exécuté, seule sa présence et son chargement local ont été vérifiés statiquement. **P2** : à confirmer par un test manuel dans un navigateur avant mise en production.
- Filtres par niveau/séance/audience/type : la page d'accueil ne propose que la recherche texte libre ; aucun contrôle de filtre dédié (case à cocher / select) n'est généré par `tools/build.py::portal_page`. **P1** : la section 7.2 exige explicitement des « filtres par niveau, séance, audience et type » en plus de la recherche — actuellement absent, à ajouter dans `portal_page()`.

## Zones public/privé

- Séparation strictement respectée : 0 fuite de nom d'élève dans `dist/site-public` ni dans `MANIFEST_PUBLIC.csv` (contrôle exhaustif par grep des 11 noms sur les 67 pages publiques). **Conforme.**
- Bandeau de confidentialité visible sur chaque page confidentielle (`<p class="notice confidential">CONFIDENTIEL — diffusion strictement limitée.</p>`), badge `PRIVÉ` dans l'en-tête de la zone privée. **Conforme** à la section 5.4/7.3.

## Responsive et zoom (limites de l'audit statique)

- `assets/site.css` n'a pas été lu dans le détail par ce script (hors périmètre lien/orphelins/dédoublonnage) : la présence de règles `@media` responsive et d'un `prefers-reduced-motion` n'est vérifiée qu'au niveau de l'existence du fichier et de son chargement local, pas de son contenu exhaustif. **À valider par l'agent UI/UX dédié ou par un test manuel** (redimensionnement navigateur à 320 px et 390 px, zoom 200 %) avant de considérer ce point comme un gate vert. Marqué **non testé en conditions réelles**, pas « conforme ».
- Comportement `file://` : les 213 pages HTML utilisent exclusivement des chemins relatifs (0 ressource externe, 0 appel réseau détecté), ce qui est nécessaire mais pas suffisant pour garantir un fonctionnement parfait en `file://` (certains navigateurs restreignent XHR/`fetch` même relatif en `file://` — ici non utilisé, donc pas de risque identifié). **Conforme sous réserve.**

## Clavier

- Lien d'évitement (« Aller au contenu principal ») présent sur les 213 pages. **Conforme.**
- Aucun `tabindex` positif détecté (piège clavier potentiel) sur l'ensemble du corpus. **Conforme.**
- Focus visible : dépend des règles CSS `:focus-visible` dans `assets/site.css`, non auditées en détail ici (voir remarque responsive ci-dessus). **Non testé en conditions réelles.**

## Cohérence des titres et densité

- Chaque page a un `<title>` unique et un unique `<h1>` correspondant au titre du document. **Conforme.**
- 21 pages sur 213 présentent un saut de niveau de titre (h2 → h4 sans h3, ou pire un h2 fantôme généré par une formule LaTeX mal délimitée qui casse le parsing Markdown) — voir détail dans `reports/ACCESSIBILITY_QA.md` et le constat transverse de `reports/NAVIGATION_QA.md`. **P1/P0** selon les cas.

## Synthèse des défauts par sévérité

| Sévérité | Défaut | Occurrences |
|---|---|---|
| P0 | Liens navigation zone privée cassés (`tools/build.py:256`) | 40 liens / 4 pages |
| P0 | Formules LaTeX mal délimitées cassant le rendu Markdown (contenu visible corrompu) | ≥23 documents sources |
| P1 | Filtres niveau/séance/audience/type absents de la page d'accueil | 2 portails (public+privé) |
| P1 | Sauts de niveaux de titre restants (hors cas P0 ci-dessus) | ~18 pages |
| P2 | Recherche et responsive non testés en navigateur réel (Playwright absent) | — |
| P3 | Lien vers `FINAL_DELIVERY_REPORT.md` avant génération de ce rapport | 2 occurrences, se résout à la prochaine build |

Aucun défaut P0/P1 de cette liste n'a été corrigé par ce script — conformément à la consigne, seul le diagnostic est livré ici ; les correctifs de `tools/build.py` et de `portal_page()` restent à appliquer de façon centralisée.
