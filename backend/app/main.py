from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
import json 
import os
import uuid

from datetime import datetime
import aiofiles
import asyncio
from ML.avatar_generator.main import ProfilePictureGenerator


app = FastAPI(title="Chat App API", version="1.0.0")


# Add CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Place frontend url here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]


)


# Using static to create URLS for certain assets like profile pictures 
# the URLs will look like /static/{filename}
# The reason for static is that its faster than just doing /{filename}
# and it sorts which assets are static and not.
# name="static" used to identify URL as static or not Optional but useful
app.mount("/static", StaticFiles(directory="backend/data"), name="static")

# Data models 

class ProfilePictureRequest(BaseModel):
    user_id: str
    description: str
    style: Optional[str] = "cartoon" # cartton, anime, cyberpunk, realistic, fantasy, mimalist
    negative_prompt: Optional[str] = None

class ProfilePictureResponse(BaseModel):
    success: bool
    message: str
    filepath: Optional[str] = None
    style_used: Optional[str] = None
    prompt_used: Optional[str] = None
    generated_at: Optional[str] = None
    file_size: Optional[int] = None
    error: Optional[str] = None

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

profile_generator = ProfilePictureGenerator()
print("Successfully made ProfilePictureGenerator object")



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

"""
    Generate an AI profile picture for a user
    
    This endpoint:
    1. Validates the user exists
    2. Generates an AI image based on user description
    3. Processes it into profile picture format
    4. Saves it to storage
    5. Updates user's avatar URL in database
"""
@app.post("/users/{user_id}/profile_picture/generate", response_model=ProfilePictureResponse)
async def generate_ai_profile_picture(
    user_id: str,
    request: ProfilePictureRequest,
    background_task: BackgroundTasks
):
    try:

        # Verifying if user exists
        users = load_json(USERS_FILE)
        user = None

        for u in users:
            if u["id"] == user_id:
                user = u
                break

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Checking if the style the user picked for their AI generated profile picture is 
        
        valid_styles = ["cartoon", "realistic", "anime", "cyberpunk", "fantasy", "minimalist"]
        if request.style not in valid_styles:
            raise HTTPException(
                status_code=400,
                detail=f"Please select a valid style which are {valid_styles}"
            )
        
        # If both a user exist and the style for prompt is legitimate, then generate the AI profile picture 
        # accordingly to the prompt.
        
        # profile_generator.generate_profile_picture returns a dictionary
        # Ex) 
        # {
        #     "success": False,
        #     "error": str(e),
        #     "filepath": None
        # }
        result = await profile_generator.generate_profile_picture(
            user_description=request.description,
            user_id=user_id,
            style=request.style

        )


        # Return an error response if failed to generate AI profile picture.
        if not result["success"]:
            return ProfilePictureResponse(
                success=False,
                message="Failed to generate AI profile picture.",
                error=result.get("error", "Unknown error")

            )

        
        # Updating User's avatar URL in database
        avatar_url = f"/static/profile_pictures/{result["filepath"]}"


        # Changing the user's avatar to the newly generated one.
        for i, u in enumerate(users):
            if u["id"] == user_id:
                user[i]["avatar_url"] = avatar_url
                break

        save_data(USERS_FILE, users)

        return ProfilePictureResponse(
            success=True,
            message="Profile picture generated successfully",
            filepath=result["filepath"],
            style_used=result["style"],
            prompt_used=result["prompt_used"],
            generated_at=result["generated_at"],
            file_size=result["file_size"]
        )

    # Show the detailed error message if possible else go the the default error message.
    except HTTPException:
        raise

    except Exception as e:
        print(f"Failed to Generate AI Profile Picture")

