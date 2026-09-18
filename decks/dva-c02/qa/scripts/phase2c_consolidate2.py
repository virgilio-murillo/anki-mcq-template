#!/usr/bin/env python3
"""
PHASE 2c - Second consolidation pass on the 140 canonical topics, at a lower
cosine (0.72) so near-duplicate concepts that the 0.80 pass missed get grouped.
LLM confirms each multi-member cluster (same concept -> merge; distinct -> split).
This is SAFE because the LLM makes the final merge/split call.

Output overwrites kiro-test/consolidated_new.json with the tighter set.
"""
import json, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; EMBED="amazon.titan-embed-text-v2:0"
MERGE_COS=0.72; MAXW=10

items = json.load(open("kiro-test/consolidated_new.json", encoding="utf-8"))
_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c
def embed(t):
    for a in range(4):
        try:
            r=bc().invoke_model(modelId=EMBED,body=json.dumps({"inputText":t[:1800]}))
            v=np.array(json.loads(r["body"].read())["embedding"],dtype=np.float32)
            return v
        except Exception: time.sleep(2**a)
    raise RuntimeError("embed fail")

texts=[f"{c['topic']}. {c['concept']}" for c in items]
vecs=[None]*len(texts)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    for f in as_completed([ex.submit(lambda i:(i,embed(texts[i])),i) for i in range(len(texts))]):
        i,v=f.result(); vecs[i]=v
V=np.vstack(vecs); norms=np.linalg.norm(V,axis=1,keepdims=True); V=V/(norms+1e-9)
S=V@V.T
n=len(items); assigned=[-1]*n; clusters=[]
for i in range(n):
    if assigned[i]!=-1: continue
    cid=len(clusters); mem=[i]; assigned[i]=cid
    for j in range(n):
        if assigned[j]==-1 and S[i,j]>=MERGE_COS:
            assigned[j]=cid; mem.append(j)
    clusters.append(mem)
print(f"{n} -> {len(clusters)} clusters at cos>={MERGE_COS}")

SYS=("You are an AWS DVA-C02 expert consolidating flashcard topics. Given candidate "
     "topics grouped by similarity, MERGE only those that teach the SAME testable concept "
     "into one canonical card; keep genuinely DISTINCT concepts separate. Return STRICT JSON.")
def resolve(mem):
    if len(mem)==1:
        c=items[mem[0]]; return [c]
    lst="\n".join(f"[{k+1}] ({items[m]['service']}) {items[m]['topic']} -- {items[m]['concept']}" for k,m in enumerate(mem))
    msg=(f"CANDIDATES:\n{lst}\n\n"
         'Return JSON: {"groups":[{"member_numbers":[..],"topic":"<canonical>","concept":"<1-2 sentences>","service":"<svc>"}]}')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":1000,"temperature":0})
            txt=r["output"]["message"]["content"][0]["text"].strip()
            txt=re.sub(r"^```(json)?|```$","",txt,flags=re.M).strip()
            gs=json.loads(txt)["groups"]; out=[]
            for g in gs:
                mm=[mem[k-1] for k in g["member_numbers"] if 1<=k<=len(mem)]
                qs=sorted({q for m in mm for q in items[m]["questions"]})
                ids=[x for m in mm for x in items[m]["source_ids"]]
                out.append({"topic":g["topic"],"concept":g["concept"],"service":g.get("service",""),
                            "questions":qs,"source_ids":ids})
            return out
        except Exception: time.sleep(2**a)
    return [items[m] for m in mem]

canon=[]
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    for f in as_completed([ex.submit(resolve,c) for c in clusters]):
        canon.extend(f.result())
canon.sort(key=lambda c:(c["questions"][0],c["topic"]))
json.dump(canon,open("kiro-test/consolidated_new.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(f"DONE: {n} -> {len(canon)} canonical cards-to-build")
