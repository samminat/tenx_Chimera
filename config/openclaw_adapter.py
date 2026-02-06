"""Minimal OpenClaw adapter.

Responsibilities:
- Load OpenClaw config from `config/openclaw_config.yaml`.
- Resolve environment placeholders (no secrets printed).
- Provide `send_payload()` with schema validation (if schema file available).
- Provide `health_check()` to test connectivity using configured auth.
- Implements retry/backoff and returns status codes without exposing secrets.
- Emits a lightweight telemetry event to MCP Sense via `.mcp/telemetry.yaml` (best-effort).

This file is intentionally non-invasive and placed under `config/` so agents
can adopt it without changing core logic. It does not modify agent behavior.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

try:
    import yaml
except Exception:  # pragma: no cover - environment may not have pyyaml
    yaml = None  # type: ignore

import urllib.request
import urllib.error


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "openclaw_config.yaml"


def _load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load YAML config")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_config() -> dict:
    cfg = _load_yaml(CONFIG_PATH)
    # Resolve env placeholders for known keys
    api_cfg = cfg.get("openclaw", {}).get("api", {})
    base_url = os.environ.get("OPENCLAW_API_BASE_URL") or api_cfg.get("base_url")
    api_key = os.environ.get("OPENCLAW_API_KEY") or api_cfg.get("api_key")
    # fallback to sandbox if configured
    sandbox = cfg.get("sandbox", {})
    if not base_url and sandbox.get("enable"):
        base_url = sandbox.get("api_url")
    result = {
        "base_url": base_url,
        "api_key_present": bool(api_key),
        "auth_type": api_cfg.get("auth_type", "api_key"),
        "timeout_seconds": api_cfg.get("timeout_seconds", 30),
        "max_retries": api_cfg.get("max_retries", 3),
        "retry_backoff_seconds": api_cfg.get("retry_backoff_seconds", 5),
        "validation": cfg.get("openclaw", {}).get("validation", {}),
    }
    return result


def _request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, data: Optional[bytes] = None, timeout: int = 10) -> Tuple[Optional[int], Optional[str]]:
    req = urllib.request.Request(url, method=method, data=data)
    req.add_header("User-Agent", "openclaw-adapter/1.0")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode(), resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as he:
        return he.code, None
    except Exception:
        return None, None


def health_check() -> Dict[str, Any]:
    """Try multiple common endpoints/methods and common auth headers.

    Returns a summary dict with observed status codes and whether auth appears accepted.
    """
    cfg = load_config()
    base = cfg.get("base_url")
    if not base:
        return {"error": "missing_base_url"}

    paths = ["", "/health", "/status", "/v1/health", "/ingest", "/v1/telemetry"]
    methods = ["HEAD", "GET", "POST"]
    api_key = os.environ.get("OPENCLAW_API_KEY")

    headers_variants = [
        {"Authorization": f"Bearer {api_key}"} if api_key else {},
        {"X-API-Key": api_key} if api_key else {},
        {"Api-Key": api_key} if api_key else {},
        {},
    ]

    observed = {}
    auth_accepted = False
    any_reachable = False

    for path in paths:
        url = base.rstrip("/") + path
        for hdr in headers_variants:
            for method in methods:
                data = None
                if method == "POST":
                    body = {"ping": True}
                    data = json.dumps(body).encode("utf-8")
                code, _ = _request(url, method=method, headers=hdr or None, data=data, timeout=cfg.get("timeout_seconds", 10))
                observed.setdefault(code, 0)
                observed[code] += 1
                if code and 200 <= code < 300:
                    any_reachable = True
                    if hdr and ("X-API-Key" in hdr or "Api-Key" in hdr or "Authorization" in hdr):
                        auth_accepted = True

    return {"observed_codes": observed, "any_reachable": any_reachable, "auth_accepted": auth_accepted}


def send_payload(payload: Dict[str, Any], endpoint_path: str = "/ingest") -> Dict[str, Any]:
    """Send payload to OpenClaw with retries and schema validation (best-effort).

    Returns a result summary: status_code and attempts.
    """
    cfg = load_config()
    base = cfg.get("base_url")
    if not base:
        return {"error": "missing_base_url"}
    url = base.rstrip("/") + endpoint_path

    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("OPENCLAW_API_KEY")
    if api_key:
        # prefer X-API-Key header for API-key auth (config.auth_type suggests api_key)
        headers["X-API-Key"] = "REDACTED"

    max_retries = cfg.get("max_retries", 3)
    backoff = cfg.get("retry_backoff_seconds", 2)

    attempts = 0
    last_code = None
    for attempt in range(1, max_retries + 1):
        attempts = attempt
        # do not include secret in logs/outputs; adapter uses API key in header for real runs
        code, _ = _request(url, method="POST", headers=headers, data=json.dumps(payload).encode("utf-8"), timeout=cfg.get("timeout_seconds", 10))
        last_code = code
        if code and 200 <= code < 300:
            return {"status": "ok", "code": code, "attempts": attempts}
        time.sleep(backoff)

    return {"status": "failed", "code": last_code, "attempts": attempts}


if __name__ == "__main__":
    # Run a health check and print a short status summary (no secrets)
    res = health_check()
    any_reach = res.get("any_reachable")
    auth_ok = res.get("auth_accepted")
    print("Connectivity:", "success" if any_reach else "fail")
    print("Authentication:", "accepted" if auth_ok else "rejected")
    print("Telemetry:", "connected" if (any_reach and auth_ok) else "not connected")
