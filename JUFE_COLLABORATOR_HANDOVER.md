# JUFE / ABTM — Collaborator Handover

**Snapshot reviewed:** 21 September 2026  
**Repository:** `warrigallife/JUFE`  
**Reviewed branch:** `main`  
**Latest committed snapshot:** `ab41d7f` — *Verified JUFE project snapshot*  
**Additional source reviewed:** nine-document JUFE walkthrough set

## 1. What JUFE is

JUFE is a developing theoretical and computational research framework built around JUFE/ABTM source material. Its architecture is intended to keep original source claims, interpretation, exploratory research, formal specification, dependency tracking, validation, and executable runtime behaviour distinct.

The controlling principle is:

> Source statements, interpretations, specifications, implementations, and validation are different kinds of objects and must not be silently treated as equivalent.

JUFE is not presently a complete physical simulator, a trained AI model, or a general-purpose operating system. “Research operating system” describes its proposed research method and governance: acquire carefully, preserve provenance, retrieve relevant evidence, investigate explicit dependencies, formalise cautiously, validate, and only then promote behaviour into runtime.

## 2. Current repository state

The supplied JUFE folder contains approximately:

- 46 Python files outside the historical autofix backup
- 150 Markdown files outside the historical autofix backup
- A formal specification library
- A machine-readable ABTM specification layer
- A specification/requirements engine
- Dependency and validation records
- Research-processing records for two manuscripts
- Experimental/research tools
- A Python runtime under `src/`
- Several earlier launchers and arithmetic-analysis programs
- An Irish heritage research repository
- A separate nine-document orientation/walkthrough set

The reviewed Python source compiles successfully in the review environment. That confirms syntax, not mathematical correctness or scientific validation.

### Important Git status

The supplied folder is **not identical to the current GitHub commit**. These files are present locally but untracked by Git:

- `jufe_explorer.py`
- `Start JUFE Explorer.command`
- `JUFE Explorer - READ ME.txt`

Therefore a collaborator invited to GitHub will not receive the Explorer until Liam reviews and commits those files. They should not be committed automatically merely to make the working tree clean; first confirm that this is the intended Explorer version.

The most recent committed history visible in the snapshot is:

- `ab41d7f` — Verified JUFE project snapshot, 17 September 2026
- `d27137f` — Runtime v1 stable - unified evaluation complete, 4 August 2026

## 3. Authority hierarchy

JUFE’s intended promotion chain is:

```text
SOURCE
  → RESEARCH
  → FORMALISATION
  → SPECIFICATION
  → DEPENDENCY AND VALIDATION GATE
  → IMPLEMENTATION AND TESTS
  → TRUSTED RUNTIME
```

Persuasive language, authorship, executable code, or AI confidence must not grant authority by themselves.

### Status language

| Status | Meaning |
|---|---|
| `EXPLICIT` | Directly represented by the controlling source or specification context; not automatically physically validated |
| `PROVISIONAL` | A declared working interpretation or temporary assumption |
| `UNRESOLVED` | Required information, mathematics, or relationships remain missing |
| `PROMOTION CANDIDATE` | Mature enough for formal review, but not yet controlling |
| `REJECTED / CONTRADICTED` | Failed relevant evidence or constraints; reason should be preserved |
| `VALIDATED` | Passed a stated validation whose scope must remain explicit |

The runtime must never express more certainty than the controlling specification.

## 4. Eight-layer conceptual map

1. **Architecture and separation** — keeps the main kinds of material distinct.
2. **Manuscript to formal specification** — extracts and promotes information through controlled stages.
3. **Research layer** — permits competing interpretations, experiments, and failed ideas without controlling runtime.
4. **ABTM specification layer and engine** — represents formal requirements as inspectable machine-readable contracts.
5. **Runtime** — executes only behaviour considered sufficiently defined.
6. **Dependency and validation system** — records what is missing, what it blocks, and what completion requires.
7. **Mathematical frontier** — identifies the unresolved formal bottlenecks.
8. **Research operating system** — connects the archive, retrieval, research, specification, validation, Git, runtime, and future AI assistance.

