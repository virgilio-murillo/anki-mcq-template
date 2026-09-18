# QA2 report MLA-C01 (doble revision rigurosa con verificacion docs AWS)

- Revisadas A: 112/112  |  B: 112/112
- Desacuerdos A vs B: 29 (mla01-q12b, mla01-q13, mla01-q17, mla01-q1b, mla01-q21a, mla01-q21b, mla01-q21c, mla01-q25, mla01-q27, mla01-q29, mla01-q34, mla01-q36b, mla01-q38, mla01-q40, mla01-q41, mla01-q8, mla02-q20b, mla02-q25, mla02-q28, mla02-q29, mla02-q2b, mla02-q30, mla02-q31b, mla02-q33, mla02-q34, mla02-q41, mla02-q5, mla02-q5b, mla02-q7)
- P0=6 P1=35 P2=32 OK=39
- TOTAL a corregir (P0+P1+P2): 73


## P0 (6)

### mla01-q10  (A=FIX/3 B=FIX/3) [DISTRACTOR-TAMBIEN-CORRECTO]
- [med/A] conversion_multi_respuesta: Pregunta fuente 'Select TWO' de 5 opciones convertida a single-answer emparejando KDS+Flink. Funciona, pero la fuente subyacente descarta MSK con una justificacion tecnicamente incorrecta (MSK si hace streaming en tiempo real). Si en el futuro se reformula, no debe reforzarse la idea de que MSK 'no sirve para tiempo real'.
    fix: Mantener la respuesta pero, si se agrega nota sobre MSK, aclarar que MSK TAMBIEN puede ingerir/procesar en tiempo real; se elige KDS+Flink por ser el par canonico del escenario, no porque MSK sea batch.
- [high/B] calidad_distractores: MSK + Managed Service for Apache Flink es una pareja tambien-correcta para ingerir y procesar transacciones en tiempo real; presentarla como distractor unico incorrecto es cuestionable.
    fix: Reformular la opcion de MSK para que sea claramente inferior en el contexto (p.ej. 'Amazon MSK requiriendo autogestion de brokers/particiones y sin capa de procesamiento') o cambiar el enunciado para pedir explicitamente la opcion mas gestionada/serverless de baja operacion.
- [med/B] fidelidad_fuente: La refutacion afirma que MSK es 'principalmente para transferencia entre aplicaciones y no procesamiento en tiempo real', lo cual es incorrecto segun docs AWS.
    fix: Eliminar esa afirmacion; justificar el descarte de MSK por el requisito de minima operacion/servicio gestionado, no negando su capacidad de tiempo real.

### mla01-q24  (A=FIX/3 B=FIX/4) [DISTRACTOR-TAMBIEN-CORRECTO]
- [med/A] refutaciones_sustantivas: La refutacion del distractor 'bucket policy deniega' se basa en una distincion inexistente en S3 (conectar vs recuperar). Un Deny en bucket policy sobre s3:GetObject produce el mismo 403 al leer los .csv, por lo que ese distractor es defendible como tambien-correcto. La unicidad se sostiene solo por el 'most likely' del enunciado.
    fix: Reescribir la refutacion sin el argumento 'connect vs retrieve': explicar que un Deny explicito en bucket policy es posible pero menos comun en este escenario (normalmente el problema es que al role le falta s3:GetObject/ListBucket, o kms:Decrypt si hay CMK). Alternativamente, endurecer el enunciado indicando que 'no hay Deny en la bucket policy' para eliminar la ambiguedad.
- [med/B] refutaciones_sustantivas: La refutacion afirma que una bucket policy denegante haria fallar la conexion; en realidad una bucket policy puede permitir la conexion/ListBucket y denegar GetObject a nivel de objeto, causando el mismo 403. El motivo real de descarte es que es menos comun que un execution role sin permisos.
    fix: Reescribir: 'Una bucket policy con Deny explicito tambien podria causar 403, pero es menos frecuente que un execution role sin s3:GetObject; ademas requiere un Deny especifico. Por eso la causa mas probable es el execution role.'

### mla01-q32  (A=FIX/2 B=FIX/2) [DISTRACTOR-TAMBIEN-CORRECTO]
- respuesta_deberia_ser: Bajo documentacion AWS actual, la respuesta oficial de la fuente es cuestionable; la opcion tecnicamente correcta para redactar PII es Amazon Comprehend (opcion 'Convertir PDFs a texto y usar Comprehend'). La carta deberia reescribirse o retirarse.
- [high/A] correccion_tecnica: La respuesta 'correcta' asume que un modelo ready-to-use de SageMaker Canvas puede procesar PDFs y redactar PII/PHI. La lista oficial de Canvas no incluye tal modelo: 'Personal information detection' solo acepta texto/tabular y solo DETECTA (no redacta); los modelos que aceptan PDF no redactan PII.
    fix: Descartar o reescribir la carta. La solucion real de menor esfuerzo defendible es Comprehend (redaccion de PII via job asincrono) tras extraer texto, o combinar Textract+Comprehend. Como minimo, no afirmar una capacidad de Canvas que no existe.
- [high/A] alucinaciones: Afirmacion inventada/incorrecta sobre capacidades de SageMaker Canvas (redaccion de PII/PHI desde PDF).
    fix: Eliminar la afirmacion. Verificar contra docs Canvas ready-to-use models.
