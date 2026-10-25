# JUFE Volume III, Chapter 3 — "Horizon-Dependent Shifting" (Source 29) — Foundational Analysis

Date: 10 October 2026. Agent: Clio. Status: first pass, following the
reading plan's existing order (§4, step 6: "Volume III: source 28, then
29") and handover §38's record of source 29 as that plan's next-named,
**provisional** document. Kept concise per standing practice in this
lineage: §1 cites substantial prior coverage of this source's `\wp_P`
and `\mathbf{W}}` symbols rather than re-deriving it; depth is
concentrated on the genuinely new material (§2).

## 0. Source identification

`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/PROVENANCE_MAP.md` row 21:
`29.md → JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/CANONICAL/TFJ-Volume-III-Ch03-Horizon-Dependent-Shifting.md`,
hash `75b6a6f2108ca685ccefd81faf905099d572345d4c4c45917d5973ef513e9523`
— **recomputed and verified exact**. 18 content lines (§3.1–3.4 plus
intro and Author's Note). `git rev-parse HEAD` =
`23269415603c90593d948f76b0f9ea8c912b4193`, file's last-touching commit
`636b724...`, unchanged, not locally modified.

## 1. Prior coverage — cited, not reproduced

- **`\wp_P` as a spatial location, not a scalar pressure — the finding
  this task asks to be revisited**: already established, source-8 report
  §5 (its own direct quote): "Source 29, §3.1 (line 7) uses the same
  symbol `\wp_P` as a **spatial position** — 'the distance (`r`) from
  the horizon center (`\wp_P`)'... No source states these are the same
  quantity measured two ways... or that they are unrelated symbols that
  happen to share a glyph." Carried forward as open question 4 in that
  report's §7 ("Is `\wp_P` a single global scalar... (sources 8, 11/12,
  28) or a spatial location... (source 29)?"), and reconfirmed,
  unresolved, in the source-10, source-11/12, and source-28 reports.
  **Re-checked directly against source 29's own text for this report**:
  confirmed exact — line 7 reads "the distance (`r`) from the horizon
  center (`\wp_P`)." **Not re-derived**; this report adds no new
  resolution, only the connections in §2 below.
- **`\mathbf{W}(r) = \mathbf{W}_0\exp(-\int\kappa(r)/\mathcal{T}_P\,dr)`**
  (line 14): already quoted in full in the source-37 report (§8, Q3
  follow-up, lines 696–700: "again a different quantity (weight `W`,
  not flux) and a different functional form... from source 37's
  `\Phi_{\text{excess}}`"), and already linked, as a **plausible,
  unverified interpretation**, to source 26's own undefined `\mathbf{W}`
  ("the dynamic weighting," source-26 report §2: "Neither file states
  these are the same object... recorded... on the same footing as the
  already-established... collisions"). Source-27 report §6 raises the
  same open question from its own side. **Not re-derived here.**
- **`F_{ext}}`** (line 16, "an external pressure wave"): already
  cross-referenced to source 28's own `F_{ext}}` in its stability
  equation, "consistent in name and role... but... gives it no formula
  — recorded as a plausible, unverified shared symbol" (source-28 report
  §2). **Not re-derived.**
