#!/usr/bin/env python3
"""
AIP-C01::03 - Preguntas nuevas (deduplicadas) del examen 3, version 2.

18 cartas construidas a partir de decks/aip-c01/dedupe/new_to_generate_v2_exam3.json.
Son conceptos nuevos para el track AIP-C01. Las cartas que seguian vigentes de la v1
se conservan tal cual (misma key aip03-q<n>) para preservar el progreso de estudio.

Reglas aplicadas:
- 1 carta por pregunta (solo la MCQ directa).
- Exactamente 4 opciones (las 18 fuentes ya venian con 4).
- Espanol, HTML con entidades para acentos, sin em dashes.
- Verdict con {{L}} (nunca hardcodear la letra; el motor baraja y sustituye).
- El frente no filtra la respuesta.
- Cada dorso: define terminos, conecta escenario con solucion, refuta CADA
  distractor uno por uno bajo "Por que NO las otras", exam tip y links.
- Distractores near-miss plausibles; longitudes balanceadas entre las 4 opciones.
- key estable y unica: aip03-q<n> usando el numero n de la fuente.
- correct = indice 0-based (mismo orden de opciones que la fuente).
"""
from anki_mcq import card, create

cards = []


# ============================================================
# Q2 - SageMaker Experiments tracker en processing job
# ============================================================
cards.append(card(
    question="Un script PySpark en Amazon EMR hace feature engineering sobre datos en S3 para modelos en SageMaker AI. El desarrollador debe <b>medir como distintas combinaciones de parametros de transformacion y tama&ntilde;os de muestra afectan la precision</b>. &iquest;Que solucion cumple mejor?",
    options=[
        "SageMaker Experiments tracker ejecutando el script como un SageMaker processing job",
        "Un hook de SageMaker Debugger durante un training job de SageMaker",
        "SageMaker Model Monitor antes de cada iteracion de entrenamiento",
        "SageMaker Autopilot para elegir la configuracion de preprocesamiento PySpark",
    ],
    correct=0,
    key="aip03-q2",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SageMaker Experiments tracker en un processing job.</div>'
        '<p><b>El problema:</b> hay que comparar de forma estructurada como distintos parametros del preprocesamiento (PySpark) y tama&ntilde;os de muestra impactan la precision y la inferencia. Es un problema de <b>seguimiento de experimentos</b>: registrar parametros de entrada y metricas de salida y compararlos entre corridas.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>SageMaker Experiments</b> es el servicio dise&ntilde;ado para eso: registra (loguea) parametros y metricas de cada corrida y las organiza para compararlas. Al correr el script como <b>processing job</b> (el tipo de job pensado para preprocesamiento y transformacion de datos), el tracker captura tanto los parametros de PySpark como las metricas asociadas.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SageMaker Debugger en un training job:</b> Debugger perfila y monitorea el <b>entrenamiento</b> (tensores, gradientes, estados internos del modelo), no scripts de preprocesamiento; no registra parametros de PySpark de forma estructurada.</li>'
        '<li><b>SageMaker Model Monitor:</b> vigila modelos <b>ya desplegados</b> (deriva de datos y calidad en produccion); no rastrea parametros de preprocesamiento ni sirve para experimentar durante training/processing.</li>'
        '<li><b>SageMaker Autopilot:</b> automatiza preprocesamiento y seleccion de modelo con su propia logica; no admite scripts PySpark propios ni el control manual de los parametros de feature engineering que el equipo quiere variar.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Registrar y comparar corridas variando parametros de entrada y metricas = servicio de seguimiento de experimentos ejecutado como processing job. Debugger sirve para depurar el entrenamiento, Model Monitor para produccion y Autopilot es AutoML sin control fino.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/experiments.html">docs.aws SageMaker Experiments</a></div>'
    ),
))

# ============================================================
# Q3 - Bedrock Data Automation ingesta continua
# ============================================================
cards.append(card(
    question="Un asistente GenAI se alimenta de datos de ventas y soporte en Amazon S3. Se necesita un pipeline <b>continuo</b> que enriquezca con Comprehend y SageMaker AI y alimente un modelo fundacional, <b>minimizando el ETL manual</b>. &iquest;Que enfoque es mas escalable?",
    options=[
        "Amazon Bedrock Data Automation para ingerir S3 de forma continua, enriquecer con Comprehend y cargar los datos al reentrenamiento del FM",
        "Amazon EventBridge disparando AWS Lambda ante datos nuevos en S3, que preprocesa, llama a Comprehend y empuja a SageMaker AI",
        "Exportar el CRM a S3 cada semana y correr un SageMaker Notebook que transforma, llama a Comprehend y alimenta el reentrenamiento",
        "SageMaker Data Wrangler para transformar con Comprehend, correr training jobs aparte y disparar manualmente el reentrenamiento del FM en Bedrock",
    ],
    correct=0,
    key="aip03-q3",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Amazon Bedrock Data Automation con ingesta continua.</div>'
        '<p><b>El problema:</b> se necesita un pipeline <b>continuo y de bajo mantenimiento</b> que ingiera datos de S3, los enriquezca con Comprehend y SageMaker AI, y los cargue de forma automatica al flujo del modelo fundacional, sin ETL manual constante.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Data Automation</b> es un servicio gestionado que ingiere datos de forma continua, aplica preprocesamiento (incluida la extraccion de sentimiento y entidades) y entrega los datos enriquecidos a los pipelines de reentrenamiento. Al ser gestionado y continuo, cubre la frescura de datos y elimina el ETL manual con la menor sobrecarga operativa.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>EventBridge + Lambda:</b> orquestar preprocesamiento, Comprehend y reentrenamiento con Lambda a&ntilde;ade complejidad operativa; Lambda tiene limites de tiempo de ejecucion y de concurrencia, asi que resulta solo parcialmente automatizado y menos confiable para volumenes grandes y reentrenamiento continuo.</li>'
        '<li><b>Exportar a S3 cada semana + Notebook:</b> es un proceso periodico y manual (semanal); no da la disponibilidad continua de datos que necesita un asistente en produccion, por lo que los modelos quedan desactualizados.</li>'
        '<li><b>Data Wrangler + trigger manual:</b> automatiza parte de la transformacion, pero sigue dependiendo de ejecucion manual del entrenamiento y del reentrenamiento del FM; no es un flujo end-to-end automatizado y aumenta la carga operativa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Ingesta continua y enriquecimiento gestionado para alimentar FMs con minimo ETL = el servicio gestionado de automatizacion de datos de Bedrock. Lambda tiene limite de tiempo y de concurrencia; los Notebooks y los triggers manuales o semanales no son "continuos".</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html">docs.aws Bedrock Data Automation</a></div>'
    ),
))

# ============================================================
# Q8 - SageMaker multi-variant endpoint A/B
# ============================================================
cards.append(card(
    question="Una plataforma de recomendacion de noticias quiere <b>A/B testing</b> en vivo entre varias variantes de modelo, medir engagement en tiempo real y luego <b>volcar el 100% del trafico</b> a la mejor, con la menor sobrecarga operativa. &iquest;Que solucion cumple?",
    options=[
        "Endpoints multi-variante de Amazon SageMaker AI, con pesos de trafico ajustables",
        "Modelos en Amazon EC2 tras un Application Load Balancer (ALB) con pesos ajustados a mano",
        "Un endpoint de SageMaker AI por modelo con Amazon API Gateway y enrutamiento ponderado",
        "AWS CodeDeploy blue/green con un Application Load Balancer (ALB) entre versiones",
    ],
    correct=0,
    key="aip03-q8",
    answer=(
        '<div class="verdict">Correcta: {{L}} - endpoints multi-variante de SageMaker AI.</div>'
        '<p><b>El problema:</b> hacer A/B testing en vivo entre varias variantes, medir engagement en tiempo real y luego volcar el 100% del trafico a la ganadora, con la menor sobrecarga operativa.</p>'
        '<p><b>Por que la respuesta sirve:</b> un <b>endpoint multi-variante</b> de SageMaker aloja varias variantes de modelo detras de un unico endpoint y reparte el trafico segun <b>pesos</b> configurables. Es la forma nativa de hacer A/B testing: se ajustan los pesos para experimentar y, cuando se identifica la mejor, se pone su peso al 100%. Trae monitoreo integrado y no exige gestionar infraestructura propia.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>EC2 tras un ALB con ajuste manual:</b> exige montar y gestionar despliegue, escalado, monitoreo y enrutamiento a mano; aumenta la complejidad operativa frente a un servicio gestionado como SageMaker.</li>'
        '<li><b>Un endpoint por modelo + API Gateway:</b> tecnicamente posible, pero gestionar multiples endpoints y configurar el split y el monitoreo en API Gateway a&ntilde;ade sobrecarga y pierde la integracion nativa de los endpoints multi-variante.</li>'
        '<li><b>CodeDeploy blue/green + ALB:</b> blue/green esta pensado para despliegues de aplicaciones, no para inferencia ML en tiempo real; no ofrece split de trafico fino ni seguimiento de metricas de inferencia en vivo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>A/B testing gestionado entre modelos con un solo endpoint y pesos ajustables = production variants (endpoint multi-variante) de SageMaker. ALB/API Gateway/CodeDeploy = montaje manual o para despliegue de apps, no para variantes de modelo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-ab-testing.html">docs.aws A/B testing con production variants</a></div>'
    ),
))

# ============================================================
# Q9 - Wavelength Zones + context pruning GenAI
# ============================================================
cards.append(card(
    question="Una app GenAI enriquece video en vivo con un modelo fundacional en Amazon Bedrock. Necesita <b>latencia ultrabaja (&lt;20 ms)</b> para moviles con inferencia en el borde, <b>almacenamiento de archivos compartido</b> y <b>reducir tokens del prompt</b> en picos. &iquest;Que solucion cumple mejor?",
    options=[
        "AWS Wavelength Zones con EC2 y Bedrock, Amazon EFS como almacenamiento compartido y context pruning para reducir tokens del prompt en picos",
        "Una sola Region con EC2 y Bedrock, artefactos en Amazon S3 y subir los limites de tama&ntilde;o de respuesta del modelo",
        "AWS Lambda con Bedrock en una Region central, Redis OSS en Amazon ElastiCache y chunking fijo",
        "Varias zonas de una Region con EC2, Amazon EBS compartido entre instancias y rafagas de tokens",
    ],
    correct=0,
    key="aip03-q9",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Wavelength Zones + EFS + context pruning.</div>'
        '<p><b>El problema:</b> latencia ultrabaja (&lt;20 ms) para moviles, computo en el borde cerca del usuario, almacenamiento de archivos compartido entre instancias y reduccion de tokens en picos.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AWS Wavelength Zones</b> llevan el computo al borde de las redes 5G, junto al usuario movil, lo que habilita la latencia ultrabaja pedida. <b>Amazon EFS</b> es un sistema de archivos compartido montable por varias instancias a la vez (ideal para artefactos intermedios). El <b>context pruning</b> recorta dinamicamente el contexto del prompt, reduciendo tokens justo en los picos de trafico.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Una sola Region + S3 + subir limites de respuesta:</b> una Region central no da latencia de borde; guardar en S3 no es un sistema de archivos compartido montado; y aumentar el tama&ntilde;o de respuesta sube tokens en vez de reducirlos.</li>'
        '<li><b>Lambda central + ElastiCache + chunking fijo:</b> la ejecucion centralizada en Lambda no alcanza la latencia ultrabaja; el chunking de tama&ntilde;o fijo es rigido y usa tokens de forma ineficiente frente a tecnicas dinamicas como context pruning.</li>'
        '<li><b>Multi-AZ + EBS + rafagas de tokens:</b> las AZ siguen dentro de una Region, sin latencia de borde; <b>EBS no admite acceso compartido</b> entre varias instancias; y "rafagas de tokens" describe el trafico, no optimiza el uso de tokens.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Latencia de borde para moviles = computo en zonas de borde 5G. Almacenamiento de archivos compartido entre varias instancias = sistema de archivos elastico compartido (los volumenes de bloque son de una sola instancia). Menos tokens de forma dinamica = poda de contexto, no chunking de tama&ntilde;o fijo.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/wavelength/latest/developerguide/what-is-wavelength.html">docs.aws AWS Wavelength</a></div>'
    ),
))


# ============================================================
# Q13 - Bedrock latency-optimized inference + prompt caching
# ============================================================
cards.append(card(
    question="Un chatbot sobre Amazon Bedrock atiende 60,000 consultas diarias con picos de 180,000. El 35% comparte <b>contexto casi identico</b>. Hay que dar <b>baja latencia consistente</b> en picos de la forma <b>mas costo-eficiente</b>. &iquest;Que solucion cumple?",
    options=[
        "Inferencia latency-optimized de Amazon Bedrock combinada con prompt caching",
        "Provisioned Throughput con suficientes model units (MU) y Amazon ElastiCache (Redis OSS)",
        "Bedrock Intelligent Prompt Routing por complejidad con inferencia cross-Region",
        "Bedrock Model Distillation para crear un modelo destilado mas peque&ntilde;o del maestro",
    ],
    correct=0,
    key="aip03-q13",
    answer=(
        '<div class="verdict">Correcta: {{L}} - latency-optimized inference + prompt caching.</div>'
        '<p><b>El problema:</b> baja latencia consistente en picos y costo-eficiencia, aprovechando que el 35% de las consultas repite contexto casi identico. Se descarto <b>Bedrock Agents</b> por complejidad innecesaria.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>inferencia latency-optimized</b> de Bedrock reduce la latencia de respuesta al invocar el modelo. El <b>prompt caching</b> guarda el contexto ya procesado, asi que en las consultas repetidas (ese 35%) no se reprocesa ni se pagan de nuevo esos tokens de contexto. Es una capacidad integrada de Bedrock: ataca directamente la latencia y el costo del contexto repetido sin infraestructura extra.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Provisioned Throughput + ElastiCache:</b> el Provisioned Throughput compromete y paga capacidad fija, apto para cargas estables y no para picos de 60k a 180k; dimensionar para el pico significa pagar capacidad ociosa. Ademas ElastiCache autogestionado a&ntilde;ade infraestructura que provisionar y mantener, a diferencia del prompt caching integrado.</li>'
        '<li><b>Intelligent Prompt Routing + cross-Region:</b> el routing dirige cada peticion al FM mas adecuado por complejidad (optimiza costo/calidad), no reduce especificamente la latencia en picos; y no explota el contexto repetido como el prompt caching.</li>'
        '<li><b>Model Distillation:</b> produce un modelo mas peque&ntilde;o pero requiere un proceso de entrenamiento y evaluacion previo; no es un control de latencia inmediato para picos impredecibles ni aprovecha el contexto repetido.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Contexto repetido + latencia + costo = prompt caching + latency-optimized inference (ambos integrados en Bedrock). Provisioned Throughput = carga estable y predecible; Prompt Routing = optimiza por complejidad; Distillation = requiere entrenar antes.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html">docs.aws Bedrock prompt caching</a></div>'
    ),
))

