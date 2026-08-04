from __future__ import annotations

from typing import Iterable


class JUFEStructure:
    """
    JUFE Structure

    Canonical implementation of the Structure
    defined by the JUFE manuscripts.

    A Structure is an ordered collection of
    Relations.
    """

    def __init__(
        self,
        relations: Iterable | None = None,
        *,
        identifier: str | None = None,
        lifecycle_state: str = "ACTIVE",
    ):

        self.identifier = identifier

        self.lifecycle_state = lifecycle_state.upper()

        self.relations = []

        if relations is not None:

            for relation in relations:

                self.add_relation(relation)

    def add_relation(
        self,
        relation,
    ):

        if relation is None:

            raise ValueError(
                "Relation cannot be None."
            )

        if not hasattr(
            relation,
            "to_dict",
        ):

            raise TypeError(
                "Relation must implement to_dict()."
            )

        self.relations.append(
            relation
        )

    def relation_count(self):

        return len(
            self.relations
        )

    def is_empty(self):

        return (
            self.relation_count()
            == 0
        )

    def is_defined(self):

        return (
            self.lifecycle_state
            != "UNDEFINED"
        )

    def to_dict(self):

        return {

            "identifier": self.identifier,

            "lifecycle_state": self.lifecycle_state,

            "relation_count": self.relation_count(),

            "relations": [

                relation.to_dict()

                for relation in self.relations

            ],

        }

    def __repr__(self):

        return (

            "JUFEStructure("

            f"id={self.identifier}, "

            f"relations={self.relation_count()}, "

            f"state='{self.lifecycle_state}'"

            ")"

        )