# Fabric Sync (Workspace -> Repo)

This workflow stores a versionable inventory of Fabric workspace artifacts and generates a diff against the previous snapshot.

## Objective

- Connect what you build in Fabric (UI or API) with this repository.
- Keep commit-level traceability of artifact additions/changes/removals.
- Detect workspace drift across sessions.

## Consulting Standard and Contracts

Use these files when the workflow should behave like a reusable client-delivery accelerator instead of a one-off project:

- `06-fabric-sync/FABRIC_CONSULTING_STANDARD.md`
- `06-fabric-sync/contracts/`
- `07-fabric-bootstrap/`
- `06-fabric-sync/sql_pack_manifest.py`
- `06-fabric-sync/fabric_sql_guardrails.py`

What they add:

- one canonical operating standard for Warehouse-first vs hybrid Fabric delivery,
- starter contracts for engagement, environment, semantic model, and governance,
- one placeholder-safe onboarding package for other repos that need the same Fabric workspace/auth model,
- one source of truth for deployable vs optional vs validation SQL files,
- machine-enforced SQL guardrails for risky Fabric Warehouse schema evolution patterns.

## Generated Files

- `06-fabric-sync/state/fabric_inventory_latest.json`
- `06-fabric-sync/state/history/fabric_inventory_YYYYMMDD_HHMMSSZ.json`
- `06-fabric-sync/state/fabric_inventory_diff_latest.md`
- `06-fabric-sync/state/fabric_deploy_plan_latest.json` (deploy scaffold)
- `06-fabric-sync/state/fabric_deploy_report_latest.md` (deploy scaffold)
- `06-fabric-sync/state/parity/parity_local_latest.json`
- `06-fabric-sync/state/parity/parity_fabric_latest.json`
- `06-fabric-sync/state/parity/parity_compare_latest.json`
- `06-fabric-sync/state/parity/parity_compare_latest.md`

## Mode 1: Fabric API (Recommended)

1. Export a Fabric bearer token:

```bash
export FABRIC_BEARER_TOKEN="<your_token>"
```

2. Run sync:

```bash
python3 06-fabric-sync/fabric_sync.py \
  --mode rest \
  --workspace-id "<fabric_workspace_id>"
```

## Mode 2: Exported or Manual JSON

If you already have an items JSON payload (`items` or `value`):

```bash
python3 06-fabric-sync/fabric_sync.py \
  --mode file \
  --input 06-fabric-sync/examples/sample_items.json \
  --workspace-id "<optional_workspace_id>"
```

## Mode 3: Controlled Write Scaffold (`dry-run` + `apply`)

Use `fabric_deploy.py` for controlled, manifest-driven write automation.

1. Prepare a manifest (`operations[]`) from:
   - `06-fabric-sync/examples/sample_deploy_manifest.json`
2. Run dry-run against a local current-state file:

```bash
python3 06-fabric-sync/fabric_deploy.py \
  --action dry-run \
  --mode file \
  --input-current 06-fabric-sync/examples/sample_items.json \
  --desired-state 06-fabric-sync/examples/sample_deploy_manifest.json \
  --workspace-id "00000000-0000-0000-0000-000000000000"
```

3. Apply against Fabric REST (manual approval required in pipeline):

```bash
export FABRIC_BEARER_TOKEN="<your_token>"

python3 06-fabric-sync/fabric_deploy.py \
  --action apply \
  --confirm-apply YES \
  --mode rest \
  --workspace-id "<fabric_workspace_id>" \
  --desired-state 06-fabric-sync/examples/sample_deploy_manifest.json
```

Guardrails:

- Manifest paths must be workspace-scoped (`/v1/workspaces/{workspace_id}/...`).
- `DELETE` operations are blocked unless `--allow-delete` is explicitly passed.
- `apply` requires `--confirm-apply YES`.

## Mode 4: Warehouse SQL Apply Scaffold (`sqlcmd`)

Use `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh` when Warehouse SQL should be applied from the repo instead of manually running each file in the Fabric editor.

Preview the ordered pack:

```bash
./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only
```

Apply the canonical pack:

```bash
./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh \
  --confirm-apply YES \
  -- \
  -S "<warehouse_sql_endpoint>" \
  -d "wh_sales_analytics" \
  -U "<sql_user>" \
  -P "<sql_password>"
```

Important:

- `sqlcmd` belongs to the CLI/execution layer, not the Fabric UI.
- `sqlcmd` runs on the local machine or CI agent; the SQL executes in the remote Fabric Warehouse.
- Arguments after `--` are forwarded directly to `sqlcmd`, so authentication stays environment-specific.
- The ordered pack is resolved from `06-fabric-sync/sql_pack_manifest.py` so docs, quality checks, and the CLI share one source of truth.
- Optional cleanup/reset scripts stay opt-in:
  - `--include-legacy-cleanup`
  - `--include-reset`

Guardrail check for deployable SQL:

```bash
python3 06-fabric-sync/fabric_sql_guardrails.py
```

Current guardrail default:

- risky schema-evolution patterns such as `ALTER TABLE`, `ALTER COLUMN`, and constraint changes are blocked from the canonical deployable pack,
- one-time cleanup/reset stays outside the default path,
- validation SQL remains separate from materialization SQL.

Service principal note:

- If you want local service-principal auth without Azure CLI, first run:

