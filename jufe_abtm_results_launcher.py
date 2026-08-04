"""
JUFE / ABTM Results Launcher
============================

Separate graphical launcher.

This file does not edit:
- oldmate1(5).py
- oldmate2(4).py
- abtm_expansion.py

Input interpretation approved for this launcher:
- each non-empty line = one set
- spaces separate subgroups
- commas separate values inside each subgroup

Example:
    1,4,1,40 1,50,4 5,400,5
    7,1,90,4,5,50 60,6 5,4,5,50
"""

from __future__ import annotations

import importlib.util
import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext
from types import ModuleType
from typing import Any

import numpy as np

from abtm_expansion import ABTM_Expansion


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
        raise ValueError("Empty numerical value found.")

    try:
        value = float(token)
    except ValueError as exc:
        raise ValueError(f"'{token}' is not a valid number.") from exc

    if not np.isfinite(value):
        raise ValueError(f"'{token}' is not finite.")

    return value


def display_number(value: float) -> str:
    value = float(value)
    return str(int(value)) if value.is_integer() else str(value)


def parse_abtm_sets(raw_text: str) -> list[dict[str, Any]]:
    """
    Parse:
      line break -> separate set
      whitespace  -> separate subgroup
      comma       -> value inside subgroup
    """
    sets: list[dict[str, Any]] = []

    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        subgroup_tokens = [part for part in re.split(r"\s+", line) if part]
        groups: list[list[float]] = []

        for group_number, subgroup in enumerate(subgroup_tokens, start=1):
            value_tokens = [token for token in subgroup.split(",") if token.strip()]

            if not value_tokens:
                raise ValueError(
                    f"Set {line_number}, group {group_number} contains no values."
                )

            values = [parse_number(token) for token in value_tokens]
            groups.append(values)

        flat_values = [value for group in groups for value in group]
        group_totals = [float(sum(group)) for group in groups]
        set_total = float(sum(group_totals))
        mod7 = set_total % 7

        sets.append(
            {
                "line_number": line_number,
                "groups": groups,
                "flat_values": flat_values,
                "group_totals": group_totals,
                "set_total": set_total,
                "mod7": mod7,
                "mod7_balanced": bool(np.isclose(mod7, 0.0)),
            }
        )

    if not sets:
        raise ValueError("Enter at least one non-empty set.")

    return sets


def build_comparison_matrix(sets: list[dict[str, Any]]) -> np.ndarray:
    """
    Build a comparison matrix from subgroup totals.

    Each row represents one set.
    Shorter rows are padded with zeros only for matrix comparison/reporting.
    The original group totals and set totals remain unchanged.
    """
    max_groups = max(len(item["group_totals"]) for item in sets)
    rows = []

    for item in sets:
        row = list(item["group_totals"])
        row.extend([0.0] * (max_groups - len(row)))
        rows.append(row)

    return np.array(rows, dtype=float)


def run_abtm_analysis(raw_text: str, treatise_text: str = "") -> dict[str, Any]:
    folder = Path(__file__).resolve().parent

    oldmate1_path = find_original(folder, "oldmate1")
    oldmate2_path = find_original(folder, "oldmate2")

    oldmate1 = load_oldmate1(oldmate1_path)
    oldmate2 = load_normal_module(oldmate2_path, "jufe_oldmate2_original")

    engine = oldmate1.ABTM_Engine()
    sets = parse_abtm_sets(raw_text)

    comparison_matrix = build_comparison_matrix(sets)

    combined_total = float(sum(item["set_total"] for item in sets))
    combined_mod6 = combined_total % 6
    combined_z6_balanced = bool(np.isclose(combined_mod6, 0.0))

    all_mod7_balanced = all(item["mod7_balanced"] for item in sets)

    pairwise = []
    for left_index in range(len(sets)):
        for right_index in range(left_index + 1, len(sets)):
            difference = abs(
                sets[left_index]["set_total"]
                - sets[right_index]["set_total"]
            )
            pairwise.append(
                {
                    "left": left_index + 1,
                    "right": right_index + 1,
                    "difference": difference,
                    "difference_mod7": difference % 7,
                    "difference_mod7_balanced": bool(
                        np.isclose(difference % 7, 0.0)
                    ),
                }
            )

    pairwise_aligned = all(
        item["difference_mod7_balanced"] for item in pairwise
    ) if pairwise else True

    # Original ABTM engine method applied to the comparison matrix.
    original_engine_stable = bool(
        engine.compute_manifold_stability(comparison_matrix)
    )
    original_trace = float(np.trace(comparison_matrix))
    original_trace_mod6 = original_trace % 6

    # Expansion-layer results that are directly meaningful for this input.
    z6_expansion_result = engine.z6_stable(comparison_matrix)
    set_mod7_phases = [
        engine.mod7_phase(item["set_total"]) for item in sets
    ]

    kernel_1 = oldmate1.JUFE_Kernel(treatise_text, engine)
    kernel_2 = oldmate2.JUFE_Kernel(
        treatise_text,
        engine.__class__.__name__,
    )

    sealed_1 = kernel_1.execute_boot()
    sealed_2 = kernel_2.execute_boot()

    overall_balanced = bool(
        all_mod7_balanced
        and combined_z6_balanced
        and pairwise_aligned
    )

    return {
        "sets": sets,
        "comparison_matrix": comparison_matrix,
        "combined_total": combined_total,
        "combined_mod6": combined_mod6,
        "combined_z6_balanced": combined_z6_balanced,
        "all_mod7_balanced": all_mod7_balanced,
        "pairwise": pairwise,
        "pairwise_aligned": pairwise_aligned,
        "original_trace": original_trace,
        "original_trace_mod6": original_trace_mod6,
        "original_engine_stable": original_engine_stable,
        "z6_expansion_result": z6_expansion_result,
        "set_mod7_phases": set_mod7_phases,
        "overall_balanced": overall_balanced,
        "oldmate1_file": oldmate1_path.name,
        "oldmate2_file": oldmate2_path.name,
        "sealed_1": sealed_1,
        "sealed_2": sealed_2,
    }


