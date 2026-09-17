"""
JUFE ABTM Residue Search Engine
===============================

Optimised arrangement search for larger datasets.

This module does not edit or replace any JUFE core file.

Mathematical basis
------------------
The original stability rule is:

    trace(matrix) % 6 == 0

When one subgroup total is selected from each set for the diagonal, only the
selected totals affect the trace. Therefore, the search can operate on each
candidate's residue modulo 6 rather than constructing every full matrix first.

The engine:
1. groups candidates by residue class;
2. uses dynamic programming to identify reachable residue states;
3. prunes branches that cannot reach residue 0;
4. constructs full arranged matrices only for passing selections.

This preserves the original trace-mod-6 rule exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class ResidueCandidate:
    set_index: int
    group_index: int
    total: float
    residue: int


@dataclass(frozen=True)
class SearchSolution:
    selected_group_indices: tuple[int, ...]
    selected_group_totals: tuple[float, ...]
    trace: float
    trace_mod_6: float


@dataclass(frozen=True)
class SearchStats:
    sets: int
    total_candidates: int
    theoretical_combinations: int
    states_explored: int
    branches_pruned: int
    solutions_found: int
    truncated: bool


def _normalise_residue(value: float, modulus: int) -> int:
    residue = float(value) % modulus

    if not np.isclose(residue, round(residue)):
        raise ValueError(
            "Optimised residue search currently requires subgroup totals "
            "whose modulo result is an integer."
        )

    return int(round(residue)) % modulus


def prepare_candidates(
    group_totals_by_set: Sequence[Sequence[float]],
    *,
    modulus: int = 6,
) -> list[list[ResidueCandidate]]:
    if modulus <= 0:
        raise ValueError("modulus must be greater than zero.")

    candidate_sets: list[list[ResidueCandidate]] = []

    for set_index, totals in enumerate(group_totals_by_set, start=1):
        if not totals:
            raise ValueError(f"Set {set_index} contains no subgroup totals.")

        candidates = [
            ResidueCandidate(
                set_index=set_index,
                group_index=group_index,
                total=float(total),
                residue=_normalise_residue(float(total), modulus),
            )
            for group_index, total in enumerate(totals, start=1)
        ]
        candidate_sets.append(candidates)

    if not candidate_sets:
        raise ValueError("At least one set is required.")

    return candidate_sets


def reachable_suffix_residues(
    candidate_sets: Sequence[Sequence[ResidueCandidate]],
    *,
    modulus: int = 6,
) -> list[set[int]]:
    """
    suffix[i] contains residues reachable using sets i..end.
    """
    count = len(candidate_sets)
    suffix: list[set[int]] = [set() for _ in range(count + 1)]
    suffix[count] = {0}

    for index in range(count - 1, -1, -1):
        reachable: set[int] = set()

        for candidate in candidate_sets[index]:
            for tail_residue in suffix[index + 1]:
                reachable.add(
                    (candidate.residue + tail_residue) % modulus
                )

        suffix[index] = reachable

    return suffix


def find_stable_selections(
    group_totals_by_set: Sequence[Sequence[float]],
    *,
    modulus: int = 6,
    max_solutions: int | None = 1000,
) -> tuple[list[SearchSolution], SearchStats]:
    """
    Find selections where the sum of one subgroup total per set is divisible
    by modulus.

    max_solutions=None means return every solution.
    """
    candidate_sets = prepare_candidates(
        group_totals_by_set,
        modulus=modulus,
    )

    suffix = reachable_suffix_residues(
        candidate_sets,
        modulus=modulus,
    )

    theoretical = 1
    total_candidates = 0

    for candidates in candidate_sets:
        theoretical *= len(candidates)
        total_candidates += len(candidates)

    solutions: list[SearchSolution] = []
    states_explored = 0
    branches_pruned = 0
    truncated = False

    selected_indices: list[int] = []
    selected_totals: list[float] = []

    def backtrack(set_position: int, current_residue: int) -> None:
        nonlocal states_explored, branches_pruned, truncated

        if max_solutions is not None and len(solutions) >= max_solutions:
            truncated = True
            return

        if set_position == len(candidate_sets):
            states_explored += 1

            if current_residue % modulus == 0:
                trace = float(sum(selected_totals))
                solutions.append(
                    SearchSolution(
                        selected_group_indices=tuple(selected_indices),
                        selected_group_totals=tuple(selected_totals),
                        trace=trace,
                        trace_mod_6=float(trace % modulus),
                    )
                )
            return

        needed_tail_residue = (-current_residue) % modulus

        if needed_tail_residue not in suffix[set_position]:
            branches_pruned += 1
            return

        for candidate in candidate_sets[set_position]:
            next_residue = (
                current_residue + candidate.residue
            ) % modulus

            required_after_choice = (-next_residue) % modulus

            if required_after_choice not in suffix[set_position + 1]:
                branches_pruned += 1
                continue

            states_explored += 1
            selected_indices.append(candidate.group_index)
            selected_totals.append(candidate.total)

            backtrack(set_position + 1, next_residue)

            selected_indices.pop()
            selected_totals.pop()

            if truncated:
                return

    backtrack(0, 0)

    stats = SearchStats(
        sets=len(candidate_sets),
        total_candidates=total_candidates,
        theoretical_combinations=theoretical,
        states_explored=states_explored,
        branches_pruned=branches_pruned,
        solutions_found=len(solutions),
        truncated=truncated,
    )

    return solutions, stats


def arrange_matrix(
    group_totals_by_set: Sequence[Sequence[float]],
    selected_group_indices: Sequence[int],
) -> np.ndarray:
    """
    Build the comparison matrix for a selected solution.

    Selected group i is moved to diagonal column i while all remaining group
    totals keep their original relative order. Zero padding is used only where
    needed to form a rectangular matrix.
    """
    if len(group_totals_by_set) != len(selected_group_indices):
        raise ValueError(
            "selected_group_indices must contain one index per set."
        )

    set_count = len(group_totals_by_set)
    width = max(
        set_count,
        max(len(totals) for totals in group_totals_by_set),
    )

    rows: list[list[float]] = []

    for row_index, (totals, selected_one_based) in enumerate(
        zip(group_totals_by_set, selected_group_indices)
    ):
        selected_index = selected_one_based - 1

        if selected_index < 0 or selected_index >= len(totals):
            raise ValueError(
                f"Selected group {selected_one_based} is invalid "
                f"for set {row_index + 1}."
            )

        selected = float(totals[selected_index])
        remaining = [
            float(value)
            for index, value in enumerate(totals)
            if index != selected_index
        ]

        row: list[float | None] = [None] * width
        row[row_index] = selected

        remaining_iter = iter(remaining)

        for column in range(width):
            if row[column] is None:
                row[column] = next(remaining_iter, 0.0)

        rows.append([float(value) for value in row])

    return np.asarray(rows, dtype=float)
