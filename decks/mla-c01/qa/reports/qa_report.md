# QA report MLA-C01 (revision LLM carta-por-carta)

- Esperadas: 112  |  Revisadas: 112
- P0 (respuesta incorrecta / distractor tambien-correcto / alucinacion): 0
- P1 (refutacion/conversion/coherencia/distractor med-high): 0
- P2 (didactica / cosmetico low): 7
- OK (impecables): 105


## P2 (7)

### mla01-q11  (score 5, PASS)
- [low] alucinaciones: El distractor 'Avro RecordIO' junta dos formatos (Avro y RecordIO), heredado de la fuente TD. No afecta la correccion de la respuesta.
    fix: Opcional: separar en 'Avro' a secas para evitar confusion.

### mla01-q29  (score 5, PASS)

### mla01-q32  (score 4, PASS)
- [low] calidad_distractores: Los distractores son soluciones tecnicamente funcionales; solo pierden por overhead. El criterio 'menor esfuerzo operativo' del enunciado los desambigua correctamente.
    fix: Mantener; el enunciado ya fuerza el criterio de minimo overhead que hace unica la respuesta.

### mla02-q20b  (score 4, PASS)
- [low] fidelidad_fuente: La carta reformula el escenario fuente (cuya respuesta oficial es serverless) en una pregunta conceptual distinta sobre Batch Transform.
    fix: Ninguno obligatorio; opcionalmente marcar explicitamente como carta de refuerzo tematico.

### mla02-q23  (score 4, PASS)
- [low] calidad_distractores: El argumento 'gateway endpoint no sirve cross-region' es una simplificacion del source; en rigor la limitacion es que el gateway solo cubre trafico intra-region hacia S3, coincide con la fuente.
    fix: Ninguno obligatorio; mantener alineado con la fuente TD.

### mla02-q24  (score 4, PASS)
- [low] calidad_distractores: La conversion a respuesta unica agrupa tres servicios por opcion, generando opciones largas; funciona pero exige leer con cuidado.
    fix: Ninguno obligatorio; el gate mecanico ya cubre balance de longitud.

### mla02-q37  (score 4, PASS)
- [low] calidad_distractores: El distractor 'adjuntar policy al role del notebook' es tecnicamente valido pero menos especifico; la distincion con la respuesta correcta es sutil (viene del propio source_block de TD).
    fix: Ninguno obligatorio; mantener la refutacion 'correcto pero menos especifico' tal como la da la fuente.
