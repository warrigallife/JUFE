from __future__ import annotations


class JUFEConservation:
    """
    JUFE Conservation

    Implements the current manuscript conservation
    condition between two successive Local Field States.

    Conservation requires that the canonical
    six-component Local Field State is preserved
    through the applied transformation.
    """

    def __init__(self):

        self.name = "Conservation"

    def verify(self, before, after):
        """
        Verify conservation between two Local Field States.

        Returns
        -------
        bool
            True when the canonical Local Field State
            has been conserved.
        """

        #
        # Both objects must expose the manuscript API.
        #

        if not hasattr(before, "values"):
            return False

        if not hasattr(after, "values"):
            return False

        #
        # Canonical dimensionality.
        #

        if len(before.values) != 6:
            return False

        if len(after.values) != 6:
            return False

        #
        # Current manuscript implementation.
        #
        # The identity transformation preserves
        # every canonical component.
        #

        return before.values == after.values

    def __repr__(self):

        return "JUFEConservation()"