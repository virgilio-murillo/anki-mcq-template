# AWS Fact Verification for MLA-C01 Exam Questions

Verified against official AWS documentation on 2026-09-15. Each claim is labeled
CONFIRMED, PARTIALLY CORRECT, or INCORRECT, with the supporting doc URL(s).

Note on sourcing: the AWS documentation MCP tools were not available in this session.
Verification was performed against official AWS docs pages (docs.aws.amazon.com)
fetched directly. All cited pages are the canonical AWS documentation.

---

## (1) AWS Lambda deployment package size limits and execution limits

Source: [Lambda quotas](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)

| Claim | Verdict | Documented value |
|---|---|---|
| Container image supports up to 10 GB | CONFIRMED | "Container image code package size: 10 GB (maximum uncompressed image size, including all layers)" |
| `/tmp` up to 10 GB | CONFIRMED | "`/tmp` directory storage: Between 512 MB and 10,240 MB, in 1-MB increments" (10,240 MB = 10 GB; default is 512 MB) |
| .zip 250 MB unzipped | CONFIRMED | "Deployment package (.zip file archive): 250 MB ... The maximum size of the contents of a deployment package, including layers and custom runtimes (unzipped)" |
| 15-min timeout | CONFIRMED | "Function timeout: 900 seconds (15 minutes)" |
| 6 MB synchronous payload | CONFIRMED | "Invocation payload (request and response): 6 MB each for request and response (synchronous)" |

All five Lambda facts are CONFIRMED.

### Nuances worth knowing for exam precision (documented, not contradictions)
- `/tmp` default is 512 MB; 10 GB (10,240 MB) is the configurable maximum. If a
  question implies the *default* is 10 GB, that is wrong; the default is 512 MB.
- The 50 MB .zip limit refers to the *zipped* upload via the Lambda API/console;
  250 MB is the *unzipped* total (including layers). Both numbers are real but
  measure different things. Source: same quotas page,
  "Deployment package (.zip file archive)" row.
- Asynchronous invocation payload limit is 1 MB (not 6 MB). The 6 MB figure is
  specifically the synchronous request/response limit. Source: same quotas page;
  also [Invoke API](https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html).
- Function timeout of 15 minutes is the standard. Newer "Lambda Managed Instances"
  async/event-source invocations allow up to 90 minutes, but this is a special
  variant and not the general answer. Source: same quotas page.

---

## (2) Amazon S3 VPC endpoints (gateway vs interface)

Primary sources:
- [Gateway endpoints for Amazon S3](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- [AWS PrivateLink for Amazon S3 (Types of VPC endpoints)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html)
- [Gateway endpoints (PrivateLink guide)](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html)

### Gateway endpoints
| Claim | Verdict | Documented support |
|---|---|---|
| Regional | CONFIRMED | "A gateway endpoint is available only in the Region where you created it. Be sure to create your gateway endpoint in the same Region as your S3 buckets." |
| Route-table based | CONFIRMED | "you can add it as a target in your route table for traffic destined from your VPC to Amazon S3" |
| Free / no additional cost | CONFIRMED | "There is no additional charge for using gateway endpoints." |
| Only S3 and DynamoDB | CONFIRMED | "Gateway VPC endpoints provide reliable connectivity to Amazon S3 and DynamoDB ... Gateway endpoints do not use AWS PrivateLink" (PrivateLink guide, gateway-endpoints page) |
| Intra-region / no on-prem, no peered other-region VPC, no transit gateway | CONFIRMED | "gateway endpoints do not allow access from on-premises networks, from peered VPCs in other AWS Regions, or through a transit gateway" |

Gateway endpoint claims are CONFIRMED.

### Interface endpoints (PrivateLink)
| Claim | Verdict | Documented support |
|---|---|---|
| Use ENI / private IP | CONFIRMED | "Interface endpoints are represented by one or more elastic network interfaces (ENIs) that are assigned private IP addresses from subnets in your VPC" |
| Cost per hour | CONFIRMED (billed) | S3 "Types of VPC endpoints" table: interface = "Billed", gateway = "Not billed". (Interface endpoint pricing is per-hour-per-AZ plus data processing; the docs page confirms "billed" / "available for an additional cost".) |
| Many services | CONFIRMED | Interface endpoints (PrivateLink) support a broad set of AWS services, unlike gateway endpoints which support only S3 and DynamoDB. |
| Support on-premises access | CONFIRMED | S3 interface endpoints "are directly accessible from applications that are on premises over VPN and Direct Connect" |

Interface endpoint core claims are CONFIRMED.

### Cross-region S3 access from a VPC: PARTIALLY CORRECT / NEEDS NUANCE

The exam claim states: "accessing an S3 bucket in a DIFFERENT region from a VPC
requires VPC peering or Transit Gateway (both endpoint types are regional)."

- CONFIRMED for the *classic* S3 endpoint model. The S3 "Types of VPC endpoints"
  table explicitly says interface endpoints "Allow access from a VPC in another
  AWS Region **by using VPC peering or AWS Transit Gateway**", and gateway
  endpoints "Do not allow access from another AWS Region."
  Source: [privatelink-interface-endpoints.html](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html)
- So the exam's core mechanism (reach the interface endpoint that lives in S3's
  home region via VPC peering / Transit Gateway) is accurate for standard S3
  bucket access.

