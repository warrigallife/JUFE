from __future__ import annotations

from copy import deepcopy


class JUFETransformation:
    """
    JUFE Transformation

    Implements the current manuscript transformation
    stage.

    The present executable implementation performs
    the canonical identity mapping while preserving
    transformation provenance.

    Future manuscript transformation operators
    replace only the mapping section of this class.
    """

    def __init__(self, name="Identity"):

        self.name = name

    def apply(self, state):
        """
        Apply the current transformation.

        Returns a new Local Field State while
        preserving the original state.
        """

        new_state = deepcopy(state)

        #
        # Record transformation provenance.
        #

        new_state.transformation = self.name

        #
        # Current manuscript implementation.
        #
        # Identity mapping.
        #

        new_state.values = list(state.values)

        (
            new_state.mx,
            new_state.my,
            new_state.mz,
            new_state.ax,
            new_state.ay,
            new_state.az,
        ) = new_state.values

        return new_state

    def __repr__(self):

        return (
            f"JUFETransformation("
            f"name='{self.name}')"
        )