# ACS Database Schemas Documentation
## Working State - January 4, 2025

---

## Overview
The ACS system uses PostgreSQL (10.152.0.76:5432) with three specialized databases:
- **acs_context_db** - ACS-Manager orchestration data
- **acs_voice_hub_db** - ACS-Voice telephony platform data
- **acs_voice_agent_db** - ACS-Voice-Agent AI service data

---

## 1. acs_context_db (ACS-Manager)
**Purpose:** Central orchestration, project management, agent coordination

### Tables:

#### agent_personalities
```sql
CREATE TABLE agent_personalities (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) UNIQUE NOT NULL,
    role_title VARCHAR(100),
    personality_traits TEXT,
    expertise_areas TEXT[],
    communication_style TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** Defines each agent's personality and capabilities
**Touches:** ACS-Manager reads this to understand agent capabilities

#### agent_collaboration_rules
```sql
CREATE TABLE agent_collaboration_rules (
    id SERIAL PRIMARY KEY,
    request_pattern TEXT NOT NULL,
    primary_agent VARCHAR(50),
    supporting_agents TEXT[],
    priority INTEGER DEFAULT 5
);
```
**Usage:** Pattern matching for request routing
**Touches:** ACS-Manager uses for deciding which agents to involve

#### project_context
```sql
CREATE TABLE project_context (
    id SERIAL PRIMARY KEY,
    project_id UUID UNIQUE DEFAULT gen_random_uuid(),
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    assigned_agents TEXT[],
    created_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** Tracks active projects across agents
**Touches:** All agents can read/update their assigned projects

#### project_tasks
```sql
CREATE TABLE project_tasks (
    id SERIAL PRIMARY KEY,
    project_id UUID REFERENCES project_context(project_id),
    task_id UUID DEFAULT gen_random_uuid(),
    agent_name VARCHAR(50),
    task_description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    dependencies TEXT[],
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```
**Usage:** Individual task tracking within projects
**Touches:** Agents update their task status and results

#### conversation_memory
```sql
CREATE TABLE conversation_memory (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    agent_name VARCHAR(50),
    user_message TEXT,
    agent_response TEXT,
    context JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** Stores conversation history for context
**Touches:** All agents store their interactions

---

## 2. acs_voice_hub_db (ACS-Voice)
**Purpose:** FreeSWITCH configurations, IVR flows, telephony management

### Tables:

#### freeswitch_knowledge
```sql
CREATE TABLE freeswitch_knowledge (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    template_name VARCHAR(255) UNIQUE NOT NULL,
    xml_config TEXT,
    description TEXT,
    variables JSONB,
    examples TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** FreeSWITCH XML configuration templates
**Touches:** ACS-Voice generates configs for FreeSWITCH (10.152.0.77)

#### ivr_templates
```sql
CREATE TABLE ivr_templates (
    id SERIAL PRIMARY KEY,
    flow_id UUID DEFAULT gen_random_uuid(),
    flow_name VARCHAR(255) NOT NULL,
    menu_structure JSONB,
    prompts JSONB,
    actions JSONB,
    dtmf_mappings JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** IVR menu definitions and call flows
**Touches:** FreeSWITCH executes these flows, ACS UI displays/edits

#### sip_trunk_configs
```sql
CREATE TABLE sip_trunk_configs (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(100),
    trunk_name VARCHAR(100) UNIQUE,
    credentials JSONB,  -- Encrypted
    settings JSONB,
    inbound_did VARCHAR(20),
    outbound_cid VARCHAR(20),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** SIP provider configurations (Twilio, etc.)
**Touches:** FreeSWITCH uses for external connectivity

#### call_detail_records
```sql
CREATE TABLE call_detail_records (
    id SERIAL PRIMARY KEY,
    call_uuid UUID UNIQUE,
    caller_id VARCHAR(20),
    called_number VARCHAR(20),
    start_time TIMESTAMP,
    answer_time TIMESTAMP,
    end_time TIMESTAMP,
    duration INTEGER,
    disposition VARCHAR(50),
    recording_url TEXT,
    metadata JSONB
);
```
**Usage:** CDR storage for analytics and billing
**Touches:** FreeSWITCH writes, UI reads for reports

#### agent_expertise
```sql
CREATE TABLE agent_expertise (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50),
    skill_category VARCHAR(100),
    skill_name VARCHAR(100),
    proficiency_level INTEGER CHECK (proficiency_level BETWEEN 1 AND 10),
    examples TEXT[],
    UNIQUE(agent_name, skill_name)
);
```
**Usage:** Skills matrix for agent capabilities
**Touches:** ACS-Manager queries for task assignment

---

## 3. acs_voice_agent_db (ACS-Voice-Agent)
**Purpose:** AI configurations, voice profiles, LiveKit sessions

### Tables:

#### ai_model_configs
```sql
CREATE TABLE ai_model_configs (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) UNIQUE NOT NULL,
    provider VARCHAR(50),  -- OpenAI, Cartesia, etc.
    model_type VARCHAR(50),  -- LLM, STT, TTS
    settings JSONB,
    api_key_ref VARCHAR(100),  -- Reference to secure storage
    rate_limits JSONB,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** AI service configurations
**Touches:** Voice-Agent uses for AI processing

#### voice_profiles
```sql
CREATE TABLE voice_profiles (
    id SERIAL PRIMARY KEY,
    profile_id UUID DEFAULT gen_random_uuid(),
    profile_name VARCHAR(100) UNIQUE,
    voice_name VARCHAR(100),  -- Cartesia voice ID
    tts_provider VARCHAR(50),
    tts_settings JSONB,
    personality_prompt TEXT,
    use_cases TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** Voice synthesis profiles
**Touches:** Used when generating speech responses

#### livekit_sessions
```sql
CREATE TABLE livekit_sessions (
    id SERIAL PRIMARY KEY,
    room_id VARCHAR(255) UNIQUE,
    room_name VARCHAR(255),
    participant_id VARCHAR(255),
    participant_name VARCHAR(255),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    metadata JSONB,
    recording_id VARCHAR(255),
    transcription TEXT
);
```
**Usage:** LiveKit WebRTC session tracking
**Touches:** LiveKit cloud integration, call recordings

#### conversation_context
```sql
CREATE TABLE conversation_context (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255),
    turn_number INTEGER,
    speaker VARCHAR(50),
    text_content TEXT,
    audio_metadata JSONB,
    ai_model_used VARCHAR(100),
    processing_time_ms INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** Real-time conversation tracking
**Touches:** Used for context in ongoing calls

#### transcription_logs
```sql
CREATE TABLE transcription_logs (
    id SERIAL PRIMARY KEY,
    audio_id VARCHAR(255),
    transcription_text TEXT,
    confidence_score FLOAT,
    language VARCHAR(10),
    model_used VARCHAR(50),
    processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Usage:** STT transcription history
**Touches:** Whisper API results stored here

---

## Database Connection Info

### Connection String Format:
```
postgresql://acs_chat_user:chatdb123@10.152.0.76:5432/{database_name}
```

### Service Connections:
- **ACS-Manager**: Connects to acs_context_db (orchestration)
- **ACS-Voice**: Connects to acs_voice_hub_db (telephony)
- **ACS-Voice-Agent**: Connects to acs_voice_agent_db (AI services)
- **ACS UI (3211)**: Connects to all three for management interface

### Cross-Database References:
- Agent names are consistent across all databases
- Project IDs can be referenced across databases
- Session IDs link conversations across services

---

## Data Flow Examples

### 1. Incoming Call Flow:
```
1. Call arrives → FreeSWITCH → CDR created in voice_hub_db
2. IVR activated → ivr_templates queried
3. AI needed → livekit_sessions created in voice_agent_db
4. Conversation → transcription_logs + conversation_context
5. Project created → project_context in context_db
```

### 2. Agent Collaboration:
```
1. Request → agent_collaboration_rules checked
2. Project → project_context created
3. Tasks → project_tasks assigned to agents
4. Execution → Each agent updates their database
5. Results → Stored back in project_tasks
```

---

*Working State Captured: January 4, 2025*
