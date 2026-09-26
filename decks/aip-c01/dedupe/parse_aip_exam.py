#!/usr/bin/env python3
"""Parser de los examenes de practica AIP-C01 (formato Tutorials Dojo).

FORMATO (distinto al de MLA-C01, que usa 'A.' y 'Answer options'):
  - Ancla:      ^N. Question
  - Categoria:  Category: AIP - ...
  - Enunciado:  parrafos, terminando en la linea-pregunta (usualmente '...?')
  - Opciones:   UNA POR LINEA, SIN letra, entre la pregunta y el marcador
                'Incorrect'/'Correct' (resultado del usuario; se ignora)
  - Explicacion larga
  - Correcta single: 'Hence, the correct answer is: <texto exacto de la opcion>'
  - Correcta multi:  '... correct answers are ...' -> CUARENTENA (motor: 1 correcta)
  - Refutaciones:    'The option that says: <texto> is incorrect because ...'
  - References: URLs

El motor anki_mcq soporta 4 opciones y UNA correcta. Cualquier cosa que no
encaje (multi-select, 'select two/three', correcta no casable, != 3-5 opciones)
va a CUARENTENA con su razon; CERO descartes silenciosos (un registro por ancla).

Uso:
    python parse_aip_exam.py --exam ../../../AIP-C01/exam1.txt --tag exam1
Salidas en dedupe/:
    parsed_<tag>.json       preguntas estandar limpias (single-correct)
    quarantine_<tag>.json   no-estandar con razon (revision manual)
"""
import argparse
import json
import pathlib
import re
import unicodedata

DIR = pathlib.Path(__file__).resolve().parent

Q_ANCHOR = re.compile(r'^\s*(\d+)\.\s+Question\s*$')
CATEGORY = re.compile(r'^\s*Category:\s*(.*)$', re.IGNORECASE)
RESULT_MARK = re.compile(r'^\s*(Incorrect|Correct|Skipped|Unanswered)\s*$', re.IGNORECASE)
HENCE = re.compile(r'Hence,\s*the correct answer is:\s*(.*)', re.IGNORECASE | re.DOTALL)
MULTI_MARK = re.compile(r'correct answers are', re.IGNORECASE)
SELECT_N = re.compile(r'\b(select|choose)\s+(two|three|2|3)\b', re.IGNORECASE)
OPTION_SAYS = re.compile(
    r'The option that says:\s*(.*?)\s+is\s+(?:incorrect|partially correct|correct)\b',
    re.IGNORECASE | re.DOTALL)


def norm(s):
    """Normaliza para casar textos: minusculas, sin acentos, comillas rectas,
    espacios colapsados, sin puntuacion final."""
    s = s or ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = (s.replace("\u2018", "'").replace("\u2019", "'")
           .replace("\u201c", '"').replace("\u201d", '"')
           .replace("\u2013", "-").replace("\u2014", "-")
           .replace("\u2011", "-").replace("\u00a0", " "))
    s = s.lower()
    s = re.sub(r'\s+', ' ', s).strip()
    return s.rstrip('.').strip()


def split_blocks(lines):
    """Devuelve lista de (n, block_lines) por cada ancla 'N. Question'."""
    anchors = [i for i, l in enumerate(lines) if Q_ANCHOR.match(l)]
    blocks = []
    for k, start in enumerate(anchors):
        end = anchors[k + 1] if k + 1 < len(anchors) else len(lines)
        n = int(Q_ANCHOR.match(lines[start]).group(1))
        blocks.append((n, lines[start + 1:end]))
    return blocks


def find_question_line(stem_lines):
    """Indice de la ultima linea que parece 'la pregunta' (termina en '?').
    Si ninguna termina en '?', usa la ultima linea no vacia del pre-opciones."""
    last_q = None
    for i, l in enumerate(stem_lines):
        if l.strip().endswith('?'):
            last_q = i
    return last_q


