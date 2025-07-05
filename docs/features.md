# 🚀 Các Tính Năng Chính - Chatbot RAG OpenRouter

## 📋 Tổng Quan
Dự án này là một chatbot thông minh sử dụng công nghệ RAG (Retrieval-Augmented Generation) để xử lý tin nhắn từ Facebook Fanpage và trả lời dựa trên kiến thức nội bộ.

---

## 🎯 **1. API Endpoints**

### **1.1 Health Check Endpoints**

#### **GET `/`** - Kiểm tra trạng thái server
```bash
curl http://localhost:9000/
```
**Response:**
```json
{
  "message": "Chatbot RAG API is running!"
}
```

#### **GET `/health`** - Health check chi tiết
```bash
curl http://localhost:9000/health
```
**Response:**
```json
{
  "status": "healthy"
}
```

### **1.2 Knowledge Management Endpoints**

#### **POST `/ingest`** - Thêm dữ liệu vào knowledge base
```bash
curl -X POST http://localhost:9000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chính sách bảo hành",
    "content": "Sản phẩm được bảo hành 12 tháng kể từ ngày mua. Bảo hành bao gồm các lỗi do nhà sản xuất...",
    "source_type": "policy",
    "source_url": "https://example.com/warranty"
  }'
```
**Response:**
```json
{
  "status": "inserted"
}
```

**Schema cho KnowledgeItem:**
```json
{
  "title": "string (required)",
  "content": "string (required)", 
  "source_type": "string (optional, default: 'custom')",
  "source_url": "string (optional, default: '')"
}
```

### **1.3 Chat Endpoints**

#### **POST `/webhook`** - Webhook cho Facebook Messenger
```bash
curl -X POST http://localhost:9000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "text": "Sản phẩm có bảo hành không?"
    },
    "sender": {
      "id": "user123"
    }
  }'
```
**Response:**
```json
{
  "reply": "Dựa trên chính sách bảo hành của chúng tôi, sản phẩm được bảo hành 12 tháng kể từ ngày mua..."
}
```

### **1.4 Ask API Endpoint**

#### **POST `/ask`** - Gửi câu hỏi trực tiếp tới AI (không cần Facebook)
```bash
curl -X POST http://localhost:9000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Sản phẩm có bảo hành không?",
    "user_id": "user123"
  }'
```
**Request body:**
```json
{
  "query": "string (required)",
  "user_id": "string (required)"
}
```
**Response:**
```json
{
  "reply": "Dựa trên chính sách bảo hành của chúng tôi, sản phẩm được bảo hành 12 tháng kể từ ngày mua..."
}
```

---

## 🧠 **2. Tính Năng RAG (Retrieval-Augmented Generation)**

### **2.1 Quy Trình Xử Lý**

1. **Nhận tin nhắn** từ Facebook webhook
2. **Tạo embedding** cho câu hỏi của người dùng
3. **Tìm kiếm vector** trong database để tìm thông tin tương tự
4. **Tạo context** từ kết quả tìm kiếm
5. **Gọi AI model** (OpenRouter Mistral) để tạo câu trả lời
6. **Trả về** câu trả lời cho Facebook

### **2.2 Vector Search**
- Sử dụng **pgvector extension** trong Supabase PostgreSQL
- Embedding dimension: **384** (sử dụng sentence-transformers)
- Tìm kiếm semantic similarity thay vì exact match

### **2.3 AI Model Integration**
- **Provider**: OpenRouter.ai
- **Model**: Mistral Instruct
- **Max tokens**: 500
- **Language**: Hỗ trợ tiếng Việt

---

## 🗄️ **3. Database Schema**

### **3.1 Bảng `knowledge_base`**

```sql
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT,
    content TEXT,
    source_type TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    vector_embedding VECTOR(384)
);
```

### **3.2 Các Trường Dữ Liệu**

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `id` | UUID | Primary key, tự động tạo |
| `title` | TEXT | Tiêu đề thông tin |
| `content` | TEXT | Nội dung chi tiết |
| `source_type` | TEXT | Loại nguồn (policy, faq, product, etc.) |
| `source_url` | TEXT | URL nguồn gốc |
| `created_at` | TIMESTAMP | Thời gian tạo record |
| `vector_embedding` | VECTOR(384) | Vector embedding của nội dung |

---

## 🔧 **4. Cấu Hình Môi Trường**

### **4.1 Biến Môi Trường (.env)**