# ============================================================
# Q20 - SageMaker DeepAR forecasting global
# ============================================================
cards.append(card(
    question="Una utility maneja consumo horario de 150 tipos de medidores inteligentes con 30 a&ntilde;os de historico. Quiere un modelo a medida que <b>pronostique el uso futuro de todos los tipos</b>, con la <b>MENOR sobrecarga operativa</b>. &iquest;Que opcion conviene?",
    options=[
        "Un unico modelo global de forecasting con el algoritmo SageMaker AI DeepAR",
        "Multiples modelos con el algoritmo SageMaker AI Prophet, uno por tipo de medidor",
        "SageMaker AI Autopilot para un unico modelo con el dataset combinado",
        "Un unico modelo global con el algoritmo SageMaker AI XGBoost sobre todos los tipos",
    ],
    correct=0,
    key="aip03-q20",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SageMaker DeepAR (modelo global de forecasting).</div>'
        '<p><b>El problema:</b> pronosticar series temporales de muchos dispositivos (150 tipos) con minima operacion. Un solo modelo que aprenda de todas las series a la vez reduce el mantenimiento.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>DeepAR</b> es el algoritmo integrado de SageMaker para <b>forecasting de series temporales</b> y esta dise&ntilde;ado para entrenar un <b>modelo global</b> sobre muchas series relacionadas, capturando patrones compartidos entre todos los medidores. Un solo modelo para todos = menor sobrecarga operativa que mantener 150.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Prophet, uno por tipo:</b> gestionar 150 modelos separados dispara la complejidad de entrenamiento, despliegue y mantenimiento; Prophet encaja mejor en series univariadas simples y no escala como DeepAR para muchos series.</li>'
        '<li><b>Autopilot:</b> esta optimizado para datos tabulares y tareas de clasificacion/regresion, no para forecasting; carece de soporte nativo para dependencias temporales y estacionalidad.</li>'
        '<li><b>XGBoost:</b> es potente para datos tabulares pero no esta pensado para series temporales; obligaria a crear manualmente features de tiempo, aumentando complejidad y carga operativa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Forecasting de muchas series relacionadas con un solo modelo global de series temporales es lo de menor operacion. Entrenar un modelo por serie multiplica el mantenimiento; las opciones tabulares (AutoML o gradient boosting) no manejan de forma nativa dependencias temporales ni estacionalidad.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html">docs.aws SageMaker DeepAR</a></div>'
    ),
))


# ============================================================
# Q27 - AppConfig Agent config dinamica validada
# ============================================================
cards.append(card(
    question="Una app de IA generativa en Amazon EC2 necesita actualizar flags de configuracion de forma <b>dinamica sin reiniciar</b> la aplicacion, y los cambios deben <b>validarse contra un esquema</b> antes de desplegarse para evitar errores en runtime. &iquest;Que solucion gestiona estas configuraciones de forma eficiente?",
    options=[
        "Implementar el AppConfig Agent en la instancia EC2 para recuperar y cachear configuraciones con validacion previa al despliegue",
        "Usar AWS CloudFormation Guard para validar los archivos de configuracion y enviar las actualizaciones via Amazon S3",
        "Utilizar Amazon DynamoDB Streams para disparar una funcion AWS Lambda que actualice los archivos de configuracion locales",
        "Usar Amazon Bedrock Prompt Management para almacenar las variables de entorno y los flags de configuracion de la aplicacion",
    ],
    correct=0,
    key="aip03-q27",
    answer=(
        '<div class="verdict">Correcta: {{L}} - AppConfig Agent en la instancia EC2.</div>'
        '<p><b>El problema:</b> cambiar configuracion en caliente (sin reiniciar la app) y validar cada cambio contra un esquema antes de desplegarlo.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AWS AppConfig</b> gestiona configuracion dinamica de aplicaciones: aplica validadores (por esquema JSON o Lambda) antes del despliegue y ofrece estrategias de despliegue gradual. El <b>AppConfig Agent</b> corriendo en la EC2 recupera y <b>cachea</b> la configuracion y la actualiza sin reiniciar la app. Cubre validacion previa + actualizacion dinamica.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CloudFormation Guard + S3:</b> Guard es politica como codigo para validar plantillas de infraestructura (IaC), no configuracion dinamica de la aplicacion en runtime.</li>'
        '<li><b>DynamoDB Streams + Lambda:</b> Streams detecta cambios, pero es una solucion sobredimensionada para gestion de configuracion; no aporta la validacion integrada, las estrategias de despliegue ni el cacheo que da AppConfig.</li>'
        '<li><b>Bedrock Prompt Management:</b> versiona y gestiona <b>prompts</b> de IA generativa, no variables de entorno ni flags de configuracion de infraestructura.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Configuracion dinamica sin reinicio, con validacion por esquema y despliegue gradual = servicio gestionado de configuracion de aplicaciones (con su agente para cachear en la instancia). Validar plantillas de IaC o versionar prompts resuelven problemas distintos.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-integration-containers-agent.html">docs.aws AppConfig Agent</a></div>'
    ),
))

# ============================================================
# Q28 - Bedrock InvocationLatency y fine-tune Titan
# ============================================================
cards.append(card(
    question="Una empresa hace fine-tuning de Amazon Titan Text en SageMaker AI y despliega via la API gestionada de Bedrock. Por cumplimiento: <b>cifrar artefactos con AWS KMS</b>, <b>auditar las llamadas a Bedrock</b> y <b>monitorear latencia y throughput por Region</b>. &iquest;Que solucion es segura y observable?",
    options=[
        "Datos en S3 con KMS, Bedrock con clave del cliente, CloudTrail y CloudWatch",
        "Datos cifrados con SSE-S3, despliegue tras API Gateway, Amazon Macie y logs de API Gateway",
        "Titan en Bedrock sin fine-tuning, IAM, CloudTrail y GenAI Observability de CloudWatch",
        "Titan en SageMaker exportado a inferencia en EC2 con EBS cifrado y AWS Config",
    ],
    correct=0,
    key="aip03-q28",
    answer=(
        '<div class="verdict">Correcta: {{L}} - fine-tune en SageMaker con KMS + Bedrock con CMK + CloudTrail + CloudWatch InvocationLatency.</div>'
        '<p><b>El problema:</b> hay tres requisitos: (1) cifrar artefactos con KMS gestionado por el cliente, (2) auditar las llamadas a Bedrock, (3) monitorear latencia/throughput por Region. Y el modelo debe desplegarse por la API gestionada de Bedrock tras fine-tuning.</p>'
        '<p><b>Por que la respuesta sirve:</b> cifra los datos de entrenamiento en S3 con <b>KMS</b> y despliega en Bedrock con una <b>clave gestionada por el cliente (CMK)</b>, cumpliendo el cifrado auditable. <b>AWS CloudTrail</b> registra las llamadas a la API para la auditoria. <b>Amazon CloudWatch</b> expone metricas de Bedrock como <code>InvocationLatency</code> para vigilar latencia y throughput por Region. Cubre los tres requisitos manteniendo el despliegue en Bedrock.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SSE-S3 + API Gateway + Macie:</b> SSE-S3 no da control de clave del cliente ni la auditabilidad granular de SSE-KMS; API Gateway es innecesario frente al endpoint gestionado de Bedrock; y Macie descubre datos sensibles, no monitorea invocaciones ni rendimiento.</li>'
        '<li><b>Sin fine-tuning + CloudTrail + GenAI Observability:</b> omite la adaptacion al dominio (fine-tuning) que pide el escenario y no cubre el cifrado de artefactos con CMK, aunque el logging con CloudTrail y las metricas de GenAI Observability (InvocationLatency, InputTokenCount, OutputTokenCount) si sean validos.</li>'
        '<li><b>Exportar a EC2 + EBS + AWS Config:</b> mover la inferencia a EC2 renuncia a la seguridad y escala gestionadas de Bedrock e incumple "desplegar via la API gestionada de Bedrock"; AWS Config rastrea estado de configuracion, no latencia/throughput en tiempo real (eso es CloudWatch).</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cifrado con control del cliente = clave gestionada por el cliente (no cifrado gestionado por el servicio de almacenamiento). Auditar llamadas a la API = servicio de trazas de API. Latencia y throughput en tiempo real = metricas de CloudWatch, no el servicio de estado de configuracion. Desplegar "via Bedrock" descarta mover la inferencia a EC2.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-cw.html">docs.aws metricas de Bedrock en CloudWatch</a></div>'
    ),
))


# ============================================================
# Q30 - Bedrock Prompt Management + Guardrails
# ============================================================
cards.append(card(
    question="Un portal GenAI con Amazon Bedrock debe adaptar el estilo por audiencia, filtrar contenido toxico e informacion de salud protegida (PHI), <b>evitar hardcodear plantillas de prompt</b>, quitar scripts de post-procesamiento y <b>actualizar los filtros de seguridad sin redeployar</b>. &iquest;Que solucion tiene MENOR mantenimiento?",
    options=[
        "Bedrock Prompt Management para plantillas reutilizables con variantes por departamento, y Bedrock Guardrails con filtros de contenido e informacion sensible",
        "Bedrock Prompt Management y Guardrails, gestionando los cambios con una API interna propia",
        "Bedrock Agents para inyectar instrucciones por departamento, reglas en DynamoDB, validacion con Step Functions y Guardrails solo como post-procesamiento",
        "Bedrock Knowledge Bases para las plantillas, una Lambda que selecciona el prompt y otra Lambda que filtra con Amazon Comprehend",
    ],
    correct=0,
    key="aip03-q30",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock Prompt Management + Guardrails.</div>'
        '<p><b>El problema:</b> plantillas de prompt centralizadas y reutilizables (con variantes por audiencia), filtrado de contenido toxico/off-topic/PHI sin scripts propios, y filtros de seguridad actualizables sin redeploy, todo con minimo mantenimiento.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Prompt Management</b> centraliza plantillas reutilizables con <b>variantes</b> por departamento, evitando hardcodear o dispersar prompts. <b>Guardrails</b> aplica de forma nativa filtros de categorias de contenido y de informacion sensible (PHI), reemplazando los scripts de post-procesamiento; sus filtros se actualizan de forma independiente sin redeployar la app. Ambos son gestionados: la menor sobrecarga.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Prompt Management + Guardrails + API de administracion propia:</b> usa los servicios correctos pero a&ntilde;ade una API interna redundante; Guardrails ya expone APIs nativas para crear y actualizar guardrails, asi que esa capa extra solo suma mantenimiento.</li>'
        '<li><b>Bedrock Agents + DynamoDB + Step Functions + Guardrails al final:</b> Agents es para orquestar tareas multi-paso, no para plantillas simples; DynamoDB y Step Functions exigen esquema y maquinas de estado a mantener; y aplicar Guardrails solo despues de generar deja que el contenido da&ntilde;ino se produzca antes de filtrarse.</li>'
        '<li><b>Knowledge Bases + dos Lambdas + Comprehend:</b> Knowledge Bases es para RAG, no para almacenar plantillas; mantener dos Lambdas para seleccion de prompt y moderacion con Comprehend a&ntilde;ade codigo y tuning que el filtrado integrado de Guardrails ya evita.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Plantillas reutilizables gestionadas = Prompt Management. Filtrar toxicidad/PHI sin codigo y actualizable sin redeploy = Guardrails (aplicado en la generacion, no solo despues). Agents = orquestacion; Knowledge Bases = RAG.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
    ),
))

# ============================================================
# Q36 - Rollout gradual Bedrock con Step Functions
# ============================================================
cards.append(card(
    question="Una empresa quiere un <b>rollout gradual de versiones de modelo de Amazon Bedrock</b> guiado por metricas de inferencia en vivo, con visibilidad de latencia y errores y <b>rollback automatico sin intervencion</b> ante un fallo. &iquest;Que solucion cumple?",
    options=[
        "Versiones en Bedrock (provisioned throughput) y un flujo de Step Functions por EventBridge que consulta CloudWatch y ramifica",
        "Cada version en una Lambda versionada y AWS CodeDeploy con un alias en cronograma fijo",
        "Cada version como variante de endpoint de SageMaker AI con SageMaker Model Monitor y Lambda de rollback",
        "El split como feature flag en AWS AppConfig con despliegue gradual y alarmas de CloudWatch",
    ],
    correct=0,
    key="aip03-q36",
    answer=(
        '<div class="verdict">Correcta: {{L}} - EventBridge + Step Functions orquestando el rollout sobre Bedrock.</div>'
        '<p><b>El problema:</b> rollout gradual de versiones de modelo <b>de Bedrock</b>, guiado por metricas en vivo, con avance/retroceso automatico de trafico, visibilidad de latencia y errores y rollback sin intervencion.</p>'
        '<p><b>Por que la respuesta sirve:</b> alojar las versiones en Bedrock (provisioned throughput) y orquestar con <b>Step Functions</b> disparado por <b>EventBridge</b> permite un flujo por etapas: desplaza una porcion de trafico, pausa, y una <b>Lambda consulta CloudWatch</b> para leer latencia/errores; el flujo ramifica para subir el trafico si las metricas estan sanas o <b>revertir automaticamente</b> si bajan. Cubre el control por metricas y el rollback sin humanos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>CodeDeploy + alias de Lambda:</b> CodeDeploy con alias solo desplaza trafico entre versiones del <b>codigo de la Lambda</b>, no entre las versiones de modelo de Bedrock que esa Lambda invoca; ademas usa un cronograma fijo y no evalua metricas de inferencia ni patrones historicos.</li>'
        '<li><b>Variantes de endpoint de SageMaker:</b> las variantes aplican a modelos alojados en endpoints de SageMaker, no a los FMs gestionados de Bedrock; ese mecanismo no puede desplazar trafico entre versiones de modelo de Bedrock.</li>'
        '<li><b>AppConfig feature flag:</b> AppConfig despliega valores de configuracion y flags, no enruta ni invoca trafico entre versiones de Bedrock; la app aun necesitaria logica propia para leer el flag y enrutar, y una alarma solo detiene el despliegue de config, no orquesta un rollback en vuelo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Rollout gradual guiado por metricas de inferencia en vivo con rollback automatico = un orquestador de flujos por etapas disparado por eventos que consulta CloudWatch y ramifica. Los alias de despliegue de codigo, las variantes de endpoint de otro servicio de ML y los feature flags de configuracion no enrutan trafico entre versiones del modelo fundacional.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html">docs.aws AWS Step Functions</a></div>'
    ),
))

