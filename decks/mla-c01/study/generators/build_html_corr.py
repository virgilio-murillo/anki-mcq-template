#!/usr/bin/env python3
"""HTML de estudio: correlacion no lineal monotona -> Spearman."""
import base64
import pathlib

IMG = pathlib.Path("study/img_corr")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("tipos.png", "1) Los tres tipos de relación", "info",
     "<b>Lineal</b>: los puntos siguen una recta (Pearson la capta). <b>Monótona no lineal</b>: sube (o baja) "
     "siempre, pero en curva, no en recta; Pearson la subestima pero <b>Spearman la capta bien</b>. <b>No "
     "monótona</b>: sube y luego baja; ni Pearson ni Spearman la miden bien. La carta pide la del <b>medio</b>: "
     "una relación que es no lineal pero <b>monótona</b>."),
    ("rangos.png", "2) El truco de Spearman: usa RANGOS", "key",
     "¿Cómo capta Spearman una curva? Convierte los valores en <b>rangos</b> (posiciones: 1º, 2º, 3º...). Si "
     "cuando X sube Y también sube (aunque sea en curva), al ordenar por posición los rangos forman una "
     "<b>recta</b>. Por eso Spearman ≈ 1 en relaciones monótonas aunque los valores originales sean curvos. "
     "Pearson, en cambio, mide los valores crudos y ve la curva como 'no muy lineal'."),
    ("cuatro.png", "3) Los 4 coeficientes: cuál para qué", "ok",
     "<b>Spearman</b> = correlación monótona (no lineal) por rangos, el de rango <b>por defecto en muestras "
     "grandes</b> (esta carta). <b>Pearson</b> = solo relación lineal. <b>Kendall's Tau</b> = también monótona "
     "por rangos, pero se prefiere en muestras pequeñas/ordinales. <b>Cramér's V</b> = asociación entre "
     "variables <b>categóricas</b> (no numéricas). El truco es fijarte en 'lineal vs monótona' y en "
     "'numérica vs categórica'."),
    ("spearman_kendall.png", "4) Spearman vs Kendall: el desempate de la carta", "flow",
     "Este es el punto fino. Tanto Spearman como Kendall miden correlación monótona por rangos, así que ambos "
     "'servirían'. El desempate está en el enunciado: pide una <b>muestra grande</b> y <b>el coeficiente más "
     "usado por defecto</b> → eso es <b>Spearman</b>. Kendall's Tau no es incorrecto conceptualmente, pero es "
     "la alternativa para muestras <b>pequeñas u ordinales</b>, no el de defecto para muestras grandes."),
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
<title>MLA-C01 · Correlación no lineal (Spearman)</title>
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
  <h1>Correlación no lineal (monótona) · Spearman</h1>
  <p>MLA-C01 · tarjeta de estudio · Pearson vs Spearman vs Kendall vs Cramér's V</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Pregunta:</b> evaluar relaciones no lineales (monótonas) entre features de una <b>muestra grande</b>,
    prefiriendo el coeficiente <b>más usado por defecto</b>. ¿Qué coeficiente?</p>
    <p><b>Respuesta: A —</b> Spearman (correlación monótona por rangos).</p>
  </div>
  <div class="intro">
    <b>Clave:</b> "monótona" = sube o baja consistentemente (aunque sea en curva, no recta). Pearson solo capta
    rectas; Spearman capta curvas monótonas usando rangos. Y entre los dos de rango (Spearman y Kendall),
    "muestra grande + por defecto" apunta a Spearman.
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> <b>Lineal</b> (recta) = Pearson. &nbsp; <b>Monótona / no lineal</b> = Spearman (rangos), por defecto.
    &nbsp; <b>Muestra pequeña / ordinal</b> = Kendall's Tau. &nbsp; <b>Variables categóricas</b> = Cramér's V.
  </div>
</div>
<footer>Generado para estudio local · datos sintéticos ilustrativos</footer>
</body></html>"""

out = pathlib.Path("study/correlation_spearman.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
