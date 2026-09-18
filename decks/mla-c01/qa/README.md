# qa/ — Aseguramiento de calidad del deck MLA-C01

Rastro completo del proceso de QA aplicado a las 112 cartas (2 decks) del examen
MLA-C01. El deck ya pasó todas las rondas; esto queda como documentación y como
pipeline reutilizable para futuros decks.

## Estructura

| Carpeta | Contenido |
|---|---|
| `scripts/` | Los scripts del pipeline (extracción, emparejamiento, loteo, consolidación). |
| `reports/` | Reportes legibles (.md) de cada ronda de QA. **Empieza por aquí.** |
| `data/` | Datos derivados: cartas extraídas, fixlists, reportes JSON, material fuente. |
| `clarity/` | Proceso de validación de CLARIDAD (blind-solve). Ver `clarity/README.md`. |

## Las rondas de QA (resumen en reports/)

1. **Corrección técnica** (`qa_report.md`, `qa2_report.md`, `qa3_report.md`):
   doble revisión con verificación contra docs AWS. Detectó y corrigió defectos de
   correccion (respuestas, alucinaciones, distractores también-correctos).
   Resumen final: `QA_FINAL_SUMMARY.md`.
2. **Claridad de examen** (`clarity/`): técnica "candidato en frío" (blind-solve
   multi-candidato) para detectar preguntas ambiguas o sin respuesta única.
   Ver `clarity/PROCESS.md` y `clarity/CLARITY_FINAL.md`.
3. **Delación por forma** (`clarity/giveaway/`): auditoría de opciones que se
   adivinan por su forma; corrigió 16 cartas subiendo la calidad de los distractores.

## Pipeline (scripts/)

El flujo original fue: `split_source.py` (parte el examen por dominio) →
`qa_extract.py` (extrae las cartas de los generadores a JSON) → `qa_pair.py`
(empareja cada carta con su pregunta fuente) → `qa_make_batches.py` (lotea) →
revisores LLM en paralelo → `qa_consolidate.py` (consolida veredictos).

NOTA: los scripts tenían rutas relativas a la ubicación original (`kiro-test/`).
Quedan como referencia del método; para re-ejecutar sobre un deck nuevo hay que
ajustar las rutas de entrada/salida.

## Material fuente
El examen original (Tutorials Dojo) está en `../notes/source/`. Los bloques ya
partidos por dominio están en `data/deck01_source.txt` y `data/deck02_source.txt`.
