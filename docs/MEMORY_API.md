# Memory System API Reference

## Python SDK Examples

### 1. Store User Memory
```python
from acs_memory import MemoryManager

memory = MemoryManager()

# Store a user preference
memory.store_user_memory(
    user_id="user-123",
    key="appointment_preference",
    value="mornings only",
    memory_type="preference",
    learned_from="ACS-Voice",
    confidence=0.9
)
```

### 2. Retrieve User Context
```python
# Get all memories for a user
user_context = memory.get_user_context("user-123")

# Get specific memory type
preferences = memory.get_user_memories(
    "user-123", 
    memory_type="preference"
)
```

### 3. Store Conversation
```python
# Store a conversation turn
memory.store_conversation(
    session_id="session-456",
    user_id="user-123",
    agent_name="ACS-Manager",
    message_type="user",
    content="I need help with my bill",
    intent="billing_inquiry",
    sentiment="neutral"
)
```

### 4. Semantic Search
```python
# Search memories semantically
results = memory.semantic_search(
    query="customer service issues",
    memory_types=["knowledge_base", "system_memory"],
    limit=5
)

for result in results:
    print(f"Score: {result.similarity:.2f}")
    print(f"Content: {result.content}")
```

### 5. Knowledge Base Operations
```python
# Add knowledge article
kb_id = memory.add_knowledge(
    title="Handling Angry Customers",
    content="Best practices for de-escalation...",
    category="customer_service",
    tags=["soft_skills", "escalation"],
    created_by="ACS-Manager"
)

# Update effectiveness score
memory.update_knowledge_effectiveness(
    kb_id=kb_id,
    was_helpful=True
)
```

### 6. Session Management
```python
# Start a new session
session = memory.start_session(
    user_id="user-123",
    channel="phone"
)

# Update session context in Redis
memory.update_session_context(
    session_id=session.id,
    context={
        "current_topic": "billing",
        "mood": "frustrated"
    }
)

# End session and persist
memory.end_session(
    session_id=session.id,
    resolution_status="resolved",
    satisfaction_score=4
)
```

---

## SQL Queries

### Find User's Recent Interactions
```sql
SELECT c.*, s.channel, s.resolution_status
FROM conversations c
JOIN user_sessions s ON c.session_id = s.session_id::text
WHERE c.user_id = 'user-123'
  AND c.timestamp > NOW() - INTERVAL '30 days'
ORDER BY c.timestamp DESC;
```

### Get Most Effective Knowledge Articles
```sql
SELECT title, content, usage_count, effectiveness_score
FROM knowledge_base
WHERE status = 'active'
  AND effectiveness_score > 0.7
ORDER BY usage_count DESC
LIMIT 10;
```

### User Memory Summary
```sql
SELECT 
    memory_type,
    COUNT(*) as memory_count,
    AVG(confidence) as avg_confidence,
    MAX(last_referenced) as last_used
FROM user_memory
WHERE user_id = 'user-123'
GROUP BY memory_type;
```

---

## Redis Commands

### Session Management
```redis
# Set session context (1 hour TTL)
SET session:abc123 '{"topic":"billing","user_id":"user-123"}' EX 3600

# Get session
GET session:abc123

# Add to conversation stream
XADD conversation:abc123 * role user content "Hello"
XADD conversation:abc123 * role agent content "Hi, how can I help?"

# Get conversation history
XRANGE conversation:abc123 - +
```

### User Context Cache
```redis
# Cache user preferences
HSET user:123:prefs appointment "morning"
HSET user:123:prefs communication "email"

# Set expiry
EXPIRE user:123:prefs 86400

# Get all preferences
HGETALL user:123:prefs
```

### Knowledge Cache
```redis
# Cache frequently used knowledge
SET kb:article:456 '{"title":"FAQ","content":"..."}' EX 3600

# Track usage
ZINCRBY kb:popular 1 "article:456"

# Get top 10 popular articles
ZREVRANGE kb:popular 0 9 WITHSCORES
```

---

## REST API Endpoints

### Memory Operations
```yaml
POST /api/memory/user
  Body: {user_id, key, value, type}
  
GET /api/memory/user/{user_id}
  Query: ?type=preference&limit=10

POST /api/memory/conversation
  Body: {session_id, user_id, content, ...}
  
GET /api/memory/search
  Query: ?q=billing&types=kb,system&limit=5
```

### Knowledge Base
```yaml
GET /api/knowledge
  Query: ?category=customer_service&status=active

POST /api/knowledge
  Body: {title, content, category, tags}
  
PUT /api/knowledge/{kb_id}/effectiveness
  Body: {was_helpful: true}

POST /api/knowledge/sync-wiki
  Triggers wiki synchronization
```

---

*API Reference v1.0*
