from __future__ import annotations

import numpy as np


class JUFESensitivityMatrix:
    """
    JUFE Sensitivity Matrix

    Implements the executable form of

        δΨ = S · δE

    described in Manuscript 002.

    The sensitivity matrix determines how
    external perturbations influence the
    local manifold state.
    """

    def __init__(
        self,
        matrix=None,
    ):

        if matrix is None:

            self.matrix = np.identity(6)

        else:

            self.matrix = np.asarray(
                matrix,
                dtype=float,
            )

            if self.matrix.shape != (6, 6):

                raise ValueError(
                    "Sensitivity matrix must be 6x6."
                )

    def apply(
        self,
        perturbation,
    ):
        """
        Apply an external perturbation.

        δΨ = S · δE
        """

        perturbation = np.asarray(
            perturbation,
            dtype=float,
        )

        if perturbation.shape != (6,):

            raise ValueError(
                "Perturbation vector must contain six values."
            )

        return self.matrix @ perturbation

    def determinant(self):

        return float(
            np.linalg.det(
                self.matrix
            )
        )

    def catastrophic_transition(
        self,
        tolerance: float = 1e-9,
    ):
        """
        Returns True when the manuscript
        catastrophic transition criterion
        is approached.

            det(S) → 0
        """

        return abs(
            self.determinant()
        ) <= tolerance

    def to_dict(self):

        return {

            "matrix":
                self.matrix.tolist(),

            "determinant":
                self.determinant(),

            "catastrophic_transition":
                self.catastrophic_transition(),

        }

    def __repr__(self):

        return (

            "JUFESensitivityMatrix("

            f"det={self.determinant():.6f}"

            ")"

        )