from __future__ import annotations

import math


class JUFEToroidalFlux:
    """
    JUFE Toroidal Flux

    Implements the executable toroidal work term

        ∮ Ξ(ΩT,G) dΣ

    described in the manuscript.

    The current implementation provides the
    deterministic runtime interface while the
    complete manifold integral is introduced
    in later manuscript revisions.
    """

    def __init__(
        self,
        omega_t: float = 1.0,
    ):

        self.omega_t = float(omega_t)

    def geometric_factor(
        self,
        state,
    ) -> float:
        """
        Return the current geometric magnitude.
        """

        m = (

            state.mx ** 2
            + state.my ** 2
            + state.mz ** 2

        )

        a = (

            state.ax ** 2
            + state.ay ** 2
            + state.az ** 2

        )

        return math.sqrt(
            m + a
        )

    def xi(
        self,
        state,
    ) -> float:
        """
        Current executable Ξ operator.
        """

        return (

            self.omega_t

            * self.geometric_factor(
                state
            )

        )

    def work(
        self,
        state,
    ) -> float:
        """
        Current toroidal work contribution.

        The manifold surface integral is
        presently approximated by the local
        field contribution.
        """

        return self.xi(
            state
        )

    def to_dict(
        self,
        state,
    ):

        return {

            "omega_t":
                self.omega_t,

            "geometry":
                self.geometric_factor(
                    state
                ),

            "xi":
                self.xi(
                    state
                ),

            "work":
                self.work(
                    state
                ),

        }

    def __repr__(self):

        return (

            "JUFEToroidalFlux("

            f"ΩT={self.omega_t}"

            ")"

        )