## 5. Main repository areas

| Area | Intended role |
|---|---|
| `Specifications/` | Current loader/parser/validator/execution contracts (`SPEC-000` to `SPEC-040`) |
| `JUFE_MASTER_SPECIFICATION/` | Human- and machine-readable master specification |
| `JUFE_ABTM_SPEC_LAYER/` | Structured ABTM contract, registry, and validator |
| `JUFE_ABTM_SPEC_ENGINE/` | Requirements register and specification enforcement tooling |
| `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/` | Definitions, governance, dependency closure, release and verification records |
| `JUFE_NEXT_DEFINITION_STAGE/` | Templates and roadmap for unresolved mathematical frontiers |
| `JUFE_RESEARCH/` | Experimental research tools that must not silently control runtime |
| `Research Processing/` | Manuscript originals, definitions, assumptions, dependencies, structural analysis, and validation notes |
| `src/` | Current executable runtime modules |
| `DEPENDENCY_ATLAS/` | Dependency relationships and unresolved prerequisites |
| `JUFE_CONTINUITY_PACK/` | Earlier handover and resumption record |
| `JUFE_REPOSITORY_SPECIFICATION/` | Repository governance, layers, evolution, and research-processing method |
| `Irish_Heritage_Repository/` | Separate research collection within the broader folder |
| `_JUFE_AUTOFIX_BACKUP_20260727-061258/` | Historical backup; not current controlling runtime |

The top-level earlier Python programs and launchers represent previous or parallel execution pathways. Their presence does not by itself establish which one is controlling. Consolidation must begin with an inventory and authority decision, not deletion.

## 6. Current runtime

The current `src/` runtime includes:

- Specification loader, parser, and validator
- Kernel and runtime coordinator
- ABTM engine
- Six-component local state
- State, relation, structure, and field objects
- Identity transformation
- Conservation and global-conservation calculations
- Equilibrium handling
- Field-gradient handling
- Phase-lock-related behaviour
- Toroidal-flux representation
- Sensitivity matrix
- Harmonic layer
- Tensegrity stress tensor

The current local field state uses the canonical order:

```text
(Mx, My, Mz, Ax, Ay, Az)
```

One complete local state contains six values. The current mapping foundation describes 64 cells as an 8 × 8 frame containing 384 values. Partial cells must be reported rather than silently padded, and overflow must create further frames rather than silently rearranging values.

### What the runtime actually does now

- Validates six numerical, finite components for each local state.
- Distinguishes `ACTIVE`, `VACUUM`, and `UNDEFINED` local lifecycle states.
- Computes phase difference as `M − A`.
- Checks exact and explicitly tolerance-based phase equilibrium.
- Applies the current identity transformation while recording transformation provenance.
- Evaluates complete six-value groups and preserves remaining values separately.
- Calculates existing conservation, equilibrium, gradient, phase-lock, toroidal, harmonic, sensitivity, and tensegrity outputs.
- Uses the ABTM engine version reported in code as `3.1.0`.

This is a structured partial implementation. It is not evidence that all named physics and mathematics have been established.

### Current launch paths

- `python main.py` opens the foundation runtime menu.
- `Start JUFE.command` launches the established JUFE interface on macOS.
- The local, currently untracked `Start JUFE Explorer.command` launches the newer combined Explorer.

The Explorer describes itself as an add-on that sends the same source numbers through compatible existing JUFE pathways. It does not replace or edit the original mathematics or source files.

## 7. Verified technical concerns

These are repository facts that a collaborator should address carefully:

1. **Untracked Explorer files:** GitHub does not yet contain the newest Explorer files present in the uploaded working folder.
2. **No dedicated automated test suite was found:** source compiles, but compile success is not behavioural verification.
3. **Case-sensitive path issue:** `src/runtime.py` boots `specifications/SPEC-010.md`, while the repository directory is named `Specifications`. This can work on a default case-insensitive macOS filesystem but fail on case-sensitive Linux.
4. **Dependency declaration is unclear:** runtime code imports NumPy, but the repository does not present one obvious root `pyproject.toml` or requirements file for a fresh installation.
5. **Several execution pathways coexist:** the repository contains original, master-flow, optimised-flow, results-launcher, arrangement, grid-mapper, `main.py`, and Explorer pathways. Their authority and intended use need an explicit current map.
6. **Some implementation labels are stronger than the walkthrough’s formal status:** for example, the engine reports `IMPLEMENTED` while central transformation and phase-preservation mathematics remain unresolved. Status wording should be reviewed so runtime output does not imply scientific validation.

