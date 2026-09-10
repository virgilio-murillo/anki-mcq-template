# DVA-C02 examen_practica.txt - Temas, trazabilidad y estado

Pipeline: parse 65 preguntas -> extraccion de temas (Bedrock Claude Sonnet 4.5) -> dedup en 2 capas (embeddings Titan v2 + juicio Claude) contra las 188 tarjetas existentes de DVA-C02::* -> consolidacion de temas NEW entre si -> generacion de tarjetas para el deck DVA-C02::09.

- Temas extraidos: 176
- YA ESTUDIADOS (COVERED): 24
- NUEVOS (NEW): 152
- Tarjetas creadas en DVA-C02::09 (tras consolidar): 129

Leyenda: cada tema muestra [id] nombre (servicio), su estado, y para los NEW la tarjeta del deck 09 (card_key) donde quedo.

## Pregunta 1
- **[t001] DynamoDB Streams as a Lambda event source for change data capture** (DynamoDB) - _NUEVO_ (cos=0.471, LLM=NEW)
  - DynamoDB Streams capture item-level changes in a table and can trigger Lambda functions in near real-time, enabling immediate notification of data modifications without polling or scheduled scans.
  - -> tarjeta deck09: `dva09-2f719638` (tema canonico: DynamoDB Streams as a Lambda event source for change data capture)
- **[t002] Event-driven vs polling architectures for change detection** (Lambda) - _NUEVO_ (cos=0.35, LLM=NEW)
  - Event-driven architectures using streams or triggers detect changes immediately as they occur, while scheduled polling introduces latency and inefficiency by periodically scanning for changes at fixed intervals.
  - -> tarjeta deck09: `dva09-6109b7e6` (tema canonico: Event-driven architecture vs polling for change detection)
- **[t003] RDS database trigger limitations for Lambda invocation** (RDS) - _NUEVO_ (cos=0.363, LLM=NEW)
  - Standard RDS database engines (PostgreSQL, MySQL) cannot directly invoke Lambda functions via database triggers, unlike Aurora MySQL which supports native Lambda integration.
  - -> tarjeta deck09: `dva09-127cffe3` (tema canonico: RDS database trigger limitations for Lambda invocation)

## Pregunta 2
- **[t004] Lambda functions as SNS topic subscribers for event-driven architectures** (AWS Lambda) - _NUEVO_ (cos=0.549, LLM=NEW)
  - AWS Lambda functions can directly subscribe to Amazon SNS topics to receive and process events in a serverless, event-driven manner, eliminating the need for compute instances to poll or listen for messages.
  - -> tarjeta deck09: `dva09-9d8a76f6` (tema canonico: Lambda functions as SNS topic subscribers for event-driven architectures)
- **[t005] Serverless vs server-based compute for event processing** (AWS Lambda) - _NUEVO_ (cos=0.427, LLM=NEW)
  - Serverless architectures use managed services like Lambda that automatically scale and require no server provisioning, while EC2-based solutions require managing instances and are not considered serverless even when used with event services like SQS or SNS.
  - -> tarjeta deck09: `dva09-f1a3c82a` (tema canonico: Serverless vs server-based compute for event processing)
- **[t006] Event-driven vs request-driven invocation patterns** (Amazon SNS) - _NUEVO_ (cos=0.456, LLM=NEW)
  - Event-driven architectures use asynchronous event sources (like SNS publishing to Lambda) where events trigger function execution, while request-driven patterns (like API Gateway synchronous invocations) require explicit API calls and do not constitute event-driven design.
  - -> tarjeta deck09: `dva09-10b7b912` (tema canonico: Event-driven vs request-driven invocation patterns)

## Pregunta 3
- **[t007] DynamoDB Global Secondary Index (GSI) for alternative query patterns** (DynamoDB) - _YA ESTUDIADO_ (cos=0.705, LLM=COVERED)
  - GSIs allow querying DynamoDB tables using different partition and sort keys than the base table, enabling efficient queries on non-key attributes. GSIs can be created after table creation, unlike Local Secondary Indexes.
  - Motivo: Card [4] already teaches that GSIs use different partition/sort keys than the base table for alternative query patterns, and card [5] covers that GSIs can be created after table creation, which are the core concepts of the study topic.
- **[t008] DynamoDB Query vs Scan operations for data retrieval efficiency** (DynamoDB) - _YA ESTUDIADO_ (cos=0.882, LLM=COVERED)
  - Query operations require a partition key and optionally a sort key for efficient targeted retrieval, while Scan operations read every item in the table and should be avoided for large tables due to performance and cost implications.
  - Motivo: Card [1] already teaches the core distinction that Scan reads the entire table (costly/inefficient) while Query searches by key (efficient), which is the exact same concept as the candidate topic.
- **[t009] DynamoDB Local Secondary Index (LSI) creation constraints** (DynamoDB) - _YA ESTUDIADO_ (cos=0.739, LLM=COVERED)
  - LSIs must be created at table creation time and share the same partition key as the base table but allow a different sort key. They cannot be added to existing tables.
  - Motivo: Card [1] already teaches that LSIs must be created at table creation time and cannot be added later, which is the core constraint being tested in the candidate topic.

## Pregunta 4
- **[t010] DynamoDB eventually consistent vs strongly consistent reads RCU consumption** (DynamoDB) - _YA ESTUDIADO_ (cos=0.687, LLM=COVERED)
  - Eventually consistent reads consume half the RCUs of strongly consistent reads (0.5 RCU vs 1 RCU per 4KB). When stale data is tolerable, eventually consistent reads minimize RCU costs.
  - Motivo: Card [2] already teaches that 1 RCU equals 1 strongly consistent read or 2 eventually consistent reads (0.5 RCU each) for items up to 4KB, which is the exact same core concept about RCU consumption differences.
- **[t011] DynamoDB transactional reads RCU consumption** (DynamoDB) - _YA ESTUDIADO_ (cos=0.729, LLM=COVERED)
  - Transactional reads consume 2x the RCUs of strongly consistent reads (2 RCUs per 4KB) and are only needed for ACID guarantees across multiple items or tables, not for single-item reads.
  - Motivo: Card [4] already teaches that transactional operations in DynamoDB cost double (2x RCUs for reads, 2x WCUs for writes) compared to normal operations, which is the core concept of the study topic.
- **[t012] DynamoDB PartiQL query read consistency options** (DynamoDB) - _NUEVO_ (cos=0.54, LLM=NEW)
  - PartiQL queries in DynamoDB support both eventually consistent and strongly consistent reads with the same RCU consumption patterns as standard GetItem/Query operations.
  - -> tarjeta deck09: `dva09-477adb81` (tema canonico: DynamoDB PartiQL query read consistency options)

## Pregunta 5
- **[t013] Amazon Cognito Sync for cross-device user data synchronization** (Amazon Cognito) - _YA ESTUDIADO_ (cos=0.708, LLM=COVERED)
  - Cognito Sync enables synchronization of application-related user profile data across multiple devices and platforms using client libraries, allowing users to access the same data regardless of which device they use.
  - Motivo: Card [1] already teaches that Cognito Sync synchronizes application data across devices for a single user identity, which is the core concept of the study topic.
- **[t014] AWS DataSync use cases and limitations** (AWS DataSync) - _NUEVO_ (cos=0.579, LLM=NEW)
  - DataSync is designed for transferring data between on-premises storage systems and AWS storage services, not for synchronizing user data across client devices or mobile applications.
  - -> tarjeta deck09: `dva09-1f667ed7` (tema canonico: AWS DataSync use cases and limitations)
- **[t015] Application Load Balancer sticky sessions behavior** (Elastic Load Balancing) - _NUEVO_ (cos=0.693, LLM=NEW)
  - ALB sticky sessions bind a user's session to a specific target server for session persistence, but do not synchronize or share data across multiple devices or sessions.
  - -> tarjeta deck09: `dva09-aaae3072` (tema canonico: Application Load Balancer sticky sessions behavior)

## Pregunta 6
- **[t016] Amazon Cognito User Pool social identity provider (IdP) integration requirements** (Amazon Cognito) - _NUEVO_ (cos=0.708, LLM=NEW)
  - Social IdPs (Google, Facebook, Amazon, Apple) use OpenID Connect and require an app client ID and app client secret obtained from the social provider's developer console to integrate with Cognito User Pools.
  - -> tarjeta deck09: `dva09-aa41d56a` (tema canonico: Amazon Cognito User Pool social identity provider (IdP) integration requirements)
- **[t017] SAML vs OpenID Connect authentication protocols in Cognito** (Amazon Cognito) - _NUEVO_ (cos=0.496, LLM=NEW)
  - Social IdPs use OpenID Connect protocol requiring client ID and secret, while enterprise SAML IdPs use SAML metadata documents. These are distinct integration methods that cannot be interchanged.
  - -> tarjeta deck09: `dva09-77dbbc55` (tema canonico: SAML vs OpenID Connect authentication protocols in Cognito)

## Pregunta 7
- **[t018] CodeBuild custom Docker images for pre-installed dependencies** (CodeBuild) - _NUEVO_ (cos=0.295, LLM=NEW)
  - Custom CodeBuild images allow pre-installation of dependencies, tools, and packages in a Docker image, eliminating download and installation time during each build compared to downloading dependencies in the buildspec install phase.
  - -> tarjeta deck09: `dva09-b3ed16c9` (tema canonico: CodeBuild custom Docker images for pre-installed dependencies)
- **[t019] CodeBuild build time optimization strategies** (CodeBuild) - _NUEVO_ (cos=0.292, LLM=NEW)
  - Build time can be reduced through various methods (custom images, VPC endpoints to internal resources, S3-hosted dependencies), but pre-baking dependencies into custom Docker images provides the greatest time savings by eliminating repeated download and installation steps.
  - -> tarjeta deck09: `dva09-72c4c0db` (tema canonico: CodeBuild build time optimization strategies)
- **[t020] CodeBuild VPC configuration for private resource access** (CodeBuild) - _NUEVO_ (cos=0.384, LLM=NEW)
  - VPC-enabled CodeBuild projects can access resources within a VPC such as internally hosted package managers or EC2 instances, reducing external internet dependency but still requiring download time during builds.
  - -> tarjeta deck09: `dva09-957f8b7e` (tema canonico: CodeBuild VPC configuration for private resource access)

## Pregunta 8
- **[t021] SNS subscription dead-letter queue (DLQ) for failed message deliveries** (SNS) - _NUEVO_ (cos=0.201, LLM=NEW)
  - An Amazon SQS queue can be configured as a dead-letter queue (DLQ) for an SNS subscription to capture and store messages that fail delivery to the subscription endpoint, preventing message loss during outages or misconfigurations.
  - -> tarjeta deck09: `dva09-bd8cd220` (tema canonico: SNS subscription dead-letter queues (DLQs) for failed message delivery)
