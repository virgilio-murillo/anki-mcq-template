#!/usr/bin/env python3
"""Graficas para la carta MLA: SageMaker Feature Store online vs offline store.
Objetivo: romper la confusion de que 'offline suena mas rapido'. Explica que
online = servir en vivo (ms), offline = historico por lotes en S3.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_fs"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- 1) El malentendido: que crees vs que significa ----------
def vocab_plot():
    fig, ax = plt.subplots(figsize=(6.6, 4.6)); ax.axis("off")
    ax.set_title("El malentendido esta en la PALABRA, no en la tecnologia", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    # columna izquierda: intuicion (incorrecta)
    ax.text(0.25, 0.90, "Lo que suena (intuicion)", ha="center", fontsize=11, fontweight="bold", color=ROJO, transform=ax.transAxes)
    ax.text(0.25, 0.74, "OFFLINE\n= descargado / local\n= 'deberia ser rapido'", ha="center", fontsize=10, color=ROJO, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.85))
    ax.text(0.25, 0.44, "ONLINE\n= por internet\n= 'deberia ser lento'", ha="center", fontsize=10, color=ROJO, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.85))
    ax.text(0.25, 0.16, "X  INCORRECTO aqui", ha="center", fontsize=11, fontweight="bold", color=ROJO, transform=ax.transAxes)
    # flecha
    ax.annotate("", xy=(0.56, 0.55), xytext=(0.44, 0.55), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color="#333", lw=2))
    # columna derecha: lo que significa en AWS
    ax.text(0.76, 0.90, "Lo que significa en AWS", ha="center", fontsize=11, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.76, 0.74, "ONLINE store\n= 'EN LINEA / EN VIVO'\nsirve en produccion en ms", ha="center", fontsize=10, color=GREEN, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.9))
    ax.text(0.76, 0.44, "OFFLINE store\n= 'FUERA DE LINEA / POR LOTES'\nhistorico en S3, sin prisa", ha="center", fontsize=10, color=AZUL, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#eef4fb", ec=AZUL, alpha=0.9))
    ax.text(0.76, 0.16, "online NO = internet.\nonline = 'atendiendo en vivo'", ha="center", fontsize=9.5, fontweight="bold", color="#0f2a3f", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/vocab.png", dpi=130); plt.close(fig)


# ---------- 2) Comparacion lado a lado (tabla visual) ----------
def compare_plot():
    fig, ax = plt.subplots(figsize=(6.6, 4.6)); ax.axis("off")
    ax.set_title("Online store  vs  Offline store", fontsize=13, fontweight="bold", color="#0f2a3f")
    filas = [
        ("Para que", "Inferencia EN VIVO\n(responder una peticion ya)", "Training / batch / analisis\n(procesar mucho de golpe)"),
        ("Velocidad", "Sub-segundo (ms)", "No importa la latencia\n(minutos esta bien)"),
        ("Donde vive", "Almacen rapido tipo\nclave-valor (baja latencia)", "Amazon S3\n(barato, historico)"),
        ("Cuanto guarda", "El valor MAS RECIENTE\nde cada feature", "TODO el historico\n(series completas)"),
        ("Ejemplo", "App de fraude pide las\nfeatures del usuario X -> ms", "Entrenar el modelo con\n2 anios de datos"),
    ]
    y = 0.80; dy = 0.155
    ax.text(0.06, 0.90, "", transform=ax.transAxes)
    ax.text(0.30, 0.90, "ONLINE (en vivo)", ha="center", fontsize=10.5, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.74, 0.90, "OFFLINE (por lotes)", ha="center", fontsize=10.5, fontweight="bold", color=AZUL, transform=ax.transAxes)
    for label, on, off in filas:
        ax.text(0.02, y, label, fontsize=9.5, fontweight="bold", color="#333", va="center", transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((0.16, y - 0.06), 0.29, 0.12, fc="#e6f4ea", ec=GREEN, alpha=0.7, transform=ax.transAxes))
        ax.text(0.305, y, on, ha="center", va="center", fontsize=8.3, color="#1b4d24", transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((0.58, y - 0.06), 0.34, 0.12, fc="#eef4fb", ec=AZUL, alpha=0.7, transform=ax.transAxes))
        ax.text(0.75, y, off, ha="center", va="center", fontsize=8.3, color="#0d3a66", transform=ax.transAxes)
        y -= dy
    fig.tight_layout(); fig.savefig(f"{OUT}/compare.png", dpi=130); plt.close(fig)


# ---------- 3) El flujo: donde entra cada store ----------
def flow_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.6)); ax.axis("off")
    ax.set_title("Donde se usa cada store en el ciclo de ML", fontsize=12.5, fontweight="bold", color="#0f2a3f")

    def box(x, y, w, h, text, color, fc):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=color, lw=1.8, transform=ax.transAxes))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.6, color=color, fontweight="bold", transform=ax.transAxes)

    def arrow(x1, y1, x2, y2, color="#555"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color=color, lw=1.8))

    box(0.02, 0.62, 0.22, 0.16, "Data Wrangler\nprepara features", GRIS, "#eceff1")
    box(0.39, 0.62, 0.22, 0.16, "FEATURE STORE\n(un feature group)", MORADO, "#f3e5f5")
    arrow(0.24, 0.70, 0.39, 0.70)

    # rama offline (arriba)
    box(0.72, 0.80, 0.25, 0.15, "OFFLINE store (S3)\nhistorico completo", AZUL, "#eef4fb")
    arrow(0.61, 0.72, 0.72, 0.86, AZUL)
    box(0.72, 0.58, 0.25, 0.15, "Entrenar modelo\n(batch, lento OK)", AZUL, "#eef4fb")
    arrow(0.845, 0.80, 0.845, 0.73, AZUL)

    # rama online (abajo)
    box(0.72, 0.30, 0.25, 0.15, "ONLINE store\nvalor mas reciente", GREEN, "#e6f4ea")
    arrow(0.61, 0.68, 0.72, 0.37, GREEN)
    box(0.72, 0.08, 0.25, 0.15, "App en vivo pide\nfeatures -> responde ms", GREEN, "#e6f4ea")
    arrow(0.845, 0.30, 0.845, 0.23, GREEN)

    ax.text(0.5, 0.005, "Mismo feature, dos caminos: OFFLINE alimenta el entrenamiento; ONLINE atiende la inferencia en vivo.",
            ha="center", fontsize=8.6, color="#0f2a3f", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/flow.png", dpi=130); plt.close(fig)


# ---------- 4) Latencia comparada (barra) ----------
def latency_plot():
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    labels = ["ONLINE store\n(inferencia en vivo)", "OFFLINE store\n(lote/training)"]
    lat = [0.01, 90]  # segundos (ilustrativo): ms vs minutos
    colors = [GREEN, AZUL]
    bars = ax.barh(labels, lat, color=colors, alpha=0.85, log=True)
    ax.set_xlabel("latencia tipica por lectura (escala log, segundos)")
    ax.set_title("Quien es 'rapido': el ONLINE store (por diseno)", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(0.011, 0, "  ~10 ms  (sub-segundo)", va="center", fontsize=10, color=GREEN, fontweight="bold")
    ax.text(90, 1, "  minutos (no importa)", va="center", fontsize=10, color=AZUL, fontweight="bold")
    ax.text(0.5, -0.32, "El nombre 'offline' NO significa rapido: significa 'fuera de la ruta en vivo'.",
            transform=ax.transAxes, ha="center", fontsize=9, color=ROJO)
    ax.grid(alpha=0.25, axis="x")
    fig.tight_layout(); fig.savefig(f"{OUT}/latency.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    vocab_plot(); compare_plot(); flow_plot(); latency_plot()
    print(">> 4 graficas de feature store escritas en study/img_fs/", flush=True)
