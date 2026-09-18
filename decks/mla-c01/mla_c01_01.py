#!/usr/bin/env python3
"""
MLA-C01::01 - Data Preparation for Machine Learning.

Cartas construidas a partir de 42 preguntas fuente (Tutorials Dojo, dominio
Data Preparation + algo de Model Development). Regla: 1 a 3 cartas por pregunta.
- Carta base (siempre): la MCQ tal cual.
- Cartas de refuerzo (cuando la explicacion lo justifica): concepto/definicion o
  comparacion servicio-vs-servicio que YA aparece en la explicacion fuente.

Estandares: 4 opciones, el frente no filtra la respuesta (el motor baraja),
verdict con {{L}} (nunca hardcodear la letra), cada dorso refuta CADA distractor
uno por uno, opciones balanceadas en longitud/especificidad, keys estables y
unicas, explicaciones en espanol, HTML en los campos, sin em dashes.
"""
from anki_mcq import card, create

cards = [
    # ===================== Q1: modelo simple vs complejo =====================
    card(
        question="<b>ML - selecci&oacute;n de modelo:</b> una entidad financiera opera bajo regulaci&oacute;n estricta y debe poder <b>justificar ante auditores cada aprobaci&oacute;n o rechazo de pr&eacute;stamo</b>, mostrando qu&eacute; factores pesaron en la decisi&oacute;n. &iquest;Qu&eacute; tipo de modelo debe elegir y por qu&eacute;?",
        options=[
            "Un modelo simple, porque la explicabilidad es crucial en decisiones de aprobaci&oacute;n de pr&eacute;stamos",
            "Un modelo simple, porque la exactitud importa m&aacute;s que la explicabilidad en la aprobaci&oacute;n de pr&eacute;stamos",
            "Un modelo complejo, porque la explicabilidad es crucial en decisiones de aprobaci&oacute;n de pr&eacute;stamos",
            "Un modelo complejo, porque la exactitud importa m&aacute;s que la explicabilidad en la aprobaci&oacute;n de pr&eacute;stamos",
        ],
        correct=0,
        key="mla01-q1",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Modelo simple, porque la explicabilidad es crucial.</div>'
            '<p><b>El problema:</b> el requisito no es maximizar exactitud sino <b>justificar</b> cada decisi&oacute;n ante interesados y reguladores. <b>Explicabilidad</b> = cu&aacute;nto del sistema se puede explicar en t&eacute;rminos humanos.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> los <b>modelos simples</b> (&aacute;rboles de decisi&oacute;n, regresi&oacute;n log&iacute;stica) dan visibilidad clara de qu&eacute; factores pesan en la decisi&oacute;n, por eso son m&aacute;s adecuados cuando la transparencia manda sobre la exactitud.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Simple por exactitud:</b> elige el modelo correcto pero por la raz&oacute;n equivocada; el criterio aqu&iacute; es la explicabilidad, no la exactitud.</li>'
            '<li><b>Complejo por exactitud:</b> prioriza exactitud sobre explicabilidad, justo lo contrario del requisito; modelos complejos (redes profundas, ensembles) son poco interpretables.</li>'
            '<li><b>Complejo por explicabilidad:</b> se contradice: los modelos complejos son <b>menos</b> interpretables, no m&aacute;s.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Regla mental: mucha regulaci&oacute;n o auditor&iacute;a = prioriza explicabilidad (modelo simple); pura exactitud sin necesidad de justificar = puedes ir a modelo complejo.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-model-explainability.html">SageMaker Clarify: explicabilidad</a></div>'
        ),
    ),
    # refuerzo Q1: definicion simple vs complejo (aparece en la explicacion)
    card(
        question="<b>ML - concepto:</b> al contrastar un <b>modelo simple</b> con uno <b>complejo</b> en machine learning, &iquest;qu&eacute; compensaci&oacute;n (trade-off) los distingue?",
        options=[
            "El simple suele ser m&aacute;s explicable y r&aacute;pido pero puede perder exactitud; el complejo suele ser m&aacute;s exacto pero dif&iacute;cil de interpretar",
            "El complejo suele ser m&aacute;s explicable porque tiene m&aacute;s par&aacute;metros, y cada uno describe con detalle una parte de la decisi&oacute;n del modelo",
            "El simple suele generalizar peor porque, al tener pocos par&aacute;metros, casi siempre sobreajusta (overfitting) los datos de entrenamiento",
            "La explicabilidad y la exactitud tienden a subir juntas, as&iacute; que un modelo m&aacute;s exacto resulta adem&aacute;s m&aacute;s f&aacute;cil de interpretar",
        ],
        correct=0,
        key="mla01-q1b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Simple: m&aacute;s explicable y r&aacute;pido, menos exacto; complejo: m&aacute;s exacto, menos interpretable.</div>'
            '<p><b>El concepto:</b> la diferencia clave es el balance entre <b>exactitud</b> (cu&aacute;ntos puntos predice bien) y <b>explicabilidad</b> (cu&aacute;nto se puede explicar en t&eacute;rminos humanos).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> un modelo simple produce resultados r&aacute;pidos y explicables, pero puede ser menos exacto; uno complejo puede ser muy exacto, pero sus resultados son dif&iacute;ciles de comunicar.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Complejo m&aacute;s explicable por tener m&aacute;s par&aacute;metros:</b> suena razonable pero es al rev&eacute;s; m&aacute;s par&aacute;metros hacen la relaci&oacute;n entrada-salida m&aacute;s opaca (caja negra), no m&aacute;s f&aacute;cil de justificar factor por factor.</li>'
            '<li><b>Simple generaliza peor por sobreajustar:</b> matizado pero incorrecto; el sobreajuste es t&iacute;pico de modelos con MUCHA capacidad; un modelo simple tiende a sub-ajustar, no a sobreajustar por tener pocos par&aacute;metros.</li>'
            '<li><b>Explicabilidad y exactitud suben juntas:</b> parece intuitivo pero suele haber un trade-off; ganar exactitud con modelos complejos normalmente cuesta interpretabilidad, no la mejora.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Piensa en el eje "caja transparente vs caja negra": simple = transparente; complejo = negra pero potente.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/what-is/machine-learning/">AWS: what is machine learning</a></div>'
        ),
    ),

    # ===================== Q2: que es aprendizaje automatico =====================
    card(
        question="<b>ML - enfoque correcto:</b> una empresa quiere predecir <b>churn</b> (abandono de clientes) a partir de datos de clientes. &iquest;Cu&aacute;l describe mejor el enfoque de machine learning que deber&iacute;a seguir?",
        options=[
            "Entrenar el modelo sobre todo el hist&oacute;rico y medir su acierto sobre ese mismo conjunto, sin apartar datos de prueba",
            "Aplicar clustering no supervisado sobre los clientes y tomar cada cl&uacute;ster como si fuera la etiqueta de abandono a predecir",
            "Ajustar a mano los pesos de un modelo lineal seg&uacute;n la intuici&oacute;n del equipo en lugar de aprenderlos de los datos",
            "Alimentar los datos etiquetados a un algoritmo supervisado que aprenda patrones y generalice para predecir el abandono",
        ],
        correct=3,
        key="mla01-q2",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Entrenar un algoritmo supervisado que aprende patrones y generaliza.</div>'
            '<p><b>El problema:</b> predecir churn a partir de datos etiquetados es <b>aprendizaje supervisado</b>; hay que entrenar bien y medir la generalizaci&oacute;n, no memorizar ni forzar el m&eacute;todo equivocado.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> alimentar datos <b>etiquetados</b> a un algoritmo supervisado que aprende patrones y luego <b>generaliza</b> a clientes nuevos es exactamente el planteamiento correcto para churn.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Evaluar sobre el mismo set de entrenamiento:</b> suena a ML, pero sin apartar datos de prueba mides memorizaci&oacute;n (overfitting), no la capacidad real de predecir sobre datos no vistos.</li>'
            '<li><b>Clustering no supervisado como etiqueta:</b> churn ya viene <b>etiquetado</b>; usar clusters como etiqueta descarta esa se&ntilde;al y convierte un problema supervisado en uno no supervisado inadecuado.</li>'
            '<li><b>Ajustar los pesos a mano por intuici&oacute;n:</b> el valor del ML es que el algoritmo <b>aprende</b> los par&aacute;metros de los datos; fijarlos a mano vuelve al sesgo humano y no escala.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Con etiquetas disponibles (churn s&iacute;/no) piensa en <b>supervisado</b> con split train/test para medir generalizaci&oacute;n, no en clustering ni en ajuste manual.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/what-is/machine-learning/">AWS: what is machine learning</a></div>'
        ),
    ),

    # ===================== Q3: cuando ML aporta menos valor =====================
    card(
        question="<b>ML - cu&aacute;ndo NO aporta valor:</b> una empresa de e-commerce tiene datos hist&oacute;ricos de clientes. &iquest;En cu&aacute;l de estas tareas el machine learning ser&iacute;a <b>menos &uacute;til</b>?",
        options=[
            "Segmentar autom&aacute;ticamente a los clientes en grupos de comportamiento similar a partir de decenas de variables de compra",
            "Obtener el tiempo promedio de env&iacute;o de las entregas ya completadas agregando los tiempos que constan en la base de datos",
            "Anticipar la satisfacci&oacute;n del cliente a partir de interacciones de chat en tiempo real durante la conversaci&oacute;n",
            "Prever el gasto anual de cada cliente combinando su historial de compras, estacionalidad y campa&ntilde;as de marketing",
        ],
        correct=1,
        key="mla01-q3",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Obtener el tiempo promedio de env&iacute;o de entregas ya completadas.</div>'
            '<p><b>El problema:</b> se pide la tarea donde ML aporta menos valor. ML brilla al <b>encontrar patrones o predecir</b> lo desconocido; no aporta cuando la respuesta ya est&aacute; en los datos y basta consultarla o agregarla.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> un promedio de tiempos de <b>entregas ya completadas</b> es una <b>agregaci&oacute;n estad&iacute;stica</b> directa (un SELECT AVG sobre datos existentes); no hay patr&oacute;n que aprender ni valor que predecir, as&iacute; que ML es innecesario.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Segmentar clientes en grupos de comportamiento:</b> aunque no predice un valor futuro, descubrir agrupaciones a partir de decenas de variables es <b>clustering</b> (ML no supervisado), no una simple consulta; ML s&iacute; aporta.</li>'
            '<li><b>Satisfacci&oacute;n en chat en tiempo real:</b> requiere NLP/an&aacute;lisis de sentimiento para inferir un valor no observado durante la interacci&oacute;n; es ML.</li>'
            '<li><b>Gasto anual futuro por cliente:</b> combinar historial, estacionalidad y campa&ntilde;as para predecir un valor por venir es regresi&oacute;n, un uso can&oacute;nico de ML.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> El truco: dos opciones parecen "solo analizar datos existentes" (segmentar y promediar). Segmentar descubre patrones ocultos (ML); promediar solo resume lo que ya se sabe (sin ML). Distingue <b>descubrir/predecir</b> de <b>consultar/agregar</b>.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/what-is/machine-learning/">AWS: what is machine learning</a></div>'
        ),
    ),

    # ===================== Q4: reentrenamiento y data drift =====================
    card(
        question="<b>ML en producci&oacute;n:</b> un equipo de salud discute el ciclo de vida de modelos en producci&oacute;n. &iquest;Qu&eacute; afirmaci&oacute;n refleja correctamente los requisitos para mantener modelos de ML en producci&oacute;n?",
        options=[
            "Basta con monitorear la exactitud y reentrenar una sola vez, cuando caiga por debajo de un umbral dado",
            "El data drift solo afecta a modelos de deep learning; los &aacute;rboles y modelos lineales son inmunes y no requieren reentrenamiento",
            "Los modelos de ML deben reentrenarse peri&oacute;dicamente a medida que los datos cambian con el tiempo",
            "Reentrenar con m&aacute;s datos frescos cada vez elimina el drift de forma permanente, sin necesidad de volver a monitorear despu&eacute;s",
        ],
        correct=2,
        key="mla01-q4",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Reentrenar peri&oacute;dicamente a medida que los datos cambian.</div>'
            '<p><b>El problema:</b> los datos de producci&oacute;n cambian con el tiempo. A ese cambio en la distribuci&oacute;n se le llama <b>data drift</b> (deriva de datos), y degrada el modelo.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> reentrenar peri&oacute;dicamente adapta el modelo a los nuevos patrones y mantiene su exactitud; herramientas como <b>SageMaker Model Monitor</b> avisan cu&aacute;ndo es necesario.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Reentrenar una sola vez al cruzar un umbral:</b> monitorear la exactitud es correcto, pero el drift es continuo; un &uacute;nico reentrenamiento no cubre los cambios de distribuci&oacute;n posteriores, hace falta un ciclo peri&oacute;dico.</li>'
            '<li><b>Solo afecta a deep learning:</b> falso, el drift degrada a cualquier modelo (&aacute;rboles, lineales, ensembles) porque cambia la distribuci&oacute;n de entrada, no el tipo de algoritmo.</li>'
            '<li><b>Reentrenar elimina el drift permanentemente:</b> falso, reentrenar corrige el momento actual pero la distribuci&oacute;n vuelve a cambiar; hay que seguir monitoreando y reentrenando.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Data drift = la distribuci&oacute;n de entrada cambia respecto al entrenamiento. Se&ntilde;al de reentrenar. Model Monitor lo detecta.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html">SageMaker Model Monitor</a></div>'
        ),
    ),

    # ===================== Q5: Data Wrangler (menor overhead) =====================
    card(
        question="<b>Preparaci&oacute;n de datos - menor overhead:</b> pron&oacute;stico de demanda diaria con datos hist&oacute;ricos de ventas que tienen <b>timestamps irregulares y valores faltantes</b>. &iquest;Qu&eacute; enfoque cumple con el <b>MENOR</b> esfuerzo operativo?",
        options=[
            "Limpiar y pronosticar con un Amazon SageMaker Studio Notebook usando Pandas escrito a mano",
            "Procesar y pronosticar con Amazon EMR Serverless ejecutando trabajos PySpark personalizados",
            "Visualizar y pronosticar directamente con Amazon QuickSight sin una etapa dedicada de limpieza de datos",
            "Preparar y analizar los datos con Amazon SageMaker Data Wrangler (transformaciones visuales listas)",
        ],
        correct=3,
        key="mla01-q5",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon SageMaker Data Wrangler.</div>'
            '<p><b>El problema:</b> hay que limpiar datos con timestamps irregulares y faltantes, y hacerlo con el m&iacute;nimo esfuerzo operativo. <b>Data Wrangler</b> es la herramienta visual de preparaci&oacute;n de datos de SageMaker.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Data Wrangler ofrece transformaciones e imputaci&oacute;n listas para usar sin escribir/gestionar c&oacute;digo ni cl&uacute;steres, minimizando el overhead.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Studio Notebook + Pandas:</b> exige escribir y mantener c&oacute;digo manual, m&aacute;s overhead.</li>'
            '<li><b>EMR Serverless + PySpark:</b> potente pero implica desarrollar y operar jobs Spark, m&aacute;s complejo.</li>'
            '<li><b>QuickSight:</b> es una herramienta de BI/visualizaci&oacute;n; aunque incluye forecasting ML (ML Insights), no est&aacute; pensada para limpiar timestamps irregulares ni imputar faltantes, que es el n&uacute;cleo del requisito.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Menor esfuerzo operativo" + "preparar datos" suele apuntar a SageMaker Data Wrangler o DataBrew (sin c&oacute;digo).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html">SageMaker Data Wrangler</a></div>'
        ),
    ),

    # ===================== Q6: DataBrew + Parquet =====================
    card(
        question="<b>AWS Glue DataBrew:</b> ~1 TB de datos de <b>formatos mixtos</b> (CSV, JSON, XLSX, Parquet) conviven en <b>una sola carpeta</b> de S3. Un dataset de DataBrew exige un <b>unico formato/extension por dataset</b>, por lo que una carpeta con formatos mezclados no se puede procesar tal cual. Hay que procesarlos con DataBrew y dejar una salida con <b>formato compatible</b> para jobs de Glue posteriores. &iquest;Estrategia mas efectiva?",
        options=[
            "Separar los datos en carpetas por tipo de archivo, procesar cada carpeta por separado con DataBrew y guardar la salida en Apache Parquet",
            "Procesar los datos en la carpeta actual con DataBrew y guardar la salida directamente en formato Apache Parquet",
            "Procesar los datos en la carpeta actual con DataBrew y guardar la salida directamente en formato JSON",
            "Separar los datos en carpetas por tipo de archivo, procesar cada carpeta por separado con DataBrew y guardar la salida en CSV",
        ],
        correct=0,
        key="mla01-q6",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Separar por tipo de archivo, procesar cada carpeta y salir en Parquet.</div>'
            '<p><b>El problema:</b> un dataset de DataBrew espera archivos de un <b>mismo formato</b> por carpeta; mezclar CSV/JSON/XLSX/Parquet en una sola carpeta rompe el procesamiento. Adem&aacute;s, la salida debe ser eficiente para los jobs de Glue posteriores.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> al separar por tipo, cada dataset de DataBrew es homog&eacute;neo; guardar en <b>Parquet</b> (columnar y comprimido) da compatibilidad y eficiencia para los jobs de Glue posteriores.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Procesar la carpeta mixta y salir en Parquet:</b> el formato de salida es correcto, pero mezclar tipos en una carpeta hace fallar el dataset de DataBrew.</li>'
            '<li><b>Procesar la carpeta mixta y salir en JSON:</b> falla por partida doble: entrada mixta que rompe DataBrew, y salida JSON menos eficiente que Parquet para downstream.</li>'
            '<li><b>Separar por tipo pero salir en CSV:</b> resuelve bien la entrada (carpetas homog&eacute;neas), pero elige un formato de salida <b>por filas y sin compresi&oacute;n</b>; para los jobs anal&iacute;ticos de Glue posteriores CSV rinde peor que Parquet, por eso el discriminador es el FORMATO DE SALIDA.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Parquet (columnar, comprimido) es el formato por defecto para analytics/ML en AWS; separa entradas por formato antes de DataBrew.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/databrew/latest/dg/datasets.multiple-files.html">DataBrew: multiples archivos</a></div>'
        ),
    ),

    # ===================== Q7: SageMaker Clarify =====================
    card(
        question="<b>SageMaker - sesgo/patrones:</b> un ingeniero de ML debe analizar <b>features de entrada y predicciones</b> para descubrir sesgo o skew, sobre todo por segmentos demogr&aacute;ficos. &iquest;Qu&eacute; servicio se lo permite?",
        options=[
            "Usar SageMaker Feature Store para almacenar y versionar las features de entrenamiento de forma consistente",
            "Usar SageMaker Clarify para analizar el modelo y los datos en busca de patrones ocultos que afecten la exactitud",
            "Usar SageMaker Ground Truth para etiquetar los datos de entrada y as&iacute; evitar sesgos en las predicciones",
            "Usar SageMaker Data Wrangler para limpiar los datos de entrada antes del entrenamiento y quitar sesgos",
        ],
        correct=1,
        key="mla01-q7",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Clarify.</div>'
            '<p><b>El problema:</b> se necesita medir <b>sesgo</b> en datos y predicciones, y explicar el modelo por segmentos demogr&aacute;ficos. <b>Clarify</b> es la herramienta de detecci&oacute;n de sesgo y explicabilidad de SageMaker.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Clarify calcula m&eacute;tricas de sesgo pre y post entrenamiento y explica las predicciones, ideal para analizar equidad por grupos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Feature Store:</b> almacena y sirve features; no analiza sesgo ni explica predicciones.</li>'
            '<li><b>Ground Truth:</b> etiqueta datos; no mide sesgo del modelo.</li>'
            '<li><b>Data Wrangler:</b> prepara/limpia datos; no es la herramienta dedicada a m&eacute;tricas de sesgo y explicabilidad.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Palabras clave "bias", "fairness", "explicabilidad", "por grupo demogr&aacute;fico" = SageMaker Clarify.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-configure-processing-jobs.html">SageMaker Clarify jobs</a></div>'
        ),
    ),

    # ===================== Q8: datos relevantes para riesgo crediticio =====================
    card(
        question="<b>Datos para modelo de cr&eacute;dito:</b> un asesor financiero entrena un modelo para procesar solicitudes de hipoteca. &iquest;Qu&eacute; fuente de datos es la <b>M&Aacute;S directamente predictiva del riesgo crediticio</b> (y pertinente) para recolectar durante el entrenamiento?",
        options=[
            "Historial m&eacute;dico del solicitante, para inferir su estabilidad general de salud",
            "Historial educativo del solicitante, como t&iacute;tulos y a&ntilde;os de estudio",
            "Datos de bur&oacute; de cr&eacute;dito (credit bureau data) del solicitante",
            "Historial de empleo del solicitante, como antig&uuml;edad en cada puesto",
        ],
        correct=2,
        key="mla01-q8",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Datos de bur&oacute; de cr&eacute;dito.</div>'
            '<p><b>El problema:</b> para evaluar riesgo de hipoteca hay que usar datos <b>directamente predictivos del riesgo crediticio</b> y legalmente pertinentes.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> los datos de bur&oacute; de cr&eacute;dito (score, deudas, historial de pagos) son la se&ntilde;al m&aacute;s directa y aceptada para predecir el riesgo de un pr&eacute;stamo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Historial m&eacute;dico:</b> no es predictor de riesgo crediticio y su uso genera problemas de privacidad y discriminaci&oacute;n.</li>'
            '<li><b>Historial educativo:</b> se&ntilde;al d&eacute;bil e indirecta; puede introducir sesgo y no mide capacidad de pago.</li>'
            '<li><b>Historial de empleo:</b> aporta contexto, pero por s&iacute; solo es menos determinante que el historial crediticio formal del bur&oacute;.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> En riesgo crediticio, prioriza datos financieros directos (bur&oacute;, ingresos, deudas) y evita atributos sensibles no pertinentes.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/blogs/machine-learning/prepare-data-for-predicting-credit-risk-using-amazon-sagemaker-data-wrangler-and-amazon-sagemaker-clarify/">AWS blog: datos de riesgo crediticio</a></div>'
        ),
    ),

    # ===================== Q9: FSx for Lustre =====================
    card(
        question="<b>Almacenamiento para entrenamiento distribuido:</b> millones de im&aacute;genes de alta resoluci&oacute;n que requieren <b>acceso a nivel de archivo</b>, y m&uacute;ltiples instancias EC2 con GPU necesitan <b>alto throughput y baja latencia</b>. &iquest;Qu&eacute; almacenamiento es el M&Aacute;S adecuado?",
        options=[
            "Amazon Elastic File System (Amazon EFS) con clase de rendimiento General Purpose",
            "Amazon FSx for Windows File Server con recurso compartido SMB montado en las instancias",
            "Amazon FSx for Lustre, sistema de archivos paralelo de alto rendimiento integrado con S3",
            "Amazon Simple Storage Service (Amazon S3) accedido v&iacute;a API de objetos desde cada instancia",
        ],
        correct=2,
        key="mla01-q9",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon FSx for Lustre.</div>'
            '<p><b>El problema:</b> entrenamiento distribuido con GPU que exige un <b>sistema de archivos paralelo</b> de muy alto throughput y baja latencia y acceso a nivel de archivo.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> FSx for Lustre es un file system paralelo dise&ntilde;ado para HPC/ML, con rendimiento de cientos de GB/s, y se integra con S3 para hidratar los datos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EFS:</b> file system NFS de prop&oacute;sito general; menor throughput que Lustre para cargas de entrenamiento intensivas con GPU.</li>'
            '<li><b>FSx for Windows:</b> pensado para cargas Windows/SMB, no para HPC/ML de alto rendimiento en Linux.</li>'
            '<li><b>S3:</b> almacenamiento de objetos (no acceso a nivel de archivo POSIX); excelente para almacenar, pero no ofrece la baja latencia de un FS paralelo montado.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Entrenamiento GPU distribuido + alto throughput + acceso a archivo = FSx for Lustre (respaldado por S3).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html">FSx for Lustre</a></div>'
        ),
    ),

    # ===================== Q10: streaming (Select TWO -> single best) =====================
    card(
        question="<b>Streaming en tiempo real:</b> detecci&oacute;n de fraude sobre un flujo continuo de transacciones que luego pasa a un modelo en SageMaker, con la <b>menor carga operativa</b> posible. &iquest;Qu&eacute; pareja de servicios ingiere y procesa el stream antes de la inferencia?",
        options=[
            "Amazon Kinesis Data Streams para ingesta y Amazon Managed Service for Apache Flink para el procesamiento en tiempo real",
            "AWS Glue para ingesta por lotes y Amazon Athena para consultar los resultados del flujo de transacciones",
            "Amazon MSK autogestionando brokers y particiones, con Apache Flink desplegado y operado por el equipo sobre el cl&uacute;ster",
            "Amazon SQS como cola de ingesta y Amazon EMR con Hive para el procesamiento por lotes nocturno",
        ],
        correct=0,
        key="mla01-q10",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Kinesis Data Streams (ingesta) + Managed Service for Apache Flink (procesamiento).</div>'
            '<p><b>El problema:</b> se necesita ingesta y procesamiento <b>en tiempo real</b> de un stream de transacciones antes de inferir, con la <b>menor operaci&oacute;n</b> posible.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> <b>Kinesis Data Streams</b> ingiere el flujo con baja latencia y <b>Managed Service for Apache Flink</b> procesa/transforma en tiempo real de forma administrada (sin gestionar cl&uacute;steres) antes de enviarlo a SageMaker.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Glue + Athena:</b> Glue es ETL por lotes y Athena consulta datos en reposo; no procesan streams en tiempo real.</li>'
            '<li><b>MSK autogestionado + Flink operado por el equipo:</b> MSK tambi&eacute;n hace streaming en tiempo real, pero obliga a dimensionar y operar brokers/particiones y a desplegar y mantener el motor Flink por tu cuenta; es la opci&oacute;n de <b>mayor carga operativa</b>, no la m&aacute;s gestionada.</li>'
            '<li><b>SQS + EMR nocturno:</b> EMR por lotes de noche es lo opuesto a procesamiento en tiempo real.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Tiempo real + m&iacute;nima operaci&oacute;n = Kinesis Data Streams + Managed Service for Apache Flink. MSK tambi&eacute;n es streaming en tiempo real, pero implica autogestionar brokers/particiones y el motor de procesamiento.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/streams/latest/dev/introduction.html">Kinesis Data Streams</a></div>'
        ),
    ),

    # ===================== Q11: formato Parquet =====================
    card(
        question="<b>Formato de datos:</b> logs de eventos crudos (n&uacute;meros de veh&iacute;culo, mantenimiento, expiraci&oacute;n de garant&iacute;a, rotaci&oacute;n de ruedas) para un modelo de mantenimiento predictivo. Se busca un formato <b>eficiente para almacenar y procesar</b>. &iquest;Cu&aacute;l usar?",
        options=[
            "XML, formato estructurado y tipado con esquema (XSD) que valida los registros y es eficiente para intercambio entre sistemas",
            "CSV, formato tabular ligero y de lectura secuencial r&aacute;pida, muy usado para ingesta e intercambio de datos a gran escala",
            "Parquet, formato columnar y comprimido que lee solo las columnas necesarias, eficiente para consultas anal&iacute;ticas por lotes",
            "Avro, formato compacto con esquema y evoluci&oacute;n de esquema, eficiente para escritura e intercambio registro a registro",
        ],
        correct=2,
        key="mla01-q11",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Parquet.</div>'
            '<p><b>El problema:</b> se procesan grandes vol&uacute;menes de logs para consultas anal&iacute;ticas por lotes; conviene el formato que minimiza E/S al leer subconjuntos de columnas.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> <b>Parquet</b> es <b>columnar</b> y comprimido; al almacenar por columnas lee solo las que la consulta necesita, reduciendo E/S y almacenamiento en cargas anal&iacute;ticas de gran escala.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>XML:</b> valida y describe bien los registros, pero su overhead de parseo y su naturaleza por registro lo hacen lento para escaneos anal&iacute;ticos por columnas.</li>'
            '<li><b>CSV:</b> es ligero y r&aacute;pido de escribir, pero al ser <b>por filas</b> y sin tipado/compresi&oacute;n obliga a leer todo el registro; las consultas por columnas a gran escala son ineficientes.</li>'
            '<li><b>Avro:</b> es compacto y excelente para escritura/intercambio, pero es <b>orientado a filas</b>; para lecturas anal&iacute;ticas que tocan pocas columnas, Parquet reduce m&aacute;s la E/S.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> El discriminador no es "cu&aacute;l dice eficiente", sino la <b>orientaci&oacute;n</b>: columnar+compresi&oacute;n (Parquet, ORC) gana en lecturas anal&iacute;ticas; por filas (Avro, CSV) gana en escritura/streaming.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html">Glue: formato Parquet</a></div>'
        ),
    ),

    # ===================== Q12: matching -> 2 cartas (Glue y Firehose) =====================
    card(
        question="<b>Servicios de datos - ETL:</b> hay que <b>extraer y combinar</b> datos de Amazon RDS, DynamoDB y otras fuentes en un dataset unificado para entrenar un modelo. &iquest;Qu&eacute; servicio encaja mejor?",
        options=[
            "AWS Glue, servicio de ETL administrado con Data Catalog para descubrir, transformar y unificar datos",
            "Amazon EMR, cl&uacute;ster administrado de Spark/Hive orientado a procesar grandes vol&uacute;menes ya unificados",
            "Amazon Data Firehose, servicio de entrega de streaming en tiempo real hacia S3, Redshift u OpenSearch",
            "Amazon Athena, motor de consultas SQL sin servidor para analizar datos que ya residen en Amazon S3",
        ],
        correct=0,
        key="mla01-q12",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS Glue.</div>'
            '<p><b>El problema:</b> combinar datos de m&uacute;ltiples orgenes (RDS, DynamoDB, etc.) en un dataset unificado es una tarea de <b>ETL</b> (extract, transform, load).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> AWS Glue es un servicio de ETL administrado con Data Catalog; descubre, conecta y transforma datos de fuentes heterog&eacute;neas hacia un dataset unificado.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EMR:</b> procesa big data (Spark/Hive) pero no es el servicio ETL administrado para unificar fuentes diversas con poco esfuerzo.</li>'
            '<li><b>Firehose:</b> entrega streaming en tiempo real a destinos; no combina fuentes relacionales/NoSQL.</li>'
            '<li><b>Athena:</b> consulta SQL sobre datos en S3; no extrae ni combina desde RDS/DynamoDB.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Extraer y combinar de varias fuentes" = AWS Glue (ETL). "Analizar big data distribuido" = EMR. "Ingesta streaming" = Firehose.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html">AWS Glue</a></div>'
        ),
    ),
    card(
        question="<b>Servicios de datos - streaming:</b> hay que <b>ingerir, transformar y cargar datos de actividad social de forma continua (near real-time)</b> hacia S3 para el pipeline de ML. &iquest;Qu&eacute; servicio encaja mejor?",
        options=[
            "AWS Glue, servicio de ETL por lotes con Data Catalog para transformar datos ya almacenados",
            "Amazon EMR, cl&uacute;ster administrado de Spark para el procesamiento distribuido nocturno por lotes",
            "Amazon Data Firehose, entrega administrada de datos de streaming que carga a S3 sin gestionar infraestructura",
            "Amazon Redshift Spectrum, motor para consultar en SQL datos en S3 sin cargarlos previamente al almacen",
        ],
        correct=2,
        key="mla01-q12b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Data Firehose.</div>'
            '<p><b>El problema:</b> ingerir y cargar datos de streaming <b>de forma continua (near real-time)</b> hacia S3 con m&iacute;nimo mantenimiento. Firehose es el servicio de entrega de streaming administrado (entrega en near real-time por su buffering).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Firehose captura, transforma y entrega streaming a S3/Redshift/OpenSearch sin que administres infraestructura, ideal para datos sociales en vivo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Glue:</b> ETL por lotes sobre datos en reposo; no es entrega de streaming en tiempo real.</li>'
            '<li><b>EMR:</b> procesamiento distribuido por lotes; no es el mecanismo de ingesta streaming.</li>'
            '<li><b>Redshift Spectrum:</b> consulta datos en S3; no ingiere ni carga streaming.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Firehose = "cargar streaming a un destino sin servidores". Kinesis Data Streams = "leer/procesar el stream con baja latencia".</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html">Amazon Data Firehose</a></div>'
        ),
    ),

    # ===================== Q13: AWS Data Transfer Terminal =====================
    card(
        question="<b>Migraci&oacute;n de datos:</b> mover <b>100 TB</b> desde un data center on-premises hacia S3, con <b>conectividad a internet muy limitada</b> (transferencia online impracticable). La empresa <b>puede llevar sus dispositivos de almacenamiento a una instalaci&oacute;n de AWS cercana</b>. &iquest;Qu&eacute; servicio usar?",
        options=[
            "AWS Storage Gateway, para exponer un volumen h&iacute;brido y sincronizar gradualmente por la red existente",
            "AWS DataSync, agente que copia por la red a alta velocidad con verificaci&oacute;n de integridad autom&aacute;tica",
            "S3 Transfer Acceleration, que enruta la subida por edge locations para acelerar el transporte online",
            "AWS Data Transfer Terminal, migraci&oacute;n f&iacute;sica offline conectando equipo en una instalaci&oacute;n de AWS",
        ],
        correct=3,
        key="mla01-q13",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS Data Transfer Terminal.</div>'
            '<p><b>El problema:</b> 100 TB con internet muy limitado: cualquier m&eacute;todo <b>online</b> por la red tardar&iacute;a demasiado. Se necesita transferencia <b>offline/f&iacute;sica</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Data Transfer Terminal permite conectar f&iacute;sicamente el equipo en una instalaci&oacute;n de AWS para migraciones offline a gran escala, evitando la red saturada.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Storage Gateway:</b> es almacenamiento h&iacute;brido continuo; sigue dependiendo de la red limitada.</li>'
            '<li><b>DataSync:</b> transfiere por la red; con conectividad limitada no es pr&aacute;ctico para 100 TB.</li>'
            '<li><b>S3 Transfer Acceleration:</b> acelera subidas online, pero sigue usando internet, insuficiente aqu&iacute;.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Muchos TB/PB + poca conectividad = transferencia f&iacute;sica offline (Data Transfer Terminal / familia Snow), no soluciones por red.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/datatransferterminal/latest/userguide/what-is-dtt.html">AWS Data Transfer Terminal</a></div>'
        ),
    ),

    # ===================== Q14: Scatter Plot (Data Wrangler) =====================
    card(
        question="<b>Data Wrangler - visualizaci&oacute;n:</b> se quiere <b>visualizar la relaci&oacute;n entre DOS variables</b> concretas (una en el eje x, otra en el eje y), apreciar si suben/bajan juntas e <b>identificar outliers</b>. &iquest;Qu&eacute; t&eacute;cnica de visualizaci&oacute;n usar?",
        options=[
            "Scatter plot (gr&aacute;fico de dispersi&oacute;n) que muestra la relaci&oacute;n entre dos variables y sus outliers",
            "Histograma, que muestra la distribuci&oacute;n de frecuencias de una &uacute;nica variable en intervalos (bins)",
            "An&aacute;lisis de multicolinealidad, que cuantifica redundancia lineal entre varias variables predictoras a la vez",
            "Gr&aacute;fico de valores Shapley, que atribuye la contribuci&oacute;n de cada feature a una predicci&oacute;n del modelo",
        ],
        correct=0,
        key="mla01-q14",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Scatter plot.</div>'
            '<p><b>El problema:</b> ver la <b>relaci&oacute;n entre dos variables</b>, la fuerza de su correlaci&oacute;n y los outliers.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> el scatter plot ubica cada par (x, y) como un punto; revela correlaci&oacute;n (nube ascendente/descendente), su fuerza y puntos at&iacute;picos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Histograma:</b> muestra la distribuci&oacute;n de <b>una</b> variable, no la relaci&oacute;n entre dos.</li>'
            '<li><b>Multicolinealidad:</b> mide redundancia entre predictores, no visualiza pares individuales ni outliers.</li>'
            '<li><b>Valores Shapley:</b> explican contribuci&oacute;n de features a una predicci&oacute;n, no correlaciones entre variables.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Relaci&oacute;n entre dos variables + outliers" = scatter plot. "Distribuci&oacute;n de una variable" = histograma.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-analyses.html#data-wrangler-visualize-scatter-plot">Data Wrangler: scatter plot</a></div>'
        ),
    ),

    # ===================== Q15: Amazon EFS =====================
    card(
        question="<b>Almacenamiento compartido:</b> plataforma de an&aacute;lisis de sentimiento que necesita <b>acceso concurrente desde m&uacute;ltiples instancias EC2</b> (preprocesamiento, entrenamiento e inferencia) sobre grandes vol&uacute;menes de texto. &iquest;Qu&eacute; opci&oacute;n cumple?",
        options=[
            "AWS DataSync, agente de transferencia de datos entre almacenamientos por la red con verificaci&oacute;n",
            "Amazon EBS, volumen de bloques de baja latencia adjunto normalmente a una &uacute;nica instancia EC2",
            "Amazon EFS, sistema de archivos NFS compartido y el&aacute;stico montable por muchas instancias a la vez",
            "AWS Storage Gateway, servicio h&iacute;brido que conecta almacenamiento on-premises con la nube de AWS",
        ],
        correct=2,
        key="mla01-q15",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon EFS.</div>'
            '<p><b>El problema:</b> varias instancias EC2 deben leer/escribir <b>los mismos archivos a la vez</b>. Se necesita un file system compartido.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> EFS es un file system NFS el&aacute;stico que se monta simult&aacute;neamente en muchas instancias, perfecto para acceso concurrente.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DataSync:</b> transfiere datos entre almacenamientos; no es un file system compartido montable.</li>'
            '<li><b>EBS:</b> volumen de bloques atado normalmente a una sola instancia; no da acceso concurrente amplio.</li>'
            '<li><b>Storage Gateway:</b> integra on-premises con la nube; no es el file system compartido para el fleet EC2.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Concurrente desde muchas EC2" = EFS (NFS). "Una instancia, bloques" = EBS. "Alto rendimiento HPC/ML" = FSx for Lustre.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html">Amazon EFS</a></div>'
        ),
    ),

    # ===================== Q16: JSON Lines =====================
    card(
        question="<b>Formato para parseo en tiempo real:</b> detecci&oacute;n de fraude que ingiere datos <b>diversos</b> (estructurados, semi y no estructurados) y requiere <b>parseo y an&aacute;lisis en tiempo real</b>, registro por registro. &iquest;Qu&eacute; formato es el mejor?",
        options=[
            "ORC, formato columnar comprimido optimizado para consultas anal&iacute;ticas por lotes sobre datos en reposo",
            "JSON Lines, un objeto JSON por l&iacute;nea, flexible y f&aacute;cil de parsear registro a registro en streaming",
            "XML, formato jer&aacute;rquico autodescriptivo pero verboso y con alto overhead de parseo por documento",
            "Parquet, formato columnar orientado a lecturas anal&iacute;ticas masivas m&aacute;s que a streaming registro a registro",
        ],
        correct=1,
        key="mla01-q16",
        answer=(
            '<div class="verdict">Correcta: {{L}} - JSON Lines.</div>'
            '<p><b>El problema:</b> datos heterog&eacute;neos que llegan en streaming y deben parsearse <b>registro por registro en tiempo real</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> JSON Lines (un objeto JSON por l&iacute;nea) es flexible para datos variados y se parsea l&iacute;nea a l&iacute;nea, ideal para procesamiento en vivo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>ORC:</b> columnar por lotes; pensado para analytics en reposo, no para parseo streaming registro a registro.</li>'
            '<li><b>XML:</b> verboso y pesado de parsear en tiempo real; a&ntilde;ade overhead.</li>'
            '<li><b>Parquet:</b> columnar para lecturas anal&iacute;ticas masivas; no es &oacute;ptimo para streaming l&iacute;nea a l&iacute;nea.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Streaming/registro-a-registro y datos mixtos = JSON Lines. Analytics por lotes = columnar (Parquet/ORC).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/blogs/machine-learning/prepare-and-analyze-json-and-orc-data-with-amazon-sagemaker-data-wrangler/">AWS blog: JSON y ORC en Data Wrangler</a></div>'
        ),
    ),

    # ===================== Q17: aumentar shards en Kinesis =====================
    card(
        question="<b>Kinesis - throughput:</b> el cuello de botella est&aacute; en la ingesta <b>de Kinesis Data Streams hacia S3</b> (alta latencia, bajo throughput), seg&uacute;n CloudWatch. &iquest;Qu&eacute; soluci&oacute;n mejora el rendimiento de ingesta?",
        options=[
            "Aumentar el n&uacute;mero de shards en Kinesis Data Streams para elevar la capacidad de ingesta paralela",
            "Aplicar compresi&oacute;n de los datos antes de enviarlos a Kinesis Data Streams para reducir su tama&ntilde;o",
            "Aplicar deduplicaci&oacute;n de los datos antes de enviarlos a Kinesis Data Streams para eliminar repetidos",
            "Aumentar el n&uacute;mero de shards aprovisionados en Amazon Data Firehose para escalar la entrega a S3",
        ],
        correct=0,
        key="mla01-q17",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Aumentar los shards en Kinesis Data Streams.</div>'
            '<p><b>El problema:</b> el <b>shard</b> es la unidad de capacidad de Kinesis Data Streams; cada uno tiene l&iacute;mites fijos de escritura/lectura. Si el throughput es bajo, faltan shards.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> a&ntilde;adir shards aumenta la capacidad paralela de ingesta y baja la latencia hacia downstream.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Compresi&oacute;n:</b> comprimir reduce los bytes por registro y puede aliviar el l&iacute;mite de 1&nbsp;MB/s por shard, pero no el l&iacute;mite de registros/s ni aumenta el n&uacute;mero de shards, as&iacute; que no resuelve el cuello de forma general; a&ntilde;adir shards s&iacute;.</li>'
            '<li><b>Deduplicaci&oacute;n:</b> quita repetidos pero no aumenta la capacidad de ingesta del stream.</li>'
            '<li><b>Shards en Firehose:</b> Firehose no usa shards aprovisionados; ese concepto es de Kinesis Data Streams, as&iacute; que la opci&oacute;n es t&eacute;cnicamente inv&aacute;lida.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> En Kinesis Data Streams, escalas throughput sumando shards. Firehose escala autom&aacute;tico (no tiene shards aprovisionados).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://repost.aws/knowledge-center/kinesis-data-streams-open-shards">re:Post: shards en Kinesis</a></div>'
        ),
    ),

    # ===================== Q18: matching -> pasos (columnar) =====================
    card(
        question="<b>Optimizar formato de datos:</b> datos de interacciones en CSV para un motor de recomendaci&oacute;n. Tras filtrar columnas irrelevantes y comprimir, &iquest;a qu&eacute; formato conviene transformar el CSV para <b>acceso m&aacute;s r&aacute;pido</b>?",
        options=[
            "Transformar el CSV a un formato de almacenamiento columnar para lectura m&aacute;s r&aacute;pida por columnas",
            "Convertir el CSV a un formato jer&aacute;rquico como JSON para representar estructuras anidadas complejas",
            "Mantener el CSV existente y procesar todas las columnas tal cual, sin cambiar el formato de almacenamiento",
            "Agregar (aggregate) los datos por el nombre de los creadores de contenido antes de cualquier otra cosa",
        ],
        correct=0,
        key="mla01-q18",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Transformar el CSV a un formato columnar.</div>'
            '<p><b>El problema:</b> un motor de recomendaci&oacute;n hace lecturas intensivas por columnas; CSV (por filas) es ineficiente a gran escala.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> un formato <b>columnar</b> (p. ej. Parquet) permite leer solo las columnas necesarias, acelerando el acceso y reduciendo E/S.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Convertir a JSON:</b> jer&aacute;rquico y no optimizado para lecturas intensivas; a&ntilde;ade overhead y ralentiza el retrieval.</li>'
            '<li><b>Mantener CSV tal cual:</b> por filas y sin filtrar; procesa datos irrelevantes y rinde peor.</li>'
            '<li><b>Agregar por nombre de creadores:</b> ese campo no es relevante para el motor (que se enfoca en interacciones del usuario); a&ntilde;ade complejidad in&uacute;til.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Pipeline t&iacute;pico: filtrar columnas -> comprimir -> convertir a columnar (Parquet) para consultas r&aacute;pidas.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html">Almacenamiento columnar</a></div>'
        ),
    ),

    # ===================== Q19: S3 Transfer Acceleration =====================
    card(
        question="<b>Transferencia global a S3:</b> subidas y descargas frecuentes de datasets grandes en S3 <b>desde ubicaciones globales</b>, con meta de reducir latencia y acelerar el entrenamiento. &iquest;Qu&eacute; servicio recomendar?",
        options=[
            "AWS Global Accelerator, que enruta tr&aacute;fico TCP/UDP de aplicaciones por la red edge de AWS a endpoints",
            "Amazon S3 Transfer Acceleration, que usa las edge locations de CloudFront para acelerar subidas/bajadas a S3",
            "AWS Direct Connect, enlace dedicado de red privada entre el data center on-premises y la regi&oacute;n de AWS",
            "AWS DataSync, agente para copiar grandes vol&uacute;menes entre almacenamientos con verificaci&oacute;n de integridad",
        ],
        correct=1,
        key="mla01-q19",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon S3 Transfer Acceleration.</div>'
            '<p><b>El problema:</b> acelerar transferencias <b>a/desde S3</b> desde clientes distribuidos por el mundo.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Transfer Acceleration enruta el tr&aacute;fico por las <b>edge locations</b> de CloudFront hasta el bucket, reduciendo latencia en distancias largas.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Global Accelerator:</b> acelera aplicaciones (endpoints TCP/UDP como ALB/EC2), no subidas directas a un bucket S3.</li>'
            '<li><b>Direct Connect:</b> enlace dedicado desde un sitio fijo; no resuelve accesos globales dispersos ni es "sin cambiar el setup".</li>'
            '<li><b>DataSync:</b> orientado a migraci&oacute;n/replicaci&oacute;n programada, no a acelerar cada subida/descarga interactiva global.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Acelerar hacia S3 desde lejos" = S3 Transfer Acceleration. "Acelerar una app con endpoints" = Global Accelerator.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html">S3 Transfer Acceleration</a></div>'
        ),
    ),

    # ===================== Q20: S3 data lake =====================
    card(
        question="<b>Data lake:</b> una plataforma de e-commerce genera transacciones, im&aacute;genes de producto y rese&ntilde;as. Se requiere almacenamiento <b>seguro, muy durable y altamente disponible</b>. &iquest;Qu&eacute; servicio es el m&aacute;s adecuado?",
        options=[
            "Amazon FSx for Lustre, sistema de archivos paralelo de alto rendimiento para cargas HPC y de ML",
            "Amazon S3, almacenamiento de objetos con 11 nueves de durabilidad, base t&iacute;pica de un data lake",
            "Amazon EFS, file system NFS el&aacute;stico compartido entre m&uacute;ltiples instancias EC2 por la red",
            "AWS Storage Gateway, servicio h&iacute;brido que conecta almacenamiento on-premises con la nube de AWS",
        ],
        correct=1,
        key="mla01-q20",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon S3.</div>'
            '<p><b>El problema:</b> almacenar grandes vol&uacute;menes variados (transacciones, im&aacute;genes, texto) de forma segura, durable y disponible: la definici&oacute;n de un <b>data lake</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> S3 ofrece 11 nueves de durabilidad, alta disponibilidad, seguridad y escalabilidad pr&aacute;cticamente ilimitada; es el est&aacute;ndar para data lakes en AWS.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>FSx for Lustre:</b> sistema de archivos paralelo de alto rendimiento (tiene modos scratch y persistente), pero no es un almac&eacute;n de objetos durable y de bajo costo pensado como base de un data lake; para eso es S3.</li>'
            '<li><b>EFS:</b> file system compartido, m&aacute;s caro y no pensado como base de data lake a escala de objetos.</li>'
            '<li><b>Storage Gateway:</b> integra on-premises con la nube; no es el almacenamiento primario del data lake.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Data lake" en AWS = Amazon S3 casi siempre (durabilidad, escala, integraci&oacute;n con Glue/Athena/EMR).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/amazon-s3-data-lake-storage-platform.html">S3 como data lake</a></div>'
        ),
    ),

    # ===================== Q21: matching bias metrics -> 3 cartas =====================
    card(
        question="<b>M&eacute;tricas de sesgo (Clarify):</b> se quiere <b>comparar la proporci&oacute;n de resultados positivos entre distintos grupos raciales</b>. &iquest;Qu&eacute; m&eacute;trica de sesgo pre-entrenamiento aplica?",
        options=[
            "Difference in Proportions of Labels (DPL)",
            "Class Imbalance (CI)",
            "Total Variation Distance (TVD)",
            "Kullback-Leibler Divergence (KL)",
        ],
        correct=0,
        key="mla01-q21a",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Difference in Proportions of Labels (DPL).</div>'
            '<p><b>El problema:</b> se compara la <b>proporci&oacute;n de etiquetas positivas</b> entre grupos demogr&aacute;ficos.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> DPL mide exactamente la disparidad en la proporci&oacute;n de resultados positivos entre grupos, revelando favoritismo hacia uno.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>CI:</b> mide representaci&oacute;n de clases (imbalance), no proporci&oacute;n de resultados positivos entre grupos.</li>'
            '<li><b>TVD:</b> mide la m&aacute;xima divergencia de distribuciones, no la diferencia de proporciones de etiquetas.</li>'
            '<li><b>KL:</b> compara distribuciones de probabilidad en general; no est&aacute; hecha para comparar proporciones de etiquetas por grupo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> DPL = diferencia de proporci&oacute;n de positivos entre grupos. CI = imbalance de representaci&oacute;n. TVD = m&aacute;xima disparidad de distribuciones.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-measure-data-bias.html">Clarify: m&eacute;tricas de sesgo</a></div>'
        ),
    ),
    card(
        question="<b>M&eacute;tricas de sesgo (Clarify):</b> se debe analizar el dataset para <b>medir el desbalance entre instancias masculinas y femeninas</b>. &iquest;Qu&eacute; m&eacute;trica de sesgo pre-entrenamiento aplica?",
        options=[
            "Class Imbalance (CI)",
            "Difference in Proportions of Labels (DPL)",
            "Total Variation Distance (TVD)",
            "Kullback-Leibler Divergence (KL)",
        ],
        correct=0,
        key="mla01-q21b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Class Imbalance (CI).</div>'
            '<p><b>El problema:</b> medir cu&aacute;nto est&aacute; sub o sobrerrepresentado un grupo (hombres vs mujeres) en el dataset.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> CI eval&uacute;a la representaci&oacute;n de clases/grupos y revela desbalances que podr&iacute;an sesgar el modelo hacia la clase mayoritaria.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DPL:</b> mide proporci&oacute;n de resultados positivos entre grupos, no la representaci&oacute;n/imbalance del grupo.</li>'
            '<li><b>TVD:</b> mide m&aacute;xima divergencia de distribuciones de resultados, no el conteo/representaci&oacute;n.</li>'
            '<li><b>KL:</b> compara distribuciones en general; no es la m&eacute;trica de imbalance de clases.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Desbalance de representaci&oacute;n entre grupos" (m/f) = Class Imbalance (CI).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-data-bias.html">Clarify: detectar sesgo</a></div>'
        ),
    ),
    card(
        question="<b>M&eacute;tricas de sesgo (Clarify):</b> entre dos grupos (definidos por nivel de ingreso), se quiere una m&eacute;trica de sesgo pre-entrenamiento que sea una <b>distancia ACOTADA (rango 0 a 1) y SIM&Eacute;TRICA</b> entre las dos distribuciones de resultados (mismo valor sin importar qu&eacute; grupo se tome primero). &iquest;Qu&eacute; m&eacute;trica cumple?",
        options=[
            "Total Variation Distance (TVD)",
            "Difference in Proportions of Labels (DPL)",
            "Class Imbalance (CI)",
            "Kullback-Leibler Divergence (KL)",
        ],
        correct=0,
        key="mla01-q21c",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Total Variation Distance (TVD).</div>'
            '<p><b>El problema:</b> se pide una distancia entre las distribuciones de resultados de dos grupos que cumpla DOS propiedades concretas: estar <b>acotada en [0, 1]</b> y ser <b>sim&eacute;trica</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> la TVD es la mitad de la norma L1 entre las dos distribuciones; por construcci&oacute;n queda <b>acotada entre 0 y 1</b> y es <b>sim&eacute;trica</b> (TVD(P,Q) = TVD(Q,P)). Cumple exactamente las dos propiedades pedidas.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DPL:</b> compara la proporci&oacute;n de positivos entre grupos; no es una distancia acotada-sim&eacute;trica entre distribuciones completas.</li>'
            '<li><b>CI:</b> mide la representaci&oacute;n/imbalance del grupo, no la distancia entre distribuciones de resultados.</li>'
            '<li><b>KL:</b> Kullback-Leibler tambi&eacute;n compara dos distribuciones, pero NO est&aacute; acotada (puede tender a infinito) y NO es sim&eacute;trica (KL(P,Q) &ne; KL(Q,P)); por eso queda descartada justamente por las dos propiedades exigidas en el enunciado.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> El desempate TVD vs KL es por las propiedades: TVD es acotada [0,1] y sim&eacute;trica; KL no es acotada ni sim&eacute;trica. Si el enunciado pide "acotada y sim&eacute;trica" = TVD.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-measure-data-bias.html">Clarify: m&eacute;tricas de sesgo</a></div>'
        ),
    ),

    # ===================== Q22: DataSync =====================
    card(
        question="<b>Migraci&oacute;n on-prem a EFS:</b> mover un gran dataset de entrenamiento desde servidores on-premises a Amazon EFS, con <b>m&iacute;nima interrupci&oacute;n</b> y manejo eficiente de grandes vol&uacute;menes. &iquest;Qu&eacute; servicio es el mejor?",
        options=[
            "AWS Transfer Family, que expone un endpoint SFTP hacia Amazon EFS para que los servidores on-premises suban archivos uno a uno",
            "AWS Storage Gateway en modo File Gateway, que cachea localmente y sincroniza los archivos con Amazon EFS de forma continua",
            "Montar el EFS por VPN y copiar los archivos con rsync desde los servidores on-premises en una ventana de mantenimiento",
            "AWS DataSync, transferencia administrada y paralela on-premises a Amazon EFS con verificaci&oacute;n de integridad y m&iacute;nima interrupci&oacute;n",
        ],
        correct=3,
        key="mla01-q22",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS DataSync.</div>'
            '<p><b>El problema:</b> migrar un gran dataset on-premises a <b>Amazon EFS</b> una sola vez, r&aacute;pido, con integridad y m&iacute;nima interrupci&oacute;n. Varias opciones tocan EFS; hay que elegir la de <b>migraci&oacute;n administrada</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> DataSync copia datos on-premises a EFS (tambi&eacute;n S3/FSx) en paralelo y a alta velocidad, con <b>verificaci&oacute;n de integridad</b> y programaci&oacute;n autom&aacute;tica, ideal para un traslado masivo puntual.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Transfer Family (SFTP a EFS):</b> tambi&eacute;n escribe a EFS, pero est&aacute; pensado para flujos SFTP archivo a archivo, no para copiar en paralelo un dataset enorme con verificaci&oacute;n; ser&iacute;a lento.</li>'
            '<li><b>Storage Gateway File Gateway:</b> mantiene una cach&eacute; local sincronizada de forma <b>continua</b> con AWS; sirve para acceso h&iacute;brido permanente, no para una migraci&oacute;n masiva de una sola vez.</li>'
            '<li><b>rsync por VPN a EFS montado:</b> funciona y llega a EFS, pero es un proceso manual, sin paralelismo ni verificaci&oacute;n administrada, con m&aacute;s riesgo e interrupci&oacute;n que DataSync.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Migraci&oacute;n administrada on-prem -> EFS/S3/FSx con verificaci&oacute;n y m&iacute;nima interrupci&oacute;n = AWS DataSync. Acceso h&iacute;brido continuo = Storage Gateway.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html">AWS DataSync</a></div>'
        ),
    ),

    # ===================== Q23: Glue visual ETL =====================
    card(
        question="<b>Transformar JSON con menor esfuerzo:</b> procesar grandes vol&uacute;menes de JSON en S3 para entrenamiento, con una soluci&oacute;n <b>automatizada y de m&iacute;nimo esfuerzo operativo</b>. &iquest;Qu&eacute; enfoque conviene?",
        options=[
            "Crear un cl&uacute;ster EMR y usar Apache Drill para transformar el JSON a un formato apto para ML",
            "Usar AWS Step Functions para orquestar varias funciones Lambda que procesen el JSON por lotes",
            "Configurar una Lambda disparada por eventos S3 que procese y transforme el JSON con Pandas a medida",
            "Configurar un job de AWS Glue y usar el editor visual de ETL para transformar el JSON de S3",
        ],
        correct=3,
        key="mla01-q23",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Job de AWS Glue con el editor visual de ETL.</div>'
            '<p><b>El problema:</b> transformar JSON a gran escala con <b>m&iacute;nimo esfuerzo operativo</b> y de forma automatizada.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Glue es ETL serverless y su editor visual permite construir la transformaci&oacute;n sin gestionar servidores ni escribir mucho c&oacute;digo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>EMR + Drill:</b> exige provisionar y administrar un cl&uacute;ster; m&aacute;s overhead operativo.</li>'
            '<li><b>Step Functions + Lambdas:</b> hay que dise&ntilde;ar y mantener la orquestaci&oacute;n y el c&oacute;digo; m&aacute;s complejo.</li>'
            '<li><b>Lambda + Pandas:</b> c&oacute;digo a medida y l&iacute;mites de Lambda (tiempo/memoria) para grandes vol&uacute;menes.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Transformar datos con m&iacute;nimo esfuerzo/serverless" = AWS Glue (visual ETL). Evita construir orquestaciones manuales.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/author-job-glue.html">Glue: crear jobs</a></div>'
        ),
    ),

    # ===================== Q24: execution role (403) =====================
    card(
        question="<b>SageMaker 403 a S3:</b> un Processing job conecta al bucket pero recibe <b>403</b> al leer los .csv. El bucket existe y el job usa un VPC endpoint. &iquest;Cu&aacute;l es la causa m&aacute;s probable?",
        options=[
            "El usuario IAM que cre&oacute; el Processing job no tiene permisos de administrador en la cuenta",
            "El execution role asociado al Processing job carece de permisos para acceder al bucket S3",
            "La pol&iacute;tica del bucket S3 deniega expl&iacute;citamente el acceso al Processing job en cuesti&oacute;n",
            "El bucket S3 est&aacute; en una regi&oacute;n de AWS distinta a la del Processing job de SageMaker",
        ],
        correct=1,
        key="mla01-q24",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Al execution role le faltan permisos sobre el bucket.</div>'
            '<p><b>El problema:</b> un <b>403</b> es de <b>autorizaci&oacute;n</b>. El Processing job act&uacute;a con su <b>execution role</b> (no con el usuario que lo cre&oacute;).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> si ese role no tiene s3:GetObject/ListBucket sobre el bucket, S3 responde 403 aunque la conexi&oacute;n (VPC endpoint) funcione.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Usuario sin admin:</b> el job usa el execution role, no los permisos del usuario creador; adem&aacute;s no se requiere admin.</li>'
            '<li><b>Bucket policy deniega:</b> un Deny expl&iacute;cito en la bucket policy sobre s3:GetObject tambi&eacute;n producir&iacute;a el mismo 403 al leer los .csv, pero es menos frecuente: requiere que alguien haya escrito ese Deny concreto. Lo t&iacute;pico es que al execution role le falten s3:GetObject/ListBucket (o kms:Decrypt si hay CMK), por eso es la causa m&aacute;s probable.</li>'
            '<li><b>Regi&oacute;n distinta:</b> eso no produce 403 sino errores de resoluci&oacute;n/redirecci&oacute;n; y como conecta, no es el caso.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> 403 de SageMaker hacia S3 = casi siempre el execution role sin s3:GetObject/ListBucket (o kms:Decrypt con CMK); un Deny en bucket policy tambi&eacute;n da 403 pero es menos com&uacute;n. 404 = no existe. Timeout = red/VPC.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createprocessingjob-perms">SageMaker roles: Processing</a></div>'
        ),
    ),

    # ===================== Q25: Ground Truth =====================
    card(
        question="<b>Datos supervisados con menor esfuerzo:</b> rese&ntilde;as crudas <b>sin etiquetar</b> en S3. Antes de poder entrenar un modelo <b>propio</b> de an&aacute;lisis de sentimiento en SageMaker, hay que <b>anotar/etiquetar</b> cada rese&ntilde;a (positivo/negativo/neutral) con alta calidad para producir el dataset supervisado (no se busca clasificar el sentimiento directamente con un servicio ya entrenado). &iquest;Qu&eacute; soluci&oacute;n logra ese etiquetado con m&iacute;nimo esfuerzo?",
        options=[
            "Usar el algoritmo Neural Topic Model (NTM) de SageMaker para organizar autom&aacute;ticamente los datasets",
            "Crear un labeling job con SageMaker Ground Truth para anotar las rese&ntilde;as con alta calidad",
            "Entrenar una red neuronal convolucional (CNN) desde cero para categorizar autom&aacute;ticamente las rese&ntilde;as",
            "Usar Amazon Comprehend para analizar y clasificar el sentimiento de las rese&ntilde;as directamente",
        ],
        correct=1,
        key="mla01-q25",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Labeling job con SageMaker Ground Truth.</div>'
            '<p><b>El problema:</b> se necesitan <b>etiquetas de alta calidad</b> para datos crudos; Ground Truth es el servicio de etiquetado administrado de SageMaker.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Ground Truth orquesta el etiquetado (humano y asistido) con flujos listos, generando anotaciones consistentes con poco esfuerzo operativo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>NTM:</b> descubre t&oacute;picos, no etiqueta sentimiento; no produce las anotaciones supervisadas necesarias.</li>'
            '<li><b>CNN desde cero:</b> requiere datos ya etiquetados y mucho esfuerzo; no resuelve el etiquetado inicial.</li>'
            '<li><b>Comprehend:</b> clasifica sentimiento, pero el requisito es <b>etiquetar</b> el dataset para entrenar un modelo propio en SageMaker, no inferir directo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Etiquetar/anotar datos" = SageMaker Ground Truth. "Analizar sentimiento ya, sin entrenar" = Comprehend.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html">SageMaker Ground Truth</a></div>'
        ),
    ),

    # ===================== Q26: Ordered split =====================
    card(
        question="<b>Split cronol&oacute;gico:</b> datos ordenados por fecha de alta; el split train/validation debe <b>preservar estrictamente el orden temporal</b> para evitar fuga de datos futuros y overfitting, <b>con el m&iacute;nimo esfuerzo operativo</b>. &iquest;Qu&eacute; transform de Data Wrangler usar?",
        options=[
            "Usar el transform Ordered split de Amazon SageMaker Data Wrangler para respetar el orden temporal",
            "Ejecutar un script Python en un SageMaker Processing job para dividir el dataset por una clave",
            "Usar el transform Stratified split de Amazon SageMaker Data Wrangler para balancear clases al dividir",
            "Usar una receta de AWS Glue DataBrew para realizar un split aleatorio (randomized) del dataset",
        ],
        correct=0,
        key="mla01-q26",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Ordered split en SageMaker Data Wrangler.</div>'
            '<p><b>El problema:</b> en datos temporales, mezclar el orden filtra informaci&oacute;n del futuro al entrenamiento (data leakage) y da m&eacute;tricas enga&ntilde;osamente optimistas.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> el <b>Ordered split</b> divide respetando la secuencia (entrena con el pasado, valida con el futuro), evitando la fuga.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Script en Processing job:</b> un script a medida s&iacute; puede dividir cronol&oacute;gicamente, pero exige escribir y mantener c&oacute;digo y <b>reimplementar a mano</b> el split ordenado que Data Wrangler ya ofrece como transform administrado; es m&aacute;s esfuerzo operativo para el mismo resultado.</li>'
            '<li><b>Stratified split:</b> preserva proporci&oacute;n de clases, no el orden temporal; puede reordenar y filtrar futuro.</li>'
            '<li><b>Split aleatorio en DataBrew:</b> lo aleatorio rompe la cronolog&iacute;a, justo lo que se quiere evitar.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Series de tiempo -> Ordered split (nunca aleatorio) para no filtrar el futuro al pasado.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/blogs/machine-learning/create-train-test-and-validation-splits-on-your-data-for-machine-learning-with-amazon-sagemaker-data-wrangler/">Data Wrangler: splits</a></div>'
        ),
    ),

    # ===================== Q27: AWS DMS homogeneo =====================
    card(
        question="<b>Migraci&oacute;n MySQL a Aurora:</b> hacer una migraci&oacute;n <b>puntual (one-time)</b> de datos de entrenamiento de un MySQL on-premises a Amazon Aurora (compatible con MySQL). &iquest;Cu&aacute;l es el enfoque m&aacute;s adecuado?",
        options=[
            "Usar AWS DMS para una migraci&oacute;n homog&eacute;nea (MySQL a Aurora MySQL, motores compatibles) de forma administrada",
            "Usar AWS DMS con Schema Conversion Tool para una migraci&oacute;n heterog&eacute;nea convirtiendo el esquema de origen",
            "Exportar el MySQL a un volcado en Amazon S3 y cargarlo en Aurora con sentencias LOAD, orquestando el proceso a mano",
            "Definir un job de AWS Glue que lea el MySQL por JDBC y escriba las tablas en Aurora en una &uacute;nica corrida por lotes",
        ],
        correct=0,
        key="mla01-q27",
        answer=(
            '<div class="verdict">Correcta: {{L}} - AWS DMS, migraci&oacute;n homog&eacute;nea.</div>'
            '<p><b>El problema:</b> MySQL y Aurora MySQL son motores <b>compatibles</b>: es una migraci&oacute;n <b>homog&eacute;nea</b> puntual, que DMS realiza administrada con m&iacute;nimo esfuerzo.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> AWS DMS migra esquema y datos entre motores compatibles con m&iacute;nima interrupci&oacute;n y sin c&oacute;digo a medida, que es lo m&aacute;s adecuado para un traslado one-time.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DMS + Schema Conversion Tool (heterog&eacute;nea):</b> SCT es para motores <b>distintos</b> (p.ej. Oracle a Aurora); aqu&iacute; origen y destino son MySQL-compatibles, as&iacute; que convertir el esquema es un paso innecesario.</li>'
            '<li><b>Export a S3 + LOAD manual:</b> t&eacute;cnicamente logra el one-time, pero es un proceso manual en varios pasos, sin la gesti&oacute;n de esquema, reintentos y validaci&oacute;n que DMS ofrece de serie.</li>'
            '<li><b>Job de AWS Glue por JDBC:</b> Glue es un ETL de <b>transformaci&oacute;n</b>; para una migraci&oacute;n directa entre motores compatibles a&ntilde;ade complejidad y no aporta sobre la migraci&oacute;n administrada de DMS.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Motores compatibles = migraci&oacute;n homog&eacute;nea con DMS. Motores distintos = DMS + Schema Conversion Tool (heterog&eacute;nea).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/dms/">AWS DMS</a></div>'
        ),
    ),

    # ===================== Q28: S3 Transfer Acceleration =====================
    card(
        question="<b>Acelerar subida a S3:</b> un dataset recolectado desde varias ubicaciones sube lento a S3. Se busca acelerar <b>sin cambiar mucho el setup actual</b>. &iquest;Qu&eacute; soluci&oacute;n es m&aacute;s efectiva?",
        options=[
            "Usar S3 Transfer Acceleration, que enruta la subida por edge locations sin cambiar el flujo hacia el bucket",
            "Usar AWS Data Transfer Terminal, migraci&oacute;n f&iacute;sica offline en una instalaci&oacute;n de AWS con equipo propio",
            "Utilizar AWS Direct Connect, un enlace de red dedicado y privado desde un sitio fijo hacia la regi&oacute;n de AWS",
            "Usar Amazon S3 multipart upload est&aacute;ndar, subiendo el dataset en partes en paralelo pero sin acelerar por edge",
        ],
        correct=0,
        key="mla01-q28",
        answer=(
            '<div class="verdict">Correcta: {{L}} - S3 Transfer Acceleration.</div>'
            '<p><b>El problema:</b> acelerar subidas globales a S3 con cambios m&iacute;nimos.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Transfer Acceleration solo requiere activarlo en el bucket y usar el endpoint acelerado; enruta por edge locations reduciendo latencia sin rehacer el pipeline.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Data Transfer Terminal:</b> transferencia f&iacute;sica, un cambio grande de proceso; no es "sin cambiar el setup".</li>'
            '<li><b>Direct Connect:</b> enlace dedicado desde un sitio fijo; no ayuda a m&uacute;ltiples ubicaciones dispersas ni es cambio m&iacute;nimo.</li>'
            '<li><b>Multipart upload est&aacute;ndar:</b> paraleliza la subida en partes, lo que ayuda con archivos grandes, pero sigue viajando por la ruta p&uacute;blica de internet; no aprovecha las edge locations, as&iacute; que ante alta latencia desde ubicaciones lejanas rinde peor que Transfer Acceleration.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Acelerar S3 con m&iacute;nimos cambios" = S3 Transfer Acceleration (solo activar y usar el endpoint acelerado).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html">S3 Transfer Acceleration</a></div>'
        ),
    ),

    # ===================== Q29: Robust Scaler =====================
    # Nota de fidelidad: la fuente listaba "Z-score normalization" como distractor,
    # pero Z-score == Standard Scaler (misma tecnica), lo que duplicaba una opcion.
    # Se sustituyo por "Min-Max Scaler" (scaler real de Data Wrangler) para eliminar
    # esa redundancia; la respuesta correcta (Robust Scaler) no cambia.
    card(
        question="<b>Escalado con outliers:</b> en Data Wrangler, features con rangos muy distintos y <b>outliers</b> en CreditScore (valores at&iacute;picos tan bajos como 5). Hay que escalar todo a rango similar siendo <b>robusto a outliers</b>. &iquest;Qu&eacute; funci&oacute;n usar?",
        options=[
            "Robust Scaler, que escala con mediana y rango intercuartil (IQR), resistente a valores at&iacute;picos",
            "Standard Scaler, que centra en la media y divide por la desviaci&oacute;n est&aacute;ndar de cada feature",
            "Min-Max Scaler, que reescala linealmente cada feature al rango [0,1] tomando el valor m&iacute;nimo y m&aacute;ximo",
            "L1 normalization, que escala cada vector para que la suma de los valores absolutos sea igual a uno",
        ],
        correct=0,
        key="mla01-q29",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Robust Scaler.</div>'
            '<p><b>El problema:</b> hay outliers que distorsionan media y desviaci&oacute;n. Se necesita un escalado <b>robusto</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Robust Scaler usa <b>mediana</b> e <b>IQR</b> (rango intercuartil), estad&iacute;sticos poco sensibles a valores extremos, por eso resiste outliers.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Standard Scaler:</b> usa media y desviaci&oacute;n, ambas muy afectadas por outliers.</li>'
            '<li><b>Min-Max Scaler:</b> reescala linealmente al rango [0,1] pero es muy sensible a outliers (un valor extremo comprime el resto), por eso no es lo adecuado cuando hay outliers; el m&eacute;todo robusto usa mediana e IQR.</li>'
            '<li><b>L1 normalization:</b> normaliza la magnitud del vector, no maneja outliers por feature en escalado a rango comparable.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Outliers presentes -> Robust Scaler (mediana + IQR). Sin outliers -> Standard/Z-score suele bastar.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-transform.html#data-wrangler-transform-process-numeric">Data Wrangler: transform num&eacute;rico</a></div>'
        ),
    ),

    # ===================== Q30: EMR Spark -> RecordIO-Protobuf =====================
    card(
        question="<b>Convertir a RecordIO-Protobuf:</b> hay que convertir un dataset de entrenamiento a <b>RecordIO-Protobuf</b> (para Pipe mode de SageMaker seq2seq). El equipo <b>ya usa EMR Spark</b> para otras cargas. &iquest;Qu&eacute; opci&oacute;n es la m&aacute;s adecuada?",
        options=[
            "Desplegar una tarea AWS Fargate con un contenedor propio que haga la conversi&oacute;n del dataset a RecordIO",
            "Montar un cl&uacute;ster EMR, cargar el dataset de S3 y usar Apache Spark para hacer las conversiones necesarias",
            "Usar Amazon Redshift Spectrum para consultar el dataset en S3 y realizar las conversiones al formato requerido",
            "Usar un stream de Firehose para ingerir el dataset desde S3 y transformarlo al formato RecordIO-Protobuf",
        ],
        correct=1,
        key="mla01-q30",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Cl&uacute;ster EMR con Apache Spark.</div>'
            '<p><b>El problema:</b> transformar grandes vol&uacute;menes a RecordIO-Protobuf; el equipo <b>ya tiene experiencia y pipeline EMR Spark</b>, as&iacute; que reutilizarlo minimiza fricci&oacute;n.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Spark en EMR procesa datos a escala y, con la librer&iacute;a de serializaci&oacute;n protobuf, escribe RecordIO-Protobuf; aprovecha herramientas ya conocidas por el equipo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Fargate contenedor propio:</b> exige construir y mantener un contenedor a medida; m&aacute;s trabajo que reutilizar EMR.</li>'
            '<li><b>Redshift Spectrum:</b> consulta datos en S3 con SQL; no est&aacute; pensado para producir RecordIO-Protobuf.</li>'
            '<li><b>Firehose:</b> es ingesta de streaming; no convierte datasets por lotes a RecordIO-Protobuf.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> RecordIO-Protobuf es el formato compacto para algoritmos built-in de SageMaker en Pipe mode; EMR/Spark lo procesa a escala y, con la librer&iacute;a de serializaci&oacute;n protobuf instalada, escribe ese formato (no es un writer nativo out-of-the-box).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/cdf-training.html">SageMaker: formatos de entrenamiento</a></div>'
        ),
    ),

    # ===================== Q31: Data Wrangler en Canvas =====================
    card(
        question="<b>Faltantes con m&iacute;nimo overhead:</b> datos de series de tiempo en Redshift con valores faltantes; se quiere una soluci&oacute;n <b>totalmente administrada, dentro de SageMaker</b>, para preprocesar. &iquest;Qu&eacute; enfoque es el m&aacute;s eficiente operativamente?",
        options=[
            "Preprocesar con las funciones integradas de SageMaker Data Wrangler dentro de SageMaker Canvas",
            "Usar funciones SQL nativas de Redshift para tratar los faltantes dentro del cl&uacute;ster antes de exportar",
            "Exportar de Redshift a S3 y usar Amazon Athena con sentencias CTAS para preprocesar los faltantes",
            "Desarrollar un script propio en AWS Lambda que identifique y rellene autom&aacute;ticamente los valores faltantes",
        ],
        correct=0,
        key="mla01-q31",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Data Wrangler dentro de Canvas.</div>'
            '<p><b>El problema:</b> preprocesar faltantes de forma administrada y <b>dentro del entorno SageMaker</b>, con m&iacute;nimo overhead.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Data Wrangler (integrado en Canvas) ofrece transformaciones e imputaci&oacute;n de faltantes sin c&oacute;digo, todo dentro de SageMaker.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SQL en Redshift:</b> queda fuera del entorno SageMaker y mezcla la l&oacute;gica de ML con la base de datos.</li>'
            '<li><b>Athena CTAS en S3:</b> agrega pasos de exportaci&oacute;n y otro servicio, fuera de SageMaker; m&aacute;s overhead.</li>'
            '<li><b>Lambda propia:</b> c&oacute;digo a medida a mantener; no es una soluci&oacute;n administrada dentro de SageMaker.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Preprocesar sin c&oacute;digo dentro de SageMaker" = Data Wrangler (en Studio o Canvas).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-data-preparation.html">Canvas: preparaci&oacute;n de datos</a></div>'
        ),
    ),

    # ===================== Q32: Textract + Comprehend para redactar PII/PHI =====================
    card(
        question="<b>Redactar PII/PHI en PDFs:</b> registros m&eacute;dicos en PDF en S3; antes de entrenar hay que <b>detectar y redactar PII/PHI</b> de forma operativamente eficiente. &iquest;Qu&eacute; soluci&oacute;n conviene?",
        options=[
            "Un modelo ready-to-use de SageMaker Canvas que ingiera los PDFs y redacte por s&iacute; solo la PII/PHI",
            "Amazon Textract para extraer el texto de los PDFs y Amazon Comprehend para detectar y redactar la PII/PHI",
            "S3 Object Lambda con una funci&oacute;n propia que llame a Comprehend y redacte la PII/PHI al leer cada objeto",
            "Amazon Textract para extraer el texto y luego un modelo preentrenado de clasificaci&oacute;n de SageMaker JumpStart",
        ],
        correct=1,
        key="mla01-q32",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Textract (extraer texto del PDF) + Amazon Comprehend (detectar y redactar PII/PHI).</div>'
            '<p><b>El problema:</b> detectar y redactar PII (datos personales) y PHI (informaci&oacute;n de salud) en <b>PDFs</b> con el <b>menor esfuerzo operativo</b>. Comprehend solo procesa texto plano, no PDFs.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> <b>Amazon Textract</b> extrae el texto de los PDFs y <b>Amazon Comprehend</b> ejecuta un job as&iacute;ncrono de PII con modo de salida "redacci&oacute;n" (StartPiiEntitiesDetectionJob), que devuelve el texto con cada entidad PII/PHI enmascarada, sin entrenar modelos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Modelo ready-to-use de Canvas:</b> el modelo de "detecci&oacute;n de informaci&oacute;n personal" de Canvas solo acepta texto o tabular y &uacute;nicamente <b>detecta</b> (no redacta) ni procesa PDFs; no cumple el requisito.</li>'
            '<li><b>S3 Object Lambda + funci&oacute;n propia:</b> redacta en el momento de la lectura, pero exige desarrollar y mantener la funci&oacute;n Lambda y sigue necesitando extraer el texto del PDF; m&aacute;s overhead operativo.</li>'
            '<li><b>Textract + JumpStart:</b> un modelo de clasificaci&oacute;n de JumpStart no redacta PII; habr&iacute;a que entrenar o ajustar l&oacute;gica a medida, m&aacute;s esfuerzo que usar Comprehend.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Redactar PII/PHI de documentos = Textract (PDF a texto) + Comprehend (job as&iacute;ncrono de PII con salida redactada). Canvas ready-to-use detecta, no redacta, y no lee PDFs.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/comprehend/latest/dg/redact-api-pii.html">Comprehend: redacci&oacute;n de PII (job as&iacute;ncrono)</a></div>'
        ),
    ),

    # ===================== Q33: Feature Store cross-account =====================
    card(
        question="<b>Compartir features entre cuentas:</b> varias apps de ML requieren entrenamiento e inferencia de <b>baja latencia</b> y necesitan <b>compartir features entre cuentas AWS</b> con m&iacute;nimo overhead. &iquest;Qu&eacute; opci&oacute;n cumple?",
        options=[
            "Usar SageMaker Feature Store con online y offline store y configurar acceso cross-account para compartir features",
            "Usar Amazon RDS para almacenar features y montar replicaci&oacute;n entre bases de datos en distintas cuentas",
            "Guardar las features en Amazon S3 y gestionar manualmente pol&iacute;ticas IAM de acceso por cada cuenta involucrada",
            "Guardar en S3 y usar AWS Glue con DynamicFrames para transformar y catalogar, compartiendo luego entre cuentas",
        ],
        correct=0,
        key="mla01-q33",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Feature Store (online + offline) con acceso cross-account.</div>'
            '<p><b>El problema:</b> se requiere un repositorio de features con <b>online store</b> (baja latencia para inferencia) y <b>offline store</b> (entrenamiento), compartible entre cuentas.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Feature Store es el servicio administrado para esto: online para inferencia r&aacute;pida, offline para entrenamiento, y soporta acceso cross-account con poco overhead.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>RDS con replicaci&oacute;n:</b> no es un feature store; operar replicaci&oacute;n entre cuentas es m&aacute;s complejo y sin online/offline nativos.</li>'
            '<li><b>S3 + IAM manual:</b> gestionar pol&iacute;ticas por cuenta a mano es mucho overhead y no da online store de baja latencia.</li>'
            '<li><b>S3 + Glue DynamicFrames:</b> es ETL/cat&aacute;logo, no un feature store con inferencia de baja latencia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Compartir features + baja latencia + poco overhead" = SageMaker Feature Store (online store para inferencia, offline para training).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html">SageMaker Feature Store</a></div>'
        ),
    ),

    # ===================== Q34: anomalias tiempo real (Select TWO) =====================
    card(
        question="<b>Anomal&iacute;as en tiempo real:</b> miles de sensores IoT env&iacute;an datos <b>sin buffering</b> y hay que detectar anomal&iacute;as <b>a medida que llegan, sin retraso</b>. &iquest;Qu&eacute; pareja de servicios implementa mejor el sistema?",
        options=[
            "Amazon Kinesis Data Streams para ingesta y Amazon Managed Service for Apache Flink para detectar anomal&iacute;as en vivo",
            "Amazon Kinesis Data Streams para ingesta y Amazon OpenSearch Service para indexar y graficar los eventos en dashboards",
            "Amazon S3 como buffer y Amazon Athena consultando peri&oacute;dicamente para hallar anomal&iacute;as en los datos ya guardados",
            "Amazon SQS como cola y SageMaker Training Compiler para acelerar el entrenamiento de un detector fuera de l&iacute;nea",
        ],
        correct=0,
        key="mla01-q34",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Kinesis Data Streams + Managed Service for Apache Flink.</div>'
            '<p><b>El problema:</b> ingesta y an&aacute;lisis <b>en tiempo real sin retraso</b> sobre un stream continuo de IoT.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Kinesis Data Streams ingiere con baja latencia y Managed Service for Apache Flink ejecuta anal&iacute;tica de streaming (ventanas, detecci&oacute;n de anomal&iacute;as) en vivo.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>KDS + OpenSearch Service:</b> KDS ingiere en tiempo real, pero OpenSearch indexa y grafica en dashboards; no ejecuta la l&oacute;gica de detecci&oacute;n de anomal&iacute;as sobre el stream en vivo como lo hace Flink.</li>'
            '<li><b>S3 + Athena peri&oacute;dico:</b> analiza datos ya en reposo; no es en tiempo real.</li>'
            '<li><b>SQS + Training Compiler:</b> Training Compiler acelera <b>entrenamiento</b>, no detecta anomal&iacute;as en un stream en vivo.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Anal&iacute;tica de streaming en vivo = Managed Service for Apache Flink sobre Kinesis Data Streams. Firehose es entrega, no anal&iacute;tica en tiempo real.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/managed-service-apache-flink/">Managed Service for Apache Flink</a></div>'
        ),
    ),

    # ===================== Q35: Data Wrangler (categoricas + numericas) =====================
    card(
        question="<b>Transformar datos activos:</b> dataset con variables <b>categ&oacute;ricas nominales</b> (regi&oacute;n, preferencias) y <b>num&eacute;ricas</b> (frecuencia, gasto) que hay que preprocesar y transformar para entrenar en SageMaker. &iquest;Qu&eacute; feature de SageMaker ayuda?",
        options=[
            "SageMaker Neo, que compila y optimiza modelos ya entrenados para inferencia en distintos targets de hardware",
            "SageMaker Feature Store, repositorio para almacenar y servir features, m&aacute;s que para transformarlas desde cero",
            "SageMaker Data Wrangler, para preprocesar, codificar categ&oacute;ricas y escalar num&eacute;ricas antes de entrenar",
            "SageMaker JumpStart, cat&aacute;logo de modelos y soluciones preentrenadas para acelerar el inicio de proyectos",
        ],
        correct=2,
        key="mla01-q35",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Data Wrangler.</div>'
            '<p><b>El problema:</b> transformar categ&oacute;ricas (one-hot/encoding) y escalar num&eacute;ricas: tareas de <b>preparaci&oacute;n de datos</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Data Wrangler ofrece transformaciones listas para codificar categ&oacute;ricas y escalar num&eacute;ricas de forma visual, dejando el dataset apto para entrenar.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Neo:</b> optimiza modelos entrenados para inferencia en hardware; no transforma datos.</li>'
            '<li><b>Feature Store:</b> guarda y sirve features; no es la herramienta para transformarlas desde datos crudos.</li>'
            '<li><b>JumpStart:</b> ofrece modelos/soluciones preentrenadas; no prepara ni transforma tu dataset.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Preparar/transformar features (encoding, scaling)" = Data Wrangler. "Guardar/servir features" = Feature Store.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler.html">SageMaker Data Wrangler</a></div>'
        ),
    ),

    # ===================== Q36: PDP y DPL (matching -> 2 cartas) =====================
    card(
        question="<b>Explicabilidad (Clarify):</b> se quiere <b>identificar c&oacute;mo cambia la probabilidad de churn a medida que aumenta la edad del cliente</b>. &iquest;Qu&eacute; t&eacute;cnica de an&aacute;lisis usar?",
        options=[
            "Partial dependence plots (PDPs), que visualizan el efecto marginal de una feature sobre la predicci&oacute;n",
            "Difference in proportions of labels (DPL), que mide disparidad de etiquetas positivas entre grupos demogr&aacute;ficos",
            "Total Variation Distance (TVD), que mide la m&aacute;xima diferencia entre dos distribuciones de probabilidad",
            "Kullback-Leibler Divergence (KL), que mide la divergencia general entre dos distribuciones de probabilidad",
        ],
        correct=0,
        key="mla01-q36a",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Partial dependence plots (PDPs).</div>'
            '<p><b>El problema:</b> ver c&oacute;mo la predicci&oacute;n (probabilidad de churn) cambia al variar <b>una feature</b> (edad).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> los PDPs muestran el <b>efecto marginal</b> de una o dos features sobre la predicci&oacute;n del modelo, exactamente lo pedido.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>DPL:</b> mide disparidad de etiquetas entre grupos (sesgo), no el efecto de una feature en la predicci&oacute;n.</li>'
            '<li><b>TVD:</b> compara distribuciones; no explica el efecto marginal de una variable.</li>'
            '<li><b>KL:</b> mide divergencia entre distribuciones; no es una t&eacute;cnica de dependencia parcial.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "C&oacute;mo cambia la predicci&oacute;n al variar una feature" = PDP. "Disparidad entre grupos" = m&eacute;trica de sesgo (DPL/CI/TVD).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-processing-job-analysis-results.html#clarify-processing-job-analysis-results-pdp">Clarify: PDP</a></div>'
        ),
    ),
    card(
        question="<b>Sesgo pre-entrenamiento (Clarify):</b> se quiere <b>medir el desbalance en la proporci&oacute;n de casos positivos de churn (las etiquetas observadas) entre grupos demogr&aacute;ficos</b> (p. ej. grupos de edad) antes de entrenar. &iquest;Qu&eacute; t&eacute;cnica usar?",
        options=[
            "Difference in proportions of labels (DPL), que mide la diferencia de proporciones de etiquetas entre dos grupos",
            "Partial dependence plots (PDPs), que visualizan el efecto marginal de una feature sobre la predicci&oacute;n del modelo",
            "Total Variation Distance (TVD), que mide la m&aacute;xima diferencia entre dos distribuciones de probabilidad completas",
            "Kullback-Leibler Divergence (KL), que mide la divergencia general entre dos distribuciones de probabilidad dadas",
        ],
        correct=0,
        key="mla01-q36b",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Difference in proportions of labels (DPL).</div>'
            '<p><b>El problema:</b> medir el <b>desbalance en la proporci&oacute;n de etiquetas positivas</b> (casos de churn observados) entre grupos demogr&aacute;ficos, antes de entrenar el modelo.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> DPL es una m&eacute;trica <b>pre-entrenamiento</b> que compara la proporci&oacute;n de etiquetas positivas/negativas entre dos grupos sobre los datos observados, revelando disparidad o posible discriminaci&oacute;n.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>PDPs:</b> explican el efecto de una feature en la predicci&oacute;n, no la disparidad entre grupos.</li>'
            '<li><b>TVD:</b> mide diferencia global entre distribuciones; DPL es la m&eacute;trica directa para proporci&oacute;n de etiquetas por grupo.</li>'
            '<li><b>KL:</b> divergencia entre distribuciones en general; no es la m&eacute;trica de proporci&oacute;n de etiquetas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> DPL mide disparidad en las <b>etiquetas observadas</b> (pre-entrenamiento). Su an&aacute;logo sobre las <b>predicciones</b> del modelo (post-entrenamiento) es DPPL. "Efecto de una variable en la salida" = PDP.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-data-bias-metric-true-label-imbalance.html">Clarify: DPL</a></div>'
        ),
    ),

    # ===================== Q37: Spearman =====================
    card(
        question="<b>Correlaci&oacute;n no lineal:</b> hay que evaluar <b>relaciones no lineales</b> (mon&oacute;tonas) entre features de una muestra grande, prefiriendo el coeficiente m&aacute;s usado por defecto para este caso. &iquest;Qu&eacute; prueba/coeficiente estad&iacute;stico es el adecuado?",
        options=[
            "Cram&eacute;r's V, que mide la asociaci&oacute;n entre dos variables categ&oacute;ricas a partir de una tabla de contingencia",
            "Pearson, que mide la fuerza de una relaci&oacute;n lineal entre dos variables num&eacute;ricas continuas",
            "Spearman, que mide correlaci&oacute;n mon&oacute;tona (no lineal) usando los rangos de los valores",
            "Kendall's Tau, coeficiente basado en rangos que mide correlaci&oacute;n mon&oacute;tona contando pares concordantes y discordantes",
        ],
        correct=2,
        key="mla01-q37",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Spearman.</div>'
            '<p><b>El problema:</b> capturar relaciones <b>no lineales pero mon&oacute;tonas</b> entre variables num&eacute;ricas de una muestra grande.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> el coeficiente de Spearman opera sobre <b>rangos</b>, as&iacute; que detecta relaciones mon&oacute;tonas aunque no sean lineales, y es el coeficiente de rango m&aacute;s usado por defecto para muestras grandes.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Cram&eacute;r\'s V:</b> mide asociaci&oacute;n entre variables <b>categ&oacute;ricas</b>, no correlaci&oacute;n num&eacute;rica no lineal.</li>'
            '<li><b>Pearson:</b> mide relaci&oacute;n <b>lineal</b>; no captura bien lo no lineal.</li>'
            '<li><b>Kendall\'s Tau:</b> tambi&eacute;n mide correlaci&oacute;n mon&oacute;tona por rangos, pero suele preferirse con <b>muestras peque&ntilde;as o datos ordinales</b> y penaliza distinto las inversiones; para el caso general de muestras grandes el coeficiente de rango est&aacute;ndar es Spearman.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Lineal = Pearson. Mon&oacute;tona/no lineal = Spearman (rangos) por defecto; Kendall\'s Tau es la alternativa de rango para muestras peque&ntilde;as/ordinales. Categ&oacute;ricas = Cram&eacute;r\'s V.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/canvas-explore-data-analytics.html">Canvas: an&aacute;lisis de datos</a></div>'
        ),
    ),

    # ===================== Q38: Clarify (bias + drift) =====================
    card(
        question="<b>Sesgo y su deriva, automatizados:</b> dataset muy desbalanceado y preocupaci&oacute;n por el <b>sesgo y su deriva en el tiempo</b> (bias drift); se quiere un enfoque <b>automatizado</b> para evaluar y mitigar sesgo en las recomendaciones. &iquest;Qu&eacute; enfoque se recomienda?",
        options=[
            "Usar Amazon SageMaker Model Monitor para detectar cu&aacute;ndo cae el desempe&ntilde;o general del modelo en producci&oacute;n",
            "Usar Amazon SageMaker Clarify para detectar sesgo (bias) y, con Model Monitor, monitorear la deriva de sesgo y atribuci&oacute;n",
            "Usar Amazon SageMaker Neo para optimizar el desempe&ntilde;o del modelo y as&iacute; reducir el impacto del data drift",
            "Usar Amazon SageMaker Ground Truth para etiquetar los datos con mayor precisi&oacute;n y prevenir el data drift",
        ],
        correct=1,
        key="mla01-q38",
        answer=(
            '<div class="verdict">Correcta: {{L}} - SageMaker Clarify.</div>'
            '<p><b>El problema:</b> evaluar y mitigar <b>sesgo</b> y vigilar <b>drift</b> de forma automatizada. Clarify es la herramienta de sesgo/explicabilidad y se integra con el monitoreo.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Clarify calcula m&eacute;tricas de sesgo (pre y post entrenamiento) y detecta la deriva de sesgo y de atribuci&oacute;n de features; la deriva de calidad/estad&iacute;stica de los datos la cubre Model Monitor. Juntos cubren ambos requisitos.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Model Monitor:</b> vigila calidad/deriva de datos, pero no es la herramienta espec&iacute;fica de m&eacute;tricas de sesgo (esa es Clarify).</li>'
            '<li><b>Neo:</b> optimiza modelos para inferencia; no evita sesgo ni drift.</li>'
            '<li><b>Ground Truth:</b> etiqueta datos; mejorar etiquetas no mide ni mitiga sesgo/drift autom&aacute;ticamente.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Sesgo/equidad = Clarify. Calidad de datos/modelo en producci&oacute;n = Model Monitor (a menudo trabajan juntos).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/clarify-detect-post-training-bias.html">Clarify: sesgo post-entrenamiento</a></div>'
        ),
    ),

    # ===================== Q39: Bedrock chatbots =====================
    card(
        question="<b>Caso de uso de Amazon Bedrock:</b> &iquest;cu&aacute;l describe mejor un caso en el que <b>Amazon Bedrock</b> (IA generativa con foundation models) destaca?",
        options=[
            "Mantenimiento predictivo de veh&iacute;culos a partir de se&ntilde;ales de sensores y registros de fallas hist&oacute;ricas",
            "Predicci&oacute;n de la demanda futura de productos con series de tiempo y modelos de forecasting cl&aacute;sicos",
            "Desarrollo de chatbots conversacionales que brindan informaci&oacute;n relevante a los clientes",
            "Identificaci&oacute;n de contenido dentro de im&aacute;genes de redes sociales mediante visi&oacute;n por computadora",
        ],
        correct=2,
        key="mla01-q39",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Chatbots conversacionales que dan informaci&oacute;n a clientes.</div>'
            '<p><b>El problema:</b> identificar el caso de <b>IA generativa</b>. Bedrock da acceso a foundation models (LLMs) para lenguaje natural.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> los chatbots conversacionales son un caso can&oacute;nico de LLMs/IA generativa, justo lo que Bedrock provee.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Mantenimiento predictivo:</b> es ML predictivo cl&aacute;sico (regresi&oacute;n/clasificaci&oacute;n), no IA generativa.</li>'
            '<li><b>Predicci&oacute;n de demanda:</b> forecasting de series de tiempo, tarea de ML tradicional.</li>'
            '<li><b>Identificar contenido en im&aacute;genes:</b> es visi&oacute;n por computadora (p. ej. Rekognition), no el fuerte generativo de Bedrock.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Bedrock = IA generativa (texto/chat, resumen, generaci&oacute;n). Predicci&oacute;n num&eacute;rica/visi&oacute;n cl&aacute;sica = SageMaker/Rekognition/Forecast.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/bedrock/">Amazon Bedrock</a></div>'
        ),
    ),

    # ===================== Q40: Bedrock beneficios (Select TWO) =====================
    card(
        question="<b>Beneficios de Amazon Bedrock:</b> un retailer quiere <b>fine-tune de modelos de terceros</b> para su chatbot, con privacidad de los datos. &iquest;Qu&eacute; par de beneficios de Bedrock le sirven?",
        options=[
            "Ofrece amplia variedad de foundation models de m&uacute;ltiples proveedores y permite personalizarlos de forma privada",
            "Ofrece FMs de varios proveedores, pero al hacer fine-tuning env&iacute;a tus datos de entrenamiento al proveedor del modelo base",
            "Da acceso solo a foundation models open source de la comunidad, sin incluir modelos propietarios de proveedores comerciales",
            "Permite fine-tuning de los FMs, pero &uacute;nicamente con datos que ya sean p&uacute;blicos, no con datos privados de la empresa",
        ],
        correct=0,
        key="mla01-q40",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Variedad de FMs de varios proveedores + personalizaci&oacute;n privada.</div>'
            '<p><b>El problema:</b> se necesita elegir entre modelos de varios proveedores y ajustarlos manteniendo los datos <b>privados</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Bedrock ofrece un cat&aacute;logo de foundation models de m&uacute;ltiples proveedores y permite personalizaci&oacute;n/fine-tuning privado (prompts y datos permanecen confidenciales).</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>El fine-tuning env&iacute;a tus datos al proveedor del modelo:</b> incorrecto; el fine-tuning en Bedrock ocurre en tu entorno de AWS y tus datos NO se comparten con el proveedor del FM ni se usan para reentrenar el modelo base.</li>'
            '<li><b>Solo FMs open source:</b> incorrecto; Bedrock incluye tanto modelos open source como <b>propietarios</b> de proveedores comerciales (Anthropic, AI21, Cohere, Amazon, etc.).</li>'
            '<li><b>Fine-tuning solo con datos p&uacute;blicos:</b> incorrecto; justamente puedes ajustar con tus <b>datos privados</b> de forma segura, sin necesidad de que sean p&uacute;blicos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Ventajas clave de Bedrock: multi-proveedor de FMs con API unificada, serverless (sin infraestructura) y personalizaci&oacute;n privada de modelos.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html">Qu&eacute; es Amazon Bedrock</a></div>'
        ),
    ),

    # ===================== Q41: Bedrock (servicio) =====================
    card(
        question="<b>Elegir servicio de IA generativa:</b> una empresa de salud quiere probar y comparar distintos <b>foundation models</b>, adaptarlos a sus datos clinicos manteniendo esos datos privados, y consumirlos <b>pagando por uso, sin aprovisionar ni operar servidores ni endpoints</b>. &iquest;Qu&eacute; servicio encaja mejor?",
        options=[
            "Amazon Bedrock: acceso por API a varios foundation models, con fine-tuning privado y consumo serverless pagando por uso",
            "Amazon SageMaker JumpStart: catalogo de foundation models con fine-tuning privado que despliegas en endpoints en tu cuenta",
            "Amazon SageMaker Canvas: interfaz no-code con modelos administrados para construir y personalizar modelos sin escribir codigo",
            "Amazon SageMaker Studio: IDE administrado para elegir, entrenar y ajustar modelos gestionando el computo desde un solo lugar",
        ],
        correct=0,
        key="mla01-q41",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Amazon Bedrock.</div>'
            '<p><b>El problema:</b> las cuatro opciones dan acceso a varios modelos y alguna forma de personalizacion, asi que el nombre del servicio no basta. El discriminador real es UNO: consumir los FMs de forma <b>serverless (por API, pagando por uso, sin desplegar ni operar endpoints)</b>.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> <b>Bedrock</b> es el unico de los cuatro que es <b>serverless</b>: llamas a los foundation models por API y puedes hacer fine-tuning privado (tus datos no se usan para reentrenar el modelo base), sin aprovisionar ni mantener infraestructura ni endpoints.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>SageMaker JumpStart:</b> tambien ofrece foundation models y fine-tuning privado, PERO el modelo ajustado se <b>despliega en un endpoint en TU cuenta</b> que dimensionas y pagas mientras este activo; no es consumo serverless por uso.</li>'
            '<li><b>SageMaker Canvas:</b> es no-code y da modelos administrados, pero esta orientado a ML tabular/predictivo y a generar predicciones, no a comparar y hacer fine-tuning privado de foundation models generativos por API.</li>'
            '<li><b>SageMaker Studio:</b> es un IDE administrado para construir/entrenar/ajustar; aun asi TU eliges y pagas el computo (kernels, training jobs, endpoints), es decir gestionas infraestructura, lo contrario de serverless por uso.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Cuando varias opciones "dan varios modelos", el desempate suele ser el modelo de consumo: <b>serverless por API pagando por uso</b> = Amazon Bedrock; si hay que <b>desplegar en un endpoint propio</b> = JumpStart/SageMaker.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html">Qu&eacute; es Amazon Bedrock</a></div>'
        ),
    ),

    # ===================== Q42: LDA (topic modeling) =====================
    card(
        question="<b>Descubrir t&oacute;picos:</b> gran volumen de comentarios de clientes; se quiere <b>descubrir autom&aacute;ticamente los temas</b> recurrentes (no predefinidos). &iquest;Qu&eacute; algoritmo built-in de SageMaker es el m&aacute;s apropiado?",
        options=[
            "Latent Dirichlet Allocation (LDA), algoritmo no supervisado que descubre t&oacute;picos latentes en texto",
            "Sequence-to-Sequence, orientado a traducir o transformar una secuencia de entrada en otra de salida",
            "BlazingText en modo Text Classification, que clasifica texto en categor&iacute;as previamente etiquetadas",
            "Text Classification - TensorFlow, que asigna documentos a clases predefinidas con un modelo supervisado",
        ],
        correct=0,
        key="mla01-q42",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Latent Dirichlet Allocation (LDA).</div>'
            '<p><b>El problema:</b> los temas <b>no est&aacute;n predefinidos</b> y hay que descubrirlos: es <b>topic modeling</b> no supervisado.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> LDA es un algoritmo no supervisado que infiere t&oacute;picos latentes a partir del texto, sin necesidad de etiquetas.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Seq2Seq:</b> transforma secuencias (traducci&oacute;n, resumen); no descubre t&oacute;picos.</li>'
            '<li><b>BlazingText (clasificaci&oacute;n):</b> supervisado; requiere categor&iacute;as etiquetadas de antemano.</li>'
            '<li><b>Text Classification - TensorFlow:</b> tambi&eacute;n supervisado con clases predefinidas, contra el requisito de descubrir temas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Descubrir temas no predefinidos" = topic modeling no supervisado (LDA o NTM). "Clasificar en categor&iacute;as conocidas" = supervisado.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/lda-how-it-works.html">SageMaker LDA</a></div>'
        ),
    ),

    # ================== Refuerzos (comparaciones que aparecen en las explicaciones) ==================
    # R1: familias de formato de datos
    card(
        question="<b>Formatos de datos - familias:</b> &iquest;qu&eacute; afirmaci&oacute;n clasifica correctamente estos formatos por su orientaci&oacute;n de almacenamiento?",
        options=[
            "Parquet y ORC son columnares (buenos para analytics); Avro, CSV y JSON Lines son por filas (buenos para escritura/streaming)",
            "Parquet, ORC y Avro son columnares (buenos para analytics); solo CSV y JSON Lines son por filas para escritura/streaming",
            "Parquet y ORC son columnares; Avro es por filas; CSV y JSON Lines son columnares por guardar cada campo en su propia columna",
            "ORC y Avro son columnares (buenos para analytics); Parquet, CSV y JSON Lines son por filas orientados a escritura/streaming",
        ],
        correct=0,
        key="mla01-r1-formatos",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Parquet/ORC columnares; Avro/CSV/JSON Lines por filas.</div>'
            '<p><b>El concepto:</b> el <b>almacenamiento columnar</b> guarda por columnas (lee solo las necesarias, ideal para analytics/ML); el <b>orientado a filas</b> guarda registros completos (bueno para escritura y streaming).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Parquet y ORC son columnares y comprimidos; Avro, CSV y JSON Lines son por filas.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Avro como columnar:</b> el &uacute;nico fallo es incluir Avro entre los columnares; Avro es orientado a filas, pensado para escritura e intercambio registro a registro.</li>'
            '<li><b>CSV y JSON Lines columnares:</b> confunde "tener columnas l&oacute;gicas" con almacenamiento columnar; ambos guardan el registro completo por fila, no columna por columna.</li>'
            '<li><b>Parquet por filas y ORC/Avro columnares:</b> invierte el caso de Parquet, que s&iacute; es columnar; y clasifica mal a Avro como columnar.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Analytics/ML por lotes -> columnar (Parquet/ORC). Escritura/streaming registro a registro -> por filas (Avro/JSON Lines/CSV).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-parquet-home.html">Glue: formatos</a></div>'
        ),
    ),
    # R2: selector de almacenamiento
    card(
        question="<b>Selector de almacenamiento:</b> para entrenamiento de ML, &iquest;qu&eacute; asignaci&oacute;n servicio-caso es la correcta?",
        options=[
            "FSx for Lustre: HPC/ML de alto throughput; EFS: acceso concurrente NFS; EBS: bloques de una instancia; S3: data lake de objetos",
            "EFS: HPC/ML de alto throughput; FSx for Lustre: acceso concurrente NFS; EBS: bloques de una instancia; S3: data lake de objetos",
            "FSx for Lustre: HPC/ML de alto throughput; EFS: acceso concurrente NFS; S3: bloques de una instancia; EBS: data lake de objetos",
            "FSx for Lustre: HPC/ML de alto throughput; EBS: acceso concurrente NFS; EFS: bloques de una instancia; S3: data lake de objetos",
        ],
        correct=0,
        key="mla01-r2-storage",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Lustre=HPC/ML, EFS=concurrente NFS, EBS=bloques 1 instancia, S3=data lake.</div>'
            '<p><b>El concepto:</b> cada servicio de almacenamiento tiene un caso de uso primario en ML.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> FSx for Lustre da throughput de HPC para entrenamiento; EFS ofrece file system NFS compartido concurrente; EBS son bloques atados a una instancia; S3 es objetos, base del data lake.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Opci&oacute;n con EFS en HPC:</b> intercambia solo el par Lustre/EFS; EFS es NFS concurrente, mientras que el file system de alto throughput para entrenamiento es FSx for Lustre.</li>'
            '<li><b>Opci&oacute;n con S3 como bloques:</b> intercambia solo el par EBS/S3; los bloques de una instancia son EBS, y S3 es el data lake de objetos, no al rev&eacute;s.</li>'
            '<li><b>Opci&oacute;n con EBS en NFS:</b> intercambia solo el par EFS/EBS; el acceso concurrente NFS es EFS, mientras que EBS son bloques ligados a una sola instancia.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "GPU distribuido alto throughput" = Lustre; "muchas EC2 mismo FS" = EFS; "una instancia bloques" = EBS; "objetos duraderos a escala" = S3.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html">FSx for Lustre</a></div>'
        ),
    ),
    # R3: Kinesis Data Streams vs Firehose
    card(
        question="<b>Kinesis Data Streams vs Firehose:</b> &iquest;cu&aacute;l describe correctamente la diferencia clave entre ambos?",
        options=[
            "Data Streams: ingesta con shards para leer/procesar en tiempo real; Firehose: entrega administrada a destinos sin gestionar shards",
            "Data Streams: ingesta con shards en tiempo real; Firehose: entrega administrada a destinos y adem&aacute;s permite reprocesar el hist&oacute;rico con replay",
            "Data Streams: ingesta con shards que entrega directamente a S3 sin consumidor; Firehose: entrega administrada a destinos sin gestionar shards",
            "Data Streams: ingesta con shards y retenci&oacute;n para replay; Firehose: entrega administrada que garantiza procesamiento exactamente-una-vez de cada registro",
        ],
        correct=0,
        key="mla01-r3-kinesis",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Data Streams (shards, tiempo real) vs Firehose (entrega administrada).</div>'
            '<p><b>El concepto:</b> <b>Kinesis Data Streams</b> es un stream con <b>shards</b> que consumes/procesas con baja latencia y con retenci&oacute;n para <b>replay</b>; <b>Firehose</b> es entrega administrada (buffering + carga) a S3/Redshift/OpenSearch sin gestionar shards.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> resume exactamente esa divisi&oacute;n de responsabilidades.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Firehose con replay del hist&oacute;rico:</b> el replay/retenci&oacute;n para reprocesar es de <b>Data Streams</b>; Firehose no retiene el stream para releerlo, solo entrega y hace buffering.</li>'
            '<li><b>Data Streams entrega a S3 sin consumidor:</b> Data Streams necesita un <b>consumidor</b> (o Firehose) para llegar a S3; no deposita por s&iacute; solo en el destino.</li>'
            '<li><b>Firehose garantiza exactamente-una-vez:</b> Firehose entrega con sem&aacute;ntica al-menos-una-vez (posibles duplicados), no exactamente-una-vez por registro.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Escalas Data Streams sumando shards y puedes reprocesar con replay; procesas en vivo con Flink. Firehose = "cargar streaming a un destino sin servidores".</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/streams/latest/dev/introduction.html">Kinesis Data Streams</a></div>'
        ),
    ),
    # R4: selector de movimiento de datos
    card(
        question="<b>Selector de movimiento de datos:</b> &iquest;qu&eacute; asignaci&oacute;n es correcta para llevar datos hacia AWS?",
        options=[
            "DataSync: migrar on-prem a S3/EFS/FSx por red; S3 Transfer Acceleration: acelerar subidas a S3 por edge; Data Transfer Terminal: transferencia f&iacute;sica offline",
            "DataSync: migrar on-prem a S3/EFS/FSx por red; Data Transfer Terminal: acelerar subidas a S3 por edge; S3 Transfer Acceleration: transferencia f&iacute;sica offline",
            "S3 Transfer Acceleration: migrar on-prem a S3/EFS/FSx por red; DataSync: acelerar subidas a S3 por edge; Data Transfer Terminal: transferencia f&iacute;sica offline",
            "DataSync: migrar on-prem a S3/EFS/FSx por red; S3 Transfer Acceleration: transferencia f&iacute;sica offline; Data Transfer Terminal: acelerar subidas a S3 por edge",
        ],
        correct=0,
        key="mla01-r4-movimiento",
        answer=(
            '<div class="verdict">Correcta: {{L}} - DataSync (red), Transfer Acceleration (subidas S3 por edge), Data Transfer Terminal (offline).</div>'
            '<p><b>El concepto:</b> cada servicio resuelve un escenario de transferencia distinto.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> DataSync mueve datos por red entre on-prem y S3/EFS/FSx; Transfer Acceleration acelera subidas a un bucket usando edge locations; Data Transfer Terminal es transferencia f&iacute;sica offline para vol&uacute;menes enormes con poca red.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Terminal para acelerar por edge:</b> intercambia solo el par Transfer Acceleration/Data Transfer Terminal; acelerar subidas a S3 por edge es Transfer Acceleration, no la transferencia f&iacute;sica.</li>'
            '<li><b>Transfer Acceleration para migrar por red:</b> intercambia solo el par DataSync/Transfer Acceleration; la migraci&oacute;n administrada por red on-prem -> S3/EFS/FSx es DataSync.</li>'
            '<li><b>Transfer Acceleration como offline f&iacute;sico:</b> intercambia solo el par Transfer Acceleration/Data Transfer Terminal; lo f&iacute;sico offline es Data Transfer Terminal.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Poca red + muchos TB/PB = f&iacute;sico (Data Transfer Terminal/Snow). Migraci&oacute;n por red = DataSync. Subidas globales r&aacute;pidas a S3 = Transfer Acceleration.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html">AWS DataSync</a></div>'
        ),
    ),
    # R5: Clarify vs Model Monitor
    card(
        question="<b>Clarify vs Model Monitor:</b> &iquest;cu&aacute;l distingue correctamente sus roles en SageMaker?",
        options=[
            "Clarify: m&eacute;tricas de sesgo y explicabilidad; Model Monitor: vigila calidad de datos/modelo y deriva en producci&oacute;n",
            "Model Monitor: m&eacute;tricas de sesgo y explicabilidad del dataset; Clarify: vigila la deriva de datos/modelo en producci&oacute;n",
            "Clarify: mide sesgo, explicabilidad y adem&aacute;s detecta la deriva de datos en producci&oacute;n de forma continua",
            "Model Monitor: vigila calidad y deriva en producci&oacute;n y tambi&eacute;n calcula el sesgo previo al entrenamiento del modelo",
        ],
        correct=0,
        key="mla01-r5-clarify",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Clarify (sesgo/explicabilidad) vs Model Monitor (calidad/deriva en producci&oacute;n).</div>'
            '<p><b>El concepto:</b> <b>Clarify</b> mide sesgo y explica predicciones; <b>Model Monitor</b> vigila en producci&oacute;n calidad de datos, del modelo y deriva.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> deslinda correctamente las dos herramientas, que suelen usarse juntas.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Roles invertidos:</b> asigna el sesgo/explicabilidad a Model Monitor y la deriva a Clarify; es al rev&eacute;s.</li>'
            '<li><b>Clarify detecta deriva en producci&oacute;n:</b> Clarify aporta la l&iacute;nea base de sesgo/explicabilidad, pero la vigilancia continua de deriva en producci&oacute;n la ejecuta Model Monitor.</li>'
            '<li><b>Model Monitor calcula sesgo previo:</b> el an&aacute;lisis de sesgo pre-entrenamiento es de Clarify; Model Monitor opera sobre el endpoint ya desplegado.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Sesgo/equidad/explicabilidad = Clarify. Vigilancia continua en producci&oacute;n (calidad, deriva) = Model Monitor.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html">SageMaker Model Monitor</a></div>'
        ),
    ),
    # R6: Ground Truth vs Comprehend
    card(
        question="<b>Ground Truth vs Comprehend:</b> &iquest;cu&aacute;l describe correctamente cu&aacute;ndo usar cada uno?",
        options=[
            "Ground Truth: crear etiquetas/anotaciones para entrenar tu modelo; Comprehend: NLP administrado que infiere sentimiento/entidades sin entrenar",
            "Comprehend: crear etiquetas y anotaciones para entrenar tu modelo; Ground Truth: NLP administrado que infiere sentimiento/entidades sin entrenar",
            "Ground Truth: crear etiquetas para entrenar y adem&aacute;s inferir sentimiento directamente sin necesidad de entrenar un modelo",
            "Comprehend: NLP administrado que infiere entidades y adem&aacute;s coordina equipos humanos para etiquetar tus datos de entrenamiento",
        ],
        correct=0,
        key="mla01-r6-groundtruth",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Ground Truth (etiquetar para entrenar) vs Comprehend (NLP listo que infiere).</div>'
            '<p><b>El concepto:</b> <b>Ground Truth</b> genera etiquetas de alta calidad para construir tu propio dataset; <b>Comprehend</b> es un servicio NLP administrado que ya infiere sentimiento, entidades, idioma, etc.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> refleja la decisi&oacute;n: si necesitas datos etiquetados -> Ground Truth; si quieres NLP inmediato sin entrenar -> Comprehend.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Roles invertidos:</b> el que etiqueta datos es Ground Truth y el que infiere NLP sin entrenar es Comprehend; esta opci&oacute;n los cambia.</li>'
            '<li><b>Ground Truth infiere sentimiento:</b> Ground Truth produce etiquetas, no infiere; la inferencia de sentimiento lista para usar es de Comprehend.</li>'
            '<li><b>Comprehend coordina etiquetadores humanos:</b> la orquestaci&oacute;n de anotadores humanos es de Ground Truth; Comprehend solo infiere sobre texto.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> "Necesito etiquetar datos" = Ground Truth. "Necesito analizar texto ya, sin entrenar" = Comprehend.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/sms.html">SageMaker Ground Truth</a></div>'
        ),
    ),
    # R7: Data Wrangler vs Feature Store
    card(
        question="<b>Data Wrangler vs Feature Store:</b> &iquest;cu&aacute;l resume correctamente para qu&eacute; sirve cada uno?",
        options=[
            "Data Wrangler: preparar/transformar datos (limpiar, codificar, escalar, dividir); Feature Store: almacenar y servir features (online/offline)",
            "Feature Store: preparar/transformar datos (limpiar, codificar, escalar, dividir); Data Wrangler: almacenar y servir features (online/offline)",
            "Data Wrangler: preparar/transformar datos y adem&aacute;s servir features online de baja latencia para inferencia en producci&oacute;n",
            "Feature Store: almacenar y servir features y adem&aacute;s aplicar transformaciones visuales de limpieza y codificaci&oacute;n sobre datos crudos",
        ],
        correct=0,
        key="mla01-r7-wrangler",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Data Wrangler (preparar/transformar) vs Feature Store (almacenar/servir features).</div>'
            '<p><b>El concepto:</b> <b>Data Wrangler</b> es la etapa de preparaci&oacute;n (limpiar, codificar categ&oacute;ricas, escalar, split); <b>Feature Store</b> guarda y sirve las features listas, con online store (baja latencia) y offline store (entrenamiento).</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> separa claramente "transformar" de "almacenar/servir".</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Roles invertidos:</b> el que transforma es Data Wrangler y el que almacena/sirve es Feature Store; esta opci&oacute;n los cambia.</li>'
            '<li><b>Data Wrangler sirve features online:</b> servir features de baja latencia para inferencia es del online store de Feature Store, no de Data Wrangler.</li>'
            '<li><b>Feature Store transforma con recetas visuales:</b> las transformaciones visuales sobre datos crudos son de Data Wrangler; Feature Store solo guarda y sirve.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Flujo: Data Wrangler prepara -> Feature Store guarda/sirve -> entrenamiento/inferencia consumen las features.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html">SageMaker Feature Store</a></div>'
        ),
    ),
    # R8: Robust vs Standard scaler
    card(
        question="<b>Escalado - Robust vs Standard:</b> &iquest;cu&aacute;ndo elegir Robust Scaler en lugar de Standard Scaler?",
        options=[
            "Cuando hay outliers: Robust usa mediana e IQR (resistente a extremos); Standard usa media/desviaci&oacute;n, sensibles a outliers",
            "Cuando quieres media cero y varianza uno: Robust centra en la mediana y escala por IQR para dejar la distribuci&oacute;n est&aacute;ndar",
            "Cuando hay outliers: Standard es preferible porque recorta los valores extremos antes de restar la media y dividir por la desviaci&oacute;n",
            "Cuando hay outliers: Robust primero elimina las filas at&iacute;picas y luego aplica media y desviaci&oacute;n igual que Standard",
        ],
        correct=0,
        key="mla01-r8-scaler",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Robust (mediana/IQR) con outliers; Standard (media/desviaci&oacute;n) sin ellos.</div>'
            '<p><b>El concepto:</b> el escalado ajusta features a rangos comparables. Con <b>outliers</b>, media y desviaci&oacute;n se distorsionan.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> Robust Scaler usa mediana e IQR (poco sensibles a extremos); Standard Scaler usa media/desviaci&oacute;n, adecuado cuando no hay outliers fuertes.</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>"Media cero y varianza uno" con Robust:</b> ese objetivo es de <b>Standard</b>; Robust centra en la mediana y escala por IQR, no garantiza varianza uno.</li>'
            '<li><b>Standard recorta extremos:</b> Standard no recorta outliers; los incluye al calcular media y desviaci&oacute;n, por eso se distorsiona con valores at&iacute;picos.</li>'
            '<li><b>Robust elimina filas y luego usa media/desviaci&oacute;n:</b> Robust no borra filas ni usa media/desviaci&oacute;n; su resistencia viene de usar mediana e IQR sobre todos los datos.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Ve la palabra "outliers/at&iacute;picos" en la pregunta de escalado y piensa en Robust Scaler.</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/sagemaker/latest/dg/data-wrangler-transform.html#data-wrangler-transform-process-numeric">Data Wrangler: transform num&eacute;rico</a></div>'
        ),
    ),
    # R9: DMS homogenea vs heterogenea
    card(
        question="<b>AWS DMS - homog&eacute;nea vs heterog&eacute;nea:</b> &iquest;cu&aacute;l describe correctamente la diferencia?",
        options=[
            "Homog&eacute;nea: mismo motor o compatibles (MySQL a Aurora MySQL) solo con DMS; heterog&eacute;nea: motores distintos, DMS m&aacute;s Schema Conversion Tool",
            "Homog&eacute;nea: mismo motor o compatibles que a&uacute;n as&iacute; requiere Schema Conversion Tool; heterog&eacute;nea: motores distintos que migran solo con DMS",
            "Homog&eacute;nea: mismo motor migrado solo con DMS; heterog&eacute;nea: motores distintos que no necesitan conversi&oacute;n si ambos son bases SQL",
            "Homog&eacute;nea: mismo motor migrado solo con DMS; heterog&eacute;nea: motores distintos que se migran manualmente sin usar DMS ni SCT",
        ],
        correct=0,
        key="mla01-r9-dms",
        answer=(
            '<div class="verdict">Correcta: {{L}} - Homog&eacute;nea = motores compatibles (solo DMS); heterog&eacute;nea = distintos (DMS + SCT).</div>'
            '<p><b>El concepto:</b> una migraci&oacute;n <b>homog&eacute;nea</b> es entre motores iguales o compatibles (MySQL a Aurora MySQL); una <b>heterog&eacute;nea</b> cruza motores distintos (p. ej. Oracle a PostgreSQL) y necesita convertir el esquema.</p>'
            '<p><b>Por qu&eacute; la respuesta sirve:</b> resume cu&aacute;ndo basta DMS y cu&aacute;ndo hace falta a&ntilde;adir la Schema Conversion Tool (SCT).</p>'
            '<p><b>Por qu&eacute; NO las otras, una por una:</b></p>'
            '<ul>'
            '<li><b>Homog&eacute;nea requiere SCT:</b> la conversi&oacute;n de esquema con SCT es de la heterog&eacute;nea; entre motores compatibles no hace falta convertir.</li>'
            '<li><b>Heterog&eacute;nea sin conversi&oacute;n si ambos son SQL:</b> ser ambos SQL no basta; motores distintos (Oracle a PostgreSQL) s&iacute; requieren SCT aunque los dos sean relacionales.</li>'
            '<li><b>Heterog&eacute;nea manual sin DMS ni SCT:</b> la heterog&eacute;nea justamente se apoya en DMS + SCT; no es un proceso manual sin herramientas.</li>'
            '</ul>'
            '<div class="extra"><span class="h">Exam tip</span> Motores compatibles = DMS directo (homog&eacute;nea). Motores distintos = DMS + SCT (heterog&eacute;nea).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/dms/">AWS DMS</a></div>'
        ),
    ),
]

create(deck_name="MLA-C01::01 - Data Preparation", cards=cards,
       out_path="out/MLA-C01_01.apkg", do_import=False)
