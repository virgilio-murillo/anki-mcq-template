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
import html as _html

from .engine import render_options, _LETTERS

# ---------------------------------------------------------------------------
# Length / atomicity thresholds (see DECK_STANDARDS.md section 10).
#
# Calibrated against the MLA-C01 gold-standard deck (224 cards). Verified to
# produce ZERO false positives on MLA while flagging the verbose AIP-C01 cards:
#   MLA stem max = 67w (mla02-q38); MLA option max = 29w (mla02-q23); MLA
#   option char max = 182. ERRORs sit ~3w above those maxima so a healthy card
#   never fails, but the ~2x-longer AIP cards do.
#
# WHY ONLY LENGTH IS A HARD ERROR: a card may legitimately couple dependent
# concepts (e.g. InitialVariantWeight needs "an endpoint hosts several
# ProductionVariants"). Counting concepts, bold clauses or services would
# punish that. So bold-clause and service-stacking counts are WARNINGS only.
# The real, measurable defect is verbose option "tails" (justification glued
# onto the option that belongs on the back) and bloated stems.
# ---------------------------------------------------------------------------
STEM_WARN_WORDS = 45    # MLA stem p90 = 43
STEM_ERROR_WORDS = 70   # MLA stem max = 67; NEVER lower to <= 67
OPT_WARN_WORDS = 25     # MLA option p90 = 20
OPT_ERROR_WORDS = 32    # MLA option max = 29
OPT_WARN_CHARS = 200    # MLA option char max = 182 (density signal, WARNING only)
BOLD_WARN_CLAUSES = 5   # MLA stem <b> max = 5; >5 is a coupling/stacking signal (WARNING only)

# ---------------------------------------------------------------------------
# Deck-level DISTRIBUTION targets (see DECK_STANDARDS.md section 10).
#
# The per-card hard errors above (stem>70, opt>32) are a safety net that only
# catches extreme outliers. They are NOT enough: a deck where EVERY card sits
# just under the ceiling (opt 26-32w) passes card-by-card yet is ~2x as dense
# as the gold MLA deck and tiring to read. So we ALSO check the whole deck's
# distribution against MLA-like shape. This lets an occasional long card exist
# (some concepts need it) while catching a deck that is long ACROSS THE BOARD.
#
# Targets derived from MLA-C01 gold (measured): option p50=12 p90=20 p95=21,
# 1% of options >25w; stem p50=30 p90=43, 6% of stems >45w. The deck ceilings
# below sit a little above MLA's real p90/percentages so the gold deck itself
# passes with margin, but a mostly-long deck (like AIP after pass 1: option
# p90=31, 56% >25w) fails.
# ---------------------------------------------------------------------------
DIST_OPT_P90_MAX = 22       # MLA option p90 = 20
DIST_OPT_OVER25_PCT_MAX = 15.0   # MLA has 1% of options >25w; allow up to 15%
DIST_STEM_P90_MAX = 50      # MLA stem p90 = 43
DIST_STEM_OVER45_PCT_MAX = 35.0  # MLA has 6% of stems >45w; allow up to 35%

_TAGS = re.compile(r'<[^>]+>')


def _plain(s):
    """Strip HTML tags and unescape entities, collapse whitespace."""
    s = _TAGS.sub(' ', s or '')
    return re.sub(r'\s+', ' ', _html.unescape(s)).strip()


def _words(s):
    return len([w for w in _plain(s).split() if w])


def _chars(s):
    return len(_plain(s))


def _length_problems(card):
    """Return (errors, warnings) lists of strings for one card() dict.

    Errors are hard failures (fail the gate). Warnings are advisory (do not
    fail the gate) and cover legitimate-coupling signals plus soft length caps.
    """
    errors, warnings = [], []
    q = card.get("question", "")
    sw = _words(q)
    if sw > STEM_ERROR_WORDS:
        errors.append(
            f"enunciado {sw} palabras (>{STEM_ERROR_WORDS}); destila a un nucleo "
            f"examinable, corta requisitos no relacionados"
        )
    elif sw > STEM_WARN_WORDS:
        warnings.append(f"enunciado {sw} palabras (>{STEM_WARN_WORDS} = objetivo); considera acortar")

    nb = len(re.findall(r'<b\b', q, re.I))
    if nb > BOLD_WARN_CLAUSES:
        warnings.append(
            f"{nb} clausulas <b> en el enunciado; revisa si es dependencia legitima "
            f"(conservar) o apilamiento artificial (cortar). Test de borrado: si quitar "
            f"la clausula no cambia la respuesta correcta, es relleno"
        )

    for oi, o in enumerate(card.get("options", [])):
        ow = _words(o)
        oc = _chars(o)
        L = _LETTERS[oi] if oi < len(_LETTERS) else str(oi)
        if ow > OPT_ERROR_WORDS:
            errors.append(
                f"opcion {L} tiene {ow} palabras (>{OPT_ERROR_WORDS}); la opcion NOMBRA "
                f"el concepto, la justificacion va en el dorso"
            )
        elif ow > OPT_WARN_WORDS:
            warnings.append(f"opcion {L}: {ow} palabras (>{OPT_WARN_WORDS} = objetivo)")
        if ow <= OPT_ERROR_WORDS and oc > OPT_WARN_CHARS:
            warnings.append(f"opcion {L}: {oc} caracteres (>{OPT_WARN_CHARS}); densa, revisa")
    return errors, warnings

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
        # Length / atomicity HARD errors (see DECK_STANDARDS.md section 10).
        length_errors, _ = _length_problems(c)
        for e in length_errors:
            problems.append((idx, e))
    return problems


