# ==============================================================================
# Dockerfile para Analizador de Descomposición LU
# Permite ejecutar el programa sin tener Python instalado en el sistema anfitrión.
# ==============================================================================

FROM python:3.12-slim

# Evitar creación de archivos .pyc y habilitar salida en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar soporte de Tkinter por si se ejecuta con reenvío X11 / GUI
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    tk \
    tcl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar paquetes y módulos del proyecto
COPY core/ /app/core/
COPY examples/ /app/examples/
COPY tests/ /app/tests/
COPY main.py /app/main.py
COPY gui.py /app/gui.py

# Por defecto inicia el menú interactivo por consola en Docker
ENTRYPOINT ["python", "main.py"]
CMD ["--menu"]
