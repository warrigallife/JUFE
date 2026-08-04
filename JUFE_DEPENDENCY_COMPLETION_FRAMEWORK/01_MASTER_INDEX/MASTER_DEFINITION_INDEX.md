# JUFE Master Definition Index

Project: JUFE Universe Project  
Document ID: JUFE-MDI-001  
Version: 0.2.0  
Updated: 2026-07-16  
Status: ACTIVE SPECIFICATION DRAFT

## Purpose

This index assigns stable identifiers to concepts extracted from the current
JUFE / ABTM manuscript and supporting reference documents.

The index does not create new physical claims. Each item is labelled:

- **EXPLICIT** — directly stated or mathematically displayed in the manuscript.
- **PROVISIONAL** — an engineering formalisation consistent with the manuscript,
  but not uniquely derived from it.
- **UNRESOLVED** — referenced by the manuscript but not yet mathematically defined.
- **MODEL CLAIM** — an interpretive claim made by the manuscript that requires
  independent external validation before being treated as established physics.

Identifiers must not be renumbered after release.

---

# A. Local field objects

## DEF-0001 — Inward Compressive Field

**Status:** EXPLICIT  
**Symbol:** `M`  
**Scope:** LOCAL  
**Source:** Manuscript §1.1

**Definition**

A three-component inward compressive field:

\[
\mathbf M \in \mathbb R^3_{\mathrm{comp}}.
\]

**Components**

\[
\mathbf M=(M_x,M_y,M_z).
\]

**Used by**

- DEF-0004 Compressive Field Gradient
- DEF-0007 Local Gradient Dominance
- DEF-0013 Coupled Field Evolution
- DEF-0015 Phase-Lock Condition
- DEF-0021 Global Field-Balance Identity

---

## DEF-0002 — Outward Repulsive Field

**Status:** EXPLICIT  
**Symbol:** `A`  
**Scope:** LOCAL  
**Source:** Manuscript §1.1

**Definition**

A three-component outward repulsive field:

\[
\mathbf A \in \mathbb R^3_{\mathrm{rep}}.
\]

**Components**

\[
\mathbf A=(A_x,A_y,A_z).
\]

**Used by**

- DEF-0007 Local Gradient Dominance
- DEF-0013 Coupled Field Evolution
- DEF-0015 Phase-Lock Condition
- DEF-0021 Global Field-Balance Identity

---

## DEF-0003 — Six-Component Local Field State

**Status:** PROVISIONAL  
**Symbol:** `Psi_local`  
**Scope:** LOCAL  
**Source:** Engineering formalisation of DEF-0001 and DEF-0002; 64-cell mapping contract

**Definition**

The ordered local software state:

\[
\Psi_{\mathrm{local}}
=
(M_x,M_y,M_z,A_x,A_y,A_z).
\]

**Important limitation**

The manuscript explicitly defines `M` and `A`, but the exact equality
`Psi = (M,A)` is an engineering representation rather than a displayed
manuscript equation.

**Used by**

- 64-cell field mapping
- Local lifecycle specification
- Future runtime data model

---

## DEF-0004 — Compressive Field Gradient

**Status:** EXPLICIT  
**Symbol:** `nabla M`  
**Scope:** LOCAL  
**Source:** Manuscript §1.1

**Definition**

\[
\nabla \mathbf M
=
\left(
\frac{\partial M_x}{\partial x},
\frac{\partial M_y}{\partial y},
\frac{\partial M_z}{\partial z}
\right).
\]

**Purpose**

Provides the directional tension field used by gradient autonomy.

**Unresolved**

- boundary conditions;
- discrete derivative rule for the 64-cell projection;
- third-axis representation.

---

## DEF-0005 — Propagation Vector

**Status:** EXPLICIT  
**Symbol:** `D`  
**Scope:** LOCAL  
**Source:** Manuscript §1.1–1.2

**Definition**

\[
\vec{\mathbf D} \propto -\nabla \mathbf M
\]

and, in the local Earth-field example,

\[
\vec{\mathbf D}_{\mathrm{particle}}
=
-k\nabla\mathbf M_{\mathrm{Earth}}.
\]

