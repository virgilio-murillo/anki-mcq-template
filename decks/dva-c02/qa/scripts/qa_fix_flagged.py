#!/usr/bin/env python3
"""Regenerate the 6 flagged cards with a reinforced prompt that (a) fixes the
specific technical errors the auditor found, (b) enforces Rules 3 & 4:
define terms, connect scenario->solution, refute EACH distractor technically,
technically-complete correct answer. Keeps the same key (stable). Re-audits."""
import json, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; MAXW=6
cards=json.load(open("kiro-test/generated_cards.json",encoding="utf-8"))
report=json.load(open("kiro-test/qa_report.json",encoding="utf-8"))
by_key={c["key"]:c for c in cards}
flagged={r["key"]:r for r in report if (not r["ok"]) or r.get("tech_error")}
print("regenerating", len(flagged), "flagged cards")

_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c

SYS=(
"Eres experto en AWS DVA-C02 y creas UNA tarjeta Anki MCQ de maxima calidad en ESPANOL, "
"corrigiendo problemas de calidad detectados. CUMPLE ESTRICTO:\n"
"- 4 opciones balanceadas (la correcta NO la mas larga ni corta; sube el nivel de los distractores).\n"
"- Reverso 'answer' HTML con: <div class=\"verdict\">Correcta: {{L}} &mdash; <resumen></div>; un <p> que "
"DEFINE los terminos/siglas antes de usarlos y explica el MECANISMO de por que la respuesta resuelve "
"el problema; luego '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>' seguido de un <ul> con "
"un <li> por CADA distractor con refutacion tecnica concreta (mecanismo/parametro/servicio equivocado, "
"no vaguedades); un <div class=\"extra\"><span class=\"h\">Truco de examen</span>...</div>; y un "
"<div class=\"links\"><span class=\"h\">Link</span><a href=\"...docs.aws...\">...</a></div>.\n"
"- Usa <b> (no <strong>), <code>, <ul>/<li>, <p>. Entidades HTML para acentos. Sin em dashes (usa "
"comas/parentesis). {{L}} literal.\n"
"- TECNICAMENTE CORRECTO Y COMPLETO vs docs oficiales de AWS. Corrige el error senalado. "
"Devuelve SOLO JSON."
)
def prompt(c,r):
    issues="\n".join(f"- {x}" for x in r.get("issues",[]))
    tech=r.get("tech_error") or "ninguno"
    opts="\n".join(f"{chr(65+i)}. {re.sub('<[^>]+>','',o)}" for i,o in enumerate(c["options"]))
    return (f"TEMA: {c['topic']} (servicio {c['service']})\n\n"
            f"TARJETA ACTUAL:\nPREGUNTA: {re.sub('<[^>]+>','',c['question'])}\nOPCIONES:\n{opts}\n"
            f"CORRECTA: {chr(65+c['correct'])}\n\n"
            f"PROBLEMAS DE CALIDAD A CORREGIR:\n{issues}\nERROR TECNICO: {tech}\n\n"
            "Reescribe la tarjeta corrigiendo TODO lo anterior, manteniendo el mismo tema/objetivo examinable. "
            'JSON: {"question":"<stem HTML>","options":["o1","o2","o3","o4"],"correct":<0-3>,"answer":"<reverso con {{L}} y \'una por una\'>"}')

def strip_len(s): return len(re.sub(r"<[^>]+>","",s))
def balanced(opts,corr):
    L=[strip_len(o) for o in opts]; avg=sum(l for j,l in enumerate(L) if j!=corr)/3
    return not (L[corr]>1.4*avg or L[corr]<0.71*avg)

def regen(key):
    c=by_key[key]; r=flagged[key]
    for a in range(5):
        try:
            resp=bc().converse(modelId=CHAT,system=[{"text":SYS}],
                messages=[{"role":"user","content":[{"text":prompt(c,r)}]}],
                inferenceConfig={"maxTokens":1700,"temperature":0.2 if a==0 else 0.4})
            d=json.loads(re.sub(r"^```(json)?|```$","",resp["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip())
            o=d["options"]; corr=int(d["correct"]); ans=d["answer"]
            assert len(o)==4 and 0<=corr<=3 and "{{L}}" in ans and "una por una" in ans and "verdict" in ans
            assert "<strong>" not in ans, "usa <b>"
            if not balanced(o,corr) and a<4: raise ValueError("unbalanced")
            c["question"]=d["question"]; c["options"]=o; c["correct"]=corr; c["answer"]=ans
            print(f"  {key}: regenerated ok")
            return
        except Exception as e:
            print(f"  {key} attempt {a+1}: {str(e)[:70]}"); time.sleep(1.5*(a+1))
    print(f"  {key}: FAILED to regenerate, keeping original")

with ThreadPoolExecutor(max_workers=MAXW) as ex:
    list(ex.map(regen, list(flagged.keys())))

json.dump(cards,open("kiro-test/generated_cards.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("saved regenerated cards")
