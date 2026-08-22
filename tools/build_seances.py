"""Cahier de séances nominatif : les cinq séances d'un élève, écrites pour lui.

Les fiches de séance étaient collectives. Un élève y trouvait les huit exercices du groupe,
dont quatre ne le concernaient pas, et devait ouvrir son livret pour savoir lesquels étaient
les siens. Ce module produit à la place un cahier par élève et par matière : la même
progression commune, mais avec son objectif, son diagnostic, ses exercices, ses pièges et
son bilan.

Rien n'est recopié. Les énoncés viennent des fiches collectives, qui restent la source
unique ; les exemples résolus viennent des cartes d'aide ; l'exercice personnel vient de la
banque d'items, qui l'a déjà apparié à l'erreur exacte de l'élève ; les automatismes, la
méthode, les pièges, le transfert et la question de sortie viennent de `seance_bank`. Le
cahier assemble, il n'invente pas.
"""
from __future__ import annotations

import re
from pathlib import Path

from seance_bank import BANK, COMPLEMENTS

# Le titre de section qui ouvre le bloc d'exercices de chaque piste, dans les fiches
# collectives. Les pistes de diagnostic partagent la première plage : un élève qui n'a pas
# répondu et un élève sûr de lui et faux traitent les mêmes exercices, avec un étayage
# différent — c'est la conduite du professeur qui les sépare, pas l'énoncé.
PISTE_BLOCKS = {
    "Diagnostiquer": "Exercices 1 à 4",
    "Confronter": "Exercices 1 à 4",
    "Installer": "Exercices 1 à 4",
    "Consolider": "Exercices 3 à 6",
    "Entretenir": "Exercices 6 à 8",
    "Excellence": "piste Excellence",
}

# L'étayage dépend de la posture, pas du niveau supposé. Un élève sûr de lui et faux a
# besoin qu'on mette sa conviction en défaut avant tout exemple ; un élève lucide sur ce qui
# lui manque a besoin de l'exemple tout de suite ; un élève qui réussit sans assurance doit
# s'en passer, c'est précisément l'objet du travail. Sans cette table, les quatre élèves de
# maths qui partagent la même plage d'exercices recevaient quatre cahiers identiques à leur
# exercice personnel près.
ETAYAGE = {
    # posture: (exemple résolu, indices gradués, confrontation préalable, rédaction exigée)
    "Diagnostiquer": (True, True, False, False),
    "Confronter": (True, True, True, False),
    "Installer": (True, True, False, False),
    "Consolider": (False, True, False, True),
    "Entretenir": (False, False, False, True),
    "Excellence": (False, False, False, True),
}

# Indices gradués : on ne donne pas la solution, on donne de quoi repartir. La distinction
# entre « je ne savais pas » et « il me manquait un déclencheur » ne se lit que si l'élève
# note quel indice il a ouvert.
INDICES = (
    "**Indice 1 — orientation.** Relis l'énoncé et demande-toi de quel domaine il relève. "
    "Écris le nom de la propriété avant toute chose.",
    "**Indice 2 — méthode.** Reprends la méthode de la page précédente, étape par étape, et "
    "applique la première à ton énoncé.",
    "**Indice 3 — première étape.** Pose l'écriture de départ, sans la résoudre. Si tu y "
    "arrives, la suite t'appartient.",
)

# Ce que chaque piste exige de l'élève, en une phrase, à afficher en tête de son entraînement.
PISTE_EXIGENCE = {
    "Diagnostiquer": "Réponds même sans être sûr. Déclarer une certitude de 1 est une "
                     "réponse : c'est elle qui dira au professeur par où reprendre.",
    "Confronter": "Écris d'abord ce que tu croyais, puis ce qui l'a mis en défaut. C'est "
                  "cette trace-là qui empêche l'erreur de revenir.",
    "Installer": "Écris la propriété ou la relation que tu utilises **avant** de calculer.",
    "Consolider": "Justifie par écrit, et sans carte d'aide. Tu sais faire ; il reste à le "
                  "faire sans hésiter.",
    "Entretenir": "Rédige la démonstration en entier, pas seulement le calcul.",
    "Excellence": "Produis une rédaction complète, puis relis la copie d'un camarade sans "
                  "lui donner la réponse.",
}


