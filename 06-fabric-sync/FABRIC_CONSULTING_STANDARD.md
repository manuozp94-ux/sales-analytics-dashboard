# Fabric Consulting Standard

This document is the canonical operating standard for turning this repo into a reusable Fabric consulting accelerator.

## 1. Purpose

This standard defines:

- which Fabric practices are treated as mandatory,
- which remain preview-constrained and therefore optional,
- which repo defaults are opinionated delivery choices for consulting safety,
- which contracts every reusable engagement must provide before deployment.

## 2. Rule Classification

- `GA`: backed by generally available Microsoft Fabric guidance and safe to standardize broadly.
- `Preview`: supported by Microsoft guidance but still constrained by preview status or item-type limitations.
- `Repo default`: deliberate delivery rule for this consulting workflow, even when Fabric allows other paths.

## 3. Architecture Decision Rubric

### Warehouse-first (`GA` + repo default)

Use when:

- the workload is structured business/operations analytics,
- T-SQL is the main transformation language,
- facts, dimensions, marts, and semantic models are the primary outputs,
- multi-table SQL transactions or warehouse-native modeling are desired.

Default output:

- repo-first SQL models,
- Warehouse `stg/core/mart`,
- parity gate before BI publication,
- semantic-model contract tied to marts.

### Lakehouse + Warehouse hybrid (`GA`)

Use when:

- ingestion includes mixed structured/unstructured inputs,
- Delta landing and medallion-style raw/silver zones are important,
- data engineering and BI consumers share the same analytical estate,
- the client benefits from pairing Lakehouse ingestion with Warehouse serving.

Default output:

- Lakehouse for landing/curation,
- Warehouse for conformed SQL serving,
- semantic layer attached to curated marts.

### Semantic/report-only extension (`Repo default`)

Use when:

- a client already has a governed analytical store,
- the project is focused on metric definitions, semantic modeling, or reporting,
- there is no need to rebuild ingestion/modeling layers in the first engagement.

Default output:

- semantic-model contract,
- report assumptions and role requirements,
- lifecycle/governance review before publication.

## 4. Lifecycle Management Standard

- `GA`: isolate development from test and production with separate workspaces, permissions, and parameter values.
- `GA`: plan the Git and deployment permission model before releasing client content.
- `GA`: use parameters for values that change by stage.
- `Preview`: Fabric Git integration and Warehouse source control may be adopted when the item type and client scenario justify them.
- `Repo default`: keep this repo as the canonical source for Warehouse SQL until Warehouse Git/deployment behavior is mature enough for the engagement.
- `Repo default`: all Fabric writes remain human-gated.

## 5. Warehouse SQL Guardrail Policy

- `Repo default`: deployable Warehouse SQL must avoid schema-evolution statements that deserve reviewed migrations.
- `Preview`: treat `ALTER TABLE`, `ALTER COLUMN`, and constraint changes as unsafe in the canonical deployable pack because Microsoft documents data-loss risks in deployment/source-control workflows.
- `Repo default`: destructive or one-time cleanup actions belong in optional scripts, not in the default deployable pack.
- `Repo default`: validation queries belong in validation-only files and must not run as part of the materialization pack.

Enforcement path:

- canonical SQL pack selection comes from `06-fabric-sync/sql_pack_manifest.py`,
- deployable SQL guardrails are enforced by `06-fabric-sync/fabric_sql_guardrails.py`,
- repo quality checks fail if deployable SQL violates those rules.

## 6. Environment Contract Standard

Every reusable engagement must define:

- `dev`, `test`, and `prod` workspaces,
- per-stage warehouse/database targets,
- branch and release policy,
- parameter values that vary by stage,
- approvers for release and production deployment.

Template:

- `06-fabric-sync/contracts/environment_contract.template.json`

## 7. Semantic Model Standard

- `GA`: do not assume default semantic models are created automatically.
- `GA`: do not assume tables/views added to Warehouse automatically appear in the semantic model.
- `Repo default`: every client delivery must define the semantic layer explicitly through a contract, even when initial editing is manual.
- `Repo default`: semantic-model changes must record source marts, field formatting, measures, hidden fields, security roles, and report assumptions.

Template:

- `06-fabric-sync/contracts/semantic_model_contract.template.json`

## 8. Governance Pack Standard

Every client delivery must define:

- workspace-role strategy,
- item-sharing strategy,
- service principal or fixed-identity approach,
- RLS/CLS/OLS expectations,
- sensitivity-label approach,
- audit review cadence,
- domain/workspace ownership,
- region and data residency expectations.

Template:

- `06-fabric-sync/contracts/governance_pack.template.json`

## 9. Release Bundle Standard

Every deployment-ready engagement must produce a release bundle that includes:

- engagement manifest,
- environment contract,
- semantic-model contract,
- governance pack,
- SQL pack or deploy manifest,
- probe report,
- parity report,
- rollback notes,
- change log and operator sign-off.

Checklist:

- `06-fabric-sync/contracts/release_bundle_checklist.md`

## 10. Engagement Contract Bundle

Starter templates live under:

- `06-fabric-sync/contracts/`

Minimum starter set:

- `engagement_manifest.template.json`
- `environment_contract.template.json`
- `semantic_model_contract.template.json`
- `governance_pack.template.json`

## 11. Official Guidance Anchors

Microsoft Learn sources used to define this standard:

- Warehouse vs Lakehouse decision guide:
  - https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-lakehouse-warehouse
- Warehouse source control:
  - https://learn.microsoft.com/en-us/fabric/data-warehouse/source-control
- T-SQL surface area in Fabric Warehouse:
  - https://learn.microsoft.com/en-us/fabric/data-warehouse/tsql-surface-area
- Manage a Power BI semantic model:
  - https://learn.microsoft.com/en-us/fabric/data-warehouse/manage-semantic-model
- Best practices for lifecycle management:
  - https://learn.microsoft.com/en-us/power-bi/create-reports/deployment-pipelines-best-practices
- Governance and compliance overview:
  - https://learn.microsoft.com/en-us/fabric/governance/governance-compliance-overview
- Security overview:
  - https://learn.microsoft.com/en-us/fabric/security/security-overview

## 12. Repo Defaults Summary

These are intentional delivery defaults for this accelerator:

- repo-first Warehouse SQL,
- human-gated Fabric writes,
- parity gate before public metric publication,
- explicit semantic-model contract,
- explicit governance pack,
- structured release bundle for every reusable engagement.
