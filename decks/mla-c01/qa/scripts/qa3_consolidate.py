#!/usr/bin/env python3
"""Consolida la doble revision rigurosa (qa3_reviews/A y B).

Regla conservadora: una carta es FIX si CUALQUIERA de los dos revisores la marca FIX,
o si registra options_only_adivinable=true o distractor_tambien_correcto=true.
Une los defectos de ambos. Prioriza P0/P1/P2.
Salida: kiro-test/qa3_report.json, kiro-test/qa3_report.md, kiro-test/qa3_fixlist.json
"""
import json
import pathlib
import glob

BASE = pathlib.Path(__file__).resolve().parents[1]
KT = BASE / "kiro-test"

P0_DIMS = {"correccion_tecnica", "fidelidad_fuente", "alucinaciones"}


def load_track(letter):
    revs = {}
    for f in sorted(glob.glob(str(KT / "qa3_reviews" / letter / "*.jsonl"))):
        for line in pathlib.Path(f).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            revs[r["key"]] = r
    return revs


def worst_sev(*sevs):
    order = {"none": 0, "low": 1, "med": 2, "high": 3}
    return max(sevs, key=lambda s: order.get(s, 0))


def prio_of(merged):
    if merged["distractor_tambien_correcto"]:
        return "P0"
    for d, info in merged["dimensiones"].items():
        if info["sev"] == "high":
            return "P0" if d in P0_DIMS else "P1"
    if merged["options_only_adivinable"]:
        return "P1"
    for d, info in merged["dimensiones"].items():
        if info["sev"] == "med":
            return "P1"
    if any(info["sev"] == "low" for info in merged["dimensiones"].values()) or merged["defectos"]:
        return "P2"
    return "OK"


def main():
    A = load_track("A")
    B = load_track("B")
    all_keys = sorted(set(A) | set(B))
    expected = {c["key"] for c in json.loads((KT / "qa_cards.json").read_text(encoding="utf-8"))}

    merged_all = {}
    buckets = {"P0": [], "P1": [], "P2": [], "OK": []}
    disagreements = []
    for k in all_keys:
        a = A.get(k)
        b = B.get(k)
        dims = {}
        alldims = ["correccion_tecnica", "fidelidad_fuente", "coherencia_interna",
                   "calidad_distractores", "alucinaciones", "conversion_multi_respuesta",
                   "refutaciones_sustantivas", "didactica"]
        for d in alldims:
            sa = (a or {}).get("dimensiones", {}).get(d, {}).get("sev", "none")
            sb = (b or {}).get("dimensiones", {}).get(d, {}).get("sev", "none")
            na = (a or {}).get("dimensiones", {}).get(d, {}).get("nota", "")
            nb = (b or {}).get("dimensiones", {}).get(d, {}).get("nota", "")
            dims[d] = {"sev": worst_sev(sa, sb), "nota_A": na, "nota_B": nb}
        defectos = []
        for src, rv in (("A", a), ("B", b)):
            for df in (rv or {}).get("defectos", []) or []:
                if not isinstance(df, dict):
                    df = {"dimension": "?", "sev": "med", "descripcion": str(df)}
                else:
                    df = dict(df)
                df["por"] = src
                defectos.append(df)
        merged = {
            "key": k,
            "veredicto_A": (a or {}).get("veredicto"),
            "veredicto_B": (b or {}).get("veredicto"),
            "score_A": (a or {}).get("score_global"),
            "score_B": (b or {}).get("score_global"),
            "options_only_adivinable": bool((a or {}).get("options_only_adivinable")) or bool((b or {}).get("options_only_adivinable")),
            "distractor_tambien_correcto": bool((a or {}).get("distractor_tambien_correcto")) or bool((b or {}).get("distractor_tambien_correcto")),
            "respuesta_deberia_ser": (a or {}).get("respuesta_deberia_ser") or (b or {}).get("respuesta_deberia_ser"),
            "dimensiones": dims,
            "defectos": defectos,
        }
        merged["prio"] = prio_of(merged)
        merged_all[k] = merged
        buckets[merged["prio"]].append(merged)
        if (a and b) and (a.get("veredicto") != b.get("veredicto")):
            disagreements.append(k)

    fixlist = [m for m in merged_all.values() if m["prio"] in ("P0", "P1", "P2")]
    (KT / "qa3_fixlist.json").write_text(json.dumps(fixlist, ensure_ascii=False, indent=2), encoding="utf-8")
    (KT / "qa3_report.json").write_text(json.dumps({
        "revisadas_A": len(A), "revisadas_B": len(B), "esperadas": len(expected),
        "faltan_A": sorted(expected - set(A)), "faltan_B": sorted(expected - set(B)),
        "conteo": {k: len(v) for k, v in buckets.items()},
        "desacuerdos_A_vs_B": disagreements,
        "merged": merged_all,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# QA2 report MLA-C01 (doble revision rigurosa con verificacion docs AWS)\n"]
    lines.append(f"- Revisadas A: {len(A)}/{len(expected)}  |  B: {len(B)}/{len(expected)}")
    lines.append(f"- Desacuerdos A vs B: {len(disagreements)} ({', '.join(disagreements) or 'ninguno'})")
    lines.append(f"- P0={len(buckets['P0'])} P1={len(buckets['P1'])} P2={len(buckets['P2'])} OK={len(buckets['OK'])}")
    lines.append(f"- TOTAL a corregir (P0+P1+P2): {len(fixlist)}\n")
    for pr in ("P0", "P1", "P2"):
        if not buckets[pr]:
            continue
        lines.append(f"\n## {pr} ({len(buckets[pr])})\n")
        for m in sorted(buckets[pr], key=lambda x: x["key"]):
            flags = []
            if m["distractor_tambien_correcto"]:
                flags.append("DISTRACTOR-TAMBIEN-CORRECTO")
            if m["options_only_adivinable"]:
                flags.append("OPTIONS-ONLY-ADIVINABLE")
            fl = (" [" + ", ".join(flags) + "]") if flags else ""
            lines.append(f"### {m['key']}  (A={m['veredicto_A']}/{m['score_A']} B={m['veredicto_B']}/{m['score_B']}){fl}")
            if m["respuesta_deberia_ser"]:
                lines.append(f"- respuesta_deberia_ser: {m['respuesta_deberia_ser']}")
            for d in m["defectos"]:
                lines.append(f"- [{d.get('sev')}/{d.get('por')}] {d.get('dimension')}: {d.get('descripcion')}")
                if d.get("fix_sugerido"):
                    lines.append(f"    fix: {d.get('fix_sugerido')}")
            lines.append("")
    (KT / "qa3_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f">> A={len(A)} B={len(B)} esperadas={len(expected)}", flush=True)
    print(f">> P0={len(buckets['P0'])} P1={len(buckets['P1'])} P2={len(buckets['P2'])} OK={len(buckets['OK'])}  a_corregir={len(fixlist)}", flush=True)
    print(f">> desacuerdos A/B: {len(disagreements)}", flush=True)
    if expected - set(A):
        print(f">> FALTAN en A: {sorted(expected - set(A))}", flush=True)
    if expected - set(B):
        print(f">> FALTAN en B: {sorted(expected - set(B))}", flush=True)


if __name__ == "__main__":
    main()
