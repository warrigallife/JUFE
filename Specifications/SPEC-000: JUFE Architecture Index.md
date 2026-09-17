# SPEC-000: JUFE Architecture Index

## Purpose

This specification defines the high-level organisation of the JUFE specification library.

## Scope

SPEC-000 provides an index of the major JUFE specification series and their relationships.

It does NOT define runtime behaviour or implementation details.

## Specification Series

### 000 Series — Governance

The 000 series defines the organisational structure and governance of the JUFE framework.

Current specifications include:

- SPEC-000: JUFE Architecture Index
- SPEC-001: JUFE Specification Standard

---

### 010 Series — Runtime

The 010 series defines the JUFE runtime architecture.

Current specifications include:

- SPEC-010: Specification Loader
- SPEC-020: Specification Parser
- SPEC-030: Specification Validator
- SPEC-040: Execution Engine

---

### 100 Series — Core Runtime Extensions

Reserved for future runtime components and supporting services.

---

### 200 Series — Mathematical Specifications

Reserved for mathematical definitions, formal models, and computational theory.

---

### 300 Series — Domain Specifications

Reserved for scientific and domain-specific specifications including biology, chemistry, physics, and related disciplines.

---

### 900 Series — Experimental Specifications

Reserved for experimental or research specifications that have not yet been incorporated into the stable framework.

## Relationships

The JUFE runtime processes specifications in the following sequence:

Specification

↓

Specification Loader

↓

Specification Parser

↓

Specification Validator

↓

Execution Engine

All runtime specifications SHALL conform to SPEC-001.

## Revision

Version: 1.0

Status: Draft
