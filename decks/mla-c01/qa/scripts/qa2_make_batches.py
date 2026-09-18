#!/usr/bin/env python3
"""Re-auditoria rigurosa: lotes de 4 cartas para verificacion profunda con docs AWS.

Escribe kiro-test/qa2_batches/batch_NN.json (28 lotes de 4).
Prepara dirs para doble revisor: qa2_reviews/A/ y qa2_reviews/B/.
"""
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"
BATCH_SIZE = 4

def main():
    cards = json.loads((KT / "qa_cards_paired.json").read_text(encoding="utf-8"))
    outdir = KT / "qa2_batches"
    outdir.mkdir(exist_ok=True)
    (KT / "qa2_reviews" / "A").mkdir(parents=True, exist_ok=True)
    (KT / "qa2_reviews" / "B").mkdir(parents=True, exist_ok=True)
    n = 0
    for i in range(0, len(cards), BATCH_SIZE):
        batch = cards[i:i + BATCH_SIZE]
        bn = i // BATCH_SIZE + 1
        slim = [{
            "key": c["key"],
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
        n += 1
    print(f">> {len(cards)} cartas -> {n} lotes de <= {BATCH_SIZE} en {outdir.relative_to(BASE)}", flush=True)

if __name__ == "__main__":
    main()
