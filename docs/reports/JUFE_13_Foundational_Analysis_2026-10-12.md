# Source 13 — Foundational Analysis (Code-Provenance Kernel Fragment)

**Date**: 2026-10-12 (UTC 10:08:38 / AEST 20:08:38, confirmed via
`date -u` and `TZ="Australia/Brisbane" date`)
**Author**: Clio (mathematical interpreter persona)
**Scope**: Give source 13 the dedicated analysis it has never received —
it is one of the full-collection coverage audit's six "None" rows
(handover §48/§50: "13, 14, 35, 36, 5, the combined manuscript").
Source 14 is treated **only as comparison context**, per the task's
explicit instruction — its own dedicated analysis is not performed or
completed here. Code is inspected as text throughout; nothing in this
report was executed.

## 0. Provenance

| Field | Value |
|---|---|
| Path | `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/ORIGINAL_FRAGMENTS/13-kernel-fragment.md` |
| Provenance row | `PROVENANCE_MAP.md` row 5 (`13.md` → this path, "KEEP REPRESENTATIVE (non-manuscript/code)") |
| SHA-256 | `7e22d82eca25071e9659ca8c7695f135a15bca5132d1f3289589f7428153a67b` (recomputed directly for this report, exact match against the provenance map) |
| Lines | 34 (confirmed by `wc -l`) |
| External hash attribution | `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/README.md` attributes this hash "per `SOURCE_MANIFEST.json`." No file by that name exists inside this repository (confirmed by search); `JUFE_Repository_Assessment_2026-10-04.md` (line 561) locates the real `SOURCE_MANIFEST.json` at an **external** archive path, `~/Desktop/INFORMATION_ARCHIVE/COLLECTIONS/JUFE/Tom_Jennings_Source_Collection/SOURCE_MANIFEST.json`, outside this repository. This report independently recomputed the hash directly from the retained file (above) rather than relying on that external, inaccessible-from-here attribution. |
| Repository state | `git rev-parse HEAD` = `23269415603c90593d948f76b0f9ea8c912b4193`, matching the HEAD recorded at handover §50 — no new commits since. `git status --short` shows this fragment is not listed as modified or untracked (only `JUFE_COLLABORATOR_HANDOVER.md` and two specification files are `M`, pre-existing and unrelated). This report itself will be untracked (`??`) once saved. |

**Existing-equivalent-work check, performed before writing**: no file
matching `JUFE_13_Foundational_Analysis*` exists in `docs/reports/`.
Three existing reports already read and cite parts of source 13's
surrounding context, for different purposes, and are cited (not
reproduced) throughout this report:

- `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/README.md` — the
  project's own catalogue entry for fragments 13 and 14, tracing named
  concepts to `src/kernel.py`, `src/engines/abtm.py`, and
  `abtm_expansion.py`.
- `JUFE_Repository_Assessment_2026-10-04.md` §1–§2 — a broader
  repository survey that independently identifies `oldmate1(5).py`/
  `oldmate2(4).py` as "legacy baseline implementations kept for parity
  testing," and traces the "Z6 trace-parity mechanic" from `13.md`/
  `14.md` through to `tests/test_z6_equivalence.py`'s confirmed
  three-way parity (that parity check, as detailed in §4 below, covers
  the stability-check logic most closely associated with source 14,
  not source 13's own kernel-state logic).
- `JUFE_8_Foundational_Analysis_2026-10-06.md` §5 (citing `src/kernel.py`
  lines 66–68 and `_validate_state`, lines 119–143) — already
  independently confirms `core_twist`/`lattice_basis` are fixed-string
  dataclass fields with no computational check behind them, and that
  `tests/` contains zero references to `kernel`, `core_twist`, or
  `lattice_basis` by name. This report's own, independent search (§4.4
  below) extends that same "zero matches" finding to the class name
  `JUFEKernel` and the module path `src/kernel.py` itself, across the
  whole `tests/` directory, not only those two field names.

No report performs a dedicated, full-text reading of source 13 in its
own right, and none has previously read `oldmate2(4).py`,
`jufe_original_launcher.py`'s `run_original_system()` function, or
`src/runtime.py`'s construction of `JUFEKernel` in the detail this
report does (§4 below). This is therefore the first dedicated reading.

