# JUFE Manuscript Source Corpus

## Purpose

This directory contains the canonical manuscript source corpus used by JUFE.

These files are preserved as SOURCE material.

Their inclusion does NOT mean that every equation, proof, interpretation,
empirical claim, or theoretical statement has been independently verified
or incorporated into the JUFE specification/runtime.

Source material must not be silently corrected, reconciled, or rewritten.

---

## Corpus Status

Current canonical corpus:

- 17 canonical manuscript files
- 1 known missing manuscript/source
- duplicate source artifacts excluded
- code artifacts excluded from the manuscript corpus
- non-manuscript organizational/template artifacts excluded
- 2 known title/content mismatches excluded (label does not match body)
- 1 known canonical/template classification conflict (item 17 vs. `36.md`)

Status: CANONICAL CORPUS v1.3

### v1.1 update (3 October 2026)

Reconciled against the JUFE Source Assessment Pack's `SOURCE_MANIFEST.json`
(38 originals / 26 distinct source texts). This update added two previously
unindexed canonical manuscripts (items 15-16 below), one previously
unindexed unresolved-provenance source (`16.md`), one previously unindexed
non-manuscript template artifact (`36.md`), two previously unindexed
duplicate-copy entries (`19.md`, `33.md`), and a standalone preserved
fragment from `11.md`. No existing canonical item, DEF identifier, or
manuscript content was altered. See:

- `PROVENANCE_MAP.md` (this directory) - full 38-original disposition map
- `../CODE_PROVENANCE/README.md` - `13.md`/`14.md` code-fragment provenance
- `../../../../JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md`
  - unresolved documentation conflicts surfaced by this reconciliation

### v1.2 update (3 October 2026)

