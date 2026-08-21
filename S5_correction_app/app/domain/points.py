# -*- coding: utf-8 -*-
"""Arithmétique des points : exacte, en centièmes entiers.

Le barème distribué contient 0,3 / 0,4 / 0,6 / 0,7 : ce ne sont pas des quarts de point.
Le centième est la plus grande unité qui représente tout le barème sans arrondi. Les
points circulent donc en entiers, et ne redeviennent des ``Decimal`` que pour être
affichés ou exportés.
"""

from decimal import Decimal, InvalidOperation

SCALE = 100
STEP = 5          # tout montant du barème réel est un multiple de 0,05 point


class PointsError(ValueError):
    pass


def to_centi(value) -> int:
    """Convertit un montant de points en centièmes entiers, sans passer par un float."""
    if value is None:
        raise PointsError("montant de points absent")
    if isinstance(value, int):
        return value * SCALE
    if isinstance(value, Decimal):
        d = value
    else:
        text = str(value).strip().replace(",", ".")
        if not text:
            raise PointsError("montant de points vide")
        try:
            d = Decimal(text)
        except InvalidOperation:
            raise PointsError("montant de points illisible : %r" % value)
    scaled = d * SCALE
    if scaled != scaled.to_integral_value():
        raise PointsError("montant de points plus fin que le centième : %r" % value)
    return int(scaled)


def to_decimal(centi: int) -> Decimal:
    return (Decimal(int(centi)) / Decimal(SCALE)).quantize(Decimal("0.01"))


def format_fr(centi: int, unit: str = "") -> str:
    """« 14,5 » et non « 14.50 ». Les zéros inutiles disparaissent."""
    d = to_decimal(centi).normalize()
    text = format(d, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    text = text.replace(".", ",")
    return ("%s %s" % (text, unit)).strip() if unit else text


def allowed_scores(max_centi: int) -> list:
    """Les valeurs proposées par l'interface pour un critère de ce barème.

    Quarts lorsque le maximum est un multiple de 0,25 — c'est le cas de 292 critères sur
    337. Sinon moitiés, ce qui donne 0 / 0,15 / 0,3 plutôt qu'une échelle inutilisable.
    Le zéro et le plein score y figurent toujours.
    """
    max_centi = int(max_centi)
    if max_centi <= 0:
        raise PointsError("un critère ne peut pas valoir zéro point")
    if max_centi % 25 == 0:
        step = max_centi // 4 if max_centi % 4 == 0 else 25
        values = list(range(0, max_centi + 1, step)) if step else [0, max_centi]
    else:
        half = max_centi // 2
        values = [0, half, max_centi] if half * 2 == max_centi else [0, max_centi]
    if max_centi not in values:
        values.append(max_centi)
    return sorted(set(v for v in values if 0 <= v <= max_centi))


def is_acceptable(score_centi: int, max_centi: int) -> bool:
    """Le serveur est plus tolérant que les boutons : tout multiple de 0,05 dans [0 ; max].

    L'interface propose une échelle courte ; un correcteur qui a une raison d'accorder
    0,6 sur 0,7 doit pouvoir le faire sans contourner l'outil.
    """
    if score_centi is None:
        return False
    s = int(score_centi)
    return 0 <= s <= int(max_centi) and s % STEP == 0


def percentage(earned_centi: int, available_centi: int):
    if not available_centi:
        return None
    return (Decimal(earned_centi) * 100 / Decimal(available_centi)).quantize(Decimal("0.1"))
