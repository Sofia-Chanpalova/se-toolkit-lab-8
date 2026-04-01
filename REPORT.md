# Lab 8 — Report

## Task 1A — Bare agent

### Checkpoint 1: "What is the agentic loop?"

**Command:** `uv run nanobot agent --logs --session cli:task1a-loop -c ./config.json -m "What is the agentic loop?"`

**Response:**

> The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It typically consists of these core stages:
>
> **The Basic Loop**
>
> 1. **Perceive** — Gather information about the current state (read files, check outputs, observe environment)
> 2. **Think/Reason** — Analyze the situation, plan next steps, make decisions
> 3. **Act** — Execute actions using available tools (write files, run commands, call APIs)
> 4. **Observe** — Check the results of actions, detect errors or changes
> 5. **Repeat** — Continue the loop until the goal is achieved or a stopping condition is met
>
> **Key Characteristics**
>
> - **Autonomy**: The agent decides what to do next without constant human guidance
> - **Iteration**: Multiple loop cycles may be needed for complex tasks
> - **Feedback-driven**: Each action's outcome informs the next decision
> - **Goal-oriented**: The loop continues until the objective is met
>
> **Example in Practice**
>
> For a task like "fix the bug in this code":
>
> 1. Perceive: Read the code file and error logs
> 2. Think: Identify the bug and plan a fix
> 3. Act: Edit the file to apply the fix
> 4. Observe: Run tests to verify the fix works
> 5. Repeat: If tests fail, diagnose and try again
>
> This loop is what distinguishes agents from simple chatbots—agents can take multi-step actions and adapt based on outcomes rather than just responding once.

### Checkpoint 2: "What labs are available in our LMS?"

**Command:** `uv run nanobot agent --logs --session cli:task1a-labs -c ./config.json -m "What labs are available in our LMS?"`

**Response (NO real backend data - MCP not configured yet):**

> Based on my exploration of the workspace, here's what I found about the available labs in your LMS:
>
> **Available Labs**
>
> Lab 1 (se-toolkit-lab-8) is the current lab in your workspace. It contains:
>
> **Required Tasks:**
> - Task 1 through Task 5 (5 required tasks)
>
> **Optional Tasks:**
> - Task 1 (1 optional task)
>
> **Lab Structure:**
> - `/root/se-toolkit-lab-8/lab/` - Main lab directory with:
>   - `tasks/required/` - Required task instructions
>   - `tasks/optional/` - Optional task instructions
>   - `setup/` - Setup files
>   - `images/` - Lab images
> - `/root/se-toolkit-lab-8/wiki/lab-1/` - Lab documentation and resources
>
> The lab appears to be a Software Engineering toolkit focused on learning with AI assistants, coding agents, and collaborative work under TA supervision. The repository name is se-toolkit-lab-8.

**Note:** The agent inspected local repo files but could NOT query the live LMS backend (no MCP server connected at this stage).

---

## Task 1B — Agent with LMS tools

### MCP Server Configuration

Added `mcp-lms` to nanobot's dependencies in `nanobot/pyproject.toml`:

```toml
[project]
dependencies = [
    "mcp-lms",
    "nanobot-ai",
]

[tool.uv.sources]
mcp-lms = { workspace = true, editable = true }
```

Configured MCP server in `nanobot/config.json`:

```json
"mcpServers": {
  "lms": {
    "command": "uv",
    "args": [
      "--directory",
      "/root/se-toolkit-lab-8/mcp/mcp-lms",
      "run",
      "python",
      "-m",
      "mcp_lms.server"
    ],
    "env": {
      "NANOBOT_LMS_BACKEND_URL": "http://localhost:42002",
      "NANOBOT_LMS_API_KEY": "my-secret-api-key"
    }
  }
}
```

**9 MCP tools registered:**
- `mcp_lms_lms_health` - Check backend health
- `mcp_lms_lms_labs` - List available labs
- `mcp_lms_lms_learners` - Get learner roster
- `mcp_lms_lms_pass_rates` - Get pass rates per task
- `mcp_lms_lms_timeline` - Get submission timeline
- `mcp_lms_lms_groups` - Get per-group performance
- `mcp_lms_lms_top_learners` - Get top performers
- `mcp_lms_lms_completion_rate` - Get completion percentage
- `mcp_lms_lms_sync_pipeline` - Trigger ETL sync

