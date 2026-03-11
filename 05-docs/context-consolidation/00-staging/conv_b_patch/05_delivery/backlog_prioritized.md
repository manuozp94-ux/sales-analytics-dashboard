tarea | valor | esfuerzo relativo | riesgo | dependencia | definición de terminado | evidencia_msg_id
staging robusto order_reviews con parallel=false | desbloquea dataset | bajo | medio | duckdb conectado | tabla stg_order_reviews creada | UNKNOWN
desactivar auto typing con all_varchar | evita conversion errors | bajo | medio | tarea anterior | describe tabla funciona | UNKNOWN
confirmar staging completo stg_* | base modelo | bajo | bajo | archivos csv | show tables incluye todas | UNKNOWN
crear scripts SQL en 03-sql/models | permite star schema | medio | bajo | folder existente | archivos sql presentes | UNKNOWN
materializar dim_date | dimensión temporal | bajo | medio | stg_orders | tabla dim_date existe | UNKNOWN
materializar dim_customers | dimensión cliente | bajo | bajo | stg_customers | tabla dim_customers existe | UNKNOWN
materializar dim_products | dimensión producto | bajo | medio | stg_products | tabla dim_products existe | UNKNOWN
materializar fact_order_items | fact principal | medio | medio | dims creadas | grain validado | UNKNOWN
validar row counts | consistencia | bajo | medio | dims/fact | queries sin error | UNKNOWN
validar grain fact_order_items | unicidad | bajo | medio | fact creada | distinct(keys)=rows | UNKNOWN
