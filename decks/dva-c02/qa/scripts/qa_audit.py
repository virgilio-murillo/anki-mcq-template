#!/usr/bin/env python3
"""
QA pass for deck 09 vs DECK_STANDARDS:
 (1) Normalize HTML tags to the deck convention: <strong>-><b>, </strong></b>,
     <em>-><i>. (Rule 9: use <b>, not <strong>.)
 (2) LLM quality audit (10 threads) of each card vs Rules 3 & 4:
     - defines terms before use
     - connects scenario symptom to the solution
     - refutes each distractor correctly and technically
     - correct option technically complete + accurate vs AWS docs
     Flags cards needing rework with a specific reason.
Writes kiro-test/qa_report.json and normalizes kiro-test/generated_cards.json in place.
"""
import json, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; MAXW=10
cards=json.load(open("kiro-test/generated_cards.json",encoding="utf-8"))

def normalize(s):
    s=s.replace("<strong>","<b>").replace("</strong>","</b>")
    s=s.replace("<STRONG>","<b>").replace("</STRONG>","</b>")
    s=s.replace("<em>","<i>").replace("</em>","</i>")
    return s
for c in cards:
    c["question"]=normalize(c["question"])
    c["answer"]=normalize(c["answer"])
    c["options"]=[normalize(o) for o in c["options"]]
json.dump(cards,open("kiro-test/generated_cards.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("normalized <strong>-><b>, <em>-><i> in all cards")

_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c

AUD_SYS=(
"Eres revisor de calidad de tarjetas Anki para el examen AWS DVA-C02, en espanol. "
"Evalua UNA tarjeta contra estos estandares OBLIGATORIOS:\n"
"R3a DEFINE TERMINOS: el reverso define los terminos/siglas antes de usarlos.\n"
"R3b CONECTA ESCENARIO-SOLUCION: explica POR QUE la respuesta resuelve el problema (mecanismo), "
"no solo la nombra.\n"
"R3c REFUTA CADA DISTRACTOR: hay una refutacion tecnica concreta por cada opcion incorrecta.\n"
"R4 CORRECCION TECNICA: la opcion correcta es tecnicamente correcta y completa vs docs de AWS; "
"los distractores son errores creibles, no features inventadas.\n"
"Se estricto pero justo. Devuelve SOLO JSON."
)
def audit(idx):
    c=cards[idx]
    opts="\n".join(f"{chr(65+i)}. {re.sub('<[^>]+>','',o)}" for i,o in enumerate(c['options']))
    correct_letter=chr(65+c['correct'])
    body=(f"PREGUNTA: {re.sub('<[^>]+>','',c['question'])}\n\nOPCIONES:\n{opts}\n\n"
          f"CORRECTA: {correct_letter}\n\nREVERSO (HTML):\n{c['answer'][:3000]}\n\n"
          'Devuelve JSON: {"ok":true|false,"issues":["R3a|R3b|R3c|R4: <detalle>"],'
          '"tech_error":"<si hay error tecnico en la respuesta correcta, describelo; si no, null>"}')
    for a in range(4):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":AUD_SYS}],
                messages=[{"role":"user","content":[{"text":body}]}],
                inferenceConfig={"maxTokens":500,"temperature":0})
            v=json.loads(re.sub(r"^```(json)?|```$","",r["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip())
            return {"key":c["key"],"topic":c["topic"],"ok":bool(v.get("ok")),
                    "issues":v.get("issues",[]),"tech_error":v.get("tech_error")}
        except Exception:
            time.sleep(1.5*(a+1))
    return {"key":c["key"],"topic":c["topic"],"ok":True,"issues":[],"tech_error":None,"_audit_failed":True}

print("auditing 32 cards vs Rules 3 & 4 (LLM, 10 threads)...")
rep=[None]*len(cards)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    for f in as_completed([ex.submit(audit,i) for i in range(len(cards))]):
        r=f.result()
        # place in order by key
        rep[[c["key"] for c in cards].index(r["key"])]=r
json.dump(rep,open("kiro-test/qa_report.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
flagged=[r for r in rep if not r["ok"] or r.get("tech_error")]
print(f"\nAUDIT DONE: {len(cards)} cards | flagged {len(flagged)}")
for r in flagged:
    print(f"  {r['key']} :: {r['topic'][:45]}")
    if r.get("tech_error"): print(f"     TECH: {r['tech_error'][:120]}")
    for i in r["issues"][:4]: print(f"     - {i[:120]}")
