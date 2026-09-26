"""
Integration tests for the four opt-in diagnostic keyword arguments now
exposed on ``ABTMEngine.evaluate()`` (src/engines/abtm.py) and
``JUFERuntime.evaluate()`` (src/runtime.py):

    dominance_threshold      -> JUFEFieldGradient.evaluate_dominance
    phase_lock_tolerance     -> JUFEPhaseLock.evaluate_phase_lock
    global_balance_tolerance -> JUFEGlobalConservation.global_field_balance
    bifurcation_threshold    -> JUFESensitivityMatrix.evaluate_bifurcation

All four default to ``None`` ("not requested"). This file's central
concern is proving two things at once:

1. When all four are ``None`` (the default), ``evaluate()``'s output is
   BYTE-FOR-BYTE / VALUE-FOR-VALUE identical to its output before these
   four keyword arguments existed -- across every branch (short-input
   error, single complete state, multi-state, non-multiple-of-six
   remainder) -- with the ``"diagnostics"`` key completely ABSENT, not
   ``None`` and not ``{}``, in that case.
2. When one or more are supplied, an additive-only ``"diagnostics"``
   mapping appears, built by calling the four already-reviewed opt-in
   methods directly (this file does not reimplement their math) with
   the caller's exact value, never a default/clamped/coerced one, and
   never touching any other existing result field.

This file does not modify, and is independent of, the six existing test
files (tests/test_abtm_evaluate_baseline.py, tests/test_z6_equivalence.py,
tests/test_coupled_field_step.py, tests/test_global_field_balance.py,
tests/test_sensitivity_bifurcation.py,
tests/test_field_gradient_dominance.py). Those files' own full-suite
pass (unchanged) is the primary evidence that default-output identity
holds everywhere, not just for the specific inputs re-checked here.
"""

from __future__ import annotations

import unittest

from src.engines.abtm import ABTMEngine
from src.field_gradient import JUFEFieldGradient
from src.global_conservation import JUFEGlobalConservation
from src.local_state import JUFELocalState
from src.phase_lock import JUFEPhaseLock
from src.runtime import JUFERuntime
from src.sensitivity_matrix import JUFESensitivityMatrix
from src.transformation import JUFETransformation


def _identity_6x6():
    return [
        [1.0 if row == col else 0.0 for col in range(6)]
        for row in range(6)
    ]


def _transformed(values):
    """
    Reproduce exactly what ABTMEngine.evaluate() feeds into the four
    opt-in methods for one six-value chunk: a JUFELocalState run
    through the engine's own JUFETransformation("Identity").apply().
    """
    state = JUFELocalState([float(v) for v in values])
    return JUFETransformation("Identity").apply(state)


# ---------------------------------------------------------------------
# Golden default-output dicts (identical to the ones independently
# transcribed and verified in the prior five consolidation steps).
# ---------------------------------------------------------------------

def _expected_balanced():
    expected_state = {
        "Mx": 3.0, "My": 5.0, "Mz": 2.0,
        "Ax": 3.0, "Ay": 5.0, "Az": 2.0,
        "cell_coordinate": None,
        "frame_index": None,
        "lifecycle_state": "ACTIVE",
        "mapping_version": "JUFE-LOCAL-1",
        "transformation": "Identity",
        "phase_difference": [0.0, 0.0, 0.0],
        "phase_equilibrium": True,
        "vacuum": False,
    }
    return {
        "state": expected_state,
        "gradient": {
            "gradient": (3.0, 5.0, 2.0),
            "propagation": (-3.0, -5.0, -2.0),
            "magnitude": 6.164414002968976,
            "gradient_dominance": False,
        },
        "phase": [0.0, 0.0, 0.0],
        "phase_lock": {
            "vacuum": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "packet": expected_state,
            "phase_locked": True,
        },
        "local_conservation": True,
        "equilibrium": True,
        "toroidal_flux": {
            "omega_t": 1.0,
            "geometry": 8.717797887081348,
            "xi": 8.717797887081348,
            "work": 8.717797887081348,
        },
        "tensegrity_tensor": {
            "geometry": 6.164414002968976,
            "structural_constraint": 1.0,
            "toroidal_flux": 8.717797887081348,
            "harmonic_modulation": 1.0,
            "total": 16.882211890050325,
            "divergence_free": False,
        },
        "stable": True,
        "global_conservation": {
            "global_sum": 20.0,
            "conserved": False,
            "residual": 20.0,
        },
        "harmonic_layer": {
            "harmonic": 0,
            "phase": 0.0,
            "modulation": 1.0,
        },
        "sensitivity_matrix": {
            "matrix": _identity_6x6(),
            "determinant": 1.0,
            "catastrophic_transition": False,
        },
        "status": "IMPLEMENTED",
    }