# ============================================================
# Q45 - Amazon Fraud Detector prediction API
# ============================================================
cards.append(card(
    question="Una fintech ve mas fraude de cuentas <b>recien registradas</b> con pagos altos, y su modelo por lotes en SageMaker no lo marca a tiempo. Buscan deteccion <b>en tiempo real</b> que <b>evalue y rechace al momento</b>, con <b>minimo esfuerzo operativo</b>. &iquest;Que opcion cumple?",
    options=[
        "Usar la API de prediccion de Amazon Fraud Detector para aprobar o rechazar automaticamente las transacciones identificadas como fraudulentas",
        "Entrenar un modelo supervisado de fraude en SageMaker AI y desplegarlo en Amazon EC2 a medida",
        "Comprehend para extraer entidades de la transaccion y reentrenar un modelo en SageMaker AI",
        "Usar Amazon Lookout for Vision para detectar anomalias en imagenes de comprobantes subidos y clasificarlas como fraudulentas o legitimas",
    ],
    correct=0,
    key="aip03-q45",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Amazon Fraud Detector (prediction API).</div>'
        '<p><b>El problema:</b> deteccion de fraude en tiempo real sobre datos transaccionales, con decision inmediata (aprobar/rechazar) y minima operacion.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Amazon Fraud Detector</b> es un servicio gestionado especifico para detectar fraude en linea. Su <b>API de prediccion</b> evalua cada transaccion en tiempo real y devuelve un veredicto para aprobar o rechazar al momento, sin montar ni operar infraestructura de modelos. Es la opcion de menor esfuerzo para el caso.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Modelo propio en EC2:</b> gestionar infraestructura, escalado y codigo de inferencia a medida contradice el requisito de minimo esfuerzo y puede no dar respuesta en tiempo real.</li>'
        '<li><b>Comprehend + reentrenar en SageMaker:</b> Comprehend es NLP (sentimiento, entidades), no deteccion de fraude sobre datos transaccionales estructurados; ademas sigue siendo por lotes, sin decision en tiempo real.</li>'
        '<li><b>Lookout for Vision:</b> detecta anomalias en imagenes (por ejemplo defectos de fabricacion), no analiza datos de transacciones ni patrones de comportamiento; no aborda el fraude de pagos en tiempo real.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Deteccion de fraude en tiempo real sobre datos transaccionales con minima operacion = el servicio gestionado especifico de deteccion de fraude y su API de prediccion. Comprehend es NLP y Lookout for Vision detecta anomalias en imagenes, no en transacciones.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/frauddetector/latest/ug/what-is-frauddetector.html">docs.aws Amazon Fraud Detector</a></div>'
    ),
))


# ============================================================
# Q53 - Bedrock Knowledge Base RAG + PerformanceConfigLatency
# ============================================================
cards.append(card(
    question="Una app GenAI de viajes usa Amazon Bedrock con Anthropic Claude. Los usuarios ven <b>respuestas lentas</b> y el modelo <b>alucina paquetes no reservables</b>. Se descarto un OpenSearch propio; se requiere algo que <b>integre nativamente</b> con el flujo GenAI. &iquest;Que solucion cumple?",
    options=[
        "Una Bedrock Knowledge Base con Retrieval Augmented Generation (RAG) sobre el inventario en vivo, y el parametro PerformanceConfigLatency",
        "Reforzar el grounding de Bedrock Guardrails, activar Automated Reasoning checks y throughput dedicado",
        "Un Bedrock Agent con un action group sobre AWS Lambda que consulte el inventario, mas prompt engineering",
        "Indexar el inventario en Amazon Kendra, inyectar snippets en cada prompt y cachear en Amazon DynamoDB",
    ],
    correct=0,
    key="aip03-q53",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Bedrock Knowledge Base con RAG + PerformanceConfigLatency.</div>'
        '<p><b>El problema:</b> dos males a la vez: alucinaciones (recomienda paquetes inexistentes o no disponibles) y latencia alta. La causa de fondo es que el modelo no consulta el inventario real; hay que <b>anclar (grounding)</b> sus respuestas en datos vivos y reducir latencia, con integracion nativa.</p>'
        '<p><b>Por que la respuesta sirve:</b> una <b>Bedrock Knowledge Base</b> con <b>RAG</b> recupera fragmentos del inventario en vivo y obliga al modelo a responder solo con contenido recuperado y verificado, eliminando las alucinaciones de paquetes no reservables. Es una capa RAG gestionada y nativa de Bedrock. El parametro <b>PerformanceConfigLatency</b> optimiza la latencia de la respuesta.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Guardrails grounding + Automated Reasoning + throughput dedicado:</b> el grounding check de Guardrails solo valida tras generar si la respuesta se apoya en una fuente dada; no da al modelo acceso al inventario real para basar la recomendacion. Automated Reasoning valida consistencia logica, no exactitud del inventario, y el throughput dedicado ataca el volumen, no la causa de las alucinaciones.</li>'
        '<li><b>Bedrock Agent + Lambda + prompt engineering:</b> Agents con action groups sirve para consultas en vivo, pero esta opcion sigue confiando en prompt engineering para limitar la respuesta; como el modelo redacta el texto final, puede describir o inventar paquetes fuera de lo que devolvio la Lambda; ademas a&ntilde;ade codigo y configuracion a mantener.</li>'
        '<li><b>Kendra + inyeccion manual + cache en DynamoDB:</b> Kendra no es la integracion de vector store nativa de Bedrock Knowledge Bases; inyectar snippets a mano exige codigo de integracion propio; y como las interacciones son muy unicas, el cache en DynamoDB casi no se reutiliza.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Alucinaciones por falta de datos reales = recuperacion aumentada gestionada por Bedrock que ancla la respuesta en la fuente durante la generacion, mas el parametro de configuracion de rendimiento para la latencia. El grounding check de Guardrails solo valida despues de generar.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases (RAG)</a></div>'
    ),
))

# ============================================================
# Q59 - CountVectorizer stopwords/rare words NLP
# ============================================================
cards.append(card(
    question="Un Neural Topic Model (NTM) de SageMaker sugiere tags e incluye <b>stopwords</b> y tambien <b>palabras raras</b> que el equipo considera <b>valiosas</b>. Hay que <b>excluir las stopwords conservando las palabras raras</b>. &iquest;Como refinar el modelo?",
    options=[
        "La funcion CountVectorizer de scikit-learn para preprocesar el texto",
        "Indexar con Amazon OpenSearch filtrando stopwords durante la indexacion",
        "La deteccion de entidades de Amazon Comprehend para limpiar los articulos",
        "SageMaker Processing con un script a medida que elimine stopwords",
    ],
    correct=0,
    key="aip03-q59",
    answer=(
        '<div class="verdict">Correcta: {{L}} - CountVectorizer de scikit-learn.</div>'
        '<p><b>El problema:</b> preprocesar texto para el NTM: quitar stopwords pero <b>preservar</b> las palabras raras que aportan valor a los tags.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>CountVectorizer</b> (scikit-learn) es una herramienta de preprocesamiento de texto pensada justo para esto: acepta una lista de <b>stop_words</b> para eliminarlas y no descarta terminos poco frecuentes salvo que se lo indiques (min_df), asi que puedes conservar las palabras raras. Es el control directo y simple para limpiar el texto antes de entrenar.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Amazon OpenSearch:</b> es busqueda y analitica; puede filtrar stopwords al indexar, pero no esta optimizado para preparar texto de entrenamiento ML conservando palabras raras; su foco son consultas, no limpieza para modelos.</li>'
        '<li><b>Comprehend (entidades):</b> extrae insights (entidades, sentimiento, frases clave), no realiza limpieza de texto tipo remocion de stopwords conservando terminos raros para entrenamiento.</li>'
        '<li><b>SageMaker Processing con script a medida:</b> podria hacerlo, pero es sobredimensionado para una limpieza de texto simple; montar un pipeline de processing a&ntilde;ade complejidad innecesaria frente a un CountVectorizer.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Quitar stopwords y conservar palabras raras al preprocesar texto = la utilidad de vectorizacion de scikit-learn (lista de stop_words y control de frecuencia minima). Un motor de busqueda o un servicio de NLP de insights no son limpieza para ML, y montar un pipeline de processing es excesivo para algo tan simple.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/ntm.html">docs.aws SageMaker Neural Topic Model</a></div>'
    ),
))

# ============================================================
# Q65 - Bedrock on-demand vs Provisioned Throughput routing
# ============================================================
cards.append(card(
    question="Una plataforma documental usa Amazon Kendra y Amazon Bedrock. Maneja ~10,000 consultas simples diarias y 500 complejas de razonamiento multi-paso. Hay que <b>optimizar costo y latencia consistente</b> a la vez, siguiendo el Well-Architected para GenAI. &iquest;Que arquitectura conviene?",
    options=[
        "Claude Haiku on-demand para las simples y Claude Sonnet con Provisioned Throughput para las complejas, con Comprehend custom classification",
        "Un unico Claude Sonnet con Provisioned Throughput a 3 MU, cross-Region y routing por sentimiento de Comprehend",
        "Claude Sonnet on-demand para ambas, query suggestions de Amazon Kendra y response streaming de AWS Lambda",
        "Perfil cross-Region con Haiku y Sonnet, failover por calidad y routing por entidades de Comprehend",
    ],
    correct=0,
    key="aip03-q65",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Haiku on-demand (simples) + Sonnet con Provisioned Throughput (complejas), enrutando con Comprehend custom classification.</div>'
        '<p><b>El problema:</b> dos cargas con perfiles distintos. Las simples son muchas y baratas por token; las complejas son pocas pero criticas y necesitan latencia/throughput consistentes. Hay que optimizar costo Y latencia a la vez.</p>'
        '<p><b>Por que la respuesta sirve:</b> usar <b>Claude Haiku on-demand</b> para las consultas simples de alto volumen aprovecha su precio por token mucho menor y el pago por uso; usar <b>Claude Sonnet con Provisioned Throughput</b> para las pocas consultas complejas garantiza capacidad reservada y latencia consistente en la carga critica. El enrutamiento se hace con <b>custom classification</b> de Comprehend, que si sirve para clasificar el tipo/complejidad de la consulta. Encaja costo + latencia + Well-Architected.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Solo Sonnet a 3 MU + routing por sentimiento:</b> usar Sonnet para todo es costoso cuando Haiku basta para lo simple; y el <b>analisis de sentimiento</b> mide tono emocional, no clasifica complejidad ni sirve para enrutar.</li>'
        '<li><b>Solo Sonnet on-demand + query suggestions + Lambda streaming:</b> on-demand para las complejas introduce variabilidad de latencia y posible throttling; las query suggestions de Kendra operan en la recuperacion y no reducen los tokens de Bedrock; el streaming mejora la latencia percibida pero no resuelve costo ni throughput garantizado.</li>'
        '<li><b>Perfil cross-Region combinando Haiku y Sonnet + failover por calidad + entity recognition:</b> un perfil cross-Region da redundancia geografica del <b>mismo</b> modelo, no combina variantes distintas; el failover por calidad no es nativo de Bedrock; y el reconocimiento de entidades no clasifica complejidad para enrutar.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Alto volumen simple = modelo barato on-demand (Haiku). Pocas consultas criticas = Provisioned Throughput (latencia/throughput garantizados). Clasificar/enrutar por complejidad = Comprehend custom classification (no sentimiento ni entidades).</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html">docs.aws Bedrock Provisioned Throughput</a></div>'
    ),
))


# ============================================================
# Q34 - XGBoost max_depth reducir overfitting
# ============================================================
cards.append(card(
    question="Un modelo XGBoost de Amazon SageMaker tiene <b>AUC de entrenamiento altisimo pero la validacion cae mucho</b> (se&ntilde;al de <b>overfitting</b>). El equipo quiere ajustar hiperparametros para <b>reducir la complejidad del modelo y mejorar la generalizacion</b>. &iquest;Que cambio de hiperparametro ayuda mejor?",
    options=[
        "Aumentar el hiperparametro max_depth para arboles mas profundos",
        "Reducir el parametro min_child_weight para dividir hojas mas facil",
        "Aumentar el parametro colsample_bytree para mas features por arbol",
        "Reducir el hiperparametro max_depth para limitar la complejidad de los arboles",
    ],
    correct=3,
    key="aip03-q34",
    answer=(
        '<div class="verdict">Correcta: {{L}} - reducir max_depth.</div>'
        '<p><b>El problema:</b> el modelo memoriza el entrenamiento (AUC altisimo) pero generaliza mal (validacion baja): es <b>overfitting</b>. En XGBoost, arboles mas profundos = mas complejos = mas propensos a memorizar ruido. Para simplificar y generalizar hay que <b>reducir</b> la complejidad de los arboles.</p>'
        '<p><b>Por que la respuesta sirve:</b> <code>max_depth</code> controla la profundidad maxima de cada arbol. <b>Bajarlo</b> limita cuanto puede ramificar cada arbol, reduciendo la capacidad de memorizar outliers y patrones especificos del entrenamiento. El modelo se vuelve mas simple y suele mejorar la validacion, que es justo el objetivo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Aumentar max_depth:</b> hace cada arbol mas complejo y mas propenso a overfitting; captura mas ruido en vez de patrones generales, asi que empeora justo lo que se quiere corregir.</li>'
        '<li><b>Reducir min_child_weight:</b> baja el minimo de observaciones para crear una hoja, lo que permite mas divisiones y arboles mas profundos, aumentando la complejidad y el overfitting (direccion opuesta a la buscada).</li>'
        '<li><b>Aumentar colsample_bytree:</b> usa mas features por arbol, lo que sube la diversidad de features pero no limita la complejidad; con features dominantes correlacionadas puede incluso overfittear mas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Overfitting en arboles = reducir la complejidad. Bajar la profundidad maxima y subir el minimo de muestras por hoja regularizan; subirlos o dar mas features por arbol va en la direccion contraria.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost_hyperparameters.html">docs.aws hiperparametros de XGBoost</a></div>'
    ),
))

# ============================================================
# Q51 - Regularizacion mas fuerte contra overfitting
# ============================================================
cards.append(card(
    question="Un clasificador de especies en SageMaker AI (imagenes etiquetadas por Amazon Rekognition) logra <b>98% en entrenamiento pero 76% en validacion</b>. El dataset esta limpio y bien dividido; el modelo es <b>demasiado complejo y memoriza</b>. &iquest;Que conviene implementar?",
    options=[
        "Aumentar la complejidad del modelo a&ntilde;adiendo mas capas convolucionales para capturar patrones mas detallados de las imagenes",
        "Ajustar los hiperparametros para introducir una regularizacion mas fuerte y reentrenar el modelo para minimizar el overfitting",
        "Reasignar parte de las muestras de entrenamiento a validacion, cambiando la division a 75% entrenamiento y 25% validacion para lograr mejor balance",
        "Modificar la configuracion de etiquetado de Rekognition para generar menos etiquetas por imagen y simplificar asi la tarea de clasificacion",
    ],
    correct=1,
    key="aip03-q51",
    answer=(
        '<div class="verdict">Correcta: {{L}} - regularizacion mas fuerte y reentrenar.</div>'
        '<p><b>El problema:</b> gran brecha entre entrenamiento (98%) y validacion (76%) con datos ya limpios y bien divididos = <b>overfitting</b> por exceso de complejidad. La <b>regularizacion</b> penaliza esa complejidad para que el modelo generalice.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>regularizacion</b> (por ejemplo dropout, weight decay/L2, early stopping) restringe cuanto puede ajustarse el modelo a los datos de entrenamiento, reduciendo la memorizacion. Subirla via hiperparametros y reentrenar ataca directamente la causa (modelo demasiado complejo) y suele cerrar la brecha con la validacion.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>A&ntilde;adir mas capas convolucionales:</b> aumenta la complejidad del modelo, que ya memoriza; empeoraria el overfitting en vez de reducirlo.</li>'
        '<li><b>Cambiar el split a 75/25:</b> los cientificos ya confirmaron que la division es correcta y balanceada; mover el ratio no ataca el overfitting causado por la complejidad del modelo.</li>'
        '<li><b>Generar menos etiquetas en Rekognition:</b> simplifica en exceso la tarea y reduce la capacidad del modelo de distinguir clases; no aborda el overfitting y puede degradar el desempe&ntilde;o.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Alta precision en entrenamiento y baja en validacion, con datos ya sanos = overfitting: la respuesta es regularizar (dropout, L2, early stopping), no a&ntilde;adir capas, re-dividir datos ni reducir etiquetas.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/machine-learning/latest/dg/model-fit-underfitting-vs-overfitting.html">docs.aws underfitting vs overfitting</a></div>'
    ),
))

