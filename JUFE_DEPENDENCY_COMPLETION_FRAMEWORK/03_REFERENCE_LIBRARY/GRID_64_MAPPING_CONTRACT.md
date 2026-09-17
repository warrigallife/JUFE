# GRID_64_MAPPING_CONTRACT

## Purpose

Define the formal boundary between the JUFE M^6 field model and the
existing 64-cell computational representation without asserting an
unproven physical mapping.

## Representation Status

**Status:** PROVISIONAL_MAPPING

The existing JUFE software architecture supports a fixed 64-coordinate
representation arranged computationally as an 8 × 8 frame.

This representation SHALL NOT presently be interpreted as a complete
geometric representation of the coordinate-free shared 3D footprint.

## Established Repository Facts

1. A 64-cell field representation exists in the JUFE architecture.
2. The current computational representation uses an 8 × 8 coordinate frame.
3. The representation is implemented by `jufe_64_grid_mapper`.
4. Existing code contains a Z6/trace diagnostic.
5. Individual coordinates may carry field-state information.
6. The relationship between the 64-cell representation and the M^6 field
   is not yet formally derived.

## Unresolved Mapping Questions

The following remain UNRESOLVED:

- whether each coordinate stores one scalar, one subgroup, or the complete
  six-component M/A state;
- how the third spatial dimension is represented by an 8 × 8 frame;
- neighbour topology;
- boundary topology;
- whether multiple frames encode depth, time, or another dimension;
- the mathematical map from the shared 3D footprint into 64 coordinates;
- derivation of the original Z6 trace from the M^6 field;
- whether the trace acts on a scalar projection, cell-state matrix,
  transformed barrier matrix, or another object.

## Formalization Constraint

Until a derivation is established, no bijection, projection, embedding,
discretization, tensor mapping, or dimensional-reduction operator between
M^6 / the shared 3D footprint and the 64-cell frame SHALL be treated as
manuscript-derived.

Any proposed mapping must be labelled PROVISIONAL until independently
derived and validated.

## Required Future Mapping

A completed mapping contract must eventually define a transformation

    P_64 : M^6 -> C_64

or an appropriately revised mathematical object, where C_64 denotes the
64-coordinate computational representation.

The domain, codomain, dimensional treatment, topology, conservation
properties, and invertibility requirements of P_64 remain UNRESOLVED.

## Z6 Dependency

The existing Z6/trace diagnostic is implementation evidence, but its
derivation from the M^6 field remains UNRESOLVED.

Therefore the Z6 trace SHALL NOT currently be used as proof of the
physical validity of the 64-cell mapping.

## Current Decision

Retain the existing 64-cell / 8 × 8 architecture as a PROVISIONAL
computational representation.

Do not modify the original implementation.

Formal derivation from M^6 is deferred pending resolution of the mapping
questions above.
