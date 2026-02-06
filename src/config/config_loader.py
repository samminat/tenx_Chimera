"""Configuration loader utilities for Project Chimera.

- Loads variables from a `.env` file (simple parser, no external dependency).
- Loads YAML configuration files from a `config/` directory.
- Resolves `${ENV_VAR}` placeholders in string values using environment variables.
- Validates required keys (dot-separated) and raises clear startup errors.

This module purposely implements only configuration concerns — no business logic.

Designed for Python 3.11.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping
import logging

logger = logging.getLogger(__name__)

try:
    import yaml
except Exception as exc:  # pragma: no cover - defensive import message
    yaml = None  # type: ignore


class ConfigError(RuntimeError):
    """Raised when configuration cannot be loaded or validated."""


_ENV_PLACEHOLDER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


def parse_dotenv(path: str | Path = ".env", override: bool = False) -> Dict[str, str]:
    """Parse a simple .env file and inject variables into os.environ.

    - Lines beginning with # are ignored.
    - Supports KEY=VALUE or KEY="value" or KEY='value'.
    - Does not evaluate variables in values.

    Returns the mapping of variables loaded.
    """
    path = Path(path)
    loaded: Dict[str, str] = {}
    if not path.exists():
        logger.debug("No .env file found at %s", path)
        return loaded

    with path.open("r", encoding="utf-8") as fh:
        for i, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                logger.debug("Skipping malformed .env line %s:%d", path, i)
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            # strip optional quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if override or key not in os.environ:
                os.environ[key] = val
            loaded[key] = val
            logger.debug("Loaded .env %s=%s", key, val)
    return loaded


def _deep_merge(base: dict, extra: dict) -> dict:
    """Recursively merge extra into base and return base (modified in-place)."""
    for key, val in extra.items():
        if (
            key in base
            and isinstance(base[key], dict)
            and isinstance(val, dict)
        ):
            _deep_merge(base[key], val)
        else:
            base[key] = val
    return base


def load_yaml_files(config_dir: str | Path = "config") -> dict:
    """Load all YAML files from the provided directory and deep-merge them.

    Raises ConfigError if PyYAML is not installed or if the config directory has no YAML files.
    """
    if yaml is None:
        raise ConfigError("PyYAML is required to load YAML config files (install with 'pip install pyyaml').")

    config_dir = Path(config_dir)
    if not config_dir.exists() or not config_dir.is_dir():
        raise ConfigError(f"Configuration directory not found: {config_dir}")

    result: dict[str, Any] = {}
    yaml_files = sorted(config_dir.glob("*.yaml")) + sorted(config_dir.glob("*.yml"))
    if not yaml_files:
        raise ConfigError(f"No YAML configuration files found in: {config_dir}")

    for f in yaml_files:
        try:
            with f.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            if not isinstance(data, dict):
                raise ConfigError(f"Top-level YAML document must be a mapping in {f}")
            _deep_merge(result, data)
            logger.debug("Loaded config file: %s", f)
        except yaml.YAMLError as ye:  # pragma: no cover - YAML parsing error path
            raise ConfigError(f"Failed to parse YAML file {f}: {ye}") from ye
    return result


def _resolve_placeholders_in_str(s: str, env: Mapping[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in env:
            raise ConfigError(f"Missing environment variable for placeholder: ${{{name}}}")
        return env[name]

    return _ENV_PLACEHOLDER.sub(repl, s)


def resolve_placeholders(obj: Any, env: Mapping[str, str] | None = None) -> Any:
    """Recursively resolve ${ENV_VAR} placeholders in strings within the provided object.

    Raises ConfigError if a referenced environment variable is not set.
    """
    if env is None:
        env = os.environ

    if isinstance(obj, str):
        # quick check for presence of placeholder
        if "${" in obj:
            return _resolve_placeholders_in_str(obj, env)
        return obj
    if isinstance(obj, dict):
        return {k: resolve_placeholders(v, env) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve_placeholders(i, env) for i in obj]
    return obj


def _get_by_path(mapping: Mapping[str, Any], path: str) -> Any:
    parts = path.split(".")
    cur: Any = mapping
    for p in parts:
        if not isinstance(cur, Mapping) or p not in cur:
            raise KeyError(path)
        cur = cur[p]
    return cur


def validate_required_keys(config: Mapping[str, Any], required: Iterable[str]) -> None:
    """Ensure the provided dot-separated keys are present in the configuration.

    Raises ConfigError listing all missing keys.
    """
    missing: list[str] = []
    for key in required:
        try:
            val = _get_by_path(config, key)
            if val is None:
                missing.append(key)
        except KeyError:
            missing.append(key)
    if missing:
        raise ConfigError(f"Missing required configuration keys: {', '.join(missing)}")


def load_config(
    config_dir: str | Path = "config",
    dotenv_path: str | Path = ".env",
    required_keys: Iterable[str] | None = None,
    override_dotenv: bool = False,
) -> dict:
    """Load configuration following these steps:

    1. Parse and inject `.env` into environment (non-destructive unless `override_dotenv=True`).
    2. Load and deep-merge YAML config files from `config_dir`.
    3. Resolve ${ENV_VAR} placeholders using the current environment.
    4. Validate presence of `required_keys` (if provided).

    Returns the final config dictionary.
    """
    parse_dotenv(dotenv_path, override=override_dotenv)
    config = load_yaml_files(config_dir)

    # Resolve placeholders within the config
    config = resolve_placeholders(config)

    if required_keys:
        validate_required_keys(config, required_keys)

    logger.info("Configuration loaded from %s", config_dir)
    return config


__all__ = [
    "ConfigError",
    "parse_dotenv",
    "load_yaml_files",
    "resolve_placeholders",
    "validate_required_keys",
    "load_config",
]
