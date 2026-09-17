from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TensegrityTensor:
    """
    JUFE Tensegrity-Stress Tensor

    Implements the current executable form of the
    manuscript tensor.

        T_total =
            Geometry
          + Structural Constraint
          + Toroidal Flux
          + Harmonic Modulation

    The individual terms remain modular so each
    manuscript component can evolve independently.
    """

    geometry: float = 0.0

    structural_constraint: float = 0.0

    toroidal_flux: float = 0.0

    harmonic_modulation: float = 0.0

    def total(self) -> float:
        """
        Return the current tensor magnitude.
        """

        return (

            self.geometry

            + self.structural_constraint

            + self.toroidal_flux

            + self.harmonic_modulation

        )

    def divergence_free(
        self,
        tolerance: float = 1e-12,
    ) -> bool:
        """
        Current executable approximation of

            ∇μTμν = 0

        A complete differential implementation
        will replace this once the manifold
        operators are implemented.
        """

        return abs(
            self.total()
        ) <= tolerance

    def to_dict(self):

        return {

            "geometry":
                self.geometry,

            "structural_constraint":
                self.structural_constraint,

            "toroidal_flux":
                self.toroidal_flux,

            "harmonic_modulation":
                self.harmonic_modulation,

            "total":
                self.total(),

            "divergence_free":
                self.divergence_free(),

        }

    def __repr__(self):

        return (

            "TensegrityTensor("

            f"total={self.total():.6f}"

            ")"

        )