def warn_cards(cards):
    """Return advisory (non-fatal) length/atomicity warnings.

    Separate from verify_cards so warnings never fail the gate. Returns a list
    of (index, warning) tuples.
    """
    out = []
    for i, c in enumerate(cards):
        _, warnings = _length_problems(c)
        for w in warnings:
            out.append((i + 1, w))
    return out


def _pctile(values, p):
    if not values:
        return 0
    s = sorted(values)
    i = min(len(s) - 1, int(round((p / 100.0) * (len(s) - 1))))
    return s[i]


def check_distribution(cards):
    """Deck-level shape check against MLA-gold-like targets.

    Per-card hard errors (stem>70, opt>32) only catch extreme outliers; a deck
    can pass those yet be uniformly long (every option 26-32w). This checks the
    WHOLE deck's percentiles so an occasional long card is fine but a deck that
    is long across the board fails. Returns a list of problem strings (empty =
    distribution resembles the gold deck).
    """
    if not cards:
        return []
    opt_words = [_words(o) for c in cards for o in c.get("options", [])]
    stem_words = [_words(c.get("question", "")) for c in cards]
    n_opt = len(opt_words) or 1
    n_stem = len(stem_words) or 1
    opt_p90 = _pctile(opt_words, 90)
    stem_p90 = _pctile(stem_words, 90)
    over25 = 100.0 * sum(1 for w in opt_words if w > 25) / n_opt
    over45 = 100.0 * sum(1 for w in stem_words if w > 45) / n_stem
    problems = []
    if opt_p90 > DIST_OPT_P90_MAX:
        problems.append(
            f"distribucion: opcion p90={opt_p90}w (>{DIST_OPT_P90_MAX}); la baraja es densa "
            f"en general, acerca la forma a MLA (p90 objetivo ~20w)"
        )
    if over25 > DIST_OPT_OVER25_PCT_MAX:
        problems.append(
            f"distribucion: {over25:.0f}% de opciones >25w (max {DIST_OPT_OVER25_PCT_MAX:.0f}%); "
            f"MLA tiene ~1%. La mayoria de opciones deben ser cortas"
        )
    if stem_p90 > DIST_STEM_P90_MAX:
        problems.append(
            f"distribucion: enunciado p90={stem_p90}w (>{DIST_STEM_P90_MAX}); acerca la forma a MLA"
        )
    if over45 > DIST_STEM_OVER45_PCT_MAX:
        problems.append(
            f"distribucion: {over45:.0f}% de enunciados >45w (max {DIST_STEM_OVER45_PCT_MAX:.0f}%); "
            f"MLA tiene ~6%"
        )
    return problems