# ============================================================
# Q67 - Pinecone RAG + Comprehend + endpoint SageMaker Llama 2
# ============================================================
cards.append(card(
    question="Un chatbot RAG debe consultar una <b>base de datos vectorial</b>, analizar el contexto con Amazon Comprehend y pasarlo a un FM en un <b>endpoint en tiempo real de SageMaker AI</b>. &iquest;Que solucion integra mejor Pinecone para dar contexto al modelo Llama 2?",
    options=[
        "Pinecone para recuperar, Comprehend para el contexto y Llama 2 en un endpoint en tiempo real de SageMaker AI",
        "Pinecone para similitud, Comprehend para el sentimiento y Llama 2 en instancias Amazon EC2",
        "Pinecone para similitud y pasar el contexto a Amazon Lex antes de enviarlo a Llama 2",
        "Pinecone para recuperar y traducir los datos con Amazon Translate antes de Llama 2",
    ],
    correct=0,
    key="aip03-q67",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Pinecone -> Comprehend -> Llama 2 en endpoint de SageMaker.</div>'
        '<p><b>El problema:</b> montar RAG donde la base vectorial recupera contexto, Comprehend lo enriquece (entidades y sentimiento) y un FM en un <b>endpoint en tiempo real de SageMaker</b> genera la respuesta. Hay que respetar cada pieza que pide el escenario.</p>'
        '<p><b>Por que la respuesta sirve:</b> usa <b>Pinecone</b> como base vectorial para indexar y recuperar documentos por similitud (el paso de retrieval de RAG), <b>Comprehend</b> para analizar el contexto recuperado y <b>Llama 2 en un endpoint de inferencia en tiempo real de SageMaker AI</b> para generar, exactamente la arquitectura gestionada que exige el escenario.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Llama 2 en EC2:</b> usa EC2 en vez del endpoint de SageMaker que pide el escenario; EC2 exige montar y gestionar el hosting manualmente, perdiendo el despliegue, escalado y monitoreo gestionados de SageMaker.</li>'
        '<li><b>Pasar por Amazon Lex:</b> Lex es para IA conversacional (reconocer intenciones y gestionar dialogos), no para procesar contexto de RAG hacia un FM generativo; a&ntilde;ade complejidad innecesaria y no aporta el analisis de contexto pedido.</li>'
        '<li><b>Traducir con Amazon Translate:</b> Translate traduce texto entre idiomas, no extrae entidades ni sentimiento; el escenario necesita el enriquecimiento de Comprehend, asi que Translate solo agrega un paso irrelevante.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>RAG = base vectorial para recuperar + enriquecer contexto + generar en el endpoint gestionado indicado. Alojar el FM en EC2 renuncia a lo gestionado; Lex es para intenciones/dialogo; Translate solo traduce, no analiza contexto.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html">docs.aws SageMaker real-time inference endpoints</a></div>'
    ),
))

# ============================================================
# Q69 - SageMaker Canvas scatter plot 4 dimensiones
# ============================================================
cards.append(card(
    question="Un desarrollador quiere ver recomendaciones en <b>cuatro dimensiones</b>: interest score (X) vs conversion (Y), categoria por <b>color</b> e impresiones por el <b>tama&ntilde;o</b> de cada punto. &iquest;Que enfoque cumple mejor?",
    options=[
        "El scatter plot de SageMaker Data Wrangler coloreando los puntos por la tercera feature",
        "El Box Plot de SageMaker Canvas con un patron de relleno para la tercera dimension",
        "El Bar Chart de SageMaker Canvas por categoria con color y altura de barra",
        "El scatter plot de SageMaker Canvas mapeando categoria al color e impresiones al tama&ntilde;o",
    ],
    correct=3,
    key="aip03-q69",
    answer=(
        '<div class="verdict">Correcta: {{L}} - scatter plot de SageMaker Canvas (color + tama&ntilde;o).</div>'
        '<p><b>El problema:</b> mostrar 4 dimensiones en una sola grafica: dos en los ejes (X e Y), una en color y una en tama&ntilde;o de punto. El grafico adecuado es un <b>scatter plot</b> que soporte codificar color y tama&ntilde;o por punto.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>scatter plot de SageMaker Canvas</b> ubica interest score (X) vs conversion (Y), y ademas mapea la tercera dimension (categoria) al <b>color</b> y la cuarta (impresiones) al <b>tama&ntilde;o</b> del punto. Asi las 4 dimensiones quedan en una vista y se detectan facil los productos de alto interes/alta conversion con pocas impresiones (puntos peque&ntilde;os en la zona alta).</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Scatter de Data Wrangler solo con color:</b> solo mapea la tercera dimension al color y no codifica la cuarta (impresiones) por tama&ntilde;o, asi que pierde una dimension clave del analisis.</li>'
        '<li><b>Box Plot:</b> muestra distribuciones estadisticas (mediana, cuartiles), no relaciones entre varias variables continuas, y no mapea color/tama&ntilde;o por punto como un scatter.</li>'
        '<li><b>Bar Chart:</b> los graficos de barras se limitan a pocas dimensiones; no representan interest score y conversion a la vez con claridad ni codifican impresiones como tama&ntilde;o.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>4 dimensiones en una grafica = scatter plot con ejes X/Y mas color y tama&ntilde;o de punto. Los box plots muestran distribuciones y los bar charts pocas dimensiones; codificar color y tama&ntilde;o por punto es propio del scatter.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-visualize.html">docs.aws visualizaciones en SageMaker Canvas</a></div>'
    ),
))

# ============================================================
# CARTAS RESCATADAS (auditoria falsos-COVERED) - prefijo aip03r
# Fuente: decks/aip-c01/dedupe/rescued_exam3.json
# Enfasis en el angulo AVANZADO/feature especifica (tipo_rescate B/AB).
# ============================================================



# ============================================================
# Q12r - Glue DataBrew -> SageMaker Canvas (modelado no-code)
# ============================================================
cards.append(card(
    question="Un equipo tiene transacciones en PostgreSQL y quiere predecir churn a 90 dias. Necesita <b>automatizar la extraccion y preparacion</b> (limpieza, normalizacion, nulos, programada) y que luego <b>analistas de negocio sin cientificos de datos</b> construyan y desplieguen el modelo <b>sin escribir codigo</b>. &iquest;Que opcion cumple mejor?",
    options=[
        "AWS Glue DataBrew para preparar desde PostgreSQL y SageMaker Canvas para el modelo sin codigo",
        "AWS DMS para replicar PostgreSQL a S3 continuo, Glue DataBrew y SageMaker Canvas",
        "AWS Glue DataBrew con reglas de AWS Glue Data Quality y el modelo dentro de DataBrew",
        "AWS Glue DataBrew y luego SageMaker Studio con notebooks para cientificos de datos",
    ],
    correct=0,
    key="aip03r-q12",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Glue DataBrew para preparar y SageMaker Canvas para el modelo no-code.</div>'
        '<p><b>El problema:</b> hay dos requisitos que resolver juntos: (1) preparar datos de forma programada (limpieza, normalizacion, nulos) y (2) que <b>analistas sin conocimientos de ML</b> construyan y desplieguen el modelo <b>sin codigo</b> y hagan predicciones. La clave avanzada es distinguir el servicio de <b>modelado no-code</b>, no solo el de preparacion.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AWS Glue DataBrew</b> es preparacion visual de datos (limpia, normaliza, maneja nulos) y escribe el resultado en S3. <b>SageMaker Canvas</b> es la herramienta <b>no-code</b> de ML: un analista de negocio importa el dataset, construye un modelo de clasificacion (churn) y genera predicciones sin escribir codigo. La combinacion cubre preparacion + modelado no-code, que es justo lo pedido.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>DMS + DataBrew + Canvas:</b> DMS es para replicacion continua o migraciones con minima interrupcion; aqui la preparacion es <b>periodica</b>, no continua, asi que DMS solo agrega complejidad y costo innecesarios.</li>'
        '<li><b>DataBrew + Glue Data Quality (modelo en DataBrew):</b> DataBrew prepara y Data Quality valida reglas, pero <b>ninguno entrena ni despliega modelos</b>; no cumplen el requisito de construir y desplegar un modelo de churn.</li>'
        '<li><b>DataBrew + SageMaker Studio:</b> Studio es un entorno <b>con codigo</b> y notebooks para cientificos de datos; contradice el requisito explicito de que analistas de negocio lo hagan sin codigo.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Analistas de negocio, sin codigo, construir y desplegar un modelo" apunta a la herramienta de ML visual no-code, no a un entorno de notebooks ni a herramientas de solo preparacion o solo validacion. Preparacion programada != replicacion continua.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/canvas.html">docs.aws SageMaker Canvas</a> '
        '<a href="https://docs.aws.amazon.com/databrew/latest/dg/what-is.html">docs.aws Glue DataBrew</a></div>'
    ),
))

# ============================================================
# Q15r - Lake Formation LF-Tags (acceso fino columna/tabla, ABAC)
# ============================================================
cards.append(card(
    question="Una org de salud usa Bedrock Knowledge Bases sobre un data lake en S3 catalogado con AWS Glue. Seguridad quiere acceso fino a nivel <b>base de datos, tabla y columna</b>, <b>por atributos y escalable</b>, sin una politica IAM por combinacion usuario-recurso. &iquest;Que solucion tiene menor operacion?",
    options=[
        "AWS Lake Formation con LF-Tags en bases, tablas y columnas, y permisos por expresiones de LF-Tag",
        "Amazon Macie para descubrir datos sensibles y una AWS Lambda que los mueva a buckets S3 por depto",
        "AWS CloudFormation Guard como politica como codigo sobre el Glue Data Catalog",
        "Politicas IAM basadas en identidad con tags de recurso en los roles de las Knowledge Bases",
    ],
    correct=0,
    key="aip03r-q15",
    answer=(
        '<div class="verdict">Correcta: {{L}} - AWS Lake Formation con LF-Tags a nivel columna.</div>'
        '<p><b>El problema:</b> control de acceso fino a nivel base de datos, tabla y <b>columna</b>, con un modelo <b>por atributos (ABAC)</b> que escale sin escribir una politica IAM por cada usuario y recurso. El angulo avanzado es la <b>feature exacta</b>: LF-Tags de Lake Formation y permisos por expresion de tag.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AWS Lake Formation</b> centraliza permisos del data lake. Los <b>LF-Tags</b> (etiquetas de Lake Formation) se asignan a bases de datos, tablas y <b>columnas</b>; luego se conceden permisos a los principales IAM mediante <b>expresiones de LF-Tag</b>. Es ABAC nativo: se administran atributos, no combinaciones usuario-recurso, y se logra granularidad a nivel columna con baja operacion.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Macie + Lambda + buckets por depto:</b> Macie descubre datos sensibles; no es un sistema de control de acceso del catalogo ni ofrece filtrado a nivel de columna. Mover documentos es fragil y no escala.</li>'
        '<li><b>CloudFormation Guard:</b> valida plantillas de infraestructura como codigo contra reglas de cumplimiento; no intercepta consultas en runtime ni controla acceso a datos.</li>'
        '<li><b>IAM identity-based + tags de recurso:</b> las politicas IAM y los tags de S3 controlan a nivel de bucket u objeto; no dan el control fino de tabla y columna que exige seguridad.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Acceso fino a nivel columna/tabla con modelo por atributos y baja operacion = etiquetas del catalogo del data lake y permisos por expresion de etiqueta. IAM/tags de S3 llegan solo a bucket/objeto; Guard valida IaC; Macie descubre datos, no controla acceso.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html">docs.aws Lake Formation LF-Tags (TBAC)</a></div>'
    ),
))

# ============================================================
# Q18r - SageMaker network isolation mode + VPC endpoint Comprehend
# ============================================================
cards.append(card(
    question="Una empresa entrena e infiere con Amazon SageMaker AI y usa Amazon Comprehend para sentimiento. Por cumplimiento, todo corre en una VPC y se debe <b>bloquear por completo el acceso a Internet</b>. &iquest;Que opcion cumple con MENOR esfuerzo?",
    options=[
        "El network isolation mode de SageMaker AI mas un VPC endpoint para Comprehend en la misma VPC",
        "SageMaker AI en modo VPC only con VPC peering hacia Comprehend en otra VPC",
        "SageMaker AI en modo VPC only con un internet gateway y security groups restrictivos",
        "SageMaker AI en modo VPC only con una network ACL (NACL) que bloquee Internet",
    ],
    correct=0,
    key="aip03r-q18",
    answer=(
        '<div class="verdict">Correcta: {{L}} - network isolation mode + VPC endpoint para Comprehend.</div>'
        '<p><b>El problema:</b> aislamiento total (cero salida a Internet) para entrenamiento e inferencia, y que aun asi SageMaker pueda hablar con Comprehend de forma privada, con el menor esfuerzo. El detalle avanzado es que el modo VPC-only no es lo mismo que el <b>network isolation</b>.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>network isolation mode</b> de SageMaker corta <b>toda</b> conectividad de red del contenedor (no hay ruta a Internet ni a servicios externos), cumpliendo el bloqueo total. Para que Comprehend siga siendo accesible sin salir a Internet, un <b>VPC endpoint</b> (PrivateLink) en la misma VPC lleva el trafico por la red de AWS. Es la combinacion mas directa y de menor esfuerzo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>VPC only + VPC peering:</b> el peering agrega ruteo, security groups y mantenimiento; es facil dejar sin querer una via de acceso, y no equivale al aislamiento de red completo.</li>'
        '<li><b>VPC only + internet gateway:</b> tener un internet gateway contradice el requisito de bloquear todo acceso a Internet; los security groups por si solos no garantizan aislamiento total.</li>'
        '<li><b>VPC only + NACL:</b> las NACL no aislan por completo (el trafico puede fluir por otras rutas) y esta opcion no usa un VPC endpoint para llegar a Comprehend de forma privada.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Bloquear por completo todo acceso externo" = modo de aislamiento de red (corta toda la red), que es mas fuerte que el modo solo-VPC. Para servicios AWS sin Internet, usa un endpoint de VPC; peering, IGW o NACL no dan aislamiento total.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/mkt-algo-model-internet-free.html">docs.aws SageMaker network isolation</a></div>'
    ),
))



