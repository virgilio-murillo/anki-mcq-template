# MLA-C01 — AWS Certified Machine Learning Engineer Associate

Decks de Anki MCQ para el examen MLA-C01. 112 cartas en 2 subdecks, construidas
con el motor `anki_mcq` (mismo patron que `dva-c02`).

## Estructura

```
mla-c01/
├── mla_c01_01.py        # generador subdeck 01 (Data Preparation) — 56 cartas
├── mla_c01_02.py        # generador subdeck 02 (Modeling, Deployment & Ops) — 56 cartas
├── out/                 # .apkg generados (git-ignored, se regeneran)
├── notes/source/        # material fuente original (examen Tutorials Dojo)
├── study/               # tarjetas de estudio visuales (HTML) — ver study/README.md
└── qa/                  # rastro de aseguramiento de calidad — ver qa/README.md
```

## Subdecks

| Script | Anki deck | Cartas | Dominios |
|---|---|---|---|
| `mla_c01_01.py` | `MLA-C01::01 - Data Preparation` | 56 | Data Preparation (+ algo de Model Development) |
| `mla_c01_02.py` | `MLA-C01::02 - Modeling, Deployment & Ops` | 56 | Model Development + Deployment + Monitoring/Security |

## Regenerar y verificar

```bash
cd decks/mla-c01
../../.venv/bin/python mla_c01_01.py    # build -> verify (do_import=False)
../../.venv/bin/python mla_c01_02.py
../../.venv/bin/mcq-verify out/MLA-C01_01.apkg   # OK (0 problemas)
../../.venv/bin/mcq-verify out/MLA-C01_02.apkg
```

Para importar a Anki (con AnkiConnect corriendo), cambia `do_import=True` en el
`create(...)` o usa `mcq-import`.

## Calidad

Las 112 cartas pasaron 3 tipos de QA: correccion tecnica (verificada contra docs
AWS), claridad de examen (blind-solve), y anti-give-away (distractores plausibles).
El detalle completo esta en `qa/` (empieza por `qa/README.md` y `qa/reports/`).
