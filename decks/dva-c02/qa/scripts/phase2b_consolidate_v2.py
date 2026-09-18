#!/usr/bin/env python3
"""
PHASE 2b (v2, CALIBRATED) - Consolidate the NEW topics among themselves.
Fix from investigation: use a threshold at the REAL boundary (0.62), not 0.80/0.72
which were above the COVERED median (0.675) and made merging a no-op.
Greedy-cluster NEW topics at cos>=0.62, then LLM confirms each multi-member cluster
(same exam objective -> ONE card, listing all source questions; distinct -> split).
Output: kiro-test/consolidated_new.json
"""
import json, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; EMBED="amazon.titan-embed-text-v2:0"
MERGE_COS=0.62; MAXW=10
dedup=json.load(open("kiro-test/dedup_results.json",encoding="utf-8"))
new=[r for r in dedup if not r["covered"]]
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
    raise RuntimeError("embed")
texts=[f"{t['topic']}. {t['concept']}" for t in new]
vecs=[None]*len(texts)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    for f in as_completed([ex.submit(lambda i:(i,embed(texts[i])),i) for i in range(len(texts))]):
        i,v=f.result(); vecs[i]=v
V=np.vstack(vecs); V=V/(np.linalg.norm(V,axis=1,keepdims=True)+1e-9); S=V@V.T
n=len(new); assigned=[-1]*n; clusters=[]
for i in range(n):
    if assigned[i]!=-1: continue
    cid=len(clusters); mem=[i]; assigned[i]=cid
    for j in range(n):
        if assigned[j]==-1 and S[i,j]>=MERGE_COS: assigned[j]=cid; mem.append(j)
    clusters.append(mem)
print(f"{n} NEW -> {len(clusters)} clusters at cos>={MERGE_COS}")
SYS=("Eres experto DVA-C02 consolidando temas de estudio a GRANULARIDAD DE EXAMEN. Dados varios "
     "temas agrupados por similitud, FUSIONA en uno solo los que prueban el MISMO objetivo "
     "examinable (aunque el angulo o el escenario difieran); MANTEN separados los que son objetivos "
     "genuinamente distintos. Prefiere fusionar cuando el concepto central coincide. Solo JSON.")
def resolve(mem):
    if len(mem)==1:
        t=new[mem[0]]
        return [{"topic":t["topic"],"concept":t["concept"],"service":t["service"],
                 "questions":[t["question"]],"source_ids":[t["id"]]}]
    lst="\n".join(f"[{k+1}] Q{new[m]['question']} ({new[m]['service']}): {new[m]['topic']} -- {new[m]['concept']}" for k,m in enumerate(mem))
    msg=(f"TEMAS agrupados:\n{lst}\n\n"
         'JSON: {"groups":[{"member_numbers":[..],"topic":"<canonico>","concept":"<1-2 frases>","service":"<svc>"}]}')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":900,"temperature":0})
            gs=json.loads(re.sub(r"^```(json)?|```$","",r["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip())["groups"]
            out=[]
            for g in gs:
                mm=[mem[k-1] for k in g["member_numbers"] if 1<=k<=len(mem)]
                out.append({"topic":g["topic"],"concept":g["concept"],"service":g.get("service",""),
                            "questions":sorted({new[m]["question"] for m in mm}),
                            "source_ids":[new[m]["id"] for m in mm]})
            return out
        except Exception: time.sleep(2**a)
    return [{"topic":new[m]["topic"],"concept":new[m]["concept"],"service":new[m]["service"],
             "questions":[new[m]["question"]],"source_ids":[new[m]["id"]]} for m in mem]
canon=[]
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    for f in as_completed([ex.submit(resolve,c) for c in clusters]): canon.extend(f.result())
# drop any empty groups defensively
canon=[c for c in canon if c.get("questions") and c.get("source_ids")]
canon.sort(key=lambda c:(c["questions"][0],c["topic"]))
json.dump(canon,open("kiro-test/consolidated_new.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
merged=[c for c in canon if len(c["source_ids"])>1]
print(f"DONE: {n} NEW -> {len(canon)} canonical ({len(merged)} merged groups)")
for c in merged: print(f"   Qs{c['questions']} :: {c['topic'][:55]}")