def _expected_unbalanced():
    expected_state = {
        "Mx": 3.0, "My": 5.0, "Mz": 2.0,
        "Ax": 1.0, "Ay": 4.0, "Az": 6.0,
        "cell_coordinate": None,
        "frame_index": None,
        "lifecycle_state": "ACTIVE",
        "mapping_version": "JUFE-LOCAL-1",
        "transformation": "Identity",
        "phase_difference": [2.0, 1.0, -4.0],
        "phase_equilibrium": False,
        "vacuum": False,
    }
    return {
        "state": expected_state,
        "gradient": {
            "gradient": (3.0, 5.0, 2.0),
            "propagation": (-3.0, -5.0, -2.0),
            "magnitude": 6.164414002968976,
            "gradient_dominance": False,
        },
        "phase": [2.0, 1.0, -4.0],
        "phase_lock": None,
        "local_conservation": True,
        "equilibrium": False,
        "toroidal_flux": {
            "omega_t": 1.0,
            "geometry": 9.539392014169456,
            "xi": 9.539392014169456,
            "work": 9.539392014169456,
        },
        "tensegrity_tensor": {
            "geometry": 6.164414002968976,
            "structural_constraint": 1.0,
            "toroidal_flux": 9.539392014169456,
            "harmonic_modulation": 1.0,
            "total": 17.703806017138433,
            "divergence_free": False,
        },
        "stable": False,
        "global_conservation": {
            "global_sum": 21.0,
            "conserved": False,
            "residual": 21.0,
        },
        "harmonic_layer": {
            "harmonic": 0,
            "phase": 0.0,
            "modulation": 1.0,
        },
        "sensitivity_matrix": {
            "matrix": _identity_6x6(),
            "determinant": 1.0,
            "catastrophic_transition": False,
        },
        "status": "IMPLEMENTED",
    }


def _expected_vacuum():
    expected_state = {
        "Mx": 0.0, "My": 0.0, "Mz": 0.0,
        "Ax": 0.0, "Ay": 0.0, "Az": 0.0,
        "cell_coordinate": None,
        "frame_index": None,
        "lifecycle_state": "ACTIVE",
        "mapping_version": "JUFE-LOCAL-1",
        "transformation": "Identity",
        "phase_difference": [0.0, 0.0, 0.0],
        "phase_equilibrium": True,
        "vacuum": True,
    }
    return {
        "state": expected_state,
        "gradient": {
            "gradient": (0.0, 0.0, 0.0),
            "propagation": (-0.0, -0.0, -0.0),
            "magnitude": 0.0,
            "gradient_dominance": False,
        },
        "phase": [0.0, 0.0, 0.0],
        "phase_lock": {
            "vacuum": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "packet": expected_state,
            "phase_locked": True,
        },
        "local_conservation": True,
        "equilibrium": True,
        "toroidal_flux": {
            "omega_t": 1.0,
            "geometry": 0.0,
            "xi": 0.0,
            "work": 0.0,
        },
        "tensegrity_tensor": {
            "geometry": 0.0,
            "structural_constraint": 1.0,
            "toroidal_flux": 0.0,
            "harmonic_modulation": 1.0,
            "total": 2.0,
            "divergence_free": False,
        },
        "stable": True,
        "global_conservation": {
            "global_sum": 0.0,
            "conserved": True,
            "residual": 0.0,
        },
        "harmonic_layer": {
            "harmonic": 0,
            "phase": 0.0,
            "modulation": 1.0,
        },
        "sensitivity_matrix": {
            "matrix": _identity_6x6(),
            "determinant": 1.0,
            "catastrophic_transition": False,
        },
        "status": "IMPLEMENTED",
    }


