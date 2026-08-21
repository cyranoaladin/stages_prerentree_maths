# Dossier enseignant — Fares LAAJILI (Entrée en Troisième, Mathématiques)

**Confidentiel.** Ce répertoire contient les seuls fichiers de la séance S5 qui
révèlent une réponse attendue :

| Fichier | Contenu |
|---|---|
| `S5_ENSEIGNANT_*.tex` / `.pdf` | profil, déroulé minute par minute, corrigés, barème, clés d'interprétation |
| `evaluation_manifest.json` | métadonnées complètes des 12 items, dont la réponse attendue |
| `answer_key.json` | corrigé structuré et critères de correction |

Les documents remis à l'élève se trouvent dans le répertoire parent et ne
contiennent ni corrigé, ni barème, ni code d'erreur.

## Après la passation

1. Saisir les points dans `../responses_TEMPLATE.json` (copie renommée, par exemple
   `responses_2026-08-28.json`).
2. Lancer :

   ```
   python3 S5_cloture/tools/analyze_s5.py --student fares-laajili --responses <fichier>
   ```

3. Le script produit `post_stage_analysis.json` conforme à
   `../post_stage_analysis_schema.json`. Toute affirmation chiffrée du bilan doit
   provenir de ce fichier.
