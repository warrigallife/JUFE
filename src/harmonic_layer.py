from __future__ import annotations

import math


class JUFEHarmonicLayer:
    """
    JUFE Harmonic Layer

    Implements the executable Mod-7 temporal
    harmonic architecture described in
    Manuscript 002.

    This layer represents the temporal
    harmonic modulation acting on the
    otherwise static Z6 structural lattice.
    """

    def __init__(
        self,
        harmonic: int = 0,
    ):

        self.set_harmonic(
            harmonic
        )

    def set_harmonic(
        self,
        harmonic: int,
    ):

        self.harmonic = int(
            harmonic
        ) % 7

    def phase(
        self):

        return (

            2.0
            * math.pi
            * self.harmonic
            / 7.0

        )

    def modulation_factor(
        self,
    ):

        return math.cos(
            self.phase()
        )

    def advance(
        self,
        steps: int = 1,
    ):

        self.harmonic = (

            self.harmonic
            + steps

        ) % 7

    def reset(
        self,
    ):

        self.harmonic = 0

    def to_dict(
        self,
    ):

        return {

            "harmonic":

                self.harmonic,

            "phase":

                self.phase(),

            "modulation":

                self.modulation_factor(),

        }

    def __repr__(
        self,
    ):

        return (

            "JUFEHarmonicLayer("

            f"mod7={self.harmonic}"

            ")"

        )