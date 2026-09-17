from __future__ import annotations


class JUFEGlobalConservation:
    """
    JUFE Global Conservation

    Implements the global conservation identity
    defined in Manuscript 002.

        Σ(M + A) ≡ 0

    across the evaluated manifold.
    """

    def __init__(self):

        self.name = "Global Conservation"

    def total_field(self, states):
        """
        Return the global field sum.
        """

        total = 0.0

        for state in states:

            total += sum(state.values)

        return total

    def verify(
        self,
        states,
        tolerance: float = 1e-12,
    ):
        """
        Verify the global conservation identity.
        """

        total = self.total_field(
            states
        )

        return abs(total) <= tolerance

    def residual(
        self,
        states,
    ):

        return self.total_field(
            states
        )

    def to_dict(
        self,
        states,
    ):

        return {

            "global_sum": self.total_field(
                states
            ),

            "conserved": self.verify(
                states
            ),

            "residual": self.residual(
                states
            ),

        }

    def __repr__(self):

        return "JUFEGlobalConservation()"