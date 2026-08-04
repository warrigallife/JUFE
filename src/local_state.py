from __future__ import annotations

from math import isfinite
from numbers import Real
from typing import Sequence


class JUFELocalState:
    """
    Six-component JUFE Local Field State.

    Canonical order:
        Mx, My, Mz, Ax, Ay, Az

    Implements:
        DEF-0003 — Six-Component Local Field State
        DEF-0014 — Phase-Difference Expression
        DEF-0015 — Local Phase-Equilibrium Condition
        DEF-0019 — Absolute Vacuum State
    """

    CANONICAL_COMPONENTS = (
        "Mx",
        "My",
        "Mz",
        "Ax",
        "Ay",
        "Az",
    )

    VALID_LIFECYCLE_STATES = {
        "ACTIVE",
        "VACUUM",
        "UNDEFINED",
    }

    def __init__(
        self,
        values: Sequence[Real],
        *,
        cell_coordinate=None,
        frame_index=None,
        lifecycle_state: str = "ACTIVE",
        mapping_version: str = "JUFE-LOCAL-1",
    ) -> None:

        if len(values) != 6:
            raise ValueError(
                "Local field state requires exactly six components "
                "in the order Mx, My, Mz, Ax, Ay, Az."
            )

        validated_values = []

        for value in values:
            if not isinstance(value, Real):
                raise TypeError(
                    "Every local field component must be numerical."
                )

            numeric_value = float(value)

            if not isfinite(numeric_value):
                raise ValueError(
                    "Every local field component must be finite."
                )

            validated_values.append(numeric_value)

        lifecycle_state = lifecycle_state.upper()

        if lifecycle_state not in self.VALID_LIFECYCLE_STATES:
            raise ValueError(
                "lifecycle_state must be ACTIVE, VACUUM, or UNDEFINED."
            )

        self.values = validated_values

        (
            self.mx,
            self.my,
            self.mz,
            self.ax,
            self.ay,
            self.az,
        ) = validated_values

        self.cell_coordinate = cell_coordinate
        self.frame_index = frame_index
        self.lifecycle_state = lifecycle_state
        self.mapping_version = mapping_version

        self.transformation = None

        if self.lifecycle_state == "VACUUM" and not self.is_vacuum():
            raise ValueError(
                "A VACUUM lifecycle state requires all six components "
                "to equal zero."
            )

    @property
    def compressive(self) -> tuple[float, float, float]:
        """
        Return the compressive vector M.
        """

        return (
            self.mx,
            self.my,
            self.mz,
        )

    @property
    def repulsive(self) -> tuple[float, float, float]:
        """
        Return the repulsive vector A.
        """

        return (
            self.ax,
            self.ay,
            self.az,
        )

    def phase_difference(self) -> list[float]:
        """
        Return the explicit phase-difference expression:

            Delta = M - A
        """

        return [
            self.mx - self.ax,
            self.my - self.ay,
            self.mz - self.az,
        ]

    def is_phase_equilibrium(self) -> bool:
        """
        Test the exact local phase-equilibrium condition:

            M = A

        No numerical tolerance is assumed.
        """

        return self.phase_difference() == [
            0.0,
            0.0,
            0.0,
        ]

    def is_phase_equilibrium_with_tolerance(
        self,
        tolerance: float,
    ) -> bool:
        """
        Test phase equilibrium using an explicitly supplied
        provisional numerical tolerance.
        """

        if tolerance < 0:
            raise ValueError(
                "tolerance must be greater than or equal to zero."
            )

        return all(
            abs(component) <= tolerance
            for component in self.phase_difference()
        )

    def is_vacuum(self) -> bool:
        """
        Test the provisional six-zero vacuum representation.

        Phase equilibrium and vacuum are not equivalent:
        equal non-zero M and A vectors are phase-locked but not vacuum.
        """

        return all(
            value == 0.0
            for value in self.values
        )

    def to_dict(self) -> dict:
        """
        Return the canonical state and audit metadata.
        """

        return {
            "Mx": self.mx,
            "My": self.my,
            "Mz": self.mz,
            "Ax": self.ax,
            "Ay": self.ay,
            "Az": self.az,
            "cell_coordinate": self.cell_coordinate,
            "frame_index": self.frame_index,
            "lifecycle_state": self.lifecycle_state,
            "mapping_version": self.mapping_version,
            "transformation": self.transformation,
            "phase_difference": self.phase_difference(),
            "phase_equilibrium": self.is_phase_equilibrium(),
            "vacuum": self.is_vacuum(),
        }

    def __repr__(self) -> str:
        return (
            "JUFELocalState("
            f"values={self.values}, "
            f"lifecycle_state='{self.lifecycle_state}', "
            f"frame_index={self.frame_index}, "
            f"mapping_version='{self.mapping_version}'"
            ")"
        )