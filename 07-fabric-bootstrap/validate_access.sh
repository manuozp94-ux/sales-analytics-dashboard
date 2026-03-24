#!/usr/bin/env bash

set -euo pipefail

placeholder_exact_re='^(changeme|change_me|your[_-].*|example|example[_-].*|tbd|todo|replace[_-].*|dummy|placeholder)$'
uuid_re='^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
warehouse_host_re='^[A-Za-z0-9-]+\.datawarehouse\.fabric\.microsoft\.com,1433$'

errors=0
warnings=0

is_placeholder() {
  local value="$1"

  if [[ "${value}" == *"<"*">"* ]]; then
    return 0
  fi

  if [[ "${value}" =~ ${placeholder_exact_re} ]]; then
    return 0
  fi

  return 1
}

check_required() {
  local name="$1"
  local value="${!name:-}"

  if [[ -z "${value}" ]]; then
    printf 'FAIL  %s is not set\n' "${name}"
    errors=$((errors + 1))
    return
  fi

  if is_placeholder "${value}"; then
    printf 'FAIL  %s still contains a placeholder value\n' "${name}"
    errors=$((errors + 1))
    return
  fi

  printf 'PASS  %s is set\n' "${name}"
}

check_optional() {
  local name="$1"
  local value="${!name:-}"

  if [[ -z "${value}" ]]; then
    printf 'INFO  %s is not set\n' "${name}"
    return
  fi

  if is_placeholder "${value}"; then
    printf 'WARN  %s is set but still looks like a placeholder\n' "${name}"
    warnings=$((warnings + 1))
    return
  fi

  printf 'PASS  %s is set\n' "${name}"
}

check_uuid_like() {
  local name="$1"
  local value="${!name:-}"

  if [[ -z "${value}" ]]; then
    return
  fi

  if is_placeholder "${value}"; then
    return
  fi

  if [[ "${value}" =~ ${uuid_re} ]]; then
    printf 'PASS  %s looks like a GUID\n' "${name}"
  else
    printf 'WARN  %s does not look like a GUID\n' "${name}"
    warnings=$((warnings + 1))
  fi
}

check_endpoint_like() {
  local name="$1"
  local value="${!name:-}"

  if [[ -z "${value}" ]]; then
    return
  fi

  if is_placeholder "${value}"; then
    return
  fi

  if [[ "${value}" =~ ${warehouse_host_re} ]]; then
    printf 'PASS  %s matches Fabric Warehouse host:port pattern\n' "${name}"
  else
    printf 'WARN  %s does not match expected Fabric Warehouse host:port pattern\n' "${name}"
    warnings=$((warnings + 1))
  fi
}

check_secret_only_set() {
  local name="$1"
  local value="${!name:-}"

  if [[ -z "${value}" ]]; then
    return
  fi

  if is_placeholder "${value}"; then
    return
  fi

  printf 'PASS  %s is present (value intentionally not echoed)\n' "${name}"
}

printf 'Fabric access validation\n'
printf '\n'
printf 'Checking canonical service-principal auth path...\n'

check_required FABRIC_TENANT_ID
check_required FABRIC_CLIENT_ID
check_required FABRIC_CLIENT_SECRET
check_required FABRIC_WORKSPACE_ID

check_uuid_like FABRIC_TENANT_ID
check_uuid_like FABRIC_CLIENT_ID
check_uuid_like FABRIC_WORKSPACE_ID
check_secret_only_set FABRIC_CLIENT_SECRET

printf '\n'
printf 'Checking optional/manual REST values...\n'

check_optional FABRIC_BEARER_TOKEN
check_optional FABRIC_API_BASE_URL
check_optional FABRIC_WORKSPACE_NAME

if [[ -n "${FABRIC_API_BASE_URL:-}" ]] && ! is_placeholder "${FABRIC_API_BASE_URL}" && [[ "${FABRIC_API_BASE_URL}" != "https://api.fabric.microsoft.com" ]]; then
  printf 'WARN  FABRIC_API_BASE_URL is overridden from the repo default\n'
  warnings=$((warnings + 1))
