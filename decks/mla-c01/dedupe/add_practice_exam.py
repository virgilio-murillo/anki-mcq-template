#!/usr/bin/env python3
"""
add_practice_exam.py — Pipeline reproducible para AGREGAR un examen de practica
nuevo como un deck extra de Anki, SIN repetir conceptos que ya estudias.

Disenado por la investigacion v2-ec81d2. Convierte un examen de practica en texto
en un deck nuevo que contiene SOLO las preguntas cuyo concepto NO esta ya cubierto
en los decks Anki existentes (MLA-C01 + DVA-C02).

=========================  COMO USARLO  =========================
Requisitos: Anki abierto con AnkiConnect (localhost:8765) para el dedup.

  cd decks/mla-c01
  ../../.venv/bin/python dedupe/add_practice_exam.py \
        --exam ../../practice_exam_3.txt \
        --deck "MLA-C01::04" \
        --keyprefix mla04

Etapas (cada una es un script en dedupe/; puedes correrlas sueltas para depurar):

  1. parse_new_exam.py       Parsea el examen -> new_exam_parsed.json (limpias) +
                             new_exam_quarantine.json (multi-select/matching/vacias).
                             Emite un registro por CADA pregunta; cero descartes silenciosos.
  2. dump_existing.py        Vuelca via AnkiConnect las cartas existentes
                             (MLA-C01::* + DVA-C02::*) -> existing_cards.json (universo dedup).
  3. prepare_concepts.py     Destila concepto por carta nueva y existente.
  4. DEDUP (LLM-judge)       Un agente experto decide COVERED/NEW por CONCEPTO
                             (granularidad de examen), no por texto. -> dedup_verdicts.jsonl.
                             (Ver dedupe/README.md: como lanzar el juez.)
  5. generar el deck         Un developer-agent crea decks/mla-c01/mla_c01_NN.py con
                             SOLO las NEW, aplicando DECK_STANDARDS + anti-give-away.
  6. QA gates               qa/ (correccion) + qa/clarity/ (claridad + anti-give-away).
  7. import                 create(..., do_import=True) hacia el subdeck nuevo.

NOTA (del fallo del juez v2-ec81d2):
- El motor anki_mcq soporta 4 opciones y UNA correcta. Las multi-select y matching
  quedan en cuarentena (revision manual), nunca se fuerzan.
- El dedup por concepto usa el mismo criterio calibrado que dva-c02 (COVERED si el
  objetivo examinable ya se ensena, aunque el angulo sea distinto; NEW solo si es
  servicio/feature/objetivo no cubierto). Ante la duda: COVERED.
- Reconciliar el modelo 'MCQ (didactic)' antes de cualquier sync que preserve progreso.
=================================================================

Este archivo es la GUIA + orquestador ligero. Las etapas 4 y 5 usan agentes LLM
(dedup-judge y developer-agent); ver dedupe/README.md para los prompts exactos.
"""
import argparse
import subprocess
import sys
import pathlib

DIR = pathlib.Path(__file__).resolve().parent          # decks/<exam>/dedupe
DECKDIR = DIR.parent                                    # decks/<exam>
PY = str(DECKDIR.parents[1] / ".venv" / "bin" / "python")


def run(script, *args):
    print(f"\n=== {script} {' '.join(args)} ===", flush=True)
    subprocess.run([PY, str(DIR / script), *args], check=True)


def main():
    ap = argparse.ArgumentParser(description="Agregar un examen de practica deduplicado.")
    ap.add_argument("--exam", required=True, help="ruta al .txt del examen de practica")
    ap.add_argument("--deck", required=True, help='nombre del subdeck Anki, ej. "MLA-C01::04"')
    ap.add_argument("--keyprefix", required=True, help="prefijo de key, ej. mla04")
    args = ap.parse_args()

    print(__doc__)
    print(f"\nParametros: exam={args.exam}  deck={args.deck}  keyprefix={args.keyprefix}")
    print("\nEtapas automatizables (1-3). Las etapas 4-7 usan agentes LLM: ver dedupe/README.md.\n")

    # Etapa 1: parsear (el parser usa la ruta fija practice_exam_2.txt; parametrizar si cambias de examen)
    run("parse_new_exam.py")
    # Etapa 2: volcar universo existente (requiere Anki abierto)
    run("dump_existing.py")
    # Etapa 3: preparar conceptos
    run("prepare_concepts.py")

    print("\n>> Etapas 1-3 listas. Continua con la etapa 4 (dedup LLM-judge) segun dedupe/README.md.")
    print(">> Luego etapa 5 (generar deck), 6 (QA), 7 (import).")


if __name__ == "__main__":
    main()
