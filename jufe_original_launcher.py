"""
JUFE launcher.

This file does not edit either original source file. It loads both files at
runtime and provides the missing ABTM_Expansion name externally so that
oldmate1 can be evaluated exactly as written.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext
from types import ModuleType
from typing import Iterable

import numpy as np


from abtm_expansion import ABTM_Expansion




def find_original(folder: Path, stem: str) -> Path:
    """Locate an original file without changing it."""
    preferred_names = {
        "oldmate1": ["oldmate1(5).py", "oldmate1(4).py", "oldmate1.py"],
        "oldmate2": ["oldmate2(4).py", "oldmate2(3).py", "oldmate2.py"],
    }

    for name in preferred_names[stem]:
        candidate = folder / name
        if candidate.is_file():
            return candidate

    matches = sorted(folder.glob(f"{stem}*.py"))
    matches = [path for path in matches if path.name != Path(__file__).name]

    if not matches:
        raise FileNotFoundError(
            f"Could not find {stem}. Put this launcher in the same folder "
            f"as both original Python files."
        )

    return matches[0]


def load_oldmate1(path: Path) -> ModuleType:
    """
    Load oldmate1 unchanged while supplying its unresolved base-class name
    through the module namespace.
    """
    spec = importlib.util.spec_from_file_location("jufe_oldmate1_original", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path.name}")

    module = importlib.util.module_from_spec(spec)
    module.ABTM_Expansion = ABTM_Expansion
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_normal_module(path: Path, module_name: str) -> ModuleType:
    """Load a Python file without editing it."""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path.name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_matrix(text: str) -> np.ndarray:
    """
    Parse an explicitly arranged matrix.

    Each non-empty line is one row. Values in a row may be separated by
    commas or spaces. The launcher does not rearrange or infer sections.
    """
    rows: list[list[float]] = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        pieces = [part for part in re.split(r"[\s,]+", line) if part]

        try:
            row = [float(part) for part in pieces]
        except ValueError as exc:
            raise ValueError(
                f"Row {line_number} contains something that is not a number."
            ) from exc

        if not row:
            continue
        rows.append(row)

    if not rows:
        raise ValueError("Enter at least one matrix row.")

    width = len(rows[0])
    if any(len(row) != width for row in rows):
        lengths = ", ".join(str(len(row)) for row in rows)
        raise ValueError(
            "Every matrix row must contain the same number of values. "
            f"Current row lengths: {lengths}"
        )

    matrix = np.array(rows, dtype=float)

    if matrix.ndim != 2:
        raise ValueError("The input must form a two-dimensional matrix.")

    return matrix


def printable_number(value: float) -> int | float:
    value = float(value)
    return int(value) if value.is_integer() else value


def run_original_system(matrix_text: str, treatise_text: str = "") -> dict:
    """
    Load and run both originals.

    The stability decision is made by the original ABTM_Engine method in
    oldmate1. Both original JUFE_Kernel classes are also booted.
    """
    folder = Path(__file__).resolve().parent
    oldmate1_path = find_original(folder, "oldmate1")
    oldmate2_path = find_original(folder, "oldmate2")

    oldmate1 = load_oldmate1(oldmate1_path)
    oldmate2 = load_normal_module(oldmate2_path, "jufe_oldmate2_original")

    matrix = parse_matrix(matrix_text)
    engine = oldmate1.ABTM_Engine()

    # Calls the original method exactly as supplied.
    stable = bool(engine.compute_manifold_stability(matrix))

    trace_value = np.trace(matrix)
    sigma = trace_value % 6

    # Boot both original kernel variants. File 2 receives a JSON-safe engine
    # identifier because its original code stores the supplied value directly.
    kernel_1 = oldmate1.JUFE_Kernel(treatise_text, engine)
    kernel_2 = oldmate2.JUFE_Kernel(
        treatise_text,
        engine.__class__.__name__,
    )

    sealed_1 = kernel_1.execute_boot()
    sealed_2 = kernel_2.execute_boot()

    return {
        "oldmate1_file": oldmate1_path.name,
        "oldmate2_file": oldmate2_path.name,
        "shape": matrix.shape,
        "matrix": matrix,
        "trace": printable_number(trace_value),
        "sigma": printable_number(sigma),
        "stable": stable,
        "sealed_1": sealed_1,
        "sealed_2": sealed_2,
    }


class JUFEApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("JUFE Original-System Launcher")
        root.geometry("820x720")
        root.minsize(700, 600)

        tk.Label(
            root,
            text="JUFE Original-System Launcher",
            font=("Arial", 18, "bold"),
        ).pack(pady=(16, 5))

        tk.Label(
            root,
            text=(
                "Both original files remain untouched.\n"
                "Enter the matrix exactly as intended: one row per line."
            ),
            justify="center",
            font=("Arial", 11),
        ).pack(pady=(0, 12))

        matrix_frame = tk.Frame(root)
        matrix_frame.pack(fill="both", expand=True, padx=20)

        tk.Label(
            matrix_frame,
            text="ψ barrier matrix:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x")

        self.matrix_box = scrolledtext.ScrolledText(
            matrix_frame,
            height=10,
            wrap=tk.NONE,
            font=("Courier New", 12),
        )
        self.matrix_box.pack(fill="both", expand=True, pady=(5, 10))

        tk.Label(
            matrix_frame,
            text=(
                "Example 2 × 2 arrangement:\n"
                "1, 4\n"
                "1, 40"
            ),
            justify="left",
            anchor="w",
            font=("Arial", 10),
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            matrix_frame,
            text="Treatise/specification text (optional):",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x")

        self.treatise_box = scrolledtext.ScrolledText(
            matrix_frame,
            height=5,
            wrap=tk.WORD,
            font=("Arial", 10),
        )
        self.treatise_box.pack(fill="both", expand=True, pady=(5, 10))

        controls = tk.Frame(root)
        controls.pack(pady=4)

        tk.Button(
            controls,
            text="Run Original System",
            command=self.run,
            width=20,
            font=("Arial", 11, "bold"),
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Clear",
            command=self.clear,
            width=10,
            font=("Arial", 11),
        ).pack(side="left", padx=5)

        results_frame = tk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(10, 18))

        tk.Label(
            results_frame,
            text="Results:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x")

        self.results = scrolledtext.ScrolledText(
            results_frame,
            height=12,
            wrap=tk.WORD,
            font=("Courier New", 10),
            state="disabled",
        )
        self.results.pack(fill="both", expand=True, pady=(5, 0))

        self.matrix_box.focus_set()

    def run(self) -> None:
        matrix_text = self.matrix_box.get("1.0", tk.END).strip()
        treatise_text = self.treatise_box.get("1.0", tk.END).strip()

        try:
            result = run_original_system(matrix_text, treatise_text)
        except Exception as exc:
            messagebox.showerror("JUFE could not run", str(exc))
            return

        rows = [
            f"Loaded file 1 : {result['oldmate1_file']}",
            f"Loaded file 2 : {result['oldmate2_file']}",
            f"Matrix shape  : {result['shape'][0]} × {result['shape'][1]}",
            "",
            "Matrix:",
            np.array2string(result["matrix"]),
            "",
            f"Trace         : {result['trace']}",
            f"Trace mod 6   : {result['sigma']}",
            f"Stable        : {result['stable']}",
            "",
            f"Kernel 1 boot : completed ({len(result['sealed_1'])} encoded bytes)",
            f"Kernel 2 boot : completed ({len(result['sealed_2'])} encoded bytes)",
        ]

        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, "\n".join(rows))
        self.results.config(state="disabled")

    def clear(self) -> None:
        self.matrix_box.delete("1.0", tk.END)
        self.treatise_box.delete("1.0", tk.END)
        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.config(state="disabled")
        self.matrix_box.focus_set()


if __name__ == "__main__":
    app_root = tk.Tk()
    JUFEApp(app_root)
    app_root.mainloop()
