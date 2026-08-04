"""
JUFE Six-Component Cell Analyzer
================================

Purpose
-------
Test the provisional 64-cell mapping contract:

    one cell = (Mx, My, Mz, Ax, Ay, Az)
    one frame = 64 cells
    one full frame = 384 values

This tool does not edit any JUFE source file.

Input interpretation
--------------------
- Commas and whitespace both separate numerical values.
- Original numerical order is preserved.
- Values are grouped sequentially into blocks of six.
- Every block of six becomes one local field cell.
- Incomplete trailing values are reported, never discarded.
- More than 64 cells creates additional frames.

Diagnostics
-----------
For each cell:
- M = first three values
- A = next three values
- scalar total
- component balance M + A
- phase residual ||M - A||

For each frame:
- populated cells
- scalar global balance
- component global balance
- phase-lock count
"""

from __future__ import annotations

import json
import math
import re
import tkinter as tk
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext
from typing import Any

import numpy as np


COMPONENTS_PER_CELL = 6
CELLS_PER_FRAME = 64
VALUES_PER_FRAME = COMPONENTS_PER_CELL * CELLS_PER_FRAME


@dataclass
class FieldCell:
    global_cell_index: int
    frame_index: int
    cell_index_in_frame: int
    row: int
    column: int
    M: list[float]
    A: list[float]
    scalar_total: float
    component_total: list[float]
    phase_residual: float
    phase_locked: bool


@dataclass
class FrameSummary:
    frame_index: int
    populated_cells: int
    scalar_global_balance: float
    component_global_balance: list[float]
    phase_locked_cells: int


def display_number(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else str(value)


def parse_values(raw_text: str) -> list[float]:
    tokens = [part for part in re.split(r"[\s,]+", raw_text.strip()) if part]

    if not tokens:
        raise ValueError("Enter at least one number.")

    values: list[float] = []

    for index, token in enumerate(tokens, start=1):
        try:
            value = float(token)
        except ValueError as exc:
            raise ValueError(
                f"Value {index} ('{token}') is not a valid number."
            ) from exc

        if not np.isfinite(value):
            raise ValueError(f"Value {index} is not finite.")

        values.append(value)

    return values


def build_cells(
    values: list[float],
    *,
    phase_lock_tolerance: float = 1e-9,
) -> tuple[list[FieldCell], list[float]]:
    complete_count = len(values) // COMPONENTS_PER_CELL
    trailing = values[complete_count * COMPONENTS_PER_CELL:]
    cells: list[FieldCell] = []

    for global_index in range(complete_count):
        start = global_index * COMPONENTS_PER_CELL
        block = values[start:start + COMPONENTS_PER_CELL]

        M = np.asarray(block[:3], dtype=float)
        A = np.asarray(block[3:], dtype=float)

        frame_index = global_index // CELLS_PER_FRAME
        cell_index = global_index % CELLS_PER_FRAME
        row = cell_index // 8
        column = cell_index % 8

        component_total = M + A
        scalar_total = float(np.sum(component_total))
        phase_residual = float(np.linalg.norm(M - A))

        cells.append(
            FieldCell(
                global_cell_index=global_index,
                frame_index=frame_index,
                cell_index_in_frame=cell_index,
                row=row,
                column=column,
                M=M.tolist(),
                A=A.tolist(),
                scalar_total=scalar_total,
                component_total=component_total.tolist(),
                phase_residual=phase_residual,
                phase_locked=bool(phase_residual <= phase_lock_tolerance),
            )
        )

    return cells, trailing


def summarize_frames(cells: list[FieldCell]) -> list[FrameSummary]:
    if not cells:
        return []

    frame_count = max(cell.frame_index for cell in cells) + 1
    summaries: list[FrameSummary] = []

    for frame_index in range(frame_count):
        frame_cells = [
            cell for cell in cells
            if cell.frame_index == frame_index
        ]

        scalar_total = float(sum(cell.scalar_total for cell in frame_cells))
        component_total = np.sum(
            np.asarray([cell.component_total for cell in frame_cells], dtype=float),
            axis=0,
        )

        summaries.append(
            FrameSummary(
                frame_index=frame_index,
                populated_cells=len(frame_cells),
                scalar_global_balance=scalar_total,
                component_global_balance=component_total.tolist(),
                phase_locked_cells=sum(cell.phase_locked for cell in frame_cells),
            )
        )

    return summaries


def analyse(
    raw_text: str,
    *,
    phase_lock_tolerance: float = 1e-9,
) -> dict[str, Any]:
    values = parse_values(raw_text)
    cells, trailing = build_cells(
        values,
        phase_lock_tolerance=phase_lock_tolerance,
    )
    frames = summarize_frames(cells)

    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "mapping_version": "six_component_cell_v0.1",
        "total_values": len(values),
        "complete_cells": len(cells),
        "complete_frames": len(cells) // CELLS_PER_FRAME,
        "partial_frame_cells": len(cells) % CELLS_PER_FRAME,
        "trailing_values": trailing,
        "phase_lock_tolerance": phase_lock_tolerance,
        "cells": [asdict(cell) for cell in cells],
        "frames": [asdict(frame) for frame in frames],
    }


