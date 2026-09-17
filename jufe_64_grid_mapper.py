"""
JUFE 64-Grid Mapper
===================

Separate 8 x 8 grid preparation and validation tool.

This file does not edit:
- oldmate1(5).py
- oldmate2(4).py
- abtm_expansion.py

Supported mapping modes
-----------------------
1. Individual values:
   Every numerical value is placed into the 8 x 8 grid in original sequence
   order, row by row.

2. Subgroup totals:
   Every whitespace-separated subgroup is summed first, then each subgroup
   total is placed into the 8 x 8 grid in original subgroup order, row by row.

No multiplication rule is invented here. The tool only performs explicit
mapping, trace calculation, modulo-6 validation, and auditing.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import tkinter as tk
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from types import ModuleType
from typing import Any

import numpy as np

from abtm_expansion import ABTM_Expansion


GRID_SIZE = 8
GRID_CELLS = GRID_SIZE * GRID_SIZE


@dataclass
class SourceGroup:
    set_index: int
    group_index: int
    values: list[float]
    total: float


@dataclass
class GridResult:
    mode: str
    source_item_count: int
    used_count: int
    empty_cells: int
    overflow_count: int
    overflow_values: list[float]
    grid: list[list[float]]
    diagonal_values: list[float]
    trace: float
    trace_mod_6: float
    stable: bool


def display_number(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else str(value)


def parse_number(token: str) -> float:
    token = token.strip()
    if not token:
        raise ValueError("Empty number found.")

    value = float(token)
    if not np.isfinite(value):
        raise ValueError(f"Non-finite number found: {token}")

    return value


def parse_source(raw_text: str) -> tuple[list[list[float]], list[SourceGroup]]:
    all_values: list[list[float]] = []
    groups: list[SourceGroup] = []

    for set_index, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        group_tokens = [part for part in re.split(r"\s+", line) if part]

        for group_index, group_text in enumerate(group_tokens, start=1):
            tokens = [token for token in group_text.split(",") if token.strip()]

            if not tokens:
                raise ValueError(
                    f"Set {set_index}, group {group_index} contains no values."
                )

            values = [parse_number(token) for token in tokens]
            all_values.append(values)
            groups.append(
                SourceGroup(
                    set_index=set_index,
                    group_index=group_index,
                    values=values,
                    total=float(sum(values)),
                )
            )

    if not groups:
        raise ValueError("Enter at least one set.")

    return all_values, groups


def flatten_individual_values(groups: list[SourceGroup]) -> list[float]:
    return [
        value
        for group in groups
        for value in group.values
    ]


def flatten_group_totals(groups: list[SourceGroup]) -> list[float]:
    return [group.total for group in groups]


def map_to_grid(
    source_values: list[float],
    *,
    fill_value: float = 0.0,
) -> tuple[np.ndarray, list[float]]:
    used = source_values[:GRID_CELLS]
    overflow = source_values[GRID_CELLS:]

    padded = used + [float(fill_value)] * (GRID_CELLS - len(used))
    grid = np.asarray(padded, dtype=float).reshape(GRID_SIZE, GRID_SIZE)

    return grid, overflow


def find_original(folder: Path, stem: str) -> Path:
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
            f"Could not find {stem}. Put this mapper in the same folder "
            f"as both original Python files."
        )

    return matches[0]


def load_oldmate1(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("jufe_oldmate1_original", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path.name}")

    module = importlib.util.module_from_spec(spec)
    module.ABTM_Expansion = ABTM_Expansion
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def analyse_grid(raw_text: str, mode: str) -> tuple[GridResult, list[SourceGroup]]:
    _, groups = parse_source(raw_text)

    if mode == "Individual values":
        source_values = flatten_individual_values(groups)
    elif mode == "Subgroup totals":
        source_values = flatten_group_totals(groups)
    else:
        raise ValueError("Unknown mapping mode.")

    grid, overflow = map_to_grid(source_values)

    folder = Path(__file__).resolve().parent
    oldmate1_path = find_original(folder, "oldmate1")
    oldmate1 = load_oldmate1(oldmate1_path)
    engine = oldmate1.ABTM_Engine()

    stable = bool(engine.compute_manifold_stability(grid))
    diagonal = [float(value) for value in np.diag(grid)]
    trace = float(np.trace(grid))
    residue = float(trace % 6)

    result = GridResult(
        mode=mode,
        source_item_count=len(source_values),
        used_count=min(len(source_values), GRID_CELLS),
        empty_cells=max(0, GRID_CELLS - len(source_values)),
        overflow_count=len(overflow),
        overflow_values=[float(value) for value in overflow],
        grid=grid.tolist(),
        diagonal_values=diagonal,
        trace=trace,
        trace_mod_6=residue,
        stable=stable,
    )

    return result, groups


def format_report(result: GridResult, groups: list[SourceGroup]) -> str:
    lines: list[str] = []

    lines.extend([
        "JUFE 64-GRID REPORT",
        "=" * 72,
        f"Mapping mode      : {result.mode}",
        f"Grid dimensions   : 8 x 8",
        f"Grid capacity     : 64 cells",
        f"Source items      : {result.source_item_count}",
        f"Items used        : {result.used_count}",
        f"Empty cells       : {result.empty_cells}",
        f"Overflow items    : {result.overflow_count}",
        "",
        "SOURCE GROUPS",
        "-" * 72,
    ])

    for group in groups:
        lines.append(
            f"Set {group.set_index}, group {group.group_index}: "
            f"values={group.values}, total={display_number(group.total)}"
        )

    lines.extend([
        "",
        "8 x 8 GRID",
        "-" * 72,
    ])

    for row in result.grid:
        lines.append(
            "[" + ", ".join(display_number(value) for value in row) + "]"
        )

    lines.extend([
        "",
        "DIAGONAL / ORIGINAL ENGINE",
        "-" * 72,
        (
            "Diagonal values : "
            + ", ".join(display_number(value) for value in result.diagonal_values)
        ),
        f"Trace           : {display_number(result.trace)}",
        f"Trace mod 6     : {display_number(result.trace_mod_6)}",
        f"Original stable : {result.stable}",
    ])

    if result.overflow_count:
        lines.extend([
            "",
            "OVERFLOW",
            "-" * 72,
            (
                "The following values were not placed because the grid has "
                "only 64 cells:"
            ),
            ", ".join(display_number(value) for value in result.overflow_values),
        ])

    return "\n".join(lines)


def build_audit(
    raw_text: str,
    result: GridResult,
    groups: list[SourceGroup],
) -> dict[str, Any]:
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "raw_input": raw_text,
        "mapping_rules": {
            "line_break": "separate set",
            "space": "separate subgroup",
            "comma": "separate values within subgroup",
            "grid": "8 x 8 row-major",
            "empty_cells": "filled with zero",
            "overflow": "reported and not silently discarded",
        },
        "groups": [asdict(group) for group in groups],
        "grid_result": asdict(result),
    }


class GridMapperApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.audit_record: dict[str, Any] | None = None

        root.title("JUFE 64-Grid Mapper")
        root.geometry("1040x860")
        root.minsize(820, 650)

        tk.Label(
            root,
            text="JUFE 64-Grid Mapper",
            font=("Arial", 18, "bold"),
        ).pack(pady=(14, 5))

        tk.Label(
            root,
            text=(
                "Maps your input into a fixed 8 x 8 grid without changing "
                "the original source values."
            ),
            font=("Arial", 11),
            justify="center",
        ).pack(pady=(0, 10))

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=18)

        tk.Label(
            main,
            text="Input sequences:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x")

        self.input_box = scrolledtext.ScrolledText(
            main,
            height=12,
            wrap=tk.WORD,
            font=("Courier New", 11),
        )
        self.input_box.pack(fill="both", expand=True, pady=(5, 8))

        controls = tk.Frame(main)
        controls.pack(pady=5)

        tk.Label(
            controls,
            text="Mapping mode:",
            font=("Arial", 11, "bold"),
        ).pack(side="left", padx=(0, 5))

        self.mode_var = tk.StringVar(value="Individual values")
        self.mode_combo = ttk.Combobox(
            controls,
            textvariable=self.mode_var,
            values=["Individual values", "Subgroup totals"],
            state="readonly",
            width=20,
            font=("Arial", 11),
        )
        self.mode_combo.pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Map and Run",
            command=self.run,
            width=16,
            font=("Arial", 11, "bold"),
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Load Example",
            command=self.load_example,
            width=14,
            font=("Arial", 11),
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Save Audit",
            command=self.save_audit,
            width=12,
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
            text="64-grid report:",
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
        mode = self.mode_var.get()

        try:
            result, groups = analyse_grid(raw_text, mode)
            report = format_report(result, groups)
            self.audit_record = build_audit(raw_text, result, groups)
        except Exception as exc:
            messagebox.showerror("64-grid error", str(exc))
            return

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, report)
        self.output_box.config(state="disabled")

    def save_audit(self) -> None:
        if self.audit_record is None:
            messagebox.showwarning(
                "No report",
                "Run the 64-grid analysis before saving.",
            )
            return

        destination = filedialog.asksaveasfilename(
            title="Save JUFE 64-grid audit",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="jufe_64_grid_audit.json",
        )

        if not destination:
            return

        Path(destination).write_text(
            json.dumps(self.audit_record, indent=2),
            encoding="utf-8",
        )

        messagebox.showinfo(
            "Audit saved",
            f"Saved to:\n{destination}",
        )

    def load_example(self) -> None:
        example = (
            "1,4,1,40 1,50,4 5,400,5\n"
            "7,1,90,4,5,50 60,6 5,4,5,50"
        )
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, example)
        self.input_box.focus_set()

    def clear(self) -> None:
        self.audit_record = None
        self.input_box.delete("1.0", tk.END)
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")
        self.input_box.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    GridMapperApp(root)
    root.mainloop()
