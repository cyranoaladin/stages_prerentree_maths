# -*- coding: utf-8 -*-
"""Étape 1 à 4 de la mission : inventaire, audit S1-S4 et registre des conflits.

Produit :
    S5_cloture/_audit/inventaire_eleves.json
    S5_cloture/_audit/AUDIT_S1_S4.md
    S5_cloture/_audit/conflits_sources.json

Le script ne rédige aucun livret : il ne fait que consigner ce qui a été trouvé.
"""

import json
import os
import sys
sys.dont_write_bytecode = True  # aucune trace de cache dans la livraison

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
from data.levels import LEVELS, LEVEL_ORDER

AUDIT_DIR = os.path.join(core.S5_ROOT, "_audit")
GENERATED_ON = "2026-08-20"

CONFLITS = [
    {
        "id": "CONF-01",
        "objet": "Architecture temporelle de la séance 5",
        "information_a": {
            "contenu": "La fiche professeur de la séance 5 de chaque niveau prévoit 30 minutes d'évaluation finale (16 items) à l'intérieur des 120 minutes, suivies d'une auto-correction guidée.",
            "source": "<niveau>/02_SEANCES/S5/<niveau>_S5_PROF_Fiche.md",
        },
        "information_b": {
            "contenu": "Le cahier des charges de la présente mission impose 1 h 15 de travail pédagogique puis 45 minutes d'évaluation finale individuelle, dans deux documents séparés.",
            "source": "Instruction de mission du 20 août 2026.",
        },
        "decision": "Appliquer 75 min + 45 min dans S5_cloture. Les fiches S5 existantes ne sont pas modifiées.",
        "justification": "Instruction la plus récente et la plus spécifique (hiérarchie des sources, §4 du cahier des charges). La séance de niveau reste utilisable telle quelle pour un groupe ; S5_cloture fournit la version individualisée et instrumentée.",
        "impact": "Le déroulé minute par minute des dossiers enseignants de S5_cloture diffère de celui des fiches PROF de niveau.",
    },
    {
        "id": "CONF-02",
        "objet": "Évaluation finale de niveau contre évaluation finale individualisée",
        "information_a": {
            "contenu": "Une évaluation finale commune existe déjà par niveau : 16 items identiques pour tous les élèves du niveau, sans barème sur 20 explicite dans la version élève.",
            "source": "<niveau>/03_EVALUATIONS/<niveau>_Evaluation_Finale_ELEVE.md",
        },
        "information_b": {
            "contenu": "Le cahier des charges impose un noyau commun d'environ 70 % et environ 30 % d'items individualisés, avec double lecture note sur 20 et maîtrise par compétence.",
            "source": "Instruction de mission, §8, §9 et §12.",
        },
        "decision": "Produire dans S5_cloture une évaluation distincte de 12 items (14 points communs, 6 points individualisés, total 20), sans toucher à l'évaluation finale de niveau.",
        "justification": "Les deux instruments ont des fonctions différentes : l'un est sommatif et collectif, l'autre est un diagnostic de sortie exploitable élève par élève. Conserver les deux évite toute perte d'information.",
        "impact": "Deux évaluations coexistent pour un même niveau. L'INDEX précise laquelle relève de la clôture S5.",
    },
    {
        "id": "CONF-03",
        "objet": "Livrets S4/S5 personnalisés déjà produits pour trois élèves de Quatrième",
        "information_a": {
            "contenu": "Des livrets personnalisés S4 et S5 existent en PDF pour Ines Kefi, Sinda Chikhaoui et Fares Darghouth. Leur architecture intègre le bilan de fin de stage à l'intérieur du livret élève et n'applique pas le découpage 75/45.",
            "source": "Bilans/4e_Ines_Kefi_LIVRETS_S4_S5_PERSONNALISES.pdf ; Bilans/4e_Sinda_Chikhaoui_LIVRETS_S4_S5_PERSONNALISES.pdf ; Nexus_4e_Fares_Darghouth_S4_S5_PDF/4e_S5_Fares_Darghouth_DOSSIER_ELEVE_PERSONNALISE.pdf",
        },
        "information_b": {
            "contenu": "Le cahier des charges exige un livret de travail sans corrigé et une évaluation dans un document séparé, afin que l'élève ne voie pas l'évaluation pendant la phase de consolidation.",
            "source": "Instruction de mission, §16 et §17.",
        },
        "decision": "Ne rien écraser. Produire la version conforme dans S5_cloture, et relever les énoncés déjà utilisés dans ces livrets afin de ne pas les reprendre.",
        "justification": "Les documents existants sont des sources ; les écraser détruirait la traçabilité. Le contenu des trois livrets a été extrait et confronté aux items produits (§39 : pas de répétition exacte).",
        "impact": "Ces trois élèves disposeront de deux versions de S5. L'INDEX et le QA_REPORT signalent laquelle est conforme au présent cahier des charges.",
    },
    {
        "id": "CONF-04",
        "objet": "Périmètre : le registre content/students.json ne couvre pas la NSI",
        "information_a": {
            "contenu": "content/students.json recense 13 élèves, tous en mathématiques.",
            "source": "content/students.json",
        },
        "information_b": {
            "contenu": "Deux dossiers individuels complets existent pour le stage de Première NSI (Ahmad BELDI, Ahmed BENHADJ SALEM), avec diagnostic, remédiation et séances S1 à S5.",
            "source": "1re_nsi/05_NOMINATIFS/",
        },
        "decision": "Le périmètre S5 retenu est de 15 couples élève × matière : les 13 élèves de mathématiques et les 2 élèves de NSI.",
        "justification": "Hiérarchie des sources : le dossier individuel nominatif prime sur un registre général. Aucun élève n'est inventé ; les deux élèves de NSI sont attestés par leurs dossiers.",
        "impact": "Ahmad BELDI apparaît deux fois, avec deux dossiers S5 distincts (mathématiques et NSI).",
    },
    {
        "id": "CONF-05",
        "objet": "Deux positionnements pour Ahmed BENHADJ SALEM",
        "information_a": {
            "contenu": "Positionnement de niveau Première NSI : 18 questions traitées sur 18, programmation à 55,6 %.",
            "source": "1re_nsi/05_NOMINATIFS/Ahmed_BENHADJ_SALEM/SOURCE_Bilan_Eleve_Ahmed_BENHADJ_SALEM_Premiere_NSI.pdf",
        },
        "information_b": {
            "contenu": "Positionnement de niveau Terminale NSI : six domaines solides sur sept, avec la même erreur d'accumulateur.",
            "source": "1re_nsi/05_NOMINATIFS/Ahmed_BENHADJ_SALEM/SOURCE_Bilan_Eleve_Ahmed_BENHADJ_SALEM_Terminale_NSI.pdf",
        },
        "decision": "Retenir le positionnement Première comme référence de comparaison initiale ; utiliser le positionnement Terminale uniquement comme confirmation de l'erreur d'accumulateur.",
        "justification": "Le stage suivi est « Entrée en Première NSI ». Comparer un post-test de fin de stage à un positionnement de niveau Terminale n'aurait aucune validité.",
        "impact": "Les deltas de maîtrise ne seront calculés que sur les items du positionnement Première.",
    },
    {
        "id": "CONF-06",
        "objet": "Un bilan de Français existe pour Elyes Kefi, sans stage de Français dans le dépôt",
        "information_a": {
            "contenu": "Bilans/bilan-nexus-parents_elyes_kefi_francais.pdf est un compte rendu de positionnement en Français (cinq domaines, un à consolider, un à installer, trois à rectifier).",
            "source": "Bilans/bilan-nexus-parents_elyes_kefi_francais.pdf",
        },
        "information_b": {
            "contenu": "Le dossier nominatif de l'élève ne contient qu'un parcours de mathématiques ; aucun répertoire de stage de Français n'existe dans le dépôt.",
            "source": "3e/04_NOMINATIFS/Elyes_Kefi/",
        },
        "decision": "Hors périmètre S5. Aucun dossier S5 de Français n'est produit ; l'élément est signalé pour validation humaine.",
        "justification": "Il n'existe ni séances S1 à S4 ni objectifs de niveau en Français : produire une S5 reviendrait à fabriquer une trajectoire inexistante (§2 du cahier des charges).",
        "impact": "À vérifier avec l'équipe : s'agit-il d'un stage de Français réellement suivi ? Le cas échéant, une mission distincte est nécessaire.",
    },
    {
        "id": "CONF-07",
        "objet": "Dossier Sarra ESSANAA présent dans le répertoire",
        "information_a": {
            "contenu": "Quatre documents concernent Sarra ESSANAA : audit réglementaire, diagnostic 2 h, dossier Bac 2027 et note d'accompagnement.",
            "source": "Nexus_Reussite_Dossier_Sarra_ESSANAA_2027_AUDITE/",
        },
        "information_b": {
            "contenu": "Ces documents relèvent de la « Cellule Candidat Libre » et portent sur une inscription au baccalauréat 2027 ; ils ne comportent ni diagnostic de pré-rentrée au format du stage, ni séances S1 à S4.",
            "source": "Nexus_Reussite_Dossier_Sarra_ESSANAA_2027_AUDITE/Audit_Nexus_Reussite_Sarra_ESSANAA_2027.pdf",
        },
        "decision": "Hors périmètre. Aucune séance S5 n'est produite pour cette personne.",
        "justification": "Il ne s'agit pas d'un stage de pré-rentrée à cinq séances. Produire une S5 supposerait de fabriquer un diagnostic et une trajectoire inexistants.",
        "impact": "Aucun. Consigné pour mémoire.",
    },
    {
        "id": "CONF-08",
        "objet": "Absence de dossiers personnalisés S2 à S5 en Première spécialité",
        "information_a": {
            "contenu": "Les niveaux 4e, 3e, 2nde et 1re NSI disposent de dossiers élèves personnalisés pour S2, S3 et S4.",
            "source": "Nexus_*_S2_*/, Nexus_*_S3_*/, Bilans/",
        },
        "information_b": {
            "contenu": "Aucun document personnalisé S2 à S5 n'existe pour Ahmad Beldi, Donia Khadhrani et Malek Khadhrani en Première spécialité.",
            "source": "1ere_spe/04_NOMINATIFS/",
        },
        "decision": "Reconstruire la trajectoire de ces trois élèves à partir des séances de niveau et du plan de remédiation individuel uniquement, et le signaler explicitement dans chaque dossier enseignant.",
        "justification": "Ne pas supposer l'existence d'un document absent (§2). La personnalisation de la S5 repose donc sur le diagnostic initial et la remédiation, sans preuve intermédiaire.",
        "impact": "Pour ces trois élèves, la reconstruction de trajectoire est moins étayée que pour les douze autres.",
    },
    {
        "id": "CONF-09",
        "objet": "Absence de preuve documentée entre le diagnostic initial et la séance 5",
        "information_a": {
            "contenu": "Les dossiers individuels prévoient un tableau d'observation par séance (procédure choisie, exactitude, justification, contrôle, certitude) et une case « preuve recueillie ».",
            "source": "<niveau>/04_NOMINATIFS/<élève>/<niveau>_Dossier_Individuel_<élève>.md",
        },
        "information_b": {
            "contenu": "Ces tableaux sont vierges dans tous les dossiers consultés : aucune observation de séance n'a été saisie.",
            "source": "Inspection des 15 dossiers individuels, 20 août 2026.",
        },
        "decision": "Le statut de chaque compétence avant la S5 est fondé sur le seul diagnostic initial, avec la mention explicite « preuve postérieure non documentée ».",
        "justification": "§28 du cahier des charges : ne jamais confondre travaillé et acquis, ni affirmer une progression non attestée.",
        "impact": "Aucun delta ne peut être calculé avant la passation de l'évaluation finale. Les dossiers enseignants portent cette mention.",
    },
    {
        "id": "CONF-10",
        "objet": "Casse des noms d'élèves",
        "information_a": {
            "contenu": "content/students.json écrit « Ines KEFI », « Elyes KEFI », mais « Ahmad Beldi », « Sinda Chikhaoui ».",
            "source": "content/students.json",
        },
        "information_b": {
            "contenu": "Les dossiers individuels les plus récents emploient la forme « Ines KEFI » et « Elyes KEFI » ; les autres dossiers emploient la casse ordinaire.",
            "source": "<niveau>/04_NOMINATIFS/",
        },
        "decision": "Uniformiser dans S5_cloture : prénom en casse ordinaire, nom de famille en capitales, pour les quinze dossiers.",
        "justification": "Homogénéité de forme exigée au §41. Les identifiants stables restent ceux de content/students.json lorsqu'ils existent.",
        "impact": "Les noms de répertoires de S5_cloture diffèrent de ceux des répertoires historiques ; la correspondance est donnée dans l'inventaire.",
    },
]


