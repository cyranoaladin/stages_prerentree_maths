# -*- coding: utf-8 -*-
"""Agrégation des blueprints de niveau et des modules de consolidation."""

from . import lvl_4e, lvl_3e, lvl_2nde, lvl_1ere_spe, lvl_1re_nsi
from . import modules_maths, modules_nsi

LEVELS = {
    lvl_4e.LEVEL["key"]: lvl_4e.LEVEL,
    lvl_3e.LEVEL["key"]: lvl_3e.LEVEL,
    lvl_2nde.LEVEL["key"]: lvl_2nde.LEVEL,
    lvl_1ere_spe.LEVEL["key"]: lvl_1ere_spe.LEVEL,
    lvl_1re_nsi.LEVEL["key"]: lvl_1re_nsi.LEVEL,
}

MODULES = {}
MODULES.update(modules_maths.MODULES)
MODULES.update(modules_nsi.MODULES)

LEVEL_ORDER = ["4e", "3e", "2nde", "1ere_spe", "1re_nsi"]
