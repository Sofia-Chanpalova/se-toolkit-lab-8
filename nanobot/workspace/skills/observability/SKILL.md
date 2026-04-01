---
name: observability
description: Use observability MCP tools to investigate errors, logs, and traces
always: true
---

# Observability Skill

Use the observability MCP tools (`obs_*`) to investigate backend errors, logs, and traces when the user asks about service health, failures, or what went wrong.

## Available Tools

| Tool | Purpose | When to use |
|------|---------|-------------|
| `obs_get_recent_errors` | Get recent error logs | User asks about errors, failures, what went wrong |
| `obs_query_logs` | Search logs with LogsQL | Need specific log patterns or time ranges |
| `obs_get_service_health` | Get service health summary | User asks if a service is healthy |
| `obs_get_trace` | Get trace details by ID | Found a trace_id in logs, need full request path |
| `obs_search_traces` | Search for traces | User wants to see recent traces for a service |

## Investigation Strategy

### When user asks "What went wrong?" or "Check system health"

**One-shot investigation flow:**

1. **`obs_get_recent_errors`** — Get error count and recent errors (time_range="10m" for fresh data)
2. **`obs_query_logs`** — If errors found, search for more context on the failing service
3. **Extract trace_id** — From error logs, find the most recent trace_id
4. **`obs_get_trace`** — Fetch the full trace to see the failure path
5. **Summarize** — One coherent explanation citing both log evidence AND trace evidence

**Key discrepancy to notice:**
- Logs/traces show PostgreSQL/SQLAlchemy connection failure
- But HTTP response status might be misreported (e.g., 404 instead of 500)
- Point out this mismatch in your summary

### When user asks about errors

1. **Start with `obs_get_recent_errors`** — Get error count and recent errors for the relevant service
2. **If errors found** — Summarize: count, time, error type, affected operation
3. **If trace_id in error** — Call `obs_get_trace` to see the full request path
4. **Summarize findings** — Don't dump raw JSON, explain what happened

### When user asks about service health

1. **Call `obs_get_service_health`** — Get error rate and request count
2. **Report status** — "healthy" if no errors, "unhealthy" with error details if errors exist

## Response Guidelines

- **Be concise** — Summarize findings, don't dump raw JSON
- **Include timestamps** — When did the error occur?
- **Include trace IDs** — If found, mention them for further investigation
- **Explain impact** — How many requests affected? What operations failed?
- **Suggest next steps** — "Would you like me to check the full trace?" or "Should I look at a different time range?"

## Examples

**User**: "Any LMS backend errors in the last 10 minutes?"
→ Call `obs_get_recent_errors(service="Learning Management Service", time_range="10m")`
→ Summarize: "Found X errors. Most recent at [time]: [error type] during [operation]."

**User**: "Is the backend healthy?"
→ Call `obs_get_service_health(service="Learning Management Service")`
→ Report: "Backend is healthy/unhealthy. X requests, Y errors (Z% error rate) in the last hour."

**User**: "What went wrong with my request?"
→ Call `obs_get_recent_errors(time_range="10m")`
→ If trace_id found: "I found an error with trace ID [id]. Let me fetch the full trace..."
→ Call `obs_get_trace(trace_id="...")`
→ Explain: "The request failed at [step] because [reason]."

**User**: "Show me recent traces for the backend"
→ Call `obs_search_traces(service="Learning Management Service", limit=10)`
→ List trace IDs with timestamps and operations

## Time Ranges

Use appropriate time ranges based on user query:
- "last 10 minutes" → `time_range="10m"`
- "last hour" → `time_range="1h"`
- "today" → `time_range="24h"`
- "recent" → `time_range="1h"` (default)

## Service Names

Common service names in this stack:
- `"Learning Management Service"` — The LMS backend
- `"nanobot"` — The agent gateway
- `"Qwen Code API"` — The LLM proxy
