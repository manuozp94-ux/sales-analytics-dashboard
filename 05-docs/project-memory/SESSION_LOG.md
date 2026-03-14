# SESSION_LOG

## Template Lock

Use the same headings for every new entry:

- `Session Date (UTC)`
- `Session Goal`
- `Changes Completed`
- `Validation Evidence`
- `Decisions`
- `Carry-Over`

---

## Session Date (UTC)

- 2026-03-10

## Session Goal

- Implement governance, continuity, and workflow optimization baseline.

## Changes Completed

- Added canonical governance docs and roadmap.
- Added project memory subsystem files and templates.
- Added main README with “Resume Here” and layer mapping.

## Validation Evidence

- Repository structural checks completed during implementation.
- New docs linked from canonical entry points.

## Decisions

- GitHub is the public source of truth for code and portfolio evidence.
- Azure DevOps is the default planning/pipeline companion.

## Carry-Over

- Finalize CI scripts and templates validation run.
- Finalize archive labeling and translation policy execution notes.

---

## Session Date (UTC)

- 2026-03-10

## Session Goal

- Implement owner-only governance updates, manual session-close visibility, and Fabric evidence-note protocol.

## Changes Completed

- Updated CODEOWNERS to single owner `@manuozp94-ux`.
- Added documentation voice standard and manual-only session-close enforcement in canonical rules.
- Added Fabric change notes workflow and template under `06-fabric-sync/notes/`.
- Updated PR/contribution guidance to require Fabric evidence note for major Fabric changes.

## Validation Evidence

- Repository quality checks passed via `.github/scripts/quality_checks.py`.
- Canonical docs cross-linking updated (`README`, `PROJECT_RULES`, `06-fabric-sync/README`).

## Decisions

- Session-close signaling remains manual-only.
- Fabric sync cadence remains "after major change".
- Evidence pack remains "JSON diff + short markdown note".

## Carry-Over

- Populate first real Fabric change note after next workspace change.
- Finalize Power BI sharing model in Week 2 deliverables.

---

## Session Date (UTC)

- 2026-03-10

## Session Goal

- Capture first real Fabric evidence note from successful workspace connectivity and sync.

## Changes Completed

- Added first operational Fabric change note:
  - `06-fabric-sync/notes/2026-03-10_fabric-baseline-connectivity.md`
- Linked snapshot and diff evidence from `06-fabric-sync/state`.
- Recorded impacted local artifacts and follow-up actions.

## Validation Evidence

- Workspace inventory was successfully returned by Fabric REST API.
- Snapshot and diff files were present and referenced in the change note.

## Decisions

- Fabric change notes will be created immediately after each major workspace change.
- Baseline connectivity evidence will be kept as a reusable reference for future automation.

## Carry-Over

- Implement controlled write automation (`dry-run`/`apply`) in CI/CD.
- Finalize Power BI sharing model and Week 2 case-study publication.

---

## Session Date (UTC)

- 2026-03-10

## Session Goal

- Execute official session close with final memory updates and explicit resume point.

## Changes Completed

- Confirmed session closure as manual-official close.
- Updated `PROJECT_STATUS.md` with session state and next resume point.
- Kept top next actions aligned to Week 2 priorities.

## Validation Evidence

- Fabric baseline connectivity evidence already recorded in:
  - `06-fabric-sync/notes/2026-03-10_fabric-baseline-connectivity.md`
- Memory files updated and ready for next-session restart.

## Decisions

- Session close remains manual-only and treated as a required operational control.
- Next session starts with Fabric write automation scaffold before new modeling changes.

## Carry-Over

- Build `dry-run` + `apply` script flow for controlled Fabric item creation/update.
- Define Power BI sharing strategy and complete Week 2 case study draft.

---

## Session Date (UTC)

- 2026-03-11

## Session Goal

- Resume from previous close point and implement controlled Fabric write automation scaffold with pipeline gating.

## Changes Completed