def format_report(result: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.extend([
        "JUFE SIX-COMPONENT CELL ANALYSIS",
        "=" * 76,
        f"Mapping version      : {result['mapping_version']}",
        f"Total source values  : {result['total_values']}",
        f"Complete cells       : {result['complete_cells']}",
        f"Complete 64-cell frames: {result['complete_frames']}",
        f"Cells in partial frame : {result['partial_frame_cells']}",
        f"Trailing values      : {len(result['trailing_values'])}",
        "",
    ])

    if result["trailing_values"]:
        lines.extend([
            "INCOMPLETE TRAILING CELL",
            "-" * 76,
            "These values were preserved but could not form a complete six-component cell:",
            ", ".join(display_number(value) for value in result["trailing_values"]),
            "",
        ])

    lines.extend([
        "CELL STATES",
        "-" * 76,
    ])

    for cell in result["cells"]:
        lines.append(
            f"Frame {cell['frame_index'] + 1}, "
            f"Cell {cell['cell_index_in_frame'] + 1} "
            f"({cell['row']},{cell['column']})"
        )
        lines.append(
            "  M = [" +
            ", ".join(display_number(v) for v in cell["M"]) +
            "]"
        )
        lines.append(
            "  A = [" +
            ", ".join(display_number(v) for v in cell["A"]) +
            "]"
        )
        lines.append(
            "  M + A = [" +
            ", ".join(display_number(v) for v in cell["component_total"]) +
            "]"
        )
        lines.append(
            f"  Scalar total  = {display_number(cell['scalar_total'])}"
        )
        lines.append(
            f"  Phase residual = {cell['phase_residual']:.12g}"
        )
        lines.append(
            f"  Phase locked   = {cell['phase_locked']}"
        )
        lines.append("")

    lines.extend([
        "FRAME SUMMARIES",
        "-" * 76,
    ])

    for frame in result["frames"]:
        lines.append(f"FRAME {frame['frame_index'] + 1}")
        lines.append(
            f"  Populated cells        : {frame['populated_cells']}"
        )
        lines.append(
            f"  Scalar global balance  : "
            f"{display_number(frame['scalar_global_balance'])}"
        )
        lines.append(
            "  Component global balance: [" +
            ", ".join(
                display_number(v)
                for v in frame["component_global_balance"]
            ) +
            "]"
        )
        lines.append(
            f"  Phase-locked cells     : {frame['phase_locked_cells']}"
        )
        lines.append(
            "  Scalar balanced        : "
            f"{math.isclose(frame['scalar_global_balance'], 0.0, abs_tol=1e-9)}"
        )
        lines.append(
            "  Component balanced     : "
            f"{np.linalg.norm(frame['component_global_balance']) <= 1e-9}"
        )
        lines.append("")

    return "\n".join(lines)


class CellAnalyzerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.last_result: dict[str, Any] | None = None

        root.title("JUFE Six-Component Cell Analyzer")
        root.geometry("1000x850")
        root.minsize(800, 650)

        tk.Label(
            root,
            text="JUFE Six-Component Cell Analyzer",
            font=("Arial", 18, "bold"),
        ).pack(pady=(14, 5))

        tk.Label(
            root,
            text=(
                "Six sequential values form one cell: "
                "Mx, My, Mz, Ax, Ay, Az. "
                "Sixty-four cells form one frame."
            ),
            font=("Arial", 11),
            justify="center",
        ).pack(pady=(0, 10))

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=18)

        tk.Label(
            main,
            text="Input values:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x")

        self.input_box = scrolledtext.ScrolledText(
            main,
            height=13,
            wrap=tk.WORD,
            font=("Courier New", 11),
        )
        self.input_box.pack(fill="both", expand=True, pady=(5, 8))

        controls = tk.Frame(main)
        controls.pack(pady=5)

        tk.Button(
            controls,
            text="Analyse Six-Component Cells",
            command=self.run,
            width=25,
            font=("Arial", 11, "bold"),
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Save Audit JSON",
            command=self.save,
            width=16,
            font=("Arial", 11),
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Clear",
            command=self.clear,
            width=10,
            font=("Arial", 11),
        ).pack(side="left", padx=5)

        tk.Label(
            main,
            text="Report:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

        self.output_box = scrolledtext.ScrolledText(
            main,
            height=30,
            wrap=tk.NONE,
            font=("Courier New", 10),
            state="disabled",
        )
        self.output_box.pack(fill="both", expand=True, pady=(5, 12))

        self.input_box.focus_set()

    def run(self) -> None:
        raw_text = self.input_box.get("1.0", tk.END).strip()

        try:
            result = analyse(raw_text)
            report = format_report(result)
        except Exception as exc:
            messagebox.showerror("Cell analysis error", str(exc))
            return

        self.last_result = result
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, report)
        self.output_box.config(state="disabled")

    def save(self) -> None:
        if self.last_result is None:
            messagebox.showwarning(
                "No analysis",
                "Run the analysis before saving.",
            )
            return

        destination = filedialog.asksaveasfilename(
            title="Save six-component cell audit",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="jufe_six_component_cell_audit.json",
        )

        if not destination:
            return

        Path(destination).write_text(
            json.dumps(self.last_result, indent=2),
            encoding="utf-8",
        )

        messagebox.showinfo("Audit saved", f"Saved to:\n{destination}")

    def clear(self) -> None:
        self.last_result = None
        self.input_box.delete("1.0", tk.END)
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")
        self.input_box.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    CellAnalyzerApp(root)
    root.mainloop()
