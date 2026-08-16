# Stages de pré-rentrée Mathématiques 2026-2027

Ce paquet local rassemble les stages d’entrée en `4e`, `3e`, `2nde` et `1ere_spe`. Il génère un portail hors ligne, des PDF A4 et des packs d’impression à partir des Markdown opérationnels.

## Démarrer

```bash
make all
make serve
```

Ouvrez ensuite `http://localhost:8000`. Le portail public est dans `dist/site-public/`; le portail confidentiel est dans `dist/site-private/` et ne doit pas être diffusé.

## Source et confidentialité

- `05_SOURCES/` contient les programmes canoniques : le build ne les modifie pas.
- `04_NOMINATIFS/` et `dist/site-private/` contiennent des données de mineurs : circulation locale strictement limitée.
- Les PDF sources initiaux sont préservés et exclus des packs générés.

Voir `QUICK_START.md` et `PRINT_GUIDE.md` pour les usages courants.
