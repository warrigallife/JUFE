# IR-1 and IR-2 — separate-context reviewer receipt

Separate-context review completed, dated **21 October 2026**. This is an independent Codex reviewer context relative to the implementing parent, **not provider-diverse review**. No files, Git state, models or network were changed/used during the review. This receipt is subsequently preserved in temporary scratch storage at the parent's request.

Paths below are relative to `~/Desktop/JUFE/`.

## IR-1 — PASS within the specified scope

**Compared:** combined manuscript lines 5–19 with Chapter 3 §§3.7–3.8, lines 110–159, and Manuscript 001 Validation V-002/V-003, lines 33–73.

- Source lines 9–12 explicitly state gradient autonomy and `D ∝ −∇M`; Chapter 3 lines 114–117 preserves that relationship.
- Source lines 14–18 state the absence of an independent particle trajectory, Earth/particle dominance condition and `Dparticle = −k∇MEarth`; Chapter 3 lines 127–159 faithfully records those claims and the dominance condition.
- The source claims the 1g result is “mathematically proven” at line 19. M1 `Validation.md` does **not** adopt that claim as established: V-002 is UNRESOLVED and requires further derivation/comparison; V-003 is PROVISIONAL and explicitly says published-observation comparison remains outstanding.
- Reused the accepted bounded formula distinction in `docs/reports/JUFE_26_Foundational_Analysis_Independent_Review_2026-10-10.md:137–149`; did not reopen code or re-perform the experimental comparison.

**Disposition:** Existing analysis faithfully distinguishes source assertion from established support. IR-1’s scoped review obligation can close on this receipt. No correction required within §§3.7–3.8/V-002/V-003. This does not validate the 1g theory, nor independently certify every line of Chapter 3.

## IR-2 — CORRECTIONS REQUIRED, with substantial checked scope passing

### Passed checks

**Chapter 4, version 1.0**

- Source lines 23–25 correspond to `Chapter_4_Coupled_Evolution.md:70–199`: jam, bypass/isolation, closed manifold, coupled equation.
- Chapter 4 lines 171–184 correctly distinguishes conservation of `M+A` from a proof of convergence of `M−A`. Lines 188–199 preserve unresolved initial conditions, stability, convergence and solution questions.
- Source lines 27–29 correspond to Chapter 4 lines 201–318: qualitative helical mechanism, equilibrium target, phase lock. Operator and numerical conditions remain unresolved rather than invented.
- The sequence agrees with `00_RELEASES/RELEASE_NOTES_v0.2_CHAPTER4.md:9–15`. The historical release says v0.2 while the present file says version 1.0; the SHA-256 identifies the exact current version reviewed. This receipt does not assert the release’s historical acceptance.

**Chapter 5, version 0.2.0**

- Source lines 29–31 correspond to `Chapter_5_Post_Phase_Lock_Mechanics.md:82–254`: stabilized matrix, non-truncating ejection, harmonic packet, clean pool and source transition.
- Lines 122–142 and 274–292 correctly treat preservation as a transfer constraint and reject software copying as physical proof.
- Lines 257–270 and 294–295 appropriately identify Hawking equivalence as a manuscript claim awaiting research validation.
- The correction in `00_RELEASES/RELEASE_NOTES_v0.2_CHAPTER5.md:11–16` is implemented in Chapter 5: no independently completed preservation stage. **This current check accepts that correction in Chapter 5.**
- Chapter 5’s header “REVIEW COMPLETE” (line 7), final “REVIEW REQUIRED” (343) and release “REVIEW REQUIRED” are conflicting historical labels. Record them as historically unverified; cite this new hash-scoped review for the checked content. Do not retroactively certify the old labels or mark the complete Volume III hardening review done.

**Lemma 3.1**

`03_REFERENCE_LIBRARY/LEMMAS/LEMMA-3.1_Cross_Axial_Helical_Deflection.md:24–123,127–208,212–268,316–366` accurately separates the source-described progression, provisional residual/operator notation, conservation consequence and unresolved operator/proof. Its execution prohibition remains appropriate. Existing repository PASS labels at 398–410 are not evidence of a mathematical proof; this new receipt confirms the inspected formalization boundary.

