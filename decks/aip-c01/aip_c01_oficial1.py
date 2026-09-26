#!/usr/bin/env python3
"""
AIP-C01::Oficial-1 - 68 preguntas de un examen de practica OFICIAL de AWS.

Construido a partir de decks/aip-c01/dedupe/official_to_generate_off1.json.
Fuente de alta calidad: cada opcion trae su rationale oficial, usado para
refutar cada distractor uno por uno en el dorso.

Reglas aplicadas (docs/DECK_STANDARDS.md al 100%, estilo decks/mla-c01/mla_c01_03.py):
- 1 carta por pregunta (solo la MCQ directa).
- Exactamente 4 opciones (las 68 fuentes ya venian con 4).
- Enunciado y opciones traducidos al espanol. Opciones nombran el concepto,
  sin glosa didactica (la explicacion va en el dorso).
- Espanol, HTML con entidades para acentos, sin em dashes.
- Verdict con {{L}} (nunca hardcodear la letra; el motor baraja y sustituye).
- El frente no filtra la respuesta. Anti-give-away: longitudes de opciones
  comparables (ninguna > 1.4x del promedio); se suben los distractores, no se
  acorta la correcta.
- Cada dorso: El problema / Por que la respuesta sirve / Por que NO las otras
  (una por una, refutando CADA distractor con el rationale oficial) / exam tip
  (sin nombrar un token exclusivo de la correcta) / links docs.aws.amazon.com.
- key estable y unica: off1-q<n> usando el numero n de la fuente.
- correct = indice 0-based (mismo orden de opciones que la fuente).
"""
from anki_mcq import card, create

cards = []



# ============================================================
# Q1 - BDA parser + structured data retrieval (RAG multimodal)
# ============================================================
cards.append(card(
    question="Un desarrollador de GenAI construye una aplicacion RAG con Amazon Bedrock Knowledge Bases para responder sobre documentos de la empresa. Los documentos son PDF con <b>graficos, tablas y texto</b> guardados en Amazon S3, y ademas hay <b>datos de negocio estructurados en bases relacionales</b>. La app debe manejar 50 consultas por minuto, dar atribucion de fuente y recuperar informacion de fuentes <b>estructuradas y no estructuradas</b>. &iquest;Que solucion cumple con el <b>MENOR esfuerzo operativo</b>?",
    options=[
        "Usar Amazon Bedrock Data Automation como parser para el procesamiento multimodal e implementar structured data retrieval para consultar las bases directamente",
        "Usar Anthropic Claude Sonnet como parser con chunking por defecto, consultas federadas entre fuentes de documentos y structured data retrieval para las bases",
        "Usar Amazon OpenSearch Service para hierarchical chunking y funciones AWS Lambda que generen consultas SQL personalizadas",
        "Usar Amazon Bedrock Knowledge Bases con GraphRAG y Amazon Neptune Analytics para modelar relaciones, con Lambda para semantic chunking y transformar los datos relacionales a formato grafo",
    ],
    correct=0,
    key="off1-q1",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock Data Automation (BDA) como parser + structured data retrieval.</div>'
        '<p><b>El problema:</b> RAG que debe leer PDF <b>multimodales</b> (graficos, tablas, texto) y a la vez consultar datos <b>estructurados</b> en bases relacionales, con atribucion de fuente y el minimo esfuerzo operativo. RAG = retrieval augmented generation (recuperar contexto y luego generar la respuesta).</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Data Automation</b> hace parsing multimodal gestionado, extrayendo informacion de graficos, tablas y texto de los PDF sin codigo propio. El <b>structured data retrieval</b> deja consultar las bases relacionales en lenguaje natural. Cubre ambas fuentes con servicios gestionados, sin Lambdas ni integraciones a medida, asi que es el de menor esfuerzo operativo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Claude Sonnet como parser:</b> no ofrece el mismo parsing multimodal que BDA para extraer graficos y tablas incrustados en PDF; aunque el resto (federated + structured retrieval) toque ambas fuentes, falla el requisito de documentos con graficos y tablas.</li>'
        '<li><b>OpenSearch + Lambda con SQL a medida:</b> el hierarchical chunking no procesa contenido multimodal (graficos, tablas), y generar SQL con Lambda a mano agrega mas esfuerzo operativo que el structured data retrieval gestionado.</li>'
        '<li><b>GraphRAG + Neptune Analytics:</b> modela relaciones en contenido no estructurado pero no consulta de forma nativa datos estructurados en bases relacionales; requiere Lambdas para semantic chunking y para pasar lo relacional a grafo, lo que suma mucho overhead.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>PDF con graficos y tablas + necesidad de menor esfuerzo operativo: piensa en un parser multimodal gestionado. Combinar fuentes estructuradas y no estructuradas sin codigo propio apunta a las capacidades gestionadas de Knowledge Bases, no a Lambdas que arman SQL o convierten a grafo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q2 - OpenSearch hybrid search + Bedrock reranker
# ============================================================
cards.append(card(
    question="Se construye un asistente de investigacion legal con Amazon Bedrock y un modelo Anthropic Claude. Debe recuperar documentos de jurisprudencia muy relevantes para aumentar las respuestas del modelo, <b>identificar relaciones semanticas entre conceptos legales</b>, respetar <b>terminologia y citas legales especificas</b>, y responder <b>rapido y con resultados precisos</b>. &iquest;Que solucion cumple?",
    options=[
        "Habilitar Amazon Bedrock Knowledge Bases con configuracion de retrieval por defecto y usar Bedrock para post-procesar los resultados buscando similitud semantica",
        "Desplegar en Amazon OpenSearch Service una arquitectura de busqueda hibrida (vectorial + por palabra clave) y aplicar un modelo reranker de Amazon Bedrock para optimizar la relevancia",
        "Configurar un knowledge base de Bedrock con busqueda vectorial por defecto y usar Bedrock para expandir las consultas segun la terminologia y las citas",
        "Usar OpenSearch Service con busqueda vectorial y embeddings Titan, mas funciones Lambda que mezclen los resultados con filtros por palabra clave guardados en una base Amazon RDS",
    ],
    correct=1,
    key="off1-q2",
    answer=(
        '<div class="verdict">Correcta: {{L}} - OpenSearch busqueda hibrida + reranker de Bedrock.</div>'
        '<p><b>El problema:</b> hay que capturar a la vez <b>relaciones semanticas</b> entre conceptos legales (afinidad de significado) y <b>coincidencias exactas</b> de terminologia y citas, con baja latencia y alta precision.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>busqueda hibrida</b> de OpenSearch combina busqueda <b>vectorial</b> (relaciones semanticas entre conceptos) con busqueda por <b>palabra clave</b> (terminologia y citas exactas). El <b>reranker</b> de Bedrock re-puntua los resultados combinados para dejar arriba lo mas pertinente, asegurando precision y rapidez. Cubre semantica, precision y desempe&ntilde;o.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Knowledge Bases por defecto + post-procesar con Bedrock:</b> el paso de post-procesamiento agrega latencia (incumple el "responder rapido") y no integra igual el entendimiento semantico con la coincidencia exacta de terminologia que el hibrido con reranker.</li>'
        '<li><b>Knowledge base solo con vectorial + expansion de consultas:</b> depender solo de busqueda vectorial por defecto sin reranker no optimiza la relevancia ni garantiza traer rapido los documentos mas pertinentes.</li>'
        '<li><b>OpenSearch vectorial + Lambda que mezcla con RDS:</b> unir sistemas separados con Lambdas para fusionar resultados agrega complejidad y latencia frente al hibrido nativo de OpenSearch; incumple el "rapido" y es menos eficiente que un reranker dedicado.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cuando piden a la vez significado (semantica) y coincidencia exacta de terminos o citas, con rapidez, la respuesta es busqueda hibrida (vectorial + keyword) y un reranker gestionado, no post-procesar ni fusionar a mano con Lambda.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vector-search.html">docs.aws OpenSearch vector search</a></div>'
    ),
))

# ============================================================
# Q3 - Dynamic chunking para transcripts largos truncados
# ============================================================
cards.append(card(
    question="Una plataforma de analitica de soporte en Amazon Bedrock ingiere <b>transcripciones de varias horas</b> de llamadas y usa un modelo para resumir, detectar sentimiento y recomendar pasos. En pruebas, las transcripciones largas se <b>truncan</b>, con respuestas incompletas. Se necesita procesarlas <b>completas de principio a fin</b>, minimizar errores por truncado y mantener <b>alta fiabilidad de integracion</b> entre multiples llamadas al modelo. &iquest;Que solucion cumple?",
    options=[
        "Rearquitecturar hacia una variante de FM mas grande con ventana de contexto extendida y configurar diagnosticos de truncado y monitoreo adaptativo",
        "Aplicar chunking dinamico en segmentos coherentes con prompts que mantengan continuidad, priorizando baja latencia limitando el solape y con deteccion de overflow simplificada",
        "Aplicar chunking dinamico que divida la transcripcion en segmentos coherentes, con prompts que mantengan continuidad entre segmentos y diagnosticos que detecten overflow por truncado",
        "Montar capas de resumen semantico y reduccion de tokens antes de enviar al FM, con flujos de validacion que aseguren la fidelidad de las transcripciones comprimidas",
    ],
    correct=2,
    key="off1-q3",
    answer=(
        '<div class="verdict">Correcta: {{L}} - chunking dinamico con continuidad y deteccion de overflow.</div>'
        '<p><b>El problema:</b> las transcripciones de horas exceden la ventana de contexto del modelo (context window = cuanto texto cabe en una llamada) y se truncan. Hay que procesarlas enteras, sin perder informacion, y encadenar bien varias llamadas al FM.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>chunking dinamico</b> parte la transcripcion en segmentos que caben en la ventana, atacando el truncado de raiz. Dise&ntilde;ar prompts que <b>mantienen la continuidad entre segmentos</b> evita huecos de contexto en los bordes, y los <b>diagnosticos de overflow</b> detectan si algo se corta. Asi se procesa de principio a fin con alta fiabilidad entre llamadas.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>FM mas grande con contexto extendido:</b> incluso la ventana mas grande se queda corta ante transcripciones de varias horas, asi que el truncado puede persistir; ademas sube costo y latencia.</li>'
        '<li><b>Chunking dinamico pero limitando el solape por latencia:</b> reducir el solape crea huecos de contexto en los limites de segmento, no garantiza procesar de principio a fin y compromete la fiabilidad entre llamadas.</li>'
        '<li><b>Resumen semantico + reduccion de tokens antes del FM:</b> comprimir elimina detalle por definicion, con riesgo de perder insights; no cumple el requisito de procesamiento completo sin perdida.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Entrada mas larga que la ventana de contexto: divide en trozos coherentes manteniendo continuidad, no confies en un modelo mas grande ni en comprimir (comprimir pierde detalle). Cuidado con recortar el solape solo por latencia: crea huecos.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws estrategias de chunking</a></div>'
    ),
))

# ============================================================
# Q4 - Lineage + PII + audit compliance stack completo
# ============================================================
cards.append(card(
    question="Una empresa medica crea un sistema de GenAI con Amazon Bedrock. Debe mantener <b>linaje de datos de extremo a extremo</b>, aplicar <b>filtrado de PII en tiempo real</b> y llevar <b>audit trails</b> que reporten cumplimiento de forma automatica. &iquest;Que solucion cumple? (PII = informacion personal identificable).",
    options=[
        "AWS Glue Data Catalog para registrar fuentes y linaje, Bedrock Guardrails con filtros PII, CloudTrail para todas las llamadas de Bedrock hacia S3, Amazon Macie para escanear datos sensibles hacia CloudWatch Logs y dashboards de CloudWatch para reportes de cumplimiento",
        "Amazon Athena para consultar y reportar linaje, metricas custom de CloudWatch para monitorear exposicion de PII, trazas basadas en OpenTelemetry como audit trail y un modelo de Rekognition Custom Labels para detectar datos sensibles",
        "AWS DataSync para replicar fuentes y rastrear linaje, Macie para escanear las salidas de Bedrock, Systems Manager Session Manager para registrar interacciones y Amazon Textract con Step Functions para redactar PII de los reportes generados",
        "AWS Config para rastrear configuraciones y cambios de las fuentes, AWS WAF con reglas custom para filtrar PII en la capa de aplicacion, EventBridge para enrutar eventos de auditoria a S3 y Comprehend Medical con Lambda programado para analizar salidas almacenadas",
    ],
    correct=0,
    key="off1-q4",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Glue Data Catalog + Guardrails PII + CloudTrail + Macie + dashboards CloudWatch.</div>'
        '<p><b>El problema:</b> tres requisitos a la vez: linaje de datos de extremo a extremo (de donde vino cada dato), filtrado de PII <b>en tiempo real</b> durante la generacion, y audit trails con reporte automatico de cumplimiento.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Glue Data Catalog</b> registra y rastrea metadatos de todas las fuentes (linaje). <b>Bedrock Guardrails</b> filtra PII en tiempo real durante la generacion. <b>CloudTrail</b> captura el audit trail completo de las llamadas a Bedrock. <b>Macie</b> automatiza el escaneo de datos sensibles almacenados y los <b>dashboards de CloudWatch</b> visualizan y generan los reportes de cumplimiento. Cada pieza cubre un requisito.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Athena + OpenTelemetry + Rekognition Custom Labels:</b> Athena consulta datos pero no mantiene las relaciones de linaje entre fuentes; OpenTelemetry traza rendimiento, no un audit trail completo con reporte automatico; y Rekognition analiza imagenes, no filtra PII de texto en tiempo real.</li>'
        '<li><b>DataSync + Session Manager + Textract/Step Functions:</b> DataSync solo replica datos (no rastrea linaje); Session Manager registra sesiones de shell, no llamadas de API; y redactar con Textract despues de generar no es filtrado de PII en tiempo real.</li>'
        '<li><b>AWS Config + WAF + Comprehend Medical programado:</b> Config rastrea cambios de configuracion, no linaje entre fuentes; WAF filtra peticiones web, no contenido generado por IA; y Comprehend Medical con Lambda programado es procesamiento por lotes, no filtrado en tiempo real.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"PII en tiempo real durante la generacion" apunta a barandas de contenido en la inferencia (no a redactar despues ni por lotes). Linaje entre fuentes = catalogo de datos gestionado, no replicar ni solo consultar. Audit trail de llamadas de API = servicio de registro de actividad de API.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
    ),
))

# ============================================================
# Q5 - Provisioned throughput + geographic inference profile EU
# ============================================================
cards.append(card(
    question="Una empresa financiera construye deteccion de fraude con Amazon Bedrock para apps de trading en EE.UU. y Europa. Debe procesar 1000 transacciones por segundo con respuestas sub-500 ms, mantener <b>alta disponibilidad</b> ante cortes de conectividad y garantizar que los datos de clientes europeos se procesen <b>solo en Regiones de Europa</b>. &iquest;Que solucion cumple?",
    options=[
        "Usar InvokeModel con provisioned throughput para un modelo Claude por Region, un Application Load Balancer custom que reparta por capacidad regional y failover regional con reglas de EventBridge",
        "Provisioned throughput con InvokeModel para EE.UU., un geographic inference profile especifico de Europa para las apps europeas, auto scaling de la capacidad por utilizacion y failover cross-Region con EventBridge y Lambda",
        "InvokeModelWithResponseStream con throughput on-demand, un API Gateway REST con endpoints regionales para enrutar al endpoint de Bedrock mas cercano y roles IAM separados por Region",
        "InvokeModel con un global inference profile en Lambda y EKS, failover con health checks de Route 53, un inference profile europeo dedicado con cross-Region inference geografica y alarmas de CloudWatch",
    ],
    correct=1,
    key="off1-q5",
    answer=(
        '<div class="verdict">Correcta: {{L}} - provisioned throughput (EE.UU.) + geographic inference profile de Europa + failover con EventBridge/Lambda.</div>'
        '<p><b>El problema:</b> rendimiento garantizado (1000 tps, sub-500 ms), alta disponibilidad ante cortes y <b>soberania de datos</b>: lo europeo solo en Regiones europeas. Un inference profile define en que Regiones se ejecuta el modelo.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>provisioned throughput</b> da capacidad dedicada para el rendimiento consistente que exigen los sub-500 ms a 1000 tps. Un <b>geographic inference profile de Europa</b> asegura que los datos europeos se procesen solo en Regiones de Europa (soberania). El auto scaling por utilizacion mas el failover cross-Region con <b>EventBridge y Lambda</b> cubren la alta disponibilidad ante cortes.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Provisioned por Region + ALB + EventBridge:</b> el failover con solo EventBridge enruta dentro de la misma Region, sin cross-Region inference profiles, asi que no reencamina dinamicamente el trafico durante un corte; falla la alta disponibilidad.</li>'
        '<li><b>On-demand + API Gateway + roles IAM por Region:</b> el throughput on-demand sufre variabilidad y throttling en picos, dificil de garantizar sub-500 ms a 1000 tps; y los permisos IAM por Region no imponen la soberania de datos como un geographic inference profile.</li>'
        '<li><b>Global inference profile + Route 53:</b> un perfil global enruta a cualquier Region del mundo por disponibilidad, lo que viola el requisito de procesar datos europeos solo en Europa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Soberania de datos por region = geographic inference profile (no global, que enruta a cualquier lado). Rendimiento garantizado y estable = provisioned throughput (on-demand es variable). Failover real ante cortes = cross-Region, no solo dentro de la misma Region.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">docs.aws cross-Region inference profiles</a></div>'
    ),
))

# ============================================================
# Q6 - KB RetrieveAndGenerate citations + session IDs
# ============================================================
cards.append(card(
    question="Una app de servicio al cliente con Amazon Bedrock responde preguntas de cumplimiento regulatorio usando varias fuentes (documentos regulatorios en S3, historiales de interaccion, documentacion de producto). Los auditores deben poder <b>verificar que fuentes contribuyeron a cada respuesta</b> (trazabilidad), sin afectar el rendimiento a escala, con <b>citas en tiempo real</b> y logs de citas, manejando <b>actualizaciones de documentos sin redeploy</b> y manteniendo la exactitud de las citas aunque las fuentes cambien. &iquest;Que solucion cumple con el <b>MENOR esfuerzo operativo</b>?",
    options=[
        "Amazon Bedrock Knowledge Bases con la API RetrieveAndGenerate para citas en las respuestas, incluyendo fuente y metadatos, y session tracking con session IDs para mantener el contexto",
        "Funciones AWS Lambda que intercepten cada peticion y rastreen manualmente las fuentes, guardando el tracking en DynamoDB y actualizando registros con cada respuesta",
        "Un sistema de tracking custom en Amazon RDS para relacionar entradas y salidas, middleware que registre los accesos a datos y un modelo de SageMaker AI que prediga que dato influyo en cada respuesta",
        "Bedrock Guardrails con filtrado de entrada/salida, logging detallado a CloudWatch Logs y scripts de parsing custom que extraigan la atribucion de fuente y la guarden en S3",
    ],
    correct=0,
    key="off1-q6",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Knowledge Bases con RetrieveAndGenerate (citas nativas) + session IDs.</div>'
        '<p><b>El problema:</b> trazabilidad auditable con citas <b>en tiempo real</b>, logs de citas, tolerancia a cambios de documentos sin redeploy y exactitud de citas aunque las fuentes se modifiquen o archiven, todo con el minimo esfuerzo operativo.</p>'
        '<p><b>Por que la respuesta sirve:</b> la API <b>RetrieveAndGenerate</b> de Knowledge Bases genera citas nativas con la fuente y metadatos en cada respuesta (trazabilidad en tiempo real). Al ser gestionada, el indexado maneja las actualizaciones de documentos de forma automatica, manteniendo la exactitud de las citas cuando el documento cambia o se archiva, sin redeploy. Los session IDs mantienen el contexto de conversacion. Es la opcion de menor overhead porque no requiere desarrollo a medida.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Lambda que intercepta + DynamoDB:</b> el middleware para rastrear fuentes a mano exige mucho desarrollo, agrega latencia por peticion y no genera citas ni metadatos en tiempo real ni maneja solo los cambios de documentos.</li>'
        '<li><b>Tracking custom en RDS + modelo SageMaker que predice influencia:</b> mucho overhead operativo, y predecir con un modelo que dato influyo es inferencia, no trazado real de la fuente; no da la trazabilidad verificable pedida.</li>'
        '<li><b>Guardrails + parsing custom:</b> Guardrails filtra contenido y seguridad, no rastrea atribucion de fuente; los scripts de parsing suman overhead y no dan citas en tiempo real ni manejo automatico de cambios de documentos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Citas verificables en tiempo real con el menor esfuerzo: usa la capacidad nativa de la base de conocimiento gestionada, no middleware que rastree fuentes a mano ni modelos que "predicen" que dato influyo (eso es inferencia, no trazado).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html">docs.aws RetrieveAndGenerate y citas</a></div>'
    ),
))



# ============================================================
# Q7 - Model distillation Nova Pro a Nova Lite
# ============================================================
cards.append(card(
    question="Un hospital genera reportes medicos con un modelo Amazon Nova Pro en Amazon Bedrock. Las peticiones tienen <b>picos en horario laboral</b>. Hay que <b>optimizar costos</b>, <b>escalar</b> para varios departamentos y <b>mantener la misma calidad</b> de reporte. &iquest;Que solucion cumple?",
    options=[
        "Registrar invocaciones en CloudWatch, guardar respuestas de Nova Pro en S3 y usarlas para un distillation job de un modelo Llama 70B en Bedrock, desplegando el modelo en SageMaker JumpStart",
        "Crear un dataset JSONL con datos medicos y reportes del personal, subirlo a S3 e incluir varios ejemplos del dataset en cada prompt al invocar Nova Pro",
        "Registrar invocaciones en CloudWatch, guardar respuestas de Nova Pro en S3 y usarlas para un distillation job de Nova Lite en Bedrock, desplegando Nova Lite con inferencia on-demand",
        "Crear un dataset JSONL con datos medicos y reportes del personal, subirlo a S3, hacer fine-tuning de Nova Pro con el dataset y desplegar el modelo ajustado con provisioned throughput",
    ],
    correct=2,
    key="off1-q7",
    answer=(
        '<div class="verdict">Correcta: {{L}} - distillation de Nova Pro a Nova Lite + inferencia on-demand.</div>'
        '<p><b>El problema:</b> demanda variable (picos en horario laboral); hay que abaratar, escalar por departamentos y no perder calidad. La destilacion (distillation) transfiere el conocimiento de un modelo grande "profesor" a uno mas peque&ntilde;o y barato "alumno" de la misma familia.</p>'
        '<p><b>Por que la respuesta sirve:</b> se registran las salidas de <b>Nova Pro</b> (profesor) y se destilan a <b>Nova Lite</b> (alumno mas peque&ntilde;o y barato de la misma familia), que hereda la calidad. Desplegar Nova Lite con <b>inferencia on-demand</b> se ajusta a la demanda variable y solo paga por uso, cubriendo costo, escala y calidad.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Destilar a Llama 70B en SageMaker JumpStart:</b> desplegar en JumpStart exige gestionar infraestructura y no optimiza costo para una demanda que fluctua; on-demand seria mejor para ese patron.</li>'
        '<li><b>Few-shot con ejemplos en cada prompt:</b> mejora calidad pero no reduce costo; usa el mismo Nova Pro y suma tokens por prompt, encareciendo la inferencia.</li>'
        '<li><b>Fine-tuning de Nova Pro + provisioned throughput:</b> el fine-tuning mejora tareas especificas pero no abarata; sigue en Nova Pro y con provisioned throughput compra capacidad fija, sin reducir costo ante demanda variable.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Abaratar manteniendo calidad = destilar a un modelo mas peque&ntilde;o de la misma familia. Demanda variable con picos = inferencia on-demand (paga por uso), no provisioned throughput (capacidad fija). Few-shot y fine-tuning no reducen costo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-distillation.html">docs.aws model distillation</a></div>'
    ),
))

# ============================================================
# Q8 - Guardrails PII mask + Bedrock Evaluations comparar FMs
# ============================================================
cards.append(card(
    question="Una empresa de salud resume historias clinicas con Amazon Bedrock. La solucion debe <b>detectar y remover PHI</b> pero usar y resumir con precision la <b>terminologia medica</b>. Quiere <b>comparar varios FM</b> para hallar el mas consistente y terminar el build en <b>3 semanas</b>. &iquest;Que solucion cumple? (PHI = informacion de salud protegida).",
    options=[
        "Un pipeline con Amazon Comprehend Medical para identificar PHI, un modelo de resumen custom en SageMaker AI y muestreo manual para evaluar la calidad de salida",
        "Configurar Bedrock para probar varios FM contra registros de muestra, Comprehend Medical para detectar PHI en los resumenes generados, resultados en DynamoDB y scoring custom en Lambda para comparar la precision terminologica",
        "Probar prompts contra varios FM en el playground de la consola de Bedrock y revisar manualmente el manejo de PHI y la precision de terminologia en las salidas de muestra",
        "Usar Amazon Bedrock Guardrails con filtros de informacion sensible para detectar y enmascarar PHI, y Amazon Bedrock Evaluations para puntuar automaticamente las salidas contra un dataset de terminologia medica y comparar varios FM",
    ],
    correct=3,
    key="off1-q8",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails (mascara de PHI) + Bedrock Evaluations (comparar FMs).</div>'
        '<p><b>El problema:</b> dos cosas: quitar PHI de forma efectiva y comparar varios FM de manera sistematica para elegir el mas consistente, todo en un plazo corto (3 semanas).</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> con filtros de informacion sensible bloquea o enmascara PHI <b>durante la generacion</b>, cumpliendo el remover PHI. <b>Bedrock Evaluations</b> compara FMs automaticamente puntuando sus salidas contra un dataset de terminologia medica, permitiendo elegir el modelo mas consistente dentro de las 3 semanas.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Comprehend Medical + resumen custom en SageMaker + muestreo manual:</b> construir un modelo de resumen a medida excede el plazo de 3 semanas y no ofrece comparacion automatizada entre varios FM.</li>'
        '<li><b>Probar FMs + Comprehend Medical + scoring en Lambda + DynamoDB:</b> detecta PHI de forma reactiva despues de generar (no la remueve durante la generacion) y exige mucho desarrollo (Lambda de scoring, DynamoDB) frente a Evaluations.</li>'
        '<li><b>Playground de la consola + revision manual:</b> las revisiones manuales no dan la comparacion automatizada necesaria para evaluar sistematicamente varios FM en 3 semanas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Remover PHI/PII "durante la generacion" = barandas con filtros de informacion sensible (no detectar despues). Comparar varios FM de forma sistematica y con plazo corto = la evaluacion automatizada gestionada, no scoring a mano ni playground manual.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock model evaluation</a></div>'
    ),
))

