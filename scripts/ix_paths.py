#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Resolve ix-toolkit user data paths without depending on a specific agent."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping
from pathlib import Path

INVENTORY_ENV = "IX_INVENTORY"
MANUALS_ENV = "IX_MANUALS"


def _home(home: Path | None) -> Path:
    return home if home is not None else Path.home()


def _config_home(home: Path, environ: Mapping[str, str]) -> Path:
    value = environ.get("XDG_CONFIG_HOME")
    return Path(value).expanduser() if value else home / ".config"


def _data_home(home: Path, environ: Mapping[str, str]) -> Path:
    value = environ.get("XDG_DATA_HOME")
    return Path(value).expanduser() if value else home / ".local" / "share"


def inventory_candidates(
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
    script_dir: Path | None = None,
) -> tuple[Path, ...]:
    """Return existing-file candidates in compatibility priority order."""
    env = os.environ if environ is None else environ
    user_home = _home(home)
    candidates = [
        _config_home(user_home, env) / "ix-toolkit" / "ix-devices.json",
        user_home / ".claude" / "ix-devices.json",
    ]
    if script_dir is not None:
        # Kept last for compatibility with early standalone-script installations.
        candidates.append(script_dir / "ix-devices.json")
    return tuple(candidates)


def inventory_path(
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
    script_dir: Path | None = None,
) -> Path | None:
    """Resolve inventory: environment override, neutral path, then legacy paths."""
    env = os.environ if environ is None else environ
    override = env.get(INVENTORY_ENV)
    if override:
        return Path(override).expanduser()
    for candidate in inventory_candidates(home=home, environ=env, script_dir=script_dir):
        if candidate.is_file():
            return candidate
    return None


def manuals_path(
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Resolve manuals: environment override, neutral path, then legacy Claude path.

    If no directory exists, return the neutral path so diagnostics and generation
    commands point users at the preferred location.
    """
    env = os.environ if environ is None else environ
    override = env.get(MANUALS_ENV)
    if override:
        return Path(override).expanduser()
    user_home = _home(home)
    neutral = _data_home(user_home, env) / "ix-toolkit" / "manuals"
    legacy = user_home / ".claude" / "ix-manuals"
    if neutral.is_dir():
        return neutral
    if legacy.is_dir():
        return legacy
    return neutral


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve ix-toolkit user data paths")
    parser.add_argument("kind", choices=("inventory", "manuals"))
    parser.add_argument(
        "--require-existing",
        action="store_true",
        help="fail if the resolved file or directory does not exist",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.kind == "inventory":
        path = inventory_path(script_dir=Path(__file__).resolve().parent)
        if path is None:
            path = inventory_candidates()[0]
        exists = path.is_file()
    else:
        path = manuals_path()
        exists = path.is_dir()
    print(path)
    if args.require_existing and not exists:
        print(f"ERROR: {args.kind} path not found: {path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
