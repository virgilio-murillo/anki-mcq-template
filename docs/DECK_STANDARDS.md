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
- **Balanced length & specificity (MANDATORY).** The 4 options must be of
  comparable length and detail. NEVER make the correct option markedly longer or
  more specific than the distractors: no option may exceed ~1.4x the average
  length of the others. A learner must not be able to pick the answer by its
  shape (the "longest/most-detailed option is correct" tell). Fix by RAISING the
  distractors to the same level (make them specific, technically plausible near-
  misses), NOT by shortening the correct one. Deciding between options should be
  HARD because they look similar.
- Distractors must be concrete technical claims (a believable wrong mechanism,
  wrong parameter, wrong service role), never vague fillers like "all of them do
  the same" or "none apply".

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

## 10. Atomicity: one examinable core per card, kept short (MANDATORY)

Every card turns on **ONE examinable core**: the single fact or decision under
test. A learner who knows only that core must be able to answer. Cards must be
**concise, clear and short** to read, even when the concept is hard.

### Legitimate coupling (allowed)

A second concept MAY appear on the same card when it is an **inseparable
dependency** of the core: the core is undecidable without it. Correct examples:
- `InitialVariantWeight` needs the fact that "one SageMaker endpoint hosts
  several `ProductionVariant`s"; you cannot test the weight without it.
- Choosing between `GuardrailIdentifier` alone vs `GuardrailIdentifier +
  PromptRouterArn`: the coupling IS the testable axis.

Coupling is fine. The rules below never punish it. Counting concepts, bold
clauses or services is NOT how we detect the defect (that would punish real
professional-tier depth). We measure LENGTH.

### Artificial stacking (prohibited)

