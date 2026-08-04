"""
Reference interfaces for future JUFE / ABTM engines.
No physical rule is implemented here.
"""

from __future__ import annotations
from typing import Protocol, Any


class SpecificationAware(Protocol):
    specification_id: str


class GradientEngine(Protocol):
    specification_id: str
    def compute(self, compressive_field: Any, spacing: Any, coupling_constant: float) -> Any: ...


class ConservationEngine(Protocol):
    specification_id: str
    def step(self, M: Any, A: Any, dM_dt: Any, dt: float) -> tuple[Any, Any]: ...


class PhaseEngine(Protocol):
    specification_id: str
    def check_lock(self, M: Any, A: Any, tolerance: float) -> Any: ...


class BoundaryEngine(Protocol):
    specification_id: str
    def check_jam(
        self,
        tension: float,
        tension_capacity: float,
        resistance: float,
        resistance_threshold: float,
    ) -> Any: ...


class EquilibriumEngine(Protocol):
    specification_id: str
    def check_global(self, M_fields: Any, A_fields: Any, tolerance: float) -> Any: ...
