from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json 
import os
import uuid

from datetime import datetime
import asyncio


app = FastAPI(title="Chat App API", version="1.0.0")


# Add CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Place frontend url here
    allow_credentials=True,
    allow_methods=["*"],
    allow_header=["*"]


)

# Data models 

class User(BaseModel):
    id: str
    username:str
    email:str
    avatar_url: Optional[str] = None
    created_at:str


class Server(BaseModel):
    id:str
    name:str
    description: Optional[str] = None
    owner_id:str
    members: List[str] = []
    created_at: str

class Channel(BaseModel):
    id: str
    name:str
    server_id:str
    type:str = "text"
    created_at:str

class Message(BaseModel):
    id:str
    content:str
    user_id: str
    channel_id:str
    timestamp:str

# File path for JSON files

DATA_DIR = "backend/data"

USERS_DIR = f"{DATA_DIR}/users.json"
CHANNELS_DIR = f"{DATA_DIR}/channels.json"
SERVERS_DIR = f"{DATA_DIR}/servers.json"
MESSAGE_DIR = f"{DATA_DIR}/messages.json"




def load_json(filename:str) -> List[Dict]:

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, 'r') as f:
            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(filename:str, data: List[Dict]):

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def generate_id() -> str:

    return str(uuid.uuid4())

def get_timestamp() -> str:
    
    return datetime.now().isoformat()
    


# Websocket connection manager for real-time features 

class ConnectionManager:

    def __init__(self):

        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel_id:str):

        await websocket.accept()
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = []

        self.active_connections[channel_id].append(websocket)


    def disconnect(self, websocket: WebSocket, channel_id:str):

        if channel_id in self.active_connections:
            self.active_connections[channel_id].remove(websocket)

        
    async def broadcast_to_channel(self, message:str, channel_id:str):

        if channel_id in self.active_connections:

            for connection in self.active_connections[channel_id]:

                try:
                    await connection.send_text(message)

                except:

                    self.active_connections[channel_id].remove(connection)


    
