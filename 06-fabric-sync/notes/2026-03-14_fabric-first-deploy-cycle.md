# Fabric Change Note

## Change Summary

- Date (UTC): 2026-03-14
- Workspace: `1fd8df3e-883f-49d3-9386-d236f8b272ba`
- Change Owner: Manuel Antonio Orozco
- Change Type:
  - Pipeline
  - Security/Governance

## What Changed

- Completed the first pipeline-gated Fabric apply cycle using the P0 manifest.
- Enforced self-hosted agent execution path and runtime token generation from service principal credentials.
- Executed post-apply `fabric_sync.py` snapshot/diff capture.

## Why It Changed

- Close P0 operational unblock and validate the guarded apply workflow in a real run.
- Ensure deploy evidence is captured in repository after pipeline apply execution.

## Impact

- Data impact: No inventory-level item delta was detected in the post-apply snapshot (`Added: 0, Removed: 0, Changed: 0`).
- Metric/report impact: No metric-contract change in this cycle.
- Operational impact: Deploy path is now validated with post-apply traceability artifacts.

## Validation Evidence

- Fabric inventory diff: `06-fabric-sync/state/fabric_inventory_diff_latest.md`
- Snapshot file: `06-fabric-sync/state/history/fabric_inventory_20260314_005701Z.json`
- Additional checks:
  - `fabric_sync.py --mode rest --workspace-id 1fd8df3e-883f-49d3-9386-d236f8b272ba` completed successfully after apply.
  - Workspace ID alignment validated between pipeline variable and deployment manifest.

## Linked Local Artifacts

- SQL: N/A
- Docs:
  - `06-fabric-sync/README.md`
  - `PROJECT_STATUS.md`
  - `SESSION_LOG.md`
- Notebooks: N/A

## Risks and Follow-Up

- Residual risks:
  - Troubleshooting-era credentials may still exist in local shell history or old variable values.
  - Apply stage remains dependent on valid service principal permissions in the target Fabric workspace.
- Next actions:
  - Rotate PAT and app secret, then confirm only fresh secret values are used in Azure DevOps variables.
  - Continue with Power BI sharing model definition and GitHub Pages publication path.
