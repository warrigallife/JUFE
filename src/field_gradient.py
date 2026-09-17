from __future__ import annotations

import math


class JUFEFieldGradient:
    """
    JUFE Field Gradient

    Implements the local gradient mechanics
    defined in Manuscript 002.

    Current implementation:

        D = -k ∇M

    where the compressive field M dominates
    local propagation.
    """

    def __init__(
        self,
        coupling: float = 1.0,
    ):

        self.coupling = float(coupling)

    def gradient(
        self,
        state,
    ):
        """
        Return the local gradient vector.

        Current implementation assumes the
        Local Field State already represents
        the local field sample.
        """

        return (

            state.mx,

            state.my,

            state.mz,

        )

    def propagation_vector(
        self,
        state,
    ):
        """
        Compute

            D = -k ∇M
        """

        gx, gy, gz = self.gradient(
            state
        )

        k = self.coupling

        return (

            -k * gx,

            -k * gy,

            -k * gz,

        )

    def magnitude(
        self,
        state,
    ):

        gx, gy, gz = self.gradient(
            state
        )

        return math.sqrt(

            gx * gx

            + gy * gy

            + gz * gz

        )

    def dominant(
        self,
        state,
    ):
        """
        Returns True when

            |M| > |A|

        representing manuscript gradient
        dominance.
        """

        m = math.sqrt(

            state.mx ** 2

            + state.my ** 2

            + state.mz ** 2

        )

        a = math.sqrt(

            state.ax ** 2

            + state.ay ** 2

            + state.az ** 2

        )

        return m > a

    def to_dict(
        self,
        state,
    ):

        return {

            "gradient": self.gradient(
                state
            ),

            "propagation": self.propagation_vector(
                state
            ),

            "magnitude": self.magnitude(
                state
            ),

            "gradient_dominance": self.dominant(
                state
            ),

        }