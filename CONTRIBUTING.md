# Contributing Guide

This repository is optimized for public portfolio evidence and reproducible analytics engineering workflows.

## Maintainer Model

- Single maintainer: **Manuel Antonio Orozco**.
- CODEOWNERS handle: `@manuozp94-ux`.
- Contributors (future) should still follow full PR and documentation standards.

## Branch Naming

Use one of these branch prefixes:

- `feature/<short-scope>`
- `fix/<short-scope>`
- `docs/<short-scope>`
- `chore/<short-scope>`
- `ci/<short-scope>`

## Commit Convention

Use concise conventional prefixes:

- `feat:`
- `fix:`
- `docs:`
- `chore:`
- `ci:`

Recommended format:

- `<type>(<scope>): <summary>`

Examples:

- `feat: add monthly snapshot mart validation`
- `docs: update roadmap with week-2 portfolio targets`
- `ci(fabric): add runtime token generation for deploy apply`

## History-Curation Readiness

This repo will run a final history-curation pass near portfolio finalization.  
To keep that process safe and transparent:

- Keep commits atomic (one intent per commit).
- Avoid mixing unrelated domains in one commit.
- Use one curation track label in PR metadata:
  - `T1-foundation`
  - `T2-modeling`
  - `T3-fabric`
  - `T4-portfolio`
- Keep original-history archive references when rewrite is executed.

See `05-docs/HISTORY_CURATION_STRATEGY.md` for full policy.

## Pull Request Standard

Every PR must include:

1. Objective.
2. Data impact.
3. Validation evidence.
4. Documentation updates.
5. Project memory updates (`PROJECT_STATUS`, `SESSION_LOG`, `NEXT_ACTIONS`).
6. Fabric evidence note when Fabric artifacts changed.

Use the repository PR template.

## Quality Gates

PRs should pass baseline checks for:

- SQL file quality checks.
- Fabric Warehouse SQL guardrail checks.
- Notebook JSON sanity checks.
- Markdown relative link checks.
- Artifact policy checks (heavy file guardrails).
- Contract template validation checks.

Before proposing a commit or closing a non-trivial work session, run one short optimization sweep:

- remove low-risk noise such as unused output columns, redundant joins/aliases/CTEs, and stale compatibility paths,
- simplify verification output when it adds mostly null or non-decision-useful information,
- rerun the existing validation path after cleanup when possible.

## Release Cadence

- Create one weekly milestone tag: `portfolio-week-XX`.
- Document what shipped, what evidence was added, and what is next.

## GitHub + Azure DevOps Split

- GitHub:
  - source of truth for code and portfolio evidence,
  - PR-based collaboration.
- Azure DevOps:
  - Boards for delivery planning,
  - Pipelines for enterprise-style orchestration.

## Warehouse SQL Apply Boundary

- Editing files under `06-fabric-sync/sql/fabric-warehouse/` changes the repo only.
- Live Warehouse changes happen only after those scripts are executed:
  - in the Fabric SQL editor, or
  - through `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh`.
- The canonical deployable file set is defined in `06-fabric-sync/sql_pack_manifest.py`.
- Run `python3 06-fabric-sync/fabric_sql_guardrails.py` before treating Warehouse SQL as ready for release.
- If `sqlcmd` is used, the command runs on the local machine or pipeline agent; Fabric Warehouse is the remote execution target.
- Re-run the parity path after material Warehouse SQL changes before treating Power BI outputs as current.

## Fabric Evidence Requirement

After each major Fabric change (pipelines, schema/core model, marts, semantic model, security):

1. Run a Fabric inventory snapshot using `fabric_sync.py`.
2. Add a short markdown note under `06-fabric-sync/notes/`.
3. Link affected local SQL/docs/notebooks in that note.

## Documentation Voice

- Keep a professional senior-analyst style with explicit assumptions and validation evidence.
- Focus on business impact and engineering tradeoffs.
- Do not include internal tooling/process wording in public portfolio docs.
