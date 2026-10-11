# AIOps Deployment & Diagnostic Tool

## What This Tool Does

This tool executes a raw Python script against remote infrastructure, you can use SSH. It will returns structured diagnostic telemetry. It is used by Bob to:

- **Deploy** services to remote Linux hosts (Docker Compose, systemd, shell scripts)
- **Diagnose** infrastructure issues (check container state, read logs, inspect services, verify ports)
- **Remediate** problems by running corrective commands over SSH
- **Verify** deployments with health checks and readiness probes

## How to Use It

Pass a raw Python script as `input_value`. No JSON wrapping, no markdown code fences — plain Python only.

### Pre-injected Global Modules

Do **not** include `import` statements. The following modules are available as globals:

| Module | Use for |
|---|---|
| `requests` | HTTP calls (Doppler, health checks) |
| `paramiko` | SSH connections and SFTP |
| `io` | In-memory file operations (e.g. PEM key parsing) |
| `json` | JSON parsing |
| `urllib` | URL utilities |
| `time` | Sleeps, retries |

### Secret Management

Secrets are **not** hardcoded. Fetch them at runtime from Doppler using the pre-injected `DOPPLER_SERVICE_TOKEN` global:

```python
response = requests.get(
    "https://api.doppler.com/v3/configs/config/secrets/download?format=json",
    headers={"Authorization": f"Bearer {DOPPLER_SERVICE_TOKEN}"},
    timeout=15
)
secrets = response.json()
```

Then resolve keys dynamically — do not assume exact key names. Use inspection or fallback matching:

```python
# Example: find the SSH host key
host_key = next((k for k in secrets if "HOST" in k or "IP" in k or "ADDRESS" in k), None)
host = secrets[host_key]
```


## Output

The tool passes all `stdout`/`stderr` from script execution to a Diagnostic Agent, which returns a structured telemetry report containing:

- **STATUS**: `SUCCESS` or `FAILURE`
- **ERROR CATEGORY**: Classification of any error
- **SUMMARY**: What happened
- **ROOT CAUSE**: Why it failed (if applicable)
- **REMEDIATION CODE**: Fix script to apply (if applicable)

---

## Important Constraints

- Scripts must be **idempotent** where possible (`docker compose down` before `up`, `mkdir` with exception handling)
- Long-running commands (e.g. `docker compose pull`) should be **backgrounded** with `&` and logged to a file to avoid SSH timeout
- SSH connections must be **closed** at the end of the script (`client.close()`)
- Never hardcode secrets — always fetch from Doppler at runtime