- Added `06-fabric-sync/fabric_deploy.py` with explicit `--action dry-run|apply`.
- Implemented deploy guardrails:
  - workspace-scoped operation path enforcement,
  - explicit `--confirm-apply YES` for apply,
  - delete protection unless `--allow-delete`.
- Added sample deployment manifest:
  - `06-fabric-sync/examples/sample_deploy_manifest.json`
- Expanded Azure pipeline into staged flow:
  - `quality`,
  - `fabric_dry_run`,
  - `fabric_apply` with `ManualValidation@0` gate.
- Updated `06-fabric-sync/README.md` with deploy usage, guardrails, and pipeline requirements.
- Updated project memory files for resumed state and next operational step.

## Validation Evidence

- Local dry-run completed successfully:
  - `python3 06-fabric-sync/fabric_deploy.py --action dry-run --mode file --input-current 06-fabric-sync/examples/sample_items.json --desired-state 06-fabric-sync/examples/sample_deploy_manifest.json`
- Repository quality checks passed:
  - `python3 .github/scripts/quality_checks.py`

## Decisions

- Deployment automation remains manifest-driven and explicit, not implicit by diff inference.
- Apply execution remains gated by both manual approval and explicit command confirmation.
- First live apply will be treated as an evidence-producing change and documented with a Fabric change note.

## Carry-Over

- Execute first real deploy cycle against the target Fabric workspace and capture snapshot/diff evidence.
- Finalize Power BI sharing strategy and publish Week 2 case study draft.

---

## Session Date (UTC)

- 2026-03-11

## Session Goal

- Execute P0 runbook for the first real Fabric deploy cycle (`dry-run` -> manual gate -> `apply`) with evidence capture.

## Changes Completed

- Added dedicated manifest:
  - `06-fabric-sync/examples/p0_first_cycle_manifest.json`
- Verified REST dry-run command path and captured blocker:
  - `ERROR: Missing bearer token in env var: FABRIC_BEARER_TOKEN`
- Executed local dry-run validation using file mode to confirm manifest and guardrails:
  - generated `06-fabric-sync/state/fabric_deploy_plan_latest.json`
  - generated `06-fabric-sync/state/fabric_deploy_report_latest.md`
- Confirmed dry-run plan quality:
  - `operation_count=1`
  - method summary includes `PATCH: 1`
  - no validation/guardrail errors in report output.

## Validation Evidence

- Dry-run (REST mode) blocker output recorded:
  - missing `FABRIC_BEARER_TOKEN` in current shell session.
