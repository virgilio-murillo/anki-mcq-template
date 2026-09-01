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

from anki_mcq import build_deck
from verify_deck import verify_cards, verify_apkg

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


def create(deck_name, cards, out_path, do_import=True, verbose=True):
    """Build -> verify -> (optionally) import a deck straight into `deck_name`.

    Returns the count of cards on success. Raises if verification fails.
    """
    # 1) Quality gate on the cards themselves.
    problems = verify_cards(cards)
    if problems:
        raise SystemExit(f"verify_cards failed ({len(problems)}): {problems}")

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
