# Rebalanceo de opciones DVA-C02 (defecto: opcion correcta delata por forma)

Regla nueva (DECK_STANDARDS.md sec.5 + quality gate): las 4 opciones deben tener
longitud/especificidad comparable. NINGUN patron (mas larga NI mas corta NI mas
tecnica) debe delatar la respuesta. Fix = subir distractores al nivel de la
correcta, no recortar la correcta. Al reescribir distractores, ACTUALIZAR tambien
la seccion "Por que NO las otras" del answer para que corresponda.

Total desbalanceadas (piso 60 chars): 45

## Estado
- [x] Lote 1 (6): q9-projection, q13-appsync, q21-object-lambda-how, q50-transactional, q19-cf-func, q57-sse-c  -> APLICADO + refutaciones ajustadas (q50, q57)

## Pendientes (45)
04: q6-rcu-mistake, q10-crr-requirements, q13-why-no-encrypt, q14-origin-failover, q14-lambda-edge, q14-why-not-cache, q15-conditional-writes, q15-why-not-optimistic, q17-lsi-vs-gsi, q18-shards-concurrency, q18-poll-vs-push
05: q4-approval-timeout, q7-segment-documents, q7-segment-vs-subsegment, q11-enhanced-monitoring, q11-cw-vs-enhanced, q12-why-ttl, q21-object-lambda
06: q1-cloudtrail-vs-drift, q7-why-not-800, q10-task-role, q4-cors-allows, q4-cors-exposeheader, q4-cors-not-authz, q5-sse-header-map
07: q4-object-lambda-per-role, q4-objectlambda-vs-eventnotif, q6-gsi-capacity, q6-gsi-vs-lsi-pk, q7-proxy-vs-custom, q10-cloudfront-signed, q10-signedurl-vs-cookie, q10-why-not-nacl-cors, q15-gettracesummaries-vs-batch, q17-waf-vs-guardduty-vs-fm, q19-why-not-efs-ec2-glacier, q21-sam-transform-cfn, q23-sts-assumerole-federation, q26-lsi-new-table, q29-annotation-vs-metadata, q34-strategy-purposes, q37-sam-commands, q41-global-tables-lww, q48-code-vs-codeuri, q57-who-manages-key

## FINAL (obligatorio): re-verificar CADA carta editada contra estandares
- verdict con {{L}} intacto, no filtra respuesta, 4 opciones, refuta distractores,
  respuesta correcta sigue siendo la unica correcta, refutaciones coinciden con
  los nuevos distractores. Quality gate OK en los 4 generadores.
