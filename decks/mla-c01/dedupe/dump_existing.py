#!/usr/bin/env python3
"""Vuelca TODAS las cartas existentes en Anki (MLA-C01::* + DVA-C02::*) a JSON.
Es el 'universo de deduplicacion': lo que ya se estudia y NO debe repetirse.

Salida: dedupe/existing_cards.json  (lista de {deck, note_id, question_text})
Requiere Anki abierto con AnkiConnect (localhost:8765).
"""
import json
import re
import urllib.request
import pathlib

ANKI = "http://localhost:8765"
OUT = pathlib.Path(__file__).resolve().parent / "existing_cards.json"


def invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKI, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect {action}: {data['error']}")
    return data["result"]


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"&[a-z]+;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    out = []
    for query in ['deck:"MLA-C01::*"', 'deck:"DVA-C02::*"']:
        ids = invoke("findNotes", query=query)
        print(f">> {query}: {len(ids)} notas", flush=True)
        # notesInfo en lotes
        for i in range(0, len(ids), 100):
            batch = ids[i:i + 100]
            infos = invoke("notesInfo", notes=batch)
            for info in infos:
                flds = info.get("fields", {})
                # el campo del enunciado suele llamarse 'Question' o ser el primero
                qkey = "Question" if "Question" in flds else next(iter(flds))
                qtext = strip_html(flds.get(qkey, {}).get("value", ""))
                # incluir tambien el texto de opciones si existe un campo de opciones
                opts = ""
                for k in flds:
                    if "option" in k.lower() or "opcion" in k.lower():
                        opts += " " + strip_html(flds[k].get("value", ""))
                out.append({
                    "note_id": info["noteId"],
                    "query": query,
                    "question": qtext,
                    "options": strip_html(opts),
                })
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> volcadas {len(out)} cartas existentes -> {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
