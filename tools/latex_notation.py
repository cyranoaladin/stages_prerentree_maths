#!/usr/bin/env python3
"""Notation mathématique : de l'approximation Unicode au LaTeX réel.

Les documents Terminale ont d'abord été écrits pour un rendu HTML, avec les moyens du
texte brut : `u₀`, `0,5^n`, `≥`, `☐`. Cette notation a deux défauts que l'impression rend
visibles. D'abord elle est fausse typographiquement — une variable n'est pas en romain,
un indice n'est pas un caractère à part entière. Ensuite elle est incomplète : ni limite,
ni intégrale, ni racine ne s'écrivent ainsi.

Ce module traduit cette notation en LaTeX. Il est utilisé à deux endroits :

- une fois, pour réécrire les documents rédigés à la main (`tools/mathify_terminale.py`) ;
- à chaque génération, sur les documents nominatifs que `tools/build_terminale.py`
  produit à partir des bilans, dont le texte vient des PDF d'origine.

La conversion est délibérément prudente. Elle ne devine pas : elle reconnaît des motifs
fermés (indices, exposants, relations, formules chimiques) et laisse tout le reste
intact. Ce qu'elle ne sait pas traduire, `remaining_symbols()` le signale, et le test
`test_terminale.py` fait échouer la construction plutôt que de laisser passer un
caractère que la police ne saurait pas dessiner.
"""

from __future__ import annotations

import re

# Les caractères qui ne doivent plus apparaître dans le corpus Markdown : ils relèvent
# des mathématiques et Latin Modern n'en dessine qu'une partie.
FORBIDDEN_SYMBOLS = (
    "☐≥≤≠−×÷≈∞√∈∉⊂∪∩∀∃⇒⇔≡±‖ΔΣℝℂℤℕℚ✓↑↓←→↔↗↘⟹⟺"
    "₀₁₂₃₄₅₆₇₈₉ₙ⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁺⁻"
)

# Le jeu de caractères qu'un document peut contenir hors mathématiques : ASCII, lettres
# accentuées françaises et ponctuation typographique. Tout le reste doit passer par
# LaTeX. La liste des symboles interdits ci-dessus ne suffirait pas : elle ne connaît que
# ce qui a déjà été rencontré, alors que ce filtre attrape aussi ce qui viendra —
# caractères de dessin de tableaux, flèches inhabituelles, lettres grecques oubliées.
SUPPORTED_CHARACTERS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    " \t\n\r!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
    "àâäçéèêëîïôöùûüÿœæÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸŒÆ"
    "«»—–‘’“”…°·§€"
)

