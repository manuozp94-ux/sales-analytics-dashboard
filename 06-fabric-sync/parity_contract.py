#!/usr/bin/env python3
"""
Canonical parity contract for local DuckDB vs Fabric Warehouse validation.
"""

from __future__ import annotations

from typing import Any


CONTRACT_VERSION = "2026-03-14"

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

KPI_TYPES = {
    "total_orders": "count",
    "approval_rate": "rate",
    "on_time_delivery_rate": "rate",
    "avg_delivery_time_days": "average",
    "gmv": "money",
    "revenue_total": "money",
    "avg_order_value": "average",
    "avg_items_per_order": "average",
    "freight_ratio": "rate",
    "avg_review_score": "average",
}

KPI_SQL_DUCKDB = {
    "total_orders": """
        select count(distinct order_id)::double
        from fact_orders
    """,
    "approval_rate": """
        select
            sum(
                case
                    when order_status <> 'canceled'
                      and order_approved_at is not null
                    then 1 else 0
                end
            )::double
            / nullif(
                count(
                    case
                        when order_status <> 'canceled' then 1
                    end
                ),
                0
            )
        from fact_orders
    """,
    "on_time_delivery_rate": """
        select
            sum(
                case
                    when order_status = 'delivered'
                      and order_delivered_customer_date <= order_estimated_delivery_date
                    then 1 else 0
                end
            )::double
            / nullif(
                count(
                    case
                        when order_status = 'delivered' then 1
                    end
                ),
                0
            )
        from fact_orders
    """,
    "avg_delivery_time_days": """
        select
            avg(
                case
                    when order_status = 'delivered'
                      and order_delivered_customer_date is not null
                    then datediff('day', order_purchase_timestamp, order_delivered_customer_date)
                end
            )::double
        from fact_orders
    """,
    "gmv": """
        select sum(price)::double
        from fact_order_items
    """,
    "revenue_total": """
        select sum(price + freight_value)::double
        from fact_order_items
    """,
    "avg_order_value": """
        select sum(price)::double / nullif(count(distinct order_id), 0)
        from fact_order_items
    """,
    "avg_items_per_order": """
        select count(*)::double / nullif(count(distinct order_id), 0)
        from fact_order_items
    """,
    "freight_ratio": """
        select sum(freight_value)::double / nullif(sum(price), 0)
        from fact_order_items
    """,
    "avg_review_score": """
        select avg(cast(review_score as integer))::double
        from fact_order_reviews
    """,
}

GRAIN_CHECKS = [
    {
        "name": "dim_date_pk_unique",
        "sql_duckdb": """
            select count(*)
            from (
                select date_key
                from dim_date
                group by date_key
                having count(*) > 1
            ) x
        """,
    },
    {
        "name": "dim_customers_pk_unique",
        "sql_duckdb": """
            select count(*)
            from (
                select customer_id
                from dim_customers
                group by customer_id
                having count(*) > 1
            ) x
        """,
    },
    {
        "name": "dim_products_pk_unique",
        "sql_duckdb": """
            select count(*)
            from (
                select product_id
                from dim_products
                group by product_id
                having count(*) > 1
            ) x
        """,
    },
    {
        "name": "fact_orders_grain_order_id",
        "sql_duckdb": """
            select count(*)
            from (
                select order_id
                from fact_orders
                group by order_id
                having count(*) > 1
            ) x
        """,
    },
    {
        "name": "fact_order_items_grain_order_item",
        "sql_duckdb": """
            select count(*)
            from (
                select order_id, order_item_id
                from fact_order_items
                group by order_id, order_item_id
                having count(*) > 1
            ) x
        """,
    },
    {
        "name": "fact_order_payments_grain_payment_seq",
        "sql_duckdb": """
            select count(*)
            from (
                select order_id, payment_sequential
                from fact_order_payments
                group by order_id, payment_sequential
                having count(*) > 1
            ) x
        """,
    },
    {
        "name": "fact_order_reviews_grain_review_order",
        "sql_duckdb": """
            select count(*)
            from (
                select review_id, order_id
                from fact_order_reviews
                group by review_id, order_id
                having count(*) > 1
            ) x
        """,
    },
]

