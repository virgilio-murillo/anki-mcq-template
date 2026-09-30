#!/usr/bin/env python3
"""
AIP-C01::Oficial-2 - Preguntas de un examen de practica OFICIAL de AWS (set 2).

37 cartas construidas a partir de decks/aip-c01/dedupe/official_to_generate_off2.json.
Material oficial de alta calidad: cada opcion de la fuente trae un rationale completo,
que se usa para refutar CADA distractor en el dorso.

Reglas aplicadas (docs/DECK_STANDARDS.md al 100%):
- 1 carta por pregunta, EXACTAMENTE 4 opciones (todas las fuentes traen 4).
- Enunciado y opciones traducidos al espanol; HTML con entidades para acentos.
- El frente NO filtra la respuesta.
- Anti-give-away: opciones de longitud comparable (ninguna supera ~1.4x el promedio);
  se suben los distractores, no se acorta la correcta.
- Verdict con {{L}} (NUNCA se hardcodea la letra; el motor baraja y sustituye).
- Dorso: El problema / Por que la respuesta sirve / Por que NO las otras (una por una,
  refutando cada distractor con el rationale oficial) / exam tip (sin nombrar un token
  exclusivo de la correcta) / links docs.aws.amazon.com.
- Sin em dashes.
- key estable y unica: off2-q<n> con el numero n de la fuente.
- correct = indice 0-based en el MISMO orden que la fuente.
"""
from anki_mcq import card, create

cards = []

# ============================================================
# Q1 - Gobernanza del dataset de fine-tuning (Glue Data Catalog + ETL)
# ============================================================
cards.append(card(
    question="Fine-tuning de un FM en Bedrock con chats de soporte en S3. Se necesita linaje del dataset y solo datos aprobados, con el MENOR esfuerzo. &iquest;Como catalogar y curar?",
    options=[
        "Consultar y curar con Amazon Athena (SQL sobre S3)",
        "Referenciar las transcripciones crudas sin transformarlas para fine-tuning",
        "Crawler de AWS Glue que cataloga y Glue ETL que transforma a JSONL",
        "Transformar con Amazon EMR y Apache Spark, con linaje aparte",
    ],
    correct=2,
    key="off2-q1",
    answer=(
        '<div class="verdict">Correcta: {{L}} - crawler + Glue Data Catalog + Glue ETL a JSONL.</div>'
        '<p><b>El problema:</b> se necesita fine-tuning de un FM en Bedrock, pero con <b>linaje</b> (de donde vienen los datos y como se transformaron) y <b>gobernanza</b> (solo datos aprobados), y todo con el minimo esfuerzo operativo. Fine-tuning = reentrenar un modelo base con ejemplos propios. Linaje de datos = registro rastreable del origen y de cada transformacion.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>crawler de AWS Glue</b> infiere el esquema y guarda los metadatos en <b>Glue Data Catalog</b>, lo que da el linaje y el catalogo de origen. Los <b>jobs de Glue ETL</b> (serverless) transforman el texto no estructurado al formato <b>JSONL de la Converse API</b> que Bedrock espera para fine-tuning. Todos los servicios son serverless, asi que se cubren linaje, gobernanza y formato con el menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Athena (SQL) para curar:</b> Athena consulta datos en S3 con SQL, adecuado para datos <b>estructurados</b>, pero aqui el texto es no estructurado, asi que exige mas trabajo de consulta y transformacion; ademas por si solo no cubre linaje ni cumplimiento (haria falta agregar algo como Data Catalog).</li>'
        '<li><b>Referenciar las transcripciones crudas directamente:</b> no atiende gobernanza, linaje ni cumplimiento, y el texto crudo casi seguro no viene en el formato correcto para el job de fine-tuning; faltan transformaciones.</li>'
        '<li><b>Amazon EMR con Spark:</b> EMR si puede transformar los datos, pero <b>no</b> ofrece rastreo de linaje incorporado ni se integra con Glue Data Catalog; habria que implementar esos componentes a mano, lo que sube el esfuerzo operativo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Fine-tuning con linaje y gobernanza y minimo esfuerzo: catalogar el origen y transformar con servicios serverless al formato de entrada requerido. Alternativas de big data transforman pero no aportan linaje ni catalogo; el motor de SQL es para datos estructurados; referenciar el crudo no cumple formato ni cumplimiento.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html">docs.aws Glue Data Catalog y crawlers</a> &middot; '
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prepare.html">docs.aws preparar datos de fine-tuning en Bedrock</a></div>'
    ),
))

# ============================================================
# Q3 - Parametros de salida: temperature 0.5 + top-p 0.8 + length penalty
# ============================================================
cards.append(card(
    question="Un generador de descripciones en Bedrock debe ser creativo pero controlado, coherente con la marca pero con algo de variacion. &iquest;Que parametros logran ese equilibrio?",
    options=[
        "Temperature 0.5 y top-p 0.8 con length penalties para controlar la salida",
        "Temperature 0.9 y top-k 50 sin l&iacute;mite de longitud, priorizando variedad",
        "Temperature 0.5 con l&iacute;mites de longitud y la diversidad deshabilitada",
        "Temperature 0.2 y top-k 4 con stop sequences que fuerzan salida fija",
    ],
    correct=0,
    key="off2-q3",
    answer=(
        '<div class="verdict">Correcta: {{L}} - temperature 0.5, top-p 0.8 y length penalties.</div>'
        '<p><b>El problema:</b> hay que equilibrar creatividad y control. <b>Temperature</b> controla la aleatoriedad al elegir tokens (mas alta = mas variedad). <b>Top-p</b> (nucleus sampling) elige tokens del subconjunto mas probable para balancear diversidad y coherencia. <b>Length penalty</b> controla la verbosidad.</p>'
        '<p><b>Por que la respuesta sirve:</b> una temperature de <b>0.5</b> da creatividad manteniendo un control razonable; un top-p de <b>0.8</b> hace que el modelo considere un rango de opciones pero dentro de limites de probabilidad aceptables; las <b>penalizaciones de longitud</b> ayudan a respetar las guias de marca permitiendo algo de expresion creativa. Es el balance pedido.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Temperature 0.9, top-k 50, sin limites:</b> maximiza aleatoriedad y creatividad, pero sin consistencia ni control; sin restricciones el modelo es mas propenso a alucinar y salirse de la marca.</li>'
        '<li><b>Temperature 0.5, limites de longitud, diversidad deshabilitada:</b> mantiene salidas concisas y consistentes, pero al apagar la diversidad limita la creatividad; falta la variacion de estilo pedida.</li>'
        '<li><b>Temperature 0.2, top-k 4, stop sequences estrictas:</b> con solo 4 tokens candidatos y temperatura muy baja produce salidas casi identicas y repetitivas; demasiado determinista, sin variacion estilistica.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Creativo pero controlado = temperature media (~0.5) + top-p moderado + control de longitud. Temperatura muy alta sin limites descontrola; temperatura muy baja o pocos candidatos vuelve la salida repetitiva.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html">docs.aws parametros de inferencia</a></div>'
    ),
))

# ============================================================
# Q5 - Model cascading: modelo pequeno auto-evalua complejidad
# ============================================================
cards.append(card(
    question="Un sistema debe enrutar consultas simples a un modelo peque&ntilde;o (Llama) y complejas a uno grande (Claude), y ser escalable y de baja latencia. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Intelligent prompt router de Bedrock entre Llama y Claude",
        "Knowledge base con indicadores de complejidad para enrutar",
        "Cascada de modelos: el pequeno auto-evalua y escala al grande",
        "Step Functions con Lambda que enruta por regex y umbrales",
    ],
    correct=2,
    key="off2-q5",
    answer=(
        '<div class="verdict">Correcta: {{L}} - cascada de modelos (el pequeno auto-evalua y escala al grande).</div>'
        '<p><b>El problema:</b> enrutar por complejidad para optimizar costo y latencia, mandando lo simple a un modelo barato y lo complejo a uno potente.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>model cascading</b> (invocacion secuencial) usa primero un modelo pequeno que, por instruccion del system prompt, determina si la consulta es demasiado compleja. La Lambda inspecciona esa respuesta: si es simple, ya esta resuelta rapido y barato; si es compleja, recien entonces invoca al modelo grande con la misma consulta. Optimiza costo y desempeno a la vez.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Intelligent prompt router:</b> el enrutamiento inteligente de prompts de Bedrock solo enruta entre modelos de la <b>misma familia</b>; no puede enrutar entre Llama y Claude (familias distintas).</li>'
        '<li><b>Knowledge base para decidir complejidad:</b> un KB recupera informacion de tus fuentes para aumentar prompts; no analiza la complejidad de una consulta ni enruta entre modelos.</li>'
        '<li><b>Step Functions con regex:</b> analizar complejidad por patrones de texto es demasiado simplista, se pierde la complejidad semantica que el regex no detecta y exige mantener los patrones continuamente.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Enrutar por complejidad entre familias distintas: cascada de modelos (pequeno primero, grande solo si hace falta). El prompt router solo cruza modelos de la misma familia; regex no capta complejidad semantica.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html">docs.aws intelligent prompt routing</a></div>'
    ),
))

# ============================================================
# Q6 - Comprehend entity recognition + normalizar + Bedrock reformatea
# ============================================================
cards.append(card(
    question="Un equipo tiene datos de cat&aacute;logo heterog&eacute;neos (formatos e idiomas distintos) y debe dar entradas consistentes a los FM. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Comprehend extrae entidades, normalizar y Bedrock reformatea",
        "Normalizar, clasificacion personalizada de Comprehend y validacion propia",
        "Step Functions: Comprehend extrae entidades y Lambda valida y filtra",
        "Comprehend entidades y sentimiento, features en DynamoDB, calidad con CloudWatch",
    ],
    correct=0,
    key="off2-q6",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Comprehend (entidades) + normalizar + Bedrock reformatea.</div>'
        '<p><b>El problema:</b> mejorar la calidad de datos heterogeneos y entregar entradas consistentes al FM. La clave es que ademas de extraer y normalizar, hace falta <b>reformatear el texto</b> para el consumo del modelo.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>reconocimiento de entidades de Amazon Comprehend</b> extrae informacion estructurada del texto y ayuda a estandarizar atributos; luego se <b>normalizan</b> categorias y especificaciones; y <b>Amazon Bedrock reformatea</b> las descripciones para dar una estructura de entrada consistente al FM. Cubre extraccion, normalizacion y reformateo, que es lo que mejora la consistencia de las respuestas.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Clasificacion personalizada + reglas de validacion:</b> la clasificacion personalizada de Comprehend se enfoca en <b>categorizar</b>, no en extraer entidades, y sin capacidad de reformateo del texto no logra la mejora de calidad de entrada necesaria.</li>'
        '<li><b>Step Functions + Comprehend + validacion:</b> extrae entidades y valida, pero <b>no reformatea</b> el texto; sin reformateo no se estructura bien la entrada para el FM.</li>'
        '<li><b>Comprehend + DynamoDB + CloudWatch:</b> guardar features en DynamoDB sin reformateo no asegura entradas consistentes, y las metricas de CloudWatch por si solas no mejoran la calidad de los datos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Consistencia de entrada al FM: extraer entidades + normalizar + <b>reformatear</b> el texto con el modelo generativo. Si a la opcion le falta el paso de reformateo, no cumple aunque extraiga y valide.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/how-entities.html">docs.aws Comprehend reconocimiento de entidades</a></div>'
    ),
))


