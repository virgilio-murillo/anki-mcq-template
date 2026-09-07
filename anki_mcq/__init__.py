"""
anki_mcq - Reusable multiple-choice Anki template engine.

Public API (import from the package root):

    from anki_mcq import card, build_deck, create, verify_cards, verify_apkg, sync

See the top-level README.md for the full workflow and docs/DECK_STANDARDS.md
for the mandatory quality standards every deck must follow.
"""

from .engine import (
    card,
    build_deck,
    make_model,
    render_options,
    DEFAULT_MODEL_ID,
    DEFAULT_DECK_ID,
    CSS,
)
from .create_deck import create
from .verify_deck import verify_cards, verify_apkg
from .sync_deck import sync

__all__ = [
    "card",
    "build_deck",
    "make_model",
    "render_options",
    "DEFAULT_MODEL_ID",
    "DEFAULT_DECK_ID",
    "CSS",
    "create",
    "verify_cards",
    "verify_apkg",
    "sync",
]