### Is there a `vpce:AllowMultiRegion` / cross-region S3 interface endpoint capability?

- There is NO documented IAM condition key or endpoint flag named
  `vpce:AllowMultiRegion`. That specific term does not appear in AWS documentation.
  Verdict on that exact wording: NOT DOCUMENTED (treat as INCORRECT if a question
  presents `vpce:AllowMultiRegion` as a real feature).
- HOWEVER, two real cross-region capabilities exist and complicate any absolute
  "S3 endpoints are strictly regional, so you must peer" statement:

  1. **Cross-Region PrivateLink (interface endpoints to services in another
     Region).** AWS launched cross-region connectivity for PrivateLink. When you
     create an interface endpoint you can select "Enable cross Region endpoint"
     and choose the target service Region.
     Sources:
     [Access an AWS service using an interface VPC endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html)
     ("If creating an endpoint to an AWS service in another Region, select the
     Enable cross Region endpoint checkbox"),
     [Cross-region enabled AWS services](https://docs.aws.amazon.com/vpc/latest/privatelink/aws-services-cross-region-privatelink-support.html).
     Whether S3 (as a plain regional interface endpoint) is in the cross-region
     enabled service list should be checked against that list before asserting it
     in an exam answer; the general PrivateLink cross-region feature is real and
     documented.

  2. **S3 Multi-Region Access Points with PrivateLink.** You can provision
     interface endpoints to an S3 Multi-Region Access Point and route requests
     across multiple Regions over a private connection *without configuring VPC
     peering*.
     Source:
     [Configuring a Multi-Region Access Point for use with AWS PrivateLink](https://docs.aws.amazon.com/AmazonS3/latest/userguide/MultiRegionAccessConfiguration.html)
     ("you can route S3 requests ... across multiple AWS Regions, over a private
     connection ... you don't need to configure a VPC peering connection").

### Recommendation for the exam question
- Keep the gateway-vs-interface comparison as stated (all CONFIRMED).
- The statement "accessing an S3 bucket in a different region requires VPC peering
  or Transit Gateway" is correct for the *standard S3 regional endpoint* scenario
  and is a defensible exam answer.
- Do NOT reference `vpce:AllowMultiRegion` as a feature: it is not a documented
  AWS capability.
- If the question wants an absolute "there is no cross-region S3 endpoint option
  at all," soften it: S3 Multi-Region Access Points + PrivateLink and general
  cross-region PrivateLink are real, documented exceptions. For a clean single
  right answer, frame the peering/Transit Gateway requirement as applying to a
  standard regional S3 interface/gateway endpoint.

---

## (3) SageMaker Model Monitor: the four monitor types

Primary sources:
- [Data and model quality monitoring with Amazon SageMaker Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html)
- [SageMaker Model Monitor FAQ](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-faqs.html)
- [SageMaker Model Monitor MLOps](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-mlops.html)

| Type | Verdict |
|---|---|
| Data quality | CONFIRMED |
| Model quality | CONFIRMED |
| Bias drift | CONFIRMED |
| Feature attribution drift | CONFIRMED |

The FAQ states customers monitor along "four dimensions - Data quality, Model
quality, Bias drift, and Feature Attribution drift." The MLOps page repeats the
same four: "data quality, model quality, bias drift and feature attribution
drift." Bias drift and feature attribution drift are delivered via integration
with SageMaker Clarify.

### "Concept drift" and "latency drift"
- Neither "concept drift" nor "latency drift" is a SageMaker Model Monitor
  monitor type. CONFIRMED that these are NOT among the four types.
- "Concept drift" is a general ML term (and appears in AWS whitepapers as a
  concept), but it is not one of the four named Model Monitor types. Labeling it
  as a Model Monitor type is INCORRECT.
- "Latency drift" is not an AWS Model Monitor type at all. (Latency is an
  operational metric surfaced through CloudWatch/endpoint metrics, not a Model
  Monitor drift category.) Treating it as a Model Monitor type is INCORRECT.

Exam claim (3) is fully CONFIRMED, including that concept drift and latency drift
are distractors.

---

## (4) SageMaker execution role KMS permissions for SSE-KMS S3 training data

Primary sources:
- [Using server-side encryption with AWS KMS keys (SSE-KMS) - S3 Permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)
- [AWS managed policies for SageMaker AI jobs](https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-jobs.html)

### The core rule (from the S3 SSE-KMS Permissions section)
Documented verbatim behavior:
- To **PutObject** (write/encrypt) an object with a KMS key: you need
  `kms:GenerateDataKey` permission.
- To **download** (read/decrypt) a KMS-encrypted object: you need `kms:Decrypt`.
- To perform a **multipart upload** of a KMS-encrypted object: you need BOTH
  `kms:GenerateDataKey` and `kms:Decrypt`.

| Claim | Verdict |
|---|---|
| `kms:Decrypt` for reading SSE-KMS training data | CONFIRMED |
| `kms:GenerateDataKey` for writing SSE-KMS output | CONFIRMED |
| `kms:Encrypt` is NOT what enables reading | CONFIRMED |

Reading an SSE-KMS object requires `kms:Decrypt`, not `kms:Encrypt`. S3 uses
envelope encryption: on write, S3 calls `GenerateDataKey`; on read, S3 calls
`Decrypt` to unwrap the data key. `kms:Encrypt` is not the action that grants
read access to SSE-KMS S3 objects, so an answer choice offering `kms:Encrypt`
for reading is INCORRECT.

### SageMaker-specific confirmation
The AWS managed policy documentation for SageMaker AI jobs states the KMS
permissions granted are `Decrypt` and `GenerateDataKey` for server-side
encryption of S3 objects (restricted via `kms:ViaService` to S3), plus
`DescribeKey`. This matches the general S3 SSE-KMS requirement:
- Reading encrypted input training data -> `kms:Decrypt`
- Writing encrypted output/model artifacts -> `kms:GenerateDataKey`
Source: [security-iam-awsmanpol-jobs.html](https://docs.aws.amazon.com/sagemaker/latest/dg/security-iam-awsmanpol-jobs.html)

### One caveat (do not let it create a wrong distractor)
- A SageMaker troubleshooting knowledge-center article mentions the execution
  role policy should allow "kms:encrypt and kms:decrypt" for training-job S3
  access. This is a broader/looser guidance article, not the authoritative
  minimum-permission statement. The authoritative S3 SSE-KMS docs are precise:
  reads need `kms:Decrypt`, writes need `kms:GenerateDataKey`. For an exam that
  asks which single permission enables *reading* SSE-KMS data, the answer is
  `kms:Decrypt` (NOT `kms:Encrypt`). Source of the caveat:
  [Resolve S3 AccessDenied in SageMaker training jobs](https://aws.amazon.com/premiumsupport/knowledge-center/sagemaker-s3-accessdenied-training/)
  (support article, treat as secondary to the S3 SSE-KMS docs).

Exam claim (4) is CONFIRMED.

---

## Summary table

| # | Claim | Verdict |
|---|---|---|
| 1 | Lambda: 10 GB image, 10 GB /tmp max, 250 MB unzipped .zip, 15-min timeout, 6 MB sync payload | CONFIRMED (note: /tmp default 512 MB; async payload 1 MB) |
| 2 | Gateway = regional, route-table, free, S3/DynamoDB only, intra-region | CONFIRMED |
| 2 | Interface = ENI/private IP, billed, many services, on-prem access | CONFIRMED |
| 2 | Cross-region S3 from VPC needs VPC peering / Transit Gateway | CONFIRMED for standard regional endpoints; exceptions exist (S3 MRAP + PrivateLink, cross-region PrivateLink) |
| 2 | `vpce:AllowMultiRegion` capability | NOT DOCUMENTED / treat as INCORRECT (no such feature) |
| 3 | Model Monitor 4 types: data quality, model quality, bias drift, feature attribution drift | CONFIRMED |
| 3 | "concept drift" and "latency drift" are NOT Model Monitor types | CONFIRMED |
| 4 | Read SSE-KMS S3 data needs kms:Decrypt; write needs kms:GenerateDataKey; kms:Encrypt does not enable reading | CONFIRMED |

## Items outside the requested scope (noted, not chased)
- Cross-Region PrivateLink is a newer general feature; verifying whether plain S3
  regional interface endpoints appear in the "cross-region enabled services" list
  would require reading that list in full. Flagged for follow-up if a question
  depends on it.