# ============================================================
# Q10 - SCP forzando VPC endpoint para Bedrock
# ============================================================
cards.append(card(
    question="En prod el acceso a la API de Bedrock no debe pasar por internet publico, y debe cumplirse sin importar los roles IAM ni la app. &iquest;Que solucion cumple?",
    options=[
        "Interface VPC endpoint (ruta privada) mas una SCP que aplica en la OU de prod",
        "Interface VPC endpoint mas una pol&iacute;tica IAM configurada por cuenta",
        "NAT gateway privado con route tables que enrutan Bedrock al NAT",
        "Interface VPC endpoint con endpoint policies que limitan a la app aprobada",
    ],
    correct=0,
    key="off2-q10",
    answer=(
        '<div class="verdict">Correcta: {{L}} - interface VPC endpoint + SCP en la OU de produccion.</div>'
        '<p><b>El problema:</b> forzar acceso privado a Bedrock <b>a nivel de organizacion</b>, de forma que no dependa de como se configuren los roles IAM ni de la app. SCP (Service Control Policy) = politica de organizacion que limita permisos en todas las cuentas de una OU. Un interface VPC endpoint da conectividad privada dentro de la red de AWS.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>interface VPC endpoint</b> ofrece la ruta privada a Bedrock, y la <b>SCP</b> adjunta a la OU de produccion niega las acciones de Bedrock salvo que la peticion venga por un endpoint aprobado. Como la SCP se aplica por encima de cualquier configuracion IAM de la cuenta, la restriccion se cumple aunque un administrador cambie un rol.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Politica IAM en cada cuenta:</b> las politicas IAM se adjuntan a roles individuales y un administrador de cuenta puede modificarlas o configurarlas mal; no dan cumplimiento a nivel de organizacion ni garantizan la restriccion si cambian los roles.</li>'
        '<li><b>NAT gateway privado:</b> un NAT gateway da salida desde subredes privadas hacia internet u otras redes, pero no puede enrutar hacia servicios publicos de AWS como Bedrock salvo via conectividad privada (VPC endpoint); ademas no impone controles de organizacion ni bloquea el endpoint publico.</li>'
        '<li><b>Endpoint policies solamente:</b> controlan el acceso al endpoint en si, pero no impiden que la app evite el endpoint y llame directamente a la API publica de Bedrock.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cumplimiento a nivel de organizacion, sin depender de IAM: una politica de organizacion adjunta a la unidad de produccion (mas el VPC endpoint para la ruta privada). Las politicas IAM y las endpoint policies son locales o evadibles; el NAT gateway no alcanza servicios publicos por si solo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html">docs.aws service control policies</a> &middot; '
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html">docs.aws VPC endpoints para Bedrock</a></div>'
    ),
))

# ============================================================
# Q11 - Reranker + top-5 para reducir tokens sin perder accuracy
# ============================================================
cards.append(card(
    question="Un KB con buen recall pasa 50 resultados al LLM y los tokens se dispararon; hay que reducir tokens sin perder accuracy, con el MENOR esfuerzo. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Rehacer el chunking a sem&aacute;ntico adaptativo y pasar los 10 primeros al LLM",
        "Configurar el KB para que use semantic search puro",
        "Invocar un modelo reranker que reordena y pasar al LLM solo los 5 mejores",
        "Limitar el contexto a los 5 primeros documentos recuperados, sin reordenar",
    ],
    correct=2,
    key="off2-q11",
    answer=(
        '<div class="verdict">Correcta: {{L}} - reranker + solo los 5 mejor rankeados.</div>'
        '<p><b>El problema:</b> el recall ya es suficiente, pero falta <b>precision</b> (ordenar bien por relevancia). Pasar 50 chunks al LLM gasta tokens. Hay que reducir tokens manteniendo accuracy, con minimo esfuerzo. Reranker = modelo que reordena los resultados recuperados por relevancia.</p>'
        '<p><b>Por que la respuesta sirve:</b> los knowledge bases soportan <b>modelos reranker</b> que reordenan los resultados para mejorar la precision. Al activar el reranker y limitar a los <b>5 mejor rankeados</b>, se mantiene la accuracy (los 5 son los mas relevantes) y bajan los tokens que llegan al LLM. Es un cambio directo en el knowledge base: minimo esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Chunking semantico adaptativo + top 10:</b> baja tokens y da mejor contexto, pero obliga a <b>reprocesar y reindexar</b> todo el corpus; mas esfuerzo.</li>'
        '<li><b>Cambiar a semantic search:</b> el hybrid actual ya incluye busqueda semantica; pasar a semantico puro no arregla el ranking ni el uso de tokens (da recall, no precision).</li>'
        '<li><b>Solo limitar a 5 sin reranker:</b> reduce tokens, pero sin reordenar, esos 5 pueden no ser los mas relevantes; cae la accuracy, que es justo lo que no se puede sacrificar.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Buen recall pero mal orden, y hay que bajar tokens sin perder accuracy: reranker + top-N pequeno. Recortar a top-N sin reranker sacrifica precision; reindexar (chunking nuevo) es mas esfuerzo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html">docs.aws reranking en Bedrock</a></div>'
    ),
))

# ============================================================
# Q13 - CloudWatch dashboard + invocation logs para diagnosticar RAG
# ============================================================
cards.append(card(
    question="Diagnosticar la causa ra&iacute;z de la latencia inconsistente de un RAG en prod (Bedrock + OpenSearch) es el objetivo, con el MENOR esfuerzo. &iquest;Qu&eacute; soluci&oacute;n conviene?",
    options=[
        "Metricas custom de CloudWatch y alarmas compuestas de similitud y tokens",
        "Monitoreo detallado, metric math y deteccion de anomalias",
        "Trazado distribuido con AWS X-Ray y subsegmentos custom",
        "Dashboard de CloudWatch de OpenSearch mas invocation logs de Bedrock",
    ],
    correct=3,
    key="off2-q13",
    answer=(
        '<div class="verdict">Correcta: {{L}} - dashboard de CloudWatch + invocation logs de Bedrock.</div>'
        '<p><b>El problema:</b> diagnosticar latencia inconsistente en un pipeline RAG con el minimo esfuerzo, usando lo que ya viene incorporado en vez de construir instrumentacion propia.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>dashboard de CloudWatch</b> combina, con metricas ya existentes, la latencia de recuperacion de contexto de OpenSearch con los conteos de operaciones, dando la correlacion visual entre el rendimiento de la busqueda vectorial y el tiempo total. Los <b>invocation logs de Bedrock</b> contienen el detalle de cada interaccion con el modelo, asi que permiten identificar que consultas al KB se estan degradando. Usa metricas y logs integrados: menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Metricas custom + alarmas compuestas:</b> crear metricas personalizadas y condiciones de alarma complejas suma esfuerzo operativo, y correlacionar umbrales de similitud con consumo de tokens puede no revelar la causa raiz de la latencia.</li>'
        '<li><b>Metric math + anomaly detection:</b> sobrecomplica el analisis; correlacionar busqueda vectorial e inferencia via metric math no dice claramente si el problema esta en la recuperacion o en el modelo, y la deteccion de anomalias puede dar falsos positivos por la complejidad del RAG.</li>'
        '<li><b>X-Ray con subsegmentos custom:</b> el trazado ayuda a visualizar el flujo, pero crear subsegmentos personalizados para operaciones vectoriales y tokens requiere esfuerzo operativo adicional para ese nivel de granularidad.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Diagnostico de RAG con minimo esfuerzo: dashboard con metricas integradas + los invocation logs del servicio de inferencia. Metricas custom, metric math con anomaly detection y subsegmentos de X-Ray suman trabajo de instrumentacion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html">docs.aws model invocation logging</a></div>'
    ),
))

# ============================================================
# Q15 - Bedrock Prompt Management (compare versions, sin deploy)
# ============================================================
cards.append(card(
    question="Un equipo quiere catalogar prompts como plantillas con variables, versionarlos, comparar versiones y probarlos antes de desplegar, con el MENOR esfuerzo. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Prompt Management con variables; probar con compare versions sin desplegar",
        "Plantillas JSON en S3, Prompt Management para A/B y Lambda para versionar",
        "Prompt Management por tipo, versionar por convencion de nombres",
        "Prompt Management con variables; probar desplegando cada version a staging",
    ],
    correct=0,
    key="off2-q15",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock Prompt Management con compare versions (sin desplegar).</div>'
        '<p><b>El problema:</b> catalogar prompts, plantillarlos con variables, versionarlos, comparar versiones y probarlos antes de desplegar, todo con minimo esfuerzo. Prompt Management es el servicio de Bedrock para almacenar, catalogar y gestionar prompts.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Prompt Management</b> centraliza el catalogo de prompts, soporta plantillas parametrizadas con variables y system instructions que fijan el rol del modelo, y trae versionado y prueba integrados. La funcion <b>compare versions</b> permite probar y evaluar versiones lado a lado <b>sin desplegar</b>; luego se crea una version y se ejecuta por las APIs de Bedrock. Cubre todo sin infraestructura propia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>JSON en S3 + Lambda + CloudWatch:</b> S3 versiona objetos pero no cataloga, versiona ni prueba prompts; requiere Lambda propia para sustitucion de variables y control de versiones, lo que duplica capacidades que Prompt Management ya trae y suma esfuerzo.</li>'
        '<li><b>Prompts separados por tipo con convencion de nombres:</b> versionar por nombres es propenso a errores y no escala; ademas los system prompts estaticos no personalizan el rol por cliente y no cumple el requisito de variables parametrizadas para nombre de cliente y contenido.</li>'
        '<li><b>Probar desplegando a staging:</b> usa Prompt Management, pero obliga a <b>desplegar</b> a un entorno de staging para probar, lo que suma esfuerzo operativo frente a comparar versiones sin desplegar.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Catalogar, versionar, plantillar con variables y probar prompts sin desplegar y con minimo esfuerzo: el servicio de gestion de prompts con su funcion de comparar versiones. Construirlo en S3 con funciones propias o versionar por nombres suma trabajo; probar en staging exige desplegar.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
    ),
))

# ============================================================
# Q19 - Multiples guardrails con tags + EventBridge por horario
# ============================================================
cards.append(card(
    question="Un asistente Bedrock usado por varios departamentos necesita filtrado distinto por horario y por departamento con Guardrails, con el MENOR esfuerzo. &iquest;Que solucion cumple?",
    options=[
        "Un guardrail maximo y Step Functions que post-procesa, reglas en Parameter Store",
        "Varios guardrails con tags y una Lambda por EventBridge que elige segun la hora",
        "Guardrails estaticos por escenario y una funcion con la logica en DynamoDB",
        "Crear/actualizar guardrails por peticion via API, con cache en ElastiCache",
    ],
    correct=1,
    key="off2-q19",
    answer=(
        '<div class="verdict">Correcta: {{L}} - varios guardrails con tags + EventBridge por horario.</div>'
        '<p><b>El problema:</b> aplicar filtrado distinto por horario y por departamento usando Guardrails, con minimo esfuerzo. Guardrails = capa de filtrado de contenido en la invocacion del modelo; soporta tags para organizar y contextualizar.</p>'
        '<p><b>Por que la respuesta sirve:</b> se crean <b>varios guardrails etiquetados</b> por contexto (horario, departamento) y se usa <b>EventBridge</b>, que trae manejo de eventos por tiempo, para disparar una Lambda que seleccione automaticamente el guardrail adecuado segun la hora. Aprovecha funciones integradas (Guardrails + EventBridge) sin bases de datos ni orquestacion compleja: menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Un guardrail maximo + Step Functions post-procesando:</b> filtrar en post-proceso desperdicia tokens en respuestas que luego se descartan y obliga a mantener varios componentes serverless; mina el control granular de los guardrails.</li>'
        '<li><b>Guardrails estaticos + DynamoDB:</b> tener un guardrail por cada combinacion departamento-horario exige actualizar muchos guardrails ante cada cambio de politica, y mantener la tabla DynamoDB de seleccion suma esfuerzo operativo.</li>'
        '<li><b>Crear/actualizar guardrails por peticion via API:</b> CreateGuardrail/UpdateGuardrail son operaciones administrativas, no para el flujo en tiempo real; usarlas por peticion agrega latencia y riesgo de condiciones de carrera, y el cluster ElastiCache suma complejidad y costo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Filtrado por contexto (horario/departamento) con minimo esfuerzo: varios guardrails con tags mas un servicio de eventos por tiempo que elija el guardrail. Post-procesar desperdicia tokens; las APIs de gestion de guardrails no son para el runtime por peticion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
    ),
))


