tarea | valor | esfuerzo relativo | riesgo | dependencia | definición de terminado | evidencia_msg_id

P0 | cargar CSV en pandas | iniciar exploración de datos | bajo | dataset desconocido | CSV en carpeta data | CSV cargado, dataframe visible, columnas inspectadas | msg_27
P0 | validar claves primarias | integridad para modelo futuro | bajo | duplicados no detectados | dataframe cargado | conteo de duplicados y verificación de unicidad | msg_28
P0 | validar grain de dataset | definir nivel de detalle analítico | medio | interpretación incorrecta | dataset cargado | clave natural identificada y grain descrito | msg_28

P1 | diseñar star schema | base de modelo analítico | medio | grain incorrecto | validación dataset | fact definida y dimensiones identificadas | msg_130
P1 | escribir SQL de transformación | preparar data marts | medio | transformación incorrecta | modelo dimensional | scripts SQL funcionales y tablas generadas | msg_130

P2 | migrar arquitectura a Microsoft Fabric | arquitectura moderna escalable | alto | desconocimiento plataforma | modelo SQL estable | lakehouse creado, warehouse implementado, notebooks migrados | msg_40
P2 | preparar semantic layer | consumo BI | medio | métricas incorrectas | warehouse implementado | dataset semántico y medidas definidas | msg_40
