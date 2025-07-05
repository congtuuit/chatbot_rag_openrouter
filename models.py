
# models.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    user_id: str

class KnowledgeItem(BaseModel):
    title: str
    content: str
    source_type: str = "custom"
    source_url: str = ""