# ============================================================
# Q20 - RAG eval: dataset humano-validado + custom metrics (LLM judge)
# ============================================================
cards.append(card(
    question="Bedrock model evaluation (RAG, LLM-as-a-judge) - la evaluacion debe medir correctness, relevance y escala de formalidad y tono propios. &iquest;Que solucion es la MAS costo-efectiva?",
    options=[
        "Dataset validado por humanos y custom metrics para formalidad y tono",
        "Dataset validado por humanos y evaluacion basada en humanos",
        "Dataset benchmark de la industria y evaluacion basada en humanos",
        "Dataset benchmark de la industria y custom metrics para formalidad y tono",
    ],
    correct=0,
    key="off2-q20",
    answer=(
        '<div class="verdict">Correcta: {{L}} - dataset humano-validado + custom metrics (LLM-as-a-judge).</div>'
        '<p><b>El problema:</b> evaluar aspectos propios de la empresa (formalidad, tono, estilo) de forma consistente, escalable y barata. LLM-as-a-judge = un LLM evalua las respuestas segun criterios definidos.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>dataset validado por humanos</b> representa fielmente los casos de uso, terminologia y patrones de contenido de la empresa. Usar <b>LLM-as-a-judge con custom metrics</b> da una evaluacion automatica, consistente y escalable: se disenan metricas propias para medir la escala de formalidad y el tono/estilo con criterios uniformes. Es la combinacion mas costo-efectiva.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Dataset humano + evaluacion basada en humanos:</b> el dataset es adecuado, pero la evaluacion humana es menos eficiente que las custom metrics (mas costo, ciclos mas largos, posible inconsistencia en el scoring) y mezclar LLM y humano suma complejidad innecesaria.</li>'
        '<li><b>Benchmark estandar + evaluacion humana:</b> el benchmark de la industria carece del contexto empresarial y no capta el tono y estilo propios; ademas la evaluacion humana es cara y lenta.</li>'
        '<li><b>Benchmark estandar + custom metrics:</b> las custom metrics estan bien, pero el dataset benchmark generico compromete los resultados porque no representa los escenarios reales ni el tono/estilo de la empresa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Evaluar tono/estilo propios de forma barata y escalable: dataset validado por humanos + LLM-as-a-judge con custom metrics. La evaluacion humana no escala en costo; el benchmark generico no capta el contexto de la empresa.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock model evaluation</a></div>'
    ),
))

