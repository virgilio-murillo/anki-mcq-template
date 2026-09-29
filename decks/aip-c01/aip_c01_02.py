#!/usr/bin/env python3
"""
AIP-C01::02 - Preguntas nuevas (deduplicadas) del examen 2.

56 cartas construidas a partir de decks/aip-c01/dedupe/new_to_generate_exam2.json.

Reglas aplicadas (docs/DECK_STANDARDS.md):
- 1 carta por pregunta (solo la MCQ directa).
- Exactamente 4 opciones por carta. Una fuente (n=37) traia 5 opciones con una
  opcion basura (el fragmento de enunciado "Which of the following solutions will");
  se descarto y se conservaron las 4 reales, remapeando el indice correcto.
- Espanol, HTML con entidades para acentos, sin em dashes. Servicios AWS en su
  forma oficial (Amazon Bedrock, AWS Lake Formation, etc.).
- Verdict con {{L}} (nunca hardcodear la letra; el motor baraja y sustituye).
- El frente no filtra la respuesta; opciones de longitud/especificidad comparable.
- Cada dorso: verdict, El problema, Por que la respuesta sirve (define terminos),
  Por que NO las otras una por una (refuta cada distractor, base en los rationale
  de la fuente traducidos), Exam tip y Links a docs.aws.amazon.com.
- key estable y unica: aip02-q<n> usando el numero n de la fuente.
- correct = indice 0-based correcto tras traducir (mismo orden que la fuente).
"""
from anki_mcq import card, create

