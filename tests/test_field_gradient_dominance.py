"""
Characterization and parity tests for
``src/field_gradient.py :: JUFEFieldGradient.evaluate_dominance``.

This new opt-in method is a native port of
``abtm_expansion.py :: ABTM_Expansion.dominance_ratio`` and
``ABTM_Expansion.local_gradient_dominates`` (a legacy/expansion module
kept outside src/). It is added purely as an additional capability on
``JUFEFieldGradient``; ``to_dict()`` does not call it, nothing in
``ABTMEngine.evaluate()`` calls it, and the class's existing
``gradient``/``propagation_vector``/``magnitude``/``dominant``/
``to_dict`` methods are untouched.

Traced source of truth (read directly, not assumed)
-----------------------------------------------------

``abtm_expansion.py`` (paraphrased here rather than pasted verbatim with
triple-quoted docstrings, to avoid nesting one inside this module's own
docstring)::

    @classmethod
    def dominance_ratio(cls, compressive_field, repulsive_field):
        # "Return ||M|| / ||A||."
        m = cls.as_array(compressive_field, name="compressive_field")
        a = cls.as_array(repulsive_field, name="repulsive_field")
        denominator = float(np.linalg.norm(a))
        numerator = float(np.linalg.norm(m))
        if denominator == 0:
            return float("inf") if numerator > 0 else 1.0
        return numerator / denominator

    @classmethod
    def local_gradient_dominates(cls, compressive_field, repulsive_field,
                                  *, dominance_threshold):
        # "Check ||M|| / ||A|| >= dominance_threshold."
        threshold = float(dominance_threshold)
        if not np.isfinite(threshold) or threshold < 0:
            raise ValueError("dominance_threshold must be finite and non-negative.")
        return bool(
            cls.dominance_ratio(compressive_field, repulsive_field) >= threshold
        )

Confirmed directly from source (not assumed from the task description):
  - the comparison is ``>=`` (greater-than-or-EQUAL), matching the
    "Check ||M|| / ||A|| >= dominance_threshold" docstring text exactly;
  - the zero-denominator rule is: ``inf`` when ``||A|| == 0`` and
    ``||M|| > 0``; exactly ``1.0`` when both norms are zero;
  - ``dominance_threshold`` (legacy name) is validated finite and
    non-negative, raising ``ValueError("dominance_threshold must be
    finite and non-negative.")`` -- note this is DIFFERENT wording from
    this session's own established validation-message style used
    elsewhere (see below).

``src/field_gradient.py :: JUFEFieldGradient.evaluate_dominance`` (the
new method under test here) reproduces this exact ratio, exact
zero-denominator handling, and exact ``>=`` comparison natively, without
importing ``abtm_expansion.py``. Differences from the legacy source,
all deliberate and documented in the method's own docstring:
  - it takes a single ``state`` object (reading ``state.compressive``
    and ``state.repulsive``) rather than two separate array arguments;
  - ``threshold`` has NO default at all (the legacy version's own
    ``dominance_threshold`` is also required/keyword-only with no
    default, so this matches);
  - the invalid-threshold message text is
    ``"threshold must be a finite value greater than or equal to
    zero."`` -- this session's own established phrasing (already used
    for ``global_field_balance``'s ``tolerance`` and
    ``evaluate_bifurcation``'s ``threshold``), not the legacy's
    ``"dominance_threshold must be finite and non-negative."`` text;
  - the returned mapping carries ``threshold_basis: "PROVISIONAL"``,
    citing REQ-TH-001 and DEF-0007 (see below), which the legacy
    ``BifurcationResult``-style dataclasses do not carry at all (in
    fact this pair of legacy functions returns a bare ``float``/``bool``,
    not a dataclass).

REQ-TH-001 and DEF-0007 (exact wording, read directly, not paraphrased
from memory)
------------------------------------------------------------------------

From ``JUFE_ABTM_SPEC_ENGINE/requirements_register.json``:

    REQ-TH-001, category "theorem", title "Local gradient dominance"
    manuscript_statement: "When ||M_local|| >> ||A_local||, trajectory
        follows -k grad(M_local)."
    software_requirement: "Compare field norms and declare dominance
        only against an explicit threshold."
    status: "partially_defined"
    implemented_by: ["abtm_expansion.ABTM_Expansion.dominance_ratio",
        "abtm_expansion.ABTM_Expansion.local_gradient_dominates"]
    open_questions: ["Numerical definition of 'much greater than'"]

From
``JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/DEFINITIONS/DEF-0007_Local_Gradient_Dominance.md``:

    DEF-0007 -- Local Gradient Dominance, Status: ACTIVE.
    Definition: "Within this specification, Local Gradient Dominance is
        the manuscript-defined mechanism by which the trajectory of a
        field manifestation is governed by the dominant local tension
        gradient of the surrounding field rather than by intrinsic
        particle properties."
    Scope: "This definition records only the manuscript-defined
        mechanism. It does not define: quantitative dominance
        thresholds; computational implementation; numerical simulation
        algorithms; software architecture; engineering constraints
        beyond the manuscript statements."
    Repository Status: Manuscript Concept: EXPLICIT. Engineering
        Formalization: PROVISIONAL. Mathematical Generalization:
        UNRESOLVED.

Scope boundary (documented plainly, not silently assumed): REQ-TH-001's
explicit-threshold field-norm comparison IS what ``evaluate_dominance``
implements -- comparing ``||M||``/``||A||`` for the ONE supplied state
against a caller-required threshold. DEF-0007's broader "surrounding
field" vs. "intrinsic particle properties" mechanism is NOT implemented
by this method: there is no notion here of a field separate from the
one supplied state's own M/A, no spatial neighbours, no topology, and
no boundary/jam mechanics. ``evaluate_dominance`` does not implement a
spatial gradient, a new propagation calculation, a boundary jam, or any
topology; it is scoped strictly to the single-state M/A dominance-ratio
comparison, exactly as ``dominance_ratio``/``local_gradient_dominates``
are scoped in the legacy source.

This file imports ``abtm_expansion.py`` directly -- permitted for
comparison purposes in the TEST only; the constraint against importing
the legacy module at runtime applies to ``src/field_gradient.py``
itself, which does not do so.
"""

