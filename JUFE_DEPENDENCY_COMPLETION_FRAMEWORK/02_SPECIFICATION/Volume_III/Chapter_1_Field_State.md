# JUFE Reference Specification

## Volume III — Local Field Mechanics

### Chapter 1 — Field State

**Specification ID:** JUFE-V3-C1  
**Version:** 1.0.0-draft  
**Status:** DRAFT REFERENCE SPECIFICATION
**Scope:** LOCAL  
**Primary source:** *Relational Unified Field Mechanics: Analytical Resolution of Critical Cosmological Anomalies*, §1.1, §2.1, §2.2 and §3  
**Related index entries:** DEF-0001, DEF-0002, DEF-0003, DEF-0014, DEF-0015, DEF-0019, DEF-0023, DEF-0025, DEF-0026

---

## 1.1 Purpose

Normative definitions begin in Section 1.3.

This chapter defines the local field quantities used by the JUFE / ABTM
specification.

It distinguishes between:

- field objects explicitly defined by the manuscript;
- engineering representations introduced for software and mapping purposes;
- unresolved quantities that must not yet be treated as executable physics.

This chapter does not define field evolution, gradient evaluation, phase-lock
dynamics, ejection, or global manifold behaviour. Those are specified in later
chapters.

## 1.12 Authority

This chapter is authoritative for all local field-state definitions used throughout Volume III.

---

## 1.2 Status Discipline

The following labels are authoritative throughout this chapter.

### EXPLICIT

Directly stated or mathematically displayed in the manuscript.

### PROVISIONAL

An engineering representation consistent with the manuscript but not uniquely
derived from it.

### UNRESOLVED

Referenced by the manuscript but not mathematically complete.

No PROVISIONAL or UNRESOLVED definition shall be silently promoted to
reference runtime behaviour.

---

## 1.3 DEF-0001 — Inward Compressive Field

**Status:** EXPLICIT  
**Symbol:** \(\mathbf M\)  
**Type:** Three-component vector  
**Domain:** \(\mathbb R^3_{\mathrm{comp}}\)

### Definition

The manuscript defines the inward compressive field as

$$
\mathbf M \in \mathbb R^3_{\mathrm{comp}}.
$$

Its component representation is

$$
\mathbf M=(M_x,M_y,M_z).
$$

### Role

The compressive field:

- forms the local mass-energy or tension contribution described by the model;
- is evaluated through the spatial gradient;
- participates in local dominance;
- participates in coupled evolution;
- contributes to the global field-balance identity.

### Required properties

A valid compressive field shall:

1. contain exactly three ordered components;
2. preserve the component order \(x,y,z\);
3. contain finite numerical values when used in software;
4. retain its source coordinate and frame identity in audit records.

### Used by

- JUFE-V3-C3 Gradient Mechanics;
- JUFE-V3-C4 Coupled Evolution;
- JUFE-V3-C5 Phase Lock;
- JUFE-V3-C6 Information Preservation;
- future global manifold specifications.

---

## 1.4 DEF-0002 — Outward Repulsive Field

**Status:** EXPLICIT  
**Symbol:** \(\mathbf A\)  
**Type:** Three-component vector  
**Domain:** \(\mathbb R^3_{\mathrm{rep}}\)

### Definition

The manuscript defines the outward repulsive field as

$$
\mathbf A \in \mathbb R^3_{\mathrm{rep}}.
$$

Its component representation is

$$
\mathbf A=(A_x,A_y,A_z).
$$

### Role

The repulsive field:

- forms the complementary local field contribution;
- participates in local dominance comparisons;
- participates in coupled evolution;
- participates in the phase-lock condition;
- contributes to the global field-balance identity.

### Required properties

A valid repulsive field shall:

1. contain exactly three ordered components;
2. preserve the component order \(x,y,z\);
3. contain finite numerical values when used in software;
4. retain its source coordinate and frame identity in audit records.

### Used by

- JUFE-V3-C4 Coupled Evolution;
- JUFE-V3-C5 Phase Lock;
- JUFE-V3-C6 Information Preservation;
- future global manifold specifications.

---

## 1.5 DEF-0003 — Six-Component Local Field State

**Status:** PROVISIONAL  
**Specification symbol:** \(\Psi_{\mathrm{local}}\)  
**Type:** Ordered six-component software state

### Definition

