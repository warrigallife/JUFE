"""
JUFE / ABTM Specification Engine
================================

Loads the requirements register and reports:
- defined requirements
- implementation coverage
- unresolved items
- category/status summaries
- readiness for future engine work
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


class SpecificationEngine:
    def __init__(self, register_path: str | Path | None = None) -> None:
        self.register_path = Path(register_path or Path(__file__).with_name("requirements_register.json"))
        self.data = json.loads(self.register_path.read_text(encoding="utf-8"))
        self.requirements = self.data["requirements"]

    def get(self, requirement_id: str) -> dict[str, Any]:
        for requirement in self.requirements:
            if requirement["id"] == requirement_id:
                return requirement
        raise KeyError(f"Unknown requirement: {requirement_id}")

    def category_summary(self) -> dict[str, int]:
        return dict(Counter(item["category"] for item in self.requirements))

    def status_summary(self) -> dict[str, int]:
        return dict(Counter(item["status"] for item in self.requirements))

    def unresolved_requirements(self) -> list[dict[str, Any]]:
        return [
            item for item in self.requirements
            if item.get("open_questions")
        ]

    def implemented_requirements(self) -> list[dict[str, Any]]:
        return [
            item for item in self.requirements
            if item.get("implemented_by")
        ]

    def unimplemented_requirements(self) -> list[dict[str, Any]]:
        return [
            item for item in self.requirements
            if not item.get("implemented_by")
        ]

    def coverage(self) -> dict[str, Any]:
        total = len(self.requirements)
        implemented = len(self.implemented_requirements())
        unresolved = len(self.unresolved_requirements())

        return {
            "total_requirements": total,
            "implemented_requirements": implemented,
            "implementation_coverage_percent": round((implemented / total) * 100, 2) if total else 0.0,
            "requirements_with_open_questions": unresolved,
            "fully_resolved_requirements": total - unresolved,
        }

    def report(self) -> str:
        coverage = self.coverage()
        lines = [
            "JUFE / ABTM SPECIFICATION REPORT",
            "=" * 64,
            f"Register version            : {self.data['version']}",
            f"Total requirements          : {coverage['total_requirements']}",
            f"Implementation coverage     : {coverage['implementation_coverage_percent']}%",
            f"Requirements with questions : {coverage['requirements_with_open_questions']}",
            f"Fully resolved requirements : {coverage['fully_resolved_requirements']}",
            "",
            "CATEGORY SUMMARY",
            "-" * 64,
        ]

        for category, count in sorted(self.category_summary().items()):
            lines.append(f"{category:20} {count}")

        lines.extend(["", "STATUS SUMMARY", "-" * 64])

        for status, count in sorted(self.status_summary().items()):
            lines.append(f"{status:24} {count}")

        lines.extend(["", "OPEN QUESTIONS", "-" * 64])

        for item in self.unresolved_requirements():
            lines.append(f"{item['id']} — {item['title']}")
            for question in item["open_questions"]:
                lines.append(f"  • {question}")
            lines.append("")

        return "\n".join(lines)


if __name__ == "__main__":
    print(SpecificationEngine().report())