# ============================================================
# Q21 - Semantic chunking + optimizar max tokens (reducir costo retrieval)
# ============================================================
cards.append(card(
    question="El chunking de tama&ntilde;o fijo (1.000 tokens) fragmenta el contenido y los costos de recuperaci&oacute;n subieron; hay que reducir costos manteniendo accuracy. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Amazon Nova para embedding de chunks y Anthropic Claude para sumarizacion",
        "Habilitar semantic chunking y optimizar el maximo de tokens",
        "Reducir el tamano de chunk y usar Bedrock Agents con recuperacion automatica",
        "Un Claude con contexto maximo y sumarizacion recursiva antes de la ingesta",
    ],
    correct=1,
    key="off2-q21",
    answer=(
        '<div class="verdict">Correcta: {{L}} - semantic chunking + optimizar el maximo de tokens.</div>'
        '<p><b>El problema:</b> el chunking fijo parte el contenido a mitad de idea, genera chunks fragmentados y desperdicia tokens al recuperar. Hay que bajar costo sin perder comprension. Semantic chunking = dividir el texto por limites naturales (parrafos, tablas, secciones).</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>semantic chunking</b> agrupa el contenido siguiendo fronteras naturales, evitando fragmentar la informacion financiera y minimizando el desperdicio de tokens. Ajustar el <b>maximo de tokens</b> equilibra accuracy de recuperacion y uso de tokens, de modo que solo la informacion mas relevante llega al modelo. Baja costos preservando la comprension.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Orquestar Nova + Claude:</b> puede bajar el costo de computo, pero alternar modelos puede aumentar el total de tokens por reprocesamiento y recreacion de contexto; no ataca la ineficiencia de tokens dentro de cada llamada ni el problema de fragmentacion.</li>'
        '<li><b>Reducir el tamano de chunk + Agents:</b> los agents no optimizan el uso de tokens por si mismos y la recuperacion automatica puede sumar contexto innecesario; chunks mas chicos mejoran precision pero pueden reducir la accuracy del modelo.</li>'
        '<li><b>Claude con contexto maximo + sumarizacion recursiva:</b> no optimiza el uso de tokens ni corrige el chunking fijo fragmentado; usar siempre el contexto maximo consume tokens de mas y la sumarizacion recursiva puede perder informacion y sumar llamadas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Chunking fijo que fragmenta y encarece: semantic chunking + ajustar el maximo de tokens. Cambiar de modelo o ampliar el contexto no arregla la fragmentacion de origen.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws estrategias de chunking en Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q22 - DynamoDB single-table + GSI + DAX + TTL para historial de chat
# ============================================================
cards.append(card(
    question="Un historial de chat necesita filtrado por metadatos, reanudar desde cualquier punto, baja latencia en lo reciente y borrado al expirar. &iquest;Qu&eacute; implementaci&oacute;n es la MAS escalable?",
    options=[
        "OpenSearch con metadatos y full-text, indices por tiempo y politicas ISM",
        "DynamoDB single-table con GSI, sort keys jerarquicos, DAX y TTL",
        "DynamoDB clave user+timestamp, Streams a ElastiCache y TTL",
        "Hibrido: ElastiCache con TTL y Aurora PostgreSQL con pgvector y pg_cron",
    ],
    correct=1,
    key="off2-q22",
    answer=(
        '<div class="verdict">Correcta: {{L}} - DynamoDB single-table con GSI + DAX + TTL.</div>'
        '<p><b>El problema:</b> historial de chat altamente escalable con busqueda por metadatos, baja latencia en lo reciente y borrado por expiracion. GSI = global secondary index (indice para consultar por atributos distintos de la clave). DAX = cache en memoria de DynamoDB. TTL = borrado automatico de items expirados.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>DynamoDB</b> con <b>GSI</b> y <b>diseno single-table</b> escala muy alto y soporta consultas por user ID, conversation ID y rangos de fecha; los <b>sort keys jerarquicos</b> permiten consultar el historial manteniendo la relacion entre mensajes y metadatos. <b>DAX</b> da lecturas en submilisegundos para lo reciente (baja latencia) y el <b>TTL</b> borra automaticamente lo expirado. Cubre todos los requisitos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>OpenSearch Service + indices por tiempo + ISM:</b> da full-text y borrado, pero no optimiza la busqueda por metadatos ni la baja latencia de lo reciente, puede tener retraso de indexado y limitaciones de escala en alta concurrencia.</li>'
        '<li><b>DynamoDB clave user+timestamp + Streams + Redis:</b> solo soporta consultas ordenadas por tiempo; no permite filtrar ni reanudar por metadatos (p.ej. conversation ID), asi que no cumple la busqueda flexible.</li>'
        '<li><b>Hibrido Redis + Aurora pgvector + pg_cron:</b> no escala como se necesita; obliga a gestionar dos datastores y logica de programacion propia, y el cluster Redis y las conexiones de PostgreSQL se vuelven cuello de botella al crecer la concurrencia.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Historial de chat escalable con filtrado por metadatos, baja latencia y expiracion: diseno single-table con indices secundarios, cache en memoria y expiracion automatica. Una clave user+timestamp solo da orden temporal; los enfoques hibridos suman datastores que no escalan.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql-B.html">docs.aws diseno single-table en DynamoDB</a></div>'
    ),
))

# ============================================================
# Q24 - RetrieveAndGenerate + Guardrails (citas + filtros)
# ============================================================
cards.append(card(
    question="Analisis de contratos legales - las respuestas deben citar una fuente autorizada, evitar consejo legal inapropiado y filtrar datos sensibles, con el MENOR esfuerzo. &iquest;Que solucion cumple?",
    options=[
        "RetrieveAndGenerate API y Guardrails con content filters y topic restrictions",
        "Retrieve API y filtrado con logica propia en Lambda",
        "RetrieveAndGenerate API y filtrado con logica propia en Lambda",
        "Retrieve API y Guardrails con content filters y topic restrictions",
    ],
    correct=0,
    key="off2-q24",
    answer=(
        '<div class="verdict">Correcta: {{L}} - RetrieveAndGenerate API + Guardrails.</div>'
        '<p><b>El problema:</b> respuestas con cita de fuente autorizada y filtrado de contenido, con minimo esfuerzo. La <b>RetrieveAndGenerate API</b> hace recuperacion y generacion en una sola llamada; la <b>Retrieve API</b> solo devuelve fragmentos.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>RetrieveAndGenerate</b> combina la busqueda semantica sobre los embeddings con la generacion en una sola llamada, y aporta automaticamente las <b>citas</b> esenciales para cumplimiento legal. Adjuntar <b>Guardrails</b> con content filters y topic restrictions previene el consejo legal inapropiado y filtra informacion sensible, todo sin desarrollo custom ni orquestacion extra.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Retrieve API + filtrado en Lambda:</b> la Retrieve API solo devuelve chunks sin generar respuesta, asi que falta implementar el RAG completo; y el filtrado custom en Lambda no tiene las funciones de seguridad integradas de Guardrails.</li>'
        '<li><b>RetrieveAndGenerate + filtrado en Lambda:</b> genera respuestas con citas, pero el filtrado custom en Lambda requiere mucho desarrollo y mantenimiento y carece de las protecciones integradas de Guardrails, sumando complejidad y riesgo de cumplimiento.</li>'
        '<li><b>Retrieve API + Guardrails:</b> Guardrails filtra, pero la Retrieve API solo devuelve chunks sin generar; habria que orquestar aparte la inferencia y la generacion, y no produce recomendaciones completas para preguntas legales complejas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>RAG con citas + filtrado con minimo esfuerzo: RetrieveAndGenerate (recupera, genera y cita en una llamada) + Guardrails. La Retrieve API sola no genera; el filtrado custom en Lambda no reemplaza a Guardrails.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-test.html">docs.aws RetrieveAndGenerate</a> &middot; '
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Guardrails</a></div>'
    ),
))

# ============================================================
# Q25 - Step Functions Standard orquestando FM largo (5-15 min)
# ============================================================
cards.append(card(
    question="Documentos que tardan 5 a 15 min con varias llamadas al FM llegan a 1.000 concurrentes en pico y necesitan audit trails y resultados disponibles. &iquest;Qu&eacute; soluci&oacute;n cumple con el MENOR esfuerzo?",
    options=[
        "S3 Event Notifications a Lambda que lanza Step Functions Standard, estado en DynamoDB",
        "API Gateway con WebSocket APIs para mantener la conexion mientras procesa",
        "Kinesis para recibir, Lambdas consumidoras en paralelo y resultados en OpenSearch",
        "API Gateway con Lambdas que llaman a Bedrock de forma sincrona y guardan en DynamoDB",
    ],
    correct=0,
    key="off2-q25",
    answer=(
        '<div class="verdict">Correcta: {{L}} - S3 + Lambda + Step Functions Standard + DynamoDB.</div>'
        '<p><b>El problema:</b> procesos largos (5 a 15 min) con multiples llamadas al FM, alta concurrencia, audit trail y resultados consultables, con minimo esfuerzo. Step Functions <b>Standard</b> = workflows de larga duracion (hasta 1 ano) con historial de ejecucion detallado.</p>'
        '<p><b>Por que la respuesta sirve:</b> S3 almacena de forma segura, las <b>S3 Event Notifications</b> invocan una Lambda que lanza un <b>workflow Standard de Step Functions</b> capaz de correr por horas y que guarda un historial de ejecucion detallado (audit trail). Step Functions orquesta las multiples llamadas a Bedrock y <b>DynamoDB</b> da acceso rapido y consistente al estado y a los resultados. Todo con servicios gestionados: menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>API Gateway WebSocket:</b> mantener conexiones abiertas 5 a 15 min por documento es costoso en recursos; gestionar miles de conexiones de larga vida (estado, reconexion, notificaciones) suma mucho esfuerzo operativo.</li>'
        '<li><b>Kinesis + Lambda + OpenSearch:</b> escala, pero obliga a gestionar el sharding del stream, monitorear las Lambdas consumidoras, mantener el cluster de OpenSearch y manejar estado y auditoria a mano; mas esfuerzo.</li>'
        '<li><b>API Gateway con llamadas sincronas:</b> API Gateway tiene timeout de 29 segundos y Lambda de 15 minutos, incompatibles con procesos de 5 a 15 min de forma sincrona; la solucion fallaria y no maneja bien la concurrencia en pico.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Orquestar procesos largos de varios pasos con auditoria y minimo esfuerzo: un workflow de larga duracion con historial de ejecucion, disparado por evento, con una tabla para estado y resultados. Recuerda el timeout de 29 s de API Gateway y los 15 min de las funciones sin servidor.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html">docs.aws Step Functions Standard vs Express</a></div>'
    ),
))


# ============================================================
# Q26 - Continued pre-training (datos no etiquetados de dominio)
# ============================================================
cards.append(card(
    question="Un FM rinde mal en un nicho. Hay 3 TB de datos NO etiquetados del dominio y se quiere que el modelo desarrolle comprension profunda de su terminologia. &iquest;Que solucion cumple?",
    options=[
        "Continued pre-training del modelo en Bedrock con los datos",
        "Fine-tuning del modelo en Bedrock con los datos",
        "Resumir los datos con un LLM e incorporarlo como system prompt",
        "Knowledge distillation para transferir el conocimiento a un modelo nuevo",
    ],
    correct=0,
    key="off2-q26",
    answer=(
        '<div class="verdict">Correcta: {{L}} - continued pre-training.</div>'
        '<p><b>El problema:</b> dar al modelo una comprension profunda de un dominio a partir de <b>mucho texto no etiquetado</b>. Continued pre-training = seguir el preentrenamiento del modelo con datos de dominio no etiquetados; fine-tuning = ajustar con ejemplos etiquetados (entrada -> salida deseada).</p>'
        '<p><b>Por que la respuesta sirve:</b> con <b>continued pre-training</b> el modelo aprende de grandes volumenes de datos no etiquetados especificos del dominio, continuando su entrenamiento de lenguaje sobre contenido nuevo. Asi desarrolla una comprension profunda de la terminologia, los conceptos y las relaciones del nicho a partir de los 3 TB propios.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Fine-tuning:</b> requiere datos <b>etiquetados</b> (ejemplos de entrada-salida) y sirve para que el modelo aprenda a generar cierta salida ante cierta entrada, no para adquirir comprension amplia de un dominio a partir de texto no etiquetado.</li>'
        '<li><b>Resumen como system prompt:</b> los system prompts guian el comportamiento del modelo, pero no son forma efectiva de incorporar grandes volumenes de datos especializados; sirven para orientar, no para expandir la base de conocimiento.</li>'
        '<li><b>Knowledge distillation:</b> crea un modelo mas pequeno y eficiente transfiriendo conocimiento de uno grande; se enfoca en compresion y eficiencia, no en incorporar nuevo conocimiento de dominio ni en mejorar la comprension.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Mucho texto NO etiquetado de dominio para comprension profunda: continued pre-training. Fine-tuning necesita datos etiquetados; los prompts no expanden conocimiento; la distillation comprime, no ensena dominio.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html">docs.aws personalizacion de modelos en Bedrock</a></div>'
    ),
))

# ============================================================
# Q27 - SageMaker Clarify + FMEval (CrowS-Pairs) + CloudWatch (bias)
# ============================================================
cards.append(card(
    question="Una app GenAI en SageMaker necesita un framework integral de fairness que detecte sesgos sutiles entre grupos socioecon&oacute;micos, edades y regiones. &iquest;Qu&eacute; soluci&oacute;n cumple con el MENOR esfuerzo?",
    options=[
        "SageMaker Model Monitor ante bias drift con alertas por umbral",
        "Datasets propios por grupo, batch transform y reentrenamiento automatico",
        "Monitoreo con CloudWatch, RBAC y Comprehend para sentimiento",
        "SageMaker Clarify, FMEval con CrowS-Pairs y metricas de CloudWatch por disparidad",
    ],
    correct=3,
    key="off2-q27",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SageMaker Clarify + FMEval (CrowS-Pairs) + CloudWatch.</div>'
        '<p><b>El problema:</b> detectar sesgos sutiles entre multiples dimensiones demograficas con un framework integral y minimo esfuerzo. Clarify = servicio de deteccion de sesgo de SageMaker; FMEval = evaluacion de FMs; CrowS-Pairs = dataset para medir sesgos estereotipicos.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Clarify</b> detecta sesgo automaticamente entre distintos grupos demograficos; <b>FMEval con CrowS-Pairs</b> prueba sesgos estereotipicos; y las <b>metricas de CloudWatch</b> monitorean de forma continua la disparidad demografica. Con capacidades integradas se cubre un framework robusto en varias dimensiones sin construir todo a mano.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Model Monitor:</b> detecta data drift, pero no esta disenado para evaluacion integral de fairness en multiples dimensiones demograficas; requeriria mucha personalizacion, sumando esfuerzo.</li>'
        '<li><b>Datasets propios + batch transform + reentrenamiento automatico:</b> exige construir todos los componentes (mas esfuerzo), y el reentrenamiento automatico al detectar sesgo puede introducir nuevos sesgos sin un framework de evaluacion adecuado.</li>'
        '<li><b>CloudWatch + RBAC + Comprehend:</b> monitoreo y RBAC son utiles para seguridad, pero no evaluan fairness entre grupos; Comprehend hace analisis de sentimiento, no mide sesgos demograficos en las salidas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Fairness integral con minimo esfuerzo en SageMaker: la deteccion de sesgo integrada + evaluaciones del modelo con un dataset de estereotipos + metricas de disparidad. Model Monitor es para drift; Comprehend no mide sesgo demografico.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-fairness-and-explainability.html">docs.aws SageMaker Clarify (fairness)</a></div>'
    ),
))

# ============================================================
# Q30 - BDA transformation con custom type reutilizable
# ============================================================
cards.append(card(
    question="En BDA hay que separar AuthorizedSigner en TITLE, FIRST_NAME, LAST_NAME, SUFFIX y JOB_TITLE, reutilizando el formato en WitnessName y ReviewerName. &iquest;Que capacidad cumple?",
    options=[
        "Transformation con un custom type reutilizable para separar el campo",
        "Normalization para separar el valor con reemplazos por patrones",
        "Extraction para mapear subcampos asignando alias",
        "Validation para exigir subcampos y rechazar nombres malformados",
    ],
    correct=0,
    key="off2-q30",
    answer=(
        '<div class="verdict">Correcta: {{L}} - transformation con custom type reutilizable.</div>'
        '<p><b>El problema:</b> separar un campo complejo (nombre completo con titulo, sufijo y cargo) en componentes estructurados y <b>reutilizar</b> esa estructura en varios campos. En BDA: transformation transforma/separa campos, un custom type define una estructura reutilizable.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>transformation</b> puede dividir campos complejos en componentes estructurados (por ejemplo, separar un nombre completo), y un <b>custom type</b> define esa estructura una vez para <b>reutilizarla</b> en campos como AuthorizedSigner, WitnessName o ReviewerName. Cubre exactamente separar y reutilizar.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Normalization:</b> estandariza el formato de un campo (por ejemplo, "NY" a "New York"), pero no hace separacion semantica ni crea grupos de campos estructurados como los componentes de un nombre.</li>'
        '<li><b>Extraction:</b> recupera valores de campos y los alias solo renombran; no parsea ni separa cadenas complejas con titulos y sufijos.</li>'
        '<li><b>Validation:</b> impone restricciones despues de transformar (chequea nulos o formatos incorrectos), pero no puede parsear ni reestructurar campos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Separar un campo compuesto y reutilizar la estructura en varios campos (BDA): transformation + custom type. Normalization estandariza formato, extraction recupera/renombra, validation solo valida despues.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html">docs.aws Bedrock Data Automation</a></div>'
    ),
))

# ============================================================
# Q35 - Amazon Comprehend custom classification para enrutar a FM
# ============================================================
cards.append(card(
    question="Hay varios FM afinados por tema y se debe enrutar cada consulta al FM correcto segun el tema, event-driven y escalable, con el MENOR esfuerzo. &iquest;Que solucion cumple?",
    options=[
        "Lambda con Comprehend que detecta el idioma dominante y enruta",
        "Endpoint de clasificacion propio en SageMaker que la Lambda llama",
        "Clasificacion personalizada de Comprehend que la Lambda llama",
        "Fine-tuning de un FM en Bedrock para clasificar temas",
    ],
    correct=2,
    key="off2-q35",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Amazon Comprehend custom classification.</div>'
        '<p><b>El problema:</b> clasificar la consulta por <b>tema</b> (facturacion, soporte tecnico, etc.) para enrutar al FM afinado correcto, con minimo esfuerzo. Comprehend custom classification = entrenar un clasificador de texto en categorias propias, servicio totalmente gestionado.</p>'
        '<p><b>Por que la respuesta sirve:</b> con <b>Comprehend custom classification</b> se entrena un modelo para clasificar el texto en etiquetas definidas por el usuario (facturacion, soporte tecnico), detectando el tema. Es totalmente gestionado y no requiere hospedar modelos, y la Lambda enruta dinamicamente al FM especializado segun el tema detectado.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Detectar idioma con Comprehend:</b> identificar el idioma dominante no basta para determinar el tema ni la intencion de la consulta.</li>'
        '<li><b>Endpoint de clasificacion en SageMaker:</b> hay que entrenar el modelo y aprovisionar y mantener un inference endpoint; mas esfuerzo operativo.</li>'
        '<li><b>Fine-tuning de un FM para clasificar:</b> introduce afinamiento innecesario y sube el esfuerzo; ademas hospedar el FM afinado agrega esfuerzo de despliegue e inferencia (Provisioned Throughput u on-demand custom model deployment de pago por uso), mas que un servicio de clasificacion gestionado.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Enrutar por tema con minimo esfuerzo: Comprehend custom classification (gestionado, sin hospedar modelos). Detectar idioma no da el tema; SageMaker o un FM afinado agregan despliegue e inferencia que mantener (el FM afinado puede servirse con Provisioned Throughput o con on-demand deployment; ninguna es obligatoria).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html">docs.aws Comprehend custom classification</a>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-use.html">docs.aws usar un modelo afinado en Bedrock</a></div>'
    ),
))

# ============================================================
# Q36 - Metadata filter por modification time
# ============================================================
cards.append(card(
    question="Un asistente sobre Knowledge Bases debe contestar <b>solo con los documentos mas recientes</b> e <b>ignorar los mas antiguos</b>. &iquest;Que solucion cumple?",
    options=[
        "Un prompt template que instruya al modelo a ignorar lo desactualizado",
        "Agregar un metadata filter que restringe por modification time",
        "Fijar el tipo de b&uacute;squeda en semantic para emparejar por significado",
        "Habilitar query modification para reescribir la consulta",
    ],
    correct=1,
    key="off2-q36",
    answer=(
        '<div class="verdict">Correcta: {{L}} - metadata filter por modification time.</div>'
        '<p><b>El problema:</b> controlar <b>que documentos se recuperan</b> segun su antiguedad. La recuperacion se filtra con metadata filters, no con instrucciones al modelo.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>metadata filter</b> por <code>modification_time</code> restringe los documentos fuente segun su timestamp, de modo que el modelo solo recupere los actualizados recientemente. Es el mecanismo correcto para filtrar por recencia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Prompt template para ignorar lo viejo:</b> los prompts controlan como responde el modelo, pero no que documentos recupera; el filtrado de recuperacion se hace con metadata filters.</li>'
        '<li><b>Busqueda semantica:</b> empareja por significado y no por recencia; sin un metadata filter, el modelo puede seguir recuperando documentos antiguos.</li>'
        '<li><b>Query modification:</b> mejora el manejo de preguntas complejas o multipartes, pero no afecta que documentos se recuperan segun su antiguedad.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Recuperar solo lo reciente: metadata filter por modification time. Los prompts no controlan la recuperacion; la busqueda semantica no filtra por recencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html">docs.aws metadata filtering en Knowledge Bases</a></div>'
    ),
))


