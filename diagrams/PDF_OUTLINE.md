# AustenTel ACS System Documentation
## Professional Architecture Guide

---

### SECTION 1: EXECUTIVE SUMMARY

**System Overview**
The AustenTel ACS (Advanced Communication System) is an intelligent voice communication platform that combines traditional telephony with cutting-edge AI technology to deliver sophisticated voice interactions.

**Key Capabilities**
- Multi-agent orchestration for complex projects
- Real-time voice processing with AI enhancement
- Integrated telephony and WebRTC support
- Distributed architecture for scalability

---

### SECTION 2: SYSTEM ARCHITECTURE

**2.1 Three-Layer Architecture**

```
External Layer:
├── Customer Phones (PSTN)
├── Twilio (SIP Trunking)
└── LiveKit (WebRTC)

Orchestration Layer:
├── ACS-Manager (Central Control)
├── ACS-Voice (Platform Management)
└── ACS-Voice-Agent (AI Services)

Data Layer:
├── PostgreSQL (3 Databases)
├── Valkey/Redis (Cache)
└── Platform Services (MCP, API)
```

**2.2 Infrastructure Layout**

| Server | IP Address | Role | Services |
|--------|------------|------|----------|
| MCP | 10.152.0.70 | Control | GitHub, Documentation |
| App | 10.152.0.71 | Application | ACS-Manager, UI |
| DNS | 10.152.0.75 | Network | Domain Resolution |
| DB | 10.152.0.76 | Database | PostgreSQL |
| FS | 10.152.0.77 | Telephony | FreeSWITCH |

---

### SECTION 3: AGENT PROFILES

**ACS-Manager**
- Role: System Orchestrator
- Responsibilities: Project management, request routing, collaboration
- Database: acs_context_db

**ACS-Voice**
- Role: Voice Platform Manager
- Responsibilities: FreeSWITCH control, IVR design, call handling
- Database: acs_voice_hub_db

**ACS-Voice-Agent**
- Role: AI Voice Specialist
- Responsibilities: LiveKit integration, speech processing, AI models
- Database: acs_voice_agent_db

---

### SECTION 4: PROCESS FLOWS

**4.1 Inbound Call Processing**

1. **Call Initiation** → Customer dials number
2. **PSTN Routing** → Carrier network
3. **SIP Trunk** → Twilio receives
4. **FreeSWITCH** → Routes to ACS
5. **IVR Processing** → Menu navigation
6. **AI Activation** → LiveKit room
7. **Speech Recognition** → Whisper STT
8. **LLM Processing** → OpenAI GPT
9. **Voice Synthesis** → Cartesia TTS
10. **Audio Delivery** → Back to caller

**4.2 Multi-Agent Collaboration**

1. **Request Receipt** → User submits project
2. **Analysis** → ACS-Manager evaluates
3. **Task Breakdown** → Identifies requirements
4. **Agent Assignment** → Delegates to experts
5. **Parallel Execution** → Agents work concurrently
6. **Integration** → Results combined
7. **Delivery** → Unified solution presented

---

### SECTION 5: TECHNOLOGY STACK

**Core Technologies**
- Language: Python 3.11
- Framework: LiveKit Agents SDK
- Container: Docker
- Database: PostgreSQL

**AI Services**
- LLM: OpenAI GPT-4o
- STT: Whisper-1
- TTS: Cartesia

**Communication**
- Telephony: FreeSWITCH
- SIP: Twilio
- WebRTC: LiveKit

---

### SECTION 6: DEPLOYMENT

**Prerequisites**
- Ubuntu 22.04 LTS
- Docker & Docker Compose
- PostgreSQL 15+
- Python 3.11+

**Network Requirements**
- Static IP addresses
- Firewall rules configured
- DNS resolution active

**Service Ports**
- 3211: ACS UI
- 8021: FreeSWITCH ESL
- 8083: MCP Server
- 5432: PostgreSQL

---

### SECTION 7: OPERATIONS

**Monitoring**
- System metrics via Prometheus
- Call analytics dashboard
- Agent performance tracking

**Maintenance**
- Daily database backups
- Log rotation policies
- Security updates schedule

**Scaling**
- Horizontal agent scaling
- Database replication
- Load balancer ready

---

### APPENDIX A: API REFERENCE

**REST Endpoints**
- `/orchestrate` - Route requests
- `/projects` - Manage projects
- `/agents/status` - Agent health
- `/calls/active` - Live calls

**WebSocket Events**
- `agent.ready` - Agent online
- `call.started` - New call
- `task.completed` - Task done

---

### APPENDIX B: TROUBLESHOOTING

**Common Issues**
1. FreeSWITCH connection failed
2. Database connection timeout
3. LiveKit room creation error
4. API rate limits exceeded

---

*Document Version: 2.0*
*Last Updated: September 2025*
*© AustenTel Communications*
