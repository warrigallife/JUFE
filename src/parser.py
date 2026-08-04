from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class ParsedSpecification:
    """
    Parsed JUFE Specification.

    Represents the executable form of a
    specification after parsing.
    """

    title: str

    content: str

    version: str

    definitions: List[str] = field(default_factory=list)

    metadata: Dict[str, str] = field(default_factory=dict)


class SpecificationParser:
    """
    JUFE Specification Parser.

    Converts a raw specification document into
    a structured executable representation.
    """

    def parse(
        self,
        raw_text: str,
    ) -> ParsedSpecification:

        if not raw_text.strip():

            raise ValueError(
                "Specification is empty."
            )

        lines = raw_text.splitlines()

        title = "Untitled Specification"

        version = "UNKNOWN"

        definitions = []

        metadata = {}

        for line in lines:

            stripped = line.strip()

            #
            # Title
            #

            if stripped.startswith("#") and title == "Untitled Specification":

                title = stripped.lstrip("#").strip()

                continue

            #
            # Version
            #

            if stripped.lower().startswith("version"):

                parts = stripped.split(":", 1)

                if len(parts) == 2:

                    version = parts[1].strip()

                continue

            #
            # Definition identifiers.
            #

            if stripped.startswith("DEF-"):

                identifier = stripped.split()[0]

                definitions.append(identifier)

                continue

            #
            # Metadata
            #

            if ":" in stripped:

                key, value = stripped.split(":", 1)

                metadata[key.strip()] = value.strip()

        return ParsedSpecification(

            title=title,

            content=raw_text,

            version=version,

            definitions=definitions,

            metadata=metadata,

        )