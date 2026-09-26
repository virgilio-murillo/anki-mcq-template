#!/usr/bin/env python3
"""Retrieval HIBRIDO (semantico + BM25, fusion RRF) para el dedup por concepto.

Disenado por la investigacion 86a5dde9 (validado adversarialmente):
- Semantico: coseno via numpy matmul contra la boveda (embeddings del universo).
- Lexico: BM25Okapi (rank-bm25) sobre los tokens del universo.
- Fusion: Reciprocal Rank Fusion (RRF), score = sum 1/(k+rank), k=60. Rank-based:
  evita calibrar escalas incomparables (BM25 no acotado vs coseno en [-1,1]).
  NO se umbraliza el score RRF (los scores no son comparables entre queries);
  se toma top-k por profundidad de fusion.
- Cascada: los candidatos incluyen el universo Anki + las NEW aceptadas de
  examenes previos (para no repetir conceptos ENTRE los 3 examenes).

Entrada: vecstore/ (build_vector_store.py) + new_concepts_<tag>.json
Salida:  candidates_hybrid_<tag>.json ->
  [{n, category, stem, correct_text,
    candidates:[{src, rrf, cos, bm25_rank, cos_rank, text}]}]

Uso:
  ../../.venv/bin/python dedupe/hybrid_retrieve.py --tag exam1
  ../../.venv/bin/python dedupe/hybrid_retrieve.py --tag exam2 --also-new exam1
  ../../.venv/bin/python dedupe/hybrid_retrieve.py --tag exam3 --also-new exam1 exam2
"""
import argparse
import json
import pathlib
import re

import numpy as np

DIR = pathlib.Path(__file__).resolve().parent
STORE = DIR / "vecstore"
RRF_K = 60
DEPTH = 40          # profundidad de cada lista antes de fusionar
TOPK = 6            # candidatos finales por pregunta

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where who will would can could should must may might not no company team wants needs approach solution option options data model models using use used el la los las de un una para que con por".split())


def bm25_tokens(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def rrf_fuse(sem_order, bm_order, k=RRF_K):
    """sem_order/bm_order: listas de indices (mejor primero). Devuelve
    {idx: {rrf, sem_rank, bm_rank}} para todos los idx que aparezcan."""
    score = {}
    for rank, idx in enumerate(sem_order, start=1):
        score.setdefault(idx, {"rrf": 0.0, "sem_rank": None, "bm_rank": None})
        score[idx]["rrf"] += 1.0 / (k + rank)
        score[idx]["sem_rank"] = rank
    for rank, idx in enumerate(bm_order, start=1):
        score.setdefault(idx, {"rrf": 0.0, "sem_rank": None, "bm_rank": None})
        score[idx]["rrf"] += 1.0 / (k + rank)
        score[idx]["bm_rank"] = rank
    return score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--also-new", nargs="*", default=[])
    args = ap.parse_args()

    # boveda del universo Anki
    U_emb = np.load(STORE / "universe_emb.npy")
    U_meta = json.loads((STORE / "universe_meta.json").read_text(encoding="utf-8"))
    U_tokens = json.loads((STORE / "bm25_tokens.json").read_text(encoding="utf-8"))
    model_name = (STORE / "model.txt").read_text(encoding="utf-8").strip()

    # corpus = universo + NEW aceptadas de examenes previos (cascada)
    corpus_texts = [m["concept_text"] for m in U_meta]
    corpus_src = ["anki"] * len(U_meta)
    corpus_tokens = list(U_tokens)
    extra_emb_texts = []
    for prev in args.also_new:
        acc = json.loads((DIR / f"accepted_new_{prev}.json").read_text(encoding="utf-8"))
        for a in acc:
            t = f"{a['stem']} || RESPUESTA: {a['correct_text']}"
            corpus_texts.append(t)
            corpus_src.append(prev)
            corpus_tokens.append(bm25_tokens(t))
            extra_emb_texts.append(t)

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)

    if extra_emb_texts:
        extra_emb = model.encode(extra_emb_texts, convert_to_numpy=True,
                                 normalize_embeddings=True).astype("float32")
        C_emb = np.vstack([U_emb, extra_emb])
    else:
        C_emb = U_emb

    from rank_bm25 import BM25Okapi
    bm25 = BM25Okapi(corpus_tokens)

    new = json.loads((DIR / f"new_concepts_{args.tag}.json").read_text(encoding="utf-8"))
    q_texts = [q["concept_text"] for q in new]
    Q_emb = model.encode(q_texts, convert_to_numpy=True,
                         normalize_embeddings=True).astype("float32")

    out = []
    for q, qv, qtxt in zip(new, Q_emb, q_texts):
        cos = C_emb @ qv                                  # coseno (vectores unitarios)
        sem_order = list(np.argsort(-cos)[:DEPTH])
        bm_scores = bm25.get_scores(bm25_tokens(qtxt))
        bm_order = list(np.argsort(-bm_scores)[:DEPTH])
        fused = rrf_fuse([int(i) for i in sem_order], [int(i) for i in bm_order])
        top = sorted(fused.items(), key=lambda kv: kv[1]["rrf"], reverse=True)[:TOPK]
        cands = []
        for idx, sc in top:
            cands.append({
                "src": corpus_src[idx],
                "rrf": round(sc["rrf"], 5),
                "cos": round(float(cos[idx]), 3),
                "sem_rank": sc["sem_rank"],
                "bm_rank": sc["bm_rank"],
                "text": corpus_texts[idx][:400],
            })
        out.append({"n": q["n"], "category": q.get("category", ""),
                    "stem": q["stem"], "correct_text": q["correct_text"],
                    "candidates": cands})

    (DIR / f"candidates_hybrid_{args.tag}.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    # diagnostico: top-cos por pregunta
    tops = sorted(o["candidates"][0]["cos"] if o["candidates"] else 0 for o in out)
    hi = sum(1 for o in out if o["candidates"] and o["candidates"][0]["cos"] >= 0.6)
    print(f">> {args.tag}: {len(out)} preguntas, corpus={len(corpus_texts)} "
          f"(anki+{len(extra_emb_texts)} prev). top-cos>=0.60: {hi}. "
          f"cos min/med/max: {tops[0]:.2f}/{tops[len(tops)//2]:.2f}/{tops[-1]:.2f}", flush=True)


if __name__ == "__main__":
    main()
