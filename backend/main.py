from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class MessageCreate(BaseModel):
    content: str
    channel_id: int
    pinned: Optional[bool] = False

@app.post("/messages")
async def create_message(msg: MessageCreate):
    return {"ok": True, "message:": msg}

@app.get("/channels/{channel_id}")
async def get_channel(channel_id: int, limit: int = 50):
    return {"channel_id": channel_id, "limit:": limit}


@app.get("/")
async def root():
    return {"message: hello"}