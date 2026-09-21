from __future__ import annotations

from pathlib import Path

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

        #
        # Anchor to the repository root and use the directory's
        # real name, so boot works on case-sensitive filesystems
        # and from any working directory.
        #

        return self.execute(
            str(
                Path(__file__).resolve().parent.parent
                / "Specifications"
                / "SPEC-010.md"
            )
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

    def evaluate(self, values):
        """
        Evaluate a single Local Field State.
        """

        return self.engine.evaluate(values)

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
        