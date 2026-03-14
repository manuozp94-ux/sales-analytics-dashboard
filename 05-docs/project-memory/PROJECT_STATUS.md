# PROJECT_STATUS

## Last Updated (UTC)

- 2026-03-14

## Session State

- Active Week 2 execution; Fabric model is materialized, parity gate is closed (`PASS`), the latest Warehouse SQL cleanup is live in Fabric, and the semantic model plus first MVP report page are now drafted in Power BI Service.

## Current Phase

- Week 2 execution in progress (Fabric architecture replication hardening before public visualization release).

## Current Sprint Goals

- Establish canonical governance docs and repo standards.
- Enable continuity system (`PROJECT_STATUS`, `SESSION_LOG`, `NEXT_ACTIONS`).
- Lock owner-only governance and documentation voice standard.
- Enforce Fabric evidence protocol (sync + change notes).

## Latest Outputs

- Canonical project rules created.
- Canonical roadmap created.
- Main README aligned to portfolio strategy and local/Fabric mapping.
- CODEOWNERS locked to `@manuozp94-ux`.
- Manual session-close checklist added to root README.
- Fabric change note template added under `06-fabric-sync/notes/`.
- First real Fabric baseline connectivity note created with snapshot and diff evidence.
- Fabric workspace API connectivity confirmed against workspace `1fd8df3e-883f-49d3-9386-d236f8b272ba`.
- Controlled deploy scaffold script added: `06-fabric-sync/fabric_deploy.py` (`dry-run` + `apply`).
- Deployment manifest example added: `06-fabric-sync/examples/sample_deploy_manifest.json`.
- Dedicated P0 manifest added: `06-fabric-sync/examples/p0_first_cycle_manifest.json`.
- P0 dry-run artifacts generated and validated:
  - `06-fabric-sync/state/fabric_deploy_plan_latest.json`
  - `06-fabric-sync/state/fabric_deploy_report_latest.md`
- Azure Pipeline expanded to stages: quality, deploy dry-run, deploy apply with manual approval gate.
- Azure Pipeline apply job now uses runtime token generation from service principal credentials (`FABRIC_TENANT_ID`, `FABRIC_CLIENT_ID`, `FABRIC_CLIENT_SECRET`) as the canonical auth path.
- Azure Pipeline now supports self-hosted pool execution path (`useSelfHosted=true`) to bypass hosted parallelism quota limits.
- Fabric sync bridge documentation updated with guarded deploy workflow and required pipeline variables.
- Canonical history-curation policy added:
  - `05-docs/HISTORY_CURATION_STRATEGY.md`
- Contribution and PR standards now include explicit curation-track metadata for future final history rewrite.
- Week 2 case study draft completed with architecture, KPI snapshot, QA evidence, and dashboard lineage:
  - `05-docs/case-study/CASE_STUDY_DRAFT.md`
- Reproducible case study evidence snapshot added:
  - `05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md`
- First pipeline-gated Fabric apply cycle executed against workspace `1fd8df3e-883f-49d3-9386-d236f8b272ba`.
- Post-apply Fabric sync evidence captured:
  - `06-fabric-sync/state/fabric_inventory_diff_latest.md`
  - `06-fabric-sync/state/history/fabric_inventory_20260314_005701Z.json`
- First deploy-cycle change note captured:
  - `06-fabric-sync/notes/2026-03-14_fabric-first-deploy-cycle.md`
- Azure Pipeline auth flow hardened to runtime token generation from service principal credentials only (no static bearer fallback in YAML).
- Repo status reassessment completed to realign priorities with the original objective (local validation base replication in Fabric).
- Parity contract code implemented:
  - `06-fabric-sync/parity_contract.py`
- Local parity baseline CLI implemented:
  - `06-fabric-sync/fabric_parity_baseline.py`
- Parity comparator CLI implemented:
  - `06-fabric-sync/fabric_parity_compare.py`
- Fabric Warehouse parity runbook and SQL pack added:
  - `06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md`
  - `06-fabric-sync/sql/fabric-warehouse/`
- Parity artifacts and fixtures initialized:
  - `06-fabric-sync/state/parity/parity_local_latest.json`
  - `06-fabric-sync/examples/parity/`
- New Fabric change note added for parity automation scaffold:
  - `06-fabric-sync/notes/2026-03-14_fabric-parity-automation-scaffold.md`
- Fabric Warehouse manual runbook execution confirmed with canonical objects in `core` + `mart`:
  - `dim_*`, `fact_*`, and `mart_*` objects present in Warehouse.
- Real Fabric parity capture completed for:
  - object counts (10/10),
  - QA grain checks (7/7 with `0` violations),
  - QA null-key checks (17/17 with `0` violations),
  - QA orphan checks (12/12 with `0` violations).
- Comparator executed against captured Fabric payload:
  - `06-fabric-sync/state/parity/parity_compare_latest.json`
  - `06-fabric-sync/state/parity/parity_compare_latest.md`
  - current result: `PASS` across counts, QA, and KPI checks.
- KPI precision fix applied to parity SQL pack:
  - `06-fabric-sync/sql/fabric-warehouse/40_parity_query_pack.sql`
  - `AVG` expressions now cast to `float` to avoid integer truncation.
- Final parity-close evidence note captured:
  - `06-fabric-sync/notes/2026-03-14_fabric-parity-close-pass.md`
- Low-risk Warehouse SQL optimization sweep applied locally:
  - removed unused `month_year` from `20_core_fact_orders.sql`,
  - replaced brittle wildcard projection in `12_core_dim_products.sql`,
  - fixed `avg_delivery_days` precision in `31_mart_monthly_business_snapshot.sql`.