# ============================================================
# Q9 - Guardrails sensitive info filter en OUTPUTS
# ============================================================
cards.append(card(
    question="Una app clinica con Amazon Bedrock sugiere diagnosticos y ya enmascara PII de las <b>entradas</b> con Comprehend Medical (95% de exactitud) reemplazando entidades por tokens antes de llamar al modelo. Aun asi, entre <b>3-5% de las salidas incluyen nombres y numeros de historia clinica que NO estaban en la entrada</b>. Hay que evitar que la app muestre PII en las salidas, con sub-500 ms y logging de auditoria. &iquest;Que solucion cumple?",
    options=[
        "Quitar el contexto medico detallado de las historias en el preprocesamiento para que el modelo no genere informacion especifica del paciente por asociacion de patrones clinicos",
        "Habilitar aislamiento de sesion en las llamadas a Bedrock y limpiar el historial entre peticiones para que la informacion del paciente no persista entre analisis",
        "Implementar una segunda capa de deteccion de PII con expresiones regulares y reconocimiento de entidades custom para detectar, antes de enviar a Bedrock, identificadores que Comprehend Medical pierde",
        "Configurar Amazon Bedrock Guardrails con filtros de informacion sensible que detecten y bloqueen los identificadores de PII en las salidas del modelo antes de que la respuesta llegue a la aplicacion clinica",
    ],
    correct=3,
    key="off1-q9",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails con filtro de informacion sensible sobre las SALIDAS.</div>'
        '<p><b>El problema clave:</b> los identificadores aparecen en la salida <b>sin estar en la entrada</b>: el modelo los <b>alucina</b> (inventa datos con forma realista a partir de patrones aprendidos). Por eso limpiar la entrada no basta; hay que filtrar la salida.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> con filtros de informacion sensible detecta y bloquea o enmascara PII <b>en la salida del modelo</b> antes de que llegue a la aplicacion. Ataca justo la PII alucinada que no venia de la entrada, y lo hace manteniendo sub-500 ms y con el logging de auditoria requerido.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Quitar contexto medico en preproceso:</b> destruye el proposito de la app (analizar historias) y no evita las alucinaciones; el modelo puede inventar identificadores aun con poco contexto.</li>'
        '<li><b>Aislamiento de sesion / limpiar historial:</b> resuelve fuga entre sesiones, pero la PII surge dentro de una sola respuesta por patrones de entrenamiento, no por arrastre de estado; no aplica.</li>'
        '<li><b>Segunda capa de deteccion en la ENTRADA:</b> mejora la entrada, pero el problema son identificadores alucinados en la salida que nunca estuvieron en la entrada; filtrar mas la entrada no los elimina.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Si aparecen datos que no estaban en la entrada, el modelo los alucina: filtra la SALIDA con barandas de contenido sobre los outputs. Reforzar el filtrado de entrada no ataca alucinaciones.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html">docs.aws Guardrails filtros de informacion sensible</a></div>'
    ),
))

# ============================================================
# Q10 - Textract + Comprehend + structured metadata prompting
# ============================================================
cards.append(card(
    question="Una empresa financiera genera recomendaciones de inversion con FMs de Amazon Bedrock a partir de documentos de clientes. El rendimiento es <b>inconsistente por mala calidad de datos</b>: algunos documentos tienen PII que hay que redactar y otros tienen <b>inconsistencias de formato</b> que confunden al FM. Hay que asegurar entradas consistentes y de alta calidad cumpliendo regulaciones y politicas de PII, con el <b>MENOR esfuerzo operativo</b>. &iquest;Que solucion cumple?",
    options=[
        "Amazon Macie para detectar y redactar PII automaticamente, funciones Lambda con Amazon Textract para imponer formato estandar y prompts dinamicos que se adapten al esquema de cada documento",
        "Amazon Textract para analizar la estructura y extraer texto, Amazon Comprehend para detectar PII y analizar sentimiento, y prompting que use metadatos estructurados para mejorar el razonamiento del FM y reducir alucinaciones",
        "Amazon Bedrock Guardrails para filtrar PII durante la inferencia, Lambda de preprocesamiento para estandarizar el formato y few-shot con ejemplos estandarizados para mejorar el desempe&ntilde;o",
        "Amazon Comprehend con custom entity recognition para detectar PII, AWS Step Functions para orquestar el preprocesamiento y plantillas de prompt con logica condicional para manejar variaciones de esquema",
    ],
    correct=1,
    key="off1-q10",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Textract (estructura) + Comprehend (PII) + prompting con metadatos estructurados.</div>'
        '<p><b>El problema:</b> la causa raiz de la inconsistencia son datos de entrada mal formados y con PII. Hay que estructurar los documentos y redactar PII con servicios gestionados (minimo overhead).</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Textract</b> analiza la estructura del documento y lo convierte en texto y metadatos legibles (tablas, formularios, pares clave-valor), atacando directamente las inconsistencias de formato. <b>Comprehend</b> da deteccion y redaccion de PII gestionada. Usar esos metadatos estructurados en el prompting mejora el razonamiento del FM y reduce alucinaciones, con el menor esfuerzo operativo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Macie + Lambda/Textract + prompts dinamicos:</b> Macie descubre y clasifica datos sensibles en S3, pero no preprocesa documentos para FMs; hace falta Lambda a medida para el formato, mas overhead que servicios gestionados de analisis de documentos.</li>'
        '<li><b>Guardrails + Lambda + few-shot:</b> Guardrails filtra contenido en la inferencia, pero no arregla la mala calidad ni las inconsistencias de formato de la entrada, que es la causa raiz.</li>'
        '<li><b>Comprehend custom entity + Step Functions + logica condicional:</b> el custom entity recognition exige entrenar y gestionar modelos propios (mas overhead que la deteccion estandar de PII), y la orquestacion con Step Functions es mas compleja que usar servicios gestionados.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Si la causa raiz es formato inconsistente de documentos, arregla la ENTRADA con analisis de documentos gestionado (Textract) + PII gestionada (Comprehend). Guardrails filtra salida, no arregla datos de entrada; custom entity de Comprehend suma overhead innecesario.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/textract/latest/dg/what-is.html">docs.aws Amazon Textract</a></div>'
    ),
))

# ============================================================
# Q11 - CDK construct library reutilizable compartida
# ============================================================
cards.append(card(
    question="Una empresa financiera desarrolla una app de procesamiento de documentos con GenAI para varias unidades de negocio. Debe soportar FMs de Amazon Bedrock y modelos en Amazon SageMaker AI, tener <b>controles de seguridad consistentes</b> entre desarrollo y produccion, monitoreo/observabilidad completos y <b>componentes tecnicos aprobados y reutilizables</b> compartidos entre unidades. &iquest;Que solucion cumple?",
    options=[
        "Desarrollar una libreria estandarizada de constructs de AWS CDK con gestion de prompts, controles de seguridad y observabilidad consistentes, empaquetada como libreria compartida para todas las unidades",
        "Crear una plantilla de AWS CloudFormation separada por cada unidad de negocio y personalizar los despliegues con parametros por entorno",
        "Desplegar todas las cargas de GenAI en una unica cuenta de AWS con arquitectura multi-tenant y politicas IAM y permisos basados en recursos separados por unidad",
        "Construir un pipeline de SageMaker AI por unidad con un endpoint de inferencia propio, Step Functions para coordinar las peticiones y monitoreo custom por despliegue",
    ],
    correct=0,
    key="off1-q11",
    answer=(
        '<div class="verdict">Correcta: {{L}} - libreria compartida de constructs de AWS CDK.</div>'
        '<p><b>El problema:</b> componentes aprobados y <b>reutilizables</b> compartidos entre unidades, con seguridad consistente entre entornos y observabilidad unificada, soportando Bedrock y SageMaker. Los constructs de CDK son bloques reutilizables que empaquetan infraestructura, configuracion y logica.</p>'
        '<p><b>Por que la respuesta sirve:</b> una <b>libreria de constructs de CDK</b> consolida gestion de prompts, controles de seguridad y observabilidad en componentes estandarizados y reutilizables. Compartida entre unidades, impone consistencia en todos los entornos y soporta tanto Bedrock como SageMaker, cumpliendo el requisito de componentes aprobados reutilizables y gobierno consistente.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CloudFormation separado por unidad:</b> plantillas independientes no garantizan componentes reutilizables ni seguridad consistente; llevan a drift de plantillas, esfuerzo duplicado e implementaciones dispares.</li>'
        '<li><b>Cuenta unica multi-tenant con IAM por unidad:</b> concentrar todo en una cuenta aumenta el radio de impacto (blast radius) y no entrega componentes compartidos ni seguridad consistente entre desarrollo y produccion.</li>'
        '<li><b>Pipeline de SageMaker por unidad con monitoreo custom:</b> genera fragmentacion, controles de seguridad inconsistentes y monitoreo duplicado; no da componentes reutilizables ni observabilidad unificada.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Componentes aprobados reutilizables y consistentes entre unidades" apunta a una libreria de constructs de infraestructura como codigo compartida, no a plantillas o pipelines separados por equipo (que causan drift y duplicacion).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/cdk/v2/guide/constructs.html">docs.aws AWS CDK constructs</a></div>'
    ),
))



# ============================================================
# Q12 - Lake Formation cross-account tag-based column access
# ============================================================
cards.append(card(
    question="Una app de GenAI debe analizar datos en <b>varias cuentas de AWS</b> con un FM. La cuenta A tiene transacciones, la B perfiles de clientes con PII y la C aloja la app; se sumaran 7 unidades mas pronto. Se exige <b>control estricto de PII</b> y que el FM acceda <b>solo a los campos (columnas) necesarios</b>, con acceso cross-account seguro. &iquest;Que solucion cumple?",
    options=[
        "Usar IAM Identity Center para un permission set de la cuenta de servicio del FM, politicas basadas en recursos por bucket que permitan acceso a la cuenta C y un Lambda authorizer custom que filtre PII antes de pasarla al FM",
        "Politicas basadas en recursos en cada bucket para permitir a la app de la cuenta C, politicas basadas en identidad para el rol del FM que permitan solo ciertas columnas via Lake Formation tag-based access, y un VPC endpoint por cuenta",
        "Configurar AWS Lake Formation en cada cuenta origen con los buckets registrados y permisos por columnas con tag-based access, y desplegar el FM en SageMaker AI con un rol en la cuenta C que asuma los roles cross-account para acceder via Lake Formation",
        "Configurar roles IAM cross-account de Amazon Bedrock, con politicas por ruta de bucket en cada cuenta origen y tag-based access sobre los objetos de S3 para clasificar y controlar el acceso a los datos de PII de los clientes",
    ],
    correct=2,
    key="off1-q12",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Lake Formation en cada cuenta con tag-based access a nivel de columna + roles cross-account.</div>'
        '<p><b>El problema:</b> control a nivel de <b>columna</b> (que el FM solo lea los campos necesarios) sobre datos con PII repartidos en varias cuentas, con acceso cross-account seguro y que escale a 10 cuentas.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Lake Formation</b> da control de acceso a nivel de <b>columna</b> mediante tag-based access, garantizando que el FM lea solo los campos necesarios. Registra los buckets en cada cuenta origen y habilita el compartir datos cross-account seguro con roles IAM. El FM en SageMaker AI usa un rol en la cuenta C que <b>asume</b> los roles cross-account para leer via Lake Formation. Cumple PII estricto y escala.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>IAM Identity Center + Lambda authorizer:</b> Identity Center gestiona SSO y acceso, no control por columna; y un Lambda authorizer autoriza peticiones de API, no da control granular por campo sobre datos en S3 en varias cuentas.</li>'
        '<li><b>Politicas de recurso en S3 + Lake Formation tags + VPC endpoint:</b> no puedes aplicar tag-based access de Lake Formation solo con politicas de bucket (hay que registrar los buckets y otorgar por las APIs de Lake Formation); y un VPC endpoint aisla la red pero no da acceso cross-account ni filtrado por columna.</li>'
        '<li><b>Roles cross-account de Bedrock + tags en objetos S3:</b> los tag-based controls de S3 operan a nivel de objeto, no pueden restringir a columnas o campos dentro del dato; no cumplen "solo los campos necesarios".</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Control a nivel de COLUMNA sobre datos en el lago = Lake Formation (tag-based access), no politicas o tags de S3 (operan a nivel de objeto) ni Identity Center. Cross-account seguro = roles que se asumen entre cuentas.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html">docs.aws Lake Formation tag-based access</a></div>'
    ),
))

# ============================================================
# Q13 - Video metadata sincronizada (frames + Transcribe + Claude)
# ============================================================
cards.append(card(
    question="Una empresa de medios debe generar metadatos <b>buscables</b> para 10.000 horas de video (escenas visuales, dialogo, musica de fondo y texto en pantalla). Necesita extraer descripciones de escena, transcripciones con <b>timestamps</b>, texto en pantalla y contexto emocional, <b>sincronizando todos los metadatos entre si</b> en un indice buscable donde el usuario salte a un momento exacto del video. &iquest;Que solucion cumple?",
    options=[
        "Un processing job de SageMaker AI que extraiga frames a intervalos fijos con timestamps, Amazon Transcribe con marcas de tiempo para el audio, un modelo Claude en Bedrock para analizar pares frame-transcripcion y guardar todo en una estructura JSON unificada que preserve las relaciones temporales",
        "Un processing job de SageMaker AI que extraiga frames a intervalos regulares, Amazon Transcribe para speech-to-text, un modelo Claude en Bedrock que procese frames de forma individual y guardar las salidas en buckets S3 separados por tipo de contenido",
        "Un processing job de SageMaker AI que configure Claude Opus en Bedrock para un analisis multimodal completo por video con una unica peticion de inferencia e indexe los resultados en Amazon OpenSearch Service para busqueda temporal",
        "Un processing job paralelo de SageMaker AI orquestado por un pipeline, con pasos para extraer segmentos, Transcribe para audio, Rekognition para detectar texto en escenas, Comprehend para sentimiento y metadatos unificados en DynamoDB con particionado por tiempo",
    ],
    correct=0,
    key="off1-q13",
    answer=(
        '<div class="verdict">Correcta: {{L}} - frames con timestamps + Transcribe con marcas de tiempo + Claude por pares frame-transcripcion + JSON unificado.</div>'
        '<p><b>El problema:</b> extraer varios tipos de metadato y <b>sincronizarlos temporalmente</b> para poder buscar por cualquiera de ellos y saltar al momento exacto del video.</p>'
        '<p><b>Por que la respuesta sirve:</b> el processing job extrae <b>frames con timestamps</b>; <b>Transcribe con marcas de tiempo</b> alinea la transcripcion a la linea de tiempo; <b>Claude</b> analiza pares frame-transcripcion (analisis multimodal, incluido contexto emocional). Guardar todo en una <b>estructura JSON unificada</b> preserva las relaciones temporales, permitiendo buscar por cualquier metadato y saltar al instante exacto.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Salidas en buckets S3 separados por tipo:</b> guardar cada tipo por separado impide la sincronizacion entre metadatos exigida; el usuario no podria saltar al momento exacto.</li>'
        '<li><b>Claude Opus con una sola peticion por video:</b> Claude analiza texto e imagenes (frames), no archivos de video completos en una sola inferencia; excederia limites de payload y de tokens.</li>'
        '<li><b>Pipeline paralelo con Comprehend para sentimiento:</b> Comprehend es NLP solo de texto; no puede analizar el contexto emocional de escenas visuales, dialogo hablado o musica de fondo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Saltar a un momento exacto" exige metadatos SINCRONIZADOS en el tiempo (una estructura unificada), no buckets separados por tipo. Un modelo texto/imagen no procesa un video entero en una sola llamada; Comprehend no analiza emocion visual/audio.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/transcribe/latest/dg/how-it-works.html">docs.aws Amazon Transcribe</a></div>'
    ),
))

# ============================================================
# Q14 - Strands supervisor agent en AgentCore Runtime
# ============================================================
cards.append(card(
    question="Una empresa educativa crea un asesor estudiantil con Amazon Bedrock. Un agente principal responde dudas academicas generales y, ante temas de becas, pasantias o salud mental, debe <b>delegar en agentes especializados</b> manteniendo el <b>contexto de conversacion</b> entre todos y con <b>metricas de uso</b> por agente, con el <b>MENOR codigo custom y esfuerzo operativo</b>. &iquest;Que solucion cumple?",
    options=[
        "Un agente por tema en Strands Agents expuestos por API Gateway, una Lambda que enrute a cada agente, el contexto en DynamoDB y CloudWatch logs para las metricas de la Lambda",
        "Un agente por tema en Strands Agents desplegados por separado en Bedrock AgentCore Runtime, un cliente frontend que enrute por coincidencia de palabras clave, transcripciones en S3 y logs de AgentCore mas analitica de frontend para las metricas",
        "Un supervisor en Strands Agents, Lambdas que clasifiquen y enruten a los agentes por tema, Step Functions para orquestar la delegacion y CloudWatch para recolectar los logs de la Lambda",
        "Un supervisor en Strands Agents desplegado en Bedrock AgentCore Runtime, con los agentes especializados registrados para que el supervisor delegue, usando la orquestacion nativa de Strands y AgentCore Observability para las metricas",
    ],
    correct=3,
    key="off1-q14",
    answer=(
        '<div class="verdict">Correcta: {{L}} - supervisor de Strands en AgentCore Runtime + orquestacion nativa + AgentCore Observability.</div>'
        '<p><b>El problema:</b> delegacion dinamica y consciente del contexto entre un agente principal y varios especializados, con contexto compartido y metricas, minimizando codigo custom y operacion.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Strands Agents</b> trae patrones nativos de orquestacion multi-agente (agents-as-tools) para que el supervisor delegue en agentes especializados manteniendo el contexto con su memoria integrada. <b>AgentCore Runtime</b> da escalado serverless, aislamiento de sesion y observabilidad integrada (<b>AgentCore Observability</b>) para las metricas. Cumple el minimo de codigo y esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Agentes + API Gateway + Lambda + DynamoDB:</b> exige infraestructura custom (API Gateway, Lambda, DynamoDB) y mucho desarrollo y operacion; no es el minimo esfuerzo.</li>'
        '<li><b>Enrutar por palabras clave en el frontend:</b> el keyword matching en el cliente requiere desarrollo custom y carece de la delegacion dinamica y consciente del contexto del patron supervisor de Strands.</li>'
        '<li><b>Supervisor + Lambdas de clasificacion + Step Functions:</b> Strands ya orquesta la delegacion de forma nativa; agregar Lambdas de clasificacion y Step Functions es codigo custom innecesario.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Delegacion multi-agente con contexto compartido y minimo codigo = el patron supervisor nativo del framework de agentes (agents-as-tools) sobre el runtime gestionado con su observabilidad integrada, no Lambdas/Step Functions/keyword matching a mano.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html">docs.aws Bedrock AgentCore</a></div>'
    ),
))

# ============================================================
# Q16 - Lambda response streaming + S3 records 10 anos
# ============================================================
cards.append(card(
    question="Una app NLP usa una funcion AWS Lambda para procesar consultas de trading con FMs de Amazon Bedrock. La respuesta suele superar <b>4 MB</b> y tarda <b>15-20 s</b> en completarse. La app debe responder al cliente en <b>menos de 10 s</b> y, por regulacion, <b>retener registros 10 a&ntilde;os</b>. &iquest;Que solucion cumple?",
    options=[
        "Usar colas Amazon SQS para invocaciones asincronas, timeout de 30 s en la Lambda y CloudWatch para monitorear tiempos de respuesta",
        "Response streaming para mostrar respuestas parciales a medida que se generan, timeout de 15 s en la Lambda y CloudWatch Lambda Insights para monitorear rendimiento",
        "Response streaming para mostrar respuestas parciales a medida que se generan, timeout de 30 s en la Lambda y guardar los registros completos de respuesta en Amazon S3",
        "Usar Amazon API Gateway para hacer polling a la app, integrar ElastiCache para cachear respuestas, timeout de 30 s en la Lambda y logs detallados de CloudWatch",
    ],
    correct=2,
    key="off1-q16",
    answer=(
        '<div class="verdict">Correcta: {{L}} - response streaming + timeout de 30 s + registros completos en S3.</div>'
        '<p><b>El problema:</b> conciliar una respuesta inicial rapida (menos de 10 s) con un procesamiento que tarda 15-20 s, mas retencion de registros por 10 a&ntilde;os. El response streaming devuelve partes de la respuesta a medida que se generan.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>response streaming</b> entrega respuestas parciales de inmediato, cumpliendo los menos de 10 s de respuesta inicial. El <b>timeout de 30 s</b> deja margen para los 15-20 s de procesamiento completo. Guardar los registros completos en <b>Amazon S3</b> (almacenamiento durable) cubre la retencion de 10 a&ntilde;os.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SQS asincrono + timeout 30 s:</b> encola y retorna de inmediato sin esperar el resultado; el cliente tendria que hacer polling aparte, no responde en menos de 10 s con el analisis.</li>'
        '<li><b>Streaming + timeout de 15 s:</b> 15 s es insuficiente para un proceso de 15-20 s, la funcion se cortaria antes de terminar; ademas Lambda Insights no cubre la retencion de 10 a&ntilde;os.</li>'
        '<li><b>API Gateway con polling + ElastiCache:</b> sin streaming, API Gateway debe esperar los 15-20 s completos, incumpliendo los menos de 10 s; y el cache no resuelve la respuesta inicial ni el guardado de 10 a&ntilde;os.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Respuesta inicial rapida con proceso largo = response streaming (partes a medida que se generan) y un timeout que cubra el tiempo total. Retencion a largo plazo = S3 durable, no metricas de CloudWatch.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/lambda/latest/dg/configuration-response-streaming.html">docs.aws Lambda response streaming</a></div>'
    ),
))

# ============================================================
# Q17 - KB reranking cross-encoder top-10 de 50
# ============================================================
cards.append(card(
    question="Un asistente legal con Amazon Bedrock y un knowledge base de millones de documentos recupera 50 documentos por busqueda semantica, pero el FM solo procesa <b>10 documentos</b> por su ventana de contexto y debe responder en <b>3 s</b>. Los precedentes muy relevantes suelen caer en las posiciones <b>15-40</b>. Hay que mejorar la <b>relevancia</b> respetando latencia y ventana de contexto. &iquest;Que solucion cumple?",
    options=[
        "Un action group de post-procesamiento con Lambda que recupere 50 documentos y calcule similitud coseno entre el embedding de la consulta y cada documento con Titan Embeddings, ordene por score y devuelva el top 10",
        "Mantener los 50 documentos pero subir el parametro temperature del FM y aplicar prompt engineering para que el modelo identifique los mas relevantes del conjunto antes de responder",
        "Habilitar reranking en el knowledge base con un modelo reranker con configuracion por idioma, recuperar 50 documentos, usar su arquitectura cross-encoder para evaluar pares consulta-documento y devolver solo los 10 mejor puntuados",
        "Configurar tres knowledge bases con chunks de 500, 1000 y 2000 tokens, un action group de preprocesamiento con Lambda que recupere 50 de cada una, mezcle los 150 resultados y use TF-IDF para elegir el top 10",
    ],
    correct=2,
    key="off1-q17",
    answer=(
        '<div class="verdict">Correcta: {{L}} - reranking con reranker cross-encoder que reordena los 50 y devuelve el top 10.</div>'
        '<p><b>El problema:</b> los precedentes relevantes estan en las posiciones 15-40, fuera del top 10 que cabe en la ventana de contexto. Hay que <b>reordenar</b> con una se&ntilde;al de relevancia mejor que la busqueda inicial, sin pasarse de 3 s.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>reranker</b> con arquitectura <b>cross-encoder</b> evalua conjuntamente cada par consulta-documento y produce un score de relevancia mas preciso. Al reordenar los 50 resultados y devolver solo el top 10, sube los precedentes de las posiciones 15-40 a la ventana de contexto, cumpliendo los 3 s y el limite de 10 documentos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Lambda recalculando similitud coseno:</b> la busqueda semantica inicial ya usa similitud coseno de embeddings; recalcular la misma metrica da casi el mismo orden, no promueve los documentos 15-40 y solo agrega latencia.</li>'
        '<li><b>Subir temperature + prompt engineering:</b> temperature controla la aleatoriedad del texto generado, no el orden ni la seleccion de documentos recuperados; no eleva los relevantes al top 10.</li>'
        '<li><b>Tres KB con distintos chunks + TF-IDF:</b> agrega complejidad y latencia (dificil cumplir 3 s), y TF-IDF es coincidencia lexica sin significado semantico, mucho menos efectivo que un cross-encoder para hallar precedentes legales relevantes.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Recuperar muchos y quedarte con los mejores para la ventana de contexto = reranking con cross-encoder (nueva se&ntilde;al de relevancia). Recalcular coseno repite el mismo orden; temperature no afecta ranking; TF-IDF es lexico, no semantico.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/rerank.html">docs.aws Bedrock reranking</a></div>'
    ),
))

# ============================================================
# Q18 - Comprehend PII EN/ES + Guardrails en outputs + logs S3
# ============================================================
cards.append(card(
    question="Una empresa de salud resume notas clinicas con Amazon Bedrock. Procesa 20.000 notas al dia (picos de 100 por minuto) con <b>preprocesamiento sub-segundo</b>. Debe remover toda la PII <b>antes</b> de enviar texto a Bedrock, detectar PII en <b>ingles y espa&ntilde;ol</b>, evitar que el FM devuelva identificadores medicos en los resumenes y dar <b>visibilidad de auditoria</b> de los campos redactados. &iquest;Que solucion cumple?",
    options=[
        "Amazon Macie para detectar PII antes de invocar el FM, reglas de AWS WAF para bloquear respuestas salientes con datos sensibles y guardar las notas procesadas en DynamoDB",
        "AWS Glue DataBrew para una transformacion de enmascarado unica sobre todas las notas, enviar las notas enmascaradas a Bedrock y Lake Formation con seguridad a nivel de columna para el acceso posterior",
        "Un flujo multi-etapa con Amazon Comprehend para PII estandar y un modelo de Bedrock afinado para identificadores medicos especializados, combinar salidas para redactar cada nota, invocar Bedrock y guardar logs de auditoria en S3",
        "Amazon Comprehend para detectar PII en ingles y espa&ntilde;ol y redactar automaticamente antes de invocar Bedrock, Bedrock Guardrails para bloquear identificadores medicos no permitidos en las salidas y guardar logs de entrada y salida redactados en S3 para auditoria",
    ],
    correct=3,
    key="off1-q18",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Comprehend (PII EN/ES) + Guardrails en salidas + logs redactados en S3.</div>'
        '<p><b>El problema:</b> redaccion de PII en tiempo real y multi-idioma (ingles y espa&ntilde;ol) con latencia sub-segundo, mas evitar identificadores medicos en la salida y dar auditoria de lo redactado.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Amazon Comprehend</b> detecta y redacta PII en texto no estructurado en ingles y espa&ntilde;ol con latencia sub-segundo para las 100 peticiones por minuto. <b>Bedrock Guardrails</b> bloquea identificadores medicos prohibidos en los resumenes generados (salida). Guardar logs de entrada y salida redactados en <b>S3</b> da la visibilidad de auditoria de cada campo redactado.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Macie + WAF + DynamoDB:</b> Macie descubre datos sensibles en objetos de S3, no da deteccion en tiempo real por peticion ni redaccion sub-segundo; y WAF filtra HTTP, no contenido generado por el FM.</li>'
        '<li><b>Glue DataBrew + Lake Formation:</b> DataBrew hace transformaciones por lotes, no deteccion continua en tiempo real; un enmascarado unico no protege las notas nuevas que llegan a diario, y Lake Formation gestiona permisos, no detecta PII ni filtra la salida del FM.</li>'
        '<li><b>Comprehend + modelo Bedrock afinado (multi-etapa):</b> agregar un FM afinado suma pasos y latencia, arriesgando el sub-segundo; la deteccion nativa de Comprehend ya cubre ingles y espa&ntilde;ol sin fine-tuning extra.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Redaccion de PII en tiempo real, multi-idioma y sub-segundo = Comprehend (deteccion/redaccion nativa). Evitar datos sensibles en la SALIDA del FM = barandas de contenido. Auditoria = logs en S3. Macie es descubrimiento en S3, no tiempo real.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html">docs.aws Comprehend deteccion de PII</a></div>'
    ),
))



