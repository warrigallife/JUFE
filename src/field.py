from __future__ import annotations


class JUFEField:
    """
    JUFE Field

    Runtime representation of the Field defined in
    Manuscript 001.

    A Field contains one or more Structures.
    """

    def __init__(self, structures=None):

        self.structures = structures if structures else []

    def add_structure(self, structure):

        self.structures.append(structure)

    def structure_count(self):

        return len(self.structures)

    def to_dict(self):

        return {
            "structure_count": self.structure_count(),
            "structures": [
                structure.to_dict()
                for structure in self.structures
            ],
        }

    def __repr__(self):

        return (
            f"JUFEField("
            f"{self.structure_count()} structures)"
        )