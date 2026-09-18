# Mejoras de CLARIDAD - 10 cartas MLA-C01

Reglas respetadas: correct_index sin cambios, key sin cambios, verdict/{{L}} intactos,
4 opciones, espanol + entidades HTML, sin em dashes. mcq-verify: OK (0 problemas) en ambos decks.

## PRIORIDAD ALTA

### mla02-q1 (correcta=A, FPR+F1) - enunciado
- Reescrito el enunciado para pedir explicitamente el par que (a) controla la tasa de
  falsos positivos Y (b) da un balance global precision-recall robusto al desbalance.
- Anadida la nota inline de que el "cut-off" es un umbral de decision, NO una metrica de
  evaluacion, para descartar D inequivocamente.
- Opciones sin cambios; dorso ya coherente (refuta cut-off como frontera, no metrica).

### mla02-q10 (correcta=A) - enunciado + opcion A (redaccion)
- Fuente (qa_cards_paired.json) confirma orden oficial: Step1 = crear bucket S3.
- Enunciado ahora dice explicitamente que los registros TODAVIA no estan en la nube
  (el bucket aun no existe) y que se arma desde cero, por lo que A (crear el bucket) es
  inequivocamente el primer paso; B (configurar KB) requiere que el bucket ya exista.
- Opcion A reformulada ("Crear el bucket... que alojara...") para reforzar el orden; sigue
  siendo A. Dorso ya consistente (orden 1-2-3).
- NO es defecto de correccion: la fuente marca A como el primer paso.

### mla02-q23 (correcta=A, interface endpoint + cross-region) - enunciado + dorso
- CASO DELICADO resuelto por claridad. La fuente especifica bucket en us-east-1 y
  SageMaker en us-west-2 (cross-region), dato que el enunciado antiguo OMITIA por completo,
  lo que empujaba a los candidatos a elegir gateway (correcto solo intra-region).
- Enunciado ahora hace el requisito cross-region EXPLICITO y prominente (us-east-1 vs
  us-west-2, "acceso privado entre regiones").
- Dorso actualizado: "El problema" y "Por que sirve" ahora giran en torno al cross-region;
  nueva seccion "Por que un gateway endpoint NO basta aqui" (intra-region, no alcanza otra
  region) y refutacion de gateway alineada.
- NO es defecto de correccion: con el cross-region explicito, A (interface + peering/TGW) es
  claramente la unica valida; el gateway (intra-region) no alcanza un bucket en otra region.

## PRIORIDAD MEDIA

### mla01-q6 (correcta=A) - enunciado
- Subido al enunciado que los formatos son MIXTOS en una sola carpeta y que DataBrew exige
  un unico formato/extension por dataset (no se puede procesar tal cual). A (separar por tipo)
  queda inequivoco frente a B (procesar la carpeta mixta). Opciones/dorso ya coherentes.

### mla01-q14 (correcta=A, scatter plot) - enunciado
- Reescrito para pedir "visualizar la RELACION entre DOS variables e identificar outliers",
  eliminando "fuerza de correlaciones entre features" (que sugeria matriz de correlacion/
  multicolinealidad). Apunta inequivocamente a scatter plot. Opciones/dorso sin cambios.

### mla01-q21c (correcta=A, TVD) - enunciado
- Reescrito para pedir "la distancia entre las distribuciones de resultados de dos grupos",
  evitando "maxima disparidad/divergencia" (que sugeria Kolmogorov-Smirnov). TVD es la unica
  distancia entre distribuciones de las opciones. Dorso (nota KL/KS) ya consistente.

### mla02-q29 (correcta=A, Precision/Recall/Accuracy/F1) - enunciado + dorso (refutacion B)
- Anadido al enunciado el criterio "cuarteto derivado de la matriz de confusion a un umbral
  fijo (no metricas que barren todos los umbrales como AUC-ROC)", haciendo UNICO el cuarteto A.
- Refutacion de B actualizada: AUC-ROC barre todos los umbrales, por eso queda fuera.

### mla02-q31b (correcta=A, "concept drift" es el intruso) - enunciado + opcion D + dorso
- Enunciado reformulado: lista los 4 tipos oficiales y pide el intruso ("cual NO es uno").
- Opcion D cambiada de "Bias drift y feature attribution drift" (bundle) a "Feature
  attribution drift" para que las 4 opciones sean PARALELAS (3 tipos reales + 1 intruso).
  correct_index sin cambios (A = concept drift sigue siendo la respuesta).
- Dorso: refutacion de D actualizada para reflejar la opcion unica (menciona que bias drift es
  el cuarto tipo oficial). Consistente.

### mla02-q38 (correcta=A, data quality drift) - enunciado
- Reescrito para que el sintoma sea inequivocamente un CAMBIO EN LA DISTRIBUCION DE LOS DATOS
  DE ENTRADA (nuevos perfiles demograficos, "aun sin ground truth para medir accuracy"),
  eliminando "pierde accuracy" como sintoma principal (que sugeria model quality drift).
- Dorso ya enfatizaba "distribucion estadistica de los datos de entrada" y refutaba model
  quality por requerir ground truth; ahora totalmente coherente.

## POSIBLES DEFECTOS DE CORRECCION
Ninguno. En los dos casos delicados (q10, q23) la fuente oficial confirma la respuesta actual
(A), y bastó con hacer explicito el criterio (orden real del flujo en q10; requisito
cross-region en q23) para que un candidato competente elija A con confianza.

## Verificacion
- correct_index sin cambios en las 10 (q25=B/idx1; resto A/idx0).
- key sin cambios en las 10.
- mcq-verify out/MLA-C01_01.apkg: OK (0 problemas)
- mcq-verify out/MLA-C01_02.apkg: OK (0 problemas)
