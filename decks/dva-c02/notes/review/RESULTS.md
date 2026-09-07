# Per-card review results (coherence stem<->answer + accuracy)

Manifest: kiro-notes/review/MANIFEST.txt maps card_NN.txt to its deck.

## Batch 1 (cards 1-7)
- card_01 (::04 KMS perms multipart): OK. Coherence confirmed; kms:Decrypt+GenerateDataKey correct. Optional polish only.
- card_02 (::04 CRR versioning cause): OK. Minor optional note on Object Lock refutation wording; not a defect.
- card_03 (::04 CRR requirements): OK. All 3 requirements confirmed; distractors refuted.
- card_04 (::04 multipart CLI): OK. multipart_threshold 8MB confirmed; optional wording on data key.
- card_05 (::04 CRR prereq versioning): OK. Object Lock only conditional; distractors fine.
- card_06 (::04 RCU meaning 1 RCU): OK. All numbers confirmed.
- card_07 (::04 RCU mistake -> 75): OK. Math exact; optional: update stale primary doc link to provisioned-capacity-mode.html.

NO incoherent stems in batch 1. Only optional link/wording polish.

## Batch 2 (cards 8-13)
- Coherence: all OK, NO irrespondible stems found.
- False positives to IGNORE: two agents flagged "Correcta: A/C hardcoded letter" — these are {{L}} render artifacts, source is fine.
- REAL finding (Lambda@Edge card in ::04, the CloudFront slow-login/504 "lambda-edge" card): explanation presents Lambda@Edge as the generic "edge auth" tool. AWS docs classify JWT/token validation at the edge as the IDEAL use case for CloudFront FUNCTIONS, not Lambda@Edge. MC answer unaffected (CF Functions is not an option there), but add a nuance. Source: edge-functions-choosing.html.
- Card 13 (poll-vs-push concurrency): OK; optional ParallelizationFactor nuance already partly present.
- Cards LSI/GSI + projection: OK.
- TODO fix: add CF-Functions-vs-Lambda@Edge nuance to the ::04 lambda-edge card back.

## Batch 3 (cards 14-17, ::04 tail)
- card_14/15/16: OK coherence. False-positive "hardcoded letter" flags (ignore, {{L}} render). Optional: refresh a couple of DynamoDB doc links (HowItWorks.ReadWriteCapacityMode -> provisioned-capacity-mode / read-write-operations).
- card_17: running at cutoff (CRR prereq versioning) — prior identical card already OK.

## FIXES APPLIED SO FAR
- ::05 write-through cache stem rewritten (coherence: cache reflects latest write; TTL expires cache entry, not DB row). [the defect you found]
- ::04 lambda-edge card: added CloudFront Functions vs Lambda@Edge nuance.

## COHERENCE DEFECT RATE
1 real incoherent stem (cache) out of ~16 cards individually reviewed + 1 accuracy nuance (lambda-edge). Rate is low.

## Batch 4 (cards 17-22, finishing ::04)
- card_18 (origin-failover) NEEDS-FIX (2 real): (a) COHERENCE: stem anchored 504 to "logins" (POST) but origin failover only fires on GET/HEAD/OPTIONS -> reworded stem to GET-servable content. (b) ACCURACY: failover code list incomplete -> corrected to 400,403,404,416,429,500,502,503,504 (none default). BOTH FIXED.
- cards 17,19,20,21,22: OK coherence + accuracy. Optional: tutorialsdojo links (kept, consistent with ::01-03).
- ::04 fully reviewed (1-22). Real fixes in ::04: cache?(no, that's ::05), lambda-edge nuance, origin-failover stem+codes.

## Batch 5 (cards 24-29, ::05)
- card_24 (why-ttl): minor -> split grouped A/B/C refutation into one-by-one. FIXED.
- card_23 (write-through, rewritten): OK confirmed (my coherence fix holds).
- cards 25 (AppSync), 26 (AppSync vs Cognito Sync), 27 (sam deploy), 28 (TDE), 29 (GSI WCU): all OK coherence + accuracy. Optional-only notes (tutorialsdojo links, Cognito Sync legacy context). No stem incoherence.

## Batch 6 (cards 30-34)
- card_31 (S3 Object Lambda) NEEDS-FIX (2 real): (a) verdict double-counted GetObject (already in option B); (b) enunciado dice "cada usuario ve solo lo suyo" pero el aislamiento lo da IAM, no mencionado. FIXED: verdict reescrito sin duplicar, y agregada la explicacion IAM (cada rol asume un rol IAM con acceso solo a su Object Lambda Access Point).
- cards 30 (GSI throttle), 32 (Object Lambda how), 33 (X-Ray segment vs subsegment), 34 (CW vs Enhanced): OK coherence + accuracy. Optional link-precision notes only.

## Batch 7 (cards 35-39)
- card_38 (::05 CodePipeline 7-day): FIXED - removed "configurable" (7-day is a service fixed period, not documented configurable). Also same fix applied to the approval-timeout card.
- card_35 (::05 Enhanced Monitoring): FIXED - console-refutation was misleading; per-process metrics DO show in console when Enhanced Monitoring is enabled; standard console metrics are aggregated.
- card_39 (::06 drift detection): FIXED - AWS Config refutation refined (Config can report drift via managed rule cloudformation-stack-drift-detection-check which invokes DetectStackDrift; native tool is drift detection).
- cards 36 (CodePipeline+SNS), 37 (?): OK; false-positive "hardcoded letter" ignored; tutorialsdojo link notes optional.

## Batch 8 (cards 40-44)
- cards 40 (drift/CloudTrail), 41 (Export/ImportValue), 42 (RCU 1600), 43 (why-800 eventual), 44 (projection expr): ALL OK coherence + accuracy. Only false-positive "hardcoded letter" flags (ignore) + optional tutorialsdojo/link-anchor notes.







