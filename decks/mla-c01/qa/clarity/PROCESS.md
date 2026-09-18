# Proceso de validacion de CLARIDAD (blind-solve multi-candidato) — MLA-C01

Diseñado por la investigacion v2-9497e8 (5 pares investigador-contrarian + juez).
Cuarta capa de QA, ORTOGONAL a la correccion tecnica (que ya cubrieron 3 rondas previas).
Proposito: encontrar mejoras de CLARIDAD y UNICIDAD-DE-RESPUESTA, no de correccion.

## Principio rector (del usuario)
Ponerse en los zapatos de quien responde: un candidato competente, viendo SOLO el enunciado
y las 4 opciones (SIN dorso, SIN fuente), debe poder elegir UNA respuesta con confianza y
justificarla con un criterio que este en el enunciado. Si el criterio decisivo solo vive en
el dorso, la carta falla (aunque su respuesta sea tecnicamente correcta).
NO se trata de hacer las preguntas mas faciles: una pregunta puede ser dificil y a la vez
clara y con una sola respuesta defendible. Estandar: producto entregable a clientes de pago.

## Regla dura (Claim 1 del juez)
Una mejora de claridad NUNCA cambia la respuesta correcta (correct_index) ni la dificultad
conceptual. Si un hallazgo implicaria cambiar la respuesta, NO es de claridad: es de
correccion y se deriva al gate de correccion, fuera de este proceso.

## Tecnica central: candidato en frio (blind-solve)
Se presenta a N candidatos LLM SOLO el enunciado + 4 opciones (texto plano, sin markup que
delate). Cada candidato elige una opcion, da confianza (1-5), marca un flag de ambiguedad si
aplica, justifica en una frase, y puntua una rubrica de 6 dimensiones (0-2 c/u).

Rubrica (0-2): self_contained, criterion_in_stem, unique_defensible, parallel_options,
no_backside_dependency, complete_scenario.

Flags: ok / ambiguous / missing_data / multiple_valid / vague_options.

## Consenso y veredicto (clarity_consolidate.py)
- agreement = fraccion de candidatos que eligieron la respuesta correcta (key).
- consensus = fraccion que eligio la opcion modal (sea o no la key).
- flag_rate = fraccion que marco cualquier flag != ok.
- rubric_min = peor rubrica sumada entre candidatos (0-12).
NEEDS_IMPROVEMENT si: agreement<0.75 O consensus<0.75 O flag_rate>=0.33 O rubric_min<9.
La CONFIANZA nunca bloquea un PASS (Dispute 2): una pregunta dificil-pero-clara pasa.
El consenso es key-INDEPENDIENTE: una carta que coincide con la key sigue NEEDS si es ambigua.

## Regla de FIX de dos senales (Dispute 4 - clave)
HARD FIX solo si S1 (rubrica del juez marca una dimension D=0) Y S2 (consenso blind roto:
agreement<2/3 O matches_key<2/3 O >=2 candidatos marcan multiple/missing/ambiguous).
Exactamente UNA senal = ADVISORY / revision humana. Cero = PASS.
"Criterio derivable del enunciado" (Dispute 6) se define empiricamente: si candidatos
independientes convergen en la key solo con el enunciado -> era derivable (bien); si se
dividen -> no lo era (defecto de claridad).

## Independencia de candidatos (Dispute 9 - limitacion)
Lo ideal: >=2 FAMILIAS de modelo distintas, votando una vez por familia. Si solo hay una
familia disponible (caso actual), es MODO DEGRADADO: S2 no puede hard-FIX sola; el resultado
es ADVISORY y requiere revision humana (mia) antes de aplicar cualquier cambio. Se declara
en el encabezado del run.

## Bucle de mejora
1. Prep: clarity_make_batches.py (o clarity_make_blind.py) -> blind_batches/ + answer_key.json
2. Blind-solve: N candidatos -> candidates/<cand>/batch_NN.jsonl
3. Consolidar: clarity_consolidate.py -> clarity_verdicts.json + clarity_report.md
4. Revisar NEEDS: aplicar mejora de claridad en el generador .py (reescribir enunciado para
   subir el criterio de decision al stem, completar datos faltantes, hacer opciones paralelas,
   quitar dependencia del dorso), SIN tocar correct_index.
5. Re-verificar: mcq-verify (el gate mecanico) debe seguir OK.
6. Re-validar: re-correr blind-solve SOLO sobre las cartas editadas (+ vecinas cuyo texto
   cambio) hasta que el consenso pase el umbral. Max 3 rondas.

## Estado de construccion (honesto, del juez)
- Front half (prep + blind-solve + consolidate + self-test): CONSTRUIDO y self-test PASA.
- Back half (judge -> merge -> re-verify automatico): la mejora se aplica manualmente por
  ahora (yo edito los generadores segun el reporte). Suficiente para ejecutar.
- Modo actual: candidatos de una sola familia => ADVISORY, con mi revision antes de aplicar.
