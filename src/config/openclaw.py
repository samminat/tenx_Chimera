"""OpenClaw integration helpers.

Provides utilities to detect the `openclaw` CLI, load authentication
credentials (e.g. `OPENCLAW_API_KEY`) from a `.env` file, and invoke
basic status checks (`openclaw models status`). This module is intentionally
lightweight and only depends on the existing `config_loader.parse_dotenv` to
help load env files used by OpenClaw.

See: https://docs.openclaw.ai/gateway/authentication
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Iterable, Optional, Tuple

from .config_loader import parse_dotenv

logger = logging.getLogger(__name__)


class OpenClawError(RuntimeError):
    """Raised for OpenClaw specific failures."""


def openclaw_cli_path() -> Optional[str]:
    """Return full path to `openclaw` CLI if available, otherwise None."""
    return shutil.which("openclaw")


def check_openclaw_cli() -> bool:
    """Return True if `openclaw` CLI is discoverable on PATH."""
    path = openclaw_cli_path()
    if path:
        logger.debug("Found openclaw CLI at %s", path)
        return True
    logger.debug("openclaw CLI not found on PATH")
    return False


def load_env_for_openclaw(dotenv_path: str | Path = "~/.openclaw/.env", override: bool = False) -> dict:
    """Load environment variables from the given dotenv into os.environ.

    By default this prefers the per-user OpenClaw env file `~/.openclaw/.env`.
    Returns the mapping loaded.
    """
    path = Path(dotenv_path).expanduser()
    logger.debug("Loading OpenClaw .env from %s (override=%s)", path, override)
    try:
        return parse_dotenv(path, override=override)
    except Exception as exc:  # preserve parse_dotenv's behavior
        raise OpenClawError(f"Failed to load dotenv {path}: {exc}") from exc


def get_openclaw_api_key() -> Optional[str]:
    """Return the `OPENCLAW_API_KEY` from environment, or None if unset."""
    return os.environ.get("OPENCLAW_API_KEY")


def run_openclaw_models_status(args: Iterable[str] | None = None, timeout: float = 15.0) -> Tuple[int, str]:
    """Invoke `openclaw models status` and return (exit_code, stdout+stderr).

    - If the `openclaw` CLI is not found, raises `OpenClawError`.
    - `args` may include additional flags like `--check`.
    """
    if not check_openclaw_cli():
        raise OpenClawError("openclaw CLI not found on PATH")

    cmd = ["openclaw", "models", "status"]
    if args:
        cmd.extend(list(args))

    logger.debug("Running command: %s", " ".join(cmd))
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = (proc.stdout or "") + (proc.stderr or "")
        logger.debug("openclaw exit=%s; output=%s", proc.returncode, out)
        return proc.returncode, out
    except subprocess.TimeoutExpired as te:
        raise OpenClawError(f"openclaw command timed out: {te}") from te
    except OSError as oe:
        raise OpenClawError(f"Failed to execute openclaw CLI: {oe}") from oe


__all__ = [
    "OpenClawError",
    "openclaw_cli_path",
    "check_openclaw_cli",
    "load_env_for_openclaw",
    "get_openclaw_api_key",
    "run_openclaw_models_status",
]
