from __future__ import annotations

import math

import numpy as np


class JUFEGlobalConservation:
    """
    JUFE Global Conservation

    Implements the global conservation identity
    defined in Manuscript 002.

        Σ(M + A) ≡ 0

    across the evaluated manifold.

    In addition to the existing scalar-only identity above (used by
    ``total_field``, ``verify``, ``residual``, and ``to_dict`` -- all
    unchanged), this class also offers an explicitly opt-in
    ``global_field_balance`` method. It is a native port of the
    scalar-plus-component-wise calculation implemented in the separate
    ``abtm_expansion.py`` expansion/legacy module
    (``ABTM_Expansion.global_field_balance``), reproduced here without
    importing that module at runtime. It is NOT wired into
    ``ABTMEngine.evaluate()``; nothing in the default evaluation path
    calls it, and ``total_field``/``verify``/``residual``/``to_dict``
    are unchanged.
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

    def global_field_balance(
        self,
        states,
        *,
        tolerance,
    ):
        """
        Evaluate both interpretations of the global conservation
        identity, distinctly and separately (opt-in method).

        Native port of
        ``abtm_expansion.py :: ABTM_Expansion.global_field_balance``.
        That method's own docstring states it evaluates both
        interpretations of the supplied global identity::

            scalar:
                sum_global sum_i (M_i + A_i) = 0

            component-wise:
                sum_global (M + A) = vector(0)

        This method reproduces that same rule and that same validation
        directly in ``src/global_conservation.py`` --
        ``abtm_expansion.py`` is never imported or called here.

        Unlike ``total_field``/``verify``/``residual``/``to_dict``
        (which operate on the flattened six-component
        ``state.values`` and only ever report one scalar-only
        "conserved" verdict), this method reads each state's own
        three-component ``compressive`` (M) and ``repulsive`` (A)
        vectors and reports the scalar verdict and the component-wise
        verdict AS TWO INDEPENDENT RESULTS. They are never collapsed
        into a single authoritative boolean: a state collection can be
        scalar-balanced while being component-unbalanced, or vice
        versa (see the "divergent verdict" tests in this change's test
        file for constructed examples of both).

        The legacy source accepts raw ``compressive_fields`` /
        ``repulsive_fields`` arrays of any shape whose final axis is
        exactly 3. This port adapts that to the ``states``-list
        convention already used by every other method on this class:
        one row of the effective (N, 3) arrays per supplied state,
        taken from that state's own ``compressive`` / ``repulsive``
        properties, matching the existing per-state, no-hasattr-guard
        access style already used by ``total_field`` above.

        Parameters
        ----------
        states:
            A non-empty sequence of Local Field State-like objects,
            each exposing three-component ``compressive`` (M) and
            ``repulsive`` (A) properties.
        tolerance:
            Keyword-only, REQUIRED -- there is no default. The legacy
            source falls back to an instance-level
            ``equilibrium_tolerance`` (default ``1e-9``) when its own
            ``tolerance`` argument is omitted; this port does not
            reproduce that fallback, since this class has no equivalent
            configured instance tolerance. The caller must supply an
            explicit value; omitting it raises
            ``TypeError`` (Python's own missing-required-keyword-only-
            argument error), and an explicitly invalid value (not
            finite, or negative) raises ``ValueError``. The tolerance
            actually used is always echoed back verbatim in the
            returned mapping under ``"tolerance"``, alongside a
            ``"tolerance_basis": "PROVISIONAL"`` label -- this
            tolerance is a runtime convenience threshold, not a value
            defined by the manuscript.

        Returns
        -------
        dict
            ``scalar_total``: float, sum_global sum_i (M_i + A_i).

            ``component_total``: list[float] of length 3, the
            component-wise sum_global (M + A) vector.

            ``scalar_residual``: float, identical to ``scalar_total``
            (the conservation target is exactly zero, so the residual
            from that target equals the total itself -- the same
            relationship already used by this class's own
            ``residual()``, which mirrors ``total_field()``).

            ``component_residual``: list[float] of length 3, identical
            to ``component_total``, for the same reason.

            ``tolerance``: float, the caller-supplied tolerance,
            echoed back.

            ``tolerance_basis``: the literal string ``"PROVISIONAL"``.

            ``scalar_balanced``: bool, ``abs(scalar_total) <=
            tolerance``.

            ``component_balanced``: bool,
            ``norm(component_total) <= tolerance`` -- computed and
            reported completely independently of ``scalar_balanced``.

        Raises
        ------
        ValueError
            If ``states`` is empty; if any compressive/repulsive
            component is not finite; if the compressive and repulsive
            vectors do not share a matching shape; if either vector's
            final axis is not exactly 3 components; or if ``tolerance``
            is not finite or is negative -- matching the legacy
            source's conditions and message text.
        TypeError
            If ``tolerance`` is omitted entirely (no default value
            exists for it).
        """

        if len(states) == 0:
            raise ValueError("compressive_fields must not be empty.")

        compressive_rows = [
            list(state.compressive) for state in states
        ]
        repulsive_rows = [
            list(state.repulsive) for state in states
        ]

        compressive_fields = np.asarray(compressive_rows, dtype=float)
        repulsive_fields = np.asarray(repulsive_rows, dtype=float)

        if compressive_fields.size == 0:
            raise ValueError("compressive_fields must not be empty.")
        if not np.all(np.isfinite(compressive_fields)):
            raise ValueError(
                "compressive_fields must contain only finite numbers."
            )

        if repulsive_fields.size == 0:
            raise ValueError("repulsive_fields must not be empty.")
        if not np.all(np.isfinite(repulsive_fields)):
            raise ValueError(
                "repulsive_fields must contain only finite numbers."
            )

        if compressive_fields.shape != repulsive_fields.shape:
            raise ValueError(
                "compressive_fields and repulsive_fields must have "
                "matching shapes."
            )
        if compressive_fields.shape[-1] != 3:
            raise ValueError(
                "The final axis must contain x, y, z components."
            )

        tol = float(tolerance)
        if not math.isfinite(tol) or tol < 0:
            raise ValueError(
                "tolerance must be a finite value greater than or "
                "equal to zero."
            )

        combined = compressive_fields + repulsive_fields
        component_total = np.sum(combined, axis=0)
        scalar_total = float(np.sum(component_total))

        component_total_list = [float(value) for value in component_total]

        scalar_balanced = bool(abs(scalar_total) <= tol)
        component_balanced = bool(
            np.linalg.norm(component_total) <= tol
        )

        return {

            "scalar_total": scalar_total,

            "component_total": component_total_list,

            "scalar_residual": scalar_total,

            "component_residual": list(component_total_list),

            "tolerance": tol,

            "tolerance_basis": "PROVISIONAL",

            "scalar_balanced": scalar_balanced,

            "component_balanced": component_balanced,

        }

    def __repr__(self):

        return "JUFEGlobalConservation()"