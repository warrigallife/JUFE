"""
Characterization and parity tests for
``src/global_conservation.py :: JUFEGlobalConservation.global_field_balance``.

This new opt-in method is a native port of
``abtm_expansion.py :: ABTM_Expansion.global_field_balance`` (a
legacy/expansion module kept outside src/). It is added purely as an
additional capability on ``JUFEGlobalConservation``; nothing in
``ABTMEngine.evaluate()`` calls it, and the class's existing
``total_field``/``verify``/``residual``/``to_dict`` methods (and
``src/conservation.py``, a completely different file implementing the
unrelated local-state conservation check) are untouched.

Traced source of truth (read directly, not assumed)
-----------------------------------------------------

``abtm_expansion.py :: ABTM_Expansion.global_field_balance`` (paraphrased
here rather than pasted verbatim with its own triple-quoted docstring, to
avoid nesting one inside this module's docstring):

    def global_field_balance(self, compressive_fields, repulsive_fields,
                              *, tolerance=None) -> BalanceResult:
        m = self.as_array(compressive_fields, name="compressive_fields")
        a = self.as_array(repulsive_fields, name="repulsive_fields")
        if m.shape != a.shape:
            raise ValueError("compressive_fields and repulsive_fields "
                              "must have matching shapes.")
        if m.shape[-1] != 3:
            raise ValueError("The final axis must contain x, y, z "
                              "components.")
        tol = (self.equilibrium_tolerance if tolerance is None
               else self._positive_or_zero(tolerance, "tolerance"))
        combined = m + a
        reduction_axes = tuple(range(combined.ndim - 1))
        component_total = np.sum(combined, axis=reduction_axes)
        scalar_total = float(np.sum(component_total))
        return BalanceResult(
            scalar_total=scalar_total,
            component_total=np.asarray(component_total, dtype=float),
            tolerance=tol,
            scalar_balanced=bool(abs(scalar_total) <= tol),
            component_balanced=bool(np.linalg.norm(component_total) <= tol),
        )

- ``as_array`` additionally rejects empty arrays and non-finite entries.
- ``self.equilibrium_tolerance`` (default ``1e-9``) is the legacy
  fallback used ONLY when its own ``tolerance`` argument is omitted
  (``None``); an explicit ``tolerance`` is validated via
  ``_positive_or_zero`` (finite, >= 0), raising ``ValueError("tolerance
  must be a finite value greater than or equal to zero.")`` otherwise.
- Returns a frozen dataclass ``BalanceResult`` with five fields:
  ``scalar_total``, ``component_total`` (a NumPy array), ``tolerance``,
  ``scalar_balanced``, ``component_balanced``.

``src/global_conservation.py :: JUFEGlobalConservation.global_field_balance``
(the new method under test here) reproduces this exact rule and exact
validation order/messages natively, without importing
``abtm_expansion.py``, adapted to the ``states``-list calling convention
already used by every other method on ``JUFEGlobalConservation``
(``total_field(self, states)`` etc.): one row of the effective (N, 3)
compressive/repulsive arrays is taken from each state's own
``compressive``/``repulsive`` properties. Unlike the legacy version,
``tolerance`` here has NO default/fallback at all -- it is a required
keyword-only argument; omitting it raises Python's own
``TypeError: ... missing 1 required keyword-only argument: 'tolerance'``.
The returned value is a plain ``dict`` (matching this codebase's general
``to_dict()``-style convention) rather than a dataclass, and additionally
separates ``scalar_residual``/``component_residual`` (identical in value
to the totals, since the conservation target is exactly zero) and an
explicit ``"tolerance_basis": "PROVISIONAL"`` label, neither of which the
legacy ``BalanceResult`` carries.

This file imports ``abtm_expansion.py`` directly -- permitted for
comparison purposes in the TEST only; the constraint against importing
the legacy module at runtime applies to ``src/global_conservation.py``
itself, which does not do so.
"""

from __future__ import annotations

import unittest
from types import SimpleNamespace

import numpy as np

from abtm_expansion import ABTM_Expansion
from src.engines.abtm import ABTMEngine
from src.global_conservation import JUFEGlobalConservation
from src.local_state import JUFELocalState


def _state_double(compressive, repulsive):
    """
    A minimal Local-Field-State-like double exposing exactly the
    `compressive` / `repulsive` properties global_field_balance() reads,
    with no other JUFELocalState machinery -- used where a test needs
    deliberately malformed shapes that JUFELocalState's own constructor
    would never allow to exist in the first place.
    """

    return SimpleNamespace(compressive=tuple(compressive), repulsive=tuple(repulsive))


