#!/usr/bin/env python3
"""Fase 4: consolida las revisiones LLM (qa_reviews/*.jsonl) en un reporte.

Salida:
  kiro-test/qa_report.json  -> lista unica de revisiones + resumen
  kiro-test/qa_report.md    -> reporte legible priorizado (P0/P1/P2)
Uso:  qa_consolidate.py
"""
import json
import pathlib
import glob

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"

P0_DIMS = {"correccion_tecnica", "fidelidad_fuente", "alucinaciones"}
P1_DIMS = {"calidad_distractores", "conversion_multi_respuesta", "refutaciones_sustantivas", "coherencia_interna"}


def prio(rev):
    """Devuelve la prioridad mas alta (P0>P1>P2) segun defectos."""
    if rev.get("distractor_tambien_correcto"):
        return "P0"
    dims = rev.get("dimensiones", {})
    for d, info in dims.items():
        sev = info.get("sev", "none")
        if sev == "high":
            return "P0" if d in P0_DIMS else "P1"
    # defectos med
    hasmed = any(info.get("sev") == "med" for info in dims.values())
    if hasmed:
        # med en dims P0 -> P1, en otras -> P1/P2
        for d, info in dims.items():
            if info.get("sev") == "med" and d in P0_DIMS:
                return "P1"
        return "P1"
    hasany = rev.get("defectos") or any(info.get("sev") == "low" for info in dims.values())
    return "P2" if hasany else "OK"


def main():
    total_expected = json.loads((KT / "qa_cards.json").read_text(encoding="utf-8"))
    expected_keys = {c["key"] for c in total_expected}

    reviews = {}
    for f in sorted(glob.glob(str(KT / "qa_reviews" / "*.jsonl"))):
        for line in pathlib.Path(f).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"!! JSON invalido en {f}: {e}", flush=True)
                continue
            reviews[r["key"]] = r

    missing = sorted(expected_keys - set(reviews))
    extra = sorted(set(reviews) - expected_keys)

    buckets = {"P0": [], "P1": [], "P2": [], "OK": []}
    for k, r in reviews.items():
        r["_prio"] = prio(r)
        buckets[r["_prio"]].append(r)

    report = {
        "total_esperadas": len(expected_keys),
        "total_revisadas": len(reviews),
        "faltantes": missing,
        "extra": extra,
        "conteo": {k: len(v) for k, v in buckets.items()},
        "reviews": reviews,
    }
    (KT / "qa_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = []
    lines.append("# QA report MLA-C01 (revision LLM carta-por-carta)\n")
    lines.append(f"- Esperadas: {len(expected_keys)}  |  Revisadas: {len(reviews)}")
    if missing:
        lines.append(f"- FALTAN por revisar ({len(missing)}): {', '.join(missing)}")
    if extra:
        lines.append(f"- Keys extra no esperadas: {', '.join(extra)}")
    lines.append(f"- P0 (respuesta incorrecta / distractor tambien-correcto / alucinacion): {len(buckets['P0'])}")
    lines.append(f"- P1 (refutacion/conversion/coherencia/distractor med-high): {len(buckets['P1'])}")
    lines.append(f"- P2 (didactica / cosmetico low): {len(buckets['P2'])}")
    lines.append(f"- OK (impecables): {len(buckets['OK'])}\n")

    for pr in ("P0", "P1", "P2"):
        if not buckets[pr]:
            continue
        lines.append(f"\n## {pr} ({len(buckets[pr])})\n")
        for r in sorted(buckets[pr], key=lambda x: x["key"]):
            lines.append(f"### {r['key']}  (score {r.get('score_global')}, {r.get('veredicto')})")
            if r.get("distractor_tambien_correcto"):
                lines.append(f"- distractor_tambien_correcto=TRUE ; respuesta_deberia_ser: {r.get('respuesta_deberia_ser')}")
            for d in r.get("defectos", []):
                lines.append(f"- [{d.get('sev')}] {d.get('dimension')}: {d.get('descripcion')}")
                if d.get("fix_sugerido"):
                    lines.append(f"    fix: {d.get('fix_sugerido')}")
            lines.append("")
    (KT / "qa_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f">> revisadas {len(reviews)}/{len(expected_keys)}", flush=True)
    print(f">> P0={len(buckets['P0'])} P1={len(buckets['P1'])} P2={len(buckets['P2'])} OK={len(buckets['OK'])}", flush=True)
    if missing:
        print(f">> FALTAN: {missing}", flush=True)
    print(">> escrito qa_report.json y qa_report.md", flush=True)


if __name__ == "__main__":
    main()
