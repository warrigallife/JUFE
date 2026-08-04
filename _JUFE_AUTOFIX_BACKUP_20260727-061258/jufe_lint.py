#!/usr/bin/env python3
"""Read-only Markdown linter for the JUFE Reference Specification."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

KNOWN_STATUSES = {
    "EXPLICIT", "PROVISIONAL", "UNRESOLVED", "DERIVED", "MODEL CLAIM",
    "DRAFT", "REVIEW", "LOCKED", "SUPERSEDED", "ARCHIVED",
    "ACTIVE SPECIFICATION DRAFT",
}
DOCUMENT_ID_PATTERN = re.compile(r"^JUFE-V(?P<volume>\d+)-CH(?P<chapter>\d{2})$")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_HEADING_PATTERN = re.compile(r"^(?P<chapter>\d+)\.(?P<section>\d+)(?:\.(?P<subsection>\d+))?\s+")
STATUS_FIELD_PATTERN = re.compile(r"^\s*(?:\*\*)?Status(?:\*\*)?\s*:\s*(.+?)\s*$", re.IGNORECASE)

@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    code: str
    severity: str
    message: str

def markdown_files(target: Path) -> Iterable[Path]:
    """Yield Markdown files from a file or directory."""

    if target.is_file():
        if target.suffix.lower() == ".md":
            yield target
        return

    markdown_paths = sorted(
        path
        for path in target.rglob("*.md")
        if ".git" not in path.parts
        and path.name != "README.md"
    )

    yield from markdown_paths

def add(
    items: list[Finding],
    path: Path,
    line: int,
    code: str,
    severity: str,
    message: str,
) -> None:
    """Append a finding to the results list."""
    items.append(Finding(path, line, code, severity, message))

def check_trailing_whitespace(
    line: str,
    line_number: int,
    path: Path,
    findings: list[Finding],
) -> None:
    """Check for invalid trailing whitespace on a line."""

    if line.rstrip() != line and not (
        line.endswith("  ") and not line.endswith("   ")
    ):
        add(
            findings,
            path,
            line_number,
            "JUFE002",
            "WARNING",
            "Trailing whitespace.",
        )


def check_final_newline(
    text: str,
    lines: list[str],
    path: Path,
    findings: list[Finding],
) -> None:
    """Check that the file ends with a newline."""

    if text and not text.endswith("\n"):
        add(
            findings,
            path,
            len(lines),
            "JUFE001",
            "WARNING",
            "File does not end with a newline.",
        )


def collect_metadata(
    lines: list[str],
) -> dict[str, tuple[int, str]]:
    """Collect recognised metadata fields from the first 40 lines."""

    metadata: dict[str, tuple[int, str]] = {}

    for i, line in enumerate(lines[:40], 1):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().strip("*")

            if key in {
                "Project",
                "Document ID",
                "Specification ID",
                "Version",
                "Status",
                "Authority",
                "Primary source",
                "Specification Layer",
                "Dependencies",
            }:
                value = value.strip().strip("*")
                if key == "Specification ID":
                    key = "Document ID"
                metadata[key] = (i, value)

    return metadata 


def validate_metadata(
    metadata: dict[str, tuple[int, str]],
    chapter: int | None,
    path: Path,
    findings: list[Finding],
) -> None:
    """Validate required metadata fields and their values."""

    for key in ("Document ID", "Version", "Status"):
        if key not in metadata:
            add(
                findings,
                path,
                1,
                "JUFE020",
                "ERROR",
                f"Missing metadata field: {key}.",
            )

    if "Document ID" in metadata:
        ln, value = metadata["Document ID"]
        match = DOCUMENT_ID_PATTERN.match(value)

        if chapter is not None and not match:
            add(
                findings,
                path,
                ln,
                "JUFE021",
                "WARNING",
                f"Non-canonical chapter document ID: {value!r}.",
            )
        elif (
            chapter is not None
            and match
            and int(match.group("chapter")) != chapter
        ):
            add(
                findings,
                path,
                ln,
                "JUFE022",
                "ERROR",
                "Document ID chapter number does not match title.",
            )

    if "Status" in metadata:
        ln, value = metadata["Status"]

        if value.upper() not in KNOWN_STATUSES:
            add(
                findings,
                path,
                ln,
                "JUFE023",
                "WARNING",
                f"Unknown document status: {value!r}.",
            )


def validate_status_fields(
    lines: list[str],
    path: Path,
    findings: list[Finding],
) -> None:
    for i, line in enumerate(lines, 1):
        match = STATUS_FIELD_PATTERN.match(line)
        if match:
            value = match.group(1).strip().strip("*").upper()
            if value not in KNOWN_STATUSES:
                add(
                    findings,
                    path,
                    i,
                    "JUFE024",
                    "WARNING",
                    f"Unknown status value: {value!r}.",
                )    

def validate_blank_runs(lines, path, findings):
    blank_run = 0

    for i, line in enumerate(lines, 1):
        if not line.strip():
            blank_run += 1
            if blank_run == 3:
                add(
                    findings,
                    path,
                    i,
                    "JUFE030",
                    "WARNING",
                    "More than two consecutive blank lines.",
                )
        else:
            blank_run = 0

def collect_headings(
    lines: list[str],
    path: Path,
    findings: list[Finding],
) -> list[tuple[int, int, str]]:
    
    headings = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        check_trailing_whitespace(
            line,
            i,
            path,
            findings,
        )
        
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_PATTERN.match(line)
        if match:
            level, title = len(match.group(1)), match.group(2).strip()
            headings.append((i, level, title))
            
    return headings

def validate_heading_spacing(
    lines: list[str],
    headings: list[tuple[int, int, str]],
    path: Path,
    findings: list[Finding],
) -> None:

    for line_number, _level, _title in headings:

        if line_number > 1 and lines[line_number - 2].strip():
            add(
                findings,
                path,
                line_number,
                "JUFE010",
                "WARNING",
                "Missing blank line before heading.",
            )

        if line_number < len(lines) and lines[line_number].strip():
            add(
                findings,
                path,
                line_number,
                "JUFE011",
                "WARNING",
                "Missing blank line after heading.",
            )
            
def validate_heading_hierarchy(
    headings: list[tuple[int, int, str]],
    path: Path,
    findings: list[Finding],
) -> None:
    """Check for unexpected jumps in heading levels."""

    previous_level = 0

    for line_number, level, title in headings:
        if previous_level and level > previous_level + 1:
            add(
                findings,
                path,
                line_number,
                "JUFE014",
                "WARNING",
                (
                    f"Heading level jumps from {previous_level} "
                    f"to {level}: {title!r}."
                ),
            )

        previous_level = level   

def validate_duplicate_headings(
    headings: list[tuple[int, int, str]],
    path: Path,
    findings: list[Finding],
) -> None:
    """Check for headings with duplicate normalised titles."""

    seen: dict[str, int] = {}

    for line_number, _level, title in headings:
        key = re.sub(r"\s+", " ", title).casefold()

        if key in seen:
            add(
                findings,
                path,
                line_number,
                "JUFE015",
                "WARNING",
                (
                    f"Duplicate heading; first seen on line "
                    f"{seen[key]}: {title!r}."
                ),
            )
        else:
            seen[key] = line_number
def validate_chapter_numbering(
    headings: list[tuple[int, int, str]],
    level_one: list[tuple[int, str]],
    path: Path,
    findings: list[Finding],
) -> int | None:
    """Determine the document chapter and validate heading chapter numbers."""

    chapter = None

    if level_one:
        match = re.search(
            r"\bChapter\s+(\d+)\b",
            level_one[0][1],
            re.IGNORECASE,
        )

        if match:
            chapter = int(match.group(1))

    for line_number, _level, title in headings:
        match = NUMBERED_HEADING_PATTERN.match(title)

        if (
            match
            and chapter is not None
            and int(match.group("chapter")) != chapter
        ):
            add(
                findings,
                path,
                line_number,
                "JUFE016",
                "ERROR",
                (
                    "Heading chapter number does not match "
                    f"document chapter {chapter}."
                ),
            )

    return chapter    



def lint_file(path: Path) -> list[Finding]:
    """Lint a single Markdown file."""
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        add(findings, path, 1, "JUFE000", "ERROR", "File is not valid UTF-8.")
        return findings

    lines = text.splitlines()

    check_final_newline(
        text,
        lines,
        path,
        findings,
    )

    headings = collect_headings(
        lines,
        path,
        findings,
    )

    validate_heading_spacing(
    lines,
    headings,
    path,
    findings,
    )

    level_one = [
        (ln, title)
        for ln, level, title in headings
        if level == 1
    ]
    
    if not level_one:
        add(
            findings,
            path,
            1,
            "JUFE012",
            "ERROR",
            "No level-one document title found.",
    )

    elif len(level_one) > 1:
        for ln, title in level_one[1:]:
            add(
                findings,
                path,
                ln,
                "JUFE013",
                "ERROR",
                f"Additional level-one heading: {title!r}.",
            )

    validate_heading_hierarchy(headings,path,findings)
    validate_duplicate_headings(headings,path,findings)
        
    chapter = validate_chapter_numbering(headings,level_one,path,findings)

    metadata = collect_metadata(lines)
    validate_metadata(metadata, chapter, path, findings)
    validate_status_fields(lines, path, findings)
    validate_blank_runs(lines, path, findings)

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only JUFE Markdown linter.")
    parser.add_argument("target", nargs="?", default="specification")
    args = parser.parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        print(f"ERROR: Target does not exist: {target}", file=sys.stderr)
        return 2
    files = list(markdown_files(target))
    if not files:
        print(f"No Markdown files found under: {target}")
        return 0
    findings = [f for path in files for f in lint_file(path)]
    print("JUFE-Lint v0.1.0")
    print(f"Scanned {len(files)} Markdown file(s).\n")
    if not findings:
        print("PASS — no findings.")
        return 0
    current = None
    for f in sorted(findings, key=lambda x: (str(x.path), x.line, x.code)):
        if f.path != current:
            current = f.path
            print(current)
        print(f"  {f.severity:<7} {f.code} line {f.line}: {f.message}")
    errors = sum(f.severity == "ERROR" for f in findings)
    warnings = sum(f.severity == "WARNING" for f in findings)
    print(f"\nSummary: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
