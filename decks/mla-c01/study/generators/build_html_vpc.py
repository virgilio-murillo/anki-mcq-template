#!/usr/bin/env python3
"""HTML de estudio: gateway vs interface VPC endpoint."""
import base64
import pathlib

IMG = pathlib.Path("study/img_vpc")


def b64(name):
    return base64.b64encode((IMG / name).read_bytes()).decode()


panels = [
    ("gateway.png", "1) Gateway endpoint — una ruta", "info",
     "Es un <b>objetivo de ruteo</b>: agregas una entrada en la <b>tabla de rutas</b> de tu VPC y el tráfico "
     "hacia S3 o DynamoDB va por la red de AWS en lugar de por internet. Es <b>gratis</b> y simple, pero "
     "<b>no crea ninguna IP privada ni interfaz de red</b>. Solo funciona para recursos <b>de esa misma VPC</b> "
     "y hacia el servicio <b>de la misma región</b>."),
    ("interface.png", "2) Interface endpoint (PrivateLink) — una ENI", "ok",
     "Crea una <b>interfaz de red (ENI) con IP privada</b> dentro de tu subred. El tráfico entra por esa IP "
     "privada y viaja por <b>AWS PrivateLink</b>. Soporta <b>muchos servicios</b> (S3, SageMaker, KMS, ECR...) "
     "y, lo clave: puede recibir tráfico <b>desde on-premises o desde otra VPC/región</b> (combinado con VPC "
     "peering o Transit Gateway). Tiene un costo por hora + por datos."),
    ("compare.png", "3) Por qué existen dos", "key",
     "Existen dos porque resuelven el mismo objetivo (llegar a un servicio AWS sin salir a internet) con "
     "<b>mecanismos distintos</b>. El <b>gateway</b> es la opción barata y por defecto para S3/DynamoDB dentro "
     "de tu región. El <b>interface</b> es más potente y flexible (más servicios, cross-VPC, cross-region, "
     "on-prem, IP privada) a cambio de un costo. No es que uno sea mejor: cada uno cubre casos que el otro no."),
    ("decision.png", "4) Cuándo elegir cuál (y esta carta)", "flow",
     "Regla: usa <b>gateway</b> por defecto si solo necesitas S3/DynamoDB dentro de la misma VPC y región "
     "(gratis). Cambia a <b>interface</b> cuando el gateway <b>no alcanza</b>: otro servicio, acceso desde "
     "on-prem u otra VPC, o <b>un bucket en otra región</b>. Esta carta cae justo en el último caso: la VPC "
     "está en us-west-2 y el bucket S3 en us-east-1 (otra región). Como el gateway es <b>intra-región</b>, no "
     "llega; por eso la respuesta es el <b>interface endpoint</b> (+ peering/TGW)."),
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
<title>MLA-C01 · Gateway vs Interface VPC endpoint</title>
<style>
  body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; background:#f4f6f8; color:#1e2227; }}
  header {{ background:#0f2a3f; color:#fff; padding:22px 28px; }}
  header h1 {{ margin:0 0 6px; font-size:20px; }}
  header p {{ margin:0; color:#b9c7d3; font-size:14px; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px; }}
  .q {{ background:#fff; border-left:5px solid #2e7d32; padding:16px 20px; border-radius:8px; margin-bottom:16px; box-shadow:0 1px 4px rgba(0,0,0,.06); }}
  .q b {{ color:#0f2a3f; }}
  .note {{ background:#eef4fb; border:1px solid #1565c0; border-radius:8px; padding:12px 18px; margin-bottom:20px; font-size:14px; }}
  .note b {{ color:#1565c0; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(460px,1fr)); gap:18px; }}
  .card {{ background:#fff; border-radius:10px; padding:14px; box-shadow:0 1px 5px rgba(0,0,0,.08); border-top:4px solid #607d8b; }}
  .card.ok {{ border-top-color:#6a1b9a; }}
  .card.key {{ border-top-color:#0f2a3f; }}
  .card.flow {{ border-top-color:#2e7d32; }}
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
  <h1>VPC Endpoints · Gateway vs Interface (PrivateLink)</h1>
  <p>MLA-C01 · tarjeta de estudio · dos formas de llegar a AWS sin salir a internet</p>
</header>
<div class="wrap">
  <div class="note">
    <b>Aclaración de nombres:</b> esto es <b>gateway endpoint</b> vs <b>interface endpoint</b> (tipos de VPC endpoint
    para conectividad privada). No confundir con "inference endpoint", que es el de servir modelos en SageMaker (otro tema).
  </div>
  <div class="q">
    <p><b>Escenario de la carta:</b> un training job en <b>us-west-2</b> debe leer un bucket S3 en <b>us-east-1</b>
    (otra región) sin salir a internet, sin duplicar datos y sin cambiar de servicio.</p>
    <p><b>Respuesta: D —</b> interface endpoint (PrivateLink) + conectividad cross-region (peering/TGW).</p>
  </div>
  <div class="grid">
    {''.join(blocks)}
  </div>
  <div class="tip">
    <b>Regla para el examen:</b> <b>Gateway</b> = ruta en la tabla, gratis, solo S3/DynamoDB, intra-región, intra-VPC.
    &nbsp; <b>Interface (PrivateLink)</b> = ENI con IP privada, muchos servicios, admite on-prem y otra VPC/región (peering/TGW).
    &nbsp; Ambos endpoints son regionales; si el recurso está en otra región o necesitas on-prem/otra VPC → interface.
  </div>
</div>
<footer>Generado para estudio local · diagramas ilustrativos</footer>
</body></html>"""

out = pathlib.Path("study/vpc_endpoints_gateway_vs_interface.html")
out.write_text(html, encoding="utf-8")
print(f">> escrito {out}", flush=True)