**Unresolved**

- units and numerical meaning of `k`;
- whether `k` varies with location, scale, or time;
- whether `D` encodes direction only or complete velocity.

---

## DEF-0006 — Gradient Autonomy

**Status:** EXPLICIT  
**Category:** AXIOM  
**Scope:** LOCAL  
**Source:** Axiom II, Manuscript §1.1–1.2

**Definition**

Instantaneous propagation is governed by the maximum local tension gradient,
not by a hard-coded trajectory conditional on intrinsic particle identity.

**Used by**

- DEF-0005 Propagation Vector
- DEF-0007 Local Gradient Dominance
- DEF-0010 Jammed-Node Bypass

---

## DEF-0007 — Local Gradient Dominance

**Status:** PARTIALLY EXPLICIT / UNRESOLVED THRESHOLD  
**Scope:** LOCAL  
**Source:** Manuscript §1.2

**Displayed condition**

\[
\|\mathbf M_{\mathrm{Earth}}\|
\gg
\|\mathbf A_{\mathrm{particle}}\|.
\]

**Definition**

The surrounding compressive field is dominant when it governs the local
propagation vector of the embedded field manifestation.

**Unresolved**

The manuscript does not provide a numerical definition of `much greater than`.

---

# B. Boundary and isolation mechanics

## DEF-0008 — Macro-Scale Tier Boundary

**Status:** EXPLICIT TERM / UNRESOLVED GEOMETRY  
**Scope:** LOCAL–MESO  
**Primary source:** Manuscript §2.1  
**Used by:** DEF-0009 Boundary Jam; Volume III Chapters 2 and 4

### Definition

The manuscript places the boundary-jam process at a macro-scale tier boundary
\(n\) associated with massive gravitational collapse.

### Explicit manuscript content

- a macro-scale tier boundary exists;
- field cells at the boundary reach maximum tension capability;
- the boundary is involved in the transition to a jammed state.

### Unresolved

- geometric representation of the boundary;
- meaning and domain of tier index \(n\);
- relationship to the 8×8 field projection;
- boundary topology and neighbour rules;
- numerical method for detecting the boundary.

### Execution gate

No runtime geometry shall be treated as authoritative until these items are
resolved or explicitly adopted as PROVISIONAL configuration.

---

## DEF-0009 — Boundary Jam

**Status:** EXPLICIT  
**Symbol:** \(C_{\mathrm{jam}}\)  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.1  
**Depends on:** DEF-0004 Compressive Field Gradient; DEF-0006 Gradient Autonomy; DEF-0008 Macro-Scale Tier Boundary  
**Used by:** DEF-0010, DEF-0011, DEF-0013; Volume III Chapters 2 and 4

### Definition

A boundary jam is the state reached when a field cell at the macro-scale tier
boundary has reached maximum tension capability while adjacent external
regions present the limiting resistance condition described by

\[
\nabla\mathbf M\to\infty.
\]

### Explicit manuscript behaviour

- ordinary traffic does not continue through the jammed node;
- active field traffic bypasses the node under Axiom II;
- the jammed cell isolates into a closed renormalization manifold.

### Unresolved

- finite resistance threshold;
- tension-capacity function;
- measurement units;
- whether the limit is scalar, component-wise, or norm-based;
- numerical detection and hysteresis rules.

---

## DEF-0010 — Jammed-Node Bypass

**Status:** EXPLICIT BEHAVIOUR / UNRESOLVED ALGORITHM  
**Scope:** MESO  
**Primary source:** Manuscript §2.1  
**Depends on:** DEF-0006 Gradient Autonomy; DEF-0009 Boundary Jam  
**Used by:** Volume III Chapters 2 and 4

### Definition

When a boundary node is jammed, active field traffic bypasses that node in
accordance with Gradient Autonomy.

### Explicit manuscript content

The bypass behaviour is stated, but no routing algorithm is supplied.

### Unresolved

- neighbour topology;
- destination selection;
- route-search procedure;
- conservation accounting during bypass;
- whether bypass is instantaneous or time-evolved;
- treatment of multiple adjacent jammed nodes.

