# JUFE Editorial Style Guide

Document ID: JUFE-ED-001  
Version: 0.1.0  
Status: PROVISIONAL  
Authority: JUFE Reference Specification editorial layer

## 1. Purpose

The purpose of this guide is to ensure editorial consistency, machine verifiability, and long-term maintainability of the JUFE Reference Specification.

This guide defines the editorial and machine-checkable conventions used throughout the JUFE Reference Specification.

It governs presentation, structure, and documentation standards only. It does not create scientific meaning, modify mathematical claims, or resolve unresolved content.

Where uncertainty exists, the Reference Specification takes precedence over automation.

## 2. Safety Boundary

Automated tools may report any suspected inconsistency.

Automated tools may only modify explicitly approved mechanical formatting.

Automated tools shall not silently modify:

- equations;
- definitions;
- theorem statements;
- scientific wording;
- status classifications;
- identifiers;
- normative meaning;
- manuscript traceability.

When uncertainty exists regarding whether a modification is editorial or scientific,
the tool shall report the issue rather than modify the document.

## 3. File Format

- Specification chapters shall be stored as UTF-8 encoded Markdown files.
- File names shall use words separated by underscores and shall not contain spaces.
- Every file ends with exactly one newline.
- Trailing whitespace is not permitted, except where deliberately used for Markdown hard line breaks in metadata.
- More than one consecutive blank line shall not normally appear unless required for a documented editorial reason.

## 4. Chapter Title

Each chapter begins with one level-one heading:

```text
# Chapter X — Chapter Title
```

A chapter file shall contain only one level-one heading.

The level-one heading uniquely identifies the document and serves as the
canonical document title.

## 5. Document Header

The title is followed by a metadata block containing:

```text
Project: JUFE Universe Project
Document ID: JUFE-V{volume}-CH{chapter:02d}
Version: 1.0.0
Status: LOCKED
Authority: Relational Unified Field Mechanics manuscript
Specification Layer: Reference Specification
Dependencies: JUFE-V3-CH01, JUFE-V3-CH02
```

Use `None` when a document has no dependencies.

The chapter number in the level-one heading shall match the chapter number specified in the Document ID, where a Document ID is present.

The metadata fields shall appear in the order shown above.

## 6. Heading Hierarchy

- `#` is reserved for the document title.
- `##` is used for numbered chapter sections.
- `###` is used for numbered subsections.
- Heading levels shall not jump, for example from `##` directly to `####`.
- Numbered headings shall match the chapter number.
- A blank line shall appear before and after each heading.
- Duplicate headings are not permitted unless explicitly justified.
- Section numbering shall be sequential within each heading level unless an intentional omission is documented.

## 7. Status Vocabulary

Scientific and specification status terms are defined in `STATUS_VOCABULARY.md`.

Core claim statuses:

- EXPLICIT
- PROVISIONAL
- UNRESOLVED
- DERIVED
- MODEL CLAIM

Document lifecycle statuses:

- DRAFT
- REVIEW
- LOCKED
- SUPERSEDED
- ARCHIVED

A tool may flag an unknown status but shall not replace it automatically.

Only statuses defined in `STATUS_VOCABULARY.md` shall be used unless a later revision of that document explicitly introduces additional terms.

## 8. Identifier Conventions

### 8.1 Chapter documents

```text
JUFE-V3-CH01
JUFE-V3-CH07
```

### 8.2 Definitions

```text
DEF-0001
```

### 8.3 Lemmas

```text
LEMMA-3.1
```

### 8.4 Theorems

```text
THEOREM-4.2
```

Released identifiers shall not be silently renumbered.

Identifiers shall be unique within their respective identifier class.

## 9. Lists

- Use `-` for unordered lists.
- Use Arabic numerals for ordered procedures.
- Do not mix bullet markers in one list.
- Use a blank line before and after a list.
- Use complete sentences where the items express requirements.

## 10. Tables

- Use Markdown pipe tables.
- Include a header row and separator row.
- Keep column meaning stable within the table.
- Do not use tables merely for visual spacing.
- Status tables shall normally use `Element` and `Status` unless a more precise schema is required.

## 11. Mathematics

- Inline symbols use `$...$` only when inline mathematical rendering is needed.
- Display equations shall use a consistent LaTeX display environment throughout a document.
- Equation contents shall never be automatically rewritten.
- Symbols must retain the manuscript's intended case and typography.
- Any engineering representation not uniquely specified by the manuscript shall be marked PROVISIONAL.

## 12. Code Blocks

- Use fenced code blocks.
- Add a language identifier where known.
- Code examples are non-normative unless explicitly stated otherwise.
- Automated formatting shall not alter code-block contents.

## 13. Normative Language

- `shall` indicates a requirement.
- `should` indicates a recommendation.
- `may` indicates permission.
- `must not` or `shall not` indicates prohibition.

Tools shall not replace one normative term with another automatically.

## 14. Standard Chapter Sections

The canonical order is:

1. Purpose
2. Scope
3. Authority
4. Dependencies
5. Definitions and mathematical content
6. Interpretation or functional role, when applicable
7. Status
8. Conformance Requirements
9. Verification Conditions
10. Traceability Matrix
11. Chapter Boundary, when applicable
12. Chapter Summary

A chapter may omit a section only when the omission is intentional and recorded.

## 15. Automatic Fix Policy

Initially, JUFE-Lint is report-only.

A later formatter may safely repair trailing whitespace, final newlines, excessive blank lines, blank lines around headings, and approved list-marker normalization.

The formatter shall require preview mode before write mode is used on the authoritative repository.

## 16. Change Control

Changes to this guide require a stated reason, review against existing chapters, confirmation that scientific meaning is unchanged, a version increment, and a repository-wide lint run.
