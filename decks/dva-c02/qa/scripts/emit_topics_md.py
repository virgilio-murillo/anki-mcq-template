#!/usr/bin/env python3
"""Write the final human-readable topic<->question<->status map to
notes/source/exam_topics.md, enriched with dedup verdict (COVERED/NEW),
consolidation, and which deck-09 card each NEW topic ended up in."""
import json, collections

topics = json.load(open("kiro-test/exam_topics.json", encoding="utf-8"))
dedup = {r["id"]: r for r in json.load(open("kiro-test/dedup_results.json", encoding="utf-8"))}
canon = json.load(open("kiro-test/consolidated_new.json", encoding="utf-8"))
gen = json.load(open("kiro-test/generated_cards.json", encoding="utf-8"))

# map source topic id -> canonical topic (and its generated card key)
# canon entries have source_ids (topic ids). gen cards were built in canon order;
# match by topic string + service to the generated card.
canon_by_topic = {(c["topic"], c["service"]): c for c in canon}
gencard_by_topic = {(g["topic"], g["service"]): g for g in gen}
srcid_to_card = {}
for c in canon:
    gc = gencard_by_topic.get((c["topic"], c["service"]))
    key = gc["key"] if gc else "(pending)"
    for sid in c["source_ids"]:
        srcid_to_card[sid] = {"canon_topic": c["topic"], "card_key": key,
                              "questions": c["questions"]}

by_q = collections.defaultdict(list)
for t in topics:
    by_q[t["question"]].append(t)

covered = sum(1 for t in topics if dedup[t["id"]]["covered"])
new = len(topics) - covered

with open("notes/source/exam_topics.md", "w", encoding="utf-8") as f:
    f.write("# DVA-C02 examen_practica.txt - Temas, trazabilidad y estado\n\n")
    f.write("Pipeline: parse 65 preguntas -> extraccion de temas (Bedrock Claude Sonnet 4.5) -> ")
    f.write("dedup en 2 capas (embeddings Titan v2 + juicio Claude) contra las 188 tarjetas ")
    f.write("existentes de DVA-C02::* -> consolidacion de temas NEW entre si -> generacion de ")
    f.write("tarjetas para el deck DVA-C02::09.\n\n")
    f.write(f"- Temas extraidos: {len(topics)}\n")
    f.write(f"- YA ESTUDIADOS (COVERED): {covered}\n")
    f.write(f"- NUEVOS (NEW): {new}\n")
    f.write(f"- Tarjetas creadas en DVA-C02::09 (tras consolidar): {len(gen)}\n\n")
    f.write("Leyenda: cada tema muestra [id] nombre (servicio), su estado, y para los NEW la ")
    f.write("tarjeta del deck 09 (card_key) donde quedo.\n\n")
    for q in sorted(by_q):
        f.write(f"## Pregunta {q}\n")
        for t in by_q[q]:
            d = dedup[t["id"]]
            status = "YA ESTUDIADO" if d["covered"] else "NUEVO"
            f.write(f"- **[{t['id']}] {t['topic']}** ({t['service']}) - _{status}_ ")
            f.write(f"(cos={d['max_cosine']}, LLM={d['llm_verdict']})\n")
            f.write(f"  - {t['concept']}\n")
            if d["covered"]:
                f.write(f"  - Motivo: {d['llm_reason']}\n")
            else:
                sc = srcid_to_card.get(t["id"])
                if sc:
                    f.write(f"  - -> tarjeta deck09: `{sc['card_key']}` (tema canonico: {sc['canon_topic']})\n")
        f.write("\n")

print("wrote notes/source/exam_topics.md")
