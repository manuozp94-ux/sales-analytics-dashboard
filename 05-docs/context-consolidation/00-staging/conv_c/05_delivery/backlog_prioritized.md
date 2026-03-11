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
