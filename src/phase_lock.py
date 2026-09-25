from __future__ import annotations

import math


class JUFEPhaseLock:
    """
    JUFE Phase Lock

    Implements the manuscript phase-lock mechanics.

    A Local Field State phase-locks when

        M - A = 0

    At that instant the state becomes a
    candidate for harmonic ejection while
    preserving information.

    In addition to the existing ``locked``/``harmonic_packet``/
    ``vacuum_state``/``eject`` methods above (all unchanged), this
    class also offers an explicitly opt-in ``evaluate_phase_lock``
    method. It is a native port of the L2-norm residual calculation
    implemented in the separate ``abtm_expansion.py`` expansion/legacy
    module (``ABTM_Expansion.phase_lock``), reproduced here without
    importing that module at runtime. It does NOT touch
    ``JUFEHarmonicLayer``, ``mod7_phase``, harmonic packets, vacuum
    representation, lifecycle logic, topology, or ``eject()``; it is
    NOT wired into ``ABTMEngine.evaluate()``; nothing in the default
    evaluation path calls it.
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

    def evaluate_phase_lock(
        self,
        state,
        *,
        tolerance,
    ):
        """
        Evaluate the M/A residual against the L2-norm phase-lock
        tolerance audit (opt-in method).

        Native port of
        ``abtm_expansion.py :: ABTM_Expansion.phase_lock``. That
        method's own docstring states it checks::

            ||M - A|| <= tolerance

        computing::

            residual = M - A
            residual_norm = ||residual||_2
            locked = residual_norm <= tolerance

        This method reproduces that same residual, that same L2-norm
        computation, and that same ``<=`` comparison directly in
        ``src/phase_lock.py`` -- ``abtm_expansion.py`` is never
        imported or called here.

        REQ-TR-002 (Phase lock), status "explicit_with_convention",
        gives the manuscript statement as::

            "lim_(t->t_lock)(M(t)-A(t))=0."

        with software_requirement::

            "Calculate ||M-A|| and compare with a declared tolerance."

        and open_questions ``["Physical basis of numerical tolerance"]``.

        TR-PHASE-001 (Phase-lock condition), status "explicit",
        mathematical_form ``"lim_(t->t_lock)(M(t) - A(t)) = 0"``,
        required_inputs ``("M", "A", "phase_lock_tolerance")``, outputs
        ``("phase_error", "locked")``, software_contract::

            "Calculate the residual M - A."
            "Use a declared tolerance and include it in every audit."

        This method IS that L2-norm audit: it calculates the residual
        ``M - A``, its L2 norm, and compares that norm against a
        caller-declared tolerance that is always echoed back in the
        result (satisfying "include it in every audit").

        This method does NOT replace the existing exact-equality
        runtime path, ``locked(state)`` above, which tests
        ``state.is_phase_equilibrium()`` (an EXACT ``M == A`` check
        with no tolerance at all, and is unchanged by this addition).

        This method also does NOT use
        ``JUFELocalState.is_phase_equilibrium_with_tolerance(tolerance)``,
        which implements a mathematically DIFFERENT criterion: it
        requires ``all(abs(component) <= tolerance for component in
        (M - A))`` -- an L-infinity (per-component / max-norm) check,
        not an L2-norm check. These two criteria are provably not
        equivalent:

        - L2-pass implies L-infinity-pass: if ``||residual||_2 <=
          tolerance``, then every individual component's absolute
          value is at most the vector's own L2 norm, so it is also
          at most ``tolerance``. This direction always holds.
        - L-infinity-pass does NOT imply L2-pass: a three-component
          residual with every component exactly equal to ``tolerance``
          (e.g. ``residual = (tolerance, tolerance, tolerance)``)
          satisfies the per-component check exactly, but has L2 norm
          ``tolerance * sqrt(3) ~= 1.732 * tolerance``, which exceeds
          ``tolerance`` whenever ``tolerance > 0``. So a state can pass
          ``is_phase_equilibrium_with_tolerance()`` while FAILING this
          method's ``locked`` result. (The reverse direction -- passing
          this method's L2 check while failing the per-component check
          -- is never possible, by the first bullet above.)

        This method must NOT be read as touching harmonic ejection,
        vacuum representation, or lifecycle logic; it is scoped
        strictly to the M/A residual L2-norm comparison on the one
        supplied state, exactly as ``phase_lock`` is scoped in the
        legacy source.

        Parameters
        ----------
        state:
            The Local Field State supplying the compressive
            (``state.compressive``, M) and repulsive
            (``state.repulsive``, A) vectors to compare. Not mutated.
        tolerance:
            Keyword-only, REQUIRED -- no default, matching REQ-TR-002's
            own open question about the physical basis of the
            numerical tolerance. Must be finite and non-negative.

        Returns
        -------
        dict
            ``residual``: list[float] of length 3, ``M - A``
            component-wise.

            ``residual_norm``: float, ``||residual||_2``.

            ``tolerance``: float, the caller-supplied tolerance,
            echoed back verbatim.

            ``tolerance_basis``: the literal string ``"PROVISIONAL"``.

            ``locked``: bool, ``residual_norm <= tolerance``.

        Raises
        ------
        ValueError
            If ``tolerance`` is not finite or is negative.
        TypeError
            If ``tolerance`` is omitted entirely (no default value
            exists for it) -- intentional, not a bug: REQ-TR-002
            records the physical basis of the numerical tolerance as
            an open question, so this method never invents one.
        """

        tol = float(tolerance)

        if not math.isfinite(tol) or tol < 0:
            raise ValueError(
                "tolerance must be a finite value greater than or "
                "equal to zero."
            )

        mx, my, mz = state.compressive
        ax, ay, az = state.repulsive

        residual = (mx - ax, my - ay, mz - az)
        residual_norm = math.sqrt(
            residual[0] ** 2 + residual[1] ** 2 + residual[2] ** 2
        )
        locked = bool(residual_norm <= tol)

        return {

            "residual": list(residual),

            "residual_norm": residual_norm,

            "tolerance": tol,

            "tolerance_basis": "PROVISIONAL",

            "locked": locked,

        }

    def __repr__(self):

        return "JUFEPhaseLock()"