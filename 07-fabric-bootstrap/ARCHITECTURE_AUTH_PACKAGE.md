# Fabric Workspace Bootstrap Package

This package documents the Microsoft Fabric connection and authentication model inferred from this repository so another repository can adopt the same pattern without copying secrets.

## Confidence Legend

- `Confirmed`: directly evidenced by code, pipeline YAML, state files, or runbooks in this repo.
- `Inference`: strongly implied by working automation, but the exact tenant/workspace setting is not spelled out in the repo.
- `Unknown`: not recoverable from the repo and must be supplied by the platform/workspace owner.

## System Overview

### Confirmed

- The repo uses a split connection model:
  - Fabric REST API for workspace inventory, metadata probes, and guarded item-level deploy operations.
  - Warehouse SQL connectivity for schema/model materialization through `sqlcmd`.
- The observed Fabric workspace contains these top-level item types:
  - `Lakehouse`
  - `SQLEndpoint`
  - `Warehouse`
  - `Notebook`
  - `DataPipeline`
  - `CopyJob`
- The repo treats Warehouse SQL as repo-first source of truth and applies it to Fabric only through an explicit execution step.
- Fabric writes are intentionally human-gated.
- The canonical authentication pattern is Entra service-principal client credentials that mint a short-lived Fabric bearer token at runtime.

### Architecture Summary

| Plane | Purpose | Tooling | Auth Model | Confidence |
|---|---|---|---|---|
| Fabric REST | Inventory, probes, guarded write operations | `fabric_sync.py`, `fabric_deploy.py`, `fabric_warehouse_probe.py` | Bearer token for `https://api.fabric.microsoft.com` | `Confirmed` |
| Warehouse SQL | Build/update schemas, dimensions, facts, marts | `apply_warehouse_sql_pack.sh` + `sqlcmd` | Service principal via `ActiveDirectoryServicePrincipal` or equivalent caller-supplied auth | `Confirmed` |
| Local parity | Compare local baseline vs Fabric outputs | DuckDB + parity scripts | No Fabric auth for local baseline; Fabric SQL results captured separately | `Confirmed` |

## Fabric Workspace Connection Architecture

### Confirmed Flow

1. A caller supplies `FABRIC_TENANT_ID`, `FABRIC_CLIENT_ID`, and `FABRIC_CLIENT_SECRET`.
2. The repo mints a token from:
   - `https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token`
   - `grant_type=client_credentials`
   - `scope=https://api.fabric.microsoft.com/.default`
3. The token is used against workspace-scoped Fabric REST endpoints under:
   - `https://api.fabric.microsoft.com/v1/workspaces/<workspace-id>/...`
4. Warehouse SQL is applied separately with `sqlcmd` against the Fabric Warehouse SQL endpoint on port `1433`.
5. The same service principal credentials are reused for Warehouse SQL login in the documented local path.

### Confirmed Design Rules

- REST item paths must stay workspace-scoped.
- `DELETE` operations are blocked unless explicitly allowed.
- `apply` requires an explicit confirm flag.
- Warehouse SQL execution is separate from REST deployment and is not performed implicitly by editing SQL files in Git.
- The Warehouse SQL pack has a canonical ordered manifest and a guardrail scanner.

### Security Boundary Notes

- Keep tenant, workspace, and Warehouse identifiers environment-specific.
- Do not reuse live item IDs from this repo in another repo.
- Do not store bearer tokens, client secrets, or passwords in Git.
- Do not point a new repo at an existing production workspace without explicit workspace-owner approval.

## Authentication Flow

### Canonical Flow: Service Principal -> Runtime Fabric Token

| Step | Detail | Confidence |
|---|---|---|
| 1 | App/service principal credentials are read from environment or CI secret variables | `Confirmed` |
| 2 | Client credentials flow mints a short-lived token for Fabric REST | `Confirmed` |
| 3 | Token is used for workspace inventory/probe/deploy calls | `Confirmed` |
| 4 | Azure DevOps stores the runtime token in a secret pipeline variable for downstream steps | `Confirmed` |
| 5 | Local helper script validates service-principal reachability by calling the workspace-items endpoint | `Confirmed` |
| 6 | Warehouse SQL connectivity uses the same service principal identity via `sqlcmd` | `Confirmed` |

### Secondary Flow: Direct Bearer Token

