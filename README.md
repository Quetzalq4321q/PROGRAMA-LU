# Analizador y Calculador de Descomposición LU

Programa en Python para el cálculo y análisis de la Descomposición LU de matrices cuadradas de orden N x N. Implementa el método de Doolittle clásico (A = L * U) y el método de Doolittle con pivoteo parcial (P * A = L * U), con soporte para cálculo exacto en fracciones o aproximación decimal, resolución de sistemas de ecuaciones lineales y desglose analítico paso a paso.

---

## Indice

1. Caracteristicas
2. Documentacion del Codigo y Estructura
3. Fundamento Matematico
4. Guia de Uso y Ejecucion
   - Ejecucion con Docker (sin instalar Python)
   - Ejecucion en Windows (acceso directo)
   - Ejecucion por linea de comandos
5. Casos de Prueba Verificados
6. Pruebas Unitarias
7. Repositorio

---

## 1. Caracteristicas

- Doble modalidad de entrada: Cuadricula visual interactiva de tamano N x N y caja de texto plano con soporte de copiado y pegado directo desde hojas de calculo, MATLAB o apuntes.
- Sincronizacion bidireccional entre la cuadricula visual y el texto plano.
- Precision analitica: Soporte para fracciones exactas mediante la biblioteca estandar de Python, evitando errores de redondeo por punto flotante.
- Modo decimal configurable de 1 a 8 cifras decimales.
- Resolucion opcional de sistemas de ecuaciones lineales A * x = b mediante sustitucion progresiva y regresiva.
- Generacion de reporte detallado con operaciones aritmeticas paso a paso.
- Empaquetado completo en Docker para ejecucion portable en cualquier sistema operativo.

---

## 2. Documentacion del Codigo y Estructura

El proyecto esta organizado bajo una arquitectura modular desacoplada en la que cada componente cumple una funcion especifica e independiente.

### Mapa de Archivos

```text
ANALIZADOR LU/
├── core/
│   ├── __init__.py           Punto de exportacion publico del paquete core.
│   ├── models.py             Estructuras de datos (LUResult, SystemSolution) y tipos.
│   ├── parsers.py            Lectura y transformacion de texto a matrices y vectores.
│   ├── matrix_ops.py         Operaciones algebraicas basicas (multiplicacion, comparacion, identidad).
│   ├── formatters.py         Alineacion de matrices en texto y generacion de reportes.
│   ├── doolittle.py          Algoritmo de Doolittle sin pivoteo (A = L * U).
│   ├── doolittle_pivot.py    Algoritmo de Doolittle con pivoteo parcial (P * A = L * U).
│   └── linear_system.py      Resolucion del sistema lineal (L*y = P*b, U*x = y).
├── examples/
│   ├── __init__.py           Exportacion de casos de prueba.
│   └── presets.py            Matrices precargadas (3x3 estandar, 3x3 pivote cero, 4x4 y 2x2).
├── tests/
│   ├── __init__.py           Inicializador de pruebas unitarias.
│   ├── test_parsers.py       Validacion de lectura de datos numericos y formatos.
│   ├── test_doolittle.py     Validacion del algoritmo de Doolittle clasico.
│   ├── test_pivot.py         Validacion del algoritmo con pivoteo parcial.
│   └── test_system.py        Validacion de resolucion de sistemas Ax = b.
├── gui.py                    Interfaz grafica de usuario desarrollada en Tkinter.
├── main.py                   Punto de entrada principal (GUI, CLI, menu y tests).
├── generate_icon.py          Script de generacion de los iconos de la aplicacion.
├── icon.ico / icon.png       Iconos oficiales del programa.
├── Dockerfile                Definicion de contenedor Docker para ejecucion portable.
├── docker-compose.yml        Orquestador de Docker Compose.
├── .dockerignore             Archivos excluidos de la imagen Docker.
├── .gitignore                Reglas de exclusion para el control de versiones Git.
├── EJECUTAR_ANALIZADOR_LU.bat  Lanzador directo para la interfaz grafica en Windows.
├── EJECUTAR_DEMO_CONSOLA.bat   Lanzador directo de la demostracion en consola en Windows.
├── CHANGELOG.md              Registro historico de versiones del proyecto.
└── README.md                 Documentacion tecnica del software.
```

