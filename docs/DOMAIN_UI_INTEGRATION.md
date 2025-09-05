# 🏢 Multi-Tenant Domain UI Integration Guide

## For Chat UI Developers

### 1. Domain Dropdown Component

```jsx
// React component for domain selector
import React, { useState, useEffect } from 'react';

const DomainSelector = ({ onDomainChange }) => {
  const [domains, setDomains] = useState([]);
  const [selectedDomain, setSelectedDomain] = useState(null);
  
  useEffect(() => {
    // Fetch available domains
    fetch('http://10.152.0.70:5051/api/domains')
      .then(res => res.json())
      .then(data => {
        setDomains(data.domains);
        // Default to first domain
        if (data.domains.length > 0) {
          setSelectedDomain(data.domains[0]);
          onDomainChange(data.domains[0]);
        }
      });
  }, []);
  
  const handleDomainChange = (e) => {
    const domain = domains.find(d => d.id === parseInt(e.target.value));
    setSelectedDomain(domain);
    onDomainChange(domain);
  };
  
  return (
    <div className="domain-selector">
      <label>🏢 Select Domain:</label>
      <select 
        value={selectedDomain?.id || ''} 
        onChange={handleDomainChange}
        className="domain-dropdown"
      >
        {domains.map(domain => (
          <option key={domain.id} value={domain.id}>
            {domain.display_name} ({domain.extension_count} extensions)
          </option>
        ))}
      </select>
      {selectedDomain && (
        <div className="domain-info">
          <small>Tier: {selectedDomain.tier} | Status: {selectedDomain.status}</small>
        </div>
      )}
    </div>
  );
};
```

### 2. Pass Domain Context to Agents

```javascript
// When sending messages to agents, include domain context
const sendMessageToAgent = async (message, domainId) => {
  // Get domain context first
  const contextResponse = await fetch(`http://10.152.0.70:5051/api/domains/${domainId}/context`);
  const domainContext = await contextResponse.json();
  
  // Include in agent message
  const agentMessage = {
    user_message: message,
    domain: {
      id: domainId,
      name: domainContext.domain.name,
      display_name: domainContext.domain.display_name,
      realm: domainContext.domain.realm,
      features: domainContext.domain.features,
      extensions: domainContext.extensions
    }
  };
  
  // Send to appropriate agent
  const response = await fetch('your-agent-endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(agentMessage)
  });
  
  return response.json();
};
```

### 3. Display Domain Stats

```jsx
const DomainStats = ({ domainId }) => {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    if (domainId) {
      fetch(`http://10.152.0.70:5051/api/domains/${domainId}/stats`)
        .then(res => res.json())
        .then(data => setStats(data.stats));
    }
  }, [domainId]);
  
  if (!stats) return <div>Loading stats...</div>;
  
  return (
    <div className="domain-stats">
      <h4>📊 Domain Statistics (Last 30 Days)</h4>
      <ul>
        <li>Total Calls: {stats.total_calls}</li>
        <li>Total Minutes: {stats.total_minutes}</li>
        <li>Inbound: {stats.inbound_calls}</li>
        <li>Outbound: {stats.outbound_calls}</li>
        <li>Avg Duration: {stats.avg_duration} min</li>
      </ul>
    </div>
  );
};
```

## For Agent Developers

### Agent Domain Awareness

```python
# In your agent code
class DomainAwareAgent:
    def __init__(self):
        self.current_domain = None
        
    def set_domain_context(self, domain_info):
        """Set the current domain context"""
        self.current_domain = domain_info
        
        # Update FreeSWITCH commands to use domain
        self.fs_domain = domain_info.get('realm', 'acs.local')
        self.sip_profile = domain_info.get('profile', 'internal')
        
    def handle_message(self, message, domain_info):
        """Process message with domain context"""
        self.set_domain_context(domain_info)
        
        # Now all operations are domain-scoped
        if "list extensions" in message.lower():
            return self.list_domain_extensions()
        elif "create extension" in message.lower():
            return self.create_domain_extension()
            
    def list_domain_extensions(self):
        """List extensions for current domain only"""
        if not self.current_domain:
            return "No domain selected"
            
        # Query only this domain's extensions
        query = f"""
            SELECT extension, first_name, last_name, registered
            FROM domain_extensions
            WHERE domain_id = {self.current_domain['id']}
            ORDER BY extension
        """
        # Execute and return results
        
    def execute_fs_command(self, command):
        """Execute FreeSWITCH command for specific domain"""
        # Always include domain in FS commands
        domain_cmd = f"{command}@{self.fs_domain}"
        return self.fs_api.execute(domain_cmd)
```

### Domain-Specific Memory

```python
# Save domain-specific knowledge
def save_domain_memory(domain_id, key, value):
    response = requests.post(
        f'http://10.152.0.70:5051/api/domains/{domain_id}/memory',
        json={'key': key, 'value': value}
    )
    return response.json()

# Example: Remember domain-specific IVR setup
save_domain_memory(
    domain_id=2,
    key='ivr_config',
    value={
        'main_menu': '5000',
        'options': {
            '1': 'sales',
            '2': 'support',
            '3': 'billing'
        }
    }
)
```

## Database Queries

### Always Filter by Domain

```sql
-- Bad (shows all domains' data)
SELECT * FROM domain_extensions;

-- Good (domain-specific)
SELECT * FROM domain_extensions WHERE domain_id = :domain_id;

-- Join with domain info
SELECT 
    de.extension,
    de.first_name,
    de.last_name,
    d.domain_name,
    d.display_name
FROM domain_extensions de
JOIN domains d ON d.id = de.domain_id
WHERE d.id = :domain_id
ORDER BY de.extension;
```

## API Endpoints Summary

### Domain Management (Port 5051)
- `GET  /api/domains` - List all domains for dropdown
- `GET  /api/domains/{id}/context` - Get full domain context
- `POST /api/domains/{id}/memory` - Save domain-specific memory
- `GET  /api/domains/{id}/stats` - Get domain statistics

### Usage Example

```bash
# List domains
curl http://10.152.0.70:5051/api/domains

# Get domain context
curl http://10.152.0.70:5051/api/domains/1/context

# Save domain memory
curl -X POST http://10.152.0.70:5051/api/domains/1/memory \
  -H "Content-Type: application/json" \
  -d '{"key":"last_ivr_update","value":"2025-01-04"}'

# Get stats
curl http://10.152.0.70:5051/api/domains/1/stats
```

## Sample Domains Created

1. **ACS Master Domain** (acs.local)
   - Full features enabled
   - System-wide administration

2. **Acme Corporation** (customer1.acs.local)
   - Business customer
   - Recording disabled

3. **TechStart Inc** (customer2.acs.local)
   - Startup customer
   - IVR disabled

---

*Multi-tenant support ready for production!*
