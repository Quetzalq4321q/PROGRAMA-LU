"""
Interfaz Gráfica de Usuario (GUI) moderna, orgánica y desacoplada para la Descomposición LU.
Permite entrada por Cuadrícula Visual interactiva (N x N) y por Texto Plano,
con visualización de matrices L, U, P, verificación y resolución de sistemas Ax=b.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fractions import Fraction
from typing import List, Optional, Tuple

from core import (
    parse_matrix_text, parse_vector_text, format_matrix, format_vector,
    format_number, build_full_report, lu_doolittle_no_pivot, lu_doolittle_pivot,
    solve_system_lu, Matrix, Vector, LUResult, SystemSolution
)
from examples import PRESETS, get_preset_by_id

# Paleta de color suave, moderna y armónica
COLOR_BG = "#f8fafc"           # Fondo principal gris perla
COLOR_SURFACE = "#ffffff"      # Superficie de tarjetas
COLOR_SURFACE_ALT = "#f1f5f9"  # Fondo de celdas y áreas secundarias
COLOR_BORDER = "#e2e8f0"       # Bordes sutiles
COLOR_BORDER_FOCUS = "#3b82f6" # Borde al enfocar celda
COLOR_TEXT = "#0f172a"         # Texto principal de alto contraste
COLOR_TEXT_MUTED = "#64748b"   # Texto secundario
COLOR_PRIMARY = "#2563eb"      # Azul rey elegante
COLOR_PRIMARY_HOVER = "#1d4ed8"# Azul hover
COLOR_ACCENT_BG = "#eff6ff"    # Azul translúcido de acento
COLOR_SUCCESS = "#059669"      # Verde esmeralda


class LUApp(tk.Tk):
    """Ventana principal del analizador y calculador LU."""

    def __init__(self):
        super().__init__()
        self.title("Descomposición LU · Analizador Matricial")
        self.geometry("1200x780")
        self.minsize(1000, 680)
        self.configure(bg=COLOR_BG)

        # Variables de control
        self.matrix_size = tk.IntVar(value=3)
        self.method_var = tk.StringVar(value="pivot")       # "pivot" o "no_pivot"
        self.format_var = tk.StringVar(value="fraction")    # "fraction" o "decimal"
        self.decimals_var = tk.IntVar(value=4)
        self.solve_system_var = tk.BooleanVar(value=False)

        # Listas de referencias a widgets interactivos
        self.grid_entries: List[List[tk.Entry]] = []
        self.b_entries: List[tk.Entry] = []

        self.apply_theme()
        self.build_layout()
        self.load_preset(1)

    def apply_theme(self):
        """Aplica estilos visuales orgánicos con ttk."""
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        # Configuración base
        self.style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=COLOR_BG)
        self.style.configure("Card.TFrame", background=COLOR_SURFACE, relief="flat", borderwidth=0)
        self.style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.style.configure("Card.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT, font=("Segoe UI", 10))
        self.style.configure("Muted.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 9))
        self.style.configure("Section.TLabel", background=COLOR_SURFACE, foreground=COLOR_TEXT, font=("Segoe UI", 11, "bold"))
        self.style.configure("Title.TLabel", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 16, "bold"))
        self.style.configure("Subtitle.TLabel", background=COLOR_BG, foreground=COLOR_TEXT_MUTED, font=("Segoe UI", 10))

        # Pestañas modernas y limpias
        self.style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background="#e2e8f0",
            foreground=COLOR_TEXT_MUTED,
            padding=[16, 7],
            font=("Segoe UI", 9, "bold"),
            borderwidth=0
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", COLOR_SURFACE)],
            foreground=[("selected", COLOR_PRIMARY)]
        )

        # Radiobuttons y Checkbuttons
        self.style.configure("TRadiobutton", background=COLOR_SURFACE, foreground=COLOR_TEXT, font=("Segoe UI", 9))
        self.style.configure("TCheckbutton", background=COLOR_SURFACE, foreground=COLOR_TEXT, font=("Segoe UI", 9))

        # Botones secundarios sutiles
        self.style.configure(
            "Soft.TButton",
            font=("Segoe UI", 9),
            background=COLOR_SURFACE_ALT,
            foreground=COLOR_TEXT,
            borderwidth=0,
            padding=[10, 5]
        )
        self.style.map(
            "Soft.TButton",
            background=[("active", "#e2e8f0"), ("pressed", "#cbd5e1")]
        )

        # Botón de preset redondeado
        self.style.configure(
            "Preset.TButton",
            font=("Segoe UI", 9),
            background=COLOR_ACCENT_BG,
            foreground=COLOR_PRIMARY,
            borderwidth=0,
            padding=[8, 4]
        )
        self.style.map(
            "Preset.TButton",
            background=[("active", "#dbeafe"), ("pressed", "#bfdbfe")]
        )

    def build_layout(self):
        """Construye la distribución de la ventana."""
        # Barra superior / Encabezado
        header = ttk.Frame(self, padding=(24, 16, 24, 8))
        header.pack(fill=tk.X)

        title_box = ttk.Frame(header)
        title_box.pack(side=tk.LEFT)
        ttk.Label(title_box, text="Descomposición LU", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            title_box,
            text="Factorización A = L·U y P·A = L·U con cálculo analítico exacto y resolución de sistemas lineales",
            style="Subtitle.TLabel"
        ).pack(anchor="w")

        # Contenedor dividido en dos columnas (Izquierda: Controles / Derecha: Resultados)
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=(6, 16))

        left_panel = ttk.Frame(paned, padding=4)
        paned.add(left_panel, weight=5)

        right_panel = ttk.Frame(paned, padding=4)
        paned.add(right_panel, weight=6)

        # ==========================================
        # PANEL IZQUIERDO: Entrada y Parámetros
        # ==========================================
        left_card = tk.Frame(left_panel, bg=COLOR_SURFACE, bd=1, relief="solid", highlightthickness=0)
        left_card.configure(highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER)
        left_card.pack(fill=tk.BOTH, expand=True)

        # Cuaderno de pestañas de entrada
        self.input_tabs = ttk.Notebook(left_card)
        self.input_tabs.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 6))

        # Pestaña 1: Cuadrícula Visual
        self.tab_grid = ttk.Frame(self.input_tabs, style="Card.TFrame", padding=10)
        self.input_tabs.add(self.tab_grid, text="Cuadrícula Visual (N × N)")

        # Pestaña 2: Texto Plano
        self.tab_text = ttk.Frame(self.input_tabs, style="Card.TFrame", padding=10)
        self.input_tabs.add(self.tab_text, text="Texto Plano")

        self.setup_tab_grid()
        self.setup_tab_text()

        # Separador visual
        tk.Frame(left_card, bg=COLOR_BORDER, height=1).pack(fill=tk.X, padx=14, pady=6)

        # Panel de Opciones de Cálculo
        self.setup_options(left_card)

        # Panel de Acciones y Presets
        self.setup_actions(left_card)

        # ==========================================
        # PANEL DERECHO: Resultados y Análisis
        # ==========================================
        self.setup_results(right_panel)

    def setup_tab_grid(self):
        """Configuración de la cuadrícula interactiva N x N."""
        toolbar = ttk.Frame(self.tab_grid, style="Card.TFrame")
        toolbar.pack(fill=tk.X, pady=(0, 10))

        # Selector de tamaño
        ttk.Label(toolbar, text="Dimensión N:", style="Card.TLabel", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))

        btn_minus = tk.Button(
            toolbar, text="−", width=2, font=("Segoe UI", 10, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT, relief="flat", bd=0,
            activebackground="#e2e8f0", command=self.decrement_size
        )
        btn_minus.pack(side=tk.LEFT, padx=1)

        size_spin = ttk.Spinbox(
            toolbar, from_=2, to=8, textvariable=self.matrix_size, width=3,
            font=("Segoe UI", 10), justify="center", command=self.on_size_change
        )
        size_spin.pack(side=tk.LEFT, padx=2)
        size_spin.bind("<Return>", lambda e: self.on_size_change())

        btn_plus = tk.Button(
            toolbar, text="+", width=2, font=("Segoe UI", 10, "bold"),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT, relief="flat", bd=0,
            activebackground="#e2e8f0", command=self.increment_size
        )
        btn_plus.pack(side=tk.LEFT, padx=1)

        # Botones de utilidad
        btn_to_text = ttk.Button(toolbar, text="Copiar a Texto", style="Soft.TButton", command=self.sync_grid_to_text)
        btn_to_text.pack(side=tk.RIGHT, padx=3)

        btn_clear = ttk.Button(toolbar, text="Limpiar Celdas", style="Soft.TButton", command=self.clear_grid)
        btn_clear.pack(side=tk.RIGHT, padx=3)

        # Contenedor scrolleable
        container = ttk.Frame(self.tab_grid, style="Card.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        self.grid_canvas = tk.Canvas(container, bg=COLOR_SURFACE, highlightthickness=0)
        v_bar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.grid_canvas.yview)
        h_bar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.grid_canvas.xview)

        self.matrix_cells_frame = tk.Frame(self.grid_canvas, bg=COLOR_SURFACE)
        self.matrix_cells_frame.bind(
            "<Configure>",
            lambda e: self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all"))
        )
        self.grid_canvas.create_window((0, 0), window=self.matrix_cells_frame, anchor="nw")
        self.grid_canvas.configure(xscrollcommand=h_bar.set, yscrollcommand=v_bar.set)

        self.grid_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_bar.pack(side=tk.RIGHT, fill=tk.Y)
        h_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.render_matrix_grid()

    def setup_tab_text(self):
        """Configuración de la entrada en texto plano."""
        top_bar = ttk.Frame(self.tab_text, style="Card.TFrame")
        top_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(
            top_bar,
            text="Escribe o pega filas separadas por espacios, comas o saltos de línea:",
            style="Muted.TLabel"
        ).pack(side=tk.LEFT)

        btn_to_grid = ttk.Button(top_bar, text="Cargar en Cuadrícula", style="Soft.TButton", command=self.sync_text_to_grid)
        btn_to_grid.pack(side=tk.RIGHT)

        self.text_matrix_input = tk.Text(
            self.tab_text, wrap=tk.NONE, font=("Consolas", 11),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT, insertbackground=COLOR_PRIMARY,
            relief="flat", bd=0, padx=10, pady=10, height=8
        )
        self.text_matrix_input.pack(fill=tk.BOTH, expand=True, pady=(2, 8))

        # Vector b
        b_box = ttk.Frame(self.tab_text, style="Card.TFrame")
        b_box.pack(fill=tk.X)

        ttk.Label(b_box, text="Vector independiente b (opcional, ej. 4, 1, 1):", style="Muted.TLabel").pack(anchor="w")
        self.text_b_input = tk.Entry(
            b_box, font=("Consolas", 10), bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT,
            relief="flat", bd=0
        )
        self.text_b_input.pack(fill=tk.X, ipady=6, pady=(3, 0))

    def setup_options(self, parent):
        """Panel de configuración de métodos y formatos numéricos."""
        box = ttk.Frame(parent, style="Card.TFrame", padding=(14, 6))
        box.pack(fill=tk.X)

        # Fila Método
        r1 = ttk.Frame(box, style="Card.TFrame")
        r1.pack(fill=tk.X, pady=2)
        ttk.Label(r1, text="Método:", style="Card.TLabel", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Radiobutton(
            r1, text="Pivoteo Parcial (P·A = L·U)",
            variable=self.method_var, value="pivot"
        ).pack(side=tk.LEFT, padx=6)

        ttk.Radiobutton(
            r1, text="Doolittle Clásico (A = L·U)",
            variable=self.method_var, value="no_pivot"
        ).pack(side=tk.LEFT, padx=6)

        # Fila Formato
        r2 = ttk.Frame(box, style="Card.TFrame")
        r2.pack(fill=tk.X, pady=4)
        ttk.Label(r2, text="Formato:", style="Card.TLabel", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Radiobutton(
            r2, text="Fracciones exactas",
            variable=self.format_var, value="fraction"
        ).pack(side=tk.LEFT, padx=6)

        ttk.Radiobutton(
            r2, text="Decimales",
            variable=self.format_var, value="decimal"
        ).pack(side=tk.LEFT, padx=6)

        ttk.Label(r2, text="Decimales:", style="Muted.TLabel").pack(side=tk.LEFT, padx=(12, 4))
        ttk.Spinbox(r2, from_=1, to=8, textvariable=self.decimals_var, width=3, font=("Segoe UI", 9)).pack(side=tk.LEFT)

        # Fila Resolver Sistema
        r3 = ttk.Frame(box, style="Card.TFrame")
        r3.pack(fill=tk.X, pady=(3, 6))
        ttk.Checkbutton(
            r3, text="Resolver sistema lineal simultáneo (A · x = b)",
            variable=self.solve_system_var, command=self.render_matrix_grid
        ).pack(side=tk.LEFT)

    def setup_actions(self, parent):
        """Botón principal de cálculo y presets organizados."""
        box = ttk.Frame(parent, style="Card.TFrame", padding=(14, 6))
        box.pack(fill=tk.X, pady=(0, 10))

        # Botón principal con diseño limpio y ergonómico
        btn_calc = tk.Button(
            box,
            text="Calcular Descomposición LU",
            font=("Segoe UI", 11, "bold"),
            bg=COLOR_PRIMARY,
            fg="white",
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            command=self.calculate_lu
        )
        btn_calc.pack(fill=tk.X, pady=(0, 10))

        # Barra de Presets rápidos
        preset_bar = ttk.Frame(box, style="Card.TFrame")
        preset_bar.pack(fill=tk.X)

        ttk.Label(preset_bar, text="Casos de prueba:", style="Muted.TLabel", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))

        for p in PRESETS:
            btn = ttk.Button(
                preset_bar,
                text=f"{p.dimension}×{p.dimension} (Ej. {p.id})",
                style="Preset.TButton",
                command=lambda pid=p.id: self.load_preset(pid)
            )
            btn.pack(side=tk.LEFT, padx=3)

    def setup_results(self, parent):
        """Panel derecho para presentación de resultados numéricos y paso a paso."""
        card = tk.Frame(parent, bg=COLOR_SURFACE, bd=1, relief="solid", highlightthickness=0)
        card.configure(highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER)
        card.pack(fill=tk.BOTH, expand=True)

        # Cabecera de resultados
        top_bar = ttk.Frame(card, style="Card.TFrame", padding=(14, 12, 14, 6))
        top_bar.pack(fill=tk.X)

        ttk.Label(top_bar, text="Reporte de Solución", style="Section.TLabel").pack(side=tk.LEFT)

        btn_save = ttk.Button(top_bar, text="Guardar Reporte (.txt)", style="Soft.TButton", command=self.save_report)
        btn_save.pack(side=tk.RIGHT, padx=3)

        btn_copy = ttk.Button(top_bar, text="Copiar al Portapapeles", style="Soft.TButton", command=self.copy_results)
        btn_copy.pack(side=tk.RIGHT, padx=3)

        # Pestañas de resultados
        self.results_tabs = ttk.Notebook(card)
        self.results_tabs.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        # Tab 1: Matrices resultantes
        tab_mat = ttk.Frame(self.results_tabs, style="Card.TFrame", padding=6)
        self.results_tabs.add(tab_mat, text="Matrices (L, U, P y Comprobación)")

        self.text_matrices_out = tk.Text(
            tab_mat, wrap=tk.NONE, font=("Consolas", 10),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT, relief="flat", bd=0, padx=12, pady=12
        )
        sy1 = ttk.Scrollbar(tab_mat, orient=tk.VERTICAL, command=self.text_matrices_out.yview)
        sx1 = ttk.Scrollbar(tab_mat, orient=tk.HORIZONTAL, command=self.text_matrices_out.xview)
        self.text_matrices_out.configure(xscrollcommand=sx1.set, yscrollcommand=sy1.set)
        self.text_matrices_out.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sy1.pack(side=tk.RIGHT, fill=tk.Y)
        sx1.pack(side=tk.BOTTOM, fill=tk.X)

        # Tab 2: Paso a paso analítico
        tab_steps = ttk.Frame(self.results_tabs, style="Card.TFrame", padding=6)
        self.results_tabs.add(tab_steps, text="Desarrollo Paso a Paso")

        self.text_steps_out = tk.Text(
            tab_steps, wrap=tk.NONE, font=("Consolas", 10),
            bg=COLOR_SURFACE_ALT, fg=COLOR_TEXT, relief="flat", bd=0, padx=12, pady=12
        )
        sy2 = ttk.Scrollbar(tab_steps, orient=tk.VERTICAL, command=self.text_steps_out.yview)
        sx2 = ttk.Scrollbar(tab_steps, orient=tk.HORIZONTAL, command=self.text_steps_out.xview)
        self.text_steps_out.configure(xscrollcommand=sx2.set, yscrollcommand=sy2.set)
        self.text_steps_out.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sy2.pack(side=tk.RIGHT, fill=tk.Y)
        sx2.pack(side=tk.BOTTOM, fill=tk.X)

        # Barra inferior de estado
        status_frame = ttk.Frame(card, style="Card.TFrame", padding=(14, 4, 14, 10))
        status_frame.pack(fill=tk.X)
        self.status_bar = ttk.Label(status_frame, text="Listo para calcular.", style="Muted.TLabel")
        self.status_bar.pack(anchor="w")

    def on_size_change(self):
        try:
            n = int(self.matrix_size.get())
            n = max(2, min(n, 10))
            self.matrix_size.set(n)
        except Exception:
            self.matrix_size.set(3)
        self.render_matrix_grid()

    def increment_size(self):
        curr = self.matrix_size.get()
        if curr < 8:
            self.matrix_size.set(curr + 1)
            self.render_matrix_grid()

    def decrement_size(self):
        curr = self.matrix_size.get()
        if curr > 2:
            self.matrix_size.set(curr - 1)
            self.render_matrix_grid()

    def render_matrix_grid(self):
        """Genera dinámicamente las entradas de la matriz con buen espaciado y legibilidad."""
        for w in self.matrix_cells_frame.winfo_children():
            w.destroy()

        n = self.matrix_size.get()
        self.grid_entries = []
        self.b_entries = []

        # Encabezado
        lbl = tk.Label(
            self.matrix_cells_frame,
            text=f"Matriz A ({n} × {n})",
            bg=COLOR_SURFACE, fg=COLOR_TEXT, font=("Segoe UI", 9, "bold")
        )
        lbl.grid(row=0, column=0, columnspan=n, pady=(4, 8), sticky="w")

        # Celdas de la matriz
        for i in range(n):
            row = []
            for j in range(n):
                cell_box = tk.Frame(self.matrix_cells_frame, bg=COLOR_SURFACE, padx=3, pady=3)
                cell_box.grid(row=i + 1, column=j)

                e = tk.Entry(
                    cell_box,
                    width=7,
                    font=("Segoe UI", 10),
                    justify="center",
                    relief="flat",
                    bd=0,
                    bg=COLOR_SURFACE_ALT,
                    fg=COLOR_TEXT,
                    highlightthickness=1,
                    highlightbackground=COLOR_BORDER,
                    highlightcolor=COLOR_BORDER_FOCUS
                )
                e.pack(ipady=5, ipadx=4)

                # Navegación intuitiva con teclado
                e.bind("<Down>", lambda event, r=i, c=j: self.nav_grid(r + 1, c))
                e.bind("<Up>", lambda event, r=i, c=j: self.nav_grid(r - 1, c))
                e.bind("<Right>", lambda event, r=i, c=j: self.nav_grid(r, c + 1))
                e.bind("<Left>", lambda event, r=i, c=j: self.nav_grid(r, c - 1))
                e.bind("<Return>", lambda event: self.calculate_lu())
                row.append(e)
            self.grid_entries.append(row)

        # Columna vector b si está activo
        if self.solve_system_var.get():
            sep = tk.Label(self.matrix_cells_frame, text="│", bg=COLOR_SURFACE, fg=COLOR_BORDER, font=("Segoe UI", 14))
            sep.grid(row=0, column=n, rowspan=n + 2, padx=8)

            lbl_b = tk.Label(
                self.matrix_cells_frame,
                text="Vector b",
                bg=COLOR_SURFACE, fg=COLOR_TEXT, font=("Segoe UI", 9, "bold")
            )
            lbl_b.grid(row=0, column=n + 1, pady=(4, 8))

            for i in range(n):
                cell_box = tk.Frame(self.matrix_cells_frame, bg=COLOR_SURFACE, padx=3, pady=3)
                cell_box.grid(row=i + 1, column=n + 1)

                eb = tk.Entry(
                    cell_box,
                    width=7,
                    font=("Segoe UI", 10),
                    justify="center",
                    relief="flat",
                    bd=0,
                    bg=COLOR_ACCENT_BG,
                    fg=COLOR_PRIMARY,
                    highlightthickness=1,
                    highlightbackground=COLOR_BORDER,
                    highlightcolor=COLOR_BORDER_FOCUS
                )
                eb.pack(ipady=5, ipadx=4)
                eb.bind("<Return>", lambda event: self.calculate_lu())
                self.b_entries.append(eb)

    def nav_grid(self, r: int, c: int):
        n = self.matrix_size.get()
        if 0 <= r < n and 0 <= c < n:
            self.grid_entries[r][c].focus_set()

    def clear_grid(self):
        for row in self.grid_entries:
            for e in row:
                e.delete(0, tk.END)
        for eb in self.b_entries:
            eb.delete(0, tk.END)

    def sync_grid_to_text(self):
        """Exporta la cuadrícula a formato texto plano."""
        matrix = []
        n = self.matrix_size.get()
        for i in range(n):
            row = []
            for j in range(n):
                val = self.grid_entries[i][j].get().strip()
                row.append(val if val else "0")
            matrix.append("  ".join(row))
        self.text_matrix_input.delete("1.0", tk.END)
        self.text_matrix_input.insert("1.0", "\n".join(matrix))

        if self.solve_system_var.get() and self.b_entries:
            b_vals = [eb.get().strip() if eb.get().strip() else "0" for eb in self.b_entries]
            self.text_b_input.delete(0, tk.END)
            self.text_b_input.insert(0, ", ".join(b_vals))

        self.input_tabs.select(self.tab_text)

    def sync_text_to_grid(self):
        """Parsea el texto plano y llena la cuadrícula visual."""
        raw_text = self.text_matrix_input.get("1.0", tk.END).strip()
        if not raw_text:
            messagebox.showwarning("Atención", "El área de texto de la matriz está vacía.")
            return

        try:
            use_frac = (self.format_var.get() == "fraction")
            M = parse_matrix_text(raw_text, use_fractions=use_frac)
            n = len(M)
            if n > 10:
                messagebox.showerror("Error", "La cuadrícula visual soporta un máximo de 10×10.")
                return

            self.matrix_size.set(n)
            self.render_matrix_grid()

            for i in range(n):
                for j in range(n):
                    val_str = format_number(M[i][j], as_fraction=use_frac, decimals=self.decimals_var.get())
                    self.grid_entries[i][j].delete(0, tk.END)
                    self.grid_entries[i][j].insert(0, val_str)

            if self.solve_system_var.get():
                b_text = self.text_b_input.get().strip()
                if b_text:
                    try:
                        vec_b = parse_vector_text(b_text, expected_len=n, use_fractions=use_frac)
                        if vec_b and self.b_entries:
                            for i in range(n):
                                val_str = format_number(vec_b[i], as_fraction=use_frac, decimals=self.decimals_var.get())
                                self.b_entries[i].delete(0, tk.END)
                                self.b_entries[i].insert(0, val_str)
                    except Exception:
                        self.text_b_input.delete(0, tk.END)
                        for eb in self.b_entries:
                            eb.delete(0, tk.END)

            self.input_tabs.select(self.tab_grid)

        except Exception as e:
            messagebox.showerror("Error al parsear matriz", str(e))

    def load_preset(self, preset_id: int):
        """Carga una de las matrices preconfiguradas."""
        p = get_preset_by_id(preset_id)
        if not p:
            return

        self.matrix_size.set(p.dimension)
        self.method_var.set(p.recommended_method)
        self.render_matrix_grid()

        for i in range(p.dimension):
            for j in range(p.dimension):
                self.grid_entries[i][j].delete(0, tk.END)
                self.grid_entries[i][j].insert(0, p.matrix_rows[i][j])

        if self.solve_system_var.get() and self.b_entries and p.vector_b:
            for i in range(p.dimension):
                self.b_entries[i].delete(0, tk.END)
                self.b_entries[i].insert(0, p.vector_b[i])

        self.text_matrix_input.delete("1.0", tk.END)
        self.text_matrix_input.insert("1.0", p.matrix_text)
        self.text_b_input.delete(0, tk.END)
        self.text_b_input.insert(0, p.b_text)

        self.status_bar.config(text=f"Cargado {p.title}: {p.description}")

    def get_current_data(self) -> Tuple[Matrix, Optional[Vector]]:
        """Extrae la matriz A y el vector b según la pestaña activa."""
        use_frac = (self.format_var.get() == "fraction")
        is_text_tab = (self.input_tabs.index(self.input_tabs.select()) == 1)

        if is_text_tab:
            raw = self.text_matrix_input.get("1.0", tk.END).strip()
            A = parse_matrix_text(raw, use_fractions=use_frac)
            b = None
            if self.solve_system_var.get():
                b_raw = self.text_b_input.get().strip()
                if b_raw:
                    b = parse_vector_text(b_raw, expected_len=len(A), use_fractions=use_frac)
            return A, b
        else:
            n = self.matrix_size.get()
            matrix: Matrix = []
            for i in range(n):
                row = []
                for j in range(n):
                    val = self.grid_entries[i][j].get().strip()
                    if not val:
                        raise ValueError(f"La casilla ({i + 1}, {j + 1}) está vacía.")
                    row.append(Fraction(val) if use_frac else float(val))
                matrix.append(row)

            b = None
            if self.solve_system_var.get() and self.b_entries:
                b_vals: Vector = []
                for i in range(n):
                    val = self.b_entries[i].get().strip()
                    if not val:
                        raise ValueError(f"El elemento b_{i + 1} está vacío.")
                    b_vals.append(Fraction(val) if use_frac else float(val))
                b = b_vals
            return matrix, b

    def calculate_lu(self):
        """Ejecuta la descomposición y actualiza los paneles de salida."""
        try:
            A, b = self.get_current_data()
            n = len(A)
            use_frac = (self.format_var.get() == "fraction")
            decimals = self.decimals_var.get()
            method = self.method_var.get()

            res: LUResult = lu_doolittle_no_pivot(A) if method == "no_pivot" else lu_doolittle_pivot(A)

            res_sys: Optional[SystemSolution] = None
            if b is not None:
                res_sys = solve_system_lu(res.P, res.L, res.U, b)

            # Generar reporte de matrices
            report = build_full_report(A, res, b, res_sys, as_fraction=use_frac, decimals=decimals)
            self.text_matrices_out.delete("1.0", tk.END)
            self.text_matrices_out.insert("1.0", report)

            # Generar paso a paso
            step_text = res.steps
            if res_sys is not None:
                step_text += "\n\n" + res_sys.steps
            self.text_steps_out.delete("1.0", tk.END)
            self.text_steps_out.insert("1.0", step_text)

            self.status_bar.config(text=f"Cálculo completado con éxito para matriz {n}×{n} ({res.method_name}).")

        except ZeroDivisionError as zde:
            messagebox.showerror("Pivote Cero Encontrado", str(zde))
            self.status_bar.config(text="División entre cero: activa pivoteo parcial para continuar.")
        except Exception as ex:
            messagebox.showerror("Error de Cálculo", str(ex))
            self.status_bar.config(text=f"Error: {str(ex)}")

    def copy_results(self):
        idx = self.results_tabs.index(self.results_tabs.select())
        content = self.text_matrices_out.get("1.0", tk.END).strip() if idx == 0 else self.text_steps_out.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("Información", "No hay resultados para copiar.")
            return

        self.clipboard_clear()
        self.clipboard_append(content)
        self.status_bar.config(text="Copiado al portapapeles.")

    def save_report(self):
        mat_text = self.text_matrices_out.get("1.0", tk.END).strip()
        step_text = self.text_steps_out.get("1.0", tk.END).strip()
        if not mat_text:
            messagebox.showinfo("Información", "No hay resultados para guardar.")
            return

        full = mat_text + "\n\n" + ("=" * 65) + "\n PROCEDIMIENTO DETALLADO\n" + ("=" * 65) + "\n\n" + step_text
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")],
            title="Guardar Reporte LU"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(full)
                messagebox.showinfo("Guardado", f"Reporte guardado en:\n{path}")
            except Exception as e:
                messagebox.showerror("Error al guardar", str(e))


def main():
    app = LUApp()
    app.mainloop()


if __name__ == "__main__":
    main()
