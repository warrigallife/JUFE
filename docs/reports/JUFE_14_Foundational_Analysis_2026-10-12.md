# Source 14 — Foundational Analysis (Code-Provenance Kernel/ABTM-Engine Fragment)

**Date**: 2026-10-12 (UTC 10:41:39 / AEST 20:41:39, confirmed via
`date -u` and `TZ="Australia/Brisbane" date`)
**Author**: Clio (mathematical interpreter persona)
**Scope**: Give source 14 the dedicated analysis it has never
received. Source 14 was treated only as comparison context in the
now-closed source-13 cycle (handover §52, citing
`JUFE_13_Foundational_Analysis_2026-10-12.md` and its accepted
independent review) — this report is the dedicated cycle that §52
explicitly left for later. Source 13 is treated here only as
comparison context, the reverse of the prior cycle. Source 35 and the
combined manuscript are **not** opened or analysed in this pass. Code
is inspected as text throughout; nothing in this report was executed.

## 0. Provenance

| Field | Value |
|---|---|
| Path | `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/ORIGINAL_FRAGMENTS/14-kernel-abtm-fragment.md` |
| Provenance row | `PROVENANCE_MAP.md` row 6 (`14.md` → this path, "KEEP REPRESENTATIVE (non-manuscript/code)") |
| SHA-256 | `fb84ae2f885ad4d38037233431aa9ac3c3dd2f3cde9df78d6a84777e63718372` (recomputed directly for this report, exact match against the provenance map) |
| Lines | 47 (confirmed by `wc -l`) |
| Repository state | `git rev-parse HEAD` = `23269415603c90593d948f76b0f9ea8c912b4193`, matching the HEAD recorded at handover §52 — no new commits since. `git status --short` shows this fragment is not listed as modified or untracked (only `JUFE_COLLABORATOR_HANDOVER.md` and two specification files are `M`, pre-existing and unrelated). This report itself will be untracked (`??`) once saved. |

**Existing-equivalent-work check, performed before writing**: no file
matching `JUFE_14_Foundational_Analysis*` exists in `docs/reports/`.
Four existing items already read or cite parts of source 14's
surrounding context, for different purposes, and are cited (not
reproduced) throughout this report:

- `JUFE_13_Foundational_Analysis_2026-10-12.md` (now closed, handover
  §52) and its accepted independent review — source 14 appears there
  only as comparison context for source 13's own fields, the
  `oldmate1(5).py`/`oldmate2(4).py` pairing, and the launcher
  work-around; this report does not repeat those findings, only cites
  them where source 14 is itself the subject.
- `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/README.md` — the
  project's own catalogue entry tracing source 14's named concepts to
  `src/kernel.py`, `src/engines/abtm.py`, and `abtm_expansion.py`.
- `JUFE_Repository_Assessment_2026-10-04.md` — identifies
  `oldmate1(5).py` as a "legacy baseline implementation kept for
  parity testing" and reports `tests/test_z6_equivalence.py`'s
  three-way comparison as "confirmed passing" — this report's own,
  more granular reading of that same test file (§5 below) refines
  what "passing" actually covers.
- `JUFE_37_Mathematical_Analysis.md` §8 Q8/Q9 — already catalogues
  source 14's (and source 13's) state-vector tuple and the
  `arithmetic_geometry.tex`/"Z6"-vocabulary connections as part of a
  wider, four-way `\Psi`-definition comparison across the retained
  collection; not repeated here.

No report performs a dedicated, full-text reading of source 14 in its
own right, and none has previously read `abtm_expansion.py`'s
`ABTM_Expansion` class methods or `tests/test_z6_equivalence.py`'s
actual test bodies (as opposed to its docstring) in the detail this
report does (§4–§5 below). This is therefore the first dedicated
reading.

## 1. Full-text catalogue — the complete 47-line fragment

Read in full via the Read tool, as text (not executed):

