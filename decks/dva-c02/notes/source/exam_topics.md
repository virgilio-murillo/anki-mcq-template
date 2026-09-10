# DVA-C02 examen_practica.txt - Temas, trazabilidad y estado

Pipeline: parse 65 preguntas -> extraccion de temas (Bedrock Claude Sonnet 4.5) -> dedup en 2 capas (embeddings Titan v2 + juicio Claude) contra las 188 tarjetas existentes de DVA-C02::* -> consolidacion de temas NEW entre si -> generacion de tarjetas para el deck DVA-C02::09.

- Temas extraidos: 65
- YA ESTUDIADOS (COVERED): 26
- NUEVOS (NEW): 39
- Tarjetas creadas en DVA-C02::09 (tras consolidar): 32

Leyenda: cada tema muestra [id] nombre (servicio), su estado, y para los NEW la tarjeta del deck 09 (card_key) donde quedo.

## Pregunta 1
- **[t001] DynamoDB Streams como fuente de eventos para Lambda** (DynamoDB) - _NUEVO_ (cos=0.505, LLM=NEW)
  - DynamoDB Streams captura cambios en tablas en tiempo real y puede invocar funciones Lambda automáticamente, permitiendo arquitecturas event-driven sin polling manual.
  - -> tarjeta deck09: `dva09-4fbdba59` (tema canonico: DynamoDB Streams como fuente de eventos para Lambda)

## Pregunta 2
- **[t002] Arquitecturas serverless event-driven con SNS y Lambda** (SNS, Lambda) - _NUEVO_ (cos=0.501, LLM=NEW)
  - SNS puede publicar eventos a funciones Lambda suscritas, creando una arquitectura serverless event-driven. Lambda se invoca automáticamente cuando SNS publica mensajes, sin necesidad de polling ni infraestructura de servidores.
  - -> tarjeta deck09: `dva09-0c7c0a0b` (tema canonico: Arquitecturas serverless event-driven con SNS y Lambda)

## Pregunta 3
- **[t003] Global Secondary Index (GSI) en DynamoDB** (DynamoDB) - _YA ESTUDIADO_ (cos=0.69, LLM=COVERED)
  - Los GSI permiten consultar datos usando claves alternativas (diferentes a la partition/sort key de la tabla base). Se pueden crear después de que la tabla existe y son esenciales para patrones de acceso eficientes como leaderboards ordenados por atributos no-clave.
  - Motivo: El concepto central de GSI (claves alternativas distintas a la tabla base) ya está cubierto; los conceptos [1-8] colectivamente enseñan qué es un GSI, sus diferencias con LSI, cuándo crearlo, y sus características de consulta, suficiente para razonar casos de uso como leaderboards.

## Pregunta 4
- **[t004] Modelos de consistencia de lectura en DynamoDB** (DynamoDB) - _YA ESTUDIADO_ (cos=0.783, LLM=COVERED)
  - Eventually consistent reads consumen la mitad de RCUs que strongly consistent reads. Usar eventually consistent cuando la aplicación tolera datos ligeramente desactualizados optimiza costos.
  - Motivo: El concepto central (eventually consistent consume mitad de RCUs que strongly consistent) ya está cubierto; la mención de optimización de costos es aplicación directa del mismo principio.

## Pregunta 5
- **[t005] Cognito Sync para sincronización de datos de usuario entre dispositivos** (Cognito) - _YA ESTUDIADO_ (cos=0.768, LLM=COVERED)
  - Cognito Sync permite sincronizar datos de perfil de usuario y preferencias de aplicación entre múltiples dispositivos y plataformas (móvil, web) para el mismo usuario autenticado.
  - Motivo: El concepto [1] ya enseña explícitamente que Cognito Sync sincroniza datos de un solo usuario entre dispositivos, cubriendo el mismo objetivo examinable central.

## Pregunta 6
- **[t006] Configuración de proveedores de identidad social en Cognito User Pools** (Cognito) - _NUEVO_ (cos=0.558, LLM=NEW)
  - Para integrar proveedores de identidad social (Google, Facebook, etc.) basados en OpenID en Cognito User Pools, se requiere registrar la aplicación con el proveedor social y obtener un App Client ID y App Client Secret, que se configuran en el user pool para establecer la federación de identidades.
  - -> tarjeta deck09: `dva09-1a0aee4b` (tema canonico: Configuración de proveedores de identidad social en Cognito User Pools)

## Pregunta 7
- **[t007] Optimización de tiempos de build en CodeBuild mediante imágenes personalizadas** (CodeBuild) - _NUEVO_ (cos=0.282, LLM=NEW)
  - Las imágenes Docker personalizadas con dependencias pre-instaladas eliminan el tiempo de descarga e instalación en cada build, siendo más eficiente que descargar paquetes desde VPC, S3 o internet en cada ejecución.
  - -> tarjeta deck09: `dva09-e2a6d52c` (tema canonico: Optimización de tiempos de build en CodeBuild mediante imágenes personalizadas)

