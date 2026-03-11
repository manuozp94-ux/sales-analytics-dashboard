# Consolidated Decisions

## CONV_A

id | decisión | contexto | alternativas | razón | consecuencias | estado | evidencia_msg_id
ADR_001 | usar Python para validación de datos | el usuario quiere validar datos antes de modelar | validar directamente en SQL | Python permite exploración flexible | se agrega dependencia pandas | aprobado | msg_190
ADR_002 | usar pandas para análisis inicial | pandas es estándar de análisis | usar solo SQL | facilidad de inspección | notebooks requeridos | aprobado | msg_214
ADR_003 | usar Jupyter Notebook | entorno interactivo | scripts Python | aprendizaje paso a paso | entorno reproducible | aprobado | msg_214
ADR_004 | ejecutar Jupyter desde terminal | flujo estándar de trabajo | IDE integrado | control directo del servidor | dependencia de terminal | aprobado | msg_221
ADR_005 | estructura de repo numerada | organización pedagógica | estructura plana | claridad progresiva | navegación clara | aprobado | msg_168
ADR_006 | usar CSV como fuente inicial | datos simples para aprendizaje | base de datos directa | accesibilidad | ingestión manual | aprobado | msg_130
ADR_007 | eliminar ":" en carpetas | error 404 detectado | mantener nombres originales | compatibilidad filesystem | notebooks funcionan | aprobado | msg_223
ADR_008 | retrasar SQL hasta validar datos | enfoque pedagógico | modelar primero | evitar errores de modelado | más tiempo de exploración | aprobado | msg_190
ADR_009 | crear notebook 01_data_validation | primer paso del pipeline | script Python | claridad de fase | estructura modular | aprobado | msg_235
ADR_010 | preparar exportación de conversación | conversación se volvió lenta | continuar sin documentación | preservar conocimiento | archivos de contexto | aprobado | msg_30

## CONV_B

id | decision | contexto | alternativas | razón | consecuencias | estado | evidencia_msg_id
ADR-001 | validate data in pandas first | CSV raw dataset | validate directly in SQL | easier inspection | duplicate logic | approved | UNKNOWN
ADR-002 | design star schema before SQL | modeling clarity | build ad-hoc tables | architectural discipline | potential redesign | approved | UNKNOWN
ADR-003 | grain = (order_id, order_item_id) | multi‑item orders | grain by order_id | accurate representation | more complex queries | approved | UNKNOWN
ADR-004 | use DuckDB | local analytics DB | SQLite/Postgres | optimized for analytics | dependency added | approved | UNKNOWN
ADR-005 | staging tables mirror raw | separation of layers | transform on ingest | traceability | more tables | approved | UNKNOWN
ADR-006 | tolerant CSV ingestion | malformed rows | clean CSV manually | pipeline continuity | types fixed later | approved | UNKNOWN
ADR-007 | document state in Word | long conversation | rely on chat history | migration reliability | duplicate docs | approved | UNKNOWN
ADR-008 | separate SQL folders | repo organization | store SQL in notebooks | clearer architecture | execution discipline required | approved | UNKNOWN

## CONV_C

| id | decisión | contexto | alternativas | razón | consecuencias | estado | evidencia_msg_id |
|----|----------|----------|--------------|-------|---------------|--------|------------------|
| ADR-001 | Usar DuckDB para prototipado local | Se necesitaba ambiente local rápido para modelado | SQLite, Pandas-only | DuckDB soporta SQL analítico eficiente | Migración posterior necesaria | aprobado | UNKNOWN |
| ADR-002 | Migrar arquitectura a Microsoft Fabric | Proyecto orientado a stack Microsoft | Snowflake, BigQuery | Integración con Power BI | Dependencia en ecosistema Microsoft | aprobado | UNKNOWN |
| ADR-003 | Separar capas stg y core | Arquitectura analítica estándar | Transformaciones directas | Claridad de pipeline | Más scripts SQL | aprobado | UNKNOWN |
| ADR-004 | Usar pipeline Copy Data | Transferir datos Lakehouse → Warehouse | Notebook ingestion | Copy pipeline es mecanismo nativo | Riesgo duplicación si full copy | aprobado | UNKNOWN |
| ADR-005 | Modelo dimensional star schema | Analítica BI eficiente | Data vault | Star schema más simple para BI | Limitaciones para historización | aprobado | UNKNOWN |
| ADR-006 | Deduplicar fact_order_reviews | Dataset presenta review_id duplicado | Mantener duplicados | Grain consistente | Puede perder granularidad alternativa | aprobado | UNKNOWN |
| ADR-007 | Crear script QA consolidado | Necesidad de validaciones automáticas | Validaciones manuales | Reproducibilidad | Mantenimiento adicional | aprobado | UNKNOWN |
| ADR-008 | Scripts idempotentes (DROP/CREATE) | Re-runs frecuentes | CREATE ONLY | Permite ejecuciones repetibles | Rebuild completo cada corrida | aprobado | UNKNOWN |
| ADR-009 | Staging sin transformaciones | Separación ingestión/modelado | Transformación directa | Trazabilidad | Más almacenamiento | aprobado | UNKNOWN |
| ADR-010 | Fact tables con date_key | Mejora joins analíticos | timestamp directo | Best practice dimensional | requiere dim_date | aprobado | UNKNOWN |