### Execution gate

A routing algorithm may be implemented only as a labelled PROVISIONAL model.

---

## DEF-0011 — Closed Renormalization Manifold

**Status:** EXPLICIT TERM / UNRESOLVED MATHEMATICAL DOMAIN  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.1  
**Depends on:** DEF-0009 Boundary Jam  
**Used by:** DEF-0013 Coupled Field Evolution; Volume III Chapters 2 and 4

### Definition

The isolated domain entered by \(C_{\mathrm{jam}}\) after ordinary traffic
bypasses the node.

### Explicit manuscript behaviour

- the jammed cell isolates;
- its internal compressive and repulsive fields continue in a coupled
  differential feedback loop;
- the isolation precedes phase lock.

### Unresolved

- state-space and boundary definition;
- closure condition;
- coordinate transformation, if any;
- relationship to the external manifold;
- whether renormalization changes scale, units, or representation.

---

## DEF-0012 — Absolute Conservation of Field Duality

**Status:** EXPLICIT AXIOM  
**Category:** AXIOM I  
**Scope:** LOCAL–GLOBAL  
**Primary source:** Manuscript §2.1 and §3  
**Used by:** DEF-0013 Coupled Field Evolution; DEF-0021 Global Field-Balance Identity

### Definition

The framework requires compressive and repulsive field contributions to remain
subject to the manuscript's declared zero-balance condition.

### Explicit local consequence

Within the isolated cell:

\[
\frac{d\mathbf M}{dt}
=
-\frac{d\mathbf A}{dt}.
\]

### Explicit global consequence

The manuscript states the global field-balance identity recorded in DEF-0021.

### Unresolved

- whether conservation is scalar, vector, tensorial, or multi-level;
- measure and domain of the global sum;
- relationship between local derivative balance and global balance;
- numerical conservation tolerance.

---

## DEF-0013 — Coupled Field Evolution

**Status:** EXPLICIT EQUATION / PARTIALLY DEFINED DYNAMICS  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.1  
**Depends on:** DEF-0001 Inward Compressive Field; DEF-0002 Outward Repulsive Field; DEF-0011 Closed Renormalization Manifold; DEF-0012 Absolute Conservation of Field Duality  
**Used by:** DEF-0014 Phase Residual; DEF-0015 Phase-Lock Condition; Volume III Chapters 2, 4, and 5

### Definition

During isolation, the internal fields obey

\[
\frac{d\mathbf M}{dt}
=
-\frac{d\mathbf A}{dt}.
\]

### Explicit manuscript interpretation

The compressive and repulsive fields participate in a coupled differential
feedback loop while the cell remains isolated.

### What the equation guarantees directly

For any differentiable evolution satisfying the equation,

\[
\frac{d}{dt}(\mathbf M+\mathbf A)=\mathbf 0.
\]

Therefore, \(\mathbf M+\mathbf A\) is constant over the coupled evolution
interval, subject to the assumptions of ordinary differentiation.

### Important limitation

The manuscript also states that the difference \(\mathbf M-\mathbf A\)
approaches zero through cross-axial helical deflection. The differential
equation alone does not specify that convergence mechanism.

### Unresolved

- explicit right-hand-side evolution function;
- integration scheme and timestep;
- time units;
- initial and boundary conditions;
- convergence proof;
- role of Lemma 3.1 in producing phase convergence.

---

# C. Phase-lock and ejection mechanics

## DEF-0014 — Phase Residual

**Status:** PROVISIONAL NAME / EXPLICIT EXPRESSION  
**Symbol:** \(\Delta\)  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.2  
**Depends on:** DEF-0001; DEF-0002; DEF-0013  
**Used by:** DEF-0015; DEF-0016; Volume III Chapters 4 and 5

### Definition

The manuscript explicitly uses the vector difference

\[
\mathbf M(t)-\mathbf A(t).
\]

The specification assigns the provisional shorthand

\[
\Delta(t)=\mathbf M(t)-\mathbf A(t).
\]

### Important limitation