- [high/B] correccion_tecnica: Afirma que un modelo ready-to-use de SageMaker Canvas procesa PDFs y redacta PII/PHI directamente; los docs indican que el modelo de deteccion de informacion personal solo acepta texto/tabular y detecta (no redacta), y los modelos de documento (PDF) no redactan PII.
    fix: Recomponer la pregunta: la respuesta minima-overhead defendible tecnicamente es 'Amazon Textract para extraer texto de PDF + Amazon Comprehend para detectar y redactar PII/PHI' (Comprehend tiene API de redaccion de PII sobre texto). Alternativamente marcar la carta como fuente defectuosa y reescribir el escenario para que Comprehend/Textract sea la correcta.
- [high/B] calidad_distractores: El distractor Textract+JumpStart y el de Comprehend son enfoques tecnicamente validos para redactar PII, por lo que hay mas de una opcion defendible como correcta.
    fix: Eliminar la ambiguedad haciendo que la unica opcion correcta sea el pipeline Textract+Comprehend y convertir la de Canvas en distractor claramente descartable.

### mla02-q23  (A=FIX/3 B=FIX/2) [DISTRACTOR-TAMBIEN-CORRECTO]
- respuesta_deberia_ser: Deshabilitar el acceso directo a internet y crear un interface endpoint (PrivateLink) en la VPC hacia S3 (la LETRA sigue siendo la mejor de las 4, pero la justificacion del cross-region debe corregirse: requiere VPC peering/Transit Gateway, no solo el endpoint)
- [med/A] refutaciones_sustantivas: El razonamiento 'interface endpoint resuelve cross-region / gateway no' es tecnicamente impreciso: los interface endpoints cross-region para S3 son una capacidad reciente que exige vpce:AllowMultiRegion y DNS regional; el argumento real de por que gateway no sirve es que es intra-region y solo por tabla de rutas.
    fix: Precisar la refutacion: el interface endpoint (PrivateLink) da acceso privado por ENI y soporta S3 cross-region con configuracion (vpce:AllowMultiRegion); el gateway endpoint es intra-region y solo via ruta, por eso no cubre el escenario us-east-1 a us-west-2.
- [high/B] correccion_tecnica: El escenario y la respuesta implican que un interface VPC endpoint por si solo da acceso privado a un bucket S3 en OTRA region; docs.aws confirman que los endpoints S3 son regionales y que el acceso desde una VPC en otra region requiere VPC peering o Transit Gateway. La distincion 'gateway=misma region / interface=cross-region' es incorrecta (ambos son regionales).
    fix: Reencuadrar: el interface endpoint aporta acceso privado (via IP privada/ENI) evitando internet, y para llegar a S3 en otra region se combina con VPC peering/Transit Gateway. Corregir el tip y la refutacion del gateway explicando que ambos son regionales pero el interface admite acceso desde on-prem/otra VPC-region via peering/TGW.

### mla02-q37  (A=FIX/3 B=FIX/3) [DISTRACTOR-TAMBIEN-CORRECTO]
- [high/A] calidad_distractores: El distractor 'managed policy al role del notebook de Studio' es esencialmente correcto (mismo execution role del computo); la unica separacion es inline-vs-managed y 'dominio' vs 'notebook role', un matiz demasiado fino para una unica respuesta indiscutible.
    fix: Reemplazar ese distractor por uno claramente incorrecto (p.ej. 'resource-based policy en el bucket concediendo al usuario' o 'permisos via SCP') para que la inline-en-execution-role-del-dominio sea la unica opcion defendible; o convertir en pregunta conceptual sobre 'a que objeto se asignan los permisos del computo en Studio'.
- [high/B] calidad_distractores: El distractor 'Adjuntar una managed policy al role que usa el notebook de Studio' es tambien correcto si ese role es el execution role del dominio; la distincion inline vs managed no altera el ambito ni el aislamiento. La pregunta tiene dos opciones defendibles.
    fix: Reescribir el distractor debil para que sea claramente incorrecto (p.ej. 'adjuntar la policy a un role compartido por todos los dominios de Studio'), de modo que la unica correcta sea la del execution role del dominio especifico. Alternativamente, cambiar la clave de discriminacion a 'ambito del role' (dominio-especifico vs compartido) en vez de inline-vs-managed.
- [med/B] correccion_tecnica: El material sugiere que inline aisla mejor que managed; tecnicamente el aislamiento depende del role, no del tipo de policy.
    fix: Aclarar que lo relevante es adjuntar al execution role del dominio especifico; inline y managed son equivalentes en ambito.

### mla02-q38  (A=FIX/3 B=FIX/3) [DISTRACTOR-TAMBIEN-CORRECTO, OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: El escenario reproduce casi textualmente la definicion de la opcion correcta ('cambia la distribucion de los datos de entrada'), y el distractor 'concept drift' pertenece a otra taxonomia (no AWS Model Monitor), mezclando marcos.
    fix: Evitar repetir la definicion en el enunciado; usar distractores dentro de la taxonomia AWS (bias, feature attribution, model quality) y, si se incluye 'concept drift', aclarar que no es un tipo de Model Monitor de AWS.
