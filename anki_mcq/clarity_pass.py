#!/usr/bin/env python3
"""
clarity_pass.py - Improve card CLARITY without inflating length (mirror of
normalize_deck.py / refocus_deck.py, for a THIRD, distinct defect).

THE PROBLEM this solves
-----------------------
Aggressive length compression can trade away readability: stems become
telegraphic comma-dumps with no conjugated verb ("Deteccion de fraude a 1000
tps sub-500 ms, datos europeos solo en Europa. Que cumple?"), and options become
bare name-drops that only list API/service names without saying what they do
("PreProcessingTrace, OrchestrationTrace y PostProcessingTrace"). For a concept
the learner has NOT seen, that teaches nothing: the discriminator is decoding a
name, not understanding the concept. This is different from length (normalize)
and from convergence cues (refocus).

Minimum-information does NOT mean telegraphic: it means ONE idea per card,
written CLEARLY. The goal is "short AND clear", not "short AND cryptic".

WHAT THE CLARITY PASS DOES (per flagged card, one LLM call)
-----------------------------------------------------------
1. Rewrite a telegraphic stem into a short but well-formed question: the setup
   as ONE sentence with a subject and conjugated verb, then a question that
   starts with an interrogative (Que/Cual/Como). Keep it short (<= ~28 words).
2. Add a MINIMAL gloss (2-4 words) ONLY to options that are pure name-drops,
   saying what the service/API does. Where the name alone is clear, leave it.
3. Factor a repeated tail (>=3 options ending the same) up into the stem
   (cover-the-options), leaving only the discriminator in each option.
4. Fix compression typos (n~ -> ñ) and keep proper UTF-8 accents.
5. Keep the back (answer) at least as explanatory; never weaken it.

Adding clarity is NOT adding length: factoring tails and turning fragments into
sentences can REDUCE words; only the 2-4 word glosses add a little, and only
where a bare name would not teach the concept.

Same safety contract as the other passes: one LLM call per flagged card;
key and correct are force-preserved; no examinable concept is dropped;
`_validate_clarity` reverts + flags any card that breaks an invariant.
"""
import re
import html as _html

from .verify_deck import _plain, _words, concepts_preserved

# --- Detection (deterministic, no LLM): which cards need a clarity pass ---

_INTERROG = re.compile(r'\b(que|cual|cuales|como|cuando|donde|por que|quien|cuanto|cuantos|cuanta)\b', re.I)
_VERB_HINT = re.compile(
    r'\b(es|son|debe|deben|cumple|conviene|permite|permiten|hace|hacen|necesita|'
    r'necesitan|requiere|requieren|usa|usan|ofrece|ofrecen|quiere|quieren|busca|'
    r'buscan|tiene|tienen|falla|fallan|logra|reduce|minimiza|maximiza|garantiza|'
    r'resuelve|elige|selecciona|esta|estan|hay|puede|pueden|sirve|sirven|exige|'
    r'exigen|deberia|procesa|entrena|despliega|corre|genera)\b', re.I)
_FUNC_VERB = re.compile(
    r'\b(para|que|con|mediante|usando|calcul\w+|valid\w+|entren\w+|sirv\w+|filtr\w+|'
    r'detect\w+|gener\w+|reduc\w+|almacen\w+|convert\w+|clasific\w+|enrut\w+|compar\w+|'
    r'evalu\w+|analiz\w+|proces\w+|ejecut\w+|invoc\w+|desplieg\w+|orquest\w+|monitor\w+|'
    r'registr\w+|configur\w+|habilit\w+)\b', re.I)
_CAMEL = re.compile(r'\b[A-Z][a-zA-Z]+[A-Z][a-zA-Z]+\b')
# n~ corruption: 'daninna' for 'dañina'. ES almost never has a real 'nn'.
_TYPO_NN = re.compile(r'\b\w*nn\w*\b')


def stem_is_fragment(question):
    """True if the stem reads as a telegraphic fragment (setup has no conjugated verb)."""
    plain = _plain(question)
    parts = re.split(r'(?<=[.?!])\s+', plain)
    setup = ' '.join(parts[:-1]) if len(parts) > 1 else plain
    return bool(setup) and not _VERB_HINT.search(setup)


def option_is_namedrop(opt):
    """True if the option only names services/APIs with no functional verb."""
    plain = _plain(opt)
    wc = len(plain.split())
    has_func = bool(_FUNC_VERB.search(plain))
    return (not has_func) and (wc <= 12 or bool(_CAMEL.search(plain)))


def repeated_tail(options, min_words=3, min_group=3):
    """Return the tail string shared by >= min_group options (or None)."""
    tails = {}
    for o in options:
        toks = _plain(o).lower().split()
        if len(toks) >= min_words:
            t = ' '.join(toks[-min_words:])
            tails[t] = tails.get(t, 0) + 1
    for t, c in tails.items():
        if c >= min_group:
            return t
    return None