from __future__ import annotations

import unittest

import numpy as np

from abtm_expansion import ABTM_Expansion
from src.engines.abtm import ABTMEngine
from src.field_gradient import JUFEFieldGradient
from src.local_state import JUFELocalState


def _identity_6x6():
    return [
        [1.0 if row == col else 0.0 for col in range(6)]
        for row in range(6)
    ]


class ParityWithLegacyTests(unittest.TestCase):
    """
    Requirement 1 -- Parity with both legacy functions.

    Fixed documented six-component states plus 60 deterministic seeded
    valid six-component states (>= the required 50) with caller-supplied
    thresholds, comparing compressive_norm/repulsive_norm/ratio/dominant
    against ABTM_Expansion.dominance_ratio and
    ABTM_Expansion.local_gradient_dominates called directly.
    """

    def _assert_matches_legacy(self, state_values, threshold):
        state = JUFELocalState([float(v) for v in state_values])
        fg = JUFEFieldGradient()

        native_result = fg.evaluate_dominance(state, threshold=threshold)

        legacy_ratio = ABTM_Expansion.dominance_ratio(
            state.compressive, state.repulsive
        )
        legacy_dominant = ABTM_Expansion.local_gradient_dominates(
            state.compressive,
            state.repulsive,
            dominance_threshold=threshold,
        )
        legacy_compressive_norm = float(
            np.linalg.norm(np.asarray(state.compressive, dtype=float))
        )
        legacy_repulsive_norm = float(
            np.linalg.norm(np.asarray(state.repulsive, dtype=float))
        )

        self.assertEqual(
            native_result["compressive_norm"], legacy_compressive_norm
        )
        self.assertEqual(
            native_result["repulsive_norm"], legacy_repulsive_norm
        )
        self.assertEqual(native_result["ratio"], legacy_ratio)
        self.assertEqual(native_result["dominant"], legacy_dominant)

    FIXED_CASES = (
        # (name, six values, threshold)
        ("balanced_state", [3, 5, 2, 3, 5, 2], 1.0),
        ("unbalanced_state", [3, 5, 2, 1, 4, 6], 1.0),
        ("vacuum_state", [0, 0, 0, 0, 0, 0], 1.0),
        ("m_much_greater_than_a", [10, 10, 10, 0.1, 0.1, 0.1], 5.0),
        ("a_much_greater_than_m", [0.1, 0.1, 0.1, 10, 10, 10], 5.0),
    )

    def test_fixed_cases_match_legacy_exactly(self):
        for name, values, threshold in self.FIXED_CASES:
            with self.subTest(case=name):
                self._assert_matches_legacy(values, threshold)

    def test_generated_cases_match_legacy_exactly(self):
        seed = 20250501
        rng = np.random.default_rng(seed)
        count = 60
        self.assertGreaterEqual(count, 50)

        for index in range(count):
            values = rng.integers(-9, 10, size=6)
            threshold = float(rng.uniform(0.0, 10.0))

            with self.subTest(index=index):
                self._assert_matches_legacy(values, threshold)


