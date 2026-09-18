#!/usr/bin/env python3
"""HTML de estudio: que es el UMBRAL y por que AUC-ROC no es de umbral fijo."""
import base64
import pathlib

IMG = pathlib.Path("study/img_thr")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("umbral.png", "1) ¿Qué es el umbral? El modelo da una PROBABILIDAD", "info",
     "Un clasificador <b>no</b> dice directamente 'Passed' o 'Failed'. Internamente calcula una "
     "<b>probabilidad</b> (ej. 'esta imagen tiene 0.73 de ser Passed'). Para convertir ese número en una "
     "etiqueta, eliges un <b>punto de corte = el umbral</b> (por defecto 0.5): si la probabilidad ≥ 0.5 → "
     "Passed; si &lt; 0.5 → Failed. La línea azul del gráfico es ese umbral."),
    ("mover.png", "2) Mover el umbral cambia los conteos", "ok",
     "El umbral lo eliges tú, y moverlo cambia los resultados. Con umbral <b>bajo</b> (0.3) el modelo dice "
     "'Passed' muy fácil → atrapa más Passed reales (más TP) pero también más errores (más FP). Con umbral "
     "<b>alto</b> (0.8) solo dice 'Passed' cuando está muy seguro → menos FP pero se le escapan Passed. Fíjate "
     "cómo cambian TP y FP en los tres paneles: <b>por eso Precision, Recall, Accuracy y F1 dependen del "
     "umbral que fijes</b>."),
    ("curva.png", "3) Cada umbral es UN punto; la curva ROC los une todos", "key",
     "Si en vez de fijar un umbral pruebas <b>todos</b> (0.0, 0.1, ... 1.0), cada uno te da un punto (un par "
     "FPR, TPR). Al unir todos esos puntos obtienes la <b>curva ROC</b>. El <b>AUC</b> es el <b>área bajo esa "
     "curva</b>. Los 3 puntos de colores son umbrales concretos (0.3, 0.5, 0.8); la curva morada es el "
     "recorrido por <b>todos</b> los umbrales. Ahí está la diferencia: Precision/Recall/etc. = un punto; "
     "AUC-ROC = la curva entera."),
    ("resumen.png", "4) La idea en una frase: foto vs película", "flow",
     "<b>Precision, Recall, Accuracy, F1</b> = una <b>FOTO</b>: fijas un umbral, cuentas TP/FP/TN/FN y sacas "
     "los números. <b>AUC-ROC</b> = <b>toda la PELÍCULA</b>: recorre todos los umbrales y resume la curva. Como "
     "la pregunta pide métricas 'a un umbral FIJO' (una foto), AUC-ROC (la película) <b>no entra en el "
     "cuarteto</b>. No es que AUC-ROC sea mala; simplemente responde a otra cosa."),
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
<title>MLA-C01 · El umbral y por qué AUC-ROC no encaja</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .intro {{ background:#eef4fb; border:1px solid #1565c0; border-radius:8px; padding:14px 18px; margin-bottom:20px; font-size:14.5px; line-height:1.55; }}
  .intro b {{ color:#1565c0; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(460px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.key {{ border-top-color:#6a1b9a; }}
  .card.flow {{ border-top-color:#c62828; }}
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
  <h1>El "umbral" (threshold) · y por qué AUC-ROC no es de umbral fijo</h1>
  <p>MLA-C01 · tarjeta de estudio · aterrizando el concepto desde cero</p>
</header>
<div class="wrap">
  <div class="intro">
    <b>La confusión está en la palabra "umbral".</b> Un modelo de clasificación no dice "Passed/Failed":
    calcula una <b>probabilidad</b> (0 a 1). Para decidir la etiqueta, cortas en un número (el <b>umbral</b>,
    por defecto 0.5). &nbsp; <b>Precision/Recall/Accuracy/F1</b> se calculan DESPUÉS de fijar ese corte (una foto).
    &nbsp; <b>AUC-ROC</b> no fija ningún corte: prueba TODOS los cortes posibles y resume la curva (la película).
    Por eso la pregunta, que pide métricas "a un umbral fijo", deja fuera a AUC-ROC.
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>En una línea:</b> el umbral es el número de corte que convierte una probabilidad en etiqueta.
    Precision/Recall/Accuracy/F1 dependen de UN umbral (foto). AUC-ROC recorre TODOS los umbrales (película).
    "Umbral fijo" en la pregunta = foto = el cuarteto A, no AUC-ROC.
  </div>
</div>
<footer>Generado para estudio local · datos sintéticos ilustrativos</footer>
</body></html>"""

out = pathlib.Path("study/threshold_and_auc.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
