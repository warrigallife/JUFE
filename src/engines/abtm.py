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

    def evaluate(
        self,
        values,
    ):
        """
        Unified evaluation entry point.

        Accepts either a single Local Field State
        or an arbitrary-length dataset.
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

            return result

        return {

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