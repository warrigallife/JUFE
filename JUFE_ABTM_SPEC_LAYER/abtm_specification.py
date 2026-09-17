"""
JUFE / ABTM Formal Specification
================================

This module is a formal software specification derived from the supplied
JUFE / ABTM manuscripts. It does not claim experimental validation and does
not edit or replace any original JUFE source file.

Purpose
-------
- Give every manuscript rule a stable identifier.
- Separate explicitly defined mathematics from unresolved implementation choices.
- Declare required inputs and outputs for each rule.
- Provide machine-readable metadata for launchers, engines, and audit records.
- Allow later rules to be added without rewriting existing rules.

Status categories
-----------------
EXPLICIT:
    Directly stated by the supplied manuscript/equations.

NUMERICAL_CONVENTION:
    Required by software but not numerically fixed by the manuscript,
    such as tolerances and finite thresholds.

PROVISIONAL_MAPPING:
    A temporary data representation chosen for software use and clearly
    marked as not yet dictated by the manuscript.

UNRESOLVED:
    A required definition that has not yet been supplied.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Mapping, Sequence


class SpecificationStatus(str, Enum):
    EXPLICIT = "explicit"
    NUMERICAL_CONVENTION = "numerical_convention"
    PROVISIONAL_MAPPING = "provisional_mapping"
    UNRESOLVED = "unresolved"


class RuleKind(str, Enum):
    DEFINITION = "definition"
    AXIOM = "axiom"
    EQUATION = "equation"
    INVARIANT = "invariant"
    TRANSITION = "transition"
    SOFTWARE_CONTRACT = "software_contract"


@dataclass(frozen=True)
class VariableSpec:
    symbol: str
    meaning: str
    shape: str
    units: str | None = None
    status: SpecificationStatus = SpecificationStatus.EXPLICIT
    notes: str = ""
    source_section: str = ""


@dataclass(frozen=True)
class RuleSpec:
    rule_id: str
    title: str
    kind: RuleKind
    status: SpecificationStatus
    mathematical_form: str
    description: str
    required_inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    software_contract: tuple[str, ...]
    unresolved_items: tuple[str, ...] = ()
    source_section: str = ""


@dataclass(frozen=True)
class ParameterSpec:
    name: str
    meaning: str
    default: float | int | None
    status: SpecificationStatus
    constraints: str
    source_basis: str


@dataclass(frozen=True)
class GridSpec:
    rows: int
    columns: int
    cell_count: int
    cell_state_components: tuple[str, ...]
    full_frame_value_count: int
    spatial_mapping_status: SpecificationStatus
    notes: tuple[str, ...] = ()


@dataclass
class ABTMSpecification:
    name: str
    version: str
    variables: dict[str, VariableSpec] = field(default_factory=dict)
    rules: dict[str, RuleSpec] = field(default_factory=dict)
    parameters: dict[str, ParameterSpec] = field(default_factory=dict)
    grid: GridSpec | None = None

    def register_variable(self, spec: VariableSpec) -> None:
        if spec.symbol in self.variables:
            raise ValueError(f"Variable already registered: {spec.symbol}")
        self.variables[spec.symbol] = spec

    def register_rule(self, spec: RuleSpec) -> None:
        if spec.rule_id in self.rules:
            raise ValueError(f"Rule already registered: {spec.rule_id}")
        self.rules[spec.rule_id] = spec

    def register_parameter(self, spec: ParameterSpec) -> None:
        if spec.name in self.parameters:
            raise ValueError(f"Parameter already registered: {spec.name}")
        self.parameters[spec.name] = spec

    def unresolved(self) -> dict[str, Any]:
        unresolved_rules = {
            rule_id: list(rule.unresolved_items)
            for rule_id, rule in self.rules.items()
            if rule.unresolved_items
        }

        unresolved_parameters = {
            name: asdict(parameter)
            for name, parameter in self.parameters.items()
            if parameter.status == SpecificationStatus.UNRESOLVED
        }

        unresolved_variables = {
            symbol: asdict(variable)
            for symbol, variable in self.variables.items()
            if variable.status == SpecificationStatus.UNRESOLVED
        }

        return {
            "rules": unresolved_rules,
            "parameters": unresolved_parameters,
            "variables": unresolved_variables,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "variables": {
                key: asdict(value)
                for key, value in self.variables.items()
            },
            "rules": {
                key: asdict(value)
                for key, value in self.rules.items()
            },
            "parameters": {
                key: asdict(value)
                for key, value in self.parameters.items()
            },
            "grid": asdict(self.grid) if self.grid else None,
            "unresolved": self.unresolved(),
        }


def build_core_specification() -> ABTMSpecification:
    spec = ABTMSpecification(
        name="JUFE / ABTM Core Specification",
        version="0.1.0",
    )

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    variables = [
        VariableSpec(
            symbol="M",
            meaning="Inward compressive field",
            shape="3-component vector per local field state: (Mx, My, Mz)",
            source_section="Local Gradient Dominance",
        ),
        VariableSpec(
            symbol="A",
            meaning="Outward repulsive field",
            shape="3-component vector per local field state: (Ax, Ay, Az)",
            source_section="Local Gradient Dominance",
        ),
        VariableSpec(
            symbol="Psi",
            meaning="Combined manifold state",
            shape="6-component local state: (Mx, My, Mz, Ax, Ay, Az)",
            notes="This is the least-assumptive software composition of M in R3 and A in R3.",
        ),
        VariableSpec(
            symbol="D",
            meaning="Instantaneous propagation vector",
            shape="3-component vector",
        ),
        VariableSpec(
            symbol="S",
            meaning="Sensitivity matrix mapping external perturbations to manifold response",
            shape="m x n numerical matrix",
        ),
        VariableSpec(
            symbol="delta_E",
            meaning="External perturbation vector",
            shape="n-component vector",
        ),
        VariableSpec(
            symbol="T_total",
            meaning="Total tensegrity-stress tensor",
            shape="square rank-2 tensor or spatial tensor field",
        ),
        VariableSpec(
            symbol="C_jam",
            meaning="Jammed local field cell",
            shape="cell state object",
        ),
        VariableSpec(
            symbol="Phi_ejected",
            meaning="Preserved structural information ejected after phase lock",
            shape="same information content as source structural state",
        ),
        VariableSpec(
            symbol="Omega_T",
            meaning="Master toroidal phase-lock frequency",
            shape="scalar",
            status=SpecificationStatus.UNRESOLVED,
            notes="Meaning supplied; numerical units and operational formula remain unresolved.",
        ),
    ]

    for variable in variables:
        spec.register_variable(variable)

    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------

    parameters = [
        ParameterSpec(
            name="equilibrium_tolerance",
            meaning="Numerical tolerance for zero-valued conservation residuals",
            default=1e-9,
            status=SpecificationStatus.NUMERICAL_CONVENTION,
            constraints="finite and >= 0",
            source_basis="Software cannot test exact floating-point equality robustly.",
        ),
        ParameterSpec(
            name="phase_lock_tolerance",
            meaning="Numerical tolerance for ||M - A|| approaching zero",
            default=1e-9,
            status=SpecificationStatus.NUMERICAL_CONVENTION,
            constraints="finite and >= 0",
            source_basis="The manuscript specifies a limit, not a finite software threshold.",
        ),
        ParameterSpec(
            name="dominance_threshold",
            meaning="Threshold representing ||M|| much greater than ||A||",
            default=None,
            status=SpecificationStatus.UNRESOLVED,
            constraints="finite and > 1 when supplied",
            source_basis="The manuscript uses the qualitative relation 'much greater than'.",
        ),
        ParameterSpec(
            name="resistance_threshold",
            meaning="Finite software threshold approximating an infinite resistance gradient",
            default=None,
            status=SpecificationStatus.UNRESOLVED,
            constraints="finite and >= 0 when supplied",
            source_basis="The manuscript states gradient approaches infinity.",
        ),
        ParameterSpec(
            name="tension_capacity",
            meaning="Maximum local cell tension capability",
            default=None,
            status=SpecificationStatus.UNRESOLVED,
            constraints="finite and >= 0 when supplied",
            source_basis="Maximum tension is named but not numerically fixed.",
        ),
        ParameterSpec(
            name="coupling_constant_k",
            meaning="Coupling coefficient in D = -k grad(M)",
            default=1.0,
            status=SpecificationStatus.NUMERICAL_CONVENTION,
            constraints="finite",
            source_basis="Equation supplies k but not its value or units.",
        ),
        ParameterSpec(
            name="time_step",
            meaning="Discrete integration interval for coupled M/A evolution",
            default=None,
            status=SpecificationStatus.UNRESOLVED,
            constraints="finite and > 0 when supplied",
            source_basis="Differential equation supplied without a numerical integration interval.",
        ),
    ]

    for parameter in parameters:
        spec.register_parameter(parameter)

    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------

    rules = [
        RuleSpec(
            rule_id="DEF-M6-001",
            title="Six-component local manifold state",
            kind=RuleKind.DEFINITION,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="Psi = (Mx, My, Mz, Ax, Ay, Az)",
            description="A local manifold state couples a three-component compressive field and a three-component repulsive field.",
            required_inputs=("M", "A"),
            outputs=("Psi",),
            software_contract=(
                "M must contain exactly three finite numerical components.",
                "A must contain exactly three finite numerical components.",
                "Psi must preserve component order and values.",
            ),
            source_section="Intersecting Space-Field Matrix M^6",
        ),
        RuleSpec(
            rule_id="AX-GRAD-001",
            title="Gradient autonomy",
            kind=RuleKind.AXIOM,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="D = -k grad(M)",
            description="Propagation is determined by the local compressive-field gradient rather than particle identity or hardcoded trajectories.",
            required_inputs=("M spatial field", "coupling_constant_k", "spatial spacing"),
            outputs=("D",),
            software_contract=(
                "Propagation direction must be computed from the supplied gradient.",
                "No branch may select direction from matter/antimatter labels.",
            ),
            unresolved_items=(
                "Boundary conditions for gradient evaluation.",
                "Exact spatial embedding of the third axis in an 8 x 8 representation.",
            ),
            source_section="1.1 Mathematical Formulation of the Gradient Field",
        ),
        RuleSpec(
            rule_id="INV-DUAL-001",
            title="Absolute conservation of field duality",
            kind=RuleKind.INVARIANT,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="dM/dt = -dA/dt",
            description="Changes in compressive and repulsive fields must be equal and opposite.",
            required_inputs=("M", "A", "dM/dt", "time_step"),
            outputs=("M_next", "A_next", "conservation_residual"),
            software_contract=(
                "The update must preserve dM + dA = 0 within tolerance.",
                "No field information may be silently discarded.",
            ),
            unresolved_items=("Numerical integration scheme beyond an explicit first-order step.",),
            source_section="2.1 The Boundary Jam Equation",
        ),
        RuleSpec(
            rule_id="INV-GLOBAL-001",
            title="Global tensegrity equilibrium",
            kind=RuleKind.INVARIANT,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="sum_global sum_i(M_i + A_i) = 0",
            description="The global scalar field balance remains zero.",
            required_inputs=("all local M states", "all local A states"),
            outputs=("scalar_balance", "component_balance", "balanced"),
            software_contract=(
                "Calculate both scalar and component-wise totals.",
                "Report both interpretations rather than silently choosing one.",
            ),
            unresolved_items=(
                "Whether component-wise zero balance is required or only scalar zero balance.",
            ),
            source_section="3. Global Tensegrity Equilibrium Matrix",
        ),
        RuleSpec(
            rule_id="TR-PHASE-001",
            title="Phase-lock condition",
            kind=RuleKind.TRANSITION,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="lim_(t->t_lock)(M(t) - A(t)) = 0",
            description="A local cell enters phase lock when compressive and repulsive field states converge.",
            required_inputs=("M", "A", "phase_lock_tolerance"),
            outputs=("phase_error", "locked"),
            software_contract=(
                "Calculate the residual M - A.",
                "Use a declared tolerance and include it in every audit.",
            ),
            source_section="2.2 Phase-Lock and Ejection Mechanics",
        ),
        RuleSpec(
            rule_id="TR-JAM-001",
            title="Boundary jam",
            kind=RuleKind.TRANSITION,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="jammed = (tension >= capacity) AND (resistance_gradient >= threshold)",
            description="A local cell jams when maximum tension and limiting external resistance occur together.",
            required_inputs=(
                "tension",
                "tension_capacity",
                "resistance_gradient_norm",
                "resistance_threshold",
            ),
            outputs=("jammed",),
            software_contract=(
                "Both conditions must pass.",
                "Thresholds must be externally declared and audited.",
            ),
            unresolved_items=(
                "Numerical tension capacity.",
                "Finite approximation of infinite resistance.",
            ),
            source_section="2.1 The Boundary Jam Equation",
        ),
        RuleSpec(
            rule_id="TR-EJECT-001",
            title="Non-truncating harmonic ejection",
            kind=RuleKind.TRANSITION,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="C_jam -> Psi_0 + Phi_ejected",
            description="After phase lock, the local coordinate resets while structural information is preserved in an ejected packet.",
            required_inputs=("jammed cell state", "phase_lock result"),
            outputs=("Psi_0", "Phi_ejected"),
            software_contract=(
                "Deep-copy or serialize structural information before reset.",
                "Reset source coordinate only after preservation succeeds.",
                "Audit before-state, packet-state, and after-state hashes.",
            ),
            unresolved_items=("Destination and reinsertion rules for the clean-cell pool.",),
            source_section="2.2 Phase-Lock and Ejection Mechanics",
        ),
        RuleSpec(
            rule_id="EQ-SENS-001",
            title="Sensitivity response",
            kind=RuleKind.EQUATION,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="delta_Psi = S delta_E",
            description="External perturbations modify the manifold through a sensitivity matrix.",
            required_inputs=("S", "delta_E"),
            outputs=("delta_Psi",),
            software_contract=(
                "Matrix columns must equal perturbation-vector length.",
                "Preserve units metadata when supplied.",
            ),
            source_section="Unified ABTM Field Equations, Harmonic Coupling and Sensitivity",
        ),
        RuleSpec(
            rule_id="TR-BIF-001",
            title="Bifurcation detection",
            kind=RuleKind.TRANSITION,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="det(S) -> 0",
            description="A near-singular sensitivity matrix indicates transition toward a nonlinear regime.",
            required_inputs=("S", "bifurcation_threshold"),
            outputs=("determinant", "near_bifurcation"),
            software_contract=(
                "S must be square.",
                "Report determinant and threshold together.",
            ),
            unresolved_items=("The physically justified bifurcation threshold.",),
            source_section="Unified ABTM Field Equations, Harmonic Coupling and Sensitivity",
        ),
        RuleSpec(
            rule_id="INV-Z6-001",
            title="Original Z6 trace residue",
            kind=RuleKind.INVARIANT,
            status=SpecificationStatus.EXPLICIT,
            mathematical_form="sigma = Trace(Psi_barrier) mod 6",
            description="The supplied original engine returns stable when the barrier-matrix trace has zero residue modulo six.",
            required_inputs=("Psi_barrier matrix",),
            outputs=("trace", "sigma", "stable"),
            software_contract=(
                "Input must be a two-dimensional numerical matrix.",
                "Return stable only when sigma equals zero.",
                "Do not present this rule as equivalent to every broader ABTM invariant.",
            ),
            unresolved_items=(
                "Derivation connecting this matrix invariant to the 64-cell M^6 field.",
            ),
            source_section="Original ABTM_Engine source code",
        ),
        RuleSpec(
            rule_id="GRID-64-001",
            title="64-cell spatial lattice",
            kind=RuleKind.SOFTWARE_CONTRACT,
            status=SpecificationStatus.PROVISIONAL_MAPPING,
            mathematical_form="8 x 8 = 64 spatial cells",
            description="The software supports a fixed 64-cell frame while preserving uncertainty about how source observations populate cells.",
            required_inputs=("cell mapping rule", "cell states"),
            outputs=("8 x 8 field frame",),
            software_contract=(
                "Every cell has a stable coordinate.",
                "Empty and overflow states must be explicit.",
                "Mapping must be audited and never silently rearranged.",
            ),
            unresolved_items=(
                "Whether each cell stores one scalar, one subgroup, or one six-component local manifold state.",
                "How the z spatial axis is encoded.",
                "Neighbour topology and boundary conditions.",
            ),
            source_section="User-specified 64-grid architecture",
        ),
    ]

    for rule in rules:
        spec.register_rule(rule)

    spec.grid = GridSpec(
        rows=8,
        columns=8,
        cell_count=64,
        cell_state_components=("Mx", "My", "Mz", "Ax", "Ay", "Az"),
        full_frame_value_count=384,
        spatial_mapping_status=SpecificationStatus.PROVISIONAL_MAPPING,
        notes=(
            "A six-component cell state follows directly from M in R3 and A in R3.",
            "The assignment of raw user sequences to these cell states remains unresolved.",
            "The 8 x 8 display is spatially two-dimensional while gradient equations are three-dimensional.",
        ),
    )

    return spec


CORE_SPEC = build_core_specification()
