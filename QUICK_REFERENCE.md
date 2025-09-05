# ACS Agent Quick Reference

## Agent Names & Roles
- **ACS-Manager**: General help, routes tasks, manages projects
- **ACS-Voice**: FreeSWITCH + UI (complete voice platform)
- **ACS-Voice-Agent**: AI tech (LiveKit, Whisper, OpenAI, Cartesia)

## How They Work Together
```
ACS-Manager coordinates →
  ACS-Voice handles telephony →
    ACS-Voice-Agent provides AI →
      Both integrate for complete solution
```

## Databases
- `acs_context_db`: Shared memory, personalities, collaboration
- `acs_voice_hub_db`: FreeSWITCH knowledge
- `acs_voice_agent_db`: AI configurations

## Key Commands
```bash
# View agents
psql -d acs_context_db -c "SELECT * FROM agent_personalities;"

# Check collaboration
psql -d acs_context_db -c "SELECT * FROM agent_collaboration_rules;"

# See capabilities  
psql -d acs_context_db -c "SELECT * FROM agent_capabilities;"
```

## Integration Points
- FreeSWITCH: 10.152.0.77:8021
- Voice UI: 10.152.0.71:3211
- Chat Hub: 10.152.0.71:3210
- Database: 10.152.0.76
- MCP: 10.152.0.70:8083
