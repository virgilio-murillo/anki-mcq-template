#!/usr/bin/env python3
"""Graficas: preprocesamiento de texto ML event-driven con minimo overhead.
Explica el flujo de la opcion B y por que ECS/EKS/Batch/Glue son mas gestion.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_prep"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


def _box(ax, x, y, w, h, text, color, fc, fs=8.4):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=color, lw=1.8, transform=ax.transAxes))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color, fontweight="bold", transform=ax.transAxes)


def _arrow(ax, x1, y1, x2, y2, color="#555", label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color=color, lw=1.9))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.04, label, fontsize=7.6, color=color, ha="center", transform=ax.transAxes)


# ---------- 1) El flujo automatico de la opcion B ----------
def flujo_plot():
    fig, ax = plt.subplots(figsize=(7.4, 3.6)); ax.axis("off")
    ax.set_title("Opcion B — flujo automatico 'event-driven' (todo administrado)", fontsize=12, fontweight="bold", color=GREEN)
    _box(ax, 0.02, 0.40, 0.17, 0.30, "1. Subes\ndatos nuevos\na Amazon S3", GRIS, "#eceff1")
    _box(ax, 0.23, 0.40, 0.19, 0.30, "2. S3 Event\nNotification\n(detecta la subida)", AMBAR, "#fff8e1")
    _box(ax, 0.46, 0.40, 0.17, 0.30, "3. Lambda /\nStep Functions\n(dispara y orquesta)", AZUL, "#eef4fb")
    _box(ax, 0.67, 0.40, 0.30, 0.30, "4. SageMaker Processing Job\nlimpieza + tokenizacion +\nembeddings (TF / HuggingFace)", GREEN, "#e6f4ea", 7.8)
    _arrow(ax, 0.19, 0.55, 0.23, 0.55)
    _arrow(ax, 0.42, 0.55, 0.46, 0.55)
    _arrow(ax, 0.63, 0.55, 0.67, 0.55)
    ax.text(0.5, 0.18, "Nadie enciende ni administra servidores: el evento dispara un job administrado que corre y se apaga solo.",
            ha="center", fontsize=8.8, color=GREEN, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/flujo.png", dpi=130); plt.close(fig)


# ---------- 2) Esfuerzo de gestion por opcion (barras) ----------
def esfuerzo_plot():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    opts = ["B) Processing Job\n+ Lambda + S3 events", "A) ECS Fargate\n+ Glue + Batch",
            "C) Batch + Glue\n+ EKS", "D) Glue + Batch\n+ ECS Fargate"]
    esfuerzo = [1, 7, 9, 7]  # ilustrativo: unidades de "gestion/overhead"
    colors = [GREEN, ROJO, ROJO, ROJO]
    bars = ax.barh(opts, esfuerzo, color=colors, alpha=0.85)
    ax.invert_yaxis()
    ax.set_xlabel("esfuerzo de gestion / overhead (ilustrativo, menos = mejor)")
    ax.set_title("El enunciado pide 'MINIMO esfuerzo de gestion'", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(1.1, 0, "  administrado + event-driven", va="center", fontsize=9, color=GREEN, fontweight="bold")
    for i in range(1, 4):
        ax.text(esfuerzo[i] + 0.1, i, "  operas clusters/colas propias", va="center", fontsize=8.5, color=ROJO)
    ax.grid(alpha=0.25, axis="x")
    fig.tight_layout(); fig.savefig(f"{OUT}/esfuerzo.png", dpi=130); plt.close(fig)


# ---------- 3) Que servicio es para que (evitar confundirlos) ----------
def roles_plot():
    fig, ax = plt.subplots(figsize=(7.2, 4.6)); ax.axis("off")
    ax.set_title("Que hace cada servicio (por que solo B encaja)", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    filas = [
        ("SageMaker Processing Job", "Preprocesamiento de ML ADMINISTRADO (limpieza, tokenizacion, embeddings);\ntrae contenedores con TensorFlow y HuggingFace. Se ejecuta y se apaga solo.", GREEN, "SI"),
        ("Lambda + S3 Event Notifications", "Disparador serverless: reacciona a 'llego un archivo nuevo' y arranca el flujo.\nCero servidores que administrar.", GREEN, "SI"),
        ("Step Functions", "Orquesta los pasos del workflow sin servidores. Complementa a Lambda.", GREEN, "SI"),
        ("AWS Glue", "ETL de datos: exige definir esquemas y crawlers. Bueno para tablas/analytics,\nno para embeddings de ML con TF/HuggingFace. Mas overhead aqui.", AMBAR, "no"),
        ("ECS Fargate / EKS", "Corren TUS contenedores/Kubernetes: tu gestionas imagenes, escalado, red.\nEs 'traer tu propia infra', lo contrario de minimo esfuerzo.", ROJO, "no"),
        ("AWS Batch", "Orquesta jobs por lotes en colas: capa extra innecesaria, los Processing Jobs\nse ejecutan directo sin Batch.", ROJO, "no"),
    ]
    y = 0.82
    for nombre, det, color, ok in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.055), 0.94, 0.115, fc=color, alpha=0.10, ec=color, lw=1.3, transform=ax.transAxes))
        ax.text(0.05, y + 0.018, nombre, fontsize=9.2, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.05, y - 0.028, det, fontsize=7.7, color="#37424c", va="center", transform=ax.transAxes)
        ax.text(0.95, y, ok, fontsize=10, fontweight="bold", color=color, va="center", ha="right", transform=ax.transAxes)
        y -= 0.135
    fig.tight_layout(); fig.savefig(f"{OUT}/roles.png", dpi=130); plt.close(fig)


# ---------- 4) Regla de decision ----------
def regla_plot():
    fig, ax = plt.subplots(figsize=(7.2, 3.8)); ax.axis("off")
    ax.set_title("Como reconocer estas preguntas en el examen", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    reglas = [
        ("'preprocesamiento de ML administrado'", "-> SageMaker Processing Job", GREEN),
        ("'disparado al subir datos / al llegar un evento'", "-> S3 Event Notifications + Lambda", AZUL),
        ("'orquestar pasos sin servidores'", "-> Step Functions", AZUL),
        ("'ETL de datos, esquemas, tablas'", "-> AWS Glue (NO para embeddings ML)", AMBAR),
        ("'minimo esfuerzo / menos gestion'", "-> descarta ECS, EKS, Batch (infra propia)", ROJO),
    ]
    y = 0.82
    for cond, sol, color in reglas:
        ax.text(0.04, y, cond, fontsize=9.2, color="#333", va="center", transform=ax.transAxes)
        ax.text(0.55, y, sol, fontsize=9.2, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        y -= 0.16
    fig.tight_layout(); fig.savefig(f"{OUT}/regla.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    flujo_plot(); esfuerzo_plot(); roles_plot(); regla_plot()
    print(">> 4 graficas de preprocesamiento escritas en study/img_prep/", flush=True)
