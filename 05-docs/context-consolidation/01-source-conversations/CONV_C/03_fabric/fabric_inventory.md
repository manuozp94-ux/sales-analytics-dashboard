# Fabric Artifact Inventory

Artifact | Purpose | Status | Dependencies
Lakehouse | ingestión CSV | activo | dataset CSV
Warehouse | modelo dimensional | activo | pipeline copy
Copy Data Pipeline | mover datos lakehouse → warehouse | activo | lakehouse tables
stg schema | staging data | activo | pipeline
core schema | modelo dimensional | activo | SQL scripts
marts schema | analítica | pendiente | core tables
QA script | validación modelo | activo | core tables
Notebooks (local) | prototipado inicial | completado | DuckDB environment
DuckDB local db | desarrollo inicial | completado | CSV dataset
