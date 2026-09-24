"""
Canonical-runtime non-regression baseline for ABTMEngine.evaluate().

These tests are a golden/snapshot capture of the COMPLETE current output of
``ABTMEngine.evaluate()`` (src/engines/abtm.py) for three fixed six-component
inputs, run through main.py -> src/runtime.py -> src/engines/abtm.py exactly
as the pipeline behaves today.

IMPORTANT: this file documents CURRENT behavior as a neutral fact, not a
claim that the behavior is scientifically correct, complete, or free of
placeholders/contradictions. Where the current pipeline produces a value
that looks like a stub or an internal contradiction (for example, the
tensegrity tensor's "divergence_free" flag reading False even for the
all-zero vacuum input, because "structural_constraint" and
"harmonic_modulation" are fixed non-zero placeholder terms rather than
functions of the input), that value is asserted on as-is. These tests exist
purely to catch unintended regressions in that behavior; they are not
correctness tests and must not be read as validating the manuscript
mathematics.

Fixed six-component inputs covered:
    - [3, 5, 2, 3, 5, 2]  balanced M/A state (M == A)
    - [3, 5, 2, 1, 4, 6]  unbalanced state (M != A)
    - [0, 0, 0, 0, 0, 0]  vacuum/zero state

For a bare six-value input, ABTMEngine.evaluate() takes the
"complete_states == 1 and not remaining" branch and returns a single
flattened dict (not the multi-state "states" wrapper), containing every
per-state field plus the whole-run fields ("global_conservation",
"harmonic_layer", "sensitivity_matrix", "status") merged in at the top
level. That flattened shape is itself part of the baseline being captured.

In addition to the three fixed six-component inputs above, this file also
characterizes five further current branches of the canonical runtime:
    - fewer than six values: the exact current ValueError and its message
      text, raised identically through both ABTMEngine.evaluate() and
      JUFERuntime.evaluate();
    - twelve values (two complete states, no remainder): the current
      multi-state "states" list response shape, its run-level fields, and
      the explicit presence (not absence) of "remaining"/"remaining_count"
      even when there is nothing left over;
    - an input that is not a multiple of six (one complete state plus
      leftover values): the current "remaining"/"remaining_count" contents
      and how the leftover values are excluded from global_conservation;
    - a pass-through check confirming JUFERuntime.evaluate() currently
      returns the same result as calling ABTMEngine.evaluate() directly
      with the same input;
    - a characterization of JUFERuntime.evaluate_dataset(), including the
      current nesting behavior where each entry in its "states" list is
      itself a fully flattened single-state ABTMEngine.evaluate() result.
"""

from __future__ import annotations

import unittest

from src.engines.abtm import ABTMEngine
from src.runtime import JUFERuntime


