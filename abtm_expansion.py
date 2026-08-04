"""
ABTM Expansion Layer
====================

Separate implementation of the mathematical operations described in:

1. The Unified ABTM Field Equations
2. Relational Unified Field Mechanics:
   Analytical Resolution of Critical Cosmological Anomalies

This module does not edit or replace either original JUFE source file.
It provides the missing ABTM_Expansion base class that ABTM_Engine expects.

The class is deliberately numerical and explicit:
- inputs must be supplied as NumPy-compatible arrays or numerical values;
- tolerances and thresholds are parameters rather than hidden constants;
- no input grouping or physical interpretation is inferred automatically.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

import numpy as np


ArrayLike = Sequence[float] | Sequence[Sequence[float]] | np.ndarray


@dataclass(frozen=True)
class BifurcationResult:
    determinant: float
    threshold: float
    near_bifurcation: bool


@dataclass(frozen=True)
class BalanceResult:
    scalar_total: float
    component_total: np.ndarray
    tolerance: float
    scalar_balanced: bool
    component_balanced: bool


@dataclass(frozen=True)
class JamResult:
    tension_reached: bool
    resistance_reached: bool
    jammed: bool


@dataclass(frozen=True)
class PhaseLockResult:
    residual: np.ndarray
    residual_norm: float
    tolerance: float
    locked: bool


class ABTM_Expansion:
    """
    Numerical base layer for the ABTM engine.

    The class exposes the supplied equations as independent operations.
    It does not decide how a user's raw sequence maps into M, A, Psi, S,
    or the stress tensor. That mapping remains explicit at the call site.
    """

    def __init__(
        self,
        *,
        equilibrium_tolerance: float = 1e-9,
        phase_lock_tolerance: float = 1e-9,
        bifurcation_threshold: float = 1e-9,
    ) -> None:
        self.equilibrium_tolerance = self._positive_or_zero(
            equilibrium_tolerance,
            "equilibrium_tolerance",
        )
        self.phase_lock_tolerance = self._positive_or_zero(
            phase_lock_tolerance,
            "phase_lock_tolerance",
        )
        self.bifurcation_threshold = self._positive_or_zero(
            bifurcation_threshold,
            "bifurcation_threshold",
        )

    # ------------------------------------------------------------------
    # Core state helpers
    # ------------------------------------------------------------------

    @staticmethod
    def as_array(value: ArrayLike, *, name: str = "value") -> np.ndarray:
        array = np.asarray(value, dtype=float)
        if array.size == 0:
            raise ValueError(f"{name} must not be empty.")
        if not np.all(np.isfinite(array)):
            raise ValueError(f"{name} must contain only finite numbers.")
        return array

    @staticmethod
    def _positive_or_zero(value: float, name: str) -> float:
        number = float(value)
        if not np.isfinite(number) or number < 0:
            raise ValueError(f"{name} must be a finite value greater than or equal to zero.")
        return number

    @classmethod
    def compose_manifold_state(
        cls,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
    ) -> np.ndarray:
        """
        Compose the M^6 state as [Mx, My, Mz, Ax, Ay, Az].

        Both vectors must have exactly three components.
        """
        m = cls.as_array(compressive_field, name="compressive_field").reshape(-1)
        a = cls.as_array(repulsive_field, name="repulsive_field").reshape(-1)

        if m.size != 3 or a.size != 3:
            raise ValueError(
                "compressive_field and repulsive_field must each contain "
                "exactly three components."
            )

        return np.concatenate((m, a))

    @classmethod
    def split_manifold_state(cls, psi: ArrayLike) -> tuple[np.ndarray, np.ndarray]:
        """Split a six-component Psi state into M and A vectors."""
        state = cls.as_array(psi, name="psi").reshape(-1)
        if state.size != 6:
            raise ValueError("psi must contain exactly six components.")
        return state[:3].copy(), state[3:].copy()

    # ------------------------------------------------------------------
    # Z6 structural layer and mod-7 temporal layer
    # ------------------------------------------------------------------

    @classmethod
    def z6_trace_residue(cls, psi_barrier: ArrayLike) -> float:
        """
        sigma = Trace(Psi) mod 6

        This is the same numerical rule used by the supplied ABTM_Engine.
        """
        matrix = cls.as_array(psi_barrier, name="psi_barrier")
        if matrix.ndim != 2:
            raise ValueError("psi_barrier must be a two-dimensional matrix.")
        return float(np.trace(matrix) % 6)

    @classmethod
    def z6_stable(cls, psi_barrier: ArrayLike) -> bool:
        """Return True when Trace(Psi) mod 6 equals zero."""
        return bool(np.isclose(cls.z6_trace_residue(psi_barrier), 0.0))

    @staticmethod
    def mod7_phase(index_or_time: float) -> float:
        """Return the supplied temporal index reduced modulo 7."""
        value = float(index_or_time)
        if not np.isfinite(value):
            raise ValueError("index_or_time must be finite.")
        return value % 7

    # ------------------------------------------------------------------
    # Global manifold and stress tensor
    # ------------------------------------------------------------------

    @classmethod
    def geometry_curvature_term(
        cls,
        phi: float,
        psi_gradient: ArrayLike,
        metric: ArrayLike,
        hamiltonian_density: float,
    ) -> np.ndarray:
        r"""
        Phi * (grad(Psi) outer grad(Psi) - 1/2 * g * H_M)

        psi_gradient must be a one-dimensional vector.
        metric must be square with matching dimension.
        """
        gradient = cls.as_array(psi_gradient, name="psi_gradient").reshape(-1)
        g = cls.as_array(metric, name="metric")

        if g.ndim != 2 or g.shape[0] != g.shape[1]:
            raise ValueError("metric must be a square matrix.")
        if g.shape[0] != gradient.size:
            raise ValueError("metric dimension must match psi_gradient length.")

        return float(phi) * (
            np.outer(gradient, gradient)
            - 0.5 * g * float(hamiltonian_density)
        )

    @classmethod
    def total_stress_tensor(
        cls,
        geometry_curvature: ArrayLike,
        z6_tensor: ArrayLike,
        *,
        kappa: float = 1.0,
        toroidal_flux: ArrayLike | None = None,
        harmonic_terms: Iterable[ArrayLike] | None = None,
    ) -> np.ndarray:
        r"""
        T_total =
            geometry_curvature
            + kappa * Z6
            + toroidal_flux
            + sum(harmonic_terms)

        Every supplied tensor must have the same shape.
        """
        geometry = cls.as_array(geometry_curvature, name="geometry_curvature")
        z6 = cls.as_array(z6_tensor, name="z6_tensor")

        if geometry.shape != z6.shape:
            raise ValueError("geometry_curvature and z6_tensor must have matching shapes.")

        total = geometry + float(kappa) * z6

        if toroidal_flux is not None:
            flux = cls.as_array(toroidal_flux, name="toroidal_flux")
            if flux.shape != total.shape:
                raise ValueError("toroidal_flux must match the stress-tensor shape.")
            total = total + flux

        if harmonic_terms is not None:
            for index, term in enumerate(harmonic_terms):
                harmonic = cls.as_array(term, name=f"harmonic_terms[{index}]")
                if harmonic.shape != total.shape:
                    raise ValueError(
                        f"harmonic_terms[{index}] must match the stress-tensor shape."
                    )
                total = total + harmonic

        return total

    @classmethod
    def divergence_from_tensor_field(
        cls,
        tensor_field: ArrayLike,
        *,
        spacing: float | Sequence[float] = 1.0,
    ) -> np.ndarray:
        r"""
        Numerically evaluate div(T) for a tensor field.

        Expected shape:
            spatial_shape + (dimension, dimension)

        The number of spatial axes must equal the tensor dimension.
        For example, a 3D field of 3x3 tensors has shape:
            (nx, ny, nz, 3, 3)
        """
        field = cls.as_array(tensor_field, name="tensor_field")

        if field.ndim < 3:
            raise ValueError(
                "tensor_field must include spatial axes followed by two tensor axes."
            )

        tensor_rows, tensor_cols = field.shape[-2:]
        if tensor_rows != tensor_cols:
            raise ValueError("The final two tensor axes must form square matrices.")

        spatial_shape = field.shape[:-2]
        dimension = tensor_rows

        if len(spatial_shape) != dimension:
            raise ValueError(
                "The number of spatial axes must equal the tensor dimension."
            )

        if isinstance(spacing, Sequence) and not isinstance(spacing, (str, bytes)):
            spacing_values = tuple(float(value) for value in spacing)
            if len(spacing_values) != dimension:
                raise ValueError("spacing must contain one value per spatial axis.")
        else:
            spacing_values = (float(spacing),) * dimension

        divergence = np.zeros(spatial_shape + (dimension,), dtype=float)

        # div(T)^nu = partial_mu T^(mu,nu)
        for nu in range(dimension):
            component = np.zeros(spatial_shape, dtype=float)
            for mu in range(dimension):
                derivative = np.gradient(
                    field[..., mu, nu],
                    spacing_values[mu],
                    axis=mu,
                    edge_order=1,
                )
                component += derivative
            divergence[..., nu] = component

        return divergence

    def divergence_free(
        self,
        divergence: ArrayLike,
        *,
        tolerance: float | None = None,
    ) -> bool:
        r"""Check ||div(T_total)|| <= tolerance."""
        residual = self.as_array(divergence, name="divergence")
        tol = (
            self.equilibrium_tolerance
            if tolerance is None
            else self._positive_or_zero(tolerance, "tolerance")
        )
        return bool(np.linalg.norm(residual) <= tol)

    # ------------------------------------------------------------------
    # Sensitivity and bifurcation
    # ------------------------------------------------------------------

    @classmethod
    def apply_sensitivity(
        cls,
        sensitivity_matrix: ArrayLike,
        external_perturbation: ArrayLike,
    ) -> np.ndarray:
        r"""delta(Psi) = S * delta(E)."""
        sensitivity = cls.as_array(
            sensitivity_matrix,
            name="sensitivity_matrix",
        )
        perturbation = cls.as_array(
            external_perturbation,
            name="external_perturbation",
        ).reshape(-1)

        if sensitivity.ndim != 2:
            raise ValueError("sensitivity_matrix must be two-dimensional.")
        if sensitivity.shape[1] != perturbation.size:
            raise ValueError(
                "sensitivity_matrix columns must match external_perturbation length."
            )

        return sensitivity @ perturbation

    def detect_bifurcation(
        self,
        sensitivity_matrix: ArrayLike,
        *,
        threshold: float | None = None,
    ) -> BifurcationResult:
        r"""Detect det(S) approaching zero."""
        sensitivity = self.as_array(
            sensitivity_matrix,
            name="sensitivity_matrix",
        )

        if sensitivity.ndim != 2 or sensitivity.shape[0] != sensitivity.shape[1]:
            raise ValueError("sensitivity_matrix must be square.")

        determinant = float(np.linalg.det(sensitivity))
        limit = (
            self.bifurcation_threshold
            if threshold is None
            else self._positive_or_zero(threshold, "threshold")
        )

        return BifurcationResult(
            determinant=determinant,
            threshold=limit,
            near_bifurcation=bool(abs(determinant) <= limit),
        )

    # ------------------------------------------------------------------
    # Local gradient mechanics
    # ------------------------------------------------------------------

    @classmethod
    def scalar_field_gradient(
        cls,
        compressive_scalar_field: ArrayLike,
        *,
        spacing: float | Sequence[float] = 1.0,
    ) -> tuple[np.ndarray, ...]:
        r"""Compute grad(M) for a scalar field sampled on a grid."""
        field = cls.as_array(
            compressive_scalar_field,
            name="compressive_scalar_field",
        )
        if field.ndim == 0:
            raise ValueError("compressive_scalar_field must have at least one axis.")
        gradients = np.gradient(field, spacing, edge_order=1)
        if isinstance(gradients, np.ndarray):
            return (gradients,)
        return tuple(gradients)

    @classmethod
    def propagation_from_gradient(
        cls,
        compressive_gradient: ArrayLike,
        *,
        coupling_constant: float = 1.0,
    ) -> np.ndarray:
        r"""D = -k * grad(M)."""
        gradient = cls.as_array(
            compressive_gradient,
            name="compressive_gradient",
        )
        k = float(coupling_constant)
        if not np.isfinite(k):
            raise ValueError("coupling_constant must be finite.")
        return -k * gradient

    @classmethod
    def dominance_ratio(
        cls,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
    ) -> float:
        r"""Return ||M|| / ||A||."""
        m = cls.as_array(compressive_field, name="compressive_field")
        a = cls.as_array(repulsive_field, name="repulsive_field")

        denominator = float(np.linalg.norm(a))
        numerator = float(np.linalg.norm(m))

        if denominator == 0:
            return float("inf") if numerator > 0 else 1.0

        return numerator / denominator

    @classmethod
    def local_gradient_dominates(
        cls,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
        *,
        dominance_threshold: float,
    ) -> bool:
        """
        Check ||M|| / ||A|| >= dominance_threshold.

        The threshold must be supplied explicitly because the manuscript uses
        the qualitative relation 'much greater than' rather than a fixed value.
        """
        threshold = float(dominance_threshold)
        if not np.isfinite(threshold) or threshold < 0:
            raise ValueError("dominance_threshold must be finite and non-negative.")
        return bool(
            cls.dominance_ratio(compressive_field, repulsive_field)
            >= threshold
        )

    # ------------------------------------------------------------------
    # M/A conservation, phase lock, and boundary jam
    # ------------------------------------------------------------------

    def global_field_balance(
        self,
        compressive_fields: ArrayLike,
        repulsive_fields: ArrayLike,
        *,
        tolerance: float | None = None,
    ) -> BalanceResult:
        r"""
        Evaluate both interpretations of the supplied global identity:

        scalar:
            sum_global sum_i (M_i + A_i) = 0

        component-wise:
            sum_global (M + A) = vector(0)
        """
        m = self.as_array(compressive_fields, name="compressive_fields")
        a = self.as_array(repulsive_fields, name="repulsive_fields")

        if m.shape != a.shape:
            raise ValueError(
                "compressive_fields and repulsive_fields must have matching shapes."
            )
        if m.shape[-1] != 3:
            raise ValueError("The final axis must contain x, y, z components.")

        tol = (
            self.equilibrium_tolerance
            if tolerance is None
            else self._positive_or_zero(tolerance, "tolerance")
        )

        combined = m + a
        reduction_axes = tuple(range(combined.ndim - 1))
        component_total = np.sum(combined, axis=reduction_axes)
        scalar_total = float(np.sum(component_total))

        return BalanceResult(
            scalar_total=scalar_total,
            component_total=np.asarray(component_total, dtype=float),
            tolerance=tol,
            scalar_balanced=bool(abs(scalar_total) <= tol),
            component_balanced=bool(np.linalg.norm(component_total) <= tol),
        )

    @classmethod
    def coupled_field_step(
        cls,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
        compressive_rate: ArrayLike,
        *,
        dt: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        r"""
        Advance one explicit time step under:

            dM/dt = -dA/dt

        Therefore:
            M_next = M + dM/dt * dt
            A_next = A - dM/dt * dt
        """
        m = cls.as_array(compressive_field, name="compressive_field")
        a = cls.as_array(repulsive_field, name="repulsive_field")
        dm_dt = cls.as_array(compressive_rate, name="compressive_rate")

        if m.shape != a.shape or m.shape != dm_dt.shape:
            raise ValueError(
                "compressive_field, repulsive_field, and compressive_rate "
                "must have matching shapes."
            )

        time_step = float(dt)
        if not np.isfinite(time_step) or time_step < 0:
            raise ValueError("dt must be finite and non-negative.")

        delta = dm_dt * time_step
        return m + delta, a - delta

    def phase_lock(
        self,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
        *,
        tolerance: float | None = None,
    ) -> PhaseLockResult:
        r"""Check ||M - A|| <= tolerance."""
        m = self.as_array(compressive_field, name="compressive_field")
        a = self.as_array(repulsive_field, name="repulsive_field")

        if m.shape != a.shape:
            raise ValueError(
                "compressive_field and repulsive_field must have matching shapes."
            )

        tol = (
            self.phase_lock_tolerance
            if tolerance is None
            else self._positive_or_zero(tolerance, "tolerance")
        )

        residual = m - a
        residual_norm = float(np.linalg.norm(residual))

        return PhaseLockResult(
            residual=residual,
            residual_norm=residual_norm,
            tolerance=tol,
            locked=bool(residual_norm <= tol),
        )

    @classmethod
    def detect_boundary_jam(
        cls,
        *,
        tension: float,
        tension_capacity: float,
        resistance_gradient_norm: float,
        resistance_threshold: float,
    ) -> JamResult:
        """
        Numerical boundary-jam gate.

        The manuscript describes maximum tension and an infinite resistance
        gradient. Software requires finite thresholds supplied by the caller.
        """
        tension_value = float(tension)
        capacity = float(tension_capacity)
        resistance = float(resistance_gradient_norm)
        threshold = float(resistance_threshold)

        for name, value in (
            ("tension", tension_value),
            ("tension_capacity", capacity),
            ("resistance_gradient_norm", resistance),
            ("resistance_threshold", threshold),
        ):
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite.")

        if capacity < 0 or threshold < 0:
            raise ValueError(
                "tension_capacity and resistance_threshold must be non-negative."
            )

        tension_reached = tension_value >= capacity
        resistance_reached = resistance >= threshold

        return JamResult(
            tension_reached=tension_reached,
            resistance_reached=resistance_reached,
            jammed=bool(tension_reached and resistance_reached),
        )

    @staticmethod
    def eject_harmonic_packet(
        structural_state: Any,
    ) -> tuple[int, Any]:
        r"""
        C_jam -> Psi_0 + Phi_ejected

        Returns:
            psi_zero: 0
            phi_ejected: a deep copy of the supplied structural information

        No information is deleted or transformed by this operation.
        """
        return 0, deepcopy(structural_state)

    # ------------------------------------------------------------------
    # Combined diagnostic
    # ------------------------------------------------------------------

    def evaluate_local_cell(
        self,
        *,
        compressive_field: ArrayLike,
        repulsive_field: ArrayLike,
        dominance_threshold: float,
        tension: float,
        tension_capacity: float,
        resistance_gradient_norm: float,
        resistance_threshold: float,
    ) -> Mapping[str, Any]:
        """
        Run the local checks without inferring any missing values.
        """
        dominance = self.dominance_ratio(
            compressive_field,
            repulsive_field,
        )
        phase = self.phase_lock(
            compressive_field,
            repulsive_field,
        )
        jam = self.detect_boundary_jam(
            tension=tension,
            tension_capacity=tension_capacity,
            resistance_gradient_norm=resistance_gradient_norm,
            resistance_threshold=resistance_threshold,
        )

        return {
            "dominance_ratio": dominance,
            "dominance_pass": dominance >= float(dominance_threshold),
            "phase_lock": phase,
            "boundary_jam": jam,
        }