The expression is explicit. The symbol \(\Delta\) and the name “phase
residual” are engineering conventions.

### Unresolved

- preferred norm;
- units;
- whether component-wise residual is sufficient;
- numerical reporting and tolerance rules.

---

## DEF-0015 — Phase-Lock Condition

**Status:** EXPLICIT  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.2  
**Depends on:** DEF-0013 Coupled Field Evolution; DEF-0014 Phase Residual; DEF-0016 Cross-Axial Helical Deflection  
**Used by:** DEF-0017, DEF-0018, DEF-0020; Volume III Chapters 2, 5, and 6

### Definition

The manuscript defines the phase-lock target as

\[
\lim_{t\to t_{\mathrm{lock}}}
\left(
\mathbf M(t)-\mathbf A(t)
\right)
=
\mathbf 0.
\]

Using the provisional residual notation:

\[
\lim_{t\to t_{\mathrm{lock}}}\Delta(t)=\mathbf 0.
\]

### Explicit manuscript consequence

At \(t_{\mathrm{lock}}\), the cell reaches internal equilibrium and becomes
eligible for the ejection process.

### Important distinction

Phase lock does not by itself imply that every component is zero. It expresses
equality of \(\mathbf M\) and \(\mathbf A\), whereas vacuum reset is a later,
distinct event.

### Unresolved

- finite lock tolerance;
- persistence duration required before lock is accepted;
- uniqueness and existence of \(t_{\mathrm{lock}}\);
- numerical proof of convergence;
- whether exact equality is physically intended.

---

## DEF-0016 — Cross-Axial Helical Deflection

**Status:** REFERENCED / UNRESOLVED OPERATOR / PROVISIONAL INTERFACE  
**Symbol:** \(\mathcal H\) (provisional)  
**Scope:** LOCAL  
**Primary source:** Lemma 3.1 reference in Manuscript §2.2  
**Depends on:** DEF-0014 Phase Residual  
**Used by:** DEF-0015 Phase-Lock Condition; Volume III Chapters 4 and 5

### Manuscript role

The manuscript states that cross-axial helical deflection bleeds asymmetric
force into orthogonal phase dimensions while the fields move toward internal
equilibrium.

### Provisional interface only

\[
\mathcal H:\Delta\mapsto\Delta'
\]

may be used as an interface placeholder, but no physical transformation is
authorised by that notation.

### Unresolved

- exact operator;
- domain and codomain;
- orthogonal phase subspace;
- helical angle, handedness, and phase parameter;
- conserved scalar, norm, tensor, or topology;
- continuous or discrete law;
- connection to the 64-cell frame.

### Execution gate

Not executable as reference physics.

---

## DEF-0017 — Stabilized Structural Matrix

**Status:** EXPLICIT TERM / UNRESOLVED REPRESENTATION  
**Symbol:** \(\Sigma\) (provisional)  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.2  
**Depends on:** DEF-0015 Phase-Lock Condition  
**Used by:** DEF-0018 Harmonic Ejection Packet; DEF-0020 Non-Truncating Ejection Map; Volume III Chapter 6

### Definition

The structural state of the cell after phase lock and before ejection.

### Explicit manuscript content

- the matrix is stabilized;
- its geometric information cannot be clipped or truncated;
- it is ejected from the boundary node.

### Unresolved

- complete mathematical contents;
- data type and dimensions;
- equivalence criterion;
- relationship to the six-component local state;
- relationship to the 64-cell frame;
- whether it includes lifecycle and provenance metadata.

---

## DEF-0018 — Harmonic Ejection Packet

**Status:** EXPLICIT NAME / UNRESOLVED PHYSICAL STRUCTURE / PROVISIONAL SOFTWARE PACKET  
**Symbol:** \(\mathbf\Phi_{\mathrm{ejected}}\)  
**Scope:** LOCAL–MESO  
**Primary source:** Manuscript §2.2  
**Depends on:** DEF-0015; DEF-0017; DEF-0020  
**Used by:** Volume III Chapter 6

### Definition

The manuscript's un-truncated structural information distributed from the
phase-locked boundary node into the network.

