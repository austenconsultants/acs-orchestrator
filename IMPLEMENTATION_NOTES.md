# Implementation Notes from Architecture Session

## Key Decisions

1. **Naming Convention**: Clear, user-friendly names
   - NOT: orchestrator, context, voice-hub
   - YES: ACS-Manager, ACS-Voice, ACS-Voice-Agent

2. **Personality Model**: IT Department approach
   - Specialized experts with soft boundaries
   - Can discuss conceptually, not just execute commands
   - Know when to escalate or collaborate

3. **Database Structure**: 
   - Each agent has own knowledge domain
   - Shared context for collaboration
   - No duplication of AUSTENTEL-ACS platform code

4. **Integration Points**:
   - ACS-Voice manages platform (FreeSWITCH + UI)
   - ACS-Voice-Agent provides AI capabilities
   - They work together for AI-enabled telephony

## UI Design Requirements

Tabs in chat interface:
- [ACS-Manager] - General help
- [ACS-Voice] - Phone system  
- [ACS-Voice-Agent] - AI voice

Show collaboration when agents work together.
