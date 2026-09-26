#!/usr/bin/env python3
"""Arma los insumos de los jueces de auditoria (A=objetivo, B=profundidad) desde
audit_signals.jsonl. Bloques autocontenidos con TEXTO COMPLETO de las cartas.

Todas las 72 COVERED van al juez A (objetivo). Las de depth_gap>=40 van tambien al
juez B (profundidad). Salida un archivo por examen para cada juez.
"""
import json
import pathlib

DIR = pathlib.Path(__file__).resolve().parent
sig = [json.loads(l) for l in (DIR / "audit_signals.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def block(o, kind):
    L = []
    L.append(f"### Q{o['n']} [{o['category']}]  (cos_recomputado={o['recomputed_top_cos']}, depth_gap={o['depth_gap']})")
    L.append(f"NUEVA (AIP profesional): {o['stem']}")
    L.append(f"RESPUESTA CORRECTA (AIP): {o['correct_text']}")
    if kind == "A":
        L.append(f"Servicios/features en la respuesta AIP AUSENTES en las cartas: {o['missing_services'] or 'ninguno detectado'}")
    else:
        L.append(f"Features/parametros AIP-especificos: {o['aip_depth_terms'] or 'ninguno'}")
        L.append(f"De esos, AUSENTES en todas las cartas: {o['missing_depth_terms'] or 'ninguno'}")
        L.append(f"Bloom AIP={o['bloom_aip']} vs Bloom carta={o['bloom_card']}; len_carta={o['len_card']}")
    L.append("Cartas-cubridoras (TEXTO COMPLETO de lo que YA estudiaste; cos=similitud 0-1):")
    for c in o["candidates"]:
        L.append(f"  - [cos={c['cos']}] {c['full_text']}")
    L.append("")
    return "\n".join(L)


for tag in ("exam1", "exam2", "exam3"):
    rows = [o for o in sig if o["exam"] == tag]
    a = [block(o, "A") for o in rows]
    b = [block(o, "B") for o in rows if o["depth_gap"] >= 40]
    (DIR / f"audit_A_{tag}.txt").write_text("\n".join(a), encoding="utf-8")
    (DIR / f"audit_B_{tag}.txt").write_text("\n".join(b), encoding="utf-8")
    print(f">> {tag}: A={len(a)} bloques, B={len([o for o in rows if o['depth_gap']>=40])} bloques")