## Pregunta 8
- **[t008] Dead-letter queues (DLQ) en SNS** (SNS) - _NUEVO_ (cos=0.245, LLM=NEW)
  - Configurar una cola SQS como DLQ para una suscripción SNS permite almacenar mensajes que fallan en su entrega, evitando pérdida de datos críticos durante interrupciones prolongadas.
  - -> tarjeta deck09: `dva09-10613d68` (tema canonico: Dead-Letter Queues (DLQ) con SQS)

## Pregunta 9
- **[t009] Roles de ejecución de Lambda y permisos IAM** (Lambda) - _NUEVO_ (cos=0.485, LLM=NEW)
  - Las funciones Lambda requieren un rol de ejecución con permisos IAM explícitos para acceder a otros servicios AWS. Un error AccessDenied indica falta de permisos en el rol, no problemas de capacidad o throttling.
  - -> tarjeta deck09: `dva09-4af54018` (tema canonico: Roles de ejecución de Lambda y permisos IAM)

## Pregunta 10
- **[t010] Políticas de despliegue en Elastic Beanstalk** (Elastic Beanstalk) - _NUEVO_ (cos=0.525, LLM=NEW)
  - Comprender las diferencias entre las políticas de despliegue (immutable, blue/green, rolling, all-at-once) y cuáles lanzan instancias nuevas versus desplegar en instancias existentes.
  - -> tarjeta deck09: `dva09-879a0d56` (tema canonico: Políticas de despliegue en Elastic Beanstalk)

## Pregunta 11
- **[t011] Integración de certificados SSL/TLS de ACM con Application Load Balancer** (Certificate Manager) - _NUEVO_ (cos=0.53, LLM=NEW)
  - Los certificados X.509 emitidos por ACM se configuran directamente en el ALB (no en instancias EC2 individuales) y no pueden exportarse. ACM gestiona automáticamente la renovación cuando se integra con servicios compatibles como ALB.
  - -> tarjeta deck09: `dva09-9b08f2e9` (tema canonico: Integración de certificados SSL/TLS de ACM con Application Load Balancer)

## Pregunta 12
- **[t012] Secrets Manager para rotación automática de credenciales** (Secrets Manager) - _NUEVO_ (cos=0.439, LLM=NEW)
  - Secrets Manager permite almacenar credenciales cifradas con KMS y rotarlas automáticamente, a diferencia de Parameter Store que no soporta rotación automática de secretos.
  - -> tarjeta deck09: `dva09-303491a1` (tema canonico: Secrets Manager para rotación automática de credenciales)

## Pregunta 13
- **[t013] Compatibilidad entre AWS Encryption SDK y S3 encryption client** (Encryption SDK) - _NUEVO_ (cos=0.557, LLM=NEW)
  - El AWS Encryption SDK y el S3 encryption client no son compatibles entre sí porque producen formatos de cifrado diferentes. Para cifrar y descifrar datos correctamente, ambas operaciones deben usar la misma herramienta (ambas con Encryption SDK o ambas con S3 encryption client).
  - -> tarjeta deck09: `dva09-61baa595` (tema canonico: Compatibilidad entre AWS Encryption SDK y S3 encryption client)

## Pregunta 14
- **[t014] Requisitos de sincronización de tiempo para operaciones de CodeDeploy** (CodeDeploy) - _NUEVO_ (cos=0.388, LLM=NEW)
  - CodeDeploy requiere que la hora del sistema en las instancias EC2 esté sincronizada correctamente para validar las firmas de las solicitudes de despliegue. Errores de 'Signature expired' indican desincronización temporal entre la instancia y el servicio.
  - -> tarjeta deck09: `dva09-302e5592` (tema canonico: Requisitos de sincronización de tiempo para operaciones de CodeDeploy)

## Pregunta 15
- **[t015] Recopilación centralizada de logs desde múltiples fuentes con CloudWatch Agent** (CloudWatch) - _YA ESTUDIADO_ (cos=0.49, LLM=COVERED)
  - El agente de CloudWatch permite recopilar logs tanto de instancias EC2 como de servidores on-premises y enviarlos a CloudWatch Logs para almacenamiento durable y visualización, sin necesidad de reescribir la aplicación.
  - Motivo: El concepto [2] ya enseña que CloudWatch Agent envía logs (PutLogEvents) desde instancias, cubriendo el mecanismo central de recopilación; que funcione también on-premises es extensión del mismo agente, no un objetivo examinable distinto.