# ============================================================
# Q19 - AppConfig feature flags + linear deploy de modelos
# ============================================================
cards.append(card(
    question="Una app de GenAI usa varios FMs de Amazon Bedrock desde funciones Lambda en tres Regiones. Necesita <b>seleccion dinamica de modelo</b> por calidad y latencia, <b>cambiar de modelo sin modificar ni redeployar codigo</b>, un despliegue gradual empezando por el <b>20% del trafico</b> y <b>rollback automatico si el error supera 1%</b>. &iquest;Que solucion cumple?",
    options=[
        "Guardar la configuracion de seleccion en DynamoDB con global tables para multi-Region, reglas de EventBridge que vigilen metricas de CloudWatch e invoquen Lambdas que actualicen la tabla, y codigo custom que consulte DynamoDB antes de cada invocacion",
        "Crear versiones de la Lambda por configuracion de modelo, usar alias y routing para desplazar el trafico gradualmente desde 20% y despliegues de CodeDeploy que vigilen CloudWatch y hagan rollback al superar umbrales",
        "Dashboards de CloudWatch para calidad y latencia, logica custom en la Lambda que elija modelo por umbrales y variables de entorno en Systems Manager Parameter Store actualizables entre Regiones",
        "Usar AWS AppConfig con feature flags para los criterios de seleccion, reglas de validacion sobre la tasa de error, la extension AppConfig Agent en Lambda para leer la configuracion en tiempo de ejecucion y estrategias de despliegue lineal que liberen modelos desde el 20% del trafico",
    ],
    correct=3,
    key="off1-q19",
    answer=(
        '<div class="verdict">Correcta: {{L}} - AWS AppConfig con feature flags, despliegue lineal y rollback automatico.</div>'
        '<p><b>El problema:</b> cambiar de modelo sin tocar ni redeployar codigo, con despliegue gradual (empezar en 20%) y rollback automatico si el error pasa de 1%. Un feature flag es un interruptor de configuracion que altera el comportamiento sin desplegar codigo.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AppConfig</b> gestiona configuracion dinamica sin desplegar codigo mediante feature flags y estrategias de despliegue. La <b>extension AppConfig Agent</b> en Lambda lee la configuracion en tiempo de ejecucion sin cambiar codigo, asi se cambia de modelo en caliente. Las <b>estrategias de despliegue lineal</b> liberan desde el 20% del trafico, y las reglas de validacion con metricas de error de CloudWatch dan el rollback automatico al superar el umbral.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>DynamoDB global tables + Lambda:</b> exige codigo custom que consulte DynamoDB antes de cada invocacion (incumple "sin modificar codigo") y no trae despliegue gradual exacto al 20% ni rollback automatico integrados.</li>'
        '<li><b>Versiones y alias de Lambda + CodeDeploy:</b> los alias reparten trafico, pero requieren una version nueva de la funcion por cada cambio de modelo, es decir redeployar codigo en cada cambio; incumple el requisito.</li>'
        '<li><b>Logica custom + Parameter Store:</b> la logica de seleccion en la Lambda exige cambios de codigo cuando cambia; Parameter Store actualiza variables sin redeploy, pero no aporta despliegue gradual al 20% ni rollback automatico integrados.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cambiar comportamiento sin redeployar + despliegue gradual + rollback automatico = el servicio gestionado de configuracion dinamica (feature flags, deployment strategies, validacion). Alias de Lambda implican una version nueva por cambio; logica custom implica cambios de codigo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html">docs.aws AWS AppConfig</a></div>'
    ),
))

# ============================================================
# Q20 - Migrar a OpenSearch + FM embeddings + kNN (semantic search)
# ============================================================
cards.append(card(
    question="Un servicio de descubrimiento de restaurantes (50M de usuarios/mes) quiere <b>busqueda semantica</b> sobre 20M de restaurantes y 200M de rese&ntilde;as guardados hoy en PostgreSQL. Debe soportar <b>consultas complejas en lenguaje natural</b>, responder el 95% en 500 ms, mantener frescura horaria y escalar de forma costo-efectiva en picos, con el <b>MENOR esfuerzo de desarrollo</b>. &iquest;Que solucion cumple?",
    options=[
        "Migrar los datos a Amazon OpenSearch Service e implementar busqueda por palabra clave con analizadores custom y ajuste de relevancia por atributos (tipo de cocina, caracteristica, ubicacion), con endpoints HTTP de API Gateway que transformen las consultas en parametros estructurados",
        "Migrar los datos a Amazon OpenSearch Service, usar un FM de Bedrock para generar embeddings de descripciones, rese&ntilde;as y menus, convertir la consulta en lenguaje natural con el mismo FM y hacer busquedas k-NN para hallar resultados semanticamente similares",
        "Guardar los datos en Amazon RDS for PostgreSQL con la extension pgvector, generar embeddings con un FM de Bedrock guardados en RDS y una Lambda que convierta la consulta a vector y ejecute busquedas de similitud en la base",
        "Migrar los datos a un knowledge base de Bedrock con un pipeline de ingesta custom, generar embeddings automaticamente y usar la Retrieve API de Bedrock con busqueda vectorial integrada para consultar en lenguaje natural",
    ],
    correct=1,
    key="off1-q20",
    answer=(
        '<div class="verdict">Correcta: {{L}} - OpenSearch + embeddings con un FM de Bedrock + busqueda k-NN.</div>'
        '<p><b>El problema:</b> busqueda semantica (por significado, no por palabras exactas) a gran escala, con latencia sub-500 ms, frescura horaria y escalado costo-efectivo, con el menor desarrollo. Los embeddings son vectores que representan el significado del texto; k-NN busca los vectores mas cercanos.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>OpenSearch</b> con <b>k-NN</b> hace busqueda semantica convirtiendo consultas y datos en embeddings con un FM de Bedrock. Soporta consultas complejas en lenguaje natural con rendimiento sub-500 ms a escala, escala solo en los picos de forma costo-efectiva y, al ser gestionado, minimiza el desarrollo frente a soluciones a medida.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>OpenSearch con busqueda por palabra clave:</b> el keyword search hace coincidencia exacta o parcial de texto, no entiende el significado; no soporta las consultas complejas en lenguaje natural pedidas.</li>'
        '<li><b>RDS PostgreSQL + pgvector + Lambda:</b> soporta vectores, pero exige mucho mas desarrollo que servicios gestionados: una Lambda que vectorice en tiempo real y gestionar la integracion Lambda-RDS.</li>'
        '<li><b>Knowledge base de Bedrock + ingesta custom:</b> los KB son para RAG y no dan busqueda semantica directa a esta escala; migrar 20M+200M con un pipeline custom es mucho mas desarrollo, y el KB agrega generacion de respuesta que aqui no se necesita.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Busqueda semantica a gran escala con minimo desarrollo = motor de busqueda gestionado + embeddings + vecinos mas cercanos. La busqueda por palabra clave no entiende significado; pgvector en una base relacional o una base de conocimiento con ingesta custom suman mucho desarrollo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html">docs.aws OpenSearch k-NN</a></div>'
    ),
))

# ============================================================
# Q21 - AgentCore outbound credential provider AssumeRole
# ============================================================
cards.append(card(
    question="Una empresa global con 25 cuentas en AWS Organizations usa Amazon Bedrock AgentCore para un asistente que debe acceder a datos de clientes en <b>varias cuentas</b> (tablas DynamoDB por unidad de negocio) y actuar <b>en nombre de usuarios especificos</b>, con fronteras de seguridad estrictas, <b>preservando la identidad del usuario</b> y escalando a mas de 40 cuentas. &iquest;Que solucion cumple con el <b>MENOR esfuerzo operativo</b>?",
    options=[
        "Configurar SCPs en la organizacion que permitan explicitamente al rol de ejecucion del asistente hacer dynamodb:GetItem y dynamodb:Query en todas las cuentas miembro, y referenciar los ARNs cross-account de las tablas directamente",
        "Configurar un outbound credential provider que ejecute AssumeRole para obtener credenciales temporales cross-account, crear en cada cuenta un rol IAM con relacion de confianza al rol del asistente y permisos a sus tablas, e incluir session tags en el AssumeRole para identificar al usuario",
        "Crear un asistente separado en cada cuenta, un API Gateway REST con logica de enrutamiento y Lambda authorizers que dirijan las consultas al asistente adecuado segun el identificador de unidad de negocio",
        "Usar AWS Resource Access Manager (RAM) para compartir las tablas DynamoDB de cada cuenta hacia una cuenta central donde corre el asistente, con permisos de RAM para el acceso cross-account y otorgar al rol de AgentCore acceso directo a los recursos compartidos",
    ],
    correct=1,
    key="off1-q21",
    answer=(
        '<div class="verdict">Correcta: {{L}} - outbound credential provider con AssumeRole + roles de confianza por cuenta + session tags.</div>'
        '<p><b>El problema:</b> acceso cross-account seguro que <b>preserva la identidad del usuario</b>, escala a 40+ cuentas y con minimo esfuerzo. AssumeRole obtiene credenciales temporales de un rol en otra cuenta; los session tags viajan con esas credenciales para identificar al usuario.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>outbound credential provider</b> ejecuta <b>AssumeRole</b> para obtener credenciales temporales y acceder a recursos en otras cuentas. Los <b>session tags</b> preservan la identidad del usuario final. Como cada cuenta nueva solo requiere crear un rol con confianza al del asistente, escala a 40+ cuentas con cambios minimos: el menor esfuerzo operativo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SCPs para "permitir" el acceso:</b> las SCPs solo restringen (son guardrails), no otorgan permisos cross-account; definen el maximo permitido pero no habilitan el acceso, asi que el asistente no llegaria a las tablas.</li>'
        '<li><b>Un asistente por cuenta + API Gateway:</b> desplegar y mantener 25 (luego 40+) asistentes con enrutamiento propio es mucho overhead, con mantenimiento y actualizaciones duplicados.</li>'
        '<li><b>AWS RAM para compartir DynamoDB:</b> DynamoDB no es un tipo de recurso compartible por RAM (RAM comparte subnets de VPC, transit gateways, licencias, etc.), asi que no aplica.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Acceso cross-account que preserva identidad y escala = asumir un rol de confianza por cuenta (credenciales temporales) + session tags. Las SCPs solo restringen (no otorgan); RAM no comparte tablas DynamoDB.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_monitor.html">docs.aws AssumeRole y session tags</a></div>'
    ),
))

# ============================================================
# Q23 - Titan Text Embeddings multilingue sin traducir + semantic chunking
# ============================================================
cards.append(card(
    question="Una empresa de salud recupera literatura medica para investigadores y desplegara la app en varios paises. Debe indexar 50.000 documentos con mucho texto y <b>terminologia especializada en ingles, frances y aleman</b>, con <b>alta precision</b> de busqueda para terminos medicos y <b>minimo codigo custom y mantenimiento</b>. &iquest;Que solucion cumple?",
    options=[
        "Usar Titan Multimodal Embeddings para convertir las paginas a imagenes y generar leyendas de texto, creando un knowledge base multimodal para el contenido medico",
        "Usar un knowledge base de Bedrock como vector store y Amazon Translate para el procesamiento multilingue, con deteccion de idioma y traduccion automatica en cada consulta",
        "Usar Titan Text Embeddings traduciendo todos los documentos no ingleses al ingles antes de procesarlos, con chunking por secciones logicas para mejorar la precision",
        "Usar Titan Text Embeddings para procesar los documentos en su idioma original sin traducir, con semantic chunking a nivel de seccion medica que preserve el contexto terminologico y mantenga dimensiones de vector moderadas",
    ],
    correct=3,
    key="off1-q23",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Titan Text Embeddings en el idioma original (sin traducir) + semantic chunking por seccion medica.</div>'
        '<p><b>El problema:</b> busqueda precisa de terminologia medica en tres idiomas (ingles, frances, aleman) con minimo codigo y mantenimiento. Un embedding multilingue representa el significado sin necesidad de traducir.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Titan Text Embeddings V2</b> soporta de forma nativa ingles, frances y aleman sin traducir, preservando el contexto de la terminologia especializada (clave para la precision). El <b>semantic chunking a nivel de seccion medica</b> mantiene el contexto terminologico con dimensiones de vector manejables. Es el enfoque de menor codigo y mantenimiento.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Titan Multimodal (paginas a imagenes):</b> esta pensado para pares imagen-texto, no para documentos con mucho texto; convertir a imagenes y luego generar leyendas agrega complejidad y overhead innecesarios.</li>'
        '<li><b>KB + Amazon Translate por consulta:</b> traducir en tiempo real cada consulta agrega latencia y requiere codigo custom para deteccion y enrutamiento de idioma en cada peticion.</li>'
        '<li><b>Traducir todo al ingles antes de procesar:</b> no cumple el soporte multilingue real y, segun la documentacion de AWS, las consultas entre idiomas dan resultados sub-optimos, bajando la precision.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Contenido multilingue con precision y minimo mantenimiento = embeddings de texto multilingue nativos (procesar en el idioma original), no traducir todo ni traducir por consulta. Titan Multimodal es para imagen-texto, no texto pesado.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html">docs.aws Titan Text Embeddings</a></div>'
    ),
))

# ============================================================
# Q24 - Step Functions Standard Map + InvokeModel + BDA API
# ============================================================
cards.append(card(
    question="Una empresa procesa reportes de proyecto en S3. Necesita un flujo que analice el <b>sentimiento general</b> de un conjunto de reportes y <b>extraiga segmentos especificos</b> de cada uno. Hay un modelo de Bedrock para el sentimiento y un proyecto de Bedrock Data Automation definido. &iquest;Como orquestar el flujo de la forma <b>MAS eficiente operativamente</b>?",
    options=[
        "Un flujo en Amazon Bedrock Flows con un nodo de data retrieval que lea los reportes de S3 y dos nodos Lambda que procesen cada reporte en secuencia, invocando el modelo para el sentimiento y la Data Automation API para extraer los segmentos",
        "Un flujo en Amazon Bedrock Flows con un nodo de data retrieval desde S3, un nodo de codigo inline que invoque la Data Automation API para extraer segmentos y un nodo de Amazon Lex que llame a un bot que interactue con el modelo para el sentimiento",
        "Una state machine de AWS Step Functions Standard con un estado Map que itere sobre los reportes en S3, un paso InvokeModel de Bedrock para el sentimiento, una Lambda que use la Data Automation API para extraer segmentos y una segunda Lambda que verifique el estado con un bucle de back-off",
        "Una state machine de AWS Step Functions Express con un estado parallel que itere sobre los reportes, un paso InvokeModel para el sentimiento y un paso Lambda que use la Data Automation API para extraer segmentos y verificar el estado hasta terminar",
    ],
    correct=2,
    key="off1-q24",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Step Functions Standard con estado Map + InvokeModel + Lambda para la Data Automation API.</div>'
        '<p><b>El problema:</b> orquestar el procesamiento por lotes de un conjunto de reportes (sentimiento + extraccion) de la forma mas eficiente, manejando la extraccion asincrona de Data Automation.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Step Functions Standard</b> orquesta flujos de forma nativa; su estado <b>Map</b> procesa el conjunto de reportes en paralelo con concurrencia configurable (lo mas eficiente). Integra directo con <b>InvokeModel</b> de Bedrock para el sentimiento, y usa Lambdas para llamar la Data Automation API con un <b>bucle de back-off</b> que maneja el proceso asincrono sin ejecuciones larguisimas.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Bedrock Flows con data retrieval de S3 + 2 Lambdas en secuencia:</b> Flows no tiene un nodo de data retrieval que lea un conjunto de archivos directo de S3 (los nodos de retrieval consultan knowledge bases); ademas encadenar en secuencia no da el paralelismo del lote ni maneja el polling asincrono.</li>'
        '<li><b>Bedrock Flows + nodo de Amazon Lex:</b> Lex es para chatbots conversacionales, no un orquestador de procesamiento de documentos; usarlo para el sentimiento agrega complejidad y no es su caso de uso.</li>'
        '<li><b>Step Functions Express con estado parallel:</b> un Express dura maximo 5 minutos y no soporta wait states (necesarios para el back-off); y un estado parallel corre ramas fijas simultaneas, no itera sobre un conjunto de entradas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Procesar un conjunto de items en paralelo con orquestacion = un workflow de larga duracion con estado Map (un estado parallel corre ramas fijas, no itera). El tipo Express dura 5 min y no soporta wait states para back-off asincrono.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-map-state.html">docs.aws Step Functions Map state</a></div>'
    ),
))



# ============================================================
# Q26 - Combo reliability + determinismo (temp + templates + cache + guardrails + retry)
# ============================================================
cards.append(card(
    question="Una app clinica con un modelo de Amazon Bedrock a veces genera <b>informacion inexacta</b>, tiene <b>latencia que oscila</b> entre 200 ms y 3 s, y ante <b>consultas identicas produce salidas distintas</b>. Hay que resolver todo para fiabilidad y precision clinica en produccion. &iquest;Que solucion cumple?",
    options=[
        "Aumentar la memoria de computo asignada y configurar provisioned concurrency, con conexiones WebSocket para entregar actualizaciones del modelo en tiempo real a los clientes",
        "Configurar una arquitectura de microservicios con contenedores en Amazon EKS y usar Apache Kafka para procesar los mensajes de forma asincrona y desacoplada entre servicios",
        "Desarrollar un modelo de ML custom, aplicar cuantizacion del modelo para optimizar el rendimiento y desplegarlo en endpoints dedicados de SageMaker AI con auto scaling",
        "Bajar la temperature del modelo, establecer plantillas de prompt, cachear respuestas, configurar Bedrock Guardrails y montar reintentos con backoff exponencial mas logging y monitoreo",
    ],
    correct=3,
    key="off1-q26",
    answer=(
        '<div class="verdict">Correcta: {{L}} - bajar temperature + plantillas + cache + Guardrails + reintentos con backoff + logging.</div>'
        '<p><b>El problema:</b> tres sintomas a la vez: salidas distintas ante la misma consulta (falta de determinismo), informacion inexacta y latencia variable. temperature controla la aleatoriedad de la generacion.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>bajar temperature</b> reduce la variabilidad (el modelo elige tokens de mayor probabilidad), atacando las salidas inconsistentes. Las <b>plantillas de prompt</b> estandarizan la entrada; el <b>cache</b> de respuestas reduce las oscilaciones de latencia; <b>Guardrails</b> filtra informacion inexacta para la precision clinica; y los <b>reintentos con backoff</b> mas logging/monitoreo mejoran la fiabilidad. Cada tecnica ataca un sintoma.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Mas memoria + provisioned concurrency + WebSockets:</b> son ajustes de infraestructura de computo que no aplican a la inferencia de Bedrock (servicio gestionado); no atacan inexactitud, inconsistencia ni oscilacion de latencia.</li>'
        '<li><b>Microservicios en EKS + Kafka:</b> resuelven escalabilidad y desacoplamiento, pero no la causa de fondo (respuestas inexactas e inconsistentes ni la variabilidad de latencia).</li>'
        '<li><b>Modelo custom + cuantizacion + SageMaker:</b> mucho overhead de desarrollo frente a usar el tuning y guardrails de Bedrock, y la cuantizacion/endpoints no corrigen inconsistencia ni inexactitud.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Misma consulta con salidas distintas = baja la temperature (determinismo). Un servicio gestionado de FMs no expone ajustes de computo (memoria, concurrency) para la inferencia. Precision = barandas de contenido; latencia = cache; fiabilidad = reintentos/monitoreo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html">docs.aws parametros de inferencia (temperature)</a></div>'
    ),
))

# ============================================================
# Q27 - Bedrock Evaluations + CodePipeline gate de calidad
# ============================================================
cards.append(card(
    question="Una empresa de servicio al cliente con Amazon Bedrock necesita un proceso de QA que <b>compare automaticamente</b> las salidas de varias plantillas de prompt, detecte problemas de calidad, de <b>metricas cuantitativas</b>, permita <b>feedback humano</b> e <b>impida desplegar</b> configuraciones que no alcancen un umbral de calidad. &iquest;Que solucion cumple?",
    options=[
        "Usar Amazon Bedrock evaluation jobs para comparar salidas con datasets de prompts custom y AWS CodePipeline para ejecutar las evaluaciones cuando cambien las plantillas y desplegar solo las configuraciones con score sobre el umbral",
        "Una Lambda que envie consultas de muestra a varias configuraciones y guarde respuestas en S3, QuickSight para visualizar patrones, revision manual diaria y CodePipeline para desplegar las que superen el umbral",
        "Un framework de testing con Lambda que muestree trafico de produccion y duplique peticiones a la version nueva, Amazon Comprehend para comparar por sentimiento y bloquear el despliegue si baja el sentimiento",
        "Alarmas de CloudWatch para latencia y errores de Bedrock, reglas de EventBridge para notificar al superar umbrales y un flujo de aprobacion en Systems Manager para chequeos manuales de calidad",
    ],
    correct=0,
    key="off1-q27",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock evaluation jobs + CodePipeline como gate de calidad.</div>'
        '<p><b>El problema:</b> comparar automaticamente varias plantillas de prompt con metricas cuantitativas y feedback humano, y bloquear despliegues que no pasen el umbral.</p>'
        '<p><b>Por que la respuesta sirve:</b> los <b>evaluation jobs</b> de Bedrock comparan salidas de modelo con datasets de prompts custom, dando metricas cuantitativas y soporte para evaluacion humana. <b>CodePipeline</b> integra esas evaluaciones en el flujo de despliegue e impone el umbral, bloqueando las configuraciones que no cumplan antes de liberar.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Lambda + QuickSight + revision manual:</b> depende de revision manual, no de comparacion automatizada entre versiones de plantilla ni de metricas estandar; no cumple lo pedido.</li>'
        '<li><b>Framework con Comprehend por sentimiento:</b> usar solo sentimiento es insuficiente para calidad de servicio (importan exactitud, relevancia y adecuacion); no compara salidas de multiples plantillas ni da metricas completas.</li>'
        '<li><b>CloudWatch + EventBridge + aprobacion manual:</b> CloudWatch mide latencia y errores operativos, no evalua la calidad de la respuesta ni compara plantillas de prompt.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Comparar prompts/modelos con metricas y feedback humano = Bedrock evaluation jobs. Meter un gate de calidad que bloquee despliegues = integrarlos en CodePipeline. Sentimiento solo o metricas operativas de CloudWatch no miden calidad de respuesta.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock model evaluation</a></div>'
    ),
))

# ============================================================
# Q28 - Strands Agents SDK + session managers + MCP + supervisor
# ============================================================
cards.append(card(
    question="Se dise&ntilde;a un sistema autonomo de soporte con Amazon Bedrock que exige <b>alto throughput con baja latencia</b>, <b>razonamiento multi-paso</b>, <b>persistir el estado de sesion</b> entre interacciones, integrar herramientas externas via <b>MCP</b> y un <b>agente supervisor</b> que delegue en agentes especializados. &iquest;Que solucion cumple?",
    options=[
        "Integrar LangChain con Bedrock, DynamoDB para el estado de sesion, servidores MCP custom para las herramientas y logica de orquestacion custom para la delegacion entre agentes",
        "FMs de Bedrock, AWS Step Functions para orquestar la delegacion, Amazon ElastiCache para datos de sesion y funciones Lambda custom para integrar herramientas externas",
        "Usar el SDK de Strands Agents con el proveedor de Amazon Bedrock, configurar session managers para memoria persistente, integrar las herramientas externas con MCP e implementar patrones supervisor-colaborador",
        "Usar Agent Squad y Amazon EventBridge para orquestar la delegacion y DynamoDB para los datos de sesion en vez de los session managers del SDK",
    ],
    correct=2,
    key="off1-q28",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Strands Agents SDK (proveedor Bedrock) + session managers + MCP + patron supervisor-colaborador.</div>'
        '<p><b>El problema:</b> baja latencia, memoria de sesion persistente, integracion nativa MCP (Model Context Protocol, estandar para conectar herramientas externas) y delegacion supervisor-especialistas, todo con poca complejidad.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>SDK de Strands Agents</b> es un framework para sistemas multi-agente autonomos que integra nativamente con Bedrock. Trae <b>session managers</b> para persistir memoria entre interacciones, <b>integracion MCP nativa</b> para herramientas externas y patrones <b>supervisor-colaborador</b> para delegar tareas. Cubre todos los requisitos sin codigo de orquestacion a medida.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>LangChain + DynamoDB + MCP custom:</b> DynamoDB para sesion agrega viajes de red por lectura/escritura (mas latencia), y los servidores MCP y la orquestacion custom suman mucha complejidad frente a patrones multi-agente integrados.</li>'
        '<li><b>FMs + Step Functions + ElastiCache + Lambda:</b> orquestar con Step Functions agrega overhead y latencia; ElastiCache es cache rapido pero requiere implementacion custom para memoria multi-agente; y las Lambdas no dan soporte MCP nativo.</li>'
        '<li><b>Agent Squad + EventBridge:</b> no da soporte MCP nativo ni session managers integrados, y orquestar con EventBridge introduce latencia asincrona frente al patron supervisor-colaborador sincrono del SDK.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Multi-agente autonomo con memoria persistente, MCP nativo y baja latencia = el SDK de agentes con session managers y patron supervisor-colaborador. Orquestar con Step Functions/EventBridge agrega latencia; DynamoDB/ElastiCache exigen memoria custom.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html">docs.aws agentes en Amazon Bedrock</a></div>'
    ),
))

# ============================================================
# Q29 - MemoryDB Valkey vector cache + RANGE query (cache semantico)
# ============================================================
cards.append(card(
    question="Un asistente con Amazon Bedrock ve que el <b>40% de las consultas</b> preguntan lo mismo con <b>distinta redaccion</b>. Se quiere <b>reducir llamadas redundantes</b> al modelo, dar <b>respuestas consistentes a preguntas semanticamente equivalentes</b> y mantener <b>baja latencia</b>. &iquest;Que solucion cumple?",
    options=[
        "Desplegar un cluster Amazon DynamoDB Accelerator (DAX) como cache en memoria, con el texto de la consulta como partition key y la respuesta como sort key, consultando con una expresion de filtro con el operador LIKE",
        "Desplegar un cluster de Amazon OpenSearch Service con k-NN para guardar pares texto consulta-respuesta y usar k-NN aproximado para hallar consultas similares y sus respuestas",
        "Un cache en Amazon DynamoDB con un indice secundario global sobre el texto de consulta normalizado, aplicando stemming a las consultas entrantes y consultando ese indice",
        "Generar embeddings de las consultas con Amazon Bedrock, guardar en Amazon MemoryDB for Valkey hash sets de embeddings y respuestas, y usar una consulta RANGE para hallar consultas similares y sus respuestas",
    ],
    correct=3,
    key="off1-q29",
    answer=(
        '<div class="verdict">Correcta: {{L}} - embeddings + Amazon MemoryDB for Valkey (cache vectorial) con consulta RANGE.</div>'
        '<p><b>El problema:</b> un cache que agrupe preguntas por <b>significado</b> (no por texto exacto), porque el 40% varia la redaccion; debe dar respuestas consistentes y baja latencia. Un cache semantico usa embeddings (vectores de significado) para hallar similares.</p>'
        '<p><b>Por que la respuesta sirve:</b> se generan <b>embeddings</b> de las consultas con Bedrock y se guardan en <b>MemoryDB for Valkey</b>, que almacena vectores y usa consultas <b>RANGE</b> para hallar los semanticamente similares. Asi preguntas equivalentes reciben la misma respuesta cacheada, se reducen llamadas redundantes y la busqueda en memoria da baja latencia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>DAX con LIKE:</b> DAX hace lookups exactos por clave, no identifica similitud semantica; con el 40% de redacciones distintas fallaria casi todos los aciertos de cache.</li>'
        '<li><b>OpenSearch k-NN con pares de texto:</b> k-NN necesita embeddings (vectores) como entrada, no pares de texto; tal cual se plantea no identificaria consultas semanticamente similares.</li>'
        '<li><b>DynamoDB con GSI + stemming:</b> normalizar y stemming son coincidencia exacta sobre texto normalizado; redacciones distintas producen formas normalizadas distintas y fallan el cache.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cache "semantico" (misma pregunta con otras palabras) = embeddings + un store vectorial en memoria. Los lookups exactos (cache clave-valor, normalizacion/stemming) fallan ante redacciones distintas; la busqueda por vecinos necesita vectores, no texto.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/memorydb/latest/devguide/vector-search.html">docs.aws MemoryDB vector search</a></div>'
    ),
))

