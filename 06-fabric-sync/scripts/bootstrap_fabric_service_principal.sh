#!/usr/bin/env bash

set -euo pipefail

# Bootstraps a Fabric service principal by minting a Fabric REST token and
# making a harmless workspace-items call. This mirrors the pipeline auth flow
# and avoids a local Azure CLI dependency.

usage() {
  cat <<'EOF'
Bootstrap a Fabric service principal for Warehouse SQL access.

Required environment variables:
  FABRIC_TENANT_ID
  FABRIC_CLIENT_ID
  FABRIC_CLIENT_SECRET
  FABRIC_WORKSPACE_ID

Usage:
  FABRIC_TENANT_ID="<tenant-id>" \
  FABRIC_CLIENT_ID="<client-id>" \
  FABRIC_CLIENT_SECRET="<client-secret>" \
  FABRIC_WORKSPACE_ID="<workspace-id>" \
  ./06-fabric-sync/scripts/bootstrap_fabric_service_principal.sh

What it does:
  1. Requests a Fabric bearer token using the service principal.
  2. Calls the workspace items endpoint to validate workspace reachability.
  3. Prints a short success/failure summary without echoing secrets.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

for required_var in FABRIC_TENANT_ID FABRIC_CLIENT_ID FABRIC_CLIENT_SECRET FABRIC_WORKSPACE_ID; do
  if [[ -z "${!required_var:-}" ]]; then
    echo "Missing required environment variable: ${required_var}" >&2
    usage >&2
    exit 1
  fi
done

token_response="$(curl -sS -X POST "https://login.microsoftonline.com/${FABRIC_TENANT_ID}/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=${FABRIC_CLIENT_ID}" \
  --data-urlencode "client_secret=${FABRIC_CLIENT_SECRET}" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "scope=https://api.fabric.microsoft.com/.default" \
  -w '\n%{http_code}')"

token_status="$(printf '%s' "${token_response}" | tail -n 1)"
token_body="$(printf '%s' "${token_response}" | sed '$d')"

if [[ "${token_status}" != "200" ]]; then
  echo "Failed to acquire Fabric bearer token (status ${token_status})." >&2
  if [[ -n "${token_body}" ]]; then
    printf '%s\n' "${token_body}" >&2
  else
    echo "Token endpoint returned an empty response body." >&2
  fi
  exit 1
fi

access_token="$(printf '%s' "${token_body}" | python3 -c '
import json
import sys

raw = sys.stdin.read().strip()
if not raw:
    print("")
    raise SystemExit(0)

try:
    payload = json.loads(raw)
except json.JSONDecodeError:
    print("")
    raise SystemExit(0)

print(payload.get("access_token", ""))
')"

if [[ -z "${access_token}" ]]; then
  echo "Token endpoint returned HTTP 200 but no access_token was present." >&2
  if [[ -n "${token_body}" ]]; then
    printf '%s\n' "${token_body}" >&2
  else
    echo "Token response body was empty." >&2
  fi
  exit 1
fi

workspace_response="$(curl -sS -w '\n%{http_code}' \
  -H "Authorization: Bearer ${access_token}" \
  "https://api.fabric.microsoft.com/v1/workspaces/${FABRIC_WORKSPACE_ID}/items")"

http_status="$(printf '%s' "${workspace_response}" | tail -n 1)"
response_body="$(printf '%s' "${workspace_response}" | sed '$d')"

if [[ "${http_status}" != "200" ]]; then
  echo "Fabric workspace bootstrap call failed (status ${http_status})." >&2
  printf '%s\n' "${response_body}" >&2
  exit 1
fi

item_count="$(printf '%s' "${response_body}" | python3 -c 'import json,sys; payload=json.load(sys.stdin); print(len(payload.get("value", payload.get("items", []))))')"

echo "Fabric service principal bootstrap succeeded."
echo "Workspace: ${FABRIC_WORKSPACE_ID}"
echo "Items visible: ${item_count}"
echo "Next step: run apply_warehouse_sql_pack.sh with sqlcmd service principal auth."
