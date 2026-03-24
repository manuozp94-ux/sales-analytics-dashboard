# RESUME_NEXT_SESSION

## Last Updated (UTC)

- 2026-03-15

## Current Snapshot

- Fabric Warehouse already has canonical objects in `core` and `mart`.
- Parity status is closed:
  - Counts: pass
  - QA grain/null/orphan: pass (all zero violations)
  - KPI: pass
- Publication track is unblocked and the latest Warehouse SQL cleanup has already been re-applied in Fabric through the local `sqlcmd` path.
- `sm_sales_analytics_mvp` exists and Page 1 of the Power BI report is already data-validated in the Fabric web UI:
  - 3 KPI cards (`orders`, `revenue`, `delivered_orders`)
  - 4 trend charts (`revenue`, `orders`, `on_time_delivery_rate`, `avg_delivery_days`)
  - page filter `purchase_month >= 2017-01-01`
- Copilot-assisted page generation is unavailable due to capacity/preview limits, so MVP report work continues manually in Power BI Service.

## First 10 Minutes (Exact Sequence)

1. Open the existing report tied to `sm_sales_analytics_mvp`.
2. Polish Page 1:
   - normalize card labels,
   - clean formatting consistency,
   - keep the current validated data bindings intact,
   - keep `purchase_month >= 2017-01-01` page filter.
3. Build Page 2 from `mart.mart_cohort_unit_economics`.
4. Build Page 3 from `mart.mart_customer_ltv_summary`.
5. Then continue with publication and final public URL registration.

## Important Notes

- Canonical analytical schema is `mart` (singular). If legacy `marts` still exists, retire it with `06-fabric-sync/sql/fabric-warehouse/02_drop_legacy_marts_schema_safe.sql`.
- Do not rerun full runbook unless base objects were dropped/changed.
- Publication is allowed because parity compare is `PASS`, and the current Warehouse cleanup is already live in Fabric.
- The current MVP report uses manual Power BI Service editing on macOS. Treat PBIP/PBIR and code-driven layout generation as post-MVP work.
- The consulting-grade Fabric accelerator foundation now starts from:
  - `06-fabric-sync/FABRIC_CONSULTING_STANDARD.md`
  - `06-fabric-sync/contracts/`
  - `06-fabric-sync/sql_pack_manifest.py`
  - `06-fabric-sync/fabric_sql_guardrails.py`

## If Fabric Model Changes Again

- Refresh `06-fabric-sync/state/parity/parity_fabric_latest.json` from the Warehouse query pack.
- Rerun the comparator and keep `06-fabric-sync/state/parity/parity_compare_latest.md` at `PASS` before updating public-facing metrics or links.

## If Agent Architecture Work Resumes

- Start from the Fabric consulting standard and contract bundle before proposing new automation layers.
- Keep repo-first Warehouse SQL as the default path unless the engagement explicitly justifies Fabric Git/deployment-pipeline adoption.
- Treat semantic-model, environment, and governance contracts as the next enforcement targets after the current MVP publication work.
