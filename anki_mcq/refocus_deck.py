#!/usr/bin/env python3
"""
refocus_deck.py - Refocus MCQ options onto the ROOT CONCEPT (mirror of
normalize_deck.py, but for a DIFFERENT defect).

THE PROBLEM this solves (distinct from length)
----------------------------------------------
A generated card can be a "convergence cue" failure (Haladyna & Downing): the
same service leads ALL four options, so the axis of decision is "which combo of
auxiliary services", not the actual examinable concept. Example: a question whose
root concept is Amazon Bedrock Data Automation (BDA) came out as four options all
starting with "BDA con <different combo>". The "cover-the-options test": if an
element appears in EVERY option, it belongs in the STEM, not the options.

normalize_deck.py only makes cards SHORTER. It does NOT fix this: four "BDA con X"
options just become four shorter "BDA con X" options. Refocusing is a separate
step that rewrites the options into COMPETING concepts (the correct one from the
source + 3 distractors that are OTHER plausible services/approaches for the same
goal), moving the auxiliary-service detail to the card back.

WHAT IT DOES / DOES NOT DO
--------------------------
- Detects (deterministically, no LLM) which cards have the combo-stacking defect
  via `needs_refocus`. This is a MINORITY of cards (measured ~4% on AIP-C01), so
  refocus is best-effort and touches few cards.
- For each flagged card, one LLM call (same pluggable backend as llm_shorten)
  rewrites ONLY the options into competing concepts. `_validate_refocus` then
  enforces: key and correct unchanged, exactly 4 options, no examinable concept
  dropped (moved to the back instead). A card that still looks wrong after the
  single call is reported for review (no retry).
- NEVER invents facts: distractors must be real AWS services plausible for the
  same objective. The validator cannot check technical truth, so refocused cards
  should get a light human review (the review list makes that easy).
- Run BEFORE normalize_deck (refocusing usually shortens; compress afterward).
"""
import re
from collections import Counter

from .verify_deck import _words, _plain, concepts_preserved

# Curated AWS service names for detecting the "convergence cue" defect. Ported
# from the validated investigation detector (kiro-notes/measure_combo_axis.py),
# which correctly isolates 10 combo-defect cards out of 266 (vs a rough regex
# that over-flags legitimate single-service variation). Sorted longest-first so
# "Bedrock Data Automation" wins over "Bedrock".
_AWS_SERVICES = [
    "Amazon Bedrock Data Automation", "Bedrock Data Automation", "BDA",
    "Amazon Bedrock", "Bedrock", "SageMaker Autopilot", "SageMaker JumpStart",
    "SageMaker Data Wrangler", "SageMaker Feature Store", "SageMaker Model Monitor",
    "SageMaker Clarify", "SageMaker Debugger", "SageMaker Experiments",
    "SageMaker Ground Truth", "SageMaker Pipelines", "SageMaker Canvas",
    "Amazon SageMaker", "SageMaker AI", "SageMaker",
    "Amazon Comprehend", "Comprehend", "Amazon Textract", "Textract",
    "Amazon Transcribe", "Transcribe", "Amazon Translate", "Translate",
    "Amazon Rekognition", "Rekognition", "Amazon Polly", "Polly",
    "Amazon Kendra", "Kendra", "Amazon Q", "Amazon Lex", "Lex",
    "Amazon Personalize", "Personalize", "Amazon Forecast", "Forecast",
    "Amazon Fraud Detector", "AWS Glue", "Glue", "Amazon Athena", "Athena",
    "AWS Lambda", "Lambda", "Amazon S3", "S3", "Amazon DynamoDB", "DynamoDB",
    "Amazon Aurora", "Aurora", "Amazon RDS", "RDS", "Amazon EMR", "EMR",
    "AWS Step Functions", "Step Functions", "Amazon EventBridge", "EventBridge",
    "Amazon API Gateway", "API Gateway", "Amazon SNS", "SNS", "Amazon SQS", "SQS",
    "Amazon CloudFront", "CloudFront", "AWS AppSync", "AppSync",
    "Knowledge Bases", "Amazon OpenSearch", "OpenSearch", "Amazon Q Business",
]
_AWS_SERVICES_SORTED = sorted(set(_AWS_SERVICES), key=len, reverse=True)


def _leader_service(opt):
    """First AWS service named in the option (by position), or None."""
    t = _plain(opt)
    best, best_pos = None, 10 ** 9
    for svc in _AWS_SERVICES_SORTED:
        m = re.search(r"\b" + re.escape(svc) + r"\b", t, re.IGNORECASE)
        if m and m.start() < best_pos:
            best_pos, best = m.start(), svc
    return best


def _normalize_leader(svc):
    """Collapse aliases to one leader (BDA == Bedrock Data Automation, etc.)."""
    if svc is None:
        return None
    s = svc.lower()
    if "data automation" in s or s == "bda":
        return "Bedrock Data Automation"
    if "sagemaker" in s:
        return "SageMaker"
    if "bedrock" in s:
        return "Bedrock"
    return svc.replace("Amazon ", "").replace("AWS ", "").strip()


def _other_services(opt, leader):
    """AWS services named in the option that are DIFFERENT from the leader."""
    t = _plain(opt)
    found = set()
    for svc in _AWS_SERVICES_SORTED:
        if re.search(r"\b" + re.escape(svc) + r"\b", t, re.IGNORECASE):
            nl = _normalize_leader(svc)
            if nl and nl != leader:
                found.add(nl)
    return found


