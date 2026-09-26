#!/usr/bin/env python3
"""Extrae las preguntas NEW completas por examen para generar el deck.

Combina: verdict NEW (vs universo Anki) AND no excluida por cascada cruzada.
Salida: new_to_generate_<tag>.json con {n, category, stem, options[], correct_index,
correct_text, concepto}.
"""
import json
import pathlib

DIR = pathlib.Path(__file__).resolve().parent
TAGS = ["exam1", "exam2", "exam3"]


def main():
    cross = json.loads((DIR / "cross_dupes.json").read_text(encoding="utf-8"))
    grand = 0
    for t in TAGS:
        parsed = {q["n"]: q for q in json.loads((DIR / f"parsed_{t}.json").read_text(encoding="utf-8"))}
        verd = {}
        concepts = {}
        for line in (DIR / f"dedup_verdicts_{t}.jsonl").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                o = json.loads(line)
                verd[o["n"]] = o["verdict"]
                concepts[o["n"]] = o.get("concepto", "")
        excl = set(cross.get(t, []))
        out = []
        for n, q in sorted(parsed.items()):
            if verd.get(n) == "NEW" and n not in excl:
                out.append({**q, "concepto": concepts.get(n, "")})
        (DIR / f"new_to_generate_{t}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        grand += len(out)
        print(f">> {t}: {len(out)} NEW a generar "
              f"(de {len(parsed)} limpias; {sum(1 for v in verd.values() if v=='COVERED')} covered, "
              f"{len(excl)} dup cruzado)", flush=True)
    print(f">> TOTAL a generar: {grand}", flush=True)


if __name__ == "__main__":
    main()
