# ACS Agent Architecture - IT Department Model

## Agent Team Structure

### 👔 ACS-Manager
**Role**: System Manager & Coordinator  
**Purpose**: General assistant that understands the entire platform, routes tasks, manages projects

### 📞 ACS-Voice  
**Role**: Voice Platform Manager  
**Purpose**: Manages FreeSWITCH telephony and ACS UI for IVR design  
**Encompasses**: Voice Hub functionality (FreeSWITCH) + UI controls

### 🤖 ACS-Voice-Agent
**Role**: AI Voice Specialist  
**Purpose**: Handles LiveKit, Whisper, OpenAI, Cartesia  
**Integration**: Works with ACS-Voice to implement AI into the platform

## Collaboration Model

```
User Request → ACS-Manager (routes) → Specialists collaborate → Solution
```

### Example: "Build an AI Receptionist"
1. ACS-Manager creates project
2. ACS-Voice sets up phone infrastructure
3. ACS-Voice-Agent configures AI
4. Both integrate for complete solution

## Database Architecture

- **acs_context_db**: Shared memory and context
- **acs_voice_hub_db**: Voice platform knowledge  
- **acs_voice_agent_db**: AI configurations
- **acs_chat_hub**: Integration tables

## Not Rigid Bots - Flexible Experts

Agents can:
- Discuss concepts broadly
- Brainstorm creative solutions
- Know when to collaborate
- Learn from interactions
