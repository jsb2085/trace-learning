"""Mock MCP server stub (for future real MCP integration)."""

from __future__ import annotations

from trace_learning.mock.mcp.tools import MOCK_MCP_TOOLS, get_mcp_tools


class MockMCPServer:
    """Placeholder MCP server that exposes our mock tools.

    When we wire up a real MCP transport, this class becomes the adapter
    between MCP protocol messages and the underlying tool implementations.
    """

    def __init__(self) -> None:
        self.tools = get_mcp_tools()

    def list_tools(self) -> list[dict]:
        return [
            {"name": t.name, "description": t.description}
            for t in self.tools
        ]

    def call_tool(self, name: str, arguments: dict) -> str:
        for tool in self.tools:
            if tool.name == name:
                return str(tool.invoke(arguments))
        raise ValueError(f"Unknown MCP tool: {name}")
