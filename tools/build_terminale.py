#!/usr/bin/env python3
"""Génération des documents nominatifs des stages de pré-rentrée Terminale.

Ce pipeline est indépendant de `tools/build.py`, qui couvre les niveaux 4e, 3e, 2nde et
1re : il ne le modifie pas et ne partage aucun registre avec lui.

Trois sources, aucune autre :

- `content/students_terminale.json`   — registre nominatif de la cohorte (2 groupes) ;
- `content/diagnostics_terminale.json` — diagnostics extraits des bilans PDF par
  `tools/extract_bilans_terminale.py` ;
- `content/items_terminale.json`      — banque des items du positionnement, avec pour chacun
  la compétence de Première évaluée, le geste correct, le lien avec le programme de Terminale
  et un exercice-variante corrigé.

Pour chaque couple (élève, matière), trois documents sont produits :

1. le livret individuel — carte maîtrise × confiance, priorités, parcours séance par séance,
   reprise **item par item** de chaque erreur commise, plan de septembre, fiches de suivi ;
2. le plan de remédiation ciblée, version élève — les exercices-variantes des items
   effectivement manqués, sans corrigé ;
3. le même plan, version enseignant — avec corrigé, relevé de maîtrise et notes de conduite.

Aucun contenu n'est extrapolé : chaque énoncé, chaque réponse donnée, chaque origine d'erreur
provient du bilan de l'élève. C'est ce qui rend les livrets individuels et vérifiables.

Usage :
    python3 tools/build_terminale.py            # écrit les documents nominatifs
    python3 tools/build_terminale.py --check    # échoue si les fichiers committés sont périmés
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.latex_notation import to_latex  # noqa: E402

REGISTRY_PATH = "content/students_terminale.json"
DIAGNOSTICS_PATH = "content/diagnostics_terminale.json"
ITEMS_PATH = "content/items_terminale.json"

def stage_frame(registry: dict) -> dict[str, str]:
    """Cadre matériel du stage : organisme, durée, rythme, dates."""
    return registry["cadre"]


CONFIDENTIAL_BANNER = (
    "> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  \n"
    "> À conserver dans le dossier pédagogique de l'élève. Ne pas diffuser hors de Nexus "
    "Réussite et de la famille concernée."
)

ANSWER_LINE = "." * 100


class BuildError(RuntimeError):
    """Registre, diagnostics ou banque d'items incohérents."""


@dataclass(frozen=True)
class Module:
    """Un module de stage : arborescence, intitulés et progression commune."""

    key: str
    label: str
    nominative_dir: str
    sources_dir: str
    subject_label: str
    source_document: str
    sessions: tuple[tuple[int, str], ...]
    # Les modules ne nomment pas leurs documents de la même façon : le support de séance
    # s'appelle « manipulation » en sciences et « pratiques » en NSI, le mini-diagnostic
    # est « pratique » en NSI seulement. Ces différences sont ici plutôt que dispersées
    # en conditions sur la clé du module.
    supports_suffix: str = "SUPPORTS_Manipulation"
    diagnostic_prefix: str = "Mini_Diagnostic"
    portfolio_dir: str = "03_EVALUATIONS"
    extra_portfolio: tuple[str, ...] = ()
    extra_teacher_documents: tuple[str, ...] = ()


MODULES: dict[str, Module] = {
    "tle_spe": Module(
        key="tle_spe",
        label="Terminale Spécialité Mathématiques",
        nominative_dir="04_NOMINATIFS",
        sources_dir="05_SOURCES",
        subject_label="Mathématiques",
        source_document="stage_prerentree_terminale_maths.md",
        sessions=(
            (1, "Suites numériques : du sens de variation à la récurrence"),
            (2, "Fonction exponentielle : exposants, équations, vers le logarithme"),
            (3, "Second degré : discriminant, signe du trinôme, tableau de signes"),
            (4, "Dérivation : du nombre dérivé aux variations, ouverture sur la convexité"),
            (5, "Produit scalaire vers l'espace, probabilités, Python, évaluation"),
        ),
        extra_teacher_documents=("tle_spe_Option_Maths_Expertes.md",),
    ),
    "tle_nsi": Module(
        key="tle_nsi",
        label="Terminale NSI",
        nominative_dir="05_NOMINATIFS",
        sources_dir="07_SOURCES",
        subject_label="NSI",
        source_document="stage_prerentree_terminale_nsi.md",
        sessions=(
            (1, "Représentation des données et booléens"),
            (2, "Types construits : tableaux, dictionnaires, mutabilité"),
            (3, "Programmation : fonctions, retour, portée, boucles"),
            (4, "Algorithmique : préconditions, recherche, tris, coût"),
            (5, "Données en tables, bases de données, systèmes, évaluation"),
        ),
        supports_suffix="SUPPORTS_Pratiques",
        diagnostic_prefix="Mini_Diagnostic_Pratique",
        portfolio_dir="04_PORTFOLIO",
        extra_portfolio=("tle_nsi_Memento_Python_Terminale_ELEVE.md",),
    ),
    "tle_pc": Module(
        key="tle_pc",
        label="Terminale Spécialité Physique-Chimie",
        nominative_dir="04_NOMINATIFS",
        sources_dir="05_SOURCES",
        subject_label="Physique-chimie",
        source_document="stage_prerentree_terminale_pc.md",
        sessions=(
            (1, "Transformations chimiques : avancement, réactif limitant, oxydo-réduction"),
            (2, "Mécanique : vecteur vitesse, forces, vers la deuxième loi de Newton"),
            (3, "Énergie : travail, énergies cinétique et potentielle, énergie mécanique"),
            (4, "Ondes et optique : période, célérité, longueur d'onde, lentilles minces"),
            (5, "Électricité, chimie organique, mesure et incertitudes, évaluation"),
        ),
        extra_portfolio=("tle_pc_Memento_Formules_Terminale_ELEVE.md",),
    ),
}

# Le quadrant d'un domaine décide de la posture de travail. L'ordre de ce tableau est
# l'ordre de traitement : une certitude erronée passe avant tout le reste.
QUADRANTS: tuple[tuple[str, str, str, str], ...] = (
    (
        "certitudes_a_revoir",
        "Certitude à revoir",
        "CONFRONTER",
        "Une réponse fausse a été donnée avec assurance. On part d'un cas qui met la "
        "conviction en défaut, on fait verbaliser le raisonnement, puis on reconstruit la "
        "notion avant tout entraînement.",
    ),
    (
        "sans_reponse",
        "Sans réponse",
        "DIAGNOSTIQUER",
        "Aucune réponse n'a été apportée sur ce domaine. On ne devine pas : un test ciblé "
        "est passé au démarrage, et la remédiation est décidée à partir de ce qu'il montre.",
    ),
    (
        "a_installer",
        "Difficulté repérée, sans fausse certitude",
        "INSTALLER",
        "La difficulté est repérée et assumée : il n'y a aucune fausse certitude à défaire. "
        "On pose les définitions utiles, on montre des exemples résolus, puis on entraîne "
        "court et souvent.",
    ),
    (
        "a_consolider",
        "Réussite hésitante",
        "CONSOLIDER",
        "Les réponses sont justes mais l'hésitation se sent encore. On organise un "
        "entraînement espacé, sans réenseigner ce qui est déjà compris.",
    ),
    (
        "acquis",
        "Acquis disponible",
        "ENTRETENIR",
        "Les réponses sont justes et assumées. Ce domaine est un point d'appui : on s'en "
        "sert comme socle pour aller plus loin.",
    ),
)
QUADRANT_BY_KEY = {key: (title, posture, method) for key, title, posture, method in QUADRANTS}
WORKED_QUADRANTS = ("certitudes_a_revoir", "sans_reponse", "a_installer", "a_consolider")

# Le livret et la fiche de séance nomment la même piste de la même façon : sans cela, un
# élève lisant « Consolidation » dans son livret devait deviner qu'il relevait de la ligne
# « CONFRONTER » du tableau d'aiguillage.
PARCOURS_BY_QUADRANT = {
    "certitudes_a_revoir": "Confronter",
    "sans_reponse": "Diagnostiquer",
    "a_installer": "Installer",
    "a_consolider": "Consolider",
    "acquis": "Entretenir",
}

# Un élève dont le bilan ne comporte aucun domaine à reprendre atteignait la fin de la fiche
# avant la fin de la phase différenciée : le parcours d'approfondissement s'arrêtait à
# l'exercice 8. Les exercices 9 et 10 de chaque séance lui sont destinés.
PARCOURS_SANS_REPRISE = "Excellence"