# ============================================================
# Q38 - SageMaker shadow test (metricas operativas sin afectar usuarios)
# ============================================================
cards.append(card(
    question="En un endpoint real-time de SageMaker hay una nueva version del modelo y se deben evaluar sus metricas operativas bajo trafico real sin afectar usuarios, con el MENOR esfuerzo. &iquest;Que solucion cumple?",
    options=[
        "A/B testing con los pesos de las production variants del endpoint",
        "SageMaker Model Monitor para evaluar el nuevo modelo",
        "Desplegar la nueva version en un shadow test de SageMaker",
        "Endpoint separado de SageMaker con enrutamiento personalizado",
    ],
    correct=2,
    key="off2-q38",
    answer=(
        '<div class="verdict">Correcta: {{L}} - shadow test de SageMaker AI.</div>'
        '<p><b>El problema:</b> medir metricas operativas del modelo nuevo con trafico real sin exponer a los usuarios, con minimo esfuerzo. Shadow test = desplegar una variante en sombra que recibe una copia del trafico pero no devuelve respuestas al usuario.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>shadow test</b> despliega la variante nueva junto a la de produccion en el mismo endpoint; la variante en sombra recibe una copia del trafico de produccion pero <b>no</b> responde a los usuarios. Asi se comparan latencia, tasa de errores y uso de recursos sin riesgo, y SageMaker maneja la replicacion de trafico y la recoleccion de metricas (no hay que montar infraestructura aparte).</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>A/B testing con pesos de variants:</b> expone a usuarios finales al modelo nuevo antes de validar sus metricas operativas; sirve para metricas de negocio con feedback de usuarios, no para evaluar sin afectar el trafico.</li>'
        '<li><b>Model Monitor:</b> detecta data drift y problemas de calidad, pero no compara metricas operativas entre versiones bajo trafico real; ademas exigiria desplegar el modelo a usuarios primero.</li>'
        '<li><b>Endpoint separado + enrutamiento custom:</b> no impacta usuarios, pero hay que construir y mantener la logica de enrutamiento propia; mas esfuerzo operativo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Evaluar metricas operativas con trafico real sin afectar usuarios: shadow test (copia del trafico, no responde al usuario). A/B expone usuarios; Model Monitor es para drift; el endpoint separado exige enrutamiento propio.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-shadow-deployment.html">docs.aws SageMaker shadow tests</a></div>'
    ),
))

# ============================================================
# Q39 - API Gateway REST non-proxy + mapping templates + Secrets Manager + cache
# ============================================================
cards.append(card(
    question="Enrutar a distintos LLM (Bedrock y terceros) sin cambios de c&oacute;digo es el objetivo, y se necesitan API keys seguras, formato consistente y cache. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "REST API non-proxy con mapping templates, stage variables y keys en Secrets Manager",
        "Todos los modelos en endpoints de SageMaker, enrutamiento por path",
        "REST API con integracion Lambda proxy, keys en Secrets Manager",
        "REST APIs separadas por proveedor, keys y cache en el cliente",
    ],
    correct=0,
    key="off2-q39",
    answer=(
        '<div class="verdict">Correcta: {{L}} - API Gateway REST non-proxy + mapping templates + Secrets Manager + cache.</div>'
        '<p><b>El problema:</b> multi-proveedor con cambio sin tocar codigo, formato consistente, keys seguras y cache. Integracion <b>non-proxy</b> = API Gateway transforma la peticion/respuesta con <b>mapping templates</b> (VTL) antes y despues de llamar al backend, sin codigo.</p>'
        '<p><b>Por que la respuesta sirve:</b> las integraciones <b>non-proxy</b> con <b>mapping templates</b> transforman peticiones y respuestas por proveedor sin cambios de codigo; el <b>enrutamiento por header</b> combinado con <b>stage variables</b> selecciona el proveedor de forma dinamica; los mapping templates dan un formato de respuesta consistente entre proveedores; <b>Secrets Manager</b> guarda las API keys de forma segura; y el <b>caching integrado</b> de API Gateway optimiza costos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Todo en SageMaker endpoints:</b> obliga a desplegar todos los modelos en SageMaker, asi que no soporta APIs de terceros; el enrutamiento por path es menos flexible y la configuracion de SageMaker no esta pensada para gestionar credenciales de multiples proveedores de forma segura.</li>'
        '<li><b>Lambda proxy:</b> la integracion proxy pasa la peticion entera a la Lambda, que maneja el enrutamiento; agregar proveedores exige cambios de codigo en la funcion y no hay caching integrado para optimizar costos.</li>'
        '<li><b>APIs separadas + enrutamiento cliente:</b> pone la logica y las API keys en el codigo cliente (vulnerabilidad) y depende del cache del cliente, con desempeno inconsistente entre sesiones.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Multi-proveedor sin cambios de codigo, formato uniforme, keys seguras y cache: integraciones non-proxy con mapping templates + stage variables + un gestor de secretos + caching integrado. La integracion proxy exige codigo por proveedor; las keys en el cliente son inseguras.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/models-mappings.html">docs.aws API Gateway mapping templates</a></div>'
    ),
))

# ============================================================
# Q40 - BDA: un proyecto con multiples blueprints (auto-seleccion)
# ============================================================
cards.append(card(
    question="Facturas PDF de luz, agua y gas llegan con formato propio, y al subir a S3 hay que identificar el tipo y extraer los campos, con el MENOR esfuerzo. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Rekognition Custom Labels y tres proyectos BDA con InvokeDataAutomationAsync",
        "Un proyecto BDA con multiples blueprints que autoselecciona el blueprint",
        "Rekognition Custom Labels y Textract AnalyzeDocument con Python propio",
        "Tres proyectos BDA separados que autoseleccionan el proyecto",
    ],
    correct=1,
    key="off2-q40",
    answer=(
        '<div class="verdict">Correcta: {{L}} - un solo proyecto BDA con multiples blueprints.</div>'
        '<p><b>El problema:</b> autoidentificar el tipo de factura y extraer sus campos con minimo esfuerzo. BDA = servicio gestionado de procesamiento de documentos; un blueprint = plantilla que define estructura y reglas para un tipo de documento.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>unico proyecto BDA con varios blueprints</b> (uno por tipo de factura, con su descripcion y campos) permite que BDA <b>autoseleccione</b> el blueprint segun el tipo de documento y extraiga los campos. Un solo proyecto simplifica la gestion sin codigo custom ni orquestar varios servicios: minimo esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Rekognition Custom Labels + 3 proyectos BDA:</b> hay que mantener un modelo Custom Labels y varios proyectos BDA; usar dos servicios (Rekognition y Bedrock) para clasificar suma complejidad sin beneficio.</li>'
        '<li><b>Custom Labels + Textract + Python:</b> exige entrenar y mantener un modelo de vision propio, mantener codigo Python de extraccion y orquestar Rekognition, Textract y Lambda; cambios de formato obligan a reentrenar y actualizar codigo.</li>'
        '<li><b>Tres proyectos BDA separados con auto-seleccion:</b> BDA <b>no</b> soporta autoseleccion de proyecto; cada documento debe procesarse contra un proyecto especifico, asi que este enfoque no funciona.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Varios tipos de documento con auto-clasificacion y minimo esfuerzo: un proyecto BDA con multiples blueprints (autoselecciona el blueprint, no el proyecto). Agregar Rekognition/Textract suma servicios y codigo que mantener.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/bda-projects.html">docs.aws proyectos y blueprints de BDA</a></div>'
    ),
))

# ============================================================
# Q41 - Guardrails + model cards en S3 + InvocationsIntervened + EventBridge
# ============================================================
cards.append(card(
    question="Moderar PII, odio y contenido inseguro (texto e imagen), documentar sesgos del FM con versionado y disparar cumplimiento en segundos tras intervenir es lo que se necesita. &iquest;Qu&eacute; cumple con el MENOR esfuerzo?",
    options=[
        "Comprehend para PII, Guardrails para el resto, versionado en DynamoDB con GSI",
        "Guardrails multimodal, Rekognition propio y model cards en S3 en paralelo",
        "Guardrails multimodal, model cards en S3 con lifecycle y parseo de CloudTrail",
        "Guardrails multimodal, model cards versionadas en S3, alarma InvocationsIntervened y EventBridge",
    ],
    correct=3,
    key="off2-q41",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails + model cards versionadas en S3 + alarma InvocationsIntervened + EventBridge.</div>'
        '<p><b>El problema:</b> moderacion inmediata multimodal, documentacion versionada del FM y respuesta event-driven en segundos, con minimo esfuerzo. InvocationsIntervened = metrica de Guardrails que cuenta las intervenciones (bloqueos).</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Guardrails</b> filtra texto y contenido multimodal y detecta/previene violaciones de inmediato con poca configuracion. Se usan <b>model cards versionadas en S3</b> para documentar sesgos y limitaciones, una <b>alarma de CloudWatch</b> sobre la metrica integrada <b>InvocationsIntervened</b> y una <b>regla de EventBridge</b> que dispara un workflow de cumplimiento en Lambda al activarse la alarma. Todo con funciones integradas: minimo esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Comprehend + DynamoDB (GSI):</b> Comprehend duplica la deteccion de PII que Guardrails ya trae; DynamoDB no da el versionado de documentos necesario para model cards aunque tenga GSI, y aqui EventBridge se plantea como monitoreo periodico, no en tiempo real, incumpliendo la respuesta inmediata.</li>'
        '<li><b>Rekognition redundante:</b> Guardrails ya soporta deteccion de toxicidad multimodal en imagenes, asi que Rekognition es redundante; el procesamiento en paralelo entre Bedrock y Rekognition agrega latencia, complejidad, puntos de fallo y duplica costos, e impide el bloqueo inmediato.</li>'
        '<li><b>Parsear logs de CloudTrail + lifecycle S3:</b> parsear CloudTrail para hallar violaciones suma esfuerzo y retrasos, y las lifecycle policies de S3 no dan el control de versiones que la documentacion del modelo requiere.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Moderacion inmediata + documentacion versionada + reaccion en segundos: Guardrails + model cards versionadas en S3 + una alarma sobre la metrica de intervenciones que dispara un workflow por evento. Comprehend/Rekognition son redundantes con Guardrails; parsear CloudTrail agrega latencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-monitor.html">docs.aws monitoreo de Guardrails (InvocationsIntervened)</a></div>'
    ),
))

