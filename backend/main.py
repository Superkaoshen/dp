from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os

app = FastAPI()

# 允许所有跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Qwen API配置
QWEN_API_URL = "https://gpt-best.apifox.cn/api/v1/chat/completions"  # 你可以根据实际文档调整
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "your_api_key")  # 建议用环境变量
QWEN_MODEL = "Qwen-14B-Chat"  # 根据实际API文档填写

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/chat")
async def chat(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": QWEN_MODEL,
        "messages": [m.model_dump() for m in req.messages],
        "temperature": 0.7
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(QWEN_API_URL, headers=headers, json=data)
        resp.raise_for_status()
        result = resp.json()
    # 只返回AI回复内容
    answer = result["choices"][0]["message"]["content"]
    return {"reply": answer}