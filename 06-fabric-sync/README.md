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

- The script is read-only for Fabric artifacts.
- Default REST endpoint: `https://api.fabric.microsoft.com`.
- If the API response is paginated, the script follows `continuationUri`, `nextLink`, or `continuationToken`.
