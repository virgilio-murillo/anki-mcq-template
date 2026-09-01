# Deck quality standards (MANDATORY for every deck)

Hard-won rules. Every deck built with this template MUST follow them, and the
build MUST pass `verify_deck.py` before importing into Anki.

## 1. Multiple-choice card structure

- **Front** shows the question + the options, with **no hint** about the correct
  one. (Never put the "correct" highlight in the field shown on the front.)
- **Back** repeats the options with the correct one highlighted, then a verdict
  line, then a full explanation, then optional callouts and links.
- Exactly **4 options** unless there is a strong reason otherwise.

## 2. The correct letter is auto-injected (never hardcode it)

Options are **shuffled**, so the correct letter changes per build. Write
`{{L}}` in the verdict and let the engine substitute the real shuffled letter:

```python
'<div class="verdict">Correct: {{L}} - Amazon DynamoDB</div>'
```

Hardcoding "Correct: C" WILL drift out of sync with the shuffled options. This
was a real bug. `verify_deck.py` fails the build if the verdict letter does not
match the highlighted option.

## 3. Explanations must be self-explanatory on first read

If a card is not understandable the first time you read it, it is not done.
Every back MUST:

- **Define each term before using it** (e.g. "un IdP = Identity Provider...",
  "PII = informacion personal identificable...", "OLAP = analisis...").
- **Connect the scenario's symptom to the solution.** If the question mentions
  "100% CPU", explain WHY the answer fixes that (e.g. stateless -> horizontal
  scaling -> load spread -> CPU drops), not just what the answer is.
- **Refute every distractor, one by one** ("Por que NO las otras, una por una:"
  with a `<ul>` listing each wrong option and why it is wrong). Do not only
  justify the correct answer.
- **Explain why the correct option works**, not just name it.

Structure that works well on the back:
1. `verdict` line (with `{{L}}`).
2. "El problema / Que pide el escenario" — restate the situation in plain words.
3. "Por que la respuesta sirve" — mechanism, with terms defined.
4. "Por que NO las otras, una por una" — `<ul>` refuting each distractor.
5. `extra` callout — one high-value exam gotcha.
6. `links` — clickable references.

## 4. Technical completeness

- The correct option must be **technically complete and correct**, not just
  "the least wrong". Example: "add a NAT gateway" alone is incomplete; the real
  answer is "private subnets whose route table points to a NAT (which egresses
  via the IGW) + security group allowing outbound".
- Verify facts against official AWS docs. Add a dated real-world note if a
  service's availability/behavior changed (e.g. S3 Object Lambda 2025-11-07),
  while keeping the exam answer intact.

## 5. Distractors (for refuerzo cards with generated options)

- Plausible, not obviously wrong.
- Each must be refuted on the back.
- Avoid inventing non-existent features unless clearly flagged as a distractor.

## 6. Preserve review progress (see PRESERVING_PROGRESS.md)

- Update decks with `sync_deck.py` (in-place `updateNoteFields`) or an `.apkg`
  re-import with stable GUIDs and unchanged note type.
- **Never** `deleteNotes` + re-add to "update".
- **Never** change the note type of a studied deck.
- Give every card a stable `key`.
- Back up (`.colpkg`) before bulk changes.

## 7. Always verify before importing

Run `verify_deck.py` on the generated `.apkg` (or on the in-memory cards). It
checks: 20-field integrity, front does not leak the answer, verdict letter
matches the highlighted option, no leftover `{{L}}`, 4 options per card, each
card has a verdict, and each back appears to refute distractors. Do NOT import
a deck that fails verification. This prevents shipping the bugs we already hit.

## 8. Import straight into the target (sub)deck — never move cards by query

Build the `.apkg` with the **full subdeck path** as the deck name (e.g.
`"DVA-C02::02"`) and let `build_deck` derive a **unique deck id from the name**
(pass `deck_id=None`, the default). Then import; Anki places the notes directly
into that subdeck. Use `create_deck.create(...)` for the whole flow
(build -> verify -> import).

**Never** import into a generic deck and then "move the new cards" with a text
query like `-deck:"X"`. That once matched 85 cards from an unrelated SAP-C02
deck and dragged them into the wrong subdeck. If you ever must move cards,
select them by an exact, unique property (their `mcqkey:` tag or their specific
note-type name), never by a broad text search.


## 9. Language & formatting

- Explanations in the user's language (Spanish here).
- No em dashes (use commas, colons, parentheses, or " - ").
- HTML, not markdown, in fields. Use `<b>`, `<code>`, `<ul>/<li>`, `<p>`.
- Use HTML entities for accents in source, or write UTF-8 directly.