- **[t022] SNS delivery policies vs dead-letter queues for message persistence** (SNS) - _NUEVO_ (cos=0.258, LLM=NEW)
  - SNS delivery policies control retry behavior with time-limited attempts that eventually exhaust, while dead-letter queues provide persistent storage for failed messages beyond retry exhaustion, making DLQs the solution for long-term message preservation during extended outages.
  - -> tarjeta deck09: `dva09-bd8cd220` (tema canonico: SNS subscription dead-letter queues (DLQs) for failed message delivery)
- **[t023] Lambda destinations vs SNS dead-letter queues** (SNS) - _NUEVO_ (cos=0.381, LLM=NEW)
  - Failure destinations are a feature of AWS Lambda asynchronous invocations, not SNS topics. SNS uses dead-letter queues (DLQs) attached to subscriptions to handle delivery failures, not failure destinations at the topic level.
  - -> tarjeta deck09: `dva09-9b77e6fa` (tema canonico: Lambda destinations vs SNS dead-letter queues)

## Pregunta 9
- **[t024] Lambda execution role IAM permissions for DynamoDB write operations** (AWS Lambda) - _NUEVO_ (cos=0.398, LLM=NEW)
  - Lambda functions require an execution role with explicit IAM permissions (e.g., dynamodb:PutItem, dynamodb:BatchWriteItem) to write to DynamoDB tables. AccessDenied errors indicate missing IAM permissions, not capacity or throttling issues.
  - -> tarjeta deck09: `dva09-1222a287` (tema canonico: Lambda execution role IAM permissions for DynamoDB write operations)
- **[t025] DynamoDB error types: AccessDeniedException vs ProvisionedThroughputExceededException vs ThrottlingException** (Amazon DynamoDB) - _NUEVO_ (cos=0.405, LLM=NEW)
  - AccessDeniedException indicates IAM permission issues, ProvisionedThroughputExceededException indicates exhausted WCU/RCU capacity, and ThrottlingException indicates API rate limit exceeded. Each error type has distinct causes and requires different remediation approaches.
  - -> tarjeta deck09: `dva09-593330f4` (tema canonico: DynamoDB error types and their causes)

## Pregunta 10
- **[t026] Elastic Beanstalk Immutable deployment policy** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.534, LLM=NEW)
  - Immutable deployments launch a completely new set of EC2 instances with the new application version, then terminate old instances after successful deployment, ensuring zero downtime and easy rollback.
  - -> tarjeta deck09: `dva09-702a71ef` (tema canonico: Elastic Beanstalk deployment policies comparison and characteristics)
- **[t027] Elastic Beanstalk Blue/Green deployment strategy** (AWS Elastic Beanstalk) - _YA ESTUDIADO_ (cos=0.585, LLM=COVERED)
  - Blue/green deployments create a separate complete environment with new instances for the new application version, allowing testing before swapping CNAMEs to redirect traffic from the old (blue) to new (green) environment.
  - Motivo: Card [1] already teaches the Blue/Green deployment strategy in Elastic Beanstalk, including the concept of creating a separate environment for the new version and the ability to swap/redirect traffic and quickly revert if needed.
- **[t028] Elastic Beanstalk Rolling deployment policies distinction** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.453, LLM=NEW)
  - Rolling and Rolling with additional batch deployments update existing instances in batches rather than launching entirely new instances, with the additional batch variant temporarily adding capacity during deployment.
  - -> tarjeta deck09: `dva09-702a71ef` (tema canonico: Elastic Beanstalk deployment policies comparison and characteristics)

## Pregunta 11
- **[t029] ACM certificate attachment to Application Load Balancer for HTTPS termination** (AWS Certificate Manager) - _NUEVO_ (cos=0.52, LLM=NEW)
  - ACM certificates can be directly attached to ALB listeners via the AWS Console to enable HTTPS termination at the load balancer level, eliminating the need to manage certificates on individual EC2 instances.
  - -> tarjeta deck09: `dva09-92e52146` (tema canonico: Application Load Balancer SSL/TLS termination with ACM certificates)
- **[t030] ACM certificate export limitations and supported integrations** (AWS Certificate Manager) - _NUEVO_ (cos=0.581, LLM=NEW)
  - ACM certificates cannot be exported (private keys remain in ACM) and cannot be directly installed on EC2 instances unless using AWS Nitro Enclaves. ACM certificates are designed for integrated AWS services like ALB, CloudFront, and API Gateway.
  - -> tarjeta deck09: `dva09-cc7a25b6` (tema canonico: ACM certificate export limitations and supported integrations)
- **[t031] Application Load Balancer SSL/TLS termination architecture** (Elastic Load Balancing) - _NUEVO_ (cos=0.479, LLM=NEW)
  - ALB performs SSL/TLS termination by decrypting HTTPS traffic using ACM certificates at the load balancer layer, then forwarding traffic to backend EC2 instances (typically over HTTP), offloading certificate management from individual instances.
  - -> tarjeta deck09: `dva09-92e52146` (tema canonico: Application Load Balancer SSL/TLS termination with ACM certificates)

## Pregunta 12
- **[t032] AWS Secrets Manager automatic rotation for database credentials** (AWS Secrets Manager) - _NUEVO_ (cos=0.482, LLM=NEW)
  - Secrets Manager supports automatic rotation of database credentials with KMS encryption at rest, unlike Parameter Store which requires manual rotation or external automation.
  - -> tarjeta deck09: `dva09-606e5cf3` (tema canonico: AWS Secrets Manager automatic rotation for database credentials)
- **[t033] Systems Manager Parameter Store SecureString vs String parameter types** (AWS Systems Manager Parameter Store) - _NUEVO_ (cos=0.26, LLM=NEW)
  - SecureString parameters support KMS encryption for sensitive data, while String parameters store plain text without encryption, but Parameter Store lacks native automatic rotation capabilities.
  - -> tarjeta deck09: `dva09-307ee5c3` (tema canonico: Systems Manager Parameter Store SecureString vs String parameter types)
- **[t034] Lambda IAM permissions for Secrets Manager secret retrieval** (AWS Lambda) - _NUEVO_ (cos=0.39, LLM=NEW)
  - Lambda functions require secretsmanager:GetSecretValue permission on the secret ARN and kms:Decrypt permission on the KMS key ARN to retrieve and decrypt secrets.
  - -> tarjeta deck09: `dva09-f75dc1dc` (tema canonico: Lambda IAM permissions for Secrets Manager secret retrieval)

## Pregunta 13
- **[t035] AWS Encryption SDK vs S3 encryption client compatibility** (AWS Encryption SDK) - _NUEVO_ (cos=0.476, LLM=NEW)
  - The AWS Encryption SDK and S3 encryption client produce incompatible ciphertext formats and cannot decrypt each other's encrypted data. Both encryption and decryption operations must use the same SDK (either both use Encryption SDK or both use S3 encryption client).
  - -> tarjeta deck09: `dva09-c6652854` (tema canonico: AWS Encryption SDK vs S3 encryption client compatibility)
- **[t036] AWS Encryption SDK cross-language compatibility** (AWS Encryption SDK) - _NUEVO_ (cos=0.383, LLM=NEW)
  - The AWS Encryption SDK supports cross-language encryption and decryption, meaning data encrypted with the Encryption SDK in one language (e.g., Java) can be decrypted using the Encryption SDK in another language (e.g., Python), as long as both use the same SDK.
  - -> tarjeta deck09: `dva09-74959814` (tema canonico: AWS Encryption SDK cross-language compatibility)

## Pregunta 14
- **[t037] CodeDeploy agent InvalidSignatureException due to time skew** (AWS CodeDeploy) - _NUEVO_ (cos=0.352, LLM=NEW)
  - CodeDeploy agent requires accurate system time on EC2 instances to validate request signatures. Time drift or incorrect date/time settings cause InvalidSignatureException errors because the signature timestamp doesn't match the instance's clock.
  - -> tarjeta deck09: `dva09-fc806b4e` (tema canonico: CodeDeploy agent InvalidSignatureException due to time skew)
- **[t038] AWS API request signature validation and time synchronization** (AWS IAM) - _NUEVO_ (cos=0.353, LLM=NEW)
  - AWS API requests use signature version 4 signing with timestamps. If an EC2 instance's system clock is skewed beyond the acceptable threshold (typically 5 minutes), AWS services reject requests with InvalidSignatureException because the signature appears expired or not yet valid.
  - -> tarjeta deck09: `dva09-b3590daa` (tema canonico: AWS API request signature validation and time synchronization)

## Pregunta 15
- **[t039] CloudWatch agent for hybrid log collection from on-premises and EC2** (CloudWatch) - _NUEVO_ (cos=0.571, LLM=NEW)
  - The CloudWatch agent can be deployed to both on-premises servers and EC2 instances to collect and send logs to CloudWatch Logs for centralized storage and monitoring in hybrid environments.
  - -> tarjeta deck09: `dva09-31d5ea5f` (tema canonico: CloudWatch agent for hybrid log collection with minimal effort)
- **[t040] CloudWatch Logs console for log visualization and metric filters** (CloudWatch) - _NUEVO_ (cos=0.474, LLM=NEW)
  - CloudWatch console provides native visualization capabilities for logs and allows creating metric filters to graph metrics derived from log events without requiring additional services or custom development.
  - -> tarjeta deck09: `dva09-235efaf7` (tema canonico: CloudWatch Logs console for log visualization and metric filters)
- **[t041] Service selection for log aggregation with minimal developer effort** (CloudWatch) - _NUEVO_ (cos=0.496, LLM=NEW)
  - CloudWatch agent-based log collection requires minimal code changes compared to rewriting applications to push logs to S3, Redshift, or QuickSight SPICE, making it the lowest-effort solution for hybrid log aggregation.
  - -> tarjeta deck09: `dva09-31d5ea5f` (tema canonico: CloudWatch agent for hybrid log collection with minimal effort)

## Pregunta 16
- **[t042] DynamoDB Streams as a Lambda event source for change notifications** (DynamoDB) - _NUEVO_ (cos=0.495, LLM=NEW)
  - DynamoDB Streams captures item-level modifications in near real-time and can trigger Lambda functions automatically when table data changes, enabling event-driven architectures without polling or modifying the application writing to DynamoDB.
  - -> tarjeta deck09: `dva09-2f719638` (tema canonico: DynamoDB Streams as a Lambda event source for change data capture)
- **[t043] Event-driven architecture vs polling for data changes** (General Architecture) - _NUEVO_ (cos=0.381, LLM=NEW)
  - Event-driven architectures using streams and triggers respond immediately to data changes, while polling introduces latency and inefficiency by repeatedly checking for changes at fixed intervals.
  - -> tarjeta deck09: `dva09-6109b7e6` (tema canonico: Event-driven architecture vs polling for change detection)
- **[t044] Serverless compute options: Lambda vs ECS Fargate vs EC2** (Lambda) - _NUEVO_ (cos=0.548, LLM=NEW)
  - Lambda is fully serverless and event-driven with automatic scaling, while ECS on Fargate requires container management and EC2 requires instance management, making Lambda the most serverless option for event processing.
  - -> tarjeta deck09: `dva09-f15fc4c6` (tema canonico: Serverless compute options: Lambda vs ECS Fargate vs EC2)

