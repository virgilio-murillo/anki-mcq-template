#!/usr/bin/env python3
"""
PHASE 1 (v2, FIXED) - Extract topics at EXAM-OBJECTIVE granularity.
Fix for over-fragmentation: extract 1 PRIMARY testable concept per question,
plus AT MOST 1 secondary ONLY if it tests a genuinely different service/feature.
Normalize service names (strip 'AWS '/'Amazon '). Output in SPANISH canonical form.
"""
import json, re, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

REGION="us-east-1"; MODEL="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; MAXW=10
questions=json.load(open("kiro-test/parsed_questions.json",encoding="utf-8"))
_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c

SYS=(
"Eres experto en el examen AWS Certified Developer Associate (DVA-C02). Dada UNA pregunta "
"de practica, identifica el OBJETIVO EXAMINABLE que prueba: el concepto central que un "
"alumno debe dominar para responderla y responder preguntas similares. "
"REGLA CLAVE DE GRANULARIDAD: extrae 1 tema PRINCIPAL. Anade un 2do tema SOLO si la pregunta "
"prueba genuinamente un servicio o feature DISTINTO e independiente (no un matiz, no un "
"distractor, no 'X vs Y' del mismo concepto). La mayoria de preguntas tienen 1 solo tema. "
"NUNCA fabriques temas satelite (event-driven vs polling, 'limitaciones de', 'distincion "
"entre' del mismo concepto). Nombres de servicio SIN prefijo (escribe 'Lambda' no 'AWS Lambda', "
"'DynamoDB' no 'Amazon DynamoDB'). Responde en ESPANOL. Devuelve SOLO JSON."
)
def prompt(q):
    return (f"PREGUNTA {q['number']} ({q['type']}):\n\n{q['full_block'][:6000]}\n\n"
        'Devuelve JSON: {"topics":[{"topic":"<objetivo examinable, canonico, en espanol>",'
        '"concept":"<1-2 frases: que hay que aprender / la distincion clave>","service":"<servicio sin prefijo>"}]}\n'
        "1 tema (o 2 solo si hay un 2do servicio/feature realmente distinto).")

def norm_svc(s):
    return re.sub(r"^(AWS|Amazon)\s+","",(s or "").strip())

def extract(q):
    for a in range(5):
        try:
            r=bc().converse(modelId=MODEL,system=[{"text":SYS}],
                messages=[{"role":"user","content":[{"text":prompt(q)}]}],
                inferenceConfig={"maxTokens":600,"temperature":0})
            txt=re.sub(r"^```(json)?|```$","",r["output"]["message"]["content"][0]["text"].strip(),flags=re.M).strip()
            tps=json.loads(txt)["topics"][:2]
            for t in tps: t["question"]=q["number"]; t["service"]=norm_svc(t.get("service",""))
            print(f"  Q{q['number']:>2}: {len(tps)} topic(s)",flush=True)
            return q["number"],tps
        except Exception as e:
            print(f"  Q{q['number']} attempt {a+1}: {str(e)[:70]}",flush=True); time.sleep(1.5*(a+1))
    return q["number"],[]

def main():
    t0=time.time(); res={}
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        futs={ex.submit(extract,q):q["number"] for q in questions}
        for f in as_completed(futs):
            n,tps=f.result(); res[n]=tps
    allt=[]; tid=0
    for n in sorted(res):
        for t in res[n]:
            tid+=1
            allt.append({"id":f"t{tid:03d}","topic":t.get("topic","").strip(),
                         "concept":t.get("concept","").strip(),"service":t.get("service","").strip(),
                         "question":n})
    json.dump(allt,open("kiro-test/exam_topics.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    import collections
    dist=collections.Counter(len(res[n]) for n in res)
    print(f"\nDONE: {len(allt)} topics from {len(res)} questions in {time.time()-t0:.1f}s")
    print("topics/question distribution:",dict(dist))

if __name__=="__main__": main()
