#!/usr/bin/env python3
"""
Compare local and Fabric parity baselines and emit PASS/FAIL evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from parity_contract import (
    GRAIN_CHECKS,
    KPI_TYPES,
    NULL_KEY_CHECKS,
    ORPHAN_CHECKS,
    REQUIRED_OBJECTS,
    kpi_tolerance,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCAL_PATH = ROOT / "06-fabric-sync" / "state" / "parity" / "parity_local_latest.json"
DEFAULT_FABRIC_PATH = ROOT / "06-fabric-sync" / "state" / "parity" / "parity_fabric_latest.json"
DEFAULT_OUTPUT_JSON = ROOT / "06-fabric-sync" / "state" / "parity" / "parity_compare_latest.json"
DEFAULT_OUTPUT_MD = ROOT / "06-fabric-sync" / "state" / "parity" / "parity_compare_latest.md"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare local DuckDB baseline against Fabric parity baseline."
    )
    parser.add_argument(
        "--local",
        default=str(DEFAULT_LOCAL_PATH),
        help="Local parity baseline JSON path.",
    )
    parser.add_argument(
        "--fabric",
        default=str(DEFAULT_FABRIC_PATH),
        help="Fabric parity baseline JSON path.",
    )
    parser.add_argument(
        "--out-json",
        default=str(DEFAULT_OUTPUT_JSON),
        help="Output JSON report path.",
    )
    parser.add_argument(
        "--out-md",
        default=str(DEFAULT_OUTPUT_MD),
        help="Output Markdown report path.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"JSON file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON file {path}: {exc}")

    if not isinstance(payload, dict):
        fail(f"JSON root must be object: {path}")
    return payload


def expect_section(payload: dict[str, Any], section: str, source_name: str) -> dict[str, Any]:
    value = payload.get(section)
    if not isinstance(value, dict):
        fail(f"Missing or invalid '{section}' section in {source_name}.")
    return value


def expect_float(value: Any, field_name: str, source_name: str) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    fail(f"Field '{field_name}' in {source_name} must be numeric.")


def compare_counts(local_counts: dict[str, Any], fabric_counts: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for object_name in REQUIRED_OBJECTS:
        if object_name not in local_counts:
            fail(f"Local baseline missing count for object: {object_name}")
        if object_name not in fabric_counts:
            fail(f"Fabric baseline missing count for object: {object_name}")

        local_value = int(expect_float(local_counts[object_name], object_name, "local"))
        fabric_value = int(expect_float(fabric_counts[object_name], object_name, "fabric"))
        passed = local_value == fabric_value
        rows.append(
            {
                "object_name": object_name,
                "local_count": local_value,
                "fabric_count": fabric_value,
                "diff": fabric_value - local_value,
                "passed": passed,
            }
        )
    return rows


def qa_map(payload: dict[str, Any], section_key: str, source_name: str) -> dict[str, int]:
    qa = expect_section(payload, "qa", source_name)
    section = qa.get(section_key)
    if not isinstance(section, dict):
        fail(f"Missing QA section '{section_key}' in {source_name}.")
    checks = section.get("checks")
    if not isinstance(checks, list):
        fail(f"QA section '{section_key}' checks must be a list in {source_name}.")

    result: dict[str, int] = {}
    for row in checks:
        if not isinstance(row, dict):
            fail(f"QA row in '{section_key}' must be object in {source_name}.")
        name = row.get("name")
        if not isinstance(name, str):
            fail(f"QA row missing name in '{section_key}' for {source_name}.")
        value = row.get("violation_count")
        result[name] = int(expect_float(value, name, source_name))
    return result


def compare_qa(
    local_payload: dict[str, Any],
    fabric_payload: dict[str, Any],
) -> list[dict[str, Any]]:
    expected_names = {
        "grain": [row["name"] for row in GRAIN_CHECKS],
        "null_keys": [row["name"] for row in NULL_KEY_CHECKS],
        "orphans": [row["name"] for row in ORPHAN_CHECKS],
    }

    rows: list[dict[str, Any]] = []
    for section, names in expected_names.items():
        local_map = qa_map(local_payload, section, "local")
        fabric_map = qa_map(fabric_payload, section, "fabric")
        for check_name in names:
            if check_name not in local_map:
                fail(f"Local QA missing check '{section}.{check_name}'.")
            if check_name not in fabric_map:
                fail(f"Fabric QA missing check '{section}.{check_name}'.")

            local_value = local_map[check_name]
            fabric_value = fabric_map[check_name]
            exact_match = local_value == fabric_value
            zero_guardrail = local_value == 0 and fabric_value == 0
            passed = exact_match and zero_guardrail
            rows.append(
                {
                    "section": section,
                    "check_name": check_name,
                    "local_violations": local_value,
                    "fabric_violations": fabric_value,
                    "exact_match": exact_match,
                    "zero_guardrail": zero_guardrail,
                    "passed": passed,
                }
            )
    return rows


def compare_kpis(local_kpis: dict[str, Any], fabric_kpis: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for metric_name in KPI_TYPES:
        if metric_name not in local_kpis:
            fail(f"Local baseline missing KPI: {metric_name}")
        if metric_name not in fabric_kpis:
            fail(f"Fabric baseline missing KPI: {metric_name}")

        local_value = expect_float(local_kpis[metric_name], metric_name, "local")
        fabric_value = expect_float(fabric_kpis[metric_name], metric_name, "fabric")
        tolerance = kpi_tolerance(metric_name)
        abs_diff = abs(local_value - fabric_value)

        passed = (
            math.isfinite(local_value)
            and math.isfinite(fabric_value)
            and abs_diff <= tolerance
        )
        rows.append(
            {
                "metric_name": metric_name,
                "metric_type": KPI_TYPES[metric_name],
                "local_value": local_value,
                "fabric_value": fabric_value,
                "abs_diff": abs_diff,
                "tolerance": tolerance,
                "passed": passed,
            }
        )
    return rows


def summarize(
    count_rows: list[dict[str, Any]],
    qa_rows: list[dict[str, Any]],
    kpi_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    count_passed = all(row["passed"] for row in count_rows)
    qa_passed = all(row["passed"] for row in qa_rows)
    kpi_passed = all(row["passed"] for row in kpi_rows)
    overall = count_passed and qa_passed and kpi_passed
    return {
        "counts_passed": count_passed,
        "qa_passed": qa_passed,
        "kpis_passed": kpi_passed,
        "overall_passed": overall,
        "counts_total": len(count_rows),
        "counts_failed": sum(1 for row in count_rows if not row["passed"]),
        "qa_total": len(qa_rows),
        "qa_failed": sum(1 for row in qa_rows if not row["passed"]),
        "kpis_total": len(kpi_rows),
        "kpis_failed": sum(1 for row in kpi_rows if not row["passed"]),
    }


def to_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Fabric Parity Comparison Report",
        "",
        f"- Generated (UTC): `{report['generated_utc']}`",
        f"- Local baseline: `{report['inputs']['local']}`",
        f"- Fabric baseline: `{report['inputs']['fabric']}`",
        f"- Status: **{'PASS' if summary['overall_passed'] else 'FAIL'}**",
        "",
        "## Summary",
        "",
        f"- Counts: `{summary['counts_total']}` checks, `{summary['counts_failed']}` failed",
        f"- QA: `{summary['qa_total']}` checks, `{summary['qa_failed']}` failed",
        f"- KPIs: `{summary['kpis_total']}` checks, `{summary['kpis_failed']}` failed",
        "",
        "## Failed Checks",
        "",
    ]

    failed_counts = [row for row in report["counts"] if not row["passed"]]
    failed_qa = [row for row in report["qa"] if not row["passed"]]
    failed_kpis = [row for row in report["kpis"] if not row["passed"]]

    if not failed_counts and not failed_qa and not failed_kpis:
        lines.append("_None_")
    else:
        for row in failed_counts:
            lines.append(
                f"- Count mismatch `{row['object_name']}`: "
                f"local={row['local_count']} fabric={row['fabric_count']}"
            )
        for row in failed_qa:
            lines.append(
                f"- QA mismatch `{row['section']}.{row['check_name']}`: "
                f"local={row['local_violations']} fabric={row['fabric_violations']}"
            )
        for row in failed_kpis:
            lines.append(
                f"- KPI mismatch `{row['metric_name']}`: "
                f"local={row['local_value']:.6f} fabric={row['fabric_value']:.6f} "
                f"(abs_diff={row['abs_diff']:.6f}, tolerance={row['tolerance']:.6f})"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    local_path = Path(args.local).resolve()
    fabric_path = Path(args.fabric).resolve()
    out_json_path = Path(args.out_json).resolve()
    out_md_path = Path(args.out_md).resolve()

    local_payload = read_json(local_path)
    fabric_payload = read_json(fabric_path)

    local_counts = expect_section(local_payload, "counts", "local")
    fabric_counts = expect_section(fabric_payload, "counts", "fabric")
    local_kpis = expect_section(local_payload, "kpis", "local")
    fabric_kpis = expect_section(fabric_payload, "kpis", "fabric")

    count_rows = compare_counts(local_counts, fabric_counts)
    qa_rows = compare_qa(local_payload, fabric_payload)
    kpi_rows = compare_kpis(local_kpis, fabric_kpis)
    summary = summarize(count_rows, qa_rows, kpi_rows)

    report = {
        "generated_utc": utc_now_iso(),
        "inputs": {
            "local": str(local_path),
            "fabric": str(fabric_path),
        },
        "summary": summary,
        "counts": count_rows,
        "qa": qa_rows,
        "kpis": kpi_rows,
        "status": "PASS" if summary["overall_passed"] else "FAIL",
    }

    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    out_md_path.parent.mkdir(parents=True, exist_ok=True)
    out_json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    out_md_path.write_text(to_markdown(report), encoding="utf-8")

    print("Parity comparison completed.")
    print(f"Status: {report['status']}")
    print(f"JSON report: {out_json_path.as_posix()}")
    print(f"Markdown report: {out_md_path.as_posix()}")

    return 0 if summary["overall_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