- [med/B] calidad_distractores: 'Concept drift' es defendible como respuesta para 'cambios en demograficos y condiciones de pacientes'; el escenario no delimita si cambia la distribucion de entrada (data drift) o la relacion X->y (concept drift).
    fix: Reformular el enunciado para dejar claro que SOLO cambia la distribucion de los datos de entrada (no la relacion con la etiqueta), o reforzar la refutacion de concept drift explicando la diferencia (X->y constante vs cambiante).
- [min/B] correccion_tecnica: 'Data quality drift' es terminologia SageMaker; en ML estandar el shift de distribucion de entrada es 'data/covariate drift'.
    fix: Añadir una nota aclarando que 'data quality drift' es el termino de SageMaker Model Monitor para el cambio de distribucion de datos de entrada.


## P1 (35)

### mla01-q1  (A=FIX/3 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Estructura de opciones factorial que junto con la palabra clave 'terminos humanos' del enunciado hace la respuesta deducible sin razonar el trade-off. Defecto heredado del formato de la fuente.
    fix: Aceptable dado que replica la pregunta fuente, pero para robustez podria reformularse el enunciado para no repetir literalmente 'explicabilidad', obligando a razonar el mapeo requisito->criterio.
- [low/B] calidad_distractores: El fraseo del enunciado ('explicar en terminos humanos', 'transparencia y equidad') alinea semanticamente con la opcion correcta, permitiendo adivinar por coincidencia de palabras sin entender el trade-off.
    fix: Reformular el enunciado para no repetir literalmente 'explicabilidad'; p.ej. pedir 'justificar cada decision ante reguladores' y dejar que el alumno mapee eso a explicabilidad.

### mla01-q11  (A=FIX/3 B=FIX/4)
- [med/A] correccion_tecnica: El distractor 'Avro RecordIO' funde dos formatos distintos. Avro es un formato row-based de Apache; RecordIO (protobuf RecordIO) es el formato de registros de SageMaker. Presentarlos como un unico formato 'Avro RecordIO' es tecnicamente incorrecto y potencialmente confuso.
    fix: Separar en un distractor limpio: usar solo 'Avro (formato row-based con schema evolution)' o solo 'RecordIO (protobuf, orientado a registros para SageMaker)'; y que la refutacion nombre el formato real. Evitar el hibrido 'Avro RecordIO'.
- [low/B] calidad_distractores: 'Avro RecordIO' conflaciona dos formatos distintos; puede confundir a un alumno que conoce que RecordIO (protobuf/MXNet) no es lo mismo que Avro.
    fix: Renombrar el distractor a solo 'Avro' (row-based) o separar 'RecordIO-protobuf' como opcion propia, para no mezclar conceptos.

### mla01-q13  (A=PASS/4 B=FIX/3) [OPTIONS-ONLY-ADIVINABLE]
- [low/B] correccion_tecnica: El razonamiento asume que DTT elude la red del data center, pero DTT requiere transportar fisicamente los dispositivos a una instalacion AWS con fibra; para 'poca conectividad on-site' el mecanismo tipico es Snow Family (dispositivo enviado al cliente).
    fix: Anadir un matiz al enunciado (p.ej. 'la empresa puede transportar sus dispositivos a una instalacion AWS') o incluir Snow Family como opcion y precisar por que se prefiere DTT en el escenario dado.

### mla01-q1b  (A=PASS/4 B=FIX/3) [OPTIONS-ONLY-ADIVINABLE]
- [med/B] calidad_distractores: Tres distractores con absolutos (siempre/nunca/no hay diferencia) frente a una unica opcion matizada; el examinado detecta la correcta por el estilo hedged sin dominar el contenido.
    fix: Rehacer distractores con afirmaciones plausibles y especificas (p.ej. 'el complejo siempre es preferible si hay GPU disponible', 'la interpretabilidad no afecta la eleccion en banca') que exijan conocimiento real para descartar.

### mla01-q21a  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: El enunciado y la definicion embebida en la opcion correcta comparten frase casi identica ('proporcion de resultados positivos entre grupos'), permitiendo emparejar por coincidencia lexica sin dominar las metricas. Afecta a las tres cartas de la serie (q21a/b/c).
    fix: Quitar (o reformular) la definicion embebida en las opciones, dejando solo el nombre de la metrica (DPL/CI/TVD/KL), o parafrasear el enunciado para que no reutilice la misma frase que la definicion de la opcion correcta. Asi se obliga a conocer que hace cada metrica.

### mla01-q21b  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Mismo defecto de give-away lexico que q21a: la definicion embebida en la opcion CI parafrasea el enunciado, permitiendo acierto por coincidencia de palabras.
    fix: Igual que q21a: dejar solo el nombre de la metrica en las opciones o parafrasear el enunciado para romper el eco lexico.

### mla01-q21c  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Give-away lexico: la definicion embebida en la opcion TVD parafrasea el enunciado ('maxima disparidad/divergencia'), permitiendo acierto por coincidencia de palabras sin dominar las metricas. Consistente con q21a/b.
    fix: Dejar solo el nombre de la metrica en las opciones o reformular el enunciado para no reutilizar 'maxima divergencia/disparidad'. Se conserva el excelente matiz KL en la refutacion.

