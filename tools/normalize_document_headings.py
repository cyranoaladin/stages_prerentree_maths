#!/usr/bin/env python3
"""Script de normalisation canonique des titres Markdown H1 pour Nexus Réussite."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEVEL_LABELS = {
    "4e": "4e",
    "3e": "3e",
    "2nde": "2nde",
    "1ere_spe": "1re Spécialité Mathématiques",
    "1re_nsi": "1re NSI",
}

TYPE_LABELS = {
    "ELEVE_ACTIVITE": "Activité élève",
    "PROF_FICHE": "Fiche enseignant",
    "SUPPORTS_MANIPULATION": "Supports de manipulation",
    "SUPPORTS_PRATIQUES": "Supports pratiques",
    "AIDES_CARTES": "Cartes d’aide",
}


SESSION_THEMES = {
    "4e": {
        "1": "Calculer avec du sens",
        "2": "Mesurer une surface ou un contour",
        "3": "Donner du sens aux lettres",
        "4": "Voir, raisonner, démontrer",
        "5": "Réinvestir, mesurer les progrès et préparer septembre",
    },
    "3e": {
        "1": "Sécuriser le moteur numérique",
        "2": "Passer du calcul à l’algèbre",
        "3": "Construire et justifier",
        "4": "Choisir un rapport trigonométrique",
        "5": "Lire les données et mobiliser l’ensemble des acquis",
    },
    "2nde": {
        "1": "Réparer le moteur de calcul",
        "2": "Construire l’algèbre du lycée",
        "3": "Modéliser une situation",
        "4": "Choisir le bon théorème",
        "5": "Relier, contrôler et expliquer",
    },
    "1ere_spe": {
        "1": "Calcul algébrique, inéquations et transition vers le second degré",
        "2": "Fonctions, fonctions de référence et première approche de la dérivation",
        "3": "Vecteurs, droites et transition vers le produit scalaire",
        "4": "Pourcentages, événements et probabilités conditionnelles",
        "5": "Suites numériques, Python et évaluation de synthèse",
    },
    "1re_nsi": {
        "1": "Variables, types, booléens et conditions",
        "2": "Boucles, compteurs et accumulateurs",
        "3": "Fonctions, contrats, tests et débogage",
        "4": "Listes, tuples, dictionnaires et tables CSV",
        "5": "Algorithmes et mini-projet de synthèse",
    },
}


def normalize_file(path: Path) -> bool:
    if any(x in path.parts for x in ("_archive", ".pytest_cache", "reports", "docs", "05_SOURCES", "07_SOURCES", "tmp", "dist")):
        return False

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        return False

    level_key = next((k for k in LEVEL_LABELS if k in path.parts), "")
    level_str = LEVEL_LABELS.get(level_key, "")
    stem = path.stem

    # 1. Traitement des MASTER_Documentation_Stage
    if "MASTER_Documentation_Stage" in stem:
        new_lines = [f"# Document maître — {level_str}", ""]
        for line in lines[1:]:
            if line.startswith("# "):
                raw = line[2:].strip()
                if "Guide_Formateur" in raw:
                    new_lines.append("## Guide du formateur")
                elif "Tableau_Bord" in raw:
                    new_lines.append("## Tableau de bord enseignant")
                elif "_S" in raw:
                    match = re.search(r'S(\d+)_([A-Z_]+)', raw)
                    if match:
                        s_num, t_key = match.group(1), match.group(2)
                        t_label = TYPE_LABELS.get(t_key.upper(), t_key.replace("_", " "))
                        theme = SESSION_THEMES.get(level_key, {}).get(s_num, "")
                        suffix = f" : {theme}" if theme else ""
                        new_lines.append(f"## Séance {s_num} — {t_label}{suffix}")
                    else:
                        new_lines.append(f"## {raw.replace('_', ' ')}")
                elif "Diagnostic" in raw:
                    new_lines.append("## Diagnostic initial")
                elif "Evaluation" in raw:
                    new_lines.append("## Évaluation finale")
                elif "Portfolio" in raw:
                    new_lines.append("## Portfolio individuel")
                else:
                    new_lines.append(f"## {raw}")
            else:
                new_lines.append(line)
        new_text = "\n".join(new_lines) + "\n"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            return True
        return False

    # 2. Traitement des fichiers avec frontmatter (ex: 1re NSI)
    if lines[0] == "---":
        end_fm = -1
        for i in range(1, len(lines)):
            if lines[i] == "---":
                end_fm = i
                break
        if end_fm != -1:
            title_val = ""
            for i in range(1, end_fm):
                if lines[i].startswith("title:"):
                    title_val = lines[i].split(":", 1)[1].strip().strip('"').strip("'")
            
            new_lines = lines[:end_fm+1]
            for i in range(end_fm+1, len(lines)):
                line = lines[i]
                if line.startswith("# "):
                    new_lines.append("#" + line)
                else:
                    new_lines.append(line)
            new_text = "\n".join(new_lines) + "\n"
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                return True
            return False

    # 3. Documents de séances S1..S5
    session_match = re.search(r'S(\d+)_([A-Z_]+)', stem)
    if session_match:
        s_num = session_match.group(1)
        t_key = session_match.group(2)
        t_label = TYPE_LABELS.get(t_key.upper(), t_key.replace("_", " "))
        theme = SESSION_THEMES.get(level_key, {}).get(s_num, "")
        
        h1 = f"# {level_str} — Séance {s_num} : {theme}"
        h2 = f"## {t_label}"

        new_lines = [h1, h2]
        # Conserver les lignes suivantes en rétrogradant tout autre # en ##
        for line in lines[2:]:
            if line.startswith("# "):
                new_lines.append("#" + line)
            else:
                new_lines.append(line)

        new_text = "\n".join(new_lines) + "\n"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            return True
        return False

    # 4. Autres documents opérationnels (Guides, Evaluatons, Diagnostics, Nominatifs)
    h1 = ""
    h2 = ""
    if "Guide_Formateur" in stem:
        h1 = f"# {level_str} — Guide du formateur"
        h2 = "## Protocole d’animation et repères pédagogiques"
    elif "Tableau_Bord_Enseignant" in stem:
        h1 = f"# {level_str} — Tableau de bord enseignant"
        h2 = "## Suivi collectif des compétences"
    elif "Mini_Diagnostic_ELEVE" in stem:
        h1 = f"# {level_str} — Diagnostic initial (Élève)"
        h2 = "## Test de positionnement"
    elif "Mini_Diagnostic_PROF_Corrige" in stem:
        h1 = f"# {level_str} — Diagnostic initial (Corrigé enseignant)"
        h2 = "## Corrigé et conseils d’exploitation"
    elif "Evaluation_Finale_ELEVE" in stem:
        h1 = f"# {level_str} — Évaluation finale (Élève)"
        h2 = "## Sujet de synthèse"
    elif "Evaluation_Finale_PROF_Corrige" in stem:
        h1 = f"# {level_str} — Évaluation finale (Corrigé & Barème)"
        h2 = "## Corrigé et barème d’évaluation"
    elif "Portfolio_Individuel" in stem:
        h1 = f"# {level_str} — Portfolio individuel de suivi"
        h2 = "## Grille d’auto-évaluation"
    elif "Dossier_Individuel_" in stem:
        name_part = stem.replace(f"{level_key}_Dossier_Individuel_", "").replace("_", " ")
        h1 = f"# {level_str} — Dossier individuel — {name_part}"
        h2 = "## Synthèse et profil élève"
    elif "Remediation_Ciblee_" in stem:
        is_prof = "PROF_Corrige" in stem
        clean_name = stem.replace(f"{level_key}_Remediation_Ciblee_", "").replace("_ELEVE", "").replace("_PROF_Corrige", "").replace("_", " ")
        audience_label = "Corrigé enseignant" if is_prof else "Élève"
        h1 = f"# {level_str} — Plan de remédiation ciblée — {clean_name} ({audience_label})"
        h2 = "## Parcours personnalisé"
    elif stem == "index":
        h1 = f"# Index — {level_str}"
        h2 = "## Documents du niveau"

    if h1:
        new_lines = [h1, h2]
        for line in lines[2:]:
            if line.startswith("# "):
                new_lines.append("#" + line)
            else:
                new_lines.append(line)
        new_text = "\n".join(new_lines) + "\n"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            return True

    return False


def main():
    count = 0
    for level in ("4e", "3e", "2nde", "1ere_spe", "1re_nsi"):
        base = ROOT / level
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.md")):
            if normalize_file(p):
                count += 1
                print(f"Modifié: {p.relative_to(ROOT)}")
    print(f"\nTerminé: {count} fichiers Markdown normalisés.")

if __name__ == "__main__":
    main()