def needs_refocus(card):
    """True if the card shows the combo-stacking defect (validated detector).

    Signal (matches the investigation's measure_combo_axis.py, which isolated 10
    real defects out of 266): ALL options share the same leader service (a
    convergence cue), AND after removing that shared leader the options name
    several DIFFERENT other services (union >= 3 AND (avg auxiliaries/option >= 1
    OR at least 2 options stack >= 2 auxiliaries)). The second half separates the
    real defect ("BDA con <different combos>") from LEGITIMATE single-service
    variation (four SageMaker VPC modes, four Bedrock agent designs), which is
    NOT flagged.
    """
    opts = card.get("options", [])
    if len(opts) < 3:
        return False
    leaders = [_normalize_leader(_leader_service(o)) for o in opts]
    known = [l for l in leaders if l]
    if not known:
        return False
    top, cnt = Counter(known).most_common(1)[0]
    if cnt != len(opts):          # require ALL options to share the leader
        return False
    per_opt_others = [_other_services(o, top) for o in opts]
    union = set().union(*per_opt_others) if per_opt_others else set()
    avg_aux = sum(len(s) for s in per_opt_others) / max(1, len(per_opt_others))
    stacked = sum(1 for s in per_opt_others if len(s) >= 2)
    return len(union) >= 3 and (avg_aux >= 1.0 or stacked >= 2)


def find_refocus_candidates(cards):
    """Return the list of keys that need refocusing (deterministic, no LLM)."""
    return [c.get("key") for c in cards if needs_refocus(c)]


def build_refocus_prompt(card):
    """Single-call LLM prompt to rewrite ONE card's options as competing concepts."""
    correct_idx = card.get("correct")
    opts = card.get("options", [])
    correct_text = opts[correct_idx] if isinstance(correct_idx, int) and 0 <= correct_idx < len(opts) else ""
    lines = [
        "Reescribe SOLO las opciones de esta tarjeta MCQ de AWS para que el EJE DE "
        "DECISION sea el CONCEPTO RAIZ, no un combo de servicios auxiliares.",
        "",
        "PROBLEMA A CORREGIR: ahora varias opciones empiezan con el mismo servicio "
        "(convergence cue). Aplica el 'cover-the-options test': si un elemento aparece "
        "en TODAS las opciones, muevelo al enunciado, no lo repitas en cada opcion.",
        "",
        f"La opcion CORRECTA debe SEGUIR SIENDO el concepto correcto de la fuente "
        f"(indice {correct_idx}): {_plain(correct_text)!r}.",
        "",
        "REESCRIBE las 4 opciones como SERVICIOS/ENFOQUES QUE COMPITEN: cada opcion "
        "debe LIDERAR con un servicio o enfoque DISTINTO. Ejemplo del patron bueno: "
        "'job de model evaluation de Bedrock' vs 'Comprehend para similitud' vs "
        "'Step Functions con logica propia' vs 'Lambda con distancia de Levenshtein'.",
        "",
        "REGLAS ABSOLUTAS:",
        f"- NO cambies cual opcion es la correcta (indice {correct_idx}).",
        "- PROHIBIDO que 3 o 4 opciones empiecen con el mismo servicio.",
        "- Cada opcion NOMBRA el concepto/servicio, no lo explica (breve).",
        "- NO inventes hechos: los distractores deben ser servicios AWS reales y "
        "plausibles para el mismo objetivo del escenario.",
        "- Todo detalle de servicios auxiliares que quites de las opciones DEBE ir "
        "al dorso (campo answer), nunca se pierde.",
        "- Manten exactamente 4 opciones, texto plano, espanol, sin em dash.",
        "",
        "TARJETA ACTUAL (JSON):",
        _card_to_json(card),
        "",
        "Devuelve SOLO el JSON de la tarjeta reescrita con las mismas claves "
        "(question, options, correct, answer, key). El dorso (answer) debe conservar "
        "o enriquecer la explicacion y refutar cada distractor nuevo.",
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


def _validate_refocus(old, new):
    """Return an error reason if the refocus broke an invariant, else ''. """
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
    # Did it actually fix the convergence cue?
    if needs_refocus(new):
        return "sigue con convergence cue (>=3 opciones mismo servicio-lider)"
    return ""


def refocus(cards, llm=None, plan_only=False):
    """Refocus the options of cards that show the combo-stacking defect.

    Args:
      cards: list of card() dicts.
      llm: callable(card_dict, prompt_str) -> rewritten card_dict, called AT MOST
        ONCE per flagged card. Reuse anki_mcq.llm_shorten.llm_shorten (set a
        backend via llm_shorten.set_backend first). If None or plan_only=True, no
        rewriting happens; only the candidate list is returned.
      plan_only: if True, return the candidates without rewriting.

    Returns dict: {
      "candidates": [keys that need refocus],
      "rewritten":  [cards] (same list if plan_only / no llm),
      "review":     [(key, reason)] flagged cards that failed validation,
    }
    Guarantees per rewrite (else the card is kept as-is and flagged):
      key/correct unchanged, exactly 4 options, no examinable concept dropped,
      and the convergence cue actually resolved.
    """
    candidates = find_refocus_candidates(cards)
    if plan_only or llm is None:
        return {"candidates": candidates, "rewritten": cards, "review": []}

    cand_set = set(candidates)
    out, review = [], []
    for c in cards:
        if c.get("key") not in cand_set:
            out.append(c)
            continue
        prompt = build_refocus_prompt(c)
        try:
            new = llm(c, prompt)          # exactly one call
        except Exception as e:            # noqa: BLE001
            review.append((c.get("key"), f"LLM error: {e}"))
            out.append(c)
            continue
        reason = _validate_refocus(c, new)
        if reason:
            review.append((c.get("key"), reason))
            out.append(c)                 # keep original, flag for human
        else:
            out.append(new)
    return {"candidates": candidates, "rewritten": out, "review": review}