class RatioVersusThresholdTests(unittest.TestCase):
    """
    Requirement 2 -- Ratio above / below / exactly equal to threshold.

    The equal-to-threshold case confirms the comparison is `>=`, not
    `>` (a strict `>` would report dominant=False at the exact
    boundary instead).
    """

    def setUp(self):
        self.fg = JUFEFieldGradient()

    def test_ratio_above_threshold_is_dominant(self):
        # |M| = 5 (3-4-0 triangle), |A| = 1, ratio = 5.0
        state = JUFELocalState([3.0, 4.0, 0.0, 1.0, 0.0, 0.0])
        result = self.fg.evaluate_dominance(state, threshold=4.0)

        self.assertEqual(result["ratio"], 5.0)
        self.assertTrue(result["dominant"])

    def test_ratio_below_threshold_is_not_dominant(self):
        state = JUFELocalState([3.0, 4.0, 0.0, 1.0, 0.0, 0.0])
        result = self.fg.evaluate_dominance(state, threshold=6.0)

        self.assertEqual(result["ratio"], 5.0)
        self.assertFalse(result["dominant"])

    def test_ratio_exactly_equal_to_threshold_is_dominant(self):
        # Confirms >= (not strict >): ratio == threshold must count as
        # dominant.
        state = JUFELocalState([3.0, 4.0, 0.0, 1.0, 0.0, 0.0])
        result = self.fg.evaluate_dominance(state, threshold=5.0)

        self.assertEqual(result["ratio"], 5.0)
        self.assertTrue(
            result["dominant"],
            "ratio == threshold must count as dominant (the comparison "
            "is >=, not >).",
        )

        legacy_dominant = ABTM_Expansion.local_gradient_dominates(
            state.compressive, state.repulsive, dominance_threshold=5.0
        )
        self.assertTrue(legacy_dominant)
        self.assertEqual(result["dominant"], legacy_dominant)