# Ce que chaque séance apporte à un élève qui n'a rien à reprendre sur son thème. Sans cette
# table, toutes ses séances portaient la même phrase d'attente, qui ne disait rien de ce
# qu'il allait faire.
OBJECTIF_SANS_PRIORITE = {
    "tle_spe": {
        1: "Rédiger la démonstration du sens de variation d'une suite géométrique, puis "
           "établir qu'une suite peut croître sans jamais dépasser une valeur.",
        2: "Mener une étude de fonction complète sur un produit faisant intervenir "
           "l'exponentielle, et trancher une équation par le tableau de variations.",
        3: "Factoriser un polynôme de degré 3 à partir d'une racine évidente, puis discuter "
           "le nombre de solutions d'une équation selon un paramètre.",
        4: "Dériver un quotient, en déduire un encadrement de la fonction, et distinguer "
           "l'annulation de la dérivée du changement de signe.",
        5: "Établir une probabilité en fonction d'un paramètre, la comparer à une valeur "
           "seuil par une factorisation, et la vérifier par un programme.",
    },
    "tle_nsi": {
        1: "Justifier la correspondance entre un chiffre hexadécimal et quatre bits, et "
           "expliquer le codage des entiers négatifs en complément à deux.",
        2: "Implémenter une structure de données à partir d'une liste et en spécifier les "
           "préconditions.",
        3: "Écrire une fonction avec sa spécification et ses tests, et distinguer ce qu'elle "
           "renvoie de ce qu'elle modifie.",
        4: "Comparer le coût de deux algorithmes sur un même problème et justifier le choix "
           "par le nombre d'opérations, pas par le temps mesuré.",
        5: "Écrire une requête faisant intervenir une jointure, et traiter le même besoin "
           "par un programme lisant le fichier.",
    },
    "tle_pc": {
        1: "Conduire un tableau d'avancement jusqu'au réactif limitant sur une "
           "transformation à trois réactifs, et écrire les demi-équations associées.",
        2: "Établir un bilan des forces sur un plan incliné et relier la variation du vecteur "
           "vitesse à la résultante.",
        3: "Traiter un mouvement avec frottement par un bilan d'énergie, et identifier "
           "l'énergie dissipée.",
        4: "Construire l'image d'un objet placé entre le foyer et le centre optique, puis "
           "traiter un système de deux lentilles.",
        5: "Contrôler un résultat par son ordre de grandeur et par le nombre de chiffres "
           "significatifs, et justifier le rejet d'une valeur.",
    },
}

AIDES = (
    ("A", "Rappel de la propriété ou de la syntaxe, sans application"),
    ("B", "Première étape faite, suite à la charge de l'élève"),
    ("C", "Exemple résolu analogue, à transposer"),
    ("D", "Découpage de la tâche en sous-questions"),
    ("E", "Corrigé partiel ou squelette à compléter"),
)