## 1. Full-text catalogue — the complete 34-line fragment

Read in full via the Read tool, as text (not executed). The fragment
is plain Python source with a leading identifier line (`13`, line 1)
preserved from its supplied form:

| Lines | Content |
|---|---|
| 1–5 | Identifier line (`13`); blank line; three stdlib imports (`zlib`, `base64`, `json`). |
| 7–11 | `class JUFE_Kernel:` with a docstring: "POST-BINARY KERNEL: Absolute physical-logic foundation. Enforces the Z6 residue class and the 3pi core twist as immutable laws." |
| 12–20 | `__init__(self, treatise_latex, abtm_engine)`: builds `self.kernel_state`, a plain dict with six keys — `version` ("1.0.0-PROD"), `integrity_hash` ("J-6-UNIFIED-FIELD"), `lattice_basis` ("Z6-CLOSED-RING"), `spec` (set to the supplied `treatise_latex` argument, unmodified), `logic` (set to the supplied `abtm_engine` argument, unmodified — **not** converted to a string or class name), `gate_state` ("ACTIVE-PARITY-LOCK"). |
| 22–25 | `execute_boot(self)`: docstring "Initializes the lattice as a zero-sum, non-singular manifold."; one code comment, "The engine self-validates against the LaTeX spec at boot."; body is a single `return self._seal_kernel()` call. |
| 27–30 | `_seal_kernel(self)`: docstring "Finalizes binary state: Non-Truncating, Self-Regulating."; serializes `self.kernel_state` via `json.dumps(...).encode('utf-8')`, compresses with `zlib.compress`, and encodes with `base64.b85encode`. |
| 32–34 | Three trailing comments: line 32, "# Execution Logic:" (a section-header comment); line 33, "Kernel initialized with full LaTeX treatise and ABTM logic."; line 34, "Manifold boot is now locked to the integrity_hash: J-6-UNIFIED-FIELD". |

No line falls outside this accounting. The fragment defines **no
other** class, function, or module-level statement; it imports no
third-party package (unlike source 14, which additionally imports
`numpy`).

## 2. Stated scope, definitions, and inputs — as literally written

**Stated scope** (docstring, lines 8–9, a **source assertion**, not
independently assessed): "POST-BINARY KERNEL: Absolute physical-logic
foundation. Enforces the Z6 residue class and the 3pi core twist as
immutable laws." The fragment's own code, however, does **not** itself
enforce or check either the "Z6 residue class" or "the 3pi core twist"
anywhere — `lattice_basis` is a hardcoded label string, not a computed
or checked value, and the fragment never references `core_twist` at
all (that key is introduced only in source 14, not here — see §6). So
the docstring's "enforces... as immutable laws" claim is not matched
by any enforcement code inside this fragment; it is a stated intent,
not a demonstrated mechanism.

**Inputs**: the constructor takes exactly two positional parameters,
`treatise_latex` and `abtm_engine`, with no type annotation, no default
value, and no validation of either (no `isinstance` check, no
emptiness check — contrast with the runtime's `JUFEKernel.__init__`,
§4.2). Both are stored into `kernel_state` exactly as supplied, with no
transformation.

**State fields** (the `kernel_state` dict, six keys): `version`,
`integrity_hash`, `lattice_basis`, `spec`, `logic`, `gate_state` — all
six values are either hardcoded literals (`version`, `integrity_hash`,
`lattice_basis`, `gate_state`) or the two raw constructor arguments
passed through unchanged (`spec`, `logic`). No field is computed from
another field or from any external input.

