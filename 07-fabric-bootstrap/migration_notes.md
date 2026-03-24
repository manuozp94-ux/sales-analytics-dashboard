# Migration Notes

This file explains how another repository should adopt the Fabric workspace/authentication setup documented from this source repo.

## What Can Stay Standard

These patterns can be copied with little or no change:

- Use Entra service-principal client credentials as the canonical automation identity.
- Mint a short-lived Fabric bearer token at runtime instead of storing a long-lived bearer token.
- Keep REST operations workspace-scoped under `/v1/workspaces/{workspace_id}/...`.
- Keep Warehouse SQL execution separate from REST deploy logic.
- Keep write/apply paths human-gated.
- Keep a canonical SQL pack manifest and SQL guardrail scan if the new repo will manage Warehouse SQL.
- Keep secrets outside Git and use placeholder-only templates in the repo.
- Use `validate_access.sh` before first live connectivity testing.

## What Must Be Adapted

Replace every source-repo-specific target value:

- `FABRIC_WORKSPACE_ID`
- `FABRIC_WORKSPACE_NAME`
- `FABRIC_WAREHOUSE_NAME`
- `FABRIC_WAREHOUSE_DATABASE`
- `FABRIC_WAREHOUSE_SQL_ENDPOINT`
- any item IDs referenced in deploy manifests
- any CI variable names or secret-store references that are organization-specific

Adapt any behavior that is model-specific:

- Warehouse SQL files
- parity queries
- deploy manifests
- semantic-model assumptions
- report/security contracts

## What Must Not Be Copied As-Is

Do not copy these directly from the source repo into another live environment:

- workspace IDs
- item IDs
- warehouse endpoints
- historical state snapshots
- parity state files
- change-note evidence files
- sample manifests that point to existing workspace items
- any troubleshooting-era local commands that included live credentials

## Required Decisions Before Adoption

Make these decisions explicitly:

1. Which environment(s) can this repo target: `dev`, `test`, `prod`, or one workspace only?
2. Which service principal will own automation for this repo?
3. What workspace role will that identity receive?
4. Will the repo be read-only, SQL-deploying, REST-writing, or all three?
5. Where will secrets live locally and in CI?
6. Who approves write/apply steps?

## Recommended Adoption Path

1. Copy the whole `07-fabric-bootstrap/` folder into the new repo, or keep the same four files together under an equivalent folder.
2. Copy the Fabric helper scripts only if the new repo needs the same operating model:
   - `fabric_sync.py`
   - `fabric_deploy.py`
   - `fabric_warehouse_probe.py`
   - `scripts/bootstrap_fabric_service_principal.sh`
   - `scripts/apply_warehouse_sql_pack.sh`
   - `sql_pack_manifest.py`
   - `fabric_sql_guardrails.py`
3. Replace all environment-specific placeholders in `07-fabric-bootstrap/env.template` with the new repo’s approved values outside Git.
4. Create new deploy manifests with the new repo’s workspace and item IDs.
5. Run `./07-fabric-bootstrap/validate_access.sh` if you keep the same folder layout.
6. Run a live workspace bootstrap/read test before enabling any write path.
7. Add a manual approval gate before any REST apply or Warehouse SQL apply stage.

If you rename the folder, update any operator docs and command examples that reference `07-fabric-bootstrap/`.

## If the New Repo Only Needs Read Access

You can keep the package lighter:

- keep the service-principal token minting pattern,
- keep `fabric_sync.py` and optionally `fabric_warehouse_probe.py`,
- skip Warehouse SQL apply scripts,
- skip REST write manifests until needed.

## If the New Repo Also Needs Warehouse SQL Deployment

Keep these controls:

- canonical ordered SQL pack,
- guardrail scan before release,
- explicit `--confirm-apply YES`,
- environment-specific endpoint/database values,
- parity or equivalent validation after material changes.

## If the New Repo Wants Managed Identity Instead

Treat that as a deliberate redesign, not a drop-in copy.

Reason:

- the source repo does not implement managed identity,
- the helper scripts assume client credentials,
- the pipeline logic assumes runtime token minting from `tenant_id + client_id + client_secret`.

## Information You Still Need From the Workspace Owner

- tenant ID
- workspace ID per environment
- service principal client ID
- service principal secret handling method
- Fabric tenant policy for service principals
- workspace role assignment for the automation identity
- Warehouse SQL endpoint
- Warehouse database name

## Final Rule

Reuse the auth pattern and guardrails. Rebuild the environment-specific identifiers, manifests, and security assignments for the new repo from approved owner-supplied values.
