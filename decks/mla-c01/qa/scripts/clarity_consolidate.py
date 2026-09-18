#!/usr/bin/env python3
"""Clarity-validation Phase C: consolidate N cold-candidate passes into a per-card
clarity verdict + prioritized fix list.

Inputs:
  kiro-test/clarity/answer_key.json                  (key -> correct_index/label)
  kiro-test/clarity/candidates/<CAND>/batch_NN.jsonl (one JSON line per card per candidate)

Each candidate line MUST be:
  {"key":"...","choice":"A|B|C|D|NONE","confidence":1-5,
   "flag":"ok|ambiguous|missing_data|multiple_valid|vague_options",
   "why":"one-sentence justification of the choice using ONLY stem+options",
   "rubric":{"self_contained":0-2,"criterion_in_stem":0-2,"unique_defensible":0-2,
             "parallel_options":0-2,"no_backside_dependency":0-2,"complete_scenario":0-2}}

Scoring:
  agreement       = fraction of candidates whose choice == answer_key choice
  consensus       = fraction of candidates who picked the modal choice (regardless of key)
  mean_confidence = mean confidence of candidates who chose the KEYED answer
  flag_rate       = fraction of candidates raising any non-"ok" flag
  rubric_min      = min across candidates of the summed rubric (0-12), i.e. worst reviewer

Verdict thresholds (see findings claims for rationale):
  NEEDS_IMPROVEMENT if ANY of:
     agreement < 0.75            (candidates do not converge on the keyed answer)
     consensus < 0.75            (candidates do not converge on ANY single option)
     flag_rate >= 0.33           (>=1/3 flagged ambiguity/missing data/multiple valid/vague)
     rubric_min <= 8             (a reviewer scored the card <=8/12 on clarity dims)
  else CLEAR.

Priority:
  P0 if agreement < 0.5 OR any candidate flag == multiple_valid with confidence>=4
  P1 if NEEDS_IMPROVEMENT and (agreement < 0.75 or flag_rate >= 0.5)
  P2 if NEEDS_IMPROVEMENT otherwise
  --  if CLEAR
"""
import collections
import json
import pathlib
import statistics
import sys

BASE = pathlib.Path(__file__).resolve().parents[1]
CL = BASE / "kiro-test" / "clarity"
CAND = CL / "candidates"

AGREE_MIN = 0.75
CONSENSUS_MIN = 0.75
FLAG_MAX = 0.33  # N=3: 1/3=0.333 >= 0.33 trips gate (1 dissenter is enough); N=5: >=2 flags
RUBRIC_MIN_OK = 9  # summed rubric must be >= 9/12 for every candidate to stay CLEAR
RUBRIC_DIMS = ["self_contained", "criterion_in_stem", "unique_defensible",
               "parallel_options", "no_backside_dependency", "complete_scenario"]


def load_candidates():
    """Return {key: [line, ...]} aggregated across candidate dirs."""
    by_key = collections.defaultdict(list)
    cand_dirs = sorted([d for d in CAND.glob("*") if d.is_dir()])
    for d in cand_dirs:
        for f in sorted(d.glob("batch_*.jsonl")):
            for ln in f.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                obj = json.loads(ln)
                obj["_candidate"] = d.name
                by_key[obj["key"]].append(obj)
    return by_key, [d.name for d in cand_dirs]


