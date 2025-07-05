import os
from dotenv import load_dotenv

# Chỉ load .env nếu chưa có sẵn biến trong hệ thống
if not os.getenv("SUPABASE_CONN_STRING") or not os.getenv("OPENROUTER_API_KEY"):
    load_dotenv()

# Lấy biến môi trường
SUPABASE_CONN_STRING = os.getenv("SUPABASE_CONN_STRING")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Kiểm tra bắt buộc
if not SUPABASE_CONN_STRING:
    raise RuntimeError("SUPABASE_CONN_STRING is missing!")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is missing!")

# Hàm kiểm tra môi trường local
def is_local():
    return ENVIRONMENT.lower() == "local"
