#!/usr/bin/env python3
"""Graficas para la carta MLA: metricas de forecasting de series de tiempo.
Ilustra: (1) que es un forecast continuo con RMSE, (2) que mide Average wQL
(bandas de cuantiles), y (3) por que las metricas de clasificacion no aplican.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

rng = np.random.default_rng(11)
OUT = "study/img_fc"
os.makedirs(OUT, exist_ok=True)

GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"


# ---------- 1) RMSE sobre un forecast de serie de tiempo ----------
def rmse_plot():
    t = np.arange(48)
    real = 22 + 6 * np.sin(t / 6) + rng.normal(0, 0.6, len(t))     # temperatura real
    pred = 22 + 6 * np.sin(t / 6) + rng.normal(0, 1.4, len(t))     # pronostico
    err = real - pred
    rmse = np.sqrt(np.mean(err ** 2))
    fig, ax = plt.subplots(figsize=(6.4, 4.5))
    ax.plot(t, real, "-o", ms=3, color=GREEN, lw=1.8, label="valor real (continuo)")
    ax.plot(t, pred, "-o", ms=3, color=AZUL, lw=1.6, label="pronostico del modelo")
    # dibujar algunos errores como lineas verticales
    for i in range(0, len(t), 4):
        ax.plot([t[i], t[i]], [real[i], pred[i]], color=ROJO, lw=1.2, alpha=0.7)
    ax.set_title(f"RMSE — error de un forecast CONTINUO  (RMSE = {rmse:.2f})", fontsize=12, fontweight="bold", color=GREEN)
    ax.set_xlabel("tiempo (horas)"); ax.set_ylabel("temperatura (continua)")
    ax.text(0.02, 0.03, "Las lineas rojas = errores (real - pred).\nRMSE penaliza MAS los errores grandes (los eleva al cuadrado).",
            transform=ax.transAxes, fontsize=8.5, color=ROJO,
            bbox=dict(boxstyle="round", fc="#fff3f3", ec=ROJO, alpha=0.85))
    ax.legend(fontsize=9, loc="upper right"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/rmse.png", dpi=130); plt.close(fig)


# ---------- 2) Average wQL: pronostico probabilistico (bandas de cuantiles) ----------
def wql_plot():
    t = np.arange(48)
    center = 60 + 15 * np.sin(t / 7)                 # humedad esperada (mediana p50)
    real = center + rng.normal(0, 5, len(t))
    p10 = center - 12; p50 = center; p90 = center + 12
    fig, ax = plt.subplots(figsize=(6.4, 4.5))
    ax.fill_between(t, p10, p90, color=AZUL, alpha=0.18, label="banda p10-p90 (incertidumbre)")
    ax.plot(t, p50, "-", color=AZUL, lw=1.8, label="pronostico mediano (p50)")
    ax.plot(t, p90, "--", color=AMBAR, lw=1.3, label="cuantil p90")
    ax.plot(t, p10, "--", color=GRIS, lw=1.3, label="cuantil p10")
    ax.scatter(t, real, s=16, color=GREEN, zorder=5, label="valor real observado")
    ax.set_title("Average wQL — calidad de un pronostico PROBABILISTICO (cuantiles)", fontsize=11.5, fontweight="bold", color=AZUL)
    ax.set_xlabel("tiempo (horas)"); ax.set_ylabel("humedad (continua)")
    ax.text(0.02, 0.03, "wQL mide que tan bien calibrados estan los CUANTILES\n(ej. el p90 debe quedar por encima del real ~90% del tiempo).",
            transform=ax.transAxes, fontsize=8.5, color=AZUL,
            bbox=dict(boxstyle="round", fc="#eef4fb", ec=AZUL, alpha=0.85))
    ax.legend(fontsize=8, loc="upper right"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/wql.png", dpi=130); plt.close(fig)


# ---------- 3) Por que NO clasificacion: ROC (mide separacion de CLASES, no valores continuos) ----------
def roc_plot():
    fpr = np.linspace(0, 1, 100)
    tpr = fpr ** 0.35   # curva ROC de un clasificador
    fig, ax = plt.subplots(figsize=(6.4, 4.5))
    ax.plot(fpr, tpr, color=GRIS, lw=2, label="curva ROC (clasificacion)")
    ax.plot([0, 1], [0, 1], "--", color="#bbb", label="azar")
    ax.fill_between(fpr, tpr, fpr, color=GRIS, alpha=0.12)
    ax.set_title("AUC-ROC / F1 / Log loss — SOLO para CLASIFICACION (no aplican)", fontsize=11.5, fontweight="bold", color=ROJO)
    ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate")
    ax.text(0.30, 0.10, "Estas metricas necesitan CLASES (spam/no-spam,\nfraude/no-fraude). Un forecast de temperatura\nno tiene clases: son valores CONTINUOS.",
            fontsize=8.6, color=ROJO, bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.9))
    ax.legend(fontsize=9, loc="lower right"); ax.grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(f"{OUT}/roc.png", dpi=130); plt.close(fig)


# ---------- 4) Mapa: que metrica para que tarea ----------
def map_plot():
    fig, ax = plt.subplots(figsize=(6.4, 4.5)); ax.axis("off")
    ax.set_title("Chuleta: que metrica para que tarea", fontsize=13, fontweight="bold", color="#0f2a3f")
    rows = [
        ("REGRESION\n(valores continuos)", "RMSE, MAE, MAPE", GREEN, 0.72),
        ("PRONOSTICO\nPROBABILISTICO", "Average wQL (cuantiles)", AZUL, 0.50),
        ("CLASIFICACION\n(clases discretas)", "Accuracy, Precision,\nRecall, F1, AUC-ROC, Log loss", ROJO, 0.22),
    ]
    for label, metrics, color, y in rows:
        ax.add_patch(plt.Rectangle((0.03, y - 0.09), 0.40, 0.18, fc=color, alpha=0.15, ec=color, lw=1.6, transform=ax.transAxes))
        ax.text(0.23, y, label, ha="center", va="center", fontsize=10, fontweight="bold", color=color, transform=ax.transAxes)
        ax.annotate("", xy=(0.55, y), xytext=(0.44, y), transform=ax.transAxes,
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.8))
        ax.text(0.57, y, metrics, ha="left", va="center", fontsize=9.5, color="#263238", transform=ax.transAxes)
    ax.text(0.5, 0.02, "Esta carta = temperatura+humedad continuas con incertidumbre  ->  RMSE + Average wQL",
            ha="center", fontsize=9, fontweight="bold", color=GREEN, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.9))
    fig.tight_layout(); fig.savefig(f"{OUT}/mapa.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    rmse_plot(); wql_plot(); roc_plot(); map_plot()
    print(">> 4 graficas de forecasting escritas en study/img_fc/", flush=True)