# ============================================================
# Q30 - Guardrails denied topics + S3 logs + PII filter
# ============================================================
cards.append(card(
    question="Una empresa financiera con Amazon Bedrock automatiza servicio al cliente. Por regulacion, el asistente <b>no debe dar consejos de inversion</b>, <b>no debe divulgar PII</b> de clientes y hay que <b>registrar todas las interacciones</b> para auditoria. &iquest;Que solucion cumple?",
    options=[
        "Usar Bedrock Guardrails con un denied topics para consejos de inversion, guardar los model invocation logs en un bucket de S3 y configurar filtros de informacion sensible para detectar PII",
        "Usar Bedrock Guardrails con un denied topics para consejos de inversion y configurar alarmas de CloudWatch para monitorear los patrones de respuesta del asistente e identificar contenido riesgoso",
        "Configurar AWS CloudTrail para registrar las llamadas de API del asistente y usar prompt engineering en la instruccion del modelo para evitar que hable de temas relacionados con inversion",
        "Crear roles IAM con politicas restrictivas de minimo privilegio y usar CloudWatch Logs para monitorear las interacciones del asistente en busca de terminos relacionados con inversion",
    ],
    correct=0,
    key="off1-q30",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails denied topics + model invocation logs en S3 + filtros de informacion sensible (PII).</div>'
        '<p><b>El problema:</b> tres requisitos: bloquear consejos de inversion, evitar divulgar PII y auditar todas las interacciones. Un denied topic es un tema que Guardrails bloquea tanto en entrada como en salida.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Guardrails</b> con un <b>denied topic</b> bloquea proactivamente los consejos de inversion en entradas y respuestas; los <b>filtros de informacion sensible</b> detectan y bloquean PII; y guardar los <b>model invocation logs en S3</b> registra todas las interacciones para auditoria. Cubre los tres requisitos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Guardrails denied topics + alarmas de CloudWatch:</b> las alarmas alertan reactivamente sobre metricas, no dan logging de auditoria completo de las interacciones, y falta el filtro de PII.</li>'
        '<li><b>CloudTrail + prompt engineering:</b> CloudTrail registra quien invoco y cuando, pero no los prompts, respuestas ni el contexto conversacional; y el prompt engineering solo no bloquea de forma fiable consejos de inversion ni PII.</li>'
        '<li><b>Roles IAM restrictivos + CloudWatch Logs:</b> IAM controla permisos de acceso, no filtra contenido; sin Guardrails no se bloquea proactivamente el contenido, y monitorear no impide generarlo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Bloquear un tema (p.ej. consejo de inversion) + bloquear datos personales = Guardrails (denied topics + filtros de informacion sensible). Auditar el contenido de las conversaciones = model invocation logs en S3, no CloudTrail (solo API) ni prompt engineering.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html">docs.aws Guardrails denied topics</a></div>'
    ),
))

# ============================================================
# Q31 - Lambda + EventBridge + CloudWatch QA semantico 500+ golden
# ============================================================
cards.append(card(
    question="Una app de GenAI con un FM de Bedrock necesita QA automatizado que verifique salidas contra respuestas esperadas y detecte regresiones. Debe comparar contra mas de <b>500 golden examples</b> por <b>similitud semantica</b>, soportar <b>reglas programadas</b>, escalar a mas de <b>2000 casos en 6 meses sin cambios de arquitectura</b>, generar <b>visualizaciones</b> de calidad y <b>alertar</b> ante degradacion. &iquest;Que solucion cumple?",
    options=[
        "Funciones Lambda que invoquen el FM sobre los casos y comparen contra las salidas esperadas, reglas programadas de EventBridge para ejecutar las pruebas y metricas custom en CloudWatch para visualizaciones y alarmas",
        "Canaries de CloudWatch Synthetics que invoquen las APIs del FM, comparen con scripts de baseline y alarmas de CloudWatch por tasa de exito de los canaries",
        "Amazon Comprehend para analizar la calidad detectando cambios de sentimiento y patrones de frases clave, alarmas de CloudWatch por umbrales de score y processing jobs de SageMaker AI para evaluaciones programadas",
        "Workflows de AWS Step Functions para ejecutar los casos y validar respuestas, resultados en DynamoDB y dashboards de CloudWatch para visualizar",
    ],
    correct=0,
    key="off1-q31",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Lambda (invoca FM y puntua similitud) + EventBridge programado + metricas custom en CloudWatch.</div>'
        '<p><b>El problema:</b> QA que compara contra 500-2000 golden examples por similitud semantica, en pruebas programadas, que escale sin rearquitectura, con visualizaciones y alertas. Golden examples = respuestas esperadas de referencia.</p>'
        '<p><b>Por que la respuesta sirve:</b> las <b>Lambda</b> implementan la logica de scoring por similitud semantica sobre datasets grandes e invocan el FM por SDK, y escalan automaticamente a miles de casos sin cambios de arquitectura. Las <b>reglas programadas de EventBridge</b> corren las pruebas periodicas, y las <b>metricas custom en CloudWatch</b> dan visualizaciones y alarmas de degradacion.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CloudWatch Synthetics canaries:</b> monitorean disponibilidad y validaciones simples; no hacen scoring de similitud semantica ni evaluan datasets de 500+ ejemplos.</li>'
        '<li><b>Amazon Comprehend (sentimiento/frases):</b> analiza propiedades del texto pero no compara salidas contra golden examples por similitud semantica; no determina si una respuesta es equivalente a la esperada.</li>'
        '<li><b>Step Functions + DynamoDB:</b> orquesta y guarda resultados, pero no soporta de forma nativa el scoring por similitud semantica y a esta escala el volumen de transiciones de estado agrega overhead excesivo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>QA semantico contra muchos golden examples, programado y escalable sin rearquitectura = funciones serverless (scoring + invocan el FM) + un scheduler de eventos + metricas custom de CloudWatch. Synthetics y Comprehend no hacen similitud semantica contra referencias.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html">docs.aws EventBridge reglas programadas</a></div>'
    ),
))



# ============================================================
# Q33 - Guardrails + Converse API con image logging a S3
# ============================================================
cards.append(card(
    question="Un banco crea un asistente con Amazon Bedrock para consultas de cuenta. No debe <b>revelar PII</b> ni <b>enviar PII</b> en los prompts al modelo, no debe dar <b>consejos de inversion</b> y debe registrar <b>audit logs</b> de todas las interacciones, <b>incluidas imagenes y documentos</b> transmitidos. &iquest;Que solucion cumple con el <b>MENOR esfuerzo operativo</b>?",
    options=[
        "Usar Amazon Macie para detectar y redactar la PII en entradas y respuestas, prompt engineering para que el asistente evite temas de inversion y AWS CloudTrail para capturar los logs completos de cada conversacion con imagenes",
        "Una Lambda con Amazon Comprehend para detectar y redactar la PII de las entradas, topic modeling de Comprehend para evitar temas de inversion y metricas custom de CloudWatch para capturar el contenido de las conversaciones",
        "Configurar Bedrock Guardrails con una politica de informacion sensible para detectar y filtrar PII, una politica de temas para que el asistente evite consejos de inversion, y usar la Converse API para el model invocation logging con delivery e image logging a S3",
        "Usar controles regex para detectar la PII, prompt engineering para no devolver PII ni temas de inversion y habilitar model invocation logging, delivery logging e image logging hacia un bucket de S3",
    ],
    correct=2,
    key="off1-q33",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails (politica de info sensible + topic policy) + Converse API con image logging a S3.</div>'
        '<p><b>El problema:</b> filtrar PII en entrada y salida, bloquear consejos de inversion y auditar todo el contenido, incluidas imagenes y documentos, con el minimo esfuerzo. La Converse API permite logging completo de invocaciones, incluido image logging.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Guardrails</b> con politica de informacion sensible detecta y filtra PII en prompts y respuestas sin codigo custom (evita que la PII llegue al modelo y al cliente); la <b>topic policy</b> (denied topics) bloquea el tema consejos de inversion; y el <b>model invocation logging via Converse API</b> con delivery e <b>image logging a S3</b> captura el contenido completo, incluidas imagenes y documentos, cumpliendo la auditoria con minimo esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Macie + prompt engineering + CloudTrail:</b> Macie descubre datos en S3, no inspecciona ni redacta PII inline en prompts/respuestas en tiempo real; el prompt engineering solo no bloquea inversion de forma fiable; y CloudTrail registra eventos de gestion de API, no el contenido, imagenes o documentos.</li>'
        '<li><b>Lambda + Comprehend + topic modeling + CloudWatch:</b> construir la Lambda con Comprehend exige codigo y mantenimiento (mas esfuerzo que un guardrail gestionado); el topic modeling agrupa documentos, no es un control en tiempo real; y CloudWatch custom metrics guarda numeros, no el contenido ni imagenes.</li>'
        '<li><b>Regex + prompt engineering + logging a S3:</b> el regex detecta PII estructurada pero no nombres o direcciones no estructuradas; el prompt engineering no bloquea inversion de forma fiable; y mantener patrones regex es mas esfuerzo que una politica gestionada.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>PII inline en prompts/respuestas + bloquear un tema + auditar contenido con imagenes = barandas (info sensible + denied topics) y model invocation logging con image logging a S3. Macie es descubrimiento en S3; el registro de solo llamadas de API no guarda el contenido conversacional.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html">docs.aws model invocation logging</a></div>'
    ),
))

