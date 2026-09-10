# DVA-C02 — AWS Certified Developer Associate

Anki MCQ decks for the DVA-C02 exam, one generator script per subdeck.

## Subdecks

| Script | Anki deck | Cards |
|---|---|---|
| `dva_c02_04.py` | `DVA-C02::04` | 22 |
| `dva_c02_05.py` | `DVA-C02::05` | 16 |
| `dva_c02_06.py` | `DVA-C02::06` | 18 |
| `dva_c02_07.py` | `DVA-C02::07` | 45 |
| `dva_c02_08.py` | `DVA-C02::08` | 26 |
| `dva_c02_09.py` | `DVA-C02::09` | 32 |

## Regenerate a deck

From the repo root (with the engine installed via `pip install -e .`), run a
generator from this folder so the `.apkg` lands in `out/`:

```bash
cd decks/dva-c02
../../.venv/bin/python dva_c02_04.py   # build -> verify -> import into DVA-C02::04
```

`create()` builds the `.apkg` into `out/`, runs the quality gate, and imports it
into the matching subdeck (needs Anki running with AnkiConnect). To only build +
verify without importing, edit the final `create(...)` call to pass
`do_import=False`.

## Notes

- `notes/review/` — per-card coherence + accuracy review (RESULTS.md, MANIFEST.txt).
- `notes/*.md` / `notes/*.html` — didactic explanations (AppSync, X-Ray).
- `notes/source/` — source material and failed-question sets used to build cards.

The `out/` folder is git-ignored; regenerate the `.apkg` files anytime.
