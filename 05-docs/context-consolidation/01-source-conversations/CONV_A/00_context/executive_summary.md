Objetivo del trabajo documentado en esta conversación:

Construir un proyecto técnico de Analytics Engineering como ejercicio de aprendizaje y portafolio profesional que cubra:

1. preparación de entorno Python
2. uso de terminal (zsh)
3. uso de Jupyter Notebooks
4. validación de datos desde CSV con pandas
5. diseño posterior de modelo analítico (star schema)
6. futura migración conceptual a Microsoft Fabric.

Estado real del proyecto al cierre de la conversación:

Entorno local configurado:

- Sistema operativo: macOS (terminal zsh).
- Python instalado.
- Librerías instaladas: pandas, duckdb, jupyter.
- Servidor Jupyter ejecutándose localmente.
- Notebook creado: `01_data_validation.ipynb`.

Repositorio de proyecto creado:

`SALES ANALYTICS DASHBOARD`

Estructura mencionada:

01 - data/  
02 - notebooks/  
03 - sql/  
04 - docs/

Problema técnico relevante resuelto:

Error al crear notebooks en Jupyter:

`404 GET /api/contents/02 - notebooks:Untitled.ipynb`

Causa:
uso de carácter `:` en nombre de carpeta.

Solución aplicada:
renombrar carpetas para eliminar `:`.

Estado del trabajo técnico:

FASE ACTUAL  
Preparación del entorno + apertura del primer notebook para validación de datos.

FASE SIGUIENTE (definida en conversación):

1. cargar CSV con pandas
2. validar claves primarias
3. validar grain de tablas
4. definir star schema
5. implementar SQL
6. eventualmente mover arquitectura a Microsoft Fabric.

Limitaciones detectadas en la conversación:

- no se proporcionaron datasets reales.
- no se definió esquema de tablas.
- no se definieron métricas de negocio.
- no existe implementación SQL todavía.

Próximos pasos recomendados:

1. implementar carga CSV en notebook.
2. validar estructura de datos.
3. definir modelo dimensional.
4. construir SQL de staging y marts.
5. preparar arquitectura compatible con Fabric (Lakehouse + Warehouse).
