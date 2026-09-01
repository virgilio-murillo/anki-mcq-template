#!/usr/bin/env python3
"""
anki_mcq — Reusable multiple-choice Anki template.

Design goals (learned the hard way):
- The FRONT shows the question + neutral options (NO hint about which is correct).
- The BACK shows the options again with the correct one highlighted, plus a
  verdict line and a didactic explanation with optional callout boxes and links.
- Options are shuffled deterministically per card so the correct letter is not
  predictable across the deck (you learn the concept, not the position).

Usage:

    from anki_mcq import card, build_deck

    cards = [
        card(
            question="What does X do?",
            options=["wrong A", "correct B", "wrong C", "wrong D"],
            correct=1,                      # 0-based index into `options`
            answer=(
                '<div class="verdict">Correct: B</div>'
                '<p>Because ...</p>'
                '<div class="extra"><span class="h">Exam tip</span>...</div>'
                '<div class="links"><span class="h">Links</span>'
                '<a href="https://...">docs</a></div>'
            ),
        ),
        # ...
    ]

    build_deck("My Deck Name", cards, "my_deck.apkg")

Then import my_deck.apkg into Anki (double-click) or use import_to_anki.py.
"""
import random
import genanki

# Stable IDs so re-importing UPDATES cards instead of duplicating them.
# Change these if you want a separate, independent template/deck.
DEFAULT_MODEL_ID = 1607393512
DEFAULT_DECK_ID = 2059400110

_LETTERS = "ABCDEFGH"

CSS = """
.card {
  font-family: -apple-system, Helvetica, Arial, sans-serif;
  font-size: 18px; line-height: 1.55; color: #1a1a2e; background: #ffffff;
  text-align: left; padding: 18px 22px; max-width: 800px; margin: 0 auto;
}
.q { font-weight: 600; font-size: 19px; margin-bottom: 12px; }
.opts { margin: 6px 0; }
.opt {
  display: block; margin: 7px 0; padding: 9px 13px;
  border: 1px solid #d0d0e0; border-radius: 7px; background: #fafaff;
}
.opt .k { font-weight: 700; color: #0b5394; margin-right: 6px; }
.opt.correct { background: #e7f6e7; border-color: #4caf50; }
.opt.correct .k { color: #2e7d32; }
.opt.correct::after { content: " \\2713"; color: #2e7d32; font-weight: 700; }
hr#answer { border: none; border-top: 2px solid #d0d0e0; margin: 16px 0; }
.ans { font-size: 17px; }
.verdict { font-weight: 700; color: #2e7d32; font-size: 17px; margin-bottom: 8px; }
b, strong { color: #0b5394; }
code {
  background: #f0f0f0; color: #c7254e; padding: 1px 5px; border-radius: 4px;
  font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 15px;
}
ul { margin: 8px 0 8px 4px; padding-left: 20px; }
li { margin: 5px 0; }
a { color: #1155cc; text-decoration: none; word-break: break-all; }
a:hover { text-decoration: underline; }
.extra {
  margin-top: 14px; padding: 10px 14px; background: #fff8e1;
  border-left: 4px solid #f0ad4e; border-radius: 4px; font-size: 15px;
}
.extra .h { font-weight: 700; color: #8a6d00; display: block; margin-bottom: 4px; }
.warn {
  margin-top: 14px; padding: 10px 14px; background: #fdecea;
  border-left: 4px solid #d9534f; border-radius: 4px; font-size: 15px;
}
.warn .h { font-weight: 700; color: #a94442; display: block; margin-bottom: 4px; }
.links { margin-top: 12px; font-size: 14px; color: #555; }
.links .h { font-weight: 700; display: block; margin-bottom: 3px; color: #444; }
"""


def make_model(model_id=DEFAULT_MODEL_ID, name="MCQ (didactic)"):
    """Build the multiple-choice note model.

    4 fields:
      Question  - the prompt
      OptionsQ  - neutral options (shown on the FRONT, no hint)
      OptionsA  - options with the correct one marked (shown on the BACK)
      Answer    - verdict + explanation + links (shown on the BACK)
    """
    return genanki.Model(
        model_id,
        name,
        fields=[
            {"name": "Question"},
            {"name": "OptionsQ"},
            {"name": "OptionsA"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "MC",
                "qfmt": '<div class="q">{{Question}}</div>'
                        '<div class="opts">{{OptionsQ}}</div>',
                "afmt": '<div class="q">{{Question}}</div>'
                        '<div class="opts">{{OptionsA}}</div>'
                        '<hr id="answer"><div class="ans">{{Answer}}</div>',
            }
        ],
        css=CSS,
    )


def render_options(options, correct_index, seed):
    """Shuffle options deterministically and return (neutral_html, marked_html, correct_letter)."""
    idx = list(range(len(options)))
    random.Random(seed).shuffle(idx)
    neutral, marked = [], []
    correct_letter = "?"
    for pos, orig in enumerate(idx):
        k = _LETTERS[pos]
        opt = options[orig]
        neutral.append(f'<span class="opt"><span class="k">{k}.</span>{opt}</span>')
        cls = "opt correct" if orig == correct_index else "opt"
        if orig == correct_index:
            correct_letter = k
        marked.append(f'<span class="{cls}"><span class="k">{k}.</span>{opt}</span>')
    return "".join(neutral), "".join(marked), correct_letter


def card(question, options, correct, answer):
    """Define one MCQ card. `correct` is a 0-based index into `options`.
    Returns a plain dict consumed by build_deck().
    """
    if not (0 <= correct < len(options)):
        raise ValueError(f"correct index {correct} out of range for {len(options)} options")
    return {"question": question, "options": options, "correct": correct, "answer": answer}


def build_deck(deck_name, cards, out_path,
               deck_id=DEFAULT_DECK_ID, model_id=DEFAULT_MODEL_ID,
               model_name="MCQ (didactic)", shuffle_seed_base=1, verbose=True):
    """Build an .apkg from a list of card() dicts.

    Options are shuffled per card using (shuffle_seed_base + index) so the layout
    is stable across reviews but the correct letter is not predictable deck-wide.
    """
    model = make_model(model_id, model_name)
    deck = genanki.Deck(deck_id, deck_name)
    for i, c in enumerate(cards):
        neutral, marked, _ = render_options(c["options"], c["correct"], seed=shuffle_seed_base + i)
        deck.add_note(genanki.Note(model=model, fields=[c["question"], neutral, marked, c["answer"]]))
    genanki.Package(deck).write_to_file(out_path)
    if verbose:
        print(f">> Wrote {len(cards)} cards -> {out_path}", flush=True)
    return out_path
