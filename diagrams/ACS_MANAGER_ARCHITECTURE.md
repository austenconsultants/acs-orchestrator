# ACS-Manager Architecture
## System Orchestrator & Project Manager

```
┌─────────────────────────────────────────────────────────────┐
│                      ACS-Manager                            │
│                  Central Control System                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Request    │   │   Project    │   │ Brainstorm   │
│   Router     │   │   Manager    │   │ Facilitator  │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Pattern    │   │    Task      │   │   Idea       │
│   Matching   │   │  Breakdown   │   │ Synthesis    │
└──────────────┘   └──────────────┘   └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  ACS-Voice   │   │ACS-Voice-    │   │   Memory     │
│   (Assign)   │   │Agent(Assign) │   │   (Store)    │
└──────────────┘   └──────────────┘   └──────────────┘
```

## Core Functions

### Request Routing Logic
```python
def route_request(user_input):
    if is_telephony_request(user_input):
        return delegate_to("ACS-Voice")
    elif is_ai_voice_request(user_input):
        return delegate_to("ACS-Voice-Agent")
    elif is_complex_project(user_input):
        return coordinate_agents(["ACS-Voice", "ACS-Voice-Agent"])
    else:
        return handle_directly()
```

### Database Tables Used
- `project_context` - Active projects
- `agent_collaboration_rules` - Routing rules
- `project_tasks` - Task assignments
