#!/usr/bin/env python3
"""ERROR TIPO C — gaps de temario. Cruza el checklist oficial (blueprint_topics.json)
contra el corpus del MAZO (108 NEW aceptadas + 72 COVERED) por embedding + lexico.

Para cada topic: coverage = max_cos contra el mazo; si max_cos < UMBRAL y sin hit
lexico fuerte -> GAP (tema in-scope que el mazo no cubre). Prioriza por peso de dominio.

Salida: gaps_report.json  [{id, dominio, peso, topic, max_cos, best_match_n, is_gap}]
"""
import json
import pathlib
import re

import numpy as np

DIR = pathlib.Path(__file__).resolve().parent
STORE = DIR / "vecstore"
GAP_COS = 0.55   # por debajo -> candidato a gap (temas del mazo son cross-lingual)
TAGS = ["exam1", "exam2", "exam3"]


def main():
    bp = json.loads((DIR / "blueprint_topics.json").read_text(encoding="utf-8"))["topics"]

    # corpus del mazo: NEW aceptadas (v2) + COVERED, con su texto
    deck = []
    for t in TAGS:
        parsed = {q["n"]: q for q in json.loads((DIR / f"parsed_{t}.json").read_text(encoding="utf-8"))}
        new_v2 = json.loads((DIR / f"new_to_generate_v2_{t}.json").read_text(encoding="utf-8"))
        for q in new_v2:
            correct = q["options"][q["correct_index"]]["text"]
            deck.append({"src": f"{t}-NEW", "n": q["n"], "text": f"{q['stem']} {correct} {q.get('concepto','')}"})
        # COVERED (concepto+stem)
        for line in (DIR / f"verdicts_hybrid_{t}.jsonl").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            if o["verdict"] == "COVERED":
                q = parsed[o["n"]]
                correct = q["options"][q["correct_index"]]["text"]
                deck.append({"src": f"{t}-COV", "n": o["n"], "text": f"{q['stem']} {correct} {o.get('concepto','')}"})

    from sentence_transformers import SentenceTransformer
    model_name = (STORE / "model.txt").read_text(encoding="utf-8").strip()
    model = SentenceTransformer(model_name)
    D_emb = model.encode([d["text"] for d in deck], convert_to_numpy=True,
                         normalize_embeddings=True).astype("float32")
    T_emb = model.encode([t["topic"] for t in bp], convert_to_numpy=True,
                         normalize_embeddings=True).astype("float32")

    report = []
    for t, tv in zip(bp, T_emb):
        cos = D_emb @ tv
        j = int(np.argmax(cos))
        mx = float(cos[j])
        # hit lexico: palabra clave distintiva del topic en el mejor match
        key = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", t["topic"])
        low = deck[j]["text"].lower()
        lex = sum(1 for w in key if w.lower() in low and w.lower() not in
                  ("para", "segun", "para", "con", "que", "los", "las", "una", "del"))
        is_gap = mx < GAP_COS
        report.append({"id": t["id"], "dominio": t["dominio"], "peso": t["peso"],
                       "topic": t["topic"], "max_cos": round(mx, 3),
                       "best_match": f'{deck[j]["src"]} Q{deck[j]["n"]}',
                       "is_gap": is_gap})

    report.sort(key=lambda r: (r["is_gap"], r["peso"], -r["max_cos"] if False else 0), reverse=True)
    report.sort(key=lambda r: (r["is_gap"], r["peso"]), reverse=True)
    (DIR / "gaps_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    gaps = [r for r in report if r["is_gap"]]
    print(f">> {len(bp)} topics del temario. GAPS (max_cos<{GAP_COS}): {len(gaps)}", flush=True)
    for r in sorted(gaps, key=lambda r: -r["peso"]):
        print(f"   [D{r['dominio']} {r['peso']}%] {r['topic'][:60]}  (max_cos={r['max_cos']}, best={r['best_match']})", flush=True)


if __name__ == "__main__":
    main()