### Explicit manuscript content

- it is harmonic;
- it carries the underlying structural information;
- it is distributed to the network;
- its ejection accompanies local vacuum reset.

### Unresolved

- packet schema;
- harmonic variables;
- physical observable;
- transport speed and path;
- destination address;
- interaction with the clean cell pool;
- reinsertion or recycling rule.

---

## DEF-0019 — Absolute Vacuum State

**Status:** EXPLICIT CONCEPT / PROVISIONAL SIX-ZERO REPRESENTATION  
**Symbol:** \(\Psi_0\)  
**Scope:** LOCAL  
**Primary source:** Manuscript §2.2  
**Depends on:** DEF-0020 Non-Truncating Ejection Map  
**Used by:** Volume III Chapters 1, 2, and 6

### Definition

The reset state of the localized boundary coordinate after successful
non-truncating ejection.

### Provisional software convention

For the six-component local representation:

\[
\Psi_0=(0,0,0,0,0,0).
\]

### Important limitation

The manuscript identifies the reset as an absolute vacuum state \(0\), but it
does not explicitly define the six-zero software tuple.

### Invariant

Reset shall not occur before preservation verification succeeds.

---

## DEF-0020 — Non-Truncating Ejection Map

**Status:** PROVISIONAL FORMALISATION OF EXPLICIT PROCESS  
**Symbol:** \(\mathcal E\)  
**Scope:** LOCAL–MESO  
**Primary source:** Manuscript §2.2 and Theorem 4.2 reference  
**Depends on:** DEF-0015, DEF-0017, DEF-0018, DEF-0019  
**Used by:** Volume III Chapters 2 and 6

### Formal interface

\[
\mathcal E(\Sigma)
=
(\Psi_0,\mathbf\Phi_{\mathrm{ejected}}).
\]

### Manuscript-aligned sequence

1. phase lock is reached;
2. the stabilized structural matrix is retained;
3. structural information is ejected rather than truncated;
4. the local boundary coordinate resets to \(\Psi_0\).

### Minimum digital preservation contract

A future software implementation shall:

1. serialize the complete pre-reset state;
2. create an immutable packet copy;
3. compute a content hash;
4. verify equivalence before reset;
5. abort reset if verification fails;
6. log destination and provenance.

A byte-level minimum is

\[
\operatorname{Hash}(\Sigma_{\mathrm{before}})
=
\operatorname{Hash}(\mathbf\Phi_{\mathrm{ejected}}).
\]

### Important limitation

Digital hash equality tests software preservation only. It does not prove the
manuscript's physical information claim.

---

## DEF-0020A — Clean Cell Pool

**Status:** EXPLICIT NAME / UNRESOLVED MECHANICS  
**Scope:** MESO–GLOBAL  
**Primary source:** Manuscript §2.2  
**Depends on:** DEF-0018 Harmonic Ejection Packet  
**Used by:** Volume III Chapter 6

### Definition

The manuscript-named destination domain into which the harmonic packet is
ejected.

### Explicit manuscript content

Only the destination name and receiving role are given.

### Unresolved

- membership rule;
- topology;
- capacity;
- clean-cell eligibility;
- packet allocation;
- reinsertion;
- collision and ordering rules;
- relationship to vacuum cells and the 64-cell projection.

### Identifier note

The suffix `A` preserves all existing permanent numerical identifiers without
renumbering them. Future revisions may assign a registry alias, but existing
IDs shall remain stable.

---

# D. Global balance and unresolved cancellation

## DEF-0021 — Global Field-Balance Identity

**Status:** EXPLICIT  
**Scope:** GLOBAL  
**Primary source:** Manuscript §3  
**Depends on:** DEF-0001; DEF-0002; DEF-0012  
**Used by:** future global manifold specification; Volume III Chapter 6 as a cross-scope constraint

### Definition

\[
\sum_{\mathrm{Global}}
\left(
\sum_{i\in\{x,y,z\}}
(M_i+A_i)
\right)
\equiv 0.
\]

### Explicit manuscript role

