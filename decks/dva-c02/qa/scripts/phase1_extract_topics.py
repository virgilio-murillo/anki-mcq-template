#!/usr/bin/env python3
"""
PHASE 1 - Extract atomic study topics from each of the 65 exam questions.
Parallel (10 threads) calls to Bedrock Claude Sonnet 4.5.

Each topic is tied to its source question number. Output:
  kiro-test/exam_topics.json  (machine)
  notes/source/exam_topics.md (human readable, topic <-> question)
"""
import json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

REGION = "us-east-1"
MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
MAXW = 10

questions = json.load(open("kiro-test/parsed_questions.json", encoding="utf-8"))

_local = threading.local()
def client():
    if not hasattr(_local, "c"):
        _local.c = boto3.client("bedrock-runtime", region_name=REGION)
    return _local.c

SYS = (
    "You are an AWS Certified Developer Associate (DVA-C02) curriculum expert. "
    "Given one practice exam question (stem, options, correct answer, rationales), "
    "extract the 2-3 ATOMIC, testable AWS concepts a learner must MASTER to answer it "
    "and questions like it. A topic is the underlying concept, NOT the scenario. "
    "Be specific and canonical (service + feature + the exact distinction being tested). "
    "Examples of good atomic topics: "
    "'DynamoDB Streams as a Lambda event source for change notifications', "
    "'SNS subscription dead-letter queue (DLQ) for failed HTTPS deliveries', "
    "'STS decode-authorization-message to decode encoded IAM authorization failures', "
    "'CodeDeploy Linear vs Canary vs All-at-once traffic-shift configs'. "
    "Return STRICT JSON only, no prose."
)

def prompt(q):
    return (
        f"QUESTION {q['number']} ({q['type']}):\n\n{q['full_block'][:6000]}\n\n"
        "Return JSON exactly like:\n"
        '{"topics":[{"topic":"<short canonical topic name>",'
        '"concept":"<1-2 sentence what must be learned / the key distinction>",'
        '"service":"<primary AWS service>"}]}\n'
        "2 or 3 topics. No extra keys, no markdown."
    )

def extract_one(q):
    for attempt in range(4):
        try:
            r = client().converse(
                modelId=MODEL,
                system=[{"text": SYS}],
                messages=[{"role": "user", "content": [{"text": prompt(q)}]}],
                inferenceConfig={"maxTokens": 700, "temperature": 0},
            )
            txt = r["output"]["message"]["content"][0]["text"].strip()
            txt = re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.M).strip()
            data = json.loads(txt)
            topics = data["topics"]
            for t in topics:
                t["question"] = q["number"]
            print(f"  Q{q['number']:>2}: {len(topics)} topics", flush=True)
            return q["number"], topics
        except Exception as e:
            wait = 2 ** attempt
            print(f"  Q{q['number']} attempt {attempt+1} failed: {str(e)[:90]} (retry in {wait}s)", flush=True)
            time.sleep(wait)
    return q["number"], []

def main():
    t0 = time.time()
    results = {}
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        futs = {ex.submit(extract_one, q): q["number"] for q in questions}
        for f in as_completed(futs):
            n, topics = f.result()
            results[n] = topics
    # flatten, keep tie to question
    all_topics = []
    tid = 0
    for n in sorted(results):
        for t in results[n]:
            tid += 1
            all_topics.append({
                "id": f"t{tid:03d}",
                "topic": t.get("topic", "").strip(),
                "concept": t.get("concept", "").strip(),
                "service": t.get("service", "").strip(),
                "question": n,
            })
    json.dump(all_topics, open("kiro-test/exam_topics.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    # human MD
    with open("notes/source/exam_topics.md", "w", encoding="utf-8") as fh:
        fh.write("# DVA-C02 examen_practica.txt - Temas extraidos (tema <-> pregunta)\n\n")
        fh.write(f"Fuente: examen_practica.txt (65 preguntas). "
                 f"Temas extraidos: {len(all_topics)}. Generado por Bedrock Claude Sonnet 4.5.\n\n")
        for n in sorted(results):
            fh.write(f"## Pregunta {n}\n")
            for t in [x for x in all_topics if x["question"] == n]:
                fh.write(f"- **[{t['id']}] {t['topic']}** ({t['service']})\n")
                fh.write(f"  - {t['concept']}\n")
            fh.write("\n")
    dt = time.time() - t0
    print(f"\nDONE: {len(all_topics)} topics from {len(results)} questions in {dt:.1f}s", flush=True)
    print("wrote kiro-test/exam_topics.json + notes/source/exam_topics.md", flush=True)

if __name__ == "__main__":
    main()
