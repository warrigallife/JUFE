"""
Requirement integrity validator.
"""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "category",
    "title",
    "manuscript_statement",
    "software_requirement",
    "status",
    "implemented_by",
    "open_questions",
}


def validate_register(path: str | Path) -> list[str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[str] = set()

    for index, item in enumerate(data.get("requirements", []), start=1):
        missing = REQUIRED_FIELDS - set(item)
        if missing:
            errors.append(f"Requirement {index} missing fields: {sorted(missing)}")

        requirement_id = item.get("id")
        if requirement_id in seen:
            errors.append(f"Duplicate requirement ID: {requirement_id}")
        seen.add(requirement_id)

        if not item.get("manuscript_statement"):
            errors.append(f"{requirement_id}: empty manuscript statement")
        if not item.get("software_requirement"):
            errors.append(f"{requirement_id}: empty software requirement")

    return errors


if __name__ == "__main__":
    register = Path(__file__).with_name("requirements_register.json")
    errors = validate_register(register)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("Requirements register valid.")
