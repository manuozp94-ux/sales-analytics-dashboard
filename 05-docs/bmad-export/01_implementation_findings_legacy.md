# Implementation Findings Legacy

This document preserves the most useful implementation findings from the repository’s current stage: local analytics engineering, Microsoft Fabric translation, Azure DevOps delivery controls, and the professional lessons that came from doing the work end to end.

## Scope

This is not a full session log rewrite. It is a curated legacy layer based on the repo’s canonical evidence:

- `../project-memory/PROJECT_STATUS.md`
- `../project-memory/SESSION_LOG.md`
- `../../06-fabric-sync/notes/2026-03-10_fabric-baseline-connectivity.md`
- `../../06-fabric-sync/notes/2026-03-14_fabric-first-deploy-cycle.md`
- `../../06-fabric-sync/notes/2026-03-14_fabric-parity-automation-scaffold.md`
- `../../06-fabric-sync/notes/2026-03-14_fabric-parity-close-pass.md`
- `../../06-fabric-sync/README.md`

## 1. Fabric Connectivity And Identity

**Implemented**

- Service-principal authentication and Fabric REST workspace access were established.
- Workspace inventory retrieval was validated against the real Fabric workspace.
- Azure DevOps moved to runtime bearer-token generation from `FABRIC_TENANT_ID`, `FABRIC_CLIENT_ID`, and `FABRIC_CLIENT_SECRET`.
- A local bootstrap helper was created so the same auth pattern could be mirrored outside Azure CLI.

**Lesson**

- Runtime token generation is more reliable and professional than relying on manually exported bearer tokens.
- Identity and permission design should be treated as first-class architecture, not as late operational glue.

**Risk**

- Stale secrets, misaligned workspace permissions, or weak secret-rotation hygiene can silently destabilize deployment paths.

**Implication For The Next Repo**

- Start with an explicit identity contract, environment boundaries, secret ownership model, and tenant/workspace access assumptions before building delivery workflows.

## 2. Repo-To-Fabric Drift Control

**Implemented**

- `fabric_sync.py` was used to snapshot Fabric workspace state into the repository.
- Inventory diffs became part of the evidence protocol for major Fabric changes.

**Lesson**

- A repo needs a deliberate bridge back to Fabric state or it quickly becomes documentation-only fiction.

**Risk**

- Workspace changes can drift away from Git history if sync evidence is not captured after meaningful operations.

**Implication For The Next Repo**

- Treat state capture, evidence artifacts, and post-change notes as standard delivery controls, not optional documentation.

## 3. Guarded Deploy Workflow

**Implemented**

- A controlled Fabric REST deploy scaffold was added with explicit `dry-run` and `apply` modes.
- Workspace-scoped path validation, delete protection, and explicit apply confirmation were enforced.
- Azure DevOps adopted manual approval gates for live apply.

**Lesson**

- Delivery guardrails matter even in a learning-stage repo because they force clearer operational intent and reduce accidental writes.

**Risk**

- Manifest/workspace mismatch or over-trusting manual steps can still create operational errors.

**Implication For The Next Repo**

- Keep guarded deployment, but push earlier toward environment-aware contracts and stricter release-bundle validation.

## 4. Azure DevOps Pipeline Execution

**Implemented**

- A staged pipeline was established for quality checks, dry-run, Warehouse probe, and manual-gated apply.
- The hosted-agent limitation was identified and the workflow was adapted to a self-hosted pool path.

**Lesson**

- Delivery architecture includes pipeline realities: quotas, agent availability, and operational ownership are part of the design.

**Risk**

- Hosted/agent assumptions can block delivery even when application logic is correct.

**Implication For The Next Repo**

- Model runner and agent strategy as part of the system design from the start, especially if the repo depends on enterprise tooling or manual approvals.

## 5. Local vs Fabric Parity

**Implemented**

- A formal parity contract, local baseline generator, Fabric comparator, and PASS/FAIL gate were implemented.
- The parity path ultimately closed at `PASS` across counts, QA checks, and KPI checks.
- Precision issues were corrected in the parity SQL pack after real comparison surfaced them.