### Checkpoint 1: "What labs are available?"

**Command:** `uv run nanobot agent --logs --session cli:task1b-labs -c ./config.json -m "What labs are available?"`

**Response (REAL backend data):**

> Here are the available labs:
>
> | ID | Lab Title |
> |----|-----------|
> | 1 | Lab 01 – Products, Architecture & Roles |
> | 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |
> | 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
> | 4 | Lab 04 — Testing, Front-end, and AI Agents |
> | 5 | Lab 05 — Data Pipeline and Analytics Dashboard |
> | 6 | Lab 06 — Build Your Own Agent |
> | 7 | Lab 07 — Build a Client with an AI Coding Agent |
> | 8 | lab-08 |
>
> There are 8 labs available in total.

### Checkpoint 2: "Is the LMS backend healthy?"

**Command:** `uv run nanobot agent --logs --session cli:task1b-health -c ./config.json -m "Is the LMS backend healthy?"`

**Response (REAL health status from LMS tool):**

> Yes, the LMS backend is healthy! It's currently tracking 56 items.

---

## Task 1C — Skill prompt

### Skill File

**Location:** `nanobot/workspace/skills/lms/SKILL.md`

**Frontmatter:**
```yaml
---
name: lms
description: Use LMS MCP tools for live course data
always: true
---
```

### Skill Strategy

The skill teaches the agent:
1. Which LMS MCP tools are available and when to use each
2. To call `lms_labs` first when a lab parameter is needed but not provided
3. To ask the user which lab they want when not specified
4. To format numeric results as percentages (e.g., `93.9%` not `0.939`)
5. To use lab titles as user-facing labels
6. To keep responses concise

### Checkpoint: "Show me the scores"

**Command:** `uv run nanobot agent --logs --session cli:task1c -c ./config.json -m "Show me the scores"`

**Response (agent lists labs and asks which one):**

> I'll check what labs are available first.
>
> Here are the available labs:
>
> | Lab ID | Title |
> |--------|-------|
> | lab-01 | Lab 01 – Products, Architecture & Roles |
> | lab-02 | Lab 02 — Run, Fix, and Deploy a Backend Service |
> | lab-03 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
> | lab-04 | Lab 04 — Testing, Front-end, and AI Agents |
> | lab-05 | Lab 05 – Data Pipeline and Analytics Dashboard |
> | lab-06 | Lab 06 – Build Your Own Agent |
> | lab-07 | Lab 07 – Build a Client with an AI Coding Agent |
> | lab-08 | lab-08 |
>
> Which lab would you like to see the scores for?

---

## Task 2A — Deployed agent

### Nanobot Gateway Deployment

**Service status:**
```
SERVICE          STATUS
nanobot          Up 56 seconds
```

### Startup Log Excerpt

```
nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-04-01 17:50:02.982 | DEBUG    | nanobot.channels.registry:discover_all:64 - Skipping built-in channel 'matrix': Matrix dependencies not installed.
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | 2026-04-01 17:50:03.508 | INFO     | nanobot.cron.service:start:202 - Cron service started with 0 jobs
nanobot-1  | 2026-04-01 17:50:06,257 INFO [mcp.server.lowlevel.server] - Processing request of type ListToolsRequest
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_timeline' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_groups' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_top_learners' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_completion_rate' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.261 | DEBUG    | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_sync_pipeline' from server 'lms'
nanobot-1  | 2026-04-01 17:50:06.262 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-04-01 17:50:06.262 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
```

**Good signs:**
- ✅ Config loaded from `config.resolved.json`
- ✅ Gateway started on port 18790
- ✅ MCP server 'lms': connected, 9 tools registered
- ✅ Agent loop started

---

## Task 2B — Web client

### WebSocket Channel and Flutter Client Deployment

**Files modified:**
1. `pyproject.toml` - Added nanobot-websocket-channel workspace members
2. `nanobot/pyproject.toml` - Added mcp-webchat and nanobot-webchat dependencies
3. `nanobot/Dockerfile` - Updated to build with workspace dependencies
4. `nanobot/entrypoint.py` - Uncommented webchat channel and MCP server config
5. `docker-compose.yml` - Uncommented nanobot-websocket-channel volume, webchat env vars, client-web-flutter service, caddy dependencies
6. `caddy/Caddyfile` - Uncommented `/ws/chat` and `/flutter*` routes

