# -*- coding: utf-8 -*-
"""BCSFE 3.6.0 compatibility fixes loaded automatically by Python startup."""

try:
    import bcsfe.core as core
    from bcsfe.core.game.catbase.cat import Talent as CatTalent

    # BCSFE 3.6.0 does not export Talent from bcsfe.core, but the web tool
    # historically references core.Talent.
    if not hasattr(core, "Talent"):
        core.Talent = CatTalent

    # Strengthen fresh-account tutorial initialization. The original BCSFE
    # implementation is still called first; afterwards we verify/re-assert the
    # exact save-side flags used by BCSFE 3.6.0 so blank generated saves do not
    # fall back into an incomplete first-launch/tutorial state.
    StoryChapters = getattr(core, "StoryChapters", None)
    if StoryChapters is not None and not getattr(
        StoryChapters.clear_tutorial, "_nyankohack_patched", False
    ):
        _original_clear_tutorial = StoryChapters.clear_tutorial

        def _clear_tutorial_fixed(save_file):
            _original_clear_tutorial(save_file)

            save_file.tutorial_state = max(int(save_file.tutorial_state), 1)
            save_file.koreaSuperiorTreasureState = max(
                int(save_file.koreaSuperiorTreasureState), 2
            )
            save_file.ui6 = max(int(save_file.ui6), 1)

            if len(save_file.new_dialogs_2) < 6:
                save_file.new_dialogs_2.extend(
                    [0] * (6 - len(save_file.new_dialogs_2))
                )
            save_file.new_dialogs_2[1] = max(
                int(save_file.new_dialogs_2[1]), 2
            )
            save_file.new_dialogs_2[5] = max(
                int(save_file.new_dialogs_2[5]), 2
            )

            try:
                if save_file.story.chapters[0].stages[0].clear_times == 0:
                    save_file.story.clear_stage(0, 0)
            except Exception:
                pass

        _clear_tutorial_fixed._nyankohack_patched = True
        StoryChapters.clear_tutorial = _clear_tutorial_fixed

except Exception:
    # Do not block the web server if BCSFE is still being initialized.
    pass
