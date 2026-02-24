import uvicorn
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm_service.QA import generate_lawyer_chat

try:
    from routes.Zhejiang.la import router as zj_la_router
    from routes.Zhejiang.el import router as zj_el_router
    from routes.Guangdong.la import router as gd_la_router
    from routes.Guangdong.el import router as gd_el_router
    from routes.others.wia import router as wia_router
except ImportError as e:
    print(f"⚠️ 路由模块导入失败，跳过注册: {e}")
    from fastapi import APIRouter
    zj_la_router = zj_el_router = gd_la_router = gd_el_router = wia_router = APIRouter()

app = FastAPI(title="PartLawyer API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(zj_la_router, prefix="/api/zhejiang/la", tags=["浙江仲裁"])
app.include_router(zj_el_router, prefix="/api/zhejiang/el", tags=["浙江证据"])
app.include_router(gd_la_router, prefix="/api/guangdong/la", tags=["广东仲裁"])
app.include_router(gd_el_router, prefix="/api/guangdong/el", tags=["广东证据"])
app.include_router(wia_router, prefix="/api/wia", tags=["工伤仲裁"])

@app.get("/")
async def root():
    return {"status": "online", "message": "PartLawyer AI Backend is Running."}

class QuestionRequest(BaseModel):
    question: str

@app.post("/api/ask")
async def qa_endpoint(req: QuestionRequest):
    chat_history = [{"role": "user", "content": req.question}]

    async def generate_stream():
        try:
            async for chunk in generate_lawyer_chat(history=chat_history):
                if chunk:
                    yield chunk
        except Exception as e:
            yield f"⚠️ 服务器内部错误: {str(e)}"

    # ==========================================
    # 核心修复区：加上禁用缓存的 Headers 和事件流 media_type
    # ==========================================
    return StreamingResponse(
        generate_stream(), 
        media_type="text/event-stream",  # 明确告诉前端和服务器：这是连绵不断的事件流
        headers={
            "Cache-Control": "no-cache", # 严禁浏览器缓存
            "Connection": "keep-alive",  # 保持连接不断开
            "X-Accel-Buffering": "no"    # 严禁网关/代理层（如 Nginx）缓冲数据
        }
    )

if __name__ == "__main__":
    print("🚀 服务启动中: http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)