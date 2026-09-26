#!/usr/bin/env python3
"""Construye la boveda de vectores del universo ya-estudiado (para dedup HIBRIDO).

Disenado por la investigacion 86a5dde9 (consenso de 5 fuentes, validado):
- Modelo: paraphrase-multilingual-MiniLM-L12-v2 (cross-lingual EN<->ES, dim 384,
  sin prefijos query/passage; el universo esta en espanol y las preguntas en ingles).
- Boveda: numpy denso (coseno via matmul). Para ~1000 vectores faiss/chroma son
  innecesarios; brute-force es exacto y sub-segundo.
- Ademas del indice denso, tokeniza el universo para BM25 (retrieval lexico).

Entrada:  existing_concepts.json  ([{id, query, concept_text}], 958 cartas Anki)
Salida (en dedupe/vecstore/):
  universe_emb.npy      float32 [N,384] L2-normalizado
  universe_meta.json    [{id, query, concept_text}] alineado con las filas
  bm25_tokens.json      [[tok,...], ...] tokens por carta (para reconstruir BM25)
  model.txt             nombre del modelo usado (para verificar consistencia)

Uso:  ../../.venv/bin/python dedupe/build_vector_store.py
"""
import json
import pathlib
import re

import numpy as np

DIR = pathlib.Path(__file__).resolve().parent
STORE = DIR / "vecstore"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where who will would can could should must may might not no company team wants needs approach solution option options data model models using use used el la los las de un una para que con por".split())


def bm25_tokens(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def main():
    existing = json.loads((DIR / "existing_concepts.json").read_text(encoding="utf-8"))
    texts = [c["concept_text"] for c in existing]
    print(f">> universo: {len(texts)} cartas", flush=True)

    from sentence_transformers import SentenceTransformer
    print(f">> cargando modelo {MODEL_NAME} (descarga ~470MB la 1a vez)...", flush=True)
    model = SentenceTransformer(MODEL_NAME)
    print(">> embebiendo universo...", flush=True)
    emb = model.encode(texts, batch_size=64, show_progress_bar=True,
                       convert_to_numpy=True, normalize_embeddings=True)
    emb = emb.astype("float32")

    STORE.mkdir(exist_ok=True)
    np.save(STORE / "universe_emb.npy", emb)
    (STORE / "universe_meta.json").write_text(
        json.dumps(existing, ensure_ascii=False), encoding="utf-8")
    (STORE / "bm25_tokens.json").write_text(
        json.dumps([bm25_tokens(t) for t in texts], ensure_ascii=False), encoding="utf-8")
    (STORE / "model.txt").write_text(MODEL_NAME, encoding="utf-8")
    print(f">> guardado en {STORE}: emb shape={emb.shape}", flush=True)


if __name__ == "__main__":
    main()
