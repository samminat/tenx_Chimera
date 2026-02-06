#!/usr/bin/env python3
"""Minimal runtime check for Tenx MCP Sense telemetry.

Checks:
- logs/ directory exists and is writable
- TENX_MCP_SENSE_ENDPOINT and TENX_MCP_SENSE_API_KEY are present in env
- Endpoint connectivity (HEAD request) without sending api_key

This script intentionally does not transmit secrets.
"""
from __future__ import annotations

import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def check_logs_dir(path: str = "logs") -> None:
    p = Path(path)
    if not p.exists():
        print(f"INFO: creating logs directory at {p}")
        p.mkdir(parents=True, exist_ok=True)
    # test writability
    try:
        test_file = p / ".mcp_write_test"
        with test_file.open("w", encoding="utf-8") as fh:
            fh.write("ok")
        test_file.unlink()
    except Exception as e:
        print(f"ERROR: logs directory not writable: {e}")
        sys.exit(2)
    print(f"OK: logs directory present and writable: {p}")


def check_env_vars() -> tuple[str, str]:
    endpoint = os.environ.get("TENX_MCP_SENSE_ENDPOINT")
    api_key = os.environ.get("TENX_MCP_SENSE_API_KEY")
    missing = []
    if not endpoint:
        missing.append("TENX_MCP_SENSE_ENDPOINT")
    if not api_key:
        missing.append("TENX_MCP_SENSE_API_KEY")
    if missing:
        print(f"ERROR: missing environment variables: {', '.join(missing)}")
        sys.exit(3)
    print("OK: required env vars present (TENX_MCP_SENSE_ENDPOINT, TENX_MCP_SENSE_API_KEY)")
    return endpoint, api_key


def check_connectivity(endpoint: str) -> None:
    # Make a HEAD request without Authorization header to verify reachability
    try:
        req = urllib.request.Request(endpoint, method="HEAD")
        # add a small identifying header but do not include secrets
        req.add_header("User-Agent", "tenx-mcp-sense-check/1.0")
        with urllib.request.urlopen(req, timeout=5) as resp:
            code = resp.getcode()
            print(f"OK: endpoint reachable, status={code}")
    except urllib.error.HTTPError as he:
        print(f"WARN: endpoint returned HTTP error {he.code}")
    except Exception as e:
        print(f"ERROR: failed to reach endpoint: {e}")
        sys.exit(4)


def main() -> None:
    check_logs_dir()
    endpoint, _ = check_env_vars()
    check_connectivity(endpoint)


if __name__ == "__main__":
    main()
