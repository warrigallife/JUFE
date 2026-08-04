"""
JUFE / ABTM Specification Validator
===================================

Active validation hooks derived from the formal specification.

These checks validate software inputs and invariant outputs. They do not
establish empirical truth of the physical interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np

from abtm_specification_registry import REGISTRY


@dataclass(frozen=True)
class ValidationResult:
    rule_id: str
    passed: bool
    residual: float | None
    details: dict[str, Any]


class SpecificationValidator:
    def validate_local_state(
        self,
        compressive_field: Sequence[float],
        repulsive_field: Sequence[float],
    ) -> ValidationResult:
        rule = REGISTRY.get_rule("DEF-M6-001")
        m = np.asarray(compressive_field, dtype=float).reshape(-1)
        a = np.asarray(repulsive_field, dtype=float).reshape(-1)

        passed = (
            m.size == 3
            and a.size == 3
            and np.all(np.isfinite(m))
            and np.all(np.isfinite(a))
        )

        return ValidationResult(
            rule_id=rule.rule_id,
            passed=bool(passed),
            residual=None,
            details={
                "M_shape": list(m.shape),
                "A_shape": list(a.shape),
                "Psi": np.concatenate((m, a)).tolist() if passed else None,
            },
        )

    def validate_global_balance(
        self,
        compressive_fields: Sequence[Sequence[float]],
        repulsive_fields: Sequence[Sequence[float]],
        *,
        tolerance: float = 1e-9,
    ) -> ValidationResult:
        rule = REGISTRY.get_rule("INV-GLOBAL-001")
        m = np.asarray(compressive_fields, dtype=float)
        a = np.asarray(repulsive_fields, dtype=float)

        if m.shape != a.shape:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                residual=None,
                details={"error": "M and A shapes do not match."},
            )

        combined = m + a
        scalar_total = float(np.sum(combined))
        component_total = np.sum(combined, axis=tuple(range(combined.ndim - 1)))
        residual = float(abs(scalar_total))

        return ValidationResult(
            rule_id=rule.rule_id,
            passed=bool(residual <= tolerance),
            residual=residual,
            details={
                "scalar_total": scalar_total,
                "component_total": np.asarray(component_total).tolist(),
                "tolerance": tolerance,
            },
        )

    def validate_phase_lock(
        self,
        compressive_field: Sequence[float],
        repulsive_field: Sequence[float],
        *,
        tolerance: float = 1e-9,
    ) -> ValidationResult:
        rule = REGISTRY.get_rule("TR-PHASE-001")
        m = np.asarray(compressive_field, dtype=float)
        a = np.asarray(repulsive_field, dtype=float)

        if m.shape != a.shape:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                residual=None,
                details={"error": "M and A shapes do not match."},
            )

        residual_vector = m - a
        residual = float(np.linalg.norm(residual_vector))

        return ValidationResult(
            rule_id=rule.rule_id,
            passed=bool(residual <= tolerance),
            residual=residual,
            details={
                "residual_vector": residual_vector.tolist(),
                "tolerance": tolerance,
            },
        )

    def validate_z6_trace(
        self,
        matrix: Sequence[Sequence[float]],
    ) -> ValidationResult:
        rule = REGISTRY.get_rule("INV-Z6-001")
        array = np.asarray(matrix, dtype=float)

        if array.ndim != 2:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                residual=None,
                details={"error": "Matrix must be two-dimensional."},
            )

        trace = float(np.trace(array))
        residue = float(trace % 6)

        return ValidationResult(
            rule_id=rule.rule_id,
            passed=bool(np.isclose(residue, 0.0)),
            residual=residue,
            details={
                "trace": trace,
                "trace_mod_6": residue,
                "shape": list(array.shape),
            },
        )


VALIDATOR = SpecificationValidator()
