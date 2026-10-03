# JUFE Code-Fragment Source Provenance

## Purpose

`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/README.md` excludes source
artifacts `13.md` and `14.md` from the manuscript corpus because they
contain code/implementation material rather than manuscript prose, and
states that they would "later be catalogued separately within the JUFE
implementation/code provenance structure." This directory is that catalog.

As with the manuscript corpus, cataloguing these fragments here does **not**
mean their content has been verified, proven, or that the current runtime
is a copy of them. It means they are preserved and their relationship to
current runtime code has been checked and is recorded below.

## Original fragments (preserved verbatim, heading-numeral stripped only)

- `ORIGINAL_FRAGMENTS/13-kernel-fragment.md` — from source artifact `13.md`
  (`sha256: 7e22d82eca25071e9659ca8c7695f135a15bca5132d1f3289589f7428153a67b`
  per `SOURCE_MANIFEST.json`). Defines a `JUFE_Kernel` class with a
  `kernel_state` dict (`version`, `integrity_hash`, `lattice_basis`,
  `spec`, `logic`, `gate_state`), an `execute_boot()` method, and a
  `_seal_kernel()` method that serializes/compresses/encodes the state.
- `ORIGINAL_FRAGMENTS/14-kernel-abtm-fragment.md` — from source artifact
  `14.md` (`sha256:`
  `fb84ae2f885ad4d38037233431aa9ac3c3dd2f3cde9df78d6a84777e63718372`). A
  later/expanded variant of the same `JUFE_Kernel` class that adds a
  `core_twist` field (`"3PI_NON_ORIENTABLE"`) to `kernel_state`, changes
  `logic` to a class-name string via `abtm_engine.__class__.__name__`, and
  adds a separate `ABTM_Engine(ABTM_Expansion)` class with a
  `compute_manifold_stability(psi_barrier)` method implementing
  `sigma = np.trace(psi_barrier) % 6; return sigma == 0`.

Both fragments were confirmed byte-identical to the source pack originals
except for the stripped leading bare-numeral heading line (`13` / `14`),
exactly as `MANUSCRIPTS/CANONICAL` does for manuscript sources.

## What `13.md` vs `14.md` actually differ on

`14.md` is not a copy of `13.md` with unrelated content; it is a direct
expansion of the same `JUFE_Kernel` class with three additions: (1) the
`core_twist` field, (2) class-name serialization for `logic` instead of
storing the engine object directly, and (3) the new `ABTM_Engine` subclass
and its trace-mod-6 stability check. `14.md` also references
`ABTM_Expansion` as a base class without defining it — the fragment assumes
that class already exists elsewhere.

## Verified relationship to the current runtime (`src/`, repo root)

The following was confirmed by direct inspection of the current JUFE
Python source — it is reported as found, not assumed:

| Concept in `13.md` / `14.md` | Current runtime location | Relationship |
|---|---|---|
| `core_twist: "3PI_NON_ORIENTABLE"` | `src/kernel.py` (field `core_twist`, value `"3PI_NON_ORIENTABLE"` set at initialization) | Same field name and same literal value as `14.md`. |
| `lattice_basis: "Z6-CLOSED-RING"` | `src/kernel.py` (`lattice_basis="Z6-CLOSED-RING"`) | Same field name and same literal value as both `13.md` and `14.md`. |
| `integrity_hash` | `src/kernel.py` (`integrity_hash` field, computed via `_compute_hash()`) | Same field name; current implementation computes rather than hardcodes the value (`13.md`/`14.md` use a hardcoded `"J-6-UNIFIED-FIELD"` placeholder). |
| `sigma = Trace(Psi) mod 6` / `compute_manifold_stability` | `src/engines/abtm.py` (`sigma = np.trace(...) % 6`) and `jufe_64_grid_mapper.py` (`trace_mod_6 = trace % 6`) | Same mathematical operation (trace modulo 6), reimplemented independently in two current runtime files. |
| `class ABTM_Engine(ABTM_Expansion)` — `ABTM_Expansion` referenced but not defined in the fragment | `abtm_expansion.py`, `class ABTM_Expansion:` (line 63) | The repository's own root-level `abtm_expansion.py` module docstring states it "provides the missing `ABTM_Expansion` base class that `ABTM_Engine` expects" and that it is a "[s]eparate implementation of the mathematical operations described in" the Unified ABTM Field Equations and the Relational Unified Field Mechanics manuscript. This is a **deliberate, disclosed, from-scratch reimplementation**, not a copy of the `13.md`/`14.md` fragment's exact code. |

## Important limitation

This table records verified **name and concept correspondence**, not proof
that the current runtime was literally derived line-by-line from `13.md` or
`14.md`. `abtm_expansion.py`'s own docstring is explicit that it is an
independent numerical implementation, not a transcription of the supplied
fragments. No claim is made here that `13.md`/`14.md` are the historical
origin of `src/kernel.py` or `src/engines/abtm.py` — only that the same
named concepts (`core_twist`, `Z6-CLOSED-RING` lattice basis, trace-mod-6
parity, and an `ABTM_Expansion` base class) appear in both the original
fragments and the current runtime, and that this correspondence was
checked, not assumed.

## What this catalog does not do

- It does not change, refactor, or annotate `src/kernel.py`,
  `src/engines/abtm.py`, `abtm_expansion.py`, or `jufe_64_grid_mapper.py`.
- It does not promote `13.md`/`14.md` into the manuscript corpus.
- It does not assert that the fragments' code ever ran as part of a
  production JUFE build; they are preserved as supplied source material.

## Traceability

- Added: 3 October 2026, as part of the source-to-documentation
  reconciliation pass.
- Referenced from: `../MANUSCRIPTS/README.md` ("Excluded Non-Manuscript
  Artifacts") and `../MANUSCRIPTS/PROVENANCE_MAP.md`.
