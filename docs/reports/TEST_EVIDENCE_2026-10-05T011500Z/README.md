# JUFE test-suite evidence — 2026-10-05

> **Publication derivative (5 October 2026).** This entire directory
> (`README.md` and the 9 other files beside it) is a copy prepared for
> in-repository publication, not the byte-identical archive original. A
> local-machine username path was shortened to a repository-relative `~/`
> form in this file and in `python_version.txt` and `working_tree.diff`;
> the other 7 files had no occurrences and are unchanged. The original,
> unredacted
> directory remains at
> `~/Desktop/INFORMATION_ARCHIVE/COLLECTIONS/JUFE/reports/TEST_EVIDENCE_2026-10-05T011500Z/`
> on the maintainer's machine. Any prior hash-verification claim describing
> this directory as byte-identical to that original (see
> `JUFE_COLLABORATOR_HANDOVER.md` §25) describes its state *before* this
> redaction — accurate as history, but this copy is no longer
> byte-identical to the archive original by design. See
> `JUFE_COLLABORATOR_HANDOVER.md` §27 for the full redaction record. The
> underlying test result itself (215/215 passing) is unaffected — none of
> the redacted text was part of the test output's substance, only
> incidental path/environment detail.

Closes the gap flagged by Nora — Workspace Auditor's "Second follow-up —
5 October 2026" review (`JUFE_Independent_Review_2026-10-04.md`, §4): the
215-test result recorded in `JUFE_COLLABORATOR_HANDOVER.md` §23 existed
only as prose, with no saved artifact. This directory is that artifact.

## Command run (exactly once)

```
.venv/bin/python3 -m unittest discover -s tests -v
```

Run from `~/Desktop/JUFE` (repository root).

## Revision and environment

- **`HEAD`:** see `HEAD.txt` — `636b724ef4a48e3c537dc8d296a101b62efe556c`
  (the authorised sync target from §23, unchanged since).
- **Python:** see `python_version.txt` — Python 3.14.7, via the project's
  own `.venv/bin/python3`. No package was installed and no code was changed
  before, during, or after this run.
- **Start time (UTC):** see `start_time.txt` — `2026-10-05T01:32:10Z`
- **End time (UTC):** see `end_time.txt` — `2026-10-05T01:32:18Z`

## Working-tree state at test time — NOT pristine, stated explicitly

The working tree was **not** a clean checkout of `HEAD` at the time this
test ran. Two tracked files had uncommitted modifications, both
documentation-only:

1. `JUFE_COLLABORATOR_HANDOVER.md` — carrying the accumulated, still
   uncommitted §16–§23 continuity record.
2. `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/KNOWN_DOCUMENTATION_CONFLICTS.md`
   — carrying a dated path-correction note added immediately before this
   test run (see the handover's next dated entry for detail).

Full `git status --porcelain=v2 --branch` output is in `git_status.txt`;
the full `git diff` for both files is in `working_tree.diff`. Neither
modified file is inside `src/` or `tests/`, and neither changes any
mathematics, specification, identifier, or runtime code — but this run
should not be described as having tested a pristine working tree, and is
not described that way anywhere in this record. The four pre-existing
untracked paths (`.workspace-os/`, `JUFE Explorer - READ ME.txt`, `Start
JUFE Explorer.command`, `jufe_explorer.py`) were also present, unchanged
from every prior pass, and are not part of the Python package under test.

## Result

- **Exit code:** see `exit_code.txt` — `0`
- **Summary:** `Ran 215 tests in 0.046s` / `OK` (215 passed, 0 failed, 0
  errored, 0 skipped) — see the tail of `stderr.txt`.
- `unittest`'s default verbose output goes to stderr, not stdout — this is
  normal `unittest` behaviour, not an error; `stdout.txt` is empty (0
  bytes) for that reason, and is included anyway for completeness rather
  than omitted.

## Files in this directory

- `README.md` — this file
- `HEAD.txt`, `git_status.txt`, `working_tree.diff` — repository state
  immediately before the test command ran
- `python_version.txt` — interpreter identity and path
- `start_time.txt`, `end_time.txt` — UTC timestamps bracketing the run
- `stdout.txt`, `stderr.txt` — complete, unedited captured output
- `exit_code.txt` — the shell exit status of the test command