**No definitions are supplied for**: what "the LaTeX spec" referenced
in the `execute_boot` comment actually is (no format, schema, or
example is given); what "self-validates" means operationally (no
validation code exists in this fragment, see §3); what "Non-Truncating,
Self-Regulating" (the `_seal_kernel` docstring) means for the output
bytes it returns, beyond the serialize/compress/encode steps actually
performed; or what distinguishes a "zero-sum, non-singular manifold"
(`execute_boot`'s docstring) from any other state — no code in this
fragment computes a sum, checks for singularity, or references a
manifold object. These are recorded as missing definitions, not
supplied by inference.

## 3. Explicit dependencies — documented, not inferred

- **`treatise_latex`** and **`abtm_engine`**: both are required,
  externally-supplied parameters with no default — the fragment
  depends on a caller to provide them, and defines neither itself.
  Nothing in the fragment states where either should come from; the
  parameter names themselves are the only textual evidence of intent
  (a LaTeX treatise document; some kind of "engine" object).
- **The trailing comment** (line 33), "Kernel initialized with full
  LaTeX treatise and ABTM logic," is the fragment's own, explicit,
  named link to "ABTM" — matching the combined manuscript's own
  self-title, "Unified ABTM Field Equations" (already established by
  `JUFE_37_Mathematical_Analysis.md`, cited there directly). This is a
  **documented naming correspondence**, not a demonstrated technical
  dependency: no code in this fragment imports, calls, or otherwise
  references anything from the combined manuscript or its runtime
  reimplementation (`abtm_expansion.py`); the only connection is the
  shared word "ABTM" in a comment and a parameter name.
  `abtm_expansion.py`'s own docstring (independently read for this
  report) confirms it is a "[s]eparate implementation of the
  mathematical operations described in... the Unified ABTM Field
  Equations and Relational Unified Field Mechanics: Analytical
  Resolution of Critical Cosmological Anomalies" — the second title
  matches the combined manuscript's provenance-map title (row 38)
  exactly. Whichever concrete `abtm_engine` object is actually
  supplied to source 13's constructor at runtime is a separate
  question from this fragment's own content, addressed in §4.3 below.
- **No reference of any kind to source 35**: this fragment contains no
  occurrence of "Shunt," "Magnon," "Radiation," `\hat{\mathcal{S}}_R`,
  or any other source-35 vocabulary (confirmed by direct reading of
  the complete 34-line text). No documented or inferred dependency on
  source 35 exists.
- **No reference to "CTTM"**: unlike source 14 (whose docstring names
  "Chiral Toroidal Tensegrity Manifold (CTTM)" directly), source 13's
  docstring and comments never mention CTTM. This is a documented
  absence, not an inferred one — checked directly.

## 4. Comparison against the current runtime

### 4.1 `oldmate2(4).py` — a near-identical, actively-loaded root-level counterpart

A root-level file, `oldmate2(4).py`, was found during this report's own
search (not previously cited in `CODE_PROVENANCE/README.md`, which
compares source 13/14 only against `src/kernel.py`, `src/engines/abtm.py`,
`jufe_64_grid_mapper.py`, and `abtm_expansion.py`). A direct,
whitespace-normalized `diff` against source 13's retained text (this
report's own check) finds the two are **identical except for two
lines**: `oldmate2(4).py` contains two additional lines, embedded
*inside* the `_seal_kernel` method's body, after its `return`
statement (hence unreachable dead code even if the method were
called):

```
        kernel = JUFE_Kernel("some text", "some engine")
        print(kernel.execute_boot())
```

These two lines do not appear anywhere in the retained source-13
fragment. `oldmate2(4).py` is not dead or unused. Six root-level
scripts reference it by name, but **statically inspecting each
script's own code path (not executing anything) shows only four of
the six ever reach `JUFE_Kernel`**:

- **Four scripts directly instantiate it**: `jufe_original_launcher.py`,
  `jufe_abtm_optimized_master_flow.py`, `jufe_abtm_results_launcher.py`,
  and `jufe_abtm_master_flow.py` each statically contain
  `oldmate2.JUFE_Kernel(...)` followed by a call to
  `.execute_boot()` on the result — confirmed by reading each
  occurrence directly, not by running the scripts.
- **Two scripts reference the filename as text only, with no code
  path reaching `JUFE_Kernel`**: `jufe_64_grid_mapper.py` lists
  `"oldmate2"` as one of two keys in `find_original()`'s
  `preferred_names` lookup dict, but `find_original()` is itself
  statically called exactly once in that file, with the literal
  argument `"oldmate1"` — the `"oldmate2"` dict entry is unused
  configuration data, never reached by that file's own code.
  `JUFE_RESEARCH/TOOLS/jufe_system_check.py` lists
  `"oldmate2(4).py"` only as a bare string inside a
  file-existence/compile-check list (`RUNTIME_FILES`); a direct
  search of that file finds zero occurrences of `JUFE_Kernel` or
  `oldmate2.` anywhere in it.

