# Fabric Change Note

## Change Summary

- Date (UTC): 2026-03-14
- Workspace: `1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Change Owner: Manuel Antonio Orozco
- Change Type:
  - Schema/Core Model
  - Marts
  - Security/Governance

## What Changed

- Refreshed the Fabric parity baseline with the corrected KPI capture from Warehouse block 2.
- Updated `06-fabric-sync/state/parity/parity_fabric_latest.json` with decimal KPI values for:
  - `avg_delivery_time_days`
  - `avg_review_score`
- Reran `fabric_parity_compare.py` and generated a clean `PASS` report.

## Why It Changed

- Close the architecture-first validation gate before any public dashboard or case-study publication step.
- Confirm that Fabric Warehouse outputs now match the local DuckDB baseline within the defined KPI tolerances.

## Impact

- Data impact: No Fabric data mutation; this was a validation-only evidence refresh.
- Metric/report impact: Counts, QA checks, and all 10 KPI checks now pass local-vs-Fabric parity.
- Operational impact: The publication path is now unblocked for Power BI sharing and GitHub Pages registration.

## Validation Evidence

- Fabric inventory diff: `06-fabric-sync/state/fabric_inventory_diff_latest.md`
- Snapshot file: `06-fabric-sync/state/history/fabric_inventory_20260314_005701Z.json`
- Additional checks:
  - `python3 06-fabric-sync/fabric_parity_compare.py --local 06-fabric-sync/state/parity/parity_local_latest.json --fabric 06-fabric-sync/state/parity/parity_fabric_latest.json --out-json 06-fabric-sync/state/parity/parity_compare_latest.json --out-md 06-fabric-sync/state/parity/parity_compare_latest.md`
  - Result: `Status: PASS`
  - Comparator summary: counts `10/10`, QA `36/36`, KPIs `10/10`

## Linked Local Artifacts

- SQL:
  - `06-fabric-sync/sql/fabric-warehouse/40_parity_query_pack.sql`
- Docs:
  - `06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md`
  - `06-fabric-sync/state/parity/parity_fabric_latest.json`
  - `06-fabric-sync/state/parity/parity_compare_latest.json`
  - `06-fabric-sync/state/parity/parity_compare_latest.md`
  - `05-docs/project-memory/PROJECT_STATUS.md`
  - `05-docs/project-memory/NEXT_ACTIONS.md`
  - `05-docs/project-memory/RESUME_NEXT_SESSION.md`
- Notebooks: N/A

## Risks and Follow-Up

- Residual risks:
  - Public sharing configuration for Power BI is still pending.
  - Troubleshooting-era credentials still require rotation and cleanup confirmation.
  - Future Fabric-side model changes can drift from this `PASS` baseline if parity artifacts are not refreshed.
- Next actions:
  - Publish the first Power BI report and attach the live link to the case study.
  - Enable GitHub Pages and register the final case-study URL in the root README.
  - Rotate PAT and Entra app secret, then confirm Azure DevOps uses fresh secret values only.
