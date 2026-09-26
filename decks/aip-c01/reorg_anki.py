#!/usr/bin/env python3
"""Mueve las notas AIP-C01 en Anki a subdecks Top70 / Extra via changeDeck.
Mapea key -> noteId por el TEXTO EXACTO del campo Question (notesInfo no da GUID).
SOLO changeDeck (mover). No borra, no cambia campos ni progreso.
"""
import importlib.util
import json
import pathlib
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
DED = HERE / "dedupe"
EP = "http://localhost:8765"


def inv(action, **p):
    r = urllib.request.urlopen(urllib.request.Request(
        EP, data=json.dumps({"action": action, "version": 6, "params": p}).encode(),
        headers={"Content-Type": "application/json"}))
    d = json.load(r)
    if d.get("error"):
        raise RuntimeError(f"{action}: {d['error']}")
    return d["result"]


def load_cards(pyfile):
    spec = importlib.util.spec_from_file_location(pyfile.stem, pyfile)
    mod = importlib.util.module_from_spec(spec)
    import anki_mcq
    orig = anki_mcq.create
    anki_mcq.create = lambda *a, **k: None
    try:
        spec.loader.exec_module(mod)
    finally:
        anki_mcq.create = orig
    return mod.cards


def cards_of_notes(note_ids):
    if not note_ids:
        return []
    q = " OR ".join(f"nid:{n}" for n in note_ids)
    return inv("findCards", query=q)


def main():
    allq = {}
    for f in ("aip_c01_01.py", "aip_c01_02.py", "aip_c01_03.py"):
        for c in load_cards(HERE / f):
            allq[c["key"]] = c["question"]

    top_keys = [c["key"] for c in json.loads((DED / "top70.json").read_text())]
    over_keys = [c["key"] for c in json.loads((DED / "overflow.json").read_text())]

    ids = inv("findNotes", query="deck:AIP-C01::*")
    infos = inv("notesInfo", notes=ids)
    q2id = {}
    for x in infos:
        q2id.setdefault(x["fields"]["Question"]["value"], []).append(x["noteId"])

    def resolve(keys):
        out, miss = [], []
        for k in keys:
            hit = q2id.get(allq[k])
            if hit:
                out.append(hit.pop(0))
            else:
                miss.append(k)
        return out, miss

    inv("createDeck", deck="AIP-C01::Top70")
    inv("createDeck", deck="AIP-C01::Extra")

    top_ids, miss_top = resolve(top_keys)
    over_ids, miss_over = resolve(over_keys)
    print(f">> resueltas top={len(top_ids)}/{len(top_keys)} miss={len(miss_top)} | "
          f"extra={len(over_ids)}/{len(over_keys)} miss={len(miss_over)}", flush=True)
    if miss_top:
        print("   MISS top:", miss_top, flush=True)
    if miss_over:
        print("   MISS extra:", miss_over, flush=True)

    top_cards = cards_of_notes(top_ids)
    over_cards = cards_of_notes(over_ids)
    inv("changeDeck", cards=top_cards, deck="AIP-C01::Top70")
    inv("changeDeck", cards=over_cards, deck="AIP-C01::Extra")
    print(f">> movidas: {len(top_cards)} -> Top70, {len(over_cards)} -> Extra", flush=True)


if __name__ == "__main__":
    main()
