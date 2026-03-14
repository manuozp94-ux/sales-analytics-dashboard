#!/usr/bin/env python3
"""
Generate canonical local parity baseline (DuckDB) for Fabric comparison.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

from parity_contract import (
    GRAIN_CHECKS,
    KPI_SQL_DUCKDB,
    NULL_KEY_CHECKS,
    ORPHAN_CHECKS,
    REQUIRED_OBJECTS,
    KPI_TYPES,
    contract_summary,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DUCKDB_PATH = ROOT / "04-duckdb" / "sales_analytics.duckdb"
DEFAULT_OUTPUT_PATH = ROOT / "06-fabric-sync" / "state" / "parity" / "parity_local_latest.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate local DuckDB parity baseline for Fabric validation."
    )
    parser.add_argument(
        "--duckdb-path",
        default=str(DEFAULT_DUCKDB_PATH),
        help="Path to DuckDB database file.",
    )
    parser.add_argument(
        "--workspace-id",
        default="1fd8df3e-883f-49d3-9386-d236f8b272ba",
        help="Target Fabric workspace ID for parity metadata.",
    )
    parser.add_argument(
        "--out-json",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output JSON file path.",
    )
    parser.add_argument(
        "--source-label",
        default="local_duckdb",
        help="Source label for traceability metadata.",
    )
    return parser.parse_args()


def existing_objects(con: duckdb.DuckDBPyConnection) -> set[str]:
    rows = con.execute(
        """
        select table_name
        from information_schema.tables
        where table_schema not in ('information_schema', 'pg_catalog')
        """
    ).fetchall()
    return {str(row[0]) for row in rows}


def run_scalar(con: duckdb.DuckDBPyConnection, sql: str) -> float:
    value = con.execute(sql).fetchone()
    if value is None:
        fail("Scalar query returned no rows.")
    result = value[0]
    if result is None:
        return 0.0
    return float(result)


def run_count_pack(
    con: duckdb.DuckDBPyConnection,
    checks: list[dict[str, str]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    total = 0
    for check in checks:
        count = int(run_scalar(con, check["sql_duckdb"]))
        rows.append({"name": check["name"], "violation_count": count})
        total += count
    return {"violations_total": total, "checks": rows}


def main() -> int:
    args = parse_args()
    duckdb_path = Path(args.duckdb_path).resolve()
    out_json_path = Path(args.out_json).resolve()

    if not duckdb_path.exists():
        fail(f"DuckDB file not found: {duckdb_path}")

    con = duckdb.connect(str(duckdb_path))
    try:
        objects = existing_objects(con)
        missing = [name for name in REQUIRED_OBJECTS if name not in objects]
        if missing:
            fail(
                "Missing required contract objects in local DuckDB: "
                + ", ".join(missing)
            )

        counts = {
            object_name: int(run_scalar(con, f"select count(*) from {object_name}"))
            for object_name in REQUIRED_OBJECTS
        }

        kpis = {
            metric_name: float(run_scalar(con, sql_text))
            for metric_name, sql_text in KPI_SQL_DUCKDB.items()
        }

        qa = {
            "grain": run_count_pack(con, GRAIN_CHECKS),
            "null_keys": run_count_pack(con, NULL_KEY_CHECKS),
            "orphans": run_count_pack(con, ORPHAN_CHECKS),
        }
        violations_total = (
            qa["grain"]["violations_total"]
            + qa["null_keys"]["violations_total"]
            + qa["orphans"]["violations_total"]
        )
        status = "PASS" if violations_total == 0 else "FAIL"

        payload = {
            "generated_utc": utc_now_iso(),
            "workspace_id": args.workspace_id,
            "source": {
                "label": args.source_label,
                "engine": "duckdb",
                "duckdb_path": str(duckdb_path),
            },
            "contract": contract_summary(),
            "counts": counts,
            "kpis": kpis,
            "qa": qa,
            "qa_violations_total": violations_total,
            "required_kpi_count": len(KPI_TYPES),
            "status": status,
        }

        out_json_path.parent.mkdir(parents=True, exist_ok=True)
        out_json_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )

        print("Local parity baseline generated.")
        print(f"Status: {status}")
        print(f"Output: {out_json_path.as_posix()}")
        print(f"Required objects: {len(REQUIRED_OBJECTS)}")
        print(f"Required KPIs: {len(KPI_TYPES)}")
        print(f"QA total violations: {violations_total}")
        return 0
    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())