def parse_block(n, block):
    """Parsea un bloque. Devuelve (record, None) o (None, quarantine_reason_dict)."""
    # localizar marcador de resultado (fin de opciones)
    res_idx = next((i for i, l in enumerate(block) if RESULT_MARK.match(l)), None)

    # texto plano del bloque para buscar 'Hence' / multi / select-two
    full_text = "\n".join(block)

    # categoria
    cat = ""
    body_start = 0
    for i, l in enumerate(block):
        m = CATEGORY.match(l)
        if m:
            cat = m.group(1).strip()
            body_start = i + 1
            break

    if res_idx is None:
        stem = " ".join(x.strip() for x in block[body_start:] if x.strip())[:400]
        return None, {"n": n, "reason": "sin marcador Incorrect/Correct (no se pudo delimitar opciones)", "stem": stem}

    pre = block[body_start:res_idx]                 # enunciado + opciones
    pre_ne = [(i, l.strip()) for i, l in enumerate(pre) if l.strip()]
    if not pre_ne:
        return None, {"n": n, "reason": "bloque vacio antes del marcador", "stem": ""}

    # la linea-pregunta separa enunciado (arriba) de opciones (abajo)
    qline_rel = find_question_line([l for _, l in pre_ne])
    if qline_rel is None:
        # sin '?': asumimos que la 1a linea no vacia es enunciado y el resto opciones
        qline_rel = 0
    stem_parts = [l for _, l in pre_ne[:qline_rel + 1]]
    option_lines = [l for _, l in pre_ne[qline_rel + 1:]]
    stem = " ".join(stem_parts).strip()

    # multi-select?
    if MULTI_MARK.search(full_text) or SELECT_N.search(stem):
        return None, {"n": n, "reason": "multi-select (motor soporta 1 correcta)",
                      "stem": stem[:400], "category": cat, "n_options": len(option_lines)}

    if not option_lines:
        return None, {"n": n, "reason": "cero opciones detectadas", "stem": stem[:400], "category": cat}

    # correcta via 'Hence, the correct answer is: <texto>'
    hm = HENCE.search(full_text)
    if not hm:
        return None, {"n": n, "reason": "sin 'Hence, the correct answer is:' (correcta no identificable)",
                      "stem": stem[:400], "category": cat, "n_options": len(option_lines)}
    correct_raw = hm.group(1).strip()
    # cortar la explicacion que suele seguir a la opcion en la misma frase:
    # tomamos hasta el primer salto de linea / doble espacio grande.
    correct_first = correct_raw.split("\n")[0].strip()

    # casar la correcta con UNA opcion (por prefijo normalizado)
    norm_opts = [norm(o) for o in option_lines]
    ncorrect = norm(correct_first)
    idx = None
    # 1) match exacto
    for i, no in enumerate(norm_opts):
        if no == ncorrect:
            idx = i
            break
    # 2) la opcion es prefijo del texto 'Hence' (Hence suele repetir la opcion + explica)
    if idx is None:
        cand = [i for i, no in enumerate(norm_opts) if no and ncorrect.startswith(no)]
        if len(cand) == 1:
            idx = cand[0]
        elif len(cand) > 1:
            idx = max(cand, key=lambda i: len(norm_opts[i]))  # el mas largo (mas especifico)
    # 3) el texto 'Hence' es prefijo de la opcion
    if idx is None:
        cand = [i for i, no in enumerate(norm_opts) if no and no.startswith(ncorrect) and len(ncorrect) > 20]
        if len(cand) == 1:
            idx = cand[0]

    if idx is None:
        return None, {"n": n, "reason": "correcta no casa con ninguna opcion",
                      "stem": stem[:400], "category": cat,
                      "correct_text": correct_first[:200], "options": option_lines}

    # rationale por distractor: 'The option that says: <texto> is incorrect because <...>'
    rationales = {}
    for m in OPTION_SAYS.finditer(full_text):
        opt_txt = m.group(1).strip()
        after = full_text[m.end():]
        # tomar la explicacion hasta el proximo 'The option that says' / 'References' / doble salto
        stop = len(after)
        for pat in (r'The option that says:', r'\nReferences', r'\nCheck out'):
            mm = re.search(pat, after)
            if mm:
                stop = min(stop, mm.start())
        why = after[:stop].strip()
        # casar opt_txt a un indice
        no = norm(opt_txt)
        for i, o in enumerate(norm_opts):
            if o == no or o.startswith(no) or no.startswith(o):
                rationales[i] = why
                break

    options = []
    for i, o in enumerate(option_lines):
        options.append({"text": o, "rationale": rationales.get(i, "")})

    if not (3 <= len(options) <= 6):
        return None, {"n": n, "reason": f"conteo de opciones fuera de rango ({len(options)})",
                      "stem": stem[:400], "category": cat}

    return {
        "n": n,
        "category": cat,
        "stem": stem,
        "options": options,
        "correct_index": idx,
        "correct_text": option_lines[idx],
    }, None


def parse(src):
    lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
    blocks = split_blocks(lines)
    clean, quarantine = [], []
    for n, block in blocks:
        rec, q = parse_block(n, block)
        if rec:
            clean.append(rec)
        else:
            quarantine.append(q)
    return clean, quarantine, len(blocks)


def main():
    ap = argparse.ArgumentParser(description="Parsea un examen AIP-C01 a JSON.")
    ap.add_argument("--exam", required=True, help="ruta al .txt del examen")
    ap.add_argument("--tag", required=True, help="etiqueta de salida, ej. exam1")
    args = ap.parse_args()
    src = pathlib.Path(args.exam)
    if not src.is_absolute():
        src = (pathlib.Path.cwd() / src).resolve()
    print(f">> parseando: {src}", flush=True)
    clean, quarantine, total = parse(src)
    (DIR / f"parsed_{args.tag}.json").write_text(
        json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIR / f"quarantine_{args.tag}.json").write_text(
        json.dumps(quarantine, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> anclas totales:      {total}", flush=True)
    print(f">> estandar (limpias):  {len(clean)}", flush=True)
    print(f">> cuarentena:          {len(quarantine)}", flush=True)
    print(f">> suma {len(clean)+len(quarantine)} == {total}? "
          f"{'OK' if len(clean)+len(quarantine)==total else 'MISMATCH'}", flush=True)
    from collections import Counter
    reasons = Counter(q["reason"] for q in quarantine)
    for r, c in reasons.most_common():
        print(f"   cuarentena[{c}]: {r}", flush=True)


if __name__ == "__main__":
    main()