## Pregunta 16
- **[t016] DynamoDB Streams con Lambda para procesamiento en tiempo real** (DynamoDB Streams) - _NUEVO_ (cos=0.518, LLM=NEW)
  - DynamoDB Streams captura cambios en tablas y permite invocar funciones Lambda automáticamente ante modificaciones, habilitando arquitecturas event-driven serverless sin modificar la aplicación origen.
  - -> tarjeta deck09: `dva09-4fbdba59` (tema canonico: DynamoDB Streams como fuente de eventos para Lambda)

## Pregunta 17
- **[t017] Control de acceso basado en atributos (ABAC) con Cognito Identity Pools** (Cognito) - _NUEVO_ (cos=0.55, LLM=NEW)
  - Configurar un único rol IAM en el identity pool con políticas que usen condiciones de tags principales (${aws:PrincipalTag/}) para controlar acceso a recursos según atributos del usuario, permitiendo permisos dinámicos sin crear múltiples roles por departamento.
  - -> tarjeta deck09: `dva09-a26e79a4` (tema canonico: Control de acceso basado en atributos (ABAC) con Cognito Identity Pools)

## Pregunta 18
- **[t018] Optimización de latencia en funciones Lambda con conexiones a bases de datos** (Lambda) - _NUEVO_ (cos=0.544, LLM=NEW)
  - Usar provisioned concurrency para pre-inicializar conexiones y mover la inicialización de clientes SDK y conexiones de base de datos fuera del handler de la función para reducir cold starts y latencia de integración.
  - -> tarjeta deck09: `dva09-2a46aa39` (tema canonico: Optimización de latencia en funciones Lambda con conexiones a bases de datos)

## Pregunta 19
- **[t019] Configuración de Availability Zones en Application Load Balancer** (Application Load Balancer) - _NUEVO_ (cos=0.413, LLM=NEW)
  - Un ALB solo enruta tráfico a instancias en Availability Zones habilitadas. Si las instancias están registradas pero no reciben tráfico, el problema típico es que sus AZs no están habilitadas en el ALB.
  - -> tarjeta deck09: `dva09-f61f7b1c` (tema canonico: Configuración de Availability Zones en Application Load Balancer)

## Pregunta 20
- **[t020] Cognito Identity Pools - Flujo de autenticación federada con proveedores de identidad externos** (Cognito) - _NUEVO_ (cos=0.775, LLM=NEW)
  - Para obtener credenciales AWS temporales usando un token OpenID de un proveedor externo, se debe usar Cognito Identity Pool con el flujo simplificado: primero llamar GetId (con el token OpenID para obtener un Cognito ID) y luego GetCredentialsForIdentity (con el Cognito ID para obtener credenciales AWS temporales).
  - -> tarjeta deck09: `dva09-e470b12f` (tema canonico: Cognito Identity Pools - Flujo de autenticación federada para credenciales AWS temporales)

## Pregunta 21
- **[t021] Paquetes de despliegue de Lambda** (Lambda) - _NUEVO_ (cos=0.463, LLM=NEW)
  - Un deployment package de Lambda debe incluir el código compilado y las dependencias de la aplicación, pero NO el runtime (provisto por Lambda), ni el execution role (configurado externamente), ni las referencias a event sources (externas a la función).
  - -> tarjeta deck09: `dva09-b9f08ce9` (tema canonico: Paquetes de despliegue de Lambda)

## Pregunta 22
- **[t022] Secrets Manager para gestión y rotación automática de credenciales** (Secrets Manager) - _NUEVO_ (cos=0.392, LLM=NEW)
  - Secrets Manager almacena credenciales de bases de datos de forma segura y permite rotación automática programada, a diferencia de Parameter Store que no soporta rotación automática ni KMS que solo cifra pero no almacena/distribuye credenciales.
  - -> tarjeta deck09: `dva09-303491a1` (tema canonico: Secrets Manager para rotación automática de credenciales)

## Pregunta 23
- **[t023] Cifrado de CloudWatch Logs con claves KMS administradas por el cliente** (CloudWatch Logs) - _NUEVO_ (cos=0.487, LLM=NEW)
  - Para cifrar log groups de CloudWatch Logs con una clave KMS customer managed key, se debe usar AWS CLI (comandos associate-kms-key o create-log-group), no la consola. La clave KMS debe ser simétrica.
  - -> tarjeta deck09: `dva09-d10caea5` (tema canonico: Cifrado de CloudWatch Logs con claves KMS administradas por el cliente)

## Pregunta 24
- **[t024] Decodificación de mensajes de error de autorización con STS** (STS) - _YA ESTUDIADO_ (cos=0.888, LLM=COVERED)
  - Cuando una operación AWS falla con un mensaje de autorización codificado (UnauthorizedOperation), se debe usar el comando 'decode-authorization-message' de STS para decodificar el mensaje y obtener detalles adicionales sobre el fallo de autorización.
  - Motivo: El concepto [1] ya enseña exactamente el mismo objetivo examinable: usar DecodeAuthorizationMessage de STS para decodificar errores UnauthorizedOperation y obtener detalles de fallos de autorización IAM.

