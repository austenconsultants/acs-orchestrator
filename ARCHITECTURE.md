# ACS Complete Architecture

## GitHub Repository Structure ✅

```
/opt/github-agents/                     GitHub Repositories
├── acs-orchestrator/          ────►    YOUR-ORG/acs-orchestrator
│   ├── README.md                       (Master documentation)
│   ├── MASTER_CONTEXT.md              
│   └── setup-github.sh                
│
├── acs-chat-hub/             ────►    YOUR-ORG/acs-chat-hub
│   └── [React UI code]                 (Main portal - port 3210)
│
├── agent-acs-voice-hub/      ────►    YOUR-ORG/agent-acs-voice-hub
│   ├── README.md                       (FreeSWITCH manager - port 3211)
│   └── context.yaml
│
├── agent-acs-voice-agent/    ────►    YOUR-ORG/agent-acs-voice-agent
│   ├── README.md                       (LiveKit AI voice - port 3212)
│   └── context.yaml
│
├── agent-acs-context/        ────►    YOUR-ORG/agent-acs-context
│   ├── README.md                       (Memory service - port 8090)
│   ├── package.json
│   └── src/server.js
│
├── agent-acs-agent/          ────►    YOUR-ORG/agent-acs-agent
│   └── [Existing code]                 (General assistant)
│
├── agent-acs-voice/          ────►    YOUR-ORG/agent-acs-voice
│   └── [Existing code]                 (Voice expert)
│
└── agent-acs-voice-assistant/ ────►   YOUR-ORG/agent-acs-voice-assistant
    └── [Existing code]                 (IVR specialist)
```

## Context Flow Design

```
1. User opens ACS Chat Agent (3210)
         ↓
2. UI loads agent tabs from Context Service (8090)
         ↓
3. Context Service queries PostgreSQL for:
   - System context (static)
   - Project context (current work)
   - Session context (today's state)
   - Conversation memory (history)
         ↓
4. User selects agent tab (Voice Hub, Voice Agent, etc.)
         ↓
5. Context auto-injected into conversation
         ↓
6. Work continues exactly where left off
```

## Database Design (PostgreSQL on .76)

### Tables Created:
- `system_context` - Static infrastructure config
- `project_context` - Active projects
- `agent_sessions` - Session persistence
- `conversation_memory` - Chat history with embeddings
- `agent_states` - Current agent status

### Functions:
- `get_agent_context(agent_name)` - Returns complete context

## Next Implementation Steps

### Phase 1: UI Development (v0)
- [ ] Create tabbed interface in acs-chat-hub
- [ ] Add agent selector sidebar
- [ ] Implement context loading UI
- [ ] Add save/load session buttons

### Phase 2: Database Setup
- [ ] Create database on .76
- [ ] Run schema creation scripts
- [ ] Install pgvector extension
- [ ] Initialize system context

### Phase 3: Context Service Deployment
- [ ] Deploy context service on .70:8090
- [ ] Connect to PostgreSQL and Valkey
- [ ] Test API endpoints
- [ ] Integrate with MCP

### Phase 4: Integration
- [ ] Wire UI to Context Service
- [ ] Test context persistence
- [ ] Implement semantic search
- [ ] Validate cross-agent memory

## Benefits Achieved

1. **No More Lost Context** - Everything persisted in database
2. **Instant Continuity** - Pick up exactly where you left off
3. **Semantic Memory** - AI finds relevant past work
4. **GitHub Backup** - All architecture documented and versioned
5. **Agent Isolation** - Each agent has its own context namespace
6. **No Browser Storage** - Professional database-driven solution

## Quick Test Commands

```bash
# Check all repos
ls -la /opt/github-agents/

# Test context service (once deployed)
curl http://10.152.0.70:8090/api/context/system

# Check PM2 apps
pm2 list

# View master context
cat /opt/github-agents/acs-orchestrator/MASTER_CONTEXT.md
```
