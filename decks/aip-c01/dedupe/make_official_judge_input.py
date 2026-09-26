#!/usr/bin/env python3
"""Insumo del juez para los examenes OFICIALES. Bloques autocontenidos con TEXTO
COMPLETO de las cartas-cubridoras y su cos. Criterio PRO-INCLUSION (oficial = valioso).
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
    L = []
    for o in cands:
        L.append(f"### Q{o['n']}")
        L.append(f"OFICIAL (AIP-C01 profesional): {o['stem']}")
        L.append(f"RESPUESTA CORRECTA: {o['correct_text']}")
        L.append("Cartas que YA tienes (otras certs + tu mazo AIP actual; cos = similitud 0-1, TEXTO COMPLETO):")
        for c in o["candidates"]:
            L.append(f"  - [cos={c['cos']} src={c['src']}] {c['full_text']}")
        L.append("")
    (DIR / f"judge_official_{args.tag}.txt").write_text("\n".join(L), encoding="utf-8")
    print(f">> judge_official_{args.tag}.txt: {len(cands)} preguntas")


if __name__ == "__main__":
    main()