# ============================================================
# Q42 - S3 metadata (system/user) + tags jerarquicos + OpenSearch con vectores
# ============================================================
cards.append(card(
    question="Millones de papers en S3 deben registrar fechas, autor&iacute;a y clasificaci&oacute;n multinivel, con filtrado combinado y contexto para los FM. &iquest;Qu&eacute; dise&ntilde;o de metadatos es MAS r&aacute;pido?",
    options=[
        "Timestamps user metadata; autor&iacute;a y clasificaciones en DynamoDB; tags; OpenSearch",
        "Timestamps system metadata; autor&iacute;a user metadata; tags jer&aacute;rquicos; OpenSearch con document vectors",
        "Guardar todos los metadatos en DynamoDB, papers m&iacute;nimos en S3 y features en SageMaker Feature Store",
        "Timestamps system metadata; autor&iacute;a en RDS for PostgreSQL; buscar con Amazon Kendra",
    ],
    correct=1,
    key="off2-q42",
    answer=(
        '<div class="verdict">Correcta: {{L}} - system metadata (fechas) + user metadata (autoria) + tags jerarquicos + OpenSearch con vectores.</div>'
        '<p><b>El problema:</b> diseno de metadatos con fechas, autoria, clasificacion multinivel, filtrado combinado y contexto para FMs, buscando la consulta mas rapida. En S3: system-defined metadata (timestamps del sistema) y user-defined metadata (definida por el usuario); object tags para clasificar.</p>'
        '<p><b>Por que la respuesta sirve:</b> los <b>timestamps como system metadata</b> dan un rastreo confiable de fechas; la <b>autoria como user metadata</b> se guarda de forma eficiente; una <b>estructura jerarquica de object tags</b> soporta la clasificacion cientifica multinivel; y <b>OpenSearch enriquecido con document vectors de Bedrock</b> aporta busqueda semantica potente. Da gestion eficiente de metadatos y la respuesta de consulta mas rapida para filtrado avanzado y busqueda semantica sobre millones de documentos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Timestamps como user metadata + tags solo de alto nivel + DynamoDB:</b> guardar timestamps como user metadata limita el querying complejo, y usar tags solo para disciplinas de alto nivel no soporta la clasificacion granular multinivel; ademas falta la capacidad de busqueda semantica para el FM.</li>'
        '<li><b>Todo en DynamoDB + Feature Store:</b> DynamoDB soporta varios patrones, pero separar todos los metadatos de los documentos dificulta la consistencia, y Feature Store es para features de ML, no para preparar metadatos.</li>'
        '<li><b>RDS PostgreSQL + Kendra:</b> una base relacional aparte plantea retos de sincronizacion, y los document attributes de Kendra no dan las capacidades vectoriales optimizadas que las interacciones con el FM requieren.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Metadatos ricos + busqueda rapida y semantica: system metadata (fechas) + user metadata (autoria) + object tags jerarquicos + un motor de busqueda enriquecido con document vectors. DynamoDB/RDS separados generan sincronizacion; Kendra no da vectores optimizados.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html">docs.aws metadatos de objetos en S3</a></div>'
    ),
))


# ============================================================
# Q45 - Hierarchical chunking para manuales tecnicos anidados
# ============================================================
cards.append(card(
    question="Un RAG para manuales de aviones maneja PDFs enormes con secciones anidadas y referencias cruzadas, y necesita alta precisi&oacute;n de recuperaci&oacute;n. &iquest;Qu&eacute; soluci&oacute;n cumple con el MENOR esfuerzo?",
    options=[
        "Knowledge Bases con hierarchical chunking y OpenSearch Serverless",
        "Knowledge Bases con semantic chunking y OpenSearch Serverless",
        "DocumentDB serverless y OpenSearch Serverless con neural plugin",
        "DocumentDB serverless, Knowledge Bases con semantic chunking, DocumentDB store",
    ],
    correct=0,
    key="off2-q45",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Knowledge Bases con hierarchical chunking + OpenSearch Serverless.</div>'
        '<p><b>El problema:</b> RAG gestionado y de alta precision para documentacion tecnica con estructura anidada y referencias cruzadas, con minimo esfuerzo. Hierarchical chunking = chunking que respeta la jerarquia (secciones y subsecciones) del documento.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Knowledge Bases</b> es un flujo RAG gestionado de extremo a extremo que se integra con <b>OpenSearch Serverless</b> como vector store, soporta S3 como fuente y soporta <b>hierarchical chunking</b>. El hierarchical chunking es el mas adecuado para documentos con estructura jerarquica como los manuales tecnicos, y da alta precision de recuperacion con el menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Knowledge Bases con semantic chunking:</b> flujo gestionado, pero el semantic chunking no es adecuado para documentacion anidada con referencias cruzadas; puede partir el contenido en fronteras importantes y romper relaciones entre procedimientos y repuestos, bajando la precision.</li>'
        '<li><b>DocumentDB + OpenSearch neural plugin:</b> DocumentDB no esta optimizado para grandes PDFs y no es un flujo RAG gestionado; crear un hierarchical chunking custom exige codigo para chunking, embeddings e integracion de busqueda por separado, sumando esfuerzo.</li>'
        '<li><b>DocumentDB como vector store + semantic chunking:</b> DocumentDB no esta optimizado para PDFs grandes y Knowledge Bases no lo soporta como fuente; ademas el semantic chunking rompe la jerarquia y reduce la precision.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Documentacion tecnica anidada con alta precision y minimo esfuerzo: Knowledge Bases + hierarchical chunking + OpenSearch Serverless. El semantic chunking rompe jerarquias; DocumentDB no es fuente de KB ni store optimo para PDFs.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws hierarchical chunking en Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q51 - Bedrock Prompt Management + Bedrock Flows (encadenar 3 LLM)
# ============================================================
cards.append(card(
    question="Un equipo debe encadenar 3 llamadas a LLM con Bedrock Flows, versionar los prompts y hacer rollback r&aacute;pido, con el MENOR esfuerzo. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Knowledge base, prompts en Parameter Store y encadenado con Flows",
        "Knowledge base, prompts en Prompt Management y encadenado con Step Functions",
        "Knowledge base, prompts en Prompt Management (versiona y hace rollback)",
        "Amazon Q Business, prompts en Prompt Management y encadenado con Flows",
    ],
    correct=2,
    key="off2-q51",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Knowledge base + Prompt Management + Bedrock Flows.</div>'
        '<p><b>El problema:</b> encadenar 3 LLM, versionar prompts y hacer rollback rapido, con minimo desarrollo. Bedrock Flows = servicio visual para encadenar varias llamadas a LLM; Prompt Management = ciclo de vida y versionado de prompts.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>knowledge base</b> conecta el LLM con los datos del producto, <b>Prompt Management</b> almacena y versiona los prompts de las 3 llamadas (permitiendo rollback rapido) y <b>Bedrock Flows</b> encadena visualmente las 3 llamadas en secuencia. Cumple encadenar, versionar y recuperar de la base de productos con el menor desarrollo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Prompts en Parameter Store + Flows:</b> Parameter Store versiona y permite rollback, pero no esta pensado para almacenar prompts de LLM; no es el servicio adecuado para ese caso.</li>'
        '<li><b>Prompt Management + Step Functions:</b> versiona bien los prompts, pero con Step Functions hay que crear y mantener el workflow y las task functions; mas esfuerzo de desarrollo que Flows.</li>'
        '<li><b>Amazon Q Business + Prompt Management + Flows:</b> Amazon Q Business es un asistente low-code que gestiona sus prompts y flujos internamente y esos no se versionan con Prompt Management; no encaja con el requisito de versionado.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Encadenar LLM + versionar prompts + rollback con minimo desarrollo: Prompt Management + Bedrock Flows. Parameter Store no es para prompts; Step Functions suma workflow propio; Q Business no versiona sus prompts con Prompt Management.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html">docs.aws Amazon Bedrock Flows</a></div>'
    ),
))

# ============================================================
# Q53 - Strands Agents (agentes especialistas, dinamico)
# ============================================================
cards.append(card(
    question="Un asistente resuelve un paso pero falla en multi-paso. Se quiere IA agentica que se ajuste dinamicamente ante fallos, con el MENOR esfuerzo. &iquest;Que enfoque de orquestacion cumple?",
    options=[
        "Strands Agents SDK: un agente especialista por tarea (BillingAgent) como Lambda",
        "EventBridge Pipes: una Lambda con un FM interpreta y pasa a Lambdas por tarea",
        "Step Functions con un estado choice y una Lambda por tarea que llama a Bedrock",
        "Un unico Bedrock Agent con esquema OpenAPI y Lambdas como tools (BillingTool)",
    ],
    correct=0,
    key="off2-q53",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Strands Agents SDK con agentes especialistas.</div>'
        '<p><b>El problema:</b> orquestar tareas multi-paso con ajuste dinamico ante fallos, con minimo desarrollo. Strands Agents = framework para componer y orquestar varios agentes GenAI especializados.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Strands Agents</b> compone y orquesta multiples agentes especializados (un BillingAgent para cambios de plan, etc.) desplegados como Lambdas y registrados en Strands, con un flujo que los recorre en la secuencia correcta. Simplifica patrones multi-agente que serian dificiles con un solo agente, y permite el manejo dinamico de errores pedido.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>EventBridge Pipes:</b> conecta fuentes con destinos en un solo sentido (source -> enrichment -> target); no tiene ramificacion, toma de decisiones ni ejecucion condicional, asi que no sirve para estas consultas.</li>'
        '<li><b>Step Functions:</b> orquesta procesos deterministas y predecibles; este escenario requiere interacciones conversacionales dinamicas con combinaciones impredecibles de tareas, dificiles de definir con Step Functions.</li>'
        '<li><b>Un unico Bedrock Agent:</b> los agentes unicos sirven para tareas enfocadas; con muchas tareas es dificil de controlar y probar (cada tarea puede necesitar otra configuracion) y no da orquestacion fiable con logica condicional y manejo de errores.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Multi-paso dinamico con manejo de errores y minimo desarrollo: un framework multi-agente que compone agentes especialistas. EventBridge Pipes es unidireccional; Step Functions es determinista; un solo agente no orquesta bien muchas tareas.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html">docs.aws agentes en Amazon Bedrock</a></div>'
    ),
))

# ============================================================
# Q54 - AgentCore Runtime + Strands + prebuilt MCP server (Aurora)
# ============================================================
cards.append(card(
    question="Consultas en lenguaje natural que invocan procesos de supply chain necesitan soporte MCP integrado y m&iacute;nimo mantenimiento, con inventario en Aurora. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "AgentCore Runtime y Strands Agents con un prebuilt MCP server sobre Aurora",
        "Amazon Lex, una Lambda que empuja a SQS y microservicios en ECS sobre Fargate",
        "MCP server propio en ECS sobre Fargate que conecta a Aurora, con un agente Bedrock",
        "API Gateway delante de una Lambda que consulta Aurora e invoca Step Functions",
    ],
    correct=0,
    key="off2-q54",
    answer=(
        '<div class="verdict">Correcta: {{L}} - AgentCore Runtime + Strands + prebuilt MCP server.</div>'
        '<p><b>El problema:</b> agente en lenguaje natural con soporte MCP integrado y minimo mantenimiento sobre datos en Aurora. MCP (Model Context Protocol) = protocolo estandar para exponer datos/herramientas a agentes; un prebuilt MCP server ya viene listo para usar.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AgentCore Runtime con Strands Agents</b> permite construir agentes con soporte MCP integrado, y un <b>prebuilt MCP server</b> expone directamente los datos de inventario de Aurora como MCP tools, sin contenedores ni gestion de APIs propias. Bedrock maneja la orquestacion y el hosting, asi que automatiza las acciones de supply chain con el menor esfuerzo operativo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Amazon Lex + SQS + ECS:</b> da lenguaje natural, pero no ofrece el soporte MCP integrado requerido e introduce varios componentes que gestionar (Lambda, SQS, ECS); mas esfuerzo operativo.</li>'
        '<li><b>MCP server propio en ECS/Fargate:</b> conecta a Aurora, pero hay que construir, desplegar y escalar un MCP containerizado propio; mas esfuerzo que el prebuilt MCP de AgentCore.</li>'
        '<li><b>API Gateway + Lambda + Step Functions:</b> requiere construir y mantener la arquitectura, no usa MCP y exige definiciones de API y coordinacion de workflow manuales.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Lenguaje natural con MCP integrado y minimo mantenimiento: un runtime de agentes gestionado con un prebuilt MCP server que expone la base de datos como tools. Un MCP server propio en contenedores o soluciones sin MCP suman operacion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html">docs.aws Amazon Bedrock AgentCore</a></div>'
    ),
))