## 8. Current mathematical frontier

### Frontier A — Lemma 3.1

Cross-axis/helical transformation mechanics remain unresolved. Required work includes:

- Exact operator
- Transformation domain
- Rotation/projection or phase geometry
- Conserved invariant
- Energy-transfer behaviour
- Continuous or discrete update law
- Relationship to the six-component state and 64-cell frame

The current runtime uses an identity transformation. It must not silently substitute invented helical mechanics.

### Frontier B — Theorem 4.2

Phase Lock and information preservation require a precise preservation contract. Preserving bytes, hashes, dictionaries, or Python objects is computational provenance; it is not automatically the claimed physical preservation mechanism.

The framework still requires a defined preserved object, transformation, equivalence relationship, scope, validator, packet destination, and reinsertion rule.

### Frontier C — Riemann–Zeta phase cancellation

The relationship is recorded as referenced but not derived. Outstanding questions include:

- Which zeta function and zero family are intended
- State-to-complex mapping `Z(Ψ)`
- What quantity cancels
- Local versus global scope
- M/A update rule
- Conservation relationship
- Relationship to the Z6 trace condition

No active field update should be presented as established until these dependencies are resolved.

### Frontier D — 64-cell/six-component mapping

The computational grouping exists, but canonical topology is not complete. Outstanding matters include:

- Neighbour rules
- Third-axis representation
- Boundary conditions
- Relationship between coordinate-free `M⁶` mechanics and the 8 × 8 projection
- Whether the grid is fundamental, projected, or an implementation convenience

The dependency chain includes:

```text
topology → neighbours → spatial gradient → field evolution
```

## 9. Relationship with Warrigal

Warrigal and JUFE should remain separate systems with a controlled connection:

```text
Warrigal archive and provenance
  → evidence retrieval
  → JUFE research
  → formalisation
  → specification
  → dependency/validation gate
  → runtime
```

Warrigal is the library: it preserves and retrieves source evidence. JUFE Research is the laboratory: it investigates selected evidence against defined questions and dependencies. Retrieved material must not be pasted directly into controlling runtime code.

The present acquisition priority remains:

1. Complete the John Kleinbauer YouTube/document pipeline in Warrigal.
2. Return to the radionics source.
3. Add Tom and “God's Scrolls” as research sources.
4. Use the growing archive to support explicit JUFE research questions.

## 10. Proposed document/book-processing role

JUFE does not require a new foundational AI model merely to work with books, manuscripts, transcripts, and passages. A practical system can retrieve preserved passages from Warrigal, attach provenance, and pass them through a defined JUFE research schema.

What is still required is a formal analysis contract specifying:

- Accepted input unit: document, section, passage, statement, definition, or equation
- What JUFE is assessing
- Permitted status outcomes
- Evidence and citation requirements
- How ambiguity and contradiction are recorded
- How a candidate interpretation is separated from source language
- How dependencies are created or updated
- What would permit later promotion into specification

Until Tom or the controlling specification supplies the missing semantic rules, software can organise, retrieve, compare, and preserve material, but it cannot honestly determine that a passage is “whole and balanced” in a JUFE-specific sense merely from the existing runtime.

## 11. Collaboration rules

