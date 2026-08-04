# JUFE Repository Style Guide

**Version:** 0.1.0  
**Status:** ACTIVE

---

# Purpose

This document defines the writing standard used throughout the JUFE
engineering specification.

Its purpose is to ensure that manuscript statements, engineering
specification, and implementation guidance remain clearly separated.

---

# Writing Levels

## Level 1 — Manuscript

Use when describing what the manuscript explicitly states.

Preferred wording:

> The manuscript states...

> The manuscript describes...

> The manuscript identifies...

Avoid introducing interpretation at this level.

---

## Level 2 — Specification

Use when translating the manuscript into engineering language.

Preferred wording:

> Within this specification...

> This specification represents...

> This chapter records...

This level may organise manuscript concepts but shall not invent new ones.

---

## Level 3 — Engineering Constraints

Use only when defining repository implementation requirements.

Preferred wording:

> Implementations shall...

> Future implementations shall not...

> Repository artifacts shall...

This level applies only to engineering guidance and not to manuscript claims.

---

# Status Labels

## EXPLICIT

Directly supported by the manuscript.

---

## PROVISIONAL

Engineering interpretation or formalisation that has not been explicitly
defined by the manuscript.

---

## UNRESOLVED

Information not supplied by the manuscript and intentionally left undefined.

---

# Repository Principle

The manuscript remains the authoritative source.

The repository exists to formalise and organise the manuscript, not to
replace or extend it.

Whenever uncertainty exists, preserve the manuscript wording and mark the
remaining concepts as PROVISIONAL or UNRESOLVED rather than silently
introducing new assumptions.