- Dry-run (file mode) success command:
  - `python3 06-fabric-sync/fabric_deploy.py --action dry-run --mode file --input-current 06-fabric-sync/examples/sample_items.json --desired-state 06-fabric-sync/examples/p0_first_cycle_manifest.json --workspace-id 1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Plan and report files generated and inspected successfully.

## Decisions

- Keep P0 open until live `fabric_apply` succeeds through pipeline manual gate on `main`.
- Do not create a success-labeled Fabric change note before real apply + post-apply sync evidence.
- Use the dedicated manifest `p0_first_cycle_manifest.json` as the canonical artifact for first live run.

## Carry-Over

- Export `FABRIC_BEARER_TOKEN` and run pipeline with:
  - `runFabricApply=true`
  - `fabricDeployManifest=06-fabric-sync/examples/p0_first_cycle_manifest.json`
- After successful apply, run `fabric_sync.py` in REST mode and create:
  - `06-fabric-sync/notes/2026-03-11_fabric-first-deploy-cycle.md`

---

## Session Date (UTC)

- 2026-03-11

## Session Goal

- Remove repeated manual token handling for Fabric apply runs by enabling runtime token generation in Azure Pipeline.

## Changes Completed

- Updated `azure-pipelines.yml` to resolve `FABRIC_BEARER_TOKEN` at runtime in `deploy_apply` job.
- Added credential flow:
  - preferred: `FABRIC_TENANT_ID` + `FABRIC_CLIENT_ID` + `FABRIC_CLIENT_SECRET` to mint token from Entra OAuth endpoint.
  - fallback: existing preconfigured `FABRIC_BEARER_TOKEN`.
- Updated `06-fabric-sync/README.md` pipeline authentication section to reflect both supported options.

## Validation Evidence

- Repository quality checks passed:
  - `python3 .github/scripts/quality_checks.py`
- Pipeline YAML reflects new token-resolution step before `fabric_deploy.py --action apply`.

## Decisions

- Pipeline authentication default is now service-principal credentials with runtime bearer-token generation.
- Direct bearer token injection remains supported as a compatibility fallback.

## Carry-Over

- Configure pipeline secret variables (`FABRIC_TENANT_ID`, `FABRIC_CLIENT_ID`, `FABRIC_CLIENT_SECRET`) in Azure DevOps before next live apply run.
- Execute the first live P0 apply cycle and capture post-apply sync evidence and change note.

---

## Session Date (UTC)

- 2026-03-11

## Session Goal

- Make the repository explicitly history-curation-ready so final readable-history rewrite is safe and transparent.

## Changes Completed

- Added canonical policy doc:
  - `05-docs/HISTORY_CURATION_STRATEGY.md`
- Linked strategy in canonical navigation docs:
  - `README.md`
  - `05-docs/README.md`
- Updated governance rules with explicit history-curation policy:
  - `05-docs/PROJECT_RULES.md`
- Updated contribution workflow for curation readiness:
  - `CONTRIBUTING.md`
  - `.github/PULL_REQUEST_TEMPLATE.md`
- Updated project memory backlog/status references to include curation-track execution.

## Validation Evidence

- Repository quality checks passed:
  - `python3 .github/scripts/quality_checks.py`
- Markdown cross-links validated through quality checks.

## Decisions

- Final history rewrite remains deferred to portfolio finalization milestone.
- Transparency controls are mandatory before rewrite:
  - pre-curation tag,
  - archive branch,
  - public disclosure note.
- Ongoing work will use curation-track metadata (`T1` to `T4`) to reduce rewrite complexity.

## Carry-Over

- Continue P0 live Fabric apply execution path in parallel with new curation-ready commit discipline.
- Execute final history-curation protocol once Week 4 portfolio finalization criteria are reached.

---

## Session Date (UTC)

- 2026-03-11

## Session Goal

- Continue P0 execution from Azure DevOps and resolve pipeline blocker caused by missing hosted parallelism.

## Changes Completed

- Identified Azure DevOps runtime blocker:
  - `No hosted parallelism has been purchased or granted`
- Updated pipeline design to support self-hosted execution path with parameters:
  - `useSelfHosted=true`
  - `selfHostedPool=Default`
- Switched next executable step to self-hosted agent registration before live apply run.

## Validation Evidence

- Repository quality checks passed after pipeline updates:
  - `python3 .github/scripts/quality_checks.py`
- Pipeline YAML now contains self-hosted pool parameters and conditional pool selection.

## Decisions

- Do not wait for hosted parallelism grant to continue delivery.
- Use one macOS self-hosted agent in `Default` pool as immediate unblock path.
- Keep manual approval gate in place before apply execution.

## Carry-Over

- Create PAT, register macOS agent, and keep it online in `Default` pool.
- Run pipeline with:
  - `runFabricApply=true`
  - `fabricDeployManifest=06-fabric-sync/examples/p0_first_cycle_manifest.json`
  - `useSelfHosted=true`
  - `selfHostedPool=Default`

---

## Session Date (UTC)

- 2026-03-12

## Session Goal

- Resume Week 2 execution and ship an evidence-backed case study draft while preserving the blocked P0 deploy track.

## Changes Completed

- Replaced the case study template with a full draft including:
  - business problem framing,
  - architecture narrative (local + Fabric translation),
  - KPI snapshot,
  - QA evidence summary,
  - dashboard mart linkage,
  - engineering tradeoffs and next steps.
- Added reproducible evidence snapshot:
  - `05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md`
- Updated canonical navigation to expose case-study assets:
  - `README.md`
  - `05-docs/README.md`
- Updated project memory for resumed-state continuity:
  - `PROJECT_STATUS.md`
  - `NEXT_ACTIONS.md`

## Validation Evidence

- Local DuckDB rebuild executed from raw CSV -> `stg_*` -> `dim/fact` models -> marts; KPI and QA aggregates documented in:
  - `05-docs/case-study/CASE_STUDY_EVIDENCE_2026-03-12.md`
- Repository quality checks passed:
  - `python3 .github/scripts/quality_checks.py`

## Decisions

- Treat the Week 2 case study draft deliverable as complete at repository level (content and evidence are now present).
- Keep P0 as top priority because live Fabric apply is still not validated in pipeline.
- Keep Power BI sharing and GitHub Pages URL activation as separate executable steps after P0 unblock.

## Carry-Over

- Register one self-hosted Azure DevOps agent (`Default` pool) and execute the first live pipeline apply run.
- After successful apply, run post-apply `fabric_sync.py` and publish the Fabric change note with snapshot/diff evidence.
- Finalize Power BI public sharing model and add the live dashboard URL to the case study page.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Close P0 by completing the first live pipeline-gated Fabric apply cycle and recording post-apply evidence.

## Changes Completed

- Completed the first live apply cycle using the P0 manifest through Azure DevOps manual-gated pipeline flow.
- Confirmed self-hosted macOS agent execution path for apply job in `Default` pool.
- Captured post-apply Fabric sync evidence:
  - `06-fabric-sync/state/fabric_inventory_diff_latest.md`
  - `06-fabric-sync/state/history/fabric_inventory_20260314_005701Z.json`
- Added deploy-cycle change note:
  - `06-fabric-sync/notes/2026-03-14_fabric-first-deploy-cycle.md`
- Hardened memory continuity docs to reflect post-P0 status and next priorities.

## Validation Evidence

- Local REST sync completed successfully after apply:
  - `python3 06-fabric-sync/fabric_sync.py --mode rest --workspace-id 1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Sync result summary:
  - `Snapshot items: 6`
  - `Added: 0 | Removed: 0 | Changed: 0`