# ============================================================
# Q34 - AgentCore + OpenSearch Serverless KB + web crawler + PII filter
# ============================================================
cards.append(card(
    question="Una empresa reemplaza su FAQ por un agente de Amazon Bedrock AgentCore con acceso a mas de 700.000 consultas de su foro de soporte; se suman mas de 1.500 al dia. El agente debe <b>refrescar los datos a diario</b> y <b>no referirse a PII</b> publicada por los usuarios. &iquest;Que solucion cumple?",
    options=[
        "Usar Amazon OpenSearch Serverless como knowledge base, configurar un web crawler como fuente de datos, aplicar filtros de informacion sensible al agente y usar RAG para recuperar del knowledge base",
        "Usar Amazon Aurora PostgreSQL Serverless como knowledge base, un web crawler como fuente custom, pedir al modelo por prompt que bloquee toda PII y usar RAG para recuperar del knowledge base",
        "Usar Step Functions con Lambda, una cola SQS, DynamoDB y Comprehend para rastrear el foro, importar incrementalmente a S3 y redactar PII, y actualizar el prompt del modelo a diario con los datos nuevos",
        "Usar Amazon S3 Vectors como knowledge base, un web crawler como fuente, Amazon Macie para identificar PII y una Lambda para redactarla, y RAG para recuperar del knowledge base",
    ],
    correct=0,
    key="off1-q34",
    answer=(
        '<div class="verdict">Correcta: {{L}} - OpenSearch Serverless como KB + web crawler + filtros de informacion sensible + RAG.</div>'
        '<p><b>El problema:</b> un vector store que soporte una fuente tipo web crawler para refrescar a diario un volumen grande, con bloqueo de PII. RAG recupera del KB y genera la respuesta.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>OpenSearch Serverless</b> es un vector store que soporta la fuente de datos <b>web crawler</b> (refresco diario del foro). Los <b>filtros de informacion sensible</b> de Guardrails enmascaran o bloquean PII, y el enfoque <b>RAG</b> deja que el agente responda con el knowledge base sin compartir PII.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Aurora PostgreSQL Serverless + web crawler:</b> Aurora sirve como KB, pero no soporta un web crawler como fuente de datos; y pedir por prompt que bloquee PII no es fiable.</li>'
        '<li><b>Step Functions + Lambda + SQS + Comprehend + prompt diario:</b> mucho overhead operativo frente al web crawler integrado, y el volumen no cabe directo en el prompt por el limite de contexto.</li>'
        '<li><b>S3 Vectors + web crawler + Macie:</b> S3 Vectors no soporta web crawler como fuente, y Macie no puede escanear buckets de S3 Vectors (solo buckets S3 tradicionales).</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Refrescar a diario un sitio/foro para una base de conocimiento = fuente de datos tipo web crawler (soportada por el vector store serverless de busqueda). Bloquear PII = filtros de informacion sensible de las barandas, no prompts. Ojo: no todos los vector stores soportan el web crawler como fuente.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html">docs.aws fuentes de datos de Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q35 - Transcribe streaming 100ms + InvokeModelWithResponseStream
# ============================================================
cards.append(card(
    question="Se construye un asistente de voz en tiempo real para apoyar a agentes durante llamadas. Debe convertir audio a texto con latencia extremo a extremo <b>menor a 500 ms</b>, generar sugerencias con GenAI, permitir que supervisores <b>califiquen las sugerencias en vivo</b> y almacenar todas las interacciones para auditoria. &iquest;Que solucion cumple?",
    options=[
        "Usar Amazon Transcribe batch para analisis post-llamada, Lambda que generen respuestas con InvokeModel de Bedrock y CloudWatch para registrar el feedback del supervisor",
        "Usar la API de streaming de Amazon Transcribe con chunks de audio de 100 ms, llamar InvokeModelWithResponseStream de Bedrock para procesar en tiempo real y guardar las calificaciones del supervisor en una tabla DynamoDB",
        "Usar la API de streaming de Transcribe con ajustes estandar, Bedrock batch para la inferencia y guardar grabaciones y metadatos en S3 con politicas de lifecycle",
        "Usar Transcribe para speech-to-text y analitica en tiempo real, Comprehend para sentimiento, SQS para encolar tareas y InvokeModel de Bedrock para generar respuestas",
    ],
    correct=1,
    key="off1-q35",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Transcribe streaming (chunks de 100 ms) + InvokeModelWithResponseStream + calificaciones en DynamoDB.</div>'
        '<p><b>El problema:</b> transcripcion y generacion en tiempo real bajo 500 ms, mas calificaciones de supervisor en vivo y almacenamiento para auditoria. El streaming y el response streaming devuelven datos a medida que se producen, minimizando latencia.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>API de streaming de Transcribe con chunks de 100 ms</b> optimiza la latencia para voz en tiempo real; <b>InvokeModelWithResponseStream</b> transmite la inferencia a medida que se genera, cumpliendo los menos de 500 ms; y <b>DynamoDB</b> da almacenamiento de baja latencia para las calificaciones del supervisor en vivo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Transcribe batch + CloudWatch:</b> el batch es para analisis post-llamada de audio grabado, no tiempo real; y CloudWatch guarda logs y metricas, no las calificaciones interactivas del supervisor.</li>'
        '<li><b>Transcribe streaming + Bedrock batch:</b> la inferencia batch es asincrona y prioriza throughput sobre latencia; no cumple los menos de 500 ms.</li>'
        '<li><b>Transcribe + Comprehend + SQS + InvokeModel:</b> SQS agrega latencia al encolar, InvokeModel (sin streaming) devuelve solo tras generar todo, y no hay mecanismo para calificar en vivo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Tiempo real de voz bajo 500 ms = transcripcion en streaming + invocacion del modelo con respuesta en stream (respuesta a medida que se genera). El batch (transcripcion o inferencia) y las colas agregan latencia; invocar sin stream espera a terminar todo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html">docs.aws Transcribe streaming</a></div>'
    ),
))

# ============================================================
# Q36 - Outposts data residency + Wavelength inferencia <100ms
# ============================================================
cards.append(card(
    question="Una empresa de salud multinacional analiza registros y ensayos clinicos con GenAI. Algunos paises exigen guardar los datos de pacientes <b>on-premises dentro de cada pais</b> (residencia de datos). Necesita diagnostico asistido de <b>baja latencia (menor a 100 ms)</b> en clinicas remotas, usar FMs en la nube para analitica a gran escala y flujos de desarrollo consistentes en entornos hibridos. &iquest;Que solucion cumple con el <b>MENOR esfuerzo operativo</b>?",
    options=[
        "AWS Global Accelerator para reducir latencia, replicar los datos on-premises a S3 con DataSync y procesar todas las peticiones en un endpoint de inferencia centralizado en una Region",
        "Desplegar FMs en varias Regiones sobre instancias EC2 con GPU, replicar los datos de pacientes a la nube y centralizar entrenamiento e inferencia",
        "Desplegar FMs open source en EC2 en cada pais para la residencia, guardar los datos en volumenes EBS locales, gestionar actualizaciones con Systems Manager y exportar manualmente insights agregados como CSV a S3 por Region",
        "Usar AWS Outposts para procesar y guardar los datos sensibles on-premises en los paises con requisitos de residencia y desplegar AWS Wavelength en las clinicas remotas para la inferencia en tiempo real",
    ],
    correct=3,
    key="off1-q36",
    answer=(
        '<div class="verdict">Correcta: {{L}} - AWS Outposts (residencia on-premises) + AWS Wavelength (inferencia en el borde, menor a 100 ms).</div>'
        '<p><b>El problema:</b> residencia de datos por pais (datos sensibles locales), inferencia de muy baja latencia en clinicas remotas y flujos de desarrollo consistentes en hibrido, con minimo overhead. Outposts lleva infraestructura AWS al sitio; Wavelength la lleva al borde de redes de telecom.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Outposts</b> mantiene los datos sensibles localmente (cumple residencia) con APIs de AWS y flujos consistentes. <b>Wavelength</b> despliega computo cerca de las clinicas en el borde de la red movil, logrando inferencia bajo 100 ms. Los FMs en la nube analizan a gran escala datos agregados o no sensibles. El hibrido da consistencia con el minimo overhead.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Global Accelerator + DataSync a S3 + endpoint central:</b> replicar los datos a S3 viola la residencia on-premises, y la inferencia centralizada en una Region suele superar los 100 ms para clinicas globales.</li>'
        '<li><b>FMs en EC2 en varias Regiones + replicar a la nube:</b> replicar todos los datos incumple la residencia, y la inferencia centralizada en la nube agrega latencia mayor a 100 ms hacia clinicas remotas.</li>'
        '<li><b>FMs open source en EC2 por pais + CSV manual:</b> cumple residencia pero con mucho overhead (gestionar infraestructura, updates y exportes CSV) y sin infraestructura de borde, EC2 en Regiones estandar no logra la latencia menor a 100 ms.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Residencia de datos on-premises = servicio que extiende la infraestructura AWS al sitio del cliente. Inferencia de muy baja latencia cerca del usuario = computo en el borde de la red movil. Replicar datos a la nube rompe la residencia; la inferencia centralizada agrega latencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html">docs.aws AWS Outposts</a></div>'
    ),
))

# ============================================================
# Q37 - Text-to-SQL sobre RDS + Guardrails + confidence scoring
# ============================================================
cards.append(card(
    question="Una empresa SaaS recomienda upgrades de cabina de avion. Hospedara modelos de SageMaker AI en Amazon Bedrock via Custom Model Import y debe analizar el <b>historial de viajes almacenado en una base relacional Amazon RDS</b>, entregando resultados <b>consistentes, relevantes y precisos</b> entre varias aerolineas y poblaciones. &iquest;Que solucion cumple?",
    options=[
        "Usar Bedrock Knowledge Bases con RAG para analizar el historial y dar busqueda semantica, con Guardrails y flujos de validacion con Step Functions y Lambda para reducir alucinaciones",
        "Usar OpenSearch Service con busqueda vectorial de embeddings del historial para recuperacion por similitud, con Guardrails, confidence scoring y busqueda semantica para reducir alucinaciones",
        "Implementar transformaciones text-to-SQL con validaciones SQL para recuperar patrones de reserva, preferencias y lealtad de RDS, con Guardrails para filtrar contenido y flujos de validacion con Step Functions y Lambda para reducir alucinaciones",
        "Implementar transformaciones text-to-SQL con validaciones SQL para recuperar patrones de reserva, preferencias y lealtad de RDS, con Guardrails para filtrar respuestas y confidence scoring mas busqueda por similitud semantica para reducir alucinaciones",
    ],
    correct=3,
    key="off1-q37",
    answer=(
        '<div class="verdict">Correcta: {{L}} - text-to-SQL sobre RDS + Guardrails + confidence scoring y similitud semantica.</div>'
        '<p><b>El problema:</b> los datos estan en una base <b>relacional (estructurada)</b> en RDS. Hay que consultarlos con fidelidad y dar resultados consistentes y precisos, reduciendo alucinaciones. text-to-SQL traduce la peticion en lenguaje natural a SQL.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>text-to-SQL con validaciones SQL</b> recupera con exactitud patrones de reserva, preferencias y lealtad de la base relacional (respeta la estructura tabular). <b>Guardrails</b> filtra las respuestas, y el <b>confidence scoring</b> mas la <b>busqueda por similitud semantica</b> reducen alucinaciones y aseguran relevancia y consistencia entre aerolineas y poblaciones.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Knowledge Bases con RAG:</b> RAG y su chunking estan optimizados para datos no estructurados en vector stores, no para datos relacionales de RDS; el chunking rompe relaciones estructurales de las tablas y pierde contexto.</li>'
        '<li><b>OpenSearch vectorial:</b> la busqueda vectorial recupera datos no estructurados por similitud; convertir datos tabulares a embeddings pierde el contexto relacional entre filas y columnas necesario para recomendar bien.</li>'
        '<li><b>text-to-SQL + Step Functions/Lambda (sin confidence scoring):</b> maneja bien lo estructurado, pero sin confidence scoring ni similitud semantica no reduce alucinaciones lo suficiente; no cumple del todo relevancia y precision.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Datos ESTRUCTURADOS en una base relacional = text-to-SQL (no RAG ni vectorial, que son para no estructurado y rompen relaciones tabulares). Reducir alucinaciones a fondo = confidence scoring + similitud semantica, no solo orquestacion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-build-structured.html">docs.aws consultas de datos estructurados (text-to-SQL)</a></div>'
    ),
))

# ============================================================
# Q38 - Hierarchical chunking + hybrid search + score threshold
# ============================================================
cards.append(card(
    question="Un desarrollador construye un RAG con Bedrock Knowledge Bases sobre 50 libros de texto (500 paginas de promedio) en S3. En pruebas, las respuestas traen <b>informacion irrelevante</b> y a veces <b>pierden contexto critico</b> de la fuente. Debe dar respuestas precisas, con baja latencia y <b>sin alucinaciones</b>. &iquest;Que solucion cumple?",
    options=[
        "Usar semantic chunking que segmente por limites de tema, un unico modelo de embeddings para todo el contenido y query expansion para reformular las preguntas antes de recuperar",
        "Configurar fixed-size chunking de 256 tokens, filtrado por metadatos segun secciones del documento y un modelo Titan Embeddings optimizado para busqueda semantica",
        "Usar Amazon ElastiCache para cache semantico de consultas comunes, Claude Sonnet para reformular consultas y bucles de feedback del modelo en tiempo real para mejorar la calidad continuamente",
        "Aplicar hierarchical chunking con chunks de 200 y de 1000 tokens, busqueda hibrida (vectorial + palabra clave) y ajustar el umbral de relevancia para filtrar resultados de baja confianza",
    ],
    correct=3,
    key="off1-q38",
    answer=(
        '<div class="verdict">Correcta: {{L}} - hierarchical chunking (200 y 1000 tokens) + busqueda hibrida + umbral de relevancia.</div>'
        '<p><b>El problema:</b> documentos muy largos (500 paginas) donde un concepto abarca varias secciones; hay resultados irrelevantes y perdida de contexto. El chunking define como se trocean los documentos para indexarlos.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>hierarchical chunking</b> crea chunks peque&ntilde;os (detalle, 200 tokens) y grandes padres (contexto amplio, 1000 tokens), preservando informacion fina y contexto a lo largo de documentos largos. La <b>busqueda hibrida</b> (vectorial + palabra clave) mejora la precision, y el <b>umbral de relevancia</b> filtra resultados de baja confianza, reduciendo alucinaciones e irrelevancia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Semantic chunking + un solo embedding + query expansion:</b> agrupa por tema pero no mantiene contexto multi-nivel en documentos grandes; mejora consistencia pero no aporta busqueda hibrida ni contexto jerarquico.</li>'
        '<li><b>Fixed-size de 256 tokens:</b> trocea de forma uniforme sin respetar limites semanticos, rompe conceptos complejos de los libros y pierde contexto; insuficiente para textos densos.</li>'
        '<li><b>ElastiCache + reformular + feedback:</b> el cache y la reformulacion ayudan con consultas repetidas o complejas, pero no atacan la causa (mal chunking y metodo de busqueda) del contexto perdido y los resultados irrelevantes.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Documentos largos con conceptos que cruzan secciones = hierarchical chunking (chunks chicos + padres grandes) para preservar detalle y contexto. Sumar busqueda hibrida y umbral de relevancia reduce irrelevancia y alucinaciones; fixed-size rompe conceptos.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws chunking en Knowledge Bases</a></div>'
    ),
))



# ============================================================
# Q39 - Glue Data Quality + Data Wrangler + Lambda alerts
# ============================================================
cards.append(card(
    question="Se dise&ntilde;a un pipeline de validacion de datos estructurados que consume un FM de Amazon Bedrock. La mala calidad ha causado alucinaciones. El pipeline debe asegurar <b>consistencia de esquema</b>, <b>detectar anomalias</b>, <b>vigilar nulos</b>, rastrear resultados de validacion, con monitoreo por metricas, <b>alertas custom</b> por umbrales y <b>validacion configurable por reglas</b>, manejando ~5 TB diarios y escalable. &iquest;Que solucion cumple con la <b>MENOR complejidad operativa</b>?",
    options=[
        "Processing jobs de SageMaker AI y Lambda para validar y detectar anomalias, metricas en CloudWatch y Step Functions para orquestar y manejar fallos",
        "AWS Glue Data Quality y SageMaker Data Wrangler para validar, reportes en S3 y metricas en CloudWatch, Data Firehose para enviar datos enriquecidos a OpenSearch, y dashboards de anomalias integrados con alarmas de CloudWatch",
        "SageMaker Data Wrangler y Lambda para validar y detectar anomalias, metricas resumidas en CloudWatch y Step Functions para ejecutar flujos ante chequeos fallidos",
        "AWS Glue Data Quality para validacion basada en reglas, SageMaker Data Wrangler para analizar features, Lambda para la logica de alertas custom y CloudWatch para monitorear metricas y umbrales",
    ],
    correct=3,
    key="off1-q39",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Glue Data Quality (reglas) + Data Wrangler + Lambda para alertas + CloudWatch.</div>'
        '<p><b>El problema:</b> validacion por reglas configurables (esquema, anomalias, nulos) a escala (5 TB/dia), con metricas, alertas custom y el menor overhead. Glue Data Quality es validacion de datos gestionada y serverless por reglas.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Glue Data Quality</b> da validacion por reglas gestionada y serverless (consistencia de esquema, anomalias, nulos, metricas) a escala de 5 TB/dia con crecimiento futuro. <b>Data Wrangler</b> analiza y entiende las features, <b>Lambda</b> implementa la logica de alertas custom y <b>CloudWatch</b> monitorea metricas y notifica al superar umbrales.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SageMaker processing jobs + Lambda + Step Functions:</b> los processing jobs son batch y exigen orquestacion, provisioning e invocacion explicita por corrida; suma gestion y overhead continuos.</li>'
        '<li><b>Glue Data Quality + Data Wrangler + Firehose a OpenSearch:</b> OpenSearch es para busqueda, analitica y visualizacion, no para validacion por reglas; enviar con Firehose y gestionar shards e indices agrega complejidad innecesaria.</li>'
        '<li><b>Solo Data Wrangler + Lambda:</b> no usa Data Quality, que es lo que aporta la validacion de esquema y deteccion de anomalias por reglas nativas; hacerlo a mano sube la complejidad de codigo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Validacion de datos por reglas configurables a escala con minimo overhead = AWS Glue Data Quality (gestionado, serverless). OpenSearch es busqueda/analitica, no validacion; processing jobs batch suman orquestacion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html">docs.aws AWS Glue Data Quality</a></div>'
    ),
))

# ============================================================
# Q40 - Metadata-aware filtering en Bedrock KB
# ============================================================
cards.append(card(
    question="Un RAG con un knowledge base de Bedrock sobre S3 (transcripciones, reportes archivados y documentos de noticias de emergencia) usa embeddings de ultima generacion y buena recuperacion, pero los usuarios reportan <b>respuestas lentas e irrelevantes</b>. La causa: las busquedas vectoriales evaluan <b>demasiados documentos, de muchos tipos y en periodos largos</b>. Los modelos no mejoraran con mas fine-tuning. Hay que mejorar la precision con <b>restricciones mas inteligentes</b> y <b>cambios minimos</b> a la arquitectura. &iquest;Que solucion cumple?",
    options=[
        "Migrar a Amazon OpenSearch Service y usar campos vectoriales y filtros por metadatos para acotar el alcance de la recuperacion",
        "Mejorar los embeddings con un modelo adaptado al dominio entrenado especificamente en contenido de noticias de emergencia",
        "Migrar a una coleccion de Amazon OpenSearch Serverless para filtrado estructurado por metadatos y categorizacion de documentos durante la recuperacion",
        "Habilitar filtrado por metadatos dentro del knowledge base de Bedrock indexando los metadatos de los objetos de S3",
    ],
    correct=3,
    key="off1-q40",
    answer=(
        '<div class="verdict">Correcta: {{L}} - habilitar metadata-aware filtering en el knowledge base de Bedrock (indexar metadatos de S3).</div>'
        '<p><b>El problema:</b> se evaluan demasiados documentos de muchos tipos y periodos; hay que <b>acotar</b> el conjunto candidato con filtros, no cambiar el modelo, y con cambios minimos.</p>'
        '<p><b>Por que la respuesta sirve:</b> los knowledge bases de Bedrock soportan <b>filtrado por metadatos</b> (timestamps, tipo de contenido, categorias) aplicado en tiempo de consulta <b>antes</b> del scoring de similitud vectorial. Esto reduce el conjunto candidato solo a los documentos relevantes, atacando la causa directa, y usa capacidades nativas: cambios minimos a la arquitectura.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Migrar a OpenSearch Service:</b> ofrece filtros por metadatos, pero migrar exige re-plataformar el vector store y reindexar todo; no es un cambio minimo.</li>'
        '<li><b>Embeddings adaptados al dominio:</b> personaliza el modelo de embeddings, pero el enunciado dice que los modelos no mejoraran con fine-tuning; la causa es el alcance, no los embeddings.</li>'
        '<li><b>Migrar a OpenSearch Serverless:</b> reemplaza la arquitectura actual del knowledge base (no es cambio minimo), y el KB de Bedrock ya soporta filtrado por metadatos de forma nativa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Se evaluan demasiados documentos y sobran resultados irrelevantes: acota el conjunto con filtrado por metadatos en tiempo de consulta (capacidad nativa de la base de conocimiento gestionada), sin migrar de plataforma ni tocar los embeddings.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html">docs.aws filtrado por metadatos en Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q41 - AgentCore para Strands+OpenAI: memory, Okta, >1h
# ============================================================
cards.append(card(
    question="Un desarrollador crea un agente con el framework open source <b>Strands Agents</b> usando modelos <b>OpenAI</b>. Al desplegar en us-east-1 necesita seguridad y escalabilidad enterprise, observabilidad en tiempo real, soportar procesos de <b>mas de 1 hora</b>, integrar con el IdP <b>Okta</b> y tener <b>memoria y contexto</b>. &iquest;Que solucion cumple de la forma <b>MAS eficiente operativamente</b>?",
    options=[
        "Desplegar una app en contenedores en Amazon ECS con Fargate usando FMs Anthropic de Bedrock, y usar Bedrock AgentCore para observabilidad e integracion con el IdP",
        "Usar el framework open source CrewAI para desplegar el agente en Bedrock, con CrewAI flows para orquestar y gestionar estados e integraciones nativas de AWS para observabilidad y autenticacion",
        "Crear una Lambda, un deployment y alias de AgentCore, un flujo custom para integrar Okta y dar contexto, y CloudWatch Logs para monitoreo y observabilidad",
        "Instrumentar y desplegar el agente en Amazon Bedrock AgentCore, usar AgentCore Memory para el contexto y las funcionalidades integradas para Okta y observabilidad",
    ],
    correct=3,
    key="off1-q41",
    answer=(
        '<div class="verdict">Correcta: {{L}} - desplegar en AgentCore + AgentCore Memory + integraciones nativas (Okta, observabilidad).</div>'
        '<p><b>El problema:</b> operar un agente Strands+OpenAI con seguridad y escala enterprise, procesos de mas de 1 hora, memoria/contexto, Okta y observabilidad, con el minimo overhead. AgentCore es una plataforma gestionada para agentes.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AgentCore</b> opera agentes de forma segura y escalable con cualquier framework y modelo (soporta Strands con OpenAI). Su Runtime soporta cargas de hasta 8 horas (cubre >1 h), <b>AgentCore Memory</b> da contexto, <b>AgentCore Identity</b> integra Okta y trae observabilidad integrada, sin gestionar infraestructura.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>ECS/Fargate con FMs Anthropic:</b> cambiar a Anthropic obliga a refactorizar el agente hecho sobre OpenAI, y gestionar contenedores y escalado suma overhead frente a la plataforma gestionada.</li>'
        '<li><b>CrewAI en Bedrock:</b> cambiar de Strands a CrewAI exige refactorizar mucho codigo e integraciones custom; no es eficiente.</li>'
        '<li><b>Lambda + flujo custom para Okta:</b> Lambda tiene timeout de 15 minutos (no cubre procesos de mas de 1 hora), y el flujo custom para Okta y contexto suma overhead frente a lo gestionado.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Operar un agente (cualquier framework/modelo) con memoria, IdP y procesos largos sin gestionar infra = la plataforma gestionada de agentes (runtime de hasta 8 h, gestion de contexto, identidad, observabilidad). Lambda topa en 15 min; cambiar de framework/modelo obliga a refactorizar.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html">docs.aws Bedrock AgentCore</a></div>'
    ),
))

# ============================================================
# Q42 - Bedrock prompt caching (checkpoints messages/system)
# ============================================================
cards.append(card(
    question="Una aseguradora tiene una app de soporte con FMs de Amazon Bedrock (Converse API): los usuarios suben documentos e imagenes y luego preguntan sobre ellos. Las respuestas son precisas pero la <b>latencia es demasiado alta</b>. Se necesita una solucion <b>costo-efectiva para reducir la latencia</b>. &iquest;Que solucion cumple?",
    options=[
        "Usar fixed-size chunking en Bedrock, convertir los chunks a embeddings, escribirlos en un indice vectorial de OpenSearch y usar ese indice al llamar la Converse API",
        "Aumentar la capacidad de invocacion configurando provisioned throughput y determinar los model units adecuados probando en Bedrock Evaluations",
        "Habilitar prompt caching de Bedrock, fijar el minimo de tokens de cache por checkpoint al valor mas bajo posible y poner el cache checkpoint en los campos messages y system de cada peticion",
        "Cachear el contexto del prompt en Amazon ElastiCache (Redis OSS) con TTL de 10 minutos y consultar ese cache al llamar la Converse API",
    ],
    correct=2,
    key="off1-q42",
    answer=(
        '<div class="verdict">Correcta: {{L}} - habilitar Bedrock prompt caching con checkpoints en messages y system.</div>'
        '<p><b>El problema:</b> la latencia viene de <b>reprocesar</b> el mismo contexto grande (documentos e imagenes subidos) en cada pregunta. Hay que evitar reprocesarlo, de forma barata. El prompt caching guarda partes del contexto ya procesadas.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>prompt caching</b> de Bedrock almacena porciones del contexto para que el modelo no reprocese entradas ya vistas. Poniendo el <b>cache checkpoint en messages y system</b> se cachean los documentos e imagenes subidos, y las preguntas siguientes usan el contenido cacheado sin reprocesarlo. Reduce a la vez la latencia de inferencia y el costo de tokens de entrada.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Fixed-size chunking + OpenSearch:</b> el chunking ayuda a la ingesta/recuperacion de un KB, no reduce la latencia de la Converse API cuando se suben documentos; agrega costo y complejidad con un indice vectorial.</li>'
        '<li><b>Provisioned throughput:</b> reserva capacidad para mas throughput, pero no reduce la latencia de reprocesar contexto grande y encarece por la capacidad por hora; no ataca la causa.</li>'
        '<li><b>ElastiCache Redis:</b> cachear el prompt no evita que el FM reprocese todo el documento e imagen en cada peticion; agrega costo de infraestructura sin atacar la causa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Latencia por reprocesar el mismo contexto grande repetidamente = Bedrock prompt caching (checkpoints en messages/system). Un cache externo (ElastiCache) no evita el reprocesamiento del FM; provisioned throughput sube capacidad, no baja la latencia por contexto.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html">docs.aws Bedrock prompt caching</a></div>'
    ),
))

# ============================================================
# Q43 - API Gateway usage plans + throttling por tier
# ============================================================
cards.append(card(
    question="Una app de GenAI tiene clientes estandar y premium y tres endpoints: generacion de imagenes (premium), text completion (todos) y un <b>servicio critico de analisis de documentos</b> que exige 99.9% de disponibilidad y sub-500 ms incluso en picos de 5x, y que empezo a devolver errores <b>429 Too Many Requests</b>. Se necesita usar Amazon API Gateway para proteger el servicio critico, dar acceso adecuado a todos y recolectar <b>metricas de throttling</b> para auditoria, con el <b>MENOR esfuerzo operativo</b>. &iquest;Que solucion cumple?",
    options=[
        "Un unico usage plan con una sola API key para todos, throttling a nivel de stage para toda la API, un dashboard de CloudWatch para los 429 y reintentos del SDK con backoff exponencial",
        "Configurar AWS WAF con rate-based rules para limitar todos los endpoints, con un limite mayor para el servicio de analisis, y un dashboard de CloudWatch para patrones de trafico",
        "Implementar throttling del lado del cliente que rastree tasas por servicio y ajuste dinamicamente antes de acercarse a los limites, con una solucion de monitoreo custom para las metricas",
        "Crear usage plans separados para premium y estandar con limites de throttling propios, configurar throttling a nivel de metodo en cada plan, asignar mayor throughput al endpoint de analisis de documentos y asignar API keys por tier",
    ],
    correct=3,
    key="off1-q43",
    answer=(
        '<div class="verdict">Correcta: {{L}} - usage plans separados por tier + throttling a nivel de metodo + mayor throughput al servicio critico.</div>'
        '<p><b>El problema:</b> priorizar un endpoint critico (99.9%, sub-500 ms) frente a los 429, diferenciar tiers de cliente y recolectar metricas de throttling, con minimo overhead. Un usage plan de API Gateway gestiona throttling y cuotas por API key.</p>'
        '<p><b>Por que la respuesta sirve:</b> los <b>usage plans</b> de API Gateway habilitan throttling y cuotas por tier con API keys. El <b>throttling a nivel de metodo</b> permite fijar un limite mayor al endpoint critico de analisis de documentos (para el 99.9%), y planes separados diferencian premium y estandar. API Gateway recolecta automaticamente metricas detalladas de throttling en CloudWatch para auditoria, con minimo overhead.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Un solo usage plan con una API key:</b> no diferencia premium de estandar, y el throttling a nivel de stage aplica limites uniformes a todos los metodos, sin poder priorizar el servicio critico.</li>'
        '<li><b>AWS WAF rate-based rules:</b> son para proteccion DDoS (bloquean tras el umbral), no para throttling que mantenga disponibilidad; no diferencian tier ni priorizan por metodo.</li>'
        '<li><b>Throttling del lado del cliente:</b> cada cliente debe implementar y mantener la logica (mucho overhead) y no garantiza el 99.9%; ademas el monitoreo custom es mas complejo que las metricas nativas de API Gateway.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Priorizar endpoints y diferenciar tiers con throttling y metricas nativas = API Gateway usage plans + throttling a nivel de metodo (no stage, que es uniforme). WAF rate-based es DDoS, no gestion de disponibilidad.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html">docs.aws API Gateway usage plans</a></div>'
    ),
))

# ============================================================
# Q44 - Step Functions circuit breaker con DynamoDB
# ============================================================
cards.append(card(
    question="Un pipeline de procesamiento de documentos con Amazon Bedrock a veces sufre timeouts en picos. Hay que <b>detectar cuando la tasa de error supera 10% en cualquier ventana de 60 s</b>, <b>cambiar a una ruta alternativa</b> al superar el umbral, <b>reanudar automaticamente</b> el procesamiento normal al recuperarse, y procesar todos los documentos en <b>15 minutos</b>. &iquest;Que solucion cumple?",
    options=[
        "Un flujo de Step Functions con una Lambda que consulte metricas de CloudWatch de Bedrock, guarde la tasa de error en DynamoDB y, al superar 10%, indique al personal actualizar manualmente el flujo para desviar el trafico",
        "Desplegar varias state machines identicas de Step Functions con varios modelos de Bedrock detras de API Gateway y una Lambda de health check que enrute a la que responda mas rapido",
        "Un flujo de Step Functions que implemente un patron circuit breaker rastreando los fallos de invocacion de Bedrock en DynamoDB y enrute los trabajos entre la ruta normal y la alternativa segun el estado de fallo actual",
        "Una state machine de Step Functions con un Task state con logica Retry/Catch para las llamadas a Bedrock y una alarma de CloudWatch que dispare una regla de EventBridge para desviar el trafico a la ruta alternativa al superar 10% de error",
    ],
    correct=2,
    key="off1-q44",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Step Functions con patron circuit breaker rastreando fallos en DynamoDB.</div>'
        '<p><b>El problema:</b> detectar una tasa de error agregada (>10% en ventanas de 60 s), conmutar a una ruta alternativa automaticamente y volver solo al recuperarse, dentro de 15 min. Un circuit breaker rastrea la tasa de fallos y enruta entre ruta normal y de respaldo.</p>'
        '<p><b>Por que la respuesta sirve:</b> el patron <b>circuit breaker</b> con Step Functions y DynamoDB mantiene el estado, rastrea los fallos de invocacion de Bedrock en una ventana movil de 60 s, <b>abre el circuito</b> cuando el error pasa de 10%, enruta a la ruta alternativa y <b>reanuda automaticamente</b> el flujo normal al recuperarse, cumpliendo el limite de 15 min.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Lambda + intervencion manual:</b> detecta el 10%, pero exige que el personal actualice el flujo a mano; no es cambio automatico ni reanudacion automatica y puede pasarse de los 15 min.</li>'
        '<li><b>Varias state machines + enrutar por rapidez:</b> se enfoca en latencia, no en la tasa de error en 60 s; no garantiza activar el respaldo cuando el error supera el umbral.</li>'
        '<li><b>Task state con Retry/Catch:</b> maneja errores de invocacion individuales, pero no rastrea la tasa agregada en el tiempo; no implementa el circuit breaker con recuperacion automatica.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Detectar una TASA de error agregada en una ventana y conmutar/reanudar automaticamente = patron circuit breaker (estado en DynamoDB con Step Functions). Retry/Catch maneja fallos individuales, no tasas; evita la intervencion manual.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html">docs.aws AWS Step Functions</a></div>'
    ),
))



# ============================================================
# Q45 - Text-to-SQL safety: Guardrails + SQL parse + RDS Data API audit
# ============================================================
cards.append(card(
    question="Una empresa financiera crea una app de GenAI donde analistas consultan datos sensibles en <b>lenguaje natural</b>. Se necesita un framework de seguridad de contenido que haga <b>text-to-SQL</b> evitando salidas da&ntilde;inas: <b>detectar y bloquear intentos de SQL injection</b> en los prompts, <b>validar el SQL generado contra esquemas predefinidos</b> y crear un <b>audit trail</b> de las transformaciones. &iquest;Que solucion cumple?",
    options=[
        "Bedrock con filtrado de contenido integrado, Amazon GuardDuty con reglas custom de deteccion de amenazas SQL, Lambda que verifiquen el SQL contra definiciones en Parameter Store y EventBridge para guardar los registros en S3",
        "Un pipeline de validacion multi-etapa que use Bedrock Guardrails para filtrar entradas, Lambda con librerias de parsing SQL para validar la sintaxis, la RDS Data API para verificar contra los esquemas y recolectar logs de auditoria antes de ejecutar cada consulta",
        "AWS CloudTrail para registrar todas las llamadas de API de la base de datos, roles IAM de minimo privilegio para acceder a los datos y AWS WAF con reglas para filtrar entradas maliciosas en la capa de aplicacion antes de generar el SQL",
        "Entrenar un modelo custom de SageMaker AI que transforme texto a SQL de forma segura, VPC endpoints para aislar la base de datos con datos sensibles y guardar el historial completo de consultas y transformaciones en una tabla de DynamoDB",
    ],
    correct=1,
    key="off1-q45",
    answer=(
        '<div class="verdict">Correcta: {{L}} - pipeline multi-etapa: Guardrails (entrada) + Lambda con parsing SQL + RDS Data API con logs de auditoria.</div>'
        '<p><b>El problema:</b> tres controles sobre text-to-SQL: bloquear SQL injection en el prompt, validar el SQL generado contra esquemas y auditar las transformaciones.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> filtra entradas y detecta ataques de prompt y patrones maliciosos en lenguaje natural. <b>Lambda con librerias de parsing SQL</b> valida la sintaxis del SQL generado contra los esquemas predefinidos, previniendo la injection. La <b>RDS Data API</b> (con CloudTrail) verifica contra esquemas y da los logs de auditoria de las transformaciones antes de ejecutar cada consulta.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>GuardDuty + Parameter Store:</b> GuardDuty detecta amenazas en la infraestructura/entorno AWS, no valida SQL ni filtra contenido de prompts en lenguaje natural; le falta el guardrail especifico para seguridad de prompts de GenAI.</li>'
        '<li><b>CloudTrail + IAM + WAF:</b> CloudTrail registra llamadas de API pero no inspecciona el contenido de los prompts ni valida el SQL contra esquemas; IAM y WAF dan control de acceso y filtrado de red, no filtrado de contenido para GenAI.</li>'
        '<li><b>Modelo custom de SageMaker + VPC endpoints:</b> entrenar un modelo propio exige muchos recursos y no da el filtrado de contenido especifico; los VPC endpoints aislan la red pero no validan entradas ni SQL ni crean audit trail.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Seguridad de text-to-SQL = barandas para el prompt (bloquear injection) + parsing/validacion del SQL contra el esquema + auditoria de las consultas. GuardDuty detecta amenazas de infraestructura; WAF e IAM no inspeccionan el contenido de los prompts.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
    ),
))

# ============================================================
# Q46 - Bedrock tracing OrchestrationTrace en agent handoffs
# ============================================================
cards.append(card(
    question="Un sistema multi-agente con Amazon Bedrock procesa 50.000 transacciones/dia. Un agente de cara al cliente interactua con agentes especializados que usan <b>distintos FMs</b> (Claude, Titan). El 8% de las transacciones falla en los <b>handoffs entre agentes</b> pese a codigos de estado exitosos: hay problemas de validacion de parametros (precision numerica y tipos de datos inconsistentes) entre FMs. Hay que <b>identificar donde ocurren</b> los fallos y dar <b>validacion consistente</b> en todas las interacciones. &iquest;Que solucion cumple?",
    options=[
        "Una regla de EventBridge que capture todas las llamadas de API de los agentes y un flujo de Step Functions que valide las peticiones entre handoffs, estandarizando formatos y aplicando transformaciones por FM",
        "CloudWatch Logs con logging estructurado y correlation IDs por transaccion entre agentes, y una Lambda de preprocesamiento que valide la conformidad del esquema de la API antes de enviar al siguiente agente",
        "Habilitar Bedrock tracing, configurar OrchestrationTrace para capturar datos de ModelInvocationInput y ModelInvocationOutput entre handoffs, e implementar chequeo de limites de parametros en el esquema de API de cada agente para las restricciones especificas de cada modelo",
        "CloudWatch Logs Insights para consultar y trazar el recorrido completo de la transaccion entre agentes, con una solucion de validacion custom en Lambda que normalice parametros entre los requisitos de cada FM",
    ],
    correct=2,
    key="off1-q46",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock tracing con OrchestrationTrace (ModelInvocationInput/Output) + chequeo de limites de parametros en el esquema.</div>'
        '<p><b>El problema:</b> saber <b>donde</b> falla la validacion de parametros entre handoffs de agentes con distintos FMs y dar validacion consistente. OrchestrationTrace captura el detalle de entrada y salida de cada invocacion de modelo.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>OrchestrationTrace</b> de Bedrock captura datos detallados de <b>ModelInvocationInput</b> y <b>ModelInvocationOutput</b> entre handoffs, dando visibilidad exacta de donde y por que fallan los parametros. El <b>chequeo de limites de parametros</b> en el esquema de API de cada agente asegura validacion consistente entre FMs con requisitos distintos (precision, tipos).</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>EventBridge + Step Functions:</b> crea un sistema de validacion aparte del framework de agentes, con cambios de arquitectura grandes, y no identifica directamente donde fallan las validaciones en el flujo actual.</li>'
        '<li><b>CloudWatch Logs + correlation IDs:</b> ayuda a rastrear transacciones, pero captura informacion despues del evento y no identifica los problemas de validacion de parametros entre FMs ni los previene.</li>'
        '<li><b>CloudWatch Logs Insights + Lambda:</b> consulta logs entre servicios, pero no captura el detalle de la invocacion del modelo necesario para diagnosticar donde falla la validacion durante la orquestacion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Diagnosticar donde fallan los parametros entre agentes = habilitar el tracing de orquestacion, que captura el detalle de entrada y salida de cada invocacion del modelo por handoff. Los logs de CloudWatch analizan despues del evento; no dan ese detalle por handoff.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents-trace.html">docs.aws trazas de agentes de Bedrock</a></div>'
    ),
))

# ============================================================
# Q47 - Guardrails + SCP enforce + StackSets multi-account
# ============================================================
cards.append(card(
    question="Una empresa de salud implementa FMs de Amazon Bedrock en <b>varias cuentas</b> de una organizacion de AWS Organizations. Quiere asistentes de chat que cumplan privacidad, <b>impedir que expongan PII</b>, aplicar <b>guardrails de seguridad de forma consistente</b> en todas las implementaciones y tener <b>gobierno centralizado</b> permitiendo a cada departamento personalizar parametros del modelo. &iquest;Que solucion cumple?",
    options=[
        "Un knowledge base de Bedrock con fuentes custom por departamento, VPC endpoints para todo el trafico de FMs y AWS WAF para inspeccionar y filtrar prompts y respuestas con contenido sensible",
        "Configurar Bedrock Guardrails con filtros de informacion sensible y de contenido, SCPs que obliguen el uso de los guardrails y CloudFormation StackSets para desplegar guardrails consistentes en todas las cuentas de la organizacion",
        "Roles IAM y permisos de Bedrock en cada cuenta, codigo custom para filtrar PII en cada asistente y alarmas de CloudWatch para monitorear PII en las respuestas",
        "Bedrock Guardrails con filtros de informacion sensible, permissions boundaries de IAM para el acceso a los FMs, una version de guardrail por departamento y distribuirlas con la replicacion cross-Region de guardrails",
    ],
    correct=1,
    key="off1-q47",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails (info sensible + contenido) + SCPs que obligan su uso + StackSets multi-cuenta.</div>'
        '<p><b>El problema:</b> gobierno centralizado y consistente entre cuentas (obligar guardrails, enmascarar PII) permitiendo personalizar parametros por departamento. Las SCPs imponen politicas a nivel de organizacion; StackSets despliega recursos en muchas cuentas.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> detecta y enmascara PII en prompts y respuestas. Las <b>SCPs</b> obligan el uso del guardrail a nivel de organizacion (proteccion consistente en todas las cuentas). <b>CloudFormation StackSets</b> despliega guardrails estandarizados en todas las cuentas y a la vez cada departamento personaliza los parametros del FM. Cubre gobierno centralizado y flexibilidad.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Knowledge base + VPC endpoints + WAF:</b> el KB no filtra PII de las respuestas del FM, los VPC endpoints protegen la red y WAF protege apps web; WAF no filtra contenido generado por el LLM ni enmascara PII, y falta el gobierno centralizado.</li>'
        '<li><b>IAM + codigo custom por cuenta:</b> filtrar PII con codigo en cada app no da gobierno centralizado, genera inconsistencia entre cuentas, y las alarmas de CloudWatch monitorean pero no imponen guardrails.</li>'
        '<li><b>Guardrails + permissions boundaries + replicacion cross-Region:</b> los permissions boundaries limitan permisos, no obligan el uso del guardrail; y la replicacion cross-Region distribuye entre Regiones (rendimiento), no entre cuentas para gobierno de toda la organizacion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Gobierno consistente entre muchas cuentas = barandas + politicas de control de servicio que obligan su uso + despliegue de stacks en toda la organizacion. Los permissions boundaries limitan, no obligan; la replicacion de barandas es cross-Region, no cross-account.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html">docs.aws SCPs en Organizations</a></div>'
    ),
))

# ============================================================
# Q48 - Step Functions ApplyGuardrail pre/post + IAM condition
# ============================================================
cards.append(card(
    question="Una empresa de mensajeria social crea un asistente con Amazon Bedrock y necesita que <b>cada inferencia cumpla una politica de seguridad aprobada</b>: <b>bloquear prompts da&ntilde;inos antes de invocar</b> el modelo, <b>filtrar la salida en streaming en tiempo real</b> y <b>enviar casos marcados a revision humana</b>. &iquest;Que solucion cumple?",
    options=[
        "Un flujo de Step Functions con un paso que llame ApplyGuardrail antes de la inferencia, luego InvokeModel sin streaming con el guardrail adjunto, guardar el resultado completo en S3 y ocultar los tokens problematicos en la interfaz del cliente despues de que el modelo termina de generar",
        "Un flujo de Step Functions con pre y post-chequeos usando ApplyGuardrail e InvokeModelWithResponseStream, con el guardrail adjunto, y controles de proceso como code reviews en vez de aplicacion por IAM para asegurar que siempre se usen los guardrails en cada peticion",
        "Un flujo de Step Functions con una Lambda que pre-chequee entradas con ApplyGuardrail, un paso InvokeModelWithResponseStream con el guardrail adjunto, una segunda Lambda que post-chequee salidas con ApplyGuardrail, enrutar lo marcado a una cola SQS y forzar el uso del guardrail con una condicion IAM bedrock:GuardrailIdentifier",
        "Un flujo de Step Functions con InvokeModelWithResponseStream con el guardrail adjunto para el filtrado en stream y una Lambda de post-chequeo con ApplyGuardrail para revisar los casos marcados, sin realizar ninguna validacion de pre-inferencia sobre los prompts entrantes",
    ],
    correct=2,
    key="off1-q48",
    answer=(
        '<div class="verdict">Correcta: {{L}} - ApplyGuardrail pre y post + InvokeModelWithResponseStream con guardrail + SQS para revision + condicion IAM bedrock:GuardrailIdentifier.</div>'
        '<p><b>El problema:</b> garantizar en TODA inferencia: bloqueo previo del prompt, filtrado en stream en tiempo real y ruteo a revision humana. La ApplyGuardrail API valida contenido sin invocar el modelo.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>ApplyGuardrail</b> pre-inferencia bloquea prompts da&ntilde;inos antes de invocar; <b>InvokeModelWithResponseStream con el guardrail adjunto</b> filtra la salida en el stream en tiempo real; una Lambda de post-chequeo con ApplyGuardrail enruta lo marcado a <b>SQS</b> para revision humana; y la condicion IAM <b>bedrock:GuardrailIdentifier</b> obliga el uso del guardrail en todas las peticiones (garantiza que ninguna inferencia lo evada).</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>InvokeModel sin streaming + ocultar en UI:</b> sin streaming no filtra la salida en tiempo real; depende de enmascarar en el cliente despues de terminar; incumple el filtrado en stream.</li>'
        '<li><b>Pre/post con code reviews en vez de IAM:</b> sin la condicion IAM bedrock:GuardrailIdentifier, un llamador podria evadir el guardrail; no garantiza que cada inferencia cumpla la politica.</li>'
        '<li><b>Sin pre-inferencia:</b> sin validacion previa, los prompts da&ntilde;inos llegan al modelo antes de bloquearse; el requisito exige bloquearlos antes de invocar.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Bloquear antes + filtrar el stream en tiempo real + revision humana + garantizar SIEMPRE = validar la baranda antes de invocar, invocar con respuesta en stream con la baranda adjunta, encolar lo marcado para revision y forzar su uso con una condicion IAM (los code reviews no lo garantizan).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html">docs.aws ApplyGuardrail API</a></div>'
    ),
))

# ============================================================
# Q49 - promptSessionAttributes sin retencion + handoff cifrado
# ============================================================
cards.append(card(
    question="Una empresa financiera usa Bedrock AgentCore para un asistente de soporte que debe manejar hasta 25.000 sesiones concurrentes con sub-500 ms, <b>transferir contexto de forma segura a agentes humanos</b>, desplegarse en varias Regiones y <b>recordar preferencias dentro de una conversacion</b>, pero con una politica que <b>prohibe retener el contexto mas alla de una sola sesion</b>. &iquest;Que solucion cumple?",
    options=[
        "Mantener el historial en memoria de la aplicacion y pasar el historial acumulado en cada InvokeAgent incluyendolo en el campo promptSessionAttributes del parametro sessionState, con un session ID unico por interaccion, limpiar la memoria al terminar la sesion y cifrar los session attributes para transferir el contexto al humano",
        "Un agente de AgentCore que invoque una Lambda para guardar el historial en DynamoDB, recuperar el contexto en cada InvokeAgent, un TTL en DynamoDB para borrar tras la sesion, cifrado en DynamoDB y optimizar Lambda y DynamoDB para alta concurrencia y baja latencia",
        "Amazon ElastiCache (Redis OSS) para retener estados con claves por sesion, incluir el historial cacheado en el prompt de cada peticion, cifrado nativo de Redis para transferir contexto y un mecanismo para limpiar el cache al terminar la sesion",
        "AgentCore con session attributes para guardar el historial, DynamoDB Streams para capturar cambios en tiempo real y una Lambda disparada por Streams que archive el historial en S3 para auditoria y luego borre los registros de sesion",
    ],
    correct=0,
    key="off1-q49",
    answer=(
        '<div class="verdict">Correcta: {{L}} - historial en memoria pasado via promptSessionAttributes (sessionState) + session ID unico + limpiar al terminar + cifrado para el handoff.</div>'
        '<p><b>El problema:</b> recordar el contexto <b>dentro</b> de una sesion sin <b>retenerlo</b> despues, con altisima concurrencia, baja latencia y handoff seguro. sessionState/promptSessionAttributes de InvokeAgent lleva el historial con cada peticion sin persistirlo.</p>'
        '<p><b>Por que la respuesta sirve:</b> mantener el historial en memoria y pasarlo en el campo <b>promptSessionAttributes</b> de <b>sessionState</b> en cada InvokeAgent, con un <b>session ID unico</b>, recuerda las preferencias dentro de la sesion sin infraestructura extra (soporta 25.000 concurrentes y sub-500 ms). Al <b>limpiar la memoria</b> al terminar se cumple la politica de no retencion, y cifrar los session attributes permite el <b>handoff seguro</b> al humano.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Lambda + DynamoDB con TTL:</b> guardar y recuperar de DynamoDB por Lambda agrega complejidad y latencia por encima del sub-500 ms frente al parametro nativo promptSessionAttributes.</li>'
        '<li><b>ElastiCache Redis:</b> retener estados en Redis agrega infraestructura y operacion (clusters, gestion de cache, limpieza) innecesarias frente al enfoque en memoria con sessionState.</li>'
        '<li><b>Session attributes + DynamoDB Streams a S3:</b> archivar a S3 retiene el contexto mas alla de la sesion, violando la politica de retencion, y suma DynamoDB, Streams, Lambda y S3.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Contexto SOLO dentro de la sesion, sin retener, con baja latencia = historial en memoria pasado en los atributos de sesion de la peticion al agente, limpiado al cerrar. Persistir en una base o cache agrega latencia u overhead, y archivar viola la no-retencion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents-session-state.html">docs.aws sessionState de agentes de Bedrock</a></div>'
    ),
))

# ============================================================
# Q50 - Contextual grounding: reference dataset + Guardrails + Evaluations
# ============================================================
cards.append(card(
    question="Una empresa de salud implementa un knowledge base clinico en Amazon Bedrock. En pruebas, el modelo a veces <b>fabrica recomendaciones de tratamiento</b> que no vienen de las guias clinicas aprobadas. Hay que <b>detectar las alucinaciones antes de publicar</b>, analizando las respuestas contra <b>informacion medica verificada</b> e identificando <b>inconsistencias semanticas</b> cuando preguntan lo mismo de formas distintas. &iquest;Que solucion cumple?",
    options=[
        "Un monitoreo en tiempo real con CloudWatch Logs Insights que analice patrones y marque inexactitudes por palabras clave predefinidas, y Lambda que comparen respuestas con respuestas conocidas en una tabla DynamoDB",
        "Bedrock Guardrails con reglas custom para detectar y bloquear contenido potencialmente alucinado identificando patrones especificos, y SageMaker Feature Store para mantener un repositorio de guias clinicas verificadas",
        "Un automatic model evaluation job de Bedrock con un dataset de prompts custom, alarmas de deteccion de anomalias para inexactitudes y notificaciones por Amazon SNS cuando se detecten",
        "Crear un dataset de referencia con pares pregunta-respuesta validados de las guias clinicas, hacer output diffing con Bedrock Guardrails para analizar la consistencia de la respuesta y usar Bedrock evaluations para detectar inexactitudes",
    ],
    correct=3,
    key="off1-q50",
    answer=(
        '<div class="verdict">Correcta: {{L}} - dataset de referencia + Guardrails (contextual grounding) + Bedrock evaluations.</div>'
        '<p><b>El problema:</b> detectar alucinaciones (recomendaciones fabricadas) contrastando la respuesta con informacion verificada y captando inconsistencias entre preguntas parafraseadas. El contextual grounding de Guardrails verifica que la respuesta este anclada en fuentes aprobadas.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>dataset de referencia</b> con pares pregunta-respuesta validados de las guias sirve de verdad de base. Los <b>contextual grounding checks</b> de Guardrails detectan alucinaciones verificando que la respuesta este anclada en esas fuentes aprobadas (exactitud factual). <b>Bedrock evaluations</b> con datasets de prompts custom evalua el desempe&ntilde;o e identifica inconsistencias entre prompts redactados de forma distinta.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CloudWatch Logs Insights + Lambda vs DynamoDB:</b> Logs Insights hace coincidencia por patrones/palabras clave y Lambda solo compara strings exactos; sin entendimiento semantico no detecta alucinaciones cuando preguntan lo mismo de otra forma.</li>'
        '<li><b>Guardrails + SageMaker Feature Store:</b> Guardrails ayuda, pero Feature Store almacena y sirve features de ML para entrenamiento/inferencia; no mantiene guias clinicas validadas ni hace el analisis semantico requerido.</li>'
        '<li><b>Automatic model evaluation job + SNS:</b> el evaluation job da evaluacion offline del desempe&ntilde;o, pero no hace los contextual grounding checks para detectar alucinaciones contra informacion verificada.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Detectar alucinaciones contra una fuente de verdad = Guardrails contextual grounding checks + un dataset de referencia; sumar Bedrock evaluations capta inconsistencias entre preguntas parafraseadas. La coincidencia por palabras clave o strings exactos no entiende semantica.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html">docs.aws Guardrails contextual grounding</a></div>'
    ),
))



# ============================================================
# Q51 - Strands en AgentCore Runtime + Gateway MCP tools
# ============================================================
cards.append(card(
    question="Una empresa hace una PoC con Amazon Bedrock para agilizar soporte al cliente. Tiene 10.000 tickets historicos con resoluciones y 500 archivos de documentacion de producto que la app debe referenciar. La app debe responder con baja latencia, mantener la <b>privacidad de datos</b>, <b>reducir el tiempo de resolucion</b> (ejecutando acciones) frente al proceso manual y monitorear precision y rendimiento <b>en tiempo real</b>. &iquest;Que solucion cumple?",
    options=[
        "Un knowledge base de Bedrock con la documentacion de producto y los tickets historicos conectado a un FM de alto rendimiento para responder consultas, con metricas custom de CloudWatch para el monitoreo de precision y rendimiento en tiempo real",
        "Un ensemble multi-modelo con varios FMs de Bedrock y consenso por votacion para generar cada respuesta, usando las metricas integradas de Bedrock para el seguimiento de throughput y uso, y DynamoDB para el estado de las conversaciones",
        "Desplegar un agente de Strands en AgentCore Runtime con un knowledge base (documentacion y tickets), AgentCore Gateway para exponer las operaciones de gestion de tickets como herramientas MCP que ejecutan acciones, y AgentCore Observability con CloudWatch para medir resolucion y precision",
        "El FM por defecto de Bedrock con una plantilla de prompt custom para procesar las consultas, CloudWatch para las metricas de invocacion del modelo y un dashboard para monitorear el tiempo de respuesta y el throughput de la aplicacion",
    ],
    correct=2,
    key="off1-q51",
    answer=(
        '<div class="verdict">Correcta: {{L}} - agente Strands en AgentCore Runtime + KB (docs + tickets) + AgentCore Gateway (MCP tools) + Observability.</div>'
        '<p><b>El problema:</b> ademas de recuperar informacion (RAG), hay que <b>ejecutar acciones</b> de resolucion (actualizar tickets, iniciar procesos) para reducir el tiempo de resolucion, con privacidad y monitoreo en tiempo real.</p>'
        '<p><b>Por que la respuesta sirve:</b> un agente de <b>Strands</b> en <b>AgentCore Runtime</b> aporta orquestacion, razonamiento y <b>ejecucion de acciones</b>. El <b>knowledge base</b> (docs + tickets) da RAG manteniendo privacidad. <b>AgentCore Gateway</b> convierte las APIs de tickets en herramientas MCP para las acciones de resolucion, y <b>AgentCore Observability</b> con CloudWatch monitorea precision y rendimiento en tiempo real.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>KB + FM de alto rendimiento:</b> solo recupera de la documentacion; no ejecuta acciones estructuradas (actualizar tickets, iniciar procesos), asi que no reduce el tiempo de resolucion.</li>'
        '<li><b>Ensemble multi-modelo con votacion:</b> invocar varios FMs y post-procesar el consenso genera mucha latencia, incumpliendo la respuesta rapida.</li>'
        '<li><b>FM por defecto + prompt template:</b> carece de RAG para referenciar los 500 documentos y 10.000 tickets; sin knowledge base no accede a la informacion necesaria.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Si ademas de responder hay que EJECUTAR acciones (tools) para resolver, piensa en un agente + herramientas (exponer las operaciones como herramientas para el agente), no solo una base de conocimiento. Un ensemble con votacion agrega latencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html">docs.aws Bedrock AgentCore</a></div>'
    ),
))

# ============================================================
# Q52 - Prompt Management A/B + Evaluations LLM-judge + flow en CI/CD
# ============================================================
cards.append(card(
    question="Una empresa financiera necesita un workflow <b>zero-touch</b> que promueva actualizaciones de prompt de dev a prod solo si mejoran la precision en <b>los 5 idiomas</b>, muestran <b>menor varianza</b> entre consultas similares y <b>pasan checks de cumplimiento regulatorio</b>. Debe correr en el <b>CI/CD existente</b>, comparar versiones de prompt, generar reportes auditables y ser costo-efectivo. &iquest;Que solucion cumple?",
    options=[
        "Usar SageMaker Canvas para comparar visualmente las salidas, un dashboard de metricas, exportar hallazgos a un sistema de colaboracion documental para revisar cumplimiento y reuniones semanales entre prompt engineers y compliance",
        "Usar Bedrock Prompt Management para control de versiones y A/B testing de prompts, Bedrock Evaluations con jueces basados en LLM para evaluaciones automaticas de precision y consistencia, un flow de Bedrock para estandarizar las pruebas entre idiomas e integrarlo con el CI/CD existente",
        "Control de versiones con object versions de S3, Lambda que puntuen respuestas manualmente, metricas en DynamoDB y un dashboard custom en QuickSight para precision por idioma y tipo de producto",
        "Un framework de evaluacion custom con AWS Amplify de frontend y Lambda de backend, votacion crowdsourced del equipo sobre la calidad y Amazon Comprehend para analizar sentimiento y consistencia entre idiomas",
    ],
    correct=1,
    key="off1-q52",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Prompt Management (versiones + A/B) + Bedrock Evaluations con jueces LLM + flow integrado al CI/CD.</div>'
        '<p><b>El problema:</b> promocion automatica (zero-touch) de prompts que exige comparar versiones, evaluar precision y varianza en 5 idiomas, pasar cumplimiento, y reportes auditables dentro del CI/CD.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Prompt Management</b> da control de versiones, A/B testing y trazabilidad (lineage) de prompts. <b>Bedrock Evaluations</b> con <b>jueces basados en LLM</b> evalua de forma automatica y escalable la precision y la varianza en los cinco idiomas sin intervencion manual. Un <b>flow de Bedrock</b> integra todo en el CI/CD, habilitando la promocion zero-touch, la comparacion de versiones y los reportes auditables, de forma costo-efectiva.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SageMaker Canvas + reuniones semanales:</b> Canvas es no-code para modelos predictivos, no para workflows de evaluacion de prompts; y las reuniones manuales no cumplen el zero-touch.</li>'
        '<li><b>S3 object versions + Lambda + QuickSight:</b> el versionado de S3 no da comparacion lado a lado, A/B ni pipelines de evaluacion integrados; puntuar con Lambda no escala a 5 idiomas y el dashboard custom suma overhead sin evaluacion automatica auditable.</li>'
        '<li><b>Amplify + Lambda + votacion crowdsourced + Comprehend:</b> mucho desarrollo y mantenimiento; la votacion no da evaluaciones automaticas y auditables para cumplimiento, y Comprehend hace sentimiento/entidades, no evalua correccion factual ni reduccion de varianza.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Promocion automatica de prompts con versiones, A/B y evaluacion multi-idioma sin humanos = la gestion de prompts nativa + la evaluacion automatizada con jueces basados en modelos + un flow integrado en la tuberia de despliegue. Canvas es para modelos predictivos; Comprehend no evalua correccion factual.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
    ),
))