# Gets user's profile picture
@app.get("/users/{user_id}/profile-picture")
async def get_user_profile_picture(user_id:str):
    
    try: 
        users = load_json(USERS_FILE)
        user = None

        for u in users:
            if u["id"] == user_id:
                user = u
                break

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user_id": user_id,
            "avatar_url": user.get("avatar_url"),
            "has_profile_picture": bool(user.get("avatar_url"))
        }
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get list of available art styles for profile picture generation
@app.get("/profile-picture/styles")
async def get_available_styles():

    return {

    "available_styles": [
            {
                "name": "cartoon",
                "description": "Colorful cartoon/Disney-like style",
                "example_prompt": "friendly cartoon character with big eyes"
            },
            {
                "name": "realistic",
                "description": "Photorealistic human portraits",
                "example_prompt": "professional headshot of a person"
            },
            {
                "name": "anime",
                "description": "Japanese anime/manga art style",
                "example_prompt": "anime character with spiky hair"
            },
            {
                "name": "cyberpunk",
                "description": "Futuristic cyberpunk aesthetic with neon colors",
                "example_prompt": "cyberpunk hacker with glowing eyes"
            },
            {
                "name": "fantasy",
                "description": "Fantasy art with magical elements",
                "example_prompt": "elven wizard with mystical aura"
            },
            {
                "name": "minimalist",
                "description": "Clean, simple artistic style",
                "example_prompt": "simple geometric portrait"
            }
        ]
    }


# Allows user to upload their own profile picture not an AI generated one by the app.
@app.post("/user/{user_id}/profile-pictures/upload")
async def upload_profile_picture(user_id: str, file: UploadFile = File(...)):

    try:

        users = load_json(USERS_FILE)
        user = None
    
        # Checking if the user exists
        for u in users:
            if u["is"] == user_id:
                user = u
                break

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validating file type of the uploaded image
        # The .content_type has the MIME type from the browser which says what 
        # the file type is.
        # Example of MIME is text/html, audio/mp3, video/mp4
        # Before the slash is the general file type so 
        # like text/, image/, audio/ 
        # and to the right of the slash is the subtype which is a specfic file extension.
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        

        # Make sure the directory for the profile pictures exist before saving them.
        upload_dir = "backend/data/profile_pictures"
        os.makedirs(upload_dir,exist_ok=True)

        # Generating unique file names
        # "%Y%m%d_%H%M%S" is the format of the timestamp
        # "% Y % m % d_ % H % M % S"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # [-1] in .split('.')[-1] means file_exention will store the right 
        # most string so if you had an image called
        # 'balloon.png' then split('.') would turn it into ['balloon', 'png']
        # where the file extension will be the last element in the list which is why 
        # [-1] is used.
        file_extension = file.filename.split('.')[-1] if '.' else 'png'
        filename = f"uploaded_{user_id}_{timestamp}.{file_extension}"

        # Generating the file path for the uploaded image to be saved.
        filepath = os.path.join(upload_dir, filename)
        
        # Asyncerously save the uploaded profile picture.
        async with aiofiles.open(filepath, 'wb') as f:
            content = await file.read()
            await f.write(content)


        # Updating the URL for the user's avatar
        avatar_url = f"static/profile_images/{filename}"

        for i, u in enumerate(users):
            if u["id"] == user_id:
                user[i]["avatar_url"] = avatar_url
                break

        save_data(USERS_FILE, user)

        return {
            "success": True,
            "message": "Profile picture uploaded successfully",
            "avatar_url": avatar_url
        }



    except HTTPException:
        raise

    except Exception as e: 
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# Remove users profile pictures.
@app.post("/users/{user_id}/profile-picture")
async def delete_profile_picture(user_id: str):

    try:
        users = load_json(USERS_FILE)
        user = None
        user_index = None

        for i, u in enumerate(users):
            if u["id"] == user_id:
                user = u
                user_index = i
                break

        if not user: 
            raise HTTPException(status_code=404, detail="User not found")

        # Remove avatar URL from record
        if "avatar_url" in users[user_index]:
            users[user_index]["avatar_url"] = None

        save_data(USERS_FILE, users)

        return {
            "success": True,
            "message": "Profile Picture was removed successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    






@app.get("/health")
async def check_health():
    return {"Status": "healthy", "timestamp": get_timestamp()}


