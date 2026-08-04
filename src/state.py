from __future__ import annotations


class JUFEState:
    """
    Fundamental JUFE State.

    Manuscript 001 defines a State as the complete relational
    description of a system at a given relational condition.

    This class is the runtime representation of that definition.
    """

    def __init__(self, values):

        self.values = list(values)

        self.count = len(self.values)

        self.sum = sum(self.values)

        self.mean = (
            self.sum / self.count
            if self.count > 0
            else 0.0
        )

    def to_dict(self):

        return {
            "values": self.values,
            "count": self.count,
            "sum": self.sum,
            "mean": self.mean,
        }

    def __repr__(self):

        return (
            f"JUFEState("
            f"values={self.values}, "
            f"count={self.count})"
        )