- Warehouse SQL CLI apply scaffold added:
  - `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh`
  - repo/docs now distinguish local source edits from live Warehouse execution and define `sqlcmd` as the reusable apply interface.
- Local Fabric service-principal bootstrap helper added:
  - `06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh`
  - local SPN setup can now mirror the pipeline token bootstrap without requiring Azure CLI.
- Local bundled `sqlcmd` installed and verified at:
  - `06-fabric-sync/tools/sqlcmd/sqlcmd`
- Canonical Warehouse SQL pack successfully re-applied in Fabric through the local service-principal `sqlcmd` path:
  - `00_schema_bootstrap.sql`
  - `05_stg_compat_views.sql`
  - `10_core_dim_date.sql`
  - `11_core_dim_customers.sql`
  - `12_core_dim_products.sql`
  - `20_core_fact_orders.sql`
  - `21_core_fact_order_items.sql`
  - `22_core_fact_order_payments.sql`
  - `23_core_fact_order_reviews.sql`
  - `30_mart_cohort_unit_economics.sql`
  - `31_mart_monthly_business_snapshot.sql`
  - `32_mart_customer_ltv_summary.sql`
- Fabric semantic model created:
  - `sm_sales_analytics_mvp`
  - sourced from `mart_monthly_business_snapshot`, `mart_cohort_unit_economics`, and `mart_customer_ltv_summary`
- First Power BI report page drafted in Fabric Service:
  - executive overview layout created with 3 KPI cards and 4 monthly trend charts
  - page validated against monthly mart totals (`orders`, `revenue`, `delivered_orders`)
  - boundary-month visual noise reduced with `purchase_month >= 2017-01-01` page filter
- Current report authoring path confirmed:
  - manual Fabric/Power BI Service editing for MVP
  - code-driven PBIP/PBIR route remains post-MVP because Copilot capacity is unavailable and Power BI Desktop is not natively available on macOS

## Active Blockers

- Power BI Service sharing model is not finalized yet.
- Page 1 data pull is validated, but the executive overview still needs final polish on labels/formatting and Pages 2 and 3 are not built yet.
- GitHub Pages publication route for case-study URL is not enabled yet.
- Troubleshooting-era credentials (PAT/app secret) still require rotation and cleanup confirmation.

## Active Risks

- Historical archive content contains mixed language and mixed confidence notes.
- Heavy artifacts were previously tracked and need controlled cleanup strategy.
- Deployment manifest can drift from real workspace IDs if not kept aligned before apply.
- Stale pipeline secrets can reintroduce 401 auth failures even after a successful run if credential rotation is delayed.
- Future Fabric-side model changes can drift from the current `PASS` baseline if parity artifacts are not refreshed before public updates.
- Manual Fabric payload capture can introduce transcription errors if JSON is not filled carefully from query results.
- If legacy schema `marts` still exists in Warehouse, it can confuse validation and future model maintenance until it is retired.
- Building visuals before semantic-model field formatting and visual-level usage rules are set can create misleading KPI cards from non-additive mart fields.
- A future DevOps `sqlcmd` stage can fail if agent-side SQL tooling or connection/auth configuration drifts from the Warehouse endpoint requirements.
- As the mart surface grows, the current explicit file list in `apply_warehouse_sql_pack.sh` can become maintenance overhead until the SQL pack is split into deployable vs optional vs validation paths.
- Power BI Service formatting/modeling limits can slow down polish work on macOS until a Windows-based PBIP/PBIR path is available for post-MVP automation.

## Mitigation Actions

- Keep archive clearly marked as non-canonical.
- Enforce artifact policy in docs + quality checks for future changes.
- Require Fabric sync evidence notes for major workspace changes.
- Require dry-run review and manual approval before every apply execution.
- Keep deployment manifest workspace ID aligned before every apply execution.
- Prefer runtime bearer-token generation in pipeline over manually managed static bearer tokens.
- Keep ongoing commits/PRs aligned to curation tracks to reduce risk when final history rewrite is executed.
- Rotate PAT and service principal secret after troubleshooting-heavy sessions.
- Refresh `06-fabric-sync/state/parity/` artifacts after every major Fabric model change and keep the current `PASS` report as the release gate.
- Keep `mart` as the only canonical Warehouse schema and retire legacy `marts` with `02_drop_legacy_marts_schema_safe.sql` once confirmed safe.
- Require a fresh comparator `PASS` before any public metric claim is updated after future Fabric-side changes.
- Build the semantic model from the refreshed `mart` schema before continuing with report design so visuals inherit the current Warehouse definitions.
- Reuse `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh` as the canonical CLI path if Warehouse SQL execution is moved into Azure DevOps later.
- After MVP publication, promote the validated local `sqlcmd` path into Azure DevOps together with an automated parity gate so Warehouse SQL and publication controls share the same pipeline path.
- Keep MVP report authoring in Fabric Service on macOS; defer PBIP/PBIR code-driven reporting to a Windows-capable environment after publication.
- Before calling the project done, refactor the Warehouse SQL pack into deployable/optional/validation folders and switch the apply scaffold to folder-based discovery for deployable SQL only.

## Next Milestone

- `portfolio-week-02`: first public case study and dashboard-sharing baseline.

## Resume Point (Next Session)

- Start from `05-docs/project-memory/RESUME_NEXT_SESSION.md`.
- Continue from the validated executive overview page, polish it, then build pages 2 and 3 and move toward publication.
- Rotate PAT and Entra app secret before the next Fabric apply cycle so the current baseline is carried forward with fresh credentials only.
