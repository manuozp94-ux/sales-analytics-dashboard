id | decision | contexto | alternativas | razón | consecuencias | estado | evidencia_msg_id
ADR-001 | validate data in pandas first | CSV raw dataset | validate directly in SQL | easier inspection | duplicate logic | approved | UNKNOWN
ADR-002 | design star schema before SQL | modeling clarity | build ad-hoc tables | architectural discipline | potential redesign | approved | UNKNOWN
ADR-003 | grain = (order_id, order_item_id) | multi‑item orders | grain by order_id | accurate representation | more complex queries | approved | UNKNOWN
ADR-004 | use DuckDB | local analytics DB | SQLite/Postgres | optimized for analytics | dependency added | approved | UNKNOWN
ADR-005 | staging tables mirror raw | separation of layers | transform on ingest | traceability | more tables | approved | UNKNOWN
ADR-006 | tolerant CSV ingestion | malformed rows | clean CSV manually | pipeline continuity | types fixed later | approved | UNKNOWN
ADR-007 | document state in Word | long conversation | rely on chat history | migration reliability | duplicate docs | approved | UNKNOWN
ADR-008 | separate SQL folders | repo organization | store SQL in notebooks | clearer architecture | execution discipline required | approved | UNKNOWN
