#!/usr/bin/env python3
"""
JUFE Read-Only System Check
===========================

Place this file in JUFE_CLEAN_VERIFIED and run:

    python3 jufe_system_check.py

It does not edit any JUFE source file. It checks:
- required runtime files
- Python syntax
- /mnt/data contamination
- module imports
- original ABTM engine
- optimised master flow
- 64-grid mapper
- optional specification engine package
"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

RUNTIME_FILES = [
    "oldmate1(5).py",
    "oldmate2(4).py",
    "abtm_expansion.py",
    "jufe_original_launcher.py",
]

OPTIMISED_FILES = [
    "abtm_residue_search.py",
    "jufe_abtm_optimized_master_flow.py",
]

OPTIONAL_FILES = [
    "jufe_abtm_master_flow.py",
    "jufe_abtm_results_launcher.py",
    "jufe_abtm_arrangement_engine.py",
    "jufe_64_grid_mapper.py",
]

KNOWN_SAMPLE = """1,4,1,40 1,50,4 5,400,5
7,1,90,4,5,50 60,6 5,4,5,50"""


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create import specification for {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def status(label: str, passed: bool, detail: str = "") -> None:
    marker = "PASS" if passed else "FAIL"
    suffix = f" — {detail}" if detail else ""
    print(f"[{marker}] {label}{suffix}")


def main() -> int:
    failures = 0

    print("=" * 72)
    print("JUFE READ-ONLY SYSTEM CHECK")
    print("=" * 72)
    print(f"Folder: {ROOT}")
    print()

    all_expected = RUNTIME_FILES + OPTIMISED_FILES + OPTIONAL_FILES

    print("1. FILE PRESENCE")
    print("-" * 72)
    for name in all_expected:
        exists = (ROOT / name).is_file()
        required = name in RUNTIME_FILES or name in OPTIMISED_FILES
        if required and not exists:
            failures += 1
        status(
            name,
            exists if required else True,
            "present" if exists else ("missing (required)" if required else "not installed (optional)"),
        )
    print()

    print("2. INTERNAL-PATH CONTAMINATION")
    print("-" * 72)
    for name in all_expected:
        path = ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        clean = "/mnt/data" not in text
        if not clean:
            failures += 1
        status(name, clean, "no /mnt/data reference" if clean else "contains /mnt/data")
    print()

    print("3. PYTHON SYNTAX")
    print("-" * 72)
    for name in all_expected:
        path = ROOT / name
        if not path.is_file():
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            status(name, True)
        except Exception as exc:
            failures += 1
            status(name, False, str(exc))
    print()

    print("4. CORE IMPORTS AND ORIGINAL ENGINE")
    print("-" * 72)
    try:
        sys.path.insert(0, str(ROOT))
        expansion = load_module("jufe_check_abtm_expansion", ROOT / "abtm_expansion.py")
        status("Import abtm_expansion.py", True)

        oldmate1_path = ROOT / "oldmate1(5).py"
        spec = importlib.util.spec_from_file_location("jufe_check_oldmate1", oldmate1_path)
        if spec is None or spec.loader is None:
            raise ImportError("Could not prepare oldmate1.")
        oldmate1 = importlib.util.module_from_spec(spec)
        oldmate1.ABTM_Expansion = expansion.ABTM_Expansion
        sys.modules[spec.name] = oldmate1
        spec.loader.exec_module(oldmate1)
        status("Load original oldmate1 with ABTM_Expansion", True)

        engine = oldmate1.ABTM_Engine()
        import numpy as np
        matrix = np.array([[410, 46, 55], [157, 64, 66]], dtype=float)
        stable = bool(engine.compute_manifold_stability(matrix))
        status(
            "Original trace-mod-6 reference test",
            stable,
            f"trace={float(np.trace(matrix)):g}, stable={stable}",
        )
        if not stable:
            failures += 1
    except Exception as exc:
        failures += 1
        status("Core engine test", False, repr(exc))
    print()

    print("5. OPTIMISED MASTER FLOW")
    print("-" * 72)
    optimized_path = ROOT / "jufe_abtm_optimized_master_flow.py"
    residue_path = ROOT / "abtm_residue_search.py"
    if optimized_path.is_file() and residue_path.is_file():
        try:
            optimized = load_module("jufe_check_optimized_flow", optimized_path)
            result = optimized.run_master_flow(KNOWN_SAMPLE)

            checks = {
                "passing arrangement found": result["selected_arrangement"] is not None,
                "original engine stable": result["original_engine_result"] is True,
                "combined Z6 balanced": result["combined_z6_balanced"] is True,
                "all set mod-7 balanced": result["all_mod7_balanced"] is True,
                "pairwise aligned": result["pairwise_aligned"] is True,
                "overall ABTM balance": result["overall_balanced"] is True,
            }

            for label, passed in checks.items():
                status(label, passed)
                if not passed:
                    failures += 1

            stats = result.get("search_stats", {})
            print(
                "    search:",
                f"theoretical={stats.get('theoretical_combinations')},",
                f"explored={stats.get('states_explored')},",
                f"pruned={stats.get('branches_pruned')}",
            )
        except Exception as exc:
            failures += 1
            status("Optimised master flow test", False, repr(exc))
    else:
        failures += 1
        status("Optimised master flow test", False, "required files missing")
    print()

    print("6. 64-GRID MAPPER")
    print("-" * 72)
    grid_path = ROOT / "jufe_64_grid_mapper.py"
    if grid_path.is_file():
        try:
            grid = load_module("jufe_check_grid_mapper", grid_path)
            result, groups = grid.analyse_grid(KNOWN_SAMPLE, "Individual values")
            valid_shape = len(result.grid) == 8 and all(len(row) == 8 for row in result.grid)
            status("8 x 8 grid construction", valid_shape)
            status("64-grid audit result produced", result.source_item_count == 22)
            print(
                f"    known sample direct mapping: trace={result.trace:g}, "
                f"mod6={result.trace_mod_6:g}, stable={result.stable}"
            )
            if not valid_shape:
                failures += 1
        except Exception as exc:
            failures += 1
            status("64-grid mapper test", False, repr(exc))
    else:
        status("64-grid mapper", True, "not installed (optional)")
    print()

    print("7. SPECIFICATION ENGINE")
    print("-" * 72)
    spec_dirs = [
        ROOT / "JUFE_ABTM_SPEC_ENGINE",
        ROOT.parent / "JUFE_ABTM_SPEC_ENGINE",
    ]
    spec_dir = next((path for path in spec_dirs if path.is_dir()), None)

    if spec_dir is None:
        status(
            "Specification engine",
            True,
            "not found beside runtime; run separately from its own folder",
        )
    else:
        try:
            validator = load_module(
                "jufe_check_validate_requirements",
                spec_dir / "validate_requirements.py",
            )
            errors = validator.validate_register(spec_dir / "requirements_register.json")
            status("Requirements register integrity", not errors, "; ".join(errors))
            if errors:
                failures += 1

            spec_engine = load_module(
                "jufe_check_specification_engine",
                spec_dir / "specification_engine.py",
            )
            report_engine = spec_engine.SpecificationEngine(
                spec_dir / "requirements_register.json"
            )
            coverage = report_engine.coverage()
            status(
                "Specification engine report",
                coverage["total_requirements"] > 0,
                f"{coverage['total_requirements']} requirements",
            )
        except Exception as exc:
            failures += 1
            status("Specification engine test", False, repr(exc))
    print()

    print("=" * 72)
    if failures:
        print(f"SYSTEM CHECK COMPLETED WITH {failures} FAILURE(S).")
        print("No JUFE files were changed.")
        return 1

    print("SYSTEM CHECK PASSED.")
    print("No JUFE files were changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