## Pregunta 17
- **[t045] Cognito Identity Pool attribute-based access control (ABAC) using Principal Tags** (Amazon Cognito) - _NUEVO_ (cos=0.471, LLM=NEW)
  - Identity pools can pass user pool custom attributes as Principal Tags to IAM roles, enabling ABAC where a single IAM role uses conditions like ${aws:PrincipalTag/attribute} to dynamically control resource access based on user attributes rather than assigning different roles per user group.
  - -> tarjeta deck09: `dva09-f78f07f2` (tema canonico: Cognito Identity Pool attribute-based access control (ABAC) using Principal Tags)
- **[t046] S3 object tag-based access control with IAM condition keys** (Amazon S3) - _NUEVO_ (cos=0.54, LLM=NEW)
  - IAM policies can use the s3:ExistingObjectTag/<tag-key> condition key to grant access to S3 objects based on their tags, enabling fine-grained access control where users can only access objects whose tags match their principal attributes.
  - -> tarjeta deck09: `dva09-fea007f3` (tema canonico: S3 object tag-based access control with IAM condition keys)
- **[t047] Cognito Identity Pool vs User Pool IAM role association** (Amazon Cognito) - _NUEVO_ (cos=0.806, LLM=NEW)
  - IAM roles are associated with identity pools (not user pools directly), and identity pools can use either role-based access control (multiple roles selected by rules) or attribute-based access control (single role with policy conditions based on principal tags from user pool attributes).
  - -> tarjeta deck09: `dva09-61e9d459` (tema canonico: Cognito Identity Pool vs User Pool IAM role association)

## Pregunta 18
- **[t048] Lambda provisioned concurrency for reducing cold start latency** (AWS Lambda) - _NUEVO_ (cos=0.562, LLM=NEW)
  - Provisioned concurrency keeps Lambda functions initialized and ready to respond immediately, eliminating cold start delays including database connection initialization time, without adding infrastructure.
  - -> tarjeta deck09: `dva09-f12d0960` (tema canonico: Lambda provisioned concurrency for reducing cold start latency)
- **[t049] Lambda function handler best practices for external connections** (AWS Lambda) - _NUEVO_ (cos=0.399, LLM=NEW)
  - Initialize SDK clients and database connections outside the Lambda function handler (in global scope) so they persist across invocations and are reused, reducing connection establishment overhead on each invocation.
  - -> tarjeta deck09: `dva09-e271cd40` (tema canonico: Lambda function handler best practices for external connections)
- **[t050] API Gateway caching limitations for write operations** (Amazon API Gateway) - _NUEVO_ (cos=0.693, LLM=NEW)
  - API Gateway caching only applies to GET requests and reduces read latency but does not improve write operation latency or Lambda integration time for non-cacheable requests.
  - -> tarjeta deck09: `dva09-e714f75f` (tema canonico: API Gateway caching limitations for write operations)

## Pregunta 19
- **[t051] ALB Availability Zone configuration for traffic distribution** (Elastic Load Balancing) - _NUEVO_ (cos=0.3, LLM=NEW)
  - Application Load Balancers must have Availability Zones explicitly enabled to route traffic to registered targets in those zones. Even if instances are registered with the ALB, they will not receive traffic if their Availability Zone is not enabled on the load balancer.
  - -> tarjeta deck09: `dva09-7fbeb29b` (tema canonico: ALB Availability Zone configuration for traffic distribution)
- **[t052] ALB target registration vs Availability Zone enablement** (Elastic Load Balancing) - _NUEVO_ (cos=0.26, LLM=NEW)
  - Target registration with an ALB is separate from Availability Zone enablement. Instances can be successfully registered as targets but remain idle if the ALB is not configured to route traffic to their Availability Zone.
  - -> tarjeta deck09: `dva09-0ad9bb88` (tema canonico: ALB target registration vs Availability Zone enablement)
- **[t053] Auto Scaling group distribution across Availability Zones with ALB** (EC2 Auto Scaling) - _NUEVO_ (cos=0.298, LLM=NEW)
  - When Auto Scaling groups launch instances across multiple Availability Zones, the associated ALB must have those same Availability Zones enabled to distribute traffic to all instances, otherwise instances in disabled zones remain idle despite being healthy and registered.
  - -> tarjeta deck09: `dva09-9cb1fbb4` (tema canonico: Auto Scaling group distribution across Availability Zones with ALB)

## Pregunta 20
- **[t054] Cognito Identity Pools vs User Pools for AWS credential vending** (Amazon Cognito) - _YA ESTUDIADO_ (cos=0.912, LLM=COVERED)
  - Identity pools provide temporary AWS credentials for federated identities (including web identity providers), while user pools only provide user authentication and management without AWS credentials.
  - Motivo: Card [1] already teaches the core distinction that User Pools authenticate and return tokens while Identity Pools provide AWS credentials, which is exactly the concept being tested.
- **[t055] Cognito Identity Pool enhanced authflow API sequence: GetId then GetCredentialsForIdentity** (Amazon Cognito) - _NUEVO_ (cos=0.563, LLM=NEW)
  - To obtain AWS credentials from an OpenID token, call GetId API with the token to get a Cognito ID, then call GetCredentialsForIdentity API with that Cognito ID to receive temporary AWS credentials.
  - -> tarjeta deck09: `dva09-c9784223` (tema canonico: Cognito Identity Pool enhanced authflow API sequence: GetId then GetCredentialsForIdentity)
- **[t056] Web identity federation with Cognito Identity Pools for mobile apps** (Amazon Cognito) - _YA ESTUDIADO_ (cos=0.633, LLM=COVERED)
  - Mobile apps can use external identity providers (Google, Facebook, etc.) to obtain OpenID tokens, then exchange them for AWS credentials via Cognito Identity Pools to access AWS services like DynamoDB.
  - Motivo: Card [1] already teaches that Cognito Identity Pools exchange social IdP credentials (Facebook, Google) for temporary AWS credentials to access services, which is the exact core concept of web identity federation with Cognito Identity Pools.

## Pregunta 21
- **[t057] Lambda deployment package contents for Java runtime** (AWS Lambda) - _NUEVO_ (cos=0.45, LLM=NEW)
  - A Lambda deployment package (.zip or .jar) must include compiled application code and application dependencies, but does NOT include the runtime environment (provided by Lambda), execution role (IAM resource configured separately), or event source references (external triggers).
  - -> tarjeta deck09: `dva09-265b3f1b` (tema canonico: Lambda deployment package contents for Java runtime)
- **[t058] Lambda managed runtime vs custom dependencies** (AWS Lambda) - _NUEVO_ (cos=0.498, LLM=NEW)
  - Lambda provides and manages the runtime environment (e.g., Java runtime), so developers only need to package their compiled code and custom dependencies, not the base runtime itself.
  - -> tarjeta deck09: `dva09-fb83ee6b` (tema canonico: Lambda managed runtime vs custom dependencies)
- **[t059] Lambda execution role configuration vs deployment package** (AWS Lambda) - _NUEVO_ (cos=0.38, LLM=NEW)
  - The Lambda execution role is an IAM role configured when creating/updating the function to grant AWS service permissions, and is NOT included in the deployment package which only contains code artifacts.
  - -> tarjeta deck09: `dva09-4e297e8c` (tema canonico: Lambda execution role configuration vs deployment package)

## Pregunta 22
- **[t060] AWS Secrets Manager automatic rotation for database credentials** (AWS Secrets Manager) - _NUEVO_ (cos=0.505, LLM=NEW)
  - Secrets Manager natively supports automatic rotation of database credentials on a schedule, unlike Parameter Store which requires custom Lambda functions for rotation. This is the recommended service for storing and rotating RDS credentials.
  - -> tarjeta deck09: `dva09-606e5cf3` (tema canonico: AWS Secrets Manager automatic rotation for database credentials)
- **[t061] Systems Manager Parameter Store vs Secrets Manager for credential storage** (AWS Systems Manager Parameter Store) - _NUEVO_ (cos=0.299, LLM=NEW)
  - Parameter Store can store secrets but does not have built-in automatic rotation capabilities, while Secrets Manager provides both secure storage and native automatic rotation for credentials. Parameter Store requires custom Lambda functions to implement rotation.
  - -> tarjeta deck09: `dva09-b7eab8a0` (tema canonico: AWS Secrets Manager vs Systems Manager Parameter Store for secret rotation)
- **[t062] AWS KMS key encryption vs credential management services** (AWS KMS) - _NUEVO_ (cos=0.523, LLM=NEW)
  - KMS encrypts data and manages encryption keys but does not store, distribute, or rotate application credentials. Credential management requires Secrets Manager or Parameter Store, not KMS alone.
  - -> tarjeta deck09: `dva09-e18af4c6` (tema canonico: AWS KMS key encryption vs credential management services)

## Pregunta 23
- **[t063] CloudWatch Logs encryption with KMS customer managed keys via AWS CLI** (CloudWatch Logs) - _NUEVO_ (cos=0.455, LLM=NEW)
  - CloudWatch Logs log groups can only be encrypted with KMS customer managed keys using the AWS CLI (associate-kms-key or create-log-group commands), not through the AWS Management Console.
  - -> tarjeta deck09: `dva09-e0d289ee` (tema canonico: CloudWatch Logs encryption with KMS customer managed keys via AWS CLI)
- **[t064] KMS symmetric vs asymmetric key types for CloudWatch Logs encryption** (AWS KMS) - _NUEVO_ (cos=0.433, LLM=NEW)
  - CloudWatch Logs encryption requires symmetric KMS customer managed keys; asymmetric keys are not supported for log group encryption.
  - -> tarjeta deck09: `dva09-e678f259` (tema canonico: KMS symmetric vs asymmetric key types for CloudWatch Logs encryption)
- **[t065] CloudWatch Logs log group encryption modification without deletion** (CloudWatch Logs) - _NUEVO_ (cos=0.426, LLM=NEW)
  - Existing CloudWatch Logs log groups can be modified to add KMS encryption using the associate-kms-key CLI command without requiring deletion and recreation of the log group.
  - -> tarjeta deck09: `dva09-e0d289ee` (tema canonico: CloudWatch Logs encryption with KMS customer managed keys via AWS CLI)

## Pregunta 24
- **[t066] STS decode-authorization-message for encoded IAM authorization failures** (AWS STS) - _YA ESTUDIADO_ (cos=0.821, LLM=COVERED)
  - When an AWS API call fails with an UnauthorizedOperation error and returns an encoded authorization failure message, use the AWS STS decode-authorization-message command to decode the message and reveal detailed information about why the request was denied.
  - Motivo: Card [1] already teaches the exact same concept: using 'sts decode-authorization-message' to decode the encoded authorization failure message returned with UnauthorizedOperation errors.
