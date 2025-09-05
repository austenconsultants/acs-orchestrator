#!/usr/bin/env python3
"""
ACS Multi-Tenant Domain API
Manages domain isolation for FreeSWITCH tenants
"""

from flask import Flask, request, jsonify
import psycopg2
import json
from datetime import datetime

app = Flask(__name__)

# Database config
DB_CONFIG = {
    "host": "10.152.0.76",
    "database": "acs_context_db",
    "user": "acs_chat_user",
    "password": "chatdb123"
}

@app.route('/api/domains', methods=['GET'])
def list_domains():
    """List all active domains for dropdown"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT 
                d.id,
                d.domain_name,
                d.display_name,
                d.description,
                d.status,
                d.tier,
                d.features,
                COUNT(DISTINCT de.id) as extension_count
            FROM domains d
            LEFT JOIN domain_extensions de ON d.id = de.domain_id
            WHERE d.status = 'active'
            GROUP BY d.id
            ORDER BY d.display_name
        """)
        
        domains = []
        for row in cur.fetchall():
            domains.append({
                "id": row[0],
                "domain_name": row[1],
                "display_name": row[2],
                "description": row[3],
                "status": row[4],
                "tier": row[5],
                "features": row[6] or {},
                "extension_count": row[7]
            })
        
        return jsonify({"domains": domains})
        
    finally:
        cur.close()
        conn.close()

@app.route('/api/domains/<int:domain_id>/context', methods=['GET'])
def get_domain_context(domain_id):
    """Get domain-specific context for agents"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # Get domain details
        cur.execute("""
            SELECT 
                domain_name,
                display_name,
                freeswitch_profile,
                sip_realm,
                features,
                max_extensions,
                max_concurrent_calls
            FROM domains 
            WHERE id = %s
        """, (domain_id,))
        
        domain = cur.fetchone()
        if not domain:
            return jsonify({"error": "Domain not found"}), 404
        
        # Get extensions
        cur.execute("""
            SELECT extension, first_name, last_name, registered
            FROM domain_extensions
            WHERE domain_id = %s
            ORDER BY extension
        """, (domain_id,))
        
        extensions = []
        for ext in cur.fetchall():
            extensions.append({
                "extension": ext[0],
                "name": f"{ext[1]} {ext[2]}".strip(),
                "registered": ext[3]
            })
        
        # Get recent calls
        cur.execute("""
            SELECT 
                caller_id_number,
                destination_number,
                direction,
                duration,
                start_stamp
            FROM domain_call_records
            WHERE domain_id = %s
            ORDER BY start_stamp DESC
            LIMIT 10
        """, (domain_id,))
        
        recent_calls = []
        for call in cur.fetchall():
            recent_calls.append({
                "from": call[0],
                "to": call[1],
                "direction": call[2],
                "duration": call[3],
                "timestamp": call[4].isoformat() if call[4] else None
            })
        
        return jsonify({
            "domain": {
                "name": domain[0],
                "display_name": domain[1],
                "profile": domain[2],
                "realm": domain[3],
                "features": domain[4] or {},
                "limits": {
                    "max_extensions": domain[5],
                    "max_concurrent_calls": domain[6]
                }
            },
            "extensions": extensions,
            "recent_calls": recent_calls
        })
        
    finally:
        cur.close()
        conn.close()

@app.route('/api/domains/<int:domain_id>/memory', methods=['POST'])
def save_domain_memory(domain_id):
    """Save domain-specific memory/context"""
    data = request.json
    key = data.get('key')
    value = data.get('value')
    
    if not key or not value:
        return jsonify({"error": "Key and value required"}), 400
    
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # Save to user_memory with domain_id
        cur.execute("""
            INSERT INTO user_memory (user_id, domain_id, key, value, type)
            VALUES ('domain_context', %s, %s, %s, 'domain')
            ON CONFLICT (user_id, key) 
            DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP
        """, (domain_id, key, json.dumps(value)))
        
        conn.commit()
        return jsonify({"status": "saved"})
        
    finally:
        cur.close()
        conn.close()

@app.route('/api/domains/<int:domain_id>/stats', methods=['GET'])
def get_domain_stats(domain_id):
    """Get domain statistics"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    try:
        # Get call stats
        cur.execute("""
            SELECT 
                COUNT(*) as total_calls,
                SUM(duration) as total_minutes,
                AVG(duration) as avg_duration,
                COUNT(CASE WHEN direction = 'inbound' THEN 1 END) as inbound_calls,
                COUNT(CASE WHEN direction = 'outbound' THEN 1 END) as outbound_calls
            FROM domain_call_records
            WHERE domain_id = %s
            AND start_stamp >= CURRENT_DATE - INTERVAL '30 days'
        """, (domain_id,))
        
        stats = cur.fetchone()
        
        return jsonify({
            "stats": {
                "total_calls": stats[0] or 0,
                "total_minutes": (stats[1] or 0) // 60,
                "avg_duration": (stats[2] or 0) // 60 if stats[2] else 0,
                "inbound_calls": stats[3] or 0,
                "outbound_calls": stats[4] or 0
            }
        })
        
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    print("🏢 Starting Domain Management API...")
    print("📍 Endpoints:")
    print("   GET  /api/domains - List domains for dropdown")
    print("   GET  /api/domains/{id}/context - Get domain context")
    print("   POST /api/domains/{id}/memory - Save domain memory")
    print("   GET  /api/domains/{id}/stats - Get domain stats")
    app.run(host='0.0.0.0', port=5051, debug=False)
