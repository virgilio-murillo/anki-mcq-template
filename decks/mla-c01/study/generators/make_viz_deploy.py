#!/usr/bin/env python3
"""Graficas para la carta MLA: despliegue de modelo con trafico intermitente.
Explica por que D (serverless SIN provisioned) gana a A (serverless CON provisioned)
y a la idea de 'comprar provisioned solo en horas pico'.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_dep"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"

# Perfil de trafico de una semana (168 h). Picos en horario laboral L-V 9-18, casi nulo noche/finde.
horas = np.arange(168)
trafico = np.zeros(168)
for d in range(7):
    for h in range(24):
        idx = d * 24 + h
        if d < 5 and 9 <= h < 18:      # L-V horario laboral
            trafico[idx] = 60 + 25 * np.sin((h - 9) / 9 * np.pi)
        elif d < 5 and (7 <= h < 9 or 18 <= h < 21):
            trafico[idx] = 12
        else:
            trafico[idx] = np.random.default_rng(h + d).uniform(0, 3)


def trafico_plot():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.fill_between(horas, trafico, color=AZUL, alpha=0.3)
    ax.plot(horas, trafico, color=AZUL, lw=1.2)
    for d in range(7):
        ax.axvline(d * 24, color="#ddd", lw=0.8)
    ax.set_xticks([d * 24 + 12 for d in range(7)])
    ax.set_xticklabels(["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"])
    ax.set_title("El trafico real: picos L-V 9-18, casi nulo de noche y fin de semana", fontsize=11.5, fontweight="bold", color=AZUL)
    ax.set_ylabel("peticiones/min")
    ax.text(0.5, 0.9, "Mucho tiempo OCIOSO (noches + fines de semana = ~65% de las horas)",
            transform=ax.transAxes, ha="center", fontsize=9, color=ROJO,
            bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.85))
    ax.grid(alpha=0.2)
    fig.tight_layout(); fig.savefig(f"{OUT}/trafico.png", dpi=130); plt.close(fig)


def costo_plot():
    """Costo acumulado en la semana por opcion (ilustrativo)."""
    # costo por hora aproximado por opcion:
    # C real-time auto-scaling: instancia SIEMPRE encendida (min 1) -> costo fijo alto + extra en picos
    c_realtime = 1.0 + 0.006 * trafico
    # A serverless CON provisioned: reserva SIEMPRE lista -> costo base medio-alto todo el tiempo + uso
    c_prov = 0.55 + 0.004 * trafico
    # D serverless SIN provisioned: SOLO paga por uso -> ~0 en reposo, sube en picos
    c_serv = 0.004 * trafico + 0.002 * (trafico > 0)
    # tu idea: provisioned SOLO en horas pico (requiere automatizacion extra) -> base solo L-V 9-18
    c_prov_horario = np.where(trafico > 15, 0.55 + 0.004 * trafico, 0.004 * trafico)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(horas, np.cumsum(c_realtime), color=ROJO, lw=2, label="C) Real-time auto-scaling (siempre encendido)")
    ax.plot(horas, np.cumsum(c_prov), color=AMBAR, lw=2, label="A) Serverless CON Provisioned (reserva 24/7)")
    ax.plot(horas, np.cumsum(c_prov_horario), color=MORADO, lw=2, ls="--", label="Tu idea: Provisioned SOLO en picos (+ automatizacion)")
    ax.plot(horas, np.cumsum(c_serv), color=GREEN, lw=2.6, label="D) Serverless SIN Provisioned (pagas por uso)")
    ax.set_title("Costo ACUMULADO en una semana (ilustrativo)", fontsize=12, fontweight="bold", color=GREEN)
    ax.set_xlabel("horas de la semana"); ax.set_ylabel("costo acumulado (relativo)")
    ax.legend(fontsize=8.2, loc="upper left")
    ax.grid(alpha=0.25)
    ax.text(0.98, 0.05, "D es el mas barato porque en reposo (noches/finde) cuesta ~0.",
            transform=ax.transAxes, ha="right", fontsize=9, color=GREEN,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/costo.png", dpi=130); plt.close(fig)


def provisioned_plot():
    """Por que 'comprar provisioned por horario' NO es la respuesta del examen."""
    fig, ax = plt.subplots(figsize=(7.2, 4.4)); ax.axis("off")
    ax.set_title("Tu idea: '¿y comprar Provisioned solo en horas pico?'", fontsize=12.5, fontweight="bold", color=MORADO)
    ax.text(0.5, 0.86, "Es una idea razonable en la vida real, PERO no es lo que pide el examen. Por que:",
            ha="center", fontsize=10, color="#333", transform=ax.transAxes)
    puntos = [
        ("Provisioned Concurrency NO es un 'horario que compras'",
         "Es capacidad RESERVADA que se factura de forma continua mientras esta configurada. No hay un\n'encender de 9 a 18 y apagar' nativo simple.", ROJO),
        ("Para hacerlo por horario necesitas AUTOMATIZACION extra",
         "EventBridge Scheduler + scripts que suban/bajen la Provisioned Concurrency cada dia. Eso es MAS\ncomplejidad operativa: ya no es 'escala solo y barato en reposo' de fabrica.", AMBAR),
        ("El enunciado pide 'escalar SOLO' y 'barato en reposo'",
         "Serverless SIN Provisioned (D) ya hace ambas cosas sin que tu configures nada: escala solo y en\nreposo cuesta ~0. Cumple el requisito con la solucion mas simple.", GREEN),
        ("El unico costo de D es el cold start",
         "En trafico intermitente, tolerar un arranque en frio ocasional es aceptable a cambio de no pagar\nreserva. Provisioned (A) solo se justifica si NO puedes tolerar cold starts (latencia critica).", AZUL),
    ]
    y = 0.70
    for titulo, det, color in puntos:
        ax.add_patch(plt.Rectangle((0.03, y - 0.11), 0.94, 0.145, fc=color, alpha=0.10, ec=color, lw=1.4, transform=ax.transAxes))
        ax.text(0.05, y, titulo, fontsize=9.6, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.05, y - 0.06, det, fontsize=8.3, color="#37424c", va="center", transform=ax.transAxes)
        y -= 0.175
    fig.tight_layout(); fig.savefig(f"{OUT}/provisioned.png", dpi=130); plt.close(fig)


def decision_plot():
    fig, ax = plt.subplots(figsize=(7.2, 4.4)); ax.axis("off")
    ax.set_title("Arbol de decision: que despliegue de SageMaker elegir", fontsize=12.5, fontweight="bold", color="#0f2a3f")

    def node(x, y, w, h, text, color, fc, fs=8.6):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=color, lw=1.7, transform=ax.transAxes))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color, fontweight="bold", transform=ax.transAxes)

    def arrow(x1, y1, x2, y2, label="", color="#555"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color=color, lw=1.6))
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.02, label, fontsize=8, color=color, ha="center", transform=ax.transAxes)

    node(0.34, 0.85, 0.32, 0.12, "Trafico\n¿constante o intermitente?", "#0f2a3f", "#eceff1")
    node(0.02, 0.60, 0.30, 0.12, "CONSTANTE / alto\n-> Real-time endpoint\n(+ auto-scaling)", ROJO, "#fdecec")
    arrow(0.40, 0.85, 0.17, 0.72, "constante", ROJO)
    node(0.66, 0.60, 0.32, 0.12, "INTERMITENTE / ocioso\n-> Serverless Inference", GREEN, "#e6f4ea")
    arrow(0.58, 0.85, 0.82, 0.72, "intermitente", GREEN)

    node(0.50, 0.32, 0.46, 0.12, "¿Toleras cold starts?", "#0f2a3f", "#eceff1")
    arrow(0.82, 0.60, 0.73, 0.44)
    node(0.30, 0.08, 0.30, 0.13, "SI (barato en reposo)\n-> D) Serverless\nSIN Provisioned", GREEN, "#e6f4ea", 8.4)
    arrow(0.62, 0.32, 0.45, 0.21, "si", GREEN)
    node(0.66, 0.08, 0.31, 0.13, "NO (latencia critica)\n-> A) Serverless\nCON Provisioned", AMBAR, "#fff8e1", 8.4)
    arrow(0.80, 0.32, 0.82, 0.21, "no", AMBAR)

    ax.text(0.5, 0.005, "Esta carta: intermitente + 'barato en reposo' + tolera cold start  ->  D",
            ha="center", fontsize=9, fontweight="bold", color=GREEN, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.9))
    fig.tight_layout(); fig.savefig(f"{OUT}/decision.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    trafico_plot(); costo_plot(); provisioned_plot(); decision_plot()
    print(">> 4 graficas de despliegue escritas en study/img_dep/", flush=True)
