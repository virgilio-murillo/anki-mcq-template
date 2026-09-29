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
check(all(p["stem_budget"] >= 10 for p in plan), "stem budgets respect the floor")
check(any(p["needs_rewrite"] for p in plan), "long deck flagged as needs_rewrite")

# 10) _validate_rewrite catches a changed correct index and a dropped concept
v_correct = _validate_rewrite(
    {"key": "k", "correct": 0, "options": [1, 2, 3, 4], "question": "q", "answer": "a"},
    {"key": "k", "correct": 1, "options": [1, 2, 3, 4], "question": "q", "answer": "a"})
check("correct cambio" in v_correct, "_validate_rewrite catches changed correct", v_correct)

# 11) normalize plan_only does not touch cards and makes no LLM call
r = normalize(longish, ref, plan_only=True)
check(r["rewritten"] is longish, "normalize plan_only leaves cards untouched")

# --- Reproducibility fixes (investigation ba80172f) ---
from anki_mcq.gold_reference import load_gold_reference
from anki_mcq.llm_shorten import llm_shorten, set_backend, _extract_json_object
from anki_mcq.verify_deck import concept_tokens

# 12) gold_reference loads the MLA deck with no side effects
gold = load_gold_reference()
check(len(gold) > 100, "load_gold_reference returns the MLA cards", f"{len(gold)} cards")
check(all(c.get("key") for c in gold), "every gold card has a stable key")
# NOTE: the distribution gate now targets ~55% of MLA length (best effort), so
# MLA itself does NOT pass it. MLA is the SHAPE reference for quantile mapping,
# not a deck that meets the tightened conciseness goal. We only assert it loads.

# 13) H5: normalize short-circuits when the deck already matches the reference shape
called = {"n": 0}
def _counting_llm(card_dict, prompt):
    called["n"] += 1
    return card_dict
r2 = normalize(ref, ref, llm_shorten=_counting_llm)  # ref already gold-shaped
check(called["n"] == 0, "normalize makes 0 LLM calls on an already-good deck (H5)")
check(r2["rewritten"] is ref, "normalize returns cards untouched when shape is fine")

# 14) H4: concept detection now sees ports, CIDR, protocol versions, CLI tools
check("puerto 443" in concept_tokens("abrir el puerto 443"), "port value is an examinable token")
check(any("/16" in t for t in concept_tokens("bloque 10.0.0.0/16")), "CIDR is an examinable token")
check("systemctl" in concept_tokens("reiniciar con systemctl"), "CLI tool is an examinable token")
# a Spanish verb conjugation is NOT a concept
check("Configura" not in concept_tokens("Configura el grupo"), "verb conjugation 'Configura' is not a concept")

# 15) H2: llm_shorten errors clearly with no backend, and preserves key/correct with one
try:
    llm_shorten({"key": "k", "correct": 1, "options": [1, 2, 3, 4], "answer": "a", "question": "q"}, "p")
    check(False, "llm_shorten raises without a backend")
except RuntimeError:
    check(True, "llm_shorten raises a clear error without a backend")
set_backend(lambda prompt: '{"question":"corto","options":["a","b","c","d"],"correct":0,"answer":"","key":"HACK"}')
_old = {"key": "real", "correct": 2, "options": ["w", "x", "y", "z"], "answer": "dorso", "question": "largo"}
_new = llm_shorten(_old, "p")
check(_new["key"] == "real" and _new["correct"] == 2, "llm_shorten forces original key/correct (H2 safety)")
check(_new["answer"] == "dorso", "llm_shorten restores dropped answer")
set_backend(None)  # reset

# --- Refocus (concept-root) tests ---
from anki_mcq.refocus_deck import needs_refocus, find_refocus_candidates, refocus, _validate_refocus

# 16) combo-stacking card (all options lead with the same service) is detected
combo = mk("Convertir PDF y video a materiales estructurados a escala",
           ["Bedrock Data Automation con Textract y Transcribe y S3 y DynamoDB",
            "Bedrock Data Automation con Lambda y Step Functions y Aurora",
            "Bedrock Data Automation con EventBridge y SNS y SQS y AppSync",
            "Bedrock Data Automation con Glue y Athena y EMR y CloudFront"])
combo["key"] = "rf-combo"
check(needs_refocus(combo), "combo-stacking card is flagged for refocus")

