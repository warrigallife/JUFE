# JUFE Foundational Reading Plan — 6 October 2026

Agent: Clio (mathematical interpreter). Status: new reading-plan report,
produced in response to handover §28's recorded instruction. This document
is additive — it does not edit the handover, the working-analysis report,
the source-37 mathematical analysis, any source file, specification, or
code. It performs no implementation, no proof, and no mathematical
correction; it only identifies a starting document and a reading order, with
citations.

## 0. Why this report exists, and what it does not do

Handover §28 (`JUFE_COLLABORATOR_HANDOVER.md`, lines 1830–1838) records:

> "**Liam's direction, recorded as instructed, not yet acted on:** retain
> this analysis as a reference document; **do not** treat it as a
> continuation point. Begin a broader reading of the retained collection
> starting from its foundations, including the conceptual and functional
> relationships between sources — **the starting document for that broader
> reading has not yet been selected.**"

This report selects that starting document and proposes a reading order. It
treats `docs/reports/JUFE_37_Mathematical_Analysis.md` (the source-37
analysis, §0–§8, 1,057 lines) as settled reference material — its ten open
questions and their status are not reopened, narrowed, or answered here. It
also does not alter the older `JUFE_Working_Analysis_and_Reading_Path_2026-10-04.md`,
which recommended starting with source 37; per the task instruction, that
recommendation is superseded by handover §28's later direction for this
specific decision, and is noted as superseded, not deleted or corrected.

**Repository state at the time of this report** (checked directly, not
assumed): `git rev-parse HEAD` = `23269415603c90593d948f76b0f9ea8c912b4193`.
`git status --short` shows `JUFE_COLLABORATOR_HANDOVER.md` as locally
modified (`M`) — consistent with §28 having been appended to it in a prior
session — and the source-37 report, this repository's `.workspace-os/`
directory, a JUFE Explorer launcher script/README, and `jufe_explorer.py` as
untracked (`??`). This report adds one further untracked file. No source,
specification, runtime, or persona file was modified to produce it.

## 1. Existing analysis checked before proposing new work

Read in full or by targeted search for this report:

- `JUFE_COLLABORATOR_HANDOVER.md` §28 (in full, lines 1781–1839) and a
  structural scan of all other section headers (§1–§27) to confirm no later
  section supersedes §28 on this question — §28 is the handover's final,
  most recent section.
- `docs/reports/JUFE_Working_Analysis_and_Reading_Path_2026-10-04.md` (in
  full — already read in the session that produced the source-37 analysis;
  re-consulted here specifically for its starting-point table, inventory of
  all 26 retained files, and its own characterizations of sources 8, 36, and
  37, quoted in §2 below).
- `docs/reports/JUFE_37_Mathematical_Analysis.md` (already produced in this
  session; treated here as reference only, per the task instruction).
- `docs/reports/JUFE_Repository_Assessment_2026-10-04.md` and
  `docs/reports/JUFE_Independent_Review_2026-10-04.md`: searched for
  "foundation," "comprehensive synthesis," "starting point," "entry point,"
  and "begin with" (case-insensitive). No matches bearing on manuscript
  reading order — both reports address repository/runtime/specification
  state (Git history, `src/` implementation, `JUFE_ABTM_PROJECT_FOUNDATION`
  scaffolding, the DEF-identifier conflicts), not the retained manuscripts'
  conceptual structure. They are not cited further in this report because
  they do not bear on the question asked.
- `docs/reports/` directory listing: confirmed no existing reading-plan,
  foundational-structure, or dependency-map report exists prior to this one
  (only the three reports above, the source-37 analysis, and a test-evidence
  folder are present). This is new work, not a duplicate of prior analysis.
- The provenance map (`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/PROVENANCE_MAP.md`)
  was re-consulted to resolve every original identifier cited below to its
  current canonical path, the same procedure used in the source-37 report.

