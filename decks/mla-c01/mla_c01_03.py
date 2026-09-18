#!/usr/bin/env python3
"""
MLA-C01::03 - Preguntas nuevas (deduplicadas).

17 cartas construidas a partir de decks/mla-c01/dedupe/new_to_generate.json.
Son conceptos que NO estan en los decks 01 y 02.

Reglas aplicadas:
- 1 carta por pregunta (solo la MCQ directa, sin refuerzos).
- Exactamente 4 opciones (las 17 fuentes ya venian con 4).
- Espanol, HTML con entidades para acentos, sin em dashes.
- Verdict con {{L}} (nunca hardcodear la letra; el motor baraja y sustituye).
- El frente no filtra la respuesta.
- Cada dorso: define terminos, conecta escenario con solucion, refuta CADA
  distractor uno por uno bajo "Por que NO las otras", exam tip y links.
- Distractores near-miss plausibles; longitudes balanceadas entre las 4 opciones.
- key estable y unica: mla03-q<n> usando el numero n de la fuente.
"""
from anki_mcq import card, create

cards = [
    # ============================================================
    # Q3 - XGBoost scale_pos_weight (dataset desbalanceado)
    # ============================================================
    card(
        question="SageMaker XGBoost - una herramienta de diagnostico predice si un paciente tiene una enfermedad. El dataset tiene <b>muchos pacientes sanos y pocos enfermos</b> (clase positiva minoritaria). El modelo identifica bien a los sanos, pero <b>casi nunca detecta a los enfermos</b>. &iquest;Que ajuste mejora la deteccion de la clase minoritaria?",
        options=[
            "Aumentar el hiperparametro <code>scale_pos_weight</code>",
            "Reducir el hiperparametro <code>scale_pos_weight</code>",
            "Reducir el hiperparametro <code>max_depth</code> del arbol",
            "Aumentar la tasa de aprendizaje (<code>learning rate</code>)",
        ],
        correct=0,
        key="mla03-q3",
        answer=(
            '<div class="verdict">Correcta: {{L}} - aumentar <code>scale_pos_weight</code>.</div>'
            '<p><b>El problema:</b> el dataset esta desbalanceado. La clase positiva (pacientes enfermos) esta subrepresentada, asi que el modelo aprende a predecir casi siempre la clase mayoritaria (sanos) y falla al detectar la minoritaria.</p>'
            '<p><b>Por que la respuesta sirve:</b> <code>scale_pos_weight</code> pondera la clase positiva durante el entrenamiento. Al <b>aumentarlo</b> se da mas peso a los positivos, aumentando la penalizacion por clasificar mal a un enfermo. Asi el modelo se vuelve mas sensible a la clase minoritaria.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Reducir <code>scale_pos_weight</code>:</b> da menos peso a la clase positiva, dificulta aun mas detectar enfermos; es lo contrario de lo pedido.</li>'
            '<li><b>Reducir <code>max_depth</code>:</b> limita la complejidad del arbol para evitar sobreajuste, pero no ataca el desbalance de clases ni la incapacidad de detectar la clase positiva.</li>'
            '<li><b>Aumentar el learning rate:</b> controla el tama&ntilde;o del paso en la optimizacion y puede acelerar la convergencia, pero no corrige el desbalance de clases.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>En XGBoost con clases desbalanceadas, <code>scale_pos_weight</code> es la palanca directa: subelo para favorecer la clase positiva minoritaria. Una guia comun es fijarlo en (negativos / positivos).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost_hyperparameters.html">docs.aws XGBoost hiperparametros</a></div>'
        ),
    ),
    # ============================================================
    # Q12 - Serverless Inference con provisioned concurrency
    # ============================================================
    card(
        question="Inferencia - un modelo recibe trafico <b>intermitente e impredecible</b>: rafagas cortas de invocaciones separadas por <b>periodos largos sin ninguna peticion</b>. La empresa quiere una solucion <b>totalmente gestionada de SageMaker</b> y pagar <b>solo por lo que se usa</b>, evitando pagar computo mientras no hay trafico. &iquest;Que opcion de inferencia conviene?",
        options=[
            "SageMaker Serverless Inference (bajo demanda, sin provisioned concurrency)",
            "SageMaker Serverless Inference con provisioned concurrency siempre activa",
            "SageMaker Asynchronous Inference con auto scaling y minimo de instancias >= 1",
            "SageMaker Real-time inference sobre un endpoint dedicado con auto scaling",
        ],
        correct=0,
        key="mla03-q12",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Serverless Inference bajo demanda (sin provisioned concurrency).</div>'
            '<p><b>El problema:</b> trafico intermitente e impredecible con largos huecos sin peticiones; se busca una opcion gestionada de SageMaker que cobre por uso y no facture computo cuando no hay trafico.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Serverless Inference</b> aprovisiona y escala la capacidad automaticamente y <b>escala a cero</b> entre rafagas, de modo que se paga solo por el computo de las inferencias y por los datos, sin pagar por tiempo ocioso. Es la opcion mas barata para cargas intermitentes e impredecibles; tolera algun cold start ocasional a cambio de no pagar reserva.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Serverless con provisioned concurrency siempre activa:</b> la PC reserva capacidad "caliente" que se factura de forma continua mientras esta configurada, asi que NO escala a cero ni cumple "pagar solo por lo que se usa"; ademas la PC esta pensada para rafagas PREDECIBLES, no para trafico impredecible.</li>'
            '<li><b>Asynchronous Inference con minimo >= 1 instancia:</b> gestionado, pero al fijar el minimo en 1 hay una instancia siempre activa (costo continuo) y esta pensado para payloads grandes o procesos largos, no para respuestas rapidas ante rafagas.</li>'
            '<li><b>Real-time con endpoint dedicado y auto scaling:</b> tambien es gestionado, pero mantiene al menos una instancia encendida de forma continua, asi que se paga computo aun en los largos periodos sin trafico; no cumple "solo por lo que se usa".</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Trafico intermitente + barato en reposo = Serverless Inference (escala a cero, pagas por uso). Provisioned concurrency = pagas una reserva continua para eliminar cold starts (solo si la latencia es critica y el patron es predecible). Real-time y async mantienen instancias encendidas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html">docs.aws Serverless Inference</a></div>'
        ),
    ),
    # ============================================================
    # Q16 - Transformacion logaritmica (skew a la derecha)
    # ============================================================
    card(
        question="Preprocesamiento - durante la exploracion de datos, una columna numerica esta <b>sesgada a la derecha</b> (right-skewed): una cola larga de valores altos. &iquest;Que tecnica de transformacion mitiga mejor este sesgo?",
        options=[
            "Transformacion logaritmica de la columna",
            "Quantile binning (asignar igual numero de observaciones por bin)",
            "Transformacion de producto cartesiano entre variables",
            "Transformacion de bigrama disperso ortogonal (OSB)",
        ],
        correct=0,
        key="mla03-q16",
        answer=(
            '<div class="verdict">Correcta: {{L}} - transformacion logaritmica.</div>'
            '<p><b>El problema:</b> una distribucion sesgada a la derecha (cola larga hacia valores altos) puede perjudicar a muchos algoritmos de ML que asumen datos mas simetricos.</p>'
            '<p><b>Por que la respuesta sirve:</b> aplicar el <b>logaritmo</b> a la columna comprime los valores grandes y estira los peque&ntilde;os, normalizando la distribucion y haciendola mas simetrica. Es el enfoque clasico para datos numericos con sesgo a la derecha.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Quantile binning:</b> reparte igual numero de observaciones por bin y sirve para categorizar variables continuas, pero no corrige directamente el sesgo de la distribucion.</li>'
            '<li><b>Producto cartesiano:</b> crea features nuevas capturando interacciones entre variables categoricas o de texto; no aplica a datos numericos sesgados.</li>'
            '<li><b>OSB (orthogonal sparse bigram):</b> es para analisis de texto (alternativa al bigrama); no tiene relacion con una columna numerica sesgada.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Sesgo a la derecha en una variable numerica: piensa en log (o raiz/Box-Cox). Binning y transformaciones de texto (OSB, cartesiano) resuelven otros problemas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/machine-learning/latest/dg/data-transformations-reference.html">docs.aws transformaciones de datos</a></div>'
        ),
    ),
    # ============================================================
    # Q18 - k-NN algoritmo built-in supervisado
    # ============================================================
    card(
        question="SageMaker - se tiene un dataset <b>etiquetado</b> con muchas features numericas <b>densas</b> y se quiere un <b>algoritmo integrado supervisado</b> que <b>clasifique por similitud</b> (asignar la clase segun los ejemplos etiquetados mas parecidos) para predecir si un cliente <b>comprara o no</b>. &iquest;Cual conviene?",
        options=[
            "K-nearest neighbors (k-NN) en modo clasificacion",
            "Factorization Machines en modo clasificacion binaria",
            "Linear Learner en modo regresion (<code>predictor_type=regressor</code>)",
            "K-means",
        ],
        correct=0,
        key="mla03-q18",
        answer=(
            '<div class="verdict">Correcta: {{L}} - k-nearest neighbors (k-NN).</div>'
            '<p><b>El problema:</b> clasificar compra si/no <b>por similitud</b> sobre un dataset etiquetado con features numericas densas, usando un algoritmo integrado supervisado.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>k-NN</b> es el algoritmo integrado supervisado basado precisamente en similitud: busca los vecinos mas cercanos de una nueva entrada y asigna la clase segun las etiquetas de esos vecinos. Encaja con "clasificar por similitud" sobre features numericas densas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Factorization Machines (clasificacion binaria):</b> es supervisado y clasifica, pero esta dise&ntilde;ado para datos de alta dimensionalidad y <b>dispersos</b> (esparsos), no para clasificar por similitud sobre features numericas densas como pide el escenario.</li>'
            '<li><b>Linear Learner en modo regresion:</b> Linear Learner es built-in y supervisado, pero en modo regresion predice un valor continuo; no produce la clase compra si/no y no clasifica por similitud.</li>'
            '<li><b>K-means:</b> es no supervisado, agrupa por proximidad (clustering) pero sin usar etiquetas; no realiza clasificacion supervisada.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Clasificar por similitud con datos etiquetados: k-NN. Factorization Machines brilla en datos dispersos de alta dimension; Linear Learner necesita el modo clasificacion (no regresion); K-means es no supervisado.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/k-nearest-neighbors.html">docs.aws algoritmo k-NN</a></div>'
        ),
    ),
    # ============================================================
    # Q23 - SageMaker Pipelines + EventBridge
    # ============================================================
    card(
        question="Orquestacion - hay que procesar mas de <b>5 TB</b> de datos en S3 (CSV, JSON, Parquet y texto plano) en <b>varios pasos consecutivos</b> con manipulaciones complejas que tardan horas, incluyendo transformaciones de NLP, y <b>todo automatizado</b>. &iquest;Que solucion cumple?",
        options=[
            "SageMaker Pipelines para los pasos de procesamiento, automatizado con Amazon EventBridge",
            "Funciones AWS Lambda por paso, orquestadas con AWS Step Functions y EventBridge",
            "SageMaker Data Wrangler por paso, automatizado con jobs de Data Wrangler",
            "Notebooks de SageMaker AI por paso, automatizados con Amazon EventBridge",
        ],
        correct=0,
        key="mla03-q23",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Pipelines + EventBridge.</div>'
            '<p><b>El problema:</b> flujo multi-paso, con datos grandes y heterogeneos, transformaciones complejas de larga duracion (horas) y NLP, y necesidad de automatizacion de extremo a extremo.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>SageMaker Pipelines</b> crea y gestiona flujos de ML a escala, encadenando pasos de procesamiento interconectados que manejan mas de 5 TB en formatos diversos y tareas largas (incluida NLP). Se puede automatizar el disparo con <b>EventBridge</b>. Da escalabilidad, flexibilidad y automatizacion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lambda + Step Functions + EventBridge:</b> Lambda tiene un limite de 15 minutos de ejecucion, insuficiente para pasos que tardan horas.</li>'
            '<li><b>Data Wrangler + jobs:</b> procesa datos tabulares e imagenes, no texto plano, y no esta pensado para flujos complejos de multiples pasos.</li>'
            '<li><b>Notebooks + EventBridge:</b> los notebooks son para experimentacion, no para automatizacion productiva de flujos complejos de procesamiento.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Flujo ML multi-paso, complejo y automatizado: SageMaker Pipelines. Recuerda el limite duro de 15 minutos de Lambda ante tareas de horas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html">docs.aws SageMaker Pipelines</a></div>'
        ),
    ),
    # ============================================================
    # Q28 - Automatic Model Tuning
    # ============================================================
    card(
        question="SageMaker - el rendimiento de un modelo de clasificacion binaria cayo. Hay que <b>ajustar los hiperparametros manteniendo el mismo tipo de modelo</b>, con el <b>MENOR esfuerzo</b> posible. &iquest;Que funcionalidad conviene?",
        options=[
            "SageMaker AI Automatic Model Tuning para buscar los hiperparametros optimos",
            "Un notebook de SageMaker AI con una busqueda aleatoria de hiperparametros propia",
            "SageMaker Autopilot ejecutado con su configuracion por defecto de candidatos",
            "SageMaker Autopilot con <code>TabularJobConfig.ProblemType</code> = BinaryClassification",
        ],
        correct=0,
        key="mla03-q28",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Automatic Model Tuning.</div>'
            '<p><b>El problema:</b> optimizar hiperparametros con minimo esfuerzo <b>sin cambiar el tipo de modelo</b> subyacente.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Automatic Model Tuning</b> automatiza la busqueda de la mejor combinacion de hiperparametros manteniendo fijo el tipo de modelo. Reduce mucho el esfuerzo frente al ajuste manual.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Notebook con busqueda aleatoria propia:</b> exige escribir codigo, gestionar la busqueda y analizar resultados a mano; mas esfuerzo, y random search suele ser menos eficiente.</li>'
            '<li><b>Autopilot por defecto:</b> prueba distintos algoritmos y tipos de modelo para hallar el mejor, por lo que cambiaria el tipo de modelo; incumple el requisito.</li>'
            '<li><b>Autopilot con ProblemType = BinaryClassification:</b> aun asi Autopilot explora varios tipos de modelo; no garantiza mantener el mismo tipo de modelo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Solo optimizar hiperparametros con mismo modelo y minimo esfuerzo: Automatic Model Tuning (HPO). Autopilot cambia de algoritmo/modelo, asi que no aplica cuando el tipo debe quedar fijo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html">docs.aws Automatic Model Tuning</a></div>'
        ),
    ),
    # ============================================================
    # Q31 - Inference components (multi-modelo sin cold start)
    # ============================================================
    card(
        question="Inferencia - varios modelos en instancias aceleradas requieren <b>respuestas en tiempo real</b>, cada uno con <b>requisitos de escalado distintos</b>, y <b>no se permite cold start</b>. &iquest;Que solucion cumple?",
        options=[
            "Un endpoint de SageMaker con un inference component por modelo, cada uno con auto scaling y minimo de copias >= 1",
            "Un unico endpoint de SageMaker real-time que aloja todos los modelos juntos, con auto scaling a nivel de instancia y minimo de instancias >= 1",
            "Un endpoint de SageMaker Asynchronous Inference por modelo, cada uno con su politica de auto scaling",
            "Un endpoint de SageMaker Serverless Inference por modelo, usando provisioned concurrency",
        ],
        correct=0,
        key="mla03-q31",
        answer=(
            '<div class="verdict">Correcta: {{L}} - endpoint con inference components y minimo de copias >= 1.</div>'
            '<p><b>El problema:</b> tiempo real, instancias aceleradas, escalado independiente <b>por modelo</b> y cero cold start.</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>inference components</b> alojan un modelo cada uno dentro de un endpoint de SageMaker sobre instancias aceleradas. Cada componente tiene su propia politica de auto scaling y su propio numero de copias, asi que <b>escala por modelo</b> (no solo por instancia), cumpliendo los requisitos de escalado distintos. Fijando el <b>minimo de copias en al menos 1</b>, siempre hay una copia activa por modelo, evitando cold starts y sosteniendo el tiempo real.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Endpoint real-time unico con todos los modelos:</b> comparte una misma flota y su auto scaling actua <b>a nivel de instancia</b> para el conjunto; no permite politicas de escalado distintas por modelo como exige el escenario.</li>'
            '<li><b>Asynchronous Inference:</b> esta pensado para cargas asincronas sin respuesta inmediata; no cumple el tiempo real.</li>'
            '<li><b>Serverless Inference:</b> no soporta instancias aceleradas (que el escenario exige) y tolera cold starts.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Muchos modelos con escalado independiente POR modelo, tiempo real y sin cold start sobre instancias aceleradas: inference components (un componente por modelo, cada uno con su auto scaling y min copies >= 1). Un endpoint comun solo escala a nivel de instancia.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html">docs.aws inferencia en tiempo real</a></div>'
        ),
    ),
    # ============================================================
    # Q33 - S3DataDistributionType ShardedByS3Key
    # ============================================================
    card(
        question="SageMaker Training API - se quiere que cada instancia de entrenamiento reciba <b>solo un subconjunto</b> (una particion) de los datos de S3, no la copia completa. &iquest;Que configuracion lo logra?",
        options=[
            "Fijar el campo <code>S3DataDistributionType</code> en <code>ShardedByS3Key</code>",
            "Fijar el campo <code>S3DataDistributionType</code> en <code>FullyReplicated</code>",
            "Fijar el campo <code>S3DataType</code> en <code>ShardedByS3Key</code>",
            "Fijar el campo <code>S3Uri</code> en <code>FullyReplicated</code>",
        ],
        correct=0,
        key="mla03-q33",
        answer=(
            '<div class="verdict">Correcta: {{L}} - <code>S3DataDistributionType = ShardedByS3Key</code>.</div>'
            '<p><b>El problema:</b> repartir (shardear) los datos entre las instancias para que cada una entrene con una parte distinta, no con el dataset completo.</p>'
            '<p><b>Por que la respuesta sirve:</b> <code>S3DataDistributionType</code> define como se distribuyen los datos entre instancias. Con <code>ShardedByS3Key</code> cada instancia recibe una particion distinta segun la clave de S3, cumpliendo el requisito del subconjunto.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b><code>S3DataDistributionType</code> = FullyReplicated:</b> replica el dataset entero en cada instancia; es lo opuesto a repartir un subconjunto.</li>'
            '<li><b><code>S3DataType</code> = ShardedByS3Key:</b> campo equivocado; ShardedByS3Key pertenece a <code>S3DataDistributionType</code>, no a <code>S3DataType</code>.</li>'
            '<li><b><code>S3Uri</code> = FullyReplicated:</b> <code>S3Uri</code> indica la ubicacion de los datos, no el modo de distribucion; el valor no corresponde a ese campo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Repartir datos entre instancias = <code>S3DataDistributionType: ShardedByS3Key</code>. Copia completa en cada una = <code>FullyReplicated</code>. Cuida no confundir el campo con <code>S3DataType</code> o <code>S3Uri</code>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_S3DataSource.html">docs.aws S3DataSource</a></div>'
        ),
    ),
    # ============================================================
    # Q34 - BLEU score (traduccion seq2seq)
    # ============================================================
    card(
        question="Evaluacion - se comparan dos modelos de <b>traduccion automatica</b> (SageMaker seq2seq) que traducen articulos de noticias a varios idiomas. &iquest;Que metrica conviene usar para comparar su calidad?",
        options=[
            "BLEU (bilingual evaluation understudy) score",
            "F1 score",
            "Recall",
            "RMSE (root mean square error)",
        ],
        correct=0,
        key="mla03-q34",
        answer=(
            '<div class="verdict">Correcta: {{L}} - BLEU score.</div>'
            '<p><b>El problema:</b> medir la calidad de una traduccion automatica, comparando la salida del modelo con traducciones de referencia.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>BLEU</b> es la metrica estandar para evaluar traduccion automatica: compara la salida del modelo con una o mas referencias humanas y puntua la coincidencia. Es la adecuada para comparar los dos modelos de traduccion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>F1 score:</b> equilibra precision y recall en clasificacion (tipicamente binaria); no evalua la calidad de una traduccion.</li>'
            '<li><b>Recall:</b> mide la proporcion de positivos reales detectados en clasificacion; no aplica a traduccion.</li>'
            '<li><b>RMSE:</b> sirve para modelos de regresion (error sobre valores continuos); no se usa para comparar traducciones.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Traduccion automatica: BLEU. Clasificacion: F1/precision/recall. Regresion: RMSE/MAE. Empareja siempre la metrica con el tipo de tarea.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/seq-2-seq.html">docs.aws seq2seq y BLEU</a></div>'
        ),
    ),
    # ============================================================
    # Q35 - SageMaker Savings Plan (carga constante)
    # ============================================================
    card(
        question="Costos - jobs de entrenamiento en SageMaker sobre una instancia compute optimized, con demanda <b>constante durante 55 semanas</b> (35 horas por semana). Hay que <b>reducir el costo de entrenamiento</b>. &iquest;Que solucion conviene?",
        options=[
            "Un SageMaker AI Savings Plan a 1 a&ntilde;o con pago All Upfront",
            "Un SageMaker Training Plan que reserve la instancia compute optimized",
            "La funcion de heterogeneous cluster de SageMaker Training para los jobs",
            "Un endpoint serverless con provisioned concurrency de 35 horas por semana",
        ],
        correct=0,
        key="mla03-q35",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker AI Savings Plan a 1 a&ntilde;o, All Upfront.</div>'
            '<p><b>El problema:</b> patron de uso predecible y sostenido (35 h/semana por 55 semanas); el objetivo es abaratar el entrenamiento.</p>'
            '<p><b>Por que la respuesta sirve:</b> los <b>SageMaker AI Savings Plans</b> dan descuento a cambio de un compromiso de uso constante por 1 o 3 a&ntilde;os. Con un uso predecible como el descrito, un plan a 1 a&ntilde;o con <b>All Upfront</b> maximiza el descuento sobre el costo de entrenamiento.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SageMaker Training Plan:</b> reserva capacidad de GPU, pero no soporta instancias compute optimized (tipo C) como la del escenario.</li>'
            '<li><b>Heterogeneous cluster:</b> combina varios tipos de instancia para optimizar recursos, pero no aporta ahorro para una carga predecible y sostenida.</li>'
            '<li><b>Endpoint serverless con provisioned concurrency:</b> serverless inference es para servir modelos (deployment), no para correr training jobs.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Uso predecible y sostenido a largo plazo: Savings Plan (1 o 3 a&ntilde;os). Training Plan reserva GPU; serverless es para inferencia, no entrenamiento.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/savings-plans.html">docs.aws SageMaker Savings Plans</a></div>'
        ),
    ),
    # ============================================================
    # Q43 - Amazon Kendra Retrieve API para RAG
    # ============================================================
    card(
        question="GenAI - una empresa <b>ya tiene un indice de busqueda semantica empresarial de Amazon Kendra</b> alimentado, mediante conectores, por sus fuentes internas (SharePoint, S3, wikis) con miles de documentos legales. Quiere <b>hacer consultas en lenguaje natural y generar respuestas</b> reutilizando ese indice existente. &iquest;Que solucion recupera los fragmentos relevantes y los pasa a un modelo para la respuesta generativa?",
        options=[
            "Usar la Retrieve API de Amazon Kendra para obtener los fragmentos relevantes del indice existente y pasarlos a un modelo de lenguaje para la respuesta",
            "Hacer fine-tuning de un modelo fundacional en Amazon Bedrock con los documentos legales para que memorice su contenido y responda las consultas",
            "Usar Amazon Comprehend (reconocimiento de entidades) para identificar los fragmentos y pasarlos a un modelo de lenguaje",
            "Usar la consola de Amazon Lex para crear un bot que consulte los documentos y devuelva fragmentos y respuestas generativas",
        ],
        correct=0,
        key="mla03-q43",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Kendra Retrieve API + modelo de lenguaje.</div>'
            '<p><b>El problema:</b> patron RAG (retrieval augmented generation) reutilizando un indice de <b>Kendra ya existente</b>: primero recuperar los pasajes relevantes, luego generar la respuesta con un LLM.</p>'
            '<p><b>Por que la respuesta sirve:</b> como ya hay un indice de busqueda semantica empresarial en <b>Amazon Kendra</b> (con conectores a las fuentes internas), su <b>Retrieve API</b> devuelve directamente los fragmentos mas relevantes de ese indice, que luego se pasan a un modelo de lenguaje para producir la respuesta. Cubre recuperacion + generacion sin reindexar ni montar infraestructura nueva.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Fine-tuning de un modelo en Bedrock:</b> el fine-tuning adapta el estilo o formato del modelo, no es un mecanismo de recuperacion de documentos; no devuelve fragmentos citables, es costoso de reentrenar ante cada cambio y desaprovecha el indice de Kendra ya existente.</li>'
            '<li><b>Amazon Comprehend (entidades):</b> el reconocimiento de entidades identifica entidades concretas (nombres, fechas), no devuelve los pasajes relevantes para responder una consulta en lenguaje natural.</li>'
            '<li><b>Amazon Lex:</b> construye interfaces conversacionales por intents; no es una solucion de recuperacion documental semantica y aun necesitaria integraciones adicionales.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Si ya existe busqueda semantica empresarial en Kendra, el RAG natural es Retrieve API de Kendra + un LLM. El fine-tuning no recupera documentos; sirve para adaptar el comportamiento del modelo, no para buscar en tu corpus.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/kendra/latest/APIReference/API_Retrieve.html">docs.aws Kendra Retrieve API</a></div>'
        ),
    ),
    # ============================================================
    # Q45 - keep_alive_period_in_seconds (managed warm pools)
    # ============================================================
    card(
        question="Entrenamiento - miles de training jobs cortos con la <b>misma configuracion</b>; cada uno debe <b>arrancar en cuanto termina el anterior</b>, y algunos dias <b>no se ejecuta ninguno</b>. Se busca la opcion MAS rentable. &iquest;Cual conviene?",
        options=[
            "Crear training jobs de SageMaker AI y fijar <code>keep_alive_period_in_seconds</code> en cada job",
            "Crear un job de AWS Batch con EC2 Spot Instances y encolar los jobs con scheduling FIFO",
            "Crear un cluster de SageMaker HyperPod y encolar los jobs con Slurm",
            "Crear un cluster de Amazon EKS con AWS Fargate y encolar los jobs con Apache Airflow",
        ],
        correct=0,
        key="mla03-q45",
        answer=(
            '<div class="verdict">Correcta: {{L}} - training jobs con <code>keep_alive_period_in_seconds</code>.</div>'
            '<p><b>El problema:</b> muchos jobs cortos y secuenciales que deben arrancar de inmediato uno tras otro, con dias de cero actividad; hay que minimizar costo.</p>'
            '<p><b>Por que la respuesta sirve:</b> <code>keep_alive_period_in_seconds</code> activa los <b>managed warm pools</b> de SageMaker: mantiene el cluster caliente entre jobs para que cada uno arranque enseguida. Es serverless y solo se paga por el tiempo activo del job o el warm pool en espera, ideal para cargas intermitentes; en dias sin jobs no hay costo persistente.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>AWS Batch con Spot:</b> las Spot pueden interrumpirse, causando retrasos entre jobs; no garantiza el arranque inmediato tras el anterior.</li>'
            '<li><b>SageMaker HyperPod con Slurm:</b> pensado para entornos persistentes de larga duracion; sigue costando aunque este ocioso, poco rentable con dias sin jobs.</li>'
            '<li><b>EKS con Fargate y Airflow:</b> el cluster sigue corriendo y generando costo incluso los dias sin training jobs; no es lo mas rentable.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Jobs cortos y secuenciales con arranque inmediato y dias ociosos: warm pools via <code>keep_alive_period_in_seconds</code>. Clusters persistentes (HyperPod, EKS) cuestan aun ociosos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/train-warm-pools.html">docs.aws managed warm pools</a></div>'
        ),
    ),
    # ============================================================
    # Q51 - Amazon Polly + SSML
    # ============================================================
    card(
        question="Text-to-speech - hay que generar un podcast de audio a partir de guiones escritos, introduciendo una <b>pausa unica despues de cada parrafo</b>. &iquest;Que solucion cumple?",
        options=[
            "Usar Amazon Polly y definir las pausas con SSML (etiqueta <code>&lt;break&gt;</code>)",
            "Usar Amazon Polly y definir las pausas con lexicons de pronunciacion",
            "Usar Amazon Polly y definir las pausas ajustando el atributo <code>rate</code> de <code>&lt;prosody&gt;</code>",
            "Usar Amazon Polly y definir las pausas con speech marks en la salida",
        ],
        correct=0,
        key="mla03-q51",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Polly con SSML (<code>&lt;break&gt;</code>).</div>'
            '<p><b>El problema:</b> convertir guiones a voz con Amazon Polly e insertar una pausa unica y controlada tras cada parrafo.</p>'
            '<p><b>Por que la respuesta sirve:</b> en <b>SSML</b>, la etiqueta <code>&lt;break&gt;</code> inserta una pausa de duracion definida en el punto exacto donde se coloca. Poniendola al final de cada parrafo se logra la pausa unica pedida. Es el mecanismo directo de Polly para pausas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Lexicons de pronunciacion:</b> los lexicons de Polly personalizan como se pronuncian palabras concretas (siglas, nombres), no insertan pausas ni controlan el ritmo entre parrafos.</li>'
            '<li><b>Atributo <code>rate</code> de <code>&lt;prosody&gt;</code>:</b> ajusta la <b>velocidad</b> del habla, no agrega una pausa; acelerar o frenar no equivale a insertar un silencio tras cada parrafo.</li>'
            '<li><b>Speech marks:</b> son metadatos que Polly emite sobre la salida (posicion de palabras, visemas) para sincronizar; describen el audio, no lo modifican ni insertan pausas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>En Polly, para una pausa usa SSML <code>&lt;break&gt;</code>. <code>&lt;prosody rate&gt;</code> cambia la velocidad, los lexicons cambian pronunciacion y los speech marks solo describen la salida.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html">docs.aws Polly SSML tags</a></div>'
        ),
    ),
    # ============================================================
    # Q52 - Comprehend PII job asincrono
    # ============================================================
    card(
        question="PII - hay cientos de curriculums en PDF en S3 cada dia. Se necesita una solucion automatizada y escalable que <b>detecte y extraiga informacion personal identificable (PII)</b> de esos PDF y guarde el resultado de vuelta en S3. &iquest;Que solucion cumple?",
        options=[
            "Crear un analysis job asincrono de deteccion de PII de Amazon Comprehend (<code>StartPiiEntitiesDetectionJob</code>) sobre el prefijo de S3",
            "Llamar de forma sincrona a <code>DetectPiiEntities</code> de Amazon Comprehend una vez por documento desde una funcion Lambda",
            "Usar Amazon Macie para descubrir PII en los objetos del bucket S3",
            "Usar Amazon Textract para extraer el texto de los PDF y tomar ese texto como las entidades PII",
        ],
        correct=0,
        key="mla03-q52",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Comprehend analysis job asincrono de PII.</div>'
            '<p><b>El problema:</b> detectar y extraer PII de cientos de PDF por dia de forma automatizada y escalable, y devolver el resultado a S3.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Amazon Comprehend</b> es un servicio de NLP que detecta (y puede redactar) PII, incluso en PDF. El <b>analysis job asincrono</b> (<code>StartPiiEntitiesDetectionJob</code>) procesa por lote todos los documentos de un prefijo de S3 y escribe los resultados de vuelta al bucket; encaja con el volumen diario y la necesidad de automatizacion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Comprehend <code>DetectPiiEntities</code> sincrono por documento:</b> es la API en tiempo real para un unico documento de texto; no procesa lotes de PDF en S3 y obliga a orquestar cientos de llamadas a mano, menos escalable que el analysis job.</li>'
            '<li><b>Amazon Macie:</b> descubre datos sensibles (incluida PII) en objetos de S3 y reporta hallazgos, pero esta orientado a seguridad/postura de datos; no extrae las entidades PII documento a documento como salida de procesamiento para este flujo de NLP.</li>'
            '<li><b>Amazon Textract:</b> extrae el texto de los PDF, pero por si mismo no identifica cuales fragmentos son PII; entregaria texto crudo, no las entidades PII pedidas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>PII en muchos documentos/PDF a escala: Comprehend analysis job asincrono. <code>DetectPiiEntities</code> es sincrono y por documento; Macie descubre PII en S3 con enfoque de seguridad; Textract solo extrae texto.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html">docs.aws Comprehend deteccion de PII</a></div>'
        ),
    ),
    # ============================================================
    # Q54 - SageMaker Model Registry collections
    # ============================================================
    card(
        question="Model Registry - hay que organizar modelos existentes (en model groups) en tres categorias (vision, NLP, reconocimiento de voz) para mejorar su descubribilidad a escala, <b>sin afectar la integridad de los artefactos ni los agrupamientos existentes</b>. &iquest;Que solucion cumple?",
        options=[
            "Crear una collection del SageMaker Model Registry por categoria y mover los model groups existentes a las collections",
            "Crear un model group por categoria y mover los modelos existentes a esos nuevos grupos",
            "Crear un tag personalizado por categoria y agregarlo a los model packages del Model Registry",
            "Usar SageMaker ML Lineage Tracking para identificar y etiquetar automaticamente a que grupo pertenece cada modelo",
        ],
        correct=0,
        key="mla03-q54",
        answer=(
            '<div class="verdict">Correcta: {{L}} - collections del Model Registry.</div>'
            '<p><b>El problema:</b> categorizar modelos para descubrirlos mejor a escala, sin romper los agrupamientos existentes ni tocar los artefactos.</p>'
            '<p><b>Por que la respuesta sirve:</b> las <b>collections</b> del SageMaker Model Registry estan dise&ntilde;adas para organizar model groups en categorias logicas <b>sin alterar su estructura existente</b>. Preservan las relaciones actuales y mejoran la descubribilidad a escala.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Crear nuevos model groups y mover modelos:</b> alteraria la organizacion actual y la integridad de los agrupamientos existentes.</li>'
            '<li><b>Tags personalizados en los model packages:</b> aunque etiquetar es posible, hacerlo a mano es manual y fragil (etiquetas inconsistentes, sin garantia de que alguien las mantenga) y <b>no crea una jerarquia navegable y descubrible</b> como si lo hacen las Collections; filtrar por tag no equivale a organizar y explorar por categorias a escala.</li>'
            '<li><b>ML Lineage Tracking:</b> rastrea relaciones y dependencias entre artefactos; no sirve para categorizar modelos ni crear jerarquias de descubribilidad.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Agrupar model groups en categorias sin tocar su estructura: collections del Model Registry. Lineage Tracking es para linaje, no para organizar por categorias.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-collections.html">docs.aws Model Registry collections</a></div>'
        ),
    ),
    # ============================================================
    # Q55 - OPT_OUT_TRACKING metadata SageMaker
    # ============================================================
    card(
        question="Privacidad - la empresa no quiere que SageMaker AI <b>recolecte metadata sobre el uso de las librerias provistas por AWS</b> durante los training jobs. &iquest;Que debe hacer en la API CreateTrainingJob?",
        options=[
            "Fijar la variable de entorno <code>OPT_OUT_TRACKING</code> en <code>1</code>",
            "Fijar la variable de entorno <code>OPT_OUT_TRACKING</code> en <code>0</code>",
            "Deshabilitar el uso de VPC en SageMaker AI mediante la opcion <code>VpcConfig</code>",
            "Configurar como privada la subnet usada por SageMaker AI mediante la opcion <code>VpcConfig</code>",
        ],
        correct=0,
        key="mla03-q55",
        answer=(
            '<div class="verdict">Correcta: {{L}} - <code>OPT_OUT_TRACKING = 1</code>.</div>'
            '<p><b>El problema:</b> impedir que SageMaker recolecte metadata sobre el uso de las librerias provistas por AWS en los training jobs.</p>'
            '<p><b>Por que la respuesta sirve:</b> fijar la variable de entorno <code>OPT_OUT_TRACKING = 1</code> en CreateTrainingJob hace explicitamente el opt-out de la recoleccion de metadata sobre esas librerias. Es la palanca directa para el requisito.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b><code>OPT_OUT_TRACKING = 0</code>:</b> permite explicitamente la recoleccion; es lo contrario de lo pedido (para opt-out debe ser 1).</li>'
            '<li><b>Deshabilitar VPC con <code>VpcConfig</code>:</b> cambia la configuracion de red, pero no afecta la recoleccion de metadata de las librerias.</li>'
            '<li><b>Subnet privada con <code>VpcConfig</code>:</b> aisla la red por seguridad, pero no impide la recoleccion de metadata.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Opt-out de tracking de librerias AWS en SageMaker: <code>OPT_OUT_TRACKING = 1</code>. La configuracion de VPC es de red, no de recoleccion de metadata.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-protection.html">docs.aws privacidad de datos en SageMaker</a></div>'
        ),
    ),
    # ============================================================
    # Q64 - Asynchronous Inference (payload grande)
    # ============================================================
    card(
        question="Inferencia - despliegue en produccion en un endpoint de SageMaker. El payload promedio varia entre <b>100 MB y 300 MB</b>, las peticiones deben procesarse en <b>60 minutos o menos</b> y el endpoint debe <b>ser persistente</b>. &iquest;Que opcion de inferencia cumple?",
        options=[
            "Asynchronous inference",
            "Real-time inference",
            "Batch transform",
            "Serverless inference",
        ],
        correct=0,
        key="mla03-q64",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Asynchronous inference.</div>'
            '<p><b>El problema:</b> payloads grandes (100 a 300 MB), procesos que pueden durar hasta 60 minutos y necesidad de un endpoint persistente.</p>'
            '<p><b>Por que la respuesta sirve:</b> <b>Asynchronous inference</b> admite payloads de hasta 1 GB (cubre 100 a 300 MB) y procesos largos de hasta 1 hora (cubre los 60 minutos), sobre un endpoint persistente. Es ideal cuando no se necesita respuesta inmediata y los payloads son grandes.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Real-time inference:</b> timeout de 60 segundos y payload maximo de 6 MB; no cubre 100 a 300 MB ni procesos largos.</li>'
            '<li><b>Batch transform:</b> sirve para grandes datasets sin endpoint persistente; incumple el requisito de endpoint persistente.</li>'
            '<li><b>Serverless inference:</b> timeout de 60 segundos y payload maximo de 4 MB; muy por debajo del tama&ntilde;o requerido.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Payload grande (hasta 1 GB) y proceso largo (hasta 1 h) con endpoint persistente: Asynchronous inference. Real-time y serverless topan en pocos MB y 60 s.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/async-inference.html">docs.aws Asynchronous Inference</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(
        deck_name="MLA-C01::03",
        cards=cards,
        out_path="out/MLA-C01_03.apkg",
        do_import=False,
    )
