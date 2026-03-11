# Git History Curation Strategy (Canonical)

This document defines how commit history will be curated for readability at project maturity while preserving technical honesty.

## 1. Intent

- Keep the learning journey real and traceable.
- Improve readability for hiring audiences at final release.
- Avoid presenting a false implementation timeline.

## 2. Transparency Rules (Non-Negotiable)

- Curated history must never hide material technical decisions.
- Before rewriting `main`, create and keep:
  - one immutable backup tag, and
  - one archive branch with the original history.
- Public documentation must disclose that history was curated for readability.

## 3. Curation Tracks

Use one track label for each work item to make final grouping deterministic:

- `T1-foundation`: governance, documentation standards, collaboration model.
- `T2-modeling`: SQL models, QA checks, marts, metric contract.
- `T3-fabric`: Fabric sync/deploy automation and evidence notes.
- `T4-portfolio`: case study, dashboard publication, navigation polish.

## 4. Working Rules From Now On

For each non-trivial change:

1. Keep commits atomic (one intent per commit).
2. Do not mix unrelated tracks in one commit.
3. Include track metadata in PR text under "History Curation Metadata".
4. Separate operational artifacts from logic/doc changes when feasible.
5. Record major decisions and evidence in `SESSION_LOG.md`.

## 5. End-of-Project Rewrite Protocol

Run this once, near portfolio finalization:

1. Create backup references from current `main`:
   - `git tag archive/pre-curation-YYYYMMDD`
   - `git branch archive/original-main-YYYYMMDD`
2. Create a curation branch from `main`.
3. Use interactive rebase/cherry-pick to produce milestone-oriented commits.
4. Validate repository quality checks and critical runbooks.
5. Update README with a short history-curation disclosure note.
6. Force-push curated history with `--force-with-lease`.
7. Keep archive branch/tag published and referenced.

## 6. Definition of Done for History Curation

History curation is complete when:

- curated `main` is readable by milestone/workstream,
- original history is still accessible through archive branch/tag,
- disclosure note exists in canonical docs,
- quality checks pass after rewrite.
