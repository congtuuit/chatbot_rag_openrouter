# rag.py
from embedding import get_embedding
from database import search_similar_vectors
import httpx
import os
from config import OPENROUTER_API_KEY

async def get_answer_with_rag(query, user_id):
    try:
        embed = get_embedding(query)
        chunks = search_similar_vectors(embed)

        if not chunks:
            return "Xin lỗi, tôi không tìm thấy thông tin liên quan để trả lời câu hỏi của bạn."

        context = "\n\n".join([f"{c[1]}\n{c[2]}" for c in chunks])
        prompt = f"Dựa trên thông tin sau, hãy trả lời câu hỏi của khách hàng:\n{context}\n\nCâu hỏi: {query}\nTrả lời:"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openai/gpt-3.5-turbo-0613",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
            
            if response.status_code == 200:
                completion = response.json()
                return completion['choices'][0]['message']['content']
            else:
                print(f"OpenRouter API error: {response.status_code} - {response.text}")
                return f"Xin lỗi, có lỗi xảy ra khi gọi AI service. Mã lỗi: {response.status_code}"
                
    except Exception as e:
        print(f"Error in get_answer_with_rag: {str(e)}")
        return f"Xin lỗi, có lỗi xảy ra: {str(e)}"
