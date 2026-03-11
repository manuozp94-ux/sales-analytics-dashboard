# GitHub + Azure DevOps Operating Model

This project uses a split collaboration model:

- **GitHub** as the public source of truth for code and portfolio visibility.
- **Azure DevOps** for enterprise-style planning and orchestration.

## Maintainer Context

- Current owner and maintainer: Manuel Antonio Orozco (`@manuozp94-ux`).
- Collaboration standards remain PR-based to preserve enterprise-readiness and future team scalability.

## Responsibility Split

## GitHub (Primary)

- Repository hosting (public).
- Branching and pull request reviews.
- Canonical code/documentation history.
- CI status visibility for external reviewers and recruiters.

## Azure DevOps (Companion)

- Boards:
  - backlog management,
  - sprint planning,
  - week-by-week milestone tracking.
- Pipelines:
  - enterprise-aligned execution orchestration,
  - optional deployment workflows for Fabric-facing automation.

## Work Tracking Standard

- Each weekly milestone has:
  - one roadmap checkpoint,
  - one `portfolio-week-XX` tag,
  - linked Board items and PRs.

## Cross-Linking Standard

- PR descriptions should include linked Board item IDs.
- Board items should include PR links and evidence links.
