#!/usr/bin/env python3
"""
DVA-C02::04 - Cards built ONLY from the questions the user got INCORRECT on the
Tutorials Dojo set, each decomposed into 2-3 one-concept cards (the same style
as DVA-C02::01-03).

Source incorrect questions:
  Q6  - RCU calculation (eventual consistency)         -> 3 cards
  Q10 - Cross-Region Replication needs versioning       -> 3 cards
  Q13 - Large-file upload to SSE-KMS bucket (multipart) -> 3 cards
  Q14 - CloudFront slow login + HTTP 504                -> 3 cards
  Q15 - DynamoDB conditional writes for bidding         -> 2 cards
  Q17 - Local Secondary Index (LSI)                     -> 3 cards
  Q18 - Kinesis shards = unit of Lambda concurrency     -> 3 cards
  Q21 - Importing a third-party SSL/TLS certificate     -> 2 cards

Spanish explanations, HTML with entities, {{L}} verdict placeholder (never
hardcode the letter), each back refutes every distractor one by one.
"""
from anki_mcq import card, create

cards = [
    # ================= Q6: RCU (eventual consistency) =================
    card(
        question="Tabla DynamoDB, items de <b>3.5 KB</b>, se esperan <b>150 lecturas eventualmente consistentes por segundo</b>. &iquest;Cu&aacute;ntas <b>RCU</b> hay que aprovisionar?",
        options=["150", "75", "300", "600"],
        correct=1,
        key="dva04-q6-rcu-calc",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 75 RCU.</div>'
            '<p><b>RCU = Read Capacity Unit</b> (unidad de capacidad de lectura). M&eacute;todo de AWS:</p>'
            '<ul>'
            '<li><b>Redondear el tama&ntilde;o</b> al siguiente m&uacute;ltiplo de 4 KB: 3.5 KB &rarr; <b>4 KB</b>.</li>'
            '<li><b>Dividir entre 4 KB</b> = unidades por lectura <b>fuerte</b>: 4/4 = <b>1</b>.</li>'
            '<li><b>Dividir entre 2</b> para pasar a <b>eventual</b>: 1/2 = <b>0.5</b> por lectura.</li>'
            '<li><b>Multiplicar</b> por las lecturas/seg: 150 &times; 0.5 = <b>75</b>.</li>'
            '</ul>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>150</b> es el valor <b>fuerte</b> (1 unidad por lectura, sin dividir entre 2). <b>300</b> es el valor <b>transaccional</b> (2 RCU por lectura). <b>600</b> no corresponde a ninguna f&oacute;rmula v&aacute;lida de RCU de lectura aqu&iacute; (ser&iacute;a el doble del transaccional); es un distractor inflado, y adem&aacute;s solo se piden RCU.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Redondea a 4 KB, divide entre 4 KB (fuerte), luego entre 2 (eventual). Transaccional = 2&times; el valor fuerte.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html">docs.aws ddb capacity mode</a><br>'
            '<a href="https://tutorialsdojo.com/calculating-the-required-read-and-write-capacity-unit-for-your-dynamodb-table/">tutorialsdojo RCU/WCU calc</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, &iquest;qu&eacute; representa <b>1 RCU</b> (Read Capacity Unit) para un item de hasta 4 KB?",
        options=[
            "1 lectura fuerte, o 2 lecturas eventuales; una lectura transaccional consume 2 RCU",
            "2 lecturas fuertes o 1 eventual",
            "1 lectura de cualquier tipo sin importar el tama&ntilde;o del item ni el tipo de consistencia",
            "4 lecturas eventuales o 2 fuertes",
        ],
        correct=0,
        key="dva04-q6-rcu-meaning",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 1 fuerte o 2 eventuales; la transaccional cuesta 2 RCU.</div>'
            '<p>Para un item de hasta <b>4 KB</b>: <b>1 RCU</b> = <b>1</b> lectura fuertemente consistente = <b>2</b> lecturas eventualmente consistentes (cada eventual cuesta <b>0.5 RCU</b>). Una lectura <b>transaccional</b> consume <b>2 RCU</b> (o sea, 1 RCU = media lectura transaccional).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> "2 fuertes o 1 eventual" invierte la relaci&oacute;n (las eventuales son m&aacute;s baratas, no m&aacute;s caras). "sin importar el tama&ntilde;o ni el tipo" es falso por partida doble: el <b>tama&ntilde;o</b> pasando de 4 KB consume m&aacute;s RCU (se redondea al siguiente m&uacute;ltiplo de 4 KB), y el <b>tipo</b> cambia el costo (fuerte 1, eventual 0.5, transaccional 2). "4 eventuales o 2 fuertes" duplica los valores reales.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Un item de 8 KB: lectura fuerte = 2 RCU; eventual = 1 RCU; transaccional = 4 RCU.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html">docs.aws provisioned throughput</a></div>'
        ),
    ),
    card(
        question="Items de <b>3.5 KB</b>; se necesitan <b>150 lecturas eventualmente consistentes por segundo</b>. Un compa&ntilde;ero calcul&oacute; <b>150 RCU</b> (deber&iacute;an ser 75). &iquest;Qu&eacute; error de c&aacute;lculo cometi&oacute;?",
        options=[
            "Us&oacute; el conteo de lectura fuerte (1 unidad por item de 4 KB) y no lo dividi&oacute; entre 2 para el modelo eventual",
            "Multiplic&oacute; por 2 por tratarse de lecturas transaccionales",
            "Olvid&oacute; redondear el tama&ntilde;o del item a 4 KB",
            "Us&oacute; un tama&ntilde;o de item de 3.5 KB sin convertirlo a bytes",
        ],
        correct=0,
        key="dva04-q6-rcu-mistake",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; us&oacute; el conteo fuerte y no lo dividi&oacute; entre 2 para el modelo eventual.</div>'
            '<p>M&eacute;todo de AWS: redondea el item a 4 KB (3.5 &rarr; 4), divide entre 4 KB para el conteo <b>fuerte</b> (4/4 = <b>1</b> por lectura) y divide ese resultado <b>entre 2</b> para el <b>eventual</b> (0.5 por lectura): 150 &times; 0.5 = <b>75</b>. Si te quedas en el conteo fuerte (1 por lectura) sin dividir entre 2, obtienes 150 &times; 1 = <b>150</b>. Ese es el error.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Multiplicar por 2 (transaccional):</b> eso dar&iacute;a <b>300</b> (2 RCU por lectura), no 150. No es este error.</li>'
            '<li><b>Olvidar redondear:</b> 3.5 KB ya redondea a 4 KB; el c&aacute;lculo s&iacute; parti&oacute; de 4 KB. Adem&aacute;s, no redondear no produce 150.</li>'
            '<li><b>No convertir a bytes:</b> la f&oacute;rmula trabaja en KB directamente; convertir a bytes no cambia el resultado ni explica el 150.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Regla</span>Eventual = la mitad de RCU que fuerte. M&eacute;todo: redondea a 4 KB, divide entre 4 KB (fuerte), luego entre 2 (eventual). Si tu resultado eventual sale igual al fuerte, olvidaste dividir entre 2.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html#ItemSizeCalculations.Reads">docs.aws item size (reads)</a></div>'
        ),
    ),

    # ================= Q10: Cross-Region Replication =================
    card(
        question="<code>put-bucket-replication</code> falla en un bucket S3 (pero funciona en otros) al configurar <b>Cross-Region Replication (CRR)</b>. &iquest;Causa m&aacute;s probable?",
        options=[
            "S3 Object Lock est&aacute; habilitado en el bucket",
            "El versionado no est&aacute; habilitado en el bucket",
            "El bucket no tiene S3 Transfer Acceleration",
            "El bucket no est&aacute; configurado como sitio web est&aacute;tico",
        ],
        correct=1,
        key="dva04-q10-crr-versioning",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; falta habilitar el versionado.</div>'
            '<p><b>CRR</b> (replicaci&oacute;n entre regiones) copia objetos de forma autom&aacute;tica y as&iacute;ncrona a un bucket en <b>otra regi&oacute;n</b>. Requisito obligatorio: <b>versioning habilitado</b> tanto en origen como en destino. Sin versionado, la API de replicaci&oacute;n falla.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>Object Lock</b> (modelo WORM: escribe-una-vez-lee-muchas) protege contra borrado/sobrescritura pero no afecta la config de CRR. <b>Transfer Acceleration</b> solo acelera subidas/bajadas v&iacute;a edge, no tiene relaci&oacute;n con CRR. El <b>hosting est&aacute;tico</b> convierte el bucket en sitio web y tampoco influye en la replicaci&oacute;n.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Regla mnemot&eacute;cnica: "sin versionado no hay replicaci&oacute;n". Es el requisito que m&aacute;s se olvida.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html">docs.aws S3 replication</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-s3/">tutorialsdojo amazon-s3</a></div>'
        ),
    ),
    card(
        question="&iquest;Cu&aacute;les son los requisitos para habilitar <b>Cross-Region Replication (CRR)</b> en S3?",
        options=[
            "Origen y destino en la MISMA regi&oacute;n, con Object Lock activo",
            "Versionado en origen y destino, buckets en regiones distintas, y permisos para que S3 replique en tu nombre",
            "Solo habilitar versionado en el bucket de origen",
            "Habilitar Transfer Acceleration en ambos buckets",
        ],
        correct=1,
        key="dva04-q10-crr-requirements",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; versionado en ambos, regiones distintas y un rol IAM que permita replicar.</div>'
            '<p>Los tres requisitos de CRR son: (1) <b>versioning</b> habilitado en <b>origen y destino</b>; (2) los buckets en <b>regiones AWS diferentes</b>; (3) un <b>rol IAM</b> que otorgue a S3 permiso para replicar los objetos por ti. La configuraci&oacute;n se agrega en el bucket de <b>origen</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> "misma regi&oacute;n" describir&iacute;a SRR (Same-Region Replication), no CRR, y Object Lock no es requisito. "solo versionado en origen" es insuficiente: el destino tambi&eacute;n lo necesita. "Transfer Acceleration" no interviene en la replicaci&oacute;n.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Origen y destino pueden estar en la MISMA cuenta o en cuentas distintas. Existe tambi&eacute;n <b>SRR</b> (misma regi&oacute;n) con los mismos requisitos de versionado.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-how-setup.html">docs.aws replication setup</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; caracter&iacute;stica de S3 debe activarse <b>antes</b> de poder configurar cualquier tipo de replicaci&oacute;n (CRR o SRR)?",
        options=["Object Lock", "Versioning (versionado)", "Static website hosting", "Transfer Acceleration"],
        correct=1,
        key="dva04-q10-crr-prereq-versioning",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; el versionado.</div>'
            '<p>La replicaci&oacute;n en S3 (tanto CRR entre regiones como SRR en la misma regi&oacute;n) <b>exige versioning</b> en origen y destino, porque S3 replica <b>versiones</b> de objetos. Es lo primero que debes habilitar.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>Object Lock</b> es opcional (WORM, Write Once Read Many: escribir una vez y leer muchas) y no es prerequisito de la replicaci&oacute;n. <b>Static website hosting</b> sirve para servir un sitio, nada que ver con replicaci&oacute;n. <b>Transfer Acceleration</b> optimiza la transferencia por edge, no la replicaci&oacute;n.</p>'
            '<div class="warn"><span class="h">Ojo</span>Una vez que hay objetos replic&aacute;ndose, <b>no puedes suspender</b> el versionado en esos buckets sin romper la replicaci&oacute;n.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html">docs.aws S3 replication</a></div>'
        ),
    ),

    # ================= Q13: Large file to SSE-KMS bucket (multipart) =================
    card(
        question="Subir un archivo <b>grande</b> (100+ GB) con <code>aws s3 cp</code> a un bucket con <b>SSE-KMS</b> da <b>Access Denied</b>, pero archivos peque&ntilde;os s&iacute; suben. &iquest;Qu&eacute; hace el CLI con archivos grandes que causa esto?",
        options=[
            "Comprime el archivo antes de subirlo",
            "Realiza una subida multipart (multipart upload)",
            "Cifra el archivo localmente con kms:Encrypt",
            "Divide el archivo en objetos separados",
        ],
        correct=1,
        key="dva04-q13-multipart",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; el CLI hace una subida multipart.</div>'
            '<p>Para archivos grandes, los comandos <code>aws s3</code> hacen autom&aacute;ticamente un <b>multipart upload</b>: parten el archivo en varias partes y las suben en paralelo. Con SSE-KMS, cada parte reutiliza la misma <b>data key</b>, que S3 debe poder <b>descifrar</b> para seguir cifrando; por eso un multipart cifrado exige permisos de KMS que un upload peque&ntilde;o no ejercita.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> el CLI no comprime ni cifra localmente el objeto (S3 hace el cifrado del lado servidor con la KMS key). Tampoco crea "objetos separados": es un solo objeto ensamblado desde varias partes.</p>'
            '<div class="extra"><span class="h">Dato extra</span>El umbral por defecto del CLI para multipart es <b>8 MB</b> (<code>multipart_threshold</code>), configurable en <code>~/.aws/config</code>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html">docs.aws CLI s3 commands</a></div>'
        ),
    ),
    card(
        question="Un multipart upload a un bucket con <b>SSE-KMS</b> da Access Denied. &iquest;Qu&eacute; permisos de KMS necesita el usuario para que funcione?",
        options=[
            "Solo <code>kms:Encrypt</code>",
            "<code>kms:Decrypt</code> y <code>kms:GenerateDataKey*</code>",
            "Solo <code>kms:GenerateDataKey*</code>",
            "<code>kms:CreateKey</code> y <code>kms:Encrypt</code>",
        ],
        correct=1,
        key="dva04-q13-kms-perms",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; kms:Decrypt + kms:GenerateDataKey*.</div>'
            '<p>Con SSE-KMS, S3 genera una <b>data key</b> desde tu KMS key para cifrar cada parte (por eso <code>kms:GenerateDataKey*</code>). En un multipart, S3 <b>reutiliza la misma data key</b> entre partes: para seguir cifrando las partes siguientes debe <b>descifrar</b> esa data key, y para eso necesita <code>kms:Decrypt</code>. Faltando uno, sale Access Denied solo en archivos grandes.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <code>kms:Encrypt</code> NO es necesario: S3 no cifra datos directamente con la KMS key (solo cifra datos de hasta 4 KB, y S3 usa data keys en su lugar). <b>Solo <code>GenerateDataKey*</code></b> bastar&iacute;a para un <code>PutObject</code> simple (una sola parte), pero en un <b>multipart</b> falta <code>kms:Decrypt</code> para descifrar la data key entre partes, y sin &eacute;l da Access Denied. <code>kms:CreateKey</code> es para crear llaves, irrelevante.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Si un upload peque&ntilde;o funciona pero el grande falla con SSE-KMS &rarr; sospecha que falta <b>kms:Decrypt</b> (necesario por el multipart).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://repost.aws/knowledge-center/s3-large-file-encryption-kms-key">repost.aws large file SSE-KMS</a><br>'
            '<a href="https://tutorialsdojo.com/aws-key-management-service-aws-kms/">tutorialsdojo aws-kms</a></div>'
        ),
    ),
    card(
        question="En un upload a bucket SSE-KMS, &iquest;por qu&eacute; <b>NO</b> se necesita el permiso <code>kms:Encrypt</code>?",
        options=[
            "Porque el cifrado lo hace el cliente, no KMS",
            "Porque S3 genera una data key desde la KMS key para cifrar; kms:Encrypt solo aplica a datos peque&ntilde;os (&le;4 KB)",
            "Porque SSE-KMS no cifra realmente los objetos",
            "Porque kms:Decrypt ya incluye a kms:Encrypt",
        ],
        correct=1,
        key="dva04-q13-why-no-encrypt",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; S3 usa una data key; kms:Encrypt es solo para datos peque&ntilde;os.</div>'
            '<p><code>kms:Encrypt</code> sirve para cifrar directamente peque&ntilde;os bloques de datos (hasta <b>4 KB</b>) con la KMS key. Para objetos S3, en su lugar S3 pide una <b>data key</b> (<code>GenerateDataKey*</code>) y cifra el objeto con ella (envelope encryption), por lo que <code>kms:Encrypt</code> no interviene.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> el cifrado NO lo hace el cliente (es del lado servidor, "SSE"). SSE-KMS s&iacute; cifra los objetos (es su prop&oacute;sito). Y <code>kms:Decrypt</code> no "incluye" a <code>Encrypt</code>: son acciones distintas.</p>'
            '<div class="extra"><span class="h">Concepto</span>Esto es <b>envelope encryption</b>: la KMS key (CMK) cifra la data key, y la data key cifra el objeto.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping">docs.aws envelope encryption</a></div>'
        ),
    ),

    # ================= Q14: CloudFront slow login + 504 =================
    card(
        question="App con CloudFront cuyo <b>origen</b> a veces no responde y devuelve <b>HTTP 504</b> al servir contenido (peticiones GET). &iquest;Qu&eacute; acci&oacute;n costo-eficiente resuelve esos 504?",
        options=[
            "Aumentar el Cache-Control max-age de los objetos",
            "Configurar origin failover con un grupo de or&iacute;genes (primario + secundario)",
            "Desplegar la app en varias regiones con Route 53 latency routing",
            "Crear VPCs en varias regiones unidas por un transit VPC",
        ],
        correct=1,
        key="dva04-q14-origin-failover",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; configurar origin failover.</div>'
            '<p>El <b>HTTP 504</b> (Gateway Timeout) indica que el origen no respondi&oacute; a tiempo. Con un <b>origin group</b> de CloudFront defines un origen <b>primario</b> y uno <b>secundario</b>: si el primario devuelve ciertos c&oacute;digos de error, CloudFront cambia autom&aacute;ticamente al secundario, eliminando esos 504 ocasionales.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> subir <b>max-age</b> mejora el cache hit de objetos est&aacute;ticos, pero no evita que el <b>origen</b> devuelva 504 cuando no responde a tiempo. <b>Multi-regi&oacute;n + Route 53</b> y <b>transit VPC</b> pueden reducir latencia pero con <b>alto costo</b>, y el escenario pide una soluci&oacute;n costo-eficiente.</p>'
            '<div class="extra"><span class="h">Dato extra</span>El origin group hace failover ante c&oacute;digos configurables: <b>400, 403, 404, 416, 429, 500, 502, 503 y 504</b>. Ninguno est&aacute; activo por defecto: eliges cu&aacute;les disparan el failover.</div>'
            '<div class="warn"><span class="h">Ojo</span>El origin failover solo act&uacute;a sobre peticiones <b>GET, HEAD y OPTIONS</b>, no sobre POST. Por eso resuelve 504 de contenido servible por GET, pero no servir&iacute;a para un POST (ej. un login por POST).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/high_availability_origin_failover.html">docs.aws origin failover</a></div>'
        ),
    ),
    card(
        question="En la misma app CloudFront, la queja principal es que el <b>login es lento</b> para usuarios globales. &iquest;Qu&eacute; opci&oacute;n costo-eficiente acerca la autenticaci&oacute;n a los usuarios?",
        options=[
            "Route 53 latency routing a m&uacute;ltiples regiones",
            "Lambda@Edge para ejecutar la autenticaci&oacute;n en ubicaciones cercanas al usuario",
            "Aumentar el TTL de la cach&eacute; de CloudFront",
            "Un transit VPC entre regiones",
        ],
        correct=1,
        key="dva04-q14-lambda-edge",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Lambda@Edge.</div>'
            '<p><b>Lambda@Edge</b> ejecuta funciones Lambda en las <b>ubicaciones edge</b> de CloudFront (cerca del usuario) en respuesta a eventos: viewer request/response y origin request/response. Corriendo la l&oacute;gica de autenticaci&oacute;n en el edge, el login deja de viajar hasta la regi&oacute;n de origen &rarr; menor latencia sin desplegar la app en varias regiones.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>latency routing</b> y <b>transit VPC</b> funcionan pero son caros (m&uacute;ltiples regiones). Subir el <b>TTL</b> solo cachea contenido est&aacute;tico, no acelera la autenticaci&oacute;n din&aacute;mica.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Lambda@Edge = mover c&oacute;mputo al edge para usuarios finales. S3 Object Lambda = transformar objetos en el GET (para servicios), no en el edge.</div>'
            '<div class="warn"><span class="h">Matiz importante</span>Si la autenticaci&oacute;n es solo <b>validar un token</b> ligero (ej. JWT), la herramienta IDEAL es <b>CloudFront Functions</b> (JS ultraligero en viewer request). <b>Lambda@Edge</b> es el correcto cuando la l&oacute;gica necesita red externa, el AWS SDK, el cuerpo de la petici&oacute;n o m&aacute;s CPU/memoria. Aqu&iacute; Lambda@Edge es la respuesta porque CloudFront Functions no est&aacute; entre las opciones.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/lambda/latest/dg/lambda-edge.html">docs.aws Lambda@Edge</a></div>'
        ),
    ),
    card(
        question="Ante logins lentos en CloudFront, &iquest;por qu&eacute; aumentar el <code>Cache-Control max-age</code> NO resuelve el problema?",
        options=[
            "Porque max-age no existe en CloudFront",
            "Porque el problema es la autenticaci&oacute;n din&aacute;mica, no el cacheo de objetos est&aacute;ticos",
            "Porque max-age solo aplica a im&aacute;genes",
            "Porque desactiva el HTTPS",
        ],
        correct=1,
        key="dva04-q14-why-not-cache",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; el cuello de botella es la autenticaci&oacute;n, no el cache.</div>'
            '<p>Subir <b>max-age</b> aumenta el <b>cache hit ratio</b>: m&aacute;s peticiones se sirven desde el edge en vez de ir al origen. Eso ayuda con <b>contenido est&aacute;tico</b>, pero el escenario describe un <b>login lento</b> (proceso din&aacute;mico por usuario) que no se cachea. Por eso es irrelevante aqu&iacute;.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <code>max-age</code> s&iacute; existe y aplica a cualquier objeto (no solo im&aacute;genes). No tiene relaci&oacute;n con activar/desactivar HTTPS.</p>'
            '<div class="extra"><span class="h">Concepto</span>Contenido din&aacute;mico/personalizado (login, carrito) casi nunca se cachea; para acelerarlo mueves c&oacute;mputo al edge (Lambda@Edge) o mejoras el origen.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html">docs.aws CloudFront cache expiration</a></div>'
        ),
    ),

    # ================= Q15: DynamoDB conditional writes (bidding) =================
    card(
        question="App de subastas: cada nueva puja debe ser <b>mayor que la puja actual</b>. &iquest;C&oacute;mo se implementa esto de forma m&aacute;s efectiva en las llamadas a DynamoDB?",
        options=[
            "Habilitar DynamoDB Transactions",
            "Usar conditional writes con una condition expression que valide que la nueva puja &gt; la actual",
            "Usar DynamoDB Streams + Lambda para comparar pujas",
            "Usar optimistic locking",
        ],
        correct=1,
        key="dva04-q15-conditional-writes",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; conditional writes con condition expression.</div>'
            '<p>Por defecto <code>PutItem</code> sobrescribe y <code>UpdateItem</code> hace upsert sin validar el valor previo. Un <b>conditional write</b> solo tiene &eacute;xito si se cumple una <b>condition expression</b> (p. ej. <code>nueva_puja &gt; puja_actual</code>); si no, devuelve error. Es la forma directa y at&oacute;mica de imponer la regla del negocio, ideal cuando varios usuarios pujan a la vez sobre el mismo item.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> <b>Transactions</b> dan ACID multi-item, pero es exagerado y m&aacute;s trabajo para una sola condici&oacute;n. <b>DynamoDB Streams</b> (flujo ordenado de cambios de la tabla) + Lambda reacciona <i>despu&eacute;s</i> del cambio, no impide una puja inv&aacute;lida; adem&aacute;s es engorroso. <b>Optimistic locking</b> solo verifica que el item no cambi&oacute; desde tu &uacute;ltima lectura (version number), no compara valores arbitrarios como "&gt; puja actual".</p>'
            '<div class="extra"><span class="h">Dato extra</span>Una escritura condicional que falla la condici&oacute;n <b>igual consume capacidad</b> (WCU) aunque no escriba nada.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html#WorkingWithItems.ConditionalUpdate">docs.aws conditional writes</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo amazon-dynamodb</a></div>'
        ),
    ),
    card(
        question="Para la regla \"nueva puja &gt; puja actual\", &iquest;por qu&eacute; <b>optimistic locking</b> NO es la soluci&oacute;n adecuada?",
        options=[
            "Porque optimistic locking bloquea la tabla entera",
            "Porque solo verifica que el item no cambi&oacute; desde tu lectura (version), no compara valores como \"&gt; actual\"",
            "Porque optimistic locking no existe en DynamoDB",
            "Porque consume 2 WCU por escritura",
        ],
        correct=1,
        key="dva04-q15-why-not-optimistic",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; solo compara la versi&oacute;n, no valores de negocio.</div>'
            '<p><b>Optimistic locking</b> (con un atributo de <i>version number</i>) garantiza que el item que actualizas es el <b>mismo</b> que le&iacute;ste: si otro lo cambi&oacute; en el intermedio, tu escritura falla. Pero <b>no</b> puede imponer una condici&oacute;n de negocio arbitraria como "el nuevo valor debe ser mayor que el actual". Para eso necesitas una <b>condition expression</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> optimistic locking <b>no bloquea la tabla</b> (es "optimista", sin locks reales). S&iacute; existe en DynamoDB (lo usa el DynamoDBMapper con <code>@DynamoDBVersionAttribute</code>). Y no cuesta fijo 2 WCU: su costo depende del tama&ntilde;o del item; el costo fijo de 2 WCU por item (preparar + confirmar) es de las <b>transacciones</b> (TransactWriteItems), no de optimistic locking.</p>'
            '<div class="extra"><span class="h">Matiz</span>Optimistic locking = "&iquest;cambi&oacute; alguien mi item?". Conditional write = "&iquest;se cumple ESTA condici&oacute;n sobre los valores?".</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.OptimisticLocking.html">docs.aws optimistic locking</a></div>'
        ),
    ),

    # ================= Q17: Local Secondary Index (LSI) =================
    card(
        question="Necesitas consultar <b>una sola partici&oacute;n</b> (por su partition key) con <b>otro sort key</b>, admitiendo lecturas <b>eventuales y fuertes</b>. &iquest;Qu&eacute; usas?",
        options=[
            "Un Global Secondary Index (GSI)",
            "Un Local Secondary Index (LSI), creado junto con la tabla",
            "Un GSI creado despu&eacute;s de la tabla",
            "Un LSI creado despu&eacute;s de la tabla",
        ],
        correct=1,
        key="dva04-q17-lsi-basics",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; un LSI (creado al crear la tabla).</div>'
            '<p>Un <b>LSI</b> (Local Secondary Index) mantiene un <b>sort key alternativo</b> para el <b>mismo partition key</b> de la tabla base. Por eso consulta dentro de <b>una sola partici&oacute;n</b> y es el &uacute;nico &iacute;ndice que permite elegir <b>consistencia fuerte o eventual</b> en las lecturas.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> un <b>GSI</b> (creado antes o despu&eacute;s de la tabla) consulta toda la tabla y <b>solo</b> ofrece consistencia <b>eventual</b>, as&iacute; que no cumple el requisito de lecturas <b>fuertes</b>. Un <b>LSI creado despu&eacute;s</b> es inv&aacute;lido: el LSI debe definirse al crear la tabla.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>Si el requisito menciona <b>strong consistency</b> en un &iacute;ndice &rarr; es <b>LSI</b> (el GSI no lo ofrece).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html">docs.aws LSI</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo amazon-dynamodb</a></div>'
        ),
    ),
    card(
        question="Sobre el <b>momento de creaci&oacute;n</b> de los &iacute;ndices en DynamoDB, &iquest;qu&eacute; es correcto?",
        options=[
            "LSI y GSI se pueden crear en cualquier momento",
            "El LSI solo se crea al crear la tabla; el GSI se puede agregar despu&eacute;s",
            "El LSI se agrega despu&eacute;s; el GSI solo al crear la tabla",
            "Ninguno de los dos se puede crear despu&eacute;s de la tabla",
        ],
        correct=1,
        key="dva04-q17-lsi-creation-time",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; LSI solo al crear la tabla; GSI se puede agregar/quitar despu&eacute;s.</div>'
            '<p>Un <b>LSI</b> debe definirse <b>al momento de crear la tabla</b> y no se puede a&ntilde;adir ni borrar despu&eacute;s. Un <b>GSI</b> s&iacute; se puede crear, modificar o eliminar en una tabla existente.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no es cierto que ambos sean libres en cualquier momento (el LSI no lo es), ni al rev&eacute;s (no es el GSI el restringido), ni que ninguno se pueda crear despu&eacute;s (el GSI s&iacute;).</p>'
            '<div class="extra"><span class="h">Dato extra</span>L&iacute;mites por defecto: hasta <b>5 LSI</b> y <b>20 GSI</b> por tabla. El LSI comparte capacidad con la tabla base; el GSI tiene su propia capacidad.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html">docs.aws secondary indexes</a></div>'
        ),
    ),
    card(
        question="&iquest;Cu&aacute;l es la diferencia clave entre <b>LSI</b> y <b>GSI</b> respecto a alcance de consulta y consistencia?",
        options=[
            "LSI consulta toda la tabla; GSI una sola partici&oacute;n",
            "LSI: misma partition key, una partici&oacute;n, fuerte O eventual. GSI: toda la tabla, solo eventual",
            "Ambos consultan una sola partici&oacute;n con consistencia fuerte",
            "GSI permite consistencia fuerte y LSI no",
        ],
        correct=1,
        key="dva04-q17-lsi-vs-gsi",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; LSI: 1 partici&oacute;n, fuerte/eventual; GSI: toda la tabla, solo eventual.</div>'
            '<p><b>LSI</b>: comparte el partition key de la tabla base, consulta dentro de <b>una partici&oacute;n</b>, y permite lecturas <b>fuertes o eventuales</b>. <b>GSI</b>: tiene su <b>propio</b> partition/sort key, consulta a trav&eacute;s de <b>toda la tabla</b>, y <b>solo</b> ofrece consistencia <b>eventual</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> se invierte quien consulta toda la tabla (es el GSI). No es cierto que ambos sean "una partici&oacute;n + fuerte". Y NO es el GSI el que da consistencia fuerte: es el LSI.</p>'
            '<div class="extra"><span class="h">Regla r&aacute;pida</span>&iquest;Necesitas otra partition key distinta? &rarr; GSI. &iquest;Necesitas otro sort key con la misma partition key y quiz&aacute; lecturas fuertes? &rarr; LSI.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html">docs.aws secondary indexes</a></div>'
        ),
    ),

    # ================= Q18: Kinesis shards = unit of concurrency =================
    card(
        question="Una Lambda procesa un stream de <b>Kinesis Data Streams</b> con <b>100 shards activos</b> (10 s por invocaci&oacute;n, 50 items/seg). &iquest;Qu&eacute; es cierto sobre la concurrencia?",
        options=[
            "La Lambda tendr&aacute; 500 ejecuciones concurrentes",
            "Habr&aacute; como m&aacute;ximo 100 invocaciones concurrentes (1 por shard)",
            "La Lambda se throttlea por exceso de shards",
            "Hay que mergear shards para aumentar la concurrencia",
        ],
        correct=1,
        key="dva04-q18-shards-concurrency",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; a lo sumo 100 invocaciones concurrentes (1 por shard).</div>'
            '<p>Con fuentes <b>poll-based</b> (de sondeo) como Kinesis o DynamoDB Streams, la <b>unidad de concurrencia es el shard</b> (fragmento del stream): Lambda procesa los registros de cada shard <b>en orden</b>, un lote a la vez. Con <b>100 shards</b> &rarr; a lo sumo <b>100</b> invocaciones concurrentes, sin importar cu&aacute;ntos items/seg lleguen.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> "500" sale de aplicar la f&oacute;rmula <b>general</b> de concurrencia (items/seg &times; duraci&oacute;n = 50 &times; 10), que gobierna las fuentes <b>event-driven</b> (API Gateway, S3), pero <b>no</b> los orígenes de sondeo, donde manda el nº de shards. No se throttlea por "exceso de shards" (100 no es excesivo; Lambda escala hasta tu l&iacute;mite). Y para aumentar capacidad se hace <b>split</b> (dividir), no merge (fusionar).</p>'
            '<div class="extra"><span class="h">Dato extra</span>Con <b>parallelization factor</b> puedes correr hasta 10 invocaciones por shard (hasta 10&times; la concurrencia) manteniendo el orden por clave de partici&oacute;n. Lambda puede reportar brevemente algo m&aacute;s que el nº de shards durante reajustes.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html">docs.aws Lambda + Kinesis</a><br>'
            '<a href="https://tutorialsdojo.com/aws-lambda/">tutorialsdojo aws-lambda</a></div>'
        ),
    ),
    card(
        question="&iquest;En qu&eacute; se diferencia la concurrencia de Lambda entre fuentes <b>poll-based</b> (Kinesis/DynamoDB Streams) y <b>push-based</b> (API Gateway/S3)?",
        options=[
            "En ambas la concurrencia = items/seg &times; duraci&oacute;n",
            "Poll-based: la concurrencia la fija el n&uacute;mero de shards. Push-based: &asymp; items/seg &times; duraci&oacute;n",
            "Poll-based no tiene l&iacute;mite; push-based s&iacute;",
            "Push-based procesa en orden; poll-based no",
        ],
        correct=1,
        key="dva04-q18-poll-vs-push",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; poll = shards; push = tasa &times; duraci&oacute;n.</div>'
            '<p><b>Poll-based</b> (de sondeo): Lambda <b>sondea</b> la fuente. Para <b>Kinesis y DynamoDB Streams</b> la concurrencia es el <b>n&uacute;mero de shards</b> (SQS tambi&eacute;n es de sondeo, pero escala por pollers/lotes, no por shards). <b>Event-driven / push</b> (API Gateway, S3 events, SNS): la concurrencia estimada &asymp; <b>peticiones/seg &times; duraci&oacute;n promedio</b> (ej. 50/seg &times; 10 s = 500).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> la f&oacute;rmula "tasa &times; duraci&oacute;n" NO aplica a streams (ah&iacute; manda el nº de shards). Ambas tienen l&iacute;mite (el l&iacute;mite de concurrencia de la cuenta/regi&oacute;n). Y son los <b>streams</b> (poll-based) los que procesan <b>en orden</b> por shard, no al rev&eacute;s.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;Ves "shards" en la pregunta? &rarr; la concurrencia es el n&uacute;mero de shards, ignora items/seg.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html">docs.aws Lambda concurrency</a></div>'
        ),
    ),
    card(
        question="Para <b>aumentar la capacidad de datos</b> de un Kinesis Data Stream (y con ello la concurrencia de la Lambda que lo consume), &iquest;qu&eacute; haces con los shards?",
        options=[
            "Merge (fusionar) shards",
            "Split (dividir) shards",
            "Reiniciar el stream",
            "Nada; se escala solo autom&aacute;ticamente (modo provisioned)",
        ],
        correct=1,
        key="dva04-q18-split-shards",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; split (dividir) shards.</div>'
            '<p>En modo <b>provisioned</b>, la capacidad del stream = n&uacute;mero de shards. Para aumentarla haces <b>shard split</b> (divides un shard en dos), lo que sube tanto el throughput como la unidad de concurrencia de la Lambda. <b>Merge</b> hace lo contrario: fusiona dos shards y <b>reduce</b> capacidad.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> "merge" reduce, no aumenta. "reiniciar" no cambia el sharding. Y el escalado autom&aacute;tico solo aplica al modo <b>on-demand</b>; en provisioned lo controlas t&uacute; con split/merge.</p>'
            '<div class="extra"><span class="h">Dato extra</span>El modo <b>on-demand</b> de Kinesis escala shards autom&aacute;ticamente; el modo <b>provisioned</b> requiere split/merge manual (o UpdateShardCount).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/streams/latest/dev/kinesis-using-sdk-java-resharding.html">docs.aws Kinesis resharding</a></div>'
        ),
    ),

    # ================= Q21: Import third-party SSL/TLS certificate =================
    card(
        question="Un desarrollador tiene un certificado SSL/TLS de una <b>CA de terceros</b> (autoridad certificadora externa) listo para importar a AWS. &iquest;En qu&eacute; servicio puede importarlo de forma segura (adem&aacute;s del IAM certificate store)?",
        options=[
            "Un bucket S3 privado con versionado",
            "AWS Certificate Manager (ACM)",
            "Amazon Cognito",
            "Amazon CloudFront",
        ],
        correct=1,
        key="dva04-q21-acm-import",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; ACM (y el IAM certificate store como la otra opci&oacute;n).</div>'
            '<p>Las DOS formas correctas de guardar/importar un certificado de terceros son <b>ACM</b> (AWS Certificate Manager, la herramienta preferida para aprovisionar y desplegar certificados) y el <b>IAM certificate store</b>. El IAM cert store se usa cuando necesitas HTTPS en una <b>regi&oacute;n que ACM no soporta</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> un <b>bucket S3</b> no es un almac&eacute;n de certificados. <b>Cognito</b> es identidad/sincronizaci&oacute;n de usuarios, no guarda certificados. <b>CloudFront</b> puede <i>usar</i> certificados, pero primero debes importarlos a ACM o al IAM cert store; no los importas directamente a CloudFront ni los puedes exportar/reutilizar desde ah&iacute;.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>ACM emite certificados <b>gratis y auto-renovables</b> para uso en AWS; los <b>importados</b> (de terceros) NO se renuevan solos, t&uacute; los renuevas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html">docs.aws IAM server certs</a><br>'
            '<a href="https://tutorialsdojo.com/aws-certificate-manager/">tutorialsdojo ACM</a></div>'
        ),
    ),
    card(
        question="&iquest;Cu&aacute;ndo se usa el <b>IAM certificate store</b> en vez de ACM para un certificado SSL/TLS?",
        options=[
            "Siempre, porque IAM es m&aacute;s barato",
            "Cuando necesitas HTTPS en una regi&oacute;n que ACM no soporta",
            "Cuando el certificado es auto-renovable de ACM",
            "Cuando quieres administrar el certificado desde la consola de IAM",
        ],
        correct=1,
        key="dva04-q21-iam-cert-store",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; cuando la regi&oacute;n no soporta ACM.</div>'
            '<p><b>ACM es la herramienta preferida</b>. El <b>IAM certificate store</b> es el recurso alterno: se usa <b>solo</b> cuando necesitas soportar HTTPS en una <b>regi&oacute;n donde ACM no est&aacute; disponible</b>. IAM cifra tu clave privada y la almacena; soporta desplegar certificados en todas las regiones, pero el certificado debe venir de un proveedor externo.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no se usa "siempre" (ACM es preferido y sus certificados son gratis). No sirve para certificados auto-renovables de ACM (esos viven en ACM). Y <b>no</b> puedes administrar certificados IAM desde la <b>consola</b>: solo v&iacute;a CLI/API.</p>'
            '<div class="warn"><span class="h">Ojo</span>No puedes subir un certificado de ACM a IAM, ni gestionar los certificados de IAM desde la consola. Los certificados importados no se renuevan solos.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html">docs.aws IAM server certs</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(deck_name="DVA-C02::04", cards=cards, out_path="out/DVA-C02_04.apkg")
