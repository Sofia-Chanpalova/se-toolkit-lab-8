"""MCP server for observability data (VictoriaLogs and VictoriaTraces)."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .client import ObservabilityClient
from .settings import Settings
from .tools import register_tools


# Create MCP server
mcp = FastMCP("mcp-obs")


# Initialize client on server startup
settings = Settings()
client = ObservabilityClient(settings)

# Register tools with the MCP server
register_tools(mcp, client)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
