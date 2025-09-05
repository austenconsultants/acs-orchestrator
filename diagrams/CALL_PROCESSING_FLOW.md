# ACS Call Processing Flow
## End-to-End Voice Communication Pipeline

```mermaid
sequenceDiagram
    participant C as Customer
    participant T as Twilio SIP
    participant F as FreeSWITCH
    participant V as ACS-Voice
    participant VA as ACS-Voice-Agent
    participant LK as LiveKit
    participant W as Whisper STT
    participant O as OpenAI
    participant CA as Cartesia TTS
    participant DB as PostgreSQL

    C->>T: 1. Dial Phone Number
    T->>F: 2. SIP Trunk Connection
    F->>V: 3. Call Route Decision
    V->>VA: 4. Request AI Processing
    VA->>LK: 5. Create WebRTC Room
    LK->>W: 6. Stream Audio
    W->>O: 7. Transcribed Text
    O->>O: 8. Process & Generate Response
    O->>CA: 9. Text for Synthesis
    CA->>LK: 10. Audio Stream
    LK->>F: 11. Return Audio
    F->>T: 12. SIP Audio
    T->>C: 13. Voice Response
    
    Note over DB: All interactions logged
```

## Processing Steps Detail

### Phase 1: Call Initiation (Steps 1-3)
- **Duration**: ~500ms
- **Components**: Customer Phone → Twilio → FreeSWITCH
- **Protocol**: SIP/RTP

### Phase 2: AI Setup (Steps 4-5)
- **Duration**: ~200ms
- **Components**: ACS-Voice → ACS-Voice-Agent → LiveKit
- **Protocol**: WebSocket

### Phase 3: Speech Processing (Steps 6-8)
- **Duration**: ~1-2s
- **Components**: Whisper → OpenAI
- **Protocol**: HTTPS/REST

### Phase 4: Response Generation (Steps 9-13)
- **Duration**: ~500ms
- **Components**: Cartesia → LiveKit → FreeSWITCH → Customer
- **Protocol**: WebRTC → SIP