- **[t067] IAM authorization error troubleshooting with encoded messages** (IAM) - _YA ESTUDIADO_ (cos=0.685, LLM=COVERED)
  - Distinguish between encrypted content (requiring KMS decrypt) and encoded authorization messages (requiring STS decode-authorization-message). Encoded messages are specifically returned by AWS when authorization fails and contain diagnostic information about the denial reason.
  - Motivo: Card [1] already teaches the core concept: when AWS returns an UnauthorizedOperation error with an encoded message, use STS decode-authorization-message to decode it—this is the exact same IAM authorization troubleshooting technique being tested.

## Pregunta 25
- **[t068] AWS X-Ray distributed tracing for microservices** (AWS X-Ray) - _NUEVO_ (cos=0.637, LLM=NEW)
  - X-Ray provides distributed tracing capabilities to track and analyze user requests as they travel through microservices architectures, identifying performance bottlenecks and issues across service boundaries. Unlike CloudWatch metrics/logs or ALB metrics, X-Ray specifically traces request paths end-to-end across distributed services.
  - -> tarjeta deck09: `dva09-0bf5a458` (tema canonico: AWS X-Ray distributed tracing for microservices and serverless architectures)
- **[t069] X-Ray daemon deployment on Amazon ECS** (AWS X-Ray) - _NUEVO_ (cos=0.548, LLM=NEW)
  - The X-Ray daemon must run as a sidecar container alongside application containers in ECS to collect trace data from instrumented applications. This requires creating a Docker image with the X-Ray daemon and configuring it to run in the ECS task definition.
  - -> tarjeta deck09: `dva09-0c1f761b` (tema canonico: X-Ray daemon deployment on Amazon ECS)
- **[t070] CloudWatch vs X-Ray for application observability** (AWS X-Ray) - _NUEVO_ (cos=0.474, LLM=NEW)
  - CloudWatch collects metrics and logs for monitoring resource utilization and application output, but does not provide distributed tracing. X-Ray is specifically designed for tracing request flows across distributed services to identify performance degradation patterns and service dependencies.
  - -> tarjeta deck09: `dva09-881c9cc3` (tema canonico: CloudWatch vs X-Ray for distributed tracing and performance analysis)

## Pregunta 26
- **[t071] DynamoDB provisioned vs on-demand capacity modes for unpredictable workloads** (DynamoDB) - _NUEVO_ (cos=0.457, LLM=NEW)
  - On-demand mode automatically scales to accommodate unpredictable traffic spikes without ProvisionedThroughputExceededException errors, while provisioned mode with Auto Scaling may not scale fast enough for rapid spikes despite having Auto Scaling enabled.
  - -> tarjeta deck09: `dva09-60490add` (tema canonico: DynamoDB provisioned vs on-demand capacity modes for unpredictable workloads)
- **[t072] DynamoDB ProvisionedThroughputExceededException error handling** (DynamoDB) - _NUEVO_ (cos=0.493, LLM=NEW)
  - This exception occurs when read/write requests exceed the provisioned capacity units (RCUs/WCUs) for a table or index, indicating the need to either increase provisioned capacity, implement exponential backoff retries, or switch to on-demand mode.
  - -> tarjeta deck09: `dva09-a8c6e6d7` (tema canonico: DynamoDB ProvisionedThroughputExceededException)

## Pregunta 27
- **[t073] Amazon Cognito for web application user authentication and identity management at scale** (Amazon Cognito) - _YA ESTUDIADO_ (cos=0.65, LLM=COVERED)
  - Amazon Cognito provides scalable user identity management for web applications, generating temporary AWS credentials that allow authenticated users to directly access AWS services like DynamoDB without creating individual IAM users.
  - Motivo: Card [1] already teaches that Cognito Identity Pool delivers temporary AWS credentials for authenticated users to access AWS services, which is the core concept of the study topic.
- **[t074] IAM users vs Amazon Cognito for application user authentication** (IAM) - _NUEVO_ (cos=0.592, LLM=NEW)
  - IAM users are intended for AWS account access and have service quotas (default 5,000 per account), making them unsuitable for authenticating application end-users at scale, whereas Amazon Cognito is purpose-built for application user authentication supporting millions of users.
  - -> tarjeta deck09: `dva09-47b9ca99` (tema canonico: IAM users vs Amazon Cognito for application user authentication)
- **[t075] Amazon Cognito temporary credentials for direct AWS service access from browser-based applications** (Amazon Cognito) - _NUEVO_ (cos=0.771, LLM=NEW)
  - Amazon Cognito Identity Pools provide temporary, limited-privilege AWS credentials to authenticated users, enabling browser-based applications using AWS SDK for JavaScript to directly access services like DynamoDB without backend servers.
  - -> tarjeta deck09: `dva09-0b8e9961` (tema canonico: Amazon Cognito temporary credentials for direct AWS service access from browser-based applications)

## Pregunta 28
- **[t076] S3 Event Notifications to invoke Lambda functions** (Amazon S3) - _NUEVO_ (cos=0.811, LLM=NEW)
  - S3 Event Notifications can trigger Lambda functions automatically when specific S3 events occur (such as object creation, deletion, or modification). This is the primary mechanism for event-driven processing of S3 objects.
  - -> tarjeta deck09: `dva09-718ae417` (tema canonico: S3 Event Notifications to invoke Lambda functions)
- **[t077] S3 feature capabilities and use cases** (Amazon S3) - _NUEVO_ (cos=0.488, LLM=NEW)
  - Understanding that S3 Storage Lens is for analytics/visibility, S3 Object Lock is for retention/compliance, and S3 Lifecycle rules are for storage class transitions and expiration—none of these can invoke Lambda functions or serve as event triggers.
  - -> tarjeta deck09: `dva09-068f74d9` (tema canonico: S3 feature capabilities and use cases)

## Pregunta 29
- **[t078] Kinesis Data Streams PutRecords vs PutRecord API for batch ingestion** (Amazon Kinesis Data Streams) - _NUEVO_ (cos=0.605, LLM=NEW)
  - PutRecords API allows batching multiple records in a single API call (up to 500 records or 5 MB), significantly reducing network overhead and CPU usage compared to individual PutRecord calls, thereby increasing throughput for high-volume data ingestion.
  - -> tarjeta deck09: `dva09-c6ca69bf` (tema canonico: Kinesis Data Streams PutRecords vs PutRecord API for batch ingestion)
- **[t079] Kinesis Client Library (KCL) purpose and limitations** (Amazon Kinesis Data Streams) - _NUEVO_ (cos=0.413, LLM=NEW)
  - KCL is designed for consuming and processing data from Kinesis streams (consumer-side), not for producing/putting records into streams. It handles shard-to-worker relationships for readers but does not provide producer functionality.
  - -> tarjeta deck09: `dva09-3a6a167c` (tema canonico: Kinesis Client Library (KCL) purpose and limitations)

## Pregunta 30
- **[t080] IAM role trust policy vs access policy for AssumeRole operations** (IAM) - _NUEVO_ (cos=0.462, LLM=NEW)
  - Trust policies control WHO can assume a role (which principals are allowed to call sts:AssumeRole), while access policies control WHAT the role can do after being assumed. An sts:AssumeRoleWithWebIdentity error indicates the trust policy is misconfigured, not the access policy.
  - -> tarjeta deck09: `dva09-d793c42a` (tema canonico: IAM role trust policy vs access policy for AssumeRole operations)
- **[t081] Cognito Identity Pool authenticated role trust policy configuration** (Amazon Cognito) - _NUEVO_ (cos=0.504, LLM=NEW)
  - When using Cognito web identity federation, the authenticated IAM role's trust policy must explicitly allow cognito-identity.amazonaws.com as the principal with sts:AssumeRoleWithWebIdentity action and proper conditions (like StringEquals for cognito-identity.amazonaws.com:aud matching the identity pool ID).
  - -> tarjeta deck09: `dva09-0d4d0501` (tema canonico: Cognito Identity Pool authenticated role trust policy configuration)
- **[t082] STS AssumeRoleWithWebIdentity authentication flow sequence** (AWS STS) - _NUEVO_ (cos=0.57, LLM=NEW)
  - The AssumeRoleWithWebIdentity call occurs AFTER successful authentication with the identity provider. Errors at the AssumeRole step indicate trust policy issues, not authentication failures which would occur earlier in the flow.
  - -> tarjeta deck09: `dva09-f84bc31a` (tema canonico: STS AssumeRoleWithWebIdentity authentication flow sequence)

## Pregunta 31
- **[t083] CodeBuild buildspec.yml default file location** (AWS CodeBuild) - _NUEVO_ (cos=0.392, LLM=NEW)
  - CodeBuild expects the buildspec.yml file to be located in the root of the source directory by default, though an alternate location can be specified in the build project configuration.
  - -> tarjeta deck09: `dva09-38efe75c` (tema canonico: CodeBuild buildspec.yml default file location)
- **[t084] CodeDeploy appspec.yml default file location** (AWS CodeDeploy) - _NUEVO_ (cos=0.557, LLM=NEW)
  - CodeDeploy requires the appspec.yml file to be placed in the root of the application source directory for the deployment to function correctly.
  - -> tarjeta deck09: `dva09-11505257` (tema canonico: CodeDeploy appspec.yml default file location)

## Pregunta 32
- **[t085] DynamoDB Global Secondary Index (GSI) query patterns with composite keys** (DynamoDB) - _NUEVO_ (cos=0.711, LLM=NEW)
  - A GSI provides an alternate partition key and sort key for querying a DynamoDB table. Items are written to the base table and automatically synchronized to the GSI; you cannot write directly to a GSI. QueryItem API on a GSI enables efficient lookups using the GSI's partition key and optional sort key.
  - -> tarjeta deck09: `dva09-68c38632` (tema canonico: DynamoDB Global Secondary Index (GSI) query patterns with composite keys)
- **[t086] S3 object metadata vs object tags for indexing and search** (S3) - _NUEVO_ (cos=0.491, LLM=NEW)
  - S3 object metadata (x-amz-meta- prefix) and object tags can store key-value pairs, but neither provides native search/indexing capabilities via S3 APIs. External indexing solutions like DynamoDB or OpenSearch are required for searchable metadata.
  - -> tarjeta deck09: `dva09-112b7945` (tema canonico: S3 object metadata vs object tags for indexing and search)
- **[t087] Lambda with Rekognition DetectLabels integration pattern for image analysis** (Lambda) - _NUEVO_ (cos=0.461, LLM=NEW)
  - S3 events can trigger Lambda functions that invoke Rekognition DetectLabels to extract labels from images. The detected labels must be stored in a separate searchable data store (like DynamoDB with GSI) since S3 itself does not provide label search functionality.
  - -> tarjeta deck09: `dva09-0db2b61e` (tema canonico: Lambda with Rekognition DetectLabels integration pattern for image analysis)