class SheetError(RuntimeError):
    """La fiche collective n'a pas la structure attendue."""


def _sections(text: str) -> list[tuple[int, str, str]]:
    """Découpe un document en (niveau, titre, corps), en ignorant les blocs de code."""
    lines = text.split("\n")
    found: list[tuple[int, str, int]] = []
    fenced = False
    for index, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
        if fenced or not line.startswith("#"):
            continue
        level = len(line) - len(line.lstrip("#"))
        found.append((level, line.lstrip("#").strip(), index))
    out = []
    for position, (level, title, start) in enumerate(found):
        stop = found[position + 1][2] if position + 1 < len(found) else len(lines)
        out.append((level, title, "\n".join(lines[start + 1:stop]).strip("\n")))
    return out


def _body(sections, predicate) -> str | None:
    for _level, title, body in sections:
        if predicate(title):
            return body.strip()
    return None


def read_sheet(module: str, session: int, root: Path) -> dict[str, str]:
    """Extrait d'une fiche collective les morceaux réutilisables."""
    path = root / module / "02_SEANCES" / f"S{session}" / f"{module}_S{session}_ELEVE_Activite.md"
    if not path.exists():
        raise SheetError(f"fiche collective introuvable : {path}")
    sections = _sections(path.read_text(encoding="utf-8"))
    parts: dict[str, str] = {}

    theme = next((title for level, title, _ in sections if level == 2), None)
    if theme is None:
        raise SheetError(f"{path} : aucun titre de niveau 2")
    parts["theme"] = theme

    spontanee = _body(sections, lambda t: "réponse spontanée" in t)
    if spontanee:
        parts["spontanee"] = spontanee
    trace = _body(sections, lambda t: "La trace écrite" in t)
    if trace:
        parts["trace"] = trace
    terminale = _body(sections, lambda t: "Terminale en fera" in t)
    if terminale:
        parts["terminale"] = terminale
    option = _body(sections, lambda t: t.startswith(("Ouverture maths expertes",
                                                     "Atelier Terminale")))
    if option:
        parts["option"] = option
        parts["option_titre"] = next(
            title for _l, title, _b in sections
            if title.startswith(("Ouverture maths expertes", "Atelier Terminale"))
        )

    for piste, marker in PISTE_BLOCKS.items():
        body = _body(sections, lambda t, m=marker: m in t)
        if body:
            parts[f"piste:{piste}"] = body

    # Les séances 5 ne sont pas découpées en pistes : elles enchaînent plusieurs domaines
    # puis l'évaluation. Leurs parties thématiques sont reprises telles quelles.
    parts["thematiques"] = "\n\n".join(
        f"### {title}\n\n{body}" for level, title, body in sections
        if level == 2 and title.startswith("Partie ") and "Bilan" not in title
        and "Entraînement" not in title and "réponse spontanée" not in title
        and "trace écrite" not in title and "Terminale en fera" not in title
    ).strip()
    return parts


def read_worked_example(module: str, session: int, root: Path) -> str | None:
    """La carte C des aides graduées : un exemple résolu, à transposer."""
    path = root / module / "02_SEANCES" / f"S{session}" / f"{module}_S{session}_AIDES_Cartes.md"
    if not path.exists():
        return None
    return _body(_sections(path.read_text(encoding="utf-8")),
                 lambda title: title.startswith("Carte C"))


def _numbered(items: list[str]) -> list[str]:
    return [f"{position}. {item}" for position, item in enumerate(items, 1)]


ANSWER = "." * 100


def _short_answers(count: int) -> list[str]:
    return [line for _ in range(count) for line in (ANSWER, "")]


