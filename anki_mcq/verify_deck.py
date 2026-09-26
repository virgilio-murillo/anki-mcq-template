#!/usr/bin/env python3
"""
verify_deck.py - Quality gate for MCQ decks. Run BEFORE importing into Anki.

Codifies the standards in DECK_STANDARDS.md so we never re-ship the bugs we
already hit (answer leaking on the front, verdict letter mismatch, unrefuted
distractors, etc.).

Two ways to use it:

1. On a list of card() dicts (before building):
       from verify_deck import verify_cards
       problems = verify_cards(cards)
       if problems: raise SystemExit(problems)

2. On a generated .apkg (after build_deck):
       from verify_deck import verify_apkg
       problems = verify_apkg("my_deck.apkg")

Both return a list of (card_index, issue) tuples; empty list == all good.
"""
import re
import sqlite3
import tempfile
import os
import shutil
import zipfile

from .engine import render_options, _LETTERS

_VERDICT_RE = re.compile(r'class="verdict">\s*(?:Correct|Correcta):\s*([A-D])\b')
_MARKED_RE = re.compile(r'class="opt correct"><span class="k">([A-D])')
# heuristics for "refutes distractors" in ES/EN
_REFUTE_RE = re.compile(
    r'Por qu&eacute; NO|Por que NO|una por una|Distractor|distractor|falsa|falso|'
    r'es tentadora|no las otras|why NO|incorrect|Cada archivo|Los otros|'
    r'describe lo relacional|no es lo que resuelve|no tiene|no sirve|'
    r'herramienta equivocada|opci&oacute;n .* incorrecta|es exagerado|overkill|'
    r'no aplica|no existe|no resuelve|contra lo pedido|es distractor',
    re.I,
)


def _check_answer_html(answer_html):
    issues = []
    if 'class="verdict"' not in answer_html:
        issues.append("sin verdict")
    if '{{L}}' in answer_html:
        issues.append("placeholder {{L}} sin reemplazar")
    if not _REFUTE_RE.search(answer_html):
        issues.append("no parece refutar distractores")
    if 'class="links"' in answer_html:
        after = answer_html.split('class="links"', 1)[1]
        if '<a href=' not in after:
            issues.append("bloque links sin href")
    return issues


# Tokens that identify a specific answer (service/API/CamelCase/code/acronyms).
_SALIENT_RE = re.compile(
    r'[A-Z][a-z]{2,}[A-Z][A-Za-z]+'      # CamelCase e.g. CreateModelInvocationJob
    r'|[a-z]+:[a-zA-Z]+'                  # code ns e.g. s3:GetObject, validation:rmse
    r'|[A-Z][a-zA-Z]{3,}'                 # Proper nouns e.g. Pipelines, Clarify, Athena
    r'|[A-Z]{2,}'                         # Acronyms e.g. ROC, DMS, ECR, PCA
)
# Generic words that are not give-aways even if capitalized/shared.
_GIVEAWAY_STOP = {
    "Amazon", "AWS", "SageMaker", "Use", "Using", "The", "This", "With",
    "Configure", "Create", "Deploy", "Set", "Usar", "Crear", "Para", "Que",
    "ML", "AI", "API", "Que", "For", "And",
}


def _salient_tokens(text):
    plain = re.sub(r'<[^>]+>', '', text or '')
    return {t for t in _SALIENT_RE.findall(plain) if t not in _GIVEAWAY_STOP}


def _extra_giveaway(cards_options, correct_idx, answer_html):
    """Flag if the Exam-tip (extra) block re-names a token UNIQUE to the correct
    option (i.e. not shared by any distractor). That leaks the answer by pointing
    the reader straight at the correct choice's proper name in the 'tip'.
    """
    m = re.search(r'class="extra">(.*?)</div>', answer_html, re.S)
    if not m:
        return None
    tip = m.group(1)
    correct = cards_options[correct_idx]
    distractor_tokens = set()
    for j, o in enumerate(cards_options):
        if j != correct_idx:
            distractor_tokens |= _salient_tokens(o)
    unique_correct = _salient_tokens(correct) - distractor_tokens
    tip_tokens = _salient_tokens(tip)
    leaked = sorted(unique_correct & tip_tokens)
    if leaked:
        return f"exam tip delata la respuesta (nombra {leaked} exclusivo de la correcta)"
    return None