```bash
FABRIC_TENANT_ID="<tenant-id>" \
FABRIC_CLIENT_ID="<client-id>" \
FABRIC_CLIENT_SECRET="<client-secret>" \
FABRIC_WORKSPACE_ID="1fd8df3e-883f-49d3-9386-d236f8b272ba" \
./06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh
```

- Then run the Warehouse apply:

```bash
./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh \
  --confirm-apply YES \
  -- \
  -S "4vqh6h2ymvqe3j4qf72umvdr5m-h3p5qhz7rdjute4g2i3prmtsxi.datawarehouse.fabric.microsoft.com,1433" \
  -d "wh_sales_analytics" \
  --authentication-method ActiveDirectoryServicePrincipal \
  -U "<client-id>" \
  -P "<client-secret>"
```

## Mode 5: Parity Baseline + Comparison Gate

Generate local baseline from DuckDB:

```bash
python3 06-fabric-sync/fabric_parity_baseline.py \
  --out-json 06-fabric-sync/state/parity/parity_local_latest.json
```

Generate Fabric parity payload manually (template + SQL query pack):

- Template: `06-fabric-sync/examples/parity/fabric_parity_baseline_template.json`
- SQL pack: `06-fabric-sync/sql/fabric-warehouse/40_parity_query_pack.sql`
- Output target: `06-fabric-sync/state/parity/parity_fabric_latest.json`

Run parity comparison:

```bash
python3 06-fabric-sync/fabric_parity_compare.py \
  --local 06-fabric-sync/state/parity/parity_local_latest.json \
  --fabric 06-fabric-sync/state/parity/parity_fabric_latest.json \
  --out-json 06-fabric-sync/state/parity/parity_compare_latest.json \
  --out-md 06-fabric-sync/state/parity/parity_compare_latest.md
```

Exit code semantics:

- `0` -> parity `PASS` (publication path can proceed)
- `1` -> parity `FAIL` (publication path is blocked until remediation)

Runbook:

- `06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md`

## Mode 6: Warehouse Probe (Inventory + Metadata Reachability)

Run locally (live REST mode):

```bash
export FABRIC_BEARER_TOKEN="<your_token>"

python3 06-fabric-sync/fabric_warehouse_probe.py \
  --mode rest \
  --workspace-id "<fabric_workspace_id>" \
  --output-json 06-fabric-sync/state/warehouse-probe/warehouse_probe_latest.json \
  --output-md 06-fabric-sync/state/warehouse-probe/warehouse_probe_latest.md
```

What it captures:

- workspace inventory focused on `Warehouse` and `SQLEndpoint` items,
- naming-rule scan (`snake_case`) on workspace item names,
- Warehouse REST metadata probes (`get`, `connectionString`, and catalog candidates),
- operator report for troubleshooting before parity remediation.

Important:

- This probe is workspace-item level evidence.
- Table/view/module definitions still require SQL-catalog query execution in Warehouse (`41_warehouse_catalog_probe.sql`).

## Azure Pipeline Integration

- `azure-pipelines.yml` now includes:
  - `quality` stage (repo checks),
  - `fabric_dry_run` stage (manifest validation),
  - `warehouse_probe` stage (warehouse metadata probe + artifact),
  - `fabric_apply` stage (manual approval + apply).
- Current pipeline does not apply Warehouse SQL by default.
- The Warehouse SQL scaffold lives in `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh` so the same execution path can be used locally first and later from an Azure DevOps agent.
- `fabric_apply` only runs when:
  - parameter `runFabricApply=true`,
  - branch is `main`,
  - manual approval is granted.
- `warehouse_probe` runs when:
  - parameter `runWarehouseProbe=true`,
  - branch is `main`.
- Required pipeline variables for apply:
  - `FABRIC_WORKSPACE_ID`
- Authentication path in pipeline:
  - `FABRIC_TENANT_ID`, `FABRIC_CLIENT_ID`, `FABRIC_CLIENT_SECRET` (secrets) -> token generated at runtime.

## Normalized Fields

Per artifact:

- `id`
- `name`
- `type`
- `workspace_id`
- `last_updated`

## Recommended Workflow

1. Change the repo SQL/docs or Fabric items intentionally.
2. Run repo validation, including `fabric_sql_guardrails.py`, and review the diff.
3. If this is a reusable/client-delivery cycle, update the contract bundle under `06-fabric-sync/contracts/`.
4. If Warehouse SQL changed, apply it in the Fabric editor or via `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh`.
5. If top-level Fabric items changed, run `fabric_sync.py` and review `fabric_inventory_diff_latest.md`.
6. Run local parity baseline (`fabric_parity_baseline.py`).
7. Capture Fabric parity payload and run `fabric_parity_compare.py`.
8. If parity status is `PASS`, continue to semantic-model or report publication steps.
9. Create a short change note in `06-fabric-sync/notes/` using `FABRIC_CHANGE_NOTE_TEMPLATE.md`.
10. Commit snapshot, parity artifacts, contracts, and notes with related SQL/notebook/doc changes.

## Required Standard

- Run one Fabric inventory snapshot for every major Fabric workspace change.
- Include the latest diff file in the same PR that introduces related updates.
- Include one Fabric change note with impact and validation context.

## Notes

- `fabric_sync.py` is read-only for Fabric artifacts.
- `fabric_deploy.py` is the controlled write scaffold and should be used behind manual approval.
- Default REST endpoint: `https://api.fabric.microsoft.com`.
- If the API response is paginated, the script follows `continuationUri`, `nextLink`, or `continuationToken`.
