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
