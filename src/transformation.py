from __future__ import annotations

import math
from copy import deepcopy

import numpy as np


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

    In addition to the default identity mapping (``apply``), this class
    also offers an explicitly opt-in ``apply_coupled_field_step`` mode.
    It is a native port of the coupled-field evolution rule found in the
    separate ``abtm_expansion.py`` expansion/legacy module
    (``ABTM_Expansion.coupled_field_step``), reproduced here without
    importing that module at runtime. It is NOT wired into
    ``ABTMEngine.evaluate()``; nothing in the default evaluation path
    calls it, and ``apply`` itself is unchanged.
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

    def apply_coupled_field_step(
        self,
        state,
        compressive_rate,
        *,
        dt,
    ):
        """
        Apply the coupled-field evolution step (opt-in mode).

        Native port of ``abtm_expansion.py :: ABTM_Expansion.coupled_field_step``.
        That module's own docstring gives the manuscript basis as:

            dM/dt = -dA/dt

            Therefore:
                M_next = M + dM/dt * dt
                A_next = A - dM/dt * dt

        This method reproduces that same rule and that same validation
        directly in ``src/transformation.py`` -- ``abtm_expansion.py`` is
        never imported or called by this method.

        Unlike ``apply`` (and unlike the legacy ``coupled_field_step``,
        which is a ``classmethod``), this is a regular instance method,
        matching the calling convention already established by ``apply``
        on this class. The legacy source computes over bare NumPy
        arrays of any matching shape; here the compressive/repulsive
        fields are taken from the supplied Local Field State's own
        three-component ``compressive`` (M) and ``repulsive`` (A)
        vectors, and ``compressive_rate`` (dM/dt) must match that same
        three-component shape.

        Parameters
        ----------
        state:
            The Local Field State supplying the current M and A
            vectors. The supplied object is not mutated; a new state is
            returned, exactly as ``apply`` already does.
        compressive_rate:
            dM/dt, a three-component sequence matching the shape of the
            state's compressive vector.
        dt:
            Keyword-only step size. Must be finite and non-negative,
            exactly as validated by ``coupled_field_step``. ``dt == 0``
            yields ``delta == 0``, i.e. M and A are numerically
            unchanged (transformation provenance is still updated).

        Returns
        -------
        A new Local Field State with M and A advanced by one coupled
        step, and ``transformation`` recorded as
        ``"CoupledFieldStep"``.

        Raises
        ------
        ValueError
            If ``compressive_field``, ``repulsive_field``, or
            ``compressive_rate`` is empty, contains non-finite values,
            or the three do not share a matching shape; or if ``dt`` is
            not finite or is negative -- the same conditions, in the
            same order, and with the same messages as
            ``coupled_field_step``.
        """

        compressive_field = np.asarray(state.compressive, dtype=float)
        repulsive_field = np.asarray(state.repulsive, dtype=float)
        rate = np.asarray(compressive_rate, dtype=float)

        for array, label in (
            (compressive_field, "compressive_field"),
            (repulsive_field, "repulsive_field"),
            (rate, "compressive_rate"),
        ):
            if array.size == 0:
                raise ValueError(f"{label} must not be empty.")
            if not np.all(np.isfinite(array)):
                raise ValueError(f"{label} must contain only finite numbers.")

        if (
            compressive_field.shape != repulsive_field.shape
            or compressive_field.shape != rate.shape
        ):
            raise ValueError(
                "compressive_field, repulsive_field, and compressive_rate "
                "must have matching shapes."
            )

        time_step = float(dt)

        if not math.isfinite(time_step) or time_step < 0:
            raise ValueError("dt must be finite and non-negative.")

        delta = rate * time_step

        next_compressive = compressive_field + delta
        next_repulsive = repulsive_field - delta

        new_state = deepcopy(state)

        #
        # Record transformation provenance.
        #

        new_state.transformation = "CoupledFieldStep"

        new_state.values = [
            float(next_compressive[0]),
            float(next_compressive[1]),
            float(next_compressive[2]),
            float(next_repulsive[0]),
            float(next_repulsive[1]),
            float(next_repulsive[2]),
        ]

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