1. Preserve original manuscripts and source material unchanged.
2. Never silently invent missing mathematics.
3. Keep source, interpretation, research, specification, runtime, and validation visibly separate.
4. Record whether a statement is explicit, provisional, unresolved, rejected, a promotion candidate, or validated.
5. A Python file or passing execution does not prove the corresponding mechanism scientifically established.
6. Experimental work belongs in the research layer until formally promoted.
7. Every controlling runtime behaviour should ultimately trace to an approved specification identifier.
8. Work on a dedicated Git branch and submit a pull request for review.
9. Do not delete older pathways or backups until their contents and authority have been compared.
10. Do not rewrite numbers, mappings, padding rules, or state meanings to obtain a preferred result.
11. Preserve partial cells, overflow, failures, rejected candidates, and unresolved status.
12. Ask Liam before making a decision that changes JUFE’s scientific or interpretive meaning.

## 12. Recommended initial GitHub issues

### Issue 1 — Decide and commit the JUFE Explorer state

**Goal:** Determine whether the three untracked Explorer files are the intended current versions and, if so, add them through a bounded commit.

**Acceptance criteria:**

- Compare the Explorer with the committed runtime and earlier interfaces.
- Confirm it does not modify original source or controlling mathematics.
- Record which pathways it calls.
- Add only the reviewed files.
- Confirm the working tree is clean afterwards.

### Issue 2 — Create a reproducible installation definition

**Goal:** Make JUFE installable on a fresh collaborator machine without guessing dependencies.

**Acceptance criteria:**

- Document supported Python version.
- Declare NumPy and every other required package in one root dependency definition.
- Separate optional graphical/development tools from runtime requirements.
- Verify installation in a fresh environment.

### Issue 3 — Repair specification-path portability

**Goal:** Make runtime specification loading behave consistently on macOS and Linux.

**Acceptance criteria:**

- Resolve the `specifications` versus `Specifications` case mismatch.
- Add a regression test.
- Do not duplicate or rename the controlling specification without confirming references.

### Issue 4 — Establish the first automated runtime tests

**Goal:** Convert already-declared runtime contracts into repeatable tests.

**Initial cases:**

- Exactly six values form one local state.
- Fewer than six values are rejected by the ABTM engine.
- Multiple complete states are evaluated without rearrangement.
- Remaining values are preserved exactly.
- Partial values are not silently padded.
- `VACUUM` requires six zeros.
- `UNDEFINED` and `VACUUM` remain distinct.
- Identity transformation preserves values and records provenance.
- Linux/case-sensitive specification boot succeeds.

### Issue 5 — Map the current execution pathways

**Goal:** Document which launcher or engine is current, historical, experimental, or compatibility-only.

**Acceptance criteria:**

- Inventory every top-level launcher and analysis pathway.
- Record inputs, outputs, dependencies, and authority status.
- Identify duplication without deleting it.
- Recommend one clearly labelled normal entry point.

### Issue 6 — Audit runtime status claims

**Goal:** Ensure runtime output distinguishes computational implementation from mathematical or physical validation.

**Acceptance criteria:**

- Review every `IMPLEMENTED`, `VALIDATED`, `stable`, and equivalent output.
- Define the scope of each label.
- Replace ambiguous labels only through an approved specification/documentation change.
- Add tests for the revised status contract.

### Issue 7 — Define the JUFE passage-analysis contract

**Goal:** Specify how archived books, documents, transcripts, and passages enter JUFE Research.

**Acceptance criteria:**

- Define the input/output schema and permitted status language.
- Preserve source identifiers and quotations separately from interpretation.
- Record contradictions and unresolved dependencies.
- Prevent research output from directly altering specification or runtime.
- Identify any decisions that must come from Tom.

### Issue 8 — Convert the mathematical frontier into a live dependency register

**Goal:** Track Lemma 3.1, Theorem 4.2, Riemann–Zeta cancellation, and 64-cell topology as explicit research objects.

**Acceptance criteria:**

- Each object records known content, missing content, evidence, dependants, experiments, completion criteria, and status.
- Status changes retain provenance.
- Alternative candidates can coexist.
- Rejected candidates remain recorded with reasons.

## 13. GitHub Project recommendation

A separate **JUFE** GitHub Project can be useful later, but it is not required to give a collaborator access or begin work. Repository access plus this handover and one assigned Issue is sufficient.

If a JUFE Project is created, use:

- Backlog
- Ready
- In progress
- Review
- Blocked
- Done

