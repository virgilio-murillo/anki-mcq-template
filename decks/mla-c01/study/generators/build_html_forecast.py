#!/usr/bin/env python3
"""HTML de estudio autocontenido para la carta de metricas de forecasting."""
import base64
import pathlib

IMG = pathlib.Path("study/img_fc")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("rmse.png", "RMSE — mide el error de valores continuos", "ok",
     "El <b>RMSE</b> (raíz del promedio de errores al cuadrado) es la métrica <b>estándar de regresión</b>. "
     "Compara el valor pronosticado contra el real punto por punto (líneas rojas = error) y <b>penaliza más "
     "los errores grandes</b> porque los eleva al cuadrado. Ideal para temperatura, un valor continuo."),
    ("wql.png", "Average wQL — calidad del pronóstico probabilístico", "ok",
     "El <b>Average Weighted Quantile Loss</b> evalúa pronósticos con <b>incertidumbre</b>: en vez de un solo "
     "número, el modelo predice cuantiles (p10, p50, p90). wQL mide qué tan bien <b>calibrados</b> están esos "
     "cuantiles (ej. el p90 de humedad debería quedar por encima del real ~90% del tiempo). Es la métrica de "
     "pronóstico probabilístico que menciona la pregunta."),
    ("roc.png", "AUC-ROC / F1 / Log loss — solo clasificación", "no",
     "Estas son las métricas de los distractores (B y D, y el F1 de A). Necesitan <b>CLASES discretas</b> "
     "(spam/no-spam, fraude/no-fraude): AUC-ROC mide separación de clases, F1 balancea Precision y Recall, "
     "Log loss penaliza probabilidades de clase. Un forecast de temperatura no tiene clases, así que "
     "<b>ninguna aplica</b>."),
    ("mapa.png", "Chuleta: qué métrica para qué tarea", "map",
     "El truco de esta pregunta es reconocer la <b>tarea</b>: temperatura y humedad son valores continuos "
     "con incertidumbre → <b>regresión + pronóstico probabilístico</b> → RMSE + Average wQL (opción C). "
     "Si ves F1, AUC-ROC o Log loss en una pregunta de forecasting/regresión, es distractor."),
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
<title>MLA-C01 · Métricas de forecasting (RMSE + wQL)</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #2e7d32; padding:16px 20px; border-radius:8px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(430px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.no {{ border-top-color:#c62828; }}
  .card.map {{ border-top-color:#1565c0; }}
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
  <h1>Métricas de evaluación · Forecasting de series de tiempo</h1>
  <p>MLA-C01 · tarjeta de estudio · regresión + pronóstico probabilístico vs clasificación</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> modelo de forecasting de series de tiempo (temperatura y humedad, valores continuos)
    en SageMaker. ¿Qué par de métricas es más adecuado?</p>
    <p><b>Respuesta: C — RMSE y Average wQL.</b> Es tarea de <b>regresión</b> (valores continuos) con
    <b>incertidumbre</b> (cuantiles): RMSE mide el error del valor continuo y Average wQL evalúa la calidad
    de los cuantiles del pronóstico probabilístico.</p>
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> primero identifica la TAREA. &nbsp;
    <b>Regresión</b> (valor continuo) → RMSE, MAE, MAPE. &nbsp;
    <b>Pronóstico probabilístico</b> (cuantiles/incertidumbre) → Average wQL. &nbsp;
    <b>Clasificación</b> (clases) → Accuracy, Precision, Recall, F1, AUC-ROC, Log loss. &nbsp;
    Si la pregunta es de forecasting y ves F1/AUC/Log loss, es distractor.
  </div>
</div>
<footer>Generado para estudio local · gráficas sintéticas ilustrativas</footer>
</body></html>"""

out = pathlib.Path("study/forecasting_metrics.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