cards = [
    # ============================================================
    # Q1 - Bedrock interface VPC endpoints + Lake Formation LF-tags
    # ============================================================
    card(
        question="Una carga de IA generativa en Amazon Bedrock: llamadas de API Gateway a Lambda en subredes privadas. Requisitos: <b>todo el trafico a Bedrock solo por red privada</b> (sin Internet) y un data lake en otra cuenta con <b>control de acceso a nivel de columna</b>. &iquest;Que solucion cumple?",
        options=[
            "Endpoints VPC de interfaz para Bedrock (Lambda privada) y AWS Lake Formation con LF-tags para permisos cross-account por columna",
            "Lambda privada con NAT Gateway hacia Bedrock y el data lake, con politicas de bucket y ACLs de Amazon S3",
            "Gateway VPC endpoint solo para S3, Bedrock por endpoints publicos y grants a nivel de base de datos en Lake Formation",
            "Endpoints VPC para Bedrock y S3 con fallback publico cross-Region, y politicas IAM por path para el data lake",
        ],
        correct=0,
        key="aip02-q1",
        answer=(
            '<div class="verdict">Correcta: {{L}} - endpoints VPC de interfaz para Bedrock + Lake Formation LF-tags.</div>'
            '<p><b>El problema:</b> conectividad <b>solo privada</b> hacia Amazon Bedrock (sin salir a Internet) y gobernanza del data lake <b>a nivel de columna</b> que aplique igual en las dos cuentas.</p>'
            '<p><b>Por que la respuesta sirve:</b> un <b>endpoint VPC de interfaz</b> (PrivateLink) expone las APIs de Bedrock dentro de la VPC, asi el trafico no pasa por Internet. Las <b>LF-tags</b> de AWS Lake Formation (etiquetas de recurso que se asignan a bases, tablas y columnas) permiten permisos cross-account granulares hasta el nivel de columna, cumpliendo ambos requisitos.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>NAT Gateway + politicas/ACLs de S3:</b> un NAT Gateway enruta la salida por Internet publico, violando la conectividad privada; las politicas de bucket y ACLs actuan a nivel de objeto/bucket, no de columna.</li>'
            '<li><b>Gateway endpoint solo S3 + Bedrock publico:</b> Bedrock no se soporta por gateway endpoints (requiere endpoints de interfaz); invocarlo por endpoints publicos rompe el requisito, y los grants a nivel de base de datos no dan control por columna.</li>'
            '<li><b>Endpoints + fallback publico:</b> el fallback a endpoints publicos reintroduce trafico por Internet; ademas las politicas IAM por path no imponen acceso por columna en el data lake.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Conectividad privada a un servicio de AWS = endpoint VPC de interfaz (PrivateLink); un NAT Gateway sigue siendo Internet publico. Control por columna y cross-account en un data lake = etiquetas de recurso (no politicas de S3 ni IAM por path).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html">docs.aws Lake Formation LF-tag access control</a></div>'
        ),
    ),
    # ============================================================
    # Q2 - Glue Data Catalog + CloudTrail para lineage GenAI
    # ============================================================
    card(
        question="Una app de IA generativa (RAG) combina datos de Amazon S3 y de SaaS via Amazon AppFlow. Necesita un <b>registro centralizado</b> de fuentes, <b>tags de metadata</b> para linaje (ligar salidas a su origen) y <b>logging inmutable</b> de accesos para auditoria. &iquest;Que arquitectura conviene?",
        options=[
            "Registrar las fuentes en AWS Glue Data Catalog con tags de metadata, y AWS CloudTrail para registro inmutable de API",
            "Integrar Amazon Macie para escanear y clasificar los reportes, y AWS CloudTrail para registrar API y accesos",
            "Crear el registro con AWS Glue Data Catalog y tags para linaje, y los logs de accesos a Amazon CloudWatch Logs",
            "Usar AWS Lake Formation para control de acceso fino, y Amazon CloudWatch Logs para recolectar logs y monitorear accesos",
        ],
        correct=0,
        key="aip02-q2",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS Glue Data Catalog (registro + tags) + AWS CloudTrail (auditoria inmutable).</div>'
            '<p><b>El problema:</b> hace falta un catalogo central de fuentes con atribucion por metadata (linaje) y un registro de auditoria inmutable de accesos y llamadas de API.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>AWS Glue Data Catalog</b> es el registro central de metadata donde se declaran las fuentes y se aplican tags para atribuir cada salida a su dataset de origen. <b>AWS CloudTrail</b> registra las llamadas de API y eventos de acceso de forma inmutable y a nivel de servicio, que es justo lo que exige el cumplimiento.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Amazon Macie + CloudTrail:</b> Macie descubre y clasifica datos sensibles y genera hallazgos, pero no es un registro central de metadata ni soporta tagging para linaje/atribucion.</li>'
            '<li><b>Glue Data Catalog + CloudWatch Logs:</b> el catalogo esta bien, pero CloudWatch Logs solo recolecta logs de aplicacion/sistema; no es el registro de auditoria inmutable a nivel de API que da CloudTrail.</li>'
            '<li><b>Lake Formation + CloudWatch Logs:</b> Lake Formation gobierna permisos del data lake, no actua como registro central de metadata para atribucion; y CloudWatch Logs no aporta la traza inmutable cross-service requerida.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Registro/catalogo de metadata para linaje = AWS Glue Data Catalog. Auditoria inmutable de llamadas de API a nivel de cuenta = AWS CloudTrail (CloudWatch Logs son logs operativos, no auditoria de API).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html">docs.aws Glue Data Catalog</a></div>'
        ),
    ),
    # ============================================================
    # Q3 - Step Functions payload por S3 URI + ResultPath
    # ============================================================
    card(
        question="Un flujo multi-agente en AWS Step Functions encadena tres agentes de Bedrock; los artefactos ya viven en Amazon S3. Falla porque los <b>payloads intermedios superan la cuota de 256 KB</b>. Hay que evitarlo con <b>minimo esfuerzo operativo</b>. &iquest;Que cambio conviene?",
        options=[
            "Guardar los logs de razonamiento en DynamoDB y pasar solo las partition keys, con un estado Map que traiga el payload",
            "Que Bedrock ingiera los payloads grandes desde una S3 URI: extraer la ubicacion con ResultSelector y pasar solo punteros ligeros con ResultPath",
            "Desplegar un cluster de Amazon ElastiCache for Redis: escribir los payloads en Redis y pasar solo las cache keys al siguiente agente",
            "Migrar la orquestacion a Amazon MWAA (Airflow) y usar XComs con un backend S3 personalizado entre tareas",
        ],
        correct=1,
        key="aip02-q3",
        answer=(
            '<div class="verdict">Correcta: {{L}} - ingerir desde S3 URI y pasar solo punteros con ResultSelector/ResultPath.</div>'
            '<p><b>El problema:</b> el payload que viaja entre estados de Step Functions no puede exceder 256 KB; los agentes se pasan textos grandes de razonamiento y revientan la cuota.</p>'
            '<p><b>Por que la respuesta sirve:</b> como los artefactos ya viven en S3, se pasa entre estados solo la <b>referencia (S3 URI)</b>, no el contenido. Bedrock lee el objeto grande directo desde S3; <b>ResultSelector</b> extrae la ubicacion del objeto generado y <b>ResultPath</b> la anexa al estado como puntero ligero. El payload se mantiene minusculo y se preserva el encadenamiento ReAct sin infraestructura nueva.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DynamoDB + estado Map:</b> agrega una base de datos innecesaria (S3 ya almacena los artefactos) y el estado Map es para procesar arreglos en paralelo, no para un pipeline secuencial de agentes.</li>'
            '<li><b>ElastiCache for Redis:</b> aprovisionar y mantener un cluster (VPC, parches, integracion) es mucho mas overhead operativo, contra el requisito de minimo esfuerzo.</li>'
            '<li><b>Migrar a MWAA:</b> reescribir toda la orquestacion en Airflow es un giro drastico con alto costo de gestion continua; incumple el minimo overhead.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cuota de 256 KB entre estados de Step Functions: guarda el dato grande en el bucket y pasa solo la referencia al objeto (patron claim-check). Los filtros de salida del estado permiten extraer la ubicacion generada y anexarla como puntero ligero.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/concepts-input-output-filtering.html">docs.aws Step Functions input/output</a></div>'
        ),
    ),
    # ============================================================
    # Q5 - Bedrock model evaluation robustness metrics
    # ============================================================
    card(
        question="Un FM de Amazon Bedrock da respuestas distintas ante prompts con diferencias minimas. Con un dataset de variantes cercanas de cada consulta, se quiere un <b>analisis cuantitativo de robustez</b> que mida su sensibilidad y consistencia. &iquest;Que solucion lo logra?",
        options=[
            "Lanzar un job de model evaluation de Amazon Bedrock con el dataset y metricas de robustez para analizar diferencias entre prompts",
            "Elegir un Anthropic Claude a temperatura 0 y un script Lambda con distancia de Levenshtein para medir cuan distintas son las respuestas",
            "Usar Bedrock Pipelines para inferencia por lote, guardar las respuestas en S3 y procesarlas con Amazon Comprehend para similitud",
            "Crear un flujo en AWS Step Functions que invoque el FM con prompts aleatorios y logica propia para la divergencia",
        ],
        correct=0,
        key="aip02-q5",
        answer=(
            '<div class="verdict">Correcta: {{L}} - job de model evaluation de Bedrock con metricas de robustez.</div>'
            '<p><b>El problema:</b> medir de forma cuantitativa y estandarizada la robustez del FM, es decir, su consistencia ante variantes minimas del mismo prompt.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock model evaluation</b> ofrece metricas de <b>robustez</b> nativas que analizan estadisticamente las diferencias de respuesta ante prompts parecidos, entregando la evaluacion cuantitativa pedida sin construir un pipeline a medida.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Temperatura 0 + Levenshtein:</b> la distancia de Levenshtein compara diferencias literales de texto; dos respuestas pueden decir lo mismo con otras palabras (o parecerse y divergir en sentido), asi que no mide robustez semantica.</li>'
            '<li><b>Bedrock Pipelines + Comprehend:</b> pueden procesar por lote y calcular similitud linguistica, pero no traen scoring de robustez ni evaluacion estadistica estandarizada; queda un pipeline sin metrica formal.</li>'
            '<li><b>Step Functions con prompts aleatorios:</b> automatiza invocaciones, pero exige logica propia para medir varianza; no aporta metricas de robustez nativas y suma complejidad.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Evaluacion cuantitativa y estandarizada de un FM (robustez, exactitud, toxicidad): usa Bedrock model evaluation. Levenshtein o similitud linguistica no capturan equivalencia semantica.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock model evaluation</a></div>'
        ),
    ),
    # ============================================================
    # Q7 - Comprehend PII + Rekognition moderation + Bedrock Guardrails
    # ============================================================
    card(
        question="Una plataforma de contenido con Amazon Bedrock. Antes de publicar debe: <b>detectar y quitar PII</b>, <b>moderar imagenes inapropiadas</b> y <b>bloquear contenido daninno del FM</b>, todo automatico y con <b>minima infraestructura</b>. &iquest;Que enfoque cumple?",
        options=[
            "Orquestar con AWS Step Functions: Amazon Comprehend para PII, Amazon Rekognition para imagenes y Bedrock Guardrails sobre entradas y salidas",
            "Disparar Lambda al subir a S3: Comprehend para PII, Rekognition para imagenes y reglas de filtrado propias en Lambda para Bedrock",
            "Usar Amazon EventBridge para enrutar eventos de S3 a Lambdas separadas: una Comprehend, otra Rekognition y una tercera invoca Bedrock",
            "Desplegar un servicio en Amazon ECS: Comprehend para PII, Rekognition para imagenes y logica propia para validar antes y despues de Bedrock",
        ],
        correct=0,
        key="aip02-q7",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Step Functions + Comprehend (PII) + Rekognition (imagenes) + Bedrock Guardrails.</div>'
            '<p><b>El problema:</b> encadenar tres controles (PII en texto, moderacion de imagenes y seguridad del FM) de forma automatica y sin montar infraestructura pesada.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Step Functions</b> coordina los pasos sin servidores. <b>Amazon Comprehend</b> detecta y redacta PII; <b>Amazon Rekognition</b> modera imagenes; y <b>Bedrock Guardrails</b> es el control gestionado que filtra entradas y salidas del modelo para bloquear contenido daninno. Todo con servicios administrados.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda con reglas propias:</b> reescribir filtros de contenido daninno en Lambda duplica lo que Guardrails ya hace de forma gestionada, y hay que mantener esas reglas.</li>'
            '<li><b>EventBridge a Lambdas separadas:</b> requiere coordinacion extra para saber si cada moderacion termino bien y omite Bedrock Guardrails, dejando sin proteger las entradas/salidas del FM.</li>'
            '<li><b>Servicio en ECS:</b> introduce mas infraestructura que desplegar, escalar y mantener, y sustituye Guardrails por logica propia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Seguridad de contenido de un FM = usar el guardrail gestionado (Comprehend para PII en texto, Rekognition para imagenes ya aparecen en varias opciones). La orquestacion serverless debe coordinar los pasos sin reimplementar filtros a mano.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
        ),
    ),
    # ============================================================
    # Q8 - Bedrock Knowledge Base semantic search + Retrieve API
    # ============================================================
    card(
        question="Un marketplace de cursos (150M resenas en PostgreSQL) quiere busqueda semantica con <b>95% de consultas &lt; 500 ms</b>, indice actualizado cada hora, escalado costo-eficiente y el <b>MENOR esfuerzo de desarrollo</b>. &iquest;Que solucion conviene?",
        options=[
            "Amazon Bedrock Knowledge Base con ingesta programada, consultada por su Retrieve API (busqueda vectorial integrada)",
            "Indice de Amazon Kendra con recuperacion NLP, sincronizacion horaria y resultados via Amazon API Gateway",
            "Migrar a Amazon OpenSearch Service, generar embeddings con un FM de Bedrock y hacer busquedas k-NN contra el indice vectorial",
            "Migrar a Amazon Neptune Analytics con indice vectorial de embeddings de Bedrock y Lambdas para generar embeddings y buscar por similitud",
        ],
        correct=0,
        key="aip02-q8",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Bedrock Knowledge Base + Retrieve API.</div>'
            '<p><b>El problema:</b> busqueda semantica de baja latencia con refresco horario y, sobre todo, <b>minimo esfuerzo de desarrollo</b>.</p>'
            '<p><b>Por que la respuesta sirve:</b> una <b>Bedrock Knowledge Base</b> genera y almacena los embeddings durante la ingesta y expone la <b>Retrieve API</b> con busqueda vectorial integrada. Es un servicio gestionado: no hay que construir pipeline de embeddings, orquestacion de embeddings en tiempo de consulta ni tuning de indice. Menos codigo que las alternativas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Amazon Kendra:</b> esta optimizado para busqueda documental empresarial y no expone busqueda vectorial cruda a la escala de 150M de resenas; su modelo de precio/concurrencia no es costo-eficiente para una plataforma de consumo con este volumen.</li>'
            '<li><b>OpenSearch + Bedrock embeddings:</b> puede cumplir el rendimiento, pero exige pipeline de embeddings propio, reingesta horaria, orquestacion de embeddings en consulta y tuning de indice: mucho desarrollo que la KB gestionada elimina.</li>'
            '<li><b>Neptune Analytics + Lambdas:</b> obliga a construir el mismo pipeline de embeddings, orquestacion en consulta y refresco horario a mano, con mayor carga de mantenimiento y sin beneficio adicional a esta escala.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG/busqueda semantica con minimo desarrollo = servicio gestionado que genere el indice de embeddings y exponga una API de recuperacion. Montar OpenSearch o Neptune tu mismo implica construir y mantener el pipeline de embeddings y el refresco.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases</a></div>'
        ),
    ),
    # ============================================================
    # Q9 - Bedrock native data privacy (no retention)
    # ============================================================
    card(
        question="Una plataforma con contenido financiero confidencial usa un FM. Por regulacion, las interacciones deben ser <b>aisladas</b>, sin <b>retener prompts ni salidas</b> ni influir en el modelo, usando capacidades gestionadas (sin sanitizacion propia). &iquest;Que solucion es la MEJOR?",
        options=[
            "Emplear las funciones nativas de privacidad de datos de Amazon Bedrock, que evitan retener prompts y salidas y aislan el FM",
            "Habilitar logging de eventos de datos de AWS CloudTrail para registrar la invocacion del FM y capturar metadata de cumplimiento",
            "Usar AWS KMS para cifrar prompts y salidas en Amazon S3, con ciclo de vida que borre los datos tras procesarlos",
            "Implementar un paso en Lambda que enmascare identificadores sensibles antes del FM y guarde las salidas para auditoria",
        ],
        correct=0,
        key="aip02-q9",
        answer=(
            '<div class="verdict">Correcta: {{L}} - funciones nativas de privacidad de datos de Amazon Bedrock.</div>'
            '<p><b>El problema:</b> cumplimiento que exige no persistir prompts ni salidas y que las interacciones del FM sean efimeras y aisladas, usando capacidades gestionadas.</p>'
            '<p><b>Por que la respuesta sirve:</b> Amazon Bedrock incorpora de forma nativa un modelo de privacidad en el que <b>no retiene tus prompts ni tus salidas</b> ni los usa para entrenar los modelos base, y las interacciones estan aisladas. Cubre el requisito sin construir sanitizacion a medida.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CloudTrail de eventos de datos:</b> esta pensado para auditoria y retiene registros de eventos, es decir, introduce almacenamiento y posible exposicion de metadata; se opone a la no-retencion estricta.</li>'
            '<li><b>KMS + ciclo de vida en S3:</b> protege datos en reposo y controla cuando se borran, pero aun asi persiste los prompts/salidas un tiempo; el requisito es no almacenarlos en absoluto.</li>'
            '<li><b>Lambda de enmascarado + auditoria:</b> el masking reduce identificabilidad, pero sigue guardando salidas derivadas y crea un repositorio de auditoria, incompatible con el aislamiento total y la no-persistencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>No-retencion e interacciones aisladas del FM: apoyate en las funciones nativas de privacidad de datos del servicio de inferencia. Cifrar y luego borrar (KMS + lifecycle) todavia almacena; auditar todavia retiene registros.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html">docs.aws Bedrock data protection</a></div>'
        ),
    ),
    # ============================================================
    # Q10 - Bedrock AgentCore Identity OIDC inbound provider
    # ============================================================
    card(
        question="Un agente en Amazon Bedrock AgentCore Runtime debe imponer SSO corporativo via un IdP OpenID Connect (OIDC), aceptando <b>tokens solo cuando el audience coincide con el ID de la aplicacion</b>. Ademas se quiere ajustar el parametro <b>maximum tokens</b>. &iquest;Que configuracion usar?",
        options=[
            "Configurar Amazon Cognito user pools como IdP entrante para AgentCore, con el application ID como audience permitido y el maximum tokens",
            "Usar autenticacion solo IAM para AgentCore Runtime, validando con SigV4 sin usar OIDC",
            "Configurar AgentCore Identity como proveedor entrante OIDC, con los audiences permitidos al application ID corporativo y el maximum tokens",
            "Enlazar AgentCore Identity al IdP solo para autenticacion saliente: el agente pide tokens pero no valida los entrantes",
        ],
        correct=2,
        key="aip02-q10",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AgentCore Identity como proveedor entrante OIDC con audiences permitidos.</div>'
            '<p><b>El problema:</b> autenticar a los usuarios del agente con el IdP corporativo OIDC ya existente y aceptar solo tokens cuyo audience sea el application ID, ajustando ademas maximum tokens.</p>'
            '<p><b>Por que la respuesta sirve:</b> configurar <b>AgentCore Identity como inbound provider OIDC</b> valida los tokens de entrada contra el IdP y, al fijar los <b>allowed audiences</b> al application ID, solo pasan tokens destinados a esa app. Y <b>maximum tokens</b> limita la longitud de generacion. Cubre exactamente lo pedido reutilizando el IdP corporativo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Cognito como IdP entrante:</b> Cognito puede validar identidad, pero anade una capa extra cuando ya existe un IdP corporativo OIDC; es mas complejo y con mas mantenimiento/latencia que configurar AgentCore Identity directo.</li>'
            '<li><b>Solo IAM + SigV4:</b> IAM autentica llamadas de API de AWS, no valida identidades del IdP corporativo ni impone restriccion de audience; no garantiza que solo el personal autorizado use el agente.</li>'
            '<li><b>OIDC solo saliente:</b> sirve para que el agente pida tokens a servicios externos, no valida los tokens entrantes; no restringe quien puede invocar al agente.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Restringir quien invoca al agente = validacion OIDC ENTRANTE (inbound) con allowed audiences = application ID. Outbound es para que el agente acceda a servicios; IAM/SigV4 no reemplaza SSO de usuario.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html">docs.aws AgentCore Identity</a></div>'
        ),
    ),
    # ============================================================
    # Q11 - Bedrock Knowledge Base query decomposition + flow
    # ============================================================
    card(
        question="Una herramienta de IA generativa para analistas responde consultas multi-parte sobre SEC filings internos; debe <b>descomponer</b> los prompts y <b>evitar la dilucion semantica</b>, con baja latencia y minima complejidad operativa. &iquest;Que solucion conviene?",
        options=[
            "Provisionar OpenSearch Serverless para embeddings y Lambdas propias que parseen y dividan los prompts antes del FM de Bedrock",
            "Configurar una Amazon Bedrock knowledge base con query decomposition nativa y un Bedrock flow que integre la KB con un FM",
            "Entrenar modelos NLP propios en Amazon SageMaker AI para parseo y expansion de consultas, con los documentos en una KB de Bedrock",
            "Crear un indice de Amazon Kendra y un Bedrock agent con razonamiento avanzado para orquestar la descomposicion paso a paso",
        ],
        correct=1,
        key="aip02-q11",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock knowledge base con query decomposition + Bedrock flow.</div>'
            '<p><b>El problema:</b> responder preguntas de varias partes sobre documentos internos, descomponiendolas para no diluir el sentido, con la menor complejidad operativa.</p>'
            '<p><b>Por que la respuesta sirve:</b> la <b>knowledge base</b> de Bedrock aloja los documentos y su <b>query decomposition</b> nativa divide las preguntas complejas en subconsultas, reduciendo la dilucion semantica sin codigo propio. Un <b>Bedrock flow</b> conecta la KB con el FM para servir la aplicacion. Todo gestionado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>OpenSearch Serverless + Lambdas propias:</b> construir y mantener funciones para descomponer consultas anade complejidad y carga administrativa frente a la funcion nativa de Bedrock.</li>'
            '<li><b>Modelos NLP propios en SageMaker:</b> desarrollar, entrenar y hospedar modelos para parseo/expansion es muchisimo overhead; las capacidades nativas de Bedrock lo evitan.</li>'
            '<li><b>Kendra + Bedrock agent:</b> orquestar la descomposicion con un agente implica mas configuracion y overhead que simplemente activar la decomposition nativa de la KB con un flow.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Descomponer consultas multi-parte con minimo overhead: query decomposition nativa de la Bedrock KB + un Bedrock flow. Agentes y Lambdas propias son mas complejos para un RAG de baja latencia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases</a></div>'
        ),
    ),
    # ============================================================
    # Q13 - Bedrock Knowledge Base metadata filtering
    # ============================================================
    card(
        question="Un asistente RAG sobre una Bedrock KB (fuente en S3) recupera documentos de instalaciones, maquinas y periodos <b>no relacionados</b>. Cada documento ya tiene atributos (instalacion, equipo, modelo, tipo, fecha). Se quiere acotar con ellos <b>sin cambiar embeddings ni rediseriar la KB</b>. &iquest;Que solucion mejora la relevancia con MENOS cambios?",
        options=[
            "Habilitar un modelo de reranking en la KB para reordenar los chunks por relevancia y traer mas resultados",
            "Ingerir los atributos como archivos de metadata asociados y aplicar filtrado por metadata para restringir la busqueda",
            "Query decomposition para dividir las preguntas en subconsultas y ejecutar cada una sobre toda la fuente de S3",
            "Rehacer los documentos con chunks mas pequenos y resincronizar la KB, con la busqueda vectorial existente",
        ],
        correct=1,
        key="aip02-q13",
        answer=(
            '<div class="verdict">Correcta: {{L}} - ingerir metadata y aplicar filtrado por metadata en la KB.</div>'
            '<p><b>El problema:</b> el retrieval considera documentos de instalaciones/equipos/fechas irrelevantes; hay atributos por documento que se pueden usar para acotar, sin tocar embeddings ni rediseriar la KB.</p>'
            '<p><b>Por que la respuesta sirve:</b> al ingerir los atributos como <b>archivos de metadata asociados</b>, la Bedrock KB puede aplicar <b>filtrado por metadata</b>: solo entran al espacio de busqueda los documentos que casan con instalacion, modelo, tipo o fecha. Ataca la causa directa (buscar en todo el corpus) con el minimo cambio.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Reranking + mas resultados:</b> el reranking solo reordena chunks ya recuperados; no usa los atributos para restringir que documentos califican, y traer mas candidatos aumenta el ruido en vez de acotarlo.</li>'
            '<li><b>Query decomposition:</b> mejora preguntas multifaceticas dividiendolas, pero sigue buscando en todo el corpus; sin filtros de metadata las subconsultas traen contenido irrelevante.</li>'
            '<li><b>Rechunking mas pequeno:</b> cambia la granularidad del retrieval, pero no impide considerar documentos de otras instalaciones/fechas; no ataca el problema.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cuando ya existen atributos por documento y sobran resultados de otras categorias: metadata filtering en la Bedrock KB. Reranking reordena, no filtra; el chunking cambia granularidad, no alcance.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html">docs.aws Bedrock KB metadata filtering</a></div>'
        ),
    ),
    # ============================================================
    # Q14 - Comprehend PII + Bedrock embeddings + OpenSearch Serverless (Step Functions)
    # ============================================================
    card(
        question="Un asistente RAG de seguros prepara ~60 GB de conversaciones (JSON en S3): <b>quitar PII</b>, <b>generar embeddings</b> y dejarlos para <b>busqueda de similitud de baja latencia</b>. Se quiere un flujo <b>gestionado</b> con la menor infraestructura propia. &iquest;Que enfoque cumple?",
        options=[
            "Lambdas por eventos de S3: parsean el JSON, Comprehend para PII y Bedrock para embeddings, con vectores en DynamoDB y similitud propia",
            "Jobs de AWS Glue ETL que quitan PII con codigo propio y Bedrock para embeddings, con vectores en S3 y Amazon Athena",
            "Usar AWS Step Functions para orquestar: Amazon Comprehend para PII, Bedrock para embeddings y los vectores en Amazon OpenSearch Serverless",
            "Amazon EMR Serverless con Spark para procesar, Comprehend para PII y Bedrock para embeddings, con los vectores en un OpenSearch autogestionado",
        ],
        correct=2,
        key="aip02-q14",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Step Functions + Comprehend + Bedrock embeddings + OpenSearch Serverless.</div>'
            '<p><b>El problema:</b> orquestar un pipeline de preparacion (quitar PII, embeddings, indexar para similitud) de forma gestionada y con poca infraestructura propia.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Step Functions</b> coordina las etapas sin servidores; <b>Comprehend</b> detecta PII; <b>Bedrock</b> genera embeddings; y <b>OpenSearch Serverless</b> ofrece indice vectorial y busqueda k-NN gestionada de baja latencia. Cada pieza es administrada, minimo codigo propio.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambdas + DynamoDB con similitud propia:</b> obliga a escribir el calculo de similitud a mano; OpenSearch Serverless ya da indexado vectorial y k-NN, asi que reimplementarlo aumenta esfuerzo.</li>'
            '<li><b>Glue ETL + S3 + Athena:</b> S3/Athena son para almacenamiento durable y SQL analitico, no para busqueda vectorial de baja latencia; guardar arreglos en S3 no da indice k-NN.</li>'
            '<li><b>EMR Serverless + OpenSearch autogestionado:</b> anade un framework Spark innecesario y un dominio OpenSearch que hay que escalar y administrar, mas overhead que la version serverless.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Pipeline gestionado PII -&gt; embeddings -&gt; vector store: orquesta con un servicio serverless de workflows y usa Comprehend, Bedrock y un vector store serverless con k-NN. Guardar embeddings en S3 o DynamoDB obliga a construir la busqueda de similitud tu mismo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-vector-search.html">docs.aws OpenSearch Serverless vector search</a></div>'
        ),
    ),
    # ============================================================
    # Q15 - Step Functions estado por fase del patron ReAct
    # ============================================================
    card(
        question="Un pipeline usa Amazon Rekognition y luego un FM de Amazon Bedrock. El equipo quiere que el FM siga un <b>patron de razonamiento por pasos (ReAct)</b> y usa AWS Step Functions para coordinar y validar cada etapa. &iquest;Que enfoque entrega ese razonamiento estructurado de la forma MAS confiable?",
        options=[
            "Una state machine que meta todo el razonamiento en un solo estado, con una unica invocacion del FM",
            "Una state machine con un estado Parallel que evalue varias direcciones y un Task final donde el modelo elija la mejor ruta",
            "Una state machine que guie al FM por una cadena de pensamiento con plantillas de prompt y estados Choice segun salidas intermedias",
            "Una state machine con cada fase del ReAct como un estado propio, un prompt por etapa y el retry/manejo de errores nativos",
        ],
        correct=3,
        key="aip02-q15",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un estado por fase del patron ReAct con retry nativo.</div>'
            '<p><b>El problema:</b> lograr razonamiento por pasos consistente y confiable, con validacion de transiciones y recuperacion ante fallos de invocacion del FM.</p>'
            '<p><b>Por que la respuesta sirve:</b> representar <b>cada fase del ReAct como un estado propio</b> con su prompt especifico aprovecha justo lo que Step Functions aporta: coordinacion controlada, validacion entre pasos y <b>retry/manejo de errores nativos</b> para fallos del FM. Esto da el proceso ordenado y reproducible que pide el escenario.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Todo en un solo estado:</b> elimina la coordinacion estructurada; sin dividir en estados no se validan salidas intermedias ni se recupera de fallos parciales, y queda una unica llamada monolitica.</li>'
            '<li><b>Estado Parallel:</b> las ramas paralelas corren aisladas sin contexto compartido; cada una razona con su vision parcial, fragmentando el resultado en lugar de un razonamiento secuencial unificado.</li>'
            '<li><b>Cadena de pensamiento con estados Choice:</b> introducir bifurcaciones segun salidas intermedias vuelve el flujo impredecible y permite que el FM se desvie de una estructura fija, reduciendo la consistencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Razonamiento por pasos confiable en una state machine: un estado por fase con prompt propio + retry/catch nativos. Un solo estado pierde control; el estado paralelo aisla el contexto; las bifurcaciones por salida intermedia vuelven el flujo impredecible.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html">docs.aws Step Functions error handling</a></div>'
        ),
    ),
    # ============================================================
    # Q16 - Bedrock multimodal FMs + Step Functions + dashboard
    # ============================================================
    card(
        question="Un equipo procesa videos y fotos de moda con un modelo de vision y un flujo de FM que interpreta tendencias para un dashboard de analitica, con <b>MINIMO overhead operativo</b>. &iquest;Cual conviene?",
        options=[
            "Instancias Amazon EC2 con codigo propio de procesamiento de imagenes, salida en Amazon RDS y exportacion a una herramienta externa",
            "AWS Step Functions orquestando FMs multimodales de Amazon Bedrock, con salidas en Amazon S3 y dashboard en Amazon Quick Suite",
            "Entrenar un modelo con Amazon Rekognition Custom Labels, detecciones en Amazon DynamoDB y metricas en Amazon Managed Grafana con plugins propios",
            "Enrutar por un SageMaker AI Pipeline con un modelo del AWS Marketplace, resultados en S3 y dashboard en Quick Suite",
        ],
        correct=1,
        key="aip02-q16",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Step Functions + FMs multimodales de Bedrock + S3 + Quick Suite.</div>'
            '<p><b>El problema:</b> procesar contenido visual y generar metricas de tendencia para un dashboard con el menor esfuerzo operativo.</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>FMs multimodales de Bedrock</b> interpretan imagenes/video sin entrenar ni gestionar modelos; <b>Step Functions</b> orquesta serverless; <b>S3</b> guarda salidas; y <b>Amazon Quick Suite</b> publica el dashboard con integracion nativa. Minima infraestructura que administrar.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EC2 + RDS + herramienta externa:</b> exige aprovisionar, escalar y parchear instancias y sumar una herramienta externa; mas overhead que las opciones serverless.</li>'
            '<li><b>Rekognition Custom Labels + Grafana:</b> Custom Labels requiere entrenar y gestionar datasets, y Grafana con plugins propios anade mantenimiento; mas pesado que usar los multimodales preentrenados de Bedrock.</li>'
            '<li><b>SageMaker Pipeline + modelo del Marketplace:</b> gestionar pasos, monitoreo y escalado del pipeline es mas overhead que dejar a Bedrock la orquestacion de inferencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Interpretar imagen/video con minimo overhead: modelos multimodales preentrenados y gestionados, orquestados por un servicio serverless de workflows, con un dashboard nativo. Entrenar (Custom Labels) o gestionar EC2/pipelines suma esfuerzo operativo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html">docs.aws Bedrock modelos soportados</a></div>'
        ),
    ),
    # ============================================================
    # Q17 - Bedrock Prompt Management versioning + alias
    # ============================================================
    card(
        question="Un equipo actualiza seguido los system prompts de una app en Amazon Bedrock y quiere <b>desacoplar el prompt engineering del despliegue de codigo</b>: los analistas prueban variantes, guardan versiones y promueven a produccion sin que ingenieria despliegue. &iquest;Que solucion cumple?",
        options=[
            "Guardar los prompts en un bucket de Amazon S3 y una Lambda que los lea en runtime, actualizando los archivos por version",
            "Usar Bedrock Prompt Management para crear, probar y versionar en consola, con la app llamando a la version del alias de produccion",
            "Codificar los prompts en una state machine de Step Functions, con una version por cambio y API Gateway apuntando a ella",
            "Un patron asincrono con Amazon SQS y Lambda que pase la version del prompt como payload antes del FM",
        ],
        correct=1,
        key="aip02-q17",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Prompt Management con versiones y alias de produccion.</div>'
            '<p><b>El problema:</b> gestionar el ciclo de vida de los prompts (probar, versionar, promover a produccion) de forma independiente del despliegue de codigo.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Prompt Management</b> permite crear, probar y <b>versionar</b> prompts en la consola y exponerlos por <b>alias</b> (por ejemplo, produccion). La app llama a la version del alias; los analistas cambian el prompt sin que ingenieria despliegue codigo. Justo el desacople pedido.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Prompts en S3 + Lambda:</b> desacopla el texto del codigo, pero carece de control de versiones, entornos de prueba y enrutamiento por alias pensados para FMs.</li>'
            '<li><b>Prompts hardcodeados en Step Functions:</b> versionar la state machine por cada cambio vuelve a acoplar el ciclo del prompt al despliegue de infraestructura, con overhead por cambio.</li>'
            '<li><b>SQS + Lambda asincrono:</b> ese patron es para desacoplar componentes por escalabilidad/resiliencia, no para versionar ni gobernar el ciclo de vida de prompts.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Versionar y promover prompts sin desplegar codigo: el servicio gestionado de gestion de prompts (versiones + alias). Guardar texto en S3 no da versionado ni alias; hardcodear reacopla el ciclo del prompt al despliegue de infraestructura.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
        ),
    ),
    # ============================================================
    # Q18 - Cross-Region Inference profiles + batching (Bedrock)
    # ============================================================
    card(
        question="Un asistente en tiempo real con Anthropic Claude 3 Haiku en Amazon Bedrock atiende varios continentes con picos impredecibles y SLA &lt; 2 s. En los picos los endpoints se saturan (throttling, latencia). Se requiere escalado entre Regiones y <b>evitar retry/routing propios complejos</b>. &iquest;Que solucion es la MAS efectiva?",
        options=[
            "Muchas provisioned throughput model units en una unica Region primaria, con backoff exponencial y circuit breaker en la app",
            "Optimizar agregando prompts en peticiones por lote y habilitar Cross-Region Inference con inference profiles por geografia que distribuyen la carga",
            "Construir una capa distribuida de funciones Lambda en varias Regiones con routing propio round-robin ponderado que escale el computo",
            "Introducir un pipeline por eventos que bufferee las peticiones en colas de Amazon SQS y las procese asincronamente con workers",
        ],
        correct=1,
        key="aip02-q18",
        answer=(
            '<div class="verdict">Correcta: {{L}} - batching + Cross-Region Inference con inference profiles por geografia.</div>'
            '<p><b>El problema:</b> picos impredecibles que saturan los endpoints del FM; hay que escalar entre Regiones y maximizar throughput sin logica propia de retry/routing.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Cross-Region Inference</b> con <b>inference profiles</b> distribuye automaticamente las invocaciones entre Regiones de una misma geografia, absorbiendo los picos sin routing manual. Agregar prompts en <b>lotes</b> mejora la eficiencia de throughput. Ataca el cuello de botella en la capa del modelo, no en la aplicacion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Provisioned throughput en una sola Region + retry:</b> concentra el limite de escalado en una Region; el backoff/circuit breaker solo retrasa fallos y los reintentos suben la latencia, dificultando el SLA.</li>'
            '<li><b>Lambdas + routing propio:</b> escala la capa de aplicacion, no la del modelo (donde esta el cuello); el routing propio no conoce en tiempo real la capacidad del FM y distribuye mal.</li>'
            '<li><b>SQS asincrono:</b> convierte el flujo en asincrono, incompatible con respuestas casi en tiempo real; suma latencia, mejor para cargas batch.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Picos y throttling del FM entre Regiones sin routing propio: inferencia distribuida entre Regiones con perfiles por geografia. Escalar solo la app (Lambda) o meter una cola no resuelve el limite en la capa del modelo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">docs.aws Bedrock Cross-Region Inference</a></div>'
        ),
    ),
    # ============================================================
    # Q19 - Bedrock intelligent prompt routing
    # ============================================================
    card(
        question="Un chatbot de soporte en Amazon Bedrock atiende consultas simples (75%) y complejas (25%). Debe ser <b>costo-eficiente</b>, con <b>minimo overhead operativo</b> y alta calidad. &iquest;Que enfoque conviene?",
        options=[
            "Provisioned throughput con Claude Sonnet para todo, con ElastiCache (Redis) para respuestas frecuentes y CloudWatch para escalar",
            "Aprovechar el intelligent prompt routing de Bedrock: Claude Haiku por defecto para lo simple y Claude Sonnet como fallback para lo complejo",
            "Combinar Amazon Lex para lo simple y Bedrock para lo complejo, con S3 para respuestas pregeneradas y CloudWatch para ajustar el uso",
            "Integrar Amazon SageMaker AI para fine-tuning continuo de un Claude Sonnet con feedback en tiempo real y Amazon Kendra para FAQs",
        ],
        correct=1,
        key="aip02-q19",
        answer=(
            '<div class="verdict">Correcta: {{L}} - intelligent prompt routing (Haiku por defecto, Sonnet como fallback).</div>'
            '<p><b>El problema:</b> abaratar sin perder calidad ni sumar overhead, sabiendo que la mayoria de consultas son simples y una minoria son complejas.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>intelligent prompt routing</b> de Bedrock envia cada consulta al modelo adecuado segun su complejidad: <b>Haiku</b> (barato/rapido) para lo simple y <b>Sonnet</b> para lo complejo. Optimiza costo y calidad con una funcion nativa y minimo overhead.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Sonnet para todo:</b> usar el modelo mas caro incluso en el 75% de consultas simples no es costo-eficiente ni optimiza recursos por complejidad.</li>'
            '<li><b>Lex + Bedrock + S3:</b> combinar varios servicios anade complejidad y overhead operativo frente al routing nativo.</li>'
            '<li><b>Fine-tuning continuo + Kendra:</b> el reentrenamiento constante y la integracion de recuperacion suman mucho overhead; contradicen el requisito de minimo esfuerzo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Mezcla de consultas simples y complejas, barato y sin overhead: intelligent prompt routing de Bedrock (modelo chico por defecto, grande como fallback). Un solo modelo grande para todo es caro.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html">docs.aws Bedrock intelligent prompt routing</a></div>'
        ),
    ),
    # ============================================================
    # Q21 - Bedrock Knowledge Base semantic chunking
    # ============================================================
    card(
        question="Un chatbot RAG sobre Bedrock Knowledge Bases (embeddings en S3 Vectors) sufre porque el <b>chunking de tamano fijo</b> corta frases relacionadas y pierde contexto. Se quiere recuperacion coherente y <b>costo minimo</b>. &iquest;Que configuracion conviene?",
        options=[
            "Desactivar el chunking e ingerir documentos completos como un solo chunk, confiando en la RetrieveAndGenerate API",
            "Desplegar un Claude con la ventana de contexto maxima y summarizacion recursiva de los documentos largos antes de la ingesta",
            "Activar el semantic chunking en la Bedrock Knowledge Base y ajustar el maximum tokens para basar los chunks en el significado",
            "Usar hierarchical chunking con chunks hijos pequenos y chunks padre grandes para la recuperacion",
        ],
        correct=2,
        key="aip02-q21",
        answer=(
            '<div class="verdict">Correcta: {{L}} - semantic chunking en la Bedrock Knowledge Base.</div>'
            '<p><b>El problema:</b> el chunking de tamano fijo parte ideas relacionadas, dejando chunks sin contexto y respuestas incompletas; se busca coherencia y bajo costo.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>semantic chunking</b> divide el texto por <b>significado</b> (limites semanticos) en vez de por longitud fija, manteniendo juntas las frases relacionadas. Ajustando maximum tokens se equilibra tamano y coherencia, mejorando relevancia y controlando costo de tokens.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Documentos completos como un chunk:</b> dispara el uso de tokens y suele exceder la ventana de contexto, forzando truncados; encarece en vez de abaratar.</li>'
            '<li><b>Summarizacion recursiva:</b> reduce texto pero solo aproxima los limites semanticos y puede omitir detalles; anade preprocesamiento y no garantiza chunks coherentes.</li>'
            '<li><b>Hierarchical chunking:</b> util para estructuras multinivel, pero los chunks hijos pueden quedar incompletos y los padres grandes traen contenido irrelevante que sube el costo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Chunks que cortan ideas relacionadas: semantic chunking (divide por significado). Documento entero explota tokens; hierarchical resuelve otra cosa (estructura multinivel).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking-parsing.html">docs.aws Bedrock KB chunking</a></div>'
        ),
    ),
    # ============================================================
    # Q23 - Bedrock Guardrails PII masking + Macie + S3 lifecycle
    # ============================================================
    card(
        question="Una plataforma en tiempo real con Amazon Bedrock recibe mensajes con PII. Debe: <b>enmascarar PII antes de la entrada al modelo</b>, <b>redactarla de las respuestas</b> y conservar los logs solo el <b>minimo de retencion</b>, con controles aprobados. &iquest;Que enfoque cumple?",
        options=[
            "Usar Amazon Textract sobre los logs en S3 para analizar PII tras el hecho, con EventBridge, S3 Lifecycle y AWS Config",
            "Bedrock Guardrails que enmascara PII in/out, con logs en S3, Amazon Macie para inspeccion y S3 Lifecycle",
            "Analisis de texto de Amazon Rekognition sobre los logs en S3, cifrado KMS, acceso IAM y S3 Lifecycle a Glacier Deep Archive",
            "Bedrock Guardrails PII in/out, con logs en S3 cifrados con KMS, CloudTrail para Bedrock, Macie y S3 Lifecycle",
        ],
        correct=1,
        key="aip02-q23",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Guardrails (mask PII in/out) + S3 + Macie + S3 Lifecycle.</div>'
            '<p><b>El problema:</b> enmascarar PII ANTES de la inferencia, redactarla de las salidas y retener logs solo el minimo, con controles aprobados.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> con filtros de informacion sensible enmascara PII en la entrada antes de que el modelo la vea y la redacta en la salida (proteccion en tiempo de inferencia). <b>Macie</b> inspecciona continuamente lo guardado en S3 y <b>S3 Lifecycle</b> aplica la retencion minima. Cubre los tres requisitos en el orden correcto.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Textract tras el hecho:</b> analiza los datos ya guardados en S3, o sea la PII cruda ya se recolecto y expuso; no enmascara antes de la inferencia.</li>'
            '<li><b>Rekognition + Glacier:</b> Rekognition es para texto en imagenes, no enmascara PII en prompts en tiempo real; y mover a Glacier Deep Archive contradice retener solo el minimo.</li>'
            '<li><b>Guardrails + KMS + CloudTrail + Macie:</b> Guardrails esta bien, pero el foco en cifrado, logging y reporte no garantiza borrar dentro de la ventana de retencion; puede persistir PII mas de lo permitido.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Enmascarar PII antes de que el modelo la vea: sensitive information filters de Bedrock Guardrails (in y out). Escanear despues (Textract/Rekognition) ya expuso la PII. Retencion minima = S3 Lifecycle que expira, no que archiva.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html">docs.aws Guardrails sensitive information filters</a></div>'
        ),
    ),
    # ============================================================
    # Q24 - Bedrock cross-region inference para resiliencia
    # ============================================================
    card(
        question="Un chatbot global sobre Amazon Bedrock sufre throttling y latencia en una Region en picos. Se busca una estrategia que evite el cuello de botella o punto unico de falla, mantenga compliance por geografia y de <b>failover transparente</b> sin routing manual en el cliente. &iquest;Que solucion conviene?",
        options=[
            "Amazon Route 53 latency-based routing entre endpoints de Bedrock en distintas Regiones",
            "Amazon Route 53 weighted routing a una Region primaria con failover a una secundaria",
            "Todas las llamadas a una sola Region, escalando el endpoint con alarmas de CloudWatch",
            "Cross-region inference que distribuye la API de Bedrock entre Regiones de la misma geografia",
        ],
        correct=3,
        key="aip02-q24",
        answer=(
            '<div class="verdict">Correcta: {{L}} - cross-region inference dentro de la misma geografia.</div>'
            '<p><b>El problema:</b> evitar que una Region sature (throttling/latencia) o sea punto unico de falla, con failover transparente y sin routing manual, respetando la geografia.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>cross-region inference</b> reparte automaticamente el trafico de la API de Bedrock entre varias Regiones de la <b>misma geografia</b>, dando balanceo y failover transparentes sin que el cliente implemente routing. Ataca la causa (capacidad del modelo por Region) y mantiene el compliance geografico.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Route 53 latency-based:</b> dirige a la Region mas cercana, pero no conoce la carga/capacidad real del endpoint; puede seguir mandando a una Region saturada.</li>'
            '<li><b>Route 53 weighted + failover:</b> es reactivo; solo cambia cuando detecta indisponibilidad, asi que antes del failover se siguen viendo throttling y latencia.</li>'
            '<li><b>Una sola Region + escalar:</b> mantiene un punto unico de falla y escala de forma reactiva; las alarmas tardan y los usuarios siguen viendo errores.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Resiliencia y failover transparente del FM sin routing propio: cross-region inference (misma geografia). Route 53 latency/weighted no conoce la capacidad del modelo ni distribuye proactivamente.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">docs.aws Bedrock Cross-Region Inference</a></div>'
        ),
    ),
    # ============================================================
    # Q26 - S3 Object Lock residencia + Macie + CloudTrail
    # ============================================================
    card(
        question="Una app de IA generativa procesa registros en varias Regiones (Europa, Norteamerica, Asia) y guarda salidas en Amazon S3. Regulacion: datos <b>procesados y almacenados solo en su Region de origen</b>, <b>auditoria a prueba de manipulacion</b> de las salidas y <b>descubrir/clasificar PII en reposo</b> por Region. &iquest;Que enfoque cumple todo?",
        options=[
            "Perfiles de cross-Region inference limitados a la Region de origen, permission boundaries de IAM, CloudWatch Logs y Amazon Comprehend para PII",
            "SCPs de AWS Organizations para restringir ingesta/almacenamiento a la Region de origen, un modelo propio por Region y CloudTrail inmutable",
            "S3 Object Lock con politicas de bucket por Region para residencia, preprocesamiento local, Amazon Macie para PII y CloudTrail inmutable",
            "Glue crawlers por Region para etiquetar PII, Athena con workgroups por Region, AWS Config para transferencias cross-Region y CloudWatch Logs",
        ],
        correct=2,
        key="aip02-q26",
        answer=(
            '<div class="verdict">Correcta: {{L}} - S3 Object Lock + politicas por Region + Macie + CloudTrail inmutable.</div>'
            '<p><b>El problema:</b> residencia de datos a nivel de almacenamiento, auditoria inmutable de las salidas y descubrimiento/clasificacion de PII en reposo, por Region.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>S3 Object Lock</b> con <b>politicas de bucket por Region</b> impone residencia a nivel de objeto (impide mover/borrar); preprocesar en la Region de origen mantiene el dato local; <b>Amazon Macie</b> descubre y clasifica PII en S3; y <b>CloudTrail inmutable</b> da la traza a prueba de manipulacion de las salidas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Cross-Region inference + boundaries + Comprehend:</b> los inference profiles controlan donde corre la inferencia, no la residencia en el almacenamiento; CloudWatch Logs no es inmutable; y Comprehend es NLP, no descubrimiento de datos sensibles en S3 (eso es Macie).</li>'
            '<li><b>SCPs + modelo propio:</b> las SCPs son guardrails de permisos a nivel de cuenta, no imponen residencia a nivel de objeto en S3; ademas omite Macie para el descubrimiento de PII.</li>'
            '<li><b>Glue + Athena + Config + CloudWatch:</b> catalogar no impone residencia, los workgroups de Athena controlan donde corre la query no donde vive el dato, Config detecta drift pero no da logs inmutables y CloudWatch Logs no es a prueba de manipulacion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Residencia de datos en reposo = bloqueo a nivel de objeto + politicas de bucket por Region (los inference profiles solo fijan donde corre la inferencia). Auditoria a prueba de manipulacion = CloudTrail inmutable, no CloudWatch Logs. Descubrir/clasificar datos sensibles en S3 = servicio de descubrimiento de datos, no Comprehend.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html">docs.aws S3 Object Lock</a></div>'
        ),
    ),
    # ============================================================
    # Q27 - Guardrails dinamicos por grupo Cognito + KB sync + lifecycle
    # ============================================================
    card(
        question="Un asistente medico sobre una Bedrock Knowledge Base debe: mostrar PII a cirujanos pero <b>enmascararla a ingenieros</b>, referenciar <b>solo reportes de los ultimos 3 anos</b> y autenticar con Amazon Cognito. &iquest;Que solucion cumple?",
        options=[
            "Deteccion de PII de Amazon Macie y una Lambda que redacta la PII de forma permanente al ingerir y resincroniza la KB",
            "Lambda que sincroniza la KB, otra con PII de Amazon Comprehend que redacta para ingenieros, y S3 Lifecycle a 3 anos",
            "S3 Lifecycle que elimina reportes de mas de 3 anos, Lambda que sincroniza la KB y Bedrock guardrails con PII por Cognito",
            "Segunda KB pre-redactada via Lambda y Comprehend, con ingenieros a la saneada y cirujanos a la original por grupo de Cognito",
        ],
        correct=2,
        key="aip02-q27",
        answer=(
            '<div class="verdict">Correcta: {{L}} - guardrails dinamicos por grupo de Cognito en tiempo de consulta + KB sync + S3 Lifecycle.</div>'
            '<p><b>El problema:</b> visibilidad de PII segun el rol (cirujano vs ingeniero) sobre una MISMA fuente, mas ventana de 3 anos y autenticacion con Cognito.</p>'
            '<p><b>Por que la respuesta sirve:</b> aplicar <b>Bedrock guardrails con deteccion de PII de forma dinamica en tiempo de inferencia</b>, segun el <b>grupo de Cognito</b> del usuario, redacta PII solo para quien no debe verla, manteniendo una unica fuente autoritativa. <b>S3 Lifecycle</b> elimina lo mayor a 3 anos y una Lambda programada resincroniza la KB.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Macie + redactar al ingerir:</b> redactar en la ingesta borra la PII de forma permanente, asi los cirujanos ya no podrian verla; incompatible con la visibilidad por rol.</li>'
            '<li><b>Comprehend al ingerir:</b> redactar en la ingesta produce visibilidad inconsistente entre usuarios y acopla la privacidad al pipeline; no usa el guardrail a nivel de respuesta.</li>'
            '<li><b>Dos KB (original y saneada):</b> duplica datos, arriesga drift de sincronizacion y sube costo/mantenimiento; un guardrail por rol en inferencia logra lo mismo con una sola fuente.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Misma fuente, PII visible a unos y oculta a otros: aplica Guardrails por rol en tiempo de respuesta (segun grupo de Cognito). Redactar en ingesta o duplicar KBs rompe la vista autorizada o crea drift.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html">docs.aws Guardrails sensitive information filters</a></div>'
        ),
    ),
    # ============================================================
    # Q28 - LLM-as-a-judge en Bedrock Model Evaluation
    # ============================================================
    card(
        question="Un sistema genera descripciones, avisos de seguridad y traducciones para millones de listados. Compliance debe evaluar varios FMs de forma <b>automatica y escalable</b> en correccion, politicas, contenido daninno y fidelidad multilingue (la revision manual y los keywords no bastan). &iquest;Que solucion es mejor?",
        options=[
            "Correr RAG evaluation para Bedrock Knowledge Bases, midiendo exactitud de recuperacion y cobertura por categoria",
            "Lambdas con keywords y regex que marcan violaciones y evaluan propiedades basicas del texto",
            "Implementar Amazon OpenSearch para indexado full-text y comparar manualmente scores de similitud vectorial entre modelos",
            "LLM-as-a-judge en Amazon Bedrock Model Evaluation, que puntua politicas, seguridad contextual, exactitud multilingue y consistencia",
        ],
        correct=3,
        key="aip02-q28",
        answer=(
            '<div class="verdict">Correcta: {{L}} - LLM-as-a-judge en Bedrock Model Evaluation.</div>'
            '<p><b>El problema:</b> evaluar automaticamente y a escala salidas de varios FMs en dimensiones semanticas (politicas, seguridad, multilingue, consistencia), no solo coincidencias literales.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>LLM-as-a-judge</b> dentro de Bedrock Model Evaluation usa un modelo juez para puntuar automaticamente la calidad de las salidas segun criterios como cumplimiento de politicas, seguridad contextual, fidelidad multilingue y consistencia. Es la evaluacion automatizada y escalable pedida.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>RAG evaluation:</b> mide exactitud de recuperacion y cobertura documental, no razonamiento, cumplimiento de politicas ni contenido daninno.</li>'
            '<li><b>Lambdas con keywords/regex:</b> solo marcan violaciones obvias y metricas basicas; no entienden contexto, matices de daninno ni fidelidad multilingue.</li>'
            '<li><b>OpenSearch full-text:</b> compara similitud textual superficial, no correccion ni alineacion con politicas de la organizacion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Evaluacion cualitativa automatica y escalable de salidas (politicas, seguridad, multilingue): usar un modelo juez dentro del servicio de evaluacion de modelos. Keywords/regex o similitud textual no capturan la semantica.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock Model Evaluation</a></div>'
        ),
    ),
    # ============================================================
    # Q30 - Bedrock Data Automation (BDA) multimodal
    # ============================================================
    card(
        question="Una app convierte contenido academico heterogeneo (PDF, slides, video) en materiales estructurados a &gt;10,000 items/dia. Debe interpretar texto y audio, resumir, usar prompt flows, dar <b>versionado</b> de salidas y <b>colaboracion multiusuario en tiempo real</b>. &iquest;Que solucion cumple?",
        options=[
            "BDA con Lambda para prompt flows, Knowledge Bases para multimedia, salidas versionadas en DynamoDB y colaboracion via SNS + SQS",
            "BDA con FMs, Transcribe (audio) y Textract (documentos), artefactos en S3 con versioning, metadata en DynamoDB y AWS AppSync (GraphQL)",
            "BDA con Step Functions, Textract y Transcribe, salidas versionadas en Amazon Aurora y colaboracion via API Gateway WebSocket con Lambda",
            "BDA con Textract y Transcribe, salidas en S3 con versioning, prompt flows via Amazon EventBridge y Amazon CloudFront con API Gateway",
        ],
        correct=1,
        key="aip02-q30",
        answer=(
            '<div class="verdict">Correcta: {{L}} - BDA + Transcribe + Textract + S3 versioning + DynamoDB + AppSync.</div>'
            '<p><b>El problema:</b> procesar multiples formatos (incluido audio), resumir, versionar salidas y habilitar colaboracion en tiempo real, a gran escala.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Data Automation</b> con FMs procesa insumos diversos; <b>Transcribe</b> convierte audio a texto y <b>Textract</b> extrae de documentos; <b>S3 con versioning</b> versiona artefactos grandes y <b>DynamoDB</b> guarda metadata; y <b>AppSync</b> con suscripciones GraphQL da sincronizacion multiusuario gestionada en tiempo real.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>KB + DynamoDB + SNS/SQS:</b> las Knowledge Bases son para recuperacion sobre datos indexados, no para procesar multimedia; DynamoDB no es ideal para contenido grande versionado; SNS/SQS son mensajeria, no colaboracion en tiempo real.</li>'
            '<li><b>Aurora + WebSocket:</b> Aurora es relacional, no optimo para contenido no estructurado grande con versiones; WebSocket exige gestion de estado propia frente a la sincronizacion gestionada de AppSync.</li>'
            '<li><b>EventBridge + CloudFront:</b> EventBridge enruta eventos, no gestiona prompt flows; CloudFront entrega contenido, no soporta colaboracion en tiempo real.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Colaboracion multiusuario en tiempo real gestionada = suscripciones gestionadas de datos en tiempo real, no SNS/SQS ni sockets a mano. Versionado de artefactos grandes = S3 versioning. Audio = Transcribe; documentos = Textract.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html">docs.aws Bedrock Data Automation</a></div>'
        ),
    ),
    # ============================================================
    # Q32 - Bedrock Guardrails content/word filters + grounding
    # ============================================================
    card(
        question="Una fintech integra Amazon Bedrock en un sistema conversacional sobre datos financieros regulados. Seguridad exige: <b>prevenir salida daninna</b>, <b>evitar divulgar datos sensibles</b> y <b>bloquear contenido de actividad ilegal</b>, con el MENOR esfuerzo. &iquest;Que cumple?",
        options=[
            "Amazon Macie para inspeccionar las respuestas, alertas de Amazon SNS ante contenido ilegal y restricciones basicas a nivel de prompt en Bedrock",
            "Safe completion generico en Bedrock Guardrails, reglas de AWS WAF y una alarma de CloudWatch que dispara Lambda para suprimir respuestas",
            "SageMaker Clarify para patrones inseguros, limites a nivel de prompt en Bedrock y metric filters de CloudWatch para indicadores de contenido ilegal",
            "Bedrock Guardrails con content filters para contenido daninno, word filters para contenido ilegal y contextual grounding checks para no revelar datos sensibles",
        ],
        correct=3,
        key="aip02-q32",
        answer=(
            '<div class="verdict">Correcta: {{L}} - content filters + word filters + contextual grounding de Bedrock Guardrails.</div>'
            '<p><b>El problema:</b> bloquear contenido daninno, evitar divulgaciones sensibles y detectar/bloquear contenido ilegal, con minimo esfuerzo.</p>'
            '<p><b>Por que la respuesta sirve:</b> Bedrock Guardrails resuelve los tres con funciones nativas: <b>content filters</b> interceptan contenido daninno/restringido, <b>word filters</b> bloquean terminos prohibidos o ilegales, y <b>contextual grounding checks</b> ayudan a que la respuesta no revele informacion sensible ni alucine. Todo en un solo servicio gestionado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Macie + SNS + prompt basico:</b> Macie es para clasificar datos en S3, no para inspeccionar respuestas conversacionales en tiempo real; requiere integraciones y esfuerzo manual.</li>'
            '<li><b>Guardrails generico + WAF + CloudWatch + Lambda:</b> usa Guardrails, pero sumar WAF, CloudWatch y Lambda anade complejidad y overhead innecesarios.</li>'
            '<li><b>SageMaker Clarify + metric filters:</b> Clarify es para sesgo/explicabilidad de modelos ML, no filtrado en tiempo real; los metric filters son reactivos y el contenido inseguro puede llegar al cliente.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Seguridad de contenido de un FM con minimo esfuerzo: content filters + word filters + contextual grounding de Bedrock Guardrails (todo nativo). Macie/Clarify no filtran respuestas en tiempo real.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html">docs.aws Guardrails components</a></div>'
        ),
    ),
    # ============================================================
    # Q33 - Haiku + hybrid search + inference profile cross-region
    # ============================================================
    card(
        question="Un chatbot RAG usa Bedrock con Claude Sonnet sobre 50,000+ chunks, pero la latencia es 3-4 s (SLA &lt; 1 s) y debe escalar a 10,000 usuarios concurrentes. &iquest;Que debe implementar para el SLA sub-segundo?",
        options=[
            "Cambiar a Anthropic Claude Haiku, hybrid search con filtrado por metadata que acota candidatos, e inference profile con cross-region routing",
            "Aumentar las model units de Claude Sonnet, agregar retry exponencial y Container Insights para el vector store, sin cambiar el retrieval",
            "Reemplazar el vector store por Amazon Kendra, usar inferencia por lote y el chunking por defecto de las Bedrock Knowledge Bases",
            "Prompt caching de los chunks frecuentes, cambiar a Provisioned Throughput con Claude Opus y traer solo los 3 chunks mas relevantes",
        ],
        correct=0,
        key="aip02-q33",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Haiku + hybrid search con metadata + inference profile cross-region.</div>'
            '<p><b>El problema:</b> bajar la latencia por peticion a menos de 1 s manteniendo exactitud y soportando alta concurrencia.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Claude Haiku</b> tiene menor latencia de inferencia; el <b>hybrid search con filtrado por metadata</b> reduce el conjunto candidato antes de la busqueda vectorial (menos trabajo, mas rapido y preciso); y un <b>inference profile con cross-region routing</b> reparte la carga en pico. Atacan directamente la latencia y la escala.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Mas model units + retry:</b> las MU suben capacidad concurrente, no la latencia por peticion; Sonnet seguiria en 3-4 s. El retry ademas aumenta la latencia.</li>'
            '<li><b>Kendra + inferencia por lote:</b> el batch procesa en cola con demoras de minutos u horas; es incompatible con tiempo real sub-segundo.</li>'
            '<li><b>Opus + provisioned throughput:</b> Claude Opus es el mas lento (5-8 s); va en direccion opuesta al SLA sub-segundo pese al caching o reducir chunks.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Latencia por peticion: elige un modelo mas rapido, no mas capacidad (model units) ni un modelo mas grande como Opus. Hybrid search + metadata acota los candidatos; el cross-region routing reparte el pico.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-hybrid-search.html">docs.aws Bedrock KB hybrid search</a></div>'
        ),
    ),
    # ============================================================
    # Q35 - Bedrock Knowledge Base built-in reranking
    # ============================================================
    card(
        question="Un asistente RAG legal sobre Bedrock Knowledge Bases (RetrieveAndGenerateStream) alucina porque el retrieval usa solo similitud semantica y sube documentos cercanos pero irrelevantes. Se quiere mas precision con la <b>menor infraestructura adicional</b>. &iquest;Que enfoque conviene?",
        options=[
            "Cross-encoder de reranking propio en un endpoint de SageMaker con un ALB delante, invocado en cada consulta",
            "Amazon Neptune para modelar relaciones entre documentos y rankear por scores de centralidad antes de generar",
            "Retrieve API para candidatos, Bedrock Rerank API como llamada aparte para reordenar y luego InvokeModelWithResponseStream",
            "Reranking integrado de las Bedrock Knowledge Bases con los reranker models mas recientes, que reordena por relevancia contextual",
        ],
        correct=3,
        key="aip02-q35",
        answer=(
            '<div class="verdict">Correcta: {{L}} - reranking integrado de las Bedrock Knowledge Bases.</div>'
            '<p><b>El problema:</b> mejorar la relevancia del retrieval (que solo usa similitud semantica) y reducir alucinaciones con el minimo de infraestructura adicional.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>reranking integrado</b> de las Bedrock KB reordena los documentos recuperados por relevancia contextual usando reranker models gestionados, y opera de forma transparente dentro de la misma llamada RetrieveAndGenerateStream. Es un simple cambio de configuracion, sin infraestructura nueva.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Cross-encoder propio en SageMaker + ALB:</b> hay que construir y mantener el modelo, gestionar escalado del endpoint y un balanceador; mucho overhead frente al reranker gestionado.</li>'
            '<li><b>Neptune con centralidad:</b> exige aprovisionar un cluster, modelar y sincronizar el grafo de documentos; infraestructura y operacion innecesarias.</li>'
            '<li><b>Rerank API como llamada aparte:</b> es valida, pero unir Retrieve + Rerank + InvokeModelWithResponseStream como tres llamadas obliga a mantener la orquestacion y el manejo de errores tu mismo; la KB ya lo ofrece integrado.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Mejorar relevancia RAG con minimo overhead: activa el reranking integrado de la Bedrock KB (config, no infraestructura). Cross-encoder propio o la Rerank API suelta hacen el trabajo por el camino dificil.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-reranking.html">docs.aws Bedrock KB reranking</a></div>'
        ),
    ),
    # ============================================================
    # Q36 - Semantic cache con OpenSearch k-NN
    # ============================================================
    card(
        question="Un asistente en Amazon Bedrock recibe muchas preguntas <b>equivalentes en significado pero con distinta redaccion</b>, causando llamadas repetidas al FM. Se quiere reducir redundancia y latencia reutilizando pares consulta-respuesta previos cuando una consulta sea similar. &iquest;Que enfoque conviene?",
        options=[
            "Guardar preguntas y respuestas en Amazon DynamoDB, con el texto normalizado como partition key para devolver la respuesta ante coincidencia exacta",
            "Cachear respuestas en Amazon ElastiCache con un hash de la consulta como clave, devolviendo lo cacheado e invocando Bedrock en los misses",
            "Pares consulta-respuesta en Amazon OpenSearch Service con busqueda por keywords, devolviendo el de mayor score cuando supere un umbral",
            "Amazon OpenSearch como cache semantica: embeddings de los pares en un indice k-NN y busqueda k-NN que sirve la respuesta cacheada",
        ],
        correct=3,
        key="aip02-q36",
        answer=(
            '<div class="verdict">Correcta: {{L}} - cache semantica con indice k-NN en OpenSearch.</div>'
            '<p><b>El problema:</b> reutilizar respuestas ante preguntas equivalentes en significado aunque esten redactadas distinto, para evitar llamadas redundantes al FM.</p>'
            '<p><b>Por que la respuesta sirve:</b> una <b>cache semantica</b> guarda <b>embeddings</b> de los pares consulta-respuesta en un indice <b>k-NN</b>. Para cada nueva consulta se genera su embedding y se busca el vecino mas cercano; si es suficientemente similar, se sirve la respuesta cacheada. Reconoce equivalencia semantica, no solo texto identico.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DynamoDB por texto normalizado:</b> solo casa consultas que normalizan a la misma clave; redacciones distintas del mismo intento no coinciden.</li>'
            '<li><b>ElastiCache por hash:</b> el hash detecta entradas identicas; un pequeno cambio de redaccion cambia la clave y vuelve a invocar el FM.</li>'
            '<li><b>OpenSearch por keywords:</b> la busqueda por palabras clave enfatiza el solape lexico; la busqueda vectorial (embeddings) capta el significado, que es lo que se necesita.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Reusar respuestas ante preguntas parecidas en sentido pero distinta redaccion = cache SEMANTICA (embeddings + busqueda de vecinos por similitud). Un hash o una clave normalizada solo capturan coincidencias exactas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html">docs.aws OpenSearch k-NN</a></div>'
        ),
    ),
    # ============================================================
    # Q37 - CloudWatch Logs Insights + X-Ray + Q Developer (5 opciones -> drop garbage)
    # ============================================================
    card(
        question="Un equipo mejora el troubleshooting de una app de FM en tiempo real (NLP + vision). Necesita analizar logs de varias fuentes, <b>trazar llamadas de API entre servicios</b> y <b>detectar patrones de error de GenAI automaticamente</b>. &iquest;Que solucion conviene?",
        options=[
            "CloudWatch Logs Insights para agregar logs, Amazon SageMaker AI para deteccion de anomalias por ML y Lambda para alertas en tiempo real",
            "CloudWatch Logs Insights para correlacionar logs, AWS X-Ray para trazar API entre servicios y Amazon Q Developer para errores de GenAI",
            "CloudWatch Logs Insights por tipo de error, AWS X-Ray entre microservicios y AWS Glue para extraer/transformar los datos de error",
            "CloudWatch Logs Insights para logs de APIs externas, AWS X-Ray para los modelos GenAI y Amazon Kinesis para transmitir errores",
        ],
        correct=1,
        key="aip02-q37",
        answer=(
            '<div class="verdict">Correcta: {{L}} - CloudWatch Logs Insights + X-Ray + Amazon Q Developer.</div>'
            '<p><b>El problema:</b> analizar logs de varias fuentes, trazar llamadas de API entre servicios y detectar patrones de error propios de GenAI de forma automatica.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>CloudWatch Logs Insights</b> consulta y correlaciona logs en tiempo real; <b>AWS X-Ray</b> traza el recorrido de las llamadas de API entre servicios; y <b>Amazon Q Developer</b> aporta reconocimiento de patrones de error asistido por GenAI. Cubre las tres capacidades pedidas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SageMaker + Lambda:</b> carece de soporte nativo para deteccion de errores de GenAI y de tracing distribuido; la deteccion de anomalias exigiria desarrollar modelos propios.</li>'
            '<li><b>Glue:</b> es ETL por lotes, no troubleshooting en tiempo real; suma latencia y no aporta visibilidad especifica de GenAI.</li>'
            '<li><b>Kinesis:</b> hace streaming en tiempo real, pero no da observabilidad de GenAI ni reconocimiento automatico de patrones de error.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Trazar llamadas entre servicios = X-Ray; consultar/correlacionar logs en tiempo real = CloudWatch Logs Insights; reconocimiento de patrones de error de GenAI = un asistente de GenAI para desarrolladores, no Glue (batch) ni Kinesis (streaming).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html">docs.aws AWS X-Ray</a></div>'
        ),
    ),
    # ============================================================
    # Q41 - Knowledge Base query decomposition + Bedrock flow
    # ============================================================
    card(
        question="Una app de IA generativa para salud debe cruzar terminologia medica tecnica contra documentos clinicos privados, <b>evitando la dilucion semantica</b>, a 1,000 consultas/minuto con latencia &lt; 2 s y el MENOR overhead. &iquest;Que solucion conviene?",
        options=[
            "Documentos en un indice de Amazon Kendra y un Bedrock agent que usa Step Functions para descomponer las consultas manualmente",
            "Knowledge base con query decomposition nativa para reducir la dilucion semantica y un Bedrock flow que enlaza el FM con la base",
            "Desplegar modelos ML propios de descomposicion y expansion en Amazon SageMaker AI, con los documentos en una knowledge base de Bedrock",
            "Documentos en una coleccion vectorial de OpenSearch Serverless y un Bedrock agent con plantillas de prompt, via API Gateway (Ingerir)",
        ],
        correct=1,
        key="aip02-q41",
        answer=(
            '<div class="verdict">Correcta: {{L}} - knowledge base con query decomposition nativa + Bedrock flow.</div>'
            '<p><b>El problema:</b> cruzar terminologia tecnica contra documentos privados sin diluir el sentido, con alto throughput y baja latencia y el menor overhead.</p>'
            '<p><b>Por que la respuesta sirve:</b> una <b>knowledge base</b> con <b>query decomposition</b> nativa divide las consultas complejas para reducir la dilucion semantica sin codigo propio, y un <b>Bedrock flow</b> enlaza el FM con la KB de forma eficiente. Todo gestionado, minimo overhead y baja latencia.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Kendra + Bedrock agent + Step Functions:</b> orquestar la descomposicion manualmente anade overhead y latencia, dificil de cumplir el &lt; 2 s.</li>'
            '<li><b>Modelos ML propios en SageMaker:</b> construir, entrenar y hospedar modelos de descomposicion implica enorme overhead; las funciones nativas de Bedrock lo evitan.</li>'
            '<li><b>OpenSearch Serverless + agent con prompts:</b> configurar un agente para descomponer via prompt engineering sube complejidad y latencia; los agentes sirven mejor para tool calling que como proxy RAG de alto throughput.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Reducir dilucion semantica con minimo overhead: query decomposition nativa de la Bedrock KB + Bedrock flow. Agentes/Step Functions para descomponer manualmente suman latencia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html">docs.aws Bedrock flows</a></div>'
        ),
    ),
    # ============================================================
    # Q44 - CloudTrail + Bedrock Prompt Management lineage
    # ============================================================
    card(
        question="Un sistema de resumen de feedback con Amazon Bedrock guarda prompts y resumenes en S3. Por regulacion: <b>registrar todas las interacciones con Bedrock</b>, <b>linaje</b> de cada prompt y resumen, y <b>rastrear versiones de plantilla e invocaciones de modelo</b>. &iquest;Que cumple?",
        options=[
            "Amazon Data Firehose que transmite los prompts a S3, Lambda que guarda los logs de invocacion en DynamoDB y CloudWatch para monitorear",
            "Amazon Kinesis Data Stream que captura prompts y resumenes, con Amazon Athena para consultar y auditar la metadata en S3",
            "Prompts y resumenes en Amazon DynamoDB con metadata, y DynamoDB Streams que disparan Lambdas para procesar el linaje y el seguimiento",
            "Server access logging en S3, AWS CloudTrail para la API de Bedrock y Bedrock Prompt Management para el linaje y la metadata",
        ],
        correct=3,
        key="aip02-q44",
        answer=(
            '<div class="verdict">Correcta: {{L}} - S3 server access logging + AWS CloudTrail + Bedrock Prompt Management.</div>'
            '<p><b>El problema:</b> gobernanza regulatoria con logging de las llamadas a Bedrock, linaje de prompts/resumenes y seguimiento de versiones de plantilla e invocaciones de modelo.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>CloudTrail</b> registra todas las llamadas de API a Bedrock (auditoria de compliance); el <b>server access logging</b> de S3 registra el acceso a los objetos; y <b>Bedrock Prompt Management</b> gobierna el linaje de prompts y la metadata de plantillas/modelos. Los tres cubren cada requisito.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Firehose + Lambda + CloudWatch:</b> hace streaming y monitoreo, pero no da logging de compliance nativo de las llamadas de API de Bedrock ni linaje de prompts.</li>'
            '<li><b>Kinesis + Athena:</b> permite stream y consulta, pero no gobierna las interacciones de Bedrock ni rastrea versiones de plantilla e invocaciones.</li>'
            '<li><b>DynamoDB + Streams:</b> puede guardar metadata, pero carece del logging de compliance de las llamadas de API de Bedrock y no se integra con su prompt management.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Auditar llamadas de API del servicio de inferencia = registro de auditoria inmutable de API; linaje y versiones de plantilla/modelo = el servicio gestionado de gestion de prompts; acceso a objetos = server access logging de S3.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/logging-using-cloudtrail.html">docs.aws Bedrock con CloudTrail</a></div>'
        ),
    ),
    # ============================================================
    # Q46 - Guardrails + Model Evaluations + drift monitoring
    # ============================================================
    card(
        question="Un banco lanza una solucion GenAI en Amazon Bedrock. Necesita bloquear contenido daninno, detectar alucinaciones, <b>monitoreo en tiempo real de comportamiento y drift</b> y un <b>log inmutable auditable</b>, en 60 dias, con latencia &lt; 200 ms y el MENOR overhead. &iquest;Que enfoque cumple?",
        options=[
            "Bedrock Guardrails para contenido, Model Evaluations para calidad y alucinaciones, logs en DynamoDB con TTL y metricas custom en CloudWatch para drift",
            "Lambdas propias para exactitud y seguridad, un endpoint de SageMaker Model Monitor para drift, y los pares en S3 al dashboard",
            "Bedrock Agents + Knowledge Base para grounding, un clasificador de texto propio en SageMaker, e ingestar los pares en OpenSearch con QuickSight",
            "AWS WAF ante API Gateway para inyecciones, Amazon Macie para alucinaciones y drift, interacciones en Amazon RDS Multi-AZ y CloudWatch",
        ],
        correct=0,
        key="aip02-q46",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Guardrails + Model Evaluations + DynamoDB (TTL) + CloudWatch.</div>'
            '<p><b>El problema:</b> seguridad de contenido, deteccion de alucinaciones, monitoreo de comportamiento/drift y auditoria inmutable, en 60 dias, baja latencia y minimo overhead.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> filtra contenido daninno de forma nativa; <b>Model Evaluations</b> evalua calidad y descubre alucinaciones; <b>DynamoDB con TTL</b> guarda los pares para auditoria con retencion automatica; y <b>metricas custom en CloudWatch</b> monitorean comportamiento y drift, integrando con el dashboard. Es la ruta de menor overhead que cumple todo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambdas propias + SageMaker Model Monitor:</b> filtrar toxicidad y exactitud a mano es enorme desarrollo (dificil en 60 dias) y varias Lambdas sincronas pueden exceder los 200 ms.</li>'
            '<li><b>Clasificador propio + OpenSearch + QuickSight:</b> entrenar/mantener un clasificador de seguridad y montar OpenSearch/QuickSight es mucho mas overhead que Guardrails + DynamoDB + CloudWatch.</li>'
            '<li><b>WAF + Macie + RDS:</b> WAF no evalua semanticamente el texto GenAI, Macie descubre PII en S3 (no detecta alucinaciones/drift) y RDS para logging de alta velocidad suma overhead y latencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Marco responsable con minimo overhead: el guardrail gestionado (seguridad) + evaluacion de modelos (calidad/alucinaciones) + un store con expiracion automatica (auditoria) + CloudWatch (drift). WAF/Macie no evaluan contenido GenAI.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
        ),
    ),
    # ============================================================
    # Q47 - OpenSearch Serverless vector store + Bedrock KB RAG
    # ============================================================
    card(
        question="Un asistente de compliance hace busqueda semantica sobre documentos regulatorios en tres idiomas, con <b>filtrado por metadata</b> (fecha, autoridad, categoria), ~10M de embeddings con <b>optimizacion automatica de indice</b> (sub-segundo sin tuning) y un enfoque <b>totalmente gestionado</b>. &iquest;Que solucion cumple?",
        options=[
            "Amazon OpenSearch Serverless como vector store con filtrado por metadata, y Bedrock Knowledge Bases para el RAG con un FM Anthropic Claude",
            "Un cluster Amazon Aurora PostgreSQL con pgvector: esquemas relacionales para embeddings + metadata y similitud por SQL, enviando los documentos a Bedrock",
            "Amazon Kendra como buscador empresarial con attribute filters por autoridad/fecha/categoria, conectando los resultados a Bedrock",
            "Amazon MemoryDB con vector search para 10M embeddings, con pre-filtros de metadata y resultados enviados a Bedrock",
        ],
        correct=0,
        key="aip02-q47",
        answer=(
            '<div class="verdict">Correcta: {{L}} - OpenSearch Serverless como vector store + Bedrock Knowledge Bases (RAG).</div>'
            '<p><b>El problema:</b> vector store gestionado para ~10M embeddings con filtrado por metadata, optimizacion automatica de indice (sub-segundo sin tuning manual) y minimo esfuerzo de infraestructura.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>OpenSearch Serverless</b> maneja similitud vectorial y filtrado por metadata a escala con optimizacion de indice gestionada (sin tuning manual), y <b>Bedrock Knowledge Bases</b> arma el pipeline RAG de forma nativa con un FM Claude. Es la combinacion totalmente gestionada.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Aurora PostgreSQL + pgvector:</b> almacena y consulta vectores, pero requiere gestion de infraestructura y tuning fino de SQL; no es la ruta totalmente gestionada ni la integracion nativa con Bedrock KB.</li>'
            '<li><b>Amazon Kendra:</b> no es una base vectorial ni almacena/consulta embeddings a escala de 10M; es busqueda documental empresarial, mal ajuste para RAG con vectores densos.</li>'
            '<li><b>Amazon MemoryDB:</b> soporta vector search, pero su modelo en memoria es costoso y complejo para 10M embeddings de alta dimension y no integra nativamente con Bedrock KB.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Vector store gestionado a gran escala con filtrado por metadata y pipeline de recuperacion aumentada: un vector store serverless integrado con el servicio gestionado de bases de conocimiento. Kendra no es base vectorial; Aurora/MemoryDB suman gestion.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html">docs.aws OpenSearch Serverless</a></div>'
        ),
    ),
    # ============================================================
    # Q49 - Lake Formation LF-Tags column masking + CloudTrail
    # ============================================================
    card(
        question="Una institucion financiera con un data lake en AWS Lake Formation quiere que un FM de Bedrock acceda a registros para AML, pero debe <b>enmascarar PII por columna</b>, restringir al FM a subconjuntos autorizados y <b>registrar todos los accesos</b>. &iquest;Que enfoque cumple?",
        options=[
            "Amazon Macie para clasificar PII en el S3 del data lake, S3 access points con roles IAM pre-filtrados y S3 server access logging",
            "LF-Tags en Lake Formation sobre bases, tablas y columnas; FM por rol IAM con expresiones LF-Tag que excluyen la PII, y AWS CloudTrail",
            "Reglas de AWS Glue Data Quality para PII, redaccion con Glue Studio ETL a un prefijo S3, FM por IAM y CloudWatch Logs",
            "FM con rol IAM y credenciales STS, una API middleware con presigned URLs de S3 por division y auditoria con CloudTrail",
        ],
        correct=1,
        key="aip02-q49",
        answer=(
            '<div class="verdict">Correcta: {{L}} - LF-Tags en Lake Formation (columna) + roles IAM + CloudTrail.</div>'
            '<p><b>El problema:</b> control de acceso <b>a nivel de columna</b> que excluya PII, restringir al FM a subconjuntos autorizados y auditar todos los accesos.</p>'
            '<p><b>Por que la respuesta sirve:</b> las <b>LF-Tags</b> de Lake Formation etiquetan bases, tablas y columnas; con <b>expresiones LF-Tag</b> se imponen permisos que excluyen las columnas PII del alcance del FM (autenticado por rol IAM), aplicando control dinamico a nivel de columna. <b>CloudTrail</b> registra los accesos a nivel de API.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Macie + S3 access points:</b> Macie identifica donde hay PII pero no la enmascara en tiempo de consulta; los access points operan a nivel de objeto, no de columna; y S3 access logging audita menos que CloudTrail.</li>'
            '<li><b>Glue Data Quality + ETL:</b> redacta en la ingesta produciendo copias estaticas saneadas que hay que sincronizar; no es control dinamico por columna ni usa el modelo LF-Tag, y CloudWatch de Glue no es una traza de acceso completa.</li>'
            '<li><b>STS + presigned URLs:</b> operan a nivel de objeto, no de columna, no pueden redactar campos PII; ademas la middleware suma complejidad. Aunque usa CloudTrail, sin Lake Formation no logra el enmascarado por columna.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Enmascarado/exclusion de PII a nivel de columna en un data lake = control basado en etiquetas de recurso (dinamico, en tiempo de consulta). Access points y presigned URLs son a nivel de objeto; Macie descubre, no enmascara.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html">docs.aws Lake Formation LF-Tags</a></div>'
        ),
    ),
    # ============================================================
    # Q50 - Bedrock KB hybrid search + Kendra + Personalize
    # ============================================================
    card(
        question="Un asistente de soporte debe recuperar contenido estructurado y no estructurado (manuales, tickets, notas), integrando Amazon Kendra (intencion) y Amazon Personalize (personalizacion) con generacion, de forma cohesiva y a escala. &iquest;Que solucion conviene?",
        options=[
            "Preprocesar con Bedrock Model Customizations (embeddings + plantillas) y manejar el ranking de Kendra y Personalize en pipelines separados",
            "Construir una Amazon Bedrock Knowledge Base con hybrid search, metadata de Kendra y Personalize para guiar recuperacion y recomendaciones",
            "Ingestar y transformar el contenido con Bedrock Data Automation, usar Personalize para recomendar y hacer full-text search con Kendra de forma independiente",
            "Orquestar con Bedrock Prompt Flows, Kendra y Personalize para rankear/personalizar y guardar fuera de una knowledge base central",
        ],
        correct=1,
        key="aip02-q50",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Knowledge Base con hybrid search + metadata de Kendra + Personalize.</div>'
            '<p><b>El problema:</b> unificar recuperacion (estructurada y no estructurada), personalizacion y generacion de forma cohesiva y a escala.</p>'
            '<p><b>Por que la respuesta sirve:</b> una <b>Bedrock Knowledge Base con hybrid search</b> combina busqueda semantica y por keywords en una capa central; enriquecer con <b>metadata de Kendra</b> mejora la relevancia por intencion y <b>Personalize</b> guia la recuperacion/recomendacion por usuario. Todo orquestado alrededor de la KB, no en silos.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Model Customizations + pipelines separados:</b> solo prepara embeddings/plantillas y deja Kendra y Personalize en silos, subiendo latencia y rompiendo la cohesion.</li>'
            '<li><b>BDA + Kendra/Personalize independientes:</b> BDA resuelve ETL, no relevancia de retrieval; correr Kendra y Personalize sueltos no da orquestacion central ni hybrid search nativo.</li>'
            '<li><b>Prompt Flows fuera de una KB:</b> los flows gestionan el workflow, no un motor de retrieval hibrido; guardar fuera de una KB central desconecta el scoring de relevancia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Retrieval cohesivo estructurado + no estructurado = Bedrock KB con hybrid search como capa central; enriquece con metadata (Kendra) y personaliza (Personalize). Correr servicios en silos degrada relevancia y latencia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-hybrid-search.html">docs.aws Bedrock KB hybrid search</a></div>'
        ),
    ),
    # ============================================================
    # Q51 - Guardrails sensitive info filter mask/block por region
    # ============================================================
    card(
        question="Una firma financiera evalua su chatbot en Amazon Bedrock. La residencia <b>prohibe inferencia cross-Region</b> (todo en la Region del cliente) y compliance quiere una evaluacion estructurada de cuan bien el chatbot <b>identifica y suprime PII</b> en las respuestas. &iquest;Que solucion cumple?",
        options=[
            "Logs de conversacion en S3 cifrados, Amazon Macie para escanear PII y un flujo de Step Functions que redacte antes de los reportes",
            "Bedrock Guardrail con sensitive information filters in/out, mask mode en evaluacion, block mode en produccion y una instancia por Region",
            "Activar Guardrails con sensitive information filters en detect mode, salidas a Kinesis Data Stream y PII redactada con un job de AWS Glue",
            "Content y word filters en un guardrail de Bedrock cross-Region, detect mode en evaluacion y mask mode en produccion",
        ],
        correct=1,
        key="aip02-q51",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Guardrail con sensitive information filters (mask en eval, block en prod) por Region.</div>'
            '<p><b>El problema:</b> evaluar la supresion de PII en las respuestas y respetar la residencia (nada de inferencia cross-Region).</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>sensitive information filters</b> de Guardrails detectan/suprimen PII en entradas y salidas. Usar <b>mask mode</b> en evaluacion permite medir la efectividad de la supresion; pasar a <b>block mode</b> en produccion la refuerza; y una instancia de guardrail <b>por Region</b> mantiene la residencia (sin cross-Region).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>S3 + Macie + Step Functions:</b> procesa tras almacenar, o sea la PII puede llegar al usuario antes de redactarse; no es filtrado en tiempo real de las respuestas del modelo.</li>'
            '<li><b>Detect mode + Kinesis + Glue:</b> detect mode no toma accion correctiva (no suprime PII) y Glue redacta asincronamente, dejando pasar PII a los usuarios.</li>'
            '<li><b>Guardrail cross-Region con content/word filters:</b> content/word filters bloquean categorias/frases, no PII contextual (nombres, cuentas); y cross-Region viola la residencia de datos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Suprimir PII = sensitive information filters (no content/word filters). Evaluar efectividad = mask mode; hacer cumplir = block mode. detect mode no actua. Residencia = un guardrail por Region, nada cross-Region.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-sensitive-filters.html">docs.aws Guardrails sensitive information filters</a></div>'
        ),
    ),
    # ============================================================
    # Q52 - Bedrock model invocation logging a S3
    # ============================================================
    card(
        question="Un chatbot llama a Bedrock InvokeModel desde Lambda. En produccion hay salidas inesperadas y <b>no hay visibilidad</b> de los prompts ni las respuestas crudas. Hace falta loggear el <b>contenido completo de prompts y completions</b> de cada llamada <b>sin tocar la logica de negocio</b>. &iquest;Que enfoque es mas efectivo?",
        options=[
            "Sentencias de logging de CloudWatch en la Lambda que registran la entrada y la respuesta de InvokeModel",
            "Usar AWS X-Ray para trazar las ejecuciones de la Lambda e identificar demoras en las llamadas a InvokeModel",
            "Model invocation logging de Bedrock que captura prompts y respuestas crudos via InvocationLogsConfig hacia Amazon S3",
            "Enrutar las solicitudes de InvokeModel por Amazon EventBridge para capturar eventos y monitorear las invocaciones",
        ],
        correct=2,
        key="aip02-q52",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock model invocation logging a Amazon S3.</div>'
            '<p><b>El problema:</b> capturar el contenido completo (prompts y completions crudos) de cada invocacion a Bedrock, sin tocar la logica de negocio.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>model invocation logging</b> de Bedrock registra de forma nativa los prompts y respuestas exactos que recibe/devuelve el modelo, entregandolos a S3 mediante InvocationLogsConfig. Es a nivel de servicio, asi que no requiere cambiar el codigo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Logging en la Lambda:</b> solo captura lo que la Lambda maneja, no el contenido exacto que Bedrock recibe/devuelve, y exige modificar el codigo; insuficiente para auditar el completion crudo.</li>'
            '<li><b>X-Ray:</b> es para rendimiento/latencia y trazas; no captura el contenido crudo de prompts o salidas.</li>'
            '<li><b>EventBridge:</b> captura eventos/metadata de las invocaciones, no el contenido completo de solicitud y respuesta.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Auditar el contenido crudo de prompts/respuestas sin tocar codigo: el model invocation logging nativo del servicio (entregado a S3). Loggear en la Lambda no captura lo que el modelo realmente recibio/devolvio; X-Ray solo mide latencia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html">docs.aws Bedrock model invocation logging</a></div>'
        ),
    ),
    # ============================================================
    # Q53 - MemoryDB vector search para semantic caching
    # ============================================================
    card(
        question="Un agente de soporte usa embeddings propios (SageMaker JumpStart) y Amazon Bedrock. Recibe miles de consultas casi duplicadas al dia y cada invocacion cuesta y agrega latencia. Se quiere <b>reconocer consultas similares ya respondidas y servir la cacheada</b>, generando fresco solo ante preguntas nuevas. &iquest;Que solucion cumple?",
        options=[
            "Store clave-valor en memoria que cachea strings exactos de request/respuesta y llama al FM solo ante miss de clave",
            "Embeddings pre-computados en SageMaker guardados en una base relacional, con busqueda por coincidencia exacta de string",
            "Embeddings de consultas y respuestas en Amazon MemoryDB con vector search, aplicando semantic caching para servir respuestas cacheadas",
            "Amazon Kendra que indexa consultas y respuestas y recupera consultas similares antes de invocar el FM",
        ],
        correct=2,
        key="aip02-q53",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon MemoryDB con vector search + semantic caching.</div>'
            '<p><b>El problema:</b> reducir llamadas al FM reconociendo consultas equivalentes en significado (no solo texto identico) y sirviendolas rapido desde cache.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Amazon MemoryDB con vector search</b> guarda embeddings de los pares consulta-respuesta y permite <b>semantic caching</b>: busca el vecino mas cercano por significado y, si es suficientemente similar, devuelve la respuesta cacheada con baja latencia, invocando el FM solo ante preguntas realmente nuevas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Store en memoria por string exacto:</b> solo casa strings identicos; no reconoce parafraseos (por ejemplo, "resetear contrasena" vs "cambiar credenciales").</li>'
            '<li><b>Embeddings en base relacional por match exacto:</b> aunque usa embeddings, sigue comparando strings exactos, lo que anula el proposito de la similitud semantica; las bases relacionales no estan optimizadas para busqueda vectorial.</li>'
            '<li><b>Amazon Kendra:</b> esta pensado para recuperacion de documentos/FAQ, no para cache semantica de baja latencia y alto throughput de consultas conversacionales.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Semantic caching de baja latencia: un store con vector search. El match exacto (in-memory o relacional) no capta parafraseos; Kendra es para busqueda documental, no para cache.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/memorydb/latest/devguide/vector-search.html">docs.aws MemoryDB vector search</a></div>'
        ),
    ),
    # ============================================================
    # Q54 - Provisioned throughput + Guardrails + Prompt Management
    # ============================================================
    card(
        question="Una app usa Amazon Bedrock con una cadena de prompts de tres etapas. Presenta recomendaciones <b>inconsistentes para entradas identicas</b>, alta latencia y <b>salidas inseguras</b>. Hay que desplegar controles validados, garantizar <b>consistencia &gt;= 99.5%</b> y latencia &lt; 1 s. &iquest;Que solucion cumple todo?",
        options=[
            "Bedrock provisioned throughput para latencia consistente, Guardrails con denegacion semantica contra salidas inseguras y Prompt Management con aprobacion",
            "Correr model evaluation en las tres etapas, un modelo de validacion en un endpoint SageMaker y alarmas de CloudWatch para rollbacks",
            "Cache de repetidas en Amazon ElastiCache, preprocesar con Lambda por etapa y AWS X-Ray para la latencia extremo a extremo",
            "Prompt compression para reducir tokens, Bedrock Agents para orquestar y Amazon Comprehend para marcar formulaciones fuera de umbrales",
        ],
        correct=0,
        key="aip02-q54",
        answer=(
            '<div class="verdict">Correcta: {{L}} - provisioned throughput + Guardrails (denegacion semantica) + Prompt Management (aprobacion/versionado).</div>'
            '<p><b>El problema:</b> tres exigencias a la vez: seguridad validada de salidas, consistencia &gt;= 99.5% para entradas identicas y latencia &lt; 1 s.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>provisioned throughput</b> da capacidad reservada y latencia consistente; <b>Guardrails con reglas de denegacion semantica</b> es el control validado que bloquea salidas inseguras; y <b>Prompt Management con flujos de aprobacion y versionado</b> gobierna las plantillas, que es la raiz de la inconsistencia (prompts no gobernados). Cubre las tres metas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Model evaluation + validacion en SageMaker + rollback:</b> la evaluacion es offline por lotes, no garantiza consistencia en vivo; el modelo secundario suma latencia; y los rollbacks son reactivos (la salida inconsistente ya llego).</li>'
            '<li><b>ElastiCache + Lambda + X-Ray:</b> la cache solo cubre entradas repetidas y no garantiza 99.5% en todo el espacio de entradas; Lambda por etapa puede subir la latencia y X-Ray solo observa, no corrige; ademas falta el control de seguridad validado.</li>'
            '<li><b>Prompt compression + Agents + Comprehend:</b> la compresion no impone consistencia, los agentes no resuelven la falta de plantillas gobernadas y Comprehend no es un control de seguridad validado para bloquear salidas inseguras.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Consistencia de salidas = gobernar y versionar los prompts. Latencia consistente = capacidad reservada de inferencia. Bloqueo validado de salidas inseguras = el guardrail con reglas de denegacion semantica (no Comprehend, ni evaluacion offline).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html">docs.aws Bedrock provisioned throughput</a></div>'
        ),
    ),
    # ============================================================
    # Q55 - Aurora pgvector HNSW como vector store para RAG
    # ============================================================
    card(
        question="Un proveedor industrial genera embeddings con SageMaker y responde via Bedrock. Almacena millones de registros y requiere recuperacion semantica <b>mas filtrado por metadata relacional</b> (equipo, fecha, severidad), busqueda ANN de alta velocidad e <b>integracion directa con el entorno relacional</b>. &iquest;Que solucion cumple?",
        options=[
            "pgvector en Amazon Aurora (PostgreSQL Compatible) con indice HNSW, join con las tablas de metadata y recuperacion desde Bedrock",
            "Amazon OpenSearch Service con motor K-NN, embeddings de SageMaker, metadata en el indice e IDs de documento a Bedrock",
            "Desplegar PostgreSQL con embeddings como arrays o JSON, UDFs para similitud coseno en runtime, join con metadata y recuperacion desde Bedrock",
            "Usar SageMaker Feature Store para embeddings y metadata y, en consulta, un endpoint real-time de SageMaker que calcula vecinos para Bedrock",
        ],
        correct=0,
        key="aip02-q55",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Aurora PostgreSQL con pgvector + indice HNSW + join con metadata relacional.</div>'
            '<p><b>El problema:</b> busqueda ANN de alta velocidad sobre millones de embeddings con <b>filtrado por metadata relacional</b> e integracion estrecha con ese entorno relacional.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>pgvector</b> en Amazon Aurora almacena los embeddings en una columna; un indice <b>HNSW</b> da ANN rapido; y como es una base relacional, los <b>joins SQL</b> combinan la similitud con la metadata (tipo, fecha, severidad) de forma nativa y expresiva. Cumple carga eficiente, ANN y la integracion relacional pedida.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>OpenSearch K-NN:</b> soporta busqueda vectorial, pero su filtrado por metadata es menos expresivo/performante que los joins SQL y carece de la integracion relacional estrecha que exige el escenario.</li>'
            '<li><b>PostgreSQL con arrays/JSON + UDFs:</b> calcular similitud con UDFs en runtime es ineficiente y sin indice ANN escala mal con millones de registros.</li>'
            '<li><b>Feature Store + endpoint real-time:</b> Feature Store no esta optimizado para busqueda de similitud; usar inferencia para kNN suma latencia y complejidad.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Busqueda vectorial + metadata relacional expresiva e integrada: una base relacional con extension de vectores e indice de vecinos aproximados (joins por SQL). Arrays/JSON + UDFs no escalan (sin ANN); un feature store no es un vector store.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html">docs.aws Aurora PostgreSQL pgvector</a></div>'
        ),
    ),
    # ============================================================
    # Q58 - Invocation logs + Guardrails grounding + anomaly tokens
    # ============================================================
    card(
        question="Una app medica en Amazon Bedrock resume registros y sufre <b>alucinaciones factuales</b>; el gasto supera el presupuesto 40%. Se necesita observabilidad casi en tiempo real para <b>descubrir alucinaciones</b>, monitorear tokens y alertar por picos de costo, con el MENOR overhead. &iquest;Que solucion cumple?",
        options=[
            "Alarmas de CloudWatch sobre InputTokenCount/OutputTokenCount, invocation logs a S3 con captura de texto y AWS Glue + Athena para detectar alucinaciones",
            "Bedrock Model Evaluation en jobs continuos para alucinaciones e invocation logs a CloudWatch Logs con Logs Insights para picos de tokens",
            "Model invocation logs de Bedrock (text output) a Amazon S3, Guardrails con contextual grounding checks y anomaly detection de CloudWatch sobre tokens",
            "Bedrock agent con Action Group de Lambda que valida alucinaciones, e invocation logs a Amazon OpenSearch con alertas propias sobre los tokens",
        ],
        correct=2,
        key="aip02-q58",
        answer=(
            '<div class="verdict">Correcta: {{L}} - invocation logs a S3 + Guardrails contextual grounding + CloudWatch anomaly detection.</div>'
            '<p><b>El problema:</b> detectar alucinaciones casi en tiempo real, monitorear tokens y alertar por costo, con minimo overhead.</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>model invocation logs con text output</b> centralizan prompts/respuestas en S3; los <b>contextual grounding checks</b> de Guardrails marcan inexactitudes factuales en linea (detectan alucinaciones); y las <b>alarmas de anomaly detection</b> de CloudWatch baselinean el uso de tokens para avisar de picos de costo. Todo nativo, sin scripting pesado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Glue + Athena:</b> es analisis batch/asincrono, no casi en tiempo real para alucinaciones; y escribir ETL/SQL propio suma overhead; los umbrales estaticos son menos precisos que anomaly detection.</li>'
            '<li><b>Model Evaluation continuo + Logs Insights:</b> Model Evaluation es benchmarking puntual, no deteccion inline en vivo; y Logs Insights exige correr o programar queries a mano en vez de alarmas automaticas.</li>'
            '<li><b>Agent + Lambda + OpenSearch:</b> validar con Lambda propia y montar OpenSearch anade desarrollo, latencia y gestion de infraestructura frente a grounding nativo y CloudWatch.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Detectar alucinaciones inline = los contextual grounding checks del guardrail gestionado. Picos de tokens/costo = CloudWatch anomaly detection (baseline, no umbral fijo). Glue/Athena es batch; Model Evaluation es offline.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html">docs.aws contextual grounding del guardrail</a></div>'
        ),
    ),
    # ============================================================
    # Q59 - Semantic caching de prompts
    # ============================================================
    card(
        question="Un pipeline GenAI multi-region invoca el FM desde flujos recurrentes con prompts <b>redactados distinto pero con el mismo intento</b>, causando sobrecostos y latencia. Se necesita caching que <b>evite llamadas redundantes para prompts del mismo significado</b>, con claves consistentes. &iquest;Que estrategia conviene?",
        options=[
            "Implementar hashing determinista de solicitudes generando hashes unicos y repetibles del contenido del prompt",
            "Implementar semantic caching que empareje prompts semanticamente similares y reutilice las salidas del modelo",
            "Implementar edge caching para guardar las salidas del FM en ubicaciones edge distribuidas geograficamente",
            "Implementar prompt caching guardando cada prompt exacto y su salida correspondiente",
        ],
        correct=1,
        key="aip02-q59",
        answer=(
            '<div class="verdict">Correcta: {{L}} - semantic caching que empareja prompts similares en significado.</div>'
            '<p><b>El problema:</b> evitar invocaciones redundantes cuando prompts distintos en redaccion expresan el mismo intento.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>semantic caching</b> compara el significado (via embeddings) y reutiliza la salida cuando un nuevo prompt es suficientemente similar a uno previo, sin importar la redaccion. Reduce costo y latencia justo para el patron descrito.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Hashing determinista:</b> el hash cambia ante minimas variaciones de texto, asi que no reconoce prompts equivalentes con otra redaccion.</li>'
            '<li><b>Edge caching:</b> acerca resultados geograficamente para bajar latencia, pero no resuelve las invocaciones redundantes por prompts no identicos.</li>'
            '<li><b>Prompt caching exacto:</b> solo sirve la salida ante un prompt identico; falla ante parafraseos, que es el nucleo del problema.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Mismo intento, distinta redaccion: semantic caching (embeddings). Hashing y prompt caching exacto solo capturan coincidencias identicas; edge caching es geografico.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html">docs.aws Bedrock prompt caching</a></div>'
        ),
    ),
    # ============================================================
    # Q60 - Invocation logging + Guardrails grounding + token anomaly
    # ============================================================
    card(
        question="Una financiera usa Amazon Bedrock para resumir evaluaciones de riesgo. Aun con limites de longitud, hay <b>detalles financieros fabricados</b> y el costo excede la proyeccion 35%. Se necesita monitoreo casi en tiempo real para detectar alucinaciones, consumo anormal de tokens y anomalias de costo, con minimo desarrollo. &iquest;Que solucion cumple?",
        options=[
            "Alarmas de CloudWatch sobre InputTokenCount y OutputTokenCount, invocation logs en S3 y AWS Glue con Athena para analizar salidas y detectar alucinaciones",
            "Amazon Comprehend para inconsistencias factuales y una regla de EventBridge que enrute las metricas de tokens a un topico de Amazon SNS",
            "Model invocation logging con text output en S3, Guardrails con contextual grounding check para alucinaciones y anomaly detection de CloudWatch sobre tokens",
            "Invocation logs a Amazon OpenSearch via Firehose, con el plugin de Observability para dashboards y reglas de anomalia propias de tokens",
        ],
        correct=2,
        key="aip02-q60",
        answer=(
            '<div class="verdict">Correcta: {{L}} - invocation logging (text output) + Guardrails contextual grounding + CloudWatch anomaly detection.</div>'
            '<p><b>El problema:</b> detectar alucinaciones en tiempo casi real, identificar consumo anormal de tokens y alertar de costo, con minimo desarrollo/mantenimiento.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>model invocation logging con text output</b> centraliza las interacciones en S3; el <b>contextual grounding check</b> de Guardrails marca inexactitudes en linea; y las <b>alarmas de anomaly detection</b> de CloudWatch baselinean los tokens para detectar picos anormales (incluidos posibles prompt injections) y avisar de costo. Todo nativo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Glue + Athena:</b> opera en batch y no detecta alucinaciones en tiempo de inferencia; los umbrales estaticos de CloudWatch no baselinean el consumo como anomaly detection.</li>'
            '<li><b>Comprehend + EventBridge/SNS:</b> Comprehend no hace grounding de alucinaciones de FM, y un pipeline EventBridge-SNS sin anomaly detection no distingue picos genuinos de uso normal.</li>'
            '<li><b>OpenSearch + Observability:</b> introduce mucho overhead (cluster, streams, reglas propias) y su analisis es retrospectivo, no inline como el grounding de Guardrails.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Alucinaciones inline = contextual grounding check del guardrail; tokens anormales/costo = CloudWatch anomaly detection; contenido crudo = invocation logging a S3. Comprehend no hace grounding de un FM.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html">docs.aws Guardrails contextual grounding</a></div>'
        ),
    ),
    # ============================================================
    # Q61 - Bedrock agent action group Lambda con OAuth
    # ============================================================
    card(
        question="Un asistente en Amazon Bedrock trae datos de una REST API interna cuya API key <b>expira cada 30 minutos</b> y se refresca dinamicamente desde un proveedor OAuth. Se integra en un metodo de Amazon API Gateway, con acceso seguro y baja latencia. &iquest;Cual es el mejor enfoque?",
        options=[
            "API Gateway con Lambda por proxy: la Lambda autentica via OAuth y pasa el token fresco como header al Bedrock agent",
            "Lambda con API Gateway que genera el token OAuth y lo inyecta como header custom, invocando la Lambda hacia el agente",
            "Amazon CloudFront que cachea las credenciales OAuth, una Lambda que lee el token y llama a la API, y API Gateway la invoca",
            "Lambda del action group del Bedrock agent genera el token OAuth y llama a la REST API; API Gateway usa InvokeAgent y IAM",
        ],
        correct=3,
        key="aip02-q61",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Lambda en el action group del agente maneja OAuth + API Gateway usa InvokeAgent.</div>'
            '<p><b>El problema:</b> refrescar dinamicamente un token OAuth y llamar a una API externa desde un asistente de Bedrock, integrado en API Gateway, con seguridad y baja latencia.</p>'
            '<p><b>Por que la respuesta sirve:</b> una <b>Lambda del action group</b> del Bedrock agent es el lugar correcto para generar el token OAuth y llamar a la REST API (separa la gestion del token del flujo del agente). El metodo de API Gateway usa la <b>InvokeAgent API</b> para comunicarse con el agente, con los permisos IAM apropiados.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda proxy:</b> el proxy sirve para reenviar solicitudes al backend, no para gestionar generacion dinamica de tokens e interactuar con el agente; complica el flujo con capas extra.</li>'
            '<li><b>Lambda que inyecta token como header:</b> mezcla la logica del token con el flujo principal del agente en una sola funcion, reduciendo separacion de responsabilidades; lo correcto es la Lambda del action group + InvokeAgent.</li>'
            '<li><b>CloudFront cacheando tokens:</b> CloudFront es para contenido estatico, no para cachear credenciales OAuth dinamicas; introduce riesgo de seguridad y latencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Integrar un agente con una API externa que requiere tokens: la Lambda del action group maneja OAuth y la llamada, y API Gateway invoca al agente por su API dedicada. No caches tokens dinamicos en CloudFront.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-create.html">docs.aws Bedrock agent action groups</a></div>'
        ),
    ),
    # ============================================================
    # Q62 - InvokeModelWithResponseStream sobre WebSocket API
    # ============================================================
    card(
        question="Un asistente de inversiones en Amazon Bedrock procesa cada peticion por completo antes de responder, causando demoras. Se quiere entregar <b>respuestas parciales/preliminares mientras el modelo sigue procesando</b>, con el MENOR esfuerzo de desarrollo. &iquest;Que solucion cumple?",
        options=[
            "Un HTTP API con API Gateway y Lambda, Step Functions en paralelo, resultados parciales en DynamoDB y un DynamoDB Stream con Lambda",
            "WebSocket API de Amazon API Gateway con Lambda, usando InvokeModelWithResponseStream de Bedrock para transmitir resultados por WebSockets a los clientes",
            "REST API con API Gateway y Lambda que usa InvokeModel secuencial, guarda en S3 y expone polling del cliente via setInterval",
            "Un API en tiempo real con AWS AppSync y resolvers Lambda, un esquema GraphQL e InvokeModel con suscripciones para clientes",
        ],
        correct=1,
        key="aip02-q62",
        answer=(
            '<div class="verdict">Correcta: {{L}} - WebSocket API + InvokeModelWithResponseStream.</div>'
            '<p><b>El problema:</b> mostrar resultados parciales en streaming mientras el FM genera, con el menor desarrollo.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>InvokeModelWithResponseStream</b> expone los chunks de la respuesta a medida que se generan, y un <b>WebSocket API</b> de API Gateway mantiene una conexion bidireccional persistente para empujar esos updates al cliente sin polling. Es la ruta directa y de menor esfuerzo para streaming en tiempo real.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>HTTP API + Step Functions + DynamoDB Stream:</b> Step Functions es para orquestar workflows y agrega complejidad/latencia; los triggers de Stream no dan feedback continuo durante el analisis.</li>'
            '<li><b>REST + InvokeModel + polling:</b> InvokeModel devuelve la respuesta completa (sin streaming) y el polling agrega latencia; S3 no es para streaming en tiempo real.</li>'
            '<li><b>AppSync + InvokeModel:</b> GraphQL/suscripciones anaden complejidad y overhead frente a WebSockets, y usar InvokeModel (no la version stream) no entrega chunks parciales.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Streaming de respuestas del FM al cliente: la API de invocacion con respuesta en streaming + una API de socket bidireccional de API Gateway. La invocacion normal devuelve todo de una; el polling y GraphQL suman latencia y complejidad.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/api-methods-run.html">docs.aws Bedrock InvokeModelWithResponseStream</a></div>'
        ),
    ),
    # ============================================================
    # Q64 - Comprehend toxicity + PII redaction + prompt safety (parallel)
    # ============================================================
    card(
        question="Un portal de soporte filtra mensajes con Amazon Comprehend antes del FM de Bedrock: suprimir lenguaje ofensivo, <b>redactar PII</b> y marcar solicitudes de consejo inapropiado. El pipeline debe completar en el preprocesamiento <b>sin retrasar la invocacion del FM</b>. &iquest;Que arquitectura cumple?",
        options=[
            "Correr todo en paralelo con APIs asincronas: toxicity detection, prompt safety classification y PII detection con redaccion antes del FM",
            "Una Lambda que evalue cada mensaje contra una blocklist en DynamoDB y luego toxicity detection, reenviando los limpios al FM (logs en S3)",
            "Una cola SQS que bufferee mensajes, una Lambda con Comprehend PII que guarde versiones en S3, y Bedrock Guardrails con topic filters",
            "Toxicity detection con umbral 0.5, prompt safety classification y PII detection con redaccion en paralelo, con alarmas de CloudWatch antes del FM",
        ],
        correct=3,
        key="aip02-q64",
        answer=(
            '<div class="verdict">Correcta: {{L}} - toxicity (umbral 0.5) + prompt safety + PII redaction en paralelo + alarmas de CloudWatch.</div>'
            '<p><b>El problema:</b> tres filtros de Comprehend (ofensivo, PII, consejo inapropiado) que completen en el preprocesamiento sin retrasar la invocacion del FM.</p>'
            '<p><b>Por que la respuesta sirve:</b> ejecutar <b>toxicity detection con umbrales calibrados (0.5)</b>, <b>prompt safety classification</b> y <b>PII detection con redaccion</b> en <b>paralelo</b> cubre las tres necesidades minimizando latencia, y las <b>alarmas de CloudWatch</b> vigilan que el pipeline se mantenga dentro de la ventana de preprocesamiento bajo carga.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Paralelo sin umbrales ni monitoreo:</b> no define umbrales de deteccion calibrados (por ejemplo, 0.5) ni un mecanismo (alarmas de CloudWatch) para asegurar que el preprocesamiento termine a tiempo bajo carga.</li>'
            '<li><b>Blocklist en DynamoDB + toxicity secuencial:</b> una blocklist estatica no detecta contenido ofensivo matizado, patrones de consejo inapropiado ni PII; ademas omite PII/redaccion y correr secuencial suma latencia.</li>'
            '<li><b>SQS + Guardrails topic filters:</b> la cola SQS agrega latencia asincrona y aplicar Guardrails ocurre en el borde del modelo, no como paso previo; ademas omite toxicity detection.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Filtrado previo multicapa con Comprehend y baja latencia: toxicity (umbral calibrado) + prompt safety + PII redaction EN PARALELO, con alarmas de monitoreo vigilando el SLA del preprocesamiento. Blocklists estaticas y colas SQS no encajan.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/trust-safety.html">docs.aws Comprehend toxicity y prompt safety</a></div>'
        ),
    ),
    # ============================================================
    # Q66 - Prompt Management parametrizado + Guardrails + CloudTrail
    # ============================================================
    card(
        question="Una agencia necesita en Bedrock Prompt Management plantillas reutilizables y <b>parametrizadas</b> (tono, features, guias), imponer <b>reglas de estilo estrictas</b> (restricciones de tono, exclusion de keywords), y <b>rastrear uso/cambios para compliance</b> con un proceso formal de revision y aprobacion antes de activar. &iquest;Que solucion cumple?",
        options=[
            "Plantillas parametrizadas por cliente con versionado y proceso formal de revision, Bedrock Guardrails para el estilo y Amazon CloudWatch para monitorear uso",
            "Bedrock Guardrails para las guias de estilo, AWS CloudTrail para logs de uso y cambios, y versionado para gestionar actualizaciones",
            "Plantillas parametrizadas por cliente con versionado y revision formal, Bedrock Guardrails para imponer estilo y AWS CloudTrail para rastrear cambios y uso",
            "Plantillas parametrizadas en Prompt Management con versionado, Amazon Comprehend para imponer estilo (tono, keywords) y AWS CloudTrail para monitorear cambios",
        ],
        correct=2,
        key="aip02-q66",
        answer=(
            '<div class="verdict">Correcta: {{L}} - plantillas parametrizadas + versionado + revision formal + Guardrails + CloudTrail.</div>'
            '<p><b>El problema:</b> plantillas parametrizadas reutilizables, estilo estricto impuesto, y auditoria de compliance con revision/aprobacion formal antes de activar.</p>'
            '<p><b>Por que la respuesta sirve:</b> las <b>plantillas parametrizadas con versionado y proceso formal de revision</b> cubren la reutilizacion y la gobernanza de cambios; <b>Bedrock Guardrails</b> impone tono y exclusion de keywords; y <b>AWS CloudTrail</b> da la auditoria a nivel de API de uso y modificaciones. Combina los tres requisitos correctamente.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Con CloudWatch en vez de CloudTrail:</b> CloudWatch es para metricas operativas, no un registro de auditoria con la granularidad de compliance que da CloudTrail.</li>'
            '<li><b>Sin proceso formal de revision:</b> omite la revision/aprobacion antes de activar; no cumple el requisito de gobernanza de cambios.</li>'
            '<li><b>Comprehend para el estilo:</b> Comprehend analiza tono/sentimiento pero no impone restricciones ni exclusiones; el control de estilo es Bedrock Guardrails.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Imponer estilo = Bedrock Guardrails (no Comprehend). Auditoria de compliance de API = CloudTrail (no CloudWatch). Gobernanza de cambios = versionado + revision/aprobacion formal.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
        ),
    ),
    # ============================================================
    # Q67 - ApplyGuardrail por grupo Cognito + KB sync + S3 lifecycle
    # ============================================================
    card(
        question="Un asistente sobre una Bedrock KB con datos clinicos debe: mostrar PII solo a investigadores autorizados y <b>redactarla automaticamente a los auditores</b>, y referenciar solo documentos de los ultimos 3 anos. Los reportes llegan a S3 y Cognito autentica. &iquest;Que enfoque cumple?",
        options=[
            "Lambda que invoque Amazon Rekognition al subir cada documento, KBs separadas por rol via grupo de Cognito y S3 Lifecycle a 3 anos",
            "Bedrock agent con action group que lee el grupo de Cognito y usa Amazon Comprehend para PII, con S3 Lifecycle de 3 anos",
            "S3 Lifecycle a los 3 anos, Lambda que sincroniza la KB y la ApplyGuardrail API que redacta PII por grupo de Cognito",
            "S3 Lifecycle de 3 anos, una Lambda que empuje archivos a la KB primaria y otra KB pre-redactada via Comprehend por Cognito",
        ],
        correct=2,
        key="aip02-q67",
        answer=(
            '<div class="verdict">Correcta: {{L}} - ApplyGuardrail por grupo de Cognito en tiempo de consulta + KB sync + S3 Lifecycle.</div>'
            '<p><b>El problema:</b> visibilidad de PII por rol sobre una misma KB, ventana de 3 anos y autenticacion con Cognito, con minimo overhead.</p>'
            '<p><b>Por que la respuesta sirve:</b> la <b>ApplyGuardrail API</b> aplica redaccion de PII en tiempo de sesion segun el <b>grupo de Cognito</b>, sin duplicar KBs ni redactar en la ingesta; <b>S3 Lifecycle</b> expira lo mayor a 3 anos y una Lambda programada sincroniza la KB. Una sola fuente autoritativa, rol-aware.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Rekognition + KBs por rol:</b> Rekognition es vision (imagenes/video), no redacta PII en texto; y KBs separadas por rol anaden overhead operativo innecesario.</li>'
            '<li><b>Agent + Comprehend por consulta:</b> Comprehend puede redactar, pero invocar ese pipeline propio en cada consulta suma latencia y complejidad, duplicando lo que Guardrails ya hace nativo.</li>'
            '<li><b>Dos KBs (primaria y pre-redactada):</b> duplica infraestructura y sincronizacion, y pre-redactar borra el contexto PII de forma permanente, limitando la flexibilidad futura.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Redaccion de PII por rol sobre una sola base de conocimiento: aplicar el guardrail en tiempo de consulta segun el grupo del usuario. Rekognition no lee PII de texto; duplicar bases o redactar en la ingesta suma overhead o pierde contexto.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html">docs.aws ApplyGuardrail API</a></div>'
        ),
    ),
    # ============================================================
    # Q68 - AWS Strands Agents SDK agente autonomo
    # ============================================================
    card(
        question="Una firma quiere un <b>agente de investigacion autonomo</b>: ante una transaccion marcada, invoca inferencia en SageMaker AI, trae imagenes de Rekognition, llama APIs internas y decide escalar o cerrar la cuenta. Necesita <b>herramientas personalizadas</b> y <b>seleccion de multiples FMs</b>. &iquest;Que solucion es la mas apropiada?",
        options=[
            "Usar Amazon Bedrock Agents con action groups predefinidos para SageMaker AI y Rekognition, dejando que el agente orqueste los pasos",
            "El AWS Strands Agents SDK para un agente autonomo que integre SageMaker AI, Rekognition y APIs internas, con un FM de Bedrock",
            "Un orquestador Lambda con AWS Step Functions hacia SageMaker, Rekognition y APIs internas, con un motor de reglas para el escalado",
            "SageMaker AI Pipelines que ejecuten la inferencia y el chequeo de Rekognition, con causal chain prompting embebido en el modelo para decidir",
        ],
        correct=1,
        key="aip02-q68",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS Strands Agents SDK para un agente autonomo personalizado.</div>'
            '<p><b>El problema:</b> un agente autonomo que razone y decida, con integraciones de herramientas personalizadas (APIs internas) y eleccion de multiples FMs.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>AWS Strands Agents SDK</b> permite construir agentes autonomos a medida con maxima flexibilidad: integra SageMaker, Rekognition y APIs internas como herramientas propias y deja seleccionar el FM via Bedrock para el razonamiento y la decision. Cubre justo los requisitos de personalizacion y multi-modelo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bedrock Agents con action groups predefinidos:</b> ofrecen menos flexibilidad para integrar APIs internas arbitrarias y para seleccionar dinamicamente entre multiples FMs en investigaciones complejas.</li>'
            '<li><b>Lambda + Step Functions + motor de reglas:</b> orquesta, pero carece de razonamiento autonomo; un motor de reglas es estatico y no adapta como un FM.</li>'
            '<li><b>SageMaker Pipelines + causal chain prompting:</b> los pipelines son para flujos ML, no para orquestar un agente autonomo multi-servicio; embeber la decision por prompting es fragil y poco modular.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Agente autonomo con herramientas personalizadas y eleccion de varios modelos: un kit de desarrollo de agentes a medida. Un orquestador con motor de reglas no razona; los action groups predefinidos son menos flexibles.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html">docs.aws agentes en AWS</a></div>'
        ),
    ),
    # ============================================================
    # Q71 - Bedrock Custom Model Import + Provisioned Throughput
    # ============================================================
    card(
        question="Una biotech tiene un modelo Llama personalizado (entrenado en SageMaker, formato Hugging Face .safetensors en S3) y quiere desplegarlo en Amazon Bedrock. La carga es <b>predecible</b> y se busca <b>no gestionar infraestructura</b> con inferencia de <b>baja latencia y alto throughput</b>. &iquest;Que solucion conviene?",
        options=[
            "Convertir el modelo a formato ONNX en Amazon EC2 Auto Scaling Groups con un load balancer al frente para escalar la inferencia",
            "Importar el modelo Hugging Face desde S3 con Bedrock Custom Model Import y desplegarlo con inferencia on-demand de pago por uso",
            "Usar Bedrock Custom Model Import para el modelo Llama .safetensors desde S3, desplegado con Bedrock Provisioned Throughput para inferencia de baja latencia",
            "Importar el modelo Llama afinado en SageMaker Serverless Inference para escalado automatico y pago por uso ante cargas fluctuantes",
        ],
        correct=2,
        key="aip02-q71",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Custom Model Import + Provisioned Throughput.</div>'
            '<p><b>El problema:</b> desplegar un modelo propio en Bedrock, sin gestionar infraestructura, con latencia consistente y alto throughput concurrente ante carga predecible.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Custom Model Import</b> trae el modelo Llama en formato Hugging Face (.safetensors) desde S3 al entorno gestionado de Bedrock, y <b>Provisioned Throughput</b> reserva capacidad para garantizar latencia baja y consistente a escala, ideal para una carga predecible.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>ONNX en EC2 Auto Scaling:</b> exige gestion total de infraestructura (parches, monitoreo, escalado); no aprovecha el despliegue gestionado de Bedrock.</li>'
            '<li><b>Custom Model Import on-demand:</b> on-demand es para cargas impredecibles y por uso; no garantiza latencia consistente bajo alta concurrencia como el provisioned throughput.</li>'
            '<li><b>SageMaker Serverless Inference:</b> escala por uso para trafico esporadico, pero no asegura latencia baja predecible para inferencia concurrente y sostenida.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Modelo propio en Bedrock con carga predecible y latencia consistente: Custom Model Import con capacidad reservada de inferencia. On-demand y serverless sirven para cargas impredecibles, sin garantia de latencia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html">docs.aws Bedrock Custom Model Import</a></div>'
        ),
    ),
    # ============================================================
    # Q72 - Bedrock Knowledge Bases data source connectors + sync
    # ============================================================
    card(
        question="Un organismo debe integrar varias fuentes (guias regulatorias internas, resumenes historicos y wikis de compliance que cambian seguido) para un asistente de IA, con una <b>capa de acceso consistente</b>, <b>minimo mantenimiento manual</b> y que el asistente referencie siempre la informacion mas actual. &iquest;Que se debe implementar?",
        options=[
            "AWS DataSync para transferir los documentos a un S3 central y Amazon EMR para reestructurar, con jobs cron que re-procesan en intervalos",
            "Unificar el acceso con Amazon Bedrock Knowledge Bases, configurar data source connectors para cada base y wiki, y habilitar la sincronizacion automatica",
            "Amazon AppFlow para las fuentes SaaS y AWS Transfer Family para archivo, hacia Amazon OpenSearch y refrescos con AWS Step Functions",
            "Amazon Neptune como grafo central de conocimiento, con scripts de ingesta que convierten todo a grafo y actualizaciones por lote programadas",
        ],
        correct=1,
        key="aip02-q72",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Knowledge Bases con data source connectors y sincronizacion automatica.</div>'
            '<p><b>El problema:</b> capa de acceso unica y lista para IA sobre fuentes que cambian seguido, con minimo mantenimiento y contenido siempre actual.</p>'
            '<p><b>Por que la respuesta sirve:</b> las <b>Bedrock Knowledge Bases</b> unifican el acceso para RAG; los <b>data source connectors</b> conectan cada repositorio/wiki y la <b>sincronizacion automatica</b> mantiene el contenido al dia sin trabajo manual. Es la capa gestionada y AI-ready pedida.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DataSync + EMR + cron:</b> depende de transferencias por lote y scheduling manual; sube el overhead y no ofrece una capa unificada AI-ready con sincronizacion automatica.</li>'
            '<li><b>AppFlow + Transfer Family + OpenSearch + Step Functions:</b> requiere varios servicios con orquestacion propia (mas complejidad y mantenimiento) y carece de una KB AI-ready nativa.</li>'
            '<li><b>Neptune como grafo:</b> exige modelado e ingesta a medida, actualizaciones por lote y no esta optimizado para RAG ni sincronizacion automatica entre fuentes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Consolidar multiples fuentes para un asistente con minimo mantenimiento y contenido fresco: el servicio gestionado de bases de conocimiento con conectores de fuente y sincronizacion automatica. Cron/EMR o varios servicios cosidos a mano suman overhead.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds.html">docs.aws Bedrock KB data sources</a></div>'
        ),
    ),
    # ============================================================
    # Q73 - Text-to-SQL + Custom Model Import + Guardrails + confidence/semantic
    # ============================================================
    card(
        question="Un sistema de recomendacion de upgrades usa un modelo importado a Bedrock via Custom Model Import y debe consultar historial de pasajeros en <b>Amazon RDS</b>, dar recomendaciones consistentes y seguras y <b>reducir alucinaciones</b>. &iquest;Que enfoque cumple?",
        options=[
            "Cachear registros en DynamoDB, una Lambda que los transforme en prompts, Bedrock Guardrails para filtrar salidas y Step Functions para orquestar",
            "Text-to-SQL validado sobre RDS, modelo via Custom Model Import, Bedrock Guardrails y un workflow post-inferencia en Step Functions + Lambda",
            "Ingerir el historial de RDS a un data lake S3 con Glue ETL, features con Athena, Guardrails para filtrar y Step Functions",
            "Text-to-SQL validado sobre RDS, modelo via Bedrock Custom Model Import, Guardrails y confidence scoring + similitud semantica para alucinaciones",
        ],
        correct=3,
        key="aip02-q73",
        answer=(
            '<div class="verdict">Correcta: {{L}} - text-to-SQL validado + Custom Model Import + Guardrails + confidence/semantic scoring.</div>'
            '<p><b>El problema:</b> consultar RDS con precision, servir el modelo propio de forma segura y reducir alucinaciones con un mecanismo adecuado.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>text-to-SQL con validaciones</b> extrae con exactitud los registros de RDS (base relacional); el modelo se sirve via <b>Custom Model Import</b>; <b>Guardrails</b> impone seguridad de contenido; y el <b>confidence scoring + similitud semantica</b> mide la relevancia factual de la salida, que es el mecanismo apropiado para reducir alucinaciones.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DynamoDB + Lambda a prompts:</b> DynamoDB es NoSQL, no soporta el SQL estructurado para consultar RDS con precision; transformar a prompts a mano introduce inconsistencia y Step Functions no suprime alucinaciones por si mismo.</li>'
            '<li><b>text-to-SQL + Step Functions/Lambda para suprimir alucinaciones:</b> los componentes de datos son correctos, pero Step Functions y Lambda son orquestacion/logica, no un mecanismo nativo para evaluar la relevancia semantica o la confianza factual de la salida.</li>'
            '<li><b>Glue ETL + Athena:</b> mover a un data lake y materializar features con Athena es innecesario cuando los datos ya estan en RDS y consultables por text-to-SQL; y no aporta un mecanismo de reduccion de alucinaciones.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Reducir alucinaciones = medir relevancia/confianza (confidence scoring + similitud semantica), no orquestacion (Step Functions/Lambda). Consultar RDS con precision = text-to-SQL validado, no DynamoDB.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html">docs.aws Bedrock Custom Model Import</a></div>'
        ),
    ),
    # ============================================================
    # Q75 - Transcribe streaming + InvokeModelWithResponseStream + WebSocket
    # ============================================================
    card(
        question="Un asistente en tiempo real para call center debe transcribir voz en vivo y empezar a analizar el <b>contexto parcial antes de que el cliente termine de hablar</b>, minimizando la latencia hasta la primera sugerencia, con servicios gestionados y <b>streaming bidireccional</b> continuo. &iquest;Que solucion cumple?",
        options=[
            "Amazon Transcribe que espera cada segmento final antes de Bedrock con InvokeModel, con respuesta completa via un REST API de API Gateway",
            "Partial-result streaming de Amazon Transcribe con fragmentos a Bedrock via InvokeModelWithResponseStream y salida en streaming a los agentes por un WebSocket API",
            "Amazon Transcribe con partial results a Kinesis Data Streams, Lambda que agrupa fragmentos e invoca a Bedrock, y respuesta via WebSocket API",
            "Transcribe streaming con partial results a Bedrock via InvokeModelWithResponseStream, pero bufferizando los chunks en Lambda y enviando la respuesta completa via WebSocket",
        ],
        correct=1,
        key="aip02-q75",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Transcribe partial-result streaming + InvokeModelWithResponseStream + WebSocket API.</div>'
            '<p><b>El problema:</b> minimizar la latencia hasta la primera sugerencia, procesando el habla parcial y transmitiendo respuestas de forma bidireccional y continua.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>partial-result streaming</b> de Transcribe entrega segmentos interinos mientras el cliente sigue hablando; <b>InvokeModelWithResponseStream</b> expone los chunks del FM a medida que se generan; y un <b>WebSocket API</b> empuja esos updates a los agentes en tiempo real. Todo gestionado y de minima latencia.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Esperar segmento final + InvokeModel + REST:</b> esperar la finalizacion y usar InvokeModel (respuesta completa) mas un patron REST request-response elimina el streaming e introduce demora en cada etapa.</li>'
            '<li><b>Kinesis + Lambda que agrupa:</b> acumular fragmentos antes de invocar Bedrock retrasa el inicio de la inferencia, contra el objetivo de minima latencia a la primera sugerencia.</li>'
            '<li><b>Bufferizar chunks en Lambda:</b> guardar toda la salida antes de enviarla anula la ventaja del response streaming; los chunks deben fluir en cuanto se generan.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Sugerencias en vivo con minima latencia: Transcribe partial results + InvokeModelWithResponseStream + WebSocket API. Esperar segmentos finales, agrupar fragmentos o bufferizar la salida rompe el streaming.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html">docs.aws Transcribe streaming</a></div>'
        ),
    ),
    # ============================================================
    # Q63 - Step Functions human-in-the-loop waitForTaskToken
    # ============================================================
    card(
        question="Una agencia genera con Amazon Bedrock recomendaciones de alerta (IA) desde telemetria por Amazon Kinesis Data Streams. Por regulacion, <b>cada recomendacion debe ser aprobada por un oficial antes de emitir la alerta</b> y hay que <b>registrar cada decision de revision</b> para auditoria. &iquest;Que enfoque cumple?",
        options=[
            "Step Functions con revision humana via waitForTaskToken; la decision hace que una Lambda llame a SendTaskSuccess y guarde en DynamoDB",
            "Step Functions con callback que emite un task token; una Lambda llama a SendTaskSuccess y guarda en DynamoDB, sin definir su disparador",
            "Cada recomendacion de Kinesis a un topic de Amazon MSK Kafka; una Lambda la reenvia al oficial por Amazon SNS, aprobaciones en Aurora",
            "Una API GraphQL de AWS AppSync empuja las recomendaciones a un dashboard; una Lambda suscrita captura la aprobacion y guarda en Amazon S3",
        ],
        correct=0,
        key="aip02-q63",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Step Functions con <code>waitForTaskToken</code> + <code>SendTaskSuccess</code> + DynamoDB.</div>'
            '<p><b>El problema:</b> ninguna alerta puede salir al publico sin la aprobacion formal de un oficial (una <b>compuerta humana obligatoria</b>, human-in-the-loop), y cada decision debe quedar registrada de forma consultable para auditoria post-incidente.</p>'
            '<p><b>Por que la respuesta sirve:</b> el patron <b><code>waitForTaskToken</code></b> de Step Functions <b>pausa</b> la ejecucion del flujo en el estado de revision y genera un <b>task token</b>; el flujo no avanza hasta que llega la decision. Cuando el oficial responde, una Lambda invoca <b><code>SendTaskSuccess</code></b> con ese token y el resultado, lo que <b>reanuda</b> el flujo de forma controlada. Aqui el disparador esta explicito (la accion del oficial invoca la Lambda), asi que la transicion aprobacion -> reanudacion es fiable. Guardar cada decision en <b>Amazon DynamoDB</b> da un registro estructurado y de baja latencia, apto para auditoria.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Step Functions callback con token pero sin disparador definido:</b> usa los mecanismos correctos (SendTaskSuccess, DynamoDB), pero <b>no define que hace fire a la Lambda</b> tras la decision del oficial; el handoff entre la aprobacion y la reanudacion queda ambiguo, y una compuerta obligatoria no puede depender de un paso no definido.</li>'
            '<li><b>MSK + SNS + Aurora:</b> MSK (streaming Kafka gestionado) y SNS (pub/sub de notificaciones) pueden entregar la recomendacion al oficial, pero <b>no ofrecen un mecanismo nativo para pausar el flujo</b> y esperar una aprobacion formal; no hay estado de aprobacion estructurado ni callback por token que garantice capturar la decision antes de continuar.</li>'
            '<li><b>AppSync GraphQL + S3:</b> AppSync sirve para sincronizacion en tiempo real y dashboards, pero <b>no pausa el flujo</b> ni impone una compuerta de aprobacion obligatoria; ademas registrar en S3 por eventos no da la consulta estructurada y de baja latencia que exige una auditoria de cumplimiento (a diferencia de DynamoDB).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Aprobacion humana obligatoria que debe <b>pausar</b> un flujo hasta la respuesta de una persona: orquesta con Step Functions y su patron de callback por task token. Un pub/sub o un dashboard en tiempo real notifican, pero no bloquean el flujo hasta la decision.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html">docs.aws Step Functions waitForTaskToken</a></div>'
        ),
    ),
    # ============================================================
    # Q69 - CDK + CodePipeline multi-stage con FoundationModel
    # ============================================================
    card(
        question="Una empresa despliega un moderador de contenido con IA generativa que evalua texto con <b>varios FM de Amazon Bedrock</b> para comparar calidad y latencia. Debe desplegarse en <b>staging y produccion</b> de forma <b>automatizada y consistente</b> y permitir que los product managers <b>cambien de modelo sin tocar el codigo</b>. &iquest;Que arquitectura conviene?",
        options=[
            "Una app de AWS CDK con FoundationModel.fromFoundationModelId() y un CodePipeline multi-etapa (staging y produccion) con CodeBuild y cambio de FM controlado",
            "Una app de AWS CDK con varios CodePipeline, uno por FM, invocando los modelos con ProvisionedModel.fromProvisionedModelArn() para la evaluacion multi-modelo",
            "Apps de AWS CDK separadas para staging y produccion, con CodeBuild y FMs por configuracion estatica en objetos de Amazon S3",
            "Una app de AWS CDK solo para produccion con CodePipeline y CodeBuild; staging manual y el FM por variables de entorno",
        ],
        correct=0,
        key="aip02-q69",
        answer=(
            '<div class="verdict">Correcta: {{L}} - una app CDK unica + un CodePipeline multi-etapa con <code>FoundationModel.fromFoundationModelId()</code>.</div>'
            '<p><b>El problema:</b> desplegar el mismo sistema en staging y produccion de forma automatizada y <b>consistente</b> (sin drift), soportar evaluacion multi-modelo y permitir que un product manager <b>cambie de FM sin modificar codigo</b>.</p>'
            '<p><b>Por que la respuesta sirve:</b> una <b>sola app de CDK</b> (infraestructura como codigo) define la infra una vez y la reutiliza, evitando duplicacion y divergencia entre entornos. Un <b>unico pipeline de CodePipeline con varias etapas</b> (staging luego produccion) da un despliegue automatizado y consistente en ambos entornos. <b><code>FoundationModel.fromFoundationModelId()</code></b> referencia un FM por su id de forma flexible, lo que habilita el <b>cambio controlado de modelo</b> por configuracion sin tocar el codigo de la aplicacion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Varios pipelines + <code>ProvisionedModel.fromProvisionedModelArn()</code>:</b> multiplicar pipelines <b>duplica</b> la logica de despliegue y aumenta la carga operativa en vez de consolidar los entornos; ademas <code>fromProvisionedModelArn()</code> es para throughput aprovisionado y no soporta bien la evaluacion flexible entre varios modelos.</li>'
            '<li><b>Apps CDK separadas + config estatica en S3:</b> mantener apps separadas <b>fragmenta</b> la infra y reduce la consistencia entre entornos; la configuracion estatica en S3 no ofrece un mecanismo centralizado ni controlado para cambiar de modelo.</li>'
            '<li><b>App CDK solo para produccion + staging manual:</b> configurar staging a mano <b>rompe la consistencia y la automatizacion</b>, introduce configuration drift entre entornos y no da un mecanismo fiable de despliegue estandarizado ni de cambio controlado de modelo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Multi-entorno consistente y automatizado con cambio de modelo por configuracion: una sola app de IaC (CDK) + un pipeline con multiples etapas. Duplicar pipelines o apps, o configurar entornos a mano, genera drift y carga operativa.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrock.FoundationModel.html">docs.aws CDK Bedrock FoundationModel</a></div>'
        ),
    ),
    # ============================================================
    # RESCATADAS (auditoria falsos-COVERED). Prefijo aip02r-.
    # Nivel PROFESIONAL: enfatizan el detalle avanzado/feature especifica.
    # ============================================================
    # Q6r - ECS Fargate para WebSocket persistente (serverless, sin gestion de servidores)
    card(
        question="Un agente de Amazon Bedrock necesita una <b>herramienta de telemetria propia que mantenga una conexion WebSocket de larga vida</b> para eventos GPS continuos. Las opciones serverless fallaron por <b>timeouts de ejecucion</b>. Se busca un despliegue con sesiones de red persistentes <b>sin gestionar servidores</b>. &iquest;Que solucion cumple?",
        options=[
            "Desplegar la herramienta en Amazon ECS con el tipo de lanzamiento AWS Fargate, que soporta WebSocket de larga vida sin administrar servidores",
            "Desplegar la herramienta en Amazon EC2 con un script propio que mantenga la sesion WebSocket y escale las instancias por carga",
            "Ejecutar la herramienta en AWS Lambda y refrescar la sesion WebSocket con invocaciones programadas para simular una conexion continua",
            "Desplegar la herramienta como servicio contenedorizado en Amazon App Runner con autoescalado para las conexiones WebSocket y la carga variable",
        ],
        correct=0,
        key="aip02r-q6",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon ECS con el tipo de lanzamiento AWS Fargate.</div>'
            '<p><b>El problema:</b> mantener una conexion WebSocket <b>persistente y con estado</b> (stateful) para streaming continuo, pero <b>sin administrar servidores</b>. Las opciones serverless de funciones cortan la sesion por el limite de tiempo de ejecucion.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el matiz que decide la pregunta es que <b>Fargate es el modo serverless de ECS</b>: ejecuta contenedores <b>sin que tu aprovisiones, parchees ni escales servidores</b>, y a la vez permite <b>tareas de larga vida</b> que sostienen la conexion WebSocket. Reune las dos exigencias en tension: proceso persistente Y cero gestion de servidores. ECS por si solo (sobre EC2) daria control total del host pero te devuelve la gestion de servidores; la clave examinable es elegir el <b>launch type Fargate</b>.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EC2 con script propio:</b> soporta conexiones largas, pero exige aprovisionar, parchear, escalar y monitorear el host tu mismo; contradice el requisito de no gestionar servidores.</li>'
            '<li><b>Lambda + invocaciones programadas:</b> Lambda esta hecho para cargas cortas y dirigidas por eventos; sus limites de tiempo hacen inviable una conexion WebSocket de larga vida, y refrescarla por schedule provoca desconexiones intermitentes.</li>'
            '<li><b>App Runner:</b> esta optimizado para trafico HTTP sin estado y autoescalado web; las sesiones WebSocket persistentes y con estado pueden volverse inestables o desconectarse.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Proceso de larga vida y con estado que ademas debe ser serverless: elige contenedores gestionados con el modo sin servidores subyacente. Las funciones por evento tienen limite de ejecucion; el modo de instancias te devuelve la administracion del host.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html">docs.aws ECS on AWS Fargate</a></div>'
        ),
    ),
    # Q12r - Exponential backoff con jitter (SDK) + throttling por cliente (API Gateway)
    card(
        question="API Gateway dispara Lambda, que llama a la API de Amazon Bedrock. En pruebas de carga aparecen latencia y errores <b>ThrottlingException</b> en Bedrock durante los picos de concurrencia. Hay que manejar el pico y <b>reducir la frecuencia de ThrottlingException</b> sin perder velocidad. &iquest;Que implementar?",
        options=[
            "Exponential backoff con jitter en el AWS SDK para los reintentos, mas throttling por cliente en API Gateway en los picos",
            "Habilitar AWS Global Accelerator para optimizar el enrutamiento y reducir la latencia acortando los saltos de red en la alta demanda",
            "Usar AWS Step Functions para el flujo de solicitudes con reintento de intervalo fijo que mantenga la capacidad de respuesta bajo carga",
            "Implementar reintento exponencial en el AWS SDK, con esperas crecientes constantes entre reintentos para el throttling en el pico",
        ],
        correct=0,
        key="aip02r-q12",
        answer=(
            '<div class="verdict">Correcta: {{L}} - exponential backoff con jitter en el SDK + throttling por cliente en API Gateway.</div>'
            '<p><b>El problema:</b> Bedrock lanza ThrottlingException por volumen de solicitudes en concurrencia alta; hay que atacar el problema por <b>dos frentes a la vez</b>.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el detalle que decide es la <b>combinacion de dos mecanismos</b>, no uno solo. En el <b>lado del cliente</b>, el <b>exponential backoff con jitter</b> del SDK reintenta con esperas crecientes <b>mas una componente aleatoria (jitter)</b>: el jitter <b>desincroniza</b> los reintentos de muchos clientes y evita las tormentas de reintentos. En el <b>lado de la entrada</b>, los <b>limites de throttling por cliente</b> en API Gateway recortan la tasa antes de que golpee a Bedrock. Backoff+jitter absorbe los throttles que ocurren; el rate limiting por cliente reduce que ocurran.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Global Accelerator:</b> mejora el pathing y la latencia de red al edge, no los limites de tasa del servicio; un enrutamiento mas rapido puede incluso aumentar la tasa de llamadas entrantes y empeorar el throttling.</li>'
            '<li><b>Step Functions con reintento de intervalo fijo:</b> los reintentos a intervalo fijo se sincronizan y provocan tormentas de reintentos, y agregan latencia de orquestacion inadecuada para trafico sincrono de API.</li>'
            '<li><b>Reintento exponencial SIN jitter:</b> al no tener jitter, varios clientes reintentan en los mismos instantes; esa sincronizacion crea tormentas de reintentos y amplifica el throttling en vez de reducirlo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Ante throttling de un servicio con alta concurrencia: combina reintentos con backoff <b>y jitter</b> en el cliente (el jitter es lo que evita el retry storm) con limitacion de tasa en la puerta de entrada. Backoff sin jitter no basta.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html">docs.aws Retry with backoff and jitter</a></div>'
        ),
    ),
    # Q25r - Glue Data Quality + chunking (angulo avanzado B)
    card(
        question="Una firma legal prepara datos no estructurados en Amazon S3 para una app de Amazon Bedrock. Antes del FM debe: <b>descubrir y catalogar</b> las fuentes, aplicar <b>transformaciones y chunking a medida</b> y <b>validar con seguimiento continuo de metricas de calidad</b>, minimizando desarrollo. &iquest;Que solucion cumple?",
        options=[
            "Crawler de AWS Glue que descubre y cataloga, jobs de Glue ETL para transformaciones y chunking, y AWS Glue Data Quality de metricas",
            "Lambdas por subida a S3 que parsean, generan metadata y hacen chunking, con resultados en DynamoDB, metricas en CloudWatch y salida a Bedrock",
            "Amazon EMR Serverless con Spark que descubre y transforma, con validacion y chunking en Spark, metadata en S3 y la salida a Bedrock",
            "Amazon Athena que consulta S3 con metadata en el Glue Data Catalog, y Lambdas que validan, chunkean y reescriben a S3 para Bedrock",
        ],
        correct=0,
        key="aip02r-q25",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Glue crawler + Data Catalog + Glue ETL + <b>Glue Data Quality</b>.</div>'
            '<p><b>El problema:</b> no basta con catalogar y transformar; el requisito diferenciador es <b>validar los datasets y seguir metricas de calidad de forma continua</b>, con minimo desarrollo.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el discriminador es <b>AWS Glue Data Quality</b>, la pieza que muchas veces se pasa por alto. Glue no es solo ETL + Data Catalog: <b>Glue Data Quality</b> evalua reglas sobre los datos procesados y <b>trackea metricas de calidad</b> de forma gestionada, detectando problemas antes de que lleguen al FM. Sumado al <b>crawler</b> (descubre y cataloga), los <b>jobs ETL</b> (transformacion y logica de chunking) y el <b>Data Catalog</b> (metadata auditable), se cubre todo el flujo <b>sin construir un framework de calidad propio</b>. Ese componente de calidad gestionado es lo que la pregunta evalua, no la definicion generica de Glue como ETL.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda + DynamoDB + CloudWatch:</b> obliga a construir y mantener tu propia extraccion de metadata, chunking, validacion y monitoreo de calidad, dispersos en tres servicios en vez del flujo integrado de Glue.</li>'
            '<li><b>EMR Serverless + Spark:</b> escala transformaciones, pero tu debes implementar el framework de metadata y de calidad en Spark; no trae crawler, Data Catalog ni Data Quality integrados, asi que no minimiza el desarrollo.</li>'
            '<li><b>Athena + Lambda programadas:</b> Athena solo consulta; sigues necesitando codigo Lambda propio para validacion y chunking, aumentando el mantenimiento frente a Glue ETL + Glue Data Quality.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cuando el enunciado exige <b>validar y trackear metricas de calidad</b> de datos con minimo desarrollo, busca el modulo de calidad gestionado del mismo ecosistema de datos, no un pipeline de funciones y bases propias. Descubrir con crawler, catalogar en el catalogo, transformar y chunkear con los jobs, validar con el modulo de calidad.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html">docs.aws AWS Glue Data Quality</a></div>'
        ),
    ),
    # Q34r - Step Functions Standard como orquestador con handler de evento S3 (angulo avanzado B)
    card(
        question="Una fintech tiene un modelo de Amazon SageMaker AI en tiempo real; sus datos de entrenamiento en Amazon S3 crecen de continuo. Quiere <b>eliminar el reentrenamiento manual</b> con un pipeline que reentrene y <b>redepliegue</b> al subir un dataset a S3, con orquestacion <b>durable</b> (reintentos, log, auditoria). &iquest;Que solucion cumple?",
        options=[
            "Un flujo AWS Step Functions Standard cuyo primer estado es una Lambda handler del evento S3 y el siguiente ejecuta SageMaker AI Pipelines",
            "Una regla de Amazon EventBridge que monitorea el bucket y enruta directo a SageMaker AI Pipelines, que reentrena y actualiza el endpoint",
            "AWS Glue que cataloga cada dataset, Glue DataBrew que normaliza y una llamada al endpoint de SageMaker AI para predecir sin reentrenar",
            "Un flujo AWS Step Functions Express con integraciones del SDK que trae S3, exporta con SageMaker AI Data Wrangler a Autopilot y redespliega",
        ],
        correct=0,
        key="aip02r-q34",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS Step Functions <b>Standard</b> como orquestador con handler de evento S3.</div>'
            '<p><b>El problema:</b> automatizar reentrenamiento y redeploy ante subidas a S3, pero con una <b>orquestacion durable</b> que garantice reintentos, historial de ejecucion y auditoria de un job de ML potencialmente largo.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el discriminador es elegir <b>Step Functions Standard como la columna de orquestacion</b>. Standard (a diferencia de Express) tiene <b>estado durable e historial de ejecucion completo</b>, ideal para flujos de larga duracion y auditables; su primer estado usa una <b>Lambda como handler del evento de subida a S3</b> y el siguiente estado ejecuta el pipeline de SageMaker para reentrenar y redesplegar. Ese backbone durable es lo que garantiza que un reentrenamiento fallido se reintente, se registre y se escale. Saber cual FEATURE (Standard vs Express) y el patron de handler de evento es justo lo que la pregunta evalua.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EventBridge directo a SageMaker Pipelines:</b> se salta la capa de orquestacion durable; SageMaker Pipelines no es un target nativo directo de EventBridge del mismo modo que Lambda o Step Functions, y sin ese backbone no hay garantia de reintento, log ni escalado del fallo.</li>'
            '<li><b>Glue + DataBrew + llamar al endpoint:</b> llamar al endpoint solo hace inferencia; no actualiza los pesos del modelo ni redepliega. El escenario exige reentrenar y redesplegar el artefacto.</li>'
            '<li><b>Step Functions Express + Autopilot:</b> los flujos Express carecen del estado durable y del historial para jobs de ML largos; el entrenamiento sobre un dataset creciente puede exceder sus limites de tiempo y no conserva historial para auditoria.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Orquestacion de ML de larga duracion con reintentos, auditoria e historial completo: elige el tipo de flujo durable, no el efimero (el efimero pierde historial y tiene limite de tiempo). Un evento de S3 se conecta al flujo mediante un handler, no siempre por integracion directa del servicio final.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/concepts-standard-vs-express.html">docs.aws Step Functions Standard vs Express</a></div>'
        ),
    ),
    # Q38r - Estrategia de despliegue A/B testing + model evaluation (angulo avanzado AB)
    card(
        question="Un asistente de IA generativa da recomendaciones en tiempo real (usa Amazon Comprehend para sentimiento/entidades y SageMaker AI para engagement). Antes del despliegue total, el equipo quiere una <b>evaluacion comparando varias versiones de modelo a la vez</b>, con metricas para decidir con datos. &iquest;Que estrategia de despliegue conviene?",
        options=[
            "Usar A/B testing que enruta segmentos a varias versiones a la vez, con metricas de Comprehend y SageMaker AI para elegir el mejor",
            "Desplegar con Blue/Green el nuevo modelo en paralelo, con metricas de Comprehend y SageMaker AI y cambio de todo el trafico tras verificar",
            "Implementar un Canary a un subconjunto, con sentimiento y engagement via Comprehend y SageMaker AI, subiendo el trafico gradualmente",
            "Un despliegue Linear que desplaza el trafico en incrementos fijos, monitoreando engagement con Comprehend y SageMaker AI en cada incremento",
        ],
        correct=0,
        key="aip02r-q38",
        answer=(
            '<div class="verdict">Correcta: {{L}} - estrategia de despliegue A/B testing para evaluar varias versiones a la vez.</div>'
            '<p><b>El problema:</b> la clave no son los servicios de sentimiento (Comprehend, SageMaker aparecen en todas las opciones); es la <b>estrategia de despliegue</b> que permita <b>comparar varias versiones de modelo simultaneamente</b> para una eleccion basada en datos.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el detalle examinable es distinguir estrategias de despliegue. <b>A/B testing</b> es la unica que enruta <b>segmentos distintos de usuarios a multiples versiones al mismo tiempo</b>, de modo que se recolectan metricas comparables en paralelo y se elige el mejor modelo objetivamente. Es evaluacion comparativa de modelos, no solo un rollout seguro. Ese matiz (comparacion simultanea vs rollout secuencial) es lo que la pregunta evalua.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Blue/Green:</b> asegura un cambio suave con minima interrupcion, pero evalua <b>un solo modelo en produccion a la vez</b>; no permite la comparacion simultanea de varias versiones.</li>'
            '<li><b>Canary:</b> libera una version a un subconjunto y sube trafico gradualmente para detectar problemas temprano, pero tambien evalua <b>una version a la vez</b>; no sirve para comparacion sistematica entre modelos.</li>'
            '<li><b>Linear:</b> desplaza el trafico en incrementos fijos; se centra en un rollout controlado y en mitigar riesgo, no en la evaluacion paralela de varias versiones.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Comparar varias versiones de modelo AL MISMO TIEMPO para decidir con metricas = A/B testing. Blue/Green, Canary y Linear son patrones de rollout seguro y evaluan una version por vez, no una comparacion simultanea.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-ab-testing.html">docs.aws A/B testing de modelos</a></div>'
        ),
    ),
    # Q48r - CloudWatch composite alarms + anomaly detection (angulo avanzado A)
    card(
        question="Una empresa usa un FM para descripciones de catalogo. DevOps monitorea con Amazon CloudWatch metricas tecnicas (tokens, latencia, fallos); ventas mide metricas comerciales (CTR, ingresos) en sistemas externos. Se requiere observabilidad <b>unificada que correlacione desempeno y negocio</b> y que <b>alerte ante degradacion anomala</b>. &iquest;Que solucion cumple?",
        options=[
            "Dashboards de CloudWatch con los datos operativos y comerciales, composite alarms con anomaly detection sobre lo correlacionado y Amazon SNS para alertar",
            "Trazas de AWS X-Ray para latencia y errores, ventas en Amazon DynamoDB y una regla de EventBridge hacia una maquina de Step Functions",
            "Desplegar Amazon Managed Grafana con CloudWatch y metricas externas, y alertas de Grafana que disparen Lambdas de remediacion por umbrales estaticos",
            "Metricas y ventas a CloudWatch Logs, un modelo propio en SageMaker AI para anomalias y un endpoint que dispara notificaciones de Amazon SNS",
        ],
        correct=0,
        key="aip02r-q48",
        answer=(
            '<div class="verdict">Correcta: {{L}} - dashboards de CloudWatch + <b>composite alarms con anomaly detection</b> + SNS.</div>'
            '<p><b>El problema:</b> correlacionar metricas heterogeneas (tecnicas y comerciales) en una vista unica y alertar de forma automatica ante <b>degradacion anomala</b>, no ante un umbral fijo.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el discriminador es usar <b>composite alarms</b> (que combinan varias alarmas para razonar sobre datos correlacionados de distintos dominios) <b>potenciadas con anomaly detection</b>, que aprende una <b>linea base a partir de patrones historicos</b> en vez de depender de umbrales estaticos. CloudWatch agrega ambos conjuntos de metricas en dashboards y SNS <b>notifica al personal</b> (no remedia solo). Ese detalle de alarma compuesta + deteccion de anomalias es exactamente lo que separa la respuesta de un CloudWatch generico con umbral fijo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>X-Ray + DynamoDB + Step Functions:</b> X-Ray es para trazado distribuido de solicitudes individuales, no para agregar metricas de negocio y operacion; DynamoDB y Step Functions no aportan deteccion de anomalias sobre metricas.</li>'
            '<li><b>Managed Grafana con remediacion Lambda:</b> visualiza ambos datasets, pero el requisito es <b>alertar a las personas</b>, no ejecutar remediacion autonoma; ademas usa umbrales estaticos, que no se adaptan a la linea base historica.</li>'
            '<li><b>CloudWatch Logs + modelo propio en SageMaker:</b> convertir metricas numericas en logs y entrenar un modelo de anomalias a medida agrega un overhead enorme e innecesario; CloudWatch ya ofrece anomaly detection nativo sobre metricas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Alertar por <b>degradacion anomala</b> segun patrones historicos, no por umbral fijo, correlacionando varios dominios: composite alarms + anomaly detection nativos de CloudWatch, con SNS para notificar (notificar &ne; remediar).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html">docs.aws CloudWatch composite alarms</a></div>'
        ),
    ),
    # Q56r - CloudWatch Application Insights (autodescubrimiento + anomaly detection ML + EMF)
    card(
        question="Un motor de recomendaciones en Amazon EC2 monta un EBS con cache de vectores antes de FMs de Amazon Bedrock. La calidad se degrada y no se sabe si es <b>I/O de EBS</b> o <b>deriva del FM</b>. Se necesita observabilidad que <b>autodescubra EC2 y EBS como un stack</b>, detecte desviaciones por <b>patrones historicos</b> y minimice la configuracion. &iquest;Que solucion cumple?",
        options=[
            "Amazon CloudWatch Application Insights sobre el resource group de EC2 y EBS, con embedded metric format y anomaly detection con ML",
            "Amazon CloudWatch Container Insights en las EC2 para CPU, memoria e I/O, con alarmas de umbral estatico sobre la lectura de EBS",
            "AWS X-Ray en los procesos EC2, segmentos a Amazon Data Firehose y QuickSight, con alertas a mano para EBS y el FM",
            "Un cluster de Amazon OpenSearch Service con el plugin de Observability, metricas de EC2/EBS y logs de Bedrock via Firehose, con detectores propios",
        ],
        correct=0,
        key="aip02r-q56",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon CloudWatch <b>Application Insights</b> sobre el resource group.</div>'
            '<p><b>El problema:</b> descubrir y monitorear <b>EC2 + EBS como un solo stack</b> de forma automatica, detectar anomalias por patrones historicos y correlacionar alertas rapido, con minima configuracion manual.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el servicio/feature exacto es <b>CloudWatch Application Insights</b>, que muchas cartas no cubren. A diferencia de un CloudWatch generico, Application Insights <b>autodescubre el stack de la aplicacion</b> a partir de un resource group (EC2 y sus EBS), aplica <b>anomaly detection con ML</b> para fijar lineas base sin umbrales estaticos, y genera <b>alertas correlacionadas entre capas</b>. Ademas el <b>embedded metric format (EMF)</b> permite emitir metricas de calidad personalizadas con dimensiones (segmento, model ID) para incluir la capa del FM. Reconocer este servicio y sus tres rasgos (autodescubrimiento, anomaly detection ML, EMF) es lo que la pregunta evalua; el escenario EC2/EBS es solo el vestido.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Container Insights + umbrales estaticos:</b> esta pensado para cargas en contenedores (ECS/EKS/Kubernetes), no para stacks EC2/EBS standalone; no monitorea EBS a fondo ni ofrece anomaly detection ML cross-layer, y usa umbrales estaticos.</li>'
            '<li><b>X-Ray + Firehose + QuickSight:</b> X-Ray no hace anomaly detection con ML y el pipeline a QuickSight impone mucho trabajo manual; no correlaciona automaticamente I/O de EBS con deriva del FM ni garantiza alertas en 10 minutos por linea base dinamica.</li>'
            '<li><b>OpenSearch con plugin de Observability:</b> introduce overhead operativo alto (provisionar cluster, gestionar indices, escribir detectores y reglas a mano), lo contrario a minimizar la configuracion manual.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Autodescubrir un stack (EC2+EBS), anomaly detection con ML por linea base historica y alertas correlacionadas con minima configuracion apuntan al modulo de insights de aplicacion de CloudWatch; el modulo para contenedores no cubre EC2/EBS standalone y depende de umbrales estaticos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html">docs.aws CloudWatch Application Insights</a></div>'
        ),
    ),
    # Q65r - Amazon Kendra indexing + Query API (angulo avanzado AB)
    card(
        question="Un chatbot usa Amazon Lex (NLU) y Amazon Transcribe (voz a texto). Ahora la empresa quiere <b>automatizar respuestas recuperando</b> de su gran biblioteca de documentacion (manuales, FAQs) de forma rapida y precisa, en tiempo real y <b>con el menor esfuerzo de desarrollo</b> (sin entrenar modelos). &iquest;Que enfoque cumple?",
        options=[
            "Usar Amazon Kendra para indexar los documentos e integrarlo con el chatbot mediante la Kendra Query API para respuestas dinamicas",
            "Almacenar la documentacion en una Amazon Bedrock Knowledge Base y usar Amazon Comprehend para analizar las consultas y extraer los insights relevantes",
            "Entrenar un modelo BiDAF con las preguntas y la documentacion en Amazon SageMaker AI, integrado por la API InvokeEndpoint de SageMaker Runtime",
            "Un modelo BERT en Amazon SageMaker AI, la documentacion en Amazon S3 y Lex que invoque el endpoint de SageMaker",
        ],
        correct=0,
        key="aip02r-q65",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Kendra para indexar + Kendra Query API.</div>'
            '<p><b>El problema:</b> recuperar respuestas precisas desde una biblioteca de documentacion en tiempo real, con <b>minimo desarrollo</b> y sin entrenar modelos. El solape con lo ya estudiado es solo el escenario de chatbot/Lex.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el servicio/feature exacto es <b>Amazon Kendra</b>, un servicio de <b>busqueda inteligente sobre documentos</b> que <b>indexa la documentacion directamente</b> y expone la <b>Kendra Query API</b> para consultas en lenguaje natural. No requiere entrenar ni desplegar modelos: es la ruta de menor esfuerzo para recuperacion documental. Reconocer Kendra + su Query API (frente a soluciones que exigen entrenamiento) es lo que la pregunta evalua.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bedrock Knowledge Base + Comprehend:</b> Comprehend hace analisis de texto (sentimiento, entidades), no recuperacion documental; usarlo para extraer respuestas exige integracion manual y es menos eficiente que el indexado y busqueda nativos de Kendra.</li>'
            '<li><b>Modelo BiDAF en SageMaker:</b> requiere entrenar y desplegar un modelo a medida (preparacion de datos, tuning), justo el esfuerzo que se busca evitar.</li>'
            '<li><b>Modelo BERT + S3 + Lex:</b> tambien implica construir y entrenar un modelo propio; almacenar en S3 e invocar un endpoint agrega complejidad frente al indexado directo y la Query API de Kendra.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Recuperacion de respuestas sobre una biblioteca documental con minimo desarrollo y sin entrenar modelos: servicio de busqueda inteligente que indexa documentos y ofrece una API de consulta. Entrenar BERT/BiDAF es el camino de maximo esfuerzo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html">docs.aws Amazon Kendra</a></div>'
        ),
    ),
    # Q70r - Lake Formation LF-Tag fine-grained access control (angulo avanzado A)
    card(
        question="Una organizacion de salud procesa registros medicos sensibles usando Amazon Rekognition y Amazon Textract, con datos en Amazon S3. Debe: <b>dar acceso solo a subconjuntos autorizados</b>, <b>clasificar datasets con metadata</b> (salud, imagenes, facturacion), <b>control de acceso granular</b> y <b>auditar todos los accesos</b>. &iquest;Que solucion es la mejor?",
        options=[
            "Usar AWS Lake Formation con control de acceso fino basado en LF-Tags para politicas granulares, con gobernanza integral, auditoria y cifrado",
            "Implementar politicas de bucket de Amazon S3 para acceso a nivel de objeto sobre los datos, con AWS KMS para cifrado en reposo",
            "Configurar roles de AWS IAM y VPC endpoints para conectividad privada segura, de modo que solo servicios autorizados interactuen con los datos",
            "Utilizar AWS Secrets Manager para gestionar las API keys y credenciales, con controles de acceso para interacciones seguras con los datos sensibles",
        ],
        correct=0,
        key="aip02r-q70",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS Lake Formation con control de acceso fino basado en <b>LF-Tags</b>.</div>'
            '<p><b>El problema:</b> control de acceso <b>granular por subconjuntos</b> de datos sensibles, clasificacion por metadata y auditoria centralizada; el escenario (S3, Textract, Rekognition) es solo el contexto.</p>'
            '<p><b>Por que la respuesta sirve (angulo avanzado):</b> el servicio/feature exacto es <b>AWS Lake Formation con LF-Tags</b>. Las <b>LF-Tags</b> son etiquetas de recurso que se asignan a bases, tablas y columnas para <b>clasificar datasets</b> (salud, imagenes, facturacion) y conceder acceso <b>fino</b> (hasta nivel de columna) a usuarios y servicios autorizados. Lake Formation centraliza la gobernanza, con <b>auditoria y cifrado integrados</b> para cumplimiento. Reconocer este control basado en etiquetas frente a mecanismos a nivel de objeto o de red es lo que la pregunta evalua.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Politicas de bucket S3 + KMS:</b> controlan a nivel de objeto/bucket, no ofrecen el acceso fino a nivel de tabla/columna ni la gobernanza centralizada a escala que exige el escenario.</li>'
            '<li><b>IAM roles + VPC endpoints:</b> dan seguridad de red y controlan que servicios se conectan, pero no aportan control fino centralizado por dataset ni la auditoria integrada de Lake Formation.</li>'
            '<li><b>Secrets Manager:</b> gestiona credenciales y API keys, no el acceso granular a grandes datasets en un data lake; carece de la gobernanza, permisos por recurso y auditoria requeridos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Acceso fino por subconjuntos de datos, clasificacion por metadata y auditoria centralizada en un data lake apuntan al servicio de gobernanza con control basado en etiquetas de recurso; las politicas de bucket y los controles de red no llegan al nivel de columna ni centralizan la gobernanza.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/lake-formation/latest/dg/tag-based-access-control.html">docs.aws Lake Formation LF-Tag access control</a></div>'
        ),
    ),
]

create(deck_name="AIP-C01::02", cards=cards, out_path="out/AIP-C01_02.apkg", do_import=False)
