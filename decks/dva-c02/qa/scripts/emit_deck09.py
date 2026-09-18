#!/usr/bin/env python3
"""Emit dva_c02_09.py generator file from kiro-test/generated_cards.json."""
import json

cards = json.load(open("kiro-test/generated_cards.json", encoding="utf-8"))

def pyrepr(s):
    return json.dumps(s, ensure_ascii=False)

lines = []
lines.append('#!/usr/bin/env python3')
lines.append('"""')
lines.append('DVA-C02::09 - Cards generated from examen_practica.txt (65-question official-style practice exam).')
lines.append('')
lines.append('Pipeline (see kiro-test/): parse 65 Qs -> extract 176 atomic topics via Bedrock Claude ->')
lines.append('dedup against existing 188 DVA-C02 cards using TWO layers (Titan embeddings similarity +')
lines.append('Claude LLM judgment) -> consolidate NEW topics among themselves (embeddings clustering +')
lines.append('LLM merge) -> 129 canonical gap topics -> one atomic MCQ card each (Claude, DECK_STANDARDS).')
lines.append('Each card key is dva09-<hash>. src_questions ties each card back to its exam question(s).')
lines.append('"""')
lines.append('from anki_mcq import card, create')
lines.append('')
lines.append('cards = [')
for c in cards:
    src = ",".join(str(q) for q in c["src_questions"])
    lines.append(f'    # src exam Q{src} | {c["service"]}: {c["topic"][:70]}')
    lines.append('    card(')
    lines.append(f'        question={pyrepr(c["question"])},')
    lines.append('        options=[')
    for o in c["options"]:
        lines.append(f'            {pyrepr(o)},')
    lines.append('        ],')
    lines.append(f'        correct={c["correct"]},')
    lines.append(f'        key={pyrepr(c["key"])},')
    lines.append(f'        answer={pyrepr(c["answer"])},')
    lines.append('    ),')
lines.append(']')
lines.append('')
lines.append('if __name__ == "__main__":')
lines.append('    create(deck_name="DVA-C02::09", cards=cards, out_path="out/DVA-C02_09.apkg")')
lines.append('')

open("dva_c02_09.py", "w", encoding="utf-8").write("\n".join(lines))
print(f"wrote dva_c02_09.py with {len(cards)} cards")
