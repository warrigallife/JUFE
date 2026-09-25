"""
Characterization and parity tests for
``src/sensitivity_matrix.py :: JUFESensitivityMatrix.evaluate_bifurcation``.

This new opt-in method is a native port of
``abtm_expansion.py :: ABTM_Expansion.detect_bifurcation`` (a
legacy/expansion module kept outside src/). It is added purely as an
additional capability on ``JUFESensitivityMatrix``; ``to_dict()`` does
not call it, nothing in ``ABTMEngine.evaluate()`` calls it, and the
class's existing ``apply``/``determinant``/``catastrophic_transition``/
``to_dict`` methods are untouched.

Traced source of truth (read directly, not assumed)
-----------------------------------------------------

``abtm_expansion.py :: ABTM_Expansion.detect_bifurcation`` (paraphrased
here rather than pasted verbatim with its own triple-quoted docstring,
to avoid nesting one inside this module's docstring)::

    def detect_bifurcation(self, sensitivity_matrix, *, threshold=None):
        # "Detect det(S) approaching zero."
        sensitivity = self.as_array(sensitivity_matrix, name="sensitivity_matrix")
        if sensitivity.ndim != 2 or sensitivity.shape[0] != sensitivity.shape[1]:
            raise ValueError("sensitivity_matrix must be square.")
        determinant = float(np.linalg.det(sensitivity))
        limit = (self.bifurcation_threshold if threshold is None
                 else self._positive_or_zero(threshold, "threshold"))
        return BifurcationResult(
            determinant=determinant,
            threshold=limit,
            near_bifurcation=bool(abs(determinant) <= limit),
        )

- The comparison is ``<=`` (less-than-or-EQUAL), not ``<`` -- confirmed
  by reading the exact source line, not assumed. A determinant whose
  absolute value exactly equals the threshold counts as
  near-bifurcation.
- ``threshold`` falls back to an instance-level ``bifurcation_threshold``
  (default ``1e-9``) when omitted (``None``); an explicit value is
  validated via ``_positive_or_zero`` (finite, >= 0), raising
  ``ValueError("threshold must be a finite value greater than or equal
  to zero.")`` otherwise.
- ``sensitivity_matrix`` may be any SQUARE matrix (not restricted to
  6x6) -- the legacy function itself imposes no 6x6 restriction; that
  restriction only exists on ``JUFESensitivityMatrix.__init__`` in
  src/sensitivity_matrix.py.

``src/sensitivity_matrix.py :: JUFESensitivityMatrix.evaluate_bifurcation``
(the new method under test here) reproduces this exact determinant/
threshold/comparison rule natively, without importing
``abtm_expansion.py``. Unlike the legacy version:
  - it takes no matrix argument at all -- it operates on ``self.matrix``,
    the same matrix every other method on this class already operates
    on, which ``__init__`` already restricts to exactly 6x6
    (``ValueError("Sensitivity matrix must be 6x6.")``). That existing
    restriction is reused as-is, not loosened;
  - ``threshold`` has NO default and NO legacy-style
    instance-level fallback -- it is a required keyword-only argument;
    omitting it raises Python's own
    ``TypeError: ... missing 1 required keyword-only argument: 'threshold'``;
  - the returned mapping carries an explicit ``"threshold_basis":
    "PROVISIONAL"`` label, citing DEF-0036 (Bifurcation Criterion,
    status "EXPLICIT LIMIT / UNRESOLVED THRESHOLD", which lists the
    "finite numerical threshold" as Unresolved) and REQ-TR-004
    (Bifurcation, status "explicit_with_convention", open_questions:
    ["Physically justified determinant threshold"]) -- both read
    directly from
    JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/MASTER_DEFINITION_INDEX.md
    and JUFE_ABTM_SPEC_ENGINE/requirements_register.json respectively,
    not paraphrased from memory.

This file imports ``abtm_expansion.py`` directly -- permitted for
comparison purposes in the TEST only; the constraint against importing
the legacy module at runtime applies to ``src/sensitivity_matrix.py``
itself, which does not do so.
"""

from __future__ import annotations

import unittest

import numpy as np

