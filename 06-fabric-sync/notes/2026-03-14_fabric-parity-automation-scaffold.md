# Fabric Change Note

## Change Summary

- Date (UTC): 2026-03-14
- Workspace: `1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Change Owner: Manuel Antonio Orozco
- Change Type:
  - Pipeline
  - Schema/Core Model
  - Security/Governance

## What Changed

- Added a canonical parity contract for local vs Fabric validation.
- Added local baseline automation:
  - `fabric_parity_baseline.py`
- Added parity comparator with hard `PASS/FAIL` exit codes:
  - `fabric_parity_compare.py`
- Added Fabric Warehouse materialization + parity runbook and SQL pack:
  - schema bootstrap,
  - core model scripts,
  - mart scripts,
  - parity query pack.
- Added parity state folder, template payload, and comparator test fixtures.

## Why It Changed

- Enforce architecture-first execution and block public visualization unless Fabric parity is evidenced.
- Move from ad-hoc checks to reproducible, contract-driven parity validation.

## Impact

- Data impact: No direct workspace data mutation was executed by this repo change.
- Metric/report impact: KPI contract is now machine-checkable through parity artifacts.
- Operational impact: Dashboard publication path now depends on parity gate outcome (`PASS` required).

## Validation Evidence

- Local parity baseline generated:
  - `06-fabric-sync/state/parity/parity_local_latest.json`
- Comparator validation scenarios executed:
  - PASS fixture -> exit code `0`
  - FAIL fixture (count mismatch) -> exit code `1`
  - FAIL fixture (KPI mismatch) -> exit code `1`
- Quality checks:
  - `python3 .github/scripts/quality_checks.py`

## Linked Local Artifacts

- SQL:
  - `06-fabric-sync/sql/fabric-warehouse/`
- Docs:
  - `06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md`
  - `06-fabric-sync/README.md`
  - `05-docs/project-memory/PROJECT_STATUS.md`
  - `05-docs/project-memory/SESSION_LOG.md`
  - `05-docs/project-memory/NEXT_ACTIONS.md`
- Notebooks: N/A

## Risks and Follow-Up

- Residual risks:
  - Fabric parity still depends on manual Fabric SQL execution and correct payload capture.
  - Credential rotation is still pending.
- Next actions:
  - Execute runbook in Fabric and generate `parity_fabric_latest.json`.
  - Run comparator against real Fabric payload and remediate until parity `PASS`.
  - Proceed to Power BI publication only after parity `PASS`.
