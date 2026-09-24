"""
Focused regression tests for JUFE runtime boot validation.

Covers two defects identified in the boot-validation audit:

1. `SpecificationValidator` was rejecting any specification with no
   `DEF-` prefixed lines, even though SPEC-001 ("JUFE Specification
   Standard") lists "Definitions" as an OPTIONAL section. This made
   `JUFERuntime.boot()` fail unconditionally, since SPEC-010 (like
   SPEC-001/020/030/040) is a process specification with no
   Definitions section.
2. `JUFERuntime.boot()` referenced the specification path using the
   lowercase directory name `specifications/`, while the directory on
   disk is `Specifications/`. This resolves only on case-insensitive
   filesystems (e.g. default macOS/Windows) and fails on
   case-sensitive filesystems (e.g. Linux, most CI).
"""

from __future__ import annotations

import os
import unittest
from pathlib import Path

from src.parser import ParsedSpecification
from src.runtime import JUFERuntime
from src.validator import SpecificationValidator

REPO_ROOT = Path(__file__).resolve().parent.parent


class SpecificationValidatorDefinitionsTests(unittest.TestCase):
    """SPEC-001 makes 'Definitions' an optional section."""

    def setUp(self):
        self.validator = SpecificationValidator()

    def _spec(self, definitions):
        return ParsedSpecification(
            title="Sample Specification",
            content="# Sample Specification\n\nBody text.",
            version="1.0",
            definitions=definitions,
        )

    def test_empty_definitions_are_accepted(self):
        """A process specification with no DEF- lines must still validate."""

        self.assertTrue(self.validator.validate(self._spec([])))

    def test_duplicate_definitions_still_rejected(self):
        """The duplicate-identifier guard must remain enforced."""

        with self.assertRaises(ValueError):
            self.validator.validate(self._spec(["DEF-0001", "DEF-0001"]))

    def test_missing_title_still_rejected(self):
        """Unrelated mandatory checks must be unaffected by this fix."""

        spec = ParsedSpecification(
            title="",
            content="body",
            version="1.0",
            definitions=[],
        )

        with self.assertRaises(ValueError):
            self.validator.validate(spec)


class RuntimeBootPathCasingTests(unittest.TestCase):
    """The boot path must match the on-disk directory name exactly."""

    def test_boot_path_matches_actual_directory_case(self):
        """
        Path.exists() silently case-folds on case-insensitive
        filesystems, masking a bad reference. This test instead reads
        the literal directory entry names so it fails the same way on
        every filesystem, regardless of OS case-sensitivity.
        """

        source = Path("src/runtime.py").read_text(encoding="utf-8")

        marker = 'self.execute(\n            "'
        start = source.index(marker) + len(marker)
        end = source.index('"', start)
        referenced_path = source[start:end]

        referenced_dir = referenced_path.split("/", 1)[0]

        on_disk_entries = os.listdir(REPO_ROOT)

        self.assertIn(
            referenced_dir,
            on_disk_entries,
            f"runtime.py references directory {referenced_dir!r}, which "
            f"does not literally exist on disk (case-sensitive check); "
            f"available: {[e for e in on_disk_entries if e.lower() == referenced_dir.lower()]}",
        )


class RuntimeBootTests(unittest.TestCase):
    """End-to-end confirmation that boot() completes successfully."""

    def test_boot_succeeds(self):
        runtime = JUFERuntime()

        result = runtime.boot()

        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["specification"], "SPEC-010: Specification Loader")


if __name__ == "__main__":
    unittest.main()
