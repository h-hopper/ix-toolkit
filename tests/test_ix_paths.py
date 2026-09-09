import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ix_paths  # noqa: E402


class InventoryPathTests(unittest.TestCase):
    def test_environment_override_wins_even_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            neutral = home / ".config" / "ix-toolkit" / "ix-devices.json"
            neutral.parent.mkdir(parents=True)
            neutral.write_text("{}", encoding="utf-8")
            override = home / "elsewhere.json"

            actual = ix_paths.inventory_path(
                home=home, environ={"IX_INVENTORY": str(override)}
            )

            self.assertEqual(actual, override)

    def test_neutral_inventory_precedes_legacy_claude_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            neutral = home / ".config" / "ix-toolkit" / "ix-devices.json"
            legacy = home / ".claude" / "ix-devices.json"
            neutral.parent.mkdir(parents=True)
            legacy.parent.mkdir(parents=True)
            neutral.write_text("{}", encoding="utf-8")
            legacy.write_text("{}", encoding="utf-8")

            actual = ix_paths.inventory_path(home=home, environ={})

            self.assertEqual(actual, neutral)

    def test_legacy_claude_inventory_remains_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            legacy = home / ".claude" / "ix-devices.json"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("{}", encoding="utf-8")

            actual = ix_paths.inventory_path(home=home, environ={})

            self.assertEqual(actual, legacy)


class ManualsPathTests(unittest.TestCase):
    def test_environment_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            override = Path(tmp) / "manual-corpus"
            actual = ix_paths.manuals_path(
                home=Path(tmp), environ={"IX_MANUALS": str(override)}
            )
            self.assertEqual(actual, override)

    def test_neutral_manuals_precede_legacy_claude_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            neutral = home / ".local" / "share" / "ix-toolkit" / "manuals"
            legacy = home / ".claude" / "ix-manuals"
            neutral.mkdir(parents=True)
            legacy.mkdir(parents=True)

            actual = ix_paths.manuals_path(home=home, environ={})

            self.assertEqual(actual, neutral)

    def test_legacy_claude_manuals_remain_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            legacy = home / ".claude" / "ix-manuals"
            legacy.mkdir(parents=True)

            actual = ix_paths.manuals_path(home=home, environ={})

            self.assertEqual(actual, legacy)

    def test_missing_manuals_reports_error_without_affecting_other_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            stderr = io.StringIO()
            original = ix_paths.manuals_path
            ix_paths.manuals_path = lambda: Path(tmp) / "missing"
            try:
                with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(
                    io.StringIO()
                ):
                    status = ix_paths.main(["manuals", "--require-existing"])
            finally:
                ix_paths.manuals_path = original

            self.assertEqual(status, 1)
            self.assertIn("manuals path not found", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
