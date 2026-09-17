from __future__ import annotations

import base64
import hashlib
import json
import zlib
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class KernelState:
    """
    Immutable JUFE Kernel State.

    Represents the sealed execution context
    for a verified JUFE runtime.
    """

    version: str
    integrity_hash: str
    lattice_basis: str
    core_twist: str
    specification: str
    engine_name: str
    gate_state: str


class JUFEKernel:
    """
    JUFE Kernel

    Establishes, validates and seals the
    executable JUFE runtime environment.
    """

    def __init__(
        self,
        specification: str,
        engine: Any,
    ) -> None:

        if not isinstance(specification, str):
            raise TypeError(
                "specification must be a string."
            )

        if not specification.strip():
            raise ValueError(
                "Specification cannot be empty."
            )

        if engine is None:
            raise ValueError(
                "A computational engine is required."
            )

        self._engine = engine

        self._state = KernelState(

            version="0.2.0",

            integrity_hash="PENDING",

            lattice_basis="Z6-CLOSED-RING",

            core_twist="3PI_NON_ORIENTABLE",

            specification=specification,

            engine_name=engine.__class__.__name__,

            gate_state="ACTIVE",

        )

        #
        # Compute deterministic integrity hash.
        #

        self._state = KernelState(

            version=self._state.version,

            integrity_hash=self._compute_hash(),

            lattice_basis=self._state.lattice_basis,

            core_twist=self._state.core_twist,

            specification=self._state.specification,

            engine_name=self._state.engine_name,

            gate_state=self._state.gate_state,

        )

    @property
    def state(self) -> KernelState:

        return self._state

    @property
    def engine(self):

        return self._engine

    def execute_boot(self) -> bytes:
        """
        Validate and seal the Kernel.
        """

        self._validate_state()

        return self._seal_kernel()

    def _validate_state(self):

        required = (

            self._state.version,

            self._state.integrity_hash,

            self._state.lattice_basis,

            self._state.core_twist,

            self._state.specification,

            self._state.engine_name,

            self._state.gate_state,

        )

        if not all(required):

            raise RuntimeError(
                "Kernel state is incomplete."
            )

    def _compute_hash(self) -> str:
        """
        Compute a deterministic integrity
        digest for the Kernel state.
        """

        payload = json.dumps(

            {

                "version": self._state.version,

                "lattice_basis": self._state.lattice_basis,

                "core_twist": self._state.core_twist,

                "specification": self._state.specification,

                "engine_name": self._state.engine_name,

                "gate_state": self._state.gate_state,

            },

            sort_keys=True,

        ).encode("utf-8")

        return hashlib.sha256(payload).hexdigest()

    def _seal_kernel(self) -> bytes:
        """
        Produce a deterministic sealed
        representation of the Kernel.
        """

        payload = json.dumps(

            asdict(self._state),

            sort_keys=True,

            separators=(",", ":"),

        ).encode("utf-8")

        compressed = zlib.compress(payload)

        return base64.b85encode(compressed)

    def __repr__(self):

        return (

            "JUFEKernel("

            f"version='{self._state.version}', "

            f"engine='{self._state.engine_name}', "

            f"gate='{self._state.gate_state}')"

        )