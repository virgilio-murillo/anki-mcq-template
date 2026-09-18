#!/usr/bin/env python3
"""
PHASE 2 (v2, FIXED) - Dedup topics vs existing cards, correcting the cross-language
bug that made almost everything look NEW.

Fixes:
 - Translate/normalize each English topic into a Spanish canonical phrase so the
   embedding compares like-for-like against the Spanish cards (adds ~+0.10 cosine).
 - Retrieve top-K=8 candidate cards (was 5) so the LLM sees enough real context.
 - Two mandatory layers preserved: (A) Titan embedding similarity to pick
   candidates, (B) Claude LLM final verdict COVERED/NEW.
 - Lower auto-nothing: LLM always decides; but we also pass the raw Spanish topic
   AND its English original to the judge so wording never blocks a match.

Output: kiro-test/dedup_results.json (overwrites)
"""
import json, re, time, threading, html
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; EMBED="amazon.titan-embed-text-v2:0"
MAXW=10; TOPK=8

topics=json.load(open("kiro-test/exam_topics.json",encoding="utf-8"))
cards=json.load(open("kiro-test/existing_cards.json",encoding="utf-8"))

def strip_html(s): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",html.unescape(s or ""))).strip()
for c in cards: c["text"]=strip_html(c["front"]+" "+c.get("extra",""))[:600]

_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c

def embed(t):
    for a in range(4):
        try:
            r=bc().invoke_model(modelId=EMBED,body=json.dumps({"inputText":t[:1800]}))
            v=np.array(json.loads(r["body"].read())["embedding"],dtype=np.float32); return v
        except Exception: time.sleep(2**a)
    raise RuntimeError("embed fail")

# --- Step 1: translate topics to Spanish canonical phrases (batch, LLM) ---
TR_SYS=("Traduce conceptos tecnicos de AWS del ingles al espanol de forma canonica y concisa, "
        "conservando nombres propios de servicios/APIs/parametros en su forma oficial "
        "(p.ej. DynamoDB Streams, UpdateItem, GetSessionToken, Read Replica). Devuelve SOLO JSON.")
def translate_batch(batch):
    items="\n".join(f'{i+1}. {t["topic"]} :: {t["concept"]}' for i,t in enumerate(batch))
    msg=(f"Traduce al espanol cada 'topic :: concept':\n{items}\n\n"
         'Devuelve JSON: {"tr":["<topic_es. concept_es>", ...]} en el mismo orden.')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":TR_SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":1500,"temperature":0})
            txt=r["output"]["message"]["content"][0]["text"].strip()
            txt=re.sub(r"^```(json)?|```$","",txt,flags=re.M).strip()
            return json.loads(txt)["tr"]
        except Exception: time.sleep(2**a)
    return [f'{t["topic"]}. {t["concept"]}' for t in batch]

print("Translating topics to Spanish...",flush=True)
BATCH=8
batches=[topics[i:i+BATCH] for i in range(0,len(topics),BATCH)]
tr_results=[None]*len(batches)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    futs={ex.submit(translate_batch,b):i for i,b in enumerate(batches)}
    for f in as_completed(futs): tr_results[futs[f]]=f.result()
topic_es=[]
for bi,b in enumerate(batches):
    tr=tr_results[bi]
    for j,t in enumerate(b):
        topic_es.append(tr[j] if j<len(tr) else f'{t["topic"]}. {t["concept"]}')
assert len(topic_es)==len(topics)

# --- Step 2: embeddings (cards + spanish topics) ---
def embed_all(items,label):
    out=[None]*len(items)
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        done=0
        for f in as_completed([ex.submit(lambda i:(i,embed(items[i])),i) for i in range(len(items))]):
            i,v=f.result(); out[i]=v; done+=1
            if done%50==0: print(f"  embedded {done}/{len(items)} {label}",flush=True)
    return np.vstack(out)

print("Embedding cards + spanish topics...",flush=True)
cv=embed_all([c["text"] for c in cards],"cards"); cv/= (np.linalg.norm(cv,axis=1,keepdims=True)+1e-9)
tv=embed_all(topic_es,"topics"); tv/=(np.linalg.norm(tv,axis=1,keepdims=True)+1e-9)

# --- Step 3: LLM judge with top-K real candidates ---
JUDGE_SYS=("Eres experto en DVA-C02 deduplicando temas de flashcards. Decide si un TEMA DE ESTUDIO "
           "ya esta CUBIERTO por alguna de las tarjetas existentes del alumno (en espanol), o es un "
           "hueco NUEVO. 'Cubierto' = una tarjeta ya ensena el mismo concepto/distincion central, "
           "aunque este redactado distinto o en otro idioma. Servicio distinto, feature distinta, o "
           "un matiz evaluable claramente diferente = NUEVO. Se GENEROSO reconociendo cobertura: si el "
           "concepto central ya se ensena, es CUBIERTO aunque el angulo sea ligeramente distinto. "
           "Devuelve SOLO JSON.")
def judge(i):
    t=topics[i]; sims=cv@tv[i]; order=np.argsort(-sims)[:TOPK]
    cands=[{"text":cards[j]["text"],"cos":float(sims[j])} for j in order]
    ct="\n".join(f"[{k+1}] (cos={c['cos']:.2f}) {c['text'][:280]}" for k,c in enumerate(cands))
    msg=(f"TEMA (EN): {t['topic']}\nTEMA (ES): {topic_es[i]}\nCONCEPTO: {t['concept']}\nSERVICIO: {t['service']}\n\n"
         f"TARJETAS EXISTENTES MAS SIMILARES DEL ALUMNO:\n{ct}\n\n"
         'JSON: {"verdict":"COVERED"|"NEW","covered_by":<num|null>,"reason":"<una frase>"}')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":JUDGE_SYS}],
                messages=[{"role":"user","content":[{"text":msg}]}],
                inferenceConfig={"maxTokens":250,"temperature":0})
            txt=r["output"]["message"]["content"][0]["text"].strip()
            txt=re.sub(r"^```(json)?|```$","",txt,flags=re.M).strip()
            v=json.loads(txt)
        except Exception:
            time.sleep(2**a); continue
        covered=(v.get("verdict")=="COVERED")
        return {"id":t["id"],"question":t["question"],"topic":t["topic"],"topic_es":topic_es[i],
                "concept":t["concept"],"service":t["service"],"max_cosine":round(cands[0]["cos"],3),
                "llm_verdict":v.get("verdict"),"llm_reason":v.get("reason",""),"covered":covered,
                "top_candidate":cands[0]["text"][:160]}
    return {"id":t["id"],"question":t["question"],"topic":t["topic"],"topic_es":topic_es[i],
            "concept":t["concept"],"service":t["service"],"max_cosine":round(cands[0]["cos"],3),
            "llm_verdict":"NEW","llm_reason":"judge-failed","covered":False,"top_candidate":cands[0]["text"][:160]}

print("Judging with LLM (top-8 candidates)...",flush=True)
results=[None]*len(topics)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    futs={ex.submit(judge,i):i for i in range(len(topics))}
    done=0
    for f in as_completed(futs):
        i=futs[f]; results[i]=f.result(); done+=1
        if done%40==0: print(f"  judged {done}/{len(topics)}",flush=True)
json.dump(results,open("kiro-test/dedup_results.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
cov=sum(1 for r in results if r["covered"])
print(f"\nDONE | total {len(results)} | COVERED {cov} | NEW {len(results)-cov}",flush=True)
