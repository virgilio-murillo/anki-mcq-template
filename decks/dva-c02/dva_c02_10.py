#!/usr/bin/env python3
"""
DVA-C02::10 - "Risk" cards: the 10 questions from a 65-question practice set most
likely to be failed, chosen by cross-referencing against the topics ALREADY covered
in the user's Anki decks DVA-C02::01-07 (148 cards) and the prior failed sets.

Selected questions (all GAP or weakly-covered topics):
  Q2  Step Functions: Catch + ResultPath (vs Parameters / ItemsPath)
  Q6  AWS CDK: cdk bootstrap on NoSuchBucket
  Q47 SAM local testing of CDK: cdk synth + sam local invoke
  Q21 Lambda Function URL: FunctionUrlAuthType NONE + custom auth
  Q58 DynamoDB BatchGetItem: UnprocessedKeys + exponential backoff + SDK
  Q40 DynamoDB: rate-limited PARALLEL scan
  Q48 DynamoDB fine-grained access: dynamodb:LeadingKeys
  Q43 STS: decode-authorization-message
  Q55 CloudWatch Embedded Metric Format (EMF)
  Q31 STS: GetSessionToken (MFA-protected API calls)

Each question is decomposed into 2-3 one-concept cards, same house style as ::01-08.
Quality gate (verify_cards/verify_apkg) applied: 4 balanced options, {{L}} verdict,
every distractor refuted, unique keys, links with href.
"""
from anki_mcq import card, create