The identity bounds the collective framework and states that local compressive
events are balanced against global outward repulsive space.

### Important limitation

The manuscript states the identity as part of the model. Its empirical
validity and relationship to established physical conservation laws require
independent validation.

### Unresolved

- domain and measure of the global sum;
- scalar versus component-wise balance;
- convergence for an unbounded domain;
- units and normalization;
- relationship to the divergence-free total stress tensor;
- relationship to the 64-cell computational frame.

---

## DEF-0022 — Riemann-Zeta Phase Cancellation

**Status:** REFERENCED / UNRESOLVED  
**Scope:** LOCAL–GLOBAL  
**Primary source:** Manuscript §3  
**Used by:** future global manifold and research specifications

### Current placeholder

\[
\zeta(Z(\Psi))=0.
\]

### Explicit manuscript content

The manuscript states that a local compressive spike may resolve through phase
cancellation at a Riemann-Zeta zero.

### Unresolved

- which zeta function;
- trivial or nontrivial zeros;
- state-to-complex map \(Z\);
- cancelled quantity;
- local or global scope;
- field update;
- conservation law;
- relationship to Z6.

### Execution gate

Candidate-zero testing may be performed as research instrumentation, but no
field update is authorised.


# E. 64-cell and ABTM structures

## DEF-0023 — Six-Component Field Cell

**Status:** PROVISIONAL APPROVED FOUNDATION  
**Scope:** MESO  
**Source:** 64-cell mapping contract

**Definition**

\[
\Psi_{r,c}
=
(M_x,M_y,M_z,A_x,A_y,A_z).
\]

---

## DEF-0024 — 64-Cell Field Frame

**Status:** PROVISIONAL APPROVED FOUNDATION  
**Scope:** MESO  
**Source:** 64-cell mapping contract

**Definition**

An `8 x 8` coordinate projection containing 64 six-component cells.

**Complete input size**

\[
64\times 6=384
\]

field values.

**Unresolved**

- canonical topology;
- third axis;
- boundary conditions;
- derivation from coordinate-free `M^6`.

---

## DEF-0025 — Vacuum Cell

**Status:** PROVISIONAL  
**Scope:** MESO  
**Source:** 64-cell mapping contract

**Definition**

A cell explicitly assigned all six zero components and lifecycle state
`VACUUM`.

---

## DEF-0026 — Undefined Cell

**Status:** PROVISIONAL  
**Scope:** MESO  
**Source:** 64-cell mapping contract

**Definition**

A coordinate for which no field state was supplied.

**Invariant**

An undefined cell must never be silently treated as a vacuum cell.

---

## DEF-0027 — Original Z6 Trace Diagnostic

**Status:** EXPLICIT IN ORIGINAL CODE / UNRESOLVED DERIVATION  
**Scope:** DIAGNOSTIC  
**Source:** Original JUFE runtime and mapping contract

**Definition**

The original stability diagnostic based on matrix trace modulo six.

**Important limitation**

No derivation from the six-component 64-cell field frame is currently assumed.

---

## DEF-0028 — Dynamic Mod-7 Harmonic

**Status:** EXPLICIT IN UNIFIED ABTM EQUATIONS / UNRESOLVED MECHANICS  
**Scope:** GLOBAL–TEMPORAL  
**Source:** Unified ABTM Field Equations §1

**Definition**

A dynamic seven-fold temporal harmonic coupled to the static Z6 structural
lattice.

**Unresolved**

- mathematical phase variable;
- update law;
- timescale;
- empirical mapping;
- coupling to the local field state.

---

# F. Global ABTM manifold equations

## DEF-0029 — Global Manifold State

**Status:** EXPLICIT TERM / UNRESOLVED TYPE  
**Symbol:** `Psi_global`  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §1

**Definition**

The global state formed by coupling the static Z6 structural lattice and the
dynamic mod-7 temporal harmonic.

**Important distinction**

`Psi_global` must not be silently conflated with provisional local state
`Psi_local`.

---

## DEF-0030 — Total Tensegrity-Stress Tensor

