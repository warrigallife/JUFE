# Chapter 3 — Gradient Mechanics

Document ID: JUFE-V3-CH03
Title: Gradient Mechanics
Volume: III – Reference Specification
Status: DRAFT
Authority: Relational Unified Field Mechanics: Analytical Resolution of Critical Cosmological Anomalies (Thomas F. Jennings)
Specification Layer: Reference Specification
Implementation Dependency: Chapter 1, Chapter 2

## 3.1 Purpose

This chapter specifies the canonical gradient mechanics governing local field evolution within the JUFE framework.
It formalizes the mathematical definition of the compressive gradient field, the propagation vector, and the principle of Gradient Autonomy as presented in Sections 1.1 and 1.2 of the manuscript.
This chapter specifies the mathematical relationships that govern local propagation. It does not prescribe implementation algorithms.

## 3.2 Scope

This chapter applies exclusively to local gradient mechanics.
It specifies:

- Inward Compressive Field
- Gradient Field
- Propagation Vector
- Gradient Autonomy
- Local Gradient Dominance
- Local Propagation
This chapter does not specify:
- Global equilibrium
- Boundary Jam formation
- Coupled evolution
- Phase Lock
- Runtime discretisation
- Numerical solvers
Those subjects are defined elsewhere.

## 3.3 Authority

This chapter is derived directly from:
Manuscript Section 1.1 — Mathematical Formulation of the Gradient Field
Manuscript Section 1.2 — Mechanical Resolution
Axiom II — Gradient Autonomy
No additional physical mechanisms are introduced.
Where the manuscript is silent, the specification records the uncertainty explicitly rather than inventing behaviour.

## 3.4 Status Discipline

Each statement shall be classified according to the following specification rules.

- **EXPLICIT** — Directly stated by the manuscript.
- **DERIVED** — Immediate mathematical consequence of explicit manuscript equations.
- **PROVISIONAL** — Engineering wording introduced solely for specification clarity.
- **UNRESOLVED** — Behaviour not sufficiently defined by the manuscript.

No implementation shall interpret a PROVISIONAL statement as an explicit manuscript requirement.

## 3.5 Inward Compressive Field

### Definition

The manuscript defines the Inward Compressive Field as the compressive component of the six-dimensional field architecture.
It is represented as
M ∈ ℝ³comp
**Status:** EXPLICIT

### Purpose

The Inward Compressive Field defines the local compressive contribution from which spatial gradients are calculated.
**Status:** DERIVED

### Properties

The manuscript identifies the field as:
continuous;
spatially distributed;
locally differentiable for gradient evaluation.
No additional properties are introduced.
**Status:** EXPLICIT

## 3.6 Gradient Field

### Definition

The spatial gradient of the compressive field is defined by
∇M = (∂Mx/∂x, ∂My/∂y, ∂Mz/∂z)
This operator produces the local tension gradient governing propagation.
**Status:** EXPLICIT

### Purpose

The gradient field determines the direction of maximum local compressive change.
Propagation depends upon this field rather than intrinsic particle characteristics.
**Status:** EXPLICIT

### Behaviour

The gradient field is evaluated within the shared three-dimensional spatial footprint.
The manuscript specifies no preferred coordinate system.
**Status:** EXPLICIT

### Engineering Interpretation

Implementations may employ any numerical representation that preserves the mathematical meaning of the gradient operator.
No specific discretisation method is prescribed.
**Status:** PROVISIONAL

## 3.7 Gradient Autonomy

### Definition

Axiom II specifies that propagation is governed exclusively by the local field gradient.
The propagation vector satisfies
D ∝ −∇M
**Status:** EXPLICIT

### Purpose

Gradient Autonomy removes dependence upon intrinsic particle trajectories.
Propagation is determined solely by the surrounding field geometry.
**Status:** EXPLICIT

### Behaviour

Under Gradient Autonomy:
propagation follows the local gradient;
intrinsic particle properties do not define trajectory;
local field structure determines direction of motion.
**Status:** EXPLICIT

### Engineering Constraint

No implementation shall introduce particle-specific trajectory rules that override the local gradient.
**Status:** DERIVED

## 3.8 Local Gradient Dominance

### Definition

The manuscript defines Local Gradient Dominance by the condition
‖M_Earth‖ ≫ ‖A_particle‖
where the surrounding compressive field dominates the local repulsive contribution.
**Status:** EXPLICIT

### Purpose

Local Gradient Dominance establishes the conditions under which propagation becomes effectively determined by the surrounding compressive field.
**Status:** DERIVED

### Behaviour

When Local Gradient Dominance exists:
local propagation follows the Earth's gradient;
particle-specific field contributions become negligible relative to the surrounding field;
propagation aligns with the dominant compressive gradient.

**Status:** EXPLICIT