class ABTMEvaluateBalancedStateBaselineTests(unittest.TestCase):
    """
    Golden baseline for evaluate([3, 5, 2, 3, 5, 2]) -- a balanced M/A
    state (M == A, exact phase equilibrium, exact phase lock).

    Documents current behavior only; not a correctness claim.
    """

    def setUp(self):
        self.engine = ABTMEngine()
        self.result = self.engine.evaluate([3, 5, 2, 3, 5, 2])

    def assertFloatEqual(self, actual, expected, msg=None):
        self.assertAlmostEqual(actual, expected, places=9, msg=msg)

    def test_transformation_state(self):
        state = self.result["state"]

        self.assertEqual(state["Mx"], 3.0)
        self.assertEqual(state["My"], 5.0)
        self.assertEqual(state["Mz"], 2.0)
        self.assertEqual(state["Ax"], 3.0)
        self.assertEqual(state["Ay"], 5.0)
        self.assertEqual(state["Az"], 2.0)
        self.assertIsNone(state["cell_coordinate"])
        self.assertIsNone(state["frame_index"])
        self.assertEqual(state["lifecycle_state"], "ACTIVE")
        self.assertEqual(state["mapping_version"], "JUFE-LOCAL-1")
        self.assertEqual(state["transformation"], "Identity")
        self.assertEqual(state["phase_difference"], [0.0, 0.0, 0.0])
        self.assertTrue(state["phase_equilibrium"])
        self.assertFalse(state["vacuum"])

    def test_top_level_phase_difference(self):
        # Delta = M - A, reported separately from state["phase_difference"].
        self.assertEqual(self.result["phase"], [0.0, 0.0, 0.0])

    def test_local_conservation(self):
        self.assertIs(self.result["local_conservation"], True)

    def test_equilibrium(self):
        self.assertIs(self.result["equilibrium"], True)

    def test_gradient(self):
        gradient = self.result["gradient"]

        self.assertEqual(gradient["gradient"], (3.0, 5.0, 2.0))
        self.assertEqual(gradient["propagation"], (-3.0, -5.0, -2.0))
        self.assertFloatEqual(gradient["magnitude"], 6.164414002968976)
        self.assertIs(gradient["gradient_dominance"], False)

    def test_phase_lock(self):
        phase_lock = self.result["phase_lock"]

        self.assertIsNotNone(phase_lock)
        self.assertEqual(phase_lock["vacuum"], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertIs(phase_lock["phase_locked"], True)
        self.assertEqual(phase_lock["packet"], self.result["state"])

    def test_toroidal_flux(self):
        toroidal = self.result["toroidal_flux"]

        self.assertEqual(toroidal["omega_t"], 1.0)
        self.assertFloatEqual(toroidal["geometry"], 8.717797887081348)
        self.assertFloatEqual(toroidal["xi"], 8.717797887081348)
        self.assertFloatEqual(toroidal["work"], 8.717797887081348)

    def test_global_conservation(self):
        global_conservation = self.result["global_conservation"]

        self.assertEqual(global_conservation["global_sum"], 20.0)
        self.assertIs(global_conservation["conserved"], False)
        self.assertEqual(global_conservation["residual"], 20.0)

    def test_sensitivity_matrix(self):
        sensitivity = self.result["sensitivity_matrix"]

        identity_6x6 = [
            [1.0 if row == col else 0.0 for col in range(6)]
            for row in range(6)
        ]
        self.assertEqual(sensitivity["matrix"], identity_6x6)
        self.assertEqual(sensitivity["determinant"], 1.0)
        self.assertIs(sensitivity["catastrophic_transition"], False)

    def test_harmonic_layer(self):
        harmonic = self.result["harmonic_layer"]

        self.assertEqual(harmonic["harmonic"], 0)
        self.assertEqual(harmonic["phase"], 0.0)
        self.assertEqual(harmonic["modulation"], 1.0)

    def test_tensegrity_tensor(self):
        tensor = self.result["tensegrity_tensor"]

        self.assertFloatEqual(tensor["geometry"], 6.164414002968976)
        self.assertEqual(tensor["structural_constraint"], 1.0)
        self.assertFloatEqual(tensor["toroidal_flux"], 8.717797887081348)
        self.assertEqual(tensor["harmonic_modulation"], 1.0)
        self.assertFloatEqual(tensor["total"], 16.882211890050325)
        self.assertIs(tensor["divergence_free"], False)

    def test_stability_and_status(self):
        self.assertIs(self.result["stable"], True)
        self.assertEqual(self.result["status"], "IMPLEMENTED")


class ABTMEvaluateUnbalancedStateBaselineTests(unittest.TestCase):
    """
    Golden baseline for evaluate([3, 5, 2, 1, 4, 6]) -- an unbalanced
    state (M != A, no phase equilibrium, no phase lock ejection).

    Documents current behavior only; not a correctness claim.
    """

    def setUp(self):
        self.engine = ABTMEngine()
        self.result = self.engine.evaluate([3, 5, 2, 1, 4, 6])

    def assertFloatEqual(self, actual, expected, msg=None):
        self.assertAlmostEqual(actual, expected, places=9, msg=msg)

    def test_transformation_state(self):
        state = self.result["state"]

        self.assertEqual(state["Mx"], 3.0)
        self.assertEqual(state["My"], 5.0)
        self.assertEqual(state["Mz"], 2.0)
        self.assertEqual(state["Ax"], 1.0)
        self.assertEqual(state["Ay"], 4.0)
        self.assertEqual(state["Az"], 6.0)
        self.assertIsNone(state["cell_coordinate"])
        self.assertIsNone(state["frame_index"])
        self.assertEqual(state["lifecycle_state"], "ACTIVE")
        self.assertEqual(state["mapping_version"], "JUFE-LOCAL-1")
        self.assertEqual(state["transformation"], "Identity")
        self.assertEqual(state["phase_difference"], [2.0, 1.0, -4.0])
        self.assertFalse(state["phase_equilibrium"])
        self.assertFalse(state["vacuum"])

    def test_top_level_phase_difference(self):
        self.assertEqual(self.result["phase"], [2.0, 1.0, -4.0])

    def test_local_conservation(self):
        # Conservation here checks that the (identity) transformation
        # preserved the canonical component values, which it did -- it
        # is independent of whether M and A are balanced.
        self.assertIs(self.result["local_conservation"], True)

    def test_equilibrium(self):
        self.assertIs(self.result["equilibrium"], False)

    def test_gradient(self):
        gradient = self.result["gradient"]

        # Gradient is defined from M alone, so it is identical to the
        # balanced case above (A does not participate here).
        self.assertEqual(gradient["gradient"], (3.0, 5.0, 2.0))
        self.assertEqual(gradient["propagation"], (-3.0, -5.0, -2.0))
        self.assertFloatEqual(gradient["magnitude"], 6.164414002968976)
        self.assertIs(gradient["gradient_dominance"], False)

    def test_phase_lock(self):
        # No phase lock is reached, so eject() currently returns None
        # rather than any dict shape.
        self.assertIsNone(self.result["phase_lock"])

    def test_toroidal_flux(self):
        toroidal = self.result["toroidal_flux"]

        self.assertEqual(toroidal["omega_t"], 1.0)
        self.assertFloatEqual(toroidal["geometry"], 9.539392014169456)
        self.assertFloatEqual(toroidal["xi"], 9.539392014169456)
        self.assertFloatEqual(toroidal["work"], 9.539392014169456)

    def test_global_conservation(self):
        global_conservation = self.result["global_conservation"]

        self.assertEqual(global_conservation["global_sum"], 21.0)
        self.assertIs(global_conservation["conserved"], False)
        self.assertEqual(global_conservation["residual"], 21.0)

    def test_sensitivity_matrix(self):
        sensitivity = self.result["sensitivity_matrix"]

        identity_6x6 = [
            [1.0 if row == col else 0.0 for col in range(6)]
            for row in range(6)
        ]
        self.assertEqual(sensitivity["matrix"], identity_6x6)
        self.assertEqual(sensitivity["determinant"], 1.0)
        self.assertIs(sensitivity["catastrophic_transition"], False)

    def test_harmonic_layer(self):
        harmonic = self.result["harmonic_layer"]

        self.assertEqual(harmonic["harmonic"], 0)
        self.assertEqual(harmonic["phase"], 0.0)
        self.assertEqual(harmonic["modulation"], 1.0)

    def test_tensegrity_tensor(self):
        tensor = self.result["tensegrity_tensor"]

        self.assertFloatEqual(tensor["geometry"], 6.164414002968976)
        self.assertEqual(tensor["structural_constraint"], 1.0)
        self.assertFloatEqual(tensor["toroidal_flux"], 9.539392014169456)
        self.assertEqual(tensor["harmonic_modulation"], 1.0)
        self.assertFloatEqual(tensor["total"], 17.703806017138433)
        self.assertIs(tensor["divergence_free"], False)

    def test_stability_and_status(self):
        # stable = local_conservation AND equilibrium; here
        # equilibrium is False so stable is False even though
        # local_conservation is True.
        self.assertIs(self.result["stable"], False)
        self.assertEqual(self.result["status"], "IMPLEMENTED")


class ABTMEvaluateVacuumStateBaselineTests(unittest.TestCase):
    """
    Golden baseline for evaluate([0, 0, 0, 0, 0, 0]) -- the vacuum/zero
    state (M == A == 0, exact phase equilibrium, exact phase lock,
    provisional six-zero vacuum representation satisfied).

    Documents current behavior only; not a correctness claim.
    """

    def setUp(self):
        self.engine = ABTMEngine()
        self.result = self.engine.evaluate([0, 0, 0, 0, 0, 0])

    def assertFloatEqual(self, actual, expected, msg=None):
        self.assertAlmostEqual(actual, expected, places=9, msg=msg)

    def test_transformation_state(self):
        state = self.result["state"]

        self.assertEqual(state["Mx"], 0.0)
        self.assertEqual(state["My"], 0.0)
        self.assertEqual(state["Mz"], 0.0)
        self.assertEqual(state["Ax"], 0.0)
        self.assertEqual(state["Ay"], 0.0)
        self.assertEqual(state["Az"], 0.0)
        self.assertIsNone(state["cell_coordinate"])
        self.assertIsNone(state["frame_index"])
        # Current behavior: the vacuum *input* is still constructed with
        # the default lifecycle_state="ACTIVE" (ABTMEngine.evaluate()
        # never passes lifecycle_state="VACUUM"); "vacuum" below is a
        # separately computed boolean flag, not the lifecycle_state.
        self.assertEqual(state["lifecycle_state"], "ACTIVE")
        self.assertEqual(state["mapping_version"], "JUFE-LOCAL-1")
        self.assertEqual(state["transformation"], "Identity")
        self.assertEqual(state["phase_difference"], [0.0, 0.0, 0.0])
        self.assertTrue(state["phase_equilibrium"])
        self.assertTrue(state["vacuum"])

    def test_top_level_phase_difference(self):
        self.assertEqual(self.result["phase"], [0.0, 0.0, 0.0])

    def test_local_conservation(self):
        self.assertIs(self.result["local_conservation"], True)

    def test_equilibrium(self):
        self.assertIs(self.result["equilibrium"], True)

    def test_gradient(self):
        gradient = self.result["gradient"]

        self.assertEqual(gradient["gradient"], (0.0, 0.0, 0.0))
        # Current behavior: -k * 0.0 yields IEEE-754 negative zero in
        # each component; -0.0 == 0.0 under Python's float equality, so
        # this is asserted the same way as any other zero vector.
        self.assertEqual(gradient["propagation"], (-0.0, -0.0, -0.0))
        self.assertFloatEqual(gradient["magnitude"], 0.0)
        self.assertIs(gradient["gradient_dominance"], False)

    def test_phase_lock(self):
        phase_lock = self.result["phase_lock"]

        self.assertIsNotNone(phase_lock)
        self.assertEqual(phase_lock["vacuum"], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertIs(phase_lock["phase_locked"], True)
        self.assertEqual(phase_lock["packet"], self.result["state"])

    def test_toroidal_flux(self):
        toroidal = self.result["toroidal_flux"]

        self.assertEqual(toroidal["omega_t"], 1.0)
        self.assertFloatEqual(toroidal["geometry"], 0.0)
        self.assertFloatEqual(toroidal["xi"], 0.0)
        self.assertFloatEqual(toroidal["work"], 0.0)

    def test_global_conservation(self):
        global_conservation = self.result["global_conservation"]

        self.assertEqual(global_conservation["global_sum"], 0.0)
        self.assertIs(global_conservation["conserved"], True)
        self.assertEqual(global_conservation["residual"], 0.0)

    def test_sensitivity_matrix(self):
        sensitivity = self.result["sensitivity_matrix"]

        identity_6x6 = [
            [1.0 if row == col else 0.0 for col in range(6)]
            for row in range(6)
        ]
        self.assertEqual(sensitivity["matrix"], identity_6x6)
        self.assertEqual(sensitivity["determinant"], 1.0)
        self.assertIs(sensitivity["catastrophic_transition"], False)

    def test_harmonic_layer(self):
        harmonic = self.result["harmonic_layer"]

        self.assertEqual(harmonic["harmonic"], 0)
        self.assertEqual(harmonic["phase"], 0.0)
        self.assertEqual(harmonic["modulation"], 1.0)

    def test_tensegrity_tensor(self):
        tensor = self.result["tensegrity_tensor"]

        # Current behavior / documented contradiction: even for the
        # all-zero vacuum input, "structural_constraint" and
        # "harmonic_modulation" are fixed placeholder terms (1.0 each,
        # from float(conserved) and cos(0)) rather than functions of the
        # vacuum state, so "total" is 2.0 (not 0.0) and
        # "divergence_free" is False. This is recorded as-is, not
        # endorsed as correct.
        self.assertFloatEqual(tensor["geometry"], 0.0)
        self.assertEqual(tensor["structural_constraint"], 1.0)
        self.assertFloatEqual(tensor["toroidal_flux"], 0.0)
        self.assertEqual(tensor["harmonic_modulation"], 1.0)
        self.assertFloatEqual(tensor["total"], 2.0)
        self.assertIs(tensor["divergence_free"], False)

    def test_stability_and_status(self):
        self.assertIs(self.result["stable"], True)
        self.assertEqual(self.result["status"], "IMPLEMENTED")


class ABTMEvaluateShortInputBaselineTests(unittest.TestCase):
    """
    Golden baseline for the current fewer-than-six-values error path.

    Documents current behavior only; not a correctness claim.
    """

    def test_engine_evaluate_raises_with_current_message(self):
        engine = ABTMEngine()

        with self.assertRaises(ValueError) as ctx:
            engine.evaluate([1, 2, 3])

        self.assertEqual(
            str(ctx.exception),
            "At least six values are required.",
        )

    def test_runtime_evaluate_raises_with_same_message(self):
        # JUFERuntime.evaluate() currently forwards straight to
        # ABTMEngine.evaluate() with no additional handling, so the
        # short-input error is identical through either entry point.
        runtime = JUFERuntime()

        with self.assertRaises(ValueError) as ctx:
            runtime.evaluate([1, 2, 3])

        self.assertEqual(
            str(ctx.exception),
            "At least six values are required.",
        )


class ABTMEvaluateTwelveValuesBaselineTests(unittest.TestCase):
    """
    Golden baseline for evaluate() given twelve values (two complete
    six-component states, no remainder): [3,5,2,3,5,2, 3,5,2,1,4,6],
    i.e. the balanced state from the class above immediately followed
    by the unbalanced state from the class above.

    Because complete_states (2) is not 1, this does NOT take the
    single-flattened-result branch used by the three six-value baseline
    cases; it takes the "states" list branch instead. Documents current
    behavior only; not a correctness claim.
    """

    def setUp(self):
        self.engine = ABTMEngine()
        self.result = self.engine.evaluate(
            [3, 5, 2, 3, 5, 2, 3, 5, 2, 1, 4, 6]
        )

    def assertFloatEqual(self, actual, expected, msg=None):
        self.assertAlmostEqual(actual, expected, places=9, msg=msg)

    def test_top_level_keys_and_counts(self):
        self.assertEqual(
            sorted(self.result.keys()),
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
        self.assertEqual(self.result["complete_states"], 2)
        self.assertEqual(len(self.result["states"]), 2)
        self.assertEqual(self.result["status"], "IMPLEMENTED")

    def test_remaining_fields_are_present_but_empty(self):
        # Current behavior: for an exact multiple of six, "remaining"
        # and "remaining_count" are NOT omitted -- the multi-state
        # return branch always attaches them, just with an empty list
        # and a zero count. Asserted explicitly rather than assumed.
        self.assertIn("remaining", self.result)
        self.assertIn("remaining_count", self.result)
        self.assertEqual(self.result["remaining"], [])
        self.assertEqual(self.result["remaining_count"], 0)

    def test_first_state_matches_balanced_single_state_fields(self):
        # states[0] corresponds to [3,5,2,3,5,2], the same balanced
        # input characterized in ABTMEvaluateBalancedStateBaselineTests
        # above. Its per-state field values are identical here; only
        # the run-level fields (global_conservation, harmonic_layer,
        # sensitivity_matrix, status) are NOT embedded in this entry,
        # unlike the flattened single-state return shape.
        state = self.result["states"][0]

        self.assertEqual(
            sorted(state.keys()),
            [
                "equilibrium",
                "gradient",
                "local_conservation",
                "phase",
                "phase_lock",
                "stable",
                "state",
                "tensegrity_tensor",
                "toroidal_flux",
            ],
        )
        self.assertEqual(state["state"]["Mx"], 3.0)
        self.assertEqual(state["state"]["Ax"], 3.0)
        self.assertTrue(state["state"]["phase_equilibrium"])
        self.assertEqual(state["phase"], [0.0, 0.0, 0.0])
        self.assertIs(state["local_conservation"], True)
        self.assertIs(state["equilibrium"], True)
        self.assertIsNotNone(state["phase_lock"])
        self.assertIs(state["phase_lock"]["phase_locked"], True)
        self.assertFloatEqual(
            state["gradient"]["magnitude"], 6.164414002968976
        )
        self.assertFloatEqual(
            state["toroidal_flux"]["work"], 8.717797887081348
        )
        self.assertFloatEqual(
            state["tensegrity_tensor"]["total"], 16.882211890050325
        )
        self.assertIs(state["stable"], True)

    def test_second_state_matches_unbalanced_single_state_fields(self):
        # states[1] corresponds to [3,5,2,1,4,6], the same unbalanced
        # input characterized in
        # ABTMEvaluateUnbalancedStateBaselineTests above.
        state = self.result["states"][1]

        self.assertEqual(state["state"]["Mx"], 3.0)
        self.assertEqual(state["state"]["Ax"], 1.0)
        self.assertFalse(state["state"]["phase_equilibrium"])
        self.assertEqual(state["phase"], [2.0, 1.0, -4.0])
        self.assertIs(state["local_conservation"], True)
        self.assertIs(state["equilibrium"], False)
        self.assertIsNone(state["phase_lock"])
        self.assertFloatEqual(
            state["gradient"]["magnitude"], 6.164414002968976
        )
        self.assertFloatEqual(
            state["toroidal_flux"]["work"], 9.539392014169456
        )
        self.assertFloatEqual(
            state["tensegrity_tensor"]["total"], 17.703806017138433
        )
        self.assertIs(state["stable"], False)

    def test_global_conservation_spans_both_states(self):
        # Current behavior: the run-level global_conservation is
        # computed across BOTH transformed states together (20.0 + 21.0
        # component sums = 41.0), not per state.
        global_conservation = self.result["global_conservation"]

        self.assertEqual(global_conservation["global_sum"], 41.0)
        self.assertIs(global_conservation["conserved"], False)
        self.assertEqual(global_conservation["residual"], 41.0)

    def test_harmonic_layer_and_sensitivity_matrix(self):
        harmonic = self.result["harmonic_layer"]
        self.assertEqual(harmonic["harmonic"], 0)
        self.assertEqual(harmonic["phase"], 0.0)
        self.assertEqual(harmonic["modulation"], 1.0)

        sensitivity = self.result["sensitivity_matrix"]
        identity_6x6 = [
            [1.0 if row == col else 0.0 for col in range(6)]
            for row in range(6)
        ]
        self.assertEqual(sensitivity["matrix"], identity_6x6)
        self.assertEqual(sensitivity["determinant"], 1.0)
        self.assertIs(sensitivity["catastrophic_transition"], False)


class ABTMEvaluateNonMultipleOfSixBaselineTests(unittest.TestCase):
    """
    Golden baseline for evaluate() given an input that is not a
    multiple of six: [3,5,2,3,5,2, 7,8,9] -- one complete balanced
    state followed by three leftover values.

    Documents current behavior only; not a correctness claim.
    """

    def setUp(self):
        self.engine = ABTMEngine()
        self.result = self.engine.evaluate(
            [3, 5, 2, 3, 5, 2, 7, 8, 9]
        )

    def test_complete_state_and_remaining_counts(self):
        self.assertEqual(self.result["complete_states"], 1)
        self.assertEqual(len(self.result["states"]), 1)

        # Current behavior: "remaining" preserves the exact leftover
        # values, in their original order and as the original (here
        # int) values passed in -- they are never coerced through
        # JUFELocalState / float() the way the complete-state values
        # are.
        self.assertEqual(self.result["remaining"], [7, 8, 9])
        self.assertEqual(self.result["remaining_count"], 3)

    def test_single_complete_state_matches_balanced_baseline(self):
        state = self.result["states"][0]

        self.assertEqual(state["state"]["Mx"], 3.0)
        self.assertEqual(state["state"]["Az"], 2.0)
        self.assertTrue(state["state"]["phase_equilibrium"])
        self.assertIs(state["stable"], True)

    def test_global_conservation_reflects_only_the_complete_state(self):
        # Current behavior: the leftover [7, 8, 9] values never become
        # a JUFELocalState and are NOT included in global_conservation
        # -- global_sum here is 20.0 (from the one complete state
        # alone), not 20.0 + 7 + 8 + 9.
        global_conservation = self.result["global_conservation"]

        self.assertEqual(global_conservation["global_sum"], 20.0)
        self.assertIs(global_conservation["conserved"], False)
        self.assertEqual(global_conservation["residual"], 20.0)

    def test_status(self):
        self.assertEqual(self.result["status"], "IMPLEMENTED")


class JUFERuntimeEvaluatePassThroughBaselineTests(unittest.TestCase):
    """
    Golden baseline confirming that JUFERuntime.evaluate() (src/runtime.py)
    currently returns the same result as calling ABTMEngine.evaluate()
    directly with the same input.

    This documents that the runtime is a thin pass-through today; it is
    not an assertion that thin pass-through is the "correct" or final
    design.
    """

    def test_runtime_evaluate_matches_a_fresh_engine_evaluate(self):
        runtime = JUFERuntime()
        standalone_engine = ABTMEngine()

        runtime_result = runtime.evaluate([3, 5, 2, 3, 5, 2])
        standalone_result = standalone_engine.evaluate([3, 5, 2, 3, 5, 2])

        self.assertEqual(runtime_result, standalone_result)

    def test_runtime_evaluate_matches_its_own_engine_evaluate_directly(self):
        runtime = JUFERuntime()

        runtime_result = runtime.evaluate([3, 5, 2, 3, 5, 2])
        direct_result = runtime.engine.evaluate([3, 5, 2, 3, 5, 2])

        self.assertEqual(runtime_result, direct_result)


class JUFERuntimeEvaluateDatasetBaselineTests(unittest.TestCase):
    """
    Golden baseline for JUFERuntime.evaluate_dataset() (src/runtime.py),
    using [3, 5, 2, 3, 5, 2] -- the same balanced M/A state already
    fully characterized in ABTMEvaluateBalancedStateBaselineTests above
    -- as the representative input. It is representative because it is
    an exact multiple of six (no remainder to further complicate the
    shape) and its per-field values are already independently pinned
    down elsewhere in this file, so any divergence between
    evaluate_dataset()'s handling and evaluate()'s handling of the same
    values is isolated and visible here.

    Documents current behavior only; not a correctness claim.
    """

    def setUp(self):
        self.runtime = JUFERuntime()
        self.result = self.runtime.evaluate_dataset([3, 5, 2, 3, 5, 2])

    def test_top_level_keys_and_counts(self):
        # Current behavior: unlike ABTMEngine.evaluate()'s own
        # multi/remainder branch (which attaches global_conservation,
        # harmonic_layer, sensitivity_matrix, and status at the top
        # level -- see ABTMEvaluateTwelveValuesBaselineTests above),
        # JUFERuntime.evaluate_dataset()'s top level carries none of
        # those keys.
        self.assertEqual(
            sorted(self.result.keys()),
            ["complete_states", "remaining", "remaining_count", "states"],
        )
        self.assertEqual(self.result["complete_states"], 1)
        self.assertEqual(self.result["remaining"], [])
        self.assertEqual(self.result["remaining_count"], 0)
        self.assertEqual(len(self.result["states"]), 1)

    def test_state_entry_is_itself_a_flattened_single_state_result(self):
        # Current behavior / documented oddity: evaluate_dataset()
        # builds its "states" list by calling
        # self.engine.evaluate(state) once per six-value chunk. Because
        # each chunk is itself exactly six values, that nested call
        # independently takes ABTMEngine.evaluate()'s
        # "complete_states == 1 and not remaining" branch and returns
        # the FULLY FLATTENED single-state dict -- including its own
        # embedded global_conservation / harmonic_layer /
        # sensitivity_matrix / status, computed from that one chunk in
        # isolation. So each entry in evaluate_dataset()'s "states"
        # list is shaped differently from an entry in
        # ABTMEngine.evaluate()'s own multi-state "states" list (which
        # has no such embedded keys; compare
        # ABTMEvaluateTwelveValuesBaselineTests.
        # test_first_state_matches_balanced_single_state_fields above).
        state = self.result["states"][0]

        self.assertIn("global_conservation", state)
        self.assertIn("harmonic_layer", state)
        self.assertIn("sensitivity_matrix", state)
        self.assertIn("status", state)
        self.assertEqual(state["status"], "IMPLEMENTED")
        self.assertEqual(
            state["global_conservation"],
            {"global_sum": 20.0, "conserved": False, "residual": 20.0},
        )

    def test_state_entry_matches_direct_engine_evaluate_on_same_chunk(self):
        # Because of the nesting described above, the single entry in
        # evaluate_dataset()'s "states" list is currently identical to
        # calling ABTMEngine.evaluate() directly on that same 6-value
        # chunk (i.e. identical to the balanced-state baseline captured
        # in ABTMEvaluateBalancedStateBaselineTests).
        standalone_engine = ABTMEngine()
        direct_result = standalone_engine.evaluate([3, 5, 2, 3, 5, 2])

        self.assertEqual(self.result["states"][0], direct_result)


if __name__ == "__main__":
    unittest.main()