## Pregunta 25
- **[t025] Distributed tracing con X-Ray en arquitecturas de microservicios** (X-Ray) - _YA ESTUDIADO_ (cos=0.65, LLM=COVERED)
  - X-Ray proporciona capacidades de distributed tracing para rastrear requests a través de múltiples servicios y identificar cuellos de botella. Requiere ejecutar el daemon de X-Ray como contenedor sidecar en ECS para recopilar datos de trazabilidad.
  - Motivo: El concepto central de X-Ray daemon recolectando segment documents ya está cubierto; el detalle específico del sidecar en ECS es solo una variante de deployment del mismo mecanismo de tracing distribuido.

## Pregunta 26
- **[t026] Modos de capacidad de DynamoDB (provisioned vs on-demand)** (DynamoDB) - _YA ESTUDIADO_ (cos=0.548, LLM=COVERED)
  - On-demand mode escala automáticamente para manejar cargas de trabajo impredecibles y picos de tráfico sin errores de ProvisionedThroughputExceededException, mientras que provisioned capacity requiere configuración manual o Auto Scaling que puede no responder suficientemente rápido a picos repentinos.
  - Motivo: Application Auto Scaling ya cubre el escalado automático de DynamoDB RCU/WCU; on-demand es simplemente el modo nativo que elimina la necesidad de Auto Scaling, pero el objetivo examinable (escalado automático vs manual en DynamoDB) ya está cubierto.

## Pregunta 27
- **[t027] Autenticación y autorización de usuarios a escala con Cognito** (Cognito) - _YA ESTUDIADO_ (cos=0.719, LLM=COVERED)
  - Cognito proporciona identidades únicas para usuarios a gran escala y genera credenciales temporales de IAM para acceder a servicios AWS como DynamoDB, sin necesidad de crear usuarios IAM individuales.
  - Motivo: El concepto central de Identity Pool entregando credenciales AWS temporales para acceso a servicios sin usuarios IAM individuales ya está cubierto; este tema solo enfatiza la escala y el caso de uso DynamoDB.

## Pregunta 28
- **[t028] S3 Event Notifications para invocar Lambda** (S3) - _YA ESTUDIADO_ (cos=0.749, LLM=COVERED)
  - S3 Event Notifications permite invocar funciones Lambda automáticamente en respuesta a eventos del bucket (PUT, DELETE, etc.), habilitando arquitecturas event-driven para procesamiento de objetos.
  - Motivo: El concepto [1] ya enseña explícitamente que S3 Event Notification triggers on write/state-change events (PUT, DELETE), cubriendo el mismo objetivo examinable de cuándo y cómo S3 invoca Lambda automáticamente.

## Pregunta 29
- **[t029] Optimización de throughput en Kinesis Data Streams usando PutRecords para batch processing** (Kinesis Data Streams) - _YA ESTUDIADO_ (cos=0.678, LLM=COVERED)
  - PutRecords permite enviar múltiples registros en una sola llamada API, reduciendo significativamente el uso de CPU y red comparado con múltiples llamadas individuales de PutRecord. Es la forma recomendada de optimizar la ingesta de datos en productores.
  - Motivo: El concepto [1] ya cubre la distinción entre PutRecord y PutRecords para batch processing en Kinesis Data Streams, que es el objetivo examinable central aquí.

## Pregunta 30
- **[t030] Trust policy vs access policy en roles IAM para Cognito Identity Pools** (IAM) - _NUEVO_ (cos=0.489, LLM=NEW)
  - La trust policy controla QUIÉN puede asumir el rol (sts:AssumeRoleWithWebIdentity). La access policy controla QUÉ puede hacer después de asumirlo. Errores en trust policy impiden asumir el rol; errores en access policy ocurren al usar credenciales ya asumidas.
  - -> tarjeta deck09: `dva09-68ee6010` (tema canonico: Trust policy vs access policy en roles IAM para Cognito Identity Pools)

## Pregunta 31
- **[t031] Ubicación de archivos de configuración buildspec.yml y appspec.yml** (CodeBuild, CodeDeploy) - _NUEVO_ (cos=0.41, LLM=NEW)
  - Los archivos buildspec.yml (CodeBuild) y appspec.yml (CodeDeploy) deben ubicarse en el directorio raíz del repositorio de código fuente por defecto, no en subdirectorios.
  - -> tarjeta deck09: `dva09-bc3c8a7b` (tema canonico: Ubicación de archivos de configuración buildspec.yml y appspec.yml)

