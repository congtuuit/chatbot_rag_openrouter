# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from rag import get_answer_with_rag
from database import insert_knowledge_item
from models import KnowledgeItem, QueryRequest
import os

app = FastAPI()

class WebhookPayload(BaseModel):
    message: dict
    sender: dict

@app.post("/webhook")
async def handle_facebook_webhook(payload: WebhookPayload):
    message = payload.message.get("text", "")
    user_id = payload.sender.get("id")
    if not message:
        return {"status": "no message"}

    response = await get_answer_with_rag(message, user_id)
    return {"reply": response}

@app.post("/ingest")
async def ingest_knowledge(item: KnowledgeItem):
    try:
        insert_knowledge_item(
            title=item.title,
            content=item.content,
            source_type=item.source_type,
            source_url=item.source_url
        )
        return {"status": "inserted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/ask")
async def ask_api(request: QueryRequest):
    response = await get_answer_with_rag(request.query, request.user_id)
    return {"reply": response}

@app.get("/")
async def root():
    return {"message": "Chatbot RAG API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
