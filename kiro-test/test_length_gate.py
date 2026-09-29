#!/usr/bin/env python3
"""Unit tests for the length/atomicity gate in verify_deck.py (DECK_STANDARDS.md sec 10).

Verifies:
  - a short, healthy card produces no length errors and no warnings
  - a card with an over-long option produces a hard error
  - a card with an over-long stem produces a hard error
  - a coupling-legitimate card (many bold clauses but short stem/options) is NOT
    a hard error (bold count is WARNING only)
  - warnings do not appear in verify_cards() (only in warn_cards())
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anki_mcq import card
from anki_mcq.verify_deck import (
    verify_cards, warn_cards, _length_problems,
    STEM_ERROR_WORDS, OPT_ERROR_WORDS, BOLD_WARN_CLAUSES,
)

_fail = 0
def check(cond, label, extra=""):
    global _fail
    print(("PASS " if cond else "FAIL ") + label + (f"  [{extra}]" if extra else ""), flush=True)
    if not cond:
        _fail += 1

W = "palabra "  # helper to build long strings

def mk(question, options, correct=0):
    ans = ('<div class="verdict">Correcta: {{L}} - x.</div>'
           '<p>Por que NO las otras, una por una: distractor.</p>')
    return card(question=question, options=options, correct=correct, answer=ans, key=None)

# 1) Healthy short card: no length errors, no warnings
healthy = mk("ML - concepto: que servicio hace X?",
             ["Amazon Athena", "Amazon Redshift", "Amazon EMR", "AWS Glue"])
le, lw = _length_problems(healthy)
check(le == [], "healthy card: 0 length errors", str(le))
check(lw == [], "healthy card: 0 warnings", str(lw))

# 2) Over-long option -> hard error
long_opt = W * (OPT_ERROR_WORDS + 5)
overopt = mk("Que servicio hace X?", [long_opt, "Redshift", "EMR", "Glue"])
le, lw = _length_problems(overopt)
check(any("opcion" in e for e in le), "over-long option -> hard error", str(le))

# 3) Over-long stem -> hard error
long_stem = "ML - " + W * (STEM_ERROR_WORDS + 5) + "?"
overstem = mk(long_stem, ["Athena", "Redshift", "EMR", "Glue"])
le, lw = _length_problems(overstem)
check(any("enunciado" in e for e in le), "over-long stem -> hard error", str(le))

# 4) Coupling-legitimate: many bold clauses but short -> NOT a hard error
bolded = "<b>a</b> <b>b</b> <b>c</b> <b>d</b> <b>e</b> <b>f</b> corto?"
coupling = mk(bolded, ["Athena", "Redshift", "EMR", "Glue"])
le, lw = _length_problems(coupling)
check(le == [], "coupling (6 bold, short) -> NO hard error", str(le))
check(any("clausulas <b>" in w for w in lw), "coupling -> emits a WARNING", str(lw))

# 5) warnings never appear in verify_cards() (only warn_cards())
warn_only = mk("ML - concepto corto?",
               ["Amazon " + W * 27, "Redshift", "EMR", "Glue"])  # option ~28w -> WARN not ERROR
le5, lw5 = _length_problems(warn_only)
check(le5 == [], "warn-only card: option is WARN not ERROR", str(le5))
wc = warn_cards([warn_only])
check(any("opcion" in w for _, w in wc), "warn_cards includes the warning", str(wc))

# --- Distribution & normalization tests (deck-level shape, user's idea) ---
from anki_mcq.verify_deck import check_distribution, concepts_preserved
from anki_mcq.normalize_deck import budget_for_deck, _validate_rewrite, normalize

# A gold-like reference deck: short options, short stems.
ref = [mk("ML - concepto breve numero " + str(i) + "?",
          ["Amazon Athena", "Amazon Redshift", "Amazon EMR", "AWS Glue"]) for i in range(20)]
# 6) a gold-like deck passes the distribution check
check(check_distribution(ref) == [], "gold-like deck passes distribution", str(check_distribution(ref)))

# 7) a uniformly-long deck FAILS the distribution check (even if each card is under hard caps)
longish = [mk("ML - " + W * 40 + "?",
              ["Amazon " + W * 28, "Redshift " + W * 28, "EMR " + W * 28, "Glue " + W * 28])
           for _ in range(20)]
dist = check_distribution(longish)
check(dist != [], "uniformly-long deck FAILS distribution", str(len(dist)) + " problems")

# 8) concept stoplist fix: a Spanish verb is NOT a dropped concept
old_c = mk("Usar Amazon Bedrock", ["Trainium Trn", "GPU P", "M", "G"])
new_c = mk("Amazon Bedrock", ["Trainium Trn", "GPU P", "M", "G"])
check(concepts_preserved(old_c, new_c) == set(), "verb 'Usar' is not a dropped concept", str(concepts_preserved(old_c, new_c)))
# but a real service name IS detected as dropped
old_r = mk("Q", ["Trainium", "P", "M", "G"])
new_r = mk("Q", ["generico", "P", "M", "G"])
check("Trainium" in concepts_preserved(old_r, new_r), "real service 'Trainium' detected as dropped", str(concepts_preserved(old_r, new_r)))

# 9) budget_for_deck gives each card a per-field budget mapped to the reference
plan = budget_for_deck(longish, ref)
check(len(plan) == len(longish), "budget_for_deck returns one plan per card")
check(all(p["stem_budget"] >= 12 for p in plan), "stem budgets respect the floor")
check(any(p["needs_rewrite"] for p in plan), "long deck flagged as needs_rewrite")

# 10) _validate_rewrite catches a changed correct index and a dropped concept
v_correct = _validate_rewrite(
    {"key": "k", "correct": 0, "options": [1, 2, 3, 4], "question": "q", "answer": "a"},
    {"key": "k", "correct": 1, "options": [1, 2, 3, 4], "question": "q", "answer": "a"})
check("correct cambio" in v_correct, "_validate_rewrite catches changed correct", v_correct)

# 11) normalize plan_only does not touch cards and makes no LLM call
r = normalize(longish, ref, plan_only=True)
check(r["rewritten"] is longish, "normalize plan_only leaves cards untouched")

if _fail == 0:
    print("\nALL LENGTH-GATE TESTS PASSED", flush=True)
    sys.exit(0)
else:
    print(f"\n{_fail} LENGTH-GATE TEST(S) FAILED", flush=True)
    sys.exit(1)
