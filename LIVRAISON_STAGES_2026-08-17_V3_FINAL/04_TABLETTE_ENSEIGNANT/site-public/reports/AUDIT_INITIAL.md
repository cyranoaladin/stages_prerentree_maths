# Audit initial — 2026-08-16

## Périmètre et gel

- Racine auditée : `Nexus_Reussite_Documentation_Stages_Maths_2026`.
- Dépôt Git parent : `Nexus_Reussite`, initialement sur `master` et déjà sale hors du paquet.
- Branche locale créée : `refactor/documentation-stages-maths-2026` ; aucun envoi distant n'est autorisé ni effectué.
- Le sous-paquet `1re_nsi/` est hors périmètre de la mission mathématiques et n'est pas modifié.

## Comptage initial des quatre niveaux mathématiques

| Niveau | Markdown | HTML | PDF source | Fichiers |
|---|---:|---:|---:|---:|
| 4e | 34 | 34 | 5 | 73 |
| 3e | 38 | 38 | 9 | 85 |
| 2nde | 34 | 34 | 5 | 73 |
| 1ere_spe | 36 | 36 | 7 | 79 |
| Total | 142 | 142 | 26 | 310 |

- Taille des quatre niveaux : 32 086 239 octets.
- Documents/fichiers nominatifs : 66.
- Fichiers vides : 0.
- Doublons exacts actifs : 0.
- Liens relatifs HTML vérifiés : 186 ; liens cassés : 0.
- Erreurs structurelles HTML : 142 (toutes les pages : attribut `lang` absent et nombre de `h1` non normalisé).

## Défauts reproduits

1. Les index sont écrits à la main et exposent directement les dossiers nominatifs.
2. Les HTML existants sont des exportations Pandoc brutes, sans portail, breadcrumbs, recherche, filtre, séparation public/privé ni accessibilité homogène.
3. La chaîne de build ne génère que du HTML, sans PDF opérationnels, packs, manifests séparés, QA ni reproductibilité contrôlée.
4. Les fiches professeur décrivent toutes des créneaux se terminant à 120 minutes ; le contrôle automatique doit néanmoins calculer les intervalles plutôt que sommer les heures de fin.
5. Les supports SVG locaux existent, mais leur référencement et l'impression doivent être contrôlés dans les sorties finales.

## Outillage disponible

- Python 3.12.3, Pandoc, Google Chrome, WeasyPrint 68.1, XeLaTeX, qpdf, pdfinfo, pdftotext, pdffonts, pdftoppm et mutool.
- Modules Python détectés : WeasyPrint, pypdf 6.11.0, SymPy 1.14.0 et pytest 9.0.2.
