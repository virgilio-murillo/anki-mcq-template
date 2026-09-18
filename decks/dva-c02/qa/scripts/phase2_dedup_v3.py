#!/usr/bin/env python3
"""
PHASE 2 (v3, DEFINITIVE) - Concept-vs-concept dedup.
 - Existing cards indexed by their DISTILLED core concept (Spanish, noise-free).
 - Topics translated to Spanish canonical phrases.
 - Embed both (concept-level) -> top-8 candidate CONCEPTS per topic (programmatic).
 - Claude judges COVERED/NEW seeing topic + its concept + top-8 card concepts (LLM).
Both layers preserved; matching is now apples-to-apples.

Output: kiro-test/dedup_results.json (overwrites)
"""
import json, re, time, threading, html
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; EMBED="amazon.titan-embed-text-v2:0"
MAXW=10; TOPK=8

topics=json.load(open("kiro-test/exam_topics.json",encoding="utf-8"))
card_concepts=json.load(open("kiro-test/card_concepts.json",encoding="utf-8"))
# reuse spanish topic translations if present in prior dedup; else translate now
prev={}
try:
    for r in json.load(open("kiro-test/dedup_results.json",encoding="utf-8")):
        if r.get("topic_es"): prev[r["id"]]=r["topic_es"]
except Exception: pass

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

# spanish topics
TR_SYS=("Traduce conceptos AWS al espanol canonico y conciso, conservando nombres oficiales "
        "(DynamoDB Streams, UpdateItem, Read Replica, Lambda Layers, atomic counter). Solo JSON.")
def translate_batch(batch):
    items="\n".join(f'{i+1}. {t["topic"]} :: {t["concept"]}' for i,t in enumerate(batch))
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":TR_SYS}],
                messages=[{"role":"user","content":[{"text":f"{items}\n\nJSON: {{\"tr\":[\"<topic_es. concept_es>\",...]}}"}]}],
                inferenceConfig={"maxTokens":1500,"temperature":0})
            txt=re.sub(r"^```(json)?|```$","",r["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip()
            return json.loads(txt)["tr"]
        except Exception: time.sleep(2**a)
    return [f'{t["topic"]}. {t["concept"]}' for t in batch]

topic_es=[None]*len(topics)
need=[i for i,t in enumerate(topics) if t["id"] not in prev]
for i,t in enumerate(topics):
    if t["id"] in prev: topic_es[i]=prev[t["id"]]
if need:
    idxb=[need[i:i+8] for i in range(0,len(need),8)]
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        futs={ex.submit(translate_batch,[topics[j] for j in b]):b for b in idxb}
        for f in as_completed(futs):
            b=futs[f]; tr=f.result()
            for k,j in enumerate(b): topic_es[j]=tr[k] if k<len(tr) else f'{topics[j]["topic"]}. {topics[j]["concept"]}'

# embeddings: card concepts + topic(spanish)
def embed_all(items):
    out=[None]*len(items)
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        for f in as_completed([ex.submit(lambda i:(i,embed(items[i])),i) for i in range(len(items))]):
            i,v=f.result(); out[i]=v
    return np.vstack(out)

print("embedding card concepts + topics...",flush=True)
CC=embed_all([c["concept"] for c in card_concepts]); CC/=(np.linalg.norm(CC,axis=1,keepdims=True)+1e-9)
TT=embed_all(topic_es); TT/=(np.linalg.norm(TT,axis=1,keepdims=True)+1e-9)

JUDGE_SYS=("Eres experto DVA-C02 deduplicando temas. Decide si un TEMA ya esta CUBIERTO por alguno "
           "de los CONCEPTOS de tarjetas que el alumno ya estudio, o es NUEVO. Ambos estan en espanol "
           "y ya destilados a su concepto central. 'Cubierto' = el mismo concepto/mecanismo/distincion "
           "central ya se ensena (aunque el angulo sea algo distinto). Servicio distinto, feature "
           "distinta o matiz claramente diferente = NUEVO. Se GENEROSO con la cobertura: prioriza "
           "detectar solapes reales. Solo JSON.")
def judge(i):
    sims=CC@TT[i]; order=np.argsort(-sims)[:TOPK]
    cands=[{"c":card_concepts[j]["concept"],"cos":float(sims[j])} for j in order]
    ct="\n".join(f"[{k+1}] (cos={c['cos']:.2f}) {c['c'][:200]}" for k,c in enumerate(cands))
    msg=(f"TEMA (EN): {topics[i]['topic']}\nTEMA (ES): {topic_es[i]}\nCONCEPTO: {topics[i]['concept']}\n"
         f"SERVICIO: {topics[i]['service']}\n\nCONCEPTOS YA ESTUDIADOS MAS SIMILARES:\n{ct}\n\n"
         'JSON: {"verdict":"COVERED"|"NEW","covered_by":<num|null>,"reason":"<una frase>"}')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":JUDGE_SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":220,"temperature":0})
            v=json.loads(re.sub(r"^```(json)?|```$","",r["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip())
        except Exception:
            time.sleep(2**a); continue
        cov=(v.get("verdict")=="COVERED")
        return {"id":topics[i]["id"],"question":topics[i]["question"],"topic":topics[i]["topic"],
                "topic_es":topic_es[i],"concept":topics[i]["concept"],"service":topics[i]["service"],
                "max_cosine":round(cands[0]["cos"],3),"llm_verdict":v.get("verdict"),
                "llm_reason":v.get("reason",""),"covered":cov,"top_candidate":cands[0]["c"][:160]}
    return {"id":topics[i]["id"],"question":topics[i]["question"],"topic":topics[i]["topic"],
            "topic_es":topic_es[i],"concept":topics[i]["concept"],"service":topics[i]["service"],
            "max_cosine":round(cands[0]["cos"],3),"llm_verdict":"NEW","llm_reason":"judge-failed",
            "covered":False,"top_candidate":cands[0]["c"][:160]}

print("judging concept-vs-concept...",flush=True)
results=[None]*len(topics)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    futs={ex.submit(judge,i):i for i in range(len(topics))}
    done=0
    for f in as_completed(futs):
        results[futs[f]]=f.result(); done+=1
        if done%40==0: print(f"  judged {done}/{len(topics)}",flush=True)
json.dump(results,open("kiro-test/dedup_results.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
cov=sum(1 for r in results if r["covered"])
print(f"\nDONE | total {len(results)} | COVERED {cov} | NEW {len(results)-cov}",flush=True)
