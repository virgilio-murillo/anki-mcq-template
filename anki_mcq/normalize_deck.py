#!/usr/bin/env python3
"""
normalize_deck.py - Automated deck NORMALIZATION step (run AFTER generating a deck).

THE PROBLEM this solves
-----------------------
A freshly generated deck (especially from an exam dump) tends to be uniformly
verbose: long stems, long options carrying justification that belongs on the
back. A flat word cap either over-compresses cards that genuinely need more
text, or is too loose and leaves everything long. Neither matches the shape of
a good, hand-tuned deck.

THE IDEA (quantile normalization against a reference deck)
----------------------------------------------------------
Take a KNOWN-GOOD reference deck (e.g. MLA-C01) and map the new deck's length
distribution onto it. For each card we compute WHERE it sits in the new deck's
distribution (its percentile) and assign it the length that the SAME percentile
has in the reference. So:

  - the median card gets the reference's median budget,
  - a genuinely long card (95th percentile) gets the reference's 95th-percentile
    budget - still one of the longest, but on a healthy scale,
  - a short card is left alone.

This preserves the RELATIVE ordering (cards that need more text stay longest)
while pulling the whole shape onto the reference. Example the user gave: new
deck averages 1000w, reference averages 500w, a 1500w card lands near ~750w.
We do it per-percentile (not a single ratio) so the tail is not crushed.

THE REWRITE (one LLM call per card, max)
----------------------------------------
Computing the target budget is deterministic (no LLM). ACTUALLY shortening the
text without losing meaning needs an LLM. So for each card that exceeds its
budget we make AT MOST ONE LLM call, handing it: the card, its per-field word
budget, and the hard rule "move justification to the back, never delete an
examinable concept". Cards already within budget are left untouched (0 calls).

After rewriting we VERIFY (deterministic): concepts preserved (no AWS
service/API/parameter dropped), correct answer unchanged, gate passes,
distribution now resembles the reference. A card that fails verification is
REPORTED for human review - we do NOT loop (respects the one-call budget).

This module provides the deterministic budgeting + the orchestration contract.
The actual LLM call is injected as a callable so the caller controls the model;
if none is provided, `plan_only=True` returns the budget plan without rewriting.
"""
import re
import html as _html

from .verify_deck import (
    _words, _plain, concept_tokens, concepts_preserved, verify_cards,
    check_distribution,
)


def _percentile_of(sorted_vals, x):
    """Fraction of values <= x (the empirical percentile rank of x), 0..1."""
    if not sorted_vals:
        return 0.0
    lo = 0
    for v in sorted_vals:
        if v <= x:
            lo += 1
    return lo / len(sorted_vals)


def _value_at_percentile(sorted_vals, frac):
    if not sorted_vals:
        return 0
    i = min(len(sorted_vals) - 1, max(0, int(round(frac * (len(sorted_vals) - 1)))))
    return sorted_vals[i]


def reference_distribution(ref_cards):
    """Sorted option-word and stem-word lists from the reference (gold) deck."""
    opt = sorted(_words(o) for c in ref_cards for o in c.get("options", []))
    stem = sorted(_words(c.get("question", "")) for c in ref_cards)
    return {"opt": opt, "stem": stem}


def budget_for_deck(new_cards, ref_cards, floor_opt=6, floor_stem=12):
    """Compute a per-card word budget by quantile-mapping the NEW deck's length
    distribution onto the REFERENCE deck's distribution.

    Returns a list (parallel to new_cards) of dicts:
      {"key", "stem_now", "stem_budget", "opt_now":[...], "opt_budget":[...],
       "needs_rewrite": bool}

    A field needs shortening only if it currently exceeds its mapped budget by
    a margin (we do not touch fields already at/under budget). Budgets never go
    below small floors so we never demand nonsense.
    """
    ref = reference_distribution(ref_cards)
    new_opt_sorted = sorted(_words(o) for c in new_cards for o in c.get("options", []))
    new_stem_sorted = sorted(_words(c.get("question", "")) for c in new_cards)

    plans = []
    for c in new_cards:
        sw = _words(c.get("question", ""))
        # percentile of this stem within the NEW deck -> reference value at that percentile
        p = _percentile_of(new_stem_sorted, sw)
        stem_budget = max(floor_stem, _value_at_percentile(ref["stem"], p))
        opt_now, opt_budget = [], []
        for o in c.get("options", []):
            ow = _words(o)
            po = _percentile_of(new_opt_sorted, ow)
            ob = max(floor_opt, _value_at_percentile(ref["opt"], po))
            opt_now.append(ow)
            opt_budget.append(ob)
        needs = sw > stem_budget + 3 or any(n > b + 3 for n, b in zip(opt_now, opt_budget))
        plans.append({
            "key": c.get("key"),
            "stem_now": sw, "stem_budget": stem_budget,
            "opt_now": opt_now, "opt_budget": opt_budget,
            "needs_rewrite": needs,
        })
    return plans


