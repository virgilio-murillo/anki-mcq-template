#!/usr/bin/env python3
"""Cascada ENTRE examenes: detecta preguntas casi-duplicadas entre exam1/2/3.

Los 3 examenes de practica se solapan entre si. Tras el juicio vs universo Anki,
si un mismo concepto aparece como NEW en mas de un examen, queremos generarlo UNA
sola vez, en el examen de MENOR numero (exam1 gana a exam2 gana a exam3).

Usa TF-IDF sobre (stem+respuesta) y marca como duplicada la pregunta de un examen
posterior cuyo par (stem,respuesta) sea muy similar a una NEW ya aceptada de un
examen anterior. Umbral alto (0.6) para no borrar conceptos distintos.

Salida: cross_dupes.json -> {tag: [ns duplicados a excluir]} y un log legible.
"""
import json
import math
import pathlib
import re
from collections import Counter

DIR = pathlib.Path(__file__).resolve().parent
TOKEN = re.compile(r"[a-z0-9][a-z0-9\-\.]*")
STOP = set("a an the of to in on for with and or is are be as by from at into that this these those which what when where will would can could should must may might not company team wants needs approach solution option options data model models using use used".split())
THRESHOLD = 0.6


def toks(s):
    s = re.sub(r"<[^>]+>", " ", (s or "")).lower()
    return [t.strip(".-") for t in TOKEN.findall(s)
            if len(t.strip(".-")) >= 2 and t not in STOP and not t.isdigit()]


def vecs(texts):
    tks = [toks(t) for t in texts]
    df = Counter()
    for x in tks:
        for w in set(x):
            df[w] += 1
    n = len(tks) or 1
    idf = {w: math.log((n + 1) / (c + 1)) + 1 for w, c in df.items()}
    out = []
    for x in tks:
        tf = Counter(x)
        v = {w: (1 + math.log(c)) * idf[w] for w, c in tf.items()}
        norm = math.sqrt(sum(a * a for a in v.values())) or 1.0
        out.append({w: a / norm for w, a in v.items()})
    return out


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(k, 0.0) for k, v in a.items())


def main():
    # cargar verdicts + parsed para armar "NEW por examen" con su texto
    tags = ["exam1", "exam2", "exam3"]
    parsed = {t: {q["n"]: q for q in json.loads((DIR / f"parsed_{t}.json").read_text(encoding="utf-8"))}
              for t in tags}
    verdicts = {}
    for t in tags:
        vf = DIR / f"dedup_verdicts_{t}.jsonl"
        vv = {}
        for line in vf.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                o = json.loads(line)
                vv[o["n"]] = o["verdict"]
        verdicts[t] = vv

    # lista global de NEW (en orden exam1, exam2, exam3) con texto concepto
    items = []  # (tag, n, text)
    for t in tags:
        for n, q in sorted(parsed[t].items()):
            if verdicts[t].get(n) == "NEW":
                correct = q["options"][q["correct_index"]]["text"]
                items.append((t, n, f"{q['stem']} {correct}"))

    V = vecs([it[2] for it in items])
    excluded = {t: [] for t in tags}
    kept_vecs = []  # (tag, n, vec)
    log = []
    for (t, n, _), v in zip(items, V):
        dup_of = None
        for (pt, pn, pv) in kept_vecs:
            if cos(v, pv) >= THRESHOLD:
                dup_of = (pt, pn, round(cos(v, pv), 3))
                break
        if dup_of:
            excluded[t].append(n)
            log.append(f"{t} Q{n} ~ {dup_of[0]} Q{dup_of[1]} (sim={dup_of[2]}) -> excluida de {t}")
        else:
            kept_vecs.append((t, n, v))

    (DIR / "cross_dupes.json").write_text(
        json.dumps(excluded, ensure_ascii=False, indent=2), encoding="utf-8")
    print(">> duplicados cruzados entre examenes (umbral %.2f):" % THRESHOLD, flush=True)
    for l in log:
        print("   " + l, flush=True)
    for t in tags:
        print(f">> {t}: {len(excluded[t])} excluidas por duplicado cruzado", flush=True)


if __name__ == "__main__":
    main()
