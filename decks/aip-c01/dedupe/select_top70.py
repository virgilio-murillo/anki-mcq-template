#!/usr/bin/env python3
"""Selecciona las MEJORES 70 cartas del inventario (161) maximizando valor
examinable AIP-C01 + COBERTURA de temas + diversidad conceptual.

Metodo:
- Cuotas por dominio proporcionales al peso oficial del examen (31/26/20/12/11)
  sobre 70 -> asi las 70 abarcan el temario en la proporcion en que se examina.
- Score por carta: valor de dominio + senal de novedad/profundidad + centralidad
  GenAI (terminos in-scope del temario) - penalizacion por concepto repetido.
- Seleccion greedy por dominio: dentro de cada cuota, toma las de mayor score
  evitando duplicar concepto (MMR-like: baja el score si el concepto ya entro).

Salida: top70.json (las elegidas) y overflow.json (el resto), con key y motivo.
"""
import json
import pathlib
import re
from collections import defaultdict

DIR = pathlib.Path(__file__).resolve().parent
inv = json.loads((DIR / "inventory.json").read_text(encoding="utf-8"))
sig = {}
for l in (DIR / "audit_signals.jsonl").read_text(encoding="utf-8").splitlines():
    if l.strip():
        o = json.loads(l)
        sig[(o["exam"], o["n"])] = o

# peso oficial por dominio (nombre corto -> peso)
DOMAIN_W = {
    "Foundation Model Integration": 31,
    "Implementation and Integration": 26,
    "AI Safety, Security, and Governance": 20,
    "Operational Efficiency": 12,
    "Testing, Validation": 11,
}


def domain_of(cat):
    for k in DOMAIN_W:
        if k.split(",")[0].lower() in cat.lower() or k.lower() in cat.lower():
            return k
    if "foundation model" in cat.lower():
        return "Foundation Model Integration"
    if "operational" in cat.lower():
        return "Operational Efficiency"
    if "implementation" in cat.lower():
        return "Implementation and Integration"
    if "safety" in cat.lower():
        return "AI Safety, Security, and Governance"
    if "testing" in cat.lower():
        return "Testing, Validation"
    return "Foundation Model Integration"


# terminos centrales GenAI (del blueprint) que suben el valor examinable
CENTRAL = ["bedrock", "guardrail", "rag", "retrieval", "agent", "knowledge base", "foundation model",
           "prompt", "embedding", "vector", "llm", "fine-tun", "provisioned throughput",
           "cross-region", "reranker", "chunk", "hallucin", "token", "inference", "titan",
           "amazon q", "model evaluation", "distillation", "caching", "mcp", "guardrails",
           "structured output", "temperature", "streaming", "quantiz", "lora"]


def score(card):
    dom = domain_of(card["category"])
    s = DOMAIN_W[dom] * 1.0                      # valor de dominio
    text = (card["stem"] + " " + card.get("concepto", "")).lower()
    s += 6 * sum(1 for t in CENTRAL if t in text) ** 0.5   # centralidad GenAI (raiz: no premiar amontonar)
    k = (card["exam"], card["n"])
    g = sig.get(k, {})
    if card["kind"] == "RESC":
        # fuerza de la evidencia de rescate
        cos = g.get("recomputed_top_cos", 0.6)
        if cos < 0.50:
            s += 14          # objetivo claramente no cubierto = alto valor nuevo
        elif cos < 0.60:
            s += 8
        else:
            s += 2           # rescate debil = menor prioridad
        if g.get("missing_depth_terms"):
            s += 6           # feature avanzada ausente = valioso para examen pro
        if g.get("depth_gap", 0) >= 40:
            s += 4
    else:
        s += 5               # NEW genuina (no estaba en el universo)
    return s, dom


def concept_key(card):
    """clave de concepto para deduplicar seleccion (servicio + verbo aproximado)."""
    t = (card.get("concepto") or card["stem"]).lower()
    toks = re.findall(r"[a-z][a-z\-]{3,}", t)
    stop = {"para", "amazon", "aws", "with", "using", "sagemaker", "model", "data", "company",
            "which", "para", "that", "este", "para", "genai", "generative"}
    key = tuple(sorted(set(w for w in toks if w not in stop))[:4])
    return key


# cuotas por dominio (proporcional al peso, suma 70)
total = 70
present_doms = defaultdict(list)
for c in inv:
    sc, dom = score(c)
    c["_score"] = sc
    c["_dom"] = dom
    present_doms[dom].append(c)
wsum = sum(DOMAIN_W[d] for d in present_doms)
quota = {d: max(1, round(total * DOMAIN_W[d] / wsum)) for d in present_doms}
# ajustar a exactamente 70
while sum(quota.values()) > total:
    d = max(quota, key=lambda x: quota[x]); quota[d] -= 1
while sum(quota.values()) < total:
    d = max(present_doms, key=lambda x: len(present_doms[x]) - quota[x]); quota[d] += 1

chosen, overflow = [], []
for dom, cards in present_doms.items():
    cards = sorted(cards, key=lambda c: -c["_score"])
    seen_concepts = set()
    picked = 0
    q = min(quota[dom], len(cards))
    # primera pasada: diversidad de concepto
    for c in cards:
        if picked >= q:
            break
        ck = concept_key(c)
        if ck in seen_concepts:
            continue
        seen_concepts.add(ck)
        chosen.append(c); picked += 1
    # completar cuota si faltó (conceptos repetidos permitidos al final)
    for c in cards:
        if picked >= q:
            break
        if c not in chosen:
            chosen.append(c); picked += 1
    for c in cards:
        if c not in chosen:
            overflow.append(c)

# si por diversidad quedaron <70, rellenar del overflow por score global
if len(chosen) < total:
    for c in sorted(overflow, key=lambda c: -c["_score"]):
        if len(chosen) >= total:
            break
        chosen.append(c); overflow.remove(c)

json.dump([{k: c[k] for k in ("exam", "n", "kind", "key", "category", "concepto", "_score", "_dom")} for c in chosen],
          open(DIR / "top70.json", "w"), ensure_ascii=False, indent=2)
json.dump([{k: c[k] for k in ("exam", "n", "kind", "key", "category", "_dom")} for c in overflow],
          open(DIR / "overflow.json", "w"), ensure_ascii=False, indent=2)

from collections import Counter
print(f"Elegidas: {len(chosen)}  | overflow: {len(overflow)}")
print("Cuotas por dominio:", {d.split(',')[0][:20]: quota[d] for d in quota})
print("Elegidas por dominio:", dict(Counter(c["_dom"].split(',')[0][:20] for c in chosen)))
print("Elegidas por tipo:", dict(Counter(c["kind"] for c in chosen)))
