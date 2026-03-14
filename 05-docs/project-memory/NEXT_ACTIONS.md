# NEXT_ACTIONS

## Last Updated (UTC)

- 2026-03-14

## Top 3 Actions

| Priority | Action | Owner | ETA | Definition of Done |
|---|---|---|---|---|
| P0 | Polish and finalize Page 1 of the Power BI report | Manuel Antonio Orozco | Next session | Executive overview page has consistent labels/formatting, KPI cards are clean, and the monthly charts are presentation-ready |
| P1 | Build Pages 2 and 3 from the cohort and customer marts | Manuel Antonio Orozco | Week 2 | Cohort retention page and customer value page both exist and are sourced from the Fabric marts |
| P2 | Publish the first Power BI report and register final public URLs in the case study + root README | Manuel Antonio Orozco | Week 2 | Report is shared, the live URL is added to `05-docs/case-study/CASE_STUDY_DRAFT.md`, and root `README.md` contains the final public case-study/dashboard links |

## Backlog (Short Horizon)

- Keep `warehouse_probe` pipeline stage as pre-flight before major model changes.
- Decide whether to wire `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh` into Azure DevOps after one or two successful local uses.
- Post-MVP, promote the local Warehouse SQL apply path into Azure DevOps with a real `warehouse_sql_apply` stage plus automated parity compare.
- Post-MVP, evaluate a Windows-based PBIP/PBIR workflow for code-driven report generation, since Power BI Desktop is not natively available on macOS.
- Before declaring the project complete, split `06-fabric-sync/sql/fabric-warehouse/` into deployable vs optional vs validation folders and update the apply scaffold to auto-discover only the deployable SQL files.
- Configure Azure DevOps board columns aligned to roadmap weeks.
- Start application tracker with target companies and submission dates.
- Set weekly certification checkpoint table for PL-300 and DP-600.
- Plan controlled cleanup path for previously tracked heavy artifacts.
- Keep commit/PR metadata aligned to `HISTORY_CURATION_STRATEGY.md` to simplify final readable-history rewrite.
- Upgrade cohort logic to `customer_unique_id` so retention metrics reflect repeat behavior.
- Keep Fabric deploy manifests aligned to active workspace IDs before each apply run.
- Keep `06-fabric-sync/state/parity/` artifacts updated at every major Fabric model cycle.
- Run `06-fabric-sync/sql/fabric-warehouse/02_drop_legacy_marts_schema_safe.sql` once if legacy schema `marts` still exists and is empty.
- Rotate troubleshooting-era credentials and refresh Azure DevOps secret variables after the reporting baseline is stabilized.

## Notes

- Keep this file focused on executable actions only.
- Replace completed items immediately to maintain continuity.