# Un élève qui réussit déjà les deux tiers d'un domaine n'a pas besoin de refaire
# l'application directe : il a besoin du reste de la série. Un élève à moins de 40 % la
# refait, parce que c'est là que se joue l'accès. Le seuil ne retire aucun objectif, il
# décale le point d'entrée — les exercices sautés restent dans la fiche collective, et le
# professeur peut les redonner s'il constate le contraire en séance.
def entry_point(reussite: float | None) -> int:
    """Nombre d'exercices d'accès à passer, d'après la réussite au positionnement."""
    if reussite is None or reussite < 40:
        return 0
    if reussite < 70:
        return 1
    return 2


EXERCISE = re.compile(r"^\*\*Exercice \d+\.\*\*", re.M)


def trim_exercises(block: str, skip: int) -> tuple[str, int]:
    """Retire les `skip` premiers exercices d'un bloc. Rend le bloc et le nombre retiré."""
    starts = [match.start() for match in EXERCISE.finditer(block)]
    if skip <= 0 or len(starts) <= skip + 1:
        return block, 0
    return block[:starts[0]] + block[starts[skip]:], skip


def render_seance(number: int, theme: str, row: dict, parts: dict[str, str],
                  module: str, student_name: str, personals: list[dict],
                  option_ouverte: bool, reactivation_differee: str | None,
                  reussite: float | None = None, intersession: str | None = None,
                  appui: str | None = None) -> list[str]:
    """Une séance du cahier, dans l'ordre où elle se déroule."""
    piste = str(row["parcours"])
    bank = BANK[(module, number)]
    extra = COMPLEMENTS[(module, number)]
    exemple_donne, indices_donnes, confrontation, redaction = ETAYAGE[piste]
    out: list[str] = []
    add = out.append

    focus = str(row["focus"])
    domaine = focus.split(" (")[0]
    # Le point personnel porte-t-il sur le thème du jour, ou sur un autre domaine traité
    # pendant le temps différencié ? La réponse change ce que l'élève doit attendre de
    # l'heure qui vient, et elle doit donc être écrite.
    decale = domaine not in theme and focus not in (
        "Consolidation d'ensemble", "Rédaction et raisonnement",
        "Diagnostic à établir en séance 1")

    add(f"# Séance {number} — {theme}")
    add("")
    add(f"**Le thème du groupe aujourd'hui :** {theme}.  ")
    if decale:
        add(f"**Ton point personnel pendant le temps différencié :** {domaine}.  ")
    add(f"**Ta piste :** {piste}. {PISTE_EXIGENCE[piste]}")
    add("")
    add("## Aujourd'hui, tu vas…")
    add("")
    add(str(row["objectif"]))
    if decale:
        add("")
        add(f"L'entraînement collectif porte sur {theme.split(' :')[0].lower()} ; ton "
            f"exercice personnel, plus bas, porte sur {domaine.lower()}. Les deux sont à "
            f"traiter : le premier avec le groupe, le second pendant le temps différencié.")
    add("")
    if focus not in ("Consolidation d'ensemble", "Rédaction et raisonnement"):
        chiffre = ""
        if piste == "Diagnostiquer":
            # Le taux de réussite d'un domaine sans réponse ne mesure rien : le publier
            # transformerait une absence d'information en constat d'échec.
            chiffre = (" Les questions de ce domaine sont restées sans réponse : on ne sait "
                       "donc pas encore ce que tu sais faire dessus, et c'est ce que la "
                       "séance va établir.")
        elif reussite is not None:
            chiffre = (f" Sur ce domaine, tu as réussi {reussite:.0f} % des questions du "
                       f"positionnement.")
        add(f"> **Remarque.** Ce que ton positionnement a montré sur ce point : "
            f"{row['focus']}.{chiffre} C'est de là que part ta séance.")
        add("")
    if appui:
        add(f"> **Rappel.** Un point sur lequel tu peux t'appuyer aujourd'hui : {appui}")
        add("")

    # --- réactivation -------------------------------------------------------------
    add("## Pour commencer — dix minutes, de tête")
    add("")
    add("Ces questions ne sont pas notées. Elles servent à réveiller ce dont la séance a "
        "besoin. Si l'une te bloque, signale-la : c'est une information utile.")
    add("")
    for position, question in enumerate(bank["reactivation"], 1):
        add(f"{position}. {question}  ....................")
    add("")
    if reactivation_differee:
        add(f"> **Rappel.** {reactivation_differee}")
        add("")

    # --- essentiel ----------------------------------------------------------------
    if parts.get("spontanee") and (confrontation or piste == "Diagnostiquer"):
        add("## Avant tout : ta réponse spontanée")
        add("")
        if confrontation:
            add("> **Remarque.** Réponds **avant** de lire la suite, et note ta certitude "
                "honnêtement. Sur ce domaine, ton positionnement a donné une réponse fausse "
                "assurée : c'est cette réponse-là qu'il faut voir apparaître pour pouvoir "
                "la reprendre.")
            add("")
        add(parts["spontanee"])
        add("")
    if parts.get("trace"):
        add("## L'essentiel à retenir")
        add("")
        add(parts["trace"])
        add("")

    add("## La méthode, dans l'ordre")
    add("")
    for step in _numbered(list(bank["methode"])):
        add(step)
    add("")

    if parts.get("exemple") and exemple_donne:
        add("## Un exemple mené jusqu'au bout")
        add("")
        add(parts["exemple"])
        add("")
    elif redaction:
        add("> **Méthode.** Aucun exemple résolu ne t'est donné ici : sur ce domaine, tu "
            "réussis. Ce qui est attendu de toi aujourd'hui, c'est la **rédaction** — la "
            "propriété écrite avant le calcul, la conclusion qui répond à la question posée.")
        add("")

    add("## Les pièges de ce domaine")
    add("")
    for piege in bank["pieges"]:
        add(f"- {piege}")
    add("")

    # --- entraînement -------------------------------------------------------------
    add("## Ton entraînement")
    add("")
    exercises = parts.get(f"piste:{piste}")
    if exercises:
        # On ne décale le point d'entrée que sur les pistes de remédiation : un élève en
        # entretien ou en excellence traite sa série entière, elle est déjà courte.
        skip = entry_point(reussite) if piste in ("Installer", "Confronter") else 0
        exercises, removed = trim_exercises(exercises, skip)
        if removed:
            add(f"> **Remarque.** Les {removed} premier(s) exercice(s) d'application directe "
                f"ne figurent pas ici : ton positionnement montre que ce geste-là est "
                f"acquis. On commence donc plus loin dans la série. Si tu bloques malgré "
                f"tout, demande-les : ils existent.")
            add("")
        add(exercises)
    elif parts.get("thematiques"):
        add(parts["thematiques"])
    add("")

    # --- exercice personnel -------------------------------------------------------
    if personals:
        titre = ("## Tes exercices, ceux qui viennent de ton positionnement"
                 if len(personals) > 1
                 else "## Ton exercice, celui qui vient de ton positionnement")
        add(titre)
        add("")
        for position, personal in enumerate(personals, 1):
            marque = f"**{position}. " if len(personals) > 1 else "**"
            add(f"{marque}{personal['domaine']} — {personal['competence']}.** Cet exercice "
                f"est là parce que, au positionnement, la question correspondante a donné "
                f"une {personal['motif']}.")
            add("")
            add(str(personal["enonce"]))
            add("")
            for line in _short_answers(4):
                add(line)
            if personal.get("origine_erreur"):
                add(f"> **Piège.** {personal['origine_erreur']}")
                add("")
            add(f"> **Méthode.** {personal['geste']}")
            add("")
        if indices_donnes:
            add("### Si tu bloques — ouvre les indices dans l'ordre")
            add("")
            add("N'ouvre l'indice suivant que si le précédent n'a pas suffi, et note lequel "
                "t'a débloqué : « je ne savais pas » et « il me manquait un déclencheur » ne "
                "se traitent pas de la même façon.")
            add("")
            for indice in INDICES:
                add(f"- {indice}")
            add("")
            add("Indice qui m'a débloqué : $\\square$1 $\\square$2 $\\square$3 "
                "$\\square$aucun, j'ai trouvé seul")
            add("")

    # --- transfert ----------------------------------------------------------------
    add("## Transfert — à toi de choisir la méthode")
    add("")
    add("Rien dans cet énoncé ne dit quelle notion employer. C'est la question.")
    if redaction:
        add("")
        add("Ici, on attend une rédaction complète : la propriété citée, le calcul mené, la "
            "conclusion écrite en français.")
    add("")
    add(str(extra["transfert"]))
    add("")
    for line in _short_answers(5):
        add(line)

    # --- passerelle ---------------------------------------------------------------
    if parts.get("terminale"):
        add("## Pour aller vers la Terminale")
        add("")
        add("Ce qui suit n'est pas attendu de toi aujourd'hui. C'est là pour que tu voies "
            "à quoi sert ce que tu viens de travailler.")
        add("")
        add(parts["terminale"])
        add("")

    if option_ouverte and parts.get("option"):
        add(f"## {parts.get('option_titre', 'Ouverture')}")
        add("")
        add(parts["option"])
        add("")

    # --- recul et sortie ----------------------------------------------------------
    add("## Prendre du recul")
    add("")
    for question in extra["controle"]:
        add(f"- {question}")
        add("")
        add(ANSWER)
        add("")

    add("## Avant de partir")
    add("")
    add("Trois questions courtes. Elles disent au professeur ce qui est acquis, ce qui est "
        "à confirmer, et ce qui doit être repris à la séance suivante.")
    add("")
    for position, question in enumerate(extra["exit"], 1):
        add(f"**{position}.** {question}")
        add("")
        add(ANSWER)
        add("")
    if intersession:
        add("### D'ici la prochaine séance — quinze minutes, pas davantage")
        add("")
        add(intersession)
        add("")
        add("Fait : $\\square$oui $\\square$non    Ce que j'ai noté : "
            "..................................................")
        add("")
    add("**Ma certitude sur cette séance :** $\\square$1 $\\square$2 $\\square$3 $\\square$4  ")
    add("**L'aide maximale que j'ai utilisée :** $\\square$A $\\square$B $\\square$C "
        "$\\square$D $\\square$E $\\square$aucune")
    add("")
    return out


