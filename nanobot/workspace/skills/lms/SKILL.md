---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to fetch and present live course data.

## Available Tools

- `mcp_lms_lms_health` - Check backend health (no params)
- `mcp_lms_lms_labs` - List all available labs (no params)
- `mcp_lms_lms_learners` - Get learner roster (no params)
- `mcp_lms_lms_pass_rates` - Get pass rates per task (requires `lab`)
- `mcp_lms_lms_timeline` - Get daily submission counts (requires `lab`)
- `mcp_lms_lms_groups` - Get per-group performance (requires `lab`)
- `mcp_lms_lms_top_learners` - Get top N learners (requires `lab`, optional `limit`)
- `mcp_lms_lms_completion_rate` - Get completion percentage (requires `lab`)
- `mcp_lms_lms_sync_pipeline` - Trigger ETL sync (no params)

## Strategy

### When lab is NOT specified

If the user asks for scores, pass rates, completion, groups, timeline, or top learners **without naming a lab**:

1. Call `mcp_lms_lms_labs` first to get the list of available labs
2. If multiple labs exist, ask the user to choose one
3. Use each lab's `title` field as the user-facing label
4. Pass the `id` field (e.g., `lab-01`) as the `lab` parameter to other tools

### When lab IS specified

If the user names a specific lab:

1. Map the user's lab name to the lab ID using `mcp_lms_lms_labs` if needed
2. Call the appropriate analytics tool with the `lab` parameter
3. Format numeric results as percentages or counts

### Response Formatting

- **Percentages**: Show as `93.9%` not `0.939`
- **Tables**: Use markdown tables for multi-row data
- **Health**: Include item count from health check
- **Keep responses concise**

### Examples

**User**: "Show me the scores"
→ Call `lms_labs` first, then ask "Which lab would you like to see scores for?"

**User**: "Is the LMS healthy?"
→ Call `lms_health`
→ Respond: "Yes, the LMS backend is healthy! It's currently tracking X items."

**User**: "What's the pass rate for Lab 01?"
→ Call `lms_pass_rates` with `lab: "lab-01"`
→ Show task-by-task breakdown

**User**: "What can you do?"
→ Explain: "I can query the LMS backend for live data: lab listings, learner rosters, score distributions, pass rates, completion rates, group performance, submission timelines, and top performers. Just ask about any lab by name, or say 'show me the labs' to see all available labs."
