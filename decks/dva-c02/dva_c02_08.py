#!/usr/bin/env python3
"""
DVA-C02::08 - Cards from PRACTICE SET 3, only the questions the user got INCORRECT.
Source: notes/source/set3_failed.txt (Q5, Q6, Q7, Q21, Q29, Q32, Q36, Q40)

Each long exam question is broken into 2-3 atomic cards (one concept per card),
following DECK_STANDARDS.md: self-contained stems, {{L}} verdict, refute every
distractor one by one, explanations in Spanish, 4 options, stable keys.
"""
from anki_mcq import card, create

cards = [
    # ================= Q5: Cognito Identity Pools (guest + social) =================
    card(
        question="Un juego m&oacute;vil necesita entregar <b>credenciales AWS temporales</b> tanto a usuarios autenticados por redes sociales (Facebook, Google) como a <b>usuarios invitados sin autenticar</b> (guest). &iquest;Qu&eacute; servicio AWS usas?",
        options=[
            "Amazon Cognito Identity Pools, habilitando el acceso a identidades no autenticadas (unauthenticated)",
            "Amazon Cognito User Pools, habilitando el acceso a identidades no autenticadas (unauthenticated)",
            "Amazon Cognito Sync para sincronizar los datos de usuario entre dispositivos",
            "AWS IAM Identity Center para gestionar el acceso de la fuerza laboral a varias cuentas",
        ],
        correct=0,
        key="dva08-q5-cognito-identity-pools",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Cognito Identity Pools + unauthenticated identities.</div>'
            '<p>Un <b>Identity Pool</b> (grupo de identidades) de Amazon Cognito es lo que <b>entrega credenciales AWS temporales</b> (v&iacute;a STS) para acceder a servicios AWS. Puede dar credenciales a usuarios de un User Pool, a usuarios autenticados por <b>proveedores externos</b> (Facebook, Google, SAML) y, si activas <b>unauthenticated identities</b>, tambi&eacute;n a <b>usuarios invitados</b> sin login. Eso cubre exactamente el requisito: social + guest con credenciales temporales.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Cognito User Pools:</b> es solo un <b>directorio de usuarios</b> (autenticaci&oacute;n, devuelve tokens JWT). No entrega credenciales AWS ni maneja acceso invitado; para credenciales AWS necesitas un Identity Pool.</li>'
            '<li><b>Cognito Sync:</b> es una librer&iacute;a cliente para <b>sincronizar datos de usuario entre dispositivos</b>, no un servicio de autenticaci&oacute;n ni de credenciales.</li>'
            '<li><b>IAM Identity Center:</b> gestiona el acceso <b>de empleados/fuerza laboral</b> a varias cuentas AWS; no ofrece acceso invitado ni federaci&oacute;n con redes sociales para apps de consumidores.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"credenciales AWS temporales" o "acceso invitado/guest"? &rarr; <b>Identity Pool</b>. &iquest;"directorio de usuarios / login / MFA"? &rarr; User Pool.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/cognito/latest/developerguide/identity-pools.html">docs.aws Identity Pools</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cognito/">tutorialsdojo Cognito</a></div>'
        ),
    ),
    card(
        question="En Amazon Cognito, &iquest;cu&aacute;l es la diferencia principal entre un <b>User Pool</b> y un <b>Identity Pool</b>?",
        options=[
            "User Pool = directorio de usuarios que autentica y devuelve tokens (JWT); Identity Pool = entrega credenciales AWS temporales para servicios AWS",
            "User Pool = entrega credenciales AWS temporales para servicios AWS; Identity Pool = directorio de usuarios que autentica y devuelve tokens (JWT)",
            "User Pool e Identity Pool = ambos entregan credenciales AWS temporales; solo cambia el proveedor de identidad soportado por cada uno",
            "User Pool = sincroniza datos de usuario entre dispositivos; Identity Pool = solo aplica MFA a los usuarios del directorio",
        ],
        correct=0,
        key="dva08-q5-userpool-vs-identitypool",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; User Pool autentica (tokens); Identity Pool da credenciales AWS.</div>'
            '<p><b>User Pool:</b> es el <b>directorio de usuarios</b>. Maneja registro, login, MFA y devuelve <b>tokens</b> (ID/access JWT) que prueban qui&eacute;n eres. <b>Identity Pool (federated identities):</b> toma una identidad (de un User Pool o de un IdP externo) y la cambia por <b>credenciales AWS temporales</b> v&iacute;a STS, para llamar directamente a servicios AWS. Muchas apps usan los dos: User Pool autentica, luego Identity Pool entrega las credenciales.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invertir los roles es falso (User Pool no da credenciales AWS). No es cierto que "ambos entreguen credenciales": solo el Identity Pool lo hace. Y ni User Pool sincroniza dispositivos (eso es Cognito Sync) ni Identity Pool se limita a MFA.</p>'
            '<div class="extra"><span class="h">Dato</span>Regla: token/login &rarr; User Pool. Credenciales AWS temporales &rarr; Identity Pool.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/cognito/latest/developerguide/getting-started-with-identity-pools.html">docs.aws getting started identity pools</a></div>'
        ),
    ),

    # ================= Q6: KMS envelope encryption =================
    card(
        question="&iquest;Cu&aacute;l describe correctamente el proceso de <b>envelope encryption</b> (cifrado en sobre)?",
        options=[
            "Cifrar los datos en claro con una data key, y luego cifrar esa data key con una clave de nivel superior en claro (plaintext root key)",
            "Cifrar los datos en claro con una data key, y luego cifrar esa data key con una clave de nivel superior ya cifrada (encrypted key)",
            "Cifrar los datos en claro con una KMS key, y luego cifrar esa KMS key con una data key de nivel superior en claro",
            "Cifrar los datos en claro con una KMS key, y luego cifrar esa KMS key con una data key de nivel superior ya cifrada",
        ],
        correct=0,
        key="dva08-q6-envelope-encryption-flow",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; datos con data key; data key con una root key en claro.</div>'
            '<p><b>Envelope encryption:</b> ciframos los <b>datos en claro con una data key</b> (clave de datos, sim&eacute;trica y r&aacute;pida) y luego ciframos <b>esa data key con otra clave</b>. Puedes encadenar varias capas, pero al final <b>una clave debe quedar en claro</b> (la <b>root key</b> / clave de nivel superior) para poder descifrar la cadena. En AWS, esa root key vive protegida dentro de <b>AWS KMS</b> (nunca sale en claro de los HSM), y llamas a KMS para usarla.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>data key cifrada con una clave superior ya cifrada:</b> imposible como tope de la cadena. La clave del nivel m&aacute;s alto (root key) debe estar <b>en claro</b>; si tambi&eacute;n estuviera cifrada, no habr&iacute;a forma de arrancar el descifrado.</li>'
            '<li><b>datos con KMS key + KMS key cifrada con data key en claro:</b> los datos se cifran con una <b>data key</b>, no con la KMS key directamente; y la root/top-level debe ser la clave superior en claro, no una data key.</li>'
            '<li><b>datos con KMS key + KMS key cifrada con data key cifrada:</b> mismo doble error: se cifra con data key (no KMS key) y el tope debe ir en claro.</li>'
            '</ul>'
            '<div class="warn"><span class="h">Precisi&oacute;n</span>"En claro" aqu&iacute; significa <b>no cifrada por otra clave</b> (para poder arrancar el descifrado), <b>no</b> que sea visible o accesible. En AWS KMS la root key nunca sale en claro de los HSM validados FIPS; para usarla llamas a KMS.</div>'
            '<div class="extra"><span class="h">Truco de examen</span>La <b>root key</b> (clave superior) es la que queda <b>sin cifrar por otra clave</b>; las data keys se almacenan <b>cifradas</b> junto al dato.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping">docs.aws envelope encryption</a><br>'
            '<a href="https://tutorialsdojo.com/aws-key-management-service-aws-kms/">tutorialsdojo KMS</a></div>'
        ),
    ),
    card(
        question="En envelope encryption con AWS KMS, &iquest;por qu&eacute; conviene cifrar el mismo dato bajo varias claves reencriptando <b>solo la data key</b> en vez de reencriptar el dato completo?",
        options=[
            "Porque re-cifrar solo la data key (peque&ntilde;a) es mucho m&aacute;s r&aacute;pido que re-cifrar objetos de datos grandes",
            "Porque una data key no puede cifrarse dos veces bajo claves distintas, as&iacute; que hay que copiar el dato entero",
            "Porque KMS cobra por cada byte de dato cifrado y en cambio cifrar las data keys peque&ntilde;as es gratis",
            "Porque reencriptar el objeto de datos completo cambia su tama&ntilde;o y eso rompe la integridad del cifrado",
        ],
        correct=0,
        key="dva08-q6-reencrypt-datakey-only",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; re-cifrar solo la data key (peque&ntilde;a) es mucho m&aacute;s r&aacute;pido.</div>'
            '<p>Cifrar objetos grandes es costoso en tiempo. Con envelope encryption el dato queda cifrado <b>una vez</b> con su data key; si necesitas protegerlo bajo otra clave (rotaci&oacute;n, otro destinatario), solo <b>re-cifras la data key</b>, que es diminuta. As&iacute; evitas re-encriptar gigabytes de datos crudos.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> una data key <b>s&iacute;</b> puede cifrarse varias veces (bajo distintas claves). El beneficio es de <b>rendimiento</b>, no de facturaci&oacute;n por byte. Y reencriptar el dato no lo "rompe": simplemente es innecesariamente lento comparado con reencriptar solo la clave.</p>'
            '<div class="extra"><span class="h">Dato</span>Otros beneficios: proteger la data key (la guardas cifrada junto al dato) y combinar algoritmos sim&eacute;tricos (r&aacute;pidos) con asim&eacute;tricos (mejor gesti&oacute;n de claves).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping">docs.aws envelope encryption</a></div>'
        ),
    ),

    # ================= Q7: API Gateway Lambda Authorizer TOKEN =================
    card(
        question="Con un <b>API Gateway Lambda Authorizer</b>, necesitas una estrategia de autenticaci&oacute;n similar a <b>OAuth o SAML</b> (el llamador env&iacute;a un bearer token, ej. un JWT). &iquest;Qu&eacute; tipo de autorizador usas?",
        options=[
            "Token-based authorization (autorizador tipo TOKEN)",
            "Request parameter-based authorization (autorizador tipo REQUEST)",
            "Cross-Account Lambda Authorizer",
            "AWS STS-based authentication",
        ],
        correct=0,
        key="dva08-q7-token-authorizer",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Token-based (TOKEN) authorizer.</div>'
            '<p>Un <b>Lambda Authorizer</b> es una funci&oacute;n Lambda que API Gateway invoca para decidir el acceso, devolviendo una pol&iacute;tica IAM. Hay dos tipos. El <b>TOKEN authorizer</b> recibe la identidad del llamador en un <b>bearer token</b> (por ejemplo un JWT u OAuth token) enviado en un header. Es justo el patr&oacute;n para esquemas tipo <b>OAuth/SAML</b> basados en token.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>REQUEST authorizer:</b> deriva la identidad de una <b>combinaci&oacute;n de headers, query strings, stageVariables y $context</b>, no de un bearer token. No encaja con OAuth/SAML por token.</li>'
            '<li><b>Cross-Account Lambda Authorizer:</b> no es un <b>tipo</b> de autorizador; solo describe usar una Lambda autorizadora que vive en <b>otra cuenta AWS</b>. Los tipos siguen siendo TOKEN o REQUEST.</li>'
            '<li><b>AWS STS-based authentication:</b> no existe como tipo de Lambda Authorizer en API Gateway. Es un distractor.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"bearer token / JWT / OAuth / SAML"? &rarr; <b>TOKEN authorizer</b>. &iquest;"headers + query params + contexto"? &rarr; REQUEST authorizer.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html">docs.aws Lambda Authorizer</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-api-gateway/">tutorialsdojo API Gateway</a></div>'
        ),
    ),
    card(
        question="En API Gateway, &iquest;de d&oacute;nde obtiene la identidad del llamador un <b>REQUEST authorizer</b> (autorizador basado en par&aacute;metros de la petici&oacute;n)?",
        options=[
            "De una combinaci&oacute;n de headers, query string parameters, stageVariables y variables de $context de la petici&oacute;n",
            "De un bearer token (JWT u OAuth) enviado en un header de autorizaci&oacute;n, tal como en el flujo OAuth/SAML",
            "De las credenciales IAM firmadas con SigV4 que acompa&ntilde;an a la petici&oacute;n entrante del cliente",
            "De una sesi&oacute;n STS creada con AssumeRole por el cliente justo antes de llamar a la API",
        ],
        correct=0,
        key="dva08-q7-request-authorizer",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; headers + query strings + stageVariables + $context.</div>'
            '<p>El <b>REQUEST authorizer</b> recibe la identidad del llamador a partir de una <b>combinaci&oacute;n</b> de: headers, par&aacute;metros de query string, <code>stageVariables</code> y variables de <code>$context</code>. Sirve cuando la decisi&oacute;n de acceso depende de m&aacute;s que un solo token (ej. cabeceras m&uacute;ltiples, IP de origen, etc.).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> el <b>bearer token/JWT</b> corresponde al <b>TOKEN authorizer</b>, no al REQUEST. La firma <b>SigV4/IAM</b> es autorizaci&oacute;n IAM nativa de API Gateway, no un Lambda Authorizer. Y una <b>sesi&oacute;n STS</b> no es el mecanismo de entrada de un REQUEST authorizer.</p>'
            '<div class="extra"><span class="h">Dato</span>Los dos &uacute;nicos tipos de Lambda Authorizer son <b>TOKEN</b> y <b>REQUEST</b>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-input.html">docs.aws authorizer input</a></div>'
        ),
    ),

    # ================= Q21: CloudWatch agent IAM policy =================
    card(
        question="Instancias EC2 en un Auto Scaling group tienen instalado el <b>CloudWatch agent</b> para publicar m&eacute;tricas personalizadas, pero las <b>instancias reci&eacute;n lanzadas fallan al enviar</b> las m&eacute;tricas a CloudWatch. &iquest;Qu&eacute; cambio lo corrige?",
        options=[
            "Adjuntar la pol&iacute;tica CloudWatchAgentServerPolicy al IAM role del launch template de las instancias",
            "Adjuntar la pol&iacute;tica CloudWatchAgentAdminPolicy al IAM role del launch template para dar permisos ampliados al agente",
            "Configurar el IAM role con CloudWatchAgentReadOnlyAccess para que el agente lea y publique m&eacute;tricas por defecto",
            "A&ntilde;adir un user data script en el launch template que instale e inicie el CloudWatch agent al arrancar",
        ],
        correct=0,
        key="dva08-q21-cwagent-serverpolicy",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CloudWatchAgentServerPolicy en el IAM role.</div>'
            '<p><b>CloudWatchAgentServerPolicy</b> es la pol&iacute;tica administrada por AWS que da al agente los permisos necesarios para <b>publicar</b> m&eacute;tricas y logs: acciones como <code>cloudwatch:PutMetricData</code> y <code>logs:PutLogEvents</code>. Al adjuntarla al <b>IAM role</b> (v&iacute;a instance profile) del launch template, toda instancia nueva del ASG nace con permiso para enviar m&eacute;tricas. La causa ra&iacute;z del fallo eran <b>permisos IAM insuficientes</b>, no el arranque del agente.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CloudWatchAgentAdminPolicy:</b> s&iacute; permite publicar, pero da permisos <b>excesivos</b> (incluye escribir la config del agente en Parameter Store). Viola el principio de m&iacute;nimo privilegio; ServerPolicy es la adecuada.</li>'
            '<li><b>CloudWatchAgentReadOnlyAccess:</b> es <b>solo lectura</b>; permite ver m&eacute;tricas/logs pero <b>no publicar</b> m&eacute;tricas personalizadas. No resuelve el env&iacute;o.</li>'
            '<li><b>User data para instalar/iniciar el agente:</b> el agente ya est&aacute; instalado y corriendo; falta el <b>permiso</b>. Aunque instalarlo por user data es v&aacute;lido en general, aqu&iacute; no ataca la causa ra&iacute;z (IAM).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Agente que "no puede enviar/publicar m&eacute;tricas" &rarr; falta <b>CloudWatchAgentServerPolicy</b> en el role. Admin = demasiado; ReadOnly = insuficiente.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/aws-managed-policy/latest/reference/CloudWatchAgentServerPolicy.html">docs.aws CloudWatchAgentServerPolicy</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cloudwatch/">tutorialsdojo CloudWatch</a></div>'
        ),
    ),
    card(
        question="&iquest;Por qu&eacute; se asocia un <b>IAM role</b> (v&iacute;a instance profile) a una instancia EC2 en lugar de incrustar claves de acceso de larga duraci&oacute;n en la instancia?",
        options=[
            "Porque el role provee credenciales temporales rotadas autom&aacute;ticamente, evitando distribuir claves de larga duraci&oacute;n",
            "Porque un role cifra el disco de la instancia mientras que las claves de acceso est&aacute;ticas no cifran nada del disco",
            "Porque solo asociando un IAM role la instancia EC2 puede obtener una direcci&oacute;n IP p&uacute;blica enrutable",
            "Porque las claves de acceso de larga duraci&oacute;n no funcionan cuando la instancia est&aacute; en una subred privada de una VPC",
        ],
        correct=0,
        key="dva08-q21-iam-role-temp-creds",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; el role da credenciales temporales rotadas autom&aacute;ticamente.</div>'
            '<p>Un <b>IAM role</b> asignado a la EC2 (a trav&eacute;s de un <b>instance profile</b>) entrega a las apps de la instancia <b>credenciales temporales</b> obtenidas de STS, que AWS <b>rota autom&aacute;ticamente</b>. As&iacute; no tienes que distribuir claves de acceso de larga duraci&oacute;n a cada instancia ni rotarlas manualmente, reduciendo el riesgo de fuga.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> un role no cifra discos (eso es EBS encryption/KMS), no controla si la instancia tiene IP p&uacute;blica (eso es red/VPC), y las claves de larga duraci&oacute;n funcionan igual dentro de una VPC privada; el punto es la <b>gesti&oacute;n segura de credenciales</b>, no la conectividad.</p>'
            '<div class="extra"><span class="h">Dato</span>Solo se puede asociar <b>un</b> role por instancia; todas las apps de esa instancia comparten sus permisos.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html">docs.aws IAM roles for EC2</a></div>'
        ),
    ),

    # ================= Q29: Elasticity - Spot Fleet + DynamoDB =================
    card(
        question="Buscas los servicios que aporten <b>MAYOR elasticidad</b> (ajustar oferta de recursos a la demanda) manteniendo costo-eficiencia. &iquest;Cu&aacute;les dos aplican mejor? (elige el par correcto)",
        options=[
            "Amazon EC2 Spot Fleet y Amazon DynamoDB (ambos escalan v&iacute;a Application Auto Scaling)",
            "Amazon CloudFront y AWS WAF (CDN global mas firewall de aplicaci&oacute;n)",
            "Amazon RDS y AWS WAF (base de datos administrada mas firewall)",
            "Amazon CloudFront y Amazon RDS (CDN mas base de datos relacional)",
        ],
        correct=0,
        key="dva08-q29-elasticity-spotfleet-dynamodb",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; EC2 Spot Fleet y DynamoDB.</div>'
            '<p><b>Elasticidad</b> = ajustar autom&aacute;ticamente los recursos (que cuestan dinero) a la demanda real. <b>Application Auto Scaling</b> puede escalar, entre otros, un <b>EC2 Spot Fleet</b> (lanza/termina instancias dentro de un rango seg&uacute;n pol&iacute;ticas) y una tabla <b>DynamoDB</b> (sube/baja RCU/WCU aprovisionados seg&uacute;n el tr&aacute;fico, sin throttling y sin pagar capacidad ociosa). Ambos escalan por volumen y bajan costo cuando la demanda cae.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CloudFront:</b> es un CDN para <b>escalar la entrega</b> de contenido est&aacute;tico/din&aacute;mico al usuario; no escala el <b>c&oacute;mputo ni el almacenamiento</b> de la aplicaci&oacute;n, que es la elasticidad que pide el escenario.</li>'
            '<li><b>AWS WAF:</b> mejora la <b>seguridad</b> (filtra tr&aacute;fico malicioso), no la elasticidad de recursos.</li>'
            '<li><b>Amazon RDS:</b> escala, pero con menos elasticidad fina y mayor costo continuo (instancia siempre encendida, storage, backups) frente a Spot Fleet + DynamoDB.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"elasticidad + costo-eficiencia por volumen"? Piensa en lo que <b>Application Auto Scaling</b> puede escalar: EC2/Spot Fleet, ECS, DynamoDB, EMR, AppStream.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html">docs.aws DynamoDB Auto Scaling</a><br>'
            '<a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet.html">docs.aws EC2 Spot Fleet</a></div>'
        ),
    ),
    card(
        question="En elasticidad AWS, &iquest;qu&eacute; distingue la elasticidad <b>basada en tiempo</b> (time-based) de la basada en <b>volumen</b> (volume-based)?",
        options=[
            "Time-based = apagar recursos cuando no se usan (ej. dev solo en horario laboral); volume-based = escalar la magnitud seg&uacute;n la demanda",
            "Time-based = escalar CPU/almacenamiento seg&uacute;n la carga; volume-based = apagar recursos fuera del horario laboral programado",
            "Time-based = solo aplica a bases de datos gestionadas; volume-based = solo aplica a instancias de c&oacute;mputo EC2 en un ASG",
            "Ambas significan lo mismo: pagar por recursos encendidos 24/7 sin importar el uso real que reciban en cada momento",
        ],
        correct=0,
        key="dva08-q29-elasticity-time-vs-volume",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; tiempo = apagar cuando no se usa; volumen = escalar la magnitud.</div>'
            '<p><b>Time-based:</b> apagar recursos cuando no se necesitan (ej. un entorno de desarrollo encendido solo en horario laboral). <b>Volume-based:</b> ajustar la <b>escala</b> a la intensidad de la demanda (n&uacute;mero de cores, tama&ntilde;o de almacenamiento, throughput). Auto Scaling + monitoreo + tagging + automatizaci&oacute;n te permiten aprovechar ambas y optimizar costo.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invertir las definiciones es falso; ninguna se limita a un solo tipo de servicio; y no significan pagar 24/7, precisamente la idea es <b>pagar por uso</b>.</p>'
            '<div class="extra"><span class="h">Dato</span>En la nube pagas por uso; casar uso con capacidad (elasticidad) es clave para optimizar costo.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html">docs.aws Application Auto Scaling (DynamoDB)</a></div>'
        ),
    ),

    # ================= Q32: DynamoDB Query + eventual consistency (least RCU) =================
    card(
        question="Una app recibe <code>ProvisionedThroughputExceeded</code> por picos de <b>RCU</b> en DynamoDB. Necesitas buscar &iacute;tems por <b>valores de primary key</b> usando la <b>MENOR cantidad de RCU</b>. &iquest;Qu&eacute; haces?",
        options=[
            "Usar la operaci&oacute;n Query con lecturas de consistencia eventual (eventual consistency)",
            "Usar la operaci&oacute;n Query con lecturas de consistencia fuerte (strong consistency)",
            "Usar la operaci&oacute;n Scan con lecturas de consistencia eventual",
            "Usar la operaci&oacute;n Scan con lecturas de consistencia fuerte",
        ],
        correct=0,
        key="dva08-q32-query-eventual-least-rcu",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Query + eventual consistency.</div>'
            '<p><b>Query</b> encuentra &iacute;tems por <b>primary key</b> (partition key, opcional sort key), leyendo solo lo que coincide. <b>Scan</b>, en cambio, lee <b>toda</b> la tabla o &iacute;ndice y luego filtra, consumiendo mucha m&aacute;s capacidad. Adem&aacute;s, las <b>lecturas eventualmente consistentes cuestan la mitad de RCU</b> que las fuertemente consistentes. Por eso, para buscar por clave con el m&iacute;nimo RCU: Query + eventual consistency.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Query + strong consistency:</b> es la operaci&oacute;n correcta, pero las lecturas fuertes consumen <b>el doble</b> de RCU que las eventuales. No es el m&iacute;nimo.</li>'
            '<li><b>Scan + eventual:</b> Scan recorre toda la tabla; no busca por primary key y gasta mucho m&aacute;s, aunque la lectura sea eventual.</li>'
            '<li><b>Scan + strong:</b> lo peor: recorre todo <b>y</b> usa lecturas fuertes (doble RCU). M&aacute;ximo consumo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Menos RCU: <b>Query</b> (no Scan) + <b>eventual</b> (no strong). Regla RCU: eventual = 1/2 de strong.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-query-scan.html">docs.aws Query vs Scan</a><br>'
            '<a href="https://tutorialsdojo.com/dynamodb-scan-vs-query/">tutorialsdojo Scan vs Query</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, &iquest;por qu&eacute; una operaci&oacute;n <b>Scan</b> suele ser mucho m&aacute;s costosa e ineficiente que una <b>Query</b>?",
        options=[
            "Scan lee cada &iacute;tem de toda la tabla o &iacute;ndice y luego filtra; Query localiza &iacute;tems por primary key",
            "Scan solo funciona con lecturas fuertemente consistentes, por eso siempre gasta el doble de RCU que un Query",
            "Scan no puede correr sobre ning&uacute;n &iacute;ndice, mientras que un Query siempre exige un GSI dedicado para la tabla",
            "Scan cifra los resultados en tr&aacute;nsito y Query no lo hace, por eso Scan consume mucha m&aacute;s capacidad de lectura",
        ],
        correct=0,
        key="dva08-q32-why-scan-costly",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Scan recorre toda la tabla; Query busca por clave.</div>'
            '<p><b>Scan</b> examina <b>todos</b> los &iacute;tems de la tabla o &iacute;ndice y despu&eacute;s aplica el filtro, por lo que consume capacidad proporcional al tama&ntilde;o total y se vuelve m&aacute;s lento conforme crece la tabla. <b>Query</b> usa el <b>primary key</b> para ir directo a los &iacute;tems que necesita. Dise&ntilde;a tablas/&iacute;ndices para poder usar Query en vez de Scan.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> Scan admite lecturas eventuales o fuertes (no "solo fuerte"). Scan <b>s&iacute;</b> puede correr sobre un &iacute;ndice, y Query no exige siempre un GSI (funciona sobre la tabla base con su primary key). El cifrado no es el motivo del consumo; el motivo es <b>cu&aacute;ntos &iacute;tems se leen</b>.</p>'
            '<div class="extra"><span class="h">Dato</span>El RCU se calcula por <b>tama&ntilde;o de los &iacute;tems le&iacute;dos</b>, no por lo que devuelves; un filtro no reduce el costo de lo ya le&iacute;do.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html">docs.aws Scan</a></div>'
        ),
    ),

    # ================= Q36: EC2 IAM role vs AWS CLI key =================
    card(
        question="Una instancia EC2 ten&iacute;a un IAM role para escribir en los buckets S3 de dev y prod, y adem&aacute;s tiene claves de acceso configuradas en el <b>AWS CLI</b>. Le asignas un nuevo IAM role que solo permite el bucket dev, pero la app <b>sigue escribiendo en ambos</b> buckets. &iquest;Causa m&aacute;s probable?",
        options=[
            "La aplicaci&oacute;n sigue usando el IAM role/credenciales configurados en la clave del AWS CLI, no el instance profile role",
            "El instance profile role de una EC2 en ejecuci&oacute;n es est&aacute;tico y no puede reemplazarse nunca",
            "Por consistencia eventual, hay que esperar 24 horas para que el cambio se propague en todo AWS",
            "El nuevo IAM role tiene una inline policy adjunta que amplia sus permisos",
        ],
        correct=0,
        key="dva08-q36-cli-key-overrides-role",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; la app sigue usando las credenciales del AWS CLI.</div>'
            '<p>La cadena de credenciales del SDK/CLI busca claves en varios lugares. Si la instancia tiene <b>claves de acceso est&aacute;ticas configuradas en el AWS CLI</b> (perfil/credenciales locales), la app puede estar usando <b>esas</b> credenciales (que a&uacute;n permiten ambos buckets) en vez de las del <b>instance profile role</b> reci&eacute;n cambiado. Por eso sigue escribiendo en dev y prod: hay que actualizar/eliminar tambi&eacute;n las credenciales del CLI, no solo el role.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>El role es est&aacute;tico y no puede cambiarse:</b> falso; puedes reemplazar el role del instance profile en cualquier momento.</li>'
            '<li><b>Esperar 24h por consistencia eventual:</b> no hay tal ventana fija; el cambio de role se refleja pronto. La causa real son las claves del CLI.</li>'
            '<li><b>Inline policy en el nuevo role:</b> una inline policy es solo una pol&iacute;tica embebida; el nuevo role solo permite dev, as&iacute; que no explica el acceso a prod. El culpable son las credenciales est&aacute;ticas del CLI.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Si conviven <b>instance profile role</b> y <b>claves est&aacute;ticas del CLI</b>, las claves del CLI pueden tener precedencia. Elimina las claves para forzar el uso del role.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html">docs.aws roles for EC2</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; es un <b>instance profile</b> en EC2 y cu&aacute;ntos IAM roles puede entregar a la instancia a la vez?",
        options=[
            "Es el contenedor que asocia un IAM role a la instancia y le provee credenciales temporales; un solo role por instancia",
            "Es una pol&iacute;tica inline adjunta directamente a la instancia EC2; puede contener hasta 10 IAM roles simult&aacute;neos",
            "Es un par de claves de acceso est&aacute;ticas guardadas dentro de la instancia; admite asociar m&uacute;ltiples roles a la vez",
            "Es un grupo IAM asignado a la instancia EC2; permite combinar y sumar los permisos de varios roles al mismo tiempo",
        ],
        correct=0,
        key="dva08-q36-instance-profile",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; contenedor que asocia un role; un solo role por instancia.</div>'
            '<p>Un <b>instance profile</b> es el contenedor que vincula un <b>IAM role</b> a una instancia EC2 y le suministra las <b>credenciales temporales</b> del role a las apps que corren en ella. Solo puede haber <b>un role activo por instancia</b>; todas las aplicaciones de esa instancia comparten sus permisos. Puedes quitar el role actual y poner otro cuando quieras.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no es una inline policy ni admite 10 roles; no es un par de claves est&aacute;ticas (justo lo contrario: evita usarlas); y no es un grupo IAM (los grupos son para usuarios, no para instancias) ni combina varios roles.</p>'
            '<div class="extra"><span class="h">Dato</span>Con la consola, el instance profile se crea por ti; con CLI/API debes crearlo y asignarle el role como paso aparte.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html">docs.aws instance profiles</a></div>'
        ),
    ),

    # ================= Q40: Lambda CPU scales with memory =================
    card(
        question="Necesitas <b>aumentar la CPU disponible</b> para una funci&oacute;n Lambda que procesa registros en un fan-out desde un Kinesis data stream. &iquest;Cu&aacute;l es la MEJOR forma de lograrlo?",
        options=[
            "Aumentar la memoria asignada (allocated memory) de la funci&oacute;n",
            "Aumentar el l&iacute;mite de ejecuciones concurrentes de la funci&oacute;n",
            "Configurar la funci&oacute;n para usar unreserved account concurrency",
            "Usar Lambda@Edge para la funci&oacute;n",
        ],
        correct=0,
        key="dva08-q40-lambda-cpu-memory",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; aumentar la memoria asignada.</div>'
            '<p>En Lambda, la <b>CPU (y otros recursos) escalan de forma proporcional a la memoria</b> que asignas a la funci&oacute;n. No existe un control de CPU independiente: para darle m&aacute;s CPU (y as&iacute; procesar m&aacute;s r&aacute;pido cada registro) subes el par&aacute;metro de <b>memoria</b>. Es la palanca directa de rendimiento por invocaci&oacute;n.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Aumentar la concurrencia:</b> permite ejecutar <b>m&aacute;s invocaciones en paralelo</b>, no da m&aacute;s CPU a una sola invocaci&oacute;n. No acelera el procesamiento de cada registro.</li>'
            '<li><b>Unreserved account concurrency:</b> es solo el pool de concurrencia no reservada compartido; tampoco cambia la CPU por funci&oacute;n.</li>'
            '<li><b>Lambda@Edge:</b> ejecuta funciones en ubicaciones de borde de CloudFront para procesar peticiones HTTP; no es una forma de aumentar CPU ni aplica a procesar un stream de Kinesis.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"m&aacute;s CPU en Lambda"? &rarr; sube la <b>memoria</b>. Umbral clave: <b>1769 MB = 1 vCPU</b> completo; a <b>10.240 MB</b> obtienes ~<b>6 vCPUs</b>. Concurrencia = m&aacute;s invocaciones en paralelo, no m&aacute;s CPU por invocaci&oacute;n.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html">docs.aws Lambda memory/CPU</a><br>'
            '<a href="https://tutorialsdojo.com/aws-lambda/">tutorialsdojo Lambda</a></div>'
        ),
    ),
    card(
        question="En AWS Lambda, &iquest;qu&eacute; significan las <b>concurrent executions</b> (ejecuciones concurrentes) y c&oacute;mo se relacionan con la CPU?",
        options=[
            "Es el n&uacute;mero de invocaciones en paralelo; sube el paralelismo pero no la CPU de una invocaci&oacute;n (la CPU depende de la memoria)",
            "Es la CPU total asignada a la funci&oacute;n; subir la concurrencia da m&aacute;s CPU a cada invocaci&oacute;n individual que corre",
            "Es la memoria disponible por funci&oacute;n; la concurrencia controla directamente los MB de RAM que recibe cada invocaci&oacute;n",
            "Es el n&uacute;mero de reintentos por invocaci&oacute;n antes de descartar el evento en una invocaci&oacute;n asincr&oacute;nica fallida",
        ],
        correct=0,
        key="dva08-q40-concurrency-vs-cpu",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; concurrencia = invocaciones en paralelo, no CPU por invocaci&oacute;n.</div>'
            '<p><b>Concurrent executions</b> es cu&aacute;ntas ejecuciones de tu funci&oacute;n ocurren <b>al mismo tiempo</b>. Aumentarla te deja atender m&aacute;s eventos en paralelo, pero <b>no</b> le da m&aacute;s CPU a una invocaci&oacute;n concreta. La CPU (y I/O) de cada invocaci&oacute;n depende de la <b>memoria</b> asignada.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> concurrencia no es "CPU total" ni "memoria por funci&oacute;n" (esas son otras configuraciones), ni es el conteo de reintentos (eso es el manejo de errores de invocaci&oacute;n asincr&oacute;nica).</p>'
            '<div class="extra"><span class="h">Dato</span>F&oacute;rmula &uacute;til: concurrent executions ~= invocaciones por segundo x duraci&oacute;n media (s).</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html">docs.aws Lambda concurrency</a></div>'
        ),
    ),

    # ============================================================
    # SECCION 2: 10 preguntas adicionales de temas NO estudiados aun
    # (gaps reales verificados contra decks 04-08). Fuente: set3 Q41-Q65.
    # ============================================================

    # ================= Q41: Cognito Adaptive Authentication =================
    card(
        question="Una app usa Cognito User Pools con <b>MFA desactivado</b>. Tras una filtraci&oacute;n de datos ajena, temen que atacantes usen credenciales robadas. Quieren <b>exigir MFA solo a los inicios de sesi&oacute;n sospechosos</b>, no a todos. &iquest;Qu&eacute; habilitas?",
        options=[
            "Adaptive Authentication (autenticaci&oacute;n adaptativa) en el User Pool",
            "TOTP software token MFA en el User Pool para todos los usuarios",
            "Recrear el User Pool y activar SMS text message MFA",
            "Una Lambda con subscription filter que vigile la m&eacute;trica CompromisedCredentialRisk en CloudWatch Logs y dispare MFA",
        ],
        correct=0,
        key="dva08-q41-cognito-adaptive-auth",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Adaptive Authentication.</div>'
            '<p><b>Adaptive Authentication</b> (parte de las funciones de seguridad avanzada de Cognito) calcula un <b>risk score</b> por cada intento de inicio de sesi&oacute;n (basado en dispositivo, ubicaci&oacute;n, patr&oacute;n de uso, etc.). Cuando Cognito detecta <b>riesgo</b>, puede <b>bloquear</b> el inicio o <b>exigir/activar MFA</b> solo para ese usuario. As&iacute; se cumple el requisito: MFA <b>condicional</b>, solo ante inicios sospechosos, sin molestar al resto.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>TOTP MFA para todos:</b> activar MFA a nivel de User Pool desafiar&iacute;a a <b>todos</b> los usuarios, no solo a los sospechosos. No cumple "solo sospechosos".</li>'
            '<li><b>Recrear el User Pool + SMS MFA:</b> recrear el pool <b>pierde</b> todos los usuarios registrados (habr&iacute;a que re-importarlos) y adem&aacute;s MFA universal desaf&iacute;a a todos. Doble problema.</li>'
            '<li><b>Lambda vigilando una m&eacute;trica en CloudWatch:</b> opera <b>fuera</b> del flujo de autenticaci&oacute;n de Cognito; no puede insertar un reto MFA en pleno sign-in. Adem&aacute;s MFA se configura a nivel de User Pool/usuario, no reaccionando a una m&eacute;trica externa.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"MFA solo en logins sospechosos / basado en riesgo"? &rarr; <b>Adaptive Authentication</b> de Cognito.</div>'
            '<div class="warn"><span class="h">Nota (2024-11)</span>Cognito reorganiz&oacute; sus capacidades en <b>feature plans</b>: Lite, Essentials y Plus. Las Advanced Security Features (adaptive authentication y detecci&oacute;n de credenciales comprometidas) ahora requieren el plan <b>Plus</b> del User Pool. La respuesta del examen no cambia; solo activa la funci&oacute;n en el plan Plus.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-settings-adaptive-authentication.html">docs.aws adaptive authentication</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cognito/">tutorialsdojo Cognito</a></div>'
        ),
    ),

    # ================= Q42: IAM cross-account access (role switching) =================
    card(
        question="Una empresa tiene 3 cuentas AWS propias (A=Dev, B=Test, C=Prod). Un developer necesita acceso para <b>auditar</b> los despliegues en las cuentas B y C. &iquest;Cu&aacute;l es la forma M&Aacute;S eficiente de darle ese acceso?",
        options=[
            "Dar al developer acceso cross-account (asumir un IAM role) a los recursos de las cuentas B y C",
            "Crear identidades y contrase&ntilde;as separadas para el developer en las cuentas B y C",
            "Habilitar MFA en el IAM User del developer",
            "Configurar AWS Organizations y adjuntar una Service Control Policy (SCP) al developer para acceder a las otras cuentas",
        ],
        correct=0,
        key="dva08-q42-cross-account-role",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; acceso cross-account asumiendo un IAM role.</div>'
            '<p>Con <b>cross-account access</b> creas un <b>IAM role</b> en las cuentas B y C con los permisos de auditor&iacute;a y una <b>trust policy</b> que permite al usuario de la cuenta A asumirlo. El developer <b>cambia de rol</b> (switch role en consola, o <code>sts:AssumeRole</code> por CLI/API) para operar en B y C sin crear usuarios en cada cuenta ni cerrar/abrir sesi&oacute;n. Es la forma m&aacute;s eficiente y segura de delegar entre cuentas propias.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Identidades/contrase&ntilde;as separadas por cuenta:</b> funciona pero es <b>ineficiente</b>: el developer tiene que iniciar sesi&oacute;n por separado en cada cuenta y gestionar m&uacute;ltiples credenciales.</li>'
            '<li><b>MFA en el IAM User:</b> mejora la seguridad pero <b>no resuelve el acceso</b> a las otras cuentas. Es complementario, no suficiente.</li>'
            '<li><b>Organizations + SCP:</b> las SCP son <b>l&iacute;mites</b> de permisos (guardarra&iacute;les), <b>necesarias pero no suficientes</b>: una SCP no <b>otorga</b> permisos; a&uacute;n necesitas pol&iacute;ticas/roles IAM que concedan el acceso.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"acceso entre cuentas propias, eficiente"? &rarr; <b>IAM role + AssumeRole</b> (cross-account). SCP = l&iacute;mite, no concede.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_aws-accounts.html">docs.aws cross-account roles</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),

    # ================= Q44: STS GetSessionToken (MFA) =================
    card(
        question="Un developer quiere usar <b>MFA</b> para proteger llamadas program&aacute;ticas a operaciones como <code>ec2:StopInstances</code>. Necesita una API donde <b>enviar el c&oacute;digo MFA</b> de su dispositivo y recibir credenciales temporales para luego llamar a operaciones que exigen MFA. &iquest;Qu&eacute; API de STS usa?",
        options=[
            "GetSessionToken",
            "AssumeRoleWithSAML",
            "AssumeRoleWithWebIdentity",
            "GetFederationToken",
        ],
        correct=0,
        key="dva08-q44-getsessiontoken-mfa",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; GetSessionToken.</div>'
            '<p><b>GetSessionToken</b> devuelve credenciales temporales (access key, secret key y session token) para una cuenta AWS o un IAM user. Es la API t&iacute;pica para <b>proteger con MFA</b> llamadas program&aacute;ticas: el usuario con MFA habilitado llama a GetSessionToken <b>enviando su c&oacute;digo MFA</b>; con las credenciales devueltas puede invocar operaciones que exigen MFA. Si el c&oacute;digo MFA es incorrecto, la API devuelve Access Denied.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>AssumeRoleWithWebIdentity:</b> credenciales para usuarios federados v&iacute;a IdPs p&uacute;blicos (Amazon, Facebook, Google, OpenID). No es para MFA y el escenario no menciona IdP externo.</li>'
            '<li><b>AssumeRoleWithSAML:</b> credenciales para usuarios autenticados por una respuesta <b>SAML</b>. No soporta el flujo MFA de este caso.</li>'
            '<li><b>GetFederationToken:</b> credenciales temporales para un usuario federado, pero <b>no soporta MFA</b>. La correcta para MFA es GetSessionToken.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"MFA + llamadas program&aacute;ticas del propio IAM user"? &rarr; <b>GetSessionToken</b>. SAML &rarr; AssumeRoleWithSAML; IdP p&uacute;blico &rarr; AssumeRoleWithWebIdentity.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html">docs.aws GetSessionToken</a><br>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#stsapi_comparison">docs.aws comparaci&oacute;n STS</a></div>'
        ),
    ),

    # ================= Q47: CodeDeploy Linear deployment config =================
    card(
        question="Una app serverless (varias Lambda) se despliega con SAM y CodeDeploy. En cada despliegue debe desplazarse <b>10% del tr&aacute;fico a la nueva versi&oacute;n cada 10 minutos</b> hasta migrar todo. &iquest;Qu&eacute; deployment configuration de CodeDeploy usas?",
        options=[
            "Linear (incrementos iguales de tr&aacute;fico con el mismo intervalo de minutos entre cada uno)",
            "Canary (el tr&aacute;fico se desplaza en dos incrementos: un porcentaje y luego el resto)",
            "All-at-once (todo el tr&aacute;fico se mueve a la nueva versi&oacute;n de una sola vez)",
            "Immutable (estrategia de Elastic Beanstalk que crea un grupo nuevo de instancias)",
        ],
        correct=0,
        key="dva08-q47-codedeploy-linear",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Linear.</div>'
            '<p>Para Lambda/ECS, CodeDeploy ofrece configuraciones de desplazamiento de tr&aacute;fico. <b>Linear</b> desplaza el tr&aacute;fico en <b>incrementos iguales con el mismo intervalo de minutos</b> entre cada uno (p.ej. 10% cada 10 min). Eso encaja exactamente con el requisito.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Canary:</b> desplaza el tr&aacute;fico en <b>dos incrementos</b> (un % inicial y, tras un intervalo, el resto de golpe). No es "10% cada 10 min" continuo.</li>'
            '<li><b>All-at-once:</b> mueve <b>todo</b> el tr&aacute;fico a la nueva versi&oacute;n de una sola vez. Sin incrementos.</li>'
            '<li><b>Immutable:</b> es una estrategia de <b>Elastic Beanstalk</b>, no una deployment configuration de CodeDeploy para Lambda.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"X% cada Y minutos, incrementos iguales"? &rarr; <b>Linear</b>. &iquest;"dos pasos" (un % y luego el resto)? &rarr; Canary. &iquest;"todo de golpe"? &rarr; All-at-once.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html">docs.aws CodeDeploy deployment configs</a><br>'
            '<a href="https://tutorialsdojo.com/aws-codedeploy/">tutorialsdojo CodeDeploy</a></div>'
        ),
    ),

    # ================= Q48: Kinesis PutRecord + SequenceNumberForOrdering =================
    card(
        question="App de subastas en tiempo real con Kinesis Data Streams. Reglas: cada puja se procesa <b>una sola vez</b> y un consumidor EC2 debe procesarlas <b>en el mismo orden</b> en que llegaron. &iquest;Qu&eacute; soluci&oacute;n cumple?",
        options=[
            "Incrustar un ID &uacute;nico en cada puja, escribir con la API Kinesis PutRecord y asignar un valor basado en timestamp al par&aacute;metro SequenceNumberForOrdering",
            "Incrustar un ID &uacute;nico en cada puja, escribir con la API Kinesis PutRecords y asignar un valor basado en timestamp al par&aacute;metro PartitionKey",
            "Reemplazar el stream por una cola SQS FIFO y escribir con SendMessage, con un id &uacute;nico en MessageDeduplicationId por puja",
            "Reemplazar el stream por una cola SQS FIFO y escribir con SendMessageBatch, con un id &uacute;nico en MessageDeduplicationId por puja",
        ],
        correct=0,
        key="dva08-q48-kinesis-putrecord-ordering",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; PutRecord + SequenceNumberForOrdering + ID &uacute;nico.</div>'
            '<p>Kinesis tiene dos APIs de escritura: <b>PutRecord</b> (un registro) y <b>PutRecords</b> (lote). <b>PutRecords NO garantiza el orden</b>: un fallo en un registro no detiene los dem&aacute;s, as&iacute; que pueden desordenarse. Para forzar orden usas <b>PutRecord</b> con <b>SequenceNumberForOrdering</b>.</p>'
            '<div class="warn"><span class="h">Matiz clave (el orden es POR SHARD)</span>El orden en Kinesis es <b>por shard</b>, determinado por la <b>partition key</b>. <code>SequenceNumberForOrdering</code> garantiza n&uacute;meros de secuencia estrictamente crecientes <b>solo</b> para escrituras del <b>mismo cliente</b>, a la <b>misma partition key</b> (mismo shard), hechas <b>en serie</b> encadenando el sequence number del PutRecord anterior. NO hay orden global entre shards ni corrige escrituras concurrentes.</div>'
            '<p>Para el "una sola vez", incrustas un <b>ID &uacute;nico</b> en cada registro y el consumidor lleva la cuenta de IDs ya procesados (p.ej. en DynamoDB) para descartar duplicados.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>PutRecords + PartitionKey por timestamp:</b> PutRecords no garantiza orden; el PartitionKey decide el shard, no fuerza el encadenamiento de secuencia.</li>'
            '<li><b>SQS FIFO (SendMessage / SendMessageBatch):</b> FIFO garantiza orden y evita duplicados, pero el escenario <b>exige mantener Kinesis</b> (no cambiar de servicio) y FIFO tiene <b>l&iacute;mites de throughput</b> (~300 msg/s, ~3.000 con batching) frente a la alta tasa de un stream de Kinesis.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"orden en Kinesis"? &rarr; <b>PutRecord + SequenceNumberForOrdering</b>, misma partition key/shard, escritura serial (no PutRecords, no orden global). Dedup &rarr; ID &uacute;nico + registro en DynamoDB.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html">docs.aws PutRecord</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-kinesis/">tutorialsdojo Kinesis</a></div>'
        ),
    ),

    # ================= Q51: RDS Read Replica =================
    card(
        question="Un sitio (ALB + Auto Scaling EC2 + RDS MySQL) va lento al leer art&iacute;culos por un <b>alto n&uacute;mero de lecturas</b> en la BD. Quieren aliviar la carga de lectura con <b>el m&iacute;nimo cambio de c&oacute;digo</b>. &iquest;Qu&eacute; haces?",
        options=[
            "Crear un RDS Read Replica y configurar la app para dirigir las consultas de lectura a esa r&eacute;plica",
            "Lanzar un cl&uacute;ster grande de ElastiCache como cach&eacute; de la BD y aplicar el cambio de c&oacute;digo requerido",
            "Configurar RDS en modo Multi-AZ para que el standby atienda parte de las consultas de lectura del sitio",
            "Subir las instancias EC2 de la capa de aplicaci&oacute;n a un tipo mayor con m&aacute;s CPU y memoria disponibles",
        ],
        correct=0,
        key="dva08-q51-rds-read-replica",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; RDS Read Replica.</div>'
            '<p>Un <b>Read Replica</b> es una copia de solo lectura de la BD que se replica de forma as&iacute;ncrona. Diriges las <b>consultas de lectura</b> a la r&eacute;plica y descargas la instancia principal, escalando horizontalmente para cargas read-heavy. El cambio de c&oacute;digo es m&iacute;nimo: apuntar las lecturas al endpoint de la r&eacute;plica.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>ElastiCache como cach&eacute;:</b> mejora lecturas pero exige <b>bastante c&oacute;digo</b> (l&oacute;gica de cache-aside/invalidaci&oacute;n). El escenario pide m&iacute;nimo cambio de c&oacute;digo.</li>'
            '<li><b>Multi-AZ:</b> mejora la <b>disponibilidad</b> (failover), <b>no</b> el rendimiento de lectura: el standby no atiende lecturas.</li>'
            '<li><b>Instancias EC2 mayores:</b> el cuello de botella est&aacute; en la <b>BD</b>, no en los servidores de aplicaci&oacute;n. Escalar EC2 no ayuda.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"escalar lecturas, m&iacute;nimo c&oacute;digo"? &rarr; <b>Read Replica</b>. Multi-AZ = disponibilidad, no lectura. Cache = m&aacute;s c&oacute;digo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/rds/features/read-replicas/">aws.amazon RDS Read Replicas</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-relational-database-service-amazon-rds/">tutorialsdojo RDS</a></div>'
        ),
    ),

    # ================= Q52: DynamoDB TTL =================
    card(
        question="Una app usa Amplify DataStore que sincroniza estado de sesi&oacute;n en una tabla DynamoDB. La tabla crece much&iacute;simo. Debes <b>reducir el almacenamiento y el costo de datos irrelevantes SIN usar provisioned throughput</b>. &iquest;Qu&eacute; soluci&oacute;n es la m&aacute;s costo-efectiva?",
        options=[
            "Activar Time To Live (TTL) en la tabla para que expiren y se borren los items obsoletos",
            "Usar una Lambda con EventBridge que purgue los items obsoletos de la tabla a diario",
            "Implementar una estrategia de caching Write-Through en la app para los items de sesi&oacute;n",
            "Implementar una estrategia de caching Lazy Loading en la app para los items de sesi&oacute;n",
        ],
        correct=0,
        key="dva08-q52-dynamodb-ttl",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; activar TTL en la tabla DynamoDB.</div>'
            '<p><b>Time To Live (TTL)</b> de DynamoDB permite definir, por item, un timestamp de expiraci&oacute;n; DynamoDB <b>borra autom&aacute;ticamente</b> los items vencidos. Es <b>gratis</b> y <b>no consume</b> el throughput aprovisionado, justo lo que pide el escenario. Ideal para datos que pierden relevancia con el tiempo: sesiones, logs de eventos, datos temporales.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda + EventBridge para purgar a diario:</b> funciona pero requiere <b>m&aacute;s configuraci&oacute;n</b> y las escrituras de borrado <b>consumen WCU</b> (costo extra). TTL lo hace sin coste ni throughput.</li>'
            '<li><b>Write-Through caching:</b> escribe a la cach&eacute; al escribir a la BD; mejora lecturas, <b>no borra</b> items obsoletos de la tabla. No aplica.</li>'
            '<li><b>Lazy Loading caching:</b> carga a cach&eacute; solo al leer; tampoco expira ni borra los items obsoletos de DynamoDB.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"borrar datos que caducan, sin costo ni throughput"? &rarr; <b>DynamoDB TTL</b>. Ojo: distinto del TTL de una cach&eacute; (ElastiCache).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html">docs.aws DynamoDB TTL</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),

    # ================= Q56: Elastic Beanstalk Blue/Green =================
    card(
        question="Una app en Elastic Beanstalk corre en runtime <b>Java 7</b> y debe subir a <b>Java 8</b> (cambio de runtime). Todo el tr&aacute;fico debe ir <b>de inmediato</b> a la nueva versi&oacute;n y, si hay problemas, poder <b>revertir r&aacute;pido</b>. &iquest;Qu&eacute; acci&oacute;n es la m&aacute;s apropiada?",
        options=[
            "Realizar un Blue/Green Deployment (nuevo entorno + swap de CNAMEs para el cambio instant&aacute;neo)",
            "Actualizar la platform version del entorno a Java 8 con el update de plataforma est&aacute;ndar",
            "Realizar un Traffic splitting deployment liberando la nueva versi&oacute;n a un subconjunto de usuarios",
            "Actualizar manualmente el runtime de Java en las instancias EC2 del entorno una por una",
        ],
        correct=0,
        key="dva08-q56-beanstalk-bluegreen",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Blue/Green Deployment.</div>'
            '<p>En Elastic Beanstalk hay dos m&eacute;todos de update de plataforma. Cuando cambias de <b>runtime, web/app server o major platform version</b> (como Java 7 &rarr; Java 8), AWS recomienda <b>Blue/Green</b>: despliegas la nueva versi&oacute;n en un <b>entorno separado</b> (green) y luego <b>intercambias los CNAMEs</b> para dirigir todo el tr&aacute;fico <b>al instante</b>. Si algo falla, vuelves a intercambiar CNAMEs para <b>revertir r&aacute;pido</b> al entorno viejo (blue).</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Actualizar la platform version del entorno:</b> es el m&eacute;todo recomendado solo cuando <b>NO</b> cambias runtime/web server ni major version. Aqu&iacute; s&iacute; cambia el runtime.</li>'
            '<li><b>Traffic splitting:</b> libera la nueva versi&oacute;n a un <b>subconjunto</b> de usuarios de forma incremental; el escenario exige mover <b>todo el tr&aacute;fico de inmediato</b>.</li>'
            '<li><b>Actualizar Java a mano en las EC2:</b> mucha configuraci&oacute;n y riesgo operativo (el entorno puede caerse durante el cambio). Blue/Green es m&aacute;s seguro y con rollback instant&aacute;neo.</li>'
            '</ul>'
            '<div class="warn"><span class="h">Ojo (RDS)</span>Blue/Green requiere que la BD sea <b>independiente</b> del entorno. Si el RDS est&aacute; acoplado al entorno de Beanstalk, los datos no pasan al nuevo entorno y se pierden al terminar el original.</div>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"cambio de runtime/major version + switch instant&aacute;neo + rollback r&aacute;pido" en Beanstalk? &rarr; <b>Blue/Green (swap CNAME)</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.platform.upgrade.html#using-features.platform.upgrade.bluegreen">docs.aws Beanstalk Blue/Green</a><br>'
            '<a href="https://tutorialsdojo.com/aws-elastic-beanstalk/">tutorialsdojo Beanstalk</a></div>'
        ),
    ),

    # ================= Q60: CodeDeploy agent + platforms + in-place =================
    card(
        question="Sobre AWS CodeDeploy, &iquest;cu&aacute;les DOS afirmaciones son correctas? (elige el par correcto)",
        options=[
            "CodeDeploy puede desplegar a instancias EC2 y tambi&eacute;n a servidores on-premises; y los despliegues a Lambda NO pueden usar el tipo in-place",
            "El agente de CodeDeploy se comunica por HTTP en el puerto 80; y CodeDeploy solo despliega a EC2, Lambda y ECS",
            "Debes instalar el agente de CodeDeploy en las instancias EC2 y en el cl&uacute;ster ECS; y Lambda solo admite in-place",
            "CodeDeploy solo despliega a EC2, Lambda y ECS; y el agente se comunica por HTTP en el puerto 80",
        ],
        correct=0,
        key="dva08-q60-codedeploy-agent-platforms",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; EC2 + on-premises; y Lambda no usa in-place.</div>'
            '<p>CodeDeploy despliega a <b>EC2, on-premises, Lambda y ECS</b>. Dos hechos clave: (1) <b>solo</b> EC2/On-Premises pueden usar el tipo <b>in-place</b>; los despliegues a <b>Lambda</b> son siempre <b>blue/green</b> (traffic shifting), nunca in-place. (2) El <b>agente CodeDeploy</b> se comunica <b>saliente por HTTPS en el puerto 443</b>, y solo se necesita para la plataforma <b>EC2/On-Premises</b> (no para Lambda ni ECS).</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>"agente por HTTP puerto 80":</b> falso, es <b>HTTPS 443</b>.</li>'
            '<li><b>"solo EC2, Lambda y ECS":</b> incompleto, tambi&eacute;n despliega a <b>on-premises</b>.</li>'
            '<li><b>"instalar el agente en EC2 y en el cl&uacute;ster ECS":</b> falso para ECS: el agente <b>no</b> se requiere en ECS ni en Lambda, solo en EC2/On-Premises.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Agente CodeDeploy = <b>HTTPS 443</b>, solo EC2/On-Prem. Lambda = siempre blue/green (nunca in-place).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent.html">docs.aws CodeDeploy agent</a><br>'
            '<a href="https://tutorialsdojo.com/aws-codedeploy/">tutorialsdojo CodeDeploy</a></div>'
        ),
    ),

    # ================= Q62: IAM Policy Simulator =================
    card(
        question="Usando AWS Organizations, quieres <b>probar el impacto de SCPs sobre tus IAM policies y resource policies antes de aplicarlas</b>, sin ejecutar acciones reales. &iquest;Qu&eacute; servicio usas para probar y depurar pol&iacute;ticas IAM y basadas en recursos?",
        options=[
            "IAM Policy Simulator",
            "AWS Config",
            "AWS Systems Manager",
            "Amazon Inspector",
        ],
        correct=0,
        key="dva08-q62-iam-policy-simulator",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; IAM Policy Simulator.</div>'
            '<p>El <b>IAM Policy Simulator</b> eval&uacute;a las pol&iacute;ticas que elijas y determina los permisos efectivos por cada acci&oacute;n, usando el <b>mismo motor de evaluaci&oacute;n</b> que las peticiones reales, pero <b>sin</b> hacer llamadas reales al servicio (seguro para probar). Puede probar pol&iacute;ticas de usuarios/grupos/roles, pol&iacute;ticas basadas en recursos, y &mdash;si la cuenta est&aacute; en una Organization&mdash; el <b>impacto de las SCPs</b> sobre tus pol&iacute;ticas. Devuelve Allow/Deny e identifica qu&eacute; sentencia decide.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>AWS Config:</b> eval&uacute;a/auditar&iacute;a la <b>configuraci&oacute;n</b> de recursos y su cumplimiento; no simula permisos de pol&iacute;ticas.</li>'
            '<li><b>Systems Manager:</b> gesti&oacute;n operativa unificada y automatizaci&oacute;n de tareas; no simula pol&iacute;ticas.</li>'
            '<li><b>Amazon Inspector:</b> evaluaci&oacute;n automatizada de <b>seguridad/vulnerabilidades</b> de apps; no eval&uacute;a permisos IAM.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"probar/depurar permisos de pol&iacute;ticas (incl. impacto de SCPs) sin ejecutar acciones"? &rarr; <b>IAM Policy Simulator</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html">docs.aws Policy Simulator</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(deck_name="DVA-C02::08", cards=cards, out_path="out/DVA-C02_08.apkg")
