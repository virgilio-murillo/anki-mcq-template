#!/usr/bin/env python3
"""
gold_reference.py - Load the gold reference deck (MLA-C01) as plain card dicts,
with NO side effects (no build, no import, no AnkiConnect).

Why this exists
---------------
`normalize_deck.normalize(new_cards, ref_cards, ...)` needs the reference deck's
cards to compute the length distribution to normalize toward. The reference is
the hand-tuned MLA-C01 deck. But the deck `.py` files call `create(...)` (some
at module level), which would try to build/import and hit AnkiConnect just from
importing them. This loader executes each deck module with `create` and the
AnkiConnect entry points stubbed out, then returns the accumulated `cards` list.

Usage
-----
    from anki_mcq.gold_reference import load_gold_reference
    mla_cards = load_gold_reference()   # ~224 card dicts, safe to load anywhere
"""
import os
import glob
import re

# Repo root = parent of the anki_mcq package directory.
_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_PKG_DIR)
DEFAULT_GOLD_GLOB = os.path.join(_REPO_ROOT, "decks", "mla-c01", "mla_c01_*.py")


def _load_cards_from_file(path):
    """Exec one deck .py with create() neutralized; return its `cards` list."""
    import anki_mcq
    src = open(path, encoding="utf-8").read()
    # Neutralize any top-level create(...) call so importing has no side effects.
    src = re.sub(r'(?m)^create\(', '_MCQ_NOOP(', src)
    ns = {
        "card": anki_mcq.card,
        "create": lambda *a, **k: None,   # in case it is referenced but not called at top level
        "_MCQ_NOOP": lambda *a, **k: None,
        "__name__": "_gold_ref_module",   # so `if __name__ == "__main__"` guards do NOT fire
        "__file__": path,
        "os": os,
    }
    exec(compile(src, path, "exec"), ns)
    cards = ns.get("cards", [])
    return list(cards) if cards else []


def load_gold_reference(glob_pattern=DEFAULT_GOLD_GLOB):
    """Return the reference deck's cards as a flat list of card dicts.

    No build, no import, no AnkiConnect. Safe to call from any flow that needs
    the reference length distribution (e.g. normalize_deck.normalize).

    Raises FileNotFoundError if no reference deck files are found, so a caller
    never silently normalizes against an empty reference.
    """
    files = sorted(glob.glob(glob_pattern))
    if not files:
        raise FileNotFoundError(
            f"No gold reference deck files matched {glob_pattern!r}. "
            "The reference deck (MLA-C01) is required to normalize a new deck."
        )
    cards = []
    for f in files:
        cards.extend(_load_cards_from_file(f))
    if not cards:
        raise FileNotFoundError(
            f"Gold reference files matched {glob_pattern!r} but yielded 0 cards."
        )
    return cards
