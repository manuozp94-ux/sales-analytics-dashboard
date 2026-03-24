# Fabric SQL Pack

This folder contains the Fabric Warehouse SQL pack used by the parity runbook:

- runbook: `06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md`
- execution scripts: `06-fabric-sync/sql/fabric-warehouse/`
- CLI apply scaffold: `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh`
- canonical manifest: `06-fabric-sync/sql_pack_manifest.py`
- deployable SQL guardrails: `06-fabric-sync/fabric_sql_guardrails.py`

Execution order is fixed and documented in the runbook.

Notes:

- The CLI scaffold forwards connection/authentication flags directly to `sqlcmd`, so the same ordered pack can run locally or from a CI agent.
- The CLI scaffold resolves the ordered default pack from `sql_pack_manifest.py`, so docs and quality checks share the same file list.
- Optional scripts remain opt-in in the CLI path:
  - `02_drop_legacy_marts_schema_safe.sql`
  - `01_reset_core_mart_safe.sql`
- `01_reset_core_mart_safe.sql` resets canonical model schemas `core` and `mart` only and keeps `stg` intact.
- `02_drop_legacy_marts_schema_safe.sql` is a one-time cleanup helper to retire a legacy empty `marts` schema.
- `05_stg_compat_views.sql` creates compatibility views (`stg.stg_*`) when staging
  is loaded with short table names (`stg.orders`, `stg.customers`, etc.).
- Deployable SQL guardrails block risky schema-evolution patterns from the canonical pack by default; reviewed one-time changes should stay in optional paths.