Closed the `4.md` indexing gap (see "atriΩ Non-Arbitrary Predictor
Development Pt.2" below - `4.md` is now named alongside `18.md`).
The earlier pass verified original checksums. The unwanted repository
archive has since been removed; original custody remains in the user's
main archive. Exact retained variants `4.md`, `5.md`, `16.md`, and `34.md`
are preserved in the existing `MISSING_SOURCE/` folder.
Confirmed that `Research Processing/Manuscript 001/Original Manuscript.md`
and `Research Processing/Manuscript 002/Original Manuscript.md` (elsewhere
in the JUFE repository, outside this `MANUSCRIPTS/` tree) are
word-for-word matches to the two halves of the combined "Relational Unified
Field Mechanics" / "Unified ABTM Field Equations" source artifact, distinct
from and more faithful than the independently-rewritten
`Specifications/Research Archive/Manuscript 001/002` files discussed in
`KNOWN_DOCUMENTATION_CONFLICTS.md` Conflict A. Full detail and the complete
1-38 checksummed table are in the rebuilt `PROVENANCE_MAP.md`.

### v1.3 update (3 October 2026)

This pass pulled in `origin/main` commit `08ec6da` ("Add TFJ canonical
monograph architecture V4 manuscript"), which had added
`CANONICAL/TFJ-Canonical-Self-Bootstrapping-Monograph-Architecture-V4.md`
directly to the repository, outside of and prior to this reconciliation's
local work. That file was previously absent from this README's numbered
list entirely (the list above still only counted up to item 16). It is now
named as item 17 below so the index matches the contents of `CANONICAL/`.

**Flag — not resolved by this pass:** item 17's text is, modulo line-wrap
and whitespace only, the same underlying content as source artifact
`36.md`, which this same README (see "Non-Manuscript Organizational /
Template Artifacts" below) already classifies as a non-manuscript
`FILES_MANIFEST` template and preserves at
`NON_MANUSCRIPT_TEMPLATES/36-v4-files-manifest-template.md` — not as a
canonical manuscript. The source pack's classification and the
already-committed GitHub classification disagree on the same text. Neither
file was moved, edited, or deleted to resolve this; see
`../../../../JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md`
Conflict C.

---

## Canonical Manuscripts

1. TFJ-Holistic-Stability-and-Universal-Scaling.md
2. TFJ-Non-Arbitrary-Initialization-Protocol-Foundation-Layer.md
3. TFJ-atriOmega-Non-Arbitrary-Predictor-Pt4.md
4. TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md
5. TFJ-Volume-I-Ch01-Planck-Floor-Constraint.md
6. TFJ-Volume-I-Ch02-Generalized-Field-Syntax-and-Operator-Formalism.md
7. TFJ-Volume-II-Ch01-Mechanics-of-Transmission.md
8. TFJ-Volume-II-Ch03-Quadrature-Protocols.md
9. TFJ-Volume-III-Ch01-Singularity-Synthesis-and-Planck-Scale-Horizon.md
10. TFJ-Volume-III-Ch03-Horizon-Dependent-Shifting.md
11. TFJ-Volume-IV-Hysteresis-and-Emergent-Evolution.md
12. TFJ-Unified-Harmonic-Manifold-Executive-Abstract.md
13. TFJ-Formal-Proofs-Appendices-and-Theoretical-Lineage.md
14. TFJ-Shunt-Radiation-Equivalence-in-Magnon-Systems.md
15. TFJ-Unified-Harmonic-Manifold-Four-Volume-Outline-and-Verification-Protocols.md
16. TFJ-Zero-Sum-Constraint-Load-and-Shunt-Mechanics.md
17. TFJ-Canonical-Self-Bootstrapping-Monograph-Architecture-V4.md

### Items 15-16 (added 3 October 2026)

**15.** Source artifact `7.md`. Four-volume architectural outline and
implementation-verification directions for the M^6 / Unified Harmonic
Manifold treatise. Distinct from the comprehensive synthesis already held
as canonical item 4 (`TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md`);
this source ends mid-sentence ("...to ensure no energy is \"lost") in the
supplied artifact. Redundant copy: `19.md` (now listed under "Excluded
Duplicate Source Artifacts" below).

**16.** Source artifact `37.md`. Explanatory source covering the zero-sum
tension constraint, the Golden-Ratio-derived damping/load constant, the
Shunt operator for over-pressure redistribution, and a geometric derivation
of the fine-structure coupling. The supplied artifact carries no
author/comment/post identifier; attribution to Thomas F. Jennings is
supplied context from the source pack, not an in-file statement. No
redundant copies identified.

### Item 17 (already present in `CANONICAL/`; indexed 3 October 2026)

**17.** `TFJ-Canonical-Self-Bootstrapping-Monograph-Architecture-V4.md`.
Added directly to `origin/main` by commit `08ec6da` prior to this
reconciliation's local work; not drawn from the source-pack's 1-38
numbered artifacts by this pass. See the "Flag" in the v1.3 update note
above and Conflict C in `KNOWN_DOCUMENTATION_CONFLICTS.md` for the
unresolved classification question (same text also held as a non-manuscript
template under source `36.md`).

---

# Missing / Unresolved Sources

## atriΩ Non-Arbitrary Predictor Development Pt.3

STATUS: MISSING_SOURCE

Known artifact:

    5.md

The supplied artifact contained the title identifying Pt.3 but no
substantive manuscript body.

Required action:

Obtain the original complete Pt.3 manuscript/source from Thomas F. Jennings.

DO NOT reconstruct Pt.3 from Pt.1, Pt.2, Pt.4, JUFE, or inference.

---

## atriΩ Non-Arbitrary Predictor Development Pt.2

STATUS: SOURCE_PROVENANCE_UNRESOLVED

Known artifacts:

    4.md  (manifest KEEP REPRESENTATIVE for this duplicate group)
    18.md (manifest REDUNDANT ACTIVE COPY of 4.md)

**Gap closed 3 October 2026:** `4.md` is the artifact `SOURCE_MANIFEST.json`
designates as the representative for this duplicate group (five repeated
Foundation Layer blocks with metadata/preamble variants), but it was
previously absent from this README entirely - only its redundant copy
`18.md` was discussed. Both are now named here together. Neither is
separately copied into `CANONICAL/`, because their substantive content is
the same Non-Arbitrary Initialization Protocol / Foundation Layer material
already held as canonical item 2
(`TFJ-Non-Arbitrary-Initialization-Protocol-Foundation-Layer.md`, sourced
from `3.md`). The retained `4.md` variant is preserved unchanged at `MISSING_SOURCE/4.md`.
Its redundant `18.md` copy remains in the external source pack; it is not
copied into this repository. See `PROVENANCE_MAP.md`.

The supplied artifact identifies itself as Pt.2, but its substantive
material corresponds to the Non-Arbitrary Initialization Protocol /
Foundation Layer material already represented in the canonical corpus.

Required action:

Ask Thomas F. Jennings whether:

1. this is the intended Pt.2 source; or
2. a distinct/original Pt.2 manuscript exists.

Do not create a separate canonical Pt.2 manuscript until this is resolved.

---

## Vacuum Mass Gap

STATUS: SOURCE_PROVENANCE_UNRESOLVED

Known artifact:

    34.md

The source artifact was labelled "Vacuum Mass Gap", but its substantive
contents identify themselves as:

    Non-Arbitrary Initialization Protocol: Foundation Layer

Required action:

Ask Thomas F. Jennings whether a separate/original "Vacuum Mass Gap"
manuscript exists.

Do not infer or reconstruct its contents from the mislabeled artifact.

---

## "a tri Ω=smoke" (added 3 October 2026)

STATUS: SOURCE_PROVENANCE_UNRESOLVED

Known artifact:

    16.md

The source artifact carries the title/label "a tri Ω=smoke" and contains
two repeated Foundation Layer blocks. Its substantive content corresponds
to the Non-Arbitrary Initialization Protocol / Foundation Layer material
already represented in the canonical corpus (see canonical item 2), the
same pattern already recorded above for the "Vacuum Mass Gap" artifact
(`34.md`). The artifact's body overlaps the Pt.1/Pt.2 material, but its
metadata and title provenance are distinct from both.

Required action:

Ask Thomas F. Jennings whether a separate/original "a tri Ω=smoke"
manuscript exists.

Do not infer or reconstruct its contents from the mislabeled artifact. Do
not create a separate canonical entry until this is resolved.

---

# Excluded Duplicate Source Artifacts

The following numbered artifacts were not deliberately imported into the
canonical corpus because they duplicate material represented by canonical
sources:

- 9.md
- 11.md**
- 15.md
- 17.md
- 18.md*
- 19.md (duplicate of canonical item 15, `7.md`; added 3 October 2026)
- 20.md
- 21.md
- 22.md
- 23.md
- 24.md
- 25.md
- 33.md (duplicate of canonical item 14, `35.md`; added 3 October 2026)

*18.md is additionally retained as an unresolved Pt.2 provenance record.

**11.md's manuscript body duplicates 12.md, but 11.md also carries a unique
51-word closing conversational prompt not present in 12.md. That prompt is
preserved verbatim, separately from the canonical manuscript body, at
`CANONICAL/TFJ-Volume-I-Closing-Conversational-Prompt-Fragment.md` (added 3
October 2026). The prompt's speaker/attribution is unknown and is recorded
as such in that file.

Original/archive copies should be retained outside CANONICAL where available.

---

# Excluded Non-Manuscript Artifacts

The following supplied artifacts contain code/implementation material rather
than manuscript source material:

- 13.md
- 14.md

These should not be stored in MANUSCRIPTS/CANONICAL.

Catalogued separately within the JUFE implementation/code provenance
structure at `../CODE_PROVENANCE/README.md` (added 3 October 2026), which
also records verified links to the current runtime files that independently
reimplement the same named concepts (`core_twist`, the Z6 trace diagnostic,
and the `ABTM_Expansion` base class).

## Non-Manuscript Organizational / Template Artifacts (added 3 October 2026)

The following supplied artifact is a Python-style organizational template
(a `FILES_MANIFEST` of LaTeX chapter stubs for a planned "V4" monograph
re-architecture), not manuscript prose and not executable code:

- 36.md - "Canonical Self-Bootstrapping Monograph Architecture (V4)".
  Defines a terminology-normalization and chapter-ontology scheme for a
  future monograph restructuring; does not itself contain completed
  dynamics, proofs, or a working generator. Preserved verbatim at
  `NON_MANUSCRIPT_TEMPLATES/36-v4-files-manifest-template.md`. Not counted
  in the canonical manuscript corpus.

---

# Source Integrity Rule

CANONICAL means:

"the selected canonical source copy held by JUFE"

It does NOT mean:

"scientifically verified"
"mathematically proven"
"accepted into the JUFE specification"
"implemented in runtime"

Manuscript claims remain manuscript claims until separately analysed.

---

# Questions for Thomas F. Jennings

1. Can you provide the complete original source for:
   "atriΩ Non-Arbitrary Predictor Development Pt.3"?

2. Does a distinct original source exist for:
   "atriΩ Non-Arbitrary Predictor Development Pt.2"?
   The supplied Pt.2 artifact appears to contain Foundation Layer material.

3. Does a distinct manuscript titled:
   "Vacuum Mass Gap"
   exist?
   The supplied artifact bearing that label contains Foundation Layer
   material instead.

When these questions are resolved, update this README and the corresponding
source status before changing the canonical corpus.

---

## Corpus Principle

PRESERVE FIRST -> CATALOGUE -> VERIFY -> FORMALISE -> IMPLEMENT

Never silently invent missing mathematics or repair source history.
## Retained unresolved source artifacts

`MISSING_SOURCE/4.md`, `5.md`, `16.md`, and `34.md` preserve the supplied
artifacts unchanged, including their original labels and title-only material.
These are source records, not reconstructed or reclassified manuscripts.