Useful fields are Area, Status authority, Priority, Work type, and Assignee.

Do not mix Warrigal and JUFE tasks merely because the projects interact. Cross-system tasks should link the two relevant Issues while preserving separate repositories and responsibility boundaries.

## 14. What the collaborator needs

- A direct invitation to the private JUFE repository
- This handover in the repository, preferably under `docs/`
- One bounded Issue to begin with
- Agreement to work on a branch and use a pull request
- No authority to reinterpret or “complete” missing mathematics without review
- Clarification that the untracked Explorer exists locally and is not yet on GitHub
- The nine-document walkthrough as orientation material if Liam chooses to add it to the repository

## 15. Recommended first assignment

The first assignment should be **reproducible installation plus the specification-path portability fix**. It is concrete, testable, and does not require the collaborator to make scientific decisions.

After that, the collaborator can establish the automated test foundation and map the overlapping execution pathways. The unresolved mathematical frontier should remain research/specification work rather than being guessed into code.

## 16. Source-to-documentation reconciliation (3 October 2026)

A read-only reconciliation pass cross-referenced the JUFE Source Assessment
Pack (`SOURCE_MANIFEST.json`, 38 originals / 26 distinct source texts)
against this repository's documentation, producing
`JUFE_Source_Assessment_Pack/SOURCE_DOC_RECONCILIATION_2026-10-03.md`. Once
reviewed and authorized, a second, documentation-only pass made the
following additions/restorations. No mathematics, DEF identifier, runtime
file, or controlling specification was changed by either pass.

**Added:**

- Four previously undocumented sources now tracked: `7.md` and `37.md` as
  new canonical manuscripts (items 15-16), `16.md` as a new
  provenance-unresolved entry, and `36.md` as a new non-manuscript template
  entry. See
  `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/README.md` (v1.1) and the new
  `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/PROVENANCE_MAP.md` (full
  38-original disposition map).
- `11.md`'s previously undocumented unique closing passage, preserved at
  `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/CANONICAL/TFJ-Volume-I-Closing-Conversational-Prompt-Fragment.md`.
- A code-provenance catalog for the two non-manuscript code fragments
  `13.md`/`14.md`, including verified links to the current `src/kernel.py`,
  `src/engines/abtm.py`, and `abtm_expansion.py`, at
  `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/README.md`.

**Restored:**

- `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/CTTM_ACCORD.md`, previously present
  but empty despite being cited as the source for GOV-0001, now contains
  the verbatim Accord text from the source pack in a clearly separated
  "Accord Text" section, with provenance notes kept in a distinct
  "Commentary / Notes" section. GOV-0001 itself was not touched.

**Documented but deliberately NOT resolved — see
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md`:**

- **Conflict A:** two incompatible documentary representations of the same
  "Relational Unified Field Mechanics" manuscript — a faithful, section-cited
  quotation layer in `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/`
  and `03_REFERENCE_LIBRARY/`, versus unrelated rewritten prose in
  `Specifications/Research Archive/Manuscript 001/` and `Manuscript 002/`.
- **Conflict B:** DEF identifier numbering disagrees across
  `MASTER_DEFINITION_INDEX.md`, the individual `01_MASTER_INDEX/DEFINITIONS/*.md`
  files, and `JUFE_ABTM_PROJECT_FOUNDATION/Specification/Definitions/definitions.json`
  for the same concepts (Boundary Jam, Coupled Differential Feedback,
  Harmonic Packet, Clean Cell Pool), including a direct same-folder
  collision: two files in `03_REFERENCE_LIBRARY/EVIDENCE/` both named for
  `DEF-0019` but describing different concepts, one of them empty
  (`EVIDENCE_DEF-0019_Boundary_Jam.md`).

**A future collaborator should not casually "fix" either conflict** (by
renumbering a DEF identifier, deleting a file, or merging the two manuscript
representations) without first reading
`KNOWN_DOCUMENTATION_CONFLICTS.md` in full and getting explicit sign-off —
the identifiers and both manuscript representations are treated as fixed
reference points until a deliberate review decides otherwise.
