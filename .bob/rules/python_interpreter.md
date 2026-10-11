---
name: aiops-deployment-tool
description: Use when the user wants to deploy, diagnose, or remediate remote infrastructure using the AIOps deployment MCP tool — covers script patterns for Docker Compose, Docker Run, systemd, Node.js/npm, port diagnostics, and secret management via Doppler.
---

# AIOps Deployment & Diagnostic Tool

This skill provides instructions for using the `deployment_tool_with_diagnosti` MCP tool to execute Python scripts against remote infrastructure via SSH.

## Key Rules

1. **No `import` statements** — modules are pre-injected: `requests`, `paramiko`, `io`, `subprocess`, `json`, `urllib`, `time`.
2. **No hardcoded secrets** — always fetch from Doppler at runtime using `DOPPLER_SERVICE_TOKEN`.
3. **Pass raw Python only** — no JSON wrapping, no markdown code fences in `input_value`.
4. **Always close the SSH connection** — call `client.close()` at the end of every script.
5. **Background long-running commands** — `docker compose pull` or large installs must be backgrounded with `&` and logged to a file to avoid SSH timeout.

## Step 1 — Fetch Secrets from Doppler

Always start every script with this block:

```python
response = requests.get(
    "https://api.doppler.com/v3/configs/config/secrets/download?format=json",
    headers={"Authorization": f"Bearer {DOPPLER_SERVICE_TOKEN}"},
    timeout=15
)
if response.status_code != 200:
    raise RuntimeError(f"Failed to fetch Doppler secrets: {response.status_code} {response.text}")
secrets = response.json()
```

Resolve key names dynamically — do not assume exact names:

```python
host_key = next((k for k in secrets if "HOST" in k or "IP" in k or "ADDRESS" in k), None)
user_key = next((k for k in secrets if "USER" in k), None)
pem_key  = next((k for k in secrets if "PEM" in k or "KEY" in k), None)

host     = secrets[host_key]
username = secrets[user_key]
pem      = secrets[pem_key]
```

## Step 2 — Establish SSH Connection

```python
pkey = paramiko.RSAKey.from_private_key(io.StringIO(pem))
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=username, pkey=pkey, timeout=30)
```

## Step 3 — Choose a Script Pattern

### Docker Compose Deployment

```python
compose_content = """services:
  myapp:
    image: myimage:latest
    container_name: myapp
    restart: always
    ports:
      - "8080:8080"
"""
sftp = paramiko.SFTPClient.from_transport(client.get_transport())
try:
    sftp.mkdir(f"/home/{username}/myapp")
except Exception:
    pass
sftp.putfo(io.StringIO(compose_content), f"/home/{username}/myapp/docker-compose.yml")
sftp.close()

cmd = f"""
set -e
cd /home/{username}/myapp
sudo docker compose down 2>/dev/null || true
sudo docker compose pull > /tmp/deploy.log 2>&1 &
wait
sudo docker compose up -d
echo "Done"
"""
_, out, err = client.exec_command(cmd, timeout=300)
print(out.read().decode())
```

### Docker Run (single container)

```python
cmd = (
    "sudo docker run -d "
    "--name myapp --restart always "
    "-p 8080:8080 myimage:latest"
)
_, out, _ = client.exec_command(cmd, timeout=60)
print(out.read().decode())
```

### systemd Service Deployment

```python
unit = """[Unit]
Description=My App
After=network.target

[Service]
ExecStart=/usr/bin/node /opt/myapp/index.js
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
"""
sftp = paramiko.SFTPClient.from_transport(client.get_transport())
sftp.putfo(io.StringIO(unit), "/tmp/myapp.service")
sftp.close()

cmds = """
sudo mv /tmp/myapp.service /etc/systemd/system/myapp.service
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl restart myapp
"""
_, out, err = client.exec_command(cmds, timeout=30)
print(out.read().decode())
```

### Node.js / npm Deployment (PM2)

```python
cmds = """
set -e
cd /opt/myapp
npm install --production
pm2 restart myapp || pm2 start index.js --name myapp
pm2 save
"""
_, out, err = client.exec_command(cmds, timeout=120)
print(out.read().decode())
if err:
    print("STDERR:", err.read().decode())
```

### Port / Network Diagnostic (`ss -tlnp`)

```python
_, out, _ = client.exec_command("ss -tlnp", timeout=10)
print(out.read().decode())

# Check a specific port
_, out, _ = client.exec_command("ss -tlnp | grep :3001", timeout=10)
result = out.read().decode()
print(result if result else "Nothing listening on port 3001")
```

### systemd Diagnostic

```python
_, out, _ = client.exec_command("sudo systemctl status myapp --no-pager", timeout=10)
print(out.read().decode())

_, out, _ = client.exec_command("sudo journalctl -u myapp --since '10 minutes ago' --no-pager", timeout=10)
print(out.read().decode())
```

### Docker Container Diagnostic

```python
_, out, _ = client.exec_command("sudo docker ps", timeout=10)
print(out.read().decode())

_, out, _ = client.exec_command("sudo docker inspect --format='{{.State.Status}}' myapp", timeout=10)
print(out.read().decode())

_, out, _ = client.exec_command("sudo docker logs --tail 50 myapp", timeout=10)
print(out.read().decode())
```

### Docker Remediation

```python
# Restart
_, out, _ = client.exec_command("sudo docker restart myapp", timeout=30)
print(out.read().decode())

# Remove and recreate
_, out, _ = client.exec_command(
    "sudo docker rm -f myapp && sudo docker run -d --name myapp --restart always myimage:latest",
    timeout=60
)
print(out.read().decode())
```

### Process / Resource Diagnostic

```python
_, out, _ = client.exec_command("ps aux --sort=-%cpu | head -20", timeout=10)
print(out.read().decode())

_, out, _ = client.exec_command("df -h", timeout=10)
print(out.read().decode())

_, out, _ = client.exec_command("free -h", timeout=10)
print(out.read().decode())
```

### Firewall Diagnostic

```python
_, out, _ = client.exec_command("sudo ufw status verbose", timeout=10)
print(out.read().decode())
```

### HTTP Readiness Probe

```python
print("Waiting for service...")
for i in range(10):
    try:
        r = requests.get(f"http://{host}:8080", timeout=5)
        if r.status_code < 500:
            print(f"Service ready! Status: {r.status_code}")
            break
    except Exception:
        pass
    time.sleep(5)
    print(f"Retry {i+1}/10...")
else:
    print("Warning: service did not respond within timeout.")
```

## Step 4 — Close the Connection

Always end the script with:

```python
client.close()
print(f"\nService accessible at: http://{host}:<port>")
```

## Tool Output

The tool returns a structured diagnostic report:
- **STATUS**: `SUCCESS` or `FAILURE`
- **ERROR CATEGORY**: Classification of the error
- **SUMMARY**: What happened
- **ROOT CAUSE**: Why it failed (if applicable)
- **REMEDIATION CODE**: Fix script to apply (if applicable)