Beyond these, this report draws on the direct reading of all 26 retained
sources already performed across the two source-37 analysis passes (§0–§8 of
`JUFE_37_Mathematical_Analysis.md`), which by its own coverage statement
completed a direct reading of the full retained collection at least once.
No new source content needed to be read to answer this task; the work here
is comparative and organisational — deciding which already-read document
best serves as the entry point and in what order the rest should follow.

## 2. Candidates considered for the starting document

The task asks for a document that lets a reader "assess definitions,
conceptual and functional relationships, assumptions, mathematics and
evidence together" — i.e., a single entry point that touches all five of
those dimensions, not a narrow slice of one. Four candidates were weighed
directly against that standard, each already read in full in the prior
session:

**Source 31** (`TFJ-Unified-Harmonic-Manifold-Executive-Abstract.md`, the
Executive Abstract). Prose orientation only; contains no displayed equation
and no explicit definition beyond naming operators in passing (`\mathcal{T}_P`,
`\hat{\mathcal{D}}_\wp`, `\hat{\mathcal{H}}_y`, `\mathcal{P}_{LR}`). The
working-analysis report already classifies it as "Short orientation, not a
derivation" (its inventory table, `JUFE_Working_Analysis_and_Reading_Path_2026-10-04.md`
line 71). Fails the "mathematics" and "definitions" criteria on its own.

**Source 7** (`TFJ-Unified-Harmonic-Manifold-Four-Volume-Outline-and-Verification-Protocols.md`,
the Four-Volume Outline). States three named axioms (Planck-Floor, `3\pi`
Harmonic Closure, Universal Connectedness — lines 6–8) and lists
"Implementation Protocols"/verification standards (lines 22–26), but gives
no worked equation beyond labelling `\mathcal{T}_P = \phi^{-3}` — it is a
table of contents plus axiom names, not a derivation. Its final line is cut
off mid-sentence ("...to ensure no energy is 'lost," line 26), consistent
with the working-analysis report's note that its "final line appears
unfinished in supplied text" (line 58 of that report). Strong on naming the
axioms; weak on "mathematics" and "evidence" in worked form.

**Source 36** (`TFJ-Canonical-Self-Bootstrapping-Monograph-Architecture-V4.md`,
the V4 architecture). Supplies the functional ontology (State → Potential →
Constraint → Transfer → Transformation → Regulation → Equilibrium,
lines 109–125), a terminology crosswalk (lines 137–166), and an operator
hierarchy (lines 171–207) — genuinely useful organisational scaffolding.
But directly confirmed on inspection: most of its chapters are empty
`\chapter{...}` headings with no body text (e.g. the entire
`spectral_structure.tex` block, lines 326–346, and `verification.tex`,
lines 366–380, list chapter titles only). The working-analysis report
already notes "Many sections are stubs" (line 42 of that report, in the
starting-point table). It is the strongest candidate for *organising* a
reading plan — and is used that way below — but it cannot itself serve as
the content-bearing starting document, because most of the "definitions"
and "mathematics" it promises are not actually present in the file.

**Source 8** (`TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md`,
the Comprehensive Synthesis, 39 lines). Directly confirmed to contain, in a
single compact file: explicit definitions (`\mathcal{T}_P`, the
non-orientable manifold `\mathbb{M}^6`, the Elastic Linkage Tensor
`\mathbf{E}_{\alpha\beta}`, the index set `\mathbf{\Omega}`, lines 7–13);
worked equations spanning all four volumes (the Global Harmonic Closure
integral, line 11; the Master UFE, line 18; the Dispersion operator, line
25; the Hysteresis operator description, line 30); stated assumptions
(non-orientable topology, instantaneous propagation, line 13); and an
explicit evidence/verification section — "Verification and Compliance"
(lines 33–37): Torque Equilibrium, Planck Normalization, and Continuity,
each given as a named, checkable condition. This is the only one of the
four candidates that supplies all five dimensions the task asks for, in one
document, with actual mathematical content rather than headings or prose
alone.