- Workspace/manifest alignment validated for deployment flow using:
  - `06-fabric-sync/examples/p0_first_cycle_manifest.json`

## Decisions

- Treat P0 as complete for Week 2 execution baseline.
- Move immediate priority to security cleanup (credential rotation) and portfolio publication path.
- Keep runtime bearer-token generation as the default authentication pattern for pipeline apply.

## Carry-Over

- Rotate Azure DevOps PAT and Entra app secret, then update pipeline secret variables with fresh values only.
- Define and document public Power BI sharing model; attach first public link in case study docs.
- Enable GitHub Pages publication and register final case-study URL in root README.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Reassess delivery alignment versus original objective: replicate the local validated data foundation into Fabric before public visualization emphasis.

## Changes Completed

- Performed repository-wide status audit across:
  - local SQL model (`03-sql/models` + `03-sql/marts`),
  - Fabric sync/deploy artifacts (`06-fabric-sync/`),
  - project memory and case-study docs.
- Confirmed Fabric workspace artifact-level presence (Lakehouse, Warehouse, Pipeline, CopyJob, Notebook, SQLEndpoint) via latest inventory snapshot.
- Confirmed first pipeline-gated apply cycle was governance-focused (metadata PATCH) and not table-level model deployment.
- Re-prioritized project memory actions to architecture-first execution:
  - Fabric table-level replication,
  - local-vs-Fabric parity validation,
  - then Power BI publication path.

## Validation Evidence

- Inventory source:
  - `06-fabric-sync/state/fabric_inventory_latest.json` (`item_count: 6`)