def build_inventaire():
    entries = []
    for st in core.all_students():
        level = core.level_of(st)
        srcs = core.student_sources(st)
        rows = core.skill_table(st)
        entries.append({
            "student_id": st["id"],
            "nom_affiche": st["name"],
            "repertoire_s5": os.path.relpath(core.student_output_dir(st), core.REPO_ROOT),
            "repertoire_source": os.path.dirname(srcs[0]),
            "niveau_entree": level["label"],
            "niveau_cle": level["key"],
            "matiere": level["subject"],
            "annee_n_moins_1": level["year_prev"],
            "annee_n": level["year_next"],
            "parcours": st.get("parcours"),
            "diagnostic_initial": {
                "disponible": st["baseline"]["available"],
                "instrument": level["baseline_instrument"]["name"],
                "fichier": level["baseline_instrument"]["file"],
                "items_traites": st["baseline"]["items"],
                "date_bilan": st["baseline"]["date"],
                "calibration_reussite_confiance": st["baseline"]["calibration"],
                "synthese": st["baseline"]["summary"],
            },
            "points_forts_identifies": st["baseline"]["appuis"],
            "difficultes_identifiees": st["baseline"]["priorites"],
            "observations_par_domaine": [
                {"domaine": d, "statut": s, "observation": o}
                for (d, s, o) in st["baseline"]["observations"]
            ],
            "competences_evaluees_initialement": sorted(
                {sid for sid, sk in level["skills"].items() if sk["baseline_items"]}),
            "competences_sans_item_initial": sorted(
                {sid for sid, sk in level["skills"].items() if not sk["baseline_items"]}),
            "contenus_seances": {
                "S1": level["sessions"]["S1"], "S2": level["sessions"]["S2"],
                "S3": level["sessions"]["S3"], "S4": level["sessions"]["S4"],
                "S5_niveau": level["sessions"]["S5"],
            },
            "documents_personnalises_disponibles": [
                s for s in st.get("extra_sources", []) if core.source_exists(s)],
            "documents_personnalises_absents": [
                s for s in st.get("extra_sources", []) if not core.source_exists(s)],
            "remediation_individuelle": [s for s in srcs if "Remediation" in s],
            "sources": [{"chemin": s, "existe": core.source_exists(s)} for s in srcs],
            "progression_objectivable": "aucune : les tableaux d'observation S1 à S5 du dossier individuel sont vierges",
            "elements_non_documentes": sorted(
                {r["skill_id"] for r in rows if r["statut_avant_s5"] in ("non_evalue", "non_travaille")}),
            "priorites_s5": {"P1": st["p1"], "P2": st["p2"]},
            "objectif_s5": st["objectif"],
            "statut_competences_avant_s5": rows,
        })
    return {
        "schema": "nexus-s5-inventaire-v1",
        "genere_le": GENERATED_ON,
        "perimetre": "Séance 5 de clôture — stages de pré-rentrée Nexus Réussite 2026-2027",
        "nb_couples_eleve_matiere": len(entries),
        "niveaux": [{"cle": k, "libelle": LEVELS[k]["label"], "matiere": LEVELS[k]["subject"]}
                    for k in LEVEL_ORDER],
        "hors_perimetre": [
            {"objet": "Sarra ESSANAA (dossier Bac 2027, Cellule Candidat Libre)",
             "motif": "aucun diagnostic de stage ni séances S1 à S4 ; ne relève pas d'un stage de pré-rentrée à cinq séances"},
            {"objet": "Bilan de positionnement en Français d'Elyes Kefi",
             "motif": "aucun stage de Français n'existe dans le dépôt : aucune trajectoire S1 à S4 à prolonger"},
        ],
        "eleves": entries,
    }


