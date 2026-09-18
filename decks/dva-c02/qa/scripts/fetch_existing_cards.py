#!/usr/bin/env python3
"""
Fetch existing DVA-C02 cards from Anki (all subdecks) with their real text,
to build the corpus we dedup against. Writes kiro-test/existing_cards.json.
"""
import json, urllib.request

ANKI = "http://localhost:8765"
def invoke(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKI, data=payload, headers={"Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    if d.get("error"): raise RuntimeError(d["error"])
    return d["result"]

note_ids = invoke("findNotes", query="deck:DVA-C02::*")
notes = invoke("notesInfo", notes=note_ids)
cards = []
for n in notes:
    f = n["fields"]
    # Common MCQ note types store the question in a field; grab the most text-y fields.
    front = ""
    for key in ("Front", "Question", "Text"):
        if key in f and f[key]["value"].strip():
            front = f[key]["value"]; break
    if not front:
        # fallback: first non-empty field
        for k, v in f.items():
            if v["value"].strip():
                front = v["value"]; break
    # also capture options/answer field if present for richer context
    extra = ""
    for key in ("Options", "Back", "Answer", "Extra"):
        if key in f and f[key]["value"].strip():
            extra = f[key]["value"]; break
    tags = n.get("tags", [])
    mcqkey = next((t.split(":",1)[1] for t in tags if t.startswith("mcqkey:")), "")
    cards.append({"noteId": n["noteId"], "key": mcqkey, "front": front, "extra": extra, "tags": tags})

json.dump(cards, open("kiro-test/existing_cards.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"fetched {len(cards)} existing cards -> kiro-test/existing_cards.json")
# quick tag/key coverage
with_key = sum(1 for c in cards if c["key"])
print(f"cards with mcqkey tag: {with_key}/{len(cards)}")
