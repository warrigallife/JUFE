from __future__ import annotations

import math

import numpy as np


class JUFESensitivityMatrix:
    """
    JUFE Sensitivity Matrix

    Implements the executable form of

        δΨ = S · δE

    described in Manuscript 002.

    The sensitivity matrix determines how
    external perturbations influence the
    local manifold state.

    In addition to the existing ``apply``/``determinant``/
    ``catastrophic_transition``/``to_dict`` methods above (all
    unchanged), this class also offers an explicitly opt-in
    ``evaluate_bifurcation`` method. It is a native port of the
    bifurcation-detection calculation implemented in the separate
    ``abtm_expansion.py`` expansion/legacy module
    (``ABTM_Expansion.detect_bifurcation``), reproduced here without
    importing that module at runtime. It is NOT called from
    ``to_dict()`` and is NOT wired into ``ABTMEngine.evaluate()``;
    nothing in the default evaluation path calls it.
    """

    def __init__(
        self,
        matrix=None,
    ):

        if matrix is None:

            self.matrix = np.identity(6)

        else:

            self.matrix = np.asarray(
                matrix,
                dtype=float,
            )

            if self.matrix.shape != (6, 6):

                raise ValueError(
                    "Sensitivity matrix must be 6x6."
                )

    def apply(
        self,
        perturbation,
    ):
        """
        Apply an external perturbation.

        δΨ = S · δE
        """

        perturbation = np.asarray(
            perturbation,
            dtype=float,
        )

        if perturbation.shape != (6,):

            raise ValueError(
                "Perturbation vector must contain six values."
            )

        return self.matrix @ perturbation

    def determinant(self):

        return float(
            np.linalg.det(
                self.matrix
            )
        )

    def catastrophic_transition(
        self,
        tolerance: float = 1e-9,
    ):
        """
        Returns True when the manuscript
        catastrophic transition criterion
        is approached.

            det(S) → 0
        """

        return abs(
            self.determinant()
        ) <= tolerance

    def to_dict(self):

        return {

            "matrix":
                self.matrix.tolist(),

            "determinant":
                self.determinant(),

            "catastrophic_transition":
                self.catastrophic_transition(),

        }

    def evaluate_bifurcation(
        self,
        *,
        threshold,
    ):
        """
        Detect bifurcation approach: det(S) -> 0 (opt-in method).

        Native port of
        ``abtm_expansion.py :: ABTM_Expansion.detect_bifurcation``.
        That method's own docstring states it "Detect[s] det(S)
        approaching zero", computing::

            determinant = float(np.linalg.det(sensitivity))
            near_bifurcation = bool(abs(determinant) <= limit)

        This method reproduces that same rule directly in
        ``src/sensitivity_matrix.py`` -- ``abtm_expansion.py`` is never
        imported or called here.

        Unlike the legacy version (which accepts an arbitrary
        ``sensitivity_matrix`` argument of any square shape, and falls
        back to an instance-level ``bifurcation_threshold`` of ``1e-9``
        when its own ``threshold`` argument is omitted), this method
        operates on ``self.matrix`` -- the same matrix every other
        method on this class already operates on, which ``__init__``
        already restricts to exactly 6x6
        (``ValueError("Sensitivity matrix must be 6x6.")``). That
        existing 6x6 restriction is reused as-is here, not loosened or
        duplicated: since ``self.matrix`` can never be anything other
        than a validated 6x6 array by the time an instance exists,
        there is nothing further to validate about its shape in this
        method.

        ``threshold`` is REQUIRED and keyword-only, with no default and
        no invented manuscript constant, per:

        - DEF-0036 (Bifurcation Criterion), status "EXPLICIT LIMIT /
          UNRESOLVED THRESHOLD", which explicitly lists the "finite
          numerical threshold" as one of several Unresolved items for
          this criterion (alongside conditioning criterion, physical
          interpretation, and validation data).
        - REQ-TR-004 (Bifurcation), status "explicit_with_convention",
          manuscript_statement "det(S) -> 0 indicates transition to a
          nonlinear regime.", software_requirement "Calculate det(S)
          and compare to a declared threshold.", with open_questions
          listing "Physically justified determinant threshold".

        Because no physically justified threshold exists yet, this
        method never falls back to a default or to any legacy
        instance-level convention value -- the caller must supply one
        explicitly. Omitting ``threshold`` entirely raises Python's own
        ``TypeError`` for a missing required keyword-only argument;
        that is intentional, not a bug, and is not caught or replaced
        with an invented default here.

        Parameters
        ----------
        threshold:
            Keyword-only, REQUIRED. Must be finite and non-negative
            (matching the sign constraint implied by the legacy
            ``abs(determinant) <= limit`` comparison: a negative
            threshold could never be satisfied by a non-negative
            ``abs(...)`` value, so it is rejected explicitly rather
            than silently accepted as a threshold nothing can ever
            cross).

        Returns
        -------
        dict
            ``determinant``: float, ``det(self.matrix)``.

            ``threshold``: float, the caller-supplied threshold,
            echoed back verbatim.

            ``threshold_basis``: the literal string ``"PROVISIONAL"``
            -- see DEF-0036 / REQ-TR-004 above.

            ``near_bifurcation``: bool,
            ``abs(determinant) <= threshold`` -- note this is a
            less-than-or-EQUAL comparison (matching the legacy
            ``<=`` exactly, not ``<``), so a determinant whose absolute
            value equals the threshold exactly counts as
            near-bifurcation.

        Raises
        ------
        ValueError
            If ``threshold`` is not finite or is negative.
        TypeError
            If ``threshold`` is omitted entirely (no default value
            exists for it).
        """

        limit = float(threshold)

        if not math.isfinite(limit) or limit < 0:
            raise ValueError(
                "threshold must be a finite value greater than or "
                "equal to zero."
            )

        determinant = self.determinant()
        near_bifurcation = bool(abs(determinant) <= limit)

        return {

            "determinant": determinant,

            "threshold": limit,

            "threshold_basis": "PROVISIONAL",

            "near_bifurcation": near_bifurcation,

        }

    def __repr__(self):

        return (

            "JUFESensitivityMatrix("

            f"det={self.determinant():.6f}"

            ")"

        )