## Pregunta 32
- **[t032] DynamoDB Global Secondary Indexes** (DynamoDB) - _YA ESTUDIADO_ (cos=0.705, LLM=COVERED)
  - Los GSI permiten consultas eficientes usando claves alternativas (partition key y sort key diferentes a la tabla base). Se crean sobre la tabla base y se sincronizan automáticamente; no se pueden insertar items directamente en el índice.
  - Motivo: El concepto central de GSI (claves alternativas diferentes a la tabla base) ya está cubierto; los conceptos 2, 3, 4, 6, 7 y 8 ya enseñan las características fundamentales de GSI que permitirían razonar sobre consultas eficientes con claves alternativas.

## Pregunta 33
- **[t033] Secciones de plantillas CloudFormation** (CloudFormation) - _NUEVO_ (cos=0.377, LLM=NEW)
  - Comprender el propósito de cada sección de una plantilla CloudFormation, especialmente Mappings para definir valores condicionales basados en claves como regiones, y distinguirlas de Parameters, Resources y Outputs.
  - -> tarjeta deck09: `dva09-586a57c8` (tema canonico: Secciones de plantillas CloudFormation)

## Pregunta 34
- **[t034] Manejo de duplicados en SQS con visibility timeout y deduplicación a nivel de aplicación** (SQS) - _NUEVO_ (cos=0.357, LLM=NEW)
  - SQS garantiza entrega at-least-once, lo que puede causar duplicados. Se previenen aumentando el visibility timeout para que exceda el tiempo de procesamiento completo y/o implementando lógica de deduplicación en la aplicación antes de escribir a la base de datos.
  - -> tarjeta deck09: `dva09-2d4efbd2` (tema canonico: Manejo de duplicados en SQS con visibility timeout y deduplicación a nivel de aplicación)

## Pregunta 35
- **[t035] Lambda Layers para compartir dependencias** (Lambda) - _NUEVO_ (cos=0.468, LLM=NEW)
  - Lambda Layers permite empaquetar y compartir código común (librerías, dependencias) entre múltiples funciones Lambda de forma centralizada, evitando duplicación y facilitando actualizaciones sin modificar cada función individualmente.
  - -> tarjeta deck09: `dva09-d4712472` (tema canonico: Lambda Layers para compartir dependencias)

## Pregunta 36
- **[t036] Políticas de bucket de S3 para forzar cifrado en tránsito** (S3) - _NUEVO_ (cos=0.549, LLM=NEW)
  - Usar la condición 'aws:SecureTransport': 'false' con efecto 'Deny' para bloquear conexiones HTTP no cifradas y forzar HTTPS en todas las solicitudes al bucket, independientemente de otras políticas existentes.
  - -> tarjeta deck09: `dva09-921bc16b` (tema canonico: Políticas de bucket de S3 para forzar cifrado en tránsito)

## Pregunta 37
- **[t037] API Gateway caching** (API Gateway) - _NUEVO_ (cos=0.564, LLM=NEW)
  - Habilitar el caché en API Gateway reduce el tráfico al endpoint backend almacenando respuestas y sirviéndolas directamente desde el gateway, mejorando el rendimiento sin escalar la infraestructura subyacente.
  - -> tarjeta deck09: `dva09-4e81de94` (tema canonico: API Gateway caching)

## Pregunta 38
- **[t038] Estrategias de caching en CodeBuild para optimizar tiempos de build** (CodeBuild) - _NUEVO_ (cos=0.374, LLM=NEW)
  - Entender las diferencias entre local caching (almacena en el host de build, ideal para archivos grandes y builds frecuentes) vs S3 caching (almacena en bucket S3, más lento para transferir archivos grandes) y cómo configurar rutas de cache en buildspec.
  - -> tarjeta deck09: `dva09-7e41b8d8` (tema canonico: Estrategias de caching en CodeBuild para optimizar tiempos de build)

## Pregunta 39
- **[t039] Cálculo de capacidad provisionada (RCU y WCU) en DynamoDB** (DynamoDB) - _YA ESTUDIADO_ (cos=0.724, LLM=COVERED)
  - Calcular RCU considerando el tamaño del ítem (múltiplos de 4 KB), tipo de consistencia (eventually consistent usa 50% de RCU) y operaciones por segundo. Calcular WCU basándose en múltiplos de 1 KB por ítem y escrituras por segundo.
  - Motivo: El concepto [3] ya enseña el cálculo completo de RCU incluyendo redondeo a múltiplos de 4KB, división entre 2 para eventually consistent, y multiplicación por operaciones/segundo; los conceptos [2] y [5] cubren WCU con bloques de 1KB.

## Pregunta 40
- **[t040] Garantías de entrega en SQS: Standard vs FIFO queues** (SQS) - _NUEVO_ (cos=0.317, LLM=NEW)
  - Las colas SQS Standard ofrecen entrega 'at-least-once' (pueden duplicar mensajes), mientras que las colas FIFO garantizan procesamiento 'exactly-once'. No se puede cambiar el tipo de cola después de crearla; se debe crear una nueva cola FIFO.
  - -> tarjeta deck09: `dva09-7943aa9f` (tema canonico: Garantías de entrega en SQS: Standard vs FIFO queues)

