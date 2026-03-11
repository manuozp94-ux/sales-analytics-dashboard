#!/usr/bin/env python3
"""
Controlled Fabric deployment scaffold.

This utility executes a curated set of workspace-scoped REST operations with
two explicit modes:
- dry-run: validate and persist a deployment plan without write calls.
- apply: execute validated operations against Fabric REST API.
"""

from __future__ import annotations

import argparse
import json
import os
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


ALLOWED_METHODS = {"POST", "PATCH", "PUT", "DELETE"}
DEFAULT_PLAN_OUTPUT = "06-fabric-sync/state/fabric_deploy_plan_latest.json"
DEFAULT_REPORT_OUTPUT = "06-fabric-sync/state/fabric_deploy_report_latest.md"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Controlled Fabric deployment scaffold with dry-run and apply actions."
    )
    parser.add_argument("--workspace-id", default=None, help="Target Fabric workspace ID.")
    parser.add_argument(
        "--mode",
        choices=["rest", "file"],
        required=True,
        help="Current-state source mode: Fabric REST API or local JSON file.",
    )
    parser.add_argument(
        "--input-current",
        default=None,
        help="Path to a current items JSON file when --mode file.",
    )
    parser.add_argument(
        "--desired-state",
        required=True,
        help="Path to deployment manifest JSON (expects an operations list).",
    )
    parser.add_argument(
        "--action",
        choices=["dry-run", "apply"],
        required=True,
        help="Deployment action: validate only or execute writes.",
    )
    parser.add_argument(
        "--token-env",
        default="FABRIC_BEARER_TOKEN",
        help="Environment variable that stores a Fabric bearer token.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Fabric API base URL.",
    )
    parser.add_argument(
        "--plan-output",
        default=DEFAULT_PLAN_OUTPUT,
        help="Plan output path (JSON).",
    )
    parser.add_argument(
        "--report-output",
        default=DEFAULT_REPORT_OUTPUT,
        help="Report output path (Markdown).",
    )
    parser.add_argument(
        "--allow-delete",
        action="store_true",
        help="Allow DELETE operations from the manifest.",
    )
    parser.add_argument(
        "--confirm-apply",
        default="",
        help="Must be YES when --action apply.",
    )
    return parser.parse_args()


def resolve_workspace_id(cli_workspace_id: str | None, manifest: dict[str, Any]) -> str:
    manifest_workspace_id = manifest.get("workspace_id")
    if manifest_workspace_id is not None and not isinstance(manifest_workspace_id, str):
        fail("Manifest workspace_id must be a string when provided.")

    if cli_workspace_id and manifest_workspace_id and cli_workspace_id != manifest_workspace_id:
        fail(
            "Workspace mismatch between --workspace-id "
            f"({cli_workspace_id}) and manifest workspace_id ({manifest_workspace_id})."
        )

    workspace_id = cli_workspace_id or manifest_workspace_id
    if not workspace_id:
        fail("Workspace ID is required (pass --workspace-id or set workspace_id in manifest).")
    return workspace_id


