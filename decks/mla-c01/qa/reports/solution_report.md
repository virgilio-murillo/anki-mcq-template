# Solution report: MLA-C01 options-only give-away fix (16 cards)

Goal: remove "the correct option gives itself away by shape" without changing any
`correct_index` or `key`. Distractors rewritten as plausible near-misses (one
subtle technical error each), refutations updated, quality gate kept green.

## Build + verify
```bash
cd decks/mla-c01
../../.venv/bin/python mla_c01_01.py     # >> Wrote 56 cards, verify OK
../../.venv/bin/python mla_c01_02.py     # >> Wrote 56 cards, verify OK
../../.venv/bin/mcq-verify out/MLA-C01_01.apkg   # OK (0 problemas)
../../.venv/bin/mcq-verify out/MLA-C01_02.apkg   # OK (0 problemas)
```
correct_index confirmed unchanged for all 16 keys (script check: ALL OK).

## Per-key summary (absurd removed -> near-miss added)

- **mla01-q2** (correct=3): removed obvious non-ML options (manual analysis, raw data,
  if-else rules). Added ML-but-wrong approaches: train/evaluate on same set (no
  train/test split), unsupervised clustering used as labels, hand-set weights by
  intuition. Now all four sound like ML; you must know supervised + generalization.

- **mla01-q3** (correct=1): the average was the only "simple calc". Reframed correct as
  aggregating already-completed deliveries; added a predictive option that *looks*
  arithmetic (probability a future order is late). Discriminator = "summarize past"
  (no ML) vs "estimate the not-yet-observed" (ML).

- **mla01-q11** (correct=2, Parquet): removed the "optimizado para ML/analytics" echo that
  lived only on Parquet, plus keyword tells (heredadas, hojas de calculo). All four
  now claim efficiency; discriminator = columnar+compression for analytical reads vs
  row-based.

- **mla01-q22** (correct=3, DataSync->EFS): "EFS" now appears in three options (Transfer
  Family SFTP to EFS, Storage Gateway File Gateway to EFS, rsync over VPN to EFS).
  Discriminator = managed parallel on-prem->EFS migration with integrity verification.

- **mla01-q27** (correct=0, DMS homogeneous): removed the CDC-contradiction and the
  "upload Aurora via SDK" absurdity. New C/D are one-time-plausible (S3 dump + LOAD;
  Glue JDBC batch). Discriminator = MySQL->Aurora MySQL is homogeneous, managed by DMS.

- **mla01-q41** (correct=1, Bedrock): premium adjectives spread across options (Canvas =
  several managed models no-code; JumpStart = private fine-tune but deploy in your
  account; Studio = managed, choose/tune without operating servers). Discriminator =
  serverless multi-FM + private fine-tune by API, no endpoints to operate = Bedrock.

- **mla01-r1-formatos** (correct=0): removed absurdities (CSV binary, "todos columnares",
  "sirven igual"). Each distractor now has one subtle error (Avro wrongly listed as
  columnar; CSV/JSON Lines "columnar"; Parquet as row-based).

- **mla01-r2-storage** (correct=0): canonical matching. Instead of shuffling everything,
  each distractor swaps exactly ONE pair (Lustre/EFS, EBS/S3, EFS/EBS), leaving 3/4
  correct. Must know the exact mapping.

- **mla01-r3-kinesis** (correct=0): removed "identicos" and "exclusivo archivos en reposo".
  New near-misses: replay/reprocess attributed to Firehose; Data Streams "delivers to
  S3 without a consumer"; Firehose "exactly-once" guarantee.

- **mla01-r4-movimiento** (correct=0): removed "los tres hacen lo mismo". Each distractor
  swaps exactly one pair among DataSync (network) / S3 Transfer Acceleration (edge) /
  Data Transfer Terminal (physical offline).

- **mla01-r5-clarify** (correct=0): removed "compila modelos"/"etiqueta con humanos".
  Fine Clarify<->Model Monitor crosses (role swap; Clarify "detects drift"; Model
  Monitor "computes pre-train bias").

- **mla01-r6-groundtruth** (correct=0): removed "CNN desde cero"/"compila edge". Fine
  Ground Truth<->Comprehend crosses (role swap; Ground Truth "infers sentiment";
  Comprehend "coordinates human labelers").

- **mla01-r7-wrangler** (correct=0): removed "streaming IoT"/"compila edge". Fine Data
  Wrangler<->Feature Store crosses (role swap; Wrangler "serves online features";
  Feature Store "applies visual transforms").

- **mla01-r8-scaler** (correct=0): removed "Robust solo categoricas"/"identicos". New
  statistical near-misses (Robust as "mean 0 / var 1"; Standard "clips outliers";
  Robust "drops outlier rows then uses mean/std").

- **mla01-r9-dms** (correct=0): removed "transferencia fisica offline"/"solo NoSQL".
  Plausible confusions (homogeneous needs SCT; heterogeneous needs no conversion if
  both SQL; heterogeneous done manually without DMS/SCT).

- **mla02-q15** (correct=0, FSx Lustre): gave EFS (Max I/O), File Cache, EBS io2 Block
  Express comparable throughput/latency detail so "sub-millisecond/performance" no
  longer lands only on the correct option. Discriminator = parallel shared HPC file
  system for distributed training = Lustre. Also rebalanced option lengths.

## Confirmation
- correct_index unchanged in all 16 (verified programmatically).
- key unchanged in all 16.
- mcq-verify: **OK (0 problemas)** on both MLA-C01_01.apkg and MLA-C01_02.apkg.
- mla02-q33 left untouched (no defect).