## Pregunta 41
- **[t041] AWS SAM para desarrollo y despliegue de aplicaciones serverless** (SAM) - _YA ESTUDIADO_ (cos=0.658, LLM=COVERED)
  - SAM permite empaquetar y desplegar aplicaciones serverless completas (Lambda + DynamoDB) como una unidad, y ejecutar pruebas locales mediante SAM CLI, a diferencia de otras herramientas de despliegue que no ofrecen testing local.
  - Motivo: SAM CLI ya cubre las capacidades de testing local y despliegue completo de aplicaciones serverless; el concepto central de SAM como herramienta integral ya está enseñado.

## Pregunta 42
- **[t042] Multipart upload en S3** (S3) - _YA ESTUDIADO_ (cos=0.769, LLM=COVERED)
  - Para archivos grandes que exceden el límite de 5GB de PUT simple, se debe usar multipart upload que permite subir objetos hasta 5TB dividiéndolos en partes.
  - Motivo: El concepto [1] ya cubre que AWS CLI usa multipart upload automáticamente para archivos grandes, enseñando el mismo mecanismo central de subida en partes para objetos grandes en S3.

## Pregunta 43
- **[t043] Offloading de contenido estático a S3 para reducir carga en instancias EC2** (S3) - _YA ESTUDIADO_ (cos=0.555, LLM=COVERED)
  - S3 puede servir contenido estático (HTML, CSS, JS, imágenes) directamente a clientes sin pasar por servidores web, reduciendo la carga computacional y de red en las instancias EC2 de la aplicación.
  - Motivo: El concepto central de usar S3 para servir contenido estático (reduciendo carga en compute) ya está cubierto en la tarjeta sobre CloudFront origin selection que explica que S3 es el origen optimizado para contenido estático versus EC2 para dinámico.

## Pregunta 44
- **[t044] Cifrado del lado del cliente (client-side encryption) en S3** (S3) - _YA ESTUDIADO_ (cos=0.624, LLM=COVERED)
  - El cifrado client-side permite usar claves asimétricas gestionadas por el cliente para cifrar datos antes de subirlos a S3, mientras que las opciones server-side (SSE-C, SSE-S3, SSE-KMS) solo soportan claves simétricas.
  - Motivo: El concepto [1] ya enseña que client-side encryption permite claves gestionadas por el cliente (vs SSE-C que son customer-provided), cubriendo el objetivo examinable de distinguir opciones de cifrado según gestión de claves.

## Pregunta 45
- **[t045] Ejecución paralela de acciones dentro de un stage en CodePipeline** (CodePipeline) - _NUEVO_ (cos=0.407, LLM=NEW)
  - Las acciones dentro de un mismo stage de CodePipeline pueden ejecutarse en paralelo, mientras que los stages se ejecutan secuencialmente. Para paralelizar tareas (como tests), se deben configurar múltiples acciones paralelas dentro del mismo stage.
  - -> tarjeta deck09: `dva09-a17f9dc4` (tema canonico: Ejecución paralela de acciones dentro de un stage en CodePipeline)

## Pregunta 46
- **[t046] Programación de tareas periódicas con EventBridge y Lambda** (EventBridge) - _NUEVO_ (cos=0.456, LLM=NEW)
  - EventBridge permite invocar funciones Lambda en horarios programados (cron/rate expressions). Lambda con conectividad VPC puede acceder a recursos privados como instancias EC2 para ejecutar scripts personalizados de forma serverless.
  - -> tarjeta deck09: `dva09-0321f18d` (tema canonico: Programación de tareas periódicas con EventBridge y Lambda)

## Pregunta 47
- **[t047] Canary deployments en API Gateway con versiones de Lambda** (API Gateway) - _NUEVO_ (cos=0.442, LLM=NEW)
  - Usar canary releases en un stage de API Gateway para dirigir un porcentaje del tráfico a una nueva versión de función Lambda ($LATEST) mientras se mantiene la versión estable anterior, permitiendo pruebas graduales en producción sin cambiar la URL del API.
  - -> tarjeta deck09: `dva09-3b210dc3` (tema canonico: Canary deployments en API Gateway con versiones de Lambda)

## Pregunta 48
- **[t048] Permisos de ejecución de Lambda para escribir logs en CloudWatch Logs** (Lambda) - _YA ESTUDIADO_ (cos=0.525, LLM=COVERED)
  - Las funciones Lambda requieren permisos explícitos en su rol de ejecución (logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents) para que los logs generados automáticamente se escriban en CloudWatch Logs.
  - Motivo: Ambos enseñan el mismo objetivo: un servicio AWS (CloudWatch Agent/Lambda) requiere permisos IAM explícitos (PutLogEvents incluido) para escribir logs en CloudWatch Logs.

