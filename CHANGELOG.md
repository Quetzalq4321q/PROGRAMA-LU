# Changelog

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-10-05

### Añadido
- **Empaquetado en Docker**: Creación de `Dockerfile`, `docker-compose.yml` y `.dockerignore` para ejecutar el programa en cualquier sistema sin necesidad de tener Python instalado.
- **Modo Menú Interactivo en Terminal**: Nuevo flag `python main.py --menu` y fallback automático cuando no hay servidor gráfico disponible (entornos headless/Docker).
- **Scripts de Ejecución Rápida en Windows**: Archivos batch `EJECUTAR_ANALIZADOR_LU.bat` y `EJECUTAR_DEMO_CONSOLA.bat`.
- **Configuración de Control de Versiones**: Integración con repositorio remoto de GitHub (`https://github.com/Quetzalq4321q/PROGRAMA-LU.git`) y `.gitignore` exhaustivo.

### Cambiado
- **Rediseño Orgánico de la GUI**: Eliminación de emojis/iconos superpuestos en botones y sustitución por una estética minimalista, bordes suaves, paleta Slate/Azul y espaciado proporcional en celdas.
- **Renombrado de Módulo de Modelos**: Migración de `core/types.py` a `core/models.py` para prevenir colisiones con la biblioteca estándar `types` de Python.
- **Resolución Automática de Rutas (`sys.path`)**: Cada módulo cuenta con su propio bloque `__main__` y resolución de directorio raíz para permitir ejecución individual directa.

---

## [1.1.0] - 2026-10-05

### Añadido
- **Arquitectura Modular Desacoplada**: Subdivisión del motor de cálculo en el paquete `core/` (`doolittle.py`, `doolittle_pivot.py`, `parsers.py`, `matrix_ops.py`, `formatters.py`, `linear_system.py`).
- **Paquete de Ejemplos**: Módulo `examples/presets.py` con matrices representativas precargadas (3x3 clásico, 3x3 con pivote 0, 4x4 y 2x2).
- **Suite de Pruebas Unitarias**: Directorio `tests/` con cobertura para parseo, algoritmos de Doolittle con y sin pivoteo, y resolución de sistemas $Ax=b$.

### Cambiado
- Desacoplamiento total de la lógica matemática respecto a la interfaz gráfica.

---

## [1.0.0] - 2026-10-05

### Añadido
- Implementación inicial del método de Doolittle para descomposición LU ($A = L \cdot U$).
- Implementación de Doolittle con pivoteo parcial ($P \cdot A = L \cdot U$).
- Soporte para cálculo exacto mediante `fractions.Fraction` y representación decimal.
- Resolución de sistemas de ecuaciones lineales simultáneos $A \cdot x = b$.
- Interfaz gráfica inicial en Tkinter con cuadrícula interactiva y área de texto plano.
