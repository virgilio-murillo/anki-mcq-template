#!/usr/bin/env python3
"""Retrieval hibrido (semantico + BM25, RRF) de los examenes OFICIALES contra el
universo AMPLIADO (vecstore_v2 = otras certs + 161 AIP ya en el mazo).

Igual metodo que hybrid_retrieve.py pero SIN truncar el texto de la carta (bug fix),
usando vecstore_v2 y los parsed_off{1,2}.json.

Uso: python hybrid_retrieve_official.py --tag off1
Salida: candidates_hybrid_<tag>.json
"""
import argparse
import json
import pathlib
import re

import numpy as np

DIR = pathlib.Path(__file__).resolve().parent
STORE = DIR / "vecstore_v2"
RRF_K = 60
DEPTH = 40
TOPK = 6
_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where will would can could should must may might not company team wants needs approach solution option options data model models using use used el la los las de un una para que con por".split())


def toks(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def rrf(sem, bm, k=RRF_K):
    sc = {}
    for r, i in enumerate(sem, 1):
        sc.setdefault(i, {"rrf": 0.0, "sem": None, "bm": None}); sc[i]["rrf"] += 1/(k+r); sc[i]["sem"] = r
    for r, i in enumerate(bm, 1):
        sc.setdefault(i, {"rrf": 0.0, "sem": None, "bm": None}); sc[i]["rrf"] += 1/(k+r); sc[i]["bm"] = r
    return sc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    args = ap.parse_args()

    U_emb = np.load(STORE / "universe_emb.npy")
    U_meta = json.loads((STORE / "universe_meta.json").read_text(encoding="utf-8"))
    U_tok = json.loads((STORE / "bm25_tokens.json").read_text(encoding="utf-8"))
    model_name = (STORE / "model.txt").read_text(encoding="utf-8").strip()
    ctext = [m["concept_text"] for m in U_meta]
    csrc = [("aip-deck" if m.get("query") == "aip-deck" else "otra-cert") for m in U_meta]

    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    model = SentenceTransformer(model_name)
    bm25 = BM25Okapi(U_tok)

    new = json.loads((DIR / f"parsed_{args.tag}.json").read_text(encoding="utf-8"))
    qtexts = [f"{q['stem']} || RESPUESTA: {q['correct_text']}" for q in new]
    Q = model.encode(qtexts, convert_to_numpy=True, normalize_embeddings=True).astype("float32")

    out = []
    for q, qv, qt in zip(new, Q, qtexts):
        cos = U_emb @ qv
        sem = [int(i) for i in np.argsort(-cos)[:DEPTH]]
        bm = [int(i) for i in np.argsort(-bm25.get_scores(toks(qt)))[:DEPTH]]
        fused = rrf(sem, bm)
        top = sorted(fused.items(), key=lambda kv: kv[1]["rrf"], reverse=True)[:TOPK]
        cands = [{"src": csrc[i], "cos": round(float(cos[i]), 3), "full_text": ctext[i]} for i, _ in top]
        out.append({"n": q["n"], "stem": q["stem"], "correct_text": q["correct_text"], "candidates": cands})

    (DIR / f"candidates_hybrid_{args.tag}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    hi = sum(1 for o in out if o["candidates"] and o["candidates"][0]["cos"] >= 0.60)
    tops = sorted(o["candidates"][0]["cos"] if o["candidates"] else 0 for o in out)
    print(f">> {args.tag}: {len(out)} preguntas. top-cos>=0.60: {hi}. "
          f"cos min/med/max: {tops[0]:.2f}/{tops[len(tops)//2]:.2f}/{tops[-1]:.2f}", flush=True)


if __name__ == "__main__":
    main()