| Lines | Content |
|---|---|
| 1–6 | Identifier line (`14`); blank line; four imports — `numpy as np`, `zlib`, `base64`, `json`. (Source 13 imports the same three stdlib modules but **not** `numpy`.) |
| 8–11 | `class JUFE_Kernel:` with a docstring: "POST-BINARY KERNEL: Absolute physical-logic foundation. Integrates Chiral Toroidal Tensegrity Manifold (CTTM) constraints." (Different second sentence from source 13's docstring, which instead reads "Enforces the Z6 residue class and the 3pi core twist as immutable laws.") |
| 13–22 | `__init__(self, treatise_latex, abtm_engine)`: builds `self.kernel_state`, a plain dict with **seven** keys — `version` ("1.0.0-PROD"), `integrity_hash` ("J-6-UNIFIED-FIELD"), `lattice_basis` ("Z6-CLOSED-RING"), `core_twist` ("3PI_NON_ORIENTABLE" — **absent from source 13**), `spec` (the supplied `treatise_latex`, unmodified), `logic` (**`abtm_engine.__class__.__name__`** — a string, computed from the supplied engine, unlike source 13's raw pass-through), `gate_state` ("ACTIVE-PARITY-LOCK"). |
| 24–27 | `execute_boot(self)`: docstring "Initializes the lattice as a zero-sum, non-singular manifold." (identical wording to source 13's); one code comment, "Validate against orthogonality constraint: M_k * A_k^T = 0" (**different claim from source 13's** "The engine self-validates against the LaTeX spec at boot."); body is a single `return self._seal_kernel()` call. |
| 29–31 | `_seal_kernel(self)`: **no docstring** (source 13's equivalent method has one, "Finalizes binary state: Non-Truncating, Self-Regulating."); serializes `self.kernel_state` via `json.dumps(...).encode('utf-8')`, compresses with `zlib.compress`, encodes with `base64.b85encode` — byte-for-byte the same three-step pipeline as source 13. |
| 33–37 | `class ABTM_Engine(ABTM_Expansion):` — **not present in source 13 at all**. Docstring: "Enforces the Hydraulic Escapement Sequence and Scale-Transfer Projection Operators." `ABTM_Expansion` is referenced as a base class but never imported or defined anywhere in this fragment. |
| 38–39 | `__init__(self): super().__init__()` — a no-argument constructor that only calls the (unsupplied) base class's own `__init__`. |
| 41–44 | `compute_manifold_stability(self, psi_barrier)`: comment "Trace parity check: sigma = Trace(Psi) mod 6"; body `sigma = np.trace(psi_barrier) % 6; return sigma == 0`; trailing inline comment "Returns True if Core Degeneracy Void is active." |
| 46–47 | Two trailing comments: "Execution Lock:" and "The logic is now non-truncating and bounded by the Z6 residue class." |

No line falls outside this accounting — the full 47-line file is
accounted for, including both trailing comment lines (46 and 47),
checked individually per the completeness note already applied to
the sibling source-13 report (handover §52).

## 2. Stated scope, state fields, and inputs — as literally written

**Stated scope** (docstring, lines 10–11, a **source assertion**, not
independently assessed): "POST-BINARY KERNEL: Absolute physical-logic
foundation. Integrates Chiral Toroidal Tensegrity Manifold (CTTM)
constraints." No code in this fragment references CTTM again outside
this one docstring line, and no "constraint" of any kind is checked
anywhere in `JUFE_Kernel`'s own methods. `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/CTTM_ACCORD.md`
already exists as the collection's own CTTM-named governance text; the
source-37 report already established (cited, not re-verified here)
that the CTTM Accord contains no mathematical content. This fragment's
CTTM reference is therefore a named link to a document already known
to be governance prose, not a mathematical dependency.

**State fields** — `kernel_state`, seven keys (one more than source
13's six): `version`, `integrity_hash`, `lattice_basis`, `core_twist`,
`spec`, `logic`, `gate_state`. Five of the seven are hardcoded literal
strings; `spec` and `logic` are derived from the two constructor
arguments — but, unlike source 13, `logic` is **not** stored raw: it
is explicitly converted via `abtm_engine.__class__.__name__` inside
`__init__` itself (line 20), before anything is stored.

**No definitions are supplied for**: what the "Hydraulic Escapement
Sequence" or "Scale-Transfer Projection Operators" (the `ABTM_Engine`
docstring) actually are, in any formula or algorithm — `ABTM_Engine`
defines exactly one method (`compute_manifold_stability`), which
implements neither of those two named concepts; what "Core Degeneracy
Void" (the trailing inline comment on `compute_manifold_stability`'s
`return` line) means beyond being "active" when `sigma == 0`; or what
`M_k` and `A_k` (the `execute_boot` comment's orthogonality constraint,
`M_k * A_k^T = 0`) are, dimensionally or otherwise — no code in this
fragment defines, constructs, or references `M_k`/`A_k` anywhere, and
`execute_boot`'s body does not check this or any other constraint; it
only calls `_seal_kernel()`. These are recorded as missing
definitions, not supplied by inference.

## 3. What source 14 adds beyond source 13 — differences, not only additions

Compared directly against source 13's 34-line text (already
catalogued in `JUFE_13_Foundational_Analysis_2026-10-12.md` §1,
accepted per handover §52):

- **`core_twist`** is a wholly new field, absent from source 13's
  `kernel_state` dict entirely.
- **`logic`'s value is computed, not passed through raw** — the one
  place source 14's own code is already more defensive than source
  13's (source 13's equivalent field stores the raw `abtm_engine`
  object unmodified, which the now-closed source-13 report found
  would make `_seal_kernel`'s `json.dumps` call fail on a
  non-serialisable object; source 14 does not have this specific
  failure mode, because it converts to a string first).
