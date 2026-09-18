# DVA-C02 Flashcard Fact Verification (AWS Documentation)

Verified 2026-09-09 against official AWS documentation. All 8 facts CONFIRMED.
Confidence labels: CONFIRMED = stated verbatim in official AWS docs.

---

## 1. Decoding an authorization message from UnauthorizedOperation — CONFIRMED

- **CLI form:** `aws sts decode-authorization-message` (accepts `--encoded-message`).
- **API operation:** `DecodeAuthorizationMessage` (AWS STS).
- **Required IAM permission:** `sts:DecodeAuthorizationMessage`.

Doc quote (STS API ref): to decode an authorization status message, the user must be granted permissions via an IAM policy to request the `DecodeAuthorizationMessage` (`sts:DecodeAuthorizationMessage`) action. The message is encoded because the authorization status details can contain privileged information the requester should not see.

**Flashcard-safe statement:** The encoded message returned in an `UnauthorizedOperation` / `AccessDenied` error is decoded with the STS `DecodeAuthorizationMessage` API (`aws sts decode-authorization-message`), and the caller needs the `sts:DecodeAuthorizationMessage` IAM permission.

Sources:
- API: https://docs.aws.amazon.com/STS/latest/APIReference/API_DecodeAuthorizationMessage.html
- CLI: https://docs.aws.amazon.com/cli/latest/reference/sts/decode-authorization-message.html

---

## 2. Step Functions — which state types support `Catch` and `Retry` — CONFIRMED

**Answer: NOT only Task and Parallel. Map states ALSO support both `Catch` and `Retry`.**
The three states that support error handling are **Task, Parallel, and Map**.

Doc quotes (Handling errors in Step Functions workflows):
- Catchers: "Step Functions catchers are available for **Task, Parallel and Map** states, but not for top-level state machine execution failures."
- Retry: "`Task`, `Parallel`, and `Map` states can have a field named `Retry` ..."
- Catch / Fallback: "`Task`, `Map` and `Parallel` states can each have a field named `Catch`."

Note: `Pass` and `Wait` states cannot encounter runtime errors, so they do not use Catch/Retry. `Choice`, `Succeed`, `Fail` do not support Catch/Retry either. Only Task, Parallel, and Map do.

**Flashcard-safe statement:** In Amazon States Language, `Retry` and `Catch` are supported by Task, Parallel, AND Map states (not just Task and Parallel). Any flashcard claiming "only Task and Parallel" is WRONG.

Source:
- https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html

---

## 3. DynamoDB BatchGetItem limits — CONFIRMED

- **Per-operation limits:** up to **100 items** AND up to **16 MB** of data.
- **Partial results:** yes, `BatchGetItem` returns **`UnprocessedKeys`** when it cannot process everything in a single call (response size limit exceeded, provisioned throughput exceeded, more than 1 MB requested per partition, or an internal processing failure).

Doc quote (BatchGetItem API ref): a single operation can retrieve up to 16 MB of data, which can contain as many as 100 items. Example given: if you request 100 items each 300 KB in size, the system returns 52 items (to stay under 16 MB) plus an appropriate `UnprocessedKeys` value so you can get the next page.

**Flashcard-safe statement:** `BatchGetItem` retrieves up to 100 items OR 16 MB per call (whichever limit is hit first) and returns `UnprocessedKeys` for anything not returned; the app should retry those keys (ideally with backoff).

Source:
- https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchGetItem.html

---

## 4. Lambda Function URL — FunctionUrlAuthType values — CONFIRMED

**Answer: Yes. The only two values are `AWS_IAM` and `NONE`.**

