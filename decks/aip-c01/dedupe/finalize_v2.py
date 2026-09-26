#!/usr/bin/env python3
"""Consolida v2: aplica cascada cruzada sobre los verdicts HIBRIDOS y extrae las
NEW finales por examen (para regenerar solo lo que cambie).

Cascada: si una NEW aparece casi identica (TF-IDF sim>=0.6) en un examen posterior,
se conserva solo en el de menor numero (los 3 sets de Tutorials Dojo se solapan).

Salida: new_to_generate_v2_<tag>.json  (mismo formato que new_to_generate_<tag>.json)
"""
import json
import math
import pathlib
import re
from collections import Counter

DIR = pathlib.Path(__file__).resolve().parent
TAGS = ["exam1", "exam2", "exam3"]
THRESHOLD = 0.6
_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where will would can could should must may might not company team wants needs approach solution option options data model models using use used".split())


def toks(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def vecs(texts):
    tk = [toks(t) for t in texts]
    df = Counter()
    for x in tk:
        for w in set(x):
            df[w] += 1
    n = len(tk) or 1
    idf = {w: math.log((n + 1) / (c + 1)) + 1 for w, c in df.items()}
    out = []
    for x in tk:
        tf = Counter(x)
        v = {w: (1 + math.log(c)) * idf[w] for w, c in tf.items()}
        nrm = math.sqrt(sum(a * a for a in v.values())) or 1.0
        out.append({w: a / nrm for w, a in v.items()})
    return out


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def main():
    parsed = {t: {q["n"]: q for q in json.loads((DIR / f"parsed_{t}.json").read_text(encoding="utf-8"))}
              for t in TAGS}
    verd = {}
    concepts = {}
    for t in TAGS:
        vv, cc = {}, {}
        for line in (DIR / f"verdicts_hybrid_{t}.jsonl").read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                o = json.loads(line)
                vv[o["n"]] = o["verdict"]
                cc[o["n"]] = o.get("concepto", "")
        verd[t] = vv
        concepts[t] = cc

    # items NEW en orden exam1..3
    items = []
    for t in TAGS:
        for n, q in sorted(parsed[t].items()):
            if verd[t].get(n) == "NEW":
                correct = q["options"][q["correct_index"]]["text"]
                items.append((t, n, f"{q['stem']} {correct}"))
    V = vecs([it[2] for it in items])

    excluded = {t: [] for t in TAGS}
    kept = []
    for (t, n, _), v in zip(items, V):
        dup = None
        for (pt, pn, pv) in kept:
            if cos(v, pv) >= THRESHOLD:
                dup = (pt, pn, round(cos(v, pv), 3)); break
        if dup:
            excluded[t].append(n)
        else:
            kept.append((t, n, v))

    grand = 0
    for t in TAGS:
        excl = set(excluded[t])
        out = []
        for n, q in sorted(parsed[t].items()):
            if verd[t].get(n) == "NEW" and n not in excl:
                out.append({**q, "concepto": concepts[t].get(n, "")})
        (DIR / f"new_to_generate_v2_{t}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        grand += len(out)
        cov = sum(1 for x in verd[t].values() if x == "COVERED")
        print(f">> {t}: NEW_final={len(out)} (covered={cov}, dup_cruzado={len(excl)})", flush=True)
    print(f">> TOTAL v2 a generar: {grand}", flush=True)


if __name__ == "__main__":
    main()
