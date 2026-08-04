# 64-Cell Mapping Contract

## Status

UNRESOLVED CORE MAPPING

## Purpose

Define exactly how user-provided sequences become field states in a fixed 8 x 8 frame.

## Required decision

Choose one primary cell representation:

### Option A — Scalar cell

One number per cell.

### Option B — Subgroup-total cell

One subgroup total per cell.

### Option C — Six-component field cell

One cell stores:

- Mx
- My
- Mz
- Ax
- Ay
- Az

A full frame then requires:
64 cells x 6 components = 384 values.

## Required fields

- Cell representation
- Input grouping rule
- Coordinate order
- Empty-cell meaning
- Overflow rule
- Neighbour topology
- Boundary topology
- Third-axis representation
- Time/frame representation
- Z6 trace projection
- Audit requirements

## Non-negotiable software requirements

- No silent rearrangement
- Every source value traceable to a destination
- Empty and overflow states explicit
- Mapping version recorded in every audit
- Experimental mappings clearly marked provisional