# ============================================================
# Q53 - CloudWatch/S3 logs + parameterized prompts versioning approval
# ============================================================
cards.append(card(
    question="Una empresa de salud global despliega GenAI en Amazon Bedrock para recomendaciones de tratamiento. Las regulaciones varian: algunos paises exigen <b>retener inputs y outputs 2 a&ntilde;os</b>, otros solo enviar datos a auditorias locales. Se requiere <b>terminologia medica consistente</b> pero recomendaciones que se <b>adapten a la demografia local</b>, integrar con EHR, soportar 10.000 consultas/dia sub-segundo, <b>revisar y aprobar cambios de prompt</b> antes de desplegar y <b>logs completos</b> de prompts, respuestas y contexto. &iquest;Que solucion cumple?",
    options=[
        "AWS CloudTrail para registrar llamadas de API, prompts estandar en Bedrock Prompt Management con variables para demografia y politicas IAM para restringir el acceso a los prompts",
        "Funciones Lambda que generen los prompts dinamicamente para imponer el lenguaje clinico consistente, CloudWatch Logs para registrar las invocaciones del modelo y colas SQS para implementar el flujo de aprobacion de los cambios de prompt",
        "Guardar las plantillas de prompt en S3 con S3 Object Lock para el control de versiones, EventBridge para rastrear las invocaciones del modelo y AWS Config para monitorear los cambios en las plantillas de prompt entre entornos",
        "Usar CloudWatch Logs para logs detallados de invocacion del modelo, guardarlos en S3, crear prompts parametrizados en Bedrock Prompt Management con variables para opciones de tratamiento, y habilitar versionado de prompts con un flujo de aprobacion",
    ],
    correct=3,
    key="off1-q53",
    answer=(
        '<div class="verdict">Correcta: {{L}} - CloudWatch Logs de invocacion en S3 + prompts parametrizados en Prompt Management con versionado y aprobacion.</div>'
        '<p><b>El problema:</b> logs completos (prompts, respuestas, contexto) para retencion/auditoria por region, prompts que sean consistentes pero adaptables por demografia, y aprobacion de cambios antes de desplegar.</p>'
        '<p><b>Por que la respuesta sirve:</b> exportar los <b>model invocation logs de CloudWatch a S3</b> da logging completo (prompts, inputs, outputs, metadatos de usuario) que cumple la retencion multi-region. <b>Prompt Management</b> con <b>prompts parametrizados</b> mantiene terminologia consistente y adapta el tratamiento a la demografia local via variables, y su <b>versionado con flujo de aprobacion</b> permite revisar y aprobar cambios (gobierno clinico).</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CloudTrail + prompts + IAM:</b> CloudTrail registra quien invoco (eventos de gestion), no el contenido de prompts, inputs, outputs ni contexto de usuario que exige la auditoria clinica.</li>'
        '<li><b>Lambda dinamica + SQS de aprobacion:</b> generar prompts con Lambda agrega overhead y latencia (arriesga el sub-segundo a 10.000/dia), y SQS no es un flujo de aprobacion (exigiria desarrollo), mientras Prompt Management lo trae nativo.</li>'
        '<li><b>S3 + Object Lock + EventBridge + Config:</b> Object Lock no da parametrizacion para terminologia consistente adaptable; EventBridge rastrea cambios de estado de jobs, no es logging de invocaciones, y falta el logging detallado de inputs/outputs/contexto.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Auditoria de contenido (prompts/respuestas/contexto) = model invocation logs (CloudWatch a S3), no CloudTrail. Prompts consistentes pero adaptables + aprobacion de cambios = Prompt Management (parametrizados + versionado/aprobacion).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html">docs.aws model invocation logging</a></div>'
    ),
))

# ============================================================
# Q54 - Comprehend parallel async: toxicity + prompt safety + PII sin redaccion
# ============================================================
cards.append(card(
    question="Una plataforma de comunicacion usa un FM de Amazon Bedrock que resume mensajes y genera borradores. Se quiere <b>filtrado de contenido en capas con Amazon Comprehend</b> que evite contenido ofensivo, proteja la privacidad y detecte <b>solicitudes de consejo inapropiado</b> (practicas no eticas, actividades da&ntilde;inas, manipulacion). Todos los filtros de preprocesamiento deben <b>terminar antes</b> de llegar al FM manteniendo tiempos de respuesta aceptables. &iquest;Que solucion cumple?",
    options=[
        "Usar custom classification para construir un FM que detecte contenido ofensivo y consejo inapropiado, y aplicar deteccion de PII como filtro secundario solo cuando los mensajes pasen el clasificador",
        "Un proceso multi-etapa que use primero prompt safety classification, luego toxicity detection solo sobre los prompts seguros y por ultimo deteccion de PII, enrutando lo marcado a revision humana via EventBridge",
        "Toxicity detection con umbrales de 0.5 en todas las categorias, procesamiento paralelo de prompt safety classification y deteccion de PII con redaccion de entidades, y alarmas de CloudWatch para filtrar metricas",
        "Procesamiento paralelo con llamadas API asincronas: toxicity detection para contenido ofensivo, prompt safety classification para el consejo inapropiado y deteccion de PII sin redaccion",
    ],
    correct=3,
    key="off1-q54",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Comprehend en paralelo (async): toxicity + prompt safety classification + deteccion de PII sin redaccion.</div>'
        '<p><b>El problema:</b> tres filtros (ofensivo, privacidad, consejo inapropiado) que deben terminar antes del FM sin degradar la latencia. Correr en paralelo hace que el tiempo total sea el del filtro mas lento, no la suma.</p>'
        '<p><b>Por que la respuesta sirve:</b> Comprehend ofrece los tres controles en tiempo real: <b>toxicity detection</b> (ofensivo), <b>prompt safety classification</b> (consejo inapropiado: no etico, da&ntilde;ino, manipulador) y <b>deteccion de PII</b> (privacidad). Ejecutarlos <b>en paralelo</b> deja el tiempo total en el del filtro mas lento (mantiene la latencia). Detectar PII <b>sin redaccion</b> (DetectPiiEntities) marca la exposicion pero conserva el contexto y evita la latencia de los jobs asincronos de redaccion.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Custom classification para "construir un FM":</b> custom classification entrena un clasificador de texto, no un FM, y exige entrenamiento/mantenimiento innecesario; ademas correr PII solo tras el clasificador crea dependencia secuencial que sube la latencia.</li>'
        '<li><b>Multi-etapa estrictamente secuencial:</b> acumula la latencia de cada llamada (no mantiene tiempos aceptables) y correr toxicity solo sobre lo que pasa prompt safety deja pasar contenido ofensivo en los mensajes marcados.</li>'
        '<li><b>Toxicity 0.5 + PII con redaccion + alarmas CloudWatch:</b> la redaccion de PII via jobs asincronos batch introduce retrasos (no termina antes del FM en tiempo aceptable), y CloudWatch monitorea metricas, no filtra el contenido del mensaje.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Varios filtros antes del FM sin matar la latencia = ejecutarlos EN PARALELO (el tiempo es el del mas lento). PII sin redaccion (DetectPiiEntities) evita el retraso de los jobs de redaccion batch; secuencial acumula latencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/trust-safety.html">docs.aws Comprehend trust and safety</a></div>'
    ),
))

# ============================================================
# Q55 - EventBridge Lambda keep-warm ModelNotReadyException
# ============================================================
cards.append(card(
    question="Una empresa financiera importo un modelo custom a Amazon Bedrock (Custom Model Import) para analisis de transacciones en tiempo real. En horas pico, tras periodos de baja actividad, los usuarios reciben errores <b>ModelNotReadyException</b>. Se necesita mantener el modelo disponible en pico <b>minimizando llamadas innecesarias y costo</b>, prevenir el <b>eviction</b> del modelo y recuperarse bien cuando ocurra, y minimizar costo fuera de pico. &iquest;Que solucion cumple?",
    options=[
        "Una Lambda que invoque el modelo cada minuto durante las horas pico para mantenerlo caliente, con reintentos sincronos ante fallos y CloudWatch para monitorear el estado del modelo importado",
        "Una Lambda de pre-warming invocada 15 minutos antes de cada pico para calentar el modelo, con reintentos de backoff lineal ante fallos y health checks sincronos cada 5 minutos",
        "Un pipeline de warm-up con Step Functions que mantenga actividad constante del modelo en pico, con rutas de ejecucion paralelas para redundancia y failover automatico",
        "Configurar Amazon EventBridge para invocar una Lambda cada 45 minutos que invoque el modelo, con reintentos de backoff exponencial para las llamadas de API y CloudWatch Logs para analizar patrones de disponibilidad",
    ],
    correct=3,
    key="off1-q55",
    answer=(
        '<div class="verdict">Correcta: {{L}} - EventBridge que invoca una Lambda cada 45 min (keep-warm) + backoff exponencial + CloudWatch Logs.</div>'
        '<p><b>El problema:</b> los modelos importados se <b>evictan</b> (descargan) tras inactividad y al reaccederse tardan en restaurarse (ModelNotReadyException). Hay que mantenerlo caliente en pico sin gastar de mas fuera de pico.</p>'
        '<p><b>Por que la respuesta sirve:</b> invocar el modelo periodicamente con <b>EventBridge Scheduler cada 45 min</b> evita el eviction manteniendo disponibilidad en pico y minimiza costo fuera de pico (intervalo equilibrado). El <b>backoff exponencial</b> (via Config de Boto3) es la practica recomendada para errores transitorios y ModelNotReadyException, y CloudWatch Logs analiza patrones de disponibilidad.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Invocar cada minuto:</b> es excesivamente frecuente y genera costo innecesario de llamadas fuera de pico; muy por encima de lo necesario para evitar el eviction.</li>'
        '<li><b>Pre-warm 15 min antes + backoff lineal:</b> 15 min es insuficiente ante inactividad mas larga (deja huecos con el modelo evictado), y el backoff lineal no es la practica recomendada (AWS recomienda exponencial con jitter).</li>'
        '<li><b>Step Functions con actividad constante:</b> mantener actividad constante no minimiza el costo fuera de pico, y las rutas paralelas agregan complejidad sin atacar el eviction/recuperacion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Modelo importado que se evicta por inactividad = keep-warm periodico (un scheduler de eventos a intervalo equilibrado, p.ej. 45 min) + reintentos con backoff exponencial. Cada minuto gasta de mas; 15 min o actividad constante no equilibran costo/disponibilidad.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html">docs.aws Custom Model Import</a></div>'
    ),
))

