"""
JUFE / ABTM Specification Registry
==================================

Provides an active registry that engines and launchers can query without
hardcoding specification text.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from abtm_specification import (
    ABTMSpecification,
    CORE_SPEC,
    ParameterSpec,
    RuleSpec,
    VariableSpec,
)


class SpecificationRegistry:
    def __init__(self, specification: ABTMSpecification | None = None) -> None:
        self.specification = specification or CORE_SPEC

    def get_rule(self, rule_id: str) -> RuleSpec:
        try:
            return self.specification.rules[rule_id]
        except KeyError as exc:
            raise KeyError(f"Unknown specification rule: {rule_id}") from exc

    def get_variable(self, symbol: str) -> VariableSpec:
        try:
            return self.specification.variables[symbol]
        except KeyError as exc:
            raise KeyError(f"Unknown specification variable: {symbol}") from exc

    def get_parameter(self, name: str) -> ParameterSpec:
        try:
            return self.specification.parameters[name]
        except KeyError as exc:
            raise KeyError(f"Unknown specification parameter: {name}") from exc

    def unresolved(self) -> dict[str, Any]:
        return self.specification.unresolved()

    def export_json(self, destination: str | Path) -> Path:
        path = Path(destination)
        path.write_text(
            json.dumps(self.specification.to_dict(), indent=2, default=str),
            encoding="utf-8",
        )
        return path


REGISTRY = SpecificationRegistry()
