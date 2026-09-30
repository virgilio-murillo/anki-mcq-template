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
        question="Se hace fine-tuning de un <b>LLM propio enorme</b> sobre terabytes de datos en SageMaker AI, minimizando tiempo y costo. ¿Que instancia EC2 conviene?",
        options=[
            "Instancias EC2 serie Trn (AWS Trainium) para entrenamiento a gran escala",
            "Instancias EC2 GPU serie P, sirviendo el modelo con endpoints de SageMaker",
            "Instancias EC2 de proposito general serie M con SageMaker distribuido",
            "Instancias EC2 de computo acelerado serie G, preprocesando con Comprehend",
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
        question="Un endpoint de SageMaker debe <b>evaluar una version nueva con trafico real</b> sin afectar el throughput ni cambiar la invocacion del cliente. ¿Que opcion cumple?",
        options=[
            "SageMaker Model Registry con un Lambda que haga swap del endpoint",
            "Dos endpoints de SageMaker separados, enrutando a mano y comparando en CloudWatch",
            "Un API Gateway que reparta el trafico y que los clientes invoquen",
            "Agregar el modelo como ProductionVariant en el mismo endpoint, con InitialVariantWeight pequeño",
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
        question="Un asistente con <b>Bedrock Agents</b> hace pasos con permisos y herramientas distintos (tickets, notificar, CRM). Se busca un diseño <b>modular</b> con minima orquestacion propia. ¿Que diseño conviene?",
        options=[
            "Un unico agente de Bedrock con un gran system prompt y un solo action group",
            "Varios foundation models en Bedrock con enrutamiento propio en la aplicacion",
            "Una knowledge base de Bedrock apoyada en RAG (retrieval-augmented generation)",
            "Colaboracion multi-agente: varios agentes de Bedrock, uno por responsabilidad",
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
        question="Un asistente de soporte debe <b>preservar contexto</b>, recuperar docs, ejecutar pedidos via API y dejar <b>auditoria</b>, con minima infraestructura propia. ¿Que enfoque cumple mejor?",
        options=[
            "Step Functions con historial en DynamoDB, recuperacion aparte y logs a CloudWatch",
            "AgentCore, que ejecuta el agente y aporta Memory, Gateway (API y Knowledge Base) y Observability gestionados",
            "Agente propio en Lambda con sesion en ElastiCache, Knowledge Bases y API Gateway",
            "Bedrock Knowledge Bases, historial en el cliente, pedidos con Lambda y auditoria en S3",
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
        question="Un prompt de Bedrock que resume historiales clinicos da <b>inconsistencias</b>. Se quiere <b>comparar versiones de prompt contra objetivos medibles</b> y conservar el historial. ¿Que enfoque cumple mejor?",
        options=[
            "Versionar los prompts y validar cada revision contra un benchmark medible",
            "Refinar con una muestra pequeña y revisar a mano, sin criterios de aceptacion",
            "Crear prompts separados para documentos simples y complejos, sin medir calidad",
            "Hacer fine-tuning con resumenes aceptados, asumiendo que el problema es del modelo",
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
        question="Varios equipos mantienen cientos de <b>plantillas de prompt</b> multi-Region y necesitan <b>gobierno centralizado</b>: versiones, aprobacion antes de produccion, notificar a revisores y trazar cada accion. ¿Que arquitectura conviene?",
        options=[
            "Step Functions, prompts en S3 con object tags y EventBridge para notificar",
            "Plantillas en S3 con Versioning, aprobacion de CodePipeline con SNS, CloudTrail e IAM",
            "Bedrock Prompt Management, aprobacion de CodePipeline con SNS, IAM y CloudTrail",
            "Bedrock AgentCore: Runtime, Identity e IAM, Observability, EventBridge y Memory",
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
        question="Una org regulada exige que <b>toda llamada a FMs use guardrails de Bedrock</b>. Los equipos llaman directo a las APIs; hay que cubrir InvokeModel y Converse con minimo overhead. ¿Que solucion lo logra?",
        options=[
            "Politicas IAM sobre InvokeModel y Converse que exijan bedrock:GuardrailIdentifier y bedrock:PromptRouterArn",
            "Un proxy con API Gateway y Lambda que inyecte los guardrails antes de Bedrock",
            "Guardar el identificador de guardrail en Secrets Manager y recuperarlo antes de llamar",
            "Politicas IAM sobre InvokeModel y Converse que exijan bedrock:GuardrailIdentifier",
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
        question="Un asistente en vivo necesita <b>muy baja latencia</b> con <b>capacidad de modelo predecible</b> en pico sostenido, costo fijo y con auto scaling de la app en todos los casos. ¿Que capa de modelo cumple?",
        options=[
            "Inferencia on-demand en Bedrock con aumentos de cuota",
            "Modelo de Bedrock de baja latencia con Provisioned Throughput",
            "Inferencia latency-optimized con cross-Region inference y on-demand en picos",
            "Batch inference de Bedrock con ventanas programadas",
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
        question="Un chatbot financiero en Bedrock debe frenar <b>prompt injection</b>, <b>auditar cada intervencion de seguridad</b> y ser <b>resiliente multi-Region</b>. ¿Que arquitectura cumple?",
        options=[
            "Guardrails de Bedrock, WAF en el endpoint HTTP, CloudTrail y el despliegue de la app",
            "Clasificadores de Comprehend, validacion de API Gateway y logs a CloudWatch Logs",
            "Guardrails de Bedrock con filtros de palabras clave, app multi-Region y CloudTrail",
            "Guardrails de Bedrock (umbral alto), un guardrail profile cross-Region y logs a CloudWatch",
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
        question="El FM debe <b>consultar varias fuentes</b> (Kinesis Data Streams, CloudWatch, embeddings de SageMaker) de forma segura, <b>sin APIs ni credenciales en los prompts</b>. ¿Que diseño cumple mejor?",
        options=[
            "Funciones Lambda por fuente, invocadas por sintaxis que genera el prompt",
            "Un servicio intermedio que exponga las fuentes como herramientas via Model Context Protocol (MCP)",
            "Solo los embeddings de SageMaker JumpStart y el conocimiento general del FM",
            "Microservicios separados por fuente y enrutamiento por prompt en Bedrock",
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
        question="Un chatbot en Bedrock usa un <b>cross-region inference profile</b> pero debe mantener los <b>datos dentro de EE. UU.</b>, transmitir seguro y escalar en picos. ¿Que enfoque cumple?",
        options=[
            "Un inference profile cross-Region global, con Kendra para la busqueda",
            "Un inference profile cross-Region de EE. UU. mas SageMaker con Provisioned Throughput",
            "Un inference profile cross-Region de EE. UU. mas Comprehend para categorizar",
            "Un inference profile cross-Region de EE. UU., cifrado en transito y Step Functions para picos",
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
        question="Las peticiones a FMs de Bedrock tardan; hay que ver la <b>respuesta incremental</b>, con <b>miles de sesiones concurrentes</b> y minima latencia. ¿Que arquitectura cumple mejor?",
        options=[
            "REST API en API Gateway con Lambda e InvokeModel, devolviendo todo al final",
            "WebSocket API en API Gateway con Lambda e InvokeModelWithResponseStream, empujando cada parcial",
            "Lambda con InvokeModelWithResponseStream que guarda parciales en DynamoDB y clientes por polling",
            "REST API en API Gateway e InvokeModelWithResponseStream, pero con buffer y una sola respuesta HTTP",
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
        question="Textract y Comprehend procesan documentos, pero <b>errores de OCR</b> fuerzan revision humana. Se quiere <b>reducir la revision manual</b> manteniendo precision. ¿Cual es la forma mas efectiva?",
        options=[
            "Claude de Bedrock para reanalizar el texto de baja confianza y luego revisar a mano",
            "Textract para marcar palabras de baja confianza y enviarlas a SageMaker Ground Truth",
            "Textract reenvia las predicciones de baja confianza a Amazon Augmented AI (A2I)",
            "Automatizar mas enviando el texto a un FM Amazon Titan, sin revision humana",
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
        question="Bedrock AgentCore usara un <b>LLM ya fine-tuned en SageMaker</b>. Debe dar inferencia segura dentro de Bedrock, monitorear en CloudWatch y minimizar overhead. ¿Que solucion cumple?",
        options=[
            "Desplegar el LLM en SageMaker, invocar sus endpoints con Lambda y monitorear en CloudWatch",
            "Importar el modelo a Bedrock con Custom Model Import, rol gestionado por AgentCore y CloudWatch",
            "Hospedar el LLM en EC2, conectarlo a Bedrock AgentCore via REST API y usar CloudWatch Logs",
            "Guardar el modelo en S3, que AgentCore lo cargue en runtime y monitorear con CloudWatch",
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
        question="Un asistente de Bedrock recibe demanda subita de Europa y Asia Pacifico. Debe mantener <b>baja latencia global</b> cumpliendo data residency con minimo overhead. ¿Que solucion cumple?",
        options=[
            "Endpoints de SageMaker en varias Regiones con enrutamiento por latencia en Route 53",
            "Comprehend en tiempo real en una Region central, copiando datos por adelantado",
            "El inference profile cross-Region de Bedrock, que enruta a Regiones con capacidad",
            "Desplegar el FM en cada Region via Bedrock, con enrutamiento propio en el cliente",
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
        question="Un flujo genera captions de imagenes en S3 con <b>picos impredecibles</b> (Rekognition, luego Bedrock) al subir. Debe autoescalar con minima infraestructura. ¿Que solucion cumple?",
        options=[
            "Un pipeline con ECS on Fargate por schedule, guardando en Aurora",
            "Un endpoint de SageMaker Asynchronous Inference con escalado automatico",
            "Un EC2 Auto Scaling group con una app que monitorea el bucket S3",
            "SQS para encolar y Lambda que ejecuten Rekognition y Bedrock por imagen",
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
        question="Por compliance se necesita <b>trazabilidad de cada invocacion de Bedrock</b> en todas las APIs (Converse, ConverseStream, InvokeModel, InvokeModelWithResponseStream), con salidas de imagen y analitica consultable. ¿Que solucion cumple?",
        options=[
            "Habilitar model invocation logs de Bedrock hacia S3 y CloudWatch Logs; texto e imagen",
            "Data Firehose para hacer streaming de los logs a S3 y OpenSearch Service",
            "Model invocation logs de Bedrock con un bucket S3 como unico destino; texto e imagen",
            "CloudTrail para capturar las invocaciones, logs en S3 y analitica con Athena",
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
        question="Amazon Q Business consulta S3 con prefijos por departamento (Finanzas, Legal, RR. HH., Ingenieria) y IAM Identity Center. Debe devolver <b>solo el prefijo del grupo del empleado</b> con minimo esfuerzo. ¿Que solucion cumple?",
        options=[
            "Un data source de Q Business por prefijo, con un rol IAM distinto y sync por carpeta",
            "Un archivo de metadatos por documento con el grupo, resincronizando en cada cambio",
            "Un unico acl.json en la raiz que mapee prefijo, grupo de IAM Identity Center y permiso",
            "Bucket policies de S3 por grupo, con Q Business rastreando todo el bucket",
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
        question="Un LLM de SageMaker resume historiales medicos y los <b>medicos deben revisar y corregir</b> antes del despliegue. Debe escalar e integrarse con los pipelines de SageMaker. ¿Que enfoque cumple?",
        options=[
            "SageMaker Model Monitor para marcar resumenes de baja confianza y guardarlos en S3",
            "La knowledge base de Bedrock para enriquecer el dataset con conocimiento externo",
            "Amazon Augmented AI (A2I) para una revision humana que valide los resumenes a escala",
            "SageMaker Ground Truth Plus: human-in-the-loop por expertos, integrado con el pipeline",
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
        question="Un asistente regulatorio en Bedrock recupera de varias fuentes y cada afirmacion debe <b>citar la fuente</b>, priorizar lo relevante y guardar citas para auditoria. ¿Que arquitectura cumple mejor?",
        options=[
            "Armar las citas a mano en la aplicacion, guardando afirmacion y fuente en DynamoDB",
            "Recuperacion vectorial propia con OpenSearch Serverless y citas en codigo",
            "RetrieveAndGenerate de Knowledge Bases con citas nativas y reranking, auditoria en S3",
            "Orquestar la recuperacion con Bedrock Agents que sigan instrucciones de citar",
        ],
        correct=2,
        key="aip01-q37",
        answer=(
            '<div class="verdict">Correcta: {{L}} - RetrieveAndGenerate de Knowledge Bases con citas nativas + reranking, auditoria en S3.</div>'
            '<p><b>El problema:</b> RAG con citas trazables, priorizando solo lo mas relevante y guardando razonamiento y citas para auditoria, con minima operacion.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>RetrieveAndGenerate</b> de <b>Bedrock Knowledge Bases</b> recupera y devuelve <b>citas</b> al contenido de soporte de forma nativa. Aplicar <b>reranking</b> prioriza los chunks mas relevantes (mejor precision, menor latencia y costo) antes de generar. Guardar razonamiento y citas en <b>S3</b> conserva artefactos durables para auditoria. Todo con poco desarrollo custom, frente a los enfoques que ensamblan la recuperacion o las citas a mano.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Citas a mano en la aplicacion + DynamoDB:</b> recrea en codigo la funcionalidad de citas que Knowledge Bases ya ofrece de forma nativa, añadiendo desarrollo y riesgo de desalinear afirmaciones con fuentes.</li>'
            '<li><b>Recuperacion vectorial propia con OpenSearch Serverless:</b> montar y mantener un vector store y el ensamblado de citas en codigo reproduce a mano lo que RetrieveAndGenerate ya gestiona, con mas operacion.</li>'
            '<li><b>Orquestar con Bedrock Agents:</b> los agentes orquestan flujos multi-paso con herramientas; aqui solo hace falta recuperar, rankear, generar, citar y guardar, asi que el agente añade complejidad innecesaria.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG con citas trazables y minima operacion: usa la recuperacion gestionada con citas nativas + reranking para relevancia. Guarda citas/razonamiento en un almacen durable, no solo la respuesta; evita reinventar la recuperacion o las citas a mano y no metas un agente para un flujo lineal.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws Bedrock Knowledge Bases</a></div>'
        ),
    ),
    # ============================================================
    # Q40 - Bedrock Model Evaluations job
    # ============================================================
    card(
        question="Se quiere <b>evaluar configuraciones de modelo</b> (variante, temperatura, prompt) por exactitud sobre consultas de compliance, con modelos base y personalizados de Bedrock. ¿Que solucion cumple?",
        options=[
            "Un job de Bedrock Model Evaluations, task Question and answer, con prompt dataset personalizado",
            "CloudWatch Synthetics para simular consultas y monitorear tiempo de respuesta",
            "Un job de Bedrock Model Evaluations, task Question and answer, con un dataset predefinido",
            "SageMaker Debugger para comparar configuraciones por salidas de capa y gradientes",
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
        question="Servidores MCP sobre la Cloud Control API responden lento con inventarios grandes. Se busca <b>latencia predecible, servidores stateless para escalar</b> y mejor throughput. ¿Que enfoque cumple mejor?",
        options=[
            "Servidores MCP stateless en ECS autoescalado con batching y concurrencia, y estado externo",
            "API Gateway delante de las llamadas MCP, con throttling y cache de respuestas",
            "EventBridge para invocar la Cloud Control API async y escribir en S3",
            "ElastiCache for Redis como cache de las respuestas mas consultadas",
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
        question="<b>Fine-tuning de un FM de SageMaker JumpStart con datos propios</b>, servido como endpoint, con una KB en OpenSearch. Hay que mapear la Generative AI Security Scoping Matrix. ¿Cual describe el scope?",
        options=[
            "Scope 3 (preentrenados): revisar licencia del FM para que el proveedor no reentrene",
            "Scope 4 (fine-tuned): clasificar y cifrar datos propios y auditar versiones y linaje",
            "Scope 2 (apps empresariales): cumplir terminos contractuales y SLAs de terceros",
            "Scope 5 (desde cero): propiedad total de infraestructura, clusteres de GPU y versionado",
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
        question="Un asistente financiero usa SageMaker y Kendra. Debe aplicar <b>content safety</b>, no filtrar datos personales y defenderse de <b>prompt injection</b>. ¿Que solucion cumple?",
        options=[
            "Amazon Bedrock Guardrails (contenido y automated reasoning) sobre Kendra y SageMaker",
            "Kendra con filtros de busqueda semantica y SageMaker para refinar respuestas",
            "SageMaker con post-procesamiento y los query filters de Kendra",
            "Las funciones de compliance integradas de Bedrock, invocando SageMaker si se confirma",
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
        question="Un agente de Bedrock alucina. Se necesita <b>observabilidad de como interpreta, razona y genera</b> (no solo la salida) y validar contra un golden dataset. ¿Que mecanismo cumple?",
        options=[
            "Model invocation logs y muestreo, que miden solo la salida",
            "GuardrailTrace, RoutingClassifierTrace y ModelInvocationInput, que exponen seguridad y enrutamiento",
            "Traces de las 3 fases del agente (pre-proceso, orquestacion y post-proceso)",
            "Prompt versioning y A/B testing, que comparan salidas entre versiones",
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
        question="Un equipo necesita clasificar correos spam con <b>transfer learning sobre un BERT preentrenado</b> en SageMaker, sin reentrenar desde cero. ¿Que enfoque inicializa correctamente el modelo?",
        options=[
            "Cargar los pesos y poner un clasificador externo sobre la salida; entrenar solo ese",
            "Aplicar los pesos, descartar la capa final, poner un clasificador nuevo y entrenarlo",
            "Usar los pesos y adjuntar un segundo clasificador en paralelo; entrenar solo ese",
            "Inicializar con los pesos y convertir la salida en un clasificador multitarea",
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
        question="Una editorial con PDFs, imagenes, audio y video quiere un asistente generativo. Ya procesa el contenido con <b>Bedrock Data Automation (BDA)</b> y planea SageMaker AI. ¿Como montar la recuperacion y generacion?",
        options=[
            "Un vector store propio con Lambda para indexar el contenido crudo en S3",
            "Indexar la salida de BDA en Knowledge Bases y generar con SageMaker AI",
            "Extraer entidades y sentimiento con Comprehend y servir el modelo en EC2",
            "Alimentar la salida de BDA directo al modelo para generar, sin busqueda semantica",
        ],
        correct=1,
        key="aip01-q54",
        answer=(
            '<div class="verdict">Correcta: {{L}} - indexar la salida de BDA en Knowledge Bases + generar via SageMaker AI.</div>'
            '<p><b>El problema:</b> procesar multimedia heterogeneo y montar un RAG que recupere contexto por busqueda semantica para generar respuestas.</p>'
            '<p><b>Por que la respuesta sirve:</b> con el contenido ya procesado por <b>BDA</b>, indexarlo en <b>Bedrock Knowledge Bases</b> habilita la busqueda semantica (recuperacion optimizada), y el contexto recuperado alimenta al foundation model via <b>SageMaker AI</b> para la respuesta. Es el flujo RAG completo y gestionado, frente a las alternativas que arman el vector store a mano o saltan la busqueda semantica.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Vector DB propia con Lambda + S3:</b> crear un vector store custom fuera de Knowledge Bases añade complejidad y pasos manuales; Knowledge Bases ya indexa y hace busqueda semantica de forma optimizada.</li>'
            '<li><b>Comprehend + FM en EC2:</b> Comprehend extrae entidades/sentimiento pero no da recuperacion semantica, y hospedar el FM en EC2 suma overhead operativo (provisionar, escalar, mantener) frente a SageMaker AI gestionado.</li>'
            '<li><b>Directo al FM sin busqueda semantica:</b> omitir el indexado y la recuperacion elimina la busqueda de contexto relevante; sin ella las respuestas son menos precisas o mas lentas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG sobre multimedia (docs/imagenes/audio/video): procesar con BDA + indexar/buscar con la base gestionada + generar con el FM. No reinventes el vector store ni omitas la busqueda semantica.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/bda.html">docs.aws Bedrock Data Automation</a></div>'
        ),
    ),
    # ============================================================
    # Q55 - AppConfig routing dinamico de FMs + failover
    # ============================================================
    card(
        question="Una app GenAI enruta cada tarea a un FM. Debe <b>cambiar el enrutamiento en runtime sin redeploy</b>, operar cross-Region y hacer failover, con minimo esfuerzo. ¿Que enfoque cumple?",
        options=[
            "Router en Flask sobre ECS con reglas en Aurora, invocando con el SDK de Bedrock",
            "API Gateway a una Lambda por tarea, config en S3 y Route 53; requiere redeploy",
            "Lambda con AppConfig Agent que lee reglas en runtime, Step Functions y endpoints regionales",
            "Router de Kubernetes en EKS con ConfigMaps, failover reiniciando Pods",
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
        question="Un modelo base en un endpoint real-time de SageMaker se quiere personalizar para cinco mercados con <b>adaptadores LoRA</b> sin reentrenar ni usar endpoints separados. ¿Que solucion cumple?",
        options=[
            "El modelo base con un inference component de adaptador LoRA por region que corre en el mismo endpoint",
            "Un multi-model endpoint, cada adaptador LoRA como artefacto y enrutamiento por contenedor",
            "El modelo base y los pesos LoRA de cada region en EFS que se monta en el endpoint",
            "El modelo base y un Lambda que recupere los pesos del adaptador y los inyecte",
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
        question="Se necesita un framework que cubra <b>RAG</b>, orqueste <b>workflows de agente en grafo</b> con estado durable y permita rollback y replay. Ya usa Feature Store, MLflow y Bedrock. ¿Que framework conviene?",
        options=[
            "Kendra para busqueda, Glue DataBrew para preprocesar y estado en ElastiCache for Redis",
            "LangChain para el pipeline RAG y LangGraph para el agente con estado, grafo y checkpoints",
            "SageMaker Pipelines para la recuperacion y EventBridge Pipes para el estado",
            "Step Functions para la orquestacion y OpenSearch Serverless como vector store, con Map states",
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
        question="Un asistente usa Kendra y un FM en Bedrock. Requiere <b>plantillas de prompt versionadas y reutilizables</b>, con temperature y max_tokens ajustables por consulta. ¿Que solucion conviene?",
        options=[
            "Bedrock Prompt Management: plantillas versionadas con parametros, invocado tras Kendra",
            "Incrustar el prompt y los parametros en una Lambda, editando el codigo en cada cambio",
            "Archivos de prompt en S3 que lee la Lambda, enviados con CreateModelCustomizationJob",
            "Un pipeline de Bedrock Prompt Flows que encadene prompts y modelos",
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
        question="Se compro Provisioned Throughput en Bedrock pero la app necesita salir del <b>throttling</b>: CloudWatch no muestra uso porque aun pasa el ID del modelo base en modelId. ¿Que cambio consume la capacidad provisionada?",
        options=[
            "Aumentar los model units y seguir usando el ID del modelo base en modelId",
            "Usar el nombre del modelo provisionado como modelId, sin cambiar el payload",
            "Actualizar modelId al ARN del modelo provisionado que devuelve CreateProvisionedModelThroughput",
            "Un inference profile cross-Region del FM, con el ID base como fallback",
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
        question="Un asistente de salud en Bedrock nunca debe dar <b>diagnosticos</b>, debe bloquear contenido daniño, <b>enmascarar PII</b> y filtrar entrada y salida, con minimos falsos positivos. ¿Que guardrails cumplen?",
        options=[
            "Content Filters al maximo, diagnosticos como denied topic y filtros que bloqueen toda PII",
            "Comprehend para PII y Macie sobre los logs, con un guardrail de Content Filters en alto",
            "Content Filters en medio, diagnosticos como denied topic, PII enmascarada y evaluacion in/out",
            "Tres guardrails separados encadenados con un workflow de Step Functions",
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
        question="Un FM de Bedrock da salidas malformadas y CloudWatch Logs solo muestra errores 400 y 500 sin metadatos. Se necesita <b>observabilidad de la ruta de invocacion</b>: request-response y tracing. ¿Que solucion cumple?",
        options=[
            "SageMaker Inference Recommender para analizar rendimiento y throughput del endpoint",
            "Step Functions Distributed Map para reprocesar a escala y analizar fallos entre lotes",
            "Bedrock AgentCore Observability para invocation traces y registros request-response del FM",
            "Metricas de invocacion de Bedrock con retry para latencia, throttling y anomalias",
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
        question="Una app en EC2 que llama a FMs de Bedrock ve peor calidad y mas latencia por segmento. Necesita <b>observabilidad centralizada que correlacione app y modelo</b>, con minimo esfuerzo. ¿Que enfoque cumple?",
        options=[
            "CloudWatch Application Insights, metricas por segmento, anomaly detection y Logs Insights",
            "Logging de Bedrock a CloudWatch Logs, metric filters, alarmas estaticas y dashboards manuales",
            "Agente de CloudWatch en EC2 para CPU/memoria/disco y revision manual",
            "Tracing con X-Ray de app y Bedrock, percentiles en CloudWatch y umbrales fijos a mano",
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
        question="Un chatbot con Nova Pro y contexto de Kendra da <b>respuestas distintas</b> aunque Kendra no cambie. Ante preguntas repetidas se quieren respuestas mas deterministas, sin tocar la recuperacion. ¿Que enfoque lo resuelve?",
        options=[
            "Bajar temperature y bajar top_k para reducir la aleatoriedad de tokens",
            "Subir temperature y subir top_k para ampliar la diversidad de tokens",
            "Bajar temperature y subir top_p para admitir mas candidatos de tokens",
            "Bajar temperature y bajar top_p para acotar la probabilidad acumulada",
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
        question="Una editorial construye un asistente RAG con Bedrock Agents. Necesita <b>embeddings semanticos gestionados</b> y, por el volumen, una <b>estrategia de distribucion de datos</b>. ¿Que enfoque cumple mejor?",
        options=[
            "Kendra para indexar y recuperar por busqueda semantica gestionada, ajustando facetas",
            "SageMaker JumpStart para fine-tuning y hospedar un modelo de resumen, replicado en nodos",
            "Amazon Titan Text Embeddings guardando vectores en OpenSearch Service, con sharding del indice",
            "SageMaker Data Wrangler para features por clustering, particionados entre nodos",
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
        question="Una red social quiere detectar <b>lenguaje toxico en tiempo real</b> en su pipeline de SageMaker, con alto throughput y puntajes de confianza. ¿Que servicio gestionado aporta clasificadores de toxicidad?",
        options=[
            "El analisis de sentimiento de Comprehend para detectar comentarios negativos",
            "Amazon Translate para convertir el texto antes de la moderacion",
            "La deteccion de toxicidad (toxicity detection) de Amazon Comprehend sobre el texto",
            "Bedrock para fine-tuning de un FM de comprension general del lenguaje",
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
        question="Se analizan reseñas con notebooks de SageMaker y Comprehend, datos en S3. Exige que <b>todo quede en una VPC</b> sin salir a internet. ¿Que solucion cumple?",
        options=[
            "Notebook de SageMaker en subnet privada con internet gateway y un proxy hacia S3",
            "Notebook de SageMaker en subnet privada con VPC peering a otra VPC con acceso a S3",
            "Notebook de SageMaker en subnet privada con VPC endpoints privados para SageMaker y S3",
            "Notebook de SageMaker en subnet privada con NAT gateway hacia S3, restringido a buckets",
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
        question="Un chatbot RAG usa <b>Pinecone</b>, Comprehend para el contexto y un FM en SageMaker. ¿Que solucion integra mejor Pinecone para dar contexto a Llama 2?",
        options=[
            "Pinecone para recuperar, Comprehend para el contexto y pasarlo a Llama 2 en un endpoint de SageMaker",
            "Pinecone para similitud, Comprehend para sentimiento y Llama 2 gestionado a mano en EC2",
            "Pinecone para similitud, contexto a Amazon Lex para la intencion y luego a Llama 2",
            "Pinecone para catalogar y recuperar, traduciendo con Translate antes de Llama 2",
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
        question="Los resumenes con IA de una firma economica tienen <b>alucinaciones</b>. Necesita verificacion que detecte afirmaciones no respaldadas y valide cada respuesta contra fuentes confiables. ¿Que solucion cumple mejor?",
        options=[
            "Un flujo de grounding con recuperacion (retrieval-augmented grounding) sobre Bedrock Knowledge Bases",
            "La clasificacion de Comprehend por tema, enrutando lo de baja confianza a SageMaker",
            "Validaciones SQL con Athena sobre los numeros y EventBridge para alertar desviaciones",
            "Un pipeline de SageMaker Model Monitor que compare embeddings, metadatos en DynamoDB",
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
        question="Un modelo de fraude en SageMaker usa numeros de tarjeta y Comprehend. Debe <b>cifrar todo y redactar la PII antes de entrenar</b>. ¿Que solucion cumple?",
        options=[
            "SageMaker Data Wrangler con cifrado propio, subida cifrada a S3 con AWS CLI",
            "Detectar y redactar la PII con Comprehend, guardar en S3 y entrenar, cifrando propio",
            "Reducir dimensionalidad con PCA de SageMaker para eliminar lo sensible, guardando en S3",
            "Cifrar con AWS KMS en S3 antes de SageMaker y usar AWS Glue para redactar las tarjetas",
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
        question="Una electrica con 150 tipos de medidor y 30 años de historico usa Data Wrangler y Canvas y quiere un <b>modelo propio de forecasting</b> para todos con minimo overhead. ¿Que opcion cumple?",
        options=[
            "Un unico modelo global de forecasting con el algoritmo SageMaker DeepAR sobre todos los medidores",
            "Multiples modelos con el algoritmo SageMaker Prophet, uno por tipo de medidor",
            "SageMaker Autopilot para crear un unico modelo con el dataset combinado",
            "Un unico modelo global con el algoritmo SageMaker XGBoost sobre todos los medidores",
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
        question="Un asistente clinico con Bedrock debe responder solo con <b>guias aprobadas y citar la fuente</b>, con minima recuperacion propia. ¿Que enfoque cumple con menor esfuerzo?",
        options=[
            "Guardar los documentos en S3 e incluir extractos en cada prompt, instruyendo a citar",
            "Hacer fine-tuning de un FM de Bedrock con la documentacion aprobada, exigiendo referencias",
            "Kendra para indexar y recuperar pasajes, con logica propia y citas por separado",
            "Una Bedrock Knowledge Base con las guias, invocando RetrieveAndGenerate con citas",
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
        question="Un sistema con SageMaker y Comprehend debe, por compliance, <b>quedar todo en una VPC</b> y bloquear internet con minimo esfuerzo. ¿Que solucion cumple?",
        options=[
            "SageMaker en modo VPC only y VPC peering para acceder a Comprehend en otra VPC",
            "SageMaker en modo VPC only con un internet gateway y security groups restrictivos",
            "Network isolation mode de SageMaker y un VPC endpoint para Comprehend en la misma VPC",
            "SageMaker en modo VPC only con una NACL que bloquee internet y permita a Comprehend",
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
        question="Un modelo XGBoost de SageMaker tiene AUC alto en train pero cae en validacion; Clarify indica <b>overfitting</b> por pocas features dominantes. ¿Que cambio de hiperparametro lo reduce mejor?",
        options=[
            "Aumentar max_depth para arboles mas profundos que capturen relaciones raras",
            "Disminuir min_child_weight para que cada hoja se divida con mas facilidad",
            "Aumentar colsample_bytree para que cada arbol use mas features",
            "Disminuir max_depth para limitar la complejidad de los arboles",
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
        question="Se hace fine-tuning de <b>Amazon Titan Text</b> en SageMaker, servido via Bedrock. Compliance exige artefactos cifrados con KMS, llamadas auditables y monitorear latencia cross-region. ¿Que solucion es segura, auditable y observable?",
        options=[
            "Titan con datos en S3 cifrados con KMS, Bedrock con clave del cliente, CloudTrail e InvocationLatency por region",
            "Titan con datos cifrados SSE-S3, un API Gateway frente a Bedrock y Macie para exfiltracion",
            "Titan en Bedrock sin fine-tuning, acceso con roles de IAM y solo CloudTrail",
            "Titan entrenado en SageMaker, exportado a EC2 con volumenes EBS cifrados y AWS Config",
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
        question="Un endpoint real-time de SageMaker sufre latencia alta. Ante <b>eventos de ventas planificados</b> se quiere garantizar capacidad antes de los picos conocidos. ¿Que solucion optimiza el escalado?",
        options=[
            "Una scheduled scaling policy para aumentar la capacidad del endpoint antes de los eventos",
            "Un Lambda para reiniciar el endpoint durante el pico y refrescar instancias",
            "Una step scaling policy que escale segun utilizacion de CPU y memoria",
            "Aumentar el tamaño de instancia del endpoint a un tipo mas grande",
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
        question="Un pipeline de fraude en SageMaker (ingesta por Kinesis Data Streams, DynamoDB, S3) debe <b>cifrar en transito y reposo, controlar acceso y rastrear el rendimiento</b>. ¿Que solucion asegura el flujo y el monitoreo?",
        options=[
            "Cifrado SSE-KMS, roles de IAM para el acceso y CloudWatch para el rendimiento del modelo",
            "Cifrado SSE-S3 y Amazon Macie para descubrir datos expuestos, con roles de IAM",
            "VPC endpoints entre SageMaker, DynamoDB y Kinesis, y CloudTrail para auditar la API",
            "Data Firehose hacia SageMaker y AWS Glue para catalogar, con CloudWatch e IAM",
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
            '<li><b>VPC endpoints + CloudTrail:</b> los VPC endpoints aislan el trafico pero no cifran en reposo con claves gestionadas, y CloudTrail audita actividad de API, no el rendimiento del modelo (eso es CloudWatch).</li>'
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
        question="En SageMaker Automatic Model Tuning muchos jobs debiles siguen corriendo y gastan GPU. Se quiere una estrategia que <b>detenga los ensayos debiles y reasigne recursos</b>. ¿Que estrategia usar?",
        options=[
            "Optimizacion bayesiana para refinar iterativamente el espacio de busqueda",
            "La estrategia Hyperband de SageMaker con detencion temprana de los ensayos debiles",
            "Grid search para evaluar todas las combinaciones sin detencion temprana",
            "Random search para muestrear combinaciones de forma uniforme",
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
        question="Un notebook de SageMaker debe <b>leer de un bucket S3 y escribir en otro distinto</b> de forma segura, con GetObject, PutObject y ListBucket. ¿Que mecanismo conviene para darle permiso?",
        options=[
            "Una bucket policy que autorice al notebook por su ARN sobre esos buckets",
            "Un S3 access point dedicado que controle el acceso del notebook",
            "Adjuntar esos permisos al rol de IAM (execution role) que usa el notebook",
            "Federacion de identidades de IAM para acceso temporal, asumiendo un rol federado",
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
        question="Un equipo necesita visualizar recomendaciones en <b>cuatro dimensiones</b> (interes X, conversion Y, categoria por color, impresiones por grupo) para detectar alto interes con bajas impresiones. ¿Que enfoque cumple mejor?",
        options=[
            "El scatter plot de SageMaker Data Wrangler que colorea la tercera feature, sin separar por la cuarta",
            "El Box Plot de SageMaker Canvas con un patron de relleno para la tercera dimension",
            "El Bar Chart de SageMaker Canvas por categoria, con color y altura para dos features",
            "El scatter plot de SageMaker Canvas con Color by (categoria) y Group by (impresiones)",
        ],
        correct=3,
        key="aip01r-q69",
        answer=(
            '<div class="verdict">Correcta: {{L}} - scatter plot de SageMaker Canvas: Color by = categoria, Group by = impresiones.</div>'
            '<p><b>El problema:</b> representar cuatro dimensiones a la vez (X, Y, mas dos atributos) para hallar productos de alto interes y alta conversion con pocas impresiones.</p>'
            '<p><b>Por que la respuesta sirve (detalle avanzado):</b> segun la doc de AWS, el <b>scatter plot de SageMaker Canvas</b> usa eje X e Y (numericos) para las dos primeras dimensiones, <b>Color by</b> para una tercera feature (categoria) y <b>Group by</b> para una cuarta (genera un scatter separado por cada valor del grupo). Esas cuatro codificaciones cubren las cuatro dimensiones. Canvas NO ofrece codificar una feature por el <b>tamano</b> del punto.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Scatter de Data Wrangler solo con color:</b> mapea la tercera dimension por color pero no separa por la cuarta (Group by), perdiendo una parte del analisis.</li>'
            '<li><b>Box Plot:</b> muestra distribuciones estadisticas (mediana, cuartiles) y solo admite Group by; no relaciona dos variables continuas por punto como el scatter.</li>'
            '<li><b>Bar Chart:</b> usa Group by y Stack by sobre barras; no representa interes y conversion como nube de puntos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Para 4 dimensiones usa el scatter plot de SageMaker Canvas: X, Y y dos codificaciones adicionales (una por color, otra por grupos separados). Canvas NO codifica por tamano de punto; una opcion que diga "tamano" es incorrecta.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-explore-data-visualization.html">docs.aws visualizaciones en SageMaker Canvas</a></div>'
        ),
    ),
    # ------------------------------------------------------------
    # Q72r - Hybrid search (vector + keyword) en OpenSearch
    # ------------------------------------------------------------
    card(
        question="Un RAG con <b>similitud vectorial en OpenSearch</b> omite codigos, protocolos y acronimos exactos. Hay que preservar la relevancia semantica y coincidir con la terminologia precisa. ¿Que solucion cumple mejor?",
        options=[
            "Aumentar los resultados vectoriales y subir el umbral de similitud",
            "Hybrid search: combinar similitud vectorial con recuperacion por palabras clave para terminos exactos",
            "Solo palabras clave con el algoritmo BM25 en OpenSearch para codigos y acronimos exactos",
            "Busqueda semantica en OpenSearch con consultas neuronales por similitud contextual",
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
        question="Se monitorea feedback social (posts en S3) con Rekognition y Kendra. Debe puntuar sentimiento, ver tendencias y <b>alarmar ante umbrales</b> para reaccionar a picos negativos. ¿Que combinacion cumple mejor?",
        options=[
            "Un job de Glue y uno de SageMaker Processing, sentimiento en DynamoDB y dashboards en QuickSight",
            "Lambda al llegar un post a S3 y Comprehend, publicando los puntajes como metricas de CloudWatch con alarmas por umbral",
            "Notificacion de S3 hacia SQS, Comprehend desde la cola y tendencias en QuickSight",
            "Modelo BlazingText en SageMaker invocado por Lambda, resultados en DynamoDB y metrica de CloudWatch",
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
