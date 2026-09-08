#!/usr/bin/env python3
"""
DVA-C02::06 - Cards from the RANDOMIZED-TEST questions the user got INCORRECT.
Q3 (S3 Object Lambda) is intentionally NOT here (built in ::05, same question).
Source: kiro-notes/source/randomized_failed.txt

Lessons applied: self-contained questions, {{L}} verdict, refute every distractor,
no distractor that collides with the taught rule, no "see next card", real AWS methods.
"""
from anki_mcq import card, create

cards = [
    # ================= Q1: CloudFormation drift detection =================
    card(
        question="Los IAM roles de unas Lambdas gestionadas por CloudFormation fueron <b>modificados a mano</b>. Necesitas identificar esos cambios no autorizados y ver qu&eacute; recursos ya no coinciden con el stack. &iquest;Qu&eacute; haces?",
        options=[
            "Ejecutar una comprobaci&oacute;n de drift detection sobre el stack de CloudFormation",
            "Usar AWS Config para monitorear cambios en las Lambdas y los IAM roles",
            "Revisar los logs de CloudTrail para rastrear los cambios en los IAM roles",
            "Analizar CloudWatch Logs para identificar cambios en los permisos del rol",
        ],
        correct=0,
        key="dva06-q1-drift-detection",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; drift detection del stack.</div>'
            '<p><b>Drift detection</b> compara la configuraci&oacute;n <b>real</b> de los recursos con la <b>esperada</b> definida en la plantilla del stack, y reporta las diferencias ("drift"). Es exactamente lo que detecta cambios hechos <b>fuera</b> de CloudFormation (out-of-band), como una edici&oacute;n manual del IAM role, y te dice qu&eacute; propiedades ya no coinciden con el stack.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>AWS Config:</b> rastrea cambios de configuraci&oacute;n y cumplimiento. Puede reportar drift, pero solo a trav&eacute;s de la regla administrada <code>cloudformation-stack-drift-detection-check</code>, que por debajo invoca el propio <b>DetectStackDrift</b> de CloudFormation. La herramienta directa/nativa para esto es la <b>drift detection</b> del stack.</li>'
            '<li><b>CloudTrail:</b> registra <b>qui&eacute;n</b> hizo la llamada API que cambi&oacute; el rol, pero no dice si fue autorizado ni si el recurso est&aacute; en sync con el stack.</li>'
            '<li><b>CloudWatch Logs:</b> es recolecci&oacute;n de logs/monitoreo; no rastrea cambios de permisos IAM frente al stack.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;"coincide con el stack de CloudFormation"? &rarr; <b>drift detection</b>. &iquest;"qui&eacute;n hizo el cambio"? &rarr; CloudTrail.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html">docs.aws CFN drift detection</a><br>'
            '<a href="https://tutorialsdojo.com/aws-cloudformation/">tutorialsdojo CloudFormation</a></div>'
        ),
    ),
    card(
        question="Para saber <b>qui&eacute;n</b> (qu&eacute; llamada API) modific&oacute; un IAM role, versus saber si un recurso <b>ya no coincide con la plantilla</b> de CloudFormation, &iquest;qu&eacute; servicio corresponde a cada caso?",
        options=[
            "CloudTrail identifica qui&eacute;n hizo el cambio; drift detection de CloudFormation detecta que no coincide con la plantilla",
            "CloudTrail identifica qui&eacute;n hizo el cambio y tambi&eacute;n detecta que el recurso no coincide con la plantilla",
            "Drift detection de CloudFormation identifica qui&eacute;n hizo el cambio y tambi&eacute;n si no coincide con la plantilla",
            "AWS Config identifica qui&eacute;n hizo el cambio; CloudWatch detecta que el recurso no coincide con la plantilla",
        ],
        correct=0,
        key="dva06-q1-cloudtrail-vs-drift",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CloudTrail = qui&eacute;n; drift detection = desviaci&oacute;n del stack.</div>'
            '<p><b>CloudTrail</b> registra las llamadas API (qui&eacute;n, cu&aacute;ndo, desde d&oacute;nde) que modificaron un recurso. <b>Drift detection</b> de CloudFormation te dice si la config actual del recurso <b>difiere de la plantilla</b> del stack. Son preguntas distintas: autor&iacute;a vs. conformidad con el stack.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> CloudTrail no compara con la plantilla del stack. Drift detection no dice qui&eacute;n hizo el cambio. AWS Config rastrea cambios pero no da el contexto de sync-con-stack, y CloudWatch es monitoreo/logs, no autor&iacute;a.</p>'
            '<div class="extra"><span class="h">Dato extra</span>CloudTrail + drift detection se complementan: uno da la evidencia forense, el otro la conformidad con IaC.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/detect-drift-stack.html">docs.aws detect drift</a></div>'
        ),
    ),

    # ================= Q2: Export + Fn::ImportValue =================
    card(
        question="Quieres que el endpoint de una API creado en un stack de CloudFormation pueda <b>referenciarse desde otros stacks</b> (misma cuenta y regi&oacute;n). &iquest;Qu&eacute; haces?",
        options=[
            "Usar la propiedad Export en Outputs y luego Fn::ImportValue en los otros templates",
            "Usar la propiedad Export en Outputs y luego la funci&oacute;n Ref en los otros templates",
            "Usar Fn::ImportValue con HelloWorldApi como par&aacute;metro en los otros templates",
            "Agregar el transform AWS::Include en el template original",
        ],
        correct=0,
        key="dva06-q2-export-importvalue",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Export en Outputs + Fn::ImportValue.</div>'
            '<p>Para compartir valores entre stacks (misma cuenta y regi&oacute;n) usas <b>referencias cruzadas</b>: en el stack origen exportas el valor con la propiedad <b>Export</b> dentro de la secci&oacute;n <b>Outputs</b>, y en los otros stacks lo importas con <b>Fn::ImportValue</b> usando el nombre exportado.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Export + Ref:</b> <code>Ref</code> no puede devolver valores de <b>otros</b> templates.</li>'
            '<li><b>Fn::ImportValue con el nombre del recurso:</b> <code>Fn::ImportValue</code> no es autosuficiente; primero debes declarar un <b>nombre de Export</b>.</li>'
            '<li><b>AWS::Include:</b> sirve para reutilizar fragmentos de plantilla guardados en S3, no para exportar el endpoint.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato de examen</span>Un valor exportado no se puede borrar/modificar mientras otro stack lo est&eacute; importando.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-exports.html">docs.aws CFN stack exports</a><br>'
            '<a href="https://tutorialsdojo.com/aws-cloudformation/">tutorialsdojo CloudFormation</a></div>'
        ),
    ),

    # ================= Q7 (randomized): RCU cost optimization -> 1600 =================
    card(
        question="Una Lambda hace <b>320 lecturas fuertemente consistentes/seg</b> a una tabla con <b>RCU provisionado = 5440</b>; items de <b>17 KB</b> promedio. Para bajar costo manteniendo el rendimiento, &iquest;a cu&aacute;nto ajustas el RCU?",
        options=["1600", "5440", "800", "3200"],
        correct=0,
        key="dva06-q7-rcu-optimize",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 1600 RCU.</div>'
            '<p>M&eacute;todo de AWS para lecturas <b>fuertes</b>: redondea el item al siguiente m&uacute;ltiplo de 4 KB y divide entre 4 KB para las unidades por lectura. 17 KB &rarr; se redondea a 20 KB &rarr; 20/4 = <b>5</b> unidades por lectura fuerte. Multiplicado por 320 lecturas/seg: 320 &times; 5 = <b>1600 RCU</b>. El 5440 estaba mal calculado (320 &times; 17 = 5440 es una f&oacute;rmula tipo WCU, no RCU).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>5440:</b> valor inflado por el c&aacute;lculo incorrecto (usar 17 KB sin dividir entre 4 KB).</li>'
            '<li><b>800:</b> ser&iacute;a la matem&aacute;tica de lecturas <b>eventuales</b> (la mitad), pero el escenario pide <b>fuertes</b>.</li>'
            '<li><b>3200:</b> ser&iacute;a el valor <b>transaccional</b> (2&times; el fuerte); no se pide.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>RCU fuerte = lecturas/seg &times; ceil(tama&ntilde;o/4KB). Eventual = la mitad. Transaccional = el doble.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html#ItemSizeCalculations.Reads">docs.aws item size (reads)</a><br>'
            '<a href="https://tutorialsdojo.com/calculating-the-required-read-and-write-capacity-unit-for-your-dynamodb-table/">tutorialsdojo RCU/WCU calc</a></div>'
        ),
    ),
    card(
        question="En el mismo caso (320 lecturas/seg, items de 17 KB), &iquest;por qu&eacute; <b>800 RCU</b> es incorrecto si el requisito es lectura <b>fuertemente consistente</b>?",
        options=[
            "Porque 800 aplica la f&oacute;rmula eventual (1600 dividido entre 2) y no la consistencia fuerte pedida",
            "Porque 800 usa el valor transaccional, que en realidad exige el doble: 3200 RCU para esos items",
            "Porque 800 redondea el item a 16 KB en vez de 20 KB, arrojando 4 unidades por lectura y no 5",
            "Porque 800 asume items de 4 KB (1 unidad) e ignora las 5 unidades que exigen los 17 KB reales",
        ],
        correct=0,
        key="dva06-q7-why-not-800",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 800 es la cuenta eventual, no cumple consistencia fuerte.</div>'
            '<p>Las lecturas <b>eventuales</b> cuestan la <b>mitad</b> de RCU que las fuertes: 1600 / 2 = <b>800</b>. Bajar a 800 abarata, pero el escenario exige lecturas <b>fuertemente consistentes</b>, as&iacute; que 800 se quedar&iacute;a corto y habr&iacute;a throttling. El valor correcto para fuertes es 1600.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> 800 no supera ning&uacute;n l&iacute;mite. S&iacute; parte del redondeo correcto (5 unidades por lectura). Y 800 no es el transaccional: el transaccional ser&iacute;a el doble del fuerte (3200).</p>'
            '<div class="extra"><span class="h">Dato extra</span>on-demand se descarta aqu&iacute; porque el tr&aacute;fico es conocido/predecible; provisioned bien dimensionado es m&aacute;s barato.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ProvisionedThroughput.html#ItemSizeCalculations.Reads">docs.aws item size (reads)</a></div>'
        ),
    ),

    # ================= Q9: Projection expression =================
    card(
        question="Tus consultas a DynamoDB devuelven <b>todos los atributos</b> por defecto, pero solo quieres traer <b>ciertos atributos</b> (ej. course_id y price). &iquest;Qu&eacute; usas?",
        options=[
            "Un projection expression",
            "Un condition expression",
            "Un filter expression",
            "Expression attribute names",
        ],
        correct=0,
        key="dva06-q9-projection-expression",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; projection expression.</div>'
            '<p>Un <b>projection expression</b> es una cadena con los nombres de los atributos que quieres que devuelva un <code>GetItem</code>/<code>Query</code>/<code>Scan</code> (separados por comas). As&iacute; traes solo <code>course_id</code> y <code>price</code> en lugar de todo el item.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>condition expression:</b> decide qu&eacute; items se <b>modifican</b> en Put/Update/Delete; no filtra atributos de lectura.</li>'
            '<li><b>filter expression:</b> filtra qu&eacute; <b>items</b> se devuelven tras un Query/Scan, no qu&eacute; <b>atributos</b>.</li>'
            '<li><b>expression attribute names:</b> es un placeholder (<code>#nombre</code>) que se usa <b>dentro</b> de un projection expression cuando un nombre es reservado/inv&aacute;lido; no es el mecanismo en s&iacute;.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;Filtrar ATRIBUTOS? &rarr; projection expression. &iquest;Filtrar ITEMS/filas? &rarr; filter expression.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ProjectionExpressions.html">docs.aws projection expressions</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-dynamodb/">tutorialsdojo DynamoDB</a></div>'
        ),
    ),
    card(
        question="En DynamoDB, &iquest;cu&aacute;l es la diferencia entre un <b>projection expression</b> y un <b>filter expression</b>?",
        options=[
            'Projection expression elige qu&eacute; <b>atributos</b> se devuelven; filter expression decide qu&eacute; <b>items</b> se conservan tras un Query/Scan',
            'Projection expression decide qu&eacute; <b>items</b> se devuelven; filter expression elige qu&eacute; <b>atributos</b> aparecen en cada item resultante',
            'Filter expression se eval&uacute;a durante el Query/Scan y reduce la capacidad de lectura consumida; projection expression no afecta a los items',
            'Projection expression filtra items por la clave; filter expression recorta los atributos devueltos una vez terminado el Query/Scan',
        ],
        correct=0,
        key="dva06-q9-projection-vs-filter",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; projection = atributos; filter = items.</div>'
            '<p>Un <b>projection expression</b> recorta <b>columnas/atributos</b> del resultado (traes solo los que nombras). Un <b>filter expression</b> recorta <b>filas/items</b>: tras ejecutar el Query/Scan, descarta los items que no cumplen la condici&oacute;n (pero ya consumi&oacute; capacidad al leerlos).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no son lo mismo. No est&aacute;n invertidos (projection = atributos). Ninguno de los dos modifica items: la modificaci&oacute;n en una escritura la hace <code>PutItem</code> o el <i>update expression</i> de <code>UpdateItem</code>; una <b>condition expression</b> solo decide si esa escritura procede.</p>'
            '<div class="warn"><span class="h">Ojo</span>El filter expression se aplica <b>despu&eacute;s</b> de leer, as&iacute; que consume RCU por todos los items le&iacute;dos, no solo los que pasan el filtro.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ProjectionExpressions.html">docs.aws projection expressions</a></div>'
        ),
    ),

    # ================= Q10: IAM Role per ECS task (Fargate) =================
    card(
        question="Tienes 4 tareas ECS con Fargate y cada una necesita acceder a <b>recursos AWS distintos</b>. &iquest;Cu&aacute;l es la forma m&aacute;s eficiente de darles acceso?",
        options=[
            "Crear 4 IAM Roles distintos y asignar uno a cada tarea como task role (taskRoleArn)",
            "Crear 4 Container Instance Roles (ecsInstanceRole) y asignar uno a cada tarea",
            "Crear 4 Service-Linked Roles de ECS y asignar uno a cada tarea como task role",
            "Crear 4 IAM Groups con permisos distintos y asignar uno a cada tarea como task role",
        ],
        correct=0,
        key="dva06-q10-task-role",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; 4 IAM Roles (task roles), uno por tarea.</div>'
            '<p>En ECS, cada tarea puede tener su propio <b>IAM task role</b>: defines un rol por task definition con exactamente los permisos que esa tarea necesita. Con 4 tareas que acceden a recursos distintos, creas <b>4 roles</b> y asignas uno a cada tarea.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>IAM Group:</b> no puedes adjuntar un IAM Group a una tarea ECS; los grupos son para usuarios IAM.</li>'
            '<li><b>Container Instance IAM Role:</b> solo aplica al <b>launch type EC2</b> (las instancias contenedoras), no a Fargate.</li>'
            '<li><b>Service-Linked Role:</b> es un rol especial ligado al <b>servicio</b> ECS en s&iacute;, no para dar permisos por tarea.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Permisos que usa el c&oacute;digo de la tarea &rarr; <b>task role</b>. Permisos para que ECS baje la imagen/env&iacute;e logs &rarr; execution role.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html">docs.aws ECS task IAM roles</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-elastic-container-service-amazon-ecs/">tutorialsdojo ECS</a></div>'
        ),
    ),

    # ================= Q17: On-prem SDK -> IAM user access keys =================
    card(
        question="Una app Node.js corre en un servidor Linux <b>on-premises</b> (fuera de AWS) y usa el AWS SDK para acceder a S3, DynamoDB y ElastiCache. &iquest;Cu&aacute;l es la forma m&aacute;s adecuada de darle acceso?",
        options=[
            "Crear un IAM user con acceso programm&aacute;tico y poner sus access keys en ~/.aws/credentials del servidor",
            "Crear un IAM role con permisos y asignarlo al servidor on-premises",
            "Crear un IAM role y pedir credenciales temporales a STS con AssumeRole en cada llamada",
            "Crear un IAM user y poner su usuario y contrase&ntilde;a (hash) en ~/.aws/credentials",
        ],
        correct=0,
        key="dva06-q17-onprem-access-keys",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; IAM user con access keys en ~/.aws/credentials.</div>'
            '<p>Regla: los recursos <b>dentro</b> de AWS usan <b>IAM roles</b>; las apps <b>fuera</b> de AWS (on-premises, herramientas de terceros) necesitan <b>access keys</b> para acceso programm&aacute;tico. El AWS SDK lee esas claves del archivo <code>~/.aws/credentials</code> (en Windows, <code>C:\\Users\\USER\\.aws\\credentials</code>).</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>IAM role asignado al servidor on-prem:</b> no puedes asignar un rol directamente a un servidor fuera de AWS como si fuera una instancia EC2.</li>'
            '<li><b>IAM role + STS AssumeRole:</b> conceptualmente v&aacute;lido, pero requiere un mecanismo para obtener credenciales fuera de AWS. La respuesta cl&aacute;sica del examen para "app on-prem con el SDK" son las <b>access keys</b> en <code>~/.aws/credentials</code>.</li>'
            '<li><b>Usuario + contrase&ntilde;a en credentials:</b> el usuario/contrase&ntilde;a son credenciales de <b>consola</b> (para humanos), no sirven para llamadas programm&aacute;ticas del SDK.</li>'
            '</ul>'
            '<div class="warn"><span class="h">Matiz moderno</span>Hoy la mejor pr&aacute;ctica para cargas on-premises es <b>IAM Roles Anywhere</b>: entrega credenciales temporales usando certificados X.509, evitando las access keys de larga duraci&oacute;n. La respuesta con access keys sigue siendo la esperada en DVA-C02, pero en la vida real prefiere Roles Anywhere.</div>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;C&oacute;digo dentro de AWS (EC2, Lambda, ECS)? &rarr; IAM role. &iquest;C&oacute;digo on-premises con SDK? &rarr; access keys en ~/.aws/credentials.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html">docs.aws credential types</a><br>'
            '<a href="https://tutorialsdojo.com/aws-identity-and-access-management-iam/">tutorialsdojo IAM</a></div>'
        ),
    ),

    # ================= Q18: ElastiCache for Redis (Multi-AZ replication) =================
    card(
        question="Quieres una capa de cach&eacute; frente a un RDS MySQL que soporte <b>replicaci&oacute;n Multi-AZ</b> con respuesta sub-milisegundo, con el <b>menor esfuerzo</b>. &iquest;Qu&eacute; eliges?",
        options=[
            "ElastiCache for Redis con replicaci&oacute;n para alta disponibilidad",
            "ElastiCache for Memcached con replicaci&oacute;n para alta disponibilidad",
            "Migrar a DynamoDB con DAX usando el Schema Conversion Tool",
            "AWS Global Accelerator integrado con la aplicaci&oacute;n",
        ],
        correct=0,
        key="dva06-q18-redis",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; ElastiCache for Redis con replicaci&oacute;n.</div>'
            '<p><b>ElastiCache for Redis</b> soporta <b>replicaci&oacute;n</b> (y Multi-AZ con failover autom&aacute;tico) y da latencia <b>sub-milisegundo</b>. Es la opci&oacute;n de menor esfuerzo para poner una cach&eacute; con alta disponibilidad delante de RDS.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Memcached:</b> tambi&eacute;n da sub-ms, pero <b>no soporta replicaci&oacute;n</b>, as&iacute; que no cumple el requisito de Multi-AZ.</li>'
            '<li><b>DynamoDB + DAX:</b> exige convertir el esquema y migrar datos; muchísimo esfuerzo, contra el requisito de "menor esfuerzo".</li>'
            '<li><b>Global Accelerator:</b> mejora el rendimiento de red usando la red global de AWS; no es una cach&eacute;.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>&iquest;Cach&eacute; con replicaci&oacute;n/Multi-AZ/failover? &rarr; <b>Redis</b>. &iquest;Multi-hilo y escalar nodos simples sin replicaci&oacute;n? &rarr; Memcached.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html">docs.aws ElastiCache select engine</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-elasticache/">tutorialsdojo ElastiCache</a></div>'
        ),
    ),
    card(
        question="Entre <b>ElastiCache for Redis</b> y <b>ElastiCache for Memcached</b>, &iquest;cu&aacute;l soporta replicaci&oacute;n y alta disponibilidad Multi-AZ?",
        options=[
            "Memcached",
            "Redis",
            "Ambos por igual",
            "Ninguno; se necesita RDS para eso",
        ],
        correct=1,
        key="dva06-q18-redis-vs-memcached",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; Redis.</div>'
            '<p><b>Redis</b> soporta r&eacute;plicas de lectura, <b>replicaci&oacute;n</b> y <b>Multi-AZ</b> con failover autom&aacute;tico, adem&aacute;s de persistencia y m&aacute;s estructuras de datos. <b>Memcached</b> es m&aacute;s simple y multi-hilo, pero <b>no</b> soporta replicaci&oacute;n; escala a&ntilde;adiendo/quitando nodos.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> Memcached no replica. No es "ambos por igual" (esa es la diferencia clave). Y no necesitas RDS: ElastiCache (Redis) ya ofrece la HA de la cach&eacute;.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Elige Memcached cuando quieres el modelo m&aacute;s simple, nodos grandes multi-core y escalar horizontalmente sin replicaci&oacute;n.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/SelectEngine.html">docs.aws select engine</a></div>'
        ),
    ),

    # ================= Q19: CloudFront Functions (Viewer Request) JWT =================
    card(
        question="Fargate detr&aacute;s de un ALB, con CloudFront delante. Un aluvi&oacute;n de logins <b>no autenticados</b> dispara la CPU de Fargate. Para validar el JWT y quitar carga de la forma m&aacute;s eficiente, &iquest;qu&eacute; haces?",
        options=[
            "Crear una CloudFront Function para validar el JWT y asociarla al evento Viewer Request",
            "Crear una Lambda@Edge para validar el JWT y asociarla al evento Origin Response",
            "Crear una Lambda que valide el JWT y enrutar los logins a ella desde el ALB",
            "Habilitar auto-scaling en las tareas Fargate",
        ],
        correct=0,
        key="dva06-q19-cloudfront-function",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CloudFront Function en Viewer Request.</div>'
            '<p>Una <b>CloudFront Function</b> es c&oacute;digo JavaScript ultraligero que corre en las <b>edge locations</b> en los eventos <b>viewer request/response</b>. Validar el <b>JWT</b> en el evento <b>Viewer Request</b> rechaza a los usuarios no autenticados <b>en el edge</b>, antes de que la petici&oacute;n llegue a CloudFront cache, al ALB o a Fargate. Es altamente escalable y de muy baja latencia, as&iacute; quita la carga del backend.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>Lambda@Edge en Origin Response:</b> se ejecuta <b>despu&eacute;s</b> de que el origen ya proces&oacute; la petici&oacute;n; no reduce la carga del backend (es demasiado tarde).</li>'
            '<li><b>Lambda v&iacute;a ALB:</b> las peticiones igual viajan hasta el ALB/Lambda; no evita que el tr&aacute;fico no autenticado consuma recursos y a&ntilde;ade latencia.</li>'
            '<li><b>Auto-scaling de Fargate:</b> es reactivo; escala pero no impide que las peticiones no autenticadas consuman recursos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Autorizaci&oacute;n ligera de tokens en el edge, antes del origen &rarr; <b>CloudFront Functions + Viewer Request</b>. Lambda@Edge es m&aacute;s pesado y cubre tambi&eacute;n origin request/response.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cloudfront-functions.html">docs.aws CloudFront Functions</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-cloudfront/">tutorialsdojo CloudFront</a></div>'
        ),
    ),
    card(
        question="&iquest;En qu&eacute; se diferencian <b>CloudFront Functions</b> y <b>Lambda@Edge</b>, y cu&aacute;ndo conviene cada uno?",
        options=[
            "CloudFront Functions: JS ligero (ECMAScript 5.1), solo viewer request/response, submilisegundo, sin acceso de red. Lambda@Edge: Node/Python, los 4 eventos incluido origin, con acceso de red",
            "CloudFront Functions: Node/Python en los 4 eventos con acceso de red. Lambda@Edge: JS ligero submilisegundo solo en viewer request/response, sin acceso de red",
            "CloudFront Functions: JS en los 4 eventos incluido origin y con acceso de red. Lambda@Edge: solo viewer request/response y sin poder llamar a otros servicios",
            "Ambas usan Node/Python en los 4 eventos incluido origin; la &uacute;nica diferencia es que Lambda@Edge se factura aparte y CloudFront Functions va incluido",
        ],
        correct=0,
        key="dva06-q19-cf-func-vs-lambda-edge",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CF Functions = ligero, viewer only; Lambda@Edge = m&aacute;s pesado, 4 eventos.</div>'
            '<p><b>CloudFront Functions</b> ejecuta JavaScript ultraligero y de muy alta escala, solo en los eventos <b>viewer request</b> y <b>viewer response</b>. Sirve para tareas cortas como validar tokens (JWT), reescribir URLs o manipular headers. <b>Lambda@Edge</b> es m&aacute;s pesado (m&aacute;s CPU/tiempo, acceso a red) y puede ejecutarse en los cuatro eventos, incluyendo <b>origin request/response</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b> no son el mismo servicio. No est&aacute;n invertidos (es CF Functions el limitado a viewer). Y CF Functions no se limita a im&aacute;genes; hace autorizaci&oacute;n, redirecciones, manipulaci&oacute;n de headers, etc.</p>'
            '<div class="extra"><span class="h">Dato extra</span>Para <b>filtrar tr&aacute;fico no autenticado antes del origen</b>, CloudFront Functions en Viewer Request es lo m&aacute;s eficiente.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions-choosing.html">docs.aws choosing edge functions</a></div>'
        ),
    ),

    # ================= Q4: S3 CORS configuration =================
    card(
        question="Una config CORS de un bucket S3 tiene <code>AllowedOrigin=https://tutorialsdojo.com</code>, <code>AllowedMethod</code> = GET, PUT, POST, DELETE, <code>AllowedHeader=*</code>, <code>MaxAgeSeconds=3600</code>. &iquest;Qu&eacute; DOS afirmaciones son ciertas? (marca la de los <b>metodos</b>)",
        options=[
            "Permite a un usuario ver, agregar, borrar o actualizar objetos del bucket desde el dominio tutorialsdojo.com",
            "Permite ejecutar los m&eacute;todos GET, PUT, POST y DELETE sobre el bucket desde cualquier origen o dominio web",
            "Habilita absolutamente todos los m&eacute;todos HTTP existentes para las solicitudes de origen cruzado al bucket",
            "La solicitud de origen cruzado falla si el navegador no incluye el header x-amz-meta-custom-header en ella",
        ],
        correct=0,
        key="dva06-q4-cors-allows",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; permite ver/agregar/borrar/actualizar desde ese origen (la otra cierta: cachea el preflight 1 hora).</div>'
            '<p><b>CORS</b> (Cross-Origin Resource Sharing) deja que una app web cargada en un dominio interactue con recursos de otro dominio. Esta regla permite al origen <code>https://tutorialsdojo.com</code> hacer <b>GET</b> (ver), <b>PUT/POST</b> (agregar/actualizar) y <b>DELETE</b> (borrar) objetos del bucket. Adem&aacute;s, <code>MaxAgeSeconds=3600</code> hace que el navegador <b>cachee 1 hora</b> la respuesta al preflight <code>OPTIONS</code>, evitando repetir el preflight.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>"Todos los metodos HTTP":</b> falso, falta <b>HEAD</b>. Solo se listaron GET, PUT, POST, DELETE.</li>'
            '<li><b>"Falla sin x-amz-meta-custom-header":</b> falso. Eso est&aacute; en <code>ExposeHeader</code>, que expone un header en la <b>respuesta</b>; no es un requisito de la peticion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Dato de examen</span>CORS <b>no</b> autoriza acciones (eso lo hacen IAM y las bucket policies). CORS solo decide qu&eacute; <b>orígenes</b> del navegador pueden llamar al bucket.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html">docs.aws S3 CORS</a><br>'
            '<a href="https://tutorialsdojo.com/amazon-s3/">tutorialsdojo S3</a></div>'
        ),
    ),
    card(
        question="En una regla CORS de S3, &iquest;qu&eacute; hace exactamente el elemento <code>ExposeHeader</code> (ej. <code>ExposeHeader=ETag</code>)?",
        options=[
            "Expone ese header de la respuesta para que el JavaScript del cliente pueda leerlo",
            "Autoriza ese header en el preflight v&iacute;a Access-Control-Request-Headers del navegador",
            "Fija cu&aacute;ntos segundos el navegador cachea ese header antes de volver a pedirlo",
            "Define ese header como m&eacute;todo HTTP permitido en la regla CORS del bucket",
        ],
        correct=0,
        key="dva06-q4-cors-exposeheader",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; expone un header de la respuesta al c&oacute;digo del cliente.</div>'
            '<p><code>ExposeHeader</code> identifica los headers de la <b>respuesta</b> que la app (ej. un <code>XMLHttpRequest</code> en JavaScript) podr&aacute; <b>leer</b>. Por defecto el navegador solo deja leer unos pocos headers; con <code>ExposeHeader</code> permites leer otros como <code>ETag</code> o <code>x-amz-meta-custom-header</code>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>"Obliga a incluirlo o falla":</b> no; <code>ExposeHeader</code> no impone nada sobre la <b>peticion</b>, solo expone headers de la respuesta.</li>'
            '<li><b>"Permite ese header en el preflight":</b> eso es <code>AllowedHeader</code>, no <code>ExposeHeader</code>.</li>'
            '<li><b>"Cachea el header":</b> el cacheo del preflight lo controla <code>MaxAgeSeconds</code>, no <code>ExposeHeader</code>.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span><code>AllowedHeader</code> = headers permitidos en la peticion/preflight. <code>ExposeHeader</code> = headers de la respuesta que el cliente puede leer. <code>MaxAgeSeconds</code> = cuanto cachea el navegador el preflight.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html">docs.aws S3 CORS</a></div>'
        ),
    ),
    card(
        question="&iquest;Qu&eacute; hace (y qu&eacute; NO hace) una configuraci&oacute;n CORS en un bucket S3?",
        options=[
            "Define qu&eacute; or&iacute;genes (dominios) del navegador pueden hacer peticiones cross-origin al bucket; NO autoriza acciones",
            "Concede a los or&iacute;genes listados permiso para ejecutar acciones sobre los objetos, igual que una bucket policy",
            "Cifra en reposo los objetos servidos a or&iacute;genes cross-origin y gestiona las claves de ese cifrado",
            "Sustituye a las bucket policies e IAM como mecanismo de autorizaci&oacute;n para el acceso desde el navegador",
        ],
        correct=0,
        key="dva06-q4-cors-not-authz",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; CORS define orígenes permitidos del navegador; no autoriza acciones.</div>'
            '<p><b>CORS</b> es un mecanismo del <b>navegador</b>: decide desde qu&eacute; <b>orígenes</b> (dominios) una app web puede hacer peticiones cross-origin al bucket, y qu&eacute; metodos/headers se permiten en esas peticiones. <b>No</b> concede permisos: la autorizaci&oacute;n de acciones sobre S3 la dan <b>IAM</b> y las <b>bucket policies</b>.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>"Autoriza acciones como una policy":</b> falso; CORS hace lo contrario: no autoriza, solo habilita el cross-origin del navegador.</li>'
            '<li><b>"Cifra los objetos":</b> el cifrado en reposo es SSE-S3/SSE-KMS/SSE-C, no CORS.</li>'
            '<li><b>"Reemplaza bucket policies e IAM":</b> no; CORS y la autorizaci&oacute;n (IAM/policies) son capas distintas y complementarias.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Concepto</span>Aunque CORS permita un origen, la peticion igual necesita permiso de IAM/bucket policy para tener &eacute;xito. Son controles separados.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html">docs.aws S3 CORS</a></div>'
        ),
    ),

    # ================= Q5: SSE-KMS upload with default key (least config) =================
    card(
        question="Un job debe subir archivos a un bucket con <b>SSE-KMS</b> usando la <b>KMS key por defecto</b>. Con la <b>MENOR configuraci&oacute;n</b>, &iquest;qu&eacute; header incluyes en la petici&oacute;n de subida?",
        options=[
            "x-amz-server-side-encryption con valor aws:kms",
            "x-amz-server-side-encryption con valor aws:kms MAS x-amz-server-side-encryption-aws-kms-key-id con el ID de la key por defecto",
            "x-amz-server-side-encryption con valor AES256",
            "x-amz-server-side-encryption-customer-algorithm, -customer-key y -customer-key-MD5",
        ],
        correct=0,
        key="dva06-q5-ssekms-header",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; solo x-amz-server-side-encryption: aws:kms.</div>'
            '<p>Para subir a un bucket con <b>SSE-KMS</b> basta el header <code>x-amz-server-side-encryption: aws:kms</code>. Si <b>no</b> incluyes <code>x-amz-server-side-encryption-aws-kms-key-id</code>, S3 asume la <b>KMS key por defecto</b> de la cuenta/regi&oacute;n. Como se pide la <b>menor configuraci&oacute;n</b> y se usa la key por defecto, este header solo es suficiente.</p>'
            '<p><b>Por qu&eacute; NO las otras:</b></p>'
            '<ul>'
            '<li><b>aws:kms + el key-id de la key por defecto:</b> es v&aacute;lido, pero a&ntilde;ade un header innecesario; con la key por defecto no hace falta el <code>-aws-kms-key-id</code>.</li>'
            '<li><b>AES256:</b> ese valor es para <b>SSE-S3</b> (y en SSE-C), no para SSE-KMS. El valor correcto es <code>aws:kms</code>.</li>'
            '<li><b>Los headers -customer-*:</b> son para <b>SSE-C</b> (claves provistas por el cliente), no para SSE-KMS.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Truco de examen</span>Menor configuraci&oacute;n + key por defecto = solo <code>x-amz-server-side-encryption: aws:kms</code>. Agrega <code>-aws-kms-key-id</code> solo si quieres una KMS key espec&iacute;fica (no la por defecto).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html">docs.aws SSE-KMS</a><br>'
            '<a href="https://tutorialsdojo.com/aws-key-management-service-aws-kms/">tutorialsdojo KMS</a></div>'
        ),
    ),
    card(
        question="Al subir a S3, &iquest;qu&eacute; valor del header <code>x-amz-server-side-encryption</code> corresponde a cada tipo de cifrado del lado servidor?",
        options=[
            "SSE-KMS usa aws:kms, SSE-S3 usa AES256 y SSE-C usa headers -customer-*",
            "SSE-KMS usa AES256, SSE-S3 usa aws:kms y SSE-C usa headers -customer-*",
            "SSE-KMS, SSE-S3 y SSE-C usan todos el valor aws:kms en el mismo header",
            "SSE-KMS usa aws:kms, SSE-S3 usa AES256 y SSE-C usa el valor aws:kms",
        ],
        correct=0,
        key="dva06-q5-sse-header-map",
        answer=(
            '<div class="verdict">Correcta: {{L}} &mdash; aws:kms=SSE-KMS, AES256=SSE-S3, headers -customer-*=SSE-C.</div>'
            '<p>El mapa de cifrado del lado servidor en la subida:</p>'
            '<ul>'
            '<li><b>SSE-KMS</b> (claves gestionadas por KMS): <code>x-amz-server-side-encryption: aws:kms</code> (opcional <code>-aws-kms-key-id</code> para una key espec&iacute;fica).</li>'
            '<li><b>SSE-S3</b> (claves gestionadas por S3): <code>x-amz-server-side-encryption: AES256</code>.</li>'
            '<li><b>SSE-C</b> (claves provistas por el cliente): los headers <code>-customer-algorithm</code>, <code>-customer-key</code> y <code>-customer-key-MD5</code>.</li>'
            '</ul>'
            '<p><b>Por qu&eacute; NO las otras:</b> "AES256 para SSE-KMS" invierte los valores (AES256 es SSE-S3). "aws:kms para todos" es falso (SSE-S3 usa AES256 y SSE-C usa los headers -customer-*). "SSE-C usa aws:kms" es falso: SSE-C no usa <code>x-amz-server-side-encryption</code>, usa los headers de cliente.</p>'
            '<div class="extra"><span class="h">Truco de examen</span>aws:kms &rarr; SSE-KMS. AES256 &rarr; SSE-S3. Headers <code>-customer-*</code> &rarr; SSE-C.</div>'
            '<div class="links"><span class="h">Link</span><a href="https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html">docs.aws PutObject encryption headers</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(deck_name="DVA-C02::06", cards=cards, out_path="out/DVA-C02_06.apkg")
