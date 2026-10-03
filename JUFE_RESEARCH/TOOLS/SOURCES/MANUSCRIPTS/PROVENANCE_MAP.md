# JUFE Source Provenance Map — All 38 Originals (Final Form)

Document ID: JUFE-SRC-PROVMAP-001 (v2 — supersedes the 3 October 2026 v1
table added earlier the same day; this version adds independently-verified
checksums, the originals archive, the `4.md` gap fix, and the Research
Processing verbatim-split finding)

Added/updated: 3 October 2026, as part of the source-to-documentation
reconciliation pass (see
`JUFE_Source_Assessment_Pack/SOURCE_DOC_RECONCILIATION_2026-10-03.md` for
the original reconciliation report this map implements).

## Method

For every one of the 38 entries in `SOURCE_MANIFEST.json`, this document's
sha256 column was computed independently by this pass directly from the
external pack file at
`~/Desktop/JUFE_Source_Assessment_Pack/ORIGINALS/<original>` using Python's
`hashlib.sha256`, not copied from the manifest. Every computed value was
then compared against the `sha256` field `SOURCE_MANIFEST.json` states for
that same entry.

**Result: all 38 independently-computed hashes matched the manifest's
stated hashes exactly. Zero mismatches.**

Where an in-repository curated copy exists (in `CANONICAL/`,
`MISSING_SOURCE/`, `../CODE_PROVENANCE/`, or `NON_MANUSCRIPT_TEMPLATES/`),
its sha256 was also computed and compared against the original. Curated
copies that underwent the disclosed heading-numeral-stripping normalization
(the same convention already used for the pre-existing 14 canonical files)
do **not** hash-match the original file — this is expected and was
verified at the content level (word-for-word diff) in the original
reconciliation pass, not assumed. Copies made with no normalization at all
(`36.md`, `37.md`) hash-match the original exactly.

Original custody remains in the user's main archive at
`INFORMATION_ARCHIVE/COLLECTIONS/JUFE/Tom_Jennings_Source_Collection/`.
The redundant repository archive was removed. Exact retained variants
`4.md`, `5.md`, `16.md`, and `34.md` are held in `MISSING_SOURCE/`;
other retained content remains in the curated locations below.

## Full 1-38 table (manifest order)

