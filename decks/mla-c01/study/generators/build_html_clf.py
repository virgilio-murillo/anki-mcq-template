#!/usr/bin/env python3
"""HTML de estudio: cuarteto de metricas de clasificacion binaria."""
import base64
import pathlib

IMG = pathlib.Path("study/img_clf")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("matriz.png", "1) Todo nace de la matriz de confusión", "info",
     "En clasificación binaria (Passed/Failed) el modelo, a un <b>umbral fijo</b>, produce 4 conteos: "
     "<b>TP</b> (Passed acertado), <b>FP</b> (dijo Passed pero era Failed), <b>FN</b> (dijo Failed pero era "
     "Passed) y <b>TN</b> (Failed acertado). Todas las métricas del cuarteto correcto se calculan a partir de "
     "estos 4 números."),
    ("formulas.png", "2) De dónde sale cada métrica del cuarteto (A)", "ok",
     "<b>Precision</b> = TP/(TP+FP): de lo que marqué Passed, cuánto acerté. <b>Recall</b> = TP/(TP+FN): de los "
     "Passed reales, cuántos atrapé. <b>Accuracy</b> = (TP+TN)/total: aciertos totales. <b>F1</b> = media "
     "armónica de Precision y Recall: su balance. Las cuatro son operaciones directas sobre los conteos <b>a "
     "un umbral fijo</b> → por eso son el cuarteto pedido."),
    ("auc.png", "3) Por qué AUC-ROC queda fuera (distractor D)", "key",
     "AUC-ROC <b>sí</b> es una métrica de clasificación válida, pero <b>no se deriva de un umbral fijo</b>: "
     "recorre <b>todos</b> los umbrales posibles y mide el área bajo la curva ROC. Precision/Recall/Accuracy/F1 "
     "corresponden a <b>UN punto</b> (un umbral); AUC-ROC es <b>toda la curva</b>. Como la pregunta pide "
     "métricas de conteo a umbral fijo, AUC-ROC no entra en este cuarteto."),
    ("mapa.png", "4) Los otros distractores son de OTRO problema", "flow",
     "El truco para descartar rápido: cada métrica pertenece a un tipo de problema. <b>R-cuadrado</b> (opción B) "
     "es de <b>regresión</b> (valor continuo), no aplica a etiquetas Passed/Failed. <b>Perplexity</b> (opción C) "
     "es de <b>modelos de lenguaje/NLP</b> (qué tan bien predicen texto). Si ves R-cuadrado o Perplexity en una "
     "pregunta de clasificación, es distractor automático."),
]

blocks = []
for fname, title, kind, desc in panels:
    blocks.append(f"""
    <div class="card {kind}">
      <div class="head"><span class="title">{title}</span></div>
      <img src="data:image/png;base64,{b64(fname)}" alt="{title}"/>
      <p class="desc">{desc}</p>
    </div>""")

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MLA-C01 · Cuarteto de métricas de clasificación</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #2e7d32; padding:16px 20px; border-radius:8px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(450px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.key {{ border-top-color:#6a1b9a; }}
  .card.flow {{ border-top-color:#f9a825; }}
  .card.info {{ border-top-color:#1565c0; }}
  .card img {{ width:100%; height:auto; border-radius:6px; }}
  .head {{ margin-bottom:8px; }}
  .title {{ font-weight:700; font-size:15px; }}
  .desc {{ font-size:13.5px; line-height:1.55; color:#37424c; margin:10px 2px 2px; }}
  .tip {{ background:#fff8e1; border:1px solid #f9a825; border-radius:8px; padding:12px 16px; margin-top:20px; font-size:14px; }}
  .tip b {{ color:#b26a00; }}
  footer {{ text-align:center; color:#90a4ae; font-size:12px; padding:18px; }}
</style></head>
<body>
<header>
  <h1>Métricas de clasificación binaria · el cuarteto de la matriz de confusión</h1>
  <p>MLA-C01 · tarjeta de estudio · Precision, Recall, Accuracy, F1</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> clasificación binaria (Passed/Failed) con imágenes/video. Se busca el cuarteto de
    métricas derivadas de la <b>matriz de confusión a un umbral de decisión fijo</b> (conteo TP/FP/TN/FN, no
    métricas que barren todos los umbrales como AUC-ROC). ¿Qué cuarteto?</p>
    <p><b>Respuesta: A —</b> Precision, Recall, Accuracy y F1 Score.</p>
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> cuarteto clásico de clasificación = <b>Precision, Recall, Accuracy, F1</b> (todas de la matriz a umbral fijo).
    &nbsp; Otras válidas de clasificación: <b>AUC-ROC</b> y <b>especificidad</b> (pero AUC-ROC barre todos los umbrales).
    &nbsp; <b>R-cuadrado / RMSE / MAE</b> = regresión. &nbsp; <b>Perplexity / BLEU / ROUGE</b> = lenguaje/NLP.
  </div>
</div>
<footer>Generado para estudio local · diagramas ilustrativos (conteos de ejemplo)</footer>
</body></html>"""

out = pathlib.Path("study/classification_metrics.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