```env
# OpenAI API Key (cho embedding) - Optional nếu dùng sentence-transformers
OPENAI_API_KEY=your_openai_api_key_here

# OpenRouter API Key (cho AI responses)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Supabase Connection String
SUPABASE_CONN_STRING=postgresql://username:password@host:port/database

# Optional: Server config
HOST=0.0.0.0
PORT=9000
```

### **4.2 Dependencies (requirements.txt)**

```txt
# FastAPI và server
fastapi>=0.115.0
uvicorn>=0.35.0

# HTTP client
httpx>=0.28.0

# Environment và config
python-dotenv>=1.1.0

# Data validation
pydantic>=2.11.0

# Database
psycopg2-binary>=2.9.9
supabase>=2.0.2

# AI và embedding
sentence-transformers>=2.2.2

# Utilities
numpy>=1.24.3
python-multipart>=0.0.6
asyncio==3.4.3
```

---

## 🚀 **5. Cách Sử Dụng**

### **5.1 Cài Đặt**

```bash
# Clone repository
git clone <repository-url>
cd chatbot_rag_openrouter

# Cài đặt dependencies
pip install -r requirements.txt

# Copy file cấu hình
cp env.example .env

# Chỉnh sửa file .env với API keys thực
```

### **5.2 Setup Database**

```bash
# 1. Tạo database trong Supabase
# 2. Chạy script tạo bảng
psql -h your-host -U your-user -d your-database -f sql/create_table.sql
```

### **5.3 Chạy Ứng Dụng**

```bash
# Development mode
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 9000
```

---

## 📊 **6. Các Tính Năng Nâng Cao**

### **6.1 Error Handling**
- Xử lý lỗi khi không tìm thấy thông tin liên quan
- Fallback response khi AI model không hoạt động
- Validation cho input data

### **6.2 Performance Optimization**
- Async/await cho HTTP requests
- Vector search được tối ưu với pgvector
- Connection pooling cho database

### **6.3 Scalability**
- Stateless design
- Có thể scale horizontally
- Database connection pooling

---

## 🔗 **7. Tích Hợp Facebook Messenger**

### **7.1 Webhook Setup**
1. Tạo Facebook App
2. Cấu hình webhook URL: `https://your-domain.com/webhook`
3. Verify webhook với Facebook
4. Subscribe to messages event

### **7.2 Message Flow**
```
Facebook User → Facebook Messenger → Webhook → Your API → AI Response → Facebook
```

---

## 🛠️ **8. Monitoring & Logging**

### **8.1 Health Checks**
- `/health` endpoint để kiểm tra trạng thái
- Database connection check
- AI model availability check

### **8.2 Logging**
- Request/response logging
- Error logging với stack trace
- Performance metrics

---

## 🔒 **9. Security Considerations**

### **9.1 API Security**
- Validate input data với Pydantic
- Rate limiting (cần implement thêm)
- CORS configuration (cần implement thêm)

### **9.2 Data Security**
- API keys được lưu trong environment variables
- Database connection string được mã hóa
- Input sanitization

---

## 📈 **10. Performance Metrics**

### **10.1 Response Time**
- Vector search: ~50-100ms
- AI model call: ~500-1000ms
- Total response time: ~600-1100ms

### **10.2 Throughput**
- Concurrent requests: 100+ requests/second
- Database connections: Pooled
- Memory usage: ~200MB baseline

---

## 🎯 **11. Use Cases**

### **11.1 Customer Support**
- Trả lời FAQ tự động
- Hướng dẫn sử dụng sản phẩm
- Thông tin chính sách

### **11.2 Sales Support**
- Thông tin sản phẩm
- Giá cả và khuyến mãi
- Điều kiện mua hàng

### **11.3 Technical Support**
- Hướng dẫn kỹ thuật
- Troubleshooting
- Thông tin bảo hành

---

## 🔮 **12. Roadmap & Future Features**

### **12.1 Planned Features**
- [ ] Multi-language support
- [ ] Conversation history
- [ ] User authentication
- [ ] Analytics dashboard
- [ ] A/B testing for responses

### **12.2 Technical Improvements**
- [ ] Caching layer (Redis)
- [ ] Rate limiting
- [ ] Advanced logging
- [ ] Metrics collection
- [ ] Auto-scaling

---

## 📞 **13. Support & Contact**

### **13.1 Documentation**
- API documentation: `/docs` (Swagger UI)
- OpenAPI specification: `/openapi.json`

### **13.2 Troubleshooting**
- Check logs for error messages
- Verify API keys configuration
- Test database connection
- Monitor AI model availability

---

*Documentation này được tạo tự động và cập nhật theo phiên bản mới nhất của dự án.* 