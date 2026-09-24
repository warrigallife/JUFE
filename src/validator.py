from __future__ import annotations

from .parser import ParsedSpecification


class SpecificationValidator:
    """
    JUFE Specification Validator.

    Verifies that a parsed specification
    satisfies the minimum executable
    requirements before runtime execution.
    """

    def validate(
        self,
        specification: ParsedSpecification,
    ) -> bool:

        #
        # Title
        #

        if not specification.title.strip():

            raise ValueError(
                "Specification title is missing."
            )

        #
        # Content
        #

        if not specification.content.strip():

            raise ValueError(
                "Specification content is empty."
            )

        #
        # Version
        #

        if not specification.version.strip():

            raise ValueError(
                "Specification version is missing."
            )

        #
        # Duplicate definitions.
        #
        # SPEC-001 lists "Definitions" as an OPTIONAL specification
        # section, so an empty definitions list is not itself a
        # failure condition; only duplicates among any that exist are.
        #

        if len(specification.definitions) != len(
            set(specification.definitions)
        ):

            raise ValueError(
                "Duplicate definition identifiers detected."
            )

        return True