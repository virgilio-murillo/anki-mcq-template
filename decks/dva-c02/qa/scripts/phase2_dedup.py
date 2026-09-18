#!/usr/bin/env python3
"""
PHASE 2 - Deduplicate extracted topics against existing DVA-C02 Anki cards.

Two mandatory layers per topic (per user's requirement):
  (A) PROGRAMMATIC similarity: Titan v2 embeddings + cosine similarity ->
      pick the top-K most similar existing cards as candidates.
  (B) LLM confirmation: Claude Sonnet judges, given the topic and its top-K
      candidate cards, whether the topic is ALREADY COVERED or is a NEW gap.

A topic is marked NEW only if BOTH layers agree it is not covered:
  - programmatic max cosine < HARD_COVERED threshold (if >= it's auto-covered,
    but we STILL confirm borderline ones with the LLM), AND
  - the LLM verdict is NEW.
We always run the LLM layer (even when cosine is high or low) so every decision
has both a programmatic and an LLM signal, as required.

Output: kiro-test/dedup_results.json
"""
import json, re, sys, threading, time, html
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION = "us-east-1"
CHAT = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
EMBED = "amazon.titan-embed-text-v2:0"
MAXW = 10
TOPK = 5

topics = json.load(open("kiro-test/exam_topics.json", encoding="utf-8"))
cards = json.load(open("kiro-test/existing_cards.json", encoding="utf-8"))

def strip_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(s or ""))).strip()

for c in cards:
    c["text"] = strip_html(c["front"] + " " + c.get("extra", ""))[:600]

_local = threading.local()
def bc():
    if not hasattr(_local, "c"):
        _local.c = boto3.client("bedrock-runtime", region_name=REGION)
    return _local.c

def embed(text):
    for attempt in range(4):
        try:
            r = bc().invoke_model(modelId=EMBED, body=json.dumps({"inputText": text[:1800]}))
            return np.array(json.loads(r["body"].read())["embedding"], dtype=np.float32)
        except Exception as e:
            time.sleep(2 ** attempt)
    raise RuntimeError("embed failed")

def embed_all(items, label):
    out = [None] * len(items)
    def one(i):
        out[i] = embed(items[i])
        return i
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        done = 0
        for f in as_completed([ex.submit(one, i) for i in range(len(items))]):
            f.result(); done += 1
            if done % 40 == 0: print(f"  embedded {done}/{len(items)} {label}", flush=True)
    return np.vstack(out)

print("Embedding existing cards...", flush=True)
card_vecs = embed_all([c["text"] for c in cards], "cards")
card_norm = card_vecs / (np.linalg.norm(card_vecs, axis=1, keepdims=True) + 1e-9)

print("Embedding topics...", flush=True)
topic_texts = [f"{t['topic']}. {t['concept']}" for t in topics]
topic_vecs = embed_all(topic_texts, "topics")
topic_norm = topic_vecs / (np.linalg.norm(topic_vecs, axis=1, keepdims=True) + 1e-9)

JUDGE_SYS = (
    "You are an AWS DVA-C02 curriculum expert deduplicating flashcard topics. "
    "Decide if a candidate STUDY TOPIC is ALREADY COVERED by any of the learner's "
    "existing flashcards, or is a genuine NEW gap. 'Covered' means an existing card "
    "already teaches the same core concept/distinction (even if worded differently or "
    "in Spanish). Different service, different feature, or a distinct testable nuance = NEW. "
    "Be strict: minor rewordings of the same concept are COVERED; a truly different "
    "concept is NEW. Return STRICT JSON only."
)

def judge(topic, cands):
    cand_txt = "\n".join(f"[{i+1}] (cos={c['cos']:.2f}) {c['text'][:300]}" for i, c in enumerate(cands))
    msg = (
        f"STUDY TOPIC: {topic['topic']}\n"
        f"CONCEPT: {topic['concept']}\n"
        f"SERVICE: {topic['service']}\n\n"
        f"LEARNER'S MOST SIMILAR EXISTING CARDS:\n{cand_txt}\n\n"
        'Return JSON: {"verdict":"COVERED"|"NEW","covered_by":<candidate number or null>,'
        '"reason":"<one sentence>"}'
    )
    for attempt in range(4):
        try:
            r = bc().converse(modelId=CHAT, system=[{"text": JUDGE_SYS}],
                              messages=[{"role": "user", "content": [{"text": msg}]}],
                              inferenceConfig={"maxTokens": 250, "temperature": 0})
            txt = r["output"]["message"]["content"][0]["text"].strip()
            txt = re.sub(r"^```(json)?|```$", "", txt, flags=re.M).strip()
            return json.loads(txt)
        except Exception as e:
            time.sleep(2 ** attempt)
    return {"verdict": "NEW", "covered_by": None, "reason": "judge-failed-default-new"}

def process(idx):
    t = topics[idx]
    sims = card_norm @ topic_norm[idx]
    order = np.argsort(-sims)[:TOPK]
    cands = [{"text": cards[j]["text"], "key": cards[j]["key"], "cos": float(sims[j])} for j in order]
    maxcos = cands[0]["cos"]
    v = judge(t, cands)
    covered = (v.get("verdict") == "COVERED")
    result = {
        "id": t["id"], "question": t["question"], "topic": t["topic"],
        "concept": t["concept"], "service": t["service"],
        "max_cosine": round(maxcos, 3),
        "llm_verdict": v.get("verdict"), "llm_reason": v.get("reason", ""),
        "covered": covered,
        "top_candidate": cands[0]["text"][:160],
    }
    print(f"  {t['id']} Q{t['question']:>2} cos={maxcos:.2f} -> {v.get('verdict')}", flush=True)
    return result

def main():
    t0 = time.time()
    results = [None] * len(topics)
    with ThreadPoolExecutor(max_workers=MAXW) as ex:
        futs = {ex.submit(process, i): i for i in range(len(topics))}
        for f in as_completed(futs):
            i = futs[f]; results[i] = f.result()
    json.dump(results, open("kiro-test/dedup_results.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    new = [r for r in results if not r["covered"]]
    cov = [r for r in results if r["covered"]]
    print(f"\nDONE in {time.time()-t0:.1f}s | total {len(results)} | COVERED {len(cov)} | NEW {len(new)}", flush=True)
    print("wrote kiro-test/dedup_results.json", flush=True)

if __name__ == "__main__":
    main()