def verdict_for(key, lines, keyed_label):
    n = len(lines)
    choices = [l.get("choice", "NONE") for l in lines]
    agree = sum(1 for c in choices if c == keyed_label) / n
    modal, modal_n = collections.Counter(choices).most_common(1)[0]
    consensus = modal_n / n
    keyed_conf = [l.get("confidence", 0) for l in lines if l.get("choice") == keyed_label]
    mean_conf = statistics.mean(keyed_conf) if keyed_conf else 0
    flag_rate = sum(1 for l in lines if l.get("flag", "ok") != "ok") / n
    rubric_sums = []
    for l in lines:
        r = l.get("rubric", {})
        rubric_sums.append(sum(int(r.get(d, 0)) for d in RUBRIC_DIMS))
    rubric_min = min(rubric_sums) if rubric_sums else 0

    reasons = []
    if agree < AGREE_MIN:
        reasons.append(f"agreement {agree:.2f} < {AGREE_MIN}")
    if consensus < CONSENSUS_MIN:
        reasons.append(f"consensus {consensus:.2f} < {CONSENSUS_MIN}")
    if flag_rate >= FLAG_MAX:
        reasons.append(f"flag_rate {flag_rate:.2f} >= {FLAG_MAX}")
    if rubric_min < RUBRIC_MIN_OK:
        reasons.append(f"rubric_min {rubric_min} < {RUBRIC_MIN_OK}")

    needs = bool(reasons)
    multiple_valid_strong = any(
        l.get("flag") == "multiple_valid" and l.get("confidence", 0) >= 4 for l in lines)
    if not needs:
        prio = "--"
    elif agree < 0.5 or multiple_valid_strong:
        prio = "P0"
    elif agree < AGREE_MIN or flag_rate >= 0.5:
        prio = "P1"
    else:
        prio = "P2"

    return {
        "key": key,
        "verdict": "NEEDS_IMPROVEMENT" if needs else "CLEAR",
        "priority": prio,
        "n_candidates": n,
        "keyed_label": keyed_label,
        "agreement": round(agree, 3),
        "consensus_label": modal,
        "consensus": round(consensus, 3),
        "mean_conf_on_keyed": round(mean_conf, 2),
        "flag_rate": round(flag_rate, 3),
        "rubric_min": rubric_min,
        "flags": collections.Counter(l.get("flag", "ok") for l in lines),
        "reasons": reasons,
        "candidate_choices": {l["_candidate"]: l.get("choice") for l in lines},
    }


def main():
    if not CAND.exists():
        print(f"!! no existe {CAND} - corre primero las pasadas de candidato", flush=True)
        sys.exit(1)
    key_map = json.loads((CL / "answer_key.json").read_text(encoding="utf-8"))
    by_key, cand_names = load_candidates()
    print(f">> candidatos detectados: {cand_names}", flush=True)

    rows = []
    for key, meta in key_map.items():
        lines = by_key.get(key, [])
        if not lines:
            rows.append({"key": key, "verdict": "NO_DATA", "priority": "P?",
                         "reasons": ["ningun candidato respondio esta carta"]})
            continue
        rows.append(verdict_for(key, lines, meta["correct_label"]))

    # order: P0, P1, P2, NO_DATA, then CLEAR
    order = {"P0": 0, "P1": 1, "P2": 2, "P?": 3, "--": 9}
    rows.sort(key=lambda r: (order.get(r.get("priority", "--"), 9), -r.get("flag_rate", 0)))

    # Counter isn't JSON-serializable; coerce
    for r in rows:
        if isinstance(r.get("flags"), collections.Counter):
            r["flags"] = dict(r["flags"])

    (CL / "clarity_verdicts.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    needs = [r for r in rows if r["verdict"] == "NEEDS_IMPROVEMENT"]
    clear = [r for r in rows if r["verdict"] == "CLEAR"]
    nodata = [r for r in rows if r["verdict"] == "NO_DATA"]
    md = ["# Clarity verdicts", "",
          f"- candidatos: {len(cand_names)} ({', '.join(cand_names)})",
          f"- CLEAR: {len(clear)}",
          f"- NEEDS_IMPROVEMENT: {len(needs)} (P0={sum(1 for r in needs if r['priority']=='P0')}, "
          f"P1={sum(1 for r in needs if r['priority']=='P1')}, "
          f"P2={sum(1 for r in needs if r['priority']=='P2')})",
          f"- NO_DATA: {len(nodata)}", "",
          "## Necesitan mejora (prioridad desc)", "",
          "| key | prio | agree | consensus | flag_rate | rubric_min | motivos |",
          "|---|---|---|---|---|---|---|"]
    for r in needs:
        md.append(f"| {r['key']} | {r['priority']} | {r['agreement']} | "
                  f"{r['consensus']} ({r['consensus_label']}) | {r['flag_rate']} | "
                  f"{r['rubric_min']} | {'; '.join(r['reasons'])} |")
    (CL / "clarity_report.md").write_text("\n".join(md), encoding="utf-8")
    print(f">> escrito clarity_verdicts.json y clarity_report.md", flush=True)
    print(f">> CLEAR={len(clear)} NEEDS={len(needs)} NO_DATA={len(nodata)}", flush=True)


if __name__ == "__main__":
    main()
