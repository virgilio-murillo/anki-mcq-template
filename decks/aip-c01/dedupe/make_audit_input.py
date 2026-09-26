#!/usr/bin/env python3
"""Insumo para la AUDITORIA de falsos-COVERED (investigacion 638727cf).

Por cada pregunta marcada COVERED en verdicts_hybrid_<tag>.jsonl, junta:
  - la pregunta AIP completa (stem + opcion correcta + opciones)
  - el concepto y top_cos que registro el juez v2
  - sus candidatos hibridos (las cartas del universo que supuestamente la cubren),
    con su texto y coseno.
El auditor decide RESCATAR (tipo A objetivo-distinto | tipo B profundidad) o
CONFIRMAR_COVERED.

Salida: audit_covered_<tag>.txt (bloques autocontenidos) y audit_covered_<tag>.json
"""
import argparse
import json
import pathlib

DIR = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    args = ap.parse_args()

    parsed = {q["n"]: q for q in json.loads((DIR / f"parsed_{args.tag}.json").read_text(encoding="utf-8"))}
    cands = {o["n"]: o for o in json.loads((DIR / f"candidates_hybrid_{args.tag}.json").read_text(encoding="utf-8"))}
    verd = {}
    for line in (DIR / f"verdicts_hybrid_{args.tag}.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            o = json.loads(line)
            verd[o["n"]] = o

    covered = [n for n in sorted(verd) if verd[n]["verdict"] == "COVERED"]
    blocks, rows = [], []
    for n in covered:
        q = parsed[n]
        v = verd[n]
        c = cands.get(n, {"candidates": []})
        correct = q["options"][q["correct_index"]]["text"]
        rows.append({"n": n, "category": q.get("category", ""), "stem": q["stem"],
                     "correct_text": correct, "concepto": v.get("concepto", ""),
                     "top_cos": v.get("top_cos"),
                     "candidates": c.get("candidates", [])})
        blocks.append(f"### Q{n}  [{q.get('category','')}]  (juez v2: COVERED, concepto='{v.get('concepto','')}', top_cos={v.get('top_cos')})")
        blocks.append(f"PREGUNTA AIP (Professional/GenAI): {q['stem']}")
        blocks.append(f"RESPUESTA CORRECTA: {correct}")
        blocks.append("Otras opciones: " + " | ".join(
            o["text"] for i, o in enumerate(q["options"]) if i != q["correct_index"]))
        blocks.append("Carta(s) del universo que supuestamente la cubren (lo que YA estudiaste, nivel associate/foundational):")
        for cc in c.get("candidates", [])[:4]:
            blocks.append(f"  - [cos={cc['cos']} src={cc['src']}] {cc['text']}")
        blocks.append("")

    (DIR / f"audit_covered_{args.tag}.txt").write_text("\n".join(blocks), encoding="utf-8")
    (DIR / f"audit_covered_{args.tag}.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> {args.tag}: {len(covered)} COVERED a auditar", flush=True)


if __name__ == "__main__":
    main()
