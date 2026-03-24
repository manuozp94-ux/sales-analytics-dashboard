# Project Rules (Canonical)

This document is the single source of truth for operating rules in this repository.

## 1. Language and Naming Policy

- Canonical content must be in **English**.
- Markdown docs, issue titles, PR titles, commit messages, and folder/file names must be in English.
- Historical conversational material may exist for traceability but is non-canonical.

## 2. Documentation Voice Standard

- Use a professional tone consistent with a senior Data Analyst transitioning into Analytics Engineering.
- Be explicit and instructional in canonical documentation.
- Always include:
  - assumptions,
  - validation evidence,
  - business interpretation,
  - implementation tradeoffs.
- Avoid casual/internal phrasing in public docs.
- Do not mention internal tooling/process details in public-facing portfolio documentation.

## 3. Artifact and Data Policy

- Follow a **metadata-only** policy for heavy artifacts.
- Do not track generated binaries or heavy exports (`.duckdb`, `.duckdb.wal`, `.zip`, large ad-hoc raw exports).
- Keep reproducibility through scripts, SQL, and documented execution steps.
- Use small sample assets only when needed for demonstration.

## 4. Definition of Done (All Work Items)

A task is done only when all conditions are met:

1. Reproducible execution path is documented.
2. Validation evidence is recorded (query output, checks, or QA status).
3. Canonical docs are updated.
4. Project memory files are updated:
   - `PROJECT_STATUS.md`
   - `SESSION_LOG.md`
   - `NEXT_ACTIONS.md`

## 5. Session-Close Ritual (Mandatory, Manual-Only)

Before ending any work session:

1. Update `PROJECT_STATUS.md` with current phase, blockers, outputs, and risks.
2. Append a new log entry in `SESSION_LOG.md`.
3. Refresh `NEXT_ACTIONS.md` with top 3 executable actions (owner + ETA).

This protocol is manual-only and non-optional.
If these files are not updated, the session is incomplete.

## 6. Collaboration and Branch Standards

- Use PR-based workflow for all non-trivial changes.
- Single maintainer ownership model:
  - Maintainer: Manuel Antonio Orozco
  - CODEOWNERS handle: `@manuozp94-ux`
- Branch naming:
  - `feature/<short-scope>`
  - `fix/<short-scope>`
  - `docs/<short-scope>`
  - `chore/<short-scope>`
- Commit style:
  - `feat: ...`
  - `fix: ...`
  - `docs: ...`
  - `chore: ...`
  - `ci: ...`
- Every PR must include:
  - objective,
  - data impact,
  - validation evidence,
  - docs/memory updates.

## 7. GitHub + Azure DevOps Operating Split

- GitHub:
  - public code repository,
  - branching and PR review,
  - community-visible portfolio evidence.
- Azure DevOps:
  - Boards for planning and delivery tracking,
  - Pipelines for enterprise-style CI/CD orchestration.

## 8. Fabric-to-Repo Evidence Protocol

Run Fabric sync after each major Fabric change:

- data pipelines,
- warehouse schema/core model,
- marts,
- semantic model,
- security/governance settings.

Minimum evidence pack required:

1. `fabric_sync.py` snapshot/diff JSON output.
2. One short markdown change note under `06-fabric-sync/notes/`.

Each Fabric change note must include links to impacted local artifacts (SQL, docs, or notebooks).

## 8.1 Fabric Consulting Standard

- Use `06-fabric-sync/FABRIC_CONSULTING_STANDARD.md` as the canonical operating standard for reusable Fabric client delivery.
- For client-ready or reusable delivery work, keep the contract bundle under `06-fabric-sync/contracts/` current.
- Treat environment, semantic-model, and governance contracts as delivery inputs, not optional afterthoughts.

## 9. Release Cadence

- Create one weekly milestone tag using `portfolio-week-XX`.
- Each weekly milestone should summarize:
  - what shipped,
  - what evidence was added,
  - what is next.

## 10. Canonical vs Archive Documentation

- Canonical governance documents:
  - `PROJECT_RULES.md` (this file)
  - `ROADMAP.md`
- Historical/conversational documentation under `context-consolidation` is archive material.
- Canonical updates must be reflected in English docs, not only in archived transcripts.

## 11. Git History Curation Policy

- This project may perform a final history curation pass for readability near portfolio finalization.
- Curation is allowed only under explicit transparency controls:
  - keep one published archive branch with original history,
  - keep one immutable pre-curation tag,
  - include a short disclosure note in canonical documentation.
- Ongoing work must remain curation-ready:
  - atomic commits,
  - no mixed unrelated scopes in one commit,
  - PR metadata includes one curation track label.
- Reference workflow: `05-docs/HISTORY_CURATION_STRATEGY.md`.

## 12. Optimization Sweep

Before proposing a commit, recommending session close, or marking non-trivial work complete:

1. Run a short optimization sweep.
2. Remove low-risk noise such as:
   - unused output columns,
   - redundant joins/aliases/CTEs,
   - stale compatibility branches that are no longer canonical,
   - verification fields that produce mostly null or low-value output.
3. Keep changes behavior-safe:
   - do not change business logic unless explicitly intended,
   - prefer simplification over broad refactors.
4. Re-run existing validation after the sweep when possible.
