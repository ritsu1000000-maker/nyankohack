# -*- coding: utf-8 -*-
"""BCSFE 3.6.0 compatibility fixes loaded automatically by Python startup."""

try:
    import bcsfe.core as core
    from bcsfe.core.game.catbase.cat import Talent as CatTalent

    if not hasattr(core, "Talent"):
        core.Talent = CatTalent
except Exception:
    # Do not block the web server if BCSFE is still being initialized.
    pass
