#!/usr/bin/env python3
"""Graficas: metricas de clasificacion binaria desde la matriz de confusion.
Explica de donde sale Precision/Recall/Accuracy/F1, por que AUC-ROC NO es de
umbral fijo, y que R-cuadrado/Perplexity son de otros problemas.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_clf"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- 1) La matriz de confusion (Passed/Failed) ----------
def matriz_plot():
    TP, FP, FN, TN = 45, 8, 7, 40
    fig, ax = plt.subplots(figsize=(6.4, 4.8)); ax.axis("off")
    ax.set_title("La matriz de confusion (a un umbral FIJO)", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    cells = [
        (0.30, 0.55, "TP = 45\n(Passed real,\npredicho Passed)", GREEN, "#e6f4ea"),
        (0.58, 0.55, "FP = 8\n(Failed real,\npredicho Passed)", ROJO, "#fdecec"),
        (0.30, 0.25, "FN = 7\n(Passed real,\npredicho Failed)", AMBAR, "#fff8e1"),
        (0.58, 0.25, "TN = 40\n(Failed real,\npredicho Failed)", AZUL, "#eef4fb"),
    ]
    for x, y, t, c, fc in cells:
        ax.add_patch(plt.Rectangle((x, y), 0.28, 0.30, fc=fc, ec=c, lw=2, transform=ax.transAxes))
        ax.text(x + 0.14, y + 0.15, t, ha="center", va="center", fontsize=8.4, color=c, fontweight="bold", transform=ax.transAxes)
    ax.text(0.44, 0.90, "PREDICHO", ha="center", fontsize=9.5, fontweight="bold", transform=ax.transAxes)
    ax.text(0.44, 0.86, "Passed        Failed", ha="center", fontsize=8.5, transform=ax.transAxes)
    ax.text(0.22, 0.70, "Passed", ha="center", va="center", rotation=90, fontsize=8.5, transform=ax.transAxes)
    ax.text(0.22, 0.40, "Failed", ha="center", va="center", rotation=90, fontsize=8.5, transform=ax.transAxes)
    ax.text(0.12, 0.55, "REAL", ha="center", va="center", rotation=90, fontsize=9.5, fontweight="bold", transform=ax.transAxes)
    ax.text(0.5, 0.10, "Clasificacion binaria = 4 conteos. Precision/Recall/Accuracy/F1 se calculan de estos 4 numeros.",
            ha="center", fontsize=8.6, color="#0f2a3f", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#eef4fb", ec=AZUL, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/matriz.png", dpi=130); plt.close(fig)


# ---------- 2) De donde sale cada metrica ----------
def formulas_plot():
    fig, ax = plt.subplots(figsize=(6.4, 4.8)); ax.axis("off")
    ax.set_title("El cuarteto correcto sale de la matriz (umbral fijo)", fontsize=12, fontweight="bold", color=GREEN)
    filas = [
        ("Precision", "TP / (TP + FP)", "de lo que marque Passed, cuanto acerte"),
        ("Recall", "TP / (TP + FN)", "de los Passed reales, cuantos atrape"),
        ("Accuracy", "(TP + TN) / total", "aciertos totales sobre todo"),
        ("F1 Score", "media armonica(Precision, Recall)", "balance entre precision y recall"),
    ]
    y = 0.78
    for nombre, formula, idea in filas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.075), 0.94, 0.135, fc=GREEN, alpha=0.09, ec=GREEN, lw=1.3, transform=ax.transAxes))
        ax.text(0.06, y + 0.028, f"{nombre}", fontsize=10, fontweight="bold", color=GREEN, va="center", transform=ax.transAxes)
        ax.text(0.06, y - 0.022, f"= {formula}", fontsize=8.8, color="#1b4d24", family="monospace", va="center", transform=ax.transAxes)
        ax.text(0.62, y, idea, fontsize=8.0, color="#37424c", va="center", transform=ax.transAxes)
        y -= 0.185
    ax.text(0.5, 0.02, "Las 4 son operaciones directas sobre TP/FP/TN/FN a UN umbral fijo.",
            ha="center", fontsize=8.6, color=GREEN, fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/formulas.png", dpi=130); plt.close(fig)


# ---------- 3) Por que AUC-ROC NO es de umbral fijo ----------
def auc_plot():
    thr = np.linspace(0, 1, 100)
    tpr = thr ** 0.35
    fpr = thr ** 1.6
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.plot(fpr, tpr, color=MORADO, lw=2.2, label="curva ROC (todos los umbrales)")
    ax.plot([0, 1], [0, 1], "--", color="#bbb")
    ax.fill_between(fpr, tpr, fpr, color=MORADO, alpha=0.12, label="AUC = area bajo la curva")
    # marcar UN umbral fijo (un punto)
    ax.scatter([0.16], [0.62], s=120, color=GREEN, zorder=5, label="UN umbral fijo = 1 punto\n(de aqui salen Precision/Recall/...)")
    ax.set_title("AUC-ROC barre TODOS los umbrales (por eso NO es del cuarteto)", fontsize=11, fontweight="bold", color=MORADO)
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
    ax.legend(fontsize=8, loc="lower right")
    ax.text(0.03, 0.92, "Precision/Recall/Accuracy/F1 = UN punto (umbral fijo).\nAUC-ROC = TODA la curva (todos los umbrales).",
            transform=ax.transAxes, fontsize=8.4, color=MORADO, va="top",
            bbox=dict(boxstyle="round", fc="#f3e5f5", ec=MORADO, alpha=0.85))
    ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/auc.png", dpi=130); plt.close(fig)


# ---------- 4) Que metrica pertenece a que problema (descartar distractores) ----------
def mapa_plot():
    fig, ax = plt.subplots(figsize=(6.4, 4.6)); ax.axis("off")
    ax.set_title("A que problema pertenece cada metrica (descartar distractores)", fontsize=11.5, fontweight="bold", color="#0f2a3f")
    grupos = [
        ("CLASIFICACION\n(umbral fijo, matriz de confusion)", "Precision, Recall, Accuracy, F1, Especificidad", GREEN),
        ("CLASIFICACION\n(barre umbrales)", "AUC-ROC  (valida, pero NO de umbral fijo)", MORADO),
        ("REGRESION\n(valor continuo)", "R-cuadrado, RMSE, MAE, MAPE", ROJO),
        ("LENGUAJE / NLP\n(generacion de texto)", "Perplexity, BLEU, ROUGE", AMBAR),
    ]
    y = 0.76
    for prob, mets, color in grupos:
        ax.add_patch(plt.Rectangle((0.03, y - 0.085), 0.42, 0.14, fc=color, alpha=0.12, ec=color, lw=1.5, transform=ax.transAxes))
        ax.text(0.24, y, prob, ha="center", va="center", fontsize=8.4, fontweight="bold", color=color, transform=ax.transAxes)
        ax.annotate("", xy=(0.55, y), xytext=(0.46, y), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color=color, lw=1.6))
        ax.text(0.57, y, mets, ha="left", va="center", fontsize=8.2, color="#263238", transform=ax.transAxes)
        y -= 0.19
    ax.text(0.5, 0.02, "Distractores: R-cuadrado (regresion), Perplexity (NLP), AUC-ROC (barre umbrales) -> fuera del cuarteto.",
            ha="center", fontsize=8.2, color=ROJO, transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/mapa.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    matriz_plot(); formulas_plot(); auc_plot(); mapa_plot()
    print(">> 4 graficas de clasificacion escritas en study/img_clf/", flush=True)
