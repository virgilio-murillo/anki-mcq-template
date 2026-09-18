#!/usr/bin/env python3
"""Genera las 4 visualizaciones de la carta MLA (Data Wrangler - visualizacion).
Cada figura ilustra que muestra la tecnica y por que SOLO el scatter plot
responde 'relacion entre DOS variables + outliers'.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
OUT = "study/img"
import os
os.makedirs(OUT, exist_ok=True)

GREEN = "#2e7d32"
GRIS = "#90a4ae"
AZUL = "#1565c0"
AMBAR = "#f9a825"
ROJO = "#c62828"


# ---------- A) SCATTER PLOT (la correcta) ----------
def scatter():
    n = 120
    x = rng.normal(50, 12, n)              # variable 1 (eje x): p.ej. gasto
    y = 2.1 * x + rng.normal(0, 15, n)     # variable 2 (eje y): sube junto con x
    # inyectar 3 outliers claros
    ox = np.array([20, 85, 30]); oy = np.array([190, 30, 10])
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    ax.scatter(x, y, s=38, c=GREEN, alpha=0.65, edgecolors="white", linewidths=0.5, label="cada punto = un par (x, y)")
    ax.scatter(ox, oy, s=140, facecolors="none", edgecolors=ROJO, linewidths=2.2, label="outliers (atipicos)")
    # linea de tendencia
    m, b = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, m * xs + b, "--", color=AZUL, lw=1.8, label="tendencia (suben juntas)")
    ax.set_title("A) Scatter plot  — RELACION entre DOS variables + outliers", fontsize=12, fontweight="bold", color=GREEN)
    ax.set_xlabel("Variable 1  (eje X)")
    ax.set_ylabel("Variable 2  (eje Y)")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/a_scatter.png", dpi=130); plt.close(fig)


# ---------- C) HISTOGRAMA (distribucion de UNA variable) ----------
def histograma():
    data = rng.normal(50, 12, 2000)
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    ax.hist(data, bins=25, color=GRIS, edgecolor="white")
    ax.set_title("C) Histograma  — distribucion de UNA sola variable (en bins)", fontsize=12, fontweight="bold", color="#455a64")
    ax.set_xlabel("Valor de UNA variable")
    ax.set_ylabel("Frecuencia (conteo por intervalo)")
    ax.text(0.02, 0.95, "No muestra relacion entre dos variables\nni outliers de pares", transform=ax.transAxes,
            fontsize=8.5, va="top", color=ROJO, bbox=dict(boxstyle="round", fc="#fff3f3", ec=ROJO, alpha=0.8))
    ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/c_histograma.png", dpi=130); plt.close(fig)


# ---------- D) MULTICOLINEALIDAD (matriz de correlacion entre VARIAS variables) ----------
def multicolinealidad():
    labels = ["gasto", "ingreso", "edad", "visitas", "compras"]
    k = len(labels)
    base = rng.normal(size=(300, k))
    base[:, 1] = 0.9 * base[:, 0] + 0.2 * rng.normal(size=300)  # ingreso ~ gasto (redundantes)
    base[:, 4] = 0.8 * base[:, 3] + 0.3 * rng.normal(size=300)  # compras ~ visitas
    corr = np.corrcoef(base, rowvar=False)
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(k)); ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=9)
    ax.set_yticks(range(k)); ax.set_yticklabels(labels, fontsize=9)
    for i in range(k):
        for j in range(k):
            ax.text(j, i, f"{corr[i,j]:.2f}", ha="center", va="center",
                    color="white" if abs(corr[i, j]) > 0.5 else "black", fontsize=8)
    ax.set_title("D) Multicolinealidad — redundancia lineal entre VARIAS variables", fontsize=11.5, fontweight="bold", color="#455a64")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="correlacion")
    ax.text(0.5, -0.32, "Cuantifica redundancia global, NO visualiza pares individuales ni outliers",
            transform=ax.transAxes, ha="center", fontsize=8.5, color=ROJO)
    fig.tight_layout(); fig.savefig(f"{OUT}/d_multicol.png", dpi=130); plt.close(fig)


# ---------- B) VALORES SHAPLEY (contribucion de features a UNA prediccion) ----------
def shapley():
    feats = ["ingreso", "antiguedad", "n_reclamos", "uso_mensual", "region"]
    vals = np.array([0.32, 0.18, -0.25, 0.09, -0.05])  # aportes a la prediccion
    order = np.argsort(np.abs(vals))
    feats = [feats[i] for i in order]; vals = vals[order]
    colors = [GREEN if v >= 0 else ROJO for v in vals]
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    ax.barh(feats, vals, color=colors, alpha=0.85)
    ax.axvline(0, color="#333", lw=1)
    ax.set_title("B) Valores Shapley — cuanto aporta cada feature a UNA prediccion", fontsize=11.5, fontweight="bold", color="#455a64")
    ax.set_xlabel("Contribucion a la prediccion (+ sube, - baja)")
    ax.text(0.5, -0.22, "Explica el MODELO, no la correlacion entre dos variables ni outliers",
            transform=ax.transAxes, ha="center", fontsize=8.5, color=ROJO)
    ax.grid(alpha=0.25, axis="x")
    fig.tight_layout(); fig.savefig(f"{OUT}/b_shapley.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    scatter(); histograma(); multicolinealidad(); shapley()
    print(">> 4 graficas escritas en study/img/", flush=True)