## Pregunta 33
- **[t088] CloudFormation Mappings section for region-specific values** (AWS CloudFormation) - _NUEVO_ (cos=0.425, LLM=NEW)
  - The Mappings section in CloudFormation templates is used to define key-value pairs that map to different values based on conditions like AWS Region, enabling region-specific resource configurations such as AMI IDs. This differs from Parameters (user inputs), Resources (stack components), and Outputs (exported values).
  - -> tarjeta deck09: `dva09-81f6703a` (tema canonico: CloudFormation Mappings section for region-specific values)
- **[t089] CloudFormation template sections and their purposes** (AWS CloudFormation) - _NUEVO_ (cos=0.433, LLM=NEW)
  - Understanding the distinct purposes of CloudFormation template sections: Parameters for user inputs, Resources for defining stack components, Outputs for exporting values, and Mappings for conditional value lookups based on keys like Region or environment.
  - -> tarjeta deck09: `dva09-1bf7aa93` (tema canonico: CloudFormation template sections and their purposes)

## Pregunta 34
- **[t090] SQS at-least-once delivery and application-level idempotency** (Amazon SQS) - _NUEVO_ (cos=0.346, LLM=NEW)
  - SQS standard queues guarantee at-least-once delivery, meaning messages can be delivered multiple times. Applications must implement idempotency checks (e.g., verifying duplicates before processing) to handle the same message being processed more than once.
  - -> tarjeta deck09: `dva09-04c96414` (tema canonico: SQS at-least-once delivery and application-level idempotency)
- **[t091] SQS visibility timeout configuration to prevent duplicate processing** (Amazon SQS) - _NUEVO_ (cos=0.237, LLM=NEW)
  - If a message's visibility timeout expires before the consumer processes and deletes it, another consumer can retrieve and process the same message, creating duplicates. The visibility timeout must be set longer than the maximum processing time to prevent this.
  - -> tarjeta deck09: `dva09-ea888875` (tema canonico: SQS visibility timeout configuration to prevent duplicate processing)

## Pregunta 35
- **[t092] Lambda Layers for shared dependencies across multiple functions** (AWS Lambda) - _NUEVO_ (cos=0.45, LLM=NEW)
  - Lambda layers allow you to package and centrally manage common dependencies, libraries, or custom runtimes that can be attached to multiple Lambda functions, avoiding the need to bundle dependencies with each function's deployment package individually.
  - -> tarjeta deck09: `dva09-3b3a8304` (tema canonico: Lambda Layers for shared dependencies across multiple functions)
- **[t093] Lambda deployment package options: container images vs layers vs inline code** (AWS Lambda) - _NUEVO_ (cos=0.471, LLM=NEW)
  - Lambda supports three deployment methods: container images (bundle everything including dependencies in a Docker image), layers (separate reusable components attached to functions), and inline code with dependencies. Layers are optimal for centrally managing shared dependencies across multiple functions without modifying each function's code.
  - -> tarjeta deck09: `dva09-9d2ad493` (tema canonico: Lambda deployment package options: container images vs layers vs inline code)

## Pregunta 36
- **[t094] S3 bucket policy aws:SecureTransport condition key for enforcing HTTPS** (Amazon S3) - _NUEVO_ (cos=0.384, LLM=NEW)
  - The aws:SecureTransport condition key evaluates to true for HTTPS requests and false for HTTP requests. To enforce HTTPS-only access, use a Deny effect with aws:SecureTransport=false, which blocks all HTTP requests regardless of other Allow policies.
  - -> tarjeta deck09: `dva09-f83dc6dc` (tema canonico: S3 bucket policy aws:SecureTransport condition key for enforcing HTTPS)
- **[t095] IAM policy evaluation logic: explicit Deny overrides Allow** (IAM) - _NUEVO_ (cos=0.32, LLM=NEW)
  - In AWS IAM policy evaluation, an explicit Deny always takes precedence over any Allow statements. This means a Deny policy with aws:SecureTransport=false will block HTTP requests even when other policies allow them, whereas an Allow policy with aws:SecureTransport=true won't prevent HTTP if other policies allow it.
  - -> tarjeta deck09: `dva09-eecb7e6b` (tema canonico: IAM policy evaluation logic: explicit Deny overrides Allow)

## Pregunta 37
- **[t096] API Gateway caching to reduce backend load** (Amazon API Gateway) - _YA ESTUDIADO_ (cos=0.707, LLM=COVERED)
  - API Gateway can cache endpoint responses to reduce traffic to backend services. When enabled, API Gateway returns cached responses for duplicate requests during the TTL period instead of invoking the backend, improving performance and reducing load.
  - Motivo: Card [1] already teaches that API Gateway can cache responses to avoid calling the backend on every request (faster and cheaper), which is the core concept of using caching to reduce backend load.
- **[t097] ElastiCache vs API Gateway caching use cases** (Amazon API Gateway) - _NUEVO_ (cos=0.56, LLM=NEW)
  - ElastiCache is used for application-level caching of database queries or computed results, while API Gateway caching is specifically for caching API responses at the gateway layer. API Gateway caching directly reduces traffic to backend endpoints, whereas ElastiCache reduces database load but not API endpoint traffic.
  - -> tarjeta deck09: `dva09-519d1d39` (tema canonico: ElastiCache vs API Gateway caching use cases)

## Pregunta 38
- **[t098] CodeBuild local caching vs S3 caching for build artifacts** (AWS CodeBuild) - _NUEVO_ (cos=0.454, LLM=NEW)
  - Local caching stores build artifacts on the build host itself and is optimal for large dependency files and frequent builds, while S3 caching stores artifacts in an S3 bucket across multiple hosts but incurs network transfer overhead that can degrade performance for large files.
  - -> tarjeta deck09: `dva09-699a25a9` (tema canonico: CodeBuild local caching vs S3 caching for build artifacts)
- **[t099] CodeBuild buildspec cache configuration with paths** (AWS CodeBuild) - _NUEVO_ (cos=0.303, LLM=NEW)
  - The buildspec file's cache section must specify the cache type (local or S3) and include paths to directories containing reusable build dependencies (like /.m2 for Maven) to enable caching of those artifacts across builds.
  - -> tarjeta deck09: `dva09-20fad8af` (tema canonico: CodeBuild buildspec cache configuration with paths)
- **[t100] CodeArtifact as artifact repository vs CodeBuild caching** (AWS CodeArtifact) - _NUEVO_ (cos=0.326, LLM=NEW)
  - CodeArtifact serves as a managed artifact repository for storing and retrieving approved packages but does not provide the same build performance optimization as CodeBuild caching, which stores already-downloaded dependencies locally to avoid repeated downloads.
  - -> tarjeta deck09: `dva09-5e925b4e` (tema canonico: CodeArtifact as artifact repository vs CodeBuild caching)

## Pregunta 39
- **[t101] DynamoDB RCU calculation for eventually consistent reads** (DynamoDB) - _YA ESTUDIADO_ (cos=0.817, LLM=COVERED)
  - One RCU supports one strongly consistent read per second for items up to 4 KB. Eventually consistent reads consume half the RCUs (divide by 2). Must round item size up to nearest 4 KB multiple before calculating.
  - Motivo: Card [1] already teaches the exact same concept: eventually consistent reads consume half the RCUs (divide by 2) and item size must be rounded up to nearest 4 KB multiple before calculating, demonstrated with a worked example.
- **[t102] DynamoDB WCU calculation based on item size** (DynamoDB) - _YA ESTUDIADO_ (cos=0.854, LLM=COVERED)
  - One WCU supports one write per second for items up to 1 KB. For items larger than 1 KB, round up the item size to calculate required WCUs (e.g., 7 KB item requires 7 WCUs per write).
  - Motivo: Card [1] already teaches the exact same WCU calculation concept: 1 WCU = 1 write/sec up to 1 KB, larger items consume WCUs in 1 KB blocks rounded up, with the same 2 KB example.
- **[t103] DynamoDB capacity unit provisioning for throughput requirements** (DynamoDB) - _YA ESTUDIADO_ (cos=0.686, LLM=COVERED)
  - Multiply per-item capacity units by the number of operations per second to determine minimum provisioned capacity. Must account for item size and consistency model (eventual vs strong) when calculating total RCU/WCU needs.
  - Motivo: Cards 1, 2, 3, and 5 collectively teach the core concept: calculating RCU/WCU by multiplying per-item capacity units (based on item size rounded to 4KB/1KB blocks) by operations per second, accounting for consistency model (eventual vs strong), which is exactly what the candidate topic describes.

## Pregunta 40
- **[t104] SQS Standard vs FIFO queue delivery guarantees** (Amazon SQS) - _NUEVO_ (cos=0.278, LLM=NEW)
  - SQS Standard queues provide at-least-once delivery (allowing duplicates), while SQS FIFO queues provide exactly-once processing semantics. Queue type cannot be changed after creation, requiring a new queue to switch from Standard to FIFO.
  - -> tarjeta deck09: `dva09-fdc7035e` (tema canonico: SQS Standard vs FIFO queue delivery guarantees)
- **[t105] SQS FIFO queue exactly-once processing** (Amazon SQS) - _NUEVO_ (cos=0.311, LLM=NEW)
  - SQS FIFO queues guarantee exactly-once message processing through deduplication and strict ordering, eliminating duplicate message processing that occurs with Standard queues.
  - -> tarjeta deck09: `dva09-067a43d4` (tema canonico: SQS FIFO queue exactly-once processing)
- **[t106] SQS DelaySeconds parameter behavior** (Amazon SQS) - _NUEVO_ (cos=0.242, LLM=NEW)
  - The DelaySeconds parameter postpones delivery of new messages to consumers but does not prevent duplicate deliveries in Standard queues, as it only affects initial message visibility timing.
  - -> tarjeta deck09: `dva09-a902258c` (tema canonico: SQS DelaySeconds parameter behavior)

## Pregunta 41
- **[t107] AWS SAM local testing and deployment capabilities** (AWS SAM) - _NUEVO_ (cos=0.718, LLM=NEW)
  - AWS SAM (Serverless Application Model) provides both local testing capabilities via SAM CLI (sam local invoke, sam local start-api) and unified deployment of serverless resources (Lambda, DynamoDB, API Gateway) as a single packaged unit, distinguishing it from other deployment tools.
  - -> tarjeta deck09: `dva09-fc72d12f` (tema canonico: AWS SAM capabilities and comparison to CloudFormation)
- **[t108] AWS SAM vs CloudFormation for serverless deployments** (AWS SAM) - _NUEVO_ (cos=0.813, LLM=NEW)
  - AWS SAM extends CloudFormation with simplified syntax for serverless resources and adds local testing capabilities, while plain CloudFormation (including nested stacks) can deploy Lambda and DynamoDB but lacks built-in local testing features.
  - -> tarjeta deck09: `dva09-fc72d12f` (tema canonico: AWS SAM capabilities and comparison to CloudFormation)
- **[t109] CodeDeploy Lambda deployment limitations** (AWS CodeDeploy) - _NUEVO_ (cos=0.686, LLM=NEW)
  - AWS CodeDeploy handles Lambda function deployment strategies (linear, canary, all-at-once traffic shifting) but cannot deploy Lambda functions together with other resources like DynamoDB tables as a unified infrastructure-as-code package.
  - -> tarjeta deck09: `dva09-3d9d10c5` (tema canonico: CodeDeploy Lambda deployment limitations)

