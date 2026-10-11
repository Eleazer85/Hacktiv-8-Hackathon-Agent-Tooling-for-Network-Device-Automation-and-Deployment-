# Hacktiv8 Hackathon — Agent Tooling for Network Device Automation and Deployment

A Langflow-based AI agent platform that integrates **GitHub**, **MikroTik shell**, **Alpine shell**,**Python Interpreter**, and **web search** actions via the [Composio](https://composio.dev) SDK, enabling AI agents to automate network device deployment and management directly from a Langflow pipeline.

---

## Features

### GitHub Actions
Execute GitHub API actions directly from a Langflow agent flow via the [Composio](https://composio.dev) SDK. A custom Langflow component (`github_custom_component.py`) wraps the Composio GitHub tools behind an allowlist, so only approved operations can be triggered. Credentials are passed securely through a `SecretStrInput` field — never exposed in the flow graph.

### MikroTik Shell
Send RouterOS commands to a MikroTik router over SSH from within a Langflow agent flow. The agent connects to the router using SSH credentials and executes commands directly on RouterOS, enabling automated network configuration and monitoring.

### Alpine Shell
Run shell commands on a lightweight Alpine Linux container (`agent-shell`) over SSH. The sidecar container is provisioned alongside Langflow via Docker Compose, giving the agent a sandboxed Linux environment to execute scripts, install packages, or inspect the host network.

### Python Interpreter
Executes raw Python scripts against remote infrastructure over SSH directly from within the Langflow pipeline. Designed for AIOps tasks—such as deploying services via Docker Compose, inspecting container status, analyzing logs, and running network health checks. Integrates natively with Doppler for dynamic, runtime secret injection to ensure zero hardcoded credentials.

### Web Search
Perform live web searches from within a Langflow agent flow, enabling the agent to look up documentation, error messages, or current events as part of an automated workflow.

### Containerized Stack
The entire platform runs as a Docker Compose stack — a custom Langflow image built on `langflowai/langflow` and a sidecar `linuxserver/openssh-server` container networked together. SSH key-based auth is used throughout; no passwords are stored.

---

## Project Structure

```
.
├── custom_component/
│   └── github_custom_component.py   # Langflow custom component for GitHub via Composio
├── langflow_flow/
│   ├── Github access.json           # Composio GitHub agent flow
│   ├── Python Interpreter.json      # AIOps deploy/diagnose flow with optional Doppler secrets
│   ├── shell_MikroTik.json          # MikroTik shell agent flow
│   ├── shell_alpine.json            # Alpine shell agent flow
│   └── web_search.json              # Web search agent flow
├── Dockerfile                       # Custom image built on langflowai/langflow
├── docker_compose.yml               # Full stack: Langflow + OpenSSH server
├── LICENSE
└── README.md
```

---

## Requirements

- Docker & Docker Compose

For local development without Docker:

- Python 3.10+
- [Langflow](https://github.com/langflow-ai/langflow)

```bash
pip install composio composio_langchain lfx-bundles requests paramiko librouteros
```

---

## SSH Key Setup

The OpenSSH server (`agent-shell`) uses key-based authentication only. Generate a dedicated key pair before starting the stack:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/<your_key_name> -N "" -C "langflow-agent"
```

Replace `<your_key_name>` with whatever name you want (e.g. `my_agent_key`).

This creates:
- `~/.ssh/<your_key_name>` — private key
- `~/.ssh/<your_key_name>.pub` — public key

Then update the volume paths in `docker_compose.yml` to match your chosen key name:

```yaml
# Under langflow service:
- ~/.ssh/<your_key_name>:/app/keys/agent_key:ro

# Under openssh-server service:
- ~/.ssh/<your_key_name>.pub:/keys/agent_key.pub:ro
```

---

## Docker Setup

### 1. Build the custom Langflow image

```bash
docker build -t <your_image_name> .
```

### 2. Update `docker_compose.yml`

Replace the image placeholder with your built image name:

```yaml
# docker_compose.yml
image: <your_image_name>   # was: <dockerfile_image>
```

### 3. Pull the OpenSSH server image

```bash
docker pull linuxserver/openssh-server:latest
```

### 4. Start the full stack

```bash
docker compose -f docker_compose.yml up
```

Then open **http://127.0.0.1:7860** in your browser.

| Service | Container | Port |
|---|---|---|
| Langflow | `langflow` | `127.0.0.1:7860` |
| OpenSSH server | `agent-shell` | internal only |

> SSH access uses key-based auth only (`~/.ssh/agent_key`). Use `/app/keys/agent_key` as the key path inside the Langflow container.

---

## Python Interpreter — Doppler Setup (Optional)

The `Python Interpreter.json` flow supports fetching secrets at runtime from [Doppler](https://doppler.com). To use it, paste your **Doppler Service Token** into the `DOPPLER_SERVICE_TOKEN` input of the flow.

> If you skip Doppler, provide credentials directly as Langflow Global Variables or component inputs instead.

---

## Usage

### Import flows

1. Open Langflow at `http://127.0.0.1:7860`
2. Go to **My Flows** → **Import**
3. Import any flow from the `langflow_flow/` directory

### GitHub Custom Component Inputs

| Input | Type | Description |
|---|---|---|
| `tools_choosen` | `MessageTextInput` | The GitHub tool slug to execute |
| `API_KEY` | `SecretStrInput` | Your Composio API key |

### Component Output

Returns a `Data` object containing the result of the GitHub API call, or an error message if the tool slug is not in the allowlist.

---

## MikroTik Connection Setup

To use the MikroTik shell agent flow, your router must be reachable over the network and configured to accept SSH connections.

### 1. Requirements

- A MikroTik router or device running **RouterOS**
- Network access from the machine running this stack to the router's IP address

### 2. Enable SSH on RouterOS

Connect to your MikroTik via Winbox, WebFig, or its existing console, then run:

```routeros
/ip service enable ssh
/ip service set ssh port=22
```

Confirm SSH is active:

```routeros
/ip service print
```

Look for `ssh` with status `enabled`.

### 3. (Optional) Restrict SSH access by IP

To allow SSH only from your host machine:

```routeros
/ip service set ssh address=<your_host_ip>/32
```

### 4. (Optional) Set a strong password or use key-based auth

```routeros
# Set password for the admin user
/user set admin password=<your_password>
```

For key-based auth, import your public key:

```routeros
/user ssh-keys import public-key-file=<your_key_name>.pub user=admin
```

### 5. Test the connection from your host

```bash
ssh admin@<mikrotik_ip>
```

Once confirmed, use the same credentials inside the Langflow MikroTik shell flow (`shell_MikroTik.json`).

---

## Allowed GitHub Tools

| Category | Tools |
|---|---|
| **User** | `GITHUB_GET_THE_AUTHENTICATED_USER` |
| **Repositories** | `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`, `GITHUB_GET_A_REPOSITORY`, `GITHUB_GET_REPOSITORY_CONTENT`, `GITHUB_GET_A_TREE` |
| **Branches & Commits** | `GITHUB_LIST_BRANCHES`, `GITHUB_LIST_COMMITS`, `GITHUB_GET_A_COMMIT` |
| **Issues** | `GITHUB_LIST_REPOSITORY_ISSUES`, `GITHUB_GET_AN_ISSUE`, `GITHUB_LIST_ISSUE_COMMENTS`, `GITHUB_CREATE_AN_ISSUE`, `GITHUB_UPDATE_AN_ISSUE`, `GITHUB_CREATE_AN_ISSUE_COMMENT` |
| **Pull Requests** | `GITHUB_LIST_PULL_REQUESTS`, `GITHUB_GET_A_PULL_REQUEST`, `GITHUB_LIST_PULL_REQUESTS_FILES`, `GITHUB_CREATE_A_PULL_REQUEST`, `GITHUB_UPDATE_A_PULL_REQUEST`, `GITHUB_CREATE_A_REVIEW_FOR_A_PULL_REQUEST` |
| **Search** | `GITHUB_SEARCH_CODE`, `GITHUB_SEARCH_REPOSITORIES`, `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS` |
| **Files** | `GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS`, `GITHUB_COMMIT_MULTIPLE_FILES` |
| **Branches** | `GITHUB_CREATE_BRANCH` |

---

## Bob MCP Server Guide

Once the stack is running, you can connect [IBM Bob](https://www.ibm.com/products/bob) to Langflow as an MCP server so Bob can invoke your agent flows directly from the IDE.

### Steps

1. **Open Langflow** at `http://127.0.0.1:7860`.
2. Go to **Settings** → **MCP Server**.
3. Copy the MCP server URL shown on that page.
4. Open **IBM Bob** in your IDE.
5. Click the **Settings** icon (⚙️) in the Bob panel and navigate to the **MCP** tab.
6. Click **Add MCP Server** and paste the URL you copied from Langflow.
7. Give the server a name (e.g. `langflow`) and save.
8. Bob connects to the server automatically — your Langflow flows now appear as callable tools inside Bob.

### Usage

Once connected, you can ask Bob things like:

- *"Run the MikroTik shell flow and list all firewall rules."*
- *"Use the Python Interpreter flow to check the container status on the remote host."*
- *"Trigger the GitHub flow to list open pull requests on my repo."*

Bob will route the request to the correct Langflow flow via MCP without you having to open the Langflow UI.

> **Tip:** To disable the MCP server without removing it, set `"disabled": true` in `.bob/mcp.json` under the server entry.

---

## License

See [LICENSE](LICENSE) for details.