- **A second class, `ABTM_Engine(ABTM_Expansion)`, with one method**
  (`compute_manifold_stability`) — source 13 defines no second class
  and no stability-check method at all.
- **A different `execute_boot` comment** — an orthogonality-constraint
  claim (`M_k * A_k^T = 0`) rather than source 13's self-validation
  claim — and, as with source 13's comment, this one is also not
  matched by any check in the fragment's own code (§2 above).
- **`_seal_kernel` lacks a docstring** that source 13's equivalent
  method has; this is the one place source 14 supplies *less* text
  than source 13, not more.
- **An additional import** (`numpy`), required only by the new
  `ABTM_Engine.compute_manifold_stability` method — `JUFE_Kernel`
  itself uses no NumPy functionality in either fragment.

## 4. Comparison against the current runtime

### 4.1 `oldmate1(5).py` — a byte-identical, actively-loaded root-level counterpart

A root-level file, `oldmate1(5).py`, is byte-for-byte identical to
source 14's text (a whitespace-normalized `diff`, run independently
for this report, shows no difference at all beyond the trailing
newline and the supplied leading identifier/blank lines that are
artefacts of the `.md` wrapping, not code). This is a tighter
correspondence than source 13 has with its own counterpart,
`oldmate2(4).py` (which the now-closed source-13 report found differs
by two extra, dead lines). `oldmate1(5).py` is loaded by name (as
`"oldmate1"`) and its `ABTM_Engine`/`JUFE_Kernel` classes are directly
used — confirmed in `jufe_original_launcher.py`'s
`run_original_system()` function (already read in full for the
source-13 cycle, re-confirmed here): `engine = oldmate1.ABTM_Engine()`,
then `bool(engine.compute_manifold_stability(matrix))` is "the
stability decision" the launcher reports, and `kernel_1 =
oldmate1.JUFE_Kernel(treatise_text, engine)` is booted alongside
source 13's `oldmate2`-equivalent kernel.

**The unresolved `ABTM_Expansion` base class is supplied externally,
not defined anywhere in source 14 or `oldmate1(5).py`**: both declare
`class ABTM_Engine(ABTM_Expansion):` without importing or defining
`ABTM_Expansion`. `jufe_original_launcher.py`'s `load_oldmate1()`
helper (already read in full for the source-13 cycle) resolves this by
injecting the name into the freshly-created module's namespace
(`module.ABTM_Expansion = ABTM_Expansion`, imported at the top of the
launcher from `abtm_expansion.py`) **before** executing the module —
i.e., the fragment's own code is never edited to add the missing
import; the loader supplies the name externally instead. Six
root-level scripts use this identical loading pattern, confirmed by
name and by `tests/test_z6_equivalence.py`'s own docstring (§5 below),
which explicitly states it "reuses that exact approach... rather than
inventing a new one."

### 4.2 `src/kernel.py` and `src/engines/abtm.py` — which parts of the runtime trace to source 14 specifically

The now-closed source-13 report already gives the full field-by-field
`kernel_state`/`KernelState` comparison table. Revisited here with
source 14 as the subject: `core_twist` and the `logic`→`engine_name`
class-name-serialization choice are the two elements of
`src/kernel.py`'s `KernelState`/`JUFEKernel.__init__` that trace to
source 14 specifically, not to source 13 — source 13 has neither.
`src/kernel.py`'s `engine_name=engine.__class__.__name__` (confirmed at
line 72 in the now-closed source-13 report's own reading) is the
**same conversion source 14 already performs internally**; the
runtime did not need to add this defensiveness for source 14's
pattern, only for source 13's.

`src/engines/abtm.py`'s `ABTMEngine` class (read in full for this
report, 407 lines) is the runtime's own reimplementation of the
stability check. Its `compute_manifold_stability` (lines 56–70):

```python
def compute_manifold_stability(
    self,
    psi_barrier: np.ndarray,
) -> bool:
    if psi_barrier.ndim != 2:
        raise ValueError("psi_barrier must be a matrix.")
    sigma = np.trace(psi_barrier) % 6
    return sigma == 0
