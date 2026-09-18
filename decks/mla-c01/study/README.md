# study/ — Tarjetas de estudio visuales (MLA-C01)

Explicaciones visuales autocontenidas (HTML con imágenes embebidas en base64) para
los temas más confusos del examen. Cada HTML se abre directo en el navegador, sin
dependencias externas.

## Cómo abrir
```bash
open html/<archivo>.html          # macOS
```

## Índice de tarjetas (html/)

| Archivo | Tema |
|---|---|
| `data_wrangler_viz.html` | Técnicas de visualización de Data Wrangler (scatter, histograma, etc.) |
| `forecasting_metrics.html` | Métricas de forecasting: RMSE y Average wQL vs clasificación |
| `feature_store_online_offline.html` | Feature Store: online store vs offline store (aclara el nombre) |
| `deployment_serverless.html` | Despliegue: serverless SIN provisioned vs con provisioned |
| `vpc_endpoints_gateway_vs_interface.html` | Gateway endpoint vs Interface endpoint (PrivateLink) |
| `preprocessing_event_driven.html` | Preprocesamiento ML event-driven (Processing Job + Lambda + S3 events) |
| `classification_metrics.html` | Cuarteto de clasificación: Precision/Recall/Accuracy/F1 |
| `threshold_and_auc.html` | Qué es el umbral y por qué AUC-ROC no es de umbral fijo |
| `precision_vs_recall.html` | Precision vs Recall (de qué conjunto es cada fracción) |
| `streaming_realtime.html` | Streaming tiempo real: Kinesis Data Streams + Managed Flink |
| `bias_metrics_dpl.html` | Métricas de sesgo de Clarify: DPL (y CI, TVD, KL) |
| `why_bias_metrics.html` | Qué problema resuelve cada métrica de sesgo |
| `correlation_spearman.html` | Correlación no lineal (monótona): Spearman |
| `correlation_deep.html` | Coeficientes de correlación en profundidad (Pearson/Spearman/Kendall/Cramér's V) |

## Regenerar
Los scripts que generan estas tarjetas están en `generators/`:
- `make_viz_*.py` — generan las gráficas (matplotlib).
- `build_html_*.py` — arman el HTML autocontenido embebiendo las gráficas en base64.

Requieren matplotlib + numpy. Para regenerar una tarjeta, crea un venv temporal:
```bash
python3 -m venv /tmp/study-venv && /tmp/study-venv/bin/pip install matplotlib numpy
/tmp/study-venv/bin/python generators/make_viz_<tema>.py
/tmp/study-venv/bin/python generators/build_html_<tema>.py
```
(Las imágenes intermedias se embeben en el HTML final, así que no se versionan.)
