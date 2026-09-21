"""
Characterisation tests for the already-declared JUFE runtime contracts
(handover Issue 3 and Issue 4).

These tests pin CURRENT behaviour only. They do not assert that any
mathematics is established, and they add no new mathematics.

Run from the repository root:

    python -m unittest discover -s tests -t . -v
"""

from __future__ import annotations

import os
import tempfile
import unittest

from src.engines.abtm import ABTMEngine
from src.local_state import JUFELocalState
from src.runtime import JUFERuntime
from src.transformation import JUFETransformation


class LocalStateContract(unittest.TestCase):

    def test_exactly_six_values_form_one_local_state(self):
        state = JUFELocalState([1, 2, 3, 4, 5, 6])

        self.assertEqual(
            state.values, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        )
        self.assertEqual(
            (state.mx, state.my, state.mz, state.ax, state.ay, state.az),
            (1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
        )

    def test_other_counts_are_rejected(self):
        for count in (0, 5, 7):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    JUFELocalState([1.0] * count)

    def test_vacuum_requires_six_zeros(self):
        vacuum = JUFELocalState([0] * 6, lifecycle_state="VACUUM")
        self.assertTrue(vacuum.is_vacuum())

        with self.assertRaises(ValueError):
            JUFELocalState([0, 0, 0, 0, 0, 1], lifecycle_state="VACUUM")

    def test_undefined_and_vacuum_remain_distinct(self):
        undefined = JUFELocalState([1, 2, 3, 4, 5, 6], lifecycle_state="UNDEFINED")
        vacuum = JUFELocalState([0] * 6, lifecycle_state="VACUUM")

        self.assertEqual(undefined.lifecycle_state, "UNDEFINED")
        self.assertEqual(vacuum.lifecycle_state, "VACUUM")
        self.assertNotEqual(undefined.lifecycle_state, vacuum.lifecycle_state)

        # UNDEFINED is not bound by the six-zero rule; VACUUM is.
        self.assertFalse(undefined.is_vacuum())

    def test_phase_equilibrium_is_not_vacuum(self):
        locked = JUFELocalState([1, 2, 3, 1, 2, 3])

        self.assertTrue(locked.is_phase_equilibrium())
        self.assertFalse(locked.is_vacuum())

    def test_non_finite_and_non_numeric_components_are_rejected(self):
        with self.assertRaises(ValueError):
            JUFELocalState([float("nan"), 0, 0, 0, 0, 0])
        with self.assertRaises(ValueError):
            JUFELocalState([float("inf"), 0, 0, 0, 0, 0])
        with self.assertRaises(TypeError):
            JUFELocalState(["1", 0, 0, 0, 0, 0])


class EngineGrouping(unittest.TestCase):

    def setUp(self):
        self.engine = ABTMEngine()

    def test_fewer_than_six_values_are_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.evaluate([1, 2, 3, 4, 5])

    def test_multiple_complete_states_are_evaluated_without_rearrangement(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        result = self.engine.evaluate(values)

        self.assertEqual(result["complete_states"], 2)
        self.assertEqual(result["remaining_count"], 0)

        first = result["states"][0]["state"]
        second = result["states"][1]["state"]

        self.assertEqual(
            [first[k] for k in ("Mx", "My", "Mz", "Ax", "Ay", "Az")],
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        )
        self.assertEqual(
            [second[k] for k in ("Mx", "My", "Mz", "Ax", "Ay", "Az")],
            [7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
        )

    def test_remaining_values_are_preserved_exactly(self):
        values = [1, 2, 3, 4, 5, 6, 99, 98]
        result = self.engine.evaluate(values)

        self.assertEqual(result["complete_states"], 1)
        self.assertEqual(list(result["remaining"]), [99, 98])
        self.assertEqual(result["remaining_count"], 2)

    def test_partial_values_are_not_silently_padded(self):
        result = self.engine.evaluate([1, 2, 3, 4, 5, 6, 7])

        # Seven values: one complete state, one value reported, no padded second state.
        self.assertEqual(len(result["states"]), 1)
        self.assertEqual(result["complete_states"], 1)
        self.assertEqual(result["remaining_count"], 1)
        self.assertEqual(list(result["remaining"]), [7])

    def test_single_complete_state_without_remainder_is_returned_flat(self):
        result = self.engine.evaluate([1, 2, 3, 4, 5, 6])

        self.assertNotIn("states", result)
        self.assertIn("state", result)


class IdentityTransformation(unittest.TestCase):

    def test_values_are_preserved_and_provenance_is_recorded(self):
        original = JUFELocalState([1, 2, 3, 4, 5, 6])
        transformed = JUFETransformation("Identity").apply(original)

        self.assertIsNot(transformed, original)
        self.assertEqual(transformed.values, original.values)
        self.assertEqual(transformed.transformation, "Identity")

    def test_original_state_is_left_untouched(self):
        original = JUFELocalState([1, 2, 3, 4, 5, 6])
        JUFETransformation("Identity").apply(original)

        self.assertIsNone(original.transformation)
        self.assertEqual(original.values, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])


class SpecificationBoot(unittest.TestCase):
    """
    Handover Issue 3: runtime boot must not depend on filesystem case
    or on the current working directory.
    """

    def _boot_reaches_validation(self):
        """
        Boot must FIND and LOAD SPEC-010. Reaching the validator
        (ValueError) proves the file was located; only
        FileNotFoundError means the path is wrong.
        """
        try:
            JUFERuntime().boot()
        except FileNotFoundError:
            self.fail("Boot could not locate Specifications/SPEC-010.md")
        except ValueError:
            pass

    def test_boot_locates_the_specification(self):
        self._boot_reaches_validation()

    def test_boot_locates_the_specification_from_a_different_working_directory(self):
        previous = os.getcwd()
        with tempfile.TemporaryDirectory() as elsewhere:
            os.chdir(elsewhere)
            try:
                self._boot_reaches_validation()
            finally:
                os.chdir(previous)

    @unittest.expectedFailure
    def test_boot_completes_end_to_end(self):
        """
        OPEN, needs a decision from the project owner.

        The parser counts a definition only when a line STARTS with
        'DEF-', and the validator rejects a specification with none.
        Specifications/SPEC-010.md contains no such line, so boot stops
        at 'Specification contains no executable definitions.'
        Do not "fix" this by editing the parser or the specification
        without approval: it changes what a definition means.
        """
        result = JUFERuntime().boot()

        self.assertIn("kernel", result)


if __name__ == "__main__":
    unittest.main()
