# -*- coding: utf-8 -*-
"""Arithmétique des points : exacte, sans flottant."""

from decimal import Decimal

import pytest

from app.domain import points


def test_les_montants_du_bareme_reel_se_representent_sans_arrondi():
    for value in ("0.25", "0.3", "0.4", "0.5", "0.6", "0.7", "0.75", "1", "1.25", "1.5"):
        centi = points.to_centi(value)
        assert centi % points.STEP == 0
        assert points.to_decimal(centi) == Decimal(value)


def test_un_montant_plus_fin_que_le_centieme_est_refuse():
    with pytest.raises(points.PointsError):
        points.to_centi("0.333")


def test_aucun_flottant_ne_traverse_le_calcul():
    total = 0
    for value in ["0.3"] * 10:
        total += points.to_centi(value)
    assert total == 300
    assert points.format_fr(total) == "3"


def test_affichage_a_la_francaise():
    assert points.format_fr(1450) == "14,5"
    assert points.format_fr(2000) == "20"
    assert points.format_fr(25) == "0,25"


def test_les_valeurs_proposees_restent_dans_le_bareme():
    for max_centi in (25, 30, 40, 50, 60, 70, 75, 100, 125, 150):
        values = points.allowed_scores(max_centi)
        assert values[0] == 0 and values[-1] == max_centi
        assert all(points.is_acceptable(v, max_centi) for v in values)
    assert not points.is_acceptable(101, 100)
    assert not points.is_acceptable(-5, 100)
    assert not points.is_acceptable(33, 100)      # pas un multiple de 0,05


def test_pourcentage_exact():
    assert points.percentage(1750, 2000) == Decimal("87.5")
    assert points.percentage(0, 0) is None
