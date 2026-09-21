# How we work on JUFE with agents

Written for the project owner. Plain language first; details after.

## What we want

To help with JUFE and the Warrigal research suite using the same kind of tooling
used on other projects, without weakening JUFE's own rule: **source, interpretation,
specification, implementation and validation stay separate, and nothing is called
established because code exists, sounds persuasive, or an AI agrees.**

In practice that means:

- Small, checkable steps, each on a branch, each reviewed by the owner.
- Tests that record what the code does today, so change is visible.
- Every open question written down and left to the owner, not settled by us.

## What an "agent" is here

An agent is a separate Claude session given one bounded job. It reads, reports, or
writes to exactly one place. A coordinator (the "lead") checks the results and owns
commits. Agents do not talk to the owner directly and never push anything.

The arrangement is hierarchical: one lead, many specialists, one writer per file,
and no fixed cap on how many agents run.

**Honest limits**

- The agents used so far were plain Claude sessions; no separate system records
  their work.
- Agents agreeing with each other proves nothing, and a vote is not a validation
  gate. Only the gate in JUFE's own specification promotes a claim.
- Tests here record current behaviour. They do not show the mathematics is correct.

## Who did what so far

| Agent | Job | Result |
|---|---|---|
| lead | Path fix, commits, integration | `src/runtime.py` fix, this branch |
| launcher-mapper | Read-only inventory (Issue 5) | `docs/LAUNCHER_MAP.md` |
| grid-tester | 64-cell tests (Issue 4) | `tests/test_grid_mapping.py`: 18 tests, 5 mark open decisions |
| warrigal-checker | Run the Warrigal suite off the Mac, no network | 173 of 179 pass; 3 need undeclared `instaloader`, 3 need a `python` command |
| status auditor | Find every status label (Issue 6) | reported only; nothing renamed |

## Handover issues: where each stands

| Issue | State |
|---|---|
| 1 Explorer files | Waiting for the owner: the files exist only on the Mac |
| 2 Dependency definition | `requirements.txt` added; clean install not verified |
| 3 Path portability | Path fixed. Boot still stops: the boot spec has no `DEF-` lines. Owner decision |
| 4 First tests | 34 tests, 28 pass, 6 expected failures marking open decisions |
| 5 Execution pathways | Done: `docs/LAUNCHER_MAP.md` |
| 6 Status claims | Audited, not changed. `IMPLEMENTED` is hard-coded; `stable` has two meanings |
| 7 Passage-analysis contract | Blocked on the owner and Tom |
| 8 Frontier register | Not started |

## Ideas considered

Not adopted, only noted, until the owner has answered the open questions:

- A small checker that flags a claim carrying no evidence, modelled on JUFE's own
  status tiers.
- Lean 4 for the mathematical frontiers, once they are precise enough to state.
- A typed Rust core for the six-value cell, after tests pin the Python behaviour.
- Trying AISP notation on one specification as an experiment.

Not wanted: agent voting as validation; replacing Lean, NumPy or the tracker with
rewrites that describe their own target state.

## Rules every agent follows

1. Preserve original manuscripts and source unchanged.
2. Never invent or complete missing mathematics.
3. Record status as explicit, provisional, unresolved, rejected, promotion candidate,
   or validated, and keep source and interpretation apart.
4. Ask the owner before any change to scientific or interpretive meaning.
5. Work on a branch. No push, pull request or merge without the owner's approval.
6. One writer per file; everyone else read-only.
7. Delete nothing until its contents and authority are compared.
8. Report what could not be verified. Never claim a pass that was not observed.

## Run the tests

    python -m unittest discover -s tests -t . -v
