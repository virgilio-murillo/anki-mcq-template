#!/usr/bin/env python3
"""HTML de estudio para online vs offline store (Feature Store)."""
import base64
import pathlib

IMG = pathlib.Path("study/img_fs")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("vocab.png", "1) El malentendido está en la palabra", "key",
     "Tu intuición dice: 'offline = descargado = rápido, online = por internet = lento'. Eso es correcto en la "
     "vida diaria, pero <b>en Feature Store significa lo contrario</b>. Aquí <b>online</b> no quiere decir "
     "'por internet': quiere decir <b>'en línea / en vivo, atendiendo peticiones en producción'</b>. Y "
     "<b>offline</b> quiere decir <b>'fuera de la ruta en vivo, trabajo por lotes'</b>. No es una cuestión de "
     "conexión, sino de <b>en qué momento del ciclo de ML se usa</b>."),
    ("compare.png", "2) Comparación lado a lado", "ok",
     "El <b>online store</b> guarda solo el <b>valor más reciente</b> de cada feature en un almacén rápido "
     "(clave-valor) para responder en <b>milisegundos</b> cuando tu app pide 'dame las features del usuario X "
     "ahora'. El <b>offline store</b> guarda <b>todo el histórico</b> en <b>S3</b> (barato) para entrenar el "
     "modelo o hacer análisis por lotes, donde tardar minutos no importa."),
    ("latency.png", "3) ¿Quién es realmente rápido?", "ok",
     "Por diseño, el <b>online store es el rápido</b> (sub-segundo), porque su trabajo es servir inferencia en "
     "vivo. El offline store ni siquiera intenta ser rápido por lectura: procesa grandes volúmenes de golpe. "
     "El nombre 'offline' <b>no</b> significa veloz; significa 'no está en la ruta de producción en vivo'."),
    ("flow.png", "4) Dónde entra cada uno en el flujo", "flow",
     "El mismo feature group alimenta <b>dos caminos</b>: el <b>offline store</b> (→ S3 → entrenar el modelo, "
     "por lotes) y el <b>online store</b> (→ la app en vivo que necesita responder ya). Por eso la respuesta "
     "correcta a la pregunta es <b>A: el online store da lecturas de baja latencia para inferencia en tiempo "
     "real</b>."),
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
<title>MLA-C01 · Feature Store: online vs offline</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #6a1b9a; padding:16px 20px; border-radius:8px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .myth {{ background:#fdecec; border:1px solid #c62828; border-radius:8px; padding:14px 18px; margin-bottom:20px; font-size:14.5px; }}
  .myth b {{ color:#c62828; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(440px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.key {{ border-top-color:#6a1b9a; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.flow {{ border-top-color:#1565c0; }}
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
  <h1>SageMaker Feature Store · Online store vs Offline store</h1>
  <p>MLA-C01 · tarjeta de estudio · aclarando la confusión del nombre</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> ¿para qué sirve el <b>online store</b> (frente al offline store)?</p>
    <p><b>Respuesta: A —</b> lecturas de baja latencia (sub-segundo) de features para <b>inferencia en tiempo real</b>.</p>
  </div>
  <div class="myth">
    <b>Tu duda (muy común):</b> "yo entendería que offline es más rápido que online". &nbsp;
    <b>Por qué no:</b> aquí <b>online</b> no significa 'por internet' sino <b>'en vivo, sirviendo peticiones en producción'</b> →
    por eso es el que necesita ser <b>ultra rápido (ms)</b>. <b>Offline</b> significa <b>'por lotes, fuera de la ruta en vivo'</b> →
    guarda el histórico en S3 y no le corre prisa. El nombre describe el <b>momento de uso</b>, no la velocidad de la conexión.
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> <b>Online store</b> = inferencia en vivo, baja latencia (ms), valor más reciente.
    &nbsp; <b>Offline store</b> = training / batch / análisis, histórico completo en S3.
    &nbsp; Mnemónica: "onLINE = en LÍNEA atendiendo ahora" (rápido) ; "OFFline = trabajo apartado por lotes".
  </div>
</div>
<footer>Generado para estudio local · diagramas ilustrativos</footer>
</body></html>"""

out = pathlib.Path("study/feature_store_online_offline.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