# ============================================================
# Q55 - CreateEvaluationJob con evaluator model + Spearman (Lambda)
# ============================================================
cards.append(card(
    question="Un equipo debe evaluar varios FM en calidad, seguridad y juicio tipo humano a escala, con validaci&oacute;n estad&iacute;stica de las diferencias y evaluadores gestionados. &iquest;Qu&eacute; soluci&oacute;n cumple con el MENOR esfuerzo?",
    options=[
        "CreateEvaluationJob con evaluator model consistente y Spearman en Lambda",
        "Batch inference para generar, luego LLM-as-a-judge propio y Spearman en Lambda",
        "Batch inference con Guardrails, monitorear InvocationsIntervened y patrones",
        "CreateEvaluationJob con task type question-answering y datasets en JSONL",
    ],
    correct=0,
    key="off2-q55",
    answer=(
        '<div class="verdict">Correcta: {{L}} - CreateEvaluationJob con evaluator model consistente + Spearman en Lambda.</div>'
        '<p><b>El problema:</b> evaluar calidad, utilidad y seguridad con juicio tipo humano a escala y validar estadisticamente las diferencias, con minimo esfuerzo. Evaluator model = modelo gestionado que juzga las respuestas; correlacion de Spearman = medida estadistica de consistencia de rangos.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>CreateEvaluationJob API</b> con un <b>evaluator model consistente</b> corre jobs gestionados que escalan a datasets grandes y dan juicio tipo humano sobre aspectos matizados (relevancia, tono, exactitud) mas metricas de IA responsable con intervalos de confianza. Los resultados van a S3 y una <b>Lambda</b> aplica <b>correlacion de Spearman</b> para comparar estadisticamente los modelos. Usa el framework gestionado: minimo esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Batch inference + LLM-as-a-judge propio:</b> da evaluacion matizada, pero hay que correr jobs separados de generacion y evaluacion y gestionar varios pipelines y orquestacion; mas esfuerzo operativo.</li>'
        '<li><b>Batch inference + Guardrails + InvocationsIntervened:</b> se enfoca solo en seguridad; no evalua calidad, utilidad ni tono, y analizar patrones de intervencion no da el juicio tipo humano requerido.</li>'
        '<li><b>CreateEvaluationJob con task type question-answering:</b> produce metricas estandar de exactitud factual; no aporta el juicio tipo humano para tono, adecuacion contextual o utilidad, ni las evaluaciones de IA responsable/seguridad integrales.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Evaluar a escala con juicio tipo humano y validacion estadistica, minimo esfuerzo: CreateEvaluationJob con evaluator model consistente + Spearman en Lambda. El task type question-answering solo da exactitud factual; Guardrails solo mide seguridad.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws model evaluation (CreateEvaluationJob)</a></div>'
    ),
))


# ============================================================
# Q57 - Cuota de 1.000 prompts por dataset de evaluacion
# ============================================================
cards.append(card(
    question="Un dataset de 5.000 prompts en JSONL hace que el job de automatic model evaluation no arranque, con error de configuracion del dataset. &iquest;Que enfoque resuelve el problema?",
    options=[
        "Habilitar versioning en el bucket S3 y actualizar CORS para la consola",
        "Dividir en datasets de maximo 1.000 prompts y correr jobs separados",
        "Convertir el dataset de JSONL a CSV y reintentar",
        "Comprimir el archivo con gzip y reintentar apuntando al comprimido",
    ],
    correct=1,
    key="off2-q57",
    answer=(
        '<div class="verdict">Correcta: {{L}} - dividir en datasets de hasta 1.000 prompts.</div>'
        '<p><b>El problema:</b> el job falla por la <b>configuracion del dataset</b>. Los jobs de automatic model evaluation de Bedrock tienen una <b>cuota de 1.000 prompts por dataset</b>, y 5.000 la exceden.</p>'
        '<p><b>Por que la respuesta sirve:</b> como la cuota es de <b>1.000 prompts por dataset</b>, dividir los 5.000 en cinco datasets de 1.000 y correr jobs separados respeta el limite y resuelve el fallo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Versioning + CORS:</b> CORS es requisito para jobs creados desde consola (acceso del navegador) y el versioning no se relaciona con el fallo; ninguna atiende el limite de tamano del dataset.</li>'
        '<li><b>Convertir a CSV:</b> la evaluacion exige el dataset en JSONL con extension .jsonl; pasar a CSV crea una incompatibilidad de formato en vez de resolver.</li>'
        '<li><b>Comprimir con gzip:</b> el problema es la <b>cantidad</b> de prompts, no el tamano de archivo; comprimir no evita la cuota, Bedrock procesa la misma cantidad de prompts.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Job de evaluacion que no arranca por dataset: recuerda la cuota de 1.000 prompts por dataset (divide y corre varios jobs). El formato debe ser JSONL; comprimir o cambiar a CSV no ayuda.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation-prompt-datasets-custom.html">docs.aws datasets de prompts para evaluacion</a></div>'
    ),
))

# ============================================================
# Q61 - AWS Config custom rule (RDK) para SSE-KMS con CMK
# ============================================================
cards.append(card(
    question="Asegurar que los datasets de training usen KMS customer managed keys, rechazar claves de AWS o sin cifrar y validar continuamente los existentes es la meta. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Amazon Macie para escanear S3 y reportar los que no usan CMK",
        "EventBridge ante PutObject dispara Step Functions que verifica CMK y notifica por SNS",
        "AWS Config custom rule (RDK) que verifica SSE-KMS con CMK y remedia",
        "Lambda por EventBridge con Athena sobre CloudTrail para hallar PutObject sin aws:kms",
    ],
    correct=2,
    key="off2-q61",
    answer=(
        '<div class="verdict">Correcta: {{L}} - AWS Config custom rule (RDK) para SSE-KMS con CMK.</div>'
        '<p><b>El problema:</b> validar de forma <b>continua</b> que los buckets existentes cifran con customer managed key (CMK) y remediar los no conformes. AWS Config = evalua continuamente la configuracion de los recursos; RDK = kit para escribir reglas custom de Config.</p>'
        '<p><b>Por que la respuesta sirve:</b> una <b>Config custom rule con RDK</b> aplica compliance-as-code: revisa continuamente los buckets de datos de entrenamiento para determinar si usan <b>SSE-KMS con una customer managed key</b> y soporta remediacion automatica (por ejemplo, via Systems Manager). Verifica y fuerza el uso de CMK de forma continua, cumpliendo las buenas practicas de IA responsable.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Amazon Macie:</b> se usa sobre todo para descubrir datos sensibles (como PII); no es lo mas adecuado para el cumplimiento continuo de una politica de cifrado con CMK.</li>'
        '<li><b>EventBridge + Step Functions por PutObject:</b> liga el chequeo al pipeline y evita usar datos no cifrados a futuro, pero solo aplica a <b>archivos nuevos</b> individuales, no a la politica de cifrado del bucket; no garantiza cumplimiento continuo de todos los buckets.</li>'
        '<li><b>Lambda + Athena sobre CloudTrail:</b> da visibilidad de PutObject sospechosos, pero no puede forzar el uso de CMK; CloudTrail registra llamadas de API, no la configuracion de cifrado del bucket ni las politicas de CMK aplicadas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cumplimiento continuo de cifrado con CMK en buckets: una regla custom del servicio de evaluacion de configuracion, con remediacion automatica. Los enfoques por PutObject solo ven archivos nuevos; CloudTrail no registra la config de cifrado del bucket; Macie es para datos sensibles.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules.html">docs.aws AWS Config custom rules (RDK)</a></div>'
    ),
))

# ============================================================
# Q63 - Model invocation logging para depurar clasificaciones
# ============================================================
cards.append(card(
    question="Triage de tickets (Bedrock InvokeModel) - con un prompt bien estructurado (categorias, ejemplos, validacion) hay clasificaciones inesperadas <b>intermitentes</b>. Se necesita hallar la <b>causa raiz</b> de esas anomalias. &iquest;Que enfoque cumple?",
    options=[
        "Usar CloudWatch Logs Insights para analizar los logs de la Lambda buscando patrones de error y respuestas del modelo",
        "Crear una metrica custom de CloudWatch que rastree la distribucion de categorias y una alarma ante picos o nulos",
        "Habilitar el model invocation logging de Amazon Bedrock para inspeccionar los prompts crudos y las respuestas del FM",
        "Trazas de AWS X-Ray para ver timeouts o throttling entre la Lambda y las llamadas a la API de Bedrock",
    ],
    correct=2,
    key="off2-q63",
    answer=(
        '<div class="verdict">Correcta: {{L}} - model invocation logging de Bedrock.</div>'
        '<p><b>El problema:</b> encontrar por que ocurren clasificaciones inesperadas intermitentes, pese a un prompt bien estructurado y con validacion. Model invocation logging = registro detallado de las interacciones con el modelo (prompts y respuestas).</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>model invocation logging</b> registra el detalle de cada interaccion, incluyendo el <b>prompt crudo enviado</b> y la <b>respuesta recibida</b>. Permite analizar directamente los casos anomalos e identificar patrones o condiciones que llevaron a la clasificacion inesperada; es la vista mas directa del comportamiento intermitente del modelo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CloudWatch Logs Insights:</b> sirve para errores y excepciones a nivel de la funcion, pero no da visibilidad de las interacciones especificas con el modelo que causan las anomalias.</li>'
        '<li><b>Metrica custom de distribucion:</b> ayuda a detectar <b>cuando</b> ocurren las anomalias, pero no <b>por que</b>; el sistema ya valida y sigue buenas practicas, asi que hace falta ver las interacciones concretas.</li>'
        '<li><b>X-Ray:</b> identifica latencia, timeouts o throttling en la integracion de servicios, pero la causa esta en interacciones especificas del modelo, no en la integracion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Depurar clasificaciones raras intermitentes: model invocation logging (ves prompt y respuesta crudos). Las metricas dicen cuando, no por que; X-Ray es para latencia/throttling, no para el contenido del modelo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html">docs.aws model invocation logging</a></div>'
    ),
))

# ============================================================
# Q64 - MCP server para estandarizar API legacy del CMS
# ============================================================
cards.append(card(
    question="Automatizacion de contenido - varios agentes de IA fallan con la API de un CMS legacy de endpoints inconsistentes y esquemas mal documentados. Estandarizar, mantener los endpoints existentes y que sea reutilizable entre agentes, con el MENOR esfuerzo operativo. &iquest;Que solucion cumple?",
    options=[
        "Nueva capa REST de transformacion que estandariza las respuestas y publica OpenAPI, como proxy entre los agentes y el CMS",
        "Refactorizar la API del CMS legacy a REST moderno con esquemas consistentes y migrar todos los agentes a los nuevos endpoints",
        "Un Model Context Protocol (MCP) server con interfaz estandar al CMS y function schemas que manejan las inconsistencias, con AgentCore",
        "Middleware custom que transforma peticiones del CMS, como contenedor sidecar junto a cada agente para manejar las inconsistencias",
    ],
    correct=2,
    key="off2-q64",
    answer=(
        '<div class="verdict">Correcta: {{L}} - un MCP server que estandariza el acceso al CMS.</div>'
        '<p><b>El problema:</b> dar a los agentes una interfaz consistente y reutilizable sobre una API legacy inconsistente, manteniendo los endpoints existentes, con minimo esfuerzo. MCP = protocolo estandar para que modelos y agentes interactuen con herramientas y APIs externas via function calling.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>MCP server</b> da una interfaz consistente al CMS mediante <b>function schemas</b>, y la implementacion de esas funciones maneja internamente las inconsistencias de la API, abstrayendo la complejidad. Es <b>reutilizable</b> entre distintos workflows (todos usan las mismas funciones MCP) y los cambios de API o nuevos edge cases se actualizan en un solo lugar central, reduciendo integracion y esfuerzo operativo. AgentCore interactua con el CMS via esas funciones.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Capa REST de transformacion como proxy:</b> mejora documentacion y estandariza respuestas, pero no atiende las necesidades de los agentes, exige integracion custom por agente, puede sumar latencia y no ofrece la interfaz de function calling ni la comprension semantica de MCP.</li>'
        '<li><b>Refactorizar el CMS:</b> requiere cambios grandes que pueden romper la compatibilidad con apps legacy, no da la interfaz de function calling para agentes y obliga a actualizar todos los agentes; mucho esfuerzo.</li>'
        '<li><b>Middleware sidecar por agente:</b> resuelve el sintoma, pero no escala ni es mantenible: hay que desplegar y mantener middleware separado por cada agente, sumando esfuerzo, y no usa la interfaz estandar de function calling.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Estandarizar una API legacy para varios agentes, reutilizable y con minimo esfuerzo: un servidor de protocolo estandar con function schemas y cambios en un solo lugar central. Un proxy REST o un sidecar por agente exigen integracion o mantenimiento por agente.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html">docs.aws AgentCore y MCP</a></div>'
    ),
))

