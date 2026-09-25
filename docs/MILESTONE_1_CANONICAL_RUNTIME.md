# Milestone 1 — Canonical Runtime

This document records the state of the JUFE canonical Python runtime at
the close of the diagnostic-consolidation work covered by this
milestone. Every path cited below was independently verified against
the actual filesystem in this repository (via `ls`/`find`/`grep`), and
every numerical example was produced by actually executing the current
runtime — none are invented, approximated, or reconstructed from
memory. Where a verification attempt found a broken, missing, or
ambiguous reference, that is stated explicitly in
["Verification notes and open discrepancies"](#verification-notes-and-open-discrepancies)
below rather than papered over.

---

## 1. Canonical runtime entry points and execution flow

The canonical entry point is `main.py` (repository root). Its
evaluation flow, traced directly from source, is:

```
main.py
  -> src/runtime.py :: JUFERuntime.evaluate(values, ...)
    -> src/engines/abtm.py :: ABTMEngine.evaluate(values, ...)
```

`main.py` is an interactive menu loop with three choices: "Boot
Runtime" (menu option 1, which goes through
`JUFERuntime.boot()` -> `JUFERuntime.execute()` -> `src/kernel.py ::
JUFEKernel.execute_boot()` -- a *separate* specification-loading path,
unrelated to the diagnostics documented here), "Evaluate" (menu option
2, the path shown above), and "Exit" (option 3). `JUFERuntime.__init__`
(`src/runtime.py`) constructs exactly one `ABTMEngine()` instance
(`src/engines/abtm.py`), which is reused for every `evaluate()` call
made through that runtime instance.

`JUFERuntime.evaluate()` is a thin pass-through: it forwards `values`
and the four diagnostic keyword arguments (see §3 below) straight to
`self.engine.evaluate(...)` with no additional logic of its own.

---

## 2. The six-component input model

Traced directly from `src/local_state.py :: JUFELocalState`:

```python
CANONICAL_COMPONENTS = (
    "Mx", "My", "Mz",
    "Ax", "Ay", "Az",
)
```

Every Local Field State is exactly six numeric components, in this
fixed order: `Mx, My, Mz` (the compressive/"M" vector, exposed as the
`compressive` property) and `Ax, Ay, Az` (the repulsive/"A" vector,
exposed as the `repulsive` property). `JUFELocalState.__init__` raises
`ValueError` if given anything other than exactly six values, raises
`TypeError` if any value is not a real number, and raises `ValueError`
if any value is not finite. The class's own docstring states it
implements `DEF-0003 -- Six-Component Local Field State`,
`DEF-0014 -- Phase-Difference Expression`,
`DEF-0015 -- Local Phase-Equilibrium Condition`, and
`DEF-0019 -- Absolute Vacuum State` (see §11 for verified paths to
these definitions).

`ABTMEngine.evaluate(values)` (`src/engines/abtm.py`) accepts an
arbitrary-length flat sequence of numbers, splits it into
`len(values) // 6` complete six-component `JUFELocalState` instances,
and preserves any leftover `values` (fewer than six) as `remaining`
(see §5).

---

## 3. Verified examples of default evaluation and each diagnostic keyword

All output below was produced by actually running, in this task:

```python
from src.engines.abtm import ABTMEngine
engine = ABTMEngine()
engine.evaluate([3, 5, 2, 3, 5, 2])
```

### 3.1 Default evaluation (no diagnostic kwargs) -- balanced state `[3,5,2,3,5,2]`

