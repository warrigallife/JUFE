# Research Processing Guide

## Purpose

The Research Processing Guide defines the standard workflow through which manuscripts, exploratory research, and theoretical developments enter the JUFE repository.

Its purpose is to ensure that new knowledge is introduced in a structured, traceable, and reproducible manner while preserving the architectural separation between research, formal specification, validation, and runtime implementation.

Rather than prescribing scientific outcomes, this guide defines the process through which understanding matures within the JUFE framework.

## Scope

This guide applies to all original manuscripts, research notes, theoretical investigations, mathematical developments, literature reviews, and exploratory work introduced into the repository.

It establishes a consistent workflow for processing research before it is incorporated into the Mathematical Specification Layer or implemented within the Runtime Layer.

The guide applies equally to original contributions, collaborative research, and future revisions.

## Research Processing Workflow

All research should progress through a structured sequence of stages.

Although individual projects may revisit earlier stages as understanding evolves, the overall direction of development should preserve traceability and separation of responsibilities.

The recommended workflow is:

```text
Original Manuscript
        │
        ▼
Definitions
        │
        ▼
Notation and Terminology
        │
        ▼
Assumptions
        │
        ▼
Mathematical Objects
        │
        ▼
Relationships and Dependencies
        │
        ▼
Research Status Classification
        │
        ▼
Validation Requirements
        │
        ▼
Runtime Implications
...
```

Each stage should build upon the previous stage while preserving references to the original source material.

## Research Status Classification

Every significant research contribution should be assigned a clearly documented status.

The repository adopts the following classifications:

**EXPLICIT**

The concept is directly supported by the original manuscript or documented evidence.

**PROVISIONAL**

The concept represents a plausible interpretation, extension, or working hypothesis requiring further investigation.

**UNRESOLVED**

The concept remains incomplete, uncertain, or dependent upon additional evidence before further progression.
These classifications preserve transparency throughout the research process and distinguish established material from ongoing investigation.

## Traceability

Every processed research artefact should remain traceable to its origin.

Where possible, contributors should preserve references linking:

- original manuscripts;
- supporting literature;
- mathematical definitions;
- validation activities;
- runtime implementations.
  
The repository should preserve not only final conclusions but also the reasoning that led to those conclusions.

## Promotion Between Layers

Progression between repository layers should occur only after appropriate review and documentation.

The typical progression is:

Research
        │
        ▼
Mathematical Specification
        │
        ▼
Validation
        │
        ▼
Runtime

Research should not be implemented directly within the Runtime Layer without first being formalised within the Mathematical Specification Layer or other appropriate specification.

Similarly, runtime implementation should not redefine or replace established specifications.

## Guiding Principles

Research processing within JUFE is guided by several enduring principles:

- Preserve original manuscripts unchanged.
- Separate observation from interpretation.
- Document assumptions explicitly.
- Record unresolved questions.
- Maintain traceability throughout the workflow.
- Preserve architectural separation between repository layers.
- Never silently invent mathematical results.
- Revise transparently as understanding evolves.
  
These principles promote scientific integrity while supporting continual refinement of the framework.

## Long-Term Role

The Research Processing Guide provides a repeatable methodology for incorporating new knowledge into the JUFE repository.

As the framework grows, this workflow enables successive manuscripts to be processed consistently while preserving historical context, scientific transparency, and architectural coherence.

Rather than serving as a one-time procedure, the guide is intended to become a permanent component of the repository's long-term research methodology.

## Summary

The Research Processing Guide establishes the standard workflow through which ideas mature from exploratory research into formal specification, validation, and eventual runtime implementation.

By preserving traceability, explicit status classification, and architectural separation, the guide ensures that the continued evolution of the JUFE framework remains organised, reproducible, and scientifically rigorous.
