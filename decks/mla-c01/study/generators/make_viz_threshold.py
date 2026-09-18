#!/usr/bin/env python3
"""Explica el concepto de UMBRAL (threshold) y por que AUC-ROC no es de umbral fijo.
Pensado para alguien que no tiene claro que es el umbral.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_thr"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"

rng = np.random.default_rng(3)
# probabilidades que da el modelo: los Failed suelen tener prob baja, los Passed prob alta (con solape)
prob_failed = np.clip(rng.normal(0.35, 0.16, 60), 0, 1)   # clase real = Failed
prob_passed = np.clip(rng.normal(0.68, 0.16, 60), 0, 1)   # clase real = Passed


# ---------- 1) Que es el umbral: el modelo da PROBABILIDADES, tu cortas ----------
def umbral_plot():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.scatter(prob_failed, rng.uniform(0.55, 0.95, len(prob_failed)), s=30, color=ROJO, alpha=0.6, label="imagenes que SON Failed")
    ax.scatter(prob_passed, rng.uniform(0.05, 0.45, len(prob_passed)), s=30, color=GREEN, alpha=0.6, label="imagenes que SON Passed")
    ax.axvline(0.5, color=AZUL, lw=2.5, label="UMBRAL = 0.5 (linea de corte)")
    ax.text(0.5, 1.02, "UMBRAL", ha="center", color=AZUL, fontweight="bold", fontsize=10, transform=ax.get_xaxis_transform())
    ax.annotate("prob < 0.5\n-> el modelo dice FAILED", (0.18, 0.5), fontsize=8.5, color=ROJO, ha="center")
    ax.annotate("prob >= 0.5\n-> el modelo dice PASSED", (0.82, 0.5), fontsize=8.5, color=GREEN, ha="center")
    ax.set_xlim(0, 1); ax.set_yticks([])
    ax.set_xlabel("probabilidad que da el modelo de que sea 'Passed'")
    ax.set_title("El UMBRAL: el modelo no dice Passed/Failed, da una PROBABILIDAD", fontsize=11.5, fontweight="bold", color=AZUL)
    ax.legend(fontsize=8, loc="upper center", ncol=1)
    ax.text(0.5, -0.22, "Para decidir la etiqueta, cortas en un numero (aqui 0.5). Ese corte ES el umbral.",
            transform=ax.transAxes, ha="center", fontsize=9, color="#333")
    fig.tight_layout(); fig.savefig(f"{OUT}/umbral.png", dpi=130); plt.close(fig)


# ---------- 2) Mover el umbral cambia los conteos (y por tanto las metricas) ----------
def mover_plot():
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 3.2))
    for ax, thr, titulo in zip(axes, [0.3, 0.5, 0.8], ["Umbral BAJO (0.3)", "Umbral MEDIO (0.5)", "Umbral ALTO (0.8)"]):
        # contar TP/FP con este umbral
        pred_passed_ok = np.sum(prob_passed >= thr)      # TP
        pred_passed_bad = np.sum(prob_failed >= thr)     # FP
        ax.scatter(prob_failed, rng.uniform(0.55, 0.95, len(prob_failed)), s=14, color=ROJO, alpha=0.5)
        ax.scatter(prob_passed, rng.uniform(0.05, 0.45, len(prob_passed)), s=14, color=GREEN, alpha=0.5)
        ax.axvline(thr, color=AZUL, lw=2)
        ax.set_xlim(0, 1); ax.set_yticks([]); ax.set_xticks([0, 0.5, 1])
        ax.set_title(titulo, fontsize=9.5, fontweight="bold", color=AZUL)
        ax.text(0.5, -0.28, f"marca Passed:\nTP={pred_passed_ok}  FP={pred_passed_bad}", transform=ax.transAxes,
                ha="center", fontsize=8, color="#333")
    fig.suptitle("Mover el umbral cambia TP/FP -> cambia Precision, Recall, Accuracy, F1", fontsize=11, fontweight="bold", color="#0f2a3f")
    fig.tight_layout(rect=[0, 0.05, 1, 0.93]); fig.savefig(f"{OUT}/mover.png", dpi=130); plt.close(fig)


# ---------- 3) Cada umbral = un punto de la curva ROC ----------
def curva_plot():
    thrs = np.linspace(0, 1, 41)
    tprs, fprs = [], []
    P = len(prob_passed); N = len(prob_failed)
    for t in thrs:
        tp = np.sum(prob_passed >= t); fp = np.sum(prob_failed >= t)
        tprs.append(tp / P); fprs.append(fp / N)
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.plot(fprs, tprs, "-", color=MORADO, lw=2, label="curva ROC = union de TODOS los umbrales")
    # marcar 3 umbrales concretos como puntos
    for t, c, lbl in [(0.3, AMBAR, "umbral 0.3"), (0.5, AZUL, "umbral 0.5"), (0.8, GREEN, "umbral 0.8")]:
        tp = np.sum(prob_passed >= t) / P; fp = np.sum(prob_failed >= t) / N
        ax.scatter([fp], [tp], s=110, color=c, zorder=5, label=f"{lbl}  (UN punto)")
    ax.plot([0, 1], [0, 1], "--", color="#ccc")
    ax.fill_between(fprs, tprs, 0, color=MORADO, alpha=0.10, label="AUC = area bajo la curva")
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate (Recall)")
    ax.set_title("Cada UMBRAL es UN punto. AUC-ROC es TODA la curva.", fontsize=11.5, fontweight="bold", color=MORADO)
    ax.legend(fontsize=7.8, loc="lower right")
    ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/curva.png", dpi=130); plt.close(fig)


# ---------- 4) Resumen: foto vs pelicula ----------
def resumen_plot():
    fig, ax = plt.subplots(figsize=(6.6, 3.8)); ax.axis("off")
    ax.set_title("La idea en una frase", fontsize=13, fontweight="bold", color="#0f2a3f")
    ax.add_patch(plt.Rectangle((0.04, 0.45), 0.44, 0.38, fc="#e6f4ea", ec=GREEN, lw=1.8, transform=ax.transAxes))
    ax.text(0.26, 0.72, "Precision / Recall\nAccuracy / F1", ha="center", fontsize=11, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.26, 0.55, "= UNA FOTO\n(fijas 1 umbral, cuentas)", ha="center", fontsize=9, color="#1b4d24", transform=ax.transAxes)
    ax.add_patch(plt.Rectangle((0.52, 0.45), 0.44, 0.38, fc="#f3e5f5", ec=MORADO, lw=1.8, transform=ax.transAxes))
    ax.text(0.74, 0.72, "AUC-ROC", ha="center", fontsize=11, fontweight="bold", color=MORADO, transform=ax.transAxes)
    ax.text(0.74, 0.55, "= TODA LA PELICULA\n(recorre todos los umbrales)", ha="center", fontsize=9, color="#4a148c", transform=ax.transAxes)
    ax.text(0.5, 0.28, "La pregunta pide metricas 'a un umbral FIJO' = una foto.\nPor eso AUC-ROC (toda la pelicula) NO entra en el cuarteto.",
            ha="center", fontsize=9.5, color=ROJO, fontweight="bold", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/resumen.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    umbral_plot(); mover_plot(); curva_plot(); resumen_plot()
    print(">> 4 graficas de umbral escritas en study/img_thr/", flush=True)