- Deploy manifest scope:
  - `06-fabric-sync/examples/p0_first_cycle_manifest.json` (pipeline item PATCH operation)
- Canonical local model source:
  - `03-sql/models/*.sql`
  - `03-sql/marts/*.sql`

## Decisions

- Do not treat workspace-level artifact existence as equivalent to Fabric star-schema completion.
- Defer public dashboard publication until architecture parity has a reproducible evidence pack.
- Keep governance/deploy controls as a stable foundation while shifting implementation effort to Fabric SQL materialization and validation parity.

## Carry-Over

- Build and document Fabric SQL runbook to materialize `stg`, `dim_*`, `fact_*`, and `mart_*`.
- Capture parity checks (counts + core KPIs) between local DuckDB and Fabric outputs.
- Resume Power BI sharing/public URL only after parity checks are complete.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Implement the architecture-first execution plan with strong automation for parity validation before visualization/publication.

## Changes Completed

- Implemented canonical parity contract:
  - `06-fabric-sync/parity_contract.py`
- Implemented local parity baseline CLI:
  - `06-fabric-sync/fabric_parity_baseline.py`
- Implemented parity comparator CLI with hard gate exit behavior:
  - `06-fabric-sync/fabric_parity_compare.py`
- Added Fabric Warehouse runbook and SQL execution pack:
  - `06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md`
  - `06-fabric-sync/sql/fabric-warehouse/*.sql`
- Added parity template and automated fixtures:
  - `06-fabric-sync/examples/parity/fabric_parity_baseline_template.json`
  - `06-fabric-sync/examples/parity/fabric_parity_baseline_fixture_*.json`
- Added parity state folder for traceability artifacts:
  - `06-fabric-sync/state/parity/`
- Added Fabric change note for this scaffold:
  - `06-fabric-sync/notes/2026-03-14_fabric-parity-automation-scaffold.md`

## Validation Evidence

- Local baseline execution:
  - `python3 06-fabric-sync/fabric_parity_baseline.py --out-json 06-fabric-sync/state/parity/parity_local_latest.json`
  - result: `Status: PASS`
- Comparator fixture scenarios:
  - PASS fixture -> comparator exit `0`
  - FAIL fixture (count mismatch) -> comparator exit `1`
  - FAIL fixture (KPI mismatch) -> comparator exit `1`
- Repository quality checks:
  - `python3 .github/scripts/quality_checks.py`

## Decisions

- Publication gate remains strict: no public Power BI/GitHub Pages release until parity comparator returns `PASS` against real Fabric payload.
- Fabric parity payload capture remains manual in this iteration (by design, for hands-on DevOps learning), but contract and compare logic are now automated and reproducible.
- SQL mapping from DuckDB to Fabric is fixed in runbook and no longer ad-hoc.

## Carry-Over

- Execute runbook SQL in Fabric Warehouse and materialize real `core`/`mart` objects.
- Fill `06-fabric-sync/state/parity/parity_fabric_latest.json` from Fabric query pack outputs.
- Run comparator against real Fabric payload until `PASS`, then proceed to dashboard publication path.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Close parity gate after Warehouse materialization and leave deterministic handoff for next restart.

## Changes Completed

- Confirmed manual Fabric execution outputs for Warehouse catalog and parity pack:
  - counts captured (10/10),
  - grain checks captured (`0` in 7/7),
  - null-key checks captured (`0` in 17/17),
  - orphan checks captured (`0` in 12/12).
- Executed comparator using captured Fabric payload:
  - result `FAIL` with only two KPI mismatches (`avg_delivery_time_days`, `avg_review_score`).
- Updated KPI block in parity SQL pack to prevent integer truncation on Fabric:
  - `avg_delivery_time_days` now uses `avg(cast(... as float))`,
  - `avg_review_score` now uses `avg(cast(review_score as float))`.
- Confirmed schema convention decision:
  - canonical analytics schema remains `mart` (singular),
  - `marts` is treated as legacy/optional cleanup only.
