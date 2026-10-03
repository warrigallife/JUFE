# Known Documentation Conflicts (Unresolved — Do Not Resolve Without Review)

Document ID: JUFE-CONFLICTS-001

Added: 3 October 2026, as part of a source-to-documentation reconciliation
pass requested and authorized by the repository owner. This document is a
**record of conflicts as found**. It does not resolve, merge, renumber, or
rewrite any of the material it describes. Any future resolution (choosing
one representation over another, renumbering a DEF identifier, deleting a
stale file) requires a deliberate, separately authorized review — not a
casual cleanup.

See also `JUFE_COLLABORATOR_HANDOVER.md` (section added 3 October 2026) and
`JUFE_Source_Assessment_Pack/SOURCE_DOC_RECONCILIATION_2026-10-03.md` for the
full reconciliation report these conflicts were drawn from.

---

## Conflict A — Two incompatible documentary representations of the same manuscript

The combined source file `Relational Unified Field Mechanics: Analytical
Resolution of Critical Cosmological Anomalies` (by Thomas F. Jennings,
which also carries an appended section titled "The Unified ABTM Field
Equations") is represented twice in this repository, with materially
different content:

**Representation 1 — faithful, section-cited quotation layer:**

- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/MASTER_DEFINITION_INDEX.md`
  (DEF-0001 through DEF-0036, GOV-0001)
- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/DEFINITIONS/*.md`
- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/03_REFERENCE_LIBRARY/LEMMAS/LEMMA-3.1_Cross_Axial_Helical_Deflection.md`
- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/03_REFERENCE_LIBRARY/THEOREMS/03_REFERENCE_LIBRARY/THEOREMS/THEOREM_4_2.md`
- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/03_REFERENCE_LIBRARY/EVIDENCE/*.md`
- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/02_SPECIFICATION/Volume_III/00-Normative-Traceability-Matrix.md`
  (states this manuscript "is the normative authority for Volume III")

These files quote the manuscript closely and cite specific sections (e.g.
"§1.1", "§2.1", "§2.2", "§3"). Spot-checking during the reconciliation pass
confirmed verbatim or near-verbatim matches against the actual source text
(e.g. THEOREM-4.2 quotes "the underlying geometric information cannot be
clipped or truncated" directly from the manuscript's Section 2.2).

**Addendum (3 October 2026, follow-up pass):** a third location was found
to hold a full word-for-word copy of the combined source (modulo markdown
heading-marker formatting only): `Research Processing/Manuscript
001/Original Manuscript.md` and `Research Processing/Manuscript
002/Original Manuscript.md` (note — this is the `Research Processing/`
directory at the JUFE repository root, a different location from
`Specifications/Research Archive/` below). This strengthens, and does not
change, the conclusion of this conflict: a faithful verbatim copy of the
manuscript was available elsewhere in the repository that
`Specifications/Research Archive/Manuscript 001/002` could have drawn from
but evidently did not. See
`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/PROVENANCE_MAP.md` for the
verification detail. This addendum does not alter the conflict's
conclusion and nothing in `Research Processing/` was changed to record it.

**Representation 2 — independently written prose, same claimed title/split:**

- `Specifications/Research Archive/Manuscript 001/Manuscript-001.md` —
  titled "Relational Unified Field Mechanics: Analytical Resolution of
  Critical Cosmological Anomalies", but its body consists of generic
  relational-philosophy definitions (Relation, State, Structure, Field,
  Information, Observer, Interaction, Emergence, Symmetry, Transformation,
  Conservation, Equilibrium, Perturbation, Evolution) and a JUFE Kernel/
  Domain Engine architecture description. None of the manuscript's actual
  axioms (Axiom I "Absolute Conservation of Field Duality", Axiom II
  "Gradient Autonomy"), named mechanisms (Boundary Jam, Phase Lock,
  Cross-Axial Helical Deflection, Harmonic Packet ejection), or equations
  (e.g. `D ∝ -∇M`, `dM/dt = -dA/dt`) appear anywhere in this file.
- `Specifications/Research Archive/Manuscript 002/Manuscript 002.md` —
  titled "Analytical Boundary Transfer Mechanics (ABTM)", building on
  Manuscript 001. Its body describes Z6 residue-class trace parity,
  Chiral Toroidal Tensegrity Manifold (CTTM) geometry (chirality, toroidal
  continuity, tensegrity), a "Hydraulic Escapement Sequence", and
  "Scale-Transfer Projection Operators". This vocabulary matches the code
  fragment in source artifact `14.md` (see
  `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/README.md`) much more closely
  than it matches the "Unified ABTM Field Equations" section of the actual
  combined manuscript (which instead describes a static Z6 lattice coupled
  to a *dynamic mod-7 temporal harmonic*, a Tensegrity-Stress Tensor
  `∇_μ T_total^(μν) = 0`, a sensitivity matrix `δΨ_i = S_ij δE_j`, and a
  bifurcation criterion `det(S) → 0` — none of which appear in
  `Manuscript 002.md`).

**Why this matters:** a reviewer relying on `Specifications/Research
Archive/` for "what the manuscript says" will reach materially different
conclusions than one relying on
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/`. Both subsystems are
currently present and active (neither is marked deprecated or draft-only
relative to the other).

**Not done by this reconciliation pass:** no attempt was made to decide
which representation is "correct," to merge them, to rewrite Manuscript
001/002 to match the DEF layer, or to delete either subsystem. This
conflict is recorded for human review only.

---

## Conflict B — DEF identifier numbering is inconsistent across repository locations

The same handful of concepts carry **different DEF numbers** depending on
which file is consulted. All identifiers below are reported exactly as
found; none were renumbered as part of this reconciliation pass.

| Concept | `01_MASTER_INDEX/MASTER_DEFINITION_INDEX.md` (v0.2.0) | `01_MASTER_INDEX/DEFINITIONS/*.md` (individual files) | `JUFE_ABTM_PROJECT_FOUNDATION/Specification/Definitions/definitions.json` (v0.1.0) |
|---|---|---|---|
| Boundary Jam | DEF-0009 | `DEF-0020_Boundary_Jam.md` | DEF-007 |
| Coupled Differential Feedback / Coupled Field Evolution | DEF-0013 | `DEF-0021_Coupled_Differential_Feedback.md` | — |
| Harmonic (Ejection) Packet | DEF-0018 | `DEF-0022 — Harmonic Packet` (file has no `.md` extension) | DEF-008 |
| Clean Cell Pool | DEF-0020A | `DEF-0023_Clean_Cell_Pool.md` | DEF-009 |
| Absolute Vacuum State | DEF-0019 | `DEF-0019_Absolute_Vacuum_State.md` (numbers agree here) | — |

### Direct same-folder identifier collision

`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/03_REFERENCE_LIBRARY/EVIDENCE/`
contains **two different files both claiming identifier `DEF-0019`** for two
different concepts:

- `EVIDENCE-DEF-0019_Absolute_Vacuum_State.md` — has real content; agrees
  with `MASTER_DEFINITION_INDEX.md`'s numbering (DEF-0019 = Absolute Vacuum
  State).
- `EVIDENCE_DEF-0019_Boundary_Jam.md` — **confirmed empty (0 bytes of
  content)**; its filename differs from the other file only by a hyphen vs.
  underscore immediately after "EVIDENCE". Its implied numbering (DEF-0019 =
  Boundary Jam) matches neither `MASTER_DEFINITION_INDEX.md` (which has
  Boundary Jam at DEF-0009) nor the sibling `DEF-0020_Boundary_Jam.md` file
  (which uses DEF-0020).

### Other overlapping-but-non-colliding ID schemes

These use different prefixes, so they do not collide syntactically with
`DEF-xxxx`, but they describe overlapping concepts and should not be assumed
interchangeable with any `DEF-xxxx` numbering:

- `JUFE_ABTM_PROJECT_FOUNDATION/Specification/Axioms/axioms.json` —
  `AX-001` through `AX-004`.
- `DEPENDENCY_ATLAS/JUFE_Dependency_Atlas_v1.md` — `ENT-`, `FLD-`, `GEO-`,
  `DYN-`, and its own `AX-001`/`AX-005` references.

**Why this matters:** a dependency edge, requirement ID, or future
cross-reference written against "DEF-0020" (for example) means a different
concept depending on which of the three files above is treated as
authoritative. The empty `EVIDENCE_DEF-0019_Boundary_Jam.md` file is also a
silent data-loss risk: anything that was meant to populate it was never
written, and its filename makes it easy to mistake for the populated
`EVIDENCE-DEF-0019_Absolute_Vacuum_State.md` file at a glance.

**Not done by this reconciliation pass:** no identifier was renumbered, no
file was deleted or merged, and no content was moved between these files.
`MASTER_DEFINITION_INDEX.md` explicitly states "Identifiers must not be
renumbered after release" — this document takes that instruction at face
value and defers reconciliation of the conflicting schemes to an explicit,
separately authorized decision.

---

## Conflict C — Duplicate V4 source copy removed (4 October 2026)

Source `36.md` is now preserved whole and unchanged once at
`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/CANONICAL/TFJ-Canonical-Self-Bootstrapping-Monograph-Architecture-V4.md`.
The second template copy was removed. This is duplicate removal, not a
scientific or mathematical classification decision.

## Current original-source location (4 October 2026)

The complete combined manuscript is preserved unchanged at
`Research Processing/Relational Unified Field Mechanics Analytical Resolution of CriticalΓÇª.md`.
References above to Manuscript 001/002 split original-source copies describe
the earlier state: those source copies have been removed. Their separate
analysis documents remain. Conflicts A and B are not resolved by preservation.

---

## Secondary, lower-severity items noticed alongside the above (not acted on)

These were observed during the same reconciliation pass but are outside the
scope of what was authorized to be fixed in this phase. They are recorded
here only so they are not lost:

- `JUFE_NEXT_DEFINITION_STAGE/GRID_64_MAPPING_CONTRACT.md` and
  `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/03_REFERENCE_LIBRARY/GRID_64_MAPPING_CONTRACT.md`
  share a filename but contain materially different content (one still
  "UNRESOLVED CORE MAPPING" with open Option A/B/C choices; the other
  "PROVISIONAL_MAPPING" with the choice already recorded as made).
- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/03_REFERENCE_LIBRARY/RIEMANN_PHASE_CANCELLATION_STATUS.md`
  is an unfilled stub ("Copy your current reference document here.") despite
  `MASTER_DEFINITION_INDEX.md` DEF-0022 already describing this concept's
  manuscript basis.
- ~~Source artifact `4.md` ... is not itself named anywhere in
  `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/README.md`~~ — **Resolved 3
  October 2026**: `4.md` is now named there alongside its duplicate `18.md`
  (see `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/README.md`, "atriΩ...Pt.2",
  and `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/PROVENANCE_MAP.md` row 31).
  This line is left struck through rather than deleted so the record of the
  original gap is not lost.