def build_llm_prompt(card, plan):
    """Build the single-call LLM prompt for shortening ONE card to its budget.

    The caller passes this to its own model. The prompt is explicit about the
    two hard invariants (preserve every examinable concept by moving it to the
    back; never change which option is correct).
    """
    opts = card.get("options", [])
    lines = [
        "Reescribe esta tarjeta MCQ de AWS para que sea mas CONCISA, sin perder "
        "significado, calidad ni ningun concepto examinable.",
        "",
        "REGLAS ABSOLUTAS:",
        "- NO elimines informacion: si quitas un servicio/API/parametro de una "
        "opcion o del enunciado, DEBE seguir presente en el dorso (campo answer).",
        "- NO cambies cual opcion es la correcta. El indice correcto es "
        f"{card.get('correct')} y debe seguir siendo la respuesta.",
        "- Mantén exactamente 4 opciones, en texto plano, en espanol, sin em dash.",
        "- Las 4 opciones deben seguir siendo distinguibles entre si.",
        "",
        "PRESUPUESTO DE PALABRAS (objetivo, no lo excedas salvo que el concepto lo exija):",
        f"- enunciado: ~{plan['stem_budget']} palabras (ahora {plan['stem_now']})",
    ]
    for i, (n, b) in enumerate(zip(plan["opt_now"], plan["opt_budget"])):
        lines.append(f"- opcion {i}: ~{b} palabras (ahora {n})")
    lines += [
        "",
        "TARJETA ACTUAL (JSON):",
        _card_to_json(card),
        "",
        "Devuelve SOLO el JSON de la tarjeta reescrita con las mismas claves "
        "(question, options, correct, answer, key). El campo answer debe "
        "conservar o enriquecer la explicacion y la refutacion de cada distractor.",
    ]
    return "\n".join(lines)


def _card_to_json(card):
    import json
    return json.dumps({
        "question": card.get("question", ""),
        "options": card.get("options", []),
        "correct": card.get("correct"),
        "answer": card.get("answer", ""),
        "key": card.get("key"),
    }, ensure_ascii=False, indent=2)


def normalize(new_cards, ref_cards, llm_shorten=None, plan_only=False):
    """Normalize a deck's length distribution toward the reference deck.

    Args:
      new_cards: list of card() dicts to normalize (the freshly generated deck).
      ref_cards: list of card() dicts from the known-good reference deck (gold).
      llm_shorten: optional callable(card_dict, prompt_str) -> rewritten card_dict.
        Called AT MOST ONCE per over-budget card. If None or plan_only=True, no
        rewriting happens and only the budget plan is returned.
      plan_only: if True, return the plan without rewriting.

    Returns dict: {
      "plan": [...per-card budget...],
      "rewritten": [...cards...] (same list if plan_only),
      "review": [(key, reason), ...] cards that failed post-rewrite verification,
    }

    Guarantees enforced after each rewrite (else the card is reverted + flagged):
      - key and correct unchanged,
      - no examinable concept dropped (concepts_preserved),
      - exactly 4 options.
    """
    plan = budget_for_deck(new_cards, ref_cards)
    if plan_only or llm_shorten is None:
        return {"plan": plan, "rewritten": new_cards, "review": []}

    # H5: if the deck already matches the reference SHAPE, do not rewrite anything.
    # budget_for_deck is per-card and stricter than the deck-level distribution
    # gate, so a deck that already passes check_distribution would otherwise
    # trigger dozens of needless LLM calls. Skip when the shape is already good.
    if not check_distribution(new_cards):
        return {"plan": plan, "rewritten": new_cards, "review": []}

    out = []
    review = []
    for card, p in zip(new_cards, plan):
        if not p["needs_rewrite"]:
            out.append(card)
            continue
        prompt = build_llm_prompt(card, p)
        try:
            new = llm_shorten(card, prompt)  # exactly one call
        except Exception as e:  # noqa: BLE001
            review.append((card.get("key"), f"LLM error: {e}"))
            out.append(card)
            continue
        reason = _validate_rewrite(card, new)
        if reason:
            review.append((card.get("key"), reason))
            out.append(card)  # keep original, flag for human
        else:
            out.append(new)
    # Final distribution check on the resulting deck.
    dist = check_distribution(out)
    if dist:
        review.append((None, "distribucion aun no coincide con la referencia: " + "; ".join(dist)))
    return {"plan": plan, "rewritten": out, "review": review}


def _validate_rewrite(old, new):
    """Return an error reason if the rewrite broke an invariant, else ''. """
    if not isinstance(new, dict):
        return "la reescritura no devolvio un dict de tarjeta"
    if new.get("key") != old.get("key"):
        return f"key cambio ({old.get('key')} -> {new.get('key')})"
    if new.get("correct") != old.get("correct"):
        return f"correct cambio ({old.get('correct')} -> {new.get('correct')})"
    if len(new.get("options", [])) != 4:
        return f"{len(new.get('options', []))} opciones (se esperan 4)"
    dropped = concepts_preserved(old, new)
    if dropped:
        return f"conceptos examinables perdidos: {sorted(dropped)}"
    return ""
