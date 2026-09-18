#!/usr/bin/env python3
"""Parser de practice_exam_2.txt -> emite UN registro por cada ancla 'Question'
(sin descartes silenciosos), y separa las no-estandar en cuarentena.

Segun el fallo del juez (v2-ec81d2):
- 65 preguntas totales (anclas '^Question$').
- Detectar tipo por conteo de lineas '^Correct$' por bloque (>=2 => multi-select).
- Cuarentenar: multi-select (motor no soporta 2-de-N), matching (sin 'Answer options'),
  zero-option (bloque con 'Answer options' pero 0 opciones A-E).
- Strip de las lineas de cabecera de tabla antes de segmentar opciones.

Salidas en dedupe/:
  new_exam_parsed.json    -> preguntas estandar limpias (single-correct, 4-5 opciones)
  new_exam_quarantine.json-> no-estandar con razon (para revision manual)
"""
import json
import re
import pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "notes" / "source" / "practice_exam_2.txt"
DIR = pathlib.Path(__file__).resolve().parent
OPT_RE = re.compile(r'^([A-E])\.\s+(.*)$')
HEADER = {"Option", "Correct answer", "Your selection", "Rationale"}


def parse():
    lines = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
    anchors = [i for i, l in enumerate(lines) if l.strip() == "Question"]
    clean, quarantine = [], []

    for qi, start in enumerate(anchors):
        end = anchors[qi + 1] if qi + 1 < len(anchors) else len(lines)
        block = lines[start + 1:end]
        n = qi + 1

        # matching-type u otro sin 'Answer options'
        ao_idx = next((k for k, l in enumerate(block) if l.strip() == "Answer options"), None)
        if ao_idx is None:
            stem = " ".join(x.strip() for x in block if x.strip())[:400]
            quarantine.append({"n": n, "reason": "sin 'Answer options' (matching-type u otro)", "stem": stem})
            continue

        stem = " ".join(x.strip() for x in block[:ao_idx] if x.strip())
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
                elif s in ("Not selected", "Selected") or s in HEADER:
                    pass
                elif s:
                    cur["rationale"] += (" " + s)
        if cur:
            options.append(cur)
        for o in options:
            o["rationale"] = o["rationale"].strip()

        correct = [o["letter"] for o in options if o["correct"]]

        if len(options) == 0:
            quarantine.append({"n": n, "reason": "zero-option (Answer options pero sin opciones A-E)", "stem": stem[:400]})
            continue
        if len(correct) >= 2:
            quarantine.append({"n": n, "reason": f"multi-select ({len(correct)} correctas; motor no soporta 2-de-N)",
                               "stem": stem[:400], "correct_letters": correct})
            continue
        if len(correct) == 0:
            quarantine.append({"n": n, "reason": "sin opcion marcada Correct", "stem": stem[:400]})
            continue

        clean.append({
            "n": n, "stem": stem,
            "options": [{"letter": o["letter"], "text": o["text"], "rationale": o["rationale"]} for o in options],
            "correct_letter": correct[0],
            "correct_index": [o["letter"] for o in options].index(correct[0]),
        })

    return clean, quarantine, len(anchors)


def main():
    clean, quarantine, total = parse()
    (DIR / "new_exam_parsed.json").write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIR / "new_exam_quarantine.json").write_text(json.dumps(quarantine, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> anclas 'Question' totales: {total}", flush=True)
    print(f">> estandar (a deduplicar): {len(clean)}", flush=True)
    print(f">> cuarentena (no-estandar): {len(quarantine)}", flush=True)
    print(f">> suma {len(clean)+len(quarantine)} == {total}? {'OK' if len(clean)+len(quarantine)==total else 'MISMATCH'}", flush=True)
    for q in quarantine:
        print(f"   Q{q['n']}: {q['reason']}", flush=True)


if __name__ == "__main__":
    main()
