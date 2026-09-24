"""
Characterization and parity tests for
``src/transformation.py :: JUFETransformation.apply_coupled_field_step``.

This new opt-in method is a native port of the coupled-field evolution
rule implemented in the separate legacy/expansion module
``abtm_expansion.py :: ABTM_Expansion.coupled_field_step``. It is added
purely as an additional capability on ``JUFETransformation``; nothing in
``ABTMEngine.evaluate()`` calls it, and the class's existing default
``apply`` method (the identity mapping) is untouched.

Traced source of truth (read directly, not assumed)
-----------------------------------------------------

``abtm_expansion.py :: ABTM_Expansion.coupled_field_step``::

    @classmethod
    def coupled_field_step(
        cls,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
        compressive_rate: ArrayLike,
        *,
        dt: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        # Docstring (paraphrased here to avoid nesting a triple-quoted
        # string inside this module's own docstring):
        #   Advance one explicit time step under:
        #       dM/dt = -dA/dt
        #   Therefore:
        #       M_next = M + dM/dt * dt
        #       A_next = A - dM/dt * dt
        m = cls.as_array(compressive_field, name="compressive_field")
        a = cls.as_array(repulsive_field, name="repulsive_field")
        dm_dt = cls.as_array(compressive_rate, name="compressive_rate")

        if m.shape != a.shape or m.shape != dm_dt.shape:
            raise ValueError(
                "compressive_field, repulsive_field, and compressive_rate "
                "must have matching shapes."
            )

        time_step = float(dt)
        if not np.isfinite(time_step) or time_step < 0:
            raise ValueError("dt must be finite and non-negative.")

        delta = dm_dt * time_step
        return m + delta, a - delta

- ``cls.as_array`` (also in ``abtm_expansion.py``) additionally rejects
  empty arrays (``ValueError("<name> must not be empty.")``) and
  non-finite entries (``ValueError("<name> must contain only finite
  numbers.")``) before the shape check ever runs.
- ``dt`` is validated as finite and non-negative -- a negative ``dt`` is
  explicitly invalid, and ``dt == 0`` is explicitly valid (yields
  ``delta == 0``).
- The function returns a bare ``tuple`` of two NumPy arrays
  ``(m_next, a_next)`` -- it does not return or know about any Local
  Field State object.

``src/transformation.py :: JUFETransformation.apply_coupled_field_step``
(the new method under test here) reproduces this exact rule and exact
validation order/messages natively, without importing
``abtm_expansion.py``, but adapts the calling convention to match the
existing ``JUFETransformation.apply(self, state)`` method already on the
class: it is a regular instance method (not a ``classmethod``, unlike the
legacy version) that reads M and A from a supplied Local Field State's
``compressive``/``repulsive`` properties, and returns a new Local Field
State (via ``deepcopy``, exactly as ``apply`` already does) rather than a
bare tuple.

This file imports ``abtm_expansion.py`` directly -- that is permitted
for comparison purposes in the TEST only; the constraint against
importing the legacy module at runtime applies to
``src/transformation.py`` itself, which this file does not modify beyond
what was already ported.
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from abtm_expansion import ABTM_Expansion
from src.engines.abtm import ABTMEngine
from src.local_state import JUFELocalState
from src.transformation import JUFETransformation


def _identity_6x6():
    return [
        [1.0 if row == col else 0.0 for col in range(6)]
        for row in range(6)
    ]


class DefaultTransformationUnchangedTests(unittest.TestCase):
    """
    Requirement 1 -- Default unchanged.

    Proves that ABTMEngine.evaluate() (which internally calls only
    JUFETransformation.apply(), never the new
    apply_coupled_field_step()) still produces, value-for-value, the
    exact same output as the golden/snapshot baseline already captured
    for the three fixed fixtures in tests/test_abtm_evaluate_baseline.py
    (balanced [3,5,2,3,5,2], unbalanced [3,5,2,1,4,6], vacuum
    [0,0,0,0,0,0]). This file does not import or modify that other test
    file; the expected values below were independently captured from
    ABTMEngine.evaluate() BEFORE apply_coupled_field_step() was added
    (verified via `git stash` during development of this change: the
    pickled evaluate() output for all three fixtures compared equal,
    byte-for-byte, before and after editing src/transformation.py).
    """

    def setUp(self):
        self.engine = ABTMEngine()

    def test_balanced_state_output_unchanged(self):
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
        expected = {
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

        self.assertEqual(self.engine.evaluate([3, 5, 2, 3, 5, 2]), expected)

    def test_unbalanced_state_output_unchanged(self):
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
        expected = {
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

        self.assertEqual(self.engine.evaluate([3, 5, 2, 1, 4, 6]), expected)

    def test_vacuum_state_output_unchanged(self):
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
        expected = {
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

        self.assertEqual(
            self.engine.evaluate([0, 0, 0, 0, 0, 0]), expected
        )


class DtZeroIdentityTests(unittest.TestCase):
    """
    Requirement 2 -- dt=0 identity.

    Traced from source: delta = compressive_rate * dt, so dt == 0 always
    yields delta == 0 regardless of compressive_rate, and therefore
    M_next == M and A_next == A numerically. This is the only sense in
    which dt=0 is "identity" here: transformation provenance is still
    recorded as "CoupledFieldStep" (not "Identity"), since a step was
    still explicitly applied -- this is verified explicitly rather than
    assumed.
    """

    def test_dt_zero_leaves_compressive_and_repulsive_numerically_unchanged(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        transformation = JUFETransformation("Identity")

        new_state = transformation.apply_coupled_field_step(
            state,
            [7.0, -3.0, 100.0],
            dt=0,
        )

        self.assertEqual(new_state.compressive, state.compressive)
        self.assertEqual(new_state.repulsive, state.repulsive)
        self.assertEqual(new_state.values, state.values)

    def test_dt_zero_still_records_coupled_field_step_provenance(self):
        # dt=0 is numerically an identity on M/A, but it is NOT the same
        # code path as apply() -- provenance reflects that explicitly.
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        transformation = JUFETransformation("Identity")

        new_state = transformation.apply_coupled_field_step(
            state,
            [7.0, -3.0, 100.0],
            dt=0,
        )

        self.assertEqual(new_state.transformation, "CoupledFieldStep")
        self.assertEqual(state.transformation, None)


class NonzeroDtParityTests(unittest.TestCase):
    """
    Requirement 3 -- Nonzero dt parity.

    Compares JUFETransformation.apply_coupled_field_step() (the native
    src port) against ABTM_Expansion.coupled_field_step() (the legacy
    implementation, imported here for comparison only) on:
      - fixed, documented cases, and
      - 60 deterministic seeded generated cases (>= 50), reusing the
        same seeded-generation convention already established in
        tests/test_z6_equivalence.py: numpy with a fixed integer seed
        via np.random.default_rng(<fixed int>), since numpy is already
        a hard dependency of every implementation involved.
    """

    FIXED_CASES = (
        # (name, M, A, compressive_rate, dt)
        ("balanced_unit_rate", [3, 5, 2, 3, 5, 2], [1.0, 1.0, 1.0], 1.0),
        ("unbalanced_fractional_dt", [3, 5, 2, 1, 4, 6], [0.5, -1.5, 2.0], 0.25),
        ("vacuum_nonzero_rate", [0, 0, 0, 0, 0, 0], [4.0, -4.0, 0.0], 3.0),
        ("large_dt", [3, 5, 2, 3, 5, 2], [1.5, -2.0, 0.25], 2.0),
        ("zero_rate_nonzero_dt", [3, 5, 2, 1, 4, 6], [0.0, 0.0, 0.0], 10.0),
    )

    def _compare(self, state_values, rate, dt):
        state = JUFELocalState([float(v) for v in state_values])
        transformation = JUFETransformation("Identity")

        new_state = transformation.apply_coupled_field_step(
            state, rate, dt=dt
        )
        m_next, a_next = ABTM_Expansion.coupled_field_step(
            state.compressive,
            state.repulsive,
            rate,
            dt=dt,
        )

        self.assertTrue(
            np.array_equal(np.array(new_state.compressive), m_next),
            f"M mismatch: {new_state.compressive} vs {m_next}",
        )
        self.assertTrue(
            np.array_equal(np.array(new_state.repulsive), a_next),
            f"A mismatch: {new_state.repulsive} vs {a_next}",
        )

    def test_fixed_cases_match_legacy_exactly(self):
        for name, state_values, rate, dt in self.FIXED_CASES:
            with self.subTest(case=name):
                self._compare(state_values, rate, dt)

    def test_generated_cases_match_legacy_exactly(self):
        seed = 20250101
        rng = np.random.default_rng(seed)
        count = 60
        self.assertGreaterEqual(count, 50)

        for index in range(count):
            m = rng.integers(-9, 10, size=3)
            a = rng.integers(-9, 10, size=3)
            rate = rng.uniform(-5.0, 5.0, size=3)
            dt = float(rng.uniform(0.0, 5.0))

            with self.subTest(index=index):
                self._compare(list(m) + list(a), rate, dt)


class ConservationRelationTests(unittest.TestCase):
    """
    Requirement 4 -- Delta M = -Delta A component-wise.

    Verifies, directly from the outputs of apply_coupled_field_step(),
    that (M_next - M) == -(A_next - A) component-wise. Internally, delta
    is computed once and applied with a plain sign flip
    (M + delta, A - delta), so the relationship holds exactly at the
    point of computation; but re-deriving delta_m/delta_a here via a
    second, independent subtraction (new_state - original_state) can
    differ from that internal delta by ordinary floating-point rounding
    when M/A have a different magnitude than delta, so a tight numeric
    tolerance (not bit-exact equality) is used for the float-valued
    generated cases below. The fixed integer-valued case is checked
    exactly, since integers up to this magnitude are exactly
    representable and no rounding occurs.
    """

    def test_delta_m_equals_negative_delta_a_fixed_case(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 3.0, 5.0, 2.0])
        transformation = JUFETransformation("Identity")

        new_state = transformation.apply_coupled_field_step(
            state,
            [1.5, -2.0, 0.25],
            dt=2.0,
        )

        delta_m = np.array(new_state.compressive) - np.array(state.compressive)
        delta_a = np.array(new_state.repulsive) - np.array(state.repulsive)

        self.assertTrue(np.array_equal(delta_m, -delta_a))

    def test_delta_m_equals_negative_delta_a_generated_cases(self):
        rng = np.random.default_rng(20250102)

        for index in range(50):
            m = rng.integers(-9, 10, size=3)
            a = rng.integers(-9, 10, size=3)
            rate = rng.uniform(-5.0, 5.0, size=3)
            dt = float(rng.uniform(0.0, 5.0))

            state = JUFELocalState(
                [float(v) for v in list(m) + list(a)]
            )
            transformation = JUFETransformation("Identity")
            new_state = transformation.apply_coupled_field_step(
                state, rate, dt=dt
            )

            delta_m = (
                np.array(new_state.compressive) - np.array(state.compressive)
            )
            delta_a = (
                np.array(new_state.repulsive) - np.array(state.repulsive)
            )

            with self.subTest(index=index):
                self.assertTrue(
                    np.allclose(delta_m, -delta_a, rtol=1e-9, atol=1e-9),
                    f"delta_m={delta_m} vs -delta_a={-delta_a}",
                )


class InvalidInputHandlingTests(unittest.TestCase):
    """
    Requirement 5 -- Invalid input handling.

    From the trace in the module docstring above, "invalid" means
    exactly what abtm_expansion.py's coupled_field_step /
    ABTM_Expansion.as_array define as invalid:
      - compressive_rate is empty
      - compressive_rate contains non-finite values
      - compressive_rate's shape does not match the (always
        three-component) compressive/repulsive shape
      - dt is not finite (NaN or +/-inf)
      - dt is negative

    (compressive_field/repulsive_field can only become empty or
    non-finite here if the supplied `state` object itself is malformed,
    since JUFELocalState's own constructor already rejects non-finite
    values and always produces exactly three-component M/A vectors; the
    reachable invalid-input surface for a normal caller is
    compressive_rate and dt, exercised below.)
    """

    def setUp(self):
        self.state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        self.transformation = JUFETransformation("Identity")

    def test_negative_dt_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.transformation.apply_coupled_field_step(
                self.state, [1.0, 1.0, 1.0], dt=-0.5
            )
        self.assertEqual(
            str(ctx.exception), "dt must be finite and non-negative."
        )

    def test_nan_dt_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.transformation.apply_coupled_field_step(
                self.state, [1.0, 1.0, 1.0], dt=float("nan")
            )
        self.assertEqual(
            str(ctx.exception), "dt must be finite and non-negative."
        )

    def test_infinite_dt_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.transformation.apply_coupled_field_step(
                self.state, [1.0, 1.0, 1.0], dt=float("inf")
            )
        self.assertEqual(
            str(ctx.exception), "dt must be finite and non-negative."
        )

    def test_mismatched_rate_shape_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.transformation.apply_coupled_field_step(
                self.state, [1.0, 2.0], dt=1.0
            )
        self.assertEqual(
            str(ctx.exception),
            "compressive_field, repulsive_field, and compressive_rate "
            "must have matching shapes.",
        )

    def test_empty_rate_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.transformation.apply_coupled_field_step(
                self.state, [], dt=1.0
            )
        self.assertEqual(
            str(ctx.exception), "compressive_rate must not be empty."
        )

    def test_nonfinite_rate_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.transformation.apply_coupled_field_step(
                self.state, [1.0, float("inf"), 3.0], dt=1.0
            )
        self.assertEqual(
            str(ctx.exception),
            "compressive_rate must contain only finite numbers.",
        )

    def test_dt_zero_is_explicitly_valid_not_an_error(self):
        # dt == 0 is the boundary of "non-negative" and must NOT raise.
        try:
            self.transformation.apply_coupled_field_step(
                self.state, [1.0, 1.0, 1.0], dt=0
            )
        except ValueError:
            self.fail("dt=0 must be accepted, not rejected.")


class NoMutationTests(unittest.TestCase):
    """
    Requirement 6 -- No mutation.

    Verifies the original input state object passed to
    apply_coupled_field_step() is left completely unmodified: same
    values, same component attributes, same (unset) transformation
    provenance, and a genuinely distinct object from the one returned.
    """

    def test_original_state_is_not_mutated(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])

        original_values = list(state.values)
        original_compressive = state.compressive
        original_repulsive = state.repulsive
        original_transformation = state.transformation

        transformation = JUFETransformation("Identity")
        new_state = transformation.apply_coupled_field_step(
            state,
            [7.0, -3.0, 100.0],
            dt=5.0,
        )

        # The original object's own attributes are unchanged.
        self.assertEqual(state.values, original_values)
        self.assertEqual(state.compressive, original_compressive)
        self.assertEqual(state.repulsive, original_repulsive)
        self.assertEqual(state.transformation, original_transformation)
        self.assertIsNone(state.transformation)

        # The returned state is a genuinely different object, not the
        # same instance mutated in place.
        self.assertIsNot(new_state, state)
        self.assertNotEqual(new_state.values, state.values)

    def test_compressive_rate_argument_is_not_mutated(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        transformation = JUFETransformation("Identity")

        rate = np.array([7.0, -3.0, 100.0])
        rate_copy_before = rate.copy()

        transformation.apply_coupled_field_step(state, rate, dt=5.0)

        self.assertTrue(np.array_equal(rate, rate_copy_before))


if __name__ == "__main__":
    unittest.main()
