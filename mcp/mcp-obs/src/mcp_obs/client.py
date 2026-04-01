"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx
from .settings import Settings


class ObservabilityClient:
    """Client for querying VictoriaLogs and VictoriaTraces."""

    def __init__(self, settings: Settings):
        self.victorialogs_url = settings.victorialogs_url
        self.victoriatraces_url = settings.victoriatraces_url
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self._client.aclose()

    async def query_logs(self, query: str, time_range: str = "1h") -> list[dict]:
        """Query VictoriaLogs using LogsQL.
        
        Args:
            query: LogsQL query string (e.g., 'severity:ERROR')
            time_range: Time range (e.g., '1h', '30m', '24h')
            
        Returns:
            List of log entries as dictionaries
        """
        url = f"{self.victorialogs_url}/select/logsql/query"
        params = {"query": f"_time:{time_range} {query}"}
        
        try:
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            # VictoriaLogs returns newline-delimited JSON
            lines = response.text.strip().split('\n')
            results = []
            for line in lines:
                if line.strip():
                    import json
                    try:
                        results.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return results
        except httpx.HTTPError as e:
            return [{"error": f"Query failed: {str(e)}"}]

    async def get_recent_errors(self, service: str | None = None, time_range: str = "1h") -> list[dict]:
        """Get recent error logs, optionally filtered by service.
        
        Args:
            service: Optional service name filter
            time_range: Time range (e.g., '1h', '30m')
            
        Returns:
            List of error log entries
        """
        query = "severity:ERROR"
        if service:
            query = f'service.name:"{service}" severity:ERROR'
        return await self.query_logs(query, time_range)

    async def get_trace(self, trace_id: str) -> dict:
        """Get a trace by ID from VictoriaTraces.
        
        Args:
            trace_id: The trace ID to look up
            
        Returns:
            Trace data with spans
        """
        url = f"{self.victoriatraces_url}/api/v1/traces/{trace_id}"
        try:
            response = await self._client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Trace lookup failed: {str(e)}"}

    async def search_traces(
        self,
        service: str | None = None,
        operation: str | None = None,
        time_range: str = "1h",
        limit: int = 20,
    ) -> list[dict]:
        """Search for traces matching criteria.
        
        Args:
            service: Optional service name filter
            operation: Optional operation/span name filter
            time_range: Time range (e.g., '1h', '30m')
            limit: Maximum number of traces to return
            
        Returns:
            List of trace summaries
        """
        url = f"{self.victoriatraces_url}/api/v1/traces"
        params = {"limit": limit}
        
        # Note: VictoriaTraces API may have different query parameters
        # This is a basic implementation
        try:
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            return response.json().get("data", [])
        except httpx.HTTPError as e:
            return [{"error": f"Trace search failed: {str(e)}"}]

    async def get_service_health(self, service: str, time_range: str = "1h") -> dict:
        """Get health summary for a service.
        
        Args:
            service: Service name
            time_range: Time range for analysis
            
        Returns:
            Health summary with error count, request count, etc.
        """
        logs = await self.get_recent_errors(service, time_range)
        error_count = len(logs)
        
        # Get total request count from logs
        all_logs = await self.query_logs(f'service.name:"{service}"', time_range)
        request_count = sum(1 for log in all_logs if log.get("event") == "request_started")
        
        return {
            "service": service,
            "time_range": time_range,
            "error_count": error_count,
            "request_count": request_count,
            "error_rate": error_count / max(request_count, 1),
            "healthy": error_count == 0,
        }
