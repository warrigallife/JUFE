# JUFE / ABTM Project Continuity Record

Updated: 2026-07-15T15:05:44

## Project purpose

Develop a formal computational framework from:

**Relational Unified Field Mechanics: Analytical Resolution of Critical Cosmological Anomalies**

Author: Thomas F. Jennings  
Project: JUFE Universe Project  
Supplement date: July 7, 2026

## Non-negotiable rules

1. Do not alter the original JUFE source files without explicit approval.
2. Preserve the distinction between:
   - manuscript statements;
   - formal specification;
   - provisional engineering choices;
   - unresolved mathematics;
   - experimental research tools;
   - verified runtime software.
3. Never silently invent missing mathematics.
4. Every core implementation should cite the specification ID it implements.
5. Preserve source values, ordering, mappings, overflow, and audit history.
6. Experimental tools must remain outside the verified runtime until tested and approved.

## Project layers

### 1. Manuscripts
Original scientific and theoretical source material.

### 2. Specification
Contains:
- Master Specification;
- Requirements Register;
- Dependency Atlas;
- Definitions;
- Axioms;
- Theorems;
- State Machines;
- Mapping Contracts;
- Open Questions.

### 3. Research
Contains:
- six-component cell analyser;
- 64-grid mapper;
- arrangement engines;
- residue search;
- experimental topology and transformation tools;
- datasets and audits.

### 4. Verified runtime
Contains stable working software only:
- oldmate1(5).py;
- oldmate2(4).py;
- abtm_expansion.py;
- original launcher;
- optimised master flow;
- required runtime modules.

## Current formal cell mapping

Provisional approved foundation:

\[
\Psi_{r,c}=(M_x,M_y,M_z,A_x,A_y,A_z)
\]

- 1 cell = 6 field values;
- 64 cells = one 8 × 8 frame;
- 384 values = one fully populated frame;
- partial cells must be reported;
- UNDEFINED and VACUUM must remain distinct;
- overflow creates additional frames;
- no silent rearrangement.

## Current state machine

```text
ACTIVE
→ GRADIENT_DRIVEN
→ JAMMED
→ ISOLATED
→ LOCKING
→ LOCKED
→ EJECTED
→ VACUUM
→ REUSED
→ ACTIVE
```

## Current critical dependencies

### Lemma 3.1 — Cross-Axial Helical Deflection

Current status: **PROVISIONAL / NOT YET EXECUTABLE**

Known:
- acts during isolated-cell M/A evolution;
- uses phase asymmetry:
  \[
  \Delta(t)=M(t)-A(t)
  \]
- redistributes asymmetric force into orthogonal phase dimensions;
- must preserve a declared invariant.

Still required:
- exact operator \(\mathcal H\);
- helical parameter or angle;
- exact orthogonal phase-space definition;
- conserved quantity;
- continuous or discrete update law;
- relationship to the 64-cell frame.

### Theorem 4.2 — Information Cannot Be Clipped or Truncated

Current status: **PROVISIONAL SOFTWARE PRESERVATION CONTRACT**

Known:
- phase-locked structural state is preserved in an ejected packet;
- the local cell resets only after preservation succeeds;
- software minimum:
  \[
  \operatorname{Hash}(\Sigma_{before})
  =
  \operatorname{Hash}(\Phi_{ejected})
  \]

Still required:
- physical definition of geometric information;
- equivalence beyond byte identity;
- local/global information relationship;
- clean-cell pool topology;
- reinsertion rule;
- physical observable represented by the packet.

### Riemann-Zeta Phase Cancellation

Current status: **REFERENCED / NOT DERIVED**

Placeholder:
\[
\zeta(Z(\Psi))=0
\]

Still required:
- exact zeta function;
- trivial or nontrivial zero family;
- map \(Z\);
- cancellation target;
- local/global scope;
- M/A update rule;
- conservation rule;
- relationship to Z6.

## Current open topology questions

- FOUR_NEIGHBOUR;
- EIGHT_NEIGHBOUR;
- TOROIDAL_FOUR_NEIGHBOUR;
- TOROIDAL_EIGHT_NEIGHBOUR;
- third spatial-axis encoding;
- boundary conditions;
- relationship between coordinate-free 3D mechanics and the 8 × 8 representation.

## Existing validated arithmetic workflow

Known balanced reference sequence:

```text
1,4,1,40 1,50,4 5,400,5
7,1,90,4,5,50 60,6 5,4,5,50
```

Current implemented arithmetic findings:

- Set 1 total = 511; mod 7 = 0;
- Set 2 total = 287; mod 7 = 0;
- combined total = 798; mod 6 = 0;
- difference = 224; mod 7 = 0;
- arrangement search selects subgroup totals 410 and 64;
- trace = 474; trace mod 6 = 0;
- original engine stable = True.

This arithmetic workflow is a diagnostic/research layer. It is not yet derived from the full 64-cell \(M^6\) field.

## Exact next task

Deepen the specification in this order:

1. Define the mathematical form of the helical operator \(\mathcal H\).
2. Define the preserved invariant under \(\mathcal H\).
3. Define the orthogonal phase dimensions.
4. Define whether the operation acts on \(M\), \(A\), \(\Delta\), or \(\Psi\).
5. Define a testable update rule.
6. Define the clean-cell packet destination and reinsertion rule.
7. Define the Riemann-Zeta state map \(Z(\Psi)\).
8. Choose and document the 64-cell neighbour topology.
9. Update:
   - Master Specification;
   - Requirements Register;
   - Dependency Atlas;
   - validation tests.
10. Only then promote the transformation into executable reference code.

## Resume instruction for a future session

Use this continuity record as the starting context.

The next response should:
- confirm the current specification status;
- avoid modifying original runtime files;
- continue with the next unresolved formal definition;
- separate explicit manuscript content from proposed formalization;
- produce versioned files and an audit/change record.
