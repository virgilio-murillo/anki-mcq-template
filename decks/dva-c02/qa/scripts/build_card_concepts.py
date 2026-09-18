#!/usr/bin/env python3
"""
Build a concept index for the 188 existing cards: use Claude to distill each
card's CORE concept into one canonical Spanish phrase (service + feature +
tested distinction), stripping the scenario noise. This makes concept-vs-concept
matching far more accurate than raw-text matching.

Output: kiro-test/card_concepts.json  [{idx, key, concept}]
"""
import json, re, time, threading, html
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; MAXW=10
cards=json.load(open("kiro-test/existing_cards.json",encoding="utf-8"))
def strip_html(s): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",html.unescape(s or ""))).strip()

_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c

SYS=("Eres experto en DVA-C02. Dada una tarjeta flashcard (pregunta + opciones), destila el "
     "CONCEPTO CENTRAL evaluado en UNA frase canonica y concisa: servicio + feature + la "
     "distincion/mecanismo exacto que se prueba. Ignora el escenario. Conserva nombres oficiales "
     "(DynamoDB Streams, UpdateItem, Read Replica, Lambda Layers, atomic counter, multipart upload). "
     "Devuelve SOLO JSON.")

def distill_batch(batch):
    items="\n\n".join(f"[{i+1}] {strip_html(c['front']+' '+c.get('extra',''))[:500]}" for i,c in enumerate(batch))
    msg=(f"Destila el concepto central de cada tarjeta:\n{items}\n\n"
         'JSON: {"concepts":["<frase canonica 1>", ...]} en orden.')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":1200,"temperature":0})
            txt=r["output"]["message"]["content"][0]["text"].strip()
            txt=re.sub(r"^```(json)?|```$","",txt,flags=re.M).strip()
            return json.loads(txt)["concepts"]
        except Exception: time.sleep(2**a)
    return [strip_html(c["front"])[:120] for c in batch]

BATCH=6
batches=[cards[i:i+BATCH] for i in range(0,len(cards),BATCH)]
res=[None]*len(batches)
print(f"distilling {len(cards)} card concepts in {len(batches)} batches...",flush=True)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    futs={ex.submit(distill_batch,b):i for i,b in enumerate(batches)}
    done=0
    for f in as_completed(futs):
        res[futs[f]]=f.result(); done+=1
        if done%8==0: print(f"  {done}/{len(batches)} batches",flush=True)
concepts=[]
gi=0
for bi,b in enumerate(batches):
    cc=res[bi]
    for j,c in enumerate(b):
        concepts.append({"idx":gi,"key":c["key"],
                         "concept":cc[j] if j<len(cc) else strip_html(c["front"])[:120],
                         "text":strip_html(c["front"])[:300]})
        gi+=1
json.dump(concepts,open("kiro-test/card_concepts.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(f"DONE: {len(concepts)} card concepts -> kiro-test/card_concepts.json",flush=True)
print("sample:")
for c in concepts[:5]: print("  -",c["concept"][:90])