class ParityWithLegacyTests(unittest.TestCase):
    """
    Requirement 1 -- Parity with legacy.

    Compares JUFEGlobalConservation.global_field_balance() (the native
    src port) against ABTM_Expansion.global_field_balance() (the legacy
    implementation, imported here for comparison only) on fixed
    documented cases and 60 deterministic seeded generated collections
    of states (>= the required 50), reusing this session's established
    seeding convention: numpy with a fixed integer seed via
    np.random.default_rng(<fixed int>).
    """

    def _legacy_result(self, states, tolerance):
        expansion = ABTM_Expansion()
        compressive = np.array(
            [state.compressive for state in states], dtype=float
        )
        repulsive = np.array(
            [state.repulsive for state in states], dtype=float
        )
        return expansion.global_field_balance(
            compressive, repulsive, tolerance=tolerance
        )

    def _assert_matches_legacy(self, states, tolerance):
        gc = JUFEGlobalConservation()
        native_result = gc.global_field_balance(states, tolerance=tolerance)
        legacy_result = self._legacy_result(states, tolerance)

        self.assertEqual(native_result["scalar_total"], legacy_result.scalar_total)
        self.assertEqual(
            native_result["component_total"],
            [float(v) for v in legacy_result.component_total],
        )
        self.assertEqual(native_result["scalar_residual"], legacy_result.scalar_total)
        self.assertEqual(
            native_result["component_residual"],
            [float(v) for v in legacy_result.component_total],
        )
        self.assertEqual(native_result["tolerance"], legacy_result.tolerance)
        self.assertEqual(
            native_result["scalar_balanced"], legacy_result.scalar_balanced
        )
        self.assertEqual(
            native_result["component_balanced"], legacy_result.component_balanced
        )

    FIXED_CASES = (
        # (name, [(M, A), ...] per state, tolerance)
        (
            "single_balanced_state",
            [((3.0, 5.0, 2.0), (3.0, 5.0, 2.0))],
            1e-9,
        ),
        (
            "single_unbalanced_state",
            [((3.0, 5.0, 2.0), (1.0, 4.0, 6.0))],
            1e-9,
        ),
        (
            "two_states_vacuum",
            [((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)), ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))],
            1e-9,
        ),
        (
            "three_states_mixed",
            [
                ((3.0, 5.0, 2.0), (3.0, 5.0, 2.0)),
                ((1.0, -1.0, 0.0), (-1.0, 1.0, 0.0)),
                ((2.0, 2.0, 2.0), (-2.0, -2.0, -2.0)),
            ],
            0.5,
        ),
        (
            "loose_tolerance",
            [((10.0, -3.0, 4.0), (2.0, 2.0, 2.0))],
            100.0,
        ),
    )

    def test_fixed_cases_match_legacy_exactly(self):
        for name, pairs, tolerance in self.FIXED_CASES:
            with self.subTest(case=name):
                states = [
                    _state_double(m, a) for m, a in pairs
                ]
                self._assert_matches_legacy(states, tolerance)

    def test_generated_cases_match_legacy_exactly(self):
        seed = 20250301
        rng = np.random.default_rng(seed)
        collection_count = 60
        self.assertGreaterEqual(collection_count, 50)

        for index in range(collection_count):
            state_count = int(rng.integers(1, 6))  # 1..5 states
            states = []
            for _ in range(state_count):
                m = rng.integers(-9, 10, size=3)
                a = rng.integers(-9, 10, size=3)
                states.append(_state_double(m, a))
            tolerance = float(rng.uniform(0.0, 5.0))

            with self.subTest(index=index, state_count=state_count):
                self._assert_matches_legacy(states, tolerance)


