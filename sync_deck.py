#!/usr/bin/env python3
"""
sync_deck.py - Update an MCQ deck in Anki WITHOUT losing review progress.

Why this exists
---------------
Deleting notes + re-importing an .apkg resets each card's scheduling
(due/interval/ease/reps/lapses and review history), because delete removes the
cards. To keep your progress, we edit the EXISTING notes in place via
AnkiConnect's `updateNoteFields`, and only `addNote` for genuinely new cards.
We NEVER call deleteNotes here.

How it works
------------
- Each card has a stable `key` (or question) -> stored in a hidden tag
  `mcqkey:<hash>` on the note. On sync we match by that tag.
- Existing note found  -> updateNoteFields (scheduling preserved).
- No match             -> addNote (new card).
- Notes in the deck that are no longer in your source are LEFT ALONE (reported,
  not deleted) so you never lose progress by accident.

Requirements: Anki running + AnkiConnect add-on (localhost:8765).
IMPORTANT: do not have the target notes open in the Anki Browser during sync
(AnkiConnect issue #82 makes updates silently no-op).

Usage
-----
    from anki_mcq import card, make_model, render_options
    from sync_deck import sync

    cards = [ card(...), ... ]
    sync(deck_name="DVA-C02::01", cards=cards)
"""
import hashlib
import json
import urllib.request

from anki_mcq import make_model, render_options, DEFAULT_MODEL_ID

ANKICONNECT = "http://localhost:8765"
KEY_TAG_PREFIX = "mcqkey:"


def _invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKICONNECT, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect '{action}': {data['error']}")
    return data["result"]


def _key_tag(card_dict):
    raw = card_dict.get("key") or card_dict["question"]
    h = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]
    return KEY_TAG_PREFIX + h


def _ensure_model(model_name, model_id):
    names = _invoke("modelNames")
    if model_name not in names:
        # Create the model by importing a throwaway note via addNote requires the model.
        # genanki can't push a model directly; instead create it via AnkiConnect.
        m = make_model(model_id, model_name)
        tmpl = m.templates[0]
        _invoke("createModel",
                modelName=model_name,
                inOrderFields=[f["name"] for f in m.fields],
                css=m.css,
                cardTemplates=[{"Name": tmpl["name"], "Front": tmpl["qfmt"], "Back": tmpl["afmt"]}])


def sync(deck_name, cards, model_name="MCQ (didactic)", model_id=DEFAULT_MODEL_ID,
         shuffle_seed_base=1, verbose=True):
    """Sync cards into `deck_name`, preserving scheduling of existing notes.

    Returns a summary dict: {"updated": n, "added": n, "orphans": [note_ids]}.
    """
    _invoke("createDeck", deck=deck_name)
    _ensure_model(model_name, model_id)

    # Map existing notes in this deck by their mcqkey tag.
    existing_ids = _invoke("findNotes", query=f'deck:"{deck_name}"')
    existing = _invoke("notesInfo", notes=existing_ids) if existing_ids else []
    by_key = {}
    for n in existing:
        for t in n.get("tags", []):
            if t.startswith(KEY_TAG_PREFIX):
                by_key[t] = n["noteId"]
                break

    seen_keys = set()
    updated = added = 0
    for i, c in enumerate(cards):
        neutral, marked, letter = render_options(c["options"], c["correct"], seed=shuffle_seed_base + i)
        answer = c["answer"].replace("{{L}}", letter)
        fields = {"Question": c["question"], "OptionsQ": neutral, "OptionsA": marked, "Answer": answer}
        ktag = _key_tag(c)
        seen_keys.add(ktag)
        if ktag in by_key:
            # UPDATE IN PLACE -> scheduling preserved.
            _invoke("updateNoteFields", note={"id": by_key[ktag], "fields": fields})
            updated += 1
        else:
            _invoke("addNote", note={
                "deckName": deck_name, "modelName": model_name,
                "fields": fields, "tags": [ktag],
                "options": {"allowDuplicate": False},
            })
            added += 1

    orphans = [nid for tag, nid in by_key.items() if tag not in seen_keys]
    if verbose:
        print(f">> sync '{deck_name}': updated={updated} added={added} orphans={len(orphans)}", flush=True)
        if orphans:
            print(f"   NOTE: {len(orphans)} note(s) exist in the deck but not in your source.")
            print(f"   They were LEFT ALONE (not deleted) to protect progress. IDs: {orphans}")
            print("   Delete them manually in Anki only if you are sure.")
    return {"updated": updated, "added": added, "orphans": orphans}