Source 8 also makes an explicit, citable self-declaration of foundational
status, in its own closing Author's Note (line 38): **"This treatise
represents the first comprehensive synthesis of the `\mathbb{M}^6`
framework. It is intended to serve as the foundational text for future
rigorous derivation and experimental verification of harmonic flux
theory."** This is a source assertion (the author's own claim about the
document's role), not an independent verification that the theory itself is
sound — but it directly supports using this specific file as the entry
point for a foundational reading, which is the question this report is
answering.

This is corroborated by the working-analysis report's own prior
characterization of source 8, already on record before this task began:
**"Combines foundations, transmission, dispersion, memory and verification
with more notation"** (`JUFE_Working_Analysis_and_Reading_Path_2026-10-04.md`,
line 43, in the row recommending source 8 to "Connect the mechanisms"). That
report placed source 8 third in its own three-item starting sequence (37,
then 36, then 8) — but its own description of source 8's content is, word
for word, the closest existing match to what this task now asks the
starting document to supply ("definitions, conceptual and functional
relationships, assumptions, mathematics and evidence together"). Given
handover §28's instruction to no longer start from source 37, and given
source 36's content gap identified above, source 8 is the strongest
remaining candidate from the original three, and the strongest of all four
candidates considered.

**Recommendation: start with source 8**,
`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/CANONICAL/TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md`
(original identifier `8.md`; provenance-map row 35; SHA-256 not
re-verified in this pass — see §6 evidence limits).

## 3. The collection's "main spine": how the rest of the retained sources relate to source 8

Reading source 8 alongside the other Volume-labelled sources (already done
across the source-37 analysis passes) shows a direct structural
correspondence: source 8 is a compact, single-file pass through the same
four-volume treatise that several other retained sources expand chapter by
chapter. This is an **interpretation** formed by comparing the texts
side by side — no source file states "this is the compact version of that
chapter" in so many words — but the correspondence is close enough in
subject matter, ordering, and shared terminology to record as the
organising structure for a reading plan:

| Tier | Source(s) | Relation to source 8 |
|---|---|---|
| Abstract | 31 (`TFJ-Unified-Harmonic-Manifold-Executive-Abstract.md`) | Prose summary of the same `\mathbb{M}^6` treatise (Planck-Floor, UFE, dispersion, hysteresis, `\mathcal{P}_{LR}` all named, lines 11–13), with no equations. |
| Outline + axioms | 7 (`TFJ-Unified-Harmonic-Manifold-Four-Volume-Outline-and-Verification-Protocols.md`) | Names the same four volumes in the same order as source 8's headings, states the three governing axioms, lists the same verification standard ("net torque... sums to zero," line 24) that source 8 states as an equation (line 35). |
| Compact synthesis (recommended entry point) | **8** | Single-file pass through all four volumes with worked equations. |
| Volume I expansion | 10 (`TFJ-Volume-I-Ch01-Planck-Floor-Constraint.md`), 11/12 (`CANONICAL/11.md` + `TFJ-Volume-I-Ch02-Generalized-Field-Syntax-and-Operator-Formalism.md`) | Expand source 8 §1.1–1.3: 10 gives a longer argument for `\mathcal{T}_P = \phi^{-3}` (and states, in its own Author's Note, that this constraint "serves as the 'Grounding Axiom' for all subsequent volumes"); 11/12 gives the full operator syntax table and the master state vector `\Psi_\alpha` only named implicitly in source 8. |
| Volume II expansion | 26 (`TFJ-Volume-II-Ch01-Mechanics-of-Transmission.md`), 27 (`TFJ-Volume-II-Ch03-Quadrature-Protocols.md`) | Expand source 8 §2.1–2.2, **qualified 6 October 2026**: 26 derives a Kinetic Coupling equation under the same name (`\mathcal{K}`) as the term in source 8's Master UFE, but `JUFE_8_Foundational_Analysis_2026-10-06.md` §5 found the two are not the same functional form (source 8's `\mathbf{\mathcal{K}}(\Delta v)` is a separate additive term from its own `\Phi_\alpha/G_k` expression, while source 26's `\mathcal{K}` *is* the `\Phi_\alpha/G_k`-weighted sum) and no text reconciles them — this row's "derives the equation only named in" phrasing should be read as a shared name under an unconfirmed functional identity, not a demonstrated compatible expansion; still provisional, now flagged rather than assumed. 27 gives the Quadrature convergence criteria only described in prose in source 8 §2.2 (unaffected by this qualification). |
| Volume III expansion | 28 (`TFJ-Volume-III-Ch01-Singularity-Synthesis-and-Planck-Scale-Horizon.md`), 29 (`TFJ-Volume-III-Ch03-Horizon-Dependent-Shifting.md`) | Expand source 8 §3.1: 28 restates the identical Dispersion operator formula found at source 8 line 25 and adds the Kinetic Vortex Induction equation. 29 adds the Horizon-Dependent Shifting operator not present in source 8 at all — **qualified 6 October 2026**: `JUFE_8_Foundational_Analysis_2026-10-06.md` §5 also found that source 29 (line 7) uses `\wp_P` as a spatial "horizon center" location, while source 8 (lines 25, 36) and sources 11/12 and 28 use the identical symbol as a scalar, time-dependent "Planck pressure," with no source reconciling the two readings; 29's relationship to source 8 is therefore better described as an addition **plus** an unreconciled notation conflict, not "an addition, not a contradiction" as this row previously implied. |
| Volume IV expansion | 30 (`TFJ-Volume-IV-Hysteresis-and-Emergent-Evolution.md`) | Expands source 8 §4.1–4.2: gives the full Memory Kernel integral only described in prose in source 8 line 30, and the `\mathcal{P}_{LR}` minimization formula only named in source 8 line 32. |
| Proofs, appendices, bibliography | 32 (`TFJ-Formal-Proofs-Appendices-and-Theoretical-Lineage.md`) | Describes (but, per the source-37 report §8 Q5 finding, does not supply) proofs for claims stated across source 8 and its chapter expansions; lists the theoretical-lineage bibliography. |

Sources **not** part of this main spine, with their established status
(per the working-analysis report and the source-37 report, not
re-adjudicated here):

- **3, 4, 5, 6, 16, 34** — repeated or overlapping "Foundation Layer"
  calibration material, several with label/body provenance mismatches
  already on record (working-analysis report, lines 54–57, 65, 73). Useful
  as cross-checks on the `\mathcal{T}_P = \phi^{-3}` and `3\pi` closure
  claims once those are first encountered via source 8/10, not as an entry
  point.
- **1/1** (`TFJ-Holistic-Stability-and-Universal-Scaling.md`) — a second,
  independent compact synthesis with its own equations, but containing an
  unresolved internal inconsistency found during the source-37 follow-up
  (its stated Fibonacci-ratio limit does not match the standard
  mathematical result for the classical Fibonacci sequence, and the
  sequence `\Phi_n` it uses is never defined — `JUFE_37_Mathematical_Analysis.md`
  §8, Q2). Read after source 8, as a comparison text, not as the entry
  point.
- **35** (Shunt-Radiation Equivalence in Magnon Systems) and the combined
  RUFM/ABTM manuscript — applications/extensions built on the main spine's
  vocabulary (Elastic Linkage Tensor, Planck-Floor Constraint), read after
  the spine, consistent with the working-analysis report's own sequencing
  (its "Recommended progression," step 7, places the Magnon application
  after the core mechanics).
- **37** — per handover §28, retained as reference (the existing
  mathematical analysis already covers it in depth); not re-sequenced here.
- **CTTM Accord** — governance text, confirmed in the source-37 follow-up to
  contain no mathematical content (`JUFE_37_Mathematical_Analysis.md` §8,
  general note under Q9). Relevant to stewardship questions, not to
  foundational mathematics.
- **13, 14** (code-provenance fragments) — runtime/kernel fragments with
  their own documented provenance notes; read against the specification and
  runtime, not as manuscript foundations.

## 4. Recommended reading order

1. **Source 8** — `JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/CANONICAL/TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md`.
   Read first, in full (39 lines). Establishes the full vocabulary (`\mathcal{T}_P`,
   `\mathbb{M}^6`, `\mathbf{E}_{\alpha\beta}`, `\mathbf{\Omega}` as index
   set, `\hat{\mathcal{D}}_\wp`, `\hat{\mathcal{H}}_y`, `\mathcal{P}_{LR}`)
   and the four-volume shape of the whole collection in one sitting.
2. **Source 36** — `TFJ-Canonical-Self-Bootstrapping-Monograph-Architecture-V4.md`,
   read immediately after, specifically for its ontology (lines 109–125),
   terminology crosswalk (lines 137–166), and operator hierarchy
   (lines 171–207) — used here as the working-analysis report already
   recommended ("Organise the analysis"), but now as a second step rather
   than a parallel reference alongside source 37.
3. **Source 7** — the outline, to see the three axioms named explicitly and
   the verification protocols, now that source 8 has supplied their
   mathematical content.
4. **Volume I**: source 10, then 11/12 — the Planck-Floor argument and the
   full operator syntax/state-vector table.
5. **Volume II**: source 26, then 27 — transmission mechanics and
   quadrature.
6. **Volume III**: source 28, then 29 — singularity synthesis and
   horizon-dependent shifting.
7. **Volume IV**: source 30 — hysteresis and emergent evolution.
8. **Source 32** — proofs/appendices/bibliography, read last among the main
   spine, with the explicit awareness (already established in the source-37
   report §8, Q5) that its "proofs" are descriptions of results, not worked
   derivations.
9. **Cross-checks, in any order**: 1/1 (compare its independent synthesis
   and flagged inconsistency against the spine), 3/4/5/6/16/34 (compare the
   repeated Foundation Layer claims against source 10/11-12's fuller
   treatment), 35 and the combined RUFM/ABTM manuscript (applications built
   on the spine's vocabulary).
10. **Source 37 and the CTTM Accord** remain where they already are: 37 as
    settled reference material via the existing mathematical analysis;
    the Accord as governance context, not mathematics.

This order follows the collection's own internal structure (abstract →
outline → compact synthesis → chapter-by-chapter expansion → appendices)
rather than imposing an external one, and it surfaces the conceptual and
functional relationships between sources as it goes, per the task's
request, rather than only after the fact.

## 5. Labelling

- **Source assertion**: source 8's self-description as "the first
  comprehensive synthesis" and "the foundational text" (§2); source 10's
  self-description as supplying the "Grounding Axiom" (§3 table); source
  7's and 36's stated content (axioms, ontology, terminology) as described
  in their own text.
- **Verified**: the line-and-file citations in §2–§3 (confirmed present at
  the stated locations in each file on direct reading); the git HEAD/status
  check in §0; the absence of reading-order guidance in the Repository
  Assessment and Independent Review reports (confirmed by direct search,
  §1).
- **Interpretation**: the "main spine" structural mapping in §3 (no source
  file states explicitly that it is the expanded version of a specific
  source 8 section — this is a judgement formed by comparing shared
  terminology, equation overlap, and stated volume/chapter numbering across
  the files); the overall recommendation to start with source 8 in §2.
- **Unresolved / out of scope for this report**: all ten of the source-37
  report's open questions remain exactly as that report left them — this
  plan does not address, narrow, or depend on resolving any of them to
  propose a reading order. Whether the "main spine" sources (8, 10, 11/12,
  26–32) are internally consistent with each other on the same points of
  tension already found for source 37 (locality vs. global coupling,
  equilibrium semantics, state-vector composition) was partially surfaced
  during the source-37 follow-up (§8 of that report draws on sources 26,
  27, 28, 29, 30, 31, 32 for exactly this reason) but is not re-litigated
  here; a reader following this plan will encounter those same tensions
  directly in the main-spine sources themselves.

## 6. Coverage and evidence limits

- This report did not re-read full file contents beyond the specific lines
  quoted in §2–§3; it relies on the direct, full readings of all 26 retained
  sources already performed and recorded across the source-37 report's two
  passes (§0–§8 of `JUFE_37_Mathematical_Analysis.md`), plus the
  working-analysis report's own inventory and starting-point table. Where a
  claim here depends on a specific line, that line was re-checked directly
  for this report (source 8 in full, via a fresh read; the handover's §28
  in full; the working-analysis report's starting-point table lines 41–43).
- SHA-256 hashes were not recomputed for source 8 or the other main-spine
  files in this pass (only source 37's hash was independently verified, in
  the earlier report). The paths cited here match the provenance map
  consulted for this report; if the provenance map or canonical files have
  changed since the source-37 report's HEAD check
  (`0da2a3d1b64e58b8599cedad5e213d3f93593a5b` for the manuscript blobs,
  `23269415603c90593d948f76b0f9ea8c912b4193` for this session's HEAD), that
  would need to be re-verified before relying on this plan for
  implementation work.
- The "main spine" correspondence in §3 is this report's own interpretation,
  clearly labelled as such in §5. It is offered to help sequence reading, not
  as a claim that the source texts declare these relationships themselves.
- This report does not assess whether the theory described across these
  sources is correct, complete, or implementable — consistent with the
  Clio role, it identifies structure and reading order only, and explicitly
  does not propose mathematics, assumptions, or corrections of its own.

## 7. What Liam/Dana get from this plan, and what is still needed

Following §4's order gives a reader the full vocabulary and mathematical
backbone of the `\mathbb{M}^6` treatise in a deliberate, source-justified
sequence, before returning to source 37's narrower balance/load/shunt
material with that fuller context already in hand. It does not resolve any
of the source-37 report's ten open questions, and it does not establish
that the main-spine sources are free of the same kinds of internal
tensions already found in source 37 and its dependencies (notation
collisions, locality-vs-global-coupling, equilibrium-semantics variation) —
a reader following this plan should expect to encounter those same
unresolved issues directly, not a cleaner account of the same theory.

## 8. Correction trail — 6 October 2026 (response to Nora's independent review of the source-8 report)

An independent review of `docs/reports/JUFE_8_Foundational_Analysis_2026-10-06.md`
(`JUFE_8_Foundational_Analysis_Independent_Review_2026-10-06.md`, agent
Nora) found that two of that report's own §5 findings — the source 26/8
Kinetic Coupling mismatch and the `\wp_P` notation collision between source
29 and sources 8/11-12/28 — were not connected back to this reading plan's
"main spine" table (§3 above), even though they directly qualify how its
Volume II and Volume III rows describe sources 26 and 29. Both findings had
already been independently re-verified as genuine by Nora's review before
this correction, and were re-confirmed directly by this agent against the
primary texts (source 8 line 18 vs. source 26 line 13 for the Kinetic
Coupling mismatch; source 29 line 7 vs. source 8 lines 25/36 for the
`\wp_P` collision) before editing.

**Correction applied**: §3's table rows for "Volume II expansion" (sources
26, 27) and "Volume III expansion" (sources 28, 29) are each updated in
place with a dated qualification reflecting the source-8 report's findings.
The Volume II row's description of source 26 as deriving "the Kinetic
Coupling equation only named in" source 8 is now flagged as a shared name
under an unconfirmed functional identity, not a demonstrated compatible
expansion. The Volume III row's description of source 29 as adding content
"not present in source 8 at all" — previously elaborated elsewhere in this
report's original text as "an addition, not a contradiction" — is now
corrected to record that 29 also introduces an unreconciled notation
conflict with source 8 over `\wp_P`, not merely an addition.

**Preserved, not changed**: both rows' overall classification as part of
the "main spine" interpretation remains exactly as provisional as before —
this correction adds a qualification to two specific claims within that
interpretation, it does not retract the interpretation itself, assert a
contradiction has been resolved, or claim the two sources are unrelated.
§5's existing labelling of the whole "main spine" mapping as
**interpretation**, not verified fact, is unchanged and still applies to
both corrected rows. No external evidence was assessed in making this
correction; both qualifications rest entirely on direct re-reading of the
retained manuscript texts already cited.
