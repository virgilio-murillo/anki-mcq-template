#!/usr/bin/env python3
"""HTML de estudio: Precision vs Recall."""
import base64
import pathlib

IMG = pathlib.Path("study/img_prec")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("precision.png", "1) Precision = de lo que MARQUÉ positivo, cuánto acerté", "ok",
     "Precision mira <b>solo la columna de lo que el modelo predijo Passed</b> (TP + FP). De esa columna, "
     "¿qué fracción era realmente correcta? = <b>TP / (TP + FP)</b>. Se equivoca cuando hay muchos <b>falsos "
     "positivos (FP)</b>: cosas que marcó Passed pero no lo eran. Respuesta <b>D</b> = esta."),
    ("recall.png", "2) Recall = de lo que ERA positivo, cuánto atrapé", "info",
     "Recall mira <b>solo la fila de lo que realmente era Passed</b> (TP + FN). De esa fila, ¿qué fracción "
     "logró detectar el modelo? = <b>TP / (TP + FN)</b>. Se equivoca cuando hay muchos <b>falsos negativos "
     "(FN)</b>: Passed reales que se le escaparon. Es la opción A del examen (sensibilidad), <b>no</b> Precision."),
    ("compara.png", "3) La diferencia clave: mismo numerador, distinto conjunto", "key",
     "Las dos usan el mismo numerador (<b>TP</b>, los aciertos positivos), pero <b>dividen entre conjuntos "
     "distintos</b>: Precision divide entre 'lo que yo predije positivo' (TP+FP); Recall divide entre 'lo que "
     "realmente era positivo' (TP+FN). Truco: <b>Precision</b> se castiga por FP; <b>Recall</b> se castiga por FN."),
    ("cuando.png", "4) Cuándo importa cada una y qué son los distractores", "flow",
     "<b>Precision alta</b> importa cuando un falso positivo es costoso (ej. un frenado innecesario en "
     "conducción autónoma). <b>Recall alto</b> importa cuando perder un positivo real es grave (fraude, "
     "diagnóstico). Los distractores son OTRAS métricas: A = Recall/sensibilidad; B = Accuracy (aciertos sobre "
     "el total); C = False Positive Rate (negativos marcados como positivos). Solo D describe la Precision."),
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
<title>MLA-C01 · Precision vs Recall</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #2e7d32; padding:16px 20px; border-radius:8px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .intro {{ background:#eef4fb; border:1px solid #1565c0; border-radius:8px; padding:12px 18px; margin-bottom:20px; font-size:14.5px; }}
  .intro b {{ color:#1565c0; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(460px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.info {{ border-top-color:#1565c0; }}
  .card.key {{ border-top-color:#6a1b9a; }}
  .card.flow {{ border-top-color:#f9a825; }}
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
  <h1>Precision vs Recall · qué mide cada una</h1>
  <p>MLA-C01 · tarjeta de estudio · Precision = TP / (TP + FP)</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> ¿qué mide la <b>Precision</b> (a diferencia del Recall)?</p>
    <p><b>Respuesta: D —</b> la proporción de positivos correctos entre todos los que el modelo predijo como positivos = <b>TP / (TP + FP)</b>.</p>
  </div>
  <div class="intro">
    <b>La idea en una frase:</b> Precision y Recall comparten el mismo numerador (TP, los aciertos positivos)
    pero dividen entre conjuntos distintos. &nbsp; <b>Precision</b> = "de lo que MARQUÉ positivo, cuánto acerté".
    &nbsp; <b>Recall</b> = "de lo que ERA positivo, cuánto atrapé".
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> <b>Precision</b> = TP/(TP+FP), la castigan los <b>falsos positivos</b> (importa si un FP es caro).
    &nbsp; <b>Recall</b> = TP/(TP+FN), lo castigan los <b>falsos negativos</b> (importa si perder un positivo es grave).
    &nbsp; <b>F1</b> = balance de ambas. &nbsp; Accuracy = aciertos/total; FPR = negativos marcados como positivos.
  </div>
</div>
<footer>Generado para estudio local · conteos de ejemplo (TP=45, FP=8, FN=7, TN=40)</footer>
</body></html>"""

out = pathlib.Path("study/precision_vs_recall.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
