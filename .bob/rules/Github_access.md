# Guide to use the Github Access

## There's only a few github option available, which are
"GITHUB_GET_THE_AUTHENTICATED_USER", "GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER",
"GITHUB_GET_A_REPOSITORY", "GITHUB_GET_REPOSITORY_CONTENT", "GITHUB_GET_A_TREE",
"GITHUB_LIST_BRANCHES", "GITHUB_LIST_COMMITS", "GITHUB_GET_A_COMMIT",
"GITHUB_LIST_REPOSITORY_ISSUES", "GITHUB_GET_AN_ISSUE", "GITHUB_LIST_ISSUE_COMMENTS",
"GITHUB_LIST_PULL_REQUESTS", "GITHUB_GET_A_PULL_REQUEST", "GITHUB_LIST_PULL_REQUESTS_FILES",
"GITHUB_SEARCH_CODE", "GITHUB_SEARCH_REPOSITORIES", "GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS",
"GITHUB_CREATE_AN_ISSUE", "GITHUB_UPDATE_AN_ISSUE", "GITHUB_CREATE_AN_ISSUE_COMMENT",
"GITHUB_CREATE_BRANCH", "GITHUB_CREATE_OR_UPDATE_FILE_CONTENTS", "GITHUB_COMMIT_MULTIPLE_FILES",
"GITHUB_CREATE_A_PULL_REQUEST", "GITHUB_UPDATE_A_PULL_REQUEST",
"GITHUB_CREATE_A_REVIEW_FOR_A_PULL_REQUEST",

Other than those option, the MCP server will return a permission error

## Input format

The input is a single line of text separated by the `,` (comma) character:

```
TOOL_SLUG, key=value, key=value
```

- The **first** item (before the first `,`) is always the tool name (one of the options above).
- Every item **after** it is an argument written as `key=value`.
- Items are separated by `,`. Spaces around each `,` are ignored.
- Tools that need no arguments only need the tool name.
- Values must **not** contain a `,`, since it is the separator.
- Quotes around a value (e.g. `q='filebrowser'`) are optional and are removed automatically.

## Examples

No arguments:
```
GITHUB_GET_THE_AUTHENTICATED_USER
```

Search repositories:
```
GITHUB_SEARCH_REPOSITORIES, q=filebrowser
GITHUB_SEARCH_REPOSITORIES, q=filebrowser, per_page=5
```

Search code:
```
GITHUB_SEARCH_CODE, q=composio repo:langflow-ai/langflow
```

Get a repository:
```
GITHUB_GET_A_REPOSITORY, owner=filebrowser, repo=filebrowser
```

List branches:
```
GITHUB_LIST_BRANCHES, owner=filebrowser, repo=filebrowser
```

List commits:
```
GITHUB_LIST_COMMITS, owner=filebrowser, repo=filebrowser, per_page=5
```

List issues:
```
GITHUB_LIST_REPOSITORY_ISSUES, owner=filebrowser, repo=filebrowser, state=open
```

Get an issue:
```
GITHUB_GET_AN_ISSUE, owner=filebrowser, repo=filebrowser, issue_number=1
```

Create an issue:
```
GITHUB_CREATE_AN_ISSUE, owner=youruser, repo=yourrepo, title=Bug report
```
