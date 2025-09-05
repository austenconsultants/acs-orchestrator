-- Software Documentation Knowledge Base
-- Extends the existing knowledge_base table with software-specific structure

\c acs_context_db;

-- ============================================
-- SOFTWARE DOCUMENTATION SCHEMA
-- ============================================

-- Software catalog (what we're tracking)
DROP TABLE IF EXISTS software_catalog CASCADE;
CREATE TABLE software_catalog (
    id SERIAL PRIMARY KEY,
    software_name VARCHAR(100) NOT NULL,
    vendor VARCHAR(100),
    category VARCHAR(50), -- 'telephony', 'framework', 'language', 'database'
    current_version VARCHAR(50),
    documentation_url TEXT,
    license_type VARCHAR(50),
    active BOOLEAN DEFAULT true,
    UNIQUE(software_name)
);

-- Version-specific documentation
DROP TABLE IF EXISTS software_docs CASCADE;
CREATE TABLE software_docs (
    id SERIAL PRIMARY KEY,
    software_id INTEGER REFERENCES software_catalog(id),
    version VARCHAR(50) NOT NULL,
    os_type VARCHAR(50), -- 'ubuntu22', 'debian11', 'any'
    doc_type VARCHAR(50), -- 'api', 'config', 'tutorial', 'reference'
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    original_url TEXT, -- where it came from
    file_path TEXT, -- local file location if large
    search_vector tsvector,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_validated TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    UNIQUE(software_id, version, title)
);

CREATE INDEX idx_software_docs_search ON software_docs USING GIN(search_vector);
CREATE INDEX idx_software_docs_software ON software_docs(software_id, version);

-- Software dependencies
DROP TABLE IF EXISTS software_dependencies CASCADE;
CREATE TABLE software_dependencies (
    id SERIAL PRIMARY KEY,
    software_id INTEGER REFERENCES software_catalog(id),
    depends_on INTEGER REFERENCES software_catalog(id),
    version_constraint VARCHAR(50),
    dependency_type VARCHAR(20) -- 'required', 'optional', 'development'
);

-- Agent software expertise mapping
DROP TABLE IF EXISTS agent_software_expertise CASCADE;
CREATE TABLE agent_software_expertise (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    software_id INTEGER REFERENCES software_catalog(id),
    expertise_level INTEGER CHECK (expertise_level BETWEEN 1 AND 10),
    primary_expert BOOLEAN DEFAULT false,
    UNIQUE(agent_name, software_id)
);

-- ============================================
-- POPULATE SOFTWARE CATALOG
-- ============================================

INSERT INTO software_catalog (software_name, vendor, category, current_version) VALUES
-- Core Technologies
('FreeSWITCH', 'SignalWire', 'telephony', '1.10.11'),
('Node.js', 'OpenJS Foundation', 'runtime', '20.11.0'),
('React', 'Meta', 'framework', '18.2.0'),
('PostgreSQL', 'PostgreSQL Global', 'database', '15.5'),
('Redis', 'Redis Ltd', 'cache', '7.2.4'),
('Docker', 'Docker Inc', 'container', '24.0.7'),
('Python', 'Python Software Foundation', 'language', '3.11.7'),

-- AI/ML Technologies
('LiveKit', 'LiveKit Inc', 'webrtc', '1.5.3'),
('OpenAI API', 'OpenAI', 'ai_service', 'v1'),
('Whisper', 'OpenAI', 'ai_model', '20230918'),
('Cartesia', 'Cartesia', 'tts', 'v1'),

-- Web Technologies
('Express.js', 'OpenJS Foundation', 'framework', '4.18.2'),
('FastAPI', 'Sebastian Ramirez', 'framework', '0.109.0'),
('Next.js', 'Vercel', 'framework', '14.1.0'),
('Tailwind CSS', 'Tailwind Labs', 'framework', '3.4.1');

-- Map agent expertise
INSERT INTO agent_software_expertise (agent_name, software_id, expertise_level, primary_expert) VALUES
-- ACS-Voice is the FreeSWITCH expert
('ACS-Voice', (SELECT id FROM software_catalog WHERE software_name = 'FreeSWITCH'), 10, true),
('ACS-Voice', (SELECT id FROM software_catalog WHERE software_name = 'Express.js'), 7, false),

-- ACS-Voice-Agent is the AI/WebRTC expert
('ACS-Voice-Agent', (SELECT id FROM software_catalog WHERE software_name = 'LiveKit'), 10, true),
('ACS-Voice-Agent', (SELECT id FROM software_catalog WHERE software_name = 'OpenAI API'), 10, true),
('ACS-Voice-Agent', (SELECT id FROM software_catalog WHERE software_name = 'Whisper'), 9, true),
('ACS-Voice-Agent', (SELECT id FROM software_catalog WHERE software_name = 'Python'), 8, false),

-- ACS-Manager knows a bit of everything
('ACS-Manager', (SELECT id FROM software_catalog WHERE software_name = 'PostgreSQL'), 8, false),
('ACS-Manager', (SELECT id FROM software_catalog WHERE software_name = 'Node.js'), 7, false),
('ACS-Manager', (SELECT id FROM software_catalog WHERE software_name = 'Docker'), 6, false);

-- ============================================
-- SEARCH FUNCTIONS
-- ============================================

-- Function to search software documentation
CREATE OR REPLACE FUNCTION search_software_docs(
    p_query TEXT,
    p_software_names TEXT[] DEFAULT NULL,
    p_versions TEXT[] DEFAULT NULL,
    p_limit INTEGER DEFAULT 10
) RETURNS TABLE(
    software_name VARCHAR,
    version VARCHAR,
    title VARCHAR,
    content TEXT,
    relevance FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sc.software_name,
        sd.version,
        sd.title,
        sd.content,
        ts_rank(sd.search_vector, plainto_tsquery('english', p_query)) as relevance
    FROM software_docs sd
    JOIN software_catalog sc ON sd.software_id = sc.id
    WHERE 
        sd.search_vector @@ plainto_tsquery('english', p_query)
        AND (p_software_names IS NULL OR sc.software_name = ANY(p_software_names))
        AND (p_versions IS NULL OR sd.version = ANY(p_versions))
    ORDER BY relevance DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Function to get expert for software
CREATE OR REPLACE FUNCTION get_software_expert(p_software_name VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    v_expert VARCHAR;
BEGIN
    SELECT ase.agent_name INTO v_expert
    FROM agent_software_expertise ase
    JOIN software_catalog sc ON ase.software_id = sc.id
    WHERE sc.software_name = p_software_name
      AND ase.primary_expert = true
    LIMIT 1;
    
    RETURN COALESCE(v_expert, 'ACS-Manager');
END;
$$ LANGUAGE plpgsql;

-- Update trigger for search vector
CREATE OR REPLACE FUNCTION update_software_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', 
        COALESCE(NEW.title, '') || ' ' || 
        COALESCE(NEW.content, '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER software_docs_search_update
    BEFORE INSERT OR UPDATE ON software_docs
    FOR EACH ROW
    EXECUTE FUNCTION update_software_search_vector();

-- ============================================
-- VIEWS FOR EASY ACCESS
-- ============================================

CREATE OR REPLACE VIEW software_knowledge_summary AS
SELECT 
    sc.software_name,
    sc.current_version,
    sc.category,
    COUNT(sd.id) as doc_count,
    ARRAY_AGG(DISTINCT sd.version) as documented_versions,
    ARRAY_AGG(DISTINCT sd.doc_type) as doc_types,
    MAX(sd.imported_at) as last_updated
FROM software_catalog sc
LEFT JOIN software_docs sd ON sc.id = sd.software_id
GROUP BY sc.id, sc.software_name, sc.current_version, sc.category
ORDER BY sc.category, sc.software_name;

COMMENT ON TABLE software_catalog IS 'Catalog of all software we maintain documentation for';
COMMENT ON TABLE software_docs IS 'Version-specific documentation for each software';
COMMENT ON TABLE agent_software_expertise IS 'Maps which agents are experts on which software';
