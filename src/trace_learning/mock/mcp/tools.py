"""Mock MCP tool definitions.

These simulate tools exposed by an MCP server. Because we control the
implementation, expected outputs in the eval dataset are deterministic.
"""

from __future__ import annotations

from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Tool input schemas
# ---------------------------------------------------------------------------


class ReadFileInput(BaseModel):
    path: str = Field(description="Relative path inside the mock filesystem")


class SearchFilesInput(BaseModel):
    query: str = Field(description="Search term for filenames or content")
    directory: str = Field(default="/", description="Directory to search under")


class GetUserInput(BaseModel):
    user_id: str = Field(description="User identifier, e.g. u-001")


# ---------------------------------------------------------------------------
# Mock filesystem (deterministic — used by eval expected outputs)
# ---------------------------------------------------------------------------

MOCK_FILESYSTEM: dict[str, str] = {
    "docs/onboarding.md": "# Onboarding\nComplete the security training within 7 days.",
    "docs/policies/remote-work.md": "# Remote Work\nEmployees may work remotely up to 3 days per week.",
    "config/app.json": '{"env": "staging", "max_retries": 3}',
    "logs/deploy.txt": "2026-08-01 deploy succeeded\n2026-08-15 deploy succeeded",
}

MOCK_USERS: dict[str, dict[str, str]] = {
    "u-001": {"name": "Alice Chen", "team": "platform", "role": "engineer"},
    "u-002": {"name": "Bob Rivera", "team": "data", "role": "analyst"},
    "u-003": {"name": "Carol Wu", "team": "platform", "role": "manager"},
}


def _read_file(path: str) -> str:
    content = MOCK_FILESYSTEM.get(path)
    if content is None:
        return f"Error: file not found — {path}"
    return content


def _search_files(query: str, directory: str = "/") -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for path, content in MOCK_FILESYSTEM.items():
        if directory != "/" and not path.startswith(directory.lstrip("/")):
            continue
        if query.lower() in path.lower() or query.lower() in content.lower():
            results.append({"path": path, "snippet": content[:120]})
    return results


def _get_user(user_id: str) -> dict[str, Any]:
    user = MOCK_USERS.get(user_id)
    if user is None:
        return {"error": f"User not found: {user_id}"}
    return {"user_id": user_id, **user}


# ---------------------------------------------------------------------------
# LangChain tool exports
# ---------------------------------------------------------------------------

MOCK_MCP_TOOLS = [
    StructuredTool.from_function(
        func=_read_file,
        name="mcp_read_file",
        description="Read a file from the mock MCP filesystem.",
        args_schema=ReadFileInput,
    ),
    StructuredTool.from_function(
        func=_search_files,
        name="mcp_search_files",
        description="Search the mock MCP filesystem by filename or content.",
        args_schema=SearchFilesInput,
    ),
    StructuredTool.from_function(
        func=_get_user,
        name="mcp_get_user",
        description="Look up a user record from the mock MCP user directory.",
        args_schema=GetUserInput,
    ),
]


def get_mcp_tools() -> list[StructuredTool]:
    return list(MOCK_MCP_TOOLS)
