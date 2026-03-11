# Resumen ejecutivo (conversación CONV_B)

## Objetivo
Construir un proyecto “Sales Analytics Dashboard” con enfoque de Analytics Engineering, con:
- Validación de datos en notebook (pandas) y documentación de hallazgos.
- Materialización en DuckDB (staging `stg_*`) a partir de CSVs.
- Preparación para modelado en SQL (carpeta `03-sql/`) y validaciones posteriores.

evidence_msg_id: UNKNOWN — La interfaz no expone msg_id verificables en esta exportación.

## Alcance real cubierto en la conversación
Hecho:
- Resolución de rutas/estructura de repo para acceder a `01-data/01-raw`.
- Carga de datasets CSV y verificación de shapes/heads.
- Validaciones de integridad (PK/FK/grain) con outputs explícitos compartidos.
- Inicio de Phase 3: creación de staging tables en DuckDB desde CSV.
- Diagnóstico y workaround de parsing en `order_reviews_dataset.csv` (CSV malformado).

En progreso:
- Materialización del star schema (dims/facts) en DuckDB a través de scripts SQL.
- Estructuración de `03-sql/models` y `03-sql/schema` (se observó vacío: `([], [])`).

Pendiente:
- Creación y versionado de scripts SQL reales (dim/fact).
- Validaciones post-materialización.
- Implementación real en Microsoft Fabric (no hay evidencia de artefactos).

## Estado técnico confirmado
- Archivos raw: order_payments_dataset.csv, orders_dataset.csv, order_items_dataset.csv,
  order_reviews_dataset.csv, product_summarize_dataset.csv, customers_dataset.csv
- orders cargado con shape (99441, 9)
- Missing product_id: 611 IDs; 1604 filas (~1.42%)
- order_reviews huérfanas: 2
- DuckDB version: v1.4.4
- 03-sql/models y schema vacíos ([], [])