| # | Original | Manifest decision | Duplicate of | Independently-verified sha256 (matches manifest: yes, all 38) | Retained / curated location | Original custody / retained variant |
|---|---|---|---|---|---|---|
| 1 | `1/1.md` | KEEP REPRESENTATIVE | - | `cba479a20b289c48e14a4e6b654d0e26a65c2f3e3cd06cc0c71096872712b0ab` | `CANONICAL/TFJ-Holistic-Stability-and-Universal-Scaling.md` (heading-stripped, normalized) | Main archive source pack (external) |
| 2 | `10.md` | KEEP REPRESENTATIVE | - | `781c3a5a50400892c36710683092a3fbf0bc2f387711850560f0c8fa3448917f` | `CANONICAL/TFJ-Volume-I-Ch01-Planck-Floor-Constraint.md` (normalized) | Main archive source pack (external) |
| 3 | `11.md` | KEEP REPRESENTATIVE | body: `12.md` | `9f6fb824106b2c77f45b43a6698ba8fe3e5f9ec67c030232f776f9370933f793` | Body: see `12.md` row. Unique closing passage: `CANONICAL/TFJ-Volume-I-Closing-Conversational-Prompt-Fragment.md` (fragment only) | Main archive source pack (external) |
| 4 | `12.md` | KEEP REPRESENTATIVE | - | `c075e0815d668d1e98cf1bd724caa7f8e8684c07d556803649f6db03ad93e297` | `CANONICAL/TFJ-Volume-I-Ch02-Generalized-Field-Syntax-and-Operator-Formalism.md` (normalized) | Main archive source pack (external) |
| 5 | `13.md` | KEEP REPRESENTATIVE (non-manuscript/code) | - | `7e22d82eca25071e9659ca8c7695f135a15bca5132d1f3289589f7428153a67b` | `../CODE_PROVENANCE/ORIGINAL_FRAGMENTS/13-kernel-fragment.md` (normalized) | Main archive source pack (external) |
| 6 | `14.md` | KEEP REPRESENTATIVE (non-manuscript/code) | - | `fb84ae2f885ad4d38037233431aa9ac3c3dd2f3cde9df78d6a84777e63718372` | `../CODE_PROVENANCE/ORIGINAL_FRAGMENTS/14-kernel-abtm-fragment.md` (normalized) | Main archive source pack (external) |
| 7 | `15.md` | REDUNDANT ACTIVE COPY | `1/1.md` | `197b4b5b849f5dcd11fb3d1faf504567290d7d20e80c05c4529b1e3706044d21` | Not separately curated (duplicate) | Main archive source pack (external) |
| 8 | `16.md` | KEEP REPRESENTATIVE (provenance unresolved) | - | `498bfbc4da80ae5916ee29ae97da8abe771521da80e81d14b7cb1d0066056f90` | Not separately curated - content duplicates Foundation Layer text already curated via `3.md`. Tracked in `README.md` -> "a tri Ω=smoke" (Missing/Unresolved Sources) | `MISSING_SOURCE/16.md` |
| 9 | `17.md` | REDUNDANT ACTIVE COPY | `3.md` | `8786293d1a46a230b23e018c846bc10053da8644048615ff8966f2fb95cb41de` | Not separately curated (duplicate) | Main archive source pack (external) |
| 10 | `18.md` | REDUNDANT ACTIVE COPY | `4.md` | `834c16dc560334316a9bf73ac94878c4b682ffa49f9ceb9ee7517cc93483088e` | Not separately curated (duplicate). Tracked in `README.md` -> "atriΩ...Pt.2" (named alongside `4.md`) | Main archive source pack (external) |
| 11 | `19.md` | REDUNDANT ACTIVE COPY | `7.md` | `c4bca0ec5acbba1eec0cf0b6216cfc4698a987becd500565348d70e46a0a8277` | Not separately curated (duplicate). Tracked in `README.md` -> "Excluded Duplicate Source Artifacts" | Main archive source pack (external) |
| 12 | `20.md` | REDUNDANT ACTIVE COPY | `8.md` | `b5af1d977bf27e2082d8828c8843c3ea661e13abcf3d256b00785cc52dc1a2be` | Not separately curated (duplicate) | Main archive source pack (external) |
| 13 | `21.md` | REDUNDANT ACTIVE COPY | `8.md` | `6f0b0e35f4452756b157094d8a5573f5cf54a2765cf40a22f20702cbfeb433a2` | Not separately curated (duplicate) | Main archive source pack (external) |
| 14 | `22.md` | REDUNDANT ACTIVE COPY | `10.md` | `32a7d409e3308c4a07af919c3042a472f2f11497a8a1e8237b9e69446df24745` | Not separately curated (duplicate) | Main archive source pack (external) |
| 15 | `23.md` | REDUNDANT ACTIVE COPY | `12.md` | `155e6e15eab52eb6f5d6c152557774b58580bc9bf7034d55b1c5bc99d5945e38` | Not separately curated (duplicate) | Main archive source pack (external) |
| 16 | `24.md` | REDUNDANT ACTIVE COPY | `12.md` | `ae0edf5e0e97d1385b43e3f9393ca14d9bd8818037334628bc2c6d557a86439a` | Not separately curated (duplicate) | Main archive source pack (external) |
| 17 | `25.md` | REDUNDANT ACTIVE COPY | `12.md` | `7fa3d251a9821824713826d2d2d5b085bb63da28765885b7f153ba7fd0894d31` | Not separately curated (duplicate) | Main archive source pack (external) |
| 18 | `26.md` | KEEP REPRESENTATIVE | - | `732bf802afedd569bf4eeddff06915651eae64d0b2029ba09a18ff67d30fe676` | `CANONICAL/TFJ-Volume-II-Ch01-Mechanics-of-Transmission.md` (normalized) | Main archive source pack (external) |
| 19 | `27.md` | KEEP REPRESENTATIVE | - | `41b7952a78451248e656c058218fb7b9767afc9a5a00615079ffbaf43ff63537` | `CANONICAL/TFJ-Volume-II-Ch03-Quadrature-Protocols.md` (normalized) | Main archive source pack (external) |
| 20 | `28.md` | KEEP REPRESENTATIVE | - | `486e12ec67ef488658eb93529e19228b7f95578d82fb863680ea5e2a97d84392` | `CANONICAL/TFJ-Volume-III-Ch01-Singularity-Synthesis-and-Planck-Scale-Horizon.md` (normalized) | Main archive source pack (external) |
| 21 | `29.md` | KEEP REPRESENTATIVE | - | `75b6a6f2108ca685ccefd81faf905099d572345d4c4c45917d5973ef513e9523` | `CANONICAL/TFJ-Volume-III-Ch03-Horizon-Dependent-Shifting.md` (normalized) | Main archive source pack (external) |
| 22 | `3.md` | KEEP REPRESENTATIVE | - | `77ba65eb1b09f1d8f6509f4947ccc362bc6ebd34b1024825e9b86a19e22103c4` | `CANONICAL/TFJ-Non-Arbitrary-Initialization-Protocol-Foundation-Layer.md` (normalized) | Main archive source pack (external) |
| 23 | `30.md` | KEEP REPRESENTATIVE | - | `79f182643d247f4f831f4fe67974e2413472cdd626edf69364e06d9deccfcb58` | `CANONICAL/TFJ-Volume-IV-Hysteresis-and-Emergent-Evolution.md` (normalized) | Main archive source pack (external) |
| 24 | `31.md` | KEEP REPRESENTATIVE | - | `fa956ba2edb3b71ce7659a0412342e87fe93fd969822d6ce5013a517bbae265b` | `CANONICAL/TFJ-Unified-Harmonic-Manifold-Executive-Abstract.md` (normalized) | Main archive source pack (external) |
| 25 | `32.md` | KEEP REPRESENTATIVE | - | `2ab18f94f7e0538f8e234a5378d9f6597bd3ec527c4a65c8b3cdb826707348b0` | `CANONICAL/TFJ-Formal-Proofs-Appendices-and-Theoretical-Lineage.md` (normalized) | Main archive source pack (external) |
| 26 | `33.md` | REDUNDANT ACTIVE COPY | `35.md` | `da947506e8110e83ab1127864204fdc301fb849d0524213e26602a32f8dcd1c4` | Not separately curated (duplicate). Tracked in `README.md` -> "Excluded Duplicate Source Artifacts" | Main archive source pack (external) |
| 27 | `34.md` | KEEP REPRESENTATIVE (provenance unresolved) | - | `5648f451251310f8a744b389ac8ec97d59a78572ea107d51711d25acd98db03d` | Not separately curated - content duplicates Foundation Layer text already curated via `3.md`. Tracked in `README.md` -> "Vacuum Mass Gap" (Missing/Unresolved Sources) | `MISSING_SOURCE/34.md` |
| 28 | `35.md` | KEEP REPRESENTATIVE | - | `266f099bb841d6cbeaecffc38ced19e9bb16e4315e2d3ad38dafcbc160388c76` | `CANONICAL/TFJ-Shunt-Radiation-Equivalence-in-Magnon-Systems.md` (reformatted line-wrap; word-for-word identical) | Main archive source pack (external) |
| 29 | `36.md` | KEEP REPRESENTATIVE (non-manuscript/template) | - | `44294abb7ce041a4c16d6ae73b306d9cbc571c7e3b9f7284ea4807b3b231f5c7` | `NON_MANUSCRIPT_TEMPLATES/36-v4-files-manifest-template.md` (byte-identical - no heading line existed to strip) | Main archive source pack (external) |
| 30 | `37.md` | KEEP REPRESENTATIVE | - | `335ae2a70055ca438731a5e6b686d4ebe6bf17b47373b055d5f33f6c494882e0` | `CANONICAL/TFJ-Zero-Sum-Constraint-Load-and-Shunt-Mechanics.md` (byte-identical - no heading line existed to strip) | Main archive source pack (external) |
| 31 | `4.md` | KEEP REPRESENTATIVE | - | `0f1422eefbe7fdac666e86123e62ccb85ed1fbaa3d26cd84f5ddb57ed8bee7df` | **Gap closed 3 Oct 2026:** not separately curated as its own canonical file (content is Foundation-Layer-pattern text, same editorial rationale as `16.md`/`34.md`), but now explicitly named in `README.md` -> "atriΩ...Pt.2" alongside its duplicate `18.md` | `MISSING_SOURCE/4.md` |
| 32 | `5.md` | KEEP REPRESENTATIVE (title only, no body) | - | `bed7639820c4869d3f71e31646d30f672cfabccc453487f03bda9e21e1dc06a2` | `MISSING_SOURCE/TFJ-atriOmega-Non-Arbitrary-Predictor-Pt3-MISSING.md` (descriptive record that quotes the title verbatim; not a byte-identical copy of the 56-byte original) | `MISSING_SOURCE/5.md` |
| 33 | `6.md` | KEEP REPRESENTATIVE | - | `787fb1cd571ea412b2f73d94f8e6864f7f531048061b2916e46356c498ef236e` | `CANONICAL/TFJ-atriOmega-Non-Arbitrary-Predictor-Pt4.md` (normalized) | Main archive source pack (external) |
| 34 | `7.md` | KEEP REPRESENTATIVE | - | `25ab4d71ebd398c754ee74c48283f04faee5cf3659ae2bdac08abfffa5d858a7` | `CANONICAL/TFJ-Unified-Harmonic-Manifold-Four-Volume-Outline-and-Verification-Protocols.md` (normalized) | Main archive source pack (external) |
| 35 | `8.md` | KEEP REPRESENTATIVE | - | `a2621d0f271e2fb5d026d8fac4ba6874278dcb3b4c8d8b096c3c435409672666` | `CANONICAL/TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md` (normalized) | Main archive source pack (external) |
| 36 | `9.md` | REDUNDANT ACTIVE COPY | `8.md` | `3bfbf3d860dece45373e6efefe3478adfec65cea5d1d1fb35ad0fbd31f66fd43` | Not separately curated (duplicate) | Main archive source pack (external) |
| 37 | `MANIFESTO FOR UNIVERSAL UTILITY The CTTM Accord.md` | KEEP REPRESENTATIVE | - | `37b2751055b6eb6a9414482861e2140fe383818b14a9d6a634ed05d012621b10` | `../../../../JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/CTTM_ACCORD.md` - "Accord Text" section is verbatim; file also carries a separated "Commentary / Notes" section, so the full-file hash does not match this original's hash (expected) | Main archive source pack (external) |
| 38 | `Relational Unified Field Mechanics Analytical Resolution of Critical...md` (combined essay + "Unified ABTM Field Equations") | KEEP REPRESENTATIVE | - | `79f2bd4521bb0fc84dd8daf1a056d53c49e8b664a799f870bdda3e5ee9777fa1` | **Split, dual/triple representation - see `../../../../JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md` Conflict A.** (a) Word-for-word verbatim split copy (markdown-heading formatting only differs) at `Research Processing/Manuscript 001/Original Manuscript.md` (part 1) and `Research Processing/Manuscript 002/Original Manuscript.md` (part 2) - confirmed 3 Oct 2026. (b) Faithfully quoted with section citations (not verbatim, paraphrased with direct quotes) via DEF-0001-DEF-0036, LEMMA-3.1, THEOREM-4.2 in `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/`. (c) Independently rewritten, non-matching prose at `Specifications/Research Archive/Manuscript 001/002` | Main archive source pack (external) |

