#!/usr/bin/env python3
"""HTML de estudio: streaming tiempo real con minima operacion (opcion A)."""
import base64
import pathlib

IMG = pathlib.Path("study/img_stream")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("flujo.png", "1) El pipeline que arma la opción A", "ok",
     "La cadena es: el <b>flujo de transacciones</b> entra por <b>Kinesis Data Streams</b> (ingesta de baja "
     "latencia) → <b>Managed Service for Apache Flink</b> transforma/agrega en tiempo real → el resultado va a "
     "<b>SageMaker</b> para la inferencia de fraude. Las dos primeras piezas son las que 'ingieren y procesan "
     "el stream antes de la inferencia', y ambas son <b>administradas</b> (no gestionas clústeres)."),
    ("cuadrante.png", "2) Las DOS preguntas que resuelven la carta", "key",
     "Esta pregunta tiene dos requisitos a la vez: <b>tiempo real</b> y <b>mínima operación</b>. Ubica cada "
     "opción en el cuadrante: <b>A</b> está arriba-derecha (tiempo real + administrado) = ganadora. <b>B y D</b> "
     "están a la izquierda (por lotes) → fallan 'tiempo real'. <b>C</b> está abajo-derecha (tiempo real, pero "
     "autogestionado) → falla 'mínima operación'. Solo A cumple ambos ejes."),
    ("kinesis_msk.png", "3) Kinesis vs MSK: la trampa de la opción C", "info",
     "Ojo con C: <b>MSK (Kafka) también hace streaming en tiempo real</b>, así que técnicamente 'funciona'. La "
     "diferencia es la <b>carga operativa</b>: con MSK tú dimensionas y operas los brokers y particiones, y "
     "además despliegas y mantienes Flink sobre el clúster. Kinesis Data Streams + Managed Flink hacen lo mismo "
     "pero <b>administrado</b>. Como la carta pide 'la menor carga operativa', C queda descartada por ser la de "
     "MAYOR operación."),
    ("regla.png", "4) Cómo decidir en el examen", "flow",
     "Primero pregunta: ¿tiempo real o por lotes? Glue, Athena, EMR nocturno y SQS son de <b>lotes</b> → "
     "descarta B y D de inmediato. Luego: entre las de tiempo real, ¿cuál es administrada? Kinesis + Managed "
     "Flink (A) es administrada; MSK + Flink propio (C) te obliga a operar todo. Respuesta: <b>A</b>."),
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
<title>MLA-C01 · Streaming en tiempo real (Kinesis + Flink)</title>
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
  .card.key {{ border-top-color:#6a1b9a; }}
  .card.info {{ border-top-color:#1565c0; }}
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
  <h1>Streaming en tiempo real · Kinesis Data Streams + Managed Flink</h1>
  <p>MLA-C01 · tarjeta de estudio · tiempo real + mínima operación</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> detección de fraude sobre un flujo continuo de transacciones que luego pasa a SageMaker,
    con la <b>menor carga operativa</b>. ¿Qué pareja ingiere y procesa el stream antes de la inferencia?</p>
    <p><b>Respuesta: A —</b> Amazon Kinesis Data Streams (ingesta) + Amazon Managed Service for Apache Flink (procesamiento en tiempo real).</p>
  </div>
  <div class="intro">
    <b>La carta tiene dos requisitos a la vez:</b> (1) <b>tiempo real</b> y (2) <b>mínima operación</b>.
    B y D fallan el primero (son de lotes). C falla el segundo (tiempo real, pero tú operas los brokers y el motor). Solo A cumple ambos.
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> tiempo real + mínima operación = <b>Kinesis Data Streams + Managed Service for Apache Flink</b>.
    &nbsp; <b>MSK</b> también es streaming en tiempo real, pero implica autogestionar brokers/particiones y el motor Flink (mayor operación).
    &nbsp; <b>Glue/Athena/EMR/SQS</b> = por lotes, no tiempo real.
  </div>
</div>
<footer>Generado para estudio local · diagramas ilustrativos</footer>
</body></html>"""

out = pathlib.Path("study/streaming_realtime.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
