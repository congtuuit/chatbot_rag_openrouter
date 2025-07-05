# 🧠 Mô tả
# - Framework: FastAPI (thay cho Flask)
# - Vector Search: Supabase PostgreSQL + pgvector
# - AI Model: OpenRouter.ai (Free models)
# - Dùng để xử lý tin nhắn từ Facebook Fanpage, tìm kiếm dữ liệu nội bộ, trả lời bằng AI

# 📁 Cấu trúc thư mục
# chatbot_rag_openrouter/
# ├── main.py                # FastAPI entry point
# ├── rag.py                 # Logic tìm kiếm & gọi OpenRouter
# ├── embedding.py           # Tạo vector từ văn bản
# ├── database.py            # Kết nối Supabase & truy vấn + insert
# ├── models.py              # Định nghĩa schema dữ liệu
# ├── create_table.sql       # Tạo bảng knowledge_base
# └── .env                   # Biến môi trường

# 🔧 Cài đặt

## 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 2. Cấu hình môi trường
```bash
# Copy file env.example thành .env
cp env.example .env

# Chỉnh sửa file .env với API keys thực
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
SUPABASE_CONN_STRING=your_supabase_connection_string
```

## 3. Setup Database
- Tạo database trong Supabase
- Chạy script `sql/create_table.sql` để tạo bảng

## 4. Chạy ứng dụng
```bash
uvicorn main:app --reload
```

## 5. Test API
- GET `/` - Kiểm tra server
- GET `/health` - Health check
- POST `/ingest` - Thêm dữ liệu vào knowledge base
- POST `/webhook` - Webhook cho Facebook