## Pregunta 49
- **[t049] Cognito Identity Pools para acceso no autenticado** (Cognito) - _YA ESTUDIADO_ (cos=0.85, LLM=COVERED)
  - Usar Cognito Identity Pools para otorgar credenciales temporales a usuarios no autenticados que necesitan acceder a servicios AWS desde aplicaciones cliente (browser/mobile), evitando exponer credenciales permanentes en el código.
  - Motivo: El concepto [1] ya enseña que Identity Pool entrega credenciales temporales AWS y permite acceso unauthenticated, cubriendo el mismo objetivo examinable de acceso no autenticado sin exponer credenciales permanentes.

## Pregunta 50
- **[t050] Archivos de configuración .ebextensions en Elastic Beanstalk** (Elastic Beanstalk) - _NUEVO_ (cos=0.433, LLM=NEW)
  - Los archivos de configuración en el directorio .ebextensions deben tener extensión .config (no .yaml, .yml u otra) para que Elastic Beanstalk los procese correctamente durante el despliegue de la aplicación.
  - -> tarjeta deck09: `dva09-b0f28e7b` (tema canonico: Archivos de configuración .ebextensions en Elastic Beanstalk)

## Pregunta 51
- **[t051] Stage variables en API Gateway** (API Gateway) - _NUEVO_ (cos=0.625, LLM=NEW)
  - Las stage variables permiten parametrizar configuraciones entre stages (dev/prod) y pueden usarse en integration requests para referenciar dinámicamente aliases o versiones de Lambda mediante la sintaxis ${stageVariables.NOMBRE}.
  - -> tarjeta deck09: `dva09-9dd7d9cf` (tema canonico: Stage variables en API Gateway)

## Pregunta 52
- **[t052] Dead-Letter Queues en Lambda** (Lambda) - _NUEVO_ (cos=0.286, LLM=NEW)
  - Configurar una cola SQS como dead-letter queue (DLQ) para almacenar de forma duradera eventos que Lambda no puede procesar exitosamente, usando la propiedad DeadLetterConfig con el ARN de la cola SQS.
  - -> tarjeta deck09: `dva09-10613d68` (tema canonico: Dead-Letter Queues (DLQ) con SQS)

## Pregunta 53
- **[t053] IAM Roles para EC2** (IAM) - _YA ESTUDIADO_ (cos=0.705, LLM=COVERED)
  - Las aplicaciones en instancias EC2 deben usar roles de IAM (credenciales temporales) en lugar de credenciales permanentes para acceder a servicios de AWS como DynamoDB de forma segura.
  - Motivo: El concepto central (EC2 usa IAM roles para credenciales temporales en lugar de permanentes) ya está cubierto por la tarjeta [1] que enseña exactamente ese mecanismo de seguridad.

## Pregunta 54
- **[t054] Rotación automática de secretos con Secrets Manager** (Secrets Manager) - _NUEVO_ (cos=0.381, LLM=NEW)
  - Secrets Manager proporciona rotación automática de secretos mediante plantillas de Lambda, cifrado por defecto y gestión programada de credenciales, eliminando la necesidad de implementar manualmente la lógica de rotación con EventBridge o código personalizado.
  - -> tarjeta deck09: `dva09-303491a1` (tema canonico: Secrets Manager para rotación automática de credenciales)

## Pregunta 55
- **[t055] Políticas de despliegue en Elastic Beanstalk** (Elastic Beanstalk) - _NUEVO_ (cos=0.598, LLM=NEW)
  - Comprender las diferentes estrategias de despliegue (all-at-once, rolling, rolling with additional batch, blue/green) y cuándo usar blue/green deployment para cutover completo con capacidad de rollback y mínimo downtime.

## Pregunta 56
- **[t056] DynamoDB Streams - Configuración de tipos de eventos para proteger datos sensibles** (DynamoDB) - _NUEVO_ (cos=0.504, LLM=NEW)
  - Comprender los diferentes tipos de eventos de DynamoDB Streams (KEYS_ONLY, NEW_IMAGE, OLD_IMAGE, NEW_AND_OLD_IMAGES) y cómo KEYS_ONLY registra solo claves de partición/ordenamiento sin exponer atributos con PII, mientras que NEW_IMAGE expone todos los datos del item.

## Pregunta 57
- **[t057] Acciones de aprobación manual en CodePipeline** (CodePipeline) - _YA ESTUDIADO_ (cos=0.669, LLM=COVERED)
  - CodePipeline soporta acciones de aprobación (approval actions) como tipo de acción nativa dentro de un stage, permitiendo pausar el pipeline para revisión manual antes de continuar con el despliegue.
  - Motivo: El concepto [1] ya enseña que CodePipeline soporta aprobación manual con notificación SNS para pausar y revisar antes de continuar, cubriendo el mismo objetivo examinable de acciones de aprobación nativas en el pipeline.