**Lesson**

- Architecture translation is not finished when SQL runs; it is finished when outputs match within defined tolerances.
- Validation logic should live near the delivery path, not only near local modeling.

**Risk**

- Manual Fabric payload capture remains error-prone.
- Future Fabric-side changes can drift silently if parity evidence is not refreshed.

**Implication For The Next Repo**

- Keep parity as a release gate, but reduce manual capture steps and move toward more structured automation and environment-aware validation.

## 6. Warehouse Materialization

**Implemented**

- A canonical Warehouse SQL pack, ordered manifest, and local `sqlcmd` apply path were created.
- The pack was successfully applied through the local service-principal path.
- Low-risk SQL cleanups were made after validation.

**Lesson**

- Editing SQL in Git and changing live Warehouse state are separate operational acts; making that boundary explicit improves delivery discipline.

**Risk**

- Tooling drift, endpoint/auth drift, or an aging explicit file list can erode reliability over time.

**Implication For The Next Repo**

- Preserve repo-first SQL and guardrails, but evolve toward cleaner deployable/optional/validation separation and stronger environment contracts.

## 7. Semantic Model And Reporting

**Implemented**

- A Fabric semantic model was created from the mart layer.
- The first MVP report page in Power BI Service was drafted and validated against mart totals.

**Lesson**

- The semantic/report layer exposes a separate lifecycle problem from data modeling: formatting, sharing, and environment-specific tooling matter.

**Risk**

- The semantic model path is still manual.
- macOS and Power BI Service constraints slow the move toward fully code-driven reporting.

**Implication For The Next Repo**

- Treat semantic-model lifecycle, field governance, and reporting automation as their own architectural track instead of a late presentation step.

## 8. Reusable Onboarding And Contracts

**Implemented**

- Reusable Fabric bootstrap documentation was created under `../../07-fabric-bootstrap/`.
- Reusable consulting-style contracts were introduced for environment, governance, semantic model, and release bundle expectations.

**Lesson**

- Reusability appears when you abstract environment assumptions, identities, and delivery rules out of chat history and into explicit artifacts.

**Risk**

- The contract layer exists, but it is not yet enforced at runtime.

**Implication For The Next Repo**

- Start from contracts and system boundaries earlier so the repo is architecture-led rather than retrofitted into structure later.

## 9. Capability Gaps Identified And Corrected

- Manual bearer-token handling -> corrected with runtime token generation.
- Ad hoc Fabric evidence -> corrected with sync snapshots and change notes.
- Local-only correctness assumptions -> corrected with parity automation and PASS/FAIL gating.
- Unclear Warehouse execution boundary -> corrected with a dedicated `sqlcmd` scaffold.
- Weak reusability story -> corrected with bootstrap and contract packages.

## 10. What A More Mature Practice Would Do Differently

- Start from architecture, environments, identity boundaries, and product/system briefs before optimizing for coding throughput.
- Treat delivery pipelines, release criteria, and evidence artifacts as part of the design from day one.
- Avoid waiting until late in the repo to formalize contracts, guardrails, and repo purpose.
- Reduce manual capture steps earlier, especially around parity and semantic-model lifecycle.
- Separate “learning a tool” from “designing a system” more deliberately.

## 11. Legacy Assets Worth Carrying Forward

- `../../06-fabric-sync/`
  - Fabric implementation, parity, and guarded delivery evidence.
- `../../07-fabric-bootstrap/`
  - reusable onboarding/auth package.
- `../../03-sql/`
  - local semantic foundation and marts.
- `../case-study/`
  - business-facing proof that the technical work supports analytical storytelling.
- `../project-memory/PROJECT_STATUS.md`
  - canonical snapshot of what was really achieved and what remained open.

## 12. Legacy Summary

This repository’s strongest legacy is not just that code was written. It is that the work evolved from local modeling into real Fabric delivery with evidence, then began to correct itself toward more professional patterns: identity design, release guardrails, parity validation, reusable contracts, and better repo-safe onboarding. That makes this repo worth preserving as a serious phase in a larger engineering trajectory.