AUDIT_HEADER = """# Audit du stage — du diagnostic initial à la séance 4

> Document de travail produit avant toute rédaction de livret, conformément au §2 du
> cahier des charges. Il consigne ce qui a été trouvé dans le dépôt, et uniquement cela.

**Date de l'audit :** {date}
**Périmètre :** {n} couples élève × matière, {nl} niveaux, 2 matières.

---

## 1. Ce que contient réellement le dépôt

| Élément | Constat |
|---|---|
| Répertoires de stage | `4e`, `3e`, `2nde`, `1ere_spe` (mathématiques) et `1re_nsi` (NSI) |
| Structure par niveau | `00_MASTER`, `01_ENSEIGNANT`, `02_SEANCES/S1..S5`, `03_EVALUATIONS`, `04_NOMINATIFS` (ou `05_NOMINATIFS` en NSI), `05_SOURCES` |
| Diagnostic initial | un test de positionnement par niveau, 18 items QCM, 25 minutes, certitude 1 à 4 |
| Documents par séance | fiche élève, fiche professeur, cartes d'aide, supports de manipulation |
| Dossiers nominatifs | dossier individuel, plan de remédiation ciblée élève et professeur, bilans élève et parents |
| Format de production historique | Markdown → HTML → PDF (`tools/build.py`), avec `assets/print.css` |
| Format LaTeX le plus récent | `Bilans/1re_NSI_S4_Ahmad_BELDI_DOSSIER_ELEVE_PERSONNALISE.tex` |
| Données structurées existantes | `content/students.json`, `content/catalog.json`, `reports/AUDIT_INITIAL.json`, `reports/QA_STATUS.json` |

**Charte graphique retenue.** Aucune identité nouvelle n'a été créée. Le fichier
`S5_cloture/_common/nexusS5.sty` reprend, sans modification, les couleurs, les encadrés,
les titres et les réglages typographiques du seul fichier LaTeX du dépôt, qui est aussi
le plus récent.

---

## 2. Ce qui manque

1. **Aucune observation de séance n'a été saisie.** Les dossiers individuels prévoient,
   pour chacune des cinq séances, un tableau « procédure choisie / exactitude /
   justification / contrôle / certitude » ainsi qu'une colonne « preuve recueillie ».
   Ces tableaux sont vierges dans les quinze dossiers. Il n'existe donc **aucune preuve
   documentée postérieure au diagnostic initial**.
2. **Aucun dossier personnalisé S2 à S5 en Première spécialité.** Les quatre autres
   niveaux disposent de livrets élèves individualisés pour S2, S3 et S4 ; la Première
   spécialité n'en a aucun.
3. **Aucun corrigé nominatif renseigné.** Les plans de remédiation professeur existent,
   mais aucune production d'élève corrigée n'est archivée.
4. **Aucun résultat item par item du diagnostic initial.** Les dossiers restituent des
   statuts par domaine et des observations qualitatives, non les réponses aux 18 items.
   La comparaison initial/final sera donc conduite **au niveau de la compétence**, non
   au niveau de la réponse.

Ces quatre lacunes déterminent une règle appliquée partout dans `S5_cloture` : le statut
d'une compétence avant la séance 5 est qualifié à partir du diagnostic initial, jamais
à partir d'une acquisition supposée pendant les séances.

---

## 3. Trajectoire de niveau reconstruite

"""