### mla01-q25  (A=PASS/5 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/B] calidad_distractores: Match lexico: 'etiquetar' en el stem apunta directo a 'labeling job'; el examinado acierta sin evaluar NTM/CNN/Comprehend.
    fix: Reformular el stem evitando la palabra 'etiquetar/labeling' literal (p.ej. 'preparar anotaciones supervisadas de alta calidad') para forzar el razonamiento.

### mla01-q27  (A=FIX/4 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Adivinable por options-only: correcta es la unica opcion 'DMS administrado' sin bandera negativa; distractores con senales obvias (equipo fisico, script fragil, complejidad innecesaria).
    fix: Hacer que un distractor use tambien DMS de forma neutral (p.ej. 'DMS heterogenea con Schema Conversion Tool') para forzar discriminar homogenea vs heterogenea en vez de detectar la bandera roja.
- [med/A] refutaciones_sustantivas: La refutacion de la opcion CDC/ongoing invoca 'el escenario pide migrar una vez', premisa ausente del enunciado de la carta.
    fix: Anadir al enunciado que es una migracion puntual/one-time, o refutar CDC por 'anade complejidad de sincronizacion continua no requerida para un dataset de entrenamiento estatico'.

### mla01-q28  (A=FIX/4 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: El distractor 'KMS cifrar y comprimir' es el unico que no es un servicio de transferencia de datos y ademas atribuye compresion a KMS (falso), haciendolo eliminable de inmediato y bajando la calidad del set.
    fix: Reemplazar por un distractor de transferencia plausible, p.ej. 'Usar Amazon CloudFront con upload via distribucion' o 'subir con multipart upload estandar sin acelerar', que exijan discriminar de verdad frente a Transfer Acceleration.
- [med/B] calidad_distractores: El distractor de KMS mezcla cifrado+compresion (KMS no comprime) resultando en una opcion no plausible/descartable a simple vista; el resto son geograficamente/operativamente ajenos, haciendo la correcta adivinable.
    fix: Sustituir el distractor KMS por uno plausible del dominio de transferencia (p.ej. DataSync por red, o Snowball) que exija razonar 'minimo cambio de setup'.

### mla01-q29  (A=FIX/3 B=PASS/5)
- [med/A] fidelidad_fuente: La carta reemplaza el distractor fuente 'Z-score normalization' por 'Min-Max Scaler'. Aunque tecnicamente correcto y mejora la calidad (Z-score y Standard Scaler son la misma tecnica = redundancia en la fuente), es una desviacion de las opciones oficiales sin documentar.
    fix: Documentar la sustitucion (nota de que se elimino la redundancia Standard/Z-score), o mantener las 4 opciones fuente si el objetivo es fidelidad estricta. Como esta, aceptable pero debe registrarse la alteracion.

### mla01-q34  (A=PASS/5 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/B] calidad_distractores: Solo la opcion correcta menciona un motor de analitica de streaming (Flink); las demas emparejan servicios claramente de reposo/lotes/entrenamiento, permitiendo adivinar por eliminacion sin dominar el tema.
    fix: Fortalecer un distractor con un par plausible de tiempo real (p.ej. 'Kinesis Data Streams + Lambda con Kinesis Data Analytics deprecado' o 'KDS + OpenSearch') para que la eleccion exija distinguir capacidades reales de analitica.

### mla01-q36b  (A=PASS/5 B=FIX/3)
- [med/B] correccion_tecnica: Se aplica DPL (metrica sobre etiquetas observadas, pre-training) a 'tasas de churn PREDICHAS'; la metrica correcta para predicciones es DPPL. Desajuste label-vs-prediction heredado de la fuente.
    fix: Reformular el stem para hablar de 'desbalance en la proporcion de ETIQUETAS/casos positivos entre grupos en los datos' (que es lo que mide DPL), o aclarar en el answer_html que DPL es pre-entrenamiento sobre labels (y mencionar que DPPL es su analogo sobre predicciones).