class DivergentVerdictTests(unittest.TestCase):
    """
    Requirement 2 -- Divergent-verdict cases.

    Explicitly constructed cases proving scalar_balanced and
    component_balanced are genuinely independent results, not collapsed
    into one verdict. All four combinations are demonstrated:
    (True, True), (True, False), (False, True), (False, False).
    """

    def setUp(self):
        self.gc = JUFEGlobalConservation()

    def test_scalar_passes_component_fails(self):
        # Two states whose per-axis contributions cancel on sum
        # (scalar_total == 0) but whose component vector is far from
        # zero (component_total == [10, -10, 0], norm ~= 14.14).
        states = [
            _state_double((10.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
            _state_double((0.0, 0.0, 0.0), (0.0, -10.0, 0.0)),
        ]
        result = self.gc.global_field_balance(states, tolerance=1e-9)

        self.assertEqual(result["scalar_total"], 0.0)
        self.assertEqual(result["component_total"], [10.0, -10.0, 0.0])
        self.assertTrue(result["scalar_balanced"])
        self.assertFalse(result["component_balanced"])

    def test_component_passes_scalar_fails(self):
        # A single state whose component vector [0.5, 0.5, 0.5] has
        # L2 norm ~= 0.866, which IS within tolerance=1.0 (component
        # balanced), but whose scalar sum is 1.5, which is NOT within
        # the same tolerance=1.0 (scalar unbalanced). This is possible
        # because |sum(v)| <= sqrt(3) * ||v||_2, so a vector can be
        # small in norm while still summing to something larger than
        # the shared tolerance.
        states = [_state_double((0.5, 0.5, 0.5), (0.0, 0.0, 0.0))]
        result = self.gc.global_field_balance(states, tolerance=1.0)

        self.assertEqual(result["scalar_total"], 1.5)
        self.assertEqual(result["component_total"], [0.5, 0.5, 0.5])
        self.assertFalse(result["scalar_balanced"])
        self.assertTrue(result["component_balanced"])

    def test_both_pass(self):
        states = [
            _state_double((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
            _state_double((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        ]
        result = self.gc.global_field_balance(states, tolerance=1e-9)

        self.assertEqual(result["scalar_total"], 0.0)
        self.assertEqual(result["component_total"], [0.0, 0.0, 0.0])
        self.assertTrue(result["scalar_balanced"])
        self.assertTrue(result["component_balanced"])

    def test_both_fail(self):
        states = [_state_double((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))]
        result = self.gc.global_field_balance(states, tolerance=1e-9)

        self.assertEqual(result["scalar_total"], 6.0)
        self.assertEqual(result["component_total"], [2.0, 2.0, 2.0])
        self.assertFalse(result["scalar_balanced"])
        self.assertFalse(result["component_balanced"])

    def test_all_four_verdict_combinations_are_reachable(self):
        # Consolidates the four cases above into one explicit proof
        # that the two verdicts are never collapsed together.
        combinations_seen = set()

        cases = (
            ([_state_double((10.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
              _state_double((0.0, 0.0, 0.0), (0.0, -10.0, 0.0))], 1e-9),
            ([_state_double((0.5, 0.5, 0.5), (0.0, 0.0, 0.0))], 1.0),
            ([_state_double((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))], 1e-9),
            ([_state_double((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))], 1e-9),
        )
        for states, tolerance in cases:
            result = self.gc.global_field_balance(states, tolerance=tolerance)
            combinations_seen.add(
                (result["scalar_balanced"], result["component_balanced"])
            )

        self.assertEqual(
            combinations_seen,
            {(True, True), (True, False), (False, True), (False, False)},
        )


class ValidationTests(unittest.TestCase):
    """
    Requirement 3 -- Validation.

    Dimension mismatches, non-finite values, missing tolerance (raises,
    no default), and invalid tolerance -- exact exception type/message
    asserted for each, matching the legacy source's own conditions and
    message text (see module docstring above).
    """

    def setUp(self):
        self.gc = JUFEGlobalConservation()
        self.states = [
            _state_double((3.0, 5.0, 2.0), (3.0, 5.0, 2.0)),
        ]

    def test_empty_states_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance([], tolerance=1e-9)
        self.assertEqual(
            str(ctx.exception), "compressive_fields must not be empty."
        )

    def test_mismatched_compressive_repulsive_shape_within_state(self):
        # compressive has 3 components, repulsive has 4 -- a shape a
        # real JUFELocalState could never produce, constructed here via
        # the test double specifically to exercise this check.
        bad_state = SimpleNamespace(
            compressive=(1.0, 2.0, 3.0),
            repulsive=(1.0, 2.0, 3.0, 4.0),
        )
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance([bad_state], tolerance=1e-9)
        self.assertEqual(
            str(ctx.exception),
            "compressive_fields and repulsive_fields must have "
            "matching shapes.",
        )

    def test_non_three_component_vectors_raise_value_error(self):
        bad_state = _state_double((1.0, 2.0), (1.0, 2.0))
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance([bad_state], tolerance=1e-9)
        self.assertEqual(
            str(ctx.exception),
            "The final axis must contain x, y, z components.",
        )

    def test_non_finite_compressive_component_raises_value_error(self):
        bad_state = _state_double((1.0, float("inf"), 3.0), (1.0, 2.0, 3.0))
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance([bad_state], tolerance=1e-9)
        self.assertEqual(
            str(ctx.exception),
            "compressive_fields must contain only finite numbers.",
        )

    def test_non_finite_repulsive_component_raises_value_error(self):
        bad_state = _state_double((1.0, 2.0, 3.0), (1.0, float("nan"), 3.0))
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance([bad_state], tolerance=1e-9)
        self.assertEqual(
            str(ctx.exception),
            "repulsive_fields must contain only finite numbers.",
        )

    def test_missing_tolerance_raises_type_error(self):
        # No default exists for tolerance -- omitting it is a Python-
        # level missing-required-keyword-only-argument TypeError, not a
        # silently invented default.
        with self.assertRaises(TypeError):
            self.gc.global_field_balance(self.states)

    def test_negative_tolerance_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance(self.states, tolerance=-1.0)
        self.assertEqual(
            str(ctx.exception),
            "tolerance must be a finite value greater than or equal "
            "to zero.",
        )

    def test_nan_tolerance_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance(self.states, tolerance=float("nan"))
        self.assertEqual(
            str(ctx.exception),
            "tolerance must be a finite value greater than or equal "
            "to zero.",
        )

    def test_infinite_tolerance_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.gc.global_field_balance(self.states, tolerance=float("inf"))
        self.assertEqual(
            str(ctx.exception),
            "tolerance must be a finite value greater than or equal "
            "to zero.",
        )

    def test_zero_tolerance_is_explicitly_valid_not_an_error(self):
        # tolerance == 0 is the boundary of ">= 0" and must NOT raise.
        try:
            self.gc.global_field_balance(self.states, tolerance=0)
        except ValueError:
            self.fail("tolerance=0 must be accepted, not rejected.")


class NonMutationTests(unittest.TestCase):
    """
    Requirement 4 -- Non-mutation.

    Verifies the input states list (and each state's own
    compressive/repulsive values) is left completely unmodified by a
    global_field_balance() call.
    """

    def test_states_are_not_mutated(self):
        states = [
            JUFELocalState([3.0, 5.0, 2.0, 3.0, 5.0, 2.0]),
            JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0]),
        ]
        original_values = [list(state.values) for state in states]

        gc = JUFEGlobalConservation()
        gc.global_field_balance(states, tolerance=1e-9)

        self.assertEqual(
            [list(state.values) for state in states], original_values
        )

    def test_states_list_object_itself_is_unchanged(self):
        states = [
            JUFELocalState([3.0, 5.0, 2.0, 3.0, 5.0, 2.0]),
        ]
        original_list_identity = states
        original_length = len(states)

        gc = JUFEGlobalConservation()
        gc.global_field_balance(states, tolerance=1e-9)

        self.assertIs(states, original_list_identity)
        self.assertEqual(len(states), original_length)


class ProvisionalToleranceReportingTests(unittest.TestCase):
    """
    Requirement 5 -- Provisional-tolerance reporting.

    Asserts the returned structure explicitly carries the caller's
    tolerance value back AND the "provisional" label, as two distinct
    fields.
    """

    def test_tolerance_is_echoed_back_verbatim(self):
        gc = JUFEGlobalConservation()
        states = [_state_double((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))]

        result = gc.global_field_balance(states, tolerance=0.0037)

        self.assertIn("tolerance", result)
        self.assertEqual(result["tolerance"], 0.0037)

    def test_tolerance_basis_is_explicitly_labeled_provisional(self):
        gc = JUFEGlobalConservation()
        states = [_state_double((1.0, 1.0, 1.0), (1.0, 1.0, 1.0))]

        result = gc.global_field_balance(states, tolerance=1e-9)

        self.assertIn("tolerance_basis", result)
        self.assertEqual(result["tolerance_basis"], "PROVISIONAL")
        # The two fields are distinct keys, not merged into one.
        self.assertNotEqual("tolerance", "tolerance_basis")
        self.assertIn("tolerance", result)


class RegressionTests(unittest.TestCase):
    """
    Requirement 6 -- Regression.

    Confirms ABTMEngine.evaluate() output for the three baseline
    fixtures (balanced/unbalanced/vacuum) is byte-for-byte unchanged by
    the addition of global_field_balance() -- same technique as the
    "default unchanged" tests added for the coupled-field-step task:
    literal golden dicts captured from evaluate() output, independently
    transcribed, asserted via full-dict equality. (Whether the rest of
    the previously-existing 91 tests still pass is confirmed by running
    the complete suite alongside this file, not duplicated here.)
    """

    def setUp(self):
        self.engine = ABTMEngine()

    def _identity_6x6(self):
        return [
            [1.0 if row == col else 0.0 for col in range(6)]
            for row in range(6)
        ]

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
                "matrix": self._identity_6x6(),
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
                "matrix": self._identity_6x6(),
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
                "matrix": self._identity_6x6(),
                "determinant": 1.0,
                "catastrophic_transition": False,
            },
            "status": "IMPLEMENTED",
        }

        self.assertEqual(
            self.engine.evaluate([0, 0, 0, 0, 0, 0]), expected
        )


if __name__ == "__main__":
    unittest.main()
