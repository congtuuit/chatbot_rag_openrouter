
# database.py
import psycopg2
import os
from embedding import get_embedding
from config import SUPABASE_CONN_STRING

print(f"SUPABASE_CONN_STRING {SUPABASE_CONN_STRING}")
conn = psycopg2.connect(SUPABASE_CONN_STRING)

# Tìm kiếm vector tương đồng
def search_similar_vectors(query_vector, top_k=3):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, content, 1 - (vector_embedding <=> %s::vector) AS similarity
            FROM knowledge_base
            ORDER BY vector_embedding <=> %s::vector
            LIMIT %s
        """, (query_vector, query_vector, top_k))
        return cur.fetchall()

# Thêm dữ liệu vào knowledge_base
def insert_knowledge_item(title, content, source_type="custom", source_url=""):
    vector = get_embedding(content)
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO knowledge_base (title, content, source_type, source_url, vector_embedding)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, content, source_type, source_url, vector))
        conn.commit()