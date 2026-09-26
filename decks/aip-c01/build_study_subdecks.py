#!/usr/bin/env python3
"""Reparte las 161 cartas AIP-C01 en dos subdecks de estudio, SIN reescribir cartas:
  AIP-C01::Top70   -> las 70 mejores (top70.json)
  AIP-C01::Extra   -> el resto (overflow.json)

Reutiliza las cartas YA verificadas de aip_c01_0{1,2,3}.py (misma key => mismo GUID
estable, asi Anki las MUEVE al reimportar, no las duplica). Construye 2 .apkg.

Uso: ../../.venv/bin/python decks/aip-c01/build_study_subdecks.py
Requiere correr desde la raiz del repo o dejar que resuelva rutas absolutas.
"""
import importlib.util
import json
import pathlib

from anki_mcq.engine import build_deck

HERE = pathlib.Path(__file__).resolve().parent          # decks/aip-c01
DED = HERE / "dedupe"


def load_cards(pyfile):
    spec = importlib.util.spec_from_file_location(pyfile.stem, pyfile)
    mod = importlib.util.module_from_spec(spec)
    # evitar que el create(...) del final importe a Anki: parchear create
    import anki_mcq
    orig_create = anki_mcq.create
    anki_mcq.create = lambda *a, **k: None
    try:
        spec.loader.exec_module(mod)
    finally:
        anki_mcq.create = orig_create
    return mod.cards


def main():
    # 1) juntar todas las cartas por key
    allcards = {}
    for f in ("aip_c01_01.py", "aip_c01_02.py", "aip_c01_03.py"):
        for c in load_cards(HERE / f):
            allcards[c["key"]] = c
    print(f">> cartas totales cargadas: {len(allcards)}")

    top = json.loads((DED / "top70.json").read_text(encoding="utf-8"))
    over = json.loads((DED / "overflow.json").read_text(encoding="utf-8"))
    top_keys = [c["key"] for c in top]
    over_keys = [c["key"] for c in over]

    missing = [k for k in top_keys + over_keys if k not in allcards]
    if missing:
        raise SystemExit(f"keys en seleccion pero no en cartas: {missing[:10]} ...")

    top_cards = [allcards[k] for k in top_keys]
    extra_cards = [allcards[k] for k in over_keys]
    print(f">> Top70={len(top_cards)}  Extra={len(extra_cards)}  (suma {len(top_cards)+len(extra_cards)})")

    out = HERE / "out"
    build_deck("AIP-C01::Top70", top_cards, str(out / "AIP-C01_Top70.apkg"), verbose=True)
    build_deck("AIP-C01::Extra", extra_cards, str(out / "AIP-C01_Extra.apkg"), verbose=True)


if __name__ == "__main__":
    main()
