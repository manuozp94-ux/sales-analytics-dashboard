# Consolidated Backlog

## CONV_A

tarea | valor | esfuerzo relativo | riesgo | dependencia | definición de terminado | evidencia_msg_id

P0 | cargar CSV en pandas | iniciar exploración de datos | bajo | dataset desconocido | CSV en carpeta data | CSV cargado, dataframe visible, columnas inspectadas | msg_27
P0 | validar claves primarias | integridad para modelo futuro | bajo | duplicados no detectados | dataframe cargado | conteo de duplicados y verificación de unicidad | msg_28
P0 | validar grain de dataset | definir nivel de detalle analítico | medio | interpretación incorrecta | dataset cargado | clave natural identificada y grain descrito | msg_28

P1 | diseñar star schema | base de modelo analítico | medio | grain incorrecto | validación dataset | fact definida y dimensiones identificadas | msg_130
P1 | escribir SQL de transformación | preparar data marts | medio | transformación incorrecta | modelo dimensional | scripts SQL funcionales y tablas generadas | msg_130

P2 | migrar arquitectura a Microsoft Fabric | arquitectura moderna escalable | alto | desconocimiento plataforma | modelo SQL estable | lakehouse creado, warehouse implementado, notebooks migrados | msg_40
P2 | preparar semantic layer | consumo BI | medio | métricas incorrectas | warehouse implementado | dataset semántico y medidas definidas | msg_40

## CONV_B

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

## CONV_C

# Prioritized Backlog

## P0

tarea | valor | esfuerzo relativo | riesgo | dependencia | definición de terminado | evidencia_msg_id
Implementar marts analíticos en Warehouse | habilita analítica avanzada | medio | medio | core tables | marts creados y QA PASS | UNKNOWN
Crear semantic model en Fabric | habilita Power BI | medio | bajo | marts | semantic model publicado | UNKNOWN
Resolver duplicación por full copy | integridad datos | bajo | alto | pipeline | staging sin duplicados | UNKNOWN
Integrar QA en pipeline | calidad automática | bajo | medio | QA script | QA ejecutado en cada corrida | UNKNOWN

## P1

tarea | valor | esfuerzo relativo | riesgo | dependencia | definición de terminado | evidencia_msg_id
Automatizar deployment SQL | reproducibilidad enterprise | medio | medio | repositorio | CI/CD scripts | UNKNOWN
Monitoring y alertas pipeline | operación estable | medio | medio | pipeline | alertas activas | UNKNOWN
Documentar métricas y contratos | gobernanza | bajo | bajo | metric contract | documento completo | UNKNOWN

## P2

tarea | valor | esfuerzo relativo | riesgo | dependencia | definición de terminado | evidencia_msg_id
Optimización performance SQL | costo/tiempo | medio | bajo | warehouse | queries optimizadas | UNKNOWN
SCD para dimensiones | analítica temporal | alto | medio | core | SCD implementado | UNKNOWN
Data catalog / lineage | gobernanza | medio | bajo | fabric | lineage visible | UNKNOWN
