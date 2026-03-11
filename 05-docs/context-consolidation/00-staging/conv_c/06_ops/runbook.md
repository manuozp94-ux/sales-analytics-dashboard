# Operational Runbook

## Precondiciones
- Lakehouse creado y accesible
- Warehouse creado y accesible
- Tablas Delta en Lakehouse
- Pipeline Copy Data configurado

## Operación estándar

1) Ingestión
- Cargar CSV a Lakehouse → generar Delta tables

2) Staging load
- Ejecutar pipeline Copy Data Lakehouse → Warehouse `stg`

3) Model build
- Ejecutar scripts SQL para `core.dim_*` y `core.fact_*`

4) QA
- Ejecutar script QA consolidado
- Validar PASS

5) Consumo
- Conectar Power BI / semantic model (pendiente)

## Troubleshooting

### Duplicación de registros (full copy)
Síntoma: row counts duplicados tras correr pipeline dos veces.
Acción:
- Truncar tablas staging
- Reconfigurar pipeline para truncate+load o incremental

### Errores de datatype (datetime2 precision)
Síntoma: error de precisión 0-6 requerida.
Acción:
- Usar datetime2(0) ... datetime2(6) explícito.

### Tablas no visibles
Acción:
- Refresh en explorer
- Verificar schema correcto

## Post-run checklist
- Row counts staging esperados
- Dims/facts creados
- QA PASS
