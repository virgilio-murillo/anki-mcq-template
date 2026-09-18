#!/usr/bin/env python3
"""
Parse examen_practica.txt into 65 structured questions.
The file format (as pasted) repeats blocks like:

  Question N            <- header (Q1 may lack the number)
  Multiple Choice / Multi-Select
  Time to answer: ...
  Answer status: ...
  Question
  <stem text ...>
  Answer options
  Option / Correct answer / Your selection / Rationale
  A. <option text> ... Correct/Not selected ... <rationale>
  ...

We split on the "Question <N>" / "Question" boundaries and, within each block,
capture: number, type, stem, and the raw options+rationale text. We do NOT try
to perfectly separate every option; the LLM will read the whole block. We only
need clean per-question chunks tied to their number.
"""
import re, json, sys

SRC = "examen_practica.txt"
raw = open(SRC, encoding="utf-8").read()

lines = raw.split("\n")

# Detect block starts.
# Q2..Q65 begin with a line "Question <N>" followed (within 3 lines) by a type marker.
# Q1 (special) begins at the very first standalone "Question" line (no number, no type
# marker) and its stem follows immediately.
block_starts = []
for i, ln in enumerate(lines):
    s = ln.strip()
    if re.match(r"^Question \d+$", s):
        look = "\n".join(lines[i+1:i+4])
        if "Multiple Choice" in look or "Multi-Select" in look:
            block_starts.append(("num", i))

# Q1: first standalone "Question" that is BEFORE the first numbered block start.
first_numbered = min([i for _, i in block_starts], default=len(lines))
for i, ln in enumerate(lines):
    if i >= first_numbered:
        break
    if ln.strip() == "Question":
        block_starts.append(("q1", i))
        break

# sort by line index
block_starts = sorted(block_starts, key=lambda t: t[1])
idxs = [i for _, i in block_starts]
idxs.append(len(lines))

questions = []
for k in range(len(block_starts)):
    kind, a = block_starts[k]
    b = idxs[k+1]
    chunk = "\n".join(lines[a:b]).strip()
    if kind == "q1":
        num = 1
    else:
        m = re.match(r"^Question (\d+)", chunk)
        num = int(m.group(1))
    qtype = "Multi-Select" if "Multi-Select" in chunk[:80] else "Multiple Choice"
    ao = chunk.find("Answer options")
    head = chunk[:ao] if ao != -1 else chunk
    hlines = head.split("\n")
    qlabel_idx = max([j for j, l in enumerate(hlines) if l.strip() == "Question"], default=-1)
    stem = "\n".join(hlines[qlabel_idx+1:]).strip() if qlabel_idx != -1 else head.strip()
    questions.append({
        "number": num,
        "type": qtype,
        "stem": stem,
        "full_block": chunk,
    })

questions.sort(key=lambda q: q["number"])

# sanity
print(f"Parsed {len(questions)} question blocks", file=sys.stderr)
nums = [q["number"] for q in questions]
print("numbers:", nums[:5], "...", nums[-5:], file=sys.stderr)
missing = sorted(set(range(1,66)) - set(nums))
if missing:
    print("WARNING missing numbers:", missing, file=sys.stderr)
dupes = sorted([n for n in set(nums) if nums.count(n)>1])
if dupes:
    print("WARNING duplicate numbers:", dupes, file=sys.stderr)

json.dump(questions, open("kiro-test/parsed_questions.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote kiro-test/parsed_questions.json ({len(questions)} questions)", file=sys.stderr)
