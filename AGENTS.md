# Repository Agent Instructions

## Optimization Sweep

For any non-trivial change, and always before proposing a commit or declaring a session complete, perform a brief optimization sweep.

Review for:

- unused selected columns, variables, joins, CTEs, or debug outputs,
- verification/probe fields that add noise without decision value,
- duplicate or legacy paths that are no longer canonical,
- comments or runbook steps that no longer match real behavior,
- avoidable null-heavy output in operational SQL scripts.

Default behavior:

- make safe, low-risk cleanups directly,
- call out higher-risk refactors separately before changing behavior,
- rerun existing validation after cleanup when possible.

If the user asks for a review, include unnecessary information/noise reduction as part of the review, after correctness and regression risks.