def load_manifest(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    if not isinstance(payload, dict):
        fail(f"Manifest must be a JSON object: {path.as_posix()}")
    operations = payload.get("operations")
    if not isinstance(operations, list):
        fail("Manifest must include an operations array.")
    return payload


def normalize_operation(
    raw_operation: Any,
    index: int,
    workspace_id: str,
    base_url: str,
    allow_delete: bool,
) -> dict[str, Any] | None:
    if not isinstance(raw_operation, dict):
        fail(f"Operation {index} must be a JSON object.")

    enabled = raw_operation.get("enabled", True)
    if not isinstance(enabled, bool):
        fail(f"Operation {index} has invalid enabled flag (must be boolean).")
    if not enabled:
        return None

    name = raw_operation.get("name", f"operation_{index}")
    if not isinstance(name, str) or not name.strip():
        fail(f"Operation {index} has invalid name.")
    name = name.strip()

    method = raw_operation.get("method")
    if not isinstance(method, str):
        fail(f"Operation {index} is missing method.")
    method = method.upper().strip()
    if method not in ALLOWED_METHODS:
        fail(f"Operation {index} uses unsupported method: {method}")

    raw_path = raw_operation.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        fail(f"Operation {index} is missing path.")
    if raw_path.startswith(("http://", "https://")):
        fail(f"Operation {index} path must be relative (not absolute URL).")

    path = raw_path.replace("{workspace_id}", workspace_id)
    if "{workspace_id}" in path:
        fail(f"Operation {index} has unresolved placeholders in path: {raw_path}")
    if not path.startswith("/"):
        fail(f"Operation {index} path must start with '/': {raw_path}")
    if not path.startswith("/v1/workspaces/"):
        fail(f"Operation {index} path must be workspace scoped: {raw_path}")
    if f"/workspaces/{workspace_id}" not in path:
        fail(f"Operation {index} path must target workspace_id={workspace_id}: {raw_path}")

    body = raw_operation.get("body")
    if body is not None and not isinstance(body, (dict, list, str, int, float, bool)):
        fail(f"Operation {index} has unsupported body type.")

    raw_headers = raw_operation.get("headers", {})
    if not isinstance(raw_headers, dict):
        fail(f"Operation {index} headers must be an object when provided.")
    headers: dict[str, str] = {}
    for key, value in raw_headers.items():
        if not isinstance(key, str) or not isinstance(value, str):
            fail(f"Operation {index} headers must contain string keys and values.")
        headers[key] = value

    description = raw_operation.get("description")
    if description is not None and not isinstance(description, str):
        fail(f"Operation {index} description must be a string.")

    if method == "DELETE" and not allow_delete:
        fail(f"Operation {index} uses DELETE but --allow-delete was not provided.")

    normalized = {
        "sequence": index,
        "name": name,
        "description": description or "",
        "method": method,
        "path_template": raw_path,
        "path": path,
        "url": f"{base_url.rstrip('/')}{path}",
        "headers": headers,
        "body": body,
    }
    return normalized


def load_current_items(args: argparse.Namespace, workspace_id: str) -> dict[str, Any]:
    if args.mode == "rest":
        token = os.getenv(args.token_env)
        if not token:
            fail(f"Missing bearer token in env var: {args.token_env}")
        raw_items = fetch_workspace_items(
            base_url=args.base_url.rstrip("/"),
            workspace_id=workspace_id,
            token=token,
        )
        source = {"mode": "rest", "workspace_id": workspace_id, "base_url": args.base_url}
    else:
        if not args.input_current:
            fail("--input-current is required in --mode file.")
        payload = read_json(Path(args.input_current))
        raw_items = extract_items(payload)
        if not raw_items and isinstance(payload, list):
            raw_items = [row for row in payload if isinstance(row, dict)]
        source = {"mode": "file", "input": str(Path(args.input_current).resolve())}

    items = canonical_items(raw_items, workspace_id=workspace_id)
    type_counts: dict[str, int] = {}
    for item in items:
        item_type = item["type"]
        type_counts[item_type] = type_counts.get(item_type, 0) + 1

    return {"source": source, "count": len(items), "type_counts": type_counts}


def summarize_methods(operations: list[dict[str, Any]]) -> dict[str, int]:
    counts = {method: 0 for method in ALLOWED_METHODS}
    for operation in operations:
        counts[operation["method"]] += 1
    return counts


def truncate_text(value: str, max_chars: int = 600) -> str:
    if len(value) <= max_chars:
        return value
    return f"{value[:max_chars]}...<truncated>"


def execute_operation(operation: dict[str, Any], token: str) -> dict[str, Any]:
    body = operation.get("body")
    request_data: bytes | None = None
    if body is not None:
        request_data = json.dumps(body, ensure_ascii=True).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if request_data is not None:
        headers["Content-Type"] = "application/json"
    headers.update(operation["headers"])

    req = request.Request(
        operation["url"],
        method=operation["method"],
        headers=headers,
        data=request_data,
    )

    try:
        with request.urlopen(req, timeout=120) as response:
            raw_response = response.read().decode("utf-8", errors="replace")
            return {
                "status": "success",
                "http_status": response.status,
                "response_preview": truncate_text(raw_response),
            }
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        return {
            "status": "failed",
            "http_status": exc.code,
            "response_preview": truncate_text(response_body),
            "error": f"HTTPError: {exc.reason}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "status": "failed",
            "http_status": None,
            "response_preview": "",
            "error": str(exc),
        }


def to_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Fabric Deploy Report",
        "",
        f"- Generated (UTC): `{plan['generated_utc']}`",
        f"- Action: `{plan['action']}`",
        f"- Workspace: `{plan['workspace_id']}`",
        f"- Current items discovered: **{plan['current_state']['count']}**",
        "",
        "## Method Summary",
        "",
    ]
    method_counts = plan["summary"]["method_counts"]
    for method in sorted(method_counts):
        lines.append(f"- `{method}`: **{method_counts[method]}**")
    lines.extend(["", "## Operations", ""])

    operations = plan.get("operations", [])
    if not operations:
        lines.extend(["_None_", ""])
        return "\n".join(lines)

    for op in operations:
        result = op.get("result", {})
        status = result.get("status", "planned")
        lines.append(f"- `{status}` | `{op['method']}` | `{op['name']}`")
        lines.append(f"  - Path: `{op['path']}`")
        if op.get("description"):
            lines.append(f"  - Description: {op['description']}")
        if result:
            if result.get("http_status") is not None:
                lines.append(f"  - HTTP status: `{result['http_status']}`")
            if result.get("error"):
                lines.append(f"  - Error: `{result['error']}`")
        lines.append("")

    return "\n".join(lines)


