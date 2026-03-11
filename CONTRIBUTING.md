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

Examples:

- `feat: add monthly snapshot mart validation`
- `docs: update roadmap with week-2 portfolio targets`

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
- Notebook JSON sanity checks.
- Markdown relative link checks.
- Artifact policy checks (heavy file guardrails).

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

## Fabric Evidence Requirement

After each major Fabric change (pipelines, schema/core model, marts, semantic model, security):

1. Run a Fabric inventory snapshot using `fabric_sync.py`.
2. Add a short markdown note under `06-fabric-sync/notes/`.
3. Link affected local SQL/docs/notebooks in that note.

## Documentation Voice

- Keep a professional senior-analyst style with explicit assumptions and validation evidence.
- Focus on business impact and engineering tradeoffs.
- Do not include internal tooling/process wording in public portfolio docs.