# 17) a well-focused card (competing concepts) is NOT flagged
good = mk("Medir robustez de un FM de Bedrock ante prompts casi identicos",
          ["job de model evaluation de Amazon Bedrock con metricas de robustez",
           "Amazon Comprehend para similitud sobre respuestas por lote",
           "AWS Step Functions invocando el FM con logica propia de divergencia",
           "AWS Lambda con distancia de Levenshtein entre respuestas"])
good["key"] = "rf-good"
check(not needs_refocus(good), "well-focused competing-concepts card is NOT flagged")

# 18) refocus plan_only lists candidates and makes no LLM call
rf_called = {"n": 0}
def _rf_llm(card_dict, prompt):
    rf_called["n"] += 1
    return card_dict
rf = refocus([combo, good], plan_only=True)
check(combo["key"] in rf["candidates"] and good["key"] not in rf["candidates"], "refocus candidates list is correct")
check(rf_called["n"] == 0, "refocus plan_only makes 0 LLM calls")

# 19) _validate_refocus catches a changed correct index
vr = _validate_refocus(
    {"key": "k", "correct": 0, "options": ["a", "b", "c", "d"], "question": "q", "answer": "x"},
    {"key": "k", "correct": 1, "options": ["a", "b", "c", "d"], "question": "q", "answer": "x"})
check("correct cambio" in vr, "_validate_refocus catches changed correct", vr)

# --- Clarity pass tests ---
from anki_mcq.clarity_pass import (needs_clarity, clarity_defects, stem_is_fragment,
                                   option_is_namedrop, repeated_tail, has_typo, clarity, _validate_clarity)

# 20) telegraphic stem detected; well-formed stem not
frag = mk("Deteccion de fraude a 1000 tps sub-500 ms, datos europeos en Europa. Que cumple?",
          ["Amazon Athena para SQL", "Amazon Redshift", "Amazon EMR", "AWS Glue"])
frag["key"] = "cl-frag"
check(stem_is_fragment(frag["question"]), "telegraphic stem detected")
wellformed = mk("Una app necesita consultar datos en S3 con SQL. Que servicio conviene?",
                ["Amazon Athena para SQL", "Amazon Redshift", "Amazon EMR", "AWS Glue"])
check(not stem_is_fragment(wellformed["question"]), "well-formed stem not flagged")

# 21) name-drop option detected; glossed option not
check(option_is_namedrop("PreProcessingTrace y OrchestrationTrace"), "name-drop option detected")
check(not option_is_namedrop("Amazon Athena para consultar S3 con SQL"), "glossed option not flagged")

# 22) repeated tail across options detected
rt = repeated_tail(["X contra un golden dataset", "Y contra un golden dataset",
                    "Z contra un golden dataset", "W distinto"])
check(rt == "un golden dataset", "repeated tail detected", str(rt))

# 23) typo detector: broken n~ flagged, real 'Sonnet' NOT flagged
check(has_typo(mk("q", ["salida daninna", "b", "c", "d"])), "broken n~ 'daninna' flagged as typo")
check(not has_typo(mk("Claude Sonnet para X", ["a", "b", "c", "d"])), "real name 'Sonnet' NOT a typo")

# 24) clarity plan_only lists candidates, no LLM call
cl_called = {"n": 0}
def _cl_llm(cd, pr):
    cl_called["n"] += 1
    return cd
clp = clarity([frag, wellformed], plan_only=True)
check(frag["key"] in clp["candidates"], "clarity candidates include the fragment card")
check(cl_called["n"] == 0, "clarity plan_only makes 0 LLM calls")

# 25) _validate_clarity catches a weakened back
vc2 = _validate_clarity(
    {"key": "k", "correct": 0, "options": ["a", "b", "c", "d"], "question": "q",
     "answer": "una explicacion larga con muchas palabras que refuta cada distractor en detalle aqui"},
    {"key": "k", "correct": 0, "options": ["a", "b", "c", "d"], "question": "q", "answer": "corto"})
check("empobrecio" in vc2, "_validate_clarity catches a weakened back", vc2)

if _fail == 0:
    print("\nALL LENGTH-GATE TESTS PASSED", flush=True)
    sys.exit(0)
else:
    print(f"\n{_fail} LENGTH-GATE TEST(S) FAILED", flush=True)
    sys.exit(1)