# ============================================================
# Q67 - Semantic chunking + prompt chaining para resumir
# ============================================================
cards.append(card(
    question="Resumen de documentos (Knowledge Bases) - con papers largos los resumenes omiten secciones criticas del medio o el final, aunque el texto se subio y tokenizo bien y no hay errores de API ni truncamiento. &iquest;Que solucion resuelve el problema?",
    options=[
        "Elegir un FM con ventana de contexto mas grande para procesar el documento completo en una inferencia, con compresion de texto",
        "Recuperar mas chunks del knowledge base, resumir cada uno de forma independiente y combinar en un resumen final",
        "Configurar semantic chunking en Bedrock, resumir cada segmento y usar prompt chaining para combinar los parciales en uno consolidado",
        "Standard chunking en Bedrock, segmentos de igual tamano, resumir cada uno de forma independiente y combinar",
    ],
    correct=2,
    key="off2-q67",
    answer=(
        '<div class="verdict">Correcta: {{L}} - semantic chunking + prompt chaining.</div>'
        '<p><b>El problema:</b> los resumenes pierden informacion del medio/final de documentos largos. Semantic chunking = segmentar por partes coherentes segun el significado; prompt chaining = encadenar prompts pasando la salida de un paso como entrada del siguiente.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>semantic chunking</b> segmenta el texto en partes coherentes, el modelo resume cada segmento por separado y el <b>prompt chaining</b> combina esos resumenes parciales en uno final consolidado. Asi se cubre todo el contenido y se evita el desbordamiento de la ventana de contexto, resolviendo la omision de secciones.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>FM con contexto mas grande + compresion:</b> una ventana mayor no afecta la recuperacion de chunks, y la compresion del lado del cliente puede eliminar detalles importantes y perder contexto critico.</li>'
        '<li><b>Recuperar mas chunks + resumir por separado:</b> aumenta cobertura, pero sin una estrategia para fusionar coherentemente puede dar resumenes fragmentados y omitir detalles que abarcan varios chunks; falta el paso de sintesis (como prompt chaining).</li>'
        '<li><b>Standard chunking:</b> el chunking de tamano fijo parte oraciones o separa ideas relacionadas, lo que produce resumenes con omisiones o sin cohesion, especialmente cuando el contexto abarca varios segmentos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Resumenes que omiten secciones de documentos largos: semantic chunking + prompt chaining (segmentar coherente y sintetizar). Ampliar el contexto o el standard chunking no resuelven la fragmentacion ni la cobertura.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws semantic chunking en Bedrock</a></div>'
    ),
))

# ============================================================
# Q68 - Custom chunking via Lambda + LangChain (jerarquia variable)
# ============================================================
cards.append(card(
    question="Preservar la relaci&oacute;n art&iacute;culo-p&aacute;rrafos y minimizar respuestas irrelevantes es la meta en un RAG sobre HTML con p&aacute;rrafos de longitud muy variable y jerarqu&iacute;a compleja. &iquest;Qu&eacute; soluci&oacute;n cumple?",
    options=[
        "Knowledge base de Bedrock con hierarchical chunking integrado, con parent y child chunks de tamanos estimados por la longitud promedio",
        "Amazon Textract para extraer el texto de los HTML, chunks por parrafo en S3 y un knowledge base con la opcion no chunking",
        "Una Lambda que implementa hierarchical chunking custom con LangChain, usada como configuracion de chunking custom del knowledge base",
        "Knowledge base de Bedrock con semantic chunking integrado, dividiendo por significado en vez de por estructura sintactica",
    ],
    correct=2,
    key="off2-q68",
    answer=(
        '<div class="verdict">Correcta: {{L}} - custom chunking via Lambda + LangChain.</div>'
        '<p><b>El problema:</b> preservar la jerarquia articulo-parrafos cuando la longitud de los parrafos es muy variable. Knowledge Bases permite chunking custom mediante una Lambda.</p>'
        '<p><b>Por que la respuesta sirve:</b> Knowledge Bases soporta <b>chunking custom via Lambda</b>. Una Lambda con <b>LangChain</b> implementa una estrategia jerarquica a medida capaz de manejar articulos y parrafos de cualquier longitud y de preservar las relaciones jerarquicas. Da el control y la flexibilidad necesarios para estructuras complejas y longitudes variables.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Hierarchical chunking integrado con tamanos promedio:</b> mantiene relaciones parent-child, pero fijar tamanos por el promedio es inadecuado con parrafos de longitud muy variable; parte contenido cuando los parrafos son mucho mayores o menores que el promedio y rompe relaciones.</li>'
        '<li><b>Textract + no chunking:</b> Textract es para documentos de imagen/PDF, no para HTML, y crear chunks sin considerar la jerarquia no mantiene la relacion articulo-parrafos; la opcion no chunking trata cada extraccion como unidad independiente y pierde contexto.</li>'
        '<li><b>Semantic chunking integrado:</b> divide por significado priorizando el contenido sobre la estructura, asi que puede romper la jerarquia articulo-parrafos y perder las relaciones explicitas necesarias.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Jerarquia con longitudes muy variables: chunking custom mediante una funcion propia con una libreria de procesamiento de HTML. El hierarchical integrado con tamanos promedio parte contenido variable; el semantic rompe la jerarquia; Textract no es para HTML.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws custom chunking en Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q71 - S3 presigned + EventBridge + Step Functions (Rekognition + Bedrock)
# ============================================================
cards.append(card(
    question="App de video - los usuarios suben videos cortos y se quiere <b>resumir contenido, generar transcripciones, detectar objetos e identificar celebridades</b> usando Amazon Rekognition (objetos/celebridades) y FMs de Bedrock (resumen/transcripcion), con el MENOR esfuerzo operativo y menor privilegio en la subida. &iquest;Como orquestar el flujo?",
    options=[
        "Disparar un blueprint de Bedrock Data Automation (BDA) desde una Event Notification, con presigned URL",
        "Un state machine de Step Functions que orquesta Lambdas, disparado por Event Notification tras un PutObject",
        "Lambdas en paralelo con Step Functions para reintentos, disparadas por Event Notification tras un PutObject",
        "EventBridge que invoca Step Functions con integracion directa de servicios, subiendo con presigned URL",
    ],
    correct=3,
    key="off2-q71",
    answer=(
        '<div class="verdict">Correcta: {{L}} - S3 presigned + EventBridge + Step Functions (integracion directa) + Rekognition + Bedrock.</div>'
        '<p><b>El problema:</b> orquestar analisis de video con minimo esfuerzo y siguiendo el principio de menor privilegio en la subida. Presigned URL = URL temporal para subir sin dar permisos IAM amplios; Step Functions puede llamar APIs de servicio directamente (sin Lambdas intermedias).</p>'
        '<p><b>Por que la respuesta sirve:</b> las <b>S3 presigned URLs</b> permiten subidas seguras respetando el menor privilegio; <b>S3 envia eventos a EventBridge</b> y una regla invoca un <b>Step Functions state machine</b> que orquesta llamando <b>directamente a las APIs de servicio</b> (sin Lambdas intermedias), reduciendo el esfuerzo. Usa <b>Rekognition</b> para deteccion de objetos y celebridades y <b>FMs de Bedrock</b> para resumen y transcripcion, maximizando capacidades gestionadas y minimizando codigo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Presigned + BDA blueprint:</b> las presigned URLs estan bien, pero BDA tiene limitaciones para flujos complejos de media y las S3 Event Notifications no pueden disparar blueprints de BDA directamente; requiere integracion custom.</li>'
        '<li><b>PutObject + Step Functions via Lambda:</b> PutObject exige permisos IAM directos (viola el menor privilegio), las S3 Event Notifications no invocan Step Functions directamente y usar Lambda intermedia suma esfuerzo operativo.</li>'
        '<li><b>PutObject + Lambdas en paralelo:</b> PutObject viola el menor privilegio y cada paso como Lambda separada crea sobrecarga operativa; ademas conviene Rekognition (vision especializada) para celebridades y objetos en vez de solo FMs.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Orquestar media con minimo esfuerzo y menor privilegio: subida con presigned URL, un bus de eventos que dispare un workflow con integracion directa de servicios, vision gestionada para objetos/celebridades y FMs para resumen/transcripcion. Las S3 Event Notifications no disparan un state machine ni BDA directamente; PutObject exige permisos amplios.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-services.html">docs.aws integraciones directas de servicio en Step Functions</a></div>'
    ),
))

# ============================================================
# Q72 - IAM Identity Center + Active Directory + failover regional
# ============================================================
cards.append(card(
    question="Servicios financieros (GenAI multi-cuenta con Bedrock) usan Microsoft Active Directory para autenticar empleados y dan acceso a los FM por departamento, con permisos consistentes entre cuentas y failover regional. &iquest;Qu&eacute; cumple con el MENOR esfuerzo?",
    options=[
        "Federacion SAML 2.0 con IAM en cada cuenta, roles con trust policies por departamento y condition keys que restringen los modelos",
        "Configurar AWS IAM Identity Center federado con Active Directory, permission sets de acceso a modelos por departamento y multi-cuenta con failover regional",
        "Configurar federacion entre Active Directory y Amazon Cognito, identity pools por departamento y AWS STS para asumir roles de acceso a Bedrock",
        "Crear usuarios IAM en cada cuenta que coinciden con Active Directory y roles cross-account por departamento con condition keys para Bedrock",
    ],
    correct=1,
    key="off2-q72",
    answer=(
        '<div class="verdict">Correcta: {{L}} - IAM Identity Center + Active Directory + failover regional.</div>'
        '<p><b>El problema:</b> federacion con Active Directory, permisos consistentes entre cuentas, control por departamento y resiliencia regional de la autenticacion, con minimo esfuerzo. IAM Identity Center = federacion de identidad centralizada con permission sets aplicables a varias cuentas.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>IAM Identity Center</b> ofrece federacion centralizada con Active Directory y <b>permisos consistentes entre cuentas</b> via permission sets. Soporta control de acceso por departamento a recursos como los modelos de Bedrock y provee <b>failover regional</b> para resiliencia. Cubre todos los requisitos con el menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SAML 2.0 con IAM en cada cuenta:</b> usa federacion, pero hay que mantener configuraciones SAML separadas por cuenta; no da una forma centralizada de gestionar permisos consistentes y se complica al escalar.</li>'
        '<li><b>Active Directory + Cognito:</b> Cognito puede federar con AD, pero esta pensado para apps orientadas a clientes, no para identidad de fuerza laboral entre varias cuentas; no centraliza permisos consistentes y suma esfuerzo.</li>'
        '<li><b>Usuarios IAM que replican AD:</b> crear usuarios IAM que espejen AD viola las buenas practicas al no usar federacion, crea credenciales de larga vida en vez de temporales, suma esfuerzo y no da resiliencia regional.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Federacion con AD, permisos consistentes multi-cuenta, control por departamento y resiliencia regional: el servicio centralizado de federacion de identidad con permission sets. La federacion SAML por cuenta no centraliza; Cognito es para clientes; usuarios IAM que espejan AD son credenciales de larga vida.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">docs.aws IAM Identity Center</a></div>'
    ),
))

create(deck_name="AIP-C01::Oficial-2", cards=cards, out_path="out/AIP-C01_Oficial2.apkg", do_import=False)
