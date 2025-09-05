# ACS-Voice Architecture
## Voice Platform & Telephony Manager

```
┌─────────────────────────────────────────────────────────────┐
│                        ACS-Voice                            │
│                 Complete Voice Platform                      │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  FreeSWITCH  │ │   ACS UI     │ │     IVR      │
    │   Backend    │ │   Frontend   │ │   Designer   │
    └──────────────┘ └──────────────┘ └──────────────┘
            │               │               │
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │     SIP      │ │   Call Flow  │ │    Menu      │
    │   Trunks     │ │   Manager    │ │   Builder    │
    └──────────────┘ └──────────────┘ └──────────────┘
                            │
                            ▼
    ┌─────────────────────────────────────────────────┐
    │              Integration Layer                   │
    │                                                 │
    │  • Receives AI configs from ACS-Voice-Agent    │
    │  • Implements AI features into IVR             │
    │  • Updates call routing with intelligence       │
    └─────────────────────────────────────────────────┘
```

## Component Details

### FreeSWITCH Integration
- **Server**: 10.152.0.77
- **Protocol**: ESL (Event Socket Library)
- **Port**: 8021

### Database Schema
- `freeswitch_knowledge` - Configuration templates
- `sip_trunk_configs` - Provider settings
- `ivr_templates` - Flow patterns
- `cdr_cache` - Call records
