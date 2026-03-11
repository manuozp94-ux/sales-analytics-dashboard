# Objectives and Scope

## Objetivos

1. Construir una arquitectura reproducible de analytics engineering.
2. Migrar un prototipo local hacia Microsoft Fabric.
3. Implementar modelado dimensional estándar.
4. Crear validaciones de calidad de datos automatizadas.
5. Permitir consumo analítico por BI tools.

## No objetivos

1. Machine learning pipelines.
2. Streaming ingestion.
3. Real-time analytics.
4. Optimización avanzada de rendimiento.

## Supuestos

- Datos fuente provienen de dataset de e-commerce tipo Olist.
- Datos cargados inicialmente como CSV.
- Fabric Lakehouse utilizado para ingestión inicial.
- Warehouse utilizado para modelado dimensional.

## Restricciones

- Uso exclusivo de información contenida en la conversación.
- No se definieron controles de seguridad explícitos.
- No se discutieron esquemas de encriptación o clasificación de datos.

## Ambigüedades detectadas

1. No se definió explícitamente el dataset exacto.
2. No se especificaron identificadores de workspace.
3. No se documentaron configuraciones de RBAC.
