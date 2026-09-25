from __future__ import annotations

import math


class JUFEFieldGradient:
    """
    JUFE Field Gradient

    Implements the local gradient mechanics
    defined in Manuscript 002.

    Current implementation:

        D = -k ∇M

    where the compressive field M dominates
    local propagation.

    In addition to the existing ``gradient``/``propagation_vector``/
    ``magnitude``/``dominant``/``to_dict`` methods above (all
    unchanged), this class also offers an explicitly opt-in
    ``evaluate_dominance`` method. It is a native port of the
    dominance-ratio calculation implemented in the separate
    ``abtm_expansion.py`` expansion/legacy module
    (``ABTM_Expansion.dominance_ratio`` and
    ``ABTM_Expansion.local_gradient_dominates``), reproduced here
    without importing that module at runtime. It is NOT called from
    ``to_dict()`` and is NOT wired into ``ABTMEngine.evaluate()``;
    nothing in the default evaluation path calls it.
    """

    def __init__(
        self,
        coupling: float = 1.0,
    ):

        self.coupling = float(coupling)

    def gradient(
        self,
        state,
    ):
        """
        Return the local gradient vector.

        Current implementation assumes the
        Local Field State already represents
        the local field sample.
        """

        return (

            state.mx,

            state.my,

            state.mz,

        )

    def propagation_vector(
        self,
        state,
    ):
        """
        Compute

            D = -k ∇M
        """

        gx, gy, gz = self.gradient(
            state
        )

        k = self.coupling

        return (

            -k * gx,

            -k * gy,

            -k * gz,

        )

    def magnitude(
        self,
        state,
    ):

        gx, gy, gz = self.gradient(
            state
        )

        return math.sqrt(

            gx * gx

            + gy * gy

            + gz * gz

        )

    def dominant(
        self,
        state,
    ):
        """
        Returns True when

            |M| > |A|

        representing manuscript gradient
        dominance.
        """

        m = math.sqrt(

            state.mx ** 2

            + state.my ** 2

            + state.mz ** 2

        )

        a = math.sqrt(

            state.ax ** 2

            + state.ay ** 2

            + state.az ** 2

        )

        return m > a

    def to_dict(
        self,
        state,
    ):

        return {

            "gradient": self.gradient(
                state
            ),

            "propagation": self.propagation_vector(
                state
            ),

            "magnitude": self.magnitude(
                state
            ),

            "gradient_dominance": self.dominant(
                state
            ),

        }

    def evaluate_dominance(
        self,
        state,
        *,
        threshold,
    ):
        """
        Evaluate the M/A dominance ratio for ONE supplied state
        against an explicit, caller-required threshold (opt-in
        method).

        Native port of
        ``abtm_expansion.py :: ABTM_Expansion.dominance_ratio`` and
        ``ABTM_Expansion.local_gradient_dominates``. Those methods'
        own logic (read directly from source, not assumed):

            dominance_ratio(compressive_field, repulsive_field):
                numerator = ||compressive_field||
                denominator = ||repulsive_field||
                if denominator == 0:
                    return inf if numerator > 0 else 1.0
                return numerator / denominator

            local_gradient_dominates(..., *, dominance_threshold):
                # "Check ||M|| / ||A|| >= dominance_threshold."
                return dominance_ratio(...) >= dominance_threshold

        This method reproduces that same ratio, that same
        zero-denominator handling, and that same ``>=`` comparison
        directly in ``src/field_gradient.py`` -- ``abtm_expansion.py``
        is never imported or called here. Unlike this class's existing
        ``dominant(state)`` (which tests the strict inequality
        ``|M| > |A|`` with NO threshold at all, and is unchanged by
        this addition), this method requires an explicit threshold and
        uses ``>=``, matching the legacy ``local_gradient_dominates``
        exactly rather than ``dominant()``'s own different rule.

        REQ-TH-001 (Local gradient dominance), status
        "partially_defined", gives the manuscript statement as::

            "When ||M_local|| >> ||A_local||, trajectory follows
            -k grad(M_local)."

        with software_requirement::

            "Compare field norms and declare dominance only against an
            explicit threshold."

        and open_questions ``["Numerical definition of 'much greater
        than'"]``. This method IS that comparison: it computes
        ``||M|| / ||A||`` for the supplied state's own compressive and
        repulsive vectors and declares dominance only against the
        caller-supplied ``threshold`` -- never against an invented
        default, since REQ-TH-001 itself records the numerical
        definition of "much greater than" as an open question.

        Scope boundary against DEF-0007 (Local Gradient Dominance,
        status ACTIVE): DEF-0007 defines Local Gradient Dominance as
        "the manuscript-defined mechanism by which the trajectory of a
        field manifestation is governed by the dominant local tension
        gradient of the **surrounding field** rather than by intrinsic
        particle properties" (emphasis added), and its own Scope
        section explicitly states it does not define "quantitative
        dominance thresholds; computational implementation; numerical
        simulation algorithms; software architecture; engineering
        constraints beyond the manuscript statements." This method
        does NOT implement that broader surrounding-field-vs-particle
        framing: it compares the M and A vectors already carried by
        ONE supplied ``state`` object, with no notion of a separate
        "surrounding field," no spatial neighbours, no topology, and no
        boundary/jam mechanics. That is a deliberate scope boundary,
        not an oversight -- this method operationalizes only
        REQ-TH-001's explicit-threshold field-norm comparison, and
        leaves DEF-0007's wider mechanism (which its own Repository
        Status records as "Engineering Formalization: PROVISIONAL" and
        "Mathematical Generalization: UNRESOLVED") untouched.

        This method must NOT be read as implementing a spatial
        gradient, a new propagation calculation, a boundary jam, or any
        topology -- it is scoped strictly to the M/A dominance-ratio
        comparison on the one supplied state, exactly like
        ``dominance_ratio``/``local_gradient_dominates`` are scoped in
        the legacy source.

        Parameters
        ----------
        state:
            The Local Field State supplying the compressive
            (``state.compressive``, M) and repulsive
            (``state.repulsive``, A) vectors to compare. Not mutated.
        threshold:
            Keyword-only, REQUIRED -- no default, matching
            REQ-TH-001's own open question about the numerical
            definition of "much greater than". Must be finite and
            non-negative (mirroring the legacy
            ``local_gradient_dominates``'s own validation of
            ``dominance_threshold``, though this method uses this
            session's own established message wording rather than the
            legacy's distinct "dominance_threshold must be finite and
            non-negative." text).

        Returns
        -------
        dict
            ``compressive_norm``: float, ``||M||``.

            ``repulsive_norm``: float, ``||A||``.

            ``ratio``: float, ``||M|| / ||A||`` -- ``float("inf")``
            when ``||A|| == 0`` and ``||M|| > 0``; exactly ``1.0`` when
            both norms are zero; otherwise the plain quotient.

            ``threshold``: float, the caller-supplied threshold,
            echoed back verbatim.

            ``threshold_basis``: the literal string ``"PROVISIONAL"``.

            ``dominant``: bool, ``ratio >= threshold``.

        Raises
        ------
        ValueError
            If ``threshold`` is not finite or is negative.
        TypeError
            If ``threshold`` is omitted entirely (no default value
            exists for it) -- intentional, not a bug: REQ-TH-001
            records the numerical "much greater than" threshold as an
            open question, so this method never invents one.
        """

        limit = float(threshold)

        if not math.isfinite(limit) or limit < 0:
            raise ValueError(
                "threshold must be a finite value greater than or "
                "equal to zero."
            )

        mx, my, mz = state.compressive
        ax, ay, az = state.repulsive

        compressive_norm = math.sqrt(mx * mx + my * my + mz * mz)
        repulsive_norm = math.sqrt(ax * ax + ay * ay + az * az)

        if repulsive_norm == 0:
            ratio = float("inf") if compressive_norm > 0 else 1.0
        else:
            ratio = compressive_norm / repulsive_norm

        dominant = bool(ratio >= limit)

        return {

            "compressive_norm": compressive_norm,

            "repulsive_norm": repulsive_norm,

            "ratio": ratio,

            "threshold": limit,

            "threshold_basis": "PROVISIONAL",

            "dominant": dominant,

        }