NULL_KEY_CHECKS = [
    {"name": "dim_date_date_key_nulls", "sql_duckdb": "select count(*) from dim_date where date_key is null"},
    {
        "name": "dim_customers_customer_id_nulls",
        "sql_duckdb": "select count(*) from dim_customers where customer_id is null",
    },
    {
        "name": "dim_products_product_id_nulls",
        "sql_duckdb": "select count(*) from dim_products where product_id is null",
    },
    {"name": "fact_orders_order_id_nulls", "sql_duckdb": "select count(*) from fact_orders where order_id is null"},
    {
        "name": "fact_orders_customer_id_nulls",
        "sql_duckdb": "select count(*) from fact_orders where customer_id is null",
    },
    {
        "name": "fact_orders_purchase_date_key_nulls",
        "sql_duckdb": "select count(*) from fact_orders where purchase_date_key is null",
    },
    {
        "name": "fact_order_items_order_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_items where order_id is null",
    },
    {
        "name": "fact_order_items_order_item_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_items where order_item_id is null",
    },
    {
        "name": "fact_order_items_customer_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_items where customer_id is null",
    },
    {
        "name": "fact_order_items_product_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_items where product_id is null",
    },
    {
        "name": "fact_order_items_date_key_nulls",
        "sql_duckdb": "select count(*) from fact_order_items where date_key is null",
    },
    {
        "name": "fact_order_payments_order_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_payments where order_id is null",
    },
    {
        "name": "fact_order_payments_customer_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_payments where customer_id is null",
    },
    {
        "name": "fact_order_payments_purchase_date_key_nulls",
        "sql_duckdb": "select count(*) from fact_order_payments where purchase_date_key is null",
    },
    {
        "name": "fact_order_reviews_order_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_reviews where order_id is null",
    },
    {
        "name": "fact_order_reviews_customer_id_nulls",
        "sql_duckdb": "select count(*) from fact_order_reviews where customer_id is null",
    },
    {
        "name": "fact_order_reviews_purchase_date_key_nulls",
        "sql_duckdb": "select count(*) from fact_order_reviews where purchase_date_key is null",
    },
]

ORPHAN_CHECKS = [
    {
        "name": "fact_orders_orphans_dim_customers",
        "sql_duckdb": """
            select count(*)
            from fact_orders f
            left join dim_customers d on d.customer_id = f.customer_id
            where d.customer_id is null
        """,
    },
    {
        "name": "fact_orders_orphans_dim_date",
        "sql_duckdb": """
            select count(*)
            from fact_orders f
            left join dim_date d on d.date_key = f.purchase_date_key
            where d.date_key is null
        """,
    },
    {
        "name": "fact_order_items_orphans_fact_orders",
        "sql_duckdb": """
            select count(*)
            from fact_order_items f
            left join fact_orders o on o.order_id = f.order_id
            where o.order_id is null
        """,
    },
    {
        "name": "fact_order_items_orphans_dim_customers",
        "sql_duckdb": """
            select count(*)
            from fact_order_items f
            left join dim_customers d on d.customer_id = f.customer_id
            where d.customer_id is null
        """,
    },
    {
        "name": "fact_order_items_orphans_dim_products",
        "sql_duckdb": """
            select count(*)
            from fact_order_items f
            left join dim_products d on d.product_id = f.product_id
            where d.product_id is null
        """,
    },
    {
        "name": "fact_order_items_orphans_dim_date",
        "sql_duckdb": """
            select count(*)
            from fact_order_items f
            left join dim_date d on d.date_key = f.date_key
            where d.date_key is null
        """,
    },
    {
        "name": "fact_order_payments_orphans_fact_orders",
        "sql_duckdb": """
            select count(*)
            from fact_order_payments f
            left join fact_orders o on o.order_id = f.order_id
            where o.order_id is null
        """,
    },
    {
        "name": "fact_order_payments_orphans_dim_customers",
        "sql_duckdb": """
            select count(*)
            from fact_order_payments f
            left join dim_customers d on d.customer_id = f.customer_id
            where d.customer_id is null
        """,
    },
    {
        "name": "fact_order_payments_orphans_dim_date",
        "sql_duckdb": """
            select count(*)
            from fact_order_payments f
            left join dim_date d on d.date_key = f.purchase_date_key
            where d.date_key is null
        """,
    },
    {
        "name": "fact_order_reviews_orphans_fact_orders",
        "sql_duckdb": """
            select count(*)
            from fact_order_reviews f
            left join fact_orders o on o.order_id = f.order_id
            where o.order_id is null
        """,
    },
    {
        "name": "fact_order_reviews_orphans_dim_customers",
        "sql_duckdb": """
            select count(*)
            from fact_order_reviews f
            left join dim_customers d on d.customer_id = f.customer_id
            where d.customer_id is null
        """,
    },
    {
        "name": "fact_order_reviews_orphans_dim_date",
        "sql_duckdb": """
            select count(*)
            from fact_order_reviews f
            left join dim_date d on d.date_key = f.purchase_date_key
            where d.date_key is null
        """,
    },
]


def kpi_tolerance(metric_name: str) -> float:
    metric_type = KPI_TYPES[metric_name]
    if metric_type == "count":
        return 0.0
    if metric_type in {"money", "average"}:
        return 0.01
    if metric_type == "rate":
        return 0.0005
    raise ValueError(f"Unsupported metric type for {metric_name}: {metric_type}")


def contract_summary() -> dict[str, Any]:
    return {
        "version": CONTRACT_VERSION,
        "required_objects": REQUIRED_OBJECTS,
        "required_kpis": list(KPI_TYPES.keys()),
        "kpi_types": KPI_TYPES,
        "acceptance_tolerances": {
            "count_exact": 0.0,
            "money_absolute": 0.01,
            "average_absolute": 0.01,
            "rate_absolute": 0.0005,
        },
        "qa_expected": {
            "grain_checks": len(GRAIN_CHECKS),
            "null_key_checks": len(NULL_KEY_CHECKS),
            "orphan_checks": len(ORPHAN_CHECKS),
        },
    }
