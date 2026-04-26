from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Cấu hình CORS để Frontend (hoặc UI khác) có thể truy cập API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong thực tế nên sửa thành domain của Frontend (vd: http://localhost:8501)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đấu nối các endpoints từ thư mục app/api/endpoints.py
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Onboarding Assistant API"}

if __name__ == "__main__":
    import uvicorn
    # Entry point for backend
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
