id | decisión | contexto | alternativas | razón | consecuencias | estado | evidencia_msg_id
ADR_001 | usar Python para validación de datos | el usuario quiere validar datos antes de modelar | validar directamente en SQL | Python permite exploración flexible | se agrega dependencia pandas | aprobado | msg_190
ADR_002 | usar pandas para análisis inicial | pandas es estándar de análisis | usar solo SQL | facilidad de inspección | notebooks requeridos | aprobado | msg_214
ADR_003 | usar Jupyter Notebook | entorno interactivo | scripts Python | aprendizaje paso a paso | entorno reproducible | aprobado | msg_214
ADR_004 | ejecutar Jupyter desde terminal | flujo estándar de trabajo | IDE integrado | control directo del servidor | dependencia de terminal | aprobado | msg_221
ADR_005 | estructura de repo numerada | organización pedagógica | estructura plana | claridad progresiva | navegación clara | aprobado | msg_168
ADR_006 | usar CSV como fuente inicial | datos simples para aprendizaje | base de datos directa | accesibilidad | ingestión manual | aprobado | msg_130
ADR_007 | eliminar ":" en carpetas | error 404 detectado | mantener nombres originales | compatibilidad filesystem | notebooks funcionan | aprobado | msg_223
ADR_008 | retrasar SQL hasta validar datos | enfoque pedagógico | modelar primero | evitar errores de modelado | más tiempo de exploración | aprobado | msg_190
ADR_009 | crear notebook 01_data_validation | primer paso del pipeline | script Python | claridad de fase | estructura modular | aprobado | msg_235
ADR_010 | preparar exportación de conversación | conversación se volvió lenta | continuar sin documentación | preservar conocimiento | archivos de contexto | aprobado | msg_30
