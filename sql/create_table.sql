CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT,
    content TEXT,
    source_type TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    vector_embedding VECTOR(384)
);