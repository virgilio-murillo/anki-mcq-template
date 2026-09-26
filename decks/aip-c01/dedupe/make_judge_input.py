#!/usr/bin/env python3
"""Construye el insumo COMPACTO para el juez de dedup de un examen.

Escribe dedupe/judge_<tag>.txt: por cada pregunta nueva, su enunciado+respuesta y
sus candidatos mas cercanos del universo (Anki + examenes previos en cascada).
El juez decide COVERED/NEW por CONCEPTO y escribe dedup_verdicts_<tag>.jsonl.
"""
import argparse
import json
import pathlib

DIR = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    args = ap.parse_args()
    cands = json.loads((DIR / f"candidates_{args.tag}.json").read_text(encoding="utf-8"))
    lines = []
    for o in cands:
        lines.append(f"### Q{o['n']}  [{o['category']}]")
        lines.append(f"NUEVA: {o['stem']}")
        lines.append(f"RESPUESTA CORRECTA: {o['correct_text']}")
        if o["candidates"]:
            lines.append("Candidatas mas parecidas de lo que YA estudias:")
            for c in o["candidates"]:
                lines.append(f"  - [{c['src']} sim={c['score']}] {c['text']}")
        else:
            lines.append("(sin candidatas parecidas en el universo)")
        lines.append("")
    (DIR / f"judge_{args.tag}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f">> judge_{args.tag}.txt: {len(cands)} preguntas", flush=True)


if __name__ == "__main__":
    main()
