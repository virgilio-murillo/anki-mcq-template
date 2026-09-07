# DVA-C02::07 — Quality review (v2 investigation + 20 per-question agents + direct review)

Date: 2026-09-07
Deck: decks/dva-c02/dva_c02_07.py (27 atomic cards from 20 incorrect exam questions)

## Verdict summary: NO factual errors that change any correct answer.
All 20 questions verified against official AWS docs. Every marked-correct answer is CORRECT.
Findings are precision/clarity improvements (imprecise refutations, over-strong claims), not wrong answers.

## Per-question agent verification (docs-investigator vs official AWS docs)

| Q | Card key(s) | Verdict | Fix needed |
|---|---|---|---|
| Q2 | dva07-q2-* | OK | none (INDEXES/TOTAL/NONE, TRUE invalid all confirmed) |
| Q4 | dva07-q4-* | OK w/ nuance | Soften distractor "single shared Access Point + Lambda decides role": per docs a single OLAP branching on caller identity IS valid; per-role isolation comes from IAM/AP policies + Lambda logic, not from 1-OLAP-per-role being a requirement. Reword so it's "not the pattern the scenario asks", not "impossible". |
| Q6 | dva07-q6-* | OK | none (GSI own throughput + eventual only) |
| Q7 | dva07-q7-* | OK | none (Lambda custom non-proxy unambiguous; HTTP custom is plausible distractor, correctly refuted) |
| Q10 | dva07-q10-* | OK w/ optional note | Optional: mention that for PURE anti-hotlinking the most direct tool is a CloudFront Function validating Referer (already mentioned in extra). Answer stands. |
| Q15 | dva07-q15-* | OK | none (GetTraceSummaries has FilterExpression; BatchGetTraces by ID only) |
| Q17 | dva07-q17-* | OK | none (WAF for SQLi/XSS) |
| Q19 | dva07-q19-* | OK | none (S3+CloudFront; EFS not a native origin, confirmed by absence) |
| Q21 | dva07-q21-* | OK | none (SAM native, transforms to CFN) |
| Q23 | dva07-q23-* | OK w/ precision | Precise wording: it's the EXTERNAL third-party IdP connection of IAM Identity Center that is SAML-based (IC also has its own store + AWS Managed Microsoft AD). Reword "se apoya en federacion SAML" -> "su conexion a IdP externo de terceros es SAML". Answer stands. |
| Q26 | dva07-q26-* | OK | none (LSI same PK/alt sort/strong, created-with-table-only; GSI anytime) |
| Q29 | dva07-q29-* | OK | none (annotations indexed, in subsegment; metadata not indexed) |
| Q34 | dva07-q34-* | OK w/ nuance | Card already frames as "explicitly selecting a strategy / least config" which makes random unambiguous. Optional: strengthen spread refutation noting spread-across-AZ is the implicit SERVICE default (so avoid pure "default" framing). |
| Q37 | dva07-q37-* | OK | none (build->package->deploy-from-S3 confirmed; sam deploy implicit package) |
| Q41 | dva07-q41-* | OK w/ precision | Soften "DynamoDB no bloquea items asi": no NATIVE single-API item lock, but pessimistic locking IS achievable via TransactWriteItems / lock client. Reword to "no tiene un bloqueo de item nativo integrado". Answer (optimistic locking) stands. |
| Q45 | dva07-q45-* | OK | none (1600 RCU confirmed with doc worked examples) |
| Q47 | dva07-q47-* | **FIX (imprecision)** | Card ties AWSXRayDaemonWriteAccess to Elastic Beanstalk. Beanstalk docs actually name **AWSXrayWriteOnlyAccess** (in the EB instance profile). AWSXRayDaemonWriteAccess is correct for EC2/general daemon. Exam/tutorialsdojo source uses AWSXRayDaemonWriteAccess, so keep the exam answer, but add a nuance callout distinguishing EB (AWSXrayWriteOnlyAccess) vs general (AWSXRayDaemonWriteAccess), and note casing "XRay" vs "Xray". |
| Q48 | dva07-q48-* | OK | none (Code.ZipFile inline Node/Python, file 'index'; Handler distractor correctly refuted) |
| Q50 | dva07-q50-* | OK | none (20 WCU, 10 RCU eventual confirmed) |
| Q57 | dva07-q57-* | OK | none (SSE-C + client-side = customer-managed keys; SSE-S3/SSE-KMS = AWS-managed) |

## Direct-review (option b) additional clarity notes
- Q57: the correct option packs two techniques ("elige el par correcto"). Clear enough given the framing; keep.
- No card leaks the answer on the front; all backs refute distractors one by one; all use {{L}}; 4 options each. DECK_STANDARDS.md compliant.

## Fixes to apply (all are precision/clarity, none change a correct answer)
1. Q47: add EB vs general daemon policy nuance (AWSXrayWriteOnlyAccess vs AWSXRayDaemonWriteAccess) + casing note. [most important]
2. Q4: soften "single shared Access Point" distractor refutation.
3. Q41: reword "DynamoDB no bloquea items asi" -> "no tiene bloqueo de item nativo integrado".
4. Q23: precise "IdP externo de terceros via SAML".
5. Q34: (optional) strengthen spread refutation re: implicit service default.

## v2 investigation findings (6 investigator-contrarian pairs) — ADDED 2 findings the single-agent pass under-weighted

### Q6 dva07-q6-gsi-capacity — HIGH (factual error in explanation)
The explanation says WRITES consume WCU "del indice, no de la tabla". WRONG for writes:
a write consumes WCU from the base table AND additionally from the GSI (it's the SUM,
not "index instead of table"). "Del indice, no de la tabla" is only correct for
QUERY/SCAN reads on the index. Source: GSI.html "Provisioned throughput considerations".
FIX: separate reads (from index) vs writes (base table + index).

### Q29 dva07-q29-annotations-subsegment — HIGH/CRITICAL (no strictly-unique answer)
Stem asks to "buscar con filter expressions". Annotations are indexed/filterable whether
on a SEGMENT or a SUBSEGMENT (aggregated at trace level). So "annotation en el segment"
ALSO satisfies searchability. The card's refutation conflates WHERE the SQL call is
captured (subsegment, correct) with WHETHER the annotation is searchable (identical).
Source: xray-concepts.html "Annotations can be added to any segment or subsegment".
FIX: retighten the stem to ask WHERE the downstream RDS call is recorded (subsegment).

### Other v2 confirmations
- Q4 refutation weak (single shared OLAP can branch on caller role) -> soften. [MED/LOW]
- Q41 "no bloquea items asi" imprecise (pessimistic possible via TransactWriteItems/lock client). [MED]
- Q23 IAM Identity Center: it's the EXTERNAL third-party IdP connection that is SAML-based. [MED]
- Q57 SSE-KMS "subes tu material" phrasing imprecise. [MED]
- Q10 hotlinking: signed URLs = access control; pure anti-hotlink = Referer via CF Functions. [MED]
- Q34 spread is the implicit SERVICE default -> avoid pure "default" framing. [LOW]

## FINAL FIX LIST (priority order)
1. [HIGH] Q6: fix write-capacity explanation (base table + index, not "index not table").
2. [HIGH] Q29: retighten stem to "donde se registra la llamada a RDS" so subsegment is unique.
3. [FIX] Q47: EB vs general daemon policy nuance + casing.
4. [MED] Q4, Q41, Q23, Q57: soften/precise the flagged refutations.
5. [LOW] Q34 spread wording.

All marked-correct ANSWERS remain correct. Fixes are explanation precision + one stem tightening.

## v2 investigation: v2-371a06 (judge report pending; 6-pair findings captured above)
