#!/usr/bin/env python3
"""HTML: por que importa DPL (que problema resuelve) + el proposito de CI/TVD/KL."""
import base64
import pathlib

IMG = pathlib.Path("study/img_why")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


dpl_panels = [
    ("ejemplo.png", "1) Un ejemplo concreto: préstamos", "info",
     "Imagina que entrenas un modelo para aprobar préstamos usando datos históricos. En esos datos, al "
     "<b>Grupo A se le aprobó el 70%</b> de las solicitudes y al <b>Grupo B solo el 35%</b>. Esa brecha de 35 "
     "puntos es la <b>DPL</b>. Hasta aquí es solo un número; el problema aparece en el siguiente panel."),
    ("propaga.png", "2) El problema: el modelo copia el sesgo", "key",
     "Un modelo <b>aprende del pasado</b>. Si lo entrenas con datos donde un grupo salió sistemáticamente "
     "favorecido, el modelo <b>aprende ese patrón</b> ('A sí, B no') y lo <b>repite en cada decisión futura</b> "
     ", a gran escala y automáticamente. El modelo no inventa el sesgo: lo <b>hereda</b> de los datos. El "
     "resultado son decisiones injustas y, en dominios como crédito o contratación, potencialmente <b>ilegales</b>."),
    ("matiz.png", "3) Matiz clave: DPL alta NO siempre es problema", "info",
     "Una DPL alta es una <b>señal para investigar</b>, no una condena. Es un problema si la diferencia se debe "
     "a un <b>atributo protegido</b> (raza, género) sin razón legítima → discriminación. Pero puede ser "
     "aceptable si se explica por un <b>factor legítimo y relevante</b> (ej. ingresos reales distintos entre "
     "grupos). DPL no dice 'esto es injusto'; dice '<b>aquí hay una brecha grande, averigua por qué</b>'."),
    ("accion.png", "4) Qué haces al detectarla", "flow",
     "Por eso DPL es una métrica <b>pre-entrenamiento</b>: la revisas ANTES de entrenar. El ciclo es: "
     "<b>detectar</b> (Clarify la calcula) → <b>investigar</b> (¿legítima o sesgo?) → <b>corregir</b> los datos "
     "si es sesgo (re-balancear, quitar features problemáticas, recolectar más datos del grupo "
     "sub-representado) → <b>re-verificar</b> y monitorear en producción."),
]

otras_panels = [
    ("ci_why.png", "CI — el problema de la REPRESENTACIÓN", "ok",
     "CI no mira quién recibe positivos, sino <b>cuántos ejemplos hay de cada grupo</b>. Si el Grupo B es solo "
     "el 10% de los datos, el modelo <b>casi no lo ve</b> y aprende a predecir mal para él. El problema que "
     "resuelve CI: evitar que un grupo sub-representado reciba predicciones de peor calidad solo por falta de "
     "datos."),
    ("dist_why.png", "TVD y KL — el problema de las DISTRIBUCIONES completas", "ok",
     "DPL compara un solo número (la proporción de positivos). Pero a veces el problema es más sutil: la "
     "<b>distribución completa</b> de resultados/scores difiere entre grupos, no solo el promedio. <b>TVD</b> y "
     "<b>KL</b> miden cuánto se separan esas curvas enteras. Resuelven el problema de detectar diferencias de "
     "<b>forma</b> entre grupos que un solo promedio no capturaría. TVD lo hace de forma acotada [0,1] y "
     "simétrica; KL como divergencia general (no acotada)."),
    ("resumen_metricas.png", "Resumen: qué problema resuelve cada una", "key",
     "Todas responden de fondo la misma pregunta: <b>¿los datos tratan distinto a un grupo?</b> pero desde "
     "ángulos distintos. <b>DPL</b>: ¿a un grupo se le dan más resultados favorables? <b>CI</b>: ¿un grupo está "
     "sub-representado? <b>TVD/KL</b>: ¿la distribución completa de resultados difiere entre grupos? Elegir la "
     "métrica correcta depende de qué aspecto del sesgo te importa medir."),
]


def render(panels):
    out = []
    for fname, title, kind, desc in panels:
        out.append(f"""
    <div class="card {kind}">
      <div class="head"><span class="title">{title}</span></div>
      <img src="data:image/png;base64,{b64(fname)}" alt="{title}"/>
      <p class="desc">{desc}</p>
    </div>""")
    return "".join(out)


html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MLA-C01 · ¿Qué problema resuelven las métricas de sesgo?</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #6a1b9a; padding:16px 20px; border-radius:8px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  h2.sec {{ margin:28px 0 6px; color:#0f2a3f; font-size:17px; border-bottom:2px solid #cfd8dc; padding-bottom:6px; }}
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
  <h1>¿Qué problema resuelven las métricas de sesgo de Clarify?</h1>
  <p>MLA-C01 · tarjeta de estudio · el "por qué" detrás de DPL, CI, TVD y KL</p>
</header>
<div class="wrap">
  <div class="q">
    <p><b>Tu pregunta:</b> ¿cuál es el problema de que un grupo tenga muchos más positivos que otro?</p>
    <p><b>Respuesta corta:</b> un modelo aprende de los datos históricos. Si esos datos ya venían sesgados a
    favor de un grupo, el modelo <b>hereda y automatiza</b> ese sesgo, tomando decisiones injustas (y a veces
    ilegales). Las métricas de sesgo lo detectan <b>antes</b> de entrenar, para poder corregir los datos.</p>
  </div>

  <h2 class="sec">El problema que resuelve DPL (ejemplo de préstamos)</h2>
  <div class="grid">
    {render(dpl_panels)}
  </div>

  <h2 class="sec">Y las otras tres métricas: qué problema resuelve cada una</h2>
  <div class="grid">
    {render(otras_panels)}
  </div>

  <div class="tip">
    <b>La idea de fondo:</b> las 4 métricas responden "¿los datos tratan distinto a un grupo?" desde ángulos distintos.
    <b>DPL</b> = ¿más resultados positivos a un grupo? &nbsp; <b>CI</b> = ¿un grupo sub-representado? &nbsp;
    <b>TVD/KL</b> = ¿la distribución completa difiere entre grupos? &nbsp;
    Todas son pre-entrenamiento: sirven para detectar y corregir el sesgo ANTES de que el modelo lo aprenda.
  </div>
</div>
<footer>Generado para estudio local · ejemplos ilustrativos (no datos reales)</footer>
</body></html>"""

out = pathlib.Path("study/why_bias_metrics.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
