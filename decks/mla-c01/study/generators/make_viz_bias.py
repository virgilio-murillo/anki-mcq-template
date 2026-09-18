#!/usr/bin/env python3
"""Graficas: metricas de sesgo pre-entrenamiento de SageMaker Clarify.
Foco en DPL (diferencia de proporcion de positivos entre grupos) y como distinguir
CI / DPL / TVD / KL por su palabra clave.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_bias"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- 1) DPL: proporcion de positivos por grupo (barras) ----------
def dpl_plot():
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    grupos = ["Grupo A", "Grupo B", "Grupo C"]
    prop_pos = [0.68, 0.41, 0.55]   # proporcion de resultados positivos por grupo
    bars = ax.bar(grupos, prop_pos, color=[GREEN, ROJO, AMBAR], alpha=0.85, width=0.55)
    for b, p in zip(bars, prop_pos):
        ax.text(b.get_x() + b.get_width() / 2, p + 0.02, f"{p:.0%}", ha="center", fontsize=11, fontweight="bold")
    ax.axhline(np.mean(prop_pos), ls="--", color=GRIS, label=f"promedio ({np.mean(prop_pos):.0%})")
    # marcar la diferencia entre el mayor y el menor
    ax.annotate("", xy=(0, 0.68), xytext=(0, 0.41), arrowprops=dict(arrowstyle="<->", color=MORADO, lw=2))
    ax.text(0.15, 0.545, "DPL\n= diferencia de\nproporciones", color=MORADO, fontsize=9, fontweight="bold")
    ax.set_ylim(0, 0.85); ax.set_ylabel("proporcion de resultados POSITIVOS")
    ax.set_title("DPL — diferencia en la PROPORCION de positivos entre grupos", fontsize=11.5, fontweight="bold", color=MORADO)
    ax.legend(fontsize=8, loc="upper right")
    ax.text(0.5, -0.18, "Si un grupo recibe muchos mas 'positivos' que otro -> DPL alta -> posible favoritismo/sesgo.",
            transform=ax.transAxes, ha="center", fontsize=8.6, color=MORADO)
    ax.grid(alpha=0.2, axis="y")
    fig.tight_layout(); fig.savefig(f"{OUT}/dpl.png", dpi=130); plt.close(fig)


# ---------- 2) Las 4 metricas de Clarify, cada una con SU pregunta ----------
def cuatro_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.8)); ax.axis("off")
    ax.set_title("Las 4 metricas de sesgo pre-entrenamiento (Clarify)", fontsize=12, fontweight="bold", color="#0f2a3f")
    filas = [
        ("DPL", "Difference in Proportions of Labels", "¿Un grupo recibe mas ETIQUETAS POSITIVAS que otro?", GREEN, "SI (esta carta)"),
        ("CI", "Class Imbalance", "¿Un grupo esta sobre/sub-REPRESENTADO en el dataset?", AZUL, "no"),
        ("TVD", "Total Variation Distance", "¿Cual es la DISTANCIA (acotada/simetrica) entre dos distribuciones?", AMBAR, "no"),
        ("KL", "Kullback-Leibler Divergence", "¿Cual es la DIVERGENCIA general (no acotada) entre dos distribuciones?", ROJO, "no"),
    ]
    y = 0.80
    for sigla, nombre, pregunta, color, ok in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.075), 0.94, 0.14, fc=color, alpha=0.10, ec=color, lw=1.4, transform=ax.transAxes))
        ax.text(0.06, y + 0.03, f"{sigla}  -  {nombre}", fontsize=9.4, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.06, y - 0.028, pregunta, fontsize=8.2, color="#37424c", va="center", transform=ax.transAxes)
        ax.text(0.95, y, ok, fontsize=8.6, fontweight="bold", color=color, va="center", ha="right", transform=ax.transAxes)
        y -= 0.185
    fig.tight_layout(); fig.savefig(f"{OUT}/cuatro.png", dpi=130); plt.close(fig)


# ---------- 3) DPL vs CI: no confundir 'resultados' con 'representacion' ----------
def dpl_vs_ci_plot():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.8))
    # DPL: mismo tamano de grupo, distinta tasa de positivos
    ax = axes[0]
    ax.bar(["A", "B"], [50, 50], color="#cfd8dc", label="tamano del grupo (igual)")
    ax.bar(["A", "B"], [34, 20], color=[GREEN, ROJO], alpha=0.9, label="positivos")
    ax.set_title("DPL mira los RESULTADOS", fontsize=10, fontweight="bold", color=MORADO)
    ax.text(0.5, -0.22, "grupos del mismo tamano,\npero A recibe mas positivos", transform=ax.transAxes, ha="center", fontsize=8, color=MORADO)
    ax.legend(fontsize=7, loc="upper right")
    # CI: distinto tamano de grupo (representacion)
    ax = axes[1]
    ax.bar(["A", "B"], [80, 20], color=[AZUL, "#90caf9"], alpha=0.9)
    ax.set_title("CI mira la REPRESENTACION", fontsize=10, fontweight="bold", color=AZUL)
    ax.text(0.5, -0.22, "un grupo es mucho mas grande\nque el otro en el dataset", transform=ax.transAxes, ha="center", fontsize=8, color=AZUL)
    fig.suptitle("DPL (proporcion de positivos)  vs  CI (tamano/representacion del grupo)", fontsize=10.5, fontweight="bold", color="#0f2a3f")
    fig.tight_layout(rect=[0, 0.05, 1, 0.92]); fig.savefig(f"{OUT}/dpl_vs_ci.png", dpi=130); plt.close(fig)


# ---------- 4) Regla por palabra clave ----------
def regla_plot():
    fig, ax = plt.subplots(figsize=(6.8, 3.6)); ax.axis("off")
    ax.set_title("Reconoce la metrica por la PALABRA CLAVE del enunciado", fontsize=11.5, fontweight="bold", color="#0f2a3f")
    reglas = [
        ("'proporcion de positivos / etiquetas entre grupos'", "-> DPL", GREEN),
        ("'representacion / imbalance / un grupo mas grande'", "-> CI", AZUL),
        ("'distancia acotada [0,1] y simetrica entre distribuciones'", "-> TVD", AMBAR),
        ("'divergencia general (no acotada) entre distribuciones'", "-> KL", ROJO),
    ]
    y = 0.78
    for cond, sol, color in reglas:
        ax.text(0.04, y, cond, fontsize=8.8, color="#333", va="center", transform=ax.transAxes)
        ax.text(0.82, y, sol, fontsize=10, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        y -= 0.19
    ax.text(0.5, 0.03, "Esta carta dice 'proporcion de resultados positivos entre grupos raciales' -> DPL.",
            ha="center", fontsize=8.8, color=GREEN, fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/regla.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    dpl_plot(); cuatro_plot(); dpl_vs_ci_plot(); regla_plot()
    print(">> 4 graficas de metricas de sesgo escritas en study/img_bias/", flush=True)
