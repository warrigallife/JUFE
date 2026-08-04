"""
JUFE / ABTM Master Flow Launcher
================================

This file links the full workflow without editing the core files:

- oldmate1(5).py
- oldmate2(4).py
- abtm_expansion.py

Signal flow
-----------
Raw user sequences
    -> parse into sets and subgroups
    -> calculate subgroup totals
    -> search all diagonal arrangements
    -> select the first stable arrangement (trace mod 6 == 0)
    -> run that arranged matrix through the original ABTM_Engine
    -> run the ABTM expansion diagnostics that are applicable
    -> display a complete report
    -> optionally save a JSON audit record

Input format
------------
Each non-empty line is one set.
Spaces separate subgroups.
Commas separate values inside each subgroup.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import re
import sys
import tkinter as tk
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext
from types import ModuleType
from typing import Any

import numpy as np

from abtm_expansion import ABTM_Expansion


@dataclass
class ParsedSet:
    set_index: int
    groups: list[list[float]]
    group_totals: list[float]
    set_total: float
    mod7: float


@dataclass
class ArrangementResult:
    selected_group_indices: list[int]
    selected_group_totals: list[float]
    arranged_matrix: list[list[float]]
    trace: float
    trace_mod_6: float
    stable: bool


def display_number(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else str(value)


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
            f"Could not find {stem}. Put this launcher in the same folder "
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


def load_normal_module(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {path.name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_number(token: str) -> float:
    token = token.strip()
    if not token:
        raise ValueError("Empty number found.")

    value = float(token)

    if not np.isfinite(value):
        raise ValueError(f"Non-finite value found: {token}")

    return value


def parse_sets(raw_text: str) -> list[ParsedSet]:
    parsed_sets: list[ParsedSet] = []

    for set_index, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()

        if not line:
            continue

        group_tokens = [part for part in re.split(r"\s+", line) if part]
        groups: list[list[float]] = []

        for group_index, group_text in enumerate(group_tokens, start=1):
            value_tokens = [
                token for token in group_text.split(",")
                if token.strip()
            ]

            if not value_tokens:
                raise ValueError(
                    f"Set {set_index}, group {group_index} has no values."
                )

            groups.append([
                parse_number(token)
                for token in value_tokens
            ])

        group_totals = [float(sum(group)) for group in groups]
        set_total = float(sum(group_totals))

        parsed_sets.append(
            ParsedSet(
                set_index=set_index,
                groups=groups,
                group_totals=group_totals,
                set_total=set_total,
                mod7=float(set_total % 7),
            )
        )

    if not parsed_sets:
        raise ValueError("Enter at least one set.")

    return parsed_sets


def arrange_row(
    totals: list[float],
    selected_index: int,
    diagonal_column: int,
    width: int,
) -> list[float]:
    selected = totals[selected_index]

    remaining = [
        value
        for index, value in enumerate(totals)
        if index != selected_index
    ]

    row: list[float | None] = [None] * width
    row[diagonal_column] = selected

    remaining_iter = iter(remaining)

    for column in range(width):
        if row[column] is None:
            row[column] = next(remaining_iter, 0.0)

    return [float(value) for value in row]


def search_arrangements(
    parsed_sets: list[ParsedSet],
) -> tuple[list[ArrangementResult], int]:
    set_count = len(parsed_sets)
    width = max(
        set_count,
        max(len(item.group_totals) for item in parsed_sets),
    )

    choice_ranges = [
        range(len(item.group_totals))
        for item in parsed_sets
    ]

    passing_results: list[ArrangementResult] = []
    tested = 0

    for selected_indices in itertools.product(*choice_ranges):
        tested += 1
        rows: list[list[float]] = []
        selected_totals: list[float] = []

        for row_index, (item, selected_index) in enumerate(
            zip(parsed_sets, selected_indices)
        ):
            selected_totals.append(item.group_totals[selected_index])
            rows.append(
                arrange_row(
                    item.group_totals,
                    selected_index,
                    row_index,
                    width,
                )
            )

        matrix = np.asarray(rows, dtype=float)
        trace = float(np.trace(matrix))
        residue = float(trace % 6)
        stable = bool(np.isclose(residue, 0.0))

        if stable:
            passing_results.append(
                ArrangementResult(
                    selected_group_indices=[
                        index + 1
                        for index in selected_indices
                    ],
                    selected_group_totals=selected_totals,
                    arranged_matrix=rows,
                    trace=trace,
                    trace_mod_6=residue,
                    stable=True,
                )
            )

    return passing_results, tested


def run_master_flow(
    raw_text: str,
    treatise_text: str = "",
) -> dict[str, Any]:
    folder = Path(__file__).resolve().parent

    oldmate1_path = find_original(folder, "oldmate1")
    oldmate2_path = find_original(folder, "oldmate2")

    oldmate1 = load_oldmate1(oldmate1_path)
    oldmate2 = load_normal_module(
        oldmate2_path,
        "jufe_oldmate2_original",
    )

    engine = oldmate1.ABTM_Engine()
    parsed_sets = parse_sets(raw_text)

    passing_arrangements, tested = search_arrangements(parsed_sets)

    selected_arrangement = (
        passing_arrangements[0]
        if passing_arrangements
        else None
    )

    original_engine_result = None
    arranged_matrix = None

    if selected_arrangement is not None:
        arranged_matrix = np.asarray(
            selected_arrangement.arranged_matrix,
            dtype=float,
        )

        original_engine_result = bool(
            engine.compute_manifold_stability(arranged_matrix)
        )

    combined_total = float(
        sum(item.set_total for item in parsed_sets)
    )
    combined_mod6 = float(combined_total % 6)

    pairwise = []

    for left_index in range(len(parsed_sets)):
        for right_index in range(left_index + 1, len(parsed_sets)):
            difference = abs(
                parsed_sets[left_index].set_total
                - parsed_sets[right_index].set_total
            )

            pairwise.append({
                "left": left_index + 1,
                "right": right_index + 1,
                "difference": float(difference),
                "difference_mod7": float(difference % 7),
                "aligned": bool(
                    np.isclose(difference % 7, 0.0)
                ),
            })

    all_mod7_balanced = all(
        np.isclose(item.mod7, 0.0)
        for item in parsed_sets
    )

    pairwise_aligned = all(
        item["aligned"]
        for item in pairwise
    ) if pairwise else True

    combined_z6_balanced = bool(
        np.isclose(combined_mod6, 0.0)
    )

    expansion_matrix_z6 = (
        engine.z6_stable(arranged_matrix)
        if arranged_matrix is not None
        else None
    )

    mod7_phases = [
        engine.mod7_phase(item.set_total)
        for item in parsed_sets
    ]

    kernel_1 = oldmate1.JUFE_Kernel(
        treatise_text,
        engine,
    )

    kernel_2 = oldmate2.JUFE_Kernel(
        treatise_text,
        engine.__class__.__name__,
    )

    sealed_1 = kernel_1.execute_boot()
    sealed_2 = kernel_2.execute_boot()

    overall_balanced = bool(
        selected_arrangement is not None
        and original_engine_result is True
        and all_mod7_balanced
        and combined_z6_balanced
        and pairwise_aligned
    )

    return {
        "raw_input": raw_text,
        "parsed_sets": parsed_sets,
        "arrangements_tested": tested,
        "passing_arrangements": passing_arrangements,
        "selected_arrangement": selected_arrangement,
        "original_engine_result": original_engine_result,
        "combined_total": combined_total,
        "combined_mod6": combined_mod6,
        "combined_z6_balanced": combined_z6_balanced,
        "all_mod7_balanced": all_mod7_balanced,
        "pairwise": pairwise,
        "pairwise_aligned": pairwise_aligned,
        "mod7_phases": mod7_phases,
        "expansion_matrix_z6": expansion_matrix_z6,
        "overall_balanced": overall_balanced,
        "oldmate1_file": oldmate1_path.name,
        "oldmate2_file": oldmate2_path.name,
        "sealed_1": sealed_1,
        "sealed_2": sealed_2,
    }


def build_audit_record(
    result: dict[str, Any],
) -> dict[str, Any]:
    selected = result["selected_arrangement"]

    return {
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "signal_flow": [
            "raw_input",
            "parse_sets",
            "calculate_group_totals",
            "search_trace_mod_6_arrangements",
            "select_first_passing_arrangement",
            "run_original_abtm_engine",
            "run_abtm_expansion_diagnostics",
            "report_results",
        ],
        "input_rules": {
            "line_break": "separate set",
            "space": "separate subgroup",
            "comma": "separate values within subgroup",
        },
        "raw_input": result["raw_input"],
        "sets": [
            asdict(item)
            for item in result["parsed_sets"]
        ],
        "arrangements_tested": result[
            "arrangements_tested"
        ],
        "passing_arrangements": [
            asdict(item)
            for item in result["passing_arrangements"]
        ],
        "selected_arrangement": (
            asdict(selected)
            if selected is not None
            else None
        ),
        "original_engine_result": result[
            "original_engine_result"
        ],
        "combined_total": result["combined_total"],
        "combined_mod6": result["combined_mod6"],
        "combined_z6_balanced": result[
            "combined_z6_balanced"
        ],
        "all_mod7_balanced": result[
            "all_mod7_balanced"
        ],
        "pairwise": result["pairwise"],
        "pairwise_aligned": result[
            "pairwise_aligned"
        ],
        "mod7_phases": result["mod7_phases"],
        "expansion_matrix_z6": result[
            "expansion_matrix_z6"
        ],
        "overall_balanced": result[
            "overall_balanced"
        ],
    }


def format_report(
    result: dict[str, Any],
) -> str:
    lines: list[str] = []

    lines.extend([
        "JUFE / ABTM MASTER FLOW REPORT",
        "=" * 68,
        f"Loaded file 1: {result['oldmate1_file']}",
        f"Loaded file 2: {result['oldmate2_file']}",
        "",
        "INPUT INTERPRETATION",
        "-" * 68,
        "Line break = separate set",
        "Space      = separate subgroup",
        "Comma      = separate value",
        "",
    ])

    for item in result["parsed_sets"]:
        lines.append(f"SET {item.set_index}")
        lines.append(
            "Group totals : "
            + ", ".join(
                display_number(value)
                for value in item.group_totals
            )
        )
        lines.append(
            f"Set total    : "
            f"{display_number(item.set_total)}"
        )
        lines.append(
            f"Set mod 7    : "
            f"{display_number(item.mod7)}"
        )
        lines.append(
            "Harmonic     : "
            + (
                "BALANCED"
                if np.isclose(item.mod7, 0.0)
                else "NOT BALANCED"
            )
        )
        lines.append("")

    lines.extend([
        "ARRANGEMENT STAGE",
        "-" * 68,
        (
            f"Arrangements tested : "
            f"{result['arrangements_tested']}"
        ),
        (
            f"Passing arrangements: "
            f"{len(result['passing_arrangements'])}"
        ),
        "",
    ])

    selected = result["selected_arrangement"]

    if selected is None:
        lines.extend([
            "No trace-mod-6 passing arrangement was found.",
            "",
            "ORIGINAL ENGINE",
            "-" * 68,
            "Original stable: NOT RUN",
            "",
        ])
    else:
        lines.append("Selected passing arrangement:")

        for set_index, (
            group_index,
            total,
        ) in enumerate(
            zip(
                selected.selected_group_indices,
                selected.selected_group_totals,
            ),
            start=1,
        ):
            lines.append(
                f"Set {set_index}: group {group_index}, "
                f"total {display_number(total)}"
            )

        lines.append("")
        lines.append("Arranged matrix:")

        for row in selected.arranged_matrix:
            lines.append(
                "["
                + ", ".join(
                    display_number(value)
                    for value in row
                )
                + "]"
            )

        lines.extend([
            "",
            (
                f"Trace       : "
                f"{display_number(selected.trace)}"
            ),
            (
                f"Trace mod 6 : "
                f"{display_number(selected.trace_mod_6)}"
            ),
            "",
            "ORIGINAL ENGINE",
            "-" * 68,
            (
                f"Original stable: "
                f"{result['original_engine_result']}"
            ),
            "",
        ])

    lines.extend([
        "ABTM EXPANSION",
        "-" * 68,
        (
            "Set mod-7 phases: "
            + ", ".join(
                display_number(value)
                for value in result["mod7_phases"]
            )
        ),
        (
            f"Combined total    : "
            f"{display_number(result['combined_total'])}"
        ),
        (
            f"Combined mod 6    : "
            f"{display_number(result['combined_mod6'])}"
        ),
        (
            "Combined Z6       : "
            + (
                "BALANCED"
                if result["combined_z6_balanced"]
                else "NOT BALANCED"
            )
        ),
        (
            f"Arranged matrix Z6: "
            f"{result['expansion_matrix_z6']}"
        ),
        "",
    ])

    if result["pairwise"]:
        lines.extend([
            "PAIRWISE COMPARISON",
            "-" * 68,
        ])

        for item in result["pairwise"]:
            lines.append(
                f"Set {item['left']} vs Set "
                f"{item['right']}"
            )
            lines.append(
                f"Difference      : "
                f"{display_number(item['difference'])}"
            )
            lines.append(
                f"Difference mod 7: "
                f"{display_number(item['difference_mod7'])}"
            )
            lines.append(
                "Aligned         : "
                + (
                    "TRUE"
                    if item["aligned"]
                    else "FALSE"
                )
            )
            lines.append("")

    lines.extend([
        "FINAL RESULT",
        "-" * 68,
        (
            "OVERALL ABTM BALANCE: "
            + (
                "TRUE"
                if result["overall_balanced"]
                else "FALSE"
            )
        ),
        "",
        (
            f"Kernel 1 boot: completed "
            f"({len(result['sealed_1'])} encoded bytes)"
        ),
        (
            f"Kernel 2 boot: completed "
            f"({len(result['sealed_2'])} encoded bytes)"
        ),
    ])

    return "\n".join(lines)


class MasterFlowApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.audit_record: dict[str, Any] | None = None

        root.title("JUFE / ABTM Master Flow")
        root.geometry("1020x860")
        root.minsize(800, 650)

        tk.Label(
            root,
            text="JUFE / ABTM Master Flow",
            font=("Arial", 18, "bold"),
        ).pack(pady=(14, 5))

        tk.Label(
            root,
            text=(
                "Paste once. The system parses, arranges, "
                "runs the original engine, applies ABTM diagnostics, "
                "and returns one report."
            ),
            justify="center",
            font=("Arial", 11),
        ).pack(pady=(0, 10))

        main = tk.Frame(root)
        main.pack(
            fill="both",
            expand=True,
            padx=18,
        )

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
        self.input_box.pack(
            fill="both",
            expand=True,
            pady=(5, 8),
        )

        controls = tk.Frame(main)
        controls.pack(pady=5)

        tk.Button(
            controls,
            text="Run Full ABTM Flow",
            command=self.run,
            width=22,
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
            text="Save Full Audit",
            command=self.save_audit,
            width=15,
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
            text="Full report:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(
            fill="x",
            pady=(8, 0),
        )

        self.output_box = scrolledtext.ScrolledText(
            main,
            height=30,
            wrap=tk.WORD,
            font=("Courier New", 10),
            state="disabled",
        )
        self.output_box.pack(
            fill="both",
            expand=True,
            pady=(5, 12),
        )

        self.input_box.focus_set()

    def run(self) -> None:
        raw_text = self.input_box.get(
            "1.0",
            tk.END,
        ).strip()

        try:
            result = run_master_flow(raw_text)
            report = format_report(result)
            self.audit_record = build_audit_record(result)
        except Exception as exc:
            messagebox.showerror(
                "ABTM flow error",
                str(exc),
            )
            return

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, report)
        self.output_box.config(state="disabled")

    def save_audit(self) -> None:
        if self.audit_record is None:
            messagebox.showwarning(
                "No report",
                "Run the full ABTM flow before saving.",
            )
            return

        destination = filedialog.asksaveasfilename(
            title="Save JUFE ABTM audit",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
            ],
            initialfile="jufe_abtm_full_audit.json",
        )

        if not destination:
            return

        Path(destination).write_text(
            json.dumps(
                self.audit_record,
                indent=2,
            ),
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
    MasterFlowApp(root)
    root.mainloop()
