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
    allow_headers=["*"]


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

USERS_FILE = f"{DATA_DIR}/users.json"
CHANNELS_FILE = f"{DATA_DIR}/channels.json"
SERVERS_FILE = f"{DATA_DIR}/servers.json"
MESSAGE_FILE = f"{DATA_DIR}/messages.json"




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

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"Message": "Chat App is running"}



@app.post("/register")
async def register_user(username: str, email:str):

    users = load_json(USERS_FILE)

    for user in users:
        if user["email"] == email:
            raise HTTPException(status_code=400, detail="Email has already been registered.")


    new_user = User(
        id=generate_id(),
        username=username,
        email=email,
        created_at=get_timestamp()
    )

    users.append(new_user)
    save_data(USERS_FILE, users)

    return {"Message": "User registered succuessfully", " user": new_user}



    
@app.get("/users/{user_id}")
async def get_user(user_id:str):

    users = load_json(USERS_FILE)

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")



@app.post("/servers")
async def create_server(name:str, owner_id: str, description: Optional[str] = None):
    servers = load_json(SERVERS_FILE)
    channels = load_json(CHANNELS_FILE)

    new_server = Server(
        id=generate_id(),
        name=name,
        description=description,
        owner_id=owner_id,
        members=[owner_id],
        created_at=get_timestamp()
    )

    servers.append(new_server)
    save_data(SERVERS_FILE, servers)

    general_channel = Channel(
       id=generate_id(),
       name="general",
       server_id=new_server.id,
       created_at=get_timestamp()
    )

    channels.append(general_channel)
    save_data(CHANNELS_FILE, channels)

    return {"Message": "Server was created successfully", "Server": new_server}


@app.get("/servers/{server_id}")
async def get_server(server_id: str):
    servers = load_json(SERVERS_FILE)

    for server in servers:
        if server["id"] == server_id:
            return server

    raise HTTPException(status_code=404, detail="Server not found")


# Gets all of the servers a user is apart of
@app.get("/users/{user_id}/server")
async def get_user_server(user_id:str):

    servers = load_json(SERVERS_FILE)

    user_servers = [server for server in servers if user_id in server["member"]]

    return {"Servers": user_servers}



@app.post("/servers/{server_id}/channels")
async def create_channel(server_id: str, channel_name:str, channel_type:str):
    channels = load_json(CHANNELS_FILE)

    new_channel = Channel(
        id=generate_id(),
        name=channel_name,
        server_id=server_id,
        type=channel_type,
        created_at=get_timestamp()
    )

    channels.append(new_channel)

    save_data(CHANNELS_FILE, channels)

    return {"Message": "Channel was create ", "Channel": new_channel}



# Gets all of the channels in a particular server
@app.get("/servers/{server_id}/channels")
async def get_server_channels(server_id: str):
    Channels = load_json(CHANNELS_FILE)
    server_channels = [channel for channel in Channels if channel["server_id"] == server_id]

    return {"All of the channels in this server": server_channels}


@app.post("/channels/{channel_id}/messages")
async def send_message(channel_id:str, content:str, user_id:str):

    messages = load_json(MESSAGE_FILE)

    new_message = Message(
        id=generate_id(),
        content=content,
        user_id=user_id,
        channel_id=channel_id,
        timestamp=get_timestamp()
    )

    messages.append(new_message)

    save_data(MESSAGE_FILE, messages)

    await manager.broadcast_to_channel(
        json.dump(new_message),
        channel_id=channel_id
    )

    return {"Message": "Sucessfully"}


# Gets all of the messages in a channel witihin a limit
@app.get("/channels/{channel_id}/messages")
async def get_channel_messages(channel_id: str, limit:int = 50):
    messages = load_json(MESSAGE_FILE)

    channel_messages = [message for message in messages if message["channel_id"] == channel_id]

    # Have to do reverse or the limit will cut off the newer messages instead of the older ones
    channel_messages.sort(key=lambda x: x["timestamp"], reverse=True)

    # Saves messages only the to the allotted limit and revsere the 
    # list of messages.
    return {"message": channel_messages[:limit][::-1]}


# Websocket endpoint for real time messaging
@app.websocket("/ws/{channel_id}")
async def websocket_endpoint(channel_id:str, websocket:WebSocket):
    await manager.connect(websocket=websocket, channel_id=channel_id)

    try:
        while True:

            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")

    
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket, channel_id=channel_id)


@app.get("/health")
async def check_health():
    return {"Status": "healthy", "timestamp": get_timestamp()}


