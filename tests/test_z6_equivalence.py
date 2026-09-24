"""
Z6 trace-residue / manifold-stability equivalence characterization.

This file is TEST-ONLY. It does not modify, rename, or otherwise touch any
of the three implementations it exercises. It exists to determine -- by
running real inputs through all three and comparing outputs -- whether they
currently behave the same way, and to record plainly where they do not.

The three implementations under test
-------------------------------------

1. ``src/engines/abtm.py :: ABTMEngine.compute_manifold_stability``
   (the canonical src implementation)

   Read directly from source, the method is::

       def compute_manifold_stability(
           self,
           psi_barrier: np.ndarray,
       ) -> bool:
           if psi_barrier.ndim != 2:
               raise ValueError("psi_barrier must be a matrix.")
           sigma = np.trace(psi_barrier) % 6
           return sigma == 0

   - Bound instance method; requires an ``ABTMEngine()`` instance.
   - Only validation performed: ``psi_barrier.ndim != 2`` raises
     ``ValueError("psi_barrier must be a matrix.")``. This means the input
     must already expose a ``.ndim`` attribute (a NumPy array or
     array-like object) -- a plain Python list has no ``.ndim`` and raises
     ``AttributeError`` instead of the documented ``ValueError`` (see the
     domain-difference tests below).
   - Does NOT validate squareness, finiteness, or emptiness.
   - Does NOT expose the intermediate residue (``sigma``) separately --
     only the final boolean is returned.
   - The returned value is ``sigma == 0``, i.e. a ``numpy.bool_``
     (NumPy's boolean scalar type), not a native Python ``bool``.

2. ``oldmate1(5).py :: ABTM_Engine.compute_manifold_stability``
   (a legacy file with an unusual, parenthesised filename, found at the
   repository root; not importable with a normal ``import`` statement)

   Read directly from source, the method is::

       def compute_manifold_stability(self, psi_barrier):
           sigma = np.trace(psi_barrier) % 6
           return sigma == 0

   - Same arithmetic rule as src, but with NO explicit validation at all.
     Whatever ``numpy.trace`` does with the given input is what happens:
     a 1-D input raises NumPy's own ``ValueError`` ("diag requires an
     array of at least two dimensions"), not src's message; an N-D input
     with N > 2 does not raise at all and instead returns an array of
     booleans (see the domain-difference tests below).
   - Accepts plain Python nested lists directly (NumPy converts them
     internally), unlike src.
   - ``class ABTM_Engine(ABTM_Expansion):`` -- the file references
     ``ABTM_Expansion`` as a base class but never imports it. The file is
     NOT self-contained / independently importable; ``ABTM_Expansion``
     must be injected into the module's namespace before execution. This
     is exactly the situation the existing repository launcher scripts
     (``jufe_original_launcher.py``, ``jufe_abtm_master_flow.py``,
     ``jufe_abtm_optimized_master_flow.py``,
     ``jufe_abtm_results_launcher.py``, ``jufe_64_grid_mapper.py``,
     ``JUFE_RESEARCH/TOOLS/jufe_system_check.py``) already solve, each
     with its own ``load_oldmate1()`` helper following the same pattern:
     ``importlib.util.spec_from_file_location`` +
     ``importlib.util.module_from_spec``, set
     ``module.ABTM_Expansion = ABTM_Expansion`` on the freshly created
     module BEFORE ``exec_module`` runs (so the class statement can
     resolve the name), register the module in ``sys.modules``, then
     ``spec.loader.exec_module(module)``. This test file reuses that
     exact approach (see ``_load_oldmate1_module`` below) rather than
     inventing a new one.

3. ``abtm_expansion.py :: ABTM_Expansion.z6_trace_residue`` and
   ``ABTM_Expansion.z6_stable``
   (a legacy/expansion file at the repository root; normally importable)

   Read directly from source::

       @classmethod
       def z6_trace_residue(cls, psi_barrier: ArrayLike) -> float:
           matrix = cls.as_array(psi_barrier, name="psi_barrier")
           if matrix.ndim != 2:
               raise ValueError("psi_barrier must be a two-dimensional matrix.")
           return float(np.trace(matrix) % 6)

       @classmethod
       def z6_stable(cls, psi_barrier: ArrayLike) -> bool:
           return bool(np.isclose(cls.z6_trace_residue(psi_barrier), 0.0))

   - Both are ``classmethod``s; callable as ``ABTM_Expansion.z6_trace_residue(...)``
     with no instance required (unlike src and oldmate1, which are bound
     instance methods).
   - ``z6_trace_residue`` explicitly exposes the residue as a plain
     Python ``float`` -- the only one of the three call sites that
     returns the intermediate value at all.
   - Input validation goes through ``ABTM_Expansion.as_array``, which
     rejects EMPTY arrays (``ValueError("psi_barrier must not be
     empty.")``) and NON-FINITE entries (``ValueError("psi_barrier must
     contain only finite numbers.")``) -- both of which src and oldmate1
     silently accept.
   - ``z6_stable`` uses ``np.isclose(residue, 0.0)`` -- an
     approximate-tolerance comparison (NumPy defaults: ``rtol=1e-05``,
     ``atol=1e-08``) -- NOT the exact ``residue == 0`` equality that both
     src and oldmate1 use. For purely integer inputs this makes no
     observable difference (a nonzero integer residue is never within
     tolerance of zero), but for a residue that is a very small nonzero
     float, ``z6_stable`` can report "stable" while src and oldmate1
     report "unstable" for the identical input. This is demonstrated
     explicitly below and is NOT proven equivalence -- it is a
     documented disagreement.
   - Both accept plain Python nested lists (auto-converted via
     ``np.asarray`` inside ``as_array``).

Everything in this file is characterization only: it records what each
implementation currently does. No claim is made that any one of the three
behaviors is more "correct" than another, except where the task explicitly
asks for an equivalence verdict, which is reported in the class docstrings
below strictly on the basis of what the tests actually demonstrate.
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
import unittest
from pathlib import Path

import numpy as np

from src.engines.abtm import ABTMEngine
from abtm_expansion import ABTM_Expansion

REPO_ROOT = Path(__file__).resolve().parent.parent
OLDMATE1_PATH = REPO_ROOT / "oldmate1(5).py"


def _load_oldmate1_module():
    """
    Load oldmate1(5).py unchanged, exactly the way the repository's own
    launcher scripts already do (see e.g. jufe_original_launcher.py ::
    load_oldmate1()): supply the unresolved ABTM_Expansion base-class name
    through the module namespace before executing the file, since the
    file itself never imports it.

    The file is neither renamed, edited, nor copied -- it is executed
    from its real on-disk path, parentheses included.
    """

    if not OLDMATE1_PATH.is_file():
        raise FileNotFoundError(
            f"Expected legacy file not found: {OLDMATE1_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "jufe_test_oldmate1_original",
        OLDMATE1_PATH,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {OLDMATE1_PATH.name}")

    module = importlib.util.module_from_spec(spec)
    module.ABTM_Expansion = ABTM_Expansion
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_OLDMATE1_MODULE = _load_oldmate1_module()

SRC_ENGINE = ABTMEngine()
OLDMATE1_ENGINE = _OLDMATE1_MODULE.ABTM_Engine()


def _canonical_residue(matrix) -> int:
    """
    Recreate src's own arithmetic (sigma = trace(psi) % 6) independently,
    purely to have something to compare abtm_expansion's explicitly
    exposed z6_trace_residue() against -- src itself never returns the
    residue, only the final boolean.
    """

    return np.trace(np.asarray(matrix, dtype=float)) % 6


class SignatureAndReturnShapeDocumentationTests(unittest.TestCase):
    """
    Turns the signature/return-shape claims made in the module docstring
    above into executable checks via introspection, so the documentation
    cannot silently drift from the actual current source.
    """

    def test_src_compute_manifold_stability_signature(self):
        signature = inspect.signature(
            ABTMEngine.compute_manifold_stability
        )
        self.assertEqual(
            list(signature.parameters),
            ["self", "psi_barrier"],
        )
        self.assertEqual(
            signature.parameters["psi_barrier"].annotation,
            "np.ndarray",
        )
        self.assertEqual(signature.return_annotation, "bool")

    def test_oldmate1_compute_manifold_stability_signature(self):
        signature = inspect.signature(
            _OLDMATE1_MODULE.ABTM_Engine.compute_manifold_stability
        )
        self.assertEqual(
            list(signature.parameters),
            ["self", "psi_barrier"],
        )
        # Current behavior: no type annotations at all on this method.
        self.assertEqual(
            signature.parameters["psi_barrier"].annotation,
            inspect.Parameter.empty,
        )
        self.assertEqual(
            signature.return_annotation,
            inspect.Signature.empty,
        )

    def test_expansion_z6_functions_are_classmethods_with_explicit_types(self):
        residue_signature = inspect.signature(
            ABTM_Expansion.z6_trace_residue
        )
        stable_signature = inspect.signature(ABTM_Expansion.z6_stable)

        # classmethod: no "self" parameter when accessed via the class.
        self.assertEqual(list(residue_signature.parameters), ["psi_barrier"])
        self.assertEqual(list(stable_signature.parameters), ["psi_barrier"])
        self.assertEqual(residue_signature.return_annotation, "float")
        self.assertEqual(stable_signature.return_annotation, "bool")

    def test_oldmate1_class_requires_injected_abtm_expansion_base(self):
        # Current behavior: oldmate1(5).py's own source text never
        # imports ABTM_Expansion, yet its ABTM_Engine class is declared
        # as `class ABTM_Engine(ABTM_Expansion):`. Confirm the loaded
        # class really did resolve to abtm_expansion's own class (via
        # the injected module attribute), not some other definition.
        self.assertIn(
            ABTM_Expansion,
            _OLDMATE1_MODULE.ABTM_Engine.__mro__,
        )
        source_text = OLDMATE1_PATH.read_text(encoding="utf-8")
        self.assertIn("class ABTM_Engine(ABTM_Expansion):", source_text)
        # The file imports numpy/zlib/base64/json, but never imports the
        # name ABTM_Expansion itself -- confirm that specifically, rather
        # than assuming the file has no imports at all.
        self.assertNotIn("import ABTM_Expansion", source_text)
        self.assertNotIn("ABTM_Expansion import", source_text)


class FixedCaseEquivalenceTests(unittest.TestCase):
    """
    Fixed, explicitly named matrices, chosen to exercise the arithmetic
    rule (sigma = trace mod 6) at meaningful boundary points, run through
    all three implementations and compared over their SHARED valid input
    domain (i.e. inputs none of the three reject).

    Each case is restricted to plain finite integer-valued 2-D matrices,
    which is the input shape all three implementations accept without
    raising and without any tolerance ambiguity (see
    DomainAndTypeDifferenceTests below for the inputs that are NOT
    shared / NOT tolerance-safe, kept separate on purpose).
    """

    FIXED_CASES = {
        # trace = 1 + 1 = 2, 2 % 6 = 2 -> unstable. Trivial baseline case.
        "identity_2x2": (
            np.array([[1, 0], [0, 1]]),
            False,
        ),
        # trace = 0, 0 % 6 = 0 -> stable. Degenerate all-zero case.
        "zero_2x2": (
            np.array([[0, 0], [0, 0]]),
            True,
        ),
        # trace = 6, 6 % 6 = 0 -> stable. Smallest identity matrix whose
        # trace is an exact positive multiple of 6.
        "identity_6x6": (
            np.eye(6, dtype=int),
            True,
        ),
        # trace = 1 + 1 + 1 = 3, 3 % 6 = 3 -> unstable. Known-unstable
        # case built from nonzero diagonal entries (not just zero/identity).
        "diag_111_3x3": (
            np.diag([1, 1, 1]),
            False,
        ),
        # trace = -3 + -3 = -6, (-6) % 6 = 0 -> stable. Exercises negative
        # trace wrapping around to a stable residue, identically across
        # NumPy's modulo convention in all three implementations.
        "negative_wraparound_2x2": (
            np.array([[-3, 0], [0, -3]]),
            True,
        ),
        # trace = 1 + 5 = 6 (only the two on-diagonal entries count; the
        # extra column is not part of the trace), 6 % 6 = 0 -> stable.
        # None of the three implementations require a square matrix, so
        # this documents that a non-square 2-D input is accepted, not
        # rejected, by all three.
        "non_square_2x3": (
            np.array([[1, 2, 3], [4, 5, 6]]),
            True,
        ),
    }

    def test_fixed_cases_agree_across_all_three_implementations(self):
        for name, (matrix, expected_stable) in self.FIXED_CASES.items():
            with self.subTest(case=name):
                canonical_residue = _canonical_residue(matrix)
                self.assertEqual(
                    bool(canonical_residue == 0),
                    expected_stable,
                    f"{name}: fixture's own expected_stable disagrees "
                    "with the canonical formula; fixture is wrong.",
                )

                src_result = SRC_ENGINE.compute_manifold_stability(matrix)
                oldmate1_result = OLDMATE1_ENGINE.compute_manifold_stability(
                    matrix
                )
                expansion_residue = ABTM_Expansion.z6_trace_residue(matrix)
                expansion_stable = ABTM_Expansion.z6_stable(matrix)

                # Residue equivalence: src/oldmate1 do not expose a
                # residue directly, so compare the canonical formula
                # (independently reproduced from src's own source text)
                # against abtm_expansion's explicitly exposed residue.
                self.assertAlmostEqual(
                    float(canonical_residue),
                    expansion_residue,
                    places=9,
                    msg=f"{name}: residue mismatch",
                )

                # Boolean stability equivalence across all three.
                self.assertEqual(bool(src_result), expected_stable)
                self.assertEqual(bool(oldmate1_result), expected_stable)
                self.assertEqual(expansion_stable, expected_stable)


class GeneratedMatrixEquivalenceTests(unittest.TestCase):
    """
    At least 50 deterministic, seeded, integer square matrices (sizes
    2x2, 3x3, 4x4 -- all valid for every implementation, since none of
    the three require anything beyond a 2-D array; square is not
    required either, but square matrices keep the generated set simple
    and unambiguous), covering a mix of residues that are stable and
    unstable under the canonical (src) rule.

    NumPy is used for generation (via a fixed seed) rather than the
    stdlib `random` module because NumPy is already a hard runtime
    dependency of every implementation under test (src/engines/abtm.py,
    oldmate1(5).py, and abtm_expansion.py all import numpy directly),
    whereas this repository has no dependency on the stdlib `random`
    module anywhere in its source.
    """

    SEED = 20240924
    SIZES = (2, 3, 4)
    MATRICES_PER_SIZE = 20  # 3 sizes * 20 = 60 matrices, >= the required 50

    @classmethod
    def setUpClass(cls):
        rng = np.random.default_rng(cls.SEED)
        cls.matrices = [
            rng.integers(-9, 10, size=(size, size))
            for size in cls.SIZES
            for _ in range(cls.MATRICES_PER_SIZE)
        ]
        # Sanity check on the requirement itself: at least 50 matrices.
        assert len(cls.matrices) >= 50

    def test_generated_matrix_count_meets_minimum(self):
        self.assertGreaterEqual(len(self.matrices), 50)

    def test_generated_matrices_include_both_stable_and_unstable_cases(self):
        residues = [int(_canonical_residue(m)) for m in self.matrices]
        stable_count = sum(1 for r in residues if r == 0)
        unstable_count = sum(1 for r in residues if r != 0)

        self.assertGreater(
            stable_count,
            0,
            "Deterministic generation produced no stable-residue matrices; "
            "the mix requirement is not met for this seed.",
        )
        self.assertGreater(
            unstable_count,
            0,
            "Deterministic generation produced no unstable-residue "
            "matrices; the mix requirement is not met for this seed.",
        )

    def test_all_generated_matrices_agree_across_all_three_implementations(self):
        for index, matrix in enumerate(self.matrices):
            with self.subTest(index=index, shape=matrix.shape):
                canonical_residue = _canonical_residue(matrix)
                expected_stable = bool(canonical_residue == 0)

                src_result = SRC_ENGINE.compute_manifold_stability(matrix)
                oldmate1_result = OLDMATE1_ENGINE.compute_manifold_stability(
                    matrix
                )
                expansion_residue = ABTM_Expansion.z6_trace_residue(matrix)
                expansion_stable = ABTM_Expansion.z6_stable(matrix)

                self.assertAlmostEqual(
                    float(canonical_residue),
                    expansion_residue,
                    places=9,
                )
                self.assertEqual(bool(src_result), expected_stable)
                self.assertEqual(bool(oldmate1_result), expected_stable)
                self.assertEqual(expansion_stable, expected_stable)


class DomainAndTypeDifferenceTests(unittest.TestCase):
    """
    Explicit, clearly labeled documentation of where the three
    implementations DIFFER in accepted input domain, accepted types,
    validation behavior, error handling, or output type -- kept
    completely separate from the equivalence tests above so that a
    passing equivalence suite cannot be mistaken for proof that the
    three implementations are interchangeable in general. They are not:
    each difference below is demonstrated with a real call, not asserted
    from reading the source alone.
    """

    def test_1d_input_src_explicit_valueerror_oldmate1_numpy_valueerror(self):
        vector = np.array([1.0, 2.0, 3.0])

        with self.assertRaises(ValueError) as src_ctx:
            SRC_ENGINE.compute_manifold_stability(vector)
        self.assertEqual(
            str(src_ctx.exception),
            "psi_barrier must be a matrix.",
        )

        # oldmate1 performs no validation of its own; whatever error
        # numpy.trace itself raises for a 1-D input is what propagates,
        # with a different message than src's.
        with self.assertRaises(ValueError) as oldmate1_ctx:
            OLDMATE1_ENGINE.compute_manifold_stability(vector)
        self.assertEqual(
            str(oldmate1_ctx.exception),
            "diag requires an array of at least two dimensions",
        )

        # abtm_expansion raises its own explicit, differently worded
        # ValueError for the same input.
        with self.assertRaises(ValueError) as expansion_ctx:
            ABTM_Expansion.z6_trace_residue(vector)
        self.assertEqual(
            str(expansion_ctx.exception),
            "psi_barrier must be a two-dimensional matrix.",
        )

    def test_3d_input_src_rejects_oldmate1_silently_returns_array_not_bool(self):
        cube = np.zeros((2, 2, 2))

        with self.assertRaises(ValueError):
            SRC_ENGINE.compute_manifold_stability(cube)

        with self.assertRaises(ValueError):
            ABTM_Expansion.z6_trace_residue(cube)

        # oldmate1 has no ndim check, so numpy.trace on a 3-D array
        # computes a trace over axes (0, 1) and returns an ARRAY (one
        # value per remaining axis), not a scalar. The subsequent
        # `== 0` comparison then produces an array of booleans, not a
        # single bool -- a genuinely different return SHAPE, not just a
        # different value.
        oldmate1_result = OLDMATE1_ENGINE.compute_manifold_stability(cube)
        self.assertIsInstance(oldmate1_result, np.ndarray)
        self.assertEqual(oldmate1_result.shape, (2,))
        self.assertFalse(isinstance(oldmate1_result, np.bool_))

    def test_empty_matrix_expansion_rejects_src_and_oldmate1_accept(self):
        empty_matrix = np.empty((0, 0))

        # src and oldmate1 both silently accept an empty 2-D matrix:
        # np.trace(empty) == 0.0, 0.0 % 6 == 0.0, so both report "stable".
        self.assertTrue(
            bool(SRC_ENGINE.compute_manifold_stability(empty_matrix))
        )
        self.assertTrue(
            bool(OLDMATE1_ENGINE.compute_manifold_stability(empty_matrix))
        )

        # abtm_expansion explicitly rejects empty input instead.
        with self.assertRaises(ValueError) as ctx:
            ABTM_Expansion.z6_trace_residue(empty_matrix)
        self.assertEqual(
            str(ctx.exception),
            "psi_barrier must not be empty.",
        )

    def test_nan_entries_expansion_rejects_src_and_oldmate1_accept(self):
        nan_matrix = np.array([[np.nan, 0.0], [0.0, 1.0]])

        # src and oldmate1 both silently propagate NaN through the
        # arithmetic: NaN % 6 is NaN, and NaN == 0 is False in NumPy, so
        # both report "unstable" without ever raising.
        self.assertFalse(
            bool(SRC_ENGINE.compute_manifold_stability(nan_matrix))
        )
        self.assertFalse(
            bool(OLDMATE1_ENGINE.compute_manifold_stability(nan_matrix))
        )

        # abtm_expansion explicitly rejects non-finite input instead.
        with self.assertRaises(ValueError) as ctx:
            ABTM_Expansion.z6_trace_residue(nan_matrix)
        self.assertEqual(
            str(ctx.exception),
            "psi_barrier must contain only finite numbers.",
        )

    def test_near_zero_residue_expansion_tolerant_src_and_oldmate1_exact(self):
        # trace = 1e-10, which is NOT exactly zero, so src's and
        # oldmate1's exact `sigma == 0` comparison both report
        # "unstable". abtm_expansion's z6_stable() instead compares with
        # np.isclose(residue, 0.0) (default rtol=1e-05, atol=1e-08), and
        # 1e-10 IS within that tolerance of zero, so it reports "stable".
        #
        # This input is accepted without error by all three
        # implementations -- it is squarely in their SHARED valid
        # domain -- and they still disagree on the boolean result. This
        # is a genuine behavioral divergence, not a validation-boundary
        # difference, and is the reason full equivalence between
        # abtm_expansion.z6_stable and the other two is NOT proven by
        # this test suite.
        near_zero_matrix = np.array([[1e-10, 0.0], [0.0, 0.0]])

        src_result = bool(
            SRC_ENGINE.compute_manifold_stability(near_zero_matrix)
        )
        oldmate1_result = bool(
            OLDMATE1_ENGINE.compute_manifold_stability(near_zero_matrix)
        )
        expansion_result = ABTM_Expansion.z6_stable(near_zero_matrix)

        self.assertFalse(src_result)
        self.assertFalse(oldmate1_result)
        self.assertTrue(expansion_result)
        self.assertNotEqual(
            src_result,
            expansion_result,
            "Expected src and abtm_expansion.z6_stable to disagree here "
            "(exact equality vs np.isclose tolerance); if this now "
            "passes as equal, the tolerance behavior has changed.",
        )

    def test_plain_python_list_src_rejects_others_accept(self):
        nested_list = [[1, 2], [3, 4]]

        # src requires something exposing a `.ndim` attribute (a NumPy
        # array or array-like object). A plain Python list has no such
        # attribute, so src fails with an AttributeError -- not even the
        # ValueError src itself documents for bad shapes, an entirely
        # different, uncontrolled exception type.
        with self.assertRaises(AttributeError) as ctx:
            SRC_ENGINE.compute_manifold_stability(nested_list)
        self.assertEqual(
            str(ctx.exception),
            "'list' object has no attribute 'ndim'",
        )

        # oldmate1 accepts it directly: numpy.trace() converts the list
        # internally.
        oldmate1_result = OLDMATE1_ENGINE.compute_manifold_stability(
            nested_list
        )
        self.assertFalse(bool(oldmate1_result))

        # abtm_expansion also accepts it directly, via its own explicit
        # np.asarray() conversion in as_array().
        expansion_residue = ABTM_Expansion.z6_trace_residue(nested_list)
        self.assertEqual(expansion_residue, 5.0)

    def test_return_types_differ_on_a_shared_valid_input(self):
        matrix = np.array([[1, 2], [3, 4]])

        src_result = SRC_ENGINE.compute_manifold_stability(matrix)
        oldmate1_result = OLDMATE1_ENGINE.compute_manifold_stability(matrix)
        expansion_stable = ABTM_Expansion.z6_stable(matrix)
        expansion_residue = ABTM_Expansion.z6_trace_residue(matrix)

        # src and oldmate1 both return numpy.bool_ (NumPy's boolean
        # scalar), not Python's built-in bool.
        self.assertIsInstance(src_result, np.bool_)
        self.assertIsInstance(oldmate1_result, np.bool_)
        self.assertNotIsInstance(src_result, bool)
        self.assertNotIsInstance(oldmate1_result, bool)

        # abtm_expansion.z6_stable explicitly casts to a native Python
        # bool via bool(...).
        self.assertIsInstance(expansion_stable, bool)

        # Only abtm_expansion exposes the intermediate residue at all,
        # and it does so as a native Python float.
        self.assertIsInstance(expansion_residue, float)


if __name__ == "__main__":
    unittest.main()
