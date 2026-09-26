#!/usr/bin/env python3
"""Genera el insumo del juez HIBRIDO: un bloque AUTOCONTENIDO por pregunta con sus
candidatos hibridos (semantico+BM25 via RRF) y la evidencia (coseno).

El juez debe emitir UN veredicto por pregunta, tratando cada bloque de forma
INDEPENDIENTE (una decision por pregunta, sin arrastrar contexto entre ellas).
"""
import argparse
import json
import pathlib

DIR = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    args = ap.parse_args()
    cands = json.loads((DIR / f"candidates_hybrid_{args.tag}.json").read_text(encoding="utf-8"))
    lines = []
    for o in cands:
        lines.append(f"### Q{o['n']}  [{o['category']}]")
        lines.append(f"NUEVA (ingles): {o['stem']}")
        lines.append(f"RESPUESTA CORRECTA: {o['correct_text']}")
        lines.append("Candidatas mas parecidas de lo que YA estudias "
                     "(retrieval hibrido semantico+lexico; cos = similitud semantica 0-1):")
        if o["candidates"]:
            for c in o["candidates"]:
                lines.append(f"  - [cos={c['cos']} src={c['src']}] {c['text']}")
        else:
            lines.append("  (sin candidatas)")
        lines.append("")
    (DIR / f"judge_hybrid_{args.tag}.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f">> judge_hybrid_{args.tag}.txt: {len(cands)} preguntas", flush=True)


if __name__ == "__main__":
    main()