class DefaultOutputIdentityTests(unittest.TestCase):
    """
    Requirement 1 -- Default-output byte-for-byte identity.

    For the three six-component fixtures (no diagnostic kwargs), the
    short-input error, twelve values, and a non-multiple-of-six
    remainder, assert the full result equals today's golden result
    EXACTLY, including the absence of any "diagnostics" key.
    """

    def setUp(self):
        self.engine = ABTMEngine()

    def test_balanced_state_unchanged(self):
        result = self.engine.evaluate([3, 5, 2, 3, 5, 2])
        self.assertEqual(result, _expected_balanced())
        self.assertNotIn("diagnostics", result)

    def test_unbalanced_state_unchanged(self):
        result = self.engine.evaluate([3, 5, 2, 1, 4, 6])
        self.assertEqual(result, _expected_unbalanced())
        self.assertNotIn("diagnostics", result)

    def test_vacuum_state_unchanged(self):
        result = self.engine.evaluate([0, 0, 0, 0, 0, 0])
        self.assertEqual(result, _expected_vacuum())
        self.assertNotIn("diagnostics", result)

    def test_short_input_still_raises_identical_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.engine.evaluate([1, 2, 3])
        self.assertEqual(
            str(ctx.exception), "At least six values are required."
        )

    def test_twelve_values_unchanged(self):
        result = self.engine.evaluate(
            [3, 5, 2, 3, 5, 2, 3, 5, 2, 1, 4, 6]
        )
        self.assertEqual(
            sorted(result.keys()),
            [
                "complete_states",
                "global_conservation",
                "harmonic_layer",
                "remaining",
                "remaining_count",
                "sensitivity_matrix",
                "states",
                "status",
            ],
        )
        self.assertNotIn("diagnostics", result)
        self.assertEqual(result["complete_states"], 2)
        self.assertEqual(result["remaining"], [])
        self.assertEqual(result["remaining_count"], 0)
        self.assertEqual(
            result["global_conservation"],
            {"global_sum": 41.0, "conserved": False, "residual": 41.0},
        )

    def test_remainder_input_unchanged(self):
        result = self.engine.evaluate([3, 5, 2, 3, 5, 2, 7, 8, 9])
        self.assertNotIn("diagnostics", result)
        self.assertEqual(result["complete_states"], 1)
        self.assertEqual(result["remaining"], [7, 8, 9])
        self.assertEqual(result["remaining_count"], 3)
        self.assertEqual(
            result["global_conservation"],
            {"global_sum": 20.0, "conserved": False, "residual": 20.0},
        )


