#!/usr/bin/env python3
"""Prepara la deduplicacion para AIP-C01: extrae un texto-concepto por cada
pregunta nueva (de cada examen) y por cada carta existente del universo Anki.

No 'destila' con LLM aqui (eso lo hace el juez). Normaliza a texto plano
enunciado+opcion-correcta (nueva) / enunciado+opciones (existente).

Salidas:
  dedupe/existing_concepts.json        -> [{id, query, concept_text}]  (universo Anki)
  dedupe/new_concepts_<tag>.json       -> [{n, concept_text, stem, correct_text, category}]
"""
import argparse
import json
import pathlib
import re

DIR = pathlib.Path(__file__).resolve().parent


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"&[a-z]+;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def build_existing():
    existing = json.loads((DIR / "existing_cards.json").read_text(encoding="utf-8"))
    out = []
    for c in existing:
        concept = f"{c['question']} {c.get('options','')}".strip()
        out.append({"id": c["note_id"], "query": c.get("query", ""),
                    "concept_text": clean(concept)})
    (DIR / "existing_concepts.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(out)


def build_new(tag):
    new = json.loads((DIR / f"parsed_{tag}.json").read_text(encoding="utf-8"))
    out = []
    for q in new:
        correct = q["options"][q["correct_index"]]["text"]
        concept = f"{clean(q['stem'])} || RESPUESTA: {clean(correct)}"
        out.append({"n": q["n"], "concept_text": concept,
                    "stem": clean(q["stem"]), "correct_text": clean(correct),
                    "category": q.get("category", "")})
    (DIR / f"new_concepts_{tag}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="*", default=["exam1", "exam2", "exam3"])
    args = ap.parse_args()
    ne = build_existing()
    print(f">> {ne} conceptos existentes (universo Anki)", flush=True)
    for tag in args.tags:
        nn = build_new(tag)
        print(f">> {nn} conceptos nuevos en {tag}", flush=True)


if __name__ == "__main__":
    main()