- `FABRIC_BEARER_TOKEN` is supported by the REST scripts.
- The repo history shows this exists as a compatibility/manual path.
- The pipeline and later docs treat service-principal runtime token generation as the canonical path.
- This fallback is not the full repo-standard bootstrap for Warehouse SQL apply, which still depends on service-principal-style connectivity.

Confidence: `Confirmed`

### Managed Identity

- No managed identity implementation path was found in repo code, scripts, or pipeline YAML.

Confidence: `Confirmed`

## Required Environment Variables

Use placeholders only. Keep secrets out of Git. Store real secret values in a local secret manager, CI secret store, or shell profile excluded from version control.

### Core Auth

| Variable | Required | Purpose | Used By | Confidence |
|---|---|---|---|---|
| `FABRIC_TENANT_ID` | Yes for canonical path | Entra tenant for token minting | bootstrap helper, pipeline token generation | `Confirmed` |
| `FABRIC_CLIENT_ID` | Yes for canonical path | Service principal / app registration client ID | bootstrap helper, pipeline token generation, Warehouse SQL login | `Confirmed` |
| `FABRIC_CLIENT_SECRET` | Yes for canonical path | Client secret for service principal | bootstrap helper, pipeline token generation, Warehouse SQL login | `Confirmed` |
| `FABRIC_BEARER_TOKEN` | Optional manual fallback | Pre-minted Fabric bearer token | REST scripts in manual/local mode | `Confirmed` |
| `FABRIC_API_BASE_URL` | Optional | Override for Fabric API base URL; default is `https://api.fabric.microsoft.com` | REST scripts | `Confirmed` |

### Target Selection

| Variable | Required | Purpose | Confidence |
|---|---|---|---|
| `FABRIC_WORKSPACE_ID` | Yes | Target Fabric workspace for REST inventory, probes, and deploy operations | `Confirmed` |
| `FABRIC_WORKSPACE_NAME` | Optional but recommended | Human-readable workspace label for docs and operator checks | `Inference` |
| `FABRIC_WAREHOUSE_NAME` | Recommended | Friendly Warehouse item name used by runbooks and operators | `Confirmed` |
| `FABRIC_WAREHOUSE_DATABASE` | Yes for `sqlcmd` path | Database name passed to `sqlcmd -d` | `Confirmed` |
| `FABRIC_WAREHOUSE_SQL_ENDPOINT` | Yes for `sqlcmd` path | Remote Fabric Warehouse SQL endpoint host and port | `Confirmed` |

### Tooling

| Variable | Required | Purpose | Confidence |
|---|---|---|---|
| `SQLCMD_BIN` | Optional | Override path to `sqlcmd` if not on `PATH` or not using bundled binary | `Confirmed` |

### Variables Not Required By Default

- Item IDs should normally live in deploy manifests, not environment variables.
- Semantic-model settings are adjacent to this package but are not required to establish workspace/API access.

## Required Azure / Fabric / Entra Roles and Permissions

### Confirmed Access That Already Exists in the Source Repo

The identity used by this repo has enough permission to:

- mint a Fabric-scoped bearer token,
- list workspace items through Fabric REST,
- patch at least one workspace item through Fabric REST,
- access Warehouse metadata endpoints,
- authenticate to the Warehouse SQL endpoint,
- execute the canonical Warehouse SQL pack successfully.

### Minimum Access for a New Repo to Work Immediately

| Scope | Requirement | Confidence | Notes |
|---|---|---|---|
| Entra ID | An app registration/service principal that can obtain a token for `https://api.fabric.microsoft.com/.default` | `Inference` | Exact app permission/consent configuration is not documented in repo |
| Tenant/Fabric | Service principal usage must be allowed by tenant policy or tenant allowlist | `Inference` | Required because client-credential Fabric access works in this repo |
| Fabric Workspace | Grant the service principal a workspace role that supports item discovery and intended writes | `Inference` | Exact minimum role is not stated; use `Contributor` or higher for immediate success |
| Fabric Workspace | If the repo will only read inventory/probe data, a lower read-oriented role may be enough | `Inference` | Not proven by repo because the working identity also performed write/SQL tasks |
| Warehouse SQL | The same identity must be able to connect to the Warehouse endpoint and execute schema/model SQL | `Inference` | Exact SQL-level grant is not separately documented |
| CI/CD | Secret variables for tenant/client/secret/workspace must be available to the pipeline or runner | `Confirmed` | Present in `azure-pipelines.yml` |

