#!/usr/bin/env python3
"""Graficas: Precision vs Recall (y por que los distractores son Recall/Accuracy/FPR).
Se apoya en la misma matriz de confusion para mostrar de que conjunto es cada fraccion.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

OUT = "study/img_prec"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"

TP, FP, FN, TN = 45, 8, 7, 40


def _matriz(ax, highlight):
    """Dibuja la matriz 2x2 y resalta las celdas de 'highlight' (dict celda->color)."""
    celdas = {
        "TP": (0.30, 0.52, f"TP = {TP}"),
        "FP": (0.58, 0.52, f"FP = {FP}"),
        "FN": (0.30, 0.24, f"FN = {FN}"),
        "TN": (0.58, 0.24, f"TN = {TN}"),
    }
    for k, (x, y, t) in celdas.items():
        fc = highlight.get(k, "#f5f5f5"); ec = "#999"; lw = 1.4; tc = "#555"
        if k in highlight:
            ec = {"num": AZUL, "den": AMBAR}.get(highlight[k + "_role"], "#333")
            lw = 2.4; tc = "#222"
        ax.add_patch(Rectangle((x, y), 0.28, 0.28, fc=fc, ec=ec, lw=lw, transform=ax.transAxes))
        ax.text(x + 0.14, y + 0.14, t, ha="center", va="center", fontsize=9, fontweight="bold", color=tc, transform=ax.transAxes)
    ax.text(0.44, 0.86, "PREDICHO:   Passed        Failed", ha="center", fontsize=8, transform=ax.transAxes)
    ax.text(0.18, 0.66, "REAL\nPassed", ha="center", va="center", fontsize=7.5, transform=ax.transAxes)
    ax.text(0.18, 0.38, "REAL\nFailed", ha="center", va="center", fontsize=7.5, transform=ax.transAxes)
    ax.axis("off")


# ---------- 1) Precision: fraccion de la COLUMNA 'predije positivo' ----------
def precision_plot():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    hl = {"TP": "#c8e6c9", "TP_role": "num", "FP": "#ffe0b2", "FP_role": "den"}
    _matriz(ax, hl)
    ax.set_title("PRECISION = TP / (TP + FP)", fontsize=13, fontweight="bold", color=GREEN)
    # marcar la columna 'predije Passed'
    ax.add_patch(Rectangle((0.29, 0.23), 0.30, 0.58, fc="none", ec=MORADO, lw=2.5, ls="--", transform=ax.transAxes))
    ax.text(0.44, 0.08, "Miras SOLO lo que el modelo predijo Passed (columna izquierda).\nDe eso, ¿cuanto era correcto? = TP / (TP + FP)",
            ha="center", fontsize=8.5, color=MORADO, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#f3e5f5", ec=MORADO, alpha=0.85))
    ax.text(0.95, 0.5, f"= {TP}/({TP}+{FP})\n= {TP/(TP+FP):.2f}", fontsize=11, fontweight="bold", color=GREEN, va="center", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/precision.png", dpi=130); plt.close(fig)


# ---------- 2) Recall: fraccion de la FILA 'realmente positivo' ----------
def recall_plot():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    hl = {"TP": "#c8e6c9", "TP_role": "num", "FN": "#ffe0b2", "FN_role": "den"}
    _matriz(ax, hl)
    ax.set_title("RECALL = TP / (TP + FN)", fontsize=13, fontweight="bold", color=AZUL)
    # marcar la fila 'real Passed'
    ax.add_patch(Rectangle((0.29, 0.51), 0.58, 0.30, fc="none", ec=MORADO, lw=2.5, ls="--", transform=ax.transAxes))
    ax.text(0.44, 0.08, "Miras SOLO lo que REALMENTE era Passed (fila de arriba).\nDe eso, ¿cuanto atrapaste? = TP / (TP + FN)",
            ha="center", fontsize=8.5, color=MORADO, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#f3e5f5", ec=MORADO, alpha=0.85))
    ax.text(0.95, 0.5, f"= {TP}/({TP}+{FN})\n= {TP/(TP+FN):.2f}", fontsize=11, fontweight="bold", color=AZUL, va="center", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/recall.png", dpi=130); plt.close(fig)


# ---------- 3) Comparacion directa: mismo numerador, distinto denominador ----------
def compara_plot():
    fig, ax = plt.subplots(figsize=(6.6, 4.2)); ax.axis("off")
    ax.set_title("Misma TP arriba, distinto conjunto abajo", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    ax.text(0.28, 0.72, "PRECISION", ha="center", fontsize=12, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.28, 0.55, "TP\n----------------\nTP + FP", ha="center", fontsize=11, family="monospace", color="#333", transform=ax.transAxes)
    ax.text(0.28, 0.33, "'de lo que MARQUE\npositivo, cuanto acerte'", ha="center", fontsize=9, color=GREEN, transform=ax.transAxes)
    ax.text(0.72, 0.72, "RECALL", ha="center", fontsize=12, fontweight="bold", color=AZUL, transform=ax.transAxes)
    ax.text(0.72, 0.55, "TP\n----------------\nTP + FN", ha="center", fontsize=11, family="monospace", color="#333", transform=ax.transAxes)
    ax.text(0.72, 0.33, "'de lo que ERA\npositivo, cuanto atrape'", ha="center", fontsize=9, color=AZUL, transform=ax.transAxes)
    ax.axvline(0.5, ymin=0.15, ymax=0.85, color="#ccc", lw=1)
    ax.text(0.5, 0.10, "Precision se equivoca por FALSOS POSITIVOS (FP). Recall se equivoca por FALSOS NEGATIVOS (FN).",
            ha="center", fontsize=8.8, color="#0f2a3f", fontweight="bold", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#eef4fb", ec=AZUL, alpha=0.8))
    fig.tight_layout(); fig.savefig(f"{OUT}/compara.png", dpi=130); plt.close(fig)


# ---------- 4) Cuando importa cada una + que son los distractores ----------
def cuando_plot():
    fig, ax = plt.subplots(figsize=(6.6, 4.6)); ax.axis("off")
    ax.set_title("Cuando importa cada una · y que son los distractores", fontsize=11.5, fontweight="bold", color="#0f2a3f")
    filas = [
        ("Precision alta importa cuando...", "un FALSO POSITIVO es costoso\n(ej. frenado innecesario en conduccion autonoma)", GREEN),
        ("Recall alto importa cuando...", "perder un POSITIVO real es grave\n(fraude, diagnostico de enfermedad)", AZUL),
        ("(A) 'positivos reales detectados'", "= RECALL / sensibilidad, NO Precision", GRIS),
        ("(B) 'aciertos sobre el total'", "= ACCURACY, NO Precision", GRIS),
        ("(C) 'negativos marcados como positivos'", "= FALSE POSITIVE RATE, NO Precision", GRIS),
    ]
    y = 0.80
    for izq, der, color in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.06), 0.94, 0.10, fc=color, alpha=0.10, ec=color, lw=1.2, transform=ax.transAxes))
        ax.text(0.05, y, izq, fontsize=8.8, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.55, y, der, fontsize=8.2, color="#37424c", va="center", transform=ax.transAxes)
        y -= 0.155
    ax.text(0.5, 0.03, "Respuesta D = Precision = TP/(TP+FP) = 'de lo que predije positivo, cuanto acerte'.",
            ha="center", fontsize=8.8, color=GREEN, fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/cuando.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    precision_plot(); recall_plot(); compara_plot(); cuando_plot()
    print(">> 4 graficas de precision/recall escritas en study/img_prec/", flush=True)