# ============================================================
# Q19r - VPC endpoints privados para notebook + S3
# ============================================================
cards.append(card(
    question="Una minorista usa notebooks de Amazon SageMaker AI y Amazon Comprehend sobre rese&ntilde;as en Amazon S3. Por sensibilidad, todo debe quedar en una VPC y <b>toda la comunicacion ocurrir por la red de AWS</b>, nunca por Internet. &iquest;Que solucion cumple?",
    options=[
        "El notebook en una subred privada con VPC endpoints privados para SageMaker AI y S3",
        "El notebook en una subred privada con ruta a un internet gateway y un proxy externo a S3",
        "El notebook en una subred privada con VPC peering hacia otra VPC donde S3 sea accesible",
        "El notebook en una subred privada con un NAT gateway hacia S3 restringido a ciertos buckets",
    ],
    correct=0,
    key="aip03r-q19",
    answer=(
        '<div class="verdict">Correcta: {{L}} - subred privada con VPC endpoints para SageMaker y S3.</div>'
        '<p><b>El problema:</b> que el notebook alcance S3 (y SageMaker) sin que el trafico salga jamas a Internet publico. El detalle avanzado es como lograr conectividad <b>privada</b> a servicios AWS: con VPC endpoints, no con peering ni NAT.</p>'
        '<p><b>Por que la respuesta sirve:</b> colocar el notebook en una <b>subred privada</b> y crear <b>VPC endpoints</b> para SageMaker AI y para S3 hace que el trafico viaje por la red interna de AWS (PrivateLink / gateway endpoint de S3), sin pasar por Internet. Cumple el requisito de comunicacion 100% privada.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Internet gateway + proxy externo:</b> enrutar por un internet gateway y un proxy expone el trafico al Internet publico, violando el requisito de red privada.</li>'
        '<li><b>VPC peering:</b> el peering no da acceso privado a servicios como S3; seguiria necesitando endpoints publicos salvo que se configuren VPC endpoints, que esta opcion no garantiza.</li>'
        '<li><b>NAT gateway:</b> el NAT gateway enruta hacia el Internet publico; aunque se restrinjan buckets, la ruta no cumple la exigencia de red privada de AWS.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Todo por la red de AWS, sin Internet" para acceder a servicios AWS = endpoints de VPC (PrivateLink; gateway endpoint para S3). Un NAT gateway y un internet gateway siguen usando Internet publico; el peering no habilita acceso privado a servicios administrados.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/interface-vpc-endpoint.html">docs.aws VPC endpoints para SageMaker</a></div>'
    ),
))

# ============================================================
# Q22r - Politica IAM condicionada a VPC endpoint sobre acciones sagemaker
# ============================================================
cards.append(card(
    question="Un equipo tiene notebooks de Amazon SageMaker AI en una VPC aislada con VPC interface endpoints. Descubre que usuarios <b>fuera de la VPC</b> aun acceden por Internet. &iquest;Como limitar el acceso a <b>solo usuarios autorizados via la VPC</b>?",
    options=[
        "Una politica IAM que permita sagemaker:CreatePresignedNotebookInstanceUrl y sagemaker:DescribeNotebookInstance solo desde los VPC interface endpoints",
        "Actualizar el security group de las instancias notebook para restringir el trafico entrante solo a los bloques CIDR de la VPC",
        "Configurar VPC Traffic Mirroring para capturar el trafico e identificar accesos no autorizados",
        "Aplicar VPC Endpoint Policies para controlar que usuarios o servicios IAM pueden acceder a SageMaker AI a traves del interface endpoint",
    ],
    correct=0,
    key="aip03r-q22",
    answer=(
        '<div class="verdict">Correcta: {{L}} - politica IAM condicionada al VPC endpoint sobre acciones sagemaker.</div>'
        '<p><b>El problema:</b> el acceso al notebook se obtiene llamando a la <b>API</b> de SageMaker (que genera la URL prefirmada); aunque la red este aislada, si la API se puede invocar desde Internet el usuario entra. El angulo avanzado es una decision de dise&ntilde;o <b>IAM a nivel de accion con condicion de VPC endpoint</b>, no solo aislamiento de red.</p>'
        '<p><b>Por que la respuesta sirve:</b> una <b>politica IAM</b> que permita <code>sagemaker:CreatePresignedNotebookInstanceUrl</code> y <code>sagemaker:DescribeNotebookInstance</code> <b>solo cuando la peticion llega por el VPC endpoint</b> (condicion tipo <code>aws:sourceVpce</code>) cierra el acceso desde fuera: sin la URL prefirmada no hay entrada al notebook, y esa accion queda restringida al endpoint de la VPC.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Security group por CIDR:</b> restringe a nivel de interfaz de red de las instancias, pero no impide invocar la API de SageMaker por Internet para obtener la URL de acceso.</li>'
        '<li><b>VPC Traffic Mirroring:</b> es monitoreo: captura e inspecciona trafico e identifica intentos, pero no bloquea ni restringe el acceso.</li>'
        '<li><b>VPC Endpoint Policies:</b> controlan quien usa el endpoint hacia el servicio, pero no restringen especificamente el acceso a las instancias notebook via la accion de URL prefirmada como lo hace la condicion IAM sobre esa accion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cerrar el acceso al notebook = restringir la ACCION de la API que genera la URL prefirmada con una condicion de origen por VPC endpoint. Los security groups filtran red, el traffic mirroring solo observa, y la endpoint policy no ata la accion a nivel de usuario/role como la politica IAM condicionada.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-interface-endpoint.html">docs.aws restringir acceso a notebooks via VPC endpoint</a></div>'
    ),
))

# ============================================================
# Q26r - Data augmentation para invarianza de orientacion
# ============================================================
cards.append(card(
    question="Un clasificador de imagenes con Amazon Rekognition Custom Labels comete mas del 75% de sus errores con pandas <b>boca abajo</b> (sensibilidad a la orientacion). Deben mejorar el reconocimiento <b>sin recolectar un dataset nuevo ni modificar mucho el pipeline</b>. &iquest;Que enfoque es el mas efectivo?",
    options=[
        "Ampliar el dataset de entrenamiento aplicando tecnicas de data augmentation como rotacion, volteo (flip) y escalado de las imagenes",
        "Aplicar pasos de preprocesamiento de normalizacion para que todas las imagenes compartan una escala y una distribucion de brillo comunes",
        "Aumentar el numero de epochs de entrenamiento para prolongar la optimizacion y reforzar la representacion de features dentro del dataset existente",
        "Aplicar transfer learning reutilizando las capas base de un modelo de vision probado",
    ],
    correct=0,
    key="aip03r-q26",
    answer=(
        '<div class="verdict">Correcta: {{L}} - data augmentation (rotacion, flip, escalado).</div>'
        '<p><b>El problema:</b> el modelo falla especificamente cuando el panda esta rotado (boca abajo). Es un problema de <b>falta de variedad de orientaciones</b> en los datos, no de escala/brillo, epochs ni arquitectura. El detalle avanzado es reconocer que la tecnica correcta es la <b>aumentacion de datos</b> que crea variantes rotadas.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>data augmentation</b> genera copias transformadas (rotacion, flip, escalado) a partir de las imagenes existentes. Al exponer al modelo a pandas en muchas orientaciones durante el entrenamiento, aprende <b>invarianza rotacional</b> y deja de fallar con las imagenes boca abajo, sin recolectar datos nuevos ni cambiar el pipeline.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Normalizacion:</b> estandariza intensidad y brillo para estabilizar el entrenamiento, pero no ense&ntilde;a a reconocer objetos en distintas orientaciones.</li>'
        '<li><b>Mas epochs:</b> itera mas sobre los mismos datos; no agrega variedad y puede incluso sobreajustar a los patrones existentes sin ganar invarianza a la rotacion.</li>'
        '<li><b>Transfer learning:</b> acelera y reutiliza features aprendidas, pero no supera el sesgo de orientacion cuando el dataset carece de esa diversidad; no reemplaza la aumentacion que expone multiples orientaciones.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Errores ligados a orientacion/pose con dataset limitado = aumentar datos con transformaciones geometricas (rotacion, flip, escalado) para lograr invarianza. Normalizacion, mas epochs o transfer learning atacan otros problemas, no la falta de variedad de orientaciones.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/training-model.html">docs.aws Rekognition Custom Labels entrenamiento</a></div>'
    ),
))



# ============================================================
# Q37r - SageMaker Ground Truth Plus HITL integrado al pipeline
# ============================================================
cards.append(card(
    question="Un sistema de IA generativa resume historias clinicas. Antes del despliegue necesita un proceso <b>robusto para que profesionales de salud revisen y corrijan</b> los resumenes, que <b>escale a grandes volumenes</b> y se <b>integre con los pipelines de SageMaker</b> para reentrenamiento y despliegue. &iquest;Que enfoque cumple mejor?",
    options=[
        "SageMaker Ground Truth Plus como flujo human-in-the-loop integrado al pipeline de SageMaker",
        "SageMaker Model Monitor para marcar resumenes de baja confianza y guardarlos en S3",
        "La knowledge base de Amazon Bedrock para enriquecer el dataset de entrenamiento",
        "Amazon Augmented AI (A2I) para un proceso de revision humana a escala",
    ],
    correct=0,
    key="aip03r-q37",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SageMaker Ground Truth Plus (HITL gestionado) integrado al pipeline.</div>'
        '<p><b>El problema:</b> se necesita revision y correccion experta (human-in-the-loop, HITL) a gran escala, integrada al pipeline de SageMaker para retraining y despliegue. El angulo avanzado es elegir el servicio <b>gestionado de HITL y etiquetado a escala</b> pensado para industrias reguladas, no un monitor ni una revision puntual.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>SageMaker Ground Truth Plus</b> ofrece un flujo <b>human-in-the-loop gestionado</b>: operaciones de revision y etiquetado escalables con expertos, ideal para volumenes grandes y entornos regulados. Se integra con el pipeline de SageMaker, asi las correcciones alimentan el reentrenamiento y el despliegue de forma continua.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Model Monitor:</b> vigila drift, calidad y sesgo de modelos desplegados; puede marcar baja confianza, pero no provee un flujo estructurado de validacion y correccion humana.</li>'
        '<li><b>Bedrock knowledge base:</b> enriquece al modelo con conocimiento externo (RAG); no garantiza la correccion clinica ni el cumplimiento, que exigen revision humana explicita.</li>'
        '<li><b>Amazon A2I:</b> habilita revision humana en tareas puntuales de inferencia; Ground Truth Plus extiende eso con revision gestionada y operaciones de etiquetado escalables, mas adecuadas al volumen y a la integracion con retraining pedida.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Revision y correccion experta a gran escala, en industria regulada e integrada al reentrenamiento = servicio gestionado de HITL/etiquetado. El monitor solo detecta, la knowledge base solo enriquece y la revision puntual no cubre operaciones de etiquetado a escala.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-ground-truth-plus.html">docs.aws SageMaker Ground Truth Plus</a></div>'
    ),
))

# ============================================================
# Q38r - SageMaker Autopilot + Clarify (importancia de features)
# ============================================================
cards.append(card(
    question="Un equipo quiere predecir churn con 10,000 registros y 1,500 atributos. Busca una forma <b>automatizada</b> de construir el modelo en Amazon SageMaker AI y ademas <b>identificar las features mas relevantes</b>, con minimo esfuerzo. &iquest;Que solucion cumple mejor?",
    options=[
        "SageMaker Autopilot para el modelo de clasificacion de churn y SageMaker Clarify para las features influyentes",
        "SageMaker Ground Truth para etiquetar y un modelo TensorFlow a medida analizando pesos",
        "El algoritmo k-means en SageMaker AI para agrupar clientes por patrones de compra",
        "SageMaker Data Wrangler para entrenar y su visualizacion rapida de modelo para importancia",
    ],
    correct=0,
    key="aip03r-q38",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SageMaker Autopilot + SageMaker Clarify.</div>'
        '<p><b>El problema:</b> dos objetivos a la vez: (1) construir el modelo de clasificacion de forma <b>automatizada</b> (AutoML) y (2) explicar que features pesan mas. El detalle avanzado es la combinacion exacta Autopilot + Clarify para importancia de features.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>SageMaker Autopilot</b> es AutoML: entrena y ajusta automaticamente un modelo de clasificacion (churn) con minimo esfuerzo. <b>SageMaker Clarify</b> aporta explicabilidad (atribucion/importancia de features), indicando cuales influyen mas en la prediccion. Juntos cubren automatizacion e interpretabilidad.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Ground Truth + TensorFlow a medida:</b> exige etiquetado manual y construir/ajustar un modelo propio y analizar pesos a mano; es lo contrario de automatizado.</li>'
        '<li><b>k-means:</b> es no supervisado (clustering), no clasificacion; no predice churn directamente y necesitaria pasos y supuestos adicionales.</li>'
        '<li><b>Data Wrangler:</b> es preparacion y visualizacion de datos; no entrena de forma automatizada ni da atribucion de features de extremo a extremo como Autopilot + Clarify.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Automatico" + "que features influyen" = AutoML para el modelo y la herramienta de explicabilidad para la importancia de features. El etiquetado y el modelo a medida no son automaticos, el clustering no clasifica y la herramienta de preparacion no entrena de punta a punta.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-feature-attribute.html">docs.aws SageMaker Clarify atribucion de features</a></div>'
    ),
))

# ============================================================
# Q39r - IAM role del notebook con permisos S3 (Get/Put/List)
# ============================================================
cards.append(card(
    question="Un desarrollador entrena en Amazon SageMaker AI con datos en Amazon S3 y debe guardar artefactos y logs en <b>otro bucket S3</b>. Necesita dar a la instancia notebook permisos de <b>lectura y escritura</b> sobre esos buckets, de forma segura y con buenas practicas. &iquest;Que enfoque usar?",
    options=[
        "Una politica en el rol IAM del notebook con s3:GetObject, s3:PutObject y s3:ListBucket",
        "Una politica de bucket S3 que permita al notebook, por su ARN, Get/Put/ListBucket",
        "Un S3 access point para el notebook limitado a s3:GetObject, s3:PutObject y s3:ListBucket",
        "Federacion de identidades IAM para que el notebook asuma un rol federado temporal",
    ],
    correct=0,
    key="aip03r-q39",
    answer=(
        '<div class="verdict">Correcta: {{L}} - politica en el rol IAM del notebook con Get/Put/List.</div>'
        '<p><b>El problema:</b> dar a un <b>servicio de AWS</b> (la instancia notebook) permisos de lectura y escritura sobre buckets concretos, siguiendo la buena practica de comunicacion servicio-a-servicio. El detalle avanzado: incluir <code>s3:PutObject</code> (escritura) y usar el <b>rol IAM del notebook</b>, no politicas de bucket ni federacion.</p>'
        '<p><b>Por que la respuesta sirve:</b> adjuntar una <b>politica al rol IAM</b> asociado a la instancia con <code>s3:GetObject</code>, <code>s3:PutObject</code> y <code>s3:ListBucket</code> concede lectura, escritura y listado sobre los buckets designados. Es el patron recomendado, mantenible y de least privilege para que un servicio de AWS acceda a S3.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Bucket policy por ARN:</b> las politicas de bucket sirven mejor para acceso entre cuentas o permisos amplios; para acceso servicio-a-servicio, el rol IAM es mas mantenible y seguro.</li>'
        '<li><b>S3 access point:</b> los access points estan pensados para gestionar acceso a datasets compartidos a escala/multi-tenant; para una sola instancia, el rol IAM es mas directo y sin complejidad extra.</li>'
        '<li><b>Federacion de identidades IAM:</b> es para identidades externas (usuarios corporativos, apps de terceros), no para servicios AWS como SageMaker, que deben usar su rol IAM.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Un servicio de AWS que necesita leer y escribir en S3 = permisos en su ROL IAM (Get/Put/List). Las bucket policies encajan en cross-account, los access points en datasets compartidos y la federacion en identidades externas, no en servicios AWS.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html">docs.aws roles IAM de SageMaker</a></div>'
    ),
))