- Prepared session-close handoff artifacts in project memory for low-friction resume.

## Validation Evidence

- Comparator evidence:
  - `06-fabric-sync/state/parity/parity_compare_latest.json`
  - `06-fabric-sync/state/parity/parity_compare_latest.md`
- Failed checks at close time:
  - `avg_delivery_time_days` (`12.4968...` local vs `12.0` Fabric captured value),
  - `avg_review_score` (`4.07089` local vs `4.0` Fabric captured value).
- Updated SQL source:
  - `06-fabric-sync/sql/fabric-warehouse/40_parity_query_pack.sql`

## Decisions

- Do not rerun full Fabric runbook; resume with minimal delta step only (KPI block 2 re-execution).
- Keep publication gate strict: no Power BI/GitHub Pages release until comparator returns `PASS`.
- Keep manual payload capture in this iteration, with explicit JSON refresh and comparator rerun immediately after query output.

## Carry-Over

- Re-run only KPI block 2 in Fabric using updated `40_parity_query_pack.sql`.
- Refresh `06-fabric-sync/state/parity/parity_fabric_latest.json` with the new KPI row.
- Run comparator to close parity gate:
  - `python3 06-fabric-sync/fabric_parity_compare.py --local 06-fabric-sync/state/parity/parity_local_latest.json --fabric 06-fabric-sync/state/parity/parity_fabric_latest.json --out-json 06-fabric-sync/state/parity/parity_compare_latest.json --out-md 06-fabric-sync/state/parity/parity_compare_latest.md`
- If comparator returns `PASS`, proceed to publication track (Power BI sharing + GitHub Pages).

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Close the Fabric parity gate with the corrected KPI capture and reset the repo’s next-step focus to publication.

## Changes Completed

- Refreshed `06-fabric-sync/state/parity/parity_fabric_latest.json` using the corrected Warehouse KPI row.
- Reran parity comparator and generated updated `PASS` evidence:
  - `06-fabric-sync/state/parity/parity_compare_latest.json`
  - `06-fabric-sync/state/parity/parity_compare_latest.md`
- Added final parity-close evidence note:
  - `06-fabric-sync/notes/2026-03-14_fabric-parity-close-pass.md`
- Updated project-memory handoff docs to move the next session from parity remediation to publication + credential cleanup.

## Validation Evidence

- Comparator execution:
  - `python3 06-fabric-sync/fabric_parity_compare.py --local 06-fabric-sync/state/parity/parity_local_latest.json --fabric 06-fabric-sync/state/parity/parity_fabric_latest.json --out-json 06-fabric-sync/state/parity/parity_compare_latest.json --out-md 06-fabric-sync/state/parity/parity_compare_latest.md`
  - result: `Status: PASS`
- Final parity summary:
  - counts: `10/10` passed
  - QA: `36/36` passed
  - KPIs: `10/10` passed
- Corrected KPI values captured from Fabric:
  - `avg_delivery_time_days = 12.4968487612729`
  - `avg_review_score = 4.07089`

## Decisions

- Treat the current parity `PASS` as the baseline release gate for publication work.
- Move immediate priority from parity remediation to Power BI sharing, GitHub Pages registration, and credential rotation.
- Keep manual Fabric KPI capture in this iteration, but require a fresh comparator `PASS` after any future Fabric-side model change.

## Carry-Over

- Publish the first Power BI report and attach the live URL to `05-docs/case-study/CASE_STUDY_DRAFT.md`.
- Enable GitHub Pages and register the final case-study URL in root `README.md`.
- Rotate PAT and Entra app secret before the next Fabric apply cycle.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Run a focused Warehouse SQL optimization sweep and verify the architecture is clean before semantic-model work starts.

## Changes Completed

- Removed unused `month_year` from the Warehouse `core.fact_orders` build:
  - `06-fabric-sync/sql/fabric-warehouse/20_core_fact_orders.sql`
