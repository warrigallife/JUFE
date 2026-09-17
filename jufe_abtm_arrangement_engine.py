"""
JUFE ABTM Arrangement Engine
============================

A separate tool that does not edit:
- oldmate1(5).py
- oldmate2(4).py
- abtm_expansion.py
- jufe_abtm_results_launcher.py

Purpose
-------
1. Parse user sequences:
   - each non-empty line is one set
   - spaces separate subgroups
   - commas separate values within a subgroup
2. Preserve the original sets and subgroup order.
3. Search for subgroup alignments whose comparison-matrix trace is divisible by 6.
4. Show every passing arrangement.
5. Save a JSON audit record containing:
   - original input
   - parsed groups
   - group totals
   - selected diagonal groups
   - arranged matrix
   - trace
   - trace modulo 6
   - pass/fail result

The tool never changes source data silently. Every rearrangement is reported.
"""

from __future__ import annotations

import itertools
import json
import re
import tkinter as tk
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext
from typing import Any

import numpy as np


@dataclass
class ParsedSet:
    set_index: int
    groups: list[list[float]]
    group_totals: list[float]


@dataclass
class ArrangementResult:
    selected_group_indices: list[int]
    selected_group_totals: list[float]
    arranged_group_totals: list[list[float]]
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
        raise ValueError(f"Non-finite value found: {token}")
    return value


def parse_sets(raw_text: str) -> list[ParsedSet]:
    parsed: list[ParsedSet] = []

    for set_index, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        group_tokens = [part for part in re.split(r"\s+", line) if part]
        groups: list[list[float]] = []

        for group_index, group_text in enumerate(group_tokens, start=1):
            tokens = [token for token in group_text.split(",") if token.strip()]
            if not tokens:
                raise ValueError(
                    f"Set {set_index}, group {group_index} has no values."
                )
            groups.append([parse_number(token) for token in tokens])

        parsed.append(
            ParsedSet(
                set_index=set_index,
                groups=groups,
                group_totals=[float(sum(group)) for group in groups],
            )
        )

    if not parsed:
        raise ValueError("Enter at least one set.")

    return parsed


def arrange_row_for_diagonal(
    totals: list[float],
    selected_index: int,
    diagonal_column: int,
    width: int,
) -> list[float]:
    """
    Place one selected subgroup total in the requested diagonal column.
    Keep all remaining subgroup totals in their original relative order.
    Pad unused cells with zero.
    """
    selected = totals[selected_index]
    remaining = [
        value for index, value in enumerate(totals)
        if index != selected_index
    ]

    row: list[float | None] = [None] * width
    row[diagonal_column] = selected

    remaining_iter = iter(remaining)
    for column in range(width):
        if row[column] is None:
            row[column] = next(remaining_iter, 0.0)

    return [float(value) for value in row]


def search_trace_stable_arrangements(
    parsed_sets: list[ParsedSet],
) -> tuple[list[ArrangementResult], int]:
    """
    Search all choices of one diagonal subgroup per set.

    For N sets, the comparison matrix has N rows.
    The width is max(N, largest subgroup count).
    Set i contributes its selected subgroup total at diagonal position (i, i).
    """
    set_count = len(parsed_sets)
    width = max(
        set_count,
        max(len(item.group_totals) for item in parsed_sets),
    )

    choice_ranges = [
        range(len(item.group_totals))
        for item in parsed_sets
    ]

    results: list[ArrangementResult] = []
    tested = 0

    for selected_indices in itertools.product(*choice_ranges):
        tested += 1

        matrix_rows = []
        selected_totals = []

        for row_index, (item, selected_index) in enumerate(
            zip(parsed_sets, selected_indices)
        ):
            selected_totals.append(item.group_totals[selected_index])
            matrix_rows.append(
                arrange_row_for_diagonal(
                    item.group_totals,
                    selected_index,
                    row_index,
                    width,
                )
            )

        matrix = np.asarray(matrix_rows, dtype=float)
        trace = float(np.trace(matrix))
        residue = float(trace % 6)
        stable = bool(np.isclose(residue, 0.0))

        if stable:
            results.append(
                ArrangementResult(
                    selected_group_indices=[
                        index + 1 for index in selected_indices
                    ],
                    selected_group_totals=selected_totals,
                    arranged_group_totals=matrix_rows,
                    trace=trace,
                    trace_mod_6=residue,
                    stable=True,
                )
            )

    return results, tested


