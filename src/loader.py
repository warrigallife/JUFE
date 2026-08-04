from __future__ import annotations

from pathlib import Path


class SpecificationLoader:
    """
    JUFE Specification Loader.

    Loads executable JUFE specifications from
    persistent storage.
    """

    def load(
        self,
        filepath: str,
    ) -> str:

        path = Path(filepath)

        #
        # Existence.
        #

        if not path.exists():

            raise FileNotFoundError(
                f"Specification not found: {filepath}"
            )

        #
        # File type.
        #

        if not path.is_file():

            raise ValueError(
                "Specification path is not a file."
            )

        #
        # Read specification.
        #

        text = path.read_text(
            encoding="utf-8"
        )

        #
        # Empty specification.
        #

        if not text.strip():

            raise ValueError(
                "Specification is empty."
            )

        #
        # Canonical JUFE heading.
        #

        first_line = text.splitlines()[0].strip()

        if not first_line.startswith("#"):

            raise ValueError(
                "Specification must begin with a Markdown heading."
            )

        return text