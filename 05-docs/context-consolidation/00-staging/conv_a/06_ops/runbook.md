Precondiciones
1. Python instalado (msg_4)
2. pip funcional (msg_6)
3. librerías pandas duckdb jupyter instaladas (msg_6)
4. repositorio SALES ANALYTICS DASHBOARD creado (msg_18)

Comandos principales (zsh)
- cd ~/Desktop/SALES\ ANALYTICS\ DASHBOARD (msg_223)
- pwd (msg_223)
- ls (msg_223)

Instalar librerías
- python3 -m pip install pandas duckdb jupyter (msg_214)

Iniciar Jupyter
- jupyter notebook --port 8890 (msg_221)

Acceso
- http://localhost:8890 (msg_221)

Troubleshooting

1) ModuleNotFoundError: pandas (msg_214)
Causa: librería no instalada en el entorno activo.
Solución: instalar con pip. (msg_214)

2) 404 GET /api/contents/... (msg_223)
Causa: carácter ':' en nombre de carpeta.
Solución: renombrar carpetas eliminando ':'. (msg_223)

Cerrar servidor Jupyter
- presionar CTRL + C en la terminal donde corre Jupyter (msg_218)
