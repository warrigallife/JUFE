from __future__ import annotations


class JUFEPhaseLock:
    """
    JUFE Phase Lock

    Implements the manuscript phase-lock mechanics.

    A Local Field State phase-locks when

        M - A = 0

    At that instant the state becomes a
    candidate for harmonic ejection while
    preserving information.
    """

    def __init__(self):

        self.name = "Phase Lock"

    def locked(
        self,
        state,
    ) -> bool:
        """
        Exact manuscript phase-lock condition.
        """

        return state.is_phase_equilibrium()

    def harmonic_packet(
        self,
        state,
    ):
        """
        Construct the preserved harmonic packet.

        Current implementation preserves the
        complete Local Field State.
        """

        return state.to_dict()

    def vacuum_state(
        self,
    ):
        """
        Return the canonical vacuum state.
        """

        return [

            0.0,

            0.0,

            0.0,

            0.0,

            0.0,

            0.0,

        ]

    def eject(
        self,
        state,
    ):
        """
        Execute manuscript phase-lock behaviour.

        If phase lock has not been reached,
        no ejection occurs.
        """

        if not self.locked(state):

            return None

        return {

            "vacuum": self.vacuum_state(),

            "packet": self.harmonic_packet(
                state
            ),

            "phase_locked": True,

        }

    def __repr__(self):

        return "JUFEPhaseLock()"