For specification and software purposes, the two manuscript-defined vectors
are combined into the ordered local state

$$
\Psi_{\mathrm{local}}
=
(\mathbf M,\mathbf A)
=
(M_x,M_y,M_z,A_x,A_y,A_z).
$$

### Important limitation

The manuscript explicitly defines \(\mathbf M\) and \(\mathbf A\), but it does
not display the exact equation

$$
\Psi_{\mathrm{local}}=(\mathbf M,\mathbf A).
$$

The six-component local state is therefore an approved engineering
formalisation, not an independently established manuscript equation.

### Canonical order

The canonical component order is

```text
Mx, My, Mz, Ax, Ay, Az
```

Software shall not silently reorder these components.

### Required properties

A valid local field state shall:

1. contain exactly six numerical components;
2. preserve canonical component order;
3. distinguish local state from global manifold state;
4. record its cell coordinate and frame index;
5. record whether the state is ACTIVE, VACUUM, UNDEFINED, or another declared
   lifecycle state;
6. retain its mapping-version identifier.

### Forbidden behaviour

An implementation shall not:

- infer missing components;
- silently substitute zero for missing data;
- treat UNDEFINED as VACUUM;
- silently swap compressive and repulsive components;
- conflate \(\Psi_{\mathrm{local}}\) with the later global manifold variable.

---

## 1.6 DEF-0014 — Phase-Difference Expression

**Status:** EXPLICIT EXPRESSION / PROVISIONAL NAME  
**Specification symbol:** \(\Delta\)  
**Type:** Three-component derived vector

### Definition

The manuscript explicitly uses

$$
\mathbf M(t)-\mathbf A(t)
$$

in the phase-lock limit.

For specification purposes, define

$$
\Delta(t)
=
\mathbf M(t)-\mathbf A(t).
$$

### Important limitation

The expression is explicit. The name **phase residual** and the symbol
\(\Delta\) are specification conventions.

### Component form

$$
\Delta
=
(M_x-A_x,\;M_y-A_y,\;M_z-A_z).
$$

### Role

The phase-difference expression is used to:

- represent local compressive/repulsive mismatch;
- define the target of phase-lock evolution;
- report the distance from the declared equilibrium condition;
- support validation of locking behaviour.

### Unresolved

The manuscript does not specify:

- a preferred norm for reporting the residual;
- a finite numerical lock tolerance;
- whether component-wise equality or another equivalence rule is sufficient in
  all future formulations.

---

## 1.7 DEF-0015 — Local Phase-Equilibrium Condition

**Status:** EXPLICIT  
**Scope:** LOCAL

### Definition

The manuscript states

$$
\lim_{t\to t_{\mathrm{lock}}}
\left(
\mathbf M(t)-\mathbf A(t)
\right)
=
\mathbf 0.
$$

Accordingly, the exact local phase-equilibrium target is

$$
\Delta=\mathbf 0.
$$

Equivalently,

$$
\mathbf M=\mathbf A.
$$

### Interpretation

Local phase equilibrium is not automatically equivalent to a vacuum state.

A cell may have equal non-zero compressive and repulsive vectors while the
phase difference is zero.

### Important limitation

A numerical implementation generally requires a tolerance. The manuscript
does not provide one. Any finite tolerance remains PROVISIONAL and must be
declared in configuration and audit output.

---

## 1.8 DEF-0019 — Absolute Vacuum State

**Status:** EXPLICIT CONCEPT / PROVISIONAL SIX-ZERO REPRESENTATION  
**Symbol:** \(\Psi_0\)

### Definition

The manuscript describes the local coordinate as resetting to an absolute
vacuum state after successful non-truncating ejection.

### Provisional software representation

For the six-component local state, the current software convention is

$$
\Psi_0=(0,0,0,0,0,0).
$$

### Important limitation

The manuscript explicitly names the vacuum reset state, but the six-zero tuple
is an engineering representation.

### Distinction from phase equilibrium

The following states are not interchangeable:

- phase equilibrium:
  $$
  \mathbf M=\mathbf A;
  $$
- vacuum:
  $$
  \mathbf M=\mathbf 0
  \quad\text{and}\quad
  \mathbf A=\mathbf 0.
  $$

A locked non-zero state shall not be silently labelled VACUUM.

---

## 1.9 DEF-0025 — Vacuum Cell

**Status:** PROVISIONAL  
**Scope:** MESO