## Pregunta 42
- **[t110] S3 single PUT operation size limit vs multipart upload requirement** (Amazon S3) - _NUEVO_ (cos=0.551, LLM=NEW)
  - S3 has a 5GB maximum size limit for single PUT operations. Files larger than 100MB should use multipart upload, and files larger than 5GB must use multipart upload to overcome the EntityTooLarge error.
  - -> tarjeta deck09: `dva09-80fa3497` (tema canonico: S3 upload size limits and multipart upload requirements)
- **[t111] S3 multipart upload for large objects** (Amazon S3) - _NUEVO_ (cos=0.578, LLM=NEW)
  - Multipart upload allows uploading large objects in parts (5MB to 5GB per part, up to 10,000 parts), enabling uploads up to 5TB and providing better performance, pause/resume capability, and recovery from network issues.
  - -> tarjeta deck09: `dva09-80fa3497` (tema canonico: S3 upload size limits and multipart upload requirements)
- **[t112] S3 Transfer Acceleration limitations and use cases** (Amazon S3) - _NUEVO_ (cos=0.375, LLM=NEW)
  - S3 Transfer Acceleration speeds up long-distance transfers using CloudFront edge locations but does not increase the 5GB single PUT operation limit or eliminate the need for multipart uploads for large files.
  - -> tarjeta deck09: `dva09-72e767aa` (tema canonico: S3 Transfer Acceleration limitations and use cases)

## Pregunta 43
- **[t113] S3 static website hosting to offload EC2 web server requests** (Amazon S3) - _NUEVO_ (cos=0.537, LLM=NEW)
  - S3 can serve static content (HTML, CSS, JavaScript, images) directly to clients via HTTP/HTTPS, bypassing EC2 instances entirely and reducing compute load on the application tier.
  - -> tarjeta deck09: `dva09-7860b7cc` (tema canonico: S3 static website hosting to offload EC2 web server requests)
- **[t114] EBS Multi-Attach volume scope and limitations for shared storage** (Amazon EBS) - _NUEVO_ (cos=0.273, LLM=NEW)
  - EBS Multi-Attach volumes can only be attached to instances within a single Availability Zone and still require EC2 instances to serve content, making them unsuitable for offloading HTTP requests to AWS infrastructure.
  - -> tarjeta deck09: `dva09-80670bd2` (tema canonico: EBS Multi-Attach volume scope and limitations for shared storage)
- **[t115] ElastiCache as in-memory cache vs static content delivery** (Amazon ElastiCache) - _NUEVO_ (cos=0.476, LLM=NEW)
  - ElastiCache is an in-memory key-value store for caching application data and database query results, but cannot directly serve HTTP static content to clients and still requires EC2 instances as intermediaries.
  - -> tarjeta deck09: `dva09-12895ee0` (tema canonico: ElastiCache as in-memory cache vs static content delivery)

## Pregunta 44
- **[t116] S3 client-side encryption with asymmetric customer-managed keys** (Amazon S3) - _NUEVO_ (cos=0.63, LLM=NEW)
  - Client-side encryption with customer-managed keys supports both symmetric and asymmetric encryption, allowing users to encrypt data before upload using a public key while only the key owner can decrypt with the private key.
  - -> tarjeta deck09: `dva09-895fa2cb` (tema canonico: S3 client-side encryption with asymmetric customer-managed keys)
- **[t117] S3 server-side encryption key type limitations (SSE-C, SSE-KMS, SSE-S3)** (Amazon S3) - _NUEVO_ (cos=0.712, LLM=NEW)
  - All S3 server-side encryption options (SSE-C, SSE-KMS, SSE-S3) only support symmetric encryption keys, not asymmetric keys, regardless of whether KMS can create asymmetric keys.
  - -> tarjeta deck09: `dva09-d3ec0065` (tema canonico: S3 server-side encryption key type limitations (SSE-C, SSE-KMS, SSE-S3))
- **[t118] Client-side vs server-side encryption in S3** (Amazon S3) - _NUEVO_ (cos=0.522, LLM=NEW)
  - Client-side encryption encrypts data before sending to S3 and supports asymmetric keys, while server-side encryption encrypts data after S3 receives it and only supports symmetric keys.
  - -> tarjeta deck09: `dva09-65a9cc78` (tema canonico: Client-side vs server-side encryption in S3)

## Pregunta 45
- **[t119] CodePipeline parallel actions within a stage** (AWS CodePipeline) - _NUEVO_ (cos=0.483, LLM=NEW)
  - Multiple actions within the same CodePipeline stage can execute in parallel, while stages themselves execute sequentially. This enables parallel execution of independent tasks like test segments without creating separate stages.
  - -> tarjeta deck09: `dva09-73fc1072` (tema canonico: CodePipeline parallel actions within a stage)
- **[t120] CodeBuild actions for parallel test execution** (AWS CodeBuild) - _NUEVO_ (cos=0.436, LLM=NEW)
  - CodeBuild actions can be configured to run in parallel within a single CodePipeline stage to execute independent test segments concurrently, reducing overall test execution time compared to sequential execution.
  - -> tarjeta deck09: `dva09-99bc381d` (tema canonico: CodeBuild actions for parallel test execution)

## Pregunta 46
- **[t121] EventBridge scheduled rules for Lambda function invocation** (Amazon EventBridge) - _NUEVO_ (cos=0.435, LLM=NEW)
  - EventBridge (formerly CloudWatch Events) can invoke Lambda functions on a schedule using cron or rate expressions, enabling periodic execution of custom logic without managing infrastructure.
  - -> tarjeta deck09: `dva09-8ab11fa9` (tema canonico: EventBridge scheduled rules for Lambda function invocation)
- **[t122] Lambda VPC configuration for private resource access** (AWS Lambda) - _NUEVO_ (cos=0.642, LLM=NEW)
  - Lambda functions can be configured to connect to a VPC to access private resources like EC2 instances, requiring proper VPC configuration including subnets and security groups for network connectivity.
  - -> tarjeta deck09: `dva09-6b0d6392` (tema canonico: Lambda VPC configuration for private resource access)
- **[t123] ALB health check limitations and customization** (Application Load Balancer) - _NUEVO_ (cos=0.298, LLM=NEW)
  - ALB health checks are HTTP/HTTPS requests that expect specific status codes and cannot execute custom scripts; custom health logic requires external solutions like Lambda functions that can programmatically assess instance health.
  - -> tarjeta deck09: `dva09-2e7c4ce0` (tema canonico: ALB health check limitations and customization)

## Pregunta 47
- **[t124] API Gateway canary deployments with Lambda function versions** (API Gateway) - _NUEVO_ (cos=0.487, LLM=NEW)
  - API Gateway canary releases allow splitting traffic between two Lambda function versions (stable and canary) on the same stage without changing the API URL. The canary deployment directs a configurable percentage of traffic to the canary version while the rest goes to the base version.
  - -> tarjeta deck09: `dva09-9eef633a` (tema canonico: API Gateway canary deployments and stage deployment differences)
- **[t125] Lambda function versions vs $LATEST for production traffic splitting** (Lambda) - _NUEVO_ (cos=0.489, LLM=NEW)
  - Lambda function versions are immutable snapshots that enable stable references for production traffic, while $LATEST always points to the most recent code. For canary testing, the stable production code must be a numbered version, and the new code can be referenced via $LATEST or a new version in the canary configuration.
  - -> tarjeta deck09: `dva09-58fabf33` (tema canonico: Lambda function versions vs $LATEST for production traffic splitting)
- **[t126] API Gateway stage deployment vs canary release within a stage** (API Gateway) - _NUEVO_ (cos=0.342, LLM=NEW)
  - Deploying to a new API Gateway stage creates a different URL endpoint, while a canary release within an existing stage maintains the same URL and splits traffic between two backend configurations (e.g., different Lambda versions) based on percentage.
  - -> tarjeta deck09: `dva09-9eef633a` (tema canonico: API Gateway canary deployments and stage deployment differences)

## Pregunta 48
- **[t127] Lambda execution role permissions for CloudWatch Logs** (AWS Lambda) - _NUEVO_ (cos=0.379, LLM=NEW)
  - Lambda functions require explicit IAM permissions (logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents) in their execution role to write logs to CloudWatch Logs, even though logging happens automatically when permissions are present.
  - -> tarjeta deck09: `dva09-20dd9e76` (tema canonico: Lambda execution role permissions for CloudWatch Logs)
- **[t128] Lambda execution role vs invocation permissions** (AWS Lambda) - _NUEVO_ (cos=0.436, LLM=NEW)
  - The execution role (what Lambda assumes to access AWS resources) is distinct from invocation permissions (who can invoke Lambda). Logging requires execution role permissions, not invocation permissions or permissions from other services.
  - -> tarjeta deck09: `dva09-4230093b` (tema canonico: Lambda execution role vs invocation permissions)

## Pregunta 49
- **[t129] Amazon Cognito Identity Pools for unauthenticated access** (Amazon Cognito) - _YA ESTUDIADO_ (cos=0.802, LLM=COVERED)
  - Cognito identity pools can provide temporary AWS credentials to unauthenticated users, enabling browser-based applications to access AWS services without embedding long-term credentials in client-side code.
  - Motivo: Card [1] already teaches that Cognito Identity Pools deliver temporary AWS credentials and enable unauthenticated (guest) access, which is the exact core concept of the study topic.
- **[t130] AWS SDK credential management for browser-based applications** (AWS SDK) - _NUEVO_ (cos=0.632, LLM=NEW)
  - Browser-based AWS SDK calls require temporary credentials (not IAM user access keys or role ARNs directly), which can be obtained through AWS.CognitoIdentityCredentials for unauthenticated access scenarios.
  - -> tarjeta deck09: `dva09-8471fc0f` (tema canonico: AWS SDK credential management for browser-based applications)
- **[t131] IAM security best practices for client-side credentials** (IAM) - _NUEVO_ (cos=0.403, LLM=NEW)
  - Long-term credentials (IAM user access keys) must never be embedded in client-side code or websites; temporary credentials from services like Cognito Identity Pools should be used instead for browser-based access.
  - -> tarjeta deck09: `dva09-780354bd` (tema canonico: IAM security best practices for client-side credentials)

## Pregunta 50
- **[t132] Elastic Beanstalk .ebextensions configuration file naming requirements** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.409, LLM=NEW)
  - Configuration files in the .ebextensions directory must use the .config extension (not .yaml, .yml, or .json) to be recognized and processed by Elastic Beanstalk during deployment.
  - -> tarjeta deck09: `dva09-6d255bc0` (tema canonico: Elastic Beanstalk .ebextensions configuration file naming requirements)
