#!/usr/bin/env python3
"""
DVA-C02::07 - Cards from PRACTICE SET 2, only the questions the user got INCORRECT.
Source: notes/source/set2_practice_questions.txt (Q2,4,6,7,10,15,17,19,21,23,26,29,34,37,41,45,47,48,50,57)

Each long exam question is broken into 2-3 atomic cards (one concept per card),
following DECK_STANDARDS.md: self-contained stems, {{L}} verdict, refute every
distractor one by one, explanations in Spanish, 4 options, stable keys.
"""
from anki_mcq import card, create

cards = [
    # ================= Q2: DynamoDB ReturnConsumedCapacity =================
    card(
        question="En una operaci&oacute;n de escritura de DynamoDB (UpdateItem/PutItem/DeleteItem) quieres el <b>total de write capacity units consumidos, con subtotales para la tabla y cada &iacute;ndice secundario</b> afectado. &iquest;Qu&eacute; valor pones en el par&aacute;metro <code>ReturnConsumedCapacity</code>?",
        options=["INDEXES", "TOTAL", "NONE", "TRUE"],
        correct=0,
        key="dva07-q2-returnconsumedcapacity-indexes",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; INDEXES.</div>'
            '<p><code>ReturnConsumedCapacity</code> controla qu&eacute; informaci&oacute;n de capacidad devuelve la operaci&oacute;n de escritura. El valor <b>INDEXES</b> devuelve el total de WCU consumidos <b>m&aacute;s los subtotales</b> para la tabla base y para cada &iacute;ndice secundario (GSI/LSI) que la operaci&oacute;n toc&oacute;. Eso es justo lo que pide el escenario para diagnosticar throttling por &iacute;ndice.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>TOTAL:</b> devuelve solo el total agregado, <b>sin</b> desglosar por tabla e &iacute;ndices. No te deja ver qu&eacute; &iacute;ndice consume.</li>'
            '<li><b>NONE:</b> no devuelve ning&uacute;n detalle de capacidad (es el valor por defecto).</li>'
            '<li><b>TRUE:</b> no es un valor v&aacute;lido; el par&aacute;metro no es booleano. Solo acepta TOTAL, INDEXES o NONE.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"subtotales por tabla e &iacute;ndices"? &rarr; <b>INDEXES</b>. &iquest;"solo el total"? &rarr; TOTAL.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html">docs.aws UpdateItem</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, &iquest;cu&aacute;l es el valor <b>por defecto</b> del par&aacute;metro <code>ReturnConsumedCapacity</code> y qu&eacute; hace?",
        options=[
            "NONE: no devuelve ning&uacute;n detalle de capacidad consumida",
            "TOTAL: devuelve el total de capacidad consumida",
            "INDEXES: devuelve subtotales por tabla e &iacute;ndices",
            "FALSE: desactiva el conteo de capacidad",
        ],
        correct=0,
        key="dva07-q2-returnconsumedcapacity-default",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; NONE es el valor por defecto.</div>'
            '<p>Si no especificas <code>ReturnConsumedCapacity</code>, DynamoDB usa <b>NONE</b>: la respuesta <b>no</b> incluye informaci&oacute;n de capacidad consumida. Debes pedir expl&iacute;citamente TOTAL o INDEXES para verla.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> TOTAL e INDEXES devuelven datos de capacidad pero no son el valor por defecto; hay que activarlos. FALSE no existe: el par&aacute;metro no es booleano, solo acepta TOTAL, INDEXES y NONE.</p>'
            '<div class="extra"><span class="h">Dato</span>Pedir capacidad no cuesta unidades extra; solo cambia lo que la respuesta reporta.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html">docs.aws PutItem</a></div>'
        ),
    ),

    # ================= Q4: S3 Object Lambda redaction per role =================
    card(
        question="Debes servir a cada rol una versi&oacute;n <b>redactada distinta</b> de los mismos registros PII en S3, manteniendo <b>una sola copia</b> de los datos, aplicando una Lambda RedactPII-[role] por rol. &iquest;Qu&eacute; combinaci&oacute;n de recursos S3 usas?",
        options=[
            "Un S3 Access Point por rol + un S3 Object Lambda Access Point por rol asociado a su Lambda RedactPII",
            "Un solo S3 Access Point compartido + una Lambda que decide el rol internamente",
            "S3 Replication para crear una copia redactada por rol",
            "S3 Event Notification que invoca RedactPII en cada GET",
        ],
        correct=0,
        key="dva07-q4-object-lambda-per-role",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; un S3 Access Point + un Object Lambda Access Point por rol.</div>'
            '<p><b>S3 Object Lambda</b> ejecuta tu c&oacute;digo durante un <b>GET</b> para transformar el objeto <b>al momento de recuperarlo</b>, sin guardar copias transformadas. La arquitectura: creas un <b>S3 Access Point por rol</b>, y encima un <b>Object Lambda Access Point por rol</b> asociado a la Lambda <code>RedactPII-[role]</code> correspondiente. Cada usuario hace un GetObject a su propio Object Lambda Access Point y recibe la redacci&oacute;n adecuada a su rol. As&iacute; hay <b>una sola copia</b> en el bucket.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Access Point compartido con l&oacute;gica interna:</b> t&eacute;cnicamente un solo Object Lambda Access Point con una Lambda que ramifica seg&uacute;n la identidad IAM del caller <b>tambi&eacute;n funcionar&iacute;a</b>. Pero el patr&oacute;n que pide el escenario (un endpoint y permisos por rol, con una Lambda RedactPII-[role] por rol) da un aislamiento por rol m&aacute;s limpio y directo v&iacute;a Access Points separados, y es la combinaci&oacute;n correcta entre las opciones dadas.</li>'
            '<li><b>S3 Replication:</b> crea <b>copias adicionales</b>, contradice el requisito de una sola copia.</li>'
            '<li><b>S3 Event Notification:</b> notifica en creaci&oacute;n de objetos (ObjectCreated), <b>no</b> se dispara en GET para transformar la respuesta.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"transformar el dato al recuperarlo, una sola copia, distinto por rol"? &rarr; <b>S3 Object Lambda Access Points</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/s3/features/object-lambda/">aws.amazon S3 Object Lambda</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-s3/">tutorialsdojo S3</a></div>'
        ),
    ),
    card(
        question="Con S3 Object Lambda, &iquest;qu&eacute; API usa el cliente para obtener el dato ya transformado (redactado) a trav&eacute;s del Object Lambda Access Point?",
        options=[
            "GetObject (est&aacute;ndar) contra el Object Lambda Access Point",
            "GetObjectLegalHold para recuperar el dato redactado",
            "InvokeFunction directamente sobre la Lambda RedactPII",
            "SelectObjectContent con una consulta SQL",
        ],
        correct=0,
        key="dva07-q4-object-lambda-getobject",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; GetObject est&aacute;ndar.</div>'
            '<p>El cliente emite un <b>GetObject</b> normal apuntando al <b>Object Lambda Access Point</b>. S3 invoca por debajo la Lambda asociada, que transforma el objeto y devuelve la versi&oacute;n redactada. No cambia el API del cliente: sigue siendo GetObject.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>GetObjectLegalHold</b> solo devuelve el estado de retenci&oacute;n legal de un objeto, nada que ver con redactar. <b>InvokeFunction</b> directo salta toda la integraci&oacute;n de Object Lambda y su control de acceso por Access Point. <b>SelectObjectContent</b> es S3 Select (consulta SQL sobre CSV/JSON/Parquet), no aplica la transformaci&oacute;n de Object Lambda.</p>'
            '<div class="extra"><span class="h">Dato</span>La gracia de Object Lambda: el cliente no cambia su c&oacute;digo, solo apunta a otro Access Point.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html">docs.aws transforming objects</a></div>'
        ),
    ),
    card(
        question="&iquest;En qu&eacute; se diferencia <b>S3 Object Lambda</b> de una <b>S3 Event Notification</b> que invoca una Lambda, respecto a cu&aacute;ndo actua?",
        options=[
            "Object Lambda transforma el objeto al RECUPERARLO (GET); Event Notification dispara en eventos de escritura/estado (ObjectCreated), no en GET",
            "Ambas actuan en el GET del objeto",
            "Object Lambda actua al subir; Event Notification al recuperar",
            "Ambas crean copias transformadas del objeto",
        ],
        correct=0,
        key="dva07-q4-objectlambda-vs-eventnotif",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Object Lambda en el GET; Event Notification en escrituras.</div>'
            '<p><b>S3 Object Lambda</b> se ejecuta durante la <b>recuperaci&oacute;n</b> (GET/LIST/HEAD) para transformar el objeto sobre la marcha, sin guardar copias. <b>S3 Event Notification</b> dispara ante eventos de <b>escritura o cambio de estado</b> (ObjectCreated, ObjectRemoved, etc.), t&iacute;picamente para procesar un objeto <b>tras subirlo</b> (ej. generar un thumbnail). No se dispara en GET.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no ambas actuan en GET; se invierten los momentos (Object Lambda = recuperar, Event Notification = escribir); y Object Lambda justamente <b>evita</b> copias transformadas.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;transformar al leer, sin copias? &rarr; Object Lambda. &iquest;procesar al subir? &rarr; Event Notification &rarr; Lambda.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html">docs.aws event notifications</a></div>'
        ),
    ),
    card(
        question="Al usar un <b>Global Secondary Index (GSI)</b> en DynamoDB, &iquest;de d&oacute;nde se consumen las unidades de capacidad de las queries/scans sobre ese &iacute;ndice?",
        options=[
            "Del propio GSI, no de la tabla base",
            "De la tabla base, no del &iacute;ndice",
            "Se reparten al 50% entre &iacute;ndice y tabla base",
            "No consumen capacidad porque el &iacute;ndice es solo lectura",
        ],
        correct=0,
        key="dva07-q6-gsi-capacity",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; del propio GSI.</div>'
            '<p>Un <b>GSI</b> tiene su <b>propia capacidad provisionada</b> (RCU/WCU) separada de la tabla base. Las <b>queries y scans sobre el &iacute;ndice</b> consumen capacidad <b>del &iacute;ndice</b> (no de la tabla base): esto es lo que pregunta la carta.</p>'
            '<p><b>Ojo con las escrituras (matiz importante):</b> cuando escribes en la tabla y eso actualiza el GSI, la escritura consume WCU de la <b>tabla base</b> Y <b>adicionalmente</b> WCU del <b>&iacute;ndice</b>. Es la <b>suma</b> de ambos, no "&iacute;ndice en vez de tabla". El "del &iacute;ndice, no de la tabla" aplica solo a <b>lecturas</b> (query/scan) sobre el GSI.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> para lecturas sobre el &iacute;ndice, la capacidad sale del GSI, no de la tabla base (esa es la confusi&oacute;n t&iacute;pica con LSI, que s&iacute; usa la capacidad de la tabla). No se reparte 50/50. Y s&iacute; consume capacidad: leer de un &iacute;ndice no es gratis.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Lectura sobre GSI &rarr; capacidad del <b>&iacute;ndice</b>. Escritura que toca el GSI &rarr; <b>tabla base + &iacute;ndice</b> (suma). LSI &rarr; comparte la capacidad de la <b>tabla base</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html">docs.aws GSI</a><br>'
            '<a href="https://tutorialsdojo.com/global-secondary-index-vs-local-secondary-index/">tutorialsdojo GSI vs LSI</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; consistencia de lectura soporta un <b>Global Secondary Index (GSI)</b> de DynamoDB?",
        options=[
            "Solo consistencia eventual (eventual consistency)",
            "Solo consistencia fuerte (strong consistency)",
            "Eventual o fuerte, a elecci&oacute;n del cliente",
            "Consistencia transaccional garantizada",
        ],
        correct=0,
        key="dva07-q6-gsi-eventual",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; solo eventual consistency.</div>'
            '<p>Las lecturas contra un <b>GSI</b> son <b>siempre eventualmente consistentes</b>. DynamoDB propaga los cambios de la tabla al GSI de forma as&iacute;ncrona, por lo que un GSI puede ir ligeramente atrasado. <b>No</b> puedes pedir strong consistency en un GSI.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> la strong consistency (y la opci&oacute;n de elegir eventual o fuerte) aplica a la tabla base y a los <b>LSI</b>, no a los GSI. No existe una garant&iacute;a transaccional propia del &iacute;ndice.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;Necesitas strong consistency con sort key alterna? &rarr; usa <b>LSI</b>, no GSI.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html">docs.aws GSI</a></div>'
        ),
    ),
    card(
        question="Respecto a la <b>partition key</b>: &iquest;en qu&eacute; se diferencian un <b>GSI</b> y un <b>LSI</b> de DynamoDB?",
        options=[
            "GSI puede tener una partition key DISTINTA a la de la tabla; LSI debe usar la MISMA partition key con una sort key alterna",
            "GSI debe usar la misma partition key; LSI puede usar una distinta",
            "ambos deben usar la misma partition key que la tabla",
            "ambos pueden usar cualquier partition key distinta",
        ],
        correct=0,
        key="dva07-q6-gsi-vs-lsi-pk",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; GSI PK distinta; LSI misma PK.</div>'
            '<p>Un <b>GSI</b> es "global" porque puede tener una <b>partition key (y sort key) diferentes</b> a las de la tabla base, abarcando todas las particiones. Un <b>LSI</b> es "local" porque comparte la <b>misma partition key</b> de la tabla y solo cambia la <b>sort key</b>, consultando dentro de una sola partici&oacute;n.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten la regla o igualan ambos &iacute;ndices; el punto clave es que solo el GSI puede cambiar la partition key.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;otra partition key? &rarr; GSI. &iquest;misma PK, otra sort key? &rarr; LSI (y strong consistency posible).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html">docs.aws secondary indexes</a></div>'
        ),
    ),
    card(
        question="En API Gateway con backend Lambda, necesitas <b>especificar c&oacute;mo se mapean</b> los datos de la petici&oacute;n entrante a la integraci&oacute;n y la respuesta de la integraci&oacute;n al m&eacute;todo. &iquest;Qu&eacute; tipo de integraci&oacute;n usas?",
        options=[
            "Lambda custom (non-proxy) integration",
            "Lambda proxy integration",
            "HTTP proxy integration",
            "HTTP custom integration",
        ],
        correct=0,
        key="dva07-q7-lambda-custom-integration",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Lambda custom (non-proxy) integration.</div>'
            '<p>La <b>Lambda custom (non-proxy) integration</b> te obliga a configurar la <b>integration request</b> y la <b>integration response</b>, definiendo <b>mapping templates</b> que transforman los datos entre el m&eacute;todo y la Lambda. Eso es exactamente "especificar c&oacute;mo se mapea la petici&oacute;n y la respuesta".</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda proxy:</b> pasa la petici&oacute;n <b>tal cual</b> a la Lambda y devuelve su salida sin mapeos configurables. Justo lo contrario de lo que pide el escenario.</li>'
            '<li><b>HTTP proxy / HTTP custom:</b> son para backends <b>HTTP</b>, no Lambda. Como el backend es Lambda, debes usar una integraci&oacute;n de tipo Lambda.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"mapear request/response"? &rarr; <b>custom (non-proxy)</b>. &iquest;"pasar todo sin tocar"? &rarr; proxy.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-integration-types.html">docs.aws integration types</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-api-gateway/">tutorialsdojo API Gateway</a></div>'
        ),
    ),
    card(
        question="En API Gateway con backend Lambda, &iquest;qu&eacute; diferencia hay entre <b>Lambda proxy</b> y <b>Lambda custom (non-proxy)</b> integration?",
        options=[
            "Proxy pasa la petici&oacute;n tal cual y devuelve la salida sin mapeos; custom exige configurar integration request/response con mapping templates",
            "Proxy exige mapping templates; custom pasa todo sin tocar",
            "Ambas exigen configurar mapping templates",
            "Proxy es para backends HTTP; custom es para backends Lambda",
        ],
        correct=0,
        key="dva07-q7-proxy-vs-custom",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; proxy = pass-through; custom = mapeos configurables.</div>'
            '<p>En <b>Lambda proxy</b> (<code>AWS_PROXY</code>) API Gateway pasa la petici&oacute;n <b>tal cual</b> a la Lambda (headers, query, body, contexto) y devuelve lo que la Lambda responda, sin que configures integration request/response. En <b>Lambda custom (non-proxy)</b> s&iacute; configuras la <b>integration request</b> y la <b>integration response</b> con <b>mapping templates</b> (plantillas VTL, Velocity Template Language) para transformar los datos.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten cu&aacute;l usa mapeos (es custom, no proxy). No es cierto que ambas los exijan (proxy no). Y ambas integraciones son de tipo Lambda: proxy no es "para HTTP" (eso ser&iacute;a HTTP proxy, otra cosa).</p>'
            '<div class="extra"><span class="h">Truco de examen</span>proxy = simple, pass-through, tu c&oacute;digo arma la respuesta. custom = mapping templates en API Gateway.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html">docs.aws Lambda proxy</a></div>'
        ),
    ),
    card(
        question="Otros sitios est&aacute;n <b>hotlinkeando</b> tus fotos alojadas en S3 (las enlazan desde sus p&aacute;ginas), subiendo tus costos de transferencia. Quieres controlar el acceso de forma <b>escalable</b>. &iquest;Qu&eacute; soluci&oacute;n es la m&aacute;s efectiva?",
        options=[
            "CloudFront con signed URLs o signed cookies",
            "Habilitar CORS permitiendo GET desde todos los or&iacute;genes",
            "Bloquear las IP de los sitios ofensores con Network ACL",
            "Generar pre-signed URLs de S3 con expiraci&oacute;n para cada objeto",
        ],
        correct=0,
        key="dva07-q10-cloudfront-signed",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CloudFront signed URLs o signed cookies.</div>'
            '<p>Con <b>CloudFront</b> puedes exigir <b>signed URLs</b> (URL con firma, fecha de expiraci&oacute;n y pol&iacute;tica) o <b>signed cookies</b> (para varios archivos sin cambiar las URLs). As&iacute; solo clientes autorizados acceden al contenido en la capa de CDN, y se controlan los costos de transferencia. Adem&aacute;s, <b>CloudFront Functions</b> puede validar el header Referer para permitir solo tu propio dominio.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CORS a todos los or&iacute;genes:</b> empeora el problema, permite que cualquier sitio use tus objetos.</li>'
            '<li><b>Network ACL por IP:</b> un cambio de IP lo evade; no es eficiente ni escalable.</li>'
            '<li><b>Pre-signed URLs de S3 por objeto:</b> no escala; habr&iacute;a que generar una URL por cada uno de miles/millones de objetos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato</span>signed URL = un archivo; signed cookie = muchos archivos sin cambiar las URLs existentes.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-urls.html">docs.aws signed URLs</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cloudfront/">tutorialsdojo CloudFront</a></div>'
        ),
    ),
    card(
        question="En CloudFront, &iquest;cu&aacute;ndo usas <b>signed URL</b> y cu&aacute;ndo <b>signed cookies</b> para restringir contenido?",
        options=[
            "signed URL para archivos individuales; signed cookies para varios archivos sin cambiar las URLs",
            "signed URL para varios archivos; signed cookies para uno solo",
            "signed URL solo para HTTP; signed cookies solo para HTTPS",
            "son intercambiables, no hay diferencia funcional",
        ],
        correct=0,
        key="dva07-q10-signedurl-vs-cookie",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; URL = archivo individual; cookie = varios archivos.</div>'
            '<p><b>Signed URL:</b> das acceso a <b>un archivo</b> (o cuando tu cliente no soporta cookies). <b>Signed cookies:</b> das acceso a <b>varios archivos</b> (por ejemplo, toda el &aacute;rea de suscriptores) <b>sin cambiar</b> las URLs existentes. Ambos llevan una pol&iacute;tica con expiraci&oacute;n y restricciones.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> se invierten los casos de uso; no dependen de HTTP vs HTTPS; y no son intercambiables sin criterio (dependen de si necesitas 1 o muchos archivos y de si puedes/quieres cambiar las URLs).</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;muchos archivos sin tocar URLs? &rarr; <b>signed cookies</b>. &iquest;un archivo puntual? &rarr; <b>signed URL</b>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-choosing-signed-urls-cookies.html">docs.aws elegir URL vs cookies</a></div>'
        ),
    ),
    card(
        question="Para frenar el <b>hotlinking</b> de tus im&aacute;genes en CloudFront, &iquest;por qu&eacute; una <b>Network ACL por IP</b> y <b>CORS abierto a todos</b> son malas soluciones?",
        options=[
            "La NACL por IP se evade cambiando de IP; CORS abierto permite que cualquier sitio use tus objetos (empeora)",
            "La NACL por IP es la mejor opci&oacute;n; CORS abierto tambi&eacute;n sirve",
            "Ambas bloquean el hotlinking a nivel de aplicaci&oacute;n",
            "CORS por IP y NACL abierto son equivalentes a signed URLs",
        ],
        correct=0,
        key="dva07-q10-why-not-nacl-cors",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; NACL por IP se evade; CORS abierto empeora.</div>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Network ACL por IP:</b> los sitios ofensores pueden <b>cambiar de IP</b> f&aacute;cilmente, as&iacute; que bloquear IPs no es eficiente ni escalable.</li>'
            '<li><b>CORS abierto a todos:</b> CORS no es un control de acceso; abrirlo a <code>*</code> permite que <b>cualquier</b> origen consuma tus objetos, empeorando el problema (adem&aacute;s CORS ni siquiera bloquea un <code>&lt;img src&gt;</code> hotlink).</li>'
            '<li><b>"NACL por IP es la mejor" / "ambas bloquean a nivel app":</b> falso; ninguna opera en capa de aplicaci&oacute;n contra hotlinking de forma escalable.</li>'
            '</ul>'
            '<p>Lo escalable es controlar el acceso en la CDN (signed URLs/cookies) o validar el header Referer con una CloudFront Function.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>CORS no es seguridad de acceso; NACL por IP no escala contra atacantes que rotan IP.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html">docs.aws private content</a></div>'
        ),
    ),
    card(
        question="Quieres <b>filtrar trazas de X-Ray por annotations</b> con la <b>m&iacute;nima configuraci&oacute;n</b>, y obtener los trace IDs y annotations program&aacute;ticamente. &iquest;Qu&eacute; dos acciones eliges? (elige el par correcto)",
        options=[
            "Filter expressions en la consola de X-Ray + la API GetTraceSummaries",
            "La API BatchGetTraces + configurar Sampling Rules",
            "Enviar trazas a S3 + consultar con Amazon Athena",
            "La API GetTraceGraph + configurar grupos de X-Ray",
        ],
        correct=0,
        key="dva07-q15-filter-gettracesummaries",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; filter expressions + GetTraceSummaries.</div>'
            '<p>Las <b>annotations</b> son pares clave-valor <b>indexados</b>, as&iacute; que puedes buscarlas con <b>filter expressions</b> en la consola de X-Ray. Program&aacute;ticamente, <b>GetTraceSummaries</b> devuelve los <b>trace IDs y annotations</b> de un rango de tiempo, aceptando un filtro opcional. Ambas requieren poca configuraci&oacute;n.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>BatchGetTraces:</b> recupera trazas <b>por ID</b>; no soporta filter expressions ni devuelve annotations para buscar.</li>'
            '<li><b>Sampling Rules:</b> solo controlan <b>cu&aacute;ntas</b> peticiones se registran, no sirven para filtrar/buscar trazas.</li>'
            '<li><b>S3 + Athena:</b> funciona pero implica <b>mucha</b> configuraci&oacute;n, contrario al requisito de m&iacute;nima config.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"buscar/filtrar por annotation"? &rarr; est&aacute;n <b>indexadas</b> &rarr; filter expressions + GetTraceSummaries.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html">docs.aws X-Ray filters</a><br>'
            '<a href="https://tutorialsdojo.com/aws-x-ray/">tutorialsdojo X-Ray</a></div>'
        ),
    ),
    card(
        question="En X-Ray, &iquest;cu&aacute;l es la diferencia entre las APIs <b>GetTraceSummaries</b> y <b>BatchGetTraces</b>?",
        options=[
            "GetTraceSummaries busca por rango de tiempo con filter expression y devuelve IDs + annotations; BatchGetTraces recupera trazas completas por ID (sin filtro)",
            "BatchGetTraces acepta filter expressions; GetTraceSummaries solo por ID",
            "Ambas aceptan filter expressions",
            "GetTraceSummaries configura sampling; BatchGetTraces filtra por annotation",
        ],
        correct=0,
        key="dva07-q15-gettracesummaries-vs-batch",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Summaries filtra por tiempo; BatchGetTraces por ID.</div>'
            '<p><b>GetTraceSummaries</b>: recibe StartTime/EndTime y una <b>FilterExpression</b> opcional, y devuelve los <b>resumenes</b> (trace IDs y annotations) que coinciden. Es la forma de <b>descubrir</b> qu&eacute; trazas te interesan. <b>BatchGetTraces</b>: recibe una lista de <b>trace IDs</b> (1 a 5) y devuelve las trazas <b>completas</b>; no acepta filter expression.</p>'
            '<p><b>Flujo t&iacute;pico:</b> primero GetTraceSummaries (filtras y obtienes IDs), luego BatchGetTraces con esos IDs para el detalle completo.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten qui&eacute;n filtra; ni ambas filtran; y ni Summaries configura sampling (eso son las Sampling Rules).</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Buscar/filtrar &rarr; <b>GetTraceSummaries</b>. Traer el detalle por ID &rarr; <b>BatchGetTraces</b>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/xray/latest/api/API_GetTraceSummaries.html">docs.aws GetTraceSummaries</a></div>'
        ),
    ),
    card(
        question="Tu portal (detr&aacute;s de ALB/CloudFront/API Gateway) recibe muchos intentos de <b>SQL injection</b> y <b>cross-site scripting (XSS)</b>. &iquest;Qu&eacute; servicio mitiga estos ataques a nivel de capa 7?",
        options=["AWS WAF", "Amazon GuardDuty", "AWS Firewall Manager", "Network ACL"],
        correct=0,
        key="dva07-q17-waf-sqli-xss",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; AWS WAF.</div>'
            '<p><b>AWS WAF</b> (Web Application Firewall) inspecciona el tr&aacute;fico <b>HTTP/HTTPS</b> hacia CloudFront, ALB o API Gateway y bloquea seg&uacute;n reglas. Tiene reglas espec&iacute;ficas contra <b>SQL injection</b> y <b>XSS</b> (y managed rule groups). Es la herramienta correcta para ataques de capa de aplicaci&oacute;n.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>GuardDuty:</b> detecci&oacute;n de amenazas/actividad maliciosa; <b>alerta</b> pero no bloquea peticiones web.</li>'
            '<li><b>Firewall Manager:</b> administra WAF/Shield <b>a escala</b> en varias cuentas; no es el que inspecciona/bloquea por s&iacute; mismo.</li>'
            '<li><b>Network ACL:</b> filtra por IP/puerto (capa 3/4) en la VPC; no entiende SQLi ni XSS (capa 7).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;SQLi/XSS a nivel HTTP? &rarr; <b>WAF</b>. &iquest;Muchas cuentas administradas central? &rarr; Firewall Manager (encima de WAF).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html">docs.aws WAF</a><br>'
            '<a href="https://tutorialsdojo.com/aws-waf/">tutorialsdojo WAF</a></div>'
        ),
    ),
    card(
        question="Distingue el rol de <b>AWS WAF</b>, <b>Amazon GuardDuty</b> y <b>AWS Firewall Manager</b>. &iquest;Cu&aacute;l describe correctamente a cada uno?",
        options=[
            "WAF filtra/bloquea tr&aacute;fico web (capa 7); GuardDuty detecta amenazas (alerta); Firewall Manager administra WAF/Shield a escala en varias cuentas",
            "WAF detecta amenazas; GuardDuty bloquea tr&aacute;fico web; Firewall Manager es un firewall de red",
            "Los tres bloquean SQLi/XSS de la misma forma",
            "Firewall Manager reemplaza a WAF inspeccionando peticiones HTTP",
        ],
        correct=0,
        key="dva07-q17-waf-vs-guardduty-vs-fm",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; WAF bloquea web, GuardDuty detecta, Firewall Manager administra.</div>'
            '<p><b>AWS WAF:</b> inspecciona y <b>bloquea</b> peticiones HTTP/HTTPS (SQLi, XSS, rate limiting) en CloudFront/ALB/API Gateway. <b>GuardDuty:</b> servicio de <b>detecci&oacute;n de amenazas</b> que analiza logs y <b>alerta</b> sobre actividad maliciosa, pero no bloquea el tr&aacute;fico web. <b>Firewall Manager:</b> <b>administra centralmente</b> reglas de WAF y Shield Advanced <b>a escala</b> en muchas cuentas de una organizaci&oacute;n; se apoya en WAF, no lo reemplaza.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten los roles de WAF/GuardDuty; no los tres bloquean SQLi/XSS igual (solo WAF inspecciona capa 7); y Firewall Manager no inspecciona peticiones por s&iacute; mismo.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Bloquear web &rarr; WAF. Detectar/alertar &rarr; GuardDuty. Administrar a escala &rarr; Firewall Manager.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html">docs.aws WAF</a></div>'
        ),
    ),
    card(
        question="Sirves un sitio est&aacute;tico (im&aacute;genes, videos, HTML, JS) con la <b>menor latencia posible para usuarios globales</b>. &iquest;Qu&eacute; combinaci&oacute;n de servicios usas?",
        options=[
            "Amazon S3 (almacenamiento) + Amazon CloudFront (CDN)",
            "Amazon EC2 + Amazon CloudFront",
            "Amazon EFS + Amazon CloudFront",
            "Amazon S3 Glacier + Amazon CloudFront",
        ],
        correct=0,
        key="dva07-q19-s3-cloudfront",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; S3 + CloudFront.</div>'
            '<p><b>S3</b> guarda los archivos est&aacute;ticos de forma durable y barata; <b>CloudFront</b> es la CDN que cachea el contenido en <b>edge locations</b> cerca del usuario, reduciendo la latencia global. S3 se configura como <b>origen</b> de la distribuci&oacute;n de CloudFront.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EC2:</b> procesamiento din&aacute;mico y es regional; no es &oacute;ptimo como origen de est&aacute;ticos globales.</li>'
            '<li><b>EFS:</b> sistema de archivos regional; no es adecuado para est&aacute;ticos y no se conecta directo a CloudFront como S3.</li>'
            '<li><b>Glacier:</b> archivado con recuperaci&oacute;n lenta; no sirve para servir contenido con baja latencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"est&aacute;tico + baja latencia global"? &rarr; <b>S3 + CloudFront</b> casi siempre.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/cloudfront/">aws.amazon CloudFront</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cloudfront/">tutorialsdojo CloudFront</a></div>'
        ),
    ),
    card(
        question="Para servir contenido est&aacute;tico global con baja latencia, &iquest;por qu&eacute; <b>EC2</b>, <b>EFS</b> y <b>Glacier</b> NO son buenos como almacenamiento/origen frente a S3?",
        options=[
            "EC2 es regional y para procesamiento din&aacute;mico; EFS es regional y no es origen nativo de CloudFront; Glacier es archivado con recuperaci&oacute;n lenta",
            "EC2 es la mejor opci&oacute;n como origen est&aacute;tico global",
            "EFS se conecta directo a CloudFront igual que S3",
            "Glacier sirve contenido con la menor latencia posible",
        ],
        correct=0,
        key="dva07-q19-why-not-efs-ec2-glacier",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; EC2 regional/din&aacute;mico, EFS no es origen nativo, Glacier es archivado.</div>'
            '<p><b>EC2:</b> pensado para procesamiento del lado del servidor y es <b>regional</b>; como origen de est&aacute;ticos globales no es &oacute;ptimo (ser&iacute;a un "custom origin" que t&uacute; operas). <b>EFS:</b> sistema de archivos <b>regional</b> y <b>no</b> figura en la lista de or&iacute;genes nativos de CloudFront (S3, MediaStore/MediaPackage, ALB, NLB, Lambda URL, EC2/custom, API Gateway). <b>Glacier:</b> es <b>archivado</b> con recuperaci&oacute;n de minutos u horas, incompatible con baja latencia.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> afirman lo contrario a cada punto (EC2 mejor origen, EFS directo a CloudFront, Glacier de baja latencia), todo falso.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Or&iacute;genes nativos de CloudFront no incluyen EFS. Glacier = archivado, nunca "servir r&aacute;pido".</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html">docs.aws or&iacute;genes CloudFront</a></div>'
        ),
    ),
    card(
        question="Necesitas un framework <b>simple y nativo de AWS</b> para definir Lambda + API Gateway + DynamoDB en un solo stack, compartir config (memoria, timeouts) y desplegar todo como una <b>&uacute;nica entidad versionada</b>. &iquest;Qu&eacute; usas?",
        options=[
            "AWS SAM (Serverless Application Model)",
            "AWS CloudFormation puro",
            "Serverless Framework (de terceros)",
            "AWS Systems Manager",
        ],
        correct=0,
        key="dva07-q21-sam-serverless",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; AWS SAM.</div>'
            '<p><b>AWS SAM</b> es un framework open source de AWS con <b>sintaxis abreviada</b> (YAML) para funciones, APIs y tablas. En el <b>deploy</b> transforma esa sintaxis a CloudFormation, que provisiona todo. Simplifica definir Lambda + API Gateway + DynamoDB como un solo conjunto versionado, compartiendo propiedades comunes.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CloudFormation puro:</b> funciona, pero es m&aacute;s verboso; SAM es la capa <b>simplificada</b> pensada para serverless.</li>'
            '<li><b>Serverless Framework:</b> es de <b>terceros</b>, no nativo de AWS.</li>'
            '<li><b>Systems Manager:</b> gesti&oacute;n/operaci&oacute;n de recursos (patching, config), no es un framework de despliegue de apps.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato</span>SAM se apoya en CloudFormation por debajo: un <code>Transform: AWS::Serverless-2016-10-31</code> lo expande.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html">docs.aws SAM</a><br>'
            '<a href="https://tutorialsdojo.com/aws-serverless-application-model-sam/">tutorialsdojo SAM</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; relaci&oacute;n tiene <b>AWS SAM</b> con <b>CloudFormation</b> al desplegar?",
        options=[
            "SAM es una extensi&oacute;n de CloudFormation: su sintaxis abreviada se expande a CloudFormation v&iacute;a el Transform AWS::Serverless-2016-10-31 durante el deploy",
            "SAM y CloudFormation no tienen relaci&oacute;n; SAM despliega por su cuenta",
            "CloudFormation es una capa encima de SAM",
            "SAM reemplaza a CloudFormation y no lo usa por debajo",
        ],
        correct=0,
        key="dva07-q21-sam-transform-cfn",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; SAM se expande a CloudFormation v&iacute;a Transform.</div>'
            '<p><b>SAM</b> es una <b>extensi&oacute;n</b> de CloudFormation. La plantilla declara <code>Transform: AWS::Serverless-2016-10-31</code>; en el deploy, ese transform <b>expande</b> los recursos abreviados de SAM (<code>AWS::Serverless::Function</code>, etc.) a recursos completos de CloudFormation, que es quien realmente provisiona. Por eso obtienes las capacidades de CloudFormation (change sets, rollback, stacks) con menos YAML.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> SAM s&iacute; usa CloudFormation por debajo (no despliega solo, no lo reemplaza), y la jerarqu&iacute;a es SAM encima de CloudFormation, no al rev&eacute;s.</p>'
            '<div class="extra"><span class="h">Dato</span>Como es CloudFormation por debajo, puedes mezclar recursos SAM y recursos CloudFormation normales en la misma plantilla.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html">docs.aws SAM spec</a></div>'
        ),
    ),
    card(
        question="Debes integrar un directorio <b>LDAP on-premises</b> con AWS IAM, pero el identity store <b>no es compatible con SAML 2.0</b>. &iquest;Cu&aacute;l es la soluci&oacute;n m&aacute;s adecuada?",
        options=[
            "Un custom identity broker on-premises que use STS para emitir credenciales temporales",
            "Una pol&iacute;tica IAM que referencie los identificadores LDAP y credenciales AWS",
            "AWS IAM Identity Center para gestionar el acceso con LDAP",
            "Crear IAM roles que roten las credenciales cuando cambien las de LDAP",
        ],
        correct=0,
        key="dva07-q23-custom-identity-broker",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; custom identity broker + STS.</div>'
            '<p>Si el identity store <b>no</b> soporta SAML 2.0, construyes una <b>aplicaci&oacute;n identity broker</b>: autentica al usuario contra tu LDAP/AD y luego llama a <b>STS</b> (<code>AssumeRole</code> o <code>GetFederationToken</code>) para obtener <b>credenciales temporales</b> de AWS (access key, secret, session token) que la app usa y renueva al expirar.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Solo una pol&iacute;tica IAM:</b> no integra LDAP; necesitas SAML, STS o un broker.</li>'
            '<li><b>IAM Identity Center:</b> su conexi&oacute;n a un <b>IdP externo de terceros</b> se hace v&iacute;a <b>SAML 2.0</b>; el escenario dice que el store <b>no</b> es SAML-compatible, as&iacute; que no lo puedes conectar como IdP externo. (Identity Center tambi&eacute;n tiene un store propio y puede usar AWS Managed Microsoft AD, pero eso no aplica a un LDAP externo no-SAML.)</li>'
            '<li><b>Rotar IAM credentials manualmente:</b> no es una integraci&oacute;n real ni &oacute;ptima; se resuelve con STS/broker.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"no compatible con SAML" + on-prem? &rarr; <b>custom identity broker + STS</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_federated-users.html">docs.aws federated users</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),
    card(
        question="En un custom identity broker, &iquest;qu&eacute; llamadas de <b>STS</b> se usan para obtener credenciales temporales de AWS y qu&eacute; devuelven?",
        options=[
            "AssumeRole o GetFederationToken; devuelven access key, secret key y session token temporales",
            "GetCallerIdentity; devuelve credenciales permanentes",
            "CreateUser + CreateAccessKey; devuelven claves de larga duraci&oacute;n",
            "AssumeRoleWithSAML unicamente; requiere que el store sea SAML",
        ],
        correct=0,
        key="dva07-q23-sts-assumerole-federation",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; AssumeRole o GetFederationToken.</div>'
            '<p>El broker, tras autenticar al usuario contra el LDAP/AD, llama a <b>STS</b>: <code>AssumeRole</code> o <code>GetFederationToken</code>. Ambas devuelven <b>credenciales temporales</b> (access key ID, secret access key y <b>session token</b>) con expiraci&oacute;n; la app las cachea y pide unas nuevas al vencer.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>GetCallerIdentity:</b> solo dice qui&eacute;n eres (identidad de la llamada), no emite credenciales.</li>'
            '<li><b>CreateUser + CreateAccessKey:</b> crea credenciales <b>permanentes</b> de IAM, justo lo que se quiere evitar (deben ser temporales).</li>'
            '<li><b>AssumeRoleWithSAML:</b> requiere un IdP <b>SAML</b>; el escenario dice que el store <b>no</b> es SAML, as&iacute; que no aplica.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Credenciales temporales &rarr; STS (AssumeRole / GetFederationToken). SAML disponible &rarr; AssumeRoleWithSAML.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html">docs.aws credenciales temporales</a></div>'
        ),
    ),
    card(
        question="Necesitas consultar con la <b>misma partition key</b> pero una <b>sort key alterna</b> y con <b>strong consistency</b>. La tabla <b>ya existe</b> con datos. &iquest;Qu&eacute; haces?",
        options=[
            "Crear una nueva tabla con un LSI (misma PK, sort key alterna) y migrar los datos",
            "A&ntilde;adir un LSI a la tabla existente",
            "Crear un GSI con la misma partition key y la sort key alterna",
            "Crear un GSI usando la sort key alterna como atributo proyectado",
        ],
        correct=0,
        key="dva07-q26-lsi-new-table",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; nueva tabla con LSI + migrar datos.</div>'
            '<p>El requisito (<b>misma partition key</b> + <b>sort key alterna</b> + <b>strong consistency</b>) apunta a un <b>Local Secondary Index (LSI)</b>: un LSI comparte la PK de la tabla, ofrece una sort key distinta y <b>s&iacute;</b> soporta lecturas fuertemente consistentes. Pero los LSI <b>solo se crean junto con la tabla</b>: no puedes a&ntilde;adir un LSI a una tabla existente. Por eso hay que <b>crear una tabla nueva</b> con el LSI y <b>migrar</b> los datos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>A&ntilde;adir LSI a la tabla existente:</b> imposible; los LSI se definen al crear la tabla y no se pueden agregar despu&eacute;s.</li>'
            '<li><b>GSI (cualquiera de las dos opciones):</b> un GSI solo da <b>eventual</b> consistency, no cumple el requisito de strong consistency. Adem&aacute;s, aqu&iacute; se mantiene la misma PK, que es el caso de LSI.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Misma PK + sort key alterna + strong consistency &rarr; <b>LSI</b>. Y LSI = <b>solo al crear la tabla</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html">docs.aws LSI</a><br>'
            '<a href="https://tutorialsdojo.com/global-secondary-index-vs-local-secondary-index/">tutorialsdojo GSI vs LSI</a></div>'
        ),
    ),
    card(
        question="Sobre los &iacute;ndices secundarios de DynamoDB: &iquest;cu&aacute;l se puede <b>a&ntilde;adir o borrar en cualquier momento</b> y cu&aacute;l solo se crea <b>junto con la tabla</b>?",
        options=[
            "GSI: en cualquier momento. LSI: solo al crear la tabla",
            "LSI: en cualquier momento. GSI: solo al crear la tabla",
            "Ambos se pueden a&ntilde;adir en cualquier momento",
            "Ambos solo se crean junto con la tabla",
        ],
        correct=0,
        key="dva07-q26-gsi-vs-lsi-lifecycle",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; GSI cualquier momento, LSI solo al crear.</div>'
            '<p>Los <b>GSI</b> se pueden <b>crear y eliminar en cualquier momento</b> sobre una tabla existente. Los <b>LSI</b> deben definirse <b>al crear la tabla</b> y no se pueden a&ntilde;adir ni borrar despu&eacute;s. Esta restricci&oacute;n del ciclo de vida es clave y suele decidir la respuesta en escenarios de "tabla ya existente".</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> las opciones que igualan ambos &iacute;ndices o invierten los roles ignoran que solo el LSI est&aacute; atado a la creaci&oacute;n de la tabla.</p>'
            '<div class="extra"><span class="h">Dato</span>Por eso, si te piden sort key alterna en una tabla existente y se acepta eventual consistency, la salida pr&aacute;ctica suele ser un <b>GSI</b>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html">docs.aws secondary indexes</a></div>'
        ),
    ),

    # ================= Q29: X-Ray annotations in subsegment =================
    card(
        question="En X-Ray quieres que la <b>llamada downstream a RDS</b> (incluida la <b>query SQL</b>) quede registrada como una unidad de trabajo propia y adem&aacute;s <b>buscable con filter expressions</b>. &iquest;D&oacute;nde la registras y con qu&eacute; tipo de dato?",
        options=[
            "Annotations en el subsegment del segment document",
            "Annotations en el segment (el request principal de tu app)",
            "Metadata en el subsegment",
            "Metadata en el segment",
        ],
        correct=0,
        key="dva07-q29-annotations-subsegment",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; annotations en el subsegment.</div>'
            '<p>Dos decisiones: <b>d&oacute;nde</b> (segment vs subsegment) y <b>qu&eacute; dato</b> (annotation vs metadata).</p>'
            '<p><b>D&oacute;nde:</b> las llamadas <b>downstream</b> (a AWS, HTTP y bases SQL) se registran en <b>subsegments</b>. Como la llamada a RDS es downstream, va en un <b>subsegment</b>, que es donde vive el objeto <code>sql</code> con la query. Registrarla en el segment (el request principal) no captura la llamada a RDS como unidad de trabajo propia.</p>'
            '<p><b>Qu&eacute; dato:</b> para poder <b>buscar/filtrar</b> necesitas <b>annotations</b> (indexadas). La metadata no se indexa, as&iacute; que no se puede filtrar.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Annotations en el segment:</b> una annotation en el segment tambi&eacute;n ser&iacute;a buscable (X-Ray indexa annotations en segment o subsegment), pero el segment representa el <b>request principal de tu app</b>, no la llamada a RDS. Para registrar la llamada downstream como unidad propia debes usar su <b>subsegment</b>.</li>'
            '<li><b>Metadata (subsegment o segment):</b> la metadata <b>no</b> se indexa, as&iacute; que no se puede buscar con filter expressions. Sirve para datos que quieres guardar pero no filtrar.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Buscar/filtrar &rarr; <b>annotation</b> (indexada, sea en segment o subsegment). Llamada downstream (RDS/HTTP/SQL) &rarr; su <b>subsegment</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html#xray-concepts-annotations">docs.aws annotations vs metadata</a><br>'
            '<a href="https://tutorialsdojo.com/aws-x-ray/">tutorialsdojo X-Ray</a></div>'
        ),
    ),
    card(
        question="En X-Ray, &iquest;cu&aacute;l es la diferencia entre <b>annotations</b> y <b>metadata</b>?",
        options=[
            "Annotations se indexan y sirven para filter expressions; metadata no se indexa",
            "Metadata se indexa y sirve para filtrar; annotations no",
            "Ambas se indexan y ambas sirven para filtrar",
            "Ninguna se indexa; ambas son solo para visualizaci&oacute;n",
        ],
        correct=0,
        key="dva07-q29-annotation-vs-metadata",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; annotations indexadas (filtrables); metadata no.</div>'
            '<p><b>Annotations</b>: pares clave-valor simples que X-Ray <b>indexa</b> (hasta 50 por traza) y que puedes usar en <b>filter expressions</b> y en <code>GetTraceSummaries</code>. <b>Metadata</b>: pares clave-valor de cualquier tipo (objetos, listas) que <b>no</b> se indexan; los guardas en la traza pero <b>no</b> puedes buscarlos por ellos.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten los roles o niegan la indexaci&oacute;n de annotations. La regla fija: si necesitas <b>buscar</b>, usa annotation.</p>'
            '<div class="extra"><span class="h">Dato</span>L&iacute;mite: hasta 50 annotations indexadas por traza.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html">docs.aws X-Ray concepts</a></div>'
        ),
    ),

    # ================= Q34: ECS random task placement strategy =================
    card(
        question="En ECS quieres colocar tareas en instancias con recursos suficientes, respetando las constraints (impl&iacute;citas o expl&iacute;citas), con la <b>menor configuraci&oacute;n</b> posible. &iquest;Qu&eacute; task placement strategy usas?",
        options=[
            "random",
            "binpack",
            "spread con instanceId y host",
            "spread con placement constraints personalizadas",
        ],
        correct=0,
        key="dva07-q34-ecs-random-placement",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; random.</div>'
            '<p>La estrategia <b>random</b> coloca las tareas al azar pero <b>sigue respetando</b> las constraints y asegura que la instancia tenga recursos suficientes. No requiere par&aacute;metros extra, as&iacute; que es la de <b>menor configuraci&oacute;n</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>binpack:</b> coloca por menor CPU/memoria disponible para usar menos instancias; requiere especificar el campo (CPU o memory), o sea m&aacute;s config.</li>'
            '<li><b>spread con instanceId/host:</b> distribuye uniformemente pero exige indicar el atributo, m&aacute;s configuraci&oacute;n que random. Ojo: spread across-AZ es el <b>default impl&iacute;cito de un servicio</b> (CreateService), pero como <b>estrategia elegida expl&iacute;citamente</b> necesita un campo, as&iacute; que sigue siendo m&aacute;s config que random.</li>'
            '<li><b>spread con constraints personalizadas:</b> a&ntilde;ade reglas extra, todav&iacute;a m&aacute;s configuraci&oacute;n.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"menor configuraci&oacute;n"? &rarr; <b>random</b>. &iquest;"menos instancias / optimizar recursos"? &rarr; binpack. &iquest;"alta disponibilidad"? &rarr; spread.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html">docs.aws task placement strategies</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-elastic-container-service-amazon-ecs/">tutorialsdojo ECS</a></div>'
        ),
    ),
    card(
        question="En ECS, &iquest;para qu&eacute; sirve cada task placement strategy: <b>binpack</b>, <b>spread</b> y <b>random</b>?",
        options=[
            "binpack: minimiza instancias (empaca por CPU/mem); spread: distribuye uniformemente (alta disponibilidad); random: al azar honrando constraints",
            "binpack: distribuye uniformemente; spread: empaca; random: usa m&aacute;s instancias",
            "los tres minimizan el n&uacute;mero de instancias",
            "binpack maximiza disponibilidad; spread minimiza costo; random balancea CPU",
        ],
        correct=0,
        key="dva07-q34-strategy-purposes",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; binpack empaca, spread distribuye, random al azar.</div>'
            '<p><b>binpack:</b> coloca tareas en las instancias con <b>menos</b> CPU/memoria disponible para <b>usar el menor n&uacute;mero de instancias</b> (optimiza costo/utilizaci&oacute;n). <b>spread:</b> distribuye las tareas <b>uniformemente</b> seg&uacute;n un atributo (ej. Availability Zone) para maximizar la <b>disponibilidad</b>. <b>random:</b> coloca al <b>azar</b>, honrando constraints y recursos, con m&iacute;nima configuraci&oacute;n.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten los prop&oacute;sitos de binpack/spread o afirman que los tres minimizan instancias (solo binpack lo hace).</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Costo/menos instancias &rarr; binpack. Disponibilidad &rarr; spread. Simplicidad &rarr; random.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-strategies.html">docs.aws placement strategies</a></div>'
        ),
    ),
    card(
        question="Ya tienes una plantilla SAM y el c&oacute;digo Lambda en local. &iquest;Cu&aacute;l es el flujo correcto de despliegue de una app SAM?",
        options=[
            "Build en local, empaquetar la app, y desplegar la plantilla desde un bucket S3",
            "Build en una instancia EC2, empaquetar, y desplegar desde CodePipeline",
            "Build con el AWS SDK para CodeDeploy, empaquetar, y desplegar desde EC2",
            "Desplegar directamente sin build ni empaquetado",
        ],
        correct=0,
        key="dva07-q37-sam-deploy-workflow",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; build local &rarr; package &rarr; deploy desde S3.</div>'
            '<p>Flujo t&iacute;pico de SAM: <b>sam build</b> compila el c&oacute;digo y prepara los artefactos <b>en local</b>; luego se <b>empaqueta</b> (sube artefactos a un bucket <b>S3</b> y genera la plantilla con referencias a S3); finalmente <b>sam deploy</b> usa esa plantilla en S3 para que CloudFormation cree/actualice los recursos. (Hoy <b>sam deploy</b> hace el package impl&iacute;citamente.)</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Build en EC2 / deploy desde CodePipeline:</b> no se requiere EC2; CodePipeline es CI/CD opcional, no un paso obligatorio del flujo local.</li>'
            '<li><b>Build con el SDK de CodeDeploy:</b> ese SDK es para operar CodeDeploy, no para construir SAM. El build es con la SAM CLI.</li>'
            '<li><b>Deploy sin build/package:</b> falta preparar y subir artefactos; CloudFormation necesita los artefactos en S3.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato</span>CloudFormation referencia los artefactos <b>desde S3</b>; por eso el empaquetado los sube ah&iacute; primero.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-deploying.html">docs.aws SAM deploying</a><br>'
            '<a href="https://tutorialsdojo.com/aws-serverless-application-model-sam/">tutorialsdojo SAM</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; hace cada comando de la SAM CLI: <b>sam build</b>, <b>sam package</b>, <b>sam deploy</b> y <b>sam publish</b>?",
        options=[
            "build: compila artefactos en local; package: sube artefactos a S3 y genera plantilla con refs S3; deploy: crea/actualiza el stack (hace package impl&iacute;cito); publish: publica al Serverless Application Repository",
            "build: despliega el stack; package: publica al repositorio; deploy: compila; publish: sube a S3",
            "los cuatro despliegan el stack de formas equivalentes",
            "build: sube a S3; deploy: solo valida la plantilla; publish: crea el stack",
        ],
        correct=0,
        key="dva07-q37-sam-commands",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; build, package, deploy, publish (cada uno su rol).</div>'
            '<p><b>sam build:</b> compila el c&oacute;digo y prepara artefactos en <code>.aws-sam/</code> (local). <b>sam package:</b> sube esos artefactos a un bucket <b>S3</b> y devuelve una plantilla con las referencias reemplazadas por ubicaciones en S3. <b>sam deploy:</b> crea/actualiza el stack v&iacute;a CloudFormation (y hoy hace el <b>package impl&iacute;citamente</b>). <b>sam publish:</b> publica la app al <b>Serverless Application Repository</b> (no despliega a tu cuenta).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> mezclan/invierten las funciones (deploy no compila, publish no crea tu stack, build no sube a S3), o dicen que los cuatro despliegan igual, lo cual es falso.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>publish = Serverless App Repository, NO despliegue. deploy = crea el stack (empaqueta solo).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference.html">docs.aws SAM CLI</a></div>'
        ),
    ),
    card(
        question="Varios usuarios actualizan el <b>mismo item</b> de DynamoDB concurrentemente y unos sobrescriben los cambios de otros. Quieres que una escritura solo tenga &eacute;xito si el item no cambi&oacute; desde que lo le&iacute;ste. &iquest;Qu&eacute; estrategia usas?",
        options=[
            "Optimistic locking con un atributo de n&uacute;mero de versi&oacute;n",
            "Pessimistic locking con un atributo de n&uacute;mero de versi&oacute;n",
            "DynamoDB global tables con optimistic locking",
            "DynamoDB global tables con pessimistic locking",
        ],
        correct=0,
        key="dva07-q41-optimistic-locking",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; optimistic locking con n&uacute;mero de versi&oacute;n.</div>'
            '<p><b>Optimistic locking</b>: cada item tiene un atributo de <b>versi&oacute;n</b>. Al leer, guardas la versi&oacute;n; al escribir, la operaci&oacute;n solo tiene &eacute;xito si la versi&oacute;n en el servidor <b>no cambi&oacute;</b>. Si otro la modific&oacute; antes, tu update falla y reintentas. As&iacute; evitas sobrescribir cambios ajenos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Pessimistic locking:</b> DynamoDB no tiene un <b>bloqueo de item nativo integrado</b>; el mecanismo del DynamoDBMapper para este caso se llama <b>optimistic</b> locking (con versi&oacute;n). Se puede emular un patr&oacute;n pessimistic con <code>TransactWriteItems</code> o un lock client, pero no es lo que aplica aqu&iacute;.</li>'
            '<li><b>Global tables (con cualquiera de las dos):</b> las global tables usan reconciliaci&oacute;n <b>"last writer wins"</b>; con ellas el locking por versi&oacute;n <b>no</b> funciona como esperas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Concurrencia sobre el mismo item &rarr; <b>optimistic locking + versi&oacute;n</b>. Y ojo: global tables = last-writer-wins.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.OptimisticLocking.html">docs.aws optimistic locking</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),
    card(
        question="&iquest;Por qu&eacute; el <b>optimistic locking</b> por n&uacute;mero de versi&oacute;n <b>no funciona como esperas</b> con <b>DynamoDB global tables</b>?",
        options=[
            "Las global tables reconcilian escrituras concurrentes con 'last writer wins', que puede sobrescribir sin comprobar la versi&oacute;n",
            "Las global tables bloquean la escritura hasta validar la versi&oacute;n en todas las regiones",
            "Las global tables no permiten escrituras concurrentes",
            "El optimistic locking solo funciona en global tables",
        ],
        correct=0,
        key="dva07-q41-global-tables-lww",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; global tables usan last-writer-wins.</div>'
            '<p>Las <b>global tables</b> son multi-regi&oacute;n activo-activo y reconcilian conflictos con <b>"last writer wins"</b> (gana la escritura con el timestamp m&aacute;s reciente). Una escritura en la regi&oacute;n A puede <b>sobrescribir</b> una escritura concurrente en la regi&oacute;n B <b>sin</b> comprobar el atributo de versi&oacute;n, as&iacute; que el optimistic locking no garantiza lo esperado entre regiones. AWS recomienda manejar conflictos a nivel de aplicaci&oacute;n en ese caso.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> las global tables no bloquean ni validan versi&oacute;n cross-region, s&iacute; permiten escrituras concurrentes, y el optimistic locking no depende de global tables (funciona en tablas normales de una regi&oacute;n).</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;Ves "global tables" + "locking/versi&oacute;n"? Recuerda: last-writer-wins rompe esa expectativa.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables_HowItWorks.html">docs.aws global tables</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, con lecturas <b>fuertemente consistentes</b>: &iquest;cu&aacute;ntas lecturas por segundo cubre <b>1 RCU</b> y de qu&eacute; tama&ntilde;o de item?",
        options=[
            "1 lectura fuertemente consistente/seg de un item de hasta 4 KB",
            "2 lecturas fuertemente consistentes/seg de hasta 4 KB",
            "1 lectura fuertemente consistente/seg de hasta 1 KB",
            "2 lecturas fuertemente consistentes/seg de hasta 8 KB",
        ],
        correct=0,
        key="dva07-q45-rcu-basics",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 1 RCU = 1 lectura fuerte de hasta 4 KB.</div>'
            '<p>Regla base de RCU: <b>1 RCU</b> = <b>1</b> lectura <b>fuertemente consistente</b> por segundo de un item de hasta <b>4 KB</b>, o <b>2</b> lecturas <b>eventualmente</b> consistentes por segundo de hasta 4 KB. Items mayores a 4 KB consumen RCU adicionales en bloques de 4 KB (redondeando hacia arriba).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> las que dicen 1 KB u 8 KB confunden el bloque (es 4 KB); la de "2 lecturas fuertes" corresponde a lecturas <b>eventuales</b>, no fuertes.</p>'
            '<div class="extra"><span class="h">Recordatorio</span>Eventual = el doble de lecturas por RCU que fuerte. WCU en cambio es por bloques de 1 KB.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html">docs.aws provisioned throughput</a></div>'
        ),
    ),
    card(
        question="Una Lambda hace <b>320 lecturas fuertemente consistentes/seg</b> de items de <b>17 KB</b>. &iquest;Cu&aacute;ntos RCU necesitas (valor &oacute;ptimo para bajar costo sin perder rendimiento)?",
        options=["1600", "5440", "800", "3200"],
        correct=0,
        key="dva07-q45-rcu-calc-1600",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 1600 RCU.</div>'
            '<p>C&aacute;lculo para lecturas <b>fuertes</b>:</p>'
            '<ul>'
            '<li>Paso 1: tama&ntilde;o / 4 KB, redondeando arriba &rarr; 17 / 4 = 4.25 &rarr; <b>5</b> bloques.</li>'
            '<li>Paso 2: lecturas/seg x bloques &rarr; 320 x 5 = <b>1600</b> RCU (para fuerte no se divide entre 2).</li>'
            '</ul>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>5440:</b> es 320 x 17, la f&oacute;rmula de <b>WCU</b> (bloques de 1 KB), no de RCU. Sobredimensiona y encarece.</li>'
            '<li><b>800:</b> ser&iacute;a como para lecturas <b>eventuales</b> (1600/2); el escenario pide fuertes, no cumple.</li>'
            '<li><b>3200:</b> no corresponde a ning&uacute;n c&aacute;lculo correcto (doble de lo necesario).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>RCU: divide el tama&ntilde;o entre <b>4 KB</b> y redondea. Fuerte = x1; eventual = /2. WCU: entre <b>1 KB</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html">docs.aws capacity</a><br>'
            '<a href="https://tutorialsdojo.com/calculating-the-required-read-and-write-capacity-unit-for-your-dynamodb-table/">tutorialsdojo c&aacute;lculo RCU/WCU</a></div>'
        ),
    ),
    card(
        question="Un item de <b>17 KB</b>: &iquest;cu&aacute;ntos bloques cuenta para <b>RCU</b> (bloque 4 KB) y cu&aacute;ntos para <b>WCU</b> (bloque 1 KB)?",
        options=[
            "RCU: ceil(17/4)=5 bloques; WCU: ceil(17/1)=17 bloques",
            "RCU: 17 bloques; WCU: 5 bloques",
            "RCU: 4 bloques; WCU: 4 bloques",
            "RCU: 5 bloques; WCU: 5 bloques",
        ],
        correct=0,
        key="dva07-q45-rcu-vs-wcu-blocks",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; RCU 5 bloques (4 KB); WCU 17 bloques (1 KB).</div>'
            '<p>El tama&ntilde;o del bloque difiere: <b>RCU usa bloques de 4 KB</b> (17/4 = 4.25 &rarr; <b>5</b>), y <b>WCU usa bloques de 1 KB</b> (17/1 = <b>17</b>). Por eso, para 320 lecturas fuertes de 17 KB salen 320 x 5 = 1600 RCU; y por eso "320 x 17 = 5440" es en realidad el patr&oacute;n de <b>WCU</b>, no de RCU. Confundir los bloques es el error cl&aacute;sico.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten los bloques (17 para RCU / 5 para WCU) o usan un bloque igual para ambos, lo cual es falso: 4 KB para lectura, 1 KB para escritura.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Lectura &rarr; /4 KB. Escritura &rarr; /1 KB. Si ves 320 x 17 = 5440 en una pregunta de RCU, es la trampa de usar el bloque de WCU.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html">docs.aws capacity</a></div>'
        ),
    ),
    card(
        question="En Elastic Beanstalk corres el <b>X-Ray daemon</b> en las instancias para subir trazas a X-Ray, usando el instance profile por defecto. &iquest;Qu&eacute; managed policy de IAM necesita el daemon para <b>subir datos</b>?",
        options=[
            "AWSXRayDaemonWriteAccess",
            "AWSXrayReadOnlyAccess",
            "AWSXrayFullAccess",
            "AWSXRayElasticBeanstalkWriteAccess",
        ],
        correct=0,
        key="dva07-q47-xray-daemon-policy",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; AWSXRayDaemonWriteAccess.</div>'
            '<p>Para que el <b>X-Ray daemon</b> suba (write) las trazas a X-Ray, necesita la managed policy <b>AWSXRayDaemonWriteAccess</b>, que incluye permiso para subir segmentos y algunos permisos de lectura para las sampling rules. Esta policy ya viene en el instance profile de Elastic Beanstalk.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>AWSXrayReadOnlyAccess:</b> solo lectura; sirve para ver el service map en la consola, no para subir trazas.</li>'
            '<li><b>AWSXrayFullAccess:</b> da acceso amplio (incluye configuraci&oacute;n), pero viola el principio de m&iacute;nimo privilegio y no es la usada por Beanstalk para el daemon.</li>'
            '<li><b>AWSXRayElasticBeanstalkWriteAccess:</b> no existe como managed policy.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Daemon = <b>escribir</b> trazas &rarr; <b>...DaemonWriteAccess</b>. Ver en consola = ReadOnly. Ojo con las may&uacute;sculas: la policy del daemon es "X<b>R</b>ay" (R may&uacute;scula), mientras ReadOnly/FullAccess usan "X<b>r</b>ay" (min&uacute;scula). AWS es inconsistente aqu&iacute;.</div>'
            '<div class="warn"><span class="h">Matiz Elastic Beanstalk</span>La respuesta del examen es <code>AWSXRayDaemonWriteAccess</code> (correcta para el daemon en EC2/general). Pero la doc espec&iacute;fica de Elastic Beanstalk referencia <code>AWSXrayWriteOnlyAccess</code>, que su instance profile ya incluye. Si ves ambas en un examen de EB, la de Beanstalk documentada es <code>AWSXrayWriteOnlyAccess</code>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-permissions.html">docs.aws X-Ray permissions</a><br>'
            '<a href="https://tutorialsdojo.com/aws-x-ray/">tutorialsdojo X-Ray</a></div>'
        ),
    ),
    card(
        question="Para X-Ray, &iquest;qu&eacute; managed policy usas para (a) solo ver el service map en la consola y (b) configurar encryption y sampling rules?",
        options=[
            "(a) AWSXrayReadOnlyAccess para ver; (b) AWSXrayFullAccess para configurar encryption/sampling",
            "(a) AWSXrayFullAccess para ver; (b) AWSXrayReadOnlyAccess para configurar",
            "(a) AWSXRayDaemonWriteAccess para ver; (b) AWSXrayReadOnlyAccess para configurar",
            "una sola policy cubre ambos: AWSXRayDaemonWriteAccess",
        ],
        correct=0,
        key="dva07-q47-readonly-vs-full",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; ReadOnly para ver; FullAccess para configurar.</div>'
            '<p><b>AWSXrayReadOnlyAccess:</b> permisos de <b>solo lectura</b>, suficientes para ver service maps y trazas en la consola. <b>AWSXrayFullAccess:</b> acceso amplio que incluye <b>configurar</b> encryption key settings y sampling rules (las policies de escritura del daemon <b>no</b> incluyen esa configuraci&oacute;n). Para subir trazas usas la de escritura del daemon (<code>AWSXRayDaemonWriteAccess</code>).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten ReadOnly/FullAccess, o usan la policy de escritura del daemon (que no da lectura de consola completa ni configuraci&oacute;n) para tareas que no le corresponden; y ninguna sola policy cubre todo bien bajo m&iacute;nimo privilegio.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Ver &rarr; ReadOnly. Subir trazas (daemon) &rarr; DaemonWriteAccess. Configurar encryption/sampling &rarr; FullAccess.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/xray/latest/devguide/xray-permissions.html">docs.aws X-Ray permissions</a></div>'
        ),
    ),
    card(
        question="En una plantilla CloudFormation con <code>AWS::Lambda::Function</code>, quieres escribir el c&oacute;digo Python <b>inline</b> (unas pocas l&iacute;neas) dentro de la plantilla. &iquest;Qu&eacute; par&aacute;metro usas?",
        options=[
            "ZipFile (dentro de la propiedad Code)",
            "Code (directamente, pegando el c&oacute;digo)",
            "Handler",
            "CodeUri",
        ],
        correct=0,
        key="dva07-q48-cfn-zipfile-inline",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; ZipFile (bajo Code).</div>'
            '<p>En <code>AWS::Lambda::Function</code>, la propiedad <b>Code</b> es el contenedor del paquete de despliegue. Para c&oacute;digo <b>inline</b> (solo Node.js y Python) usas <b>Code.ZipFile</b>: CloudFormation toma ese texto, lo pone en un archivo <code>index</code> y lo comprime como paquete de despliegue (de ah&iacute; el nombre "ZipFile", no porque acepte un .zip).</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Code (a secas):</b> es la propiedad <b>padre</b>; el c&oacute;digo inline va en su sub-propiedad <b>ZipFile</b>.</li>'
            '<li><b>Handler:</b> especifica la funci&oacute;n de entrada (m&eacute;todo a invocar), no el c&oacute;digo. Adem&aacute;s aqu&iacute; es propiedad de SAM/Lambda distinta.</li>'
            '<li><b>CodeUri:</b> es de <b>AWS SAM</b> (AWS::Serverless::Function) y apunta a una ruta/URL en S3, no c&oacute;digo inline.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato</span>ZipFile inline solo aplica a Node.js y Python; otros runtimes requieren el paquete en S3.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html">docs.aws Lambda Code (ZipFile)</a><br>'
            '<a href="https://tutorialsdojo.com/aws-cloudformation/">tutorialsdojo CloudFormation</a></div>'
        ),
    ),
    card(
        question="&iquest;A qu&eacute; recurso pertenece cada propiedad: <code>Code</code> (con ZipFile/S3Bucket) y <code>CodeUri</code>?",
        options=[
            "Code -> AWS::Lambda::Function (CloudFormation); CodeUri -> AWS::Serverless::Function (SAM)",
            "Code -> SAM; CodeUri -> CloudFormation",
            "ambas pertenecen a CloudFormation",
            "ambas pertenecen a SAM",
        ],
        correct=0,
        key="dva07-q48-code-vs-codeuri",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Code = CloudFormation; CodeUri = SAM.</div>'
            '<p><b>Code</b> (con sub-propiedades como <code>ZipFile</code>, <code>S3Bucket</code>, <code>S3Key</code>, <code>ImageUri</code>) pertenece al recurso <b>AWS::Lambda::Function</b> de <b>CloudFormation</b>. <b>CodeUri</b> pertenece a <b>AWS::Serverless::Function</b> de <b>AWS SAM</b> y apunta a la ubicaci&oacute;n del c&oacute;digo (ruta local o S3). Confundirlas es un error t&iacute;pico de examen.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten la pertenencia o meten ambas en el mismo framework; cada una es de un recurso distinto (CFN vs SAM).</p>'
            '<div class="extra"><span class="h">Dato</span>SAM tambi&eacute;n tiene <code>InlineCode</code> (equivalente a Code.ZipFile) en AWS::Serverless::Function.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html">docs.aws SAM function</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, &iquest;cu&aacute;nto cubre <b>1 WCU</b> y c&oacute;mo calculas las WCU para <b>10 escrituras/seg</b> de items de <b>2 KB</b>?",
        options=[
            "1 WCU = 1 escritura/seg de hasta 1 KB; 10 x 2 = 20 WCU",
            "1 WCU = 1 escritura/seg de hasta 4 KB; 10 x 1 = 10 WCU",
            "1 WCU = 2 escrituras/seg de hasta 1 KB; 10 WCU",
            "1 WCU = 1 escritura/seg de hasta 2 KB; 10 WCU",
        ],
        correct=0,
        key="dva07-q50-wcu-calc",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 1 WCU = 1 escritura de hasta 1 KB; 20 WCU.</div>'
            '<p><b>1 WCU</b> = <b>1</b> escritura por segundo de un item de hasta <b>1 KB</b>. Items mayores consumen WCU en bloques de 1 KB (redondeando arriba). Para 2 KB: ceil(2/1) = 2 WCU por escritura. Con 10 escrituras/seg: 10 x 2 = <b>20 WCU</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> usar 4 KB o 2 KB como bloque de WCU es error (ese 4 KB es para RCU). WCU no duplica como el eventual read.</p>'
            '<div class="extra"><span class="h">Recordatorio</span>WCU = bloques de <b>1 KB</b>. RCU = bloques de <b>4 KB</b>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html">docs.aws capacity</a></div>'
        ),
    ),
    card(
        question="Para <b>20 lecturas eventualmente consistentes/seg</b> de items de <b>2 KB</b> en DynamoDB, &iquest;cu&aacute;ntos RCU necesitas?",
        options=["10", "20", "5", "40"],
        correct=0,
        key="dva07-q50-eventual-rcu-calc",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 10 RCU.</div>'
            '<p>C&aacute;lculo para lecturas <b>eventuales</b>:</p>'
            '<ul>'
            '<li>Paso 1: tama&ntilde;o / 4 KB, redondeando arriba &rarr; 2 / 4 = 0.5 &rarr; <b>1</b> bloque.</li>'
            '<li>Paso 2: lecturas/seg x bloques &rarr; 20 x 1 = 20. Como es <b>eventual</b>, se divide entre 2 &rarr; <b>10</b> RCU.</li>'
            '</ul>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>20</b> ser&iacute;a con lecturas <b>fuertes</b> (no se divide). <b>5</b> y <b>40</b> no salen del c&aacute;lculo (uno es la mitad de m&aacute;s, otro corresponde a transaccional).</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Eventual &rarr; divide entre 2 al final. Un item &lt; 4 KB igual cuenta como 1 bloque.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html">docs.aws read/write capacity</a><br>'
            '<a href="https://tutorialsdojo.com/calculating-the-required-read-and-write-capacity-unit-for-your-dynamodb-table/">tutorialsdojo c&aacute;lculo RCU/WCU</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, &iquest;c&oacute;mo cambia el costo de capacidad para operaciones <b>transaccionales</b> (TransactGetItems / TransactWriteItems) frente a lecturas fuertes / escrituras normales?",
        options=[
            "Las transaccionales consumen el DOBLE: una lectura transaccional = 2x una lectura fuerte; una escritura transaccional = 2x una escritura normal",
            "Consumen la mitad que las normales",
            "Consumen lo mismo que las lecturas eventuales",
            "No consumen capacidad porque son at&oacute;micas",
        ],
        correct=0,
        key="dva07-q50-transactional-cost",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; transaccional = el doble.</div>'
            '<p>Las operaciones <b>transaccionales</b> cuestan <b>el doble</b>: una <b>lectura transaccional</b> consume 2 veces lo de una lectura <b>fuertemente consistente</b>, y una <b>escritura transaccional</b> consume 2 veces lo de una escritura normal (DynamoDB hace preparaci&oacute;n y commit en dos fases). Por eso, en un c&aacute;lculo, "40 RCU/WCU" suele salir cuando el escenario es transaccional, no eventual ni fuerte simple.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no cuestan la mitad, no equivalen a eventual (eventual es la mitad de fuerte, lo opuesto), y por supuesto s&iacute; consumen capacidad.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Eventual = mitad de fuerte. Transaccional = doble de fuerte/normal. Fuerte/normal = base.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html">docs.aws read/write capacity</a></div>'
        ),
    ),
    card(
        question="Debes cifrar datos <b>en reposo</b> en S3 con una clave de cifrado <b>provista y gestionada por tu empresa</b> (no por AWS), con AES-256. &iquest;Qu&eacute; dos opciones cumplen? (elige el par correcto)",
        options=[
            "SSE-C (server-side con clave provista por el cliente) + cifrado del lado del cliente con tu propia master key",
            "SSE-S3 (claves gestionadas por S3) + SSE-KMS",
            "SSE-KMS + SSL/TLS en tr&aacute;nsito",
            "SSE-S3 + pre-signed URLs",
        ],
        correct=0,
        key="dva07-q57-sse-c-clientside",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; SSE-C + client-side encryption con tu master key.</div>'
            '<p>El requisito clave: la clave la <b>provee y gestiona la empresa</b>, no AWS. Dos formas cumplen:</p>'
            '<ul>'
            '<li><b>SSE-C:</b> server-side encryption donde <b>t&uacute; provees la clave</b> en cada request; S3 cifra/descifra con ella (AES-256) pero no la almacena.</li>'
            '<li><b>Client-side encryption con tu propia master key:</b> ciframos en el cliente <b>antes</b> de subir; t&uacute; gestionas la clave por completo.</li>'
            '</ul>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SSE-S3:</b> las claves las gestiona <b>AWS</b> (S3), no tu empresa. No cumple.</li>'
            '<li><b>SSE-KMS:</b> aunque uses una KMS key tuya (incluso con material importado), las claves las <b>gestiona KMS</b>, no directamente tu empresa. El escenario pide una clave <b>provista y gestionada por ti</b>, as&iacute; que SSE-KMS no cumple ese matiz.</li>'
            '<li><b>SSL/TLS:</b> protege datos <b>en tr&aacute;nsito</b>, no en reposo (y la app ya usa HTTPS).</li>'
            '<li><b>Pre-signed URLs:</b> control de acceso temporal, no cifrado en reposo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"clave gestionada por el cliente/empresa"? &rarr; <b>SSE-C</b> o <b>client-side</b>. &iquest;"gestionada por AWS"? &rarr; SSE-S3/SSE-KMS.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html">docs.aws S3 encryption</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-s3/">tutorialsdojo S3</a></div>'
        ),
    ),
    card(
        question="En el cifrado de S3, &iquest;qui&eacute;n gestiona la clave en cada opci&oacute;n: SSE-S3, SSE-KMS, SSE-C y client-side encryption?",
        options=[
            "SSE-S3: AWS (S3); SSE-KMS: AWS KMS; SSE-C: el cliente la provee en cada request; client-side: el cliente por completo",
            "SSE-S3: el cliente; SSE-KMS: el cliente; SSE-C: AWS; client-side: AWS",
            "las cuatro son gestionadas por AWS",
            "las cuatro son gestionadas por el cliente",
        ],
        correct=0,
        key="dva07-q57-who-manages-key",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; S3/KMS = AWS; SSE-C y client-side = el cliente.</div>'
            '<p><b>SSE-S3:</b> la clave la gestiona <b>S3 (AWS)</b>, transparente. <b>SSE-KMS:</b> la clave vive en <b>AWS KMS</b> (AWS la gestiona, aunque t&uacute; controles pol&iacute;ticas). <b>SSE-C:</b> <b>t&uacute; provees</b> la clave en cada request; S3 cifra/descifra pero <b>no</b> la almacena. <b>Client-side encryption:</b> t&uacute; ciframos antes de subir y gestionas la clave <b>por completo</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten qui&eacute;n gestiona, o dicen que todas son de AWS o todas del cliente, lo cual es falso: el eje es exactamente qui&eacute;n controla la clave.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"clave del cliente/empresa"? &rarr; SSE-C o client-side. &iquest;"AWS gestiona"? &rarr; SSE-S3 o SSE-KMS.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html">docs.aws S3 encryption</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(deck_name="DVA-C02::07", cards=cards, out_path="out/DVA-C02_07.apkg")
