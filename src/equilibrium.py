from __future__ import annotations


class JUFEEquilibrium:
    """
    JUFE Equilibrium

    Implements the current manuscript equilibrium
    condition for a single Local Field State.

    Equilibrium is satisfied when the compressive
    and repulsive components are in exact local
    phase equilibrium.
    """

    def __init__(self):

        self.name = "Equilibrium"

    def evaluate(self, state):
        """
        Evaluate the Local Field State.

        Returns
        -------
        bool
            True when the Local Field State
            satisfies the current manuscript
            equilibrium condition.
        """

        #
        # State must provide the manuscript API.
        #

        if not hasattr(state, "is_phase_equilibrium"):
            return False

        #
        # Respect explicitly undefined states.
        #

        if getattr(
            state,
            "lifecycle_state",
            "ACTIVE",
        ) == "UNDEFINED":
            return False

        #
        # Exact manuscript equilibrium.
        #

        return state.is_phase_equilibrium()

    def __repr__(self):

        return "JUFEEquilibrium()"