def build_audit_md(inv):
    parts = [AUDIT_HEADER.format(date=GENERATED_ON, n=inv["nb_couples_eleve_matiere"],
                                 nl=len(inv["niveaux"]))]
    for key in LEVEL_ORDER:
        lv = LEVELS[key]
        parts.append("### %s — %s\n" % (lv["label"], lv["subject"]))
        parts.append("Année N−1 : %s. Année N : %s.\n" % (lv["year_prev"], lv["year_next"]))
        parts.append("| Séance | Thème réellement travaillé |\n|---|---|")
        for s in ("S1", "S2", "S3", "S4", "S5"):
            parts.append("| %s | %s |" % (s, lv["sessions"][s]))
        parts.append("")
        parts.append("Prérequis critiques retenus pour l'entrée en %s : %s.\n"
                     % (lv["year_next"], ", ".join(lv["critical_prereqs"])))
        parts.append("Ponts vers l'année N introduits en phase 4 de la S5 : %s.\n"
                     % " ; ".join(lv["n_bridges"]))
    parts.append("---\n\n## 4. Élèves détectés\n")
    parts.append("| Élève | Niveau | Matière | Diagnostic | S1 | S2 | S3 | S4 | Priorité 1 | Priorité 2 |")
    parts.append("|---|---|---|:--:|:--:|:--:|:--:|:--:|---|---|")
    for e in inv["eleves"]:
        pers = e["documents_personnalises_disponibles"]
        def mark(tag):
            if any(("_%s_" % tag) in p or ("%s_" % tag) in os.path.basename(p) for p in pers):
                return "perso."
            return "niveau"
        parts.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            e["nom_affiche"], e["niveau_cle"], e["matiere"],
            "oui" if e["diagnostic_initial"]["disponible"] else "non",
            "niveau", mark("S2"), mark("S3"), mark("S4"),
            e["priorites_s5"]["P1"], e["priorites_s5"]["P2"]))
    parts.append("""
*« niveau »* : seuls les documents communs du niveau sont attestés pour cette séance.
*« perso. »* : un livret personnalisé de cette séance existe pour cet élève.

---

## 5. Lecture élève par élève

""")
    for e in inv["eleves"]:
        parts.append("### %s — %s (%s)\n" % (e["nom_affiche"], e["niveau_entree"], e["matiere"]))
        parts.append("**Diagnostic initial.** %s — %s%s\n" % (
            e["diagnostic_initial"]["items_traites"],
            e["diagnostic_initial"]["synthese"],
            "" if not e["diagnostic_initial"]["calibration_reussite_confiance"]
            else " Calibration réussite-confiance : %s." % e["diagnostic_initial"]["calibration_reussite_confiance"]))
        parts.append("**Points d'appui documentés.** %s\n" % " ; ".join(e["points_forts_identifies"]))
        parts.append("**Difficultés documentées.** %s\n" % " ".join(
            (d if d.endswith(".") else d + ".") for d in e["difficultes_identifiees"]))
        if e["observations_par_domaine"]:
            parts.append("| Domaine | Statut au diagnostic | Observation issue du bilan |")
            parts.append("|---|---|---|")
            for o in e["observations_par_domaine"]:
                parts.append("| %s | %s | %s |" % (o["domaine"], o["statut"], o["observation"]))
            parts.append("")
        else:
            parts.append("*Le dossier individuel de cet élève ne comporte pas de tableau détaillé par domaine : "
                         "seuls la synthèse, les points d'appui et les priorités sont documentés.*\n")
        p1 = e["priorites_s5"]["P1"]
        p2 = e["priorites_s5"]["P2"]
        parts.append("**Axes retenus pour la séance 5.** Priorité 1 : `%s`. Priorité 2 : `%s`.\n" % (p1, p2))
        parts.append("**Objectif de la séance.** %s\n" % e["objectif_s5"])
        nd = e["elements_non_documentes"]
        if nd:
            parts.append("**Compétences non évaluées ou non travaillées à ce jour.** %s\n" % ", ".join("`%s`" % s for s in nd))
        parts.append("**Progression objectivable avant la S5.** %s.\n" % e["progression_objectivable"])
        parts.append("")
    parts.append("""---

## 6. Conséquences pour la conception de la séance 5

1. La S5 ne peut pas être présentée comme une mesure de progrès déjà acquis : elle
   **produit** la mesure. Toutes les formulations des livrets et des dossiers enseignants
   emploient « à vérifier lors de l'évaluation finale » plutôt que « désormais maîtrisé ».
2. La comparaison initial/final est possible pour toute compétence disposant d'au moins
   un item du test de positionnement. Elle est impossible pour les compétences sans item
   de référence : elles sont marquées `non_comparable_absence_baseline`.
3. Les compétences introduites en phase 4 (ponts vers l'année N) sont marquées
   `non_comparable_contenu_nouveau` : elles sont notées, mais ne peuvent pas produire de delta.
4. Les axes de consolidation retenus proviennent exclusivement des priorités écrites
   dans les dossiers individuels ; aucun besoin n'a été déduit du seul niveau scolaire.
""")
    return "\n".join(parts)


def main():
    os.makedirs(AUDIT_DIR, exist_ok=True)
    inv = build_inventaire()
    with open(os.path.join(AUDIT_DIR, "inventaire_eleves.json"), "w", encoding="utf-8") as f:
        json.dump(inv, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(AUDIT_DIR, "AUDIT_S1_S4.md"), "w", encoding="utf-8") as f:
        f.write(build_audit_md(inv))
    with open(os.path.join(AUDIT_DIR, "conflits_sources.json"), "w", encoding="utf-8") as f:
        json.dump({"schema": "nexus-s5-conflits-v1", "genere_le": GENERATED_ON,
                   "nb_conflits": len(CONFLITS), "conflits": CONFLITS},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("inventaire : %d élèves" % inv["nb_couples_eleve_matiere"])
    manquants = [(e["nom_affiche"], s["chemin"]) for e in inv["eleves"]
                 for s in e["sources"] if not s["existe"]]
    if manquants:
        print("SOURCES INTROUVABLES :")
        for n, p in manquants:
            print("   %-24s %s" % (n, p))
    else:
        print("toutes les sources déclarées existent")


if __name__ == "__main__":
    main()
