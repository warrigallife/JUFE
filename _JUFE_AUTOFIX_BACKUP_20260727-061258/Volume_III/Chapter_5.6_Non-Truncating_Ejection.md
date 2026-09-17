# Chapter 5.6 — Non-Truncating Ejection

**Document ID:** JUFE-V3-CH05.6

**Version:** 1.0

**Status:** DRAFT

Following Phase Lock, the manuscript states that the stabilized
Structural Matrix is ejected without clipping or truncation.

Within the manuscript sequence, ejection represents the transfer of the
preserved structural information from the isolated field cell.

The specification records this behaviour as occurring after Phase Lock, with non-truncation treated as a constraint on the transfer rather than as a separate physical stage.

---

## Functional Role

Within the manuscript sequence, non-truncating ejection:

- transfers the preserved Structural Matrix;
- preserves the integrity of the stabilized structure during transfer;
- occurs as harmonic packet transfer;
- occurs before local Absolute Vacuum reset.

---

## Explicit Manuscript Statements

The manuscript explicitly supports the following:

- ejection occurs after phase lock;
- the preserved structure is not clipped;
- the preserved structure is not truncated;
- the stabilized structural matrix is ejected as a harmonic packet;
- the harmonic packet is transferred into the Clean Cell Pool.

---

## Unresolved Mathematical Representation

The manuscript does not specify:

- the ejection operator;
- propagation equations;
- transport geometry;
- propagation velocity;
- boundary conditions;
- numerical implementation.

These remain **UNRESOLVED** within the present specification.

---

## Engineering Constraints

Future implementations shall not assume:

- a transport algorithm;
- packet routing;
- numerical propagation models;
- implementation-specific communication mechanisms;

unless explicitly defined by later specification layers.

The present chapter records only the manuscript-defined sequence.
