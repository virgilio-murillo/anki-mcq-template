# anki-mcq-template

A small, reusable template for building **multiple-choice Anki decks** with
[genanki](https://github.com/kerrickstaley/genanki) — with a clean, didactic
card design and the anti-patterns already fixed.

![format](https://img.shields.io/badge/format-.apkg-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green)

## Why this template

Building MCQ cards by hand is easy to get wrong. This template bakes in the
lessons learned:

- **The front never leaks the answer.** Options are stored in two fields: a
  neutral one shown on the front, and a marked one (correct highlighted) shown
  only on the back. (A naive single-field approach shows the green ✓ on the
  question side — useless as a test.)
- **Options are shuffled** deterministically per card, so the correct letter is
  not predictable across the deck. You learn the concept, not the position.
- **Didactic back:** a verdict line, an explanation, and optional callout boxes
  (amber "exam tip", red "heads up") plus a links section.
- **Stable IDs:** re-importing an updated `.apkg` updates the same cards instead
  of duplicating them.

## Card anatomy

**Front:** question + neutral options (A, B, C, D).

**Back:** the same options with the correct one highlighted in green (✓), a
`verdict` line, the explanation, optional callouts, and links.

## Quick start

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python example_deck.py     # writes example_deck.apkg
```

Then import `example_deck.apkg` into Anki (double-click) or, if Anki is running
with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on:

```bash
./.venv/bin/python import_to_anki.py example_deck.apkg
```

## Writing your own deck

```python
from anki_mcq import card, build_deck

cards = [
    card(
        question="What does X do?",
        options=["wrong A", "correct B", "wrong C", "wrong D"],
        correct=1,                       # 0-based index into options
        answer=(
            '<div class="verdict">Correct: {{L}} - option B</div>'
            '<p>Because ...</p>'
            '<div class="extra"><span class="h">Exam tip</span>...</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://example.com">docs</a></div>'
        ),
    ),
    # ...more cards
]

build_deck("My Deck Name", cards, "my_deck.apkg")
```

### The correct letter: use `{{L}}`, never hardcode it

Options are **shuffled**, so the correct answer's letter changes. **Never** write
`Correct: C` in the answer text (it will drift out of sync with the shuffled
options). Instead, write the placeholder `{{L}}` and `build_deck` substitutes the
real shuffled letter:

```python
'<div class="verdict">Correct: {{L}} - Amazon DynamoDB</div>'
# renders as e.g. "Correct: A - Amazon DynamoDB", always matching the highlighted option
```

### The `answer` field is HTML

Anki renders fields as HTML. Useful building blocks (all styled by the template CSS):

| Snippet | Purpose |
|---|---|
| `<div class="verdict">Correct: {{L}} - ...</div>` | Green verdict line (`{{L}}` becomes the real letter; put it first) |
| `<div class="extra"><span class="h">Exam tip</span> ...</div>` | Amber callout |
| `<div class="warn"><span class="h">Heads up</span> ...</div>` | Red callout |
| `<div class="links"><span class="h">Links</span><a href="...">...</a></div>` | Links block |
| `<code>...</code>`, `<b>...</b>`, `<ul><li>...</li></ul>` | Inline formatting |

Use HTML entities for accents in source (e.g. `&oacute;` for ó) if you want to
keep files ASCII-safe, or just write UTF-8 directly — both work.

## Card-writing best practices

Baked into the design, but worth stating (full list in
[DECK_STANDARDS.md](DECK_STANDARDS.md) — MANDATORY reading):

- **One concept per card** (minimum information principle).
- **Prefix the topic** in the question so it reads well when reviews are interleaved.
- **Self-explanatory on first read:** define each term before using it, connect
  the scenario's symptom to why the answer fixes it.
- **Refute every distractor, one by one** on the back — not just justify the correct one.
- **Technically complete** correct option (not "least wrong").
- **Make distractors plausible.**
- **Keep 10–20 new cards/day** in Anki's deck settings to avoid review pileup.

## Updating a deck WITHOUT losing review progress

This is critical: **do not delete + re-import to update a studied deck** — it
resets each card's scheduling (due/interval/ease/reps and history).

Two safe options:

1. **In-place sync (recommended, Anki running):** use `sync_deck.py`, which
   edits existing notes via AnkiConnect `updateNoteFields` (progress kept) and
   only adds genuinely new cards. It never deletes.
   ```python
   from anki_mcq import card
   from sync_deck import sync
   cards = [ card(question="...", options=[...], correct=1, answer="...",
                  key="my-deck-q1") ]   # stable key
   sync(deck_name="DVA-C02::01", cards=cards)
   ```
2. **Re-import an `.apkg`:** `build_deck` writes stable GUIDs, so re-importing
   updates matched notes in place **if the note type is unchanged** and you
   leave "Import any learning progress" unchecked in the import dialog.

Full rules and rationale: see [PRESERVING_PROGRESS.md](PRESERVING_PROGRESS.md).
Always back up first: File -> Export -> Anki Collection Package (`.colpkg`).

## Files

| File | Purpose |
|---|---|
| `anki_mcq.py` | The reusable engine: model, CSS, `card()`, `build_deck()` (stable GUIDs + per-name deck id) |
| `create_deck.py` | Recommended flow: build -> verify -> import straight into the target (sub)deck |
| `sync_deck.py` | Update a deck in place via AnkiConnect, preserving review progress |
| `verify_deck.py` | Quality gate — run before importing (enforces the standards) |
| `example_deck.py` | Minimal 3-card example (passes `verify_deck.py`) |
| `import_to_anki.py` | Import a `.apkg` via AnkiConnect |
| `DECK_STANDARDS.md` | MANDATORY quality standards every deck must follow |
| `PRESERVING_PROGRESS.md` | How to update decks without losing scheduling |
| `requirements.txt` | `genanki` |

## Recommended flow for a NEW deck

Use `create_deck.create`, which builds, runs the quality gate, and imports the
package **directly into the target subdeck** (no card-moving, no ambiguous
queries):

```python
from anki_mcq import card
from create_deck import create

cards = [ card(question="...", options=[...], correct=1, answer="...",
               key="dva02-q1") ]
create(deck_name="DVA-C02::02", cards=cards, out_path="DVA-C02_02.apkg")
```

`build_deck` derives a unique deck id from the name, so each subdeck imports
cleanly to its own place.

## Quality gate (run before importing)

Every deck must pass `verify_deck.py`, which enforces [DECK_STANDARDS.md](DECK_STANDARDS.md):
front does not leak the answer, verdict letter matches the highlighted option,
no leftover `{{L}}`, 4 options per card, each card has a verdict, and each back
refutes its distractors.

```bash
./.venv/bin/python verify_deck.py my_deck.apkg   # must print "OK (0 problemas)"
```

Do not import a deck that fails verification.

## Requirements

- Python 3.8+
- `genanki`
- (optional) Anki + AnkiConnect add-on for `import_to_anki.py`

## License

MIT — see [LICENSE](LICENSE).