**Theorem 4.2’s unresolved-proof boundary**

`03_REFERENCE_LIBRARY/THEOREMS/03_REFERENCE_LIBRARY/THEOREMS/THEOREM_4_2.md:39–57,99–111` correctly preserves the missing proof and excludes executable mechanics. That part passes.

### Specific remaining corrections

**IR2-C1 — Carry the preservation correction through the theorem reference**

The theorem record still says the matrix is “preserved and subsequently ejected” (line 23), “remains intact and is subsequently transferred” (35), and its relationship chain places **Theorem 4.2 — Non-Truncating Information Preservation** between phase lock and ejection (63–95).

That presentation does not make the corrected constraint-versus-stage distinction clear and can still imply the superseded sequential preservation stage. It conflicts with the explicit discipline now present in Chapter 5 lines 77–78, 122–129 and 276–279 and its July 16 release correction.

**Required correction:** in a future separately authorised reference-file correction, make non-truncation expressly a constraint on ejection rather than a separate prior physical stage; align the relationship diagram accordingly. No new physics or proof is required. Recheck only the corrected passage/diagram.

**IR2-C2 — Distinguish theorem paraphrase from literal source**

The theorem blockquote at line 33 says:

> Following Phase Lock, the stabilized structural information of the isolated field cannot be clipped, truncated, or destroyed through the boundary process.

The manuscript line 29 says underlying geometric information cannot be “clipped or truncated”; it does not contain that quoted sentence or the added word “destroyed.” The theorem’s line 37 says it is recorded **“exactly as presented by the manuscript.”**

**Required correction:** identify line 33 as a repository paraphrase, remove the exact-transcription assertion, and avoid attributing the additional wording as literal manuscript text. Alternatively use the actual source passage, already quoted much more faithfully at theorem line 127. This is attribution correction, not mathematical analysis.

**Disposition:** IR-2 review was performed and reached a decision, but **acceptance remains open for these two narrow reference-record corrections and their recheck**. No new manuscript analysis is needed. Historical review-label provenance remains unverified, with a new scoped receipt now supplied. Missing operators, proofs and physical validation remain unresolved science, not missing review work.

## Version evidence

Directly computed SHA-256 for reviewed source/key analyses:

| File | SHA-256 |
|---|---|
| Combined manuscript | `79f2bd4521bb0fc84dd8daf1a056d53c49e8b664a799f870bdda3e5ee9777fa1` |
| M1 `Validation.md` | `62c646e243db6392484041a25c659f9d3a5e9572a68d4e835b893f8e383d3044` |
| Chapter 3 | `5c19e77d15d8fc19c56ca6d418c5fa3efff6063b06276564f150d8cdb61c347b` |
| Chapter 4 | `41201ebffa9a20f1da8af74f6b5dd4c11dcf13547b355e3d1264c3e2f3f3ebf5` |
| Chapter 5 Post-Phase-Lock | `55f5829f527c28b8af7b69a987b0aff40ed68e240b75d10c2cd992d859c3302c` |
| Lemma 3.1 | `6da9deb005268efb0542b76feb503880ec587db4fb802a5df8c2913224b223a7` |
| Theorem 4.2 | `8f925219d7706383701489f35d18264f77fee64e1937e91599dd58ea7ec21556` |

Actual reads: completion record; source lines 1–35; all M1 validation; all Chapter 3; Chapter 4 lines 1–340; all Chapter 5 Post-Phase-Lock; all lemma/theorem; both v0.2 release notes; source-26 review lines 130–160; provenance map lines 50–56. No other sources assessed.

## Clarification after parent reconciliation

The theorem relationship diagram alone could represent dependencies rather than temporal stages. The concrete concern is its combination with “preserved and subsequently ejected” / “remains intact and is subsequently transferred.” The minimal correction is an explicit constraint qualification, not a claim that the diagram independently proves an added temporal mechanism. This clarification does not change the disposition or require source changes in the current task.
