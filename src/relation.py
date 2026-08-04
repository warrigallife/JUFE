from __future__ import annotations


class JUFERelation:
    """
    JUFE Relation

    Canonical relational object defined by
    the JUFE manuscripts.

    A Relation connects two manuscript
    objects while preserving relational
    identity and lifecycle state.
    """

    VALID_STATES = {
        "ACTIVE",
        "VACUUM",
        "UNDEFINED",
    }

    def __init__(
        self,
        source,
        target,
        relation_type: str = "GENERIC",
        *,
        identifier: str | None = None,
        lifecycle_state: str = "ACTIVE",
    ):

        if source is None:
            raise ValueError(
                "Relation source cannot be None."
            )

        if target is None:
            raise ValueError(
                "Relation target cannot be None."
            )

        lifecycle_state = lifecycle_state.upper()

        if lifecycle_state not in self.VALID_STATES:
            raise ValueError(
                "Invalid lifecycle_state."
            )

        self.identifier = identifier

        self.source = source

        self.target = target

        self.relation_type = relation_type.upper()

        self.lifecycle_state = lifecycle_state

    def is_defined(self):

        return (
            self.lifecycle_state
            != "UNDEFINED"
        )

    def is_self_relation(self):

        return (
            self.source
            == self.target
        )

    def to_dict(self):

        return {

            "identifier": self.identifier,

            "source": self.source,

            "target": self.target,

            "relation_type": self.relation_type,

            "lifecycle_state": self.lifecycle_state,

            "self_relation": self.is_self_relation(),

        }

    def __repr__(self):

        return (

            "JUFERelation("

            f"id={self.identifier}, "

            f"{self.source} -> "

            f"{self.target}, "

            f"type='{self.relation_type}', "

            f"state='{self.lifecycle_state}'"

            ")"

        )