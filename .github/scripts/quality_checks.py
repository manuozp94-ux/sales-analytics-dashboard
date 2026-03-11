#!/usr/bin/env python3
"""
Repository quality checks for CI baseline.

Checks:
1) SQL file sanity checks
2) Notebook JSON sanity checks
3) Markdown relative link checks
4) Artifact policy guardrails
5) Project memory template heading checks
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
MAX_TRACKED_FILE_BYTES = 100 * 1024 * 1024  # 100 MB hard limit
TRANSITION_ALLOWLIST = {
    "04-duckdb/sales_analytics.duckdb",
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FORBIDDEN_PUBLIC_TERMS = [
    "vibecoding",
    "vibe coding",
]

MEMORY_TEMPLATES = {
    "05-docs/project-memory/PROJECT_STATUS.md": [
        "## Last Updated (UTC)",
        "## Current Phase",
        "## Latest Outputs",
        "## Active Blockers",
        "## Active Risks",
        "## Next Milestone",
    ],
    "05-docs/project-memory/SESSION_LOG.md": [
        "## Template Lock",
        "## Session Date (UTC)",
        "## Session Goal",
        "## Changes Completed",
        "## Validation Evidence",
        "## Decisions",
        "## Carry-Over",
    ],
    "05-docs/project-memory/NEXT_ACTIONS.md": [
        "## Last Updated (UTC)",
        "## Top 3 Actions",
        "## Backlog (Short Horizon)",
    ],
}


def run_cmd(args: list[str]) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def fail(errors: list[str]) -> int:
    if errors:
        print("QUALITY CHECKS FAILED")
        for err in errors:
            print(f"- {err}")
        return 1
    print("QUALITY CHECKS PASSED")
    return 0


def check_sql(errors: list[str]) -> None:
    sql_files = sorted((ROOT / "03-sql").rglob("*.sql"))
    if not sql_files:
        errors.append("No SQL files found under 03-sql.")
        return

    for path in sql_files:
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8").strip()
        low = text.lower()

        if not text:
            errors.append(f"Empty SQL file: {rel}")
            continue

        if "create" not in low and "select" not in low:
            errors.append(f"SQL file missing expected statements: {rel}")

        if ("03-sql/models/" in rel or "03-sql/marts/" in rel) and "create or replace" not in low:
            errors.append(f"Model/mart SQL should use create or replace pattern: {rel}")

        if not text.endswith(";"):
            errors.append(f"SQL file should end with semicolon: {rel}")


def check_notebooks(errors: list[str]) -> None:
    notebooks = sorted((ROOT / "02-notebooks").glob("*.ipynb"))
    if not notebooks:
        errors.append("No notebooks found under 02-notebooks.")
        return

    for nb in notebooks:
        rel = nb.relative_to(ROOT).as_posix()
        try:
            payload = json.loads(nb.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Notebook is not valid JSON ({rel}): {exc}")
            continue

        if not isinstance(payload.get("cells"), list):
            errors.append(f"Notebook missing cells list: {rel}")
        if "nbformat" not in payload:
            errors.append(f"Notebook missing nbformat: {rel}")

        for idx, cell in enumerate(payload.get("cells", []), start=1):
            if not isinstance(cell, dict):
                errors.append(f"Notebook cell is not object ({rel}, cell {idx})")
                continue
            if cell.get("cell_type") not in {"code", "markdown", "raw"}:
                errors.append(f"Notebook invalid cell_type ({rel}, cell {idx})")
            if "source" not in cell:
                errors.append(f"Notebook missing source ({rel}, cell {idx})")


def parse_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith("http"):
        target = target.split(" ", 1)[0]
    return target


def check_markdown_links(errors: list[str]) -> None:
    markdown_files = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    markdown_files += sorted((ROOT / "05-docs").rglob("*.md"))
    markdown_files += sorted((ROOT / "06-fabric-sync").rglob("*.md"))

    for md in markdown_files:
        rel_md = md.relative_to(ROOT).as_posix()
        content = md.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(content):
            raw_target = match.group(1)
            target = parse_markdown_target(raw_target)

            if not target or target.startswith("#"):
                continue
            if target.startswith(("http://", "https://", "mailto:")):
                continue

            target_path = unquote(target.split("#", 1)[0])
            if not target_path:
                continue
            if target_path.startswith("/"):
                # In canonical docs we expect repo-relative links, not absolute filesystem paths.
                errors.append(f"Absolute path link not allowed in canonical docs: {rel_md} -> {target}")
                continue

            resolved = (md.parent / target_path).resolve()
            if not resolved.exists():
                errors.append(f"Broken relative link: {rel_md} -> {target}")


def check_artifacts(errors: list[str]) -> None:
    tracked = run_cmd(["git", "ls-files"]).splitlines()
    forbidden_suffixes = (".duckdb", ".duckdb.wal", ".zip")

    for rel in tracked:
        rel = rel.strip()
        if not rel:
            continue
        path = ROOT / rel
        if not path.exists():
            continue

        size = path.stat().st_size
        lower = rel.lower()

        if size > MAX_TRACKED_FILE_BYTES:
            errors.append(f"Tracked file exceeds 100MB limit: {rel}")

        if lower.endswith(forbidden_suffixes) and rel not in TRANSITION_ALLOWLIST:
            errors.append(
                f"Forbidden tracked artifact by policy: {rel}. "
                "Use metadata-only strategy and keep generated artifacts untracked."
            )


def check_memory_templates(errors: list[str]) -> None:
    for rel, headings in MEMORY_TEMPLATES.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"Missing required memory file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in headings:
            if heading not in text:
                errors.append(f"Memory template heading missing ({rel}): {heading}")


def check_codeowners(errors: list[str]) -> None:
    codeowners = ROOT / ".github/CODEOWNERS"
    if not codeowners.exists():
        errors.append("Missing .github/CODEOWNERS.")
        return

    lines = [line.strip() for line in codeowners.read_text(encoding="utf-8").splitlines()]
    owners = [line for line in lines if line and not line.startswith("#")]

    if len(owners) != 1:
        errors.append("CODEOWNERS must contain exactly one active ownership rule.")
        return

    if not owners[0].startswith("* @"):
        errors.append("CODEOWNERS active rule must be in format: * @github-handle")


def check_public_doc_voice(errors: list[str]) -> None:
    doc_paths = [ROOT / "README.md", ROOT / "CONTRIBUTING.md"]
    doc_paths += sorted((ROOT / "05-docs").rglob("*.md"))
    doc_paths += sorted((ROOT / "06-fabric-sync").rglob("*.md"))

    for path in doc_paths:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("05-docs/context-consolidation/"):
            continue

        text = path.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_PUBLIC_TERMS:
            if term in text:
                errors.append(f"Forbidden wording in canonical/public docs ({rel}): '{term}'")


def main() -> int:
    errors: list[str] = []
    check_sql(errors)
    check_notebooks(errors)
    check_markdown_links(errors)
    check_artifacts(errors)
    check_memory_templates(errors)
    check_codeowners(errors)
    check_public_doc_voice(errors)
    return fail(errors)


if __name__ == "__main__":
    sys.exit(main())
