# ACS-Voice-Agent Architecture
## AI Voice Technology Specialist

```
┌─────────────────────────────────────────────────────────────┐
│                    ACS-Voice-Agent                          │
│                  AI Voice Technology                         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   LiveKit    │   │   Whisper    │   │    OpenAI    │
│   WebRTC     │   │     STT      │   │     LLM      │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                ┌──────────────────┐
                │    Cartesia      │
                │      TTS         │
                └──────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Integration Points                         │
│                                                             │
│  Provides to ACS-Voice:                                    │
│  • AI model configurations                                 │
│  • Voice synthesis settings                                │
│  • Transcription parameters                                │
│  • Real-time processing pipelines                          │
└─────────────────────────────────────────────────────────────┘
```

## Processing Pipeline

### Real-time Voice Flow
```
1. Audio Input → LiveKit Room
2. Stream → Whisper STT
3. Text → OpenAI Processing
4. Response → Cartesia TTS
5. Audio Output → LiveKit Stream
```

### Database Schema
- `ai_model_configs` - Model settings
- `voice_profiles` - Synthesis profiles
- `livekit_sessions` - Active sessions
- `transcription_logs` - STT records