### Exact Minimum Role Status

- Exact minimum Fabric workspace role: `Unknown`
- Exact SQL permission model inside the Warehouse: `Unknown`
- Exact tenant setting name or Entra group used to allow the service principal: `Unknown`

Use `Workspace Contributor` or higher as the safe bootstrap role unless the platform team validates a narrower role.

## Required Service Principals, App Registrations, or Managed Identities

### Confirmed

- A service principal/app registration is required for the canonical automated path.
- The source repo uses one service-principal credential set for both:
  - Fabric REST token minting
  - Warehouse SQL authentication

### Not Implemented

- Managed identity
- Azure CLI-dependent login flow
- Interactive user auth as the canonical automation path

### Unknown

- App registration display name
- Enterprise application object ID
- Whether separate non-prod/prod service principals already exist
- Whether the service principal is grouped through a tenant allowlist security group

## Repo-Level Prerequisites

### Required

- `bash`
- `python3`
- `curl`
- `git`
- `sqlcmd` available on `PATH` or a repo-bundled equivalent

### Required Repo Patterns to Copy if You Want the Same Operating Model

- Runtime token minting script or equivalent
- Workspace inventory script
- Guarded deploy script for REST writes
- Warehouse SQL apply script
- Ordered SQL manifest
- SQL guardrail check
- Manual approval gate in CI/CD

### Optional But Strongly Recommended

- Warehouse probe script
- Environment/governance contract templates
- Parity gate between local outputs and Fabric outputs

## Step-by-Step Setup Checklist

Follow these steps in order.

### 1. Establish the Security Boundary

- Choose the target tenant.
- Choose the target Fabric workspace.
- Choose whether the repo is allowed to touch `dev`, `test`, `prod`, or only one stage.
- Decide whether this repo is read-only, SQL-deploying, REST-writing, or all three.

### 2. Prepare the Service Principal

- Create or select an Entra app registration.
- Create or rotate a client secret outside Git.
- Ensure the app/service principal is allowed to obtain Fabric tokens in the tenant.
- Record only non-secret metadata in repo docs.

### 3. Grant Workspace Access

- Add the service principal to the target Fabric workspace.
- For immediate success, grant `Contributor` or higher unless a narrower role is validated by the platform owner.
- Confirm the identity is allowed to reach the Warehouse SQL endpoint if SQL apply is required.

### 4. Capture Non-Secret Configuration

- Copy `07-fabric-bootstrap/env.template` to your local secret-loading mechanism.
- Fill placeholders for:
  - workspace ID
  - workspace name
  - warehouse name
  - warehouse database
  - warehouse SQL endpoint
  - optional API base URL override

### 5. Store Secrets Safely

- Put `FABRIC_CLIENT_SECRET` in a secret store or CI secret variable.
- Do not commit `.env` files with live credentials.
- Do not store bearer tokens as long-lived repo variables.

### 6. Validate Local Assumptions

- Run:

```bash
./07-fabric-bootstrap/validate_access.sh
```

- Fix any missing or placeholder values before moving on.

### 7. Validate Live REST Reachability

- If you copied the helper scripts, run:

```bash
FABRIC_TENANT_ID="<tenant-id>" \
FABRIC_CLIENT_ID="<client-id>" \
FABRIC_CLIENT_SECRET="<client-secret>" \
FABRIC_WORKSPACE_ID="<workspace-id>" \
./06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh
```

Expected result:

- token acquisition succeeds,
- workspace-items call returns `200`,
- at least the expected workspace items are visible.

### 8. Validate Workspace Inventory

- Run:

```bash
python3 06-fabric-sync/fabric_sync.py \
  --mode rest \
  --workspace-id "$FABRIC_WORKSPACE_ID"
```

Expected result:

- a normalized workspace snapshot is produced,
- workspace item count is non-zero,
- item types match what the repo expects to operate on.

### 9. Validate Warehouse Connectivity

- Confirm `sqlcmd` is available:

```bash
${SQLCMD_BIN:-sqlcmd} --help >/dev/null
```

- Preview the canonical apply pack:

```bash
./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only
```

- Then validate SQL login using service principal auth in your environment-specific way.

### 10. Enable CI/CD Safely

- Add secret variables for:
  - `FABRIC_TENANT_ID`
  - `FABRIC_CLIENT_ID`
  - `FABRIC_CLIENT_SECRET`
- Add non-secret pipeline variables for:
  - `FABRIC_WORKSPACE_ID`