# Tokens that identify examinable content (services, APIs, CamelCase, acronyms,
# code namespaces). Used to verify a rewrite did not DROP a concept the learner
# must study. Reuses the salient-token idea from _extra_giveaway.
_CONCEPT_RE = re.compile(
    r'[A-Z][a-z]+[A-Z][A-Za-z]+'       # CamelCase e.g. ProductionVariant
    r'|[a-z]+:[a-zA-Z]+'               # code ns e.g. bedrock:GuardrailIdentifier
    r'|[A-Z][a-zA-Z]{3,}'              # Proper nouns e.g. Bedrock, Trainium
    r'|[A-Z]{2,}'                      # Acronyms e.g. RAG, LLM, CRIS
)
_CONCEPT_STOP = {
    "Amazon", "AWS", "The", "This", "That", "With", "For", "And", "Una", "Un",
    "Que", "Los", "Las", "Por", "Para", "Con", "Del", "SQL", "API",
    # Spanish verbs / generic prose words (capitalized at sentence/option start)
    # are NOT examinable concepts. Without this, concepts_preserved fires on
    # "Usar", "Debe", etc. and produces false positives on every rewrite.
    "Usar", "Crear", "Desplegar", "Configurar", "Construir", "Implementar",
    "Utilizar", "Aprovechar", "Emplear", "Aplicar", "Habilitar", "Activar",
    "Adquirir", "Lanzar", "Integrar", "Generar", "Ejecutar", "Convertir",
    "Definir", "Permitir", "Gestionar", "Gestiona", "Confirman", "Sospechan",
    "Quiere", "Planea", "Entrenar", "Debe", "Durante", "Cuando", "Anadir",
    "Anade", "Mantener", "Reducir", "Enviar", "Recuperar", "Almacenar",
    "Procesar", "Procesa", "Analizar", "Monitorear", "Registrar", "Validar",
    "Verificar", "Optimizar", "Escalar", "Automatizar", "Orquestar", "Necesita",
    "Tiene", "Hospedara", "Preocupa", "Destilar", "Guardar", "Ingerir",
    "Ademas", "Antes", "Dado", "Detectar", "Ajustar", "Agregar", "Este",
    "Esta", "Cada", "Todos", "Todas", "Many", "Requests", "Load", "Balancer",
    "Service", "Application", "Processing", "Control", "Manager", "Systems",
    # Generic domain words that appear everywhere, not a specific examinable service
    "IA", "ML", "AI", "FM", "LLM", "NLP", "JSON", "GenAI", "REST", "SDK",
    "Modelos", "Funciones", "Lambdas", "Regiones", "MENOR", "MENORES",
    "SALIDAS", "RRHH", "Europa", "Fine",
    # Spanish verb CONJUGATIONS (3rd person / imperative) seen at option/stem
    # start in non-AWS domains (networking, security, Linux). Infinitives above
    # are not enough; a deck may say "Configura...", "Ejecuta...".
    "Configura", "Ejecuta", "Crea", "Habilita", "Aplica", "Usa", "Rota",
    "Valida", "Escala", "Despliega", "Reinicia", "Monitorea", "Registra",
    "Almacena", "Recupera", "Procesa", "Analiza", "Optimiza", "Integra",
    "Genera", "Define", "Permite", "Mantiene", "Reduce", "Envia", "Activa",
    "Verifica", "Automatiza", "Orquesta", "Construye", "Implementa", "Utiliza",
}

# Examinable NON-CamelCase values that _CONCEPT_RE misses: network ports, CIDR
# blocks, protocol versions, common CLI tools. Changing "puerto 443" -> "puerto 53"
# or "/16" -> "/24" IS an examinable change; these regexes make it visible so
# concepts_preserved can catch it in networking/security/Linux decks.
_VALUE_RES = [
    re.compile(r'\bpuerto\s+\d{1,5}\b', re.IGNORECASE),          # puerto 443
    re.compile(r'\bport\s+\d{1,5}\b', re.IGNORECASE),            # port 22
    re.compile(r'\b\d{1,3}(?:\.\d{1,3}){3}/\d{1,2}\b'),          # 10.0.0.0/16
    re.compile(r'/\d{1,2}\b'),                                   # bare /16 mask
    re.compile(r'\b(?:TLS|SSL|HTTP|HTTPS|IPv|TCP|UDP|SSH|BGP)\s*[0-9.]*\b', re.IGNORECASE),
    re.compile(r'\b(?:systemctl|systemd|nginx|kubectl|chmod|chown|iptables|'
               r'crontab|journalctl|firewalld|selinux)\b', re.IGNORECASE),
]


def _value_tokens(plain):
    out = set()
    for rx in _VALUE_RES:
        for m in rx.findall(plain):
            out.add(m.strip().lower() if isinstance(m, str) else m)
    return out


def concept_tokens(text):
    """Salient examinable tokens (service/API/acronym names + network/CLI values)."""
    plain = _plain(text)
    toks = {t for t in _CONCEPT_RE.findall(plain) if t not in _CONCEPT_STOP}
    toks |= _value_tokens(plain)
    return toks


def concepts_preserved(old_card, new_card):
    """Check no examinable concept was DROPPED when a card was rewritten.

    Every salient token present ANYWHERE in the old card (question + options +
    answer) must still appear SOMEWHERE in the new card (question + options +
    answer). Moving a concept from an option to the back is fine; deleting it
    entirely is not. Returns the set of dropped tokens (empty = safe).
    """
    def all_text(c):
        return " ".join([c.get("question", "")] + list(c.get("options", [])) + [c.get("answer", "")])
    old_tokens = concept_tokens(all_text(old_card))
    new_tokens = concept_tokens(all_text(new_card))
    return old_tokens - new_tokens


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
            # Length / atomicity HARD errors on the built package (secondary net;
            # the authoritative check runs on card() dicts before build).
            sw = _words(q)
            if sw > STEM_ERROR_WORDS:
                problems.append((idx, f"enunciado {sw} palabras (>{STEM_ERROR_WORDS})"))
            # Split the front options field into the 4 option bodies. Each option
            # is: <span class="opt"><span class="k">X.</span>BODY</span>
            parts = re.split(r'<span class="opt"><span class="k">[A-H]\.</span>', oq)
            for body in parts[1:]:
                body = body.rsplit('</span>', 1)[0]  # drop the closing opt span
                ow = _words(body)
                if ow > OPT_ERROR_WORDS:
                    problems.append((idx, f"una opcion tiene {ow} palabras (>{OPT_ERROR_WORDS})"))
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
