# JUFE Build-Inputs Reconciliation — Two Manuscripts, Two Code Files, and the "Combined Manuscript"

Date: 16 October 2026 (UTC 02:18:04 / AEST 12:18:04). Agent: Clio
(mathematical interpreter persona). Status: reconciliation-only pass —
no manuscript content was analysed, no file was modified, no code was
executed, no agent was invoked. Local filesystem only: this report
makes no claim about the current remote GitHub state; `git rev-parse
HEAD` = `23269415603c90593d948f76b0f9ea8c912b4193`, matching the local
`origin/main` ref recorded at handover §54 — a local reference only,
no fetch run.

## 0. Scope and existing-equivalent-work check

Read for this report: handover §54 (source-35 closure, the latest
entry); `JUFE_Full_Collection_Coverage_Audit_2026-10-11.md` in full
(already read in earlier sessions, re-consulted here for row 26's
"combined manuscript" entry and its own stated gap);
`JUFE_Repository_Assessment_2026-10-04.md` (its repository map §1,
existing-work map §2, authority map §3, and §0's self-correction on
the Manuscript 001/002 path); `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/README.md`
and `PROVENANCE_MAP.md` in full; `docs/MILESTONE_1_CANONICAL_RUNTIME.md`
§14; `abtm_expansion.py`'s module docstring; and
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md`,
including its locally-uncommitted "Additional item (9 October 2026)"
addendum (`git diff` against that file, read directly — this report
treats the on-disk working-tree text as current, consistent with the
task's local-only instruction, and does not assess whether that edit
has been committed).

**No existing report performs this specific reconciliation.** A
targeted search (`docs/reports/` for "two manuscripts," "two code
files," "two original," and by filename for "reconcil*"/"build*input*")
found no prior document stating the correspondence below. The
closest-named existing document,
`JUFE_Coordinator_Build_Brief_2026-10-07.md`, is unrelated — it is a
Workspace-OS agent-orchestration design brief, not a source/manuscript
reconciliation. This report is therefore new work, not a duplicate,
but it is explicitly a **synthesis of facts already established** in
the documents above — no new manuscript content was read or analysed
to produce it.

## 1. Liam's account, verified: two manuscripts and two code files

**Verified, with exact paths and recorded relationships**, subject to
one genuine ambiguity recorded in §3 below (which specific "two code
files" are meant):

### 1.1 The two manuscripts

`abtm_expansion.py`'s own module docstring (root of the repository,
lines 5–9, already cited in the now-closed source-13/14 cycles) names
exactly two source documents it is a "[s]eparate implementation of the
mathematical operations described in":

1. "The Unified ABTM Field Equations"
2. "Relational Unified Field Mechanics: Analytical Resolution of
   Critical Cosmological Anomalies"

These are the two manuscripts Liam's account refers to. They are
**not** two of the 26 artifacts the current source-collection
provenance system tracks as separate manuscripts — see §2.

### 1.2 The two code files

Two code files are confirmed, but **the current source-collection
record and the runtime's own documentation name two different, only
partially-overlapping pairs** — this is reported as a genuine
ambiguity, not resolved by assumption:

- **Within the 26-artifact source-collection record**: `PROVENANCE_MAP.md`
  rows 5–6 are the **only two** entries disposed "(non-manuscript/code)"
  — `13.md` → `JUFE_RESEARCH/TOOLS/SOURCES/CODE_PROVENANCE/ORIGINAL_FRAGMENTS/13-kernel-fragment.md`
  and `14.md` → `.../14-kernel-abtm-fragment.md`. Both are now fully
  analysed and closed (handover §52, §53): their content is confirmed
  byte-near-identical to the root-level scripts `oldmate2(4).py` and
  `oldmate1(5).py` respectively (`JUFE_13_Foundational_Analysis_2026-10-12.md`
  §4.1; `JUFE_14_Foundational_Analysis_2026-10-12.md` §4.1).
- **Within the runtime's own documented lineage**:
  `docs/MILESTONE_1_CANONICAL_RUNTIME.md` §14 names a different pair
  together, verbatim: "`abtm_expansion.py` and `oldmate1(5).py` (both
  at the repository root) are a **separate, historical/legacy
  implementation path**... used **exclusively** from test files... as
  a comparison/parity target to prove the native `src/` ports behave
  identically to the legacy functions they were derived from." This
  pair shares `oldmate1(5).py` with the first reading but substitutes
  `abtm_expansion.py` for `oldmate2(4).py`.

`abtm_expansion.py` is **not** one of the 26 retained source-collection
artifacts — it is a separate, root-level runtime/legacy file, outside
the provenance system this reconciliation is checking against.
`oldmate2(4).py`/source 13, conversely, is confirmed (same two closed
reports) to correspond to `src/kernel.py`'s `JUFEKernel` — a
**specification-loading/boot-sealing path explicitly described as
"separate... unrelated to the diagnostics documented here"**
(`MILESTONE_1_CANONICAL_RUNTIME.md` §1) from the `ABTMEngine`
math-evaluation path `abtm_expansion.py` and `oldmate1(5).py` feed.

**Reconciliation**: both pairings are independently documented and
true of different things. If "the two code files used to build JUFE"
means the two code-type artifacts the source collection itself
retains, the answer is source 13 + source 14 (`oldmate2(4).py` +
`oldmate1(5).py`'s content). If it means the two files the current
canonical math engine (`ABTMEngine`) was ported from and is still
tested for parity against, the answer is `oldmate1(5).py` +
`abtm_expansion.py`. Both readings agree on `oldmate1(5).py`/source 14;
they disagree on whether the second file is `oldmate2(4).py` (source
13) or `abtm_expansion.py` (untracked by the source collection).

## 2. How the "combined manuscript" relates to the two original manuscripts

**Established directly, closing a gap the audit itself flagged as
unverified.** The full-collection audit's own row for this artifact
states: "this file uses an entirely different symbolic apparatus...
from the `\mathbb{M}^6` Unified Harmonic Manifold treatise this
reading plan tracks... it belongs to a separate document lineage,
already tracked elsewhere by
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/MASTER_DEFINITION_INDEX.md`/
`KNOWN_DOCUMENTATION_CONFLICTS.md`, which this audit did **not**
check — whether *that* separate tracking already covers it **is
unverified here**" (`JUFE_Full_Collection_Coverage_Audit_2026-10-11.md`,
row 26). This report performs that check.