The real defect is **verbose padding**, not multiple concepts:
- Stems that pile up unrelated requirements ("highly optimized AND scalable AND
  minimize time AND cost AND without changing the client AND minimal overhead")
  when the core is simply "which EC2 instance for LLM training".
- Options that are full-paragraph architectures of 4-5 services when the choice
  is one thing (e.g. "multi-agent vs monolith"). The option's **head** should
  NAME the concept; the justification ("which ensures that...", "allowing the
  system to...") belongs on the BACK, not glued onto the option.

Measured on real decks: in the gold MLA-C01 deck an option is a 6-word head that
names the concept and stops. In the bad AIP-C01 decks each option dragged ~76% of
its text as a justification tail. That tail is what makes cards hard to READ (not
hard to reason), and it is what these rules cut. This is the same idea as rule 5
("options name the concept, never explain it") applied as a hard length cap.

### The delete test (operational rule for authors and reviewers)

For each extra clause in a stem, or tail in an option, ask: **"if I remove it,
is the card still answerable and does the correct answer stay the same?"**
- YES it stays answerable -> the clause was padding. Cut it.
- NO it becomes ambiguous/undecidable -> it is a legitimate dependency. Keep it.

### Length limits derived from MLA-C01 (the healthy baseline)

Measured over the 224-card MLA gold deck (HTML stripped): stem max 67 words,
option max 29 words / 182 chars. The gate (`verify_deck.py`) enforces:

| Field | Target (WARNING) | Hard limit (ERROR, fails the gate) |
|---|---|---|
| Stem (question) | <= 45 words | **> 70 words** |
| Each option | <= 25 words | **> 32 words** |
| Option chars | <= 200 chars (WARNING only) | (no char ERROR) |
| Bold `<b>` clauses in stem | <= 5 (WARNING if more) | (no bold ERROR) |

These thresholds produce **0 false positives** on MLA-C01. Never lower the stem
ERROR to 67 or below (MLA has legitimate 65-67w cards). Bold-clause and
service-count checks are **WARNINGS only** so legitimate coupling never fails.

### Fixing a card: SHORTEN, almost never SPLIT

Most defects are verbose options on a single-core card: **shorten in place,
keeping the same `key`** (preserves review progress; see section 6 and
PRESERVING_PROGRESS.md). Only SPLIT into new cards when the delete test leaves
**two independent examinable cores** in the same stem, each needing a different
correct answer. Splitting creates new-key cards that start with no history, so
when in doubt, SHORTEN.

## 11. MANDATORY final step: normalize the deck against the gold deck

Per-card caps are a floor, not the goal. A freshly generated deck (especially
from an exam dump) tends to be uniformly verbose and, even under the hard caps,
ends up roughly twice as dense as the gold MLA deck and tiring to study. So
after generating any new deck, run the NORMALIZATION step (`normalize_deck.py`)
BEFORE importing. This is the guardrail that stops the "everything is long"
regression from happening again on the next exam.

**How it works (the idea):** it maps the new deck's length distribution onto a
known-good REFERENCE deck (MLA-C01) by quantile. Each card is assigned the word
budget that the SAME percentile has in the reference:
- the median card gets the reference's median size,
- a card that genuinely needs more text (high percentile) still gets a high-
  percentile budget - it stays one of the longest, but on a healthy scale,
- a short card is left alone.

This preserves the RELATIVE ordering (cards that need more text stay longest)
while pulling the whole shape onto the gold deck. It neither over-compresses the
cards that need room nor leaves the easy ones bloated. Example: if the new deck
averages 1000 words and the gold averages 500, a 1500-word card lands near ~750,
not chopped to the mean.

**The rewrite uses an LLM, at most ONE call per card.** Computing the budget is
deterministic (no model). Actually shortening prose without losing meaning needs
an LLM, so each over-budget card gets exactly one call with its per-field word
budget and the hard rules below. Cards already within budget are not touched
(zero calls). A card whose rewrite fails verification is REPORTED for human
review; we do not retry in a loop (one-call budget).

**Invariants enforced automatically after each rewrite (else revert + flag):**
- `key` and `correct` unchanged (never lose review progress; never move the
  right answer),
- no examinable concept dropped: every AWS service / API / parameter present in
  the old card must still appear somewhere in the new card. If it is removed
  from an option, it MUST be relocated to the back (`answer`), never deleted.
  Verified by `concepts_preserved()`,
- exactly 4 options, still mutually distinguishable.

**Deck-level distribution gate.** `verify_deck.check_distribution(cards)` fails a
deck whose shape is far from the gold: option p90 > 22w, or > 15% of options
> 25w, or stem p90 > 50w, or > 35% of stems > 45w. The gold MLA deck passes
this with margin; a mostly-long deck does not. Run it as the acceptance check
for the normalization step.

Usage sketch:

```python
from anki_mcq.normalize_deck import normalize
from anki_mcq.gold_reference import load_gold_reference
from anki_mcq.llm_shorten import llm_shorten

mla_cards = load_gold_reference()          # 224 MLA cards, no side effects
# NOTE: ref_cards is POSITIONAL (not reference_cards=).
result = normalize(new_cards, mla_cards, llm_shorten=llm_shorten)
# llm_shorten(card_dict, prompt_str) -> rewritten card_dict, called <=1x per card
new_cards = result["rewritten"]
for key, reason in result["review"]:
    ...  # human-review the few cards the LLM could not safely shorten
```

Or let `create()` do it in one shot (see `create_deck.create(ref_cards=...)`):

```python
from anki_mcq import create
from anki_mcq.gold_reference import load_gold_reference
from anki_mcq.llm_shorten import llm_shorten
create(deck_name="SAA-C03::01", cards=new_cards, out_path="out/saa_01.apkg",
       ref_cards=load_gold_reference(), llm_shorten=llm_shorten)
# create() normalizes, runs check_distribution as a hard gate, builds, verifies, imports.
```


## 12. Refocus options onto the ROOT CONCEPT (convergence-cue fix)

A card can pass every length check yet still be wrong in a subtler way: if the
SAME service leads all four options (e.g. every option starts "BDA con ..."),
the axis of decision is "which combo of auxiliary services", not the examinable
concept. This is a "convergence cue" (Haladyna & Downing) and fails the
"cover-the-options test": if an element appears in EVERY option, it belongs in
the STEM, not repeated in each option.

This is a DIFFERENT defect from length. `normalize_deck.py` only shortens; it
does not refocus. `refocus_deck.py` handles this:

- `needs_refocus(card)` detects it deterministically (no LLM): all options share
  the same leader service AND the options stack several different auxiliary
  services. This is a minority of cards (measured ~4% on AIP-C01), so refocus is
  best effort and touches few cards. Legitimate single-service variation (four
  SageMaker VPC modes, four Bedrock agent designs, temperature tuning) is NOT
  flagged.
- For each flagged card, one LLM call rewrites ONLY the options into COMPETING
  concepts: the correct one stays the correct concept from the source, and the
  three distractors become OTHER real, plausible services/approaches for the
  same goal (never invented). The shared service moves to the stem. Auxiliary
  detail moves to the back (`answer`), never deleted.
- `_validate_refocus` enforces: key and correct unchanged, exactly 4 options,
  no examinable concept dropped, and the convergence cue actually resolved. A
  card that still looks wrong is reported for review (no retry).

Good vs bad (real examples):
- BAD (convergence cue): four options all "BDA con <different combo>". Axis =
  auxiliary combo. Distracts from the root concept (BDA), long, teaches nothing.
- GOOD (competing concepts): options lead with distinct approaches, e.g. "job de
  model evaluation de Bedrock" / "Comprehend para similitud" / "Step Functions
  con logica propia" / "Lambda con distancia de Levenshtein". One correct, short,
  hard because of the concept.

RUN ORDER: refocus BEFORE normalize (refocusing changes what the options are and
usually shortens them; compress afterward). `create()` does both when you pass
`refocus_llm` and `ref_cards`:

```python
from anki_mcq import create
from anki_mcq.gold_reference import load_gold_reference
from anki_mcq.llm_shorten import llm_shorten, set_backend
set_backend(my_model_fn)
create(deck_name="SAA-C03::01", cards=new_cards, out_path="out/saa_01.apkg",
       refocus_llm=llm_shorten,                 # step 12: refocus options
       ref_cards=load_gold_reference(), llm_shorten=llm_shorten)  # step 11: shorten
```

`verify_deck.warn_cards` also emits a non-blocking advisory (the cover-the-options
test) whenever a token leads every option, so a future deck surfaces the issue
even if refocus is not run.