### mla01-q37  (A=FIX/4 B=FIX/3) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] fidelidad_fuente: La carta reemplaza el distractor fuente 'Kendall's Tau' por 'Chi-cuadrado (prueba de independencia)'. Es una mejora (Kendall's Tau tambien mide asociacion monotona y era semi-correcto), pero es una alteracion del conjunto oficial sin nota.
    fix: Documentar la sustitucion (motivo: Kendall's Tau era distractor also-correct por medir asociacion monotona). Alternativa fiel: mantener Kendall's Tau pero entonces el enunciado debe distinguir explicitamente por que Spearman > Kendall (tamano de muestra/uso), como hace el propio source.
- [med/B] calidad_distractores: Se elimino el distractor mas fuerte (Kendall's Tau, tambien monotono no-parametrico) y se puso Chi-cuadrado (categorico). Ahora Spearman es la unica opcion de correlacion monotona numerica y se adivina por eliminacion.
    fix: Restaurar 'Kendall's Tau' como cuarta opcion (distractor fuerte) y explicar por que Spearman es preferible (Kendall se usa mas con muestras pequenas/datos ordinales), tal como hace la fuente original.

### mla01-q4  (A=FIX/3 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Distractores redundantes: 'produccion siempre consistente' y 'produccion no difiere con el tiempo' son la misma idea; sumado al patron 1-contra-3, la correcta es adivinable sin leer el enunciado. Heredado de la fuente pero corregible.
    fix: Reemplazar uno de los dos distractores de 'no drift' por uno cualitativamente distinto, p.ej. 'basta con reentrenar una sola vez al detectar el primer error' o 'el drift se corrige subiendo la tasa de aprendizaje sin nuevos datos', para romper la redundancia y el patron 1-contra-3.
- [low/B] calidad_distractores: Dos de los cuatro distractores son parafrasis del mismo error (produccion == entrenamiento), reduciendo la dificultad; el alumno descarta ambos de golpe.
    fix: Sustituir uno de los dos por un distractor plausible pero distinto, p.ej. 'basta monitorear metricas de negocio sin reentrenar' o 'el reentrenamiento solo es necesario si cambia el esquema de features'.

### mla01-q40  (A=PASS/5 B=FIX/3) [OPTIONS-ONLY-ADIVINABLE]
- [med/B] calidad_distractores: Los distractores son afirmaciones categoricamente falsas sobre Bedrock; la unica opcion verdadera es la correcta, adivinable sin conocimiento (patron 'la que suena bien').
    fix: Convertir al menos un distractor en un beneficio real pero NO pedido (p.ej. 'ofrece APIs distintas por FM' como en la fuente) para forzar a distinguir cual par de beneficios responde al requisito, no cual afirmacion es verdadera.
- [low/B] fidelidad_fuente: El stem introduce 'privacidad de los datos' como requisito, mientras la fuente descarto la opcion de privacidad por no ser el foco del escenario.
    fix: Alinear el stem con la logica de la fuente (enfatizar 'elegir entre modelos de terceros' y 'fine-tune') sin sobre-enfatizar privacidad, o aceptar privacidad y ajustar la explicacion.

### mla01-q41  (A=PASS/5 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [low/B] calidad_distractores: Dos de tres distractores (Comprehend Medical, Rekognition) son de dominio ajeno y triviales de descartar; la pregunta se reduce a Bedrock vs SageMaker Studio.
    fix: Sustituir uno de los distractores ajenos por una opcion generativa/administrada mas cercana (p.ej. 'SageMaker JumpStart') para exigir distinguir 'elegir/fine-tune FMs sin infra' con mayor finura.

### mla01-q5  (A=FIX/3 B=FIX/4)
- [med/A] refutaciones_sustantivas: Refutar QuickSight diciendo que 'no es de prediccion de ML' es tecnicamente incorrecto: QuickSight ofrece forecasting ML integrado. La verdadera razon para descartarlo es que no realiza la preparacion/limpieza de datos (timestamps irregulares, faltantes) con el menor overhead.
    fix: Cambiar la refutacion a: 'QuickSight es una herramienta de BI; aunque tiene forecasting ML basico, no esta pensada para limpiar/imputar timestamps irregulares y faltantes, que es el nucleo del requisito; Data Wrangler lo hace con menor overhead.'
- [low/B] refutaciones_sustantivas: La refutacion insinua que QuickSight no hace forecasting; QuickSight ML Insights si lo hace. El eje de descarte real es que no es herramienta de preparacion/limpieza de datos.
    fix: Reescribir la refutacion de QuickSight: 'QuickSight es BI/visualizacion (incluso con forecasting ML Insights), pero no esta pensado para limpiar timestamps irregulares ni imputar faltantes, que es el requisito central.'

### mla02-q1  (A=FIX/3 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] correccion_tecnica: Afirma que 'minimizar FPR cumple el requisito de minimizar falsos positivos'; en un dataset con 3% de positivos el FPR es poco sensible a los FP (denominador = negativos reales, muy grande), mientras que Precision es la metrica directa. Imprecision heredada de TutorialsDojo pero no corregida.
    fix: Anadir en la explicacion que Precision es la metrica que mide directamente el costo de falsos positivos y que el F1 la incorpora; aclarar que el FPR es complementario pero menos sensible en desbalance extremo.
- [med/B] calidad_distractores: Adivinable por eliminacion: RMSE (x2) y cut-off marcan sus opciones como no-clasificacion, dejando solo A como par valido de clasificacion.
    fix: Sustituir al menos un distractor por un par plausible de clasificacion (ej. 'Precision y Accuracy global' o 'Recall y Accuracy') para forzar razonamiento sobre desbalanceo en vez de descarte por RMSE.

### mla02-q20  (A=FIX/3 B=FIX/3)
- [med/A] correccion_tecnica: La carta afirma que 'el modelo de 2 GB excede los limites de despliegue de Lambda'. Verificado contra docs de limites de Lambda: la imagen de contenedor admite hasta 10 GB y /tmp hasta 10 GB (solo el ZIP se limita a 250 MB descomprimido). Un modelo de 2 GB no excede esos limites.
    fix: Reemplazar el motivo por el real: Lambda no es la mejor opcion porque no es un servicio de inferencia ML administrado, sufre cold starts, tiene timeout de 15 min y cargar un modelo de 2 GB desde S3 en cada invocacion es ineficiente; NO porque el tamano exceda el limite (con imagen de contenedor Lambda admite hasta 10 GB).
- [med/B] refutaciones_sustantivas: La refutacion 'el modelo de 2 GB excede los limites de despliegue de Lambda' es incorrecta: Lambda con imagen de contenedor soporta hasta 10 GB (verificado en docs de limites de Lambda); 2 GB cabe. Solo excede el limite de .zip (250 MB descomprimido).
    fix: Reescribir la refutacion: descartar Lambda porque cargar un modelo de 2 GB desde S3 en CADA invocacion es impractico (arranque en frio prolongado, latencia alta, cobro por duracion) y Lambda no es la opcion 'fully managed' de inferencia de SageMaker que pide el enunciado; NO por un limite de tamano de despliegue.

### mla02-q20b  (A=PASS/4 B=FIX/3) [OPTIONS-ONLY-ADIVINABLE]
- [med/B] fidelidad_fuente: El source_block citado corresponde a una pregunta cuya respuesta oficial es Serverless Inference (no Batch Transform); la carta reencuadra el tema sin evidencia directa en el bloque.
    fix: Sustituir el source_block por la pregunta/explicacion fuente que realmente trate Batch Transform (p.ej. la de q25), o marcar la carta como refuerzo_tematico con source null.
- [min/B] calidad_distractores: Correcta adivinable por forma (unica que describe lote programado sin endpoint).
    fix: Endurecer un distractor para que tambien mencione 'sin endpoint' o 'programado' y forzar discriminacion conceptual real.

### mla02-q21  (A=FIX/3 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La respuesta correcta es adivinable solo mirando opciones: es la unica accion 'inicial/fundacional'; las demas presuponen un feature group existente o son claramente de inferencia.
    fix: Reformular distractores para que compitan como posibles 'primeros pasos' plausibles (p.ej. 'Definir el schema de los records', 'Crear el feature group', 'Registrar los features en el catalogo'), o cambiar el enunciado para preguntar por la funcion del feature group en vez de 'primer paso'.
- [min/B] calidad_distractores: La correcta se adivina por ser la unica accion 'inicial'; los distractores delatan que son pasos posteriores.
    fix: Reformular distractores para que suenen igualmente iniciales (p.ej. 'Definir el schema del offline store') sin delatar orden.

### mla02-q23b  (A=FIX/3 B=FIX/3) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Tres distractores contienen afirmaciones claramente invertidas o absurdas (gateway con ENI, gateway cross-region nativo, 'identicos salvo precio con interface gratis'), haciendo la correcta adivinable por eliminacion sin conocer el tema.
    fix: Sustituir por distractores mas sutiles y parcialmente verdaderos (p.ej. 'el interface tambien es gratis y va por tabla de rutas', 'el gateway soporta cualquier servicio dentro de la VPC') para exigir conocimiento real.
- [med/B] correccion_tecnica: El exam tip y el encuadre sugieren que la diferencia gateway/interface es 'misma region vs cross-region'. Segun docs.aws ambos endpoints de S3 son regionales; el interface solo admite acceso desde on-prem o desde una VPC en otra region via peering/TGW.
    fix: Ajustar tip: 'Gateway = ruta, gratis, S3/DynamoDB, IPs publicas de S3, sin on-prem. Interface = ENI/PrivateLink, IP privada, muchos servicios, admite on-prem y otra VPC-region via peering/TGW.' Evitar decir que el interface es 'cross-region' a secas.

### mla02-q28  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La correcta es adivinable por coincidencia lexica: 'pipeline completo' en el enunciado <-> 'CodePipeline'. No exige entender la diferencia real de orquestacion vs build/deploy.
    fix: Evitar el termino 'pipeline' en el enunciado (p.ej. 'coordinar automaticamente las fases build->test->deploy en cada cambio de codigo') y/o incluir un distractor de orquestacion real como 'AWS Step Functions' para forzar discriminacion conceptual.

### mla02-q29  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La correcta es adivinable por eliminacion: es el unico cuarteto sin RMSE ni ROUGE (metricas obviamente de otro dominio). No fuerza a razonar cuales metricas aplican a clasificacion binaria.
    fix: Usar distractores que solo mezclen metricas de clasificacion entre si con un solo intruso sutil, o incluir metricas de clasificacion tambien validas pero no pedidas (AUC, especificidad) para exigir discriminacion mas fina.

### mla02-q2b  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: El enunciado usa 'segmentar cada pixel' y la unica opcion con 'cada pixel' es la correcta: adivinable solo por coincidencia lexica (options-only).
    fix: Reformular el enunciado para NO usar 'cada pixel' (ej. 'asignar una categoria a nivel de pixel a toda la escena') o quitar la frase 'clasifica cada pixel' del texto de la opcion correcta para eliminar el eco.

### mla02-q30  (A=PASS/5 B=FIX/4)
- [med/B] correccion_tecnica: El permiso descrito (kms:Encrypt + kms:Decrypt) es impreciso para el caso de LECTURA de datos de entrenamiento: docs.aws indican que descargar objetos SSE-KMS requiere kms:Decrypt (y GenerateDataKey para subir/escribir). kms:Encrypt no habilita la lectura.
    fix: Precisar: el execution role necesita kms:Decrypt para leer los datos cifrados SSE-KMS (y kms:GenerateDataKey si tambien escribe salida cifrada). Mantener la LETRA correcta pero corregir el detalle de permisos en verdict/definicion.

### mla02-q31b  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La intrusa correcta ('latency drift') se identifica por ser el unico concepto de sistema/red entre tres tipos de calidad/sesgo, sin necesidad de conocer los 4 tipos reales.
    fix: Usar como intrusa un termino que suene a Model Monitor pero no lo sea (p.ej. 'concept drift' o 'schema drift'), que compita en registro con los tres verdaderos y exija conocer la lista exacta.

### mla02-q33  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La correcta es adivinable por coincidencia lexica: 'consultar/analizar logs' <-> 'CloudWatch Logs Insights' (unico con 'Logs' en el nombre).
    fix: Anadir un distractor con 'log' en el nombre o concepto (p.ej. 'Amazon OpenSearch Service' o 'CloudWatch Logs (sin Insights)') para forzar discriminacion mas alla del keyword; o reformular el enunciado sin la palabra 'logs'.

### mla02-q34  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: Dos de los tres distractores (Trusted Advisor, Secrets Manager) son de dominios muy alejados de logging/auditoria, reduciendo la pregunta a CloudTrail vs Config y facilitando el acierto por eliminacion.
    fix: Reemplazar Trusted Advisor y Secrets Manager por servicios que tambien registran/observan actividad (p.ej. Amazon CloudWatch Logs, AWS CloudTrail Lake, Amazon Macie, VPC Flow Logs) para forzar discriminacion entre opciones de observabilidad/seguridad.

### mla02-q35  (A=FIX/3 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La correcta se adivina por ser la unica accion inicial (las demas presuponen tags existentes). Ademas, la distincion 'crear' vs 'adjuntar' tags no refleja el flujo real de AWS (los user-defined tags nacen al aplicarse).
    fix: Reformular a una pregunta conceptual (p.ej. 'que se requiere para que un tag aparezca en los reportes de costos?' -> activarlo en Billing) o alinear los pasos con el flujo real AWS (etiquetar recursos -> activar en Billing) evitando el paso ficticio de 'crear tag' separado.
- [min/B] calidad_distractores: La correcta se adivina por ser la unica accion 'inicial'; los distractores delatan orden.
    fix: Reformular distractores para que no revelen su posicion en la secuencia (evitar 'habilitar/adjuntar' explicitos).
- [min/B] conversion_multi_respuesta: El paso 'crear user-defined tags' separado de 'adjuntarlos' es artificial en AWS (un tag se crea al aplicarlo).
    fix: Aclarar en la explicacion que 'crear' aqui significa definir el esquema clave-valor a usar antes de aplicarlo, para evitar la impresion de una API de 'crear tag' independiente.

### mla02-q39  (A=FIX/3 B=FIX/4) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: La correcta se identifica por antonimia: 'baja latencia/tiempo real' vs distractores 'batch' e 'intervalos'. El examinado descarta batch por definicion sin razonar el monitoreo.
    fix: Sustituir los dos distractores 'batch' por opciones que tambien sean real-time pero subóptimas (p.ej. 'CloudWatch alarms sobre latencia', 'sampling parcial del trafico'), evitando que 'batch' delate por antonimia.
- [min/B] calidad_distractores: Dos distractores basados en batch (continuo-con-batch y on-schedule-batch) son casi redundantes, permitiendo descartarlos como grupo.
    fix: Sustituir uno por un distractor de otra naturaleza (p.ej. 'usar solo alarmas de CloudWatch sobre latencia') para diversificar la discriminacion.

### mla02-q41  (A=FIX/3 B=PASS/5)
- [med/A] refutaciones_sustantivas: La refutacion de Bedrock se apoya en una premisa desactualizada (Bedrock no analiza/modera imagenes). Bedrock Guardrails ya incluye un filtro de contenido de imagenes daninas (ApplyGuardrail).
    fix: Reescribir el descarte de Bedrock: reconocer que Bedrock Guardrails puede filtrar imagenes, pero Rekognition Content Moderation es la opcion de MINIMO esfuerzo por ser una API de moderacion lista y purpose-built para deteccion de contenido inapropiado.

### mla02-q5  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: El enunciado ('datos categoricos, conteos por categoria') y la opcion correcta comparten las palabras clave 'categoricos'/'conteos', haciendola adivinable solo por lexico.
    fix: Quitar la aclaracion parentetica del enunciado (dejar solo 'frecuencia de compra de distintos articulos en un periodo') y/o eliminar 'ideal para datos categoricos con conteos' del texto de la opcion correcta.

### mla02-q5b  (A=FIX/3 B=PASS/5) [OPTIONS-ONLY-ADIVINABLE]
- [med/A] calidad_distractores: El enunciado ('rango continuo') y la opcion correcta ('valores continuos en bins') comparten 'continuo'; adivinable por coincidencia lexica.
    fix: Reformular el enunciado sin la palabra 'continuo' (ej. 'ver como se reparten los montos de transaccion') o quitar 'valores continuos' del texto de la opcion correcta.


## P2 (32)

### mla01-q12b  (A=PASS/4 B=FIX/4)
- [low/B] correccion_tecnica: El enunciado dice 'en tiempo real' pero Firehose entrega en NEAR real-time por su buffering; podria inducir confusion frente a KDS.
    fix: Cambiar 'en tiempo real' por 'streaming near real-time' o 'de forma continua/administrada' para ser tecnicamente exacto.

### mla01-q15  (A=PASS/4 B=PASS/5)

### mla01-q17  (A=PASS/5 B=FIX/4)
- [low/B] refutaciones_sustantivas: La refutacion de compresion afirma que no mejora performance/latencia; comprimir reduce bytes por registro y puede mejorar el throughput efectivo bajo el limite de 1MB/s por shard (aunque no bajo el limite de 1000 rec/s).
    fix: Precisar: 'la compresion puede aliviar el limite de bytes por shard pero no el de registros/s ni el numero de shards, por eso no resuelve el cuello de forma general; anadir shards es la solucion directa.'

### mla01-q18  (A=PASS/4 B=PASS/5)

### mla01-q20  (A=PASS/4 B=PASS/5)

### mla01-q30  (A=FIX/4 B=FIX/4)
- [low/A] didactica: El enunciado usa 'seq2seq' asociado a un modelo de recomendacion (heredado de la fuente). Seq2seq es para traduccion/resumen; asociarlo a recomendacion es impreciso y potencialmente confuso.
    fix: Neutralizar el enunciado a 'algoritmo built-in de SageMaker que usa Pipe mode / RecordIO-Protobuf' sin afirmar que seq2seq es para recomendacion, o cambiar el ejemplo de algoritmo.
- [low/B] didactica: El exam tip implica que Spark produce RecordIO-Protobuf de forma directa; en realidad exige codigo/protobuf custom sobre el cluster EMR.
    fix: Matizar el tip: 'EMR/Spark procesa a escala y, con la libreria protobuf instalada, serializa a RecordIO-Protobuf' para no sugerir soporte nativo.

### mla01-q38  (A=FIX/4 B=PASS/4)
- [low/A] didactica: El enunciado usa 'data drift' de forma generica (heredado del source, que confunde bias drift con data drift). La carta corrige el cuerpo, pero el enunciado y el titulo de la opcion siguen sugiriendo que Clarify 'monitorea data drift', cuando la deriva de calidad de datos es de Model Monitor.
    fix: Ajustar el enunciado a 'evaluar/mitigar sesgo y vigilar la DERIVA DE SESGO' y, si se quiere cubrir data drift, la opcion correcta debe nombrar explicitamente Clarify + Model Monitor como pareja.

### mla01-q8  (A=PASS/4 B=FIX/4)
- [low/B] calidad_distractores: Empleo y educacion no son irrelevantes en scoring real; son distractores 'menos correctos' por grado, lo que puede generar debate en un examinado estricto.
    fix: Reforzar el enunciado con 'la fuente MAS directamente predictiva del riesgo crediticio' para dejar claro que se pide un ranking, no exclusion absoluta.

### mla02-q10  (A=PASS/4 B=PASS/5)

### mla02-q11  (A=PASS/4 B=PASS/5)

### mla02-q12  (A=PASS/4 B=PASS/5)

### mla02-q13  (A=PASS/4 B=PASS/5)

### mla02-q14  (A=PASS/4 B=PASS/5)

### mla02-q16  (A=PASS/4 B=PASS/5)

### mla02-q17  (A=PASS/4 B=PASS/5)

### mla02-q18  (A=PASS/4 B=PASS/5)

### mla02-q2  (A=PASS/4 B=PASS/5)

### mla02-q22  (A=PASS/4 B=PASS/5)

### mla02-q24  (A=PASS/4 B=PASS/5)

### mla02-q25  (A=PASS/4 B=FIX/4)
- [min/B] correccion_tecnica: La carta afirma que Serverless Inference tiene un maximo de ~60 s por invocacion; docs.aws de serverless no establece ese tope explicito. Es un dato heredado de TutorialsDojo que puede confundir.
    fix: Reemplazar '~60 s' por una razon verificable: serverless esta pensado para baja latencia/rafagas cortas y no para procesamiento por lotes de 45 min; evitar citar una cifra de timeout no confirmada.

### mla02-q27  (A=PASS/5 B=PASS/5)

### mla02-q3  (A=PASS/4 B=PASS/5)

### mla02-q32  (A=PASS/4 B=PASS/5)

### mla02-q32b  (A=PASS/4 B=PASS/5)

### mla02-q36  (A=PASS/4 B=PASS/5)

### mla02-q38b  (A=PASS/4 B=PASS/5)

### mla02-q4  (A=PASS/4 B=PASS/5)
- [low/A] calidad_distractores: Las opciones incorrectas incluyen coletillas ('de clasificacion binaria', 'probabilistica de clases', 'combinando clasificacion y regresion') que las delatan como no-regresion; la correcta carece de esa etiqueta.
    fix: Homogeneizar las descripciones de los pares o quitar las coletillas 'de clasificacion' de los distractores para que no se autodescarten.

### mla02-q40  (A=PASS/4 B=PASS/5)

### mla02-q40b  (A=PASS/4 B=PASS/5)

### mla02-q6  (A=PASS/4 B=PASS/5)

### mla02-q7  (A=PASS/4 B=FIX/4)
- [low/B] coherencia_interna: 'Primer paso del proceso de personalizacion' es ambiguo: preparar el dataset ES el primer paso real del proceso; solo el contexto (dataset e IAM ya listos) hace que el fine-tuning sea el primer paso restante.
    fix: Reformular la pregunta a 'dado que ya tiene el dataset JSONL y el rol IAM, cual es el primer paso RESTANTE' para eliminar la ambiguedad entre 'proceso completo' y 'pasos restantes'.

### mla02-q8  (A=PASS/4 B=PASS/5)