# ============================================================
# Q40r - SSE-KMS + IAM + CloudWatch para flujo ML seguro y observable
# ============================================================
cards.append(card(
    question="Una financiera entrena deteccion de fraude en Amazon SageMaker AI sobre historico en S3. Debe cifrar en transito y reposo, <b>controlar estrictamente el acceso</b> y <b>monitorear el desempe&ntilde;o del modelo</b>. &iquest;Que solucion cumple?",
    options=[
        "Cifrado en reposo con SSE-KMS, roles IAM para el acceso y Amazon CloudWatch para las metricas del modelo",
        "Cifrado en reposo con SSE-S3, roles IAM para el acceso y Amazon Macie para datos sensibles",
        "Modelo y metadata en DynamoDB, VPC endpoints entre SageMaker, DynamoDB y Kinesis, y AWS CloudTrail para monitorear el acceso y la actividad",
        "Amazon Data Firehose para ingerir, catalogo con AWS Glue, CloudWatch para el modelo y IAM",
    ],
    correct=0,
    key="aip03r-q40",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SSE-KMS + roles IAM + CloudWatch para el desempe&ntilde;o.</div>'
        '<p><b>El problema:</b> tres requisitos juntos: cifrado auditable en reposo, control estricto de acceso y <b>monitoreo del desempe&ntilde;o del modelo</b>. El detalle avanzado es emparejar cada requisito con el servicio correcto: SSE-KMS (no SSE-S3), IAM y CloudWatch (metricas de modelo), no CloudTrail (que es de actividad API).</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>SSE-KMS</b> cifra en reposo con clave gestionada y auditable (mejor que SSE-S3 para cumplimiento en finanzas). Los <b>roles IAM</b> controlan el acceso a datos y modelo. <b>Amazon CloudWatch</b> es el servicio para <b>metricas de desempe&ntilde;o</b> del modelo y logging, cubriendo el monitoreo continuo pedido.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>SSE-S3 + Macie:</b> SSE-S3 no da control de clave del cliente ni la auditabilidad de SSE-KMS; y Macie descubre datos sensibles (PII), no monitorea el desempe&ntilde;o del modelo.</li>'
        '<li><b>Modelo en DynamoDB + CloudTrail:</b> DynamoDB no es para artefactos grandes (van a S3); y CloudTrail registra actividad de API, no metricas de desempe&ntilde;o del modelo.</li>'
        '<li><b>Data Firehose + Glue:</b> Firehose y Glue no son necesarios aqui (SageMaker ingiere directo de S3/Kinesis); ademas la opcion no menciona cifrado KMS para el requisito de cumplimiento.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cifrado auditable en reposo = cifrado del lado del servidor con clave gestionada y auditable, no con la clave por defecto del servicio. "Monitorear el desempe&ntilde;o del modelo" = servicio de metricas, no el de registro de actividad de la API.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/monitoring-cloudwatch.html">docs.aws SageMaker con CloudWatch</a></div>'
    ),
))

# ============================================================
# Q41r - TrainingJobEarlyStoppingType=AUTO (early stopping en AMT)
# ============================================================
cards.append(card(
    question="Un desarrollador usa SageMaker automatic model tuning (AMT) y nota que <b>algunos training jobs corren de mas</b> cuando la accuracy de validacion deja de mejorar temprano. Quiere reducir el tiempo total dejando que <b>SageMaker decida automaticamente cuando detener</b> los jobs que rinden mal. &iquest;Que configuracion resuelve esto?",
    options=[
        "Habilitar el early stopping poniendo el parametro TrainingJobEarlyStoppingType en el valor AUTO en la configuracion del tuning job",
        "Modificar la metrica objetivo del tuning con un umbral de validacion mas estricto",
        "Aumentar el parametro MaxRuntimeInSeconds en la configuracion del tuning para dar mas tiempo a que los training jobs con bajo rendimiento completen",
        "Configurar la estrategia de tuning para usar optimizacion bayesiana, asegurando que todos los training jobs completen por entero antes de evaluar resultados",
    ],
    correct=0,
    key="aip03r-q41",
    answer=(
        '<div class="verdict">Correcta: {{L}} - TrainingJobEarlyStoppingType = AUTO.</div>'
        '<p><b>El problema:</b> cortar automaticamente los training jobs que ya no mejoran para ahorrar computo y tiempo <b>durante</b> el tuning. El detalle avanzado es el <b>parametro y valor exactos</b> del early stopping en AMT, no un cambio de metrica ni de estrategia.</p>'
        '<p><b>Por que la respuesta sirve:</b> poner <code>TrainingJobEarlyStoppingType = AUTO</code> activa el <b>early stopping</b> del automatic model tuning: SageMaker detiene por si mismo los jobs cuya metrica objetivo deja de mejorar, reduciendo computo y tiempo total sin intervencion manual.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Umbral de metrica mas estricto:</b> solo cambia como se rankean los modelos <b>despues</b> de entrenar; no detiene jobs en curso ni reduce computo durante el tuning.</li>'
        '<li><b>Aumentar MaxRuntimeInSeconds:</b> extiende cuanto puede correr cada job, justo lo contrario de reducir el tiempo desperdiciado.</li>'
        '<li><b>Optimizacion bayesiana:</b> decide que combinacion de hiperparametros probar; forzar que todos completen no ahorra computo ni implementa la parada temprana.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Que SageMaker decida cuando detener jobs que no mejoran" en AMT = habilitar el parametro de early stopping en su valor automatico. Cambiar la metrica solo afecta el ranking posterior; subir el runtime alarga; la estrategia de busqueda no para jobs.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-early-stopping.html">docs.aws AMT early stopping</a></div>'
    ),
))

# ============================================================
# Q42r - Estrategia Hyperband (parada temprana + reasignacion)
# ============================================================
cards.append(card(
    question="Un equipo usa SageMaker Automatic Model Tuning (AMT) y muchos jobs siguen corriendo pese a mal desempe&ntilde;o temprano, gastando GPU. Quieren una <b>estrategia que detenga los trials debiles y reasigne recursos</b> a los prometedores. &iquest;Que estrategia deben emplear?",
    options=[
        "Utilizar la estrategia Hyperband en SageMaker AI para asignar recursos de forma eficiente y detener temprano los trials debiles",
        "Implementar optimizacion bayesiana para refinar iterativamente el espacio de busqueda de hiperparametros",
        "Usar grid search para evaluar de forma exhaustiva todas las combinaciones posibles de hiperparametros sin parada temprana",
        "Utilizar random search para muestrear combinaciones de hiperparametros de forma uniforme en todo el espacio de busqueda",
    ],
    correct=0,
    key="aip03r-q42",
    answer=(
        '<div class="verdict">Correcta: {{L}} - estrategia Hyperband.</div>'
        '<p><b>El problema:</b> no basta con "buscar bien" hiperparametros: hay que <b>matar trials debiles temprano</b> y reasignar el computo a los buenos para ahorrar GPU. El detalle avanzado es la sub-feature especifica de AMT: la estrategia <b>Hyperband</b>, frente a bayesian/grid/random.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Hyperband</b> es una estrategia de AMT que combina asignacion adaptativa de recursos con <b>parada temprana</b>: evalua muchas configuraciones con poco presupuesto, elimina las debiles y concentra recursos en las prometedoras. Reduce GPU desperdiciada, que es justo el objetivo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Optimizacion bayesiana:</b> explora eficientemente el espacio segun resultados previos, pero <b>no</b> termina trials automaticamente ni reasigna recursos de forma dinamica.</li>'
        '<li><b>Grid search:</b> prueba todas las combinaciones y cada job corre hasta el final; ineficiente y sin parada temprana.</li>'
        '<li><b>Random search:</b> muestrea al azar; puede hallar buenas configuraciones, pero tampoco detiene jobs debiles ni gestiona recursos de forma adaptativa.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Detener trials debiles y reasignar recursos" = la estrategia de tuning con asignacion adaptativa y parada temprana. La busqueda bayesiana, la exhaustiva y la aleatoria no matan jobs temprano ni reparten computo de forma dinamica.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-how-it-works.html">docs.aws estrategias de AMT (Hyperband)</a></div>'
    ),
))



# ============================================================
# Q43r - Warm start TRANSFER_LEARNING + early stopping (AMT)
# ============================================================
cards.append(card(
    question="Un equipo reentrena un modelo de regresion en SageMaker AI. Guardo buenos hiperparametros de un tuning AMT previo, pero el nuevo dataset es <b>mas grande y con distribucion distinta</b>. Exigen que el tuning <b>no empiece desde cero</b> (presupuesto limitado) y que <b>se detenga solo</b> si la validation loss deja de mejorar. &iquest;Que configuracion usar?",
    options=[
        "Warm start tipo TRANSFER_LEARNING para importar el tuning previo, y AMT Early Stopping",
        "Warm start con el modo IDENTICAL_DATA_AND_ALGORITHM y AMT Early Stopping",
        "Un tuning job con espacio ampliado y optimizacion bayesiana desde cero",
        "Un nuevo tuning job con estrategia Hyperband, sin usar el warm start previo",
    ],
    correct=0,
    key="aip03r-q43",
    answer=(
        '<div class="verdict">Correcta: {{L}} - warm start TRANSFER_LEARNING + early stopping.</div>'
        '<p><b>El problema:</b> reutilizar el tuning anterior (no partir de cero) pese a que <b>cambiaron los datos</b>, y parar solo cuando ya no mejore. El detalle avanzado son las sub-features exactas: el <b>tipo de warm start</b> correcto cuando cambia el dataset, mas el early stopping.</p>'
        '<p><b>Por que la respuesta sirve:</b> el warm start tipo <b>TRANSFER_LEARNING</b> importa el conocimiento del tuning previo <b>aunque los datos y el algoritmo hayan cambiado</b>, arrancando desde ese aprendizaje en vez de cero (respeta el presupuesto). El <b>AMT Early Stopping</b> corta la exploracion cuando la validation loss deja de mejorar, sin intervencion manual.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>IDENTICAL_DATA_AND_ALGORITHM:</b> ese modo asume el <b>mismo</b> dataset y algoritmo; como el nuevo dataset tiene otra distribucion y tama&ntilde;o, es invalido y daria resultados subo&ptimos o errores.</li>'
        '<li><b>Espacio ampliado + bayesiana desde cero:</b> ignora el requisito de reutilizar y de presupuesto limitado; empezar de cero es ineficiente cuando hay resultados previos utiles.</li>'
        '<li><b>Hyperband sin warm start:</b> mejora la eficiencia con parada temprana, pero igual empieza desde cero y no aprovecha el tuning anterior, gastando computo de mas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Reutilizar tuning previo cuando CAMBIA el dataset = warm start de transferencia (el modo de "datos identicos" no aplica). Anade parada temprana para cortar cuando ya no mejora. Empezar de cero (bayesiana/Hyperband solos) desperdicia presupuesto.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-warm-start.html">docs.aws AMT warm start</a></div>'
    ),
))

# ============================================================
# Q44r - Amazon Comprehend toxicity detection
# ============================================================
cards.append(card(
    question="Una plataforma social quiere <b>detectar lenguaje toxico en tiempo real</b> (odio, acoso, amenazas), integrarse con su pipeline de SageMaker y dar <b>puntajes de confianza</b> para bloquear o revisar. &iquest;Que solucion gestionada detecta toxicidad en texto?",
    options=[
        "Utilizar la deteccion de toxicidad de Amazon Comprehend para identificar lenguaje abusivo o da&ntilde;ino en el texto",
        "Utilizar el analisis de sentimiento de Amazon Comprehend para detectar comentarios negativos y bloquear el contenido automaticamente",
        "Usar Amazon Translate para convertir el texto a otro idioma antes de moderar y asi reducir el contenido ofensivo",
        "Usar Amazon Bedrock para hacer fine-tuning de un modelo fundacional orientado a la comprension general del lenguaje",
    ],
    correct=0,
    key="aip03r-q44",
    answer=(
        '<div class="verdict">Correcta: {{L}} - deteccion de toxicidad de Amazon Comprehend.</div>'
        '<p><b>El problema:</b> se quiere una capacidad <b>gestionada</b> especifica para <b>toxicidad</b> (odio, acoso, amenazas) con puntajes de confianza, no un analisis de tono generico. El detalle avanzado es distinguir la feature exacta de <b>toxicity detection</b> frente al sentimiento.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>toxicity detection de Amazon Comprehend</b> es un clasificador gestionado que identifica lenguaje abusivo/da&ntilde;ino y devuelve puntajes de confianza por categoria. Se integra al pipeline y permite bloquear o enviar a revision segun el score, cubriendo justo el requisito.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Sentimiento de Comprehend:</b> clasifica el tono (positivo/negativo/neutral); no detecta toxicidad, asi que se perderia contenido da&ntilde;ino o marcaria negativos no toxicos.</li>'
        '<li><b>Amazon Translate:</b> solo traduce entre idiomas; no detecta ni reduce contenido ofensivo.</li>'
        '<li><b>Fine-tuning en Bedrock:</b> mejora comprension general del lenguaje, pero no detecta toxicidad "de fabrica"; requeriria desarrollo a medida frente a un servicio gestionado.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Deteccion gestionada de lenguaje toxico con puntajes por categoria = la feature de toxicity detection del servicio de NLP, no el analisis de sentimiento (que solo da el tono) ni traducir o hacer fine-tuning generico.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/toxicity-detection.html">docs.aws Comprehend toxicity detection</a></div>'
    ),
))

# ============================================================
# Q47r - SAML a IAM Identity Center + permission sets + SCP (Bedrock RBAC)
# ============================================================
cards.append(card(
    question="Una empresa global usa modelos Titan en Amazon Bedrock con AWS Organizations (una OU por departamento). Exige least privilege, RBAC estricto con <b>IdP centralizado</b>, que solo equipos aprobados invoquen ciertos FMs y que <b>todo se registre</b>. &iquest;Que accion es la mas segura?",
    options=[
        "Federacion SAML a AWS IAM Identity Center, permission sets por OU y una SCP que limite los modelos aprobados",
        "Amazon Cognito user pools por departamento, politicas IAM en los grupos y CloudWatch Logs",
        "Politicas IAM por tags con tags de recurso en los modelos Bedrock y AWS Config para las OUs",
        "Politicas IAM con Bedrock Guardrails, reglas de EventBridge que alerten y AWS CloudTrail",
    ],
    correct=0,
    key="aip03r-q47",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SAML a IAM Identity Center + permission sets por OU + SCP.</div>'
        '<p><b>El problema:</b> gobernanza multi-cuenta con IdP central, RBAC por departamento, restringir que FMs se invocan y auditar todo. El detalle avanzado es combinar identidad de fuerza laboral federada + <b>permission sets</b> por OU + <b>SCP</b> como barrera organizacional.</p>'
        '<p><b>Por que la respuesta sirve:</b> la <b>federacion SAML a AWS IAM Identity Center</b> integra el IdP corporativo y da identidad de fuerza laboral en todas las cuentas. Los <b>permission sets</b> por OU implementan RBAC least-privilege autorizando solo ciertas invocaciones de modelos. Una <b>SCP</b> pone el limite organizacional que impide usar modelos fuera del conjunto aprobado. La auditoria de invocaciones se cubre con el registro de API.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Cognito + grupos:</b> Cognito autentica usuarios finales de aplicaciones, no identidades de fuerza laboral multi-cuenta; no se integra con Organizations ni impone gobernanza por OU.</li>'
        '<li><b>IAM + tags de sesion en modelos:</b> los modelos fundacionales de Bedrock no admiten tag-based authorization; sin recursos etiquetables no se puede restringir por tags, y Config solo observa configuracion.</li>'
        '<li><b>IAM + Guardrails + EventBridge:</b> los Guardrails filtran contenido/seguridad, no controlan que equipo puede invocar cada modelo; EventBridge solo alerta, no bloquea, y IAM por si solo no aplica RBAC a nivel de toda la organizacion.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Gobernanza multi-cuenta con IdP central y RBAC = federacion al servicio de identidad de fuerza laboral con permission sets, mas una politica de control de servicios como barrera de la organizacion. Cognito es para apps, los guardrails filtran contenido y los tags no aplican a los FMs de Bedrock.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html">docs.aws IAM Identity Center permission sets</a></div>'
    ),
))



