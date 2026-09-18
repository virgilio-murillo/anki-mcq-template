#!/usr/bin/env python3
"""Graficas: correlacion no lineal (monotona) -> Spearman.
Explica lineal vs monotona, como Spearman usa rangos, y cuando cada coeficiente.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_corr"
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(5)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- 1) Lineal vs monotona-no-lineal vs no-monotona ----------
def tipos_plot():
    fig, axes = plt.subplots(1, 3, figsize=(7.8, 3.2))
    x = np.linspace(1, 10, 40)
    # lineal
    y1 = 2 * x + rng.normal(0, 1.5, len(x))
    axes[0].scatter(x, y1, s=18, color=AZUL, alpha=0.7)
    axes[0].set_title("LINEAL\n(recta)", fontsize=9.5, fontweight="bold", color=AZUL)
    axes[0].text(0.5, -0.28, "Pearson alto y Spearman alto", transform=axes[0].transAxes, ha="center", fontsize=7.6, color="#333")
    # monotona no lineal (curva que solo sube)
    y2 = np.exp(x / 3) + rng.normal(0, 2, len(x))
    axes[1].scatter(x, y2, s=18, color=GREEN, alpha=0.7)
    axes[1].set_title("MONOTONA no lineal\n(sube siempre, curva)", fontsize=9.5, fontweight="bold", color=GREEN)
    axes[1].text(0.5, -0.28, "Pearson BAJA, Spearman ALTO", transform=axes[1].transAxes, ha="center", fontsize=7.6, color=GREEN, fontweight="bold")
    # no monotona (sube y baja)
    y3 = -(x - 5.5) ** 2 + rng.normal(0, 2, len(x))
    axes[2].scatter(x, y3, s=18, color=ROJO, alpha=0.7)
    axes[2].set_title("NO monotona\n(sube y baja)", fontsize=9.5, fontweight="bold", color=ROJO)
    axes[2].text(0.5, -0.28, "Pearson y Spearman bajos", transform=axes[2].transAxes, ha="center", fontsize=7.6, color="#333")
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("Tres tipos de relacion (la carta pide la del MEDIO: monotona no lineal)", fontsize=10.5, fontweight="bold", color="#0f2a3f")
    fig.tight_layout(rect=[0, 0.04, 1, 0.90]); fig.savefig(f"{OUT}/tipos.png", dpi=130); plt.close(fig)


# ---------- 2) Por que Spearman capta lo monotono: usa RANGOS ----------
def rangos_plot():
    x = np.linspace(1, 10, 12)
    y = np.exp(x / 3)  # monotona no lineal
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.6))
    # izquierda: valores crudos (curva)
    axes[0].scatter(x, y, s=40, color=GREEN)
    axes[0].plot(x, y, color=GREEN, alpha=0.4)
    axes[0].set_title("Valores crudos: es una CURVA", fontsize=9.5, fontweight="bold", color=GREEN)
    axes[0].set_xlabel("X"); axes[0].set_ylabel("Y")
    # derecha: rangos (se vuelve recta)
    rx = np.argsort(np.argsort(x)) + 1
    ry = np.argsort(np.argsort(y)) + 1
    axes[1].scatter(rx, ry, s=40, color=MORADO)
    axes[1].plot(rx, ry, color=MORADO, alpha=0.5, ls="--")
    axes[1].set_title("Con RANGOS (posiciones): es una RECTA", fontsize=9.5, fontweight="bold", color=MORADO)
    axes[1].set_xlabel("rango de X"); axes[1].set_ylabel("rango de Y")
    fig.suptitle("El truco de Spearman: convierte los valores en RANGOS (1o, 2o, 3o...)", fontsize=10.5, fontweight="bold", color="#0f2a3f")
    fig.text(0.5, 0.01, "Si al ordenar, cuando X sube Y tambien sube -> los rangos forman una recta -> Spearman ~ 1 (aunque los valores sean curvos).",
             ha="center", fontsize=7.8, color="#333")
    fig.tight_layout(rect=[0, 0.06, 1, 0.90]); fig.savefig(f"{OUT}/rangos.png", dpi=130); plt.close(fig)


# ---------- 3) Los 4 coeficientes: cuando usar cada uno ----------
def cuatro_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.6)); ax.axis("off")
    ax.set_title("Los 4 coeficientes: cuando usar cada uno", fontsize=12, fontweight="bold", color="#0f2a3f")
    filas = [
        ("Spearman", "correlacion MONOTONA (no lineal) por rangos; por DEFECTO en muestras GRANDES", GREEN, "SI (esta carta)"),
        ("Pearson", "solo relacion LINEAL (recta) entre numericas continuas", AZUL, "no"),
        ("Kendall's Tau", "tambien monotona por rangos, pero se prefiere en muestras PEQUENAS / ordinales", AMBAR, "no"),
        ("Cramer's V", "asociacion entre variables CATEGORICAS (tabla de contingencia)", ROJO, "no"),
    ]
    y = 0.80
    for sigla, det, color, ok in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.075), 0.94, 0.145, fc=color, alpha=0.10, ec=color, lw=1.4, transform=ax.transAxes))
        ax.text(0.06, y + 0.03, sigla, fontsize=9.8, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.06, y - 0.028, det, fontsize=8.0, color="#37424c", va="center", transform=ax.transAxes)
        ax.text(0.95, y, ok, fontsize=8.6, fontweight="bold", color=color, va="center", ha="right", transform=ax.transAxes)
        y -= 0.185
    fig.tight_layout(); fig.savefig(f"{OUT}/cuatro.png", dpi=130); plt.close(fig)


# ---------- 4) Spearman vs Kendall: el desempate de la carta ----------
def spearman_kendall_plot():
    fig, ax = plt.subplots(figsize=(6.8, 3.8)); ax.axis("off")
    ax.set_title("Spearman vs Kendall (ambos monotonos por rangos): el desempate", fontsize=11, fontweight="bold", color="#0f2a3f")
    ax.add_patch(plt.Rectangle((0.04, 0.45), 0.44, 0.38, fc="#e6f4ea", ec=GREEN, lw=1.8, transform=ax.transAxes))
    ax.text(0.26, 0.74, "SPEARMAN", ha="center", fontsize=11, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.26, 0.56, "el de rango POR DEFECTO\nen muestras GRANDES\n(caso de esta carta)", ha="center", fontsize=8.3, color="#1b4d24", transform=ax.transAxes)
    ax.add_patch(plt.Rectangle((0.52, 0.45), 0.44, 0.38, fc="#fff8e1", ec=AMBAR, lw=1.8, transform=ax.transAxes))
    ax.text(0.74, 0.74, "KENDALL'S TAU", ha="center", fontsize=11, fontweight="bold", color="#b26a00", transform=ax.transAxes)
    ax.text(0.74, 0.56, "alternativa para muestras\nPEQUENAS / datos ordinales", ha="center", fontsize=8.3, color="#7a4a00", transform=ax.transAxes)
    ax.text(0.5, 0.28, "La carta dice 'muestra GRANDE' + 'el mas usado por defecto' -> Spearman.\nKendall no es incorrecto conceptualmente, pero no es el de defecto para muestras grandes.",
            ha="center", fontsize=8.4, color="#0f2a3f", fontweight="bold", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#eef4fb", ec=AZUL, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/spearman_kendall.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    tipos_plot(); rangos_plot(); cuatro_plot(); spearman_kendall_plot()
    print(">> 4 graficas de correlacion escritas en study/img_corr/", flush=True)