class IndividualDiagnosticRequestTests(unittest.TestCase):
    """
    Requirement 2 -- Each diagnostic requested individually.

    Four separate tests, one per kwarg: only that one diagnostic key
    appears under "diagnostics", and its value matches calling the
    underlying opt-in method directly with the same input/threshold.
    """

    def test_only_dominance_requested(self):
        engine = ABTMEngine()
        result = engine.evaluate([3, 5, 2, 1, 4, 6], dominance_threshold=1.0)

        self.assertEqual(list(result["diagnostics"].keys()), ["dominance"])

        transformed = _transformed([3, 5, 2, 1, 4, 6])
        expected = JUFEFieldGradient().evaluate_dominance(
            transformed, threshold=1.0
        )
        self.assertEqual(result["diagnostics"]["dominance"], expected)

    def test_only_phase_lock_requested(self):
        engine = ABTMEngine()
        result = engine.evaluate(
            [3, 5, 2, 1, 4, 6], phase_lock_tolerance=1.0
        )

        self.assertEqual(list(result["diagnostics"].keys()), ["phase_lock"])

        transformed = _transformed([3, 5, 2, 1, 4, 6])
        expected = JUFEPhaseLock().evaluate_phase_lock(
            transformed, tolerance=1.0
        )
        self.assertEqual(result["diagnostics"]["phase_lock"], expected)

    def test_only_global_balance_requested(self):
        engine = ABTMEngine()
        result = engine.evaluate(
            [3, 5, 2, 1, 4, 6], global_balance_tolerance=1e-9
        )

        self.assertEqual(
            list(result["diagnostics"].keys()), ["global_balance"]
        )

        transformed = _transformed([3, 5, 2, 1, 4, 6])
        expected = JUFEGlobalConservation().global_field_balance(
            [transformed], tolerance=1e-9
        )
        self.assertEqual(result["diagnostics"]["global_balance"], expected)

    def test_only_bifurcation_requested(self):
        engine = ABTMEngine()
        result = engine.evaluate(
            [3, 5, 2, 1, 4, 6], bifurcation_threshold=1e-9
        )

        self.assertEqual(
            list(result["diagnostics"].keys()), ["bifurcation"]
        )

        expected = JUFESensitivityMatrix().evaluate_bifurcation(
            threshold=1e-9
        )
        self.assertEqual(result["diagnostics"]["bifurcation"], expected)


class AllFourRequestedTogetherTests(unittest.TestCase):
    """
    Requirement 3 -- All four requested together.

    Verify all four appear, each matching the underlying opt-in method
    called directly.
    """

    def test_all_four_present_and_match_direct_calls(self):
        engine = ABTMEngine()
        result = engine.evaluate(
            [3, 5, 2, 1, 4, 6],
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
            global_balance_tolerance=1e-9,
            bifurcation_threshold=1e-9,
        )

        diagnostics = result["diagnostics"]
        self.assertEqual(
            set(diagnostics.keys()),
            {"dominance", "phase_lock", "global_balance", "bifurcation"},
        )

        transformed = _transformed([3, 5, 2, 1, 4, 6])

        self.assertEqual(
            diagnostics["dominance"],
            JUFEFieldGradient().evaluate_dominance(
                transformed, threshold=1.0
            ),
        )
        self.assertEqual(
            diagnostics["phase_lock"],
            JUFEPhaseLock().evaluate_phase_lock(transformed, tolerance=1.0),
        )
        self.assertEqual(
            diagnostics["global_balance"],
            JUFEGlobalConservation().global_field_balance(
                [transformed], tolerance=1e-9
            ),
        )
        self.assertEqual(
            diagnostics["bifurcation"],
            JUFESensitivityMatrix().evaluate_bifurcation(threshold=1e-9),
        )

        # Sample of the actual structure produced, for the report.
        self.assertIn("ratio", diagnostics["dominance"])
        self.assertIn("residual_norm", diagnostics["phase_lock"])
        self.assertIn("scalar_total", diagnostics["global_balance"])
        self.assertIn("determinant", diagnostics["bifurcation"])
        # The engine's canonical sensitivity matrix is a fixed 6x6
        # identity, so its determinant is always 1.0.
        self.assertEqual(diagnostics["bifurcation"]["determinant"], 1.0)

    def test_other_existing_fields_untouched_when_diagnostics_present(self):
        # "diagnostics" must be additive only -- everything else in the
        # single-state result must still equal the golden default.
        engine = ABTMEngine()
        result = engine.evaluate(
            [3, 5, 2, 1, 4, 6],
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
            global_balance_tolerance=1e-9,
            bifurcation_threshold=1e-9,
        )

        without_diagnostics = dict(result)
        del without_diagnostics["diagnostics"]

        self.assertEqual(without_diagnostics, _expected_unbalanced())


