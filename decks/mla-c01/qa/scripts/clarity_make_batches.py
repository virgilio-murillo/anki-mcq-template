#!/usr/bin/env python3
"""Clarity-validation Phase A: build BLIND (stem-only) batches for the cold-candidate pass.

Reads kiro-test/qa_cards_paired.json and emits, per card, a STRIPPED payload that
contains ONLY what a cold candidate is allowed to see:
    key, question (plain text, tags+entities removed), options[4] (plain text, LABELED A-D)
It DELIBERATELY OMITS: correct_index, correct_text, answer_html, source_block, source_q.

Two artifact families are written:
  1. kiro-test/clarity/blind_batches/batch_NN.json   -> what candidates receive (NO answer key)
  2. kiro-test/clarity/answer_key.json               -> key -> correct_index (used ONLY by the
                                                        consolidator to score agreement; NEVER
                                                        shown to a candidate)

Also writes a rendered plain-text prompt file per batch so a human or an agent can eyeball
exactly what the candidate will read (kiro-test/clarity/blind_prompts/batch_NN.txt).
"""
import html
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"
OUT = KT / "clarity"
BLIND = OUT / "blind_batches"
PROMPTS = OUT / "blind_prompts"

BATCH_SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 8
LABELS = ["A", "B", "C", "D"]


def to_plain(s: str) -> str:
    """Strip HTML tags and unescape entities so the candidate sees clean prose.

    Cards store stems/options with tags like <b> and entities like &oacute;.
    A cold candidate must read natural text, not markup, so markup differences
    cannot leak the answer.
    """
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)          # drop remaining tags
    s = html.unescape(s)                    # &oacute; -> ó
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main():
    cards = json.loads((KT / "qa_cards_paired.json").read_text(encoding="utf-8"))
    BLIND.mkdir(parents=True, exist_ok=True)
    PROMPTS.mkdir(parents=True, exist_ok=True)

    answer_key = {}
    n = 0
    for i in range(0, len(cards), BATCH_SIZE):
        batch = cards[i:i + BATCH_SIZE]
        bn = i // BATCH_SIZE + 1
        blind = []
        prompt_lines = []
        for c in batch:
            opts = [to_plain(o) for o in c["options"]]
            item = {
                "key": c["key"],
                "question": to_plain(c["question"]),
                "options": {LABELS[j]: opts[j] for j in range(len(opts))},
            }
            blind.append(item)
            answer_key[c["key"]] = {
                "correct_index": c["correct_index"],
                "correct_label": LABELS[c["correct_index"]],
                "deck_file": c["deck_file"],
                "is_refuerzo_tematico": c["is_refuerzo_tematico"],
            }
            prompt_lines.append(f"### CARD {c['key']}")
            prompt_lines.append(item["question"])
            for lab in LABELS[:len(opts)]:
                prompt_lines.append(f"  {lab}. {item['options'][lab]}")
            prompt_lines.append("")
        (BLIND / f"batch_{bn:02d}.json").write_text(
            json.dumps(blind, ensure_ascii=False, indent=2), encoding="utf-8")
        (PROMPTS / f"batch_{bn:02d}.txt").write_text(
            "\n".join(prompt_lines), encoding="utf-8")
        n += 1

    (OUT / "answer_key.json").write_text(
        json.dumps(answer_key, ensure_ascii=False, indent=2), encoding="utf-8")

    # leak self-check: assert no blind item carries any answer-bearing field
    leaked = []
    for f in sorted(BLIND.glob("batch_*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            for banned in ("correct_index", "correct_text", "answer_html",
                           "source_block", "source_q", "correct_label"):
                if banned in it:
                    leaked.append((f.name, it["key"], banned))
    print(f">> {len(cards)} cartas -> {n} lotes blind de <= {BATCH_SIZE}", flush=True)
    print(f">> answer_key.json: {len(answer_key)} entradas (NUNCA se muestra al candidato)", flush=True)
    print(f">> leak-check campos prohibidos en blind: {'FALLO ' + str(leaked) if leaked else 'OK (0)'}", flush=True)


if __name__ == "__main__":
    main()