`JUFE_Repository_Assessment_2026-10-04.md` (line 174) already
identified `oldmate2(4).py` as a "legacy baseline implementation kept
for parity testing," verified "via test names/content" — this report's
own byte-level diff against the retained source-13 fragment, and its
static, code-path-level reading of each of the six scripts (§4.3), are
both new, more granular findings beyond that prior, higher-level
characterization.

### 4.2 `src/kernel.py` — renamed class, renamed fields, added validation

Read in full for this report (206 lines). The runtime class is named
`JUFEKernel` (no underscore) — a different literal name from source
13's `JUFE_Kernel`, not previously flagged in `CODE_PROVENANCE/README.md`'s
own comparison table. It uses an immutable `@dataclass(frozen=True)`
`KernelState` with seven fields: `version`, `integrity_hash`,
`lattice_basis`, `core_twist`, `specification`, `engine_name`,
`gate_state`.

Field-by-field comparison against source 13's six-key `kernel_state`
dict, checked directly (not assumed from the README's partial table,
which covered only `core_twist`, `lattice_basis`, and `integrity_hash`):

| Source 13 key | Runtime (`KernelState`) field | Relationship |
|---|---|---|
| `version` | `version` | Same field name; **different literal value** — source 13 hardcodes `"1.0.0-PROD"`; the runtime hardcodes `"0.2.0"`. Not previously noted in the README's table. |
| `integrity_hash` | `integrity_hash` | Same field name; source 13 hardcodes `"J-6-UNIFIED-FIELD"`; the runtime computes a real SHA-256 digest via `_compute_hash()` (lines 145–173) over the other six fields. Already noted in the README's table and independently re-confirmed here. |
| `lattice_basis` | `lattice_basis` | Same field name and same literal value, `"Z6-CLOSED-RING"`, in both. Already noted in the README's table and in `JUFE_8_Foundational_Analysis_2026-10-06.md` §5; re-confirmed here. |
| *(absent)* | `core_twist` | Source 13 has no `core_twist` key at all — this field exists only because the runtime's dataclass was evidently modelled on source 14's expanded structure (which does have `core_twist`), not source 13's. Not previously stated this way in any report consulted. |
| `spec` | `specification` | **Renamed**, not identically named — the README's table does not cover this pair at all. |
| `logic` | `engine_name` | **Renamed**, and also re-typed: source 13 stores whatever raw `abtm_engine` object is supplied; the runtime always stores `engine.__class__.__name__` (a string), set inside `JUFEKernel.__init__` itself (line 72). Not previously covered by the README's table. |
| `gate_state` | `gate_state` | Same field name; **different literal value** — source 13 hardcodes `"ACTIVE-PARITY-LOCK"`; the runtime hardcodes `"ACTIVE"`. Not previously noted anywhere consulted. |

**Added validation, absent from source 13**: the runtime constructor
raises `TypeError` if `specification` is not a string, `ValueError` if
it is empty, and `ValueError` if `engine` is `None` (lines 43–56).
Source 13's constructor performs no such checks on either parameter.
The runtime also adds `_validate_state()` (lines 119–143), called from
`execute_boot()` before sealing, which checks only that all seven
`KernelState` fields are truthy (`all(required)`) — **this is a
presence/non-emptiness check, not a check of any mathematical property**.
Source 13 has no equivalent validation step inside `execute_boot` at
all — it calls `_seal_kernel()` directly. The comment in source 13's
own `execute_boot`, "The engine self-validates against the LaTeX spec
at boot," is **not matched by code in either source 13 or the current
runtime**: neither performs any check of the supplied specification's
mathematical content, structure, or consistency with the manuscript
theory — both, at most, check that fields are non-empty strings. This
directly supports the task's instruction not to assume the current
implementation validates the underlying mathematics: it does not, and
neither did the original fragment's own code (only its comment claimed
otherwise).

**What gets passed as `specification` in practice**: `src/runtime.py`
(read in full for this report, 60+ lines relevant) constructs
`JUFEKernel(specification=parsed.title, engine=self.engine)` inside
`JUFERuntime.execute()` (lines 47–50) — `parsed.title` is a short title
string produced by `SpecificationParser`, not the full document text
that source 13's parameter name `treatise_latex` suggests. Any
validation of the parsed specification's content happens earlier, via
a separate `self.validator.validate(parsed)` call (line 43) — outside
and before `JUFEKernel` is even constructed, not as part of the
Kernel's own "boot" as source 13's comment implies.

