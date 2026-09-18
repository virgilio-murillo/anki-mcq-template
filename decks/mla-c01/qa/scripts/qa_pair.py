#!/usr/bin/env python3
"""Fase 1: empareja cada carta con su bloque fuente (pregunta + respuesta oficial).

- Keys tipo mla01-q7, mla01-q7b, mla01-q21a -> PREGUNTA 7/21 del deck01_source.txt
- Keys tipo mla01-r3-kinesis -> refuerzo tematico SIN pregunta base directa (source_block=None,
  se marca is_refuerzo_tematico=True; el revisor las juzga por correccion tecnica/alucinacion,
  no por fidelidad a una pregunta fuente).
Salida: kiro-test/qa_cards_paired.json
"""
import json
import re
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"

SRC = {
    "mla_c01_01.py": KT / "deck01_source.txt",
    "mla_c01_02.py": KT / "deck02_source.txt",
}


def load_blocks(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    parts = re.split(r'(?m)^===== PREGUNTA (\d+) =====\s*$', text)
    blocks = {}
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        blocks[n] = parts[i + 1].strip()
    return blocks


def qnum(key):
    # mla01-q7b -> 7 ; mla01-q21a -> 21 ; mla02-q40b -> 40 ; refuerzo r* -> None
    m = re.search(r'-q(\d+)', key)
    return int(m.group(1)) if m else None


def main():
    cards = json.loads((KT / "qa_cards.json").read_text(encoding="utf-8"))
    blocks_by_deck = {df: load_blocks(p) for df, p in SRC.items()}

    paired = 0
    thematic = 0
    unmatched = []
    for c in cards:
        df = c["deck_file"]
        n = qnum(c["key"])
        if n is None:
            c["source_block"] = None
            c["is_refuerzo_tematico"] = True
            c["source_q"] = None
            thematic += 1
        else:
            blk = blocks_by_deck[df].get(n)
            c["source_block"] = blk
            c["is_refuerzo_tematico"] = False
            c["source_q"] = n
            if blk:
                paired += 1
            else:
                unmatched.append(c["key"])
    dst = KT / "qa_cards_paired.json"
    dst.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> cartas totales: {len(cards)}", flush=True)
    print(f">> emparejadas con pregunta fuente: {paired}", flush=True)
    print(f">> refuerzos tematicos (sin pregunta base): {thematic}", flush=True)
    if unmatched:
        print(f">> SIN MATCH ({len(unmatched)}): {unmatched}", flush=True)
    print(f">> escrito {dst.relative_to(BASE)}", flush=True)


if __name__ == "__main__":
    main()