cards = [
    # ================= Q2: Step Functions Catch + ResultPath =================
    card(
        question="Un workflow de Step Functions con 4 states maneja la l&oacute;gica y los errores. Si el proceso <b>falla</b>, hay que <b>agregar en un solo output todos los datos</b> que pasaron por los nodos (input + error + output). &iquest;Qu&eacute; usas?",
        options=[
            "Un campo <code>Catch</code> en la definici&oacute;n del state machine y <code>ResultPath</code> para unir el input de cada nodo con su output",
            "Un campo <code>Catch</code> en la definici&oacute;n del state machine y <code>ItemsPath</code> para unir el input de cada nodo con su output",
            "Un campo <code>Parameters</code> en la definici&oacute;n del state machine y <code>ResultPath</code> para unir el input de cada nodo con su output",
            "Un campo <code>Parameters</code> en la definici&oacute;n del state machine e <code>ItemsPath</code> para unir el input de cada nodo con su output",
        ],
        correct=0,
        key="dva10-q2-catch-resultpath",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Catch para capturar el error y ResultPath para agregar input+output.</div>'
            '<p>El campo <code>Catch</code> (v&aacute;lido en <b>Task</b>, <b>Parallel</b> y <b>Map</b> states) captura el error: es un array de "catchers" con <code>ErrorEquals</code>, <code>Next</code> y <code>ResultPath</code>. El <code>ResultPath</code> controla qu&eacute; combinaci&oacute;n de <b>input y resultado</b> se pasa al output del state, permitiendo <b>agregar en un solo paso</b> el input, el error y el output de cada nodo.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>Parameters</code>: solo arma pares clave-valor (est&aacute;ticos o tomados del input) para pasar a la integraci&oacute;n; <b>no</b> captura errores de un state.</li>'
            '<li><code>ItemsPath</code>: solo aplica en un <b>Map state</b> (para iterar sobre una lista); no sirve para agregar input+output aqu&iacute;.</li>'
            '<li>La combinaci&oacute;n <code>Parameters</code> + <code>ItemsPath</code> falla por partida doble: ni captura el error ni corresponde a este caso.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Capturar error &rarr; <code>Catch</code>. Combinar input+resultado en el output &rarr; <code>ResultPath</code>. Iterar una lista &rarr; <code>ItemsPath</code> (solo Map).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html">docs.aws Step Functions error handling</a><br>'
            '<a href="https://tutorialsdojo.com/aws-step-functions/">tutorialsdojo Step Functions</a></div>'
        ),
    ),
    card(
        question="En Amazon States Language (Step Functions), &iquest;para qu&eacute; sirve cada campo: <code>Catch</code>, <code>Retry</code>, <code>ResultPath</code> y <code>ItemsPath</code>?",
        options=[
            "Catch captura errores y transiciona a otro state; Retry reintenta; ResultPath combina input y resultado; ItemsPath elige la lista a iterar en un Map",
            "Catch reintenta con backoff; Retry captura errores; ResultPath elige la lista del Map; ItemsPath combina input y resultado del state",
            "Catch e ItemsPath capturan errores; Retry y ResultPath solo definen el orden de ejecuci&oacute;n entre states del workflow",
            "Catch arma pares clave-valor para la integraci&oacute;n; Retry itera listas; ResultPath captura errores; ItemsPath reintenta el state",
        ],
        correct=0,
        key="dva10-q2-asl-fields",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; cada campo tiene un rol distinto en ASL.</div>'
            '<p><code>Catch</code>: array de catchers; cuando el error coincide con <code>ErrorEquals</code>, transiciona al state en <code>Next</code>. <code>Retry</code>: array de retriers; reintenta el mismo state (con <code>IntervalSeconds</code>, <code>MaxAttempts</code>, <code>BackoffRate</code>). <code>ResultPath</code>: decide qu&eacute; parte del input y del resultado sigue en el output. <code>ItemsPath</code>: solo en un <b>Map state</b>, apunta a la lista sobre la que se itera.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> confunden los roles (Retry no captura errores; ResultPath no elige listas; Catch no arma Parameters). Solo la primera asigna correctamente cada campo.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Si no hay <code>Retry</code> o los reintentos fallan, Step Functions recorre los <code>Catch</code> en orden hasta encontrar un <code>ErrorEquals</code> que coincida.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultpath.html">docs.aws ResultPath</a></div>'
        ),
    ),

    # ================= Q6: CDK bootstrap =================
    card(
        question="Un equipo despliega una app serverless con AWS CDK (<code>cdk deploy</code>). En una <b>cuenta AWS nueva</b> el primer despliegue falla con <code>NoSuchBucket</code>. No cambiaron el c&oacute;digo ni la config del CDK. &iquest;Qu&eacute; comando del CDK CLI hay que correr primero?",
        options=[
            "<code>cdk bootstrap</code>",
            "<code>cdk synth</code>",
            "<code>cdk context</code>",
            "<code>cdk import</code>",
        ],
        correct=0,
        key="dva10-q6-cdk-bootstrap",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; cdk bootstrap.</div>'
            '<p>El error <code>NoSuchBucket</code> indica que el CDK intenta usar un <b>bucket de assets de S3</b> que no existe en la cuenta/regi&oacute;n nueva. El CDK guarda ah&iacute; los artefactos de despliegue (c&oacute;digo Lambda, im&aacute;genes Docker). <code>cdk bootstrap</code> provisiona esos recursos base (bucket S3, roles IAM, ECR) en ese entorno. Hay que ejecutarlo una vez por cada cuenta+regi&oacute;n nueva.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>cdk synth</code>: solo genera la plantilla CloudFormation a partir del c&oacute;digo; no crea recursos en la cuenta.</li>'
            '<li><code>cdk context</code>: solo cachea informaci&oacute;n del entorno (AZs, VPCs) que el CDK consulta; no aprovisiona nada.</li>'
            '<li><code>cdk import</code>: importa recursos ya existentes a un stack v&iacute;a CloudFormation; no crea el bucket de assets faltante.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Cuenta o regi&oacute;n <b>nueva</b> + error de bucket/roles de assets del CDK &rarr; <code>cdk bootstrap</code> (una sola vez por cuenta+regi&oacute;n).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html">docs.aws CDK bootstrapping</a><br>'
            '<a href="https://tutorialsdojo.com/aws-cloud-development-kit-cdk/">tutorialsdojo CDK</a></div>'
        ),
    ),
    card(
        question="En AWS CDK, &iquest;qu&eacute; hace cada comando: <code>bootstrap</code>, <code>synth</code>, <code>context</code> e <code>import</code>?",
        options=[
            "bootstrap provisiona los recursos base del entorno; synth genera el template; context cachea datos del entorno; import trae recursos existentes al stack",
            "bootstrap genera el template CloudFormation; synth provisiona el entorno; context importa recursos; import cachea datos del entorno en el proyecto",
            "bootstrap importa recursos existentes; synth cachea datos del entorno; context provisiona el bucket de assets; import genera el template del stack",
            "bootstrap cachea AZs y VPCs; synth importa recursos al stack; context genera el template; import provisiona los roles IAM del entorno CDK",
        ],
        correct=0,
        key="dva10-q6-cdk-commands",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; cada comando cumple una funci&oacute;n distinta.</div>'
            '<p><code>bootstrap</code>: prepara el entorno (bucket S3 de assets, roles, ECR) en una cuenta+regi&oacute;n. <code>synth</code>: "compila" el c&oacute;digo CDK a una plantilla CloudFormation. <code>context</code>: cachea informaci&oacute;n del entorno (AZs, VPCs) que el CDK consulta al sintetizar. <code>import</code>: incorpora recursos ya existentes a un stack v&iacute;a CloudFormation resource imports.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> intercambian las definiciones (synth no aprovisiona, context no importa, import no genera el template). Solo la primera las asigna bien.</p>'
            '<div class="extra"><span class="h">Dato extra</span>El flujo t&iacute;pico: <code>bootstrap</code> (una vez por entorno) &rarr; escribir el c&oacute;digo &rarr; <code>synth</code> &rarr; <code>deploy</code>.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/cdk/v2/guide/cli.html">docs.aws CDK CLI</a></div>'
        ),
    ),

    # ================= Q47: SAM local + CDK =================
    card(
        question="Una API serverless est&aacute; definida con constructs L2 de AWS CDK. El desarrollador quiere <b>probar localmente</b> algunas funciones Lambda (SAM y CDK ya configurados). &iquest;Qu&eacute; dos acciones combina? (marca el par correcto)",
        options=[
            "Correr <code>cdk synth</code> para el stack y luego <code>sam local invoke</code> apuntando al template sintetizado y al identificador de cada funci&oacute;n",
            "Correr <code>cdk bootstrap</code> para preparar los assets y luego <code>sam local invoke</code> apuntando al template sintetizado de cada funci&oacute;n",
            "Correr <code>sam package</code> para subir el c&oacute;digo a un bucket S3 y luego <code>cdk synth</code> para invocar cada funci&oacute;n en local",
            "Correr <code>cdk synth</code> para el stack y luego <code>sam local start-lambda</code> para levantar el endpoint que emula el servicio Lambda",
        ],
        correct=0,
        key="dva10-q47-cdk-synth-sam-invoke",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; cdk synth + sam local invoke.</div>'
            '<p><code>sam local invoke</code> prueba funciones Lambda localmente emulando el entorno de ejecuci&oacute;n, pero necesita un template que SAM entienda. Como los recursos est&aacute;n en CDK, primero se ejecuta <code>cdk synth</code> para "compilar" el CDK a una plantilla <b>CloudFormation</b>; luego <code>sam local invoke</code> usa esa plantilla y el identificador de cada funci&oacute;n para ejecutarla.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>cdk bootstrap</code>: solo prepara la cuenta para despliegues; no es parte de las pruebas locales.</li>'
            '<li><code>sam package</code>: empaqueta y sube a S3 para desplegar en AWS; no prueba en local.</li>'
            '<li><code>sam local start-lambda</code>: levanta un endpoint que emula el servicio Lambda (&uacute;til si otro servicio invoca la funci&oacute;n); para probar funciones puntuales una a una, <code>sam local invoke</code> es lo directo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Probar CDK con SAM en local: <code>cdk synth</code> (genera template) &rarr; <code>sam local invoke</code> (ejecuta la funci&oacute;n). Invocar 1 funci&oacute;n &rarr; invoke; emular el servicio &rarr; start-lambda.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-invoke.html">docs.aws sam local invoke</a><br>'
            '<a href="https://tutorialsdojo.com/aws-cloud-development-kit-cdk/">tutorialsdojo CDK</a></div>'
        ),
    ),

    # ================= Q21: Lambda Function URL =================
    card(
        question="Una plataforma externa manda <b>webhooks</b> por HTTPS a una Lambda y <b>firma cada request con una clave secreta en los headers</b>. La funci&oacute;n debe ejecutar la l&oacute;gica solo si el request viene de un origen v&aacute;lido, con el <b>m&iacute;nimo esfuerzo</b>. &iquest;Qu&eacute; haces?",
        options=[
            "Crear una Lambda Function URL con <code>FunctionUrlAuthType: NONE</code> y validar la firma de los headers con l&oacute;gica propia en la funci&oacute;n",
            "Crear una Lambda Function URL con <code>FunctionUrlAuthType: AWS_IAM</code> para que solo un usuario o rol IAM autorizado pueda invocarla",
            "Crear una Lambda Function URL con la condici&oacute;n <code>lambda:CodeSigningConfigArn</code> para que solo se invoque con c&oacute;digo firmado",
            "Configurar API Gateway con integraci&oacute;n proxy y un Lambda authorizer que valide la firma provista en los headers del request",
        ],
        correct=0,
        key="dva10-q21-function-url-none",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Function URL con AuthType NONE + validaci&oacute;n propia de la firma.</div>'
            '<p>Una <b>Lambda Function URL</b> es un endpoint HTTPS directo sobre la funci&oacute;n, sin configurar servicios extra (m&iacute;nimo esfuerzo). Con <code>FunctionUrlAuthType: NONE</code> el endpoint es p&uacute;blico, as&iacute; que la plataforma externa puede llamarlo; luego la funci&oacute;n <b>valida la firma</b> de los headers para confirmar que el request viene de un origen de confianza.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>AWS_IAM</code>: exige que quien llama sea un usuario/rol IAM firmando con SigV4; la plataforma externa firma con <b>su propia</b> clave, no con IAM, as&iacute; que no aplica.</li>'
            '<li><code>lambda:CodeSigningConfigArn</code>: es code signing (verifica la integridad del c&oacute;digo desplegado), no la autenticaci&oacute;n de requests entrantes.</li>'
            '<li><b>API Gateway + Lambda authorizer</b>: funciona, pero agrega configuraci&oacute;n de un servicio extra solo para invocar una &uacute;nica funci&oacute;n; no es el m&iacute;nimo esfuerzo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Webhook firmado por un tercero + m&iacute;nimo esfuerzo &rarr; Function URL <code>NONE</code> + validar firma en el c&oacute;digo. IAM firma con SigV4 (no sirve para terceros).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/lambda/latest/dg/lambda-urls.html">docs.aws Lambda function URLs</a><br>'
            '<a href="https://tutorialsdojo.com/aws-lambda/">tutorialsdojo Lambda</a></div>'
        ),
    ),
    card(
        question="En una <b>Lambda Function URL</b>, &iquest;qu&eacute; diferencia hay entre los tipos de autorizaci&oacute;n <code>AWS_IAM</code> y <code>NONE</code>?",
        options=[
            "AWS_IAM exige que quien invoca sea un usuario o rol IAM autorizado (firma SigV4); NONE la deja p&uacute;blica y t&uacute; validas el request en el c&oacute;digo",
            "AWS_IAM deja la funci&oacute;n p&uacute;blica sin autenticaci&oacute;n; NONE exige que quien invoca sea un usuario o rol IAM autorizado con permisos",
            "AWS_IAM valida un token OAuth o JWT en el header Authorization; NONE valida un certificado TLS mutuo entre el cliente y la funci&oacute;n",
            "AWS_IAM firma la respuesta de la funci&oacute;n con KMS; NONE cifra el payload de entrada usando la clave por defecto de la cuenta",
        ],
        correct=0,
        key="dva10-q21-authtype-diff",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; AWS_IAM restringe a identidades IAM; NONE es p&uacute;blico y validas t&uacute;.</div>'
            '<p>Con <code>AWS_IAM</code>, solo un usuario o rol IAM con los permisos necesarios puede invocar la Function URL (la petici&oacute;n va firmada con SigV4). Con <code>NONE</code>, cualquiera puede invocarla; si necesitas restringir el origen (p. ej. un webhook firmado por un tercero), debes <b>validar el request dentro de la funci&oacute;n</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> invierten los roles (NONE no es IAM), o inventan mecanismos (Function URL no hace OAuth/JWT ni mTLS ni cifrado por AuthType; eso ser&iacute;a l&oacute;gica propia o API Gateway).</p>'
            '<div class="extra"><span class="h">Dato extra</span>Solo hay dos AuthType para Function URLs: <code>AWS_IAM</code> y <code>NONE</code>. Para OAuth/JWT usar&iacute;as API Gateway con un authorizer.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html">docs.aws Function URL auth</a></div>'
        ),
    ),

    # ================= Q58: BatchGetItem UnprocessedKeys =================
    card(
        question="Un script usa la API de bajo nivel <code>BatchGetItem</code> de DynamoDB y a menudo recibe resultados parciales: buena parte de las claves vuelve en <code>UnprocessedKeys</code>. &iquest;Qu&eacute; dos enfoques dan la recuperaci&oacute;n M&Aacute;S fiable? (marca el par correcto)",
        options=[
            "Implementar backoff exponencial con jitter entre reintentos del batch, y usar el AWS SDK (que trae reintentos y backoff autom&aacute;ticos)",
            "Reintentar el batch de inmediato sin espera, y aumentar los RCU de la tabla habilitando Auto Scaling para absorber los picos",
            "Crear un Global Secondary Index con su propia capacidad de lectura, y reintentar el batch de inmediato sobre el &iacute;ndice creado",
            "Aumentar los RCU de la tabla con Auto Scaling, y crear un Global Secondary Index con capacidad de lectura dedicada para el batch",
        ],
        correct=0,
        key="dva10-q58-backoff-sdk",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; backoff exponencial con jitter + usar el AWS SDK.</div>'
            '<p><code>BatchGetItem</code> devuelve resultados parciales si se supera el l&iacute;mite de tama&ntilde;o (16 MB / 100 items), si se excede el throughput o por fallos internos; las claves no le&iacute;das vuelven en <code>UnprocessedKeys</code>. Lo recomendado es <b>reintentar esas claves con backoff exponencial y jitter</b>. El <b>AWS SDK</b> ya trae esa l&oacute;gica de reintentos y backoff, as&iacute; que usarlo es la forma m&aacute;s fiable.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Reintentar de inmediato:</b> tiene m&aacute;s chance de volver a fallar por throttling que de tener &eacute;xito; por eso se espacian los reintentos.</li>'
            '<li><b>Subir RCU + Auto Scaling:</b> ayuda con el throughput, pero <code>BatchGetItem</code> puede devolver parciales igual (l&iacute;mite de 16 MB por respuesta); no es lo m&aacute;s fiable para manejar <code>UnprocessedKeys</code>.</li>'
            '<li><b>Crear un GSI:</b> no cambia el comportamiento de <code>BatchGetItem</code> ni ayuda con <code>UnprocessedKeys</code>.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;<code>UnprocessedKeys</code> / <code>UnprocessedItems</code>? &rarr; reintentar esas claves con <b>backoff exponencial + jitter</b>, idealmente v&iacute;a el SDK. Nunca reintentar de inmediato.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html#Programming.Errors.BatchOperations">docs.aws DynamoDB batch errors</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),

    # ================= Q40: rate-limited parallel scan =================
    card(
        question="Un developer quiere <b>reducir el tiempo</b> de un <code>Scan</code> de DynamoDB en horas de baja demanda <b>sin afectar</b> las cargas normales. El scan consume la mitad de los RCU fuertemente consistentes en horario normal. &iquest;C&oacute;mo lo mejora?",
        options=[
            "Ejecutar un scan en paralelo con l&iacute;mite de tasa (rate-limited parallel scan)",
            "Ejecutar un scan secuencial con l&iacute;mite de tasa (rate-limited sequential scan)",
            "Ejecutar un scan en paralelo sin ning&uacute;n l&iacute;mite de tasa para maximizar el throughput",
            "Usar lecturas eventualmente consistentes en lugar de fuertemente consistentes en el scan",
        ],
        correct=0,
        key="dva10-q40-rate-limited-parallel-scan",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; scan en paralelo con l&iacute;mite de tasa.</div>'
            '<p>Por defecto <code>Scan</code> es <b>secuencial</b> y lee una partici&oacute;n a la vez, as&iacute; que su throughput lo limita una sola partici&oacute;n. Un <b>parallel scan</b> divide la tabla en segmentos y varios workers los leen a la vez, aprovechando todas las particiones y reduciendo el tiempo. Pero un parallel scan sin control puede consumir <b>todo</b> el throughput y provocar throttling en la app; por eso hay que <b>limitar la tasa</b> (rate-limiting) del cliente.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Sequential con rate limit:</b> el scan ya es secuencial por defecto; no hay mejora de tiempo.</li>'
            '<li><b>Parallel sin rate limit:</b> puede acaparar el throughput y afectar la carga normal (contra el requisito).</li>'
            '<li><b>Lecturas eventuales:</b> abaratan el costo pero el scan sigue siendo secuencial; no acelera nada.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Acelerar un Scan grande sin da&ntilde;ar la app &rarr; <b>parallel scan + rate limiting</b>. Parallel solo = riesgo de throttle. Eventual reads = solo costo, no velocidad.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html#Scan.ParallelScan">docs.aws DynamoDB parallel scan</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),

    # ================= Q48: dynamodb:LeadingKeys =================
    card(
        question="Con Web Identity Federation, cada usuario debe acceder <b>solo a los items cuya partition key es su propio user ID</b> en una tabla DynamoDB. &iquest;Qu&eacute; condition key pones en la pol&iacute;tica IAM del rol del proveedor de identidad?",
        options=[
            "<code>dynamodb:LeadingKeys</code>",
            "<code>dynamodb:Attributes</code>",
            "<code>dynamodb:Select</code>",
            "<code>dynamodb:ReturnValues</code>",
        ],
        correct=0,
        key="dva10-q48-leadingkeys",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; dynamodb:LeadingKeys.</div>'
            '<p>El fine-grained access control de DynamoDB se hace con el elemento <code>Condition</code> de una pol&iacute;tica IAM. <code>dynamodb:LeadingKeys</code> restringe el acceso a los <b>items cuya partition key</b> coincide con el identificador del usuario (p. ej. el sub de la identidad federada), de modo que cada usuario solo ve <b>sus</b> items.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>dynamodb:Attributes</code>: limita a qu&eacute; <b>atributos</b> (columnas) se accede, no a qu&eacute; items.</li>'
            '<li><code>dynamodb:Select</code>: controla qu&eacute; atributos devuelve un Query/Scan; no restringe por partition key.</li>'
            '<li><code>dynamodb:ReturnValues</code>: controla si se devuelven los valores antes/despu&eacute;s de un update; no es control de acceso por item.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Restringir por <b>partition key</b> (items del propio usuario) &rarr; <code>dynamodb:LeadingKeys</code>. Restringir <b>atributos</b> &rarr; <code>dynamodb:Attributes</code>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html">docs.aws DynamoDB fine-grained access</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),

    # ================= Q43: STS decode-authorization-message =================
    card(
        question="Al correr <code>stop-instance</code> por el AWS CLI recibes un <code>UnauthorizedOperation</code> con un mensaje de fallo adicional en <b>texto cifrado (encoded)</b>. &iquest;C&oacute;mo decodificas ese mensaje?",
        options=[
            "Llamar al comando <code>sts decode-authorization-message</code> del AWS STS",
            "Llamar al comando <code>iam decode-authorization-message</code> del AWS IAM",
            "Llamar al comando <code>kms decrypt</code> del AWS KMS con la clave por defecto",
            "Decodificarlo con una librer&iacute;a de criptograf&iacute;a externa fuera de AWS",
        ],
        correct=0,
        key="dva10-q43-decode-auth-message",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; sts decode-authorization-message.</div>'
            '<p>Cuando una operaci&oacute;n devuelve <code>UnauthorizedOperation</code> (HTTP 403), a veces incluye un <b>mensaje codificado</b> con detalles de por qu&eacute; fall&oacute; la autorizaci&oacute;n. Se decodifica con la API <code>DecodeAuthorizationMessage</code> de <b>AWS STS</b> (CLI: <code>sts decode-authorization-message</code>). El llamante necesita el permiso <code>sts:DecodeAuthorizationMessage</code>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>kms decrypt</code>: el mensaje no est&aacute; cifrado con una KMS key, as&iacute; que KMS no puede descifrarlo.</li>'
            '<li><code>iam decode-authorization-message</code>: ese comando no existe en IAM; la acci&oacute;n vive en STS.</li>'
            '<li><b>Librer&iacute;a externa:</b> el mensaje lo genera STS; solo STS puede decodificarlo, no una herramienta de terceros.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Mensaje "encoded" tras un <code>UnauthorizedOperation</code> &rarr; <code>sts decode-authorization-message</code> (no KMS, no IAM).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html">docs.aws STS DecodeAuthorizationMessage</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),

    # ================= Q55: CloudWatch Embedded Metric Format =================
    card(
        question="Un equipo necesita <b>extraer m&eacute;tricas personalizadas</b> (p. ej. tiempos de procesamiento) directamente de los <b>logs</b> de una Lambda, analizarlas y poner alarmas en tiempo real. &iquest;Qu&eacute; enfoque usas?",
        options=[
            "Formatear los logs con el Embedded Metric Format (EMF) de CloudWatch usando las librer&iacute;as open-source, y monitorear y alarmar esas m&eacute;tricas en CloudWatch",
            "Enviar las m&eacute;tricas a Amazon EventBridge con <code>PutMetricData</code> y crear reglas de EventBridge que disparen acciones seg&uacute;n cada m&eacute;trica",
            "Usar CloudWatch Lambda Insights para extraer esas m&eacute;tricas custom desde los logs y crear dashboards y alarmas dentro de Lambda Insights",
            "Enviar los logs con Amazon Data Firehose a un cl&uacute;ster de Redshift y correr consultas SQL para analizar m&eacute;tricas y alertar anomal&iacute;as",
        ],
        correct=0,
        key="dva10-q55-emf",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CloudWatch Embedded Metric Format (EMF).</div>'
            '<p>El <b>Embedded Metric Format</b> es una especificaci&oacute;n JSON que hace que CloudWatch Logs <b>extraiga autom&aacute;ticamente</b> valores de m&eacute;tricas embebidos en eventos de log estructurados. Es ideal para recursos ef&iacute;meros (Lambda, contenedores): escribes las m&eacute;tricas junto al log y luego las graficas y les pones <b>alarmas</b> en CloudWatch. Las librer&iacute;as open-source de AWS facilitan formatear los logs en EMF.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>EventBridge + PutMetricData:</b> EventBridge es para arquitecturas dirigidas por eventos; <code>PutMetricData</code> es de CloudWatch, no de EventBridge; no extrae m&eacute;tricas de logs.</li>'
            '<li><b>Lambda Insights:</b> monitorea rendimiento del runtime (CPU, memoria), no extrae m&eacute;tricas custom desde tus logs.</li>'
            '<li><b>Firehose + Redshift:</b> es un pipeline de analytics a gran escala; excesivo para extraer m&eacute;tricas de logs y alarmar en tiempo real.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>M&eacute;tricas custom <b>desde logs</b> de recursos ef&iacute;meros + alarmas en tiempo real &rarr; <b>Embedded Metric Format (EMF)</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html">docs.aws CloudWatch EMF</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cloudwatch/">tutorialsdojo CloudWatch</a></div>'
        ),
    ),

    # ================= Q31: STS GetSessionToken (MFA) =================
    card(
        question="Un developer quiere proteger con <b>MFA</b> llamadas program&aacute;ticas a operaciones como <code>ec2:StopInstances</code>. Necesita una API donde <b>enviar el c&oacute;digo MFA</b> de su dispositivo y recibir credenciales temporales para luego llamar a operaciones que exigen MFA. &iquest;Qu&eacute; API de STS usa?",
        options=[
            "<code>GetSessionToken</code>",
            "<code>GetFederationToken</code>",
            "<code>AssumeRoleWithWebIdentity</code>",
            "<code>AssumeRoleWithSAML</code>",
        ],
        correct=0,
        key="dva10-q31-getsessiontoken",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; GetSessionToken.</div>'
            '<p><code>GetSessionToken</code> devuelve credenciales temporales a un usuario IAM existente y es la &uacute;nica de las opciones que soporta <b>MFA</b>: puedes exigir que las peticiones a AWS solo se permitan cuando el usuario aport&oacute; su c&oacute;digo MFA. Ideal para proteger operaciones sensibles llamadas program&aacute;ticamente.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><code>GetFederationToken</code>: da credenciales temporales a un usuario federado (t&iacute;pico en un proxy con credenciales de largo plazo); no es el mecanismo MFA de este caso.</li>'
            '<li><code>AssumeRoleWithWebIdentity</code>: para usuarios autenticados por un IdP p&uacute;blico (Login with Amazon, Facebook, Google, OIDC).</li>'
            '<li><code>AssumeRoleWithSAML</code>: para usuarios autenticados por un IdP corporativo v&iacute;a SAML 2.0 (AD/OpenLDAP).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Enviar el c&oacute;digo <b>MFA</b> y recibir credenciales temporales para un usuario IAM existente &rarr; <code>GetSessionToken</code>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html">docs.aws STS GetSessionToken</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),
    card(
        question="Distingue las APIs de AWS STS: <code>AssumeRole</code>, <code>AssumeRoleWithWebIdentity</code>, <code>AssumeRoleWithSAML</code>, <code>GetFederationToken</code> y <code>GetSessionToken</code>. &iquest;Cu&aacute;l afirmaci&oacute;n es correcta?",
        options=[
            "GetSessionToken da credenciales temporales a un usuario IAM y soporta MFA; WithWebIdentity usa IdP p&uacute;blico; WithSAML usa IdP corporativo SAML 2.0",
            "GetFederationToken es la &uacute;nica que soporta MFA; WithWebIdentity usa SAML corporativo; WithSAML usa proveedores p&uacute;blicos como Google",
            "AssumeRole solo funciona con IdP p&uacute;blicos; GetSessionToken federa usuarios SAML; WithSAML da credenciales a un usuario IAM con MFA",
            "AssumeRoleWithWebIdentity soporta MFA para usuarios IAM; GetSessionToken federa v&iacute;a Facebook; GetFederationToken usa SAML corporativo",
        ],
        correct=0,
        key="dva10-q31-sts-apis",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; cada API de STS tiene un caso distinto.</div>'
            '<p><code>AssumeRole</code>: un usuario IAM existente asume un rol (incluye poder exigir MFA). <code>AssumeRoleWithWebIdentity</code>: usuarios autenticados por un IdP <b>p&uacute;blico</b> (Login with Amazon, Facebook, Google, OIDC). <code>AssumeRoleWithSAML</code>: usuarios de un IdP <b>corporativo</b> v&iacute;a SAML 2.0. <code>GetFederationToken</code>: credenciales para un usuario federado desde un proxy con credenciales de largo plazo. <code>GetSessionToken</code>: credenciales temporales a un usuario IAM, con soporte de <b>MFA</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> mezclan los proveedores (WebIdentity no es SAML; SAML no es Google) o atribuyen MFA/federaci&oacute;n a la API equivocada.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Regla r&aacute;pida: p&uacute;blico &rarr; WebIdentity; corporativo SAML &rarr; WithSAML; usuario IAM + MFA program&aacute;tico &rarr; GetSessionToken.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html">docs.aws STS API comparison</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(deck_name="DVA-C02::10", cards=cards, out_path="out/DVA-C02_10.apkg")
