import os
import unittest
from pathlib import Path
from unittest.mock import patch

from ix_ssh.infrastructure.permissions import _allowed_windows_sids, _trusted_windows_users, fix_command


class WindowsPermissionPolicyTest(unittest.TestCase):
    def test_trusted_executor_names_are_trimmed_and_deduplicated(self):
        with patch.dict(os.environ, {"IX_SSH_TRUSTED_WINDOWS_USERS": " runner ;RUNNER; second "}):
            self.assertEqual(_trusted_windows_users(), ["runner", "second"])

    def test_fix_command_grants_current_and_trusted_executor(self):
        with (
            patch("ix_ssh.infrastructure.permissions.os.name", "nt"),
            patch("ix_ssh.infrastructure.permissions._current_windows_user", return_value="interactive-user"),
            patch("ix_ssh.infrastructure.permissions._trusted_windows_users", return_value=["sandbox-user"]),
        ):
            command = fix_command(Path("devices.json"))
        self.assertIn('"interactive-user:F"', command)
        self.assertIn('"sandbox-user:F"', command)

    def test_owner_system_admin_and_current_process_user_are_allowed(self):
        with (
            patch("ix_ssh.infrastructure.permissions._current_windows_user_sid", return_value="S-1-5-21-current"),
            patch("ix_ssh.infrastructure.permissions._trusted_windows_user_sids", return_value={"S-1-5-21-trusted"}),
        ):
            allowed = _allowed_windows_sids("S-1-5-21-owner")
        self.assertEqual(allowed, {"S-1-5-18", "S-1-5-32-544", "S-1-5-21-owner", "S-1-5-21-current", "S-1-5-21-trusted"})

    def test_unresolved_current_process_user_does_not_broaden_policy(self):
        with (
            patch("ix_ssh.infrastructure.permissions._current_windows_user_sid", return_value=""),
            patch("ix_ssh.infrastructure.permissions._trusted_windows_user_sids", return_value=set()),
        ):
            allowed = _allowed_windows_sids("S-1-5-21-owner")
        self.assertEqual(allowed, {"S-1-5-18", "S-1-5-32-544", "S-1-5-21-owner"})


if __name__ == "__main__":
    unittest.main()
