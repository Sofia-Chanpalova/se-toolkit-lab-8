"""MCP tools for observability queries."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from .client import ObservabilityClient
from .settings import Settings


def register_tools(mcp: FastMCP, client: ObservabilityClient):
    """Register observability tools with the MCP server."""

    @mcp.tool()
    async def obs_query_logs(query: str, time_range: str = "1h") -> str:
        """Query VictoriaLogs using LogsQL.
        
        Use this to search for log entries matching specific criteria.
        
        Args:
            query: LogsQL query (e.g., 'severity:ERROR', 'service.name:"backend"')
            time_range: Time range like '1h', '30m', '24h' (default: '1h')
            
        Returns:
            Formatted log entries or error message
        """
        results = await client.query_logs(query, time_range)
        if not results:
            return "No log entries found matching your query."
        
        lines = []
        for entry in results[:10]:  # Limit to 10 entries
            timestamp = entry.get("_time", "unknown")
            severity = entry.get("severity", "unknown")
            event = entry.get("event", "unknown")
            message = entry.get("_msg", "no message")
            error = entry.get("error", "")
            
            line = f"[{timestamp}] {severity} - {event}: {message}"
            if error:
                line += f" (Error: {error})"
            lines.append(line)
        
        if len(results) > 10:
            lines.append(f"... and {len(results) - 10} more entries")
        
        return "\n".join(lines)

    @mcp.tool()
    async def obs_get_recent_errors(
        service: str | None = None,
        time_range: str = "1h",
    ) -> str:
        """Get recent error logs from VictoriaLogs.
        
        Use this when the user asks about errors, failures, or what went wrong.
        
        Args:
            service: Optional service name (e.g., 'Learning Management Service')
            time_range: Time range like '1h', '30m' (default: '1h')
            
        Returns:
            Formatted error entries
        """
        results = await client.get_recent_errors(service, time_range)
        if not results:
            return f"No errors found in the last {time_range}."
        
        lines = [f"Found {len(results)} error(s) in the last {time_range}:\n"]
        for entry in results[:5]:  # Show top 5 errors
            timestamp = entry.get("_time", "unknown")
            event = entry.get("event", "unknown")
            error = entry.get("error", "unknown error")
            trace_id = entry.get("trace_id", "")
            
            line = f"- [{timestamp}] {event}: {error}"
            if trace_id:
                line += f" (trace: {trace_id[:8]}...)"
            lines.append(line)
        
        if len(results) > 5:
            lines.append(f"\n... and {len(results) - 5} more errors")
        
        return "\n".join(lines)

    @mcp.tool()
    async def obs_get_trace(trace_id: str) -> str:
        """Get details of a specific trace by ID.
        
        Use this when the user provides a trace ID or asks about a specific request.
        
        Args:
            trace_id: The trace ID (e.g., '931ffab4f828fddafd02b205bfdb7cbd')
            
        Returns:
            Trace details with span hierarchy
        """
        result = await client.get_trace(trace_id)
        if "error" in result:
            return f"Trace lookup failed: {result['error']}"
        
        # Format trace data
        spans = result.get("data", {}).get("spans", [])
        if not spans:
            return f"Trace {trace_id} not found or has no spans."
        
        lines = [f"Trace {trace_id}:\n"]
        for span in spans:
            name = span.get("operationName", "unknown")
            duration = span.get("duration", 0)
            tags = span.get("tags", [])
            status = "✓" if not span.get("hasError") else "✗"
            lines.append(f"  {status} {name} ({duration}μs)")
        
        return "\n".join(lines)

    @mcp.tool()
    async def obs_get_service_health(service: str, time_range: str = "1h") -> str:
        """Get health summary for a service.
        
        Use this when the user asks if a service is healthy or about service status.
        
        Args:
            service: Service name (e.g., 'Learning Management Service')
            time_range: Time range for analysis (default: '1h')
            
        Returns:
            Health summary with error rate and status
        """
        result = await client.get_service_health(service, time_range)
        
        status = "✅ healthy" if result["healthy"] else "❌ unhealthy"
        error_rate = result["error_rate"] * 100
        
        return (
            f"Service: {result['service']}\n"
            f"Status: {status}\n"
            f"Time range: {result['time_range']}\n"
            f"Requests: {result['request_count']}\n"
            f"Errors: {result['error_count']}\n"
            f"Error rate: {error_rate:.2f}%"
        )

    @mcp.tool()
    async def obs_search_traces(
        service: str | None = None,
        operation: str | None = None,
        time_range: str = "1h",
        limit: int = 10,
    ) -> str:
        """Search for traces matching criteria.
        
        Use this when the user wants to see recent traces or trace history.
        
        Args:
            service: Optional service name filter
            operation: Optional operation/span name filter
            time_range: Time range (default: '1h')
            limit: Maximum traces to return (default: 10)
            
        Returns:
            List of trace summaries
        """
        results = await client.search_traces(service, operation, time_range, limit)
        if not results:
            return "No traces found matching your criteria."
        
        if "error" in results[0]:
            return f"Trace search failed: {results[0]['error']}"
        
        lines = [f"Found {len(results)} trace(s):\n"]
        for trace in results[:limit]:
            trace_id = trace.get("traceID", "unknown")[:16]
            lines.append(f"- {trace_id}...")
        
        return "\n".join(lines)