class SingleVersusMultiStateShapeTests(unittest.TestCase):
    """
    Requirement 4 -- Single-state vs multi-state response shape and
    ordering.

    Single-state: dominance/phase_lock are unwrapped single objects.
    Multi-state (12 values, two complete states): dominance/phase_lock
    are lists of length 2, in state order, each matching a direct
    per-state call.
    """

    def test_single_state_dominance_and_phase_lock_are_unwrapped(self):
        engine = ABTMEngine()
        result = engine.evaluate(
            [3, 5, 2, 1, 4, 6],
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
        )

        self.assertIsInstance(result["diagnostics"]["dominance"], dict)
        self.assertIsInstance(result["diagnostics"]["phase_lock"], dict)

    def test_multi_state_dominance_and_phase_lock_are_ordered_lists(self):
        engine = ABTMEngine()
        values = [3, 5, 2, 3, 5, 2, 3, 5, 2, 1, 4, 6]  # balanced + unbalanced
        result = engine.evaluate(
            values,
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
        )

        dominance_list = result["diagnostics"]["dominance"]
        phase_lock_list = result["diagnostics"]["phase_lock"]

        self.assertIsInstance(dominance_list, list)
        self.assertIsInstance(phase_lock_list, list)
        self.assertEqual(len(dominance_list), 2)
        self.assertEqual(len(phase_lock_list), 2)

        transformed_balanced = _transformed([3, 5, 2, 3, 5, 2])
        transformed_unbalanced = _transformed([3, 5, 2, 1, 4, 6])

        self.assertEqual(
            dominance_list[0],
            JUFEFieldGradient().evaluate_dominance(
                transformed_balanced, threshold=1.0
            ),
        )
        self.assertEqual(
            dominance_list[1],
            JUFEFieldGradient().evaluate_dominance(
                transformed_unbalanced, threshold=1.0
            ),
        )
        self.assertEqual(
            phase_lock_list[0],
            JUFEPhaseLock().evaluate_phase_lock(
                transformed_balanced, tolerance=1.0
            ),
        )
        self.assertEqual(
            phase_lock_list[1],
            JUFEPhaseLock().evaluate_phase_lock(
                transformed_unbalanced, tolerance=1.0
            ),
        )

        # Ordering sanity: state 0 is the balanced (locked) case, state
        # 1 is the unbalanced (not locked) case.
        self.assertTrue(phase_lock_list[0]["locked"])
        self.assertFalse(phase_lock_list[1]["locked"])

    def test_multi_state_global_balance_and_bifurcation_are_single_not_lists(self):
        engine = ABTMEngine()
        values = [3, 5, 2, 3, 5, 2, 3, 5, 2, 1, 4, 6]
        result = engine.evaluate(
            values,
            global_balance_tolerance=1e-9,
            bifurcation_threshold=1e-9,
        )

        self.assertIsInstance(result["diagnostics"]["global_balance"], dict)
        self.assertIsInstance(result["diagnostics"]["bifurcation"], dict)


