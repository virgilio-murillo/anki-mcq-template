#!/usr/bin/env python3
"""Genera lotes BLIND (candidato en frio) para la validacion de claridad.

Cada carta se presenta con SOLO: key, question, options (etiquetadas A-D en orden fijo).
NO se incluye correct_index, correct_text, answer_html ni source_block: el candidato
debe elegir a ciegas basandose solo en enunciado + opciones. Guardamos aparte el
mapeo key->correct_letter para comparar despues.

Salida:
  kiro-test/clarity/blind_batches/batch_NN.json  (lotes para candidatos)
  kiro-test/clarity/answer_key.json              (key -> letra correcta, SOLO para el consolidador)
"""
import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"
OUT = KT / "clarity"
BATCH = 8
LETTERS = ["A", "B", "C", "D"]


def main():
    cards = json.loads((KT / "qa_cards_paired.json").read_text(encoding="utf-8"))
    (OUT / "blind_batches").mkdir(parents=True, exist_ok=True)
    answer_key = {}
    blind = []
    for c in cards:
        # Presentamos las opciones en su ORDEN de autoria (indice 0..3 -> A..D).
        opts = c["options"]
        ci = c["correct_index"]
        answer_key[c["key"]] = {
            "correct_letter": LETTERS[ci],
            "correct_text": c["correct_text"],
            "is_refuerzo": c["is_refuerzo_tematico"],
        }
        blind.append({
            "key": c["key"],
            "question": c["question"],
            "options": {LETTERS[i]: opts[i] for i in range(4)},
        })
    n = 0
    for i in range(0, len(blind), BATCH):
        n += 1
        (OUT / "blind_batches" / f"batch_{n:02d}.json").write_text(
            json.dumps(blind[i:i + BATCH], ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "answer_key.json").write_text(json.dumps(answer_key, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> {len(blind)} cartas ciegas -> {n} lotes de {BATCH} en clarity/blind_batches", flush=True)
    print(f">> answer_key.json con {len(answer_key)} entradas (uso interno del consolidador)", flush=True)


if __name__ == "__main__":
    main()