def load_json(root: Path, relative: str) -> dict:
    path = root / relative
    if not path.exists():
        raise BuildError(f"Fichier source introuvable : {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def slug(value: str) -> str:
    """Identifiant de fichier stable, sans accent ni espace."""
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
    kept = [c if c.isalnum() else "_" for c in stripped]
    return "_".join(part for part in "".join(kept).split("_") if part)


def format_percentage(value: float) -> str:
    return f"{value:.1f}".replace(".", ",").rstrip("0").rstrip(",") + " %"


def check_sources(registry: dict, diagnostics: dict, items: dict) -> None:
    """Vérifie que les trois sources se répondent, avant toute écriture."""
    errors: list[str] = []
    groups = {group["id"] for group in registry["groupes"]}
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()

    for student in registry["students"]:
        where = f"élève '{student['id']}'"
        if student["id"] in seen_ids:
            errors.append(f"{where} : identifiant dupliqué")
        seen_ids.add(student["id"])
        if student["slug"] in seen_slugs:
            errors.append(f"{where} : slug dupliqué '{student['slug']}'")
        seen_slugs.add(student["slug"])
        if student["groupe"] not in groups:
            errors.append(f"{where} : groupe inconnu '{student['groupe']}'")
        # Un élève inscrit après la campagne de positionnement n'a aucune matière
        # diagnostiquée : ses matières figurent toutes dans matieresSansDiagnostic.
        # Ce qui serait fautif, c'est de n'avoir aucune matière du tout.
        if not student["matieres"] and not student.get("matieresSansDiagnostic"):
            errors.append(f"{where} : aucune matière déclarée")
        option = student.get("optionAnnuelle")
        if option is not None:
            if option["diagnosticId"] not in diagnostics["diagnostics"]:
                errors.append(
                    f"{where} : diagnostic d'option introuvable '{option['diagnosticId']}'"
                )
            elif option["intitule"] not in items["instruments"]:
                errors.append(f"{where} : aucun instrument pour '{option['intitule']}'")

        for missing in student.get("matieresSansDiagnostic", []):
            if missing["module"] not in MODULES:
                errors.append(f"{where} : module inconnu '{missing['module']}'")
            if not missing.get("motif", "").strip():
                errors.append(
                    f"{where} : matière '{missing.get('matiere')}' sans diagnostic doit "
                    "porter un motif expliquant ce qui manque"
                )

        for subject in student["matieres"]:
            if subject["module"] not in MODULES:
                errors.append(f"{where} : module inconnu '{subject['module']}'")
            diagnostic_id = subject["diagnosticId"]
            diagnostic = diagnostics["diagnostics"].get(diagnostic_id)
            if diagnostic is None:
                errors.append(f"{where} : diagnostic introuvable '{diagnostic_id}'")
                continue
            if normalize(diagnostic["eleve"]) not in {normalize(a) for a in student["aliases"]}:
                errors.append(
                    f"{where} : le bilan '{diagnostic_id}' est au nom de "
                    f"'{diagnostic['eleve']}', absent des alias déclarés"
                )
            if diagnostic["matiere"] != subject["matiere"]:
                errors.append(
                    f"{where} : matière '{subject['matiere']}' différente de celle du bilan "
                    f"'{diagnostic['matiere']}'"
                )
            instrument = items["instruments"].get(diagnostic["matiere"])
            if instrument is None:
                errors.append(f"{where} : aucun instrument pour '{diagnostic['matiere']}'")
                continue
            bank = instrument["items"]
            if len(bank) != len(diagnostic["items"]):
                errors.append(
                    f"{where} : {len(diagnostic['items'])} items au bilan contre "
                    f"{len(bank)} en banque pour '{diagnostic['matiere']}'"
                )
                continue
            for rank, (item, reference) in enumerate(zip(diagnostic["items"], bank), 1):
                if item["question"] != reference["question"]:
                    errors.append(f"{where} : énoncé divergent à l'item {rank}")
                if item["domaine"] != reference["domaine"]:
                    errors.append(f"{where} : domaine divergent à l'item {rank}")

    if errors:
        raise BuildError("Sources incohérentes :\n- " + "\n- ".join(errors))


def specialites(student: dict, group: dict) -> list[str]:
    """Spécialités réellement suivies par l'élève.

    Le groupe porte une combinaison nominale — « mathématiques et NSI », « mathématiques et
    physique-chimie » — mais il sert d'abord à organiser les séances. Un élève peut y être
    rattaché sans suivre exactement cette combinaison ; son livret doit alors annoncer ce
    qu'il suit vraiment, pas l'étiquette du groupe.
    """
    return student.get("specialites") or group["specialites"]


def worked_domains(diagnostic: dict) -> list[tuple[str, str]]:
    """Domaines à travailler, dans l'ordre de priorité, avec leur quadrant."""
    card = diagnostic["carte_maitrise_confiance"]
    ordered: list[tuple[str, str]] = []
    for key in WORKED_QUADRANTS:
        for domain in card.get(key, []):
            ordered.append((domain, key))
    return ordered


def domains_to_fix(diagnostic: dict) -> list[str]:
    """Domaines portant une erreur, par opposition à ceux qui ne demandent qu'à être affermis.

    Un acquis hésitant se travaille par répétition, pas par remédiation : un élève qui n'a
    qu'un domaine à consolider n'a rien à reprendre au sens strict, et relève de la piste
    excellence sur toutes les séances où aucun focus personnel ne lui est assigné.
    """
    card = diagnostic["carte_maitrise_confiance"]
    return [domain
            for key in ("certitudes_a_revoir", "sans_reponse", "a_installer")
            for domain in card.get(key, [])]


def domain_quadrant(diagnostic: dict, domain: str) -> str:
    for key, _title, _posture, _method in QUADRANTS:
        if domain in diagnostic["carte_maitrise_confiance"].get(key, []):
            return key
    return "acquis"


def items_to_revisit(diagnostic: dict, bank: list[dict]) -> list[tuple[int, dict, dict]]:
    """Items effectivement manqués ou laissés vides, avec leur entrée de banque."""
    return [
        (rank, item, reference)
        for rank, (item, reference) in enumerate(zip(diagnostic["items"], bank), 1)
        if item["verdict"] != "JUSTE"
    ]


# Au plus deux items de consolidation par domaine : au-delà, la feuille devient une
# feuille d'entraînement générale et perd son caractère ciblé.
MAX_CONSOLIDATION_PAR_DOMAINE = 2


def items_to_secure(diagnostic: dict, bank: list[dict]) -> list[tuple[int, dict, dict]]:
    """Items réussis dont l'acquis reste fragile : à affermir, pas à réenseigner.

    Deux signaux, et non un seul. Le premier est la certitude déclarée item par item. Le
    second est le classement du domaine en « réussite hésitante » par le bilan lui-même :
    il reste disponible quand l'élève n'a renseigné aucune certitude, cas où le premier
    signal ne dirait rien alors que le bilan, lui, a tranché.
    """
    hesitant = set(diagnostic["carte_maitrise_confiance"].get("a_consolider", []))
    selected: list[tuple[int, dict, dict]] = []
    par_domaine: dict[str, int] = {}
    for rank, (item, reference) in enumerate(zip(diagnostic["items"], bank), 1):
        if item["verdict"] != "JUSTE":
            continue
        certainty = item["certitude_sur_4"]
        fragile = (certainty is not None and certainty <= 2) or item["domaine"] in hesitant
        if not fragile:
            continue
        if par_domaine.get(item["domaine"], 0) >= MAX_CONSOLIDATION_PAR_DOMAINE:
            continue
        par_domaine[item["domaine"]] = par_domaine.get(item["domaine"], 0) + 1
        selected.append((rank, item, reference))
    return selected


def session_focus(diagnostic: dict, module: Module) -> list[dict[str, object]]:
    """Croise la progression commune du module et le parcours personnel du bilan."""
    personal = {entry["seance"]: entry for entry in diagnostic["parcours_seances"]}
    rows: list[dict[str, object]] = []
    for number, theme in module.sessions:
        entry = personal.get(number, {})
        focus = entry.get("focus") or []
        if focus:
            domains = " · ".join(f"{f['domaine']} ({f['posture']})" for f in focus)
            objectives = " ".join(f["objectif"] for f in focus)
            quadrant = domain_quadrant(diagnostic, focus[0]["domaine"])
        else:
            domains = "Consolidation d'ensemble"
            objectives = OBJECTIF_SANS_PRIORITE[module.key][number]
            quadrant = "acquis"
        parcours = PARCOURS_BY_QUADRANT[quadrant]
        if not focus and not domains_to_fix(diagnostic):
            parcours = PARCOURS_SANS_REPRISE
            domains = "Rédaction et raisonnement"
        rows.append({
            "seance": number,
            "theme": theme,
            "focus": domains,
            "objectif": objectives,
            "parcours": parcours,
        })
    return rows


def render_option_section(student: dict, option_diagnostic: dict,
                          option_instrument: dict) -> list[str]:
    """Section « option annuelle » du livret de mathématiques.

    L'option mathématiques expertes ne fait pas l'objet d'un stage à part : elle se prépare
    à l'intérieur du stage de mathématiques. Son positionnement propre est donc reversé
    ici, avec les mêmes règles de lecture que le reste du livret — et le même refus
    d'extrapoler au-delà du bilan.
    """
    intitule = student["optionAnnuelle"]["intitule"]
    bank = option_instrument["items"]
    domains = option_instrument["domaines"]
    scores = option_diagnostic["reussite_par_domaine"]
    revisit = items_to_revisit(option_diagnostic, bank)
    priorities = worked_domains(option_diagnostic)

    out: list[str] = []
    add = out.append

    add("<div class=\"page-break\"></div>")
    add("")
    add(f"## Option annuelle — {intitule}")
    add("")
    add(f"Tu suivras l'enseignement optionnel de **{intitule.lower()}** en Terminale, en plus "
        "de la spécialité. **Il n'y a pas de stage séparé pour cette option** : elle se "
        "prépare à l'intérieur du stage de mathématiques, sur le temps différencié.")
    add("")
    add(f"Un positionnement distinct t'a été proposé le {option_diagnostic['date_bilan']}. "
        "Voici ce qu'il montre, et ce que l'option en fera.")
    add("")
    add(f"**Source :** `Bilans/{Path(option_diagnostic['source_pdf']).name}`")
    add("")

    add("### Ta réussite par domaine")
    add("")
    add("| Domaine | Réussite | Situation | Ce que l'option en fait en Terminale |")
    add("|---|---:|---|---|")
    for domain, score in scores.items():
        quadrant = domain_quadrant(option_diagnostic, domain)
        title, _posture, _method = QUADRANT_BY_KEY[quadrant]
        opening = domains.get(domain, {}).get("ouverture_terminale", "—")
        add(f"| {domain} | {format_percentage(score)} | {title} | {opening} |")
    add("")

    add("### Tes priorités pour l'option")
    add("")
    if not priorities:
        add("Aucune priorité ne ressort de ce positionnement : les prérequis de l'option sont "
            "en place. Le temps différencié servira à aller plus loin, pas à combler.")
        add("")
    else:
        add("| # | Domaine | Posture | Ce qu'on en fait |")
        add("|---:|---|---|---|")
        for index, (domain, quadrant) in enumerate(priorities, 1):
            _title, posture, method = QUADRANT_BY_KEY[quadrant]
            add(f"| {index} | {domain} | **{posture}** | {method} |")
        add("")

    if revisit:
        add("### Les items à reprendre pour l'option")
        add("")
        add(f"**{len(revisit)} item(s)** à reprendre, avec l'énoncé exact et l'origine de "
            "l'erreur telle qu'établie par ton bilan.")
        add("")
        for rank, item, reference in revisit:
            unanswered = item["verdict"] in ("NON TRAITÉE", "NON TRAITÉ", "SANS RÉPONSE")
            add(f"#### Item {rank} — {item['domaine']} · {reference['competence']}")
            add("")
            add(f"**Énoncé.** {item['question']}")
            add("")
            if unanswered:
                add("**Ta réponse.** _Question non traitée._ On fera le point au démarrage, "
                    "sans rien supposer.")
            else:
                add(f"**Ta réponse.** {item['reponse_donnee']}")
            add("")
            if item["reponse_attendue"]:
                add(f"**Réponse attendue.** {item['reponse_attendue']}")
                add("")
            if item["origine_erreur"]:
                add(f"**D'où vient l'erreur.** {item['origine_erreur']}")
                add("")
            add(f"**Ce qu'il faut retenir.** {item['a_retenir']}")
            add("")
            add(f"**Le geste à installer.** {reference['geste_correct']}")
            add("")
    else:
        add("### Aucun item à reprendre")
        add("")
        add("Ton positionnement d'option ne comporte ni réponse fausse ni question laissée "
            "vide. Le travail portera sur la rédaction des démonstrations, que l'option "
            "exige plus que la spécialité et que le positionnement ne mesure pas.")
        add("")

    add("### Comment l'option sera travaillée pendant le stage")
    add("")
    add("| Séance | Ce qui est prévu pour l'option |")
    add("|---:|---|")
    for number, contenu in (
        (1, "Division euclidienne : poser a = bq + r et contrôler 0 ≤ r < b"),
        (2, "Diviseurs, nombres premiers, décomposition en facteurs premiers"),
        (3, "PGCD et algorithme d'Euclide ; fractions irréductibles"),
        (4, "Logique : contraposée, réciproque, contre-exemple"),
        (5, "Calcul littéral et systèmes ; ouverture sur les matrices et les complexes"),
    ):
        add(f"| {number} | {contenu} |")
    add("")
    add("Ces vingt minutes sont prélevées sur le temps différencié de chaque séance : elles "
        "ne retirent rien au programme commun du stage.")
    add("")
    return out


def render_livret(student: dict, subject: dict, diagnostic: dict, instrument: dict,
                  module: Module, group: dict, frame: dict,
                  option: tuple[dict, dict] | None = None) -> str:
    """Livret individuel : le document principal remis à l'élève et à sa famille."""
    name = student["displayName"]
    bank = instrument["items"]
    domains = instrument["domaines"]
    card = diagnostic["carte_maitrise_confiance"]
    scores = diagnostic["reussite_par_domaine"]
    revisit = items_to_revisit(diagnostic, bank)
    secure = items_to_secure(diagnostic, bank)
    priorities = worked_domains(diagnostic)

    out: list[str] = []
    add = out.append

    add(f"# {module.label} — Livret individuel — {name}")
    add(f"## {subject['matiere']} — Stage de pré-rentrée 2026-2027")
    add("")
    add(CONFIDENTIAL_BANNER)
    add("")
    add(f"**Élève :** {name}  ")
    add(f"**Groupe :** {group['libelle']}  ")
    add(f"**Spécialités conservées :** {', '.join(specialites(student, group))}  ")
    add(f"**Matière de ce livret :** {subject['matiere']}  ")
    if student.get("optionAnnuelle"):
        add(f"**Option suivie en Terminale :** {student['optionAnnuelle']['intitule']}  ")
    add(f"**Organisme :** {frame['organisme']} — {frame['natureOrganisme'].lower()}  ")
    add(f"**Stage :** {frame['dureeParSpecialite']}, {frame['rythme']}  ")
    add(f"**Dates :** {frame['dates']}  ")
    add("**Année scolaire préparée :** 2026-2027  ")
    add(f"**Diagnostic du :** {diagnostic['date_bilan']}  ")
    add(f"**Source :** `Bilans/{Path(diagnostic['source_pdf']).name}`")
    add("")
    if student.get("noteGroupe"):
        add(f"> **Rattachement au groupe.** {student['noteGroupe']}")
        add("")
    if student.get("homonymeAvertissement"):
        add(f"> **Attention — homonymie.** {student['homonymeAvertissement']}")
        add("")

    add("---")
    add("")
    add("## 1. Comment lire ce livret")
    add("")
    add("Ce livret ne donne aucune note. Il croise deux informations issues de ton "
        "positionnement : **ce que tu réussis**, et **la confiance** avec laquelle tu "
        "réponds.")
    add("")
    add("C'est ce croisement qui distingue quatre situations, qui ne se travaillent pas de la "
        "même façon :")
    add("")
    add("| | Certitude faible (1-2) | Certitude forte (3-4) |")
    add("|---|---|---|")
    add("| **Réponse fausse** | une notion manque : on l'**installe** | une idée fausse est "
        "tenue pour vraie : on la **confronte** |")
    add("| **Réponse juste** | l'acquis est fragile : on le **consolide** | l'acquis est "
        "disponible : on l'**entretient** |")
    add("")
    add("Les certitudes à revoir passent en premier : tant qu'on croit juste une idée fausse, "
        "on ne la corrige pas seul.")
    add("")
    add("Tout ce qui suit vient de **ton** bilan. Aucun contenu n'a été ajouté ni deviné.")
    add("")

    add("## 2. Ta carte maîtrise × confiance")
    add("")
    add("| Situation | Tes domaines | Ce qu'on en fait |")
    add("|---|---|---|")
    for key, title, posture, _method in QUADRANTS:
        listed = card.get(key, [])
        content = " · ".join(listed) if listed else "_aucun_"
        add(f"| {title} | {content} | **{posture}** |")
    add("")

    add("### Ta réussite par domaine")
    add("")
    add("| Domaine | Réussite | Situation | Prérequis de Première évalué |")
    add("|---|---:|---|---|")
    for domain, score in scores.items():
        quadrant = domain_quadrant(diagnostic, domain)
        title, _posture, _method = QUADRANT_BY_KEY[quadrant]
        prerequisite = domains.get(domain, {}).get("prerequis_premiere", "—")
        add(f"| {domain} | {format_percentage(score)} | {title} | {prerequisite} |")
    add("")
    add("_Ces chiffres décrivent ta réussite domaine par domaine. Ce livret ne donne pas de "
        "note._")
    add("")

    add("## 3. Ce qui est en jeu pour la Terminale")
    add("")
    add("Pour chaque domaine évalué, voici ce que le programme de Terminale en fera. C'est ce "
        "qui explique pourquoi ce stage porte sur ces contenus-là et pas sur d'autres.")
    add("")
    for domain in scores:
        info = domains.get(domain, {})
        quadrant = domain_quadrant(diagnostic, domain)
        title, posture, _method = QUADRANT_BY_KEY[quadrant]
        add(f"### {domain} — {format_percentage(scores[domain])} · {title} · **{posture}**")
        add("")
        add(f"**Ce que tu dois avoir en entrant en Terminale.** {info.get('prerequis_premiere', '—')}")
        add("")
        add(f"**Ce que la Terminale en fera.** {info.get('ouverture_terminale', '—')}")
        add("")
        add(f"**Au programme officiel :** {info.get('reference_programme', '—')}")
        add("")

    add("## 4. Tes priorités, dans l'ordre")
    add("")
    if not priorities:
        add("Ton bilan ne fait apparaître aucune priorité : tous les domaines évalués sont "
            "acquis et assumés. Le stage servira à **prolonger** ces acquis. Choisis dès la "
            "première séance un domaine que tu veux pousser plus loin : le parcours "
            "d'approfondissement partira de là.")
        add("")
    else:
        add("| # | Domaine | Posture | Pourquoi, et comment on s'y prend |")
        add("|---:|---|---|---|")
        for index, (domain, quadrant) in enumerate(priorities, 1):
            _title, posture, method = QUADRANT_BY_KEY[quadrant]
            add(f"| {index} | {domain} | **{posture}** | {method} |")
        add("")
    if diagnostic["points_appui"]:
        add("### Tes points d'appui")
        add("")
        for point in diagnostic["points_appui"]:
            add(f"- {point}")
        add("")
    if diagnostic["auto_evaluation"]:
        add("### Ta calibration")
        add("")
        add(f"> {diagnostic['auto_evaluation']}")
        add("")

    add("## 5. Ton parcours, séance par séance")
    add("")
    add("Le thème de la séance est commun au groupe. Le focus, l'objectif et le parcours sont "
        "les tiens.")
    add("")
    add("| Séance | Thème commun du stage | Ton focus personnel | Ton parcours | Aide max. utilisée | Preuve recueillie |")
    add("|---:|---|---|---|---|---|")
    for row in session_focus(diagnostic, module):
        add(f"| {row['seance']} | {row['theme']} | {row['focus']} | {row['parcours']} | | |")
    add("")
    add("**Objectif de chaque séance, pour toi :**")
    add("")
    for row in session_focus(diagnostic, module):
        add(f"- **Séance {row['seance']}** — {row['objectif']}")
    add("")

    add("<div class=\"page-break\"></div>")
    add("")
    add("## 6. Tes erreurs, une par une")
    add("")
    if not revisit:
        add("**Aucune erreur à reprendre.** Ton positionnement ne comporte ni réponse fausse, "
            "ni question laissée vide. C'est rare, et cela change la nature de ton stage : tu "
            "suis la **piste excellence** dès la première séance — les exercices 9 et 10 de chaque "
            "fiche, un problème de type bac et une question ouverte — et le travail porte "
            "sur la **rédaction** et la **justification**, que le positionnement ne mesurait "
            "pas.")
        add("")
    else:
        add(f"Ton positionnement comporte **{len(revisit)} item(s)** à reprendre. Pour chacun : "
            "l'énoncé exact, ta réponse, la réponse attendue, l'origine de l'erreur, ce qu'il "
            "faut retenir, et le geste correct à installer.")
        add("")
        for rank, item, reference in revisit:
            unanswered = item["verdict"] in ("NON TRAITÉE", "NON TRAITÉ", "SANS RÉPONSE")
            certainty = (
                f"certitude déclarée {item['certitude_sur_4']}/4 — « {item['certitude_mot']} »"
                if item["certitude_sur_4"] is not None else "certitude non renseignée"
            )
            add(f"### Item {rank} — {item['domaine']} · {reference['competence']}")
            add("")
            add(f"**Statut :** {item['verdict']} · {certainty}")
            add("")
            add(f"**Énoncé.** {item['question']}")
            add("")
            if unanswered:
                add("**Ta réponse.** _Question non traitée._ Une question laissée vide "
                    "renseigne aussi : on fera le point ensemble au démarrage, sans rien "
                    "supposer.")
            else:
                add(f"**Ta réponse.** {item['reponse_donnee']}")
            add("")
            if item["reponse_attendue"]:
                add(f"**Réponse attendue.** {item['reponse_attendue']}")
                add("")
            if item["origine_erreur"]:
                add(f"**D'où vient l'erreur.** {item['origine_erreur']}")
                add("")
            add(f"**Ce qu'il faut retenir.** {item['a_retenir']}")
            add("")
            add(f"**Le geste à installer.** {reference['geste_correct']}")
            add("")
            add("**Ma reformulation, avec mes mots :**")
            add("")
            add(ANSWER_LINE)
            add("")
            add(ANSWER_LINE)
            add("")

    if secure:
        add("## 7. Ce que tu réussis sans en être sûr")
        add("")
        add(f"Sur **{len(secure)} item(s)**, ta réponse était juste mais l'assurance n'y "
            "était pas encore — soit parce que ta certitude déclarée était basse, soit parce "
            "que le domaine est classé en réussite hésitante. Ce ne sont pas des erreurs : ce "
            "sont des acquis à affermir par répétition espacée. C'est le travail le moins "
            "coûteux et le plus rentable de ton stage.")
        add("")
        add("| Item | Domaine | Compétence | Ta certitude | Le geste qui la rendra sûre |")
        add("|---:|---|---|:---:|---|")
        for rank, item, reference in secure:
            certainty = (f"{item['certitude_sur_4']}/4"
                         if item["certitude_sur_4"] is not None else "non déclarée")
            add(f"| {rank} | {item['domaine']} | {reference['competence']} | "
                f"{certainty} | {reference['geste_correct']} |")
        add("")

    add("<div class=\"page-break\"></div>")
    add("")
    add("## 8. Ton plan de travail entre les séances")
    add("")
    if diagnostic["plan_action_inter_seances"]:
        for action in diagnostic["plan_action_inter_seances"]:
            add(f"- {action}")
        add("")
    add("**Mes quatre semaines de septembre :**")
    add("")
    add("| Semaine | Ce que je travaille | Comment je vérifie que c'est acquis |")
    add("|---:|---|---|")
    plan = priorities[:4] if priorities else []
    for week in range(1, 5):
        if week <= len(plan):
            domain, quadrant = plan[week - 1]
            _title, posture, _method = QUADRANT_BY_KEY[quadrant]
            add(f"| {week} | {domain} — {posture.lower()} | |")
        else:
            add(f"| {week} | | |")
    add("")

    add("## 9. Fiches de suivi")
    add("")
    add("### Fiche de suivi enseignant")
    add("")
    add("| Observation | S1 | S2 | S3 | S4 | S5 |")
    add("|---|:---:|:---:|:---:|:---:|:---:|")
    for observation in ("Procédure choisie", "Exactitude", "Justification écrite",
                        "Contrôle effectué", "Certitude cohérente"):
        add(f"| {observation} | | | | | |")
    add("")
    add("### Relevé des aides utilisées")
    add("")
    add("| Aide | Contenu |")
    add("|---|---|")
    for letter, description in AIDES:
        add(f"| {letter} | {description} |")
    add("")
    add("| Séance | 1 | 2 | 3 | 4 | 5 |")
    add("|---|:---:|:---:|:---:|:---:|:---:|")
    add("| Aide maximale utilisée | | | | | |")
    add("")
    add("_L'aide maximale doit décroître entre la séance 1 et la séance 5. C'est l'un des "
        "cinq critères de réussite du stage._")
    add("")

    add("### Fiche de suivi élève — une par séance")
    add("")
    for number, theme in module.sessions:
        add(f"**Séance {number} — {theme}**")
        add("")
        add(f"- Ce que j'ai compris : {ANSWER_LINE[:70]}")
        add(f"- Mon ancienne erreur : {ANSWER_LINE[:70]}")
        add(f"- Comment je la corrige : {ANSWER_LINE[:70]}")
        add("- Ma certitude aujourd'hui : ☐1 ☐2 ☐3 ☐4 · Aide utilisée : ☐A ☐B ☐C ☐D ☐E ☐aucune")
        add("")

    add("## 10. Auto-évaluation finale")
    add("")
    add("| Affirmation | Pas encore | Avec aide | Seul | Je peux expliquer |")
    add("|---|:---:|:---:|:---:|:---:|")
    for domain in scores:
        add(f"| Je maîtrise : {domain} | ☐ | ☐ | ☐ | ☐ |")
    add("| J'écris la propriété avant de calculer | ☐ | ☐ | ☐ | ☐ |")
    add("| Je contrôle avant de déclarer une certitude | ☐ | ☐ | ☐ | ☐ |")
    add("| Ma certitude est cohérente avec ma réussite | ☐ | ☐ | ☐ | ☐ |")
    add("")

    if option is not None:
        out.extend(render_option_section(student, option[0], option[1]))

    add("## 11. Bilan final")
    add("")
    add("### Comparaison initiale / finale")
    add("")
    add("| Domaine | Situation au positionnement | Situation à l'évaluation finale | Déplacement |")
    add("|---|---|---|---|")
    for domain in scores:
        quadrant = domain_quadrant(diagnostic, domain)
        title, _posture, _method = QUADRANT_BY_KEY[quadrant]
        add(f"| {domain} | {title} | | |")
    add("")
    for heading in ("Progrès observés", "Notions encore fragiles", "Aides devenues inutiles",
                    "Recommandations pour septembre", "Avis de l'enseignant"):
        add(f"### {heading}")
        add("")
        add(ANSWER_LINE)
        add("")
    add("**Date :** ......................................  "
        "**Signature :** ......................................")
    add("")
    add("---")
    add(f"_Source pédagogique unique : `{module.source_document}`. Diagnostic issu du bilan de "
        f"positionnement du {diagnostic['date_bilan']} ; aucun contenu n'est extrapolé au-delà._")
    return "\n".join(out) + "\n"


def _remediation_exercises(diagnostic: dict, bank: list[dict]) -> list[dict[str, object]]:
    """Sélectionne les exercices du plan de remédiation, dans l'ordre de priorité.

    Un exercice par item manqué (la variante de la compétence exacte qui a échoué), puis un
    exercice par item réussi avec une certitude faible. La composition d'une feuille est donc
    entièrement déterminée par le profil de l'élève : deux élèves n'ont pas la même feuille.
    """
    priority_order = {domain: index for index, (domain, _q) in enumerate(worked_domains(diagnostic))}
    exercises: list[dict[str, object]] = []

    for rank, item, reference in items_to_revisit(diagnostic, bank):
        exercises.append({
            "rang_item": rank,
            "domaine": item["domaine"],
            "competence": reference["competence"],
            "motif": ("question laissée sans réponse"
                      if item["verdict"] in ("NON TRAITÉE", "NON TRAITÉ", "SANS RÉPONSE")
                      else "réponse fausse au positionnement"),
            "certitude": item["certitude_sur_4"],
            "origine_erreur": item["origine_erreur"],
            "enonce": reference["variante"],
            "corrige": reference["corrige_variante"],
            "geste": reference["geste_correct"],
            "tri": (0, priority_order.get(item["domaine"], 99), rank),
        })

    for rank, item, reference in items_to_secure(diagnostic, bank):
        exercises.append({
            "rang_item": rank,
            "domaine": item["domaine"],
            "competence": reference["competence"],
            "motif": (f"réussi avec une certitude de {item['certitude_sur_4']}/4"
                      if item["certitude_sur_4"] is not None
                      else "réussi, domaine classé en réussite hésitante"),
            "certitude": item["certitude_sur_4"],
            "origine_erreur": None,
            "enonce": reference["variante"],
            "corrige": reference["corrige_variante"],
            "geste": reference["geste_correct"],
            "tri": (1, priority_order.get(item["domaine"], 99), rank),
        })

    exercises.sort(key=lambda exercise: exercise["tri"])
    return exercises


def _remediation_header(student: dict, subject: dict, diagnostic: dict, module: Module,
                        audience: str) -> list[str]:
    lines = [
        f"# {module.label} — Plan de remédiation ciblée — {student['displayName']} ({audience})",
        f"## {subject['matiere']} — Parcours personnalisé",
        "",
        CONFIDENTIAL_BANNER,
        "",
        f"**Élève :** {student['displayName']}  ",
        f"**Matière :** {subject['matiere']}  ",
        f"**Diagnostic du :** {diagnostic['date_bilan']}  ",
        f"**Source :** `Bilans/{Path(diagnostic['source_pdf']).name}`",
        "",
    ]
    return lines


def render_remediation_eleve(student: dict, subject: dict, diagnostic: dict, instrument: dict,
                             module: Module, option: tuple[dict, dict] | None = None) -> str:
    exercises = _remediation_exercises(diagnostic, instrument["items"])
    option_exercises = (_remediation_exercises(option[0], option[1]["items"])
                        if option is not None else [])
    out = _remediation_header(student, subject, diagnostic, module, "Élève")
    add = out.append

    add("### Comment cette feuille a été construite")
    add("")
    if exercises:
        add("Chaque exercice ci-dessous reprend **une compétence précise** que ton "
            "positionnement a signalée. Ce n'est pas une feuille d'exercices générale : c'est "
            "la tienne. Les exercices sont classés dans l'ordre de tes priorités.")
    else:
        add("Ton positionnement ne signale aucune compétence à reprendre : ni réponse fausse, "
            "ni question laissée vide, ni réussite hésitante. Cette feuille propose donc un "
            "travail d'**approfondissement** plutôt qu'une remédiation.")
    add("")
    add("### Consignes")
    add("")
    add("- J'écris la propriété, la relation ou la précondition utilisée **avant** de calculer "
        "ou de coder.")
    add("- J'indique ma certitude de 1 à 4 pour chaque exercice.")
    add("- J'effectue un contrôle avant de déclarer une certitude de 4.")
    add("- Je ne consulte le corrigé qu'après une tentative complète.")
    add("")
    add("---")
    add("")

    if not exercises:
        add("## Travail d'approfondissement")
        add("")
        add("Ton positionnement est complet. Choisis **un** domaine parmi ceux que tu maîtrises "
            "et traite les deux tâches suivantes, qui portent sur ce que le positionnement ne "
            "mesurait pas : la rédaction et la justification.")
        add("")
        add("**Tâche 1 — Rédiger une démonstration.** Choisis une propriété que tu utilises "
            "souvent sans l'avoir démontrée. Écris sa démonstration complète, en justifiant "
            "chaque étape.")
        add("")
        add("Domaine choisi : ..........................................................")
        add("")
        for _ in range(6):
            add(ANSWER_LINE)
            add("")
        add("**Tâche 2 — Construire un contre-exemple.** Écris une affirmation plausible mais "
            "fausse dans ce domaine, puis le cas précis qui la réfute. Explique pourquoi ce cas "
            "est bien choisi.")
        add("")
        for _ in range(6):
            add(ANSWER_LINE)
            add("")
        add("Certitude : ☐1 ☐2 ☐3 ☐4   Aide utilisée : ☐A ☐B ☐C ☐D ☐E ☐aucune")
        add("")
    else:
        for number, exercise in enumerate(exercises, 1):
            add(f"## Exercice {number} — {exercise['domaine']}")
            add("")
            add(f"*Compétence visée : {exercise['competence']}.*")
            add("")
            add(f"**{exercise['enonce']}**")
            add("")
            add("Propriété, relation ou précondition utilisée :")
            add("")
            add(ANSWER_LINE)
            add("")
            add("Résolution :")
            add("")
            for _ in range(4):
                add(ANSWER_LINE)
                add("")
            add("Contrôle effectué : ☐oui ☐non — lequel ? ......................................")
            add("")
            add("Certitude : ☐1 ☐2 ☐3 ☐4   Aide utilisée : ☐A ☐B ☐C ☐D ☐E ☐aucune")
            add("")

    if option_exercises:
        intitule = student["optionAnnuelle"]["intitule"]
        add("<div class=\"page-break\"></div>")
        add("")
        add(f"## Exercices de l'option — {intitule}")
        add("")
        add("Ces exercices préparent l'option que tu suivras en Terminale. Ils se traitent "
            "sur le temps différencié, pas à la place du reste.")
        add("")
        for number, exercise in enumerate(option_exercises, 1):
            add(f"### Option, exercice {number} — {exercise['domaine']}")
            add("")
            add(f"*Compétence visée : {exercise['competence']}.*")
            add("")
            add(f"**{exercise['enonce']}**")
            add("")
            add("Propriété, relation ou précondition utilisée :")
            add("")
            add(ANSWER_LINE)
            add("")
            add("Résolution :")
            add("")
            for _ in range(4):
                add(ANSWER_LINE)
                add("")
            add("Certitude : ☐1 ☐2 ☐3 ☐4   Aide utilisée : ☐A ☐B ☐C ☐D ☐E ☐aucune")
            add("")

    add("---")
    add(f"_Source pédagogique unique : `{module.source_document}`._")
    return "\n".join(out) + "\n"


def render_remediation_prof(student: dict, subject: dict, diagnostic: dict, instrument: dict,
                            module: Module, option: tuple[dict, dict] | None = None) -> str:
    exercises = _remediation_exercises(diagnostic, instrument["items"])
    option_exercises = (_remediation_exercises(option[0], option[1]["items"])
                        if option is not None else [])
    domains = instrument["domaines"]
    out = _remediation_header(student, subject, diagnostic, module, "Corrigé enseignant")
    add = out.append

    add("## Profil de l'élève, en une page")
    add("")
    add("| Domaine | Réussite | Situation | Posture de travail |")
    add("|---|---:|---|---|")
    for domain, score in diagnostic["reussite_par_domaine"].items():
        quadrant = domain_quadrant(diagnostic, domain)
        title, posture, _method = QUADRANT_BY_KEY[quadrant]
        add(f"| {domain} | {format_percentage(score)} | {title} | **{posture}** |")
    add("")

    priorities = worked_domains(diagnostic)
    if priorities:
        add("**Ordre de traitement.** " + " → ".join(
            f"{domain} ({QUADRANT_BY_KEY[quadrant][1]})" for domain, quadrant in priorities))
    else:
        add("**Ordre de traitement.** Aucun domaine à reprendre : parcours "
            "d'approfondissement dès la séance 1, centré sur la rédaction et la "
            "justification — ce que le positionnement ne mesure pas.")
    add("")
    if diagnostic["auto_evaluation"]:
        add(f"**Calibration de la confiance.** {diagnostic['auto_evaluation']}")
        add("")

    add("## Composition de la feuille")
    add("")
    if exercises:
        add("| # | Item du positionnement | Domaine | Compétence | Motif de sélection |")
        add("|---:|---:|---|---|---|")
        for number, exercise in enumerate(exercises, 1):
            add(f"| {number} | item {exercise['rang_item']} | {exercise['domaine']} | "
                f"{exercise['competence']} | {exercise['motif']} |")
        add("")
        add("Chaque exercice est la **variante** de l'item que l'élève a manqué ou réussi sans "
            "assurance : même compétence, énoncé différent. La feuille d'un autre élève n'a "
            "donc pas la même composition.")
    else:
        add("Aucun item manqué ni réussi avec une certitude faible : la feuille propose deux "
            "tâches d'approfondissement (démonstration rédigée, construction d'un "
            "contre-exemple).")
    add("")

    add("<div class=\"page-break\"></div>")
    add("")
    add("## Corrigé")
    add("")
    if not exercises:
        add("**Tâche 1 — Démonstration rédigée.** Il n'y a pas de corrigé unique : ce qui est "
            "évalué est la chaîne des justifications. Exiger que chaque étape soit reliée à une "
            "propriété nommée, et refuser tout « on voit que ».")
        add("")
        add("**Tâche 2 — Contre-exemple.** Vérifier trois points : l'affirmation proposée est "
            "bien plausible (sinon la tâche est vide de sens) ; le cas produit la réfute "
            "réellement ; l'élève sait dire **pourquoi** un autre cas n'aurait pas convenu. Ce "
            "troisième point est le plus formateur — c'est celui que la séance 2 du module de "
            "mathématiques travaille avec le test en x = 1.")
        add("")
    else:
        for number, exercise in enumerate(exercises, 1):
            add(f"### Exercice {number} — {exercise['domaine']}")
            add("")
            add(f"**Énoncé.** {exercise['enonce']}")
            add("")
            add(f"**Corrigé.** {exercise['corrige']}")
            add("")
            add(f"**Geste à installer.** {exercise['geste']}")
            add("")
            if exercise["origine_erreur"]:
                add(f"**Erreur à surveiller chez cet élève.** {exercise['origine_erreur']} "
                    f"(constatée à l'item {exercise['rang_item']} du positionnement"
                    + (f", donné avec une certitude de {exercise['certitude']}/4"
                       if exercise["certitude"] is not None else "") + ".)")
            elif exercise["motif"].startswith("question laissée"):
                add("**Point de vigilance.** L'item correspondant est resté sans réponse : ne "
                    "rien conclure du silence. Faire traiter l'exercice en observation, puis "
                    "décider de la suite à partir de ce qui est effectivement produit.")
            else:
                add("**Point de vigilance.** L'item était réussi mais avec une certitude "
                    "faible : l'objectif est la **vitesse et l'assurance**, pas la "
                    "compréhension. Ne pas réenseigner ; faire refaire à intervalle espacé.")
            add("")

    add("## Relevé de maîtrise")
    add("")
    count = max(len(exercises), 2)
    add("| Exercice | Juste sans aide | Juste avec aide | Erreur de procédure | Erreur de calcul | À reprendre |")
    add("|---:|:---:|:---:|:---:|:---:|:---:|")
    for number in range(1, count + 1):
        add(f"| {number} | ☐ | ☐ | ☐ | ☐ | ☐ |")
    add("")

    add("## Conduite recommandée")
    add("")
    if priorities:
        for domain, quadrant in priorities:
            _title, posture, method = QUADRANT_BY_KEY[quadrant]
            opening = domains.get(domain, {}).get("ouverture_terminale", "")
            add(f"### {domain} — {posture}")
            add("")
            add(method)
            add("")
            if opening:
                add(f"**Argument à donner à l'élève.** {opening}")
                add("")
    else:
        add("Cet élève ne relève d'aucune remédiation. Deux écueils à éviter : le laisser sans "
            "tâche pendant les temps différenciés, et lui confier l'explication d'une notion à "
            "un camarade porteur d'une certitude erronée — la confrontation demande un pilotage "
            "que seul l'enseignant peut assurer.")
        add("")
        add("Trois usages utiles de son temps : la **piste excellence** de chaque séance, "
            "c'est-à-dire les exercices 9 et 10 de la fiche élève ; le rôle de "
            "**vérificateur** (relire la rédaction d'un camarade et dire si la propriété a "
            "été écrite avant le calcul, sans donner la réponse) ; la rédaction de "
            "démonstrations, que le positionnement ne mesure pas.")
        add("")

    if option_exercises:
        intitule = student["optionAnnuelle"]["intitule"]
        add("<div class=\"page-break\"></div>")
        add("")
        add(f"## Option — {intitule}")
        add("")
        add("Cette option ne fait l'objet d'aucun stage : elle se prépare sur le temps "
            "différencié du stage de mathématiques, à raison de vingt minutes par séance.")
        add("")
        add("| # | Item du positionnement | Domaine | Compétence | Motif de sélection |")
        add("|---:|---:|---|---|---|")
        for number, exercise in enumerate(option_exercises, 1):
            add(f"| {number} | item {exercise['rang_item']} | {exercise['domaine']} | "
                f"{exercise['competence']} | {exercise['motif']} |")
        add("")
        for number, exercise in enumerate(option_exercises, 1):
            add(f"### Option, exercice {number} — {exercise['domaine']}")
            add("")
            add(f"**Énoncé.** {exercise['enonce']}")
            add("")
            add(f"**Corrigé.** {exercise['corrige']}")
            add("")
            add(f"**Geste à installer.** {exercise['geste']}")
            add("")
            if exercise["origine_erreur"]:
                add(f"**Erreur à surveiller chez cet élève.** {exercise['origine_erreur']} "
                    f"(item {exercise['rang_item']} du positionnement d'option.)")
                add("")

    add("## Décision de fin de parcours")
    add("")
    add("| Domaine | Situation initiale | Situation finale | Décision pour septembre |")
    add("|---|---|---|---|")
    for domain in diagnostic["reussite_par_domaine"]:
        quadrant = domain_quadrant(diagnostic, domain)
        title, _posture, _method = QUADRANT_BY_KEY[quadrant]
        add(f"| {domain} | {title} | | |")
    add("")
    add("---")
    add(f"_Document enseignant. Source pédagogique unique : `{module.source_document}`._")
    return "\n".join(out) + "\n"


def render_missing_subject_notice(student: dict, missing: dict, module: Module,
                                  group: dict, frame: dict) -> str:
    """Livret d'un élève dont le positionnement de cette matière n'a pas été passé.

    On ne produit pas un livret vide, et on n'invente rien : le document dit explicitement
    ce qui manque, et organise le diagnostic de la séance 1.
    """
    name = student["displayName"]
    out: list[str] = []
    add = out.append

    add(f"# {module.label} — Livret individuel — {name}")
    add(f"## {missing['matiere']} — Diagnostic à établir")
    add("")
    add(CONFIDENTIAL_BANNER)
    add("")
    add(f"**Élève :** {name}  ")
    add(f"**Groupe :** {group['libelle']}  ")
    add(f"**Spécialités conservées :** {', '.join(specialites(student, group))}  ")
    add(f"**Matière de ce livret :** {missing['matiere']}  ")
    add(f"**Organisme :** {frame['organisme']} — {frame['natureOrganisme'].lower()}  ")
    add(f"**Stage :** {frame['dureeParSpecialite']}, {frame['rythme']}  ")
    add(f"**Dates :** {frame['dates']}  ")
    add("**Année scolaire préparée :** 2026-2027")
    add("")
    if student.get("noteGroupe"):
        add(f"> **Rattachement au groupe.** {student['noteGroupe']}")
        add("")
    if student.get("homonymeAvertissement"):
        add(f"> **Attention — homonymie.** {student['homonymeAvertissement']}")
        add("")

    add("---")
    add("")
    add("## 1. Pourquoi ce livret est différent des autres")
    add("")
    add(missing["motif"])
    add("")
    add("Les autres livrets de la cohorte reprennent, item par item, les erreurs effectivement "
        "commises au positionnement. Ici, il n'y a pas de positionnement à reprendre.")
    add("")
    add("**Aucune conclusion n'est donc formulée à la place de l'élève.** Ni point fort, ni "
        "priorité, ni parcours : tout cela se décide après le diagnostic de la séance 1.")
    add("")

    add("## 2. Le diagnostic de la séance 1")
    add("")
    add("Un positionnement est passé en début de séance 1, dans les mêmes conditions que celui "
        "de la cohorte : mêmes items, même déclaration de certitude de 1 à 4.")
    add("")
    add("| Étape | Quand | Qui |")
    add("|---|---|---|")
    add("| Passation du positionnement (18 items) | Séance 1, 25 premières minutes | Élève |")
    add("| Dépouillement et report ci-dessous | Séance 1, pendant l'entraînement différencié | Enseignant |")
    add("| Attribution du parcours de la séance 2 | Fin de séance 1 | Enseignant |")
    add("| Livret complété à l'identique des autres | Avant la séance 2 | Enseignant |")
    add("")
    add("En attendant, l'élève suit le **parcours maîtrise** de la séance 1 : c'est le parcours "
        "médian, qui n'anticipe ni un niveau élevé ni des lacunes.")
    add("")

    add("## 3. Grille de report du diagnostic")
    add("")
    add("À remplir en séance 1, puis à reporter dans un livret complet.")
    add("")
    add("| Domaine | Réussite | Certitude moyenne | Situation dans la matrice |")
    add("|---|---:|---:|---|")
    for domain in ("Second degré", "Dérivation", "Fonction exponentielle",
                   "Suites numériques", "Produit scalaire"):
        add(f"| {domain} | | | |")
    add("")
    add("**Matrice de lecture, identique à celle des autres livrets :**")
    add("")
    add("| | Certitude faible (1-2) | Certitude forte (3-4) |")
    add("|---|---|---|")
    add("| **Réponse fausse** | Notion absente → on installe | Conception erronée → on confronte |")
    add("| **Réponse juste** | Acquis fragile → on consolide | Acquis disponible → on entretient |")
    add("")

    add("## 4. Parcours prévisionnel")
    add("")
    add("| Séance | Thème commun du stage | Focus personnel | Parcours |")
    add("|---:|---|---|---|")
    for number, theme in module.sessions:
        focus = "Diagnostic initial" if number == 1 else "à définir après la séance 1"
        parcours = "Installer (par défaut)" if number == 1 else "à définir"
        add(f"| {number} | {theme} | {focus} | {parcours} |")
    add("")

    add("## 5. Fiches de suivi")
    add("")
    add("| Observation | S1 | S2 | S3 | S4 | S5 |")
    add("|---|:---:|:---:|:---:|:---:|:---:|")
    for observation in ("Procédure choisie", "Exactitude", "Justification écrite",
                        "Contrôle effectué", "Certitude cohérente"):
        add(f"| {observation} | | | | | |")
    add("")
    add("| Séance | 1 | 2 | 3 | 4 | 5 |")
    add("|---|:---:|:---:|:---:|:---:|:---:|")
    add("| Aide maximale utilisée | | | | | |")
    add("")

    add("## 6. Bilan final")
    add("")
    for heading in ("Progrès observés", "Notions encore fragiles",
                    "Recommandations pour septembre", "Avis de l'enseignant"):
        add(f"### {heading}")
        add("")
        add(ANSWER_LINE)
        add("")
    add("**Date :** ......................................  "
        "**Signature :** ......................................")
    add("")
    add("---")
    add(f"_Source pédagogique unique : `{module.source_document}`. Ce livret ne comporte aucun "
        "diagnostic reporté : il en organise l'établissement._")
    return "\n".join(out) + "\n"


def render_dashboard(module: Module, entries: list[dict]) -> str:
    """Tableau de bord enseignant du module. Nominatif, donc confidentiel."""
    out: list[str] = []
    add = out.append

    add(f"# {module.label} — Tableau de bord enseignant")
    add("## Suivi collectif du stage de pré-rentrée 2026-2027")
    add("")
    add("> **DOCUMENT CONFIDENTIEL — DONNÉES NOMINATIVES**  ")
    add("> Ce tableau réunit les diagnostics de plusieurs élèves mineurs. Il ne sort pas du "
        "dossier pédagogique de l'enseignant et n'est jamais remis à une famille : chaque "
        "famille reçoit le livret de son enfant, et lui seul.")
    add("")

    add("## 1. Le groupe en une page")
    add("")
    add("| Élève | Matière | Réussite globale | Certitudes à revoir | À installer | À consolider | Acquis |")
    add("|---|---|---:|---|---|---|---|")
    for entry in entries:
        diagnostic = entry["diagnostic"]
        if diagnostic is None:
            add(f"| {entry['name']} | {entry['matiere']} | _non passé_ | — | — | — | — |")
            continue
        scores = diagnostic["reussite_par_domaine"]
        overall = sum(scores.values()) / len(scores)
        card = diagnostic["carte_maitrise_confiance"]

        def listed(key: str) -> str:
            values = card.get(key, [])
            return ", ".join(values) if values else "—"

        add(f"| {entry['name']} | {entry['matiere']} | {format_percentage(overall)} | "
            f"{listed('certitudes_a_revoir')} | {listed('a_installer')} | "
            f"{listed('a_consolider')} | {listed('acquis')} |")
    add("")

    add("## 2. Réussite par domaine")
    add("")
    domains: list[str] = []
    for entry in entries:
        if entry["diagnostic"] is None:
            continue
        for domain in entry["diagnostic"]["reussite_par_domaine"]:
            if domain not in domains:
                domains.append(domain)
    if domains:
        header = "| Élève | " + " | ".join(domains) + " |"
        add(header)
        add("|---|" + "---:|" * len(domains))
        for entry in entries:
            diagnostic = entry["diagnostic"]
            if diagnostic is None:
                add(f"| {entry['name']} | " + " | ".join("—" for _ in domains) + " |")
                continue
            cells = []
            for domain in domains:
                score = diagnostic["reussite_par_domaine"].get(domain)
                cells.append(format_percentage(score) if score is not None else "—")
            add(f"| {entry['name']} | " + " | ".join(cells) + " |")
        add("")

    add("## 3. Attribution des parcours, séance par séance")
    add("")
    add("À relire avant chaque séance. Un même élève change de parcours d'une séance à l'autre : "
        "c'est le cas le plus fréquent, pas l'exception.")
    add("")
    for number, theme in module.sessions:
        add(f"### Séance {number} — {theme}")
        add("")
        add("| Élève | Focus personnel | Parcours | Aide maximale | Erreur dominante | Décision pour la suite |")
        add("|---|---|---|---|---|---|")
        for entry in entries:
            diagnostic = entry["diagnostic"]
            if diagnostic is None:
                add(f"| {entry['name']} | Diagnostic en cours | Installer (par défaut) | | | |")
                continue
            row = next(r for r in session_focus(diagnostic, module) if r["seance"] == number)
            add(f"| {entry['name']} | {row['focus']} | {row['parcours']} | | | |")
        add("")

    add("## 4. Relevé de l'autonomie")
    add("")
    add("L'aide maximale utilisée doit décroître entre la séance 1 et la séance 5.")
    add("")
    add("| Élève | S1 | S2 | S3 | S4 | S5 | Décroissance observée |")
    add("|---|:---:|:---:|:---:|:---:|:---:|:---:|")
    for entry in entries:
        add(f"| {entry['name']} | | | | | | ☐oui ☐non |")
    add("")

    add("## 5. Critères de réussite du stage")
    add("")
    add("| Élève | Plus de certitude erronée | Propriété écrite avant calcul | Contrôle systématique | Aide en baisse | Plan de septembre rempli |")
    add("|---|:---:|:---:|:---:|:---:|:---:|")
    for entry in entries:
        add(f"| {entry['name']} | ☐ | ☐ | ☐ | ☐ | ☐ |")
    add("")
    add("## 6. Accès aux dossiers nominatifs")
    add("")
    add("Ces liens sont volontairement absents de l'index du module : celui-ci ne nomme aucun "
        "élève, et c'est ici que se fait la navigation nominative.")
    add("")
    for entry in entries:
        base = f"../{module.nominative_dir}/{entry['slug']}"
        suffix = entry["file_suffix"]
        links = [f"[livret]({base}/{module.key}_Livret_Individuel_{suffix}.md)"]
        if entry["diagnostic"] is not None:
            links.append(
                f"[remédiation élève]({base}/{module.key}_Remediation_Ciblee_{suffix}_ELEVE.md)")
            links.append(
                f"[corrigé enseignant]({base}/{module.key}_Remediation_Ciblee_{suffix}_PROF_Corrige.md)")
        label = entry["name"]
        if entry["matiere"] != module.subject_label:
            label += f" — {entry['matiere']}"
        add(f"- **{label}** : " + " · ".join(links))
    add("")
    add("---")
    add(f"_Document enseignant nominatif. Source pédagogique unique : `{module.source_document}`._")
    return "\n".join(out) + "\n"


def render_index(module: Module, entries: list[dict]) -> str:
    out: list[str] = []
    add = out.append
    add(f"# Index — {module.label}")
    add("")
    add("## Documents généraux")
    add("")
    add(f"- [Documentation d'ensemble du stage](./{module.key}_MASTER_Documentation_Stage.md)")
    if module.key == "tle_nsi":
        add(f"- [Programme du stage (présentation aux familles)](./{module.key}_Programme_Stage_PUBLIC.md)")
        add(f"- [Démarrage rapide](./{module.key}_QUICK_START.md)")
    add(f"- [Guide du formateur](../01_ENSEIGNANT/{module.key}_Guide_Formateur.md)")
    add(f"- [Tableau de bord enseignant](../01_ENSEIGNANT/{module.key}_Tableau_Bord_Enseignant.md) "
        "— **confidentiel**")
    if module.key == "tle_spe":
        add(f"- [Module mathématiques expertes](../01_ENSEIGNANT/{module.key}_Option_Maths_Expertes.md)")
    add("")

    add("## Séances")
    add("")
    supports = "SUPPORTS_Pratiques" if module.key == "tle_nsi" else "SUPPORTS_Manipulation"
    for number, theme in module.sessions:
        add(f"### Séance {number} — {theme}")
        add("")
        add(f"- [Fiche professeur](../02_SEANCES/S{number}/{module.key}_S{number}_PROF_Fiche.md)")
        add(f"- [Fiche élève](../02_SEANCES/S{number}/{module.key}_S{number}_ELEVE_Activite.md)")
        add(f"- [Supports](../02_SEANCES/S{number}/{module.key}_S{number}_{supports}.md)")
        add(f"- [Cartes d'aide](../02_SEANCES/S{number}/{module.key}_S{number}_AIDES_Cartes.md)")
        add("")

    add("## Évaluations")
    add("")
    if module.key == "tle_spe":
        add(f"- [Mini-diagnostic élève](../03_EVALUATIONS/{module.key}_Mini_Diagnostic_ELEVE.md)")
        add(f"- [Mini-diagnostic corrigé](../03_EVALUATIONS/{module.key}_Mini_Diagnostic_PROF_Corrige.md)")
    else:
        add(f"- [Mini-diagnostic pratique élève](../03_EVALUATIONS/{module.key}_Mini_Diagnostic_Pratique_ELEVE.md)")
        add(f"- [Mini-diagnostic pratique corrigé](../03_EVALUATIONS/{module.key}_Mini_Diagnostic_Pratique_PROF_Corrige.md)")
    add(f"- [Évaluation finale élève](../03_EVALUATIONS/{module.key}_Evaluation_Finale_ELEVE.md)")
    add(f"- [Évaluation finale corrigée](../03_EVALUATIONS/{module.key}_Evaluation_Finale_PROF_Corrige_Bareme.md)")
    if module.key == "tle_spe":
        add(f"- [Portfolio du stage](../03_EVALUATIONS/{module.key}_Portfolio_Individuel.md)")
    else:
        add(f"- [Mémento Python](../04_PORTFOLIO/{module.key}_Memento_Python_Terminale_ELEVE.md)")
        add(f"- [Portfolio du stage](../04_PORTFOLIO/{module.key}_Portfolio_Individuel.md)")
    add("")

    if module.key == "tle_nsi":
        add("## Code")
        add("")
        add("- [Scripts des cinq séances](../06_CODE/README_CODE.md)")
        add("")

    add("## Source pédagogique")
    add("")
    sources_dir = "07_SOURCES" if module.key == "tle_nsi" else "05_SOURCES"
    add(f"- [Programme complet du stage](../{sources_dir}/{module.source_document})")
    add("")

    add("## Dossiers nominatifs")
    add("")
    add(f"Le dossier `{module.nominative_dir}/` contient, pour chaque élève, son livret "
        "individuel et son plan de remédiation en deux versions.")
    add("")
    add("> **Ces documents portent des données personnelles d'élèves mineurs.** Cet index ne "
        "les nomme pas : la liste et les liens figurent dans le "
        f"[tableau de bord enseignant](../01_ENSEIGNANT/{module.key}_Tableau_Bord_Enseignant.md), "
        "qui est lui-même confidentiel. Ne jamais placer un document nominatif dans un pack "
        "collectif, ni le remettre à un autre élève du groupe.")
    add("")
    add(f"_{len(entries)} dossier(s) nominatif(s) dans ce module._")
    add("")
    return "\n".join(out) + "\n"


def build_documents(root: Path = ROOT) -> dict[str, str]:
    """Construit tous les documents nominatifs. Retourne {chemin relatif: contenu}."""
    registry = load_json(root, REGISTRY_PATH)
    diagnostics = load_json(root, DIAGNOSTICS_PATH)
    items = load_json(root, ITEMS_PATH)
    check_sources(registry, diagnostics, items)

    groups = {group["id"]: group for group in registry["groupes"]}
    frame = stage_frame(registry)
    documents: dict[str, str] = {}
    module_entries: dict[str, list[dict]] = {key: [] for key in MODULES}

    for student in registry["students"]:
        if not student.get("active", True):
            continue
        group = groups[student["groupe"]]

        # L'option annuelle n'a pas de stage : son diagnostic complète le livret de la
        # spécialité correspondante au lieu de produire un document séparé.
        option_entry = student.get("optionAnnuelle")
        option = None
        if option_entry is not None:
            option = (
                diagnostics["diagnostics"][option_entry["diagnosticId"]],
                items["instruments"][option_entry["intitule"]],
            )

        for subject in student["matieres"]:
            module = MODULES[subject["module"]]
            diagnostic = diagnostics["diagnostics"][subject["diagnosticId"]]
            instrument = items["instruments"][subject["matiere"]]
            suffix = student["slug"]
            attached = option if module.key == "tle_spe" else None

            directory = f"{module.key}/{module.nominative_dir}/{student['slug']}"
            documents[f"{directory}/{module.key}_Livret_Individuel_{suffix}.md"] = (
                render_livret(student, subject, diagnostic, instrument, module, group,
                              frame, attached)
            )
            documents[f"{directory}/{module.key}_Remediation_Ciblee_{suffix}_ELEVE.md"] = (
                render_remediation_eleve(student, subject, diagnostic, instrument, module,
                                         attached)
            )
            documents[f"{directory}/{module.key}_Remediation_Ciblee_{suffix}_PROF_Corrige.md"] = (
                render_remediation_prof(student, subject, diagnostic, instrument, module,
                                        attached)
            )
            module_entries[module.key].append({
                "name": student["displayName"],
                "slug": student["slug"],
                "file_suffix": suffix,
                "matiere": subject["matiere"],
                "diagnostic": diagnostic,
            })

        option = student.get("optionAnnuelle")
        if option is not None:
            if option["diagnosticId"] not in diagnostics["diagnostics"]:
                errors.append(
                    f"{where} : diagnostic d'option introuvable '{option['diagnosticId']}'"
                )
            elif option["intitule"] not in items["instruments"]:
                errors.append(f"{where} : aucun instrument pour '{option['intitule']}'")

        for missing in student.get("matieresSansDiagnostic", []):
            module = MODULES[missing["module"]]
            suffix = student["slug"]
            directory = f"{module.key}/{module.nominative_dir}/{student['slug']}"
            documents[f"{directory}/{module.key}_Livret_Individuel_{suffix}.md"] = (
                render_missing_subject_notice(student, missing, module, group, frame)
            )
            module_entries[module.key].append({
                "name": student["displayName"],
                "slug": student["slug"],
                "file_suffix": suffix,
                "matiere": missing["matiere"],
                "diagnostic": None,
            })

    for key, module in MODULES.items():
        entries = module_entries[key]
        if not entries:
            continue
        documents[f"{key}/01_ENSEIGNANT/{key}_Tableau_Bord_Enseignant.md"] = (
            render_dashboard(module, entries)
        )
        documents[f"{key}/00_MASTER/index.md"] = render_index(module, entries)

    # Le texte des bilans est repris tel qu'il a été extrait des PDF : il porte encore la
    # notation Unicode des sujets d'origine (u₀, ≥, Cu²⁺). La conversion en LaTeX se fait
    # ici, sur le document complet, pour que les livrets composés par LuaLaTeX portent de
    # vraies mathématiques et de vraies équations de réaction.
    return {
        relative: to_latex(content, chemistry=relative.startswith("tle_pc/"))
        for relative, content in documents.items()
    }


def orphan_documents(documents: dict[str, str], root: Path = ROOT) -> list[str]:
    """Documents nominatifs présents sur le disque mais que la génération ne produit plus.

    Un élève retiré de la cohorte, une matière fondue dans une autre : sans ce contrôle,
    ses documents resteraient sur le disque et pourraient être imprimés ou distribués. Ce
    sont des données personnelles de mineurs — un fichier périmé n'est pas un détail.
    """
    expected = set(documents)
    orphans: list[str] = []
    for module in MODULES.values():
        nominative = root / module.key / module.nominative_dir
        if not nominative.exists():
            continue
        for path in sorted(nominative.rglob("*.md")):
            relative = path.relative_to(root).as_posix()
            if relative not in expected:
                orphans.append(relative)
    return orphans


def empty_student_directories(root: Path = ROOT) -> list[str]:
    """Répertoires nominatifs vidés de leurs documents, à supprimer."""
    empties: list[str] = []
    for module in MODULES.values():
        nominative = root / module.key / module.nominative_dir
        if not nominative.exists():
            continue
        for entry in sorted(nominative.iterdir()):
            if entry.is_dir() and not any(entry.glob("*.md")):
                empties.append(entry.relative_to(root).as_posix())
    return empties


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="échoue si un document committé diffère de la génération")
    args = parser.parse_args(argv)

    try:
        documents = build_documents()
    except BuildError as error:
        print(f"ÉCHEC : {error}")
        return 1

    if args.check:
        stale: list[str] = []
        for relative, content in sorted(documents.items()):
            path = ROOT / relative
            if not path.exists():
                stale.append(f"{relative} : absent")
            elif path.read_text(encoding="utf-8") != content:
                stale.append(f"{relative} : périmé")
        stale += [f"{relative} : orphelin, à supprimer" for relative in orphan_documents(documents)]
        stale += [f"{relative} : répertoire vide, à supprimer" for relative in empty_student_directories()]
        if stale:
            print("ÉCHEC : documents nominatifs non à jour.")
            for line in stale:
                print(f"  - {line}")
            return 1
        print(f"OK : les {len(documents)} documents nominatifs Terminale sont à jour.")
        return 0

    for relative, content in sorted(documents.items()):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    # Les orphelins sont supprimés, pas seulement signalés : laisser sur le disque le
    # livret d'un élève retiré de la cohorte, c'est risquer de l'imprimer.
    removed = orphan_documents(documents)
    for relative in removed:
        (ROOT / relative).unlink()
    emptied = empty_student_directories()
    for relative in emptied:
        (ROOT / relative).rmdir()

    print(f"Écrit {len(documents)} documents nominatifs Terminale.")
    for relative in removed:
        print(f"  supprimé (orphelin) : {relative}")
    for relative in emptied:
        print(f"  supprimé (répertoire vide) : {relative}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
