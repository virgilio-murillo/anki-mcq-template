#!/usr/bin/env python3
"""Consolida los oficiales: cascada entre off1/off2 (no repetir entre sets) y
extrae las NEW con contenido completo para generar.

Salida: official_to_generate_off1.json / official_to_generate_off2.json
"""
import json
import math
import pathlib
import re
from collections import Counter

DIR = pathlib.Path(__file__).resolve().parent
TAGS = ["off1", "off2"]
TH = 0.6
_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
_STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where will would can could should must may might not company team wants needs approach solution option options data model models using use used".split())


def toks(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in _TOKEN.findall(s) if len(t.strip(".-")) >= 2 and t not in _STOP and not t.isdigit()]


def vecs(texts):
    tk = [toks(t) for t in texts]; df = Counter()
    for x in tk:
        for w in set(x): df[w] += 1
    n = len(tk) or 1; idf = {w: math.log((n+1)/(c+1))+1 for w, c in df.items()}
    out = []
    for x in tk:
        tf = Counter(x); v = {w: (1+math.log(c))*idf[w] for w, c in tf.items()}
        nn = math.sqrt(sum(a*a for a in v.values())) or 1.0; out.append({w: a/nn for w, a in v.items()})
    return out


def cos(a, b):
    if len(a) > len(b): a, b = b, a
    return sum(v*b.get(k, 0.0) for k, v in a.items())


def main():
    parsed = {t: {q["n"]: q for q in json.loads((DIR/f"parsed_{t}.json").read_text())} for t in TAGS}
    verd = {t: {json.loads(l)["n"]: json.loads(l) for l in (DIR/f"verdicts_official_{t}.jsonl").read_text().splitlines() if l.strip()} for t in TAGS}
    items = []
    for t in TAGS:
        for n, q in sorted(parsed[t].items()):
            if verd[t].get(n, {}).get("verdict") == "NEW":
                items.append((t, n, f"{q['stem']} {q['correct_text']}"))
    V = vecs([it[2] for it in items]); excl = {t: set() for t in TAGS}; kept = []
    for (t, n, _), v in zip(items, V):
        if any(cos(v, pv) >= TH for (_, _, pv) in kept):
            excl[t].add(n)
        else:
            kept.append((t, n, v))
    grand = 0
    for t in TAGS:
        out = []
        for n, q in sorted(parsed[t].items()):
            if verd[t].get(n, {}).get("verdict") == "NEW" and n not in excl[t]:
                out.append({**q, "concepto": verd[t][n].get("concepto", "")})
        (DIR/f"official_to_generate_{t}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        grand += len(out)
        print(f">> {t}: NEW_final={len(out)} (covered={sum(1 for x in verd[t].values() if x['verdict']=='COVERED')}, dup_cruzado={len(excl[t])})")
    print(f">> TOTAL oficial a generar: {grand}")


if __name__ == "__main__":
    main()
