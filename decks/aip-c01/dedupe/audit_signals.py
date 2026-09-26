#!/usr/bin/env python3
"""Auditoria de falsos-COVERED (investigacion 638727cf) — senales deterministas.

Corrige los 2 bugs detectados:
  - top_cos desalineado: RE-RECUPERA cos desde el vecstore VIGENTE (no confia en el guardado).
  - truncado a 400 chars: usa el TEXTO COMPLETO de la carta cubridora.

Por cada pregunta COVERED calcula:
  - candidatos re-recuperados (hibrido RRF) con cos recomputado y TEXTO COMPLETO.
  - missing_services: tokens de servicio/feature de la RESPUESTA CORRECTA AIP ausentes en las cartas.
  - aip_depth_terms / missing_depth_terms: lexico de profundidad presente en la pregunta AIP y ausente en las cartas.
  - depth_gap heuristico (formula del reporte).
Salida: audit_signals.jsonl  (una linea por COVERED)
"""
import json
import pathlib
import re

import numpy as np

DIR = pathlib.Path(__file__).resolve().parent
STORE = DIR / "vecstore"
TAGS = ["exam1", "exam2", "exam3"]
RRF_K = 60
DEPTH = 40
TOPK = 5

# Lexico de profundidad AIP-C01 (consolidado c1+c4 de la investigacion).
DEPTH_TERMS = [
    "provisioned throughput", "cross-region inference", "cross region inference", "lora",
    "adapters", "peft", "reranker", "rerank", "cohere rerank", "hierarchical chunking",
    "hybrid search", "metadata filtering", "query decomposition", "pgvector", "neural plugin",
    "prompt flows", "prompt management", "agentcore", "strands", "agent squad", "mcp", "react",
    "guardrails", "denied topics", "contextual grounding", "pii redaction", "structured output",
    "json schema", "logprobs", "tool calling", "function calling", "model evaluation",
    "llm-as-a-judge", "llm as a judge", "answer accuracy", "completeness", "expression quality",
    "bedrock agent evaluations", "semantic caching", "prompt caching", "model distillation",
    "temperature", "top-k", "top_k", "top-p", "top_p", "model registry", "model cards",
    "titan embeddings", "model invocation logs", "embedding drift", "latency-optimized",
    "smote", "hyperband", "transfer_learning", "warm start", "warm-start", "max_depth",
    "detectpiientities", "retrieveandgenerate", "performanceconfiglatency",
    "modelexplainabilitymonitor", "knowledge base", "knowledge bases", "step functions",
    "productionvariant", "variant weight", "shadow", "a/b", "inference component",
    "scheduled scaling", "async", "asynchronous", "batch inference", "trainium", "trn",
    "inferentia", "chunking", "embeddings", "vector", "fine-tune", "fine tune", "fine-tuning",
]

# tokens de servicio/feature: CamelCase, ns:accion, nombres propios, acronimos
_SALIENT = re.compile(
    r"[A-Z][a-z]{2,}[A-Z][A-Za-z]+|[a-z]+:[a-zA-Z]+|[A-Z][a-zA-Z]{3,}|[A-Z]{2,}")
_GENERIC = {"Amazon", "AWS", "The", "This", "With", "Using", "Use", "For", "And", "You",
            "When", "Which", "That", "From", "Into", "SageMaker", "API", "ML", "AI"}

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where will would can could should must may might not company team wants needs approach solution option options data model models using use used el la los las de un una para que con por".split())


