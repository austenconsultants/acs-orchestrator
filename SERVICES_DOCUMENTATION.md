# ACS Services Documentation
## Working State - January 4, 2025

---

## Service Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   User Interface                         │
│            ACS UI (Node.js - Port 3211)                 │
│                  10.152.0.71                            │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Agent Services Layer                    │
├───────────────────┬────────────────┬────────────────────┤
│   ACS-Manager     │   ACS-Voice    │  ACS-Voice-Agent  │
│  (Orchestrator)   │  (Telephony)   │   (AI Services)   │
└───────────────────┴────────────────┴────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Services                         │
├──────────────────────────┬───────────────────────────────┤
│    PostgreSQL (.76)      │      FreeSWITCH (.77)        │
│   ┌─────────────────┐   │    ┌──────────────────┐     │
│   │ acs_context_db  │   │    │  SIP/ESL:8021    │     │
│   │ acs_voice_hub   │   │    │  RTP/Media       │     │
│   │ acs_voice_agent │   │    └──────────────────┘     │
│   └─────────────────┘   │                              │
└──────────────────────────┴───────────────────────────────┘
```

---

## 1. ACS UI Service
**Location:** 10.152.0.71:3211
**Technology:** Node.js/Express
**Purpose:** Web interface for ACS management

### Configuration:
```javascript
// config.json
{
  "port": 3211,
  "database": {
    "host": "10.152.0.76",
    "port": 5432,
    "user": "acs_chat_user",
    "password": "chatdb123",
    "databases": [
      "acs_context_db",
      "acs_voice_hub_db", 
      "acs_voice_agent_db"
    ]
  },
  "agents": {
    "manager": {
      "name": "ACS-Manager",
      "endpoint": "http://10.152.0.71:8001"
    },
    "voice": {
      "name": "ACS-Voice",
      "endpoint": "http://10.152.0.71:8002"
    },
    "voiceAgent": {
      "name": "ACS-Voice-Agent",
      "endpoint": "http://10.152.0.71:8003"
    }
  },
  "freeswitch": {
    "host": "10.152.0.77",
    "eslPort": 8021,
    "eslPassword": "ClueCon"
  }
}
```

### What it touches:
- **Reads from:** All three PostgreSQL databases
- **Writes to:** Project configurations, IVR templates
- **Connects to:** Agent endpoints for status/control
- **Manages:** FreeSWITCH via ESL connection

---

## 2. ACS-Manager Service
**Purpose:** Central orchestration and routing
**Database:** acs_context_db

### Service Flow:
```python
# Pseudo-code for request handling
def handle_request(user_input):
    # 1. Check collaboration rules
    rules = db.query("SELECT * FROM agent_collaboration_rules WHERE request_pattern MATCHES")
    
    # 2. Create project if complex
    if is_complex_request(user_input):
        project = create_project(user_input)
        
    # 3. Assign to agents
    agents = determine_agents(rules, user_input)
    
    # 4. Create tasks
    for agent in agents:
        create_task(project.id, agent, task_description)
    
    # 5. Monitor execution
    monitor_task_completion(project.id)
    
    return aggregate_results(project.id)
```

### Database interactions:
- **Reads:** agent_personalities, agent_collaboration_rules
- **Writes:** project_context, project_tasks, conversation_memory
- **Triggers:** Task assignments to other agents

---

## 3. ACS-Voice Service  
**Purpose:** FreeSWITCH management and IVR control
**Database:** acs_voice_hub_db
**External:** FreeSWITCH (10.152.0.77)

### Service Components:
```python
# FreeSWITCH ESL Connection
class FreeSWITCHManager:
    def __init__(self):
        self.host = "10.152.0.77"
        self.port = 8021
        self.password = "ClueCon"
    
    def generate_dialplan(self, ivr_template):
        # Convert IVR template to FreeSWITCH XML
        xml = build_xml_from_template(ivr_template)
        return self.esl.send_command(f"reloadxml dialplan")
    
    def handle_sip_trunk(self, config):
        # Configure SIP gateway
        gateway_xml = build_gateway_xml(config)
        return self.esl.send_command(f"sofia profile external rescan")
