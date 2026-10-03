# JUFE Originals Archive — Plain Preservation Copies

Document ID: JUFE-SRC-ARCHIVE-001

Added: 3 October 2026, as part of the source-to-documentation reconciliation
pass.

## Purpose

This directory holds a **verbatim, byte-for-byte copy** of every one of the
38 original files catalogued in the JUFE Source Assessment Pack's
`SOURCE_MANIFEST.json`, including all 12 redundant/duplicate copies that the
manifest's own curation decision excluded from the manuscript corpus.

This is **plain preservation, not a curation decision**. It does not change,
override, or supersede:

- which file is treated as the `KEEP REPRESENTATIVE` for any duplicate
  group (that remains exactly as `SOURCE_MANIFEST.json` and
  `../MANUSCRIPTS/PROVENANCE_MAP.md` record it);
- the canonical manuscript corpus in `../MANUSCRIPTS/CANONICAL/` (which
  intentionally strips only the leading bare-numeral heading line from
  manuscript-style sources, per the existing normalization convention);
- any DEF identifier, specification, or runtime file.

Every file here is identical, byte-for-byte, to its counterpart in the
external JUFE Source Assessment Pack
(`~/Desktop/JUFE_Source_Assessment_Pack/ORIGINALS/`), which remains the
read-only source of truth. This was verified by independently computing the
sha256 of every archived file and confirming it matches both the pack file
and the `sha256` field recorded for that file in `SOURCE_MANIFEST.json`
(zero mismatches across all 38 files; see
`../MANUSCRIPTS/PROVENANCE_MAP.md` for the full checksum table).

## Contents

All 38 originals, including the nested `1/1.md`, using their exact supplied
filenames (including the two long/special-character names). No file was
renamed, reformatted, or normalized in this archive.

## Duplicates are archived too

Redundant/duplicate copies (e.g. `9.md`, `15.md`, `17.md`, `19.md`-`25.md`,
`33.md`) are present here in full, even though they are excluded from the
curated manuscript corpus. Their duplicate-of relationships are **not**
repeated in this README to avoid drift between two copies of the same fact
— see `../MANUSCRIPTS/PROVENANCE_MAP.md` for the authoritative, single
source of each file's disposition (representative vs. duplicate, and of
what).

## What this archive does not do

- It does not assert that every archived file is scientifically correct,
  verified, or implemented in any specification or runtime.
- It does not add a 39th or 40th "version" of any source — it is the same
  38 files already accounted for in `SOURCE_MANIFEST.json`.
- It does not replace the external source pack as the point of original
  custody; the pack remains untouched and authoritative for provenance
  questions (e.g. original file timestamps, the pack's own assessment
  narrative).