def format_results(result: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.extend(
        [
            f"Loaded file 1 : {result['oldmate1_file']}",
            f"Loaded file 2 : {result['oldmate2_file']}",
            "",
        ]
    )

    for index, item in enumerate(result["sets"], start=1):
        lines.append(f"SET {index}")
        lines.append("-" * 50)
        lines.append(f"Groups        : {len(item['groups'])}")
        lines.append(
            "Group totals  : "
            + ", ".join(display_number(v) for v in item["group_totals"])
        )
        lines.append(f"Set total     : {display_number(item['set_total'])}")
        lines.append(f"Mod 7         : {display_number(item['mod7'])}")
        lines.append(
            f"Harmonic      : "
            f"{'BALANCED' if item['mod7_balanced'] else 'NOT BALANCED'}"
        )
        lines.append("")

    lines.extend(
        [
            "COMBINED STRUCTURE",
            "-" * 50,
            f"Combined total : {display_number(result['combined_total'])}",
            f"Combined mod 6 : {display_number(result['combined_mod6'])}",
            (
                "Z6 structure   : "
                + (
                    "BALANCED"
                    if result["combined_z6_balanced"]
                    else "NOT BALANCED"
                )
            ),
            "",
        ]
    )

    if result["pairwise"]:
        lines.extend(["PAIRWISE COMPARISON", "-" * 50])
        for item in result["pairwise"]:
            lines.append(
                f"Set {item['left']} vs Set {item['right']} difference: "
                f"{display_number(item['difference'])}"
            )
            lines.append(
                f"Difference mod 7: "
                f"{display_number(item['difference_mod7'])}"
            )
            lines.append(
                "Pair alignment : "
                + (
                    "BALANCED"
                    if item["difference_mod7_balanced"]
                    else "NOT BALANCED"
                )
            )
            lines.append("")

    lines.extend(
        [
            "ORIGINAL ENGINE VIEW",
            "-" * 50,
            "Comparison matrix built from subgroup totals:",
            np.array2string(result["comparison_matrix"]),
            "",
            f"Trace          : {display_number(result['original_trace'])}",
            (
                f"Trace mod 6    : "
                f"{display_number(result['original_trace_mod6'])}"
            ),
            f"Original stable: {result['original_engine_stable']}",
            "",
            "ABTM EXPANSION VIEW",
            "-" * 50,
            (
                "Set mod-7 phases : "
                + ", ".join(
                    display_number(value)
                    for value in result["set_mod7_phases"]
                )
            ),
            f"Z6 matrix stable: {result['z6_expansion_result']}",
            "",
            "OVERALL",
            "-" * 50,
            (
                "ABTM BALANCE: "
                + ("TRUE" if result["overall_balanced"] else "FALSE")
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
        ]
    )

    return "\n".join(lines)


class ABTMResultsApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        root.title("JUFE ABTM Results Launcher")
        root.geometry("940x800")
        root.minsize(760, 620)

        tk.Label(
            root,
            text="JUFE ABTM Results Launcher",
            font=("Arial", 18, "bold"),
        ).pack(pady=(14, 5))

        tk.Label(
            root,
            text=(
                "Each line is one set. Spaces separate subgroups. "
                "Commas separate values."
            ),
            font=("Arial", 11),
            justify="center",
        ).pack(pady=(0, 10))

        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=18)

        tk.Label(
            main,
            text="ABTM datasets:",
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

        example = (
            "1,4,1,40 1,50,4 5,400,5\n"
            "7,1,90,4,5,50 60,6 5,4,5,50"
        )

        buttons = tk.Frame(main)
        buttons.pack(pady=5)

        tk.Button(
            buttons,
            text="Analyse ABTM Sets",
            command=self.run,
            width=20,
            font=("Arial", 11, "bold"),
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Load Example",
            command=lambda: self.load_example(example),
            width=14,
            font=("Arial", 11),
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Clear",
            command=self.clear,
            width=10,
            font=("Arial", 11),
        ).pack(side="left", padx=5)

        tk.Label(
            main,
            text="Results:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

        self.results_box = scrolledtext.ScrolledText(
            main,
            height=24,
            wrap=tk.WORD,
            font=("Courier New", 10),
            state="disabled",
        )
        self.results_box.pack(fill="both", expand=True, pady=(5, 12))

        self.input_box.focus_set()

    def run(self) -> None:
        raw_text = self.input_box.get("1.0", tk.END).strip()

        try:
            result = run_abtm_analysis(raw_text)
            output = format_results(result)
        except Exception as exc:
            messagebox.showerror("ABTM analysis error", str(exc))
            return

        self.results_box.config(state="normal")
        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, output)
        self.results_box.config(state="disabled")

    def load_example(self, example: str) -> None:
        self.input_box.delete("1.0", tk.END)
        self.input_box.insert(tk.END, example)
        self.input_box.focus_set()

    def clear(self) -> None:
        self.input_box.delete("1.0", tk.END)
        self.results_box.config(state="normal")
        self.results_box.delete("1.0", tk.END)
        self.results_box.config(state="disabled")
        self.input_box.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    ABTMResultsApp(root)
    root.mainloop()
