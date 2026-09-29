#!/usr/bin/env python3
"""
create_deck.py - Safe end-to-end flow to build, verify and import an MCQ deck
into a specific (sub)deck, WITHOUT moving cards around afterwards.

Why this exists
---------------
genanki writes every note into the deck named in the .apkg. If you rely on a
shared deck id and then try to "move the new cards" with a text query, you can
accidentally grab cards from OTHER decks (this happened once and dragged 85
SAP-C02 cards into the wrong subdeck). The fix:

- `build_deck(deck_name=...)` derives a UNIQUE deck id from the name and writes
  the FULL subdeck path (e.g. "DVA-C02::02") into the package, so Anki imports
  it straight into the right (sub)deck. No moving. No ambiguous queries.
- We run `verify_deck` as a quality gate BEFORE importing.

Usage
-----
    from anki_mcq import card
    from create_deck import create

    cards = [ card(..., key="dva02-q1"), ... ]
    create(deck_name="DVA-C02::02", cards=cards, out_path="DVA-C02_02.apkg")

Requirements: genanki; and (to import) Anki running with AnkiConnect.
"""
import json
import os
import urllib.request

from .engine import build_deck
from .verify_deck import verify_cards, verify_apkg, warn_cards, check_distribution

ANKICONNECT = "http://localhost:8765"


def _invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKICONNECT, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect '{action}': {data['error']}")
    return data["result"]


def create(deck_name, cards, out_path, do_import=True, verbose=True,
           ref_cards=None, llm_shorten=None, enforce_distribution=True):
    """Build -> verify -> (optionally) import a deck straight into `deck_name`.

    Returns the count of cards on success. Raises if verification fails.

    NORMALIZATION (see DECK_STANDARDS.md section 11): pass `ref_cards` (the gold
    reference deck, e.g. from gold_reference.load_gold_reference()) to normalize
    this deck's length distribution toward it BEFORE building. If `llm_shorten`
    is also given, over-budget cards are shortened (one model call each, concepts
    preserved); without it, normalization only plans (no rewrite) but the
    distribution gate below still runs.

    DISTRIBUTION GATE: when `ref_cards` is given and `enforce_distribution` is
    True (default), `check_distribution` runs as a HARD gate so a deck that is
    uniformly too long (the "everything is verbose" regression) fails loudly
    instead of shipping. When `ref_cards` is None the gate is skipped (backward
    compatible with existing per-deck scripts that do not pass a reference).
    """
    # 0) Normalize toward the gold reference (optional, but recommended). This is
    #    the step that keeps a freshly generated deck from being 2x denser than
    #    the gold. See DECK_STANDARDS.md section 11.
    if ref_cards is not None:
        from .normalize_deck import normalize
        result = normalize(cards, ref_cards, llm_shorten=llm_shorten)
        cards = result["rewritten"]
        if result["review"] and verbose:
            print(f">> normalizacion: {len(result['review'])} card(s) para revision manual:")
            for key, reason in result["review"]:
                print(f"   - {key}: {reason}")

    # 1) Quality gate on the cards themselves.
    problems = verify_cards(cards)
    if problems:
        raise SystemExit(f"verify_cards failed ({len(problems)}): {problems}")

    # 1b) Advisory warnings (do NOT fail the build).
    warnings = warn_cards(cards)
    if warnings and verbose:
        print(f">> {len(warnings)} advertencia(s) (no bloquean):")
        for idx, w in warnings:
            print(f"   - card {idx}: {w}")

    # 1c) Distribution gate: fail a deck whose SHAPE is far from the gold. Only
    #     enforced when a reference is provided (so legacy calls are unaffected).
    if ref_cards is not None and enforce_distribution:
        dist_issues = check_distribution(cards)
        if dist_issues:
            raise SystemExit(
                "check_distribution failed (la baraja es mas densa que la de "
                f"referencia): {dist_issues}"
            )

    # 2) Build the .apkg with the FULL subdeck name and a unique, stable deck id.
    build_deck(deck_name, cards, out_path, verbose=verbose)

    # 3) Quality gate on the built package.
    problems = verify_apkg(out_path)
    if problems:
        raise SystemExit(f"verify_apkg failed ({len(problems)}): {problems}")
    if verbose:
        print(f">> verify: OK ({len(cards)} cards)")

    # 4) Import straight into the (sub)deck. No card moving.
    if do_import:
        _invoke("createDeck", deck=deck_name)  # ensure the subdeck exists
        _invoke("importPackage", path=os.path.abspath(out_path))
        if verbose:
            # sanity check: report how many cards are now in that exact deck
            n = len(_invoke("findCards", query=f'deck:"{deck_name}"'))
            print(f">> imported into '{deck_name}': {n} cards in that deck")
    return len(cards)