class RemainderExclusionTests(unittest.TestCase):
    """
    Requirement 5 -- Remainder exclusion.

    Non-multiple-of-six input (9 values): diagnostics.global_balance
    (if requested) reflects only the complete state(s), excluding
    `remaining` -- matches the existing `global_conservation` field's
    scope exactly. State-level diagnostics (dominance/phase_lock) are
    only computed for the complete state, never for the remainder.
    """

    def test_global_balance_matches_global_conservation_scope(self):
        engine = ABTMEngine()
        values = [3, 5, 2, 3, 5, 2, 7, 8, 9]  # 1 complete state + [7, 8, 9]

        result = engine.evaluate(values, global_balance_tolerance=1e-9)

        # The existing global_conservation field already excludes the
        # remainder (this is unchanged, existing behavior); its
        # global_sum must equal diagnostics.global_balance's
        # scalar_total, since both are computed from the SAME
        # transformed_states list, excluding [7, 8, 9].
        self.assertEqual(
            result["global_conservation"]["global_sum"],
            result["diagnostics"]["global_balance"]["scalar_total"],
        )
        self.assertEqual(
            result["diagnostics"]["global_balance"]["scalar_total"], 20.0
        )

        transformed = _transformed([3, 5, 2, 3, 5, 2])
        expected = JUFEGlobalConservation().global_field_balance(
            [transformed], tolerance=1e-9
        )
        self.assertEqual(result["diagnostics"]["global_balance"], expected)

    def test_state_level_diagnostics_cover_only_the_complete_state(self):
        engine = ABTMEngine()
        values = [3, 5, 2, 3, 5, 2, 7, 8, 9]

        result = engine.evaluate(
            values,
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
        )

        self.assertEqual(len(result["states"]), 1)
        self.assertEqual(len(result["diagnostics"]["dominance"]), 1)
        self.assertEqual(len(result["diagnostics"]["phase_lock"]), 1)

        transformed = _transformed([3, 5, 2, 3, 5, 2])
        self.assertEqual(
            result["diagnostics"]["dominance"][0],
            JUFEFieldGradient().evaluate_dominance(transformed, threshold=1.0),
        )
        self.assertEqual(
            result["diagnostics"]["phase_lock"][0],
            JUFEPhaseLock().evaluate_phase_lock(transformed, tolerance=1.0),
        )

    def test_fifteen_value_input_diagnostics_cover_only_complete_states_and_ignore_remainder(self):
        # Two complete six-component states (12 values: balanced +
        # unbalanced) plus a 3-value remainder = 15 values total.
        engine = ABTMEngine()
        complete_values = [3, 5, 2, 3, 5, 2, 3, 5, 2, 1, 4, 6]
        remainder_a = [7, 8, 9]
        remainder_b = [10, 20, 30]  # different remainder content

        values_a = complete_values + remainder_a
        values_b = complete_values + remainder_b

        kwargs = dict(
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
            global_balance_tolerance=1e-9,
            bifurcation_threshold=1e-9,
        )

        result_a = engine.evaluate(values_a, **kwargs)
        result_b = engine.evaluate(values_b, **kwargs)

        # (1) The existing, already-covered remainder fields still
        # behave correctly for this 12+3 split.
        self.assertEqual(result_a["complete_states"], 2)
        self.assertEqual(result_a["remaining"], remainder_a)
        self.assertEqual(result_a["remaining_count"], 3)

        # (2) diagnostics.dominance / diagnostics.phase_lock are each
        # lists of exactly 2 results, in states[] order, each matching
        # a direct per-state call.
        transformed_balanced = _transformed([3, 5, 2, 3, 5, 2])
        transformed_unbalanced = _transformed([3, 5, 2, 1, 4, 6])

        dominance_list = result_a["diagnostics"]["dominance"]
        phase_lock_list = result_a["diagnostics"]["phase_lock"]
        self.assertEqual(len(dominance_list), 2)
        self.assertEqual(len(phase_lock_list), 2)
        self.assertEqual(
            dominance_list[0],
            JUFEFieldGradient().evaluate_dominance(
                transformed_balanced, threshold=1.0
            ),
        )
        self.assertEqual(
            dominance_list[1],
            JUFEFieldGradient().evaluate_dominance(
                transformed_unbalanced, threshold=1.0
            ),
        )
        self.assertEqual(
            phase_lock_list[0],
            JUFEPhaseLock().evaluate_phase_lock(
                transformed_balanced, tolerance=1.0
            ),
        )
        self.assertEqual(
            phase_lock_list[1],
            JUFEPhaseLock().evaluate_phase_lock(
                transformed_unbalanced, tolerance=1.0
            ),
        )

        # (3) diagnostics.global_balance reflects exactly the two
        # complete states, not the remainder.
        expected_global_balance = JUFEGlobalConservation().global_field_balance(
            [transformed_balanced, transformed_unbalanced], tolerance=1e-9
        )
        self.assertEqual(
            result_a["diagnostics"]["global_balance"], expected_global_balance
        )
        self.assertEqual(
            result_a["diagnostics"]["global_balance"]["scalar_total"], 41.0
        )

        # Prove it would differ if the 3 remainder values were
        # (incorrectly) included: pad them into a synthetic third
        # six-component state purely for this comparison (this is NOT
        # a claim about how the remainder should be handled -- it only
        # demonstrates that including it changes the result).
        incorrectly_included = _transformed([7, 8, 9, 0, 0, 0])
        incorrect_global_balance = JUFEGlobalConservation().global_field_balance(
            [transformed_balanced, transformed_unbalanced, incorrectly_included],
            tolerance=1e-9,
        )
        self.assertNotEqual(
            result_a["diagnostics"]["global_balance"], incorrect_global_balance
        )
        self.assertNotEqual(
            result_a["diagnostics"]["global_balance"]["scalar_total"],
            incorrect_global_balance["scalar_total"],
        )

        # (4) The remainder values appear ONLY in
        # remaining/remaining_count -- they do not appear in or
        # influence any diagnostic. Proven concretely: two 15-value
        # inputs sharing the same 12 leading values but a DIFFERENT
        # 3-value remainder must produce IDENTICAL diagnostics (only
        # "remaining" differs).
        self.assertEqual(result_a["diagnostics"], result_b["diagnostics"])
        self.assertNotEqual(result_a["remaining"], result_b["remaining"])
        self.assertEqual(result_b["remaining"], remainder_b)