### 4.3 How `oldmate2`/source 13's own class is actually driven

`jufe_original_launcher.py`'s `run_original_system()` function (lines
131–175, read in full for this report) is the clearest documented
account of how code matching source 13 is actually exercised. Read as
text, not executed, it:

- Loads `oldmate1` (source-14-equivalent) and `oldmate2`
  (source-13-equivalent) as separate modules (lines 142–143).
- Instantiates `oldmate1.ABTM_Engine()` and uses it to compute the
  stability check — "Calls the original method exactly as supplied"
  (line 148) — this exercises source 14's logic, not source 13's; no
  equivalent `ABTM_Engine`-style class exists in source 13 or
  `oldmate2(4).py`.
- Boots **both** kernel variants (lines 154–163), with an explicit
  comment: **"File 2 receives a JSON-safe engine identifier because
  its original code stores the supplied value directly"** — i.e., the
  launcher itself pre-converts the engine object to
  `engine.__class__.__name__` *before* passing it to
  `oldmate2.JUFE_Kernel(...)`, because source 13's own `__init__` would
  otherwise store the raw engine object unmodified into `kernel_state["logic"]`.

This comment is significant, independently-verified evidence of a
**latent limitation in source 13's own code as written**: `_seal_kernel`
calls `json.dumps(self.kernel_state)` directly on whatever was stored
in `logic`. A raw, non-JSON-serializable object (an engine instance)
passed as `abtm_engine` would make that `json.dumps` call raise a
`TypeError` at boot time — source 13's own code contains no safeguard
against this (unlike source 14, whose `__init__` already converts the
engine to a class-name string internally, line 20 of that fragment).
This is reasoned directly from reading what `json.dumps` requires and
what source 13's code does with its input, consistent with the task's
restriction against executing code — it was not observed by running
anything, only by reading both the fragment and the launcher's own
explanatory comment about why it works around exactly this.

### 4.4 Test coverage — asymmetric, and absent for source 13's own logic

A direct search of the complete `tests/` directory (9 files) for
`JUFEKernel`, `kernel.py`, `from .kernel import`, or `src.kernel`
returns **zero matches** anywhere. `src/kernel.py`'s `JUFEKernel` is
imported and used only by `src/runtime.py` (confirmed directly) — no
test exercises it. This extends `JUFE_8_Foundational_Analysis_2026-10-06.md`
§5's existing, narrower finding ("`tests/` was checked directly for
any reference to `kernel`, `core_twist`, or `lattice_basis` — zero
matches") to the class name and module path themselves, across the
whole test suite, not only those two field names.

By contrast, `tests/test_z6_equivalence.py` (its docstring read
directly for this report) performs extensive three-way comparison of
`compute_manifold_stability` across `src/engines/abtm.py`'s
`ABTMEngine`, `oldmate1(5).py`'s `ABTM_Engine`, and
`abtm_expansion.py`'s `ABTM_Expansion` — already confirmed passing by
`JUFE_Repository_Assessment_2026-10-04.md` (lines 210–214). **None of
the three implementations under that test is source 13 or
`oldmate2(4).py`** — the equivalence testing that exists covers the
stability-check logic associated with source 14, not source 13's own
kernel-state/sealing logic, which has no test coverage anywhere in the
repository.

## 5. Specification layer — checked, no dedicated governance found

`JUFE_REPOSITORY_SPECIFICATION/Part I - Repository Foundations/Chapter 4
- Mathematical Specification Layer.md.md` (read in full for this
report) was searched directly for "kernel," "Z6," "trace," "CTTM," and
"gate_state" — zero matches; the chapter is abstract governance prose
about how a mathematical specification layer *should* behave, with no
concrete content about this kernel at all. No other file under
`JUFE_REPOSITORY_SPECIFICATION/` references these terms (confirmed by
directory-wide search). No dedicated specification document formalizes
or governs the `"Z6-CLOSED-RING"` lattice-basis claim, the
`"3PI_NON_ORIENTABLE"` core-twist claim (source 14 only), or any other
hardcoded field in either source 13 or `src/kernel.py`'s `KernelState`.