# ============================================================
# Q56 - CloudWatch metric filters + anomaly detection por tool
# ============================================================
cards.append(card(
    question="Una app de GenAI con FMs de Amazon Bedrock y varias integraciones de herramientas custom sufre <b>picos inesperados de consumo de tokens</b> pese a trafico constante. Se necesita, con el <b>model invocation logging</b> de Bedrock, monitorear InputTokenCount y OutputTokenCount, <b>detectar patrones inusuales por herramienta</b>, identificar que integracion causa el consumo anormal y <b>ajustar los umbrales automaticamente</b> al cambiar el trafico. &iquest;Que solucion cumple?",
    options=[
        "Guardar los logs de invocacion en S3, una Lambda que los procese en tiempo real y actualizar manualmente los umbrales de las alarmas de CloudWatch segun las tendencias que identifique la Lambda",
        "Usar CloudWatch Logs para capturar los logs, crear dashboards por InputTokenCount y OutputTokenCount y configurar alarmas estaticas de CloudWatch con umbrales fijos por integracion",
        "Guardar los logs en S3, catalogarlos con AWS Glue y analizar patrones con consultas programadas de Athena que generen reportes de tendencias de uso por herramienta",
        "Usar CloudWatch Logs para capturar los logs, crear metric filters de CloudWatch que extraigan patrones de invocacion por herramienta y aplicar alarmas de anomaly detection de CloudWatch que ajusten las baselines por cada metrica de herramienta",
    ],
    correct=3,
    key="off1-q56",
    answer=(
        '<div class="verdict">Correcta: {{L}} - CloudWatch metric filters por herramienta + alarmas de anomaly detection que ajustan baselines.</div>'
        '<p><b>El problema:</b> detectar anomalias de consumo de tokens por herramienta en tiempo real y que los umbrales se <b>ajusten solos</b> al cambiar el trafico. La anomaly detection de CloudWatch usa ML para mover la baseline automaticamente.</p>'
        '<p><b>Por que la respuesta sirve:</b> los <b>metric filters</b> de CloudWatch extraen de los logs los patrones de invocacion <b>por herramienta</b>, y las <b>alarmas de anomaly detection</b> usan ML para ajustar automaticamente las baselines de cada metrica segun patrones historicos (horarios, diarios, semanales), sin intervencion manual. Identifica que herramienta causa el consumo anormal sin servicios extra ni codigo custom.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>S3 + Lambda + umbrales manuales:</b> registra y procesa, pero exige actualizar los umbrales a mano; no cumple el ajuste automatico al evolucionar el trafico.</li>'
        '<li><b>Dashboards + alarmas estaticas:</b> los umbrales fijos no se ajustan solos cuando cambian los patrones; requeririan ajuste manual.</li>'
        '<li><b>S3 + Glue + Athena programado:</b> identifica tendencias, pero no da deteccion de anomalias en tiempo real; las consultas programadas no ajustan umbrales solas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Umbrales que se ajustan solos al cambiar el trafico = CloudWatch anomaly detection (baselines por ML). Alarmas estaticas o actualizacion manual no cumplen "automatico". Metric filters separan las metricas por herramienta.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html">docs.aws CloudWatch anomaly detection</a></div>'
    ),
))

# ============================================================
# Q57 - SQS + Fargate cascada de modelos por confianza
# ============================================================
cards.append(card(
    question="Una empresa de medios crea moderacion de contenido con Amazon Bedrock: primero un modelo peque&ntilde;o de baja latencia clasifica el texto, y las peticiones con <b>confianza menor a 0.65</b> escalan a un modelo mas grande y caro. Debe responder casi en tiempo real los casos de alta confianza, procesar los de baja confianza de forma <b>asincrona</b>, escalar ante picos, <b>invocar el modelo grande solo cuando haga falta</b> y usar componentes <b>desacoplados</b> para alta resiliencia. &iquest;Que solucion cumple?",
    options=[
        "Un flujo de Step Functions con ramas paralelas que ejecute el modelo peque&ntilde;o y el grande en cada peticion, eligiendo el resultado del grande cuando difieran las confianzas",
        "Desplegar ambos modelos en instancias EC2 con auto scaling habilitado y usar una heuristica de la aplicacion que enrute cada peticion al modelo adecuado segun la longitud de la frase y reglas de palabras clave",
        "Enviar las peticiones a una cola Amazon SQS, procesar los mensajes con AWS Fargate invocando primero el modelo peque&ntilde;o y, si la confianza es menor a 0.65, colocar la peticion en una segunda cola SQS para procesarla de forma asincrona con el modelo grande",
        "Usar Amazon API Gateway para invocar el modelo peque&ntilde;o de forma sincrona y, si la confianza es menor a 0.65, llamar sincronamente al modelo grande, con provisioned concurrency para los picos",
    ],
    correct=2,
    key="off1-q57",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SQS + Fargate en cascada por confianza (segunda cola para el modelo grande).</div>'
        '<p><b>El problema:</b> cascada por confianza (barato primero, caro solo si hace falta), con procesamiento asincrono de baja confianza, desacople para resiliencia y absorcion de picos.</p>'
        '<p><b>Por que la respuesta sirve:</b> las colas <b>SQS</b> desacoplan los componentes y absorben picos (buffer resiliente). <b>Fargate</b> procesa mensajes con paralelismo controlado: invoca primero el modelo peque&ntilde;o (respuesta casi en tiempo real) y escala solo las peticiones de <b>baja confianza a una segunda cola SQS</b> para procesarlas de forma asincrona con el modelo grande. Cumple costo, resiliencia y latencia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Step Functions con ramas paralelas para ambos modelos:</b> corre el modelo grande en CADA peticion, incumpliendo "invocar el grande solo cuando haga falta", y no es la arquitectura desacoplada por mensajes para picos.</li>'
        '<li><b>EC2 + heuristica por longitud/keywords:</b> exige gestionar infraestructura, el enrutamiento por heuristica es menos fiable que por confianza y no ofrece la arquitectura desacoplada por mensajes.</li>'
        '<li><b>API Gateway sincrono + provisioned concurrency:</b> las llamadas sincronas no desacoplan los componentes ni procesan la baja confianza de forma asincrona; menos resiliente ante picos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cascada de modelos (barato primero, caro solo si baja la confianza) + resiliencia y picos = arquitectura desacoplada por colas de mensajes + computo serverless de contenedores, con una segunda cola para el trabajo asincrono. Correr el grande siempre o de forma sincrona no optimiza costo ni desacopla.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html">docs.aws Amazon SQS</a></div>'
    ),
))



# ============================================================
# Q58 - Semantic chunking buffer 1 breakpoint 85%
# ============================================================
cards.append(card(
    question="Una farmaceutica tiene un RAG con un knowledge base de Bedrock sobre OpenSearch con mas de 25 millones de papers cientificos. Las respuestas son <b>inconsistentes y citan secciones irrelevantes</b> cuando las consultas cruzan metodologia, resultados y discusion. Hay que mejorar el KB para <b>preservar el contexto semantico entre parrafos relacionados</b> a escala de todo el corpus. &iquest;Que solucion cumple?",
    options=[
        "Configurar hierarchical chunking con chunks padre de 1000 tokens e hijos de 200 tokens y un solape de 50 tokens entre chunks",
        "Configurar semantic chunking con buffer size 1 y un breakpoint percentile threshold de 85% para determinar los limites de chunk segun el significado del contenido",
        "Configurar el KB sin chunking, dividir manualmente cada documento en archivos separados antes de la ingesta y aplicar reranking de post-procesamiento durante la recuperacion",
        "Configurar fixed-size chunking con tama&ntilde;o maximo de 300 tokens y 10% de solape entre chunks, usando un modelo de embeddings de Bedrock adecuado",
    ],
    correct=1,
    key="off1-q58",
    answer=(
        '<div class="verdict">Correcta: {{L}} - semantic chunking con buffer size 1 y breakpoint percentile 85%.</div>'
        '<p><b>El problema:</b> las consultas cruzan secciones (metodologia, resultados, discusion) y se citan pasajes adyacentes pero irrelevantes. Hay que trocear por <b>significado</b>, no por tama&ntilde;o fijo.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>semantic chunking</b> agrupa oraciones por similitud de significado e inserta un corte solo cuando hay un giro tematico real. Un <b>buffer size 1</b> embebe cada oracion con sus vecinas inmediatas (conserva el flujo local), y un <b>breakpoint percentile de 85%</b> solo separa el 15% de pares de oraciones menos similares, produciendo chunks mas coherentes. Es especialmente eficaz cuando las consultas cruzan varias secciones y reduce las citas fuera de tema.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Hierarchical chunking (padre 1000 / hijo 200):</b> al recuperar un hijo se puede subir a su padre para dar contexto amplio, pero ese padre puede abarcar metodologia y discusion a la vez, aumentando la chance de citar pasajes adyacentes irrelevantes.</li>'
        '<li><b>Sin chunking + dividir a mano:</b> con 25M de documentos es ineficiente y exige mucho preprocesamiento manual; los trozos quedan con demasiada informacion o rompen relaciones semanticas, y el reranking no arregla la causa de fondo.</li>'
        '<li><b>Fixed-size 300 tokens con 10% de solape:</b> el tama&ntilde;o fijo rompe limites semanticos naturales y no preserva el contexto entre parrafos relacionados; no resuelve las citas irrelevantes.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Consultas que cruzan secciones y citan pasajes adyacentes irrelevantes = semantic chunking (corta por giro tematico real; buffer conserva contexto local). El hierarchical puede subir a un padre demasiado amplio; fixed-size rompe la semantica.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws chunking en Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q59 - API Gateway HTTP API + Lambda streaming + token limits + retry
# ============================================================
cards.append(card(
    question="Se dise&ntilde;a una API para una app de GenAI con un FM en un servicio gestionado. La API debe <b>hacer streaming de respuestas</b> para reducir latencia, <b>imponer limites de tokens</b> para controlar el computo e implementar <b>logica de reintentos</b> para timeouts y respuestas parciales del modelo. &iquest;Que solucion cumple con el <b>MENOR esfuerzo operativo</b>?",
    options=[
        "Integrar un HTTP API de Amazon API Gateway con una Lambda que invoque Bedrock, usar Lambda response streaming, imponer los limites de tokens en la Lambda e implementar reintentos con las configuraciones de timeout de Lambda y API Gateway",
        "Conectar un HTTP API de API Gateway directo a Bedrock, simular streaming con polling del cliente, imponer los limites de tokens en el frontend y configurar reintentos con los ajustes de integracion de API Gateway",
        "Conectar un WebSocket API de API Gateway a un servicio de Amazon ECS con un servidor de inferencia en contenedor, hacer streaming por WebSocket, imponer limites de tokens en ECS y manejar timeouts con lifecycle hooks y restart policies de tareas ECS",
        "Integrar un REST API de API Gateway con una Lambda que invoque Bedrock, usar Lambda response streaming, imponer los limites de tokens en la Lambda e implementar reintentos con las configuraciones de timeout de Lambda y API Gateway",
    ],
    correct=0,
    key="off1-q59",
    answer=(
        '<div class="verdict">Correcta: {{L}} - HTTP API de API Gateway + Lambda con response streaming + limites de tokens en Lambda + reintentos.</div>'
        '<p><b>El problema:</b> streaming token a token, limites de tokens y reintentos, con el minimo overhead. Clave: que tipo de API de Gateway soporta el streaming de Lambda.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>HTTP API</b> puede usar integracion proxy con una Lambda function URL configurada para streaming, entregando tokens en tiempo real (menor latencia). Los <b>limites de tokens</b> se imponen en la Lambda antes de invocar Bedrock, y la <b>logica de reintentos</b> para timeouts se implementa en la Lambda. Cubre todo con el minimo overhead.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>HTTP API directo + polling del cliente:</b> el polling no es streaming (agrega latencia y peticiones repetidas), imponer tokens en el frontend no controla el computo en la capa de invocacion, y los ajustes de integracion dan control de reintento limitado.</li>'
        '<li><b>WebSocket API + ECS en contenedor:</b> mucho overhead operativo (gestionar contenedores, conexiones WebSocket, escalado, ciclo de vida de tareas), y los restart policies actuan a nivel de tarea, no de peticion; no manejan bien timeouts ni respuestas parciales de una inferencia.</li>'
        '<li><b>REST API + Lambda streaming:</b> los REST API de API Gateway no soportan Lambda response streaming, asi que no entregan tokens en tiempo real.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Streaming de Lambda detras de API Gateway = HTTP API (no REST API, que no soporta response streaming). Imponer limites de tokens y reintentos en la Lambda, no en el frontend.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/lambda/latest/dg/configuration-response-streaming.html">docs.aws Lambda response streaming</a></div>'
    ),
))

# ============================================================
# Q60 - Step Functions: Bedrock evals + Synthetics canaries + rollback nightly
# ============================================================
cards.append(card(
    question="Una empresa actualiza un asistente basado en Amazon Bedrock cada sprint y necesita validacion de despliegue automatizada: validacion prerelease y control automatico de releases, monitoreo continuo post-deploy, alarmas y <b>rollback automatico</b>, <b>replay de workflows sinteticos</b> por intent, evaluaciones especificas de IA contra la baseline de produccion (tasa de alucinacion, drift semantico) y chequeos de consistencia con un set de prompts de referencia. Un stage pre-deploy de CodePipeline llama a un flujo de Step Functions. &iquest;Que configuracion cumple?",
    options=[
        "Correr solo canaries de CloudWatch Synthetics y chequeos de consistencia, con rollback automatico ante fallos, en corridas horarias sin evaluaciones de modelo",
        "Correr Bedrock model evaluations y canaries de Synthetics, con aprobacion automatica en exito, en corridas post-deploy con alarmas y seguimiento de metricas de rendimiento",
        "Correr Bedrock model evaluations y chequeos de consistencia, con aprobacion manual, en corridas semanales sin alarmas",
        "Correr Bedrock model evaluations y canaries de Synthetics, chequeos de consistencia basados en embeddings, aprobacion o rollback automatico, en corridas nocturnas con alarmas de CloudWatch",
    ],
    correct=3,
    key="off1-q60",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock evaluations + Synthetics canaries + chequeos por embeddings + aprobacion/rollback automatico + corridas nocturnas con alarmas.</div>'
        '<p><b>El problema:</b> combinar evaluaciones especificas de IA (alucinacion, drift), replay de workflows por intent, chequeos de consistencia contra prompts de referencia, y control automatico de release con rollback y monitoreo continuo.</p>'
        '<p><b>Por que la respuesta sirve:</b> las <b>Bedrock model evaluations</b> dan las metricas de IA (faithfulness, coherencia) que detectan alucinaciones e inconsistencias contra la baseline. Las <b>canaries de Synthetics</b> reproducen los workflows sinteticos por intent. Los <b>chequeos por embeddings</b> con el set de referencia hacen la validacion prerelease de consistencia. La <b>aprobacion o rollback automatico</b> controla el release, y las corridas <b>nocturnas con alarmas</b> dan monitoreo continuo con rollback.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Solo canaries + consistencia, horario, sin evals:</b> sin las model evaluations no hay evaluacion de IA (alucinacion, drift) contra la baseline; falta un requisito central.</li>'
        '<li><b>Evals + canaries, solo aprobacion en exito, post-deploy:</b> le faltan los chequeos de consistencia por embeddings contra prompts de referencia; las metricas de rendimiento miden latencia/throughput, no consistencia semantica.</li>'
        '<li><b>Evals + consistencia, aprobacion manual, semanal, sin alarmas:</b> la aprobacion manual no es control automatico de release, y semanal sin alarmas no es monitoreo continuo con rollback.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Validacion de despliegue de IA = model evaluations (alucinacion/drift) + Synthetics canaries (replay de intents) + chequeos por embeddings (consistencia) + aprobacion/rollback automatico. Aprobacion manual o sin evals/alarmas no cumple.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock model evaluation</a></div>'
    ),
))

# ============================================================
# Q61 - Guardrail multi-strategy: filters medium + denied topics + mask/block
# ============================================================
cards.append(card(
    question="Una empresa financiera crea un asistente con Amazon Bedrock que <b>no debe dar consejos de inversion</b>, debe <b>bloquear contenido da&ntilde;ino</b>, <b>enmascarar PII</b>, mantener audit trails y aplicar filtrado a entradas y respuestas, con <b>minimos falsos positivos</b> y <b>varias estrategias</b> segun el tipo de contenido sensible. &iquest;Que configuracion de guardrail cumple?",
    options=[
        "Varios guardrails con politicas por niveles: uno con content filters en high que bloquee PII para interacciones publicas, otro en medium que enmascare PII para uso interno, y varios guardrails por tema para bloquear inversion con contextual grounding checks",
        "Un unico guardrail con content filters en high en todas las categorias, denied topics para inversion con frases de ejemplo y filtros de informacion sensible que apliquen la accion block a todas las entidades de PII detectadas, aplicado por igual a todas las inferencias del asistente",
        "Un guardrail separado por cada caso de uso (uno de contenido da&ntilde;ino, otro de temas de inversion y otro de PII), encadenados secuencialmente con Step Functions y logica condicional que decida cual aplicar segun la clasificacion del contenido de cada mensaje",
        "Un guardrail con content filters en medium para contenido da&ntilde;ino, denied topics para inversion con definiciones y frases de ejemplo, filtros de informacion sensible que enmascaren PII en respuestas y bloqueen informacion financiera en entradas, y evaluaciones de entrada y salida con mensajes de bloqueo custom para auditoria",
    ],
    correct=3,
    key="off1-q61",
    answer=(
        '<div class="verdict">Correcta: {{L}} - un guardrail con filters en medium + denied topics + enmascarar/bloquear (varias estrategias) + evaluaciones I/O con mensajes custom.</div>'
        '<p><b>El problema:</b> un guardrail que balancee deteccion y falsos positivos, con multiples estrategias de manejo por tipo de contenido, sobre entradas y salidas, y con soporte de auditoria.</p>'
        '<p><b>Por que la respuesta sirve:</b> un solo guardrail con content filters en <b>medium</b> equilibra deteccion de contenido da&ntilde;ino y minimiza falsos positivos. Los <b>denied topics</b> con definiciones y frases de ejemplo apuntan con precision a los consejos de inversion. Los filtros de informacion sensible dan <b>varias estrategias</b>: <b>enmascarar</b> PII en respuestas y <b>bloquear</b> informacion financiera en entradas. Filtra prompts y salidas, y los mensajes de bloqueo custom apoyan la auditoria.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Varios guardrails por niveles:</b> multiples guardrails con politicas distintas crean complejidad operativa e inconsistencias, exigen logica para elegir cual aplicar y dispersan la auditoria; ademas contextual grounding reduce alucinaciones, no enmascara temas/PII/contenido da&ntilde;ino.</li>'
        '<li><b>Un guardrail con todo en high + block a toda PII:</b> high en todo y block a cada entidad PII dispara falsos positivos y aplica una sola estrategia, no las multiples que pide el escenario.</li>'
        '<li><b>Guardrails separados encadenados con Step Functions:</b> encadenar en secuencia agrega latencia, complejidad y puntos de fallo sin beneficio; un solo guardrail ya maneja multiples tipos de politica, y encadenar independientes compone errores.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Multiples estrategias (enmascarar vs bloquear) y minimos falsos positivos = UN guardrail con filters en medium + denied topics precisos + filtros de info sensible con acciones distintas. Varios guardrails o encadenarlos suma complejidad e inconsistencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
    ),
))

# ============================================================
# Q62 - Prompt Management variants + Guardrails (formato/tono por BU)
# ============================================================
cards.append(card(
    question="Una empresa crea un asistente interno con Amazon Bedrock que resume documentos para varias unidades de negocio. Debe responder en <b>formato consistente</b> (resumen, clasificacion de riesgos, terminos marcados), <b>adaptar el tono</b> por unidad (legal, RRHH, finanzas), bloquear discurso de odio, temas inapropiados y datos sensibles como PHI, <b>gestionar centralmente variantes de prompt</b>, minimizar orquestacion y post-procesamiento, y poder <b>ajustar la moderacion con el tiempo</b>. &iquest;Que solucion cumple con el <b>MENOR mantenimiento</b>?",
    options=[
        "Bedrock Prompt Management para plantillas base, imponer el tono por unidad con variables del system prompt, Guardrails con tuning de umbrales por audiencia y gestionar los guardrails con una API de administracion interna",
        "Bedrock con inyeccion de instrucciones por unidad en las llamadas API, reglas de formato en DynamoDB, Step Functions para validar respuestas y Amazon Comprehend para filtrar contenido despues de generar",
        "Bedrock con plantillas de prompt custom en DynamoDB, una Lambda que seleccione el prompt por unidad y otra Lambda que llame a Comprehend para filtrar contenido prohibido de las respuestas",
        "Bedrock Prompt Management para configurar plantillas reutilizables y variantes de prompt por unidad de negocio, y aplicar Bedrock Guardrails con category filters y listas de terminos sensibles para bloquear contenido prohibido",
    ],
    correct=3,
    key="off1-q62",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Prompt Management (plantillas reutilizables + variantes por unidad) + Guardrails (category filters + listas de terminos).</div>'
        '<p><b>El problema:</b> formato/tono consistentes por unidad gestionados centralmente y moderacion ajustable, con minimo mantenimiento y sin orquestacion ni post-procesamiento a medida.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Prompt Management</b> configura plantillas reutilizables con <b>variantes por unidad</b> gestionadas de forma centralizada, asegurando estructura consistente (resumen, riesgos, terminos marcados) y tono por departamento sin orquestacion externa. <b>Guardrails</b> con category filters y listas de terminos sensibles bloquea contenido prohibido, y permite actualizar categorias, terminos y umbrales sin redeployar codigo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Prompt Management + tono con variables del system prompt:</b> usar variables en vez de variantes gestionadas reduce el control central y arriesga drift de tono/estructura; y los umbrales de guardrail no se personalizan por audiencia sin duplicar o enrutar (mas complejidad).</li>'
        '<li><b>Inyeccion por unidad + DynamoDB + Step Functions + Comprehend:</b> mueve el formato a Step Functions y DynamoDB (mas orquestacion y estado) y filtrar con Comprehend despues de generar agrega latencia e integraciones.</li>'
        '<li><b>Plantillas en DynamoDB + Lambdas + Comprehend:</b> enfoque descentralizado con orquestacion de Lambda y filtrado custom continuos; mas mantenimiento y mas dificil de escalar que Prompt Management + Guardrails.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Gestion central de prompts con variantes por equipo + formato consistente + moderacion ajustable sin redeploy = Prompt Management (variantes) + Guardrails. Meter el formato/filtrado en Lambdas, DynamoDB o Comprehend post-generacion suma mantenimiento.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
    ),
))

# ============================================================
# Q63 - Lambda prune + summarize con embedding + token limits
# ============================================================
cards.append(card(
    question="Un asistente con Amazon Bedrock maneja ~100 req/s por API Gateway hacia una Lambda que llama a un FM y a DynamoDB. Se vuelve caro porque los clientes envian <b>historiales conversacionales largos</b> con informacion repetida o de bajo valor; el uso de tokens sube y causa latencia inconsistente y costo innecesario. Hay que <b>reducir los tokens de entrada sin degradar la calidad</b> y sin cambios grandes de arquitectura. &iquest;Que solucion cumple?",
    options=[
        "Configurar una nueva Lambda que pode el contenido repetido o de bajo valor, resuma los historiales largos con un modelo de embeddings peque&ntilde;o y fije limites maximos de tokens de entrada y salida en la peticion InvokeModel de Bedrock",
        "Guardar el historial completo de cada interaccion del cliente en una tabla DynamoDB y enviar todo ese historial acumulado al FM en cada peticion para conservar el contexto de la conversacion",
        "Indexar todas las conversaciones en Amazon OpenSearch Service para que el FM busque en todo el contexto conversacional completo antes de generar cada respuesta y recupere los mensajes mas relevantes",
        "Reemplazar el FM actual por una familia de modelos de mayor razonamiento que soporte una ventana de contexto mas grande para aceptar los historiales conversacionales largos sin truncarlos",
    ],
    correct=0,
    key="off1-q63",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Lambda que poda + resume el historial + fija limites de tokens en InvokeModel.</div>'
        '<p><b>El problema:</b> el costo/latencia sube por historiales largos con contenido repetido; hay que <b>reducir tokens de entrada</b> preservando calidad, sin rearquitecturar.</p>'
        '<p><b>Por que la respuesta sirve:</b> una <b>Lambda de preprocesamiento</b> poda contenido redundante o de bajo valor, <b>resume</b> los historiales largos (condensando el contexto sin perder lo clave) y fija <b>limites de tokens</b> en la peticion InvokeModel. Reduce directamente el volumen de tokens de entrada, preserva la calidad via resumen y encaja en la arquitectura existente.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Guardar y enviar el historial completo:</b> hace lo contrario a lo pedido; aumenta tokens, costo y latencia.</li>'
        '<li><b>Indexar todo en OpenSearch:</b> da busqueda/recuperacion pero no reduce tokens; el contenido recuperado se suma como tokens de entrada y aumenta complejidad y costo.</li>'
        '<li><b>Cambiar a un modelo de ventana mas grande:</b> permite aceptar mas tokens pero no reduce el volumen de entrada (la causa del costo/latencia) y exige cambios grandes de arquitectura.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Reducir tokens de entrada preservando calidad = preprocesar (podar + resumir el historial) y fijar limites de tokens, no enviar todo el historial ni solo agrandar la ventana de contexto (eso no reduce el volumen).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html">docs.aws parametros de inferencia (limites de tokens)</a></div>'
    ),
))

# ============================================================
# Q64 - Glue Data Catalog crawlers + S3 tags + invocation logs Object Lock + CloudTrail integrity
# ============================================================
cards.append(card(
    question="Una empresa de investigacion genera resumenes de documentos tecnicos. Debe <b>catalogar todas las fuentes en un lugar central</b> con <b>descubrimiento y actualizacion automaticos</b>, <b>etiquetar cada resumen con citas</b> como metadatos consultables, y retener <b>audit logs inmutables y a prueba de manipulacion</b> de cada invocacion del modelo con los registros de entrada/salida. &iquest;Que solucion cumple?",
    options=[
        "Usar Amazon Comprehend para identificar las fuentes en los documentos, guardar los resumenes generados en S3 con S3 Object Lock, usar metricas de CloudWatch para generar reportes de throughput de la aplicacion y no incluir logs por cada invocacion del modelo",
        "Usar feature flags de AWS AppConfig para implementar el versionado de los datos, restringir el acceso al modelo con condiciones de IAM y mantener en S3 un archivo de mapeo versionado con las relaciones de fuente a salida para la trazabilidad",
        "Guardar las salidas de la aplicacion en DynamoDB con tags a nivel de item que incluyan la atribucion de fuente, escribir los eventos de la aplicacion a CloudWatch Logs y usar roles de IAM para proporcionar la trazabilidad de auditoria requerida",
        "Usar AWS Glue Data Catalog con crawlers para mantener las fuentes, guardar los resumenes en S3 con object tags que incluyan un source ID, guardar los model invocation logs de Bedrock en S3 con S3 Object Lock, y usar la validacion de integridad de log files de CloudTrail para inmutabilidad a prueba de manipulacion",
    ],
    correct=3,
    key="off1-q64",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Glue Data Catalog + crawlers + S3 object tags (source ID) + invocation logs en S3 con Object Lock + CloudTrail con log file integrity.</div>'
        '<p><b>El problema:</b> catalogo central autoactualizado de fuentes, citas como metadatos consultables por resumen, y audit logs inmutables (tamper-evident) de cada invocacion con su I/O.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Glue Data Catalog con crawlers</b> es un catalogo central que descubre y actualiza fuentes automaticamente. Los <b>object tags de S3</b> guardan el source ID (cita) consultable por objeto. El <b>model invocation logging</b> captura el I/O y metadatos por invocacion; guardarlo en S3 con <b>Object Lock</b> da retencion inmutable, y <b>CloudTrail con log file integrity validation</b> aporta el audit trail a prueba de manipulacion de cada llamada.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Comprehend + S3 Object Lock, sin logs por invocacion:</b> Comprehend extrae insights pero no es un catalogo central autoactualizado, y las metricas de CloudWatch son agregadas, no los logs de I/O por invocacion requeridos.</li>'
        '<li><b>AppConfig feature flags + mapeo en S3:</b> AppConfig gestiona configuracion/rollout, no cataloga ni autoactualiza fuentes; un archivo de mapeo no captura audit logs inmutables por invocacion.</li>'
        '<li><b>DynamoDB con tags de item + CloudWatch Logs + IAM:</b> DynamoDB no soporta tags a nivel de item (no se puede etiquetar cada resumen), y CloudWatch Logs e IAM no dan la inmutabilidad tamper-evident requerida.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Catalogo central autoactualizado = un catalogo de datos gestionado con crawlers. Audit inmutable de invocaciones = model invocation logs en S3 con Object Lock + validacion de integridad de los log files. Las metricas de CloudWatch son agregadas; DynamoDB no tiene tags por item.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html">docs.aws Glue Data Catalog y crawlers</a></div>'
    ),
))