### Descripcion de Modulos Principales

- `core/models.py`: Define los tipos de datos principales (`Matrix`, `Vector`, `Number`) y las clases contenedoras de resultados (`LUResult` y `SystemSolution`).
- `core/parsers.py`: Interpreta entradas de texto escritas por el usuario. Maneja elementos separados por espacios, comas, punto y coma, corchetes, fracciones como `3/4` y decimales con punto o coma.
- `core/matrix_ops.py`: Contiene funciones matematicas base para la multiplicacion de matrices (`matmul`), multiplicacion matriz-vector (`mat_vec_mul`), generacion de matrices identidad y comparacion de matrices con tolerancia numerica.
- `core/doolittle.py`: Ejecuta la factorizacion clasica de Doolittle. Calcula fila por fila la matriz triangular superior `U` y columna por columna los multiplicadores de la matriz triangular inferior `L` (con unos en la diagonal principal). Registra cada sustitucion analitica en un historial de pasos. Lanza una excepcion explicita si encuentra un pivote nulo.
- `core/doolittle_pivot.py`: Aplica la eliminacion gaussiana con pivoteo parcial por columnas. Localiza el valor de mayor magnitud absoluta bajo la diagonal principal, permuta las filas correspondientes en la matriz de permutacion `P`, en la matriz de trabajo y en los coeficientes ya calculados de `L`, garantizando estabilidad numerica.
- `core/linear_system.py`: Utiliza las matrices calculadas para resolver sistemas lineales:
  1. Aplica la permutacion al vector de terminos independientes: `b* = P * b`.
  2. Resuelve por sustitucion hacia adelante el sistema triangular inferior: `L * y = b*`.
  3. Resuelve por sustitucion hacia atras el sistema triangular superior: `U * x = y`.
- `core/formatters.py`: Transforma estructuras matriciales en texto con columnas monoespaciadas perfectamente alineadas y ensambla el reporte consolidado listo para copiar o exportar.
- `gui.py`: Construye la interfaz visual mediante Tkinter. Gestiona la interaccion de la cuadricula de celdas, el editor de texto, los selectores de metodos y la visualizacion de resultados en pestañas independientes.

---

## 3. Fundamento Matematico

### Metodo de Doolittle sin Pivoteo
Dada una matriz cuadrada A de dimension n x n, se busca descomponerla en el producto:

```text
A = L * U
```

donde:
- L es una matriz triangular inferior con diagonal unitaria (l_ii = 1 para todo i).
- U es una matriz triangular superior (u_ij = 0 para todo i > j).

Las formulas de calculo para la etapa k (k = 0, ..., n - 1) son:

1. Elementos de la fila k de U:
```text
u_kj = a_kj - SUM(l_km * u_mj)  para j = k, ..., n - 1 (m desde 0 hasta k - 1)
```

2. Multiplicadores de la columna k de L:
```text
l_ik = (a_ik - SUM(l_im * u_mk)) / u_kk  para i = k + 1, ..., n - 1 (m desde 0 hasta k - 1)
```

Si en cualquier etapa el elemento pivote `u_kk` resulta ser igual a cero, la division no puede realizarse y el metodo requiere pivoteo parcial.

### Metodo de Doolittle con Pivoteo Parcial
Para evitar divisiones entre cero y reducir la propagacion de errores por redondeo, en cada etapa k se localiza el indice de fila p tal que:

```text
|a_pk| = max { |a_ik| } para i = k, ..., n - 1
```

