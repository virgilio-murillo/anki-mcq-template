#!/usr/bin/env python3
"""HTML de estudio para la carta de despliegue (serverless sin provisioned)."""
import base64
import pathlib

IMG = pathlib.Path("study/img_dep")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("trafico.png", "1) El tráfico del enunciado", "info",
     "Picos solo en horario laboral (L-V 9-18) y casi nulo de noche y fin de semana. Eso significa que "
     "<b>la mayor parte de las horas de la semana el modelo está ocioso</b>. El enunciado además pide dos "
     "cosas explícitas: <b>escalar solo</b> y ser <b>barato en reposo</b>."),
    ("costo.png", "2) Costo acumulado de cada opción", "ok",
     "<b>D (serverless SIN provisioned)</b> es la línea más baja: en reposo (noches y fines de semana) cuesta "
     "prácticamente <b>0</b> porque solo pagas por inferencia ejecutada. Real-time (C) y serverless CON "
     "provisioned (A) mantienen capacidad reservada, así que <b>siguen cobrando aunque no haya tráfico</b>. "
     "Tu idea (provisioned solo en picos, línea morada) baja el costo, pero mira el siguiente panel."),
    ("provisioned.png", "3) Tu pregunta: ¿y comprar provisioned solo en las horas pico?", "key",
     "Es una idea razonable en la vida real, pero <b>no es la respuesta del examen</b> por 4 razones: (1) "
     "Provisioned Concurrency no es 'un horario que compras', es capacidad <b>reservada y facturada de forma "
     "continua</b> mientras esté configurada; (2) para encenderla/apagarla por horario necesitas "
     "<b>automatización extra</b> (EventBridge + scripts), lo que añade complejidad y ya no es 'escala solo'; "
     "(3) el enunciado pide la solución que <b>de fábrica</b> escala sola y es barata en reposo, y eso es D; "
     "(4) el único precio de D es tolerar algún <b>cold start</b>, aceptable con tráfico intermitente."),
    ("decision.png", "4) Árbol de decisión", "flow",
     "La regla del examen: primero mira si el tráfico es <b>constante</b> (→ Real-time endpoint) o "
     "<b>intermitente</b> (→ Serverless). Si es serverless, la única pregunta que queda es: ¿toleras cold "
     "starts? <b>Sí</b> (y quieres barato en reposo) → <b>D, serverless SIN provisioned</b>. <b>No</b> "
     "(latencia crítica, no puedes permitir el arranque en frío) → A, serverless CON provisioned. Esta carta "
     "cae en la rama D."),
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
<title>MLA-C01 · Despliegue: serverless sin provisioned</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #2e7d32; padding:16px 20px; border-radius:8px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .myth {{ background:#f3e5f5; border:1px solid #6a1b9a; border-radius:8px; padding:14px 18px; margin-bottom:20px; font-size:14.5px; }}
  .myth b {{ color:#6a1b9a; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(460px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.key {{ border-top-color:#6a1b9a; }}
  .card.flow {{ border-top-color:#1565c0; }}
  .card.info {{ border-top-color:#607d8b; }}
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
  <h1>Despliegue de modelo · Serverless SIN Provisioned Concurrency</h1>
  <p>MLA-C01 · tarjeta de estudio · por qué D gana a A</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> modelo de 2 GB, tráfico impredecible (picos en horario laboral, casi nulo de
    noche/fin de semana); debe escalar solo y ser barato en reposo. ¿Qué despliegue conviene?</p>
    <p><b>Respuesta: D —</b> endpoint serverless de SageMaker <b>SIN</b> Provisioned Concurrency.</p>
  </div>
  <div class="myth">
    <b>Tu duda:</b> "si los picos son en horarios predecibles, ¿no podríamos comprar provisioned para esos horarios?"
    &nbsp; <b>Respuesta corta:</b> en la vida real podrías, pero requeriría automatización extra (EventBridge subiendo/bajando
    la reserva) y dejaría de ser 'escala solo y barato en reposo de fábrica'. El examen premia la solución más simple que
    cumple los dos requisitos, y esa es <b>D</b>. Provisioned (A) solo se justifica si <b>no toleras cold starts</b>
    (latencia crítica), cosa que esta pregunta no pide.
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> tráfico <b>intermitente + barato en reposo</b> = <b>Serverless SIN Provisioned</b>.
    &nbsp; <b>Provisioned Concurrency</b> = pagas una reserva 24/7 para <b>eliminar el cold start</b> (solo si la latencia es crítica).
    &nbsp; Tráfico <b>constante/alto</b> = Real-time endpoint con auto-scaling. &nbsp; Lambda alojando el modelo casi nunca es la respuesta 'fully managed'.
  </div>
</div>
<footer>Generado para estudio local · gráficas de costo ilustrativas (no precios reales)</footer>
</body></html>"""

out = pathlib.Path("study/deployment_serverless.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