```json
{
  "state": {
    "Mx": 3.0, "My": 5.0, "Mz": 2.0,
    "Ax": 3.0, "Ay": 5.0, "Az": 2.0,
    "cell_coordinate": null, "frame_index": null,
    "lifecycle_state": "ACTIVE", "mapping_version": "JUFE-LOCAL-1",
    "transformation": "Identity",
    "phase_difference": [0.0, 0.0, 0.0],
    "phase_equilibrium": true, "vacuum": false
  },
  "gradient": {
    "gradient": [3.0, 5.0, 2.0],
    "propagation": [-3.0, -5.0, -2.0],
    "magnitude": 6.164414002968976,
    "gradient_dominance": false
  },
  "phase": [0.0, 0.0, 0.0],
  "phase_lock": {
    "vacuum": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    "packet": { "...": "same as \"state\" above" },
    "phase_locked": true
  },
  "local_conservation": true,
  "equilibrium": true,
  "toroidal_flux": {
    "omega_t": 1.0,
    "geometry": 8.717797887081348,
    "xi": 8.717797887081348,
    "work": 8.717797887081348
  },
  "tensegrity_tensor": {
    "geometry": 6.164414002968976,
    "structural_constraint": 1.0,
    "toroidal_flux": 8.717797887081348,
    "harmonic_modulation": 1.0,
    "total": 16.882211890050325,
    "divergence_free": false
  },
  "stable": true,
  "global_conservation": { "global_sum": 20.0, "conserved": false, "residual": 20.0 },
  "harmonic_layer": { "harmonic": 0, "phase": 0.0, "modulation": 1.0 },
  "sensitivity_matrix": {
    "matrix": "6x6 identity",
    "determinant": 1.0,
    "catastrophic_transition": false
  },
  "status": "IMPLEMENTED"
}
```

No `"diagnostics"` key is present -- confirmed absent (not `null`, not
`{}`) whenever all four diagnostic kwargs are `None`, in every branch.

### 3.2 `dominance_threshold=1.0` on the unbalanced state `[3,5,2,1,4,6]`

```python
engine.evaluate([3, 5, 2, 1, 4, 6], dominance_threshold=1.0)["diagnostics"]
```

```json
{
  "dominance": {
    "compressive_norm": 6.164414002968976,
    "repulsive_norm": 7.280109889280518,
    "ratio": 0.8467473838610141,
    "threshold": 1.0,
    "threshold_basis": "PROVISIONAL",
    "dominant": false
  }
}
```

### 3.3 `phase_lock_tolerance=1.0` on the same unbalanced state

```json
{
  "phase_lock": {
    "residual": [2.0, 1.0, -4.0],
    "residual_norm": 4.58257569495584,
    "tolerance": 1.0,
    "tolerance_basis": "PROVISIONAL",
    "locked": false
  }
}
```

### 3.4 `global_balance_tolerance=1e-9` on the same unbalanced state

```json
{
  "global_balance": {
    "scalar_total": 21.0,
    "component_total": [4.0, 9.0, 8.0],
    "scalar_residual": 21.0,
    "component_residual": [4.0, 9.0, 8.0],
    "tolerance": 1e-09,
    "tolerance_basis": "PROVISIONAL",
    "scalar_balanced": false,
    "component_balanced": false
  }
}
```

### 3.5 `bifurcation_threshold=1e-9` on the same unbalanced state

```json
{
  "bifurcation": {
    "determinant": 1.0,
    "threshold": 1e-09,
    "threshold_basis": "PROVISIONAL",
    "near_bifurcation": false
  }
}
```

### 3.6 Same call via `JUFERuntime` instead of `ABTMEngine` directly

```python
from src.runtime import JUFERuntime
JUFERuntime().evaluate([3, 5, 2, 1, 4, 6], dominance_threshold=1.0)["diagnostics"]
```

produces byte-for-byte the same `"dominance"` object shown in §3.2 --
confirming the pass-through described in §1.

---

## 4. Single-state, multi-state, and remainder response shapes

### 4.1 Single complete state (exactly six values, no remainder)

`ABTMEngine.evaluate([3,5,2,3,5,2])` takes the "flattened single-state"
branch: one dict with every per-state field
(`state`, `gradient`, `phase`, `phase_lock`, `local_conservation`,
`equilibrium`, `toroidal_flux`, `tensegrity_tensor`, `stable`) plus the
run-level fields (`global_conservation`, `harmonic_layer`,
`sensitivity_matrix`, `status`) merged directly into the same dict --
shown in full in §3.1. When a diagnostic is requested in this branch,
`diagnostics.dominance` / `diagnostics.phase_lock` are unwrapped single
objects (not one-element lists).

### 4.2 Multi-state (twelve values, two complete states, no remainder)

Executed:

