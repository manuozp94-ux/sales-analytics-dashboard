# Fabric Sync (Workspace -> Repo)

This workflow stores a versionable inventory of Fabric workspace artifacts and generates a diff against the previous snapshot.

## Objective

- Connect what you build in Fabric (UI or API) with this repository.
- Keep commit-level traceability of artifact additions/changes/removals.
- Detect workspace drift across sessions.

## Generated Files

- `06-fabric-sync/state/fabric_inventory_latest.json`
- `06-fabric-sync/state/history/fabric_inventory_YYYYMMDD_HHMMSSZ.json`
- `06-fabric-sync/state/fabric_inventory_diff_latest.md`
- `06-fabric-sync/state/fabric_deploy_plan_latest.json` (deploy scaffold)
- `06-fabric-sync/state/fabric_deploy_report_latest.md` (deploy scaffold)

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

## Azure Pipeline Integration

- `azure-pipelines.yml` now includes:
  - `quality` stage (repo checks),
  - `fabric_dry_run` stage (manifest validation),
  - `fabric_apply` stage (manual approval + apply).
- `fabric_apply` only runs when:
  - parameter `runFabricApply=true`,
  - branch is `main`,
  - manual approval is granted.
- Required pipeline variables for apply:
  - `FABRIC_WORKSPACE_ID`
- Authentication options in pipeline:
  - Option A (recommended): `FABRIC_TENANT_ID`, `FABRIC_CLIENT_ID`, `FABRIC_CLIENT_SECRET` (secrets) and token is generated at runtime.
  - Option B: provide `FABRIC_BEARER_TOKEN` directly as a secret variable.

## Normalized Fields

Per artifact:

- `id`
- `name`
- `type`
- `workspace_id`
- `last_updated`

## Recommended Workflow

1. Complete a change in Fabric.
2. Run `fabric_sync.py`.
3. Review `fabric_inventory_diff_latest.md`.
4. Create a short change note in `06-fabric-sync/notes/` using `FABRIC_CHANGE_NOTE_TEMPLATE.md`.
5. Commit snapshot, diff, and note with related SQL/notebook/doc changes.

## Required Standard

- Run one Fabric inventory snapshot for every major Fabric workspace change.
- Include the latest diff file in the same PR that introduces related updates.
- Include one Fabric change note with impact and validation context.

## Notes

- `fabric_sync.py` is read-only for Fabric artifacts.
- `fabric_deploy.py` is the controlled write scaffold and should be used behind manual approval.
- Default REST endpoint: `https://api.fabric.microsoft.com`.
- If the API response is paginated, the script follows `continuationUri`, `nextLink`, or `continuationToken`.