## 6. Source 14 — comparison context only, not analysed

Per the task's instruction, source 14 is not given a dedicated
analysis in this report. It is referenced above only where source 13
and 14 are directly comparable (§4.1's `oldmate1(5).py`/`oldmate2(4).py`
pairing, §4.2's field-structure comparison, §4.3's launcher
orchestration, §4.4's test-coverage asymmetry). Source 14's own full
chapter-by-chapter content, its `ABTM_Engine(ABTM_Expansion)`
inheritance chain, and its relationship to `abtm_expansion.py` and the
combined manuscript are **not** independently catalogued or assessed
here — any such reading is left to a future, dedicated source-14
report.

## 7. Unresolved questions and missing definitions — preserved, not adjudicated

- What "the LaTeX spec" (source 13's own comment) concretely refers
  to, in format or content, is not stated anywhere in the fragment,
  and no retained source defines it for this specific kernel.
- Whether the current runtime's `JUFEKernel` is intended as a
  successor to, replacement for, or independent reimplementation of
  source 13's `JUFE_Kernel` is not stated by any file read for this
  report — `CODE_PROVENANCE/README.md`'s own "Important limitation"
  section explicitly disclaims that its correspondence table is "not
  proof that the current runtime was literally derived line-by-line
  from `13.md`." This report does not resolve that question; it
  documents the concept-level correspondences and renames found (§4.2)
  without asserting lineage.
- Whether `oldmate2(4).py`'s two extra, unreachable lines (§4.1) were
  an accidental paste, a deliberate but abandoned test stub, or
  something else is not stated anywhere; this report records the
  textual fact only.
- Whether the `abtm_engine` object actually supplied to source 13's
  constructor, in any real invocation, is ever a non-string object
  that would trigger the `json.dumps` limitation identified in §4.3 is
  not established — the launcher's own comment shows the risk was
  recognised and avoided by the caller, not that it was ever
  triggered.

## 8. Coverage, dependencies, and limitations

**Full-text coverage**: source 13's complete 34 lines were read for
this report (not sampled) — the first dedicated reading on record.

**Files read in full or by targeted, text-only inspection for this
report**: source 13 (34 lines); `oldmate2(4).py` and `oldmate1(5).py`
(both, for the diff in §4.1); `src/kernel.py` (206 lines, in full);
`src/runtime.py` (relevant construction/boot code); `src/engines/abtm.py`
(class/method signatures relevant to §4.3); `abtm_expansion.py`'s
module docstring; `jufe_original_launcher.py`'s `run_original_system`
function and `find_original`/`load_oldmate1`/`load_normal_module`
helpers; `tests/test_z6_equivalence.py`'s docstring; `CODE_PROVENANCE/README.md`
and `MANUSCRIPTS/README.md`'s excluded-artifacts table; the relevant
`PROVENANCE_MAP.md` row; `JUFE_REPOSITORY_SPECIFICATION`'s Chapter 4.
None of these files was executed, imported at runtime, or run as a
script — all reading was done as text via the Read/Grep tools.

**Dependencies**: §4.1 and §4.3's claims about which scripts load
`oldmate2(4).py` rest on direct text search (`grep`) across the named
files, not on running them. §4.4's test-coverage claim rests on a
direct, complete search of `tests/`, not on running the test suite
(consistent with the task's restriction against execution — this
report does not know whether the tests currently pass, only what they
do and do not reference by name).

**Limitations**:
- Of the six root-level scripts confirmed to reference `oldmate2` by
  name (§4.1), only `jufe_original_launcher.py`'s own
  `run_original_system` function was read in full; the other three
  that do instantiate `oldmate2.JUFE_Kernel(...)`
  (`jufe_abtm_optimized_master_flow.py`, `jufe_abtm_results_launcher.py`,
  `jufe_abtm_master_flow.py`) were checked only for the specific
  instantiation/boot call cited in §4.1/§9, not read line-by-line in
  full, and may differ from `jufe_original_launcher.py`'s own
  JSON-serialization work-around in other respects not inspected here.
  The two that do **not** instantiate it (`jufe_64_grid_mapper.py`,
  `jufe_system_check.py`) were specifically checked for this absence
  (§4.1) and are not a coverage gap on that point.
- `src/engines/abtm.py` (407 lines) and `abtm_expansion.py` (670 lines)
  were read only for the specific methods/docstrings cited; neither
  was read in full.
- This report does not assess whether `src/kernel.py`, `oldmate2(4).py`,
  or any other file's code is correct, secure, or fit for any purpose
  — only what each states and does, as text.
- Per the task's scope, source 14's own full content was not
  catalogued; source 35 and the combined manuscript were not opened in
  this pass — §3's combined-manuscript naming correspondence rests on
  already-cited material from `JUFE_37_Mathematical_Analysis.md` and a
  direct read of `abtm_expansion.py`'s own docstring, not on opening
  the combined manuscript itself.
- No independent review, correction, or handover/continuity update was
  performed in this pass, consistent with the task's scope.

## 9. Summary for the record

- **Exact path saved**: `~/Desktop/JUFE/docs/reports/JUFE_13_Foundational_Analysis_2026-10-12.md` (this file).
- **Source 13 is**: a 34-line Python fragment defining `JUFE_Kernel`, a
  minimal, unvalidated class that stores two caller-supplied values
  (`treatise_latex`, `abtm_engine`) and four hardcoded literals into a
  plain dict, then serializes/compresses/encodes that dict. Its
  docstring and comments claim more ("enforces... as immutable laws,"
  "self-validates against the LaTeX spec") than its code performs —
  none of those claims is backed by any check in the fragment itself.
- **Already-covered material, cited not reproduced**: the
  `lattice_basis`/`core_twist` name-echo-without-computation finding
  (`JUFE_8_Foundational_Analysis_2026-10-06.md` §5); the Z6
  trace-parity lineage from `13.md`/`14.md` through to
  `test_z6_equivalence.py`'s confirmed three-way parity
  (`JUFE_Repository_Assessment_2026-10-04.md`); `oldmate1(5).py`/
  `oldmate2(4).py`'s general characterization as parity-test legacy
  files (same report).
- **New findings from this pass**: `oldmate2(4).py` is byte-identical
  to source 13 except for two unreachable, misplaced example-usage
  lines; the runtime's `JUFEKernel`/`KernelState` renames two of
  source 13's six fields (`spec`→`specification`, `logic`→`engine_name`)
  and changes two literal values (`version`, `gate_state`) not
  previously compared; of the six root-level scripts that reference
  `oldmate2` by name, static inspection of each script's own code path
  shows only **four** actually instantiate `oldmate2`/source 13's
  class (`jufe_original_launcher.py`, `jufe_abtm_optimized_master_flow.py`,
  `jufe_abtm_results_launcher.py`, `jufe_abtm_master_flow.py`), with
  one of those four explicitly working around a latent
  JSON-serialization limitation in source 13's own, unmodified
  `__init__` logic; the other two (`jufe_64_grid_mapper.py`,
  `jufe_system_check.py`) reference only the filename as text, with no
  code path reaching `JUFE_Kernel`. No test anywhere in the repository
  exercises `JUFEKernel`, `kernel.py`, or `oldmate2`'s `JUFE_Kernel` by
  name — only source 14's stability-check logic has equivalence test
  coverage.
- **Coverage status**: source 13 now has a first full-text reading and
  a detailed runtime comparison. Per the full-collection audit's own
  criterion, this does not by itself constitute an accepted
  independent-review cycle, so source 13 should not yet be treated as
  meeting that criterion until reviewed.
- **Neither source 13's kernel nor the runtime's `JUFEKernel`/
  `KernelState` sealing layer validates the underlying mathematics**:
  confirmed directly, scoped to these two specifically — neither
  checks any mathematical property of the manifold theory; both, at
  most, check that string fields are non-empty. `src/validator.py`'s
  own `SpecificationValidator.validate()` method, called earlier in
  `JUFERuntime.execute()` (§4.2) before the Kernel is even
  constructed, was **not** inspected in this pass; whether its checks
  are mathematical or merely structural is not assessed here, and this
  report's conclusion does not extend to it or to any other part of
  the current implementation.
- **Remaining limitations**: as stated in §8.

## 10. Correction trail — 12 October 2026, 20:27 AEST (2026-10-12T10:27:52Z)

An independent review
(`docs/reports/JUFE_13_Foundational_Analysis_Independent_Review_2026-10-12.md`,
agent Nora) found provenance, the field-by-field `kernel_state`/
`KernelState` comparison (§4.2), the `oldmate2(4).py` byte-diff finding
(§4.1), the launcher's JSON-serialization work-around (§4.3), the
test-coverage asymmetry (§4.4), and the specification-layer search
(§5) all accurate on independent, direct re-verification. **One
correction, one qualification, and one low-severity completeness note
were required**, confined to §§1, 4.1, 8, and 9.

**Independently re-verified before correcting**:
1. Re-read source 13's lines 32–34 directly: line 32 is `# Execution
   Logic:`, a distinct section-header comment; lines 33–34 are the two
   comments the original §1 table row quoted. The row's own stated
   range ("32–34") included line 32, but its content was never
   individually quoted, so "No line falls outside this accounting"
   (the sentence immediately following) was not fully precise about
   that one line's specific text.
2. Statically re-checked all six scripts named in §4.1 for whether
   `oldmate2.JUFE_Kernel` is actually instantiated, by direct reading
   (not execution): `jufe_original_launcher.py`,
   `jufe_abtm_optimized_master_flow.py`, `jufe_abtm_results_launcher.py`,
   and `jufe_abtm_master_flow.py` each do. `jufe_64_grid_mapper.py`
   calls `find_original()` exactly once, with the literal argument
   `"oldmate1"` only — its `"oldmate2"` dict entry in
   `preferred_names` is unused configuration data. `jufe_system_check.py`
   contains `"oldmate2(4).py"` only as a bare string inside a
   `RUNTIME_FILES` existence/compile-check list, with zero occurrences
   of `JUFE_Kernel` or `oldmate2.` anywhere in the file. The original
   §4.1/§9 text's "directly instantiated in... six... scripts" claim
   was therefore true of only four of the six.
3. Confirmed `src/validator.py` exists (65 lines) and defines
   `SpecificationValidator.validate()` at line 15, called from
   `src/runtime.py`'s `JUFERuntime.execute()` (line 43) before
   `JUFEKernel` is constructed — and confirmed this file's own method
   body was not read for the original report (absent from its §8
   "Files read" list). §9's original headline, "The current
   implementation does not validate the underlying mathematics,"
   therefore extended further than what was actually inspected, even
   though §2's and §4.2's own specific claims (about source 13 and
   `src/kernel.py`/`_validate_state()` only) were already correctly
   scoped and required no change.

**Corrections applied**:
- §1's table row for lines 32–34 now reads "Three trailing comments"
  and quotes all three, including line 32's "# Execution Logic:".
- §4.1 now states that static inspection of each script's own code
  path (not execution) shows `JUFE_Kernel` is directly instantiated in
  **four** of the six scripts that reference `oldmate2` by name, and
  describes precisely why the other two (`jufe_64_grid_mapper.py`,
  `jufe_system_check.py`) do not reach it — an unused lookup-table
  entry and a file-existence-check string, respectively.
- §8's corresponding limitations bullet is rewritten to match: it no
  longer implies all six scripts' instantiation status was uncertain;
  it now distinguishes the three instantiating scripts whose
  surrounding code was not fully read (a genuine remaining gap) from
  the two non-instantiating scripts (specifically checked, not a gap).
- §9's "New findings" bullet and headline validation bullet are both
  corrected: the former now states "four" with the two non-reaching
  scripts named and explained; the latter is rescoped to "neither
  source 13's kernel nor the runtime's `JUFEKernel`/`KernelState`
  sealing layer," with `src/validator.py` explicitly named as unread
  and excluded from the conclusion.

**Preserved, not changed**: §0, §2–§4.2 (other than the §4.1 edits
above), §4.3, §4.4, §5, §6, §7, and the rest of §8 are unchanged — the
review found them accurate, including the specific (correctly scoped)
claims in §2 and §4.2 about source 13 and `src/kernel.py`'s own
sealing/validation logic. The substantive findings are otherwise
unchanged: `oldmate2(4).py` remains confirmed byte-identical to source
13 apart from the two dead lines; the field renames and value changes
in §4.2 are unaffected; the test-coverage asymmetry in §4.4 is
unaffected.

This report stops here for Nora 2's recheck.
