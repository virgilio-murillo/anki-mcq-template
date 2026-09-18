#!/usr/bin/env python3
"""Prepara la deduplicacion: extrae un texto-concepto por cada pregunta nueva
(las 57 estandar) y por cada carta existente (las 332), para el matching semantico.

No 'destila' con LLM aqui (eso lo hace el juez despues); simplemente normaliza a
texto plano enunciado+opcion-correcta (nueva) / enunciado+opciones (existente),
que es suficiente para el retrieval por embeddings.

Salidas:
  dedupe/new_concepts.json       -> [{n, concept_text, stem, correct_text}]
  dedupe/existing_concepts.json  -> [{id, concept_text}]
"""
import json
import re
import pathlib

DIR = pathlib.Path(__file__).resolve().parent


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"&[a-z]+;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    new = json.loads((DIR / "new_exam_parsed.json").read_text(encoding="utf-8"))
    existing = json.loads((DIR / "existing_cards.json").read_text(encoding="utf-8"))

    new_out = []
    for q in new:
        correct = next(o for o in q["options"] if o["letter"] == q["correct_letter"])
        # concepto = enunciado + la opcion correcta (el par pregunta-respuesta define el tema)
        concept = f"{clean(q['stem'])} || RESPUESTA: {clean(correct['text'])}"
        new_out.append({"n": q["n"], "concept_text": concept,
                        "stem": clean(q["stem"]), "correct_text": clean(correct["text"])})

    ex_out = []
    for i, c in enumerate(existing):
        concept = f"{c['question']} {c.get('options','')}".strip()
        ex_out.append({"id": c["note_id"], "query": c.get("query", ""), "concept_text": clean(concept)})

    (DIR / "new_concepts.json").write_text(json.dumps(new_out, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIR / "existing_concepts.json").write_text(json.dumps(ex_out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f">> {len(new_out)} conceptos nuevos, {len(ex_out)} conceptos existentes", flush=True)


if __name__ == "__main__":
    main()