def _reactivations(rows: list[dict]) -> dict[int, str]:
    """Reprise espacée : ce qui a été travaillé en séance n est rappelé plus tard.

    Une réussite le jour même ne prouve pas qu'une notion est installée. Le domaine
    travaillé en séance 1 revient donc en séance 3, celui de la séance 2 en séance 4, et
    ainsi de suite — assez tard pour que le rappel coûte quelque chose, assez tôt pour
    qu'il reste rattrapable avant la fin du stage.
    """
    differed: dict[int, str] = {}
    for row in rows:
        focus = str(row["focus"])
        if focus in ("Consolidation d'ensemble", "Rédaction et raisonnement"):
            continue
        target = int(row["seance"]) + 2
        if target > 5:
            continue
        domain = focus.split(" (")[0]
        differed[target] = (
            f"Tu as travaillé **{domain}** en séance {row['seance']}. Avant de commencer, "
            f"écris en une phrase la règle que tu en as retenue — sans regarder tes notes. "
            f"Si elle ne vient pas, c'est le moment de le dire."
        )
    return differed


def render_cahier(student: dict, subject: dict, module, rows: list[dict],
                  exercises: list[dict], frame: dict, group: dict,
                  banner: str, option_ouverte: bool, root: Path,
                  diagnostic: dict | None = None) -> str:
    """Le cahier des cinq séances d'un élève, dans une matière."""
    name = student["displayName"]
    out: list[str] = []
    add = out.append

    add(f"# {module.label} — Cahier des cinq séances — {name}")
    add(f"## {subject['matiere']} — Stage de pré-rentrée 2026-2027")
    add("")
    add(banner)
    add("")
    add(f"**Élève :** {name}  ")
    add(f"**Groupe :** {group['libelle']}  ")
    add(f"**Matière :** {subject['matiere']}  ")
    add(f"**Organisme :** {frame['organisme']}  ")
    add(f"**Stage :** {frame['dureeParSpecialite']}, {frame['rythme']}  ")
    add(f"**Dates :** {frame['dates']}")
    add("")
    add("---")
    add("")

    add("## Ton parcours de pré-rentrée")
    add("")
    add("Le thème de chaque séance est commun au groupe. L'objectif, la piste et les "
        "exercices sont les tiens : ils viennent de ton positionnement.")
    add("")
    add("| Séance | Thème | Ton objectif | Ta piste |")
    add("|---:|---|---|:---:|")
    for row in rows:
        add(f"| {row['seance']} | {row['theme']} | {row['objectif']} | {row['parcours']} |")
    add("")

    add("## Comment utiliser ce cahier")
    add("")
    add("- Chaque séance suit le même ordre : réactivation, essentiel, méthode, "
        "entraînement, transfert, ouverture, bilan.")
    add("- Tu ne traites que les exercices de ta piste. Ils sont déjà sélectionnés ici : "
        "ce cahier ne contient pas ceux des autres.")
    add("- Écris la propriété ou la relation **avant** de calculer. C'est la seule habitude "
        "que ce stage cherche à installer partout.")
    add("- Note à chaque fois la lettre de l'aide utilisée. Ce n'est pas un aveu : c'est la "
        "mesure de ton autonomie, et on veut la voir baisser d'ici la séance 5.")
    add("")
    add("---")
    add("")

    diagnostic = diagnostic or {}
    scores = diagnostic.get("reussite_par_domaine", {})
    plan = list(diagnostic.get("plan_action_inter_seances", []))
    appuis = list(diagnostic.get("points_appui", []))
    differed = _reactivations(rows)
    per_domain: dict[str, list[dict]] = {}
    for exercise in exercises:
        per_domain.setdefault(str(exercise["domaine"]), []).append(exercise)

    for row in rows:
        number = int(row["seance"])
        parts = read_sheet(module.key, number, root)
        example = read_worked_example(module.key, number, root)
        if example:
            parts["exemple"] = example
        # Les exercices personnels de la séance sont **tous** ceux qui portent sur le
        # domaine mis au travail ce jour-là : un élève qui a manqué trois questions du même
        # domaine en reçoit trois, un élève qui en a manqué une en reçoit une. C'est le
        # bilan qui fixe la quantité, pas un quota.
        domain = str(row["focus"]).split(" (")[0]
        personals = [e for e in exercises if str(e["domaine"]) == domain]
        for personal in personals:
            exercises.remove(personal)
        # Aucun domaine au programme ce jour-là : on place le premier exercice encore en
        # attente, pour que rien du bilan ne reste sans être traité d'ici la séance 5.
        if not personals and exercises:
            personals = [exercises.pop(0)]
        add('<div class="page-break"></div>')
        add("")
        out.extend(render_seance(
            number, str(row["theme"]), row, parts, module.key, name, personals,
            option_ouverte, differed.get(number),
            reussite=scores.get(domain),
            # Le plan d'action du bilan est réparti sur les séances : une consigne par
            # séance, dans l'ordre où le bilan les a écrites. La dernière séance ferme le
            # stage, elle ne prépare rien.
            intersession=plan[number - 1] if number - 1 < len(plan) and number < 5 else None,
            appui=appuis[(number - 1) % len(appuis)] if appuis else None,
        ))
        add("---")
        add("")

    add('<div class="page-break"></div>')
    add("")
    add("## Bilan personnel — à remplir à la fin du stage")
    add("")
    add("Rien n'est prérempli ici : ce sont des constats, et ils n'existent qu'après les "
        "cinq séances.")
    add("")
    for question in (
        "Ce que je consolide vraiment, et que je saurais refaire seul",
        "Le point que je dois encore surveiller à la rentrée",
        "Une méthode que je retiens, écrite avec mes mots",
        "La première notion de Terminale que je me sens prêt à aborder",
    ):
        add(f"**{question}**")
        add("")
        add(ANSWER)
        add("")
        add(ANSWER)
        add("")
    add("| Séance | 1 | 2 | 3 | 4 | 5 |")
    add("|---|:---:|:---:|:---:|:---:|:---:|")
    add("| Aide maximale utilisée | | | | | |")
    add("| Certitude déclarée | | | | | |")
    add("")
    return "\n".join(out).rstrip() + "\n"
