# Analizador y Calculador de Descomposición LU

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-11%20passing-brightgreen.svg)

Software de álgebra lineal numérica para realizar la **Descomposición LU** de matrices cuadradas $N \times N$, implementando el método de **Doolittle clásico ($A = L \cdot U$)** y **Doolittle con pivoteo parcial ($P \cdot A = L \cdot U$)**, resolución simultánea de sistemas de ecuaciones lineales $A \cdot x = b$, representación en **fracciones analíticas exactas** o **decimales**, desglose paso a paso y empaquetado en **Docker**.

---

## 📑 Tabla de Contenidos
1. [Características Principales](#-características-principales)
2. [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
3. [Ejecución con Docker (Sin necesidad de instalar Python)](#-ejecución-con-docker-sin-python-instalado)
4. [Ejecución Local en Windows/Linux/macOS](#-ejecución-local)
5. [Casos de Prueba y Resultados](#-casos-de-prueba-y-resultados)
6. [Flujo de Git y Repositorio](#-repositorio-github)

---

## 🌟 Características Principales

- **Doble Modo de Entrada Flexible:**
  - **Cuadrícula Visual ($N \times N$):** Interfaz interactiva con celdas independientes, navegación ergonómica mediante flechas del teclado (`↑`, `↓`, `←`, `→`), `Tab` y `Enter`.
  - **Texto Plano:** Permite pegar matrices directamente desde apuntes, Excel, MATLAB o Python (filas delimitadas por saltos de línea, espacios, comas o `;`).
  - **Sincronización Bidireccional:** Un clic para convertir de cuadrícula a texto plano o viceversa.
- **Precisión Aritmética:**
  - **Fracciones exactas:** Sin errores de redondeo numérico (ej. `1/3`, `-3/4`, `9/4`).
  - **Decimales:** Con selector de precisión configurable (de 1 a 8 decimales).
- **Resolución de Sistemas $A \cdot x = b$:**
  - Sustitución progresiva: $L \cdot y = P \cdot b$.
  - Sustitución regresiva: $U \cdot x = y$.
- **Transparencia Analítica:** Pestaña de procedimiento paso a paso que expone fórmulas, multiplicadores y sumas calculadas en cada iteración.
- **Multiplataforma y Portable:** Funciona en Windows, Linux, macOS y dentro de contenedores Docker.

---

## 📂 Arquitectura del Proyecto

El código está organizado siguiendo principios de responsabilidad única y bajo acoplamiento:

```text
ANALIZADOR LU/
├── core/                       # Motor matemático central
│   ├── __init__.py             # API unificada del núcleo
│   ├── models.py               # Estructuras de datos (LUResult, SystemSolution)
│   ├── parsers.py              # Parseo tolerante de texto a matrices
│   ├── matrix_ops.py           # Álgebra matricial (matmul, mat_vec_mul, identidad)
│   ├── formatters.py           # Alineación tipográfica y generación de reportes
│   ├── doolittle.py            # Algoritmo de Doolittle clásico (A = L·U)
│   ├── doolittle_pivot.py      # Algoritmo de Doolittle con pivoteo (P·A = L·U)
│   └── linear_system.py        # Sustitución hacia adelante y hacia atrás
├── examples/                   # Casos de prueba representativos
│   ├── __init__.py
│   └── presets.py              # Matrices precargadas (3x3 clásico, 3x3 pivote 0, 4x4, 2x2)
├── tests/                      # Suite de pruebas unitarias
│   ├── test_parsers.py         # Pruebas de lectura y parseo
│   ├── test_doolittle.py       # Pruebas del método sin pivoteo
│   ├── test_pivot.py           # Pruebas de pivoteo parcial
│   └── test_system.py          # Pruebas de resolución de sistemas Ax = b
├── gui.py                      # Interfaz gráfica de usuario (Tkinter)
├── main.py                     # Punto de entrada unificado (GUI, CLI, menú y tests)
├── Dockerfile                  # Empaquetado Docker para ejecución sin Python
├── docker-compose.yml          # Orquestación de Docker Compose
├── EJECUTAR_ANALIZADOR_LU.bat  # Lanzador directo con 1 clic en Windows
├── EJECUTAR_DEMO_CONSOLA.bat   # Lanzador directo de consola en Windows
├── CHANGELOG.md                # Registro histórico de versiones
└── README.md                   # Esta documentación
```

---

## 🐳 Ejecución con Docker (Sin Python Instalado)

Si no tienes Python instalado en tu máquina o prefieres aislar la ejecución, puedes usar Docker:

### Opción 1: Con Docker Compose (Recomendado)
```bash
docker compose run --rm analizador-lu
```
Iniciará el menú interactivo por terminal donde podrás seleccionar ver las demostraciones o ingresar cualquier matriz $N \times N$.

### Opción 2: Construir y Ejecutar con Docker CLI
1. Construir la imagen:
   ```bash
   docker build -t analizador-lu .
   ```
2. Ejecutar el menú interactivo:
   ```bash
   docker run -it --rm analizador-lu
   ```
3. Ejecutar solo las pruebas automáticas:
   ```bash
   docker run --rm analizador-lu --run-tests
   ```
4. Ejecutar la demostración rápida de matrices:
   ```bash
   docker run --rm analizador-lu --cli
   ```

---

## 💻 Ejecución Local

### En Windows (Sin tocar comandos)
- Haz doble clic sobre **`EJECUTAR_ANALIZADOR_LU.bat`** para abrir la interfaz gráfica.
- Haz doble clic sobre **`EJECUTAR_DEMO_CONSOLA.bat`** para ver la demostración en consola.

### Desde Terminal / PyCharm
```bash
# Iniciar la interfaz gráfica
python main.py

# Iniciar en modo consola interactivo
python main.py --menu

# Ejecutar demostración en consola
python main.py --cli

# Ejecutar la suite completa de pruebas unitarias (11 tests)
python main.py --run-tests
```

---

## 🧪 Casos de Prueba y Resultados

### Caso 1: Matriz 3×3 sin pivoteo ($A = L \cdot U$)
$$A_1 = \begin{pmatrix} 2 & -1 & -2 \\ -4 & 6 & 3 \\ -4 & -2 & 8 \end{pmatrix}$$

- **Matriz $L$ (Triangular inferior unitaria):**
  $$L = \begin{pmatrix} 1 & 0 & 0 \\ -2 & 1 & 0 \\ -2 & -1 & 1 \end{pmatrix}$$
- **Matriz $U$ (Triangular superior):**
  $$U = \begin{pmatrix} 2 & -1 & -2 \\ 0 & 4 & -1 \\ 0 & 0 & 3 \end{pmatrix}$$
- **Verificación:** $L \cdot U = A_1$ $\checkmark$
- **Determinante:** $\det(A_1) = 24$.

---

### Caso 2: Matriz 3×3 con pivoteo parcial ($P \cdot A = L \cdot U$)
$$A_2 = \begin{pmatrix} 0 & 2 & 1 \\ 1 & -1 & 1 \\ 2 & 1 & -1 \end{pmatrix}$$

*(Presenta $a_{11} = 0$, requiriendo permutación para evitar división entre cero).*

- **Matriz de Permutación $P$:**
  $$P = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$$
- **Matriz $L$:**
  $$L = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 1/2 & -3/4 & 1 \end{pmatrix}$$
- **Matriz $U$:**
  $$U = \begin{pmatrix} 2 & 1 & -1 \\ 0 & 2 & 1 \\ 0 & 0 & 9/4 \end{pmatrix}$$
- **Verificación:** $L \cdot U = P \cdot A_2$ $\checkmark$
- **Determinante:** $\det(A_2) = 9$.

---

## 🌐 Repositorio GitHub

Repositorio oficial:
👉 **[https://github.com/Quetzalq4321q/PROGRAMA-LU.git](https://github.com/Quetzalq4321q/PROGRAMA-LU.git)**
