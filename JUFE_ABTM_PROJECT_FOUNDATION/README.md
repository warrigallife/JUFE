# JUFE / ABTM Project Foundation

This package establishes the formal project structure for developing the JUFE / ABTM system without altering the original source files.

## Core principle

Every implementation must identify the specification rule it implements.

## Structure

- `Specification/Definitions` — formal vocabulary and object definitions
- `Specification/Axioms` — rules treated as foundational
- `Specification/Theorems` — derived conditional results
- `Specification/State_Machines` — operational state transitions
- `Core_Engine` — reference implementation interfaces
- `Research` — datasets, 64-grid work, and development records
- `Validation` — tests tied to definitions, axioms, and theorems

## Status labels

- `EXPLICIT` — directly stated in supplied manuscript/code
- `NUMERICAL_CONVENTION` — needed for software but not fixed by manuscript
- `PROVISIONAL_MAPPING` — temporary implementation choice
- `UNRESOLVED` — definition still required

## Original files

The original JUFE files should remain outside this package and unchanged:

- `oldmate1(5).py`
- `oldmate2(4).py`
- `abtm_expansion.py`

This package is designed to sit beside them.
