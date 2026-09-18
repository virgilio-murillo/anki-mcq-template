#!/usr/bin/env python3
"""Explica el PROBLEMA que resuelve cada una de las otras metricas de sesgo:
CI, TVD, KL. Con ejemplos concretos de que sale mal si NO las revisas.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_why"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- CI: el problema de la representacion ----------
def ci_plot():
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    ax.bar(["Grupo A", "Grupo B"], [900, 100], color=[AZUL, "#90caf9"], alpha=0.9, width=0.5)
    ax.text(0, 910, "900 ejemplos", ha="center", fontsize=10, fontweight="bold")
    ax.text(1, 110, "100 ejemplos", ha="center", fontsize=10, fontweight="bold")
    ax.set_ylabel("cuantos ejemplos hay en el dataset")
    ax.set_title("CI (Class Imbalance) — el problema de la REPRESENTACION", fontsize=11.5, fontweight="bold", color=AZUL)
    ax.text(0.5, -0.22, "Problema: el modelo casi no ve al Grupo B (solo 10%). Aprende bien a A y MAL a B\n-> predice peor para el grupo poco representado. CI lo detecta antes de entrenar.",
            transform=ax.transAxes, ha="center", fontsize=8.5, color=ROJO)
    ax.grid(alpha=0.2, axis="y")
    fig.tight_layout(); fig.savefig(f"{OUT}/ci_why.png", dpi=130); plt.close(fig)


# ---------- TVD / KL: el problema de que las distribuciones difieran ----------
def dist_plot():
    import numpy as np
    x = np.linspace(0, 100, 200)
    # distribucion de 'score de credito' por grupo, con formas distintas
    gA = np.exp(-0.5 * ((x - 65) / 12) ** 2)
    gB = np.exp(-0.5 * ((x - 45) / 18) ** 2)
    gA /= gA.sum(); gB /= gB.sum()
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(x, gA, color=GREEN, lw=2, label="Grupo A (distribucion)")
    ax.plot(x, gB, color=ROJO, lw=2, label="Grupo B (distribucion)")
    ax.fill_between(x, gA, gB, where=(gA > gB), color=GREEN, alpha=0.12)
    ax.fill_between(x, gA, gB, where=(gB > gA), color=ROJO, alpha=0.12)
    ax.set_title("TVD y KL — el problema de que las DISTRIBUCIONES difieran", fontsize=11, fontweight="bold", color=MORADO)
    ax.set_xlabel("distribucion completa de resultados/scores por grupo"); ax.set_yticks([])
    ax.legend(fontsize=8.5)
    ax.text(0.5, -0.22, "No solo importa el promedio: la FORMA completa de la distribucion puede diferir.\nTVD/KL miden cuanto se separan las curvas enteras (no solo la proporcion de positivos).",
            transform=ax.transAxes, ha="center", fontsize=8.3, color=MORADO)
    fig.tight_layout(); fig.savefig(f"{OUT}/dist_why.png", dpi=130); plt.close(fig)


# ---------- Resumen: que problema resuelve cada una ----------
def resumen_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.6)); ax.axis("off")
    ax.set_title("¿Que problema resuelve cada metrica de sesgo?", fontsize=12, fontweight="bold", color="#0f2a3f")
    filas = [
        ("DPL", "diferencia de proporcion de POSITIVOS entre grupos",
         "Problema: a un grupo se le dan mas resultados favorables (aprobado, contratado).\nEl modelo copiaria ese favoritismo.", GREEN),
        ("CI", "REPRESENTACION (cuantos ejemplos hay de cada grupo)",
         "Problema: un grupo esta sub-representado; el modelo aprende poco de el\ny predice peor para ese grupo.", AZUL),
        ("TVD", "DISTANCIA acotada/simetrica entre las distribuciones",
         "Problema: la distribucion COMPLETA de resultados difiere entre grupos,\nno solo el promedio. TVD lo cuantifica de forma acotada.", AMBAR),
        ("KL", "DIVERGENCIA general (no acotada) entre distribuciones",
         "Problema: mismo caso (distribuciones distintas), pero medido como\ndivergencia relativa; util para comparar formas de distribucion.", ROJO),
    ]
    y = 0.80
    for sigla, que, prob, color in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.075), 0.94, 0.155, fc=color, alpha=0.10, ec=color, lw=1.4, transform=ax.transAxes))
        ax.text(0.06, y + 0.04, f"{sigla}  -  mide: {que}", fontsize=8.8, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.06, y - 0.028, prob, fontsize=7.7, color="#37424c", va="center", transform=ax.transAxes)
        y -= 0.195
    ax.text(0.5, 0.01, "Todas responden lo mismo de fondo: '¿los datos tratan distinto a un grupo?' desde angulos distintos.",
            ha="center", fontsize=8.4, color="#0f2a3f", fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/resumen_metricas.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    ci_plot(); dist_plot(); resumen_plot()
    print(">> 3 graficas extra (CI/TVD/KL) escritas en study/img_why/", flush=True)
