from __future__ import annotations

from .kernel import JUFEKernel
from .loader import SpecificationLoader
from .parser import SpecificationParser
from .validator import SpecificationValidator

from .engines.abtm import ABTMEngine


class JUFERuntime:
    """
    Coordinates the execution of JUFE specifications.
    """

    def __init__(self) -> None:

        self.loader = SpecificationLoader()
        self.parser = SpecificationParser()
        self.validator = SpecificationValidator()

        self.engine = ABTMEngine()

    def boot(self):

        return self.execute(
            "Specifications/SPEC-010.md"
        )

    def execute(
        self,
        specification_path: str,
    ):

        raw_text = self.loader.load(
            specification_path
        )

        parsed = self.parser.parse(
            raw_text
        )

        self.validator.validate(
            parsed
        )

        kernel = JUFEKernel(
            specification=parsed.title,
            engine=self.engine,
        )

        sealed_state = kernel.execute_boot()

        return {

            "kernel": sealed_state,

            "specification": parsed.title,

            "engine": self.engine.name,

            "status": "READY",

        }

    def evaluate(
        self,
        values,
        *,
        dominance_threshold=None,
        phase_lock_tolerance=None,
        global_balance_tolerance=None,
        bifurcation_threshold=None,
    ):
        """
        Evaluate a single Local Field State.

        The four keyword-only diagnostic arguments (all defaulting to
        ``None``, meaning "not requested") are forwarded straight
        through to ``ABTMEngine.evaluate()`` unchanged -- see that
        method's own docstring for the exact opt-in diagnostic methods
        each one exposes and the byte-for-byte default-output identity
        guarantee when all four are omitted.
        """

        return self.engine.evaluate(
            values,
            dominance_threshold=dominance_threshold,
            phase_lock_tolerance=phase_lock_tolerance,
            global_balance_tolerance=global_balance_tolerance,
            bifurcation_threshold=bifurcation_threshold,
        )

    def evaluate_dataset(self, values):
        """
        Evaluate an arbitrary-length dataset.

        Complete Local Field States are evaluated.
        Remaining values are preserved.
        """

        results = []

        complete = len(values) // 6

        remaining = values[complete * 6:]

        for i in range(complete):

            state = values[i * 6:(i + 1) * 6]

            results.append(
                self.engine.evaluate(state)
            )

        return {

            "states": results,

            "remaining": remaining,

            "complete_states": complete,

            "remaining_count": len(remaining),

        }
        