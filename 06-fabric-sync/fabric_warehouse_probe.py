#!/usr/bin/env python3
"""
Fabric Warehouse probe utility.

Purpose:
- Capture a workspace-level inventory focused on Warehouse and SQL artifacts.
- Attempt Warehouse REST metadata endpoints to discover what is currently exposed.
- Emit machine-readable JSON + operator-friendly Markdown evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

from fabric_sync import (
    DEFAULT_BASE_URL,
    canonical_items,
    extract_items,
    fetch_workspace_items,
    read_json,
    write_json,
)

try:
    from parity_contract import REQUIRED_OBJECTS
except ModuleNotFoundError:
    # Fallback contract for environments where parity_contract.py is not present.
    REQUIRED_OBJECTS = [
        "dim_date",
        "dim_customers",
        "dim_products",
        "fact_orders",
        "fact_order_items",
        "fact_order_payments",
        "fact_order_reviews",
        "mart_monthly_business_snapshot",
        "mart_cohort_unit_economics",
        "mart_customer_ltv_summary",
    ]


SNAKE_CASE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

# Candidate API paths that may expose warehouse catalog metadata.
# If not supported by the current API version, probe output will include
# non-200 responses so we can track capability gaps explicitly.
WAREHOUSE_CATALOG_PROBES = {
    "schemas": "/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/schemas",
    "tables": "/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/tables",
    "views": "/v1/workspaces/{workspace_id}/warehouses/{warehouse_id}/views",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe Fabric Warehouse metadata and naming evidence."
    )
    parser.add_argument(
        "--mode",
        choices=["rest", "file"],
        default="rest",
        help="Probe source mode. Use 'rest' for live workspace probing.",
    )
    parser.add_argument(
        "--workspace-id",
        default=None,
        help="Fabric workspace ID (required in --mode rest).",
    )
    parser.add_argument(
        "--input",
        default=None,
        help="Input items JSON path when --mode file.",
    )
    parser.add_argument(
        "--token-env",
        default="FABRIC_BEARER_TOKEN",
        help="Environment variable containing Fabric bearer token for --mode rest.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Fabric API base URL for --mode rest.",
    )
    parser.add_argument(
        "--output-json",
        default="06-fabric-sync/state/warehouse-probe/warehouse_probe_latest.json",
        help="Path for JSON probe output.",
    )
    parser.add_argument(
        "--output-md",
        default="06-fabric-sync/state/warehouse-probe/warehouse_probe_latest.md",
        help="Path for Markdown probe report.",
    )
    parser.add_argument(
        "--fail-if-no-warehouse",
        action="store_true",
        help="Fail if no Warehouse item is found in the workspace inventory.",
    )
    return parser.parse_args()


def trim_payload(payload: Any, max_chars: int = 4000) -> Any:
    text = json.dumps(payload, ensure_ascii=True)
    if len(text) <= max_chars:
        return payload
    return {"_truncated": True, "_preview": text[:max_chars]}


def api_get(url: str, token: str) -> dict[str, Any]:
    req = request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            payload: Any
            try:
                payload = json.loads(body) if body else {}
            except json.JSONDecodeError:
                payload = {"raw": body}
            return {
                "ok": True,
                "status_code": int(getattr(resp, "status", 200)),
                "url": url,
                "payload": trim_payload(payload),
            }
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return {
            "ok": False,
            "status_code": int(exc.code),
            "url": url,
            "error": str(exc),
            "payload": trim_payload(payload),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "status_code": None,
            "url": url,
            "error": str(exc),
            "payload": None,
        }


def fetch_workspace_items_input(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.mode == "file":
        if not args.input:
            fail("--input is required in --mode file.")
        payload = read_json(Path(args.input))
        rows = extract_items(payload)
        if not rows and isinstance(payload, list):
            rows = [item for item in payload if isinstance(item, dict)]
        return rows

    if not args.workspace_id:
        fail("--workspace-id is required in --mode rest.")
    token = os.getenv(args.token_env)
    if not token:
        fail(f"Missing bearer token in env var: {args.token_env}")
    return fetch_workspace_items(
        base_url=args.base_url.rstrip("/"),
        workspace_id=args.workspace_id,
        token=token,
    )


def naming_issues(items: list[dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for row in items:
        name = row.get("name", "")
        if not isinstance(name, str):
            continue
        if SNAKE_CASE_RE.match(name):
            continue
        issues.append(
            {
                "id": str(row.get("id", "")),
                "type": str(row.get("type", "")),
                "name": name,
                "issue": "non_snake_case_name",
            }
        )
    issues.sort(key=lambda x: (x["type"], x["name"], x["id"]))
    return issues


def contract_name_scan(items: list[dict[str, Any]]) -> dict[str, Any]:
    names = {str(item.get("name", "")).strip().lower() for item in items}
    matched = sorted([name for name in REQUIRED_OBJECTS if name in names])
    missing = sorted([name for name in REQUIRED_OBJECTS if name not in names])
    return {
        "required_objects": REQUIRED_OBJECTS,
        "workspace_name_matches": matched,
        "workspace_name_missing": missing,
    }


def type_counts(items: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        key = str(item.get("type", "UNKNOWN"))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: kv[0]))


def query_candidates(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        item_type = str(item.get("type", "")).lower()
        name = str(item.get("name", ""))
        if "query" in item_type or "sql" in item_type:
            out.append(item)
            continue
        if "query" in name.lower() or name.lower().startswith("sql_"):
            out.append(item)
    out.sort(key=lambda x: (x.get("type", ""), x.get("name", ""), x.get("id", "")))
    return out


def probe_warehouses(
    workspace_id: str,
    base_url: str,
    token: str,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    warehouses = [row for row in items if str(row.get("type", "")) == "Warehouse"]
    output: list[dict[str, Any]] = []

    for wh in warehouses:
        wh_id = str(wh.get("id", ""))
        wh_name = str(wh.get("name", ""))
        detail_url = f"{base_url.rstrip('/')}/v1/workspaces/{workspace_id}/warehouses/{wh_id}"
        conn_url = (
            f"{base_url.rstrip('/')}/v1/workspaces/{workspace_id}/warehouses/{wh_id}/connectionString"
        )

        row = {
            "id": wh_id,
            "name": wh_name,
            "detail": api_get(detail_url, token),
            "connection_string": api_get(conn_url, token),
            "catalog_probe": [],
        }

        for probe_name, template in WAREHOUSE_CATALOG_PROBES.items():
            path = template.format(workspace_id=workspace_id, warehouse_id=wh_id)
            url = f"{base_url.rstrip('/')}{path}"
            row["catalog_probe"].append({"probe": probe_name, **api_get(url, token)})
        output.append(row)

    return output


def markdown_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Fabric Warehouse Probe Report",
        "",
        f"- Generated (UTC): `{payload['generated_utc']}`",
        f"- Workspace ID: `{payload['workspace_id'] or 'UNKNOWN'}`",
        f"- Source mode: `{payload['source']['mode']}`",
        f"- Total workspace items: **{summary['item_count']}**",
        f"- Warehouses found: **{summary['warehouse_count']}**",
        f"- SQL endpoint items: **{summary['sql_endpoint_count']}**",
        f"- Query candidate items: **{summary['query_candidate_count']}**",
        f"- Naming issues (non-snake-case): **{summary['naming_issue_count']}**",
        "",
        "## Item Type Counts",
        "",
    ]

    for key, value in payload["item_type_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.append("")

    lines.append("## Warehouses")
    lines.append("")
    warehouses = payload.get("warehouses", [])
    if not warehouses:
        if payload["source"]["mode"] == "file" and summary["warehouse_count"] > 0:
            lines.append("_Warehouse items were detected, but live metadata probes are skipped in file mode._")
        else:
            lines.append("_No Warehouse items found in workspace inventory._")
        lines.append("")
    else:
        for wh in warehouses:
            lines.append(f"### `{wh['name']}` (`{wh['id']}`)")
            lines.append("")
            detail = wh["detail"]
            conn = wh["connection_string"]
            lines.append(
                f"- Get warehouse: {'OK' if detail['ok'] else 'FAIL'} "
                f"(status: `{detail['status_code']}`)"
            )
            lines.append(
                f"- Get connection string: {'OK' if conn['ok'] else 'FAIL'} "
                f"(status: `{conn['status_code']}`)"
            )
            if conn.get("ok"):
                conn_payload = conn.get("payload", {})
                connection_string = conn_payload.get("connectionString")
                if isinstance(connection_string, str) and connection_string:
                    lines.append(f"- Connection host: `{connection_string}`")
            lines.append("- Catalog probes:")
            for probe in wh.get("catalog_probe", []):
                lines.append(
                    f"  - `{probe['probe']}`: "
                    f"{'OK' if probe['ok'] else 'FAIL'} "
                    f"(status: `{probe['status_code']}`)"
                )
            lines.append("")

    lines.append("## Naming Issues")
    lines.append("")
    issues = payload.get("naming_issues", [])
    if not issues:
        lines.append("_No naming issues detected under snake_case rule._")
        lines.append("")
    else:
        for issue in issues:
            lines.append(
                f"- `{issue['type']}` | `{issue['name']}` | `{issue['id']}` "
                f"-> {issue['issue']}"
            )
        lines.append("")

    lines.append("## Contract Name Presence (Workspace Item Names)")
    lines.append("")
    contract = payload["contract_scan"]
    lines.append(
        f"- Matches: **{len(contract['workspace_name_matches'])}/{len(contract['required_objects'])}**"
    )
    if contract["workspace_name_matches"]:
        lines.append("- Present:")
        for name in contract["workspace_name_matches"]:
            lines.append(f"  - `{name}`")
    else:
        lines.append("- Present: _None_")
    lines.append("")
    lines.append("- Missing:")
    for name in contract["workspace_name_missing"]:
        lines.append(f"  - `{name}`")
    lines.append("")

    lines.append(
        "Note: workspace inventory tracks top-level Fabric items. Table/view-level presence "
        "inside Warehouse must be validated with Warehouse SQL catalog queries."
    )
    lines.append("")
    return "\n".join(lines)


def write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows = fetch_workspace_items_input(args)
    workspace_id = args.workspace_id
    items = canonical_items(rows, workspace_id=workspace_id)

    whs = [item for item in items if str(item.get("type", "")) == "Warehouse"]
    sql_endpoints = [item for item in items if str(item.get("type", "")) == "SQLEndpoint"]
    candidate_queries = query_candidates(items)
    issues = naming_issues(items)
    contract_scan = contract_name_scan(items)

    warehouses_probe: list[dict[str, Any]] = []
    if args.mode == "rest":
        token = os.getenv(args.token_env)
        if not token:
            fail(f"Missing bearer token in env var: {args.token_env}")
        warehouses_probe = probe_warehouses(
            workspace_id=str(args.workspace_id),
            base_url=args.base_url,
            token=token,
            items=items,
        )

    payload = {
        "generated_utc": utc_now_iso(),
        "workspace_id": workspace_id,
        "source": {
            "mode": args.mode,
            "base_url": args.base_url if args.mode == "rest" else None,
            "input": args.input if args.mode == "file" else None,
        },
        "summary": {
            "item_count": len(items),
            "warehouse_count": len(whs),
            "sql_endpoint_count": len(sql_endpoints),
            "query_candidate_count": len(candidate_queries),
            "naming_issue_count": len(issues),
        },
        "item_type_counts": type_counts(items),
        "workspace_items": items,
        "query_candidates": candidate_queries,
        "naming_issues": issues,
        "contract_scan": contract_scan,
        "warehouses": warehouses_probe,
    }

    output_json = Path(args.output_json)
    output_md = Path(args.output_md)
    write_json(output_json, payload)
    write_markdown(output_md, markdown_report(payload))

    print("Fabric warehouse probe completed.")
    print(f"Workspace items: {len(items)}")
    print(f"Warehouses: {len(whs)}")
    print(f"SQL endpoints: {len(sql_endpoints)}")
    print(f"Query candidates: {len(candidate_queries)}")
    print(f"JSON output: {output_json.as_posix()}")
    print(f"Markdown output: {output_md.as_posix()}")

    if args.fail_if_no_warehouse and not whs:
        fail("No Warehouse item found in workspace inventory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
