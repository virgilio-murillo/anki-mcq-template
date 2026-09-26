#!/usr/bin/env python3
"""Boveda de vectores AMPLIADA para deduplicar los examenes OFICIALES.

Universo ya-conocido = 958 cartas de otras certs (existing_concepts.json)
                     + las 161 cartas AIP ya generadas (Top70+Extra), leidas de
                       los aip_c01_0{1,2,3}.py, para NO repetir lo que ya esta en el mazo.

Salida: vecstore_v2/  (universe_emb.npy, universe_meta.json, bm25_tokens.json, model.txt)
"""
import importlib.util
import json
import pathlib
import re

import numpy as np

DIR = pathlib.Path(__file__).resolve().parent
DECK = DIR.parent
STORE = DIR / "vecstore_v2"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where will would can could should must may might not company team wants needs approach solution option options data model models using use used el la los las de un una para que con por".split())


def bm25_tokens(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def strip_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def load_aip_cards():
    """Lee las 161 cartas AIP ya generadas desde los .py (question+opciones+key)."""
    import anki_mcq
    orig = anki_mcq.create
    anki_mcq.create = lambda *a, **k: None
    out = []
    try:
        for f in ("aip_c01_01.py", "aip_c01_02.py", "aip_c01_03.py"):
            spec = importlib.util.spec_from_file_location(f[:-3], DECK / f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for c in mod.cards:
                txt = strip_html(c["question"]) + " " + " ".join(strip_html(o) for o in c["options"])
                out.append({"note_id": None, "query": "aip-deck", "concept_text": txt, "src_key": c["key"]})
    finally:
        anki_mcq.create = orig
    return out


def main():
    base = json.loads((DIR / "existing_concepts.json").read_text(encoding="utf-8"))
    aip = load_aip_cards()
    universe = base + aip
    texts = [c["concept_text"] for c in universe]
    print(f">> universo ampliado: {len(base)} otras-certs + {len(aip)} AIP = {len(universe)}", flush=True)

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)
    emb = model.encode(texts, batch_size=64, show_progress_bar=True,
                       convert_to_numpy=True, normalize_embeddings=True).astype("float32")

    STORE.mkdir(exist_ok=True)
    np.save(STORE / "universe_emb.npy", emb)
    (STORE / "universe_meta.json").write_text(json.dumps(universe, ensure_ascii=False), encoding="utf-8")
    (STORE / "bm25_tokens.json").write_text(json.dumps([bm25_tokens(t) for t in texts], ensure_ascii=False), encoding="utf-8")
    (STORE / "model.txt").write_text(MODEL_NAME, encoding="utf-8")
    print(f">> guardado en {STORE}: emb {emb.shape}", flush=True)


if __name__ == "__main__":
    main()
