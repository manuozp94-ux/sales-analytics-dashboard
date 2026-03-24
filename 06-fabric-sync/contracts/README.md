# Fabric Contract Bundle

This folder contains reusable contract templates for client-ready Fabric delivery.

## Purpose

Use these files when a project should move from one-off portfolio work into a repeatable consulting engagement.

They are designed to help agents and humans exchange structured requirements instead of relying on chat history or implicit repo knowledge.

## Templates

- `engagement_manifest.template.json`
  - client identity, delivery mode, architecture pattern, release policy.
- `environment_contract.template.json`
  - `dev/test/prod` workspaces, database targets, branches, stage-specific parameters, approvals.
- `semantic_model_contract.template.json`
  - semantic-model sources, fields, measures, formatting, relationships, report assumptions, security roles.
- `governance_pack.template.json`
  - workspace roles, identity strategy, RLS/CLS/OLS, labels, audit cadence, domains, residency.
- `release_bundle_checklist.md`
  - operator-facing checklist for what must exist before a client release is treated as complete.

## Operating Rules

- Keep contracts client-specific and commit-safe; never hardcode live secrets.
- Prefer repo references, logical IDs, and placeholders over copying credentials or temporary tokens.
- Treat these templates as the canonical starter set for new engagements until a client-specific contract is created.
- Keep Warehouse SQL as repo-first unless the engagement deliberately adopts Fabric Git/deployment-pipeline support.

## Related Standards

- `../FABRIC_CONSULTING_STANDARD.md`
- `../README.md`
- `../../07-fabric-bootstrap/ARCHITECTURE_AUTH_PACKAGE.md`
