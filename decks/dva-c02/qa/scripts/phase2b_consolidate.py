#!/usr/bin/env python3
"""
PHASE 2b - Consolidate the NEW topics among THEMSELVES so we don't create
multiple cards for the same concept (many questions touch the same service).

(A) PROGRAMMATIC: embed all NEW topics, greedy-cluster by cosine >= MERGE_COS.
(B) LLM: for each multi-member cluster, Claude confirms whether members are the
    SAME concept (merge into one canonical card, listing all source questions)
    or should stay separate. Singletons pass through.

Output: kiro-test/consolidated_new.json  (canonical topics to build as cards)
"""
import json, re, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3, numpy as np

REGION = "us-east-1"
CHAT = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
EMBED = "amazon.titan-embed-text-v2:0"
MERGE_COS = 0.80
MAXW = 10

dedup = json.load(open("kiro-test/dedup_results.json", encoding="utf-8"))
new_topics = [r for r in dedup if not r["covered"]]

_local = threading.local()
def bc():
    if not hasattr(_local, "c"):
        _local.c = boto3.client("bedrock-runtime", region_name=REGION)
    return _local.c

def embed(text):
    for a in range(4):
        try:
            r = bc().invoke_model(modelId=EMBED, body=json.dumps({"inputText": text[:1800]}))
            return np.array(json.loads(r["body"].read())["embedding"], dtype=np.float32)
        except Exception:
            time.sleep(2 ** a)
    raise RuntimeError("embed fail")

texts = [f"{t['topic']}. {t['concept']}" for t in new_topics]
vecs = [None] * len(texts)
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    for f in as_completed([ex.submit(lambda i: (i, embed(texts[i])), i) for i in range(len(texts))]):
        i, v = f.result(); vecs[i] = v
V = np.vstack(vecs)
V = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
S = V @ V.T

# greedy clustering
n = len(new_topics)
assigned = [-1] * n
clusters = []
order = list(range(n))
for i in order:
    if assigned[i] != -1:
        continue
    cid = len(clusters)
    members = [i]
    assigned[i] = cid
    for j in range(n):
        if assigned[j] == -1 and S[i, j] >= MERGE_COS:
            assigned[j] = cid
            members.append(j)
    clusters.append(members)

print(f"{n} NEW topics -> {len(clusters)} candidate clusters (>= {MERGE_COS} cos)")

MERGE_SYS = (
    "You are an AWS DVA-C02 expert consolidating flashcard topics. Given several "
    "candidate topics that a similarity model grouped together, decide if they are "
    "the SAME testable concept (should become ONE card) or actually DISTINCT concepts "
    "(should stay separate). If they are the same, produce one canonical topic + concept "
    "that best captures it. Return STRICT JSON."
)

def resolve_cluster(members):
    if len(members) == 1:
        t = new_topics[members[0]]
        return [{"topic": t["topic"], "concept": t["concept"], "service": t["service"],
                 "questions": [t["question"]], "source_ids": [t["id"]]}]
    items = "\n".join(
        f"[{k+1}] Q{new_topics[m]['question']} ({new_topics[m]['service']}): "
        f"{new_topics[m]['topic']} -- {new_topics[m]['concept']}"
        for k, m in enumerate(members))
    msg = (
        f"CANDIDATE TOPICS grouped by similarity:\n{items}\n\n"
        'Return JSON: {"groups":[{"member_numbers":[..],"topic":"<canonical>",'
        '"concept":"<1-2 sentences>","service":"<service>"}]}\n'
        "Merge same-concept members into one group; split distinct ones into separate groups."
    )
    for a in range(4):
        try:
            r = bc().converse(modelId=CHAT, system=[{"text": MERGE_SYS}],
                              messages=[{"role": "user", "content": [{"text": msg}]}],
                              inferenceConfig={"maxTokens": 900, "temperature": 0})
            txt = r["output"]["message"]["content"][0]["text"].strip()
            txt = re.sub(r"^```(json)?|```$", "", txt, flags=re.M).strip()
            groups = json.loads(txt)["groups"]
            out = []
            for g in groups:
                mnums = [members[k-1] for k in g["member_numbers"] if 1 <= k <= len(members)]
                qs = sorted({new_topics[m]["question"] for m in mnums})
                ids = [new_topics[m]["id"] for m in mnums]
                out.append({"topic": g["topic"], "concept": g["concept"],
                            "service": g.get("service", ""), "questions": qs, "source_ids": ids})
            return out
        except Exception:
            time.sleep(2 ** a)
    # fallback: keep separate
    return [{"topic": new_topics[m]["topic"], "concept": new_topics[m]["concept"],
             "service": new_topics[m]["service"], "questions": [new_topics[m]["question"]],
             "source_ids": [new_topics[m]["id"]]} for m in members]

multi = [c for c in clusters if len(c) > 1]
print(f"resolving {len(multi)} multi-member clusters with LLM...")
canonical = []
with ThreadPoolExecutor(max_workers=MAXW) as ex:
    futs = [ex.submit(resolve_cluster, c) for c in clusters]
    for f in as_completed(futs):
        canonical.extend(f.result())

# sort by first question for stable ordering
canonical.sort(key=lambda c: (c["questions"][0], c["topic"]))
json.dump(canonical, open("kiro-test/consolidated_new.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"DONE: {len(new_topics)} NEW topics consolidated into {len(canonical)} canonical cards-to-build")
print("wrote kiro-test/consolidated_new.json")
