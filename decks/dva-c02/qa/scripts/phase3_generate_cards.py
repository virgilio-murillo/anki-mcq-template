#!/usr/bin/env python3
"""
PHASE 3 - Generate one atomic MCQ card per canonical NEW topic, via Bedrock
Claude Sonnet (10 threads). Each card follows DECK_STANDARDS.md:
 - self-contained Spanish stem, 4 balanced options, one correct
 - back: verdict with {{L}}, why-correct, refute EACH distractor, exam gotcha
 - balanced option lengths (correct not the longest/shortest) -> passes verify
Outputs kiro-test/generated_cards.json  (list of {question,options,correct,key,answer,src_questions})
"""
import json, re, time, threading, hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

REGION="us-east-1"; CHAT="us.anthropic.claude-sonnet-4-5-20250929-v1:0"; MAXW=10
topics=json.load(open("kiro-test/consolidated_new.json",encoding="utf-8"))

_local=threading.local()
def bc():
    if not hasattr(_local,"c"): _local.c=boto3.client("bedrock-runtime",region_name=REGION)
    return _local.c

SYS=(
"Eres un experto en el examen AWS Certified Developer Associate (DVA-C02) y creas "
"tarjetas Anki de opcion multiple de altisima calidad, en ESPANOL. Debes cumplir "
"ESTRICTAMENTE estas reglas:\n"
"1. El 'stem' es autocontenido (no depende de ningun escenario externo) y pregunta "
"por el concepto atomico dado.\n"
"2. EXACTAMENTE 4 opciones. Solo UNA correcta.\n"
"3. BALANCE OBLIGATORIO: las 4 opciones deben tener longitud y especificidad "
"comparables. La opcion correcta NO puede ser la mas larga ni la mas corta ni la mas "
"detallada. Ninguna opcion puede exceder ~1.4x el promedio de las otras. Sube el nivel "
"de los distractores (hazlos especificos y plausibles), no acortes la correcta.\n"
"4. Los distractores son errores tecnicos creibles (servicio/feature/parametro "
"equivocado), nunca rellenos vagos.\n"
"5. El 'answer' (reverso) es HTML e incluye: un <div class=\"verdict\">Correcta: {{L}} "
"&mdash; <resumen></div> (usa LITERALMENTE {{L}}, el motor sustituye la letra), un "
"parrafo <p> de por que la correcta funciona (define terminos), una lista <ul> que "
"refuta CADA distractor una por una ('Por que NO las otras, una por una:'), un "
"<div class=\"extra\"><span class=\"h\">Truco de examen</span>...</div>, y un "
"<div class=\"links\"><span class=\"h\">Link</span><a href=\"...docs.aws...\">...</a></div>.\n"
"6. Sin em dashes (usa comas, parentesis o ' - '). Usa entidades HTML para acentos "
"(&aacute; &eacute; &iacute; &oacute; &uacute; &ntilde; &iquest; &iexcl;) o UTF-8 correcto.\n"
"7. Contenido tecnicamente correcto y verificable contra docs oficiales de AWS.\n"
"Devuelve SOLO JSON valido."
)

def gen_prompt(t):
    qs=", ".join(f"Q{q}" for q in t["questions"])
    return (
        f"TEMA: {t['topic']}\nCONCEPTO: {t['concept']}\nSERVICIO: {t['service']}\n"
        f"(Proviene de: {qs} del examen de practica DVA-C02)\n\n"
        "Crea UNA tarjeta MCQ atomica en espanol sobre este tema. "
        'Devuelve JSON EXACTO: {"question":"<stem HTML>","options":["op1","op2","op3","op4"],'
        '"correct":<indice 0-3 de la correcta>,"answer":"<reverso HTML con {{L}}>"}\n'
        "Recuerda el BALANCE de longitud entre las 4 opciones."
    )

def strip_html_len(s):
    return len(re.sub(r"<[^>]+>"," ",s))

def balanced(options, correct):
    lens=[strip_html_len(o) for o in options]
    avg=sum(l for j,l in enumerate(lens) if j!=correct)/3
    return not (lens[correct] > 1.4*avg or lens[correct] < 0.71*avg)

def make_key(t):
    base=(t["topic"]+"|"+t["service"]).lower()
    h=hashlib.sha1(base.encode()).hexdigest()[:8]
    return f"dva09-{h}"

def gen_one(idx):
    t=topics[idx]
    for attempt in range(5):
        try:
            r=bc().converse(modelId=CHAT,system=[{"text":SYS}],
                messages=[{"role":"user","content":[{"text":gen_prompt(t)}]}],
                inferenceConfig={"maxTokens":1600,"temperature":0.2 if attempt==0 else 0.4})
            txt=r["output"]["message"]["content"][0]["text"].strip()
            txt=re.sub(r"^```(json)?|```$","",txt,flags=re.M).strip()
            d=json.loads(txt)
            opts=d["options"]; corr=int(d["correct"]); ans=d["answer"]; q=d["question"]
            assert len(opts)==4, "need 4 options"
            assert 0<=corr<=3
            assert "{{L}}" in ans, "answer must contain {{L}}"
            assert "verdict" in ans and "extra" in ans
            if not balanced(opts,corr):
                if attempt<4:
                    raise ValueError("unbalanced options, retrying")
            key=make_key(t)
            print(f"  [{idx+1}/{len(topics)}] {key} ok", flush=True)
            return {"question":q,"options":opts,"correct":corr,"key":key,"answer":ans,
                    "src_questions":t["questions"],"topic":t["topic"],"service":t["service"]}
        except Exception as e:
            print(f"  [{idx+1}] attempt {attempt+1} fail: {str(e)[:80]}", flush=True)
            time.sleep(1.5*(attempt+1))
    return None

def main():
    t0=time.time(); out=[None]*len(topics)
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        futs={ex.submit(gen_one,i):i for i in range(len(topics))}
        for f in as_completed(futs):
            i=futs[f]; out[i]=f.result()
    cards=[c for c in out if c]
    # dedup keys (hash collisions) by suffixing
    seen={}
    for c in cards:
        k=c["key"]
        if k in seen:
            seen[k]+=1; c["key"]=f"{k}{seen[k]}"
        else:
            seen[k]=0
    json.dump(cards,open("kiro-test/generated_cards.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    print(f"\nDONE: generated {len(cards)}/{len(topics)} cards in {time.time()-t0:.1f}s")
    print("wrote kiro-test/generated_cards.json")

if __name__=="__main__":
    main()