def has_typo(card):
    text = " ".join([card.get("question", "")] + list(card.get("options", [])))
    plain = _plain(text)
    # Real AWS/product names that legitimately contain 'nn' (not broken 'ñ').
    _ok = {"sonnet", "onnx", "connectors", "connector", "runner", "innecesaria",
           "innecesario", "connect", "annotation", "annotations", "perenne"}
    for w in re.findall(r'\b\w+\b', plain):
        wl = w.lower()
        if len(w) > 3 and _TYPO_NN.search(wl) and wl not in _ok:
            return True
    return False


def clarity_defects(card):
    """Return the list of clarity defects for a card (empty = clear enough)."""
    d = []
    if stem_is_fragment(card.get("question", "")):
        d.append("stem_fragment")
    nd = sum(1 for o in card.get("options", []) if option_is_namedrop(o))
    if nd >= 2:
        d.append(f"namedrop_options({nd})")
    if repeated_tail(card.get("options", [])):
        d.append("repeated_tail")
    if has_typo(card):
        d.append("typo")
    return d


def needs_clarity(card):
    return bool(clarity_defects(card))


def find_clarity_candidates(cards):
    return [c.get("key") for c in cards if needs_clarity(c)]


# --- LLM rewrite (one call per flagged card) ---

def build_clarity_prompt(card):
    defects = clarity_defects(card)
    tail = repeated_tail(card.get("options", []))
    lines = [
        "Mejora la CLARIDAD de esta tarjeta MCQ de AWS SIN alargarla. Debe quedar "
        "CORTA pero AUTOEXPLICATIVA en la primera lectura.",
        "",
        f"Defectos detectados: {', '.join(defects)}.",
        "",
        "HAZ ESTO segun aplique:",
        "- Si el enunciado es telegrafico (lista de constraints sin verbo): reescribelo "
        "como UNA oracion con sujeto y verbo + una pregunta que empiece por Que/Cual/Como. "
        "Manten <= 28 palabras. NO lo alargues de mas.",
        "- Si una opcion solo NOMBRA un servicio/API sin decir que hace: anade una glosa "
        "MINIMA de 2 a 4 palabras que diga su funcion (ej: 'PreProcessingTrace' -> "
        "'PreProcessingTrace (traza de pre-proceso del agente)'). Donde el nombre ya es "
        "claro, NO lo toques.",
    ]
    if tail:
        lines.append(
            f"- Varias opciones terminan igual ('...{tail}'): mueve esa parte comun al "
            "ENUNCIADO y deja en cada opcion solo lo que la distingue (cover-the-options)."
        )
    lines += [
        "- Corrige cualquier typo (por ejemplo 'daninna' debe ser 'dañina') y usa acentos "
        "correctos en espanol (UTF-8).",
        "",
        "REGLAS ABSOLUTAS:",
        f"- NO cambies cual opcion es la correcta (indice {card.get('correct')}).",
        "- NO elimines ningun concepto examinable; si algo sale del frente, va al dorso "
        "(answer). El dorso NO se empobrece, solo puede mejorar.",
        "- Mantén exactamente 4 opciones, texto plano en opciones, espanol, sin em dash.",
        "- Objetivo de longitud: parecido o MAS CORTO que ahora; las glosas de 2-4 palabras "
        "son la unica adicion permitida y solo donde hacen falta.",
        "",
        "TARJETA ACTUAL (JSON):",
        _card_to_json(card),
        "",
        "Devuelve SOLO el JSON de la tarjeta con las mismas claves "
        "(question, options, correct, answer, key).",
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


def _validate_clarity(old, new):
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
    # back must not shrink materially (clarity pass must not weaken the explanation)
    old_back = _words(old.get("answer", ""))
    new_back = _words(new.get("answer", ""))
    if old_back and new_back < 0.8 * old_back:
        return f"el dorso se empobrecio ({old_back} -> {new_back} palabras)"
    return ""


def clarity(cards, llm=None, plan_only=False):
    """Run the clarity pass. Returns {candidates, rewritten, review}.

    `llm(card_dict, prompt_str) -> rewritten card_dict`, called at most once per
    flagged card (reuse anki_mcq.llm_shorten.llm_shorten with a backend set).
    A rewrite that breaks an invariant is reverted and flagged in `review`.
    """
    candidates = find_clarity_candidates(cards)
    if plan_only or llm is None:
        return {"candidates": candidates, "rewritten": cards, "review": []}
    cand = set(candidates)
    out, review = [], []
    for c in cards:
        if c.get("key") not in cand:
            out.append(c)
            continue
        try:
            new = llm(c, build_clarity_prompt(c))
        except Exception as e:  # noqa: BLE001
            review.append((c.get("key"), f"LLM error: {e}"))
            out.append(c)
            continue
        reason = _validate_clarity(c, new)
        if reason:
            review.append((c.get("key"), reason))
            out.append(c)
        else:
            out.append(new)
    return {"candidates": candidates, "rewritten": out, "review": review}
