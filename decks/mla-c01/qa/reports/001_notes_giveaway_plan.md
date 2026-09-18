# Plan: fix options-only give-away in 16 MLA-C01 cards

Rule: NEVER change correct_index. Keep key. Rewrite only distractors (and light
question tweak if needed). Update the matching refutation in answer_html.
Balance option lengths (correct not longest >1.4x avg, not shortest <0.71x avg
when maxlen>=60). No {{L}} hardcode. 4 options. Spanish, HTML entities, no em dash.

## file 01 (mla_c01_01.py)
- mla01-q2 (correct=3): distractors -> plausible-but-suboptimal ML approaches.
- mla01-q3 (correct=1): keep the average outlier but add a 2nd deterministic-looking
  candidate so B is not the only "simple calc"; give distractors comparable framing.
- mla01-q11 (correct=2): remove "optimizado para ML/analytics" echo only on Parquet;
  describe each format with comparable strengths; discriminator = columnar+compression.
- mla01-q22 (correct=3): make 2-3 distractors mention EFS/file storage; discriminator
  = managed on-prem->EFS migration w/ verification.
- mla01-q27 (correct=0): raise C/D to one-time-plausible (export+LOAD, Glue ETL).
- mla01-q41 (correct=1): spread premium attributes; C/D also say "sin infra"/"varios modelos";
  discriminator = serverless multi-FM + private fine-tune (Bedrock) vs JumpStart deploys in your acct vs Studio IDE.
- r1-formatos (correct=0): one subtle error per distractor, no absurdities.
- r2-storage (correct=0): swap ONE pair per distractor, 3/4 correct.
- r3-kinesis (correct=0): near-misses (attribute replay to Firehose, etc.).
- r4-movimiento (correct=0): remove "los tres hacen lo mismo"; swap one pair.
- r5-clarify (correct=0): fine Clarify<->Model Monitor cross; remove "compila"/"etiqueta humanos".
- r6-groundtruth (correct=0): fine Ground Truth<->Comprehend cross; remove CNN/edge.
- r7-wrangler (correct=0): fine Data Wrangler<->Feature Store cross; remove IoT/edge.
- r8-scaler (correct=0): statistical near-misses; remove "solo categoricas"/"identicos".
- r9-dms (correct=0): plausible homogenea/heterogenea/SCT confusions; remove offline/NoSQL.

## file 02 (mla_c01_02.py)
- mla02-q15 (correct=0): give B/C/D comparable throughput/latency detail;
  discriminator = Lustre is the HPC FS for distributed training.

## NOT touched
- mla02-q33 (no defect).
