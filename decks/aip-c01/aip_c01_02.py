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
        question="Una carga de IA generativa en Amazon Bedrock corre en una cuenta de aplicacion; llamadas de API Gateway a funciones Lambda en subredes privadas. Requisitos: <b>todas las llamadas a Bedrock deben viajar solo por red privada</b> (sin Internet publico) y el data lake gobernado (en otra cuenta) debe imponer <b>control de acceso a nivel de columna</b> consistente entre ambas cuentas. &iquest;Que solucion cumple?",
        options=[
            "Endpoints VPC de interfaz para las APIs de Bedrock + Lambda en subredes privadas + AWS Lake Formation con control basado en LF-tags para permisos cross-account a nivel de tabla y columna",
            "Lambda en subredes privadas con un NAT Gateway hacia Bedrock y el data lake, y permisos del data lake con politicas de bucket y ACLs de Amazon S3",
            "Un gateway VPC endpoint solo para S3, invocando Bedrock por endpoints publicos, y grants a nivel de base de datos en AWS Lake Formation",
            "Endpoints VPC para Bedrock y S3 pero con fallback a endpoints publicos para lecturas cross-Region, y politicas IAM basadas en path para el data lake",
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
        question="Una app de IA generativa (RAG) combina datos de Amazon S3 y de SaaS integrados con Amazon AppFlow. Necesita un <b>registro centralizado</b> de fuentes de datos, <b>etiquetado de metadata</b> para ligar las salidas a sus datasets de origen (linaje), y <b>logging inmutable</b> de todo acceso y actividad para auditoria. &iquest;Que arquitectura conviene?",
        options=[
            "Registrar las fuentes en el AWS Glue Data Catalog y aplicar tags de metadata para atribucion, y habilitar AWS CloudTrail para registrar de forma inmutable la actividad de API y accesos",
            "Integrar Amazon Macie para escanear y clasificar los reportes, y usar AWS CloudTrail para registrar las solicitudes de API y accesos",
            "Crear un registro unificado con el AWS Glue Data Catalog y tags para linaje, y enviar todos los logs de ejecucion y accesos a Amazon CloudWatch Logs",
            "Usar AWS Lake Formation para gestionar el control de acceso fino, y usar Amazon CloudWatch Logs para recolectar logs y monitorear patrones de acceso",
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
        question="Un flujo multi-agente en AWS Step Functions encadena tres agentes de Bedrock; los artefactos ya se guardan en Amazon S3. Falla porque los <b>payloads intermedios superan la cuota de 256 KB</b> de Step Functions. Hay que evitar esas fallas conservando la observabilidad y el patron ReAct, con <b>minimo esfuerzo operativo</b>. &iquest;Que cambio arquitectonico conviene?",
        options=[
            "Guardar en DynamoDB los logs de razonamiento y pasar solo las partition keys; agregar un estado Map que consulte DynamoDB para traer el payload completo antes de cada agente",
            "Que las llamadas a Bedrock ingieran los payloads grandes directamente desde una S3 URI; extraer las ubicaciones de los objetos con ResultSelector y pasar solo esos punteros ligeros con ResultPath",
            "Desplegar un cluster de Amazon ElastiCache for Redis para cachear los logs; escribir los payloads grandes en Redis y pasar solo las cache keys al siguiente agente",
            "Migrar la orquestacion de Step Functions a Amazon MWAA (Airflow) y usar XComs con un backend S3 personalizado para pasar los payloads entre tareas",
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
        question="Un asistente basado en un FM de Amazon Bedrock da respuestas distintas ante prompts con diferencias minimas de redaccion. Con un dataset de variantes cercanas de cada consulta, se quiere un <b>analisis cuantitativo de robustez</b> que mida cuan sensible es el FM a esas pequenas variaciones y la consistencia de sus respuestas. &iquest;Que solucion lo logra?",
        options=[
            "Lanzar un job de model evaluation de Amazon Bedrock con el dataset preparado y habilitar metricas de robustez para analizar las diferencias estadisticas entre prompts similares",
            "Elegir un modelo Anthropic Claude en Bedrock a temperatura 0 y correr un script Lambda que aplique distancia de Levenshtein para medir cuan distintas son las respuestas",
            "Usar Bedrock Pipelines para inferencia por lote sobre los prompts agrupados, guardar las respuestas en S3 y procesarlas con Amazon Comprehend para similitud linguistica",
            "Crear un flujo en AWS Step Functions que invoque el FM repetidamente con prompts de sistema aleatorios y usar logica propia para evaluar la divergencia de salidas",
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
        question="Una plataforma de contenido usa Amazon Bedrock. Antes de procesar o publicar, debe: <b>detectar y eliminar PII</b> del texto, <b>identificar imagenes inapropiadas</b>, y <b>evitar que Bedrock acepte o genere contenido daninno</b>, coordinando todo de forma automatica y con <b>minima infraestructura</b>. &iquest;Que enfoque cumple?",
        options=[
            "Orquestar con AWS Step Functions: Amazon Comprehend para detectar y redactar PII del texto, Amazon Rekognition para moderar imagenes, y Bedrock Guardrails sobre entradas y salidas del modelo",
            "Disparar Lambda al subir contenido a S3: Comprehend para PII y Rekognition para imagenes, e implementar reglas de filtrado propias en Lambda para las entradas y salidas de Bedrock",
            "Usar Amazon EventBridge para enrutar eventos de S3 a Lambdas separadas: una llama a Comprehend, otra a Rekognition y una tercera invoca Bedrock tras completar la moderacion",
            "Desplegar un servicio en Amazon ECS que procese los archivos: Comprehend para PII, Rekognition para imagenes y logica propia para validar antes y despues de invocar Bedrock",
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
        question="Un marketplace de cursos (40M usuarios, 15M cursos, 150M resenas en PostgreSQL) quiere busqueda semantica en lenguaje natural con <b>95% de consultas en menos de 500 ms</b>, indice actualizado cada hora, escalado costo-eficiente y el <b>MENOR esfuerzo de desarrollo</b>. &iquest;Que solucion conviene?",
        options=[
            "Cargar el catalogo en una Amazon Bedrock Knowledge Base con pipeline de ingesta programado; que genere y almacene embeddings en la ingesta y usar la Retrieve API (busqueda vectorial integrada) directamente sobre el lenguaje natural",
            "Conectar el catalogo a un indice de Amazon Kendra, usar su recuperacion NLP para el lenguaje natural, programar jobs de sincronizacion horarios para reflejar cambios y exponer los resultados de busqueda a la aplicacion via un endpoint de Amazon API Gateway",
            "Migrar a Amazon OpenSearch Service, generar embeddings con un FM de Bedrock, convertir la consulta a embeddings y hacer busquedas k-NN contra el indice vectorial",
            "Migrar a Amazon Neptune Analytics, configurar un indice vectorial con embeddings de Bedrock y usar Lambdas para generar embeddings y ejecutar la busqueda de similitud",
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
        question="Una plataforma que procesa contenido financiero altamente confidencial usa un FM. Por mandato regulatorio, las interacciones con el FM deben quedar <b>totalmente aisladas</b>, sin <b>retener prompts ni almacenar salidas</b>, y sin que los datos influyan en el comportamiento futuro del modelo, apoyandose en capacidades gestionadas de AWS (sin sistemas de sanitizacion propios). &iquest;Que solucion es la MEJOR?",
        options=[
            "Emplear las funciones nativas de privacidad de datos de Amazon Bedrock para evitar la retencion de prompts y salidas y asegurar interacciones aisladas del FM",
            "Habilitar logging de eventos de datos de AWS CloudTrail para registrar la actividad de invocacion del FM y capturar metadata operativa de cumplimiento",
            "Usar AWS KMS para cifrar todos los prompts y salidas en Amazon S3, con politicas de ciclo de vida que borren los datos poco despues de procesarlos",
            "Implementar un paso de preprocesamiento en Lambda que enmascare identificadores sensibles antes de enviar al FM, y guardar las salidas enmascaradas para auditoria limitada",
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
        question="Un agente en Amazon Bedrock AgentCore Runtime debe imponer SSO corporativo via un IdP OpenID Connect (OIDC), aceptando <b>tokens entrantes solo cuando el audience del token coincide con el ID de la aplicacion</b>. Ademas se quiere optimizar el parametro <b>maximum tokens</b> para controlar el largo de las respuestas. &iquest;Que configuracion usar?",
        options=[
            "Configurar Amazon Cognito user pools como IdP entrante para AgentCore, mapear el application ID del IdP como audience permitido y fijar el maximum tokens",
            "Usar autenticacion solo IAM para AgentCore Runtime y validar solicitudes con SigV4 sin usar OIDC",
            "Configurar AgentCore Identity como proveedor entrante via OIDC, fijar los audiences permitidos al application ID corporativo y ajustar el parametro maximum tokens",
            "Enlazar AgentCore Identity al IdP solo para autenticacion saliente, de modo que el agente pida tokens al IdP pero no imponga validacion OIDC entrante",
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
        question="Una herramienta de IA generativa para analistas debe responder consultas financieras multi-parte referenciando SEC filings internos, <b>descomponer</b> bien los prompts y <b>evitar la dilucion semantica</b>, con latencia baja y alta concurrencia, minimizando la complejidad operativa. &iquest;Que solucion conviene?",
        options=[
            "Provisionar OpenSearch Serverless para embeddings y escribir Lambdas propias que parseen y dividan los prompts antes de enviarlos al FM de Bedrock",
            "Configurar una Amazon Bedrock knowledge base con los documentos y activar la funcion nativa de query decomposition, e implementar un Bedrock flow que integre la KB con un FM",
            "Entrenar modelos NLP propios en Amazon SageMaker AI para parseo y expansion de consultas, y guardar los documentos cifrados en una KB de Bedrock",
            "Crear un indice de Amazon Kendra e usar un Bedrock agent con razonamiento avanzado para orquestar paso a paso la descomposicion de la consulta",
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
        question="Un asistente RAG de mantenimiento sobre una Bedrock KB (fuente en S3) recupera con frecuencia documentos de instalaciones, maquinas y periodos <b>no relacionados</b>, bajando la precision. Cada documento ya tiene atributos (instalacion, categoria de equipo, modelo, tipo de doc, fecha). Se quiere usar esos atributos para acotar los resultados <b>sin cambiar el modelo de embeddings ni rediseriar la KB</b>. &iquest;Que solucion mejora la relevancia con los MENOS cambios?",
        options=[
            "Habilitar un modelo de reranking en la KB para reordenar los chunks por relevancia y aumentar el numero de resultados recuperados",
            "Ingerir la metadata de los documentos de S3 mediante archivos de metadata asociados y aplicar filtrado por metadata para restringir la busqueda a los atributos relevantes",
            "Habilitar query decomposition para dividir las preguntas en subconsultas y ejecutar cada una sobre toda la fuente de S3, combinando luego los resultados",
            "Rehacer los documentos con chunks de texto mas pequenos y resincronizar la KB, manteniendo la busqueda vectorial existente",
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
        question="Un asistente RAG de seguros debe preparar ~60 GB de conversaciones (JSON en S3): <b>identificar y quitar PII</b>, <b>generar embeddings</b> y dejarlos disponibles para <b>busqueda de similitud de baja latencia</b>. Se quiere un flujo <b>gestionado</b> que coordine estas etapas con la menor infraestructura propia. &iquest;Que enfoque cumple?",
        options=[
            "Lambdas disparadas por eventos de S3 que parsean el JSON, llaman a Comprehend para PII e invocan a Bedrock para embeddings, guardando los vectores en DynamoDB con logica de similitud propia",
            "Jobs de AWS Glue ETL que procesan el JSON, quitan PII con codigo propio y llaman a Bedrock para embeddings, escribiendo los vectores de vuelta a S3 y consultando con Amazon Athena",
            "Usar AWS Step Functions para orquestar: Amazon Comprehend identifica PII, el texto saneado va a Bedrock para crear embeddings y los vectores se escriben en Amazon OpenSearch Serverless para busqueda por similitud",
            "Usar Amazon EMR Serverless con Spark para procesar, Comprehend para PII y Bedrock para embeddings, cargando los vectores en un dominio de OpenSearch autogestionado",
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
        question="Un pipeline usa Amazon Rekognition y luego un FM de Amazon Bedrock. El equipo quiere que el FM siga un <b>patron de razonamiento por pasos (ReAct)</b> y evalua AWS Step Functions para coordinar cada etapa, validar transiciones y ejecutar los pasos de forma consistente. &iquest;Que enfoque entrega ese razonamiento estructurado de la manera MAS confiable?",
        options=[
            "Una state machine que meta todas las instrucciones de razonamiento en un solo estado y dependa de una unica invocacion del FM para producir todo el razonamiento",
            "Una state machine con un estado Parallel que evalue varias direcciones de razonamiento y un Task final donde el modelo elija la mejor ruta del conjunto",
            "Una state machine que guie al FM por una cadena de pensamiento con plantillas de prompt y estados Choice que cambien la ruta segun salidas intermedias",
            "Una state machine donde cada fase de razonamiento del patron ReAct sea su propio estado, con un prompt especifico por etapa, apoyandose en el retry y manejo de errores nativos",
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
        question="Un equipo procesa grandes colecciones de videos y fotos de moda con un modelo de vision y un flujo de FM que interpreta tendencias, para alimentar un dashboard de analitica. Se busca cumplirlo con <b>MINIMO overhead operativo</b>. &iquest;Cual conviene?",
        options=[
            "Instancias Amazon EC2 con codigo propio de procesamiento de imagenes, salida en Amazon RDS y exportacion a una herramienta analitica externa para el dashboard",
            "Coordinar con AWS Step Functions el procesamiento de videos y fotos invocando FMs multimodales de Amazon Bedrock, guardar las salidas estructuradas en Amazon S3 y publicar metricas en un dashboard de Amazon Quick Suite",
            "Entrenar un modelo con Amazon Rekognition Custom Labels, guardar detecciones en Amazon DynamoDB y mostrar metricas en Amazon Managed Grafana con plugins propios",
            "Enrutar todo por un SageMaker AI Pipeline que llame a un modelo preentrenado del AWS Marketplace, guardar resultados en S3 y presentarlos en Amazon Quick Suite",
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
        question="Un equipo actualiza con frecuencia los system prompts de una app en Amazon Bedrock y quiere <b>desacoplar el ciclo de prompt engineering del despliegue de codigo</b>: los analistas deben probar variantes, guardar versiones especificas y pasar de desarrollo a produccion sin que ingenieria despliegue codigo nuevo. &iquest;Que solucion cumple?",
        options=[
            "Guardar los prompts en un bucket de Amazon S3 y una Lambda que los lea en runtime, actualizando los archivos de texto cuando los analistas cambien la version",
            "Usar Bedrock Prompt Management para crear, probar y versionar los prompts en la consola, y hacer que la app llame al endpoint de la version desplegada en el alias de produccion",
            "Codificar los prompts dentro de una state machine de Step Functions, creando una version nueva por cambio y apuntando la integracion de API Gateway a la nueva version",
            "Un modelo asincrono con Amazon SQS y Lambda que pase las nuevas versiones de prompt como payload del mensaje para construir el prompt antes de invocar el FM",
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
        question="Un asistente en tiempo real con Anthropic Claude 3 Haiku en Amazon Bedrock atiende varios continentes con picos impredecibles (mas del triple del trafico normal) y SLA de respuesta &lt; 2 s. En los picos, los endpoints se saturan (throttling, latencia, fallos). Se requiere escalado entre Regiones, maxima eficiencia de throughput y <b>evitar retry/routing propios complejos</b>. &iquest;Que solucion es la MAS efectiva?",
        options=[
            "Asignar muchas provisioned throughput model units en una unica Region primaria e implementar en la aplicacion una estrategia de retry con backoff exponencial y patrones de circuit breaker para manejar el throttling y los fallos transitorios",
            "Optimizar la inferencia agregando prompts en peticiones por lote y habilitar Cross-Region Inference en Bedrock con inference profiles por geografia, invocando endpoints por Region que distribuyen la carga automaticamente",
            "Construir una capa de aplicacion distribuida con funciones Lambda en varias Regiones y una libreria de routing propia que reparta con round-robin ponderado y escale dinamicamente el computo segun la demanda creciente",
            "Introducir un pipeline dirigido por eventos que bufferee las peticiones entrantes en colas de Amazon SQS y las procese asincronamente con servicios worker, agregando los resultados y devolviendo la respuesta al finalizar",
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
        question="Un chatbot de soporte en Amazon Bedrock atiende consultas simples (75%) y complejas de razonamiento (25%). Debe ser <b>costo-eficiente</b>, con <b>minimo overhead operativo</b> y alta calidad. &iquest;Que enfoque conviene?",
        options=[
            "Bedrock con provisioned throughput usando Claude Sonnet para todo tipo de consulta, con ElastiCache (Redis) para respuestas frecuentes y CloudWatch para escalar",
            "Aprovechar el intelligent prompt routing de Bedrock: Claude Haiku por defecto para consultas simples y Claude Sonnet como fallback para las complejas, enrutando segun la complejidad",
            "Combinar Amazon Lex para consultas simples y Bedrock para razonamiento complejo, con S3 para respuestas pregeneradas y CloudWatch para ajustar el uso",
            "Integrar Amazon SageMaker AI para fine-tuning continuo de un Claude Sonnet con feedback en tiempo real y Amazon Kendra para recuperar contexto de FAQs",
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
        question="Un chatbot RAG sobre Bedrock Knowledge Bases (embeddings en S3 Vectors) sufre porque el <b>chunking de tamano fijo</b> corta frases relacionadas en chunks distintos y algunas respuestas pierden contexto. Se quiere recuperacion coherente, respuestas relevantes y <b>costo minimo</b>. &iquest;Que configuracion conviene?",
        options=[
            "Desactivar el chunking e ingerir documentos completos como un solo chunk, confiando en la RetrieveAndGenerate API para manejar contextos largos",
            "Desplegar un Claude con la ventana de contexto maxima y aplicar summarizacion recursiva a los documentos largos antes de la ingesta",
            "Activar el semantic chunking en la Bedrock Knowledge Base y optimizar el parametro maximum tokens para basar los chunks en el significado",
            "Usar hierarchical chunking para generar chunks hijos pequenos y chunks padre grandes para la recuperacion",
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
        question="Una plataforma en tiempo real con Amazon Bedrock recibe mensajes con PII. Debe: <b>enmascarar PII antes de que el modelo procese la entrada</b>, <b>quitar datos sensibles de las respuestas</b>, y conservar los logs de interaccion solo el <b>minimo periodo de retencion</b>, con controles aprobados de almacenamiento de PII. &iquest;Que enfoque cumple?",
        options=[
            "Usar Amazon Textract para extraer texto de los logs en S3 y analizarlos por PII tras el hecho, con EventBridge disparando Textract y S3 Lifecycle + AWS Config para retencion",
            "Usar Bedrock Guardrails para enmascarar PII en las solicitudes antes de que el modelo las evalue y redactar datos sensibles de las respuestas; guardar registros en S3, activar Amazon Macie para inspeccion continua y aplicar S3 Lifecycle para retener solo lo requerido",
            "Usar el analisis de texto de Amazon Rekognition para escanear los logs almacenados en S3 en busca de informacion sensible, cifrar en reposo con AWS KMS, restringir el acceso con IAM y aplicar reglas de S3 Lifecycle que muevan los logs a Glacier Deep Archive para retencion a largo plazo",
            "Usar Bedrock Guardrails para bloquear/sanitizar PII en entradas y salidas, guardar en S3 con cifrado KMS, activar CloudTrail para la actividad de API de Bedrock y Macie para hallazgos, con reglas de S3 Lifecycle",
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
        question="Un chatbot global sobre Amazon Bedrock recibe throttling y mayor latencia en una Region en horas pico. El equipo quiere una estrategia de despliegue que evite que una Region sea cuello de botella o punto unico de falla, mantenga compliance por geografia y haga el <b>failover transparente</b> sin logica de routing manual en el cliente. &iquest;Que solucion conviene?",
        options=[
            "Usar Amazon Route 53 latency-based routing para distribuir el trafico entre endpoints de Bedrock en distintas Regiones",
            "Usar Amazon Route 53 weighted routing hacia una Region primaria con failover a una secundaria solo si la primaria falla",
            "Enviar todas las llamadas a una sola Region y escalar el endpoint para el pico, apoyandose en alarmas de CloudWatch para escalar",
            "Habilitar cross-region inference para distribuir automaticamente el trafico de la API de Bedrock entre varias Regiones de la misma geografia",
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
        question="Una app de IA generativa procesa miles de millones de registros por dia en varias Regiones (Europa, Norteamerica, Asia) y guarda salidas en Amazon S3. Regulacion: los datos deben <b>procesarse y almacenarse solo en la Region de origen</b>; se necesita <b>auditoria a prueba de manipulacion</b> de las salidas de IA y <b>descubrir/clasificar PII en reposo</b> por Region. &iquest;Que enfoque cumple todo?",
        options=[
            "Perfiles de cross-Region inference para limitar invocaciones a la Region de origen, permission boundaries de IAM, CloudWatch Logs para las salidas y Amazon Comprehend para clasificar PII",
            "SCPs de AWS Organizations para restringir ingesta/almacenamiento a la Region de origen, importar un modelo propio a cada Region y CloudTrail inmutable para auditar salidas",
            "S3 Object Lock con politicas de bucket por Region para imponer residencia, preprocesar los registros en la Region de origen, Amazon Macie para descubrir/clasificar PII y CloudTrail inmutable para auditar las salidas de IA",
            "Glue crawlers por Region para catalogar/etiquetar PII, Athena con workgroups por Region, AWS Config para detectar transferencias cross-Region y CloudWatch Logs para las salidas",
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
        question="Un asistente medico sobre una Bedrock Knowledge Base debe: mostrar PII a cirujanos pero <b>enmascararla a ingenieros</b> usando deteccion de PII, referenciar <b>solo reportes de los ultimos 3 anos</b>, y autentica con Amazon Cognito. &iquest;Que solucion cumple?",
        options=[
            "Habilitar la deteccion de PII de Amazon Macie sobre el bucket de S3 y un trigger de evento de S3 que invoque una Lambda para redactar permanentemente la informacion sensible antes de almacenar el documento, y configurar la Lambda para quitar reportes vencidos y resincronizar la knowledge base",
            "Disparar una Lambda al subir reportes para sincronizar el bucket de S3 con la knowledge base, usar otra Lambda con deteccion de PII de Amazon Comprehend para redactar la informacion sensible destinada a ingenieros, y aplicar reglas de S3 Lifecycle para borrar los reportes de mas de tres anos",
            "S3 Lifecycle para eliminar reportes de mas de 3 anos, una Lambda programada que sincronice el bucket con la knowledge base, y en tiempo de consulta aplicar deteccion de PII y Bedrock guardrails dinamicamente segun el grupo de Cognito del usuario para redactar PII en la respuesta cuando corresponda",
            "Crear una segunda knowledge base con reportes ya redactados mediante Lambda y deteccion de PII de Amazon Comprehend, y enrutar a los ingenieros a la base saneada y a los cirujanos a la base original segun la pertenencia al grupo de Cognito",
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
        question="Un sistema genera descripciones de producto, avisos de seguridad y traducciones para millones de listados. Compliance debe evaluar varios FMs de forma <b>automatica y escalable</b> en correccion, alineacion con politicas, deteccion de contenido daninno y fidelidad multilingue (la revision manual y el filtrado por keywords no bastan). &iquest;Que solucion satisface mejor la evaluacion?",
        options=[
            "Correr RAG evaluation para Bedrock Knowledge Bases y medir exactitud de recuperacion y cobertura por categoria de producto",
            "Usar Lambdas con listas de keywords y regex para marcar posibles violaciones, contar violaciones por modelo y evaluar propiedades basicas del texto",
            "Implementar Amazon OpenSearch para indexado full-text de las descripciones y comparar manualmente scores de similitud vectorial entre modelos",
            "Usar LLM-as-a-judge dentro de Amazon Bedrock Model Evaluation para puntuar automaticamente las salidas en cumplimiento de politicas, seguridad contextual, exactitud multilingue y consistencia",
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
        question="Una app convierte contenido academico heterogeneo (PDF, slides, documentos, video) en materiales estructurados: &gt;10,000 items/dia con picos de 500 subidas concurrentes. Debe interpretar texto y audio, resumir, usar prompt flows, dar <b>versionado</b> de salidas y <b>colaboracion multiusuario en tiempo real</b>. &iquest;Que solucion cumple?",
        options=[
            "Bedrock Data Automation con Lambda para ingesta/prompt flows, Bedrock Knowledge Bases para procesar documento y multimedia, salidas en DynamoDB con atributos de version y colaboracion via SNS + SQS",
            "Bedrock Data Automation (BDA) con FMs para procesar y resumir diversos insumos; Amazon Transcribe para audio y Amazon Textract para documentos; artefactos en Amazon S3 con versioning y metadata en DynamoDB; colaboracion en tiempo real con AWS AppSync (suscripciones GraphQL)",
            "Bedrock Data Automation con Step Functions para orquestar prompt flows, Textract y Transcribe para extraer, salidas en Amazon Aurora con columnas de version y colaboracion via API Gateway WebSocket con Lambda",
            "Bedrock Data Automation con Amazon Textract y Amazon Transcribe para procesar todos los tipos de contenido, salidas en Amazon S3 con versioning habilitado, prompt flows gestionados con Amazon EventBridge y coordinacion de la colaboracion con Amazon CloudFront y Amazon API Gateway",
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
        question="Una fintech integra Amazon Bedrock para un sistema conversacional sobre datos financieros regulados. Seguridad exige: <b>prevenir salida daninna</b>, <b>evitar divulgaciones no autorizadas de datos sensibles</b> y <b>detectar/bloquear contenido que indique actividad ilegal</b>, con el MENOR esfuerzo. &iquest;Que cumple?",
        options=[
            "Usar Amazon Macie para inspeccionar las respuestas del modelo en busca de datos sensibles, integrar notificaciones de Amazon SNS que disparen alertas ante contenido potencialmente ilegal y aplicar restricciones basicas a nivel de prompt en Bedrock para limitar la salida daninna",
            "Safe completion generico en Bedrock Guardrails, reglas de AWS WAF para bloquear contenido, y una alarma de CloudWatch que dispara Lambda para revisar y suprimir respuestas sensibles",
            "SageMaker Clarify para identificar patrones inseguros, limites a nivel de prompt en Bedrock y metric filters de CloudWatch para capturar indicadores de contenido ilegal",
            "Configurar content filters en Bedrock Guardrails para interceptar contenido daninno, agregar word filters para bloquear contenido prohibido/ilegal y habilitar contextual grounding checks para que las respuestas no revelen informacion sensible",
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
        question="Un chatbot RAG usa Bedrock con Claude Sonnet sobre 50,000+ chunks, pero la latencia es de 3-4 s (SLA &lt; 1 s) y debe escalar a 10,000 usuarios concurrentes, manteniendo exactitud. &iquest;Que debe implementar para cumplir el SLA sub-segundo?",
        options=[
            "Cambiar a Anthropic Claude Haiku por inferencia mas rapida, implementar hybrid search con filtrado por metadata para reducir el conjunto candidato antes de la busqueda vectorial, y usar un inference profile con cross-region routing para distribuir carga y reducir latencia en pico",
            "Aumentar las model units aprovisionadas para Claude Sonnet, agregar retry exponencial y habilitar Container Insights para monitorear el vector store, sin cambiar la estrategia de retrieval",
            "Reemplazar el vector store por Amazon Kendra para la busqueda semantica, implementar inferencia por lote en vez de tiempo real para reducir costos y usar el chunking por defecto de las Bedrock Knowledge Bases para simplificar la implementacion y mejorar los tiempos de respuesta",
            "Implementar prompt caching de los chunks recuperados con frecuencia para consultas comunes y reutilizarlos, cambiar a Bedrock Provisioned Throughput con Claude Opus para capacidad garantizada y mejor calidad, y optimizar el retrieval trayendo solo los 3 chunks mas relevantes en vez de 10",
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
        question="Un asistente RAG legal sobre Bedrock Knowledge Bases (stream con RetrieveAndGenerateStream) da respuestas suboptimas y alucina porque el retrieval inicial usa solo similitud semantica y sube documentos que parecen cercanos pero no son relevantes. Se quiere mejorar la precision con la <b>menor infraestructura adicional</b>. &iquest;Que enfoque conviene?",
        options=[
            "Desplegar un cross-encoder de reranking propio en un endpoint de SageMaker con un ALB delante e invocarlo por cada consulta para reordenar candidatos",
            "Desplegar Amazon Neptune para modelar relaciones entre documentos y usar scores de centralidad para rankear resultados antes de generar",
            "Usar la Retrieve API para traer candidatos, invocar la Bedrock Rerank API como llamada independiente para reordenar y luego InvokeModelWithResponseStream para generar",
            "Configurar la capacidad de reranking integrada de las Bedrock Knowledge Bases con los reranker models de Bedrock mas recientes, para reordenar automaticamente por relevancia contextual antes de generar",
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
        question="Un asistente en Amazon Bedrock recibe muchas preguntas <b>semanticamente equivalentes pero con distinta redaccion</b>, causando llamadas repetidas al FM por respuestas ya generadas. Se quiere reducir llamadas redundantes, dar respuestas consistentes y baja latencia, reutilizando pares consulta-respuesta previos cuando una nueva consulta sea suficientemente similar. &iquest;Que enfoque conviene?",
        options=[
            "Guardar preguntas y respuestas en Amazon DynamoDB, normalizar cada consulta entrante y usar el texto normalizado como partition key para devolver la respuesta ante coincidencia exacta",
            "Cachear respuestas en Amazon ElastiCache usando un hash de la consulta como clave, devolviendo la respuesta cacheada ante la misma consulta e invocando Bedrock en los misses",
            "Indexar los pares consulta-respuesta en Amazon OpenSearch Service y usar busqueda por keywords para localizar preguntas ya respondidas, devolviendo la respuesta del documento con mayor score cuando la relevancia por keyword supere un umbral configurado",
            "Usar Amazon OpenSearch como cache semantica: guardar embeddings de los pares consulta-respuesta en un indice k-NN, y para cada nueva consulta generar su embedding y hacer una busqueda k-NN aproximada; si hay match suficiente, devolver la respuesta cacheada",
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
        question="Un equipo mejora el troubleshooting de una app de FM en tiempo real (NLP + vision). Necesita analizar logs de multiples fuentes, <b>trazar llamadas de API entre servicios</b> y <b>detectar patrones de error especificos de GenAI automaticamente</b>, soportando modelos que evolucionan y mejorando el tiempo de respuesta a incidentes. &iquest;Que solucion conviene?",
        options=[
            "CloudWatch Logs Insights para agregar logs, Amazon SageMaker AI para deteccion de anomalias por ML sobre los logs y Lambda para disparar alertas en tiempo real",
            "CloudWatch Logs Insights para consultar y correlacionar logs en tiempo real, AWS X-Ray para trazar llamadas de API entre la app y fuentes externas, y Amazon Q Developer para reconocimiento de patrones de error de GenAI",
            "CloudWatch Logs Insights para analisis por tipo de error, AWS X-Ray para trazar entre microservicios internos y AWS Glue para automatizar la extraccion/transformacion de los datos de error",
            "CloudWatch Logs Insights para recolectar logs de APIs externas, AWS X-Ray para monitorear las llamadas a los modelos GenAI y Amazon Kinesis para transmitir y analizar los datos de error en tiempo real",
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
        question="Una app de IA generativa para salud debe cruzar terminologia medica muy tecnica contra una base privada de documentos clinicos, <b>evitando la dilucion semantica</b> y sosteniendo 1,000 consultas/minuto con latencia &lt; 2 s, con el MENOR overhead operativo. &iquest;Que solucion conviene?",
        options=[
            "Guardar los documentos en un indice de Amazon Kendra y desplegar un Bedrock agent que use Step Functions para procesar manualmente la descomposicion de consultas",
            "Montar una knowledge base con los documentos, habilitar la query decomposition nativa para reducir la dilucion semantica y construir un Bedrock flow que enlace un FM con la knowledge base",
            "Desplegar modelos ML propios de descomposicion y expansion de consultas en Amazon SageMaker AI y guardar los documentos en una knowledge base de Bedrock",
            "Ingerir los documentos en una coleccion vectorial de OpenSearch Serverless y usar un Bedrock agent con plantillas de prompt avanzadas para la descomposicion, enrutando por API Gateway",
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
        question="Un sistema de resumen de feedback con Amazon Bedrock guarda prompts y resumenes en S3. Por regulacion se requiere: <b>registrar todas las interacciones con Bedrock</b> para compliance, <b>trazabilidad de linaje</b> de cada prompt y resumen, y <b>rastrear las versiones de plantilla y las invocaciones de modelo</b>. &iquest;Que cumple?",
        options=[
            "Aprovechar Amazon Data Firehose para transmitir los datos de prompt hacia S3 en tiempo real, usar funciones AWS Lambda para parsear y guardar los logs de invocacion de modelo en Amazon DynamoDB, y habilitar Amazon CloudWatch para monitorear todas las interacciones de prompts y resumenes",
            "Configurar un Amazon Kinesis Data Stream para capturar en tiempo real los datos de prompts y resumenes, y usar Amazon Athena para consultar y auditar la metadata almacenada en Amazon S3 con fines de cumplimiento",
            "Guardar los prompts y resumenes en Amazon DynamoDB con atributos de metadata adicionales, y utilizar DynamoDB Streams para disparar funciones AWS Lambda que procesen las actualizaciones relacionadas con el linaje y el seguimiento de metadata",
            "Habilitar server access logging en S3 para las interacciones con prompts/resumenes, usar AWS CloudTrail para registrar todas las llamadas de API a Bedrock y configurar Bedrock Prompt Management para el linaje de prompts y la metadata de modelo",
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
        question="Un banco lanza una solucion GenAI en Amazon Bedrock. Necesita: bloquear contenido daninno, detectar/mitigar alucinaciones, <b>monitoreo en tiempo real de comportamiento y drift</b>, y un <b>log inmutable y auditable</b> de todas las interacciones, en 60 dias, con latencia &lt; 200 ms e integracion con dashboards de compliance, con el MENOR overhead. &iquest;Que enfoque cumple?",
        options=[
            "Bedrock Guardrails como marco de seguridad de contenido, Bedrock Model Evaluations para calidad y alucinaciones, logs de prompt-respuesta en Amazon DynamoDB con TTL, y metricas custom a CloudWatch para monitorear comportamiento y drift, alimentando el dashboard existente",
            "Lambdas propias para evaluar exactitud y aplicar politicas de seguridad, un endpoint de SageMaker Model Monitor para drift, y archivar los pares en S3 exportando los eventos al dashboard",
            "Bedrock Agents + Knowledge Base para grounding, filtros de seguridad con un clasificador de texto propio en SageMaker, e ingestar los pares en OpenSearch conectado a QuickSight",
            "Desplegar AWS WAF delante de Amazon API Gateway para filtrar prompts entrantes por amenazas de inyeccion y aplicar rate limiting, usar Amazon Macie para analizar las respuestas y detectar alucinaciones y drift, archivar todas las interacciones en Amazon RDS Multi-AZ y conectar los log streams de CloudWatch al dashboard",
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
        question="Un asistente de compliance hace busqueda semantica sobre documentos regulatorios en tres idiomas, con <b>filtrado por metadata</b> (fecha, autoridad, categoria), ~10 millones de embeddings que requieren <b>optimizacion automatica de indice</b> para latencia sub-segundo sin tuning manual, y un enfoque <b>totalmente gestionado</b>. &iquest;Que solucion cumple?",
        options=[
            "Configurar Amazon OpenSearch Serverless como vector store para similitud y filtrado por metadata, y usar Bedrock Knowledge Bases para un pipeline RAG con un FM Anthropic Claude",
            "Un cluster Amazon Aurora PostgreSQL con pgvector; disenar esquemas relacionales para embeddings + metadata y ejecutar similitud por SQL, enviando los documentos a Bedrock",
            "Amazon Kendra como buscador empresarial con attribute filters por autoridad/fecha/categoria, conectando los resultados a Bedrock",
            "Amazon MemoryDB con vector search para 10M embeddings, aplicando pre-filtros de metadata y enviando resultados a Bedrock",
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
        question="Una institucion financiera tiene un data lake en AWS Lake Formation y quiere que un FM de Bedrock acceda a registros para AML, pero debe <b>enmascarar PII a nivel de columna</b>, restringir el acceso del FM a subconjuntos autorizados y <b>registrar todos los accesos</b> para auditoria. &iquest;Que enfoque cumple?",
        options=[
            "Habilitar Amazon Macie para escanear y clasificar la PII en las ubicaciones de S3 del data lake, configurar S3 access points con politicas basadas en roles IAM para servir subconjuntos de datos pre-filtrados al FM y usar S3 server access logging para retener el registro de todas las solicitudes de recuperacion",
            "Crear LF-Tags en Lake Formation por division/mercado y aplicarlas a bases, tablas y columnas; autenticar al FM con roles IAM e imponer permisos de Lake Formation con expresiones LF-Tag que excluyan las columnas PII, y registrar accesos con AWS CloudTrail",
            "Aplicar reglas de AWS Glue Data Quality para marcar columnas PII, redactar con Glue Studio ETL a un prefijo S3 dedicado, dar acceso al FM por IAM y auditar con CloudWatch Logs",
            "Que el FM asuma un rol IAM y pida credenciales temporales a STS, usar una API middleware que genere presigned URLs de S3 con filtros por division/region y auditar con CloudTrail",
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
            "Construir una Amazon Bedrock Knowledge Base con hybrid search habilitado, enriquecer los documentos con metadata de Kendra y usar Personalize para guiar la recuperacion y las recomendaciones del asistente",
            "Ingestar y transformar el contenido de forma continua con Bedrock Data Automation, usar Personalize para recomendar y hacer full-text search con Kendra de forma independiente",
            "Orquestar los modelos con Bedrock Prompt Flows, llamar a Kendra y Personalize para rankear/personalizar salidas y guardar resultados fuera de una knowledge base centralizada",
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
        question="Una firma financiera evalua su chatbot en Amazon Bedrock antes de produccion. La residencia de datos <b>prohibe inferencia cross-Region</b> (todo debe correr en la Region del cliente) y compliance quiere una evaluacion estructurada de cuan bien el chatbot <b>identifica y suprime PII</b> en sus respuestas. &iquest;Que solucion cumple?",
        options=[
            "Guardar todos los logs de conversacion del chatbot en un bucket de Amazon S3 con cifrado del lado del servidor, usar Amazon Macie para escanear automaticamente en busca de PII y configurar un flujo de AWS Step Functions que redacte la PII detectada antes de incluir los registros en los reportes de compliance",
            "Configurar un Bedrock Guardrail con sensitive information filters en entradas y salidas, usar mask mode en la fase de evaluacion, pasar a block mode en produccion, y provisionar una instancia de guardrail dedicada en cada Region donde haya clientes",
            "Activar Guardrails con sensitive information filters en detect mode, transmitir salidas marcadas a Kinesis Data Stream y redactar PII con un job de AWS Glue antes de entregar en produccion",
            "Implementar filtrado de contenido y de palabras configurando un guardrail de Bedrock cross-Region, empezar en detect mode para monitorear y registrar violaciones de politica durante la evaluacion, y pasar a mask mode para hacer cumplir en el entorno de produccion",
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
        question="Un chatbot llama a Bedrock InvokeModel desde Lambda. En produccion aparecen salidas inesperadas y <b>no hay visibilidad</b> de que prompts se envian a Bedrock ni de las respuestas crudas. Hace falta un mecanismo de logging para depurar, auditar y trazar el <b>contenido completo de prompts y completions</b> de cada llamada, <b>sin modificar la logica de negocio</b>. &iquest;Que enfoque es mas efectivo?",
        options=[
            "Agregar sentencias de logging de CloudWatch en la Lambda para registrar el mensaje de entrada y la respuesta que devuelve InvokeModel",
            "Usar AWS X-Ray para trazar las ejecuciones de la Lambda e identificar demoras en las llamadas a InvokeModel",
            "Habilitar el model invocation logging de Bedrock para capturar prompts y respuestas crudos configurando un InvocationLogsConfig que entregue logs a Amazon S3",
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
        question="Un agente de soporte usa embeddings propios (SageMaker JumpStart) y Amazon Bedrock. Recibe miles de consultas casi duplicadas al dia y cada invocacion del FM cuesta y agrega latencia. Se quiere <b>reconocer consultas semanticamente similares ya respondidas y servir la respuesta cacheada</b>, generando fresco solo ante preguntas nuevas. &iquest;Que solucion cumple?",
        options=[
            "Usar un store clave-valor en memoria para cachear strings de request y respuesta exactos, y llamar al FM solo si falta la clave exacta",
            "Pre-computar embeddings con SageMaker AI, guardarlos en una base relacional y buscar por coincidencia exacta de string antes de invocar el FM",
            "Guardar embeddings de consultas y respuestas en Amazon MemoryDB con vector search habilitado e implementar semantic caching para devolver respuestas cacheadas en lugar de invocar el FM",
            "Integrar Amazon Kendra para indexar todas las consultas y respuestas y usar su busqueda para recuperar consultas similares antes de invocar el FM",
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
        question="Una app usa Amazon Bedrock con una cadena de prompts de tres etapas. Presenta: recomendaciones <b>inconsistentes para entradas identicas</b>, alta latencia de recuperacion y <b>salidas inseguras</b> (concentraciones fuera de limites). Hay que desplegar controles de seguridad validados, garantizar <b>consistencia &gt;= 99.5%</b> para entradas identicas y bajar la latencia a &lt; 1 s. &iquest;Que solucion cumple todo?",
        options=[
            "Habilitar Bedrock provisioned throughput para latencia consistente entre Regiones, implementar Bedrock Guardrails con reglas de denegacion semantica para bloquear salidas inseguras y usar Bedrock Prompt Management con flujos de aprobacion para gobernar y versionar las plantillas de la cadena",
            "Correr jobs de model evaluation para las tres etapas, desplegar un modelo de validacion secundario en un endpoint de SageMaker y configurar alarmas de CloudWatch que disparen rollbacks automaticos ante inconsistencia",
            "Cachear salidas de entradas repetidas en Amazon ElastiCache, preprocesar las preferencias con Lambda antes de cada etapa e integrar AWS X-Ray para monitorear la latencia extremo a extremo",
            "Aplicar prompt compression a la cadena de tres etapas para reducir el uso de tokens y mejorar el throughput de la etapa de recuperacion, usar Bedrock Agents para orquestar y gestionar las salidas de cada etapa, y usar Amazon Comprehend para detectar y marcar formulaciones que excedan los umbrales seguros de concentracion antes de entregarlas",
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
        question="Un proveedor industrial genera embeddings con SageMaker y responde via Bedrock. Almacena millones de registros y requiere recuperacion semantica <b>mas filtrado por metadata relacional</b> (tipo de equipo, fecha, severidad), con carga eficiente de embeddings, busqueda ANN de alta velocidad e <b>integracion directa con el entorno de metadata relacional</b>. &iquest;Que solucion cumple?",
        options=[
            "Configurar la extension pgvector en Amazon Aurora (PostgreSQL Compatible), construir un indice HNSW sobre la columna de embeddings, cargar los embeddings desde SageMaker, hacer join con tablas de metadata y consultar desde Bedrock via recuperacion integrada",
            "Usar Amazon OpenSearch Service con su motor de busqueda vectorial K-NN, cargar alli los embeddings generados por SageMaker AI, almacenar la metadata dentro del propio indice de OpenSearch y reenviar los IDs de documento recuperados a Bedrock para la generacion",
            "Desplegar PostgreSQL con embeddings como arrays o JSON, usar UDFs para calcular similitud coseno en runtime, hacer join con metadata e invocar la recuperacion desde Bedrock",
            "Usar SageMaker Feature Store para embeddings y metadata y, en tiempo de consulta, invocar un endpoint real-time de SageMaker para calcular los vecinos y pasar los resultados a Bedrock",
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
        question="Una app medica en Amazon Bedrock resume registros y sufre <b>alucinaciones factuales</b> intermitentes; el gasto supera el presupuesto 40%. Se necesita observabilidad casi en tiempo real para <b>descubrir alucinaciones</b>, monitorear el consumo de tokens y alertar temprano por picos de costo, con el MENOR overhead. &iquest;Que solucion cumple?",
        options=[
            "Alarmas de CloudWatch sobre InputTokenCount/OutputTokenCount, enviar los invocation logs a S3 con captura de texto e integrar AWS Glue + Athena para analizar y detectar alucinaciones casi en tiempo real",
            "Bedrock Model Evaluation en jobs automatizados continuos para detectar alucinaciones y stream de invocation logs a CloudWatch Logs con Logs Insights para detectar picos de tokens",
            "Exportar los model invocation logs de Bedrock (con text output activado) a Amazon S3, aplicar Bedrock guardrails con contextual grounding checks para marcar inexactitudes factuales y desplegar alarmas de anomaly detection de CloudWatch sobre las metricas de tokens",
            "Desplegar un Bedrock agent configurado con un Action Group de AWS Lambda para validar dinamicamente las salidas en busca de alucinaciones factuales, y exportar los model invocation logs a Amazon OpenSearch Service con alertas propias para detectar desviaciones en la capacidad de procesamiento de tokens",
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
            '<div class="extra"><span class="h">Exam tip</span>Detectar alucinaciones inline = Guardrails contextual grounding checks. Picos de tokens/costo = CloudWatch anomaly detection (baseline, no umbral fijo). Glue/Athena es batch; Model Evaluation es offline.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html">docs.aws Guardrails contextual grounding</a></div>'
        ),
    ),
    # ============================================================
    # Q59 - Semantic caching de prompts
    # ============================================================
    card(
        question="Un pipeline GenAI multi-region tiene muchas invocaciones al FM desde flujos recurrentes con prompts <b>redactados distinto pero con el mismo intento</b>, causando sobrecostos y picos de latencia. Se necesita una estrategia de caching que <b>evite llamadas redundantes para prompts con el mismo significado</b>, soporte multi-region, genere claves de cache consistentes y salidas cacheadas confiables. &iquest;Que estrategia conviene?",
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
        question="Una financiera usa Amazon Bedrock para resumir evaluaciones de riesgo. Aun con limites de longitud de generacion, hay <b>detalles financieros fabricados</b> y el costo excede la proyeccion 35%. Se necesita monitoreo casi en tiempo real para detectar alucinaciones, identificar consumo anormal de tokens y avisar temprano de anomalias de costo, minimizando desarrollo y mantenimiento. &iquest;Que solucion cumple?",
        options=[
            "Configurar alarmas de Amazon CloudWatch sobre las metricas InputTokenCount y OutputTokenCount para vigilar actividad inusual, archivar los model invocation logs en un bucket de Amazon S3 y usar AWS Glue con Amazon Athena para analizar las salidas almacenadas y detectar posibles alucinaciones factuales",
            "Usar Amazon Comprehend para analizar el texto de salida del FM en busca de inconsistencias factuales y asignar puntajes de calidad, y configurar una regla de Amazon EventBridge que se dispare con los eventos de invocacion y enrute las metricas de uso de tokens a un topico de Amazon SNS para notificaciones de costo",
            "Habilitar el model invocation logging de Bedrock con text output en S3, configurar Bedrock Guardrails con un contextual grounding check para detectar alucinaciones y crear alarmas de anomaly detection de CloudWatch sobre metricas de tokens para consumo anormal y avisos tempranos de costo",
            "Enviar los invocation logs a Amazon OpenSearch via Firehose y usar el plugin de Observability para dashboards y reglas de anomalia propias que detecten patrones de tokens y alucinaciones",
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
        question="Un asistente en Amazon Bedrock debe traer datos de una REST API interna que exige una API key que <b>expira cada 30 minutos</b> y hay que refrescar; la key nueva se obtiene dinamicamente de un proveedor OAuth. La solucion se integra en un metodo de Amazon API Gateway, con acceso seguro, gestion de tokens y baja latencia. &iquest;Cual es el mejor enfoque?",
        options=[
            "Integrar API Gateway con Lambda por proxy: la Lambda autentica via OAuth, obtiene un token fresco y lo pasa como header al Bedrock agent para llamar al sistema externo",
            "Una Lambda propia integrada con API Gateway que genere el token OAuth y lo inyecte como header custom para el Bedrock agent; el metodo de API Gateway invoca la Lambda pasando request y token al agente",
            "Usar Amazon CloudFront para cachear las credenciales y tokens OAuth, configurar una funcion AWS Lambda que obtenga el token desde el cache de CloudFront y realice la llamada a la API externa, y hacer que el metodo de API Gateway invoque esa Lambda para pasar el token al Bedrock agent",
            "Desarrollar una Lambda para el action group del Bedrock agent que maneje la generacion del token OAuth y llame a la REST API externa; configurar el metodo de API Gateway para usar la Bedrock InvokeAgent API y otorgar los permisos IAM adecuados",
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
            "Un HTTP API con API Gateway y Lambda, Step Functions para procesamiento en paralelo, resultados parciales en DynamoDB y un DynamoDB Stream que dispare una Lambda para enviar updates",
            "Un WebSocket API con Amazon API Gateway y AWS Lambda, usando la InvokeModelWithResponseStream API de Bedrock para transmitir resultados por WebSockets y una Lambda que maneje conexiones y entregue mensajes dinamicamente",
            "Un REST API con Amazon API Gateway y AWS Lambda que use la InvokeModel API de Bedrock para procesar las solicitudes de forma secuencial y guardar las respuestas en Amazon S3, con polling del lado del cliente via setInterval para buscar actualizaciones",
            "Un API en tiempo real con AWS AppSync y resolvers Lambda, un esquema GraphQL para stream e InvokeModel con suscripciones para actualizar clientes",
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
        question="Un portal de soporte con un FM de Bedrock debe filtrar mensajes con Amazon Comprehend antes de pasarlos al FM: detectar/suprimir lenguaje ofensivo, detectar y <b>redactar PII</b>, y marcar mensajes que soliciten consejos inapropiados. El pipeline debe completarse en el preprocesamiento <b>sin retrasar la invocacion del FM</b>. &iquest;Que arquitectura cumple?",
        options=[
            "Correr todas las operaciones en paralelo con APIs asincronas: toxicity detection para bloquear ofensivo, prompt safety classification para consejos inapropiados y PII detection con redaccion de entidades antes de llegar al FM",
            "Una Lambda que evalue cada mensaje contra una blocklist en DynamoDB y, si pasa, invoque toxicity detection; reenviar solo los mensajes limpios al FM y loguear los marcados en S3",
            "Una cola SQS que bufferee los mensajes, una Lambda que llame a Comprehend PII y guarde versiones redactadas en S3, y Bedrock Guardrails con topic filters antes de enrutar al FM",
            "Activar toxicity detection con umbrales de 0.5 en todas las categorias, ejecutar prompt safety classification y PII detection con redaccion en paralelo, y monitorear el pipeline con alarmas de CloudWatch antes de reenviar al FM",
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
            "Plantillas reutilizables con parametros por cliente y versionado con proceso formal de revision, Bedrock Guardrails para el estilo y Amazon CloudWatch para monitorear uso y modificaciones de plantillas",
            "Bedrock Guardrails para asegurar las guias de estilo, AWS CloudTrail para logs detallados de uso y cambios, y versionado para gestionar actualizaciones",
            "Plantillas reutilizables con parametros por cliente y versionado con un proceso formal de revision, Bedrock Guardrails para imponer reglas de estilo y AWS CloudTrail para rastrear modificaciones y uso de plantillas para compliance",
            "Plantillas parametrizadas en Prompt Management con versionado, Amazon Comprehend para imponer reglas de estilo (tono, keywords) y AWS CloudTrail para monitorear cambios y uso",
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
            "Lambda que invoque Amazon Rekognition al subir cada documento para escanear identificadores, KBs separadas por rol con enrutamiento por grupo de Cognito y S3 Lifecycle para borrar mayores a 3 anos",
            "Un Bedrock agent con action group que en cada consulta obtenga el grupo de Cognito y llame a Amazon Comprehend para detectar y redactar PII antes de responder, con S3 Lifecycle para 3 anos",
            "Una regla de S3 Lifecycle que expire documentos de mas de 3 anos, una Lambda programada que sincronice el bucket con la KB y, por sesion, determinar el grupo de Cognito e invocar la ApplyGuardrail API para redactar PII segun el rol",
            "S3 Lifecycle de 3 anos, una Lambda que al llegar un archivo lo empuje a la KB primaria, y otra KB secundaria con contenido pre-redactado via Comprehend, enrutando por grupo de Cognito",
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
        question="Una firma quiere un <b>agente de investigacion totalmente autonomo</b>: ante una transaccion marcada, debe invocar inferencia en SageMaker AI, traer imagenes de Rekognition, llamar APIs internas y decidir si escalar a revision manual o cerrar la cuenta. Necesita integracion con AWS, <b>integraciones de herramientas personalizadas</b> y <b>seleccion de multiples FMs</b> para el razonamiento. &iquest;Que solucion es la mas apropiada?",
        options=[
            "Usar Amazon Bedrock Agents con action groups predefinidos para SageMaker AI y Rekognition y dejar que el agente orqueste todos los pasos",
            "Usar el AWS Strands Agents SDK para construir un agente autonomo personalizado que integre SageMaker AI, Rekognition y APIs internas, seleccionando un FM via Amazon Bedrock",
            "Un orquestador basado en Lambda con AWS Step Functions que llame secuencialmente a SageMaker, Rekognition y APIs internas y use un motor de reglas simple para la logica de escalado",
            "SageMaker AI Pipelines que ejecuten la inferencia y el chequeo de Rekognition como pasos, con una estrategia de causal chain prompting embebida en el modelo para decidir",
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
        question="Una biotech tiene un modelo Llama personalizado (entrenado en SageMaker, exportado en formato Hugging Face con .safetensors, artefactos en S3) y quiere desplegarlo en Amazon Bedrock para produccion. La carga es <b>predecible</b> y se busca <b>no gestionar infraestructura</b> con inferencia de <b>baja latencia y alto throughput</b> concurrente. &iquest;Que solucion conviene?",
        options=[
            "Convertir el modelo al formato ONNX y desplegarlo sobre Amazon EC2 Auto Scaling Groups con un load balancer al frente para manejar los picos de trafico y escalar la capacidad de inferencia",
            "Importar los archivos del modelo en formato Hugging Face desde S3 con Bedrock Custom Model Import y desplegarlo usando inferencia on-demand para un despliegue flexible de pago por uso",
            "Usar Bedrock Custom Model Import para importar el modelo Llama .safetensors desde S3 y desplegarlo con Bedrock Provisioned Throughput para inferencia consistente y de baja latencia a escala",
            "Importar el modelo Llama afinado en SageMaker Serverless Inference para obtener inferencia con escalado automatico y pago por uso ante cargas de trabajo fluctuantes",
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
            "AWS DataSync para transferir periodicamente los documentos a un bucket S3 central y Amazon EMR para procesar/reestructurar, con jobs cron para re-copiar y re-procesar en intervalos fijos",
            "Unificar el acceso con Amazon Bedrock Knowledge Bases, configurar data source connectors para cada base y wiki, y habilitar la sincronizacion automatica para mantener el contenido actualizado",
            "Amazon AppFlow para las fuentes SaaS y AWS Transfer Family para las de archivo, alimentando Amazon OpenSearch y coordinando refrescos con AWS Step Functions",
            "Amazon Neptune como grafo central de conocimiento con scripts de ingesta para convertir todo a formato de grafo y actualizaciones por lote programadas",
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
            "Cachear registros en DynamoDB, una Lambda que transforme los registros cacheados en prompts, Bedrock Guardrails para filtrar salidas y Step Functions para orquestar y reducir alucinaciones",
            "Text-to-SQL con validaciones SQL para extraer registros de RDS, alimentar el modelo importado via Custom Model Import, Bedrock Guardrails para seguridad y Step Functions + Lambda para un workflow de validacion post-inferencia que suprima alucinaciones",
            "Ingerir el historial de RDS a un data lake S3 con Glue ETL, materializar features con Athena en tiempo de inferencia, Guardrails para filtrar y Step Functions para orquestar y reducir alucinaciones",
            "Text-to-SQL con validaciones SQL para extraer registros de RDS, alimentar el modelo importado via Bedrock Custom Model Import, imponer seguridad con Bedrock Guardrails y aplicar confidence scoring y busquedas de similitud semantica para medir la relevancia y reducir alucinaciones",
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
            "Enviar el audio a Amazon Transcribe pero esperar a que cada segmento se finalice antes de mandar el texto a Bedrock con InvokeModel, y devolver la respuesta completa via un REST API de API Gateway",
            "Habilitar partial-result streaming en Amazon Transcribe para tener segmentos interinos mientras el cliente habla, enviar los fragmentos a Bedrock con InvokeModelWithResponseStream y entregar la salida en streaming a los agentes via un WebSocket API de Amazon API Gateway",
            "Enviar el audio a Amazon Transcribe con partial results habilitado y escribir cada fragmento de transcripcion en Amazon Kinesis Data Streams, usar AWS Lambda para agrupar los fragmentos e invocar a Amazon Bedrock tras acumular suficiente contexto, y devolver la respuesta generada via un WebSocket API de Amazon API Gateway",
            "Transcribe streaming con partial results enviando fragmentos a Bedrock con InvokeModelWithResponseStream, pero bufferizar todos los chunks generados en Lambda y enviar la respuesta completa via WebSocket API",
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
        question="Una agencia gubernamental usa Amazon Bedrock para generar recomendaciones de alerta temprana a partir de telemetria de sensores que llega por Amazon Kinesis Data Streams. Por regulacion, <b>toda recomendacion generada por IA debe ser revisada y aprobada por un oficial certificado antes de emitir la alerta al publico</b>, y hay que <b>guardar un registro de cada decision de revision</b> para auditoria. &iquest;Que enfoque cumple?",
        options=[
            "Un flujo de AWS Step Functions con un estado de revision humana que usa la API waitForTaskToken para suspender la ejecucion hasta que el oficial responda; al recibir la decision, una Lambda llama a SendTaskSuccess con el resultado y las decisiones se persisten en Amazon DynamoDB para auditoria",
            "Un flujo de AWS Step Functions con un estado de aprobacion basado en callback que emite un task token y detiene la ejecucion a la espera del oficial; una Lambda llama a SendTaskSuccess para reanudar y las decisiones se archivan en Amazon DynamoDB, sin definir que dispara esa Lambda tras la decision",
            "Enviar cada recomendacion desde Kinesis a un topic de Amazon MSK (Kafka); una Lambda consumidora la reenvia al oficial por Amazon SNS y las respuestas de aprobacion se registran en una base de datos Amazon Aurora para fines de auditoria",
            "Una API GraphQL de AWS AppSync empuja las recomendaciones a un dashboard del oficial en tiempo real; una Lambda suscrita a la mutacion captura la aprobacion y los resultados se guardan en Amazon S3 mediante notificaciones de eventos para el reporte de auditoria",
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
        question="Una empresa despliega un sistema de moderacion de contenido con IA generativa que evalua texto con <b>varios modelos de fundacion (FM) de Amazon Bedrock</b> para comparar calidad y relacion latencia/calidad. Debe desplegarse en entornos <b>staging y produccion</b> de forma <b>automatizada y consistente</b>, permitir que los product managers <b>cambien de modelo sin tocar el codigo</b> y estandarizar la configuracion por modelo. &iquest;Que arquitectura conviene?",
        options=[
            "Una unica app de AWS CDK que integra Bedrock con FoundationModel.fromFoundationModelId() y un unico pipeline de AWS CodePipeline con varias etapas de despliegue para staging y produccion, usando acciones de AWS CodeBuild por etapa y habilitando el cambio controlado entre FMs",
            "Una unica app de AWS CDK con varios pipelines de AWS CodePipeline, cada uno con parametros para un FM distinto, invocando los modelos mediante ProvisionedModel.fromProvisionedModelArn() para la evaluacion multi-modelo entre entornos",
            "Apps de AWS CDK separadas para staging y produccion, desplegadas de forma independiente con proyectos de AWS CodeBuild, seleccionando los FMs de Bedrock mediante configuracion estatica almacenada en objetos de Amazon S3 por entorno",
            "Una unica app de AWS CDK solo para produccion automatizada con CodePipeline y CodeBuild; el entorno de staging se configura manualmente y la seleccion del FM de Bedrock se gestiona con variables de entorno fuera del pipeline",
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
        question="Un agente de Amazon Bedrock da recomendaciones de despacho usando datos en vivo (SageMaker AI para ETAs, Amazon Comprehend para feedback de conductores). Debe integrar una <b>herramienta de telemetria propia que mantenga una conexion WebSocket de larga vida</b> para transmitir eventos GPS continuos. Las pruebas con opciones serverless fallaron por <b>timeouts por limites de ejecucion</b>. Se necesita un despliegue que soporte sesiones de red persistentes <b>sin gestionar servidores</b>. &iquest;Que solucion cumple?",
        options=[
            "Desplegar la herramienta de telemetria como contenedor en Amazon ECS con el tipo de lanzamiento AWS Fargate, que soporta conexiones WebSocket de larga vida sin administrar servidores",
            "Desplegar la herramienta de telemetria en Amazon EC2 con un script propio que mantenga viva la sesion WebSocket y escale las instancias segun la carga",
            "Ejecutar la herramienta de telemetria en AWS Lambda y refrescar la sesion WebSocket con invocaciones programadas para simular una conexion continua",
            "Desplegar la herramienta como servicio contenedorizado en Amazon App Runner con autoescalado para gestionar las conexiones WebSocket y la carga variable",
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
        question="Una plataforma de soporte usa API Gateway que dispara Lambda, y Lambda llama a la API de Amazon Bedrock. En pruebas de carga aparecen latencia intermitente y errores <b>ThrottlingException</b> en las llamadas a Bedrock durante los picos de concurrencia. Hay que manejar el trafico pico y <b>reducir la frecuencia de ThrottlingException</b> manteniendo respuestas rapidas. &iquest;Que se debe implementar?",
        options=[
            "Inicializar exponential backoff con jitter en el AWS SDK para la gestion de reintentos, y configurar limites de throttling por cliente en API Gateway para controlar la tasa de solicitudes en los picos",
            "Habilitar AWS Global Accelerator para optimizar el enrutamiento del trafico y reducir la latencia acortando los saltos de red durante los eventos de alta demanda",
            "Usar AWS Step Functions para gestionar el flujo de solicitudes con un mecanismo de reintento de intervalo fijo que mantenga la capacidad de respuesta bajo alta carga",
            "Implementar reintento exponencial en el AWS SDK, con tiempos de espera crecientes de forma constante entre reintentos para gestionar el throttling en el pico",
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
        question="Una empresa de investigacion legal prepara grandes volumenes de datos no estructurados (expedientes, transcripciones, documentos regulatorios) en Amazon S3 para una app de Amazon Bedrock. Antes de pasar los documentos al FM debe: <b>descubrir y catalogar</b> las fuentes, generar metadata auditable, aplicar <b>transformaciones y logica de chunking a medida</b>, y <b>validar los datasets procesados con seguimiento continuo de metricas de calidad</b> para detectar problemas antes del uso, minimizando desarrollo e infraestructura. &iquest;Que solucion cumple?",
        options=[
            "Un crawler de AWS Glue descubre las fuentes y registra su metadata en el Glue Data Catalog; jobs de Glue ETL aplican las transformaciones y el chunking, y AWS Glue Data Quality evalua los datos procesados y trackea las metricas de calidad antes de exponerlos a Bedrock",
            "Funciones AWS Lambda disparadas por subidas a S3 parsean los documentos, generan metadata y hacen el chunking; guardan resultados en Amazon DynamoDB, publican metricas de calidad en Amazon CloudWatch y envian el contenido validado a Bedrock",
            "Amazon EMR Serverless con jobs de Apache Spark descubre y transforma los documentos, implementa reglas de validacion y chunking en Spark, guarda la metadata de proceso en S3 y entrega la salida a Bedrock",
            "Amazon Athena consulta los datos en S3 y mantiene la metadata en tablas del Glue Data Catalog; funciones Lambda programadas validan y hacen el chunking y reescriben el contenido a S3 para Bedrock",
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
        question="Una fintech tiene un modelo de Amazon SageMaker AI que genera estimaciones en tiempo real; sus datos de entrenamiento en Amazon S3 crecen de continuo. Quiere <b>eliminar el reentrenamiento manual</b> con un pipeline automatizado que dispare reentrenamiento y <b>redepliegue</b> el modelo cada vez que un analista sube un nuevo dataset a S3, con orquestacion <b>durable</b> (reintentos, log, auditoria). &iquest;Que solucion cumple?",
        options=[
            "Un flujo AWS Step Functions Standard: el primer estado invoca una Lambda con handler que responde a la subida del archivo a S3, y el siguiente estado ejecuta SageMaker AI Pipelines para reentrenar y redesplegar el modelo tras recibir la respuesta",
            "Una regla de Amazon EventBridge que monitorea el bucket y enruta el evento directamente a SageMaker AI Pipelines, que reentrena el modelo y actualiza el endpoint al completar el pipeline",
            "AWS Glue cataloga y perfila cada dataset nuevo, un job de Glue DataBrew normaliza los datos y luego se llama al endpoint existente de SageMaker AI con esos datos para generar predicciones actualizadas sin reentrenar",
            "Un flujo AWS Step Functions Express con integraciones del SDK que trae los datos de S3, exporta con SageMaker AI Data Wrangler a Autopilot y usa Autopilot para redesplegar el modelo reentrenado",
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
        question="Un asistente de IA generativa da recomendaciones de producto, mensajes promocionales y resumenes de soporte en tiempo real (usa Amazon Comprehend para sentimiento/entidades y SageMaker AI para scoring de engagement). Antes del despliegue total, el equipo quiere una <b>evaluacion sistematica comparando varias versiones de modelo a la vez</b>, recolectando metricas de desempeno para decidir con datos. &iquest;Que estrategia de despliegue es la mas apropiada?",
        options=[
            "Usar una estrategia de A/B testing que enruta segmentos de usuarios a varias versiones de modelo simultaneamente, recolecta metricas con Comprehend y SageMaker AI y elige el mejor modelo",
            "Desplegar con estrategia Blue/Green, corriendo el nuevo modelo en paralelo con el actual, recolectar metricas con Comprehend y SageMaker AI y cambiar todo el trafico tras verificar estabilidad",
            "Desplegar el nuevo modelo como Canary a un subconjunto pequeno de usuarios, monitorear sentimiento y engagement con Comprehend y SageMaker AI y subir el trafico de forma gradual si cumple la calidad",
            "Implementar un despliegue Linear que desplaza el trafico al nuevo modelo en incrementos fijos, monitoreando desempeno y engagement con Comprehend y SageMaker AI en cada incremento",
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
        question="Una empresa usa un FM para escribir descripciones de catalogo. DevOps monitorea con Amazon CloudWatch metricas tecnicas (consumo de tokens, latencia, tasa de fallos); ventas mide metricas comerciales (CTR, impacto en ingresos) en sistemas externos. Se requiere observabilidad <b>unificada que correlacione desempeno con resultados comerciales</b> y que <b>alerte automaticamente ante degradacion anomala</b>. &iquest;Que solucion cumple?",
        options=[
            "Construir dashboards de CloudWatch que agreguen los datos operativos y las metricas comerciales importadas; usar composite alarms de CloudWatch potenciadas con anomaly detection para evaluar los datos correlacionados y Amazon SNS para alertar al personal ante anomalias",
            "Implementar trazas de AWS X-Ray para agregar latencia y errores, exportar las metricas de ventas a una tabla de Amazon DynamoDB y disparar una regla de EventBridge que ejecute una maquina de estados de Step Functions para unificar la observabilidad",
            "Desplegar Amazon Managed Grafana para dashboards unificados que combinen CloudWatch con metricas externas, y crear alertas de Grafana que disparen Lambdas con scripts de remediacion autonoma cuando las metricas superen umbrales estaticos",
            "Exportar todas las metricas y datos de ventas a CloudWatch Logs, entrenar y desplegar un modelo propio en SageMaker AI para detectar anomalias en los streams de logs y configurar el endpoint para disparar notificaciones de Amazon SNS",
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
        question="Un motor de recomendaciones corre en Amazon EC2; cada instancia monta un volumen Amazon EBS con cache de vectores que la app lee antes de llamar a FMs de Amazon Bedrock. La calidad se degrada de forma intermitente y el equipo no sabe si la causa es <b>latencia de I/O de EBS</b> o <b>deriva del FM</b>. Se necesita observabilidad que <b>autodescubra y monitoree EC2 y los EBS como un stack unificado</b>, detecte desviaciones con <b>patrones historicos (no umbrales estaticos)</b>, correlacione alertas en menos de 10 minutos y minimice la configuracion manual. &iquest;Que solucion cumple?",
        options=[
            "Habilitar Amazon CloudWatch Application Insights sobre el resource group con las EC2 y los EBS; definir metricas con el embedded metric format y usar su anomaly detection con ML para lineas base y alertas correlacionadas entre capas",
            "Habilitar Amazon CloudWatch Container Insights en las instancias EC2 para recolectar CPU, memoria e I/O de disco a nivel de instancia y poner alarmas con umbrales estaticos de latencia cuando la lectura de EBS exceda un limite definido",
            "Desplegar AWS X-Ray en los procesos de EC2, enrutar los segmentos de traza a Amazon Data Firehose y a Amazon QuickSight y construir dashboards con reglas de alerta a mano para la latencia de EBS y los tiempos de respuesta del FM",
            "Provisionar un cluster de Amazon OpenSearch Service con el plugin de Observability, ingerir metricas de EC2 y EBS y logs de Bedrock con Firehose y escribir detectores de anomalias y reglas de alerta propios en OpenSearch",
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
        question="Un chatbot de soporte usa Amazon Lex (NLU) y Amazon Transcribe (voz a texto). Ahora la empresa quiere <b>automatizar respuestas recuperando</b> informacion de su gran biblioteca de documentacion (manuales, FAQs, articulos) de forma rapida y precisa, integrandose con las herramientas AWS existentes en tiempo real y <b>con el menor esfuerzo de desarrollo</b> (sin entrenar modelos propios). &iquest;Que enfoque cumple?",
        options=[
            "Usar Amazon Kendra para indexar los documentos de la empresa e integrarlo con el chatbot mediante la Kendra Query API para generar respuestas dinamicas",
            "Almacenar la documentacion en una Amazon Bedrock Knowledge Base y usar Amazon Comprehend para analizar las consultas y extraer los insights relevantes de la documentacion",
            "Entrenar un modelo BiDAF con las preguntas de clientes y la documentacion, desplegarlo en Amazon SageMaker AI e integrarlo por la API InvokeEndpoint de SageMaker Runtime",
            "Usar un modelo basado en BERT en Amazon SageMaker AI, guardar la documentacion en Amazon S3 y que Lex maneje las consultas e invoque el endpoint de SageMaker para responder",
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
        question="Una organizacion de salud procesa registros medicos sensibles (historias, imagenes diagnosticas) usando Amazon Rekognition y Amazon Textract, con datos en Amazon S3. Debe garantizar que <b>solo usuarios y servicios autorizados accedan a subconjuntos especificos</b> de datos sensibles, <b>clasificar datasets con metadata</b> (informacion de salud, imagenes, facturacion), aplicar <b>control de acceso granular</b> y <b>monitorear y auditar</b> todos los accesos. &iquest;Que solucion es la mejor?",
        options=[
            "Usar AWS Lake Formation con control de acceso fino basado en LF-Tags para aplicar politicas granulares, con gobernanza integral, auditoria y cifrado para cumplimiento",
            "Implementar politicas de bucket de Amazon S3 para control de acceso a nivel de objeto sobre los datos sensibles, complementadas con AWS KMS para cifrado en reposo",
            "Configurar roles de AWS IAM y VPC endpoints para conectividad privada segura al acceder a los datos medicos, de modo que solo servicios autorizados interactuen con ellos",
            "Utilizar AWS Secrets Manager para gestionar de forma segura las API keys y credenciales, con controles de acceso para interacciones seguras con los datos sensibles",
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