def build_audit_record(
    raw_text: str,
    parsed_sets: list[ParsedSet],
    results: list[ArrangementResult],
    tested: int,
) -> dict[str, Any]:
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input_rules": {
            "line_break": "separate set",
            "space": "separate subgroup",
            "comma": "separate values inside subgroup",
        },
        "raw_input": raw_text,
        "sets": [asdict(item) for item in parsed_sets],
        "arrangements_tested": tested,
        "passing_arrangements": [asdict(item) for item in results],
    }


def format_report(
    parsed_sets: list[ParsedSet],
    results: list[ArrangementResult],
    tested: int,
) -> str:
    lines: list[str] = []

    lines.append("ORIGINAL DATA")
    lines.append("=" * 64)

    for item in parsed_sets:
        lines.append(f"SET {item.set_index}")
        lines.append(
            "Group totals: "
            + ", ".join(display_number(value) for value in item.group_totals)
        )
        lines.append(
            f"Set total: {display_number(sum(item.group_totals))}"
        )
        lines.append("")

    lines.append("ARRANGEMENT SEARCH")
    lines.append("=" * 64)
    lines.append(f"Arrangements tested: {tested}")
    lines.append(f"Trace-mod-6 passing arrangements: {len(results)}")
    lines.append("")

    if not results:
        lines.append("No trace-mod-6 stable arrangement was found.")
        return "\n".join(lines)

    for result_index, result in enumerate(results, start=1):
        lines.append(f"PASSING ARRANGEMENT {result_index}")
        lines.append("-" * 64)

        for set_index, (group_index, total) in enumerate(
            zip(
                result.selected_group_indices,
                result.selected_group_totals,
            ),
            start=1,
        ):
            lines.append(
                f"Set {set_index}: group {group_index} selected "
                f"for diagonal, total = {display_number(total)}"
            )

        lines.append("")
        lines.append("Arranged comparison matrix:")

        for row in result.arranged_group_totals:
            lines.append(
                "[" + ", ".join(display_number(value) for value in row) + "]"
            )

        lines.append("")
        lines.append(f"Trace       : {display_number(result.trace)}")
        lines.append(
            f"Trace mod 6 : {display_number(result.trace_mod_6)}"
        )
        lines.append(f"Stable      : {result.stable}")
        lines.append("")

    return "\n".join(lines)


class ArrangementApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.audit_record: dict[str, Any] | None = None

        root.title("JUFE ABTM Arrangement Engine")
        root.geometry("980x820")
        root.minsize(780, 620)

        tk.Label(
            root,
            text="JUFE ABTM Arrangement Engine",
            font=("Arial", 18, "bold"),
        ).pack(pady=(14, 5))

        tk.Label(
            root,
            text=(
                "Each line is one set. Spaces separate subgroups. "
                "Commas separate values.\n"
                "The search preserves all source values and reports every "
                "trace-mod-6 passing arrangement."
            ),
            justify="center",
            font=("Arial", 11),
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

        tk.Button(
            controls,
            text="Find Stable Arrangements",
            command=self.analyse,
            width=24,
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
            text="Save Audit JSON",
            command=self.save_audit,
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
            text="Analysis:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

        self.output_box = scrolledtext.ScrolledText(
            main,
            height=28,
            wrap=tk.WORD,
            font=("Courier New", 10),
            state="disabled",
        )
        self.output_box.pack(fill="both", expand=True, pady=(5, 12))

        self.input_box.focus_set()

    def analyse(self) -> None:
        raw_text = self.input_box.get("1.0", tk.END).strip()

        try:
            parsed = parse_sets(raw_text)
            results, tested = search_trace_stable_arrangements(parsed)
            report = format_report(parsed, results, tested)
            self.audit_record = build_audit_record(
                raw_text,
                parsed,
                results,
                tested,
            )
        except Exception as exc:
            messagebox.showerror("Arrangement error", str(exc))
            return

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, report)
        self.output_box.config(state="disabled")

    def save_audit(self) -> None:
        if self.audit_record is None:
            messagebox.showwarning(
                "No analysis",
                "Run the arrangement search before saving an audit record.",
            )
            return

        destination = filedialog.asksaveasfilename(
            title="Save ABTM arrangement audit",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="abtm_arrangement_audit.json",
        )

        if not destination:
            return

        Path(destination).write_text(
            json.dumps(self.audit_record, indent=2),
            encoding="utf-8",
        )

        messagebox.showinfo(
            "Audit saved",
            f"Audit record saved to:\n{destination}",
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
    ArrangementApp(root)
    root.mainloop()