`PROVENANCE_MAP.md` row 38 records the retained "combined manuscript"
artifact's own supplied name as: `Relational Unified Field Mechanics
Analytical Resolution of Critical…md` **"(combined essay + 'Unified
ABTM Field Equations')"** — i.e., the provenance record's own
disposition note already states that this single retained file
combines both of the two manuscript titles named in §1.1.

`JUFE_Repository_Assessment_2026-10-04.md` (§0's self-correction,
independently re-verifying against `origin/main`) establishes the
historical mechanism of that combination: commit `636b724`
("Preserve all 26 retained source files whole and byte-unchanged")
"[d]eletes `Research Processing/Manuscript 001/Original Manuscript.md`
and `Manuscript 002/Original Manuscript.md`... superseded by the
single whole file [already] added at `Research Processing/` root" —
the same file now tracked at `PROVENANCE_MAP.md` row 38. **The
"combined manuscript" is therefore the later-merged, single-file
successor to what were previously two separate split files
(`Research Processing/Manuscript 001/Original Manuscript.md` and
`Manuscript 002/Original Manuscript.md`), not a third, independent
document.** This is a provenance/history fact, verified from commit
history and file-disposition metadata — it does not require, and this
report does not perform, any analysis of the combined manuscript's
own mathematical content, consistent with its continued "None" status
(handover §54: 2 "None" rows remain — source 5 and the combined
manuscript).

**One further, already-documented complication, correctly distinguished
from the above and not conflated with it**: `KNOWN_DOCUMENTATION_CONFLICTS.md`'s
"Conflict A" records that **a separate pair of files**,
`Specifications/Research Archive/Manuscript 001/002`, independently
and *differently* represents "the same manuscript" (`Relational Unified
Field Mechanics`) from the `01_MASTER_INDEX/`+`03_REFERENCE_LIBRARY/`
DEF-identifier chain — confirmed still open at `origin/main`
(`JUFE_Repository_Assessment_2026-10-04.md` §3's authority-map row,
"Conflict A, still holds"). This is a **different pair of files** from
the `Research Processing/Manuscript 001/002` subfolders §1.1's
manuscripts trace through (per the Repository Assessment's own
existing-work map §2: "`Specifications/Research Archive/Manuscript
001/002` connects to nothing in `src/` or `tests/`... it reads as a
standalone philosophical restatement with no onward specification or
implementation link. The `DEF-layer` chain... is the one that actually
reaches running, tested code"). This report does not resolve Conflict
A — it is already tracked, already open, and outside this
reconciliation's scope — but records it here so the two similarly-named
"Manuscript 001/002" locations (`Research Processing/` vs.
`Specifications/Research Archive/`) are not confused with each other.

A third, textually distinct manuscript lineage — the "Unified
Harmonic Manifold" (`\mathbb{M}^6`) treatise (sources 7, 8, 10, 11/12,
26–32, the reading plan's "main spine") — is unrelated to either
manuscript named in §1.1, confirmed by `KNOWN_DOCUMENTATION_CONFLICTS.md`'s
own "Additional item (9 October 2026)" entry (locally present,
uncommitted per `git status`): "none of the three files [Conflicts
A–C, `MASTER_DEFINITION_INDEX.md`, the Dependency Atlas] contains
'Unified Harmonic Manifold,' 'Elastic Linkage,' 'Master UFE,'
`\mathbb{M}^6`, or 'Comprehensive Synthesis' anywhere." Noted here
only to confirm it is not a candidate for either of Liam's "two
manuscripts" — it has its own, separately-closed/substantial analysis
(`JUFE_37_Mathematical_Analysis.md`, `JUFE_8_Foundational_Analysis_2026-10-06.md`
and its independent review), not repeated here.

## 3. Distinguishing prior use, prior assessment, newly completed analysis, and outstanding coverage

| Item | Prior use in implementation | Prior assessment | Newly completed analysis (this report) | Outstanding |
|---|---|---|---|---|
| "Unified ABTM Field Equations" + "Relational Unified Field Mechanics..." (the two manuscripts, §1.1) | Cited as the basis for `abtm_expansion.py`'s reimplementation (that file's own docstring) | Content already read/catalogued piecemeal via the combined-manuscript's chapter correspondences in `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK` (DEF-layer, Volume III) — not a dedicated Clio-style source analysis | None — this report only establishes provenance/naming correspondence (§2), not content | The combined-manuscript artifact itself remains "None" under the audit's own criterion (handover §54) — a dedicated analysis is still outstanding, explicitly **not** performed here per the task's restriction |
| `oldmate1(5).py` / source 14 | Historical implementation basis for `ABTMEngine`'s math (parity-tested, `MILESTONE_1` §14) | Full dedicated analysis closed (handover §53) | None | None — closed |
| `oldmate2(4).py` / source 13 | Basis for `src/kernel.py`'s `JUFEKernel` (boot-sealing path, separate from `ABTMEngine`) | Full dedicated analysis closed (handover §52) | None | None — closed |
| `abtm_expansion.py` | Historical implementation basis for `ABTMEngine`'s math, alongside `oldmate1(5).py` (`MILESTONE_1` §14); parity-tested in `tests/test_z6_equivalence.py` and others | Characterised in the now-closed source-13/14 reports (as comparison context) and in `JUFE_Repository_Assessment_2026-10-04.md`; never given its own dedicated source-style analysis, and is **not** a retained source-collection artifact, so none is owed under the audit's criterion | None | Not outstanding under the audit (it is not one of the 26 tracked artifacts) |
| The "combined manuscript" ↔ the two original manuscripts' identity (§2) | — | Partially established (Repository Assessment §0's commit-history finding; the audit's own "unverified here" flag) | **Yes — this report connects those two existing findings explicitly**, closing the audit's own flagged gap | Whether this reconciliation should be reflected back into the audit or `KNOWN_DOCUMENTATION_CONFLICTS.md` is itself a follow-up question (§4) |
| Conflict A (`Specifications/Research Archive/` vs. DEF-layer) | — | Already tracked and open (`KNOWN_DOCUMENTATION_CONFLICTS.md`, confirmed still open) | None — only distinguished from §2's finding so the two are not confused | Conflict A's own resolution remains outstanding, unchanged by this report |

## 4. Is a targeted follow-up needed?

**Yes, one narrow follow-up — recording, not performing it here, per
the task's restriction against beginning new manuscript analysis or
modifying existing files in this pass:**

`JUFE_Full_Collection_Coverage_Audit_2026-10-11.md` row 26 explicitly
states its own "combined manuscript ↔ `KNOWN_DOCUMENTATION_CONFLICTS.md`"
relationship as "unverified here." This report has now verified it
(§2) using already-existing evidence (the Repository Assessment's
commit-history finding and the provenance map's own disposition note).
**The follow-up need is to have that verification reflected back into
the audit's own row 26 and/or into
`KNOWN_DOCUMENTATION_CONFLICTS.md`**, so a future reader of either
document does not re-open a question this reconciliation has already
answered. This report does not make that edit itself — the task
restricts this pass to inspection and reconciliation, not modification
of existing files — and the relevant audit/handover owners should
decide the correct location for that cross-reference (handover
continuity recording is Marguerite's documented write boundary, not
Clio's; see the established per-agent write-boundary convention
already recorded in this project's prior cycles).

**No follow-up is needed to re-verify which pair of files is "the two
code files"** beyond what §1.2 already states: both candidate pairs
are independently, correctly documented for different purposes
(source-collection provenance vs. runtime implementation lineage); the
ambiguity is a fact about Liam's informal phrasing mapping onto two
different existing records, not a gap in either record itself.

**No new manuscript analysis is needed or recommended by this report**
for the combined manuscript specifically as a result of this
reconciliation — its "None" status is a separate, already-tracked,
pre-existing fact (handover §54), and whether/when to schedule its
dedicated analysis is unchanged by establishing its provenance here.

## 5. Limitations

- This report inspects local files only; it does not fetch, assume, or
  claim anything about the current remote GitHub state.
- `KNOWN_DOCUMENTATION_CONFLICTS.md`'s "Additional item (9 October
  2026)" section is read from the current, locally-modified working
  tree (confirmed present via `git diff`) — this report does not
  assess whether that edit has been committed, and treats it only as
  current local content, consistent with the task's instruction.
- No manuscript content (the combined manuscript, the `\mathbb{M}^6}`
  treatise, or the `Specifications/Research Archive/` texts) was read
  or analysed in this pass beyond what the cited, already-existing
  reports already establish.
- Conflict A and the `01_MASTER_INDEX/`/`03_REFERENCE_LIBRARY/`
  numbering disagreements (Conflict B) are cited, not re-verified or
  resolved, here.
- This report does not assess whether `abtm_expansion.py`'s
  reimplementation is mathematically faithful to either named
  manuscript — only that it names them as its stated source, per its
  own docstring.
- No code was executed to produce this report.

## 6. Summary for the record

- **Exact path saved**: `~/Desktop/JUFE/docs/reports/JUFE_Build_Inputs_Reconciliation_2026-10-16.md` (this file) — no adequate existing equivalent was found (§0).
- **Liam's account is verified**, with the precision that "two code
  files" maps onto two different, independently-documented pairs
  depending on whether the source-collection record or the runtime's
  own legacy-implementation lineage is meant (§1.2) — not a
  contradiction, but a genuine terminological ambiguity now recorded
  precisely.
- **The "combined manuscript" is the later-merged, single-file
  successor to the two manuscripts named in Liam's account** (the two
  split `Research Processing/Manuscript 001/002/Original Manuscript.md`
  files, deleted by commit `636b724` in favour of the single file now
  at `PROVENANCE_MAP.md` row 38) — closing the audit's own,
  explicitly-flagged "unverified here" gap (§2).
- **A separate, already-open documentation conflict (Conflict A)**
  concerns a different pair of files
  (`Specifications/Research Archive/Manuscript 001/002`) and must not
  be confused with the manuscripts this reconciliation addresses (§2).
- **One targeted follow-up is recorded, not performed**: reflecting
  this reconciliation's finding back into the audit's row 26 and/or
  `KNOWN_DOCUMENTATION_CONFLICTS.md` (§4).
- No existing analysis was repeated; no new manuscript analysis was
  begun; no file was modified.

Stop.