def bm25_tokens(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def salient(text):
    plain = re.sub(r"<[^>]+>", " ", text or "")
    return {t for t in _SALIENT.findall(plain) if t not in _GENERIC}


def depth_terms_in(text):
    low = (text or "").lower()
    return {t for t in DEPTH_TERMS if t in low}


def rrf_fuse(sem_order, bm_order, k=RRF_K):
    score = {}
    for rank, idx in enumerate(sem_order, 1):
        score.setdefault(idx, 0.0)
        score[idx] += 1.0 / (k + rank)
    for rank, idx in enumerate(bm_order, 1):
        score.setdefault(idx, 0.0)
        score[idx] += 1.0 / (k + rank)
    return score


def bloom_level(text):
    """Heuristica de Bloom: alto si hay verbos de diseno/optimizacion/troubleshoot."""
    low = (text or "").lower()
    high = any(w in low for w in ("design", "optimi", "troubleshoot", "integrat", "evaluat",
                                  "disen", "optimiz", "resolver", "arquitect", "configure",
                                  "implement", "reduce latency", "cost-effective", "least"))
    lowb = any(w in low for w in ("what is", "which service", "define", "que es", "cual servicio",
                                  "identify", "describe"))
    return "alto" if high else ("bajo" if lowb else "medio")


def main():
    U_emb = np.load(STORE / "universe_emb.npy")
    U_meta = json.loads((STORE / "universe_meta.json").read_text(encoding="utf-8"))
    U_tokens = json.loads((STORE / "bm25_tokens.json").read_text(encoding="utf-8"))
    model_name = (STORE / "model.txt").read_text(encoding="utf-8").strip()
    corpus_texts = [m["concept_text"] for m in U_meta]

    from sentence_transformers import SentenceTransformer
    from rank_bm25 import BM25Okapi
    model = SentenceTransformer(model_name)
    bm25 = BM25Okapi(U_tokens)

    out = []
    for tag in TAGS:
        parsed = {q["n"]: q for q in json.loads((DIR / f"parsed_{tag}.json").read_text(encoding="utf-8"))}
        covered = [json.loads(l)["n"] for l in (DIR / f"verdicts_hybrid_{tag}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip() and json.loads(l)["verdict"] == "COVERED"]
        qtexts = [f"{parsed[n]['stem']} || RESPUESTA: {parsed[n]['options'][parsed[n]['correct_index']]['text']}" for n in covered]
        Q_emb = model.encode(qtexts, convert_to_numpy=True, normalize_embeddings=True).astype("float32")
        for n, qv, qtxt in zip(covered, Q_emb, qtexts):
            q = parsed[n]
            correct = q["options"][q["correct_index"]]["text"]
            cos = U_emb @ qv
            sem_order = [int(i) for i in np.argsort(-cos)[:DEPTH]]
            bm_order = [int(i) for i in np.argsort(-bm25.get_scores(bm25_tokens(qtxt)))[:DEPTH]]
            fused = rrf_fuse(sem_order, bm_order)
            top = sorted(fused.items(), key=lambda kv: kv[1], reverse=True)[:TOPK]
            cands = [{"cos": round(float(cos[i]), 3), "full_text": corpus_texts[i]} for i, _ in top]
            cards_blob = " ".join(c["full_text"].lower() for c in cands)

            # senales
            ans_serv = salient(correct)
            missing_services = sorted(s for s in ans_serv if s.lower() not in cards_blob)
            aip_depth = depth_terms_in(q["stem"] + " " + correct)
            missing_depth = sorted(t for t in aip_depth if t not in cards_blob)
            top_cos = cands[0]["cos"] if cands else 0.0
            bloom_aip = bloom_level(q["stem"] + " " + correct)
            bloom_card = bloom_level(cands[0]["full_text"] if cands else "")
            len_card = len(cands[0]["full_text"]) if cands else 0
            depth_gap = (40 * (1 if missing_depth else 0)
                         + 20 * (1 if (bloom_aip == "alto" and bloom_card in ("bajo", "medio")) else 0)
                         + 15 * (1 if any(p in " ".join(missing_depth) for p in ("temperature", "top-k", "top_k", "top-p", "top_p", "chunk")) else 0)
                         + 15 * (1 if (top_cos > 0.60 and missing_services) else 0)
                         + 10 * (1 if len_card < 220 else 0))
            out.append({
                "n": n, "exam": tag, "category": q.get("category", ""),
                "stem": q["stem"], "correct_text": correct,
                "recomputed_top_cos": top_cos,
                "missing_services": missing_services[:8],
                "aip_depth_terms": sorted(aip_depth)[:12],
                "missing_depth_terms": missing_depth[:12],
                "bloom_aip": bloom_aip, "bloom_card": bloom_card, "len_card": len_card,
                "depth_gap": depth_gap,
                "candidates": cands,
            })

    (DIR / "audit_signals.jsonl").write_text(
        "\n".join(json.dumps(o, ensure_ascii=False) for o in out), encoding="utf-8")
    # diagnostico
    n_gap = sum(1 for o in out if o["depth_gap"] >= 40)
    n_missserv = sum(1 for o in out if o["missing_services"])
    lo = sum(1 for o in out if o["recomputed_top_cos"] < 0.55)
    print(f">> {len(out)} COVERED con senales. depth_gap>=40: {n_gap}. "
          f"con missing_services: {n_missserv}. recomputed_cos<0.55: {lo}", flush=True)


if __name__ == "__main__":
    main()
