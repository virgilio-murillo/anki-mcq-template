# Preserving Anki review progress when updating a deck

This is the most important operational rule in this repo. Read it before you
touch an already-studied deck.

## The problem (learned the hard way)

Anki review progress (a card's `due` date, `interval`, `ease`/factor, `reps`,
`lapses`, and the `revlog` history) lives on the **card**, not on the `.apkg`
file. If you "update" a deck by deleting the notes and re-importing, Anki
**deletes those cards and creates brand-new ones** -> all progress is lost.

Two things reset progress:

1. **`deleteNotes` (delete + re-add).** Deleting a note deletes its cards and
   their scheduling. Never do this to "update" content.
2. **Changing the note type / model.** If the model structure changes (fields,
   templates, or a different model), Anki can't update in place and may
   regenerate cards.

## The rule

- **Edit content in place.** Use AnkiConnect `updateNoteFields` on the existing
  note ID. It changes only the text; scheduling is untouched. Use `sync_deck.py`
  in this repo, which does exactly this.
- **Keep the note type stable.** Do not change the model's fields/templates/ID
  once a deck has been studied. (This template's model is fixed; don't bump the
  model id for content edits.)
- **Use stable GUIDs / keys.** `build_deck` derives each note's GUID from
  `card["key"]` (or the question). Keep the key immutable so a re-import updates
  the same note instead of creating a duplicate. Prefer an explicit `key`, e.g.
  `key="dva-c02-01-lambda-envvars"`.
- **Never import the author's scheduling.** When importing an `.apkg` in the
  Anki GUI (23.10+), leave **"Import any learning progress" unchecked** so your
  local scheduling survives. `.apkg` files from `build_deck` carry no scheduling.
- **Never `deleteNotes` to update.** If a card is obsolete, remove it
  deliberately in Anki; don't wipe-and-rebuild the whole deck.

## Two safe ways to update a studied deck

### A) In-place sync via AnkiConnect (recommended, preserves progress)

```python
from anki_mcq import card
from sync_deck import sync

cards = [
    card(question="...", options=[...], correct=1, answer="...",
         key="dva-c02-01-q1"),   # stable key
    # ...
]
sync(deck_name="DVA-C02::01", cards=cards)
```

`sync` updates existing notes in place (progress kept), adds only new ones, and
**leaves orphans alone** (never deletes) — it just reports them.

### B) Re-import an .apkg with stable GUIDs (also preserves progress)

`build_deck` writes stable GUIDs, so re-importing the `.apkg` updates matched
notes in place **as long as the note type is unchanged** and you leave "Import
any learning progress" unchecked. Prefer method A when Anki is running, because
it needs no import-dialog options.

## Before any bulk change: back up

Export a full-collection backup first (includes scheduling):
File -> Export -> "Anki Collection Package" (`.colpkg`). If anything goes wrong,
you can restore it.

## Quick reference

| Action | Progress kept? |
|---|---|
| `updateNoteFields` / `sync_deck.py` | Yes |
| `.apkg` re-import, same GUID + same note type, no learning-progress import | Yes |
| `changeDeck` (move card to another deck) | Yes — moving decks does NOT reset scheduling |
| `deleteNotes` then re-add | No — resets scheduling |
| Change note type / model structure | No — can regenerate cards |
| Import with "Import any learning progress" checked | Adopts author's intervals (usually not what you want) |

## Do NOT move cards by broad text query

When placing a new deck, import it straight into the target subdeck (see
`create_deck.py` and DECK_STANDARDS.md #8). Do **not** import into a generic
deck and then move "the new cards" with a query like `-deck:"X"`: that once
matched 85 cards from an unrelated deck and moved them by mistake. Moving cards
does not lose scheduling, but moving the WRONG cards still disrupts the user.
If you must move cards, select them by an exact unique property (their
`mcqkey:` tag or specific note-type name), never a broad text search.
