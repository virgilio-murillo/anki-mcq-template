#!/usr/bin/env python3
"""Retrieval de candidatos para el dedup por concepto (prefiltro, sin dependencias).

Para cada pregunta NUEVA de un examen, encuentra las cartas EXISTENTES del universo
(y opcionalmente de examenes previos ya aceptados como NEW, para la cascada) mas
parecidas por TF-IDF sobre terminos tecnicos. Esto NO decide COVERED/NEW: solo
reduce 958+ existentes a un puñado de candidatos por pregunta, para que el JUEZ
(agente) decida por concepto leyendo solo lo relevante.

Salida:
  dedupe/candidates_<tag>.json -> [{n, stem, correct_text, category,
                                    candidates:[{src, score, text}]}]

src = "anki" (universo) o "newN" (pregunta ya aceptada de un examen previo).
"""
import argparse
import json
import math
import pathlib
import re
from collections import Counter

DIR = pathlib.Path(__file__).resolve().parent

STOP = set("""a an the of to in on for with and or is are be as by from at into that this these those
which what when where who whom will would can could should must may might not no least most best
using use used uses following given requirements requirement solution solutions option options company
team wants needs need requires require approach provide provides provided minimal overhead operational
their its our your it they them then than also such over under across per each any all both new
data model models application applications service services aws amazon customer customers user users
would like want scenario meets meet""".split())

TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")


def toks(s):
    s = re.sub(r"<[^>]+>", " ", s or "").lower()
    out = []
    for t in TOKEN.findall(s):
        t = t.strip(".-")
        if len(t) < 2 or t in STOP or t.isdigit():
            continue
        out.append(t)
    return out


def build_idf(docs_tokens):
    df = Counter()
    for tks in docs_tokens:
        for t in set(tks):
            df[t] += 1
    n = len(docs_tokens)
    return {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}


def vec(tks, idf):
    tf = Counter(tks)
    v = {t: (1 + math.log(c)) * idf.get(t, math.log(len(idf) + 1)) for t, c in tf.items()}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {t: x / norm for t, x in v.items()}


def cosine(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, help="exam1|exam2|exam3")
    ap.add_argument("--also-new", nargs="*", default=[],
                    help="tags de examenes previos cuyas NEW aceptadas entran al universo (cascada)")
    ap.add_argument("--topk", type=int, default=6)
    args = ap.parse_args()

    existing = json.loads((DIR / "existing_concepts.json").read_text(encoding="utf-8"))
    new = json.loads((DIR / f"new_concepts_{args.tag}.json").read_text(encoding="utf-8"))

    # corpus existente = universo Anki + NEW aceptadas de examenes previos (cascada)
    corpus = [{"src": "anki", "text": e["concept_text"]} for e in existing]
    for prev in args.also_new:
        accepted = json.loads((DIR / f"accepted_new_{prev}.json").read_text(encoding="utf-8"))
        for a in accepted:
            corpus.append({"src": prev, "text": f"{a['stem']} || RESPUESTA: {a['correct_text']}"})

    corpus_tokens = [toks(c["text"]) for c in corpus]
    new_tokens = [toks(q["concept_text"]) for q in new]
    idf = build_idf(corpus_tokens + new_tokens)
    corpus_vecs = [vec(t, idf) for t in corpus_tokens]

    out = []
    for q, qt in zip(new, new_tokens):
        qv = vec(qt, idf)
        scored = sorted(
            ((cosine(qv, cv), i) for i, cv in enumerate(corpus_vecs)),
            reverse=True)[:args.topk]
        cands = [{"src": corpus[i]["src"], "score": round(s, 3),
                  "text": corpus[i]["text"][:400]} for s, i in scored if s > 0.02]
        out.append({"n": q["n"], "category": q.get("category", ""),
                    "stem": q["stem"], "correct_text": q["correct_text"],
                    "candidates": cands})

    (DIR / f"candidates_{args.tag}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    tops = [o["candidates"][0]["score"] if o["candidates"] else 0 for o in out]
    hi = sum(1 for s in tops if s >= 0.35)
    print(f">> {args.tag}: {len(out)} preguntas, corpus={len(corpus)} "
          f"(anki+{len(args.also_new)} prev). top-score>=0.35: {hi}", flush=True)


if __name__ == "__main__":
    main()
