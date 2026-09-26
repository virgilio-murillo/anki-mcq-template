#!/usr/bin/env python3
"""
AIP-C01::01 - Preguntas nuevas (deduplicadas) del examen 1.

36 cartas (v2, dedup mejorado) a partir de decks/aip-c01/dedupe/new_to_generate_v2_exam1.json.

Reglas aplicadas (docs/DECK_STANDARDS.md):
- 1 carta por pregunta (solo la MCQ directa).
- Exactamente 4 opciones (las 38 fuentes ya venian con 4).
- Espanol, HTML con UTF-8 directo para acentos, sin em dashes.
- Verdict con {{L}} (nunca hardcodear la letra; el motor baraja y sustituye).
- El frente no filtra la respuesta.
- Cada dorso: define terminos, conecta escenario con solucion, refuta CADA
  distractor uno por uno bajo "Por que NO las otras", exam tip y links.
- Distractores near-miss plausibles; longitudes balanceadas entre las 4 opciones.
- key estable y unica: aip01-q<n> usando el numero n de la fuente.
- correct= es el indice 0-based tras traducir (mismo orden que la fuente).
"""
import os

from anki_mcq import card, create

cards = [
    # ============================================================
    # Q3 - Instancias Trainium (Trn) para entrenar LLM
    # ============================================================
    card(
        question="Una empresa de medios entrena (fine-tuning) un <b>LLM propio de cientos de miles de millones de parametros</b> sobre <b>terabytes</b> de datos con Amazon SageMaker AI. Necesita infraestructura <b>altamente optimizada y escalable</b> para minimizar tiempo y costo de entrenamiento. ¿Que tipo de instancia EC2 es el mas apropiado para el fine-tuning?",
        options=[
            "Instancias EC2 de la serie Trn (AWS Trainium), diseñadas a proposito para entrenamiento de alto rendimiento de LLM a gran escala",
            "Instancias EC2 GPU de la serie P para entrenar el LLM y servirlo mediante endpoints de SageMaker AI",
            "Instancias EC2 de proposito general de la serie M con SageMaker AI para entrenamiento distribuido",
            "Instancias EC2 de computo acelerado de la serie G para desplegar una version mas pequeña del modelo tras preprocesar con Comprehend",
        ],
        correct=0,
        key="aip01-q3",
        answer=(
            '<div class="verdict">Correcta: {{L}} - instancias Trn (AWS Trainium).</div>'
            '<p><b>El problema:</b> entrenar un LLM enorme (cientos de miles de millones de parametros) sobre terabytes de datos, minimizando tiempo y costo. Eso exige mucha memoria de acelerador y un interconnect de alto ancho de banda para entrenamiento distribuido.</p>'
            '<p><b>Por que la respuesta sirve:</b> las instancias <b>Trn</b> usan chips <b>AWS Trainium</b>, acceleradores construidos a proposito para el <b>entrenamiento</b> de modelos de deep learning grandes (LLM). Ofrecen alto rendimiento por dolar y buen escalado distribuido, por lo que reducen tiempo y costo frente a GPU genericas para este tamaño de modelo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Serie P (GPU):</b> sirven para entrenamiento de ML estandar y aceleracion GPU general, pero no estan optimizadas para LLM de cientos de miles de millones de parametros: se traducen en tiempos y costos mayores por memoria e interconnect insuficientes a esa escala.</li>'
            '<li><b>Serie M (proposito general):</b> son de computo general y cargas ligeras, sin aceleracion GPU ni la memoria/interconnect que exige el fine-tuning masivo; provocarian cuellos de botella severos.</li>'
            '<li><b>Serie G (computo acelerado):</b> orientadas a graficos e inferencia de modelos pequeños; su arquitectura no soporta la memoria ni el computo de un modelo de ese tamaño, y ademas la opcion propone desplegar una version reducida, que no es lo pedido.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Entrenar LLM muy grandes al menor costo: chips construidos a proposito para training (serie Trn). Inferencia optimizada en costo: aceleradores de inferencia (serie Inf). Serie P = GPU de entrenamiento general; G = graficos/inferencia; M = proposito general sin GPU.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/trainium.html">docs.aws SageMaker y Trainium</a></div>'
        ),
    ),
    # ============================================================
    # Q4 - SageMaker ProductionVariant y traffic weights
    # ============================================================
    card(
        question="Un modelo de deteccion de fraude ya esta desplegado en un endpoint de SageMaker AI. Se reentreno una nueva version y el equipo debe <b>evaluar su exactitud y latencia en produccion</b> con <b>trafico real</b>, <b>sin afectar el throughput del modelo actual</b>, con <b>minimo overhead operativo</b> y <b>sin cambiar como los clientes invocan el endpoint</b>. ¿Que opcion cumple?",
        options=[
            "Registrar la nueva version en SageMaker Model Registry y usar un trigger en AWS Lambda que cambie automaticamente el endpoint al nuevo modelo tras una validacion inicial",
            "Desplegar el modelo nuevo y el actual en dos endpoints de SageMaker separados, enrutar manualmente parte del trafico al nuevo y comparar sus resultados en post-procesamiento con metricas de Amazon CloudWatch antes de decidir",
            "Configurar un endpoint de Amazon API Gateway que reparta el trafico entre el endpoint de SageMaker actual y el nuevo para hacer pruebas A/B, y que los clientes invoquen ese endpoint de API Gateway en lugar del de SageMaker",
            "Modificar la configuracion del endpoint agregando el nuevo modelo como un ProductionVariant (via la API de ProductionVariant) con un InitialVariantWeight pequeño frente al peso del modelo existente, para controlar el porcentaje de trafico enrutado a el",
        ],
        correct=3,
        key="aip01-q4",
        answer=(
            '<div class="verdict">Correcta: {{L}} - agregar el nuevo modelo como ProductionVariant con peso pequeño.</div>'
            '<p><b>El problema:</b> evaluar un modelo nuevo con trafico real (A/B o canary) sin degradar al actual, con poco esfuerzo y sin que los clientes cambien la forma de invocar el endpoint.</p>'
            '<p><b>Por que la respuesta sirve:</b> un endpoint de SageMaker puede alojar varios <b>ProductionVariant</b> (variantes de produccion). Al agregar el nuevo modelo como otra variante con un <b>InitialVariantWeight</b> bajo, SageMaker enruta solo un pequeño porcentaje del trafico al modelo nuevo dentro del <b>mismo endpoint</b>. Asi se comparan exactitud y latencia en vivo, sin tocar el cliente (misma URL de invocacion) y sin arriesgar el throughput del modelo actual.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Model Registry + Lambda que hace swap:</b> reemplaza por completo el modelo, impidiendo la evaluacion lado a lado; arriesga la estabilidad y agrega complejidad innecesaria de automatizacion.</li>'
            '<li><b>Dos endpoints separados + CloudWatch:</b> obliga a gestionar multiples endpoints y a enrutar el trafico manualmente, lo que aumenta el overhead y viola el requisito de no cambiar como invoca el cliente.</li>'
            '<li><b>API Gateway repartiendo trafico:</b> agrega infraestructura extra y obliga a los clientes a invocar un endpoint nuevo de API Gateway en vez del endpoint de SageMaker existente, contradiciendo el requisito de mantener el mismo metodo de invocacion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>A/B o canary de modelos en SageMaker sin cambiar el cliente: varias variantes de produccion en UN mismo endpoint, ajustando su peso de trafico. Nada de endpoints nuevos ni capas de API Gateway.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-ab-testing.html">docs.aws pruebas A/B con variantes de produccion</a></div>'
        ),
    ),
    # ============================================================
    # Q6 - Bedrock Agents multi-agent collaboration
    # ============================================================
    card(
        question="Una empresa construye un asistente con <b>Amazon Bedrock Agents</b> que debe: recuperar datos de cuentas de sistemas internos, aplicar controles de cumplimiento, generar explicaciones al cliente y disparar acciones (abrir tickets, notificar, actualizar CRM). Cada paso requiere <b>permisos, herramientas, APIs y logica de razonamiento distintos</b>. Se busca un diseño <b>modular, escalable y facil de evolucionar</b>, minimizando codigo de orquestacion propio fuera de Bedrock. ¿Que diseño conviene?",
        options=[
            "Crear un unico agente de Bedrock con un gran system prompt y un solo action group que maneje secuencialmente deteccion de intencion, recuperacion de datos, controles de cumplimiento y ejecucion del flujo",
            "Crear varios foundation models en Bedrock e implementar logica de enrutamiento propia en la capa de aplicacion para pasar peticiones entre modelos, con seguimiento de coordinacion multi-agente para los handoffs",
            "Crear una knowledge base de Bedrock y apoyarse principalmente en RAG (retrieval-augmented generation) para responder todas las peticiones de los usuarios",
            "Crear una colaboracion multi-agente definiendo varios agentes de Bedrock, cada uno especializado en una responsabilidad y colaborando con los demas para completar la peticion de extremo a extremo",
        ],
        correct=3,
        key="aip01-q6",
        answer=(
            '<div class="verdict">Correcta: {{L}} - colaboracion multi-agente de Bedrock Agents.</div>'
            '<p><b>El problema:</b> un flujo empresarial de varios pasos, cada uno con distintos permisos, herramientas y razonamiento, que debe ser modular, escalable y facil de mantener, con minima orquestacion propia.</p>'
            '<p><b>Por que la respuesta sirve:</b> la <b>colaboracion multi-agente</b> de Bedrock Agents permite definir varios agentes, cada uno especializado en una responsabilidad (datos, cumplimiento, generacion, acciones) con sus propios action groups y permisos, coordinados de forma nativa por Bedrock. Aisla responsabilidades, escala mejor y evita escribir orquestacion a mano.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Un solo agente con un gran prompt y un action group:</b> mezclar todas las responsabilidades en un agente lo hace dificil de mantener, actualizar y asegurar; no aisla dominios y eleva el riesgo de errores en flujos de varios pasos.</li>'
            '<li><b>Varios FM con enrutamiento propio en la app:</b> construir routing fuera de Bedrock contradice el requisito de minimizar codigo de orquestacion, y gestionar varios modelos por una capa custom añade overhead; el "seguimiento de handoffs" solo monitorea, no aporta la colaboracion modular pedida.</li>'
            '<li><b>Solo knowledge base + RAG:</b> RAG unicamente recupera informacion de documentos; no razona en varios pasos, no llama APIs ni dispara acciones downstream, que son requisitos criticos aqui.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Flujo empresarial con responsabilidades separadas, herramientas y acciones: multi-agent collaboration de Bedrock Agents (agentes especializados). RAG solo responde preguntas sobre documentos; un solo agente monolitico no escala.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html">docs.aws colaboracion multi-agente</a></div>'
        ),
    ),
    # ============================================================
    # Q7 - Bedrock AgentCore Runtime/Memory/Gateway/Observability
    # ============================================================
    card(
        question="Un asistente de soporte procesa miles de consultas diarias, debe <b>preservar contexto entre turnos</b>, <b>recuperar documentacion de producto actualizada</b>, <b>ejecutar operaciones de pedidos via una API interna</b> y mantener <b>auditoria detallada</b> de que fuentes de conocimiento y herramientas contribuyeron a cada respuesta, con <b>minima orquestacion e infraestructura propia</b>. ¿Que enfoque cumple mejor?",
        options=[
            "Coordinar la recuperacion de producto y las llamadas a la API de pedidos con AWS Step Functions, guardar el historial de conversacion en Amazon DynamoDB, construir la recuperacion de conocimiento aparte y enviar los logs de ejecucion del workflow a Amazon CloudWatch para la auditoria",
            "Desplegar el agente con Amazon Bedrock AgentCore Runtime y usar AgentCore Memory para el contexto multi-turno; registrar la API REST de pedidos y una Knowledge Base como herramientas en AgentCore Gateway, y habilitar AgentCore Observability para trazar recuperacion, invocaciones de herramientas y respuestas",
            "Desplegar el agente en AWS Lambda y guardar la sesion en Amazon ElastiCache; consultar las Bedrock Knowledge Bases por separado, invocar la API de pedidos via Amazon API Gateway desde logica de aplicacion propia y registrar cada paso para la auditoria",
            "Usar Bedrock Knowledge Bases para responder consultas de producto y mantener el historial de conversacion en la aplicacion cliente; invocar la API de pedidos por separado con AWS Lambda y guardar las respuestas en Amazon S3 para conservar el rastro de auditoria",
        ],
        correct=1,
        key="aip01-q7",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock AgentCore (Runtime + Memory + Gateway + Observability).</div>'
            '<p><b>El problema:</b> un agente productivo que necesita memoria de sesion, recuperacion de conocimiento, ejecucion de herramientas (API de pedidos) y trazabilidad de auditoria, todo con la menor operacion posible.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>AgentCore</b> aporta piezas gestionadas que encajan una a una: <b>Runtime</b> ejecuta el agente; <b>Memory</b> preserva el contexto entre turnos; <b>Gateway</b> expone la API REST de pedidos y la Knowledge Base como herramientas unificadas; <b>Observability</b> traza recuperacion de conocimiento, invocaciones de herramientas y procesamiento de la respuesta para la auditoria. Cubre todos los requisitos sin construir persistencia ni orquestacion propias.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Step Functions + DynamoDB + CloudWatch:</b> Step Functions orquesta workflows de aplicacion, no memoria de agente ni descubrimiento gestionado de herramientas; obligaria a construir persistencia, recuperacion y orquestacion que AgentCore Memory y Gateway ya ofrecen.</li>'
            '<li><b>Lambda + ElastiCache + API Gateway:</b> traslada la gestion de memoria, el ruteo de herramientas y la recuperacion a codigo propio, justo lo que AgentCore evita con Gateway y Memory gestionados.</li>'
            '<li><b>Knowledge Bases + historial en el cliente + Lambda + S3:</b> una KB recupera informacion, pero no orquesta operaciones transaccionales ni gestiona toda la sesion; guardar el historial en el cliente fragmenta el flujo y exige coordinacion adicional.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Agente gestionado con memoria de sesion, herramientas unificadas y trazas de auditoria con minima operacion: el stack gestionado de agentes de Bedrock. Orquestar con Step Functions, Lambda y DynamoDB implica construir a mano esas piezas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html">docs.aws Bedrock AgentCore</a></div>'
        ),
    ),
    # ============================================================
    # Q8 - Versionado y evaluacion de prompts
    # ============================================================
    card(
        question="Un prompt de Amazon Bedrock genera resumenes de alta clinicos: funciona en casos rutinarios, pero en historiales complejos produce <b>inconsistencias</b> en completitud, terminologia y detalles clave. La empresa quiere <b>saber que cambios de prompt mejoran la calidad</b> en casos dificiles, <b>comparar versiones contra objetivos medibles</b> y <b>conservar el historial</b> de cambios y evaluaciones. ¿Que enfoque cumple mejor?",
        options=[
            "Versionar los prompts en un repositorio bajo control de versiones y validar cada revision contra un conjunto benchmark de documentos clinicos complejos con criterios de evaluacion medibles; automatizar pruebas lado a lado para detectar regresiones, mejoras y patrones consistentes entre versiones",
            "Refinar el prompt actual con una muestra pequeña de resumenes problematicos, revisar manualmente las salidas caso por caso y desplegar cada version actualizada a Bedrock cuando el revisor la apruebe, sin criterios de aceptacion definidos",
            "Crear prompts separados para documentos simples y complejos y enrutar cada tipo al prompt correspondiente segun la longitud y la estructura del documento, sin medir la calidad ni registrar el desempeño de cada version",
            "Hacer fine-tuning de un modelo con resumenes clinicos previamente aceptados, usar el modelo personalizado para los documentos complejos y mantener el prompt actual para los casos rutinarios, asumiendo que el problema es del modelo y no del prompt",
        ],
        correct=0,
        key="aip01-q8",
        answer=(
            '<div class="verdict">Correcta: {{L}} - versionar prompts y evaluarlos contra un benchmark medible.</div>'
            '<p><b>El problema:</b> determinar sistematicamente que cambios de prompt mejoran la calidad en casos dificiles, compararlos con metricas y conservar el historial para revision futura.</p>'
            '<p><b>Por que la respuesta sirve:</b> versionar cada prompt y validarlo contra un <b>conjunto benchmark</b> fijo de documentos complejos con <b>criterios de evaluacion medibles</b> permite comparar de forma repetible, con pruebas <b>lado a lado</b> automatizadas que detectan regresiones y mejoras. Es lo que ofrecen las evaluaciones de Bedrock: datasets definidos y metricas para comparar de forma sistematica, con trazabilidad de cambios.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Muestra pequeña con revision manual:</b> da evidencia limitada e inconsistente; no establece un benchmark repetible, criterios de aceptacion medibles ni pruebas de regresion automatizadas.</li>'
            '<li><b>Prompts separados por longitud/estructura:</b> cambia como se enrutan las peticiones, pero no explica por que un prompt rinde mejor ni aporta comparacion por metricas, deteccion de regresiones ni historial sobre los mismos casos.</li>'
            '<li><b>Fine-tuning con resumenes aceptados:</b> es un paso de personalizacion mayor de lo necesario cuando el problema se identifico como inconsistencia de prompt; primero conviene un proceso de evaluacion repetible que cuantifique si ajustar el prompt resuelve el problema.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Mejorar y comparar prompts de forma medible: versionado + dataset benchmark + metricas + pruebas lado a lado (evaluaciones de Bedrock). El fine-tuning se justifica despues, si el prompt no basta.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation.html">docs.aws evaluaciones de modelos en Bedrock</a></div>'
        ),
    ),
    # ============================================================
    # Q10 - Bedrock Prompt Management con governance
    # ============================================================
    card(
        question="Varios equipos mantienen cientos de <b>plantillas de prompt reutilizables</b> y las despliegan a varias Regiones de AWS. Se requiere un proceso <b>centralizado de gobierno</b> que: preserve versiones, estandarice variables y configuraciones de inferencia, <b>impida que plantillas no aprobadas lleguen a produccion</b>, <b>notifique a los revisores</b> cuando hay algo pendiente y permita saber <b>que identidad creo, modifico, aprobo o desplego</b> cada prompt. ¿Que arquitectura conviene?",
        options=[
            "Construir la aprobacion con AWS Step Functions, guardar los prompts como objetos en Amazon S3 con object tags para versionar y usar Amazon EventBridge para notificar revisiones pendientes",
            "Guardar las plantillas en Amazon S3 con Versioning; usar acciones de aprobacion manual de AWS CodePipeline con notificaciones Amazon SNS antes del despliegue; usar AWS CloudTrail para registrar la actividad de objetos S3 e IAM para controlar el acceso a los archivos",
            "Gestionar plantillas parametrizadas con variables y versiones numeradas usando Bedrock Prompt Management; agregar una accion de aprobacion manual de AWS CodePipeline con notificaciones Amazon SNS antes del despliegue; usar IAM para separar responsabilidades y AWS CloudTrail para registrar la actividad de API",
            "Desplegar las aplicaciones con Bedrock AgentCore Runtime; usar AgentCore Identity e IAM para el acceso de revisores, AgentCore Observability para el tracing de prompts y Amazon EventBridge para notificar; guardar las revisiones de prompt en AgentCore Memory",
        ],
        correct=2,
        key="aip01-q10",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Prompt Management + CodePipeline (aprobacion) + SNS + IAM + CloudTrail.</div>'
            '<p><b>El problema:</b> gobernar plantillas de prompt como recursos gestionados: versiones numeradas, variables y configuracion de inferencia estandarizadas, aprobacion antes de produccion, notificacion a revisores y trazabilidad de quien hizo cada accion.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Prompt Management</b> gestiona plantillas parametrizadas (variables) con <b>versiones numeradas</b> y configuraciones de inferencia estandarizadas, tratando los prompts como recursos nativos. La <b>aprobacion manual de CodePipeline</b> con <b>SNS</b> bloquea lo no aprobado y notifica a revisores; <b>IAM</b> separa responsabilidades y <b>CloudTrail</b> registra la actividad de API (quien creo/modifico/aprobo/desplego).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Step Functions + S3 + tags + EventBridge:</b> puede implementar un flujo de aprobacion y notificaciones, pero exige una implementacion custom y guarda los prompts como objetos S3 comunes en vez de prompts gestionados de Bedrock (sin variables ni versiones nativas).</li>'
            '<li><b>S3 Versioning + CodePipeline + CloudTrail:</b> el versioning y la aprobacion existen, pero los prompts siguen siendo archivos, no recursos de Prompt Management con variables y configuraciones de inferencia estandarizadas.</li>'
            '<li><b>AgentCore (Runtime/Identity/Observability/Memory):</b> AgentCore es para desplegar, asegurar y observar agentes; AgentCore Memory retiene contexto de interacciones, no plantillas versionadas. No reemplaza a Prompt Management para prompts reutilizables con variables y versiones numeradas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Prompts reutilizables, versionados y gobernados: el servicio nativo de gestion de prompts de Bedrock (variables + versiones). Aprobacion antes de prod: aprobacion manual de pipeline + notificaciones. Quien hizo que: auditoria de API. AgentCore es para agentes, no para versionar prompts.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
        ),
    ),
    # ============================================================
    # Q11 - IAM bedrock:GuardrailIdentifier enforcement
    # ============================================================
    card(
        question="Una organizacion regulada exige que <b>todas las interacciones con foundation models</b> esten protegidas por guardrails de Amazon Bedrock. Los equipos llaman directamente a las APIs de Bedrock. Los arquitectos deben: <b>forzar el uso de guardrails</b> en todas las interacciones, cubrir <b>InvokeModel y Converse</b> y <b>evitar que cualquier peticion los omita</b>, con el <b>menor overhead operativo</b>. ¿Que solucion lo logra?",
        options=[
            "Aplicar politicas IAM sobre InvokeModel y Converse que exijan tanto la clave de condicion bedrock:GuardrailIdentifier como bedrock:PromptRouterArn, obligando a que todas las peticiones pasen por un prompt router que adjunte y valide guardrails",
            "Desplegar un proxy con API Gateway y AWS Lambda que inyecte los guardrails en todas las peticiones InvokeModel y Converse antes de reenviarlas a Bedrock",
            "Guardar el identificador de guardrail en AWS Secrets Manager y exigir que las aplicaciones lo recuperen antes de llamar a InvokeModel o Converse",
            "Aplicar politicas IAM sobre InvokeModel y Converse que exijan la presencia de bedrock:GuardrailIdentifier, garantizando que toda peticion al foundation model incluya un guardrail adjunto",
        ],
        correct=3,
        key="aip01-q11",
        answer=(
            '<div class="verdict">Correcta: {{L}} - IAM que exige bedrock:GuardrailIdentifier en las llamadas.</div>'
            '<p><b>El problema:</b> garantizar que ninguna llamada a un FM se ejecute sin guardrail, cubriendo InvokeModel y Converse, con la menor operacion posible.</p>'
            '<p><b>Por que la respuesta sirve:</b> una politica <b>IAM</b> con una condicion que requiere la presencia de <b>bedrock:GuardrailIdentifier</b> hace que Bedrock rechace cualquier InvokeModel o Converse que no adjunte un guardrail. Es enforcement declarativo, sin infraestructura adicional: la clave de condicion hace cumplir el requisito directamente sobre la API.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>IAM + prompt router obligatorio:</b> forzar todo el trafico por un router añade complejidad y overhead innecesarios; IAM ya puede exigir el guardrail directamente sin una capa de enrutamiento.</li>'
            '<li><b>Proxy API Gateway + Lambda:</b> exige construir y mantener infraestructura propia, agrega overhead frente al enfoque IAM y aun deja margen a bypass si una app llama a Bedrock directamente.</li>'
            '<li><b>Guardar el ID en Secrets Manager:</b> almacenar el identificador no obliga a usarlo; una app podria omitir la recuperacion o llamar a Bedrock sin adjuntar el guardrail, sin garantizar cumplimiento.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Forzar guardrails en toda llamada a FM con minimo esfuerzo: politica IAM con la clave de condicion bedrock:GuardrailIdentifier. Proxies o secretos no garantizan el enforcement.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-use-independent-api.html">docs.aws guardrails y control de acceso</a></div>'
        ),
    ),
    # ============================================================
    # Q13 - Bedrock Provisioned Throughput baja latencia
    # ============================================================
    card(
        question="Un asistente de coaching en vivo debe responder con <b>muy baja latencia</b> durante <b>picos subitos</b> (torneos, lanzamientos). La empresa quiere <b>capacidad de modelo predecible</b> durante demanda pico sostenida, dentro de un <b>presupuesto mensual fijo</b>, conservando <b>auto scaling</b> para que los componentes de la aplicacion escalen sin intervencion manual. ¿Que enfoque cumple?",
        options=[
            "Usar inferencia on-demand en Amazon Bedrock y pedir aumentos de cuota de servicio para el pico; configurar auto scaling en los recursos de la aplicacion y monitorear el uso para mantenerse dentro del presupuesto",
            "Elegir un modelo de Bedrock de baja latencia para cargas en tiempo real y asignar Provisioned Throughput para capacidad de modelo predecible; configurar auto scaling en los recursos de aplicacion para que se ajusten segun la demanda",
            "Usar inferencia latency-optimized en Bedrock con cross-Region inference para distribuir peticiones entre Regiones, apoyandose en capacidad on-demand durante los picos y configurando auto scaling en la capa de aplicacion",
            "Usar batch inference de Bedrock para procesar peticiones en grandes grupos durante los picos, escalar los recursos de aplicacion automaticamente y programar ventanas de procesamiento para controlar el costo mensual",
        ],
        correct=1,
        key="aip01-q13",
        answer=(
            '<div class="verdict">Correcta: {{L}} - modelo de baja latencia con Provisioned Throughput + auto scaling de la app.</div>'
            '<p><b>El problema:</b> baja latencia en tiempo real durante picos sostenidos, con <b>capacidad de modelo predecible</b> y costo mensual fijo, sin perder auto scaling en la aplicacion.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>Provisioned Throughput</b> de Bedrock reserva capacidad dedicada del modelo (throughput garantizado) con un costo fijo y predecible, ideal para demanda pico sostenida y baja latencia. El auto scaling se aplica a los <b>recursos de la aplicacion</b> (no al modelo), cumpliendo la elasticidad pedida.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>On-demand + subir cuotas:</b> el on-demand no reserva throughput dedicado; subir cuotas permite mas peticiones pero no da la capacidad dedicada ni el costo fijo predecible que exige el pico sostenido.</li>'
            '<li><b>Latency-optimized + cross-Region + on-demand:</b> optimiza respuesta y reparte entre Regiones, pero sigue dependiendo de on-demand; ademas los inference profiles de cross-Region no soportan Provisioned Throughput, asi que no aporta la capacidad dedicada requerida.</li>'
            '<li><b>Batch inference:</b> es asincrono y escribe resultados en S3 al terminar el job; no sirve para coaching interactivo de baja latencia y ademas no soporta modelos provisionados.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Capacidad de modelo predecible + costo fijo + baja latencia en pico sostenido: reservar throughput dedicado del modelo. Los inference profiles cross-Region NO soportan esa capacidad reservada; el batch es asincrono (S3), no tiempo real.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html">docs.aws Provisioned Throughput</a></div>'
        ),
    ),
    # ============================================================
    # Q14 - Bedrock Guardrails y prompt injection
    # ============================================================
    card(
        question="Un chatbot financiero en Amazon Bedrock debe: proteger en <b>capas</b> contra <b>prompt injection</b> avanzado, dejar <b>registros de auditoria detallados cuando una regla de seguridad interviene</b> (entrada o salida bloqueada/modificada) y soportar <b>resiliencia multi-Region</b> si una Region falla. ¿Que arquitectura cumple?",
        options=[
            "Habilitar guardrails de Bedrock con filtros de contenido estrictos y adjuntar AWS WAF al endpoint de la API para inspeccionar las peticiones entrantes a nivel HTTP; registrar toda la actividad con AWS CloudTrail y confiar en el despliegue de la app para la resiliencia entre Regiones",
            "Implementar clasificadores personalizados de Amazon Comprehend para detectar prompt injection antes de que las peticiones lleguen al modelo, usar validacion de peticiones de Amazon API Gateway y exportar los logs a Amazon CloudWatch Logs para su revision posterior",
            "Configurar guardrails de Bedrock con filtros de palabras clave estrictos, habilitar el despliegue multi-Region de la aplicacion para tolerar la caida de una Region y auditar los logs de operaciones almacenados en AWS CloudTrail",
            "Configurar guardrails de Bedrock con filtros de contenido en umbral alto para mitigar prompt injection, aplicar un guardrail profile para inferencia de guardrail cross-Region, y enviar logs detallados de intervencion del guardrail a Amazon CloudWatch Logs con metricas personalizadas",
        ],
        correct=3,
        key="aip01-q14",
        answer=(
            '<div class="verdict">Correcta: {{L}} - guardrails con filtros de contenido en umbral alto + guardrail profile cross-Region + logs a CloudWatch.</div>'
            '<p><b>El problema:</b> mitigar prompt injection con proteccion a nivel del modelo, registrar cada intervencion de seguridad y ser resiliente entre Regiones.</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>filtros de contenido</b> de guardrails operan en el contexto del prompt/respuesta (donde ocurre la injection) y en umbral alto detectan manipulaciones sofisticadas. Un <b>guardrail profile</b> habilita inferencia de guardrail <b>cross-Region</b> (resiliencia). Los <b>logs de intervencion del guardrail</b> enviados a <b>CloudWatch Logs</b> (con metricas custom) capturan exactamente cuando se bloquea o modifica entrada/salida, cumpliendo la auditoria.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Guardrails + WAF + CloudTrail:</b> WAF filtra a nivel red/HTTP, pero la prompt injection vive dentro del contexto del prompt, que WAF no analiza; ademas CloudTrail registra actividad de API, no los eventos de intervencion del guardrail.</li>'
            '<li><b>Comprehend custom + API Gateway + CloudWatch:</b> los clasificadores NLP tradicionales fallan ante injection que explota el comportamiento del prompt; carece de enforcement nativo de guardrails y de capacidad cross-Region de guardrail.</li>'
            '<li><b>Guardrails con filtros de palabras + multi-Region + CloudTrail:</b> los filtros de palabras clave son insuficientes ante injection contextual, y CloudTrail registra operaciones de API, no las intervenciones detalladas del guardrail (prompts bloqueados, respuestas filtradas).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Auditar intervenciones de seguridad del modelo: logs de guardrail a CloudWatch Logs (CloudTrail solo registra la API). Resiliencia de guardrail entre Regiones: guardrail profile / cross-Region guardrail inference. WAF y filtros de palabras no frenan prompt injection contextual.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
        ),
    ),
    # ============================================================
    # Q19 - Model Context Protocol (MCP) como tools
    # ============================================================
    card(
        question="Un asistente para analistas de riesgo debe permitir que el foundation model <b>consulte dinamicamente</b> varias fuentes (precios en vivo por Amazon Kinesis Data Streams, alertas de Amazon CloudWatch y embeddings de SageMaker) de forma <b>segura y consistente</b>, <b>sin incrustar llamadas a APIs, SQL ni credenciales en los prompts</b>. ¿Que diseño cumple mejor?",
        options=[
            "Implementar funciones Lambda que encapsulen la logica de API para Kinesis, CloudWatch y los embeddings de SageMaker, y que el foundation model genere en sus prompts la sintaxis de invocacion para llamar a cada funcion",
            "Desplegar un unico servicio intermedio que exponga de forma segura Kinesis, CloudWatch y los embeddings de SageMaker como herramientas invocables mediante el Model Context Protocol (MCP), permitiendo a Bedrock consultar cada fuente dinamicamente",
            "Usar solo los embeddings de SageMaker JumpStart y apoyarse en el conocimiento financiero general del foundation model para responder las consultas",
            "Desplegar microservicios separados para cada fuente de datos y apoyarse en enrutamiento por prompt en Bedrock para seleccionar dinamicamente que servicio consultar",
        ],
        correct=1,
        key="aip01-q19",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un servicio que expone las fuentes como herramientas via MCP.</div>'
            '<p><b>El problema:</b> dar al modelo acceso dinamico, seguro y consistente a varias fuentes de datos sin poner llamadas, SQL ni credenciales dentro del prompt.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>Model Context Protocol (MCP)</b> es un estandar para exponer capacidades (Kinesis, CloudWatch, embeddings) como <b>herramientas invocables</b> a traves de una interfaz unificada. Un unico servicio intermedio MCP centraliza control de acceso, logging y validacion, y Bedrock consulta cada fuente de forma predecible y con permisos controlados, sin credenciales en el prompt.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda + el modelo genera la sintaxis de invocacion:</b> confia en que el modelo produzca llamadas correctas (inconsistente y propenso a fallos) y no centraliza control de acceso, logging ni validacion.</li>'
            '<li><b>Solo embeddings + conocimiento general:</b> los embeddings enriquecen contexto, pero no aportan precios en vivo ni alertas operativas; ignora la necesidad de consultar datos dinamicos y seguros.</li>'
            '<li><b>Microservicios + enrutamiento por prompt:</b> deja que el modelo infiera que microservicio llamar (propenso a errores y a alucinar nombres de servicio) y es dificil de asegurar; una capa MCP unificada da acceso predecible y con permisos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Exponer herramientas/datos a un LLM de forma estandar, segura y con permisos: un protocolo de herramientas unificado servido por un unico servicio intermedio. Dejar que el modelo invente llamadas o el enrutamiento por prompt es fragil e inseguro.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html">docs.aws AgentCore Gateway y MCP</a></div>'
        ),
    ),
    # ============================================================
    # Q21 - Bedrock cross-region inference profile (data residency)
    # ============================================================
    card(
        question="Un chatbot en Amazon Bedrock usa server-sent events para hacer streaming de respuestas y un <b>cross-region inference profile</b> para optimizar throughput. Debe transmitir prompts y salidas de forma <b>segura entre Regiones</b>, con los <b>datos permaneciendo dentro de EE. UU.</b> (compliance), y mantenerse <b>escalable y responsivo</b> durante picos. ¿Que enfoque cumple?",
        options=[
            "Usar Bedrock con un inference profile cross-Region global que enrute a las mejores Regiones del mundo para maximizar throughput y rendimiento del modelo, y usar Amazon Kendra para la busqueda por consultas y asi mejorar la experiencia y la relevancia de las respuestas",
            "Implementar un inference profile cross-Region ligado a la geografia de EE. UU. y enrutar a Regiones destino dentro de EE. UU.; usar SageMaker AI para manejar la inferencia en los picos habilitando Provisioned Throughput y sostener un rendimiento consistente durante las rafagas de trafico",
            "Configurar Bedrock con un inference profile cross-Region ligado a EE. UU. y usar Amazon Comprehend para analizar y categorizar las consultas del cliente antes de enrutar la inferencia, procesando solo las relevantes para mejorar el throughput del sistema",
            "Usar Bedrock con un inference profile cross-Region ligado a la geografia de EE. UU., de modo que las peticiones desde Regiones de EE. UU. se enruten a Regiones destino optimas dentro de EE. UU., manteniendo cifrados prompts y salidas en transito; ademas usar AWS Step Functions para gestionar picos y no exceder cuotas de servicio",
        ],
        correct=3,
        key="aip01-q21",
        answer=(
            '<div class="verdict">Correcta: {{L}} - inference profile cross-Region ligado a EE. UU., cifrado en transito, y Step Functions para picos.</div>'
            '<p><b>El problema:</b> optimizar throughput con cross-Region inference pero manteniendo los datos dentro de EE. UU. (data residency), con transmision segura y escalado ante picos.</p>'
            '<p><b>Por que la respuesta sirve:</b> un <b>inference profile cross-Region ligado a la geografia de EE. UU.</b> enruta solo a Regiones destino dentro de EE. UU., respetando la residencia de datos, mientras prompts y salidas viajan <b>cifrados en transito</b>. <b>Step Functions</b> ayuda a gestionar rafagas y a no exceder las cuotas del servicio.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Perfil cross-Region global:</b> enruta a Regiones fuera de EE. UU., violando el requisito de mantener los datos en EE. UU. por compliance.</li>'
            '<li><b>Perfil US + SageMaker con Provisioned Throughput:</b> Provisioned Throughput no es compatible con inference profiles cross-Region de Bedrock, y SageMaker no aporta el mecanismo de inferencia cross-Region que pide el escenario.</li>'
            '<li><b>Perfil US + Comprehend para categorizar:</b> Comprehend analiza texto (sentimiento, entidades) pero no gestiona trafico ni enrutamiento cross-Region; no resuelve el objetivo de enrutar y escalar la inferencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Data residency + throughput: inference profile cross-Region ligado a la geografia (US). Recuerda: cross-Region inference profiles NO soportan Provisioned Throughput. Comprehend no enruta trafico.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">docs.aws cross-Region inference</a></div>'
        ),
    ),
    # ============================================================
    # Q24 - Bedrock InvokeModelWithResponseStream (streaming)
    # ============================================================
    card(
        question="Un asistente de analisis de incidentes usa foundation models de Amazon Bedrock. Las peticiones complejas tardan varios segundos, y los analistas necesitan ver la <b>respuesta apareciendo de forma incremental</b> para empezar a leer de inmediato. La solucion debe manejar <b>miles de sesiones concurrentes</b> con <b>minima latencia</b> y sin esperar la respuesta completa. ¿Que arquitectura cumple mejor?",
        options=[
            "Configurar una REST API en Amazon API Gateway con integracion AWS Lambda que invoque la API InvokeModel de Bedrock y devuelva la respuesta completa al cliente cuando termina la generacion",
            "Configurar una WebSocket API en Amazon API Gateway integrada con AWS Lambda que invoque la API InvokeModelWithResponseStream de Bedrock y envie cada respuesta parcial a los clientes conectados por el WebSocket",
            "Configurar una Lambda que invoque InvokeModelWithResponseStream y guarde las respuestas parciales en Amazon DynamoDB, y que los clientes hagan polling de la tabla via Amazon API Gateway para recuperar los segmentos nuevos",
            "Configurar una REST API en Amazon API Gateway con integracion Lambda que invoque InvokeModelWithResponseStream pero acumule (buffer) la salida en la funcion y devuelva la respuesta completa en una sola respuesta HTTP",
        ],
        correct=1,
        key="aip01-q24",
        answer=(
            '<div class="verdict">Correcta: {{L}} - WebSocket API + Lambda con InvokeModelWithResponseStream.</div>'
            '<p><b>El problema:</b> mostrar la respuesta de forma incremental (streaming) con baja latencia y miles de sesiones concurrentes, sin esperar la salida completa.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>InvokeModelWithResponseStream</b> entrega la salida en fragmentos a medida que se genera. Una <b>WebSocket API</b> de API Gateway permite <b>empujar</b> cada fragmento a los clientes conectados en tiempo real, cubriendo el streaming incremental y la baja latencia a escala.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>REST + InvokeModel (respuesta completa):</b> InvokeModel sigue un patron request-response y devuelve la salida al final; no da los fragmentos incrementales requeridos.</li>'
            '<li><b>InvokeModelWithResponseStream + DynamoDB + polling:</b> guardar fragmentos y hacer polling añade operaciones de base de datos y peticiones repetidas; el WebSocket empuja directamente y elimina el polling, mejor para minima latencia.</li>'
            '<li><b>REST + buffer en Lambda:</b> usa el streaming solo internamente, pero el usuario espera a que se ensamble toda la respuesta antes de recibir nada, anulando el requisito de mostrarla incrementalmente.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Respuesta incremental (streaming) a escala: la API de invocacion con response stream + una API bidireccional que empuja los fragmentos al cliente. InvokeModel es request-response; el polling o el buffering rompen el streaming.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/inference-invoke.html">docs.aws invocar modelos (streaming)</a></div>'
        ),
    ),
    # ============================================================
    # Q25 - Amazon Augmented AI (A2I) human review
    # ============================================================
    card(
        question="Una aseguradora procesa miles de documentos con Amazon Textract y Amazon Comprehend, pero <b>formatos inconsistentes y errores de OCR</b> hacen que ciertos documentos <b>fallen la validacion automatica</b> y requieran revision humana, creando cuellos de botella. Quiere <b>reducir la revision manual</b> manteniendo alta precision/recall y que los sistemas downstream consuman datos fiables. ¿Cual es la forma mas efectiva?",
        options=[
            "Desplegar un modelo Claude de Amazon Bedrock para reanalizar el texto extraido de baja confianza y refinar las predicciones de validacion, y luego enrutar las salidas a revision manual",
            "Usar Textract para marcar palabras de baja confianza y enviarlas a Amazon SageMaker Ground Truth para inspeccion manual antes de la validacion",
            "Configurar Textract para reenviar las predicciones de baja confianza a Amazon Augmented AI (Amazon A2I) para verificacion antes de ejecutar los flujos de validacion",
            "Automatizar mas la validacion enviando el texto extraido a un foundation model Amazon Titan para predecir errores sin revision humana",
        ],
        correct=2,
        key="aip01-q25",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Textract reenvia lo de baja confianza a Amazon A2I.</div>'
            '<p><b>El problema:</b> reducir la revision manual pero mantener precision, enrutando solo los casos de baja confianza a un flujo de revision humana integrado con el pipeline.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Amazon Augmented AI (A2I)</b> es el servicio gestionado para <b>human-in-the-loop</b> durante la inferencia: se integra con Textract para enviar las predicciones de <b>baja confianza</b> a revisores humanos antes de continuar la validacion. Asi baja el volumen de revision (solo lo incierto) manteniendo la calidad.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Claude de Bedrock reanalizando:</b> Bedrock sirve para generacion, no para revision humana basada en confianza; no se integra con Textract para enrutar predicciones de baja confianza a verificacion, por lo que no encaja en la validacion de documentos.</li>'
            '<li><b>SageMaker Ground Truth:</b> esta pensado para crear datasets etiquetados de entrenamiento, no para validacion de documentos en produccion en tiempo real; carece de integracion nativa con Textract para verificacion automatica.</li>'
            '<li><b>Titan sin revision humana:</b> usar un FM para predecir errores sin verificacion humana aumenta el riesgo de errores en un proceso orientado a compliance; no reemplaza el scoring de confianza ni la revision humana.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Human-in-the-loop en inferencia (marcar baja confianza y enviar a personas): Amazon A2I, integrado con Textract/Rekognition/Comprehend. Ground Truth es para etiquetar datasets de entrenamiento, no revision de produccion.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/textract/latest/dg/a2i-textract.html">docs.aws Textract con Amazon A2I</a></div>'
        ),
    ),
    # ============================================================
    # Q26 - Bedrock Custom Model Import
    # ============================================================
    card(
        question="Un sistema de recomendaciones con Amazon Bedrock AgentCore usara un <b>LLM ya fine-tuned en SageMaker AI</b>. La solucion debe garantizar <b>inferencia segura y escalable en tiempo real dentro del entorno de Bedrock</b>, monitorear latencia y metricas en Amazon CloudWatch, y <b>minimizar el overhead operativo</b>. ¿Que solucion cumple?",
        options=[
            "Desplegar el LLM fine-tuned en SageMaker AI, configurar una Lambda para invocar los endpoints de SageMaker y monitorear el rendimiento con metricas de CloudWatch",
            "Importar el modelo fine-tuned directamente a Bedrock con Custom Model Import, asignar un rol de ejecucion gestionado por AgentCore y configurar CloudWatch para monitorear en tiempo real las metricas del modelo",
            "Hospedar el LLM en una instancia Amazon EC2, conectarlo a Bedrock AgentCore via una REST API y usar CloudWatch Logs para monitorear las llamadas a la API",
            "Guardar el modelo en Amazon S3, configurar Bedrock AgentCore para cargarlo en tiempo de ejecucion y usar CloudWatch para monitorear el rendimiento de la API",
        ],
        correct=1,
        key="aip01-q26",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Custom Model Import + rol gestionado + CloudWatch.</div>'
            '<p><b>El problema:</b> servir un modelo propio fine-tuned <b>dentro de Bedrock</b> con inferencia segura y escalable en tiempo real y minima operacion.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Custom Model Import</b> lleva el modelo fine-tuned directamente a Bedrock y lo sirve con la experiencia serverless de baja latencia del servicio (sin gestionar infraestructura), integrandose con Knowledge Bases, Guardrails y Agents. Con un rol gestionado por AgentCore y CloudWatch para metricas se cubre seguridad y monitoreo con poco overhead.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SageMaker + Lambda invocando endpoints:</b> añade una capa (Lambda) que gestionar y escalar, con posibles cold starts y mayor latencia; se aleja de la experiencia serverless de baja latencia de Bedrock.</li>'
            '<li><b>EC2 + REST API:</b> requiere aprovisionar, escalar y parchear manualmente, introduce puntos de fallo y latencia, y no integra de forma nativa con Knowledge Bases/Guardrails/Agents de Bedrock.</li>'
            '<li><b>Modelo en S3 cargado en runtime:</b> cargar el modelo dinamicamente en cada inferencia genera cuellos de botella de latencia (sobre todo con modelos grandes) y es menos eficiente que tenerlo importado y optimizado en Bedrock.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Servir un modelo propio DENTRO de Bedrock con minima operacion: importar el modelo personalizado a Bedrock (serverless, integrado con guardrails, knowledge bases y agentes). SageMaker+Lambda, EC2 o carga desde S3 en runtime añaden overhead y latencia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-import-model.html">docs.aws Custom Model Import</a></div>'
        ),
    ),
    # ============================================================
    # Q27 - Bedrock cross-region inference profile (capacidad)
    # ============================================================
    card(
        question="Durante un pico internacional, un asistente de Amazon Bedrock recibe un <b>aumento subito e impredecible</b> de peticiones desde Europa y Asia Pacifico. El equipo debe mantener <b>respuestas de baja latencia globalmente</b> cumpliendo <b>data residency</b> con el <b>menor overhead operativo</b>. ¿Que solucion cumple?",
        options=[
            "Desplegar endpoints de inferencia de SageMaker AI en varias Regiones y dirigir el trafico a la Region mas cercana con una politica de enrutamiento por latencia en Amazon Route 53",
            "Usar procesamiento en tiempo real de Comprehend en una Region central y copiar los datos de interaccion a Regiones cercanas antes de la demanda prevista",
            "Usar el inference profile cross-Region de Bedrock para que las llamadas de una Region se enruten automaticamente a otra Region con capacidad de computo disponible",
            "Desplegar el foundation model elegido en cada Region de Europa y Asia Pacifico via Bedrock y gestionar la distribucion de trafico con un mecanismo de enrutamiento propio en el cliente",
        ],
        correct=2,
        key="aip01-q27",
        answer=(
            '<div class="verdict">Correcta: {{L}} - inference profile cross-Region de Bedrock.</div>'
            '<p><b>El problema:</b> absorber un pico impredecible manteniendo baja latencia global y data residency, con la menor operacion posible, sobre la carga generativa de Bedrock.</p>'
            '<p><b>Por que la respuesta sirve:</b> el <b>inference profile cross-Region</b> de Bedrock enruta automaticamente las llamadas a otra Region (dentro de la geografia definida) con capacidad disponible, absorbiendo picos sin gestionar infraestructura extra. Es la opcion nativa de menor overhead para esta carga.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Endpoints de SageMaker multi-Region + Route 53:</b> obliga a gestionar endpoints separados (mas overhead) y no atiende directamente la carga generativa basada en Bedrock del asistente.</li>'
            '<li><b>Comprehend en tiempo real + copiar datos:</b> el problema es escalar la inferencia de Bedrock, no procesar texto con Comprehend; no aborda ni la baja latencia generativa ni la residencia de datos de Bedrock.</li>'
            '<li><b>Desplegar el FM por Region + enrutamiento propio en el cliente:</b> requiere construir y mantener una solucion de routing en el cliente, con overhead y complejidad considerables.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Picos impredecibles de inferencia Bedrock con minima operacion: cross-Region inference profile (enruta a Regiones con capacidad dentro de la geografia). Routing propio o multi-endpoint de SageMaker suman overhead.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">docs.aws cross-Region inference</a></div>'
        ),
    ),
    # ============================================================
    # Q30 - SageMaker Asynchronous Inference endpoint
    # ============================================================
    card(
        question="Una plataforma genera texto de accesibilidad para <b>imagenes de hasta 60 MB</b> subidas a Amazon S3, con <b>picos de trafico impredecibles</b>. El flujo (Rekognition, luego Bedrock para captions) <b>arranca automaticamente al subir una imagen</b>. Se necesita una solucion que <b>escale automaticamente</b>, mantenga alta disponibilidad en picos y opere con <b>minima gestion de infraestructura</b>. ¿Que solucion cumple?",
        options=[
            "Construir un pipeline con Amazon ECS on Fargate que corra por schedule para procesar las imagenes e insertar los datos procesados en Amazon Aurora",
            "Desplegar un endpoint de Amazon SageMaker Asynchronous Inference con una politica de escalado que ajuste la capacidad automaticamente y procese cada imagen del bucket S3",
            "Lanzar un Amazon EC2 Auto Scaling group que hospede una app de inferencia que monitorea el bucket S3 y guarda los resultados en otro bucket",
            "Usar Amazon SQS para encolar tareas y disparar funciones AWS Lambda que ejecuten Rekognition y Bedrock por cada imagen subida",
        ],
        correct=1,
        key="aip01-q30",
        answer=(
            '<div class="verdict">Correcta: {{L}} - endpoint de SageMaker Asynchronous Inference con auto scaling.</div>'
            '<p><b>El problema:</b> procesar imagenes grandes (hasta 60 MB) ante picos impredecibles, con escalado automatico, alta disponibilidad y minima gestion de infraestructura.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>SageMaker Asynchronous Inference</b> encola las peticiones internamente, maneja payloads grandes y tareas largas, y su politica de <b>auto scaling</b> ajusta capacidad (incluso a cero) segun la cola. Es gestionado (sin servidores que administrar) y absorbe picos, encajando con el disparo por subida a S3.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>ECS on Fargate por schedule:</b> las tareas programadas responden a un horario fijo, no a eventos de subida a S3; aunque Fargate quita servidores, aun exige configurar scheduling, monitoreo y escalado, sin la responsividad event-driven pedida.</li>'
            '<li><b>EC2 Auto Scaling group:</b> requiere gestion continua de infraestructura (parcheo, escalado, monitoreo) y carece del encolado y procesamiento asincrono nativos; mas overhead y escalado menos eficiente.</li>'
            '<li><b>SQS + Lambda:</b> Lambda tiene limites de payload, memoria y tiempo de ejecucion, inadecuados para imagenes de hasta 60 MB y jobs de inferencia largos; en picos podria fallar o hacer timeout.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Payloads grandes o inferencia larga con picos y escalado a cero: el endpoint asincrono gestionado de SageMaker (encola y escala solo). Lambda topa en 15 min y payload limitado; ECS/EC2 suman gestion de infraestructura.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html">docs.aws SageMaker Asynchronous Inference</a></div>'
        ),
    ),
    # ============================================================
    # Q32 - Bedrock model invocation logging (S3+CloudWatch)
    # ============================================================
    card(
        question="Por compliance, un equipo debe tener <b>trazabilidad completa de cada invocacion</b> de Bedrock (prompt de entrada, respuesta, metadatos) y almacenarla para auditoria, consulta y retencion. La solucion debe: registrar <b>todas</b> las invocaciones (Converse, ConverseStream, InvokeModel, InvokeModelWithResponseStream), permitir <b>almacenar salidas binarias de imagen</b> y soportar <b>analitica consultable</b> posterior. ¿Que solucion cumple?",
        options=[
            "Habilitar los model invocation logs de Bedrock y configurar como destinos tanto un bucket de Amazon S3 como un log group de Amazon CloudWatch Logs; almacenar datos de texto e imagen",
            "Usar Amazon Data Firehose para capturar y hacer streaming de todos los logs de invocacion a Amazon S3 y Amazon OpenSearch Service para analitica",
            "Habilitar los model invocation logs de Bedrock y configurar un bucket de Amazon S3 como unico destino; almacenar datos de texto e imagen",
            "Usar AWS CloudTrail para capturar todas las invocaciones de Bedrock, almacenar los logs en Amazon S3 y ejecutar analitica con Amazon Athena",
        ],
        correct=0,
        key="aip01-q32",
        answer=(
            '<div class="verdict">Correcta: {{L}} - model invocation logs de Bedrock hacia S3 y CloudWatch Logs.</div>'
            '<p><b>El problema:</b> registrar el contenido completo de cada invocacion (prompt, respuesta, metadatos), incluyendo salidas binarias de imagen, y poder consultarlo/monitorearlo despues.</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>model invocation logs</b> de Bedrock capturan entradas, salidas y metadatos de todas las APIs de invocacion. Usar <b>S3</b> permite retener texto e <b>imagenes</b> (objetos binarios grandes), y <b>CloudWatch Logs</b> agrega monitoreo en tiempo casi real, insights de consulta y alertas para las metricas de auditoria.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Data Firehose a S3 + OpenSearch:</b> Bedrock no soporta Data Firehose como destino de los model invocation logs, asi que no aplica.</li>'
            '<li><b>Solo S3 como destino:</b> S3 guarda texto e imagen, pero pierde las capacidades de consulta y monitoreo en tiempo casi real de CloudWatch Logs (insights y alertas) utiles para metricas de auditoria.</li>'
            '<li><b>CloudTrail + S3 + Athena:</b> CloudTrail registra la actividad de API (quien llamo), pero no los prompts, respuestas ni payloads; no cumple la trazabilidad completa ni captura salidas binarias.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Contenido de las invocaciones (prompt/respuesta/imagenes): model invocation logging de Bedrock, con dos destinos (almacenamiento de objetos para binarios y un servicio de logs para consulta y alertas). El servicio de auditoria de API solo registra quien llamo, no los payloads.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html">docs.aws model invocation logging</a></div>'
        ),
    ),
    # ============================================================
    # Q34 - Amazon Q Business ACL por grupo (acl.json)
    # ============================================================
    card(
        question="Una firma usa Amazon Q Business sobre documentos en S3 con prefijos por departamento (Finanzas, Legal, RR. HH., Ingenieria). Los empleados se autentican con IAM Identity Center y cada departamento mapea a un grupo. Q Business debe <b>devolver solo informacion del prefijo del grupo del empleado</b> conectado, <b>sin mantener metadatos de control de acceso por cada documento</b> y con minimo esfuerzo administrativo. ¿Que solucion cumple?",
        options=[
            "Crear data sources (conectores) de Q Business separados por cada prefijo de departamento, configurar un rol IAM distinto por departamento restringido a su prefijo de S3 y sincronizar cada conector de forma independiente cada vez que cambie el contenido de esa carpeta",
            "Crear archivos de metadatos individuales para cada documento en el bucket con el grupo de IAM Identity Center apropiado y volver a sincronizar el data source cada vez que cambie la membresia de grupos de cualquier empleado",
            "Crear un unico archivo acl.json en la raiz del bucket que defina, por departamento, el prefijo de S3, el grupo de IAM Identity Center y el permiso de acceso a nivel de grupo; luego habilitar control de acceso en el data source S3 de Q Business e indicar la ruta al acl.json para que Q Business aplique el mapeo prefijo-grupo durante la recuperacion",
            "Aplicar bucket policies de S3 que den a cada grupo de IAM Identity Center acceso solo a su prefijo de departamento y configurar Q Business para rastrear todo el bucket, confiando en la bucket policy para filtrar las respuestas de cada usuario durante la recuperacion",
        ],
        correct=2,
        key="aip01-q34",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un unico acl.json con mapeo prefijo-grupo en el data source S3.</div>'
            '<p><b>El problema:</b> que Q Business filtre las respuestas segun el grupo del usuario a nivel de prefijo, sin mantener ACL por documento y con minimo esfuerzo.</p>'
            '<p><b>Por que la respuesta sirve:</b> un unico <b>acl.json</b> en la raiz define, por departamento, la relacion prefijo de S3 + grupo de IAM Identity Center + permiso. Al habilitar control de acceso en el data source S3 e indicar ese archivo, Q Business aplica el mapeo <b>a nivel de prefijo</b> durante la recuperacion, asi la misma regla cubre todos los documentos bajo el prefijo sin metadatos por archivo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Data sources y roles IAM por departamento:</b> los roles del data source autorizan a Q Business a ingerir contenido, no filtran por usuario; crear un conector y rol por departamento añade configuracion y mantenimiento cuando un solo conector con ACL por prefijo basta.</li>'
            '<li><b>Metadatos por documento:</b> exige mantener control de acceso archivo por archivo (y re-sincronizar ante cada cambio de grupo), justo lo que se quiere evitar; el ACL por prefijo aplica automaticamente a todo lo que cuelga de el.</li>'
            '<li><b>Bucket policies de S3:</b> controlan si un principal de AWS puede operar sobre recursos S3; no reemplazan la ACL de documento que Q Business indexa para filtrar respuestas por usuario/grupo durante la recuperacion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Filtrar respuestas de Q Business por grupo sin ACL por documento: acl.json a nivel de prefijo en el conector S3. Las bucket policies controlan acceso a objetos, no el filtrado de respuestas por usuario.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/s3-data-source-connector.html">docs.aws conector S3 de Q Business (ACL)</a></div>'
        ),
    ),
    # ============================================================
    # Q35 - SageMaker Ground Truth Plus human-in-the-loop
    # ============================================================
    card(
        question="Un sistema resume historiales medicos con un LLM fine-tuned en SageMaker. Antes del despliegue pleno, los <b>profesionales de salud deben revisar y corregir</b> los resumenes generados por su alto impacto. La solucion debe <b>escalar a grandes volumenes</b> e <b>integrarse con los pipelines de SageMaker</b> para reentrenamiento y despliegue fluidos. ¿Que enfoque cumple mejor?",
        options=[
            "Usar SageMaker Model Monitor para detectar y marcar resumenes de baja confianza para revision del medico y guardar los casos marcados en S3 para revision manual antes del despliegue",
            "Aprovechar la knowledge base de Amazon Bedrock para enriquecer el dataset de entrenamiento con conocimiento externo y mejorar el rendimiento del modelo antes de desplegar",
            "Implementar Amazon Augmented AI (A2I) para crear un proceso de revision humana y que los profesionales validen y refinen los resumenes antes del despliegue a escala",
            "Usar SageMaker Ground Truth Plus para crear un flujo human-in-the-loop de validacion y correccion por expertos, e integrarlo con el pipeline de SageMaker existente para reentrenamiento y despliegue fluidos",
        ],
        correct=3,
        key="aip01-q35",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Ground Truth Plus (human-in-the-loop gestionado).</div>'
            '<p><b>El problema:</b> revision y correccion por expertos a gran escala, integrada con los pipelines de SageMaker para reentrenar y desplegar de forma fluida.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Ground Truth Plus</b> ofrece operaciones de revision humana y etiquetado <b>gestionadas y escalables</b>, ideales para industrias reguladas. Permite que expertos validen y corrijan los resumenes y esos datos alimentan el pipeline de SageMaker para reentrenamiento y despliegue continuos.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SageMaker Model Monitor:</b> detecta drift, sesgo o degradacion de calidad del modelo desplegado; puede marcar baja confianza, pero no provee un flujo estructurado de validacion y correccion humana ni integra feedback continuo de expertos.</li>'
            '<li><b>Knowledge base de Bedrock:</b> enriquece con datos externos (RAG), pero no garantiza correccion clinica ni cumplimiento; la validacion regulatoria exige revision humana explicita, que no aporta.</li>'
            '<li><b>Amazon A2I:</b> sirve para tareas puntuales de revision humana en inferencia, no para operaciones de etiquetado y correccion a gran escala integradas al reentrenamiento; Ground Truth Plus extiende esa capacidad con revision gestionada y escalable.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Revision/correccion experta gestionada y a escala, ligada al reentrenamiento: la operacion de etiquetado humano gestionada de SageMaker. A2I es revision puntual en inferencia; Model Monitor detecta drift, no valida contenido clinico.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/gtp.html">docs.aws SageMaker Ground Truth Plus</a></div>'
        ),
    ),
    # ============================================================
    # Q37 - Bedrock Knowledge Bases con citations y reranking
    # ============================================================
    card(
        question="Un asistente de inteligencia regulatoria en Amazon Bedrock recupera de multiples fuentes internas. Cada afirmacion debe <b>citar la fuente</b> trazable al documento original, la recuperacion debe <b>priorizar solo el contenido mas relevante</b> y se debe <b>almacenar el razonamiento y las citas para auditoria</b> con el <b>MENOR esfuerzo operativo</b>. ¿Que arquitectura cumple mejor?",
        options=[
            "Usar Bedrock Knowledge Bases para recuperar documentos, invocar un modelo Claude directamente con el texto recuperado y que la propia aplicacion genere sus propios enlaces de fuente, arme las citas a mano y guarde las respuestas finales en Amazon DynamoDB para consultarlas despues",
            "Usar Bedrock Knowledge Bases con RetrieveAndGenerate para generar respuestas con citas, devolviendo todos los chunks recuperados al modelo Claude sin reranking ni filtro de relevancia, y guardar solo la respuesta final en Amazon S3",
            "Configurar Bedrock Knowledge Bases para recuperar documentos altamente relevantes y devolver citas al contenido de soporte, aplicar reranking para priorizar los resultados mas relevantes antes de enviar el contexto a un modelo Claude via la Messages API, y guardar el razonamiento y las citas en Amazon S3 para auditoria",
            "Usar Bedrock Agents con una knowledge base para recuperar documentos, configurar las instrucciones del agente para explicar cada recomendacion y citar los documentos, y enviar la salida generada a Amazon CloudWatch Logs para auditoria",
        ],
        correct=2,
        key="aip01-q37",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Knowledge Bases con citas + reranking + Messages API, auditoria en S3.</div>'
            '<p><b>El problema:</b> RAG con citas trazables, priorizando solo lo mas relevante y guardando razonamiento y citas para auditoria, con minima operacion.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Knowledge Bases</b> recupera y devuelve <b>citas</b> al contenido de soporte de forma nativa. Aplicar <b>reranking</b> prioriza los chunks mas relevantes (mejor precision, menor latencia y costo) antes de enviarlos al modelo por la <b>Messages API</b>. Guardar razonamiento y citas en <b>S3</b> conserva artefactos durables para auditoria. Todo con poco desarrollo custom.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>KB + Claude directo + enlaces propios + DynamoDB:</b> recrea a mano la funcionalidad de citas que Knowledge Bases ya ofrece (RetrieveAndGenerate), añadiendo desarrollo y riesgo de desalinear afirmaciones con fuentes.</li>'
            '<li><b>RetrieveAndGenerate sin reranking + solo respuesta final:</b> devolver todos los chunks deja pasar contenido poco relevante; guardar solo la respuesta omite las citas y el razonamiento requeridos para auditoria.</li>'
            '<li><b>Bedrock Agents + CloudWatch Logs:</b> los agentes orquestan flujos multi-paso con herramientas; aqui solo hace falta recuperar, rankear, generar, citar y guardar, asi que el agente añade complejidad; ademas S3 es mejor que CloudWatch Logs para retener artefactos estructurados de auditoria.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG con citas trazables y minima operacion: Knowledge Bases (RetrieveAndGenerate) + reranking para relevancia. Guarda citas/razonamiento en S3 (durable), no solo la respuesta; evita reinventar las citas a mano.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases</a></div>'
        ),
    ),
    # ============================================================
    # Q40 - Bedrock Model Evaluations job
    # ============================================================
    card(
        question="Un equipo quiere <b>evaluar sistematicamente distintas configuraciones</b> de modelos (variante, temperatura, estrategias de prompt) para medir <b>exactitud y robustez</b> ante un dataset de consultas de compliance, usando modelos out-of-the-box y personalizados de Amazon Bedrock. ¿Que solucion cumple este requisito?",
        options=[
            "Configurar un job de evaluacion con Bedrock Model Evaluations, especificar el task type Question and answer y seleccionar metricas como exactitud y robustez, con un prompt dataset personalizado",
            "Usar Amazon CloudWatch Synthetics para simular consultas de usuario a los modelos de Bedrock y monitorear su rendimiento por tiempo de respuesta y disponibilidad",
            "Configurar un job de evaluacion con Bedrock Model Evaluations, especificar el task type Question and answer y seleccionar metricas como exactitud y robustez, con un dataset predefinido",
            "Usar SageMaker Debugger para analizar el rendimiento del modelo y comparar configuraciones inspeccionando salidas por capa y gradientes",
        ],
        correct=0,
        key="aip01-q40",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Model Evaluations (Q&A) con dataset de prompts personalizado.</div>'
            '<p><b>El problema:</b> comparar de forma sistematica configuraciones de modelo por exactitud y robustez sobre consultas de compliance especificas del dominio.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Model Evaluations</b> ejecuta jobs de evaluacion sobre datasets definidos; con el task type <b>Question and answer</b> y metricas como exactitud y robustez, y un <b>dataset de prompts personalizado</b>, se refleja la naturaleza especifica de las consultas regulatorias y se comparan las configuraciones de forma medible.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CloudWatch Synthetics:</b> monitorea disponibilidad y latencia de aplicaciones, no evalua exactitud ni robustez de las respuestas del modelo.</li>'
            '<li><b>Model Evaluations con dataset predefinido:</b> el enfoque correcto es Model Evaluations, pero un dataset predefinido no refleja el dominio regulatorio; se necesita un prompt dataset personalizado para una evaluacion significativa.</li>'
            '<li><b>SageMaker Debugger:</b> es para debugging de entrenamiento (gradientes, overfitting), no para evaluar prompts ni comparar configuraciones de inferencia (temperatura, estrategias de prompt) de modelos desplegados.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Evaluar exactitud/robustez de modelos y configuraciones: Bedrock Model Evaluations con dataset de prompts personalizado (no predefinido). Synthetics mide disponibilidad; Debugger es para training.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html">docs.aws Bedrock Model Evaluations</a></div>'
        ),
    ),
    # ============================================================
    # Q46 - MCP servers stateless en ECS autoescalado
    # ============================================================
    card(
        question="Servidores MCP consumen la <b>AWS Cloud Control API</b> y sufren respuestas <b>lentas o incompletas</b> con inventarios grandes o multi-Region. Se necesita <b>latencia predecible</b> para los agentes LLM y servidores MCP <b>stateless</b> para escalabilidad horizontal y failover, mejorando <b>throughput, concurrencia y consistencia</b> al consultar la Cloud Control API. ¿Que enfoque cumple mejor?",
        options=[
            "Ejecutar servidores MCP stateless en una capa Amazon ECS autoescalada con batching y concurrencia controlados para las peticiones a la Cloud Control API, usando gestion de estado externa para coordinar entre instancias",
            "Poner Amazon API Gateway delante de las llamadas de los servidores MCP a la Cloud Control API y habilitar throttling y cache de respuestas para absorber la concurrencia de los inventarios grandes o multi-Region",
            "Usar Amazon EventBridge para que los servidores MCP invoquen las operaciones de la Cloud Control API de forma asincrona y escribir los resultados en Amazon S3 para que los agentes los lean despues del procesamiento",
            "Agregar Amazon ElastiCache for Redis como capa de cache para las respuestas de la Cloud Control API que consumen los servidores MCP, sirviendo desde memoria los estados de recursos consultados con frecuencia",
        ],
        correct=0,
        key="aip01-q46",
        answer=(
            '<div class="verdict">Correcta: {{L}} - servidores MCP stateless en ECS autoescalado con batching/concurrencia y estado externo.</div>'
            '<p><b>El problema:</b> mejorar throughput, concurrencia y consistencia al consultar la Cloud Control API, con latencia predecible y servidores MCP stateless para escalar y hacer failover.</p>'
            '<p><b>Por que la respuesta sirve:</b> ejecutar los MCP <b>stateless</b> en <b>ECS autoescalado</b> permite escalar horizontalmente y tolerar fallos; el <b>batching y la concurrencia controlados</b> mejoran throughput sin saturar la API, y la <b>gestion de estado externa</b> coordina entre instancias manteniendo el diseño stateless. Ataca directamente los cuellos de botella de concurrencia y latencia.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>API Gateway con throttling y cache:</b> es una capa de entrega de APIs; no mejora el rendimiento de fondo de la Cloud Control API ni resuelve la latencia/concurrencia al recuperar inventarios grandes o multi-Region.</li>'
            '<li><b>EventBridge asincrono + S3:</b> introduce procesamiento asincrono, incompatible con la inspeccion de recursos sincrona y de baja latencia que exigen los flujos MCP.</li>'
            '<li><b>ElastiCache for Redis:</b> los estados de recursos cambian con frecuencia; cachearlos arriesga informacion obsoleta y no garantiza sincronizacion en tiempo real de datos autoritativos de AWS.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Escalar servidores sin estado con throughput/concurrencia y consistencia: una capa de contenedores autoescalada + batching/concurrencia controlados + estado externo. Cache (Redis) arriesga datos obsoletos; EventBridge es asincrono.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html">docs.aws ECS Service Auto Scaling</a></div>'
        ),
    ),
    # ============================================================
    # Q47 - Generative AI Security Scoping Matrix (Scope 4)
    # ============================================================
    card(
        question="Una empresa hace <b>fine-tuning de un foundation model de SageMaker JumpStart</b> con datos propios sensibles y lo despliega como endpoint en tiempo real, con una knowledge base en OpenSearch. Debe mapear correctamente la <b>Generative AI Security Scoping Matrix</b> e implementar los controles adecuados. ¿Cual describe mejor el scope y la responsabilidad de seguridad clave?",
        options=[
            "Scope 3: Modelos preentrenados. La empresa es responsable de revisar la licencia y los terminos del FM para confirmar que el proveedor no use los datos propios para reentrenar",
            "Scope 4: Modelos fine-tuned. La empresa debe clasificar y cifrar todos los datos de entrenamiento propios (en reposo y en transito), controlar estrictamente el acceso y mantener un rastro de auditoria de versiones del modelo, linaje de datos y procesos de fine-tuning",
            "Scope 2: Aplicaciones empresariales. La responsabilidad principal es hacer cumplir terminos contractuales, SLAs y restricciones de uso de datos del proveedor, porque el modelo se accede solo via un servicio gestionado de terceros",
            "Scope 5: Modelos entrenados desde cero. La empresa asume la propiedad total de la infraestructura del modelo, incluidos clusteres de GPU, pipelines de entrenamiento, configuraciones de seguridad y gobierno de release y versionado",
        ],
        correct=1,
        key="aip01-q47",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Scope 4: modelos fine-tuned.</div>'
            '<p><b>El problema:</b> ubicar el workload en la Generative AI Security Scoping Matrix. La clave es que la empresa <b>hace fine-tuning</b> de un FM con datos propios, no que solo lo consume ni que lo entrena desde cero.</p>'
            '<p><b>Por que la respuesta sirve:</b> hacer fine-tuning con datos propios corresponde al <b>Scope 4 (fine-tuned models)</b>. Las responsabilidades van mas alla del proveedor: clasificar y cifrar los datos de entrenamiento en reposo y en transito, controlar acceso estricto y mantener auditoria de versiones del modelo, linaje de datos y procesos de fine-tuning.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Scope 3 (preentrenados):</b> aplica cuando solo se consume el modelo revisando licencia/terminos; aqui se esta fine-tuneando con datos propios, lo que amplia las responsabilidades a asegurar el dataset y las versiones (propio del Scope 4).</li>'
            '<li><b>Scope 2 (apps empresariales):</b> es para SaaS/productos gestionados donde la responsabilidad es sobre todo contractual; aqui la empresa maneja y fine-tunea el modelo, exigiendo controles mas amplios.</li>'
            '<li><b>Scope 5 (desde cero):</b> aplica al construir el modelo en infraestructura propia de extremo a extremo; usar JumpStart para fine-tuning evita gestionar toda la infraestructura, asi que es Scope 4, no 5.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Fine-tuning de un FM con datos propios = Scope 4. Solo consumir un preentrenado = Scope 3; SaaS gestionado = Scope 2; entrenar desde cero en infra propia = Scope 5.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/whitepapers/latest/generative-ai-security-scoping-matrix/generative-ai-security-scoping-matrix.html">docs.aws Generative AI Security Scoping Matrix</a></div>'
        ),
    ),
    # ============================================================
    # Q48 - Bedrock Guardrails content filters + automated reasoning
    # ============================================================
    card(
        question="Un asistente financiero usa SageMaker (fine-tuning) y Amazon Kendra (busqueda semantica sobre documentos regulatorios). Debe implementar frameworks de <b>content safety</b> para <b>evitar consejos inexactos</b>, <b>no filtrar datos personales de inversores</b> y <b>defenderse de prompt injection</b>. ¿Que solucion cumple?",
        options=[
            "Configurar Amazon Bedrock Guardrails con filtros de contenido y automated reasoning checks, y adjuntarlos tanto a los resultados de recuperacion de Kendra como a la salida del modelo de SageMaker",
            "Configurar Kendra para aplicar filtros de busqueda semantica a los documentos regulatorios y usar SageMaker para refinar las respuestas y que cumplan la regulacion",
            "Configurar SageMaker para monitorear y limitar las salidas del modelo con post-procesamiento, y usar los query filters de Kendra para prevenir prompt injection antes de pasar las consultas al modelo",
            "Usar las funciones de compliance integradas de Amazon Bedrock para aplicar filtros regulatorios segun el contenido de la consulta y luego invocar el modelo de SageMaker solo cuando se confirme el cumplimiento",
        ],
        correct=0,
        key="aip01-q48",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Guardrails (filtros de contenido + automated reasoning) sobre Kendra y la salida del modelo.</div>'
            '<p><b>El problema:</b> aplicar barreras de seguridad de contenido antes y despues de la generacion: evitar consejos inexactos, no filtrar PII y resistir prompt injection.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Guardrails</b> provee filtros de contenido, filtros de informacion sensible (PII) y <b>automated reasoning checks</b> (verificacion logica contra politicas) de forma nativa. Adjuntarlos tanto a los <b>resultados de Kendra</b> (entrada/contexto) como a la <b>salida del modelo</b> protege ambos extremos: bloquea completaciones inseguras, redacta datos sensibles y mitiga injection.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Kendra + SageMaker para refinar:</b> Kendra mejora la relevancia y SageMaker afina salidas, pero ninguno aporta guardrails ni chequeos de seguridad; no bloquea completaciones inseguras, no redacta PII ni frena injection.</li>'
            '<li><b>Post-procesamiento en SageMaker + query filters de Kendra:</b> el post-procesamiento es reactivo (no garantiza seguridad antes de generar) y los query filters de Kendra no sanitizan el contenido recuperado ni las injection embebidas.</li>'
            '<li><b>Funciones de compliance integradas de Bedrock:</b> no protegen contra salidas inseguras ni prompt injection a menos que se configuren explicitamente guardrails; por si solas no cumplen el requisito.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Content safety (PII, injection, consejos inexactos): las barreras de seguridad nativas de Bedrock, aplicadas a entrada Y salida. El post-procesamiento es reactivo; los filtros de Kendra no sanitizan injection.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html">docs.aws Bedrock Guardrails</a></div>'
        ),
    ),
    # ============================================================
    # Q52 - Bedrock Agent traces (Pre/Orchestration/PostProcessing)
    # ============================================================
    card(
        question="Un agente de Amazon Bedrock da respuestas inconsistentes y alucinaciones. El equipo necesita observabilidad que exponga <b>como el agente interpreta prompts, razona y genera respuestas</b> (no solo la salida), <b>reducir alucinaciones</b>, medir la <b>tasa de alucinacion en el tiempo</b> y validar el comportamiento contra el razonamiento esperado. ¿Cual cumple?",
        options=[
            "Configurar el agente con model invocation logs y muestreo de respuestas; analizar tendencias de exactitud y calcular la tasa de alucinacion comparando respuestas finales con un golden dataset",
            "Habilitar GuardrailTrace y RoutingClassifierTrace y analizar ModelInvocationInput para evaluar el enrutamiento de prompts y las decisiones de seguridad; comparar respuestas muestreadas con un golden dataset para estimar la tasa de alucinacion",
            "Habilitar PreProcessingTrace, OrchestrationTrace y PostProcessingTrace y validar continuamente el comportamiento del agente con un golden dataset para detectar desviaciones de razonamiento y alucinaciones",
            "Habilitar prompt versioning y A/B testing del agente; medir la tasa de alucinacion siguiendo la consistencia de respuestas entre versiones y revisando las desviaciones frente a respuestas esperadas",
        ],
        correct=2,
        key="aip01-q52",
        answer=(
            '<div class="verdict">Correcta: {{L}} - habilitar PreProcessingTrace, OrchestrationTrace y PostProcessingTrace + golden dataset.</div>'
            '<p><b>El problema:</b> exponer el <b>flujo interno de razonamiento</b> del agente (no solo la salida) para diagnosticar y reducir alucinaciones y validar el comportamiento.</p>'
            '<p><b>Por que la respuesta sirve:</b> las <b>traces</b> del agente de Bedrock (<b>PreProcessing</b>, <b>Orchestration</b>, <b>PostProcessing</b>) revelan como interpreta el prompt, como orquesta los pasos y como forma la respuesta final. Validarlas de forma continua contra un <b>golden dataset</b> detecta desviaciones de razonamiento y alucinaciones a lo largo del tiempo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Invocation logs + muestreo:</b> solo monitorea a nivel de salida y tendencias; no expone el flujo de razonamiento interno, asi que no valida como el agente interpreta prompts u orquesta pasos.</li>'
            '<li><b>GuardrailTrace + RoutingClassifierTrace:</b> exponen seguridad/compliance y enrutamiento, pero no la ruta completa de razonamiento, dejando huecos en la interpretabilidad de extremo a extremo.</li>'
            '<li><b>Prompt versioning + A/B testing:</b> compara salidas finales entre prompts/modelos, pero no expone las etapas internas necesarias para diagnosticar y reducir alucinaciones.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Ver el razonamiento interno del agente (no solo la salida): PreProcessing/Orchestration/PostProcessing traces + golden dataset. Los invocation logs y el A/B solo miran la salida final.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents-trace.html">docs.aws traces de agentes de Bedrock</a></div>'
        ),
    ),
    # ============================================================
    # Q53 - Transfer learning BERT (reemplazar capa final)
    # ============================================================
    card(
        question="Un equipo quiere aplicar <b>transfer learning</b> con un modelo <b>BERT preentrenado</b> para clasificar correos como spam/no spam, usando varios miles de correos etiquetados en SageMaker AI, sin reentrenar todo desde cero. ¿Que enfoque <b>inicializa correctamente</b> el modelo BERT para lograrlo?",
        options=[
            "Cargar los pesos preentrenados de cada capa y colocar un clasificador externo encima del vector de salida del modelo primario; entrenar el nuevo clasificador con el dataset etiquetado",
            "Aplicar los parametros preentrenados en todas las capas, luego descartar la capa final existente, introducir un clasificador personalizado y entrenarlo con los datos etiquetados para deteccion de spam",
            "Usar los pesos preentrenados en todas las capas transformer y adjuntar un segundo clasificador en paralelo a la capa de salida existente; entrenar solo ese clasificador adicional con el dataset etiquetado",
            "Inicializar el modelo con pesos preentrenados, convertir la capa de salida en un clasificador multitarea que prediga varias clases de texto ademas de spam, y entrenar ese clasificador con el dataset etiquetado",
        ],
        correct=1,
        key="aip01-q53",
        answer=(
            '<div class="verdict">Correcta: {{L}} - reutilizar todas las capas, descartar la capa final y entrenar un clasificador nuevo.</div>'
            '<p><b>El problema:</b> hacer transfer learning con BERT: aprovechar el conocimiento preentrenado pero adaptar la salida a la tarea nueva (clasificacion binaria spam/no spam).</p>'
            '<p><b>Por que la respuesta sirve:</b> el patron correcto es cargar los pesos preentrenados en <b>todas las capas</b> (que capturan el lenguaje), <b>descartar la capa final</b> original (entrenada para otra tarea) e introducir un <b>clasificador nuevo</b> alineado a spam/no spam, entrenandolo con los datos etiquetados. Asi el modelo se adapta a la tarea sin reentrenar desde cero.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Clasificador externo encima sin reemplazar la capa final:</b> apilar una capa sin quitar la salida original deja una capa entrenada para otra tarea, generando desalineacion entre las representaciones y la clasificacion nueva, y reduce la eficacia del fine-tuning.</li>'
            '<li><b>Segundo clasificador en paralelo a la salida:</b> introduce decisiones en conflicto (multiples salidas simultaneas), causa ambiguedad y complica la optimizacion, degradando el rendimiento.</li>'
            '<li><b>Convertir la salida en multitarea:</b> el multi-task añade complejidad innecesaria para una tarea binaria, encareciendo y complicando el entrenamiento sin aportar valor a la deteccion de spam.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Transfer learning: conservar los pesos preentrenados, reemplazar la capa de salida por una nueva acorde a la tarea y entrenar esa cabeza. Apilar o duplicar clasificadores desalinea el modelo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-fine-tune.html">docs.aws fine-tuning y transfer learning</a></div>'
        ),
    ),
    # ============================================================
    # Q54 - Bedrock Data Automation (BDA) multimedia
    # ============================================================
    card(
        question="Una editorial gestiona <b>PDFs, imagenes, audio y video</b> y quiere un asistente de investigacion generativo que responda consultas en lenguaje natural (por ejemplo, que articulo menciono cierto tema e incluyo imagenes aereas). Planea usar <b>Amazon Bedrock Data Automation (BDA)</b> para procesar el contenido no estructurado y <b>SageMaker AI</b> para hospedar el modelo generativo. ¿Que enfoque cumple mejor?",
        options=[
            "Usar BDA para procesar los archivos, guardar el contenido crudo en Amazon S3 y desplegar una Lambda que cree tu propia base de datos de vectores fuera de Bedrock Knowledge Bases antes de pasarla a SageMaker AI",
            "Aprovechar BDA para procesar documentos, imagenes, audio y video, indexar los resultados en Bedrock Knowledge Bases para busqueda semantica y luego pasar el contexto recuperado a un foundation model via SageMaker AI para generar la respuesta",
            "Usar BDA para procesar los archivos, analizar el contenido estructurado con Amazon Comprehend para entidades y sentimiento, y luego enviar los resultados a un foundation model hospedado en Amazon EC2 para generar respuestas",
            "Emplear BDA para procesar todos los tipos de medios y alimentar directamente la salida estructurada a un foundation model via SageMaker AI, omitiendo el uso de una knowledge base",
        ],
        correct=1,
        key="aip01-q54",
        answer=(
            '<div class="verdict">Correcta: {{L}} - BDA + indexar en Knowledge Bases + generar via SageMaker AI.</div>'
            '<p><b>El problema:</b> procesar multimedia heterogeneo y montar un RAG que recupere contexto por busqueda semantica para generar respuestas.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Data Automation (BDA)</b> procesa documentos, imagenes, audio y video y extrae insights estructurados. Indexarlos en <b>Bedrock Knowledge Bases</b> habilita la busqueda semantica (recuperacion optimizada), y el contexto recuperado alimenta al foundation model via SageMaker AI para la respuesta. Es el flujo RAG completo y gestionado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>BDA + S3 + vector DB propia con Lambda:</b> crear un vector store custom fuera de Knowledge Bases añade complejidad y pasos manuales; Knowledge Bases ya indexa y hace busqueda semantica de forma optimizada.</li>'
            '<li><b>BDA + Comprehend + FM en EC2:</b> hospedar el FM en EC2 en vez de SageMaker AI suma overhead operativo (provisionar, escalar, mantener); SageMaker AI es el entorno gestionado recomendado.</li>'
            '<li><b>BDA directo al FM sin knowledge base:</b> omitir la KB elimina el indexado y la busqueda semantica, clave para recuperar contexto relevante; sin ella las respuestas son menos precisas o mas lentas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG sobre multimedia (docs/imagenes/audio/video): BDA para procesar + Knowledge Bases para indexar/buscar + FM para generar. No reinventes el vector store ni omitas la KB.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html">docs.aws Bedrock Data Automation</a></div>'
        ),
    ),
    # ============================================================
    # Q55 - AppConfig routing dinamico de FMs + failover
    # ============================================================
    card(
        question="Una app GenAI enruta cada tarea (traduccion, recomendaciones, descripciones) a un FM distinto. Debe: <b>dirigir la inferencia al FM correcto</b> segun tarea y configuracion del cliente, <b>cambiar el enrutamiento en runtime sin redeploy</b>, optimizar latencia/fiabilidad y operacion cross-Region, e implementar <b>failover</b> a un modelo o Region de respaldo. ¿Que enfoque cumple con el menor esfuerzo operativo?",
        options=[
            "Montar un router en Flask sobre Amazon ECS con datos de enrutamiento en Amazon Aurora; enrutar via API Gateway al Flask que selecciona e invoca el modelo con el SDK de Bedrock; usar alarmas de CloudWatch para monitorear errores y actualizar la tabla de enrutamiento",
            "Configurar API Gateway para enrutar a una Lambda por tipo de tarea, guardar las configuraciones de modelo en Amazon S3, habilitar retry con backoff exponencial en la Lambda para las llamadas a Bedrock y usar Amazon Route 53 para failover regional; actualizar el enrutamiento modificando el archivo de S3 y redesplegando la Lambda",
            "Crear una Lambda con la extension AppConfig Agent para obtener dinamicamente las reglas de enrutamiento desde AWS AppConfig; usar AWS Step Functions para gestionar los workflows por tarea con una estrategia de failover con circuit breaker; invocar los modelos usando endpoints regionales de Bedrock, reintentando en una Region secundaria si falla",
            "Desplegar un router de Kubernetes en Amazon EKS con ConfigMaps para las reglas; reenviar de API Gateway a un Ingress controller que envie al router, que invoca el FM con el SDK de Bedrock; gestionar el failover actualizando ConfigMaps y reiniciando Pods cuando falla una Region o modelo",
        ],
        correct=2,
        key="aip01-q55",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AppConfig para reglas dinamicas + Step Functions con circuit breaker + endpoints regionales de Bedrock.</div>'
            '<p><b>El problema:</b> enrutar por tarea/cliente, poder <b>cambiar el enrutamiento en runtime sin redeploy</b>, con failover cross-Region y minimo overhead.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>AWS AppConfig</b> sirve reglas de enrutamiento que se actualizan <b>en runtime sin redesplegar</b> (la extension AppConfig Agent las obtiene dinamicamente). <b>Step Functions</b> orquesta los flujos por tarea con una estrategia de failover con <b>circuit breaker</b>, y usar <b>endpoints regionales de Bedrock</b> con reintento en una Region secundaria da el failover cross-Region. Todo gestionado, con poco overhead.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Flask en ECS + Aurora + alarmas:</b> ECS exige gestionar cluster, parcheo y escalado (mas overhead); Aurora no es para configuracion que cambia rapido y las alarmas de CloudWatch no actualizan el enrutamiento en runtime por si solas, ni dan failover nativo cross-Region.</li>'
            '<li><b>API Gateway + Lambda + config en S3 + Route 53:</b> S3 no es para configuracion dinamica en tiempo real y actualizar por redeploy incumple el cambio en runtime; Route 53 hace failover de DNS pero no enrutamiento de modelo por peticion.</li>'
            '<li><b>Router en EKS con ConfigMaps:</b> los ConfigMaps suelen requerir reiniciar Pods para aplicar cambios (no hay update en runtime), EKS añade gestion de cluster y no da failover nativo cross-Region para invocaciones de Bedrock.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cambiar el enrutamiento en runtime sin redeploy: un servicio de configuracion dinamica gestionado. Orquestacion + failover: un orquestador de workflows con circuit breaker + endpoints regionales de Bedrock. S3/ConfigMaps implican redeploy o reinicio.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html">docs.aws AWS AppConfig</a></div>'
        ),
    ),
    # ============================================================
    # Q57 - LoRA adapters como inference components
    # ============================================================
    card(
        question="Un asistente tiene un <b>modelo base grande</b> desplegado como endpoint real-time de SageMaker AI. Se quiere <b>personalizarlo para cinco mercados</b> con <b>adaptadores LoRA</b> (adaptacion parameter-efficient) en lugar de reentrenar todo el modelo, manteniendo el base sin cambios e <b>invocando dinamicamente el adaptador correcto</b> en inferencia, <b>sin crear endpoints separados</b> por region. ¿Que solucion cumple?",
        options=[
            "Desplegar el modelo base una vez en un endpoint real-time de SageMaker AI y, por cada region, usar un inference component de adaptador que contenga los artefactos LoRA de esa region, invocando el mismo endpoint y especificando el adaptador de la region",
            "Aprovisionar un multi-model endpoint grande, cargar el adaptador LoRA de cada region como un artefacto de modelo separado y apoyarse en logica de enrutamiento a nivel de contenedor para seleccionar el adaptador en inferencia",
            "Desplegar el modelo base una vez en un endpoint real-time y guardar los pesos LoRA de cada region en Amazon EFS, montando el filesystem para adjuntar dinamicamente el adaptador correcto en inferencia",
            "Hospedar el modelo base en un endpoint real-time y usar una capa de pre-procesamiento en AWS Lambda que recupere los pesos del adaptador de cada region y los inyecte en el contenedor del modelo antes de reenviar la peticion",
        ],
        correct=0,
        key="aip01-q57",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un inference component de adaptador LoRA por region sobre el mismo endpoint.</div>'
            '<p><b>El problema:</b> servir varios adaptadores LoRA sobre un unico modelo base en el mismo endpoint, invocando el adaptador correcto por region sin endpoints separados ni reentrenar el base.</p>'
            '<p><b>Por que la respuesta sirve:</b> SageMaker AI soporta <b>adapter inference components</b>: se despliega el modelo base una vez y cada region tiene un <b>inference component</b> con sus artefactos <b>LoRA</b>. Se invoca el mismo endpoint especificando el adaptador de la region, con seleccion dinamica, ligera y nativa, sin duplicar el modelo base.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Multi-model endpoint con cada LoRA como modelo:</b> los MME alojan modelos independientes, no overlays de adaptador; los LoRA no son modelos autonomos (requieren el base), asi que complica el enrutamiento y eleva el consumo de recursos.</li>'
            '<li><b>Pesos LoRA en EFS montado:</b> SageMaker AI no soporta de forma nativa el cambio dinamico de adaptadores via montaje EFS en real-time; añade complejidad, latencia y riesgos de teardown, sin las optimizaciones de los adapter inference components.</li>'
            '<li><b>Lambda que inyecta pesos en el contenedor:</b> los contenedores de modelo de SageMaker son inmutables una vez desplegados; no se pueden inyectar pesos nuevos en un contenedor en ejecucion, y no esta soportado por la arquitectura real-time.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Muchos adaptadores LoRA sobre un base, mismo endpoint, seleccion dinamica: adapter inference components de SageMaker. Los LoRA no son modelos independientes (no van en un MME); el contenedor es inmutable.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/inference-components.html">docs.aws inference components</a></div>'
        ),
    ),
    # ============================================================
    # Q61 - LangChain/LangGraph para orquestacion RAG con estado
    # ============================================================
    card(
        question="Un asistente de asesoria de inversion necesita un framework que gestione el <b>ciclo RAG completo</b>, orqueste <b>workflows de agente con ejecucion en grafo</b>, mantenga <b>estado durable</b> y permita <b>rollback y replay controlados</b> en un entorno regulado (con memoria de largo plazo del cliente versionada para auditoria). Ya usa SageMaker Feature Store, MLflow y FMs de Bedrock. ¿Que framework es el mas adecuado?",
        options=[
            "Usar Amazon Kendra para busqueda semantica y AWS Glue DataBrew para preprocesar documentos, con el estado de memoria en Amazon ElastiCache for Redis",
            "Usar LangChain para implementar el pipeline RAG y LangGraph para crear el agente con estado persistente, orquestacion basada en grafo y ejecucion con checkpoints",
            "Usar SageMaker Pipelines para los workflows de recuperacion y Amazon EventBridge Pipes para gestionar las transiciones de estado del agente y las actualizaciones de memoria",
            "Usar AWS Step Functions para la orquestacion multi-paso y Amazon OpenSearch Serverless como vector store para embeddings, con Map states de Step Functions para simular la memoria del agente",
        ],
        correct=1,
        key="aip01-q61",
        answer=(
            '<div class="verdict">Correcta: {{L}} - LangChain (RAG) + LangGraph (agente con estado, grafo y checkpoints).</div>'
            '<p><b>El problema:</b> un framework que cubra el ciclo RAG y ademas orqueste al agente en grafo con estado durable y capacidad de rollback/replay para auditoria en un entorno regulado.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>LangChain</b> implementa el pipeline RAG (recuperacion + generacion), y <b>LangGraph</b> modela al agente como un <b>grafo</b> de ejecucion con <b>estado persistente</b> y <b>checkpoints</b>, habilitando rollback y replay controlados. Es el unico de las opciones que aporta razonamiento de agente con memoria durable, versionada y reproducible.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Kendra + Glue DataBrew + Redis:</b> Kendra no implementa RAG por embeddings ni orquesta inferencia de Bedrock, DataBrew es prep de datos low-code y Redis no da memoria de agente durable, versionada ni reproducible.</li>'
            '<li><b>SageMaker Pipelines + EventBridge Pipes:</b> Pipelines automatiza workflows de ML (training), no recuperacion RAG ni razonamiento de agente; EventBridge Pipes rutea eventos pero no mantiene estado persistente, memoria reproducible ni ejecucion estructurada del agente.</li>'
            '<li><b>Step Functions + OpenSearch Serverless (Map states):</b> Step Functions orquesta y OpenSearch guarda embeddings, pero los Map states solo simulan memoria: no dan estado durable versionado con rollback/replay, requisito de compliance del escenario.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Agente con estado durable, grafo de ejecucion y rollback/replay sobre recuperacion aumentada: un framework de orquestacion de agentes con checkpoints. Step Functions/Redis solo simulan memoria; SageMaker Pipelines es para ML training.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html">docs.aws agentes y orquestacion en Bedrock</a></div>'
        ),
    ),
    # ============================================================
    # Q64 - Bedrock Prompt Management (plantillas versionadas)
    # ============================================================
    card(
        question="Un asistente de salud usa Amazon Kendra (busqueda) y un FM en Amazon Bedrock. La organizacion requiere <b>plantillas de prompt estandarizadas, versionadas y reutilizables</b> entre flujos clinicos, y que parametros como <b>temperature y max_tokens sean ajustables</b> segun la complejidad de la consulta. ¿Que solucion es la mas apropiada para gestionar las plantillas de prompt?",
        options=[
            "Usar Bedrock Prompt Management para guardar plantillas reutilizables y versionadas, definir parametros de inferencia ajustables dentro de la configuracion del prompt e invocar el prompt via la InvokeModel API tras inyectar los resultados de Kendra",
            "Incrustar el prompt completo y los parametros de inferencia directamente en una Lambda que hace las busquedas en Kendra y llama a la API de Bedrock; actualizar el codigo de la Lambda cada vez que cambien el texto o la configuracion en los distintos flujos",
            "Subir archivos de texto de prompt a un bucket de Amazon S3, que la Lambda lea e interprete las preguntas del paciente y los resultados de Kendra, y enviar el archivo a Bedrock con CreateModelCustomizationJob para reutilizar los prompts",
            "Crear un pipeline multi-paso de Bedrock Prompt Flows que encadene varios prompts y modelos, enrutando las consultas del paciente por pasos separados para la fase de busqueda y la de generacion de respuesta",
        ],
        correct=0,
        key="aip01-q64",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Prompt Management para plantillas versionadas y parametros ajustables.</div>'
            '<p><b>El problema:</b> gestionar plantillas de prompt estandarizadas, reutilizables y versionadas entre flujos, con parametros de inferencia (temperature, max_tokens) ajustables.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Bedrock Prompt Management</b> almacena plantillas <b>reutilizables y versionadas</b> con variables y permite definir <b>parametros de inferencia</b> dentro de la configuracion del prompt. Se invoca via <b>InvokeModel</b> tras inyectar los resultados de Kendra, dando gobierno centralizado y colaboracion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Prompt incrustado en la Lambda:</b> acopla la logica; cualquier cambio de texto o parametro exige actualizar codigo, redesplegar y probar, sin versionado ni reutilizacion centralizada entre equipos.</li>'
            '<li><b>Archivos en S3 + CreateModelCustomizationJob:</b> ese job es para fine-tuning/pretraining, no para inferencia ni reutilizar plantillas; añade costo y complejidad y no da versionado ni configuracion de parametros como Prompt Management.</li>'
            '<li><b>Bedrock Prompt Flows:</b> orquesta flujos multi-paso, pero sin Prompt Management no satisface la necesidad de plantillas estandarizadas, reutilizables y versionadas; usarlo solo fragmenta las definiciones de prompt.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Plantillas de prompt reutilizables, versionadas y con parametros: el servicio nativo de gestion de prompts de Bedrock. Prompt Flows orquesta pasos (no versiona plantillas); CreateModelCustomizationJob es fine-tuning.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html">docs.aws Bedrock Prompt Management</a></div>'
        ),
    ),
    # ============================================================
    # Q65 - Bedrock provisioned model ARN en modelId
    # ============================================================
    card(
        question="Una empresa compro Provisioned Throughput en Bedrock con CreateProvisionedModelThroughput, pero CloudWatch muestra el modelo provisionado <b>casi sin uso</b> mientras las peticiones <b>siguen con throttling</b>. La app aun pasa el <b>identificador del foundation model base</b> en el campo modelId. Debe hacer que todas las peticiones consuman la capacidad provisionada <b>sin cambiar prompts ni payloads</b>. ¿Que cambio de configuracion cumple?",
        options=[
            "Aumentar el numero de model units asignados al Provisioned Throughput existente y seguir usando el ID del modelo base en el parametro modelId",
            "Usar el nombre del modelo provisionado devuelto durante la creacion como modelId en la peticion del runtime de Bedrock, manteniendo el payload de inferencia sin cambios",
            "Actualizar el parametro modelId para usar el ARN del modelo provisionado devuelto por la API CreateProvisionedModelThroughput",
            "Configurar la aplicacion para usar un inference profile cross-Region del foundation model y conservar el ID del modelo base como fallback cuando ocurra throttling",
        ],
        correct=2,
        key="aip01-q65",
        answer=(
            '<div class="verdict">Correcta: {{L}} - usar el ARN del modelo provisionado como modelId.</div>'
            '<p><b>El problema:</b> las peticiones no consumen la capacidad comprada porque siguen apuntando al modelo base; hay que enrutarlas al recurso provisionado sin tocar prompts ni payloads.</p>'
            '<p><b>Por que la respuesta sirve:</b> el Provisioned Throughput es un recurso con su propio identificador. Al poner el <b>ARN del modelo provisionado</b> (devuelto por CreateProvisionedModelThroughput) en <b>modelId</b>, Bedrock enruta la inferencia a la capacidad dedicada, eliminando el throttling. Solo cambia el identificador; el payload queda igual.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Aumentar model units con el ID base:</b> agregar unidades solo amplia la capacidad del recurso provisionado; las peticiones que siguen referenciando el modelo base no la usan, asi que no resuelve el enrutamiento.</li>'
            '<li><b>Usar el nombre del modelo provisionado:</b> el identificador que el runtime de Bedrock espera para dirigir la inferencia al recurso provisionado es el ARN, no un nombre; pasar un nombre no enruta correctamente a la capacidad comprada.</li>'
            '<li><b>Inference profile cross-Region con fallback al base:</b> es otro mecanismo de enrutamiento y no hace que las peticiones consuman el Provisioned Throughput ya comprado; hay que invocar explicitamente el recurso por su ARN.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Consumir el throughput reservado ya comprado: pasar el identificador de recurso del modelo provisionado en modelId. Subir units o usar el ID del modelo base no enruta a la capacidad; cross-Region no la consume.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html">docs.aws Provisioned Throughput</a></div>'
        ),
    ),
    # ============================================================
    # Q66 - Bedrock Guardrails (denied topics, PII, filtros)
    # ============================================================
    card(
        question="Un asistente de salud en Amazon Bedrock <b>nunca debe discutir diagnosticos medicos</b>, debe <b>bloquear contenido daniño</b>, <b>enmascarar PII</b>, preservar <b>auditoria</b> y filtrar <b>entrada y salida</b> segun sensibilidad, con <b>minimos falsos positivos</b> y <b>estrategias de manejo distintas</b> segun el tipo de contenido. ¿Que configuracion de guardrails cumple?",
        options=[
            "Construir un guardrail y subir cada categoria de Content Filters al maximo; agregar diagnosticos medicos como denied topic con frases de ejemplo que disparen bloqueo; configurar Sensitive Information Filters para bloquear por completo todo tipo de PII detectado; adjuntarlo a cada peticion de inferencia",
            "Usar Amazon Comprehend para detectar la PII en los mensajes del paciente antes de que lleguen a Bedrock y Amazon Macie para escanear los logs de conversacion almacenados; aplicar ademas un solo guardrail con Content Filters en alto unicamente para contenido daniño, sin abordar el topic de diagnosticos medicos",
            "Fijar la fuerza de Content Filters en medio para contenido daniño; agregar diagnosticos medicos como denied topic con definicion clara y frases de ejemplo; configurar Sensitive Information Filters para enmascarar PII en las respuestas y bloquear detalles de seguros en las entradas; activar la evaluacion de entrada y salida con mensajes de bloqueo personalizados para auditoria",
            "Construir tres guardrails separados (uno para contenido daniño, otro para el topic de diagnostico medico y otro para bloqueo de PII) y conectarlos en orden con un workflow de AWS Step Functions que enrute cada mensaje segun su clasificacion",
        ],
        correct=2,
        key="aip01-q66",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un guardrail con filtros en medio, denied topic, PII enmascarada/bloqueada segun caso y evaluacion in/out.</div>'
            '<p><b>El problema:</b> aplicar politicas variadas (denied topics, contenido daniño, PII con distinto trato) en entrada y salida, con minimos falsos positivos y auditoria.</p>'
            '<p><b>Por que la respuesta sirve:</b> un <b>unico guardrail</b> bien configurado combina Content Filters en fuerza <b>media</b> (equilibra deteccion y falsos positivos), un <b>denied topic</b> para diagnosticos medicos con definicion y ejemplos, y <b>Sensitive Information Filters</b> con manejo diferenciado (enmascarar PII en respuestas, bloquear seguros en entradas). Activar evaluacion de <b>entrada y salida</b> con mensajes de bloqueo personalizados cubre el logging de auditoria.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Todo al maximo y bloquear toda PII:</b> subir cada filtro al maximo dispara falsos positivos (contra el requisito) y bloquear todo tipo de PII no ofrece las estrategias diferenciadas pedidas (enmascarar lo menos critico vs bloquear lo de mayor riesgo).</li>'
            '<li><b>Comprehend + Macie + un guardrail solo para daniño:</b> mover la deteccion de PII fuera de Guardrails obliga a integracion custom; Macie escanea datos en S3, no entradas/salidas conversacionales en tiempo real, y no aborda el denied topic de diagnosticos.</li>'
            '<li><b>Tres guardrails encadenados con Step Functions:</b> fragmentar las protecciones añade complejidad, orquestacion y puntos de fallo cuando un unico guardrail ya combina filtros, denied topics y PII; ademas no minimiza falsos positivos ni evita logica custom.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Politicas mixtas con pocos falsos positivos: UN guardrail con Content Filters moderados, denied topics, y PII con manejo diferenciado (mask vs block) + evaluacion de entrada y salida. Nada de encadenar varios guardrails.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-components.html">docs.aws componentes de Guardrails</a></div>'
        ),
    ),
    # ============================================================
    # Q71 - Bedrock AgentCore Observability (traces FM)
    # ============================================================
    card(
        question="Una app integra un FM de Bedrock y sufre fallos intermitentes de invocacion, salidas malformadas y recomendaciones inconsistentes con las mismas entradas. CloudWatch Logs registra errores 400 y 500, pero sin metadatos suficientes para aislar las llamadas fallidas. Se necesita <b>observabilidad granular de toda la ruta de invocacion</b>: inspeccion request-response, tracing detallado y diagnosticos accionables. ¿Que solucion cumple?",
        options=[
            "Usar Amazon SageMaker Inference Recommender para analizar perfiles de rendimiento del endpoint, evaluar patrones de throughput e identificar desajustes de configuracion que afecten el comportamiento upstream de la API",
            "Implementar AWS Step Functions Distributed Map para orquestar reprocesamiento a gran escala, consolidar logs de diagnostico y analizar fallos repetidos entre lotes de ejecucion",
            "Habilitar Bedrock AgentCore Observability para generar invocation traces, capturar registros estructurados de request-response y exponer errores de integracion del FM para flujos de troubleshooting detallado",
            "Configurar metricas de invocacion de Bedrock con logica de retry mejorada para analizar latencia de invocacion, monitorear eventos de throttling e identificar anomalias a nivel de respuesta",
        ],
        correct=2,
        key="aip01-q71",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock AgentCore Observability (invocation traces).</div>'
            '<p><b>El problema:</b> aislar fallos de integracion del FM con visibilidad granular de la ruta de invocacion: inspeccion request-response y tracing detallado, algo que los logs de alto nivel no dan.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>AgentCore Observability</b> genera <b>invocation traces</b> y captura registros <b>estructurados de request-response</b>, exponiendo errores de integracion del FM. Eso permite inspeccionar payloads (detectar los malformados) y trazar cada llamada, entregando diagnosticos accionables.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SageMaker Inference Recommender:</b> ayuda a elegir la configuracion de despliegue de endpoints de SageMaker; no captura traces ni inspecciona payloads malformados enviados a un FM de Bedrock.</li>'
            '<li><b>Step Functions Distributed Map:</b> es para procesamiento paralelo masivo; puede reprocesar a escala, pero no inspecciona la estructura request-response del FM ni traza rutas de invocacion individuales.</li>'
            '<li><b>Metricas de invocacion + retry:</b> ofrecen telemetria de alto nivel (latencia, throttling, tasas de error) pero sin contexto de debugging ni inspeccion a nivel de payload; insuficiente para identificar payloads malformados o errores profundos de integracion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Tracing granular request-response de invocaciones del modelo: la capa de observabilidad de agentes de Bedrock (invocation traces). Las metricas de invocacion solo dan telemetria de alto nivel; Inference Recommender y Distributed Map no trazan la ruta de invocacion.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html">docs.aws AgentCore Observability</a></div>'
        ),
    ),
    # ============================================================
    # Q2 - CloudWatch Application Insights + anomaly detection (observabilidad FM)
    # ============================================================
    card(
        question="Una plataforma de recomendaciones de viaje corre en Amazon EC2 y llama a foundation models de Amazon Bedrock. A veces hay <b>recomendaciones de peor calidad</b>, <b>aumentos inesperados de consumo de tokens</b> y <b>respuestas mas lentas</b> para ciertos tipos de viaje y segmentos de cliente. Se necesita observabilidad <b>centralizada</b> que <b>correlacione la salud de la aplicacion con el comportamiento del modelo</b>, <b>detecte desviaciones respecto a patrones de desempeño establecidos</b> y <b>analice logs</b> para hallar causas recurrentes, con el <b>MENOR esfuerzo operativo</b>. ¿Que enfoque cumple?",
        options=[
            "Configurar Amazon CloudWatch Application Insights para monitorear los recursos de la aplicacion, publicar metricas personalizadas de calidad de recomendacion, consumo de tokens y latencia con embedded metric format segmentadas por tipo de peticion y grupo de usuario, aplicar CloudWatch anomaly detection a las metricas del modelo y usar CloudWatch Logs Insights para identificar patrones recurrentes",
            "Habilitar el logging de invocacion de modelos de Bedrock hacia Amazon CloudWatch Logs, crear metric filters para uso de tokens y latencia de respuesta segmentados por tipo de peticion, configurar alarmas estaticas de CloudWatch con umbrales fijos predefinidos por tipo de viaje y segmento, y construir dashboards para revisar manualmente las desviaciones de calidad cuando se disparen esas alarmas",
            "Instalar el agente de Amazon CloudWatch en las instancias EC2 para recolectar CPU, memoria, disco y logs de aplicacion, crear dashboards de esas metricas de infraestructura por instancia y segmento, definir alarmas de host y revisar manualmente la latencia de la API de Bedrock y la calidad de las recomendaciones cada vez que la salida se degrade",
            "Habilitar tracing con AWS X-Ray para la aplicacion y las llamadas a la API de Bedrock, usar las trazas para identificar peticiones lentas por tipo de viaje y segmento, publicar la latencia promedio y percentiles en Amazon CloudWatch, y configurar alarmas para peticiones que superen umbrales fijos de tiempo de respuesta predefinidos manualmente",
        ],
        correct=0,
        key="aip01-q2",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Application Insights + metricas personalizadas (EMF) + anomaly detection + Logs Insights.</div>'
            '<p><b>El problema:</b> observar de forma centralizada la salud de la app junto con el comportamiento del modelo (calidad, tokens, latencia), detectar desviaciones frente a un patron normal aprendido y analizar logs para causas recurrentes, con la menor operacion.</p>'
            '<p><b>Por que la respuesta sirve:</b> las <b>metricas personalizadas</b> (calidad de recomendacion, tokens, latencia) publicadas con <b>embedded metric format (EMF)</b> y <b>segmentadas</b> por tipo de peticion y grupo de usuario permiten correlacionar la degradacion con caracteristicas concretas de la carga. <b>CloudWatch anomaly detection</b> aprende una linea base (banda de comportamiento normal) y alerta ante desviaciones sin umbrales fijos. <b>CloudWatch Logs Insights</b> consulta los logs para hallar patrones recurrentes. <b>Application Insights</b> ata la observabilidad de los recursos de la aplicacion. Todo son capacidades gestionadas de CloudWatch, sin construir infraestructura propia.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Logging + metric filters + alarmas estaticas:</b> las alarmas estaticas comparan contra umbrales fijos, no se adaptan al patron historico; ademas no crea una metrica de calidad segmentada por tipo de peticion y usuario, asi que no detecta desviaciones respecto a una linea base como si lo hace anomaly detection.</li>'
            '<li><b>Agente de CloudWatch (CPU/memoria/disco):</b> da visibilidad de host e infraestructura; CPU, memoria y disco no miden calidad de recomendacion ni consumo de tokens, y la revision manual no cumple la deteccion automatica de comportamiento anomalo del modelo.</li>'
            '<li><b>X-Ray tracing:</b> se enfoca en rutas de peticion y latencia, no en metricas multidimensionales de negocio y calidad del modelo; ademas usa umbrales fijos de latencia y no aporta linea base adaptativa ni analisis de patrones en logs.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Detectar desviaciones frente a lo normal sin fijar numeros a mano: deteccion de anomalias sobre metricas (linea base aprendida), no alarmas de umbral fijo. Metricas de negocio segmentadas se publican con embedded metric format; los logs se analizan con la herramienta de consultas de logs.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html">docs.aws CloudWatch anomaly detection</a> '
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html">docs.aws embedded metric format</a></div>'
        ),
    ),
    # ============================================================
    # Q59 - Parametros de inferencia: bajar temperature y top_k (determinismo)
    # ============================================================
    card(
        question="Un chatbot de soporte usa Amazon Bedrock con un LLM Amazon Nova Pro y adjunta al prompt articulos recuperados con Amazon Kendra. Los usuarios reportan que ante <b>preguntas similares repetidas</b> a veces se devuelven <b>respuestas distintas</b>, aunque los resultados de Kendra <b>no cambien</b>. El desarrollador debe lograr respuestas <b>mas consistentes, deterministas y menos aleatorias</b>, <b>sin modificar el proceso de recuperacion de conocimiento</b>. ¿Que enfoque lo resuelve?",
        options=[
            "Ajustar los parametros de inferencia bajando tanto el valor de temperature como el umbral de muestreo top_k para reducir la aleatoriedad de la eleccion de tokens",
            "Ajustar los parametros de inferencia subiendo tanto el valor de temperature como el umbral de muestreo top_k para ampliar la diversidad de la eleccion de tokens",
            "Ajustar los parametros de inferencia bajando el valor de temperature y subiendo el umbral de muestreo top_p para admitir mas candidatos de tokens por nucleo",
            "Ajustar los parametros de inferencia bajando tanto el valor de temperature como el umbral de muestreo top_p para acotar la probabilidad acumulada de tokens",
        ],
        correct=0,
        key="aip01-q59",
        answer=(
            '<div class="verdict">Correcta: {{L}} - bajar temperature y bajar top_k.</div>'
            '<p><b>El problema:</b> el mismo prompt (con el mismo contexto de Kendra) produce respuestas variables. Hay que reducir la aleatoriedad del muestreo del modelo para que sea mas determinista, tocando solo los parametros de inferencia.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>temperature</b> escala cuanta aleatoriedad hay al elegir el siguiente token; bajarla concentra la probabilidad en los tokens mas probables (mas determinista). <b>top_k</b> limita el muestreo a los K tokens mas probables; bajarlo reduce el conjunto de candidatos, forzando salidas mas enfocadas y repetibles. Bajar <b>ambos</b> minimiza la variabilidad sin tocar la recuperacion de Kendra.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Subir temperature y top_k:</b> hace lo contrario: mas temperature aumenta la variabilidad y mas top_k amplia el conjunto de candidatos, con lo que las respuestas serian menos predecibles.</li>'
            '<li><b>Bajar temperature y subir top_p:</b> bajar temperature ayuda, pero subir top_p (muestreo por nucleo) amplia la masa de probabilidad admitida y permite mas tokens diversos, contrarrestando el determinismo buscado.</li>'
            '<li><b>Bajar temperature y bajar top_p:</b> reduce aleatoriedad, pero limitar por top_p (umbral de probabilidad acumulada) acota los candidatos de forma menos directa que limitar por conteo; para respuestas enfocadas y consistentes, restringir por numero de candidatos es mas efectivo aqui.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Mas determinismo = menos aleatoriedad de muestreo: baja la temperatura y estrecha el conjunto de candidatos. temperature controla que tan aleatoria es la eleccion; top_k limita por numero de tokens candidatos; top_p limita por probabilidad acumulada (nucleo).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/inference-parameters.html">docs.aws parametros de inferencia de Bedrock</a></div>'
        ),
    ),
    # ============================================================
    # RESCATADAS (auditoria falsos-COVERED). Prefijo de key aip01r-.
    # Enfasis en el detalle AVANZADO/feature especifica de cada pregunta.
    # ============================================================
    # ------------------------------------------------------------
    # Q16r - Titan Embeddings + OpenSearch, con SHARDING para escalar
    # ------------------------------------------------------------
    card(
        question="Una editorial multinacional construye un asistente interno con agentes de Amazon Bedrock para recuperar, resumir y analizar documentos de investigacion, apoyandose en RAG. Necesita representar consultas y contenido como <b>embeddings semanticos</b>, con una solucion gestionada y escalable. Dado el <b>gran volumen de documentos</b>, tambien debe optimizar el rendimiento con una <b>estrategia de distribucion de datos y manejo de consultas</b>. ¿Que enfoque cumple mejor?",
        options=[
            "Implementar Amazon Kendra para indexar los documentos, dar soporte a consultas en lenguaje natural y que los agentes recuperen resultados mediante la busqueda semantica y el ranking gestionados del servicio, ajustando relevancia y facetas para escalar el volumen de consultas",
            "Desplegar SageMaker JumpStart para hacer fine-tuning y hospedar un modelo de lenguaje preentrenado de resumen y generacion, integrarlo con los agentes para el descubrimiento de contenido y replicar el endpoint en varios nodos para distribuir la carga de consultas",
            "Usar Amazon Titan Text Embeddings en Bedrock para convertir texto en vectores semanticos y almacenarlos en Amazon OpenSearch Service; aplicar una estrategia de sharding para distribuir el indice vectorial entre nodos y lograr consultas paralelas y escalabilidad horizontal",
            "Configurar SageMaker Data Wrangler para preprocesar el texto, extraer features mediante clustering y que los agentes analicen la similitud de documentos dentro de datasets estructurados, particionando los datos agrupados entre nodos para acelerar las consultas",
        ],
        correct=2,
        key="aip01r-q16",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Titan Text Embeddings + OpenSearch con sharding del indice vectorial.</div>'
            '<p><b>El problema:</b> generar embeddings semanticos gestionados para RAG y, ante un gran volumen de documentos, escalar la recuperacion vectorial con una estrategia de distribucion de datos y manejo de consultas.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> <b>Amazon Titan Text Embeddings</b> convierte texto en vectores y <b>OpenSearch Service</b> los indexa para busqueda por similitud. La clave a nivel profesional es el <b>sharding</b>: OpenSearch divide el indice vectorial en <b>shards</b> repartidos entre varios nodos, de modo que las consultas se ejecutan en paralelo y el sistema escala <b>horizontalmente</b> a medida que crece el corpus. Esa estrategia de distribucion es lo que sostiene latencia baja y throughput alto en volumenes grandes, no solo "usar embeddings".</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Amazon Kendra:</b> es busqueda empresarial que indexa y recupera con lenguaje natural y ranking, pero no genera ni gestiona los embeddings vectoriales que exige el RAG con agentes de Bedrock ni expone una estrategia de sharding del indice vectorial.</li>'
            '<li><b>SageMaker JumpStart:</b> acelera desplegar y ajustar modelos preentrenados, pero no genera embeddings ni realiza busqueda por similitud vectorial para el flujo de RAG.</li>'
            '<li><b>SageMaker Data Wrangler:</b> prepara y transforma datos (limpieza, feature engineering); no crea ni almacena embeddings de texto ni habilita busqueda vectorial semantica.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG a gran escala: modelo de embeddings + almacen vectorial gestionado. El detalle que decide es el escalado del indice: sharding = reparto del indice vectorial entre nodos para consultas paralelas y escalado horizontal. Kendra recupera pero no da vectores; Data Wrangler prepara datos, no busca.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html">docs.aws OpenSearch shards y dimensionamiento</a> '
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html">docs.aws Titan Text Embeddings</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q20r - Comprehend TOXICITY DETECTION (feature especifica)
    # ------------------------------------------------------------
    card(
        question="Una red social entrena modelos en Amazon SageMaker AI para moderar contenido y quiere <b>detectar en tiempo real lenguaje toxico o dañino</b> (discurso de odio, acoso, amenazas explicitas). La solucion debe <b>integrarse con el pipeline de inferencia de SageMaker</b>, manejar alto throughput y devolver <b>puntajes de confianza</b> por clasificacion para bloquear o revisar automaticamente. ¿Que solucion gestionada aporta clasificadores de seguridad para detectar toxicidad en texto?",
        options=[
            "Usar el analisis de sentimiento de Amazon Comprehend para detectar comentarios negativos y bloquear el contenido automaticamente",
            "Usar Amazon Translate para convertir el texto a otro idioma antes de la moderacion y asi reducir el contenido ofensivo",
            "Usar la deteccion de toxicidad (toxicity detection) de Amazon Comprehend para identificar lenguaje abusivo o dañino en el texto",
            "Usar Amazon Bedrock para hacer fine-tuning de un foundation model orientado a la comprension general del lenguaje",
        ],
        correct=2,
        key="aip01r-q20",
        answer=(
            '<div class="verdict">Correcta: {{L}} - deteccion de toxicidad de Amazon Comprehend.</div>'
            '<p><b>El problema:</b> detectar toxicidad (odio, acoso, amenazas) en texto, en tiempo real, con puntajes de confianza y bajo esfuerzo, integrado al pipeline de SageMaker.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> Comprehend no es solo NLP de sentimiento: incluye una capacidad especifica de <b>toxicity detection</b> que clasifica el texto en categorias de contenido dañino y devuelve <b>scores de confianza</b> por categoria. Es gestionada (sin entrenar ni hospedar modelos propios) y esos puntajes permiten enrutar automaticamente a bloqueo o revision. La sub-feature exacta (toxicity detection) es lo que resuelve el caso, no el analisis de sentimiento generico.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Analisis de sentimiento de Comprehend:</b> solo clasifica el tono (positivo, negativo, neutro); no identifica lenguaje toxico, asi que perderia contenido dañino o marcaria negativos no toxicos.</li>'
            '<li><b>Amazon Translate:</b> traduce entre idiomas; no detecta ni mide toxicidad, solo cambia el idioma del texto.</li>'
            '<li><b>Fine-tuning en Bedrock:</b> mejora la comprension general del lenguaje, pero no detecta toxicidad de forma nativa; exigiria desarrollo custom, mas complejo que una feature gestionada.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Moderar toxicidad en texto sin construir modelo: la feature toxicity detection de Comprehend (scores por categoria). El sentiment analysis solo da tono; Translate solo traduce.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/trust-safety.html">docs.aws Comprehend toxicity detection</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q23r - Endpoints privados (VPC) tanto SageMaker como S3
    # ------------------------------------------------------------
    card(
        question="Una empresa minorista analiza reseñas de clientes con notebooks de Amazon SageMaker AI y Amazon Comprehend, con los datos en Amazon S3. Por sensibilidad, exige que <b>todos los recursos permanezcan dentro de una VPC</b> segura y que <b>toda la comunicacion ocurra sobre la red de AWS</b> (sin salir a internet). ¿Que solucion cumple?",
        options=[
            "Desplegar el notebook de SageMaker AI en una subnet privada con ruta a un internet gateway y enrutar todas las solicitudes a S3 a traves de un proxy externo",
            "Desplegar el notebook de SageMaker AI en una subnet privada dentro de una VPC y usar una conexion de VPC peering con otra VPC donde S3 sea accesible",
            "Desplegar el notebook de SageMaker AI en una subnet privada dentro de una VPC y asegurar que la VPC tenga endpoints privados tanto para SageMaker AI como para S3",
            "Desplegar el notebook de SageMaker AI en una subnet privada, usar un NAT gateway para dar salida a internet hacia S3 y restringir el acceso solo a buckets S3 especificos",
        ],
        correct=2,
        key="aip01r-q23",
        answer=(
            '<div class="verdict">Correcta: {{L}} - subnet privada con endpoints privados (VPC endpoints) para SageMaker AI y S3.</div>'
            '<p><b>El problema:</b> mantener todos los recursos en la VPC y que el trafico a los servicios de AWS no salga a internet, viajando solo por la red de AWS.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el objetivo exacto es cubrir con <b>endpoints privados (VPC endpoints)</b> AMBOS servicios: SageMaker AI y S3. Un VPC endpoint (interface endpoint para SageMaker, gateway endpoint para S3) mantiene la comunicacion dentro de la red de AWS, sin pasar por internet gateway ni proxies. Poner endpoints para los dos servicios cierra la ruta publica por completo, que es lo que exige el escenario. No basta con aislar la subnet: hay que rutear cada servicio por su endpoint privado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Subnet privada + internet gateway + proxy externo:</b> enrutar por un IGW y un proxy externo expone el trafico a internet publico, contradiciendo el requisito de comunicacion privada por la red de AWS.</li>'
            '<li><b>VPC peering con otra VPC:</b> el peering no da acceso privado nativo a servicios como S3; sin VPC endpoints seguiria dependiendo de endpoints publicos.</li>'
            '<li><b>NAT gateway hacia S3:</b> el NAT enruta por internet publico; aun restringiendo buckets, la ruta no cumple el aislamiento exigido.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Trafico a servicios AWS sin salir a internet: VPC endpoints para CADA servicio implicado (aqui SageMaker + S3), no NAT, no IGW, no peering. Interface endpoint (ENI) para APIs; gateway endpoint para S3/DynamoDB.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/interface-vpc-endpoint.html">docs.aws VPC endpoints de SageMaker</a> '
            '<a href="https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html">docs.aws gateway endpoint para S3</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q39r - Pinecone + Comprehend + Llama 2 en SageMaker endpoint
    # ------------------------------------------------------------
    card(
        question="Un equipo construye un chatbot de soporte con arquitectura RAG: consulta una <b>base de datos vectorial Pinecone</b> para recuperar documentos relevantes, analiza el contexto con <b>Amazon Comprehend</b> (entidades y sentimiento) y luego alimenta ese contexto a un foundation model desplegado en un <b>endpoint de inferencia en tiempo real de Amazon SageMaker AI</b>. ¿Que solucion integra mejor Pinecone en este sistema RAG para dar contexto al modelo Llama 2?",
        options=[
            "Usar Pinecone para indexar la documentacion, recuperar informacion relevante segun la consulta, analizar el contexto con Comprehend y pasar el contexto refinado a un modelo Llama 2 desplegado en un endpoint de inferencia en tiempo real de SageMaker AI para generar la respuesta",
            "Usar Pinecone para busquedas de similitud sobre las consultas, recuperar el contexto, analizar el sentimiento con Comprehend y enviar la informacion al chatbot, que interactuara con un modelo Llama 2 hospedado y gestionado manualmente en instancias Amazon EC2",
            "Usar Pinecone para busquedas de similitud sobre las consultas, reunir el contexto relevante y pasarlo a Amazon Lex para procesar la intencion del usuario antes de enviarlo al modelo Llama 2 para la generacion de la respuesta",
            "Usar Pinecone para catalogar la documentacion, recuperar la informacion contextual relevante y traducirla con Amazon Translate antes de reenviarla al modelo Llama 2 para que genere la respuesta al cliente",
        ],
        correct=0,
        key="aip01r-q39",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Pinecone + Comprehend + Llama 2 en un endpoint en tiempo real de SageMaker.</div>'
            '<p><b>El problema:</b> integrar Pinecone en un RAG que recupera contexto, lo enriquece con Comprehend y lo entrega a Llama 2 alojado en un endpoint de tiempo real de SageMaker AI, respetando la arquitectura pedida.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el matiz esta en los componentes EXACTOS: <b>Pinecone</b> como vector store para la recuperacion, <b>Comprehend</b> para extraer entidades y sentimiento del contexto, y <b>Llama 2</b> servido en un <b>endpoint de inferencia en tiempo real de SageMaker AI</b> (hosting gestionado, escalable y monitoreable). Solo esta opcion conserva SageMaker como capa de inferencia y usa Comprehend para enriquecer el contexto, tal como exige el escenario.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Llama 2 en EC2:</b> aloja el modelo en EC2 en vez del endpoint en tiempo real de SageMaker especificado; exige gestion manual y no aprovecha el hosting gestionado, el escalado y el monitoreo de SageMaker.</li>'
            '<li><b>Contexto a Amazon Lex:</b> Lex gestiona intencion y dialogo, no procesa el contexto para un modelo generativo; añade complejidad sin aportar el enriquecimiento (entidades/sentimiento) requerido.</li>'
            '<li><b>Amazon Translate:</b> traduce texto; no analiza sentimiento ni entidades. El escenario pide enriquecer el contexto con Comprehend, no traducirlo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG con vector store externo (Pinecone) + enriquecimiento (Comprehend) + generacion en hosting gestionado: endpoint en tiempo real de SageMaker. EC2 = gestion manual; Lex = intencion/dialogo; Translate = traduccion, no analisis.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html">docs.aws endpoints en tiempo real de SageMaker</a> '
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/how-entities.html">docs.aws Comprehend entidades</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q41r - Grounding anti-alucinacion con Bedrock Knowledge Bases
    # ------------------------------------------------------------
    card(
        question="Una organizacion de investigacion economica genera resumenes analiticos con IA a partir de reportes de resultados y documentos regulatorios. En pruebas tempranas aparecen <b>alucinaciones</b> sobre ingresos proyectados y exposicion al riesgo. Por compliance y auditoria necesita un mecanismo de verificacion que <b>detecte afirmaciones no respaldadas</b>, haga <b>cross-check a nivel de documento</b> y valide cada respuesta generada contra <b>fuentes empresariales confiables</b>. ¿Que solucion cumple mejor?",
        options=[
            "Implementar un flujo de verificacion de exactitud basado en grounding con recuperacion (retrieval-augmented grounding) respaldado por Amazon Bedrock Knowledge Bases",
            "Usar la clasificacion personalizada de Amazon Comprehend para categorizar las respuestas por tema financiero y enrutar las de baja confianza a un endpoint de SageMaker para evaluacion",
            "Ejecutar validaciones SQL con Amazon Athena sobre los valores numericos de los resumenes y usar Amazon EventBridge para alertar cuando los resultados se desvien de patrones historicos",
            "Desplegar un pipeline de SageMaker Model Monitor que compare embeddings de cada respuesta contra vectores historicos, alerte ante discrepancias y almacene metadatos en Amazon DynamoDB",
        ],
        correct=0,
        key="aip01r-q41",
        answer=(
            '<div class="verdict">Correcta: {{L}} - grounding con recuperacion respaldado por Bedrock Knowledge Bases.</div>'
            '<p><b>El problema:</b> reducir alucinaciones validando cada afirmacion generada contra documentos fuente confiables, con cross-check a nivel documento y trazabilidad para auditoria.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el mecanismo clave es el <b>grounding</b>: <b>Bedrock Knowledge Bases</b> recupera pasajes de fuentes autorizadas y ancla la generacion en esa evidencia, de modo que las afirmaciones quedan respaldadas por documentos reales (retrieval-augmented grounding). Eso es exactamente la verificacion anti-alucinacion pedida, no un monitoreo generico: la respuesta se contrasta contra el conocimiento curado antes de aceptarse.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Comprehend custom classification:</b> clasifica temas o patrones linguisticos, pero no recupera contexto autorizado ni valida la correccion factual frente a fuentes confiables.</li>'
            '<li><b>Athena + EventBridge:</b> Athena consulta datos estructurados y valida numeros o desviaciones, pero no verifica si el texto generativo esta fundamentado en documentos autorizados.</li>'
            '<li><b>SageMaker Model Monitor:</b> detecta drift de datos/features y degradacion de calidad, no correccion factual; comparar embeddings no confirma que la afirmacion coincida con documentos financieros autorizados.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Anti-alucinacion con evidencia verificable: grounding via retrieval que ancla cada respuesta en fuentes confiables. Model Monitor detecta drift, no falsedad; Athena valida numeros, no narrativa.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q42r - KMS (cifrado) + AWS Glue para REDACTAR PII
    # ------------------------------------------------------------
    card(
        question="Una empresa de servicios financieros entrena en Amazon SageMaker AI un modelo de deteccion de fraude sobre datos historicos con informacion sensible (numeros de tarjeta) y usa Amazon Comprehend para extraer features del texto. Debe garantizar que todos los datos esten <b>cifrados</b> y que la <b>PII (incluidos numeros de tarjeta) se redacte</b> antes de usarse para entrenar. ¿Que solucion cumple el requisito?",
        options=[
            "Procesar los datos con SageMaker AI Data Wrangler aplicando cifrado con un algoritmo propio, automatizar la subida cifrada a Amazon S3 con AWS CLI y entrenar con el dataset cifrado",
            "Detectar y redactar la PII con Comprehend, almacenar los datos redactados en Amazon S3 y entrenar con SageMaker AI, cifrando los datos con un algoritmo propio",
            "Reducir la dimensionalidad de los datos con el algoritmo PCA de SageMaker AI antes de entrenar, eliminando la informacion sensible durante el proceso de PCA y guardando los datos en Amazon S3",
            "Cifrar los datos con AWS KMS en Amazon S3 antes de importarlos a SageMaker AI y usar AWS Glue para redactar los numeros de tarjeta antes de usarlos en el entrenamiento",
        ],
        correct=3,
        key="aip01r-q42",
        answer=(
            '<div class="verdict">Correcta: {{L}} - cifrado con AWS KMS en S3 + AWS Glue para redactar PII.</div>'
            '<p><b>El problema:</b> cifrar los datos con una solucion gestionada y compatible con compliance, y redactar la PII (numeros de tarjeta) antes del entrenamiento.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> son dos features concretas y correctas. <b>AWS KMS</b> proporciona cifrado gestionado con claves auditables (lo esperado en finanzas, frente a un algoritmo propio). Y la redaccion de PII se hace con <b>AWS Glue</b>: Glue transforma el dato y puede <b>redactar/reemplazar</b> los numeros de tarjeta durante el ETL, dejando el dataset limpio antes de entrenar. El detalle avanzado es usar Glue para la redaccion efectiva, no solo descubrir PII.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Data Wrangler + algoritmo de cifrado propio:</b> Data Wrangler prepara datos, no redacta PII, y un cifrado propio no cumple estandares; KMS es el enfoque gestionado recomendado.</li>'
            '<li><b>Comprehend redacta + cifrado propio:</b> aunque Comprehend detecta y redacta PII, el cifrado con algoritmo propio introduce riesgo y puede no ser compatible; KMS es lo apropiado.</li>'
            '<li><b>PCA para eliminar PII:</b> PCA reduce dimensionalidad, no sanea ni garantiza la eliminacion de numeros de tarjeta; no es un metodo de redaccion seguro.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cifrado en finanzas: claves gestionadas y auditables (servicio de gestion de claves), nunca algoritmo propio. Redactar PII en el pipeline: transformarla con un servicio ETL gestionado. PCA reduce dimensiones, no redacta.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/detect-PII.html">docs.aws AWS Glue deteccion y redaccion de PII</a> '
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html">docs.aws cifrado S3 con KMS</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q43r - SageMaker DeepAR (algoritmo de forecasting)
    # ------------------------------------------------------------
    card(
        question="Una empresa electrica gestiona consumo horario de 150 tipos de medidores en varias regiones, con 30 años de historico enriquecido (clima, precios, mantenimiento). El equipo ya usa SageMaker AI Data Wrangler y Canvas, y ahora quiere construir un modelo de ML propio para <b>pronosticar patrones futuros de consumo de todos los tipos de medidor</b>. ¿Que opcion cumple con el <b>MENOR overhead operativo</b>?",
        options=[
            "Construir un unico modelo global de forecasting con el algoritmo SageMaker AI DeepAR, entrenado sobre todos los tipos de medidor para capturar patrones de consumo compartidos",
            "Entrenar multiples modelos con el algoritmo SageMaker AI Prophet, uno por cada tipo de medidor, para capturar patrones estacionales de cada dispositivo",
            "Usar SageMaker AI Autopilot para crear y ajustar automaticamente un unico modelo predictivo para todos los tipos de medidor con el dataset combinado",
            "Crear un unico modelo global de forecasting con el algoritmo SageMaker AI XGBoost, entrenado sobre todos los tipos de medidor para predecir el consumo futuro",
        ],
        correct=0,
        key="aip01r-q43",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un modelo global con el algoritmo SageMaker DeepAR.</div>'
            '<p><b>El problema:</b> pronosticar series de tiempo de muchos tipos de medidor a la vez, con el minimo overhead operativo.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el algoritmo exacto es <b>DeepAR</b>, el algoritmo de forecasting integrado de SageMaker diseñado para <b>multiples series de tiempo relacionadas</b>. Entrena un <b>unico modelo global</b> que aprende patrones compartidos entre todas las series (los 150 tipos de medidor), en vez de un modelo por serie. Eso captura estacionalidad comun y reduce drasticamente el overhead de entrenar, desplegar y mantener modelos separados.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Prophet, uno por medidor:</b> gestionar 150 modelos separados dispara la complejidad de entrenamiento, despliegue y mantenimiento; ademas escala peor que DeepAR para muchas series.</li>'
            '<li><b>Autopilot:</b> esta optimizado para datos tabulares (clasificacion/regresion), sin soporte nativo de dependencias temporales ni estacionalidad, criticas en forecasting.</li>'
            '<li><b>XGBoost:</b> es potente para datos tabulares, pero no esta diseñado para series de tiempo; obligaria a ingenieria manual de features temporales, aumentando la complejidad operativa.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Forecasting de muchas series de tiempo relacionadas con menor overhead: un modelo global con el algoritmo de series de tiempo integrado. XGBoost es tabular (features manuales); Autopilot no maneja temporalidad; un modelo por serie no escala.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/deepar.html">docs.aws algoritmo DeepAR</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q45r - Bedrock KB con API RetrieveAndGenerate + CITAS
    # ------------------------------------------------------------
    card(
        question="Una red hospitalaria construye un asistente clinico con Amazon Bedrock que debe responder <b>solo con guias clinicas aprobadas</b> y <b>citar la fuente especifica</b> de cada recomendacion para que el medico la verifique. Quiere <b>reducir alucinaciones</b> y prefiere un enfoque gestionado con <b>minima logica de recuperacion propia</b>. ¿Que enfoque cumple minimizando el esfuerzo operativo?",
        options=[
            "Guardar los documentos aprobados en Amazon S3 e incluir extractos seleccionados directamente en cada prompt de Bedrock, instruyendo al modelo para que cite los nombres de documento al generar recomendaciones",
            "Hacer fine-tuning de un foundation model de Bedrock con la documentacion clinica aprobada y exigir al modelo que incluya referencias a la fuente en cada respuesta generada",
            "Usar Amazon Kendra para indexar los documentos aprobados y recuperar pasajes, pasar el contenido recuperado a Bedrock mediante logica de aplicacion propia y generar las citas por separado en la aplicacion",
            "Crear una Bedrock Knowledge Base con las referencias clinicas aprobadas como fuente e invocar la API RetrieveAndGenerate para anclar las respuestas en la evidencia recuperada e incluir citas que apunten a los documentos fuente",
        ],
        correct=3,
        key="aip01r-q45",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bedrock Knowledge Base + API RetrieveAndGenerate con citas.</div>'
            '<p><b>El problema:</b> responder solo con fuentes aprobadas, citar el documento exacto por cada recomendacion y reducir alucinaciones, con el menor codigo de recuperacion propio.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el matiz clave no es "RAG generico", sino la <b>API RetrieveAndGenerate</b> de Bedrock Knowledge Bases. Esa API es un flujo gestionado de recuperacion + generacion que, en una sola llamada, recupera pasajes de la KB, ancla la respuesta en ellos y devuelve <b>citas</b> estructuradas con la metadata de las referencias usadas. Asi el medico verifica el origen y se minimiza el codigo custom. La sub-feature (RetrieveAndGenerate + citas nativas) es exactamente lo evaluado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Extractos en el prompt + citar por instruccion:</b> obliga a construir la recuperacion, el armado del prompt y la atribucion a mano, y pedir al modelo que "cite" no entrega las citas estructuradas ni la metadata que devuelve RetrieveAndGenerate.</li>'
            '<li><b>Fine-tuning con referencias:</b> cambia el comportamiento del modelo pero no ancla dinamicamente cada respuesta en documentos recuperados ni devuelve citas a los pasajes exactos.</li>'
            '<li><b>Kendra + logica propia + citas aparte:</b> exige integracion y codigo de citacion adicionales; Knowledge Bases ya ofrece recuperacion, generacion y citas nativas con menos operacion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Respuestas ancladas con citas y minima operacion: la API gestionada que recupera, genera y cita en una sola llamada sobre una base de conocimiento. Meter extractos en el prompt o pedir citas por instruccion no da citas estructuradas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/kb-test-config.html">docs.aws RetrieveAndGenerate y citas</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q49r - SageMaker network isolation mode + VPC endpoint Comprehend
    # ------------------------------------------------------------
    card(
        question="Una empresa despliega un sistema de recomendacion con Amazon SageMaker AI (entrenamiento e inferencia en tiempo real) y usa Amazon Comprehend para NLP de reseñas. Por compliance, tanto el entrenamiento como la inferencia y los servicios asociados deben quedar dentro de una VPC segura, y la solucion debe <b>bloquear por completo todo acceso a internet o recursos externos</b>, con el <b>MENOR esfuerzo de desarrollo</b>. ¿Que solucion cumple?",
        options=[
            "Configurar SageMaker AI en modo VPC only y establecer una conexion de VPC peering para acceder a Comprehend en otra VPC",
            "Desplegar SageMaker AI en modo VPC only y configurar un internet gateway con reglas restrictivas de security group para bloquear el acceso externo",
            "Activar el network isolation mode de SageMaker AI para bloquear todo acceso externo y establecer un VPC endpoint para Comprehend dentro de la misma VPC",
            "Usar modo VPC only para SageMaker AI, configurar una NACL para bloquear el acceso a internet y permitir el trafico hacia Comprehend",
        ],
        correct=2,
        key="aip01r-q49",
        answer=(
            '<div class="verdict">Correcta: {{L}} - network isolation mode de SageMaker + VPC endpoint para Comprehend.</div>'
            '<p><b>El problema:</b> aislamiento total (sin internet) para SageMaker y sus servicios, con Comprehend accesible de forma privada, y minimo desarrollo.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> la feature exacta es el <b>network isolation mode</b> de SageMaker: cuando esta activo, el contenedor de entrenamiento/inferencia <b>no tiene acceso de red saliente</b>, garantizando el aislamiento total exigido. Para que el flujo aun alcance Comprehend sin salir a internet, se añade un <b>VPC endpoint</b> (PrivateLink) a Comprehend en la misma VPC. La combinacion (isolation mode + interface endpoint) cubre el bloqueo total con poco desarrollo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>VPC only + VPC peering:</b> el peering añade complejidad de rutas y grupos de seguridad, y no garantiza por si mismo que no haya acceso a internet.</li>'
            '<li><b>VPC only + internet gateway:</b> la presencia de un IGW contradice el requisito de bloquear internet por completo; las reglas de security group no dan aislamiento total.</li>'
            '<li><b>VPC only + NACL:</b> las NACL no bloquean todo el acceso externo de forma equivalente al isolation mode, y esta opcion no usa VPC endpoint para conectar de forma privada a Comprehend.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Aislamiento TOTAL del contenedor (sin salida a internet): network isolation mode de SageMaker. Para hablar con otro servicio AWS sin internet: VPC endpoint (PrivateLink). IGW o NACL no dan aislamiento completo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/mkt-algo-model-internet-free.html">docs.aws SageMaker network isolation</a> '
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/vpc-interface-endpoints.html">docs.aws VPC endpoint de Comprehend</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q50r - XGBoost: BAJAR max_depth para reducir overfitting
    # ------------------------------------------------------------
    card(
        question="Un modelo de prediccion de devoluciones con el algoritmo SageMaker XGBoost muestra un <b>AUC de entrenamiento muy alto pero cae mucho en validacion</b>. Los reportes de explicabilidad de SageMaker Clarify indican que el modelo es demasiado sensible a unas pocas features dominantes, señal de <b>overfitting</b>. El equipo decide ajustar hiperparametros para reducir la complejidad y mejorar la generalizacion. ¿Que modificacion de hiperparametro ayuda mejor a reducir el overfitting?",
        options=[
            "Aumentar el hiperparametro max_depth para permitir arboles mas profundos que capturen mejor las relaciones entre features poco frecuentes",
            "Disminuir el parametro min_child_weight para que cada hoja se divida con mas facilidad y capture mayor complejidad del dataset",
            "Aumentar el parametro colsample_bytree para que cada arbol use un subconjunto mayor de features y mejore la varianza del modelo",
            "Disminuir el valor del hiperparametro max_depth para limitar la complejidad de los arboles y evitar el sobreajuste a los patrones dominantes del entrenamiento",
        ],
        correct=3,
        key="aip01r-q50",
        answer=(
            '<div class="verdict">Correcta: {{L}} - disminuir max_depth para limitar la complejidad de los arboles.</div>'
            '<p><b>El problema:</b> el modelo memoriza el entrenamiento (AUC alto) pero generaliza mal (validacion baja). Hay que reducir la complejidad para combatir el overfitting.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el hiperparametro exacto es <b>max_depth</b> de XGBoost, que fija la <b>profundidad maxima de cada arbol</b>. Arboles mas profundos capturan mas interacciones pero tambien memorizan ruido; <b>bajar max_depth</b> hace arboles mas simples que aprenden patrones generales en vez de outliers, reduciendo el overfitting y mejorando la validacion. El matiz profesional es saber la direccion correcta de ese parametro concreto.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Aumentar max_depth:</b> hace cada arbol mas complejo y propenso a memorizar ruido; empeora el overfitting existente.</li>'
            '<li><b>Disminuir min_child_weight:</b> baja el minimo de observaciones para crear una hoja, generando mas splits y mas complejidad, justo lo contrario de lo buscado.</li>'
            '<li><b>Aumentar colsample_bytree:</b> usa mas features por arbol; aumenta la diversidad de features pero no limita la complejidad y puede favorecer el overfitting en inputs correlacionados.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Overfitting en XGBoost: reducir complejidad. Bajar max_depth (arboles menos profundos), subir min_child_weight, subir regularizacion (lambda/alpha), bajar eta. Aumentar profundidad o bajar min_child_weight hace lo contrario.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost_hyperparameters.html">docs.aws hiperparametros de XGBoost</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q56r - Metrica CloudWatch InvocationLatency de Bedrock (cross-region)
    # ------------------------------------------------------------
    card(
        question="Una empresa de e-commerce hace fine-tuning de Amazon Titan Text en SageMaker AI y lo despliega en produccion via la API gestionada de Amazon Bedrock. Por compliance, los artefactos deben cifrarse con AWS KMS y las llamadas a Bedrock deben ser auditables. Ademas quiere <b>monitorear continuamente latencia y throughput del modelo entre regiones</b> para asegurar rendimiento consistente. ¿Que solucion aporta una arquitectura segura, auditable y observable?",
        options=[
            "Hacer fine-tuning de Titan en SageMaker AI con datos en S3 cifrados con KMS, desplegar el modelo via Bedrock con una clave KMS del cliente, habilitar AWS CloudTrail para auditar la API y seguir la metrica InvocationLatency de Bedrock en CloudWatch por region",
            "Hacer fine-tuning de Titan en SageMaker AI con datos cifrados con SSE-S3, desplegarlo tras un endpoint de API Gateway frente a Bedrock y usar Amazon Macie para monitorear eventos de exfiltracion de datos sensibles hacia el exterior",
            "Desplegar Titan en Bedrock sin fine-tuning, restringir el acceso solo con roles de IAM y apoyarse unicamente en AWS CloudTrail para monitorear tanto las llamadas a la API como la latencia del modelo",
            "Entrenar Titan por completo en SageMaker AI, exportarlo a un servidor de inferencia en Amazon EC2 con cifrado de volumenes Amazon EBS y usar AWS Config para el monitoreo continuo de cumplimiento y rendimiento",
        ],
        correct=0,
        key="aip01r-q56",
        answer=(
            '<div class="verdict">Correcta: {{L}} - KMS gestionada por el cliente + CloudTrail + metrica CloudWatch InvocationLatency de Bedrock.</div>'
            '<p><b>El problema:</b> arquitectura segura (cifrado KMS), auditable (CloudTrail) y observable, con monitoreo continuo de latencia y throughput del modelo entre regiones.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el componente distintivo es la observabilidad con una <b>metrica CloudWatch especifica de Bedrock</b>: <b>InvocationLatency</b>. Bedrock publica metricas por modelo en CloudWatch, y seguir InvocationLatency (junto con conteos de invocacion/tokens) permite monitorear latencia y throughput <b>por region</b> de forma continua. Sumado a una clave <b>KMS gestionada por el cliente</b> (control y auditabilidad de cifrado) y <b>CloudTrail</b> (auditoria de API), cierra los tres requisitos. El matiz es nombrar la metrica correcta de Bedrock.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SSE-S3 + API Gateway + Macie:</b> SSE-S3 no da control ni auditabilidad de claves del cliente, API Gateway frente a Bedrock es innecesario, y Macie descubre datos sensibles en S3, no monitorea invocaciones ni latencia.</li>'
            '<li><b>Sin fine-tuning + solo CloudTrail:</b> omite la adaptacion de dominio requerida y el cifrado de artefactos con clave gestionada por el cliente; CloudTrail audita pero no mide latencia/throughput.</li>'
            '<li><b>Inferencia en EC2 + AWS Config:</b> mover la inferencia a EC2 abandona la API gestionada de Bedrock exigida, y Config rastrea configuracion, no latencia/throughput en tiempo real (eso es CloudWatch).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Observabilidad del modelo: la metrica nativa de latencia de invocacion (mas conteos de invocacion y de tokens) por region, publicada en el servicio de metricas. CloudTrail = auditoria de API; Config = estado de configuracion; Macie = descubrimiento de PII. Control de cifrado = clave del cliente (CMK).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-cw.html">docs.aws metricas de Bedrock en CloudWatch</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q60r - Scheduled scaling policy (pre-escalar antes del evento)
    # ------------------------------------------------------------
    card(
        question="Un endpoint de inferencia en tiempo real de Amazon SageMaker AI sirve recomendaciones. Ante <b>eventos de ventas planificados</b>, el equipo observa latencia alta por el aumento de actividad y quiere ajustar la politica de escalado para <b>garantizar capacidad antes de los picos conocidos</b> y evitar que la latencia afecte la experiencia. ¿Que solucion optimiza mejor el escalado del endpoint?",
        options=[
            "Configurar una scheduled scaling policy (politica de escalado programado) para aumentar la capacidad del endpoint de inferencia de SageMaker antes de que comiencen los eventos de ventas",
            "Usar AWS Lambda para reiniciar periodicamente el endpoint de inferencia de SageMaker durante el trafico pico y asi refrescar el rendimiento de las instancias del endpoint",
            "Implementar una step scaling policy para el endpoint de inferencia que escale segun metricas de utilizacion de recursos como el uso de CPU y de memoria de las instancias",
            "Aumentar el tamaño de instancia del endpoint de inferencia a un tipo mas grande para soportar el mayor trafico esperado durante los eventos de ventas planificados",
        ],
        correct=0,
        key="aip01r-q60",
        answer=(
            '<div class="verdict">Correcta: {{L}} - scheduled scaling policy para pre-escalar antes del evento.</div>'
            '<p><b>El problema:</b> los picos son <b>planificados</b> (eventos de ventas con fecha conocida); hay que tener capacidad lista de antemano para no acumular latencia mientras el auto scaling reactivo se pone al dia.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el matiz frente al auto scaling generico (target tracking) es usar una <b>scheduled scaling policy</b>: como se conoce la fecha/hora del pico, se programa el aumento de capacidad <b>antes</b> de que empiece. Asi el endpoint ya tiene instancias suficientes cuando llega el trafico, evitando el retraso de reaccionar a la demanda. El target tracking reacciona a metricas en vivo; el scheduled scaling se anticipa a un evento conocido.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda que reinicia el endpoint:</b> reiniciar no mejora la escalabilidad, introduce downtime y no ataca la causa (capacidad insuficiente en el pico).</li>'
            '<li><b>Step scaling por CPU/memoria:</b> los endpoints de SageMaker escalan mejor por metricas de inferencia (invocaciones por instancia), no por CPU/memoria granular; ademas sigue siendo reactivo, no anticipado.</li>'
            '<li><b>Instancia mas grande:</b> es una solucion estatica que no se ajusta al patron de trafico; lleva a sobreaprovisionar fuera del pico o quedarse corto dentro de el.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Pico con fecha conocida: scheduled scaling (pre-escala por horario). Pico impredecible: target tracking sobre invocaciones por instancia. Subir el tipo de instancia es estatico; reiniciar no escala.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html">docs.aws auto scaling de endpoints de SageMaker</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q62r - Workflow ML seguro: SSE-KMS + IAM + CloudWatch
    # ------------------------------------------------------------
    card(
        question="Una empresa financiera entrena en Amazon SageMaker AI un modelo de deteccion de fraude en tiempo real, con ingesta por Amazon Kinesis Data Streams, metadatos en Amazon DynamoDB e historico en Amazon S3. Debe cifrar los datos en transito y en reposo, controlar estrictamente el acceso a datos y resultados, y <b>rastrear el rendimiento del modelo en el tiempo</b>. ¿Que solucion asegura el flujo, controla el acceso y permite el monitoreo continuo del modelo?",
        options=[
            "Entrenar el modelo con datos de S3, habilitar el cifrado del lado del servidor SSE-KMS para los datos en reposo, configurar roles de IAM para controlar el acceso al modelo y a los datos, y usar Amazon CloudWatch para monitorear metricas de rendimiento y el logging del modelo",
            "Entrenar el modelo con datos de S3, habilitar el cifrado del lado del servidor SSE-S3 para los datos en reposo, guardar los resultados del modelo en S3 con roles de IAM para el acceso y usar Amazon Macie para monitorear la exposicion de datos sensibles",
            "Entrenar el modelo con datos de S3, almacenar el modelo y los metadatos en DynamoDB, configurar VPC endpoints entre SageMaker AI, DynamoDB y Kinesis, y usar AWS CloudTrail para monitorear el acceso y la actividad de la API a lo largo del tiempo",
            "Entrenar el modelo con datos de S3, configurar Amazon Data Firehose para ingerir los datos hacia SageMaker AI, catalogar los datos de transacciones con AWS Glue y usar CloudWatch para el monitoreo junto con politicas de IAM para restringir el acceso",
        ],
        correct=0,
        key="aip01r-q62",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SSE-KMS + roles de IAM + CloudWatch para monitoreo del modelo.</div>'
            '<p><b>El problema:</b> combinar cifrado gestionado y auditable, control de acceso granular y monitoreo continuo del rendimiento del modelo, en un flujo de ML de deteccion de fraude.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el matiz es la <b>decision combinada</b> correcta del workflow seguro: <b>SSE-KMS</b> cifra en reposo con claves gestionadas y auditables (superior a SSE-S3 para finanzas), los <b>roles de IAM</b> dan control de acceso de grano fino al modelo y los datos, y <b>Amazon CloudWatch</b> es el servicio adecuado para <b>monitorear metricas de rendimiento del modelo</b> en el tiempo. Cada pieza cumple un requisito distinto y juntas cubren cifrado, acceso y observabilidad.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SSE-S3 + Macie:</b> SSE-S3 no ofrece el control ni la auditabilidad de claves gestionadas por el cliente de SSE-KMS, y Macie descubre PII en S3, no monitorea el rendimiento del modelo ni controla el acceso al modelo.</li>'
            '<li><b>Modelo/metadatos en DynamoDB + CloudTrail:</b> DynamoDB no es apto para artefactos grandes de modelo (van en S3), y CloudTrail audita actividad de API, no el rendimiento del modelo (eso es CloudWatch).</li>'
            '<li><b>Data Firehose + Glue:</b> Firehose y Glue no son necesarios para ingerir/entrenar en tiempo real desde Kinesis o S3, y no aportan el nucleo pedido (cifrado con claves gestionadas + control de acceso + monitoreo del modelo).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Workflow ML seguro y observable: cifrado en reposo con claves gestionadas y auditables + control de acceso granular (IAM) + monitoreo de rendimiento del modelo (CloudWatch). CloudTrail audita API; Macie descubre PII; el cifrado gestionado por S3 solo no da control de claves del cliente.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html">docs.aws SageMaker Model Monitor</a> '
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html">docs.aws cifrado S3 con KMS</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q67r - Estrategia de tuning Hyperband (early stopping)
    # ------------------------------------------------------------
    card(
        question="Un equipo optimiza hiperparametros con SageMaker AI Automatic Model Tuning (AMT). Durante el tuning, muchos jobs siguen corriendo aunque las validaciones tempranas indican mal desempeño, gastando GPU innecesariamente. La empresa quiere una estrategia de tuning que <b>detenga automaticamente los ensayos de bajo rendimiento y reasigne recursos</b> a las configuraciones prometedoras para reducir costo de computo. ¿Que estrategia usar?",
        options=[
            "Implementar optimizacion bayesiana para refinar iterativamente el espacio de busqueda de hiperparametros",
            "Utilizar la estrategia Hyperband en SageMaker AI para asignar recursos de forma eficiente y detener temprano (early stop) los ensayos debiles",
            "Usar grid search para evaluar exhaustivamente todas las combinaciones posibles de hiperparametros sin detencion temprana",
            "Utilizar random search para muestrear combinaciones de hiperparametros de forma uniforme en el espacio de busqueda",
        ],
        correct=1,
        key="aip01r-q67",
        answer=(
            '<div class="verdict">Correcta: {{L}} - estrategia Hyperband con early stopping.</div>'
            '<p><b>El problema:</b> dejar de gastar GPU en ensayos que ya se ven malos y redirigir recursos a las configuraciones prometedoras, acelerando la busqueda.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> la estrategia exacta es <b>Hyperband</b>. A diferencia de bayesian/grid/random, Hyperband asigna recursos de forma <b>adaptativa</b> y aplica <b>early stopping</b>: evalua muchas configuraciones con poco presupuesto, descarta pronto las de bajo rendimiento y concentra el computo en las mejores. Ese mecanismo nativo de detencion temprana y reasignacion es justo lo que reduce el gasto de GPU, y es una feature de AMT que las otras estrategias no ofrecen.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Optimizacion bayesiana:</b> explora el espacio de forma eficiente construyendo un modelo probabilistico, pero no termina automaticamente los ensayos malos ni reasigna computo dinamicamente.</li>'
            '<li><b>Grid search:</b> prueba todas las combinaciones sin early stopping; cada job corre hasta el final, gastando muchos recursos, inviable en espacios grandes.</li>'
            '<li><b>Random search:</b> muestrea al azar pero tampoco detiene los jobs debiles temprano; corre cada ensayo completo, desperdiciando recursos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Detener temprano ensayos malos y reasignar computo en HPO: la estrategia con early stopping y asignacion adaptativa de recursos. Bayesian, grid y random NO paran los jobs debiles antes de tiempo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-how-it-works.html">docs.aws AMT Hyperband y early stopping</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q68r - Rol IAM del notebook con s3:GetObject/PutObject/ListBucket
    # ------------------------------------------------------------
    card(
        question="Un desarrollador entrena en Amazon SageMaker AI con datos en un bucket S3 y debe escribir artefactos, logs y resultados a un <b>bucket S3 distinto</b> al terminar. Necesita otorgar a la instancia de notebook de SageMaker los permisos adecuados para <b>leer de un bucket y escribir en otro</b> de forma segura. ¿Que enfoque conviene?",
        options=[
            "Definir una bucket policy en el bucket S3 que permita a la instancia de notebook de SageMaker, por su ARN, ejecutar las acciones s3:GetObject, s3:PutObject y s3:ListBucket",
            "Crear un S3 access point para la instancia de notebook, darle acceso a los datos necesarios y configurarlo para permitir solo las acciones s3:GetObject, s3:PutObject y s3:ListBucket",
            "Adjuntar una politica al rol de IAM asociado a la instancia de notebook que le otorgue s3:GetObject, s3:PutObject y s3:ListBucket sobre los buckets S3 designados",
            "Usar federacion de identidades de IAM para dar acceso temporal al bucket, configurando la instancia de notebook para asumir un rol federado que acceda a los datos",
        ],
        correct=2,
        key="aip01r-q68",
        answer=(
            '<div class="verdict">Correcta: {{L}} - adjuntar la politica al rol de IAM del notebook (Get/Put/ListBucket).</div>'
            '<p><b>El problema:</b> conceder a un servicio de AWS (el notebook de SageMaker) permisos de <b>lectura y escritura</b> a buckets S3 concretos, de forma segura y mantenible.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el patron correcto para acceso servicio-a-servicio es adjuntar una politica al <b>rol de IAM (execution role)</b> asociado al notebook. El detalle que suele fallar es incluir <b>s3:PutObject</b>: no basta con leer (GetObject/ListBucket), hay que permitir tambien la <b>escritura</b> al segundo bucket. Con el rol de IAM cubriendo las tres acciones sobre los buckets designados, el notebook lee del origen y escribe artefactos/logs al destino, siguiendo el enfoque recomendado por AWS.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bucket policy por ARN:</b> las bucket policies encajan mejor para acceso cross-account o permisos amplios; para un servicio propio, el rol de IAM es mas mantenible y alineado con las buenas practicas.</li>'
            '<li><b>S3 access point:</b> pensado para gestionar acceso a datasets compartidos a escala/multi-tenant; para un solo notebook añade complejidad innecesaria frente a un rol de IAM.</li>'
            '<li><b>Federacion de identidades:</b> es para identidades externas (usuarios corporativos, apps de terceros), no para servicios de AWS; SageMaker debe usar su rol de IAM, no identidades federadas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Permisos de un servicio AWS a S3: politica en su execution role de IAM. Para leer y escribir hacen falta GetObject + ListBucket + PutObject (no olvides la escritura). Bucket policy = cross-account; access point = datasets compartidos; federacion = identidades externas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html">docs.aws roles de ejecucion de SageMaker</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q69r - SageMaker Canvas scatter plot (color = 3a dim, size = 4a dim)
    # ------------------------------------------------------------
    card(
        question="Un desarrollador quiere visualizar recomendaciones en <b>cuatro dimensiones</b>: interes del usuario (eje X) contra tasa de conversion previa del producto (eje Y), la categoria del producto como <b>tercera dimension</b> y el numero de impresiones como <b>cuarta dimension</b>. El objetivo es detectar segmentos con alto interes y alta conversion pero bajas impresiones. ¿Que enfoque cumple mejor los requisitos?",
        options=[
            "Visualizar con el scatter plot de SageMaker Data Wrangler y colorear los puntos por la tercera feature para representar las cuatro dimensiones",
            "Usar la visualizacion Box Plot de SageMaker Canvas para comparar distribuciones y usar un patron de relleno para la tercera dimension",
            "Usar la visualizacion Bar Chart de SageMaker Canvas para agrupar productos por categoria y aplicar color y altura de barra para representar interes y conversion",
            "Usar el scatter plot de SageMaker Canvas y mapear la tercera dimension (categoria del producto) al color del punto y la cuarta dimension (numero de impresiones) al tamaño del punto",
        ],
        correct=3,
        key="aip01r-q69",
        answer=(
            '<div class="verdict">Correcta: {{L}} - scatter plot de SageMaker Canvas: color = categoria, tamaño = impresiones.</div>'
            '<p><b>El problema:</b> representar cuatro dimensiones a la vez (X, Y, mas dos atributos) para hallar productos de alto interes y alta conversion con pocas impresiones.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> la feature exacta es el <b>scatter plot de SageMaker Canvas</b> con codificaciones adicionales: eje X e Y para las dos primeras dimensiones, <b>color</b> del punto para la tercera (categoria) y <b>tamaño</b> del punto para la cuarta (impresiones). Ese mapeo de color y tamaño es lo que permite ver las cuatro dimensiones en un solo grafico y localizar el segmento buscado. El matiz es usar ambas codificaciones (color y size), no solo una.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Scatter de Data Wrangler solo con color:</b> mapea la tercera dimension por color pero omite la cuarta (impresiones) al no usar el tamaño del punto, perdiendo una parte clave del analisis.</li>'
            '<li><b>Box Plot:</b> muestra distribuciones estadisticas (mediana, cuartiles); no relaciona varias variables continuas ni codifica color/tamaño por punto como el scatter.</li>'
            '<li><b>Bar Chart:</b> se limita a pocas dimensiones; no puede representar con claridad interes y conversion a la vez ni codificar impresiones como tamaño.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cuatro dimensiones en un grafico: scatter plot con X, Y, color (3a dim) y tamaño de punto (4a dim). Box plot = distribuciones; bar chart = pocas dimensiones. Usar color solo cubre 3, faltaria el tamaño para la 4a.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-explore-data.html">docs.aws visualizaciones en SageMaker Canvas</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q72r - Hybrid search (vector + keyword) en OpenSearch
    # ------------------------------------------------------------
    card(
        question="Un asistente de troubleshooting con RAG indexa manuales e incidentes en Amazon OpenSearch Service y usa <b>busqueda por similitud vectorial</b>. Los ingenieros reportan que las busquedas devuelven documentos de significado similar pero <b>omiten registros con codigos de dispositivo, nombres de protocolo y acronimos exactos</b>. Hay que mejorar la precision preservando la relevancia semantica y ademas <b>coincidir con la terminologia precisa</b>, manteniendo baja latencia al crecer el repositorio. ¿Que solucion cumple mejor?",
        options=[
            "Aumentar el numero de resultados de la busqueda vectorial y aplicar un umbral de similitud mas alto para descartar documentos no relacionados antes de pasarlos al flujo de RAG",
            "Usar hybrid search para combinar la busqueda por similitud vectorial con la recuperacion basada en palabras clave, mejorando la relevancia semantica y a la vez coincidiendo con terminos y acronimos exactos",
            "Usar busqueda solo por palabras clave con el algoritmo BM25 en OpenSearch Service para priorizar terminos tecnicos, codigos y acronimos exactos antes de enviar los documentos al modelo",
            "Configurar busqueda semantica en OpenSearch Service con consultas neuronales para mejorar la comprension de la intencion y recuperar documentos por similitud contextual",
        ],
        correct=1,
        key="aip01r-q72",
        answer=(
            '<div class="verdict">Correcta: {{L}} - hybrid search (vectorial + keyword) en OpenSearch.</div>'
            '<p><b>El problema:</b> conservar la relevancia semantica de la busqueda vectorial pero tambien acertar en terminos exactos (codigos, protocolos, acronimos), con baja latencia al escalar.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> la tecnica exacta es <b>hybrid search</b>: OpenSearch <b>combina</b> la busqueda por similitud <b>vectorial</b> (significado) con la <b>lexical/keyword</b> (BM25, coincidencia exacta) y fusiona sus puntajes. Asi recupera tanto documentos conceptualmente relacionados como los que contienen el codigo o acronimo literal. La busqueda vectorial pura falla en terminologia precisa; la hibrida cubre ambos requisitos a la vez, que es el matiz avanzado evaluado.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Mas resultados + umbral mas alto:</b> solo ajusta como se seleccionan los resultados vectoriales; sigue siendo semantica y no añade el matching lexical de codigos y acronimos exactos.</li>'
            '<li><b>Solo BM25 (keyword):</b> acierta en terminos exactos pero pierde la comprension semantica; documentos que expresan el mismo concepto con otras palabras se quedarian fuera.</li>'
            '<li><b>Solo busqueda semantica/neuronal:</b> mejora la intencion y el contexto, pero no aporta el matching lexical preciso de identificadores tecnicos y acronimos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Necesitas significado Y terminos exactos: hybrid search (vector + keyword/BM25 con fusion de puntajes). Vector puro pierde acronimos/codigos; BM25 puro pierde sinonimos y contexto.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vector-search.html">docs.aws OpenSearch vector y hybrid search</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q73r - Pipeline Lambda+Comprehend -> metricas CloudWatch -> alarmas
    # ------------------------------------------------------------
    card(
        question="Una plataforma de e-commerce monitorea feedback en redes sociales (posts en Amazon S3). Amazon Rekognition extrae sentimiento visual y Amazon Kendra recupera texto relevante. El grupo de analitica debe puntuar sentimiento sobre el contenido recuperado, generar visualizaciones de tendencia de largo plazo y, sobre todo, <b>configurar alarmas automaticas ante umbrales de sentimiento</b> para responder rapido a picos de sentimiento negativo durante el lanzamiento. ¿Que combinacion de servicios cumple mejor?",
        options=[
            "Ejecutar un job de AWS Glue cuando lleguen posts a S3 para preprocesar el texto y llamar a un job de SageMaker Processing que calcule los puntajes; guardar el sentimiento en Amazon DynamoDB y visualizar con dashboards manuales en Amazon QuickSight",
            "Disparar una funcion AWS Lambda cuando S3 reciba un post nuevo y usar Amazon Comprehend para detectar sentimiento; guardar los resultados en S3, publicar los puntajes de sentimiento como metricas de Amazon CloudWatch y habilitar alarmas de CloudWatch para alertar automaticamente segun umbrales de sentimiento",
            "Configurar una notificacion de evento de S3 hacia Amazon SQS al llegar posts, analizar sentimiento con Amazon Comprehend desde la cola, guardar resultados en otro bucket S3 y visualizar tendencias con dashboards y reportes periodicos en Amazon QuickSight",
            "Crear un modelo de sentimiento basado en BlazingText en Amazon SageMaker AI y exponerlo con un endpoint; invocarlo con Lambda al llegar datos a S3, capturar resultados en Amazon DynamoDB y enviarlos a una metrica custom de CloudWatch para monitoreo y alertas",
        ],
        correct=1,
        key="aip01r-q73",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Lambda + Comprehend, publicar sentimiento como metricas CloudWatch y alarmas por umbral.</div>'
            '<p><b>El problema:</b> puntuar sentimiento en tiempo casi real y, sobre todo, <b>alertar automaticamente</b> ante picos de sentimiento negativo durante el lanzamiento, con poco overhead.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> el diseño de produccion exacto es el pipeline event-driven: <b>Lambda</b> se dispara al llegar un post a S3, <b>Comprehend</b> detecta el sentimiento (gestionado, sin entrenar), y el paso clave es <b>publicar el puntaje como metrica de CloudWatch</b> para luego encender <b>alarmas de CloudWatch por umbral</b>. Convertir el sentimiento en una metrica y alarmarla es lo que da la respuesta rapida y automatica pedida; las visualizaciones BI o los buffers no reaccionan en el momento.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Glue + SageMaker Processing + DynamoDB + QuickSight:</b> es ETL por lotes y BI; QuickSight no tiene alarmas por umbral en vivo y DynamoDB no analiza tendencias, asi que no da la reaccion automatica ante picos.</li>'
            '<li><b>S3 -> SQS -> Comprehend + QuickSight periodico:</b> SQS solo bufferea y los reportes periodicos revelan cambios en ciclos de revision, no de forma instantanea; se retrasa la deteccion de picos negativos.</li>'
            '<li><b>BlazingText en SageMaker:</b> añade complejidad innecesaria (entrenar, hospedar, mantener) cuando Comprehend ya da sentimiento gestionado; ademas DynamoDB limita el analisis de tendencias.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Alertar en tiempo real ante un umbral: convierte la señal en metrica de CloudWatch y ponle una alarma. Comprehend evita entrenar un modelo; QuickSight/SQS no alarman al instante. Patron: S3 event -> Lambda -> Comprehend -> metrica CloudWatch -> alarma.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html">docs.aws alarmas de CloudWatch</a> '
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/how-sentiment.html">docs.aws Comprehend sentimiento</a></div>'
        ),
    ),
]

_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "AIP-C01_01.apkg")

create(deck_name="AIP-C01::01", cards=cards, out_path=_OUT, do_import=False)
