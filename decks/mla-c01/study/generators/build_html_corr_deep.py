#!/usr/bin/env python3
"""HTML de estudio profundo: los 4 coeficientes de correlacion en detalle."""
import base64
import pathlib

IMG = pathlib.Path("study/img_corr2")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("pearson.png", "PEARSON · ¿qué tan RECTA es la relación?", "azul",
     "<b>Qué mide:</b> qué tan cerca de una <b>línea recta</b> están los puntos. <b>Lógica:</b> asume que la "
     "relación es proporcional (si X sube el doble, Y sube el doble). <b>Situación real:</b> horas de estudio vs "
     "nota, temperatura vs consumo eléctrico... cuando esperas una relación lineal entre <b>números continuos</b>. "
     "<b>Su debilidad:</b> si la relación es una curva (aunque suba siempre), Pearson la subestima, porque no es "
     "una recta."),
    ("spearman.png", "SPEARMAN · ¿se conserva el ORDEN?", "verde",
     "<b>Qué mide:</b> si cuando X sube, Y también sube (o baja) de forma consistente, <b>sin importar si es "
     "recta o curva</b>. <b>Lógica:</b> convierte los valores en <b>rangos</b> (1º, 2º, 3º...) y mide la "
     "correlación de esos rangos; así una curva monótona se vuelve una recta de rangos. <b>Situación real:</b> "
     "ranking de precio vs demanda, nivel socioeconómico vs gasto... relaciones que suben/bajan pero no "
     "proporcionalmente. <b>Por qué por defecto:</b> es rápido y estándar para <b>muestras grandes</b>."),
    ("kendall.png", "KENDALL'S TAU · ¿cuántos PARES van igual?", "ambar",
     "<b>Qué mide:</b> toma cada <b>par</b> de observaciones y cuenta si van en el mismo sentido "
     "(<b>concordante</b>) o al revés (<b>discordante</b>). Tau = (concordantes − discordantes) / total. "
     "<b>Lógica:</b> en vez de rangos globales, cuenta acuerdos par a par, lo que lo hace muy robusto con pocos "
     "datos. <b>Situación real:</b> muestras <b>pequeñas</b> o datos <b>ordinales</b> (encuestas 'malo/regular/"
     "bueno', rankings). <b>Diferencia con Spearman:</b> mismo objetivo (correlación monótona), pero Kendall es "
     "más estable con pocos datos; Spearman es el estándar con muchos."),
    ("cramer.png", "CRAMÉR'S V · ¿se asocian dos CATEGORÍAS?", "rojo",
     "<b>Qué mide:</b> la asociación entre dos variables <b>categóricas</b> (sin orden numérico): color, ciudad, "
     "sí/no, tipo de producto. <b>Lógica:</b> construye una <b>tabla de contingencia</b> (cuántos caen en cada "
     "combinación) y resume en un número de 0 a 1 qué tan relacionadas están. <b>Situación real:</b> ¿el género "
     "se asocia con la preferencia de producto? ¿la región con si compra o no? <b>Diferencia clave:</b> los "
     "otros tres son para <b>números</b>; Cramér's V es el único para <b>categorías</b>."),
    ("decision.png", "Cómo decidir cuál usar", "flow",
     "La lógica de elección va en tres pasos: (1) ¿tus datos son <b>números o categorías</b>? Categorías → "
     "Cramér's V. (2) Si son números, ¿la relación es <b>recta o curva-monótona</b>? Recta → Pearson; "
     "curva-monótona → Spearman/Kendall. (3) Entre Spearman y Kendall: <b>muestra grande</b> → Spearman (por "
     "defecto); <b>muestra pequeña/ordinal</b> → Kendall. Esa es toda la lógica."),
]

kind_map = {"azul": "info", "verde": "ok", "ambar": "warn", "rojo": "bad", "flow": "flow"}
blocks = []
for fname, title, kind, desc in panels:
    blocks.append(f"""
    <div class="card {kind_map[kind]}">
      <div class="head"><span class="title">{title}</span></div>
      <img src="data:image/png;base64,{b64(fname)}" alt="{title}"/>
      <p class="desc">{desc}</p>
    </div>""")

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MLA-C01 · Coeficientes de correlación en profundidad</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .intro {{ background:#eef4fb; border:1px solid #1565c0; border-radius:8px; padding:14px 18px; margin-bottom:20px; font-size:14.5px; line-height:1.55; }}
  .intro b {{ color:#1565c0; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(470px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.info {{ border-top-color:#1565c0; }}
  .card.ok {{ border-top-color:#2e7d32; }}
  .card.warn {{ border-top-color:#f9a825; }}
  .card.bad {{ border-top-color:#c62828; }}
  .card.flow {{ border-top-color:#6a1b9a; }}
  .card img {{ width:100%; height:auto; border-radius:6px; }}
  .head {{ margin-bottom:8px; }}
  .title {{ font-weight:700; font-size:15px; }}
  .desc {{ font-size:13.5px; line-height:1.6; color:#37424c; margin:10px 2px 2px; }}
  .tip {{ background:#fff8e1; border:1px solid #f9a825; border-radius:8px; padding:12px 16px; margin-top:20px; font-size:14px; }}
  .tip b {{ color:#b26a00; }}
  footer {{ text-align:center; color:#90a4ae; font-size:12px; padding:18px; }}
</style></head>
<body>
<header>
  <h1>Coeficientes de correlación · utilidad, situación, diferencias y lógica</h1>
  <p>MLA-C01 · tarjeta de estudio profunda · Pearson · Spearman · Kendall · Cramér's V</p>
</header>
<div class="wrap">
  <div class="intro">
    <b>La idea base:</b> una correlación es un número (de −1 a +1) que dice: "cuando una variable cambia, ¿la
    otra cambia de forma predecible?". &nbsp; <b>+1</b> = suben juntas; <b>0</b> = sin relación; <b>−1</b> = una
    sube y la otra baja. &nbsp; Los 4 coeficientes responden esa misma pregunta, pero cada uno asume un
    <b>tipo distinto de "cambio predecible"</b> y sirve para un <b>tipo distinto de datos</b>. Por eso existen varios.
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Resumen en una línea:</b>
    <b>Pearson</b> = relación recta (lineal), números. &nbsp;
    <b>Spearman</b> = relación monótona (curva que sube/baja), por rangos, por defecto en muestras grandes. &nbsp;
    <b>Kendall's Tau</b> = igual que Spearman pero por pares concordantes/discordantes, mejor con muestras pequeñas/ordinales. &nbsp;
    <b>Cramér's V</b> = asociación entre categorías (no números).
  </div>
</div>
<footer>Generado para estudio local · datos y ejemplos ilustrativos</footer>
</body></html>"""

out = pathlib.Path("study/correlation_deep.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
