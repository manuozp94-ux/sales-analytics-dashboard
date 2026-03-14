#!/usr/bin/env bash

set -euo pipefail

# Applies the canonical Warehouse SQL pack with sqlcmd.
# sqlcmd runs on the calling host (local shell or CI agent); the SQL executes
# against the remote Fabric Warehouse endpoint provided in the forwarded args.

usage() {
  cat <<'EOF'
Apply the canonical Fabric Warehouse SQL pack with sqlcmd.

Usage:
  ./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only
  ./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh \
    [--include-legacy-cleanup] \
    [--include-reset] \
    --confirm-apply YES \
    -- <sqlcmd args...>

Examples:
  ./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh --print-only

  ./06-fabric-sync/scripts/apply_warehouse_sql_pack.sh \
    --confirm-apply YES \
    -- \
    -S "<warehouse_sql_endpoint>" \
    -d "wh_sales_analytics" \
    -U "<sql_user>" \
    -P "<sql_password>"

Notes:
  - Arguments after `--` are passed directly to sqlcmd.
  - Optional scripts are skipped by default:
      --include-legacy-cleanup -> 02_drop_legacy_marts_schema_safe.sql
      --include-reset          -> 01_reset_core_mart_safe.sql
  - The parity query pack and catalog probe are not materialization steps and
    are intentionally excluded from this apply script.
EOF
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
warehouse_sql_dir="${repo_root}/06-fabric-sync/sql/fabric-warehouse"
bundled_sqlcmd_bin="${repo_root}/06-fabric-sync/tools/sqlcmd/sqlcmd"

if [[ -n "${SQLCMD_BIN:-}" ]]; then
  sqlcmd_bin="${SQLCMD_BIN}"
elif [[ -x "${bundled_sqlcmd_bin}" ]]; then
  sqlcmd_bin="${bundled_sqlcmd_bin}"
else
  sqlcmd_bin="sqlcmd"
fi

print_only=false
include_legacy_cleanup=false
include_reset=false
confirm_apply=""
declare -a sqlcmd_args=()

while (($# > 0)); do
  case "$1" in
    --print-only)
      print_only=true
      shift
      ;;
    --include-legacy-cleanup)
      include_legacy_cleanup=true
      shift
      ;;
    --include-reset)
      include_reset=true
      shift
      ;;
    --confirm-apply)
      shift
      if (($# == 0)); then
        echo "Missing value for --confirm-apply." >&2
        usage >&2
        exit 1
      fi
      confirm_apply="$1"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      sqlcmd_args=("$@")
      break
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

declare -a sql_files=(
  "00_schema_bootstrap.sql"
)

if [[ "${include_legacy_cleanup}" == "true" ]]; then
  sql_files+=("02_drop_legacy_marts_schema_safe.sql")
fi

if [[ "${include_reset}" == "true" ]]; then
  sql_files+=("01_reset_core_mart_safe.sql")
fi

sql_files+=(
  "05_stg_compat_views.sql"
  "10_core_dim_date.sql"
  "11_core_dim_customers.sql"
  "12_core_dim_products.sql"
  "20_core_fact_orders.sql"
  "21_core_fact_order_items.sql"
  "22_core_fact_order_payments.sql"
  "23_core_fact_order_reviews.sql"
  "30_mart_cohort_unit_economics.sql"
  "31_mart_monthly_business_snapshot.sql"
  "32_mart_customer_ltv_summary.sql"
)

if [[ "${print_only}" == "true" ]]; then
  echo "Planned Warehouse SQL apply order:"
  for idx in "${!sql_files[@]}"; do
    printf '  %02d. %s\n' "$((idx + 1))" "${sql_files[idx]}"
  done
  exit 0
fi

if [[ "${confirm_apply}" != "YES" ]]; then
  echo "Refusing to execute without --confirm-apply YES." >&2
  exit 1
fi

if ((${#sqlcmd_args[@]} == 0)); then
  echo "No sqlcmd connection arguments were provided." >&2
  usage >&2
  exit 1
fi

if ! command -v "${sqlcmd_bin}" >/dev/null 2>&1; then
  echo "sqlcmd was not found. Install it or set SQLCMD_BIN to the executable path." >&2
  exit 1
fi

echo "Applying ${#sql_files[@]} Warehouse SQL files with ${sqlcmd_bin}..."

for idx in "${!sql_files[@]}"; do
  sql_file="${sql_files[idx]}"
  sql_path="${warehouse_sql_dir}/${sql_file}"

  if [[ ! -f "${sql_path}" ]]; then
    echo "Missing SQL file: ${sql_path}" >&2
    exit 1
  fi

  printf '\n[%02d/%02d] %s\n' "$((idx + 1))" "${#sql_files[@]}" "${sql_file}"
  "${sqlcmd_bin}" "${sqlcmd_args[@]}" -i "${sql_path}"
done

echo ""
echo "Warehouse SQL pack apply completed."
