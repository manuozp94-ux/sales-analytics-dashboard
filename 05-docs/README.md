# Technical Documentation Index

This folder is the canonical documentation surface for the repository. Use it to understand the model, the Fabric implementation path, the evidence trail, and the BMAD-oriented legacy package without having to read the full session log history.

## 1. Start Here

- [Root README](../README.md)
  - public portfolio entry point and high-level story.
- [BMAD Export Package](bmad-export/README.md)
  - curated legacy, findings, planning input, and portfolio-positioning assets.
- [Case Study Draft](case-study/CASE_STUDY_DRAFT.md)
  - business framing, KPI snapshot, QA evidence, and dashboard linkage.
- [Fabric Sync Bridge](../06-fabric-sync/README.md)
  - Fabric implementation workflow, guarded delivery, and validation path.

## 2. Architecture And Model

- [Star Schema](STAR_SCHEMA.md)
  - canonical grain, keys, and model structure.
- [Metric Contract](PHASE_4_METRIC_CONTRACT.md)
  - governed KPI definitions and business semantics.
- `../03-sql/models/`
  - dimensions and facts.
- `../03-sql/marts/`
  - dashboard-facing marts.
- `../02-notebooks/`
  - orchestration and validation support.

## 3. Fabric Implementation And Evidence

- [Fabric Warehouse Parity Runbook](../06-fabric-sync/RUNBOOK_FABRIC_WAREHOUSE_PARITY.md)
  - Warehouse materialization and parity workflow.
- [Fabric Change Notes](../06-fabric-sync/notes/README.md)
  - point-in-time evidence of implementation milestones.
- [Latest Parity Report](../06-fabric-sync/state/parity/parity_compare_latest.md)
  - current local-vs-Fabric validation result.
- [Fabric Bootstrap Package](../07-fabric-bootstrap/ARCHITECTURE_AUTH_PACKAGE.md)
  - reusable onboarding package for other repos.

## 4. BMAD And Transition Assets

- [BMAD Export Index](bmad-export/README.md)
- [Implementation Findings Legacy](bmad-export/01_implementation_findings_legacy.md)
- [BMAD Product Brief Input](bmad-export/02_bmad_product_brief_input.md)
- [Repo Transition Storyline](bmad-export/03_repo_transition_storyline.md)
- [Portfolio Positioning](bmad-export/04_portfolio_positioning.md)

These documents treat this repository as the first meaningful stage in a broader transition from code-first learning to architecture-first, agent-assisted platform delivery.

## 5. Portfolio Evidence

- [Case Study Evidence Snapshot](case-study/CASE_STUDY_EVIDENCE_2026-03-12.md)
- `case-study/pbi-source/`
  - exported mart data used for portfolio-facing Power BI evidence.
- [Roadmap](ROADMAP.md)
  - milestone framing and delivery intent.

## 6. Standards And Governance

- [Project Rules](PROJECT_RULES.md)
- [GitHub + Azure DevOps Operating Model](GITHUB_ADO_OPERATING_MODEL.md)
- [History Curation Strategy](HISTORY_CURATION_STRATEGY.md)
- [Fabric Consulting Standard](../06-fabric-sync/FABRIC_CONSULTING_STANDARD.md)
- [Fabric Contract Bundle](../06-fabric-sync/contracts/README.md)

## 7. Supporting Operational Memory

These files are important for continuity, but they are supporting artifacts rather than public-first docs:

- `project-memory/PROJECT_STATUS.md`
- `project-memory/SESSION_LOG.md`
- `project-memory/NEXT_ACTIONS.md`
- `project-memory/RESUME_NEXT_SESSION.md`

## 8. Historical Archive

`context-consolidation/` is a traceability archive. Use it when you need raw historical context, source conversations, or consolidation provenance. Do not treat it as the first place to understand the repository.
