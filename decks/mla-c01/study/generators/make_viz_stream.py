#!/usr/bin/env python3
"""Graficas: ingesta+procesamiento de stream en tiempo real con minima operacion.
Explica por que A (Kinesis Data Streams + Managed Flink) gana a MSC autogestionado
y a las opciones por lotes.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_stream"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


def _box(ax, x, y, w, h, text, color, fc, fs=8.3):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=color, lw=1.8, transform=ax.transAxes))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color, fontweight="bold", transform=ax.transAxes)


def _arrow(ax, x1, y1, x2, y2, color="#555", label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color=color, lw=1.9))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.04, label, fontsize=7.4, color=color, ha="center", transform=ax.transAxes)


# ---------- 1) El flujo de la opcion A ----------
def flujo_plot():
    fig, ax = plt.subplots(figsize=(7.6, 3.4)); ax.axis("off")
    ax.set_title("Opcion A — pipeline de streaming en tiempo real (administrado)", fontsize=11.5, fontweight="bold", color=GREEN)
    _box(ax, 0.01, 0.42, 0.17, 0.30, "Transacciones\n(flujo continuo)", GRIS, "#eceff1")
    _box(ax, 0.21, 0.42, 0.21, 0.30, "Kinesis Data Streams\nINGESTA baja latencia", AZUL, "#eef4fb")
    _box(ax, 0.45, 0.42, 0.25, 0.30, "Managed Service for\nApache Flink\nPROCESA en vivo", GREEN, "#e6f4ea")
    _box(ax, 0.73, 0.42, 0.24, 0.30, "SageMaker\nINFERENCIA\n(deteccion de fraude)", MORADO, "#f3e5f5")
    _arrow(ax, 0.18, 0.57, 0.21, 0.57)
    _arrow(ax, 0.42, 0.57, 0.45, 0.57)
    _arrow(ax, 0.70, 0.57, 0.73, 0.57)
    ax.text(0.5, 0.22, "Ingerir (Kinesis) -> transformar/agregar en tiempo real (Flink) -> inferir (SageMaker). Todo administrado.",
            ha="center", fontsize=8.6, color=GREEN, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/flujo.png", dpi=130); plt.close(fig)


# ---------- 2) El cuadrante: tiempo real vs lotes  x  administrado vs autogestionado ----------
def cuadrante_plot():
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axhline(5, color="#bbb", lw=1); ax.axvline(5, color="#bbb", lw=1)
    ax.set_xlabel("<-- POR LOTES            TIEMPO REAL -->", fontsize=9.5)
    ax.set_ylabel("<-- AUTOGESTIONADO        ADMINISTRADO -->", fontsize=9.5)
    ax.set_title("Las dos preguntas: ¿tiempo real? y ¿minima operacion?", fontsize=11.5, fontweight="bold", color="#0f2a3f")
    # A: tiempo real + administrado (arriba-derecha) = ganador
    ax.scatter([8], [8.2], s=260, color=GREEN, zorder=5)
    ax.text(8, 9.2, "A) Kinesis + Managed Flink\nTIEMPO REAL + ADMINISTRADO", ha="center", fontsize=8.4, color=GREEN, fontweight="bold")
    # C: tiempo real + autogestionado (abajo-derecha)
    ax.scatter([8], [2], s=200, color=ROJO, zorder=5)
    ax.text(8, 1.0, "C) MSK + Flink propio\nTIEMPO REAL pero MUCHA operacion", ha="center", fontsize=8.2, color=ROJO)
    # B: lotes + administrado (arriba-izquierda)
    ax.scatter([2.2], [7], s=180, color=AMBAR, zorder=5)
    ax.text(2.2, 8.0, "B) Glue + Athena\nPOR LOTES (no tiempo real)", ha="center", fontsize=8.2, color=AMBAR)
    # D: lotes (abajo-izquierda)
    ax.scatter([2], [2.5], s=180, color=AMBAR, zorder=5)
    ax.text(2, 1.4, "D) SQS + EMR nocturno\nPOR LOTES de noche", ha="center", fontsize=8.2, color=AMBAR)
    ax.text(7.5, 5.3, "zona objetivo:\ntiempo real +\nminima operacion", fontsize=8, color=GREEN, style="italic")
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); fig.savefig(f"{OUT}/cuadrante.png", dpi=130); plt.close(fig)


# ---------- 3) Kinesis vs MSK: la diferencia de operacion ----------
def kinesis_msk_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.2)); ax.axis("off")
    ax.set_title("Kinesis Data Streams  vs  Amazon MSK (ambos son streaming)", fontsize=11.5, fontweight="bold", color="#0f2a3f")
    ax.text(0.30, 0.86, "Kinesis Data Streams", ha="center", fontsize=10.5, fontweight="bold", color=AZUL, transform=ax.transAxes)
    ax.text(0.74, 0.86, "Amazon MSK (Kafka)", ha="center", fontsize=10.5, fontweight="bold", color=ROJO, transform=ax.transAxes)
    filas = [
        ("Tiempo real", "si", "si (tambien es streaming)"),
        ("Operacion", "administrado por AWS\n(no gestionas brokers)", "TU dimensionas y operas\nbrokers y particiones"),
        ("Motor de proceso", "Managed Flink\n(sin cluster que operar)", "TU despliegas y mantienes\nFlink sobre el cluster"),
        ("Carga operativa", "BAJA (la que pide la carta)", "ALTA"),
    ]
    y = 0.72; dy = 0.16
    for label, k, m in filas:
        ax.text(0.02, y, label, fontsize=8.8, fontweight="bold", color="#333", va="center", transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((0.16, y - 0.065), 0.28, 0.13, fc="#eef4fb", ec=AZUL, alpha=0.7, transform=ax.transAxes))
        ax.text(0.30, y, k, ha="center", va="center", fontsize=7.7, color="#0d3a66", transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((0.58, y - 0.065), 0.32, 0.13, fc="#fdecec", ec=ROJO, alpha=0.7, transform=ax.transAxes))
        ax.text(0.74, y, m, ha="center", va="center", fontsize=7.7, color="#8a1c1c", transform=ax.transAxes)
        y -= dy
    ax.text(0.5, 0.02, "MSK es correcto tecnicamente, pero es la opcion de MAYOR operacion -> falla 'minima carga operativa'.",
            ha="center", fontsize=8.4, color=ROJO, fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/kinesis_msk.png", dpi=130); plt.close(fig)


# ---------- 4) Regla de decision ----------
def regla_plot():
    fig, ax = plt.subplots(figsize=(6.8, 3.6)); ax.axis("off")
    ax.set_title("Como decidir en el examen", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    reglas = [
        ("¿Es TIEMPO REAL o por lotes?", "Glue/Athena/EMR-nocturno/SQS = LOTES -> descartar (B, D)", AMBAR),
        ("Si es tiempo real: ¿minima operacion?", "Kinesis + Managed Flink = administrado -> (A)", GREEN),
        ("MSK + Flink propio", "tiempo real SI, pero TU operas todo -> mucha carga (C)", ROJO),
    ]
    y = 0.72
    for cond, sol, color in reglas:
        ax.add_patch(plt.Rectangle((0.03, y - 0.08), 0.94, 0.12, fc=color, alpha=0.10, ec=color, lw=1.3, transform=ax.transAxes))
        ax.text(0.05, y, cond, fontsize=9.2, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.97, y, sol, fontsize=8.2, color="#333", va="center", ha="right", transform=ax.transAxes)
        y -= 0.22
    ax.text(0.5, 0.04, "Tiempo real + minima operacion = Kinesis Data Streams + Managed Service for Apache Flink (A).",
            ha="center", fontsize=8.8, color=GREEN, fontweight="bold", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/regla.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    flujo_plot(); cuadrante_plot(); kinesis_msk_plot(); regla_plot()
    print(">> 4 graficas de streaming escritas en study/img_stream/", flush=True)