## Totals (arithmetic rechecked)

- **38** originals total, independently re-verified by sha256 against
  `SOURCE_MANIFEST.json` - **0 mismatches**.
- **26** `KEEP REPRESENTATIVE` entries + **12** `REDUNDANT ACTIVE COPY`
  entries = **38**. Confirmed.
- Of the 26 representatives:
  - **16** have a full, separately curated (normalized) copy in
    `MANUSCRIPTS/CANONICAL/`: `1/1.md`, `3.md`, `6.md`, `7.md`, `8.md`,
    `10.md`, `12.md`, `26.md`, `27.md`, `28.md`, `29.md`, `30.md`, `31.md`,
    `32.md`, `35.md`, `37.md`.
  - **1** (`11.md`) has a partial curated copy - only its unique closing
    fragment, since its body duplicates `12.md`.
  - **1** (`5.md`) has a descriptive `MISSING_SOURCE/` record (title
    quoted, no body to copy).
  - **2** (`13.md`, `14.md`) have a curated copy in `../CODE_PROVENANCE/`.
  - **1** (`36.md`) has a curated copy in `NON_MANUSCRIPT_TEMPLATES/`.
  - **1** (the MANIFESTO/CTTM Accord) has a curated, restored copy at
    `CTTM_ACCORD.md`.
  - **1** (the combined Relational Unified Field Mechanics / Unified ABTM
    Field Equations source) has a verbatim split copy in
    `Research Processing/`, plus a separate faithful-but-paraphrased
    quotation layer in `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/`, plus a
    non-matching independent rewrite in `Specifications/Research Archive/`
    (Conflict A, undisturbed).
  - **3** (`4.md`, `16.md`, `34.md`) retain their original label/body variants
    unchanged in `MISSING_SOURCE/`, with their status tracked in `README.md`.
  - 16 + 1 + 1 + 2 + 1 + 1 + 1 + 3 = **26**. Confirmed.
- All 38 originals remain in the user's external main archive source pack.
  GitHub retains the curated collection and four exact unresolved/title-only
  artifacts, without a second blanket archive of originals and duplicates.