# ============================================================
# Q49r - Preprocesamiento: excluir ID + codificar label a numerico
# ============================================================
cards.append(card(
    question="Un proveedor de pagos prepara datos para deteccion de fraude. Cada registro tiene client_identifier (string), account_category, payment_value, account_duration y operation_status (&quot;legitimate&quot;/&quot;suspicious&quot;). Antes de entrenar con <b>algoritmos integrados de SageMaker</b> necesita una <b>etiqueta valida</b> para clasificacion. &iquest;Que preprocesamiento hacer?",
    options=[
        "Excluir el campo client_identifier y codificar operation_status en etiquetas numericas, y luego iniciar el entrenamiento del modelo en SageMaker AI",
        "Conservar todos los campos y usar Comprehend para transformar operation_status en scores numericos basados en sentimiento antes de iniciar el training job",
        "Excluir tanto client_identifier como operation_status para reducir la correlacion de datos e iniciar el entrenamiento con los atributos restantes",
        "Convertir todos los campos a string para consistencia y luego entrenar en SageMaker AI",
    ],
    correct=0,
    key="aip03r-q49",
    answer=(
        '<div class="verdict">Correcta: {{L}} - excluir el ID y codificar la etiqueta a numerico.</div>'
        '<p><b>El problema:</b> preparar los datos para <b>algoritmos integrados</b> (que esperan features numericas) y conservar una <b>etiqueta valida</b> para clasificacion supervisada. El detalle avanzado es saber que campo se descarta (el identificador) y que se debe <b>codificar</b> (la etiqueta de clase).</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>client_identifier</b> es un identificador sin valor predictivo (se excluye). El <b>operation_status</b> es la etiqueta de clase categorica: se <b>codifica a numerico</b> (legitimate/suspicious a 0/1) para que los algoritmos integrados la usen como target valido. Asi el dataset queda compatible y con label correcta.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Comprehend para score de sentimiento del status:</b> operation_status ya es una etiqueta categorica estructurada; Comprehend es para NLP sobre texto, no aporta nada y desvirtua la etiqueta.</li>'
        '<li><b>Excluir tambien operation_status:</b> eliminar la etiqueta destruye el target; sin ella no hay clasificacion supervisada posible.</li>'
        '<li><b>Convertir todo a string:</b> los algoritmos integrados esperan numeros; pasar todo a string degrada el desempe&ntilde;o e impide usar features numericas como payment_value.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Para algoritmos integrados: descarta identificadores sin poder predictivo y codifica la etiqueta categorica a numerico; nunca elimines la columna objetivo ni conviertas features numericas a texto.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html">docs.aws algoritmos integrados de SageMaker</a></div>'
    ),
))

# ============================================================
# Q52r - Re-baseline de Model Monitor para violaciones persistentes
# ============================================================
cards.append(card(
    question="Un desarrollador desplego un modelo reentrenado en un endpoint de SageMaker AI con Model Monitor. Pese al modelo actualizado y a trafico nuevo, el monitoring job <b>sigue mostrando violaciones</b>. Confirmo que el nuevo dataset es estadisticamente representativo del trafico actual, pero las violaciones persisten. &iquest;Que accion correctiva las resuelve?",
    options=[
        "Ejecutar un baseline job sobre los nuevos datos y apuntar Model Monitor a esas estadisticas",
        "Disparar un nuevo training job con el mismo dataset de baseline existente y reevaluar",
        "Ajustar los umbrales de Model Monitor para reducir las violaciones reportadas",
        "Eliminar y recrear el endpoint con la misma configuracion para reiniciar el monitoring job",
    ],
    correct=0,
    key="aip03r-q52",
    answer=(
        '<div class="verdict">Correcta: {{L}} - regenerar el baseline sobre los nuevos datos.</div>'
        '<p><b>El problema:</b> las violaciones persisten porque Model Monitor compara el trafico actual contra un <b>baseline viejo</b>. Si el modelo y los datos cambiaron pero el baseline no, la comparacion siempre marca desviacion. El detalle avanzado es el <b>re-baselining</b> como accion correctiva, no tocar el modelo ni los umbrales.</p>'
        '<p><b>Por que la respuesta sirve:</b> ejecutar un <b>baseline job</b> sobre los nuevos datos de entrenamiento y apuntar Model Monitor a esas <b>nuevas estadisticas de baseline</b> alinea la referencia con la distribucion actual. Al comparar contra el baseline correcto, desaparecen las violaciones espurias.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Reentrenar con el baseline viejo:</b> el problema no es el modelo sino el baseline desactualizado; reentrenar no corrige la referencia obsoleta.</li>'
        '<li><b>Ajustar umbrales:</b> solo reduce la cantidad de alertas; enmascara el sintoma sin resolver la comparacion incorrecta de fondo.</li>'
        '<li><b>Recrear el endpoint:</b> reconstruir el endpoint no actualiza el baseline de Model Monitor; seguira comparando contra estadisticas viejas.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Violaciones persistentes con datos ya representativos = baseline desactualizado; la solucion es regenerar el baseline y apuntar el monitor a las nuevas estadisticas, no reentrenar, subir umbrales ni recrear el endpoint.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-create-baseline.html">docs.aws Model Monitor crear baseline</a></div>'
    ),
))

# ============================================================
# Q54r - Combinacion de IA gestionada multimodal (Comprehend/Transcribe/Rekognition)
# ============================================================
cards.append(card(
    question="Una empresa de medios tiene petabytes de imagenes, videos, podcasts y transcripciones <b>sin etiquetar</b> en S3. Analistas con <b>poca experiencia en ML</b> deben habilitar tagging e indexado automatico en varias modalidades, <b>sin entrenar modelos, sin etiquetado manual ni aprovisionar infraestructura</b>. &iquest;Que solucion es la mas rapida y efectiva?",
    options=[
        "Amazon Comprehend, Amazon Transcribe y Amazon Rekognition como servicios gestionados para etiquetar el multimedia",
        "AWS Batch para correr periodicamente scripts Python en contenedores sobre el multimedia",
        "Amazon Polly, Amazon Translate y Amazon Lex en un pipeline de SageMaker para catalogar",
        "Amazon Transcribe y luego entrenar Neural Topic Model (NTM) y Object Detection de SageMaker",
    ],
    correct=0,
    key="aip03r-q54",
    answer=(
        '<div class="verdict">Correcta: {{L}} - servicios de IA gestionada (Comprehend, Transcribe, Rekognition).</div>'
        '<p><b>El problema:</b> tagging multimodal (imagen, video, audio, texto) <b>sin entrenar, sin etiquetar ni aprovisionar</b>, para un equipo no experto. El detalle avanzado es elegir la <b>combinacion de servicios de IA gestionados</b> por modalidad, no algoritmos que exijan entrenamiento.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Rekognition</b> analiza imagen/video (objetos, escenas), <b>Transcribe</b> convierte audio a texto y <b>Comprehend</b> extrae entidades/temas del texto. Son APIs gestionadas y pre-entrenadas: cubren todas las modalidades sin entrenamiento, sin etiquetado y sin infraestructura, con implementacion rapida.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>AWS Batch + scripts:</b> Batch corre jobs por lotes, no da capacidades de analisis multimedia listas; exige configurar, orquestar y mantener, agregando complejidad innecesaria.</li>'
        '<li><b>Polly + Translate + Lex:</b> son sintesis de voz, traduccion y chatbots; no detectan objetos ni extraen entidades para taggear e indexar medios.</li>'
        '<li><b>Transcribe + NTM + Object Detection:</b> NTM y Object Detection son algoritmos de <b>entrenamiento</b> (Object Detection requiere datos etiquetados); introducen training y labeling, justo lo que se quiere evitar.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Tagging multimodal sin entrenar ni etiquetar = combinar los servicios de IA gestionados por modalidad (vision, voz-a-texto, NLP). Los algoritmos integrados exigen entrenamiento/etiquetado; voz, traduccion y chatbots no clasifican contenido.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html">docs.aws Amazon Rekognition</a> '
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html">docs.aws Amazon Comprehend</a></div>'
    ),
))



# ============================================================
# Q56r - ModelExplainabilityMonitor + baseline SHAP (attribution drift)
# ============================================================
cards.append(card(
    question="Un modelo de reclamos en un endpoint de SageMaker AI daba peso al da&ntilde;o y costo, pero en produccion ahora enfatiza la <b>antiguedad del vehiculo</b>, con riesgo de cumplimiento. Deben monitorear cuando la <b>atribucion de importancia de variables cambia en produccion</b> y alertar. &iquest;Que implementar?",
    options=[
        "La clase ModelExplainabilityMonitor con baseline SHAP y CloudWatch para alertar",
        "SageMaker Clarify sobre el dataset de entrenamiento con CloudWatch para alertar",
        "SageMaker DataCapture con un pipeline propio de distribuciones y CloudWatch para alertar",
        "Un baseline con la clase ModelQualityMonitor (accuracy, recall) y CloudWatch",
    ],
    correct=0,
    key="aip03r-q56",
    answer=(
        '<div class="verdict">Correcta: {{L}} - ModelExplainabilityMonitor con baseline SHAP.</div>'
        '<p><b>El problema:</b> hay que detectar <b>drift de atribucion de features</b> (que variable pesa mas) <b>en produccion y de forma continua</b>, con alerta automatica. El detalle avanzado es la <b>clase especifica</b> y el <b>baseline SHAP</b>, no un analisis estatico ni un monitor de calidad.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>ModelExplainabilityMonitor</b> con un <b>baseline SHAP</b> es la capacidad de Model Monitor dise&ntilde;ada para vigilar la <b>atribucion de features en produccion</b>: compara periodicamente la importancia asignada por el modelo contra el baseline y, via CloudWatch, alerta cuando se desvia del umbral. Es exactamente el feature attribution drift pedido.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Clarify sobre el dataset de entrenamiento:</b> Clarify hace analisis <b>estatico</b> en desarrollo; no monitorea el modelo desplegado ni la atribucion en vivo de forma continua.</li>'
        '<li><b>DataCapture + pipeline propio:</b> DataCapture solo registra entradas/salidas; construir el analisis de atribucion a mano agrega complejidad y no es la solucion nativa para attribution drift.</li>'
        '<li><b>ModelQualityMonitor:</b> vigila metricas de desempe&ntilde;o (accuracy, recall), no como el modelo pondera las features; no detecta el cambio de importancia salvo que degrade la metrica.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>"Cambia el peso/atribucion de features en produccion" = el monitor de explicabilidad con un baseline de atribucion. El analisis estatico solo mira desarrollo, la captura de datos solo registra y el monitor de calidad mira accuracy/recall, no la atribucion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-monitor-feature-attribution-drift.html">docs.aws monitoreo de feature attribution drift</a></div>'
    ),
))

# ============================================================
# Q60r - KMS + Glue para redaccion de PII (credit card) antes de entrenar
# ============================================================
cards.append(card(
    question="Una financiera construye un modelo de fraude con SageMaker AI y Comprehend. Los datos incluyen numeros de tarjeta. Todo debe estar cifrado de forma segura y la PII se debe <b>redactar antes</b> de entrenar. &iquest;Que solucion cumple?",
    options=[
        "Cifrar los datos con AWS KMS en Amazon S3 y usar AWS Glue para redactar los numeros de tarjeta antes de entrenar",
        "SageMaker Data Wrangler con cifrado por un algoritmo propio, subida a S3 via AWS CLI y entrenamiento con el dataset cifrado",
        "Comprehend para detectar y redactar PII, guardar lo redactado en S3, entrenar en SageMaker AI y cifrar con un algoritmo propio",
        "El algoritmo PCA de SageMaker AI para reducir dimensionalidad y eliminar los numeros de tarjeta",
    ],
    correct=0,
    key="aip03r-q60",
    answer=(
        '<div class="verdict">Correcta: {{L}} - cifrar con AWS KMS en S3 + redactar PII con AWS Glue.</div>'
        '<p><b>El problema:</b> dos exigencias de cumplimiento: cifrado <b>gestionado y auditable</b> y <b>redaccion de PII</b> (numeros de tarjeta) antes de entrenar. El detalle avanzado es usar cifrado gestionado por KMS (no un algoritmo propio) y un servicio de datos como Glue para la redaccion.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>AWS KMS</b> cifra los datos en S3 con claves gestionadas y auditables, el enfoque recomendado en finanzas. <b>AWS Glue</b> transforma y <b>redacta los numeros de tarjeta</b> antes del entrenamiento. Cumple cifrado seguro + redaccion previa de PII con servicios gestionados.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Data Wrangler + algoritmo propio:</b> Data Wrangler no redacta PII y un algoritmo de cifrado propio no cumple estandares ni se integra bien; KMS es el metodo recomendado.</li>'
        '<li><b>Comprehend + algoritmo propio:</b> aunque Comprehend puede redactar PII, el cifrado con algoritmo propio introduce riesgo y no cumple los estandares; se prefiere KMS.</li>'
        '<li><b>PCA:</b> es reduccion de dimensionalidad, no una tecnica de sanitizacion; no garantiza eliminar PII como los numeros de tarjeta.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Cumplimiento = cifrado gestionado por el servicio de claves (nunca "algoritmo propio") + un servicio de datos que redacte PII antes de entrenar. PCA no sanitiza y descubrir datos no es lo mismo que redactar.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/glue/latest/dg/detect-PII.html">docs.aws Glue deteccion y redaccion de PII</a></div>'
    ),
))

