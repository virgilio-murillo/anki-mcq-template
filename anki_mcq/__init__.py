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
from .verify_deck import verify_cards, verify_apkg, check_distribution, concepts_preserved
from .normalize_deck import normalize as normalize_deck
from .refocus_deck import refocus as refocus_deck, needs_refocus
from .gold_reference import load_gold_reference
from .sync_deck import sync
from .universe import (
    build_universe,
    get_deck_roots,
    union_cards,
    extract_id,
    sha16,
    normalize,
    strip_html,
    strip_cloze,
    pick_question_field,
    AnkiWriteAttempt,
    AnkiUnreachable,
)
from .deck_classifier import (
    build_relevant_decks,
    heuristic_classify,
    relevant_roots,
    CLASSIFIER_PROMPT,
)
from .extract import (
    segment_exam,
    classify_block_type,
    reconcile,
    normalize as extract_normalize,
    token_overlap,
    contained,
    load_jsonl,
    write_canonical,
    SegmentationError,
    EXTRACTION_PROMPT,
)

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
    "check_distribution",
    "concepts_preserved",
    "normalize_deck",
    "refocus_deck",
    "needs_refocus",
    "load_gold_reference",
    "sync",
    # universe builder
    "build_universe",
    "get_deck_roots",
    "union_cards",
    "extract_id",
    "sha16",
    "normalize",
    "strip_html",
    "strip_cloze",
    "pick_question_field",
    "AnkiWriteAttempt",
    "AnkiUnreachable",
    "build_relevant_decks",
    "heuristic_classify",
    "relevant_roots",
    "CLASSIFIER_PROMPT",
    # exam extraction
    "segment_exam",
    "classify_block_type",
    "reconcile",
    "extract_normalize",
    "token_overlap",
    "contained",
    "load_jsonl",
    "write_canonical",
    "SegmentationError",
    "EXTRACTION_PROMPT",
]