- **[t133] Elastic Beanstalk option_settings namespace for Application Healthcheck URL** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.422, LLM=NEW)
  - The correct namespace for configuring application health check URLs in Elastic Beanstalk is 'aws:elasticbeanstalk:application' with option_name 'Application Healthcheck URL', used within option_settings section of .config files.
  - -> tarjeta deck09: `dva09-6037becd` (tema canonico: Elastic Beanstalk option_settings namespace for Application Healthcheck URL)

## Pregunta 51
- **[t134] API Gateway stage variables for dynamic Lambda function routing** (API Gateway) - _NUEVO_ (cos=0.717, LLM=NEW)
  - Stage variables in API Gateway allow different stages (dev, prod) to invoke different Lambda function versions or aliases by using ${stageVariables.variableName} syntax in integration requests, enabling environment-specific configurations without duplicating API definitions.
  - -> tarjeta deck09: `dva09-9e3d981c` (tema canonico: API Gateway stage variables for dynamic Lambda function routing)
- **[t135] Lambda function aliases for version management** (Lambda) - _NUEVO_ (cos=0.54, LLM=NEW)
  - Lambda aliases (like dev and prod) are pointers to specific Lambda function versions that can be referenced in invocations using the function-name:alias-name syntax, enabling stable references to different versions across environments.
  - -> tarjeta deck09: `dva09-38a77ced` (tema canonico: Lambda function aliases for version management)
- **[t136] API Gateway integration request Lambda function name configuration** (API Gateway) - _NUEVO_ (cos=0.656, LLM=NEW)
  - Integration requests in API Gateway define how API methods connect to backend services like Lambda, and the Lambda function name can include dynamic references (stage variables) or static suffixes (aliases) to control which function version is invoked.
  - -> tarjeta deck09: `dva09-8170e87a` (tema canonico: API Gateway integration request Lambda function name configuration)

## Pregunta 52
- **[t137] Lambda DeadLetterConfig for asynchronous invocation failures** (AWS Lambda) - _NUEVO_ (cos=0.411, LLM=NEW)
  - Lambda functions can be configured with a DeadLetterConfig property that sends failed event payloads to an SQS queue or SNS topic for durable storage and later processing when asynchronous invocations fail after all retry attempts are exhausted.
  - -> tarjeta deck09: `dva09-07bdd61c` (tema canonico: Lambda DeadLetterConfig for asynchronous invocation failures)
- **[t138] SQS as Lambda dead-letter queue target for durable message storage** (Amazon SQS) - _NUEVO_ (cos=0.32, LLM=NEW)
  - SQS queues provide durable message storage and are the appropriate target for Lambda DeadLetterConfig when events need to be persisted for later processing, unlike ephemeral storage or email notifications which are not durable.
  - -> tarjeta deck09: `dva09-f46eece1` (tema canonico: SQS as Lambda dead-letter queue target for durable message storage)
- **[t139] CloudFormation AWS::Lambda::Function DeadLetterConfig property configuration** (AWS CloudFormation) - _NUEVO_ (cos=0.352, LLM=NEW)
  - In CloudFormation templates, the DeadLetterConfig property of AWS::Lambda::Function resource requires a TargetArn that references either an SQS queue ARN or SNS topic ARN to capture failed asynchronous invocations.
  - -> tarjeta deck09: `dva09-07bdd61c` (tema canonico: Lambda DeadLetterConfig for asynchronous invocation failures)

## Pregunta 53
- **[t140] EC2 instance IAM roles for application access to AWS services** (IAM) - _YA ESTUDIADO_ (cos=0.742, LLM=COVERED)
  - EC2 instances should use IAM roles (temporary credentials) rather than IAM users (permanent credentials) to securely access AWS services like DynamoDB. IAM roles are attached via launch templates in Auto Scaling groups.
  - Motivo: Card [1] already teaches the core concept that EC2 instances should use IAM roles (via instance profile) for temporary credentials instead of embedding long-lived access keys, which is the same fundamental distinction being tested.
- **[t141] Lambda authorizers scope and compatibility with load balancers vs API Gateway** (API Gateway) - _NUEVO_ (cos=0.738, LLM=NEW)
  - Lambda authorizers are only compatible with API Gateway for custom authorization logic, not with Application Load Balancers or Network Load Balancers.
  - -> tarjeta deck09: `dva09-7155a1c3` (tema canonico: Lambda authorizers scope and compatibility with load balancers vs API Gateway)
- **[t142] Cognito User Pools vs Identity Pools for AWS service access** (Amazon Cognito) - _YA ESTUDIADO_ (cos=0.876, LLM=COVERED)
  - Cognito User Pools provide authentication for application users but do not provide AWS credentials for accessing services like DynamoDB. Identity Pools (federated identities) are needed to exchange user pool tokens for temporary AWS credentials.
  - Motivo: Card [1] already teaches the core distinction that User Pools authenticate and return tokens while Identity Pools provide AWS credentials, which is exactly the concept being tested.

## Pregunta 54
- **[t143] AWS Secrets Manager automatic rotation with rotation templates** (AWS Secrets Manager) - _NUEVO_ (cos=0.396, LLM=NEW)
  - Secrets Manager provides built-in rotation templates (SecretsManagerRotationTemplate) and native scheduling to automatically rotate secrets every N days with minimal code, unlike Parameter Store which requires custom Lambda functions and EventBridge rules for rotation.
  - -> tarjeta deck09: `dva09-606e5cf3` (tema canonico: AWS Secrets Manager automatic rotation for database credentials)
- **[t144] AWS Secrets Manager vs Systems Manager Parameter Store for secret rotation** (AWS Secrets Manager) - _NUEVO_ (cos=0.354, LLM=NEW)
  - Secrets Manager is purpose-built for secrets with automatic rotation capabilities and mandatory encryption at rest, while Parameter Store SecureString requires manual rotation implementation using Lambda and EventBridge, making Secrets Manager the lower-effort choice for rotation requirements.
  - -> tarjeta deck09: `dva09-b7eab8a0` (tema canonico: AWS Secrets Manager vs Systems Manager Parameter Store for secret rotation)
- **[t145] Lambda functions retrieving secrets from Secrets Manager at runtime** (AWS Lambda) - _NUEVO_ (cos=0.417, LLM=NEW)
  - Lambda functions can dynamically pull secrets from Secrets Manager using API calls at runtime, automatically receiving rotated values without requiring environment variable updates or redeployment when secrets rotate.
  - -> tarjeta deck09: `dva09-6bc61567` (tema canonico: Lambda functions retrieving secrets from Secrets Manager at runtime)

## Pregunta 55
- **[t146] Elastic Beanstalk Blue/Green deployment using environment URL swap** (AWS Elastic Beanstalk) - _YA ESTUDIADO_ (cos=0.559, LLM=COVERED)
  - Blue/Green deployment via creating a new Elastic Beanstalk environment and swapping environment URLs enables zero-downtime full cutover with instant rollback capability, ideal for incompatible version updates.
  - Motivo: Card [1] already teaches Blue/Green deployment in Elastic Beanstalk for incompatible version updates with instant cutover and fast rollback capability, which is the same core concept as environment URL swap for zero-downtime deployment.
- **[t147] Elastic Beanstalk deployment policies: All-at-once vs Rolling vs Rolling with additional batch** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.482, LLM=NEW)
  - All-at-once updates all instances simultaneously causing downtime; Rolling updates instances in batches maintaining partial availability; Rolling with additional batch launches new instances first but all three perform in-place updates unsuitable for incompatible versions requiring full cutover.
  - -> tarjeta deck09: `dva09-702a71ef` (tema canonico: Elastic Beanstalk deployment policies comparison and characteristics)

## Pregunta 56
- **[t148] DynamoDB Streams view types (KEYS_ONLY vs NEW_IMAGE vs OLD_IMAGE vs NEW_AND_OLD_IMAGES)** (DynamoDB) - _NUEVO_ (cos=0.425, LLM=NEW)
  - KEYS_ONLY stream view type records only partition and sort keys without attribute values, preventing PII exposure, while NEW_IMAGE, OLD_IMAGE, and NEW_AND_OLD_IMAGES include full item data with all attributes.
  - -> tarjeta deck09: `dva09-04ecb7dc` (tema canonico: DynamoDB Streams view types (KEYS_ONLY vs NEW_IMAGE vs OLD_IMAGE vs NEW_AND_OLD_IMAGES))
- **[t149] AWS SDK API response structure (response data vs response metadata)** (AWS SDK) - _NUEVO_ (cos=0.342, LLM=NEW)
  - AWS SDK API responses contain both response data (actual item attributes/content) and response metadata (request ID, HTTP status, retry attempts). Logging only metadata provides operational visibility without exposing sensitive data content.
  - -> tarjeta deck09: `dva09-6e06260b` (tema canonico: AWS SDK API response structure (response data vs response metadata))
- **[t150] Lambda function logging strategies for PII compliance** (Lambda) - _NUEVO_ (cos=0.483, LLM=NEW)
  - When processing PII in Lambda functions, developers must selectively log workflow events and API metadata while avoiding logging the actual data payload to maintain compliance and operational visibility.
  - -> tarjeta deck09: `dva09-ceca3e9d` (tema canonico: Lambda function logging strategies for PII compliance)

## Pregunta 57
- **[t151] CodePipeline approval actions for manual intervention** (AWS CodePipeline) - _YA ESTUDIADO_ (cos=0.784, LLM=COVERED)
  - CodePipeline supports approval actions as a built-in action type that enables manual approval gates within a pipeline stage, allowing human review before proceeding to subsequent stages like production deployment.
  - Motivo: Card [1] already teaches that CodePipeline has a built-in manual approval action type that stops the pipeline for human review before proceeding to the next stage, which is the exact same core concept as the candidate topic.
- **[t152] CodePipeline stage transitions vs approval actions** (AWS CodePipeline) - _NUEVO_ (cos=0.643, LLM=NEW)
  - Disabling stage transitions prevents pipeline executions from entering a stage but does not provide manual approval functionality; approval actions are the correct mechanism for requiring explicit human authorization before proceeding.
  - -> tarjeta deck09: `dva09-82c7a3d8` (tema canonico: CodePipeline stage transitions vs approval actions)
- **[t153] CodePipeline action types (source, build, test, deploy, approval, invoke)** (AWS CodePipeline) - _NUEVO_ (cos=0.645, LLM=NEW)
  - CodePipeline has six valid action types, each serving distinct purposes in the CI/CD workflow, with approval being the specific action type designed for manual review gates rather than using stage manipulation or multiple pipelines.
  - -> tarjeta deck09: `dva09-be8eaaa0` (tema canonico: CodePipeline action types (source, build, test, deploy, approval, invoke))

## Pregunta 58
- **[t154] DynamoDB ProvisionedThroughputExceededException error meaning and causes** (DynamoDB) - _NUEVO_ (cos=0.419, LLM=NEW)
  - ProvisionedThroughputExceededException indicates that write or read requests exceed the provisioned WCU/RCU capacity for a table or its global secondary indexes, not permissions, item size, or storage issues.
  - -> tarjeta deck09: `dva09-a8c6e6d7` (tema canonico: DynamoDB ProvisionedThroughputExceededException)