def run() -> None:
    args = parse_args()
    manifest_path = Path(args.desired_state)
    plan_output_path = Path(args.plan_output)
    report_output_path = Path(args.report_output)

    manifest = load_manifest(manifest_path)
    workspace_id = resolve_workspace_id(args.workspace_id, manifest)
    current_state = load_current_items(args, workspace_id=workspace_id)

    operations: list[dict[str, Any]] = []
    for index, raw_operation in enumerate(manifest.get("operations", []), start=1):
        normalized = normalize_operation(
            raw_operation=raw_operation,
            index=index,
            workspace_id=workspace_id,
            base_url=args.base_url,
            allow_delete=args.allow_delete,
        )
        if normalized:
            operations.append(normalized)

    if not operations:
        fail("No enabled operations found in manifest.")

    plan: dict[str, Any] = {
        "generated_utc": utc_now_iso(),
        "action": args.action,
        "workspace_id": workspace_id,
        "manifest_path": str(manifest_path.resolve()),
        "guardrails": {
            "allow_delete": args.allow_delete,
            "confirm_apply_required": True,
        },
        "current_state": current_state,
        "summary": {
            "operation_count": len(operations),
            "method_counts": summarize_methods(operations),
        },
        "operations": operations,
    }

    if args.action == "apply":
        if args.mode != "rest":
            fail("--action apply requires --mode rest.")
        if args.confirm_apply != "YES":
            fail("--confirm-apply YES is required for --action apply.")
        token = os.getenv(args.token_env)
        if not token:
            fail(f"Missing bearer token in env var: {args.token_env}")

        execution_results: list[dict[str, Any]] = []
        apply_failed = False
        for operation in operations:
            result = execute_operation(operation, token=token)
            operation["result"] = result
            execution_results.append(result)
            if result["status"] != "success":
                apply_failed = True
                break

        plan["executed_utc"] = utc_now_iso()
        plan["apply_summary"] = {
            "attempted": len(execution_results),
            "succeeded": sum(1 for row in execution_results if row["status"] == "success"),
            "failed": sum(1 for row in execution_results if row["status"] == "failed"),
            "failed_fast": apply_failed,
        }

    write_json(plan_output_path, plan)
    report_output_path.parent.mkdir(parents=True, exist_ok=True)
    report_output_path.write_text(to_markdown(plan), encoding="utf-8")

    print("Fabric deploy scaffold completed.")
    print(f"Action: {args.action}")
    print(f"Workspace: {workspace_id}")
    print(f"Operations: {len(operations)}")
    print(f"Plan output: {plan_output_path.as_posix()}")
    print(f"Report output: {report_output_path.as_posix()}")

    if args.action == "apply" and plan.get("apply_summary", {}).get("failed", 0) > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