**Status:** EXPLICIT SYMBOL / PARTIALLY DEFINED  
**Symbol:** `T_total^(mu nu)`  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §1–2

**Equilibrium condition**

\[
\nabla_\mu
\mathcal T_{\mathrm{total}}^{\mu\nu}
=
0.
\]

**Unresolved**

- tensor domain;
- units;
- metric signature;
- complete term definitions;
- boundary conditions.

---

## DEF-0031 — Geometric/Curvature Tensor Contribution

**Status:** EXPLICIT TERM / UNRESOLVED COMPONENTS  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §2

**Displayed contribution**

\[
\Phi
\left(
\nabla^\mu\Psi\nabla^\nu\Psi
-
\frac12 g^{\mu\nu}\mathcal H_\mathcal M
\right).
\]

**Unresolved**

- `Phi`;
- `H_M`;
- field type of `Psi`;
- metric and units.

---

## DEF-0032 — Z6 Structural Constraint Tensor

**Status:** EXPLICIT TERM / UNRESOLVED CONSTRUCTION  
**Symbol:** `Z6^(mu nu)`  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §2

**Displayed contribution**

\[
\kappa\,\mathbb Z_6^{\mu\nu}.
\]

**Unresolved**

- tensor construction;
- coupling `kappa`;
- connection to trace-mod-6 runtime diagnostic.

---

## DEF-0033 — Toroidal Flux/Work Contribution

**Status:** EXPLICIT TERM / UNRESOLVED OPERATOR  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §2

**Displayed contribution**

\[
\oint_\mathcal T
\Xi(\Omega_T,\mathcal G)\,d\Sigma.
\]

**Unresolved**

- integration domain;
- integrand;
- orientation;
- units;
- definition of `Omega_T` and `G`.

---

## DEF-0034 — Harmonic Modulation Contribution

**Status:** EXPLICIT TERM / UNRESOLVED FUNCTION  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §2

**Displayed contribution**

\[
\sum_{k\in\{6,7\}}
\Gamma_k(\Psi_{\mathrm{ext}}).
\]

**Unresolved**

- `Gamma_k`;
- external-state type;
- units;
- interaction with Z6 and mod-7 layers.

---

## DEF-0035 — Sensitivity Response

**Status:** EXPLICIT EQUATION / UNRESOLVED DATA CONTRACT  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §3

**Definition**

\[
\delta\Psi_i
=
\mathbf S_{ij}\,\delta\mathcal E_j.
\]

**Unresolved**

- dimensions and units;
- provenance of `S`;
- components of `delta E`;
- calibration and validation.

---

## DEF-0036 — Bifurcation Criterion

**Status:** EXPLICIT LIMIT / UNRESOLVED THRESHOLD  
**Scope:** GLOBAL  
**Source:** Unified ABTM Field Equations §3

**Definition**

\[
\det(\mathbf S)\to 0.
\]

**Meaning in manuscript**

Signals transition into a nonlinear catastrophic regime.

**Unresolved**

- finite numerical threshold;
- conditioning criterion;
- physical interpretation;
- validation data.

---

# G. Governance

## GOV-0001 — CTTM Accord

**Status:** EXPLICIT GOVERNANCE DOCUMENT  
**Scope:** PROJECT GOVERNANCE  
**Source:** CTTM Accord

**Purpose**

States the intended open-stewardship, non-harm, non-exploitation, and
non-extractive-use principles of the project.

**Important limitation**

This is a governance and mission statement, not a mathematical axiom or
software validation rule.

---

# Current index status

Total entries: 38 (including DEF-0020A, added without renumbering existing IDs)

- Local field and mechanics: DEF-0001 to DEF-0022, including DEF-0020A
- 64-cell and ABTM structures: DEF-0023 to DEF-0028
- Global ABTM equations: DEF-0029 to DEF-0036
- Governance: GOV-0001

## Next controlled update

1. Add exact chapter cross-references.
2. Add requirement IDs.
3. Add dependency edges to the Master Dependency Index.
4. Reconcile terminology across Volume III and the reference library.
5. Never promote UNRESOLVED entries without a source or approved derivation.