class InvalidThresholdPropagationTests(unittest.TestCase):
    """
    Requirement 6 -- Invalid thresholds/tolerances propagate existing
    validation errors.

    e.g. dominance_threshold=-1 raises the same ValueError with the
    same message that evaluate_dominance itself raises; same for the
    other three.
    """

    def test_invalid_dominance_threshold_raises_same_error(self):
        engine = ABTMEngine()

        with self.assertRaises(ValueError) as via_evaluate:
            engine.evaluate([3, 5, 2, 1, 4, 6], dominance_threshold=-1)

        with self.assertRaises(ValueError) as via_direct:
            JUFEFieldGradient().evaluate_dominance(
                _transformed([3, 5, 2, 1, 4, 6]), threshold=-1
            )

        self.assertEqual(str(via_evaluate.exception), str(via_direct.exception))

    def test_invalid_phase_lock_tolerance_raises_same_error(self):
        engine = ABTMEngine()

        with self.assertRaises(ValueError) as via_evaluate:
            engine.evaluate([3, 5, 2, 1, 4, 6], phase_lock_tolerance=float("nan"))

        with self.assertRaises(ValueError) as via_direct:
            JUFEPhaseLock().evaluate_phase_lock(
                _transformed([3, 5, 2, 1, 4, 6]), tolerance=float("nan")
            )

        self.assertEqual(str(via_evaluate.exception), str(via_direct.exception))

    def test_invalid_global_balance_tolerance_raises_same_error(self):
        engine = ABTMEngine()

        with self.assertRaises(ValueError) as via_evaluate:
            engine.evaluate(
                [3, 5, 2, 1, 4, 6], global_balance_tolerance=float("inf")
            )

        with self.assertRaises(ValueError) as via_direct:
            JUFEGlobalConservation().global_field_balance(
                [_transformed([3, 5, 2, 1, 4, 6])], tolerance=float("inf")
            )

        self.assertEqual(str(via_evaluate.exception), str(via_direct.exception))

    def test_invalid_bifurcation_threshold_raises_same_error(self):
        engine = ABTMEngine()

        with self.assertRaises(ValueError) as via_evaluate:
            engine.evaluate([3, 5, 2, 1, 4, 6], bifurcation_threshold=-1)

        with self.assertRaises(ValueError) as via_direct:
            JUFESensitivityMatrix().evaluate_bifurcation(threshold=-1)

        self.assertEqual(str(via_evaluate.exception), str(via_direct.exception))