fi

printf '\n'
printf 'Checking Warehouse SQL assumptions...\n'

check_optional FABRIC_WAREHOUSE_NAME
check_optional FABRIC_WAREHOUSE_DATABASE
check_optional FABRIC_WAREHOUSE_SQL_ENDPOINT
check_optional SQLCMD_BIN
check_endpoint_like FABRIC_WAREHOUSE_SQL_ENDPOINT

if [[ -n "${SQLCMD_BIN:-}" ]]; then
  if is_placeholder "${SQLCMD_BIN}"; then
    :
  elif [[ -x "${SQLCMD_BIN}" ]]; then
    printf 'PASS  SQLCMD_BIN points to an executable\n'
  else
    printf 'WARN  SQLCMD_BIN is set but not executable from this shell\n'
    warnings=$((warnings + 1))
  fi
else
  if command -v sqlcmd >/dev/null 2>&1; then
    printf 'PASS  sqlcmd is available on PATH\n'
  else
    printf 'WARN  sqlcmd is not on PATH and SQLCMD_BIN is not set\n'
    warnings=$((warnings + 1))
  fi
fi

printf '\n'
printf 'Checking connection-model consistency...\n'

if [[ -n "${FABRIC_WAREHOUSE_SQL_ENDPOINT:-}" && -z "${FABRIC_WAREHOUSE_DATABASE:-}" ]]; then
  printf 'WARN  FABRIC_WAREHOUSE_SQL_ENDPOINT is set but FABRIC_WAREHOUSE_DATABASE is missing\n'
  warnings=$((warnings + 1))
fi

if [[ -n "${FABRIC_WAREHOUSE_DATABASE:-}" && -z "${FABRIC_WAREHOUSE_SQL_ENDPOINT:-}" ]]; then
  printf 'WARN  FABRIC_WAREHOUSE_DATABASE is set but FABRIC_WAREHOUSE_SQL_ENDPOINT is missing\n'
  warnings=$((warnings + 1))
fi

if [[ -n "${FABRIC_BEARER_TOKEN:-}" && -n "${FABRIC_CLIENT_SECRET:-}" ]] && ! is_placeholder "${FABRIC_BEARER_TOKEN}" && ! is_placeholder "${FABRIC_CLIENT_SECRET}"; then
  printf 'INFO  Both service-principal credentials and FABRIC_BEARER_TOKEN are set; canonical repo path prefers runtime token minting\n'
fi

if [[ -n "${FABRIC_BEARER_TOKEN:-}" ]] && ! is_placeholder "${FABRIC_BEARER_TOKEN}" && [[ -z "${FABRIC_TENANT_ID:-}" || -z "${FABRIC_CLIENT_ID:-}" || -z "${FABRIC_CLIENT_SECRET:-}" ]]; then
  printf 'INFO  FABRIC_BEARER_TOKEN can support REST-only testing, but the repo-standard bootstrap still expects service-principal credentials for full parity with Warehouse SQL access\n'
fi

if [[ -n "${FABRIC_WAREHOUSE_NAME:-}" && -n "${FABRIC_WAREHOUSE_DATABASE:-}" ]] && ! is_placeholder "${FABRIC_WAREHOUSE_NAME}" && ! is_placeholder "${FABRIC_WAREHOUSE_DATABASE}" && [[ "${FABRIC_WAREHOUSE_NAME}" != "${FABRIC_WAREHOUSE_DATABASE}" ]]; then
  printf 'INFO  FABRIC_WAREHOUSE_NAME and FABRIC_WAREHOUSE_DATABASE differ; this is valid if your environment uses different display and database names\n'
fi

printf '\n'
printf 'Summary\n'
printf 'Errors: %s\n' "${errors}"
printf 'Warnings: %s\n' "${warnings}"

if (( errors > 0 )); then
  printf 'Result: FAIL\n'
  exit 1
fi

if (( warnings > 0 )); then
  printf 'Result: PASS WITH WARNINGS\n'
  exit 0
fi

printf 'Result: PASS\n'
