#!/usr/bin/env python3
"""Parte el material fuente MLA-C01 en preguntas y las reparte en 2 decks por dominio.

Salida:
  deck01_source.txt  -> Data Preparation + parte de Model Development (~42 preguntas)
  deck02_source.txt  -> resto Model Development + Deployment + Monitoring/Security (~42)
  split_manifest.md  -> resumen del reparto
"""
import re

SRC = [
    "../notes/source/mla_exam_part_1.txt",
    "../notes/source/mla_exam_part_2.txt",
]

def parse(path):
    """Devuelve lista de (category, raw_text) por pregunta."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    parts = re.split(r'(?m)^(\d+)\.\s+Question\s*$', text)
    out = []
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        mcat = re.search(r'(?m)^Category:\s*(.+?)\s*$', body)
        cat = mcat.group(1).strip() if mcat else "UNKNOWN"
        out.append((cat, body.strip()))
    return out

def main():
    print("Parseando fuentes...", flush=True)
    questions = []
    for p in SRC:
        qs = parse(p)
        print(f"  {p}: {len(qs)} preguntas", flush=True)
        questions.extend(qs)
    print(f"TOTAL: {len(questions)} preguntas", flush=True)

    def dom(cat):
        c = cat.lower()
        if "data preparation" in c:
            return "dataprep"
        if "model development" in c:
            return "modeldev"
        if "deployment" in c or "orchestration" in c:
            return "deploy"
        if "monitoring" in c or "maintenance" in c or "security" in c:
            return "monitor"
        return "other"

    buckets = {}
    for cat, body in questions:
        buckets.setdefault(dom(cat), []).append((cat, body))

    for k, v in sorted(buckets.items()):
        print(f"  dominio {k}: {len(v)}", flush=True)

    dataprep = buckets.get("dataprep", [])
    modeldev = buckets.get("modeldev", [])
    deploy = buckets.get("deploy", [])
    monitor = buckets.get("monitor", [])

    md_to_deck1 = modeldev[:4]
    md_to_deck2 = modeldev[4:]
    deck1 = dataprep + md_to_deck1
    deck2 = md_to_deck2 + deploy + monitor

    print(f"\nDeck 01: {len(deck1)} preguntas  (dataprep {len(dataprep)} + modeldev {len(md_to_deck1)})", flush=True)
    print(f"Deck 02: {len(deck2)} preguntas  (modeldev {len(md_to_deck2)} + deploy {len(deploy)} + monitor {len(monitor)})", flush=True)

    def dump(fname, items, title):
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(f"# {title}\n# {len(items)} preguntas\n\n")
            for n, (cat, body) in enumerate(items, 1):
                fh.write(f"===== PREGUNTA {n} =====\n")
                fh.write(f"Category: {cat}\n")
                fh.write(body)
                fh.write("\n\n")
        print(f"escrito {fname} ({len(items)} preguntas)", flush=True)

    dump("deck01_source.txt", deck1, "MLA-C01 Deck 01 - Data Preparation")
    dump("deck02_source.txt", deck2, "MLA-C01 Deck 02 - Modeling, Deployment & Ops")

    with open("split_manifest.md", "w", encoding="utf-8") as fh:
        fh.write("# Reparto de preguntas MLA-C01\n\n")
        fh.write(f"- Total preguntas: {len(questions)}\n")
        fh.write(f"- Data Preparation: {len(dataprep)}\n")
        fh.write(f"- ML Model Development: {len(modeldev)}\n")
        fh.write(f"- Deployment & Orchestration: {len(deploy)}\n")
        fh.write(f"- Monitoring/Maintenance/Security: {len(monitor)}\n\n")
        fh.write(f"## Deck 01 (MLA-C01::01 - Data Preparation): {len(deck1)} preguntas\n")
        fh.write(f"## Deck 02 (MLA-C01::02 - Modeling, Deployment & Ops): {len(deck2)} preguntas\n")
    print("escrito split_manifest.md", flush=True)
    print("LISTO", flush=True)

if __name__ == "__main__":
    main()