SUBSCRIPT_DIGITS = {c: str(i) for i, c in enumerate("₀₁₂₃₄₅₆₇₈₉")}
SUBSCRIPT_DIGITS["ₙ"] = "n"
SUPERSCRIPT_DIGITS = {c: str(i) for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
SUPERSCRIPT_DIGITS.update({"ⁿ": "n", "⁺": "+", "⁻": "-"})

# Symboles traduits tels quels dès qu'ils entrent dans une expression mathématique.
# `\leqslant` et `\geqslant` plutôt que `\leq`/`\geq` : c'est la forme employée dans
# l'enseignement français, et celle des sujets de baccalauréat.
SYMBOL_TO_LATEX = {
    "≥": r"\geqslant", "≤": r"\leqslant", "≠": r"\neq", "≈": r"\approx",
    "≡": r"\equiv", "±": r"\pm", "−": "-", "×": r"\times", "÷": r"\div",
    "∞": r"\infty", "∈": r"\in", "∉": r"\notin", "⊂": r"\subset",
    "∪": r"\cup", "∩": r"\cap", "∀": r"\forall", "∃": r"\exists",
    "⇒": r"\Rightarrow", "⇔": r"\Leftrightarrow", "→": r"\to", "√": r"\surd",
    "⟹": r"\implies", "⟺": r"\iff", "↔": r"\leftrightarrow", "←": r"\leftarrow",
    "↑": r"\uparrow", "↓": r"\downarrow", "↗": r"\nearrow", "↘": r"\searrow",
    "✓": r"\checkmark", "‖": r"\|",
    # Le discriminant, la somme, et les ensembles de nombres du programme.
    "Δ": r"\Delta", "Σ": r"\sum", "ℝ": r"\mathbb{R}", "ℂ": r"\mathbb{C}",
    "ℤ": r"\mathbb{Z}", "ℕ": r"\mathbb{N}", "ℚ": r"\mathbb{Q}",
}

# Le point médian sépare les facteurs d'un produit scalaire ou d'une unité composée
# (m·s⁻¹). Il sert aussi de puce décorative dans les entêtes : il n'entre donc dans une
# formule que si un vrai signe mathématique l'accompagne, et n'en déclenche jamais une.
NEUTRAL_SYMBOLS = {"·": r"\cdot", "×": r"\times"}

# Fonctions usuelles : en LaTeX elles se composent en romain, pas en italique.
FUNCTIONS = ("arccos", "arcsin", "arctan", "cos", "sin", "tan", "ln", "log",
             "exp", "lim", "max", "min", "sup", "inf")


def _protect(text: str) -> tuple[str, list[str]]:
    """Met de côté ce qui ne doit jamais être touché : code, maths déjà écrites, liens."""
    kept: list[str] = []

    def stash(match: re.Match[str]) -> str:
        kept.append(match.group(0))
        return f"\x00{len(kept) - 1}\x00"

    # L'ordre compte : les blocs de code englobent parfois des backticks isolés.
    for pattern in (
        r"```.*?```",              # bloc de code clôturé
        r"~~~.*?~~~",
        r"`[^`\n]+`",              # code en ligne
        r"\$[^$\n]+\$",            # mathématiques déjà en LaTeX
        r"\]\([^)\n]*\)",          # cible d'un lien Markdown
        r"https?://\S+",
    ):
        text = re.sub(pattern, stash, text, flags=re.DOTALL)
    return text, kept


def _restore(text: str, kept: list[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], text)


def _ascii_scripts(text: str) -> str:
    """`u₀` devient `u_0`, `x²` devient `x^2` : une notation intermédiaire en ASCII."""
    def sub_run(match: re.Match[str]) -> str:
        digits = "".join(SUBSCRIPT_DIGITS[c] for c in match.group(0))
        return f"_{{{digits}}}" if len(digits) > 1 else f"_{digits}"

    def sup_run(match: re.Match[str]) -> str:
        digits = "".join(SUPERSCRIPT_DIGITS[c] for c in match.group(0))
        return f"^{{{digits}}}" if len(digits) > 1 else f"^{digits}"

    text = re.sub("[" + "".join(SUBSCRIPT_DIGITS) + "]+", sub_run, text)
    text = re.sub("[" + "".join(SUPERSCRIPT_DIGITS) + "]+", sup_run, text)
    return text


# --- reconnaissance d'une expression mathématique ---------------------------------
# Un atome : un nombre, une fonction usuelle, une variable d'une seule lettre, un
# symbole, un opérateur ou une parenthèse. Un mot de plusieurs lettres arrête
# l'expression : c'est ce qui empêche la prose française d'y être absorbée.
#
# `_LETTER` couvre tout l'alphabet Unicode, accents compris. Avec `[a-zA-Z]`, le « d »
# de « décroissante » passait pour une variable parce que le « é » qui le suit n'est pas
# une lettre ASCII, et la phrase se retrouvait coupée en plein milieu.
_LETTER = r"[^\W\d_]"
_NUMBER = r"\d+(?:[.,]\d+)?"
_FUNCTION = "|".join(FUNCTIONS)
_SYMBOLS = "".join(SYMBOL_TO_LATEX)
# `|`, `*` et `!` sont volontairement absents des opérateurs : le premier sépare les
# cellules d'un tableau Markdown, le deuxième délimite le gras, le troisième ponctue le
# français. Les absorber dans une formule casserait la source.
# `['’]` : la dérivée f'. Elle n'est reconnue que si aucune lettre ne suit, ce qui la
# distingue de l'élision française : dans « n'a pas de solution », le « n' » n'est pas
# une dérivée, et sans cette garde il emportait le « a » du verbe dans la formule.
_VARIABLE = rf"(?<!{_LETTER})[a-zA-Z](?:['’](?!{_LETTER}))?(?!{_LETTER})"
_ATOM = (
    rf"(?:{_NUMBER}|(?:{_FUNCTION})(?![a-zA-Z])|{_VARIABLE}"
    rf"|[{_SYMBOLS}·]|[-+/=<>;()\[\]])"
)
# `e^(3x + (1 - x))` : le corpus met l'exposant entre parenthèses faute de mieux. Il faut
# le reconnaître avec un niveau d'imbrication, sans quoi le `^` reste orphelin et la
# formule se scinde en plein milieu.
_PARENTHESES = r"\((?:[^()\n]|\([^()\n]*\))*\)"
_SCRIPT = rf"(?:[_^](?:\{{[^{{}}\n]*\}}|{_PARENTHESES}|[a-zA-Z0-9+-]))*"
_RUN = re.compile(rf"(?:{_ATOM}{_SCRIPT})(?:[ \t]*(?:{_ATOM}{_SCRIPT}))*")

# Sans l'un de ces signes, une suite d'atomes n'est pas une formule : « 5 » ou
# « A, B, C » doivent rester du texte. Une application de fonction — `f(`, `u(` — en est
# un : sans elle, « Calculer f(a) et f'(a) » resterait en romain dans un document où la
# ligne voisine compose la même expression en italique.
_MARKERS = re.compile(
    r"[_^=<>" + "".join(SYMBOL_TO_LATEX) + rf"]|{_VARIABLE}\(|(?:{_FUNCTION})\("
)

# `a` et `y` sont aussi des mots français. En fin d'expression, « x² − 4 a pour racines »
# les livre à la formule et coupe la phrase ; on les rend au texte, sauf s'ils suivent un
# opérateur, où ils sont bien l'opérande attendue (« f(x) = a »).
_TRAILING_FRENCH_WORD = re.compile(r"(?<![-+=<>*/])\s+([ay])$")
# Une lettre isolée suivie d'une apostrophe dans la source est une élision — l', d', n',
# qu' — et non une variable : la dérivée, elle, a déjà emporté son apostrophe.
_TRAILING_ELISION = re.compile(r"\s*[a-zA-Z]$")
# Le même piège au début : « on a v(n+1) − v_n = … ». Le « a » n'est l'opérande d'aucun
# opérateur, il est le verbe de la phrase.
_LEADING_FRENCH_WORD = re.compile(r"^([ay])\s+(?![-+=<>/*])")
# Une étiquette d'énumération — « b) » en tête de ligne — n'appartient pas à la formule
# qui la suit.
_ENUMERATION_LABEL = re.compile(r"^[a-z]\)\s+")

# Une formule ne commence jamais par un opérateur : un tiret en début de ligne est une
# puce Markdown, pas un signe moins.
_LEADING_OPERATORS = " \t-+=<>/;"

# Une formule chimique : suite d'éléments, avec charge éventuelle. `\ce{}` de mhchem
# la compose selon les conventions de la chimie (indices bas, charge en exposant).
_CHEMICAL = re.compile(
    r"\b((?:[A-Z][a-z]?(?:_\{?\d+\}?)?){1,6})(\^\{?[0-9]*[+-]\}?)?"
)


def _looks_chemical(formula: str, charge: str | None) -> bool:
    """Distingue `H_2O` d'un simple sigle. Une charge ou un indice tranche."""
    if charge:
        return True
    return "_" in formula and len(re.findall(r"[A-Z]", formula)) >= 1


# Un exposant ou un indice parenthésé devient un groupe LaTeX : e^(3x) donne e^{3x}.
_PARENTHESISED_SCRIPT = re.compile(rf"([_^])({_PARENTHESES})")


def _brace_scripts(expression: str) -> str:
    return _PARENTHESISED_SCRIPT.sub(
        lambda m: f"{m.group(1)}{{{m.group(2)[1:-1]}}}", expression
    )


def _latex_atoms(expression: str) -> str:
    expression = _brace_scripts(expression)
    for symbol, replacement in NEUTRAL_SYMBOLS.items():
        expression = expression.replace(symbol, f" {replacement} ")
    for symbol, replacement in SYMBOL_TO_LATEX.items():
        expression = expression.replace(symbol, f" {replacement} ")
    for function in FUNCTIONS:
        # `\b` ne convient pas : entre « log » et « _2 » il n'y a pas de frontière de mot,
        # le souligné étant lui-même un caractère de mot. La garde amont écarte aussi une
        # fonction déjà échappée par un passage précédent.
        expression = re.sub(
            rf"(?<![a-zA-Z\\]){function}(?![a-zA-Z])", rf"\\{function}", expression
        )
    # La virgule décimale française : `{,}` empêche LaTeX d'y mettre l'espace d'une
    # énumération. C'est la différence entre « 0,5 » et « 0, 5 ».
    expression = re.sub(r"(?<=\d),(?=\d)", "{,}", expression)
    return re.sub(r"\s+", " ", expression).strip()


_BRACKETS = {"(": ")", "[": "]"}


def _balanced(run: str) -> tuple[str, str, str]:
    """Retire les parenthèses orphelines d'une expression, et les rend au texte.

    « Δ = 0 (signe de a partout) » : la parenthèse ouvrante appartient à la phrase, pas
    à la formule. Absorbée, elle collait le texte au symbole et laissait une parenthèse
    seule en italique.
    """
    prefix = suffix = ""
    changed = True
    while changed and run:
        changed = False
        opened = sum(run.count(key) - run.count(value) for key, value in _BRACKETS.items())
        if opened > 0 and run.rstrip()[-1:] in _BRACKETS:
            cut = len(run.rstrip())
            suffix = run[cut - 1:] + suffix
            run, changed = run[: cut - 1], True
        elif opened < 0 and run.lstrip()[:1] in _BRACKETS.values():
            cut = len(run) - len(run.lstrip())
            prefix += run[: cut + 1]
            run, changed = run[cut + 1:], True
    # L'espace qui séparait la formule de la parenthèse rendue au texte lui revient
    # aussi : sans lui, « $\Delta = 0$(signe… » collerait les deux.
    body = run.strip()
    return body, prefix + run[: len(run) - len(run.lstrip())], run[len(run.rstrip()):] + suffix


def _convert_runs(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        run = match.group(0)
        if not _MARKERS.search(run):
            return run
        # Une expression se terminant par un opérateur isolé emporterait la ponctuation
        # de la phrase ; on la rend au texte.
        trailing = ""
        while run and run[-1] in " \t,;:":
            trailing = run[-1] + trailing
            run = run[:-1]
        label = _ENUMERATION_LABEL.match(run)
        prefix = ""
        at_line_start = match.start() == 0 or match.string[match.start() - 1] == "\n"
        if label and at_line_start:
            prefix, run = label.group(0), run[label.end():]
        opening = _LEADING_FRENCH_WORD.match(run)
        if opening:
            prefix += opening.group(0)
            run = run[opening.end():]
        if match.string[match.end():match.end() + 1] in "'\u2019":
            elision = _TRAILING_ELISION.search(run)
            if elision:
                trailing = run[elision.start():] + trailing
                run = run[:elision.start()]
        stripped = _TRAILING_FRENCH_WORD.search(run)
        if stripped:
            trailing = run[stripped.start():] + trailing
            run = run[:stripped.start()]
        leading = ""
        while run and run[0] in _LEADING_OPERATORS:
            leading += run[0]
            run = run[1:]
        run, opener, closer = _balanced(run)
        trailing = closer + trailing
        prefix += opener
        if not run or not _MARKERS.search(run):
            return match.group(0)
        return f"{prefix}{leading}${_latex_atoms(run)}${trailing}"

    return _RUN.sub(replace, text)


# Une équation de réaction complète : deux formules au moins de part et d'autre d'une
# flèche. mhchem la compose d'un bloc — flèche, coefficients et états compris — ce qu'une
# conversion espèce par espèce ne saurait pas faire.
_REACTION = re.compile(
    r"(?<![\w$])((?:\d*\s*[A-Z][A-Za-z0-9_{}^+-]*(?:\s*\+\s*)?)+)"
    r"\s*(→|->|⇌|=)\s*"
    r"((?:\d*\s*[A-Z][A-Za-z0-9_{}^+-]*(?:\s*\+\s*)?)+)"
)


def _ce_body(formula: str) -> str:
    """Passe à la syntaxe de mhchem : `H_2O` s'y écrit `H2O`, la charge garde son `^`."""
    formula = re.sub(r"_\{?(\d+)\}?", r"\1", formula)
    return re.sub(r"\^\{([0-9]*[+-])\}", r"^\1", formula)


def _convert_chemistry(text: str) -> str:
    def reaction(match: re.Match[str]) -> str:
        left, arrow, right = match.group(1), match.group(2), match.group(3)
        species = re.findall(r"[A-Z][a-z]?", left + right)
        if len(species) < 2 or arrow == "=":
            return match.group(0)
        symbol = {"→": "->", "->": "->", "⇌": "<=>"}[arrow]
        body = f"{_ce_body(left.strip())} {symbol} {_ce_body(right.strip())}"
        body = re.sub(r"\s+", " ", body)
        return rf"\ce{{{body}}}"

    def species(match: re.Match[str]) -> str:
        formula, charge = match.group(1), match.group(2)
        if not _looks_chemical(formula, charge):
            return match.group(0)
        body = _ce_body(formula + (charge or ""))
        return rf"\ce{{{body}}}"

    text = _REACTION.sub(reaction, text)
    return _CHEMICAL.sub(species, text)


# --- unités du programme de physique-chimie ---------------------------------------
# siunitx compose « 3,0 × 10⁸ m·s⁻¹ » avec la virgule décimale française, le produit et
# l'exposant corrects, et une espace insécable entre le nombre et l'unité. Écrit à la
# main en mode mathématique, « m » et « s » ressortiraient en italique, ce qui en
# physique désigne une grandeur et non une unité.
UNIT_MACROS = {
    "m": r"\metre", "km": r"\kilo\metre", "cm": r"\centi\metre", "mm": r"\milli\metre",
    "s": r"\second", "ms": r"\milli\second", "min": r"\minute", "h": r"\hour",
    "kg": r"\kilogram", "g": r"\gram", "mg": r"\milli\gram",
    "mol": r"\mole", "mmol": r"\milli\mole", "L": r"\litre", "mL": r"\milli\litre",
    "K": r"\kelvin", "°C": r"\degreeCelsius",
    "V": r"\volt", "mV": r"\milli\volt", "A": r"\ampere", "mA": r"\milli\ampere",
    "Ω": r"\ohm", "J": r"\joule", "kJ": r"\kilo\joule", "W": r"\watt",
    "Hz": r"\hertz", "kHz": r"\kilo\hertz", "N": r"\newton", "Pa": r"\pascal",
    "bar": r"\bar", "eV": r"\electronvolt", "C": r"\coulomb", "F": r"\farad",
}
_UNIT_TOKEN = r"(?:°C|[A-Za-zΩ]{1,3})(?:\^\{?-?\d+\}?)?"
_UNITS = re.compile(
    r"(?<![\w.])(\d+(?:[.,]\d+)?)"                     # le nombre
    r"(?:\s*×\s*10\^\{?(-?\d+)\}?)?"                  # la puissance de dix, si elle est là
    rf"\s+({_UNIT_TOKEN}(?:[·.]{_UNIT_TOKEN})*)(?![\w·])"
)


def _unit_macro(unit: str) -> str | None:
    parts = []
    for token in re.split(r"[·.]", unit):
        exponent = re.search(r"\^\{?(-?\d+)\}?$", token)
        symbol = token[: exponent.start()] if exponent else token
        macro = UNIT_MACROS.get(symbol)
        if macro is None:
            return None
        power = int(exponent.group(1)) if exponent else 1
        if power < 0:
            parts.append(r"\per" + macro + (_POWERS.get(-power, "") if power != -1 else ""))
        else:
            parts.append(macro + (_POWERS.get(power, "") if power != 1 else ""))
    return "".join(parts)


_POWERS = {2: r"\squared", 3: r"\cubed"}


def _convert_units(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        number, exponent, unit = match.group(1), match.group(2), match.group(3)
        macro = _unit_macro(unit)
        if macro is None:
            return match.group(0)
        value = number.replace(",", ".")
        if exponent:
            value = f"{value}e{exponent}"
        return rf"\SI{{{value}}}{{{macro}}}"

    return _UNITS.sub(replace, text)


# Faute d'indices, le corpus notait le terme suivant d'une suite « u(n+1) ». En LaTeX il
# s'écrit u_{n+1} : ce n'est pas l'image de n+1 par une fonction u, c'est un terme de
# rang n+1. Seules les lettres qui désignent des suites dans ce corpus sont concernées ;
# f(x), g(x) et p(A) restent des applications.
_SEQUENCE_LETTERS = "uvwt"
_SEQUENCE_TERM = re.compile(rf"(?<![{_LETTER[1:-1]}])([{_SEQUENCE_LETTERS}])\(n([+-]\d+)?\)")


def _convert_sequences(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        name, shift = match.group(1), match.group(2)
        return f"{name}_{{n{shift}}}" if shift else f"{name}_n"

    return _SEQUENCE_TERM.sub(replace, text)


def to_latex(text: str, *, chemistry: bool = False) -> str:
    """Traduit la notation Unicode d'un document en LaTeX, hors code et liens."""
    text, kept = _protect(text)
    text = text.replace("☐", "$\\square$")
    text = _ascii_scripts(text)
    text = _convert_sequences(text)
    if chemistry:
        text = _convert_units(text)
        text = _convert_chemistry(text)
        # `\ce{}` compose lui-même ce qu'il contient : le laisser repasser par le
        # convertisseur d'expressions y injecterait des `$` au milieu de la formule.
        text, kept = _protect_chemistry(text, kept)
    text = _convert_runs(text)
    return _restore(text, kept)


def _protect_chemistry(text: str, kept: list[str]) -> tuple[str, list[str]]:
    def stash(match: re.Match[str]) -> str:
        kept.append(match.group(0))
        return f"\x00{len(kept) - 1}\x00"

    return re.sub(r"\\(?:ce|SI)\{[^{}]*\}(?:\{[^{}]*\})?", stash, text), kept


def remaining_symbols(text: str) -> list[str]:
    """Les caractères mathématiques Unicode encore présents, sans doublon, triés."""
    return sorted({char for char in text if char in FORBIDDEN_SYMBOLS})


def unsupported_characters(text: str) -> list[str]:
    """Les caractères qu'aucune police du document ne saurait dessiner, triés."""
    return sorted({char for char in text if char not in SUPPORTED_CHARACTERS})
