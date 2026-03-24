#!/usr/bin/env python3
"""
Guardrails for deployable Fabric Warehouse SQL.

The goal is to fail early on risky schema-evolution patterns that deserve an
explicit migration or one-time reviewed path instead of silently shipping in the
canonical deployable SQL pack.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from sql_pack_manifest import WAREHOUSE_SQL_DIR, selected_sql


COMMENT_BLOCK_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
COMMENT_LINE_RE = re.compile(r"--[^\n]*")

RULES = [
    {
        "rule_id": "alter_table_requires_review",
        "classification": "repo_opinionated_default",
        "pattern": re.compile(r"\balter\s+table\b", re.IGNORECASE),
        "message": (
            "ALTER TABLE is blocked in the deployable Fabric Warehouse pack. "
            "Move schema evolution into a one-time reviewed path and update the "
            "consulting standard before shipping it."
        ),
    },
    {
        "rule_id": "constraint_changes_require_review",
        "classification": "preview_limitation_guardrail",
        "pattern": re.compile(r"\b(add|drop)\s+constraint\b", re.IGNORECASE),
        "message": (
            "Constraint changes are blocked in deployable Warehouse SQL because "
            "Fabric deployment/source-control workflows can drop and recreate tables."
        ),
    },
    {
        "rule_id": "alter_column_requires_review",
        "classification": "preview_limitation_guardrail",
        "pattern": re.compile(r"\balter\s+column\b", re.IGNORECASE),
        "message": (
            "ALTER COLUMN is blocked in deployable Warehouse SQL. Use an explicit "
            "migration review path instead."
        ),
    },
    {
        "rule_id": "drop_column_requires_review",
        "classification": "repo_opinionated_default",
        "pattern": re.compile(r"\bdrop\s+column\b", re.IGNORECASE),
        "message": (
            "DROP COLUMN is blocked in deployable Warehouse SQL. Treat destructive "
            "schema changes as reviewed migrations."
        ),
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check deployable Fabric Warehouse SQL against repo guardrails."
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--include-legacy-cleanup",
        action="store_true",
        help="Include the optional legacy cleanup file in the scan.",
    )
    parser.add_argument(
        "--include-reset",
        action="store_true",
        help="Include the optional reset file in the scan.",
    )
    return parser.parse_args()


def strip_sql_comments(sql_text: str) -> str:
    without_blocks = COMMENT_BLOCK_RE.sub(" ", sql_text)
    return COMMENT_LINE_RE.sub(" ", without_blocks)


def scan_file(path: Path) -> list[dict[str, Any]]:
    content = strip_sql_comments(path.read_text(encoding="utf-8"))
    violations: list[dict[str, Any]] = []
    for rule in RULES:
        if rule["pattern"].search(content):
            violations.append(
                {
                    "path": path.as_posix(),
                    "rule_id": rule["rule_id"],
                    "classification": rule["classification"],
                    "message": rule["message"],
                }
            )
    return violations


def run_scan(include_legacy_cleanup: bool, include_reset: bool) -> dict[str, Any]:
    files = selected_sql(
        include_legacy_cleanup=include_legacy_cleanup,
        include_reset=include_reset,
        include_validation=False,
    )
    violations: list[dict[str, Any]] = []
    checked_paths: list[str] = []

    for file_name in files:
        path = WAREHOUSE_SQL_DIR / file_name
        checked_paths.append(path.as_posix())
        violations.extend(scan_file(path))

    return {
        "checked_files": checked_paths,
        "checked_count": len(checked_paths),
        "violation_count": len(violations),
        "violations": violations,
    }


def main() -> int:
    args = parse_args()
    report = run_scan(
        include_legacy_cleanup=args.include_legacy_cleanup,
        include_reset=args.include_reset,
    )
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        if report["violation_count"] == 0:
            print(
                "Fabric Warehouse SQL guardrails passed. "
                f"Checked {report['checked_count']} deployable SQL files."
            )
        else:
            print("Fabric Warehouse SQL guardrails failed.")
            for violation in report["violations"]:
                print(
                    f"- {violation['path']}: {violation['rule_id']} "
                    f"({violation['classification']}) -> {violation['message']}"
                )
    return 1 if report["violation_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