### Definition

A 64-cell coordinate explicitly containing the approved vacuum representation
and lifecycle state `VACUUM`.

### Required properties

A vacuum cell shall:

1. have all six components explicitly assigned;
2. have lifecycle state `VACUUM`;
3. retain its coordinate and frame identity;
4. record how and when the vacuum state was established.

---

## 1.10 DEF-0026 — Undefined Cell

**Status:** PROVISIONAL  
**Scope:** MESO

### Definition

A coordinate for which no local field state has been supplied or derived.

### Required invariant

An undefined cell shall never be silently treated as a vacuum cell.

### Software representation

The undefined state should use explicit metadata, such as

```text
state = UNDEFINED
components = absent
```

rather than six inferred zeros.

---

## 1.11 Local Field-State Relationships

The approved relationship hierarchy is

```text
M  ─┐
    ├──> Psi_local  (PROVISIONAL engineering representation)
A  ─┘

M and A
   │
   └──> Delta = M - A

Delta = 0
   │
   └──> Local phase-equilibrium target

Successful preservation and ejection
   │
   └──> Psi_0 vacuum reset
```

No arrow in this hierarchy authorises an unspecified dynamic update.

---

## 1.12 Software Contract

A future local-state implementation shall provide, at minimum:

### Inputs

```text
Mx
My
Mz
Ax
Ay
Az
coordinate
frame_index
lifecycle_state
mapping_version
```

### Derived output

```text
M_vector
A_vector
phase_difference
is_exact_phase_equilibrium
is_vacuum
is_defined
```

### Validation failures

The implementation shall reject:

- a component count other than six;
- non-numeric or non-finite components;
- missing component order;
- an undefined state falsely marked as vacuum;
- a vacuum state containing non-zero components;
- a local/global symbol collision that removes scope information.

---

## 1.13 Audit Contract

Every serialized local state shall include:

```text
definition_ids:
  - DEF-0001
  - DEF-0002
  - DEF-0003

component_order:
  - Mx
  - My
  - Mz
  - Ax
  - Ay
  - Az

coordinate:
frame_index:
lifecycle_state:
mapping_version:
source_record:
created_at:
```

Derived values may be included, but shall not replace the original six
components.

---

## 1.14 Dependencies

This chapter depends upon:

- the manuscript definitions of \(\mathbf M\) and \(\mathbf A\);
- the phase-lock expression in manuscript §2.2;
- the 64-cell mapping contract for meso-scale cell representation.

This chapter is referenced by:

- Volume III Chapter 2 — Field Lifecycle;
- Volume III Chapter 3 — Gradient Mechanics;
- Volume III Chapter 4 — Coupled Evolution;
- Volume III Chapter 5 — Phase Lock;
- Volume III Chapter 6 — Information Preservation;
- the Master Definition Index;
- the future Master Dependency Index.

---

## 1.15 Outstanding Questions

The following remain unresolved:

1. Are \(\mathbf M\) and \(\mathbf A\) physical vectors, generalized field
   components, or computational coordinates at every scale?
2. What units apply to each component?
3. Is the local-state combination \((\mathbf M,\mathbf A)\) the unique
   representation?
4. What norm should measure phase difference?
5. What finite tolerance should define numerical phase lock?
6. Is exact component equality required, or may a stronger geometric
   equivalence replace it?
7. How does the two-dimensional 8×8 projection represent the third spatial
   axis?
8. How is the local state embedded into the global manifold variable?
9. Is the six-zero tuple the intended physical vacuum state or only a software
   reset convention?

These questions shall remain visible until resolved by manuscript extension,
approved derivation, or validated engineering decision.

---

## 1.16 Validation Requirements

A conforming implementation shall demonstrate:

- exact six-component storage;
- canonical ordering;
- correct separation of \(\mathbf M\) and \(\mathbf A\);
- correct calculation of \(\Delta=\mathbf M-\mathbf A\);
- distinction between phase equilibrium and vacuum;
- distinction between undefined and vacuum;
- preservation of source values through serialization;
- explicit reporting of all provisional conventions.

---

## 1.17 Completion Status

This chapter is complete as a **draft reference specification** for the current
manuscript and mapping contract.

It is not frozen as final because several physical and numerical definitions
remain unresolved.

**Next chapter:** Volume III Chapter 2 — Field Lifecycle.