```python
engine.evaluate([3, 5, 2, 3, 5, 2, 3, 5, 2, 1, 4, 6])
```

Top-level keys (verified):

```python
['complete_states', 'global_conservation', 'harmonic_layer',
 'remaining', 'remaining_count', 'sensitivity_matrix', 'states', 'status']
```

with `complete_states == 2`, `remaining == []`, `remaining_count == 0`
(the `"states"` list holds one per-state result dict per complete
state; `"remaining"`/`"remaining_count"` keys are present -- not
omitted -- even though there is nothing left over). When a diagnostic
is requested in this branch, `diagnostics.dominance` and
`diagnostics.phase_lock` are lists of length `complete_states`, in the
same order as `states[]`; `diagnostics.global_balance` and
`diagnostics.bifurcation` are single objects, each computed once across
the whole call (see §5, §6).

### 4.3 Remainder (input not a multiple of six)

Executed:

```python
engine.evaluate([3, 5, 2, 3, 5, 2, 7, 8, 9], global_balance_tolerance=1e-9)
```

Result: `remaining == [7, 8, 9]`, `remaining_count == 3`,
`complete_states == 1`, one entry in `"states"`.
`global_conservation == {"global_sum": 20.0, "conserved": false, "residual": 20.0}`
and `diagnostics["global_balance"]["scalar_total"] == 20.0` -- both
computed from the one complete state alone (see §5).

### 4.4 Short input (fewer than six values)

`ABTMEngine.evaluate([1, 2, 3])` raises
`ValueError("At least six values are required.")` -- unaffected by any
diagnostic kwarg, since the length check runs before any diagnostic
kwarg is consulted.

---

## 5. Remainder values are excluded from diagnostics

Verified directly (§4.3): for `[3,5,2,3,5,2, 7,8,9]`, both the existing
`global_conservation.global_sum` field and the new
`diagnostics.global_balance.scalar_total` field equal `20.0` --
exactly the sum contributed by the one complete state `[3,5,2,3,5,2]`
alone. The 3-value remainder `[7, 8, 9]` is never converted into a
`JUFELocalState` (it is too short) and never enters either
calculation. This was further verified with a dedicated regression
test (`tests/test_evaluate_diagnostics_integration.py ::
RemainderExclusionTests.test_fifteen_value_input_diagnostics_cover_only_complete_states_and_ignore_remainder`)
which evaluates two 15-value inputs sharing the same 12 leading values
but different 3-value remainders and asserts the resulting
`"diagnostics"` mappings are identical between the two calls -- proving
the remainder content has zero effect on any diagnostic, not just that
its value happens to be excluded from one field.

---

## 6. The bifurcation determinant remains 1.0

`ABTMEngine.__init__` constructs `self.sensitivity = JUFESensitivityMatrix()`
with no matrix argument (`src/engines/abtm.py`). `JUFESensitivityMatrix.__init__`
(`src/sensitivity_matrix.py`) defaults to `self.matrix = np.identity(6)`
when no matrix is supplied. Nothing in `ABTMEngine.evaluate()` ever
replaces or mutates `self.sensitivity.matrix` -- the same instance,
holding the same fixed 6x6 identity matrix, is reused for every
`evaluate()` call for the lifetime of the engine.

`diagnostics.bifurcation` calls `self.sensitivity.evaluate_bifurcation(threshold=...)`,
which computes `det(self.matrix)`. Since `self.matrix` never changes
and never depends on the evaluated `values`, this determinant is
**sequence-independent** -- verified by executing it against three
very different inputs in this task:

```python
engine.evaluate([3, 5, 2, 3, 5, 2],           bifurcation_threshold=1e-9)["diagnostics"]["bifurcation"]["determinant"]  # 1.0
engine.evaluate([0, 0, 0, 0, 0, 0],           bifurcation_threshold=1e-9)["diagnostics"]["bifurcation"]["determinant"]  # 1.0
engine.evaluate([-9, 4, 100, -3, 0.5, 7],     bifurcation_threshold=1e-9)["diagnostics"]["bifurcation"]["determinant"]  # 1.0
```

All three return `1.0`, and `engine.sensitivity.matrix == numpy.identity(6)`
was confirmed `True` in the same run.