# ============================================================
# Q61r - Data Wrangler histograma para distribucion de feature
# ============================================================
cards.append(card(
    question="Un equipo usa SageMaker Data Wrangler y una feature numerica (brillo) afecta la convergencia. Quiere <b>explorar la distribucion del brillo</b> antes de decidir si normalizar. &iquest;Que accion entiende mejor el rango y la distribucion?",
    options=[
        "Usar la visualizacion de histograma de SageMaker Data Wrangler para inspeccionar el rango de valores de la feature de brillo e identificar outliers",
        "Usar Comprehend para hacer analisis de sentimiento sobre los valores de brillo y determinar si se necesita normalizacion",
        "Exportar el dataset a Amazon S3 y usar AWS Glue DataBrew para crear una visualizacion de box plot de la feature de brillo",
        "Usar SageMaker Clarify para detectar sesgo en los datos de la feature de brillo antes de realizar cualquier normalizacion",
    ],
    correct=0,
    key="aip03r-q61",
    answer=(
        '<div class="verdict">Correcta: {{L}} - histograma de SageMaker Data Wrangler.</div>'
        '<p><b>El problema:</b> entender la <b>distribucion y el rango</b> de una feature numerica (brillo) antes de decidir normalizar, dentro de Data Wrangler. El detalle avanzado es que el grafico adecuado para ver la <b>frecuencia y outliers</b> es el histograma, y que ya esta en Data Wrangler.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>histograma de SageMaker Data Wrangler</b> muestra la distribucion de frecuencia de los valores de brillo, revelando rango, forma y outliers de un vistazo, justo lo necesario para decidir la normalizacion, sin salir de la herramienta ya en uso.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Comprehend (sentimiento):</b> es NLP para texto; no puede analizar ni visualizar valores numericos como el brillo.</li>'
        '<li><b>Exportar a Glue DataBrew (box plot):</b> mover los datos a otro servicio agrega complejidad innecesaria (ya se usa Data Wrangler) y un box plot resume dispersion/outliers pero no muestra la distribucion de frecuencia completa como el histograma.</li>'
        '<li><b>SageMaker Clarify:</b> sirve para sesgo y explicabilidad, no para EDA de la distribucion de una feature numerica.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Ver rango, distribucion de frecuencia y outliers de una feature numerica = histograma en la propia herramienta de preparacion. El analisis de texto no aplica a numeros, el box plot no muestra la frecuencia completa y la herramienta de sesgo no hace EDA.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-analysis.html">docs.aws analisis y visualizaciones en Data Wrangler</a></div>'
    ),
))



# ============================================================
# Q64r - SageMaker Asynchronous Inference (payload grande + picos)
# ============================================================
cards.append(card(
    question="Una empresa procesa imagenes de <b>hasta 60 MB</b> con Rekognition y Bedrock para captions. El flujo arranca al subir a S3 y hay <b>picos impredecibles</b>. Debe escalar sola con <b>minima gestion de infraestructura</b>. &iquest;Que solucion tiene menor operacion?",
    options=[
        "Un endpoint de Amazon SageMaker Asynchronous Inference con una scaling policy automatica",
        "Un pipeline en Amazon ECS on Fargate por schedule que inserte en Amazon Aurora",
        "Un Auto Scaling group de Amazon EC2 que monitoree el bucket S3 por imagenes nuevas",
        "Amazon SQS para encolar tareas y AWS Lambda que ejecute Rekognition y Bedrock",
    ],
    correct=0,
    key="aip03r-q64",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SageMaker Asynchronous Inference con scaling policy.</div>'
        '<p><b>El problema:</b> payloads <b>grandes</b> (hasta 60 MB), <b>picos impredecibles</b> y minima gestion de infraestructura. El detalle avanzado es elegir el <b>tipo de inferencia</b> correcto: asincrono, que encola y maneja payloads grandes, no Lambda ni EC2.</p>'
        '<p><b>Por que la respuesta sirve:</b> el <b>Asynchronous Inference</b> de SageMaker esta hecho para payloads grandes y cargas con picos: encola internamente las peticiones, procesa de forma asincrona y con una <b>scaling policy</b> ajusta la capacidad (incluso a cero cuando no hay trabajo). Es gestionado, asi que hay minima operacion.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>ECS on Fargate por schedule:</b> las tareas programadas responden a un horario fijo, no a eventos de subida; sigue requiriendo configurar scheduling, monitoreo y escalado, sin la respuesta dinamica pedida.</li>'
        '<li><b>EC2 Auto Scaling:</b> exige aplicar parches, configurar y monitorear instancias; agrega operacion y carece del encolado y del procesamiento asincrono gestionado.</li>'
        '<li><b>SQS + Lambda:</b> Lambda tiene limites de payload, memoria y tiempo; no encaja con imagenes de 60 MB ni con inferencia ML pesada y larga, y puede fallar o hacer timeout en picos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Payload grande + picos + minima operacion = endpoint de inferencia asincrona (encola y escala, incluso a cero). Lambda topa en payload/tiempo, EC2 agrega gestion y las tareas por schedule no son event-driven.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html">docs.aws SageMaker Asynchronous Inference</a></div>'
    ),
))

# ============================================================
# Q66r - SMOTE (oversampling sintetico de clase minoritaria)
# ============================================================
cards.append(card(
    question="Un clasificador binario de fraude tiene muchos <b>falsos negativos</b> pese a una accuracy &gt;96%, por un <b>desbalance severo</b> (el fraude es menos del 0.5% del dataset). Quieren <b>corregir directamente el desbalance</b> antes del proximo reentrenamiento. &iquest;Que solucion aumenta la deteccion de casos fraudulentos?",
    options=[
        "Aplicar SMOTE (Synthetic Minority Oversampling Technique) sobre la clase minoritaria de fraude antes de entrenar",
        "Realizar oversampling aleatorio sobre las transacciones no fraudulentas para igualar los tama&ntilde;os de batch durante el entrenamiento",
        "Habilitar early stopping en SageMaker para detener automaticamente el entrenamiento cuando la accuracy de validacion deje de mejorar",
        "Habilitar automatic model tuning con optimizacion bayesiana y aumentar el numero de tuning jobs para explorar un rango mas amplio de hiperparametros",
    ],
    correct=0,
    key="aip03r-q66",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SMOTE sobre la clase minoritaria (fraude).</div>'
        '<p><b>El problema:</b> muchos falsos negativos por <b>desbalance severo</b>; una accuracy alta enga&ntilde;a porque el modelo casi siempre predice "no fraude". Hay que <b>corregir el desbalance</b> de datos. El detalle avanzado es la tecnica exacta: <b>oversampling sintetico de la clase minoritaria</b>.</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>SMOTE</b> genera ejemplos <b>sinteticos</b> de la clase minoritaria (fraude) interpolando entre muestras reales, equilibrando el dataset antes de entrenar. Con mas representacion de fraude, el modelo aprende a detectarlo y bajan los falsos negativos.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Oversampling de la clase mayoritaria (no fraude):</b> aumenta la clase equivocada, <b>empeora</b> el desbalance y sesga aun mas hacia "no fraude".</li>'
        '<li><b>Early stopping:</b> evita sobreajuste pero no corrige el desbalance ni mejora la deteccion de la clase rara.</li>'
        '<li><b>Automatic model tuning:</b> optimiza hiperparametros, pero sin atacar la distribucion sesgada no reduce de forma significativa los falsos negativos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Desbalance severo con muchos falsos negativos = generar muestras sinteticas de la clase MINORITARIA antes de entrenar. Sobremuestrear la mayoritaria empeora el sesgo; early stopping y tuning no corrigen la distribucion.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-balance-data.html">docs.aws balancear datos (SMOTE) en SageMaker</a></div>'
    ),
))

# ============================================================
# Q71r - SMOTE en Data Wrangler (churn, XGBoost)
# ============================================================
cards.append(card(
    question="Un equipo prepara datos de churn en SageMaker Data Wrangler y solo ~8% de los clientes hizo churn (<b>desbalance de clases</b>). Al entrenar un XGBoost, el modelo predice casi siempre &quot;no churn&quot;, con <b>mala recall</b> para los que abandonan. &iquest;Que enfoque resuelve el desbalance <b>antes</b> de lanzar el training job?",
    options=[
        "SMOTE (Synthetic Minority Oversampling Technique) en SageMaker Data Wrangler antes del training job",
        "SageMaker Model Monitor para detectar el desbalance tras el despliegue y ajustar umbrales",
        "Random Undersampling en SageMaker Data Wrangler eliminando muestras de la clase mayoritaria",
        "SageMaker Clarify para analizar el desbalance y generar metricas de sesgo",
    ],
    correct=0,
    key="aip03r-q71",
    answer=(
        '<div class="verdict">Correcta: {{L}} - SMOTE en SageMaker Data Wrangler.</div>'
        '<p><b>El problema:</b> desbalance de clases (8% churn) que hace que el modelo ignore la clase rara (mala recall). Hay que <b>corregir el desbalance antes</b> de entrenar. El detalle avanzado es la tecnica exacta (SMOTE) y donde aplicarla (Data Wrangler).</p>'
        '<p><b>Por que la respuesta sirve:</b> aplicar <b>SMOTE en Data Wrangler</b> genera muestras <b>sinteticas</b> de la clase minoritaria (churn) para rebalancear el dataset dentro del mismo flujo de preparacion, antes del training job. Con las clases equilibradas, el XGBoost mejora la recall de los que abandonan.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Model Monitor:</b> observa modelos ya <b>desplegados</b>; no rebalancea el dataset de entrenamiento ni corrige la causa raiz antes de entrenar.</li>'
        '<li><b>Random Undersampling:</b> balancea eliminando muestras de la mayoritaria, pero pierde informacion valiosa y reduce el dataset, debilitando la generalizacion.</li>'
        '<li><b>SageMaker Clarify:</b> diagnostica y documenta el sesgo/desbalance, pero no lo <b>corrige</b>; es diagnostico, no la solucion al problema de recall.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Corregir desbalance ANTES de entrenar = generar muestras sinteticas de la clase minoritaria en la herramienta de preparacion. El monitor es post-despliegue, el undersampling tira informacion y la herramienta de sesgo solo diagnostica.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-balance-data.html">docs.aws balancear datos (SMOTE) en Data Wrangler</a></div>'
    ),
))



# ============================================================
# Q72r - Comprehend topic detection (topic modeling / clustering)
# ============================================================
cards.append(card(
    question="Una firma de research guarda miles de briefings de analistas (audio) en S3. La proxima fase requiere <b>agrupar las discusiones por tema</b> (estrategia de renta variable, politica macro, tendencias de divisas). El desarrollador debe elegir un enfoque que <b>categorice automaticamente</b> las grabaciones por topico <b>minimizando el desarrollo a medida</b>. &iquest;Que solucion cumple de forma mas eficiente?",
    options=[
        "Amazon Transcribe para pasar las grabaciones a texto y un job de topic detection de Amazon Comprehend",
        "Amazon Transcribe seguido de un clasificador personalizado de Amazon Comprehend con topicos predefinidos",
        "Un flujo de etiquetado en SageMaker AI Ground Truth, Amazon Transcribe y semantic segmentation de SageMaker AI",
        "Amazon Transcribe y entrenar semantic segmentation y Neural Topic Model (NTM) de SageMaker AI",
    ],
    correct=0,
    key="aip03r-q72",
    answer=(
        '<div class="verdict">Correcta: {{L}} - Transcribe + Comprehend topic detection.</div>'
        '<p><b>El problema:</b> agrupar por tema sin conocer las categorias de antemano y con <b>minimo desarrollo</b>. El detalle avanzado es distinguir <b>topic detection</b> (no supervisado, sin etiquetas ni entrenamiento) del clasificador personalizado (supervisado, requiere labeling).</p>'
        '<p><b>Por que la respuesta sirve:</b> <b>Transcribe</b> pasa el audio a texto y el <b>topic detection de Comprehend</b> (topic modeling) descubre y agrupa temas de forma <b>no supervisada</b>, sin etiquetar datos ni entrenar modelos. Es la ruta gestionada con menor desarrollo a medida.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Clasificador personalizado de Comprehend:</b> requiere etiquetar datos y entrenar el clasificador con topicos predefinidos; mas esfuerzo, contrario a minimizar desarrollo.</li>'
        '<li><b>Ground Truth + semantic segmentation:</b> semantic segmentation es para imagenes, no texto; ademas exige etiquetado manual y orquestacion innecesaria.</li>'
        '<li><b>NTM + semantic segmentation entrenados:</b> implica entrenar varios modelos (uno irrelevante para texto), aumentando esfuerzo y complejidad frente a un servicio gestionado.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Agrupar por tema sin categorias previas y con minimo desarrollo = deteccion de topicos no supervisada (topic modeling) gestionada, no un clasificador personalizado (que exige etiquetar y entrenar) ni algoritmos de imagen.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/topic-modeling.html">docs.aws Comprehend topic modeling</a></div>'
    ),
))

# ============================================================
# Q73r - Scheduled scaling policy (trafico predecible por evento)
# ============================================================
cards.append(card(
    question="Un e-commerce usa un endpoint de SageMaker AI para recomendaciones. Ante <b>eventos de ventas programados</b>, la latencia sube y da mala experiencia. Deben ajustar la politica de escalado para los <b>picos de alto trafico conocidos</b>. &iquest;Que solucion optimiza mejor el escalado?",
    options=[
        "Configurar una scheduled scaling policy para aumentar la capacidad del endpoint de inferencia antes de que comiencen los eventos de venta",
        "Usar AWS Lambda para reiniciar periodicamente el endpoint durante el trafico pico y asi refrescar el rendimiento de las instancias",
        "Implementar una step scaling policy para el endpoint que escale segun metricas de utilizacion de recursos como uso de CPU y memoria",
        "Aumentar el tama&ntilde;o de instancia del endpoint a un tipo mas grande para acomodar el mayor trafico durante los eventos de venta",
    ],
    correct=0,
    key="aip03r-q73",
    answer=(
        '<div class="verdict">Correcta: {{L}} - scheduled scaling policy.</div>'
        '<p><b>El problema:</b> los picos son <b>conocidos y programados</b> (eventos de venta). El detalle avanzado es elegir la sub-feature de escalado adecuada al patron predecible: el <b>escalado programado</b>, frente a auto-scaling reactivo o cambios estaticos.</p>'
        '<p><b>Por que la respuesta sirve:</b> una <b>scheduled scaling policy</b> aumenta la capacidad del endpoint <b>antes</b> de cada evento segun un horario, dejando capacidad lista cuando llega el pico. Como el trafico es predecible, escalar por calendario evita la latencia inicial del escalado reactivo.</p>'
        '<p><b>Por que NO las otras, una por una:</b></p>'
        '<ul>'
        '<li><b>Lambda para reiniciar el endpoint:</b> reiniciar no mejora la escalabilidad ni el desempe&ntilde;o; introduce downtime y no ataca la falta de capacidad en el pico.</li>'
        '<li><b>Step scaling por CPU/memoria:</b> los endpoints escalan mejor por metricas como invocaciones por instancia; ademas es reactivo y llega tarde a un pico predecible.</li>'
        '<li><b>Instancia mas grande:</b> es una solucion estatica y rigida; no se adapta al patron de trafico y lleva a sobreaprovisionar fuera de los picos.</li>'
        '</ul>'
        '<div class="extra"><span class="h">Exam tip</span>Picos conocidos por calendario = escalado programado (provisiona antes del evento). El escalado reactivo llega tarde, subir el tama&ntilde;o de instancia es estatico y reiniciar no escala.</div>'
        '<div class="links"><span class="h">Links</span>'
        '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html">docs.aws auto scaling de endpoints de SageMaker</a></div>'
    ),
))

create(deck_name="AIP-C01::03", cards=cards, out_path="out/AIP-C01_03.apkg", do_import=False)