```

— the arithmetic core (`np.trace(psi_barrier) % 6`, `== 0`) is
identical to source 14's `ABTM_Engine.compute_manifold_stability`,
confirmed by direct, line-level comparison. The runtime version adds
exactly one check absent from source 14: `psi_barrier.ndim != 2`
raises `ValueError("psi_barrier must be a matrix.")`. It does **not**
inherit from anything resembling `ABTM_Expansion` — `ABTMEngine` is a
standalone class with no base class at all (`class ABTMEngine:`,
confirmed directly), unlike source 14's `ABTM_Engine(ABTM_Expansion)`.
The runtime class is also renamed (`ABTMEngine`, no underscore) and
constructs nine other component objects in its own `__init__`
(`JUFETransformation`, `JUFEConservation`, `JUFEGlobalConservation`,
`JUFEEquilibrium`, `JUFEFieldGradient`, `JUFEPhaseLock`,
`JUFEToroidalFlux`, `JUFESensitivityMatrix`, `JUFEHarmonicLayer`) that
have no counterpart of any kind in source 14's three-line
`ABTM_Engine.__init__`.

### 4.3 `abtm_expansion.py`'s `ABTM_Expansion` — the supplied base class, read directly (not only its docstring)

Read in full for this report (670 lines; prior citations of this file,
including in the now-closed source-13 cycle, quoted only its module
docstring). The class relevant to source 14's `ABTM_Engine(ABTM_Expansion)`
declaration supplies, among other methods:

- `compose_manifold_state(compressive_field, repulsive_field)` —
  composes a six-component `\Psi` state as `[Mx, My, Mz, Ax, Ay, Az]`
  from two separate three-component vectors, docstringed as "the M^6
  state." This is the closest textual match found anywhere to source
  14's own `execute_boot` comment, "M_k * A_k^T = 0" — both name `M`
  and `A` as paired vector-like quantities — but `ABTM_Expansion`
  supplies no `orthogonal`/orthogonality-check method anywhere
  (confirmed by a direct, repository-wide search for "orthogonal":
  zero matches in `abtm_expansion.py` or anywhere under `src/`). So
  the specific constraint source 14's comment names is not implemented
  by the class that resolves its missing base — the naming
  correspondence (`M`, `A`) is a **structural echo**, not evidence
  that the constraint itself is implemented anywhere.
- `z6_trace_residue(psi_barrier)` (a `classmethod`) — `sigma =
  Trace(Psi) mod 6`, its own docstring stating "This is the same
  numerical rule used by the supplied `ABTM_Engine`." Its own input
  validation (`as_array`) rejects empty arrays and non-finite entries
  — checks source 14's `ABTM_Engine.compute_manifold_stability` does
  not perform at all.
- `z6_stable(psi_barrier)` (a `classmethod`) — returns
  `bool(np.isclose(z6_trace_residue(psi_barrier), 0.0))`, an
  **approximate**, tolerance-based comparison (NumPy defaults
  `rtol=1e-05`, `atol=1e-08`), in contrast to source 14's own
  `sigma == 0`, an **exact** comparison. This difference is not
  academic — §5 below shows it is an actual, test-demonstrated
  behavioural divergence for specific inputs, not merely a
  stylistic one.

### 4.4 Serialisation pipeline — unchanged core, no added validation

`src/kernel.py`'s `_seal_kernel`/`execute_boot` (already read in full
for the source-13 cycle) adds a `_validate_state()` truthiness check
and computes `integrity_hash` via SHA-256 rather than hardcoding it —
both already catalogued there as applying equally to whichever of
source 13/14's fields survive into `KernelState`. Nothing in that
validation checks `core_twist`'s value, the Z6 residue class, or any
other claim specific to source 14 beyond non-emptiness; this is
unchanged from the now-closed report's finding and is not re-derived
here.

## 5. `tests/test_z6_equivalence.py` — read in full, not only its docstring

This is the one test file in the repository that exercises code
descended from source 14 (`ABTM_Engine`/`compute_manifold_stability`).
Read in full for this report (589+ lines). It compares three
implementations — `src/engines/abtm.py`'s `ABTMEngine`,
`oldmate1(5).py`'s `ABTM_Engine` (loaded via the injection pattern
described in §4.1), and `abtm_expansion.py`'s `ABTM_Expansion` — and
states its own purpose directly in its module docstring, quoted
verbatim: **"Everything in this file is characterization only: it
records what each implementation currently does. No claim is made
that any one of the three behaviors is more 'correct' than another,
except where the task explicitly asks for an equivalence verdict,
which is reported in the class docstrings below strictly on the basis
of what the tests actually demonstrate."** This is the test suite's
own, explicit disclaimer against
treating it as validation of the underlying manifold theory — directly
relevant to this task's instruction not to assume parity tests
validate the theory, and stated by the test file's own author, not
inferred by this report.

**Where the three implementations are demonstrated to agree**
(`FixedCaseEquivalenceTests`, `GeneratedMatrixEquivalenceTests`): six
named fixed matrices and sixty deterministically-generated integer
matrices (sizes 2×2, 3×3, 4×4, seeded, confirmed in the test's own
`setUpClass`) are each run through all three implementations. Every
case is explicitly restricted, by the test class's own docstring, to
"plain finite integer-valued 2-D matrices, which is the input shape
all three implementations accept without raising and without any
tolerance ambiguity." Agreement is demonstrated **only** within this
restricted domain.

**Where the three implementations are demonstrated to disagree**
(`DomainAndTypeDifferenceTests`, whose own class docstring states this
is "kept completely separate from the equivalence tests above so that
a passing equivalence suite cannot be mistaken for proof that the
three implementations are interchangeable in general"):

- A 1-D input: `ABTMEngine` raises `ValueError("psi_barrier must be a
  matrix.")`; `oldmate1`'s `ABTM_Engine` raises NumPy's own
  `ValueError("diag requires an array of at least two dimensions")`
  (a different message, since it performs no validation of its own);
  `ABTM_Expansion.z6_trace_residue` raises its own, third differently-
  worded `ValueError`.
- A 3-D input: `ABTMEngine` and `ABTM_Expansion` both raise
  `ValueError`; `oldmate1`'s version has no dimensionality check at
  all, so `np.trace` on a 3-D array returns an **array** of booleans,
  not a scalar `bool` — a different return *shape*, not just a
  different value, confirmed directly in the test's own assertions
  (`isinstance(oldmate1_result, np.ndarray)`, `shape == (2,)`).
- An empty `(0, 0)` matrix: `ABTMEngine` and `oldmate1` both silently
  report "stable" (`np.trace` of an empty array is `0.0`); `ABTM_Expansion`
  explicitly raises `ValueError("psi_barrier must not be empty.")`.
- A matrix containing `NaN`: `ABTMEngine` and `oldmate1` both silently
  report "unstable" (`NaN == 0` is `False` in NumPy, no exception);
  `ABTM_Expansion` explicitly raises `ValueError("psi_barrier must
  contain only finite numbers.")`.
- **A near-zero-but-nonzero trace** (`[[1e-10, 0.0], [0.0, 0.0]]`):
  `ABTMEngine` and `oldmate1` both report "unstable" (exact `== 0`
  fails); `ABTM_Expansion.z6_stable` reports "stable" (`np.isclose`
  tolerance). The test's own comment states this explicitly: **"This
  input is accepted without error by all three implementations — it
  is squarely in their SHARED valid domain — and they still disagree
  on the boolean result. This is a genuine behavioral divergence...
  and is the reason full equivalence between `abtm_expansion.z6_stable`
  and the other two is NOT proven by this test suite."** The test
  asserts this disagreement directly (`assertNotEqual(src_result,
  expansion_result, ...)`), i.e. the test is *designed* to demonstrate
  the divergence, not to hide it.
- A plain Python nested list: `ABTMEngine` raises `AttributeError`
  (not even the `ValueError` it documents for bad shapes, since a list
  has no `.ndim` attribute); `oldmate1` and `ABTM_Expansion` both
  accept it (via internal NumPy conversion).

**Recorded test evidence, not re-run for this report**: an existing,
dated test-run log, `docs/reports/TEST_EVIDENCE_2026-10-05T011500Z/stderr.txt`
(5 October 2026, predating this report), records all 215 tests across
the full suite — including every `test_z6_equivalence.py` test named
above, by its exact test-ID string — as `ok`, ending `Ran 215 tests in
0.046s` / `OK`. This report cites that existing, already-saved log as
evidence that the disagreement test itself passed (i.e., the
documented divergence was reproduced, not merely asserted in
isolation) — it does **not** re-run the suite; nothing was executed
for this report.

**What this test suite does and does not establish**: it demonstrates
that, for integer-valued inputs within a shared accepted domain, all
three implementations currently compute the same `trace mod 6`
parity-stability result, and it demonstrates specific, real points of
divergence outside that domain. It does **not** demonstrate, and its
own docstring explicitly disclaims, that any of the three
implementations correctly captures whatever physical or mathematical
claim "stability" is meant to represent in the manifold theory — no
test in this file compares any result against a value derived from
the manuscript sources, only against the other two implementations or
against a "canonical" formula independently re-derived from `src`'s
own text (`_canonical_residue`, used as the fixture-correctness check,
not as an external, theory-derived reference).

## 6. Specification layer — checked, no dedicated governance found

A repository-wide search of `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/`,
`JUFE_ABTM_SPEC_LAYER/`, `JUFE_ABTM_PROJECT_FOUNDATION/`, and
`Specifications/` for "orthogonality constraint," "M_k," "core_twist,"
and "3PI_NON_ORIENTABLE" returns zero matches anywhere. No dedicated
specification formalizes the `M_k * A_k^T = 0` orthogonality claim
named in source 14's `execute_boot` comment, or the `core_twist`
field's "3PI_NON_ORIENTABLE" label. This extends the same negative
finding already recorded for source 13 against
`JUFE_REPOSITORY_SPECIFICATION`'s Chapter 4 (handover §52) to this
wider set of specification trees and to source 14's own, additional
claims.

## 7. Unresolved mathematical justification — preserved, not adjudicated

- **The orthogonality constraint, `M_k * A_k^T = 0`**: named once, in
  a comment, with no implementation anywhere found (fragment, runtime,
  or specification trees). `abtm_expansion.py`'s `compose_manifold_state`
  supplies `M`/`A` as named vector components of a composed `\Psi`,
  which is the closest structural echo found, but no code computes
  `M_k * A_k^T` or checks it against zero. Whether this constraint is
  meant to be implemented elsewhere, is aspirational, or has been
  superseded is not stated by any source read for this report.
- **"Hydraulic Escapement Sequence" and "Scale-Transfer Projection
  Operators"** (the `ABTM_Engine` docstring): named, not defined or
  implemented anywhere in this fragment or in `abtm_expansion.py`'s
  `ABTM_Expansion` (checked directly: neither phrase occurs in that
  file). Not resolved by this report.
- **Whether `np.isclose`'s tolerance (`abtm_expansion.py`) or exact
  equality (source 14, `oldmate1(5).py`, `src/engines/abtm.py`) is the
  mathematically intended comparison** for `\sigma = 0` is not stated
  by any source read for this report — both exist in the current
  codebase, disagree on at least one concrete input (§5), and no file
  states which is authoritative.
- **Whether the `core_twist`/`"3PI_NON_ORIENTABLE"` label is meant to
  be checked computationally at all**, beyond being a stored string,
  is not stated anywhere; no code in source 14, `oldmate1(5).py`, or
  `src/kernel.py` computes or verifies a "3π" quantity.

## 8. Coverage, dependencies, and limitations

**Full-text coverage**: source 14's complete 47 lines were read for
this report (not sampled) — the first dedicated reading on record,
closing the gap the now-closed source-13 cycle explicitly left open.

**Files read in full or by targeted, text-only inspection for this
report**: source 14 (47 lines); `oldmate1(5).py` (diffed against
source 14); `src/engines/abtm.py` (407 lines, in full, for this
report — previously only its class/method signatures had been read in
the source-13 cycle); `abtm_expansion.py` (670 lines, in full, for
this report — previously only its module docstring had been read);
`tests/test_z6_equivalence.py` (read in full for this report,
589+ lines — previously only its docstring had been read);
`docs/reports/TEST_EVIDENCE_2026-10-05T011500Z/stderr.txt` (existing,
dated log, read for its recorded pass/fail status only, not
re-generated); `CODE_PROVENANCE/README.md`, the relevant
`PROVENANCE_MAP.md` row, and the specification-tree directories
searched in §6. None of these files was executed, imported, or run as
a script for this report — all reading was done as text via the
Read/Grep tools; the one test-run log cited was already on disk before
this report began.

**Dependencies**: §4.1's claim about `oldmate1(5).py`'s loading
pattern rests on the already-verified `jufe_original_launcher.py`
reading from the source-13 cycle, re-confirmed here by name/text
search across the five other scripts that use the identical pattern
(not re-read line-by-line individually in this pass). §5's "all three
agree within the shared integer domain" and "documented disagreement
outside it" claims rest on direct reading of the test file's own
assertions and the cited, pre-existing test-run log — not on running
anything.

**Limitations**:
- Per the task's explicit scope, source 13 was used only as comparison
  context (its own dedicated findings are cited from the now-closed
  report, not re-derived); source 35 and the combined manuscript were
  not opened in this pass.
- `jufe_original_launcher.py`'s five sibling scripts that use the same
  `oldmate1`-loading pattern were confirmed by name/text search only
  (consistent with the now-closed source-13 cycle's own treatment of
  the parallel `oldmate2` case), not individually re-read in full for
  this report.
- `abtm_expansion.py` was read in full for the methods and classes
  relevant to `ABTM_Engine`'s resolution and the Z6/manifold-state
  vocabulary (§4.3); its remaining methods (phase-lock, bifurcation,
  global-balance, and other dataclasses named at the top of the file)
  were not individually analysed, as they fall outside source 14's
  own content.
- This report does not assess whether `src/engines/abtm.py`,
  `abtm_expansion.py`, `oldmate1(5).py`, or any other file's code is
  correct, secure, or fit for any purpose — only what each states and
  does, as text.
- No independent review, correction, or handover/continuity update was
  performed in this pass, consistent with the task's scope.

## 9. Summary for the record

- **Exact path saved**: `~/Desktop/JUFE/docs/reports/JUFE_14_Foundational_Analysis_2026-10-12.md` (this file).
- **Source 14 is**: a 47-line Python fragment, closely related to
  source 13 (same `JUFE_Kernel` class pattern, same serialisation
  pipeline) but adding a `core_twist` field, a safer `logic`
  serialisation (class-name string, not a raw object), and a second
  class, `ABTM_Engine(ABTM_Expansion)`, with one method,
  `compute_manifold_stability`, implementing `sigma = np.trace(psi_barrier)
  % 6; return sigma == 0`. Its `execute_boot` comment names an
  orthogonality constraint (`M_k * A_k^T = 0`) that, like source 13's
  "self-validates" claim, is not matched by any check in the
  fragment's own code.
- **`ABTM_Expansion` is supplied externally, not defined in this
  fragment**: resolved at load time by six root-level launcher
  scripts' shared `module.ABTM_Expansion = ABTM_Expansion` injection
  pattern, pointing at `abtm_expansion.py`'s own, independently
  numerical reimplementation — read in full for this report, not only
  by docstring, revealing that its `z6_stable` uses a tolerance
  comparison (`np.isclose`) where source 14 and the runtime both use
  exact equality.
- **Test evidence, read in full, is explicitly characterization-only**:
  `tests/test_z6_equivalence.py`'s own docstring disclaims any
  correctness verdict; it demonstrates agreement across all three
  implementations strictly within a shared integer-input domain, and
  demonstrates — by design, with a dedicated, passing-per-existing-
  evidence test — a genuine, non-hypothetical disagreement for a
  near-zero float trace. **Parity within the tested domain is not
  evidence that any implementation validates the manifold theory
  itself** — no test compares a result against anything derived from
  the manuscript sources, only against the other implementations or a
  same-codebase "canonical" reformulation.
- **No dedicated specification governs source 14's distinctive claims**
  (the orthogonality constraint, `core_twist`'s label, "Hydraulic
  Escapement Sequence," "Scale-Transfer Projection Operators") —
  confirmed by a repository-wide search of the specification trees
  (§6), extending the equivalent, already-established finding for
  source 13 to this wider search and to source 14's own additional
  claims.
- **Coverage status**: source 14 now has a first full-text reading and
  a detailed runtime/test comparison. Per the full-collection audit's
  own criterion, this does not by itself constitute an accepted
  independent-review cycle, so source 14 should not yet be treated as
  meeting that criterion until reviewed.
- **Remaining limitations**: as stated in §8.

## 10. Correction trail — 12 October 2026, 21:03 AEST (2026-10-12T11:03:43Z)

An independent review
(`docs/reports/JUFE_14_Foundational_Analysis_Independent_Review_2026-10-12.md`,
agent Nora) found provenance, full-file coverage (including the
trailing-comment handling), the kernel additions, the engine-name
serialization claim, the `oldmate1(5).py` byte-identity finding, the
launcher injection pattern and "six scripts" claim (independently
re-verified at the code level), the exact-vs-tolerance distinction,
the integer-domain agreement and near-zero disagreement, the
historical test-evidence attribution, and the specification-layer
search all accurate on independent, direct re-verification. **Two
numeric/counting corrections and two low-severity quotation-precision
notes were required**, confined to §4.2 and §5.

**Independently re-verified before correcting**:
1. Re-counted `src/engines/abtm.py`'s `ABTMEngine.__init__` directly
   (lines 25–53): nine objects are constructed
   (`self.transformation`, `self.conservation`,
   `self.global_conservation`, `self.equilibrium`, `self.gradient`,
   `self.phase_lock`, `self.toroidal_flux`, `self.sensitivity`,
   `self.harmonics`), matching the nine class names already listed in
   §4.2's own parenthetical — the original "eight" undercounted the
   very list it quoted.
2. Re-counted `tests/test_z6_equivalence.py`'s `FIXED_CASES` dict
   directly (lines 273–310): exactly six keys (`identity_2x2`,
   `zero_2x2`, `identity_6x6`, `diag_111_3x3`,
   `negative_wraparound_2x2`, `non_square_2x3`) — the original "seven"
   overcounted by one. The separately stated "sixty
   deterministically-generated" figure was independently reconfirmed
   correct and untouched.
3. Re-read the module docstring's full sentence directly: it continues
   past "...more 'correct' than another" with "except where the task
   explicitly asks for an equivalence verdict, which is reported in
   the class docstrings below strictly on the basis of what the tests
   actually demonstrate" — the original quotation stopped short of
   this exception clause, reading more absolute than the source text.
4. Re-read the near-zero-trace test's comment directly (line 537 area):
   it spells "behavioral," not "behavioural" — the original quotation
   used the latter spelling inside what was presented as a verbatim
   quote.

**Corrections applied**:
- §4.2: "eight other component objects" corrected to "nine other
  component objects" — the parenthetical list of nine names is
  unchanged, since it was already correct.
- §5: "seven named fixed matrices" corrected to "six named fixed
  matrices."
- §5: the "characterization only" quotation is extended to include
  the previously-omitted exception clause in full, so the quotation
  now matches the source sentence exactly rather than stopping before
  its own stated exception.
- §5: the near-zero-trace test quotation's "behavioural" is corrected
  to "behavioral," matching the source code comment's own spelling.
  (This report's own prose elsewhere, e.g. §4.3's "behavioural
  divergence," is not inside quotation marks and is left in this
  report's own house spelling, unaffected by this correction.)

**Preserved, not changed**: §0–§3, §4.1, §4.3 (other than the one
quotation-adjacent sentence noted above), §4.4, §6–§9 are unchanged —
the review found them accurate, including the "six scripts" launcher
claim (independently re-verified by the review at the code level, not
only by name-match, and confirmed to hold exactly for source 14,
unlike the parallel source-13 finding) and the historical
test-evidence attribution. The substantive findings are otherwise
unchanged: the exact-vs-tolerance distinction, the integer-domain
agreement, the near-zero disagreement, and the specification-layer
search all stand as originally written.

This report stops here for Nora 2's recheck.
