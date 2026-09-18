#!/usr/bin/env python3
"""
PHASE 2 (v4, CALIBRATED) - Concept-vs-concept dedup with FIXED judge.
Fixes from the v1 investigation:
 - Judge prompt no longer contains the contradictory "matiz diferente = NUEVO"
   clause. Now: EXAM-OBJECTIVE granularity. If an existing card teaches the same
   exam objective / core mechanism, it is COVERED even if this question probes a
   slightly different angle or an extra detail. NEW only if it is a different
   service, a different feature, or a distinct exam objective not taught at all.
 - On judge failure we RETRY; we do NOT silently default to NEW (we mark
   'UNCERTAIN' and treat as COVERED-review so failures don't inflate NEW).
 - Topics already Spanish + service-normalized (from phase1 v2).
 - Cards indexed by distilled concept (card_concepts.json).
Output: kiro-test/dedup_results.json (overwrites)
"""
import json, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; EMBED="amazon.titan-embed-text-v2:0"
MAXW=10; TOPK=8
topics=json.load(open("kiro-test/exam_topics.json",encoding="utf-8"))
card_concepts=json.load(open("kiro-test/card_concepts.json",encoding="utf-8"))
_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c
def embed(t):
    for a in range(4):
        try:
            r=bc().invoke_model(modelId=EMBED,body=json.dumps({"inputText":t[:1000]}))
            return np.array(json.loads(r["body"].read())["embedding"],dtype=np.float32)
        except Exception: time.sleep(2**a)
    raise RuntimeError("embed fail")
def embed_all(items):
    out=[None]*len(items)
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        for f in as_completed([ex.submit(lambda i:(i,embed(items[i])),i) for i in range(len(items))]):
            i,v=f.result(); out[i]=v
    return np.vstack(out)

print("embedding...",flush=True)
CC=embed_all([c["concept"] for c in card_concepts]); CC/=(np.linalg.norm(CC,axis=1,keepdims=True)+1e-9)
TT=embed_all([f"{t['topic']}. {t['concept']}" for t in topics]); TT/=(np.linalg.norm(TT,axis=1,keepdims=True)+1e-9)

JUDGE_SYS=(
"Eres experto en DVA-C02 deduplicando temas de estudio a GRANULARIDAD DE EXAMEN. "
"Decide si un TEMA ya esta CUBIERTO por alguno de los CONCEPTOS que el alumno ya estudio, "
"o es NUEVO. Ambos estan en espanol y destilados a su concepto central.\n"
"CRITERIO (granularidad de examen, NO de detalle fino):\n"
"- COVERED = una tarjeta existente ya ensena el MISMO OBJETIVO EXAMINABLE / mecanismo central, "
"AUNQUE esta pregunta lo pruebe desde un angulo algo distinto, con otro escenario, o pida un "
"detalle adicional. Si el alumno, sabiendo la tarjeta existente, ya podria razonar la respuesta, "
"es COVERED.\n"
"- NEW = un SERVICIO distinto, una FEATURE distinta, o un OBJETIVO EXAMINABLE que NO se ensena "
"en ninguna tarjeta. La ausencia de un sub-detalle menor (un limite exacto, un nombre de "
"parametro) NO convierte en NEW algo cuyo concepto central ya esta cubierto.\n"
"Prioriza reconocer cobertura. Ante la duda entre COVERED y NEW cuando el concepto central "
"coincide, elige COVERED. Devuelve SOLO JSON."
)
def judge(i):
    sims=CC@TT[i]; order=np.argsort(-sims)[:TOPK]
    cands=[{"c":card_concepts[j]["concept"],"cos":float(sims[j])} for j in order]
    ct="\n".join(f"[{k+1}] (cos={c['cos']:.2f}) {c['c'][:220]}" for k,c in enumerate(cands))
    msg=(f"TEMA: {topics[i]['topic']}\nCONCEPTO: {topics[i]['concept']}\nSERVICIO: {topics[i]['service']}\n\n"
         f"CONCEPTOS YA ESTUDIADOS MAS SIMILARES:\n{ct}\n\n"
         'JSON: {"verdict":"COVERED"|"NEW","covered_by":<num|null>,"reason":"<una frase>"}')
    last=None
    for a in range(5):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":JUDGE_SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":220,"temperature":0})
            v=json.loads(re.sub(r"^```(json)?|```$","",r["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip())
            cov=(v.get("verdict")=="COVERED")
            return {"id":topics[i]["id"],"question":topics[i]["question"],"topic":topics[i]["topic"],
                    "concept":topics[i]["concept"],"service":topics[i]["service"],
                    "max_cosine":round(cands[0]["cos"],3),"llm_verdict":v.get("verdict"),
                    "llm_reason":v.get("reason",""),"covered":cov,"top_candidate":cands[0]["c"][:160]}
        except Exception as e:
            last=str(e)[:80]; time.sleep(1.5*(a+1))
    # judge failed after retries: mark UNCERTAIN, treat as covered-review (do NOT inflate NEW)
    return {"id":topics[i]["id"],"question":topics[i]["question"],"topic":topics[i]["topic"],
            "concept":topics[i]["concept"],"service":topics[i]["service"],
            "max_cosine":round(cands[0]["cos"],3),"llm_verdict":"UNCERTAIN",
            "llm_reason":f"judge-failed:{last}","covered":True,"top_candidate":cands[0]["c"][:160]}

print("judging (exam-granularity, calibrated)...",flush=True)
results=[None]*len(topics)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    futs={ex.submit(judge,i):i for i in range(len(topics))}
    for f in as_completed(futs): results[futs[f]]=f.result()
json.dump(results,open("kiro-test/dedup_results.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
cov=sum(1 for r in results if r["covered"]); unc=sum(1 for r in results if r["llm_verdict"]=="UNCERTAIN")
print(f"\nDONE | total {len(results)} | COVERED {cov} | NEW {len(results)-cov} | UNCERTAIN {unc}")
