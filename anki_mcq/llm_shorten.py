#!/usr/bin/env python3
"""
llm_shorten.py - Reference `llm_shorten` implementation for normalize_deck.

`normalize_deck.normalize(new_cards, ref_cards, llm_shorten=...)` calls this
callable AT MOST ONCE per over-budget card to shorten it without losing meaning.
Contract:

    llm_shorten(card_dict, prompt_str) -> rewritten card_dict

- `card_dict` has keys: question, options (list of 4), correct (int), answer, key.
- `prompt_str` is produced by `normalize_deck.build_llm_prompt(card, budget)` and
  already states the word budget and the hard rules (move justification to the
  back, never delete an examinable concept, never change which option is correct).
- The return MUST be a dict with the SAME keys. `normalize._validate_rewrite`
  then checks key/correct unchanged, exactly 4 options, and no concept dropped;
  if it fails, the ORIGINAL card is kept and flagged for review (no retry).

HOW THE MODEL IS CALLED
-----------------------
This repo has no bundled LLM client, and different environments expose different
models. So the model call is pluggable via `set_backend(fn)` where
`fn(prompt_str) -> str` returns the model's raw text (expected to contain the
rewritten card as JSON). By default no backend is set and `llm_shorten` raises a
clear error telling you to wire one, rather than silently doing nothing.

Wiring a backend (examples):

    from anki_mcq.llm_shorten import set_backend

    # Option A: Amazon Bedrock (boto3)
    import boto3, json
    _rt = boto3.client("bedrock-runtime")
    def bedrock(prompt):
        r = _rt.invoke_model(modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            body=json.dumps({"anthropic_version":"bedrock-2023-05-31",
                "max_tokens":1500,"messages":[{"role":"user","content":prompt}]}))
        return json.loads(r["body"].read())["content"][0]["text"]
    set_backend(bedrock)

    # Option B: any callable you already have (OpenAI, local model, the agent's
    # own model via a tool, etc.) as long as it maps prompt -> text.

Then pass `llm_shorten` to normalize/create and it will use your backend, one
call per over-budget card.
"""
import json
import re

# The pluggable text-completion backend: fn(prompt_str) -> raw model text.
_BACKEND = None


def set_backend(fn):
    """Register the model call. `fn(prompt_str: str) -> str` (raw model output)."""
    global _BACKEND
    _BACKEND = fn


def _extract_json_object(text):
    """Pull the first balanced {...} JSON object out of arbitrary model text."""
    if not text:
        raise ValueError("respuesta del modelo vacia")
    # Prefer a fenced ```json block if present.
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    candidate = fence.group(1) if fence else None
    if candidate is None:
        start = text.find("{")
        if start < 0:
            raise ValueError("no se encontro un objeto JSON en la respuesta del modelo")
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    candidate = text[start:i + 1]
                    break
        if candidate is None:
            raise ValueError("objeto JSON sin cerrar en la respuesta del modelo")
    return json.loads(candidate)


def llm_shorten(card, prompt):
    """Shorten one card via the registered backend. Returns a card dict.

    Preserves `key` and `correct` from the ORIGINAL card even if the model omits
    or alters them, so the update-in-place identity and the right answer can
    never drift here. `normalize._validate_rewrite` still re-checks everything
    and reverts to the original card if any invariant is violated.
    """
    if _BACKEND is None:
        raise RuntimeError(
            "llm_shorten: no hay backend de modelo registrado. Llama a "
            "anki_mcq.llm_shorten.set_backend(fn) con fn(prompt)->texto antes de "
            "normalizar. Ver el docstring del modulo para ejemplos (Bedrock, etc.)."
        )
    raw = _BACKEND(prompt)               # exactly one model call
    obj = _extract_json_object(raw)
    # Force-preserve identity and the correct index from the original card.
    obj["key"] = card.get("key")
    obj["correct"] = card.get("correct")
    # Keep the original answer if the model dropped it (answer holds the moved
    # justification; losing it would be worse than a slightly long back).
    if not obj.get("answer"):
        obj["answer"] = card.get("answer", "")
    if not isinstance(obj.get("options"), list):
        obj["options"] = card.get("options")
    return obj