---

## 7. `JUFETransformation.apply_coupled_field_step()` -- separate, not wired in

`src/transformation.py :: JUFETransformation.apply_coupled_field_step(self, state, compressive_rate, *, dt)`
is a native port of the coupled-field evolution rule, added as an
opt-in method and confirmed, in this task, to still not be called from
anywhere in `src/engines/abtm.py` (`grep -rn "apply_coupled_field_step" src/engines/abtm.py`
returns no matches) -- `ABTMEngine.evaluate()` calls only
`self.transformation.apply(state)` (the identity mapping).

Its governing equation, as documented on the method itself:

```
dM/dt = -dA/dt

Therefore, for one explicit step of size dt:
    M_next = M + dM/dt * dt
    A_next = A - dM/dt * dt
```

This matches `DEF-0013 -- Coupled Field Evolution`
(`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/MASTER_DEFINITION_INDEX.md`),
whose status is explicitly recorded as **"EXPLICIT EQUATION / PARTIALLY
DEFINED DYNAMICS"**, and whose own "Unresolved" list states plainly:

> - explicit right-hand-side evolution function;
> - integration scheme and timestep;
> - time units;
> - initial and boundary conditions;
> - convergence proof;
> - role of Lemma 3.1 in producing phase convergence.

Stated plainly for this runtime: **none of the following are resolved
by the current implementation, and this is a known open question, not
a defect to fix**:

- **Rate source**: `compressive_rate` (`dM/dt`) is supplied entirely by
  the caller with no defined origin -- there is no function in this
  codebase that derives it from a state, a field, or any other input.
- **Timestep meaning/units**: `dt` is validated only as "finite and
  non-negative"; it carries no defined physical unit or manuscript-tied
  meaning.
- **Activation trigger**: nothing decides *when* a coupled step should
  be applied -- the method must be called explicitly by a caller.
- **Iteration**: the method performs exactly one explicit step per
  call; there is no loop, no multi-step integrator, and no notion of
  simulation time accumulation anywhere in `src/`.
- **Stopping rule**: there is no convergence check or termination
  condition -- the manuscript's own stated convergence mechanism
  ("cross-axial helical deflection") is explicitly named in DEF-0013 as
  *not* specified by the differential equation alone.

---

## 8. Classification table

