#!/usr/bin/env python3
"""Graficas: Gateway endpoint vs Interface endpoint (VPC endpoints / PrivateLink).
Explica el mecanismo de cada uno, cuando usar cual, por que existen dos, y el caso
cross-region de la carta.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUT = "study/img_vpc"
os.makedirs(OUT, exist_ok=True)
GREEN = "#2e7d32"; AZUL = "#1565c0"; ROJO = "#c62828"; AMBAR = "#f9a825"; GRIS = "#607d8b"; MORADO = "#6a1b9a"


def _box(ax, x, y, w, h, text, color, fc, fs=8.6):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=color, lw=1.8, transform=ax.transAxes))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color, fontweight="bold", transform=ax.transAxes)


def _arrow(ax, x1, y1, x2, y2, color="#555", label="", ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), transform=ax.transAxes,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.8, linestyle=ls))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.03, label, fontsize=7.8, color=color, ha="center", transform=ax.transAxes)


# ---------- 1) Gateway endpoint: como funciona ----------
def gateway_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.4)); ax.axis("off")
    ax.set_title("GATEWAY endpoint — una ENTRADA en la tabla de rutas", fontsize=12, fontweight="bold", color=AZUL)
    _box(ax, 0.05, 0.55, 0.34, 0.30, "VPC (us-east-1)\n\nEC2 / SageMaker", GRIS, "#eceff1", 9)
    _box(ax, 0.10, 0.40, 0.24, 0.10, "Tabla de rutas\n(ruta -> S3)", AZUL, "#eef4fb", 8.2)
    _box(ax, 0.62, 0.55, 0.33, 0.30, "Amazon S3\n(MISMA region)\nus-east-1", GREEN, "#e6f4ea", 9)
    _arrow(ax, 0.34, 0.45, 0.62, 0.62, AZUL, "por la RUTA")
    ax.text(0.5, 0.28, "Es un objetivo de ruteo: agregas una ruta en la route table y el trafico a S3/DynamoDB\nde ESA region va por AWS, no por internet. Gratis. NO usa IP privada ni ENI.",
            ha="center", fontsize=8.6, color="#333", transform=ax.transAxes)
    ax.text(0.5, 0.10, "Solo S3 y DynamoDB · solo dentro de la MISMA region · solo para recursos de ESA VPC",
            ha="center", fontsize=8.8, color=ROJO, fontweight="bold", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#fdecec", ec=ROJO, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/gateway.png", dpi=130); plt.close(fig)


# ---------- 2) Interface endpoint: como funciona ----------
def interface_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.4)); ax.axis("off")
    ax.set_title("INTERFACE endpoint (PrivateLink) — una ENI con IP privada", fontsize=11.5, fontweight="bold", color=MORADO)
    _box(ax, 0.05, 0.55, 0.34, 0.30, "VPC\n\nEC2 / SageMaker", GRIS, "#eceff1", 9)
    _box(ax, 0.16, 0.40, 0.16, 0.10, "ENI\n(IP privada)", MORADO, "#f3e5f5", 8)
    _box(ax, 0.62, 0.55, 0.33, 0.30, "Servicio AWS\n(S3, SageMaker,\nKMS, ECR, ...)", GREEN, "#e6f4ea", 8.6)
    _arrow(ax, 0.32, 0.45, 0.62, 0.62, MORADO, "via PrivateLink")
    ax.text(0.5, 0.28, "Crea una interfaz de red (ENI) con IP PRIVADA dentro de tu subred. El trafico entra por\nesa IP y viaja por PrivateLink. Tiene un costo por hora + por datos.",
            ha="center", fontsize=8.6, color="#333", transform=ax.transAxes)
    ax.text(0.5, 0.10, "Muchos servicios AWS · admite acceso desde ON-PREM y desde OTRA VPC/region (via peering/TGW)",
            ha="center", fontsize=8.8, color=GREEN, fontweight="bold", transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.85))
    fig.tight_layout(); fig.savefig(f"{OUT}/interface.png", dpi=130); plt.close(fig)


# ---------- 3) Tabla comparativa ----------
def compare_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.6)); ax.axis("off")
    ax.set_title("Gateway  vs  Interface  (por que existen dos)", fontsize=12.5, fontweight="bold", color="#0f2a3f")
    ax.text(0.32, 0.90, "GATEWAY endpoint", ha="center", fontsize=10.5, fontweight="bold", color=AZUL, transform=ax.transAxes)
    ax.text(0.74, 0.90, "INTERFACE endpoint", ha="center", fontsize=10.5, fontweight="bold", color=MORADO, transform=ax.transAxes)
    filas = [
        ("Mecanismo", "entrada en tabla de rutas", "ENI con IP privada (PrivateLink)"),
        ("Servicios", "SOLO S3 y DynamoDB", "muchos (S3, SageMaker, KMS,\nECR, SM runtime, etc.)"),
        ("Alcance", "misma region, misma VPC", "on-prem, otra VPC, otra region\n(via peering / Transit Gateway)"),
        ("Costo", "gratis", "por hora + por datos"),
        ("Da IP privada", "no", "si (una ENI en tu subred)"),
    ]
    y = 0.78; dy = 0.145
    for label, g, i in filas:
        ax.text(0.02, y, label, fontsize=9.3, fontweight="bold", color="#333", va="center", transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((0.17, y - 0.055), 0.30, 0.11, fc="#eef4fb", ec=AZUL, alpha=0.7, transform=ax.transAxes))
        ax.text(0.32, y, g, ha="center", va="center", fontsize=8.0, color="#0d3a66", transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((0.58, y - 0.055), 0.33, 0.11, fc="#f3e5f5", ec=MORADO, alpha=0.7, transform=ax.transAxes))
        ax.text(0.745, y, i, ha="center", va="center", fontsize=8.0, color="#4a148c", transform=ax.transAxes)
        y -= dy
    fig.tight_layout(); fig.savefig(f"{OUT}/compare.png", dpi=130); plt.close(fig)


# ---------- 4) Cuando elegir cual + el caso de la carta ----------
def decision_plot():
    fig, ax = plt.subplots(figsize=(6.8, 4.6)); ax.axis("off")
    ax.set_title("¿Cual elegir? y por que esta carta necesita INTERFACE", fontsize=12, fontweight="bold", color="#0f2a3f")
    ax.text(0.5, 0.88, "Regla simple: por defecto GATEWAY para S3/DynamoDB (gratis, simple).\nUsa INTERFACE cuando el gateway NO alcanza.", ha="center", fontsize=9.2, color="#333", transform=ax.transAxes)
    casos = [
        ("Solo S3/DynamoDB, misma VPC, misma region", "GATEWAY (gratis, por ruta)", AZUL),
        ("Necesitas otro servicio (KMS, ECR, SageMaker runtime...)", "INTERFACE (gateway no lo soporta)", MORADO),
        ("Acceso desde ON-PREM o desde OTRA VPC", "INTERFACE (gateway es solo intra-VPC)", MORADO),
        ("Bucket en OTRA region que tu VPC  <-- ESTA CARTA", "INTERFACE + peering/TGW (gateway es intra-region)", GREEN),
    ]
    y = 0.68
    for cond, sol, color in casos:
        ax.add_patch(plt.Rectangle((0.03, y - 0.075), 0.94, 0.10, fc=color, alpha=0.10, ec=color, lw=1.3, transform=ax.transAxes))
        ax.text(0.05, y, cond, fontsize=8.7, color="#333", va="center", transform=ax.transAxes)
        ax.text(0.95, y, sol, fontsize=8.5, fontweight="bold", color=color, va="center", ha="right", transform=ax.transAxes)
        y -= 0.135
    ax.text(0.5, 0.05, "Carta: VPC en us-west-2, bucket S3 en us-east-1 (otra region) -> gateway (intra-region) NO llega -> INTERFACE",
            ha="center", fontsize=8.4, fontweight="bold", color=GREEN, transform=ax.transAxes,
            bbox=dict(boxstyle="round", fc="#e6f4ea", ec=GREEN, alpha=0.9))
    fig.tight_layout(); fig.savefig(f"{OUT}/decision.png", dpi=130); plt.close(fig)


if __name__ == "__main__":
    gateway_plot(); interface_plot(); compare_plot(); decision_plot()
    print(">> 4 graficas VPC endpoints escritas en study/img_vpc/", flush=True)