- Keep a manual approval gate in front of any write/apply stage.

## Validation Checklist

Mark each item `PASS` before treating the setup as ready.

- `./07-fabric-bootstrap/validate_access.sh` reports no missing required values.
- Service principal can mint a Fabric token successfully.
- `GET /v1/workspaces/<workspace-id>/items` succeeds.
- Workspace inventory contains the expected Fabric item types.
- Warehouse endpoint and database values are populated and not placeholder text.
- `sqlcmd` is available from the runner/host.
- Warehouse SQL authentication succeeds for the chosen identity.
- REST dry-run/deploy manifests use the correct workspace ID.
- Manual approval exists before write/apply stages.

## Troubleshooting

### `Missing required environment variable`

Likely cause:

- A required variable from `07-fabric-bootstrap/env.template` was never populated.

Fix:

- Fill the variable locally or in CI secrets.
- Re-run `./07-fabric-bootstrap/validate_access.sh`.

### `Failed to acquire Fabric bearer token`

Likely cause:

- Wrong tenant ID, client ID, or client secret.
- App is not allowed to request Fabric tokens.

Check:

- `FABRIC_TENANT_ID`
- `FABRIC_CLIENT_ID`
- `FABRIC_CLIENT_SECRET`
- tenant policy for service principals

### Fabric REST returns `401` or `403`

Likely cause:

- Token is valid but the identity is not allowed in the workspace.
- Workspace ID points to the wrong environment.

Check:

- `FABRIC_WORKSPACE_ID`
- workspace membership/role for the service principal
- tenant allowlist/group restrictions

### Fabric deploy fails with workspace mismatch

Likely cause:

- Manifest `workspace_id` does not match the CLI variable.

Fix:

- Keep manifest paths and `workspace_id` aligned to the same environment.

### `sqlcmd` authentication fails

Likely cause:

- Wrong endpoint, wrong database, unsupported auth mode, or insufficient Warehouse access.

Check:

- `FABRIC_WAREHOUSE_SQL_ENDPOINT`
- `FABRIC_WAREHOUSE_DATABASE`
- service principal SQL auth mode
- workspace/Warehouse access for the identity

### No Warehouse found in probe output

Likely cause:

- Wrong workspace ID, read-only inventory from the wrong workspace, or Warehouse item not created yet.

Fix:

- Verify workspace selection first.
- Create or locate the correct Warehouse before attempting SQL apply.

## Assumptions / Unknowns

### Confirmed Unknowns From Repo Analysis

- Exact minimum Fabric workspace role for the automation identity
- Exact Warehouse SQL permission grant model
- Exact app registration / enterprise app names
- Exact tenant allowlist/group configuration
- Exact non-prod/prod workspace topology in real use

### Working Assumptions Used in This Package

- Another repo wants the same auth model, not necessarily the same exact artifacts.
- Service-principal client credentials remain the standard path.
- The target repo may need both REST and Warehouse SQL planes.
- Human approval before write/apply remains a required control.

### Information That Must Come From the Platform or Workspace Owner

- Tenant ID
- Service principal client ID
- Service principal secret or secret-management path
- Workspace ID per environment
- Workspace role assignment decision
- Warehouse SQL endpoint
- Warehouse database name
- Any tenant policy or allowlist constraints for service principals

### Missing Information Matrix

| Missing Item | Why It Matters | Normally Comes From |
|---|---|---|
| Exact Fabric workspace role required for the automation identity | Determines least-privilege bootstrap for read vs write paths | Fabric workspace owner or Fabric platform admin |
| Exact Warehouse SQL permission model | Determines whether the identity can authenticate only, or also execute DDL/DML | Fabric workspace owner, SQL/Fabric administrator |
| Exact Entra app registration / enterprise app identity | Needed to onboard a new repo without guessing which app to reuse | Entra administrator or platform owner |
| Exact tenant setting / allowlist controlling service-principal Fabric access | Needed when token minting works in Entra but Fabric still denies access | Fabric tenant admin |
| Exact environment mapping for `dev/test/prod` workspaces | Needed to avoid crossing environment boundaries | Delivery lead, workspace owner, environment contract owner |

## Recommended Adoption Rule

Copy the connection pattern, not the live identifiers. Keep the auth flow, guardrails, and validation steps standard; replace every workspace-, warehouse-, item-, and environment-specific value with your own approved placeholders.