def verify_cards(cards, shuffle_seed_base=1):
    """Verify a list of card() dicts. Returns list of (index, issue)."""
    problems = []
    seen_keys = set()
    for i, c in enumerate(cards):
        idx = i + 1
        if len(c["options"]) != 4:
            problems.append((idx, f'{len(c["options"])} opciones (se esperan 4)'))
        # Balance check: the correct option must NOT be a length outlier in
        # EITHER direction. Patterns that give away the answer by shape:
        #   - correct is the LONGEST and much longer than the rest ("most detailed")
        #   - correct is the SHORTEST and much shorter than the rest ("terse tell")
        # Fix by matching all 4 options' length/specificity, not by any pattern.
        _opts = c["options"]
        _ci = c["correct"]
        if len(_opts) == 4 and 0 <= _ci < 4:
            _lens = [len(re.sub(r'<[^>]+>', '', o)) for o in _opts]
            _clen = _lens[_ci]
            _others = [_lens[j] for j in range(4) if j != _ci]
            _avg = sum(_others) / len(_others) if _others else 0
            _maxlen = max(_lens)
            # Only judge when options are substantial (avoid one-word answers).
            if _avg and _maxlen >= 60:
                if _clen == _maxlen and _clen > 1.4 * _avg:
                    problems.append((idx, f"opcion correcta es la MAS LARGA y desbalanceada (len {_clen} vs prom {round(_avg)}, >1.4x)"))
                if _clen == min(_lens) and _clen * 1.4 < _avg:
                    problems.append((idx, f"opcion correcta es la MAS CORTA y desbalanceada (len {_clen} vs prom {round(_avg)}, <0.71x)"))
        neutral, marked, letter = render_options(c["options"], c["correct"], seed=shuffle_seed_base + i)
        if 'opt correct' in neutral:
            problems.append((idx, "FRENTE filtra la respuesta"))
        answer = c["answer"].replace("{{L}}", letter)
        mv = _VERDICT_RE.search(answer)
        if mv and mv.group(1) != letter:
            problems.append((idx, f"verdict dice {mv.group(1)} pero la correcta es {letter}"))
        for iss in _check_answer_html(answer):
            problems.append((idx, iss))
        _leak = _extra_giveaway(c["options"], c["correct"], answer)
        if _leak:
            problems.append((idx, _leak))
        # No emphasis markup inside options: bold/code/italic/underline on the
        # front would visually flag one option (the answer). Options must be
        # uniform plain text.
        for _oi, _o in enumerate(c["options"]):
            if re.search(r'</?(b|strong|code|i|em|u|mark)\b', _o, re.I):
                problems.append((idx, f"opcion {_LETTERS[_oi]} tiene markup de enfasis (delata/desnivela); las opciones deben ser texto plano"))
        key = c.get("key") or c["question"]
        if key in seen_keys:
            problems.append((idx, f"key duplicada: {key!r}"))
        seen_keys.add(key)
    return problems


def verify_apkg(apkg_path):
    """Verify a generated .apkg. Returns list of (note_index, issue)."""
    problems = []
    d = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(apkg_path) as z:
            z.extractall(d)
        db = os.path.join(d, "collection.anki2")
        con = sqlite3.connect(db)
        rows = [r[0].split("\x1f") for r in con.execute("select flds from notes").fetchall()]
        con.close()
        for i, f in enumerate(rows):
            idx = i + 1
            if len(f) != 4:
                problems.append((idx, f"{len(f)} campos (se esperan 4)"))
                continue
            q, oq, oa, ans = f
            if 'opt correct' in oq:
                problems.append((idx, "FRENTE filtra la respuesta"))
            mk = _MARKED_RE.search(oa)
            mv = _VERDICT_RE.search(ans)
            if mk and mv and mk.group(1) != mv.group(1):
                problems.append((idx, f"verdict {mv.group(1)} != opcion marcada {mk.group(1)}"))
            if oq.count('class="k"') != 4:
                problems.append((idx, f'{oq.count(chr(34)+"k"+chr(34))} opciones en el frente (se esperan 4)'))
            for iss in _check_answer_html(ans):
                problems.append((idx, iss))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return problems


def _print(problems, label):
    if not problems:
        print(f">> {label}: OK (0 problemas)")
        return 0
    print(f">> {label}: {len(problems)} problema(s):")
    for idx, iss in problems:
        print(f"   - card {idx}: {iss}")
    return 1


def _cli():
    import sys
    if len(sys.argv) != 2:
        print("usage: mcq-verify <deck.apkg>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(_print(verify_apkg(sys.argv[1]), sys.argv[1]))


if __name__ == "__main__":
    _cli()