class ZeroRepulsiveNormTests(unittest.TestCase):
    """
    Requirement 3 -- Zero repulsive norm, nonzero compressive norm.

    Ratio is infinity, dominant is True for any finite threshold.
    """

    def test_zero_repulsive_nonzero_compressive_ratio_is_infinite(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 0.0, 0.0, 0.0])
        fg = JUFEFieldGradient()
        result = fg.evaluate_dominance(state, threshold=1.0)

        self.assertEqual(result["repulsive_norm"], 0.0)
        self.assertGreater(result["compressive_norm"], 0.0)
        self.assertEqual(result["ratio"], float("inf"))
        self.assertTrue(result["dominant"])

    def test_zero_repulsive_nonzero_compressive_is_dominant_for_large_threshold(self):
        # Dominant regardless of how large the (finite) threshold is.
        state = JUFELocalState([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        fg = JUFEFieldGradient()
        result = fg.evaluate_dominance(state, threshold=1_000_000.0)

        self.assertEqual(result["ratio"], float("inf"))
        self.assertTrue(result["dominant"])


class BothNormsZeroTests(unittest.TestCase):
    """
    Requirement 4 -- Both norms zero.

    Ratio is exactly 1.0 (the vacuum case).
    """

    def test_both_norms_zero_ratio_is_exactly_one(self):
        state = JUFELocalState([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        fg = JUFEFieldGradient()
        result = fg.evaluate_dominance(state, threshold=1.0)

        self.assertEqual(result["compressive_norm"], 0.0)
        self.assertEqual(result["repulsive_norm"], 0.0)
        self.assertEqual(result["ratio"], 1.0)

    def test_both_norms_zero_dominant_depends_on_threshold(self):
        state = JUFELocalState([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        fg = JUFEFieldGradient()

        at_or_below_one = fg.evaluate_dominance(state, threshold=1.0)
        above_one = fg.evaluate_dominance(state, threshold=1.5)

        self.assertTrue(at_or_below_one["dominant"])  # 1.0 >= 1.0
        self.assertFalse(above_one["dominant"])  # 1.0 >= 1.5 is False


class RequiredThresholdBehaviorTests(unittest.TestCase):
    """
    Requirement 5 -- Required-threshold behavior.

    Omitting threshold raises TypeError. Documented as intentional:
    REQ-TH-001 records the numerical definition of "much greater than"
    as an open question, so no default is invented.
    """

    def test_missing_threshold_raises_type_error(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        fg = JUFEFieldGradient()

        with self.assertRaises(TypeError):
            fg.evaluate_dominance(state)

    def test_missing_threshold_type_error_mentions_the_parameter(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        fg = JUFEFieldGradient()

        with self.assertRaises(TypeError) as ctx:
            fg.evaluate_dominance(state)
        self.assertIn("threshold", str(ctx.exception))


class ThresholdValidationTests(unittest.TestCase):
    """
    Requirement 6 -- Threshold validation.

    Negative, NaN, infinite threshold all rejected with exact exception
    type/message; threshold=0 explicitly accepted.
    """

    def setUp(self):
        self.state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        self.fg = JUFEFieldGradient()

    def test_negative_threshold_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.fg.evaluate_dominance(self.state, threshold=-1.0)
        self.assertEqual(
            str(ctx.exception),
            "threshold must be a finite value greater than or equal "
            "to zero.",
        )

    def test_nan_threshold_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.fg.evaluate_dominance(self.state, threshold=float("nan"))
        self.assertEqual(
            str(ctx.exception),
            "threshold must be a finite value greater than or equal "
            "to zero.",
        )

    def test_infinite_threshold_raises_value_error_with_exact_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.fg.evaluate_dominance(self.state, threshold=float("inf"))
        self.assertEqual(
            str(ctx.exception),
            "threshold must be a finite value greater than or equal "
            "to zero.",
        )

    def test_zero_threshold_is_explicitly_valid_not_an_error(self):
        try:
            self.fg.evaluate_dominance(self.state, threshold=0)
        except ValueError:
            self.fail("threshold=0 must be accepted, not rejected.")


class ProvisionalLabelReportingTests(unittest.TestCase):
    """
    Requirement 7 -- Provisional-label reporting.

    Result carries the exact caller threshold and
    threshold_basis == "PROVISIONAL" as distinct keys.
    """

    def test_threshold_is_echoed_back_verbatim(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        fg = JUFEFieldGradient()
        result = fg.evaluate_dominance(state, threshold=0.0091)

        self.assertIn("threshold", result)
        self.assertEqual(result["threshold"], 0.0091)

    def test_threshold_basis_is_explicitly_labeled_provisional(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        fg = JUFEFieldGradient()
        result = fg.evaluate_dominance(state, threshold=1.0)

        self.assertIn("threshold_basis", result)
        self.assertEqual(result["threshold_basis"], "PROVISIONAL")
        self.assertIn("threshold", result)
        self.assertNotEqual("threshold", "threshold_basis")

    def test_full_result_shape(self):
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        fg = JUFEFieldGradient()
        result = fg.evaluate_dominance(state, threshold=1.0)

        self.assertEqual(
            set(result.keys()),
            {
                "compressive_norm",
                "repulsive_norm",
                "ratio",
                "threshold",
                "threshold_basis",
                "dominant",
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

        fg = JUFEFieldGradient()
        fg.evaluate_dominance(state, threshold=1.0)

        self.assertEqual(state.values, original_values)
        self.assertEqual(state.compressive, original_compressive)
        self.assertEqual(state.repulsive, original_repulsive)

    def test_self_coupling_is_not_mutated(self):
        fg = JUFEFieldGradient(coupling=2.5)
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])

        fg.evaluate_dominance(state, threshold=1.0)

        self.assertEqual(fg.coupling, 2.5)

    def test_existing_methods_still_behave_identically(self):
        # gradient()/propagation_vector()/magnitude()/dominant()/
        # to_dict() are untouched -- confirmed by direct behavioral
        # check here, in addition to the full regression suite below.
        state = JUFELocalState([3.0, 5.0, 2.0, 1.0, 4.0, 6.0])
        fg = JUFEFieldGradient()

        fg.evaluate_dominance(state, threshold=1.0)  # must not affect below

        self.assertEqual(fg.gradient(state), (3.0, 5.0, 2.0))
        self.assertEqual(fg.propagation_vector(state), (-3.0, -5.0, -2.0))
        self.assertAlmostEqual(fg.magnitude(state), 6.164414002968976, places=9)
        self.assertFalse(fg.dominant(state))
        self.assertEqual(
            fg.to_dict(state),
            {
                "gradient": (3.0, 5.0, 2.0),
                "propagation": (-3.0, -5.0, -2.0),
                "magnitude": fg.magnitude(state),
                "gradient_dominance": False,
            },
        )


class RegressionTests(unittest.TestCase):
    """
    Requirement 9 -- Regression.

    Confirms ABTMEngine.evaluate() output for the three baseline
    fixtures (balanced/unbalanced/vacuum) is byte-for-byte unchanged by
    the addition of evaluate_dominance() -- same technique as the
    "default unchanged" tests from the three prior consolidation steps:
    literal golden dicts captured from evaluate() output, independently
    transcribed, asserted via full-dict equality. (Whether the rest of
    the previously-existing 139 tests still pass is confirmed by
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
