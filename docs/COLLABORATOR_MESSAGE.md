# Collaborator message and findings — 2026-09-21

Branch: `collab/linux-portability-and-tests`. Nothing on `main` has been changed.

## Message for Liam

Hi! I worked from the repos you invited me to, in a separate copy and on a separate
branch. Nothing has been changed on `main`. I found some things we should decide
together before going further.

**JUFE**

1. **Boot fails on the committed files.** The parser counts a definition only when a
   line starts with `DEF-`, and the validator rejects a specification with none.
   `Specifications/SPEC-010.md` has none, so `python main.py` -> Boot stops with
   "Specification contains no executable definitions." Does your copy on the Mac
   differ? Should boot use a different file, or should the parser accept more?
   (This changes what "definition" means, so I did not touch it.)
2. **The Explorer files are not on GitHub.** `jufe_explorer.py`,
   `Start JUFE Explorer.command` and `JUFE Explorer - READ ME.txt` exist only on your
   Mac. Can you upload the intended versions?
3. **What is a cell in the 64-cell grid?** The handover says a cell holds a 6-value
   state, so 384 values fill one 8x8 frame. `jufe_64_grid_mapper.py` puts one value in
   each cell instead, pads short input with `0.0`, and does not open a second frame
   for 768 values. Which is intended?
4. **What should `IMPLEMENTED` mean?** The engine prints it on every successful run.
   Separately, `stable` means two different checks (trace mod 6 == 0 in
   `compute_manifold_stability`; `conserved and equilibrium` in `evaluate`).
5. **Which launcher is the normal entry point?** `Start JUFE.command` runs
   `jufe_original_launcher.py`; the handover points new users to `python main.py`.
   See `docs/LAUNCHER_MAP.md`.
6. **Stray copy of the engine** at `src/src/engines/abtm.py` (version 2.3.0,
   tracked, not importable). Keep or retire? Nothing was deleted.
7. **Who is Tom,** and which of the semantic rules are his to supply?

**Warrigal research suite**

8. **Where is the rest of the work?** The handover reviewed branch
   `warrigal-foundation-01` (commit `a7d1685`). GitHub has only `main`
   (`1516770`), with 39 test modules / 179 tests / 48 source files, against the
   handover's 54 / 250 / 61. The README on `main` is empty. Is work still only on
   your Mac?
9. **`instaloader` is not declared** in `pyproject.toml`, but three source files
   import it (`instagram_cli.py`, `instagram_browser_campaign.py`,
   `acquisition/instagram.py`). OK to add it?
10. **Python 3.14** is required by `pyproject.toml`. The suite was only run on 3.12.

The four mathematical frontiers (Lemma 3.1, Theorem 4.2, Riemann-Zeta phase
cancellation, 64-cell topology) are yours and Tom's to define. Nothing here attempts
them.

## What this branch changes

- `src/runtime.py`: boot resolves `Specifications/SPEC-010.md` from the repository
  root, so it no longer depends on filesystem case or working directory (Issue 3).
- `requirements.txt`: `numpy`. Verified on Linux, Python 3.12.3, NumPy 2.5.3. A clean
  install was not verified (Issue 2).
- `tests/`: 34 tests (Issue 4). Run from the repository root:

      python -m unittest discover -s tests -t . -v

  Result: 28 pass, 6 expected failures. Each expected failure is marked
  `OPEN: needs project-owner decision` and asserts the handover's stated contract
  where the code differs (items 1 and 3 above). Tests pin current behaviour only.
- `docs/LAUNCHER_MAP.md`: read-only inventory of every launcher (Issue 5).

Not done, and needing approval: renaming status labels (Issue 6), changing the
parser or any specification, deleting any older pathway.

## Limits

- No GUI was run: the test machine has no `tkinter`. `analyse_grid`,
  `format_report` and the Tk apps are untested.
- Git dates do not distinguish current from historical files (two commits each).
- Passing tests do not show the mathematics is established.
