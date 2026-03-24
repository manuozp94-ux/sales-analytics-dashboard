#!/usr/bin/env python3
"""
Canonical manifest for the Fabric Warehouse SQL pack.

This module keeps deployable, optional, and validation SQL paths in one place so
the repo can reuse the same definition across shell scripts, docs, and quality
checks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WAREHOUSE_SQL_DIR = ROOT / "sql" / "fabric-warehouse"

DEPLOYABLE_SQL = [
    "00_schema_bootstrap.sql",
    "05_stg_compat_views.sql",
    "10_core_dim_date.sql",
    "11_core_dim_customers.sql",
    "12_core_dim_products.sql",
    "20_core_fact_orders.sql",
    "21_core_fact_order_items.sql",
    "22_core_fact_order_payments.sql",
    "23_core_fact_order_reviews.sql",
    "30_mart_cohort_unit_economics.sql",
    "31_mart_monthly_business_snapshot.sql",
    "32_mart_customer_ltv_summary.sql",
]

OPTIONAL_SQL = {
    "include_legacy_cleanup": ["02_drop_legacy_marts_schema_safe.sql"],
    "include_reset": ["01_reset_core_mart_safe.sql"],
}

VALIDATION_SQL = [
    "40_parity_query_pack.sql",
    "41_warehouse_catalog_probe.sql",
]


def manifest() -> dict[str, object]:
    return {
        "sql_dir": str(WAREHOUSE_SQL_DIR),
        "deployable": DEPLOYABLE_SQL,
        "optional": OPTIONAL_SQL,
        "validation": VALIDATION_SQL,
    }


def selected_sql(
    include_legacy_cleanup: bool = False,
    include_reset: bool = False,
    include_validation: bool = False,
) -> list[str]:
    files = list(DEPLOYABLE_SQL)
    if include_legacy_cleanup:
        files = ["02_drop_legacy_marts_schema_safe.sql", *files]
    if include_reset:
        files = [*files[:1], "01_reset_core_mart_safe.sql", *files[1:]]
    if include_validation:
        files.extend(VALIDATION_SQL)
    return files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print or export the canonical Fabric Warehouse SQL pack manifest."
    )
    parser.add_argument(
        "--format",
        choices=["newline", "json"],
        default="newline",
        help="Output format.",
    )
    parser.add_argument(
        "--include-legacy-cleanup",
        action="store_true",
        help="Include the optional legacy marts cleanup file.",
    )
    parser.add_argument(
        "--include-reset",
        action="store_true",
        help="Include the optional core/mart reset file.",
    )
    parser.add_argument(
        "--include-validation",
        action="store_true",
        help="Append validation-only SQL files.",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Emit the categorized manifest instead of a selected ordered file list.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.manifest_only:
        payload = manifest()
        print(json.dumps(payload, ensure_ascii=True, indent=2))
        return 0

    files = selected_sql(
        include_legacy_cleanup=args.include_legacy_cleanup,
        include_reset=args.include_reset,
        include_validation=args.include_validation,
    )
    if args.format == "json":
        print(json.dumps(files, ensure_ascii=True, indent=2))
    else:
        for file_name in files:
            print(file_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
