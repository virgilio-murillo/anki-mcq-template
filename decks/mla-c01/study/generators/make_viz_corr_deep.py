#!/usr/bin/env python3
"""Explicacion profunda de los 4 coeficientes de correlacion: utilidad, situacion
de uso, diferencias y logica. Pearson / Spearman / Kendall / Cramer's V.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_corr2"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(9)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- 1) PEARSON: mide que tan RECTA es la nube ----------
def pearson_plot():
    fig, axes = plt.subplots(1, 3, figsize=(7.8, 3.0))
    x = np.linspace(0, 10, 40)
    datos = [
        (2 * x + rng.normal(0, 1, 40), "recta apretada\nPearson ~ +0.98", GREEN),
        (2 * x + rng.normal(0, 6, 40), "recta con ruido\nPearson ~ +0.6", AMBAR),
        (np.exp(x / 2.5) + rng.normal(0, 3, 40), "curva (sube siempre)\nPearson BAJA ~ 0.7\naunque sube claramente", ROJO),
    ]
    for ax, (y, t, c) in zip(axes, datos):
        ax.scatter(x, y, s=14, color=c, alpha=0.7)
        ax.set_title(t, fontsize=8.2, color=c, fontweight="bold")
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("PEARSON: mide que tan cerca de una LINEA RECTA estan los puntos", fontsize=10.5, fontweight="bold", color=AZUL)
    fig.text(0.5, 0.02, "Util para: relaciones lineales entre numeros continuos (ej. horas de estudio vs nota, si es proporcional).",
             ha="center", fontsize=8, color="#333")
    fig.tight_layout(rect=[0, 0.06, 1, 0.90]); fig.savefig(f"{OUT}/pearson.png", dpi=130); plt.close(fig)


# ---------- 2) SPEARMAN: mide si el ORDEN se conserva ----------
def spearman_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    y = np.array([2, 3, 5, 9, 16, 30, 55, 100])  # crece en curva pero SIEMPRE sube
    ax.plot(x, y, "-o", color=GREEN, lw=1.8)
    for xi, yi, r in zip(x, y, range(1, 9)):
        ax.annotate(f"rango {r}", (xi, yi), textcoords="offset points", xytext=(-5, 8), fontsize=7.5, color=MORADO)
    ax.set_title("SPEARMAN: ¿se conserva el ORDEN? (aunque sea curva)", fontsize=11, fontweight="bold", color=GREEN)
    ax.set_xlabel("X (ordenado 1o..8o)"); ax.set_ylabel("Y")
    ax.text(0.03, 0.92, "Cada punto que avanza en X tambien avanza en el ranking de Y\n-> el ORDEN se conserva perfecto -> Spearman = 1.",
            transform=ax.transAxes, fontsize=8.2, color=GREEN, va="top",
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.85))
    ax.text(0.5, -0.2, "Util para: relaciones que suben/bajan consistentemente aunque no sean rectas (ej. ranking de precio vs demanda).",
            transform=ax.transAxes, ha="center", fontsize=8, color="#333")
    fig.tight_layout(); fig.savefig(f"{OUT}/spearman.png", dpi=130); plt.close(fig)


# ---------- 3) KENDALL: cuenta pares concordantes vs discordantes ----------
def kendall_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.2)); ax.axis("off")
    ax.set_title("KENDALL'S TAU: cuenta PARES concordantes vs discordantes", fontsize=11, fontweight="bold", color=AMBAR)
    ax.text(0.5, 0.86, "Toma cada PAR de observaciones y pregunta: ¿van en el mismo sentido?", ha="center", fontsize=9, color="#333", transform=ax.transAxes)
    # dos ejemplos de pares
    ax.add_patch(plt.Rectangle((0.05, 0.50), 0.42, 0.28, fc="#e6f4ea", ec=GREEN, lw=1.6, transform=ax.transAxes))
    ax.text(0.26, 0.72, "PAR CONCORDANTE", ha="center", fontsize=9, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.26, 0.58, "Persona 1: mas edad Y mas ingreso\nPersona 2: menos edad Y menos ingreso\n-> van igual (concordante)", ha="center", fontsize=7.8, color="#1b4d24", transform=ax.transAxes)
    ax.add_patch(plt.Rectangle((0.53, 0.50), 0.42, 0.28, fc="#fdecec", ec=ROJO, lw=1.6, transform=ax.transAxes))
    ax.text(0.74, 0.72, "PAR DISCORDANTE", ha="center", fontsize=9, fontweight="bold", color=ROJO, transform=ax.transAxes)
    ax.text(0.74, 0.58, "Persona 1: mas edad pero MENOS ingreso\nPersona 2: menos edad pero MAS ingreso\n-> van al reves (discordante)", ha="center", fontsize=7.8, color="#8a1c1c", transform=ax.transAxes)
    ax.text(0.5, 0.36, "Tau = (concordantes - discordantes) / total de pares.", ha="center", fontsize=9.5, fontweight="bold", color="#0f2a3f", transform=ax.transAxes)
    ax.text(0.5, 0.16, "Util para: muestras PEQUENAS o datos ORDINALES (ej. rankings tipo 1o/2o/3o, encuestas 'malo/regular/bueno').\nEs mas robusto con pocos datos y mas interpretable, pero mas lento de calcular en muestras grandes.",
            ha="center", fontsize=7.9, color="#333", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/kendall.png", dpi=130); plt.close(fig)


# ---------- 4) CRAMER'S V: para CATEGORIAS (tabla de contingencia) ----------
def cramer_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.2)); ax.axis("off")
    ax.set_title("CRAMER'S V: asociacion entre CATEGORIAS (no numeros)", fontsize=11, fontweight="bold", color=ROJO)
    ax.text(0.5, 0.88, "Para variables sin orden numerico: color, ciudad, si/no, tipo de producto.", ha="center", fontsize=8.8, color="#333", transform=ax.transAxes)
    # tabla de contingencia simple
    cols = ["Compra: SI", "Compra: NO"]
    rows = ["Region Norte", "Region Sur"]
    data = [[80, 20], [30, 70]]
    x0, y0, w, h = 0.28, 0.30, 0.20, 0.14
    for j, c in enumerate(cols):
        ax.text(x0 + 0.10 + j * w, y0 + 2 * h + 0.03, c, ha="center", fontsize=8, fontweight="bold", transform=ax.transAxes)
    for i, r in enumerate(rows):
        ax.text(x0 - 0.02, y0 + (1 - i) * h + h / 2, r, ha="right", va="center", fontsize=8, fontweight="bold", transform=ax.transAxes)
        for j in range(2):
            ax.add_patch(plt.Rectangle((x0 + j * w, y0 + (1 - i) * h), w, h, fc="#eef4fb", ec=AZUL, lw=1.2, transform=ax.transAxes))
            ax.text(x0 + j * w + w / 2, y0 + (1 - i) * h + h / 2, str(data[i][j]), ha="center", va="center", fontsize=9, transform=ax.transAxes)
    ax.text(0.5, 0.20, "Cuenta cuantos caen en cada combinacion de categorias (tabla de contingencia).\nCramer's V (0 a 1) resume que tan asociadas estan: aqui la region SI influye en la compra.",
            ha="center", fontsize=7.9, color=ROJO, transform=ax.transAxes)
    ax.text(0.5, 0.05, "Util para: ¿el genero se asocia con la preferencia de producto? ¿la ciudad con el tipo de plan?",
            ha="center", fontsize=7.9, color="#333", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/cramer.png", dpi=130); plt.close(fig)


# ---------- 5) Cuadro de decision: que usar segun tus datos ----------
def decision_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.4)); ax.axis("off")
    ax.set_title("¿Cual usar? Decide segun TUS datos", fontsize=12, fontweight="bold", color="#0f2a3f")
    filas = [
        ("¿Son numeros continuos y la relacion parece RECTA?", "PEARSON", AZUL),
        ("¿Numeros, pero la relacion sube/baja en CURVA (monotona)? muestra grande", "SPEARMAN", GREEN),
        ("¿Rankings/ordinales o MUESTRA PEQUENA?", "KENDALL'S TAU", AMBAR),
        ("¿Variables CATEGORICAS (sin orden numerico)?", "CRAMER'S V", ROJO),
    ]
    y = 0.76
    for cond, sol, color in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.075), 0.94, 0.12, fc=color, alpha=0.10, ec=color, lw=1.4, transform=ax.transAxes))
        ax.text(0.05, y, cond, fontsize=8.6, color="#333", va="center", transform=ax.transAxes)
        ax.text(0.95, y, sol, fontsize=9.6, fontweight="bold", color=color, va="center", ha="right", transform=ax.transAxes)
        y -= 0.175
    ax.text(0.5, 0.03, "Logica: primero mira el TIPO de dato (numerico vs categorico), luego la FORMA (recta vs monotona), luego el TAMANO de muestra.",
            ha="center", fontsize=8.3, color="#0f2a3f", fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/decision.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    pearson_plot(); spearman_plot(); kendall_plot(); cramer_plot(); decision_plot()
    print(">> 5 graficas profundas de correlacion escritas en study/img_corr2/", flush=True)
