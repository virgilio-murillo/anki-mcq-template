#!/usr/bin/env python3
"""Consolida la auditoria: extrae las preguntas RESCATADAS (falsos-COVERED) con su
contenido completo, para generar cartas y AGREGARLAS al mazo (v3).

Una pregunta se rescata si CUALQUIER juez (A objetivo o B profundidad) dijo RESCATAR.
Salida: rescued_examN.json (mismo formato que new_to_generate_v2, + tipo_rescate, razon_rescate)
"""
import json
import pathlib

DIR = pathlib.Path(__file__).resolve().parent
TAGS = ["exam1", "exam2", "exam3"]


def main():
    grand = 0
    for t in TAGS:
        parsed = {q["n"]: q for q in json.loads((DIR / f"parsed_{t}.json").read_text(encoding="utf-8"))}
        # recolectar decisiones por n
        resc = {}
        for line in (DIR / f"audit_verdicts_{t}.jsonl").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            if o["decision"] == "RESCATAR":
                r = resc.setdefault(o["n"], {"tipos": [], "razones": [], "faltante": []})
                r["tipos"].append(o.get("tipo"))
                r["razones"].append(o.get("razon", ""))
                if o.get("feature_o_parametro_faltante"):
                    r["faltante"].append(o["feature_o_parametro_faltante"])
        out = []
        for n in sorted(resc):
            q = parsed[n]
            out.append({**q,
                        "tipo_rescate": "".join(sorted(set(resc[n]["tipos"]))),
                        "razon_rescate": " | ".join(resc[n]["razones"])[:300],
                        "feature_faltante": "; ".join(sorted(set(resc[n]["faltante"])))[:200]})
        (DIR / f"rescued_{t}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        grand += len(out)
        print(f">> {t}: {len(out)} rescatadas", flush=True)
    print(f">> TOTAL rescatadas a generar: {grand}", flush=True)


if __name__ == "__main__":
    main()
