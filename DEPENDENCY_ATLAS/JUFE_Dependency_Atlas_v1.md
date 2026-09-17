# JUFE Dependency Atlas (Draft v1.0)

## Purpose

This atlas records how the concepts in the JUFE Master Specification
depend on one another. It is an architectural map for the software, not
a source of new physics.

# Level 1 -- Core Entity

ENT-001 Manifold - Contains → ENT-002 Field Cell - Constrained by →
AX-005 Global Equilibrium - Evaluated by → FLD-004 Gradient - Produces →
FLD-005 Propagation Vector

# Level 2 -- Cell Structure

ENT-002 Field Cell Stores: - ENT-003 Local State - FLD-001 Compressive
Field (M) - FLD-002 Repulsive Field (A) - Current State - History

Depends on: - GEO-001 Coordinate - GEO-002 Neighbours

# Level 3 -- Geometry

GEO-001 Coordinate → defines location

GEO-002 Neighbours → required for gradient evaluation

GEO-003 Footprint → contains local field interaction

GEO-004 Boundary → enables boundary detection

GEO-005 Tier → enables tier boundaries

# Level 4 -- Field Calculations

FLD-001 M FLD-002 A

produce

FLD-003 Magnitude

used by

FLD-004 Gradient

which produces

FLD-005 Propagation Vector

# Level 5 -- Dynamic Flow

FLD-005 Propagation Vector → DYN-001 Traffic → DYN-002 Propagation Event
→ DYN-003 Route

If blocked

→ DYN-004 Bypass Route

# Level 6 -- State Machine

ACTIVE → GRADIENT_DRIVEN → JAMMED → ISOLATED → LOCKING → LOCKED →
EJECTED → VACUUM → REUSED → ACTIVE

Dependencies:

JAMMED requires: - Boundary - Gradient - Traffic

ISOLATED requires: - Jammed - Bypass

LOCKING requires: - Coupled evolution

LOCKED requires: - Phase residual below tolerance

EJECTED requires: - Information preservation

VACUUM requires: - Successful ejection

# Level 7 -- Axioms

AX-001 Field Duality supports: - Coupled evolution

AX-002 Gradient Autonomy supports: - Gradient calculation - Propagation

AX-003 No Static Trajectories supports: - Runtime evaluation only

AX-004 Information Preservation supports: - Non-truncating ejection

AX-005 Global Equilibrium supports: - Global validation

# Level 8 -- Validation

Global Equilibrium ↓ Diagnostics ↓ Simulation Report ↓ Research
Comparison

# Open Dependencies

The following remain to be defined from future manuscript work:

-   Lemma 3.1
-   Theorem 4.2
-   64-cell topology
-   Z6 derivation
-   Phase-cancellation definition
-   Dominance threshold
-   Phase-lock tolerance
-   Tension capacity
-   Resistance threshold

## Architectural Principle

Every future software module should cite: - the definitions it uses, -
the axioms it depends upon, - the state transitions it implements, - the
validation rules it satisfies.

This atlas is intended to evolve alongside the JUFE Master Specification
while keeping stable identifiers.