- **Author's Note (line 17), the local/global "bridge" framing**:
  already quoted and classified in the source-37 report (§8, Q6: "frames
  the Horizon-Dependent Shifting operator as 'the bridge between the
  local matter state and the global field state'... having both a local
  tier and a global tier, with a named operator mediating between
  them"). **Not re-derived**; §2 below connects this prose framing to a
  formula for the first time.
- **Horizon Layer forward-dependency**: already recorded, from source
  28's side, as an unverified **interpretation** that this chapter
  "builds on this same concept name without redefining it" (source-28
  report §2). **Not re-derived.**

## 2. New analysis

**E1 — The Shifting Operator** (`\hat{\mathcal{S}}_H(\Psi) =
\nabla\left(\frac{\mathbf{W}_{local}}{\mathbf{W}_{global}}\right)\cdot
G_k(r)`, line 8): **not previously quoted or classified anywhere in
this lineage.** *Stated*: the full formula, glossed as "gradient-
dependent," unlike "standard sympathetic shifts" (an explicit, if
unexplained, contrast with sources 11/12's `\hat{\mathcal{S}}_y}`).
*Derived*: nothing — introduced directly. *Undefined*: `\mathbf{W}_{local}}`
and `\mathbf{W}_{global}}` are both new symbols, named only by their
subscripts, with no formula given for either — see the well-definedness
note below; `G_k(r)` — among the sources actually checked for this
comparison (26, 10, 11/12), this is the only one where `G_k}` is
written explicitly as a function of a spatial coordinate `r` rather
than a per-junction scalar `G_k}` (those three all use bare `G_k}` or
`\delta G_k}`, never `G_k(r)`). **This is scoped to the named sources
only** — the remaining retained sources were not re-checked for this
specific syntactic question in this pass, so no claim is made about
`G_k`'s form across the collection as a whole.

**Checked directly, not assumed**: whether `\mathbf{W}_{local}}` and
`\mathbf{W}_{global}}` in E1 relate to the single `\mathbf{W}(r)}` in
E3 (line 14, already cited in §1) is **not stated anywhere in this
file** — E1's ratio and E3's exponential-decay formula for `\mathbf{W}`
are never connected by an equation showing, e.g., that `\mathbf{W}_{local}}`
*is* `\mathbf{W}(r)}` or that `\mathbf{W}_{global}}` is `\mathbf{W}_0}`.
This is a new, **within-chapter** unresolved question, distinct from
the already-catalogued cross-chapter `\mathbf{W}}` ambiguity against
source 26 (§1 above). **This relationship, and the two symbols'
individual meaning, remain unresolved — recorded as such, not assumed
resolved in either direction by anything in §1 or here.**

**Both `\mathbf{W}_{local}}` and `\mathbf{W}_{global}}` are written
bold** — consistent, typographically, with this collection's other bold
symbols (`\mathbf{M}`, `\mathbf{A}`, `\mathbf{E}_{\alpha\beta}`,
`\mathbf{\Sigma}`), which prior reports in this lineage have read as
vector- or tensor-typed objects rather than scalars. **Typography alone
does not establish this** — source 29 states no type for either
symbol, and nothing here confirms the bold-implies-vector/tensor
reading actually applies to these two. More importantly, E1's own
notation (`\mathbf{W}_{local}}/\mathbf{W}_{global}}`) presents what
reads as a ratio of two such objects, but **source 29 does not state
what "division" means for two vector- or tensor-typed quantities**
(component-wise division, a scalar norm, or otherwise) — so even if
both operands are eventually given a type, the operation combining them
is not shown to be well-defined or computable from this file's own
text. This is a gap in the formula's own definition, not only in the
two operands' individual definitions.

**New connection, not previously drawn**: the Author's Note's "bridge
between the local 'matter' state and the global 'field' state" (already
cited in §1 as a prose-level framing) is **given a plausible
mathematical counterpart** by E1's own `\mathbf{W}_{local}/
\mathbf{W}_{global}}` ratio — a gradient of a local-to-global weighting
quotient reads as literally what E1's formula computes. **This is a
conceptual interpretation only**: neither the Author's Note nor §3.1
states this connection explicitly, and — given the unresolved typing
and division convention just noted — source 29 does not itself
establish that this ratio is mathematically well-defined or computable
in the first place, only that the notation is suggestive of the prose
framing. Recorded as **interpretation**, supported by the formula's own
structure, not a textual cross-reference, and not a demonstration that
the underlying quantity is well-formed.

**E2 — The Continuity Condition** (`\lim_{r\to\wp_P^+}\hat{\mathcal{S}}_H(\Phi)
= \lim_{r\to\wp_P^-}\hat{\mathcal{S}}_H(\Phi)`, line 11): **not
previously quoted or classified.** *Stated*: a two-sided limit equality
at the horizon location `\wp_P}` (using `\wp_P}` in its already-
established **spatial** sense, §1 — the limit is taken as `r` approaches
a *location*, consistent with, not contradicting, that reading).
*Derived*: nothing — asserted as "the primary constraint... must hold."
*Undefined*: no topology or metric for the domain of `r` is given (the
same kind of gap already noted for sources 11/12's bare "continuous
field map `\mathbb{M}^6\to\mathbb{R}}`" constraint and independently,
in the combined manuscript's own `Chapter_6`, §6.9.1, already found to
leave "which kind of continuity" explicitly UNRESOLVED — source-11/12
report §6). **Among these two named comparisons** (sources 11/12's bare
constraint and `Chapter_6`'s own unresolved discussion), **this
chapter's E2 is, by contrast, the only one of the three that gives a
continuity requirement a concrete mathematical form** (a two-sided
limit match at a named point), rather than asserting it in prose alone.
**This comparison is scoped to the two sources named** — the remaining
retained sources were not checked in this pass for a competing concrete
continuity form, so no claim is made that E2 is unique across the
collection as a whole. It does not resolve the general ambiguity about
what "continuous" means (E2's condition is specific to
`\hat{\mathcal{S}}_H}` at one location, not a general topological claim
about `\mathbb{M}^6}`), but it is the most concretely-formalized
instance found among the sources compared here.

**E3 — Adaptive Weighting** (line 14): classification reused from §1,
not repeated. One small, previously-unnoted textual echo: line 9's "to
ensure a seamless transition of flux without **harmonic leakage**" uses
near-identical language to source 26's own line 27, "preventing
harmonic 'backlash' or **energy leakage**" — both describe the same
kind of failure mode (loss during a gear/weight adjustment) in similar
but not identical phrasing. Neither file cites the other; recorded as a
thematic echo, not a verified link.

## 3. Correspondence with specifications, code, and tests

Checked directly against `src/`, `tests/`, `Specifications/`,
`JUFE_ABTM_PROJECT_FOUNDATION/`, `JUFE_MASTER_SPECIFICATION/`,
`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/`:

- Exact phrases ("Horizon-Dependent Shifting," "Shifting Operator,"
  "Continuity Condition," "Adaptive Weighting," "energy-trapping wall,"
  "transmission lens," "geometric elasticity") and standalone words
  ("elasticity," "ambient temperature," "gradient-dependent,"
  "re-indexes"): **zero matches anywhere checked.**
- "**cascade**" (standalone) appears only in `Chapter_7_Unified_ABTM_Field_Equations.md`
  ("the resulting behaviour enters a resonance cascade," line 715) —
  **checked directly**: the combined manuscript's own "Planetary
  Homeostasis"/damping-exceeded concept (already an established
  different lineage), not this chapter's "cascade of re-gearing"
  (line 16). No correspondence.
- "**weight**"/"**weighting**" (standalone, central to this chapter's
  `\mathbf{W}}`, `\mathbf{W}_{local}}`, `\mathbf{W}_{global}}`):
  **zero matches anywhere checked** across all six directories — a
  clean negative for one of this chapter's central symbols.
- **No specification, code, or test file anywhere checked demonstrably
  implements this chapter's own apparatus** (E1, E2, or E3) — this is
  not asserted as exhaustive beyond the terms actually checked above.

## 4. Open questions (new, not overlapping prior reports)

1. Is `\mathbf{W}_{local}}`/`\mathbf{W}_{global}}` (E1) the same object
   as `\mathbf{W}(r)}`/`\mathbf{W}_0}` (E3), within this chapter itself?
   Not stated.
2. Does E2's two-sided limit condition generalize to, or remain
   independent of, sources 11/12's bare continuity constraint and
   `Chapter_6`'s own unresolved "which kind of continuity" question?
3. Is `G_k(r)` (E1) the same gear-ratio quantity as the per-junction
   `G_k}` used elsewhere (sources 10, 11/12, 26), reparametrized by
   distance, or a distinct object?
4. Does the Author's Note's local/global "bridge" framing, now linked
   to E1's ratio (§2, interpretation), extend to or conflict with the
   collection's other local-vs-global statements (already catalogued,
   source-37 report §8 Q6)? Not examined further here.

## 5. Coverage statement

**Reused by citation**: the `\wp_P` spatial-location finding, the
`\mathbf{W}(r)}` formula and its source-26 link, the `F_{ext}}`
cross-reference to source 28, and the Author's Note's local/global
framing (all §1). **New**: full classification of E1 and E2 (first time
quoted in this lineage); the within-chapter `\mathbf{W}_{local/global}}`
vs. `\mathbf{W}(r)}` question, left unresolved; the unflagged
well-definedness gap in E1's local/global ratio (bold typing asserted
by typographic convention only, division convention unstated); the
Author's Note-to-E1 formula connection, labelled interpretation and not
a demonstration of well-formedness; `G_k(r)`'s novelty as a spatial
parametrization of a gear ratio, **scoped to sources 26, 10, and 11/12
only** (the sources actually compared, not the collection as a whole);
a fresh correspondence check (§3). **Not done**: sources 8, 10, 11/12,
26, 27, and 28 were not re-read in full, only cited; source 36 was not
consulted; no claim is made about source 30, the plan's next-named
document after this one. **External physical evidence was not sought
or assessed** — stated plainly, not implied otherwise.

## 6. Correction trail — 10 October 2026, 21:33 AEST (2026-10-10T11:33:46Z)

An independent review (`docs/reports/JUFE_29_Foundational_Analysis_Independent_Review_2026-10-10.md`,
agent Nora) found every citation checked against source 29 itself exact,
and identified two corrections, both re-verified directly against
source 29's own text before correcting:

1. **§2's local/global weighting-ratio interpretation did not flag that
   `\mathbf{W}_{local}}` and `\mathbf{W}_{global}}` are bold-typed**
   (confirmed directly, line 8) — consistent, typographically, with this
   collection's other bold symbols that prior reports have read as
   vector- or tensor-typed, though source 29 itself states no type for
   either — **nor that source 29 states what "division" means for two
   such objects**. The report treated the ratio as a computable quotient
   without flagging that the operation itself, not only the two
   operands, is unverified as well-defined. **Corrected**: §2 now states
   both symbols' bold typography, notes that typography alone does not
   establish their type, and states plainly that source 29 does not
   establish the ratio is mathematically well-defined or computable —
   the local/global "bridge" connection is now explicitly labelled a
   conceptual interpretation resting on suggestive notation, not a
   demonstration that the underlying quantity is well-formed. The
   already-correct, unresolved relationship between these weights and
   `\mathbf{W}(r)}` (E3) is preserved unchanged.
2. **Two "first/only place in the collection" claims** — for `G_k(r)`
   (§2) and for E2's concretely-formalized continuity condition (§2) —
   **asserted a collection-wide scope that this report's own disclosed
   work does not cover** (§5 already states most sources were "cited
   only, not re-read in full"). **Corrected**: both claims are now
   scoped explicitly to the sources actually named and compared in each
   case (sources 26, 10, and 11/12 for `G_k(r)`; sources 11/12 and
   `Chapter_6` §6.9.1 for the continuity form), with an explicit
   statement that the remaining retained sources were not checked for
   either specific question in this pass. **Nora's review independently
   performed an additional check of sources 7, 8, 27, 30, and 32 for
   `G_k(r)` usage and found the original claim held up even under that
   broader check** — per the task's instruction, that additional check
   is **not** adopted as this report's own: this report's claims now
   reflect only what Clio itself checked and disclosed, not Nora's
   further verification, which remains recorded solely in her review.

**Checked for consistency after both fixes**: searched the full report
for other instances of "first place," "only place," "first time," and
"the collection" — one further instance in §5's coverage statement
repeated the unscoped `G_k(r)` "first explicit spatial parametrization"
phrasing and has been corrected to match §2's scoped wording; the
remaining instances (§1's "connects this prose framing to a formula for
the first time," referring to this report's own citation history, not a
collection-wide mathematical claim) were checked and found not to need
correction.

Neither correction changes this chapter's own mathematics, the
already-accurate within-chapter `\mathbf{W}}` relationship finding (§2,
unchanged), the `\wp_P}`/`F_{ext}}` findings (§1, unchanged), the
correspondence-check results (§3), or any open question (§4). No
external evidence was assessed in making these corrections — both rest
entirely on direct re-reading of source 29 (line 8) and this report's
own already-disclosed coverage statement (§5).
