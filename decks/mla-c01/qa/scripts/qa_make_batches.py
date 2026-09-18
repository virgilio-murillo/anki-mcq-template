#!/usr/bin/env python3
"""Fase 3: parte las 112 cartas emparejadas en lotes para revisores LLM.

Escribe kiro-test/qa_batches/batch_NN.json con una lista de cartas (con su
source_block) para que cada sub-agente revisor audite ese lote y emita
kiro-test/qa_reviews/batch_NN.jsonl (una linea JSON por carta).
"""
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"
BATCH_SIZE = 7

def main():
    cards = json.loads((KT / "qa_cards_paired.json").read_text(encoding="utf-8"))
    outdir = KT / "qa_batches"
    outdir.mkdir(exist_ok=True)
    (KT / "qa_reviews").mkdir(exist_ok=True)
    n_batches = 0
    for i in range(0, len(cards), BATCH_SIZE):
        batch = cards[i:i + BATCH_SIZE]
        bn = i // BATCH_SIZE + 1
        # Solo los campos que el revisor necesita (evita ruido)
        slim = [{
            "key": c["key"],
            "card_index": c["card_index"],
            "deck_file": c["deck_file"],
            "is_refuerzo_tematico": c["is_refuerzo_tematico"],
            "source_q": c["source_q"],
            "question": c["question"],
            "options": c["options"],
            "correct_index": c["correct_index"],
            "correct_text": c["correct_text"],
            "answer_html": c["answer_html"],
            "source_block": c["source_block"],
        } for c in batch]
        (outdir / f"batch_{bn:02d}.json").write_text(
            json.dumps(slim, ensure_ascii=False, indent=2), encoding="utf-8")
        n_batches += 1
    print(f">> {len(cards)} cartas -> {n_batches} lotes de <= {BATCH_SIZE} en {outdir.relative_to(BASE)}", flush=True)

if __name__ == "__main__":
    main()
