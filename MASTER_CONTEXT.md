# ACS Master Context - Load This First

## System Architecture
```yaml
infrastructure:
  chat_agent:
    host: 10.152.0.71
    port: 3210
    type: orchestrator
    tech: [React, Next.js, TypeScript]
    
  voice_hub:
    host: 10.152.0.71
    port: 3211
    backend: 10.152.0.77 (FreeSWITCH)
    tech: [React, Node.js, FreeSWITCH]
    databases: [PostgreSQL, Valkey]
    
  voice_agent:
    host: 10.152.0.71
    port: 3212
    tech: [LiveKit, OpenAI, Cartesia, Whisper]
    databases: [PostgreSQL, Valkey]
    
  context_service:
    host: 10.152.0.70
    port: 8090
    tech: [Node.js, Express, pgvector]
    databases: [PostgreSQL, Valkey]
    
  mcp_backbone:
    host: 10.152.0.70
    port: 8083
    type: integration_layer
    
  database:
    host: 10.152.0.76
    postgres_port: 5432
    valkey_port: 6379
```

## Quick Commands
```bash
# PM2 Management
pm2 list
pm2 restart acs-chat-hub
pm2 restart acs-voicehub-pro
pm2 logs --lines 100

# Context Service
curl http://10.152.0.70:8090/api/context/system
curl http://10.152.0.70:8090/api/context/agent/voice-hub

# Test Endpoints
curl http://10.152.0.71/         # Chat Agent
curl http://10.152.0.71:3211/    # Voice Hub
curl http://10.152.0.71:3212/    # Voice Agent

# Database
psql -h 10.152.0.76 -U acs_admin -d acs_chat_db
```

## Active Projects
- [ ] Context management system implementation
- [ ] pgvector semantic search
- [ ] Agent memory persistence
- [ ] Cross-agent communication via MCP
