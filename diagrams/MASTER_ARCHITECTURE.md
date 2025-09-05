# AustenTel ACS System Architecture
## Unified Voice & AI Platform
Documentation Version: 1.0 | September 2025

---

## Master System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AUSTENTEL ACS PLATFORM                              │
│                     Intelligent Voice Communication System                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              EXTERNAL LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                │
│  │   Customer   │    │    Twilio    │    │   LiveKit    │                │
│  │    Phone     │───►│  SIP Trunk   │───►│    Cloud     │                │
│  └──────────────┘    └──────────────┘    └──────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENT ORCHESTRATION LAYER                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     ┌────────────────────────────────────────────────────────┐            │
│     │                    ACS-Manager                          │            │
│     │              (Orchestration & Routing)                  │            │
│     │                                                         │            │
│     │  • Project Management    • Task Distribution           │            │
│     │  • Agent Coordination    • Brainstorming               │            │
│     └────────────┬─────────────────────┬─────────────────────┘            │
│                  │                     │                                   │
│         ┌────────▼────────┐   ┌────────▼────────┐                        │
│         │   ACS-Voice     │◄──┤ ACS-Voice-Agent │                        │
│         │                 │   │                 │                        │
│         │ • FreeSWITCH    │   │ • LiveKit       │                        │
│         │ • SIP Config    │   │ • Whisper       │                        │
│         │ • IVR Design    │   │ • OpenAI        │                        │
│         │ • ACS UI        │   │ • Cartesia      │                        │
│         └─────────────────┘   └─────────────────┘                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │ PostgreSQL  │  │ acs_context  │  │acs_voice_hub │  │acs_voice_    │ │
│   │   (10.76)   │  │     _db      │  │     _db      │  │  agent_db    │ │
│   └─────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                                             │
│   ┌─────────────┐  ┌──────────────────────────────────────────────────┐  │
│   │   Valkey/   │  │              Platform Services                    │  │
│   │   Redis     │  │   MCP (10.70:8083) | API Gateway | WebSocket    │  │
│   └─────────────┘  └──────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Color Scheme (AustenTel Brand)
- Primary: #003366 (Deep Blue)
- Secondary: #FF6B35 (Orange Accent)
- Success: #28A745 (Green)
- Info: #17A2B8 (Cyan)
- Background: #F8F9FA (Light Gray)

---

## Component Breakdown

### ACS-Manager (Orchestration Layer)
**Purpose**: Central orchestrator and project manager
**Location**: 10.152.0.71
**Database**: acs_context_db

**Key Functions**:
- Route requests to appropriate agents
- Manage multi-agent projects
- Facilitate brainstorming sessions
- Maintain system context

### ACS-Voice (Telephony Platform)
**Purpose**: Complete voice platform management
**Components**:
- FreeSWITCH Server (10.152.0.77)
- ACS Voice UI (10.152.0.71:3211)
- SIP Trunk Management
- IVR Flow Designer

**Database**: acs_voice_hub_db

### ACS-Voice-Agent (AI Services)
**Purpose**: AI voice technology provider
**Technologies**:
- LiveKit (Real-time WebRTC)
- Whisper (Speech-to-Text)
- OpenAI (LLM Processing)
- Cartesia (Text-to-Speech)

**Database**: acs_voice_agent_db

---

## Data Flow Sequences

### 1. Inbound Call Processing
```
Customer → Twilio SIP → FreeSWITCH → ACS-Voice → ACS-Voice-Agent → AI Processing → Response
```

### 2. Project Coordination
```
User Request → ACS-Manager → Task Analysis → Agent Assignment → Parallel Execution → Integration
```

### 3. AI Enhancement Flow
```
ACS-Voice (IVR) → ACS-Voice-Agent (AI Config) → Model Selection → Implementation → Platform Update
```
