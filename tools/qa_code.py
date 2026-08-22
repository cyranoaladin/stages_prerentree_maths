"""Vérifie le code Python du corpus : ce qui est censé s'exécuter s'exécute.

Un bloc de code faux dans un livret de NSI est une faute plus grave qu'une coquille : il
apprend l'erreur. Les blocs volontairement fautifs — ceux des exercices de débogage — sont
reconnus à leur consigne et exclus du contrôle syntaxique, mais listés pour qu'on sache
qu'ils existent.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^```python\n(.*?)^```", re.M | re.S)
# Un bloc qu'un exercice demande de corriger ne doit pas être valide : c'est l'exercice.
DEBOGAGE = re.compile(
    r"(contient une erreur|trouve[- ]la|erreur à trouver|déboguer|corrige|à corriger"
    r"|échoue à l'exécution|ce programme échoue)", re.I)
# Un squelette à compléter non plus : les pointillés sont l'espace laissé à l'élève, et le
# corps vide d'une fonction est la place où il écrira sa réponse.
TROU = re.compile(r"\.{3,}")
ENTETE = re.compile(r"^\s*(def|class) .*:\s*$")
# Guillemets triples, construits par leur code pour ne pas fermer cette chaîne.
DOC = (chr(34) * 3, chr(39) * 3)


def blocks(path: Path) -> list[tuple[int, str, bool]]:
    """Les blocs Python d'un document, avec leur ligne et s'ils sont volontairement fautifs."""
    text = path.read_text(encoding="utf-8")
    out = []
    for match in FENCE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        # La consigne des cinq cents caractères qui précèdent dit si l'erreur est voulue.
        contexte = text[max(0, match.start() - 500):match.start()]
        out.append((line, match.group(1), bool(DEBOGAGE.search(contexte))))
    return out


def squelette(corps: str) -> bool:
    """Un en-tête de fonction ou de classe dont le corps est vide.

    C'est la forme d'un squelette à compléter : l'élève écrit sous l'en-tête. Python ne
    sait pas l'analyser, et c'est normal — ce n'est pas encore du code.
    """
    lignes = corps.split("\n")
    for position, ligne in enumerate(lignes):
        if not ENTETE.match(ligne):
            continue
        suite = [l for l in lignes[position + 1:] if l.strip()]
        if not suite:
            return True
        indentation = len(ligne) - len(ligne.lstrip())
        if len(suite[0]) - len(suite[0].lstrip()) <= indentation:
            return True
    return False


def main() -> int:
    vides = valides = attendus = trous = 0
    erreurs: list[str] = []
    for path in sorted(ROOT.glob("tle_*/**/*.md")):
        for line, code, fautif in blocks(path):
            corps = code.strip()
            if not corps or corps.replace(".", "").strip() == "":
                vides += 1          # espace d'écriture laissé à l'élève
                continue
            try:
                ast.parse(code)
            except SyntaxError as error:
                if fautif:
                    attendus += 1
                elif TROU.search(corps) or squelette(corps):
                    trous += 1
                else:
                    erreurs.append(
                        f"{path.relative_to(ROOT)}:{line} — {error.msg} (ligne {error.lineno})")
                continue
            valides += 1
    print(f"{valides} bloc(s) Python syntaxiquement valides, "
          f"{vides} bloc(s) vides laissés à l'élève, "
          f"{trous} squelette(s) à compléter, "
          f"{attendus} bloc(s) fautifs par construction.")
    if erreurs:
        print(f"\n{len(erreurs)} bloc(s) invalides sans consigne de débogage :")
        for erreur in erreurs:
            print(f"  - {erreur}")
        return 1
    print("Aucun bloc invalide en dehors des exercices de débogage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
