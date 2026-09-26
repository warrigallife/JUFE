from __future__ import annotations

import numpy as np

from ..local_state import JUFELocalState
from ..transformation import JUFETransformation
from ..conservation import JUFEConservation
from ..global_conservation import JUFEGlobalConservation
from ..equilibrium import JUFEEquilibrium
from ..field_gradient import JUFEFieldGradient
from ..phase_lock import JUFEPhaseLock
from ..toroidal_flux import JUFEToroidalFlux
from ..sensitivity_matrix import JUFESensitivityMatrix
from ..harmonic_layer import JUFEHarmonicLayer
from ..tensegrity_stress_tensor import TensegrityTensor


class ABTMEngine:
    """
    Analytical Boundary Transfer Mechanics Engine.

    Executes the current JUFE manuscript mathematics.
    """

    def __init__(self) -> None:

        self.name = "ABTM Engine"
        self.version = "3.1.0"

        self.transformation = JUFETransformation(
            "Identity"
        )

        self.conservation = JUFEConservation()

        self.global_conservation = (
            JUFEGlobalConservation()
        )

        self.equilibrium = JUFEEquilibrium()

        self.gradient = JUFEFieldGradient()

        self.phase_lock = JUFEPhaseLock()

        self.toroidal_flux = JUFEToroidalFlux()

        self.sensitivity = (
            JUFESensitivityMatrix()
        )

        self.harmonics = (
            JUFEHarmonicLayer()
        )

    def compute_manifold_stability(
        self,
        psi_barrier: np.ndarray,
    ) -> bool:

        if psi_barrier.ndim != 2:
            raise ValueError(
                "psi_barrier must be a matrix."
            )

        sigma = np.trace(
            psi_barrier
        ) % 6

        return sigma == 0

    def _build_diagnostics(
        self,
        states,
        *,
        dominance_threshold,
        phase_lock_tolerance,
        global_balance_tolerance,
        bifurcation_threshold,
        single_state,
    ):
        """
        Build the additive, opt-in ``diagnostics`` mapping for
        ``evaluate()``.

        Every entry here is computed by calling one of the four
        already-reviewed opt-in diagnostic methods directly
        (``JUFEFieldGradient.evaluate_dominance``,
        ``JUFEPhaseLock.evaluate_phase_lock``,
        ``JUFEGlobalConservation.global_field_balance``,
        ``JUFESensitivityMatrix.evaluate_bifurcation``) -- this helper
        does not reimplement any of their math or validation. A
        diagnostic is included only when its corresponding
        ``evaluate()`` keyword argument is not ``None``; the caller's
        exact value is always passed straight through, never defaulted,
        clamped, or coerced. When every kwarg is ``None`` this returns
        an empty dict, and ``evaluate()`` does not attach a
        ``"diagnostics"`` key at all in that case.

        ``states`` must be the same ``transformed_states`` list already
        built by the caller's normal per-state loop (i.e. it never
        includes any ``remaining`` values), so ``global_balance`` uses
        exactly the same scope the existing ``global_conservation``
        field already uses.

        ``dominance``/``phase_lock`` are computed once per entry in
        ``states``, in that same order. When ``single_state`` is True
        (the flattened one-state return shape) the single result object
        is stored directly rather than wrapped in a one-element list,
        matching how every other single-state field already appears
        unwrapped in that branch. ``global_balance`` and
        ``bifurcation`` are always single results, regardless of branch
        -- ``global_balance`` spans all of ``states`` at once, and
        ``bifurcation`` is evaluated once against the engine's own
        canonical ``self.sensitivity`` matrix, never per state.
        """

        diagnostics = {}

        if dominance_threshold is not None:

            dominance_results = [
                self.gradient.evaluate_dominance(
                    state,
                    threshold=dominance_threshold,
                )
                for state in states
            ]

            diagnostics["dominance"] = (
                dominance_results[0]
                if single_state
                else dominance_results
            )

        if phase_lock_tolerance is not None:

            phase_lock_results = [
                self.phase_lock.evaluate_phase_lock(
                    state,
                    tolerance=phase_lock_tolerance,
                )
                for state in states
            ]

            diagnostics["phase_lock"] = (
                phase_lock_results[0]
                if single_state
                else phase_lock_results
            )

        if global_balance_tolerance is not None:

            diagnostics["global_balance"] = (
                self.global_conservation.global_field_balance(
                    states,
                    tolerance=global_balance_tolerance,
                )
            )

        if bifurcation_threshold is not None:

            diagnostics["bifurcation"] = (
                self.sensitivity.evaluate_bifurcation(
                    threshold=bifurcation_threshold,
                )
            )

        return diagnostics

    def evaluate(
        self,
        values,
        *,
        dominance_threshold=None,
        phase_lock_tolerance=None,
        global_balance_tolerance=None,
        bifurcation_threshold=None,
    ):
        """
        Unified evaluation entry point.

        Accepts either a single Local Field State
        or an arbitrary-length dataset.

        Four optional, keyword-only diagnostic arguments -- all
        defaulting to ``None`` (meaning "not requested") -- expose the
        already-reviewed opt-in diagnostic methods added in prior
        consolidation steps:

            dominance_threshold      -> JUFEFieldGradient.evaluate_dominance
            phase_lock_tolerance     -> JUFEPhaseLock.evaluate_phase_lock
            global_balance_tolerance -> JUFEGlobalConservation.global_field_balance
            bifurcation_threshold    -> JUFESensitivityMatrix.evaluate_bifurcation

        When all four are ``None`` (the default), the returned result
        is byte-for-byte identical to calling ``evaluate()`` with no
        diagnostic arguments at all in every prior consolidation step:
        no ``"diagnostics"`` key is added to the result under any
        circumstance in that case -- not present, not ``None``, not an
        empty dict. Every existing field, in every existing branch
        (short-input error, single complete state, multi-state,
        non-multiple-of-six remainder), is computed by exactly the same
        unchanged code path as before this method gained these
        arguments.

        When one or more diagnostic arguments are supplied, an
        additive-only ``"diagnostics"`` key is attached to the result
        AFTER it is otherwise fully built, containing only the
        diagnostics that were actually requested. See
        ``_build_diagnostics`` above for the exact per-branch shape
        (single object vs. list, and which diagnostics apply once
        across the whole call vs. once per state).

        This method never calls ``JUFETransformation.apply_coupled_field_step``
        and accepts no ``rate``/``dt`` arguments -- automatic coupled
        evolution is out of scope for this integration step.
        """

        if len(values) < 6:
            raise ValueError(
                "At least six values are required."
            )

        results = []

        complete_states = len(values) // 6

        remaining = values[
            complete_states * 6:
        ]

        transformed_states = []

        for i in range(complete_states):

            state_values = values[
                i * 6:(i + 1) * 6
            ]

            state = JUFELocalState(
                state_values
            )

            transformed = (
                self.transformation.apply(
                    state
                )
            )

            transformed_states.append(
                transformed
            )

            conserved = (
                self.conservation.verify(
                    state,
                    transformed,
                )
            )

            equilibrium = (
                self.equilibrium.evaluate(
                    transformed
                )
            )

            gradient = (
                self.gradient.to_dict(
                    transformed
                )
            )

            phase_lock = (
                self.phase_lock.eject(
                    transformed
                )
            )

            toroidal = (
                self.toroidal_flux.to_dict(
                    transformed
                )
            )

            tensor = TensegrityTensor(
                geometry=gradient["magnitude"],
                structural_constraint=float(
                    conserved
                ),
                toroidal_flux=toroidal["work"],
                harmonic_modulation=(
                    self.harmonics.modulation_factor()
                ),
            )

            results.append({

                "state":
                    transformed.to_dict(),

                "gradient":
                    gradient,

                "phase":
                    transformed.phase_difference(),

                "phase_lock":
                    phase_lock,

                "local_conservation":
                    conserved,

                "equilibrium":
                    equilibrium,

                "toroidal_flux":
                    toroidal,

                "tensegrity_tensor":
                    tensor.to_dict(),

                "stable":
                    conserved and equilibrium,

            })

        global_conservation = (
            self.global_conservation.to_dict(
                transformed_states
            )
        )

        if complete_states == 1 and not remaining:

            result = results[0]

            result[
                "global_conservation"
            ] = global_conservation

            result[
                "harmonic_layer"
            ] = self.harmonics.to_dict()

            result[
                "sensitivity_matrix"
            ] = self.sensitivity.to_dict()

            result[
                "status"
            ] = "IMPLEMENTED"

            diagnostics = self._build_diagnostics(
                transformed_states,
                dominance_threshold=dominance_threshold,
                phase_lock_tolerance=phase_lock_tolerance,
                global_balance_tolerance=global_balance_tolerance,
                bifurcation_threshold=bifurcation_threshold,
                single_state=True,
            )

            if diagnostics:
                result["diagnostics"] = diagnostics

            return result

        result = {

            "states":
                results,

            "global_conservation":
                global_conservation,

            "harmonic_layer":
                self.harmonics.to_dict(),

            "sensitivity_matrix":
                self.sensitivity.to_dict(),

            "complete_states":
                complete_states,

            "remaining":
                remaining,

            "remaining_count":
                len(remaining),

            "status":
                "IMPLEMENTED",

        }

        diagnostics = self._build_diagnostics(
            transformed_states,
            dominance_threshold=dominance_threshold,
            phase_lock_tolerance=phase_lock_tolerance,
            global_balance_tolerance=global_balance_tolerance,
            bifurcation_threshold=bifurcation_threshold,
            single_state=False,
        )

        if diagnostics:
            result["diagnostics"] = diagnostics

        return result