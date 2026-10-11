# Hacktiv8 Hackathon — Agent Tooling for Network Device Automation and Deployment

A Langflow-based custom component that integrates **GitHub actions** via the [Composio](https://composio.dev) SDK, enabling AI agents to interact with GitHub repositories directly from a Langflow pipeline.

---

## Features

- Execute GitHub API actions through a Langflow custom component
- Secure API key input via `SecretStrInput`
- Allowlist-based tool filtering to prevent unauthorized GitHub actions
- Returns structured `Data` objects for downstream Langflow components

---

## Project Structure

```
.
├── github_custom_component.py   # Main Langflow custom component
├── Dockerfile                   # Container image built on langflowai/langflow
├── Github access.json           # Composio GitHub tool config
├── shell_MikroTik.json          # MikroTik shell tool config
├── shell_alpine.json            # Alpine shell tool config
├── web_search.json              # Web search tool config
└── README.md
```

---

## Requirements

- Python 3.10+
- [Langflow](https://github.com/langflow-ai/langflow)
- [Composio](https://pypi.org/project/composio/)
- [composio-langchain](https://pypi.org/project/composio-langchain/)

Install dependencies:
```bash
pip install composio composio_langchain lfx-bundles requests paramiko librouteros
```

---

## Docker Setup

Build and run using the provided Dockerfile:

```bash
docker build -t hackathon-agent .
docker run -p 7860:7860 hackathon-agent
```

---

## Usage

### Component Inputs

| Input | Type | Description |
|---|---|---|
| `tools_choosen` | `MessageTextInput` | The GitHub tool slug to execute |
| `API_KEY` | `SecretStrInput` | Your Composio API key |

### Component Output

Returns a `Data` object containing the result of the GitHub API call, or an error message if the tool slug is not in the allowlist.

---

## Allowed GitHub Tools

The component restricts execution to the following tools:

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

## License

See [LICENSE](LICENSE) for details.
