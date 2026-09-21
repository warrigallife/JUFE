# Answers

Fill in by editing this file (pencil icon). Put an `x` inside the brackets, like `[x]`.
Anything you leave blank we will treat as "not decided".

## JUFE

### 1. Starting JUFE (the "Boot" option) stops with "no executable definitions"

The start-up check reads `Specifications/SPEC-010.md` and needs lines starting with
`DEF-` in it. The copy on GitHub has none.

- [ ] My Mac copy of `SPEC-010.md` is different and has `DEF-` lines — I uploaded it to `incoming/`
- [ ] Boot should read a different file. Which one? ______________________
- [ ] Boot should accept more than lines starting with `DEF-`
- [ ] Not sure

### 2. The Explorer files

- [ ] I uploaded the three Explorer files to `incoming/` (step 2 in `START_HERE.md`)
- [ ] Not ready yet — I will do it later
- [ ] The Explorer should not be shared

### 3. The 64-cell grid: what does one cell hold?

`jufe_64_grid_mapper.py` puts **one value** in each cell. The handover says a cell holds
**six values** (one local state), so 384 values fill one 8×8 frame.

- [ ] One value per cell (the mapper is right)
- [ ] Six values per cell (the handover is right)
- [ ] It depends / not decided yet — notes: ______________________

### 4. The word "stable" and the status `IMPLEMENTED`

`IMPLEMENTED` is printed every time the engine runs. And "stable" currently means two
different checks: (a) the matrix trace mod 6 equals 0, or (b) conservation and
equilibrium both hold.

`IMPLEMENTED` should mean:

- [ ] "the code ran" (nothing more)
- [ ] something weaker, such as `PROVISIONAL`
- [ ] other: ______________________

"Stable" should mean:

- [ ] (a) trace mod 6 equals 0
- [ ] (b) conservation and equilibrium
- [ ] both, under two different names

### 5. Which launcher is the normal way in?

- [ ] `python main.py`
- [ ] `Start JUFE.command` (runs `jufe_original_launcher.py`)
- [ ] The new Explorer
- [ ] Other: ______________________

### 6. A stray old copy of the engine exists at `src/src/engines/abtm.py` (version 2.3.0)

Nothing will be deleted until you say so.

- [ ] Keep it for now
- [ ] Retire it (you confirm it is not needed)
- [ ] Not sure

### 7. Tom

- Who is Tom, and how can we reach them? ______________________
- Which rules or decisions are Tom's to supply? ______________________

## Warrigal research suite

### 8. Where is the rest of the work?

Your handover describes branch `warrigal-foundation-01` (commit `a7d1685`) and about 250
tests. GitHub has only `main`, with 179 tests and an empty README.

- [ ] The rest is still on my Mac — I will upload it
- [ ] The handover numbers were an earlier count
- [ ] Not sure

### 9. A missing requirement

Three Instagram tests need a package called `instaloader`, which is used by the code
but not listed in `pyproject.toml`. May we add it to the list?

- [ ] Yes
- [ ] No
- [ ] Not sure

### 10. Versions on your Mac

- Python version: ______________________
- NumPy version: ______________________

## Permission

May we send our changes to your repositories as separate branches or pull requests, for
you to accept or refuse?

- [ ] Yes, separate branches / pull requests are fine
- [ ] Ask me each time
- [ ] No

## Anything else you want us to know

______________________
