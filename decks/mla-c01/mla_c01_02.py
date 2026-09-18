#!/usr/bin/env python3
"""
MLA-C01::02 - Modeling, Deployment & Ops.

Cartas construidas a partir de 42 preguntas fuente (deck02_source.txt),
cubriendo los dominios ML Model Development, Deployment & Orchestration of ML
Workflows y ML Solution Monitoring, Maintenance & Security.

Reglas aplicadas:
- 1 a 3 cartas por pregunta (siempre la MCQ; cartas de refuerzo de concepto o
  comparacion servicio-vs-servicio solo cuando la explicacion lo justifica).
- Las preguntas "select TWO/THREE" y "order the steps" se convierten a MCQ de
  respuesta unica (que par, que servicio, que paso va primero, etc.).
- Espanol, HTML con entidades, verdict con {{L}} (nunca hardcodear la letra).
- Cada dorso refuta cada distractor uno por uno bajo "Por que NO las otras".
- Opciones balanceadas en longitud (distractores concretos, no rellenos).
- key estable y unica por carta.
"""
from anki_mcq import card, create

cards = [
    # ============================================================
    # Q1 - metricas para deteccion de fraude (dataset desbalanceado)
    # ============================================================
    card(
        question="Deteccion de fraude - solo el <b>3%</b> de las transacciones son fraudulentas. Se busca el <b>par de metricas de evaluacion</b> que a la vez (a) <b>controle la tasa de falsos positivos</b> sobre las transacciones legitimas y (b) de un <b>balance global entre precision y recall robusto al desbalance</b>. (Nota: el <i>cut-off</i> es un umbral de decision, no una metrica de evaluacion.) &iquest;Que par conviene optimizar?",
        options=[
            "False Positive Rate (FPR) y F1 Score (media armonica de Precision y Recall)",
            "Recall (True Positive Rate) y Accuracy global sobre todas las clases",
            "Precision y Accuracy global sobre todas las transacciones",
            "Recall (True Positive Rate) y el valor de Cut-off (umbral de decision)",
        ],
        correct=0,
        key="mla02-q1",
        answer=(
            '<div class="verdict">Correcta: {{L}} - False Positive Rate (FPR) y F1 Score.</div>'
            '<p><b>El problema:</b> el dataset esta muy desbalanceado (3% fraude) y el objetivo doble es detectar fraude sin marcar como fraudulentas demasiadas transacciones genuinas (falsos positivos).</p>'
            '<p><b>Por que sirve:</b> el <b>FPR</b> (False Positive Rate = proporcion de negativos reales clasificados como positivos) controla directamente la tasa de transacciones legitimas marcadas por error, y el <b>F1 Score</b> (media armonica de Precision y Recall) equilibra atrapar fraude real con mantener alta la Precision, ideal en clases desbalanceadas donde Accuracy enga&ntilde;a. El par combina el <b>control de la tasa de falsos positivos (FPR)</b> con el <b>balance entre precision y recall (F1)</b>.</p>'
            '<p><b>Matiz importante:</b> FPR y Precision son <b>complementarias</b>, no rivales. El FPR responde "&iquest;que fraccion de las transacciones legitimas marco por error?" (denominador = negativos reales), mientras que la Precision responde "&iquest;de lo que marque como fraude, cuanto lo era de verdad?" (denominador = predichos positivos). El par elegido cubre ambos angulos: el FPR acota el ruido sobre los clientes legitimos y el F1 (que incorpora la Precision) asegura que el modelo no sacrifique calidad de las alertas ni deteccion de fraude real.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Recall + Accuracy global:</b> con 3% de fraude, un modelo que dice "todo genuino" tiene 97% de Accuracy pero cero utilidad; y el Recall solo mide deteccion de positivos, no limita falsos positivos.</li>'
            '<li><b>Precision + Accuracy global:</b> la Precision si es relevante para falsos positivos, pero emparejarla con Accuracy global la arruina en desbalance (Accuracy enga&ntilde;a); falta una metrica que balancee Recall como hace F1.</li>'
            '<li><b>Recall + Cut-off:</b> el <b>cut-off</b> (umbral) no es una metrica, es la frontera de decision que se ajusta para optimizar metricas; Recall por si solo no limita falsos positivos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>En clases desbalanceadas evita Accuracy. FPR y Precision son complementarias para controlar falsos positivos; el par FPR+F1 combina el control de la tasa de falsos positivos con el balance precision/recall (F1). RMSE/MAE solo para regresion.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/machine-learning/latest/dg/amazon-machine-learning-key-concepts.html">docs.aws ML key concepts</a></div>'
        ),
    ),
    # refuerzo Q1: Precision vs Recall
    card(
        question="Clasificacion - &iquest;que mide la <b>Precision</b> (a diferencia del Recall)?",
        options=[
            "La proporcion de positivos correctos entre todos los que el modelo predijo como positivos",
            "La proporcion de positivos reales que el modelo logro detectar (sensibilidad)",
            "La proporcion de predicciones correctas entre el total de predicciones hechas",
            "La proporcion de negativos reales clasificados erroneamente como positivos",
        ],
        correct=0,
        key="mla02-q1b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - positivos correctos entre todos los predichos positivos.</div>'
            '<p><b>Definicion:</b> <b>Precision</b> = TP / (TP + FP); importa cuando un falso positivo es costoso (ej. frenado innecesario en conduccion autonoma). <b>Recall</b> = TP / (TP + FN); importa cuando perder un positivo real es grave (fraude, diagnostico).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Positivos reales detectados:</b> esa es la definicion de <b>Recall</b> (sensibilidad), no de Precision.</li>'
            '<li><b>Predicciones correctas sobre el total:</b> esa es la <b>Accuracy</b>.</li>'
            '<li><b>Negativos mal clasificados como positivos:</b> ese es el <b>False Positive Rate</b>.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Precision = "de lo que marque, cuanto acerte". Recall = "de lo que debia atrapar, cuanto atrape". F1 balancea ambas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-accuracy-evaluation.html">docs.aws metricas</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="SageMaker - se necesita <b>identificar un articulo en una imagen y dar su ubicacion</b> (bounding box) en estanterias en tiempo real. &iquest;Que algoritmo integrado conviene?",
        options=[
            "Object Detection - MXNet (detecta y localiza objetos con bounding boxes)",
            "Object2Vec (aprende embeddings vectoriales de objetos discretos para similitud)",
            "K-Means Clustering (agrupa vectores numericos por similitud, no supervisado)",
            "Random Cut Forest (detecta anomalias en series de tiempo y datos tabulares)",
        ],
        correct=0,
        key="mla02-q2",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Object Detection - MXNet.</div>'
            '<p><b>El problema:</b> hay dos capacidades juntas, clasificar el objeto (que es) y localizarlo (donde esta, con caja delimitadora).</p>'
            '<p><b>Por que sirve:</b> <b>Object Detection - MXNet</b> es un algoritmo supervisado que usa el framework SSD (Single Shot multibox Detector) para detectar todas las instancias de objetos en una imagen, asignarles clase con score de confianza y dibujar un <b>bounding box</b>. Cubre exactamente identificar + ubicar.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Object2Vec:</b> aprende embeddings vectoriales de objetos discretos (IDs de usuario o item) para recomendacion o similitud; no procesa imagenes.</li>'
            '<li><b>K-Means:</b> agrupa vectores numericos por similitud; no entiende clases ni cajas en imagenes.</li>'
            '<li><b>Random Cut Forest (RCF):</b> detecta anomalias en series de tiempo o datos tabulares; no localiza objetos en imagenes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Vision en SageMaker: Image Classification = una etiqueta por imagen; Object Detection = varias cajas + clases; Semantic Segmentation = clase por pixel.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/object-detection.html">docs.aws object detection</a></div>'
        ),
    ),
    # refuerzo Q2: comparacion de algoritmos de vision
    card(
        question="SageMaker vision - un vehiculo autonomo necesita etiquetar <b>a nivel de pixel</b> toda la escena (ej. carretera vs peaton vs cielo), no solo localizar objetos. &iquest;Que algoritmo integrado corresponde?",
        options=[
            "Semantic Segmentation (mapa denso que asigna una clase a cada region de la escena)",
            "Image Classification (asigna una unica etiqueta a la imagen completa)",
            "Object Detection - MXNet (dibuja cajas alrededor de objetos)",
            "Object2Vec (aprende embeddings de objetos discretos)",
        ],
        correct=0,
        key="mla02-q2b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Semantic Segmentation.</div>'
            '<p><b>Definiciones:</b> la <b>segmentacion semantica</b> etiqueta cada pixel de la imagen con una clase, produciendo un mapa denso (util en vehiculos autonomos o imagenologia medica).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Image Classification:</b> da una sola etiqueta a toda la imagen, no distingue regiones ni pixeles.</li>'
            '<li><b>Object Detection - MXNet:</b> localiza objetos con cajas rectangulares, no a nivel de pixel.</li>'
            '<li><b>Object2Vec:</b> genera embeddings de objetos discretos para similitud o recomendacion; no procesa imagenes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Granularidad creciente: Classification (imagen) - Detection (caja) - Segmentation (pixel).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html">docs.aws algoritmos integrados</a></div>'
        ),
    ),

    # ============================================================
    # Q3 - inter-container traffic encryption (TLS)
    # ============================================================
    card(
        question="Training job distribuido en SageMaker (healthcare) - hay que <b>cifrar la comunicacion en transito entre nodos</b> del cluster de entrenamiento. &iquest;Que se debe habilitar?",
        options=[
            "Inter-container traffic encryption en el cluster de entrenamiento (usa certificados TLS)",
            "Una clave de AWS KMS junto con AWS Secrets Manager al crear el cluster de entrenamiento",
            "Una clave de AWS Secrets Manager al enviar la solicitud del training job",
            "Cifrado de comunicacion entre nodos dentro de los jobs de batch transform",
        ],
        correct=0,
        key="mla02-q3",
        answer=(
            '<div class="verdict">Correcta: {{L}} - inter-container traffic encryption (TLS) en el cluster de entrenamiento.</div>'
            '<p><b>El problema:</b> en entrenamiento distribuido los nodos intercambian informacion del modelo (pesos, gradientes) por la red; hay que cifrar ese trafico en transito.</p>'
            '<p><b>Por que sirve:</b> el <b>inter-container traffic encryption</b> habilita <b>TLS</b> (Transport Layer Security) entre los contenedores/nodos del training job, protegiendo los datos en transito y cumpliendo requisitos regulatorios.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>KMS + Secrets Manager al crear el cluster:</b> KMS cifra <b>en reposo</b> (S3, artefactos, logs), no el trafico entre nodos; ademas SageMaker aprovisiona el cluster automaticamente, no lo creas manualmente.</li>'
            '<li><b>Secrets Manager en el training job:</b> Secrets Manager almacena credenciales/API keys, no cifra datos en transito.</li>'
            '<li><b>Cifrado entre nodos en batch transform:</b> batch transform es <b>inferencia</b> por lotes, no entrenamiento; el caso pide seguridad del training job.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>En transito = TLS (inter-container encryption). En reposo = KMS. Secrets Manager NO cifra datos, guarda secretos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/encryption-in-transit.html">docs.aws encryption in transit</a></div>'
        ),
    ),
    # refuerzo Q3: KMS vs Secrets Manager vs TLS (roles de cifrado)
    card(
        question="Seguridad en SageMaker - &iquest;que servicio o mecanismo se usa para el <b>cifrado en reposo</b> (datos en S3, artefactos, logs)?",
        options=[
            "AWS KMS (Key Management Service)",
            "TLS mediante inter-container traffic encryption",
            "AWS Secrets Manager con rotacion de claves",
            "AWS Certificate Manager (ACM) para certificados publicos",
        ],
        correct=0,
        key="mla02-q3b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS KMS.</div>'
            '<p><b>Definicion:</b> <b>KMS</b> gestiona claves para cifrar datos <b>en reposo</b> (SSE-KMS en S3, artefactos, volumenes, logs). El cifrado <b>en transito</b> es responsabilidad de TLS.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>TLS (inter-container):</b> cifra datos <b>en transito</b> entre nodos, no en reposo.</li>'
            '<li><b>Secrets Manager:</b> almacena y rota secretos (credenciales, API keys); no cifra datasets en reposo.</li>'
            '<li><b>ACM:</b> gestiona certificados TLS/SSL para endpoints, no cifra datos en reposo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Reposo = KMS. Transito = TLS. Secretos = Secrets Manager. Certificados = ACM. No los mezcles.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/train-encrypt.html">docs.aws train encrypt</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Modelo de <b>forecasting de series de tiempo</b> (temperatura y humedad, valores continuos) en SageMaker. &iquest;Que <b>par de metricas</b> es mas adecuado para evaluarlo?",
        options=[
            "Root Mean Square Error (RMSE) y Average Weighted Quantile Loss (Average wQL)",
            "Area Under the Curve (AUC-ROC) y F1 Score (media armonica de Precision y Recall)",
            "Log loss (cross-entropy) y Area Under the Curve (AUC-ROC de separacion de clases)",
            "F1 Score y Mean Absolute Percentage Error (MAPE, error porcentual promedio)",
        ],
        correct=0,
        key="mla02-q4",
        answer=(
            '<div class="verdict">Correcta: {{L}} - RMSE y Average wQL.</div>'
            '<p><b>El problema:</b> predecir temperatura y humedad es una tarea de <b>regresion</b> (valores continuos), y ademas hay incertidumbre (rangos, cuantiles).</p>'
            '<p><b>Por que sirve:</b> el <b>RMSE</b> (Root Mean Square Error, raiz del promedio de errores al cuadrado) es la metrica estandar de regresion y penaliza mas los errores grandes. El <b>Average wQL</b> (Average Weighted Quantile Loss) evalua pronosticos <b>probabilisticos</b>, midiendo la calidad de cuantiles (ej. percentil 90 de humedad).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>AUC + F1:</b> AUC mide separacion de clases en <b>clasificacion binaria</b> (TPR vs FPR) y F1 es media armonica de Precision/Recall; ninguna evalua exactitud de valores continuos.</li>'
            '<li><b>Log loss + AUC:</b> Log loss penaliza probabilidades de clase y AUC es de clasificacion; no aplican a un pronostico continuo.</li>'
            '<li><b>F1 + MAPE:</b> el par mezcla una metrica de clasificacion (F1) con una de regresion (MAPE); MAPE ademas se distorsiona con valores cercanos a cero y no captura la calidad de cuantiles como wQL.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Regresion: RMSE, MAE, MAPE, wQL. Clasificacion: Accuracy, Precision, Recall, F1, AUC, Log loss. Pronostico probabilistico: wQL.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/forecast/latest/dg/metrics.html">docs.aws forecast metrics</a></div>'
        ),
    ),

    # ============================================================
    # Q5 - visualizaciones (bar/histogram/heatmap vs density plot)
    # ============================================================
    card(
        question="Analisis de compras - se quiere <b>comparar cuantas veces se compro cada articulo</b> del catalogo en un periodo. &iquest;Que visualizacion es la adecuada?",
        options=[
            "Bar chart (una barra por articulo, altura = su valor)",
            "Histogram (agrupa datos continuos en bins de rango)",
            "Density plot (curva suave de densidad de una variable continua)",
            "Heatmap (intensidad de color para datos bidimensionales)",
        ],
        correct=0,
        key="mla02-q5",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bar chart.</div>'
            '<p><b>Por que sirve:</b> un <b>bar chart</b> (grafico de barras) es ideal para <b>datos categoricos</b>: cada barra es una categoria (ej. producto) y su altura es el conteo o frecuencia, facilitando comparar articulos distintos en un periodo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Histogram:</b> muestra la <b>distribucion de datos continuos</b> agrupados en bins (ej. montos de transaccion), no conteos por categoria discreta.</li>'
            '<li><b>Density plot:</b> curva suave de densidad de una variable continua; no da conteos exactos ni maneja categorias.</li>'
            '<li><b>Heatmap:</b> representa datos <b>bidimensionales</b> con color (ej. categoria vs hora); util para patrones cruzados, no para una simple frecuencia por articulo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Categorico y conteos: bar chart. Distribucion continua: histogram. Patron 2D (categoria x tiempo): heatmap.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/quicksight/latest/user/bar-charts.html">docs.aws bar charts</a></div>'
        ),
    ),
    # refuerzo Q5: histogram vs heatmap
    card(
        question="Analisis de compras - se busca <b>ver como se reparten los montos de transaccion</b> y donde se concentran la mayoria. &iquest;Que visualizacion conviene?",
        options=[
            "Histogram (agrupa los montos en bins y cuenta cuantos caen en cada rango)",
            "Bar chart (compara valores entre articulos discretos del catalogo)",
            "Heatmap (intensidad de color sobre dos dimensiones cruzadas)",
            "Density plot (suaviza la distribucion pero sin conteos exactos por bin)",
        ],
        correct=0,
        key="mla02-q5b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Histogram.</div>'
            '<p><b>Por que sirve:</b> un <b>histograma</b> divide un rango continuo (montos) en <b>bins</b> y cuenta cuantos registros caen en cada uno, revelando concentraciones y la forma de la distribucion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bar chart:</b> compara categorias discretas, no rangos continuos de un mismo atributo.</li>'
            '<li><b>Heatmap:</b> sirve para patrones cruzados de dos dimensiones (ej. hora x item), no para la distribucion de una sola variable continua.</li>'
            '<li><b>Density plot:</b> util para la forma general, pero carece de la precision y los conteos por bin que da el histograma en escenarios de negocio.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Bar chart y histograma se parecen visualmente pero: bar = categorias; histograma = bins de una variable continua.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/quicksight/latest/user/histogram-charts.html">docs.aws histogram charts</a></div>'
        ),
    ),

    # ============================================================
    # Q6 - Random Cut Forest (anomalias en sensores)
    # ============================================================
    card(
        question="Miles de sensores (calidad de aire, temperatura, humedad) con <b>picos inusuales</b>; se necesita un algoritmo integrado de SageMaker para <b>detectar anomalias</b>. &iquest;Cual?",
        options=[
            "Random Cut Forest (RCF), no supervisado para deteccion de anomalias",
            "Principal Component Analysis (PCA), reduccion de dimensionalidad",
            "Neural Topic Model (NTM), modelado de temas en texto",
            "Convolutional Neural Networks (CNN), procesamiento de imagenes",
        ],
        correct=0,
        key="mla02-q6",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Random Cut Forest (RCF).</div>'
            '<p><b>El problema:</b> flujos continuos de sensores con picos que se desvian del patron normal; se busca detectar esos puntos anomalos.</p>'
            '<p><b>Por que sirve:</b> <b>RCF</b> es un algoritmo <b>no supervisado</b> dise&ntilde;ado para identificar puntos que se desvian del patron, ideal para series de tiempo y datos de alta dimension, y se adapta a patrones cambiantes.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>PCA:</b> tecnica de <b>reduccion de dimensionalidad</b> que preserva varianza; no es un detector de anomalias en si.</li>'
            '<li><b>NTM:</b> descubre temas latentes en <b>texto</b>, no aplica a se&ntilde;ales de sensores.</li>'
            '<li><b>CNN:</b> potente en <b>imagenes</b>; no es el algoritmo integrado de anomalias no supervisadas como RCF.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Anomalias en numeros/series = RCF. Anomalias asociadas a IPs = IP Insights.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/randomcutforest.html">docs.aws random cut forest</a></div>'
        ),
    ),
    # refuerzo algoritmos SageMaker: chooser (deriva de Q6/Q8/Q12)
    card(
        question="Algoritmos integrados de SageMaker - &iquest;cual es el uso principal de <b>Principal Component Analysis (PCA)</b>?",
        options=[
            "Reduccion de dimensionalidad preservando la mayor varianza posible",
            "Deteccion no supervisada de anomalias en series de tiempo",
            "Prediccion de un valor continuo a partir de features tabulares",
            "Descubrimiento de temas latentes en colecciones de texto",
        ],
        correct=0,
        key="mla02-q6b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - reduccion de dimensionalidad preservando varianza.</div>'
            '<p><b>Definicion:</b> <b>PCA</b> proyecta los datos sobre componentes principales (ejes ortogonales) para reducir dimensiones conservando la mayor varianza; sirve para extraccion de features o visualizacion.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Anomalias en series de tiempo:</b> eso lo hace <b>Random Cut Forest (RCF)</b>.</li>'
            '<li><b>Predecir valor continuo tabular:</b> eso es regresion, tarea de <b>Linear Learner</b> o XGBoost.</li>'
            '<li><b>Temas latentes en texto:</b> eso lo hace <b>NTM</b> (Neural Topic Model) o LDA.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>PCA = reducir dimensiones. RCF = anomalias. Linear Learner/XGBoost = regresion/clasificacion. NTM/LDA = temas de texto.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html">docs.aws algoritmos integrados</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Amazon Bedrock, la empresa YA tiene el dataset etiquetado en JSONL y el rol IAM listo. Dado esto, &iquest;cual es el <b>primer paso RESTANTE</b> del proceso de personalizacion (fine-tuning) del modelo?",
        options=[
            "Ajustar hiperparametros y crear el fine-tuning job",
            "Analizar resultados revisando metricas de entrenamiento o validacion",
            "Comprar provisioned throughput para el modelo ajustado",
            "Preparar un dataset etiquetado en formato JSONL con ejemplos de fraude",
        ],
        correct=0,
        key="mla02-q7",
        answer=(
            '<div class="verdict">Correcta: {{L}} - ajustar hiperparametros y crear el fine-tuning job.</div>'
            '<p><b>El problema:</b> los prerrequisitos (dataset JSONL, rol IAM) ya estan; por eso el proceso arranca en el entrenamiento, no en la preparacion de datos.</p>'
            '<p><b>Orden correcto:</b> (1) ajustar hiperparametros y crear el fine-tuning job, (2) analizar metricas de entrenamiento/validacion, (3) comprar provisioned throughput y desplegar.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Analizar metricas:</b> ocurre <b>despues</b> de entrenar, no puede ser el primer paso.</li>'
            '<li><b>Comprar provisioned throughput:</b> es el paso final antes de servir en produccion, tras validar el desempe&ntilde;o.</li>'
            '<li><b>Preparar dataset JSONL:</b> ya esta hecho segun el enunciado, no se repite.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Bedrock custom model: preparar datos - fine-tune - evaluar metricas - comprar provisioned throughput - desplegar.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html">docs.aws bedrock custom models</a></div>'
        ),
    ),

    # ============================================================
    # Q8 - IP Insights (anomalias de IPv4)
    # ============================================================
    card(
        question="Logs historicos de trafico de red; objetivo: <b>identificar direcciones IPv4 que se desvian del patron normal</b>. &iquest;Que algoritmo integrado de SageMaker es el mas adecuado?",
        options=[
            "Amazon SageMaker IP Insights",
            "Random Cut Forest (RCF)",
            "Principal Component Analysis (PCA)",
            "K-Means Cluster Algorithm",
        ],
        correct=0,
        key="mla02-q8",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon SageMaker IP Insights.</div>'
            '<p><b>El problema:</b> detectar IPv4 anomalas y sus asociaciones con entidades (usuarios, cuentas), no solo un outlier numerico generico.</p>'
            '<p><b>Por que sirve:</b> <b>IP Insights</b> es no supervisado y esta especificamente optimizado para analizar patrones de uso de <b>IPv4</b> y capturar asociaciones IP-entidad (ej. login desde IP anomala). Se puede desplegar como endpoint en tiempo real o batch.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>RCF:</b> detecta anomalias en datos numericos/series de tiempo, pero no captura asociaciones IP-entidad como IP Insights.</li>'
            '<li><b>PCA:</b> reduce dimensionalidad; no es un detector de IPs anomalas.</li>'
            '<li><b>K-Means:</b> agrupa por distancia a centroides; no esta optimizado para asociaciones de IPv4.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Palabra clave "IPv4"/"direcciones IP" + anomalias = IP Insights, no RCF.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/ip-insights.html">docs.aws ip insights</a></div>'
        ),
    ),

    # ============================================================
    # Q9 - SageMaker Model Cards (documentacion)
    # ============================================================
    card(
        question="Hay 35 modelos en SageMaker y se necesita <b>documentar cada uno</b> (proposito, metricas, contexto de negocio) de forma accesible y con <b>minimo overhead operativo</b>. &iquest;Que usar?",
        options=[
            "SageMaker Model Cards",
            "SageMaker Model Registry",
            "La clase ModelExplainabilityMonitor",
            "Documentacion en S3 consultada con Athena",
        ],
        correct=0,
        key="mla02-q9",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Model Cards.</div>'
            '<p><b>El problema:</b> documentar modelos (proposito, metricas, contexto) de manera estructurada, accesible y sin infraestructura extra ni mantenimiento continuo.</p>'
            '<p><b>Por que sirve:</b> los <b>Model Cards</b> capturan de forma estructurada el fondo, uso previsto, metricas y contexto de negocio de cada modelo, integrados dentro de SageMaker, exportables y compartibles, con minimo setup.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Model Registry:</b> cataloga y gobierna versiones de modelos para despliegue, se enfoca en gobernanza y CI/CD, no en documentacion descriptiva.</li>'
            '<li><b>ModelExplainabilityMonitor:</b> monitorea deriva de atribucion de features en produccion, no crea documentacion estatica.</li>'
            '<li><b>S3 + Athena:</b> a&ntilde;ade complejidad de consultas SQL y no ofrece un formato de documentacion estructurado, aumentando el overhead.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Model Cards = documentacion. Model Registry = versionado/gobernanza. Model Monitor = deriva en produccion.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-cards.html">docs.aws model cards</a></div>'
        ),
    ),

    # ============================================================
    # Q10 - construir knowledge base RAG en Bedrock (primer paso)
    # ============================================================
    card(
        question="Chatbot RAG con Amazon Bedrock. Los registros sanitizados <b>todavia no estan en la nube</b> (aun no existe el bucket de almacenamiento) y hay que armar la knowledge base desde cero. Ordenando el flujo real, &iquest;cual es el <b>primer paso</b>?",
        options=[
            "Crear el bucket de Amazon S3 que alojara los registros sanitizados",
            "Configurar una knowledge base en Bedrock enlazada al bucket S3",
            "Cargar la informacion dentro de la knowledge base ya creada",
            "Crear una instancia de Amazon RDS para alojar las transacciones",
        ],
        correct=0,
        key="mla02-q10",
        answer=(
            '<div class="verdict">Correcta: {{L}} - crear un bucket de Amazon S3.</div>'
            '<p><b>El problema:</b> ordenar los pasos para armar la knowledge base RAG; primero necesitas donde vivan los datos.</p>'
            '<p><b>Orden correcto:</b> (1) crear el bucket S3 para los registros sanitizados, (2) configurar la knowledge base en Bedrock apuntando a ese bucket como data source, (3) cargar la informacion en la knowledge base.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Configurar la knowledge base:</b> es el paso 2, requiere que el bucket ya exista para enlazarlo.</li>'
            '<li><b>Cargar la informacion:</b> es el paso final, cuando ya hay bucket y knowledge base configurados.</li>'
            '<li><b>Crear una instancia RDS:</b> RDS no es una fuente de datos valida para las knowledge bases de Bedrock.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Bedrock KB: la fuente de datos tipica es S3, no RDS ni SNS. Flujo: S3 - KB - ingestar.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws bedrock knowledge base</a></div>'
        ),
    ),

    # ============================================================
    # Q11 - Feature Store: UpdateFeatureGroup + PutRecord
    # ============================================================
    card(
        question="SageMaker Feature Store - se agrega una nueva feature a un feature group con datos historicos y todos los registros (incluidos historicos) deben reflejarla. &iquest;Que <b>par de acciones</b> corresponde?",
        options=[
            "UpdateFeatureGroup para agregar la feature (nombre y tipo) y luego PutRecord para poblar los registros",
            "DeleteFeatureGroup para eliminar el grupo y PutRecord para recrear los registros",
            "Fijar la nueva feature como primary key y reindexar el feature group para propagarla",
            "Reindexar el feature group y usar PutRecord solo en los registros nuevos",
        ],
        correct=0,
        key="mla02-q11",
        answer=(
            '<div class="verdict">Correcta: {{L}} - UpdateFeatureGroup mas PutRecord.</div>'
            '<p><b>El problema:</b> a&ntilde;adir una columna (feature) al grupo sin perder los registros historicos y luego llenar esa columna en todos ellos.</p>'
            '<p><b>Por que sirve:</b> <b>UpdateFeatureGroup</b> agrega la nueva feature (columna) especificando nombre y tipo; luego <b>PutRecord</b> ingiere o sobrescribe registros para poblar el atributo en historicos y nuevos.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DeleteFeatureGroup:</b> borrar el grupo elimina TODOS los registros historicos, lo contrario del requisito.</li>'
            '<li><b>Fijar como primary key:</b> las primary keys son identificadores unicos que no se cambian ni actualizan registros retroactivamente.</li>'
            '<li><b>Reindexar:</b> "reindexar" no es una operacion valida en Feature Store; se actualiza con PutRecord.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Feature = columna, Record = fila. Agregar columna = UpdateFeatureGroup; llenar filas = PutRecord.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-update-feature-group.html">docs.aws update feature group</a></div>'
        ),
    ),
    # refuerzo Q21/Q11: offline vs online store
    card(
        question="SageMaker Feature Store - &iquest;para que sirve el <b>online store</b> (frente al offline store)?",
        options=[
            "Lecturas de baja latencia (sub-segundo) de features para inferencia en tiempo real",
            "Almacenar datos historicos en Amazon S3 para training y batch inference",
            "Ejecutar trabajos de ETL programados para limpiar los datos crudos",
            "Guardar los artefactos del modelo y sus versiones para el despliegue",
        ],
        correct=0,
        key="mla02-q21b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - lecturas de baja latencia para inferencia en tiempo real.</div>'
            '<p><b>Definicion:</b> el <b>online store</b> sirve features con latencia sub-segundo para inferencia en vivo; el <b>offline store</b> guarda el historico en S3 para exploracion, training y batch inference.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Historico en S3:</b> ese es el <b>offline store</b>, no el online.</li>'
            '<li><b>ETL programado:</b> es tarea de AWS Glue u otros, no del online store.</li>'
            '<li><b>Artefactos y versiones del modelo:</b> eso corresponde al Model Registry, no al Feature Store.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Online store = inferencia baja latencia. Offline store = training/batch en S3.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-concepts.html">docs.aws feature store concepts</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Pronosticar <b>precios de vivienda</b> (variable continua) a partir de features tabulares (metros, recamaras, ubicacion, a&ntilde;o). &iquest;Que algoritmo integrado de SageMaker conviene?",
        options=[
            "Linear Learner (regresion y clasificacion sobre datos tabulares)",
            "DeepAR (pronostico de series de tiempo)",
            "Random Cut Forest (deteccion de anomalias)",
            "Convolutional Neural Networks (procesamiento de imagenes)",
        ],
        correct=0,
        key="mla02-q12",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Linear Learner.</div>'
            '<p><b>El problema:</b> predecir un valor continuo (precio) desde features estructuradas; es una tarea de <b>regresion</b> supervisada.</p>'
            '<p><b>Por que sirve:</b> <b>Linear Learner</b> soporta regresion y clasificacion sobre datos tabulares; para regresion aprende la relacion lineal entre features y el valor continuo objetivo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DeepAR:</b> pronostica <b>series de tiempo</b> (valores futuros por temporalidad), no regresion sobre features estaticas.</li>'
            '<li><b>Random Cut Forest:</b> solo detecta anomalias, no hace regresion.</li>'
            '<li><b>CNN:</b> dise&ntilde;ada para imagenes, no para features numericas/categoricas tabulares.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Regresion tabular = Linear Learner o XGBoost. Series de tiempo = DeepAR. Anomalias = RCF.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/linear-learner.html">docs.aws linear learner</a></div>'
        ),
    ),

    # ============================================================
    # Q13 - RAG: OpenSearch vector DB + Bedrock KB con Titan
    # ============================================================
    card(
        question="Chatbot RAG sobre PDFs en S3 con LLMs. &iquest;Que <b>par de soluciones</b> hace buscables las guias operativas para el chatbot?",
        options=[
            "Ingerir los PDFs en una base vectorial de Amazon OpenSearch Service, y crear una knowledge base en Bedrock con Titan Embeddings G1 usando los PDFs en S3",
            "Convertir los PDFs a texto y guardarlos en Amazon Aurora PostgreSQL, y transformarlos con AWS Glue hacia Amazon RDS",
            "Extraer entidades y frases clave con Amazon Comprehend hacia DynamoDB, y transformar los PDFs con AWS Glue hacia RDS",
            "Guardar los PDFs convertidos en Aurora PostgreSQL, y extraer entidades con Comprehend hacia DynamoDB",
        ],
        correct=0,
        key="mla02-q13",
        answer=(
            '<div class="verdict">Correcta: {{L}} - OpenSearch como base vectorial y knowledge base de Bedrock con Titan Embeddings G1.</div>'
            '<p><b>El problema:</b> RAG necesita almacenar embeddings (vectores) y hacer busqueda semantica por similitud sobre los PDFs.</p>'
            '<p><b>Por que sirve:</b> <b>OpenSearch</b> funciona como base <b>vectorial</b> para guardar y recuperar vectores de alta dimension por similitud. Una <b>knowledge base de Bedrock</b> con <b>Titan Embeddings G1</b> convierte el texto de los PDFs en embeddings, habilitando busqueda semantica precisa.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Aurora PostgreSQL (texto plano):</b> una relacional no esta optimizada para busqueda semantica por vectores.</li>'
            '<li><b>Glue hacia RDS:</b> crear tablas para texto es ineficiente y no da recuperacion semantica.</li>'
            '<li><b>Comprehend hacia DynamoDB:</b> guardar solo entidades y frases clave pierde contexto, insuficiente para respuestas RAG precisas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG = embeddings + vector DB. En AWS: Bedrock KB + OpenSearch (o pgvector). Relacional pura no sirve para busqueda semantica.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html">docs.aws opensearch</a></div>'
        ),
    ),
    # refuerzo Q13: rol de los embeddings (Titan) en RAG
    card(
        question="En un flujo RAG, &iquest;cual es el rol de un modelo de <b>embeddings</b> como Amazon Titan Embeddings G1?",
        options=[
            "Convertir el texto en vectores numericos para habilitar la busqueda semantica por similitud",
            "Generar la respuesta final en lenguaje natural a partir del contexto recuperado",
            "Almacenar de forma duradera los documentos originales antes de indexarlos",
            "Orquestar el pipeline de ingesta programando los trabajos de carga de datos",
        ],
        correct=0,
        key="mla02-q13b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - convertir texto en vectores para busqueda semantica.</div>'
            '<p><b>Definicion:</b> un modelo de <b>embeddings</b> transforma texto en <b>vectores</b> de alta dimension; al comparar vectores por similitud se recuperan los fragmentos mas relevantes (la R de RAG).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Generar la respuesta final:</b> eso lo hace el <b>LLM</b> generador, no el modelo de embeddings.</li>'
            '<li><b>Almacenar documentos:</b> eso es tarea de S3; los embeddings no guardan los originales.</li>'
            '<li><b>Orquestar la ingesta:</b> eso corresponde a la knowledge base o a un orquestador, no al embedding.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>RAG: embeddings (vectorizar) - vector DB (recuperar) - LLM (generar). Titan Embeddings vectoriza, no genera.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html">docs.aws bedrock knowledge base</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Conteo de animales en imagenes de dron (detectar y ubicar multiples objetos por escena). &iquest;Que algoritmo integrado de SageMaker es el mas adecuado?",
        options=[
            "Object Detection (dibuja cajas y clasifica multiples objetos por imagen)",
            "Semantic Segmentation (clasifica cada pixel de la imagen)",
            "Image Classification (asigna una unica etiqueta a la imagen completa)",
            "Object2Vec (aprende representaciones vectoriales de objetos)",
        ],
        correct=0,
        key="mla02-q14",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Object Detection.</div>'
            '<p><b>El problema:</b> contar exige detectar y distinguir <b>varias instancias</b> del mismo objeto (animales) en cada imagen.</p>'
            '<p><b>Por que sirve:</b> <b>Object Detection</b> dibuja bounding boxes y clasifica multiples objetos por imagen, incluso en escenas complejas, lo que permite contar individuos.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Semantic Segmentation:</b> etiqueta pixeles por categoria, no separa ni cuenta instancias individuales.</li>'
            '<li><b>Image Classification:</b> da una sola etiqueta a la imagen; no localiza ni cuenta objetos.</li>'
            '<li><b>Object2Vec:</b> aprende embeddings de objetos discretos para similitud/recomendacion; no analiza imagenes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Contar = distinguir instancias = Object Detection. Segmentacion no cuenta instancias por separado.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/object-detection.html">docs.aws object detection</a></div>'
        ),
    ),

    # ============================================================
    # Q15 - FSx for Lustre (HPC/ML alto I/O)
    # ============================================================
    card(
        question="Entrenar deep learning con dataset masivo de video en un file system distribuido, requiriendo <b>alto throughput y baja latencia</b> con lecturas/escrituras intensivas. &iquest;Que almacenamiento conviene?",
        options=[
            "Amazon FSx for Lustre, file system paralelo de HPC/ML que se integra con S3 para entrenamiento distribuido a gran escala",
            "Amazon Elastic File System (EFS) en modo Max I/O, que escala su throughput agregado con el volumen de datos almacenado",
            "Amazon File Cache, cache administrada de baja latencia que acelera el acceso a datos ya le&iacute;dos desde or&iacute;genes remotos",
            "Amazon EBS io2 Block Express, volumen de bloque de alta IOPS y baja latencia atado a una &uacute;nica instancia de c&oacute;mputo",
        ],
        correct=0,
        key="mla02-q15",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon FSx for Lustre.</div>'
            '<p><b>El problema:</b> entrenamiento distribuido con enormes vol&uacute;menes de video en un <b>file system compartido</b> que exige throughput muy alto y baja latencia con I/O intensivo. Varias opciones prometen rendimiento; el matiz es cu&aacute;l es el file system paralelo de HPC.</p>'
            '<p><b>Por que sirve:</b> <b>FSx for Lustre</b> es un file system <b>paralelo</b> dise&ntilde;ado para <b>HPC y ML</b>: cientos de GB/s de throughput, latencias sub-milisegundo y se integra con S3, ideal para entrenamiento distribuido que muchas instancias leen a la vez.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EFS Max I/O:</b> es NFS compartido y escala throughput con el tama&ntilde;o, pero su latencia por operaci&oacute;n es mayor que la de Lustre; no alcanza el rendimiento del file system paralelo de HPC.</li>'
            '<li><b>File Cache:</b> ofrece baja latencia, pero solo acelera datos ya cacheados desde or&iacute;genes; no es el file system primario de alto throughput para todo el dataset de entrenamiento.</li>'
            '<li><b>EBS io2 Block Express:</b> da IOPS altas y baja latencia, pero es de <b>bloque</b> y se adjunta a una sola instancia; no es un file system compartido para entrenamiento distribuido.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>File system paralelo compartido para ML/HPC de alto throughput = FSx for Lustre. NFS compartido general = EFS. Bloque de una instancia = EBS.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html">docs.aws fsx lustre</a></div>'
        ),
    ),

    # ============================================================
    # Q16 - SageMaker vs Comprehend vs Lex (asignacion)
    # ============================================================
    card(
        question="Servicios AWS de ML - &iquest;que servicio es el mas adecuado para <b>analizar feedback de clientes (sentimiento e insights de texto)</b>?",
        options=[
            "Amazon Comprehend (NLP: sentimiento, entidades, frases clave)",
            "Amazon Lex (interfaces conversacionales y chatbots)",
            "Amazon SageMaker AI (construir, entrenar y desplegar modelos propios)",
            "Amazon Rekognition (analisis de imagenes y video)",
        ],
        correct=0,
        key="mla02-q16",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Comprehend.</div>'
            '<p><b>Por que sirve:</b> <b>Comprehend</b> es un servicio de NLP administrado que extrae sentimiento, entidades y frases clave de texto, perfecto para evaluar feedback de clientes sin construir modelos.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Amazon Lex:</b> construye chatbots e interfaces conversacionales; no analiza sentimiento de texto en lote.</li>'
            '<li><b>SageMaker AI:</b> permite construir modelos propios (ej. deteccion de fraude), pero implica mas esfuerzo que un servicio de NLP administrado.</li>'
            '<li><b>Amazon Rekognition:</b> analiza imagenes y video, no texto.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Sentimiento/NLP administrado = Comprehend. Chatbot = Lex. Modelo a medida = SageMaker. Imagen/video = Rekognition.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/tutorial-reviews.html">docs.aws comprehend</a></div>'
        ),
    ),

    # ============================================================
    # Q17 - CodePipeline vs CodeBuild vs CodeDeploy
    # ============================================================
    card(
        question="CI/CD de ML - &iquest;que servicio <b>orquesta todo el proceso</b> de entrenar, probar y desplegar (build, test, deploy) automaticamente ante cada cambio de codigo?",
        options=[
            "AWS CodePipeline (orquesta build, test y deploy de extremo a extremo)",
            "AWS CodeBuild (compila el codigo, corre pruebas y produce artefactos)",
            "AWS CodeDeploy (despliega a EC2/Lambda/on-prem evitando downtime)",
            "AWS CodeArtifact (almacena y comparte paquetes de software)",
        ],
        correct=0,
        key="mla02-q17",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS CodePipeline.</div>'
            '<p><b>Por que sirve:</b> <b>CodePipeline</b> es entrega continua administrada que automatiza y <b>orquesta</b> las fases build, test y deploy cada vez que cambia el codigo, integrando a CodeBuild, CodeDeploy y otros.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CodeBuild:</b> es la fase de <b>build/test</b> (compila y corre pruebas), no orquesta todo el pipeline.</li>'
            '<li><b>CodeDeploy:</b> se encarga de la fase de <b>despliegue</b> (evita downtime), no de la orquestacion completa.</li>'
            '<li><b>CodeArtifact:</b> es un repositorio de paquetes (npm, PyPI, Maven), no orquesta ni construye.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Pipeline = orquestador. Build = compilar/testear. Deploy = liberar. Artifact = repositorio de paquetes.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html">docs.aws codepipeline</a></div>'
        ),
    ),

    # ============================================================
    # Q18 - Canary deployment
    # ============================================================
    card(
        question="Se despliega un modelo XGBoost nuevo enviando <b>un pequeno porcentaje del trafico</b> al nuevo mientras la mayoria sigue con el viejo, para vigilar y poder revertir. &iquest;Que estrategia es?",
        options=[
            "Canary deployment (enruta un subconjunto pequeno al nuevo modelo y monitorea)",
            "Blue/green deployment (cambia todo el trafico de golpe tras probar)",
            "Linear deployment (desplaza trafico de forma gradual y constante)",
            "Shadow deployment (corre el nuevo en paralelo sin afectar trafico real)",
        ],
        correct=0,
        key="mla02-q18",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Canary deployment.</div>'
            '<p><b>El problema:</b> validar el nuevo modelo a peque&ntilde;a escala con trafico real y poder revertir si hay problemas.</p>'
            '<p><b>Por que sirve:</b> el <b>canary</b> despliega la nueva version a un subconjunto peque&ntilde;o del trafico real, permite monitorear metricas y detectar problemas temprano antes de un rollout total.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Blue/green:</b> cambia TODO el trafico de golpe del viejo (blue) al nuevo (green); no es fase inicial peque&ntilde;a.</li>'
            '<li><b>Linear:</b> desplaza trafico gradual y constante, pero sin la fase inicial de evaluacion a escala minima del canary.</li>'
            '<li><b>Shadow:</b> corre el nuevo en paralelo con copias del trafico, sin servir predicciones reales a usuarios.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Canary = arranque peque&ntilde;o. Linear = incremento parejo. Blue/green = switch total. Shadow = espejo sin impacto.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green-canary.html">docs.aws deployment guardrails</a></div>'
        ),
    ),
    # refuerzo Q18: shadow deployment
    card(
        question="Estrategias de despliegue - &iquest;que caracteriza al <b>shadow deployment</b>?",
        options=[
            "Corre la nueva version en paralelo con trafico espejo, sin servir sus respuestas a usuarios reales",
            "Envia un pequeno porcentaje del trafico real a la nueva version y monitorea antes del rollout",
            "Cambia todo el trafico del entorno viejo al nuevo de una sola vez tras las pruebas",
            "Desplaza el trafico de forma gradual y constante del entorno viejo al nuevo",
        ],
        correct=0,
        key="mla02-q18b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - corre en paralelo con trafico espejo sin afectar a usuarios.</div>'
            '<p><b>Definicion:</b> el <b>shadow deployment</b> ejecuta la nueva version recibiendo una copia del trafico real, pero sus respuestas NO se entregan a usuarios; sirve para validar comportamiento sin riesgo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Porcentaje pequeno de trafico real:</b> eso es el <b>canary</b>, que si sirve respuestas.</li>'
            '<li><b>Switch total de una vez:</b> eso es <b>blue/green</b>.</li>'
            '<li><b>Desplazamiento gradual y constante:</b> eso es <b>linear</b>.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Shadow = espejo sin impacto en usuarios. Canary = arranque pequeno real. Blue/green = switch. Linear = incremento parejo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-shadow-deployment.html">docs.aws shadow deployment</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Entrenamiento con datos sensibles que debe estar <b>aislado de redes externas</b> (sin acceso a internet durante el training). &iquest;Que solucion cumple el requisito?",
        options=[
            "Habilitar el modo network isolation de SageMaker AI en el training job",
            "Usar el cifrado en reposo y en transito integrado de SageMaker",
            "Usar SageMaker Canvas con un VPC interface endpoint para bloquear internet",
            "Guardar los datos de entrenamiento en un bucket S3 cifrado con acceso restringido",
        ],
        correct=0,
        key="mla02-q19",
        answer=(
            '<div class="verdict">Correcta: {{L}} - habilitar el modo network isolation de SageMaker AI.</div>'
            '<p><b>El problema:</b> el contenedor de entrenamiento no debe tener acceso a internet durante el proceso (aislamiento de red total).</p>'
            '<p><b>Por que sirve:</b> el <b>network isolation mode</b> ejecuta los training jobs y modelos <b>sin acceso a internet</b>, aislando por completo el entrenamiento de redes externas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Cifrado en reposo/transito:</b> protege los datos pero no aisla la red; el contenedor podria seguir alcanzando internet.</li>'
            '<li><b>SageMaker Canvas + VPC endpoint:</b> Canvas es una interfaz low-code para construir modelos, no garantiza aislamiento de red del entrenamiento.</li>'
            '<li><b>S3 cifrado con acceso restringido:</b> asegura los datos en reposo, no impide que el entorno se comunique con redes externas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Aislar de internet = network isolation mode. Cifrado y VPC endpoints complementan, pero no aislan por si solos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/mkt-algo-model-internet-free.html#mkt-algo-model-internet-free-isolation">docs.aws network isolation</a></div>'
        ),
    ),

    # ============================================================
    # Q20 - Serverless Inference sin Provisioned Concurrency
    # ============================================================
    card(
        question="Modelo de 2 GB con trafico impredecible (picos en horario laboral, casi nulo de noche/fin de semana); debe escalar solo y ser barato en reposo. &iquest;Que despliegue conviene?",
        options=[
            "Endpoint serverless de SageMaker AI SIN Provisioned Concurrency",
            "Endpoint serverless de SageMaker AI CON Provisioned Concurrency",
            "Endpoint real-time de SageMaker AI con auto-scaling habilitado",
            "AWS Lambda alojando el modelo, cargandolo desde S3 en cada invocacion",
        ],
        correct=0,
        key="mla02-q20",
        answer=(
            '<div class="verdict">Correcta: {{L}} - endpoint serverless SIN Provisioned Concurrency.</div>'
            '<p><b>El problema:</b> trafico intermitente con periodos ociosos y necesidad de minimizar costo cuando no hay demanda.</p>'
            '<p><b>Por que sirve:</b> <b>Serverless Inference</b> escala automaticamente y <b>solo cobra por la duracion de la inferencia y los datos</b>, no por tiempo ocioso; sin Provisioned Concurrency tolera cold starts pero es lo mas barato para trafico intermitente.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Serverless CON Provisioned Concurrency:</b> reserva capacidad siempre lista, lo que sube el costo en periodos ociosos.</li>'
            '<li><b>Real-time con auto-scaling:</b> mantiene instancias corriendo aun sin trafico, caro en reposo.</li>'
            '<li><b>Lambda cargando el modelo:</b> aunque una imagen de contenedor de Lambda admite hasta 10 GB (el modelo de 2 GB cabe), Lambda no es un servicio de inferencia ML administrado: cargar 2 GB desde S3 en cada invocacion provoca cold starts largos y latencia, tiene timeout de 15 min y factura por duracion, lo que lo hace ineficiente y no "fully managed" para servir el modelo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Trafico intermitente y barato en reposo = Serverless Inference. Provisioned Concurrency = quitar cold start pero pagar reserva.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/serverless-endpoints.html">docs.aws serverless endpoints</a></div>'
        ),
    ),
    # refuerzo Q20: comparacion opciones de inferencia de SageMaker
    card(
        question="SageMaker inference - &iquest;cual describe mejor el caso ideal del <b>Batch Transform</b> frente a un endpoint real-time o serverless?",
        options=[
            "Inferencia sobre grandes datasets de forma programada, sin endpoint persistente ni tiempo real",
            "Inferencia bajo demanda sin endpoint dedicado, escalando a cero y cobrando solo por invocacion",
            "Servir predicciones en linea 24/7 con instancias siempre encendidas, auto-scaling y baja latencia",
            "Procesar payloads grandes de forma asincrona encolando las solicitudes en un endpoint persistente",
        ],
        correct=0,
        key="mla02-q20b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - inferencia por lotes programada, sin endpoint persistente.</div>'
            '<p><b>Definicion:</b> <b>Batch Transform</b> corre inferencia sobre grandes datasets sin mantener un endpoint vivo; ideal para trabajos programados que pueden durar minutos u horas y no exigen respuesta inmediata.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bajo demanda escalando a cero:</b> describe el <b>Serverless Inference</b>; tambien evita un endpoint 24/7, pero esta pensado para peticiones online cortas de baja latencia, no para procesar un dataset completo en un job programado.</li>'
            '<li><b>Predicciones 24/7 con instancias encendidas:</b> describe el <b>real-time endpoint</b> con auto-scaling.</li>'
            '<li><b>Payloads grandes asincronos en cola:</b> describe el <b>Asynchronous Inference</b> (endpoint persistente con cola), no un job por lotes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Real-time = online 24/7. Serverless = online intermitente, escala a cero. Async = payloads grandes en cola sobre un endpoint. Batch = lote programado sin endpoint.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-deployment.html">docs.aws opciones de despliegue</a></div>'
        ),
    ),

    # ============================================================
    # Q21 - Feature Store: primer paso (definir feature group)
    # ============================================================
    card(
        question="Montar un Feature Store centralizado en SageMaker. Segun el flujo oficial, &iquest;con cual de estas acciones se <b>arranca la configuracion</b> de un feature group para retraining por lotes?",
        options=[
            "Definir un nuevo feature group",
            "Definir el esquema clave-valor de un registro individual",
            "Registrar los features en un catalogo de datos externo",
            "Provisionar un online store de baja latencia para el grupo",
        ],
        correct=0,
        key="mla02-q21",
        answer=(
            '<div class="verdict">Correcta: {{L}} - definir un nuevo feature group.</div>'
            '<p><b>El problema:</b> el <b>feature group</b> es el contenedor logico que agrupa features relacionadas y su metadata; nada puede definirse "dentro" de el hasta que el grupo existe.</p>'
            '<p><b>Orden correcto:</b> (1) definir el feature group, (2) conectar el <b>offline store</b> (historico en S3, para batch), (3) cargar/ingestar los registros por batch.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Definir el esquema de un registro:</b> las definiciones de features (nombre, tipo, record identifier, event time) se declaran <b>al crear el feature group</b>; no es un paso previo suelto.</li>'
            '<li><b>Registrar en un catalogo externo:</b> el offline store del Feature Store ya se cataloga en el Glue Data Catalog automaticamente; no necesitas un catalogo externo aparte, y menos como primer paso.</li>'
            '<li><b>Provisionar un online store:</b> el online store (baja latencia para inferencia) se habilita como opcion del feature group; no aplica al retraining por lotes descrito y presupone el grupo ya creado.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Feature Store: primero el feature group (define features y metadata), luego offline store (S3, training/batch) u online store (inferencia de baja latencia).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-concepts.html">docs.aws feature store concepts</a></div>'
        ),
    ),

    # ============================================================
    # Q22 - CodeArtifact (almacenar paquetes construidos)
    # ============================================================
    card(
        question="En el ciclo CI/CD, &iquest;que servicio AWS <b>almacena y gestiona los paquetes ya construidos</b> (con versionado, formatos npm/PyPI/Maven)?",
        options=[
            "AWS CodeArtifact (repositorio de artefactos y paquetes de software)",
            "AWS CodeDeploy (automatiza despliegues evitando downtime)",
            "AWS CodeBuild (compila el codigo y ejecuta pruebas)",
            "AWS CodePipeline (orquesta el flujo build-test-deploy)",
        ],
        correct=0,
        key="mla02-q22",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS CodeArtifact.</div>'
            '<p><b>Por que sirve:</b> <b>CodeArtifact</b> almacena, publica y comparte paquetes (Maven, npm, PyPI) con control de versiones; tras compilar en CodeBuild, los artefactos se guardan aqui de forma segura.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CodeDeploy:</b> despliega a EC2/Lambda/on-prem evitando downtime, no almacena paquetes.</li>'
            '<li><b>CodeBuild:</b> compila y prueba el codigo, produce los artefactos pero no es su repositorio.</li>'
            '<li><b>CodePipeline:</b> orquesta las fases del pipeline, no guarda paquetes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Artifact = repositorio de paquetes (npm/PyPI/Maven). No confundir con S3 ni con ECR (imagenes de contenedor).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html">docs.aws codeartifact</a></div>'
        ),
    ),

    # ============================================================
    # Q23 - interface VPC endpoint (S3 privado); ambos endpoints regionales
    # ============================================================
    card(
        question="Dataset sensible en un bucket de S3 en la region <b>us-east-1</b>, pero las instancias de entrenamiento de SageMaker corren en una VPC de <b>us-west-2</b> (otra region). El trafico hacia S3 NO debe exponerse a internet publico en ningun momento, sin duplicar los datos ni cambiar de servicio de transferencia. &iquest;Que solucion aporta el acceso privado <b>entre regiones</b>?",
        options=[
            "Deshabilitar el acceso directo a internet y usar un interface endpoint (PrivateLink) combinado con VPC peering / Transit Gateway hacia la VPC de la region del bucket",
            "Deshabilitar el acceso directo a internet y crear un gateway endpoint en la VPC de us-west-2, agregando su prefix list a la tabla de rutas para llegar al bucket",
            "Replicar el bucket con S3 Cross-Region Replication hacia us-west-2 y entrenar el modelo sobre esa copia local dentro de la misma VPC del training job",
            "Usar AWS Transfer Family con un endpoint SFTP para copiar el dataset a un bucket local en us-west-2 de forma segura antes de lanzar el entrenamiento",
        ],
        correct=0,
        key="mla02-q23",
        answer=(
            '<div class="verdict">Correcta: {{L}} - interface endpoint (PrivateLink) con VPC peering / Transit Gateway hacia la region del bucket, sin internet directo.</div>'
            '<p><b>El problema:</b> el training job en us-west-2 debe alcanzar un bucket de S3 en us-east-1 (OTRA region) sin que el trafico salga a internet publico, sin duplicar los datos y sin cambiar de servicio.</p>'
            '<p><b>Por que sirve:</b> un <b>interface VPC endpoint</b> (AWS PrivateLink) crea una <b>ENI con IP privada</b> en tus subredes; como es regional, se combina con conectividad entre regiones (<b>VPC peering</b> o <b>Transit Gateway</b>) para que SageMaker en us-west-2 llegue de forma privada al S3 de us-east-1, sin internet gateway ni NAT. La opcion nombra ambas piezas, por eso es tecnicamente completa y la unica que da acceso privado cross-region sin duplicar datos ni cambiar de servicio.</p>'
            '<p><b>Por que un gateway endpoint NO basta aqui:</b> el gateway endpoint es <b>intra-region</b> y se aplica solo por la <b>tabla de rutas</b> de la VPC hacia el S3 de <b>su propia region</b>. Como el bucket vive en otra region (us-east-1) que la VPC (us-west-2), un gateway endpoint no puede alcanzarlo; ademas no ofrece IP privada/ENI ni acceso desde otra VPC.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Gateway endpoint:</b> es <b>intra-region</b> (solo alcanza el S3 de la propia region via tabla de rutas); con el bucket en us-east-1 y la VPC en us-west-2 no puede llegar, y ademas no da IP privada/ENI ni acceso cross-region.</li>'
            '<li><b>Cross-Region Replication:</b> duplica el dataset (mas costo, storage y tiempo); el requisito es acceder de forma segura, no replicar.</li>'
            '<li><b>AWS Transfer Family (SFTP):</b> es transferencia de archivos, no integra con SageMaker para acceso privado durante el entrenamiento.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Gateway = ruta, gratis, S3/DynamoDB, intra-region. Interface (PrivateLink) = ENI/IP privada, muchos servicios, admite on-prem y otra VPC-region via peering/TGW. Ambos endpoints son regionales.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/interface-vpc-endpoint.html">docs.aws interface vpc endpoint</a></div>'
        ),
    ),
    # refuerzo Q23: gateway vs interface endpoint
    card(
        question="VPC endpoints - &iquest;que diferencia clave hay entre un <b>gateway endpoint</b> y un <b>interface endpoint</b> (PrivateLink)?",
        options=[
            "El gateway endpoint solo soporta S3 y DynamoDB; el interface usa una ENI privada para muchos servicios",
            "El interface endpoint tambien es gratuito y, como el gateway, se aplica por la tabla de rutas",
            "El gateway endpoint da acceso desde on-premises via VPN; el interface queda limitado a la VPC local",
            "El interface endpoint permite acceder a un bucket S3 de otra region por si solo, sin peering ni TGW",
        ],
        correct=0,
        key="mla02-q23b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - gateway solo S3/DynamoDB; interface usa ENI privada y muchos servicios.</div>'
            '<p><b>Definiciones:</b> el <b>gateway endpoint</b> se agrega a la tabla de rutas, es gratuito y solo soporta <b>S3 y DynamoDB</b> dentro de la region; no da IP privada ni acceso on-prem. El <b>interface endpoint</b> (AWS PrivateLink) crea una <b>ENI</b> con IP privada en tus subredes, se cobra por hora, cubre muchos servicios AWS y admite acceso desde on-prem u otra VPC-region via peering/TGW.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Interface gratis y por tabla de rutas:</b> falso; el interface se factura por hora (y por datos) y funciona por una <b>ENI</b>, no por rutas; el que va por rutas y es gratis es el gateway.</li>'
            '<li><b>Gateway con acceso on-prem via VPN:</b> falso; el gateway endpoint NO es accesible desde on-premises; el que admite on-prem es el interface (PrivateLink).</li>'
            '<li><b>Interface cross-region a un bucket remoto por si solo:</b> falso; ambos endpoints son <b>regionales</b>; alcanzar S3 en otra region requiere VPC peering o Transit Gateway hacia una VPC de esa region.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Gateway = ruta, gratis, S3/DynamoDB, intra-region, sin on-prem. Interface = ENI/PrivateLink, IP privada, se cobra por hora, muchos servicios, admite on-prem y otra VPC-region via peering/TGW.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/whitepapers/latest/aws-privatelink/what-are-vpc-endpoints.html">docs.aws vpc endpoints</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Preprocesar texto (limpieza, tokenizacion, embeddings con TensorFlow/HuggingFace) desde S3 con <b>minimo esfuerzo de gestion</b>, disparado al subir datos nuevos. &iquest;Que trio de acciones?",
        options=[
            "Un SageMaker Processing Job para preprocesar y generar embeddings, una Lambda que lo dispare al subir datos a S3, y S3 Event Notifications con Step Functions",
            "Desplegar un cluster ECS en Fargate para los scripts, usar AWS Glue para limpiar el texto, y AWS Batch para orquestar los jobs de embeddings",
            "Usar AWS Glue para limpiar el texto, AWS Batch para ejecutar los Processing Jobs, y un cluster ECS en Fargate para generar embeddings",
            "Usar AWS Batch para gestionar los Processing Jobs, Glue para limpiar el texto, y un cluster EKS para orquestar el flujo de embeddings",
        ],
        correct=0,
        key="mla02-q24",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Processing Job, Lambda como disparador y S3 Event Notifications con Step Functions.</div>'
            '<p><b>El problema:</b> automatizar el preprocesamiento de ML con el menor overhead, arrancando cuando llegan datos nuevos.</p>'
            '<p><b>Por que sirve:</b> el <b>SageMaker Processing Job</b> es administrado y trae soporte para TensorFlow y HuggingFace; <b>Lambda</b> lo dispara automaticamente; las <b>S3 Event Notifications</b> reaccionan a nuevas cargas y activan el workflow. Todo administrado, minimo mantenimiento.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>ECS en Fargate:</b> correr contenedores propios agrega gestion innecesaria frente a Processing Jobs administrados.</li>'
            '<li><b>AWS Glue:</b> es ETL que exige definir esquemas y crawlers, mas overhead para este flujo de ML.</li>'
            '<li><b>AWS Batch / EKS:</b> a&ntilde;aden orquestacion extra; los Processing Jobs se ejecutan directo sin necesidad de Batch ni Kubernetes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Preprocesamiento ML administrado = SageMaker Processing Job. Glue = ETL de datos. "Minimo esfuerzo" descarta ECS/EKS/Batch propios.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html">docs.aws processing job</a></div>'
        ),
    ),

    # ============================================================
    # Q25 - Batch Transform (job diario, costo minimo)
    # ============================================================
    card(
        question="Modelo que corre <b>una vez al dia</b>, el procesamiento toma 45 min y la prioridad es minimizar costo. &iquest;Que despliegue es el mas costo-efectivo?",
        options=[
            "Un job de SageMaker Batch Transform programado a diario",
            "Un endpoint serverless de SageMaker con escalado a cero",
            "Amazon EMR para procesar los datos e invocar el modelo",
            "El ModelExplainabilityMonitor para agendar la inferencia",
        ],
        correct=0,
        key="mla02-q25",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un job de SageMaker Batch Transform.</div>'
            '<p><b>El problema:</b> inferencia programada (1 vez al dia, 45 min), sin necesidad de tiempo real y con foco en costo.</p>'
            '<p><b>Por que sirve:</b> <b>Batch Transform</b> corre inferencia sobre datasets sin mantener un endpoint persistente; se paga solo por el job, evitando costo de un endpoint 24/7. Maneja trabajos de minutos a horas.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Endpoint serverless:</b> esta pensado para trafico impredecible de <b>baja latencia y rafagas cortas</b>, escalando a cero entre picos; no para procesar un dataset completo en un job de 45 min.</li>'
            '<li><b>Amazon EMR:</b> es big data (Hadoop/Spark); mantener un cluster cuesta mas y no es para inferencia programada simple.</li>'
            '<li><b>ModelExplainabilityMonitor:</b> detecta bias/drift de explicabilidad en endpoints, no agenda ni ejecuta inferencia batch.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Job diario/programado, sin tiempo real, barato = Batch Transform. Serverless = online intermitente de baja latencia, no lotes largos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html">docs.aws batch transform</a></div>'
        ),
    ),

    # ============================================================
    # Q26 - cooldown period (auto scaling inestable)
    # ============================================================
    card(
        question="Un endpoint de SageMaker con target tracking sobre CPU escala <b>demasiado seguido</b>, causando inestabilidad. &iquest;Que se debe configurar para resolverlo?",
        options=[
            "Un periodo de enfriamiento (cooldown) entre acciones de escalado",
            "Incrementar el valor objetivo de utilizacion de CPU",
            "Reducir el numero minimo de instancias",
            "Usar una metrica distinta de CloudWatch para el escalado",
        ],
        correct=0,
        key="mla02-q26",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un cooldown period entre acciones de escalado.</div>'
            '<p><b>El problema:</b> el escalado se dispara con demasiada frecuencia (thrashing), sin dar tiempo a estabilizarse.</p>'
            '<p><b>Por que sirve:</b> el <b>cooldown period</b> define cuanto esperar tras una accion de escalado antes de iniciar otra, dando tiempo a la aplicacion para estabilizarse y evitando el escalado excesivo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Subir el target de CPU:</b> puede reducir escalados pero arriesga sub-aprovisionar (instancias sobrecargadas antes de escalar); no ataca la frecuencia.</li>'
            '<li><b>Reducir el minimo de instancias:</b> baja la capacidad base y puede provocar mas escalados, no menos.</li>'
            '<li><b>Cambiar la metrica:</b> ayuda si la metrica es mala, pero el problema es de <b>frecuencia/tiempo</b>, no de que metrica se usa.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Escalado inestable/thrashing = ajustar cooldown period. La metrica no es el problema si el disparo es demasiado frecuente.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling-add-code-define.html#endpoint-auto-scaling-add-code-cooldown">docs.aws cooldown</a></div>'
        ),
    ),

    # ============================================================
    # Q27 - contenedor Docker en ECR (scripts custom en SageMaker)
    # ============================================================
    card(
        question="Un equipo tiene scripts Python propios (con dependencias especificas) y quiere ejecutarlos en SageMaker de forma escalable. &iquest;Como incorporarlos?",
        options=[
            "Crear un contenedor Docker con las dependencias, subirlo a Amazon ECR y usarlo como processing/training container en SageMaker",
            "Guardar los scripts Python en un bucket S3 y ejecutarlos directamente en SageMaker sin empaquetarlos",
            "Crear una funcion Lambda con los scripts propios e invocarla desde SageMaker para el entrenamiento",
            "Crear una imagen de contenedor para Amazon EKS y ejecutar alli los scripts de preprocesamiento",
        ],
        correct=0,
        key="mla02-q27",
        answer=(
            '<div class="verdict">Correcta: {{L}} - contenedor Docker en Amazon ECR usado como container en SageMaker.</div>'
            '<p><b>El problema:</b> ejecutar scripts propios con dependencias exactas dentro del entorno administrado de SageMaker.</p>'
            '<p><b>Por que sirve:</b> SageMaker soporta contenedores <b>Docker</b> a la medida; se empaquetan las dependencias, se sube la imagen a <b>ECR</b> (Elastic Container Registry) y se usa como processing o training container, garantizando el entorno exacto.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Scripts en S3 directamente:</b> S3 es almacenamiento de objetos, no ejecuta codigo; hay que empaquetarlo en un contenedor.</li>'
            '<li><b>Lambda:</b> es para funciones cortas y sin estado, no para flujos de ML complejos ni entrenamiento.</li>'
            '<li><b>EKS:</b> Kubernetes agrega complejidad innecesaria; SageMaker trabaja directamente con Docker/ECR.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Codigo/dependencias propias en SageMaker = imagen Docker en ECR (bring your own container).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/build-your-own-processing-container.html">docs.aws bring your own container</a></div>'
        ),
    ),

    # ============================================================
    # Q28 - CodePipeline como orquestador CI/CD (repetido en otro contexto)
    # ============================================================
    card(
        question="Se busca un servicio que <b>coordine automaticamente las fases build, test y deploy</b> de un proyecto ML en cada cambio de codigo, enlazando los demas servicios del ciclo. &iquest;Cual usar?",
        options=[
            "AWS CodePipeline",
            "AWS CodeBuild",
            "AWS CodeDeploy",
            "AWS Step Functions",
        ],
        correct=0,
        key="mla02-q28",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS CodePipeline.</div>'
            '<p><b>Por que sirve:</b> <b>CodePipeline</b> es el servicio de entrega continua purpose-built para el ciclo de codigo: modela las etapas build-test-deploy y las dispara ante cada cambio, integrando CodeBuild, SageMaker y CodeDeploy de forma nativa.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CodeBuild:</b> es integracion continua (compilar y probar), una pieza del ciclo, no el coordinador de todas las etapas.</li>'
            '<li><b>CodeDeploy:</b> automatiza solo la fase de despliegue.</li>'
            '<li><b>Step Functions:</b> orquesta flujos de trabajo genericos (state machines) y puede coordinar pasos de ML, pero no es el servicio de entrega continua de codigo con etapas source/build/deploy integradas ante cada commit; para CI/CD de codigo el servicio dedicado es CodePipeline.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Entrega continua de codigo (build-test-deploy por commit) = CodePipeline. Orquestacion generica de estados/tareas = Step Functions. CodeBuild = build/test. CodeDeploy = deploy.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html">docs.aws codepipeline</a></div>'
        ),
    ),

    # ============================================================
    # Q29 - metricas de clasificacion binaria (4 correctas)
    # ============================================================
    card(
        question="Clasificacion binaria de calidad (Passed/Failed) con imagenes y video. Se busca el <b>cuarteto de metricas derivadas de la matriz de confusion a un umbral de decision fijo</b> (es decir, metricas de conteo TP/FP/TN/FN, no metricas que barren todos los umbrales como AUC-ROC). &iquest;Que cuarteto es el apropiado?",
        options=[
            "Precision, Recall, Accuracy y F1 Score",
            "Precision, Recall, Especificidad y AUC-ROC",
            "Precision, Recall, Accuracy y R-cuadrado (coeficiente de determinacion)",
            "Precision, Recall, F1 Score y Perplexity",
        ],
        correct=0,
        key="mla02-q29",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Precision, Recall, Accuracy y F1 Score.</div>'
            '<p><b>Definiciones:</b> <b>Precision</b> = positivos correctos entre todos los predichos positivos; <b>Recall</b> = positivos correctos entre todos los positivos reales; <b>Accuracy</b> = predicciones correctas entre el total; <b>F1</b> = media armonica de Precision y Recall. Las cuatro miden desempeno de <b>clasificacion</b> y son las pedidas por la fuente para Passed/Failed.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Precision, Recall, Especificidad, AUC-ROC:</b> las cuatro son de clasificacion, pero <b>AUC-ROC no se deriva de la matriz de confusion a un umbral fijo</b>: barre TODOS los umbrales posibles (area bajo la curva ROC). Por eso queda fuera del cuarteto pedido (metricas de conteo a un umbral fijo); la especificidad si es de matriz de confusion, pero el cuarteto estandar Passed/Failed es Precision/Recall/Accuracy/F1.</li>'
            '<li><b>...con R-cuadrado:</b> el <b>R-cuadrado</b> es una metrica de <b>regresion</b> (varianza explicada de un valor continuo), no aplica a etiquetas discretas Passed/Failed.</li>'
            '<li><b>...con Perplexity:</b> la <b>Perplexity</b> evalua modelos de lenguaje (que tan bien predicen texto), no clasificacion binaria de imagenes/video.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Cuarteto clasico de clasificacion: Precision, Recall, Accuracy, F1. Otras validas: AUC-ROC, especificidad. R-cuadrado=regresion. Perplexity/ROUGE/BLEU=lenguaje/NLP.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-accuracy-evaluation.html">docs.aws evaluacion de accuracy</a></div>'
        ),
    ),

    # ============================================================
    # Q30 - IAM KMS permisos en execution role (SSE-KMS)
    # ============================================================
    card(
        question="Tras cambiar un bucket de SSE-S3 a <b>SSE-KMS</b>, los training jobs fallan con AccessDenied (antes funcionaban). &iquest;Como se corrige?",
        options=[
            "Agregar kms:Decrypt (y kms:GenerateDataKey si escribe salida cifrada) a la IAM policy del execution role del training job",
            "Agregar permisos kms:Decrypt y kms:GenerateDataKey a la IAM policy del usuario que lanzo el job",
            "Agregar s3:ListBucket y s3:GetObject a la IAM policy del execution role del training job",
            "Agregar s3:ListBucket y s3:GetObject a la IAM policy del usuario que inicio el job",
        ],
        correct=0,
        key="mla02-q30",
        answer=(
            '<div class="verdict">Correcta: {{L}} - dar kms:Decrypt al execution role del training job.</div>'
            '<p><b>El problema:</b> el error aparecio justo al cambiar a SSE-KMS; el training job usa el <b>execution role</b>, no las credenciales del usuario. Al leer objetos cifrados con KMS necesita permisos sobre la clave.</p>'
            '<p><b>Por que sirve:</b> para <b>descifrar y leer</b> los datos de entrenamiento cifrados con SSE-KMS, el execution role necesita <code>kms:Decrypt</code>. Si ademas el job <b>escribe salida cifrada</b> (modelo, checkpoints) necesita <code>kms:GenerateDataKey</code>. Nota: <code>kms:Encrypt</code> por si solo NO habilita la lectura.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>KMS al usuario:</b> el job usa el execution role, no las credenciales del usuario; dar KMS al usuario no ayuda.</li>'
            '<li><b>s3:ListBucket/GetObject al role:</b> el job funcionaba antes, asi que ya tenia esos permisos S3; la causa es KMS, no S3.</li>'
            '<li><b>s3:ListBucket/GetObject al usuario:</b> irrelevante por partida doble (permisos S3 ya presentes y en el role, no en el usuario).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>SageMaker actua con su execution role. AccessDenied nuevo tras SSE-KMS = falta permiso sobre la KMS key en el role: kms:Decrypt para leer, kms:GenerateDataKey para escribir salida cifrada.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html">docs.aws SSE-KMS</a></div>'
        ),
    ),

    # ============================================================
    # Q31 - SageMaker Model Monitor (deriva de accuracy)
    # ============================================================
    card(
        question="Se necesita detectar la <b>baja de accuracy del modelo con el tiempo</b> usando datos en vivo (endpoint de SageMaker). &iquest;Que enfoque conviene?",
        options=[
            "Configurar un job de Amazon SageMaker Model Monitor que compare datos en vivo contra baseline y constraints del entrenamiento",
            "Revisar los logs de latencia y utilizacion en CloudWatch para detectar el drift del modelo",
            "Usar EventBridge Scheduler para sondear la Lambda y analizar su salida en busca de drift",
            "Usar AWS Glue para analizar datos de inferencia y crear un pipeline ETL que alerte ante drift",
        ],
        correct=0,
        key="mla02-q31",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un job de SageMaker Model Monitor contra baseline y constraints.</div>'
            '<p><b>El problema:</b> vigilar la deriva de <b>calidad del modelo</b> (accuracy) con datos entrantes en produccion.</p>'
            '<p><b>Por que sirve:</b> <b>Model Monitor</b> monitorea calidad de datos, calidad del modelo (ej. accuracy), bias drift y feature attribution drift, comparando datos en vivo contra el <b>baseline</b> de estadisticas/constraints del entrenamiento.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CloudWatch latencia/utilizacion:</b> mide rendimiento del sistema, no la distribucion de datos ni la accuracy.</li>'
            '<li><b>EventBridge Scheduler + Lambda:</b> dispara por horario pero no analiza estadisticas ni detecta drift por si solo.</li>'
            '<li><b>AWS Glue ETL:</b> es ETL batch, sin comparacion nativa contra baseline de entrenamiento.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Deriva de accuracy/datos en produccion = SageMaker Model Monitor. CloudWatch = rendimiento del sistema, no drift.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html">docs.aws model monitor</a></div>'
        ),
    ),
    # refuerzo Q31/Q38: los 4 tipos de monitoreo de Model Monitor
    card(
        question="SageMaker Model Monitor expone <b>cuatro</b> tipos oficiales de monitoreo: data quality, model quality, bias drift y feature attribution drift. De las siguientes opciones, &iquest;cual <b>NO</b> es uno de esos cuatro tipos (es el intruso)?",
        options=[
            "Concept drift (deriva en la relacion entre las features y la etiqueta objetivo)",
            "Data quality drift (deriva en la distribucion/calidad de los datos de entrada)",
            "Model quality drift (deriva en metricas del modelo como accuracy)",
            "Feature attribution drift (deriva en la importancia relativa de las features)",
        ],
        correct=0,
        key="mla02-q31b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - "concept drift" NO es un tipo de Model Monitor.</div>'
            '<p><b>Definicion:</b> Model Monitor ofrece 4 tipos oficiales: <b>data quality</b>, <b>model quality</b> (ej. accuracy), <b>bias drift</b> y <b>feature attribution drift</b>. El <b>concept drift</b> (cambio en la relacion X-&gt;y) es un termino de la literatura general de ML, pero <b>no</b> es uno de los tipos que expone SageMaker Model Monitor.</p>'
            '<p><b>Por que NO las otras (si son tipos validos):</b></p>'
            '<ul>'
            '<li><b>Data quality drift:</b> si es un tipo (vigila la distribucion/calidad de los datos de entrada frente al baseline).</li>'
            '<li><b>Model quality drift:</b> si es un tipo (baja de accuracy y otras metricas contra el ground truth).</li>'
            '<li><b>Feature attribution drift:</b> si es un tipo (cambio en la importancia relativa de las features), apoyado por SageMaker Clarify (junto con bias drift, el cuarto tipo oficial).</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Los 4 tipos: data quality, model quality, bias, feature attribution. "Concept drift" existe en ML pero NO es un tipo de Model Monitor; latencia/CPU se ven en CloudWatch.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html">docs.aws model monitor</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Training semanal fijo (55 semanas, 40 h/semana) que NO tolera interrupciones ni retrasos, pero se quiere <b>reducir costo</b>. &iquest;Que solucion cumple?",
        options=[
            "Suscribir un SageMaker Savings Plan de 1 anio con pago upfront y correr sobre instancias On-Demand",
            "Usar heterogeneous cluster en SageMaker Training con Spot Instances en uno o mas grupos",
            "Usar el resizing automatico de instancias de SageMaker Studio segun la complejidad del job",
            "Configurar AWS Budgets para topar el gasto mensual y gestionar el schedule automaticamente",
        ],
        correct=0,
        key="mla02-q32",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Savings Plan de 1 anio (upfront) sobre On-Demand.</div>'
            '<p><b>El problema:</b> el schedule es estricto (sin interrupciones) pero se quiere ahorrar; hay que reducir precio sin arriesgar continuidad.</p>'
            '<p><b>Por que sirve:</b> los <b>SageMaker Savings Plans</b> dan hasta ~64% de descuento vs On-Demand a cambio de un compromiso de uso por 1 o 3 anios; corriendo On-Demand se mantiene la continuidad y se abarata el costo.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Spot Instances:</b> son interrumpibles; violan el requisito de no interrupciones/retrasos.</li>'
            '<li><b>Resizing automatico de Studio:</b> Studio no redimensiona instancias durante el training; la seleccion es previa y manual.</li>'
            '<li><b>AWS Budgets:</b> solo alerta al superar un umbral; no controla ni agenda jobs ni garantiza ahorro con continuidad.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Ahorro sin interrupciones = Savings Plans sobre On-Demand. Spot = mas barato pero interrumpible. Budgets = alertas, no control.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html">docs.aws savings plans</a></div>'
        ),
    ),

    # ============================================================
    # Q33 - CloudWatch Logs Insights (analisis de logs)
    # ============================================================
    card(
        question="Se quiere <b>consultar interactivamente</b> grandes volumenes de registros operativos de varios recursos AWS, agrupando entradas similares con deteccion de patrones respaldada por ML, sin administrar infraestructura. &iquest;Que servicio conviene?",
        options=[
            "Amazon CloudWatch Logs Insights",
            "Amazon OpenSearch Service",
            "AWS CloudTrail",
            "AWS Config",
        ],
        correct=0,
        key="mla02-q33",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon CloudWatch Logs Insights.</div>'
            '<p><b>Por que sirve:</b> <b>CloudWatch Logs Insights</b> consulta los logs ya centralizados en CloudWatch con un lenguaje propio, sin aprovisionar ni administrar infraestructura; su comando <code>pattern</code> (respaldado por ML) agrupa y resume entradas similares para detectar tendencias y cuellos de botella.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Amazon OpenSearch Service:</b> tambien busca y analiza logs, pero implica <b>aprovisionar y operar un dominio/cluster</b> (o Serverless con su propio setup) e ingestar los logs; es mas pesado que consultar directamente los logs de CloudWatch con Insights.</li>'
            '<li><b>CloudTrail:</b> registra llamadas API para auditoria/gobernanza (quien hizo que), no es un motor de consulta interactiva de logs operativos.</li>'
            '<li><b>AWS Config:</b> evalua configuraciones y cumplimiento de recursos, no consulta logs.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Consultar logs ya en CloudWatch sin operar infra = Logs Insights. Busqueda/analitica a gran escala con cluster propio = OpenSearch. Auditar API = CloudTrail. Config de recursos = Config.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html">docs.aws logs insights</a></div>'
        ),
    ),

    # ============================================================
    # Q34 - CloudTrail (auditoria de API)
    # ============================================================
    card(
        question="Un auditor necesita el <b>historial de quien invoco cada API</b> de AWS (identidad, IP de origen, timestamp) en toda la cuenta, para cumplimiento. &iquest;Que servicio conviene?",
        options=[
            "AWS CloudTrail",
            "AWS Config",
            "Amazon CloudWatch Logs",
            "VPC Flow Logs",
        ],
        correct=0,
        key="mla02-q34",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS CloudTrail.</div>'
            '<p><b>Por que sirve:</b> <b>CloudTrail</b> registra las llamadas API del plano de control/gestion (consola, SDK, CLI y servicios) con la identidad del usuario, IP de origen y timestamp, dando el historial de "quien hizo que y cuando" para auditoria y cumplimiento.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>AWS Config:</b> registra el <b>estado y los cambios de configuracion</b> de los recursos (drift), no el historial de llamadas API por identidad.</li>'
            '<li><b>Amazon CloudWatch Logs:</b> centraliza y consulta logs de aplicaciones/sistemas, pero no captura de forma nativa el registro de actividad de API de la cuenta como lo hace CloudTrail.</li>'
            '<li><b>VPC Flow Logs:</b> captura metadata del <b>trafico de red</b> (IPs, puertos, aceptado/rechazado) a nivel de VPC/ENI, no las llamadas API ni la identidad que las hizo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>"Quien llamo que API y cuando" = CloudTrail. Estado/cambios de configuracion = Config. Logs de app/sistema = CloudWatch Logs. Trafico de red = VPC Flow Logs.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/cloudtrail/">docs.aws cloudtrail</a></div>'
        ),
    ),

    # ============================================================
    # Q35 - cost allocation tags: primer paso
    # ============================================================
    card(
        question="Ya se etiquetaron los recursos de ML con pares clave-valor, pero los tags <b>no aparecen todavia</b> en Cost Explorer ni en los reportes de costos. &iquest;Que accion es indispensable para que empiecen a desglosar el gasto?",
        options=[
            "Activar esos tags como cost allocation tags en la consola de Billing",
            "Volver a aplicar los mismos tags a cada recurso una segunda vez",
            "Crear un nuevo par clave-valor distinto para cada recurso de ML",
            "Configurar una alarma de AWS Budgets por cada proyecto etiquetado",
        ],
        correct=0,
        key="mla02-q35",
        answer=(
            '<div class="verdict">Correcta: {{L}} - activar los tags como cost allocation tags en Billing.</div>'
            '<p><b>El problema:</b> aplicar un tag a un recurso NO basta para el desglose de costos; AWS solo incluye un tag en los reportes de facturacion cuando lo <b>activas</b> explicitamente como cost allocation tag en la consola de Billing. Hasta entonces el tag existe en el recurso pero no aparece en Cost Explorer ni en el CUR.</p>'
            '<p><b>Flujo real:</b> etiquetar los recursos (clave-valor) - <b>activar</b> los user-defined tags en Billing - esperar a que se propaguen (hasta ~24 h) - usarlos en Cost Explorer/CUR.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Reaplicar los mismos tags:</b> no cambia nada; el tag ya esta en el recurso, lo que falta es activarlo en Billing.</li>'
            '<li><b>Crear un par clave-valor distinto por recurso:</b> fragmentaria el reporte y no resuelve la causa (falta la activacion); ademas dificulta agrupar por proyecto/departamento.</li>'
            '<li><b>Alarma de AWS Budgets:</b> Budgets solo alerta/topa gasto; no hace que un tag aparezca en el desglose de costos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Un tag no desglosa costos hasta ACTIVARLO como cost allocation tag en Billing. Etiquetar != activar; la propagacion tarda hasta ~24 h.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html">docs.aws cost allocation tags</a></div>'
        ),
    ),

    # ============================================================
    # Q36 - IAM Roles con Identity-Based Policies (least privilege)
    # ============================================================
    card(
        question="Controlar el acceso a SageMaker, S3 y Glue segun <b>minimo privilegio</b>. &iquest;Que componentes de IAM son los mas apropiados?",
        options=[
            "IAM Roles con Identity-Based Policies",
            "Service Control Policies (SCPs)",
            "SageMaker Endpoint Policies",
            "AWS Resource Access Manager (RAM)",
        ],
        correct=0,
        key="mla02-q36",
        answer=(
            '<div class="verdict">Correcta: {{L}} - IAM Roles con Identity-Based Policies.</div>'
            '<p><b>El problema:</b> otorgar solo los permisos necesarios a cada servicio (SageMaker, S3, Glue) aplicando least privilege.</p>'
            '<p><b>Por que sirve:</b> los <b>IAM roles</b> con <b>identity-based policies</b> permiten crear roles separados por servicio y adjuntar politicas con solo los permisos requeridos, con credenciales temporales; es la forma recomendada de control fino.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SCPs:</b> ponen limites/guardarraliles maximos pero <b>no otorgan</b> permisos a un usuario o role.</li>'
            '<li><b>SageMaker Endpoint Policies:</b> son especificas de endpoints, no cubren S3 ni Glue.</li>'
            '<li><b>RAM:</b> comparte recursos entre cuentas, no gestiona control de acceso fino intra-cuenta.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Least privilege granular = IAM roles + identity-based policies. SCPs solo restringen, nunca conceden.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html">docs.aws IAM policies</a></div>'
        ),
    ),

    # ============================================================
    # Q37 - inline policy en execution role del dominio Studio
    # ============================================================
    card(
        question="En un SageMaker Studio con varios dominios, hay que <b>aislar los permisos de un solo dominio de Studio</b> para darle acceso a un bucket S3 sin afectar a otros dominios/usuarios, ligando los permisos al entorno de computo (no a usuarios). &iquest;Que enfoque?",
        options=[
            "Adjuntar la policy de acceso al execution role del dominio de Studio que se quiere aislar",
            "Adjuntar la misma policy a un execution role compartido por todos los dominios de Studio",
            "Adjuntar la policy al execution role a nivel de user profile dentro del dominio de Studio",
            "Poner una resource-based policy en el bucket S3 que conceda acceso al usuario IAM",
        ],
        correct=0,
        key="mla02-q37",
        answer=(
            '<div class="verdict">Correcta: {{L}} - policy en el execution role del dominio que se quiere aislar.</div>'
            '<p><b>El problema:</b> los permisos deben ligarse al <b>computo</b> (el dominio) y no a usuarios, y solo a ESE dominio, sin afectar a otros. La clave es <b>a que rol se adjunta la policy</b>: al execution role propio del dominio.</p>'
            '<p><b>Por que sirve:</b> adjuntar la policy al <b>execution role a nivel de dominio</b> concede permisos unicamente a las cargas que corren en ese dominio, alineado con least privilege. El aislamiento lo da el <b>alcance del rol</b>, no el tipo de policy (inline o managed logran lo mismo si se pegan al mismo rol).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Policy a un role compartido por todos los dominios de Studio:</b> otorgaria esos permisos a cargas de otros dominios, rompiendo el aislamiento pedido.</li>'
            '<li><b>Policy al execution role a nivel de user profile:</b> combina execution role y dominio, pero baja el alcance al <b>perfil de usuario</b>; aplicarla ah&iacute; solo cubre a ese usuario y no aisla el dominio completo como pide el escenario (los permisos deben ligarse al dominio, no a un profile).</li>'
            '<li><b>Resource-based policy en el bucket concediendo al usuario:</b> abre el recurso a un principal (el usuario) en vez de acotar el permiso al computo del dominio; no cumple "permisos al computo, aislados por dominio".</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Permisos al computo (no a usuarios) + aislar un dominio = policy en el <b>execution role especifico del dominio</b>. El aislamiento depende del rol, no de si la policy es inline o managed.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html">docs.aws sagemaker roles</a></div>'
        ),
    ),

    # ============================================================
    # Q38 - tipos de drift (data quality vs bias vs feature attribution)
    # ============================================================
    card(
        question="Deriva de modelo - en un modelo de readmision hospitalaria, el monitoreo detecta que la <b>distribucion estadistica de los datos de entrada</b> (edad, region, comorbilidades) ha cambiado: llegan <b>nuevos perfiles demograficos de pacientes</b> con distribuciones distintas a las del entrenamiento, aun sin disponer todavia del ground truth para medir accuracy. Dentro de los tipos de <b>SageMaker Model Monitor</b>, &iquest;que tipo de drift corresponde a este sintoma?",
        options=[
            "Data quality drift (el monitor de calidad de datos frente al baseline de entrenamiento)",
            "Bias drift (el modelo empieza a favorecer o penalizar a ciertos grupos)",
            "Feature attribution drift (cambia la importancia relativa de las features en las predicciones)",
            "Model quality drift (se degradan metricas como accuracy medidas contra el ground truth real)",
        ],
        correct=0,
        key="mla02-q38",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Data quality drift.</div>'
            '<p><b>Definicion:</b> en SageMaker Model Monitor, el <b>data quality drift</b> es el tipo que vigila la <b>distribucion estadistica de los datos de entrada</b> (medias, rangos, tipos, valores faltantes) comparandola contra un baseline; cuando llegan perfiles de entrada distintos a los del entrenamiento, se dispara este monitor.</p>'
            '<p><b>Nota de terminologia:</b> "data quality drift" es el nombre que usa <b>SageMaker</b> para lo que en la literatura general de ML se llama <b>data drift</b> o <b>covariate drift</b> (cambio en la distribucion de las features de entrada, X). No confundir con "concept drift", que es el cambio en la relacion X-&gt;y y NO es un tipo de Model Monitor.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bias drift:</b> vigila que el modelo no empiece a favorecer o penalizar a grupos protegidos; el escenario habla de distribucion de entrada, no de equidad.</li>'
            '<li><b>Feature attribution drift:</b> detecta cambios en el peso/importancia de cada feature en las predicciones, no en la distribucion global de los datos de entrada.</li>'
            '<li><b>Model quality drift:</b> mide la degradacion de metricas (accuracy, etc.) contra el <b>ground truth real</b>; requiere etiquetas verdaderas y detecta el sintoma, no la causa de distribucion de entrada que describe el escenario.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Los 4 tipos de Model Monitor: data quality, model quality, bias drift, feature attribution drift. Distribucion de entrada cambia = data quality drift (el "data/covariate drift" de la literatura). "Concept drift" NO es un tipo de Model Monitor.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-quality.html">docs.aws data quality drift</a></div>'
        ),
    ),
    # refuerzo Q38: bias drift + Clarify
    card(
        question="Un modelo empieza a <b>marcar de forma desproporcionada a ciertos grupos</b> de pacientes. &iquest;Que tipo de drift es y que servicio ayuda a detectarlo?",
        options=[
            "Bias drift, detectado con Amazon SageMaker Clarify",
            "Data quality drift, detectado con Amazon SageMaker Clarify",
            "Feature attribution drift, detectado con Amazon CloudWatch",
            "Virtual drift, detectado con Amazon SageMaker Debugger",
        ],
        correct=0,
        key="mla02-q38b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Bias drift, detectado con Amazon SageMaker Clarify.</div>'
            '<p><b>Definicion:</b> el <b>bias drift</b> ocurre cuando el modelo empieza a favorecer o penalizar a grupos especificos por cambios en la distribucion o parametros; <b>Clarify</b> mide y explica sesgo en datos y predicciones.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Data quality drift con Clarify:</b> el tipo no corresponde a "marcado desproporcionado de grupos" (eso es sesgo), aunque Clarify sirve para bias.</li>'
            '<li><b>Feature attribution drift con CloudWatch:</b> el tipo no encaja y CloudWatch no detecta drift de atribucion; eso lo hace Clarify/Model Monitor.</li>'
            '<li><b>Virtual drift con Debugger:</b> Debugger depura el entrenamiento, no monitorea sesgo en produccion.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Sesgo/fairness = SageMaker Clarify. Atribucion de features y calidad de datos = Model Monitor (que usa Clarify por debajo para bias y attribution).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-monitor-bias-drift.html">docs.aws bias drift</a></div>'
        ),
    ),

    # ============================================================
    # Q39 - monitoreo continuo con real-time endpoint
    # ============================================================
    card(
        question="Sistema de recomendaciones en produccion que exige <b>respuestas de baja latencia</b> y monitoreo continuo de desempeno/calidad. &iquest;Que opcion de monitoreo conviene?",
        options=[
            "Monitoreo continuo (data quality/model quality) sobre el real-time endpoint",
            "Solo alarmas de CloudWatch sobre latencia y errores del endpoint, sin data capture",
            "Muestreo parcial del trafico una vez por semana para revisar drift de datos",
            "Monitoreo on-schedule sobre trabajos de batch transform del historico",
        ],
        correct=0,
        key="mla02-q39",
        answer=(
            '<div class="verdict">Correcta: {{L}} - monitoreo continuo sobre el real-time endpoint.</div>'
            '<p><b>El problema:</b> las recomendaciones necesitan baja latencia (real-time endpoint) y deteccion inmediata de drift/anomalias en produccion sobre el trafico real.</p>'
            '<p><b>Por que sirve:</b> el <b>monitoreo continuo</b> de un real-time endpoint captura las inferencias en vivo (data capture) y las evalua contra el baseline de forma permanente, permitiendo detectar drift de datos o calidad al instante; SageMaker Studio visualiza los resultados.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Solo alarmas de CloudWatch:</b> vigilan metricas de sistema (latencia, errores) pero NO detectan drift de datos o de calidad del modelo; se quedan cortas para el monitoreo de desempeno pedido.</li>'
            '<li><b>Muestreo semanal parcial:</b> revisa solo una fraccion y a intervalos largos; puede pasar por alto anomalias que aparecen entre muestreos, contra el requisito de deteccion inmediata.</li>'
            '<li><b>On-schedule sobre batch transform:</b> analiza datos historicos por lotes a intervalos, sin insights en tiempo real sobre el trafico en vivo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Baja latencia + deteccion inmediata sobre trafico en vivo = monitoreo continuo del real-time endpoint (con data capture). Las alarmas de CloudWatch cubren sistema, no drift.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html">docs.aws model monitor</a></div>'
        ),
    ),

    # ============================================================
    # Q40 - SageMaker Inference Recommender (tipo de instancia optimo)
    # ============================================================
    card(
        question="Se quiere elegir el <b>tipo de instancia mas costo-efectivo</b> para desplegar un modelo en tiempo real cumpliendo latencia y throughput. &iquest;Que feature de SageMaker lo determina?",
        options=[
            "Amazon SageMaker Inference Recommender",
            "Amazon SageMaker Automatic Scaling",
            "Amazon SageMaker Automatic Model Tuning",
            "Amazon SageMaker Multi-Model Endpoints",
        ],
        correct=0,
        key="mla02-q40",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon SageMaker Inference Recommender.</div>'
            '<p><b>Por que sirve:</b> el <b>Inference Recommender</b> analiza el modelo y hace pruebas de carga para recomendar el tipo de instancia y configuracion mas costo-efectivos que cumplan objetivos de latencia y throughput.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Automatic Scaling:</b> ajusta el numero de instancias segun trafico, pero no elige el tipo de instancia optimo.</li>'
            '<li><b>Automatic Model Tuning:</b> optimiza hiperparametros del modelo, no la instancia de despliegue.</li>'
            '<li><b>Multi-Model Endpoints:</b> aloja varios modelos tras un endpoint; no determina la instancia optima para uno solo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Elegir tipo/config de instancia = Inference Recommender. Escalar cantidad = Automatic Scaling. Tunear modelo = Automatic Model Tuning.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/inference-recommender-recommendation-jobs.html">docs.aws inference recommender</a></div>'
        ),
    ),
    # refuerzo Q40: Multi-Model Endpoints
    card(
        question="SageMaker - &iquest;cual es el proposito principal de los <b>Multi-Model Endpoints</b>?",
        options=[
            "Alojar muchos modelos tras un solo endpoint para compartir recursos y bajar costo",
            "Elegir el tipo de instancia mas costo-efectivo segun latencia y throughput",
            "Ajustar automaticamente el numero de instancias segun el trafico entrante",
            "Optimizar los hiperparametros de un modelo mediante busqueda automatica",
        ],
        correct=0,
        key="mla02-q40b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - alojar muchos modelos tras un endpoint para compartir recursos.</div>'
            '<p><b>Definicion:</b> los <b>Multi-Model Endpoints</b> sirven muchos modelos desde un mismo endpoint, cargandolos bajo demanda; reducen costo cuando tienes muchos modelos con trafico intermitente.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Elegir instancia costo-efectiva:</b> eso lo hace el <b>Inference Recommender</b>.</li>'
            '<li><b>Ajustar numero de instancias:</b> eso es <b>Automatic Scaling</b>.</li>'
            '<li><b>Optimizar hiperparametros:</b> eso es <b>Automatic Model Tuning</b>.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Muchos modelos, un endpoint = Multi-Model Endpoints. No confundir con elegir instancia (Recommender) ni escalar (Auto Scaling).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/multi-model-endpoints.html">docs.aws multi-model endpoints</a></div>'
        ),
    ),
    # refuerzo Q32: Spot vs On-Demand vs Savings Plan
    card(
        question="Entrenamiento en SageMaker - &iquest;por que las <b>Spot Instances</b> NO sirven cuando el schedule no tolera interrupciones?",
        options=[
            "Porque AWS puede interrumpirlas al reclamar la capacidad, arriesgando retrasos en el job",
            "Porque son mas caras que On-Demand y no dan descuento alguno",
            "Porque no soportan instancias de computo optimizado para entrenamiento",
            "Porque exigen un compromiso de uso de 1 o 3 anios por adelantado",
        ],
        correct=0,
        key="mla02-q32b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS puede reclamar la capacidad e interrumpir el job.</div>'
            '<p><b>Definicion:</b> las <b>Spot Instances</b> usan capacidad sobrante con gran descuento, pero AWS puede <b>interrumpirlas</b> con poco aviso; por eso no encajan en trabajos con deadlines estrictos sin manejo de interrupciones (checkpointing).</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Mas caras sin descuento:</b> falso; Spot es lo mas barato, el problema es la interrupcion.</li>'
            '<li><b>No soportan computo optimizado:</b> falso; Spot esta disponible para muchas familias, incluidas compute-optimized.</li>'
            '<li><b>Compromiso de 1-3 anios:</b> eso describe los <b>Savings Plans</b>, no Spot.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Spot = barato pero interrumpible (usa checkpoints). Savings Plans = descuento por compromiso, sin interrupcion. On-Demand = sin compromiso, precio full.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-managed-spot-training.html">docs.aws managed spot training</a></div>'
        ),
    ),
    # ============================================================
    card(
        question="Detectar y marcar automaticamente <b>imagenes que violan las guias de comunidad</b> subidas por usuarios, con minimo esfuerzo. &iquest;Que enfoque conviene?",
        options=[
            "Usar las APIs de moderacion de contenido de Amazon Rekognition",
            "Entrenar una CNN a medida en SageMaker para clasificar y marcar las imagenes",
            "Usar Amazon Bedrock para generar insights de moderacion de imagenes",
            "Usar las reglas integradas de Amazon SageMaker Debugger para monitorear la calidad de imagen",
        ],
        correct=0,
        key="mla02-q41",
        answer=(
            '<div class="verdict">Correcta: {{L}} - las APIs de moderacion de Amazon Rekognition.</div>'
            '<p><b>Por que sirve:</b> <b>Rekognition</b> ofrece APIs de moderacion listas que identifican contenido inapropiado u ofensivo en imagenes, rapido y con minimo esfuerzo manual.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CNN a medida en SageMaker:</b> es posible pero intensivo en recursos y experiencia; mas complejo que una API administrada.</li>'
            '<li><b>Amazon Bedrock:</b> hoy <b>Bedrock Guardrails</b> si puede filtrar imagenes daninas (via ApplyGuardrail), asi que no es que "Bedrock no sirva para imagenes"; el punto es el esfuerzo: montar el filtrado con Bedrock exige mas ingenieria (configurar guardrails, pipeline, integracion) que llamar una API de moderacion lista. <b>Rekognition Content Moderation</b> es purpose-built y resuelve el caso con MINIMO esfuerzo, por eso es la mejor respuesta.</li>'
            '<li><b>SageMaker Debugger:</b> depura y monitorea el entrenamiento de modelos, no modera contenido de imagenes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Moderacion de imagenes/video con minimo esfuerzo = Rekognition (API lista, purpose-built). Bedrock Guardrails tambien filtra imagenes, pero requiere mas montaje. CNN propia solo si necesitas control total.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/rekognition/latest/dg/moderation.html">docs.aws rekognition moderation</a></div>'
        ),
    ),

    # ============================================================
    # Q42 - IAM role cross-account (assume role, S3 entre cuentas)
    # ============================================================
    card(
        question="Un startup en OTRA cuenta AWS necesita acceso (programatico y por consola) al bucket S3 de otra empresa, de forma segura. &iquest;Que solucion conviene?",
        options=[
            "Crear un IAM role en la cuenta duena que el startup asuma con sts:AssumeRole para acceder al bucket",
            "Crear una bucket policy en la cuenta del startup que otorgue acceso al bucket de la empresa duena",
            "Usar Amazon S3 Access Points en la cuenta duena para dar acceso directo al startup sin roles",
            "Habilitar S3 Block Public Access en la cuenta duena del bucket para permitir el acceso externo",
        ],
        correct=0,
        key="mla02-q42",
        answer=(
            '<div class="verdict">Correcta: {{L}} - un IAM role cross-account que el startup asume via sts:AssumeRole.</div>'
            '<p><b>El problema:</b> acceso seguro entre cuentas AWS distintas, tanto programatico como por consola, sin credenciales permanentes.</p>'
            '<p><b>Por que sirve:</b> se crea un <b>IAM role cross-account</b> en la cuenta duena con permisos al bucket; el startup lo asume con <code>sts:AssumeRole</code> y obtiene credenciales temporales de STS, siguiendo least privilege sin acceso permanente.</p>'
            '<p><b>Por que NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Bucket policy en la cuenta del startup:</b> las bucket policies se definen en la cuenta <b>duena</b> del bucket, no en la que accede; no otorgaria acceso.</li>'
            '<li><b>S3 Access Points:</b> dan un camino de red al bucket pero requieren igualmente IAM roles/policies para autenticar cross-account.</li>'
            '<li><b>S3 Block Public Access:</b> es buena practica de seguridad pero no concede acceso al startup.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span>Acceso cross-account seguro = IAM role + sts:AssumeRole (credenciales temporales), no compartir claves permanentes.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html">docs.aws cross-account roles</a></div>'
        ),
    ),
]

if __name__ == "__main__":
    create(
        deck_name="MLA-C01::02 - Modeling, Deployment & Ops",
        cards=cards,
        out_path="out/MLA-C01_02.apkg",
        do_import=False,
    )