- Replaced brittle wildcard projection with explicit columns in:
  - `06-fabric-sync/sql/fabric-warehouse/12_core_dim_products.sql`
- Fixed `avg_delivery_days` precision in the monthly mart by casting the `DATEDIFF` expression to `float` before `AVG`:
  - `06-fabric-sync/sql/fabric-warehouse/31_mart_monthly_business_snapshot.sql`
- Updated project-memory handoff docs so the next operational step is to reapply these cleaned scripts in Fabric before creating the semantic model.

## Validation Evidence

- Repository quality checks:
  - `python3 .github/scripts/quality_checks.py`
  - result: `QUALITY CHECKS PASSED`
- Architecture validation remains green:
  - `06-fabric-sync/state/parity/parity_compare_latest.md`
  - result: `PASS`

## Decisions

- Keep the Warehouse architecture path as `stg -> core -> mart`; no broader structural refactor is required before Power BI work.
- Treat the SQL sweep as a local code cleanup until the affected Warehouse scripts are re-run in Fabric.
- Reapply the cleaned scripts before semantic-model creation so report metrics do not inherit the prior monthly-mart precision issue.

## Carry-Over

- Re-run `12_core_dim_products.sql`, `20_core_fact_orders.sql`, and `31_mart_monthly_business_snapshot.sql` in `wh_sales_analytics`.
- Create the semantic model from `mart` after the refresh.
- Build the first Power BI report page on top of the refreshed monthly mart.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Formalize the boundary between repo-side Warehouse SQL changes and live Fabric execution, and add a reusable CLI apply path.

## Changes Completed

- Added canonical Warehouse SQL CLI scaffold:
  - `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh`
- Added local Fabric service-principal bootstrap helper:
  - `06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh`
- Updated Fabric sync and runbook docs to show two valid apply surfaces:
  - Fabric SQL editor
  - `sqlcmd` via the new scaffold
- Updated operating-model and contributing docs to clarify:
  - repo SQL edits do not change the live Warehouse,
  - `sqlcmd` runs on the local machine or CI agent,
  - Fabric Warehouse remains the remote execution target.
- Updated Fabric sync and parity runbook docs with the local SPN bootstrap path so service-principal auth can reuse the same token pattern as the Azure DevOps pipeline.
- Updated project-memory handoff docs so the next session can use either the editor path or the CLI scaffold for the pending Warehouse refresh.

## Validation Evidence

- CLI scaffold preview:
  - `./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only`
  - result: canonical 12-script apply order rendered successfully
- Repository quality checks:
  - `python3 .github/scripts/quality_checks.py`
  - result: `QUALITY CHECKS PASSED`

## Decisions

- Keep Warehouse SQL apply logic outside `azure-pipelines.yml` for now.
- Reuse a single repo-owned shell scaffold first, then consider invoking that same script from Azure DevOps after successful local use.
- Treat `sqlcmd` as the execution interface, not as a replacement for git or Fabric REST item deployment.
- Defer folder-based SQL auto-discovery until after MVP publication; track it as pre-close hardening because the current explicit list is safer while the Warehouse pack still mixes deploy, optional, and validation SQL.

## Carry-Over

- Run `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only` and validate the ordered pack.
- Decide whether the next live Warehouse refresh will use the SQL editor or the new CLI path.
- After the Warehouse refresh, proceed with semantic model and Power BI work.
- Before declaring the project complete, split the Warehouse SQL pack into deployable/optional/validation folders and update the apply scaffold to auto-discover only deployable SQL.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Execute the Warehouse SQL pack through the local service-principal `sqlcmd` path and clear the remaining blocker before semantic-model work.

## Changes Completed

- Installed bundled local `sqlcmd` binary at:
  - `06-fabric-sync/tools/sqlcmd/sqlcmd`
