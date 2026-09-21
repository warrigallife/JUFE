"""
Characterisation tests for the 64-cell / six-component mapping
(handover: one complete local state = 6 values in order Mx,My,Mz,Ax,Ay,Az;
64 cells = one 8 x 8 frame holding 384 values; partial cells are REPORTED,
never silently padded; overflow creates FURTHER frames, never a silent
rearrangement).

These tests pin CURRENT behaviour only. They add no mathematics, mappings
or rules. Where current behaviour contradicts the handover contract the
test asserts the CONTRACT and is marked expectedFailure ("OPEN").

Two code paths exist and behave differently:

* src.engines.abtm.ABTMEngine.evaluate groups values into 6-value states.
  It has no 8 x 8 frame concept at all.
* jufe_64_grid_mapper.map_to_grid puts ONE source value in each of 64
  cells (not 6 per cell), zero-pads short input and returns anything past
  64 as a flat overflow list (no further frames).

jufe_64_grid_mapper.py imports tkinter at module level, and tkinter is not
installed in every environment. Its pure parts are therefore loaded by
extracting their source with ast (no stubbing of tkinter, no execution of
the GUI class). The GUI (GridMapperApp) and analyse_grid (which loads
oldmate1 from disk) are NOT covered here.

Run from the repository root:

    python -m unittest discover -s tests -t . -v
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

import numpy as np

from src.engines.abtm import ABTMEngine

MAPPER_PATH = Path(__file__).resolve().parent.parent / "jufe_64_grid_mapper.py"
PURE_NAMES = {"GRID_SIZE", "GRID_CELLS", "map_to_grid"}
STATE_KEYS = ("Mx", "My", "Mz", "Ax", "Ay", "Az")


def _load_mapper_pure_parts() -> dict:
    """Execute only the named constants/functions of the mapper module."""
    tree = ast.parse(MAPPER_PATH.read_text(encoding="utf-8"))
    kept = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = {t.id for t in node.targets if isinstance(t, ast.Name)}
        elif isinstance(node, ast.FunctionDef):
            names = {node.name}
        else:
            names = set()
        if names & PURE_NAMES:
            kept.append(node)
    module = ast.Module(body=kept, type_ignores=[])
    ast.fix_missing_locations(module)
    namespace = {"np": np}
    exec(compile(module, str(MAPPER_PATH), "exec"), namespace)
    missing = PURE_NAMES - set(namespace)
    if missing:
        raise RuntimeError(f"Could not extract from mapper: {sorted(missing)}")
    return namespace


MAPPER = _load_mapper_pure_parts()
map_to_grid = MAPPER["map_to_grid"]


def _states(result: dict) -> list[list[float]]:
    """Ordered six-value lists from an evaluate() result."""
    if "states" in result:
        return [[s["state"][k] for k in STATE_KEYS] for s in result["states"]]
    return [[result["state"][k] for k in STATE_KEYS]]


def _floats(values) -> list[float]:
    return [float(v) for v in values]


class EngineSixValueGrouping(unittest.TestCase):
    """ABTMEngine.evaluate: matches the contract for grouping and remainder."""

    def setUp(self):
        self.engine = ABTMEngine()

    def test_six_values_make_one_cell(self):
        result = self.engine.evaluate(list(range(1, 7)))

        self.assertEqual(_states(result), [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]])

    def test_384_values_make_64_states_in_order(self):
        values = list(range(384))
        result = self.engine.evaluate(values)

        self.assertEqual(result["complete_states"], 64)
        self.assertEqual(result["remaining_count"], 0)
        flat = [v for state in _states(result) for v in state]
        self.assertEqual(flat, _floats(values))

    def test_385_to_389_values_report_extra_values_without_padding(self):
        for count in range(385, 390):
            with self.subTest(count=count):
                values = list(range(count))
                result = self.engine.evaluate(values)

                self.assertEqual(result["complete_states"], 64)
                self.assertEqual(len(result["states"]), 64)
                self.assertEqual(result["remaining_count"], count - 384)
                self.assertEqual(list(result["remaining"]), values[384:])

    def test_768_values_make_128_states_in_order(self):
        # The engine has no frame concept; it only yields 128 six-value states.
        values = list(range(768))
        result = self.engine.evaluate(values)

        self.assertEqual(result["complete_states"], 128)
        self.assertEqual(result["remaining_count"], 0)
        flat = [v for state in _states(result) for v in state]
        self.assertEqual(flat, _floats(values))

    def test_count_not_divisible_by_six_reports_remainder(self):
        for remainder in range(1, 6):
            with self.subTest(remainder=remainder):
                values = list(range(12 + remainder))
                result = self.engine.evaluate(values)

                self.assertEqual(result["complete_states"], 2)
                self.assertEqual(result["remaining_count"], remainder)
                self.assertEqual(list(result["remaining"]), values[12:])

    def test_order_is_preserved_across_the_64_state_boundary(self):
        values = list(range(390))
        states = _states(self.engine.evaluate(values))

        self.assertEqual(len(states), 65)
        self.assertEqual(states[63], _floats(values[378:384]))
        self.assertEqual(states[64], _floats(values[384:390]))

    def test_empty_and_short_input_are_rejected(self):
        for count in (0, 1, 5):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    self.engine.evaluate(list(range(count)))


class MapperCurrentBehaviour(unittest.TestCase):
    """map_to_grid as it behaves today: one value per cell, zero padded."""

    def test_constants(self):
        self.assertEqual(MAPPER["GRID_SIZE"], 8)
        self.assertEqual(MAPPER["GRID_CELLS"], 64)

    def test_64_values_fill_the_grid_row_major_with_no_overflow(self):
        grid, overflow = map_to_grid(_floats(range(64)))

        self.assertEqual(grid.shape, (8, 8))
        self.assertEqual(grid.flatten().tolist(), _floats(range(64)))
        self.assertEqual(overflow, [])

    def test_overflow_past_64_is_returned_in_order_not_dropped(self):
        values = _floats(range(70))
        grid, overflow = map_to_grid(values)

        self.assertEqual(grid.flatten().tolist(), values[:64])
        self.assertEqual(overflow, values[64:])

    def test_short_input_is_zero_padded_to_64_cells(self):
        grid, overflow = map_to_grid([1.0, 2.0, 3.0])

        flat = grid.flatten().tolist()
        self.assertEqual(grid.shape, (8, 8))
        self.assertEqual(flat[:3], [1.0, 2.0, 3.0])
        self.assertEqual(flat[3:], [0.0] * 61)
        self.assertEqual(overflow, [])

    def test_empty_input_gives_an_all_zero_grid(self):
        grid, overflow = map_to_grid([])

        self.assertEqual(grid.shape, (8, 8))
        self.assertFalse(grid.any())
        self.assertEqual(overflow, [])

    def test_custom_fill_value_is_used_for_padding(self):
        grid, _ = map_to_grid([1.0], fill_value=-1.0)

        self.assertEqual(grid.flatten().tolist()[1:], [-1.0] * 63)


class MapperContractDiscrepancies(unittest.TestCase):
    """
    Handover contract asserted against map_to_grid. Each contradiction is an
    expectedFailure: OPEN, needs project-owner decision. Do not "fix" the
    mapper without that decision (it changes what a cell and a frame mean).
    """

    @unittest.expectedFailure
    def test_384_values_fill_one_frame(self):
        """
        OPEN: needs project-owner decision.

        Contract: 384 values (64 cells x 6) fill one 8 x 8 frame. Today one
        value occupies one cell, so 320 of 384 values become overflow.
        """
        _, overflow = map_to_grid(_floats(range(384)))

        self.assertEqual(overflow, [])

    @unittest.expectedFailure
    def test_768_values_make_exactly_two_frames(self):
        """
        OPEN: needs project-owner decision.

        Contract: overflow creates FURTHER frames (768 -> 2 frames). Today
        map_to_grid builds one frame and returns the rest as a flat list;
        no second frame is ever built. Asserted here as: nothing is left
        unframed after mapping.
        """
        _, overflow = map_to_grid(_floats(range(768)))

        self.assertEqual(overflow, [])

    @unittest.expectedFailure
    def test_six_values_occupy_only_one_cell(self):
        """
        OPEN: needs project-owner decision.

        Contract: 6 values -> 1 cell, partial cells reported not padded.
        Today 6 values occupy 6 cells and the other 58 are silently
        zero-filled inside the returned array.
        """
        grid, _ = map_to_grid(_floats(range(1, 7)))

        self.assertEqual(grid.size, 1)

    @unittest.expectedFailure
    def test_short_input_is_not_padded(self):
        """
        OPEN: needs project-owner decision.

        Contract: partial cells are never silently padded. Today
        map_to_grid returns a full 64-cell array with invented 0.0 values.
        """
        grid, _ = map_to_grid([1.0, 2.0, 3.0])

        self.assertEqual(grid.size, 3)

    @unittest.expectedFailure
    def test_empty_input_creates_no_cells(self):
        """
        OPEN: needs project-owner decision.

        Contract: nothing is padded into existence. Today empty input still
        returns an 8 x 8 grid of zeros, indistinguishable from real zeros.
        """
        grid, _ = map_to_grid([])

        self.assertEqual(grid.size, 0)


if __name__ == "__main__":
    unittest.main()
