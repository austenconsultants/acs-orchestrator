#!/usr/bin/env python3
"""
Software Documentation Importer
Downloads and stores software docs locally for offline access
"""

import os
import json
import psycopg2
import requests
from datetime import datetime
import hashlib

class DocImporter:
    def __init__(self):
        self.db_config = {
            'host': '10.152.0.76',
            'port': 5432,
            'database': 'acs_context_db',
            'user': 'acs_chat_user',
            'password': 'chatdb123'
        }
        self.doc_storage = '/opt/acs/knowledge/software_docs'
        
    def import_freeswitch_docs(self, version='1.10.11'):
        """Import FreeSWITCH documentation"""
        docs = [
            {
                'title': 'FreeSWITCH ESL Commands',
                'doc_type': 'api',
                'content': """
                    Core ESL Commands:
                    - api <command> - Execute API command
                    - bgapi <command> - Execute background API
                    - status - System status
                    - sofia status - SIP status
                    - show channels - Active channels
                    - originate - Make outbound call
                    - uuid_kill <uuid> - Hangup call
                    - conference list - Show conferences
                    - reloadxml - Reload configuration
                """
            },
            {
                'title': 'FreeSWITCH Dialplan XML',
                'doc_type': 'config',
                'content': """
                    <extension name="example">
                        <condition field="destination_number" expression="^(\d+)$">
                            <action application="answer"/>
                            <action application="playback" data="welcome.wav"/>
                            <action application="bridge" data="user/$1"/>
                        </condition>
                    </extension>
                """
            },
            {
                'title': 'FreeSWITCH IVR Configuration',
                'doc_type': 'tutorial',
                'content': """
                    IVR Menu Structure:
                    1. Create menu in autoload_configs/ivr_menus.conf.xml
                    2. Define prompts and DTMF mappings
                    3. Set timeout and retry behaviors
                    4. Link to extensions or applications
                """
            }
        ]
        
        self._store_docs('FreeSWITCH', version, 'ubuntu22', docs)
    
    def import_react_docs(self, version='18.2.0'):
        """Import React documentation"""
        docs = [
            {
                'title': 'React Hooks Reference',
                'doc_type': 'api',
                'content': """
                    Essential Hooks:
                    - useState: const [state, setState] = useState(initial)
                    - useEffect: useEffect(() => {}, [deps])
                    - useContext: const value = useContext(MyContext)
                    - useReducer: const [state, dispatch] = useReducer(reducer, initial)
                    - useCallback: const memoized = useCallback(() => {}, [deps])
                    - useMemo: const memoized = useMemo(() => compute, [deps])
                """
            },
            {
                'title': 'React Component Patterns',
                'doc_type': 'tutorial',
                'content': """
                    Common Patterns:
                    1. Container/Presentational Components
                    2. Higher-Order Components (HOCs)
                    3. Render Props
                    4. Custom Hooks
                    5. Context Provider Pattern
                    6. Compound Components
                """
            }
        ]
        
        self._store_docs('React', version, 'any', docs)
    
    def import_nodejs_docs(self, version='20.11.0'):
        """Import Node.js documentation"""
        docs = [
            {
                'title': 'Node.js Core Modules',
                'doc_type': 'reference',
                'content': """
                    Core Modules:
                    - fs: File system operations
                    - path: Path utilities
                    - http/https: HTTP servers
                    - crypto: Cryptographic functions
                    - stream: Stream interfaces
                    - cluster: Multi-process
                    - child_process: Spawn processes
                """
            },
            {
                'title': 'Express.js Middleware',
                'doc_type': 'api',
                'content': """
                    app.use(express.json())
                    app.use(express.urlencoded())
                    app.use(cors())
                    app.use(helmet())
                    
                    Custom middleware:
                    app.use((req, res, next) => {
                        // Process request
                        next()
                    })
                """
            }
        ]
        
        self._store_docs('Node.js', version, 'ubuntu22', docs)
    
    def _store_docs(self, software_name, version, os_type, docs):
        """Store documentation in database"""
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()
        
        # Get software ID
        cur.execute(
            "SELECT id FROM software_catalog WHERE software_name = %s",
            (software_name,)
        )
        result = cur.fetchone()
        if not result:
            print(f"Software {software_name} not found in catalog")
            return
        
        software_id = result[0]
        
        # Insert docs
        for doc in docs:
            try:
                cur.execute("""
                    INSERT INTO software_docs 
                    (software_id, version, os_type, doc_type, title, content)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (software_id, version, title) 
                    DO UPDATE SET 
                        content = EXCLUDED.content,
                        last_validated = CURRENT_TIMESTAMP
                """, (
                    software_id,
                    version,
                    os_type,
                    doc.get('doc_type', 'reference'),
                    doc['title'],
                    doc['content']
                ))
            except Exception as e:
                print(f"Error inserting {doc['title']}: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Imported {len(docs)} docs for {software_name} v{version}")

if __name__ == "__main__":
    importer = DocImporter()
    importer.import_freeswitch_docs()
    importer.import_react_docs()
    importer.import_nodejs_docs()
    print("Documentation import complete!")