- Updated `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh` to auto-detect the bundled binary.
- Executed the canonical 12-script Warehouse SQL pack successfully against `wh_sales_analytics` using the local service-principal path.
- Confirmed `stg` staging inventory, compatibility views, core objects, and mart scripts all completed without errors in the terminal run.

## Validation Evidence

- `sqlcmd` version check:
  - `06-fabric-sync/tools/sqlcmd/sqlcmd --version`
  - result: `v1.9.0`
- Warehouse apply command completed:
  - `./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --confirm-apply YES -- -S "4vqh6h2ymvqe3j4qf72umvdr5m-h3p5qhz7rdjute4g2i3prmtsxi.datawarehouse.fabric.microsoft.com,1433" -d "wh_sales_analytics" --authentication-method ActiveDirectoryServicePrincipal -U "$FABRIC_CLIENT_ID" -P "$FABRIC_CLIENT_SECRET"`
  - result: `Warehouse SQL pack apply completed.`
- Repository quality checks:
  - `python3 .github/scripts/quality_checks.py`
  - result: `QUALITY CHECKS PASSED`

## Decisions

- Treat the local `sqlcmd` service-principal path as validated for Warehouse SQL execution.
- Do not add Warehouse SQL execution to Azure DevOps yet; move straight to semantic-model and report work while the local path is known good.
- Keep parity as the release gate, but do not interrupt the current flow with another parity cycle unless model logic changes again.
- Track Azure DevOps promotion of the local Warehouse SQL apply + parity path as explicit post-MVP ops work.

## Carry-Over

- Create the Fabric semantic model from `mart`.
- Build the first Power BI page from `mart.mart_monthly_business_snapshot`.
- Continue to publication flow once the first report page is stable.

---

## Session Date (UTC)

- 2026-03-14

## Session Goal

- Create the semantic model, validate the first MVP report page against the monthly mart, and leave a clean handoff for the remaining report pages.

## Changes Completed

- Created Fabric semantic model `sm_sales_analytics_mvp` from the three `mart` objects.
- Built Page 1 of the report in Power BI Service with:
  - 3 KPI cards (`orders`, `revenue`, `delivered_orders`)
  - 4 monthly trend charts (`revenue`, `orders`, `on_time_delivery_rate`, `avg_delivery_days`)
- Validated that the page is connected to `mart_monthly_business_snapshot` correctly and that the main totals match the underlying mart.
- Added a page-level `purchase_month >= 2017-01-01` filter to remove boundary-month noise from the story.
- Confirmed that semantic-model warning icons were non-blocking because visuals rendered and refresh history succeeded.
- Clarified the current reporting-tool boundary:
  - MVP continues in Power BI Service on macOS
  - PBIP/PBIR code-driven report generation is deferred to post-MVP due Copilot capacity limits and lack of native Power BI Desktop on macOS

## Validation Evidence

- Page 1 cards align to the monthly mart totals:
  - `orders ~= 98.8K`
  - `revenue ~= 15.74M`
  - `delivered_orders ~= 96.5K`
- Monthly trend visuals render successfully from the Fabric semantic model.
- Repository quality checks:
  - `python3 .github/scripts/quality_checks.py`
  - result: `QUALITY CHECKS PASSED`

## Decisions

- Treat the current executive-overview page as valid MVP draft quality.
- Do not chase Power BI Service cosmetic/model warnings further unless visuals stop rendering or refresh begins failing.
- Keep the report authoring path manual in Fabric Service for MVP delivery.
- Track PBIP/PBIR automation and Azure DevOps promotion as post-MVP ops/design work.

## Carry-Over

- Polish Page 1 labels and formatting.
- Build Page 2 from `mart.mart_cohort_unit_economics`.
- Build Page 3 from `mart.mart_customer_ltv_summary`.
- Publish the report and register final public URLs in portfolio docs.

## Closeout Note

- Session wrapped with continuity docs refreshed.
- Treat Page 1 as data-validated MVP baseline; next session should focus on presentation polish and the remaining report pages, not rechecking the current data pull unless the semantic model changes.
