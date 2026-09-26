#!/usr/bin/env python3
"""Parser de los examenes de practica OFICIALES de AWS (AIP-C01).

FORMATO oficial (distinto a Tutorials Dojo):
  Question N
  Multiple Choice | Multiple Response | Matching | Ordering
  Time to answer: / Answer status: <tu resultado, ignorar>
  Question
  <enunciado, varios parrafos, termina en la pregunta>
  Answer options
  Option / Correct answer / Your selection / Rationale   (cabecera, ignorar)
  A. <texto opcion>
  Correct | Not selected            <- 'Correct' marca la opcion correcta
  Not selected
  <rationale de la opcion, puede incluir 'Learn more about ...'>
  B. <texto> ...

El motor anki_mcq soporta 4 opciones y UNA correcta. Multiple Response (>=2 Correct),
Matching y Ordering van a CUARENTENA. Cero descartes silenciosos.

Uso: python parse_official_exam.py --exam ../../../AIP-C01/official-practice-set.txt --tag off1
Salidas: parsed_<tag>.json, quarantine_<tag>.json  (mismo esquema que parse_aip_exam.py)
"""
import argparse
import json
import pathlib
import re

DIR = pathlib.Path(__file__).resolve().parent
Q_ANCHOR = re.compile(r'^Question\s+(\d+)\s*$')
OPT_RE = re.compile(r'^([A-H])\.\s+(.*)$')
TYPE_RE = re.compile(r'^(Multiple Choice|Multiple Response|Multiple response|Matching results|Matching|Ordering)\s*$', re.I)
HEADER = {"Option", "Correct answer", "Your selection", "Rationale", "Answer options"}
STATUS = {"Correct", "Not selected", "Incorrect", "Selected", "Skipped", "Unanswered", "Partially correct"}


def parse(src):
    lines = src.read_text(encoding="utf-8", errors="replace").splitlines()
    anchors = [i for i, l in enumerate(lines) if Q_ANCHOR.match(l.strip())]
    clean, quarantine = [], []

    for qi, start in enumerate(anchors):
        end = anchors[qi + 1] if qi + 1 < len(anchors) else len(lines)
        block = lines[start + 1:end]
        n = int(Q_ANCHOR.match(lines[start].strip()).group(1))

        # tipo de pregunta
        qtype = None
        for l in block[:4]:
            m = TYPE_RE.match(l.strip())
            if m:
                qtype = m.group(1).lower()
                break
        if qtype and ("matching" in qtype or "ordering" in qtype or "response" in qtype):
            stem = " ".join(x.strip() for x in block if x.strip())[:300]
            quarantine.append({"n": n, "reason": f"tipo no soportado ({qtype})", "stem": stem})
            continue

        # localizar 'Question' (inicio del enunciado) y 'Answer options'
        q_idx = next((k for k, l in enumerate(block) if l.strip() == "Question"), None)
        ao_idx = next((k for k, l in enumerate(block) if l.strip() == "Answer options"), None)
        if q_idx is None or ao_idx is None or ao_idx <= q_idx:
            stem = " ".join(x.strip() for x in block if x.strip())[:300]
            quarantine.append({"n": n, "reason": "sin 'Question'/'Answer options'", "stem": stem})
            continue

        stem = " ".join(x.strip() for x in block[q_idx + 1:ao_idx] if x.strip())
        opt_block = block[ao_idx + 1:]

        options, cur = [], None
        for l in opt_block:
            s = l.strip()
            m = OPT_RE.match(s)
            if m:
                if cur:
                    options.append(cur)
                cur = {"letter": m.group(1), "text": m.group(2).strip(), "correct": False, "rationale": ""}
            elif cur is not None:
                if s == "Correct":
                    cur["correct"] = True
                elif s in STATUS or s in HEADER:
                    pass
                elif s.startswith("Learn more") or s.startswith("Watch ") or not s:
                    pass  # enlaces / vacio
                else:
                    cur["rationale"] += (" " + s)
        if cur:
            options.append(cur)
        for o in options:
            o["rationale"] = o["rationale"].strip()

        correct = [o["letter"] for o in options if o["correct"]]
        if len(options) < 2:
            quarantine.append({"n": n, "reason": f"pocas opciones ({len(options)})", "stem": stem[:300]})
            continue
        if len(correct) >= 2:
            quarantine.append({"n": n, "reason": f"multi-respuesta ({len(correct)} correctas)", "stem": stem[:300], "correct_letters": correct})
            continue
        if len(correct) == 0:
            quarantine.append({"n": n, "reason": "sin opcion marcada Correct", "stem": stem[:300]})
            continue

        letters = [o["letter"] for o in options]
        clean.append({
            "n": n, "stem": stem,
            "options": [{"text": o["text"], "rationale": o["rationale"]} for o in options],
            "correct_letter": correct[0],
            "correct_index": letters.index(correct[0]),
            "correct_text": options[letters.index(correct[0])]["text"],
        })

    return clean, quarantine, len(anchors)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exam", required=True)
    ap.add_argument("--tag", required=True)
    args = ap.parse_args()
    src = pathlib.Path(args.exam)
    if not src.is_absolute():
        src = (pathlib.Path.cwd() / src).resolve()
    print(f">> parseando OFICIAL: {src}", flush=True)
    clean, quarantine, total = parse(src)
    (DIR / f"parsed_{args.tag}.json").write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIR / f"quarantine_{args.tag}.json").write_text(json.dumps(quarantine, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> anclas: {total} | limpias: {len(clean)} | cuarentena: {len(quarantine)} | "
          f"suma {'OK' if len(clean)+len(quarantine)==total else 'MISMATCH'}", flush=True)
    from collections import Counter
    for r, c in Counter(q["reason"] for q in quarantine).most_common():
        print(f"   cuarentena[{c}]: {r}", flush=True)
    # sanity: conteo de opciones
    print("   dist opciones:", dict(Counter(len(q["options"]) for q in clean)), flush=True)


if __name__ == "__main__":
    main()
