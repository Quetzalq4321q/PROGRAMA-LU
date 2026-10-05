"""
Punto de entrada principal para el Analizador de Descomposición LU.

Uso:
    python main.py              -> Inicia la interfaz gráfica interactiva (GUI)
    python main.py --cli        -> Ejecuta demostración de las matrices de prueba en consola
    python main.py --menu       -> Modo consola interactivo (ideal para Docker o sin entorno gráfico)
    python main.py --run-tests  -> Ejecuta la suite completa de pruebas unitarias
"""

import sys
import unittest
from pathlib import Path

# Garantizar que la raíz del proyecto esté en sys.path
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core import (
    parse_matrix_text, parse_vector_text, format_matrix, format_number,
    format_vector, build_full_report, lu_doolittle_no_pivot, lu_doolittle_pivot,
    solve_system_lu
)
from examples import PRESETS


def run_cli_demos():
    """Ejecuta demostraciones de las matrices de prueba directamente en la terminal."""
    print("=" * 70)
    print(" DEMOSTRACIÓN DE DESCOMPOSICIÓN LU (MÉTODOS DE DOOLITTLE)")
    print("=" * 70)

    # 1. Prueba para la Matriz 1 (sin pivoteo)
    p1 = PRESETS[0]
    print(f"\n>>> PRUEBA 1: {p1.title}")
    print(f"    Descripción: {p1.description}")
    A1 = parse_matrix_text(p1.matrix_text)
    print("Matriz A:")
    print(format_matrix(A1))

    res1 = lu_doolittle_no_pivot(A1)
    print("\nMatriz L (Triangular inferior unitaria):")
    print(format_matrix(res1.L))
    print("\nMatriz U (Triangular superior):")
    print(format_matrix(res1.U))
    print("\nComprobación L · U:")
    print(format_matrix(res1.LU))
    print(f"Verificación L * U == A: {res1.is_correct} [OK]")
    print(f"Determinante: det(A) = {format_number(res1.det_A)}")

    # 2. Prueba para la Matriz 2 (con pivoteo)
    p2 = PRESETS[1]
    print("\n" + "=" * 70)
    print(f">>> PRUEBA 2: {p2.title}")
    print(f"    Descripción: {p2.description}")
    A2 = parse_matrix_text(p2.matrix_text)
    print("Matriz A:")
    print(format_matrix(A2))

    res2 = lu_doolittle_pivot(A2)
    print("\nMatriz de permutación P:")
    print(format_matrix(res2.P))
    print("\nMatriz permutada P · A:")
    print(format_matrix(res2.PA))
    print("\nMatriz L (Triangular inferior unitaria):")
    print(format_matrix(res2.L))
    print("\nMatriz U (Triangular superior):")
    print(format_matrix(res2.U))
    print("\nComprobación L · U:")
    print(format_matrix(res2.LU))
    print(f"Verificación L * U == P * A: {res2.is_correct} [OK]")
    print(f"Determinante: det(A) = {format_number(res2.det_A)}")
    print("=" * 70)


def run_interactive_cli():
    """Modo consola interactivo para entornos sin interfaz gráfica (ej. contenedores Docker)."""
    print("\n==================================================")
    print(" ANALIZADOR DE DESCOMPOSICIÓN LU (MODO CONSOLA)")
    print("==================================================")
    while True:
        print("\nSeleccione una opción:")
        print("  1) Ver demostración con matrices de prueba")
        print("  2) Ingresar y descomponer matriz personalizada")
        print("  3) Ejecutar suite de pruebas unitarias")
        print("  4) Salir")
        choice = input("\nOpción (1-4): ").strip()

        if choice == "1":
            run_cli_demos()
        elif choice == "2":
            try:
                n_str = input("\nIngrese la dimensión N de la matriz cuadrada (ej. 3): ").strip()
                if not n_str.isdigit() or int(n_str) < 2:
                    print("[!] Debe ingresar un número entero mayor o igual a 2.")
                    continue
                n = int(n_str)
                print(f"\nIngrese las {n} filas de la matriz (números separados por espacios o comas):")
                lines = []
                for i in range(n):
                    row = input(f"  Fila {i + 1}: ").strip()
                    lines.append(row)
                text_matrix = "\n".join(lines)
                A = parse_matrix_text(text_matrix, use_fractions=True)

                piv = input("\n¿Usar pivoteo parcial? (S/n): ").strip().lower() != "n"
                res = lu_doolittle_pivot(A) if piv else lu_doolittle_no_pivot(A)

                solve_b = input("¿Desea resolver un sistema A·x = b? (s/N): ").strip().lower() == "s"
                b = None
                res_sys = None
                if solve_b:
                    b_str = input(f"Ingrese los {n} elementos del vector b separados por espacios o comas: ").strip()
                    b = parse_vector_text(b_str, expected_len=n, use_fractions=True)
                    if b:
                        res_sys = solve_system_lu(res.P, res.L, res.U, b)

                report = build_full_report(A, res, b, res_sys, as_fraction=True)
                print("\n" + report)

                show_steps = input("\n¿Desea ver el desarrollo paso a paso? (s/N): ").strip().lower() == "s"
                if show_steps:
                    print("\n" + res.steps)
                    if res_sys:
                        print("\n" + res_sys.steps)

            except Exception as e:
                print(f"\n[!] Error en el cálculo: {e}")
        elif choice == "3":
            run_unit_tests()
        elif choice in ("4", "q", "exit"):
            print("\nHasta luego.")
            break
        else:
            print("[!] Opción inválida.")


def run_unit_tests():
    """Ejecuta los tests unitarios descubiertos en la carpeta tests/."""
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def main():
    """Punto de entrada de ejecución con fallback automático para entornos headless."""
    if "--run-tests" in sys.argv:
        run_unit_tests()
    elif "--cli" in sys.argv or "--test" in sys.argv:
        run_cli_demos()
    elif "--menu" in sys.argv:
        run_interactive_cli()
    else:
        try:
            from gui import LUApp
            app = LUApp()
            app.mainloop()
        except Exception as e:
            # Si no hay servidor de pantalla X11/Windows (ej. contenedor Docker sin DISPLAY)
            print(f"\n[AVISO] No se pudo iniciar el entorno gráfico ({e}).")
            print("Iniciando automáticamente en modo consola interactivo...\n")
            run_interactive_cli()


if __name__ == "__main__":
    main()
