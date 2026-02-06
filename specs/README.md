# Spec Kit Integration

This project includes a basic scaffold for integrating with GitHub Spec Kit.

Install locally (recommended via pip from the authoritative repo):

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade "git+https://github.com/github/spec-kit.git"
# or run one-off via uvx (see spec-kit README):
uvx --from git+https://github.com/github/spec-kit.git specify --help
```

Run checks (example):

```bash
specify check
specify validate --config specs/spec-kit.yaml
```

If you prefer the npm path and the package is published, use the npm examples in the upstream README. If the npm package is private, authenticate with `npm login` or install from a Git URL as needed.

Files added:
- `specs/spec-kit.yaml` — sample config for the spec kit tooling

Telemetry integration:

- `.mcp/telemetry.yaml` — Tenx MCP Sense configuration (placeholders used for secrets).

Runtime notes:

- Ensure `logs/` exists and is writable before running agents.
- Populate the following environment variables (see `.env.sample`):
	- `TENX_MCP_SENSE_ENDPOINT` — MCP Sense HTTP endpoint (e.g., https://mcppulse.10academy.org/proxy)
	- `TENX_MCP_SENSE_API_KEY` — API key placeholder (do not commit secrets)

Check the `.mcp/telemetry.yaml` file for details on enabled features (request/response tracing, agent lifecycle, supervisor and safety monitoring).

Next steps:
- Replace sample fields in `specs/spec-kit.yaml` with the authoritative configuration from the Spec Kit docs.
- Optionally add a CI workflow to run Spec Kit on push/pull_request.
