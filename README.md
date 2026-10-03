# JUFE Clean Verified

## Purpose

This repository contains the development environment, specifications, research, and supporting tools for the JUFE / ABTM framework.

## Repository Structure

- JUFE_MASTER_SPECIFICATION
- JUFE_ABTM_SPEC_LAYER
- JUFE_RESEARCH
- JUFE_DEPENDENCY_COMPLETION_FRAMEWORK

## Development Environment

This repository uses:

- Git
- Visual Studio Code
- Markdownlint
- Markdown All in One

## Status

Under active development.

A source-to-documentation reconciliation pass (3 October 2026) added
previously missing source-index entries and restored
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/CTTM_ACCORD.md`. It also documented,
without resolving, unresolved DEF-identifier numbering conflicts and two
incompatible manuscript representations — see
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md`
before changing any DEF-xxxx identifier or the `Specifications/Research
Archive/` manuscripts.

## Milestone 1 — Canonical Runtime

The canonical Python runtime lives under `src/`. Its entry point is
`main.py`, and the evaluation flow is:

```
main.py -> JUFERuntime (src/runtime.py) -> ABTMEngine.evaluate() (src/engines/abtm.py)
```

`ABTMEngine.evaluate()` now accepts four optional, caller-supplied
opt-in diagnostics, each defaulting to `None` ("not requested"):
dominance (`dominance_threshold`), L2 phase lock
(`phase_lock_tolerance`), global balance (`global_balance_tolerance`),
and bifurcation (`bifurcation_threshold`). When none of the four are
supplied, default evaluation output is unchanged from before these
diagnostics existed.

The verified test suite contains 215 passing tests.

See [`docs/MILESTONE_1_CANONICAL_RUNTIME.md`](docs/MILESTONE_1_CANONICAL_RUNTIME.md)
for the full milestone record: execution flow, input model, worked
examples for every diagnostic, response shapes, known limitations, and
traceability to the underlying manuscript definitions/requirements.