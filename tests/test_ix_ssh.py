import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location("ix_ssh", SCRIPTS / "ix-ssh.py")
assert SPEC and SPEC.loader
ix_ssh = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ix_ssh)


class ArgumentParsingTests(unittest.TestCase):
    def test_show_and_target_arguments(self):
        args = ix_ssh.parse_args(
            ["--device", "router-a", "show version", "show interfaces"]
        )
        self.assertEqual(args.device, "router-a")
        self.assertEqual(args.shows, ["show version", "show interfaces"])

    def test_inventory_argument_is_available(self):
        args = ix_ssh.parse_args(["--inventory", "inventory.json", "--list"])
        self.assertEqual(args.inventory, "inventory.json")
        self.assertTrue(args.list)


class InventoryBehaviorTests(unittest.TestCase):
    def test_missing_inventory_file_is_an_explicit_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.json"
            with mock.patch.object(ix_ssh, "inventory_path", return_value=missing):
                with self.assertRaises(SystemExit) as raised:
                    ix_ssh.load_inventory()
        self.assertIn("inventory file not found", str(raised.exception))

    def test_inventory_listing_never_prints_password_value(self):
        secret = "do-not-print-this-value"
        output = ix_ssh.format_inventory(
            {
                "router-a": {
                    "host": "192.0.2.1",
                    "username": "operator",
                    "password": secret,
                }
            },
            Path("inventory.json"),
        )
        self.assertNotIn(secret, output)
        self.assertIn("auth=inventory-password", output)

    def test_cli_inventory_override_is_used_by_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            inventory = Path(tmp) / "inventory.json"
            inventory.write_text(
                '{"devices":{"router-a":{"host":"192.0.2.1",'
                '"username":"operator","password":"do-not-print"}}}',
                encoding="utf-8",
            )
            stdout = io.StringIO()
            previous = os.environ.get("IX_INVENTORY")
            try:
                with contextlib.redirect_stdout(stdout):
                    ix_ssh.main(["--inventory", str(inventory), "--list"])
            finally:
                if previous is None:
                    os.environ.pop("IX_INVENTORY", None)
                else:
                    os.environ["IX_INVENTORY"] = previous

            self.assertIn("router-a", stdout.getvalue())
            self.assertNotIn("do-not-print", stdout.getvalue())

    def test_no_target_is_never_inferred(self):
        args = ix_ssh.parse_args(["show version"])
        with mock.patch.object(ix_ssh, "load_inventory", return_value=({}, None)):
            with self.assertRaises(SystemExit) as raised:
                ix_ssh.resolve_target(args)
        self.assertIn("no target selected", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
