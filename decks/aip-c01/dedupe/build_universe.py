#!/usr/bin/env python3
"""Entrypoint por-examen: construye el universo de dedup para ESTA carpeta.

Toda la logica vive en anki_mcq.universe (paquete instalado). Este script solo
apunta la libreria a ESTA carpeta dedupe/ y usa el allowlist compartido del repo.

Uso:
    ../../.venv/bin/python dedupe/build_universe.py [--allowlist PATH]

Requiere Anki abierto con AnkiConnect (localhost:8765). SOLO LECTURA de Anki.
Escribe unicamente archivos locales:
  dedupe/universe_cards.json, dedupe/existing_cards.json,
  dedupe/universe_conflicts.json, dedupe/universe_skipped.json (si aplica)
"""
import argparse
import pathlib

from anki_mcq.universe import build_universe

DIR = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(
        description="Construye el universo de dedup (UNION local+Anki, solo lectura).")
    ap.add_argument("--allowlist", default=None,
                    help="ruta a relevant_decks.json (default: compartido en raiz del repo)")
    args = ap.parse_args()

    print(f">> construyendo universo para {DIR}", flush=True)
    summary = build_universe(str(DIR), allowlist_path=args.allowlist)
    print(">> RESUMEN:", flush=True)
    for k, v in summary.items():
        print(f"   {k}: {v}", flush=True)
    print(">> universo listo. Anki NO fue modificado (solo lectura).", flush=True)


if __name__ == "__main__":
    main()
