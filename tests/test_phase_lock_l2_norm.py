"""
Characterization and parity tests for
``src/phase_lock.py :: JUFEPhaseLock.evaluate_phase_lock``.

This new opt-in method is a native port of
``abtm_expansion.py :: ABTM_Expansion.phase_lock`` (a legacy/expansion
module kept outside src/). It is added purely as an additional
capability on ``JUFEPhaseLock``; nothing in ``ABTMEngine.evaluate()``
calls it, ``eject()`` does not call it, and the class's existing
``locked``/``harmonic_packet``/``vacuum_state``/``eject`` methods are
untouched. It also does not touch ``JUFEHarmonicLayer``, ``mod7_phase``,
harmonic packets, vacuum representation, lifecycle logic, or topology.

Traced source of truth (read directly, not assumed)
-----------------------------------------------------

``abtm_expansion.py :: ABTM_Expansion.phase_lock`` (paraphrased here
rather than pasted verbatim with its own triple-quoted docstring, to
avoid nesting one inside this module's docstring)::

    def phase_lock(self, compressive_field, repulsive_field, *, tolerance=None):
        # "Check ||M - A|| <= tolerance."
        m = self.as_array(compressive_field, name="compressive_field")
        a = self.as_array(repulsive_field, name="repulsive_field")
        if m.shape != a.shape:
            raise ValueError("compressive_field and repulsive_field "
                              "must have matching shapes.")
        tol = (self.phase_lock_tolerance if tolerance is None
               else self._positive_or_zero(tolerance, "tolerance"))
        residual = m - a
        residual_norm = float(np.linalg.norm(residual))
        return PhaseLockResult(
            residual=residual,
            residual_norm=residual_norm,
            tolerance=tol,
            locked=bool(residual_norm <= tol),
        )

Confirmed directly from source (not assumed): the comparison is ``<=``
(less-than-or-EQUAL), matching ``bool(residual_norm <= tol)`` exactly.

``src/phase_lock.py :: JUFEPhaseLock.evaluate_phase_lock`` (the new
method under test here) reproduces this exact residual, L2-norm
computation, and ``<=`` comparison natively, without importing
``abtm_expansion.py``. Differences from the legacy source, all
deliberate and documented in the method's own docstring:
  - it takes a single ``state`` object (reading ``state.compressive``
    and ``state.repulsive``) rather than two separate array arguments;
  - ``tolerance`` has NO default (the legacy version falls back to an
    instance-level ``phase_lock_tolerance`` of ``1e-9`` when omitted;
    this port does not reproduce that fallback -- it is required and
    keyword-only);
  - the returned mapping carries an explicit
    ``"tolerance_basis": "PROVISIONAL"`` label, citing REQ-TR-002 and
    TR-PHASE-001 (see below), which the legacy ``PhaseLockResult``
    dataclass does not carry.

REQ-TR-002 and TR-PHASE-001 (exact wording, read directly, not
paraphrased from memory)
------------------------------------------------------------------------

From ``JUFE_ABTM_SPEC_ENGINE/requirements_register.json``:

    REQ-TR-002, category "transition", title "Phase lock"
    manuscript_statement: "lim_(t->t_lock)(M(t)-A(t))=0."
    software_requirement: "Calculate ||M-A|| and compare with a
        declared tolerance."
    status: "explicit_with_convention"
    implemented_by: ["abtm_expansion.ABTM_Expansion.phase_lock"]
    open_questions: ["Physical basis of numerical tolerance"]

From ``JUFE_ABTM_SPEC_LAYER/abtm_specification.py`` (and the
generated/mirrored ``JUFE_ABTM_SPEC_LAYER/JUFE_ABTM_CORE_SPEC.json``):

    TR-PHASE-001, title "Phase-lock condition", kind TRANSITION,
    status EXPLICIT
    mathematical_form: "lim_(t->t_lock)(M(t) - A(t)) = 0"
    description: "A local cell enters phase lock when compressive and
        repulsive field states converge."
    required_inputs: ("M", "A", "phase_lock_tolerance")
    outputs: ("phase_error", "locked")
    software_contract: ("Calculate the residual M - A.",
        "Use a declared tolerance and include it in every audit.")
    source_section: "2.2 Phase-Lock and Ejection Mechanics"

The mathematical relationship to
``JUFELocalState.is_phase_equilibrium_with_tolerance(tolerance)``
(traced directly from ``src/local_state.py``): that method returns
``all(abs(component) <= tolerance for component in phase_difference())``
-- an L-infinity (per-component / max-norm) criterion, NOT an L2-norm
criterion. The two are provably NOT equivalent:
  - L2-pass ALWAYS implies L-infinity-pass (each component's absolute
    value can never exceed the vector's own L2 norm), so
    ``residual_norm <= tolerance`` guarantees
    ``all(abs(component) <= tolerance ...)``.
  - L-infinity-pass does NOT imply L2-pass: a three-component residual
    of ``(tolerance, tolerance, tolerance)`` satisfies the
    per-component check exactly, but has L2 norm
    ``tolerance * sqrt(3) ~= 1.732 * tolerance``, which exceeds
    ``tolerance`` for any ``tolerance > 0``.

So the only reachable divergence is: a state can pass
``is_phase_equilibrium_with_tolerance()`` while FAILING
``evaluate_phase_lock()``'s ``locked`` result. The reverse direction is
mathematically impossible and is not attempted here.

This file imports ``abtm_expansion.py`` directly -- permitted for
comparison purposes in the TEST only; the constraint against importing
the legacy module at runtime applies to ``src/phase_lock.py`` itself,
which does not do so.
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from abtm_expansion import ABTM_Expansion
from src.engines.abtm import ABTMEngine
from src.local_state import JUFELocalState
from src.phase_lock import JUFEPhaseLock


def _identity_6x6():
    return [
        [1.0 if row == col else 0.0 for col in range(6)]
        for row in range(6)
    ]


class ParityWithLegacyTests(unittest.TestCase):
    """
    Requirement 1 -- Parity with legacy.

    Fixed documented six-component states plus 60 deterministic seeded
    valid six-component states (>= the required 50) with caller-supplied
    tolerances, comparing residual/residual_norm/locked against
    ABTM_Expansion.phase_lock called directly.
    """

    def _assert_matches_legacy(self, state_values, tolerance):
        state = JUFELocalState([float(v) for v in state_values])
        pl = JUFEPhaseLock()

        native_result = pl.evaluate_phase_lock(state, tolerance=tolerance)

        expansion = ABTM_Expansion()
        legacy_result = expansion.phase_lock(
            state.compressive, state.repulsive, tolerance=tolerance
        )

        self.assertEqual(
            native_result["residual"],
            [float(v) for v in legacy_result.residual],
        )
        self.assertEqual(
            native_result["residual_norm"], legacy_result.residual_norm
        )
        self.assertEqual(native_result["tolerance"], legacy_result.tolerance)
        self.assertEqual(native_result["locked"], legacy_result.locked)

    FIXED_CASES = (
        # (name, six values, tolerance)
        ("balanced_state", [3, 5, 2, 3, 5, 2], 1e-9),
        ("unbalanced_state", [3, 5, 2, 1, 4, 6], 1.0),
        ("vacuum_state", [0, 0, 0, 0, 0, 0], 1e-9),
        ("small_residual_loose_tolerance", [1, 1, 1, 0.9, 0.9, 0.9], 1.0),
        ("large_residual_tight_tolerance", [10, -10, 5, -5, 10, -10], 1e-6),
    )

    def test_fixed_cases_match_legacy_exactly(self):
        for name, values, tolerance in self.FIXED_CASES:
            with self.subTest(case=name):
                self._assert_matches_legacy(values, tolerance)

    def test_generated_cases_match_legacy_exactly(self):
        seed = 20250601
        rng = np.random.default_rng(seed)
        count = 60
        self.assertGreaterEqual(count, 50)

        for index in range(count):
            values = rng.integers(-9, 10, size=6)
            tolerance = float(rng.uniform(0.0, 10.0))

            with self.subTest(index=index):
                self._assert_matches_legacy(values, tolerance)


class LockedUnlockedBoundaryTests(unittest.TestCase):
    """
    Requirement 2 -- Locked / unlocked / exact-boundary cases.

    The boundary case confirms the comparison is `<=`, not `<` (a
    strict `<` would report locked=False at the exact boundary
    instead).
    """

    def setUp(self):
        self.pl = JUFEPhaseLock()

    def test_locked_case(self):
        # residual = (0.5, 0, 0), norm = 0.5, tolerance = 1.0
        state = JUFELocalState([0.5, 0.0, 0.0, 0.0, 0.0, 0.0])
        result = self.pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertEqual(result["residual_norm"], 0.5)
        self.assertTrue(result["locked"])

    def test_unlocked_case(self):
        # residual = (5, 0, 0), norm = 5, tolerance = 1.0
        state = JUFELocalState([5.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        result = self.pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertEqual(result["residual_norm"], 5.0)
        self.assertFalse(result["locked"])

    def test_exact_boundary_case_is_locked(self):
        # residual = (1, 0, 0), norm == tolerance == 1.0 exactly.
        state = JUFELocalState([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        result = self.pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertEqual(result["residual_norm"], 1.0)
        self.assertTrue(
            result["locked"],
            "residual_norm == tolerance must count as locked (the "
            "comparison is <=, not <).",
        )

        expansion = ABTM_Expansion()
        legacy_result = expansion.phase_lock(
            state.compressive, state.repulsive, tolerance=1.0
        )
        self.assertTrue(legacy_result.locked)
        self.assertEqual(result["locked"], legacy_result.locked)


class DivergenceFromComponentWiseCriterionTests(unittest.TestCase):
    """
    Requirement 3 -- Divergence from the component-wise criterion.

    As traced in the module docstring above, only one divergent
    direction is mathematically reachable: a state can pass
    JUFELocalState.is_phase_equilibrium_with_tolerance()'s per-component
    (L-infinity) check while FAILING evaluate_phase_lock()'s L2-norm
    check. The reverse direction (L2 passes, per-component fails) is
    proven impossible above and is not attempted here -- forcing it
    would require a false result.
    """

    def test_component_wise_passes_but_l2_norm_fails(self):
        # residual = (1, 1, 1), tolerance = 1.0.
        # Per-component: every |component| == 1.0 <= 1.0 -> passes.
        # L2 norm: sqrt(3) ~= 1.732 > 1.0 -> fails.
        state = JUFELocalState([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
        tolerance = 1.0

        component_wise_result = state.is_phase_equilibrium_with_tolerance(
            tolerance
        )
        self.assertTrue(
            component_wise_result,
            "Fixture setup error: expected the per-component check to "
            "pass for this case.",
        )

        pl = JUFEPhaseLock()
        l2_result = pl.evaluate_phase_lock(state, tolerance=tolerance)

        self.assertAlmostEqual(
            l2_result["residual_norm"], math.sqrt(3), places=9
        )
        self.assertFalse(
            l2_result["locked"],
            "Expected the L2-norm check to fail here, demonstrating "
            "genuine divergence from the per-component check that "
            "passed above.",
        )

    def test_l2_pass_always_implies_component_wise_pass_generated(self):
        # Confirms the OTHER direction of the proven relationship: for
        # 60 deterministic generated cases, whenever the L2 check
        # passes, the per-component check must also pass (never the
        # reverse-failure), backing up the docstring's mathematical
        # claim empirically as well as by proof.
        seed = 20250602
        rng = np.random.default_rng(seed)

        for index in range(60):
            values = rng.integers(-9, 10, size=6)
            tolerance = float(rng.uniform(0.0, 10.0))
            state = JUFELocalState([float(v) for v in values])

            pl = JUFEPhaseLock()
            l2_result = pl.evaluate_phase_lock(state, tolerance=tolerance)
            component_wise_result = state.is_phase_equilibrium_with_tolerance(
                tolerance
            )

            with self.subTest(index=index):
                if l2_result["locked"]:
                    self.assertTrue(
                        component_wise_result,
                        "L2-locked must imply component-wise-locked; "
                        "found a counterexample, which would disprove "
                        "the claimed mathematical relationship.",
                    )


class ZeroResidualTests(unittest.TestCase):
    """
    Requirement 4 -- Zero residual.

    M == A exactly: residual_norm == 0, locked true for any valid
    (non-negative) tolerance, including tolerance == 0.
    """

    def test_zero_residual_when_m_equals_a(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 3.0, 5.0, 2.0])
        pl = JUFEPhaseLock()

        result = pl.evaluate_phase_lock(state, tolerance=0.0)

        self.assertEqual(result["residual"], [0.0, 0.0, 0.0])
        self.assertEqual(result["residual_norm"], 0.0)
        self.assertTrue(result["locked"])

    def test_zero_residual_locked_for_any_nonnegative_tolerance(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 3.0, 5.0, 2.0])
        pl = JUFEPhaseLock()

        for tolerance in (0.0, 1e-12, 1.0, 1000.0):
            with self.subTest(tolerance=tolerance):
                result = pl.evaluate_phase_lock(state, tolerance=tolerance)
                self.assertTrue(result["locked"])


class MissingToleranceBehaviorTests(unittest.TestCase):
    """
    Requirement 5 -- Missing-tolerance behavior.

    Omitting tolerance raises TypeError. Documented as intentional:
    REQ-TR-002 records the physical basis of the numerical tolerance as
    an open question, so no default is invented.
    """

    def test_missing_tolerance_raises_type_error(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        pl = JUFEPhaseLock()

        with self.assertRaises(TypeError):
            pl.evaluate_phase_lock(state)

    def test_missing_tolerance_type_error_mentions_the_parameter(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        pl = JUFEPhaseLock()

        with self.assertRaises(TypeError) as ctx:
            pl.evaluate_phase_lock(state)
        self.assertIn("tolerance", str(ctx.exception))


class ToleranceValidationTests(unittest.TestCase):
    """
    Requirement 6 -- Tolerance validation.

    Negative, NaN, infinite tolerance all rejected with exact exception
    type/message; tolerance=0 explicitly accepted.
    """

    def setUp(self):
        self.state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        self.pl = JUFEPhaseLock()

    def test_negative_tolerance_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.pl.evaluate_phase_lock(self.state, tolerance=-1.0)
        self.assertEqual(
            str(ctx.exception),
            "tolerance must be a finite value greater than or equal "
            "to zero.",
        )

    def test_nan_tolerance_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.pl.evaluate_phase_lock(self.state, tolerance=float("nan"))
        self.assertEqual(
            str(ctx.exception),
            "tolerance must be a finite value greater than or equal "
            "to zero.",
        )

    def test_infinite_tolerance_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.pl.evaluate_phase_lock(self.state, tolerance=float("inf"))
        self.assertEqual(
            str(ctx.exception),
            "tolerance must be a finite value greater than or equal "
            "to zero.",
        )

    def test_zero_tolerance_is_explicitly_valid_not_an_error(self):
        try:
            self.pl.evaluate_phase_lock(self.state, tolerance=0)
        except ValueError:
            self.fail("tolerance=0 must be accepted, not rejected.")


class ProvisionalLabelReportingTests(unittest.TestCase):
    """
    Requirement 7 -- Provisional-label reporting.

    Result carries the exact caller tolerance and
    tolerance_basis == "PROVISIONAL" as distinct keys.
    """

    def test_tolerance_is_echoed_back_verbatim(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        pl = JUFEPhaseLock()
        result = pl.evaluate_phase_lock(state, tolerance=0.0083)

        self.assertIn("tolerance", result)
        self.assertEqual(result["tolerance"], 0.0083)

    def test_tolerance_basis_is_explicitly_labeled_provisional(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        pl = JUFEPhaseLock()
        result = pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertIn("tolerance_basis", result)
        self.assertEqual(result["tolerance_basis"], "PROVISIONAL")
        self.assertIn("tolerance", result)
        self.assertNotEqual("tolerance", "tolerance_basis")

    def test_full_result_shape(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        pl = JUFEPhaseLock()
        result = pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertEqual(
            set(result.keys()),
            {
                "residual",
                "residual_norm",
                "tolerance",
                "tolerance_basis",
                "locked",
            },
        )


class NonMutationTests(unittest.TestCase):
    """
    Requirement 8 -- Non-mutation.

    `state` and `self` unchanged after the call.
    """

    def test_state_is_not_mutated(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        original_values = list(state.values)
        original_compressive = state.compressive
        original_repulsive = state.repulsive

        pl = JUFEPhaseLock()
        pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertEqual(state.values, original_values)
        self.assertEqual(state.compressive, original_compressive)
        self.assertEqual(state.repulsive, original_repulsive)

    def test_self_name_is_not_mutated(self):
        pl = JUFEPhaseLock()
        original_name = pl.name

        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        pl.evaluate_phase_lock(state, tolerance=1.0)

        self.assertEqual(pl.name, original_name)

    def test_existing_methods_still_behave_identically(self):
        # locked()/harmonic_packet()/vacuum_state()/eject() are
        # untouched -- confirmed by direct behavioral check here, in
        # addition to the full regression suite below.
        balanced_state = JUFELocalState([3.0, 5.0, 2.0, 3.0, 5.0, 2.0])
        pl = JUFEPhaseLock()

        pl.evaluate_phase_lock(
            balanced_state, tolerance=1.0
        )  # must not affect below

        self.assertTrue(pl.locked(balanced_state))
        self.assertEqual(
            pl.harmonic_packet(balanced_state), balanced_state.to_dict()
        )
        self.assertEqual(pl.vacuum_state(), [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        ejected = pl.eject(balanced_state)
        self.assertIsNotNone(ejected)
        self.assertEqual(ejected["phase_locked"], True)
        self.assertEqual(ejected["vacuum"], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


class RegressionTests(unittest.TestCase):
    """
    Requirement 9 -- Regression.

    Confirms ABTMEngine.evaluate() output for the three baseline
    fixtures (balanced/unbalanced/vacuum) is byte-for-byte unchanged by
    the addition of evaluate_phase_lock() -- same technique as the
    "default unchanged" tests from the four prior consolidation steps:
    literal golden dicts captured from evaluate() output, independently
    transcribed, asserted via full-dict equality. (Whether the rest of
    the previously-existing 163 tests still pass is confirmed by
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
