#!/usr/bin/env python3
"""
Fabric inventory sync utility.

Use this script to persist a normalized snapshot of Microsoft Fabric workspace
artifacts into this repo and generate a diff against the prior snapshot.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import parse, request


DEFAULT_BASE_URL = "https://api.fabric.microsoft.com"


@dataclass(frozen=True)
class ItemKey:
    item_id: str
    item_type: str
    name: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Fabric workspace inventory into a versioned JSON snapshot."
    )
    parser.add_argument("--workspace-id", help="Fabric workspace ID.", default=None)
    parser.add_argument(
        "--mode",
        choices=["rest", "file"],
        required=True,
        help="Data source mode: Fabric REST API or local JSON file.",
    )
    parser.add_argument(
        "--input",
        help="Path to input JSON file when --mode file.",
        default=None,
    )
    parser.add_argument(
        "--token-env",
        default="FABRIC_BEARER_TOKEN",
        help="Env var name containing a Fabric bearer token for --mode rest.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Fabric API base URL for --mode rest.",
    )
    parser.add_argument(
        "--state-dir",
        default="06-fabric-sync/state",
        help="Directory where snapshots and diff files are stored.",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Input file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str, token: str) -> dict[str, Any]:
    req = request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except Exception as exc:  # noqa: BLE001
        fail(f"REST request failed for {url}: {exc}")


def extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []

    for key in ("value", "items", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    return []


def next_page_url(payload: dict[str, Any], base_url: str, workspace_id: str) -> str | None:
    for key in ("continuationUri", "@odata.nextLink", "nextLink", "next"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value

    token = payload.get("continuationToken")
    if isinstance(token, str) and token.strip():
        encoded = parse.quote(token, safe="")
        return f"{base_url}/v1/workspaces/{workspace_id}/items?continuationToken={encoded}"
    return None


def fetch_workspace_items(base_url: str, workspace_id: str, token: str) -> list[dict[str, Any]]:
    first_url = f"{base_url}/v1/workspaces/{workspace_id}/items"
    items: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    current_url: str | None = first_url

    while current_url:
        if current_url in seen_urls:
            fail("Pagination loop detected while reading Fabric items.")
        seen_urls.add(current_url)
        payload = fetch_json(current_url, token)
        items.extend(extract_items(payload))
        current_url = next_page_url(payload, base_url=base_url, workspace_id=workspace_id)

    return items


def normalize_item(raw: dict[str, Any], workspace_id: str | None) -> dict[str, Any]:
    item_id = (
        raw.get("id")
        or raw.get("itemId")
        or raw.get("objectId")
        or raw.get("workspaceItemId")
        or "UNKNOWN_ID"
    )
    name = raw.get("displayName") or raw.get("name") or "UNKNOWN_NAME"
    item_type = raw.get("type") or raw.get("itemType") or raw.get("kind") or "UNKNOWN_TYPE"
    ws = raw.get("workspaceId") or workspace_id or "UNKNOWN_WORKSPACE"
    updated = (
        raw.get("lastUpdatedTime")
        or raw.get("lastUpdatedDateTime")
        or raw.get("modifiedDateTime")
        or raw.get("updatedAt")
        or None
    )

    return {
        "id": str(item_id),
        "name": str(name),
        "type": str(item_type),
        "workspace_id": str(ws),
        "last_updated": None if updated is None else str(updated),
    }


def canonical_items(raw_items: list[dict[str, Any]], workspace_id: str | None) -> list[dict[str, Any]]:
    items = [normalize_item(raw, workspace_id=workspace_id) for raw in raw_items]
    items.sort(key=lambda x: (x["type"], x["name"], x["id"]))
    return items


def load_previous_snapshot(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    payload = read_json(path)
    if isinstance(payload, dict):
        return payload
    return None


def item_key(item: dict[str, Any]) -> ItemKey:
    return ItemKey(item_id=item["id"], item_type=item["type"], name=item["name"])


def diff_snapshots(old_items: list[dict[str, Any]], new_items: list[dict[str, Any]]) -> dict[str, Any]:
    old_map = {item_key(item): item for item in old_items}
    new_map = {item_key(item): item for item in new_items}

    old_keys = set(old_map)
    new_keys = set(new_map)

    added = sorted(new_keys - old_keys, key=lambda k: (k.item_type, k.name, k.item_id))
    removed = sorted(old_keys - new_keys, key=lambda k: (k.item_type, k.name, k.item_id))

    # Tracks changed metadata for exact same key.
    changed: list[dict[str, Any]] = []
    shared = sorted(old_keys & new_keys, key=lambda k: (k.item_type, k.name, k.item_id))
    for key in shared:
        old_item = old_map[key]
        new_item = new_map[key]
        if old_item.get("last_updated") != new_item.get("last_updated"):
            changed.append(
                {
                    "id": key.item_id,
                    "type": key.item_type,
                    "name": key.name,
                    "old_last_updated": old_item.get("last_updated"),
                    "new_last_updated": new_item.get("last_updated"),
                }
            )

    def key_to_row(key: ItemKey) -> dict[str, str]:
        return {"id": key.item_id, "type": key.item_type, "name": key.name}

    return {"added": [key_to_row(k) for k in added], "removed": [key_to_row(k) for k in removed], "changed": changed}


def to_markdown(diff: dict[str, Any], snapshot_path: Path) -> str:
    added = diff["added"]
    removed = diff["removed"]
    changed = diff["changed"]

    lines = [
        "# Fabric Inventory Diff",
        "",
        f"- Snapshot file: `{snapshot_path.as_posix()}`",
        f"- Added: **{len(added)}**",
        f"- Removed: **{len(removed)}**",
        f"- Changed: **{len(changed)}**",
        "",
    ]

    def block(title: str, rows: list[dict[str, Any]]) -> None:
        lines.append(f"## {title}")
        if not rows:
            lines.append("")
            lines.append("_None_")
            lines.append("")
            return
        lines.append("")
        for row in rows:
            lines.append(f"- `{row['type']}` | `{row['name']}` | `{row['id']}`")
        lines.append("")

    block("Added", added)
    block("Removed", removed)

    lines.append("## Changed")
    if not changed:
        lines.append("")
        lines.append("_None_")
    else:
        lines.append("")
        for row in changed:
            lines.append(
                "- `{type}` | `{name}` | `{id}` | last_updated: `{old}` -> `{new}`".format(
                    type=row["type"],
                    name=row["name"],
                    id=row["id"],
                    old=row["old_last_updated"],
                    new=row["new_last_updated"],
                )
            )
    lines.append("")
    return "\n".join(lines)


def run() -> None:
    args = parse_args()
    state_dir = Path(args.state_dir)
    latest_snapshot_path = state_dir / "fabric_inventory_latest.json"
    latest_diff_md_path = state_dir / "fabric_inventory_diff_latest.md"

    if args.mode == "rest":
        if not args.workspace_id:
            fail("--workspace-id is required in --mode rest.")
        token = os.getenv(args.token_env)
        if not token:
            fail(f"Missing bearer token in env var: {args.token_env}")
        raw_items = fetch_workspace_items(
            base_url=args.base_url.rstrip("/"),
            workspace_id=args.workspace_id,
            token=token,
        )
        source = {"mode": "rest", "workspace_id": args.workspace_id, "base_url": args.base_url}
    else:
        if not args.input:
            fail("--input is required in --mode file.")
        payload = read_json(Path(args.input))
        raw_items = extract_items(payload)
        if not raw_items and isinstance(payload, list):
            raw_items = [x for x in payload if isinstance(x, dict)]
        source = {"mode": "file", "input": str(Path(args.input).resolve())}

    items = canonical_items(raw_items, workspace_id=args.workspace_id)
    snapshot = {
        "snapshot_utc": utc_now_iso(),
        "source": source,
        "workspace_id": args.workspace_id or "UNKNOWN_WORKSPACE",
        "item_count": len(items),
        "items": items,
    }

    prev_snapshot = load_previous_snapshot(latest_snapshot_path)
    prev_items = prev_snapshot.get("items", []) if prev_snapshot else []
    diff = diff_snapshots(prev_items, items)

    stamped_snapshot_path = state_dir / "history" / f"fabric_inventory_{utc_stamp()}.json"
    write_json(stamped_snapshot_path, snapshot)
    write_json(latest_snapshot_path, snapshot)
    latest_diff_md_path.parent.mkdir(parents=True, exist_ok=True)
    latest_diff_md_path.write_text(to_markdown(diff, stamped_snapshot_path), encoding="utf-8")

    print("Fabric inventory sync completed.")
    print(f"Snapshot items: {len(items)}")
    print(f"Latest snapshot: {latest_snapshot_path.as_posix()}")
    print(f"History snapshot: {stamped_snapshot_path.as_posix()}")
    print(f"Latest diff: {latest_diff_md_path.as_posix()}")
    print(f"Added: {len(diff['added'])} | Removed: {len(diff['removed'])} | Changed: {len(diff['changed'])}")


if __name__ == "__main__":
    run()
