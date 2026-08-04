from __future__ import annotations

import numpy as np

from ..local_state import JUFELocalState
from ..transformation import JUFETransformation
from ..conservation import JUFEConservation
from ..equilibrium import JUFEEquilibrium


class ABTMEngine:
    """
    Analytical Boundary Transfer Mechanics (ABTM) Engine.

    Implements the executable runtime pipeline for
    Manuscripts 001 and 002.
    """

    def __init__(self) -> None:

        self.name = "ABTM Engine"
        self.version = "2.3.0"

        self.transformation = JUFETransformation(
            "Identity"
        )

        self.conservation = JUFEConservation()

        self.equilibrium = JUFEEquilibrium()

    def compute_manifold_stability(
        self,
        psi_barrier: np.ndarray,
    ) -> bool:
        """
        Evaluate manifold stability using the current
        trace-parity criterion.

        σ = Trace(Ψ) mod 6
        """

        if psi_barrier.ndim != 2:
            raise ValueError(
                "psi_barrier must be a matrix."
            )

        sigma = np.trace(psi_barrier) % 6

        return sigma == 0

    def evaluate(self, values):
        """
        Execute one complete JUFE evaluation cycle.
        """

        #
        # Local Field State
        #

        state = JUFELocalState(values)

        #
        # Transformation
        #

        transformed = self.transformation.apply(
            state
        )

        #
        # Conservation
        #

        conserved = self.conservation.verify(
            state,
            transformed,
        )

        #
        # Equilibrium
        #

        equilibrium = self.equilibrium.evaluate(
            transformed,
        )

        #
        # Phase Difference
        #

        phase = transformed.phase_difference()

        #
        # Manuscript implementation status.
        #
        # The manuscript does not yet define
        # a final executable sigma calculation.
        #

        status = "PROVISIONAL"

        stable = (
            conserved
            and equilibrium
        )

        return {

            "state": transformed.to_dict(),

            "phase": phase,

            "status": status,

            "conservation": conserved,

            "equilibrium": equilibrium,

            "stable": stable,

        }