## Pregunta 58
- **[t058] Gestión de capacidad de throughput en DynamoDB** (DynamoDB) - _YA ESTUDIADO_ (cos=0.643, LLM=COVERED)
  - Identificar y resolver errores de ProvisionedThroughputExceededException causados por insuficientes Write Capacity Units (WCU) o Read Capacity Units (RCU) provisionadas para la tabla o sus índices secundarios globales.
  - Motivo: El concepto central de ProvisionedThroughputExceededException por WCU/RCU insuficientes ya está cubierto en [1] y [2] que explican throttling por capacidad insuficiente en tabla/GSI, el mismo mecanismo examinable.

## Pregunta 59
- **[t059] Step Functions para orquestación de reintentos con Lambda** (Step Functions) - _YA ESTUDIADO_ (cos=0.494, LLM=COVERED)
  - Step Functions permite orquestar funciones Lambda con lógica de reintentos que excede el timeout máximo de Lambda (15 minutos), usando máquinas de estado con configuración de BackoffRate y maxAttempts para manejar fallos de forma asíncrona y duradera.
  - Motivo: El concepto [1] ya enseña Retry con BackoffRate y maxAttempts en Step Functions para manejar reintentos; el tema actual solo contextualiza su uso para superar el timeout de Lambda, pero el mecanismo examinable central ya está cubierto.

## Pregunta 60
- **[t060] Trazabilidad y análisis de latencia end-to-end con X-Ray** (X-Ray) - _YA ESTUDIADO_ (cos=0.567, LLM=COVERED)
  - X-Ray permite rastrear solicitudes a través de servicios distribuidos (API Gateway, Lambda, DynamoDB) para identificar cuellos de botella de rendimiento y analizar latencia de extremo a extremo mediante trazas visuales.
  - Motivo: El concepto central de X-Ray para rastrear solicitudes distribuidas mediante segments/subsegments ya está cubierto; la trazabilidad end-to-end y análisis de latencia es el objetivo examinable que esas tarjetas ya enseñan.

## Pregunta 61
- **[t061] Server-Side Encryption con claves proporcionadas por el cliente (SSE-C) en S3** (S3) - _NUEVO_ (cos=0.723, LLM=NEW)
  - Para descifrar objetos encriptados con SSE-C, el cliente debe proporcionar la misma clave de encriptación utilizada originalmente en cada operación (GetObject, PutObject). S3 no almacena las claves del cliente, solo un HMAC salado para validación.
  - -> tarjeta deck09: `dva09-117f2eb9` (tema canonico: Server-Side Encryption con claves proporcionadas por el cliente (SSE-C) en S3)

## Pregunta 62
- **[t062] Políticas de despliegue en Elastic Beanstalk** (Elastic Beanstalk) - _NUEVO_ (cos=0.468, LLM=NEW)
  - Comprender las diferencias entre políticas de despliegue (Rolling, All at once, Immutable, Rolling with additional batch) en términos de uso de instancias existentes vs nuevas y tiempo de inactividad.

## Pregunta 63
- **[t063] Configuración de memoria y CPU en Lambda** (Lambda) - _YA ESTUDIADO_ (cos=0.615, LLM=COVERED)
  - En Lambda, aumentar la memoria asignada también incrementa proporcionalmente la CPU disponible para la función, lo que reduce el tiempo de ejecución de cargas intensivas de CPU.
  - Motivo: El concepto central de que memoria escala CPU proporcionalmente en Lambda ya está cubierto; esta pregunta solo prueba la consecuencia práctica (reducción de tiempo de ejecución) del mismo mecanismo.

## Pregunta 64
- **[t064] X-Ray para tracing y análisis de performance de funciones Lambda** (X-Ray) - _YA ESTUDIADO_ (cos=0.575, LLM=COVERED)
  - X-Ray permite rastrear llamadas API (como DynamoDB) desde Lambda, identificar cuellos de botella y analizar tiempos de ejecución mediante traces distribuidos.
  - Motivo: El concepto central de X-Ray rastreando llamadas downstream (DynamoDB, APIs) desde Lambda y analizando performance ya está cubierto en [1] que explica subsegments para llamadas downstream incluyendo RDS y AWS SDK.

## Pregunta 65
- **[t065] Conditional writes en DynamoDB** (DynamoDB) - _YA ESTUDIADO_ (cos=0.781, LLM=COVERED)
  - Mecanismo para garantizar que una operación de escritura solo se ejecute si se cumplen condiciones específicas sobre los atributos actuales del item, previniendo actualizaciones concurrentes no deseadas.
  - Motivo: El concepto [1] ya enseña que conditional writes con condition expression validan condiciones antes de escribir, que es exactamente el mecanismo central examinable aquí.