from abtm_expansion import ABTM_Expansion
from src.engines.abtm import ABTMEngine
from src.sensitivity_matrix import JUFESensitivityMatrix


def _identity_6x6():
    return [
        [1.0 if row == col else 0.0 for col in range(6)]
        for row in range(6)
    ]


class ParityWithLegacyTests(unittest.TestCase):
    """
    Requirement 1 -- Parity with legacy.

    Fixed documented 6x6 matrices (including singular and non-singular
    cases) plus 60 deterministic seeded valid 6x6 matrices (>= the
    required 50), comparing determinant + near-bifurcation boolean
    against ABTM_Expansion.detect_bifurcation() called directly.
    """

    def _assert_matches_legacy(self, matrix, threshold):
        sm = JUFESensitivityMatrix(matrix)
        native_result = sm.evaluate_bifurcation(threshold=threshold)

        expansion = ABTM_Expansion()
        legacy_result = expansion.detect_bifurcation(
            matrix, threshold=threshold
        )

        self.assertEqual(
            native_result["determinant"], legacy_result.determinant
        )
        self.assertEqual(native_result["threshold"], legacy_result.threshold)
        self.assertEqual(
            native_result["near_bifurcation"], legacy_result.near_bifurcation
        )

    FIXED_CASES = (
        # (name, 6x6 matrix, threshold)
        ("identity_far_from_bifurcation", np.identity(6), 1e-9),
        ("zero_matrix_singular", np.zeros((6, 6)), 1e-9),
        ("diagonal_nonsingular", np.diag([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), 1e-9),
        (
            "rank_deficient_singular",
            np.array(
                [
                    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                    [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],  # row 0 * 2 -> singular
                    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
                ]
            ),
            1e-9,
        ),
        ("small_diagonal_near_threshold", np.diag([1e-8] * 6), 1e-40),
        ("loose_threshold_identity", np.identity(6), 10.0),
    )

    def test_fixed_cases_match_legacy_exactly(self):
        for name, matrix, threshold in self.FIXED_CASES:
            with self.subTest(case=name):
                self._assert_matches_legacy(matrix, threshold)

    def test_generated_cases_match_legacy_exactly(self):
        seed = 20250401
        rng = np.random.default_rng(seed)
        count = 60
        self.assertGreaterEqual(count, 50)

        for index in range(count):
            matrix = rng.integers(-5, 6, size=(6, 6)).astype(float)
            threshold = float(rng.uniform(0.0, 10.0))

            with self.subTest(index=index):
                self._assert_matches_legacy(matrix, threshold)


class NearAndNonBifurcationResultTests(unittest.TestCase):
    """
    Requirement 2 -- Near-bifurcation and non-bifurcation results.

    Explicit cases of each, using the identity matrix (det=1, far from
    bifurcation under any reasonably small threshold) and the zero
    matrix (det=0, always near-bifurcation for any non-negative
    threshold).
    """

    def test_non_bifurcation_case(self):
        sm = JUFESensitivityMatrix(np.identity(6))
        result = sm.evaluate_bifurcation(threshold=1e-9)

        self.assertEqual(result["determinant"], 1.0)
        self.assertFalse(result["near_bifurcation"])

    def test_near_bifurcation_case(self):
        sm = JUFESensitivityMatrix(np.zeros((6, 6)))
        result = sm.evaluate_bifurcation(threshold=1e-9)

        self.assertEqual(result["determinant"], 0.0)
        self.assertTrue(result["near_bifurcation"])


class ThresholdBoundaryTests(unittest.TestCase):
    """
    Requirement 3 -- Exact threshold-boundary behavior.

    Confirms the legacy comparison is `abs(determinant) <= threshold`
    (less-than-or-EQUAL), by constructing a matrix whose determinant is
    exactly the chosen threshold and checking BOTH the native port and
    the legacy function agree that this boundary counts as
    near-bifurcation (a strict `<` comparison would report False here
    instead).
    """

    def test_determinant_exactly_equal_to_threshold_is_near_bifurcation(self):
        matrix = np.diag([2.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        sm = JUFESensitivityMatrix(matrix)
        determinant = sm.determinant()
        self.assertEqual(determinant, 2.0)

        result = sm.evaluate_bifurcation(threshold=determinant)
        self.assertTrue(
            result["near_bifurcation"],
            "abs(determinant) == threshold must count as near-bifurcation "
            "(the legacy comparison is <=, not <).",
        )

        expansion = ABTM_Expansion()
        legacy_result = expansion.detect_bifurcation(
            matrix, threshold=determinant
        )
        self.assertTrue(legacy_result.near_bifurcation)
        self.assertEqual(
            result["near_bifurcation"], legacy_result.near_bifurcation
        )

    def test_determinant_just_above_threshold_is_not_near_bifurcation(self):
        matrix = np.diag([2.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        sm = JUFESensitivityMatrix(matrix)
        determinant = sm.determinant()

        result = sm.evaluate_bifurcation(threshold=determinant - 1e-6)
        self.assertFalse(result["near_bifurcation"])


class SingularAndNonSingularMatrixTests(unittest.TestCase):
    """
    Requirement 4 -- Singular vs non-singular matrices.

    Both covered explicitly (beyond their appearance in the fixed-case
    parity table above), including checking the determinant sign/value
    used is correct in each case.
    """

    def test_singular_matrix_has_zero_determinant(self):
        singular = np.zeros((6, 6))
        sm = JUFESensitivityMatrix(singular)
        result = sm.evaluate_bifurcation(threshold=1e-9)

        self.assertEqual(result["determinant"], 0.0)
        self.assertTrue(result["near_bifurcation"])

    def test_non_singular_matrix_has_nonzero_determinant(self):
        non_singular = np.diag([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        sm = JUFESensitivityMatrix(non_singular)
        result = sm.evaluate_bifurcation(threshold=1e-9)

        # 1*2*3*4*5*6 = 720, but np.linalg.det's LU-decomposition-based
        # computation does not land on exactly 720.0 in floating point
        # (observed: 720.0000000000001) -- assertAlmostEqual accounts
        # for that ordinary floating-point rounding.
        self.assertAlmostEqual(result["determinant"], 720.0, places=9)
        self.assertFalse(result["near_bifurcation"])


class ThresholdValidationTests(unittest.TestCase):
    """
    Requirement 5 -- Threshold validation.

    Negative/NaN/infinite threshold rejected with exact exception
    type/message, matching the sign constraint implied by the legacy
    `abs(determinant) <= threshold` comparison (abs(...) is always
    non-negative, so a negative threshold could never be satisfied and
    is rejected explicitly).
    """

    def setUp(self):
        self.sm = JUFESensitivityMatrix()

    def test_negative_threshold_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.sm.evaluate_bifurcation(threshold=-1.0)
        self.assertEqual(
            str(ctx.exception),
            "threshold must be a finite value greater than or equal "
            "to zero.",
        )

    def test_nan_threshold_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.sm.evaluate_bifurcation(threshold=float("nan"))
        self.assertEqual(
            str(ctx.exception),
            "threshold must be a finite value greater than or equal "
            "to zero.",
        )

    def test_infinite_threshold_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.sm.evaluate_bifurcation(threshold=float("inf"))
        self.assertEqual(
            str(ctx.exception),
            "threshold must be a finite value greater than or equal "
            "to zero.",
        )

    def test_zero_threshold_is_explicitly_valid_not_an_error(self):
        try:
            self.sm.evaluate_bifurcation(threshold=0)
        except ValueError:
            self.fail("threshold=0 must be accepted, not rejected.")


class MissingThresholdBehaviorTests(unittest.TestCase):
    """
    Requirement 6 -- Missing-threshold behavior.

    Calling without `threshold` raises TypeError. This is documented as
    intentional -- DEF-0036 / REQ-TR-004 both record the determinant
    threshold as unresolved/not physically justified, so this method
    deliberately does not invent or fall back to any default value; the
    plain Python TypeError for a missing required keyword-only argument
    IS the expected behavior here, not a bug to be papered over.
    """

    def test_missing_threshold_raises_type_error(self):
        sm = JUFESensitivityMatrix()
        with self.assertRaises(TypeError):
            sm.evaluate_bifurcation()

    def test_missing_threshold_type_error_mentions_the_parameter(self):
        sm = JUFESensitivityMatrix()
        with self.assertRaises(TypeError) as ctx:
            sm.evaluate_bifurcation()
        self.assertIn("threshold", str(ctx.exception))


class ProvisionalLabelReportingTests(unittest.TestCase):
    """
    Requirement 7 -- Provisional-label reporting.

    Result carries the exact caller threshold AND
    threshold_basis: "PROVISIONAL" distinctly (two separate keys, not
    merged).
    """

    def test_threshold_is_echoed_back_verbatim(self):
        sm = JUFESensitivityMatrix()
        result = sm.evaluate_bifurcation(threshold=0.0042)

        self.assertIn("threshold", result)
        self.assertEqual(result["threshold"], 0.0042)

    def test_threshold_basis_is_explicitly_labeled_provisional(self):
        sm = JUFESensitivityMatrix()
        result = sm.evaluate_bifurcation(threshold=1e-9)

        self.assertIn("threshold_basis", result)
        self.assertEqual(result["threshold_basis"], "PROVISIONAL")
        # Two distinct keys, not collapsed into one.
        self.assertIn("threshold", result)
        self.assertNotEqual("threshold", "threshold_basis")

    def test_full_result_shape(self):
        sm = JUFESensitivityMatrix()
        result = sm.evaluate_bifurcation(threshold=0.25)

        self.assertEqual(
            set(result.keys()),
            {"determinant", "threshold", "threshold_basis", "near_bifurcation"},
        )


class NonMutationTests(unittest.TestCase):
    """
    Requirement 8 -- Non-mutation.

    Matrix/instance unchanged after the call.
    """

    def test_matrix_is_not_mutated(self):
        matrix = np.array(
            [
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 2.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 3.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 4.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 5.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 6.0],
            ]
        )
        sm = JUFESensitivityMatrix(matrix)
        original_matrix = sm.matrix.copy()

        sm.evaluate_bifurcation(threshold=1e-9)

        self.assertTrue(np.array_equal(sm.matrix, original_matrix))

    def test_instance_is_reusable_after_the_call(self):
        # A second, independent call with a different threshold must
        # produce a result consistent with the (unmutated) matrix.
        sm = JUFESensitivityMatrix(np.identity(6))

        first = sm.evaluate_bifurcation(threshold=1e-9)
        second = sm.evaluate_bifurcation(threshold=5.0)

        self.assertEqual(first["determinant"], second["determinant"])
        self.assertFalse(first["near_bifurcation"])
        self.assertTrue(second["near_bifurcation"])

    def test_original_matrix_argument_is_not_mutated(self):
        matrix = np.identity(6)
        original = matrix.copy()

        sm = JUFESensitivityMatrix(matrix)
        sm.evaluate_bifurcation(threshold=1e-9)

        self.assertTrue(np.array_equal(matrix, original))

    def test_existing_methods_still_behave_identically(self):
        # apply()/determinant()/catastrophic_transition()/to_dict() are
        # untouched -- confirmed by direct behavioral check here, in
        # addition to the full regression suite below.
        sm = JUFESensitivityMatrix()

        sm.evaluate_bifurcation(threshold=1.0)  # must not affect the below

        self.assertTrue(
            np.array_equal(sm.apply([1, 2, 3, 4, 5, 6]), [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
        )
        self.assertEqual(sm.determinant(), 1.0)
        self.assertFalse(sm.catastrophic_transition())
        self.assertEqual(
            sm.to_dict(),
            {
                "matrix": _identity_6x6(),
                "determinant": 1.0,
                "catastrophic_transition": False,
            },
        )


class RegressionTests(unittest.TestCase):
    """
    Requirement 9 -- Regression.

    Confirms ABTMEngine.evaluate() output for the three baseline
    fixtures (balanced/unbalanced/vacuum) is byte-for-byte unchanged by
    the addition of evaluate_bifurcation() -- same technique as the
    "default unchanged" tests from the two prior consolidation steps:
    literal golden dicts captured from evaluate() output, independently
    transcribed, asserted via full-dict equality. (Whether the rest of
    the previously-existing 115 tests still pass is confirmed by
    running the complete suite alongside this file, not duplicated
    here.)
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


if __name__ == "__main__":
    unittest.main()
