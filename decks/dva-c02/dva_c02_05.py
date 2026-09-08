#!/usr/bin/env python3
"""
DVA-C02::05 - Cards from the FIRST-SET questions the user got INCORRECT (Tutorials
Dojo). Each question decomposed into 2-3 one-concept cards, same style as ::01-04.
Source: kiro-notes/source/set1_failed.txt

Lessons applied: self-contained questions, {{L}} verdict, refute every distractor,
no distractor that collides with the taught rule, no "see next card", real AWS methods.
"""
from anki_mcq import card, create

cards = [
    # ================= Q4: CodePipeline manual approval + SNS =================
    card(
        question="En un pipeline de CodePipeline necesitas que <b>alguien apruebe</b> (revisi&oacute;n de c&oacute;digo) antes de pasar a la siguiente etapa: si aprueba, el pipeline sigue; si rechaza, se detiene. &iquest;Qu&eacute; soluci&oacute;n es la m&aacute;s adecuada?",
        options=[
            "Acci&oacute;n de aprobaci&oacute;n manual en CodePipeline que publica a un topic de SNS",
            "Acci&oacute;n de aprobaci&oacute;n manual en CodePipeline que env&iacute;a a una cola SQS",
            "Dividir el proceso en Task states de Step Functions con un Wait state para el timeout",
            "Rehacer el pipeline con AWS SAM",
        ],
        correct=0,
        key="dva05-q4-manual-approval",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; aprobaci&oacute;n manual + SNS.</div>'
            '<p>CodePipeline tiene una <b>acci&oacute;n de aprobaci&oacute;n manual</b>: el pipeline se detiene en ese punto hasta que alguien con permiso IAM apruebe o rechace. Esa acci&oacute;n puede <b>publicar a un topic de Amazon SNS</b> (mismo region que el pipeline) para notificar al revisor. Es la funci&oacute;n integrada para exactamente este caso.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>SQS:</b> la acci&oacute;n de aprobaci&oacute;n manual <b>no</b> se integra con SQS; usa SNS para notificar.</li>'
            '<li><b>Step Functions + Wait:</b> a&ntilde;ade complejidad innecesaria; la aprobaci&oacute;n manual ya viene integrada.</li>'
            '<li><b>AWS SAM:</b> es un framework para construir apps serverless, no un reemplazo del pipeline CI/CD.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato de examen</span>Si nadie aprueba/rechaza en <b>7 d&iacute;as</b> (plazo del servicio), la acci&oacute;n se trata como fallida y el pipeline no contin&uacute;a.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/approvals.html">docs.aws CodePipeline approvals</a><br>'
            '<a href="https://tutorialsdojo.com/aws-codepipeline/">tutorialsdojo CodePipeline</a></div>'
        ),
    ),
    card(
        question="En una acci&oacute;n de <b>aprobaci&oacute;n manual</b> de CodePipeline, &iquest;qu&eacute; pasa si nadie aprueba ni rechaza dentro del plazo l&iacute;mite?",
        options=[
            "Tras el plazo por defecto de 7 d&iacute;as la acci&oacute;n falla y el pipeline se detiene",
            "Al vencer el plazo la acci&oacute;n se aprueba y el pipeline pasa a la etapa siguiente",
            "El plazo se ignora y la etapa queda en curso hasta que alguien responda",
            "Se reintenta la aprobaci&oacute;n y se reenv&iacute;a la notificaci&oacute;n cada 24 horas",
        ],
        correct=0,
        key="dva05-q4-approval-timeout",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; a los 7 d&iacute;as se considera fallida.</div>'
            '<p>Una acci&oacute;n de aprobaci&oacute;n manual detiene el pipeline. Si se <b>rechaza</b>, o si <b>nadie</b> aprueba/rechaza en <b>7 d&iacute;as</b> (plazo del servicio), el resultado es el mismo que una acci&oacute;n fallida: el pipeline <b>no</b> contin&uacute;a.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no espera indefinidamente (hay l&iacute;mite de 7 d&iacute;as). No se auto-aprueba (ser&iacute;a inseguro). No se reinicia desde el inicio; simplemente se detiene como fallida.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Quien aprueba necesita permisos IAM sobre la acci&oacute;n de aprobaci&oacute;n (<code>codepipeline:PutApprovalResult</code>).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/approvals.html">docs.aws CodePipeline approvals</a></div>'
        ),
    ),

    # ================= Q7: X-Ray segment documents + daemon =================
    card(
        question="Debes trazar en X-Ray todas las peticiones de tu app, <b>incluyendo las llamadas a recursos AWS aguas abajo</b>. &iquest;Qu&eacute; acci&oacute;n implementas?",
        options=[
            "Usar el X-Ray SDK para generar segment documents con subsegments de llamadas aguas abajo y enviarlos al daemon, que los sube a la API en lotes",
            "Usar el X-Ray SDK para que llame directamente a PutTraceSegments y suba cada trace segment individual a la API de X-Ray sin pasar por el daemon",
            "Instalar y configurar el agente de X-Ray en cada servicio y recurso AWS aguas abajo que la aplicaci&oacute;n invoca para que reporten sus propios segments",
            "Usar el X-Ray SDK para agrupar en lotes varios trace segments y pasarlos como un &uacute;nico array en el par&aacute;metro TraceSegmentDocuments de PutTraceSegments",
        ],
        correct=0,
        key="dva05-q7-segment-documents",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; segment documents con subsegments, v&iacute;a el daemon.</div>'
            '<p>Un <b>segment document</b> es un JSON (hasta 64 kB) que describe el trabajo de una petici&oacute;n. Tu app registra su propio trabajo en <b>segments</b>, y el trabajo de servicios/recursos <b>aguas abajo</b> en <b>subsegments</b>. El SDK env&iacute;a estos documentos al <b>daemon de X-Ray</b>, que los almacena en b&uacute;fer y los sube a la API de X-Ray en <b>lotes</b> (as&iacute; el SDK no llama a AWS directamente).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Subir un "trace segment" v&iacute;a PutTraceSegments:</b> lo que se sube son <b>segment documents</b> (con subsegments), no un segment suelto.</li>'
            '<li><b>Instalar X-Ray en cada servicio:</b> no puedes trazar la app y los servicios por separado y esperar un &uacute;nico resultado; usas subsegments para capturar las llamadas aguas abajo.</li>'
            '<li><b>"Varios trace segments" como par&aacute;metro:</b> el par&aacute;metro es <code>TraceSegmentDocuments</code> (lista de documentos JSON), no trace segments.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato de examen</span>Alternativa directa: llamar a <code>PutTraceSegments</code> t&uacute; mismo. El daemon existe para agrupar y evitar llamadas directas a AWS.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-api-sendingdata.html">docs.aws X-Ray sending data</a><br>'
            '<a href="https://tutorialsdojo.com/aws-x-ray/">tutorialsdojo X-Ray</a></div>'
        ),
    ),
    card(
        question="En AWS X-Ray, &iquest;cu&aacute;l es la diferencia entre un <b>segment</b> y un <b>subsegment</b>?",
        options=[
            "El segment describe el trabajo local de tu propia app; el subsegment describe llamadas aguas abajo",
            "El segment describe llamadas aguas abajo; el subsegment describe el trabajo local de tu propia app",
            "El segment solo cubre peticiones HTTP entrantes; el subsegment solo cubre llamadas al AWS SDK",
            "El segment agrupa todos los segments de una request; el subsegment es una llamada a otra cuenta AWS",
        ],
        correct=0,
        key="dva05-q7-segment-vs-subsegment",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; segment = tu app; subsegment = llamadas aguas abajo.</div>'
            '<p>Un <b>segment</b> registra el trabajo que tu aplicaci&oacute;n hace por s&iacute; misma para servir una petici&oacute;n. Un <b>subsegment</b> registra el trabajo hecho al llamar a <b>servicios o recursos aguas abajo</b> (otra API, DynamoDB, etc.). Ambos van dentro del mismo segment document JSON.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no son sin&oacute;nimos (uno anida al otro). No se dividen por error/&eacute;xito. El subsegment no es "el resultado final"; es una unidad de trabajo aguas abajo.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Un segment document completo cabe en <b>64 kB</b> e incluye el segment y sus subsegments.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-api-segmentdocuments.html">docs.aws X-Ray segment documents</a></div>'
        ),
    ),

    # ================= Q11: RDS Enhanced Monitoring =================
    card(
        question="Necesitas ver c&oacute;mo los <b>procesos individuales</b> de una instancia RDS usan la CPU (porcentaje de CPU y memoria consumida <b>por cada proceso</b>). &iquest;Qu&eacute; usas?",
        options=[
            "Enhanced Monitoring de RDS, un agente en la instancia que expone m&eacute;tricas por proceso (CPU%, MEM%) en tiempo real",
            "La m&eacute;trica CPUUtilization de CloudWatch, que agrega el uso de CPU de toda la instancia",
            "Un script de shell en el host de RDS que publica m&eacute;tricas por proceso a CloudWatch",
            "Performance Insights de RDS, que mide la carga de la base de datos por consulta SQL",
        ],
        correct=0,
        key="dva05-q11-enhanced-monitoring",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Enhanced Monitoring de RDS.</div>'
            '<p><b>Enhanced Monitoring</b> obtiene m&eacute;tricas del sistema operativo desde un <b>agente EN la instancia</b>, en tiempo real, mostrando el uso de CPU y memoria <b>por proceso/hilo</b>. Se guardan en CloudWatch Logs (grupo <code>RDSOSMetrics</code>, 30 d&iacute;as por defecto). Es lo &uacute;nico que da el detalle por proceso.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>CloudWatch CPUUtilization:</b> toma la CPU desde el <b>hipervisor</b>, sin desglose por proceso ni memoria por proceso.</li>'
            '<li><b>Script de shell:</b> no tienes acceso al SO de una instancia RDS gestionada, as&iacute; que no puedes instalar un agente/propio script como en EC2.</li>'
            '<li><b>"CPU% y MEM% en la consola RDS":</b> las m&eacute;tricas <b>est&aacute;ndar</b> de la consola son agregadas a nivel de instancia (vienen de CloudWatch/hipervisor). El detalle <b>por proceso</b> s&iacute; se ve en la consola, pero solo cuando <b>habilitas Enhanced Monitoring</b>; no est&aacute; disponible por defecto sin activarlo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Por PROCESO/hilo en RDS &rarr; <b>Enhanced Monitoring</b> (agente en la instancia). CloudWatch = vista del hipervisor, menos detalle.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html">docs.aws RDS Enhanced Monitoring</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-relational-database-service-amazon-rds/">tutorialsdojo RDS</a></div>'
        ),
    ),
    card(
        question="&iquest;En qu&eacute; se diferencian las m&eacute;tricas de CPU de <b>CloudWatch</b> y de <b>Enhanced Monitoring</b> en RDS?",
        options=[
            "CloudWatch mide desde el hipervisor, sin desglose por proceso; Enhanced Monitoring, con un agente, por proceso",
            "CloudWatch mide por proceso con un agente; Enhanced Monitoring solo el total, desde el hipervisor de la instancia",
            "CloudWatch mide desde un agente en el sistema operativo; Enhanced Monitoring desde el hipervisor, por proceso",
            "CloudWatch mide desde el hipervisor y guarda historial; Enhanced Monitoring, por agente, sin conservar historial",
        ],
        correct=0,
        key="dva05-q11-cw-vs-enhanced",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CloudWatch = hipervisor; Enhanced = agente en la instancia.</div>'
            '<p><b>CloudWatch</b> recolecta la CPU desde la capa del <b>hipervisor</b> de la instancia; es una vista agregada, sin uso por proceso. <b>Enhanced Monitoring</b> usa un <b>agente en la instancia</b> y expone m&eacute;tricas del SO por proceso/hilo. Por eso los valores pueden diferir levemente (el hipervisor hace algo de trabajo aparte).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no son id&eacute;nticas. Es Enhanced (no CloudWatch) el que da el detalle por proceso. Enhanced S&iacute; guarda historial (CloudWatch Logs, 30 d&iacute;as por defecto, configurable).</p>'
            '<div class="extra"><span class="h">Dato extra</span>La diferencia es mayor en clases de instancia peque&ntilde;as (m&aacute;s VMs por host f&iacute;sico).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MonitoringOverview.html">docs.aws RDS monitoring overview</a></div>'
        ),
    ),

    # ================= Q12: Write-through caching =================
    card(
        question="Quieres que la cach&eacute; <b>nunca sirva datos obsoletos</b> (que siempre refleje la &uacute;ltima escritura), y que las entradas poco le&iacute;das <b>expiren solas de la cach&eacute;</b> con un TTL. &iquest;Cu&aacute;l pseudoc&oacute;digo implementa <b>write-through</b> con TTL?",
        options=[
            "UPDATE en la base de datos y luego <code>cache.set(id, valor, ttl)</code>",
            "Solo <code>cache.set(id, valor, ttl)</code> (sin tocar la base de datos)",
            "SELECT en la base de datos y luego <code>cache.set(id, valor, ttl)</code>",
            "UPDATE en la base de datos y luego <code>cache.delete(id)</code>",
        ],
        correct=0,
        key="dva05-q12-write-through",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; UPDATE en la BD y luego cache.set con TTL.</div>'
            '<p><b>Write-through</b> = cada vez que escribes en la base de datos, tambi&eacute;n <b>actualizas la misma clave en la cach&eacute;</b> con el nuevo valor. As&iacute; la cach&eacute; nunca sirve datos obsoletos: la entrada refleja siempre la &uacute;ltima escritura. El <b>TTL</b> (time-to-live) hace que las entradas poco le&iacute;das <b>expiren de la cach&eacute;</b> (no de la BD) y no se acumulen. Por eso: primero <code>UPDATE</code> en la BD, luego <code>cache.set(id, valor, ttl)</code>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Solo cache.set:</b> nunca actualiza la base de datos (la fuente de verdad).</li>'
            '<li><b>SELECT + cache.set:</b> lee, no escribe; la BD no se actualiza y la cach&eacute; podr&iacute;a quedar con un valor que no refleja una escritura.</li>'
            '<li><b>UPDATE + cache.delete:</b> actualiza la BD pero <b>invalida</b> (borra) la entrada de cach&eacute;, as&iacute; que la siguiente lectura es un miss y va a la BD (m&aacute;s lento). Eso es una estrategia de <b>invalidaci&oacute;n de cach&eacute;</b> (write-invalidate), no write-through, porque no deja el nuevo valor listo en la cach&eacute;.</li>'
            '</ul>'
            '<div class="warn"><span class="h">Ojo</span>El <b>TTL</b> expira la entrada en la <b>cach&eacute;</b>, no borra la fila en la base de datos. La fila en la BD permanece; write-through solo mantiene la copia en cach&eacute; fresca y deja que las entradas poco usadas caduquen.</div>'
            '<div class="extra"><span class="h">Dato de examen</span>Write-through: cach&eacute; siempre fresca pero gasta espacio en datos poco le&iacute;dos (por eso el TTL). Lazy loading (cache-aside): solo cachea al leer (puede servir datos obsoletos si la BD cambi&oacute;).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/Strategies.html">docs.aws caching strategies</a><br>'
            '<a href="https://aws.amazon.com/caching/best-practices/">aws caching best practices</a></div>'
        ),
    ),
    card(
        question="En caching, &iquest;por qu&eacute; se a&ntilde;ade un <b>TTL</b> a los items en una estrategia write-through?",
        options=[
            "Para que los datos poco le&iacute;dos expiren solos y no se acumule cach&eacute; que casi nunca se usa",
            "Para reducir la cantidad de conexiones abiertas contra la base de datos relacional",
            "Para forzar consistencia fuerte entre la cach&eacute; y la base de datos en cada escritura",
            "Para acelerar las escrituras a la base de datos evitando bloqueos durante el commit",
        ],
        correct=0,
        key="dva05-q12-why-ttl",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; para expirar datos poco le&iacute;dos y no desperdiciar espacio.</div>'
            '<p>En <b>write-through</b> se escribe a la cach&eacute; cada vez que escribes a la BD, aunque ese dato casi nunca se lea. Eso <b>desperdicia memoria</b>. Un <b>TTL</b> (tiempo de vida) hace que esos items expiren autom&aacute;ticamente, evitando que la cach&eacute; se llene de datos obsoletos y que el rendimiento se degrade.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Acelerar escrituras a la BD:</b> el TTL solo marca cu&aacute;ndo expira la entrada en cach&eacute;; no toca la escritura a la base de datos.</li>'
            '<li><b>Forzar consistencia fuerte en la BD:</b> la consistencia la aporta la estrategia write-through (la cach&eacute; refleja la &uacute;ltima escritura); el TTL no cambia la consistencia de la BD.</li>'
            '<li><b>Evitar cifrar:</b> el TTL no tiene relaci&oacute;n con el cifrado de los datos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato extra</span>El TTL es la forma est&aacute;ndar de mitigar el mayor defecto de write-through: cachear datos que casi nunca se leen.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/Strategies.html">docs.aws caching strategies</a></div>'
        ),
    ),

    # ================= Q13: AppSync vs Cognito Sync =================
    card(
        question="Una app de juego debe sincronizar preferencias y estado entre dispositivos, y adem&aacute;s permitir que <b>varios usuarios colaboren sobre datos compartidos en tiempo real</b>. &iquest;Qu&eacute; servicio usas?",
        options=[
            "Amazon Cognito Sync",
            "AWS AppSync",
            "AWS Amplify",
            "Amazon Pinpoint",
        ],
        correct=1,
        key="dva05-q13-appsync",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; AWS AppSync.</div>'
            '<p><b>AWS AppSync</b> es un servicio gestionado de <b>GraphQL</b> que da actualizaciones <b>en tiempo real</b>, acceso a datos sin conexi&oacute;n (offline) y sincronizaci&oacute;n con resoluci&oacute;n de conflictos. Su diferenciador clave es que permite que <b>varios usuarios colaboren sobre datos compartidos en tiempo real</b>, no solo sincronizar los datos de un &uacute;nico usuario.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Cognito Sync:</b> sincroniza datos de <b>un mismo usuario</b> entre sus dispositivos, pero NO permite colaboraci&oacute;n multi-usuario en tiempo real.</li>'
            '<li><b>Amplify:</b> es un framework para construir/desplegar apps web y m&oacute;viles, no un servicio de sincronizaci&oacute;n de datos entre dispositivos.</li>'
            '<li><b>Pinpoint:</b> es engagement de clientes (push, email, SMS, voz), no sincronizaci&oacute;n de datos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"Varios usuarios" + "tiempo real" + "datos compartidos"? &rarr; <b>AppSync</b>. Solo "un usuario en varios dispositivos" &rarr; Cognito Sync.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html">docs.aws AppSync</a><br>'
            '<a href="https://tutorialsdojo.com/aws-appsync/">tutorialsdojo AppSync</a></div>'
        ),
    ),
    card(
        question="&iquest;Cu&aacute;l es la diferencia clave entre <b>AWS AppSync</b> y <b>Amazon Cognito Sync</b> para sincronizar datos?",
        options=[
            "Cognito Sync sincroniza datos de un usuario entre sus dispositivos; AppSync a&ntilde;ade colaboraci&oacute;n multi-usuario en tiempo real sobre datos compartidos",
            "Ambos exponen una API GraphQL administrada; Cognito Sync agrega suscripciones en tiempo real y AppSync solo almacena datasets clave-valor por usuario",
            "Cognito Sync ofrece tiempo real por WebSockets entre usuarios; AppSync solo cachea datos localmente y no admite suscripciones ni notificaciones push",
            "Cognito Sync sincroniza datasets clave-valor entre servicios de backend; AppSync solo replica el estado de un &uacute;nico usuario sin compartir datos",
        ],
        correct=0,
        key="dva05-q13-appsync-vs-cognitosync",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Cognito Sync = un usuario; AppSync = multi-usuario en tiempo real.</div>'
            '<p>Ambos sincronizan datos de la app entre dispositivos. <b>Cognito Sync</b> lo hace por <b>identidad</b> (los datos de un mismo usuario, ej. preferencias o estado de juego). <b>AppSync</b> extiende eso permitiendo que <b>m&uacute;ltiples usuarios</b> sincronicen y <b>colaboren en tiempo real</b> sobre datos compartidos.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no son el mismo servicio. AppSync funciona online y offline (no "solo offline"). Es <b>AppSync</b> el que usa GraphQL, no Cognito Sync.</p>'
            '<div class="extra"><span class="h">Dato extra</span>AppSync resuelve conflictos de sincronizaci&oacute;n de forma configurable cuando los dispositivos vuelven a estar online.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/appsync/latest/devguide/what-is-appsync.html">docs.aws AppSync</a></div>'
        ),
    ),

    # ================= Q14: sam deploy =================
    card(
        question="Necesitas un solo comando que <b>comprima el c&oacute;digo, lo suba a S3, genere la plantilla empaquetada y la despliegue</b>. &iquest;Cu&aacute;l usas?",
        options=[
            "<code>sam deploy</code>",
            "<code>sam package</code>",
            "<code>sam publish</code>",
            "<code>aws cloudformation deploy</code>",
        ],
        correct=0,
        key="dva05-q14-sam-deploy",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; sam deploy.</div>'
            '<p><code>sam deploy</code> hace todo el flujo: <b>comprime</b> los artefactos, los <b>sube a S3</b>, produce la <b>plantilla empaquetada</b> y la <b>despliega</b> v&iacute;a CloudFormation (SAM usa CloudFormation por debajo).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>sam package</code>: solo comprime, sube a S3 y genera la plantilla; <b>no despliega</b>.</li>'
            '<li><code>sam publish</code>: publica la app al Serverless Application Repository; no genera plantilla ni despliega.</li>'
            '<li><code>aws cloudformation deploy</code>: espera que los artefactos <b>ya</b> est&eacute;n empaquetados y subidos a S3; no hace el empaquetado por ti.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato de examen</span>Para apps con aplicaciones anidadas, incluye la capability <code>CAPABILITY_AUTO_EXPAND</code> en <code>sam deploy</code>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-deploying.html">docs.aws SAM deploying</a><br>'
            '<a href="https://tutorialsdojo.com/aws-serverless-application-model-sam/">tutorialsdojo SAM</a></div>'
        ),
    ),

    # ================= Q17: TDE for SQL Server on RDS =================
    card(
        question="En RDS for SQL Server necesitas <b>cifrar los datos antes de escribirlos a disco y descifrarlos al leerlos</b>, a nivel de la base de datos. &iquest;Qu&eacute; habilitas?",
        options=[
            "RDS Encryption (cifrado en reposo del volumen)",
            "Transparent Data Encryption (TDE)",
            "IAM DB Authentication",
            "Microsoft SQL Server Windows Authentication",
        ],
        correct=1,
        key="dva05-q17-tde",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Transparent Data Encryption (TDE).</div>'
            '<p><b>TDE</b> cifra los archivos de datos y de log a <b>nivel de la base de datos</b>: cifra autom&aacute;ticamente antes de escribir a disco y descifra al leer. RDS lo soporta para SQL Server <b>2016 y 2017 en Enterprise Edition</b>, y <b>2019, 2022 y 2025 en Standard y Enterprise Edition</b>. Se activa con la <b>opci&oacute;n TDE en un option group</b> asociado a la instancia.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>RDS Encryption:</b> cifra el volumen de almacenamiento en reposo, pero en el marco de esta pregunta no cifra/descifra el <i>dato en s&iacute;</i> a nivel de motor como lo hace TDE.</li>'
            '<li><b>IAM DB Authentication:</b> autentica al usuario a la BD v&iacute;a IAM; no cifra datos.</li>'
            '<li><b>Windows Authentication:</b> autentica v&iacute;a AWS Managed Microsoft AD; no cifra datos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato extra</span>TDE usa arquitectura de dos niveles: un certificado (derivado de la master key de la BD) protege la clave de cifrado de datos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.SQLServer.Options.TDE.html">docs.aws RDS SQL Server TDE</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-relational-database-service-amazon-rds/">tutorialsdojo RDS</a></div>'
        ),
    ),

    # ================= Q18: GSI WCU >= base table WCU =================
    card(
        question="Creas un <b>GSI</b> en una tabla DynamoDB en modo <b>provisioned</b> con muchas escrituras. Para evitar throttling, &iquest;c&oacute;mo debes fijar la capacidad del &iacute;ndice?",
        options=[
            "El WCU del GSI debe ser igual o mayor que el WCU de la tabla base",
            "El WCU del GSI debe ser igual o menor que el WCU de la tabla base",
            "El RCU del GSI debe ser igual o mayor que el RCU de la tabla base",
            "El RCU del GSI debe ser igual o menor que el RCU de la tabla base",
        ],
        correct=0,
        key="dva05-q18-gsi-wcu",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; el WCU del GSI >= WCU de la tabla base.</div>'
            '<p>Un <b>GSI</b> (Global Secondary Index) tiene su <b>propia capacidad</b> aprovisionada, separada de la tabla base. Cada escritura en la tabla base <b>tambi&eacute;n</b> actualiza el GSI y consume WCU del GSI. Si el GSI tiene <b>WCU insuficiente</b>, se throttlea la <b>escritura sobre la tabla</b>. Por eso el WCU del GSI debe ser <b>igual o mayor</b> que el de la tabla base.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> "WCU menor" es la direcci&oacute;n equivocada (causar&iacute;a throttling). Las opciones de <b>RCU</b> no aplican: el escenario es de <b>escrituras</b>, as&iacute; que lo cr&iacute;tico es el WCU, no el RCU.</p>'
            '<div class="extra"><span class="h">Dato de examen</span>Una consulta al GSI consume RCU del <b>&iacute;ndice</b>, no de la tabla base; y las escrituras a la tabla consumen WCU del &iacute;ndice adem&aacute;s del de la tabla.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html#GSI.ThroughputConsiderations">docs.aws GSI throughput</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),
    card(
        question="Si un <b>GSI</b> en modo provisioned tiene <b>WCU insuficiente</b>, &iquest;qu&eacute; se ve afectado?",
        options=[
            "Solo las consultas al propio GSI",
            "Se throttlea la actividad de escritura sobre la tabla base",
            "Nada; el GSI toma WCU de la tabla base autom&aacute;ticamente",
            "Se borran items de la tabla base",
        ],
        correct=1,
        key="dva05-q18-gsi-throttle",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; se throttlea la escritura sobre la tabla base.</div>'
            '<p>Como cada escritura en la tabla base debe propagarse al GSI (consumiendo el WCU del &iacute;ndice), si el GSI se queda sin WCU, DynamoDB <b>throttlea la escritura en la tabla</b>. No es solo un problema del &iacute;ndice: afecta a la tabla entera.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no afecta "solo las consultas al GSI". El GSI <b>no</b> toma WCU de la tabla base (tiene capacidad propia). Y no se borran items.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Por eso la recomendaci&oacute;n es GSI WCU >= tabla base WCU cuando hay escrituras intensas.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html#GSI.ThroughputConsiderations">docs.aws GSI throughput</a></div>'
        ),
    ),

    # ================= Q21: S3 Object Lambda Access Points (role-based redaction) =================
    card(
        question="Debes redactar PII de registros en S3 de forma <b>distinta por rol</b>, cada usuario ve solo lo suyo, y manteniendo <b>una sola copia</b> de los datos. &iquest;Qu&eacute; combinaci&oacute;n usas? (marca la pieza del <b>Object Lambda</b>)",
        options=[
            "Un S3 Object Lambda Access Point por rol, con la funci&oacute;n RedactPII-[rol] adjunta; el cliente hace GetObject contra ese punto",
            "Una notificaci&oacute;n de eventos de S3 que invoca la funci&oacute;n RedactPII en cada petici&oacute;n GetObject del bucket, sin copiar datos",
            "Replicaci&oacute;n de S3 hacia un bucket por rol con una regla que redacta la PII durante la copia y el cliente lee la r&eacute;plica",
            "Un &uacute;nico access point con la API GetObjectLegalHold, que devuelve el objeto ya redactado seg&uacute;n el rol que hace la petici&oacute;n",
        ],
        correct=0,
        key="dva05-q21-object-lambda",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; un S3 Object Lambda Access Point por rol (asociado a su funci&oacute;n RedactPII-[rol]).</div>'
            '<p><b>S3 Object Lambda</b> a&ntilde;ade tu c&oacute;digo a las peticiones <b>GET</b> de S3 para transformar/redactar los datos <b>al vuelo</b>, sin guardar una segunda copia. La combinaci&oacute;n completa (esta opci&oacute;n ya incluye <code>GetObject</code>) es: (1) un <b>S3 Access Point</b> por rol, (2) un <b>S3 Object Lambda Access Point</b> por cada uno asociado a la funci&oacute;n <code>RedactPII-[rol]</code>, (3) el usuario hace <code>GetObject</code> contra su Object Lambda Access Point. El <b>aislamiento por rol</b> ("cada usuario ve solo lo suyo") lo da <b>IAM</b>: cada rol asume un rol IAM con permiso <b>solo</b> a su propio Object Lambda Access Point. As&iacute; se mantiene <b>una sola copia</b> en el bucket.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Notificaci&oacute;n de eventos S3:</b> se disparan al <b>crear</b> objetos, no en peticiones GET.</li>'
            '<li><b>S3 Replication:</b> crea copias adicionales, lo que viola el requisito de una sola copia.</li>'
            '<li><b>GetObjectLegalHold:</b> solo devuelve el estado de retenci&oacute;n legal de un objeto; no redacta datos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato de examen</span>Object Lambda transforma en el <b>GET</b> (redactar, filtrar filas, redimensionar) sin guardar copias transformadas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html">docs.aws S3 Object Lambda</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-s3/">tutorialsdojo S3</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; hace exactamente <b>S3 Object Lambda</b> y por qu&eacute; evita duplicar los datos?",
        options=[
            "Ejecuta tu funci&oacute;n Lambda durante la petici&oacute;n GET, LIST o HEAD y devuelve la versi&oacute;n transformada con WriteGetObjectResponse, sin almacenar una copia derivada",
            "Dispara una funci&oacute;n Lambda por notificaci&oacute;n de evento al subir el objeto (PUT), guardando la versi&oacute;n transformada que luego sirve cada petici&oacute;n GET",
            "Transforma el objeto en la primera lectura y guarda esa versi&oacute;n en la cach&eacute; de CloudFront, sirviendo esa copia derivada en las siguientes peticiones",
            "Aplica reglas de transformaci&oacute;n mediante replicaci&oacute;n S3 y mantiene una copia ya transformada en un bucket de destino que la aplicaci&oacute;n consulta por GET",
        ],
        correct=0,
        key="dva05-q21-object-lambda-how",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; ejecuta tu c&oacute;digo en el GET y transforma al vuelo, sin copia extra.</div>'
            '<p><b>S3 Object Lambda</b> intercepta la petici&oacute;n <b>GET</b> y ejecuta una funci&oacute;n Lambda que transforma la salida (redactar PII, filtrar filas, redimensionar im&aacute;genes, etc.) <b>en el momento de la recuperaci&oacute;n</b>. Como transforma sobre la marcha, no necesitas almacenar una copia redactada aparte: se mantiene <b>una sola copia</b> del dato original.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no copia a otro bucket (eso duplicar&iacute;a). No es cifrado por rol. No es un batch nocturno; transforma en tiempo de lectura, no por adelantado.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Un S3 Object Lambda Access Point puede incluso ser <b>origin</b> de CloudFront para transformar contenido servido por CDN.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html">docs.aws S3 Object Lambda</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(deck_name="DVA-C02::05", cards=cards, out_path="out/DVA-C02_05.apkg")