| Category | Examples | Basis |
|---|---|---|
| **Implemented mathematics** (real, tested, working computation, always active) | Identity transformation (`src/transformation.py::apply`); local conservation exact-equality check (`src/conservation.py`); local phase equilibrium / phase-difference (`src/local_state.py`); point-value gradient and its magnitude/dominance (`src/field_gradient.py::gradient/magnitude/dominant`); toroidal work term (`src/toroidal_flux.py`); tensegrity total (`src/tensegrity_stress_tensor.py`); global conservation scalar sum (`src/global_conservation.py::total_field/verify/residual/to_dict`); sensitivity-matrix application/determinant (`src/sensitivity_matrix.py::apply/determinant/catastrophic_transition`) | Exercised by `tests/test_abtm_evaluate_baseline.py` and confirmed unchanged throughout this milestone |
| **Provisional caller-supplied diagnostics** (real computation, explicitly provisional threshold basis) | `evaluate_dominance` (`src/field_gradient.py`), `evaluate_phase_lock` (`src/phase_lock.py`), `global_field_balance` (`src/global_conservation.py`), `evaluate_bifurcation` (`src/sensitivity_matrix.py`) -- each returns a `..._basis: "PROVISIONAL"` field | Each method's own docstring; REQ-TH-001, REQ-TR-002/TR-PHASE-001, REQ-INV-002 (global balance's "open_questions": ["Whether scalar balance alone is sufficient"], `JUFE_ABTM_SPEC_ENGINE/requirements_register.json`), DEF-0036/REQ-TR-004 (see §11) |
| **Characterization-only existing behavior** (documented "this is what it does," not a correctness claim) | Negative-zero propagation in `gradient.propagation` for the all-zero/vacuum input (`(-0.0, -0.0, -0.0)`, from `-k * 0.0`); `lifecycle_state` stays `"ACTIVE"` even for the six-zero vacuum input (`ABTMEngine.evaluate()` never passes `lifecycle_state="VACUUM"` to `JUFELocalState`); `tensegrity_tensor.divergence_free` is `false` even for the vacuum input (see §9); `phase_lock` is `null`, not a dict, whenever the state is not phase-locked | `tests/test_abtm_evaluate_baseline.py` (module and per-class docstrings) |
| **Topology-blocked operations** | 64-cell field frame / grid mapping -- `REQ-MAP-001`, status `"provisional"`, `implemented_by: ["jufe_64_grid_mapper"]` (a **legacy** root-level script, not in `src/`), `open_questions: ["One scalar, one subgroup, or one six-component state per cell", "Third-axis representation", "Neighbour topology", "Boundary topology"]` | `JUFE_ABTM_SPEC_ENGINE/requirements_register.json`; confirmed no topology/grid implementation exists anywhere under `src/` (`grep -rl topology src/` matches only this milestone's own docstring prose in `src/field_gradient.py`/`src/phase_lock.py`, which explicitly documents the *absence* of topology handling, not an implementation of it) |
| **Unresolved manuscript mathematics** | `DEF-0036` (Bifurcation Criterion); `REQ-TR-004` (Bifurcation); `REQ-TH-001` (Local gradient dominance); `DEF-0007` (Local Gradient Dominance); `REQ-TR-002` (Phase lock); `TR-PHASE-001` (Phase-lock condition); `DEF-0013` (Coupled Field Evolution, §7) | See §11 for verified paths and exact quoted wording (already quoted in the docstrings of `src/sensitivity_matrix.py`, `src/field_gradient.py`, `src/phase_lock.py`, `src/transformation.py`) |

---

## 9. Proven current limitations

Each item below was re-verified against actual current source in this
task, not merely restated from the task description.

1. **Current gradient is a point value, not a spatial derivative.**
   `src/field_gradient.py :: JUFEFieldGradient.gradient(self, state)`
   (line 40) returns `(state.mx, state.my, state.mz)` directly -- the
   compressive vector of the one supplied state, with no neighbouring
   cells, no finite-difference computation, and no spatial sampling of
   any kind involved.

2. **Harmonic modulation remains `1.0`.**
   `src/harmonic_layer.py :: JUFEHarmonicLayer.__init__` defaults
   `harmonic: int = 0`; `modulation_factor()` (line 49) returns
   `math.cos(self.phase())`, and `phase()` is `2*pi*harmonic/7`, which
   is `0.0` when `harmonic == 0`, so `modulation_factor() == cos(0) == 1.0`.
   `ABTMEngine.__init__` constructs `self.harmonics = JUFEHarmonicLayer()`
   with no argument (harmonic stays `0`), and `grep -n
   "advance\|set_harmonic" src/engines/abtm.py` returns **no matches**
   -- nothing in `evaluate()` ever changes the harmonic index. Verified
   by execution: every example in §3 shows `"harmonic_layer":
   {"harmonic": 0, "phase": 0.0, "modulation": 1.0}`.

3. **Structural constraint remains `1.0` under the identity
   transformation.** `src/engines/abtm.py` builds
   `TensegrityTensor(..., structural_constraint=float(conserved), ...)`
   where `conserved = self.conservation.verify(state, transformed)`.
   Because the only transformation ever applied is the identity mapping
   (`src/transformation.py :: apply`), `transformed.values == state.values`
   always, so `JUFEConservation.verify` (`src/conservation.py`) returns
   `True` for every currently reachable input, making
   `structural_constraint == float(True) == 1.0` in every executed
   example in §3.

4. **Toroidal geometry, xi, and work are always identical to one
   another for a given state** (not constant across different states --
   verified they DO vary with the input, e.g. `8.717797887081348` for
   the balanced fixture vs. `9.539392014169456` for the unbalanced
   fixture in earlier executed captures; what stays fixed is the
   *relationship between the three fields*). `src/toroidal_flux.py ::
   JUFEToroidalFlux.__init__` defaults `omega_t: float = 1.0`, and
   `ABTMEngine.__init__` constructs `self.toroidal_flux =
   JUFEToroidalFlux()` with no argument, so `omega_t` is always `1.0`.
   Since `xi(state) = omega_t * geometric_factor(state)` and
   `work(state) = xi(state)`, and `omega_t` never varies, `geometry ==
   xi == work` holds for every call in the current runtime. Confirmed
   by execution in every example in §3 (e.g. all three fields equal
   `8.717797887081348` for the balanced fixture).

5. **Current stress tensor is a scalar placeholder.**
   `src/tensegrity_stress_tensor.py :: TensegrityTensor` (line 7) is a
   `@dataclass` with exactly four scalar `float` fields (`geometry`,
   `structural_constraint`, `toroidal_flux`, `harmonic_modulation`) and
   a `total()` that simply adds them -- there is no matrix, no rank-2
   tensor structure, and no per-axis/per-component decomposition
   anywhere in this class.

6. **Current `divergence_free` can never return `True`.**
   `TensegrityTensor.divergence_free(self, tolerance=1e-12)` (line 49)
   returns `abs(self.total()) <= tolerance`. Given limitations 2 and 3
   above, under the currently reachable identity-transformation path
   `structural_constraint` is always `1.0` and `harmonic_modulation` is
   always `1.0`; since `geometry` and `toroidal_flux` are both
   non-negative square-root-based quantities, `total()` is therefore
   always at least `2.0` (structural_constraint `1.0` + harmonic_modulation
   `1.0`, at minimum) -- far larger than the `1e-12` tolerance. Verified
   by execution: every example in §3 shows
   `"divergence_free": false`, including the six-zero vacuum input
   (`geometry == 0.0`, `toroidal_flux == 0.0`, `structural_constraint
   == 1.0`, `harmonic_modulation == 1.0`, `total == 2.0`,
   `divergence_free == false`) -- the case where a reader might most
   expect `True`.

---

## 10. Test verification

Both invocation forms were executed in this task and both produced the
same result:

```
$ ./.venv/bin/python -m unittest discover -s tests
......................................................................
......................................................................
......................................................................
......................................................................
......................................................................
...
----------------------------------------------------------------------
Ran 215 tests in 0.030s

OK
```

```
$ .venv/bin/python3 -m unittest tests.test_boot_validation \
    tests.test_abtm_evaluate_baseline tests.test_z6_equivalence \
    tests.test_coupled_field_step tests.test_global_field_balance \
    tests.test_sensitivity_bifurcation tests.test_field_gradient_dominance \
    tests.test_phase_lock_l2_norm tests.test_evaluate_diagnostics_integration
----------------------------------------------------------------------
Ran 215 tests in 0.044s

OK
```

**Result: 215 tests, 0 failures, 0 errors**, confirmed at commit
`d4c6b72b759a25a5046f278eeba590fa6b97fc4c` -- verified as the actual
current `HEAD` via `git rev-parse HEAD` in this task, immediately
before this documentation was written (no code or test changes were
made in this documentation task).

---

## 11. Exact canonical paths

Every path below was confirmed to exist on disk in this task (via
`ls`/`grep`/`find`), not assumed.

**Definitions** (`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/01_MASTER_INDEX/`):

- `MASTER_DEFINITION_INDEX.md` -- contains, among others: `DEF-0003`
  (Six-Component Local Field State, line 90), `DEF-0013` (Coupled Field
  Evolution, line 394), `DEF-0014` (Phase Residual, line 447),
  `DEF-0036` (Bifurcation Criterion, line 1105). `DEF-0036` has **no**
  dedicated individual file in `DEFINITIONS/` (verified: only present
  as an inline section of this index file).
- `DEFINITIONS/DEF-0007_Local_Gradient_Dominance.md` -- dedicated file,
  confirmed present.
- `DEFINITIONS/DEF-0015_Phase_Lock.md`,
  `DEFINITIONS/DEF-0019_Absolute_Vacuum_State.md` -- dedicated files,
  confirmed present.

**Requirements** (`JUFE_ABTM_SPEC_ENGINE/requirements_register.json`,
confirmed present): contains, among others, `REQ-TR-002` (Phase lock),
`REQ-TR-004` (Bifurcation), `REQ-TH-001` (Local gradient dominance),
`REQ-INV-002` (Global tensegrity equilibrium), `REQ-MAP-001` (64-cell
field frame, topology-blocked -- see §8). Human-readable mirror:
`JUFE_ABTM_SPEC_ENGINE/SPECIFICATION_REPORT.txt` (confirmed present).

**Formal rules** (`JUFE_ABTM_SPEC_LAYER/`, confirmed present):
`abtm_specification.py` (defines the `RuleSpec` dataclass and every
`rule_id=` entry, including `TR-PHASE-001` at line 386, and `TR-JAM-001`
immediately after it) and its generated/mirrored JSON,
`JUFE_ABTM_CORE_SPEC.json` (`TR-PHASE-001` at line 196).

**Runtime specifications** (`Specifications/`, confirmed present):
`SPEC-010.md` (the specification `src/runtime.py :: JUFERuntime.boot()`
literally loads, via `self.execute("Specifications/SPEC-010.md")`);
also present in this directory: `SPEC-001.md`, `SPEC-020.md`,
`SPEC-030.md`, `SPEC-040.md`, and `SPEC-000: JUFE Architecture Index.md`.

**Volume III chapters** (`JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/02_SPECIFICATION/Volume_III/`,
confirmed present): `Chapter_1_Field_State.md`,
`Chapter_5_Post_Phase_Lock_Mechanics.md`,
`Chapter_7_Unified_ABTM_Field_Equations.md`,
`00-Normative-Traceability-Matrix.md`, `SPECIFICATION_INDEX.md`,
`README.md`. (An older, separately-named backup copy of this same
directory also exists at
`_JUFE_AUTOFIX_BACKUP_20260727-061258/Volume_III/` -- not cited as
canonical here; see §12 for why.)

**Manuscript sources** (`JUFE_RESEARCH/TOOLS/SOURCES/MANUSCRIPTS/CANONICAL/`,
confirmed present): includes
`TFJ-Volume-III-Ch01-Singularity-Synthesis-and-Planck-Scale-Horizon.md`,
`TFJ-Volume-III-Ch03-Horizon-Dependent-Shifting.md`,
`TFJ-Volume-IV-Hysteresis-and-Emergent-Evolution.md`, and
`TFJ-Unified-Harmonic-Manifold-Comprehensive-Synthesis.md`.

---

## 12. Verification notes and open discrepancies

- **`Specifications/Manuscript 002` is an empty directory.** Multiple
  `src/` docstrings (`src/sensitivity_matrix.py`, `src/harmonic_layer.py`)
  cite "Manuscript 002" as their mathematical source, and a directory
  literally named `Manuscript 002` exists at `Specifications/Manuscript 002`
  -- but `ls -la` on it in this task shows it contains **zero files**.
  This is reported here explicitly as a broken/incomplete reference
  rather than silently treated as resolved: the *name* "Manuscript 002"
  is real and consistently used across source, but no manuscript
  document currently backs it at that path in this repository snapshot.
- **The backup copy of Volume III
  (`_JUFE_AUTOFIX_BACKUP_20260727-061258/Volume_III/`) is not treated as
  canonical.** Both it and
  `JUFE_DEPENDENCY_COMPLETION_FRAMEWORK/02_SPECIFICATION/Volume_III/`
  exist and appear to hold the same chapter files; the
  `_JUFE_AUTOFIX_BACKUP_...` directory name self-identifies as a backup,
  so §11 cites only the `02_SPECIFICATION/Volume_III/` copy.

---

## 13. The nine-commit chain, corrected to eight

The task instructions for this milestone referred to a "nine-commit
diagnostic-consolidation arc" spanning `929c49b` through `d4c6b72`, and
asked that this be verified against `git log` rather than assumed,
specifically noting that `929c49b` was already `HEAD` in the git status
shown at the very start of this whole multi-task session (before any
work in this session began).

Verified via `git log --format="%H %ci %s"`:

```
d4c6b72 2026-09-25 21:17:20 -0700  Expose opt-in diagnostics through JUFE runtime
13f32d9 2026-09-25 03:35:51 -0700  Add opt-in L2 phase-lock reporting
fe2e034 2026-09-25 03:09:40 -0700  Add opt-in explicit-threshold dominance reporting
0bb8f11 2026-09-24 20:20:31 -0700  Add opt-in sensitivity bifurcation reporting
b16cf34 2026-09-24 18:07:27 -0700  Add component-wise global balance to canonical runtime
95fa900 2026-09-24 15:24:36 -0700  Port coupled field evolution into canonical runtime
8e64d4a 2026-09-24 13:05:39 -0700  Add JUFE Z6 equivalence tests
d1e470b 2026-09-24 12:13:18 -0700  Add JUFE canonical runtime baseline tests
929c49b 2026-09-24 02:32:49 -0700  Fix JUFE boot specification validation
```

`929c49b` ("Fix JUFE boot specification validation") is a genuinely
separate, unrelated piece of work: it touches `src/runtime.py`,
`src/validator.py`, and adds `tests/test_boot_validation.py`, fixing a
specification-loading defect -- not part of the diagnostic
consolidation. It was committed at `02:32:49`, roughly ten hours before
`d1e470b` (`12:13:18`), the first commit of the actual
diagnostic-consolidation arc, confirming it predates this arc's start
rather than opening it.

**The accurate diagnostic-consolidation chain is eight commits,
`d1e470b` through `d4c6b72`:**

| # | Commit | Message |
|---|---|---|
| 1 | `d1e470b` | Add JUFE canonical runtime baseline tests |
| 2 | `8e64d4a` | Add JUFE Z6 equivalence tests |
| 3 | `95fa900` | Port coupled field evolution into canonical runtime |
| 4 | `b16cf34` | Add component-wise global balance to canonical runtime |
| 5 | `0bb8f11` | Add opt-in sensitivity bifurcation reporting |
| 6 | `fe2e034` | Add opt-in explicit-threshold dominance reporting |
| 7 | `13f32d9` | Add opt-in L2 phase-lock reporting |
| 8 | `d4c6b72` | Expose opt-in diagnostics through JUFE runtime |

This is reported here as a correction, per this task's own explicit
instruction to verify rather than assume: counting inclusively from
`929c49b` through `d4c6b72` does arithmetically total nine commits, but
`929c49b` is not part of this arc's own work and its inclusion is not
accurate history.

---

## 14. Canonical runtime vs. the historical/legacy path

The canonical runtime is exclusively `main.py -> src/runtime.py ::
JUFERuntime -> src/engines/abtm.py :: ABTMEngine`, together with the
`src/` modules `ABTMEngine` composes (`transformation.py`,
`conservation.py`, `global_conservation.py`, `equilibrium.py`,
`field_gradient.py`, `phase_lock.py`, `toroidal_flux.py`,
`sensitivity_matrix.py`, `harmonic_layer.py`,
`tensegrity_stress_tensor.py`, `local_state.py`).

`abtm_expansion.py` and `oldmate1(5).py` (both at the repository root)
are a **separate, historical/legacy implementation path**, not part of
the canonical runtime. `oldmate1(5).py` is not even independently
importable -- its `ABTM_Engine` class references an `ABTM_Expansion`
base class it never imports, requiring external injection (the pattern
this session's own test files reuse from the repository's pre-existing
launcher scripts, e.g. `jufe_original_launcher.py`). In this session,
`abtm_expansion.py` and `oldmate1(5).py` were used **exclusively** from
test files (`tests/test_z6_equivalence.py`,
`tests/test_coupled_field_step.py`, `tests/test_global_field_balance.py`,
`tests/test_sensitivity_bifurcation.py`,
`tests/test_field_gradient_dominance.py`,
`tests/test_phase_lock_l2_norm.py`), as a comparison/parity target to
prove the native `src/` ports behave identically to the legacy
functions they were derived from -- never as production dependencies.
No file under `src/` imports `abtm_expansion` or executes
`oldmate1(5).py` at runtime. The Explorer launcher files
(`jufe_explorer.py`, `Start JUFE Explorer.command`,
`JUFE Explorer - READ ME.txt`) are a further separate, pre-existing
tool, untouched by and unrelated to this milestone's work.
