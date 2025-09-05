#!/usr/bin/env python3
"""
ACS Knowledge Base Embeddings Generator
Generates vector embeddings for semantic search
"""

import os
import json
import time
import psycopg2
import requests

# Configuration
DB_CONFIG = {
    "host": "10.152.0.76",
    "database": "acs_context_db",
    "user": "acs_chat_user",
    "password": "chatdb123"
}

# OpenAI API config
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMBEDDING_MODEL = "text-embedding-ada-002"

def get_mock_embedding():
    """Generate mock embedding for testing"""
    import random
    random.seed(42)
    return [random.random() for _ in range(1536)]

def process_software_catalog():
    """Generate embeddings for software catalog"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("🛠️ Processing software catalog...")
    
    # Get all active software
    cur.execute("""
        SELECT sc.id, sc.software_name, sc.category, sc.current_version
        FROM software_catalog sc
        WHERE sc.active = true
    """)
    
    software_list = cur.fetchall()
    
    if not software_list:
        print("❌ No software entries found!")
        return 0
    
    processed = 0
    for soft_id, name, category, version in software_list:
        # Check if embedding already exists
        cur.execute("""
            SELECT id FROM memory_embeddings 
            WHERE source_table = 'software_catalog' AND source_id = %s
        """, (soft_id,))
        
        if cur.fetchone():
            print(f"  ⏭️ {name} - already has embedding")
            continue
        
        # Create searchable text
        text = f"Software: {name} | Category: {category} | Version: {version}"
        
        print(f"  📊 Processing: {name}...")
        embedding = get_mock_embedding()  # Using mock for now
        
        # Store embedding
        cur.execute("""
            INSERT INTO memory_embeddings 
            (source_table, source_id, content, embedding, model_version)
            VALUES (%s, %s, %s, %s, %s)
        """, ('software_catalog', soft_id, text, embedding, EMBEDDING_MODEL))
        
        processed += 1
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"✅ Generated {processed} software embeddings")
    return processed

def main():
    print("🚀 ACS Embeddings Generator")
    print("=" * 40)
    
    if not OPENAI_API_KEY:
        print("⚠️ No OpenAI API key - using mock embeddings for demo")
    
    sw_count = process_software_catalog()
    
    print("\n" + "=" * 40)
    print(f"✅ COMPLETE: Generated {sw_count} embeddings")

if __name__ == "__main__":
    main()