class JUFERuntimePassThroughTests(unittest.TestCase):
    """
    Requirement 7 -- JUFERuntime.evaluate() pass-through.

    All four kwargs, individually and together, produce identical
    results via JUFERuntime.evaluate(...) vs calling
    ABTMEngine.evaluate(...) directly with the same arguments.
    """

    def test_no_kwargs_pass_through_identically(self):
        runtime = JUFERuntime()
        engine = ABTMEngine()

        self.assertEqual(
            runtime.evaluate([3, 5, 2, 1, 4, 6]),
            engine.evaluate([3, 5, 2, 1, 4, 6]),
        )

    def test_each_kwarg_individually_passes_through_identically(self):
        cases = (
            {"dominance_threshold": 1.0},
            {"phase_lock_tolerance": 1.0},
            {"global_balance_tolerance": 1e-9},
            {"bifurcation_threshold": 1e-9},
        )

        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                runtime = JUFERuntime()
                engine = ABTMEngine()

                runtime_result = runtime.evaluate([3, 5, 2, 1, 4, 6], **kwargs)
                engine_result = engine.evaluate([3, 5, 2, 1, 4, 6], **kwargs)

                self.assertEqual(runtime_result, engine_result)

    def test_all_four_together_pass_through_identically(self):
        kwargs = {
            "dominance_threshold": 1.0,
            "phase_lock_tolerance": 1.0,
            "global_balance_tolerance": 1e-9,
            "bifurcation_threshold": 1e-9,
        }

        runtime = JUFERuntime()
        engine = ABTMEngine()

        runtime_result = runtime.evaluate([3, 5, 2, 1, 4, 6], **kwargs)
        engine_result = engine.evaluate([3, 5, 2, 1, 4, 6], **kwargs)

        self.assertEqual(runtime_result, engine_result)


class NonMutationTests(unittest.TestCase):
    """
    Requirement 8 -- No mutation.

    Input list/values unchanged after the call; engine instance
    re-usable/unchanged across calls (e.g. calling once with
    diagnostics then again without doesn't leak state).
    """

    def test_input_values_list_is_not_mutated(self):
        values = [3, 5, 2, 1, 4, 6]
        original = list(values)

        engine = ABTMEngine()
        engine.evaluate(
            values,
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
            global_balance_tolerance=1e-9,
            bifurcation_threshold=1e-9,
        )

        self.assertEqual(values, original)

    def test_engine_is_reusable_and_default_output_unaffected_by_prior_diagnostics_call(self):
        engine = ABTMEngine()

        # First call WITH diagnostics requested.
        with_diagnostics = engine.evaluate(
            [3, 5, 2, 1, 4, 6],
            dominance_threshold=1.0,
            phase_lock_tolerance=1.0,
            global_balance_tolerance=1e-9,
            bifurcation_threshold=1e-9,
        )
        self.assertIn("diagnostics", with_diagnostics)

        # Second call on the SAME engine instance, WITHOUT any
        # diagnostic kwargs -- must be identical to the golden default
        # and must NOT carry a "diagnostics" key or any leaked state
        # from the previous call.
        without_diagnostics = engine.evaluate([3, 5, 2, 1, 4, 6])

        self.assertNotIn("diagnostics", without_diagnostics)
        self.assertEqual(without_diagnostics, _expected_unbalanced())

    def test_sensitivity_matrix_instance_state_unchanged_after_bifurcation_call(self):
        engine = ABTMEngine()
        original_matrix = engine.sensitivity.matrix.copy()

        engine.evaluate([3, 5, 2, 1, 4, 6], bifurcation_threshold=1e-9)

        self.assertTrue(
            (engine.sensitivity.matrix == original_matrix).all()
        )


if __name__ == "__main__":
    unittest.main()
