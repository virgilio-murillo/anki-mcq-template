#!/usr/bin/env python3
"""Construye un HTML de estudio autocontenido (imagenes en base64) para la carta
de tecnicas de visualizacion de Data Wrangler."""
import base64
import pathlib

IMG = pathlib.Path("study/img")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


cards = [
    ("a_scatter.png", "A", "Scatter plot (gráfico de dispersión)", True,
     "Coloca cada par <b>(x, y)</b> como un punto en el plano. De un vistazo revela: (1) si las dos "
     "variables <b>suben/bajan juntas</b> (correlación), (2) la <b>fuerza</b> de esa relación (qué tan "
     "apretada está la nube) y (3) los <b>outliers</b> (puntos que se escapan del patrón). Es la única "
     "que responde exactamente a lo pedido: relación entre DOS variables + outliers."),
    ("c_histograma.png", "C", "Histograma", False,
     "Muestra la <b>distribución de frecuencias de UNA sola variable</b>: divide su rango en intervalos "
     "(bins) y cuenta cuántos valores caen en cada uno. Sirve para ver forma, sesgo y rango de una "
     "variable, pero <b>no</b> relaciona dos variables ni muestra outliers de pares."),
    ("d_multicol.png", "D", "Análisis de multicolinealidad", False,
     "Cuantifica la <b>redundancia lineal entre VARIAS variables predictoras a la vez</b> (típicamente una "
     "matriz de correlación o el VIF). Dice si hay features que aportan lo mismo, pero es un resumen "
     "numérico global: <b>no</b> visualiza un par concreto ni marca puntos atípicos individuales."),
    ("b_shapley.png", "B", "Gráfico de valores Shapley", False,
     "Atribuye <b>cuánto contribuye cada feature a UNA predicción del modelo</b> (explicabilidad, vía "
     "SageMaker Clarify). Responde 'por qué el modelo predijo esto', <b>no</b> 'cómo se relacionan dos "
     "variables entre sí' ni dónde están los outliers."),
]

blocks = []
for fname, letter, title, correct, desc in cards:
    badge = "✓ CORRECTA" if correct else "✗ distractor"
    cls = "correct" if correct else "wrong"
    blocks.append(f"""
    <div class="card {cls}">
      <div class="head"><span class="letter">{letter}</span>
        <span class="title">{title}</span>
        <span class="badge {cls}">{badge}</span></div>
      <img src="data:image/png;base64,{b64(fname)}" alt="{title}"/>
      <p class="desc">{desc}</p>
    </div>""")

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MLA-C01 · Data Wrangler: técnicas de visualización</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #1565c0; padding:16px 20px; border-radius:8px; margin-bottom:20px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(430px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #90a4ae; }}
  .card.correct {{ border-top-color:#2e7d32; }}
  .card img {{ width:100%; height:auto; border-radius:6px; }}
  .head {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; }}
  .letter {{ background:#0f2a3f; color:#fff; width:26px; height:26px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-weight:700; font-size:14px; }}
  .card.correct .letter {{ background:#2e7d32; }}
  .title {{ font-weight:700; font-size:15px; flex:1; }}
  .badge {{ font-size:11px; font-weight:700; padding:3px 8px; border-radius:12px; }}
  .badge.correct {{ background:#e6f4ea; color:#2e7d32; }}
  .badge.wrong {{ background:#fdecec; color:#c62828; }}
  .desc {{ font-size:13.5px; line-height:1.55; color:#37424c; margin:10px 2px 2px; }}
  .tip {{ background:#fff8e1; border:1px solid #f9a825; border-radius:8px; padding:12px 16px; margin-top:20px; font-size:14px; }}
  .tip b {{ color:#b26a00; }}
  footer {{ text-align:center; color:#90a4ae; font-size:12px; padding:18px; }}
</style></head>
<body>
<header>
  <h1>Data Wrangler · Técnicas de visualización</h1>
  <p>MLA-C01 · tarjeta de estudio · las 4 técnicas comparadas</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> se quiere visualizar la <b>relación entre DOS variables</b> concretas (una en X,
    otra en Y), apreciar si suben/bajan juntas e identificar <b>outliers</b>. ¿Qué técnica usar?</p>
    <p><b>Respuesta: A — Scatter plot.</b> Es la única de las cuatro que grafica pares (x, y) individuales,
    revela la correlación y su fuerza, y deja ver los puntos atípicos.</p>
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla mnemónica para el examen:</b> "relación entre DOS variables + outliers" → <b>scatter plot</b>.
    "Distribución de UNA variable" → <b>histograma</b>. "Redundancia entre muchas variables" →
    <b>multicolinealidad</b>. "Por qué el modelo predijo X" → <b>valores Shapley</b> (Clarify).
  </div>
</div>
<footer>Generado para estudio local · imágenes sintéticas ilustrativas</footer>
</body></html>"""

out = pathlib.Path("study/data_wrangler_viz.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
