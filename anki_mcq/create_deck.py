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
           ref_cards=None, llm_shorten=None, enforce_distribution=False,
           refocus_llm=None):
    """Build -> verify -> (optionally) import a deck straight into `deck_name`.

    Returns the count of cards on success. Raises if verification fails.

    REFOCUS (see DECK_STANDARDS.md section 12): pass `refocus_llm` (a callable
    like anki_mcq.llm_shorten.llm_shorten with a backend set) to rewrite, one
    model call each, only the cards that show the combo-stacking defect (options
    that all lead with the same service, a convergence cue). Options become
    competing concepts; key/correct are preserved and no examinable concept is
    dropped. Best effort: only the few flagged cards are touched.

    NORMALIZATION (see DECK_STANDARDS.md section 11): pass `ref_cards` (the gold
    reference deck, e.g. from gold_reference.load_gold_reference()) to normalize
    this deck's length distribution toward it BEFORE building. If `llm_shorten`
    is also given, over-budget cards are shortened (one model call each, concepts
    preserved); without it, normalization only plans (no rewrite).

    CONCISENESS is BEST EFFORT: when `ref_cards` is given, `check_distribution`
    reports (as a non-blocking warning) whether the deck still exceeds the
    conciseness goal, but does NOT fail the build. The only HARD length failures
    are the per-card caps in verify_cards (stem>70w, opt>32w). Pass
    `enforce_distribution=True` to turn the shape check into a hard gate. When
    `ref_cards` is None, normalization and the shape check are skipped entirely
    (backward compatible with existing per-deck scripts).
    """
    # 0a) Refocus BEFORE compression: rewrite combo-stacking options into
    #     competing concepts. Runs first because it changes what the options ARE
    #     (usually shortening them), so compression should act on the refocused
    #     text. Best effort: only flagged cards get one model call.
    if refocus_llm is not None:
        from .refocus_deck import refocus
        rf = refocus(cards, llm=refocus_llm)
        cards = rf["rewritten"]
        if verbose and rf["candidates"]:
            print(f">> reenfoque: {len(rf['candidates'])} card(s) con convergence cue")
        if rf["review"] and verbose:
            print(f">> reenfoque: {len(rf['review'])} card(s) para revision manual:")
            for key, reason in rf["review"]:
                print(f"   - {key}: {reason}")

    # 0b) Normalize toward the gold reference (optional, but recommended). This
    #    is the step that keeps a freshly generated deck from being denser than
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

    # 1c) Distribution shape check (BEST EFFORT): report if the deck is denser
    #     than the conciseness goal, but do NOT fail the build. The only hard
    #     length failures are the per-card caps in verify_cards (stem>70,
    #     opt>32). Set enforce_distribution=True to make it a hard gate instead.
    if ref_cards is not None:
        dist_issues = check_distribution(cards)
        if dist_issues:
            if enforce_distribution:
                raise SystemExit(
                    "check_distribution failed (la baraja es mas densa que el "
                    f"objetivo): {dist_issues}"
                )
            elif verbose:
                print(">> distribucion (best effort, no bloquea) - aun por encima del objetivo:")
                for d in dist_issues:
                    print(f"   - {d}")

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