**Services running:**
```
SERVICE          STATUS
nanobot          Up (webchat channel enabled)
caddy            Up
client-web-flutter Built (volume mounted)
```

**Nanobot logs showing webchat enabled:**
```
nanobot-1  | 2026-04-01 18:14:33.432 | INFO | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-04-01 18:14:33.857 | INFO | nanobot.channels.manager:_dispatch_outbound:119 - Outbound dispatcher started
nanobot-1  | 2026-04-01 18:14:33,858 INFO [nanobot_webchat.channel] - WebChat relay listening on 127.0.0.1:8766
nanobot-1  | 2026-04-01 18:14:33,862 INFO [nanobot_webchat.channel] - WebChat starting on 0.0.0.0:8765
nanobot-1  | 2026-04-01 18:14:33,866 INFO [websockets.server] - server listening on 0.0.0.0:8765
nanobot-1  | 2026-04-01 18:14:38.055 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_webchat_ui_message' from server 'webchat'
nanobot-1  | 2026-04-01 18:14:38.056 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
```

**Endpoints:**
- WebSocket: `ws://localhost:42002/ws/chat?access_key=NANOBOT_ACCESS_KEY`
- Flutter Web UI: `http://localhost:42002/flutter`

### Checkpoint Verification

**Test 1: "What can you do in this system?"**

Response:
> I'm nanobot 🐈, your personal AI assistant! Here's what I can do in this system:
>
> **📁 File & Workspace Management**
> - Read, write, and edit files
> - Browse directories and explore project structure
> - Execute shell commands (with safety limits)
>
> **🌐 Web & Information**
> - Search the web for information
> - Fetch and extract content from URLs
> - Send messages with file attachments
>
> **⏰ Scheduling & Automation**
> - Set up reminders and recurring tasks via cron
> - Manage periodic tasks through heartbeat system
>
> **🎓 LMS Integration** (Learning Management System)
> - Query lab listings, learner rosters, and group performance
> - Check pass rates, completion rates, and submission timelines
> - Find top learners and track analytics
>
> **🧠 Memory System**
> - Store long-term facts in MEMORY.md
> - Log events in HISTORY.md (grep-searchable)
>
> **🛠️ Skills Available**
> - **structured-ui**: Interactive choice menus for webchat
> - **lms**: Live course data queries
> - **memory**: Two-layer fact/event storage
> - **clawhub**: Search/install community skills
> - **skill-creator**: Build new agent skills
> - **cron**: Schedule reminders/tasks
>
> **🤝 Multi-Agent**
> - Spawn subagents for complex background tasks

**Test 2: "How is the backend doing? Is it healthy?"**

Response (REAL backend data):
> I'll check the LMS backend health for you.
>
> Yes, the LMS backend is healthy! ✅ It's currently tracking **56 items** with no errors reported.

**Test 3: "Show me the scores" (Structured UI Choice)**

Response showing structured choice UI:
> I'll check what labs are available first, then show you the scores.
>
> Which lab would you like to see scores for?
>
> **Structured Choice Payload:**
> ```json
> {
>   "type": "choice",
>   "content": "",
>   "options": [
>     {"label": "Lab 01 – Products, Architecture & Roles", "value": "lab-01"},
>     {"label": "Lab 02 — Run, Fix, and Deploy a Backend Service", "value": "lab-02"},
>     {"label": "Lab 03 — Backend API: Explore, Debug, Implement, Deploy", "value": "lab-03"},
>     {"label": "Lab 04 — Testing, Front-end, and AI Agents", "value": "lab-04"},
>     {"label": "Lab 05 — Data Pipeline and Analytics Dashboard", "value": "lab-05"},
>     {"label": "Lab 06 — Build Your Own Agent", "value": "lab-06"},
>     {"label": "Lab 07 — Build a Client with an AI Coding Agent", "value": "lab-07"},
>     {"label": "lab-08", "value": "lab-08"}
>   ]
> }
> ```
>
> I've sent you an interactive menu to choose which lab you'd like to see scores for. Please select one from the options!

**The structured-ui skill and LMS skill cooperate correctly:**
- LMS skill calls `lms_labs` to get available labs
- Provides lab titles as labels and lab IDs as values
- structured-ui skill renders the choice UI in the Flutter client

---

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
