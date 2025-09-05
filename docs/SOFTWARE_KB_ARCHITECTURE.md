# Software Knowledge Base Architecture

## Overview
Offline software documentation system allowing agents to access docs without internet.

---

## Architecture Design

```
┌─────────────────────────────────────────────────────────┐
│                   User Query                             │
│            "How do I configure FreeSWITCH IVR?"         │
└────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 ACS-Manager                              │
│            (Knowledge Orchestrator)                      │
├─────────────────────────────────────────────────────────┤
│  1. Parse query → Identify software (FreeSWITCH)        │
│  2. Check expertise → ACS-Voice is expert               │
│  3. Search software_docs → Find relevant docs           │
│  4. Route to expert OR answer directly                  │
└─────────────────┬───────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ACS-Voice │ │Voice-Agent│ │ Direct Answer│
│(FS Expert)│ │(AI Expert)│ │ (Simple Q)   │
└──────────┘ └──────────┘ └──────────────┘
```

---

## Storage Structure

### Database Tables
```sql
software_catalog        -- What software we track
software_docs          -- Version-specific docs
software_dependencies  -- Dependency mapping
agent_software_expertise -- Who knows what
```

### File System
```
/opt/acs/knowledge/software_docs/
├── freeswitch/
│   ├── 1.10.11/
│   │   ├── api/
│   │   ├── config/
│   │   └── tutorials/
│   └── 1.10.10/
├── nodejs/
│   ├── 20.11.0/
│   └── 18.19.0/
├── react/
│   └── 18.2.0/
└── postgresql/
    └── 15.5/
```

---

## Query Flow

### 1. Simple Documentation Query
```python
# User: "What are React hooks?"
query_result = ACS_Manager.search_knowledge(
    query="React hooks",
    software=["React"],
    doc_type="api"
)
# Returns directly from knowledge base
```

### 2. Complex Implementation Query
```python
# User: "Build FreeSWITCH IVR with AI integration"
# ACS-Manager logic:
if requires_multiple_expertise(query):
    experts = identify_experts(["FreeSWITCH", "AI"])
    # Routes to both ACS-Voice and ACS-Voice-Agent
    coordinate_response(experts)
```

### 3. Version-Specific Query
```python
# User: "Node.js 20 vs 18 differences?"
docs = search_software_docs(
    software="Node.js",
    versions=["20.11.0", "18.19.0"],
    doc_type="changelog"
)
```

---

## Update Strategy

### Automated Updates (Monthly)
```bash
#!/bin/bash
# Cron job: 0 2 1 * * /opt/acs/scripts/update_docs.sh

# 1. Check for new versions
python3 check_software_versions.py

# 2. Download documentation
python3 download_official_docs.py

# 3. Process and import
python3 import_software_docs.py

# 4. Update embeddings for search
python3 update_doc_embeddings.py

# 5. Notify agents of updates
python3 notify_doc_updates.py
```

### Manual Import
```bash
# Import specific documentation
python3 import_software_docs.py --software=FreeSWITCH --version=1.10.12

# Bulk import from JSON
python3 import_software_docs.py --file=docs_export.json
```

---

## Search Implementation

### Full-Text Search
```sql
-- PostgreSQL full-text search
SELECT * FROM search_software_docs(
    'configure IVR menu',
    ARRAY['FreeSWITCH'],
    ARRAY['1.10.11']
);
```

### Semantic Search (with embeddings)
```python
# Generate embedding for query
query_embedding = openai.embed("How to setup IVR")

# Search similar docs
results = db.query("""
    SELECT title, content,
           1 - (embedding <=> %s) as similarity
    FROM software_docs_embeddings
    WHERE similarity > 0.8
    ORDER BY similarity DESC
    LIMIT 5
""", [query_embedding])
```

### Expert Routing
```sql
-- Find the expert for a software
SELECT get_software_expert('FreeSWITCH');
-- Returns: 'ACS-Voice'
```

---

## Benefits

1. **Offline Access** - No internet dependency
2. **Version Control** - Multiple versions stored
3. **OS-Specific** - Ubuntu 22, Debian 11 docs
4. **Expert Routing** - Queries go to right agent
5. **Searchable** - Full-text + semantic search
6. **Updated** - Monthly refresh cycle

---

## Example Queries

### ACS-Manager handles:
- "How do I configure FreeSWITCH?" → Routes to ACS-Voice
- "React hooks documentation" → Returns from KB
- "Setup LiveKit with Whisper" → Routes to ACS-Voice-Agent
- "PostgreSQL optimization tips" → Returns from KB or routes

### Direct KB Returns:
- API references
- Configuration examples
- Common errors
- Best practices

### Routed to Experts:
- Complex implementations
- Troubleshooting
- Integration questions
- Architecture decisions

---

## Maintenance

### Monthly Tasks
- Update software versions
- Import new documentation
- Remove deprecated docs
- Update search indexes

### Quarterly Tasks
- Review agent expertise mappings
- Analyze query patterns
- Optimize search performance
- Archive old versions

---

*Software KB Architecture v1.0*
