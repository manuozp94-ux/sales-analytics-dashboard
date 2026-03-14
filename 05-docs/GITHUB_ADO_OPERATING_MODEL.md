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

## Warehouse SQL Apply Boundary

- GitHub/repo remains the source of truth for Warehouse SQL under `06-fabric-sync/sql/fabric-warehouse/`.
- `sqlcmd` is the CLI execution interface for applying those SQL files to Fabric Warehouse.
- `sqlcmd` can run:
  - locally from a terminal, or
  - inside an Azure DevOps agent job.
- In both cases, the command runs on the host machine/agent while the SQL executes in the remote Fabric Warehouse.
- Current Azure DevOps pipeline stages focus on Fabric REST deploy/probe operations.
- Warehouse SQL apply is now scaffolded via `06-fabric-sync/scripts/apply_warehouse_sql_pack.sh` so the same execution path can be reused later in DevOps without duplicating the script order in YAML.

## Work Tracking Standard

- Each weekly milestone has:
  - one roadmap checkpoint,
  - one `portfolio-week-XX` tag,
  - linked Board items and PRs.

## Cross-Linking Standard

- PR descriptions should include linked Board item IDs.
- Board items should include PR links and evidence links.