- **[t155] DynamoDB provisioned capacity units (WCU/RCU) and throttling** (DynamoDB) - _NUEVO_ (cos=0.662, LLM=NEW)
  - Tables and GSIs have provisioned write capacity units (WCU) and read capacity units (RCU) that limit throughput; exceeding these limits causes throttling with ProvisionedThroughputExceededException errors.
  - -> tarjeta deck09: `dva09-d8405351` (tema canonico: DynamoDB provisioned capacity units (WCU/RCU) and throttling)
- **[t156] DynamoDB error types: ValidationException vs ProvisionedThroughputExceededException vs AccessDeniedException** (DynamoDB) - _NUEVO_ (cos=0.348, LLM=NEW)
  - Different DynamoDB errors indicate different issues: ValidationException for item size/format violations, ProvisionedThroughputExceededException for capacity limits, and AccessDeniedException for IAM permission issues.
  - -> tarjeta deck09: `dva09-593330f4` (tema canonico: DynamoDB error types and their causes)

## Pregunta 59
- **[t157] Lambda function timeout limits and retry constraints** (AWS Lambda) - _NUEVO_ (cos=0.518, LLM=NEW)
  - Lambda functions have a maximum timeout of 15 minutes that applies to the entire execution including extensions and layers. Synchronous invocations and nested Lambda calls cannot exceed this timeout, making them unsuitable for long-running retry scenarios that need to span hours.
  - -> tarjeta deck09: `dva09-2331d258` (tema canonico: Lambda function timeout limits and retry constraints)
- **[t158] Step Functions state machine retry configuration with BackoffRate and MaxAttempts** (AWS Step Functions) - _NUEVO_ (cos=0.478, LLM=NEW)
  - Step Functions can orchestrate long-running workflows beyond Lambda's timeout limits by using task states with retry policies. The BackoffRate and MaxAttempts parameters enable exponential backoff retries over extended periods, and state machines can be triggered directly from API Gateway.
  - -> tarjeta deck09: `dva09-f2f0b341` (tema canonico: Step Functions state machine retry configuration with BackoffRate and MaxAttempts)
- **[t159] API Gateway integration with Step Functions for asynchronous workflows** (Amazon API Gateway) - _NUEVO_ (cos=0.524, LLM=NEW)
  - API Gateway REST APIs can directly start Step Functions state machine executions using POST method integration, enabling asynchronous workflow orchestration that decouples the API response from long-running backend processes.
  - -> tarjeta deck09: `dva09-f21c7966` (tema canonico: API Gateway integration with Step Functions for asynchronous workflows)

## Pregunta 60
- **[t160] AWS X-Ray tracing for API Gateway and Lambda end-to-end latency analysis** (AWS X-Ray) - _NUEVO_ (cos=0.612, LLM=NEW)
  - X-Ray provides distributed tracing to identify performance bottlenecks across API Gateway and Lambda by capturing end-to-end request flows, showing latency at each service boundary, unlike CloudWatch Logs which only shows individual service logs without correlation.
  - -> tarjeta deck09: `dva09-0bf5a458` (tema canonico: AWS X-Ray distributed tracing for microservices and serverless architectures)
- **[t161] CloudWatch Logs vs X-Ray for performance troubleshooting** (Amazon CloudWatch) - _NUEVO_ (cos=0.468, LLM=NEW)
  - CloudWatch Logs are suitable for debugging errors and failures within individual services (API Gateway execution logs, Lambda function logs), but X-Ray is required for tracing latency and performance bottlenecks across distributed service calls.
  - -> tarjeta deck09: `dva09-881c9cc3` (tema canonico: CloudWatch vs X-Ray for distributed tracing and performance analysis)
- **[t162] CloudTrail for API Gateway service API auditing vs request tracing** (AWS CloudTrail) - _NUEVO_ (cos=0.479, LLM=NEW)
  - CloudTrail logs API Gateway control plane operations (API creation, deployment, updates) but does not capture data plane request latency or performance metrics for individual API invocations.
  - -> tarjeta deck09: `dva09-363e33b4` (tema canonico: CloudTrail for API Gateway service API auditing vs request tracing)

## Pregunta 61
- **[t163] S3 SSE-C GetObject API requirements** (Amazon S3) - _NUEVO_ (cos=0.568, LLM=NEW)
  - When retrieving objects encrypted with SSE-C (server-side encryption with customer-provided keys), the GetObject API call must include both the S3 object key and the same customer-provided encryption key used during upload. S3 does not store the encryption key, only a salted HMAC for validation.
  - -> tarjeta deck09: `dva09-b4700384` (tema canonico: S3 SSE-C GetObject API requirements)
- **[t164] S3 server-side encryption types: SSE-C vs SSE-KMS** (Amazon S3) - _YA ESTUDIADO_ (cos=0.727, LLM=COVERED)
  - SSE-C requires the customer to provide and manage encryption keys with each request, while SSE-KMS uses AWS KMS managed keys identified by ARN. The encryption method determines what credentials/keys must be provided in API calls.
  - Motivo: Card [2] already teaches who manages keys in SSE-C (customer) vs SSE-KMS (AWS/KMS), which is the core distinction of the candidate topic, even though it doesn't explicitly mention ARN or API call details.
- **[t165] S3 SSE-C encryption key storage and HMAC validation** (Amazon S3) - _NUEVO_ (cos=0.65, LLM=NEW)
  - With SSE-C, S3 stores only a randomly salted HMAC of the encryption key for validation purposes, not the actual encryption key. The HMAC cannot be used to derive or retrieve the original encryption key, requiring customers to maintain the key separately.
  - -> tarjeta deck09: `dva09-31e94b1d` (tema canonico: S3 SSE-C encryption key storage and HMAC validation)

## Pregunta 62
- **[t166] Elastic Beanstalk Rolling deployment policy characteristics** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.464, LLM=NEW)
  - Rolling deployment updates instances in batches using only existing instances, maintaining partial availability during deployment but potentially causing reduced capacity and some service degradation. It does not create new instances unlike Rolling with Additional Batch or Immutable deployments.
  - -> tarjeta deck09: `dva09-702a71ef` (tema canonico: Elastic Beanstalk deployment policies comparison and characteristics)
- **[t167] Elastic Beanstalk All-at-once vs Rolling deployment outage impact** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.449, LLM=NEW)
  - All-at-once deployment updates all instances simultaneously causing complete service outage, while Rolling deployment maintains partial service availability by updating instances in batches, resulting in minimal but not zero outage.
  - -> tarjeta deck09: `dva09-2e7903de` (tema canonico: Elastic Beanstalk All-at-once vs Rolling deployment outage impact)
- **[t168] Elastic Beanstalk deployment policies that create new instances** (AWS Elastic Beanstalk) - _NUEVO_ (cos=0.459, LLM=NEW)
  - Rolling with Additional Batch and Immutable deployment policies create new EC2 instances during deployment, while Rolling and All-at-once policies use only existing instances for in-place updates.
  - -> tarjeta deck09: `dva09-702a71ef` (tema canonico: Elastic Beanstalk deployment policies comparison and characteristics)

## Pregunta 63
- **[t169] Lambda memory allocation affects CPU allocation** (AWS Lambda) - _YA ESTUDIADO_ (cos=0.677, LLM=COVERED)
  - Increasing Lambda function memory allocation proportionally increases CPU resources available to the function, which can reduce execution time for CPU-intensive workloads.
  - Motivo: Card [1] already teaches that Lambda CPU scales proportionally with memory allocation, which is the exact same core concept as the candidate topic.
- **[t170] Lambda execution environment vs EC2 instances** (AWS Lambda) - _NUEVO_ (cos=0.424, LLM=NEW)
  - Lambda functions run in AWS-managed execution environments, not on EC2 instances. You cannot configure Lambda to run on specific EC2 instance types; Lambda abstracts the underlying compute infrastructure.
  - -> tarjeta deck09: `dva09-677a3242` (tema canonico: Lambda execution environment vs EC2 instances)
- **[t171] Lambda reserved concurrency purpose** (AWS Lambda) - _NUEVO_ (cos=0.56, LLM=NEW)
  - Reserved concurrency controls the maximum number of concurrent executions for a function but does not affect individual function execution time or timeout issues for single invocations.
  - -> tarjeta deck09: `dva09-72a7ec81` (tema canonico: Lambda reserved concurrency purpose)

## Pregunta 64
- **[t172] AWS X-Ray tracing for Lambda functions to inspect downstream service calls** (AWS X-Ray) - _NUEVO_ (cos=0.627, LLM=NEW)
  - X-Ray can be enabled on Lambda functions to trace and measure the timing of downstream API calls (like DynamoDB operations), providing detailed performance insights and identifying bottlenecks in the execution path.
  - -> tarjeta deck09: `dva09-0bf5a458` (tema canonico: AWS X-Ray distributed tracing for microservices and serverless architectures)
- **[t173] X-Ray integration with DynamoDB SDK calls for performance analysis** (AWS X-Ray) - _NUEVO_ (cos=0.619, LLM=NEW)
  - When X-Ray tracing is enabled, the AWS SDK automatically instruments DynamoDB API calls, capturing timing data, request/response details, and errors to help diagnose performance issues.
  - -> tarjeta deck09: `dva09-4a6e1bb1` (tema canonico: X-Ray integration with DynamoDB SDK calls for performance analysis)
- **[t174] CloudWatch Metrics vs X-Ray for API call inspection** (Amazon CloudWatch) - _NUEVO_ (cos=0.526, LLM=NEW)
  - CloudWatch Metrics provide aggregate statistics (invocation count, duration, errors) but cannot inspect individual API call timing or trace request flows, whereas X-Ray provides detailed tracing of individual requests and downstream service calls.
  - -> tarjeta deck09: `dva09-881c9cc3` (tema canonico: CloudWatch vs X-Ray for distributed tracing and performance analysis)

## Pregunta 65
- **[t175] DynamoDB Conditional Writes for optimistic locking** (DynamoDB) - _YA ESTUDIADO_ (cos=0.683, LLM=COVERED)
  - Conditional writes in DynamoDB allow updates to succeed only if item attributes meet expected conditions, preventing concurrent update conflicts by checking the current state before applying changes.
  - Motivo: Card [1] already teaches that conditional writes (optimistic locking with version number) ensure an update only succeeds if the item hasn't changed since read, which is the core concept of DynamoDB conditional writes for preventing concurrent update conflicts.
- **[t176] DynamoDB Atomic Counters vs Conditional Writes** (DynamoDB) - _NUEVO_ (cos=0.496, LLM=NEW)
  - Atomic counters increment/decrement numeric attributes without read-before-write but allow overcounting/undercounting, while conditional writes enforce strict consistency by validating expected conditions before updates.
  - -> tarjeta deck09: `dva09-f14e8035` (tema canonico: DynamoDB Atomic Counters vs Conditional Writes)