# ============================================================
# Q65 - Step Functions defense-in-depth input+output Guardrails+KB
# ============================================================
cards.append(card(
    question="Una app medica movil llama a un REST API de API Gateway que invoca una Lambda que envia prompts a un FM de Amazon Bedrock. Preocupa que los pacientes envien <b>prompts da&ntilde;inos o adversariales</b> y que el modelo devuelva <b>consejo medico alucinado</b> o contenido da&ntilde;ino. Se quieren controles de seguridad <b>defense-in-depth para entradas Y salidas</b>, reusando las integraciones de API Gateway y Lambda, con los <b>MENORES cambios</b> a la app. &iquest;Que solucion cumple?",
    options=[
        "Habilitar AWS WAF en el endpoint de API Gateway con un rule set basico que bloquee palabras clave sensibles y de violencia, dejar que API Gateway haga proxy directo del resto al FM y deshabilitar la logica de Lambda existente",
        "Configurar Amazon Comprehend para detectar PII y analizar el sentimiento antes de enviar los prompts, dejar que el FM responda directamente sin guardrails y revisar manualmente una muestra de las respuestas generadas en CloudWatch Logs para detectar contenido da&ntilde;ino",
        "Configurar Bedrock Guardrails para bloquear contenido da&ntilde;ino solo en las SALIDAS del FM, dejar pasar todos los prompts de entrada directamente al FM sin validarlos y guardar los prompts y respuestas en S3 para una revision offline del equipo de compliance",
        "Un flujo de Step Functions con una Lambda para saneamiento de entrada y chequeo de prompt injection, Bedrock Guardrails para filtrar prompts y respuestas inseguras, el FM con un knowledge base de contenido medico aprobado, y una Lambda de post-procesamiento que valide la respuesta y devuelva error por API Gateway si es insegura",
    ],
    correct=3,
    key="off1-q65",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Step Functions con saneamiento de entrada + Guardrails (prompts y respuestas) + KB de contenido aprobado + validacion de salida.</div>'
        '<p><b>El problema:</b> defense-in-depth de verdad: controles tanto en la entrada (prompt injection/adversarial) como en la salida (alucinacion/da&ntilde;ino), reusando API Gateway y Lambda. Defense-in-depth = varias capas de defensa.</p>'
        '<p><b>Por que la respuesta sirve:</b> combina capas: una Lambda de <b>saneamiento y chequeo de injection</b> en la entrada, <b>Guardrails</b> que filtra prompts y respuestas a nivel de modelo, un <b>knowledge base</b> de contenido medico aprobado que ancla las respuestas (reduce alucinaciones) y una Lambda de <b>post-procesamiento</b> que valida y devuelve error por API Gateway si la respuesta es insegura o no fundamentada. Reusa el patron existente con cambios minimos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>WAF por palabras clave + deshabilitar Lambda:</b> el bloqueo por keywords no detecta prompts adversariales sutiles ni alucinaciones; deshabilitar la Lambda rompe la reutilizacion de integraciones y no da validacion pre/post.</li>'
        '<li><b>Comprehend (PII/sentimiento) + FM sin guardrails + revision manual:</b> Comprehend no ataca prompt injection ni adversarial, sin guardrails no hay control a nivel de modelo, y la revision manual no protege en tiempo real de salidas da&ntilde;inas.</li>'
        '<li><b>Guardrails solo en salidas + revision offline en S3:</b> deja la entrada expuesta a injection (no es defense-in-depth en ambos lados), y la revision offline no protege en tiempo real ni verifica exactitud.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Defense-in-depth de entrada Y salida = varias capas: saneamiento de entrada + Guardrails (prompts y respuestas) + KB para anclar (grounding) + validacion de salida. Solo WAF, solo salidas o revision offline no cubren ambos lados en tiempo real.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
    ),
))

# ============================================================
# Q66 - Guardrails content filter high en flow + bajar temperature
# ============================================================
cards.append(card(
    question="Una solucion de GenAI ense&ntilde;a historia a ni&ntilde;os de 8-14 a&ntilde;os con Amazon Bedrock y Nova Pro sobre un knowledge base de libros de historia; un flow obliga a usar el KB en cada respuesta y la temperature esta en 0.7. En pruebas hay respuestas <b>historicamente inexactas, violentas e inapropiadas para ni&ntilde;os</b>. Hay que evitar respuestas inexactas e inapropiadas. &iquest;Que solucion cumple?",
    options=[
        "Aumentar la temperature en el flow y a&ntilde;adir un nodo despues de la respuesta inicial que llame a Nova para quitar la violencia y devolver ese resultado",
        "Usar Bedrock Data Automation con salida custom que elimine todo el contenido violento del knowledge base y aumentar la temperature en el flow",
        "Configurar Bedrock Guardrails para las respuestas del modelo con content filters en strength high y accion block, a&ntilde;adir el guardrail al flow y reducir la temperature en el flow",
        "Configurar Bedrock Guardrails para los prompts con content filters en high y accion block, a&ntilde;adir el guardrail al flow y reducir la temperature en el flow",
    ],
    correct=2,
    key="off1-q66",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Guardrails con content filters high (accion block) sobre las RESPUESTAS en el flow + bajar la temperature.</div>'
        '<p><b>El problema:</b> dos cosas: filtrar contenido violento/inapropiado en la <b>salida</b> hacia ni&ntilde;os y corregir la <b>inexactitud historica</b>. La temperature controla la aleatoriedad: mas baja = mas determinista y apegado al KB.</p>'
        '<p><b>Por que la respuesta sirve:</b> los <b>content filters</b> de Guardrails en <b>strength high</b> con accion <b>block</b> sobre las respuestas aseguran filtrar la violencia hacia los ni&ntilde;os; a&ntilde;adir el guardrail al <b>flow</b> lo aplica en cada invocacion. <b>Reducir la temperature</b> hace las respuestas mas deterministas y apegadas al KB, atacando la inexactitud historica.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Subir temperature + nodo que quita violencia:</b> subir la temperature reduce el determinismo y empeora la inexactitud; y un nodo de post-procesamiento agrega latencia.</li>'
        '<li><b>BDA que elimina violencia del KB + subir temperature:</b> filtrar el KB puede sobre-filtrar y aumentar la inexactitud, y subir la temperature reduce el apego al KB, empeorando el problema.</li>'
        '<li><b>Guardrails solo en los PROMPTS:</b> impide que los ni&ntilde;os envien pedidos inapropiados, pero no evita que el modelo GENERE respuestas historicamente inexactas y violentas; falta el filtro en la salida.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Filtrar lo que el modelo GENERA = Guardrails content filters sobre las respuestas (no solo prompts). Inexactitud/incoherencia = bajar la temperature (mas determinista); subirla empeora. Aplica el guardrail dentro del flow.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters.html">docs.aws Guardrails content filters</a></div>'
    ),
))

# ============================================================
# Q68 - OpenSearch hybrid BM25+vector + Cohere rerank + weighted fusion
# ============================================================
cards.append(card(
    question="Una empresa financiera crea un asistente de investigacion que busca en millones de documentos regulatorios, reportes y marketing. Debe manejar <b>coincidencia exacta de terminos regulatorios</b> y <b>similitud conceptual</b>, priorizar los documentos mas relevantes en la ventana de contexto del FM, responder en menos de 500 ms, lograr <b>99.9% de recall</b> en terminos regulatorios y <b>95% de precision</b> en busquedas conceptuales. &iquest;Que solucion cumple?",
    options=[
        "Busqueda hibrida en Amazon OpenSearch Service combinando BM25 (coincidencia por palabra clave) y busqueda por similitud vectorial, integrar un modelo Cohere de Bedrock para puntuar y reordenar, y fusion de resultados con scoring ponderado",
        "OpenSearch Service para busqueda solo BM25, embeddings Cohere de Bedrock en almacenamiento vectorial separado en Amazon RDS PostgreSQL y logica a nivel de aplicacion para combinar resultados",
        "Bedrock Knowledge Bases para indexar con conectores de fuente, Titan Embeddings para busqueda semantica y Amazon Comprehend para extraer entidades como paso de post-procesamiento",
        "OpenSearch Service con embeddings y busqueda por similitud vectorial con Titan Embeddings, alimentando directamente los top-k al FM para que puntue y reordene sin procesamiento adicional",
    ],
    correct=0,
    key="off1-q68",
    answer=(
        '<div class="verdict">Correcta: {{L}} - busqueda hibrida (BM25 + vectorial) en OpenSearch + reranker Cohere + fusion ponderada.</div>'
        '<p><b>El problema:</b> exigen a la vez coincidencia <b>exacta</b> (99.9% recall en terminos regulatorios) y <b>conceptual</b> (95% precision), con baja latencia y priorizacion en la ventana de contexto. BM25 es coincidencia lexica; la busqueda vectorial capta significado.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>busqueda hibrida</b> combina <b>BM25</b> (coincidencia exacta de terminos regulatorios, cubre el 99.9% recall) con <b>similitud vectorial</b> (conceptual). El <b>reranker Cohere</b> de Bedrock puntua y reordena para el 95% de precision, y la <b>fusion ponderada</b> prioriza los documentos mas relevantes en la ventana de contexto, todo bajo 500 ms.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>BM25 en OpenSearch + vectores en RDS + combinar en la app:</b> arquitectura distribuida que agrega latencia de red (dificil cumplir 500 ms), y combinar en la app carece del reranking sofisticado para el 95% de precision.</li>'
        '<li><b>Knowledge Bases + Titan + Comprehend post-proceso:</b> el KB no combina exacta + vectorial (no es hibrido), y Comprehend como post-proceso agrega latencia mayor a 500 ms sin reranking para el 95% de precision.</li>'
        '<li><b>Solo vectorial + top-k al FM:</b> la busqueda solo vectorial no soporta BM25 para coincidencia exacta, asi que no garantiza el 99.9% recall de terminos regulatorios, y sin reranker no logra el 95% de precision.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Exacto (alto recall de terminos) + conceptual (alta precision) = busqueda hibrida BM25 + vectorial, mas un reranker (Cohere) y fusion ponderada. Solo vectorial pierde recall exacto; combinar en la app o post-proceso con Comprehend agrega latencia.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vector-search.html">docs.aws OpenSearch hybrid/vector search</a></div>'
    ),
))

# ============================================================
# Q70 - CloudWatch Application Insights + EMF custom metrics + anomaly
# ============================================================
cards.append(card(
    question="Un sistema de recomendaciones en EC2 llama a FMs de Amazon Bedrock. Tiene problemas intermitentes: algunas recomendaciones no coinciden con las preferencias. Se necesita observabilidad que monitoree metricas operativas, <b>detecte degradacion frente a baselines establecidas</b> y <b>genere alertas con datos de correlacion en 10 minutos</b> cuando el comportamiento del FM se desvie. &iquest;Que solucion cumple?",
    options=[
        "Configurar CloudWatch Container Insights para la infraestructura de la aplicacion, alarmas por umbrales de latencia, metricas custom de conteo de tokens con embedded metric format y dashboards de CloudWatch para visualizar el rendimiento operativo",
        "Habilitar CloudWatch Application Insights, crear metricas custom de calidad de recomendacion, tokens y latencia con embedded metric format (dimensiones por tipo de peticion y segmento), configurar CloudWatch anomaly detection sobre las metricas del modelo y analisis de patrones de log con Logs Insights",
        "Configurar tracing distribuido con CloudWatch Logs para rastrear las peticiones entre componentes, CloudWatch Logs Insights para detectar patrones de error, AWS CloudTrail para monitorear todas las llamadas a Bedrock y dashboards custom en QuickSight para visualizar",
        "Amazon OpenSearch Service con el plugin de Observability, ingesta de metricas y logs mediante Amazon Kinesis, consultas PPL custom para analizar los patrones de comportamiento del modelo y dashboards operativos para visualizar las anomalias en tiempo real",
    ],
    correct=1,
    key="off1-q70",
    answer=(
        '<div class="verdict">Correcta: {{L}} - CloudWatch Application Insights + metricas custom con EMF + anomaly detection + Logs Insights.</div>'
        '<p><b>El problema:</b> detectar desviaciones frente a baselines dinamicas y alertar con correlacion en 10 min. La anomaly detection de CloudWatch establece baselines dinamicas por ML; el embedded metric format (EMF) publica metricas custom con dimensiones.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Application Insights</b> detecta anomalias y las correlaciona con logs por reconocimiento de patrones. Con <b>metricas custom via EMF</b> (calidad de recomendacion, tokens, latencia con dimensiones por tipo de peticion y segmento) se rastrean los patrones del FM e identifican que grupos reciben recomendaciones inconsistentes. La <b>anomaly detection</b> fija baselines dinamicas y detecta desviaciones automaticamente, y <b>Logs Insights</b> analiza patrones de log.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Container Insights + alarmas de latencia:</b> Container Insights es para apps en contenedores y le falta la deteccion de anomalias frente a baselines establecidas.</li>'
        '<li><b>Tracing con Logs + CloudTrail + QuickSight:</b> CloudTrail registra llamadas de API pero no metricas operativas (tokens, latencia); QuickSight es BI, no monitoreo operativo en tiempo real, y falta la anomaly detection.</li>'
        '<li><b>OpenSearch + Kinesis + PPL:</b> exige construir y mantener un pipeline complejo (Kinesis) y consultas PPL, mas complejo que los servicios nativos de CloudWatch con anomaly detection integrada.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Detectar desviacion frente a baselines + correlacionar con logs = la observabilidad de aplicaciones de CloudWatch + anomaly detection (baselines dinamicas por ML) + metricas custom via EMF. El registro de solo llamadas de API no da metricas operativas; Container Insights es para contenedores.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html">docs.aws CloudWatch anomaly detection</a></div>'
    ),
))

# ============================================================
# Q71 - Chunking por limites semanticos + regenerar embeddings
# ============================================================
cards.append(card(
    question="Una empresa legal tiene un RAG con Bedrock y OpenSearch: embeddings de 768 dimensiones para 15M de documentos. El chunking actual es de bloques fijos de 500 tokens y suele <b>partir informacion enlazada</b> (argumentos legales, opiniones, referencias a estatutos) en chunks separados. Las salidas omiten contexto clave o citan informacion desactualizada, los tiempos de respuesta subieron 40% (p95 mayor a 2 s) y el almacenamiento crecera de 90 GB a 360 GB en un a&ntilde;o. Hay que mejorar la relevancia y el rendimiento a escala. &iquest;Que solucion cumple?",
    options=[
        "Reemplazar la recuperacion dinamica por resumenes estaticos pre-escritos en S3 y servirlos con CloudFront para reducir computo y mejorar la predictibilidad",
        "Migrar de OpenSearch a Amazon DynamoDB e implementar indices por palabra clave que permitan busquedas mas rapidas de los conceptos legales frecuentes en los documentos",
        "Cambiar el chunking a limites semanticos (argumentos legales completos, clausulas o secciones) en vez de limites fijos de tokens, y regenerar los embeddings para alinearlos con la nueva estructura de chunks",
        "Aumentar la dimensionalidad de los embeddings de 768 a 4096 dimensiones sin cambiar la estrategia de chunking ni el preprocesamiento de los documentos existentes",
    ],
    correct=2,
    key="off1-q71",
    answer=(
        '<div class="verdict">Correcta: {{L}} - chunking por limites semanticos (argumentos/clausulas/secciones) + regenerar embeddings.</div>'
        '<p><b>El problema:</b> la causa raiz es el chunking de tama&ntilde;o fijo que parte informacion legal enlazada; hay que trocear por <b>limites con significado</b> para mantener juntas las ideas relacionadas.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>chunking por limites semanticos</b> divide segun fronteras con sentido (argumentos completos, clausulas, secciones) en vez de limites arbitrarios de tokens, manteniendo junta la informacion contextualmente enlazada. Ataca directo la fragmentacion de razonamiento y referencias, y regenerar los embeddings alinea el indice con la nueva estructura, mejorando relevancia y reduciendo tiempos al traer contexto mas coherente.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Resumenes estaticos en S3 + CloudFront:</b> pierden la adaptabilidad y precision contextual de RAG; los datos legales cambian y los resumenes estaticos no responden a nuevas leyes ni resuelven la fragmentacion del chunking.</li>'
        '<li><b>Migrar a DynamoDB con indices por palabra clave:</b> DynamoDB no soporta busqueda vectorial por similitud, esencial para la comprension semantica; las palabras clave no captan la intencion ni el significado.</li>'
        '<li><b>Subir dimensiones de 768 a 4096:</b> no ataca la causa (informacion partida por chunking fijo); mas dimensiones suben memoria y computo sin resolver la fragmentacion ni la latencia elevada.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Si el chunking fijo parte ideas enlazadas y se pierde contexto = trocear por limites semanticos y regenerar embeddings. Subir dimensiones o cambiar de motor no arregla la fragmentacion; resumenes estaticos rompen la adaptabilidad de RAG.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html">docs.aws chunking en Knowledge Bases</a></div>'
    ),
))

# ============================================================
# Q72 - OpenSearch multi-node + circuit breakers + vector queues
# ============================================================
cards.append(card(
    question="Una empresa de retail tiene un recomendador con un FM de Amazon Bedrock que procesa y busca millones de embeddings de productos actualizados cada hora, con productos nuevos frecuentes. En picos de compra, las <b>busquedas por similitud</b> sufren <b>alta latencia y fallos ocasionales</b>. Hay que resolver el problema de rendimiento. &iquest;Que solucion cumple?",
    options=[
        "Implementar Amazon OpenSearch Service con arquitectura multi-nodo, ajustes de indice especificos para vectores y memory circuit breakers, y colas dedicadas de operaciones vectoriales para la capacidad de sobrecarga en picos",
        "Un knowledge base de Bedrock con particionado vectorial custom, estructuras jerarquicas de metadatos e integracion con EventBridge para actualizaciones sincronizadas del catalogo y generar vectores",
        "Una tabla DynamoDB con compresion de vectores dispersos, ejecutores de consulta en paralelo y DynamoDB Streams con Lambda para mantener el indice vectorial en tiempo real",
        "Un cluster Amazon Neptune con endpoints vectoriales especializados, funciones de similitud custom y la API bulk loader de Neptune para las actualizaciones de vectores",
    ],
    correct=0,
    key="off1-q72",
    answer=(
        '<div class="verdict">Correcta: {{L}} - OpenSearch Service multi-nodo + ajustes de indice vectorial y circuit breakers + colas de operaciones vectoriales.</div>'
        '<p><b>El problema:</b> busqueda de similitud de alto rendimiento sobre millones de vectores, con picos que causan latencia y fallos. Se necesita un motor optimizado para vectores que escale horizontalmente.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>OpenSearch Service</b> tiene busqueda vectorial nativa (k-NN) optimizada para similitud de alto throughput a escala. Escala <b>horizontalmente</b> con clusters multi-nodo, y con ajustes de indice vectoriales, <b>memory circuit breakers</b> y colas dedicadas para la sobrecarga distribuye la carga entre nodos, atacando la latencia y los fallos en picos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Knowledge base de Bedrock:</b> esta pensado para RAG con document stores, no para recomendacion de alto throughput; no da el rendimiento de busqueda vectorial especializado que resuelve los picos.</li>'
        '<li><b>DynamoDB con compresion dispersa:</b> DynamoDB esta optimizado para acceso clave-valor/documento, no para busqueda vectorial; exigiria mucho desarrollo custom y no resuelve la similitud eficiente.</li>'
        '<li><b>Neptune:</b> es una base de grafos para relaciones entre entidades; no esta optimizado para busqueda vectorial de alto rendimiento a esta escala.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Busqueda vectorial de alto rendimiento a escala con picos = el motor de busqueda gestionado (vecinos mas cercanos nativos, escala horizontal multi-nodo, circuit breakers). DynamoDB y Neptune no estan optimizados para similitud vectorial; la base de conocimiento es para RAG.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html">docs.aws OpenSearch k-NN</a></div>'
    ),
))

# ============================================================
# Q73 - Comprehend custom entity + DynamoDB session (SSE, autoscaling)
# ============================================================
cards.append(card(
    question="Un retail crea un asistente conversacional con FMs de Amazon Bedrock. Los clientes preguntan por <b>varios productos</b> en una conversacion y el asistente debe <b>mantener el contexto</b> de que producto se discute, soportar alta concurrencia con baja latencia, <b>cifrar en reposo</b> las preferencias de producto y minimizar costos escalando automaticamente en picos. &iquest;Que solucion cumple?",
    options=[
        "Un custom entity recognizer de Amazon Comprehend entrenado en las taxonomias de producto, un servicio de gestion de sesion con Amazon DynamoDB para persistir estado, cifrado del lado del servidor y auto scaling, e incluir el contexto de sesion en los prompts al FM",
        "Usar la deteccion de entidades incorporada de Comprehend para extraer menciones de producto, guardarlas en DynamoDB con TTL e incluir la entidad de producto mas reciente como contexto en cada prompt",
        "Gestionar la memoria en los prompts incluyendo todo el historial de conversacion en cada peticion al FM, con priorizacion de tokens para enfatizar menciones recientes y CloudWatch para monitorear el costo de tokens",
        "Usar Amazon Lex con intents por categoria de producto y slot types predefinidos, una Lambda de fallback para las transiciones entre productos y pasar el historial directo a Bedrock para el contexto",
    ],
    correct=0,
    key="off1-q73",
    answer=(
        '<div class="verdict">Correcta: {{L}} - custom entity recognizer de Comprehend + gestion de sesion en DynamoDB (cifrado en reposo + auto scaling).</div>'
        '<p><b>El problema:</b> identificar con precision el producto en discusion (taxonomias propias), mantener el contexto de sesion, alta concurrencia con baja latencia, cifrado en reposo y costo minimo con escalado automatico.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>custom entity recognizer</b> de Comprehend entrenado en las <b>taxonomias de producto</b> identifica con precision de que producto se habla a lo largo de la conversacion. <b>DynamoDB</b> persiste el estado de sesion con latencia de milisegundos y auto scaling (alta concurrencia), cifra en reposo por defecto, y la expiracion por TTL minimiza costos en picos. El contexto de sesion se incluye en los prompts al FM.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Entidades incorporadas de Comprehend + DynamoDB con TTL:</b> la deteccion incorporada (COMMERCIAL_ITEM) no esta entrenada en las taxonomias propias, y sin un servicio de gestion de sesion no mantiene el contexto entre multiples productos de la conversacion.</li>'
        '<li><b>Todo el historial en cada prompt:</b> consume tokens en exceso y encarece con alta concurrencia, y no cifra en reposo las preferencias almacenadas.</li>'
        '<li><b>Amazon Lex con intents por categoria:</b> Lex hace reconocimiento de intents y dialogo, no mantiene el contexto de que producto se discute entre varias consultas; la Lambda de fallback sube latencia y complejidad.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Identificar productos con taxonomia propia = Comprehend custom entity recognizer (no las entidades incorporadas). Contexto de sesion con baja latencia, cifrado y escalado = DynamoDB (cifra en reposo por defecto, auto scaling, TTL). Meter todo el historial dispara costo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/custom-entity-recognition.html">docs.aws Comprehend custom entity recognition</a></div>'
    ),
))



# ============================================================
# Q74 - API Gateway REST regional + Lambda authorizers + DynamoDB global
# ============================================================
cards.append(card(
    question="Una empresa procesa tickets de soporte y quiere integrar analisis de sentimiento y auto-respuesta con <b>Amazon Bedrock</b>, priorizar urgentes y reducir 40% el tiempo de respuesta. Debe procesar 100 webhooks concurrentes sub-500 ms, mantener 99.9% de disponibilidad <b>multi-Region</b>, <b>autenticar todas las peticiones</b> (varios sistemas de ticketing con <b>multiples metodos de autenticacion de webhook</b>), <b>sin modificar la infraestructura existente</b>, y escalar a picos de 250.000 tickets/dia. &iquest;Que solucion cumple?",
    options=[
        "Una cola SQS por Region que reciba los webhooks e invoque Lambdas que llamen a Comprehend para sentimiento y a Lex para respuestas, con EventBridge para reintentar la entrega a la API de la app",
        "Un WebSocket API de API Gateway en varias Regiones, tokens de API para autenticar, rutas que publiquen a EventBridge, reglas que invoquen Lambdas con Bedrock para sentimiento y respuestas, y CloudFront para latencia",
        "Function URLs de Lambda por sistema de ticketing con auth type NONE, Lambdas que verifiquen firmas por HMAC en el codigo, despliegue multi-Region con Global Accelerator, Bedrock para sentimiento y respuestas, y respuestas por webhook callbacks",
        "Un REST API de API Gateway con endpoint regional que reciba los webhooks e invoque Lambdas, Lambda authorizers que validen todos los metodos de autenticacion, las Lambdas llamando a Bedrock para sentimiento y respuestas, y resultados en DynamoDB global tables para disponibilidad multi-Region",
    ],
    correct=3,
    key="off1-q74",
    answer=(
        '<div class="verdict">Correcta: {{L}} - REST API regional + Lambda authorizers (multiples metodos de auth) + Bedrock + DynamoDB global tables.</div>'
        '<p><b>El problema:</b> ingerir webhooks de varios sistemas con <b>distintos metodos de autenticacion</b> sin tocar la infraestructura, usar Bedrock, y dar disponibilidad multi-Region a escala. Un Lambda authorizer permite logica de autenticacion custom centralizada.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>REST API regional</b> da un endpoint HTTP escalable para los webhooks e invoca Lambdas. Los <b>Lambda authorizers</b> validan los <b>multiples metodos de autenticacion</b> de los distintos sistemas sin modificar la infraestructura existente. Las Lambdas llaman a <b>Bedrock</b> para sentimiento y respuestas, y <b>DynamoDB global tables</b> da disponibilidad multi-Region con baja latencia, soportando el 99.9% y picos de 250.000 tickets/dia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SQS + Comprehend + Lex:</b> usa Comprehend y Lex en vez de Bedrock (incumple el requisito), y el procesamiento por cola agrega latencia asincrona que puede exceder los 500 ms.</li>'
        '<li><b>WebSocket API + tokens:</b> los WebSocket API son para conexiones bidireccionales persistentes, no para ingerir webhooks; no soportan de forma nativa multiples metodos de auth heterogeneos sin integracion custom y modificar la infraestructura.</li>'
        '<li><b>Function URLs con auth NONE + HMAC:</b> las function URLs solo soportan un tipo de auth (AWS_IAM o NONE); con NONE habria que implementar HMAC custom en cada Lambda en vez de una autorizacion centralizada, subiendo complejidad y riesgo de fallos de autenticacion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Varios metodos de autenticacion de webhook sin tocar la infraestructura = una API gestionada con Lambda authorizers (autenticacion custom centralizada). Multi-Region con baja latencia = tablas globales replicadas. Ojo: debe usar el servicio de FMs (no otros de NLP), y las function URLs solo tienen un tipo de auth.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html">docs.aws API Gateway Lambda authorizers</a></div>'
    ),
))

create(deck_name="AIP-C01::Oficial-1", cards=cards, out_path="out/AIP-C01_Oficial1.apkg", do_import=False)