```

### What it manages:
- **IVR Flows:** Creates/updates via ivr_templates table
- **SIP Trunks:** Configures via sip_trunk_configs
- **Call Routing:** Dynamic dialplan generation
- **CDRs:** Stores in call_detail_records

### FreeSWITCH Integration:
- **ESL Commands:** Real-time control via port 8021
- **XML Generation:** Dynamic configuration files
- **Event Monitoring:** Call state changes
- **Media Handling:** RTP stream management

---

## 4. ACS-Voice-Agent Service
**Purpose:** AI voice processing (LiveKit, Whisper, OpenAI, Cartesia)
**Database:** acs_voice_agent_db

### AI Pipeline:
```python
class VoiceAgentPipeline:
    def __init__(self):
        self.livekit_url = "wss://livekit.cloud"
        self.openai_key = get_secure_key("OPENAI_API_KEY")
        self.cartesia_key = get_secure_key("CARTESIA_API_KEY")
    
    async def process_call(self, room_id):
        # 1. Join LiveKit room
        room = await livekit.connect(room_id)
        
        # 2. Process audio stream
        async for audio in room.audio_stream():
            # 3. Speech to text
            text = await whisper.transcribe(audio)
            
            # 4. LLM processing
            response = await openai.complete(text)
            
            # 5. Text to speech
            audio_response = await cartesia.synthesize(response)
            
            # 6. Stream back
            await room.send_audio(audio_response)
```

### Database operations:
- **Reads:** ai_model_configs, voice_profiles
- **Writes:** livekit_sessions, conversation_context, transcription_logs
- **Real-time:** Updates during active calls

### External APIs:
- **LiveKit:** WebRTC room management
- **OpenAI:** GPT-4o for conversation, Whisper for STT
- **Cartesia:** TTS with custom voices
- **Twilio:** SIP signaling (indirect via FreeSWITCH)

---

## 5. Infrastructure Services

### PostgreSQL (10.152.0.76:5432)
```yaml
Databases:
  acs_context_db:
    tables: 5
    primary_user: ACS-Manager
    
  acs_voice_hub_db:
    tables: 5
    primary_user: ACS-Voice
    
  acs_voice_agent_db:
    tables: 5
    primary_user: ACS-Voice-Agent

Connection: postgresql://acs_chat_user:chatdb123@10.152.0.76:5432/{db}
```

### FreeSWITCH (10.152.0.77:8021)
```yaml
Services:
  ESL: Port 8021 (Event Socket Layer)
  SIP: Port 5060/5080
  RTP: Ports 16384-32768
  
Configuration:
  Dialplans: /etc/freeswitch/dialplan/
  Gateways: /etc/freeswitch/sip_profiles/external/
  IVR: /etc/freeswitch/ivr_menus/
```

### MCP Server (10.152.0.70:8083)
```yaml
Purpose: Agent communication protocol
Features:
  - Inter-agent messaging
  - State synchronization
  - Event broadcasting
```

---

## Service Dependencies

```mermaid
graph TD
    UI[ACS UI :3211] --> MGR[ACS-Manager]
    UI --> VOICE[ACS-Voice]
    UI --> AGENT[ACS-Voice-Agent]
    
    MGR --> DB1[(acs_context_db)]
    VOICE --> DB2[(acs_voice_hub_db)]
    AGENT --> DB3[(acs_voice_agent_db)]
    
    VOICE --> FS[FreeSWITCH :8021]
    FS --> TWILIO[Twilio SIP]
    
    AGENT --> LK[LiveKit Cloud]
    AGENT --> OAI[OpenAI API]
    AGENT --> CART[Cartesia API]
    
    MGR -.-> MCP[MCP :8083]
    VOICE -.-> MCP
    AGENT -.-> MCP
```

---

## Health Checks

### Service Status Commands:
```bash
# Check UI
curl http://10.152.0.71:3211/health

# Check PostgreSQL
PGPASSWORD=chatdb123 psql -h 10.152.0.76 -U acs_chat_user -d acs_context_db -c "SELECT 1"

# Check FreeSWITCH
fs_cli -H 10.152.0.77 -P 8021 -p ClueCon -x "status"

# Check MCP
curl http://10.152.0.70:8083/status
```

---

## Environment Variables

### Required for all services:
```bash
# Database
DB_HOST=10.152.0.76
DB_PORT=5432
DB_USER=acs_chat_user
DB_PASSWORD=chatdb123

# FreeSWITCH
FS_HOST=10.152.0.77
FS_ESL_PORT=8021
FS_ESL_PASSWORD=ClueCon

# MCP
MCP_HOST=10.152.0.70
MCP_PORT=8083

# AI Services (stored securely)
OPENAI_API_KEY=<secure_storage_ref>
CARTESIA_API_KEY=<secure_storage_ref>
LIVEKIT_URL=wss://livekit.cloud
LIVEKIT_API_KEY=<secure_storage_ref>
```

---

*Working State Captured: January 4, 2025*
