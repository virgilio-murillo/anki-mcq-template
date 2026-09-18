#!/usr/bin/env python3
"""Explica el PROBLEMA que resuelve DPL: por que importa que un grupo tenga mas
positivos. Ejemplo: aprobacion de prestamos y propagacion del sesgo al modelo.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_why"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


# ---------- 1) El ejemplo concreto: aprobacion de prestamos ----------
def ejemplo_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    grupos = ["Grupo A", "Grupo B"]
    aprob = [0.70, 0.35]  # tasa de aprobacion historica
    bars = ax.bar(grupos, aprob, color=[GREEN, ROJO], alpha=0.85, width=0.5)
    for b, p in zip(bars, aprob):
        ax.text(b.get_x() + b.get_width()/2, p + 0.02, f"{p:.0%} aprobados", ha="center", fontsize=11, fontweight="bold")
    ax.annotate("", xy=(0, 0.70), xytext=(0, 0.35), arrowprops=dict(arrowstyle="<->", color=MORADO, lw=2.2))
    ax.text(0.12, 0.52, "DPL = 35 puntos\nde diferencia", color=MORADO, fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, 0.85); ax.set_ylabel("tasa de prestamos APROBADOS (positivos)")
    ax.set_title("Ejemplo: datos historicos de aprobacion de prestamos", fontsize=12, fontweight="bold", color="#0f2a3f")
    ax.text(0.5, -0.18, "En los datos con que vas a entrenar, al Grupo A se le aprobaron muchos mas prestamos que al B.",
            transform=ax.transAxes, ha="center", fontsize=8.8, color="#333")
    ax.grid(alpha=0.2, axis="y")
    fig.tight_layout(); fig.savefig(f"{OUT}/ejemplo.png", dpi=130); plt.close(fig)


# ---------- 2) El problema: el modelo APRENDE y perpetua el sesgo ----------
def propaga_plot():
    fig, ax = plt.subplots(figsize=(7.2, 3.8)); ax.axis("off")
    ax.set_title("El problema: el modelo aprende del pasado y lo REPITE", fontsize=12, fontweight="bold", color=ROJO)

    def box(x, y, w, h, text, color, fc, fs=8.4):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=color, lw=1.8, transform=ax.transAxes))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=color, fontweight="bold", transform=ax.transAxes)

    def arrow(x1, y1, x2, y2, color, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), transform=ax.transAxes, arrowprops=dict(arrowstyle="->", color=color, lw=2))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.05, label, fontsize=7.6, color=color, ha="center", transform=ax.transAxes)

    box(0.02, 0.45, 0.22, 0.30, "Datos historicos\nSESGADOS\n(A aprobado 70%,\nB 35%)", ROJO, "#fdecec", 7.8)
    box(0.30, 0.45, 0.20, 0.30, "Entrenas el\nmodelo con\nesos datos", GRIS, "#eceff1")
    box(0.56, 0.45, 0.20, 0.30, "El modelo\nAPRENDE\n'A si, B no'", AMBAR, "#fff8e1")
    box(0.80, 0.45, 0.18, 0.30, "Nuevas decisiones\ninjustas\n(y quiza ilegales)", ROJO, "#fdecec", 7.8)
    arrow(0.24, 0.60, 0.30, 0.60, GRIS)
    arrow(0.50, 0.60, 0.56, 0.60, AMBAR)
    arrow(0.76, 0.60, 0.80, 0.60, ROJO)
    ax.text(0.5, 0.22, "El modelo no 'inventa' el sesgo: lo COPIA de los datos. Si no lo detectas antes, lo automatizas a escala.",
            ha="center", fontsize=8.8, color=ROJO, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/propaga.png", dpi=130); plt.close(fig)


# ---------- 3) OJO: DPL alta NO siempre es problema ----------
def matiz_plot():
    fig, ax = plt.subplots(figsize=(7.2, 4.2)); ax.axis("off")
    ax.set_title("Importante: DPL alta = SENAL para investigar, no condena automatica", fontsize=11, fontweight="bold", color="#0f2a3f")
    ax.add_patch(plt.Rectangle((0.03, 0.52), 0.45, 0.34, fc="#fdecec", ec=ROJO, lw=1.8, transform=ax.transAxes))
    ax.text(0.255, 0.80, "DPL alta = PROBLEMA cuando...", ha="center", fontsize=9.5, fontweight="bold", color=ROJO, transform=ax.transAxes)
    ax.text(0.255, 0.63, "la diferencia se explica por un\natributo protegido (raza, genero)\nsin razon legitima = discriminacion", ha="center", fontsize=8.2, color="#8a1c1c", transform=ax.transAxes)
    ax.add_patch(plt.Rectangle((0.52, 0.52), 0.45, 0.34, fc="#e6f4ea", ec=GREEN, lw=1.8, transform=ax.transAxes))
    ax.text(0.745, 0.80, "DPL alta puede ser OK cuando...", ha="center", fontsize=9.5, fontweight="bold", color=GREEN, transform=ax.transAxes)
    ax.text(0.745, 0.63, "la diferencia se explica por un\nfactor legitimo y relevante\n(ej. ingresos reales distintos)", ha="center", fontsize=8.2, color="#1b4d24", transform=ax.transAxes)
    ax.text(0.5, 0.36, "DPL no dice 'esto es injusto'. Dice 'aqui hay una diferencia grande entre grupos: investiga por que'.",
            ha="center", fontsize=9, color="#0f2a3f", fontweight="bold", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#eef4fb", ec=AZUL, alpha=0.85))
    ax.text(0.5, 0.14, "Por eso es una metrica PRE-entrenamiento: la revisas ANTES de entrenar, para decidir si corriges los datos.",
            ha="center", fontsize=8.4, color="#333", transform=ax.transAxes)
    fig.tight_layout(); fig.savefig(f"{OUT}/matiz.png", dpi=130); plt.close(fig)


# ---------- 4) Que haces al detectar DPL alta ----------
def accion_plot():
    fig, ax = plt.subplots(figsize=(7.2, 3.6)); ax.axis("off")
    ax.set_title("¿Que haces si DPL revela un sesgo problematico?", fontsize=12, fontweight="bold", color="#0f2a3f")
    pasos = [
        ("1. Detectar", "Clarify calcula DPL ANTES de entrenar y te avisa de la brecha entre grupos.", AZUL),
        ("2. Investigar", "¿La diferencia es legitima (factor real) o es sesgo por atributo protegido?", AMBAR),
        ("3. Corregir", "Si es sesgo: re-balancear/re-muestrear datos, quitar features problematicas, recolectar mas datos del grupo sub-representado.", GREEN),
        ("4. Re-verificar", "Vuelves a medir DPL y monitoreas en produccion (bias drift) para que no reaparezca.", MORADO),
    ]
    y = 0.74
    for titulo, det, color in pasos:
        ax.add_patch(plt.Rectangle((0.03, y - 0.065), 0.94, 0.11, fc=color, alpha=0.10, ec=color, lw=1.3, transform=ax.transAxes))
        ax.text(0.05, y + 0.02, titulo, fontsize=9.2, fontweight="bold", color=color, va="center", transform=ax.transAxes)
        ax.text(0.05, y - 0.028, det, fontsize=8.0, color="#37424c", va="center", transform=ax.transAxes)
        y -= 0.165
    fig.tight_layout(); fig.savefig(f"{OUT}/accion.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    ejemplo_plot(); propaga_plot(); matiz_plot(); accion_plot()
    print(">> 4 graficas 'por que importa DPL' escritas en study/img_why/", flush=True)
