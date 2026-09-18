# dedupe/ — Agregar un examen de práctica SIN repetir conceptos

Proceso reproducible para tomar un examen de práctica nuevo y crear un deck Anki
extra que contiene **solo los conceptos que aún no estudias** (deduplicado contra
todos los decks existentes). Diseñado por la investigación `v2-ec81d2`.

## Idea en una frase
Parsear el examen nuevo → volcar lo que ya tienes en Anki → un juez LLM decide, por
CONCEPTO (no por texto), qué preguntas son nuevas → generar un deck solo con esas →
pasar el QA de calidad → importar.

## Requisitos
- Anki abierto con AnkiConnect (localhost:8765) — para leer las cartas existentes.
- `.venv` del repo (matplotlib no hace falta aquí).

## Pasos

### 1-3. Automatizado
```bash
cd decks/mla-c01
../../.venv/bin/python dedupe/add_practice_exam.py --exam ../../practice_exam_N.txt --deck "MLA-C01::0X" --keyprefix mla0X
```
Produce: `new_exam_parsed.json` (limpias), `new_exam_quarantine.json` (multi-select /
matching / sin-opciones — el motor solo soporta 4 opciones y 1 correcta), 
`existing_cards.json` (universo de dedup), `new_concepts.json`, `existing_concepts.json`.

Ajusta la ruta del examen dentro de `parse_new_exam.py` si el formato difiere
(el parser actual espera el formato "Question / Answer options / Correct / Rationale").

### 4. Dedup por concepto (juez LLM)
Prepara los insumos compactos y lanza un agente juez:
```bash
../../.venv/bin/python -c "import json,pathlib; ex=json.load(open('dedupe/existing_concepts.json')); new=json.load(open('dedupe/new_concepts.json')); d=pathlib.Path('dedupe'); open(d/'existing_topics.txt','w').write('\n'.join(c['concept_text'][:180].replace(chr(10),' ') for c in ex)); open(d/'new_questions.txt','w').write('\n\n'.join(f\"Q{q['n']}: {q['stem'][:240]} || RESP: {q['correct_text'][:160]}\" for q in new))"
```
Lanza un sub-agente (internal-investigator) con este encargo:
> Experto MLA-C01 deduplicando temas a GRANULARIDAD DE EXAMEN. Lee
> `dedupe/existing_topics.txt` (lo que el alumno YA estudia) y `dedupe/new_questions.txt`.
> Para cada pregunta nueva decide COVERED (el objetivo examinable ya se enseña, aunque
> el ángulo sea distinto) o NEW (servicio/feature/objetivo no cubierto). Ante la duda:
> COVERED. Compara por CONCEPTO, no por idioma. Escribe `dedupe/dedup_verdicts.jsonl`:
> `{"n":N,"verdict":"COVERED|NEW","concepto":"...","razon":"..."}`

### 5. Generar el deck (developer-agent)
Extrae las NEW completas y lanza un developer-agent que cree `mla_c01_0X.py`:
```bash
../../.venv/bin/python -c "import json; v={json.loads(l)['n']:json.loads(l) for l in open('dedupe/dedup_verdicts.jsonl') if l.strip()}; p={q['n']:q for q in json.load(open('dedupe/new_exam_parsed.json'))}; new=[dict(p[n],concepto=v[n]['concepto']) for n in sorted(v) if v[n]['verdict']=='NEW']; json.dump(new,open('dedupe/new_to_generate.json','w'),ensure_ascii=False,indent=2); print(len(new),'NEW')"
```
El developer-agent traduce a español, respeta DECK_STANDARDS.md y **anti-give-away**
(distractores plausibles; la correcta no se delata por forma), 4 opciones, verdict
con `{{L}}`, keys `mla0X-qN`, y usa los `rationale` del examen para las refutaciones.

### 6. QA de calidad
Aplica los mismos gates del deck: corrección técnica (`qa/`) y claridad + anti-give-away
(`qa/clarity/PROCESS.md`). Corre `../../.venv/bin/mcq-verify out/MLA-C01_0X.apkg`.

### 7. Importar a Anki
Cambia `do_import=True` en el `create(...)` o usa `mcq-import`.

## Regla de oro de la deduplicación
Comparar por **concepto/objetivo examinable**, NO por texto literal. Si ya tienes una
carta que enseña el mismo servicio/mecanismo, la pregunta nueva es COVERED aunque el
enunciado sea distinto. Ante la duda razonable → COVERED (no repetir).

## Historial
- Examen 2 (`practice_exam_2.txt`): 65 preguntas → 57 estándar + 8 en cuarentena →
  dedup → 17 NEW → deck `MLA-C01::03` (`mla_c01_03.py`). 40 descartadas por ya estar cubiertas.