- `AWS_IAM` — restrict access to authenticated (IAM-authorized) callers only.
- `NONE` — bypass IAM auth for a public endpoint (the function's resource-based policy must still grant public access).

Doc quote (FunctionUrlConfig API ref): the AuthType is set to `AWS_IAM` to restrict access to authenticated users only, or `NONE` to bypass IAM authentication and create a public endpoint.

**Flashcard-safe statement:** A Lambda function URL's `AuthType` (`FunctionUrlAuthType`) is either `AWS_IAM` or `NONE` — those are the only two values.

Sources:
- API type: https://docs.aws.amazon.com/lambda/latest/api/API_FunctionUrlConfig.html
- Auth model: https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html
- Config guide: https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html

---

## 5. STS GetSessionToken — MFA for a pre-existing IAM user — CONFIRMED

**Answer: Yes.** MFA-enabled IAM users call `GetSessionToken` and submit an MFA code from their device. The returned temporary credentials can then be used to make programmatic calls to operations that require MFA authentication. `GetSessionToken` accepts `SerialNumber` (MFA device ID) and `TokenCode` parameters.

Doc quote (GetSessionToken API ref): MFA-enabled IAM users must call `GetSessionToken` and submit an MFA code associated with their MFA device; the returned temporary credentials can then be used for API operations that require MFA authentication.

**Flashcard-safe statement:** `GetSessionToken` is used by an existing IAM user (long-term credentials) to obtain short-term credentials, and it supports MFA via `SerialNumber` + `TokenCode`. It is NOT used to assume roles or for federation.

Sources:
- API: https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html
- MFA sample: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_sample-code.html

---

## 6. STS AssumeRole — also supports MFA — CONFIRMED

**Answer: Yes.** `AssumeRole` can include MFA information. You pass `SerialNumber` (identifies the hardware or virtual MFA device) and `TokenCode` (the 6-digit TOTP from the device). This is used when the assumed role's trust policy contains a condition testing for MFA, e.g. `"Condition": {"Bool": {"aws:MultiFactorAuthPresent": true}}`. If the role requires MFA and `TokenCode` is missing or expired, `AssumeRole` returns an access-denied error.

Doc detail (AssumeRole API ref):
- `SerialNumber` (Optional): identification number of the MFA device associated with the calling user; hardware serial (e.g. `GAHT12345678`) or virtual-device ARN (e.g. `arn:aws:iam::123456789012:mfa/user`).
- `TokenCode` (Optional): the value from the MFA device; fixed length of 6 numeric digits.

**Flashcard-safe statement:** Both `AssumeRole` AND `GetSessionToken` support MFA via `SerialNumber` + `TokenCode`. For `AssumeRole`, MFA is typically enforced by an `aws:MultiFactorAuthPresent` condition in the role's trust policy.

Source:
- https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html

---

## 7. DynamoDB Scan — sequential by default, parallel via Segment/TotalSegments — CONFIRMED

- **Default:** "Scan operations proceed sequentially" (a single Scan reads the table/index and can effectively read one partition's worth at a time; it is not parallelized by default).
- **Parallel scan:** applications request a parallel Scan by providing the **`Segment`** and **`TotalSegments`** parameters. `TotalSegments` is the number of worker segments; each worker specifies its own `Segment` index.

Doc quote (Scan API ref): "Scan operations proceed sequentially; however, for faster performance on a large table or secondary index, applications can request a parallel Scan operation by providing the `Segment` and `TotalSegments` parameters."

**Flashcard-safe statement:** A default DynamoDB `Scan` runs sequentially; to parallelize, split the table into logical segments using `TotalSegments` (total workers) and `Segment` (this worker's index). Scans are less efficient than Query because they read the entire table/index.

Sources:
- https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html
- Best practices (parallel scan): https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-query-scan.html

---

## 8. dynamodb:LeadingKeys — fine-grained access by partition key — CONFIRMED

- **`dynamodb:LeadingKeys`** is the IAM policy condition key that restricts access to items whose **partition key** value matches a specified value (commonly the user's identity, via a policy variable such as `${www.amazon.com:user_id}` or a Cognito/federated identity substitution).
- It is used with a `Condition` block in an IAM (identity-based) policy to enforce item-level (row-level) access without application-side authorization logic.

Doc context (Using IAM policy conditions for fine-grained access control): you write an IAM permissions policy specifying conditions (e.g. `dynamodb:LeadingKeys`) that let a user access only the items whose partition key matches their identity, then attach it to users/groups/roles.

**Flashcard-safe statement:** `dynamodb:LeadingKeys` is the IAM condition key for DynamoDB fine-grained (item-level) access control — it limits a principal to items whose partition key value matches an allowed value (often the caller's user ID). Related keys include `dynamodb:Attributes` (attribute-level) and `dynamodb:Select`.

Source:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html

---

## Summary Table

| # | Fact | Verdict |
|---|------|---------|
| 1 | `aws sts decode-authorization-message` / `DecodeAuthorizationMessage` / `sts:DecodeAuthorizationMessage` | CONFIRMED |
| 2 | Catch/Retry supported by Task + Parallel + **Map** (NOT only Task & Parallel) | CONFIRMED (Map DOES support both) |
| 3 | BatchGetItem: 100 items AND 16 MB; returns `UnprocessedKeys` | CONFIRMED |
| 4 | Function URL auth: only `AWS_IAM` and `NONE` | CONFIRMED |
| 5 | GetSessionToken supports MFA for existing IAM user | CONFIRMED |
| 6 | AssumeRole also supports MFA (`SerialNumber` + `TokenCode`) | CONFIRMED |
| 7 | Scan sequential by default; parallel via `Segment` / `TotalSegments` | CONFIRMED |
| 8 | `dynamodb:LeadingKeys` = fine-grained access by partition key | CONFIRMED |

## Note on tooling
The dedicated AWS docs MCP tools (search_documentation / read_documentation / read_sections / recommend) were not available in this environment. Findings were gathered via web_search + web_fetch restricted to official `docs.aws.amazon.com` pages, and key claims (Step Functions error handling, AssumeRole MFA parameters) were verified by reading the full official pages directly.
