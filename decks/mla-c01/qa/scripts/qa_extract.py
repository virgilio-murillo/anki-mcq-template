#!/usr/bin/env python3
"""Extrae las cartas de los generadores MLA-C01 a un JSON revisable.

Estrategia: importar el modulo generador es arriesgado porque el generador llama
create(...) top-level (dispara build+verify). En su lugar ejecutamos el archivo
en un namespace controlado donde `create` es un no-op que captura los kwargs, y
`card`/anki_mcq siguen siendo los reales. Asi obtenemos la lista `cards` exacta
sin construir/verificar ni importar a Anki.
"""
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]   # decks/mla-c01
REPO = BASE.parents[1]                                # repo root
sys.path.insert(0, str(REPO))

from anki_mcq import card as real_card  # noqa: E402

GEN_FILES = ["mla_c01_01.py", "mla_c01_02.py"]


def extract(genfile):
    path = BASE / genfile
    captured = {"cards": None}

    def fake_create(deck_name, cards, out_path, **kwargs):
        captured["cards"] = cards
        captured["deck_name"] = deck_name
        return len(cards)

    ns = {
        "card": real_card,
        "create": fake_create,
        "__name__": "__gen__",
        "__file__": str(path),
    }
    code = compile(path.read_text(encoding="utf-8"), str(path), "exec")
    exec(code, ns)  # noqa: S102 - trusted local file
    # Preferir la lista pasada a create(); si no, la variable global `cards`.
    cards = captured["cards"] if captured["cards"] is not None else ns.get("cards")
    deck_name = captured.get("deck_name", genfile)
    return deck_name, cards


def main():
    out = []
    for genfile in GEN_FILES:
        deck_name, cards = extract(genfile)
        print(f">> {genfile}: {len(cards)} cartas (deck '{deck_name}')", flush=True)
        for ci, c in enumerate(cards, start=1):
            out.append({
                "deck_file": genfile,
                "deck_name": deck_name,
                "card_index": ci,           # 1-based, igual que verify_deck
                "key": c["key"],
                "question": c["question"],
                "options": c["options"],
                "correct_index": c["correct"],
                "correct_text": c["options"][c["correct"]],
                "answer_html": c["answer"],
            })
    dst = BASE / "kiro-test" / "qa_cards.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> extraidas {len(out)} cartas -> {dst.relative_to(BASE)}", flush=True)


if __name__ == "__main__":
    main()