Si p != k, se intercambia la fila k con la fila p en la matriz A, en la matriz de permutacion P y en los multiplicadores previos calculados en L. La relacion obtenida satisface:

```text
P * A = L * U
```

---

## 4. Guia de Uso y Ejecucion

### Opcion A: Ejecucion con Docker (No requiere Python instalado)

Esta opcion permite ejecutar el software en cualquier equipo con Docker instalado, sin necesidad de configurar entornos de Python.

1. Iniciar con Docker Compose:
```bash
docker compose run --rm analizador-lu
```

2. O compilar y ejecutar manualmente con la CLI de Docker:
```bash
docker build -t analizador-lu .
docker run -it --rm analizador-lu
```

El contenedor iniciara un menu interactivo en terminal para elegir entre ver demostraciones, ingresar una matriz personalizada o correr la suite de pruebas.

### Opcion B: Ejecucion en Windows con Doble Clic

Si se dispone de Windows y se desea utilizar la interfaz grafica sin abrir consolas:
- Haga doble clic sobre `EJECUTAR_ANALIZADOR_LU.bat` para iniciar la aplicacion grafica.
- Haga doble clic sobre `EJECUTAR_DEMO_CONSOLA.bat` para ver la ejecucion de prueba en terminal.

### Opcion C: Ejecucion por Linea de Comandos

En cualquier terminal con Python 3.10 o superior:

```bash
# Iniciar la interfaz grafica
python main.py

# Iniciar el menu interactivo en consola (ideal para terminales remotas)
python main.py --menu

# Ejecutar la demostracion rapida de matrices de prueba
python main.py --cli

# Ejecutar la suite de pruebas unitarias
python main.py --run-tests
```

---

## 5. Casos de Prueba Verificados

### Caso 1: Matriz 3x3 sin Pivoteo (Doolittle Clasico)

Matriz de entrada:
```text
A = [  2  -1  -2 ]
    [ -4   6   3 ]
    [ -4  -2   8 ]
```

Resultados obtenidos:
- Matriz L:
```text
L = [  1   0   0 ]
    [ -2   1   0 ]
    [ -2  -1   1 ]
```
- Matriz U:
```text
U = [  2  -1  -2 ]
    [  0   4  -1 ]
    [  0   0   3 ]
```
- Comprobacion: L * U coincide exactamente con la matriz original A.
- Determinante: det(A) = 24.

---

### Caso 2: Matriz 3x3 con Pivote Inicial Cero (Requiere Pivoteo Parcial)

Matriz de entrada:
```text
A = [  0   2   1 ]
    [  1  -1   1 ]
    [  2   1  -1 ]
```

El elemento a_11 es igual a 0, por lo que el metodo sin pivoteo falla por division entre cero. Al aplicar pivoteo parcial, se intercambia la Fila 1 con la Fila 3.

Resultados obtenidos:
- Matriz de Permutacion P:
```text
P = [  0   0   1 ]
    [  1   0   0 ]
    [  0   1   0 ]
```
- Matriz L:
```text
L = [   1     0   0 ]
    [   0     1   0 ]
    [ 1/2  -3/4   1 ]
```
- Matriz U:
```text
U = [  2    1   -1 ]
    [  0    2    1 ]
    [  0    0  9/4 ]
```
- Comprobacion: L * U coincide exactamente con la matriz permutada P * A.
- Determinante: det(A) = 9.

---

## 6. Pruebas Unitarias

El proyecto incluye 11 pruebas automatizadas que verifican el parseo de datos, la precision del calculo algebraico, el manejo de errores de pivote cero y la resolucion de sistemas lineales.

Para ejecutarlas:
```bash
python main.py --run-tests
```
o mediante el modulo estandar de Python:
```bash
python -m unittest discover tests
```

---

## 7. Repositorio

Repositorio de control de versiones:
https://github.com/Quetzalq4321q/PROGRAMA-LU.git
